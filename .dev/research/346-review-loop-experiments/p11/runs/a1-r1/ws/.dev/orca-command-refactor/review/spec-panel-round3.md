# Spec panel round 3: orca-worker-contract-spec.md (Task 8 revision)

review: 1 of 3

Result: FAIL. 4 blocking findings (R3-01 to R3-04) and 6 further findings (R3-05 to R3-10) are open; of the 15 round-2 findings, 12 are resolved and 3 partly resolved (Part 1).

## Run mode, citation keys and limits
Task 9, independent re-review of the Task 8 revision. Planning only: this file is the only file written. Command run as defined in `command.md`: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`, plus the brief's parts 1 and 2 (resolution table, citation check) in front of it.

- **Keys.** `SPEC:N` = line N of the live spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (95578 bytes, 424 lines). `V2:N` = `specs/history/spec-v2.md` (80732 bytes, the text the round-2 review read; byte-identical to the saved `spec-before-task8.md`). `R2:N` = `review/spec-panel-round2.md`. `DISP:N` = `review/disposition.md` (Task 6). `DISP2:N` = `review/disposition-round2.md` (Task 8). `INV-A:N`, `INV-B:N`, `CAPS:N` = `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `SPCMD:N` = line N of the `/sc:spec-panel` definition `command.md` in the sandbox root, used here only for the review procedure.
- **Header.** No `--re-review` or `--baseline` was passed, so under Review Loop bullet 1 (`SPCMD:258`) this is a first review of the full document and the header is `review: 1 of 3`; "round 3" is the coordinator's label. No prior-findings file at `review: 3` was supplied, so the HALT check (`SPCMD:261`) does not fire. I still tag every new finding `origin=changed` (text touched by the Task 8 revision, from `diff V2 SPEC`: 74 added or changed lines in 41 hunks, from `SPEC:5` to `SPEC:424`) or `origin=unchanged`.
- **Grading conflict, stated openly.** The brief says any finding of any severity is FAIL. Review Loop bullet 7 (`SPCMD:264`) says a brief may not grade a minor finding as blocking, and bullet 2 (`SPCMD:259`) makes MINOR a note. I follow the command for the blocking flag and the Reviser brief; the verdict is FAIL under both rules because four blocking findings are open (R3-01 to R3-04) and six more findings exist.
- **What could be checked.** The workspace holds the spec, `V2`, `V1`, the README, the three inventories, `R1`, `R2`, `DISP`, `DISP2` and the (empty) `home/.claude`. `src/`, `~/.claude`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...`, `pyproject.toml`, `orca-ide` output and Orca's JS are not in the sandbox, no `rf-qa.md` exists under `home/` or `ws/` (so the Review Loop bullet 5 re-check procedure stands alone), and no Orca command can be run. A citation to any of those is checked only against the inventory line that quotes it; otherwise it is UNVERIFIED. No live check from spec section 7 was run.
- **Method.** Read all of `command.md`, `README`, `R2`, `DISP2`, the live spec (every line), the inventory lines the Task 8 text cites, and `CAPS:40-188`. Built the changed-line set with `diff V2 SPEC` and extracted the 82 `INV-A`/`INV-B`/`CAPS`/source citation tokens in the 23 changed lines that carry any (19 of them first appear in their line). Re-ran four mechanical checks on the live spec: table column counts for every table (one defect, R3-06), the `--unattended` without `--report-dir` scan over section 7 (clean), the placeholder greps of `DISP2:12` (both results confirmed), and the phase and count arithmetic (43 = 10 + 27 + 6; 37 = 15 + 15 + 4 + 3; P1 = 14 + load). System `python3` was used for these read-only scans (no repo code exists in the sandbox, so the `uv run` rule does not apply; same departure as `R2:333`).

## Part 1: Resolution of round-2 findings N-01 to N-15 and the six overstated citations
Each row was checked against the live spec text, not against `DISP2`. `resolved` = the spec text now does what the finding asked and I found no defect on it; `partly` = the text changed but a defect remains on the same point (carried into Part 3); `open` = not resolved. `regressed` (a finding the prior report marked resolved that fails again) is empty: `R2` marked nothing resolved.

| # | Round-2 finding (grade) | What the live spec now says (evidence) | Result | Residual |
|---|---|---|---|---|
| N-01 | WC-13 vs phase gate (CRITICAL, blocking) | WC-13 passes `--unattended` only to children "whose phase has passed" and gives an interim rule (present flags, no-gate configuration, optional step left out, skills outside the 43 are outside the pass-through) (SPEC:74); the `Nested:` line must say per child which applies (SPEC:55, SPEC:74); P2 updates the parents' lines (SPEC:211); AC-1.1 asserts the per-child statement (SPEC:254), AC-1.2 checks workflow's reflect gets no flag (SPEC:255); 7.4 (SPEC:292); Decisions (SPEC:352); UNVERIFIED 23 (SPEC:385). Counts: 14 commands accept the flag when P1 ends and none is asked to pass it to an unconverted child. | resolved | Same rule leaves the tasklist to `sc:task` leg unnamed (R3-04). |
| N-02 | New report dir per attempt cannot reach a retry (MAJOR, blocking) | Report base in the brief, `<report base>/<dispatch_id>/` composed by the worker (SPEC:54, SPEC:65, SPEC:67, SPEC:79-80, SPEC:102, SPEC:236, SPEC:350); overwrite rule stated (SPEC:65); AC-2.7 now keeps the Task text unchanged and compares the first contract's hash (SPEC:264); the Dispatch ID reaching the worker is backed by `CAPS:148`; that `worker-start` returns it and takes no new text is labelled UNVERIFIED (SPEC:65, SPEC:383). | resolved | The premise it adopts (a retry reuses the Task text unchanged) breaks WC-6 for `--output` and resume values (R3-01) and for answers to a blocked gate (R3-02). |
| N-03 | Child dir not unique (MAJOR, blocking) | `<report-dir>/<child-command>-<k>/`, `k` the 1-based invocation count fixed before the child starts, tasklist uses the phase number (SPEC:74, SPEC:173); AC-2.1 (SPEC:258) and new AC-2.9 (SPEC:266); Decisions (SPEC:351). | resolved | none |
| N-04 | Four ACs trip the refusal (MAJOR, blocking) | Scan of section 7 for `--unattended` without `--report-dir` returns only AC-1.1, which runs no command (SPEC:254). AC-2.8 now has `--suite`, the safety flags by reference, `--unattended`, `--report-dir` (SPEC:265); AC-3.3, AC-3.4, AC-4.1 carry `--report-dir` (SPEC:269-271). | resolved | none |
| N-05 | WC-5 validity fails every non-contract worker (MAJOR, blocking) | Validity rule scoped to workers started with `--report-dir`; pre-conversion outcome rule (named file exists, non-empty, no failure reported; legacy words via AC-0.5) (SPEC:66); 2.3 item 2 (SPEC:79); P0 brief example (SPEC:92-98); 7.2 steps 3-4 (SPEC:239-240); AC-0.4 (SPEC:253); 7.4 (SPEC:284); Decisions (SPEC:353). | partly | The pre-conversion rule needs "the command's own named file", and the adversarial smoke run of AC-0.4 has none (R3-03); the two branches of WC-5 do not cover every flag combination (R3-05). |
| N-06 | WC-10 forbids what WC-7/E4 require (MAJOR, blocking) | Cap limited to calls that wait on something outside the session; foreground Agent-tool fan-out and synchronous work exempt; heartbeat before and after; UNVERIFIED stated (SPEC:71); cross-reference in WC-7 (SPEC:68); AC-2.8 and AC-4.3 say "wait call" (SPEC:265, SPEC:273); 7.4 (SPEC:289); Decisions (SPEC:348); UNVERIFIED 22 (SPEC:384). | resolved | none |
| N-07 | "No second copy" starves nested readers (MAJOR) | WC-13 last sentence: under `--unattended` a parent reads the child's contract in the child's report directory; the legacy location applies only to runs without `--report-dir` (SPEC:74); UNVERIFIED 16 (SPEC:378). | resolved | none |
| N-08 | Coordinator procedure contradicts itself (MAJOR) | 2.3 now says the breaker counts failed `worker-start` attempts, not a worker's own `failed` report (`CAPS:80`, `CAPS:116`), the coordinator bounds retries itself (one retry, then the person), asks the person at its own limit and keeps polling, and stops, abandons or releases only on positive proof (SPEC:85); Decisions (SPEC:354). Both `CAPS` lines say what is claimed. | resolved | The new one-retry rule is applied to `blocked` outcomes as well, where it cannot work (R3-02). |
| N-09 | Supplied `/sc:spec-panel` already has the flags (MAJOR) | AC-1.1 no longer asserts that nothing outside the P1 list carries the flag; it asserts nothing outside the list gains it in the phase's diff (SPEC:254); P0 records the baseline (SPEC:209); new AC-0.6 (SPEC:252); the spec-panel row is untouched (SPEC:171) and item 19 stays UNVERIFIED (SPEC:381). `command.md:22-23,451-461` confirm the baseline difference exists in the supplied text. Accepted as applied in part (`DISP2:26`). | resolved | none |
| N-10 | 3.1 intro stale (MINOR) | SPEC:130 names six commands converting in P1 and four in P2; matches the 3.1 rows (SPEC:134-143) and the P1 and P2 lists (SPEC:210-211). | resolved | none |
| N-11 | Rename needs a shell; version field (MINOR) | One Write call plus the WC-5 validity rule where no shell tool exists; `contract_version: 1` always added beside a legacy version field (SPEC:65). | resolved | none |
| N-12 | `--answer` grammar (MINOR) | Split at the first `=`, one quoted argument that may contain `=`, unknown or repeated id is a usage error (SPEC:64). | resolved | none |
| N-13 | Cap bounds a call, not the gap (MINOR) | "A heartbeat immediately before each wait call longer than 1 minute" (SPEC:71); Decisions row rewritten with the correct arithmetic (SPEC:348). | resolved | none |
| N-14 | Validation claims describe old text (MINOR) | SPEC:13 and SPEC:376 now say "as of the Task 4 text". The two disposition cites (`DISP:10`, `DISP:19`) were deliberately not edited (`DISP2:55`). | partly | `DISP:10` and `DISP:19` still carry the wrong claims (R3-10). |
| N-15 | Editorial nits (a) to (g) (MINOR) | (a) D1 example is `/sc:analyze` (SPEC:310); (b) pr-submit row and AC-4.3 put the contract in `--report-dir` and the run log under `--output-dir` (SPEC:165, SPEC:273); (c) AC-2.5 now before AC-2.6 and AC-2.8 (SPEC:262-265), AC-0.5 deliberately stays before AC-0.4 with "Run after AC-0.5 and AC-0.6" (SPEC:251-253); (d) AC-C1 says a prose hit fails (SPEC:223); (e) AC-2.9 and the AC-1.2 workflow check (SPEC:255, SPEC:266); (f) `SPCMD` defined (SPEC:12); (g) SA-2 names the two documents (SPEC:198). | partly | (f): the definition says `SPCMD` is cited in "sections 2.2, 9 and the UNVERIFIED list"; it is cited in the Decisions table, the UNVERIFIED list and the revision log (SPEC:349, SPEC:381, SPEC:423), not in 2.2 or 9 (R3-07). |
| C-1 | SPEC:84 (V2), `CAPS:116` circuit breaker (overstated) | SPEC:85 cites `CAPS:80` for what the breaker counts and `CAPS:116` for the retry form and the "do not route around" clause; both lines say that. | resolved | none |
| C-2 | `:151-152` range (overstated) | WC-10 evidence cell now cites `sk/sc-cli-eval-protocol/SKILL.md:151` via `INV-A:65` (SPEC:71); `INV-A:65` cites `:151` only. | resolved | none |
| C-3 | `DISP:19` places item 15 at `SPEC:370` (wrong) | Recorded in `DISP2:41` (item 15 is at `SPEC:371` in V2 and `SPEC:377` in the live spec; verified). `DISP:19` itself still says `SPEC:370`. | partly | R3-10 |
| C-4 | `DISP:10` grep "returns nothing" (inaccurate) | `DISP2:12` states both greps; I re-ran them: the loose pattern hits only `SPEC:159` (`TodoWrite`), the word-boundary pattern prints nothing. `DISP:10` itself is unchanged. | partly | R3-10 |
| C-5 | `SPEC:12` "re-read 11 locations" (stale) | SPEC:13 "as of the Task 4 text (before the Task 6 and Task 8 revisions ...)". | resolved | none |
| C-6 | UNVERIFIED 14 "about 340 citations" (stale) | SPEC:376 "as of the Task 4 text only". | resolved | none |

Summary: of the 15 round-2 findings, 12 are resolved and 3 are partly resolved (N-05, N-14, N-15); none is open. Of the six round-2 blocking findings (N-01 to N-06), five are resolved and one (N-05) is partly resolved. Of the six overstated citations, four are resolved and two (C-3, C-4) are recorded but not corrected at their source. The residuals are carried into Part 3 as R3-01 to R3-10; R3-01 and R3-02 are new defects that sit on the premise the N-02 fix adopted.

Disposition accuracy (`DISP2` against the live spec): every backticked `SPEC:N` in `DISP2:15-45` that is not marked "(before)" points at the line it names (76 citations compared side by side with the live line; four of them, `SPEC:370`, `SPEC:371`, `SPEC:158` at `DISP2:41-42` and the matching old numbers, deliberately name V2 numbering and match V2); the 34 distinct "(before: N)" line numbers were compared with V2 and all match; the stated sizes (80732, 95578, +14846), the two greps, the "no `attempt-1` directory remains" claim and the "four new Decisions rows, three new UNVERIFIED items" claim all hold. One claim needs a qualifier: `DISP2:25` cites the Decisions row at `SPEC:354` for the retry bound, but that row is the malformed merged row of R3-06.

## Part 2: Citation check (citations the Task 8 revision added or changed)
Scope: the 82 citation tokens in the 23 changed lines that carry any (`diff V2 SPEC`), plus the self-citations of `DISP2`. "Live" here means the workspace file the citation names. Results: `ok` (the cited line says what the spec claims), `ok-quoted` (a `src/`, `~/.claude` or Orca path that matches the inventory line quoting it; the source itself is UNVERIFIED), `unverified` (no workspace line to compare), `partly` (the line supports less than is claimed), `wrong`.

| Spec line | Citation | Claim in the spec | Result |
|---|---|---|---|
| SPEC:12 | grep of `SPCMD` in the spec | `SPCMD` is "cited ... (sections 2.2, 9 and the UNVERIFIED list)" | **wrong**: it occurs at SPEC:12, SPEC:349 (Decisions), SPEC:381 (UNVERIFIED 19) and SPEC:423 (revision log); none in 2.2 (SPEC:57-74) or 9 (SPEC:306-335) |
| SPEC:13 | 11 `sk/`, `cmd/` and `.dev/` locations | re-read as of the Task 4 text | ok-quoted; now correctly dated |
| SPEC:64 | `CAPS:58-61`, `CAPS:64` | ask timeout leaves the question pending, resume by ID; no heartbeat while blocked in `ask` | ok |
| SPEC:65 | `CAPS:72-74`, `CAPS:79`, `CAPS:89` | `--report-path` only with real values; Orca's check of the file is UNVERIFIED; Orca Task status `blocked` | ok |
| SPEC:65 | `INV-B:262` | `/sc:explain` and the validate-tests skill have no shell tool | partly: `INV-B:262` covers the validate-tests skill only; explain's tools are at `INV-A:48` and SPEC:159; neither has Write today (the conversions add it, SPEC:159, SPEC:176) |
| SPEC:65 | `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`; `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` | workflow's contract is versioned 1.1; brainstorm writes a named contract | ok-quoted |
| SPEC:65, SPEC:383 | `CAPS:116` | whether the `worker-start` receipt carries the Dispatch ID | ok as labelled UNVERIFIED (`CAPS:116` shows only the retry command form) |
| SPEC:66 | `CAPS:73`, `CAPS:76-77` | outcome is `succeeded` or `failed`; one `worker_done` from the dispatched pane | ok |
| SPEC:67 | `CAPS:116`; column (e) of `INV-A:35-55`, `INV-B:31-52` | retry form; resume mechanisms | ok |
| SPEC:68 | `sk/sc-pr-submit-protocol/SKILL.md:37-39`; `CAPS:159-161`; `INV-A:95` | top-level rule; nesting loses tools at the depth limit | ok / ok-quoted (`INV-B:90`) |
| SPEC:71 | `CAPS:125-127` | absence never authorizes stop, abandon, retry or release | ok (`CAPS:125` says it) |
| SPEC:71 | `CAPS:130` | cadence comes from the preamble; use of heartbeat age is UNVERIFIED | ok |
| SPEC:71 | `cmd/pr-submit.md:49` | 600 s default budget | ok-quoted (`INV-B:95`, `INV-B:299`) |
| SPEC:71, SPEC:165 | `sk/sc-pr-submit-protocol/SKILL.md:46-64` | the 600 s is a cumulative budget of "one foreground poll, then a sleep of at least `--poll-interval`", "not one blocking call" | unverified, and stated as fact: `INV-B:95` says "waits up to `--timeout` 600 s per wait over several rounds" and `INV-B:299` cites `:41-64` for "poll loop, 600 s per wait"; no inventory records the poll-then-sleep structure. Only the poll script runtime is labelled UNVERIFIED (SPEC:374). Carried from V2 into the rewritten rows |
| SPEC:71 | `sk/sc-cli-eval-protocol/SKILL.md:151` via `INV-A:65` | an eval can run up to 3600 s | ok (range narrowed from `:151-152`; resolves C-2) |
| SPEC:74 | `INV-A:39`, `INV-B:119`, `INV-B:121`, `INV-B:219`, `INV-B:201`, `INV-B:91`, `INV-B:271`, `INV-B:211`, `INV-B:112`, `INV-A:60`, `INV-B:269` | the seven nesting chains; workflow's reflect runs with defaults and no `--remediate`; adversarial's contract was found in two places | ok (each line says what is claimed; `INV-B:121` is the adversarial leg of release-split, `INV-B:119` the brainstorm leg) |
| SPEC:74 | same list, read as complete | "Nests:" names the chains that exist | partly: it omits tasklist Stage 9 `sc:task --compliance strict` (`INV-B:46`, `INV-B:211`), cli-eval create to spec-panel and adversarial (`INV-A:44`), roadmap, reflect Tier 2 and troubleshoot Tier 2 to adversarial (`INV-B:151`, `INV-B:111`, `INV-B:241`) and pr-submit to the auggie-review fallback (`INV-B:91`); only the first matters for a same-phase gate (R3-04) |
| SPEC:85 | `CAPS:126`, `CAPS:125-127`, `CAPS:80`, `CAPS:116`, `CAPS:188` | positive-proof rule; breaker counts failed `worker-start` attempts, not a worker's own `failed` report; Dispatch run time unbounded is UNVERIFIED | ok (resolves C-1) |
| SPEC:165 | `INV-B:34,87-95`; `cmd/pr-submit.md:25,39,49,55-56`; `sk/sc-pr-submit-protocol/SKILL.md:37-39,66-68,141,170,189-197,237-246` | pr-submit row | ok-quoted (`INV-B:89-95`); `:46-64` as above |
| SPEC:173 | `INV-A:14`; `INV-B:210`, `INV-B:314`; `INV-B:46,207-215`; `sk/sc-tasklist-protocol/SKILL.md:92,1452,1614-1631`; `cmd/tasklist.md:39` | tasklist row | ok / ok-quoted (`INV-B:212`, `INV-B:209`, `INV-B:215`) |
| SPEC:198 | `CAPS:145-149`; E5 | SA-2 | ok |
| SPEC:211 | `INV-A:96`; `INV-B:292` | gate conversion is the main blocker class | ok |
| SPEC:240 | `pyproject.toml:38` | PyYAML is a declared dependency | unverified (not in the workspace; carried from V2) |
| SPEC:348 | `CAPS:130` | cadence 5 minutes, arithmetic of the 4-minute wait | ok; the arithmetic is right |
| SPEC:350 | `CAPS:116` | "a retry ... reuses the Task's text and carries no replacement" | partly: `CAPS:116` quotes the retry command without a text argument; it does not say none is accepted. SPEC:65 and SPEC:383 label this UNVERIFIED, but the Decisions row states it as fact |
| SPEC:350 | `CAPS:76`, `CAPS:150` | the Dispatch ID "is in the worker's preamble" | **overstated**: `CAPS:76` and `CAPS:150` say a `worker_done` with the active task and dispatch IDs completes only from the dispatched pane and that injected preambles carry the right `--from`; the line that says the preamble carries Task and Dispatch IDs is `CAPS:148` (and `CAPS:151` shows a `dispatchId` read through `check`) |
| SPEC:351, SPEC:352, SPEC:353, SPEC:354 | `INV-B:211`; `INV-B:271`; `INV-B:242`, `INV-B:272`; `CAPS:80` | tasklist N reflects; workflow always runs reflect; troubleshoot and workflow contracts; breaker | ok |
| SPEC:384 | `INV-A:35`, `INV-B:221` | foreground Agent-tool call dispatched "in one message" | partly: `INV-A:35` says one message (`S:1048-1054`); `INV-B:221` gives agent counts, not the dispatch form. Labelled UNVERIFIED, so no harm |
| SPEC:385 | `INV-A:39` | brainstorm Wave 4 is optional | ok |
| SPEC:419 | `CAPS:116` | revision-log row | ok |
| SPEC:223, SPEC:229-233 | AC-C1 pattern | matches `orca-ide orchestration ...`, `ORCA worktree ...`, `orca open`, and the prose "the orca status line" | ok (I ran the pattern on sample lines; it does not match "Orca terminals") |
| `DISP2:15-45` | `SPEC:N` and "(before: N)" | where each fix landed | ok (see the Part 1 closing paragraph) |
| `DISP2:41` | `SPEC:377` | item 15 of the UNVERIFIED list | ok (live line 377 is item 15) |
| `DISP:10`, `DISP:19` | `SPEC:158`, `SPEC:370` and "returns nothing" | the Task 6 record | **still wrong at the source** (`DISP2:55`): the claims are corrected only in `DISP2` (R3-10) |

Wrong or overstated: SPEC:12 (where `SPCMD` is cited), SPEC:350 (`CAPS:76`, `CAPS:150`). Partly supported: SPEC:65 (`INV-B:262` for explain), SPEC:74 (list read as complete), SPEC:350 (`CAPS:116`), SPEC:384 (`INV-B:221`). Unverified and stated as fact: SPEC:71 and SPEC:165 (`SKILL.md:46-64`). Not re-readable: 23 of the 82 tokens are `src/`, `~/.claude`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration` or `pyproject.toml` paths (59 are `INV-A`, `INV-B` or `CAPS` lines, all re-read); the 23 are `ok-quoted` or `unverified` only. No wrong `INV-A`, `INV-B` or `CAPS` line number was found among the added or changed citations.

## Part 3: /sc:spec-panel critique (requirements, architecture)
```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  mode: critique
  focus_areas: [requirements, architecture]
  expert_panel: [Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Whittaker, Newman, Hohpe, Crispin (guard-table completeness)]
  review: 1 of 3
quality_assessment:
  overall_score: 7.0
  clarity: 7.5
  completeness: 7
  testability: 6.5
  consistency: 6.5
critical_issues:
  - {id: R3-01, severity: CRITICAL, expert: Fowler, issue: "N-02's fix makes a retry reuse the Task text unchanged, so WC-6's promise (resume, or a fresh output) cannot be delivered for --output paths and resume values; only --report-dir varies per attempt", recommendation: "give the worker an output base the same way as the report base, and say who adds a resume flag on a retry and from where; extend AC-2.7 to check the deliverable"}
  - {id: R3-02, severity: MAJOR, expert: Nygard, issue: "A blocked outcome settles failed; the one automatic retry repeats the gate and the person's answer has no way into a retry that keeps the Task text", recommendation: "no automatic retry on blocked; name the channel that carries the answer"}
  - {id: R3-03, severity: MAJOR, expert: Newman, issue: "The pre-conversion outcome rule needs a named report file; adversarial (and workflow's package id) has none, so AC-0.4 cannot be run as written", recommendation: "name the candidate paths in the P0 brief or pick a smoke command whose file is fixed"}
  - {id: R3-04, severity: MAJOR, expert: Hohpe, issue: "tasklist Stage 9 calls sc:task, a P2 command with gates, and neither WC-13's chain list nor the tasklist row names it", recommendation: "add the leg to the row, the Nested: line and AC-2.1"}
expert_consensus:
  - "The Task 8 revision closed 12 of 15 round-2 findings outright and 3 partly; the report-base plus Dispatch-ID rule, the interim nesting rule and the scoped WC-10 cap read correctly."
  - "The new defects sit where the revision's single new premise (a retry reuses the Task text unchanged) meets older rules: WC-6 resume and fresh output, the blocked outcome, and the answer path."
  - "Counts and cross-references reconcile: 43 = 10 + 27 + 6; phases name 15 + 15 + 4 + 3 = 37; the 41 hunks of the diff land where DISP2 says."
improvement_roadmap:
  immediate: [R3-01, R3-02, R3-03, R3-04]
  short_term: [R3-05]
  long_term: [R3-06, R3-07, R3-08, R3-09, R3-10]
adversarial_analysis: "see === ADVERSARIAL ANALYSIS (Whittaker) ==="
```

### Panel and method
Review order followed `SPCMD:101-113` for the experts active under `--focus requirements,architecture` (`SPCMD:131-148`) plus Whittaker (`SPCMD:84`) and Crispin for guard-table completeness (`SPCMD:311`). The whole document was reviewed; `origin=` records where each finding sits. Grading follows `SPCMD:259`: CRITICAL and FR-8/FR-9 findings block; a MAJOR blocks only when it names a concrete wrong outcome; MINOR is a note. `--focus correctness` is not active, so no State Variable Registry (`SPCMD:186-188`). The Guard Condition Boundary Table and the Quantity Flow Diagram are produced because the spec has flag, threshold and count guards and a multi-stage count-changing flow, and both are complete before the synthesis (FR-10, `SPCMD:330`).

### Mandatory output artifacts

#### Guard Condition Boundary Table
Guards are the ones whose value or flag state decides behaviour in the Task 8 text: G1 `--report-dir` rules (WC-4, SPEC:65), G2 report validity and the pre-conversion split (WC-5, SPEC:66), G3 nested-child eligibility and the `k` index (WC-13, SPEC:74), G4 wait cap and heartbeat (WC-10, SPEC:71), G5 retry and re-run of a command (WC-6, SPEC:67, SPEC:80, SPEC:264), G6 blocked gate and answer path (WC-3, SPEC:64, SPEC:85, SPEC:87). Construction Nygard, completeness Crispin, attack Whittaker. Every cell is populated.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 `--report-dir` composed, created, outside `.git/` | SPEC:65 | Zero/Empty | `--unattended`, no `--report-dir`, brief without a base | false | Stops before work, writes no file; worker settles `failed` (AC-2.7) | OK |
| G1 | SPEC:65 | One/Minimal | existing empty directory | true | Contract written there | OK |
| G1 | SPEC:65, SPEC:80 | Typical | new `<base>/<dispatch_id>/` | true | Contract written | OK |
| G1 | SPEC:65 | Maximum/Overflow | the 3rd attempt of one Task (3 Dispatch IDs) | true | Three distinct directories; no overwrite | OK |
| G1 | SPEC:65, SPEC:66, SPEC:199 | Sentinel Value Match | `--report-dir` given with no `--unattended` | unknown | WC-4 writes the contract "in unattended mode"; SA-3 writes it "when the caller passes `--report-dir`"; WC-5 treats the worker as a `--report-dir` worker | GAP |
| G1 | SPEC:65 | Legitimate Edge Case | directory already holds a contract (WC-3 re-invocation) | true | Overwritten; coordinator reads only its own Dispatch directory | OK |
| G2 report valid (exists, non-empty, YAML, `command`, status in four) for `--report-dir` workers | SPEC:66 | Zero/Empty | 0-byte `return-contract.yaml` | false | No report; `--outcome failed` | OK |
| G2 | SPEC:66 | One/Minimal | YAML with only `command` and `status: succeeded` | true | Valid; succeeded | OK |
| G2 | SPEC:66 | Typical | converted command, `status: succeeded` | true | succeeded | OK |
| G2 | SPEC:66, SPEC:87 | Maximum/Overflow | `partial` with a long `skipped` list | true | succeeded; coordinator reads `skipped` first | OK |
| G2 | SPEC:66, SPEC:79, SPEC:134, SPEC:253, INV-A:60 | Sentinel Value Match | pre-conversion adversarial smoke run: "named file" = "contract, but filename not fixed" | undefined | The brief must name the file (SPEC:79) and AC-0.4 step 4 runs `test -s` on it; two layouts exist (`INV-A:60`) | GAP |
| G2 | SPEC:66 | Legitimate Edge Case | audit with verdict FAIL | true | succeeded; body names the verdict | OK |
| G3 child eligible when its phase has passed; dir `<child>-<k>` | SPEC:74 | Zero/Empty | parent invokes no child | n/a | `Nested:` says none | OK |
| G3 | SPEC:74, SPEC:255 | One/Minimal | workflow (P1) to reflect (P2) | false | Interim rule: present flags, no flag passed (AC-1.2) | OK |
| G3 | SPEC:74 | Typical | brainstorm to adversarial (both P1) | true | `--unattended` and `adversarial-1/` | OK |
| G3 | SPEC:74, SPEC:173, SPEC:258, SPEC:266, INV-B:46, INV-B:211 | Maximum/Overflow | tasklist with N phases: N reflects plus the Stage 9 `sc:task` leg | N + 1 children | `reflect-<k>` named; the `sc:task` leg is in no row, no `Nested:` example and no AC | GAP |
| G3 | SPEC:74 | Sentinel Value Match | child is a skill outside the 43 (`task`, `task-builder`, `tech-research`) | false | Outside the pass-through; parent's section says how asks resolve | OK |
| G3 | SPEC:74 | Legitimate Edge Case | same child twice in parallel | true | `k` differs, directories differ | OK |
| G4 wait calls at most 240 s; heartbeat before each wait over 60 s | SPEC:71 | Zero/Empty | wait of 0 s | false | Nothing to split | OK |
| G4 | SPEC:71 | One/Minimal | one 60 s wait | false | No heartbeat needed (not longer than 1 minute) | OK |
| G4 | SPEC:71 | Typical | 3 min poll after a heartbeat | true | Allowed | OK |
| G4 | SPEC:71 | Maximum/Overflow | 241 s wait | true | Split into waits of at most 240 s | OK |
| G4 | SPEC:71, SPEC:384 | Sentinel Value Match | 9 min foreground Agent-tool fan-out (tdd research wave) | exempt | No heartbeat possible; coordinator does not read it as a stall; UNVERIFIED stated | OK |
| G4 | SPEC:71, SPEC:265 | Legitimate Edge Case | Monitor-watched eval | true | Bounded waits, heartbeats between; AC-2.8 observes | OK |
| G5 retry reuses the Task text; only `--report-dir` varies | SPEC:67, SPEC:80, SPEC:264 | Zero/Empty | first attempt (no retry) | n/a | Normal run | OK |
| G5 | SPEC:67 | One/Minimal | one retry of a command with a timestamped default output directory | true | Fresh directory | OK |
| G5 | SPEC:67, SPEC:102, SPEC:134, SPEC:141, SPEC:264 | Typical | retry of a command whose brief fixes `--output` (adversarial, tdd, analyze) | true | Same `--output` as attempt 1; AC-2.7 checks only the contract hash | GAP |
| G5 | SPEC:67, SPEC:135, SPEC:140, SPEC:141, SPEC:156, SPEC:165 | Maximum/Overflow | retry of a command whose resume flag needs a path that exists only after attempt 1 | true | The Task text written before attempt 1 cannot name it; nothing lets the worker add it | GAP |
| G5 | SPEC:85, CAPS:80 | Sentinel Value Match | a second reported failure of the same Task | true | Goes to the person with both reports | OK |
| G5 | SPEC:85, CAPS:116 | Legitimate Edge Case | `worker-start` fails before the agent is ready, three times | true | Orca's breaker counts it; do not route around | OK |
| G6 blocked gate settles `failed`; answer by flag or `--answer` | SPEC:64, SPEC:66 | Zero/Empty | `answer_wait: 0` | true | Blocked at once; `failed` (AC-2.2) | OK |
| G6 | SPEC:64 | One/Minimal | one gate answered inside `answer_wait` | true | Re-invoked with the answer, contract overwritten | OK |
| G6 | SPEC:85, SPEC:87, CAPS:90 | Typical | `answer_wait` expires; the person answers later | true | Not specified: the retry keeps the Task text, the dependents stay blocked | GAP |
| G6 | SPEC:64 | Maximum/Overflow | cli-portify, three gates, one total `answer_wait` | true | Once per gate; total wait bounded | OK |
| G6 | SPEC:64 | Sentinel Value Match | answer text containing `=` | true | Split at the first `=` | OK |
| G6 | SPEC:64 | Legitimate Edge Case | unknown or repeated gate id | true | Usage error; `failed` with the reason | OK |

GAP rows and where they are folded: G1 row 5 into R3-05; G2 row 5 into R3-03; G3 row 4 into R3-04; G5 rows 3 and 4 into R3-01; G6 row 3 into R3-02. By FR-8 each is at least MAJOR; R3-05 is kept non-blocking because both readings are inferrable and the harm is bounded (see its entry).

#### Quantity Flow Diagram (FR-17 to FR-21)
Triggered: classification and phase assignment are a multi-stage flow whose counts change, and the retry and nesting rules multiply directories. Fowler annotated counts, Whittaker attacked the divergence points.

```text
[Source: 43 commands in cmd/ (SPEC:127)]
   --> [Stage 1: classify]
        --> [6 coordinator-only (SPEC:179)]                       excluded
        --> [37 worker-capable = 10 ready (3.1) + 27 change (3.2)]
              --> [Stage 2: phase (SPEC:210-213)]
                    P1 = 14 flag-accepting + load (usage line) = 15 ; P2 = 15 ; P3 = 4 ; P4 = 3 ; total 37   OK
                    flag-accepting commands when P1 ends = 14 ; WC-13 asks the flag only of converted children   OK
[Source: 1 Task text (SPEC:237)] --> [Stage 3: attempts, A >= 1 (SPEC:80, SPEC:264)]
        --> [A Dispatch IDs --> A report directories <base>/<dispatch_id>/]     OK (WC-4)
        --> [Consumer WC-6: needs A fresh output directories, or a resume flag]
              --> [1 deliverable path in the Task text (SPEC:102,134,141); 0 resume values]   <-- MISMATCH (R3-01)
[Source: tasklist run] --> [Stage 4: children]
        --> [N reflects, one per phase: reflect-1 .. reflect-N (SPEC:173, SPEC:266)]  OK
        --> [1 sc:task --compliance strict at Stage 9 (INV-B:211)]                      <-- not in any row (R3-04)
```

Divergence at Stage 3: A attempts give A report directories but one deliverable path and no resume value. Concrete scenario (FR-19): attempt 1 of `/sc:adversarial --output D` writes 3 of 6 artifacts under `D/adversarial/` and dies; the retry gets the same text, so the same `D`; adversarial has no resume outside pipeline mode (SPEC:134), so attempt 2 writes into the same directory and WC-6's "must not corrupt the first attempt's output" fails while AC-2.7 (hash of the first contract only) passes. Graded CRITICAL under FR-19, the same convention the round-2 panel used for N-01. Stage 4 is a missing leg, not a collapse: N reflect directories are specified; the (N+1)th child is not.

### Findings by analysis bucket
Each finding gives issue, severity, expert, recommendation with rationale, priority and quality impact. `origin=` is `changed` when the text it quotes was touched by the Task 8 revision.

=== REQUIREMENTS ANALYSIS ===

**R3-02 (MAJOR, blocking; FR-8 from guard G6; origin=changed). Nygard / Wiegers: a blocked gate has no way back in.**
- Issue: a `blocked` contract maps to `worker_done --outcome failed` (SPEC:66; AC-2.2, AC-2.6 at SPEC:259, SPEC:263). SPEC:85 then says that "after a reported failure the coordinator bounds the retries itself: one retry on its own, and a second reported failure of the same Task goes to the person with both reports". A blocked report is a reported failure, yet its remedy is an answer, which travels as a flag or `--answer` in the command line (SPEC:64), and a retry keeps the Task text unchanged (SPEC:80, SPEC:264, SPEC:350). Orca keeps the dependents of a failed Task blocked until a `--retry-of` replacement completes it (`CAPS:90`), and forbids routing around the three-failure boundary with a new Task (`CAPS:116`; whether a new Task is allowed after one failure is not in `CAPS`). Coordinator follow-ups to a running worker are pull-only (`CAPS:66`) and WC-12 (SPEC:73) mentions no answer on that path. SPEC:87 hands the `blocked_question` to the person and stops there.
- Wrong outcome: `/sc:tdd "auth" --unattended` blocks on the topic; `answer_wait` ends; Task T is `failed` and its dependent D stays blocked. By SPEC:85 the coordinator retries once on its own: same text, same gate, blocked again, count 2, and only now the person sees the question. The person answers "the login API" and nothing in the spec says how that reaches a command: the retry cannot carry it, and D waits for T. An implementer either invents a channel per project or loops the retry.
- Recommendation: state that a `blocked` report is not retried automatically but goes to the person first; name the channel that carries the answer to the next attempt (a `send --to dispatch:<id>` message the retry worker reads at its first `check` and passes as `--answer`, or a replacement Task whose text carries the answer, with the Orca rule marked UNVERIFIED); extend AC-2.6's second run so it ends with the answer delivered and D unblocked. Rationale: the revision's one new premise (unchanged Task text on retry) removed the only place an answer could have been written.
- Priority: High. Quality impact: Completeness +1, Testability +1.

**R3-03 (MAJOR, blocking; FR-8 from guard G2; origin=changed). Newman / Adzic: the pre-conversion outcome rule needs a file the P0 smoke runs cannot name.**
- Issue: before conversion the report is "the command's own named file (section 3.1 column 'Report today')" (SPEC:66); the brief "also names the command's report file for `--report-path`" (SPEC:79); AC-0.4 step 4 is `test -s` on that file (SPEC:253, SPEC:240). For adversarial the column says "contract, but filename not fixed" (SPEC:134), and `INV-A:60` records two layouts in the earlier run (`.../adversarial/return-contract.yaml` and `.../adversarial/adversarial/return-contract.yaml`); the small fix that names one arrives in P1 and P0 allows no command edit (SPEC:209). For workflow the file sits in `.dev/tasks/to-do/<id>/` with `<id>` created at run time (SPEC:143). The worked brief (SPEC:92-98) escapes by "the REPORT.md path the command prints", which is stated only for troubleshoot.
- Wrong outcome: in AC-0.4 the coordinator cannot write the adversarial `--report-path` into the brief; the worker picks one of two layouts or none; step 4 passes or fails by luck, and a failure "reopens section 1" (SPEC:253). The decision test of Phase 0 can fail for a reason that is not about the decision.
- Recommendation: give the P0 brief template a rule for runtime-named files (the worker locates the file by the candidate paths the brief lists, and says which it used in the `worker_done` body), list both adversarial candidates, and add the adversarial filename fix as the single pre-smoke edit, or replace the third smoke command by one whose file is fixed (init-lite, SPEC:138).
- Priority: High. Quality impact: Testability +2.

**R3-05 (MAJOR, not blocking; origin=changed). Wiegers / Crispin: the `--unattended` by `--report-dir` matrix is only half defined.**
- Issue: WC-4 writes the contract "in unattended mode" and refuses `--unattended` without `--report-dir` (SPEC:65); WC-5 applies its validity rule to "a worker started with `--report-dir`" and its pre-conversion rule to "a worker run without `--unattended` and `--report-dir`" (SPEC:66); SA-3 writes the contract "only in unattended mode or when the caller passes `--report-dir`" (SPEC:199); AC-1.3 tests neither flag alone (SPEC:256). The four cells: (no, no) is covered; (yes, yes) is covered; (yes, no) is the WC-4 refusal, and its `failed` outcome rests on WC-5's closing "no valid report exists" because neither named branch describes that worker; (no, yes) is undefined: SA-3 says a contract is written, WC-4 says it is not.
- Wrong outcome: two implementers differ on whether `/sc:analyze x --report-dir d` (no `--unattended`) writes `d/return-contract.yaml`, and no check catches it. Harm is bounded (a person-run command either writes one extra file or does not), so not blocking.
- Recommendation: one sentence in WC-4: `--report-dir` alone is accepted and writes the contract with the standalone behaviour otherwise unchanged (or is a usage error), and name the (yes, no) worker as covered by WC-5's last sentence; add the matrix to AC-1.3.
- Priority: Medium. Quality impact: Consistency +1, Testability +1.

**R3-09 (MINOR; origin=unchanged). Wiegers: "refused" has no terminal status.** Eight rows say a flag or keyword is "refused" under `--unattended` (`--mode socratic` SPEC:153, `--interactive` SPEC:154, SPEC:161, SPEC:169, `--format interactive` SPEC:159, `--monitor 1` SPEC:165, `--watch` SPEC:174, `commit`/`push` SPEC:172, WC-9 SPEC:70). The spec defines `failed` for a usage error (conflicting grant flags SPEC:70, unknown `--answer` id SPEC:64) and `blocked` for a gate that waits on an answer (WC-2 (c), SPEC:63), but not which a refusal is; AC-2.4 expects `blocked` for the task case only (SPEC:261). One sentence in section 3's intro fixes it. Priority Low.

=== ARCHITECTURE ANALYSIS ===

**R3-01 (CRITICAL, blocking; FR-19 dimensional mismatch and FR-8 from guard G5; origin=changed). Fowler / Nygard: WC-6 cannot be delivered when a retry keeps the Task text.**
- Issue: the N-02 fix works because a retry is a new Dispatch with the same Task text and a new `<dispatch_id>` directory (SPEC:65, SPEC:80, SPEC:264, SPEC:350). WC-6 (SPEC:67) still requires that a retry "must not corrupt the first attempt's output": a command "resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean". Both alternatives need text that differs per attempt, and only `--report-dir` gets it. (1) Deliverable paths in the brief are fixed for every attempt: `--output .dev/orca-runs/analyze-1/analysis.md` (SPEC:102; analyze's resume cell is "fresh dir", SPEC:150), tdd (SPEC:120, SPEC:141), adversarial "Brief must pass `--output <dir>`" with "else fresh dir" (SPEC:134), init-lite (SPEC:138). (2) Resume flags take a value that exists only after attempt 1: `--resume-from <seed-brief>` (SPEC:135), `--resume-from <split-proposal-final.md>` (SPEC:140), `--resume <task-file>` (SPEC:141), `--resume <contract>` (SPEC:156), `--resume <run-log.jsonl>` (SPEC:165). A Task text written before attempt 1 cannot name them, and nothing in 2.3 or WC-4 lets the worker learn it is a retry or add a flag. AC-2.7 checks only the hash of the first contract (SPEC:264), so it passes while WC-6 is broken. `R2`'s N-02 (`R2:232-236`) was about the report directory; the same premise reaches the deliverable and the resume value.
- Wrong outcome: see the Quantity Flow Diagram. Attempt 1 of `/sc:adversarial --compare a b --depth quick --output D --unattended` writes 3 of 6 artifacts under `D/adversarial/` and dies; attempt 2 is started with `--retry-of`, gets the same `D`, has no resume outside pipeline mode, and writes into the same directory: stale and new artifacts mix, or attempt 1's evidence is overwritten. For tdd, attempt 2 restarts the whole research wave instead of `--resume <task-file>`.
- Recommendation: extend the report-base rule to deliverables: the brief carries an output base and the worker passes `<output base>/<dispatch_id>/` (or says that WC-6 holds only for commands whose output default is timestamped and the brief omits `--output`); state who adds a resume flag on a retry and from where (for example the worker reads the previous attempt's contract `artifacts` and `report_path`, once the coordinator tells it, in the brief or by a follow-up message, that this is a retry); extend AC-2.7 to assert that the first attempt's deliverables are unchanged. Mark the Orca side UNVERIFIED until AC-2.7 runs.
- Priority: High. Quality impact: Consistency +2, Testability +2.

**R3-04 (MAJOR, blocking; FR-8 from guard G3; origin=changed). Hohpe / Fowler: tasklist's second child is missing from WC-13, its row and its checks.**
- Issue: tasklist Stage 9 patches "via `sc:task --compliance strict`" and Stage 10.5 spawns N reflects (`INV-B:211`; "Stage 9 `sc:task`, N reflects", `INV-B:46`). `/sc:task` is a P2 command with gates: confidence below 0.70, TFEP "present to user" and FULL STOP, EXEMPT `commit`/`push` (SPEC:172). Tasklist is P2, so by WC-13 the child's phase has passed and tasklist must pass `--unattended` and `<report-dir>/task-<k>/` to it. WC-13's chain list (SPEC:74, "Nests: ... tasklist to N reflects") names only the reflect leg, the tasklist row names only `reflect-<k>` (SPEC:173), and AC-2.1 and AC-2.9 test only the reflect directories (SPEC:258, SPEC:266).
- Wrong outcome: an implementer who follows the row converts Stage 10.5 and leaves Stage 9's `sc:task` without the flag; a TFEP or low-confidence gate then opens inside an unattended worker and the worker stalls without `worker_done`, which is the failure WC-2 exists to prevent. AC-2.9 passes because it counts reflect directories.
- Recommendation: add the Stage 9 leg to the tasklist row (`task-<k>` with `k` the patch round or invocation index), to the `Nested:` line example, and assert it in AC-2.1 and AC-2.9; re-read the other rows for the same omission (the chains missing from the list in Part 2: cli-eval create, roadmap, reflect Tier 2, troubleshoot Tier 2, pr-submit's auggie-review fallback are same-phase or earlier children and fall under the generic rule).
- Priority: High. Quality impact: Completeness +1, Testability +1.

**R3-08 (MINOR; origin=unchanged text contradicted by a changed line). Fowler: R3 in section 1.3 is now false for converted commands.** SPEC:37 says "the Task and Dispatch IDs exist only in the preamble given to the worker session, not in the command's arguments". The Task 8 design puts the Dispatch ID into the command's arguments (`--report-dir <report base>/<dispatch_id>/`, SPEC:65, SPEC:80, SPEC:102). The rejection reason (a command cannot own `worker_done`) still stands because the ID in a path gives a command no way to send; the sentence should say "the Orca message identifiers" or qualify it. Priority Low.

=== CROSS-CUTTING (editorial and record) ===

**R3-06 (MINOR; origin=changed). Technical-writer pass: two Decisions rows are merged into one line.** SPEC:354 ends "... can be raised in the brief. || Answer channel for gates with no flag | Name a flag per gate; ..." with eight pipe characters where the table has four columns (checked for every table in the spec: this is the only row off). A renderer drops the cells past the fourth, so the decision that justifies `--answer` (WC-3) disappears from the rendered table, and `DISP2:25` cites that row for the retry bound only. Split the line into two rows. Priority Low.

**R3-07 (MINOR; origin=changed). Wiegers: four citations added or changed by the revision say more than their source.** (a) SPEC:12 says `SPCMD` is cited in "sections 2.2, 9 and the UNVERIFIED list"; it is cited in the Decisions table, the UNVERIFIED list and the revision log (SPEC:349, SPEC:381, SPEC:423). (b) SPEC:350 cites `CAPS:76` and `CAPS:150` for "the Dispatch ID is in the worker's preamble"; `CAPS:148` says it, `CAPS:76` and `CAPS:150` do not. (c) SPEC:350 states as fact that a retry "carries no replacement" text (`CAPS:116` quotes a command form without a text argument and does not say none is accepted), while SPEC:65 and SPEC:383 label it UNVERIFIED. (d) SPEC:71 and SPEC:165 state pr-submit's 600 s as "a cumulative per-wait budget of poll-then-sleep iterations, not one blocking call" citing `SKILL.md:46-64`; the inventories say "waits up to `--timeout` 600 s per wait" (`INV-B:95`, `INV-B:299`), so only the claim "per wait" is supported. Also SPEC:65 cites `INV-B:262` for `/sc:explain` as well as for the validate-tests skill; it covers the skill only (explain: `INV-A:48`). Correct the cite, soften (c) and (d) to match their UNVERIFIED labels. Priority Low.

**R3-10 (MINOR; origin=changed). Wiegers: the Task 6 disposition keeps the claims `DISP2` corrects.** `DISP:10` still says the placeholder grep "returns nothing" (it returns `SPEC:159`, `TodoWrite`) and `DISP:19` still places UNVERIFIED item 15 at `SPEC:370` (item 8 in the live spec, item 14 in V2; item 15 is `SPEC:377`). Its other 25 lines with `SPEC:N` citations point at V2 numbering (the spec grew by 14846 bytes), and `DISP:5` says "AFTER the revision" without naming V2. `DISP2:41` and `DISP2:55` record this; the source files were left alone because of the ownership rule. Add one line at the top of `DISP` naming `history/spec-v2.md` as its numbering base and correct the two claims. Priority Low.

=== ADVERSARIAL ANALYSIS (James Whittaker) ===
Severity classes: CRITICAL (provably wrong), MAJOR (ambiguous or incomplete under attack), MINOR (inferrable). Each attack is tied to a finding.

**A-1 (R3-01, CRITICAL). I can break this specification by a Sequence attack on retry.** The invariant at **SPEC:67 (WC-6) and SPEC:264 (AC-2.7)** fails when **the retry reuses the Task text and the command needs a per-attempt output path or resume value**. Concrete attack: **state 0: Task T text holds `--output D --report-dir <base>/<dispatch_id>/`; attempt 1 (ctx_1) leaves `D/adversarial/` with 3 of 6 artifacts and `status: failed` in `<base>/ctx_1/`. Step 1: `worker-start --task T --retry-of ctx_1`. State 1: attempt 2 (ctx_2) composes `<base>/ctx_2/` but receives the same `D`. State 2: adversarial (no resume outside pipeline mode) writes into `D/adversarial/`; the first attempt's artifacts are overwritten or mixed; AC-2.7 compares only `<base>/ctx_1/return-contract.yaml`, whose hash is unchanged, and passes.** Recommendation: see R3-01.

**A-2 (R3-02, MAJOR). I can break this specification by a Sequence attack on blocked then answered.** The invariant at **SPEC:85 and SPEC:87** fails when **a blocked report is treated as a failure to retry**. Concrete attack: **state 0: tdd "auth" blocks, `answer_wait` 15 min expires, T `failed`, dependent D blocked (`CAPS:90`). Step 1: coordinator retries once on its own (SPEC:85): same text, blocked again, count 2. Step 2: the person answers; no step in the spec carries the answer to a command (text unchanged, follow-ups pull-only, `CAPS:66`). State 2: T stays failed, D stays blocked.** Recommendation: see R3-02.

**A-3 (R3-03, MAJOR). I can break this specification by a Sentinel Collision attack on "named file".** The invariant at **SPEC:66, SPEC:79 and SPEC:253** fails when **the report column holds a description instead of a path**. Concrete attack: **AC-0.4 on `/sc:adversarial --compare a b --depth quick --output D`: the column says "contract, but filename not fixed" (SPEC:134); the brief names no `--report-path`; the worker finds `D/adversarial/adversarial/return-contract.yaml` (one of the two layouts in `INV-A:60`) or `D/adversarial/return-contract.yaml`; step 4 `test -s` is run on whichever the coordinator guessed; a miss reads as a failed smoke run and "reopens section 1".** Recommendation: see R3-03.

**A-4 (R3-04, MAJOR). I can break this specification by an Accumulation attack on the child count.** The invariant at **SPEC:74 and SPEC:173** fails when **a parent has more than one kind of child**. Concrete attack: **tasklist on a 3-phase roadmap: Stage 9 runs `sc:task --compliance strict` once (no flag, row silent), Stage 10.5 runs reflect 3 times (`reflect-1` to `reflect-3`); AC-2.9 sees 3 directories and passes; the `sc:task` run reaches a confidence gate below 0.70 (SPEC:172) and waits on a person nobody is watching.** Recommendation: see R3-04.

**A-5 (R3-05, MAJOR). I can break this specification by a Zero/Empty attack on the flag pair.** The invariant at **SPEC:65 against SPEC:199** fails when **`--report-dir` is present and `--unattended` is absent**. Concrete attack: **`/sc:analyze x --report-dir d` in a person's session: WC-4 (trigger "in unattended mode") writes nothing; SA-3 ("or when the caller passes `--report-dir`") says write `d/return-contract.yaml`; AC-1.3 runs with neither flag and passes both ways.** Recommendation: see R3-05.

**A-6 (R3-09, MINOR). I can break this specification by a Divergence attack on "refused".** The invariant at **SPEC:70 against SPEC:261** fails when **a refusal sits on the boundary between a usage error and a gate**. Concrete attack: **`/sc:task "push the fix" --unattended --report-dir d`: WC-9 says refused, WC-2 (c) would call it blocked, WC-9's conflict rule would call it failed; AC-2.4 asserts blocked; a second implementer writes failed and the check fails on correct behaviour.** Recommendation: see R3-09.

### Synthesis
Consensus points
- The Task 8 revision is sound where it meets round 2 head on: the report base plus Dispatch ID, the interim nesting rule, the scoped validity rule, the scoped wait cap, the AC fixes and the baseline check all do what the findings asked, and the counts and cross-references reconcile.
- The four blocking defects share one origin: the revision made "a retry reuses the Task text unchanged" an explicit premise (SPEC:80, SPEC:264) and applied it to one field. Output paths, resume values and answers are the other per-attempt inputs (R3-01, R3-02); the pre-conversion rule and the second nested child (R3-03, R3-04) are the places where the new scoping rules were written against the examples at hand (troubleshoot, reflect) rather than the whole table.
- The coordinator side (2.3) is again the part that carries the most new rules and the one that is least checked: no AC drives a blocked outcome through to an answer.

Disagreements
- Nygard and Wiegers wanted R3-05 blocking under FR-8 (a flag combination with two readings); Crispin and Hohpe held it at MAJOR because both readings are inferrable and the harm is one extra file. Left non-blocking under `SPCMD:259`.
- Hohpe would grade R3-04 MINOR because WC-13's generic rule covers the child; Fowler and Whittaker hold MAJOR blocking because the row, the chain list and both ACs are the sources an implementer follows and all three are silent. Left blocking.
- Wiegers asked for R3-08 and R3-09 to be MAJOR under FR-9 (no stated behaviour); the panel graded them MINOR because the intended reading is inferrable from nearby text.

Priority-ranked improvements: R3-01, R3-02 (they change what a retry may carry, so R3-03 and R3-04 are written against them), then R3-03, R3-04, R3-05, then the minor items.

### Numbered new findings
10 new findings: 1 CRITICAL, 4 MAJOR (R3-02 to R3-05), 5 MINOR (R3-06 to R3-10) in the experts' labels; 4 blocking (R3-01 to R3-04), 6 not blocking. Evidence paths are relative to the workspace root.

| # | Finding | Severity | Blocking | Origin | Spec section | Evidence (path:line) |
|---|---------|----------|----------|--------|--------------|----------------------|
| R3-01 | A retry keeps the Task text, so WC-6's resume or fresh output cannot be delivered for fixed `--output` paths and resume values; AC-2.7 checks only the contract hash (FR-19, guard G5) | CRITICAL | yes | changed | 2.2 WC-6, WC-4; 2.3 item 3; 3.1, 3.2 rows; 7.3 AC-2.7 | SPEC:67, SPEC:65, SPEC:80, SPEC:102, SPEC:120, SPEC:134-141, SPEC:156, SPEC:165, SPEC:264, SPEC:350 |
| R3-02 | A `blocked` outcome settles `failed`, the one automatic retry repeats the gate, and the person's answer has no path into a retry (guard G6) | MAJOR | yes | changed | 2.2 WC-3, WC-5; 2.3; 7.3 AC-2.6 | SPEC:64, SPEC:66, SPEC:85, SPEC:87, SPEC:263, SPEC:264; CAPS:66, CAPS:90, CAPS:116 |
| R3-03 | The pre-conversion outcome rule needs a named report file; adversarial (and workflow's `<id>`) has none, so AC-0.4 cannot be run as written (guard G2) | MAJOR | yes | changed | 2.2 WC-5; 2.3 item 2; 2.4; 6 P0; 7.3 AC-0.4 | SPEC:66, SPEC:79, SPEC:92-98, SPEC:134, SPEC:143, SPEC:209, SPEC:253; INV-A:60 |
| R3-04 | tasklist Stage 9 `sc:task` is a P2 child with gates and is in no chain list, row, `Nested:` example or AC (guard G3) | MAJOR | yes | changed | 2.2 WC-13; 3.2 tasklist and task rows; 7.3 AC-2.1, AC-2.9 | SPEC:74, SPEC:172, SPEC:173, SPEC:258, SPEC:266; INV-B:46, INV-B:211 |
| R3-05 | The `--unattended` by `--report-dir` matrix is half defined: WC-4 and SA-3 disagree on `--report-dir` alone and WC-5's branches skip (yes, no) (guard G1) | MAJOR | no | changed | 2.2 WC-4, WC-5; 5 SA-3; 7.3 AC-1.3 | SPEC:65, SPEC:66, SPEC:199, SPEC:256 |
| R3-06 | Two Decisions rows are merged on one line (8 pipes in a 4-column table) | MINOR | no | changed | Decisions | SPEC:354 |
| R3-07 | Citations added or changed by the revision say more than their source (`SPCMD` locations, `CAPS:76`/`CAPS:150`, `CAPS:116`, `SKILL.md:46-64`, `INV-B:262`) | MINOR | no | changed | header; 2.2 WC-4, WC-10; 3.2 pr-submit; Decisions | SPEC:12, SPEC:65, SPEC:71, SPEC:165, SPEC:350; CAPS:76, CAPS:148, CAPS:150; INV-B:95, INV-B:262, INV-B:299 |
| R3-08 | R3 (section 1.3) says the Dispatch ID is not in the command's arguments; the Task 8 design puts it there | MINOR | no | unchanged | 1.3 R3; 2.2 WC-4 | SPEC:37, SPEC:65, SPEC:80, SPEC:102 |
| R3-09 | "Refused" under `--unattended` has no terminal status; AC-2.4 asserts `blocked` for one case | MINOR | no | unchanged | 2.2 WC-9; 3.2 rows; 7.3 AC-2.4 | SPEC:70, SPEC:153, SPEC:154, SPEC:159, SPEC:161, SPEC:165, SPEC:169, SPEC:172, SPEC:174, SPEC:261 |
| R3-10 | The Task 6 disposition keeps two wrong claims and V2 line numbers; the correction lives only in `DISP2` | MINOR | no | changed | review record | DISP:5, DISP:10, DISP:19; DISP2:41, DISP2:55 |

Open blocking findings: R3-01, R3-02, R3-03, R3-04 (all new). Round-2 blocking findings still open: none (N-05 is partly resolved and its residue is R3-03 and R3-05).

## Decisions
| Decision | Options | Rationale |
|---|---|---|
| Review header | `review: 1 of 3`; `review: 3 of 3` | `review: 1 of 3`. The invocation carried no `--re-review` and no `--baseline`, and the coordinator supplies the count (`SPCMD:258`, `SPCMD:261`); without them the run is a first review. "Round 3" is the brief's label. |
| Brief says any finding is FAIL; command says minor findings never block | follow the brief; follow the command | The command for the blocking flag and the Reviser brief (`SPCMD:264`); the verdict is FAIL under both, so the conflict changes nothing. |
| Scope of the critique | changed lines only; whole document | Whole document with an `origin=` tag, because no baseline flag was passed; 8 of 10 findings sit on changed text. |
| Resolution table scope | the 15 findings only; the 15 plus the six overstated citations | Both, as the brief asks; C-1 to C-6 are rows of the same table. |
| Citation check scope | every citation in the spec; citations in changed lines (`diff V2 SPEC`) | Changed lines (82 tokens, 23 lines) plus `DISP2`'s self-citations; V2 is in the workspace, so the diff stays inside the sandbox. |
| FR-19 grade for R3-01 | MAJOR (as R2 graded N-02); CRITICAL (count mismatch A attempts to 1 deliverable) | CRITICAL, because the Consistency Check finds a count mismatch with specific values and FR-19 makes that CRITICAL; R2 used the same convention for N-01. |
| Guard selection | every threshold in the spec; the six guards that decide Task 8 behaviour | The six listed. Acceptance-check thresholds add rows without new findings. |
| R3-05 and R3-08 grading | blocking under FR-9; non-blocking | Non-blocking: the intended reading is inferrable and the harm is bounded; stated so a reader can disagree. |
| Pr-submit "poll-then-sleep" claim | finding of its own; part of R3-07 | Part of R3-07: it is carried from V2, labelled partly UNVERIFIED, and the consequence is confined to Phase 4 (D3). |
| Use of the system's own skill list | cite it for command-count drift; ignore | Ignored: it is outside the workspace, and the 43-command count reconciles inside it (21 + 22, 10 + 27 + 6). |
| Self-Audit | write one; omit | Omitted: the brief asks for it on PASS only. The checks run are listed under Method. |
| Python | `uv run`; system `python3` | System `python3` was used for read-only text scans and small edits to this file in the sandbox (no repo code exists here), the same departure as `R2:333`. |

## UNVERIFIED in this review
1. Every `src/`, `~/.claude`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...`, `pyproject.toml` and Orca-JS citation in the spec: checked only against the inventory line that quotes it, or not at all (23 tokens in the changed lines).
2. Whether `worker-start --task --retry-of` returns the Dispatch ID in its receipt and takes no replacement Task text (R3-01, R3-02). `CAPS:116` quotes only the command form; spec item 21 relies on both.
3. Whether a replacement Task is allowed after a single failure while dependents wait (`CAPS:90`, `CAPS:116`), and whether a coordinator `send` can carry an answer to a retry worker (R3-02).
4. Which of the two adversarial contract layouts a P0 run produces, and whether the command prints the path (R3-03; `INV-A:60`).
5. Whether tasklist's Stage 9 `sc:task` leg runs as a Skill call or an Agent-tool call, and whether its gates can open in that context (R3-04; `INV-B:46`, `INV-B:211`).
6. pr-submit's poll-then-sleep structure (`sk/sc-pr-submit-protocol/SKILL.md:46-64`) and poll script runtime.
7. Whether the repo's command baseline matches section 3, in particular `/sc:spec-panel` (`command.md:22-23,451-461` shows a different text; spec item 19).
8. The 43-command count and the grep behind E5 ("no command mentions Orca", run 2026-11-02) describe the repo at that date; only `INV-A:3`, `INV-B:3` and the spec quote them.
9. No live check from spec section 7 was run; no Orca runtime, `src/` tree or git repository exists in the sandbox, so `git status --short` could not be checked against the README rule.

## Reviser brief
Blocking finding ids only: R3-01, R3-02, R3-03, R3-04.
Rules for the reviser (the reviser reads this report, not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Report the byte size of the spec before and after.

verdict: FAIL
