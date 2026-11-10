review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (first review, whole document)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec; first review (no `--re-review`, no `--baseline`)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `395733f7a06e7778fe5ef57a893a4bf2e96dc6f3da91a7e9826eea38dedbd783` (285 lines)
- baseline: not given (first review)
- reviewer model used: claude-sonnet-5-5
- panel (focus order): Wiegers (lead, requirements), Adzic, Cockburn; Fowler (lead, architecture), Newman, Hohpe, Nygard; Whittaker (always active, after Fowler and Nygard)
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- mode: `--unattended` not passed; the user could not be asked about issues for the follow-up candidates, so none is opened (see the end of the report)

## Coverage

Read in full: the candidate, `.dev/orca-command-refactor/README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md` (cited lines spot-checked, listed below), and the review prompt file.

Checked and found consistent:
- Totals: 21 (`commands-a.md:3`) plus 22 (`commands-b.md:3`) is 43. The ready / needs-change / coordinator-only counts 5/13/3 (`commands-a.md:73`) and 5/14/3 (`commands-b.md:278`) sum to the spec's 10 / 27 / 6 (spec:76). The rows of spec 3.1 (10), 3.2 (27) and section 4 (6) match those counts.
- Phase tags in 3.2 (P1: 9 rows, P2: 11, P3: 4, P4: 3) agree with the phase rows of section 6 (spec:159-162).
- Orca-fact citations spot-checked against `orca-capabilities.md`: lines 44-47, 52, 58-61, 64, 66-68, 72-80, 84-92, 97-103, 107-116, 128-130, 135-139, 145-151, 155-161, 178-188 say what the spec attributes to them.
- Inventory citations spot-checked: `commands-a.md:14,35-55,60-61,73,95-98,106,113,118,120` and `commands-b.md:3,31-52,278-299,301,310,311,314,320,323` say what the spec attributes to them.
- README citations: `README.md:6,11-17,30,31,35` say what the spec attributes to them.

UNVERIFIED (not checkable inside this workspace, no file exists for them): every `cmd/`, `sk/` and `src/superclaude/cli/` path:line the spec carries over from the inventories; every `CLAUDE.md:N`, `HOW-WE-WORK.md:N`, `Makefile:N`, `pyproject.toml:38` citation; `EVIDENCE.md:35,39,45,56`; `.dev/codegraph-migration/...` citations; the "11 locations re-read" claim (spec:11) and the "about 340 citations re-read, 9 defects fixed" claim (spec:285). I treated them as the inventories' claims, not as facts.

Not triggered: Pipeline Dimensional Analysis (the spec describes no data pipeline whose stage counts diverge); `--focus correctness` is not active, so no State Variable Registry.

## === REQUIREMENTS ANALYSIS ===

### Blocking findings

**B1. CRITICAL (blocking). WC-4 defines the contract location as a directory, but three commands take a file in `--output`, and AC-2.2 does so too.**
- Expert: Wiegers (lead), Adzic.
- Grading sentence: an implementer who follows the stated text as written builds a contract path `<--output value>/return-contract.yaml`, and that is wrong because the same spec passes a file as `--output` for these commands. Two stated texts contradict each other.
- Stated text A, spec:62: "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"; the contract is `<output-dir>/return-contract.yaml`, and the worker passes that path as `--report-path`.
- Stated text B: spec:87 (init-lite brief passes `--output <file>`), spec:90 (tdd brief passes `--output <file>`; report is "the TDD at `--output`"), spec:120 (spec-panel row says "add `--output`; contract"), spec:200 (AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>`). The inventories agree that `--output` is a file for these (`commands-a.md:55`: `.dev/superclaude/context-audit.md` or `--output`; `commands-b.md:47`: "TDD file at `--output`").
- Concrete wrong outcome: for the tdd run of AC-2.2 the contract would be `<file>/return-contract.yaml`. On a blocked run the TDD file does not exist yet, so the command would create a directory named like the file and the next successful run could not write the TDD there. 7.2 steps 3 and 4 (spec:182-183) then check a path the spec never defines for these commands, so AC-2.2 cannot pass.
- The same ambiguity can be seen in the sibling command definition supplied with this audit: it uses `--report-dir` for the directory because `--output` is file-valued (`command.md:460-461`). That file is not part of the spec's evidence; it only shows the ambiguity is real.
- Recommendation: state one rule for the contract path when the output flag is a file (for example "the directory of that file" or a separate directory flag), and use it in WC-4, 3.1, 3.2 and AC-2.2. Priority High.

**B2. CRITICAL (blocking). The WC-4 contract is required for every worker but no phase gives it to six of the ten "ready" commands, yet the acceptance checks demand it.**
- Expert: Wiegers (traceability), Adzic (testability).
- Grading sentence: an implementer who follows the stated text as written builds no contract for tdd, troubleshoot, release-split, init-lite and brainstorm, and reflect keeps whatever fields it has, and that is wrong because AC-2.3 requires a contract with `status` in the four-value set and a non-empty `command` for each of them. A stated text that an acceptance criterion cannot pass.
- Stated texts: WC-4 (spec:62) requires `status` (four values), `command`, `report_path`, `artifacts` on every outcome and says commands that already write a contract "keep their fields and add the missing ones". The 3.1 header (spec:79) says "the worker reports the named file until Phase 1 adds the contract". The P1 row (spec:159) names only analyze, build, business-panel, design, document, explain, index, test, load and "fixes to adversarial, cleanup-audit, index-repo, workflow". The 3.1 rows for tdd (spec:90), troubleshoot (spec:91), release-split (spec:89), init-lite (spec:87) and brainstorm (spec:84, "Small fix: None") add no contract; reflect (spec:88) adds only a gate change. The P2 row (spec:160) and AC-2.1 (spec:199) cover gates only.
- AC-2.3 (spec:201) says the happy-path run of each P2 command passes the 7.2 check, and 7.2 step 4 (spec:183) runs `yaml.safe_load` on the contract and asserts `d['status']` and `d['command']`. For tdd the only report is the TDD markdown, so the check fails or errors. For troubleshoot the report is `REPORT.md` (`commands-b.md:49`). Brainstorm's and reflect's existing contracts are not shown to carry `command` or the four-value `status`; the spec never checks.
- Recommendation: add a row (or a clause in P1/P2) that adds the WC-4 contract to tdd, troubleshoot, release-split, init-lite, brainstorm and reflect, or narrow WC-4 and 7.2 step 4 to say which existing report satisfies them. Priority High.

### Medium findings (warnings, listed under follow-up candidates)

**M1. MAJOR label, graded Medium. WC-6 "fresh output directory" and WC-4 "path known before dispatch" can be read against each other.**
- Expert: Nygard, Wiegers.
- Spec:64 says a command with no resume flag "writes each run into a fresh output directory"; about 20 rows of 3.2 are "fresh dir". Spec:62 says the contract is at `<output-dir>/return-contract.yaml`, known before dispatch, and 7.2 step 3 (spec:182) checks the report path is that path. A retry worker (`--retry-of`) re-uses the Task spec (`orca-capabilities.md:116`), so the same `--output` is passed again.
- Reading 1 (the command makes a new subdirectory) breaks WC-4; reading 2 (the coordinator passes a new directory per attempt) is never stated, since spec:73 does not list it among what the coordinator owes each worker. The finding needs a guess about which reading the implementer picks, so it is Medium.
- Recommendation: in spec:73 add "a new output directory per attempt" and reword WC-6 as a coordinator duty for fresh-dir commands.

**M2. MAJOR label, graded Medium. Requirements owned by the "Worker session" have no stated carrier.**
- Expert: Fowler, Cockburn.
- WC-3, WC-5, WC-7 and WC-12 (spec:61, 63, 65, 70) are duties of the Claude session that received the Orca preamble, not of any command. Commands only get a short section pointing at `WORKER-CONTRACT.md` (spec:52), and a command run by a person must not change behaviour (SA-1). Nothing says the worker is told these rules: spec:73 lists what the brief carries and omits them; the P0 row (spec:158) says the template lists "the section 3.1 flags". The outcome mapping of WC-5 (blocked maps to failed, partial to succeeded) is not in Orca's own preamble (`orca-capabilities.md:73`).
- Recommendation: state that the coordinator brief template carries WC-3, WC-5, WC-7 and WC-12 verbatim, and add that to 2.3.

**M3. MAJOR label, graded Medium. No rule makes `--unattended` reach nested invocations.**
- Expert: Fowler, Hohpe.
- Commands call other commands or skills: tdd calls `/task` (spec:90), tasklist calls reflect (spec:122), workflow calls reflect (`commands-b.md:52,269`), brainstorm and roadmap call adversarial (`commands-a.md:39`, `commands-b.md:40`). WC-2 (spec:60) is written for "the command". Only the tdd and tasklist rows address a nested call. The task skill's own gates (confidence below 0.70, TFEP; spec:121) are a P2 item, so a tdd run in P2 may still reach them through `/task`.
- Recommendation: add a one-line propagation rule (pass `--unattended` to every nested command or skill that accepts it, else resolve its gates as blocked) to section 2.

**M4. MAJOR label, graded Medium. WC-10 covers Bash waits only, but Agent-tool calls also block the session.**
- Expert: Nygard.
- Spec:68 says a command step that blocks "a single tool call" for over 5 minutes must be split. Only cli-eval and pr-submit are listed (spec:104, 114). Commands with heavy Agent-tool fan-out (adversarial, tdd, cleanup-audit, brainstorm; `commands-a.md:35,39,42`) block one tool call while subagents run, and the P0 smoke runs use two of them (spec:158). Whether a missed heartbeat matters is UNVERIFIED (`orca-capabilities.md:130,182`), so this is a warning.
- Recommendation: either scope WC-10 to polling and eval waits, or say what the heartbeat duty is during an Agent-tool call.

**M5. MINOR label, graded Medium. AC-2.2 and WC-3 can disagree.**
- Expert: Crispin (completeness).
- WC-3 (spec:61) lets a blocked worker `ask` the coordinator. AC-2.2 (spec:200) expects `worker_done --outcome failed` with `status: blocked`. A worker that asks, as WC-3 allows, produces a `question` message instead, and the AC cannot pass. The AC does not say the brief forbids `ask`.
- Recommendation: say that AC-2.2 runs with a brief that does not permit `ask`.

**M6. Medium. `--unattended` with no output directory is unspecified.**
- Expert: Whittaker (Zero/Empty attack), Wiegers.
- Spec:62 and 73 say the brief passes the directory. Several 3.2 rows add `--output` as optional ("add `--output`; contract"). Nothing states what a command does when `--unattended` arrives with no output directory. Writing the contract nowhere would break WC-4; stopping blocked has no place to write the report. See the boundary table, row G1.
- Recommendation: one sentence in WC-4 (refuse before any work and print the refusal in chat only, or default to a fixed path).

**M7. Medium. Tasklist under `--unattended` turns on reflect remediation, against the inventory's recommendation, with no Decision entry.**
- Expert: Nygard, Fowler.
- Spec:122 has Stage 10.5 pass `--unattended` to each reflect so the headless auto-accept rule applies. `commands-b.md:46,295` recommend dropping `--remediate` in Stage 10.5 and note it runs inside subagents. The spec's Decisions table (spec:258-269) records no reason for the opposite choice, and UNVERIFIED 9 (spec:280) says the spec assumes an Orca worker is not headless. What the auto-accept does (a corrective tasklist package via sc:workflow) is in a skill file not available here: UNVERIFIED. Order inside P2 is also unstated (spec:160): tasklist needs reflect's `--unattended` first.
- Recommendation: record the choice in Decisions with its consequence, and order reflect before tasklist.

**M8. Medium. "No user decision needed" for Phases 1-3 conflicts with D1.**
- Expert: Cockburn.
- Spec:154 says "Phases 1-3 need no user decision"; spec:51 and 225-230 say D1 (the switch itself) is open and phases 0-3 only proceed "on the recommendations". Every phase depends on D1. Also spec:16 says command changes are "limited to" the contract, while 3.2 also lists drift, tools and frontmatter changes (spec:102, 108, 118, 124, 125).
- Recommendation: align the three statements.

**M9. Medium. AC-C1 text is wrong as written and conflicts with SA-2.**
- Expert: Crispin, Whittaker.
- (a) The pattern at spec:172 contains `\|` inside `grep -E`. In GNU grep -E that is a literal `|`; I ran the pattern with `\|` on `orca-ide orchestration x` and it did not match, while the unescaped alternation matched. The backslashes look like markdown table escapes, but a reader copying the source text gets a check that always prints nothing. The same escaping appears in AC-C4 (spec:175).
- (b) SA-2 (spec:147) allows Orca to be mentioned inside the contract file, which lives in `src/superclaude/core/` (spec:52), and AC-C1 scans that directory excluding only `ccsession-tag`. If the contract file names `orca orchestration ask` or `check` (WC-3, WC-12) the P0 check fails. Whether it will is not stated.
- Recommendation: give the command without table escapes, and either exclude `core/WORKER-CONTRACT.md` or forbid the verbs in it.

### Minor notes (never fail the review)

- n1. Labels `F1` and `F2` (spec:62, 73, 76, 83, 92, 159, 182, 195, 198) and "ladder rung 2" (spec:261) are used but never defined in the document; they appear to come from an absent review or ladder. The sentences around them stand alone, so nothing breaks.
- n2. Non-goal 8 (spec:220) limits scope to defects that stop a worker, but the `/sc:load` usage-line fix (spec:112, 149) does not.
- n3. AC-0.4 (spec:194) says the adversarial smoke run uses "the command's existing report file", but the inventory records that adversarial's contract path is not fixed (`commands-a.md:60`). The check should name where to look.
- n4. WC-5 (spec:63) does not say what the worker does with an unparsable or out-of-vocabulary `status`; "no report exists" is the only failure case named (boundary table row G2).
- n5. Counts of INV citations in the "Citation conventions" are fine; the "Orca guide citations" are keyed via `CAPS:10-21` and the keys exist (`orca-capabilities.md:10-21`).

## === ARCHITECTURE ANALYSIS ===

Expert view (Fowler, Newman, Hohpe, Nygard): the decision to keep Orca above the commands (spec:16, 1.2, 1.3) is supported by the Orca facts as quoted: nesting depth 1 (`orca-capabilities.md:97-98`), lifecycle messages bound to the dispatched pane (`:76,150`), standalone use without Orca (`:147-149`). The rejected alternative is argued from those facts and marks its own unverified step (`:103`). The boundaries are clean: the contract is written once and referenced by installed path (spec:52, 264), and commands carry no Orca calls (SA-2, WC-8). The integration contract is a file plus one lifecycle message, which is a sound minimal exchange pattern.

Architecture-side findings are the ones above that touch interfaces: B1 (report path interface), B2 (report interface not defined for six commands), M1 (retry and output ownership), M2 (who carries the worker-side protocol), M3 (nested invocation boundary), M4 (liveness during blocking calls). No separate architecture-only blocker was found.

Whittaker, attacks that did not produce a finding:
- **Sequence Attack** on the phase order: P2 reflect and tasklist are in the same phase, tasklist depends on reflect's flag (M7). Phase 4 items wait on D2-D4 and cannot run earlier because section 6 gates them (spec:154). No wrong outcome beyond M7.
- **Accumulation Attack** on retries: three consecutive failed starts trip the circuit breaker, but a worker's own `failed` report does not (`orca-capabilities.md:80`), so blocked outcomes mapped to `failed` (WC-5) cannot trip it. OK.
- **Sentinel Collision Attack**: `partial` mapped to `succeeded` (spec:263) is disclosed in the first sentence of the body and the contract (WC-5), so the sentinel is not hidden.

## Guard Condition Boundary Table

Guards found: the contract path rule (WC-4), the outcome mapping (WC-5), the retry rule (WC-6), the 5-minute / 4-minute wait rule (WC-10), the depth-1 limit (R1), the 60-second readiness limit (WC-1), `--interactive` refusal (3.2). Classes left out, one line each: "Maximum/Overflow" for WC-4, WC-5 and WC-6 cannot occur (no capacity); "Sentinel Value Match" for WC-1, WC-10 and R1 cannot occur (numeric limits with no reserved value).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| WC-4 contract path | spec:62 | Zero/Empty | no output directory in the brief | true (not satisfiable) | none stated for `--unattended` without a directory | GAP (M6) |
| WC-4 contract path | spec:62, 87, 90 | Legitimate Edge Case | `--output` is a file | false | contradicts spec:62 | GAP (B1) |
| WC-4 contract set | spec:62, 159, 160 | Typical | tdd happy path | contract required | no row adds it | GAP (B2) |
| WC-5 outcome mapping | spec:63 | Zero/Empty | no report exists | true | `--outcome failed` | OK |
| WC-5 outcome mapping | spec:63 | Typical | `partial` | true | `--outcome succeeded`, status in body | OK |
| WC-5 outcome mapping | spec:63 | Legitimate Edge Case | unparsable file or unknown `status` | true | not stated | GAP (n4, minor) |
| WC-6 retry rule | spec:64, 73 | Typical | `--retry-of` with the same `--output` | true | writer or coordinator creates the fresh directory is not stated | GAP (M1) |
| WC-10 wait split | spec:68 | One/Minimal | one Bash wait of 5 minutes | true | split into waits of at most 4 minutes | OK |
| WC-10 wait split | spec:68 | Legitimate Edge Case | one Agent-tool call longer than 5 minutes | not covered | not stated | GAP (M4) |
| Depth limit | spec:33 | Typical | worker calls `worker-start` | true | refused with `nested_worker_depth_exceeded`, work done in place | OK |
| `--interactive` under `--unattended` | spec:100, 103, 110, 118 | Legitimate Edge Case | `--interactive` and `--unattended` together on adversarial, brainstorm, release-split | true | only "never `--interactive`" in the brief (spec:83-84, 89), no command-side refusal | GAP (minor) |

All GAP entries above are listed with their grade: B1 and B2 are blocking, the rest are Medium or minor and follow the grading section of the command.

## Quality assessment (0-10)

Clarity 7, Completeness 6, Testability 6 (two acceptance checks are wrong as written: B1, M9, and the grep in B3), Consistency 6. The design decision and the evidence handling are strong: gaps are stated (spec:41-45), verdicts trace to inventory lines, and every open question is listed with a recommendation.

## Blocking finding B3 (listed here to keep the buckets together)

**B3. MAJOR, graded blocking. AC-C5 and AC-0.3 cannot detect deleted bullet lines, so "additive" can pass when it is not.**
- Expert: Crispin (completeness), Whittaker (Zero/Empty attack on the check).
- Grading sentence: an implementer who follows the stated text as written builds `git diff -U0 ... | grep -E '^-[^-]'` as the proof that edits are additive (SA-4, SA-5), and that is wrong because a deleted markdown bullet `- item` appears in a diff as `-- item`, which the pattern excludes.
- Location: AC-C5 (spec:176) and AC-0.3 (spec:193).
- Check: I ran the pattern over `-- item` / `--- a` / `- x`; it printed only `- x`, not `-- item`. Bullets and `---` frontmatter delimiters are used throughout command and skill files, so removing them passes the check. SA-4 (spec:149) and SA-1 rely on this check to show a person's behaviour is unchanged.
- Recommendation: use a pattern that skips only the file headers, for example `grep -E '^-' | grep -vE '^--- '`, or `git diff --numstat` with a zero-deletions condition. Priority High.

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium: M1 (retry directory ownership), M2 (carrier for worker-session rules), M3 (nested invocation propagation), M4 (Agent-tool waits and heartbeat), M5 (AC-2.2 versus `ask`), M6 (no output directory), M7 (tasklist remediation choice and order), M8 (decision statements), M9 (AC-C1 text and SA-2).
Minor: n1 to n5 and the `--interactive` GAP of the boundary table.

Per the command, the session that runs the review asks the user once per loop whether to open an issue for these. There is no user channel in this sandbox, so no question was asked and no issue was created.

## Reviser brief

Blocking finding ids: B1, B2, B3.

Rules for the reviser (restated from the command's Review Loop, bullet 6, because the reviser reads this report, not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone; do not award yourself a PASS.

What each id names: B1 is spec:62 against spec:87, 90, 120, 200 (contract path when `--output` is a file). B2 is spec:79, 159, 160 against spec:84, 87-91, 183, 201 (contract for the ready commands). B3 is the grep pattern at spec:176 and 193.

Precedence note: the audit label asked for a whole-document first review; no brief clause was overridden.

verdict: FAIL
