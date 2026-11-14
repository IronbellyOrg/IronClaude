# Adversarial Debate Transcript: Q9 owner-answer proposals

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 100% (10 of 10 points agreed by at least 2 of 3 advocates)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (spawned in parallel as separate agents; each wrote its own file)
- Variant mapping: variant-1 = proposal A, variant-2 = proposal B, variant-3 = proposal C
- Orchestrator spot-check (2026-11-14): `tests/sweep/test_cli_contract.py:1476` asserts the report `endswith("Report complete\n")`, so B's "append at the end" would fail that test; `report.py:569-599` `sanitize` neutralises backslash, `|`, `<`, `>`, `[`, `]` and not backticks, so a fenced block needs its own guard. Both confirmed.

## Round 1: Advocate Statements

### Advocate for proposal A (source file: round1-advocate-A.md)

## Round 1 statement: Advocate A (variant-1, proposal A)

Q9: should the sweep's machine-readable JSON ever be kept, and how. Mode A, depth quick, Round 1.
Evidence was re-read on 2026-11-14 from the files named in each citation.

### 1. Position summary

Do not store the sweep JSON now. Keep SW-11 deferred with an explicit trigger (a named reader needs stored sweep facts); when it fires, try caller-side capture of stdout first, and relax NFR-001 only if capture fails a named need. This is the spec's own recommended answer and default (`merged-requirements.md:200`, `:536`; ADJ `:779`), and it is the only option that changes nothing today while keeping every later path open.

### 2. Steelman of each opposing variant

**B (embed the JSON in the one report).** B finds the one design that keeps the facts and still adds exactly one file, so NFR-001's two pinned tests need not change. It puts retention in one place (the reports) instead of on every caller, removing A's risk that two callers store the JSON differently. It makes every past sweep machine-readable, which the Markdown report alone is not (C concedes "Markdown, which is not a stable machine format"). The candidate readers ADJ names (v2 and a Coder#477 status record, ADJ A-001 at `alignment-findings-adjudicated.md:361`) could then read history with no producer work. That is a real, cheap-looking win.

**C (never store, standing rule).** C notices that nobody reads stored sweep facts today: "Consumer today: the coordinator or a person; no observer consumer" (`merged-requirements.md:221`), and Q17 is "No, not now" (`:544`). A deferred item with no reader is open-ended program debt; closing it removes a decision and a W5 row for good. It also hard-codes the observer/sweep separation (ADJ A-001: "not for the observer"), so nobody builds against a stored sweep file, and it avoids a store with no named owner, retention or file mode, which v2's own criteria demand (`merged-requirements.md:401`).

### 3. Strengths claimed

1. **It is the spec's recommended answer and its default if unanswered.** SW-11 row: "Default: not now; Phase 2 caller-side stdout capture first; relax NFR-001 only if a stored file is needed" (`merged-requirements.md:200`); the Q9 row repeats it (`:536`); ADJ Part 7 recommends it (`alignment-findings-adjudicated.md:779`). Picking A costs the owner no new reasoning and no ledger rework.
2. **Zero change to merged, reviewed code and tests.** NFR-001's design line (`docs/designs/orchestrator-mode.md:128`) and both pinned tests stay; PR #539's A-004 rule ("no added sweep JSON key or sidecar relative to the reviewed head", `merged-requirements.md:194`, `:661`) is untouched now and after.
3. **The first real reader shapes the format.** ADJ A-001 action: "v2 names its field list first" (`alignment-findings-adjudicated.md:361`). V2-04 requires "named store, owner, reader set, retention and file mode" (`merged-requirements.md:401`). A defers storage until those facts exist instead of guessing them.
4. **It matches the interface contract as written.** "Optional caller capture is a Phase 2 choice (Q9), not a producer sidecar" (`merged-requirements.md:221`). Caller capture fits the existing output ("1 report and 1 JSON object on exit 0", `orchestrator-mode.md:347`) with no producer change.
5. **Keeps all doors open.** Unlike C, a later reader does not need a new owner question; unlike B, nothing is committed that must later be migrated or removed. The trigger list (v2, Coder#477 record, observer if Q17 flips) is concrete.

### 4. Weaknesses identified in the others

1. **B's placement conflicts with a pinned report invariant.** B appends the block "at the end of its dated Markdown report". The design's exit rule says a complete report "ends in `Report complete`" (`orchestrator-mode.md` section 3.4, within lines 146-153); `render`'s docstring says "ending `Report complete`" (`report.py:608`); and a test near `test_cli_contract.py:1474` asserts `report.read_text("utf-8").endswith("Report complete\n")`. The marker is how a whole report is told apart after an interruption. B must place the block before that line; this is fixable, but B's claim that the pinned tests "should pass unchanged" is not established for this one.
2. **B builds a store with no reader.** The consumer today is "the coordinator or a person; no observer consumer" (`merged-requirements.md:221`); B admits "no named reader today". That is the case V2-04's "named store, owner, reader set, retention and file mode" guards against (`:401`).
3. **B's retention is weaker than it sounds.** Reports live in `.dev/sweeps/`, gitignored (`.gitignore:256`; design `:63`, GQ-106), and report retention is out of scope: "the person deletes old reports by hand" (design `:35`, SP-22). "Retention follows the reports" therefore means no retention policy.
4. **B puts uncut worker text into a people-facing file.** The JSON is "sanitized (FR-016) but never cut" (design `:563`); the Markdown report cuts table cells to `CELL_MAX` (`report.py`, `cell`, just above `render`). Whether a value that breaks a Markdown code fence is handled is UNVERIFIED. B also needs the JSON built before the commit point and without `report_path`, so the two copies differ by design and need a drift test.
5. **C turns "not now" into "never" on no new evidence.** Every source says "not now" or "Phase 2" (`merged-requirements.md:200`, `:536`; `:544` "if yes later, Q9 becomes a real requirement"); none says never. ADJ A-001 still names v2 and a Coder#477 status record as candidate readers (78 percent). Closing SW-11 forces a fresh owner question exactly when one of them arrives.
6. **C's caller ban is unenforceable.** C concedes "never stored by callers" is "an instruction, not something the sweep can enforce"; a rule that cannot be checked adds text, not safety.

### 5. Concessions

1. A settles nothing: "The question returns later; the decision is deferred, not settled." C is cleaner as program hygiene.
2. Caller-side capture spreads storage rules (location, retention, file mode) across callers; two callers could diverge. B handles this better.
3. Until a trigger fires, past machine facts exist only as Markdown, which is not a stable machine format.
4. A's stated fallback ("relax NFR-001") costs a design line, two tests and the XC-05 registry in one PR (`merged-requirements.md:200`). B shows a stored copy without a second file is possible, and A as written does not name that as the preferred stored form.
5. Like the others, A does not address a reader on another host (see A-002).

### 6. Shared assumptions

- **A-001 (reports last long enough to be a record): QUALIFY.** A does not depend on it for storage: A's stored path is caller capture, whose retention the caller sets. A only points readers to the Markdown report as a stopgap, and that stopgap is not durable: reports are gitignored and deleted by hand (`.gitignore:256`; design `:35`). The assumption is load-bearing for B and weakens B most.
- **A-002 (readers share the sweep's host and checkout): QUALIFY.** True for today's consumer (coordinator or person, `merged-requirements.md:221`) and for v2's first release ("reads only what the same OS user on the same host can read", `:401`). Likely false for a Coder#477 status record (where it runs is UNVERIFIED). Caller capture extends most easily to a transport, since the caller already holds the JSON; none of the three provides one, and A's trigger should make "which host" a question for the first reader.

### 7. Per-point positions

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

### 8. Overall verdict

Pick A, amended with B's idea as the preferred stored form: keep SW-11 deferred with a named-reader trigger; when triggered, try caller capture first, and if a stored copy is needed, prefer embedding it inside the one report (before the `Report complete` line) over a sidecar, so NFR-001 survives. Confidence 75 percent. Reason: nothing reads stored sweep facts today, A is the spec's default with zero change, and B's one-file design is the right fallback once a reader names its fields.

### Advocate for proposal B (source file: round1-advocate-B.md)

## Round 1 statement: advocate for variant 2 (proposal B, embed the JSON in the one report)

- Debate: Q9 (should the sweep's JSON ever be kept, and how), sc:adversarial Mode A, depth quick, Round 1
- Advocate: B (variant-2-original.md)
- Date: 2026-11-14
- Evidence re-read this session: `report.py:530-695`, `commands.py:268-281`, `test_cli_contract.py:1460-1481`, `test_readonly.py:285-314`, design `:33-35`, `:62-63`, `:125-153`, `:325-347`, `:558-563`, `.gitignore:254-257`, merged-requirements `:196-225`, `:399-402`, `:534-545`, `:616-619`, ADJ `:129-134`, `:344-362`, `:777-779`.

### 1. Position summary

B's lasting idea is sound: if the sweep's machine facts are ever kept, putting them inside the one dated report keeps NFR-001 ("a sweep adds exactly one report file") true and avoids a sidecar file. But B as written has two verified defects: it puts the block after the `Report complete` marker, which a pinned test forbids, and its fence is not protected against backticks in worker-written text. It also builds a store before any reader exists. I argue that B should be kept as the preferred storage form that A's Phase 2 tries first, not adopted now.

### 2. Steelman of each opposing variant

**A (not now; caller capture first; relax NFR-001 only if needed).** A is the spec's own recommended answer and default (merged-requirements `:536`; ADJ `:779`). It changes nothing in a newly reviewed tool, and it keeps PR #539 inside A-004's "no JSON key and no sidecar" limit. It also leaves the field list and retention to the first real reader, as ADJ A-001 (`:361`) says: "v2 names its field list first". Caller capture is cheap and already fits the output. The stdout JSON is printed only after the commit point and carries `report_path` (design `:563`; `commands.py:275-278`), so a caller that saves stdout gets the facts plus a pointer to the matching report, with no producer change. A also has the only explicit trigger ("a named reader ... needs stored sweep facts"), so SW-11 cannot drift.

**C (never, as a standing rule).** C is the most decisive answer. Today's consumer is "the coordinator or a person; no observer consumer" (merged-requirements `:221`), and Q17 is recommended "No, not now" (`:544`). Every store needs a "named store, owner, reader set, retention and file mode" before it is built (V2-04, `:401`). C refuses to create anything that lacks those five, removes an open item from wave W5, and records in the contract note that the JSON has no stored form. That stops anyone from building against a stored sweep file and keeps the observer and the sweep separate (ADJ E-03 `:129`, X-017 `:360`).

### 3. Strengths claimed (B)

1. **Keeps NFR-001's file count without relaxing the rule.** The rule counts files: "a successful run never leaves two files (NFR-001)" (design `:128`); "1 report and 1 JSON object on exit 0" (design `:347`). An embedded block adds no file. The `test_cli_contract.py:1474` assertion `_reports(env.sweeps) == [f"{STEM}.md"]` still holds. This is the one variant that stores facts without the "relax NFR-001 ... two pinned tests change" path that SW-11 (`:200`) and K-NFR001 (`:618`) attach to a stored file.
2. **No sidecar, so no new crash states.** Design `:131-153` lists every on-disk state a crash can leave, and it depends on one report name per run, published through `os.link`. A sidecar would add a second publish step and a second set of crash states. An embedded block rides the existing atomic publish (temp file, then `os.link`).
3. **The machine facts and the human report cannot separate.** Caller capture (A) stores the JSON wherever each caller chooses, apart from the report it describes. Embedding ties the facts to the report by construction, which is what a later reader browsing "by report date" needs.
4. **The data is already computed before publish.** `render` runs before `_publish`, and `to_json` runs after it only to add `report_path` (`commands.py:273-277`). Every other key is a pure function of `SweepResult` and `SweepContext` (`report.py:613-695`). The embedded object needs only that function without `report_path`, so no new collection, Orca call or git call is added (NFR-014's allow-list is untouched).
5. **One storage policy instead of one per caller.** A's own cost line says "two callers could store it differently". In B the sweep owns the format, and the location is the existing `.dev/sweeps/` folder (design GQ-106 `:63`).

### 4. Weaknesses identified in the others

1. **A's fallback skips the option that keeps NFR-001.** A goes from "caller capture" straight to "a later PR relaxes NFR-001 and changes the two tests". It never considers embedding in the existing report, which stores the facts without touching the rule. If capture fails a reader that is not the caller, A takes the most expensive path first.
2. **A's caller capture does not help a reader that is not the caller.** A says capture serves the coordinator, which already holds the JSON in its own call. The candidate readers ADJ names are v2 and a Coder#477 status record (`:361`). Neither is the caller, so capture serves them only if every caller agrees on one location and one format, which A leaves to each caller.
3. **C contradicts the spec's conditional on Q17.** The spec says "if yes later, Q9 becomes a real requirement" (`:544`). C instead makes any future need "a new owner question, not a revival of SW-11", and it effectively forces Q17 to "no" (C's own cost line). It also closes off ADJ A-001's candidate carriers (v2, Coder#477) before either has written its field list.
4. **C's rule cannot be enforced.** "Never stored by ... callers" is an instruction only; C concedes the sweep cannot enforce it. A standing rule that callers can break without anyone noticing is weaker than an open, triggered deferral.
5. **A and C both point readers back to the Markdown report.** A says "anyone who needs past machine facts must parse the Markdown report"; C says "Readers of past sweeps must parse Markdown, which is not a stable machine format". The report's text is sanitized and cut for tables (`cell` cuts to `CELL_MAX`, `report.py:602-605`), while the JSON is "sanitized but never cut" (design `:563`). The fallback both variants name is therefore lossy.

### 5. Concessions (B's real weaknesses, verified this session)

1. **"Append at the end" breaks a pinned test and the completeness marker.** `test_cli_contract.py:1476` asserts `report.read_text("utf-8").endswith("Report complete\n")`. The design treats `Report complete` as the sign of a complete report (`:139`, `:153`), and `render`'s docstring says the report ends in it (`report.py:609`). B's claim that NFR-001's tests "should pass unchanged" is therefore false as written: the `:1474` test function fails at `:1476` if the block follows the footer. A corrected B must insert the block before `_footer` (the last entry of `SECTIONS`, `report.py:545-558`), or inside it before the marker.
2. **The fence is not safe against worker-written text.** `sanitize` neutralises backslashes, `|`, `<`, `>`, `[` and `]` (`report.py:569-599`), not backticks. A worker-written string containing three backticks could close the fenced block early. B's "UNVERIFIED that the existing sanitizer covers fenced blocks" is now settled: it does not. A fix is needed, such as a fence longer than any backtick run in the payload, plus a test.
3. **No named reader exists.** "Consumer today: the coordinator or a person; no observer consumer" (merged-requirements `:221`). B builds a store for readers that have not written their field list, against ADJ A-001's "v2 names its field list first" (`:361`).
4. **"Retention follows the reports" means no retention policy.** Reports live in the gitignored `.dev/sweeps/` folder (`.gitignore:255-256`: "operator-local, never posted ... Never tracked"), and "the person deletes old reports by hand" (design `:35`, SP-22). An embedded store is therefore not durable and has no owner, which fails V2-04's "named store, owner, reader set, retention and file mode" (`:401`) if v2 relied on it.
5. **It changes a newly merged and reviewed tool.** `to_json` takes `report_path` as a required argument (`report.py:613-615`), so embedding needs a signature or call-order change, plus a test pinning that the embedded and stdout copies match apart from `report_path`.
6. **Reports get harder for people to read.** One JSON object per row and per worktree, never cut (design `:563`), can be long, at the bottom of a document that people read.

### 6. Shared assumptions

| ID | Response | Reason |
|---|---|---|
| A-001 (reports last long enough to be a record) | REJECT | Verified false as a guarantee. `.dev/sweeps/` is gitignored and "never tracked" (`.gitignore:255-256`), and retention is out of scope, with reports deleted by hand (design `:35`, SP-22). This hurts B most, because B's store is the report. It also hurts A and C, whose "parse the Markdown report" fallback has no durability promise either. Only A's caller capture can choose a durable location. |
| A-002 (readers share the sweep's host and checkout) | QUALIFY | True for today's only consumer, the coordinator in the same checkout (merged-requirements `:221`), and V2-04 requires that v2's first release "reads only what the same OS user on the same host can read" (`:401`). A same-host v2 is therefore within the assumption. A Coder#477 status record on another host is not, and none of the three variants provides a transport. |

### 7. Per-point positions

| Point | Better variant | Confidence | Note |
|---|---|---|---|
| S-001 (section set) | A, B and C tie (A listed) | 50% | Identical structure; no difference on merit |
| C-001 (is the JSON kept?) | A | 70% | No named reader today (`:221`); B's form is better kept as the stored option to try later |
| C-002 (NFR-001) | B | 60% | Embedding keeps the file count, but only if the block goes before `Report complete` (`test_cli_contract.py:1476`) |
| C-003 (SW-11) | A | 70% | Deferred with an explicit trigger beats both building now (B) and closing for good (C) |
| C-004 (who owns storage rules) | B | 55% | One producer-owned format beats one per caller, but "retention follows the reports" is no retention (SP-22) |
| C-005 (later readers) | A | 65% | Leaves the field list to the first reader (ADJ A-001 `:361`); B pre-empts it and C closes it |
| X-001 (keep before a named reader?) | A | 75% | V2-04 requires store, owner, reader set, retention and file mode first (`:401`) |
| X-002 (does keeping need relaxing NFR-001?) | B | 65% | Correct: an embedded block does not need it; A assumes any stored form does |
| A-001 (report durability) | A | 60% | Only caller capture can pick a durable location; B depends most on a non-durable folder |
| A-002 (same host) | A | 55% | None of the three solves cross-host transport; A's caller capture is the most open to adding one later |

### 8. Overall verdict

The owner should pick **A, amended with B's form as the first storage option**. Keep SW-11 deferred with A's trigger. When a named reader needs stored facts, Phase 2 should try, in order: caller capture; then embedding the JSON before the `Report complete` footer, with a backtick-safe fence and a test that the embedded and stdout copies match; and only then a sidecar that relaxes NFR-001.

Confidence: 70%.

Reason: no reader exists to set the field list or retention, and the reports holding B's block are not durable, but B's embedding is the only known path that stores the facts without breaking NFR-001, so it belongs in A's fallback order ahead of relaxing the rule.

### Advocate for proposal C (source file: round1-advocate-C.md)

## Round 1 advocate statement: Proposal C (variant-3, "neither, as a standing rule")

Debate: Q9 (keep the sweep JSON?), sc:adversarial Mode A, depth quick, Round 1.
Evidence read 2026-11-14. ROOT = `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. MR = `merged-requirements.md`; ADJ = `alignment-findings-adjudicated.md`; DES = `docs/designs/orchestrator-mode.md`.

### 1. Position summary

C says the sweep's JSON is a one-time reply to its caller and is never stored, and closes SW-11 as "will not do". Its real merit is that no reader exists today, so nobody pays for a store or keeps a deferred item open. Its weak spot is that the word "never" goes further than the evidence: the adjudicated review still names two possible future readers.

### 2. Steelman of each opposing variant

**A (not now; caller capture first; a stored file only if needed).** A is the spec's own recommended answer, word for word (MR:536, ADJ:779). It changes no code and no test. It keeps PR #539 exactly as reviewed (A-004: "Add no JSON keys and no files inside #539", ADJ:210). It also respects the adjudicated finding that the sweep JSON is "a candidate carrier only for v2 and for a Coder#477 status record", with the instruction "v2 names its field list first" (ADJ:361, 78 percent). A leaves the choice to the first real reader, and that reader can define fields, retention and file mode, which V2-04 requires anyway: "named store, owner, reader set, retention and file mode" (MR:401). Its order (stdout capture first, a stored file only if that fails) is the cheapest path that stays reversible. The stdout object already carries `report_path` (`report.py:694`), so a caller can pair what it saved with the report.

**B (embed the JSON as a fenced block in the dated report).** B is the only variant that persists machine facts without touching NFR-001. The run still adds one file (DES:331: "1 report file + 1 JSON object on stdout"), so the two pinned tests (`test_readonly.py:300`, `test_cli_contract.py:1474`) should still pass. Storage rules come from the sweep itself rather than from each caller, so two callers cannot store it differently. Reports already go in one known, gitignored folder (`.gitignore:256` `.dev/sweeps/`; DES:63 GQ-106). The JSON is built from `SweepResult` only and is "sanitized ... but never cut" (DES:563; `report.py:613-694`). So the content already exists, and serialising it a second time is a small change.

### 3. Strengths claimed (C)

1. **No reader exists today, and the spec says so.** "Consumer today: the coordinator or a person; no observer consumer" (MR:221). The coordinator gets the JSON on stdout when it runs the sweep and needs nothing stored. C fits the present facts exactly.
2. **It removes a store that would have no owner.** V2-04 requires "named store, owner, reader set, retention and file mode" (MR:401). Report retention is out of scope: "the person deletes old reports by hand" (DES:35, SP-22). A store with no reader, no owner and retention by hand deletion is the kind of thing C prevents.
3. **It keeps the observer and the sweep separate.** ADJ E-03 says the two programs "never mention each other" (ADJ:129). X-017 keeps two readers, and persistence "survives only for an optional later panel" (ADJ:360). Q17 is recommended "No, not now" (MR:544). C turns that separation into a rule, so nobody builds an observer reader against a sweep file.
4. **NFR-001 becomes settled rather than provisional.** K-NFR001 lists SW-11 as the only thing that may change it, "by owner decision Q9" (MR:618). Under C nothing can relax it, so the design line (DES:128) and the two tests are never touched.
5. **Less open work.** SW-11 is listed as DEFERRED with a "later" location (MR:200). ADJ A-005 says "Nobody defends 'Phase 2 and #534 will absorb the deferred items': only a reading list exists" (ADJ:348). Closing one deferred item is honest about that.
6. **It respects the rule against refetching.** "Consumers never run another sweep merely to fetch status" (MR:221), and WC-16 limits sweeps to once per 5 minutes. With no stored copy, a later reader cannot quietly depend on sweep output. It has to name its own status source, and for status that is the observer snapshot (ADJ:346: "the first status record is the observer snapshot").

### 4. Weaknesses identified in the others

1. **B adds a second copy of the facts and has no reader for it.** B admits this: "with no named reader today" and "It answers a question the spec deliberately left for the first real reader to shape" (variant-2). ADJ A-001 tells the reader to name its field list first (ADJ:361). B fixes the field list to the stdout object, so a later v2 inherits that shape or has to change it, which is churn on `ROW_KEYS`-pinned data (MR:617; ADJ:210).
2. **B's store is not durable.** Reports sit in the gitignored `.dev/sweeps/` folder of one checkout (`.gitignore:256`), and they are deleted by hand (DES:35). The "every past sweep becomes machine-readable" benefit lasts only as long as a person keeps the files. A Coder#477 status record on another host could not read them (see A-002 below).
3. **B makes the report harder for people to read, and sanitising has to be checked again.** The report is the human artefact. The JSON is sanitized for stdout (DES:563), but B itself says it is UNVERIFIED whether that sanitizing is safe inside a Markdown fenced block (variant-2). `render` (`report.py:608`) currently emits no JSON block, so B is new format work on a tool that has only just merged or is about to.
4. **A pushes storage rules onto each caller.** A concedes that "two callers could store it differently" (variant-1). Caller capture also gives any later reader no single contract to rely on.
5. **A keeps the question open with no clock.** SW-11 is "DEFERRED ... later" (MR:200), wave W5 is "not scheduled by the spec" (question.md, MR:865), and A-005 shows that deferred items have no owner (ADJ:348). A's trigger is sound, but nothing guarantees that anyone watches for it.

### 5. Concessions (C's real weaknesses)

1. **"Never" contradicts the adjudicated finding.** ADJ A-001 (78 percent) keeps the sweep JSON as a candidate carrier for v2 and for a Coder#477 status record (ADJ:361). V2-04 depends on SW-11 "if v2 reads stored sweep facts" (MR:401). C closes a door that the evidence deliberately left open, and the cost of closing it is only a ledger line.
2. **C has nothing A lacks today.** Under both A and C the code, NFR-001 and the tests do not change now. C only adds that this will never change later, and the only evidence for that is the absence of a reader today, which is weak evidence about the future.
3. **"Never stored by callers" cannot be enforced.** The sweep cannot stop a caller from redirecting stdout (variant-3 admits this). The rule is a sentence, not a guard.
4. **Reopening costs more than deferring.** If v2 needs sweep facts, C requires "a new owner question, not a revival of SW-11" (variant-3), and the closure has to be explained. A's trigger does the same job with less friction.
5. **The fallback is weak.** C sends past readers to Markdown, which "is not a stable machine format" (variant-3). A shares this fallback, so it does not separate them.
6. **C pre-answers Q17.** Q17 effectively becomes "no" for good (variant-3). The spec keeps Q17 open and says "if yes later, Q9 becomes a real requirement" (MR:544).

### 6. Shared assumptions

- **A-001 (reports last long enough to be a record): QUALIFY.** The assumption is false as a durability claim. Reports are gitignored (`.gitignore:256`) and deleted by hand (DES:35). It does not hold for B, whose whole benefit rests on it. For A and C it is acceptable only as a best-effort route for a person to look back, not as a machine record. C's position barely depends on it, because C promises no stored machine facts. The diff-analysis wording "all three" is fair only in the sense that A and C also name the Markdown report as the fallback.
- **A-002 (readers share the sweep's host and checkout): ACCEPT for today, QUALIFY for the future.** It is true now: the consumer is the coordinator or a person (MR:221), and V2-04's first release "reads only what the same OS user on the same host can read" (MR:401). It breaks for a Coder#477 status record on another host, which none of the three variants serves. This favours A, because A lets that reader define its own transport and does not lock in a same-host store (B) or rule one out (C).

### 7. Per-point positions

| Point | Better variant | Confidence | Reason |
|---|---|---|---|
| S-001 (section set) | Tie (A) | 50% | Same five sections. No difference on the merits. |
| C-001 (is the JSON kept?) | A | 75% | "Not now" fits "no reader today" (MR:221) and keeps the named candidate readers (ADJ:361). C's "never" and B's "yes now" both go further than the evidence. |
| C-002 (NFR-001) | A | 65% | All three keep it now. A keeps the owner's lever that K-NFR001 reserves for Q9 (MR:618). C's permanence gives up that lever for no gain today. |
| C-003 (SW-11) | A | 70% | Deferred with a named trigger matches MR:200 and V2-04's conditional dependency (MR:401). C's closure is tidier but hides a live dependency. |
| C-004 (who owns storage rules) | B | 55% | B is the only one with a single owner (the sweep). A's per-caller rules can diverge, and C has no rules because there is nothing to rule. B's owner still has no retention policy (DES:35). |
| C-005 (later readers) | A | 75% | A leaves the first reader to shape the fields, as ADJ A-001 requires (ADJ:361). B pre-shapes them, and C forces a new question. |
| X-001 (keep anything before a named reader?) | A, with C agreeing | 80% | A and C both say no. A's "until a named reader" is the evidenced form. C's "and not later" is not evidenced. |
| X-002 (does keeping need NFR-001 relaxed?) | B | 70% | B is correct that embedding keeps one file (DES:331). A is correct that a separate file would need relaxing it. B made the sharper point. |
| A-001 (reports last as a record) | C | 60% | C relies on it least. B relies on it most, and it is false for durability (`.gitignore:256`; DES:35). |
| A-002 (same host and checkout) | A | 65% | A alone leaves a remote reader (Coder#477) free to choose its own transport. |

### 8. Overall verdict

The owner should pick **A** (the spec default), with one element borrowed from C: record now in the XC-05 contract note that sweep report JSON v1 is a stdout-only reply and has no stored form until a named reader triggers SW-11. Confidence is 75 percent. A matches every present fact that C relies on (no reader today, NFR-001 unchanged, no work in #539), and it does not shut out v2 and the Coder#477 status record, which the adjudicated review keeps as candidate readers (ADJ:361, MR:401). My own variant's "never" does exactly that, and nothing in the evidence supports it.

## Scoring Matrix

| Diff Point | Level | Advocate A | Advocate B | Advocate C | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | tie (no winner) | 50% | Same five sections. |
| C-001 | L2 | A 75 | A 70 | A 75 | A | 95% | Unanimous: no named reader today (merged-requirements.md:221); ADJ A-001 keeps v2 and a Coder#477 status record as candidate readers (ADJ:361). |
| C-002 | L3 | B 60 | B 60 | A 65 | B | 60% | Embedding keeps NFR-001 if placed before the `Report complete` footer; C's advocate prefers keeping the owner's lever. |
| C-003 | L2 | A 75 | A 70 | A 70 | A | 95% | Unanimous: deferred with a named trigger beats building now or closing for good. |
| C-004 | L2 | B 65 | B 55 | B 55 | B | 85% | Unanimous: one producer-owned format beats per-caller rules, if anything is stored. |
| C-005 | L2 | A 70 | A 65 | A 75 | A | 95% | Unanimous: the first reader defines the fields (ADJ:361; V2-04 at merged-requirements.md:401). |
| X-001 | L2 | A 75 | A 75 | A 80 | A | 95% | Unanimous: nothing stored before a named reader. |
| X-002 | L3 | B 70 | B 65 | B 70 | B | 90% | Unanimous: an embedded block does not need NFR-001 relaxed; a separate file would. |
| A-001 | L3 | A 65 | A 60 | C 60 | A | 65% | Reports are gitignored and deleted by hand (`.gitignore:256`; design :35), so they are not a durable store; B depends on them most. A QUALIFY, B REJECT, C QUALIFY. |
| A-002 | L2 | A 55 | A 55 | A 65 | A | 80% | True for today's reader and v2's first release (same OS user, same host, :401); false for a remote Coder#477 record; caller capture is the most open to a later transport. |

Shared-assumption responses: A-001 QUALIFY (A), REJECT (B), QUALIFY (C); A-002 QUALIFY (A), QUALIFY (B), ACCEPT now / QUALIFY later (C). No omissions.

## Overall verdicts (section 8 of each statement)

| Advocate | Picks | Confidence |
|---|---|---|
| A (for defer, caller capture first) | A, with B's embedding as the preferred stored form (before the footer) | 75% |
| B (for embed now) | A, with B's form as the first storage option: capture, then embed before the footer with a backtick-safe fence and a copy-match test, then a sidecar only last | 70% |
| C (for never) | A, plus C's sentence in the contract note that the JSON is stdout-only until a named reader triggers SW-11 | 75% |

All three chose A: 3 of 3. Mean confidence 73%.

## Convergence Assessment
- Points resolved: 10 of 10 (majority); unanimous: C-001, C-003, C-004, C-005, X-001, X-002
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 (S-001), L2 (C-001, C-003, C-004, C-005, X-001, A-002), L3 (C-002, X-002, A-001): all covered
- Invariant probe gate: not applied (Round 2.5 skipped at quick depth)
- Status: CONVERGED
- Unresolved points: none. Points won by B (C-002, C-004, X-002) are merged into A as the fallback form.
