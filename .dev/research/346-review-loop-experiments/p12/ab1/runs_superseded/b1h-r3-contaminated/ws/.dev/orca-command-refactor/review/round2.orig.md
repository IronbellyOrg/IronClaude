review: 2 of 3

# /sc:spec-panel critique, re-review 2 of 3 (focus: requirements, architecture)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 bddecb0d53d012639197cb333a623b97ec5dd535120f7fee296fb97a980e41db
baseline: .dev/orca-command-refactor/specs/history/spec-v1.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
prior: .dev/orca-command-refactor/review/round1.md sha256 dd876a370c80fa8da9fbff58abae0cbb5829e01458ba86beed8531e9e7fa7424 (`review: 1 of 3`, `verdict: FAIL`)
reviewer model: claude-haiku-5-5
review number: N = 2 (prior header `review: 1 of 3`, `.dev/orca-command-refactor/review/round1.md:1`)
baseline check: the prior report's `candidate:` hash (`round1.md:5`) equals the hash of the baseline, so the text reviewed in review 1 is the baseline text.
inputs: candidate, baseline and prior were all readable and hashable; none is missing.
rf-qa.md: neither `.claude/agents/rf-qa.md` in the workspace nor `~/.claude/agents/rf-qa.md` exists in this sandbox, so the Process of the Fix Cycle steps were not applied; the Review Loop rules in this report stand alone (`command.md` Review Loop item 5).
re-review brief: `~/.claude/rules/prompts/document_review_loop_prompts.md` RE-REVIEW prompt, read in full (lines 38-51).
not read: round1-a/b/c, verify-1.md, findings-1.md and revise1.md. They are not inputs named by the brief; the verification outcome is taken from the prior report (`round1.md:12`).
not checkable here: `src/superclaude/` and the Orca guide (`[G]` sources). Inventory lines are checked only as quoted in `.dev/orca-command-refactor/inventory/`. Anything else is marked UNVERIFIED.

## Step 1: evidence block

Command: `diff -w` of the baseline against the candidate. Changed lines copied verbatim (whitespace-only changes ignored). Roles are fixed as above: BASELINE is `specs/history/spec-v1.md`, CANDIDATE is `specs/orca-worker-contract-spec.md`.

BEFORE (baseline), lines starting with `<`:

```text
| WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
| WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
| adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
| cli-portify | each of the three approval gates resolves as blocked with the artifact to review named in the contract | contract (fields already defined; file location unnamed) | add a `--resume <contract>` flag that uses the existing `resume_phase`/`resume_substep` fields | dispatch only inside an IronClaude checkout (hardcoded template path) | `sk/sc-cli-portify-protocol/SKILL.md:69,152,170,393,464-473,517-566,529`; `cmd/cli-portify.md:23,34`; `INV-A:45,68` | P2 |
| load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
| research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract naming the generated `claudedocs/research_*.md` path | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
| AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
| `/sc:load` handling | Add a report file; use it only inside another worker's brief | Use it inside a brief: its only output is context for the current session (`INV-B:65`); a report file would be an unrequested addition. Only its usage-line defect is fixed. |
```

AFTER (candidate), lines starting with `>`:

```text
| WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer passed verbatim as the flag that the section 3 row names for that gate. This relay applies only to gates whose section 3 row names such a flag. It never applies to a safety or authorization gate: the implement Ruling (D2), the post-release and pr-submit outward authorizations (D3, D4), the cli-eval safety flags, and auggie-review posting (WC-9). Those gates resolve as blocked whatever the coordinator answers, unless the user chooses D2 option (b) [M2]. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
| WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome succeeded` only when `status` is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). `--outcome failed` for every other case: `status` is `failed` or `blocked`; `status` is missing, unparseable, or any value outside the four in WC-4 (for example `done` or an empty value); or no report exists [M4, M9]. The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
| adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Write the contract at `<output>/return-contract.yaml`, the WC-4 path, not a subdirectory (P1) [M4] | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
| workflow | `--handoff none`; from P1 also `--output-dir <dir>` [M10] | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome"); with `--output-dir`, write it to `<output-dir>/return-contract.yaml` instead of the per-run package path (P1) [M10] | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
| cli-portify | each of the three approval gates resolves as blocked with the artifact to review named in the contract | contract at `<output-dir>/return-contract.yaml` (fields already defined; file location unnamed today) [M10] | add a `--resume <contract>` flag that uses the existing `resume_phase`/`resume_substep` fields | dispatch only inside an IronClaude checkout (hardcoded template path); add `--output-dir` (new flag, SA-3) that WC-4 uses under `--unattended` [M10] | `sk/sc-cli-portify-protocol/SKILL.md:69,152,170,393,464-473,517-566,529`; `cmd/cli-portify.md:23,34`; `INV-A:45,68` | P2 |
| load | no gate | status-only contract under `--unattended` (`status`, `command`; no `report_path`, as WC-4 allows) [M8] | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
| research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract at `<output-dir>/return-contract.yaml`, naming the generated `claudedocs/research_*.md` path [M10] | fresh file | add `--output-dir` (new flag, SA-3); the research file keeps its generated path unless the flag is passed [M10] | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
| AC-C1 | `grep -rniE '\borca\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v -e '^src/superclaude/skills/ccsession-tag/' -e '^src/superclaude/core/WORKER-CONTRACT\.md:' -e '^src/superclaude/core/HOW-WE-WORK\.md:'`. Self-test, must exit 0: `printf 'orca orchestration worker-start\n' \| grep -iE '\borca\b'` | prints nothing; the self-test shows the pattern matches a bare `orca` or `orca-ide` word, not only four subcommands (SA-2, WC-8) [M7]. The two excluded core files may name Orca (SA-2, SA-5) |
| P0 | AC-0.5 | `uv run pytest tests/skills/test_worker_contract.py -q -k outcome` on planted contracts whose `status` is `done`, missing, or `partial` | `done` and missing map to `--outcome failed`; `partial` maps to `succeeded` (WC-5; M4, M9) |
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names `<output-dir>/return-contract.yaml` (no subdirectory); workflow states the contract is written for pre-creation STOPs [M4] |
| P1 | AC-1.5 | 7.2 live check on `/sc:workflow "<small change>" --handoff none --unattended --output-dir <dir>`, with one pre-creation STOP case | `worker_done --report-path` equals `<dir>/return-contract.yaml`, and the file exists (WC-4 path; M10) |
| P2 | AC-2.6 | 7.2 live check on `/sc:research` and on `/sc:cli-portify`, each with `--unattended --output-dir <dir>` | `worker_done --report-path` equals `<dir>/return-contract.yaml` for each (WC-4 path; M10) |
| `/sc:load` handling | Add a report file; use it only inside another worker's brief | Use it inside a brief: its only output is context for the current session (`INV-B:65`). Under `--unattended` it writes a status-only contract with no report file [M8], which meets WC-4 and AC-1.1 without adding a report. Only its usage-line defect is fixed. |
```

Self-check (`grep -nF`, run before the verdict): each of the 10 BEFORE lines is found in the baseline and in no line of the candidate; each of the 13 AFTER lines is found in the candidate. No role was swapped, so Step 1 stands.

## Prior blocking findings (from `round1.md:140`, "Reviser brief")

Prior blocking ids: M2, M4, M7, M8, M9, M10. Status: `resolved|open|regressed`.

| id | prior defect (round1.md) | status | basis in the candidate |
|---|---|---|---|
| M2 | WC-3 let a coordinator answer any gate, including the implement Ruling (round1.md:18-23) | resolved | WC-3 now relays only for gates whose section 3 row names a flag, and excludes the implement Ruling, the post-release and pr-submit authorizations, the cli-eval safety flags and auggie-review posting (`specs/orca-worker-contract-spec.md:61`). The implement row names no flag (spec:109), so the relay does not reach it. Residual terms are on a changed line: R2-4, R2-5. |
| M4 | A missing or unknown `status` became `succeeded` (round1.md:27-32); the adversarial contract had two paths (round1.md:34-38) | resolved | WC-5 sends `succeeded` only for `succeeded` or `partial`; missing, unparseable or other values go to `failed` (spec:63). The adversarial row now names the WC-4 path, not a subdirectory (spec:83). Planted-status test AC-0.5 added (spec:195). Its test target is undefined: R2-2. |
| M7 | AC-C1 could not fail (round1.md:40-53) | resolved | AC-C1 now matches the bare word `\borca\b` case-insensitively and carries a self-test that a planted line matches (spec:172). Whole-file exemptions on a changed line: R2-3. |
| M8 | The load row contradicted WC-4 and AC-1.1 (round1.md:55-59) | open | The row now writes a status-only contract under `--unattended` (spec:112), which fixes the missing contract. Three texts still conflict; see B1. |
| M9 | WC-5 mapped a `done` or empty status to `succeeded` (round1.md:61-65) | resolved | Same text as M4: WC-5 (spec:63), AC-0.5 (spec:195). |
| M10 | Workflow, research and cli-portify had no fixed contract path (round1.md:67-74) | resolved | Each row now names `<output-dir>/return-contract.yaml` with a new `--output-dir` flag (spec:92, spec:105, spec:116). AC-1.5 and AC-2.6 check the path (spec:200, spec:206). Residual ambiguity on the research report: R2-1. |

## Blocking findings

### B1 (= M8, open). The load row gives a contract that WC-4 does not allow, and the phase rows say the contract is not added

- Origin: changed (spec:112 is on a changed line; spec:268 is on a changed line).
- Issue, three conflicting texts:
  1. WC-4 says the contract "carries at least" `status`, `command`, `report_path` (if any), `artifacts` (every other file written) and, when blocked, `blocked_question` (spec:62). The load row writes "status-only contract ... (`status`, `command`; no `report_path`, as WC-4 allows)" (spec:112). `artifacts` is required by WC-4 and is absent from the row, so the row contradicts WC-4 on a field WC-4 does not make optional.
  2. The Decisions row says the status-only contract "meets WC-4 and AC-1.1" (spec:268). Point 1 shows it does not meet WC-4.
  3. The load row keeps "P1 (usage line only)" (spec:112, Phase column), and the P1 scope lists "load (usage line only)" (spec:159). An implementer who follows P1 adds no Unattended-mode section and no contract for load, so AC-1.1 (spec:196), which requires such a section for every command in 3.1 and 3.2, fails for load.
- Sentence that holds with no further assumption: an implementer who follows the load row writes a contract with `status` and `command` only, and WC-4 (spec:62) says it must also carry `artifacts`; an implementer who follows the P1 phase text adds nothing for load, and AC-1.1 (spec:196) then fails.
- Experts: Wiegers (traceability between the row, WC-4 and AC-1.1), Fowler (interface contract), Nygard (failure path: a contract that the coordinator cannot read the same way for each command).
- Priority: High. Impact: low to medium (one missing field and one mismatched phase label; the coordinator reads the contract only if load is dispatched as a Task, which spec:112 says it is not).
- Recommendation (for the reviser, who chooses one): give load a contract with `status`, `command` and `artifacts: []`, and change its P1 phase text to match; or name load as an exception in WC-4 and AC-1.1 with the reason. The Decisions row (spec:268) must agree with whichever is chosen.

## Findings on changed lines (Medium; follow-up candidates, not blocking)

Medium findings never trigger a revision or fail the review (`command.md` Review Loop item 2).

- R2-1 (Medium, origin=changed, spec:116). The research row says "add `--output-dir` (new flag, SA-3); the research file keeps its generated path unless the flag is passed". It does not say whether passing `--output-dir` also moves the research report. The contract's `report_path` (WC-4, spec:62) then names a file whose location the text leaves open, and AC-2.6 (spec:206) checks only the contract path. Experts: Fowler, Wiegers. Grading: needs a guess about which location the implementer picks, so Medium.
- R2-2 (Medium, origin=changed, spec:195). AC-0.5 runs `pytest -k outcome` on "planted contracts" to check the WC-5 mapping. The spec defines no function or entry point that performs the mapping: WC-5 is an instruction to the worker (spec:63), and the P0 test file is called "static" (spec:158). An implementer has to invent the code under test. If no test matches `-k outcome`, pytest exits with code 5 (UNVERIFIED here; pytest is not in the sandbox). Experts: Crispin, Adzic. Grading: Medium (needs a guess).
- R2-3 (Medium, origin=changed, spec:172). AC-C1 excludes all of `src/superclaude/core/WORKER-CONTRACT.md` and `HOW-WE-WORK.md`. SA-2 (spec:147) allows Orca text in the contract only as "an example of a caller's question channel", so an `orca orchestration ...` command line placed in the contract would pass AC-C1. The check cannot detect the one case SA-2 limits. Experts: Crispin, Nygard.
- R2-4 (Medium, origin=changed, spec:61 and spec:104). WC-3's exclusion names "the cli-eval safety flags", and the cli-eval row requires "the safety flags in the brief" (spec:104). The spec never lists them. The inventory calls them "safety flags" from the skill at `S:135-146` (`inventory/commands-a.md:44`), and that skill is not in the sandbox (UNVERIFIED). An implementer cannot tell whether `--suite` is a safety flag and so whether the relay may answer it. Also, the task row's commit/push authorization (spec:121) is not named in the exclusion list, although D4 (spec:247) lists it as an outward authorization; it is excluded only because its row names no flag. Experts: Wiegers, Whittaker.
- R2-5 (Medium, FR-9 blank behavior, origin=changed, spec:61). WC-3 passes the answer "verbatim as the flag"; it does not say what happens when the coordinator's answer is empty or a refusal. Experts: Adzic, Nygard. Grading: Medium (an implementer must guess).
- R2-6 (minor, origin=changed, spec:172). The AC-C1 pass condition reads "prints nothing; the self-test shows the pattern matches...", which joins two outputs in one cell. The self-test prints one line by design and must exit 0. A reader can misread the pass condition. Note only.

## Guard Condition Boundary Table (changed guards only; re-review scope)

Guards on changed lines: WC-5 status rule (spec:63), WC-3 relay gate (spec:61), and the load contract (spec:112 against spec:62). Input classes that cannot occur are left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 status | `specs/orca-worker-contract-spec.md:63` | Typical | `status: succeeded` | true | `--outcome succeeded` (spec:63) | OK |
| WC-5 status | spec:63 | Legitimate edge | `status: partial` | true | `--outcome succeeded` (spec:63); AC-0.5 covers it (spec:195) | OK |
| WC-5 status | spec:63 | Zero/Empty | `status:` empty, or key absent | false | `--outcome failed` (spec:63: "missing", "empty value") | OK |
| WC-5 status | spec:63 | Sentinel Value Match | `status: done` | false | `--outcome failed` (spec:63); AC-0.5 covers it (spec:195) | OK |
| WC-5 status | spec:63 | Malformed input | unparseable YAML | false | `--outcome failed` (spec:63: "unparseable") | OK (not tested by AC-0.5, spec:195) |
| WC-5 status | spec:63 | Zero/Empty (file) | no contract file | false | `--outcome failed` (spec:63: "no report exists") | OK (not tested by AC-0.5) |
| WC-5 status | spec:63 | Legitimate edge | audit with verdict FAIL and `status: succeeded` | true | `--outcome succeeded`; the verdict is only in prose | OK by text; noted M3 |
| WC-5 status | spec:63 | Maximum/Overflow | not applicable | n/a | left out: `status` is a fixed four-value set, with no bound to test | n/a |
| WC-3 relay | `specs/orca-worker-contract-spec.md:61` | Gate whose row names no flag | relay not available | false | blocked (spec:60 (c), spec:61) | OK |
| WC-3 relay | spec:61 | Excluded gate (implement Ruling) | any coordinator answer | false | blocked whatever the answer (spec:61; implement row spec:109) | OK |
| WC-3 relay | spec:61 | Gate whose flag is "safety" | cli-eval safety flags | not decidable from the text | the excluded set is not defined (spec:61, spec:104) | GAP (R2-4, Medium) |
| WC-3 relay | spec:61 | Blank answer | empty string | not specified | none stated (spec:61) | GAP (R2-5, Medium) |
| WC-4 contract | `specs/orca-worker-contract-spec.md:62` against spec:112 | load under `--unattended` | `status` and `command` only | WC-4 requires `artifacts` | contract does not match WC-4 | GAP (B1, blocking) |

Synthesis gate (FR-10): every changed guard has a row or a stated reason for being left out.

## Expert findings (focus: requirements, architecture; Whittaker always active)

- Wiegers: B1 (traceability across the load row, WC-4 and AC-1.1); R2-4 (undefined "safety flags").
- Adzic: R2-2 (no example or check that exercises the WC-5 mapping); R2-5 (blank answer has no example).
- Cockburn: no new finding on changed lines.
- Fowler: R2-1 (the research report and contract path); B1 (the contract's field set differs between commands).
- Newman, Hohpe: no new finding on changed lines; WC-3's relay path is still a request-response path with no stated timeout (spec:61 relies on UNVERIFIED `ask` timeout, spec:284 item 10).
- Nygard: R2-3 (contract exemption); R2-5 (failure path for a blank answer).
- Whittaker: WC-5 holds for each class in the guard table below; the one contested class is the audit with a FAIL verdict and `status: succeeded`, which is noted as M3 (below) and is not graded here.

## Noted, unactioned (verifier-rejected in round 1; not blocking; not re-graded)

These stay notes under the Review Loop (`round1.md:76-133`; rule in the re-review prompt, lines 56-57). Premise checks are recorded for the coordinator; I did not reinstate any of them.

- M1 (origin=unchanged; spec:118-119 unchanged). Not re-graded.
- M3 (origin=changed: WC-5 at spec:63 is on a changed line; the audit clause is unchanged from the baseline). Premise check: `inventory/orca-capabilities.md:73` quotes the rule "Never encode failure only in prose" from the Orca guide `[G]` lines 88-90, which is not in the sandbox. The inventory quote is present, so the verifier's "UNVERIFIED in this sandbox" applies to the guide text only. The coordinator should decide whether to re-run VERIFY on M3.
- M5 (origin=changed: AC-C1 is on a changed line). Its substance is R2-3 above; the verifier's rejection stands.
- M6 (origin=unchanged; spec:194 unchanged). Not re-graded.
- M11 (origin=unchanged; WC-6 spec:64 unchanged). Not re-graded.
- M12 (origin=unchanged; spec-panel row spec:120 unchanged). Premise check: the verifier said `command.md:23` and `:459-460` are not in this sandbox. They are present here. `command.md:23` lists `[--output <file>]`, and `command.md:460` says "`--output` is file-valued". `command.md:455-466` already has an "Unattended mode" section that uses `--report-dir` and `~/.claude/WORKER-CONTRACT.md`. The spec's spec-panel row says "add `--output`" (spec:120), and `inventory/commands-b.md:43` says there is no output path. The coordinator should re-check M12 before P1, since spec-panel is in the P2 scope (spec:160) and the premise differs from the command file.

## Verdict

Blocking findings open: 1 (B1, which is M8). Prior blocking findings resolved: M2, M4, M7, M9, M10. Open: M8.

Coverage: all 13 AFTER lines and all 10 BEFORE lines of the diff; all six prior blocking ids; the Guard Condition Boundary Table for the three changed guards; the expert panel for focus requirements and architecture; the rejected-id premises that the sandbox can check (M3, M12). Not covered: `src/superclaude/` and the Orca guide (not in the sandbox).

Follow-up candidates (Medium and minor; the coordinator asks the user once whether to open issues for them; none were created by this review): R2-1, R2-2, R2-3, R2-4, R2-5, R2-6.

Gating: the blocking finding goes through the VERIFY step before any revision (`command.md` Review Loop item 3 and the VERIFY prompt, prompts file lines 53-59). No fourth review is run here.

Reviser brief

Blocking finding ids: B1 (M8).
Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names (spec:62, spec:112, spec:159, spec:268 for B1); add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
