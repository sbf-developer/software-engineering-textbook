#!/usr/bin/env bash
set -euo pipefail

url="${HEALTH_URL:-http://127.0.0.1:8000/health}"
if [[ "$url" == "mock://ok" ]]; then
  printf '%s\n' ok
  exit 0
fi

if command -v curl >/dev/null 2>&1; then
  curl --fail --silent --show-error --max-time 2 "$url" >/dev/null
  printf '%s\n' ok
else
  printf '%s\n' "curl is required for a live health check" >&2
  exit 1
fi

