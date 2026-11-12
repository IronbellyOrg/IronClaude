# Consolidated findings, cycle 0 (item 7.29)

Source: a Glob of `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/qa-*-report.md` found 8 reports (not a hard-coded list):

| Report | Lens item | Verdict | Blocking count | Raw findings | Checks PASS | Checks FAIL |
|---|---|---|---|---|---|---|
| qa-completeness-report.md | 7.21 | PASS | 0 | 4 | 20 | C21 |
| qa-cross-source-report.md | 7.28 | PASS | 0 | 9 | 26 | none |
| qa-crossref-chain-report.md | 7.27 | FAIL | 1 | 6 | 18 | C13 |
| qa-decision-fidelity-report.md | 7.25 | FAIL | 2 | 6 | 22 | C2, C15, C16 |
| qa-downstream-actionability-report.md | 7.26 | FAIL | 2 | 7 | 16 | C8, C9 |
| qa-evidence-quality-report.md | 7.23 | FAIL | 1 | 7 | 17 | C2, C18 |
| qa-readonly-safety-report.md | 7.24 | PASS | 0 | 6 | 19 | C20 |
| qa-record-form-report.md | 7.22 | FAIL | 1 | 3 | 14 | C12 |

Dedup rule (item 7.29): two findings are one when they name the same `file:line` and the same defect; the highest severity is kept and the merged duplicates are listed under the kept id. 48 raw findings were merged into 36 kept findings. Severity words are the reporting agent's own (BLOCKING, MAJOR, MINOR); reports 7.24 and 7.28 used only MINOR.

## F_0 and the cycle-0 PASS set

- `F_0` = {DEC-F1, DEC-F2, DEC-F3, DEC-F4, DEC-F5}
- `|F_0|` = 5
- Cycle-0 PASS set: 152 check ids, listed in full in the section "Cycle-0 PASS set" at the end of this file (and in the cycle-0 row of `cycle-ledger.md`).
- Open owner question inside `F_0`: DEC-F2 (OQ-1) can only be closed by the owner's own answer; the fix agent (item 7.30) must not invent it.

## BLOCKING and MAJOR findings

### DEC-F1 (BLOCKING): `artifacts/owner-decisions.md` has no row for the resolved OQ-17 decision, and its closing sentence says OQ-8 and OQ-17 are still open

- Reported by: qa-record-form:F1, qa-decision-fidelity:F-2, qa-crossref-chain:X-1, qa-cross-source:F2. Kept severity BLOCKING; merged duplicates: qa-decision-fidelity:F-2, qa-crossref-chain:X-1, qa-cross-source:F2.
- Evidence: `artifacts/owner-decisions.md:5` (heading says seven rows), `:9-15` (rows OQ-1 to OQ-7 only), `:55` ("Still open ... OQ-8 ... and the optional OQ-17 and OQ-18"); `phase-outputs/plans/OQ-17-cursor-template-decision.md:3,35-40` (RESOLVED, filled); `phase-outputs/plans/OQ-8-run-id-decision.md:3,26-29` (RESOLVED). Items 7.22 (task file line 1307) and 7.25 (line 1328) require one row for each resolved OQ-17 or OQ-18 file that exists.
- Smallest fix: Append one OQ-17 row in the same shape (refuse the cursor command, allowlist stays at 10; words "Keep the 10 commands (Recommended)"; Ryan Wiancko, owner, 2026-11-11; source `OQ-17-cursor-template-decision.md:35-40`; unblocks 7.17 resume, step 1.2 on, 8.10 and 10.3 at 10 templates); change the heading count to eight rows; rewrite `:55` to say OQ-8 and OQ-17 are RESOLVED and OQ-18 was not written. Do not change any `Chosen:` line.

### DEC-F2 (MAJOR): OQ-1 (R5, `worktree ps --agent-wait`) rests on a coordinator relay, not on the owner's own answer

- Reported by: qa-decision-fidelity:F-1, qa-completeness:F2, qa-evidence-quality:F7, qa-cross-source:F3. Kept severity MAJOR; merged duplicates: qa-completeness:F2, qa-evidence-quality:F7, qa-cross-source:F3.
- Evidence: `phase-outputs/plans/OQ-1-agent-wait-decision.md:22` ("relayed by the coordinator", messages `msg_d95a87e312e1` and `msg_6ee5998d0874`); the phrase appears in the session store only inside a tool result (2026-11-08T12:05:48Z), never as a direct owner turn; `revisions/chat-output-exception-20261109-133150/BUILD-REQUEST.md:15` ("Peer relays are corroboration only"); the R5 edit sits at DESIGN `:535-536`, `:837`, `:895`, `:1047`. Disclosed at `artifacts/owner-decisions.md:17`. Note from the review of item 7.25: the R5 gate logged this relay as MINOR (R5-F8), and the direct-answer rule comes from the 2026-11-09 revision, so the MAJOR rating is the lens's reading.
- Smallest fix: Needs the owner: put one direct question ("May the sweep's allowlist include `worktree ps --agent-wait`, with and without `--json`?"). On yes, add the answer and date to the Decision source of `OQ-1-agent-wait-decision.md` and to the OQ-1 row of `owner-decisions.md` (mark the earlier words as relayed). On no, revert R5 by a design revision.

### DEC-F3 (MAJOR): "No worker-show field holds a Claude session id" is contradicted by the stored raw outputs

- Reported by: qa-evidence-quality:F1. Kept severity MAJOR; merged duplicates: none.
- Evidence: `artifacts/readonly-probe.md:499` and `phase-outputs/discovery/1.0a-facts.md:11` (row 1) say no field holds a session id; in all five `artifacts/readonly-probe-raw/b-ws-*.json`, `result.terminal.preview` contains `claude --resume <session id>`, equal to line 1 of that worker's tab-map entry (`readonly-probe.md:1048-1052`); the probe admits it for one worker only (`:1059`).
- Smallest fix: Replace the two sentences with: "No structured `worker-show` field holds a Claude session id. The id appears only as free text in `result.terminal.preview` (`claude --resume <id>`) for all 5 exited workers; whether a live worker's preview shows it is UNVERIFIED, so it is not used as a join. Path B applies." in `readonly-probe.md:499` and `1.0a-facts.md` row 1.

### DEC-F4 (MAJOR): The join field for `session_join` is never chosen

- Reported by: qa-downstream-actionability:F1. Kept severity MAJOR; merged duplicates: none.
- Evidence: `phase-outputs/discovery/1.0a-facts.md:11` says `assigneePaneKey` "and" `assigneeHandle`; the field table at `:34` says "or"; DESIGN `:457` types `session_join: str | None` (one value); `:460` stores the tab-map `file_name` with `:` already written as `+`; `:497` compares `session_join` to `file_name` or `terminal_handle`; item 8.3 (task file line 1438) names no source field.
- Smallest fix: Add one line to `1.0a-facts.md` (rows 1 and 22 and the field table): `session_join` = `result.dispatch.assigneeHandle`, compared by equality with `TabMapEntry.terminal_handle`; `assigneePaneKey` is not stored (or name the pane key plus the `:` to `+` rule).

### DEC-F5 (MAJOR): No rule for comparing the live Orca version with `CHECKED_ORCA_VERSION`, and the design's test string is stale

- Reported by: qa-downstream-actionability:F2. Kept severity MAJOR; merged duplicates: none.
- Evidence: `1.0a-facts.md:22` records live `1.4.245-aidev02.9cfecdd30b2a`; DESIGN `:30` and the `test_report.py` row (`:761`) and item 10.5 (task file line 1812) still use `...780594c521aa`; `CHECKED_ORCA_VERSION = "1.4.245"` (DESIGN `:426`); DESIGN `:611-612` pick "unlikely" or "UNVERIFIED" with no comparison rule.
- Smallest fix: State the rule in `1.0a-facts.md` row 15 or in item 8.12 (for example "text before the first `-` equals `CHECKED_ORCA_VERSION`") and make item 10.5 test the live string, `1.4.246` and a missing file.

## MINOR findings (never fail the gate)

### DEC-F6 (MINOR): `decisions-mechanical.md` run times are not real (22:40Z, 22:50Z, 22:58Z are later than the file's own last write)

- Reported by: qa-completeness:F1.
- Evidence: `phase-outputs/test-results/decisions-mechanical.md:5,237,471`.
- Smallest fix: Delete the clock times or replace them with real ones.

### DEC-F7 (MINOR): The envelope-id reading of "identical apart from timestamps" and Deviation D1 are executor judgments the owner has not acknowledged

- Reported by: qa-completeness:F3, qa-evidence-quality:F2, qa-readonly-safety:M1, qa-decision-fidelity:N-4, qa-cross-source:F7. Merged duplicates under this id: qa-evidence-quality:F2, qa-readonly-safety:M1, qa-decision-fidelity:N-4, qa-cross-source:F7.
- Evidence: `artifacts/readonly-probe.md:783,1071`; `1.0a-facts.md:21`; DESIGN `:897`.
- Smallest fix: Tell the owner at the next touchpoint; optionally add "and the envelope request id" to DESIGN `:897` when 15.1 is next edited.

### DEC-F8 (MINOR): Deviation D1 is mis-framed (DESIGN 15.1 row 8 asks for that error shape) and item 7.15's extra template 2 reads are not in the probe's compliance record

- Reported by: qa-readonly-safety:M6.
- Evidence: `artifacts/readonly-probe.md:1071`; DESIGN `:911`; `phase-outputs/plans/OQ-8-run-id-decision.md:31-44`.
- Smallest fix: Reword D1 and mention the 7.15 reads in the compliance record.

### DEC-F9 (MINOR): `1.0a-facts.md` rows 3, 6 (`agentWait`), 9 and 16 stay STILL UNVERIFIED (informational)

- Reported by: qa-completeness:F4.
- Evidence: `1.0a-facts.md:13,16,19,23`.
- Smallest fix: None; later steps use the DESIGN fail-safe behaviour.

### DEC-F10 (MINOR): OQ-8 has no options section

- Reported by: qa-record-form:M1.
- Evidence: `OQ-8-run-id-decision.md:8-22`.
- Smallest fix: None needed (it is a request, not a choice).

### DEC-F11 (MINOR): OQ-1 status lines sit in a yaml code block, not front matter

- Reported by: qa-record-form:M2.
- Evidence: `OQ-1-agent-wait-decision.md:3-6`.
- Smallest fix: None needed.

### DEC-F12 (MINOR): "11 Run ids" in facts row 2 mixes sources (1 observed, 9 from the OQ-8 paste, 1 made up)

- Reported by: qa-evidence-quality:F3.
- Evidence: `1.0a-facts.md:12`.
- Smallest fix: Write "1 observed in the capture, 9 from OQ-8, 1 made up".

### DEC-F13 (MINOR): `pr422-409-check.md` mentions two `git cat-file -t` outputs it does not record

- Reported by: qa-evidence-quality:F4.
- Evidence: `artifacts/pr422-409-check.md:3,23,31`.
- Smallest fix: Record the two outputs or drop the sentences.

### DEC-F14 (MINOR): The second `ls -la` of the tab-map folder is not listed in Deviations

- Reported by: qa-evidence-quality:F5.
- Evidence: `readonly-probe.md:1021`.
- Smallest fix: Add one line to Deviations.

### DEC-F15 (MINOR): Time-bound results in `decisions-mechanical.md` (S8 and C9 stop being true once item 8 starts)

- Reported by: qa-evidence-quality:F6.
- Evidence: `decisions-mechanical.md` S8, C9.
- Smallest fix: None today; note that they are as of the run.

### DEC-F16 (MINOR): Probe header says "every command ran in its own Bash call"; the scratch files show scripted batches

- Reported by: qa-readonly-safety:M2.
- Evidence: `readonly-probe.md:8`; `/tmp/probe-7-16/` file times.
- Smallest fix: Reword to say the reads ran in scripted batches with per-command output capture.

### DEC-F17 (MINOR): Extra writes (16 raw files, `/tmp/probe-7-16/` scratch holding the raw process-status output) are disclosed but not listed as a deviation

- Reported by: qa-readonly-safety:M3.
- Evidence: `readonly-probe.md:8,10`; DESIGN `:890`.
- Smallest fix: Add the raw folder to Deviations and delete `/tmp/probe-7-16/` once nothing needs it.

### DEC-F18 (MINOR): Fixtures keep real project, branch and folder names after the home prefix is replaced

- Reported by: qa-readonly-safety:M4.
- Evidence: `tests/sweep/fixtures/` (for example `captured-worktree-ps.json:97,197`).
- Smallest fix: State in `SOURCES.md` that project and branch names are kept on purpose.

### DEC-F19 (MINOR): Order of the reads is provable only from files outside the package

- Reported by: qa-readonly-safety:M5.
- Evidence: raw copies share one mtime (21:43:30).
- Smallest fix: None; informational.

### DEC-F20 (MINOR): The style text goes past "an exception to the table" and the owner never saw its wording

- Reported by: qa-decision-fidelity:N-1.
- Evidence: `pragmatic.md:23`; `design-addendum.md:13-21`.
- Smallest fix: Do not call the wording "owner-approved" in later gates.

### DEC-F21 (MINOR): "Accepted ... Proceed" is mapped to a specific option by the executor, and `owner-decisions.md` states the scope as fact

- Reported by: qa-decision-fidelity:N-2, qa-cross-source:F4. Merged duplicates under this id: qa-cross-source:F4.
- Evidence: `owner-decisions.md:29-33`; `step-7.10-style-exception.md:13,19`.
- Smallest fix: In `owner-decisions.md:33` say the executor read it as authorizing item 7.10 only.

### DEC-F22 (MINOR): OQ-8: the owner picked the assistant's own recommended option although the question said the assistant's pick does not count

- Reported by: qa-decision-fidelity:N-3.
- Evidence: `OQ-8-run-id-decision.md:29`.
- Smallest fix: None; the owner's own selection of a labelled option, recorded honestly.

### DEC-F23 (MINOR): Rule 5 cannot match: DESIGN needs `status == "in_progress"`, which is not in the listed status values

- Reported by: qa-downstream-actionability:F3.
- Evidence: DESIGN `:491,907`; `1.0a-facts.md:16`.
- Smallest fix: Code item 8.4 to the DESIGN literal; the class stays unreachable in Phase 1.

### DEC-F24 (MINOR): The facts "field names" table omits names steps 1.3/1.4 need (WC-13 `parent` path, `worker-list` row keys)

- Reported by: qa-downstream-actionability:F4.
- Evidence: `1.0a-facts.md` field table; `captured-worker-list.json`.
- Smallest fix: List the missing names.

### DEC-F25 (MINOR): Style to skill to test: small gaps in the traced rule (non-exempt reply wording, "summary counts" undefined, "Read successfully")

- Reported by: qa-downstream-actionability:F5.
- Evidence: item 11.3 step (4); DESIGN `:590-591`.
- Smallest fix: Add one clause to item 11.3 for each.

### DEC-F26 (MINOR): A clause is pinned by item 11.4 but not required by 11.3; skill directory name `sc-sweep-protocol` vs frontmatter name `sc:sweep-protocol`

- Reported by: qa-downstream-actionability:F6.
- Evidence: `pragmatic.md:25`; items 11.3, 11.4.
- Smallest fix: Say "style only" in 11.4 or add the clause to 11.3; key 11.4 on the directory name.

### DEC-F27 (MINOR): Stale DESIGN line numbers in downstream text (items 8.12, 10.5, 7.17, the facts file, research/09)

- Reported by: qa-downstream-actionability:F7, qa-cross-source:F6. Merged duplicates under this id: qa-cross-source:F6.
- Evidence: task file lines 1267, 1501, 1812, 1815; `1.0a-facts.md:21`; `research/09-gap-fill.md:89`.
- Smallest fix: Executors of 8.12 and 10.5 re-locate by heading (the Phase 8 preamble already says so).

### DEC-F28 (MINOR): Open Questions bullets in the task file still read PENDING

- Reported by: qa-crossref-chain:L-1.
- Evidence: task file lines 2989-2995, 3004.
- Smallest fix: Optionally add "RESOLVED, see Execution Log"; kept as history by design.

### DEC-F29 (MINOR): OQ-5 names item 10.5 but item 10.5 never cites OQ-5

- Reported by: qa-crossref-chain:L-2.
- Evidence: `OQ-5-GQ-61-window-decision.md:29`; task file line 1812.
- Smallest fix: Add "window default per the OQ-5 record" to item 10.5 Context.

### DEC-F30 (MINOR): Three blocked items rely on a gate item instead of citing the record (OQ-3: 12.2, 12.3; OQ-17: 8.10, 10.3)

- Reported by: qa-crossref-chain:L-3.
- Evidence: `OQ-3-GQ-11-rule-id-decision.md:30`; `OQ-17-cursor-template-decision.md:33`; task file lines 1487, 1490, 1798.
- Smallest fix: Add one clause to item 8.10: OQ-17 refused a cursor template, do not page by the cursor field.

### DEC-F31 (MINOR): The R5 edit surface is listed three ways (section 4 missing from the Phase 7 lists)

- Reported by: qa-crossref-chain:L-4.
- Evidence: `OQ-1-agent-wait-decision.md:41`; task file lines 1000, 1299; DESIGN `:221`.
- Smallest fix: None; the R5 gate passed and the record is frozen.

### DEC-F32 (MINOR): Consumers of OQ-2 and OQ-5 (items 11.1, 10.5) that the records do not list (informational)

- Reported by: qa-crossref-chain:L-5.
- Evidence: task file line 1958.
- Smallest fix: None.

### DEC-F33 (MINOR): The signed-off D9 text and open item 22 still say the sign-off is pending

- Reported by: qa-cross-source:F1.
- Evidence: DESIGN `:836,875,1012`; `OQ-7-D9-signoff-decision.md:40-43`.
- Smallest fix: Treat the OQ-7 record and facts row 22 as the closure; optionally append one closure sentence under section 13. Do not rewrite D9.

### DEC-F34 (MINOR): The design append points at a "section 15.2 GQ-63/style/skill/test allocation" that section 15.2 does not contain

- Reported by: qa-cross-source:F5.
- Evidence: DESIGN `:1051`; `design-addendum.md:9`.
- Smallest fix: None for this gate.

### DEC-F35 (MINOR): The pr422/#409 ancestry result rests on the local `origin/master` ref, which the item forbade refreshing

- Reported by: qa-cross-source:F8.
- Evidence: `pr422-409-check.md:3,31`; DESIGN `:947`.
- Smallest fix: None; disclosed and reproducible.

### DEC-F36 (MINOR): The D4 re-anchor for "never posted" cites the `.gitignore` comment line 736, not the WC-16 text at `:679`

- Reported by: qa-cross-source:F9.
- Evidence: `artifacts/owner-decisions.md:42`.
- Smallest fix: Cite `:679` (and `:736` as the second place).

## Coverage of every report finding (raw id to kept id)

| Report | Raw id | Kept id |
|---|---|---|
| qa-completeness | F1 | DEC-F6 |
| qa-completeness | F2 | DEC-F2 |
| qa-completeness | F3 | DEC-F7 |
| qa-completeness | F4 | DEC-F9 |
| qa-cross-source | F1 | DEC-F33 |
| qa-cross-source | F2 | DEC-F1 |
| qa-cross-source | F3 | DEC-F2 |
| qa-cross-source | F4 | DEC-F21 |
| qa-cross-source | F5 | DEC-F34 |
| qa-cross-source | F6 | DEC-F27 |
| qa-cross-source | F7 | DEC-F7 |
| qa-cross-source | F8 | DEC-F35 |
| qa-cross-source | F9 | DEC-F36 |
| qa-crossref-chain | X-1 | DEC-F1 |
| qa-crossref-chain | L-1 | DEC-F28 |
| qa-crossref-chain | L-2 | DEC-F29 |
| qa-crossref-chain | L-3 | DEC-F30 |
| qa-crossref-chain | L-4 | DEC-F31 |
| qa-crossref-chain | L-5 | DEC-F32 |
| qa-decision-fidelity | F-1 | DEC-F2 |
| qa-decision-fidelity | F-2 | DEC-F1 |
| qa-decision-fidelity | N-1 | DEC-F20 |
| qa-decision-fidelity | N-2 | DEC-F21 |
| qa-decision-fidelity | N-3 | DEC-F22 |
| qa-decision-fidelity | N-4 | DEC-F7 |
| qa-downstream-actionability | F1 | DEC-F4 |
| qa-downstream-actionability | F2 | DEC-F5 |
| qa-downstream-actionability | F3 | DEC-F23 |
| qa-downstream-actionability | F4 | DEC-F24 |
| qa-downstream-actionability | F5 | DEC-F25 |
| qa-downstream-actionability | F6 | DEC-F26 |
| qa-downstream-actionability | F7 | DEC-F27 |
| qa-evidence-quality | F1 | DEC-F3 |
| qa-evidence-quality | F2 | DEC-F7 |
| qa-evidence-quality | F3 | DEC-F12 |
| qa-evidence-quality | F4 | DEC-F13 |
| qa-evidence-quality | F5 | DEC-F14 |
| qa-evidence-quality | F6 | DEC-F15 |
| qa-evidence-quality | F7 | DEC-F2 |
| qa-readonly-safety | M1 | DEC-F7 |
| qa-readonly-safety | M2 | DEC-F16 |
| qa-readonly-safety | M3 | DEC-F17 |
| qa-readonly-safety | M4 | DEC-F18 |
| qa-readonly-safety | M5 | DEC-F19 |
| qa-readonly-safety | M6 | DEC-F8 |
| qa-record-form | F1 | DEC-F1 |
| qa-record-form | M1 | DEC-F10 |
| qa-record-form | M2 | DEC-F11 |

Check: 48 raw finding ids parsed from the report headings; 48 mapped; unmapped: none; mapped to a non-existent raw id: none.

## Cycle-0 PASS set

152 check ids (every check a report's `## Checks` table marks PASS, including `PASS (note ...)` rows), written `<report name>:C<n> (item <lens item id>)`:

- qa-completeness (item 7.21), 20 PASS: qa-completeness:C1 (item 7.21), qa-completeness:C2 (item 7.21), qa-completeness:C3 (item 7.21), qa-completeness:C4 (item 7.21), qa-completeness:C5 (item 7.21), qa-completeness:C6 (item 7.21), qa-completeness:C7 (item 7.21), qa-completeness:C8 (item 7.21), qa-completeness:C9 (item 7.21), qa-completeness:C10 (item 7.21), qa-completeness:C11 (item 7.21), qa-completeness:C12 (item 7.21), qa-completeness:C13 (item 7.21), qa-completeness:C14 (item 7.21), qa-completeness:C15 (item 7.21), qa-completeness:C16 (item 7.21), qa-completeness:C17 (item 7.21), qa-completeness:C18 (item 7.21), qa-completeness:C19 (item 7.21), qa-completeness:C20 (item 7.21)
- qa-cross-source (item 7.28), 26 PASS: qa-cross-source:C1 (item 7.28), qa-cross-source:C2 (item 7.28), qa-cross-source:C3 (item 7.28), qa-cross-source:C4 (item 7.28), qa-cross-source:C5 (item 7.28), qa-cross-source:C6 (item 7.28), qa-cross-source:C7 (item 7.28), qa-cross-source:C8 (item 7.28), qa-cross-source:C9 (item 7.28), qa-cross-source:C10 (item 7.28), qa-cross-source:C11 (item 7.28), qa-cross-source:C12 (item 7.28), qa-cross-source:C13 (item 7.28), qa-cross-source:C14 (item 7.28), qa-cross-source:C15 (item 7.28), qa-cross-source:C16 (item 7.28), qa-cross-source:C17 (item 7.28), qa-cross-source:C18 (item 7.28), qa-cross-source:C19 (item 7.28), qa-cross-source:C20 (item 7.28), qa-cross-source:C21 (item 7.28), qa-cross-source:C22 (item 7.28), qa-cross-source:C23 (item 7.28), qa-cross-source:C24 (item 7.28), qa-cross-source:C25 (item 7.28), qa-cross-source:C26 (item 7.28)
- qa-crossref-chain (item 7.27), 18 PASS: qa-crossref-chain:C1 (item 7.27), qa-crossref-chain:C2 (item 7.27), qa-crossref-chain:C3 (item 7.27), qa-crossref-chain:C4 (item 7.27), qa-crossref-chain:C5 (item 7.27), qa-crossref-chain:C6 (item 7.27), qa-crossref-chain:C7 (item 7.27), qa-crossref-chain:C8 (item 7.27), qa-crossref-chain:C9 (item 7.27), qa-crossref-chain:C10 (item 7.27), qa-crossref-chain:C11 (item 7.27), qa-crossref-chain:C12 (item 7.27), qa-crossref-chain:C14 (item 7.27), qa-crossref-chain:C15 (item 7.27), qa-crossref-chain:C16 (item 7.27), qa-crossref-chain:C17 (item 7.27), qa-crossref-chain:C18 (item 7.27), qa-crossref-chain:C19 (item 7.27)
- qa-decision-fidelity (item 7.25), 22 PASS: qa-decision-fidelity:C1 (item 7.25), qa-decision-fidelity:C3 (item 7.25), qa-decision-fidelity:C4 (item 7.25), qa-decision-fidelity:C5 (item 7.25), qa-decision-fidelity:C6 (item 7.25), qa-decision-fidelity:C7 (item 7.25), qa-decision-fidelity:C8 (item 7.25), qa-decision-fidelity:C9 (item 7.25), qa-decision-fidelity:C10 (item 7.25), qa-decision-fidelity:C11 (item 7.25), qa-decision-fidelity:C12 (item 7.25), qa-decision-fidelity:C13 (item 7.25), qa-decision-fidelity:C14 (item 7.25), qa-decision-fidelity:C17 (item 7.25), qa-decision-fidelity:C18 (item 7.25), qa-decision-fidelity:C19 (item 7.25), qa-decision-fidelity:C20 (item 7.25), qa-decision-fidelity:C21 (item 7.25), qa-decision-fidelity:C22 (item 7.25), qa-decision-fidelity:C23 (item 7.25), qa-decision-fidelity:C24 (item 7.25), qa-decision-fidelity:C25 (item 7.25)
- qa-downstream-actionability (item 7.26), 16 PASS: qa-downstream-actionability:C1 (item 7.26), qa-downstream-actionability:C2 (item 7.26), qa-downstream-actionability:C3 (item 7.26), qa-downstream-actionability:C4 (item 7.26), qa-downstream-actionability:C5 (item 7.26), qa-downstream-actionability:C6 (item 7.26), qa-downstream-actionability:C7 (item 7.26), qa-downstream-actionability:C10 (item 7.26), qa-downstream-actionability:C11 (item 7.26), qa-downstream-actionability:C12 (item 7.26), qa-downstream-actionability:C13 (item 7.26), qa-downstream-actionability:C14 (item 7.26), qa-downstream-actionability:C15 (item 7.26), qa-downstream-actionability:C16 (item 7.26), qa-downstream-actionability:C17 (item 7.26), qa-downstream-actionability:C18 (item 7.26)
- qa-evidence-quality (item 7.23), 17 PASS: qa-evidence-quality:C1 (item 7.23), qa-evidence-quality:C3 (item 7.23), qa-evidence-quality:C4 (item 7.23), qa-evidence-quality:C5 (item 7.23), qa-evidence-quality:C6 (item 7.23), qa-evidence-quality:C7 (item 7.23), qa-evidence-quality:C8 (item 7.23), qa-evidence-quality:C9 (item 7.23), qa-evidence-quality:C10 (item 7.23), qa-evidence-quality:C11 (item 7.23), qa-evidence-quality:C12 (item 7.23), qa-evidence-quality:C13 (item 7.23), qa-evidence-quality:C14 (item 7.23), qa-evidence-quality:C15 (item 7.23), qa-evidence-quality:C16 (item 7.23), qa-evidence-quality:C17 (item 7.23), qa-evidence-quality:C19 (item 7.23)
- qa-readonly-safety (item 7.24), 19 PASS: qa-readonly-safety:C1 (item 7.24), qa-readonly-safety:C2 (item 7.24), qa-readonly-safety:C3 (item 7.24), qa-readonly-safety:C4 (item 7.24), qa-readonly-safety:C5 (item 7.24), qa-readonly-safety:C6 (item 7.24), qa-readonly-safety:C7 (item 7.24), qa-readonly-safety:C8 (item 7.24), qa-readonly-safety:C9 (item 7.24), qa-readonly-safety:C10 (item 7.24), qa-readonly-safety:C11 (item 7.24), qa-readonly-safety:C12 (item 7.24), qa-readonly-safety:C13 (item 7.24), qa-readonly-safety:C14 (item 7.24), qa-readonly-safety:C15 (item 7.24), qa-readonly-safety:C16 (item 7.24), qa-readonly-safety:C17 (item 7.24), qa-readonly-safety:C18 (item 7.24), qa-readonly-safety:C19 (item 7.24)
- qa-record-form (item 7.22), 14 PASS: qa-record-form:C1 (item 7.22), qa-record-form:C2 (item 7.22), qa-record-form:C3 (item 7.22), qa-record-form:C4 (item 7.22), qa-record-form:C5 (item 7.22), qa-record-form:C6 (item 7.22), qa-record-form:C7 (item 7.22), qa-record-form:C8 (item 7.22), qa-record-form:C9 (item 7.22), qa-record-form:C10 (item 7.22), qa-record-form:C11 (item 7.22), qa-record-form:C13 (item 7.22), qa-record-form:C14 (item 7.22), qa-record-form:C15 (item 7.22)

Checks marked FAIL in cycle 0 (not in the PASS set): qa-completeness:C21 (item 7.21); qa-crossref-chain:C13 (item 7.27); qa-decision-fidelity:C2 (item 7.25); qa-decision-fidelity:C15 (item 7.25); qa-decision-fidelity:C16 (item 7.25); qa-downstream-actionability:C8 (item 7.26); qa-downstream-actionability:C9 (item 7.26); qa-evidence-quality:C2 (item 7.23); qa-evidence-quality:C18 (item 7.23); qa-readonly-safety:C20 (item 7.24); qa-record-form:C12 (item 7.22).

