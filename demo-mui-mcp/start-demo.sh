#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ ! -d node_modules ]]; then
  echo "Dipendenze mancanti: eseguo npm install..."
  npm install
fi

echo "Demo disponibile su http://127.0.0.1:5175"
echo "Premi Ctrl+C per arrestarla."
npm run dev -- --host 127.0.0.1
