#!/usr/bin/env python3
"""
EP-AGENT-001 — verify installed framework versions match the pinned requirements.
Setup check only. Does not run any study case and does not contact ExecutionProof.

Usage:
  python check_versions.py                 # check all four in the current interpreter
  python check_versions.py --framework crewai
Exit code: 0 if every checked framework PASSes, 1 otherwise.
"""
import argparse
import sys
from importlib import metadata

PINNED = {
    "openai_agents": ("openai-agents", "0.24.0"),
    "langgraph": ("langgraph", "1.2.15"),
    "crewai": ("crewai", "1.15.28"),
    "maf": ("agent-framework", "1.22.0"),
}
PYTHON_REQUIRED = (3, 11)


def check(framework: str) -> bool:
    package, pinned = PINNED[framework]
    try:
        installed = metadata.version(package)
    except metadata.PackageNotFoundError:
        print(f"FAIL  {framework:14s} {package}=={pinned}  installed: NOT INSTALLED")
        return False
    ok = installed == pinned
    print(f"{'PASS' if ok else 'FAIL'}  {framework:14s} {package}=={pinned}  installed: {installed}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--framework", choices=sorted(PINNED), help="check one framework only")
    args = parser.parse_args()

    py_ok = sys.version_info[:2] == PYTHON_REQUIRED
    print(f"{'PASS' if py_ok else 'FAIL'}  python         required 3.11.x  running: {sys.version.split()[0]}")
    targets = [args.framework] if args.framework else list(PINNED)
    results = [check(fw) for fw in targets]
    return 0 if (py_ok and all(results)) else 1


if __name__ == "__main__":
    sys.exit(main())
