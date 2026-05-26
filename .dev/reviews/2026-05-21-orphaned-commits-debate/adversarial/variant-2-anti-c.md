# Variant 2 — ANTI-Option-C ("Re-apply selectively, do NOT cherry-pick fcd28bfa")

**Position**: Reject Option C as stated. Instead: cherry-pick `1550ea5f` and
`e1c458bd` (both conflict-free), extract ONLY the `.markdownlint.json` hunk
from `fcd28bfa` and apply as a NEW commit, abandon the rest of `fcd28bfa`
(superseded by PR #70 + commit `9316d2ee`).

## Argument

**1. `fcd28bfa` is structurally unsafe to cherry-pick.** Empirical
measurement: `git diff fcd28bfa HEAD -- src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
reports **273 lines of divergence**. The HEAD version contains 4 references
to `test_is_wrong` (a new output contract field added by commit `9316d2ee`);
fcd28bfa's SKILL.md has zero. A naive cherry-pick would either conflict on
nearly every line OR silently overwrite the user's newer work. Even with
careful manual conflict resolution, the burden of reviewing 273 lines × 10
files (= ~2700 lines of merge resolution) substantially exceeds the cost of
re-applying the genuinely net-new portion.

**2. The SoT content from `fcd28bfa` is already in master via a different
path.** PR #70 (`6633c54f feat: sc:troubleshoot v2 — tiered protocol + 2
custom agents + dispatch wiring`) landed:
- `src/superclaude/skills/sc-troubleshoot-protocol/` (SKILL.md + 5 refs)
- `src/superclaude/agents/{confidence-calibrator,evidence-validator}.md`
- `src/superclaude/commands/troubleshoot.md`

All of these have HEAD versions that are *more advanced* than fcd28bfa's
versions. Cherry-picking fcd28bfa adds zero net value for these 9 of 10
files; it only adds risk of regression. Only the 10th file —
`.markdownlint.json` — is genuinely net-new content.

**3. The clean cherry-picks have empirically zero intervening commits.**
`git log --oneline 1550ea5f..HEAD -- src/superclaude/cli/eval/commands.py
tests/cli/eval/test_eval_group.py` is **empty**. Same for `e1c458bd..HEAD --
src/superclaude/hooks/scripts/freshness-pre-edit.sh`. Both should
cherry-pick cleanly with no conflict. The risk profile of cherry-picking
those two SPECIFIC commits is genuinely near-zero; only fcd28bfa is the
problem.

**4. Re-applying the .markdownlint.json hunk is trivial.** It's 9 lines, one
file, no overlap with any other work. A fresh single-purpose commit ("chore:
add .markdownlint.json with line_length 160") is cleaner to review, has a
focused commit message that doesn't carry the SoT-restore baggage from
fcd28bfa, and doesn't risk dragging in the 273-line skill-file divergence.

## Conceded weaknesses

- Loses the commit-message rationale from fcd28bfa (recoverable from this
  debate transcript and the orphan branch which still exists locally).
- Three operations (2 cherry-picks + 1 fresh commit) instead of one bulk
  cherry-pick — slightly more git ceremony.
- Future grep on commit messages won't find a unified "SoT cleanup" commit.
