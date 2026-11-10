You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r3/vf1. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r3/vf1/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r3/vf1/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r3/vf1/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. Confirm Mn when any sub-entry holds, and name that sub-entry in the reason.

### M1

#### M1.a (round1-a.md B1)
### B1. WC-3 lets a coordinator's reply stand in for a gate answer, which reopens the /sc:implement Ruling rule
- Severity (panel): MAJOR, graded blocking under Review Loop bullet 2, because it names a safety-boundary risk.
- Location: `spec:61` (WC-3), `spec:109` (implement row), `spec:218` (non-goal 6), `spec:233-236` (D2).
- Grading sentence: an implementer who follows WC-3 as written, at an implement halt, asks the coordinator with `ask`, then re-invokes or resumes `/sc:implement` "with the answer as a flag". The coordinator's reply then serves as the Ruling. That is another agent's message, which `refs/qa.md:238` says is not acceptance (quoted in `INV-A:66`). The spec itself keeps this rule (`spec:109`, `spec:218`) and recommends D2(a) (`spec:236`).
- Also: WC-3 names an answer flag but no command defines one. The implement row (`spec:109`) gives none. So the path has no interface, and an implementer would invent one.

### M2

#### M2.a (round1-a.md B2)
### B2. The contract path rule in WC-4 assumes a directory and a known path. Section 3 rows contradict it
- Location: `spec:62` says `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)". `spec:73` says the report path is "known before dispatch (WC-4)".
- Contradicted by:
  - `spec:87` init-lite takes `--output <file>`.
  - `spec:90` tdd takes `--output <file>`, and `spec:200` (AC-2.2) uses `--output <file>` for tdd.
  - `spec:85` cleanup-audit has a fixed output dir (`.claude-audit/`) and no flag (`INV-A:42`). The row says so.
  - `spec:86` index-repo has no output flag, and its location is "implied" (`INV-A:53`).
  - `spec:92` workflow writes `.dev/tasks/to-do/<id>/`, where `<id>` is made at run time (`INV-B:52`, `INV-B:272`).
  - `spec:116` research writes a timestamped path "generated at run time" (`INV-B:132`).
- Grading sentence: an implementer who follows WC-4 for tdd passes `--output <file>` and writes `<file>/return-contract.yaml`, which cannot be created. For cleanup-audit and index-repo there is no directory to pass, so the coordinator cannot open the contract before dispatch, as `spec:73` requires.

### M3

#### M3.a (round1-a.md B3)
### B3. Section 2.3 requires `--unattended` in every brief, but P0 and AC-0.4 run three commands before the flag exists
- Location: `spec:73` (the brief "states the exact command line including `--unattended`"), `spec:180` (7.2 step 1 takes the brief "per section 2.3"), `spec:194` (AC-0.4 runs `/sc:troubleshoot`, `/sc:workflow`, `/sc:adversarial` with no flag), `spec:158` (P0 adds only the contract document, the KNOWN_CORE_FILES entry and the test file), `spec:159` (P1 adds the `--unattended` flag to every command).
- Grading sentence: an implementer who follows `spec:73` and `spec:180` in P0 passes `--unattended` to three commands that do not accept it until P1. AC-0.4 then fails at argument parsing. Following AC-0.4 literally breaks `spec:73`.

### M4

#### M4.a (round1-a.md B4)
### B4. The 7.2 step 6 check requires `git status` to show only output-dir files, but gate-converted commands edit product files on their happy path
- Location: `spec:185` (7.2 step 6, pass condition), `spec:201` (AC-2.3 applies 7.2 to every P2 command with every required flag).
- Commands whose happy path writes outside the output directory, by their own rows:
  - `spec:103` cleanup applies items the file allows without approval, which are edits (`INV-A:43`).
  - `spec:110` improve (`INV-A:52`).
  - `spec:121` task edits code.
  - `spec:105` cli-portify writes to `src/superclaude/cli/<name>/` by default (`INV-A:45`).
  - `spec:109` implement "Edits product files" (`INV-A:51`).
  - `spec:107` document inline mode edits source files (`INV-A:47`).
- Grading sentence: an implementer who runs AC-2.3 for cleanup with every required flag gets applied edits to tracked product files. Step 6 then fails, and AC-2.3 cannot pass as written.

### M5

#### M5.a (round1-b.md B-1)
### B-1 (BLOCKING). AC-C1 forbids the Orca wording that the spec requires in core files
- Location: candidate:172 (AC-C1 scans `src/superclaude/core`); candidate:147 (SA-2: "the only allowed mention of Orca ... is as an example of a caller's question channel inside the contract file"); candidate:52 and :158 (the contract file is `src/superclaude/core/WORKER-CONTRACT.md`; P0 also adds "an Orca section" to `HOW-WE-WORK.md`, which is in core).
- Issue: SA-2 permits an Orca example inside the contract file, and P0 requires an Orca section in the routing guide. AC-C1 pattern `\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b` scans core and allows only ccsession-tag. A contract or routing section that shows the question channel (for example `orca orchestration ask`) makes AC-C1 fail. The spec never says core is exempt.
- Grading check: "An implementer who follows SA-2 and P0 writes `orca orchestration ask` as the example in `WORKER-CONTRACT.md` and an Orca section in `HOW-WE-WORK.md`, and AC-C1 then fails on those two files, because AC-C1 scans `src/superclaude/core` and the spec exempts nothing there, so P0 can never pass its common check."

### M6

#### M6.a (round1-b.md B-2)
### B-2 (BLOCKING). AC-0.4 cannot pass as written in P0
- Location: candidate:73 (brief "states the exact command line including `--unattended`"); candidate:180 (7.2 step 1, brief per 2.3); candidate:182 (step 3, "its report path is the WC-4 contract path"); candidate:183 (step 4, asserts `d['status']` and `d['command']`); candidate:194 (AC-0.4 runs `/sc:troubleshoot`, `/sc:workflow --handoff none` and `/sc:adversarial --compare ... --output <dir>` with no `--unattended`; says step 4 "uses the command's existing report file, since the contract arrives in P1"); candidate:62 and :158-159 (WC-4 is unattended-only and arrives in P1).
- Issue, four separate failures:
  1. Step 1 requires the brief to carry `--unattended` (candidate:73), but P0 has no such flag (candidate:158 "no command edits"; candidate:159 adds it in P1). The AC's own command lines omit it.
  2. Step 3 requires the WC-4 path, which exists only in unattended mode (candidate:62) and only from P1. Neither P0 run is unattended.
  3. Step 4 asserts YAML keys, but AC-0.4 says step 4 reads the existing report. troubleshoot's existing report is `REPORT.md` (INV-B:49), which is Markdown and fails `yaml.safe_load` as a contract. workflow's contract has `status`, `plan_path`, `reflect_report_path` and no `command` key (INV-B:272), so `d['command']` raises KeyError.
  4. AC-0.4 says "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)", but step 5 (candidate:184) searches only for AskUserQuestion. The no-wrapper clause has no check.
- Grading check: "An implementer who runs AC-0.4 exactly as written in P0, without `--unattended`, finds that step 3 has no WC-4 path and that step 4 raises KeyError on `command` for workflow, so P0 cannot pass, because the flag, the path and the keys are all introduced only in P1."

### M7

#### M7.a (round1-b.md B-3)
### B-3 (BLOCKING). 7.2 step 5 fails on a worker that made no AskUserQuestion call
- Location: candidate:184 (step 5: "search the transcript for `AskUserQuestion`. Pass: no `AskUserQuestion` call."); candidate:60 (WC-2 requires the contract to say the command "never calls `AskUserQuestion`"); candidate:52 and :158 (the contract file is `~/.claude/WORKER-CONTRACT.md` and carries the section 2 rules); candidate:51-52 (every changed command's Unattended section points to it).
- Issue: the check is a text search of the transcript. The worker reads the contract (it is named in every Unattended section), and the contract's own text contains the string "AskUserQuestion" (WC-2 quotes it). Command files that describe their gates also contain it (for example INV-A:44 on cli-eval's AskUserQuestion menu). The step as written does not limit the search to tool-call entries, so a conforming worker returns a hit.
- Grading check: "An implementer who follows step 5 as written searches the whole transcript for the string, and the worker's read of the contract (required by candidate:60 and :52) returns a hit, so step 5 fails on a worker that made no call."

### M8

#### M8.a (round1-b.md B-4)
### B-4 (BLOCKING). Section 3.1 says ready commands change only by small fixes; P1 and AC-1.1 require more
- Location: candidate:79 ("The only command changes are the small fixes in the last column"); candidate:76 ("Every changed command also gains the `## Unattended mode` section"); candidate:84 (brainstorm, fix "None") and candidate:87 (init-lite, fix "None"); candidate:159 (P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 ... The WC-4 contract in unattended mode"); candidate:195 (AC-1.1 asserts a `## Unattended mode` section in every command in sections 3.1-3.2).
- Issue: a reader who follows candidate:79 leaves brainstorm and init-lite unchanged, so they have no flag and no section. AC-1.1 then fails for those two. P1 also says the flag must be accepted by all 3.1 commands. In addition, the phase table's Commands column (candidate:158-162) lists neither brainstorm nor init-lite, so no phase owns them, and reflect, release-split, tdd and troubleshoot (ready today) sit in P2.
- Grading check: "An implementer who follows the 3.1 introduction leaves brainstorm and init-lite without a `## Unattended mode` section and without the flag, and AC-1.1 then fails for those two, because AC-1.1 requires the section for every command in 3.1."

### M9

#### M9.a (round1-b.md B-5)
### B-5 (BLOCKING). The WC-4 contract path is contradicted by the per-command rows, and several commands have no directory to write into
- Location: candidate:62 (WC-4: `<output-dir>/return-contract.yaml`, where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)"); candidate:73 (the report path must be known before dispatch); candidate:83 (adversarial: "Fix the contract filename to `<output>/adversarial/return-contract.yaml`"); candidate:87 (init-lite: brief passes `--output <file>`); candidate:90 (tdd: `--output <file>`); candidate:92 (workflow: `.dev/tasks/to-do/<id>/return-contract.yaml`, "Fresh package each run"; the id is generated at run time); candidate:85 (cleanup-audit: "output dir is fixed"); candidate:86 (index-repo: `PROJECT_INDEX.md`, no directory flag); candidate:112 (load: "none"); candidate:116 (research: "contract naming the generated `claudedocs/research_*.md` path", no directory flag in P1 or P2 scope, candidate:159-160); candidate:120 (spec-panel: "add `--output`"; `command.md:23,460` shows `--output <file>` is already file-valued and unattended uses `--report-dir <dir>`).
- Issue: WC-4 defines one fixed rule (a directory from `--output`, containing `return-contract.yaml`). Adversarial's row puts it in a subfolder. Workflow's package id is not known before dispatch, which WC-4 requires. For tdd, init-lite and spec-panel the flag is a file, so WC-4 has no directory. Research, cleanup-audit, index-repo and load have no directory flag at all. WC-4 says the contract is written "including stops before any other output exists", which for workflow means a pre-creation stop has no path.
- Grading check: "An implementer who follows WC-4 writes `return-contract.yaml` directly under the `--output` directory, so for adversarial the coordinator opens `<output>/return-contract.yaml` while candidate:83 places the file at `<output>/adversarial/...`, and for tdd or init-lite the value is a file, so there is no directory to write into; the coordinator then finds no contract and cannot apply WC-5."
---

### M10

#### M10.a (round1-b.md B-6)
### B-6 (BLOCKING). AC-2.2 expects a blocked outcome for gates that the spec resolves by default
- Location: candidate:200 (AC-2.2: "`worker_done --outcome failed`; contract `status: blocked`" for every P2 command's gate-trigger run); candidate:60 (WC-2: each gate resolves (a) documented default, (b) flag, or (c) blocked); candidate:88 (reflect: `--remediate` follows the headless auto-accept rule, no block); candidate:100 (auggie-review: `--unattended` implies `--no-post-pr --no-remediation-offer`, so no gate); candidate:103 and :110 (cleanup and improve: apply auto items, list Approval Required items unapplied; that is (a)); candidate:116 (research: `--unattended` pins `--strategy planning`, so no gate); candidate:122 (tasklist: passes `--unattended` to reflect, so no gate of its own).
- Issue: AC-2.2 was written for (c) only. For auggie-review, cleanup, improve, reflect, research and tasklist, the spec's own rows produce a clean run with no blocked_question. The AC says "with input that hits the gate", but the rows do not produce a block for that input.
- Grading check: "An implementer who follows WC-2(a) for cleanup lists each Approval Required item unapplied, so the run ends `succeeded` with no `blocked_question`, and AC-2.2 requires `failed` and a non-empty `blocked_question`, so AC-2.2 fails for cleanup as written; the same holds for improve, reflect, tasklist, auggie-review and research."

### M11

#### M11.a (round1-b.md B-7)
### B-7 (BLOCKING). AC-2.3 expects cli-portify to succeed, but its gates always block
- Location: candidate:105 (cli-portify: "each of the three approval gates resolves as blocked"); candidate:201 (AC-2.3: happy-path run "passes with `--outcome succeeded`"); candidate:160 (cli-portify is in P2).
- Grading check: "An implementer who follows candidate:105 makes each of the three approval gates write `blocked` and stop, so every cli-portify run, including the happy path, ends `failed`, and AC-2.3 requires `succeeded`."

### M12

#### M12.a (round1-b.md B-8)
### B-8 (BLOCKING). Section 1.4 and E3 contradict each other on the direct-route evidence
- Location: candidate:43 (gap 1: "The only end-to-end proof is the PR #329 run, ... so it proves the nested route, not the direct route this spec requires"); candidate:23 (E3 cites `invocation_method: "skill-direct"` at `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:10` as evidence that Orca workers ran `/sc:adversarial` in the earlier run that landed as PR #329); INV-A:13 and INV-A:35 (same contract, "Proven as a direct Orca-worker skill call"). The contract file is outside the workspace, so its content is UNVERIFIED here; the contradiction is between the spec's own sentences.
- Grading check: "Two stated texts contradict: candidate:43 says the only end-to-end proof is nested and no direct-route proof exists, and candidate:23 cites a direct-route (`skill-direct`) contract from that same run as evidence."
---

Write your full reply to .dev/orca-command-refactor/review/verify-1.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
