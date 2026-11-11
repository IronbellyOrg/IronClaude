# Handoff: step 1, bmad-spec `orca-observer` (issue 409)

**Spec:** `.dev/issues/409/bmad/spec-orca-observer/SPEC.md` + 9 companions + `.memlog.md` (50 entries). Source copy: Coder worktree `dashboard-bmad/_bmad-output/specs/spec-orca-observer/` (identical, `diff -rq`).

**What SPEC.md locks:** read-only observer; R1 data argv is only `worker-list` plus a one-time `skills list --json` discovery probe (outside the 5-per-cycle cap); 15 s cycle, 5 subprocesses, 8 MiB per call; Python + Rich `superclaude observe`-style subcommand, key-reader spike first, Textual only on failure; versioned additive-only JSON snapshot with a schema test (schema PROPOSED); staged releases R0 to R4 behind data gates; unknown never shown as 0/blank; no message bodies, prompts, files or credentials in any output; write-back is a future stage only; no TUIBBS dependency or copied code.

**Capabilities (12):** CAP-1 fixture replay (R0); CAP-2 worker ledger; CAP-3 "questions not observed" notice; CAP-4 completeness and freshness; CAP-5 separate facts, no inference; CAP-6 ID-anchored inspector; CAP-7 changes since last look; CAP-8 safe, legible rendering; CAP-9 lossless text export; CAP-10 JSON snapshot; CAP-11 question retention (R2); CAP-12 Decision Desk links (R3).

**Open questions (15, SPEC.md):** DIRECTION-SELECTED record; production-integration reading; command name; QUESTION-OBSERVATION fallback date; open owner decisions 6-9 (sample/acquisition permission, message exposure, what is a human question, multi-observer); licence opinion; TUIBBS as staff platform; write-back boundary change; snapshot row order; `read k of N Runs since start` placement (CONTRADICTION); undefined width matrix / x-width coordinates / 44-row contract; which `stage.*` subfield drives change detection and whether `stage.detail`/`.activity` enter the snapshot (CONTRADICTION).

**Validation:** Self-Validate pass 1 (coherence) FAIL, 10 blocking / 23 minor; pass 2 (preservation) FAIL, 4 blocking / 12 minor; all binding owner decisions confirmed applied. All 14 blocking fixed in one pass (fix cycle 1 of 2). Review 3 of 3 (fresh-context adversarial, coherence plus preservation, at the coordinator's request): **PASS**, 14/14 FIXED, 0 new blocking, 14 minor. All minors recorded in the review JSONs (`/tmp/orca-observer-pass{1,2,3}.json`, not copied), not fixed. Review 3 did not re-read the design package.

**UNVERIFIED:** stack-table facts (nothing run); AC-1..AC-10 mapping (from seed brief, not the issue); Orca timestamp clock/format; all message-row fields and the `check --all` candidate; `nextAction.kind` and `stage.*` value sets; `page.total` meaning; whether the owner's staging counts as DIRECTION-SELECTED; Orca `reply` sender rule (future stage).

**Contradictions recorded, not resolved:** `read k of N` placement; `stage.detail`/`.activity` in the snapshot (withheld, stricter reading). Notice wording unified to Change 28 (source T9 used a variant).

**Dropped / not done:** wrapper-only content (provenance comments, change-number bookkeeping, debate narration); design package not fully absorbed (binary exports never opened); project-context.md absent, skipped; issue's Go preference overridden by owner decision 2. No commit, push, PR or issue edit.
