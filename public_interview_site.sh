#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PORT="${1:-8765}"
echo "[1/2] 请先在另一个终端运行: ./serve_interview_site.sh $PORT"
echo "[2/2] 正在启动临时公网访问(localtunnel)..."
exec npx --yes localtunnel --port "$PORT"
