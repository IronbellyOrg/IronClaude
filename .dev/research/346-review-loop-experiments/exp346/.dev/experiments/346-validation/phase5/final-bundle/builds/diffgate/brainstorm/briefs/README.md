T10 (`T10-R3-reviser.txt`) is EXCLUDED from the diffgate arm unless the coordinator rules otherwise: the loop writes no reviser brief at review 3 and halts on a review-3 FAIL.

# S1 brief kit for `/sc:spec-panel-diffgate` (issue #346)

These templates are the verbatim S1 briefs with only the substitutions the SPEC (section 4) and the owner rulings allow, plus the coordinator step briefs and the blindness audit. Install the variant first (`.dev/brainstorms/346-diffgate/INSTALL.md`).

## Templates

| Template | Source | Exact change |
|---|---|---|
| `T05-R1-reviewer.txt` | `source/T05-R1-reviewer-L11-699ae853.txt` | The command token `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` becomes `/sc:spec-panel-diffgate` with the same arguments plus `--diffgate-dir <one directory per replicate> --expect-round 1`. Nothing else. |
| `T06-R1-reviser.txt` | `source/T06-R1-reviser-L10-3bb70411.txt` | One line inserted, followed by one space, immediately before `Finish with worker_done`: the reviser line with `<N>` = 1 and the disposition file `.dev/orca-command-refactor/review/disposition.md`. |
| `T07-R2-reviewer.txt` | `source/T07-R2-reviewer-L11-aff19d65.txt` | As T05, with `--expect-round 2`. Both "any finding of any severity is FAIL" sentences stay. |
| `T08-R2-reviser.txt` | `source/T08-R2-reviser-L10-66468bab.txt` | As T06, with `<N>` = 2 and the disposition file `.dev/orca-command-refactor/review/disposition-round2.md`. |
| `T09-R3-reviewer.txt` | `source/T09-R3-reviewer-L11-1c9a7ec8.txt` | As T05, with `--expect-round 3`. The review-3 brief text stays verbatim, including "any finding of any severity is FAIL" (owner decision). |
| `T10-R3-reviser.txt` | `source/T10-R3-reviser-L10-458bdc00.txt` | No change (byte copy; the SPEC defines no change for T10). Excluded from the diffgate arm unless the coordinator rules otherwise (first line of this file). |
| `T11-blindness-audit.txt` | new, in the style of T05 | The mandatory blindness audit: a fresh plain `/sc:spec-panel` review of the final spec in a new session with no diffgate directory, saved to `review/blindness-audit.md`, each blocking finding classified as fix-written text the loop closed or text present since the original (base commit `2cb683f5`). |
| `S-begin.txt` | new | Coordinator step: `diffgate.py begin --dir <DIR> --doc <spec> --expect-round <N>`. |
| `S-check.txt` | new | Coordinator step: `diffgate.py check --dir <DIR> --report <review report>`, then append `<DIR>/close-r<N>.md` to the report. |
| `S-fixcheck.txt` | new | Coordinator step: `diffgate.py fixcheck --dir <DIR> --doc <spec> --map <disposition file>`. |

`source/` holds byte copies of the six originals so every template can be diffed inside this worktree.

The reviser line (owner ruling, design A: a reviser may write only the spec and its disposition file, so the fix map lives in the disposition file and the reviser runs only the read-only `--dry-run`):

> Your task list is <DIR>/reviser-brief-r<N>.md, not the whole report; after editing, run `uv run --no-project python ~/.claude/skills/sc-diffgate/scripts/diffgate.py fixcheck --dir <DIR> --doc .dev/orca-command-refactor/specs/orca-worker-contract-spec.md --map <disposition file> --dry-run` (read-only: it writes no file), put its `doc_sha:` line and one line per changed hunk (confirm or decline each candidate it prints) in a `## Diffgate fixmap` block inside <disposition file>, and repeat until it exits 0.

## Placeholders and dispatch-time fills

- `<one directory per replicate>` and `<DIR>` are the same directory, unique per replicate (for example under the replicate's report directory); never reuse it across replicates.
- `<N>` in the step briefs is the review or fix-cycle number; `<review report>` is the output file the review brief names (`review/spec-panel.md`, `review/spec-panel-round2.md`, `review/spec-panel-round3.md`); `<disposition file>` is the reviser's disposition file.
- The old repo-root path `OrcaCLICommandRefactor-Specs` inside the originals is substituted at dispatch time, as for every earlier arm.
- The replicate-specific counts and id ranges inside T07, T08 and T09 ("the 24 round-1 findings", "findings N1-N13", "round-2 finding N1-N13") are filled at dispatch exactly as the Arm B filled versions show (`/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/arm-b-briefs/filled-flg-r1-T07.txt`, `-T08.txt`, `-T09.txt`); that fill is not an edit of the brief text. Under diffgate the ids are `R1.<j>` and `R2.<j>`.
- No template passes an unattended flag: the variant has no `## Unattended mode` section.

## Dispatch order (one replicate)

`S-begin` r1, T05, `S-check` r1, T06, `S-fixcheck` r1, `S-begin` r2, T07, `S-check` r2, T08, `S-fixcheck` r2, `S-begin` r3, T09, `S-check` r3, then T11. A derived PASS at any `S-check` ends the loop early (the next `S-begin` would exit 4): go to T11. A review-3 FAIL ends with `halt: escalate`. Each review and revision session runs only read-only script calls (`status`, `check --dry-run`, `fixcheck --dry-run`); every writing call is one of the `S-*` steps (owner ruling).

## Scoring note

- `R3-proxy-all` (SPEC section 5) with the owner rulings: CRITICAL or MAJOR labels on the findings first raised in review 3 (deferred, demoted and over-`via`-cap included) and on the prior blocking findings marked `open`, `regressed` or `withdrawn` in review 3, plus every critical+major finding the script deferred, demoted or withdrew at ANY review from 1 to 3 (a blocker withdrawn at review 2, a CRITICAL deferred at review 2, a MAJOR demoted at review 1 or 2), counted as still open; each id once. For the treatment arm read `proxy_all` from `<DIR>/result-r3.json`. For the control and Arm B, recompute it by hand from their reports with the same cumulative function and publish it beside their historical values before scoring any treatment replicate.
- Early terminal review (a PASS at review 1 or 2, including `acceptance: scoped`): read that review's own `proxy_all` from `<DIR>/result-r<N>.json`, carry spec growth forward to the endpoint, never fabricate `result-r3.json`, and count the run as a clean pass only if that `proxy_all` is 0. A scoped PASS with deferred critical or major findings is NOT a clean pass.
- Growth: bytes of the spec after fix cycle 2 (or at the early terminal review, carried forward) against 57,763.
- Blindness audit (T11): each blocking finding is classified as fix-written text the loop closed (its cited text differs from the original spec at `2cb683f5`) or text present since the original. F3 fires when 2 or more blockers sit in fix-written text the loop closed.
- Validity exemption: the separate T11 blindness-audit session runs plain `/sc:spec-panel` by design; it does not void the replicate under the rule that voids a replicate when plain `/sc:spec-panel` ran (that rule covers the loop's review tasks only).
