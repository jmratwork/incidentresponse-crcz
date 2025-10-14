"""Command line entry point for the KYPO client."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from .client import KypoClient
from .config import ConfigurationError, KypoConfig, load_config


def _configure_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Interact with the KYPO API")
    parser.add_argument(
        "--config",
        help="Path to the KYPO YAML configuration file (defaults to config.yaml)",
    )
    parser.add_argument(
        "--env-prefix",
        default="KYPO_",
        help="Prefix used to look for environment variables (default: KYPO_)",
    )

    subcommands = parser.add_subparsers(dest="command", required=True)

    upload_parser = subcommands.add_parser(
        "upload-topology", help="Upload a topology YAML definition"
    )
    upload_parser.add_argument("topology", type=Path, help="Path to the topology YAML file")
    upload_parser.add_argument(
        "--metadata",
        type=str,
        help="Optional JSON string with metadata sent alongside the topology",
    )

    deploy_parser = subcommands.add_parser(
        "deploy-sandbox", help="Deploy a sandbox from an imported topology"
    )
    deploy_parser.add_argument("topology_id", help="Identifier of the imported topology")
    deploy_parser.add_argument(
        "--overrides",
        type=str,
        help="Optional JSON string merged into the sandbox payload",
    )

    subcommands.add_parser("authenticate", help="Verify that authentication works")

    return parser


def _parse_json_argument(value: Optional[str], description: str) -> Dict[str, Any]:
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise SystemExit(f"Invalid JSON for {description}: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit(f"{description} must be a JSON object")
    return parsed


def _load_configuration(args: argparse.Namespace) -> KypoConfig:
    try:
        return load_config(path=args.config, env_prefix=args.env_prefix)
    except ConfigurationError as exc:
        raise SystemExit(str(exc)) from exc


def main(argv: Optional[list[str]] = None) -> int:
    parser = _configure_parser()
    args = parser.parse_args(argv)

    config = _load_configuration(args)
    client = KypoClient(config)

    if args.command == "authenticate":
        token = client.authenticate()
        print("Authentication successful. Token acquired with length", len(token))
        return 0

    if args.command == "upload-topology":
        metadata = _parse_json_argument(args.metadata, "metadata")
        client.authenticate()
        result = client.upload_topology(args.topology, metadata=metadata)
        print(json.dumps(result, indent=2))
        return 0

    if args.command == "deploy-sandbox":
        overrides = _parse_json_argument(args.overrides, "overrides")
        client.authenticate()
        result = client.deploy_sandbox(args.topology_id, overrides=overrides)
        print(json.dumps(result, indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
