# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals) plus Round 2.5 invariant probe; Round 3 not run (depth standard)
- Convergence achieved: 100% of diff points agreed (23 of 23) after Round 2; 78.3% (18 of 23) after Round 1; status BLOCKED_BY_INVARIANTS (see Convergence Assessment)
- Convergence threshold: 80%
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2 (advocate-A-c01-r1 for Variant A, advocate-B-c01-r1 for Variant B; model opus, persona architect + qa)
- Fault-finder (Round 2.5): fault-finder-c01-r25 (independent, not an advocate)
- Orchestrator note: the advocates were first told to return their answers as a message; they were then asked to persist them as files (`round1-advocate-*.md`, `round2-advocate-*.md`). The sections below embed those files verbatim. Round 2 ran sequentially: A first (after reading B's Round 1), then B (after reading A's Round 2).
- Shared-assumption responses (all five A-NNN answered by both advocates in Round 1): no omissions.

## Round 1: Advocate Statements

### Variant A Advocate (opus:architect+qa)
##### Position summary
Variant A is still the right long-term target: one parser whose v1 and v2 grammars are data profiles, and a ledger that does not care which kind of locator a finding uses. But two of A's load-bearing claims are wrong in the code. The `merge_round` crash cannot happen, and `cluster_v2` cannot cluster anchor-only findings. So the correct ruling on core shape is a HYBRID: build B's thin contract now, and take A's profile-and-locator design as the convergence target.

##### Steelman of Variant B
The two pipelines really are separate today. Nothing in `ledger.py`, `merge_cmd.py` or `ledger_cmd.py` imports from v2 (B E-1). Both kernels are two to three days old, with one commit each. I ran git log: `findings.py` and `ledger.py` were last touched in 9163bd1c7 on 2026-11-11, and `findings_v2.py` and `cluster.py` only in d2d8a2d16 on 2026-11-12 [VERIFIED by me in code]. So "you will fix every defect twice" is a projection, not a cost anyone has paid yet.

The defects that both engines share are already fixable once without merging the engines:
- `refs_norm` is one function, used by both `findings.annotate` (`findings.py:357`) and `cluster.annotate` (`cluster.py:141`).
- The v1 length limits are literals at `findings.py:104,108,114,118`. A shared constants module plus one repair step before parsing covers the drop of over-limit lines (FX-1) for both parsers [VERIFIED by me in code].

No current consumer needs a re-review ledger over citation-located findings. B also names a trigger that would prove it wrong (5.4) and a measurement rule fixed before the first run (5.3). Rewriting the shipped, test-pinned spec loop before then means paying a certain risk for a benefit nobody has asked for.

##### Strengths claimed
1. **The grammars already differ only by data, so a parser profile fits the code that exists.** `findings_v2.py:15-22` imports `_ID`, `CATEGORIES`, `SEVERITIES`, `_blocks_after` and `_check_flat` from v1. The only rule differences are:
   - anchor required (`findings.py:104`) versus anchor or citations (`findings_v2.py:122-134`);
   - `calibrated_confidence` rejected in v2 (`:96-97`);
   - `prior` lines accepted in v1 (`findings.py:175-187`) versus rejected in v2 (`findings_v2.py:279-283`).

   [VERIFIED by me in code]
2. **The ledger only ever works on spans.** `apply_revision` uses only `hunks_touch` and `map_span` over `span` and `span2` (`ledger.py:331-346`). So a ledger that accepts either locator only needs a way to turn a citation into a span. It does not need a new matching engine [VERIFIED by me in code].
3. **A fixes a real stuck-row defect that B leaves in place.** When an anchor is missing, `annotate` stores `span None` (`findings.py:352`). `hunks_touch(None, ...)` returns False (`findings.py:446-447`). So `apply_revision` records `named_not_touched` and the row can never reach `resolved_check` (`ledger.py:331-339`). A's locator policy as profile data, with a citation fallback (FX-2, T5), is the only proposal that addresses this [VERIFIED by me in code].
4. **The ledger drops a reviewer's extra keys.** Member records keep only `round`, `reviewer_id`, `fid` and `blocking` (`ledger.py:172-180`). B's claim that "in-line `origin` keeps working" is true at parse time, but the provenance is gone once the finding is in the ledger. A's declared pass-through keys (C-006) fix that [VERIFIED by me in code].
5. **The v2 kernel is not neutral about vocabulary.** `check_finding` enforces the six spec `CATEGORIES` on every line (`findings_v2.py:109-110`). So a PR review or rf-qa module cannot use it as it stands. A's design makes vocabularies profile data, and that work is needed under either shape [VERIFIED by me in code].
6. **A's T2 (replay the same input through old and new paths and compare) and T5 (row-clearing probe) are measurable acceptance rules** built on fixtures that are already committed [from the proposal, not re-checked: fixture coverage].

##### Weaknesses identified in Variant B
1. **B's one boundary guard (2.3) can never run.** `merge_round` gets its findings from `fnd.parse_block` (`ledger.py:128`). That calls `_check_finding`, which calls `_check_flat(obj.get("anchor"), ...)`. With no anchor this returns "anchor must be a string" (`findings.py:80-81,104-106`), so the line is dropped before `annotate` runs (`ledger.py:135-136`). A `LedgerError` at that point would be dead code. [VERIFIED by me in code]
2. **B's test 5.2 is specified wrongly.**
   - If the citation-only line sits alongside valid lines, today no error is raised; the line is dropped with a warning (`ledger.py:130-134`).
   - If it is the only line, the existing zero-valid-block refusal raises (`ledger.py:150-157`). That message lists warnings and does not name the finding id.

   [VERIFIED by me in code]
3. **B guards a hole that does not exist and misses the one that does.**
   - The real gap: a citation-only blocking finding is silently dropped as an invalid line, and the merge goes ahead on the other reviewers' blocks.
   - Clearing does not check whether a reviewer's block was valid (`block_ok`). `ledger.py:254-258` clears rows in `resolved_check` purely because no member re-found them, even though the docstring at `ledger.py:112` says invalid reviewers are skipped for clearing.
   - Net effect: a dropped re-find can let a row clear. That breaks the fail-closed invariant (INV-I).

   A does not name this either, but A's typed locator path at least moves the finding into the ledger. [VERIFIED by me in code]
4. **B leaves the verified stuck row (strength 3) untouched** and defers it to a measurement that has not been run.
5. **B's projection view (U-009) is a new artifact with no consumer today.** Under B's own "only build when a consumer pays for it" rule, it should be deferred too [from the proposal].
6. **B's trigger thresholds are unmeasured** ("two or more verified defects in one quarter"), as B admits in 5.4 [from the proposal].

##### Concessions
1. **E2 is wrong for the shipped path.** A citation-only finding cannot reach `annotate` through `merge_round`, because `parse_block` drops it first (weakness 1 above). The `KeyError` only happens if you call `findings.annotate()` directly. Its only source caller is `merge_round`; the other three callers are tests (codegraph callers) [VERIFIED by me in code].
   - CO-1's premise ("cannot enter the ledger path") is half right: the finding cannot enter, but because a validator drops it, not because something crashes.
   - Section 8 answer 3 ("a v2 citation-only finding crashes the ledger path") is false. That removes one of A's three reasons to converge now.
   - T4 must be restated. As written ("never KeyError") it already passes today, trivially. It should say: a citation-only line produces a located row under a profile that accepts citations, and an invalid-line error that names the id under the `spec-loop` profile.
2. **CO-3 as written is broken: `cluster_v2` cannot cluster anchor-only findings.**
   - `cluster.annotate` builds its view only from `citations` (`cluster.py:128-134`).
   - The fingerprint is None unless a resolved primary citation exists (`:143-147`).
   - `same_defect_v2` compares only resolved citations (`:170-181`).

   So under A's own `spec-loop` profile (anchor required), "new ledgers use `cluster_v2`" would make every finding its own cluster, and A's T2 would fail by construction. A must either keep v1 clustering for `spec-loop` or add an anchor-span branch to `same_defect_v2`. The second option is more rewrite and more risk than A stated [VERIFIED by me in code].
3. **A rests on a kernel that is two days old, dormant and only running in shadow mode** (git log above). That is exactly the maturity question raised in A-003.
4. **A's typed re-review line kind changes the loop brief and its plugin mirror (INV-N) for no ledger effect today,** because `prior` lines are inert: they are only logged as a `prior_note` (`ledger.py:259-272`) [VERIFIED by me in code].
5. **The effort is large, the paths A rewrites are pinned by tests, and no consumer needs a citation ledger today.** B's "converge on a trigger" is the lower-risk timing.

##### Shared assumption responses
- **A-001 (the crash happens through `merge_round`): REJECT.** `parse_block` drops a line with no anchor before `annotate` runs (`findings.py:104`, `ledger.py:128-138`). The real defect is a silent drop plus clearing that ignores block validity (`ledger.py:254-258`).
- **A-002 (reviewers give usable line numbers for a document): QUALIFY.** Neither proposal shows how line numbers reach the reviewer in the ledger path, and no measurement exists. It must be measured by A's T3 or B's 5.3, with a document arm, before any module is made to require citations.
- **A-003 (the v2 kernel is stable enough to build on): QUALIFY.** `parse_block` in v2 is pinned against v1 compatibility (`test_review_findings_v2.py:70-81`). But `cluster_v2` only works with citations (concession 2), so it is not ready to be the spec loop's clustering. Sharing constants with it (B) is safe; making the loop a profile of it (A) needs new code first.
- **A-004 (neither location type is proven reliable enough to drop the other): ACCEPT.** Both proposals' evidence agrees, and the diff analysis reconciles the two sets of numbers as different scopes.
- **A-005 (verdict and clearing fixes land in the one multi-reviewer ledger): ACCEPT.** One extra item for C-02 and C-03: clearing must check block validity, as the `merge_round` docstring already claims (`ledger.py:112` against `:254-258`).

##### Per-point assessment table
| Point | Superior | Confidence | Reason |
|---|---|---|---|
| S-001 | A | 65% | A's answer to each routed row is easier to check than B's answers spread across sections. |
| S-002 | B (CONCEDE) | 70% | A trigger that can prove B wrong is stronger than an unordered list of open points. |
| S-003 | NEITHER | 55% | Grouping the evidence differently changes no conclusion. |
| S-004 | A | 55% | A rates each invariant's level, but both cover the same set. |
| S-005 | HYBRID | 70% | Take A's T2 and T5 plus B's 5.1 and 5.3. Rewrite A's T4 and B's 5.2, which both rest on the crash that cannot happen. |
| C-001 | HYBRID | 60% | B's thin contract now, A's profile parser as the target; A's "one engine now" lost its crash premise and its clustering plan. |
| C-002 | A | 60% | A's span-from-either-locator design is needed for any citation finding to enter, and it fixes the verified stuck row; B's guard is dead code. |
| C-003 | B (CONCEDE) | 60% | `prior` is inert today, so A's new line kind costs a brief and mirror change for no effect. |
| C-004 | B (CONCEDE) | 75% | `cluster_v2` cannot match anchor-only findings (`cluster.py:128-181`), so A's plan breaks the spec loop's clustering. |
| C-005 | HYBRID | 55% | Open keys in the core plus closed keys at the PR adapter do not conflict. |
| C-006 | A | 60% | The ledger drops pass-through keys (`ledger.py:172-180`); only A keeps the provenance. |
| C-007 | B (CONCEDE) | 65% | Shared constants plus a repair step before parsing fixes the over-limit drop for both parsers without merging engines. |
| C-008 | A | 65% | The stuck row with no span is a verified defect; only A's locator policy and citation fallback addresses it. |
| C-009 | HYBRID | 55% | PR review needs no ledger (B), but both need vocabularies as data because v2 enforces spec categories (`findings_v2.py:109-110`). |
| C-010 | HYBRID | 60% | Both read the evidence correctly as "citations untested"; the numbers agree once scoped. |
| X-001 | B (CONCEDE) | 65% | The crash cannot happen and no consumer needs a citation ledger, so converging on a trigger is lower risk. |
| X-002 | B (CONCEDE) | 60% | The shared defects sit in shared helpers, and git history shows no cost has been paid twice. |
| X-003 | B (CONCEDE) | 65% | The rewrite is bigger than A stated, since `cluster_v2` needs an anchor branch. |
| X-004 | HYBRID | 55% | Same as C-005. |
| X-005 | NEITHER | 80% | Neither fix closes a real path. The real gap is the silent drop plus clearing that ignores block validity. |
| A-001 | NEITHER | 85% | The assumption is contradicted by the code; both proposals' fixes target a path that cannot be reached. |
| A-002 | B | 55% | B's pre-registered measurement with a document arm addresses it more directly than A's assumed mapping. |
| A-003 | B (CONCEDE) | 65% | The v2 kernel is two days old and can only cluster citations; that is fine for sharing constants, not for hosting the loop. |

| Status | Result |
|---|---|
| DONE | Read both variants, the diff analysis, and `findings.py`, `findings_v2.py`, `cluster.py` and `ledger.py` at HEAD. Checked the callers of `annotate` and the git history of all four modules. |
| DONE | Confirmed the orchestrator's check: the `merge_round` crash cannot happen. Found two new facts: `cluster_v2` only works with citations, and clearing ignores block validity. |
| NEXT | Route the clearing defect (rows clear while a reviewer's re-find was dropped) to slots C-02 and C-03. |

Not checked: whether `anchor_status` and `anchor_ambiguous` are read anywhere, the skill tests under `tests/skills/`, and the E1 and E2 run counts. All of those are taken from the proposals.

### Variant B Advocate (opus:architect+qa)

#### Round 1: Advocate B (Proposal B: thin shared contract, per-module engines)

Model: opus. Persona: architect + qa. Focus: correctness, risk, test-coverage. Code checked read-only at HEAD 50d4d2b9d.

##### Position summary
Variant B's core claim holds up against the code: the two pipelines are separate today, the v1 ledger already rejects any finding without an anchor at the parser, and running the shipped spec loop on the v2 kernel would break its clustering. B was wrong about the crash. Its guard in section 2.3, evidence E-3 and the boundary test in 5.2 are built on a `KeyError` that `merge_round` cannot reach, so the guard should be withdrawn and 5.2 rewritten to pin the rejection the parser already makes.

##### Steelman of Variant A
- **One place for each rule.** One parser and one drop rule mean the limits, the repair step and the locator policy each live in one place. Today v2 does copy v1's limits as literal numbers (`findings_v2.py:111,114-120,126,128,132,136`) [VERIFIED by me in code]. So the duplication A warns about already exists for constants.
- **The kernel already names the spec loop.** `LENSES` includes `"spec"` (`findings_v2.py:36`), `PRIMARY_ROLES["spec"]` exists (`cluster.py:67-71`), and v2 accepts an anchor or citations (`findings_v2.py:122-125`) [VERIFIED by me in code].
- **A found a real stuck-row defect that B missed.** A finding whose anchor is not found keeps `span None` (`findings.py:349-352`; pinned by `test_review_ledger.py:408-417`). `apply_revision` only moves a row to `resolved_check` when a change touches its span (`ledger.py:331-339`). Such a row can never be cleared by a fix and stays blocking until escalation [VERIFIED by me in code].
- **A's tests are mechanical and strong.** T1 (every existing test passes unmodified) and T2 (the same reviews produce the same ledger file) are real acceptance gates. Retrofitting later does get more expensive as more tests pin the v1 path.

##### Strengths claimed
1. **The pipelines are separate, and the v1 ledger already refuses anchorless findings.** `parse_block` reads only a `findings-v1` block (`findings.py:126`), so a `findings-v2` block is invisible to `merge_round`. Inside a v1 block, `_check_finding` runs `_check_flat(obj.get("anchor"), "anchor", 12, 200)` (`findings.py:104`), and `_check_flat` returns "anchor must be a string" for `None` (`findings.py:80-81`). The line is dropped as an error (`findings.py:188-192`). `annotate` only ever sees parsed findings (`ledger.py:135-136`), and its only caller in `src` is `merge_round` (codegraph: `merge_round` plus three tests) [VERIFIED by me in code]. This backs E-1: no code path leads from v2 findings into the ledger.
2. **Moving the spec loop onto `cluster_v2` would stop it merging duplicates. This is decisive against A on C-004.** The v2 `annotate` builds its view from citations only. With no citations there is no primary citation and the fingerprint is `None` (`cluster.py:126-154`). `same_defect_v2` then needs a resolved citation on both sides (`cluster.py:170-181`). The test `test_finding_without_citations_has_no_primary_and_stays_alone` (`test_review_cluster.py:279-293`) pins that two identical anchor-only findings from two reviewers form two separate clusters [VERIFIED by me in code]. A keeps anchors required for the spec loop but says new ledgers use `cluster_v2`. That combination turns off all agreement between reviewers in the shipped loop, and A's own differential-replay test (T2) would fail.
3. **The v2 kernel is not yet a general superset.** `check_finding` enforces the six v1 categories on every line (`findings_v2.py:109-110`) [VERIFIED by me in code]. Module-declared vocabularies (research/13 item M2) are new work under either design, so A's "profile is data" is a design to build, not something reachable today.
4. **Duplicate cost is projected, not observed.** `findings.py` and `ledger.py` were last changed in `9163bd1c7` (2026-11-11). `findings_v2.py` and `cluster.py` have only `d2d8a2d16` (2026-11-12) [VERIFIED by me, git log]. The defect that does affect both pipelines, the reference-token pattern, sits in one shared function: `cluster.annotate` calls `findings.refs_norm` (`cluster.py:64,141`; pattern at `findings.py:29`) [VERIFIED by me in code].
5. **The shipped loop is heavily pinned.** `review-ledger/1|findings-v1` appears 26 times in 10 files under src, plugins and tests [VERIFIED by me, Grep count]. That is the risk A's rewrite takes on.
6. **The re-review `prior` line does nothing today.** Prior lines are only recorded as `prior_note` history and never change a status (`ledger.py:259-272`) [VERIFIED by me in code]. A's new re-review line type would change the brief text and its plugin mirror (invariant INV-N) without changing any outcome. B's deferral costs nothing.
7. **The B parts that survive the correction are useful.** The defect-locality table (3.2), the pre-registered decision rule (5.3) and the named convergence trigger (5.4) turn "converge later" into a falsifiable plan.

##### Weaknesses identified in Variant A
1. **A-001 is false for A.** E2, the CO-1 answer, T4 and point 3 of section 8 ("the loss that does not go away ... a v2 citation-only finding crashes the ledger path") all rest on a crash `merge_round` cannot reach (strength 1). A's main reason to rewrite now loses its strongest current harm.
2. **A's clustering plan (CO-3) breaks the loop it says it keeps.** See strength 2. The section resolver idea does not help, because the fingerprint is `None` without a resolved citation (`cluster.py:143-147`) [VERIFIED by me in code]. A would have to build citations from anchors, which it does not specify.
3. **"`findings-v2` is the superset" overstates the kernel.** It enforces v1's categories (`findings_v2.py:109-110`), is one commit old, and runs only in shadow mode.
4. **The new re-review line type is a cost with no effect today.** It is inert (strength 6) and moves mirror-pinned brief text.
5. **A adds new on-disk ledger state.** A clustering marker in the header and a `citations` list in rows are added to a file whose header today is `schema, doc, cap_reviews, rounds, rows` (`ledger.py:38`) [VERIFIED by me in code]. That puts the stored-ledger invariant (INV-D) at risk for no current consumer.
6. **The fix for A's best point does not need A's design.** The stuck-row fix (FX-2, A's E11) can be made inside the v1 engine, with a policy for missing anchors and a test like A's T5, without merging engines.

##### Concessions
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

##### Shared assumption responses
- **A-001 (a citation-only finding crashes `merge_round`): REJECT.** Verified: `findings.py:104` with `:80-81` drops the line at parse, and `ledger.py:135-136` annotates only parsed findings. The `KeyError` happens only when `annotate()` is called directly. Both variants must restate.
- **A-002 (reviewers give usable line numbers for a document): QUALIFY.** Neither variant shows how line numbers reach reviewers in the ledger path. B needs it only for code targets and the document arm of 5.3. A needs it in the loop whenever a module requires citations. It is UNVERIFIED, and 5.3 or T3 must test it before either design relies on it.
- **A-003 (the v2 kernel is stable enough to build on): QUALIFY.** It is one commit old (verified), runs in shadow mode, enforces v1 categories, and cannot cluster anchor-only findings (verified). That makes it unready to host the shipped loop, which is load-bearing for A. It is acceptable as the engine for reflect and the future PR module under B, because B shares only helpers with it.
- **A-004 (neither location type is proven reliable enough to drop the other): ACCEPT.** There is no measurement comparing the two. Both variants' tests (5.3 and T3) exist to supply one.
- **A-005 (verdict and clearing fixes land in the one multi-reviewer ledger): ACCEPT.** `ledger.py` is the only ledger in the product (verified, `ledger.py:1-5,107`).

##### Per-point assessment table
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

## Round 2: Rebuttals

### Variant A Rebuttal

#### Round 2: Advocate A (rebuttal)

Model: opus. Persona: architect + qa. Focus: correctness, risk, test-coverage. Code checked read-only at HEAD 50d4d2b9d. No file under the forbidden run-1 paths was read.

##### Response to criticisms

B Round 1, "Weaknesses identified in Variant A", answered one by one.

1. **"A-001 is false for A" (E2, CO-1, T4, section 8 point 3).** CONCEDED, as I already did in Round 1, concession 1. `findings.py:104` with `:80-81` drops a line with no anchor at parse time, and `ledger.py:135-136` annotates only lines that parsed. Section 8 point 3 is withdrawn as a reason to converge now.
2. **"A's clustering plan (CO-3) breaks the loop it says it keeps."** CONCEDED. I re-checked it myself (New evidence N1):
   - `cluster.annotate` builds its view from citations only.
   - The fingerprint is None without a resolved primary citation.
   - `same_defect_v2` needs a resolved citation on both sides.
   - `test_review_cluster.py:279-293` pins that two identical anchor-only findings stay as two clusters.

   The section-resolver idea does not rescue it, because the fingerprint does not exist in the first place. A's CO-3 answer is withdrawn.
3. **"`findings-v2` is the superset overstates the kernel."** CONCEDED, with one qualification. The superset claim holds for the eight v1 fields; that is pinned by `test_review_findings_v2.py:70-81`, which I read. It does not hold for vocabularies (`findings_v2.py:109-110` enforces v1 `CATEGORIES`) or for clustering (N1). "Profile as data" is a design still to be built, not something already reachable.
4. **"The new re-review line type is a cost with no effect today."** CONCEDED. `prior` lines are only logged as a `prior_note` (`ledger.py:259-272`). The typed line kind is withdrawn from C-01.
5. **"A adds new on-disk ledger state for no current consumer."** CONCEDED. The clustering marker in the header and the `citations` list in rows put the stored-ledger invariant (INV-D) at risk, and nothing reads them today. Both are withdrawn and deferred to the convergence trigger.
6. **"The fix for A's best point does not need A's design."** PARTLY CONCEDED.
   - A v1-local fix is possible, so A's merged engine is not needed for it.
   - What B does not show is which v1-local fix is safe. N3 shows the stuck row hits exactly the case where the fix worked: nobody re-finds the defect, so nothing re-anchors the row.
   - The only v1-local ways to release such a row are (a) a policy that marks it unlocated and asks the next round to locate it or say it is gone, or (b) letting a fix map entry for a row with no span reach `resolved_check`. Option (b) then clears purely because nobody re-found it, which is the fail-open clearing rule owned by C-02.
   - So the fix fits inside v1, but its safety depends on C-02. C-01 should fix only the locator policy, as data (`on_missing`, `on_ambiguous`), and hand the clearing semantics to C-02.

B's other claims I checked:
- **B concession 1** (the existing refusal raises `LedgerError`, and `merge` turns it into exit 1): VERIFIED. `merge_cmd.py:111-112` re-raises `LedgerError` as `click.ClickException`, which exits 1.
- **B strength 3** ("profile is data" is new work): ACCEPTED.
- **B C-002 ruling** ("defer and pin today's parser rejection"): ACCEPTED. That is now my position too (see the hybrid).

##### Updated assessment of Variant B
- B's core shape is right for C-01 now. The pipelines are separate, the v1 parser already enforces the anchor boundary, and the v2 kernel cannot host the anchor loop without new clustering code.
- B's two self-corrections are correct: withdraw the 2.3 guard, and rewrite 5.2 to pin today's rejection.
- Two B items still fail B's own rule of building only when a consumer needs it:
  - the projection view (2.1), which has no consumer;
  - "closed at the PR adapter" for unknown keys, which has no evidence behind it.
- B's trigger item 2 ("two defects in one quarter") has no measured basis and should be replaced by a mechanical test (see the hybrid).
- B's remaining gap: it gives no answer for the verified stuck row (E11). B conceded this in Round 1 (concession 2) but did not propose a locator policy.

##### New evidence
All read by me at HEAD, outside the forbidden paths.

- **N1. `cluster_v2` cannot join anchor-only findings.**
  - `cluster.py:128-134` builds `citations` from `finding.get("citations")` only.
  - `:134` gives `primary` None when there are no citations.
  - `:143-147` gives `fp` None unless the primary citation is resolved.
  - `same_defect_v2` (`:163-181`) has no anchor or span branch.
  - The test `test_finding_without_citations_has_no_primary_and_stays_alone` (`test_review_cluster.py:279-293`) asserts two clusters for two identical anchor-only findings, and `primary_citation is None`.
  - The test helper `fnd` always adds a default citation (`test_review_cluster.py:35`, `list(cits) or [cit()]`), so 279-293 is the only test of the anchor-only case. It would be one of the pins A's original CO-3 plan had to break, and A's T1 pin list missed it.
- **N2. Clearing ignores block validity, and this is not new: a test pins it as intended.**
  - Outside rendering and telemetry, `block_ok` is read only at `ledger.py:129,147,150,295`. The rest are the merged-report render (`:423`) and telemetry (`telemetry.py:67`).
  - The clearing loop at `ledger.py:254-258` never reads it.
  - `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` (`test_review_ledger.py:376-385`) asserts that L1 becomes `resolved` while reviewer `t2-1` has a broken block.
  - This is the "single-valid-block pass" defect that A section 5 item 6 already assigns to C-02 and C-03. I correct my Round 1 framing: it is not a new finding.
  - What is specific to C-01: `merge_round` keeps an invalid reviewer's lines that do parse (`ledger.py:135-138` runs whatever `parsed["ok"]` is), so only the dropped line is lost. A re-find that is dropped for format reasons (citation-only, anchor over 200 characters, claim over 300) therefore cannot hold its row open, and the row can clear in that round.
  - The docstring "skipped for clearing" (`ledger.py:112`) is not implemented for each reviewer.
- **N3. The stuck row hits exactly the "fix worked" case.**
  - A row with `span None` is kept open and blocking (`test_review_ledger.py:408-417`).
  - `apply_revision` records it as `named_not_touched` (`ledger.py:331-339`; `hunks_touch(None)` is False at `findings.py:446-447`).
  - The only way such a row gets a span is a later re-find with an anchor that can be located, since `merge_round` re-anchors from the current report (`ledger.py:226-231`).
  - If the fix worked, nobody re-finds the defect, so the row stays open and blocking until escalation.
  - No test pins this outcome. The 408-417 test pins only the state after round 1.
- **N4. Nothing outside tests reads `anchor_status` or `anchor_ambiguous`.**
  - A Grep over the repo (excluding `.dev/tasks/`) finds them written only at `findings.py:350-351`.
  - They are read only by `tests/review/test_review_findings.py:219,223,227,230`.
  - The remaining hits are vendored copies and notes under `.dev/research/` and `.dev/brainstorms/`, which are not product code.
  - The ledger row does not store them (`ledger.py:184-202`). Both flags are computed and then thrown away in the product path.
- **N5. The v1 parser has no key whitelist.** `_check_finding` (`findings.py:90-121`) checks only id, severity, blocking, category, anchor, anchor2, refs and claim. v2 rejects only `calibrated_confidence` (`findings_v2.py:96-97`), and its `check_finding` (`:84-187`) has no whitelist either. Unknown keys are open in both parsers today.
- **N6. The limit literals are duplicated in two places.** v1 has them at `findings.py:104` (anchor 12..200), `:108` (anchor2), `:114` (refs at most 8) and `:118` (claim at most 300). v2 restates them at `findings_v2.py:111,117,126,132,136` plus the citation quote at `:80`. That makes B's shared constants module a real, bounded deduplication.

##### Concrete hybrid you now stand behind

C-01 decision: **B's thin shared contract now, per-module engines, with A's locator policy as data added to the v1 engine. A's merged engine is recorded as the target if and when the convergence trigger fires.**

###### Shared core NOW
1. The finding id grammar `_ID`, already shared.
2. One limits constants module imported by both parsers (N6). Names must be checked against the reserved contract-constant names (`make lint-architecture` Check 11, INV-K).
3. One repair step that runs before either `parse_block`. The policy is decided by C-06; C-01 fixes only where it sits.
4. The `refs_norm` token list, already shared (`cluster.py:64,141`), with the `T01.02` pattern added once.
5. Hash and identity helpers.

###### Engines
- The spec loop stays on v1 `findings.py`, `ledger.py`, `review-ledger/1` and v1 clustering.
- reflect stays on the v2 kernel.
- No change to `cli/reflect` (contract 1.8.0, INV-A).

###### Withdrawn from both proposals
- A: locator-agnostic `annotate` now, `citations` in ledger rows, the clustering marker, the typed re-review line kind, and `cluster_v2` for new ledgers.
- B: the 2.3 `LedgerError` guard, the projection view (until a consumer exists), and "closed at the PR adapter" (left to C-10).

###### Deferred, with a trigger
The convergence to one engine (A's profile parser, a span taken from either locator, rows keyed by citation) happens at the first of these:
- **(T-a)** A module needs re-review rounds over citation-located findings from several reviewers. B 5.4 item 1, kept.
- **(T-b)** The pre-registered measurement shows citations resolve at least as often as anchors locate on the document target. B 5.4 item 3, kept.
- **(T-c, replaces B item 2)** A verified defect fix needs a non-helper edit to both `findings._check_finding` and `findings_v2.check_finding`, or to both clusterers, beyond the shared constants and repair step. This can be checked mechanically on the fix's diff; it needs no quarterly count.

When convergence happens, it must first give `same_defect_v2` an anchor-span branch, or derive a `spec`-role citation from the located anchor span. N1's test then changes as a planned pin.

###### Stuck-row defect (E11, FX-2)
- C-01 adds a locator policy as data to the v1 engine: `on_missing` and `on_ambiguous`.
- `spec-loop` default: keep the row (as today, `test_review_ledger.py:408-417`), and surface `anchor_status` and `anchor_ambiguous`. Today they are thrown away (N4). They should appear in the merged report and the reviser brief, so the row is visibly marked unlocated and the next round is asked to locate it or say it is gone.
- How an unlocated row may clear goes to C-02, because the only release that needs no re-find depends on C-02's clearing rule (N3).

###### Clearing that ignores block validity (N2)
- This is not a C-01 defect. It goes to C-02 and C-03, together with `test_review_ledger.py:376-385`, which pins it.
- C-01 adds one constraint: the shared repair step must run before the parser decides validity, so that a re-find is not dropped for format reasons alone.

###### `cluster_v2` cannot cluster anchors (N1)
- Resolved for now by keeping the spec loop on v1 clustering.
- Recorded as the first step of any convergence (see Deferred).

###### Unknown keys
- Open in both parsers, as today (N5). No whitelist.
- `calibrated_confidence` stays accepted by v1 and rejected by v2 (`test_review_findings_v2.py:95-100`).
- Storing pass-through keys in the ledger member record (`ledger.py:172-180`) is deferred until a consumer reads provenance from the ledger.

###### Prior lines
- Unchanged: v1 accepts them (`findings.py:175-187`), v2 rejects them (`findings_v2.py:279-283`), and both are pinned (`test_review_findings_v2.py:106-113`).
- What they should do goes to C-02.
- No change to the brief, so the plugin mirror (INV-N) is untouched.

###### Tests
| Test | Fate | Content |
|---|---|---|
| T1 (A) | Survives | Every `tests/review/` and loop pin under `tests/skills/` passes unmodified after the constants module and repair step land. Add `test_review_cluster.py:279-293` to the named pins. |
| T2 (A) + 5.1 (B) | Merged | Differential replay: committed v1 ledger fixtures and a golden set of about 20 lines, run with and without the repair step. Parser output on lines that are already valid must be byte-equal, and the ledger file must be equal. 5.1's projection-totality check is dropped along with the projection view. |
| T3 (A) + 5.3 (B) | Merged | B's pre-registered rule, plus A's per-finding record (anchor found exactly once, path in the snapshot the core built, range inside the file, quote inside the range). Run only after the E1 snapshot plumbing is fixed and after A-002 (how line numbers reach reviewers) is stated. |
| T4 (A) + 5.2 (B) | Rewritten as one | Pin today's rejection of a citation-only line in a `findings-v1` block. One reviewer: `LedgerError` "no reviewer produced a valid findings block" and the ledger unchanged. Several reviewers: a warning, `block_ok` false, the line lost, the other reviewers merged. |
| T5 (A) | Rewritten | A missing anchor gives a row with `span None` whose `anchor_status` is surfaced in the merged report and reviser brief. A fix map entry naming it records `named_not_touched`. The clearing assertion is left to C-02. |
| 5.4 (B) | Survives as the trigger | Items 1 and 3, with item 2 replaced by T-c. |

##### Updated per-point table
| Point | Superior | Confidence | Reason |
|---|---|---|---|
| S-001 | A | 65% | A's answer to each routed row is easier to check than answers spread across sections. |
| S-002 | B | 75% | B's trigger, sharpened with T-c, is a falsifiable rule for when to converge; A's open points are not. |
| S-003 | NEITHER | 55% | Grouping the evidence differently changes no conclusion. |
| S-004 | A | 55% | A rates each invariant's level; the coverage is otherwise similar. |
| S-005 | HYBRID | 75% | T1, the merged T2/5.1, the merged T3/5.3, the rewritten T4/5.2 and the rewritten T5 (see the table above). |
| C-001 | B | 70% | CHANGED. Thin contract and per-module engines now; the pipelines are separate and the v2 kernel cannot host the anchor loop (N1). |
| C-002 | B | 65% | CHANGED. No reachable crash, so defer the locator-agnostic `annotate` and pin today's parser rejection; B's guard is withdrawn too. |
| C-003 | B | 65% | `prior` is inert (`ledger.py:259-272`), so no new line kind. |
| C-004 | B | 85% | `cluster_v2` never joins anchor-only findings (N1, `test_review_cluster.py:279-293`). |
| C-005 | HYBRID | 55% | Open in the core (N5); any adapter-side strictness belongs to C-10. |
| C-006 | HYBRID | 55% | CHANGED. The ledger drops pass-through keys (`ledger.py:172-180`), but no consumer reads them from the ledger yet, so defer. |
| C-007 | B | 70% | The shared constants module and repair step deduplicate real copied literals (N6) without merging parsers. |
| C-008 | HYBRID | 65% | CHANGED. A's verified defect, fixed as a locator policy inside the v1 engine (B's point); its clearing rule goes to C-02 (N3). |
| C-009 | HYBRID | 60% | PR review needs no ledger, and both designs need vocabularies as data (`findings_v2.py:109-110`). |
| C-010 | HYBRID | 60% | Citations are untested, not disproved; measure under the merged T3/5.3. |
| X-001 | B | 70% | Converge on a trigger; no current consumer, and converging needs new clustering code. |
| X-002 | B | 65% | The duplicated items are helpers and literals that the shared contract removes; git history shows no cost paid twice. |
| X-003 | B | 75% | The rewrite would break the pinned anchor-only clustering test and the loop's agreement between reviewers. |
| X-004 | HYBRID | 55% | Same as C-005. |
| X-005 | NEITHER | 85% | Neither fix closes a real path. The real issues are the stuck row (N3) and dropped re-finds that cannot hold a row open (N2). |
| A-001 | NEITHER | 90% | Contradicted by `findings.py:104` and `ledger.py:135-136`. |
| A-002 | NEITHER | 60% | CHANGED. Neither variant states how line numbers reach reviewers; it must be stated before the merged T3/5.3 runs. |
| A-003 | B | 75% | The kernel is one commit old, runs in shadow mode, enforces v1 categories and cannot cluster anchors; it is fit to share helpers with, not to host the loop. |

Not checked: B's claim that INV-K Check 11 would catch a constant-name clash (not run); the E1 and E2 run counts; and how line numbers reach reviewers in the loop brief (A-002).

### Variant B Rebuttal

#### Round 2: Advocate B (rebuttal)

Model: opus. Persona: architect + qa. Focus: correctness, risk, test-coverage. Code checked read-only at HEAD 50d4d2b9d. No file under the forbidden run-1 paths was read. Inputs read: round1-advocate-A.md, round2-advocate-A.md, my round1-advocate-B.md.

##### Response to criticisms

A's criticisms of B (Round 1 "Weaknesses identified in Variant B" and Round 2 "Updated assessment of Variant B"), answered one by one.

1. **"B's 2.3 guard can never run" (A R1 weakness 1).** CONCEDED, as in my Round 1 concession 1. `findings.py:104` with `:80-81` rejects a line without an anchor, and `ledger.py:135-136` annotates only parsed findings. The guard is withdrawn.
2. **"B's 5.2 is specified wrongly" (A R1 weakness 2).** CONCEDED. With other valid lines, the citation-only line is dropped with a warning (`ledger.py:130-134`). As the only line, the existing refusal raises (`ledger.py:150-157`), and its message lists warnings, not the finding id. I accept A's merged rewrite of T4 and 5.2 (see the position below).
3. **"B guards a hole that does not exist and misses the one that does" (A R1 weakness 3).** PARTLY CONCEDED, PARTLY COUNTERED.
   - Conceded: B did not name the clearing-ignores-block-validity behaviour.
   - Countered: A's own Round 2 (N2) agrees it is the single-valid-block defect that both proposals already route to C-02 and C-03 (A R1 section 5 item 6; my E-10). It is pinned as intended by `test_review_ledger.py:376-385` [VERIFIED by me in code]. It is not a C-01 defect.
   - Countered: A R1 claimed "A's typed locator path at least moves the finding into the ledger". A withdrew that path in Round 2, so it no longer separates the variants.
4. **"B leaves the verified stuck row untouched" (A R1 weakness 4, A R2 "remaining gap").** CONCEDED that B proposed nothing. COUNTERED on severity: the stuck row fails closed, not open. A row with `span None` stays `open` and blocking (`test_review_ledger.py:408-417`). `_brief_ids` keeps every blocking `open` or `regressed` row (`ledger.py:99-104`), and `_decision` returns `ESCALATE` at the cap (`ledger.py:93-96`); the escalation report says "do not start another fix cycle" (`test_review_ledger.py:476-490`) [VERIFIED by me in code]. So the cost is one wasted fix cycle and a human escalation, never a wrong PASS. It is a liveness defect, not an INV-I (fail-closed) breach. That argues for a cheap, visible fix in C-01, not a new configurable policy.
5. **"The projection view has no consumer" (A R1 weakness 5, A R2).** CONCEDED. Withdrawn until a consumer exists.
6. **"Trigger thresholds are unmeasured" (A R1 weakness 6, A R2).** CONCEDED. I accept A's T-c as the replacement for my 5.4 item 2.
7. **"Closed at the PR adapter has no evidence" (A R2).** CONCEDED. Unknown keys stay open in the core; adapter strictness goes to C-10.

##### Updated assessment of Variant A

- A's Round 2 hybrid is B's core shape plus a small v1-local locator change. On the shape (thin contract now, per-module engines, convergence on a trigger) we now agree.
- A's Round 2 self-corrections are all correct and I re-verified the ones that matter: the crash is unreachable, `cluster_v2` cannot join anchor-only findings (`cluster.py:126-154,161-181`; `test_review_cluster.py:279-293`), `prior` lines are inert (`ledger.py:259-272`), and the new ledger state had no consumer.
- A's best remaining contribution is the stuck-row analysis (N3) and the observation that `anchor_status` and `anchor_ambiguous` are thrown away (N4). Both are verified (below).
- A's remaining overreach is small and specific: it still wants the locator policy expressed "as data" with two knobs, and it asks the next round to "say it is gone", which has no effect today. Details in the position section.

##### New evidence

Verification of the three claims the orchestrator asked about, then new facts.

###### (a) A's N2: a re-find dropped for format reasons cannot hold its row open. AGREE, with one bound.

- `merge_round` keeps the parsed findings of every reviewer, valid block or not (`ledger.py:135-138`); a line rejected by `_check_finding` never reaches `parsed["findings"]` (`findings.py:188-192`).
- `members_by_lid` is filled only from clustered findings (`ledger.py:239`).
- The clearing loop clears a row when `status == "resolved_check"` and the row id is not in `members_by_lid` (`ledger.py:254-258`); it never reads `block_ok`, which is read only at `ledger.py:129,147,150,295,423` and `telemetry.py:67` [VERIFIED by me, Grep].
- So a re-find dropped for an over-limit anchor or claim, or for having no anchor, cannot hold its row open, and that row clears in that round.
- The bound: only rows already in `resolved_check` clear this way, that is, rows a reviser named as applied and whose span a change touched (`ledger.py:330-336`). A dropped re-find of an `open` row leaves it `open`. The defect is real but narrower than "any row can clear".
- Ownership: C-02 and C-03 (clearing rule), with the C-01 constraint A states (the repair step runs before validity is decided). I agree with that routing.

###### (b) A's N4: `anchor_status` and `anchor_ambiguous` are read only by tests. AGREE.

- Grep over the repo excluding `.dev/tasks/`: written only at `findings.py:350-351`; read only at `tests/review/test_review_findings.py:219,223,230` (the test function at `:227`). Other hits are a vendored copy under `.dev/research/346-review-loop-experiments/p18/ab5/vendor/`, an older `ledger_lite.py` under `.dev/research/`, plans, and `.dev/brainstorms/` notes; none is product code [VERIFIED by me, Grep].
- The ledger row does not store them (`ledger.py:184-202`), and `render_merged_report` prints only claim and anchor for each blocking finding (`ledger.py:447-466`) [VERIFIED by me in code].

###### (c) A's claim that the stuck row has no v1-local safe release independent of C-02. AGREE for automatic release; QUALIFY because a manual release exists.

- Automatic release paths in v1 today:
  - Re-anchoring needs a re-find with a locatable anchor (`ledger.py:226-231`). After a successful fix nobody re-finds it.
  - `apply_revision` cannot move a `span None` row to `resolved_check`, because `hunks_touch(None, ...)` is False (`findings.py:446-447`, `ledger.py:331-339`).
  - A reviewer's `prior` line saying "resolved" is only logged (`ledger.py:259-272`); making it count is C-02.
  - Letting a `span None` row reach `resolved_check` on a fix map entry alone would clear it by silence, which is C-02's rule.
- So I agree: every automatic release depends on a C-02 decision.
- Qualification: a v1-local manual release already exists and is independent of C-02. `ledger defer` (`ledger_cmd.py:83-87` calling `ledger.defer`, `ledger.py:350-360`) parks the row and recomputes the last decision to PASS when no other blocking id remains [VERIFIED by me in code]. It is a human accepted-risk release, not a verified-fix release. Together with point 4 above (the row escalates, fail-closed), this means the stuck row already has a safe, if manual, exit today.

###### New facts

- **N-B1. The merged report is pinned in a way that constrains where anchor status may be shown.** `test_rendered_merged_report` asserts that the text between `## Reviser brief` and `Rules for` contains no non-blocking id, with the comment "the reviser brief id parser of the Stage 2 harness reads these ids" (`test_review_ledger.py:459-467`) [VERIFIED by me in code]. So anchor status must be printed in the per-row `### Lx` block of `## Blocking findings` (`ledger.py:439-466`), not in the reviser brief id line, or a harness parser and this pin can break.
- **N-B2. Surfacing needs no prompt-file change.** `render_merged_report` is code in `ledger.py:408`, and its docstring says it is "the merged report the reviser and the next reviewer read" (`ledger.py:411`) [VERIFIED by me in code]. Printing anchor status there reaches both the reviser and the next reviewer without editing `document_review_loop_prompts.md` or its plugin mirror (INV-N).
- **N-B3. There are two `parse_block` functions and many callers.** `findings.py:124` and `findings_v2.py:215` [VERIFIED by me, Grep]; A's Round 1 E10 counts 15 callers of the v1 one, mostly tests [from the proposal, not re-checked]. A repair step placed in callers (for example inside `merge_round`) would miss the other callers and the v2 path. It must be called from inside both `parse_block` functions, on each block line before the check.
- **N-B4. The stuck row escalates, fail-closed.** See response 4: `ledger.py:93-104`, `test_review_ledger.py:476-490` [VERIFIED by me in code].

##### Concrete position you stand behind

**C-01 decision:** a thin shared contract now, per-module engines, convergence to one engine only on a mechanical trigger. Concretely:

1. **Shared contract now.** The id grammar `_ID` (already shared); one limits constants module imported by both parsers (names checked against INV-K, by running `make lint-architecture`); one repair function called from inside both `parse_block` functions on each line before the check (policy: C-06); the shared `refs_norm` token list with `T<PP>.<TT>` added once; hash and identity helpers.
2. **Engines.** The spec loop stays on v1 `findings.py`, `ledger.py`, `review-ledger/1` and v1 clustering. Reflect stays on the v2 kernel. No `cli/reflect` change (INV-A).
3. **Stuck row (FX-2), fixed inside v1 with no new configuration.** In `render_merged_report`, print for each blocking row whether its anchor was found, missing or ambiguous, inside its `### Lx` block (N-B1). Optionally store the status on the row additively. No knobs.
4. **Unknown keys** stay open in both parsers. No ledger passthrough keys yet.
5. **Prior lines** unchanged.
6. **Convergence trigger:** A's T-a, T-b and T-c, with the precondition A records (give `same_defect_v2` an anchor-span branch, or derive a `spec`-role citation from the located span, before any loop moves).
7. **Routed out:** clearing that ignores block validity (N2) and how an unlocated row may clear go to C-02 and C-03.

Comparison with A's Round 2 hybrid, point by point.

| Item in A's hybrid | My position | Why |
|---|---|---|
| Thin contract now, per-module engines, convergence on a trigger | AGREE | Same decision. |
| Locator policy as data in v1 (`on_missing`, `on_ambiguous`) | DISAGREE | A's own `spec-loop` default is "keep the row, as today", so each knob has one used value. A configuration value that never changes is an abstraction with no consumer, the same rule A used to drop my projection view. The other values A named in Round 1 (block, warn, fall back to a citation) either drop a blocking finding (block), add nothing over surfacing (warn), or need citations in v1 (convergence work). Hard-code "keep and surface" now; make it data when the engines converge. |
| Surface `anchor_status` and `anchor_ambiguous` in the merged report and reviser brief | AGREE, WITH A PLACEMENT CONDITION | Verified cheap and useful (N4, N-B2). It must go in the per-row `### Lx` block, not in the reviser brief id line that a harness parses and `test_review_ledger.py:459-467` pins (N-B1). It must be generated by `render_merged_report`, not added to the prompt file, so INV-N is untouched. |
| "The next round is asked to locate it or say it is gone" | DISAGREE ON THE SECOND HALF | "Say it is gone" can only be a `prior` line, which is inert (`ledger.py:259-272`). Asking reviewers for output that changes nothing is the same cost A conceded for the typed re-review line. Ask only that the row be re-located (that does re-anchor, `ledger.py:226-231`); route "say it is gone" to C-02. |
| How an unlocated row may clear goes to C-02 | AGREE | Verified in (c). Note for C-02: the row already fails closed (escalates) and `ledger defer` is a manual exit, so this is a liveness item, not an INV-I item. |
| T-c replaces my 5.4 item 2 | AGREE | It can be checked on the diff of a fix; my "two in one quarter" had no basis. |
| Projection view withdrawn | AGREE | Conceded in Round 1 and above. |
| Shared repair step placement ("before the parser decides validity") | AGREE, WITH A REFINEMENT | The step must be called inside both `parse_block` functions (`findings.py:124`, `findings_v2.py:215`), not in their callers (N-B3). It can rescue over-limit lines only; it must not invent an anchor for a citation-only line, so it narrows but does not close N2. |
| Ledger passthrough keys deferred | AGREE | No consumer reads provenance from the ledger. |
| Unknown keys open; adapter strictness to C-10 | AGREE | N5 verified by A; my "closed at the adapter" is withdrawn. |
| Prior lines unchanged, semantics to C-02 | AGREE | Verified inert. |
| T1 survives with `test_review_cluster.py:279-293` added | AGREE | Also add `test_rendered_merged_report` (`test_review_ledger.py:442-473`) to the named pins, because the surfacing change touches that function. |
| T2 + 5.1 merged, projection check dropped | AGREE | Byte-equal parser output on already-valid lines is the right gate for the repair step. |
| T3 + 5.3 merged, run after the snapshot fix and after A-002 is stated | AGREE | Keep my pre-registered decision rule. |
| T4 + 5.2 rewritten as one (pin today's rejection, one and several reviewers) | AGREE | Matches the verified behaviour (`ledger.py:130-157`). Add one assertion: in the several-reviewer case, the same reviewer's other valid lines are still merged (`ledger.py:135-138`). |
| T5 rewritten (span None row, status surfaced, `named_not_touched`, clearing left to C-02) | AGREE, WITH ONE ADDITION | Add an assertion that at the cap such a row gives `ESCALATE`, not PASS. That pins the fail-closed property the C-02 change must keep. |
| Convergence precondition (anchor-span branch or derived `spec` citation) | AGREE | Follows from N1. |

##### Updated per-point table

| Point | Superior | Confidence | Reason |
|---|---|---|---|
| S-001 | A | 65% | CHANGED (70% to 65%). A's per-row table is easier to check; it matters less now that both sides agree on most rows. |
| S-002 | B | 75% | CHANGED (70% to 75%). The trigger, sharpened by A's T-c, is now accepted by both sides. |
| S-003 | NEITHER | 55% | Grouping the evidence differently changes no conclusion. |
| S-004 | A | 55% | CHANGED (60% to 55%). A rates each invariant's level; coverage is otherwise similar. |
| S-005 | HYBRID | 80% | CHANGED (75% to 80%). The merged test set in the position table, with the ESCALATE assertion added to T5 and the merged-report pin added to T1. |
| C-001 | B | 80% | CHANGED (75% to 80%). A's Round 2 adopts the thin contract now; the kernel cannot host the anchor loop. |
| C-002 | B | 70% | CHANGED (65% to 70%). Both sides now defer the locator-agnostic `annotate` and pin today's parser rejection; my guard is withdrawn too. |
| C-003 | B | 70% | CHANGED (65% to 70%). `prior` is inert and A withdrew the typed line kind. |
| C-004 | B | 90% | CHANGED (85% to 90%). `cluster_v2` cannot join anchor-only findings, now conceded by A. |
| C-005 | HYBRID | 60% | Open unknown keys in the core; adapter strictness to C-10. |
| C-006 | HYBRID | 55% | The ledger drops passthrough keys, but no consumer reads them; both sides defer. |
| C-007 | B | 70% | CHANGED (65% to 70%). The constants module and one repair step inside both parsers remove the copied literals without merging parsers. |
| C-008 | HYBRID | 70% | CHANGED (A 70% to HYBRID 70%). A's verified stuck row, fixed inside v1 by surfacing anchor status (B's engine-local route), without configuration knobs; clearing to C-02. |
| C-009 | HYBRID | 60% | PR review needs no ledger; both designs need vocabularies as data (`findings_v2.py:109-110`). |
| C-010 | HYBRID | 60% | CHANGED (B to HYBRID). Both sides read citations as untested, not disproved; measure under the merged T3/5.3. |
| X-001 | B | 80% | CHANGED (75% to 80%). A now agrees to converge on a trigger. |
| X-002 | B | 65% | Duplication sits in helpers and literals the contract removes; no cost paid twice yet. |
| X-003 | B | 80% | CHANGED (75% to 80%). The rewrite would break the anchor-only clustering pin and reviewer overlap; A concedes. |
| X-004 | HYBRID | 60% | Same as C-005. |
| X-005 | NEITHER | 85% | Neither original fix closes a reachable path; the real items are the stuck row (C-01, surfacing) and dropped re-finds that cannot hold a row open (C-02, C-03). |
| A-001 | NEITHER | 90% | Contradicted by `findings.py:104` and `ledger.py:135-136`. |
| A-002 | NEITHER | 65% | Neither variant states how line numbers reach reviewers; state it before the merged T3/5.3 runs. |
| A-003 | B | 75% | CHANGED (70% to 75%). The kernel is one commit old, shadow-only, enforces v1 categories and cannot cluster anchors; fit to share helpers with, not to host the loop. |

Not checked: the E1 and E2 run counts; how line numbers reach reviewers (A-002); whether `make lint-architecture` Check 11 would flag a constants-module name (not run); A's count of 15 `parse_block` callers.

## Round 2.5: Invariant Probe

Independent fault-finder output (25 findings; 9 ADDRESSED, 16 UNADDRESSED; 1 HIGH, 14 MEDIUM, 1 LOW unaddressed) is in `invariant-probe.md` in this folder. The blocking item is INV-003 (HIGH): the shared repair step inside both `parse_block` functions cannot rescue over-limit lines while "T1: every existing pin passes unmodified" holds, because `tests/review/test_review_findings.py:113` and `:117` pin `parse_block(...)["ok"] is False` for an anchor of 201 and a claim of 301 characters (orchestrator re-read confirmed).

## Round 3: Final Arguments

Not run: `--depth standard`. The protocol allows Round 3 only for `--depth deep`.

## Scoring Matrix

Level = debate taxonomy level (auto-tagged, L3 > L2 > L1). R1 and R2 columns give the pair of advocate verdicts (A-advocate / B-advocate). Confidence derivation: mean of the two Round 2 confidences, +10 where an advocate explicitly conceded the winning side, capped at 95, floor 50; where the winner is HYBRID or NEITHER no side won and the mean is shown. Unanimous points that fall below the 90-100 bin did so because both advocates stated less than 90 themselves; the protocol's calibration rule ("scale with strength of evidence") was applied instead of forcing the bin.

| Diff Point | Level | R1 (A/B) | R2 (A/B) | Winner | Confidence | Evidence Summary |
|------------|-------|----------|----------|--------|------------|-----------------|
| S-001 | L2 | A/A | A/A | Variant A | 75% | Per-row answer table is easier to check; B advocate conceded in Round 1. |
| S-002 | L2 | B/B | B/B | Variant B | 85% | Falsifiable trigger (sharpened by A's T-c) beats an unordered open-points list; A conceded. |
| S-003 | L1 | N/N | N/N | NEITHER | 55% | Evidence grouping changes no conclusion. |
| S-004 | L1 | A/A | A/A | Variant A | 65% | A rates each invariant's level; B advocate conceded in Round 1. |
| S-005 | L2 | H/H | H/H | HYBRID | 78% | Merged tests: T1 (plus cluster and merged-report pins), T2+5.1, T3+5.3, rewritten T4+5.2 and T5 (with ESCALATE assertion). |
| C-001 | L2 | H/B | B/B | Variant B | 85% | Pipelines verified separate; `cluster_v2` cannot join anchor-only findings (`cluster.py:128-181`, `test_review_cluster.py:279-293`); A advocate moved to B. |
| C-002 | L3 | A/B | B/B | Variant B | 77% | KeyError unreachable via `merge_round` (`findings.py:104`, `ledger.py:135-136`); defer locator-agnostic `annotate`; B's guard also withdrawn. |
| C-003 | L2 | B/B | B/B | Variant B | 78% | `prior` lines are inert (`ledger.py:259-272`); no typed re-review line kind now. |
| C-004 | L3 | B/B | B/B | Variant B | 95% | `cluster_v2` never clusters anchor-only findings; A's CO-3 plan withdrawn. |
| C-005 | L2 | H/H | H/H | HYBRID | 58% | Open keys in the core; adapter strictness routed to C-10. |
| C-006 | L2 | A/H | H/H | HYBRID | 55% | Ledger drops passthrough keys (`ledger.py:172-180`) but no consumer reads them; deferred. |
| C-007 | L2 | B/B | B/B | Variant B | 80% | Shared constants module plus one repair step removes copied literals without merging parsers; placement and rescue semantics flagged by INV-003/004. |
| C-008 | L3 | A/A | H/H | HYBRID | 68% | Stuck row (`span None`, `ledger.py:331-339`) fixed inside v1 by surfacing anchor status; clearing routed to C-02; knobs disputed (B: hard-code). |
| C-009 | L2 | H/H | H/H | HYBRID | 60% | PR review needs no ledger; both designs need vocabularies as data (`findings_v2.py:109-110`). |
| C-010 | L2 | H/B | H/H | HYBRID | 60% | Citation reliability untested, not disproved; measure under merged T3/5.3. |
| X-001 | L2 | B/B | B/B | Variant B | 85% | Converge on a trigger; no current consumer; convergence needs new clustering code. |
| X-002 | L2 | B/B | B/B | Variant B | 75% | Duplicated items are helpers and literals the shared contract removes; no duplicate cost paid yet. |
| X-003 | L2 | B/B | B/B | Variant B | 88% | Rewrite would break the pinned anchor-only clustering test and reviewer overlap in the shipped loop. |
| X-004 | L2 | H/H | H/H | HYBRID | 58% | Same as C-005. |
| X-005 | L3 | N/N | N/N | NEITHER | 85% | Neither original fix closes a reachable path; real items are the stuck row and dropped re-finds that cannot hold a row open (C-02/C-03). |
| A-001 | L3 | N/N | N/N | NEITHER | 90% | Contradicted by `findings.py:104` and `ledger.py:135-136`; both variants' crash premise withdrawn. |
| A-002 | L3 | B/N | N/N | NEITHER | 63% | Neither variant states how line numbers reach reviewers; must be stated before T3/5.3 runs. |
| A-003 | L2 | B/B | B/B | Variant B | 85% | v2 kernel one commit old, shadow-only, enforces v1 categories, cannot cluster anchors: fit to share helpers with, not to host the loop. |

Tally of the 23 points: Variant A 2 (S-001, S-004); Variant B 10 (S-002, C-001, C-002, C-003, C-004, C-007, X-001, X-002, X-003, A-003); HYBRID 7 (S-005, C-005, C-006, C-008, C-009, C-010, X-004); NEITHER 4 (S-003, X-005, A-001, A-002).

Taxonomy coverage: L1 2 points (S-003, S-004), L2 15 points, L3 6 points (C-002, C-004, C-008, X-005, A-001, A-002). All three levels covered; no forced round needed.

## Convergence Assessment
- Points resolved: 23 of 23 (both advocates gave the same winner category on every point after Round 2; after Round 1: 18 of 23, disagreements on C-001, C-002, C-006, C-010, A-002)
- Alignment: 100% (23 / 23; denominator = 5 S + 10 C + 5 X + 3 promoted A)
- Threshold: 80%
- Taxonomy gate: PASS (L1, L2, L3 all covered)
- Invariant probe gate: BLOCKED (1 HIGH UNADDRESSED: INV-003)
- Status: BLOCKED_BY_INVARIANTS (agreement 100% >= 80% and taxonomy covered, but a HIGH-severity UNADDRESSED invariant exists)
- Unresolved points: none by advocate agreement; INV-003 (HIGH, unaddressed) is open. No Round 3 at depth standard, so the block is documented and not cleared (protocol: max rounds reached, force-select by score, flag for user review).
- Sycophancy check by the orchestrator: the near-total convergence came from verified code facts (anchor required by `findings.py:104`; `cluster.annotate` citations-only; `prior` inert), which both advocates re-read independently, not from deference. Two disputes remained between the advocates after Round 2 and are carried in the hybrid: whether the locator policy is "data with `on_missing`/`on_ambiguous` knobs" (A) or hard-coded "keep and surface" (B), and whether the next round is asked only to re-locate a row (B) or also to "say it is gone" (A). The advocates did not reach a joint statement on these two; B's Round 2 table records DISAGREE on both.
