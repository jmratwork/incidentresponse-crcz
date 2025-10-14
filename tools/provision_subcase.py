"""Provision KYPO sandboxes and apply Ansible automation for a given subcase."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from pathlib import Path
from typing import Dict, Optional

from kypo_cli.client import KypoClient
from kypo_cli.config import ConfigurationError, load_config

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INVENTORY = REPO_ROOT / "inventory.sample"
SUBCASE_TOPOLOGIES: Dict[str, Path] = {
    "1a": REPO_ROOT / "provisioning" / "subcase-1a-topology.yml",
    "1d": REPO_ROOT / "provisioning" / "subcase-1d-topology.yml",
}
SUBCASE_PLAYBOOKS: Dict[str, Path] = {
    "1a": REPO_ROOT / "provisioning" / "subcase-1a" / "site.yml",
    "1d": REPO_ROOT / "provisioning" / "subcase-1d" / "site.yml",
}


def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subcase", choices=sorted(SUBCASE_TOPOLOGIES.keys()), required=True)
    parser.add_argument("--config", help="Path to the KYPO configuration file")
    parser.add_argument(
        "--env-prefix",
        default="KYPO_",
        help="Prefix used to source environment overrides for KYPO configuration",
    )
    parser.add_argument(
        "--inventory",
        type=Path,
        default=DEFAULT_INVENTORY,
        help=f"Inventory file passed to ansible-playbook (default: {DEFAULT_INVENTORY})",
    )
    parser.add_argument(
        "--sandbox-overrides",
        help="JSON object merged into the sandbox deployment payload",
    )
    parser.add_argument(
        "--sandbox-name",
        help="Convenience flag that sets sandbox_defaults.name if provided",
    )
    parser.add_argument(
        "--ansible-extra-args",
        help="Additional arguments passed to ansible-playbook",
    )
    parser.add_argument(
        "--skip-ansible",
        action="store_true",
        help="Only interact with KYPO and skip the ansible-playbook execution",
    )
    parser.add_argument(
        "--skip-kypo",
        action="store_true",
        help="Skip KYPO interactions and only run ansible-playbook",
    )
    return parser.parse_args(argv)


def _load_kypo_config(path: Optional[str], env_prefix: str):
    try:
        return load_config(path=path, env_prefix=env_prefix)
    except ConfigurationError as exc:
        raise SystemExit(str(exc)) from exc


def _resolve_overrides(args: argparse.Namespace) -> Dict:
    overrides: Dict = {}
    if args.sandbox_overrides:
        try:
            overrides.update(json.loads(args.sandbox_overrides))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON for --sandbox-overrides: {exc}") from exc
    if args.sandbox_name:
        overrides.setdefault("name", args.sandbox_name)
    return overrides


def _run_ansible(playbook: Path, inventory: Path, extra_args: Optional[str]) -> None:
    if not playbook.exists():
        raise SystemExit(f"Playbook {playbook} does not exist")
    if not inventory.exists():
        raise SystemExit(f"Inventory file {inventory} does not exist")

    command = ["ansible-playbook", "-i", str(inventory), str(playbook)]
    if extra_args:
        command.extend(shlex.split(extra_args))

    print("Running:", " ".join(shlex.quote(part) for part in command))
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:  # pragma: no cover - environment specific
        raise SystemExit(
            "ansible-playbook command not found. Ensure Ansible is installed in the current environment"
        )


def main(argv: Optional[list[str]] = None) -> int:
    args = _parse_args(argv)

    topology_path = SUBCASE_TOPOLOGIES[args.subcase]
    playbook_path = SUBCASE_PLAYBOOKS[args.subcase]

    overrides = _resolve_overrides(args)

    if not args.skip_kypo:
        config = _load_kypo_config(args.config, args.env_prefix)
        client = KypoClient(config)
        client.authenticate()
        print(f"Uploading topology {topology_path}...")
        topology_response = client.upload_topology(topology_path, metadata={"subcase": args.subcase})
        topology_id = topology_response.get("id") or topology_response.get("topology_id")
        if not topology_id:
            raise SystemExit(
                "Could not determine topology identifier from KYPO response. "
                "Check the KYPO API response structure."
            )
        print("Topology uploaded with ID:", topology_id)
        print("Deploying sandbox...")
        sandbox_response = client.deploy_sandbox(topology_id, overrides=overrides)
        print("Sandbox deployment triggered:")
        print(json.dumps(sandbox_response, indent=2))
    else:
        print("Skipping KYPO interactions as requested.")

    if not args.skip_ansible:
        _run_ansible(playbook_path, args.inventory, args.ansible_extra_args)
    else:
        print("Skipping ansible-playbook execution as requested.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
