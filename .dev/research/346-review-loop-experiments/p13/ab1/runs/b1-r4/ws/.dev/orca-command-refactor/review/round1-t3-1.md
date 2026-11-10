review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec, round 1

## Report header

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`, run as the spec-panel worker, FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`.
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`.
- Baseline: missing (first review, no `--re-review`, no `--baseline`).
- Reviewer model: claude-haiku-5-5, one reviewer. `superclaude review panel resolve` is not available here (`command -v superclaude` printed nothing), so one reviewer ran; the loop summary records this.
- Panel lenses: Wiegers (lead), Adzic, Cockburn for requirements; Fowler (lead), Newman, Hohpe, Nygard for architecture; Whittaker is active in every panel review. Crispin, Gregory and Hightower were not invoked because the focus does not cover testing or cloud deployment; test-related points are noted as Wiegers and Adzic points.
- Mandatory artifacts: the Guard Condition Boundary Table is produced (the candidate has guard conditions). The Pipeline Dimensional Analysis is not triggered. The State Variable Registry is not required (correctness focus is not active).
- Output: this file. No other file was written; the candidate was not edited.
- Severity labels: the findings block uses the `findings-v1` labels (MAJOR, MINOR). The text grades each finding as Blocking, Medium or Minor under the command's grading rule.

## Coverage and citation check

Covered: every section of the candidate (1 to 9, the Decisions table and UNVERIFIED items), the section 7 acceptance commands, and the README at `.dev/orca-command-refactor/README.md`.

Citations checked against files in the workspace:

- `.dev/orca-command-refactor/README.md:11-17`, `:12`, `:31`: match the candidate's descriptions.
- Inventory lines spot-checked: `inventory/orca-capabilities.md` CAPS:52, 67, 73, 76-77, 80, 86, 91, 92, 103, 116, 129, 130, 145, 147, 149, 151, 155, 158, 161; `inventory/commands-a.md` INV-A:14, 38, 43, 62, 66, 76-83, 94-98; `inventory/commands-b.md` INV-B:46, 47, 114, 272, 289-299, 323. All quoted text matches the cited line.
- Every quotation this report uses from the candidate was confirmed as a single exact occurrence with `grep -F`.
- UNVERIFIED (source outside the sandbox, not checkable): `src/superclaude/**` (for example `src/superclaude/commands/auggie-review.md:51-54` and `sk/sc-implement-protocol/refs/qa.md:238`), `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/**`, `pyproject.toml:38`, `plugins/superclaude/**`, and the project CLAUDE.md rules. Where a finding depends on one of these, the finding relies on the inventory's quotation of it and says so. The implement rule (qa.md:238) is checkable only as quoted at INV-A:66.
- `command.md:459` (this review's command file) is checkable and is used in F14.

Line references to the candidate use `spec:N` for `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`.

## Requirements analysis

=== REQUIREMENTS ANALYSIS ===

**F1. Blocking (MAJOR, contradiction). WC-3 lets a coordinator's answer re-invoke a blocked gate, which contradicts the implement rule and the spec's own D2(a) recommendation.**
- Location: spec:61 (WC-3: "wait, then re-invoke or resume the command with the answer as a flag"); spec:234 (D2(a), recommended: the halt is not ruled by the coordinator); spec:235 (D2(b)); spec:67 (WC-9); spec:245 (D4(a)). The rule quoted at INV-A:66 says "another agent's message" is not acceptance.
- Grading sentence: an implementer who follows WC-3 as written, on an implement halt, re-invokes `/sc:implement` with the coordinator's reply as the Ruling flag, and that is wrong because D2(a) recommends that only the person rule and the rule quoted at INV-A:66 says another agent's message is not acceptance.
- Expert: Wiegers (consistency), Whittaker.
- Recommendation: limit WC-3's relay to gate rows in section 3 that name it. Exclude the implement Ruling (D2) and every outward flag (WC-9, D4) until the user decides, and say so in WC-3.
- Priority: High. Quality impact: high (the safety rule is decided by an unstated default).

**F2. Medium (other). The ask, resume and worker_done order is undefined.**
- Location: spec:61 (WC-3, "may instead ask ... then re-invoke or resume"), spec:63 (WC-5, `--outcome failed` when blocked), spec:200 (AC-2.2, expects `failed` and contract `blocked`). CAPS:77: a valid worker_done settles the Task and Dispatch automatically.
- Grading sentence: an implementer who follows WC-3 and WC-5 cannot tell whether worker_done is sent before the ask resolves; a failed worker_done settles the Dispatch (CAPS:77), so the later resume has nothing to resume, which needs an assumption about order, so Medium.
- Expert: Fowler (interaction), Hohpe (message order).
- Recommendation: add the sequence ask, wait, then resume or worker_done; state that worker_done is never sent while an ask is pending; AC-2.2 must name the path it tests.
- Priority: Medium.

**F3. Medium (missing-requirement). Worker tool approvals are not covered, and E2 claims tool parity without evidence.**
- Location: spec:60 (WC-2 covers only `AskUserQuestion` and chat questions), spec:22 (E2: "a command run by a worker has the same tools as a command a person runs"). CAPS:161 shows only `--agent claude`.
- Grading sentence: an implementer who follows WC-2 does not forbid or pre-approve tool-permission prompts; a worker whose permission mode prompts on a non-allowlisted Bash call parks on a prompt only a person can answer (CAPS:129), which needs an assumption about the permission mode, so Medium.
- Expert: Nygard (failure modes), Wiegers.
- Recommendation: add a worker launch requirement for permission mode and allowed tools (next to WC-1); reword E2 as a hypothesis checked by AC-0.4.
- Priority: High for the P0 smoke run.

**F4. Medium (other). Section 1.1 understates the change.**
- Location: spec:16 ("What changes in the commands is limited to the worker contract in section 2"), spec:75-125 (27 commands change, including gate conversions at spec:103-105 and spec:109-110, drift fixes at spec:118 and spec:124-125, and shared-state rules at spec:119), spec:149 (SA-4 admits existing lines change).
- Grading sentence: a reader who trusts 1.1 expects a contract-only change and underestimates the 27 command edits, which needs an assumption about which section a reader trusts, so Medium.
- Expert: Fowler (scope), Wiegers.
- Recommendation: restate 1.1 as "commands gain the worker contract, plus the per-command gate, report and drift fixes in section 3".
- Priority: Medium.

**F5. Medium (missing-requirement). Phase coverage misses two commands.**
- Location: spec:159 (P1 says `--unattended` is accepted by "every command in sections 3.1 and 3.2"), spec:84 (brainstorm), spec:87 (init-lite, small fix "None"). Brainstorm and init-lite appear in no phase, and nothing adds init-lite's WC-4 contract.
- Grading sentence: an implementer who follows P1 and P2 never adds the flag to brainstorm or the contract to init-lite, which is a missing requirement, so Medium.
- Expert: Wiegers (traceability).
- Recommendation: add brainstorm (flag only) and init-lite (contract, fresh output, and the F6 fix) to P1.
- Priority: Medium.

**F6. Blocking (MAJOR, contradiction). init-lite is "ready" while a retry overwrites the first attempt's output.**
- Location: spec:87 (init-lite: "Re-run overwrites its marked report", verdict ready), spec:64 (WC-6: a retry "must not corrupt the first attempt's output" and must either resume or "write each run into a fresh output directory"). No phase in spec:158-162 changes init-lite.
- Grading sentence: an implementer who follows the init-lite row runs a retry with `worker-start --retry-of` against the same `--output` file, overwrites the first attempt's report, and that is wrong because WC-6 forbids corrupting the first attempt's output; both stated texts cannot hold together.
- Expert: Nygard (recovery), Wiegers (consistency).
- Recommendation: move init-lite to needs-change in section 3.2; require a new `--output` path for every retry (2.3); add the change to P1.
- Priority: High.

**F7. Medium (missing-requirement). WC-4 defines no output directory for commands whose output location is fixed or has no flag.**
- Location: spec:62 (WC-4: `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)"), spec:85 (cleanup-audit: output dir fixed), spec:86 (index-repo: flags "none"), spec:87 (init-lite).
- Grading sentence: an implementer who follows WC-4 for index-repo has no flag to pass, so no path for `return-contract.yaml` is defined, which P1 resolves only by its own planned "state the output location", so Medium.
- Expert: Fowler (interface), Wiegers.
- Recommendation: name a fallback location per command in section 3 (for index-repo, the repo-root path already implied in INV-A:53).
- Priority: Medium.

**F8. Medium (other). Outcome mapping lets partial and failing audits settle dependent Tasks.**
- Location: spec:63 ("`--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL (the audit itself succeeded)"), spec:263 (decision: partial maps to succeeded). Orca settles the Task on worker_done (CAPS:77), ready dependents appear in the ready view (CAPS:86), and gates can hold a Task (CAPS:91).
- Grading sentence: an implementer who follows WC-5 and a coordinator that starts ready Tasks from the ready view starts a dependent on partial or FAIL output; the mitigation (2.3, spec:73, the coordinator opens the report) is not required before a start, so this needs an assumption, so Medium.
- Expert: Hohpe (message semantics), Whittaker (see the adversarial section).
- Recommendation: a dependent Task starts only when the contract status is `succeeded` and the verdict is not FAIL; otherwise create a gate (CAPS:91).
- Priority: High.

**F9. Medium (missing-requirement). WC-10 covers only single shell waits; Agent-tool fan-out can block past the heartbeat cadence.**
- Location: spec:68 (WC-10: "A command step that blocks a single tool call for longer than 5 minutes (a poll wait, a long eval) must be split"). Agent fan-out that runs for longer than 5 minutes: troubleshoot Tier 2 (spec:91, INV-B:49), tasklist Stage 10.5 reflect agents (spec:122, INV-B:46), tdd code agents (spec:90, INV-B:47).
- Grading sentence: an implementer who follows WC-10 cannot split an Agent call, so a 20-minute fan-out has no heartbeat and no split rule, which needs an assumption that heartbeat age matters (UNVERIFIED, CAPS:130), so Medium.
- Expert: Nygard (liveness).
- Recommendation: state the rule for Agent fan-out (no heartbeat during a blocked Agent call; the coordinator uses worker-show liveness), or split the fan-out into separate Tasks as section 1.3 does.
- Priority: Medium.

**F10. Medium (missing-requirement). WC-9 covers outward actions but not local changes that are hard to undo.**
- Location: spec:67 (WC-9 lists push, PR, GitHub post, install, provision, paid run). spec:88 (reflect: Wave 7 default-on folder move, INV-B:114), spec:103 (cleanup: applies code changes, INV-A:43).
- Grading sentence: an unattended reflect or cleanup worker moves or edits local files with no rule limiting them, which needs an assumption that such changes are acceptable, so Medium.
- Expert: Nygard, Wiegers.
- Recommendation: add a clause that unattended runs change only files inside the output directory and the files the brief names.
- Priority: Medium.

**F11. Medium (other). The auggie-review row relies on a `--post-pr` flag the inventory does not show.**
- Location: spec:100 ("posting returns only with an explicit `--post-pr` in the brief (WC-9)"). INV-A:38 says posting is the default and is turned off with `--no-post-pr` and `--no-remediation-offer`; no `--post-pr` appears. The command file cited at spec:100 is UNVERIFIED here.
- Grading sentence: an implementer who searches the command for `--post-pr` finds none, so PR posting can be neither authorized nor refused as written, which needs an assumption about the command file, so Medium.
- Expert: Wiegers (testability).
- Recommendation: name an existing flag, or add `--post-pr` to P2 (the row's "Other required change" says none).
- Priority: Medium.

**F12. Medium (unpassable-check). AC-C1 cannot match as written, and its scope conflicts with SA-2.**
- Location: spec:172 (AC-C1: the pattern contains `(orchestration\|worktree\|terminal\|agent)`, which in `grep -E` is a literal pipe, so the alternation never matches and the check prints nothing; the check scans `src/superclaude/core`). spec:147 (SA-2 allows an Orca mention in the contract file, which is installed under core per spec:52).
- Grading sentence: an implementer who copies the command literally runs a check that cannot fail, which needs the assumption that the escape is copied raw; whether it also conflicts with SA-2 depends on the contract text, so Medium.
- Expert: Wiegers (testability), Whittaker (the check itself as an attack target).
- Recommendation: use a plain `|` alternation in the grep -E pattern (outside the table escape), and either exclude `src/superclaude/core/WORKER-CONTRACT.md` from the scan or reword SA-2 to match the scan.
- Priority: Medium.

**F13. Medium (data-loss). A fenced attempt and its retry can write the same contract path. (Whittaker, Sequence attack; see the adversarial section.)**
- Location: spec:70 (WC-12: a fenced worker "stops without sending `worker_done`"), spec:62 (WC-4: "the command writes `<output-dir>/return-contract.yaml`"), spec:64 (WC-6 retry), CAPS:67 (consumer_fenced), CAPS:116 (`--retry-of`).
- Grading sentence: an implementer who writes WC-12 as the only stop rule lets a fenced attempt that is still running write its contract after the retry has written its own, which needs an assumption about timing, so Medium.
- Expert: Nygard, Whittaker.
- Recommendation: each dispatch writes to its own output directory (WC-6 default), and a fenced worker must stop writing before any further contract write.
- Priority: Medium.

**F14. Medium (other). The `--unattended` switch can be set by text (Whittaker, Sentinel Collision).**
- Location: spec:228 (D1(a): "It is testable by grep and cannot misfire on a person."), spec:51 (the term definition). `command.md:459` (this review's command file, checkable) says the mode applies only when `--unattended` is a standalone argument token outside any quoted argument; the candidate does not carry that rule.
- Grading sentence: an implementer who greps for the literal token in a brief or a quoted document turns unattended mode on, which needs an assumption about the input text, so Medium.
- Expert: Whittaker, Wiegers.
- Recommendation: copy the standalone-token rule into 2.1 and D1; drop the "cannot misfire" claim, or state that only the coordinator's brief sets the mode.
- Priority: Medium.

**F15. Medium (missing-requirement). The contract's failure cases are unspecified.**
- Location: spec:62 (WC-4: the contract is written on success, failure, blocked and partial outcomes; it "carries at least" the listed fields), spec:63 (WC-5 handles only "no report exists"), spec:183 (AC 7.2 step 4 checks the file only at acceptance).
- Grading sentence: an implementer who follows WC-5 cannot map a file with an unknown status (for example `ok`) or unparseable YAML to an outcome, which needs an assumption about the mapping, so Medium. The contract also has no version field (Newman).
- Expert: Newman (evolution), Wiegers.
- Recommendation: unparseable or missing fields map to `failed`; an unknown status maps to `blocked`; add `contract_version`.
- Priority: Medium.

**F16. Medium (missing-requirement). Retries of blocked Tasks are unbounded, and the retry brief is not specified.**
- Location: spec:73 (2.3 lists brief contents and does not require a new output directory for a retry), spec:64 (WC-6), CAPS:80 (a worker's own failed report does not trip the circuit breaker), CAPS:116 (retry and breaker).
- Grading sentence: a coordinator that retries a blocked Task with the same brief repeats the same gate without limit, because Orca counts only failed starts, which needs an assumption about the coordinator's policy, so Medium.
- Expert: Nygard.
- Recommendation: add to 2.3: a retry brief names a new output directory; a blocked Task is not retried unless the brief changes; set a retry cap.
- Priority: Medium.

**F17. Medium (missing-requirement). Section 7 has no check for hard-coded `src/superclaude` paths in installed primitives.**
- Location: spec:169-176 (common checks AC-C1 to AC-C5), spec:173 (AC-C2). The project CLAUDE.md rule "Never Hardcode `src/superclaude/` Paths in Installed Primitives" (UNVERIFIED in the sandbox; quoted in the session instructions) requires a grep before committing a new or edited primitive.
- Grading sentence: an implementer who follows section 7 can commit a new `## Unattended mode` section that names `src/superclaude/core/WORKER-CONTRACT.md`, which needs the assumption that CLAUDE.md is applied, so Medium.
- Expert: Fowler (boundaries), Wiegers.
- Recommendation: add AC-C6, the grep from CLAUDE.md, for every phase.
- Priority: Medium.

**F18. Medium (other). P1's automated test checks headings only; behaviour is covered only by live runs.**
- Location: spec:195 ("the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section"), spec:196-202 (live runs), spec:182 (step 3 needs a live Orca).
- Grading sentence: an implementer can pass AC-1.1 while a gate is mis-resolved, since the test checks only that the heading exists, so Medium.
- Expert: Adzic (examples), Wiegers (testability).
- Recommendation: add one static test per gate row in section 3.2, and label the live runs as the only behaviour evidence.
- Priority: Medium.

**F19. Medium (missing-requirement). WC-12 is silent on an empty check result and on check errors. (Guard table GAP; Whittaker, Zero attack.)**
- Location: spec:70 (WC-12). CAPS:67 says "An empty `check` never means you were replaced; `consumer_fenced` is the only way you learn that."
- Grading sentence: an implementer reading WC-12 alone can treat an empty result as a fence and stop a live worker without sending worker_done, which needs an assumption, so Medium.
- Expert: Nygard, Whittaker.
- Recommendation: quote CAPS:67 in WC-12 and state what a check error does.
- Priority: Medium.

**F20. Minor. The git row uses this run's constraint as command evidence.**
- Location: spec:133 (`/sc:git` row: "Its job is git itself ... `.dev/orca-command-refactor/README.md:31`"). README:31 is a rule for this run (README:30-31), not a property of `/sc:git`.
- Recommendation: keep the `/sc:git` evidence to `cmd/git.md` and the inventory lines.
- Priority: Low.

**F21. Minor. Citation drift in E4.**
- Location: spec:24 (E4 cites `CAPS:155` for `nested-worker-depth.js:7-11,18-22`). CAPS:155 gives lines 7-11 and 18-19; the 18-22 range appears at CAPS:40.
- Recommendation: correct the range.
- Priority: Low.

## Architecture analysis

=== ARCHITECTURE ANALYSIS ===

**F22. Medium (missing-requirement). The coordinator brief template is promised but not specified.**
- Location: spec:158 (P0 writes "a coordinator brief template listing the section 3.1 flags"), spec:73 (2.3 lists what a brief carries, but gives no template).
- Grading sentence: an implementer writing P0 produces a template that may omit the output directory or the outward authorization that 2.3 requires, which needs an assumption about what the template covers, so Medium.
- Expert: Fowler (interfaces), Newman (service boundary).
- Recommendation: put the template in the contract file as a fixed block with fields for command line, output directory, retry marker and authorizations.
- Priority: Medium.

Architecture points that are sound (no finding): the decision in 1.1 to keep commands as the unit of work with a coordinator above them is supported by the cited Orca facts (CAPS:92, CAPS:97-103), and the rejected alternative in 1.3 has evidence for each reason. The depth-1 finding (CAPS:97-101) is cited correctly.

## Whittaker adversarial analysis

Attack 1 (Sentinel Collision, F14). I can break this specification by **FR-2.3 Sentinel Collision Attack**. The invariant at **D1(a), spec:228** fails when **the literal token `--unattended` appears in quoted text that a brief or a spec-panel run reads**. Concrete attack: a document that quotes this candidate's section 2.1 (which contains `--unattended`) is passed as a brief argument; the token is read as the switch; gates that should block resolve as defaults, and nothing in the output records that the mode came from quoted text. Severity: MAJOR under attack, graded Medium because the trigger needs quoted input.

Attack 2 (Sequence Attack, F13). I can break this specification by **FR-2.4 Sequence Attack**. The invariant at **WC-12 (spec:70) and WC-4 (spec:62)** fails when **a fenced dispatch has not stopped while its retry runs**. Concrete attack: dispatch 1 writes `return-contract.yaml` with status `succeeded`; the coordinator fences it and retries into the same `--output`; dispatch 2 writes status `blocked`; dispatch 1's last write, before its next check, replaces the file with the stale `succeeded`; the coordinator opens the file and starts the dependent Task. Severity: MAJOR under attack, graded Medium (needs a race).

Attack 3 (Divergence Attack, F8). I can break this specification by **FR-2.2 Divergence Attack**. The invariant at **WC-5 (spec:63)** fails when **the report status is `partial` or an audit verdict is FAIL**. Concrete attack: a `/sc:adversarial` run returns verdict FAIL with status succeeded; Orca settles the Task (CAPS:77); the ready view lists the dependent (CAPS:86); the coordinator starts it on the failed output. Severity: MAJOR, graded Medium (needs the coordinator to skip the report).

Attack 4 (Zero/Empty, F19). I can break this specification by **FR-2.1 Zero/Empty Attack**. The invariant at **WC-12 (spec:70)** fails when **`check` returns an empty result**. Concrete attack: an empty check is read as a fence; the worker stops without worker_done; its Task stays running with no owner. CAPS:67 says this is not a fence. Severity: MAJOR, graded Medium.

## Guard Condition Boundary Table (mandatory)

Trigger: the candidate contains conditional logic (the `--unattended` switch, outcome mapping, the fence check, wait thresholds, resume-or-fresh-directory choice and gate resolution). The table is complete (FR-10): each guard lists the input classes that apply; classes left out are explained below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` switch | spec:51, spec:228 | Zero/Empty (flag absent) | `""` | false | Standalone behaviour (SA-1, spec:146) | OK |
| `--unattended` switch | spec:51, spec:228 | One/Minimal (token alone, no output dir) | `--unattended` | true | WC-4 has no output directory (spec:62) | GAP (F7) |
| `--unattended` switch | spec:51, spec:228 | Typical | `--unattended --output <dir>` | true | WC-2 to WC-4 apply | OK |
| `--unattended` switch | spec:51, spec:228 | Sentinel Value Match (token inside quoted text) | `"... --unattended ..."` | true under the D1(a) wording | D1(a) says it "cannot misfire" (spec:228) | GAP (F14) |
| `--unattended` switch | spec:51, spec:103-110 | Legitimate Edge Case (with `--interactive`) | `--unattended --interactive` | refused per row | Section 3 refuses `--interactive` per command (for example spec:103, spec:110, spec:118) | OK |
| WC-5 outcome mapping | spec:63 | Zero/Empty (no report) | none | failed | "no report exists" maps to `failed` | OK |
| WC-5 outcome mapping | spec:63, spec:263 | One/Minimal (status `partial`) | `partial` | succeeded | Mapped to `succeeded` (spec:263) | GAP (F8) |
| WC-5 outcome mapping | spec:63 | Typical (status `succeeded`) | `succeeded` | succeeded | Mapped | OK |
| WC-5 outcome mapping | spec:63 | Sentinel Value Match (unknown status, for example `ok`) | `ok` | unspecified | Not stated | GAP (F15) |
| WC-5 outcome mapping | spec:63 | Legitimate Edge Case (audit verdict FAIL, status succeeded) | `FAIL` | succeeded | Mapped to `succeeded` by spec:63 | GAP (F8) |
| WC-12 fence check | spec:70 | Zero/Empty (empty `check` result) | `""` | unspecified | Not stated | GAP (F19) |
| WC-12 fence check | spec:70 | Typical (`consumer_fenced`) | `consumer_fenced` | stop, no worker_done | Stop is specified; the stop is not immediate | GAP (F13) |
| WC-12 fence check | spec:70, spec:62 | Legitimate Edge Case (fence after the contract is written) | contract on disk | stop | Contract left behind is not addressed | GAP (F13) |
| WC-10 wait threshold | spec:68 | Zero/Empty (no wait) | 0 s | no split | Not needed | OK |
| WC-10 wait threshold | spec:68 | One/Minimal (poll wait) | 60 s | no split | Under the 4-minute limit | OK |
| WC-10 wait threshold | spec:68 | Typical | 120 s | no split | Under the 4-minute limit | OK |
| WC-10 wait threshold | spec:68, spec:91, spec:122 | Maximum/Overflow (one Agent-tool call of 20 min) | 1200 s | cannot split | No rule for Agent calls | GAP (F9) |
| WC-10 wait threshold | spec:68 | Sentinel Value Match (pr-submit 600 s cumulative budget) | 600 s | cumulative, split per iteration | Stated at spec:114 | OK |
| WC-10 wait threshold | spec:68, spec:104 | Legitimate Edge Case (cli-eval eval up to 3600 s) | 3600 s | split into waits of at most 4 min | Stated at spec:68 and spec:104 | OK |
| WC-6 resume or fresh dir | spec:64 | Zero/Empty (retry with no output path) | none | no fresh directory | Not specified (WC-4 needs the path) | GAP (F7) |
| WC-6 resume or fresh dir | spec:64 | One/Minimal (first run) | none | fresh directory | Specified | OK |
| WC-6 resume or fresh dir | spec:64, spec:104 | Typical (command has a resume flag) | resume flag | resume | Specified per row | OK |
| WC-6 resume or fresh dir | spec:64, spec:87 | Sentinel Value Match (retry reuses the failed attempt's directory) | same path | overwrite | Init-lite row accepts overwrite | GAP (F6) |
| WC-6 resume or fresh dir | spec:85 | Legitimate Edge Case (cleanup-audit fixed directory) | `.claude-audit/` | one audit per worktree | Stated at spec:85 and WC-11 | OK |
| WC-2 gate resolution | spec:60 | Zero/Empty (gate with no default, no flag) | none | blocked (c) | Specified | OK |
| WC-2 gate resolution | spec:60 | One/Minimal (one gate, blocked) | 1 | (c) | Specified | OK |
| WC-2 gate resolution | spec:60 | Typical (gate answered by flag) | flag | (b) | Specified | OK |
| WC-2 gate resolution | spec:61 | Sentinel Value Match (gate answered via `ask` reply) | reply text | re-invoke with the answer as a flag | Stated in WC-3, but conflicts with D2(a) | GAP (F1) |
| WC-2 gate resolution | spec:109, spec:234 | Legitimate Edge Case (implement Ruling) | halt | open (D2) | Open decision; WC-3 pre-decides it | GAP (F1) |

Classes left out, with reason:
- `--unattended` switch, Maximum/Overflow: a boolean token has no numeric range.
- WC-5, Maximum/Overflow: the status is one of four fixed values (spec:262).
- WC-12, Sentinel Value Match: check results are an API field, not user text (CAPS:67).
- WC-10, the other classes are all shown above.
- WC-6, Maximum/Overflow: no capacity dimension.
- WC-2, Maximum/Overflow: gates are enumerated per row in section 3; there is no count limit to exceed.

Pipeline Dimensional Analysis: not triggered. No stage in the candidate filters, aggregates or deduplicates counts. One Task gives one Dispatch and one contract; the only count change is a retry (F16), which is not a data-transforming stage. The Quantity Flow Diagram is therefore not produced.

## Follow-up candidates (Medium and minor; these never fail the review)

- F2 (ask, resume and worker_done order); F3 (worker tool and permission approvals); F4 (section 1.1 scope); F5 (phase coverage for brainstorm and init-lite); F7 (WC-4 output directory for fixed-location commands); F8 (partial and FAIL-verdict outcomes settle dependents); F9 (WC-10 and Agent fan-out); F10 (WC-9 and local changes); F11 (`--post-pr` flag); F12 (AC-C1 pattern and SA-2 scope); F13 (fenced attempt and retry share a path); F14 (`--unattended` set by text); F15 (contract failure cases and version); F16 (retry briefs and blocked-Task retries); F17 (hard-coded src paths check); F18 (headings-only test); F19 (WC-12 empty check); F20 (git row evidence, minor); F21 (E4 citation range, minor); F22 (brief template).
- The session that ran this review asks the user once whether to open issues for these. No issue is created by this worker.

## Quality metrics (0-10)

Clarity 6, Completeness 6, Testability 5, Consistency 4. Consistency is lowest because of F1, F6, F5 and F12.

## Loop summary

- Review 1 of 3, first review, no prior findings, no baseline.
- Blocking findings: F1 and F6. Verdict FAIL.
- Revision is the next step. This worker did not revise the candidate.

## Prior blocking findings

None (first review).

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "then re-invoke or resume the command with the answer as a flag", "anchor2": "The worker stops, writes the halt to its ledger and contract, and ends `failed`.", "refs": ["WC-3", "WC-9", "D2", "D4", "3.2 implement row"], "claim": "An implementer who follows WC-3 relays a coordinator answer as the implement Ruling, which the D2(a) recommendation and the rule quoted at INV-A:66 forbid."}
{"id": "F2", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "the session may instead ask the coordinator once with the preamble's", "anchor2": "`--outcome failed` when the report says `failed` or `blocked`", "refs": ["WC-3", "WC-5", "AC-2.2", "CAPS:77"], "claim": "The order of ask, resume and worker_done is undefined, so a worker can send failed first and lose the Dispatch the resume needs."}
{"id": "F3", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "never calls `AskUserQuestion`, never ends its turn on a chat question", "anchor2": "so a command run by a worker has the same tools as a command a person runs", "refs": ["WC-2", "E2", "CAPS:161", "CAPS:129"], "claim": "A worker whose permission mode prompts on a non-allowlisted tool call parks on a person-only prompt that WC-2 does not cover."}
{"id": "F4", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "What changes in the commands is limited to the worker contract in section 2", "anchor2": "Existing lines change only where section 3 names a defect fix", "refs": ["1.1", "3.2", "SA-4"], "claim": "A reader who trusts 1.1 underestimates the 27 command edits that change gate behaviour and drift."}
{"id": "F5", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "the `--unattended` flag accepted by every command in sections 3.1 and 3.2", "refs": ["P1", "3.1 brainstorm", "3.1 init-lite"], "claim": "Brainstorm and init-lite are in no phase, so the flag and init-lite's contract are never added."}
{"id": "F6", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "Re-run overwrites its marked report", "anchor2": "must not corrupt the first attempt", "refs": ["WC-6", "3.1 init-lite", "P1"], "claim": "A retry of init-lite with the same --output overwrites the first attempt's report, which WC-6 forbids, while the row still reads ready."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "is the directory the coordinator passed", "refs": ["WC-4", "3.1 cleanup-audit", "3.1 index-repo", "3.1 init-lite"], "claim": "Commands with fixed or absent output flags have no defined directory for return-contract.yaml."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "A partial run left a usable deliverable", "anchor2": "including an audit whose verdict is FAIL (the audit itself succeeded)", "refs": ["WC-5", "decision partial", "CAPS:77", "CAPS:86", "CAPS:91"], "claim": "Orca settles a partial or FAIL-verdict Task as completed, so ready dependents start on invalid input."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "A command step that blocks a single tool call for longer than 5 minutes", "refs": ["WC-10", "3.1 troubleshoot", "3.2 tasklist", "INV-B:47"], "claim": "A single Agent-tool fan-out call can block past the 5-minute heartbeat with no split rule."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "any default that pushes, opens a PR, posts to GitHub, installs, provisions or calls a paid external run is off", "refs": ["WC-9", "3.1 reflect", "3.2 cleanup", "INV-B:114", "INV-A:43"], "claim": "An unattended reflect or cleanup worker moves or edits local files with no rule limiting them."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "posting returns only with an explicit `--post-pr` in the brief", "refs": ["3.2 auggie-review", "INV-A:38"], "claim": "The --post-pr flag the row relies on is not in the inventory, so PR posting cannot be authorized or refused as written."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "unpassable-check", "anchor": "prints nothing (SA-2, WC-8)", "refs": ["AC-C1", "SA-2", "WC-8"], "claim": "AC-C1 as written never matches, so it passes whatever the commands contain."}
{"id": "F13", "severity": "MAJOR", "blocking": false, "category": "data-loss", "anchor": "if `check` returns `consumer_fenced` it stops without sending `worker_done`", "anchor2": "the command writes `<output-dir>/return-contract.yaml`", "refs": ["WC-12", "WC-4", "WC-6", "CAPS:116"], "claim": "A fenced attempt still writing its contract can overwrite the retry's contract with a stale status."}
{"id": "F14", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "It is testable by grep and cannot misfire on a person.", "anchor2": "a person never types it", "refs": ["D1", "2.1", "command.md:459"], "claim": "Quoted text containing the token switches unattended mode on, which the claim that it cannot misfire denies."}
{"id": "F15", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "It is written on success, failure, blocked and partial outcomes", "anchor2": "carries at least", "refs": ["WC-4", "WC-5", "7.2 step 4"], "claim": "A malformed, missing or unknown-status contract has no outcome mapping, so the coordinator can read an unsafe status."}
{"id": "F16", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "The contract only works if the brief carries what the command would otherwise ask a person", "refs": ["2.3", "WC-6", "CAPS:80", "CAPS:116"], "claim": "A coordinator that retries a blocked Task with an unchanged brief repeats the gate without limit, since Orca never trips a breaker on failed reports."}
{"id": "F17", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "exits 0 (SA-5)", "refs": ["AC-C2", "CLAUDE.md hardcoded-path rule"], "claim": "Section 7 lets a new Unattended-mode section ship with a hard-coded src/superclaude path because no check catches it."}
{"id": "F18", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "the test asserts that every command in sections 3.1-3.2 has", "refs": ["AC-1.1", "AC-1.2", "7.2"], "claim": "A gate can be mis-resolved while AC-1.1 still passes, since the test checks only that the heading exists."}
{"id": "F19", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "The worker runs `check` at natural checkpoints and once before `worker_done`", "refs": ["WC-12", "CAPS:67"], "claim": "A worker that reads an empty check as consumer_fenced stops without sending worker_done while still live."}
{"id": "F20", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Its job is git itself", "refs": ["4", "README:31"], "claim": "The git row uses a run-level constraint as command evidence."}
{"id": "F21", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "nested-worker-depth.js:7-11,18-22", "refs": ["E4", "CAPS:155", "CAPS:40"], "claim": "The cited line range for nested-worker-depth.js does not match CAPS:155."}
{"id": "F22", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "a coordinator brief template listing the section 3.1 flags", "refs": ["P0", "2.3"], "claim": "The promised brief template is not specified beyond the list in 2.3, so the coordinator's briefs will differ per run."}
```

Reviser brief: revise only the text that blocking findings F1 and F6 name (spec:61, spec:234-235 for F1; spec:87 for F6, with the WC-6 text at spec:64 as the requirement). Restated bullet 6: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not in this brief.

verdict: FAIL
