# Adversarial Debate Transcript

Folder: `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/remediation/watcher-plan-v3/adversarial/`. This file assembles the existing round files; it adds no new argument. Sources: `diff-analysis.md` (points), `round1-advocate-1.md` (A1, for V1 opus security), `round1-advocate-2.md` (A2, for V2 opus architect), `round1-advocate-3.md` (A3, for V3 sonnet analyzer), `round2-rebuttals.md` (R2, orchestrator verdicts). `invariant-probe.md` is used only for cross-references. Taxonomy: L1 surface, L2 structural, L3 state mechanics (guards, invariants, state changes).

## Metadata
- Depth: standard (Round 1 advocate statements, Round 2 rebuttals and verdicts; no Round 3)
- Rounds completed: 2
- Convergence achieved: 88.9% overall (48 of 54 votes); 75.0% on the eight contested points (18 of 24)
- Convergence threshold: 80%
- Focus areas: all (Q-1 to Q-10 remediation points D-01 to D-14, shared assumptions A-001, A-002, A-007)
- Advocate count: 3 (A1, A2, A3)
- Source for convergence figures: `round2-rebuttals.md` section 3

## Round 1: Advocate Statements

Each advocate steelmanned the other two variants first (A1 section 1, A2 section 1, A3 section 1). The per-point positions below summarise the cited sections.

### Per-point positions (Round 1)

| Point | Level | A1 (for V1) | A2 (for V2) | A3 (for V3) |
|---|---|---|---|---|
| D-01 guard class scope | L3 | Best result is V2's catch-all `'issue '*` after guard:652 plus V1's `label` and `project` rows; V3 weak. Conf 0.8 (A1 section 2, D-01) | Keep `'issue '*`, class ISSUE; concede V1 is right to add `label`/`project`. Conf 0.8 (A2 section 2, D-01) | Concede to V2; V1 extension optional (scope beyond the finding). Conf 0.25 for V3 (A3 section 3, D-01 / C-3) |
| D-02 / C-5 coordinator-only pattern (guard:444) | L3 | Concede to V2: V1's `*issue_pipeline*complete*` refuses `uv run pytest tests/issue_pipeline/test_complete.py` (bash case run). Suggests V2's four alternatives plus `*issue_pipeline*complete.run*`. Conf 0.9 on V2, 0.5 on the extra alternative (A1 section 2, D-02) | V2's narrow patterns are right; concedes the hyphen form still over-matches `plan-hash ... complete.md`. Conf 0.85 (A2 section 2, D-02) | Concede to V2; notes precedent `*issue_pipeline*approval_record*` already over-matches. Conf 0.3 (A3 section 3, D-02) |
| D-03 guard version stamp | L3 | Concede to V2; V1 omits it; a stale host guard passes the IR-4 preflight (guard:10, orca_worktree.py:839). Conf 0.9 (A1 section 2, D-03) | Bump to 2 in Task 10; verified :839 and :987 exact-line membership test. Conf 0.9 (A2 section 2, D-03) | Concede to V2; V3 had not read the comparison. Conf 0.15 for V3 (A3 section 3, D-03) |
| D-04 self-approval by launch account | L3 | Keep Part B; the approvers file lists the launch account (source.md:64), `approval_of` has no exclusion (predicates.py:216-223). Accepts warn-first as a retreat. Conf 0.75 some form, 0.5 hard-refuse (A1 section 2, D-04) | Concede V2 under-handles it; put it to the owner as a decision with V1's mechanism as Option A. Conf 0.7 (A2 section 2, D-04) | V1 right on the facts, V3 right that it needs the owner. Conf 0.35 (A3 section 3, D-04) |
| D-05 / D-06 / C-2 ship gate | L3 | Reject V3's config key (guard:763-765 does not protect `~/.config/superclaude`); take V2's constant plus V1's coupling test; V1's own module is overkill. Conf 0.85 vs V3, 0.6 V2 over V1 (A1 section 2, D-05) | V2 Option A (code constant) over V3's key; take V1's coupling test; the A2 split is better granularity. Conf 0.75 (A2 section 2, D-05) | Concede to V2/V1; the key is the loosest control; notes V3's own default inconsistency (`closed` vs `open`). Conf 0.35 (A3 section 3, C-2 / D-05 / D-06) |
| D-07 updatedAt approach | L3 | Partial concede to V2: the default should not include the item time. Conf 0.7 (A1 section 2, D-07) | V2 Option C (field-value times), confirmed once by Task 3a; adopt V1's "unreadable time voids". Conf 0.7 (A2 section 2, D-07) | Concede to V2; the item time has the false-void and fail-open risk V3 itself ranks #2. Conf 0.3 (A3 section 3, D-07) |
| D-08 / C-1 reason precedence | L3 | V1/V2 over V3, but close; concedes V3 is the smaller edit. Conf 0.6 (A1 section 2, D-08) | Specific reason first; adopt V1's order (approval reread first). Conf 0.75 (A2 section 2, D-08) | V3 convention (specific at examine, collapsed at revalidate) versus fidelity; concedes that if plan:71 is fixed, V2's wording is right. Conf 0.45 (A3 section 3, C-1 / D-08) |
| D-09 Status move target | L3 | Compare-and-set belongs in the plan; take V2's refusal words and `^PVT_` check. Conf 0.8 / 0.7 (A1 section 2, D-09) | Concede compare-and-set to V1; keep V2's refusals. Conf 0.75 (A2 section 2, D-09) | Concede to V1 on the Status guard, to V2 on refusals; notes read-then-write is not atomic. Conf 0.3 (A3 section 3, D-09) |
| D-10 marker | L2 | Concede to the constant `<!-- sc:issue:result -->`; objects to V1's `op=none`. Conf 0.65 for V2/V3 (A1 section 3) | Not argued separately | Marker must be per-run: with a static marker a retry after a fresh approval posts nothing (plan:141). Conf 0.3 for V3 (A3 section 3, D-10) |
| D-11 Q-7 test move | L2 | Slightly ahead V2 (0.55); keep V1's tip of writing `_PROMPT_RE` in the test (A1 section 3) | Seven files (45 hits) move into Task 6 (A2 section 4) | Concede Q-7 to V2 (A3 section 3, D-11/D-13/D-14) |
| D-12 / C-4 `String!` | L1 | V1 and V2 over V3; reject `$owner: String = "IronbellyOrg"`; take V1's count plus V2's regex. Conf 0.85 (A1 section 2, D-12) | Reject V3's default-value form; merge V2's "read DF-14 first" with V1's exact header. Conf 0.8 (A2 section 2, D-12) | Concede to V1; V3 should not have offered the default-value form. Conf 0.25 for V3 (A3 section 3, D-12 / C-4) |
| D-13 / D-14 | L1 | Converge; V2's Constraints line is best (A1 section 3) | V2 Constraints line is the strongest (A2 section 4) | Concede Q-10 to V2 (A3 section 3) |
| A-001 pr-submit still works | L3 | True for `gh` text; the residual is the script path. 0.7 (A1 section 2) | True for the text path. 0.8 (A2 section 2) | Verified by grep; scripts unseen (A3 section 3) |
| A-002 script bypass | L3 | Document and escalate; V1 names the real fix (credential separation, a Coder row). 0.85 (A1 section 2) | No fix inside this plan; concede V1's wording. 0.8 (A2 section 2) | Equal; residual only (A3 section 3) |
| A-007 fail-closed cost | L2 | Acceptable if it does not block the work launched agents do. 0.75 (A1 section 2) | Accept if each rule gives owner message text. 0.6 (A2 section 2) | Owner should confirm once (A3 section 3) |

### Variant A (V1) Advocate: concessions recorded
Concedes D-02 (pattern refuses pytest), D-03 (omits stamp), D-05 (module heavier than needed), D-07 default (item time), D-10 (op id), and prefers V2 on D-11 (A1 sections 2 and 3). Net per A1: V1 wins D-01 scope, D-04, D-09 and the framing of A-002 (A1 section 4).

### Variant B (V2) Advocate: concessions recorded
Lists six weaker areas of V2: D-04, D-01 (no label/project), D-09 (no compare-and-set), D-05 (no coupling test), D-07 (no "unreadable time voids"), D-08 (time rule before approval reread) (A2 section 3). Lists its strengths: D-02, D-03, D-07 default, D-08 specific reason, Q-7 counted hits, Q-10 Constraints line, `[SCOPE+]` flags (A2 section 4).

### Variant C (V3) Advocate: concessions recorded
Holds C-1 (convention), the DF-14 purpose, ranking, rollback notes, honest "unverified" marks. Yields on D-01, D-02/C-5, D-03, D-05/C-2, D-09, D-10, the D-12 default-value aside, Q-7 scope. D-04 and D-07 are marked owner-facing choices (A3 section 4).

## Round 2: Rebuttals

Round 2 was run by the orchestrator over the eight contested points (R2 section 1). Points settled in Round 1 and not reopened (R2 preamble): D-02 narrow V2 pattern, D-03 bump to 2, D-09 compare-and-set plus V2 refusal words, D-12 reject the default-value trick, C-2 no config key for the gate, A-001, A-002, A-007, Q-9 and Q-10. Facts used are in R2 section 0 (guard case run, pattern run on 13 commands, recount of 45 `--pipeline none` lines in 7 files, `_PENDING` has 12 entries, GitHub docs extract confirms `createdAt` on the single-select value type, `updatedAt` for that type not seen).

| R2 point | Level | Side for / rebuttal against | Verdict (R2 section 1) |
|---|---|---|---|
| (1) D-04 | L3 | H hard-refuse: total outage for a one-login workspace; A1 concedes 0.5. W warn-first: costs a closed-set config key and new warning output. R residual-only: V2's own residual risk 1 admits it does not close self-approval | Warn-first, owner decision recorded. Conf 0.70. Convergence 3/3 |
| (2) C-1 / D-08 | L3 | V1/V2: specific reason, tells the owner the remedy; plan:71 is owner-derived. V3: convention, both reasons are `("skip", 0)`. The equality check is a backstop for a fail-open time rule | V1 order: approval reread, time rule (`edited_after_approval`), equality (`revalidation_failed`). Conf 0.65. Convergence 2/3 |
| (3) D-05 | L3 | V1 module with coupling test versus V2 single constant; the A2 per-level split would pick a side in the claim.md:133 versus design:201 conflict | V2 Option A single constant plus a ~5-line coupling test; one `level_gated` REASON_TABLE row; gate in `_examine`. Conf 0.75. Convergence 3/3 |
| (4) D-07 | L3 | V1's item time risks total outage; V2 is silent on an unreadable time | V2 Option C with V1's "unreadable time voids" and V3's same-second test; item time excluded from the default. Conf 0.75. Convergence 3/3 |
| (5) D-02 extra | L3 | For (A1 0.5): closes the module-call spelling. Against: the guard is text-only, so it closes one spelling | Add `*issue_pipeline*complete.run*`, best-effort. Conf 0.55. Convergence 1/3 strict (lenient 3/3) |
| (6) D-01 merged | L3 | V3 narrow leaves close/reopen etc. to the command-position-only UNKNOWN row. New finding: `project item-list` and `project field-list` do not match `*' list'` | `'issue '*`, `'label '*`, `'project '*` after row 652, with `item-list` and `field-list` allowed first; class added to the `for LL_C` list at guard:788. Conf 0.75. Convergence 2/3 on merged scope |
| (7) D-11 | L2 | 1 file (V1/V3) versus 7 files (V2); recount confirms 45 lines in 7 files | V2's 7 files plus V1's tip. Conf 0.85. Convergence 3/3 |
| (8) D-10 | L2 | Static marker (V2/V3; A1 and A2 conceded) versus per-run (V1; A3). A static marker suppresses the second run's comment | Per-run marker keyed on the approval event id, not the op id. Conf 0.65. Convergence 1/3 strict |

## Scoring Matrix

Winner is the variant whose approach the verdict adopts as its core (additions from others noted). "Both" means V1 and V2 share the winning position and V3 loses. Evidence cites the round file section. Level is L1/L2/L3.

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| D-01a guard class: catch-all `'issue '*` after row 652 | L3 | V2 | 75% | R2 point 6; guard:646-655 plus case run: reads stay allowed, `issue close` refused; A1 and A2 take it, A3 concedes |
| D-01b `label` and `project` verbs in the class | L3 | V1 | 75% | R2 point 6; plan:23 (owner decision) and guard R17; `item-list`/`field-list` allowed first; A3 treats as optional (2/3) |
| D-02 / C-5 narrow coordinator-only pattern | L3 | V2 | 85% | R1 settled; case run: V1/V3 pattern refuses `pytest tests/issue_pipeline/test_complete.py` (R2 section 0) |
| D-02 extra `*issue_pipeline*complete.run*` | L3 | No variant (A1 proposal) | 55% | R2 point 5; 1/3 strict; best-effort only; WEAK ROW |
| D-03 guard version stamp to 2 | L3 | V2 | 90% | R1 settled; guard:10, orca_worktree.py:839 and :987 (A2) |
| D-04 self-approval exclusion | L3 | V1 (mechanism, softened to warn-first) | 70% | R2 point 1; source.md:64, predicates.py:216-223; owner decision recorded |
| D-05 gate form | L3 | V2 (V1's coupling test added) | 75% | R2 point 3; claim.md:133 versus design:201 mismatch; A1's size argument |
| D-06 / C-2 who can open the gate | L3 | Both (V3 loses) | 85% | R1 settled; guard:763-765 does not protect `~/.config/superclaude`; 3/3 |
| D-07 updatedAt approach | L3 | V2 (V1's unreadable-voids rule and V3's same-second test added) | 75% | R2 point 4; github.py:84-100 reads no time today; docs show `createdAt`; `updatedAt` on single-select unconfirmed |
| D-08 / C-1 reason precedence | L3 | V1 (V2 close) | 65% | R2 point 2; plan:71 versus plan:108; cycle.py:1012-1016; 2/3 |
| D-09 Status move target | L3 | V1 (V2 refusal words added) | 80% | R1 settled; predicates.py:268; read-then-write is not atomic (A3) |
| D-10 marker | L2 | V1 (idea only; key changed to approval event id) | 65% | R2 point 8; record.py:545-547, plan:141; overrules 2 of 3 advocates; WEAK ROW |
| D-11 Q-7 test move | L2 | V2 | 85% | R2 point 7; recount 45 lines in 7 files; launch.py:101 rejects the old prompt |
| D-12 / C-4 `String!` | L1 | Both (V3 loses) | 85% | R1 settled; reject `$owner: String = "IronbellyOrg"` |
| D-13 Q-9 governed sessions | L1 | Convergent, no winner | n/a | diff-analysis section 6; 3/3 |
| D-14 Q-10 ordering | L1 | Convergent (V2 Constraints line is the fuller text) | n/a | diff-analysis section 6; 3/3 |
| A-001 pr-submit still works | L3 | Shared assumption, no winner | 75% | all three variants; script path unseen by the guard |
| A-002 script bypass | L3 | Shared assumption (V1 names the fix) | 85% | guard:774-775; credential separation is a Coder row |
| A-007 fail-closed cost | L2 | Shared assumption | 70% | owner confirms once; messages must be owner-readable |

Debate win count used by the base-selection tiebreaker (13 scored points: D-01a, D-01b, D-02, D-03, D-04, D-05, D-06, D-07, D-08, D-09, D-10, D-11, D-12): V2 wins 6 outright (D-01a, D-02, D-03, D-05, D-07, D-11) plus half of the 2 shared points (D-06, D-12) = 7.0; V1 wins 5 outright (D-01b, D-04, D-08, D-09, D-10) plus 1.0 from the shared points = 6.0; V3 wins 0. Shares: V2 53.8%, V1 46.2%, V3 0%. D-02 extra is excluded (no variant owns it).

## Convergence Assessment

Per `round2-rebuttals.md` section 3. Rule: a point scores the advocates (of 3) whose stated Round 1 position equals the verdict without a further concession; an advocate that never addressed the alternative does not count.

| Figure | Value |
|---|---|
| Overall (18 rows, including those settled in Round 1) | 48 of 54 votes = 0.889, reaches the 0.80 threshold |
| Contested eight (D-04, C-1, D-05, D-07, D-02 extra, D-01 merged at 2/3, D-11, D-10) | 18 of 24 = 0.750, does not reach 0.80 |
| Lenient (silent advocates counted as not opposed) | contested eight 20 of 24 = 0.833; overall 50 of 54 = 0.926 |
| Rows below 0.80 | 4 of 18: D-01 label/project 0.67, D-08 0.67, D-02 extra 0.33, D-10 0.33 |

- Points resolved: 18 of 18 have a verdict; 14 at or above 0.80
- Alignment: 88.9%
- Threshold: 80%
- Status: CONVERGED (overall figure). The contested-eight figure of 75.0% is below the threshold and is reported as it stands.
- Unresolved points (below 0.80): D-01b, D-08 / C-1, D-02 extra, D-10. R2 section 3 says a third round would be needed only if the owner wants unanimity; none of the four blocks the merge.

## Rows flagged for owner awareness (weak rows)

| Row | Why weak | What the owner may want to check |
|---|---|---|
| D-10 marker | The verdict overrules 2 of 3 advocates (A1 and A2 for the constant); the deciding point (A3, plan:141 idempotency) was not answered by A1 or A2; the key choice (approval event id) is the orchestrator's own reading of record.py:545-547 and no advocate argued it (R2 section 4). Conf 0.65; strict convergence 1/3 | Whether a second run on the same issue should post a second result comment (R2 point 8) |
| D-02 extra (`*issue_pipeline*complete.run*`) | Never debated by two of three advocates; strict convergence 1/3 (lenient 3/3, nobody opposes); conf 0.55; closes one spelling only and the guard is text-only | Accept as best-effort, not a control (A-002) |

Rows also under the 0.80 line but not flagged weak by R2: D-01b (label/project, 2/3, conf 0.75) and D-08 (2/3, conf 0.65).
