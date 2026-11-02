# v5.0.0 release evidence

These files are the evidence and decisions behind the 5.0.0 release. They were written in worktrees that were deleted on 2026-11-02 before being committed, and were rebuilt on 2026-11-02 by replaying the Write and Edit calls recorded in the Claude Code session transcripts that created them (only calls that did not return an error were applied, in order).

| File | Original location | Rebuilt from |
|---|---|---|
| `RELEASE-READINESS.md` | `.dev/worktrees/release-readiness/.dev/release-readiness/` | release-readiness session `777018c5` |
| `DECISIONS.md` | same folder | coordinator session `514abb0c`; a repeated replay produced duplicate rows, so each row keeps its latest text |
| `A3-RESULT.md` | same folder, `a3-check/RESULT.md` | release-readiness session `6fdd347c` |
| `QA-LOOP-FINDINGS.md` | `.dev/worktrees/qa-loop-investigation/.dev/qa-loop-investigation/FINDINGS.md` | QA-loop session `8917d256` |

Files those reports cite under their old folders (for example `a3-check/install-state.md`, `evaluation/run3/REPORT.md`, the `debate/` folders) were not rebuilt; treat those citations as pointing at deleted files.

The release gate is section 6.3 of `RELEASE-READINESS.md` (checks G1-G9).
