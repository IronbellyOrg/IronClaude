# Spec panel round 2: orca-worker-contract-spec.md (revised)

review: 1 of 3

## Run mode, citation keys and limits
Task 7, independent re-review of the revised spec. Planning only: no file other than this one was written. Command run as defined in `command.md`: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`, plus the brief's parts 1 and 2 (resolution table, citation check) in front of it.

- **Keys.** `SPEC:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (revised, 80732 bytes, 404 lines). `V1:N` = `specs/history/spec-v1.md` (57763 bytes, the pre-revision text). `R1:N` = `review/spec-panel.md`. `DISP:N` = `review/disposition.md`. `INV-A:N`, `INV-B:N`, `CAPS:N` = `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `SPCMD:N` = line N of the `/sc:spec-panel` definition `command.md` in the sandbox root; used for the Review Loop and, as in round 1, only as evidence about what that command's text already says.
- **Run mode.** No `--re-review` or `--baseline` was passed, so under Review Loop bullet 1 (`SPCMD:258`) this is a first review of the full document: header `review: 1 of 3`, no `origin=` restriction. I still tag each new finding `origin=changed` (text touched by the revision, found by `diff` against `V1`) or `origin=unchanged`. The 22-row table in Part 1 is the brief's own check, not the command's re-review table; its blocking rows use the command's `resolved|open|regressed` vocabulary (`regressed` is empty: round 1 marked nothing resolved).
- **Grading conflict, stated openly.** The brief says any finding of any severity is FAIL. Review Loop bullet 7 (`SPCMD:264`) says a brief may not grade a minor finding as blocking, and bullet 2 (`SPCMD:259`) makes MINOR a note. I follow the command: only CRITICAL, FR-8/FR-9 and concretely-wrong-outcome MAJOR findings block. The verdict is FAIL either way, because six blocking findings are open (N-01 to N-06).
- **What could be checked.** The workspace holds the spec, `V1`, the README, the three inventories, `R1`, `DISP`, and `command.md`. `src/`, `~/.claude`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...`, `orca-ide` output and Orca's compiled JS are not in the sandbox, and `~/.claude` (sandbox `home/`) holds only an empty `rules/prompts/` folder. A citation to any of those is checked only against the inventory line that quotes it, otherwise it is UNVERIFIED. No Orca command was run; no live check from spec section 7 could be run.
- **Method.** Read all of `command.md`, `R1`, `DISP`, the spec, the three inventories and `README`. Built the changed-line set with `diff V1 SPEC` (168 changed or added lines, hunks at `SPEC:5` to `SPEC:404`). Re-ran two of the spec's own checks in the sandbox: the AC-C1 pattern on sample text, and the placeholder grep from `DISP:10`.

## Part 1: Resolution of the 22 round-1 findings
Each row was checked against the revised spec text itself, not against `DISP`. "Blocking" is the round-1 grade (`R1:264-287`). Result for blocking rows: `resolved` or `open`. For non-blocking rows: `resolved`, `partly` (the rule exists but a new defect sits on it) or `open`. Residual defects are new findings in Part 3 (N-xx).

| # | Round-1 finding | Blocking | What the spec now says (evidence) | Result | Residual |
|---|---|---|---|---|---|
| F-01 | Three spellings of the report location | yes | `--report-dir` defined once (SPEC:53), used in WC-4 (SPEC:64), section 3 intro (SPEC:126), the analyze and spec-panel rows (SPEC:149, SPEC:170), AC-1.2 (SPEC:253), D1 example (SPEC:307), Decisions (SPEC:346). `--output` and `--output-dir` keep their meanings (SPEC:53). A grep of the spec shows no remaining use of `--output`/`--output-dir` as the contract location. | resolved | Three ACs and one AC-2.8 call still omit the flag (N-04). `pr-submit` row says the contract goes "beside `monitor-run-<PR>.jsonl`" (SPEC:164), see N-15. |
| F-02 | No rule for missing or unusable location; WC-4 vs WC-6 | yes | Refusal rule: no `--report-dir`, uncreatable, unwritable or inside `.git/` means stop, no file, worker settles `failed` (SPEC:64). New directory per attempt (SPEC:64, SPEC:79, SPEC:347). WC-6 separates deliverable dir from report dir (SPEC:66). AC-2.7 tests retry and no-dir (SPEC:261). | open | The retry cannot receive the new directory: `worker-start --task --retry-of` reuses the Task spec that holds the old command line (SPEC:236, SPEC:261; CAPS:116). N-02. The refusal rule is violated by AC-2.8, AC-3.3, AC-3.4, AC-4.1 (N-04). |
| F-03 | P1 flag and AC-1.1 cover 37, 15 converted | yes (CRITICAL) | Flag accepted only in the phase of the row (SPEC:126, SPEC:204); P1 names 14 plus load (SPEC:209); P2 15, P3 4, P4 3 (SPEC:210-212). I counted the rows: P1 14 + load 1, P2 15, P3 4, P4 3 = 37; 3.1 has 10 rows and 3.2 has 27. AC-1.1 checks the P1 list only (SPEC:252). 2.3 item 2 tells the coordinator not to pass the flag early (SPEC:78). | resolved | The new nesting rule WC-13 re-creates a count mismatch of the same kind (N-01). |
| F-04 | AC-C1 cannot pass and is vacuous | yes | AC-C1 rewritten (SPEC:222) and written out as a fenced block (SPEC:228-232): case-insensitive, verbs include `status\|open\|skills`, first grep excludes only `ccsession-tag`, second grep over `core/` excludes only `WORKER-CONTRACT.md` and `HOW-WE-WORK.md`. I ran the block's pattern on sample lines: it matched `orca-ide orchestration worker-start`, `ORCA orchestration dispatch`, `orca worktree create` and `orca-ide skills get`. DISP:18 rejects the `\|` sub-claim: correct for the rendered table (GFM accepts an escaped pipe inside a cell), irrelevant now that the block replaces the cell. | resolved | The pattern also matches prose such as "the orca status line" (tested); nit in N-15. |
| F-05 | Status vocabulary unchecked; empty report undefined | yes | `worker_status` added for contracts that use other words (SPEC:64); validity rule for empty, unparseable or out-of-set reports (SPEC:65); 7.2 steps 3-4 use it (SPEC:238-239); AC-0.5 (SPEC:250); UNVERIFIED item 15 (SPEC:371). The words themselves are still not recorded: the only recorded state is workflow's `failed` (INV-B:272). | open | The validity rule is applied to every worker, including P0 smoke runs and 3.1 commands that have no conversion yet, so a healthy run whose report is `REPORT.md` or a legacy contract settles `failed` (N-05). |
| F-06 | WC-3 ask protocol incomplete | yes | "Once per gate" (SPEC:63); `--answer <gate-id>=<text>` for gates with no flag, added in the converting phase (SPEC:63, SPEC:210); rows name `clarify` and `context` inputs (SPEC:140, SPEC:165, SPEC:167); `answer_wait` in the brief (SPEC:81); decline or expiry resolves blocked then `failed` (SPEC:63); AC-2.6 covers answered and unanswered runs (SPEC:260); Decisions (SPEC:348). | resolved | `--answer` grammar is not stated (N-12, minor). |
| F-07 | WC-10 hole at 4-5 min; Monitor waits | yes | Rule is now "no single tool call may last longer than 4 minutes", Monitor waits kept alive with bounded waits and heartbeats (SPEC:70); AC-2.8 (SPEC:262); Decisions (SPEC:345). The 4.5-minute call of R1:200 is now forbidden. | resolved | The broadened rule contradicts WC-7 and E4 for foreground Agent-tool fan-out and long synchronous Bash work (N-06). The heartbeat-gap arithmetic in SPEC:345 is stated too strongly (N-13, minor). |
| F-08 | WC-9 has no authorization mechanism | yes | Grant flags named: auggie-review `--post-pr`, task `--allow-commit`/`--allow-push` (SPEC:69, SPEC:150, SPEC:171, SPEC:210); grant plus its opposite is a usage error (SPEC:69); AC-2.4 tests the conflict and the task commit case (SPEC:259); Decisions (SPEC:349). post-release and pr-submit flags deferred to the Phase 4 plan (SPEC:69), consistent with D3/D4. | resolved | none |
| F-09 | Eight requirements lack a check | no | Section 7.4 maps WC-1 to WC-13 to a check or to inspection (SPEC:272-289); new AC-2.6 to AC-2.8 (SPEC:260-262). | partly | WC-13 is checked by text assertions only (SPEC:289); WC-6 rests on AC-2.7, whose mechanism is open (N-02). |
| F-10 | No nested-invocation rule | no | WC-13 (SPEC:73), `Nested:` line (SPEC:54), AC-1.1 (SPEC:252), tasklist row (SPEC:172). | partly | WC-13 conflicts with the phase gate (N-01), its directory name is not unique (N-03), and "no second copy" in WC-4 may starve readers of nested contracts (N-07). |
| F-11 | No coordinator-side failure procedure | no | Procedure added at SPEC:84 (poll `worker-show` every 5 min, `agentWait`, positive-proof rule, retry with new directory, own limit for a silent worker). | partly | Self-contradictory and overstates the circuit breaker (N-08). |
| F-12 | `partial` undefined; FAIL verdict settles as success | no | `partial` defined; each command's section says whether it can emit it; `succeeded` does not by itself unblock dependents (SPEC:65); coordinator reads status, verdict and `skipped` before starting dependents (SPEC:86); `verdict` and `skipped` fields (SPEC:64). | resolved | none |
| F-13 | WC-11 vs fixed output paths | no | WC-11 lists cleanup-audit and index-repo as one-owner-per-worktree and tells the brief to give a second worker a separate worktree (SPEC:71, SPEC:82, SPEC:136); consistent with `CAPS:115`. | resolved | none |
| F-14 | How a worker runs a `/sc:` command | no | 2.3 item 1: Skill tool, top level, never an Agent-tool subagent; argv expansion marked UNVERIFIED (SPEC:77, SPEC:374); examples (SPEC:88-123). | resolved | none |
| F-15 | Worker-written files consumed without trust statement | no | Last paragraph of 2.3: treated as data, `blocked_question` passed to the person unchanged (SPEC:86). | resolved | none |
| F-16 | No `contract_version`, write ordering, `blocked` name clash | no | `contract_version: 1`, write-temp-then-rename completed before `worker_done`, note that the contract's `blocked` is not Orca's Task status (SPEC:64; `CAPS:89`). | resolved | Rename needs a Bash tool some commands lack, and the version field is ambiguous for commands with their own (N-11, minor). |
| F-17 | A rule of this planning run cited as product rationale | no | `README:31` is absent from WC-9 (SPEC:69) and from the `/sc:git` row (SPEC:183); the remaining `README.md:31` strings in the spec point at the codegraph-migration README (SPEC:24, SPEC:44), a different file. | resolved | `INV-A:49` and `INV-A:91` still cite `README:31`, but the spec now rests on `cmd/git.md:14-17,90` (UNVERIFIED, src). |
| F-18 | Three statements stronger than evidence | no | (a) tasklist row states both sides (SPEC:172; `INV-A:14`, `INV-B:210`, `INV-B:314` all match); (b) "is not expected to fail", with the UNVERIFIED reason (SPEC:45); (c) E3 reconciled in 1.4 (1) (SPEC:44). | resolved | none |
| F-19 | "Well inside" unmeasurable | no | "within 30 s" (SPEC:61); `CAPS:49` quotes a 30 s fallback passing and about 45 s failing. | resolved | none |
| F-20 | load and recommend scheduled though coordinator-side | no | load gets no section, no flag, usage-line fix only (SPEC:54, SPEC:162, SPEC:189, SPEC:252); recommend kept by a recorded decision (SPEC:351). The 10/27/6 and 37 counts are unchanged and consistent. | resolved | none |
| F-21 | "Phases 1-3 need no decision" vs D1 | no | Phases 1-3 assume D1 (a) and are partly rework under (b) (SPEC:204, SPEC:304). | resolved | none |
| F-22 | No worked example | no | Section 2.4 (SPEC:88-123): P0 brief, P1 brief, succeeded and blocked contracts, all marked illustrative. | resolved | The P0 brief example is where N-05 shows (SPEC:91-97). |

Summary: of the 8 blocking round-1 findings, 6 are resolved (F-01, F-03, F-04, F-06, F-07, F-08) and 2 are open (F-02, F-05). Of the 14 non-blocking ones, 11 are resolved and 3 are partly resolved (F-09, F-10, F-11). `regressed`: none.

Disposition accuracy (DISP vs the spec): every `SPEC:N` cited in `DISP:15-35` points at the claimed text except two. `DISP:19` places UNVERIFIED item 15 at `SPEC:370`; it is at `SPEC:371` (370 is item 14). `DISP:10` says the placeholder grep "returns nothing"; I ran it and it returns `SPEC:158` (the word `TodoWrite` matches `TODO` case-insensitively), which the same sentence then explains. Both are cosmetic.

## Part 2: Citation check (added or changed citations)
Scope: every citation in a line the revision added or changed (`diff V1 SPEC`), plus the self-citations in `DISP`. "Live file" here means the workspace file the citation names; anything outside the workspace is checked only through the inventory line that quotes it. Results: `ok` (the cited line says what the spec claims), `ok-quoted` (src or Orca path, matches the inventory's quote, source itself UNVERIFIED), `unverified` (no workspace line to compare), `overstated`, `wrong`.

| Spec line | Citation | Claim in the spec | Result |
|---|---|---|---|
| SPEC:44 | `INV-A:35`, `CAPS:156`, `CAPS:187` (via E3 and 1.4 (1)) | `skill-direct` records only the Skill-tool call, not top-level vs subagent | ok: `INV-A:35` quotes `invocation_method: "skill-direct"`; the spec's reading is more careful than `INV-A:35`'s "proven" |
| SPEC:45 | `CAPS:47`, `CAPS:49`, `CAPS:52`, `CAPS:129` | task reaches Claude as a launch argument; plain-launch evidence only; waiting worker is "healthy, not failed" | ok (all four lines say it) |
| SPEC:61 | `CAPS:44-45`; `EVIDENCE.md:45,56` | 30 s fallback is the longest passing; above about 45 s fails | ok-quoted: `CAPS:49` quotes both; `EVIDENCE.md` not in workspace |
| SPEC:63 | `CAPS:58-61`, `CAPS:64` | ask timeout leaves question pending, resume by ID; no heartbeat while blocked in `ask` | ok |
| SPEC:64 | `CAPS:72-74`, `CAPS:79`, `CAPS:89` | `--report-path` only with real values; Orca does not check the file (UNVERIFIED); Orca Task status `blocked` | ok |
| SPEC:64 | `INV-B:272`, `INV-A:97`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41`, `sk/sc-brainstorm-protocol/SKILL.md:335` | workflow contract is versioned 1.1; brainstorm writes a named contract | ok / ok-quoted |
| SPEC:64 | `INV-B:112`, `INV-A:35`, `INV-A:60`, `INV-B:242` (existing contract writers) | workflow, reflect, brainstorm, adversarial, troubleshoot (`--caller task-unified`) write contracts | ok |
| SPEC:65 | `CAPS:73`, `CAPS:76-77` | outcome is `succeeded` or `failed` only; one `worker_done` from the dispatched pane | ok |
| SPEC:66 | `CAPS:116` | retry command; resume mechanisms in `INV-A:35-55`, `INV-B:31-52` | ok |
| SPEC:69 | `cmd/auggie-review.md:51-54`; `INV-A:38` | posts by default with no prompt; `--no-post-pr` exists | ok-quoted (`INV-A:38` cites `C:51,52,53,54`) |
| SPEC:69 | `INV-B:204` | task EXEMPT `commit` and `push` run at once, no flag | ok |
| SPEC:69 | `cmd/git.md:14-17,90` via `INV-A:49` | git mutations need user authorization | ok-quoted |
| SPEC:70 | `CAPS:130`; `cmd/pr-submit.md:49` | cadence from the preamble; pr-submit's 600 s is per wait | ok / ok-quoted (`INV-B:95`) |
| SPEC:70 | `sk/sc-pr-submit-protocol/SKILL.md:46-64` | "one foreground poll, then a sleep of at least `--poll-interval`" | unverified: `INV-B:299` cites `41-64` for the loop but no inventory records the poll-then-sleep detail |
| SPEC:70 | `sk/sc-cli-eval-protocol/SKILL.md:151-152` via `INV-A:65` | eval timeouts up to 3600 s | overstated range: `INV-A:65` cites `:151` only; `:152` is unsupported (text unchanged from V1, carried into the rewritten row) |
| SPEC:71 | `cmd/save.md:42-45`; `CAPS:115` | single-owner keys; workers share the current worktree, a separate one only on a concrete conflict | ok |
| SPEC:73 | `INV-A:39`, `INV-B:119`, `INV-B:219`, `INV-B:201`, `INV-B:91`, `INV-B:271`, `INV-B:112` | the six nesting chains of WC-13 | ok. Note `INV-B:119` shows the nested brainstorm; the adversarial leg of release-split is at `INV-B:121`. `INV-B:219` is the nested `task` skill (MDTM), which is not one of the 43 commands (see N-01) |
| SPEC:77 | `INV-A:35` | `skill-direct` is the only evidence for the Skill-tool form | ok |
| SPEC:84 | `CAPS:126`, `CAPS:125-127`, `CAPS:188` | positive-proof rule; never act on absence; Dispatch run time unbounded is UNVERIFIED | ok |
| SPEC:84 | `CAPS:116` | a retry "is subject to Orca's three-failure circuit breaker" | **overstated / contradicted**: `CAPS:80` quotes `[G:recovery]`: "Failed `worker-start` attempts count across `--retry-of`; a worker's own `failed` report does not". A retry after `worker_done --outcome failed` is not bounded by the breaker. SPEC:342 says the opposite of SPEC:84 (N-08) |
| SPEC:86 | `CAPS:84-92`, `CAPS:107-113` | a completed Task makes dependents appear in `task-list --ready`; release after settlement | ok |
| SPEC:129 | none (prose) | "until Phase 1 adds the contract" | stale after F-03: four 3.1 commands convert in P2 (N-10) |
| SPEC:150, 171, 172 | `INV-A:38,62`, `INV-B:204`, `INV-A:14`, `INV-B:210`, `INV-B:314` | auggie-review, task and tasklist row evidence | ok |
| SPEC:162 | `INV-B:31,57-65` | load: no gate, no report, `--checkpoint` missing from Usage | ok (`INV-B:63`) |
| SPEC:164 | `INV-B:34,87-95`; `sk/sc-pr-submit-protocol/SKILL.md:37-39` | top-level rule | ok-quoted. `CAPS:161` quotes the same sentence from the home-installed skill at `:47-49`; the two copies differ by 10 lines, which suggests version drift between the installed and the src skill. UNVERIFIED which text the repo ships |
| SPEC:183 | `cmd/git.md:14-17,90`; `INV-A:49,91` | git is coordinator-only | ok-quoted; `README:31` correctly gone |
| SPEC:209-212 | `INV-A:96`, `INV-B:292`, `INV-B:294,296`; `qa.md:238`; `SKILL.md:189,196`; `SKILL.md:340,351` | phase rationale | ok / ok-quoted (`INV-A:51,66`, `INV-B:94`, `INV-B:79`) |
| SPEC:346, 375 | `SPCMD:22-23`, `SPCMD:451-461` | supplied `/sc:spec-panel` already has `--report-dir`, `--unattended` and an `## Unattended mode` section | ok: `command.md:22-23` and `command.md:451-461` say so. The key `SPCMD` is not defined in the spec's own citation conventions (SPEC:8-12); only the phrase "that review's" and `R1:9` explain it (N-15) |
| SPEC:371 | `INV-B:272`, `INV-B:112`, `INV-A:39`, `INV-A:60`, `INV-B:242` | status words not recorded | ok. One qualification: `INV-B:272` does record that workflow's contract has a `failed` state |
| SPEC:12, SPEC:370 | "re-read 11 locations", "about 340 citations ... 9 defects" | validation of the spec's citations | stale: both describe `V1`; the revision added 22969 bytes and re-cited many lines, and neither check was re-run (N-14) |
| DISP:19 | `SPEC:370` for UNVERIFIED item 15 | position of item 15 | **wrong**: item 15 is at `SPEC:371` |
| DISP:10 | placeholder grep "returns nothing" | no TBD/TODO text | inaccurate: the grep returns `SPEC:158` (`TodoWrite`); the sentence concedes this |
| DISP:15-35 (all other `SPEC:N`) | the other `SPEC:N` citations (81 occurrences in those rows in total) | where each fix landed | ok: every one that names the place of a fix was compared with the spec line; only DISP:19 was off |

Wrong or overstated: SPEC:84 (`CAPS:116`), SPEC:70 (`:151-152`), DISP:19 (`SPEC:370`), DISP:10 (grep claim), stale validation claims at SPEC:12 and SPEC:370. No wrong `INV-A`, `INV-B` or `CAPS` line number was found among the added or changed citations. Citations into `src/`, `~/.claude`, `CLAUDE.md`, `EVIDENCE.md` and Orca's JS (55 backticked path citations of that kind in the changed lines, counted with a regex) are `ok-quoted` or `unverified` only; none could be re-read.

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
  overall_score: 6.5
  clarity: 7
  completeness: 7
  testability: 6
  consistency: 5.5
critical_issues:
  - {id: N-01, severity: CRITICAL, expert: Fowler, issue: "WC-13 asks P1 commands to pass --unattended to commands that do not accept it until P2 or never", recommendation: "limit WC-13 to children already converted; name the interim behaviour"}
  - {id: N-02, severity: MAJOR, expert: Nygard, issue: "A new report directory per attempt cannot reach a retry worker started with --retry-of", recommendation: "derive the directory from the Dispatch ID, or state how the Task spec is changed"}
  - {id: N-03, severity: MAJOR, expert: Whittaker, issue: "<report-dir>/<child-command>/ is not unique when a parent runs the same child N times", recommendation: "add a per-invocation suffix"}
  - {id: N-04, severity: MAJOR, expert: Crispin, issue: "AC-2.8, AC-3.3, AC-3.4, AC-4.1 pass --unattended without --report-dir and so trip WC-4's own refusal", recommendation: "add the flag to every AC"}
  - {id: N-05, severity: MAJOR, expert: Newman, issue: "WC-5 validity rule marks every non-contract or legacy report as 'no report', so P0 and pre-conversion workers settle failed on healthy runs", recommendation: "scope WC-5 validity to workers that run with --report-dir; define the pre-conversion outcome rule"}
  - {id: N-06, severity: MAJOR, expert: Nygard, issue: "WC-10 forbids any tool call over 4 minutes but WC-7/E4 keep foreground Agent-tool fan-out and long synchronous runs", recommendation: "say which calls the cap covers and how a blocked turn heartbeats"}
expert_consensus:
  - "The revision closed 6 of the 8 round-1 blocking findings and 11 of 14 non-blocking ones; the unattended-flag phasing, report-dir, ask, grant-flag and AC-C1 fixes read correctly."
  - "The new defects sit where two revision rules meet: nesting (WC-13) with phase gating, report-dir per attempt with Orca retry, the validity rule with pre-conversion workers, and the 4-minute cap with fan-out."
  - "Counts and cross-references are accurate: 43 = 10 + 27 + 6; phases name 14 + 1 + 15 + 4 + 3 = 37."
improvement_roadmap:
  immediate: [N-01, N-02, N-03, N-04, N-05, N-06]
  short_term: [N-07, N-08, N-09]
  long_term: [N-10, N-11, N-12, N-13, N-14, N-15]
adversarial_analysis: "see === ADVERSARIAL ANALYSIS (Whittaker) ==="
```

### Panel and method
Review order followed `SPCMD:101-113` for the experts active under `--focus requirements,architecture` (`SPCMD:131-148`) plus Whittaker (`SPCMD:84`) and Crispin for guard-table completeness (`SPCMD:311`). The whole document was reviewed, not only the changed lines; `origin=` records where each finding sits. Grading follows `SPCMD:259`: CRITICAL and FR-8/FR-9 findings block; a MAJOR blocks only when it names a concrete wrong outcome; MINOR is a note. `--focus correctness` is not active, so no State Variable Registry. The Guard Condition Boundary Table and Quantity Flow Diagram are produced because the spec has threshold and flag guards and a multi-stage count-changing flow, and both were completed before the synthesis (FR-10, `SPCMD:330`).

### Mandatory output artifacts

#### Guard Condition Boundary Table
Guards are the ones whose value or flag state decides behaviour in the revised section 2 and section 6: G1 WC-10 call cap, G2 WC-4 report directory, G3 WC-5 report validity, G4 WC-3 ask gate, G5 WC-9 grant flags, G6 phase gate on the flag. Construction Nygard, completeness Crispin, attack Whittaker. Every cell is populated.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 no tool call over 4 min; heartbeat at least every 5 min | SPEC:70 | Zero/Empty | wait = 0 s | false | No splitting, nothing to heartbeat across | OK |
| G1 | SPEC:70 | One/Minimal | one 1 s call | false | Allowed | OK |
| G1 | SPEC:70 | Typical | 3 min poll after a heartbeat | false | Allowed; heartbeat between calls | OK |
| G1 | SPEC:70, SPEC:67, SPEC:25 | Maximum/Overflow | foreground Agent-tool call that runs 12 min (tdd research agents INV-B:221; cleanup-audit waves INV-A:42) | true (over 4 min) | Contradictory: WC-10 forbids it, WC-7 and E4 say a command's fan-out "stays as it is"; no rule for how a turn blocked in an Agent call heartbeats | GAP |
| G1 | SPEC:70, SPEC:345 | Sentinel Value Match | a call of exactly 240 s started 2 min after the last heartbeat | false (not longer than 4 min) | Rule satisfied; "so the session can heartbeat between them" implies a heartbeat before the call but does not say so (gap 6 min otherwise). Recorded as N-13 (minor) | OK |
| G1 | SPEC:70, SPEC:262, INV-A:44 | Legitimate Edge Case | Monitor-watched background job (cli-eval) | not evaluable per call | Turn kept open with waits of at most 4 min and heartbeats between; whether Monitor wakes an idle turn is stated UNVERIFIED; AC-2.8 observes it | OK |
| G2 `--report-dir` given, creatable, outside `.git/`, new per attempt | SPEC:64 | Zero/Empty | `--unattended` with no `--report-dir` | false | Stop before work, no file, worker settles failed | OK |
| G2 | SPEC:64 | One/Minimal | existing empty directory | true | Contract written there | OK |
| G2 | SPEC:64, SPEC:110 | Typical | new creatable directory `.dev/orca-runs/analyze-1/attempt-1/` | true | Contract written | OK |
| G2 | SPEC:64, SPEC:79, SPEC:236, SPEC:261, CAPS:116 | Maximum/Overflow | retry started with `worker-start --task <id> --retry-of <dispatch>`; the command line lives in the Task spec | unknown | Spec requires a new directory per attempt but names no way to change the command line of an existing Task; behaviour on a directory that already holds a contract is not stated | GAP |
| G2 | SPEC:64 | Sentinel Value Match | path inside `.git/` | false | Refused as unusable | OK |
| G2 | SPEC:73, SPEC:172, INV-B:211 | Legitimate Edge Case | one parent runs the same child N times (tasklist Stage 10.5 runs N reflects) | collision | `<report-dir>/<child-command>/` gives all N children one directory; tasklist row says "its own report subdirectory" without a name | GAP |
| G3 report valid only if file exists, non-empty, parses, has `command`, status in the four | SPEC:65, SPEC:239 | Zero/Empty | 0-byte `return-contract.yaml` | false | No report, worker settles failed | OK |
| G3 | SPEC:65 | One/Minimal | YAML with only `status: succeeded` and `command` | true | Valid; succeeded (other WC-4 fields are not part of validity) | OK |
| G3 | SPEC:65 | Typical | `status: succeeded` | true | succeeded | OK |
| G3 | SPEC:65, SPEC:86 | Maximum/Overflow | `status: partial` with a long `skipped` list | true | succeeded; coordinator reads `skipped` before starting dependents | OK |
| G3 | SPEC:65, SPEC:91-97, SPEC:251, INV-B:242 | Sentinel Value Match | non-contract report (markdown `REPORT.md`, a TDD file) or a legacy status word, from a P0 smoke run or a 3.1 command before its conversion | false | "Counts as no report": a healthy run settles failed. The P0 brief example names `REPORT.md` as `--report-path` and gives no outcome rule; AC-0.4 step 3 requires a WC-4 contract path that cannot exist | GAP |
| G3 | SPEC:65 | Legitimate Edge Case | audit with verdict FAIL | true | succeeded; first sentence names the verdict | OK |
| G4 ask once per gate; answer by flag or `--answer`; bounded by `answer_wait` | SPEC:63, SPEC:81 | Zero/Empty | `answer_wait: 0` | false | Gate resolves blocked at once; worker settles failed (AC-2.2) | OK |
| G4 | SPEC:63 | One/Minimal | one gate, answered inside `answer_wait` | true | Re-invoke with the answer; overwrites the blocked contract | OK |
| G4 | SPEC:63, SPEC:140 | Typical | gate with a named flag (`target_release`, `--suite`) | true | Answer travels as that flag | OK |
| G4 | SPEC:63, SPEC:155 | Maximum/Overflow | cli-portify, three gates, one total `answer_wait` | true | Once per gate; total wait bounded | OK |
| G4 | SPEC:63, SPEC:260 | Sentinel Value Match | answer text containing `=`, quotes, newlines or flag-like tokens | true | `<gate-id>=<text>` implies a split at the first `=`; quoting is not stated (minor, N-12) | OK |
| G4 | SPEC:63 | Legitimate Edge Case | coordinator never answers or declines | true | `answer_wait` expiry or decline resolves blocked, then failed; on `ask` timeout the same message ID is resumed | OK |
| G5 outward action off unless a grant flag is in the brief | SPEC:69 | Zero/Empty | no grant flag | false | Every outward default off | OK |
| G5 | SPEC:69, SPEC:150 | One/Minimal | `--post-pr` alone | true | Posting on for auggie-review | OK |
| G5 | SPEC:69, SPEC:171, SPEC:259 | Typical | `/sc:task "commit the fix" --unattended --allow-commit` with the user's words quoted | true | Commit allowed; no flag means no commit (AC-2.4) | OK |
| G5 | SPEC:69, SPEC:210 | Maximum/Overflow | `--allow-commit` and `--allow-push` together | true | Both allowed; D4 (a) | OK |
| G5 | SPEC:69, SPEC:259, INV-A:38 | Sentinel Value Match | `--post-pr` with `--no-post-pr` | conflict | Usage error; stop before work; contract `failed`; nothing posted | OK |
| G5 | SPEC:171 | Legitimate Edge Case | TFEP incident report when `--allow-commit` is given | true | "Not committed in unattended mode" regardless | OK |
| G6 flag accepted only from the phase of the row | SPEC:126, SPEC:204, SPEC:252 | Zero/Empty | Phase 0, no command edited | false for all 37 | Brief uses 3.1 flags only (SPEC:78) | OK |
| G6 | SPEC:209, SPEC:252 | One/Minimal | Phase 1, one command from the P1 list | true | Accepts `--unattended` and `--report-dir` | OK |
| G6 | SPEC:78, SPEC:252 | Typical | Phase 1 done; brief passes `--unattended` to tdd (P2) | false | Coordinator is told not to; AC-1.1 asserts no P2 command accepts it yet | OK |
| G6 | SPEC:73, SPEC:142, SPEC:138, SPEC:134, SPEC:172, INV-B:271, INV-A:39 | Maximum/Overflow | a P1 parent (workflow, brainstorm) that invokes a child outside the P1 list (reflect P2, tasklist P2, the `task` skill in no phase) | child false | WC-13 requires the parent to pass `--unattended`; the phase rule forbids the child to accept it. Interim behaviour not stated | GAP |
| G6 | SPEC:162, SPEC:252 | Sentinel Value Match | `load`: in the P1 list but no flag and no section | n/a | AC-1.1 excludes it | OK |
| G6 | SPEC:375, SPCMD:22-23 | Legitimate Edge Case | a command that already carries the flag in the real repo (the supplied `/sc:spec-panel`) | true | Deferred: each phase plan re-reads the command first; AC-1.1 "none outside the list accepts it" would fail for it (N-09) | OK |

GAP rows and where they are folded: G1 row 4 into N-06; G2 row 4 into N-02; G2 row 6 into N-03; G3 row 5 into N-05; G6 row 4 into N-01. By FR-8 each is at least MAJOR and blocking.

#### Quantity Flow Diagram (FR-17 to FR-21)
Triggered: the spec has a multi-stage flow whose count changes (classification, phase assignment, nesting). Fowler annotated counts, Whittaker attacked the divergence points.

```text
[Source: 43 commands in cmd/ (SPEC:126)]
   --> [Stage 1: classify]
        --> [6 coordinator-only (SPEC:178)]                  excluded
        --> [37 worker-capable = 10 ready (3.1) + 27 change (3.2)]
              |
              v
        [Stage 2: phase assignment (SPEC:209-212)]
              P1 = 14 flag-accepting + load (usage line only) = 15 named
              P2 = 15 ; P3 = 4 ; P4 = 3 ; total 15 + 15 + 4 + 3 = 37
              flag-accepting commands when P1 ends = 14
              |
              +--> [Consumer A: AC-1.1 section check (SPEC:252): expects 14]                       OK
              +--> [Consumer B: AC-1.2 live check (SPEC:253): expects 14]                          OK
              +--> [Consumer C: P2/P3/P4 checks repeat AC-1.1 per list (SPEC:252)]                 OK
              +--> [Consumer D: WC-13 'pass --unattended to every command or skill you invoke'     <-- MISMATCH
                     (SPEC:73): commands that must accept the flag when P1 ends
                     = 14 + reflect + tasklist = 16
                     (+ task skill, task-builder, tech-research outside the 43, in no phase)]
              +--> [Consumer E: tasklist Stage 10.5 (SPEC:172): N reflect children need N          <-- MISMATCH
                     distinct report directories; WC-13 formula gives 1]
```

Divergence at Stage 2: 14 commands accept the flag when P1 ends, 16 or more would have to. Concrete scenario (FR-19): after P1 passes, `/sc:workflow "<change>" --handoff none --unattended --report-dir R` runs. Workflow's Wave 4 invokes `sc:reflect-protocol` once (`INV-B:271`). WC-13 says pass `--unattended` and `R/reflect/`; reflect converts in P2 (SPEC:138, SPEC:210) and by SPEC:204 does not accept the flag yet. 14 accept, 15 are needed. For tasklist with N = 4 phases, 4 reflect children share one `R/reflect/` directory: 4 contracts, 1 file (N-03). Both are dimensional mismatches: the first is graded CRITICAL under FR-19 (N-01), the second is the N to 1 collapse recorded as N-03.

### Findings by analysis bucket
Each finding gives issue, severity, expert, recommendation with rationale, priority and quality impact. `origin=` is `changed` when the text was touched by the revision.

=== REQUIREMENTS ANALYSIS ===

**N-04 (MAJOR, blocking; origin=changed). Crispin / Wiegers: four acceptance checks trip the refusal rule the revision added.**
- Issue: WC-4 says that `--unattended` without `--report-dir` makes the command stop before any work, write no file, and the worker settle `failed` (SPEC:64). AC-2.8 runs `/sc:cli-eval run --unattended` (SPEC:262), AC-3.3 `/sc:validate-tests --report <path> --unattended` (SPEC:266), AC-3.4 two workers each running `/sc:save --unattended` (SPEC:267), and AC-4.1 `/sc:implement <plan> --unattended` (SPEC:268). None carries `--report-dir`. AC-2.8 also gives no `--suite` or safety flags, which the cli-eval row requires or the run is blocked at the gate (SPEC:154), so it would end blocked before the long wait it is meant to observe. The old F-01 spelling of the flag and the new F-02 refusal were applied to the prose and to some ACs, not to these four.
- Wrong outcome: an implementer who follows WC-4 sees AC-3.4 fail (two refusals, no per-session files), AC-3.3 fail (no report file), AC-4.1 fail (no ledger halt recorded, no contract) and AC-2.8 end blocked; or removes the refusal rule to make the checks pass. P2, P3 and P4 cannot be signed off as written.
- Recommendation: add `--report-dir <dir>` (and for AC-2.8 `--suite` plus the safety flags) to each; re-grep every AC for `--unattended` without `--report-dir`. Rationale: a requirement and its acceptance check must agree (Wiegers).
- Priority: High. Quality impact: Testability +2, Consistency +1.

**N-05 (MAJOR, blocking; FR-8 from guard G3; origin=changed). Newman / Wiegers: the WC-5 validity rule fails every healthy worker whose report is not a WC-4 contract.**
- Issue: WC-5 defines a valid report as a non-empty YAML file with `command` and a status in the four values, and treats anything else as "no report" with `--outcome failed` (SPEC:65). WC-5 is not limited to workers run with `--report-dir`. Phase 0 runs three ready commands with no `--unattended` and no `--report-dir`, reporting "the command's own REPORT.md" (SPEC:91-97, SPEC:208, SPEC:251); the same holds for every 3.1 command before its phase (SPEC:78, SPEC:129). `/sc:troubleshoot` reports markdown `REPORT.md` (`INV-B:242`); `/sc:tdd` and `/sc:release-split` report a TDD file and a markdown report (`INV-B:222`, `INV-B:122`); workflow and adversarial write contracts whose status words are not recorded (`INV-B:272`, `INV-A:60`). The brief example for troubleshoot tells the worker to send `--report-path` but gives no `--outcome` rule. 7.2 step 3 requires that the report path "is the WC-4 contract path" (SPEC:238) and AC-0.4 says steps 1-3 pass (SPEC:251), which cannot hold when no contract exists.
- Wrong outcome: the Phase 0 smoke runs, which exist to test the decision (SPEC:44), either settle `failed` on a correct run, or the worker improvises the outcome. This is the F-05 scenario (R1:191) moved from the live check to Phase 0.
- Recommendation: scope the validity rule and step 3's contract-path condition to workers started with `--report-dir`; for pre-conversion workers state the outcome rule (outcome `succeeded` when the command finishes and its named report file exists, `failed` otherwise) and list it in the P0 brief template.
- Priority: High. Quality impact: Consistency +2, Testability +1.

**N-06 (MAJOR, blocking; FR-8 from guard G1; origin=changed). Nygard: WC-10 now forbids calls that WC-7 and E4 require.**
- Issue: WC-10 says "No single tool call made by a command may last longer than 4 minutes" (SPEC:70). WC-7 says a command's own Agent-tool fan-out "stays as it is" (SPEC:67) and E4 says commands keep their fan-out (SPEC:25). A foreground Agent-tool call blocks the worker's turn until its agents return (inferred from how the commands dispatch "in one message", `INV-A:35`, `INV-B:221`; the Agent tool's blocking behaviour is not documented in the workspace), and tdd's research wave, cleanup-audit's waves of 7-8 agents and adversarial's advocate round routinely take longer than 4 minutes. Synchronous runs such as `/sc:test` and `/sc:build` (`INV-B:234`, `INV-A:40`) have the same shape. Only cli-eval (AC-2.8) and pr-submit (AC-4.3) have a check (SPEC:286); no row tells any other command how to comply.
- Wrong outcome: an implementer either rewrites every fan-out into background jobs plus polling (contradicting WC-7 and SA-4's "additive" edits), or ignores WC-10 for all but two commands, so the rule exists only on paper.
- Recommendation: state which calls WC-10 covers (calls the command makes to wait on something external: poll, eval, Monitor) and say that foreground Agent-tool fan-out is exempt, with the heartbeat duty falling on the coordinator's `agentWait` and the worker's own checkpoints; or list the commands that must background their long runs.
- Priority: High. Quality impact: Consistency +2.

**N-12 (MINOR; origin=changed). Wiegers: the `--answer` grammar is not stated.** `--answer <gate-id>=<text>` (SPEC:63) says nothing on quoting, `=` inside text, duplicate or unknown gate ids, and the answer is free text that ends up in a command line next to the grant flags (SPEC:69). Add one sentence: split at the first `=`, quote the text as one argument, ignore or reject unknown ids. Priority Low.

**N-14 (MINOR; origin=changed). Wiegers: validation claims in the spec and the disposition describe the old text.** SPEC:12 ("This worker re-read 11 of the load-bearing locations") and SPEC:370 ("about 340 citations ... 9 defects") belong to `V1`; the revision added 22969 bytes and re-cited many lines without repeating either check, yet the header at SPEC:5 now says the document was revised in Task 6. `DISP:19` misplaces item 15 (`SPEC:370` for `SPEC:371`) and `DISP:10` says the placeholder grep returns nothing while it returns `SPEC:158`. Mark the two spec statements "as of V1" and fix the two disposition cites. Priority Low.

=== ARCHITECTURE ANALYSIS ===

**N-01 (CRITICAL, blocking; FR-19 dimensional mismatch and FR-8 from guard G6; origin=changed). Fowler: WC-13 and the phase gate cannot both hold in Phase 1.**
- Issue: WC-13 requires a command run with `--unattended` to pass `--unattended` to every `/sc:` command or skill it invokes, and AC-1.1 asserts a `Nested:` line in all 14 P1 sections (SPEC:73, SPEC:252). SPEC:204 says a command accepts the flag only in the phase that converts it, "never earlier". Workflow is P1 (SPEC:142) and always runs reflect in Wave 4 (`INV-B:271`, `INV-B:269`); reflect is P2 (SPEC:138). Brainstorm is P1 (SPEC:134) and optionally runs the tasklist skill in Wave 4 (`INV-A:39`); tasklist is P2 (SPEC:172). tdd (P2) runs the `task` skill (`INV-B:219`) and the `task-builder` and `tech-research` skills appear elsewhere (`INV-A:39`); none is among the 43 commands or in any phase. See the Quantity Flow Diagram: 14 accept, 16 or more would have to accept it.
- Wrong outcome: in Phase 1 the workflow worker passes `--unattended --report-dir R/reflect/` to a reflect that does not know the flag (it is rejected or ignored, and AC-1.2's live check on workflow fails or passes by accident), or the implementer drops the pass-through to satisfy SPEC:204 and then violates WC-13 and the `Nested:` assertion.
- Recommendation: restrict WC-13 to children already converted at the parent's phase, and state the interim rule for the rest (the parent calls the child with its present flags, as the 3.1 rows do for Phase 0, SPEC:208); or move reflect's flag acceptance into P1 alongside workflow. Skills outside the 43 need a stated scope (for tdd, "its own section resolves the nested asks", SPEC:140).
- Priority: High. Quality impact: Consistency +2, Testability +1.

**N-02 (MAJOR, blocking; FR-8 from guard G2; origin=changed). Nygard: the "new directory per attempt" rule has no delivery path to a retry worker.**
- Issue: WC-4 and 2.3 item 3 require the coordinator to pass "a new `--report-dir <dir>` for every attempt, retries included" (SPEC:64, SPEC:79). The command line is part of the Task spec (`task-create --spec "<brief>"`, SPEC:236); a retry is `worker-start --task <task_id> --retry-of <dispatch_id> --worktree ... --agent ...` (`CAPS:116`), whose shape carries no replacement text, and AC-2.7 repeats that form "with a new `--report-dir`" (SPEC:261). Orca says not to route around the retry boundary "with a new Run, Task, or unrelated Dispatch" (`CAPS:116`). Whether `worker-start` accepts new task text on a retry, or a Task spec can be edited, is not in the capabilities inventory.
- Wrong outcome: the retry runs the old command line, finds the first attempt's `return-contract.yaml` (or overwrites it, WC-3 treats overwrite as normal), and the stale-contract case R1:186 returns; or the coordinator creates a new Task and loses `--retry-of`.
- Recommendation: let the brief carry a base directory and have the worker append its own Dispatch ID (`<base>/<dispatch_id>/`), so the path is unique per attempt and known to the coordinator from the dispatch receipt; state what a command does when the directory already holds a contract. Mark the Orca mechanism UNVERIFIED until AC-2.7 is run.
- Priority: High. Quality impact: Consistency +1, Testability +2.

**N-03 (MAJOR, blocking; FR-8 from guard G2; origin=changed). Whittaker / Hohpe: the child report directory name is not unique.**
- Issue: WC-13 gives each nested command `<report-dir>/<child-command>/` (SPEC:73). Tasklist Stage 10.5 spawns N parallel reflect children (`INV-B:211`); its row says "its own report subdirectory to each reflect" without a name (SPEC:172).
- Wrong outcome: an implementer who follows the formula gives N reflects one directory; N contracts overwrite each other (parallel writers, WC-11) and tasklist reads whichever finished last.
- Recommendation: `<report-dir>/<child-command>-<k>/` with a stable `k` (phase number or invocation index), stated in WC-13 and in the tasklist row; AC-2.1 asserts it.
- Priority: High. Quality impact: Consistency +1.

**N-07 (MAJOR, not blocking; origin=changed). Newman / Hohpe: "no second copy" may starve readers of nested contracts.**
- Issue: under `--unattended`, commands that already write a contract "write it at `<report-dir>/return-contract.yaml` and write no second copy" (SPEC:64), and nested children write under `<report-dir>/<child>/` (SPEC:73). Adversarial's contract is "returned when invoked by another command" and real runs wrote it at `<output>/adversarial/return-contract.yaml` (`INV-A:60`); brainstorm calls adversarial in Wave 3 and writes `<output>/return-contract.yaml` itself (`INV-A:39`); the 3.1 row still names `<output>/adversarial/return-contract.yaml` as the P1 fix (SPEC:133, AC-1.4). Whether brainstorm reads the child's file from disk or from the inline return is UNVERIFIED, so this is a risk, not a proven break; hence not blocking.
- Recommendation: say that a parent reads a child's contract from the child's report directory under `--unattended`, and keep the fixed `<output>/adversarial/` path only for runs without the flag.
- Priority: Medium.

**N-08 (MAJOR, not blocking; origin=changed). Nygard: the coordinator procedure contradicts itself and overstates Orca's circuit breaker.**
- Issue: SPEC:84 says the coordinator "never stops, abandons or retries on absence of information" and then "for a silent worker ... sets its own limit"; a silent worker is exactly absence (`CAPS:125`). It also says a retry "is subject to Orca's three-failure circuit breaker (`CAPS:116`)", but `CAPS:80` records that a worker's own `failed` report does not count, and SPEC:342 says so. Retries after `worker_done --outcome failed` are therefore bounded only by the coordinator.
- Recommendation: say what the coordinator does when its own limit expires (ask the person; do not stop or release the worker), and state the retry bound the coordinator applies itself.
- Priority: Medium.

**N-09 (MAJOR, not blocking; origin=unchanged, baseline UNVERIFIED). Cockburn / Fowler: the supplied `/sc:spec-panel` text already has what section 3 says to add.**
- Issue: `command.md` carries `--output <file>`, `--report-dir <dir>`, `--unattended` (`SPCMD:22-23`) and an `## Unattended mode` section that cites `~/.claude/WORKER-CONTRACT.md` (`SPCMD:451-461`, `SPCMD:453`), whose contract text names only succeeded, blocked and failed (`SPCMD:457`). The spec lists spec-panel as P2 work, "add `--output <file>`" (SPEC:170), proposes writing `WORKER-CONTRACT.md` in P0 (SPEC:208), and AC-1.1 asserts that no command outside the P1 list accepts `--unattended` yet (SPEC:252). If the repo matches the supplied text, that assertion fails at P1 and the P2 row is stale. The spec records this as UNVERIFIED (SPEC:375) and defers it to each phase plan; that is honest but leaves a check that is known to be able to fail.
- Recommendation: make AC-1.1's "none outside the list accepts it" read "no command accepts it in a form that contradicts its row", and add a P0 step that diffs section 3 against the installed commands.
- Priority: Medium.

**N-11 (MINOR; origin=changed). Newman / Nygard: two WC-4 details are not implementable as written.** The atomic write is "a temporary name, then renames it" (SPEC:64), which needs a Bash tool; `/sc:explain` lists only Read, Grep, Glob, TodoWrite, Task (SPEC:158) and the validate-tests skill has neither Write nor Bash (`INV-B:262`). And "a command with its own version field keeps it" can leave `contract_version` absent, so a coordinator cannot tell the schema version of workflow's 1.1 contract. Say that a rename is best effort where no shell tool exists, and that `contract_version` is always added next to a legacy field. Priority Low.

**N-13 (MINOR; origin=changed). Nygard: the 4-minute cap bounds a call, not the heartbeat gap.** SPEC:345 says a 4.5-minute call "cannot push two heartbeats more than 5 minutes apart". With a 4-minute call started 2 minutes after a heartbeat, the next heartbeat is 6 minutes later unless the worker heartbeats before the call. WC-10 implies this ("so the session can heartbeat between them") but does not state it, and `CAPS:130` notes it is UNVERIFIED whether Orca uses heartbeat age at all. Add "heartbeat before any call longer than 1 minute". Priority Low.

=== CROSS-CUTTING (editorial) ===

**N-10 (MINOR; origin=unchanged text made stale by the revision). Cockburn: the 3.1 intro contradicts the phase rule.** SPEC:129 says the worker "reports the named file until Phase 1 adds the contract" and that "the only command changes are the small fixes". After F-03, reflect, release-split, tdd and troubleshoot convert in P2 (SPEC:138-141), and section 3's intro says every changed command gains the section and flags (SPEC:126). The four P2 rows in 3.1 do not mention the contract work. Priority Low.

**N-15 (MINOR; origin=changed). Editorial nits, one finding.** (a) D1's example uses `/sc:troubleshoot ... --unattended --report-dir` (SPEC:307) although troubleshoot accepts the flag only from P2 (SPEC:141, SPEC:78) and 2.4 says so (SPEC:91). (b) The `pr-submit` row puts the contract "beside `monitor-run-<PR>.jsonl`" (SPEC:164), which lives under `--output-dir`, while WC-4 puts it in `--report-dir`. (c) AC-0.5 is listed before AC-0.4 and AC-2.8 before AC-2.5 (SPEC:250-251, SPEC:262-263). (d) The AC-C1 pattern also matches prose ("the orca status line", tested), so a doc sentence in a command would fail the check. (e) WC-13 has only text assertions (SPEC:289). (f) The key `SPCMD` is cited at SPEC:346 and SPEC:375 but defined only in `R1:9`. (g) SA-2's last sentence is garbled ("a changed command ... inside the contract file", SPEC:197). Priority Low.

=== ADVERSARIAL ANALYSIS (James Whittaker) ===
Severity classes: CRITICAL (provably wrong), MAJOR (ambiguous or incomplete under attack), MINOR (inferrable). Each attack is tied to a finding.

**A-1 (N-01, CRITICAL). I can break this specification by a Sequence attack on the phase order.** The invariant at **SPEC:204 ("never earlier") and SPEC:73 (WC-13)** fails when **a P1 command invokes a child that converts later**. Concrete attack: **state 0: P1 passed; reflect still has no `--unattended`. Step 1: coordinator dispatches `/sc:workflow "<change>" --handoff none --unattended --report-dir R/attempt-1/` (allowed, workflow is in the P1 list). Step 2: Wave 4 invokes reflect; WC-13 demands `--unattended R/attempt-1/reflect/`. State 2a: reflect rejects the unknown flag, workflow ends `failed` after writing its plan. State 2b: the implementer omits the flag, the `Nested:` line of workflow's section then names reflect without passing it, and WC-13 is violated.** Recommendation: see N-01.

**A-2 (N-02, MAJOR). I can break this specification by a Sequence attack on WC-4/WC-6 with a retry.** The invariant at **SPEC:79 and SPEC:261** fails when **the retry reuses the Task spec**. Concrete attack: **state 0: Task T spec carries `--report-dir R/a1/`. Attempt 1 writes `R/a1/return-contract.yaml` with `status: failed`. Step 1: `worker-start --task T --retry-of D1`. State 1: the retry worker reads the same spec, so `--report-dir R/a1/`. State 2: the command either overwrites (the first attempt's evidence is gone, WC-6 broken) or finds a stale `failed` file; a coordinator that reads the path before the retry settles sees `failed` and abandons a healthy retry.** Recommendation: see N-02.

**A-3 (N-03, MAJOR). I can break this specification by an Accumulation attack on WC-13.** The invariant at **SPEC:73** fails when **a parent runs the same child more than once**. Concrete attack: **tasklist with 4 phases starts 4 reflects in parallel; each gets `R/reflect/`; four writers rename `return-contract.yaml` in one directory; the file that remains has the `command` field of one reflect, and tasklist reports 4 passes from 1.** Recommendation: see N-03.

**A-4 (N-04, MAJOR). I can break this specification by a Zero/Empty attack on the ACs.** The invariant at **SPEC:64 (refusal) against SPEC:262, SPEC:266-268** fails when **`--report-dir` is empty**. Concrete attack: **AC-3.4 starts two `/sc:save --unattended` workers; both stop at once with `failed` and write nothing; the check "two new per-session files" fails; the same trace for AC-3.3 and AC-4.1.** Recommendation: see N-04.

**A-5 (N-05, MAJOR). I can break this specification by a Sentinel Collision attack on `status`/validity.** The invariant at **SPEC:65 and SPEC:238-239** fails when **a legitimate report is not a WC-4 contract**. Concrete attack: **Phase 0: `/sc:troubleshoot "login fails"` finishes and writes `REPORT.md`; the worker applies WC-5: not YAML, no `command`, so "no report"; `worker_done --outcome failed`. The coordinator's step 3 sees a failed outcome on a good run and, per AC-0.4, "a failure here reopens section 1" (SPEC:251).** Recommendation: see N-05.

**A-6 (N-06, MAJOR). I can break this specification by a Divergence attack on WC-10 versus WC-7.** The invariant at **SPEC:70 and SPEC:67** fails when **a command's fan-out is a single foreground call**. Concrete attack: **`/sc:tdd` at the 6-agent tier starts its research wave as one message; the call returns after 9 minutes. WC-10 says no call may exceed 4 minutes; WC-7 says fan-out stays. Either reading breaks one of them.** Recommendation: see N-06.

**A-7 (N-07, MAJOR). I can break this specification by a Sentinel Collision attack on the contract file name.** The invariant at **SPEC:64 ("no second copy") and SPEC:133** fails when **a parent reads the child's old path**. Concrete attack: **brainstorm runs adversarial with the child directory `R/adversarial/`; adversarial writes only there; brainstorm looks at `<output>/adversarial/return-contract.yaml` (`INV-A:60`), finds nothing and reports the merge as missing. UNVERIFIED: whether brainstorm reads the file.** Recommendation: see N-07.

### Synthesis
Consensus points
- The revision is largely sound. Flag phasing (14 + 1 + 15 + 4 + 3 = 37), `--report-dir`, the ask protocol, grant flags, AC-C1 and the coverage table do what round 1 asked; the counts reconcile.
- Every blocking defect found here is an interaction between two revision rules, which is what a section-by-section revision tends to leave: nesting with phasing, attempt directories with Orca retry, validity with pre-conversion workers, the 4-minute cap with fan-out, and the new refusal with older ACs.
- The coordinator side (2.3) is the thinnest part: it carries the most new rules and the two internal contradictions (N-08).

Disagreements
- Fowler and Whittaker grade N-07 (starved nested readers) MAJOR; Hohpe would call it MINOR because the reader is UNVERIFIED. Left MAJOR, not blocking, under the Review Loop rule that an unestablished outcome does not block.
- Nygard would block N-08 (a coordinator that stops a live worker on its own timer); Wiegers holds it at MAJOR because the same paragraph forbids acting on absence. Left non-blocking.
- Wiegers wanted N-12 (`--answer` grammar) graded MAJOR under FR-9; the panel graded it MINOR because the split rule is implied by `<gate-id>=<text>` and the table row is specified.

Priority-ranked improvements: N-01, N-02, N-05, N-04, N-03, N-06 (blocking, in this order because N-01 and N-02 change the rules that N-03 and N-04 are written against), then N-07, N-08, N-09, then the minor items.

### Numbered new findings
15 new findings: 1 CRITICAL, 8 MAJOR, 6 MINOR in the experts' labels (N-01 CRITICAL; N-02 to N-09 MAJOR; N-10 to N-15 MINOR); 6 blocking (N-01 to N-06), 9 not blocking. Evidence paths are relative to the workspace root.

| # | Finding | Severity | Blocking | Origin | Spec section | Evidence (path:line) |
|---|---------|----------|----------|--------|--------------|----------------------|
| N-01 | WC-13 requires P1 parents to pass `--unattended` to children that accept it only in P2 or in no phase (FR-19: 14 accept, 16 or more would have to) | CRITICAL | yes | changed | 2.2 WC-13; 6; 7.3 AC-1.1 | SPEC:73, SPEC:204, SPEC:252, SPEC:134, SPEC:138, SPEC:142, SPEC:172; INV-B:271, INV-B:269, INV-B:219; INV-A:39 |
| N-02 | A new report directory per attempt cannot reach a retry worker, which reuses the Task spec (FR-8, guard G2) | MAJOR | yes | changed | 2.2 WC-4, WC-6; 2.3 item 3; 7.3 AC-2.7 | SPEC:64, SPEC:79, SPEC:236, SPEC:261; CAPS:116 |
| N-03 | `<report-dir>/<child-command>/` is not unique when a parent runs one child N times (FR-8, guard G2) | MAJOR | yes | changed | 2.2 WC-13; 3.2 tasklist | SPEC:73, SPEC:172; INV-B:211 |
| N-04 | AC-2.8, AC-3.3, AC-3.4, AC-4.1 use `--unattended` without `--report-dir` and trip WC-4's refusal; AC-2.8 also lacks `--suite` | MAJOR | yes | changed | 7.3 | SPEC:64, SPEC:154, SPEC:262, SPEC:266, SPEC:267, SPEC:268 |
| N-05 | WC-5 validity rule makes every non-contract or legacy report "no report"; P0 and pre-conversion workers settle failed (FR-8, guard G3) | MAJOR | yes | changed | 2.2 WC-5; 2.4; 6 P0; 7.2 step 3; 7.3 AC-0.4 | SPEC:65, SPEC:78, SPEC:91-97, SPEC:238, SPEC:251; INV-B:242, INV-B:272 |
| N-06 | WC-10 caps every tool call at 4 minutes but WC-7 and E4 keep foreground Agent-tool fan-out and long synchronous runs (FR-8, guard G1) | MAJOR | yes | changed | 2.2 WC-10, WC-7; 1.2 E4 | SPEC:25, SPEC:67, SPEC:70, SPEC:286; INV-B:221, INV-A:42, INV-B:234 |
| N-07 | "No second copy" may starve parents that read a nested contract at its old path | MAJOR | no | changed | 2.2 WC-4, WC-13; 3.1 adversarial | SPEC:64, SPEC:73, SPEC:133; INV-A:39, INV-A:60 |
| N-08 | Coordinator procedure contradicts itself (own limit vs never act on absence) and overstates the circuit breaker | MAJOR | no | changed | 2.3 | SPEC:84, SPEC:342; CAPS:80, CAPS:116, CAPS:125 |
| N-09 | The supplied `/sc:spec-panel` already has the flags, section and a contract file the spec plans to add; AC-1.1 could fail at P1 (baseline UNVERIFIED) | MAJOR | no | unchanged | 3.2 spec-panel; 6 P0; 7.3 AC-1.1 | SPEC:170, SPEC:208, SPEC:252, SPEC:375; SPCMD:22-23, SPCMD:451-461 |
| N-10 | 3.1 intro still says the contract arrives in Phase 1 and that only small fixes change | MINOR | no | unchanged | 3.1 | SPEC:126, SPEC:129, SPEC:138-141 |
| N-11 | Atomic rename needs a shell tool some commands lack; `contract_version` can be missing next to a legacy version field | MINOR | no | changed | 2.2 WC-4 | SPEC:64, SPEC:158; INV-B:262, INV-B:272 |
| N-12 | `--answer` grammar (quoting, `=`, duplicates, unknown ids) is not stated | MINOR | no | changed | 2.2 WC-3 | SPEC:63 |
| N-13 | The 4-minute cap does not bound the heartbeat gap unless the worker heartbeats before a long call; SPEC:345 overstates | MINOR | no | changed | 2.2 WC-10; Decisions | SPEC:70, SPEC:345; CAPS:130 |
| N-14 | Validation claims at SPEC:12 and SPEC:370 describe V1; two cosmetic errors in the disposition | MINOR | no | changed | header; UNVERIFIED 14; DISP | SPEC:12, SPEC:370, SPEC:371; DISP:10, DISP:19 |
| N-15 | Editorial nits: D1 example, pr-submit row location, AC order, AC-C1 prose false positive, WC-13 static-only check, `SPCMD` key, SA-2 wording | MINOR | no | changed | 9 D1; 3.2; 7; 5 | SPEC:307, SPEC:164, SPEC:250-251, SPEC:262-263, SPEC:289, SPEC:346, SPEC:375, SPEC:197 |

Open blocking findings: N-01, N-02, N-03, N-04, N-05, N-06 (new), and the two round-1 findings still open, F-02 and F-05, which are covered by N-02 and N-05.

## Decisions
| Decision | Options | Rationale |
|---|---|---|
| Review header | `review: 1 of 3`; `review: 2 of 3` | `review: 1 of 3`. The invocation carried no `--re-review` and no `--baseline`, and the coordinator supplies the count (`SPCMD:258`, `SPCMD:261`); without them the run is a first review. The brief's round-1 report is used as input to Part 1 only. |
| Brief says any finding is FAIL; command says minor findings never block | follow the brief; follow the command | The command (`SPCMD:264`: a brief "may not grade a minor finding as blocking"). Verdict is FAIL regardless, from six blocking findings. |
| Scope of the critique | changed lines only; whole document | Whole document, with an `origin=` tag, because no baseline flag was passed; 13 of 15 findings came from changed text anyway. |
| Citation check scope | every citation in the spec; citations in changed lines (`diff V1 SPEC`) | Changed lines, as the brief asks, plus the disposition's self-citations. `V1` is in the workspace, so the diff does not leave the sandbox. |
| Guard selection | every threshold in the spec; the six guards that decide section 2 and 6 behaviour | The six listed in Part 3. Acceptance-check thresholds add rows without new findings. |
| GAP versus OK for the `--answer` grammar and the heartbeat sequence | GAP (blocking by FR-8); OK with a minor note | OK with a minor note (N-12, N-13): the behaviour is implied by the text, and a stricter grade would block on a drafting nit. Stated so a reader can disagree. |
| Round-1 `\|` claim in AC-C1 | accept the reviewer's claim; accept the disposition's rejection | The disposition's rejection stands for the rendered table; the fenced block makes it moot. I ran the block's pattern on sample text to confirm it matches. |
| Use of `command.md` as evidence | ignore; cite for the command's own text only | Cited only for what that command's text already says (N-09, G6 row 6), never as the repo baseline. |
| Python | `uv run`; system `python3` | System `python3` was used for a few small text edits to this report file in the sandbox; no repo code was run, so the `uv run` rule for repo Python does not apply. |

## UNVERIFIED in this review
1. Every `src/`, `~/.claude`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...` and Orca-JS citation in the spec: checked only against the inventory line that quotes it (Part 2).
2. Whether `worker-start --retry-of` accepts replacement task text, or a Task spec can be edited (N-02). Not in `CAPS`; needs the Orca CLI.
3. Whether brainstorm reads a child adversarial contract from disk or from the inline return (N-07).
4. Whether the Agent tool blocks the calling turn for the whole fan-out in the commands' dispatch pattern (N-06). Assumed from standard behaviour; no workspace line states it.
5. Whether the repo's command baseline matches section 3, in particular `/sc:spec-panel` (N-09). `command.md` is the only text in the sandbox.
6. Which copy of `sc-pr-submit-protocol/SKILL.md` carries the top-level rule at `:37-39` (src) or `:47-49` (home-installed, `CAPS:161`).
7. The `status` words of the five existing contracts (F-05 residual); only workflow's `failed` is recorded (`INV-B:272`).
8. No live check from spec section 7 was run; no Orca runtime exists in the sandbox.

## Reviser brief
Blocking finding ids only: N-01, N-02, N-03, N-04, N-05, N-06.
Rules for the reviser (the reviser reads this report, not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Report the byte size of the spec before and after.

verdict: FAIL
