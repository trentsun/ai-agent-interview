#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PORT="${1:-8765}"
METHOD="${2:-pinggy}"

echo "[1/2] 请先在另一个终端运行: ./serve_interview_site.sh $PORT"
if [ "$METHOD" = "localtunnel" ]; then
  echo "[2/2] 正在启动临时公网访问(localtunnel)..."
  exec npx --yes localtunnel --port "$PORT"
else
  echo "[2/2] 正在启动临时公网访问(pinggy)..."
  exec ssh -p 443 -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R0:localhost:"$PORT" qr@a.pinggy.io
fi
