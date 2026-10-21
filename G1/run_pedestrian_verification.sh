#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL="$SCRIPT_DIR/pedestrian_request_v1.xml"
QUERIES="$SCRIPT_DIR/pedestrian_queries.q"

if [[ -n "${VERIFYTA:-}" ]]; then
  VERIFYTA_BIN="$VERIFYTA"
elif command -v verifyta >/dev/null 2>&1; then
  VERIFYTA_BIN="$(command -v verifyta)"
elif [[ -x /Applications/UPPAAL-5.0.0.app/Contents/Resources/uppaal/bin/verifyta ]]; then
  VERIFYTA_BIN=/Applications/UPPAAL-5.0.0.app/Contents/Resources/uppaal/bin/verifyta
else
  printf 'verifyta not found. Set VERIFYTA to the executable path.\n' >&2
  exit 1
fi

printf 'Using verifyta: %s\n' "$VERIFYTA_BIN"
printf 'Model: %s\n' "$MODEL"
printf 'Queries: %s\n\n' "$QUERIES"

set +e
OUTPUT="$("$VERIFYTA_BIN" -t 1 -y "$MODEL" "$QUERIES" 2>&1)"
STATUS=$?
set -e

printf '%s\n' "$OUTPUT"

if (( STATUS != 0 )); then
  if [[ "$OUTPUT" == *"License does not cover verifier"* || "$OUTPUT" == *"License not found"* ]]; then
    printf '\nThe model file is ready, but this UPPAAL installation has no active verifier license.\n' >&2
    printf 'Activate an academic license in UPPAAL, then run this script again.\n' >&2
  fi
  exit "$STATUS"
fi
