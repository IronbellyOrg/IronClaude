# Round 1 statement: Advocate A (variant-1, proposal A)

Q9: should the sweep's machine-readable JSON ever be kept, and how. Mode A, depth quick, Round 1.
Evidence was re-read on 2026-11-14 from the files named in each citation.

## 1. Position summary

Do not store the sweep JSON now. Keep SW-11 deferred with an explicit trigger (a named reader needs stored sweep facts); when it fires, try caller-side capture of stdout first, and relax NFR-001 only if capture fails a named need. This is the spec's own recommended answer and default (`merged-requirements.md:200`, `:536`; ADJ `:779`), and it is the only option that changes nothing today while keeping every later path open.

## 2. Steelman of each opposing variant

**B (embed the JSON in the one report).** B finds the one design that keeps the facts and still adds exactly one file, so NFR-001's two pinned tests need not change. It puts retention in one place (the reports) instead of on every caller, removing A's risk that two callers store the JSON differently. It makes every past sweep machine-readable, which the Markdown report alone is not (C concedes "Markdown, which is not a stable machine format"). The candidate readers ADJ names (v2 and a Coder#477 status record, ADJ A-001 at `alignment-findings-adjudicated.md:361`) could then read history with no producer work. That is a real, cheap-looking win.

**C (never store, standing rule).** C notices that nobody reads stored sweep facts today: "Consumer today: the coordinator or a person; no observer consumer" (`merged-requirements.md:221`), and Q17 is "No, not now" (`:544`). A deferred item with no reader is open-ended program debt; closing it removes a decision and a W5 row for good. It also hard-codes the observer/sweep separation (ADJ A-001: "not for the observer"), so nobody builds against a stored sweep file, and it avoids a store with no named owner, retention or file mode, which v2's own criteria demand (`merged-requirements.md:401`).

## 3. Strengths claimed

1. **It is the spec's recommended answer and its default if unanswered.** SW-11 row: "Default: not now; Phase 2 caller-side stdout capture first; relax NFR-001 only if a stored file is needed" (`merged-requirements.md:200`); the Q9 row repeats it (`:536`); ADJ Part 7 recommends it (`alignment-findings-adjudicated.md:779`). Picking A costs the owner no new reasoning and no ledger rework.
2. **Zero change to merged, reviewed code and tests.** NFR-001's design line (`docs/designs/orchestrator-mode.md:128`) and both pinned tests stay; PR #539's A-004 rule ("no added sweep JSON key or sidecar relative to the reviewed head", `merged-requirements.md:194`, `:661`) is untouched now and after.
3. **The first real reader shapes the format.** ADJ A-001 action: "v2 names its field list first" (`alignment-findings-adjudicated.md:361`). V2-04 requires "named store, owner, reader set, retention and file mode" (`merged-requirements.md:401`). A defers storage until those facts exist instead of guessing them.
4. **It matches the interface contract as written.** "Optional caller capture is a Phase 2 choice (Q9), not a producer sidecar" (`merged-requirements.md:221`). Caller capture fits the existing output ("1 report and 1 JSON object on exit 0", `orchestrator-mode.md:347`) with no producer change.
5. **Keeps all doors open.** Unlike C, a later reader does not need a new owner question; unlike B, nothing is committed that must later be migrated or removed. The trigger list (v2, Coder#477 record, observer if Q17 flips) is concrete.

## 4. Weaknesses identified in the others

1. **B's placement conflicts with a pinned report invariant.** B appends the block "at the end of its dated Markdown report". The design's exit rule says a complete report "ends in `Report complete`" (`orchestrator-mode.md` section 3.4, within lines 146-153); `render`'s docstring says "ending `Report complete`" (`report.py:608`); and a test near `test_cli_contract.py:1474` asserts `report.read_text("utf-8").endswith("Report complete\n")`. The marker is how a whole report is told apart after an interruption. B must place the block before that line; this is fixable, but B's claim that the pinned tests "should pass unchanged" is not established for this one.
2. **B builds a store with no reader.** The consumer today is "the coordinator or a person; no observer consumer" (`merged-requirements.md:221`); B admits "no named reader today". That is the case V2-04's "named store, owner, reader set, retention and file mode" guards against (`:401`).
3. **B's retention is weaker than it sounds.** Reports live in `.dev/sweeps/`, gitignored (`.gitignore:256`; design `:63`, GQ-106), and report retention is out of scope: "the person deletes old reports by hand" (design `:35`, SP-22). "Retention follows the reports" therefore means no retention policy.
4. **B puts uncut worker text into a people-facing file.** The JSON is "sanitized (FR-016) but never cut" (design `:563`); the Markdown report cuts table cells to `CELL_MAX` (`report.py`, `cell`, just above `render`). Whether a value that breaks a Markdown code fence is handled is UNVERIFIED. B also needs the JSON built before the commit point and without `report_path`, so the two copies differ by design and need a drift test.
5. **C turns "not now" into "never" on no new evidence.** Every source says "not now" or "Phase 2" (`merged-requirements.md:200`, `:536`; `:544` "if yes later, Q9 becomes a real requirement"); none says never. ADJ A-001 still names v2 and a Coder#477 status record as candidate readers (78 percent). Closing SW-11 forces a fresh owner question exactly when one of them arrives.
6. **C's caller ban is unenforceable.** C concedes "never stored by callers" is "an instruction, not something the sweep can enforce"; a rule that cannot be checked adds text, not safety.

## 5. Concessions

1. A settles nothing: "The question returns later; the decision is deferred, not settled." C is cleaner as program hygiene.
2. Caller-side capture spreads storage rules (location, retention, file mode) across callers; two callers could diverge. B handles this better.
3. Until a trigger fires, past machine facts exist only as Markdown, which is not a stable machine format.
4. A's stated fallback ("relax NFR-001") costs a design line, two tests and the XC-05 registry in one PR (`merged-requirements.md:200`). B shows a stored copy without a second file is possible, and A as written does not name that as the preferred stored form.
5. Like the others, A does not address a reader on another host (see A-002).

## 6. Shared assumptions

- **A-001 (reports last long enough to be a record): QUALIFY.** A does not depend on it for storage: A's stored path is caller capture, whose retention the caller sets. A only points readers to the Markdown report as a stopgap, and that stopgap is not durable: reports are gitignored and deleted by hand (`.gitignore:256`; design `:35`). The assumption is load-bearing for B and weakens B most.
- **A-002 (readers share the sweep's host and checkout): QUALIFY.** True for today's consumer (coordinator or person, `merged-requirements.md:221`) and for v2's first release ("reads only what the same OS user on the same host can read", `:401`). Likely false for a Coder#477 status record (where it runs is UNVERIFIED). Caller capture extends most easily to a transport, since the caller already holds the JSON; none of the three provides one, and A's trigger should make "which host" a question for the first reader.

## 7. Per-point positions

| Point | Better variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (A) | 50% | Same section set; no difference of merit |
| C-001 | A | 75% | Keep nothing until a reader exists; spec default |
| C-002 | B | 60% | B keeps facts and NFR-001; A may later relax it |
| C-003 | A | 75% | Deferred with a trigger beats premature build (B) or closure (C) |
| C-004 | B | 65% | One owner (the sweep) beats per-caller rules, if storing at all |
| C-005 | A | 70% | Open until named; B pre-builds, C forces a new question |
| X-001 | A | 75% | V2-04 and ADJ A-001 want the reader to define fields first |
| X-002 | B | 70% | Embedding does avoid relaxing NFR-001, provided the `Report complete` ending is kept |
| A-001 | A | 65% | A depends least on report durability |
| A-002 | A | 55% | Caller capture extends most easily to a transport; none solves it |

## 8. Overall verdict

Pick A, amended with B's idea as the preferred stored form: keep SW-11 deferred with a named-reader trigger; when triggered, try caller capture first, and if a stored copy is needed, prefer embedding it inside the one report (before the `Report complete` line) over a sidecar, so NFR-001 survives. Confidence 75 percent. Reason: nothing reads stored sweep facts today, A is the spec's default with zero change, and B's one-file design is the right fallback once a reader names its fields.
