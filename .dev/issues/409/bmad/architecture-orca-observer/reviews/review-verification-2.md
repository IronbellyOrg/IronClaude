# Verification review 2: ARCHITECTURE-SPINE.md fix cycle 2

**Verdict:** FAIL

Reviewer: fresh-context adversarial verifier, final review (3 of 3). Inputs read: the spine, `reviews/review-verification.md`, `.memlog.md`, and from the spec package `adapter-contract.md`, `rendering-rules.md`, `acceptance-tests.md`, `unverified-register.md`, plus grep hits in `SPEC.md`, `owner-decisions-and-risks.md` and `release-gates.md`. Nothing was edited and nothing was run. Line numbers refer to ARCHITECTURE-SPINE.md as read for this review.

## Verdict

**FAIL.** All 4 previously open items are now RESOLVED. But the B9 fix introduced one new blocking defect (NEW-2): the Runs-read counter silently drops rows whose `runId` is unknown and renders a plain `k`, which can show `read 0 of unknown Runs since start` while rows are on screen. That breaks the binding rule "unknown never renders as zero" and the spine's own AD-8 aggregate rule.

| Count | Value |
|---|---|
| Resolved | 4 |
| Partial (counts as open) | 0 |
| Open | 0 |
| New blocking | 1 |

## Status of the 4 items

| Item | Status | Evidence (spine) |
|---|---|---|
| NEW-1 `one Run only` trigger | RESOLVED | AD-6 (l.106): "The collector does not decide `one Run only`: `view.py` adds it whenever the parsed `result.scope.source` is `bound`, whatever the observer's options (`adapter-contract.md:63`); `flag` and `all` show only `scope=<source>`, and an absent scope reads `scope unknown`." Owner: AD-8 (l.118) now lists "`one Run only` and `read k of N Runs since start` (AD-6)" and places it among the "Header literals". Test: AD-16 (l.166) "`test_view` builds a `CycleResult` with `scope.source=bound` and no observer `--run` and asserts the header shows `one Run only`". Matches `adapter-contract.md:63` and the risk row at `owner-decisions-and-risks.md:44`. |
| B9 Runs-read counter | RESOLVED (but see NEW-2) | AD-6 (l.106): "the collector keeps `runs_read`, the set of distinct `runId` source values in rows returned by successful cycles since this observer process started. It is never reset while the process runs; a restart starts it empty, which `since start` discloses. k is its size ... N is `UNKNOWN` in R1 and the token renders `read k of unknown Runs since start` (PROPOSED wording, AD-8)". Owner, k, N and restart rule are all defined; `runs_read` is carried by `CycleResult` (AD-20, l.190); placement stays CONDITIONAL (CD-10). "R1 does not rotate Runs" is supported by `adapter-contract.md:3` (one verb, optional `--run`) and `:56` (rotation set is "R2 onward"). |
| B7 fixture question data path | RESOLVED | AD-16 (l.166): "Fixture-only question rows (T7) travel one path: `fixtures/` to the fixture loader (which passes every fixture string through `sanitize.py`) to `FixtureSource` to `CycleResult.fixture_questions` to `View.questions` to the screen renderer (AD-20, AD-10), never through the live parser." AD-20 (l.190) defines the field ("a tuple of `FixtureQuestion` records ... PROPOSED fixture-only shape: asked time, requester, owner, affected dispatch IDs and text; not an Orca field"); AD-10 (l.130): "`View.questions` is built only from `CycleResult.fixture_questions` (AD-20), oldest first with requester, owner and affected IDs (T7); in live mode it is `None`". Covers every T7 element (oldest first, requester/owner, affected IDs) and `rendering-rules.md:37` (`NN MIN` derivable from asked time and the clock). |
| ADV-13 fixture extras wiring | RESOLVED | Same root cause as B7, closed by the same path: `FixtureSource` (AD-6, collector.py) loads the questions per variant and `CycleResult` carries them (AD-20); the live path sets `None` "because R1 reads no message source". No new import edge is needed (collector → parse → sanitize already exists in the AD-1 diagram). |

## New blocking findings

### NEW-2 The Runs-read count drops unknown `runId` rows and renders a clean number, so unknown can render as zero (binding-rule violation, introduced by the B9 fix)

- **Spine, AD-6 (l.106):** "k is its size, and a row whose `runId` is `UNKNOWN` adds nothing to k ... the token renders `read k of unknown Runs since start`".
- **Spine, AD-16 (l.166):** "`test_collector` asserts `runs_read` grows only on successful cycles, ignores `UNKNOWN` `runId` values and renders `read k of unknown Runs since start`". The test pins the defect.
- **Spine's own rule, AD-8 (l.118):** "aggregates with unknown members render `n+? (k unknown)`".
- **Spec, rendering-rules.md:50:** "An aggregate with unknown members is `n+? (k unknown)`. Unknown is never zero or false."

**Why this blocks.** A row with a missing `runId` belongs to some Run the observer cannot name; it may be a Run not yet counted. So k is only a lower bound whenever such rows exist, and the spine shows it as an exact count. In the worst case (for example the `missing-fields` variant, T13, where `runId` is absent on every row) the header reads `read 0 of unknown Runs since start` while rows are listed: unknown rendered as zero. This is the header token that the risk table (`owner-decisions-and-risks.md:44`) relies on to stop one Run passing as the fleet, so an understated k defeats its purpose.

**Fix needed.** Keep the set as defined, but also count rows seen with an `UNKNOWN` `runId`; when that count is above 0, render k in the AD-8 aggregate form, for example `read k+? of unknown Runs since start (j rows with unknown run)` (PROPOSED wording). Change the AD-16 test to assert the `+?` form when an `UNKNOWN` `runId` is present, and a plain `k` only when none is.

## Minor notes

None of these causes the FAIL.

1. **B-view suffix not carried.** `rendering-rules.md:17` gives the B-view header token as `read k of N Runs since start; oldest among Runs read`, shown "until every Run in the rotation set has been read once". CD-10's default places the token in the B view only, but the spine never mentions `; oldest among Runs read` or the removal condition. T45 pins only the short form, and in R1 N is unknown so the token never ends, so this is a literal-completeness gap, not wrong R0/R1 behaviour. Add the suffix to the AD-8 literal list.
2. **R2 meaning of k vs N.** From R2, N is "the size of the rotation set", which `adapter-contract.md:56` defines over message-read scopes, while k still counts Runs seen in `worker-list` rows. The two can disagree (k may exceed N, or reach N while some Run's messages were never read). Restate k for R2 when AD-18's stage B lands.
3. **Test placement.** The `read k of unknown Runs since start` rendering is asserted in `test_collector`, but rendering is `view.py`'s job (AD-8, AD-10). Move that assertion to `test_view`.
4. **No negative test for NEW-1.** Add a case asserting `scope.source=flag` and `all` do not show `one Run only`.
5. **`FixtureQuestion` home.** The type is not in the naming list, the State convention's frozen-dataclass list, or the module table; say which module defines it (likely `parse.py` beside the fixture loader).
6. **Binds lists.** T7 is now served by AD-10 and AD-20, but neither lists T7 in Binds (only AD-16, "all", covers it). CAP-1 and CAP-3 in the Capability Map do not cite AD-20.
7. **Fixture questions vs text record.** AD-10 says fixture question rows "are never exported in R1", which also keeps them out of `record_text`, while T48 and CAP-9 tie the record to the same view the screen shows. Only matters in fixture mode; state it explicitly.
8. **Gap notice in fixture mode.** AD-8 says the question area reads the UNVERIFIED notice "until QUESTION-OBSERVATION passes" without a mode qualifier, while AD-10 shows fixture questions in fixture mode, and `rendering-rules.md:31` wants the gap notice above the ledger in every view. Say whether fixture mode shows both.
9. **Empty fixture questions.** How an empty `fixture_questions` tuple renders (T33 `no observed items in this source window; not proof none exist`) is not tied to `View.questions`, and that literal is not in AD-8's list.
10. **Carry-over minors** from review 1 (notes 1, 3 to 12) were not re-checked in depth; none affects the 4 items.

## Self-Audit

There is one blocking item, so a Self-Audit is not required. It is kept for traceability.

**Binding rules**
- **R1 read-only toward Orca: holds.** The fixes add no argv; AD-4 and AD-17 are unchanged; fixture questions never touch the adapter.
- **No invented Orca field: holds.** `fixture_questions` and `FixtureQuestion` are labelled "PROPOSED fixture-only shape ... not an Orca field"; `runs_read` is observer-derived from the verified `runId` (`unverified-register.md:11`); N is `UNKNOWN` rather than an invented Run list; the rendered wording is PROPOSED.
- **Owner questions not resolved: holds.** CD-10 still holds the placement of the Runs-read token (OQ-13 contradiction, `SPEC.md:112`); T45 is written against the owner's answer. NEW-1 follows `adapter-contract.md:63` and resolves no OQ.
- **Unknown never renders as zero: VIOLATED** by NEW-2 (AD-6 Runs-read k).
- **Every AD has Binds, Prevents and Rule: holds** for AD-1 to AD-20.

**Contradiction hunt.** Searched the spine for every occurrence of `one Run only`, `runs_read`, `fixture_questions`, `FixtureQuestion` and `Runs since start` (lines 106, 118, 130, 166, 190, 304). No remaining text ties `one Run only` to the observer's `--run`. AD-7's namespace (`--run` binding or `unbound`) is unaffected by NEW-1. The fixture loader sits in `parse.py` (structural seed) and sanitizes through the existing `parse → sanitize` edge, consistent with AD-1, AD-7 and AD-9.

**Limits.** No code was run (uv, pip and pytest were forbidden). The IronClaude repo and other planning artifacts were not read. Brownfield claims were not re-verified; review 1 already confirmed them.
