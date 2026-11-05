# Refactoring Plan: Merge into Base (Variant B)

## Overview

- Base: Variant B, `variant-2-sonnet-refactorer.md` (sonnet:refactorer). Selected by the Level 1 tiebreaker (debate points B 42.5, A 35.0) after A's combined-score lead of 0.0478 fell inside the 5% band (`base-selection.md`).
- Incorporating strengths from: Variant A (opus:architect) and Variant C (haiku:qa).
- Planned changes: 24 (Changes 1-24), plus 23 base-weakness fixes, most of which are carried out by those changes.
- Overall risk: **Medium-High**. Changes 1, 6 and 8 restructure the base's central placement and accounting design (the tier split).
- Debate status carried into the merge: **CONVERGED**. INV-034 was resolved by a focused round after this plan was drafted (`debate-transcript.md`, "INV-034 Focused Round"); the merge carries the agreed rule R-034′ (see "INV-034: resolved" below). The earlier BLOCKED text below is superseded.
- Citation forms: `B:NN` and similar are variant lines. `R2-B M3` is a Round 2 item. `INV-NNN` is an `invariant-probe.md` row. "inv-A" means `round-inv-advocate-A.md`, and so on.

## Planned Changes

### Change 1: Restate the recommendation as the tier split (from A and B, consensus)

- **Source:** Round 2 consensus: R2-A §0 (A-prime) as amended by R2-B §3 M1-M6, accepted at R2-C §3.
- **Target:** Base §1.1 "The recommendation in six lines" and §1.3 "What done looks like" (restructure).
- **Integration:**
  - Tier 0: report only.
  - Tier 1: deterministic regenerate. Acts late at Wave 8 entry (B's Wave 8a), with no round, no re-trigger and no FSM edge. Ships in P1.
  - Tier 2: text by stated intent. Acts early at `C-initial` through one FSM edge `(S2_CLASSIFY, "conflicting")`, re-triggers reviewers and spends a round. Ships in P2, dark.
  - Tier 3: halts at the end of Wave 0 in the `SKILL.md:268` shape.
  - Item 1 of §1.1 no longer says "no change to any push, gate or transition code". P2 adds one edge and widens one S5a clause (Change 8).
- **Rationale:** X-001..X-004 and C-014, C-017..C-020 are unanimous Split at 90%. N1 (coupling), N4 (budget) and NE1 (S5a gate) were verified by all three advocates.
- **Risk:** High. Restructures the design core; every downstream section depends on it.

### Change 2: Mechanism inventory (from A §3.1 and the B/C consensus)

- **Source:** A §3.1 (two refs, U-003); R2-B C-B4 (scripts).
- **Target:** Base §3.1, §3.2 and §3.3 (replace rows).
- **Integration:**
  - Replace `refs/conflict-sync.md` with two refs split by tier, using A's file names: `conflict-mechanical.md` (Tier 1 and up) and `conflict-intent.md` (Tier 2 only).
  - P1 scripts: a thin `probe-merge.sh` (fetch, `foreign_op`, tree-clean, raw `-z` listing) and `finish-merge.sh`.
  - `collect-conflict-evidence.sh` is deferred to P2, or written as inline calls.
  - Add the P2 FSM edge to the inventory.
- **Rationale:** C-003 A (90%); C-004/X-032 B-modified (75%); C-001 Split (85%).
- **Risk:** Medium. Changes install-list entries and the force-push scan targets (`test_static_grep.py:758-776`).

### Change 3: `MechanicalRule` replaces `REGEN_RECIPES` (from A §7.1)

- **Source:** A §7.1 (A:391-407); U-001, U-002.
- **Target:** Base §4.2 Tier 1 rule and §3.1 core module row (replace).
- **Integration:**
  - Add `MechanicalRule(pattern, kind, sources, regenerate, check)` with one shipped row: `uv.lock`, stage set `123`, with `pattern` anchored to the repo-root path (closes LOW INV-025).
  - The rule applies only when the path is tracked and `uv` resolves on PATH (inv-B INV-033).
  - Generalize A's allowed-tools test to every new inline command and every rule program (A-004).
- **Rationale:** C-010 (95%); A-004 (90%); R2-B A-S5 conceded.
- **Risk:** Low. Additive data shape.

### Change 4: Explicit `BLOCKED` Tier 0 row (from C)

- **Source:** C:55 (U-023).
- **Target:** Base §4.2 table (insert row).
- **Integration:** `mergeStateStatus == BLOCKED` with `mergeable == MERGEABLE` is Tier 0, with its own parametrized row.
- **Rationale:** R2-A R-12; R2-C carry.
- **Risk:** Low.

### Change 5: New Core API section with a single router (from A §7)

- **Source:** A §7 (A:363-451), `conflict_action` (A:419), FR-C6 (A:473).
- **Target:** New base §3.4 "Core API (`superclaude.pr_submit.conflicts`)" (insert after §3.3).
- **Integration:**
  - One pure `conflict_action(...)` routes over tier × ordinal × hook × entering outcome × budget × cap (NE6), with an exhaustive reachable-row test and a fail-closed default row (QA-4).
  - Also in the section: `parse_stage_records`, `merge_parent_ok`, `evaluate_sync_decision`, `merge_preflight_ok`, the resume function (Change 10), and `is_conflict_cycle` with reserved prefixes (Change 21).
- **Rationale:** S-008 A (80%); R2-B A-S6 conceded; R2-C QA-4.
- **Risk:** Medium. Adds a section and consolidates routing that was spread across §5.4, §5.5 and §6.3.

### Change 6: Placement and ordinal table (from A, B M2-M4, C)

- **Source:** A §5.1 (`C-initial`); R2-B M2, M3, M4; inv-A, B and C INV-003.
- **Target:** Base §5.1, §5.2, §5.4 and §5.5 (restructure).
- **Integration:**
  - **Detection:** read-only at the end of Wave 0. Read GitHub `mergeable`/`mergeStateStatus` first; if `UNKNOWN`, re-read up to 3 times, 10 s apart. Run the local probe only on `CONFLICTING` or a persistent `UNKNOWN` (C-007, X-026, X-027).
  - **Before that**, run one unconditional local check for `MERGE_HEAD`, rebase or cherry-pick in progress, and HALT if any is present (INV-004). The reason code is OPEN: `operation_in_progress`, `foreign_op_in_progress` or `merge_in_progress`. Default to B's `foreign_op_in_progress`, which matches the base's `foreign_op` naming.
  - **Tier 3 at L3** halts at the end of Wave 0 (M3), reason `conflict_tier3`.
  - Replace §5.4 with B's M4 table. One acting site per tier per ordinal:

    | Tier | L1 | L2 | L3 |
    |---|---|---|---|
    | 1 | report, PROPOSE | resolve at Wave 8 entry, stop uncommitted | push |
    | 2 | report, PROPOSE | resolve at Wave 8 entry, stop uncommitted | `C-initial`; first seen at `C-ci` → halt `late_conflict` |
    | 3 | report | report | Wave 0 halt |

  - **Tier 1 acts on all four armed outcomes** (M2). L2 sets `S4'_HALT_BEFORE_PUSH` only when entry came from `clean` or `REPORT_ONLY`. From `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE` it reports and keeps the preserved terminal (INV-003, unanimous).
- **Rationale:** C-014, C-015, C-016, X-012 and X-031 are unanimous. S-009 B (70%).
- **Risk:** High. Rewires the base's single late hook into two hooks plus a Wave 0 halt.

### Change 7: Thin probe, with stage parsing in the core (from A)

- **Source:** A AD-6 (A:51) and the captured fixture (A:557); U-005.
- **Target:** Base §5.3 probe contract (replace output schema).
- **Integration:** `probe-merge.sh` emits the raw `merge-tree --write-tree -z` listing. `parse_stage_records` in the core parses it and is tested against `fixtures/merge_tree_conflict.z`. Fold base Appendix B (exit contract) into §5.3 and §6.4.
- **Rationale:** C-008 (95%); C-036 (95%).
- **Risk:** Medium.

### Change 8: Rounds, caps and re-trigger per tier (from A §5.4-5.5 and B M5)

- **Source:** A §5.4-5.5 (A:222-247); R2-B M5; R2-C QA-3.
- **Target:** Base §5.6 (restructure) and the §8 test plan.
- **Integration:**
  - **Tier 1 (`kind: "sync"`):** no round, no re-trigger, no reply or resolve. `SYNC_CAP = 1`.
  - **Tier 2 (`kind: "merge"`):** ticks `round_counter` on the INV-001 edge (P2).
  - Widen the S5a trigger in `fsm.py:1137` and `SKILL.md:274` to `applied_edits > 0 or kind == "merge"`, placed between the pins at `test_static_grep.py:689` and `:750` (NE-C3). Add a new static pin and the zero-edit-pair behavioural test (QA-3).
  - At `C-initial` the re-trigger targets the *configured* reviewers. Pin that substitution (MEDIUM INV-030, partly).
- **Rationale:** C-018, C-019, X-002 and X-003 Split (90%); C-032/X-028 B value 1 (75-80%).
- **Risk:** High. Edits FSM core text that has adjacent pins.

### Change 9: One sibling gate for both tiers (from B M5)

- **Source:** R2-B M5 (extends base §6.3).
- **Target:** Base §6.3 (modify).
- **Integration:** `evaluate_sync_decision` covers both tiers. Its predicates:
  - ordinal ≥ 3;
  - validated;
  - tier allowed and no halt;
  - under cap. For Tier 2, "under cap" also requires `round_counter < max_rounds`.

  No `applied_edits` predicate. Add a cross-gate property test against `evaluate_push_decision` on the shared predicates (R2-B A-B1).
- **Rationale:** C-021/X-010 B (75%); NE1.
- **Risk:** Medium.

### Change 10: Push records and kind-aware recovery (from A, B and C; INV-001, INV-002)

- **Source:** inv-A, inv-B and inv-C INV-001; C:83 (C-030); A:594 (additive kwargs); R1-B concession 4.
- **Target:** Base §5.7, §5.8 and the §3.1 records row (restructure).
- **Integration:**
  - Drop `build_sync_triad`. Add the keyword arguments `push_kind` and `base_sha` to `build_push_triad`.
  - `kind ∈ {fix, merge, sync, ci}` goes on all three push records. It defaults to `fix` when absent, so legacy logs read as today. `push_initiated` for `sync`/`ci` also records the preserved review terminal (inv-B).
  - The recovery key tuple (`recovery.py:98-110`) gains `kind`.
  - One pure resume function (inv-A) returns a resume directive (inv-C). For `sync`/`ci`:
    - Branch A: enter the Wave 8 CI wait with `source=ci`, `wait_sha = target_sha` and the preserved terminal.
    - Branch B: re-run the Wave 6 pre-push guard, plus `merge_parent_ok` for `sync`, push the recorded `target_sha`, then take the same directive.
    - Never `S4_PUSHING`, S5a or S5. A missing terminal fails closed with `resume_unrepresentable`.
  - `fix`, `merge` and absent kinds keep today's outputs byte-equal.
  - Withdraw base B:299 ("Branch A of a sync returns `S2_CLASSIFY`").
- **Rationale:** INV-001 ADDRESSED (unanimous rule); C-030 C (90%); C-031/X-030 (85%).
- **Risk:** Medium. Touches recovery; protected by the kind × branch table test (inv-C acceptance test).

### Change 11: VAL rules (from C R-C7 and A-003)

- **Source:** R2-C R-C7; A-003 (unanimous).
- **Target:** Base §6.7 (modify).
- **Integration:**
  - Tier 1 VAL = `uv lock --check` + VG-3 (`make lint`) + VG-4 (`ruff format --check`).
  - If the VG-2 target is absent or runs no tests, cap the run at Tier 1 and add the report line "no tests found for changed area".
  - **VG-2 at Tier 2 is OPEN** (X-019/C-028 unresolved). Keep base B:387 as the default and mark it OPEN.
  - Record a baseline note for MEDIUM INV-014 as an open question.
- **Rationale:** X-018 B(+C) (70%); A-003 (90%).
- **Risk:** Low.

### Change 12: Clean-tracked-tree preflight (from A; INV-008)

- **Source:** A:288; inv-A, inv-B and inv-C INV-008.
- **Target:** Base §5.3 (`index_clean` becomes `tree_clean`), §6.4 and `finish-merge.sh` (modify).
- **Integration:**
  - Act only when `git status --porcelain=v1 --untracked-files=no -z` is empty. Untracked files are tolerated.
  - On a dirty tree: HALT `merge_preflight_dirty` and name the files, in the shape of `fix_commit_failed` (majority A and C).
  - `finish-merge.sh` re-asserts the clean tree right before the regenerate. After the commit it asserts both `status --untracked-files=no` empty and `git diff --quiet HEAD` (inv-B).
  - Add a real-git test with a dirty `pyproject.toml`; it must halt with nothing merged.
- **Rationale:** INV-008 ADDRESSED; C-026/X-024 A (80-90%).
- **Risk:** Medium. Stricter than base B:241; operators with unrelated work in progress now halt.

### Change 13: Create path (from A AD-7, scoped)

- **Source:** A AD-7 (A:53); R2-A R-4/R-5.
- **Target:** Base Appendix A, §11 bullet 4, OQ-7 (replace).
- **Integration:** a separate precursor change.
  - At L1+ the create path neither rebases nor halts when behind base; behind is a Tier 0 report.
  - L0 keeps today's rebase byte for byte (`test_static_grep.py:649-657` unchanged). Only the L1+ HALT pins at `:658` and `:660` are rewritten.
- **Rationale:** C-033/X-013 A (95%).
- **Risk:** Medium. Pin rewrite.

### Change 14: `pr_conflicting` CI-wait skip (from A)

- **Source:** A:220, FR-C23 (U-004).
- **Target:** Base §5.5 (insert).
- **Integration:** when Wave 8 is entered on a still-conflicting PR and no merge is pushed (L1, L2, a tier above the cap, or a preflight halt), skip the CI wait with reason `pr_conflicting` instead of polling until `--timeout` (INV-024).
- **Rationale:** R1-B concession 2; adopted by all three.
- **Risk:** Low.

### Change 15: Flag rename (from A name, B default)

- **Source:** A:76; B:97.
- **Target:** Base §1.1, §7.1 FRs and §9 (replace).
- **Integration:** `--sync-tier` becomes `--conflict-max-tier {0,1,2}`, default 1.
- **Rationale:** C-034/X-014 (95%).
- **Risk:** Low.

### Change 16: Output contract and counting (from B M6 and C QA-1/QA-2; INV-018)

- **Source:** R2-B M6; R2-C QA-1, QA-2; inv-A INV-018 (withdraws N2).
- **Target:** Base §7.1 FR-19 and §5.6 (modify).
- **Integration:**
  - `push_count` excludes kind `sync` only. Add `sync_push_count`, which is at most `SYNC_CAP`, plus `push_kind` on the records.
  - Make the `rebuild_state` fold at `run_log.py:238-239` kind-aware.
  - Reconcile `SKILL.md:239` with `:275`.
  - Add a behavioural `rebuild_state` test with a conflict push in the fixture (QA-1) and a report-contract test (QA-2).
- **Rationale:** X-005 (90%); C-035 (85%); INV-018 ADDRESSED.
- **Risk:** Medium.

### Change 17: Wait-only sentences carve-out (INV-009)

- **Source:** inv-A, inv-B and inv-C INV-009.
- **Target:** Base §6.9 / §8.3 edit list (insert).
- **Integration:** rewrite `refs/state-machine.md:144-146`, `refs/ci-poll.md:28-29` and `SKILL.md:277` so that "never an additional push" covers model-authored fixes, with the single Tier 1 sync push (`SYNC_CAP = 1`) named as the only exception. Add a `test_static_grep.py` pin; none exists today. The exact wording is OPEN between the three proposals; the meaning is agreed.
- **Rationale:** INV-009 ADDRESSED.
- **Risk:** Medium. Normative protocol text.

### Change 18: Rejected-push handling (A-001 and INV-035, majority)

- **Source:** A-001 (unanimous); inv-A and inv-B INV-035.
- **Target:** Base §6.4 and §5.8 (insert).
- **Integration:**
  - Before the first merge push, read `mergeCommitAllowed`, `rebaseMergeAllowed` and `squashMergeAllowed` as an advisory report; never halt on an unreadable value. After the push, report `mergeStateStatus == BLOCKED` with a reason line.
  - The P1 gate requires a real PR to read `MERGEABLE`.
  - A rejected live `git push` appends `push_aborted_or_not_landed{rejected: true, stderr_tail}` and halts `push_rejected`. Recovery Branch B never re-drives a record marked `rejected`.
- **Rationale:** A-001 (85%); INV-035 majority A and B; C does not reject the halt.
- **Risk:** Low.

### Change 19: Risk register format and rows (from C)

- **Source:** C §10 (S-014); R2-C QA-10.
- **Target:** Base §10 (restructure columns; append rows).
- **Integration:**
  - Split "Likelihood / impact" into two columns.
  - Add C's R14, "Tier 2 validates but is semantically wrong", rated "Certain, partially".
  - Add a QA-10 row: a future edit re-narrows the S5a clause.
  - Add rows for the MEDIUM invariant warnings: INV-005, 010, 011, 012, 013, 014, 022, 027, 030, 031.
- **Rationale:** S-014 C (95%).
- **Risk:** Low.

### Change 20: Definitions section (from C)

- **Source:** C §2 (C:16-24; U-020).
- **Target:** New base §1.4 "Definitions" (insert).
- **Integration:** C's terms, adapted to the split (sync cycle, merge cycle, tier, marker line, HALT). Also expand **VAL** and **FSM** on first use; this fixes Clarity-4.
- **Rationale:** U-020 adopted; base-selection Clarity-4 NOT MET for every variant.
- **Risk:** Low.

### Change 21: Cycle-id prefixes (A-005)

- **Source:** A-005 (unanimous); QA-8.
- **Target:** Base §5.7 and §7.1 FR-15 (modify).
- **Integration:** reserve the `sync-` and `conflict-` prefixes, add a pure `is_conflict_cycle`, and add one test that the fix-cycle id rule can produce neither prefix.
- **Rationale:** A-005 (90%).
- **Risk:** Low.

### Change 22: Test plan additions and removals (from A, C and B concession)

- **Source:** A:557; R2-C QA-1..QA-10; C §9.3 (U-021); C:161 (U-024); R1-B concession 6.
- **Target:** Base §8.1-§8.6 (modify).
- **Integration:**
  - Add: the captured-fixture parser test; the `conflict_action` table test; QA-1..QA-10; C's "deliberately no test" list, rewritten to cover only the live push, the live re-trigger POST and real-GitHub probes; the `== 41` sweep plus the `models.py:23` docstring; per-tier call ceilings as an NFR (QA-9).
  - Remove the NFR-9 `SKILL.md <= 346` line-count assertion; keep the byte-identical fragment test (§8.4).
- **Rationale:** C-036 (95%); S-015 B+C (70%).
- **Risk:** Low.

### Change 23: P1 gate rewrite and the no-op statement (INV-033)

- **Source:** inv-A, inv-B and inv-C INV-033.
- **Target:** Base §9 P1 row and §8.5 (replace gate text), plus a §1.3 note.
- **Integration:**
  - State that P1's Tier 1 rule is a no-op in IronClaude, because `uv.lock` is gitignored (`.gitignore:169`, `:222`). P1 still pays here through Tier 0 detection, the Tier 3 Wave 0 halt and the `pr_conflicting` skip.
  - P1 gate:
    - (a) a mandatory hermetic real-git test in a pytest temporary directory with a tracked `uv.lock` and a zero-dependency `pyproject.toml` on two diverging branches. It runs probe → classify → `uv lock` (offline, real uv with a `skipif(no uv)` case) → `finish-merge.sh` → `merge_parent_ok`, with `gh` mocked. This is an allowed internal temporary checkout under CLAUDE.md.
    - (b) one **manual** live L3 run on a separate repository that tracks `uv.lock` (majority A and C). Creating that repository is the user's decision. It must be under `IronbellyOrg`, never upstream. The run also exercises INV-034.
  - Do not un-ignore `uv.lock` here.
- **Rationale:** INV-033 ADDRESSED.
- **Risk:** Low. Gate text only; the live run depends on the user.

### Change 24: Structural clean-up of the base (from A and C structure)

- **Source:** A §2 decision-record form (S-005); S-013 (A/C).
- **Target:** Base §1.2 and §13 (restructure).
- **Integration:**
  - Turn §1.2's debt table plus the reject list into AD-style decision entries with rejected alternatives (S-005 A, 70%).
  - Move Appendix B into the body (Change 7) and retire Appendix A (Change 13), so no appendix stays nested under "13. Index". This fixes base Structure-2.
- **Risk:** Low.

## Base Weaknesses and Fixes

| # | Base weakness | Better variant / source | Fix |
|---|---|---|---|
| W1 | Reviewers never see a Tier 2 resolution (K8, B:538) | A (§5.5), Split consensus | Changes 1, 6, 8: Tier 2 acts early, re-triggers and spends a round (P2) |
| W2 | Report-only after `HALT_MAX_ROUNDS`/`TERMINAL_AUGMENT_NO_RESPONSE` leaves a mechanical conflict unmergeable (B:261, OQ-4) | B's own M2 (R2-B A-B4) | Change 6 (Tier 1 acts on all four armed outcomes) plus Change 17 (wait-only carve-out) |
| W3 | Tier 0 cost understated; local `merge-tree` treated as truth (X-040, B:242) | A (A:198-203) | Change 6: GitHub first, probe only on `CONFLICTING`/persistent `UNKNOWN` |
| W4 | Create-path "unpublished branch" premise is false (X-013) | A AD-7 | Change 13 |
| W5 | "CI polls forever" blind spot overclaimed (R1-B concession 2) | A U-004 | Change 14 |
| W6 | `build_sync_triad` duplicates the triad builder (R1-B concession 4) | A additive kwargs (A:594) | Change 10 |
| W7 | `SKILL.md <= 346` line-count pin is brittle (R1-B concession 6) | B's own fragment test | Change 22 |
| W8 | OQ-11: unsure `S4'_HALT_BEFORE_PUSH` is reachable from Wave 8 (B:574) | A (caller sets S4', `fsm.py:1118-1121`) | Change 6; close OQ-11 |
| W9 | `SYNC_CAP = 2` exists only for deferred P3 | C's bound (C:112) | Change 8: `SYNC_CAP = 1` |
| W10 | `index_clean` preflight lets `uv lock` read unstaged edits (**INV-008**, HIGH) | A (A:288) | Change 12 |
| W11 | Branch A of a sync returns `S2_CLASSIFY`; Branch B returns `S4_PUSHING`, then reply, resolve and re-trigger (**INV-001**, HIGH) | Unanimous round-inv rule | Change 10 |
| W12 | `kind` only on sync records; a crashed L3 CI push resumes at S5a (INV-002) | C (C-030) plus `ci` kind | Change 10 |
| W13 | P1 gate cannot be met here; `uv.lock` is ignored (**INV-033**, HIGH) | Unanimous round-inv rule | Change 23 |
| W14 | Post-sync CI re-poll can read `clean` before any check exists (**INV-034**, HIGH) | INV-034 focused round: all three MODIFY to R-034′ | Change 25 (see "INV-034: resolved" below) |
| W15 | L2 at Wave 8a after a preserved terminal overwrites it with S4' (INV-003) | Unanimous | Change 6 |
| W16 | An L2 merge left in progress goes undetected when GitHub reads `MERGEABLE` (INV-004) | Unanimous | Change 6: unconditional Wave 0 local check |
| W17 | Wait-only sentences contradict Tier 1 pushing after terminals (INV-009) | Unanimous | Change 17 |
| W18 | `push_count` prose bounds disagree and are unpinned (INV-018, NE-C1) | B M6 plus C QA-1/QA-2 | Change 16 |
| W19 | A rejected push is re-driven on every `--resume` (INV-035) | A/B majority | Change 18 |
| W20 | Overclaims that "evidence-validator confirms" intent (B:41, B:349) | Unanimous A-002 | Reword to "grounding checked" in §1.3, §6.4 and K1 |
| W21 | VAL and FSM never expanded (Clarity-4) | C Definitions | Change 20 |
| W22 | Appendices nested under Index (Structure-2) | A/C | Change 24 |
| W23 | Recovery text and routing spread across 4 places (NE6) | A `conflict_action` | Change 5 |

### INV-034: resolved (Change 25), supersedes the BLOCKED entry that follows

- **Change 25 (from the INV-034 focused round; A's R-034′ text, B's timeout correction, C's tests).** Target: base §CI wait and §Core API, plus the test plan. Integration: insert. Risk: Medium.
  - `superclaude.pr_submit.ci.classify_checks(payload, *, wait_sha=None, expect_checks=False)`: when `expect_checks` is true and the chosen check list is empty at `head_sha == wait_sha`, return `polling`. Default off keeps every existing pin green.
  - The skill sets `expect_checks` once per push and records it in the run-log so `--resume` reuses it. True if any holds: (a) checks were seen earlier in this run on any head; (b) `pre_push_sha` has at least one check run or status context; (c) `base_sha` has at least one. Evidence for (b) and (c) comes from `poll-ci-checks.sh --evidence-sha <sha>` reading `gh api repos/$REPO/commits/<sha>/check-runs` and `/status` (commit-scoped, so it survives a PR turning conflicting), emitting `evidence_checks:<n>` or `-1` on a failed or unparsable read; `-1` counts as had checks (fail closed). `gh` stays out of the core.
  - No Actions only when (a), (b) and (c) all read zero: then an empty list is `clean`, as today.
  - Expiry with no registered check is the existing Wave 8 CI `timed_out` result with reason `ci_not_started`; never `clean`, and the report never says "tests passed".
  - Amend `refs/ci-poll.md:21` and `SKILL.md:277` ("only parsed empty ... prove there are no Actions") to add "and `expect_checks` is false".
  - Tests (`tests/pr_submit/test_ci_classify.py` plus an evidence-setter test): empty + expect + matching head = `polling`; nonempty all-pass + expect = `clean`; empty + no expect = `clean`; existing tests unmodified; head mismatch = `polling`; setter: `pre_push_sha` nonempty = true, all empty = false, read fails = true, `pre_push_sha` empty but `base_sha` nonempty = true.

### INV-034: carried as a BLOCKED decision (SUPERSEDED by Change 25 above; kept for the record)

- **Agreed by all three; merge this part.** `classify_checks` gains a keyword, default off, so every existing pin (`test_ci_classify.py:36-38`) stays green. When the keyword is on after any push (a Tier 1 sync or an L3 CI push), an empty parsed check list at `head_sha == wait_sha` classifies `polling`, not `clean`. The final report never says "tests passed" when no check was registered. Edit `refs/ci-poll.md:21` and `SKILL.md:277` to match.
- **Not agreed: merge as OPEN, blocking.** How the wait ends, and whether a no-checks end may report `clean`:
  - **Option A (inv-A):**
    - `poll-ci-checks.sh --wait-sha` emits `sha_checks` from `gh api repos/$REPO/commits/<sha>/check-runs` and `/status`.
    - `expect_checks` is true if checks were seen earlier in the run or on `base_sha`; with it true, 0 registered checks is `polling`.
    - A timeout reports `ci_not_started`, never clean.
    - A rejects settle windows as racy.
  - **Option B (inv-B):**
    - `after_push`, `empty_polls` and `settle_polls=3`; after 3 empty polls the report says "no checks registered after N polls".
    - It also emits `mergeable` and refuses `clean` while `CONFLICTING` (also covers MEDIUM INV-027).
    - The check-runs API is deferred.
  - **Option C (inv-C):**
    - A grace of about one poll interval after the first post-push poll, then empty means `clean`.
    - Script unchanged.
    - C rejects the check-runs API.
- **Required before merge-complete:** either a focused round on this one question, or the user accepting one option (or the residual risk) explicitly. The merge-executor must not choose.

### MEDIUM and LOW items carried as open questions (not adopted)

- **INV-010:** three-way split.
  - A: same action at L2 and L3, plus a monotonicity property test.
  - B: drop Tier 2 resolution at L2.
  - C: accept as a risk row.

  Add to base §12 as an open question with all three options. Add the risk row (Change 19).
- **INV-005, 011, 012, 013, 014, 022, 027, 030 (in part), 031:** add as risk rows (Change 19) and open questions. Suggested handling, from `invariant-probe.md`:
  - INV-005: re-run `finish-merge.sh` and VAL on resume.
  - INV-011: route a re-probe tier increase between hooks.
  - INV-012: route tiers above the cap at L3.
  - INV-013: staged blob == `merge-tree` result for non-resolved paths.
  - INV-014: VAL baseline on base.
  - INV-022: GitHub `CONFLICTING` with an empty local set.
  - INV-027: truthful status on post-push `CONFLICTING`.
  - INV-031: scope findings to the PR diff after a merge.
- **LOW:**
  - INV-016: `--no-renames` on both diffs.
  - INV-019: which per-run merge bound is intended (Tier 2 `<=1` plus Tier 1 `SYNC_CAP=1`).
  - INV-020: cap 8 versus 10, and whether regenerated files count.
  - INV-021: `--max-rounds 0/1` with Tier 2.
  - INV-025: root-anchored pattern (handled in Change 3).
  - INV-032: `check-merge-conflict` hook versus the marker allowance.

  Add each as a one-line note in base §12.

### Unresolved diff points: base text kept, marked OPEN

| Point | Base (kept) | Competing positions | Merge action |
|---|---|---|---|
| C-028 / X-019 | VG-2 forced only for `pr_submit/` or a `pyproject.toml` conflict (B:387) | A: VG-2 mandatory at Tier 2 (A:314). C: `is_cross_cutting` (C:112). | Keep B's text and add an OPEN marker plus an open question |
| C-029 / X-011 | `sync_started`, `sync_concluded` (41 → 43) | A: `conflict_classified`/`conflict_resolved`. C: three events (44). inv-B: no new event type in P1. | Keep B's events for Tier 1; mark P2 Tier 2 events OPEN; apply QA-6's pin sweep whatever the final count |
| X-009 | Guard order: head → parent → base ancestry → decision (B:353) | A: head → ancestry → parent → decision | Keep B's order and mark OPEN |
| S-001..S-004, S-007 | Base form | Surface preferences only | No action |

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for not adopting |
|---|---|---|
| C-018 / X-002 (A, original) | Every conflict push, including Tier 1, spends a round | N4: on a spent budget this reproduces #305. A conceded for Tier 1 (R2-A R-1). |
| X-005 / C-035 (A N2) | Count merge pushes in `push_count`, no new field | A withdrew N2 in favour of M6 plus QA-2 (inv-A INV-018). |
| C-021 / X-010 (A) | Reuse `evaluate_push_decision` with `applied_edits = resolved paths` for Tier 2 | NE1: it collides with the S5a gate or misstates INV-016 predicate 5 (R2-B M5; R2-C verified). |
| AD-4 (A) | Tier 3 through the `needs_human_decision` pre-gate | It needs an armed FSM; the Wave 0 halt in the `SKILL.md:268` shape does not (R2-B M3; R2-C accepts). |
| X-016 (A) | `WHITESPACE_ONLY` as Tier 1 | Indentation carries meaning in Python and YAML; A conceded (R1-A concession 3). |
| C-013 / X-017 (A) | `MAX_INTENT_FILES = 10` | Majority B and C chose 8. A's boundary-test form is kept with the value 8 vs 9. |
| C-015 / X-031 (A) | L1/L2 stop before review | A conceded (R1-A concession 9, R2-A R-2). |
| C-004 / X-032 (A) | Zero scripts | `finish-merge.sh` is the only gate real-repo tests can run (A conceded, R1-A concession 7). The thin probe hosts `foreign_op`/tree-clean (majority). |
| INV-008 (A extra) | Refuse untracked rule-input paths | A alone proposed it. B and C tolerate untracked files. Recorded as an open hardening question. |
| INV-035 (A extra) | Refuse the push before it happens on a rebase-only repo | A alone. B and C keep merge-method fields advisory. Recorded as an open question. |
| INV-008 (B) | A dirty tree skips the hook and reports, with no halt | Majority A and C halt with `merge_preflight_dirty`, matching the existing halt pattern. |
| INV-033 (B) | Live gate on throwaway branches in this repo that force-add `uv.lock` | Majority A and C use a separate repository that tracks `uv.lock`, so this repo is not mutated. |
| INV-035 (C) | One re-drive, then `HALT_HUMAN` | Majority A and B: a rejected push is never re-driven. |
| X-020 / X-035 (C) | Classify after a merge attempt stops | Breaks L1 and Tier 3-with-nothing-touched; C conceded. |
| X-034 (C) | Wave 0b before Wave 1, appending run-log events | The run-log does not exist before Wave 1 (`SKILL.md:269`); C conceded. |
| X-006 / X-007 (C) | Order-independent `merge_push_parent_ok` | Accepts a merge made from the base branch and inverts first-parent history; C conceded (R2-C R-C11). |
| X-023 (C) | Staged set == conflicted set | Cannot be satisfied when the base changed any clean path; C conceded. |
| X-012 (C) | L2 commits locally | Breaks T-412 "commit never" (`SKILL.md:273`); C conceded. |
| X-015 / X-033 / U-022 (C) | Tree conflicts, `.claude/` sync targets and snapshots as Tier 1 | Judgment-bearing or not trackable (`.gitignore:127-128`); C conceded (R2-C R-C6). |
| X-014 (C) | No flag | The split needs the dial; C dropped this (R2-C C-034). |
| X-018 (C) | No VAL for a lockfile-only Tier 1 | C adopted `uv lock --check` plus VG-3/VG-4 (R2-C R-C7). |
| C-004 (C) | Append fields to `poll-augment-review.sh` | Wrong hook under the split; it ripples into `test_cosmos_poll.py`; C conceded (R2-C R-C13). |
| X-039 (C) | `GIT_EDITOR=true git commit` | Does not match `Bash(git *)` (`SKILL.md:4`); use `git commit -F`. |
| U-019 / X-037 (C) | Re-check point B inside the fix-push guard | Cannot pass either parent check; C withdrew it (R2-C R-C3). |
| X-022 (C) | Any marker line blocks | Blocks legitimate documentation markers; scope stays with the introduced-marker rule (A/B equivalent). |
| X-013 (C) | Keep the create-path rebase | Same false premise as base B; A's L1+ removal is adopted (Change 13). |
| X-025 (C) | No zdiff3 | A and B both use per-invocation zdiff3 (inferred, 60%). Base kept. |
| C-027 / X-021 (A/C, inferred majority) | Leave a mid-resolution merge in progress (versus base abort, B:391) | **Not applied.** The majority is inferred at 60% only, and the choice interacts with INV-004's Wave 0 halt and with INV-010. Base §6.8 is kept with an OPEN marker, and the point is listed among the open questions. |

## Risk Summary

| Change # | Risk | Impact if failed | Rollback |
|---|---|---|---|
| 1 | High | The design narrative no longer matches the sections below it | Revert to base §1.1 and §1.3 |
| 2 | Medium | Install list or force-push scan misses the new ref or script | Revert §3 rows; `test_cli_install` and `test_static_grep` catch it |
| 3 | Low | Rule never matches | Remove the rule row; fall back to Tier 2 |
| 4 | Low | `BLOCKED` misread as a conflict | Drop the row |
| 5 | Medium | Router table diverges from §5.4 | The table test fails |
| 6 | High | Hooks misplaced; a conflict acted on twice or never | Revert to base §5.1-§5.5; the `conflict_action` table test pins it |
| 7 | Medium | Parser drift against real git output | Fixture test fails; keep the B script parser behind a flag |
| 8 | High | S5a clause re-narrowed, so Tier 2 is never re-triggered | QA-3 behavioural test; pins at `:689`/`:750` |
| 9 | Medium | Sibling gate drifts from INV-016 | Cross-gate property test |
| 10 | Medium | Legacy logs resume differently | Byte-equal regression rows for `fix`/absent |
| 11 | Low | VAL too weak or too strong for Tier 1 | Revert §6.7 |
| 12 | Medium | Operators with work in progress halt more often | The halt message names the files; revert to `index_clean` only with INV-008 reopened |
| 13 | Medium | L0 behaviour changes by accident | `test_static_grep.py:649-657` byte-identical |
| 14 | Low | CI wait skipped on a PR that is mergeable | Remove the skip |
| 15 | Low | Flag name break | Pre-release; no users yet |
| 16 | Medium | Wrong counts in the report | QA-1/QA-2 tests |
| 17 | Medium | Protocol text inconsistent | New static pin |
| 18 | Low | False `push_rejected` | Halt is safe-fail |
| 19-22, 24 | Low | Documentation or test-plan only | Remove the added rows or sections |
| 23 | Low | Live gate never run | Gate (a) still runs automatically |
| 25 (INV-034) | Medium | A conflict-sync on a repo with no workflows anywhere still waits; a repo whose checks exist but register slowly waits to timeout | Keyword default off; remove the keyword use to restore today's behaviour |

## Review Status

- [x] Auto-approved (default; `--interactive` not set)
- [ ] User-approved (`--interactive`)
- Approved by: auto
- Approval timestamp: 2026-11-04T14:57:36Z
- Condition: auto-approval covers Changes 1-25. Change 25 (INV-034) was added by the orchestrator at 2026-11-04T15:12Z from the INV-034 focused round; convergence status is CONVERGED.
