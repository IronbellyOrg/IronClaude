review: 1 of 3

# Spec-panel critique (round 1): Orca worker-contract spec

- mode: critique, first review (no `--re-review`, no `--baseline`; the full document is reviewed)
- focus: requirements, architecture
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: missing (not given; first review)
- reviewer model: claude-haiku-5-5, one reviewer. The `superclaude review panel` command is not installed in this sandbox, so one reviewer ran. The coordinator should note that in the loop summary.
- brief used: FIRST-REVIEW prompt, read in full from `home/.claude/rules/prompts/document_review_loop_prompts.md` in the sandbox home
- Read first: `.dev/orca-command-refactor/README.md` (binding shared context) and the three inventories.

Citation key. `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N` = `inventory/commands-a.md`, `inventory/commands-b.md`. `CAPS:N` = `inventory/orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `command.md:N` = the spec-panel command definition supplied for this run, in the sandbox. Any other citation (for example `src/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`) is not in the workspace and is UNVERIFIED here.

## Verdict summary

Four blocking findings are open: F1, F2, F3, F4. Twenty-three non-blocking findings are listed under follow-up candidates. The verdict is FAIL.

## Coverage

- Read in full: the candidate (all 285 lines), README, `commands-a.md`, `commands-b.md`, `orca-capabilities.md`, and the FIRST-REVIEW prompt.
- Checked the inventory citations the candidate uses in sections 1 to 9 against the inventory lines. I checked about 40 of them, including every anchor used in the findings block. They match their cited lines. I found no wrong inventory citation. The rest are UNVERIFIED in the sense that I did not re-read them.
- Checked the totals: the spec's 10 ready, 27 needs-change and 6 coordinator-only (`spec:76-126`) match the inventory summaries (`INV-A:73` 5/13/3 and `INV-B:278` 5/14/3).
- Ran the AC-C1 grep pattern (`spec:172`) against sample input in the sandbox. Result in F3.
- Did not check repository citations (`src/`, `docs/`, `.dev/evals/`, `.dev/codegraph-migration/`). They are UNVERIFIED here.
- Pipeline Dimensional Analysis: not triggered. The spec has no multi-stage data flow whose item count changes. The status mapping (`spec:63`) and the Task waves (`CAPS:86-92`) are not count-changing pipelines. No Quantity Flow Diagram is required.
- `--focus correctness` is not active, so the State Variable Registry is not required.

## === REQUIREMENTS ANALYSIS ===

### F1 (CRITICAL, BLOCKING, contradiction). The P0 smoke runs cannot follow the brief rule in section 2.3

- Issue: `spec:73` says each Task brief carries "the exact command line including `--unattended`". The live check (`spec:180`, step 1) builds each run from that brief, and AC-0.4 (`spec:194`) runs `/sc:troubleshoot`, `/sc:workflow --handoff none` and `/sc:adversarial` through it in P0. `spec:79` says these commands "run as workers now if the brief uses the stated flags". Their stated flags (`spec:83`, `spec:91`, `spec:92`) do not include `--unattended`. The flag arrives in P1 (`spec:159`) and P2 (`spec:91`).
- Grading check: an implementer who follows the stated text as written builds a P0 brief for `/sc:troubleshoot` that carries `--unattended`. P0 does not add that flag to the command, so AC-0.4 cannot pass as written.
- Severity: CRITICAL. Blocking. Category: contradiction.
- Expert: Wiegers.
- Recommendation: say per command whether the P0 brief omits `--unattended`, and say that the step-1 command line is then run without it. Or move the three P0 runs to after the P1 change for each command.
- Priority: High. Quality impact: testability 5 to 7, consistency 5 to 7.

### F2 (MAJOR, BLOCKING, contradiction). brainstorm and init-lite get no change, but P1 and AC-1.1 require the flag and a section

- Issue: `spec:79` says "The only command changes are the small fixes in the last column." The rows for brainstorm (`spec:84`) and init-lite (`spec:87`) say "None" in that column. But `spec:159` (P1) requires "the `--unattended` flag accepted by every command in sections 3.1 and 3.2". AC-1.1 (`spec:195`) asserts "every command in sections 3.1-3.2 has a `## Unattended mode` section". Under `spec:73` their briefs must carry `--unattended`.
- Grading check: an implementer who follows §3.1 leaves these two commands unchanged. AC-1.1 then fails for them, and the §2.3 brief cannot carry the flag they do not accept.
- Severity: MAJOR. Blocking. Category: contradiction.
- Expert: Wiegers, Cockburn.
- Recommendation: add the flag and the section to the brainstorm and init-lite rows as an explicit change, or drop those two from AC-1.1 and from the §2.3 rule.
- Priority: High. Quality impact: consistency 5 to 7.

### F3 (MAJOR, BLOCKING, unpassable-check). AC-C1 can never fail

- Issue: `spec:172` writes `\|` inside `grep -E`. In an extended regex, `\|` is a literal `|`, not alternation. I ran the pattern in the sandbox. Input `orca orchestration worker-start` gave no match (exit 1). The same pattern with `|` in place of `\|` matched it (exit 0). So AC-C1 prints nothing for any input.
- Consequence: SA-2 (`spec:147`: no command, skill or agent runs an `orca` command) and WC-8 (`spec:66`) have no working mechanical check. AC-C1 is a common check that every phase must pass (`spec:169-176`, `spec:167`: "A phase passes only when every check ... passes").
- Grading check: an implementer who runs AC-C1 as written, on a command file containing `orca orchestration worker-start`, gets no output and records the check as passed, while SA-2 is violated. The criterion cannot fail.
- Severity: MAJOR. Blocking. Category: unpassable-check (the criterion is not a working check).
- Expert: Wiegers (testability).
- Recommendation: use `grep -E` with `|`, or `grep -G` with `\|`. Scope the pattern as F21 requires.
- Priority: High. Quality impact: testability 5 to 8.

### F4 (CRITICAL, BLOCKING, other). WC-5 maps an unknown or missing status to success

- Issue: `spec:63`: "`--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise, including `partial`". "Otherwise" includes a contract whose `status` key is missing or empty, a value outside the four-value set (for example `status: ok`), and a file that exists but cannot be parsed. The four-value set is fixed by `spec:62`.
- Grading check: an implementer who follows the stated text as written sends `--outcome succeeded` for a contract with `status: ok`. The coordinator then reads a success, and a dependent Task can start on a result nobody could read. Dependents stay blocked only on a failed Task (`CAPS:90`), and Orca does not start ready Tasks itself (`CAPS:92`). This is a stated text that produces a wrong outcome; under the Guard rule (FR-8) it is blocking.
- Severity: CRITICAL. Blocking. Category: other (fail-open mapping).
- Expert: Whittaker (sentinel collision, zero or empty input).
- Recommendation: map `succeeded` and `partial` to success explicitly. Map every other value, a missing file, a missing `status` and an unparseable file to `failed`. The `partial` decision (`spec:263`) then stays as written.
- Priority: High. Quality impact: completeness 7 to 8, testability 5 to 7.

### F5 (MAJOR, not blocking, other). WC-2 says three resolutions, WC-3 adds a fourth path

- Issue: `spec:60`: "Each gate resolves one of three ways". `spec:61`: "the session may instead ask the coordinator once with the preamble's `ask` command". The two are not provably in conflict, because the ask comes before resolution (c). But the spec does not say whether an answer changes the command's resolution, or whether the worker's outcome changes.
- Recommendation: state that an answer re-invokes the command with the flag from resolution (b), and that WC-2 still applies. Say which outcome the worker reports while it waits.
- Expert: Wiegers.

### F6 (MAJOR, not blocking, missing-requirement). "same tools" is unsupported, and tool-permission prompts are not covered

- Issue: `spec:22` says a worker "has the same tools as a command a person runs". `CAPS:161` supports only that the worker is a top-level Claude process started with `--agent claude`. `CAPS:47` supports only that the task arrives on the command line. Nothing in the inventories gives the worker's permission mode. WC-2 (`spec:60`) lists AskUserQuestion, chat questions and `[yes / no]` offers, but not a tool-permission approval, which is also a person-blocking step.
- Consequence: if the worker runs in a prompting permission mode, it parks on approvals, and `agentWait` (`CAPS:129`) reports it as healthy. Whether this happens is UNVERIFIED. The text does not say.
- Expert: Cockburn (who answers the prompt), Nygard (silent stall).
- Recommendation: state the permission mode the worker runs with (UNVERIFIED, to be checked live). Add tool-permission prompts to WC-2 and to the §7.2 checks. Remove "same tools" unless it is verified.
- Note: this could become blocking if Orca launches in a prompting mode.

### F7 (MAJOR, not blocking, other). The evidence for "worked before" and "only proof is nested" conflict

- Issue: `spec:23` (E3) cites the P3 return contract, `invocation_method: "skill-direct"` (`INV-A:13`), as evidence that the approach "has worked before". `spec:43` (§1.4) says "The only end-to-end proof is the PR #329 run ... so it proves the nested route, not the direct route this spec requires." The spec does not say whether the P3 run and the PR #329 run are the same run.
- Consequence: the direct route is both proven (E3) and unproven (§1.4). That bears directly on the decision in section 1.
- Recommendation: name the run behind each evidence line, and say which one shows the direct route.
- Expert: Wiegers (evidence traceability).

### F8 (MAJOR, not blocking, other). The §1.1 scope sentence is wider than the text

- Issue: `spec:16`: "What changes in the commands is limited to the worker contract in section 2." Section 3 also changes commands for reasons outside section 2: roadmap flag reconciliation (`spec:118`), validate-tests target (`spec:125`), load usage line (`spec:112`), business-panel frontmatter (`spec:102`). SA-4 (`spec:149`) names these as defect fixes.
- Recommendation: rewrite `spec:16` as "section 2 plus the defect fixes that SA-4 names".
- Expert: Fowler.

### F9 (MAJOR, not blocking, other). §8.8 excludes the agent frontmatter defect, but P1 includes a business-panel frontmatter fix

- Issue: `spec:220` (§8.8): "Only defects that stop a command working as a worker are in scope", and it names `/sc:agent`'s missing opening frontmatter line as out of scope. `spec:102` puts the business-panel frontmatter move in §3.2, and P1 (`spec:159`) includes business-panel. The effect on loading is UNVERIFIED (`spec:278`, UNVERIFIED 7).
- Consequence: the same class of defect is in scope for one command and out of scope for another.
- Recommendation: either show that the business-panel defect stops a worker, or move it out of scope like the agent defect.
- Expert: Cockburn, Wiegers.

### F10 (MAJOR, not blocking, other). SA-3 and SA-4 disagree over the adversarial contract rename

- Issue: `spec:148` (SA-3): "A standalone default run writes the same files it writes today." `spec:149` (SA-4): a fix may "correct a documented defect". `spec:83` makes the P1 adversarial fix "Fix the contract filename to `<output>/adversarial/return-contract.yaml`". A standalone adversarial run writes a contract today (`INV-A:35`), under a name that varies on disk (`INV-A:60`). Renaming it changes the file that a standalone run writes.
- Recommendation: state that SA-4's exception overrides SA-3 for renamed paths. Or keep the current name as well, so a standalone run writes the same files.
- Expert: Wiegers.

### F11 (MAJOR, not blocking, other). WC-6 does not allow implement's implicit resume, and retry briefs do not require a new output directory

- Issue: `spec:64` (WC-6): a command "resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory". `spec:109` gives implement "`--resume` (implicit when a ledger matches)" (`INV-A:51`). A retry of implement with the same slug resumes with no flag, which WC-6 does not allow. `spec:73` does not require a new output directory for a retry, so a retry of a fresh-directory command can reuse the first attempt's directory.
- Recommendation: require a new output directory in every retry brief. Make implement's resume an explicit flag in the brief.
- Expert: Wiegers, Nygard.

### F12 (MAJOR, not blocking, missing-requirement). No general rule when a brief passes both `--unattended` and `--interactive`

- Issue: `spec:60` (WC-2) and the per-command rows, for example `spec:103` ("`--interactive` refused"), give no general rule. A brief that passes both is not covered. The result is undefined, and a stall is possible.
- Recommendation: state one rule. Either `--unattended` wins and `--interactive` resolves as blocked, or the brief is refused.
- Expert: Whittaker (divergence).

### F13 (MAJOR, not blocking, missing-requirement). No rule when `--output` is missing under `--unattended`

- Issue: `spec:62` (WC-4) says the contract goes to "the directory the coordinator passed". The spec does not say what happens when none is passed. `INV-A:61` shows adversarial then writes next to its input files. The report path is then not known before dispatch, which `spec:73` requires.
- Recommendation: under `--unattended`, a missing output flag resolves as blocked (WC-2 (c)).
- Expert: Whittaker (zero or empty input), Wiegers.

### F14 (MAJOR, not blocking, missing-requirement). `worker_done` exactly once, with no rule for a lost response

- Issue: `spec:63` (WC-5) says "sends `worker_done` exactly once". It does not say what the worker does when the send's response is lost. `CAPS:117` documents `--retry-request <id>` for every orchestration mutation.
- Recommendation: state that the worker uses `--retry-request` for `worker_done`, with the same ID on each retry.
- Expert: Hohpe.

### F15 (MAJOR, not blocking, missing-requirement). The coordinator's next step after partial or blocked is not specified

- Issue: `spec:73` says the coordinator "opens the report file, then releases or reuses the worker". It does not say who answers a `blocked_question`, or whether a `partial` result may start dependent Tasks. Orca does not start ready Tasks by itself (`CAPS:92`).
- Recommendation: add a coordinator rule for each status: `succeeded` may start dependents, `partial` may only with a stated decision, `blocked` surfaces the question to the person or to a later brief, and `failed` follows the retry rule.
- Expert: Cockburn (actor and next step).

### F16 (MAJOR, not blocking, testability). §7.2 step 2 cannot run as ordered, and "never non-null" passes when the field is absent

- Issue: `spec:181` (step 2) requires `worker-show` "at least once per 5 minutes". Step 3 (`spec:182`) is one `check --wait` with `--timeout-ms 900000`, so step 2 cannot run during it. The pass condition, "`observation.agentWait` is never non-null", holds when the field is absent. `CAPS:129` says an absent field means Orca never looked.
- Recommendation: loop with waits of at most 240000 ms and a `worker-show` between each. Require that the field is present (null or non-null) at each observation.
- Expert: Adzic (acceptance procedure).

### F17 (MAJOR, not blocking, testability). §7.2 step 5 checks less than WC-2 and WC-7 require, and AC-0.4 claims more

- Issue: `spec:184` (step 5) searches only for `AskUserQuestion`. WC-2 (`spec:60`) also forbids chat questions and `[yes / no]` offers. AC-0.4 (`spec:194`) says WC-7 (no Agent-tool wrapper) is "verified in the step-5 transcript". Step 5 does not check that.
- Recommendation: extend step 5 to the WC-2 patterns and to the wrapper check, or drop the WC-7 claim from AC-0.4.
- Expert: Adzic, Wiegers.

### F18 (MAJOR, not blocking, missing-requirement). WC-10 covers command steps, not top-level Agent-tool waits

- Issue: `spec:68` (WC-10) covers "a command step that blocks a single tool call for longer than 5 minutes (a poll wait, a long eval)". A top-level Task or Agent call that waits for subagents also blocks the session, and the session cannot heartbeat while it waits (`CAPS:64`, `CAPS:130`). Fan-out commands do this (`INV-A:42`, `INV-B:33`).
- Recommendation: say whether Agent-tool waits are covered. If they are not, state the accepted gap.
- Expert: Nygard.

### F19 (MAJOR, not blocking, other). The tasklist "none" verdict rests on nesting that the inventories mark UNVERIFIED

- Issue: `spec:122` says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`". `INV-B:210` calls subagent-to-agent spawning UNVERIFIED. `INV-B:314` (item 1) and `INV-B:322` (item 8) list it as open. The spec's UNVERIFIED list (`spec:271-285`) does not include it.
- Recommendation: add it to the spec's UNVERIFIED list, and make the tasklist verdict conditional on it.
- Expert: Fowler, Nygard.

### F20 (MAJOR, not blocking, other). The tdd and release-split "ready" claims depend on prompts the brief cannot switch off

- Issue: `spec:90` (tdd) says "a precise component prompt, not a bare topic" makes it ready. `INV-B:219` says the nested `/task` asks the user when several task files match or an item looks wrong, and the brief cannot prevent that. `spec:89` (release-split): a tasklist-shaped input triggers a "confirm with user" (`INV-B:119`).
- Recommendation: mark tdd ready only for inputs that `/task` will not query, or move it to needs-change with the nested prompts listed.
- Expert: Wiegers.

### F24 (MAJOR, not blocking, other). WC-4 fixes the status vocabulary, but existing contracts keep their fields

- Issue: `spec:62` (WC-4) says `status` is "one of `succeeded`, `partial`, `failed`, `blocked`", and also says "Commands that already write a contract keep their fields and add the missing ones". Existing contracts (for example the workflow contract 1.1, `INV-B:272`) may use other status values. The spec does not say whether they are renamed or mapped.
- Recommendation: give a per-command mapping, or state a version change for each contract.
- Expert: Newman (contract evolution).

## === ARCHITECTURE ANALYSIS ===

### F21 (MAJOR, not blocking, other). SA-2 permits an Orca mention that AC-C1 would reject once F3 is fixed

- Issue: `spec:147` (SA-2) allows an Orca mention "inside the contract file". The contract file is installed from `src/superclaude/core` (`spec:52`). `spec:158` (P0) adds an Orca section to `HOW-WE-WORK.md`, also in core. AC-C1 (`spec:172`) scans `src/superclaude/core` and excludes only `ccsession-tag`. Once F3 is fixed, the permitted mentions fail the check.
- Recommendation: scope AC-C1 to commands, skills and agents. Exempt the contract file and the routing guide's Orca section by name.
- Expert: Fowler (boundary definition).

### F22 (MAJOR, not blocking, other). cli-portify keeps a hardcoded `src/superclaude` lookup, and P2 edits the same file

- Issue: `spec:105` keeps "dispatch only inside an IronClaude checkout (hardcoded template path)", and P2 (`spec:160`) edits cli-portify. `INV-A:45` and `INV-A:68` show the skill reads `src/superclaude/examples/release-spec-template.md`. The repo rule that installed primitives must not point at `src/superclaude` paths is stated in the repo CLAUDE.md, which is in the session context and not in the workspace, so it is UNVERIFIED here. The spec does not address it.
- Recommendation: repoint the lookup to the installed copy, or record the exception and its scope.
- Expert: Fowler, Newman.

### F23 (MAJOR, not blocking, other). The spec-panel row describes a different command version from the one supplied for this run

- Issue: `spec:120` says spec-panel has no `--output`, needs a contract, and has no unattended mode. `INV-B:182` says no `--output` exists. The spec-panel command supplied for this run lists `[--output <file>] [--unattended] [--report-dir <dir>]` (`command.md:23`) and has a `## Unattended mode` section that cites `~/.claude/WORKER-CONTRACT.md` (`command.md:455-465`).
- Consequence: either the candidate is stale, or the command in the working tree already differs from what the spec read. Both cannot be right.
- Recommendation: record which version each inventory read, and re-check the spec-panel row and any P2 work on it.
- Expert: Wiegers (baseline).

### F25 (MINOR, other). R1 states a refusal as a fact, but the enforcing call sites are UNVERIFIED

- Issue: `spec:33` (R1) says a command that calls `worker-start` "would be refused with `nested_worker_depth_exceeded`", and in the same cell says the enforcing call sites are presumed (`CAPS:103`).
- Recommendation: write "presumed to be refused".
- Expert: Fowler.

### F26 (MINOR, missing-requirement). The installed contract is untested

- Issue: `spec:52` installs `WORKER-CONTRACT.md` to `~/.claude/`. AC-0.1 (`spec:191`) tests only `KNOWN_CORE_FILES`. No check confirms that an installed command finds the file, or that an older install without it fails clearly.
- Recommendation: add an install-and-read check, and a clear message when the file is missing.
- Expert: Newman.

### F27 (MINOR, other). An evidence-validator pass is claimed but not reproducible here

- Issue: `spec:285` (UNVERIFIED 14) reports an evidence-validator pass with nine fixes. It is not in the workspace and cannot be checked here.
- Action: none. Noted for the coordinator.

## Probes (Whittaker, always active)

- Divergence attack. I can break this specification by **divergence (`--unattended` with `--interactive`)**. The invariant at **§3.2 cleanup row and WC-2 (`spec:60`, `spec:103`)** fails when **a brief passes both flags**. Concrete attack: the brief passes `--unattended --interactive`. The per-command refusal only covers the commands that name it, so the rest run the interactive path and stall. (F12, MAJOR, not blocking.)
- Zero or empty attack. I can break this specification by **zero or empty input (no `--output`)**. The invariant at **WC-4 (`spec:62`)** fails when **the brief omits the output directory**. Concrete attack: the adversarial command defaults to the input file directory (`INV-A:61`), so the report lands next to its inputs and the path the coordinator reads is unknown. (F13, MAJOR, not blocking.)
- Sentinel collision attack. I can break this specification by **sentinel collision (`status` outside the four-value set)**. The invariant at **WC-5 (`spec:63`)** fails when **the contract has `status: ok` or no status**. Concrete attack: the worker writes `status: ok`; the "otherwise" clause sends `--outcome succeeded`; the coordinator reads success and can start dependent Tasks. (F4, CRITICAL, BLOCKING.)

## Guard Condition Boundary Table (mandatory: the spec has conditional rules)

Trigger: the spec contains guard rules (WC-2, WC-5, WC-6, WC-4, §7.2 step 2). The table is complete. Classes left out are named with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | `spec:63` | Zero/Empty | no report exists | true | `--outcome failed` (`spec:63`) | OK |
| WC-5 outcome mapping | `spec:63` | One/Minimal | contract present, `status` key missing or empty | true (falls into "otherwise") | `--outcome succeeded` by the "otherwise" clause | GAP (F4, blocking) |
| WC-5 outcome mapping | `spec:63` | Typical | `status: succeeded` | false | `--outcome succeeded` | OK |
| WC-5 outcome mapping | `spec:63` | Sentinel Value Match | `status: partial` | false | `--outcome succeeded`; the body keeps `partial` (`spec:263`) | OK |
| WC-5 outcome mapping | `spec:63` | Legitimate Edge Case | value outside the four-value set, for example `status: ok`, or an unparseable file | true (falls into "otherwise") | `--outcome succeeded` by the "otherwise" clause | GAP (F4, blocking) |
| WC-2 gate resolution | `spec:60`, `spec:103` | Zero/Empty | `--output` not passed | not stated | No rule. Only some rows require `--output` (`spec:113`) | GAP (F13, Medium) |
| WC-2 gate resolution | `spec:60` | Typical | `--unattended --output <dir>` plus the row's flags | true | Gate resolves as (a), (b) or (c) per the row | OK |
| WC-2 gate resolution | `spec:60`, `spec:103` | Sentinel Value Match | `--unattended` with `--interactive` | both true | Not specified (F12) | GAP (F12, Medium) |
| WC-2 gate resolution | `spec:60` | Legitimate Edge Case | `--unattended` with no preamble (plain session) | true | The flag decides (D1, `spec:228`) | OK |
| WC-6 resume or fresh | `spec:64`, `spec:109` | Typical | retry of a fresh-directory command, same directory | true | Fresh directory required, but no rule forces a new `--output` (F11) | GAP (F11, Medium) |
| WC-6 resume or fresh | `spec:64`, `spec:109` | Sentinel Value Match | implement with a matching ledger, no resume flag | true | Implicit resume (`spec:109`), which WC-6 does not allow (F11) | GAP (F11, Medium) |
| WC-6 resume or fresh | `spec:64` | Legitimate Edge Case | adversarial with `--pipeline-resume` | true | Resume (`spec:83`) | OK |
| WC-4 contract on outcome | `spec:62` | Zero/Empty | stop before any output exists | true | Contract written (`spec:62`) | OK |
| §7.2 step 2 liveness | `spec:181` | Zero/Empty | `worker-show` never run in the window | not applicable | Absent field passes "never non-null" (`CAPS:129`) (F16) | GAP (F16, Medium) |
| §7.2 step 2 liveness | `spec:181` | Typical | `observation.agentWait` null | false | Pass | OK |
| §7.2 step 2 liveness | `spec:181` | Legitimate Edge Case | `observation.agentWait` non-null | true | Fail | OK |

Classes left out: Maximum/Overflow for WC-5 (the status set is closed at four values, `spec:62`); One/Minimal for WC-6 and WC-2 (a single flag is covered by the Typical row).

No blank or "unspecified" Specified Behavior cell is left unrecorded (FR-9). The unspecified cells are listed above as GAP rows.

## Follow-up candidates (non-blocking, for the user)

- F5 (WC-2 vs WC-3 ask path), F6 (permission prompts and "same tools"), F7 (evidence conflict on direct route), F8 (§1.1 scope sentence), F9 (business-panel frontmatter scope), F10 (SA-3 vs SA-4 rename), F11 (WC-6 vs implicit resume), F12 (`--unattended` with `--interactive`), F13 (missing `--output`), F14 (lost `worker_done` response), F15 (coordinator steps after partial and blocked), F16 (§7.2 step 2), F17 (§7.2 step 5 coverage), F18 (Agent-tool waits and heartbeats), F19 (tasklist nesting), F20 (tdd and release-split prompts), F21 (AC-C1 scope once fixed), F22 (cli-portify path), F23 (spec-panel version drift), F24 (status vocabulary), F25 (R1 wording), F26 (install test), F27 (citation check not reproducible).
- Loop note for the coordinator: the session that ran this review asks the user once whether to open issues for these follow-ups. None has been created.

## Reviser brief

Blocking ids: F1, F2, F3, F4.

Restated rule (review-loop bullet 6): revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id. Do not grade a Medium or minor finding as blocking, and do not edit for one.

Ordering note: the findings block is the last section of the report, as the FIRST-REVIEW prompt requires. The verdict line is the final line of the report. This brief sits directly above the findings block.

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "These run as workers now if the brief uses the stated flags", "anchor2": "the exact command line including `--unattended`", "refs": ["section 2.3", "section 3.1", "AC-0.4", "7.2 step 1"], "claim": "The P0 smoke runs are built from a brief that must carry --unattended, but the commands do not accept that flag until P1 or P2, so AC-0.4 cannot pass as written."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "The only command changes are the small fixes in the last column.", "anchor2": "the `--unattended` flag accepted by every command in sections 3.1 and 3.2", "refs": ["section 3.1", "P1", "AC-1.1"], "claim": "brainstorm and init-lite have no change in section 3.1, but P1 and AC-1.1 require them to accept the flag and carry the section, so their briefs cannot pass the flag."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "(orchestration\\|worktree\\|terminal\\|agent)", "refs": ["AC-C1", "SA-2", "WC-8"], "claim": "In grep -E the escaped pipe is a literal, so AC-C1 prints nothing for any input and cannot fail, leaving SA-2 and WC-8 without a working check."}
{"id": "F4", "severity": "CRITICAL", "blocking": true, "category": "other", "anchor": "`--outcome succeeded` otherwise, including `partial`", "refs": ["WC-5", "WC-4", "section 2.2 WC-5 outcome mapping"], "claim": "A contract with a missing, unknown or unparseable status is sent as --outcome succeeded, so the coordinator reads a success for an unreadable result."}
{"id": "F5", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "Each gate resolves one of three ways", "anchor2": "the session may instead ask the coordinator once", "refs": ["WC-2", "WC-3"], "claim": "WC-2 names three resolutions, and WC-3 adds an ask path whose effect on resolution and outcome is not stated."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "has the same tools as a command a person runs", "refs": ["E2", "WC-2", "CAPS:161", "CAPS:129"], "claim": "The same-tools claim is unsupported, and tool-permission approvals, which can park a worker, are not covered by WC-2."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "It has worked before: in the codegraph planning run", "anchor2": "The only end-to-end proof is the PR #329 run", "refs": ["E3", "section 1.4", "INV-A:13"], "claim": "The direct route is cited as proven in E3 and unproven in section 1.4, and the spec does not say whether the P3 run and the PR #329 run are the same."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "What changes in the commands is limited to the worker contract in section 2", "refs": ["section 1.1", "SA-4", "section 3"], "claim": "The scope sentence in 1.1 omits the defect fixes in section 3 that SA-4 names."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "Only defects that stop a command working as a worker are in scope", "anchor2": "move the frontmatter out of its code block", "refs": ["section 8.8", "section 3.2 business-panel", "UNVERIFIED 7"], "claim": "The same frontmatter defect is out of scope for agent under 8.8 and in scope for business-panel under 3.2, with the need still UNVERIFIED."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "A standalone default run writes the same files it writes today.", "anchor2": "or correct a documented defect", "refs": ["SA-3", "SA-4", "P1 adversarial fix", "INV-A:35"], "claim": "SA-3 forbids a standalone run writing different files, while SA-4 permits renaming a contract as a defect fix, and the spec does not state which rule wins."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "resumes from its on-disk state when given its resume flag", "anchor2": "`--resume` (implicit when a ledger matches)", "refs": ["WC-6", "section 3.2 implement", "INV-A:51"], "claim": "Implement resumes without a flag, which WC-6 does not allow, and retry briefs are not required to use a new output directory."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "`--interactive` refused", "anchor2": "Under `--unattended` the command never calls `AskUserQuestion`", "refs": ["WC-2", "section 3.2 cleanup"], "claim": "No general rule covers a brief that passes both --unattended and --interactive, so a stall is possible."}
{"id": "F13", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "where `<output-dir>` is the directory the coordinator passed", "refs": ["WC-4", "section 2.3", "INV-A:61"], "claim": "A missing output directory under --unattended has no rule, so the report path is unknown before dispatch."}
{"id": "F14", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "The worker sends `worker_done` exactly once", "refs": ["WC-5", "CAPS:117"], "claim": "The exactly-once rule has no retry rule for a lost response, although Orca provides --retry-request."}
{"id": "F15", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "After `worker_done`, the coordinator opens the report file, then releases or reuses the worker", "refs": ["section 2.3", "CAPS:90", "CAPS:92"], "claim": "The coordinator's next step after partial and blocked is undefined, including who answers a blocked_question and whether partial may start dependents."}
{"id": "F16", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "at least once per 5 minutes", "anchor2": "`observation.agentWait` is never non-null", "refs": ["section 7.2 step 2", "section 7.2 step 3", "CAPS:129"], "claim": "Step 2 cannot run inside step 3's 900000 ms wait, and the never-non-null pass condition holds when the field is absent."}
{"id": "F17", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "search the transcript for `AskUserQuestion`", "anchor2": "verified in the step-5 transcript", "refs": ["section 7.2 step 5", "WC-2", "WC-7", "AC-0.4"], "claim": "Step 5 checks only AskUserQuestion, yet AC-0.4 says it verifies WC-7, and WC-2 forbids more prompt types."}
{"id": "F18", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "A command step that blocks a single tool call for longer than 5 minutes", "refs": ["WC-10", "CAPS:64", "CAPS:130"], "claim": "WC-10 does not state whether a top-level Agent-tool wait, which also blocks heartbeats, is covered."}
{"id": "F19", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit", "refs": ["section 3.2 tasklist", "INV-B:210", "INV-B:314"], "claim": "The tasklist no-change verdict relies on nested spawning that the inventories mark UNVERIFIED, and the spec's UNVERIFIED list omits it."}
{"id": "F20", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "a precise component prompt, not a bare topic", "refs": ["section 3.1 tdd", "section 3.1 release-split", "INV-B:119", "INV-B:219"], "claim": "tdd and release-split are called ready, but nested /task and tasklist-input prompts stay outside the brief's control."}
{"id": "F21", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "The only allowed mention of Orca in a changed command", "anchor2": "add an Orca section to `HOW-WE-WORK.md`", "refs": ["SA-2", "AC-C1", "P0", "section 2.1"], "claim": "SA-2 and P0 permit Orca mentions in core files that AC-C1 would reject once fixed."}
{"id": "F22", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "dispatch only inside an IronClaude checkout (hardcoded template path)", "refs": ["section 3.2 cli-portify", "P2", "INV-A:45", "INV-A:68"], "claim": "cli-portify keeps a src/superclaude lookup that the repo rule forbids for installed primitives, and P2 edits that file without fixing it."}
{"id": "F23", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "`target_release` required as a flag for TDD inputs", "refs": ["section 3.2 spec-panel", "INV-B:182", "command.md:23", "command.md:455"], "claim": "The spec-panel row describes a command without --output or unattended mode, but the supplied command definition has both, so the baseline is stale or differs."}
{"id": "F24", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "Commands that already write a contract keep their fields and add the missing ones", "anchor2": "`status` (one of `succeeded`, `partial`, `failed`, `blocked`)", "refs": ["WC-4", "INV-B:272"], "claim": "Existing contracts keep their fields, but WC-4 fixes a four-value status set, and no mapping is given for existing status values."}
{"id": "F25", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "would be refused with `nested_worker_depth_exceeded`", "refs": ["section 1.3 R1", "CAPS:103"], "claim": "R1 states the refusal as fact, while the same cell presumes the enforcing call sites."}
{"id": "F26", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "installed to `~/.claude/WORKER-CONTRACT.md`", "anchor2": "'WORKER-CONTRACT.md' in KNOWN_CORE_FILES", "refs": ["section 2.1", "AC-0.1"], "claim": "No check confirms that an installed command can read the installed contract file."}
{"id": "F27", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Independent citation check: a fresh `evidence-validator` agent", "refs": ["UNVERIFIED 14"], "claim": "The claimed evidence-validator pass is not reproducible from the workspace; noted without action."}
```

verdict: FAIL
