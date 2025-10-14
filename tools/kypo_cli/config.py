"""Configuration utilities for the KYPO CLI."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Mapping, MutableMapping, Optional
from urllib.parse import urljoin

import yaml

_DEFAULT_FILENAMES = ("config.yaml", "config.yml")
_ENV_PREFIX_DEFAULT = "KYPO_"


@dataclass
class EndpointSettings:
    """Holds the URL templates for the KYPO endpoints."""

    token: str = "/auth/realms/{realm}/protocol/openid-connect/token"
    topology_import: str = "/api/v1/topologies/import"
    sandbox_deploy: str = "/api/v1/sandboxes"


@dataclass
class KypoConfig:
    """Represents the configuration required to talk to the KYPO API."""

    portal_url: str
    username: str
    password: str
    realm: str = "academy"
    client_id: str = "kypo-web"
    client_secret: Optional[str] = None
    verify_tls: bool = True
    endpoints: EndpointSettings = field(default_factory=EndpointSettings)
    sandbox_defaults: Dict[str, Any] = field(default_factory=dict)

    @property
    def token_url(self) -> str:
        return urljoin(self.portal_url, self.endpoints.token.format(realm=self.realm))

    @property
    def topology_import_url(self) -> str:
        return urljoin(self.portal_url, self.endpoints.topology_import.format(realm=self.realm))

    @property
    def sandbox_deploy_url(self) -> str:
        return urljoin(self.portal_url, self.endpoints.sandbox_deploy.format(realm=self.realm))


_ENV_MAPPING: Mapping[str, str] = {
    "portal_url": "PORTAL_URL",
    "username": "USERNAME",
    "password": "PASSWORD",
    "realm": "REALM",
    "client_id": "CLIENT_ID",
    "client_secret": "CLIENT_SECRET",
    "verify_tls": "VERIFY_TLS",
    "token": "TOKEN_ENDPOINT",
    "topology_import": "TOPOLOGY_ENDPOINT",
    "sandbox_deploy": "SANDBOX_ENDPOINT",
}


class ConfigurationError(RuntimeError):
    """Raised when the KYPO configuration is invalid."""


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    raise ValueError(f"Cannot coerce {value!r} to boolean")


def _load_yaml(path: Path) -> MutableMapping[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as handler:
            loaded = yaml.safe_load(handler) or {}
    except yaml.YAMLError as exc:  # pragma: no cover - sanity guard
        raise ConfigurationError(f"Invalid YAML in configuration file {path}: {exc}") from exc
    if not isinstance(loaded, MutableMapping):
        raise ConfigurationError(f"Configuration file {path} must contain a mapping at the top level")
    return loaded


def _resolve_config_path(path: Optional[str]) -> Optional[Path]:
    if path:
        candidate = Path(path)
        if not candidate.exists():
            raise ConfigurationError(f"Configuration file {candidate} does not exist")
        return candidate
    for filename in _DEFAULT_FILENAMES:
        candidate = Path(filename)
        if candidate.exists():
            return candidate
    return None


def _merge_env_config(config: MutableMapping[str, Any], env_prefix: str) -> None:
    for key, env_key_suffix in _ENV_MAPPING.items():
        env_key = f"{env_prefix}{env_key_suffix}"
        if env_key not in os.environ:
            continue
        value = os.environ[env_key]
        if key == "verify_tls":
            value = _as_bool(value)
        if key in {"token", "topology_import", "sandbox_deploy"}:
            endpoints = config.setdefault("endpoints", {})
            endpoints[key] = value
        else:
            config[key] = value


def load_config(path: Optional[str] = None, env_prefix: str = _ENV_PREFIX_DEFAULT) -> KypoConfig:
    """Load the KYPO configuration from a YAML file and environment variables."""

    config_path = _resolve_config_path(path or os.environ.get(f"{env_prefix}CONFIG"))
    data: MutableMapping[str, Any] = {}
    if config_path:
        data.update(_load_yaml(config_path))
    _merge_env_config(data, env_prefix)

    missing = [key for key in ("portal_url", "username", "password") if key not in data]
    if missing:
        raise ConfigurationError(
            "Missing required KYPO configuration values: " + ", ".join(missing)
        )

    endpoints_mapping = data.get("endpoints", {})
    if not isinstance(endpoints_mapping, Mapping):
        raise ConfigurationError("'endpoints' must be a mapping")

    endpoints = EndpointSettings(**{**EndpointSettings().__dict__, **dict(endpoints_mapping)})

    verify_tls = data.get("verify_tls", True)
    if isinstance(verify_tls, str):
        verify_tls = _as_bool(verify_tls)

    sandbox_defaults = data.get("sandbox_defaults", {})
    if sandbox_defaults and not isinstance(sandbox_defaults, Mapping):
        raise ConfigurationError("'sandbox_defaults' must be a mapping if provided")

    return KypoConfig(
        portal_url=str(data["portal_url"]),
        username=str(data["username"]),
        password=str(data["password"]),
        realm=str(data.get("realm", "academy")),
        client_id=str(data.get("client_id", "kypo-web")),
        client_secret=data.get("client_secret"),
        verify_tls=bool(verify_tls),
        endpoints=endpoints,
        sandbox_defaults=dict(sandbox_defaults),
    )


__all__ = ["EndpointSettings", "KypoConfig", "ConfigurationError", "load_config"]
