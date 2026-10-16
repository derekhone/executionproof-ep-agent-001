#!/usr/bin/env bash
# EP-AGENT-001 — environment setup (one venv per framework)
# STATUS: DESIGN ONLY. Installing frameworks is setup, not study execution.
# This script does NOT run any study case and does NOT contact ExecutionProof.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON="${PYTHON:-python3.11}"

declare -A PINS=(
  [openai_agents]="openai-agents==0.24.0"
  [langgraph]="langgraph==1.2.15"
  [crewai]="crewai==1.15.28"
  [maf]="agent-framework==1.22.0"
)

command -v "$PYTHON" >/dev/null 2>&1 || { echo "ERROR: $PYTHON not found (Python 3.11.x required)"; exit 1; }

for fw in openai_agents langgraph crewai maf; do
  venv="$ROOT/.venv-$fw"
  echo "=== [$fw] creating venv at $venv"
  "$PYTHON" -m venv "$venv"
  start=$(date +%s)
  "$venv/bin/python" -m pip install --quiet --no-deps --require-hashes -r "$ROOT/locks/$fw.lock"
  "$venv/bin/python" -m pip check
  end=$(date +%s)
  echo "=== [$fw] installed ${PINS[$fw]} (hash-locked) in $((end - start))s"
  "$venv/bin/python" "$ROOT/scripts/setup/check_versions.py" --framework "$fw"
done

echo "Done. All four venvs installed from hash-locked locks/<fw>.lock (see requirements.lock)."
