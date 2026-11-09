#!/usr/bin/env bash
# Stage the brainstorm folder, inside a replay worktree, for ONE step of the S3 replay.
# The verbatim briefs name this folder, so every step uses the same path and the folder is reset each time:
#   <worktree>/.dev/brainstorms/20261105-170229-launch-level-hook/
# Usage: stage_step.sh <S3 package dir> <replay worktree> <step>
#   CHAIN  : start of a chained loop (Mode L): the 18 pipeline files + v0 as refactor-plan.md, nothing else.
#   H1     : review 1   input = v0
#   H2     : fix 1      input = v0 + ORIGINAL plan-review.md
#   H3     : review 2   input = v1 (original) + ORIGINAL plan-review.md
#   H4     : fix 2      input = v1 (original) + ORIGINAL plan-review.md + plan-review-2.md
#   H5     : review 3   input = v2 (original) + ORIGINAL plan-review.md + plan-review-2.md
# The original reviews are baseline OUTPUTS; they are staged only for the steps that read them in the original run.
set -eu -o pipefail
PKG=$1; WT=$2; STEP=$3
case "$WT" in /*) ;; *) echo "worktree path must be absolute" >&2; exit 2;; esac
git -C "$WT" rev-parse --git-dir >/dev/null 2>&1 || { echo "$WT is not a git worktree" >&2; exit 2; }
[ -f "$PKG/inputs/MANIFEST.sha256" ] || { echo "$PKG is not the S3 package" >&2; exit 2; }
(cd "$PKG/inputs" && sha256sum -c --quiet MANIFEST.sha256) || { echo "inputs/ failed its checksum" >&2; exit 1; }
DEST=$WT/.dev/brainstorms/20261105-170229-launch-level-hook
AD=$DEST/adversarial/adversarial
rm -rf "$DEST"; mkdir -p "$DEST"
cp -r "$PKG/inputs/brainstorm/." "$DEST/"          # includes refactor-plan.md = v0
R=$PKG/baseline/reviews; P=$PKG/baseline/plans
case "$STEP" in
  CHAIN|H1) ;;
  H2) cp "$R/plan-review.md" "$AD/";;
  H3) cp "$P/refactor-plan.v1.md" "$AD/refactor-plan.md"; cp "$R/plan-review.md" "$AD/";;
  H4) cp "$P/refactor-plan.v1.md" "$AD/refactor-plan.md"; cp "$R/plan-review.md" "$R/plan-review-2.md" "$AD/";;
  H5) cp "$P/refactor-plan.v2.md" "$AD/refactor-plan.md"; cp "$R/plan-review.md" "$R/plan-review-2.md" "$AD/";;
  *) echo "unknown step $STEP" >&2; exit 2;;
esac
echo "staged $STEP in $DEST"; (cd "$DEST" && find . -type f | sort | wc -l | sed 's/^/files: /'); wc -c "$AD/refactor-plan.md" | sed 's/^/plan bytes: /'
