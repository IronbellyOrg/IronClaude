review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec (focus: requirements, architecture)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: not given (first review; `--re-review` not used)
- reviewer model: claude-haiku-5-5
- prompt: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full)
- citation key: `spec:N` = `specs/orca-worker-contract-spec.md:N`; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` (relative to `.dev/orca-command-refactor/`); `README:N` = `README.md:N`
- evidence limit: this sandbox holds only `.dev/orca-command-refactor/`. Every `src/superclaude/...`, `~/.claude/...`, `/opt/Orca/...`, `.dev/evals/...` and `.dev/codegraph-migration/...` citation was NOT checked against its file and is marked UNVERIFIED where it carries a claim. Checks were made against the inventories and the README only.
- panel: Wiegers (lead), Adzic, Cockburn for requirements; Fowler (lead), Newman, Hohpe, Nygard for architecture; Whittaker is active in every panel review (`command.md:83`) and is included.

## Coverage

Read in full: `README.md`, `spec`, `inventory/orca-capabilities.md`, `inventory/commands-a.md`, `inventory/commands-b.md` (the summary, the notes and the UNVERIFIED sections were read in full; the table rows were read in full), the review-loop prompt file, and `command.md`.

Checked against the inventories (not against source): the Orca fact citations `CAPS:44-46, 52, 58-61, 66-67, 73, 76-77, 79-80, 84-88, 92, 97-103, 107-113, 115-116, 129-130, 149-151, 155-161, 178, 186-188`; the inventory row and summary citations `INV-A:14, 35, 60-62, 73, 76-83, 90, 95-97`; `INV-B:31-52, 65, 105, 107-125, 272, 278-301, 311, 320, 323`; the spec's ready / needs-change / coordinator-only counts (10 + 27 + 6 = 43; INV-A 5/13/3 and INV-B 5/14/3 reconcile with spec section 3 and section 4). Every cited inventory row and note I checked lines up with the spec's claim.

Not checkable here (UNVERIFIED): `spec:25` (E5 grep), `spec:21-24` evidence paths under `.dev/evals/` and `.dev/codegraph-migration/`, `spec:23` (PR #329 landed; only `README:12` restates it), all `/opt/Orca` file and line cites in CAPS (for example CAPS:44-45, 97-98, 145-149), the `src/superclaude` cites, `~/.claude/rules/...` cites, the `CLAUDE.md` cites (`spec:52, 152, 175, 279`).

## Guard Condition Boundary Table (mandatory: the spec contains threshold checks, boolean guards and sentinel values)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | spec:63 | Zero/Empty | contract file exists, 0 bytes | not `failed`/`blocked`, report exists: "otherwise" branch = `succeeded` | Task settles `completed`; dependents start (CAPS:77, CAPS:84-88) | GAP (B-5) |
| WC-5 outcome mapping | spec:63 | One/Minimal | `status: Succeeded` or `status: done` (outside the four-value set, spec:262) | "otherwise" = `succeeded` | same as above | GAP (B-5) |
| WC-5 outcome mapping | spec:63 | Sentinel Value Match | `status: partial` | "otherwise" = `succeeded` | Task settles `completed`; dependents start | OK as written; lossy, see M-2 |
| WC-4 contract path | spec:62 | Typical (file-valued output) | `--output <file>` for tdd (spec:90) and init-lite (spec:87) | `<output-dir>/return-contract.yaml` needs a directory; undefined for a file | not specified | GAP (B-3) |
| WC-4 contract path | spec:62 | Zero/Empty | unattended brief omits `--output` | not stated | adversarial writes beside its inputs (INV-A:61) | GAP (M-13) |
| WC-3 ask timeout | spec:61 | Zero/Empty | `--timeout-ms` omitted | default not known (CAPS:68) | resume by message ID; no bound stated | GAP (M-4) |
| WC-10 wait split | spec:68 | Boundary | one tool call of 4 min vs 5 min heartbeat | 4 min rule | a poll iteration over 4 min has no rule (poll runtime UNVERIFIED, spec:283) | GAP (M-10) |
| Task confidence gate | spec:121 | Boundary | confidence exactly 0.70 | below 0.70 = blocked | 0.70 proceeds | OK |
| cli-eval `run` gate | spec:104 | Zero/Empty | no `--suite` | blocked | blocked, contract written | OK |
| reflect remediation gate | spec:88 | Typical | `--remediate` under `--unattended` | headless auto-accept (INV-B:109) | remediation runs without a person | GAP (B-4) |
| WC-12 ownership | spec:70 | Sentinel | `check` returns `consumer_fenced` | stop, no `worker_done` (CAPS:67) | stops | OK |
| Depth fence | spec:66 | Maximum | nesting depth 1 (CAPS:97-98) | `worker-start` refused | command makes no Orca call | OK |

Synthesis is not blocked by the table (it is complete: every guard has a row and every GAP is a finding below).

## Pipeline Dimensional Analysis

Triggered: the report flow is a multi-stage pipeline (command output, contract, `worker_done`, Task settlement, dependent Tasks; spec:62-63, CAPS:73-77). No numeric count diverges along it, so FR-19's CRITICAL class does not apply. The WC-5 mapping is lossy (four statuses into two outcomes); that is recorded as M-2 and B-5, not as a count mismatch.

## === REQUIREMENTS ANALYSIS ===

### B-1 (BLOCKING): section 3 says ready commands change only by their small fixes, but P1 and AC-1.1 require every one of them to change
- Issue: `spec:79` says "The only command changes are the small fixes in the last column" for the ten ready commands. `spec:159` (P1) requires the `--unattended` flag "accepted by every command in sections 3.1 and 3.2", and `spec:195` (AC-1.1) requires a `## Unattended mode` section in every 3.1 command. Brainstorm (`spec:84`) and init-lite (`spec:87`) have no fix, so an implementer following `spec:79` leaves them untouched and fails P1 and AC-1.1. Following P1 and AC-1.1 adds a change that `spec:79` denies.
- Sentence: "An implementer who follows `spec:79` leaves brainstorm and init-lite unchanged, and that is wrong because `spec:195` requires them to carry a `## Unattended mode` section."
- Severity: MAJOR, blocking (two stated texts contradict).
- Expert: Wiegers (traceability), Cockburn.
- Recommendation: state one rule. Either every 3.1 command gets the flag and section (and `spec:79` is rewritten to say so), or AC-1.1 and P1 exclude commands whose only change is "none". Name the set explicitly.
- Priority: High. Quality impact: high (a test that cannot be made to pass as written).

### B-2 (BLOCKING): the P0 acceptance check cannot pass for a command whose report is not a YAML contract
- Issue: `spec:194` (AC-0.4) runs the 7.2 live check on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` and says "step 4 uses the command's existing report file, since the contract arrives in P1". Step 4 (`spec:183`) asserts `yaml.safe_load(...)` with `d['status']` in four values and `d['command']`. Troubleshoot writes `REPORT.md` and `audit.log`, not YAML (`INV-B:49`; `spec:91`). Adversarial's contract filename is not fixed (`INV-A:60`). So step 4 fails by construction for troubleshoot and cannot be checked for adversarial.
- Sentence: "An implementer who runs AC-0.4 step 4 on `/sc:troubleshoot` parses `REPORT.md` as YAML, and that is wrong because `REPORT.md` has no `status` field and the check fails."
- Severity: MAJOR, blocking (acceptance criterion cannot pass as written).
- Expert: Adzic (testability), Nygard (P0 gate).
- Recommendation: give P0 its own step 4 (for example "`report_path` exists and is non-empty; for YAML reports, parse them"), and name the P0 report file per command.
- Priority: High. Quality impact: high (P0 gates the whole plan, `spec:158`).

### B-3 (BLOCKING): the contract location rule (WC-4) conflicts with the per-command rows, so the coordinator cannot know the path before dispatch
- Issue: `spec:62` says the contract is `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed", and it must be "known before dispatch". Three rows break this: adversarial (`spec:83`) is to be changed to `<output>/adversarial/return-contract.yaml`, which is not `<output-dir>/return-contract.yaml`; workflow (`spec:92`) writes `.dev/tasks/to-do/<id>/return-contract.yaml`, not into a passed directory; tdd (`spec:90`) and init-lite (`spec:87`) take `--output <file>`, which is a file, not a directory. The inventory records that real adversarial runs wrote the contract in two different places (`INV-A:60`). WC-4's "keep their fields" wording does not say the location is kept.
- Sentence: "An implementer who writes the adversarial contract at `<output>/return-contract.yaml`, as `spec:62` says, breaks the path that `spec:83` requires; and one who follows `spec:83` breaks `spec:62`."
- Severity: MAJOR, blocking (two stated paths contradict, and the coordinator's brief depends on the path).
- Expert: Fowler (interface), Newman (contract evolution), Hohpe (message contract).
- Recommendation: state the rule per output kind: directory outputs get `<dir>/return-contract.yaml`; file outputs get `<file's directory>/<command>-return-contract.yaml` or similar; workflow is a named exception. Then rewrite `spec:83`, `:87`, `:90`, `:92` to match.
- Priority: High. Quality impact: high (drives every brief and the report-path check in `spec:182`).

### B-4 (BLOCKING): `--unattended` auto-accepts reflect remediation, which lets the worker approve its own corrective work
- Issue: `spec:88` (P2 for reflect) says "Under `--unattended`, make `--remediate` follow the existing headless auto-accept rule instead of the `[yes / no]` prompt". Headless auto-accept "skips the gates" for auto-fixable registers (INV-B:109, citing `remediation-handoff.md:239-247`, UNVERIFIED here). `spec:122` (tasklist) passes `--unattended` to every reflect at Stage 10.5, so the same auto-accept applies inside tasklist. The spec's own safety rule for implement (D2, `spec:236`) says the rule "exists to stop an agent approving its own work". The inventory recommended removing the nested remediation offer at Stage 10.5 (`INV-B:295`); the spec does not disposition that recommendation. SA-6 (`spec:151`) keeps the headless rule for `claude --print`; it does not require the unattended path to reuse it.
- Sentence: "An implementer who follows `spec:88` runs `/sc:workflow` or `task-builder` corrective work from a worker with no person approving it, and that is wrong because the spec treats agent self-approval as a safety boundary in D2 (`spec:236`)."
- Severity: MAJOR, blocking (safety-boundary risk; the grading rule names it).
- Expert: Nygard (failure and approval boundary), Cockburn (who approves), Wiegers (an undocumented default).
- Recommendation: under `--unattended` the reflect remediation gate resolves as blocked (WC-2 (c)) with the proposed remediation named in the contract, unless the brief passes an explicit flag that the coordinator's user instruction names (D4, `spec:244-247`). Record the choice in section 9 and disposition `INV-B:295`.
- Priority: High. Quality impact: high (a default that removes a human gate on code-changing work).

### B-5 (BLOCKING): WC-5 maps an empty, truncated or unrecognised contract to `succeeded`
- Issue: `spec:63` sends `--outcome failed` "when the report says `failed` or `blocked`, or no report exists" and `--outcome succeeded` "otherwise". A contract that exists but is empty, truncated (killed mid-write), unparseable, or has a `status` outside the four values in `spec:262` falls into "otherwise". The literal text therefore reports a crashed run as succeeded. Orca settles the Task on `succeeded` and then starts dependents (CAPS:76-77, CAPS:84-88).
- Whittaker, FR-2.1 (Zero/Empty): "I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (spec:63)** fails when **the contract exists with zero bytes or a truncated body**. Concrete attack: the command is killed after creating `return-contract.yaml`; the file exists, the status is absent, the branch falls to 'otherwise', `worker_done --outcome succeeded` is sent, the Task settles `completed`, and a dependent Task runs on no output." Trace: before = crashed run; after = Task `completed`.
- Sentence: "An implementer who follows `spec:63` as written sends `succeeded` for an empty contract, and that is wrong because the run did not finish."
- Severity: MAJOR, blocking (concrete wrong outcome from the literal text).
- Expert: Nygard (failure modes), Whittaker (FR-2.1, FR-2.3), Hohpe (ordering and delivery).
- Recommendation: default to `failed` for any contract that is missing, empty, unparseable, lacks `status`, or has a value outside the four. Keep `partial` as `succeeded` only for a parsed `partial`. Say so in the WC-5 text and add the case to AC-2.2.
- Priority: High. Quality impact: high (silent success on a crash).

### M-1 (Medium): WC-1 has no owner and no phase
- Issue: `spec:59` makes WC-1 a launch-path obligation ("Launch setup, not commands") with evidence from the `CCSESSION_ASK_TIMEOUT` fallback (EVIDENCE:39,45,56, UNVERIFIED here). No phase in section 6 (`spec:158-162`) names the wrapper or hook, and AC-0.4 only catches a failure after it happens.
- Expert: Fowler (ownership), Wiegers (requirement without an owner).
- Recommendation: assign WC-1 to P0 with its own acceptance check (a `worker-start` with no answerer reaches `input_accepted` within 60 s).

### M-2 (Medium): partial is reported as succeeded and nothing stops a dependent Task from consuming partial output
- Issue: `spec:63` and the decision at `spec:263` map `partial` to `succeeded`, and Orca settles the Task on that outcome (CAPS:77). `spec:73` says the coordinator opens the report after `worker_done`, but no rule says dependents wait for the contract `status`. A dependent therefore starts on partial output. The spec calls the partial "usable", which is a guess about the consumer.
- Sentence: "An implementer who follows `spec:73` starts a dependent Task on a partial upstream, and that is wrong if the dependent needs the complete output; the text does not forbid it."
- Expert: Hohpe (delivery semantics), Newman (contract between services).
- Recommendation: require the coordinator to read `status` before it creates or starts a dependent, or send `partial` as `failed` with the report attached.

### M-3 (Medium): the order of the contract write and `worker_done` is not stated
- Whittaker, FR-2.4 (Sequence): "I can break this specification by **Sequence Attack**. The invariant at **WC-4 and WC-5 (spec:62-63)** fails when **`worker_done` is sent before the contract is written, or the write fails after it**. Concrete attack: `worker_done --report-path <contract>` settles the Task `succeeded`; the write fails; the coordinator opens a missing file." `spec:62` implies write-then-send ("the worker passes the contract path") but does not state it.
- Recommendation: state write-then-verify (`test -s`) before `worker_done`, and that a failed write means `--outcome failed`.

### M-4 (Medium): WC-3's answer path and ask timeout are undefined
- Issue: `spec:61` lets the worker re-invoke "with the answer as a flag", but section 3 names answer flags only for a few gates (review-translation's context input, `spec:117`; cli-eval's `--suite`, `spec:104`). For tdd's topic clarification, `/task` ambiguity and similar gates no flag exists, so WC-3 cannot be carried out for them. The `ask` default timeout is unknown (CAPS:68; UNVERIFIED 10 at `spec:281`), so a parked worker has no bound on its wait.
- Whittaker, FR-2.2 (Divergence): "I can break this specification by **Divergence Attack**. The invariant at **WC-2 (c) vs WC-3 (spec:60-61)** fails when **a gate is both 'blocked' and 'asked'**. Concrete attack: the worker asks, the coordinator never replies, and the run waits with no heartbeat (`spec:70`, CAPS:64) while the coordinator's `check --wait` times out after 900 s (`spec:182`)."
- Recommendation: make WC-3 optional per gate, list each answer flag in section 3, and state the worker's maximum wait (set `--timeout-ms` explicitly in the brief).

### M-5 (Medium): the SA-2 check (AC-C1) misses `orca-cli` and uppercase `ORCA`
- Issue: `spec:172` matches `orca(-ide)? <orchestration|worktree|terminal|agent>` in lowercase only. It does not match `orca-cli worktree rm` (CAPS:115 names `orca-cli` for worktree removal) or `ORCA orchestration` as typed in the spec's own examples (`spec:180-186`). SA-2 (`spec:147`) forbids any Orca command in a command, so a violating file can pass AC-C1.
- Adzic (testability): an acceptance check that cannot fail on the thing it forbids.
- Recommendation: extend the pattern to `orca-cli`, `orca`, `ORCA` in any case, and add a negative fixture to `tests/skills/test_worker_contract.py`.

### M-6 (Medium): SA-4 allows only additive edits, but section 3 needs edits to existing lines
- Issue: SA-4 (`spec:149`) allows existing lines to change only for a named defect fix. Section 3 also requires changes to existing behaviour that are not in that list: cli-eval's wait split (`spec:104`, WC-10), cli-eval's Wave-0 "confirm" becomes STOP (`spec:104`), task's TFEP report not committed (`spec:121`). AC-C5 (`spec:176`) would fail on any of them that edits an existing line rather than adding an override.
- Recommendation: state that behaviour changes under `--unattended` are made only as added override text in the `## Unattended mode` section, and add the four cases to SA-4's list explicitly.

### M-7 (Medium): the nesting claim for tasklist and reflect is not counted
- Issue: `spec:122` says reflect's fan-out "runs one layer below the worker, inside Claude Code's nesting limit" (INV-A:14). A top-level worker (`CAPS:161`) runs tasklist, which starts a subagent per reflect (layer 1); reflect's Tier 2 reviewers and `sc:adversarial` add layers (INV-A:14 says at the limit the Agent tool is withdrawn). The spec does not count them.
- Whittaker, FR-2.5 (Accumulation): the layer count is the accumulation boundary; a reflect at the limit silently loses its Agent tool and its Tier 2 fan-out. Concrete: Stage 10.5 reports `succeeded` with a Tier 1-only audit.
- Recommendation: count the layers for each fan-out command and state the expected behaviour at the limit.

### M-8 (Medium): the plugin mirror is unresolved and not covered by any check
- Issue: `spec:279` (UNVERIFIED 8) says the update rule for `plugins/superclaude/commands/` is not read and "each phase's plan must resolve this before editing", but no phase does (`spec:158-162`). AC-C1, C2 and C5 cover only `src/superclaude/` paths. P1 edits will leave the mirror stale unless the check covers it.
- Recommendation: add a P0 step that resolves the mirror rule, and extend AC-C2 to the mirror.

### M-9 (Medium): P0 smoke runs use "ready" commands without `--unattended`, so WC-2 is not tested
- Issue: section 3.1 says the ten ready commands "run as workers now if the brief uses the stated flags" (`spec:79`), but the `--unattended` flag does not exist until P1 (`spec:159`). P0 (`spec:158`, AC-0.4 at `spec:194`) therefore tests "ready" through brief discipline, not through WC-2. A gate that a brief fails to avoid (tdd's topic-only prompt, `INV-B:47`; troubleshoot's `--depth deep` STOP) can still stall in P0.
- Recommendation: state that P0 proves only that the brief avoids gates, and add one P0 run with a gate-hitting input that must end `failed` or stall-free.

### M-10 (Medium): WC-10's 4-minute rule has no rule for an iteration over 4 minutes
- Issue: `spec:68` splits waits "of at most 4 minutes", but the pr-submit poll runtime is UNVERIFIED (`spec:283`) and cli-eval's eval can run up to 3600 s (INV-A:65). AC-4.3 (`spec:210`) tests only pr-submit. The spec does not say what the worker does when one iteration runs over 4 minutes.
- Recommendation: state the rule (for example, the command must chunk its own wait, or the brief sets a lower wait) and add a check for cli-eval.

### M-11 (Medium): testability is weak for the requirements that matter most
- Adzic/Wiegers: most acceptance checks need a live Orca run or a manual step (AC-0.4, 1.2, 1.3, 2.2 to 2.5, 3.2, 3.4, 4.1 to 4.3). Only AC-1.1, 2.1, 3.1, 3.3 and the grep checks are automated. WC-5 (the outcome mapping, the core of B-5) has no automated test at all; `tests/skills/test_worker_contract.py` (`spec:195`) only checks presence of text.
- Recommendation: add unit-level tests for the WC-5 mapping with fixture contracts (empty, truncated, `partial`, unknown `status`).

### M-12 (Medium): WC-12 says "natural checkpoints" without a definition
- `spec:70` says the worker runs `check` at "natural checkpoints and once before `worker_done`". Count and placement are undefined; the CAPS:66-67 text does not define them. Recommendation: name them (for example, before each gate, and after each fan-out wave), or name a fixed interval.

### M-13 (Medium): no rule when `--output` is omitted in an unattended brief
- Issue: `spec:62` requires `<output-dir>` from the brief. Several rows say "add an output path" (`spec:86`, `:99`, `:101`) without saying what a worker does when the flag is missing. adversarial defaults its output to the input file's directory (INV-A:61, citing `sk/sc-adversarial-protocol/SKILL.md:605`, UNVERIFIED here), so an unattended worker can write into the source tree.
- Whittaker, FR-2.1 (Zero/Empty): "I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (spec:62)** fails when **the output argument is absent**. Concrete attack: the brief omits `--output`; the adversarial run writes its six artifacts next to the input files in the checkout."
- Recommendation: under `--unattended`, a command without its output argument resolves as blocked (WC-2 (c)).

## === ARCHITECTURE ANALYSIS ===

### M-14 (Medium): WC-11 is not carried by the commands the spec says it protects
- Issue: `spec:69` (WC-11) requires default output paths to carry a timestamp or slug. Section 3 keeps fixed output dirs for several commands (cleanup-audit `.claude-audit/`, `spec:85`, and the single-owner memory keys, `spec:119`, where WC-11 is the only fix). "One audit per worktree at a time" is a restriction the coordinator must enforce, and the spec does not say so in section 4 or section 9.
- Fowler (shared state): recommend a per-command lock rule in the brief template (section 2.3).

### M-15 (Medium): the coordinator brief template has no stated owner or version
- Section 2.3 (`spec:73`) and P0 (`spec:158`) put a coordinator brief template inside `WORKER-CONTRACT.md`, which is an installed core document (`spec:52`) that the coordinator and the commands both read. The coordinator is an Orca coordinator session (`spec:215`), not a command, so one installed file serves two consumers with different owners. Newman (service boundaries): the spec does not say which side owns its versioning or what happens when the two drift.
- Recommendation: state the owner and version the template with the contract.

Architecture findings beyond these are folded into B-3 (contract path) and M-7 (nesting). Hohpe's view on the status vocabulary is folded into M-2.

## Follow-up candidates (Medium and minor, not blocking)

Medium: M-1 to M-15 above.

Minor:
- N-1: `spec:215` cites `CAPS:12-13` for "a coordinator session following Orca's own guide". Those lines are key-table entries, not the claim. Point to the `[G]` source line.
- N-2: `spec:80` (WC-11) says workers "share the current worktree by default". CAPS:115 says "Use the current or an exact existing workspace by default". The spec states more than the quote.
- N-3: `spec:23` (E3) says the PR #329 run landed; the only in-workspace reference is `README:12`, which restates the claim. Mark it as such in section 1.2.

## Quality assessment (0-10)

- Clarity: 6 (the table structure is clear; the WC-4 and WC-5 wording is not).
- Completeness: 7 (all 43 commands are placed; the rollout, acceptance checks and open decisions are present).
- Testability: 4 (most checks are live or manual; AC-C1 has a gap; WC-5 has no automated test).
- Consistency: 4 (B-1, B-3 and the SA-4 versus section 3 conflict).

## Expert consensus and disagreements

- Consensus: the decision to keep commands as units of work and to make `--unattended` opt-in is sound and matches the inventory evidence.
- Disagreement, resolved in this review: Whittaker's FR-2.1 finding on the WC-5 default (B-5) is blocking because the literal text produces a wrong outcome; Wiegers would treat it as a missing restriction (Medium). The grading check in the FIRST-REVIEW prompt decides it: the sentence holds with no further assumption, so it is blocking.

## Pipeline and FR-8 / FR-9 status

- Guard table: 12 rows, 7 GAP rows: B-3 (contract path), B-4 (reflect remediation), B-5 (two WC-5 rows), and M-4 (ask timeout), M-10 (wait over 4 min) and M-13 (missing output) carried as Medium. FR-9 (blank behaviour): none blank.
- FR-10 (table complete): satisfied.

## Reviser brief

Blocking findings: B-1, B-2, B-3, B-4, B-5.

Restated from review-loop step 6: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not part of this brief.

Brief clauses overridden: none.

verdict: FAIL
