review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md (whole-document, first review)

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| Candidate sha256 | `21fdbd31168a1ef40b1a05d12ef2b15a3e9d6f6fb4d8afb6da439fffe555cae8` |
| Baseline / prior report | none given; this is a first review of the whole document (no `--re-review`, no `--baseline`) |
| Reviewer model actually used | claude-sonnet-5-5 (Sonnet 5.5) |
| Review date | 2026-11-10 |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full) |
| Mode of run | attended-style, no `--unattended`; no improved spec written; the candidate was not edited |

Citation keys. `SPEC:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `CMD:N` = the `command.md` definition of this command. Anything the sandbox does not hold (`CLAUDE.md`, `EVIDENCE.md`, `cmd/`, `sk/`, `pyproject.toml`, Orca guides) is marked UNVERIFIED when I rely on it; I only checked it through the inventory line that quotes it.

Coverage line: whole document (SPEC:1-285) read in full and checked against the three inventories; ~45 citations to the inventories were checked line by line (list in "Citation check"); source files under `cmd/`, `sk/`, `src/` and the Orca guides could not be opened and are UNVERIFIED.

## Panel

Order per CMD:101-113, limited by `--focus requirements,architecture` plus Whittaker (active in every review, CMD:83): Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker, Newman, Hohpe (architecture and adversarial). Crispin and Gregory were consulted only on the acceptance checks of section 7 because B-1 is theirs; Hightower had nothing to add beyond Nygard's operational points.

## Grading check (FIRST-REVIEW prompt, for every finding I considered blocking)

Only B-1 passed the check. For each other finding the sentence "an implementer who follows the stated text as written builds X, and X is wrong because Y" needs a guess about which of two allowed readings the implementer picks, or the finding is a requirement the document never states. Those are Medium and sit under follow-up candidates even where the panel label is MAJOR.

## Guard Condition Boundary Table (mandatory artifact; completed before synthesis)

Trigger: the spec contains thresholds and boolean guards (readiness 60 s, heartbeat 5 min / wait 4 min, depth 1, confidence 0.70, three-failure breaker, `--unattended`, `status` mapping, roadmap resume). Lead Nygard, completeness Crispin, attack Whittaker.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `unattended` (switch) | SPEC:51,60,146 | Zero/Empty | flag absent | false | today's behaviour unchanged (SA-1) | OK |
| `unattended` | SPEC:62,73 | One/Minimal | flag present, no `--output`/`--output-dir` | true | not stated: WC-4 needs "the directory the coordinator passed"; none passed | GAP (M-1) |
| `unattended` | SPEC:62,200 | Typical | flag plus `--output <dir>` | true | contract at `<dir>/return-contract.yaml` | OK |
| `unattended` | SPEC:62,87,90,120 | Legitimate Edge Case | `--output` is a file (tdd, init-lite, spec-panel) | true | not stated: no directory exists to hold the contract | GAP (M-1) |
| `unattended` | SPEC:73,84,87 | Legitimate Edge Case | flag sent to a command that is never changed (brainstorm, init-lite) | true | not stated: 2.3 says every brief carries it; 3.1 says no change | GAP (M-2) |
| `unattended` | SPEC:51 | Sentinel Value Match | the text `--unattended` inside quoted topic/spec content | true? | not stated (the spec never defines token parsing) | GAP (M-2, minor part) |
| `heartbeat_wait_split` | SPEC:68,210 | Zero/Empty | no blocking call | false | nothing to split | OK |
| `heartbeat_wait_split` | SPEC:68 | Typical | one call of 3 min | false | no split needed | OK |
| `heartbeat_wait_split` | SPEC:68,210 | Legitimate Edge Case | one call of 4 to 5 min | false (WC-10 threshold is "longer than 5") | WC-10 allows it, AC-4.3 ("no single tool call exceeds 240 s") fails it | GAP (N-6) |
| `heartbeat_wait_split` | SPEC:68,104 | Maximum/Overflow | eval wait of 3600 s | true | split into waits of at most 4 min | OK |
| `nested_depth` | SPEC:33,214 | Zero/Empty | caller depth 0 (coordinator) | false | may dispatch workers | OK |
| `nested_depth` | SPEC:33,66 | One/Minimal and Typical | worker at depth 1 | true | refuse Orca fan-out (WC-8) | OK |
| `nested_depth` | SPEC:249-253 | Maximum/Overflow | depth raised to 2 or more | false | D5 (b), rejected by recommendation | OK |
| `retry_breaker` | SPEC:64; CAPS:80,116 | Zero/Empty | first attempt, no retry | n/a | no resume needed | OK |
| `retry_breaker` | SPEC:64 | One/Minimal | one `--retry-of` | true | resume flag, else "fresh dir" | OK (but see M-4) |
| `retry_breaker` | SPEC:64; CAPS:116 | Maximum/Overflow | third consecutive failure, then a fourth attempt | true | not stated: Orca fails the Task; the spec never says what the coordinator does | GAP (M-8) |
| `ask_wait` | SPEC:61; CAPS:60,68 | Typical | answer arrives | true | resume same message ID, re-invoke with answer | OK |
| `ask_wait` | SPEC:61,281 | Maximum/Overflow | no answer ever arrives | true | not stated: no cap on how long the worker waits before reporting blocked | GAP (M-8) |
| `outcome_map` | SPEC:63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| `outcome_map` | SPEC:63,263 | Sentinel Value Match | `status: partial` | true | `--outcome succeeded`, body names `partial` | OK |
| `outcome_map` | SPEC:63 | Legitimate Edge Case | audit verdict FAIL | true | `--outcome succeeded` | OK |
| `outcome_map` | SPEC:62,262 | Legitimate Edge Case | existing contract with its own status word | true | "keep their fields" versus a fixed four-value set | GAP (M-5) |
| `roadmap_resume` | SPEC:118,205 | Zero/Empty | no `.session-memory.md`, no flag | false | fresh start | OK |
| `roadmap_resume` | SPEC:118,205 | One/Minimal | state exists in the passed dir, no flag | false | "starts fresh" in the same dir (AC-3.2) | OK as stated; see M-4 |
| `roadmap_resume` | SPEC:118 | Legitimate Edge Case | resume flag passed, no state on disk | true | not stated | GAP (minor, N-7) |
| `confidence_gate` (task) | SPEC:121; INV-B:45 | Typical and Zero/Empty | confidence 0.0 to 0.69 | true | blocked | OK |
| `confidence_gate` (task) | SPEC:121 | Legitimate Edge Case | confidence exactly 0.70 | false | not stated; `cmd/task.md:93` not openable | UNVERIFIED |
| `pr_submit_monitor` | SPEC:114; INV-B:34 | Zero/Empty | `--monitor 0` | n/a | not stated (only `--monitor 1` is refused); P4 is gated on D3 | GAP (N-7) |

Omitted classes, one line each: `unattended` Maximum/Overflow (a boolean has no capacity); `heartbeat_wait_split` One/Minimal (same as Typical); `nested_depth` Sentinel (the only sentinel is the fallback to 1 for a malformed setting, `CAPS:100`, which the spec does not use); `retry_breaker` Typical (same as One/Minimal) and Sentinel (no reserved value); `ask_wait` Zero/Empty (an empty question is not a spec-defined input) and Sentinel (none); `outcome_map` One/Minimal and Typical (same as Zero/Empty and the success path); `roadmap_resume` Maximum/Overflow and Sentinel (no counter or reserved value); `confidence_gate` Maximum/Overflow (1.0 is just above the pass band); `pr_submit_monitor` Maximum (the spec says nothing above 1, so nothing can be graded).

Hard gate FR-10: every guard is enumerated and every class has a row or a stated reason, so synthesis proceeds. GAP rows were graded under FR-8/FR-9 by consequence (Review Loop bullet 2): none names a concrete wrong outcome without a further assumption, so all are Medium.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, FR-17 to FR-21)

Trigger: the spec runs commands through a classify, then phase, then acceptance-check pipeline whose stage counts can differ.

```text
[Inventories: 43 commands = 21 (INV-A:3) + 22 (INV-B:3)]
   --> [Classify, SPEC:76] --> ready 10 | needs-change 27 | coordinator-only 6      10+27+6 = 43 (conserved)
ready 10 (SPEC:83-92) --> P0 smoke 3 (SPEC:158, drawn from the 10, no edit)
                      --> P1 fix-only 4: adversarial, cleanup-audit, index-repo, workflow (SPEC:159)
                      --> P2 gate fix 4: reflect, release-split, tdd, troubleshoot (SPEC:160)
                      --> no change 2: brainstorm, init-lite (SPEC:84,87)            4+4+2 = 10 (conserved)
needs-change 27 (SPEC:99-125) --> P1 9 (8 + load) | P2 11 | P3 4 | P4 3             9+11+4+3 = 27 (conserved)
Changed commands in P1 = 8 + load + 4 fix-only = 13
   --> [Consumer 1: SPEC:76 "Every changed command also gains the `## Unattended mode` section" (and SPEC:52): expects 13]
   --> [Consumer 2: AC-1.1 (SPEC:195) asserts the section on 8; asserts absence on load and on P2-P4]  <-- MISMATCH 13 vs 8, the 4 fix-only commands are neither required nor forbidden
   --> [Consumer 3: 2.3 brief (SPEC:73): `--unattended` on every Task, including brainstorm and init-lite, which never change]  <-- MISMATCH
```

Counts are conserved through the split (43, 10, 27); they diverge only at the "which commands accept `--unattended`" consumers. FR-19 labels a dimensional mismatch CRITICAL; Review Loop bullet 2 (CMD:259) says to grade by consequence, not label, so it is graded Medium (M-2): the implementer has two allowed readings and neither loses data or crosses a safety boundary. This is the only place I departed from a command label, and I name it here.

## === REQUIREMENTS ANALYSIS ===

### B-1 (blocking). Acceptance check AC-0.4 cannot pass as written, and its failure "reopens section 1"
- Severity MAJOR (CRITICAL-equivalent for the gate: it is the entry check for every later phase). Experts: Crispin, Wiegers. Priority High. Quality impact: Testability 6 to 8.
- Sentence. An implementer who follows the stated text as written runs the P0 smoke check on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` and requires "steps 1-3 and 5-7 pass" (SPEC:194), and X is wrong because step 3's pass condition includes "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (SPEC:182), while in P0 no command has been edited: troubleshoot writes only `REPORT.md` with no contract (SPEC:91; INV-B:49), adversarial's contract filename "is not fixed" (SPEC:83; INV-A:35,60), and workflow's contract sits at `.dev/tasks/to-do/<id>/return-contract.yaml`, not at `<output-dir>/return-contract.yaml` that WC-4 defines (SPEC:62,92). Only step 4 is carved out ("uses the command's existing report file", SPEC:194); step 3's second and third clauses are not.
- Consequence. The P0 gate cannot be met by any of the three runs for the "WC-4 contract path" clause (troubleshoot has no contract to compare), and SPEC:194 says a failure "reopens section 1", the core decision, while SPEC:154 says no later phase starts until the earlier checks pass. A literal run therefore stalls the whole rollout or forces an undocumented reinterpretation.
- Recommendation (narrow, do not add): in AC-0.4 state that for P0 step 3 passes on "exactly one `worker_done` whose `--outcome` matches the existing report's verdict", and name the existing report path of each of the three commands; no new rule. Rationale: the contract arrives in P1 (SPEC:194 already says so for step 4).

### M-1 (Medium). WC-4's contract location rule does not fit the rows that use a file-valued or fixed path
- Experts: Wiegers, Whittaker (Divergence and Zero/Empty attacks). Priority Medium. Impact: Clarity.
- WC-4 puts the contract at `<output-dir>/return-contract.yaml`, where the directory is what the coordinator passed with `--output` / `--output-dir` (SPEC:62). The rows disagree: tdd, init-lite and spec-panel take `--output <file>` (SPEC:87,90,120); adversarial's fixed path is `<output>/adversarial/return-contract.yaml` (SPEC:83); workflow's is `.dev/tasks/to-do/<id>/…` with an id the command creates (SPEC:92), and its pre-creation stop has no directory at all (SPEC:92; INV-B:272 says no contract is written there today); and `--unattended` with no output flag has no stated behaviour. WC-4 and 2.3 say the path is "known before dispatch" (SPEC:62,73), which cannot hold for workflow's `<id>`. `CMD:22-23,460` shows `--output` is file-valued in this very command, so the ambiguity is real.
- Recommendation: one sentence in WC-4 naming where the contract goes when `--output` is a file (beside it) and for commands with a fixed path, and what happens with no output flag (blocked in chat, nothing written). Prefer narrowing the rule over adding rows.

### M-2 (Medium). Which commands accept `--unattended` is stated three different ways
- Experts: Wiegers, Fowler. See the Quantity Flow Diagram. SPEC:52 and SPEC:76 ("every changed command gains the section"; SA-4 at SPEC:149 says the same), SPEC:73 (every brief carries `--unattended`), SPEC:79 and SPEC:83-92 (ready commands run with the stated flags, no `--unattended`, four of them changed only by a small fix), SPEC:159 and SPEC:195 (eight commands). Result: the P0 brief template ("lists the section 3.1 flags", SPEC:158) and 2.3 conflict, and brainstorm and init-lite never get the flag or the section (SPEC:84,87). Smaller point: the spec never says how the token is parsed (quoted content containing the text `--unattended`); `CMD:459` does for this command.
- Graded Medium because "include `--unattended` where the command accepts it" is an allowed reading.

### M-3 (Medium). WC-9 relies on explicit flags that no row defines
- Experts: Wiegers, Nygard. WC-9 says outward defaults come back "only through the command's own explicit flag written in the brief" (SPEC:67) and D4 says the coordinator "passes the command's explicit flag" (SPEC:245). The inventories show auggie-review has only `--no-post-pr` (default posting; INV-A:38), and the rows for task and post-release name no authorization flag and list "Other required change: none" (SPEC:100,113,121). SPEC:100 mentions "an explicit `--post-pr`" as if it existed; it appears nowhere in the inventories. AC-4.2 tests "no authorization flags" (SPEC:209) without saying what they are. Also SPEC:154 says Phases 1-3 need no decision, but D4 lists auggie-review and task, which are P2 (SPEC:244,160).
- Recommendation: add the missing flag names to the "Other required change" column of those three rows, or state that authorization is out of scope until D4 is answered.

### M-4 (Medium). "Fresh dir" retry cannot be honoured when the coordinator passes the directory
- Experts: Nygard, Whittaker (Sequence attack). WC-6 says a retry must not corrupt the first attempt and that a command without a resume flag "writes each run into a fresh output directory" (SPEC:64); about 20 rows say "fresh dir" (SPEC:99-125). But WC-4 writes into "the directory the coordinator passed" (SPEC:62), and 2.3 never asks the coordinator to pass a new directory per attempt (SPEC:73). AC-3.2 even requires roadmap to "start fresh" in a directory that already holds `.session-memory.md` (SPEC:205), i.e. over the first attempt's files. Fix by one clause in 2.3 (the coordinator passes a new output directory for each `--retry-of`).

### M-5 (Medium). "Keep their fields" versus a fixed four-value `status`
- Experts: Fowler, Newman. WC-4 lets commands that already write a contract "keep their fields" (SPEC:62) while fixing `status` to `succeeded|partial|failed|blocked` (SPEC:62,262), and the live check asserts that set (SPEC:183). The existing contracts' status words are not listed anywhere (INV-B:272 only says contract 1.1 and `failed`). If an existing word differs, either the check fails or the rule is not followed. Name the existing words for the four contract-writing commands, or say `status` is the one field that is replaced.

### M-10 (Medium). `/sc:save` per-session keys are written but never read
- Expert: Cockburn (goal of the primary actor). SPEC:119 makes unattended save write only `<key>-<session-or-timestamp>.md`; `/sc:load` reads `<key>.md` only (INV-B:63) and its only change is a usage-line fix (SPEC:112). AC-3.4 checks that two new files appear and the single-owner files are unchanged (SPEC:207), so the test passes while the saved state is never loadable. Say who reads those files (for example the coordinator, by path from the contract) or accept that they are write-only.

## === ARCHITECTURE ANALYSIS ===

### M-6 (Medium). AC-C1 and SA-2 disagree about Orca text in `core/`
- Experts: Fowler, Newman. AC-C1 greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and requires no output in every phase (SPEC:172). P0 adds an Orca section to `HOW-WE-WORK.md` and a new `WORKER-CONTRACT.md` with a brief template (SPEC:158), and SA-2 allows Orca mentions only "as an example of a caller's question channel inside the contract file" (SPEC:147). Today the routing guide has zero mentions (SPEC:25). Any natural coordinator section names `orca orchestration …` and fails the P0 grep. Say that the grep excludes those two files, or that they avoid the literal command words.

### M-7 (Medium). WC-3 "may ask" makes AC-2.2 non-deterministic
- Experts: Adzic, Crispin. A worker that hits a gate "may instead ask the coordinator once" (SPEC:61); AC-2.2 requires `worker_done --outcome failed` with `status: blocked` (SPEC:200), and step 3 waits for `worker_done` (SPEC:182) although `question` is also in its type list. A conforming worker that asks produces no `worker_done` until answered. Add "in this check the coordinator does not answer, or the brief forbids `ask`".

### M-8 (Medium). Coordinator-side failure handling is thin
- Experts: Nygard, Hohpe. The spec says a command prompt produces "a silent stall with no `worker_done`" that the coordinator sees only through `worker-show` (SPEC:44), and Orca may not bound a Dispatch's run time (SPEC:282; CAPS:188), yet 2.3 lists only what the brief carries and what happens after `worker_done` (SPEC:73). Not stated: how long the coordinator waits before it treats a worker as stalled, what it does on the third failure (Orca fails the Task, CAPS:80,116), and how long a worker waits inside `ask` (SPEC:61; CAPS:68 UNVERIFIED default). `--retry-request` (CAPS:117) is not mentioned for the single `worker_done` of WC-5 (SPEC:63). Add a short coordinator duties list to 2.3 or mark these as deferred.

### M-9 (Medium). The tasklist row states a nesting fact the inventory marks UNVERIFIED, and picks a different fix
- Experts: Fowler, Whittaker (Accumulation). SPEC:122 says tasklist's reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`". INV-A:14 only states the limit; INV-B:46 marks tasklist's nesting UNVERIFIED and INV-B:314 lists it as an open question. INV-B:295 proposes removing the nested remediation; the spec instead passes `--unattended` so the reflect remediation auto-accepts (SPEC:88,122; INV-B:109), which hands off to `sc:workflow`, whose own Wave 4 runs reflect (INV-B:269-271) inside that same subagent, i.e. deeper than one layer. Recast the cell as UNVERIFIED, or keep `--no-reflect` as the worker default (SPEC:122 already calls it ready).

## === ADVERSARIAL ANALYSIS (Whittaker) ===

I can break this specification by **Zero/Empty attack**. The invariant at **WC-4 / section 2.3 (SPEC:62,73)** fails when **`--unattended` is passed with no `--output`**. Concrete attack: brief `/sc:analyze src/x.py --unattended`; before: no output directory known; WC-4 requires a contract "on every outcome" at `<output-dir>`; after: no path exists, the worker has nothing real for `--report-path` (CAPS:74 forbids placeholders) and no rule says to refuse. Severity MAJOR by label, Medium by consequence (M-1).

I can break this specification by **Divergence attack**. The invariant at **WC-4 (SPEC:62)** fails when **`--output` names a file**. Concrete attack: `/sc:tdd "auth component" --unattended --output docs/auth-tdd.md`; before: path is a file; after: the contract would be at `docs/auth-tdd.md/return-contract.yaml`, which cannot exist. Medium (M-1).

I can break this specification by **Sequence attack**. The invariant at **WC-6 / AC-3.2 (SPEC:64,205)** fails when **a retry gets the same output directory**. Concrete attack: attempt 1 of `/sc:roadmap --output D` fails after writing `D/.session-memory.md`; the coordinator re-sends the same brief with `--retry-of`; the command "starts fresh" in `D`, overwriting attempt 1's files. Medium (M-4).

I can break this specification by **Sentinel Collision attack**. The invariant at **section 1 / SA-1 (SPEC:51,146)** fails when **user content contains the token**. Concrete attack: `/sc:troubleshoot "login prints --unattended"`; whether the switch turns on is undefined. Minor (parsing rule, M-2).

I can break this specification by **Accumulation attack**. The invariant at **WC-6 plus the circuit breaker (SPEC:64; CAPS:80,116)** fails when **a fourth attempt is started**. Concrete attack: three `failed` dispatches; Orca fails the Task and says not to route around it; the spec names no coordinator action. Medium (M-8).

I could not break WC-5's mapping or WC-8's depth rule; both hold against the evidence at CAPS:73,97-102.

## Minor notes (never fail the review)

- N-1. E2 cites `CAPS:161` for "`[H:worker-start]` line 38, `--agent claude`" (SPEC:22), but CAPS:161 is the pr-submit top-level line; no CAPS line quotes `[H:worker-start]` line 38. The claim itself is supported by `INV-A:13` (EVIDENCE.md:45, UNVERIFIED here).
- N-2. The pr-submit top-level rule is cited as `SKILL.md:37-39` (SPEC:11,65; INV-A:10) but `CAPS:40,161` give `47-49` for the installed copy. Probably a copy offset; UNVERIFIED either way.
- N-3. `F1` and `F2` appear as labels at SPEC:159,195,196 with no definition anywhere in the spec.
- N-4. The 10/27/6 split (SPEC:76) counts pr-submit as a worker candidate, while D3's recommendation makes it coordinator-only (SPEC:238-242); the totals read 10/26/7 under the recommendation.
- N-5. The "Report shape" decision says adversarial "already write[s] `return-contract.yaml`" (SPEC:261) while 3.1 says its filename is not fixed (SPEC:83).
- N-6. WC-10 splits waits "longer than 5 minutes" into at most 4 minutes (SPEC:68); AC-4.3 fails any call over 240 s (SPEC:210). Align the thresholds.
- N-7. Unspecified edges with low consequence: roadmap resume flag with no state on disk (SPEC:118); pr-submit `--monitor 0` (SPEC:114).
- N-8. AC-C5's `grep -E '^-[^-]'` (SPEC:176) skips a deleted line that starts with `--` or `---`, such as a frontmatter fence moved by the business-panel fix (SPEC:102).
- N-9. Step 5 of the live check searches the transcript for the string `AskUserQuestion` (SPEC:184); loaded skill text mentions it (INV-B:49 quotes "never AskUserQuestion"), so the check needs "a tool call", not the word.
- N-10. The `return-contract.yaml` minimum fields (SPEC:62) carry no version field, although workflow's contract is versioned 1.1 (INV-B:272); consider one field for later evolution (Newman).
- N-11. WC-1 says "well inside" the 60 s limit without a number; the evidence gives 30 s passing and about 45 s failing (CAPS:49).
- N-12. The `business-panel` frontmatter move (SPEC:102) sits in P1, whose rule is "standalone behaviour unchanged" (SPEC:154), but its loading effect is UNVERIFIED (SPEC:278).

## Citation check (what I verified against the inventories)

Matched: E1 (CAPS:86,92), E4 (CAPS:155), E6 (INV-A:76-83,94-98; INV-B:289-299), R1 (CAPS:97-101,103), R2 (CAPS:147-149), R3 (CAPS:76,148,150), R4 (CAPS:145), R5 (INV-A:90; INV-B:285-286), WC-1 (CAPS:44-45,49), WC-3 (CAPS:58-61,64), WC-4 (CAPS:72-74,79), WC-5 (CAPS:73,76-77), WC-6 (CAPS:116), WC-10 (CAPS:130), WC-11 and 2.3 (CAPS:115 includes `[G:placement]` lines 8-11), WC-12 (CAPS:66-67), D5 (CAPS:97-99), UNVERIFIED 3-5, 10-11 (CAPS:178,180,186,68,188), the per-row `INV-A:35-55` and `INV-B:31-52` verdicts, the 10/27/6 totals (INV-A:73; INV-B:278), and the `INV-B:N` note ranges 57-65 through 267-275. Not matched: N-1. UNVERIFIED (sources not in the sandbox): every `cmd/…`, `sk/…`, `CLAUDE.md:…`, `EVIDENCE.md:…`, `pyproject.toml:38`, `install_core.py:…` and `Makefile:…` citation, and the claim that 11 locations were re-read on 2026-11-02 (SPEC:11).

## Follow-up candidates (Medium and minor; none triggers a revision)

M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10 and N-1 to N-12 above. Per CMD:260 the session that ran this review asks the user once per loop whether to open an issue for them. I could not ask in this run, so none is created and this list is only recorded.

## Brief clauses overridden

None. The brief narrowed nothing and widened nothing; FR-19's CRITICAL label for a count mismatch was graded by consequence (see the Quantity Flow Diagram), as CMD:259 requires.

## Process note

Two slips outside the instructed sandbox: while reading a large command output I opened two harness-saved copies of my own command outputs under `/root/.claude/projects/-home-user-IronClaude/…/tool-results/`, and I created then deleted one temporary file in the session scratchpad (`…/scratchpad/invb1.txt`). Neither holds anything outside the sandbox's own files; nothing else outside `aud2/` was read or changed, and the only file written inside it is this report.

## Reviser brief

Repair only the blocking finding B-1 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that B-1 does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS. Blocking ids: B-1.

verdict: FAIL
