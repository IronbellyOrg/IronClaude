# QA Report: Research Gate fix verification (Gate 1, cycle 0)

**Topic:** git pre-push hook semantics for the L2 launch-level guard (issue #441)
**Date:** 2026-11-08
**Phase:** research-gate (fix-cycle verification)
**Fix cycle:** 1 (verifies the cycle 0 fixes)
**Fix authorization:** false (no research file was edited)
**Inputs:** `qa/qa-consolidated-findings-phase3-cycle0.md` (blocking B1-B4), `qa/qa-research-fix-log.md`, `research/01`-`04`, `research/research-notes.md`

---

## Overall Verdict: PASS

All four blocking findings (B1-B4) are fixed and correct against their cited sources. No new CRITICAL or IMPORTANT issue was found. Four new MINOR notes are recorded below; they do not fail the gate.

## Blocking findings: fix verification

| # | Original finding | Fixed | Evidence | New issue |
|---|---|---|---|---|
| B1 | 04 has no Key Takeaways section | yes | `research/04-empirical-git-prepush-experiments.md` lines 2233-2245 hold a `## Key Takeaways` section with 9 bullets. It sits between the cross-check tally and `## Gaps and Questions`. Each bullet was checked against its experiment: E12/E13/E14 (lines 851-853: empty stdin when up to date, dry-run delivers the real records without moving a ref, `--no-verify` skips the hook); E19 (lines 1051-1068: in a mixed push, one refused ref aborts the whole push); E23 (lines 1293-1294); E26 (line 1421: `--atomic` behaves the same as non-atomic); E28 (lines 1496-1530: HOME/PATH pass-through, `/usr/lib/git-core` prepended to PATH); E28c (lines 1521-1522: `uv=UV-ABSENT`); E30 (line 1654: hook looked up in the common dir, a hook in the private dir is ignored); E31 (line 1699); F2 (line 1982); F4 (lines 2126, 2215). No bullet claims more than its source shows | M4 (MINOR) |
| B2 | Sub-question (b), push via other tools, is untested and not routed to Phase 4 | yes | Option (b) was applied. 04 lines 2265-2270 add `ROUTE web-01: (b) other tools`, which names pygit2/libgit2, dulwich, GitPython and JGit with a doc or source location for each, all tagged [UNVERIFIED] and marked not fetched. 02 Gap 6 (line 264) points to this route. `research-notes.md` line 73 adds (b) to the web-01 scope. I re-checked why option (a) could not be used: `uv pip list` shows none of dulwich, pygit2 or GitPython; none is in `/usr/lib/python3/dist-packages` or the uv wheels cache; `command -v jgit java` finds nothing | M2 (MINOR) |
| B3 | 03 wrongly says the design line-487 corpus is absent | yes | A fresh Glob of `.dev/brainstorms/2026110[56]*/**/*.md` returned 48 files: 25 under `20261105-170229-launch-level-hook/` and 23 under `20261105-024132-issue-claim-orca-worktree-flag/`. This matches 03 line 22. `git ls-files` lists 27 tracked files under the corpus and 0 under `20261106-l2-prepush-decisions/`. `git log -1` on the corpus gives `4f7e3e7e` (#414), which also matches. The quotes cited at 03 line 24 were confirmed in their files: `merged-requirements.md:1384`, `adversarial/adversarial/refactor-plan.md:1158` and `variant-1-opus-architect.md:135`. The [STALE DOC] entry (line 318) now cites only the 19.6 `20261106-l2-prepush-decisions/` files. A "Not stale" line (319) was added, and the open question (line 301) and the Summary (line 328) were corrected. The claim that no D19 row rests on this corpus holds: the "source artifact absent" rows cite 19.6 run-4 or "Q artifacts" | M1 (MINOR) |
| B4 | 01 §4 item 5 omits that a human with no uv on PATH cannot push to main/master, and 04's "absolute uv path" remedy does not work | yes | Read of `src/superclaude/hooks/scripts/launch-job-identity.sh`: lines 20-24 exit early only for no arguments or the single argument `hook`; line 25 runs `command -v uv`; lines 52-53 print `launch job: UV is required for this invocation` and `exit 2`; line 566 runs `exec uv run --no-project python -I -c ...`. So `identify` without uv on PATH exits 2 even when no store exists, which the hook treats as unknown, and unknown refuses main/master. 01 line 195 now says this. 01 line 196 explains correctly why an absolute uv path alone fails (lines 25 and 566 look uv up on PATH). It lists options (i)-(iii) and correctly notes that (ii) does not cover a human who also has a store. A Key Takeaways bullet was added at 01 line 203. In 04, the E28 uv bullet (line 1530) and the open question (line 2259) are corrected and point to 01 §4 item 5 | M3, M4 (MINOR) |

Open blocking findings after this cycle: 0, down from 4. Monotonicity holds (`|F_1| = 0 < |F_0| = 4`), and no item regressed.

## New issues introduced or exposed by the fixes (all MINOR, notes only)

| # | Severity | Location | Issue | Suggested fix |
|---|---|---|---|---|
| M1 | MINOR | `research/03` line 22 | Line 22 says every file that design line 487 names is present, and lists `adversarial/adversarial/refactor-plan.md`. Line 487 names a bare `refactor-plan.md`, and no such file exists at the corpus root; it exists only under `adversarial/adversarial/`. The conclusion holds, but the wording is imprecise | Say that line 487's bare `refactor-plan.md` resolves to `adversarial/adversarial/refactor-plan.md` |
| M2 | MINOR | `research/02` line 190 | This line still says the other-tools question "belongs to the L2 hook-semantics research" and has no pointer to the new route. Gap 6 (line 264) does have the pointer | Add "see 04 Gaps, ROUTE web-01: (b)" |
| M3 | MINOR | `research/01` line 195 | The human-without-uv behaviour is labelled "inferred", but §7 line 157 of the same file already records an observed direct call ("no uv on PATH -> exit 2"). The evidence is understated, not overstated | Cite §7 line 157 as the observed evidence |
| M4 | MINOR | `research/04` line 1530 | The corrected bullet still contains the earlier wrong reference "(E9-E11)"; the relevant experiment is E19. This is the earlier note N21 carried into an edited line | Change "(E9-E11)" to "(E19)" |

## Research-gate checklist re-applied to the changed sections

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | File inventory | PASS | 01-04 and `research-notes.md` each still show Status: Complete and have a Summary section. The edits only added content and removed no section |
| 2 | Evidence density | PASS | Each new bullet in 04 Key Takeaways cites an experiment ID and its record exists at the cited line. The new 01 bullets cite `launch-job-identity.sh` lines 19-25, 52-53 and 566, all confirmed by Read. The re-check in 03 cites three file:line quotes, all confirmed |
| 3 | Scope coverage | PASS | `launch-job-identity.sh` (EXISTING_FILES) is now covered for the no-uv path. Sub-question (b), other tools, is routed to web-01 in `research-notes.md` line 73 |
| 4 | Doc cross-validation tags | PASS | The new library claims in the ROUTE line are tagged [UNVERIFIED]. The [STALE DOC] entry in 03 was narrowed and the "Not stale" line added. No changed doc claim is untagged |
| 5 | Contradiction resolution | PASS | 04 (E28 uv bullet and open question) and 01 §4 item 5 now agree on the uv remedy. 03 no longer contradicts the Glob and `git ls-files` results. The "inferred" vs "observed" wording in 01 is M3, a MINOR note |
| 6 | Gap severity | PASS | The only new gap is the web-01 (b) route, which is assigned to Phase 4 and so is not a gap that would make the synthesis hallucinate. No CRITICAL or IMPORTANT gap remains |
| 7 | Depth appropriateness | PASS | Standard tier: file-level coverage is intact. 04 Key Takeaways now summarise the end-to-end push experiments |
| 8 | Integration point coverage | PASS | The hook-to-`identify` integration point, including the PATH/uv dependency and exit-code mapping, is documented in 01 §4 item 5 and in 04 E28 |
| 9 | Pattern documentation | PASS | 01 options (i)-(iii) document the hook-invocation pattern choices. 03 still records the no-replace publication pattern |
| 10 | Incremental writing compliance | PASS | The fixes appear as targeted insertions (new sections and bullets, a correction paragraph); the files were not rewritten in one shot. The fix log maps each change to a file and section |

## Summary

- Blocking findings verified: 4 of 4 fixed and correct (B1-B4)
- Blocking findings still open: 0
- New CRITICAL: 0. New IMPORTANT: 0. New MINOR: 4 (M1-M4, notes only)
- Checklist re-application: 10 of 10 PASS
- Issues fixed in-place: 0 (fix authorization false)

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 20 | Grep: 5 | Glob: 2 | Bash: 3 (read-only: `git ls-files`/`git log -1`, `uv pip list` plus package-path checks, `command -v jgit java`). No web research.

## Recommendations

- Proceed to Phase 4 (web research). web-01 must include the (b) other-tools route.
- The M1-M4 notes are optional wording fixes; they do not block synthesis.

## QA Complete

