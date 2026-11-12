# QA Report - Decisions gate item 7.23 - Evidence-quality lens

**Agent:** rf-qa (read-only, fix_authorization: false)
**Date:** 2026-11-12
**Phase:** decisions gate, evidence-quality lens

## Checks

| Check | What was checked | Result |
|-------|------------------|--------|
| C1 | `1.0a-facts.md` shape: 15 rows for open items 1-11, 15, 16, 22, 23; the probe heading line numbers it quotes (12, 441, 455, 461, 475, 735, 785, 830, 910, 964, 968, 982, 997, 1015) match the real `## N.` lines | PASS |
| C2 | CLOSED row 1 (`session_join` field, path B): its cited sections 4 and 13 must show "no worker-show field holds a Claude session id" | FAIL (F1) |
| C3 | The other CLOSED rows (2, 4, 5, 6 names, 7, 8, 10, 11, 15, 22, 23) each cite a probe section whose output shows the fact; raw files re-read and re-hashed | PASS (notes F2, F3) |
| C4 | Raw capture integrity: byte counts and sha256 of `s1.json`, `m-t2-workerlist.json`, `b-tl-all.json` and the five `b-ws-*.json` reproduce; before/after payloads are identical once the envelope `id` is dropped; the canonical payload hash `a50676e2...` reproduces with `json.dumps(sort_keys=True)`; `agentWait` appears in 0 of 16 raw files | PASS |
| C5 | STILL UNVERIFIED rows (3, 6 `agentWait`, 9, 16) are not shown by any probe output | PASS |
| C6 | `owner-decisions.md` seven decision rows match their OQ-1..OQ-7 records at the cited lines (OQ-1 19-22, OQ-2 33-36, OQ-3 36-39, OQ-4 40-43, OQ-5 33-36, OQ-6 32-35, OQ-7 40-43) | PASS |
| C7 | The owner's words in those rows match the session transcript: AskUserQuestion answers on 2026-11-09 (".dev/sweeps/ (Recommended)", "New WC-16 rule (Recommended)", "Pin and cite snapshot (Recommended)", "Six hours (Recommended)", "Add an exception", "Authorize bounded revision") and 2026-11-11 ("Sign off D9 as written (Recommended)", "Use run_a4723d345399 (Recommended)", "Keep the 10 commands (Recommended)"); the OQ-1 relay is in the 2026-11-08 session | PASS (note F7) |
| C8 | All 13 APPROVED quotes (D3 :10, D4 :11, D5 :12, GIT :13, L3 :20, CR-01 :25, PATHS :29, UPSTREAM :30, B1 :35, B1-N1 :36, S4 :47, G1 :71, F1 :90) are byte-equal to the decision cell of that line of `APPROVED.md`, and the first-column id matches | PASS |
| C9 | The "Constraint on Phase 1" column equals the research/09 Gap 1 table (lines 31-41) once the bracketed re-anchor notes are removed; the re-anchors hold (`WORKER-CONTRACT.md:63` is WC-14; DESIGN :736, :647, :643, :947 say what the notes claim; :638 and :925 no longer hold the cited text) | PASS |
| C10 | GQ-63 split: BUILD-REQUEST.md:15 quote is verbatim; the execution message "Accepted, I accepted, but it reported a decline.  Proceed" exists once at 2026-11-11T20:26:41.816Z in the session transcript; the interrupted question and the "Run 7.10 now (Recommended)" option text quoted in `step-7.10-style-exception.md` match the 2026-11-10T07:07:00Z AskUserQuestion call | PASS |
| C11 | `pr422-409-check.md`: points 1-3 each have their command and output; a re-run today reproduces them (gh MERGED / `2327fbd37819...` / `2026-11-07T14:15:58Z`; ancestor 1 exit 0; ancestor 2 exit 1; HEAD `5dc29d23...`; local `origin/master` `35073356...`); point 4 is a note | PASS (note F4) |
| C12 | Early style check: `git diff HEAD -U0` of `pragmatic.md` equals the diff recorded in `step-7.10-style-exception.md` and `decisions-mechanical.md` S11 (7 hunks at 22, 53, 58, 60, 69, 80, 90; 11 added, 7 removed; 234 to 238 lines; 6 qualifier lines; `## Work discipline` at 107 to end-of-file and lines 1-21 byte-identical to HEAD; no non-ASCII in added lines) | PASS |
| C13 | Style text against addendum lines 13-21 and 27 (the sentence mapping in the 7.10 table is accurate); HOME style `~/.claude/output-styles/pragmatic.md` has mtime 2026-11-11 16:25:44 and no exception text; `Makefile` `sync-dev` copies skills, agents, commands, hooks and templates, not output styles | PASS |
| C14 | Revision-check and execution claims: the four checks of both revisions exist with `VERDICT: PASS`; the PRE facts in the 7.10 file (plan sha `eb291f0b...`, 3020 lines, 132 citations, `execution_clearance: false`, open findings HIGH 2 / MEDIUM 1 / LOW 6 = nine) match `signoff.yaml` and `return-contract.yaml`; the 7.10 file does not use old PRE or waivers as approval | PASS |
| C15 | `decisions-mechanical.md` Run 3 claims (C1-C9, S1-S11) reproduce today, apart from the time-bound S8 listing | PASS (note F6) |
| C16 | `tests/sweep/fixtures/` against `SOURCES.md` and the probe: 19 `captured-*.json` plus `SOURCES.md`; the five pane-key / handle joins hold; no `coder`, real UUID or owner name is left; worktree arrays are cut to 3 and 2 with `totalCount` set; dispatch times, page object and unknown-Run bodies equal the probe | PASS |
| C17 | R5 edit: DESIGN 7.3 (10 templates, `FORBIDDEN_TOKENS` only `--include-remote`), 11 (line 759), 12 (NFR-014 row, line 815), 13 (D10, line 837, quote equal to OQ-1), 15.1 (line 895), GQ-109 row (line 66) and Fix cycle 3 R5 row (line 1047) agree with each other and with OQ-1 | PASS |
| C18 | The probe is internally consistent: section 4 line 499 ("The only place a session id was found is the tab-map entry") against the raw `worker-show` outputs and section 13 line 1059 | FAIL (F1) |
| C19 | Disclosure: the deviations and readings that the capture and the facts file rely on are stated | PASS (notes F2, F5) |

## Findings

### F1 (MAJOR): "No worker-show field holds a Claude session id" is contradicted by the stored raw outputs

- Claim: `readonly-probe.md:499` ("No field in `worker-show` holds a Claude session id. The only place a session id was found is the tab-map entry (section 13).") and `1.0a-facts.md:11` (row 1: "No `worker-show` field holds a Claude session id, so path A ... cannot apply").
- Evidence against: in all five `readonly-probe-raw/b-ws-*.json`, `result.terminal.preview` contains `claude --resume <session id>`, and each id equals line 1 of that worker's tab-map entry (04f1e248-bb2f-451f-9372-0c3c1522822e, 3ca57b4e-b4ee-407f-902a-7e2bf106084c, 72f129f1-5b59-4ea9-bddc-a349c8cc11f0, 09d4521f-b24f-4ed3-860c-33b6fb013bf6, 7832d8b6-85a3-4457-a2f7-b8b22b4d2bd2; `readonly-probe.md:1048-1052`). The probe admits this for the first worker only (`readonly-probe.md:1059`), so it contradicts itself; the fixtures keep the same preview (`tests/sweep/fixtures/SOURCES.md:11`).
- What is wrong: the CLOSED row for open item 1 rests on a sentence that the capture's own data refutes. The conclusion (path B, because the preview is free text from an exited terminal, not a join field) is probably still right, but the file never says so and never records that live workers were not checked.
- Smallest fix: in `readonly-probe.md:499` and `1.0a-facts.md` row 1, replace the two sentences with: "No structured `worker-show` field holds a Claude session id. The id appears only as free text in `result.terminal.preview` (`claude --resume <id>`) for all 5 exited workers; whether a live worker's preview shows it is UNVERIFIED, so it is not used as a join. Path B applies."

### F2 (MINOR): the M4 "no change" check rests on an unconfirmed reading

`readonly-probe.md:783` and `1.0a-facts.md:21` (row 11) read "identical apart from timestamps" as not covering the envelope `id`. All 7 pairs differ in raw bytes at that one key and nowhere else (re-confirmed: payloads equal, raw bytes differ), so the claim is true, and the reading is disclosed together with the HALT text the owner would use. It is the executor's reading, not the owner's. Fix: none needed; repeat the sentence in the next owner-facing summary.

### F3 (MINOR): row 2 "11 Run ids" mixes sources

`1.0a-facts.md:12` says it matched 11 Run ids. One is observed in the capture (`run_a4723d345399`), 9 come from the owner's pasted `run-list` recorded in `OQ-8-run-id-decision.md:35-42`, and the 11th is the made-up `run_000000000000` (`readonly-probe.md:974`). Line 3 of the facts file says every fact is sourced from the probe. The regex still matches all 11 (each has 12 lowercase hex digits). Fix: write "1 observed in the capture, 9 from OQ-8, 1 made up".

### F4 (MINOR): `pr422-409-check.md` mentions two commands it does not record

Lines 23 and 31 say `git cat-file -t` prints `commit` for both hashes, and line 3 says "the three commands below only read". The two `cat-file` outputs are not recorded. I ran them: both print `commit`. Fix: record the two outputs or drop the sentences.

### F5 (MINOR): `ls -la` of the tab-map folder was run twice

`readonly-probe.md:1021` says the listing ran twice; item 7.16 describes one listing, and the Deviations section names only D1. Read-only and harmless. Fix: add one line to Deviations.

### F6 (MINOR): time-bound results in the mechanical file

`decisions-mechanical.md` S8 (`tests/sweep` holds only `fixtures`) and C9 were true at 2026-11-11T22:58Z and are still true today (`ls tests/sweep` prints `fixtures`), but they stop being true once item 8 starts. Not a defect today.

### F7 (MINOR): OQ-1 row says "the owner" with no "relayed" mark in the row

`owner-decisions.md:9` gives Decider "the owner, 2026-11-08"; the relay is disclosed only in the Provenance paragraph (line 17). The relay is real (message `msg_d95a87e312e1`, 2026-11-08T12:05:48Z, found in session 6ee233a2). Fix: add "(relayed)" in the row.

## Evidence summary

- Tool use (approximate): Read about 25, Grep 8, Glob 2, Bash about 21 (hashes, jq, git, one gh read of PR 422, transcript searches, one `uv run python -I` script reading stdin). I wrote no file other than this report.
- Limits: the raw outputs of `worktree ps --json` and `worktree list --json` are not stored (by design), so the section 6 and 7 counts (28 worktrees) cannot be re-hashed; the fixtures and the redacted entry agree with them. The plan sha `eb291f0b...` (3020 lines) named in the 7.10 file cannot be re-hashed because the plan file has changed since (now 3033 lines); it matches `signoff.yaml` and `return-contract.yaml`. No live Orca probe was made.

## Verdict

Verdict: FAIL
Blocking count: 1
