# Owner decision pack: Orca read-only observer (IronClaude issue 409)

Prepared in step 5 (final review), 2026-11-08. Nothing here is decided: every item is open until the owner answers in writing. Recommendations are the reviewer's, not the owner's.

## How to read this

Each decision has a number (D1, D2, ...) in the order of the earliest work it blocks. Each entry gives the plain question, why it matters, the options, the reviewer's recommendation with reasons, what it blocks, and whether the first implementation tasks can start without it.

The stages named below come from the spec's release table (`_bmad-output/specs/spec-orca-observer/release-gates.md:7-18`):

- **R0, fixture replay:** the observer runs only on recorded or synthetic sample files. No live Orca call, no command registered in the shipped tool.
- **Direction selection (DIRECTION-SELECTED):** not a release. A dated record the owner writes (never an agent) that names the chosen screen design and several of the answers below (`release-gates.md:20-27`). Until it exists, only R0 work runs.
- **R1, live worker list:** the first live release. It reads Orca's verified worker list and shows one row per worker, plus a notice that the question source is UNVERIFIED (not yet checked).
- **R2, question ledger:** shows questions waiting for a human. Opens only after the question-observation gate (recorded proof that questions can be read safely and completely enough).
- **R3, links view:** links each question to the sessions it affects. Opens only after the question-link gate.
- **Later stages:** remote hosts, a read-only Go screen inside TUIBBS (the private bulletin-board terminal app), and write-back (answering from the screen), which is a future stage outside the read-only boundary.

The three screen designs are A (Signal Bridge, the worker list), B (Attention Ledger, the question list) and C (Decision Desk, one question with the sessions it affects) (`rendering-rules.md:3`).

**The first implementation tasks need no answer from this pack.** The key-reader spike, the snapshot schema test, the adapter allow-list with a fake command runner, and the text sanitizer are all R0 work. Each runs on the documented default and changes, at most, one table or constant when the owner answers.

Codes in square brackets at the end of an entry are for the record only: OQ-n is the spec's open question n, in order (`SPEC.md:98-114`); UX-OQ-n is the UX design's question n (`EXPERIENCE.md:525-534`); CD-n is the architecture's matching conditional decision, with its default (`ARCHITECTURE-SPINE.md:293-310`).

## Summary table

23 open decisions after removing duplicates. "First tasks" means the key-reader spike, the snapshot schema test, the adapter allow-list and the sanitizer.

| # | Decision (plain) | Recommendation | Earliest work blocked | First tasks wait? |
|---|---|---|---|---|
| D1 | Pass criteria for the key-reader spike | Accept the six proposed criteria | Spike verdict | No |
| D2 | Meaning of "production integration" | Reading 1 (stricter) | Command registration, all of R1 | No |
| D3 | Command name | `superclaude observe` | Command registration (R1) | No |
| D4 | Which headers show "read k of N Runs since start" | Every header | Header test, R0 review renders | No |
| D5 | Screen height and width budgets | Accept proposed numbers, confirm at direction review | R1 layout | No |
| D6 | Cut-off text marker | `>` | Nothing beyond one glyph | No |
| D7 | Colour palette | Confirm the prototype palette, meaning always in words | Nothing functional | No |
| D8 | Shared worktree on each row | No for R1: inspector and text export (T20 checks the inspector) | R1 row layout | No |
| D9 | Snapshot row order | Timestamp order | Snapshot ordering clause | No |
| D10 | Change-detection fields; two detail fields in snapshot | Keep default, fields off the snapshot | R1 change flags | No |
| D11 | Dated direction record, R1 look | Record the staged choice after viewing R0 renders | All of R1 | No |
| D12 | Export and snapshot file location | Per-user default folder, `--snapshot PATH` override, owner-only, atomic replace (suggestion) | R1 snapshot and export | No |
| D13 | Several observers at once | Disclose only | R1 release notes | No |
| D14 | Deadline for the question-observation gate | Set when R1 ships | R2 timing review | No |
| D15 | Permission to capture message samples | Yes, owner sets redaction | R2 | No |
| D16 | Message content on screen vs in files | Short excerpt on screen, metadata only in files (suggestion) | R2 | No |
| D17 | What is a human question | An explicit Orca message type | R2 | No |
| D18 | Key between question list and worker list | Pick at R2 | R2 | No |
| D19 | Default view after links work (B or C) | Decide at the link gate | R3 | No |
| D20 | Licence opinion before a Go screen in TUIBBS | Get it before any TUIBBS reader is built | Go screen | No |
| D21 | TUIBBS as staff platform | Decide after R1 is in use | Nothing in R0-R3 | No |
| D22 | Approve write-back boundary change | Not yet; revisit after R3 | Write-back stage | No |
| D23 | How Orca authenticates a reply sender | Ask Orca's owner when D22 is approved | Write-back stage | No |

The answers to D2, D3, D11 and D14 all go into one document: the owner's dated direction record (`release-gates.md:22`).

## Tier 1: touches the first offline work (R0, fixture replay)

None of these stops R0 work: each has a written default. They are listed first because the R0 renders, which the owner reviews before choosing a direction, are built on these defaults.

### D1. What counts as a pass for the key-reader spike?
- **Question:** The first task is a short experiment: can Rich (the current terminal library) plus a plain keyboard reader run the interactive screen, or must the project switch to Textual (a larger terminal framework)? What results count as a pass?
- **Why it matters:** The spike's verdict picks the toolkit for the whole screen. The spec gives no criteria (`EXPERIENCE.md:532`); the architecture proposes six (`ARCHITECTURE-SPINE.md:154`).
- **Options:** (a) accept the six proposed criteria: a lone Esc key is told apart from arrow keys; no key is lost during a redraw; the selection stays on the same worker; the terminal is restored on `q`, Ctrl-C, a termination signal and a crash; a resize redraws within one refresh; no visible flicker. (b) add or remove criteria.
- **Recommendation:** (a). They cover the failures that make a terminal screen unusable (lost keys, a broken terminal after exit), and each can be checked by an automated test in a pseudo-terminal.
- **Blocks:** the spike's final verdict, not the spike itself.
- **First tasks start without it?** Yes. The spike runs against the proposed criteria; if the owner changes them, the test is re-judged. [UX-OQ-6, CD-7]

### D2. Which meaning of "production integration" applies?
- **Question:** The issue forbids production integration before a direction is chosen, but does not define it. Reading 1: registering `superclaude observe` in the shipped command-line tool, or running any live Orca command outside the test double, counts. Reading 2: only wiring or enabling the observer in the shipped product counts, and separately authorized read-only captures count as research (`release-gates.md:29-34`).
- **Why it matters:** Until the owner confirms one, the stricter reading 1 applies: offline work only.
- **Options:** (a) reading 1; (b) reading 2.
- **Recommendation:** (a) reading 1. It costs the first tasks nothing (all offline), it is already the documented default, and it keeps every live call behind the owner's written direction record. Research captures can still be allowed one by one under D15.
- **Blocks:** registering the command and every live read, so all of R1.
- **First tasks start without it?** Yes. [OQ-2, CD-1]

### D3. What is the command called?
- **Question:** Is the command `superclaude observe`?
- **Why it matters:** The name goes into the shipped command list and every document and help text.
- **Options:** (a) `superclaude observe`; (b) another name.
- **Recommendation:** (a). It matches the binding stack decision ("a `superclaude observe` style subcommand") and every artifact already uses it.
- **Blocks:** registering the command (R1). The owner records it in the direction record (`release-gates.md:22`).
- **First tasks start without it?** Yes. [OQ-3, CD-1]

### D4. Which screens show the "read k of N Runs since start" line?
- **Question:** This header line says how many Orca runs the observer has actually read, so one run is never mistaken for the whole fleet. The source rules disagree: one puts it in the question view header only, others in every header (`SPEC.md:112`, `rendering-rules.md`).
- **Why it matters:** It is a recorded contradiction in the source. A screen without it can let a partial view pass as complete.
- **Options:** (a) question view (B) header only, the current architecture default (`ARCHITECTURE-SPINE.md:304`); (b) every header.
- **Recommendation:** (b) every header. Three of the four source passages (the adapter's scope-honesty rule, acceptance test T45 and the risks table) put it everywhere, and its purpose, stopping one run passing as the fleet, applies to the worker view that ships first.
- **Blocks:** the header test (T45) and the R0 renders shown at direction review.
- **First tasks start without it?** Yes. The change is one shared header builder. [OQ-13, CD-10]

### D5. What are the screen height and width budgets?
- **Question:** The sources name a width matrix for A, coordinates for B and a 44-row height contract for C, but never define them (`SPEC.md:113`). The UX design proposes a 44-row budget, a 12-row minimum and a shrink order (`EXPERIENCE.md:528`); the existing design exports are 48 rows (160 columns) and 42 rows (116 and 80 columns).
- **Why it matters:** It decides what disappears first on a small terminal. Fixed rules already hold: the counts line is never dropped; coverage, scope and the partial-data marker are minimum content (`ARCHITECTURE-SPINE.md:298`).
- **Options:** (a) accept the proposed budget, minimum and shrink order for R0 and confirm them at direction review; (b) set other numbers now.
- **Recommendation:** (a). The numbers live in one table, so a later change is cheap, and the owner can judge them on the R0 renders rather than in the abstract.
- **Blocks:** the final layout of R1. Not R0.
- **First tasks start without it?** Yes. [OQ-14, UX-OQ-2, CD-4]

### D6. Which character marks cut-off text?
- **Question:** When a value is too long for its column, is it cut with `>` (spec rule and test T24) or with `…` or `~` (the prototype)?
- **Why it matters:** It must be readable in plain ASCII terminals and recognizable as a cut, not data.
- **Options:** (a) `>`; (b) `…`; (c) `~`.
- **Recommendation:** (a) `>`. It is the spec rule, test T24 already uses it, and it works on ASCII-only terminals.
- **Blocks:** nothing beyond one glyph table.
- **First tasks start without it?** Yes. [UX-OQ-5, CD-5]

### D7. Which colours does the screen use?
- **Question:** The spec defines no colours; the UX design adopts the prototype's palette (`EXPERIENCE.md:533`). Is that palette confirmed?
- **Why it matters:** Colour must never carry meaning on its own (the screen must read the same with colour turned off), but it affects readability.
- **Options:** (a) confirm the prototype palette; (b) choose another; (c) keep the architecture's default: no colour at all, same as the no-colour render (`ARCHITECTURE-SPINE.md:302`).
- **Recommendation:** (a), with the rule that every meaning is also in words. It is already designed and reviewed in the UX artifacts.
- **Blocks:** nothing functional.
- **First tasks start without it?** Yes. [UX-OQ-7, CD-8]

### D8. Does each worker row show the worktree it shares?
- **Question:** Test T20 (`acceptance-tests.md:29`) checks the shared worktree through the detail panel (the inspector): two sessions that share one worktree show as two rows, each inspector shows the same `resource.worktreeId`, and a session with none shows `unknown (absent in source)`. The spec's worker list has no worktree column. Should each row also name the worktree, and if so where and how does it shorten at each screen width?
- **Why it matters:** A new column changes every width budget. After the step-5 fixes the UX design and architecture both propose that the row does not name it and the JSON snapshot carries no worktree id; all three documents, the PRD included, keep the question open (`prd.md:148`, `EXPERIENCE.md:534`, `ARCHITECTURE-SPINE.md:310`). Review 3 found the architecture saying inspector only, against the UX's inspector and plain-text export (NEW-R3-1, `findings.md`). On the owner's order it was **fixed by edit, NOT re-reviewed**: CD-16 now says inspector and plain-text export, not the JSON snapshot (`verify/owner-fix-NEW-R3-1.json`).
- **Options:** (a) keep the default: inspector and plain-text export only; (b) the row also names it, in a place and short form the owner picks.
- **Recommendation:** (a) for R1. T20 already passes without a column, and the spec forbids counting sessions by worktree, which the inspector shows without crowding the list. Revisit (b) if staff miss shared worktrees in R1 use.
- **Blocks:** the R1 row layout only; T20 does not depend on it.
- **First tasks start without it?** Yes. [UX-OQ-8, CD-16]

### D9. In what order are rows written to the snapshot file?
- **Question:** Should snapshot readers rely on timestamp order, or on the source's "newest first" order (`SPEC.md:111`)?
- **Why it matters:** A later reader (for example the Go screen) may depend on the order.
- **Options:** (a) timestamp order, the current default; (b) source order, with sorting done only on screen.
- **Recommendation:** (a). It is stable and does not depend on an Orca ordering nobody has verified. The schema does not change either way (`ARCHITECTURE-SPINE.md:297`).
- **Blocks:** the ordering clause of the snapshot contract, not the schema test.
- **First tasks start without it?** Yes. [OQ-12, CD-3]

### D10. Which fields mark a worker as changed, and do two detail fields enter the snapshot?
- **Question:** Which stage field decides that a worker "changed since last look", and may `stage.detail` and `stage.activity` be written to the snapshot (`SPEC.md:114`)?
- **Why it matters:** One source lists the two fields for the snapshot; the merged requirements keep them on the detail panel only.
- **Options:** (a) keep the default: change detection uses worker stage, dispatch stage, next action and liveness; the two fields stay off the snapshot (`ARCHITECTURE-SPINE.md:296`); (b) add the two fields.
- **Recommendation:** (a). The snapshot is additive-only, so the fields can be added later without a version change; removing a field later would break readers.
- **Blocks:** the change flags in R1.
- **First tasks start without it?** Yes. The schema test is written against the default. [OQ-15, CD-2]

## Tier 2: blocks the first live release (R1, live worker list)

### D11. The direction record: which design ships, and what does R1 look like?
- **Question:** Does the owner's staged choice (worker list first, question list after the question-observation gate, links view after the question-link gate) count as the direction selection, and will the owner write the dated record? The record must name the date, the decider and where the owner's statement lives, and hold: the default view while no questions exist, the default after question observation, the post-link choice or an explicit deferral, the fallback date (D14), the stack confirmation, the command name (D3) and the production-integration reading (D2) (`release-gates.md:22`). Part of it: is the R1 screen layout in the spec (counts line, freshness line, worker list, question-source notice) the confirmed look, given that it matches neither the earlier cockpit plan nor the built Signal Bridge prototype (`EXPERIENCE.md:527`)?
- **Why it matters:** No live release can start without it, and an agent may never write it (`release-gates.md:22`). Its status: not shown to have passed; the owner is to say (`release-gates.md:10`).
- **Options:** (a) the owner reviews the R0 renders of A, B and C at 160, 116 and 80 columns (each beside its degraded version) and records the staged choice as the selection, with the spec's R1 layout; (b) the owner selects a different direction or layout; (c) the owner defers.
- **Recommendation:** (a). It matches the binding staged-release decision, and the spec's review recommendation is the same: A with the counts line for R1, B after question observation with A one key away, C behind the question-link gate (`owner-decisions-and-risks.md:17`). One reviewer dissented and prefers C after the link gate; that choice belongs to D19, not here.
- **Blocks:** R1 entirely (`ARCHITECTURE-SPINE.md:308`).
- **First tasks start without it?** Yes. The R0 renders it needs are themselves R0 work. [OQ-1, UX-OQ-1, CD-14]

### D12. Where are exports and the snapshot written, and what do the messages say?
- **Question:** What is the file location and naming of the text export (the `e` key and `--once`) and of the per-refresh JSON snapshot, and the wording of the success and failure messages (`EXPERIENCE.md:530`)?
- **Why it matters:** R1 must write the snapshot (binding owner decision 2). Since the step-5 fixes the architecture carries a PROPOSED default: `--once` prints to the terminal; a PROPOSED `--snapshot PATH` option sets the snapshot path, defaulting to the per-user state folder `~/.local/state/superclaude/observe/`; the file is owner-only (permissions 0600) and replaced atomically each live refresh; `e` writes a timestamped text export to the same folder (`ARCHITECTURE-SPINE.md:300`). The UX lists the destination as open (`EXPERIENCE.md:530`).
- **Options:** (a) keep the proposed default folder, with `--snapshot PATH` to override it; (b) require a path on the command line, no default; (c) another default location.
- **Recommendation:** (a): one known default path is what a later Go reader needs, the option covers other setups, owner-only permissions keep worker data private, and atomic replacement means a reader never sees a half-written file. The exact folder and file names are the owner's call.
- **Blocks:** the R1 snapshot and export.
- **First tasks start without it?** Yes. The schema test checks content, not location. [UX-OQ-4, CD-6]

### D13. May several observers run at the same time?
- **Question:** Each observer process has its own limits on Orca calls; nothing stops two people (or two windows) running it at once (`owner-decisions-and-risks.md:25`). Restrict it, or only disclose it?
- **Why it matters:** Several observers multiply read load on Orca.
- **Options:** (a) disclose only (document that limits are per process); (b) a lock so only one runs; (c) a shared cache.
- **Recommendation:** (a). The observer only reads, the calls are capped per process, and a lock or cache adds code with no measured need. Revisit if Orca load is ever measured as a problem.
- **Blocks:** R1 release notes; no code under the default.
- **First tasks start without it?** Yes. [OQ-8, CD-11]

## Tier 3: blocks the question ledger (R2) and the links view (R3)

### D14. By what date must the question-observation gate pass?
- **Question:** What is the fallback date by which questions must be proven readable? When it passes, the owner re-confirms the direction; expiry never grants a switch on its own (`release-gates.md:25`, `owner-decisions-and-risks.md:21`).
- **Why it matters:** Without a date, the question list (the issue's main complaint) can wait forever with nobody prompted to re-decide.
- **Options:** (a) set a date when R1 ships; (b) set a date now; (c) no date.
- **Recommendation:** (a), as a suggestion: the date is easier to set once R1 shows real usage. On expiry, the screen stays on the worker list with its "question source UNVERIFIED" notice, which the spec offers as the re-confirm option.
- **Blocks:** the timing review of R2. It goes into the direction record (D11).
- **First tasks start without it?** Yes. [OQ-4, CD-14]

### D15. May one redacted message sample be captured from live Orca?
- **Question:** The question-observation gate needs recorded, redacted samples from the candidate read `orca orchestration check --all --run <runId> --json`. May the team capture them, and under what redaction rules? Permission to read must cover the actual read scope and is separate from permission to display or export (`owner-decisions-and-risks.md:22`).
- **Why it matters:** Without samples the gate cannot pass, so the question list (R2) cannot ship. This covers message samples only: R0 runs on the synthetic `base` fixture and does not wait on it, and the redacted worker-list samples are recorded at the first permitted live read as part of the R1 gate (`ARCHITECTURE-SPINE.md:303`).
- **Options:** (a) yes, with redaction rules the owner sets; (b) no.
- **Recommendation:** (a). It is the only path to proving the question source, and owner-set redaction keeps message content out of the repository.
- **Blocks:** R2 (the question-observation gate).
- **First tasks start without it?** Yes. [OQ-5, CD-9]

### D16. What message content may be shown on screen, and what may be exported?
- **Question:** For questions, which parts of a message may appear on screen, and which may be written to the export and snapshot? The spec keeps these as two separate permissions and makes no further recommendation (`owner-decisions-and-risks.md:23`).
- **Why it matters:** Messages can contain secrets or private text; the export and snapshot are files that outlive the session.
- **Options:** (a) show a short sanitized excerpt on screen, export metadata only (sender, time, type, IDs), no message bodies; (b) show and export full bodies; (c) metadata only everywhere.
- **Recommendation:** (a), as the reviewer's suggestion, not a spec recommendation: the person at the screen needs enough text to know what is being asked, while files that persist should not carry bodies.
- **Blocks:** R2 display and export.
- **First tasks start without it?** Yes. The sanitizer is built for any displayed text regardless. [OQ-6, CD-9]

### D17. What makes a message a "human question"?
- **Question:** Which message types count as a question for a human, and which handle or run carries it (`owner-decisions-and-risks.md:24`)? This needs the owner or Orca's owner.
- **Why it matters:** It decides which rows appear in the question list. Guessing from the text would be wrong in both directions.
- **Options:** (a) an explicit message type set by Orca; (b) inference from the message text.
- **Recommendation:** (a). The binding rules forbid inventing an Orca field, and text inference cannot be tested reliably.
- **Blocks:** R2.
- **First tasks start without it?** Yes. [OQ-7, CD-9]

### D18. Which key moves between the question list and the worker list?
- **Question:** The design says the worker list is "one key away" from the question list, but the spec's key list names no key (`EXPERIENCE.md:529`).
- **Why it matters:** Without it, the question view is not navigable as specified.
- **Options:** (a) pick the key at R2 from the keys still free; (b) pick now.
- **Recommendation:** (a). The question list ships no earlier than R2, and the key list may change before then.
- **Blocks:** R2 key help and the key handler.
- **First tasks start without it?** Yes. [UX-OQ-3, CD-15]

### D19. After the question-link gate, which view is the default: the question list (B) or the decision desk (C)?
- **Question:** Two of three design advocates prefer B as the default after links exist; one dissents for C (`rendering-rules.md:89`). The spec offers an optional owner re-confirm at that gate (`release-gates.md:13`).
- **Why it matters:** It sets the first screen people see once links work.
- **Options:** (a) B; (b) C; (c) decide at the gate.
- **Recommendation:** (c). C depends on two unverified contracts at once, so the right answer depends on what the link gate actually proves.
- **Blocks:** R3 only.
- **First tasks start without it?** Yes. [spec extra, part of the direction record]

## Tier 4: later stages (Go screen, staff platform, write-back)

### D20. Licence opinion before any Go screen in TUIBBS reads the snapshot
- **Question:** TUIBBS is licensed AGPL-3.0 (a strong copyleft licence) and is private. Before a Go screen inside TUIBBS reads the observer's snapshot, is a licence opinion needed on how the two may connect, and who gives it (`SPEC.md:108`)? Listed as open in the owner's record (`owner-decisions-20261108.md:17`).
- **Why it matters:** Whether reusing or linking TUIBBS code would put IronClaude under AGPL terms is exactly what the opinion must answer; nobody in this review is qualified to. The current design keeps the two apart: the observer writes a JSON file and contains no TUIBBS code (`ARCHITECTURE-SPINE.md:168`, `ARCHITECTURE-SPINE.md:306`).
- **Options:** (a) get a written opinion before any TUIBBS reader is built, keeping the file as the only connection; (b) build first and check later.
- **Recommendation:** (a). The opinion costs nothing now, and the file boundary already avoids the risk for R1; getting the opinion before the Go work starts prevents rework.
- **Blocks:** the later Go screen only. R1 still produces the snapshot.
- **First tasks start without it?** Yes. No AGPL code is used anywhere in R0 or R1. [OQ-9, CD-12]

### D21. Does TUIBBS become the platform for all human staff who manage agent teams?
- **Question:** The owner is exploring TUIBBS as the internal communication tool and platform for staff; the observer may become a TUIBBS module (`owner-decisions-20261108.md:15`).
- **Why it matters:** It decides whether the observer's long-term home is a standalone command or a TUIBBS screen.
- **Options:** (a) decide after R1 is in use; (b) decide now.
- **Recommendation:** (a). R1 is standalone by binding decision, and the snapshot file keeps both futures open; real R1 usage will inform the choice.
- **Blocks:** nothing in R0 to R3.
- **First tasks start without it?** Yes. [OQ-10, CD-12]

### D22. Is the change to allow write-back approved?
- **Question:** The owner wants users to send confirmations or corrections from the BBS to their agents (`owner-decisions-20261108.md:13`). Issue 409 requires a read-only observer and lists acting on workers as out of scope. Write-back needs an explicit boundary change on issue 409 and an amendment of TUIBBS rule FR-X-13 (`release-gates.md:18`).
- **Why it matters:** It is the one change that would let the screen act on agents, with the matching security and audit needs (credentials, delivery state, sender identity: `write-back-future-stage.md`).
- **Options:** (a) keep it not approved for now and revisit after R3; (b) approve the boundary change now as a future stage; (c) drop write-back.
- **Recommendation:** (a). Questions must be observable and linked (R2, R3) before an answer can be sent to the right place, and nothing in R1 may be reused as a write path (`ARCHITECTURE-SPINE.md:307`).
- **Blocks:** the future write-back stage only. Never R1.
- **First tasks start without it?** Yes. [OQ-11, CD-13]

### D23. How does Orca know who sent a reply?
- **Question:** For write-back, how does Orca's `reply` authenticate its sender? Until answered, replies must be relayed through the coordinator (`write-back-future-stage.md:50`). This needs Orca's owner.
- **Why it matters:** Without sender authentication, anyone at the screen could answer as anyone.
- **Options:** (a) ask Orca's owner when write-back is approved (D22); (b) ask now.
- **Recommendation:** (a). It only matters once D22 is approved, and Orca's answer may change by then.
- **Blocks:** the future write-back stage only.
- **First tasks start without it?** Yes. [spec extra, write-back stage]

## Already decided (not reopened)

These are binding and are not reopened here (`owner-decisions-20261108.md:5-17`):

1. **Staged releases.** R1 is Signal Bridge's worker list on the verified worker-list source, with the "question source UNVERIFIED" notice; the question list follows the question-observation gate; the decision desk sits behind the question-link gate. Whether this alone satisfies the direction gate is still the owner's to say (D11).
2. **Stack.** Python with Rich, a `superclaude observe` style command in IronClaude. R1 also writes a versioned JSON snapshot that only ever gains fields, with a schema test, for a later read-only Go screen in TUIBBS. The key-reader spike is the first task; if it fails, the project switches to Textual, never both.
3. **Read-only for R1.** Write-back is a future stage (D22).
4. **TUIBBS is background only** for R1; the licence opinion is open (D20).
5. **Unknown is never shown as zero or false.** Every fact keeps its evidence label; anything unchecked is marked UNVERIFIED; no Orca field is invented.
