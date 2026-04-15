#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PORT="${1:-8765}"
source ~/miniconda3/etc/profile.d/conda.sh
conda activate py311
python generate_nowcoder_ai_answer_bank.py >/dev/null
python build_interview_site.py >/dev/null
echo "本地网页已更新。访问地址: http://127.0.0.1:${PORT}"
cd site
python -m http.server "$PORT"
