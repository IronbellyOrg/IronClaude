# Round 2: Variant 3 Rebuttal (opus:refactorer)
<!-- Returned by a read-only advocate agent; persisted verbatim by the orchestrator (trailing DONE/NEXT table omitted). -->

## Response to criticisms

- **R3-F1 labelled `necessary` (V1, V2):** I concede, as I did in Round 1. It is **drift**. The finding itself holds: shell evidence section 5 confirms the import crash.
- **R3-F4 overreaches on the pr-submit scripts (V1):** I concede. Every bare `gh repo view` runs only after the `origin` lookup comes back empty (poll-augment-review.sh:21-22, poll-ci-checks.sh:34-35, retrigger-review.sh:49-50, reply-resolve-thread.sh:56-57). source.md limits the work to CLAUDE.md. What is left of R3-F4 is the in-scope conflict: CLAUDE.md:50 says `gh pr create --repo <repo>`, which fails plan:117, while plan:113 says to keep that sentence. That part stays medium.
- **Severity inflated (V1):** I accept this in part. After the concessions below, 4 of my 9 findings are medium (F1, F2, F3, the CLAUDE.md:50 half of F4). F5 drops to low.
- **R3-F7/F8 are conjecture; the `.venv` claim is only inferred (V1):** I concede. Both stay low. I withdraw the `.venv` claim because nothing shows it happens.
- **No deviation-resolution section (V2, S-001):** I concede. I now prefer V1's 14-row table, merged with V2's reproduction of both searches.
- **S3 dispute asserted without a coverage walk (V2):** I concede in part. Once the script fallback is out of scope, the S3 dispute rests only on CLAUDE.md:50 against plan:117, which I verified by Read. It needs no coverage walk.

## Updated assessment

- **V1:** Its Round 2 concessions (the D-001 cell, C-003, X-004) close the main gaps. V1 is now the best-calibrated card, and its coverage table should be the base for S-001.
- **V2:** R2-F1 stands, and its search reproduction is sound. R2-F3 survives only as a low completeness note.
- **V3:** It keeps the lead on Task 2 executability (C-001, C-002, C-003).

## New evidence

- **sc-implement-protocol/SKILL.md:111, :125.** The executor builds its review snapshot in a temporary index and is told "Do not `git add` to the user index for this snapshot." Only `.dev/tasks/` is staged (plan:29, :179).
  - So plain `git diff` at plan:119, :148 and :178 is vacuous only if someone stages source files by hand.
  - I downgrade R3-F5 from the diff analysis's High to **low hardening**. Changing to `git diff HEAD` is still cheap, so I keep the recommendation.
- **tests/core/test_claude_md_routing_block.py:14-16.** `_CORE = _REPO / "src/superclaude/core"` and `_CLAUDE = _CORE / "CLAUDE.md"`, which confirms the orchestrator's A-006 fact.
- **CLAUDE.md:70.** It says "explicit `--repo` on every invocation", which confirms V1's R1-4. It belongs in C-004.
- **Plan:117 check.** `grep -n 'gh ' CLAUDE.md` covers the whole file and not just the fork section. That makes V1's R1-5 (limit to the section, match `gh` as a whole word) required, not optional.
- **R2-F1.** I do **not** contest medium. Shell evidence lines 8-9 show `is-shallow=false` and `id -u=1000`. A skip in this checkout therefore has some other cause, and the rerun at plan:176 cannot be checked after the fact.

## Final per-point positions

| Point | Preferred variant | Changed since Round 1? |
|---|---|---|
| S-001 | V1, merged with V2's search reproduction | yes (was V2) |
| S-002 | V3, with F5 now low | no |
| S-003 | V3 on S1; V1 on F1 and F3; my S3 dispute narrowed to CLAUDE.md:50 | yes |
| C-001 | V3 content with V1's `drift` label | no |
| C-002 | V3 | no |
| C-003 | V3, with V1's eval_runner.py:294-295 guard note folded in | no |
| C-004 | V3's CLAUDE.md:50 point plus V1's R1-4 (:70) and R1-5 (section-limited, whole-word grep); scripts out of scope | no |
| X-001 | V1 (scripts out of scope; CLAUDE.md:50 moved into C-004) | yes |
| X-002 | V3 | no |
| X-003 | V1 (`drift`) | no |
| X-004 | V3 (medium) | no |
| X-005 | V3 (medium) | no |

## Shared assumptions

- **A-001: QUALIFY.** Local `master` exists (d953b983) but can fall behind `origin/master`. The current script already uses it, so the plan should say this choice is deliberate.
- **A-003: ACCEPT.** Shell section 5 shows the registered load runs no git command and writes no files.
- **A-004: ACCEPT.** pyproject.toml:108-109 sets `testpaths = ["tests"]` and `test_*.py`, so `tests/unit/` is collected.
- **A-006: ACCEPT** (was QUALIFY). Both tests read `src/superclaude/core/CLAUDE.md` (test_claude_md_routing_block.py:15-16), not the root file the plan edits. The two `.dev/worktrees` hits in tests are Search A rows that Task 8 classifies. They are tracked, not pinned.
