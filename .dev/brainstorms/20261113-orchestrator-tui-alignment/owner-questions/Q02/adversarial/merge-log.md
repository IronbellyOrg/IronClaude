# Merge Log: Q2

## Metadata

- Base: Variant 2 (proposal-B), `variant-2-original.md`, used as the frame
- Core answer: Variant 3 (proposal-C), `variant-3-original.md`, per Change 1
- Other source: Variant 1 (proposal-A), `variant-1-original.md` (A-002 wording, U-001 note)
- Plan: `refactor-plan.md` (6 changes, auto-approved 2026-11-14)
- Context read: `debate-transcript.md`, `../question.md`, and `merged-requirements.md` lines 331, 604, 719 and 811 (the lines the plan cites for Change 3)
- Output: `../merged-proposal.md`
- Merge date: 2026-11-14
- Carried rule: the watcher-to-orchestrator handoff is unbuilt; the merged text does not claim it exists.

## Changes Applied

### Change 1: replace the core answer with claim-only and a one-issue acceptance

- Status: Applied
- Before: title and Answer kept the default `worktree` level as a deliberate chain, gated on OB-H1 item 1 and item 5, OB-H2 and OB-H3, with an acceptance covering both sessions.
- After: title and Answer say `--pipeline none` (claim only, no worktree, no second agent) and a written acceptance for the one FU-1 test issue only; one added sentence says FU-1 waits for every listed precondition (Change 2 precondition style).
- Provenance: Variant 3 "Answer" (debate points C-001, C-002, X-002, X-003, 3 of 3).
- Consequential adjustment: base cost bullets 2 to 4 (a worktree and agent per approval, all four ship gates, the design contradiction) describe the default level and fall with it. Variant 3's cost bullets 2 to 4 were carried in their place, matching the plan's rollback target ("`variant-3-original.md` plus Changes 3 to 5"). Variant 3's bullet 2 now cites the recorded status from `docs/designs/sc-issue-launch-level-hook.md:625` (verified in the debate) in place of "UNVERIFIED".
- Validation: Answer matches the required answer; no reference to the default level remains outside "What it costs or risks" bullet 4's comparison ("not a ready plan").

### Change 2: replace the next steps with Variant 3's, keeping the base's precondition style

- Status: Applied
- Before: base steps 1 to 4 (WA-01 "default kept" branch, ship-gate confirmation, design amendment, FU-1 covering both sessions).
- After: Variant 3 steps 1 to 4 kept in order (WA-01, WA-02, WA-04, ledger record), renumbered 1, 2, 4, 5 around the inserted step 3, which uses the base step 2 form "until they all do, FU-1 does not run".
- Provenance: Variant 3 "What happens next" steps 1 to 4; base step 2 (debate point X-001, won by Variant 2).
- Validation: step order WA-01, WA-02, preconditions, WA-04, ledger matches the dependency chain at `merged-requirements.md:811`.

### Change 3: list every FU-1 precondition

- Status: Applied
- Before: no precondition step; Variant 3 named only OB-H1 item 5, as a risk.
- After: step 3 lists OB-H1 item 5 (`refs/claim.md:131`, "Pending, none run" at `sc-issue-launch-level-hook.md:625`, currency on master UNVERIFIED), the `GRANT(WA-04,live-test)` row (`merged-requirements.md:331`, `:719`), ORCA-AVAILABLE (`:604`), Q20 with WA-03 (`:811`), and the owner's written acceptance (INV-012).
- Provenance: debate consensus (all three advocates; A-001, A-003, C-003).
- Validation: each cited line was read; the 2026-11-13 Orca outage at `:604` is not stated as current ("its status today is not known").

### Change 4: word the acceptance to cover what the session could do

- Status: Applied
- Before: base first risk bullet: two permission-free sessions per approved issue, the second in a worktree with a launched agent.
- After: the acceptance covers whatever the one session does on the test issue; the FU-1 write list is the intended set, not a limit; permission checks off (TB-PERM), untrusted issue text (TB-UNTRUSTED), INV-012; limited to one test issue, not removed; the owner can write the test issue's text to shrink the risk.
- Provenance: Variant 1, A-002 (3 of 3 REJECT the assumption); Variant 3 cost bullet 1 text folded in.
- Validation: no claim that the session makes only the listed writes.

### Change 5: record permission-on feasibility during FU-1

- Status: Applied
- Before: no such item.
- After: last "What stays unresolved" bullet: whether a watcher-launched session can run with permission checks on (`CCSESSION_PERMISSIONS`, `CC_CLAUDE_FLAGS`, INV-011) and finish unattended; FU-1 adds a note to its record, no extra run.
- Provenance: Variant 1, U-001.
- Validation: adds no new run or work item.

### Change 6: unlocks and unresolved rewritten for claim-only

- Status: Applied
- Before: base unlocks ("a ready plan", FU-1 data on a second agent, no code change) and base unresolved (ship gate status, owners of `issue-<N>` agents).
- After: Variant 3 unlocks and unresolved. "FU-1 can run" now reads "Once its preconditions hold, FU-1 can run" (debate point X-001). The handoff item says the design work is deferred and the handoff is not built; the unresolved WA-07 item adds "no such handoff exists today".
- Provenance: Variant 3 "What it unlocks" and "What stays unresolved".
- Validation: no sentence claims a watcher-to-orchestrator handoff exists.

## Post-Merge Validation

- Structural integrity: Pass. One H1 title, five H2 sections in the required order (Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved); provenance header comments present; one `<!-- Source: ... -->` comment per section.
- Internal references: Pass. Every cited path and line comes from the plan, a variant, `question.md` or the debate transcript: `refs/claim.md:131`, `sc-issue-launch-level-hook.md:625`, `issue-watcher.md:44`, `merged-requirements.md:331`, `:572`, `:604`, `:719`, `:811`. Work item ids (WA-01 to WA-05, WA-07, SW-10, SW-13, V2-01, Q20, INV-011, INV-012, TB-PERM, TB-UNTRUSTED) all appear in the sources. No new ids, paths or line numbers.
- New contradictions: none found. Variant 3's "FU-1 can run" against its own gate risk (X-001) is resolved by the precondition step and the qualified unlock. The required answer (`--pipeline none`, written acceptance for the one FU-1 test issue only, FU-1 waiting for its listed preconditions) is stated in Answer and consistent with every section. No em dashes or en dashes.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 6 | 6 | 0 | 0 |

One consequential adjustment under Change 1 (base cost bullets 2 to 4 replaced by Variant 3's) is recorded above for orchestrator review.
