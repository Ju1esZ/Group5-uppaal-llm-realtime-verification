#!/usr/bin/env bash

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STRICT=false

if [[ "${1:-}" == "--strict" ]]; then
  STRICT=true
fi

missing=0
present=0

check_exact() {
  local owner="$1"
  local path="$2"
  local description="$3"

  if [[ -e "$ROOT/$path" ]]; then
    printf 'OK      %-3s %-42s %s\n' "$owner" "$path" "$description"
    present=$((present + 1))
  else
    printf 'MISSING %-3s %-42s %s\n' "$owner" "$path" "$description"
    missing=$((missing + 1))
  fi
}

check_glob() {
  local owner="$1"
  local pattern="$2"
  local description="$3"

  if compgen -G "$ROOT/$pattern" >/dev/null; then
    printf 'OK      %-3s %-42s %s\n' "$owner" "$pattern" "$description"
    present=$((present + 1))
  else
    printf 'MISSING %-3s %-42s %s\n' "$owner" "$pattern" "$description"
    missing=$((missing + 1))
  fi
}

printf 'Project delivery audit\n'
printf 'Repository: %s\n\n' "$ROOT"

check_exact G1 'G1/01_系统需求与模型边界.md' 'requirements baseline'
check_exact G1 'G1/02_Prompt对照实验方案.md' 'experiment design'
check_exact G1 'G1/03_CTL属性与验收矩阵.md' 'property matrix'
check_exact G1 'G1/04_版本管理与评审规范.md' 'version and review rules'
check_exact G1 'G1/05_协作计划与进度看板.md' 'coordination board'
check_exact G1 'G1/06_个人学习笔记.md' 'personal study notes'
check_exact G1 'G1/prompts/P0_基础Prompt.md' 'P0 frozen prompt'
check_exact G1 'G1/prompts/P1_时间自动机知识Prompt.md' 'P1 frozen prompt'
check_exact G1 'G1/prompts/P2_安全约束Prompt.md' 'P2 frozen prompt'

check_exact G2 'G2/AI使用记录.md' 'LLM usage log'
check_glob G2 'G2/raw/*/*/response.md' 'raw responses'
check_exact G3 'G3/错误清单.md' 'structure and timing error list'
check_exact G4 'G4/并发错误案例.md' 'synchronization error cases'
check_exact G5 'G5/traffic_light_v1.xml' 'v1 model'
check_exact G5 'G5/queries.q' 'v1 queries'
check_exact G5 'G5/UPPAAL_验证结果.txt' 'v1 verification result'
check_glob G6 'G6/*v3*.xml' 'v3 fault model'
check_glob G7 'G7/queries/*.q' 'safety and liveness queries'
check_glob G7 'G7/*验证结果*.md' 'verification summary'
check_glob G8 'G8/*.csv' 'experiment statistics'
check_glob G8 'G8/queries/*.q' 'time-bound queries'

printf '\nSummary: %d present, %d missing\n' "$present" "$missing"

if $STRICT && (( missing > 0 )); then
  exit 1
fi

exit 0
