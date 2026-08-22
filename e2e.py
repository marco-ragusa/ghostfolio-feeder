"""Run the feeder end-to-end against an official Ghostfolio container."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


COMPOSE = ["docker", "compose", "-f", "docker-compose.e2e.yml"]
ROOT = Path(__file__).resolve().parent


def run(command: list[str], **kwargs) -> None:
    """Run a command and stop on failure."""
    kwargs.setdefault("cwd", ROOT)
    subprocess.run(command, check=True, **kwargs)


def main() -> None:
    """Start a clean stack, run the E2E test, and remove the stack."""
    if not shutil.which("docker"):
        raise SystemExit("Docker with Compose is required to run the E2E test")

    environment = os.environ.copy()
    port = environment.get("GHOSTFOLIO_E2E_PORT", "3334")
    environment["GHOSTFOLIO_E2E_HOST"] = f"http://localhost:{port}"

    run(COMPOSE + ["down", "--volumes", "--remove-orphans"])
    try:
        run(COMPOSE + ["up", "--detach", "--wait"])
        run(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "app/tests",
                "-t",
                "app",
                "-p",
                "test_e2e.py",
                "-v",
            ],
            env=environment,
        )
    finally:
        run(COMPOSE + ["down", "--volumes", "--remove-orphans"])


if __name__ == "__main__":
    main()
