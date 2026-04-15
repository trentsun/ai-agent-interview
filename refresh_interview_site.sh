#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
source ~/miniconda3/etc/profile.d/conda.sh
conda activate py311
python collect_nowcoder_ai_app_interviews.py
python analyze_nowcoder_ai_app_interviews.py
python generate_nowcoder_ai_answer_bank.py
python build_interview_site.py
