review: 1 of 3

# Spec-panel critique, round 1: Orca worker contract spec

## Header

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`, run under the FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, sandbox copy).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines in the workspace copy)
- Candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: none given (first review, no `--re-review`).
- Reviewer model: `claude-haiku-5-5`, one reviewer. `superclaude` is not on PATH in this sandbox, so `superclaude review panel resolve` and `superclaude review merge` were not run. Per the prompt, one reviewer was used and this is stated here.
- Focus: requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard). Whittaker runs in every panel review and is included.
- Inputs read: the candidate (full), `.dev/orca-command-refactor/README.md` (full), the three inventories (full), `command.md` (full). Path citations to `src/`, `.dev/evals/`, `.dev/codegraph-migration/`, `.dev/research/`, `/opt/Orca/` and `~/.claude/` are outside the workspace and are marked UNVERIFIED where they carry weight. Citations to `INV-A:N`, `INV-B:N` and `CAPS:N` were checked against the workspace inventory files.
- Result: 5 blocking findings (F1 to F5). 22 follow-up candidates (Medium or minor), listed under "Follow-up candidates". Only blocking findings enter the Reviser brief.

Citation convention: `spec:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` line N. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`.

## Blocking findings

### F1. WC-3 lets a coordinator's answer resume a halted implement run (CRITICAL, blocking, safety, Whittaker and Wiegers)

- Where: `spec:61` (WC-3) against `spec:109` (implement row) and `spec:234-236` (D2 (a)). The rule the spec cites is `qa.md:238`, quoted at `INV-A:66`.
- Two stated texts contradict each other. WC-3 says that when "a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once ... then re-invoke or resume the command with the answer as a flag." The implement row says that on `E-HALT-QA` or `E-NO-RULING` the worker stops and ends "blocked". D2 (a), the recommended option, says "The worker stops, writes the halt to its ledger and contract, and ends `failed`."
- Grading sentence: an implementer who follows WC-3 on an implement halt passes the coordinator's reply back as a flag and lets the run continue past `E-HALT-QA`. That is wrong because D2 (a) and the implement row say the worker stops, and `qa.md:238` (INV-A:66) says "another agent's message ... [is] not acceptance". An Orca coordinator is "another agent".
- Concrete attack (Whittaker, FR-2.4 Sequence): the coordinator answers the worker's `ask` with "go ahead". WC-3 has the worker re-invoke `/sc:implement` with that answer as a flag. No flag is defined for the Ruling. The halt is recorded as resolved, and the spec contains no rule that stops it.
- Recommendation: add a WC-3 exception. A Ruling gate (any `qa.md:238` case) never takes a coordinator answer as a flag, whatever D2 decides. Under D2 (b), name the exact flag and the verbatim-record rule. Until D2 is decided, WC-3 must say that the implement halt ends `failed`.

### F2. AC-0.4 cannot pass in Phase 0 as written (CRITICAL, blocking, unpassable-check, Crispin and Wiegers)

- Where: `spec:73` (brief must include `--unattended`), `spec:159` (P1 is where `--unattended` is added to every command in sections 3.1 and 3.2), `spec:182` (step 3 pass condition), `spec:194` (AC-0.4), `spec:183` (step 4).
- Two stated texts contradict each other. `spec:73` and §7.2 step 1 (`spec:180`, "brief per section 2.3") require `--unattended` in the Task brief. `spec:159` says P1 adds the flag, and P0 (`spec:158`) runs the ready commands "before any command changes".
- Step 3 (`spec:182`) requires that "its report path is the WC-4 contract path". WC-4 is delivered in P1 (`spec:159`), so P0 has no such path. `spec:194` says step 4 "uses the command's existing report file", but step 3 is still required to pass.
- Step 4 (`spec:183`) requires `d['status']` and `d['command']` in a YAML file. The P0 troubleshoot report is `REPORT.md`, a Markdown file (`INV-B:49`; `INV-B:242`). It has no such keys.
- Grading sentence: an implementer who runs AC-0.4 as written on `/sc:troubleshoot` finds the brief fails on the unknown `--unattended` flag, then step 3 fails because no WC-4 path exists, then step 4 fails on the Markdown report. So the Phase 0 gate cannot close, and the spec's own rule that Phase 0 "uses only the 10 ready commands" (`spec:158`) cannot be satisfied.
- Recommendation: give P0 its own pass conditions. The P0 brief omits `--unattended`, step 3 checks the `worker_done` outcome against the command's existing report, and step 4 applies only to commands with a YAML contract. Or move the P1 flag work ahead of the P0 smoke runs. Either way, state the P0 brief exactly.

### F3. AC-C1 cannot detect an Orca call in a command (MAJOR, blocking, safety, Nygard and Crispin)

- Where: `spec:172` (AC-C1), which enforces SA-2 (`spec:147`, "No command ... runs an `orca` or `orca-ide` command").
- The pattern is `\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b` under `grep -E`. In GNU `grep -E`, `\|` is a literal bar, not alternation. I checked this in the sandbox: the pattern matched nothing on lines that read `orca orchestration x`, `orca worktree y` and `orca-ide terminal z`. The same expression with a plain `|` matched all three.
- Grading sentence: an implementer who runs AC-C1 as written adds `orca orchestration task-create` to a command, sees empty output, and ships a command that fails with `runtime_unavailable` for every standalone user (`INV-A` and `CAPS:147` are the sources of that failure mode). That is wrong because SA-2 is a hard requirement on every phase (`spec:142`).
- Recommendation: replace `\|` with `|` (or use `-E` with `(orchestration|worktree|terminal|agent)`), and add a self-test that the grep matches a known-bad fixture.

### F4. WC-4 requires a contract path known before dispatch, but two rows make it run-time (MAJOR, blocking, contradiction, Hohpe and Fowler)

- Where: `spec:62` (WC-4: "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed"), `spec:73` ("so the report path is known before dispatch"), `spec:92` (workflow row: brief passes only `--handoff none`; report `.dev/tasks/to-do/<id>/return-contract.yaml`), `spec:116` (research row: "contract naming the generated `claudedocs/research_*.md` path").
- Workflow's package id is generated per run ("Fresh package each run", `INV-B:52`). Research's file name is generated at run time (`INV-B:38`). Workflow has no output flag in P1 (`spec:159` lists output flags only for "commands that lack one" in §3.1 and §3.2, and workflow has only a contract fix).
- Grading sentence: an implementer who follows WC-4 for `/sc:workflow --handoff none` has no `<output-dir>` to write to and cannot tell the coordinator the contract path before dispatch. That is wrong because `spec:62` and `spec:73` require it, and §7.2 step 3 (`spec:182`) checks it.
- Recommendation: either add an `--output` flag to workflow and research (with the id or file name derived from it), or exempt these two commands from WC-4 and have the coordinator read the path from the worker's `worker_done` payload. The second choice needs a rule in §2.3 for how the coordinator reads that payload.

### F5. Two workers in one worktree can overwrite each other's source edits (MAJOR, blocking, data-loss, Nygard and Whittaker)

- Where: `spec:69` (WC-11: "Two workers in one worktree must never write the same file"), `spec:73` (the brief states "worktree placement"), `spec:103` and `spec:110` (`/sc:cleanup` and `/sc:improve` both edit code, `INV-A:43` and `INV-A:52`), `spec:109` (implement edits product files). The default placement is the current worktree (`CAPS:115`).
- WC-11 covers only "default output paths". It does not cover source edits. No rule requires a separate worktree for an editing command, and no check tests for it.
- Concrete attack (Whittaker, FR-2.5 Accumulation): the coordinator dispatches two `/sc:improve --unattended` Tasks into the current worktree. Both edit the same file. The later write replaces the earlier. Neither worker's contract mentions the other's change, and WC-5 reports both as `succeeded`.
- Grading sentence: an implementer who follows §2.3 with the default placement (`CAPS:115`) and WC-11 as written gets two editing workers in one worktree writing the same source file, which the spec says must never happen.
- Recommendation: state a rule that a command which edits source runs in its own Orca worktree, or that the coordinator never runs two editing Tasks in one worktree. Add a check that two editing Tasks never share a placement. Keep WC-11 for output paths.

## Follow-up candidates (Medium or minor, not blocking)

The session that ran the review asks the user once whether to open an issue for these. No issue is created without the user's answer. Under `--unattended` the list is only recorded.

| ID | Severity | Expert | Where | Finding | Recommendation |
|---|---|---|---|---|---|
| F6 | MAJOR label, Medium | Fowler, Hohpe | `spec:63`, `spec:263`, `spec:73` | WC-5 maps `partial` and an audit with FAIL to `succeeded`. Orca settles a succeeded Task as complete (`CAPS:34`; a cancelled Task keeps dependents blocked, `CAPS:90`), so dependents can start after a failed audit. Dependents do start only if the coordinator ignores the contract, and §2.3 says nothing about gating dependents on `status`. | Add to §2.3: dependent Tasks start only when the contract `status` is `succeeded` with no FAIL verdict in the body. |
| F7 | MINOR | Fowler | `spec:76`, `spec:114`, `spec:139`, `spec:242` | pr-submit is counted in the worker table (needs-change, P4). D3 (a) recommends coordinator-only, and §4 says it is a worker candidate only if D3 is accepted. If D3 (a) is taken, the counts become 26 worker and 7 coordinator-only, and the §3 header (`spec:76`) is wrong. | Mark the pr-submit row as conditional on D3 and state both counts. |
| F8 | MAJOR label, Medium | Fowler, Newman | `spec:158` | P0 writes `WORKER-CONTRACT.md`, `KNOWN_CORE_FILES` and the routing-guide Orca section before the smoke runs. The same row says "the smoke runs test the decision before anything is built on it". A failed smoke run leaves those edits in place, and AC-0.3 forbids changing routing rows. | Move the three smoke runs before the writes, or state that a failed smoke run reverts the P0 writes. |
| F9 | MAJOR label, Medium | Nygard | `spec:88`, `spec:151` | Under `--unattended`, `/sc:reflect --remediate` is to "follow the existing headless auto-accept rule". SA-6 says that rule keys on `claude --print` and that `--unattended` "reuses it and does not replace it". The spec does not say whether `--unattended` makes the rule apply to an interactive worker. Auto-accept runs sc:workflow or task-builder, which create packages and can change code. | State the trigger for auto-accept under `--unattended`, and whether the remediation output is an outward action under WC-9. |
| F10 | MINOR | Hohpe | `spec:52` | Commands point to `~/.claude/WORKER-CONTRACT.md`, which exists only after a fresh `superclaude install`. Nothing says what an unattended command does when the file is missing (an older install, or a plugin install). | Require each command to fail with `status: blocked` when the contract file is missing, or to carry the minimum rules inline. |
| F11 | MAJOR label, Medium | Fowler | `spec:105`, `spec:160` | `/sc:cli-portify` has a hardcoded template path, flagged at `spec:105` ("dispatch only inside an IronClaude checkout"). No phase in §6 schedules the fix. `CLAUDE.md` forbids `src/superclaude/` paths in installed primitives, and no AC grep-checks for it. | Schedule the fix in P2 and add an AC that greps `src/superclaude` in primitives, as CLAUDE.md requires. |
| F12 | MAJOR label, Medium | Newman | `spec:279`, `spec:173` | The `plugins/superclaude/commands/` mirror is an open item (UNVERIFIED 8). Each phase edits `src/superclaude/commands/`, and only `make verify-sync` (`.claude/` only) is checked. Mirror drift is not checked. | Decide the update rule for the mirror before P1 and add an AC for it. |
| F13 | MAJOR label, Medium | Wiegers | `spec:59` | WC-1 (readiness) lists its owner as "Launch setup, not commands". No phase in §6 (`spec:158-162`) covers launch setup, and no AC checks readiness. E5 (`spec:25`) names `ccsession-tag` as the only Orca-aware primitive, and no phase covers it. | Add a phase or AC that owns WC-1, or state that it is out of scope for this spec. |
| F14 | MAJOR label, Medium | Crispin | `spec:181` | §7.2 step 2 passes when `observation.agentWait` is never non-null. `CAPS:129` says an absent field means Orca never looked, so the check passes with no evidence, and a stalled worker can pass step 2. Steps 3 and 5 catch part of this. | Require a non-null `observation.status` or a recorded look, not just the absence of a wait. |
| F15 | MAJOR label, Medium | Fowler | `spec:22`, `spec:24` | E2 says a command run by a worker "has the same tools as a command a person runs". The cited evidence (`EVIDENCE.md:45`, `CAPS:161`) shows readiness only, not tool parity. E4 states "are not counted by Orca's nesting limit" as fact, but `CAPS:155` marks that UNVERIFIED. | Reword E2 and E4 as inferences with the UNVERIFIED mark, or cite a tool-list check. |
| F16 | MINOR | Hohpe, Newman | `spec:62` | WC-4 has no schema version. Existing contracts carry one (`spec:62` cites contract 1.1 for workflow). A coordinator cannot tell which fields a file promises. | Add `contract_version` to the required fields. |
| F17 | MAJOR label, Medium | Wiegers, Adzic | `spec:59` | WC-1 says a startup prompt must fall back "well inside the readiness limit". "Well inside" has no number. The cited evidence puts the failure point at about 45 s (`EVIDENCE.md:56`, outside the workspace, UNVERIFIED). | Give a number, such as a fallback of at most 30 s, and a test that fails above it. |
| F18 | MAJOR label, Medium | Whittaker | `spec:228`, `spec:51` | D1 says a flag "cannot misfire on a person". The spec has no parse rule. Concrete attack (FR-2.3 Sentinel Collision): a task string that quotes `--unattended` ("the CI job passes --unattended but fails") switches the worker's mode. The spec gives no rule on whether the flag must be a standalone token. The spec-panel command has such a rule for its own flag (`command.md`, Unattended mode, "Switch"). | State the parse rule for the flag: standalone token outside quotes, and what a command does with a target-less `--unattended`. |
| F19 | MAJOR label, Medium | Nygard | `spec:64`, `spec:73` | WC-6 says a re-run writes "into a fresh output directory". §2.3 says the coordinator passes the output directory in the brief, and a retry (`worker-start --retry-of`, `CAPS:116`) reuses the Task brief. The spec does not say whether a retry of a blocked or failed Task changes the directory. | Require a new `--output` for each retry, and say which Task states may be retried. |
| F20 | MINOR | Wiegers | `spec:147` | SA-2 says "the only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file". The sentence is about the contract file, which is not a changed command. | Reword as "No changed command names Orca. The contract file may name the question channel." |
| F21 | MINOR | Wiegers | `spec:118` | The roadmap row replaces the `Resume? [Y/n]` prompt with an explicit flag. It sits in the unattended column, but SA-1 (`spec:146`) says every prompt is unchanged without `--unattended`, and the row does not say whether the replacement is limited to unattended mode. | Say whether the change applies only under `--unattended`. |
| F22 | MINOR | Fowler | `spec:23` | E3 says "It has worked before" and cites PR #329. §1.4 (`spec:43`) says that run used the subagent route, which this spec does not require. E3 does not carry that caveat. | Add the caveat to E3. |
| F23 | MAJOR label, Medium | Nygard | `spec:60` (WC-2 (c)) | A gate that resolves as blocked after some edits leaves partial changes in the worktree. The spec writes a `status: blocked` contract and stops, but says nothing about whether partial edits stay, are reverted, or are listed in the contract. The inventories say cleanup and improve claim rollback with no mechanism (`INV-A:43`, `INV-A:52`). | Require the blocked contract to list every file changed before the stop. |
| F24 | MINOR | Wiegers | `spec:63` | WC-5 does not map a zero-byte report, or a `status` outside the four values. §7.2 step 4 (`spec:183`) treats an empty file as a failure, but WC-5 does not say so. | Add both cases to WC-5. |
| F25 | MINOR | Hohpe | `spec:70` | WC-12 says what the worker does on `consumer_fenced`, but not what it does with an ordinary coordinator follow-up. | Add one sentence on follow-up handling. |
| F26 | MINOR | Nygard | `spec:114`, `spec:283` | WC-10 needs each pr-submit poll-and-sleep iteration under 4 minutes. Its runtime is UNVERIFIED (item 12). AC-4.3 checks this only if D3 (b) is chosen. | Keep the item open and tie the WC-10 check to P2 as well. |
| F27 | MINOR | Fowler | `spec:39` | §1.3 says "Orca keeps those records only for workers the coordinator starts (`CAPS:158`)". `CAPS:158` is the provenance rule and does not say that. | Re-cite, or mark the claim as inference. |

## Adversarial attacks (Whittaker, FR-3 template)

1. I can break this specification by **FR-2.4 Sequence Attack**. The invariant at **`spec:61` (WC-3) and `spec:109`** fails when **the coordinator answers a worker's ask on an implement halt**. Concrete attack: the worker halts on `E-HALT-QA` (ledger and contract say `blocked`). The coordinator answers "approved". WC-3 has the worker re-invoke with the answer as a flag. The run continues. No flag exists in the spec, so the flag is invented. Severity: CRITICAL. This is F1.
2. I can break this specification by **FR-2.3 Sentinel Collision Attack**. The invariant at **`spec:228` (D1)** fails when **a task string quotes the flag**. Concrete attack: `/sc:troubleshoot "CI passes with --unattended but fails on login"` switches the worker to unattended mode, and `/sc:troubleshoot` then resolves its gates by default. The spec has no parse rule. Severity: MAJOR label, Medium. This is F18.
3. I can break this specification by **FR-2.5 Accumulation Attack**. The invariant at **`spec:69` (WC-11)** fails when **two editing workers share one worktree**. Concrete attack: two `/sc:improve --unattended` Tasks edit `src/a.py`. The later write replaces the earlier, and both report `succeeded`. Severity: MAJOR, blocking. This is F5.

## Guard Condition Boundary Table

Trigger: the spec contains guards (conditional rules, threshold checks, sentinel tests). The table is produced under FR-10. Each guard lists the input classes that apply. A class left out has a one-line reason. Each GAP row maps to a finding. FR-8 and FR-9 grade the GAP rows.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--unattended` switch | `spec:51`, `spec:228` | Zero/Empty | no flag | `false` | Standard behaviour (`spec:146`, SA-1) | OK |
| G1 `--unattended` switch | `spec:51` | Sentinel Value Match | `--unattended` inside a quoted task string | not stated | Spec says it "cannot misfire" (`spec:228`) but gives no parse rule | GAP (F18) |
| G1 `--unattended` switch | `spec:51` | Typical | flag with the brief's required flags | `true` | WC-2 applies (`spec:60`) | OK |
| G1 `--unattended` switch | `spec:51` | One/Minimal | `--unattended` alone, no target | not stated | Spec does not say whether a target-less run stops or is refused | GAP (F18) |
| G1 `--unattended` switch | `spec:103`, `spec:110` | Legitimate Edge Case | `--unattended` with `--interactive` | `refused` | Refused per §3 rows (cleanup, improve). No general rule. | OK (per row only) |
| G1 `--unattended` switch | `spec:51` | Maximum/Overflow | n/a | n/a | Left out: a boolean switch has no capacity bound. | (left out) |
| G2 gate resolution | `spec:60` | Zero/Empty | gate with no default and no flag | (c) blocked | Writes `status: blocked` and stops (`spec:60`) | OK |
| G2 gate resolution | `spec:60` | One/Minimal | gate with one documented default | (a) default | Uses the default | OK |
| G2 gate resolution | `spec:60` | Typical | gate with a value from the brief | (b) flag | Uses the flag | OK |
| G2 gate resolution | `spec:67` | Sentinel Value Match | default is an outward action (PR posting) | off | WC-9 (`spec:67`) overrides the default | OK |
| G2 gate resolution | `spec:60`, `spec:61` | Legitimate Edge Case | gate reached after partial edits | blocked, edits remain | Not stated whether edits are kept, reverted or listed | GAP (F23) |
| G2 gate resolution | `spec:60` | Maximum/Overflow | n/a | n/a | Left out: each gate takes one of three values; no numeric bound. | (left out) |
| G3 readiness fallback | `spec:59`, `spec:221` | Zero/Empty | no startup prompt | nothing to fall back | No fallback needed | OK |
| G3 readiness fallback | `spec:59` | One/Minimal | fallback of 1 s | passes | "well inside" met | OK |
| G3 readiness fallback | `spec:59` | Typical | fallback of 30 s | passes | Cited evidence `EVIDENCE.md:45` is outside the workspace (UNVERIFIED) | OK (UNVERIFIED) |
| G3 readiness fallback | `spec:59` | Sentinel Value Match | `--timeout-ms` omitted | 60 s default | Non-goal 9 (`spec:221`); `CAPS:44-45` | OK (cited) |
| G3 readiness fallback | `spec:59` | Legitimate Edge Case | fallback between 45 s and 60 s | fails above about 45 s (cited) | "well inside" is not a number | GAP (F17) |
| G3 readiness fallback | `spec:59` | Maximum/Overflow | fallback equal to 60 s | fails | Not covered by a number | GAP (F17) |
| G4 outcome mapping | `spec:63` | Zero/Empty | no report file | `failed` | Specified (`spec:63`) | OK |
| G4 outcome mapping | `spec:63`, `spec:183` | One/Minimal | report exists, zero bytes | not stated in WC-5 | §7.2 step 4 fails it, WC-5 does not | GAP (F24) |
| G4 outcome mapping | `spec:63` | Typical | `status: succeeded` | `succeeded` | Specified | OK |
| G4 outcome mapping | `spec:63`, `spec:263` | Sentinel Value Match | `status` outside the four values | unmapped | Not stated | GAP (F24) |
| G4 outcome mapping | `spec:63` | Legitimate Edge Case | `partial`, or audit FAIL | `succeeded` | Specified; dependent Tasks then start | OK (consequence F6) |
| G4 outcome mapping | `spec:62` | Maximum/Overflow | n/a | n/a | Left out: `status` is a fixed four-value set (`spec:263`). | (left out) |
| G5 consumer_fenced | `spec:70` | Zero/Empty | `check` returns empty | continue | Stop only on `consumer_fenced`; `CAPS:51` | OK |
| G5 consumer_fenced | `spec:70` | Sentinel Value Match | `check` returns `consumer_fenced` | stop, no `worker_done` | Specified | OK |
| G5 consumer_fenced | `spec:70` | One/Minimal | one ordinary follow-up | not stated | Handling not specified | GAP (F25) |
| G5 consumer_fenced | `spec:70` | Typical | no fence, no follow-up | continue | Specified | OK |
| G5 consumer_fenced | `spec:70` | Maximum/Overflow | n/a | n/a | Left out: `check` returns one fence state. | (left out) |
| G5 consumer_fenced | `spec:70` | Legitimate Edge Case | fence after `worker_done` | n/a | Left out: after `worker_done` the worker idles (`CAPS:78`) | (left out) |
| G6 contract check, §7.2 step 4 | `spec:183` | Zero/Empty | empty file | `test -s` fails | Specified | OK |
| G6 contract check, §7.2 step 4 | `spec:183` | One/Minimal | file with `status` and `command` only | passes | Specified | OK |
| G6 contract check, §7.2 step 4 | `spec:183` | Typical | full WC-4 contract | passes | Specified | OK |
| G6 contract check, §7.2 step 4 | `spec:183`, `spec:194` | Legitimate Edge Case | `REPORT.md` (Markdown) in P0 | parse or key error | AC-0.4 says step 4 uses the existing report | GAP (F2) |
| G6 contract check, §7.2 step 4 | `spec:183` | Sentinel Value Match | `status: partial` | passes | `partial` is in the set | OK |
| G6 contract check, §7.2 step 4 | `spec:183` | Maximum/Overflow | n/a | n/a | Left out: no size bound. | (left out) |
| G7 wait size, WC-10 | `spec:68` | Zero/Empty | no wait | no heartbeat needed | Specified | OK |
| G7 wait size, WC-10 | `spec:68` | Maximum/Overflow | single call of 300 s | exceeds 4 min | "must be split"; no consequence stated | OK (rule stated) |
| G7 wait size, WC-10 | `spec:68` | Sentinel Value Match | 240 s exactly | passes | "at most 4 minutes" | OK |
| G7 wait size, WC-10 | `spec:114`, `spec:283` | Legitimate Edge Case | pr-submit poll iteration, runtime unknown | cannot evaluate | Runtime UNVERIFIED (item 12) | GAP (F26) |
| G7 wait size, WC-10 | `spec:68` | One/Minimal | 1 s wait | passes | Specified | OK |
| G7 wait size, WC-10 | `spec:68` | Typical | 3-minute poll | passes | Specified | OK |

Pipeline Dimensional Analysis: not triggered. The spec describes one report per worker and a Task DAG. It has no multi-stage data flow in which counts change (FR-17 excludes CRUD-only flows, and this is a lifecycle, not a count pipeline). State Variable Registry: not mandatory, because `--focus correctness` is not active.

## Expert analysis (requirements and architecture)

### Requirements (Wiegers lead, Adzic, Cockburn)

- Requirements are numbered and carry evidence columns, which is a strength. Testability is weak in three places: WC-1's "well inside" (F17), §7.2 step 2's absence pass (F14), and AC-C1 (F3).
- Scope boundaries are clear (§8, Non-goals). The 10 / 27 / 6 split matches the inventories: 43 commands, 5 + 5 ready, 13 + 14 needs-change, and 3 + 3 coordinator-only (`INV-A:73`, `INV-B:278`). Counts reconcile with the §3 rows (`spec:78-125`), except that pr-submit depends on D3 (F7).
- Traceability: each WC rule names an owner (Command, Worker session, Launch setup). WC-1's owner has no phase (F13).
- Cockburn-style goal statement: the goal is stated in the workspace README (`.dev/orca-command-refactor/README.md:6`), not in the spec. The spec does not name the primary actor for the coordinator's brief. §2.3 partly covers it.

### Architecture (Fowler lead, Newman, Hohpe, Nygard)

- The decision to keep commands as units of work and put orchestration in the coordinator (§1) is sound and well argued. Its strongest weakness is the evidence for the direct route, which §1.4 admits (E2 overstates, F15). Phase 0 tests it, but P0 writes files before that test (F8).
- Contract design: a single file (WC-4) with a fixed status set (WC-5) is a good interface. It lacks a schema version (F16), and the directory rule fails for two commands (F4).
- Coupling: the contract file is installed core (§2.1), so commands depend on an installed file that may be missing (F10). The plugin mirror is unresolved (F12).
- Concurrency: WC-11 covers outputs but not source edits, which is the real risk (F5). Retries reuse the Task brief (F19).
- Failure handling: blocked outcomes leave partial edits (F23). The circuit breaker counts failed starts only (`CAPS:80`), so a worker that reports `failed` does not trip it; that is a benefit of the design, not a gap.
- Nesting: the depth-1 decision is stated as a setting (D5). The rejected alternative (§1.3) rests on UNVERIFIED enforcement sites (`CAPS:103`), which the spec marks. This is transparent but should be kept in the decision record.

## Quality assessment (0-10, standard format)

| Dimension | Score | Basis |
|---|---|---|
| Clarity | 6 | Clear structure and citations; some rules contradict each other (F1, F4) |
| Completeness | 6 | Full command coverage; missing: source-edit concurrency (F5), launch setup owner (F13), plugin mirror (F12) |
| Testability | 4 | Two checks cannot fail (F3, F14); P0 gate cannot pass (F2) |
| Consistency | 4 | WC-3 vs implement row and D2 (F1); WC-4 vs workflow and research (F4); P0 brief vs `--unattended` (F2) |
| Overall | 5 | Five blocking findings |

## Coverage

- Read in full: the candidate, the workspace README, `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`, `command.md`, and the sandbox copy of `document_review_loop_prompts.md`.
- Checked against workspace files: the spec's `INV-A`, `INV-B` and `CAPS` citations for the claims in F1 to F7 and F13 to F27. Spot-checked and matched: `INV-A:43`, `INV-A:52`, `INV-A:66`, `INV-A:76-83`, `INV-B:49`, `INV-B:52`, `INV-B:242`, `INV-B:272`, `INV-B:285-286`, `INV-B:311`, `INV-B:323`, `CAPS:34`, `CAPS:44-46`, `CAPS:51`, `CAPS:73`, `CAPS:80`, `CAPS:115`, `CAPS:129`, `CAPS:147`, `CAPS:155`, `CAPS:161`. `CAPS:158` supports only part of its claim (F27).
- Not checkable here (UNVERIFIED): every `src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `.dev/research/...`, `/opt/Orca/...` and `~/.claude/...` citation. Where a finding rests on one of them, the finding says so.
- The grep test for F3 was run in the sandbox on a four-line fixture, which was then removed.
- Not run: `superclaude review panel resolve` and `superclaude review merge` (not installed in the sandbox). Single reviewer.

## Reviser brief

Blocking ids: F1, F2, F3, F4, F5.

Restatement of the Review Loop bullet 6 for the reviser: revise only the text the blocking findings name. Add no rule, mechanism or section that a blocking finding does not call for. Cite the finding id on each added paragraph or table. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id. Do not touch the follow-up candidates. Do not award a PASS.

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "safety", "anchor": "then re-invoke or resume the command with the answer as a flag", "anchor2": "on `E-HALT-QA` or `E-NO-RULING`, stop with the halt recorded in the ledger", "refs": ["WC-3", "§3.2 implement", "D2(a)", "INV-A:66"], "claim": "WC-3 lets a coordinator answer re-invoke a halted implement run, which D2(a) and the implement row forbid, and qa.md:238 bars as a Ruling."}
{"id": "F2", "severity": "CRITICAL", "blocking": true, "category": "unpassable-check", "anchor": "the exact command line including `--unattended`", "anchor2": "its report path is the WC-4 contract path", "refs": ["§2.3", "§7.2 step 1", "§7.2 step 3", "AC-0.4", "P1 scope"], "claim": "AC-0.4 cannot pass in P0: the brief needs a flag P1 adds, the step 3 path does not exist until P1, and step 4 expects YAML from a Markdown report."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "safety", "anchor": "(orchestration\\|worktree\\|terminal\\|agent)\\b", "refs": ["AC-C1", "SA-2", "WC-8"], "claim": "In grep -E the escaped bar is literal, so AC-C1 never matches an Orca call and passes vacuously, letting a command break standalone use."}
{"id": "F4", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "where `<output-dir>` is the directory the coordinator passed", "anchor2": "contract naming the generated `claudedocs/research_*.md` path", "refs": ["WC-4", "§2.3", "workflow row", "research row", "INV-B:52", "INV-B:38"], "claim": "WC-4 requires a contract path known before dispatch, but workflow has no output flag and research and workflow names are generated at run time."}
{"id": "F5", "severity": "MAJOR", "blocking": true, "category": "data-loss", "anchor": "Two workers in one worktree must never write the same file.", "refs": ["WC-11", "§2.3", "CAPS:115", "INV-A:43", "INV-A:52"], "claim": "Editing commands can run as two workers in one worktree, and the later source write overwrites the earlier, which WC-11 forbids and nothing prevents."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "including an audit whose verdict is FAIL (the audit itself succeeded)", "refs": ["WC-5", "Decisions row partial (spec:263)", "§2.3", "CAPS:34", "CAPS:90"], "claim": "Succeeded settles a Task complete, so a dependent can start after a FAIL audit, unless the coordinator checks the contract, which §2.3 does not require."}
{"id": "F7", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "stays a worker candidate only if the user accepts open decision D3", "anchor2": "**Coordinator or person only (recommended).**", "refs": ["§3 header", "§3.2 pr-submit", "§4", "D3"], "claim": "pr-submit is counted as a worker candidate although D3 recommends coordinator-only, so the 10/27/6 counts depend on an open decision."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "the smoke runs test the decision before anything is built on it", "anchor2": "Write `src/superclaude/core/WORKER-CONTRACT.md`", "refs": ["§6 P0", "AC-0.3", "§1.4"], "claim": "P0 builds the contract and routing-guide edits before the smoke runs that test the decision, so a failed test leaves the edits behind."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "make `--remediate` follow the existing headless auto-accept rule", "anchor2": "`--unattended` reuses it and does not replace it", "refs": ["§3.1 reflect", "SA-6", "WC-9"], "claim": "It is unstated whether --unattended triggers reflect's headless auto-accept, which runs remediation that can change code."}
{"id": "F10", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "installed to `~/.claude/WORKER-CONTRACT.md`", "refs": ["§2.1", "WC-2", "§5"], "claim": "Commands point to an installed file that may be absent after a partial or older install, and no fallback is stated."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "dispatch only inside an IronClaude checkout (hardcoded template path)", "refs": ["§3.2 cli-portify", "§6 P2", "CLAUDE.md installed-path rule"], "claim": "The hardcoded src/superclaude template path is flagged but unscheduled, and no AC checks for such paths."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "How `plugins/superclaude/commands/` (which holds copies such as", "refs": ["UNVERIFIED 8", "AC-C2"], "claim": "Command edits can leave the plugins mirror out of step, and no AC checks the mirror."}
{"id": "F13", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Launch setup, not commands", "refs": ["WC-1", "§6"], "claim": "WC-1 has an owner outside every phase and no AC checks readiness."}
{"id": "F14", "severity": "MAJOR", "blocking": false, "category": "unpassable-check", "anchor": "`observation.agentWait` is never non-null", "refs": ["§7.2 step 2", "CAPS:129"], "claim": "The step 2 pass also holds when the field is absent, which means Orca never looked, so a stalled worker can pass."}
{"id": "F15", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "so a command run by a worker has the same tools as a command a person runs", "anchor2": "are not counted by Orca's nesting limit", "refs": ["E2", "E4", "CAPS:155", "EVIDENCE.md:45"], "claim": "E2 claims tool parity the cited evidence does not show, and E4 states as fact what CAPS:155 marks UNVERIFIED."}
{"id": "F16", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "It follows the return-contract pattern several commands already use", "refs": ["WC-4", "INV-B:272"], "claim": "The WC-4 contract has no schema version, although the existing workflow contract has one."}
{"id": "F17", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "must fall back on its own well inside the readiness limit", "refs": ["WC-1", "G3 rows"], "claim": "well inside is not a number, so a fallback near the limit cannot be tested."}
{"id": "F18", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "It is testable by grep and cannot misfire on a person.", "refs": ["D1", "§2.1", "G1 rows"], "claim": "No parse rule stops a quoted --unattended in task text, or a target-less run, from switching modes."}
{"id": "F19", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "writes each run into a fresh output directory so a re-run starts clean", "anchor2": "the output directory, so the report path is known before dispatch", "refs": ["WC-6", "§2.3", "CAPS:116"], "claim": "A retry reuses the Task brief and so the same output directory, which WC-6 says must be fresh."}
{"id": "F20", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "The only allowed mention of Orca in a changed command is as an example", "refs": ["SA-2"], "claim": "SA-2 is worded so that the rule for changed commands points at the contract file, which is not a changed command."}
{"id": "F21", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "prompt is replaced by the explicit resume flag (resume only when passed)", "refs": ["§3.2 roadmap", "SA-1"], "claim": "It is unclear whether the roadmap prompt change applies only under --unattended, which SA-1 requires."}
{"id": "F22", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "It has worked before: in the codegraph planning run", "refs": ["E3", "§1.4"], "claim": "E3 cites PR #329 without the subagent-route caveat that §1.4 gives."}
{"id": "F23", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "the command writes its report with `status: blocked` and the exact question, and stops", "refs": ["WC-2 (c)", "CAPS:80", "INV-A:43"], "claim": "A blocked stop after partial edits leaves no list of changed files, so the coordinator cannot tell what to revert."}
{"id": "F24", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "when the report says `failed` or `blocked`, or no report exists", "refs": ["WC-5", "§7.2 step 4"], "claim": "A zero-byte report and an out-of-set status are not mapped."}
{"id": "F25", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "The worker runs `check` at natural checkpoints and once before `worker_done`", "refs": ["WC-12"], "claim": "Ordinary follow-ups have no stated handling."}
{"id": "F26", "severity": "MINOR", "blocking": false, "category": "unpassable-check", "anchor": "the 600 s default is a cumulative per-wait budget", "refs": ["WC-10", "AC-4.3", "UNVERIFIED 12"], "claim": "The pr-submit wait check is unverifiable until the poll runtime is measured, and P2 has no check for it."}
{"id": "F27", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Orca keeps those records only for workers the coordinator starts", "refs": ["§1.3", "CAPS:158"], "claim": "CAPS:158 is the provenance rule, which only partly supports the claim it is cited for."}
```

Reviser brief: revise only F1, F2, F3, F4 and F5. Restate: revise only text a blocking finding names; add no rule, mechanism or section a blocking finding does not call for; cite the finding id on every addition; prefer deleting or narrowing; report byte size before and after, with bytes added and deleted per finding id; leave the follow-up candidates alone.

verdict: FAIL
