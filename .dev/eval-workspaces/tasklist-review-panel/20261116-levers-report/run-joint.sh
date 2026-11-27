#!/usr/bin/env bash
# Rebuilds REPORT.md and metrics.json from the score files of all tests (no hand-typed number). Run from this folder.
set -u -o pipefail
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 2
R=../20261114-recipe-ledger
S=../20261116-severity-test
uv run --no-project python -I joint_report.py --gt $R/holdout-gt --out . \
  --source sev=$S/results/scoring:$S/results/runs \
  --source holdout=$R/scoring-holdout:$R/runs-holdout:$R/runs-holdout-invalid \
  --source stronger=$R/scoring-stronger:$R/runs-stronger:$R/runs-stronger-invalid \
  --source stronger=$R/scoring-stronger-sole2:$R/runs-stronger-sole2:$R/runs-stronger-sole2-invalid \
  --source stronger=$R/scoring-stronger-wonder1:$R/runs-stronger-wonder1:$R/runs-stronger-wonder1-invalid \
  --source stronger=$R/scoring-stronger-sonsol:$R/runs-stronger-sonsol:$R/runs-stronger-sonsol-invalid \
  --source stronger=$R/scoring-stronger-wonsol:$R/runs-stronger-wonsol:$R/runs-stronger-wonsol-invalid \
  --source stronger=$R/scoring-stronger-emsol2:$R/runs-stronger-emsol2:$R/runs-stronger-emsol2-invalid \
  --arm-rule 'sev:sev1-z0-=Z0' --arm-rule 'sev:sev1-s-=S' \
  --arm-rule 'holdout:stage1-z0-=Z0' --arm-rule 'holdout:stage1-k-=K' --arm-rule 'holdout:stage1-rl-=RL' \
  --arm-rule 'stronger:stagesp-z0-sonnet-=A' --arm-rule 'stronger:stagesp-z0-=B' \
  --arm-rule 'stronger:stagese2-=sole2' --arm-rule 'stronger:stagesw1-=wonder1' --arm-rule 'stronger:stagess2-=sonsol' \
  --arm-rule 'stronger:stagesws-=wonsol' --arm-rule 'stronger:stagees2-=emsol2'
