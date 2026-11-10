Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. Confirm Mn when any sub-entry holds, and name that sub-entry in the reason.

### M1

#### M1.a (round1-a.md B1)
### B1 (CRITICAL, blocking). The standalone-behaviour rule is contradicted by two rows
- Issue: SA-1 says that without `--unattended` every prompt and default stays as it is today (spec:146). The roadmap row replaces the default-on "Resume? [Y/n]" prompt with an explicit flag and says "resume only when passed" with no `--unattended` qualifier (spec:118). The save row says to write only per-session keys and never the single-owner keys, again with no qualifier (spec:119). WC-11 limits the single-owner exclusion to unattended mode (spec:69), so the two texts disagree. SA-4 allows only defect fixes outside additive edits (spec:149). The roadmap and save changes are not named as defect fixes there (only "roadmap and validate-roadmap drift" is named).
- Grading sentence: An implementer who follows the roadmap row as written builds `/sc:roadmap` that starts fresh without asking when an earlier session exists, and that is wrong because SA-1 (spec:146) requires the prompt to stay for a person in a plain session.
- Second instance: an implementer who follows the save row builds `/sc:save` that stops writing `pm_context`, `last_session` and `next_actions` in a plain session, which breaks `/sc:load` and `/sc:pm` resume (spec:119 against spec:146).

### M2

#### M2.a (round1-a.md B2)
### B2 (CRITICAL, blocking). WC-3 lets a coordinator answer any gate, which contradicts the spec's own three-way rule and the implement Ruling rule
- Issue: WC-2 says each gate resolves one of three ways (a default, a flag, or blocked) (spec:60). WC-3 adds a fourth path: the worker may ask the coordinator and then "re-invoke or resume the command with the answer as a flag" (spec:61). The implement row blocks on a halt and keeps the Ruling rule (spec:109). D2(a) recommends keeping that rule because another agent's message is not acceptance (spec:234), and the spec cites that rule as `refs/qa.md:238` (spec:109, CAPS and INV-A:66). D4(a) says outward authorization needs the user's own words, but WC-3 needs no quoting (spec:245 against spec:61).
- Attack (Whittaker, sentinel collision, see section below): a free-text coordinator answer is turned into a flag. WC-3 does not say which flag a free answer maps to.
- Grading sentence: An implementer who follows WC-3 as written asks the coordinator at the implement Ruling gate, resumes with the coordinator's reply as the Ruling flag, and the halt is cleared; that is wrong because `refs/qa.md:238` (cited at spec:109) says another agent's message is not acceptance, and WC-3 has no exception for it.

### M3

#### M3.a (round1-a.md B3)
### B3 (MAJOR, blocking). WC-5 reports a FAIL audit as `succeeded`, and no contract field carries the verdict
- Issue: WC-5 says `--outcome succeeded` for "an audit whose verdict is FAIL" (spec:63). WC-4 lists the contract fields `status`, `command`, `report_path`, `artifacts` and `blocked_question` and has no verdict field (spec:62). The verdict is therefore only in the body of `worker_done`, which WC-5 requires as prose ("The first sentence of the body states the report's status and verdict", spec:63). The spec cites the Orca rule "Never encode failure only in prose" (CAPS:73, from `[G]` lines 88-90). The spec breaks that rule for audits.
- Grading sentence: An implementer who follows WC-5 builds a coordinator that unblocks dependent Tasks when `worker_done --outcome succeeded` arrives, and that is wrong because the audit's FAIL verdict is only in prose and the coordinator's gate cannot read it (spec:63 with spec:62; CAPS:73).

### M4

#### M4.a (round1-a.md B4)
### B4 (MAJOR, blocking). A contract with a missing or unrecognised `status` is reported as `succeeded`
- Issue: WC-5 maps "`--outcome succeeded` otherwise" (spec:63). WC-4 requires `status` to be one of four values (spec:62). The spec does not say what happens when `status` is absent, misspelled, or holds another value (for example a command's own legacy status word, INV-B:272 for workflow).
- Attack (Whittaker, zero/empty, see section below): a worker writes a contract with no `status` key because its command predates the contract. The rule yields `succeeded`.
- Grading sentence: An implementer who follows the "otherwise" rule in WC-5 reports `worker_done --outcome succeeded` for a contract with no `status`, and that is wrong because WC-4 makes `status` required (spec:62), so a missing status is a failed contract.

#### M4.b (round1-a.md B5)
### B5 (CRITICAL, blocking). Two contract paths for the same adversarial output
- Issue: WC-4 says the contract is `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (spec:62). The adversarial row fixes the path as `<output>/adversarial/return-contract.yaml` (spec:83). The coordinator "knows the report path before dispatch" and opens it (spec:73), so the two rows give it different files.
- Grading sentence: An implementer who follows WC-4 writes the adversarial contract at `<output>/return-contract.yaml`, and the coordinator following the row opens `<output>/adversarial/return-contract.yaml`, finds nothing, and per WC-5 records the worker as `failed` ("no report exists", spec:63) when the run succeeded; the two texts contradict each other (spec:62 against spec:83).

### M5

#### M5.a (round1-a.md B6)
### B6 (MAJOR, blocking). Acceptance check AC-C1 cannot pass once P0 lands
- Issue: AC-C1 greps `src/superclaude/core` as well as commands, skills and agents (spec:172). It excludes only `ccsession-tag` (spec:172). SA-2 allows Orca text in the contract file as "an example of a caller's question channel" (spec:147). SA-5 requires an Orca section in `HOW-WE-WORK.md`, which is also under core (spec:150), and P0 adds the contract to core (spec:158). An Orca section or a contract example of the form `orca orchestration ask` would therefore match AC-C1 in P0 while the spec says it is allowed.
- Grading sentence: An implementer who writes the P0 files as SA-2 and SA-5 allow runs AC-C1 as written and gets matches in `src/superclaude/core`, so the common check fails although the content is permitted; the check cannot pass as written (spec:172 against spec:147, spec:150, spec:158).

### M6

#### M6.a (round1-a.md B7)
### B7 (MAJOR, blocking). AC-0.4 step 4 cannot pass for the P0 ready commands
- Issue: step 4 requires a YAML file with `status` in four values and a `command` key (spec:183). AC-0.4 says step 4 "uses the command's existing report file" (spec:194). The existing workflow contract, as listed at INV-B:272, has `status`, `plan_path` and `reflect_report_path`, and no `command` key. The existing troubleshoot report is `REPORT.md`, which is markdown (INV-B:49). The check as written fails for both.
- Grading sentence: An implementer who runs step 4 on `/sc:workflow --handoff none` as written hits `assert d['command']` against a contract that has no `command` key (INV-B:272), so P0 cannot pass its own acceptance check; the spec says the same check applies (spec:183 against spec:194).

---

=== ARCHITECTURE ANALYSIS ===

### M7

#### M7.a (round1-b.md F1)
**F1. MAJOR, blocking. Acceptance check AC-C1 cannot fail.** Expert: Wiegers (testability), Whittaker (FR-2.3 sentinel). `SPEC:172` is the only mechanical gate for SA-2 and WC-8: "prints nothing (SA-2, WC-8)". The check cannot fail, for two reasons. (a) The `\|` alternation is a literal pipe in `grep -E` (checked above), so the pattern matches only the literal text `orchestration|worktree|terminal|agent`. (b) Even with `|`, the pattern covers only four subcommands, is case-sensitive, and does not match `orca-ide status`, which the capabilities inventory uses (`CAPS:146`), or `orca-cli`. SA-2 forbids any `orca`/`orca-ide` command (`SPEC:147`).
Grading sentence: "An implementer who runs AC-C1 exactly as written sees empty output on every tree, records pass, and a command that runs `orca-ide orchestration worker-start` also passes, which is wrong because SA-2 and WC-8 forbid it."

#### M7.b (round1-c.md F2)
**F2. AC-C1 cannot fail on a real violation. [BLOCKING]**
- Issue: AC-C1 is the only mechanical check for SA-2 and WC-8. It uses `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b'` (`spec:172`). In an ERE, `\|` is a literal bar, not alternation, so the group only matches the text `orchestration|worktree|terminal|agent`.
- Checked: on a one-line probe file containing `orca orchestration task-create`, the spec's pattern printed nothing and exited 1. The same pattern with an unescaped `|` matched the line (exit 0). So AC-C1 passes on a tree that calls Orca from a command.
- Sentence that holds with no further assumption: an implementer who runs AC-C1 as written, on a command file that contains `orca orchestration worker-start`, gets empty output and records a PASS, so SA-2 and WC-8 are not enforced.

### M8

#### M8.a (round1-b.md F2)
**F2. MAJOR, blocking. The load row contradicts WC-4 and AC-1.1.** Expert: Wiegers (traceability). `SPEC:112` gives `/sc:load` report "none", and its phase as "P1 (usage line only)". `SPEC:76` says every changed command gains a `## Unattended mode` section that names its report file. `SPEC:159` requires P1 to accept `--unattended` for every command in 3.1 and 3.2, load included. `SPEC:62` (WC-4) requires the contract on every outcome. `SPEC:265` says a load report file would be "unrequested". `SPEC:195` (AC-1.1) requires every command in 3.1 and 3.2 to have a section "naming `return-contract.yaml`".
Grading sentence: "An implementer who follows the load row writes no `return-contract.yaml` and no Unattended mode section for `/sc:load`, so AC-1.1 fails for load and P1 cannot pass; an implementer who follows AC-1.1 or WC-4 must add a contract the load row and `SPEC:265` say not to add."

### M9

#### M9.a (round1-b.md F3)
**F3. MAJOR, FR-8 GAP, blocking. The outcome rule turns invalid status into success.** Expert: Nygard (guard boundaries), Whittaker (FR-2.1 zero/invalid input). `SPEC:63` maps to `--outcome succeeded` "otherwise", after `failed` and `blocked`. `SPEC:62` allows exactly four status values. `CAPS:73` says "Never encode failure only in prose".
Grading sentence: "An implementer who follows WC-5 as written sends `--outcome succeeded` for a contract whose status is `done` or empty, and that is wrong because the contract does not state success."

### M10

#### M10.a (round1-c.md F1)
**F1. WC-4 says the report path is known before dispatch, but two §3 rows make it unknown or unnamed. [BLOCKING]**
- Issue: WC-4 requires that in unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is passed by the coordinator (`spec:62`). §2.3 relies on this: the path "is known before dispatch" (`spec:73`). The §3.1 workflow row leaves the contract at `.dev/tasks/to-do/<id>/return-contract.yaml` (`spec:92`), and the P1 fix for workflow only adds pre-creation STOP contracts (`spec:92`, `spec:159`). The inventory says that package id is generated per run with "Fresh package each run" (`INV-B:52`, `INV-B:272`). The §3.2 research row names "contract naming the generated `claudedocs/research_*.md` path" and adds no output flag (`spec:116`; `INV-B:38` for the generated name). The cli-portify row says "file location unnamed" (`spec:105`; `INV-A:45`).
- Sentence that holds with no further assumption: an implementer who follows WC-4 and §2.3 has the coordinator pass `--output` and read `<output-dir>/return-contract.yaml`. An implementer who follows the workflow row keeps the contract at a per-run `<id>` path, so the file is not at the path the coordinator passed, and `worker_done --report-path` cannot be checked against WC-4.

### M11

#### M11.a (round1-c.md F3)
**F3. A retry can overwrite or misread the first attempt's contract. [BLOCKING]**
- Issue: WC-3 lets a worker re-invoke or resume the command after an answer (`spec:61`). WC-6 says a re-run "writes each run into a fresh output directory" when the command has no resume flag (`spec:64`). §2.3 lists what the coordinator owes each brief and does not include a fresh output directory on retry (`spec:73`). The contract has no field that binds it to a dispatch or Task (`spec:62` lists `status`, `command`, `report_path`, `artifacts`, `blocked_question`). WC-5 maps "no report exists" to `failed` (`spec:63`).
- Sentence that holds with no further assumption: an implementer who follows §2.3 passes the same `--output` on a retry. A retry that crashes before writing its own contract leaves attempt 1's `return-contract.yaml` in that directory (for example `status: succeeded`). WC-5 treats it as the report and maps it to `succeeded`, so a failed retry is recorded as a success and the first attempt's output is overwritten.
- Whittaker (FR-2.4 Sequence Attack): I can break this specification by **re-running after an ask timeout**. The invariant at **spec:61 (WC-3) and spec:64 (WC-6)** fails when **the re-run uses the same output directory and the command has no resume flag**. Concrete attack: **attempt 1 writes `status: succeeded` to `D/return-contract.yaml`; attempt 2 is re-invoked with `--output D` and crashes before writing; WC-5 reads the file from attempt 1 and sends `worker_done --outcome succeeded`; `D` now holds attempt 2's partial files over attempt 1's.**

### M12

#### M12.a (round1-c.md F4)
**F4. The spec-panel row conflicts with the command definition on `--output`. [BLOCKING]**
- Issue: WC-4 treats `--output` as a directory flag (`spec:62`). The §3.2 spec-panel row says "add `--output`; contract" and "`target_release` required as a flag" (`spec:120`). The command definition already has `--output <file>`, `--unattended`, `--report-dir <dir>` and `--target-release` in its usage line (`command.md:23`), accepts `--target-release` in any run (`command.md:37`), and says `--report-dir <dir>` is the report directory and "`--output` is file-valued" (`command.md:459-460`). The inventory row this spec relies on says spec-panel has no `--output` (`INV-B:43`, citing `cmd/spec-panel.md:22`, UNVERIFIED here, because that file is not in this sandbox).
- Sentence that holds with no further assumption: an implementer who follows WC-4 gives spec-panel `--output <dir>`, and `--output` then means a directory in one place and a file in the command definition (`command.md:23`, `:460`). The contract is written to the wrong place or the file is written into a directory.
