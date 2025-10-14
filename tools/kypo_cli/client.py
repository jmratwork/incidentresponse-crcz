"""HTTP client for KYPO operations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Mapping, MutableMapping, Optional

import requests

from .config import KypoConfig


class KypoClient:
    """Simple wrapper around the KYPO REST APIs."""

    def __init__(self, config: KypoConfig, session: Optional[requests.Session] = None) -> None:
        self.config = config
        self.session = session or requests.Session()
        self._token: Optional[str] = None

    # ---------------------------------------------------------------------
    # Authentication
    # ---------------------------------------------------------------------
    def authenticate(self) -> str:
        """Authenticate against the KYPO portal and store the bearer token."""

        payload = {
            "grant_type": "password",
            "client_id": self.config.client_id,
            "username": self.config.username,
            "password": self.config.password,
        }
        if self.config.client_secret:
            payload["client_secret"] = self.config.client_secret
        response = self.session.post(
            self.config.token_url,
            data=payload,
            timeout=30,
            verify=self.config.verify_tls,
        )
        response.raise_for_status()
        token = response.json()["access_token"]
        self._token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        return token

    # ------------------------------------------------------------------
    # Topology import
    # ------------------------------------------------------------------
    def upload_topology(self, topology_path: Path, metadata: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        """Upload a topology definition file to the KYPO portal."""

        if not topology_path.exists():
            raise FileNotFoundError(f"Topology file {topology_path} does not exist")
        files = {"file": topology_path.open("rb")}
        data: MutableMapping[str, Any] = {"metadata": json.dumps(metadata or {})}
        try:
            response = self.session.post(
                self.config.topology_import_url,
                files=files,
                data=data,
                timeout=60,
                verify=self.config.verify_tls,
            )
        finally:
            files["file"].close()
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    # Sandbox deployment
    # ------------------------------------------------------------------
    def deploy_sandbox(self, topology_id: str, overrides: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        """Trigger a sandbox deployment for the provided topology."""

        payload: Dict[str, Any] = {"topology_id": topology_id}
        payload.update(self.config.sandbox_defaults)
        if overrides:
            payload.update(overrides)
        response = self.session.post(
            self.config.sandbox_deploy_url,
            json=payload,
            timeout=60,
            verify=self.config.verify_tls,
        )
        response.raise_for_status()
        return response.json()


__all__ = ["KypoClient"]
