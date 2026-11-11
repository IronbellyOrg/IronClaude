# Spec panel review, round 3: orca-worker-contract-spec.md

review: 1 of 3

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (independent re-review, Task 9) |
| Spec under review | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, revision 2 (346 lines, 90054 bytes by `wc`), not edited by this review. Round 2 read revision 1 (326 lines, 71195 bytes, kept at `specs/history/spec-v2.md`). `diff` of the two shows 152 changed diff lines |
| Review count | The invocation carries no `--re-review` and no `--baseline`, so Review Loop bullet 1 makes this run a first review of the full document and the header is `review: 1 of 3` (round 2 did the same). The coordinator keeps the real count (this is the third report on this spec) and the saved copy. The per-finding resolution table below is added because the brief asks for it; origin (changed or unchanged by revision 2) is given per finding as extra information |
| Prior reports | `review/spec-panel.md` (round 1, blocking 1-14), `review/spec-panel-round2.md` (blocking N1-N5, notes N6-N18, citations C1-C11), `review/disposition-round2.md` |
| Review date | 2026-11-10 |
| Panel (review order) | Wiegers (lead), Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin (guard-table completeness) |
| Active focus | requirements, architecture. `--focus correctness` is not active, so no State Variable Registry. The Guard Condition Boundary Table and the Quantity Flow Diagram are produced because the spec contains guards and multi-stage counts |
| Grading | Review Loop bullet 2: CRITICAL and FR-8/FR-9 findings are blocking; MINOR is minor; a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce, otherwise minor. FR-19 makes a count mismatch CRITICAL. The brief says any finding of any severity is FAIL. Review Loop bullet 7 lets a brief narrow the scope but not grade a minor finding as blocking, so this report grades by bullet 2 and the verdict follows the open blocking findings. Here both rules give FAIL |

Citation shorthand. `SPEC:N` = line N of the revised spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `V2:N` = line N of `specs/history/spec-v2.md`. `R2:N` = line N of `review/spec-panel-round2.md`. `D2:N` = line N of `review/disposition-round2.md`. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `CMD:N` = line N of `command.md`, the `/sc:spec-panel` definition that sits in this run's sandbox directory next to `ws/` (outside the workspace, inside the sandbox; I read it as the brief directs). New findings of this report are `R3-1` to `R3-14`.

Verification scope. What exists: the workspace (`ws/`) holds the revised spec, two older spec copies, the README, the three inventories, the round-1 and round-2 reports and both dispositions. It holds no `src/`, no `CLAUDE.md`, no `tests/`, no `Makefile`, no `pyproject.toml`, no `.dev/evals/`, no `.dev/codegraph-migration/`, and the sandbox `~/.claude` is an empty `rules/prompts` folder. `orca-ide` and `orca` are not on the path of this sandbox and I ran no Orca command. So the brief's step "re-read each citation against the live file or Orca guide output" cannot be done for any `src/`, `cmd/`, `sk/`, `ag/`, `CLAUDE.md`, `pyproject.toml`, `.dev/evals/`, `.dev/codegraph-migration/` or Orca-output citation: each is checked only against the inventory or capabilities line that quotes it, and the result column says so. What I could do and did: (1) check every inventory, capabilities, README and round-2 line that revision 2 added or changed, from a citation-token diff of V2 against the spec (26 new citation tokens, 5 removed) and from the row-by-row diff (152 changed lines); (2) check each spec statement about an inventory against that inventory's text; (3) check the one live file I have, `CMD`, against the spec-panel row; (4) run the spec's shell and Python acceptance snippets on sample text (stdin and process substitution only, nothing written; `python3 -I` with PyYAML 6.0.1, because the sandbox has no `uv` project). README rules ("Use `uv run`") are followed in the report's recommendations, not in this sandbox run.

## Part 1. Resolution tables

Rule used: `resolved` = the revised spec text, read in the spec and not in `D2`, closes the wrong outcome the finding named. `open` = that outcome is still reachable. `regressed` = a finding that the prior report marked resolved fails again. A residual weakness found in a resolved fix is raised as a new finding (`R3-n`), not re-opened. The disposition was used only to find where to look.

### 1A. Round-2 findings N1-N18

| # | Round-2 finding (short) | Status | Evidence in the revised spec (checked in the spec text) | Residual |
|---|---|---|---|---|
| N1 | WC-4 promised a contract path known before dispatch in every case; 11 rows gave no place, 2 no flag | resolved | The false sentence is gone (`grep -c 'every other case'` prints 0). WC-4.1 has four cases (SPEC:64). I re-derived the 36 section-bearing rows: 20 rows gain `--report-dir` (19 in 3.2, plus index-repo SPEC:94), 3 use the file-stem rule (tdd SPEC:98, init-lite SPEC:95, validate-tests SPEC:133), 3 name a fixed or generated place (cleanup-audit SPEC:93, workflow SPEC:100, implement SPEC:117 "beside the ledger"), 10 use an existing directory flag (adversarial with its fixed `adversarial/` subdirectory SPEC:91, brainstorm, auggie-review, pr-submit, post-release, reflect, release-split, troubleshoot, roadmap, validate-roadmap); 20+3+3+10 = 36 | The existing output-flag names of reflect, troubleshoot, release-split, roadmap and validate-roadmap are still not stated (SPEC:96, 97, 99, 126, 132); the spec marks each UNVERIFIED and sends the reading to P2 or P3, which is honest. Nested callees are not covered: R3-3 |
| N2 | AC-0.4 and WC-5 undefined for P0 smoke runs (no YAML contract yet) | resolved (named case) | WC-5.2 (SPEC:65) gives the rule for a command without a WC-4 contract; 3.1 intro restated (SPEC:87); 7.2 steps 3-4 branch on it (SPEC:221-222); AC-0.4 restated (SPEC:233) | The fallback in WC-5.2 fails open for legacy status vocabularies and uses an undefined "halt or STOP line" test: R3-2 (this also regresses round-1 finding 12 for legacy contracts, see 1C) |
| N3 | WC-6 sentence 1 (fresh directory) contradicts sentence 3 (same path) | resolved | WC-6 (SPEC:66) now says a command with no resume flag re-runs in place, defines the term, handles generated-name commands and fixed-location commands. `grep 'fresh dir'` prints nothing; the Resume column reads "re-run in place" (rows SPEC:91, 94-96, 99, 107-119, 122-123, 127-133), "Fresh package each run" (workflow SPEC:100) and "fresh file" (research SPEC:124), each consistent with WC-6 | none |
| N4 | Same output location for two Tasks: stale-file removal and mtime-only staleness test | resolved (as named) | Duty "One output location per Task" (SPEC:78); WC-4.4 limits the removal to "an earlier attempt of its own Task" (SPEC:64); step 4 compares `command` (SPEC:222). I re-ran the assertion on six sample documents (see 2C): the sibling-contract case now fails as intended | The `command` equality is exact-string, and conflicts with WC-3's re-invocation and with how the command renders its own line: R3-1 |
| N5 | WC-2 precedence vs the research row: `--strategy intent` stalls or is ignored | resolved | WC-2.2 exception and WC-2.5 (SPEC:62); research row forces `planning` and refuses `intent` and `unified` (SPEC:124); AC-2.6 (SPEC:242). INV-B:129 supports "no default strategy stated" | WC-2.5's qualifier ("generated at run time") leaves explicit `--remediation-offer` under the precedence rule: R3-7. AC-2.6's literal command line omits the output flag: R3-9 |
| N6 | 240 s limit with no means for one long build, test or eval call | resolved | WC-10 (SPEC:70); build row SPEC:109; test row SPEC:131; P1 scope SPEC:184; AC-1.2 transcript check SPEC:236; item 22 SPEC:345 states the feasibility is UNVERIFIED | none |
| N7 | workflow-to-reflect hand-over had no owning phase | resolved | P2 row adds "one added line in workflow's section" (SPEC:185); 3.3 row says so (SPEC:145) | none |
| N8 | 3.3 omitted four chains | resolved | Four rows added (SPEC:147-150). Each evidence cite checked: INV-B:211 (tasklist Stage 9, `sc:task --compliance strict`), INV-B:154 (roadmap `sc:save` each wave, `SKILL.md:316,420`), INV-B:151 (roadmap adversarial), INV-B:91 (pr-submit troubleshoot per finding, one auggie-review fallback) all say what the rows say | The table's callee mapping for the older tdd row is wrong: R3-4. The new rows give no callee output location: R3-3 |
| N9 | Support check reads only the coordinator's filesystem | resolved | One sentence added, with the `--on` case (SPEC:80); CAPS:128 supports the remote-worker premise | none |
| N10 | WC-9 sentence and class list differed; web search status | resolved | The sentence and the list are the same six classes (VM, real-target install, commit, push, PR, GitHub post; SPEC:69); web search and paid eval runs are stated to be outside WC-9 and the cli-eval row gates the eval (SPEC:112) | none |
| N11 | Output-location validity unspecified | resolved | WC-4.2 (SPEC:64) refuses an uncreatable or unwritable location, one inside `.git/` or under the distributable `.claude/` folders, before any work, chat only. Matches CMD:456 except that CMD also names `.codegraph/` | No acceptance check covers the refusal: R3-11 |
| N12 | Census, E5 and AC-C1 baseline possibly stale | resolved (conditional, as far as the evidence allows) | E5 now carries the date and the doubt (SPEC:27); P0 step 0 re-runs the grep, the census and `import yaml` (SPEC:183); SA-2 says exclusions are corrected from that result (SPEC:172); AC-0.5 (SPEC:234); item 23 (SPEC:346). The three commands are in neither inventory (I grepped `sc:issue`, `sc:graph`, `sc:impact` in `ws/`: 0 hits in the three inventories; only the spec and the two round-2 files mention them. That they exist rests on the session skill list, which is not a workspace file, so it stays UNVERIFIED here) | The list of sections to correct is incomplete: R3-13 |
| N13 | AC-C5 and AC-0.3 saw committed changes only | resolved | Code block 2 diffs the working tree against `git merge-base master HEAD` (SPEC:214). I ran the two `grep` stages on sample diff text: removed prose, removed bullet `--- x` and removed fence `----` print; only `--- a/` is hidden. `git diff <commit> -- <path>` includes uncommitted edits (git semantics, not run) | `master` may be a stale local ref: R3-10 |
| N14 | AC-1.2 gave every P1 command the same flags | resolved | AC-1.2 (SPEC:236) now names per-row flags and examples; AC-2.3 (SPEC:241) likewise | none |
| N15 | spec-panel row and WC-2/WC-4 disagree with the installed spec-panel section; one flag name with two meanings | resolved (reconcile deferred, explicitly) | New directory flag is `--report-dir` everywhere (SPEC:64, 128, 314); spec-panel row says P2 reconciles with the installed section (SPEC:128); WC-2.4 allows a row to record a mode that does not wait (SPEC:62). I checked the description of the installed section against `CMD:456-458`: `--report-dir`, contract at `<report-dir>/return-contract.yaml`, no person-mode flag refused, `--mode socratic` writes its questions into the report, all as the row says | The reconcile list omits differences that `CMD` shows: R3-6 |
| N16 | AC-2.2 vs WC-3's optional `ask` | resolved | AC-2.2 states that the test brief forbids `ask` (SPEC:240) | none |
| N17 | WC-2 and WC-4 not atomic | resolved | Sub-ids WC-2.1-2.6, WC-4.1-4.6, WC-5.1-5.2 (SPEC:62, 64, 65); old labels kept; no stale reference found (`grep 'WC-4 (ii)\|WC-4 iii'` prints 0) | none |
| N18 | Revision text without a finding id | resolved | Ids present on the tdd row (SPEC:98), post-release row (SPEC:121), P0 row (SPEC:183) and AC-2.2 (SPEC:240) | none |

Result: N1-N18 are all resolved as named in the spec text (18 of 18). Two of the fixes carry a new defect that blocks (N2 gives R3-2, N4 gives R3-1) and N1 leaves a gap at the nested-call boundary (R3-3).

### 1B. Round-2 citation findings C1-C11

| # | Round-2 citation defect | Status | Evidence in the revised spec | Residual |
|---|---|---|---|---|
| C1 | pr-submit poll-then-sleep structure asserted | resolved | WC-10 says the inventory gives only "600 s per wait over several rounds" and that the round structure "is this spec's reading", UNVERIFIED (SPEC:70); pr-submit row (SPEC:122) and item 12 (SPEC:335) agree; P4 measures first | The adjective "default" in "`--timeout` default of 600 s" (SPEC:122) and "600-second default budget" (SPEC:280) is not in INV-B:95 or INV-B:299 (they say "up to `--timeout` 600 s per wait"): R3-14 |
| C2 | Preamble cited to `CAPS:47` | resolved | SPEC:79 now cites `CAPS:76`, `CAPS:78`, `CAPS:148` for the preamble and `CAPS:47` for argv | "Task text inside a preamble" is slightly stronger than CAPS:78 ("fresh preamble and Task block"): R3-14 |
| C3 | Post-release line 292 unwitnessed | resolved | Dropped, with a note (SPEC:121); the remaining list (71-75, 95-99, 129-131, 221-235, 266-276, 324, 340, 351) matches INV-B:79, 82-84 | none |
| C4 | `SKILL.md:151-152` widened | resolved | WC-10 cites `:151` only (SPEC:70); INV-A:65 cites `:151` | none |
| C5 | Three ranges for one pr-submit fact | resolved | `41-64` at SPEC:70, 122, 280; `46-48` survives only in item 12 as the thing with no witness (SPEC:335) and, correctly, for roadmap at SPEC:126 | none |
| C6 | `--post-pr` assumed to exist | resolved | WC-9, auggie-review row and P2 scope call it a new flag that P2 adds (SPEC:69, 108, 185) | none |
| C7 | Tasklist "inside Claude Code's nesting limit" | resolved | Claim removed; row and item 21 state the nesting is UNVERIFIED (SPEC:130, 344). `INV-A:14` no longer appears in the spec | The new cite `INV-B:322` for "nested spawning is UNVERIFIED" is wrong (that line is about who answers the remediation offer): R3-5 |
| C8 | E2 "and answered" | resolved | E2 quotes `CAPS:49` and says the quote does not show an answer (SPEC:24); no "answered" remains in the spec (grep prints nothing) | none |
| C9 | PyYAML `pyproject.toml:38` | resolved | Claim removed; P0 step 0 runs `uv run python -c "import yaml"` with `uv run --with pyyaml` as fallback (SPEC:222, 183, 234); item 20 (SPEC:343) | none |
| C10 | E5 and AC-C1 baseline | resolved | Through N12 (above) | none |
| C11 | Unwitnessed "re-read" statements | resolved | Marked UNVERIFIED in the conventions line (SPEC:13) and item 14 (SPEC:337) | none |

Result: 11 of 11 resolved as named; three new citation weaknesses are raised below (R3-5, R3-6, R3-14).

### 1C. Round-1 blocking findings 1-14: regression check against revision 2

Revision 2 rewrote WC-2, WC-4, WC-5, WC-6, WC-9, WC-10, the 3.1 and 3.2 rows and 7.2. For each round-1 blocking finding I re-read the text that resolved it.

| # | Status after revision 2 | Note |
|---|---|---|
| 1 (phase lists) | resolved | AC-1.1 lists (SPEC:235); counts conserve: 14 + 15 + 4 + 3 = 36 = 37 - `load` |
| 2 (flag per phase) | resolved | SPEC:179, 183-187, 321 |
| 3 (retry, stale contract) | resolved | WC-4.4 and WC-6 now agree (N3) |
| 4 (placement) | resolved | WC-4.1 |
| 5 (start instruction) | resolved | SPEC:79 |
| 6 (support check) | resolved | SPEC:80 |
| 7 (propagation) | resolved | WC-2.6 and 3.3; but see R3-3 and R3-4 for what the table omits and mislabels |
| 8 (regex) | resolved | code block 2 |
| 9 (AC-C1) | resolved | code block 1; I ran it on sample lines: a `sc:issue`-style line `orca worktree create ...` is printed, the same text in `WORKER-CONTRACT.md` is not, `ORCA orchestration` (upper case) is not |
| 10 (240 s) | resolved | WC-10 |
| 11 (semantics of the switch) | resolved | SPEC:53, 62, 64 |
| **12 (WC-5 coverage)** | **regressed (legacy contracts only)** | Round 1 required that a `status` outside the four values maps to `failed`. WC-5.2 now sends a legacy contract with another vocabulary to a rule that returns `succeeded` when the file is non-empty and no "halt or STOP line" shows (SPEC:65): R3-2 |
| 13 (WC-9 authorization) | resolved | SPEC:69, 81 |
| 14 (precedence, several gates) | resolved | WC-2.2, 2.3, 2.5 |

### 1D. Round-1 notes 15-24 (not revised by rule)

| Note | Status | Note |
|---|---|---|
| 15 WC-1/3/12 no phase owner | open, unchanged | SPEC:61 still "well inside the readiness limit" |
| 16 P0 builds before it tests | open, unchanged | SPEC:183 lists deliverables before the smoke runs |
| 17 Tasklist nesting stated as fact | resolved by C7 | SPEC:130 |
| 18 `partial` maps to `succeeded` | open, unchanged | SPEC:75 gives no "check status before starting dependents" step |
| 19 "Phases 1-3 need no user decision" vs D4 | open, unchanged and slightly stronger | the new P2 flag `--post-pr` (SPEC:185) depends on D4; section 9 says phases 0-3 may proceed on the recommendations (SPEC:266) |
| 20 AC-1.3 "scratch worktree" | open, unchanged | SPEC:237 |
| 21 AC-2.4 `--jq length` | open, unchanged | SPEC:243 |
| 22 Legacy status vocabularies never inventoried | open, and now acted on by WC-5.2 | R3-2 |
| 23 Brainstorm answers its own questions | open, unchanged | SPEC:92 |
| 24 No branch for a worker that dies without `worker_done` | open, unchanged | SPEC:75 |

## Part 2. Citation-check table

Scope. A citation-token diff of V2 against the spec gives 26 citation tokens added and 5 removed by revision 2 (removed: `INV-A:14`, `SKILL.md:151-152`, the post-release list with `292`, two pr-submit ranges starting `46`). Added or re-worded: `CAPS:49`, `CAPS:78`, `INV-A:38`, `INV-A:45`, `INV-B:91`, `95`, `122`, `129`, `134`, `144`, `151`, `152`, `154`, `210`, `211`, `212`, `252`, `299`, `314`, `322`, `review/spec-panel-round2.md:238`, `sk/sc-cli-eval-protocol/SKILL.md:151`, the post-release list, the pr-submit list, `sk/sc-roadmap-protocol/SKILL.md:316,420`, `sk/sc-tasklist-protocol/SKILL.md:1614`. I also checked the older citations in every row that revision 2 re-wrote. Live files and Orca output are not in the sandbox (see Verification scope), so "confirmed" below means: the spec wording is supported by the inventory, capabilities, README or round-2 line it cites. It does not mean the underlying `src/` line was re-read.

### 2A. Wrong, overstated, stale or loose citations

| ID | Spec location | Citation and claim | Check | Result |
|---|---|---|---|---|
| X1 | SPEC:130 (tasklist row), SPEC:344 (item 21) | "whether such nested spawning works is UNVERIFIED (`INV-B:210`, `INV-B:314`, `INV-B:322`)" | INV-B:210 (b) says UNVERIFIED whether nested spawning works: yes. INV-B:314 (item 1) says whether an Agent-tool subagent can spawn agents is unknown and "Affects `/sc:tasklist` (b)": yes. INV-B:322 is item 8, "Who answers the reflect remediation offer that `/sc:tasklist` Stage 10.5 triggers inside subagents": a different question. Round 2 (C7, `R2:67`) made the same mistake and revision 2 copied it | Overstated cite (R3-5) |
| X2 | SPEC:128 (spec-panel row) | A copy "seen in round 2 uses `--report-dir`, writes the contract to `<report-dir>/return-contract.yaml`, refuses no person-mode flag and lets `--mode socratic` write its questions into the report (`review/spec-panel-round2.md:238`)" | The behaviour is correct against `CMD:456-458`. `R2:238` supports `--report-dir`, the person-mode point and the socratic point (it cites CMD:456 and CMD:458); the contract path `<report-dir>/return-contract.yaml` is at CMD:457, not at `R2:238` | Loose cite, behaviour confirmed (R3-6) |
| X3 | SPEC:128 | `cmd/spec-panel.md:22,34-35,222,451,455` | Against `CMD` (the live definition I have): 22 is the Usage line (matches); 34-35 are steps "Synthesize" and "Improve" (the TDD `target_release` question the row cites from the inventory is at CMD:36-37); 222 is the Context7 bullet (Write is CMD:224); 451 is the `## Unattended mode` heading, not "Will Not: Modify specifications" (that line is at CMD:475); 455 is the "Switch" bullet, not "Expert review document" (CMD:479-480). The inventory read an older file (INV-B:179-185, dated 2026-11-02); the line numbers are stale for the file a P2 implementer will edit | Stale against the live file (R3-6) |
| X4 | SPEC:122, SPEC:280 | pr-submit "`--timeout` default of 600 s" and "600-second default budget" | INV-B:95 and INV-B:299 say "waits up to `--timeout` 600 s per wait" and "600 s per wait". Neither says 600 s is the default | Unwitnessed adjective (R3-14) |
| X5 | SPEC:79 | "Orca places the Task text inside a preamble that carries the Task and Dispatch IDs (`CAPS:76`, `CAPS:78`, `CAPS:148`)" | CAPS:148 supports "a preamble with Task and Dispatch IDs"; CAPS:78 says "a fresh preamble and Task block"; CAPS:76 says injected preambles carry the `--from` value. "Task text inside" is an inference from "Task block" | Slightly stronger than the source (R3-14) |
| X6 | SPEC:64 (WC-4.2) | refusal for a location "under the distributable skill, agent or command folders of a `.claude/` folder (SA-5)" | SA-5 (SPEC:175) says `.claude/` copies come from `make sync-dev` and are never staged; it does not forbid writing there. The rule that matches is CMD:456. `CLAUDE.md` is not in the workspace | Loose cite (R3-14) |

### 2B. Citations added or changed by revision 2 and confirmed against workspace files

| File | Lines cited | What the line says | Supports the spec claim |
|---|---|---|---|
| `CAPS` | 47, 49, 148 | argv injection; EVIDENCE.md:45 quoted as "returned after 34s, `state: ready, stage: input_accepted`"; preamble with Task and Dispatch IDs | SPEC:24 (E2, no "answered"), SPEC:79: yes |
| `CAPS` | 52, 129, 125, 130, 128 | waiting worker is healthy; absence never authorizes stop; heartbeat cadence from the preamble; `--on` workers | SPEC:46, 62, 70, 80: yes |
| `CAPS` | 72-74, 76-77, 79, 80, 116 | `--report-path` rules, outcome mandatory, report is a pointer, own `failed` does not trip the breaker, retry and circuit breaker | WC-4.6, WC-5, WC-6, Decisions: yes |
| `CAPS` | 107-113, 115, 145-149 | one release decision; placement; executable name, `runtime_unavailable`, no preamble no lifecycle | 2.3, WC-11, R2, R4, SA-2: yes |
| `INV-A` | 35, 38, 44, 45, 53, 60-62, 65, 68, 96, 97 | rows and notes for adversarial, auggie-review, cli-eval, cli-portify, index-repo; main-blocker and contract-file summaries | the 3.1 and 3.2 Evidence columns and C6: yes |
| `INV-A` | 35-55 (rows), 3, 73, 106, 113, 118, 120 | per-command rows (row index = spec row), 21 commands, 5/13/3 summary, citation check, UNVERIFIED lines | row mapping and counts: yes |
| `INV-B` | 91, 95, 299 | pr-submit fan-out, "600 s per wait over several rounds", heartbeat row | WC-10, pr-submit row, 3.3: yes (except the word "default", X4) |
| `INV-B` | 112, 122, 129, 134, 144, 242, 252 | reflect default dir with timestamp; release-split default dir; research has no default strategy; web search in research and review-translation; troubleshoot contract only with `--caller task-unified`; validate-roadmap `<OUTPUT_DIR>` | 3.1 and 3.2 "Brief must pass", WC-9, N10: yes |
| `INV-B` | 151, 152, 154, 210, 211, 212, 269, 271, 272, 314 | roadmap adversarial; roadmap artifacts; roadmap `sc:save` each wave; tasklist nesting UNVERIFIED; Stage 9 `sc:task`; `TASKLIST_ROOT`; workflow Wave 4 reflect without `--remediate`; workflow contract | 3.3 rows, tasklist and roadmap rows: yes (322: X1) |
| `INV-B` | 31-52 (rows), 57-65 ... 267-275 (notes, 20 ranges), 3, 278, 285-287, 289-301, 311, 320, 323 | per-command rows and notes; summary and gate tables; decisions; UNVERIFIED | Evidence column of every row in 3.1 and 3.2 and sections 4, 8, 9: yes. I checked all 22 note ranges against the note headings: each begins at the command named |
| `README` | 6, 11-17, 12, 30, 31 | goal; evidence list; PR #329; planning only; no commits, pushes, PRs or GitHub comments | E3, WC-9, section 4 git row, non-goal 10: yes |
| `CMD` (live `/sc:spec-panel` definition) | 22-23, 451-461 | Usage line with `--unattended`, `--report-dir`, `--improve`; `## Unattended mode` section | The spec-panel row's description of the installed section: yes (X2, X3 for the line numbers) |
| `R2`, `D2` | `R2:238`, `R2:305-328`, `D2:18-52` | N15 text; the findings list; the disposition rows | the spec's pointers to them: yes (X2) |

### 2C. Checks I ran (stdin and process substitution only; nothing written)

| Check | Input | Result |
|---|---|---|
| Step-4 assertion of SPEC:222 (`python3 -I`, PyYAML 6.0.1; the spec's statement that it was run on five documents is consistent with my run) | matching contract; same contract with `command` rendered without the `/sc:analyze` prefix; contract written by a worker that re-invoked the command with an answer flag (WC-3); same command line with quotes escaped and one extra space; legacy contract with no `command` key; `command: /sc:tdd fix: login --unattended` unquoted | PASS; FAIL; FAIL; FAIL; FAIL; FAIL (the last is a YAML parse error, so WC-5.1 would also map it to `failed`). This is the evidence for R3-1 |
| AC-C1 pipe (SPEC:205-209) | five sample `path:line:text` lines | prints the `sc:issue`-style line `orca worktree create ...` and `orca terminal list`; does not print `WORKER-CONTRACT.md`, `ccsession-tag` or upper-case `ORCA orchestration` |
| Code block 2 (SPEC:214) `grep` stages | sample diff text | prints removed prose, removed `--- x` bullet and removed `----` fence; hides only the `--- a/` header. `git diff <commit> -- <path>` including uncommitted edits is git semantics, not run |
| Counts | spec rows and inventory summaries | 43 = 21 + 22; 10 ready (5 + 5), 27 needs-change (13 + 14), 6 coordinator-only (3 + 3); phases 14 + 15 + 4 + 3 = 36 = 37 - `load`; 36 contract placements (see 1A, N1) |
| Cross-references | spec text | WC sub-ids, AC ids and UNVERIFIED items 12, 18-23 all exist; no stale "fresh dir", "WC-4 (ii)" or "every other case" remains; placeholder scan prints only the tool name `TodoWrite` (SPEC:116) |

### 2D. Citations I could not check (file or output absent from the sandbox, no inventory witness)

| Group | Spec locations | Status |
|---|---|---|
| `CLAUDE.md` lines | SPEC:35 (`:74`), 53 (`:83,408`), 175 (`:16,157,334`), 200 (`:16`), 231 (`:334`), 280 (`:50`), 305 (`:72-83`), 331 (`:76`) | UNVERIFIED |
| `src/superclaude/cli/install_core.py`, `Makefile`, `pyproject.toml` | SPEC:53, 331, 222 | UNVERIFIED |
| `src/superclaude/core/HOW-WE-WORK.md:22,171,249,254`, `core/CLAUDE.md:65` | SPEC:171, 189 | UNVERIFIED |
| `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:39,45,56`, `.dev/codegraph-migration/...:31,33,42`, `...return-contract.yaml:10` | SPEC:24, 25, 45, 61, 199 | Partly witnessed through CAPS:49 and CAPS:156; the rest UNVERIFIED |
| Orca guide, `--help` and shipped-JS lines | all `CAPS` cites | Not re-run (no `orca-ide`); trusted only as far as the capabilities inventory quotes them |
| Every `src/superclaude/{commands,skills,agents}` line in sections 3 and 4 | rows | Witnessed by the inventories (2B), not by the files |

## Part 3. Panel critique of the revised spec

Mode: critique, whole document (first review by the command's count), with extra attention to the lines that revision 2 added or changed (152 changed diff lines against V2). The panel read in the fixed order. Scores and consensus come last.

### Guard Condition Boundary Table

Trigger: the spec has flag guards, thresholds, a staleness test and a wait limit. Six cross-cutting guards that revision 2 added or rewrote are enumerated with the six required input conditions each (36 rows). The per-command gate resolutions of section 3 are instances of G4 and are not repeated. Construction: Nygard. Completeness validation: Crispin. Attacks on entries: Whittaker. All cells are populated, so the FR-10 synthesis gate is met. Every GAP row produces a finding of MAJOR or higher (FR-8) and is blocking; the finding id is in the Status column. No row has a blank or "unspecified" behaviour without a GAP (FR-9).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 contract placement and refusal | SPEC:64 (WC-4.1, 4.2) | Zero/Empty | `--report-dir` absent or `""`, command in case (iv) | refuse | Stop before any work, chat-only refusal, worker ends `failed` (WC-4.2, WC-5.1) | OK |
| G1 | SPEC:64 | One/Minimal | `--report-dir D`, D exists and is empty | accept | `<D>/return-contract.yaml` | OK |
| G1 | SPEC:64 | Typical | existing `--output-dir D` (case i) | accept | `<D>/return-contract.yaml` | OK |
| G1 | SPEC:64 | Maximum/Overflow | location not creatable or writable, inside `.git/`, or under a `.claude/` skill, agent or command folder | refuse | Same refusal as row 1 | OK |
| G1 | SPEC:64 | Sentinel Value Match | file-valued `--output x/return-contract.md` (stem equals the contract name) | stem rule | `x/return-contract.return-contract.yaml`; defined | OK |
| G1 | SPEC:62, 64, 147, 142 | Legitimate Edge Case | a case-(iv) callee invoked under WC-2.6 with `--unattended` and no location (tasklist Stage 9 to `sc:task`; cli-eval create W2 to `/sc:spec-panel`, which CMD:456 refuses without a report dir; roadmap to `sc:save`) | unknown | WC-2.6 passes the flag only; WC-4.2 reads "the brief gave none"; nothing says what a callee gets or where its contract goes | GAP (R3-3) |
| G2 staleness and ownership | SPEC:64 (WC-4.4) | Zero/Empty | no earlier contract at the path | none | Nothing to remove | OK |
| G2 | SPEC:64, 66 | One/Minimal | retry of the same Task, same location, same command line | stale | Old contract removed before other work | OK |
| G2 | SPEC:64, 222 | Typical | first run; contract written at the end | fresh | mtime later than `worker-start`; `command` equals the Task line | OK |
| G2 | SPEC:78 | Maximum/Overflow | two Tasks given one location | collision | Duty: one location per Task; fixed-location commands one Task per worktree | OK |
| G2 | SPEC:64, 79, 222 | Sentinel Value Match | the contract's `command` is rendered differently from the brief's line: no `/sc:` prefix (Skill tool starts the command with `args`), escaped quotes, one extra space, or an unquoted `: ` that breaks the YAML | mismatch | Exact string equality after `.strip()`; nothing defines the rendering or requires quoting | GAP (R3-1) |
| G2 | SPEC:63, 78, 222 | Legitimate Edge Case | the worker used WC-3 `ask`, then re-invoked the command with the answer as a flag; or a retry with changed text (item 18) | mismatch | WC-3 requires the re-invocation; SPEC:78 and step 4 require the contract's `command` to equal the original Task line; both cannot hold | GAP (R3-1) |
| G3 outcome mapping | SPEC:65 (WC-5.1, 5.2) | Zero/Empty | contract missing, empty or unparseable | failed | `--outcome failed` | OK |
| G3 | SPEC:65 | One/Minimal | `status: partial` | succeeded | `--outcome succeeded`, first sentence names `partial` | OK |
| G3 | SPEC:65 | Typical | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| G3 | SPEC:65 | Maximum/Overflow | `status: blocked`, empty `blocked_question` | failed | `--outcome failed` | OK |
| G3 | SPEC:65 | Sentinel Value Match | a legacy contract (adversarial, brainstorm, reflect, workflow before their phase) whose `status` is a word outside the four | divergent | WC-5.1 says outside the four is `failed`; WC-5.2 says such a contract "is judged by this paragraph": `succeeded` when the file is non-empty and no "halt or STOP line" shows; "halt or STOP line" is undefined | GAP (R3-2) |
| G3 | SPEC:65, 99 | Legitimate Edge Case | troubleshoot before P2: only `REPORT.md`, non-empty, final output without a halt line | succeeded | `--outcome succeeded`, first sentence says no contract existed | OK |
| G4 gate resolution | SPEC:62 (WC-2.2, 2.3, 2.5) | Zero/Empty | gate with no default and no caller flag | blocked | `status: blocked` plus the question; stop | OK |
| G4 | SPEC:62 | One/Minimal | caller flag answers the gate | resolved | (b) | OK |
| G4 | SPEC:62 | Typical | documented default only | resolved | (a) | OK |
| G4 | SPEC:62 | Maximum/Overflow | several gates visible at the stop (cli-eval, cli-portify) | blocked | `blocked_question` lists every unresolved gate | OK |
| G4 | SPEC:62, 108, 124 | Sentinel Value Match | caller flag that itself opens a gate: `--strategy intent`; explicit `--remediation-offer` with the row's "implies `--no-remediation-offer`" | refused; read as forced | `--strategy intent` refused (WC-2.5). For `--remediation-offer` the row says "implies" and WC-2.2 ranks a caller flag first; the "implies" reading is the natural one (R3-7) | OK (note R3-7) |
| G4 | SPEC:98, 140, 141 | Legitimate Edge Case | the gate lies in a skill that is not a command and has no section in any phase: tdd's nested `/task` MDTM executor (`sk/task/SKILL.md:49,114`) | unknown | The table names callee "task (P2)", which is the `/sc:task` row; no row converts `sk/task` | GAP (R3-4) |
| G5 outward flags | SPEC:69 (WC-9) | Zero/Empty | no authorization flag in the brief | all off | Every outward default is off | OK |
| G5 | SPEC:69, 108 | One/Minimal | one flag (`--post-pr`) | one class on | That class only; no umbrella flag | OK |
| G5 | SPEC:108 | Typical | `--unattended` alone on auggie-review | no post | `--no-post-pr` and `--no-remediation-offer` implied | OK |
| G5 | SPEC:69, 121 | Maximum/Overflow | brief authorizes all six classes (post-release) | six flags | One flag per class; D4 decides whether the brief may | OK |
| G5 | SPEC:53, 69 | Sentinel Value Match | the text `--post-pr` inside a quoted topic | not a flag | Standalone unquoted token rule | OK |
| G5 | SPEC:69, 80 | Legitimate Edge Case | `--post-pr` passed before P2 adds it | unknown flag | Support check fails, flag not passed | OK |
| G6 wait limit | SPEC:70 (WC-10) | Zero/Empty | no blocking call | none | No heartbeat issue | OK |
| G6 | SPEC:70 | One/Minimal | one call of 1 minute | below | No split | OK |
| G6 | SPEC:70 | Typical | one call of 3 minutes | below | No split | OK |
| G6 | SPEC:70, 109, 131 | Maximum/Overflow | one foreground build, test or eval over 4 minutes | above 240 s | Background job polled in waits of at most 240 s (feasibility UNVERIFIED, item 22) | OK |
| G6 | SPEC:70 | Sentinel Value Match | parallel Agent-tool batch over 5 minutes; a call of exactly 240 s | exempt; at limit | Batch exempt, silence not read as a stall (CAPS:125); "longer than 4 minutes (240 s)" allows exactly 240 | OK |
| G6 | SPEC:70, 122, 335 | Legitimate Edge Case | pr-submit round structure unknown | unknown | P4 measures the longest call first (item 12) | OK |

Table result: 36 rows, 5 GAP (G1 one, G2 two, G3 one, G4 one), mapped to blocking findings R3-1 (two rows), R3-2, R3-3 and R3-4. Round 2 found 6 GAP rows; its five blocking findings are closed.

### Quantity Flow Diagram (Pipeline Dimensional Analysis)

Trigger: the spec filters 43 commands into groups, phases and contract placements, and a Task fans out into nested calls. Fowler annotated the counts and Whittaker attacked each divergence. The counts are my re-count from the rows, not from `D2`.

```text
[Source: 43 commands = 21 INV-A + 22 INV-B]                                  (SPEC:84)
   --> [Stage 1: section 4 filter] --> 6 coordinator-only                    (SPEC:157-162)
   --> 37 worker-capable          (N=43 in, M=37 out, divergence 6, accounted)
         |-- 10 ready today                                                  (SPEC:91-100)
         `-- 27 needs a change                                               (SPEC:107-133)
   --> [Stage 2: phase assignment]  P1 14 + P2 15 + P3 4 + P4 3 = 36  (+ load, usage line only)
   --> [Consumer A: AC-1.1 per-phase lists]  expects 14, then +15, +4, +3     conserved   (SPEC:235)
   --> [Stage 3: 36 section-bearing commands --> contract placement stated]
         20 case iv (--report-dir) + 10 case i (5 flag names UNVERIFIED) + 3 case ii + 3 case iii = 36   conserved
   --> [Consumer B: WC-4.2 and step 4 of 7.2]  expect ONE location per command invocation
   --> [Stage 4: nested invocations, section 3.3: 11 caller-to-callee chains]
         brief supplies 1 location per Task
         3 chains reach a case-iv callee: cli-eval create -> spec-panel, tasklist Stage 9 -> sc:task, roadmap -> save
         (a 4th if the tdd row's "task" means sc:task, R3-4)
         locations supplied to those callees: 0 of 3                    <-- MISMATCH (R3-3, FR-19: CRITICAL)
   --> [Consumer C: step 4 `command` equality]  expects the contract's command == the Task's line
         Tasks that go through WC-3 ask-and-re-invoke: command line differs     <-- MISMATCH (R3-1)
```

Divergence result: the counts 43, 37 and 36 and the per-phase counts conserve, and the 36 placements are all stated. Consumers B and C do not conserve at the nested-call and re-invocation points. By FR-19 the Stage 4 divergence is CRITICAL (R3-3).

=== REQUIREMENTS ANALYSIS ===

Each finding: issue, severity, expert, recommendation with rationale, priority, quality-impact estimate.

**R3-8. 7.2 step 1 cannot pass for the P0 smoke commands as written.** Severity MINOR. Expert: Wiegers. Spec: 7.2 step 1 (SPEC:219), 2.3 support check (SPEC:80), AC-0.4 (SPEC:233), 3.1 intro (SPEC:87).
Issue: step 1 passes only if "the section 2.3 support check passed before the call". The support check passes only when the installed command file contains `## Unattended mode`. The three P0 commands have none (their phase has not run) and 3.1 says ready commands run before their phase without `--unattended`. Read literally, step 1 fails for every command in P0, yet AC-0.4 requires steps 1-3 to pass. An implementer reads "was performed and followed". Recommendation: say step 1 passes when the check was run and its result followed (flag passed only when supported). Priority Low. Quality impact: Consistency +0.5.

**R3-9. Two acceptance command lines omit the output flag their own row requires.** Severity MINOR. Expert: Adzic. Spec: AC-2.6 (SPEC:242), AC-2.2 (SPEC:240).
Issue: AC-2.6 is `/sc:research "<topic>" --unattended --strategy intent`. Research gains `--report-dir` (SPEC:124) and WC-4.2 refuses a case-(iv) command with no location before any work, with no file (SPEC:64). Run as written the command refuses for the missing location, not for the strategy, and there is no contract to carry "the refusal reason" that AC-2.6 expects. AC-2.2's `/sc:cli-eval run --unattended` with no `--suite` has the same omission. N14 fixed this class for AC-1.2 and left these two. Recommendation: add `--report-dir <dir>` to both lines (7.2 step 1 already says the brief carries the location). Priority Low. Quality impact: Testability +0.5.

**R3-11. The refusal rules added in revision 2 have no acceptance check.** Severity MINOR. Expert: Crispin. Spec: WC-2.3, WC-2.4, WC-4.2 (SPEC:62, 64), section 7.
Issue: `grep -i refus` over section 7 finds only AC-2.6. Nothing tests the person-mode refusal (WC-2.4, `--interactive` under `--unattended`), the no-location refusal (WC-4.2) or the several-gates list (WC-2.3). WC-4.2 and WC-2.4 are exactly where N11 and N15 found defects. Extends round-1 note 15. Recommendation: one gate-trigger run each in P1 and P2 (a `--interactive` flag; a missing `--report-dir`). Priority Low. Quality impact: Testability +1.

**R3-12. cli-portify has no route to success in one run, and AC-2.3 asks for one.** Severity MINOR. Expert: Cockburn (actor and goal). Spec: cli-portify row (SPEC:113), AC-2.3 (SPEC:241).
Issue: its three approval gates resolve only as (c) blocked; there is no (b) value a caller can pass to approve, so the first gate always stops the run. The new `--resume <contract>` continues from a recorded substep but the row does not say that resuming counts as the approval. AC-2.3 asks for a happy-path run "per P2 command" that ends `--outcome succeeded`. The behaviour is inferable (block, ask a person, resume) so this is a note. Recommendation: say in the row that a resume past a gate is the approval, and that AC-2.3 for this command is the resumed run. Priority Low.

**R3-13. P0 step 0 lists too few places to correct.** Severity MINOR. Expert: Wiegers. Spec: P0 row (SPEC:183), AC-0.5 (SPEC:234).
Issue: if the census differs, step 0 corrects "section 1.2 E5, section 3, SA-2 and AC-C1". A changed census also changes the section 6 command lists and per-phase counts (14, 15, 4, 3), the AC-1.1 lists and the number 43 at SPEC:27, 84 and 234, and it needs a classification of each new command, which no step assigns. Recommendation: name sections 6 and 7.3 and say the phase report classifies each new command as ready, needs-change or coordinator-only. Priority Low.

=== ARCHITECTURE ANALYSIS ===

**R3-4. The 3.3 table maps tdd's nested `/task` to the wrong primitive, so no phase makes the callee unattended.** Severity MAJOR, blocking (FR-8 GAP row G4-6; concrete wrong outcome below). Expert: Fowler (interface and boundary), Hohpe (flow). Spec: 3.1 tdd row (SPEC:98), 3.3 first row (SPEC:140), 3.2 task row (SPEC:129), WC-2.6.
Issue: the tdd row says its P2 change makes "the topic-only clarification and nested `/task` 'ask the user' lines resolve as blocked", citing `sk/task/SKILL.md:49,114`. The 3.3 row says the callee has the mode in "task (P2)". The 3.2 row called `task` is `/sc:task`: `cmd/task.md`, `sk/sc-task-protocol/SKILL.md`, gates "confidence below 0.70" and the TFEP (SPEC:129; INV-B:45, INV-B:197-205). The nested `/task` that tdd runs is the MDTM executor skill `sk/task`, whose lines 49 and 114 ask the user when several task files match or an item looks wrong (INV-B:47, INV-B:219). The 3.3 table uses "task" for the caller of the next row (`/sc:task` to troubleshoot, SPEC:141) and for this callee, so the same word names two primitives. `sk/task` is not one of the 43 commands and appears in no phase. The "ask the user" lines are in another file than tdd's, so tdd's own edit cannot resolve them, and WC-2.6 can pass the flag only to a callee that has a section.
Concrete wrong outcome: a P2 implementer converts `/sc:task` (SPEC:129), passes `--unattended` to `/task` (SPEC:140), and ships. An unattended tdd worker reaches `sk/task/SKILL.md:49` with two matching task files; the executor does not know the flag (item 16: free text), asks the user and the worker stalls with no `worker_done`; the coordinator sees only a healthy waiting worker (CAPS:52). AC-2.2 would only catch it if its input happens to hit that gate.
Recommendation: name the primitive in the 3.3 row (`sk/task`, the MDTM executor) and either add it to the P2 list with its two gates resolved as blocked, or make tdd's section pass what removes the ask (the task-file path) and refuse an ambiguous match. Priority High. Quality impact: Consistency +1, Completeness +1.

**R3-7. WC-2.5 covers only run-time-generated questions; an explicit gate-opening flag with a fixed question falls back to the precedence rule.** Severity MINOR. Expert: Nygard. Spec: WC-2.2 and WC-2.5 (SPEC:62), auggie-review row (SPEC:108).
Issue: WC-2.5 refuses a caller flag only when "the question is generated at run time so that no (c) stop can name it in advance". `--remediation-offer` opens a fixed offer, so it falls under WC-2.2, where a caller's flag beats a documented default. The auggie-review row says `--unattended` "implies `--no-remediation-offer`". Two readings: forced (no stall) or overridden by an explicit `--remediation-offer` (stall on a plain chat offer, INV-A:62). The brief template does not pass the flag, so the exposure is a contradictory brief. Recommendation: say that "implies" is forced, or widen WC-2.5 to every flag that opens a gate. Priority Low.

**R3-10. Code block 2 and AC-C5 take the base from a local `master` that may be stale.** Severity MINOR. Expert: Nygard. Spec: code block 2 (SPEC:214).
Issue: `git merge-base master HEAD` uses the local branch. If the work branch was rebased onto a newer `origin/master`, the merge base is the old local `master` and the listing includes other people's removed lines in the files the phase edited, so "prints nothing" fails for a clean phase. The repo's own pre-PR check says the fork's `master` can be ahead of the local one (`CLAUDE.md`; not in the workspace, UNVERIFIED here). Reasoned from git semantics; not run. Recommendation: use `origin/master`, or the phase's recorded start commit. Priority Low.

**R3-6. The spec-panel row's reconcile list omits differences that the live definition shows, and its line numbers are stale.** Severity MINOR. Expert: Newman (versioning against installed copies). Spec: spec-panel row (SPEC:128), WC-4.2, WC-4.3.
Issue: `CMD` (the live definition) already has `## Unattended mode` (CMD:451-461) and the row correctly describes four differences (flag name, contract path, no refusal of person-mode flags, socratic writes its questions). It does not list: (a) CMD:457 leaves "paths git ignores" out of `artifacts` and labels that rule "WC-4" of `~/.claude/WORKER-CONTRACT.md`, while this spec's WC-4.3 says `artifacts` is "every other file written" and its WC-4 is the report-file requirement (the installed contract file is not in the workspace, so which numbering is current is UNVERIFIED); (b) CMD:456 also refuses a location inside `.codegraph/`, which WC-4.2 does not; (c) CMD:457 names the statuses succeeded, blocked and failed and does not mention a `command` field, which step 4 asserts (UNVERIFIED whether the installed contract carries it). The row's `cmd/spec-panel.md` line numbers are stale against `CMD` (X3) and `R2:238` is cited for the contract path that is at CMD:457 (X2). Recommendation: add (a) to (c) to the reconcile sentence and refresh the numbers. Priority Low.

**R3-5. A citation for the nested-spawning doubt points at the wrong inventory item.** Severity MINOR. Expert: Newman. Spec: tasklist row (SPEC:130), item 21 (SPEC:344).
Issue: see X1. INV-B:322 asks who answers the reflect remediation offer; it does not say nested spawning is UNVERIFIED. Round 2 (C7) listed the same three lines and revision 2 copied them. Recommendation: cite INV-B:210 and INV-B:314 only, or add INV-B:322 as the separate "who answers" doubt. Priority Low.

**R3-14. Three citation wordings are stronger than their sources.** Severity MINOR. Expert: Wiegers. Spec: SPEC:64, 79, 122, 280.
Issue: see X4 to X6: "default" for the 600 s; "Task text inside a preamble"; SA-5 as the source of the `.claude/` write refusal. Each is a one-word or one-cite fix. Recommendation: drop "default" or cite the live line; say "preamble and Task block"; cite CMD:456 or `CLAUDE.md` instead of SA-5. Priority Low.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

Scope: specification correctness only; resilience patterns and test strategy stay with Nygard and Crispin. The boundary table carries the zero, sentinel and divergence probes row by row; the three attacks below are the ones that survive it.

**R3-1. I can break this specification by Sequence Attack and Sentinel Collision Attack on the `command` check.** The invariant at **2.3 (SPEC:78) and step 4 of 7.2 (SPEC:222), "the contract's `command` equals this Task's command line"** fails when **the worker follows WC-3 (SPEC:63) or the command renders its own line differently from the brief.** Severity MAJOR, blocking (FR-8 GAP rows G2-5 and G2-6; concrete wrong outcome below). Expert: Whittaker with Wiegers. Origin: changed (added by revision 2 for N4).
Concrete attack. Task T brief: `/sc:spec-panel @tdd.md --unattended --report-dir D` (a TDD input with no `target_release`). State before: `D` empty, Task `dispatched`. t1: the command hits its gate and writes `D/return-contract.yaml` with `status: blocked`, `blocked_question: target_release`, `command: "/sc:spec-panel @tdd.md --unattended --report-dir D"`. t2: the worker, holding a preamble, takes the WC-3 route: `ask`, the coordinator answers `v2`, and the worker re-invokes the command "with the answer as a flag" (WC-3): `... --target-release v2`. t3: the command removes the stale blocked contract (WC-4.4), runs, writes `status: succeeded` and `command: "... --target-release v2"`. t4: the worker sends `worker_done --outcome succeeded --report-path D/return-contract.yaml`. t5: the coordinator runs step 4 against T's line, which has no `--target-release v2`: the assertion `str(d['command']).strip() == sys.argv[2].strip()` fails (my run, 2C). State after: a correct, finished run is rejected as "not this Task's contract" and ends `failed` under SPEC:78; the alternative, updating the stored Task line, removes the sibling protection N4 added. Variant on the Sentinel side: SPEC:79 starts the command through the Skill tool with `args` only, so the command may write `command` with or without `/sc:`, with different quoting or spacing; my run shows 4 of 5 renderings fail. A topic containing `: ` (for example `fix: login`) written unquoted makes the file unparseable YAML, which WC-5.1 maps to `failed`; WC-4.3 does not require quoting.
Recommendation: keep the sibling protection but compare something both sides can fix. Since SPEC:78 already gives each Task its own location, check that the contract sits at the Task's location and that its `command` starts with the Task's command name and contains the Task's output-location argument; state that `command` is the argument string after the command name, appended to (not replaced) by a WC-3 re-invocation, and is YAML-quoted. Rationale: removes the false failure and the YAML hazard without dropping the check N4 asked for. Priority High. Quality impact: Consistency +1, Testability +1.

**R3-2. I can break this specification by Divergence Attack on the outcome of a legacy contract.** The invariant at **WC-5.1 and WC-5.2 (SPEC:65)** fails when **a ready command that has not reached its phase writes a legacy contract whose `status` word is outside the four.** Severity MAJOR, blocking (FR-8 GAP row G3-5; concrete wrong outcome below; this also regresses round-1 finding 12). Expert: Whittaker with Nygard. Origin: changed (WC-5.2 added by revision 2 for N2).
Concrete attack. P0 smoke run of `/sc:adversarial --compare a.md b.md --depth quick --output D`. The skill must write a contract on every run, failures included (INV-A:35), and its vocabulary is not inventoried (note 22; the four-value set is this spec's own, SPEC:303). State: convergence falls below the threshold; the command writes `D/adversarial/return-contract.yaml` with `status: error` (any word outside the four) and ends with "Merge aborted: convergence 0.41", which contains neither "halt" nor "STOP". WC-5.1 says a `status` outside the four is `failed`. WC-5.2 sends the same file to "this paragraph": it exists, is non-empty, no halt or STOP line, so `--outcome succeeded`. Two paragraphs of one requirement give opposite outcomes, and the second selects the fail-open one. After state: the Task is `completed`; its dependents become startable on a failed merge (the ready view and the blocked-dependents rule are at CAPS:86 and CAPS:90: only a failed Task keeps them blocked); AC-0.4 records a pass on a failed run in the phase whose purpose is to test the decision (SPEC:233). "A halt or STOP line" is not defined: which commands print one, and in what words.
Recommendation: fail closed. For a legacy contract with a `status` outside the four, the worker records the word and sends `failed` unless the phase report already maps that word to success; replace the "halt or STOP line" test by the file's own status or verdict field; keep the existing-and-non-empty rule for the markdown report (`REPORT.md`) only. Rationale: restores round-1 finding 12 and keeps N2's purpose, a defined outcome for P0. Priority High. Quality impact: Consistency +1, Testability +1.

**R3-3. I can break this specification by Accumulation Attack on the number of output locations.** The invariant at **WC-4.2 with WC-2.6 and 2.3 (SPEC:62, 64, 75) and section 3.3 (SPEC:138-150)** fails when **an unattended command invokes a case-(iv) callee.** Severity CRITICAL under FR-19 (count divergence: the brief supplies 1 location per Task; WC-4.2 needs 1 per invocation; the nested invocation count is 1 + k), blocking. Expert: Whittaker with Fowler. Origin: the gap sits in text unchanged since revision 1 (WC-2.6) and revision 2 made it bite by adding WC-4.2 and the `--report-dir` rows.
Concrete attack. Brief: `/sc:tasklist <roadmap> --unattended --report-dir D`. State before: one location `D`. Stage 9 invokes `/sc:task --compliance strict` (SPEC:147); WC-2.6 requires `--unattended` on that call. `sc:task` is a case-(iv) command (SPEC:129). Branch A: the caller passes only `--unattended`; WC-4.2 makes `sc:task` stop before any work with a chat-only refusal (the one installed callee I can read, `/sc:spec-panel`, refuses exactly so, CMD:456), and tasklist's Stage 9 patch step fails. Branch B: the implementer passes `--report-dir D`; the callee removes the file at `D/return-contract.yaml` at start (WC-4.4) and later writes its own contract at the caller's path; the caller's final write replaces it, but if the caller dies after the callee finishes, the callee's contract sits at the caller's path and is read as the caller's outcome (or fails R3-1's check). After state: A gives a failed Stage 9, B a possible wrong outcome. The same happens for cli-eval create W2 to `/sc:spec-panel` and for roadmap to `sc:save` (3 of the 11 chains in 3.3; 4 if R3-4 is resolved the other way).
Recommendation: add one sentence to WC-2.6: a caller hands each callee that needs a location a location of its own below the caller's (for example `<caller dir>/<callee name>/`), the callee's contract there is the caller's evidence and not a deliverable, and the caller reads it before it writes its own. Rationale: closes both branches with one rule. Priority High. Quality impact: Completeness +1, Consistency +1.

=== CONSENSUS AND DISAGREEMENTS ===

Consensus.
- All 18 round-2 findings and all 11 citation findings are resolved as named in the spec text. The decision, the rejected alternative, the evidence-gap statement and the contract-placement table of section 3 are now the strongest parts; counts conserve (43, 37, 36, 14/15/4/3) and the 36 placements are all stated.
- The four open blocking defects sit at joins that revision 2 created or tightened: the equality check against WC-3 (R3-1), the fallback outcome against WC-5.1 (R3-2), the output location against nested calls (R3-3), and a table row that names the wrong callee (R3-4).
- The acceptance snippets still behave as described when run (AC-C1, code block 2, the step-4 assertion on a matching contract).

Disagreements.
- Nygard would grade R3-7 MAJOR (a stall on an explicit flag); Whittaker and Crispin keep it minor because the coordinator controls the flags in the brief (INV-B:307) and the row says "implies".
- Fowler grades R3-3 CRITICAL by FR-19; Newman would call it MAJOR because branch A fails loudly. The command's rule decides: CRITICAL. Both are blocking.
- Adzic holds that R3-8, R3-9 and R3-13 are notes that must not trigger a revision (Review Loop bullet 2); Wiegers agrees.

Positive checks (nothing to fix): WC-6 now reads consistently; the N1 placement table is complete for the 36 commands; WC-2.5 and AC-2.6 close the research example; the six-class list in WC-9 matches its opening sentence; the item and id cross-references all resolve.

### Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe, crispin]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 6.9     # round 2 scored 6.3
  clarity: 7
  completeness: 7        # nested-call location (R3-3), wrong callee (R3-4)
  testability: 6         # command equality brittle (R3-1), refusal rules untested (R3-11)
  consistency: 7         # WC-5.1 vs WC-5.2 (R3-2)
critical_issues:
  blocking: [R3-1, R3-2, R3-3, R3-4]
  non_blocking: [R3-5, R3-6, R3-7, R3-8, R3-9, R3-10, R3-11, R3-12, R3-13, R3-14]
expert_consensus:
  - Round-2 findings N1-N18 and citations C1-C11 are resolved as named.
  - The four blocking defects sit at joins that revision 2 introduced or tightened.
improvement_roadmap:
  immediate: [R3-1, R3-2, R3-3, R3-4]
  short_term: [R3-6, R3-5, R3-9]
  long_term: [R3-7, R3-8, R3-10, R3-11, R3-12, R3-13, R3-14]
adversarial_analysis: see === ADVERSARIAL ANALYSIS (Whittaker) === (R3-1, R3-2, R3-3)
```

## Numbered list of new findings

Evidence paths expand as in the shorthand at the top. Origin: `changed` = in lines revision 2 added or changed; `unchanged` = in text identical to V2.

| # | Finding | Severity | Blocking | Origin | Spec section | Evidence path:line |
|---|---|---|---|---|---|---|
| R3-1 | The coordinator duty and step 4 of 7.2 require the contract's `command` to equal the Task's exact command line by string equality; a worker that uses WC-3 (ask, then re-invoke with the answer as a flag) writes a different line, and the Skill-tool start (`args` only) makes the rendering ambiguous. A correct run is rejected as a sibling's contract; an unquoted `: ` breaks the YAML | MAJOR | yes (FR-8 GAP G2-5, G2-6; concrete outcome: correct run judged `failed`) | changed | 2.2 WC-3, WC-4.3; 2.3; 7.2 step 4 | SPEC:63, 64, 78, 79, 222; run of the assertion on six samples (Part 2C) |
| R3-2 | WC-5.2 sends a legacy contract with a status outside the four to a rule that returns `succeeded` for any non-empty file without a "halt or STOP line"; WC-5.1 says the same file is `failed`. A failed ready-command run in P0 (or before its phase) is recorded as success; "halt or STOP line" is undefined. Regresses round-1 finding 12 for legacy contracts | MAJOR | yes (FR-8 GAP G3-5; concrete outcome: failed run released as succeeded, dependents start) | changed | 2.2 WC-5; 6 P0; AC-0.4 | SPEC:65, 233, 303; INV-A:35; INV-B:272; R2:47 |
| R3-3 | WC-2.6 makes an unattended command pass `--unattended` to each callee with a section; WC-4.2 makes a case-(iv) callee refuse when it has no output location; the brief supplies one location per Task. 3 of 11 chains in 3.3 hand a case-(iv) callee no location (cli-eval create to spec-panel, tasklist Stage 9 to sc:task, roadmap to save); the alternative of reusing the caller's directory makes the callee overwrite or leave the caller's contract path | CRITICAL (FR-19 count divergence 1 vs 1+k) | yes | unchanged text made to bite by revision 2 | 2.2 WC-2.6, WC-4.2; 2.3; 3.3 | SPEC:62, 64, 75, 129, 138-150; CMD:456 |
| R3-4 | 3.3 maps tdd's nested `/task` (the MDTM executor `sk/task`, which asks the user at its lines 49 and 114) to callee "task (P2)", the `/sc:task` row; no phase gives `sk/task` a section, so the unattended tdd worker can stall on that ask | MAJOR | yes (FR-8 GAP G4-6; concrete outcome: silent stall) | unchanged | 3.1 tdd; 3.3; 3.2 task | SPEC:98, 129, 140, 141; INV-B:45, 47, 219 |
| R3-5 | `INV-B:322` is cited for "nested spawning is UNVERIFIED"; that line is about who answers the remediation offer (copied from round-2 C7) | MINOR | no | changed | 3.2 tasklist; UNVERIFIED 21 | SPEC:130, 344; INV-B:322; R2:67 |
| R3-6 | The spec-panel row's reconcile list omits what `CMD` shows (git-ignored paths left out of `artifacts` under that file's "WC-4"; `.codegraph/` refusal; no `command` field named); its `cmd/spec-panel.md` line numbers are stale and `R2:238` is cited for a contract path that is at CMD:457 | MINOR | no | changed | 3.2 spec-panel | SPEC:128, 314; CMD:36-37, 224, 451-461, 475, 479; R2:238 |
| R3-7 | WC-2.5 covers only run-time-generated questions; an explicit `--remediation-offer` (fixed question) falls under "caller flag beats default" against the row's "implies `--no-remediation-offer`" | MINOR | no | changed | 2.2 WC-2.2, WC-2.5; 3.2 auggie-review | SPEC:62, 108; INV-A:38, 62 |
| R3-8 | 7.2 step 1 passes only if "the support check passed", which is false for the P0 commands that have no section, yet AC-0.4 needs steps 1-3 to pass | MINOR | no | unchanged (AC-0.4 changed) | 7.2 step 1; AC-0.4 | SPEC:80, 87, 219, 233 |
| R3-9 | AC-2.6 and AC-2.2 give command lines without the `--report-dir` that WC-4.2 requires; run as written they refuse for the missing location, with no contract | MINOR | no | changed | 7.3 AC-2.2, AC-2.6 | SPEC:64, 124, 240, 242 |
| R3-10 | Code block 2 takes the base from local `master`, which can be stale after a rebase onto `origin/master`, so a clean phase lists other people's removals | MINOR | no | changed | 7.1 code block 2 | SPEC:214 (`CLAUDE.md` pre-PR check, UNVERIFIED here) |
| R3-11 | No acceptance check covers the refusal rules WC-4.2, WC-2.4 and the list rule WC-2.3 | MINOR | no | changed | 2.2; 7.3 | SPEC:62, 64; section 7 (`grep refus` finds only AC-2.6) |
| R3-12 | cli-portify has only the blocked route for three approval gates and no statement that a resume counts as approval; AC-2.3 asks for a one-run success | MINOR | no | changed | 3.2 cli-portify; AC-2.3 | SPEC:113, 241; INV-A:45 |
| R3-13 | P0 step 0 corrects only E5, section 3, SA-2 and AC-C1 if the census differs; section 6 lists, per-phase counts, AC-1.1 and the number 43 also change, and no step classifies new commands | MINOR | no | changed | 6 P0; AC-0.5 | SPEC:27, 84, 183, 234, 235 |
| R3-14 | Three wordings exceed their sources: "default" 600 s; "Task text inside a preamble"; SA-5 as the source of the `.claude/` write refusal | MINOR | no | changed | 2.3; 2.2 WC-4.2; 3.2 pr-submit; D3 | SPEC:64, 79, 122, 175, 280; INV-B:95, 299; CAPS:76, 78, 148 |

Totals: 1 CRITICAL (R3-3), 3 MAJOR blocking (R3-1, R3-2, R3-4), 10 MINOR (R3-5 to R3-14), 0 MAJOR graded minor. Blocking findings open: R3-1, R3-2, R3-3, R3-4. Round-1 notes 15, 16, 18, 19, 20, 21, 22, 23, 24 remain open and unchanged (17 is closed by C7).

Citation-check summary (Part 2): 6 weak citations in 2A (1 wrong cite X1, 1 stale against the live file X3, 4 loose X2, X4, X5, X6), none blocking on its own; everything else that revision 2 added or changed is supported by the inventory, capabilities, README or round-2 line it cites. The live `src/` files and Orca output could not be read in this sandbox, so those cites are UNVERIFIED as stated in 2D.

## Verdict

Revision 2 resolves all 18 round-2 findings (N1-N18) and all 11 citation findings (C1-C11) as named in the spec text, and the counts conserve. It does not pass: four blocking defects remain, all at joins that revision 2 created or tightened or that its new rules now expose. R3-1: the `command` equality that closes N4 contradicts WC-3 and rejects a correct run. R3-2: the fallback that closes N2 fails open and undoes round-1 finding 12 for legacy contracts. R3-3: the output-location rule has no answer for nested calls (FR-19 count divergence). R3-4: the nested-call table names the wrong primitive for tdd's `/task`. The brief's rule (any finding is FAIL) and Review Loop bullet 2 (a blocking finding is open) both give FAIL. Because the verdict is FAIL there is no Self-Audit. The report header is `review: 1 of 3` by the command's count (no `--re-review`, no `--baseline`); this is the third report on this spec, so by the coordinator's count a FAIL here is the point where Review Loop bullet 4 has the run escalate to the user instead of revising again, and the coordinator decides that.

Reviser brief

Blocking finding ids: R3-1, R3-2, R3-3, R3-4. The reviser reads this report, not the command, so the rules are restated here. Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for. Each added paragraph or table cites its finding id. The reviser reports the byte size of the spec before and after (before this revision: 90054 bytes, 346 lines). Findings R3-5 to R3-14 and round-1 notes 15 to 24 are notes and never trigger a revision. A brief may narrow this scope but may not widen it past the changed lines and the prior blocking findings, and may not grade a minor finding as blocking. At most 2 fix cycles remain by the report header (this is `review: 1 of 3` by the command's count; the coordinator keeps the real count); at review 3 with a FAIL verdict the run escalates to the user instead of revising.

verdict: FAIL
