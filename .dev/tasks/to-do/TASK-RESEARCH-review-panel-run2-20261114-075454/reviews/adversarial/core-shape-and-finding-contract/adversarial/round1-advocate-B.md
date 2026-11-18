# Round 1: Advocate B (Proposal B: thin shared contract, per-module engines)

Model: opus. Persona: architect + qa. Focus: correctness, risk, test-coverage. Code checked read-only at HEAD 50d4d2b9d.

## Position summary
Variant B's core claim holds up against the code: the two pipelines are separate today, the v1 ledger already rejects any finding without an anchor at the parser, and running the shipped spec loop on the v2 kernel would break its clustering. B was wrong about the crash. Its guard in section 2.3, evidence E-3 and the boundary test in 5.2 are built on a `KeyError` that `merge_round` cannot reach, so the guard should be withdrawn and 5.2 rewritten to pin the rejection the parser already makes.

## Steelman of Variant A
- **One place for each rule.** One parser and one drop rule mean the limits, the repair step and the locator policy each live in one place. Today v2 does copy v1's limits as literal numbers (`findings_v2.py:111,114-120,126,128,132,136`) [VERIFIED by me in code]. So the duplication A warns about already exists for constants.
- **The kernel already names the spec loop.** `LENSES` includes `"spec"` (`findings_v2.py:36`), `PRIMARY_ROLES["spec"]` exists (`cluster.py:67-71`), and v2 accepts an anchor or citations (`findings_v2.py:122-125`) [VERIFIED by me in code].
- **A found a real stuck-row defect that B missed.** A finding whose anchor is not found keeps `span None` (`findings.py:349-352`; pinned by `test_review_ledger.py:408-417`). `apply_revision` only moves a row to `resolved_check` when a change touches its span (`ledger.py:331-339`). Such a row can never be cleared by a fix and stays blocking until escalation [VERIFIED by me in code].
- **A's tests are mechanical and strong.** T1 (every existing test passes unmodified) and T2 (the same reviews produce the same ledger file) are real acceptance gates. Retrofitting later does get more expensive as more tests pin the v1 path.

## Strengths claimed
1. **The pipelines are separate, and the v1 ledger already refuses anchorless findings.** `parse_block` reads only a `findings-v1` block (`findings.py:126`), so a `findings-v2` block is invisible to `merge_round`. Inside a v1 block, `_check_finding` runs `_check_flat(obj.get("anchor"), "anchor", 12, 200)` (`findings.py:104`), and `_check_flat` returns "anchor must be a string" for `None` (`findings.py:80-81`). The line is dropped as an error (`findings.py:188-192`). `annotate` only ever sees parsed findings (`ledger.py:135-136`), and its only caller in `src` is `merge_round` (codegraph: `merge_round` plus three tests) [VERIFIED by me in code]. This backs E-1: no code path leads from v2 findings into the ledger.
2. **Moving the spec loop onto `cluster_v2` would stop it merging duplicates. This is decisive against A on C-004.** The v2 `annotate` builds its view from citations only. With no citations there is no primary citation and the fingerprint is `None` (`cluster.py:126-154`). `same_defect_v2` then needs a resolved citation on both sides (`cluster.py:170-181`). The test `test_finding_without_citations_has_no_primary_and_stays_alone` (`test_review_cluster.py:279-293`) pins that two identical anchor-only findings from two reviewers form two separate clusters [VERIFIED by me in code]. A keeps anchors required for the spec loop but says new ledgers use `cluster_v2`. That combination turns off all agreement between reviewers in the shipped loop, and A's own differential-replay test (T2) would fail.
3. **The v2 kernel is not yet a general superset.** `check_finding` enforces the six v1 categories on every line (`findings_v2.py:109-110`) [VERIFIED by me in code]. Module-declared vocabularies (research/13 item M2) are new work under either design, so A's "profile is data" is a design to build, not something reachable today.
4. **Duplicate cost is projected, not observed.** `findings.py` and `ledger.py` were last changed in `9163bd1c7` (2026-11-11). `findings_v2.py` and `cluster.py` have only `d2d8a2d16` (2026-11-12) [VERIFIED by me, git log]. The defect that does affect both pipelines, the reference-token pattern, sits in one shared function: `cluster.annotate` calls `findings.refs_norm` (`cluster.py:64,141`; pattern at `findings.py:29`) [VERIFIED by me in code].
5. **The shipped loop is heavily pinned.** `review-ledger/1|findings-v1` appears 26 times in 10 files under src, plugins and tests [VERIFIED by me, Grep count]. That is the risk A's rewrite takes on.
6. **The re-review `prior` line does nothing today.** Prior lines are only recorded as `prior_note` history and never change a status (`ledger.py:259-272`) [VERIFIED by me in code]. A's new re-review line type would change the brief text and its plugin mirror (invariant INV-N) without changing any outcome. B's deferral costs nothing.
7. **The B parts that survive the correction are useful.** The defect-locality table (3.2), the pre-registered decision rule (5.3) and the named convergence trigger (5.4) turn "converge later" into a falsifiable plan.

## Weaknesses identified in Variant A
1. **A-001 is false for A.** E2, the CO-1 answer, T4 and point 3 of section 8 ("the loss that does not go away ... a v2 citation-only finding crashes the ledger path") all rest on a crash `merge_round` cannot reach (strength 1). A's main reason to rewrite now loses its strongest current harm.
2. **A's clustering plan (CO-3) breaks the loop it says it keeps.** See strength 2. The section resolver idea does not help, because the fingerprint is `None` without a resolved citation (`cluster.py:143-147`) [VERIFIED by me in code]. A would have to build citations from anchors, which it does not specify.
3. **"`findings-v2` is the superset" overstates the kernel.** It enforces v1's categories (`findings_v2.py:109-110`), is one commit old, and runs only in shadow mode.
4. **The new re-review line type is a cost with no effect today.** It is inert (strength 6) and moves mirror-pinned brief text.
5. **A adds new on-disk ledger state.** A clustering marker in the header and a `citations` list in rows are added to a file whose header today is `schema, doc, cap_reviews, rounds, rows` (`ledger.py:38`) [VERIFIED by me in code]. That puts the stored-ledger invariant (INV-D) at risk for no current consumer.
6. **The fix for A's best point does not need A's design.** The stuck-row fix (FX-2, A's E11) can be made inside the v1 engine, with a policy for missing anchors and a test like A's T5, without merging engines.

## Concessions
1. **B's 2.3 guard, E-3 and 5.2 are wrong as written.** E-3's claim that the crash is "reached from `merge_round`" is contradicted by the code. When the only reviewer submits only citation-only lines, the existing refusal raises `LedgerError` with "no reviewer produced a valid findings block" (`ledger.py:150-157`, pinned by `test_review_ledger.py:345-373`), and the `merge` command turns it into exit 1 (`merge_cmd.py:111-112`) [VERIFIED by me in code]. So 5.2's stated behaviour already passes with zero new code. In a round with several reviewers, the line is dropped with a warning and `block_ok` is set to false.
   - Correction: withdraw the guard.
   - Restate 5.2 as a test that pins today's parser rejection, in both the one-reviewer and several-reviewer cases.
   - Name the real gap instead: a citation-only line is lost with only a warning, and that interacts with the open fail-open questions in slots C-02 and C-03.
   - Net effect: B's boundary already exists and costs nothing. B loses one of its listed contributions.
2. **B missed the stuck-row defect** (A's E11), which is real and blocking-relevant.
3. **B keeps a lasting cost.** Two clusterers, two fingerprints and two location types remain, and the limit literals are duplicated in v2 today.
4. **The projection view (2.1) has no consumer yet.** Under B's own scope rule it is speculative.
5. **The trigger thresholds in 5.4** ("two defects in one quarter") have no evidence behind them.
6. **"Closed at the PR adapter"** for unknown keys is a new policy with no supporting evidence.

## Shared assumption responses
- **A-001 (a citation-only finding crashes `merge_round`): REJECT.** Verified: `findings.py:104` with `:80-81` drops the line at parse, and `ledger.py:135-136` annotates only parsed findings. The `KeyError` happens only when `annotate()` is called directly. Both variants must restate.
- **A-002 (reviewers give usable line numbers for a document): QUALIFY.** Neither variant shows how line numbers reach reviewers in the ledger path. B needs it only for code targets and the document arm of 5.3. A needs it in the loop whenever a module requires citations. It is UNVERIFIED, and 5.3 or T3 must test it before either design relies on it.
- **A-003 (the v2 kernel is stable enough to build on): QUALIFY.** It is one commit old (verified), runs in shadow mode, enforces v1 categories, and cannot cluster anchor-only findings (verified). That makes it unready to host the shipped loop, which is load-bearing for A. It is acceptable as the engine for reflect and the future PR module under B, because B shares only helpers with it.
- **A-004 (neither location type is proven reliable enough to drop the other): ACCEPT.** There is no measurement comparing the two. Both variants' tests (5.3 and T3) exist to supply one.
- **A-005 (verdict and clearing fixes land in the one multi-reviewer ledger): ACCEPT.** `ledger.py` is the only ledger in the product (verified, `ledger.py:1-5,107`).

## Per-point assessment table
| Point | Superior | Conf. | Reason |
|---|---|---|---|
| S-001 | A (CONCEDE) | 70% | A's per-row table answers each routed conflict row explicitly; B scatters the answers across sections. |
| S-002 | B | 70% | A falsifiable convergence trigger is more actionable than a list of open points. |
| S-003 | NEITHER | 55% | Different groupings, with no effect on correctness. |
| S-004 | A (CONCEDE) | 60% | A covers more invariants (G, H, M) and states a level for each. |
| S-005 | HYBRID | 75% | A's T1, T2 and T5 plus B's 5.1 and pre-registered 5.3; both crash tests (A's T4, B's 5.2) must be rewritten per A-001. |
| C-001 | B | 75% | The pipelines are verified separate, the kernel is one commit old, and moving the loop onto it breaks clustering (`test_review_cluster.py:279-293`). |
| C-002 | B | 65% | No reachable crash means no reason to rewrite `annotate` now; B's guard is also unnecessary, so the honest answer is to defer and pin today's parser rejection. |
| C-003 | B | 65% | `prior` is inert (`ledger.py:259-272`); a new line type moves mirror-pinned brief text for no outcome. |
| C-004 | B | 85% | `cluster_v2` never joins anchor-only findings, so A's plan turns off reviewer overlap in the shipped loop. |
| C-005 | HYBRID | 60% | Open unknown keys by default (A) fits with strictness only where one module owns both ends (B). |
| C-006 | HYBRID | 55% | The ledger member record drops extra keys today (`ledger.py:172-180`); an additive passthrough is cheap under either design, but no consumer needs it yet. |
| C-007 | B | 65% | One repair step before parsing gives a single place without merging parsers. |
| C-008 | A (CONCEDE) | 70% | A found the verified stuck-row defect (`ledger.py:331-339`); B is silent. The fix still fits inside the v1 engine. |
| C-009 | HYBRID | 60% | The PR path needs no ledger today (B), and module vocabularies are needed under both (`findings_v2.py:109-110`). |
| C-010 | B | 60% | "Untested, not disproved" matches the evidence; A's "the core supplies the snapshot" is an untested design inference. |
| X-001 | B | 75% | With the crash unreachable and `cluster_v2` unfit for anchors, converging now pays real cost for no current consumer. |
| X-002 | B | 65% | The only duplicated defect is in shared `refs_norm`, and git history shows no paid duplication; A is partly right that the limit literals are copied. |
| X-003 | B | 75% | The rewrite touches the path pinned 26 times in 10 files, and its stated clustering plan would fail A's own T2. |
| X-004 | HYBRID | 60% | Same as C-005: the two policies are compatible. |
| X-005 | NEITHER | 85% | Both fix an unreachable crash. The real issues are the stuck row (A's E11) and the citation-only line lost with only a warning. |
| A-001 | NEITHER | 90% | Both variants built on a false premise (`findings.py:104`, `ledger.py:135-136`). |
| A-002 | NEITHER | 65% | Both left it unstated. B is less exposed because it does not put citations in the loop. |
| A-003 | B | 70% | A depends on kernel maturity, which the code does not support. B shares only helpers. |

Not checked: the research files cited as UNVERIFIED in both variants, the line in `cluster.py` where v2 clustering drops a whole reviewer (256-257 was read only as `if not r["valid"]: continue`), and how line numbers reach reviewers (A-002).

Files read (all under /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/):
- src/superclaude/cli/review/findings.py
- src/superclaude/cli/review/ledger.py
- src/superclaude/cli/review/findings_v2.py
- src/superclaude/cli/review/cluster.py
- src/superclaude/cli/review/merge_cmd.py (Grep only)
- tests/review/test_review_cluster.py
- tests/review/test_review_ledger.py
