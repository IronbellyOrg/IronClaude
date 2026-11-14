## Position summary
Variant A is still the right long-term target: one parser whose v1 and v2 grammars are data profiles, and a ledger that does not care which kind of locator a finding uses. But two of A's load-bearing claims are wrong in the code. The `merge_round` crash cannot happen, and `cluster_v2` cannot cluster anchor-only findings. So the correct ruling on core shape is a HYBRID: build B's thin contract now, and take A's profile-and-locator design as the convergence target.

## Steelman of Variant B
The two pipelines really are separate today. Nothing in `ledger.py`, `merge_cmd.py` or `ledger_cmd.py` imports from v2 (B E-1). Both kernels are two to three days old, with one commit each. I ran git log: `findings.py` and `ledger.py` were last touched in 9163bd1c7 on 2026-11-11, and `findings_v2.py` and `cluster.py` only in d2d8a2d16 on 2026-11-12 [VERIFIED by me in code]. So "you will fix every defect twice" is a projection, not a cost anyone has paid yet.

The defects that both engines share are already fixable once without merging the engines:
- `refs_norm` is one function, used by both `findings.annotate` (`findings.py:357`) and `cluster.annotate` (`cluster.py:141`).
- The v1 length limits are literals at `findings.py:104,108,114,118`. A shared constants module plus one repair step before parsing covers the drop of over-limit lines (FX-1) for both parsers [VERIFIED by me in code].

No current consumer needs a re-review ledger over citation-located findings. B also names a trigger that would prove it wrong (5.4) and a measurement rule fixed before the first run (5.3). Rewriting the shipped, test-pinned spec loop before then means paying a certain risk for a benefit nobody has asked for.

## Strengths claimed
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

## Weaknesses identified in Variant B
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

## Concessions
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

## Shared assumption responses
- **A-001 (the crash happens through `merge_round`): REJECT.** `parse_block` drops a line with no anchor before `annotate` runs (`findings.py:104`, `ledger.py:128-138`). The real defect is a silent drop plus clearing that ignores block validity (`ledger.py:254-258`).
- **A-002 (reviewers give usable line numbers for a document): QUALIFY.** Neither proposal shows how line numbers reach the reviewer in the ledger path, and no measurement exists. It must be measured by A's T3 or B's 5.3, with a document arm, before any module is made to require citations.
- **A-003 (the v2 kernel is stable enough to build on): QUALIFY.** `parse_block` in v2 is pinned against v1 compatibility (`test_review_findings_v2.py:70-81`). But `cluster_v2` only works with citations (concession 2), so it is not ready to be the spec loop's clustering. Sharing constants with it (B) is safe; making the loop a profile of it (A) needs new code first.
- **A-004 (neither location type is proven reliable enough to drop the other): ACCEPT.** Both proposals' evidence agrees, and the diff analysis reconciles the two sets of numbers as different scopes.
- **A-005 (verdict and clearing fixes land in the one multi-reviewer ledger): ACCEPT.** One extra item for C-02 and C-03: clearing must check block validity, as the `merge_round` docstring already claims (`ledger.py:112` against `:254-258`).

## Per-point assessment table
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
