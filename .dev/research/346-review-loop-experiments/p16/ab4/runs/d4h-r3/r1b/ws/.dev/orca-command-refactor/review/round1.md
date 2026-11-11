review: 1 of 3

# Review round 1: orca-worker-contract-spec (critique, focus requirements,architecture)

## Header

- Command: `/sc:spec-panel --mode critique --focus requirements,architecture` (FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:31-37`; `~` resolves to the sandbox home, so this is the file supplied for the run).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (computed in this run; equals the hash recorded in lint-1.md:1).
- Baseline: none (first review; no `--re-review`, no `--baseline`).
- Prior report: none. Review number: 1 of 3.
- Reviewer model actually used: claude-haiku-5-5 (Haiku 5.5), one reviewer in this worker.
- Lint: `.dev/orca-command-refactor/review/lint-1.md` (review-lint/1). It reports `Findings: 0` and `No findings.` (lint-1.md:3,5). Each lint id is addressed: none exist, so none is confirmed or dismissed. A lint id never fails a review by itself.
- Not run in this worker (coordinator steps): (a) the second independent first review and the MERGE rule (`~/.claude/rules/prompts/document_review_loop_prompts.md:35-36`); (b) the VERIFY prompt in a fresh context before any revision (`...:57-60`). Every blocking finding below is unconfirmed until VERIFY runs. Medium and minor findings are single-source.
- Verdict rule applied: `command.md:260` (verdict FAIL when a blocking finding is open).

## Coverage statement (FIRST-REVIEW brief)

- Read in full: the candidate; `README.md`; `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`; `review/lint-1.md`; the sandbox `command.md`; the review-loop prompt file.
- Checked against the workspace: about 25 inventory citations used by the spec (INV-A:13, :35, :42, :44, :90; INV-B:36, :49, :52, :109, :272, :285, :323; CAPS:46, :49, :52, :64, :74, :80, :88-90, :116-120, :125, :129-131, :161). All matched their stated content. One does not: INV-B:182 says spec-panel has no `--output` flag, which `command.md:23` contradicts (finding F-29).
- Not checkable in this sandbox, so every citation to them is UNVERIFIED here: `src/superclaude/**`, `plugins/**`, `.dev/evals/**`, `.dev/codegraph-migration/**`, the Orca application under `/opt/Orca` (quoted through CAPS), `~/.claude/WORKER-CONTRACT.md`, the installed `~/.claude/**` primitives, and CLAUDE.md (system context, not in the workspace). The spec's own claim that it re-read 11 of its src/ locations (candidate:11) is UNVERIFIED here.
- Two checks run in the sandbox with no files written: the AC-C5 pattern and the AC-C1 pattern were tested with `grep -E` on sample lines (results in F-1 and F-2). The candidate hash was computed.
- Interpretation used for the one-by-one acceptance review: an AC "cannot pass as written" when following its text literally fails, or the text gives no way to decide pass or fail. Under the grading check, such an AC is blocking when a stated text forces the failure (B-n). When the failure comes from a choice the spec leaves open, it is Medium (F-n).
- Mandatory artifacts: the Guard Condition Boundary Table is triggered (the candidate contains threshold and conditional rules: candidate:59-70, :121, :172-176) and is included below. The Pipeline Dimensional Analysis and Quantity Flow Diagram are not triggered: the spec describes dispatch, reports and release, not a record flow whose count changes between stages. The State Variable Registry is not triggered (no `--focus correctness`).
- Whittaker (adversarial, active in every panel review per `command.md:82-84`) is included in the adversarial section.

---

## Blocking findings (summary)

| ID | Bucket | Expert lead | Location | One line |
|---|---|---|---|---|
| B-1 | REQUIREMENTS | Wiegers | candidate:172, :147, :158 | AC-C1 forbids the Orca wording that SA-2 and P0 require in core files. |
| B-2 | REQUIREMENTS | Adzic | candidate:73, :180-183, :194 | AC-0.4 cannot pass in P0: it needs `--unattended`, a WC-4 path and YAML keys that P0 does not have. |
| B-3 | REQUIREMENTS | Adzic | candidate:184, :60, :52 | 7.2 step 5 literal search fails on a worker that read the contract but made no AskUserQuestion call. |
| B-4 | REQUIREMENTS | Wiegers | candidate:79, :76, :83-92, :159, :195 | Section 3.1 says ready commands change only by small fixes; P1 and AC-1.1 require the flag and section on all ten. |
| B-5 | ARCHITECTURE | Fowler | candidate:62, :73, :83, :87, :90, :92, :85-86, :112, :116, :120 | The WC-4 contract path is contradicted by per-command rows; several commands have no directory to write into. |
| B-6 | REQUIREMENTS | Wiegers | candidate:200, :60, :88, :100, :103, :110, :116, :122 | AC-2.2 expects a blocked outcome for gates that the spec resolves by default. |
| B-7 | REQUIREMENTS | Adzic | candidate:105, :201 | AC-2.3 expects cli-portify to succeed, but its three gates always block. |
| B-8 | REQUIREMENTS | Wiegers | candidate:43, :23 | Section 1.4 says no direct-route proof exists; E3 cites a skill-direct contract as proof. |

---

## === REQUIREMENTS ANALYSIS ===

### B-1 (BLOCKING). AC-C1 forbids the Orca wording that the spec requires in core files
- Expert: Karl Wiegers (lead), Gojko Adzic. Severity: CRITICAL under the blocking rule (two stated texts contradict).
- Location: candidate:172 (AC-C1 scans `src/superclaude/core`); candidate:147 (SA-2: "the only allowed mention of Orca ... is as an example of a caller's question channel inside the contract file"); candidate:52 and :158 (the contract file is `src/superclaude/core/WORKER-CONTRACT.md`; P0 also adds "an Orca section" to `HOW-WE-WORK.md`, which is in core).
- Issue: SA-2 permits an Orca example inside the contract file, and P0 requires an Orca section in the routing guide. AC-C1 pattern `\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b` scans core and allows only ccsession-tag. A contract or routing section that shows the question channel (for example `orca orchestration ask`) makes AC-C1 fail. The spec never says core is exempt.
- Grading check: "An implementer who follows SA-2 and P0 writes `orca orchestration ask` as the example in `WORKER-CONTRACT.md` and an Orca section in `HOW-WE-WORK.md`, and AC-C1 then fails on those two files, because AC-C1 scans `src/superclaude/core` and the spec exempts nothing there, so P0 can never pass its common check."
- Recommendation: exempt `src/superclaude/core/WORKER-CONTRACT.md` and the named HOW-WE-WORK section from AC-C1 by path and section, or move the example out of the scanned tree. Say in SA-2 whether core files are covered by the no-Orca-command rule.
- Priority: High. Quality impact: P0 cannot pass its common check, so every later phase is blocked.

### B-2 (BLOCKING). AC-0.4 cannot pass as written in P0
- Expert: Adzic (lead), Wiegers. Severity: MAJOR, blocking (stated texts contradict; the AC fails for every P0 command).
- Location: candidate:73 (brief "states the exact command line including `--unattended`"); candidate:180 (7.2 step 1, brief per 2.3); candidate:182 (step 3, "its report path is the WC-4 contract path"); candidate:183 (step 4, asserts `d['status']` and `d['command']`); candidate:194 (AC-0.4 runs `/sc:troubleshoot`, `/sc:workflow --handoff none` and `/sc:adversarial --compare ... --output <dir>` with no `--unattended`; says step 4 "uses the command's existing report file, since the contract arrives in P1"); candidate:62 and :158-159 (WC-4 is unattended-only and arrives in P1).
- Issue, four separate failures:
  1. Step 1 requires the brief to carry `--unattended` (candidate:73), but P0 has no such flag (candidate:158 "no command edits"; candidate:159 adds it in P1). The AC's own command lines omit it.
  2. Step 3 requires the WC-4 path, which exists only in unattended mode (candidate:62) and only from P1. Neither P0 run is unattended.
  3. Step 4 asserts YAML keys, but AC-0.4 says step 4 reads the existing report. troubleshoot's existing report is `REPORT.md` (INV-B:49), which is Markdown and fails `yaml.safe_load` as a contract. workflow's contract has `status`, `plan_path`, `reflect_report_path` and no `command` key (INV-B:272), so `d['command']` raises KeyError.
  4. AC-0.4 says "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)", but step 5 (candidate:184) searches only for AskUserQuestion. The no-wrapper clause has no check.
- Grading check: "An implementer who runs AC-0.4 exactly as written in P0, without `--unattended`, finds that step 3 has no WC-4 path and that step 4 raises KeyError on `command` for workflow, so P0 cannot pass, because the flag, the path and the keys are all introduced only in P1."
- Recommendation: state which checks are P0-valid. For P0, define the contract source per command (for example troubleshoot's REPORT.md with status taken from the worker_done outcome; workflow's existing contract with its real keys), or move AC-0.4 to after P1. Add an explicit check that the transcript shows no Agent-tool call wrapping the command.
- Priority: High. Quality impact: the decision gate in section 1.4 (candidate:43) cannot close, so Phase 0 never completes.

### B-3 (BLOCKING). 7.2 step 5 fails on a worker that made no AskUserQuestion call
- Expert: Gojko Adzic (lead). Severity: MAJOR, blocking (the check fails on a conforming worker).
- Location: candidate:184 (step 5: "search the transcript for `AskUserQuestion`. Pass: no `AskUserQuestion` call."); candidate:60 (WC-2 requires the contract to say the command "never calls `AskUserQuestion`"); candidate:52 and :158 (the contract file is `~/.claude/WORKER-CONTRACT.md` and carries the section 2 rules); candidate:51-52 (every changed command's Unattended section points to it).
- Issue: the check is a text search of the transcript. The worker reads the contract (it is named in every Unattended section), and the contract's own text contains the string "AskUserQuestion" (WC-2 quotes it). Command files that describe their gates also contain it (for example INV-A:44 on cli-eval's AskUserQuestion menu). The step as written does not limit the search to tool-call entries, so a conforming worker returns a hit.
- Grading check: "An implementer who follows step 5 as written searches the whole transcript for the string, and the worker's read of the contract (required by candidate:60 and :52) returns a hit, so step 5 fails on a worker that made no call."
- Recommendation: search tool_use entries whose name is `AskUserQuestion`, not the raw transcript text. State the transcript paging (F-8).
- Priority: High. Quality impact: every P1-P4 live check (7.2 step 5) fails on a correct run, so the phase gates cannot pass.

### B-4 (BLOCKING). Section 3.1 says ready commands change only by small fixes; P1 and AC-1.1 require more
- Expert: Karl Wiegers (lead). Severity: MAJOR, blocking (two stated texts contradict).
- Location: candidate:79 ("The only command changes are the small fixes in the last column"); candidate:76 ("Every changed command also gains the `## Unattended mode` section"); candidate:84 (brainstorm, fix "None") and candidate:87 (init-lite, fix "None"); candidate:159 (P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 ... The WC-4 contract in unattended mode"); candidate:195 (AC-1.1 asserts a `## Unattended mode` section in every command in sections 3.1-3.2).
- Issue: a reader who follows candidate:79 leaves brainstorm and init-lite unchanged, so they have no flag and no section. AC-1.1 then fails for those two. P1 also says the flag must be accepted by all 3.1 commands. In addition, the phase table's Commands column (candidate:158-162) lists neither brainstorm nor init-lite, so no phase owns them, and reflect, release-split, tdd and troubleshoot (ready today) sit in P2.
- Grading check: "An implementer who follows the 3.1 introduction leaves brainstorm and init-lite without a `## Unattended mode` section and without the flag, and AC-1.1 then fails for those two, because AC-1.1 requires the section for every command in 3.1."
- Recommendation: rewrite candidate:79 to say every ready command gains the flag and section (a no-op where there is no gate), and list brainstorm and init-lite in a phase's Commands column.
- Priority: High. Quality impact: P1 completion is ambiguous for two of ten ready commands.

### B-6 (BLOCKING). AC-2.2 expects a blocked outcome for gates that the spec resolves by default
- Expert: Karl Wiegers (lead), Gojko Adzic. Severity: MAJOR, blocking (the AC's required outcome contradicts WC-2(a)).
- Location: candidate:200 (AC-2.2: "`worker_done --outcome failed`; contract `status: blocked`" for every P2 command's gate-trigger run); candidate:60 (WC-2: each gate resolves (a) documented default, (b) flag, or (c) blocked); candidate:88 (reflect: `--remediate` follows the headless auto-accept rule, no block); candidate:100 (auggie-review: `--unattended` implies `--no-post-pr --no-remediation-offer`, so no gate); candidate:103 and :110 (cleanup and improve: apply auto items, list Approval Required items unapplied; that is (a)); candidate:116 (research: `--unattended` pins `--strategy planning`, so no gate); candidate:122 (tasklist: passes `--unattended` to reflect, so no gate of its own).
- Issue: AC-2.2 was written for (c) only. For auggie-review, cleanup, improve, reflect, research and tasklist, the spec's own rows produce a clean run with no blocked_question. The AC says "with input that hits the gate", but the rows do not produce a block for that input.
- Grading check: "An implementer who follows WC-2(a) for cleanup lists each Approval Required item unapplied, so the run ends `succeeded` with no `blocked_question`, and AC-2.2 requires `failed` and a non-empty `blocked_question`, so AC-2.2 fails for cleanup as written; the same holds for improve, reflect, tasklist, auggie-review and research."
- Recommendation: give AC-2.2 one row per P2 command naming the gate and its expected resolution. Require `failed` and `blocked_question` only where the row says (c) (for example cli-eval, tdd, spec-panel, task, recommend, review-translation, troubleshoot `--depth deep`, release-split `--r1-scope custom`, cli-portify). Expect `succeeded` for the (a) and (b) rows.
- Priority: High. Quality impact: 6 of 15 P2 gate checks cannot be run as written, and a correct run reads as a failure.

### B-7 (BLOCKING). AC-2.3 expects cli-portify to succeed, but its gates always block
- Expert: Gojko Adzic (lead), Karl Wiegers. Severity: MAJOR, blocking (the AC's required outcome contradicts a stated row).
- Location: candidate:105 (cli-portify: "each of the three approval gates resolves as blocked"); candidate:201 (AC-2.3: happy-path run "passes with `--outcome succeeded`"); candidate:160 (cli-portify is in P2).
- Grading check: "An implementer who follows candidate:105 makes each of the three approval gates write `blocked` and stop, so every cli-portify run, including the happy path, ends `failed`, and AC-2.3 requires `succeeded`."
- Recommendation: either give cli-portify a pre-approval flag in the brief that resolves its approval gates under (b), with D4 governing the authorization, or change AC-2.3 for cli-portify to expect `failed` at the first gate with a named artifact.
- Priority: High. Quality impact: P2 cannot be closed for cli-portify.

### B-8 (BLOCKING). Section 1.4 and E3 contradict each other on the direct-route evidence
- Expert: Karl Wiegers (lead). Severity: MAJOR, blocking (two stated texts contradict).
- Location: candidate:43 (gap 1: "The only end-to-end proof is the PR #329 run, ... so it proves the nested route, not the direct route this spec requires"); candidate:23 (E3 cites `invocation_method: "skill-direct"` at `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:10` as evidence that Orca workers ran `/sc:adversarial` in the earlier run that landed as PR #329); INV-A:13 and INV-A:35 (same contract, "Proven as a direct Orca-worker skill call"). The contract file is outside the workspace, so its content is UNVERIFIED here; the contradiction is between the spec's own sentences.
- Grading check: "Two stated texts contradict: candidate:43 says the only end-to-end proof is nested and no direct-route proof exists, and candidate:23 cites a direct-route (`skill-direct`) contract from that same run as evidence."
- Recommendation: reconcile the two sentences. Either candidate:43 names the skill-direct contract as partial direct-route evidence and says what it does not prove, or candidate:23 drops the citation. Phase 0 tests the direct route either way, so the decision does not change; the evidence statement does.
- Priority: Medium in impact, blocking under the rule because it is a direct contradiction.

---

## === ARCHITECTURE ANALYSIS ===

### B-5 (BLOCKING). The WC-4 contract path is contradicted by the per-command rows, and several commands have no directory to write into
- Expert: Martin Fowler (lead), Sam Newman. Severity: CRITICAL under the blocking rule (the rule and its per-command rows contradict; the coordinator opens a path that does not exist).
- Location: candidate:62 (WC-4: `<output-dir>/return-contract.yaml`, where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)"); candidate:73 (the report path must be known before dispatch); candidate:83 (adversarial: "Fix the contract filename to `<output>/adversarial/return-contract.yaml`"); candidate:87 (init-lite: brief passes `--output <file>`); candidate:90 (tdd: `--output <file>`); candidate:92 (workflow: `.dev/tasks/to-do/<id>/return-contract.yaml`, "Fresh package each run"; the id is generated at run time); candidate:85 (cleanup-audit: "output dir is fixed"); candidate:86 (index-repo: `PROJECT_INDEX.md`, no directory flag); candidate:112 (load: "none"); candidate:116 (research: "contract naming the generated `claudedocs/research_*.md` path", no directory flag in P1 or P2 scope, candidate:159-160); candidate:120 (spec-panel: "add `--output`"; `command.md:23,460` shows `--output <file>` is already file-valued and unattended uses `--report-dir <dir>`).
- Issue: WC-4 defines one fixed rule (a directory from `--output`, containing `return-contract.yaml`). Adversarial's row puts it in a subfolder. Workflow's package id is not known before dispatch, which WC-4 requires. For tdd, init-lite and spec-panel the flag is a file, so WC-4 has no directory. Research, cleanup-audit, index-repo and load have no directory flag at all. WC-4 says the contract is written "including stops before any other output exists", which for workflow means a pre-creation stop has no path.
- Grading check: "An implementer who follows WC-4 writes `return-contract.yaml` directly under the `--output` directory, so for adversarial the coordinator opens `<output>/return-contract.yaml` while candidate:83 places the file at `<output>/adversarial/...`, and for tdd or init-lite the value is a file, so there is no directory to write into; the coordinator then finds no contract and cannot apply WC-5."
- Recommendation: state one contract path per command in section 3, with the directory flag (or an explicit `--contract <path>` flag) and the exact file name. For file-valued commands, name the sibling file. For workflow, pass an explicit package id in the brief so the path is known before dispatch. For research, cleanup-audit, index-repo and load, either add the flag in P1 or mark them not worker-ready. Use the spec-panel evidence in F-29.
- Priority: High. Quality impact: AC-1.2, AC-1.4, AC-2.2 and AC-2.3 cannot be run for at least eight commands, and the coordinator cannot read their outcome from disk.

---

## Follow-up candidates (Medium and minor; not blocking)

These are listed for the coordinator's once-per-loop question. None is blocking, none fails the review, and no issue is created. Medium items that depend on an undefined input are graded Medium under the grading check.

### Acceptance-check defects (Adzic)

- F-1 (Medium). AC-C5 misses removed lines that begin with `--`. Location: candidate:176 (`git diff -U0 master...HEAD -- <file> | grep -E '^-[^-]'`). Tested in this run with `grep -E '^-[^-]'`: the removed lines `-- item` (a deleted markdown bullet) and `--- frontmatter` do not match; `-| table row |` and `-Removed prose` do. Consequence: SA-4 ("edits are additive") passes when a bullet or a horizontal rule is deleted. Recommendation: `git diff -U0 master...HEAD -- <file> | grep -E '^-' | grep -vE '^--- (a/|/dev/null)'`, plus a positive control. Quality impact: a false pass on the additive rule.
- F-2 (Medium). AC-C1 cannot be run verbatim. Location: candidate:172. The raw table cell escapes the pipes (`\|`). Tested in this run: `grep -E '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b'` matches nothing for the input `orca orchestration ask`, which is a positive case; with unescaped `|` it matches. So copied verbatim the check is always empty, and the outer `\| grep -v` is read by the shell as arguments. Recommendation: put the command in a fenced block with unescaped alternation and a positive control (the command must print a match on a known bad line).
- F-3 (Medium). The common and P0 checks do not cover everything the phases change. Location: candidate:173 (AC-C2 `make verify-sync`), :174 (AC-C3 runs `tests/skills/` only), :192 (AC-0.2 relies on "the level-table test the repo already runs"), :279 (UNVERIFIED #8: the plugin mirror `plugins/superclaude/commands/` update rule was not read). No check covers `plugins/superclaude/commands/` or the `src/superclaude/core/CLAUDE.md` level-table test. Recommendation: name these in AC-C2 and AC-C3, or add a check that they match their sources.
- F-4 (Medium). Where a new flag goes is unstated. Location: candidate:149 (SA-4: new flags are additive) and the "Add `--output`" rows at candidate:99-125; AC-C5 (candidate:176) fails when a flag is added to an existing Usage line. Recommendation: state that new flags are added on a new line or a new section, or narrow AC-C5 to deleted lines.
- F-5 (Medium). Required flags for the happy path are undefined. Location: candidate:73 ("every flag section 3 lists as required"); candidate:97 (the 3.2 table has no required-flag column); candidate:201 (AC-2.3 "every required flag in the brief"); candidate:104 ("the safety flags", never named). Recommendation: add a "Brief must pass" column to 3.2 and name cli-eval's safety flags.
- F-6 (Medium). AC-2.2 relies on `blocked_question`, which step 4 does not assert. Location: candidate:200, :183. Recommendation: add `assert d.get('blocked_question')` to step 4 when status is `blocked`.
- F-7 (Medium). Step 2 may fail a legitimate worker. Location: candidate:181 (step 2: `observation.agentWait` never non-null); candidate:61 (WC-3: a worker may block in `ask`). Evidence: CAPS:52 and CAPS:129 say `agentWait` means a prompt only a human can answer; whether an `ask` sets it is UNVERIFIED (CAPS:68 and the UNVERIFIED list). Recommendation: state whether an open `ask` sets `agentWait`; exclude it from step 2 if it does.
- F-8 (Medium). Step 3 and step 5 do not say how to finish. Location: candidate:182 (the loop "until `worker_done` arrives" does not say how to answer a `question`); candidate:184 (step 5 does not say to read every page; `worker-read` has `--limit` and `--cursor`, CAPS:131). Recommendation: say to answer each `question` with `reply` and to read all pages.
- F-9 (Medium). Step 6 and P0 runs have no output directory. Location: candidate:185 ("the brief's output directory", "the command's documented artifacts"); candidate:194 (troubleshoot and workflow runs have no `--output`). Recommendation: name the expected default directories for the P0 runs.
- F-10 (Medium). Some outward and timing checks cannot show what they claim. Location: candidate:209 (AC-4.2 says "no install", but it checks only `git log -1` and PR listing, and installs leave no git trace); candidate:210 (AC-4.3 "heartbeats ... at most 5 minutes apart" has no measurement method); candidate:207 (AC-3.4 two per-session files named `<key>-<session-or-timestamp>.md`, candidate:119; two workers in the same second can collide). Recommendation: add an install-log check, a heartbeat timestamp source, and a session id in the name.
- F-11 (Medium). Standalone behaviour is only partly tested. Location: candidate:146 and :148 (SA-1 and SA-3 say "exactly today's behaviour" and "writes the same files it writes today"); candidate:197 (AC-1.3 checks only that one file is absent); candidate:203 (AC-2.5 is manual). Recommendation: snapshot the set of files a standalone run writes before and after.
- F-12 (Medium). AC-3.2 depends on an undefined flag and an unfinished reconciliation. Location: candidate:205 (`/sc:roadmap ... --output <dir>`), candidate:118 (roadmap row: "reconcile the command's `--resume` ... with the skill's `.session-memory.md`"). Recommendation: name the roadmap directory flag and the chosen resume mechanism.

### Requirements (Wiegers, Cockburn)

- F-13 (Medium). "Well inside the readiness limit" has no number. Location: candidate:59 (WC-1). Evidence: CAPS:49 quotes a 30 s fallback that passed and a 45 s limit that failed. Guard row G-1 below. Recommendation: give the fallback value (for example 30 s) and the margin.
- F-14 (Medium). `partial` settles as `succeeded`, and dependents can start on it. Location: candidate:63 (WC-5 "including `partial`"); candidate:263 (decision row); CAPS:88-90 (a dependent Task unblocks after its prerequisite settles completed; the coordinator starts it). Candidate:73 does not require the coordinator to read the contract before starting dependents. Recommendation: require the coordinator to read `status` before starting any dependent of a `partial` Task, or make `partial` settle as `failed` for dependents.
- F-15 (Medium). The blocked rerun path is unstated. Location: candidate:61 (WC-3: re-invoke or resume with the answer as a flag); candidate:64 (WC-6: a command without a resume flag writes "a fresh output directory", and nothing says who creates it); candidate:73 (2.3 has no re-dispatch step). Evidence: CAPS:116-122 (the breaker counts failed `worker-start` attempts across `--retry-of`, not a worker's own `failed` report, CAPS:80; so a blocked re-run that starts cleanly never trips it). Whittaker attacks W-1 and W-4 below. Recommendation: say that the coordinator reads the contract before any re-dispatch, that the retry gets a new directory, and how many blocked settlements are allowed before escalation.
- F-16 (Medium). init-lite's re-run overwrites its report, which WC-6 does not allow. Location: candidate:87 (Resume column: "Re-run overwrites its marked report"); candidate:64 (WC-6: either a resume flag or a fresh directory). Recommendation: give init-lite a fresh directory, or add the overwrite to WC-6 and say the first attempt's report is lost.
- F-17 (Medium). Fixed output paths break WC-11. Location: candidate:69 (WC-11: default output paths carry a timestamp or slug); candidate:85 (cleanup-audit fixed directory, "one audit per worktree at a time"); candidate:86 (index-repo writes `PROJECT_INDEX.md`); candidate:87 (init-lite fixed report). Recommendation: state that these three commands are coordinator-serialized (one worker per worktree at a time) in the brief rule, or give each a slug.
- F-18 (Medium). The phase plan says Phases 1-3 need no user decision, but P2 includes the outward defaults of auggie-review (PR posting) and task (commit and push) that depend on D4. Location: candidate:160 (P2 note), :245-247 (D4 options). This is consistent only if D4 option (a) is taken. Recommendation: say that P2 is conditional on D4 (a) for the auggie-review and task outward flags.

### Architecture (Newman, Hohpe, Nygard, Fowler)

- F-21 (Medium, Nygard). The heartbeat rule does not cover long Agent-tool calls. Location: candidate:68 (WC-10 splits only Bash waits); candidate:91 (troubleshoot fans out inside a worker); INV-A:35 (adversarial fan-out), INV-B:47 and :49 (tdd and troubleshoot fan-out). A worker blocked in one Agent call for more than five minutes sends no heartbeat, and whether heartbeat age feeds liveness is UNVERIFIED (CAPS:130). Recommendation: require the worker to heartbeat between Agent-tool results, or state that Agent-tool fan-out is exempt and why that is safe.
- F-22 (Medium, Newman). The tasklist nesting claim is unproven. Location: candidate:122 ("its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit"). The chain is worker, then Stage 10.5 subagents, then reflect agents, then Tier 2 reviewers and adversarial agents. INV-B:46 says nesting is UNVERIFIED. Recommendation: count the depth for tasklist and show it is below the limit, or run Stage 10.5 at the top level.
- F-23 (Medium, Newman). The contract has no version field, and installed commands and the installed contract can come from different versions. Location: candidate:62 (fields are "at least" the listed set); candidate:52 (the contract is installed by `KNOWN_CORE_FILES`). Recommendation: add `contract_version`, and have each Unattended section name the version it expects.
- F-24 (Medium, Hohpe). Lost responses to a mutation are not covered. Location: candidate:63 (`worker_done` exactly once); candidate:61 (`ask` resumes by message ID). Evidence: CAPS:117 (`--retry-request` makes a mutation idempotent). Recommendation: say that `worker_done` is sent with `--retry-request` and what the worker does when the response is lost.
- F-25 (Medium, Fowler). Gate logic is repeated in each of 27 commands, and AC-2.1 tests text, not behaviour. Location: candidate:99-125 (per-command gate rules); candidate:199 (AC-2.1: "one assertion per gate ... names both `--no-post-pr` and `--no-remediation-offer`"). A test can pass with the text present and the gate still active. Recommendation: name the gate-resolution mechanism once (shared section pattern) and add one behavioural test per gate.
- F-26 (Medium, Nygard). No coordinator-loss rule. Location: candidate:73 (2.3 describes the coordinator's steps but not its loss). Evidence: Orca's recovery rules for reclaimable workers exist (CAPS:111-116). Recommendation: add a coordinator-restart paragraph that points to `worker-list --terminal-state reclaimable` before any re-dispatch.
- F-27 (Medium, Fowler). Blocked and `ask` waits have no stall rule. Location: candidate:61 (WC-3, "On an `ask` timeout it resumes the same message ID"); CAPS:68 (default timeout UNVERIFIED); CAPS:125 ("absence never authorizes stop, retry, or release"). A worker in `ask` with no reply stays dispatched with no rule to end it. Recommendation: give `ask` an explicit timeout in the contract and a coordinator action when it expires.
- F-28 (Medium). The CLAUDE.md primitive check is not in any AC. Location: no AC in candidate:170-210 runs the `grep -rn 'src/superclaude'` check that CLAUDE.md requires for a new or edited primitive (CLAUDE.md, UNVERIFIED here). Recommendation: add that check to AC-C1 or to AC-1.1.

### Evidence and stale facts

- F-29 (Medium). Spec-panel evidence is out of date. Location: candidate:120 and INV-B:182 say spec-panel has no `--output` flag; `command.md:22-23` lists `[--output <file>] [--unattended] [--report-dir <dir>]`; `command.md:459-463` gives its unattended contract and says "(`--output` is file-valued)" (`command.md:460`). `command.md:461` also cites "WC-4" for a rule about git-ignored artifacts, which is not the spec's WC-4 (candidate:62); the two numbers will collide in cross-references. Recommendation: rewrite the spec-panel row from `command.md` and rename the flag in WC-4 (see B-5).
- F-30 (Medium, Whittaker W-3). reflect's headless auto-accept boundary is not restated. Location: candidate:88. When the remediation set mixes auto-fixable and needs-decision items, the spec does not say whether the worker proceeds on all of them or stops. Recommendation: state the boundary in reflect's Unattended section (the rule itself is in remediation-handoff.md, UNVERIFIED here).

---

## Adversarial analysis (Whittaker, FR-3 template)

- W-1 (Sequence attack, Medium). I can break this specification by **Sequence Attack**. The invariant at **candidate:61-64 (WC-3, WC-6)** fails when **a coordinator re-dispatches a blocked worker with the same `--output` and an answer flag**. Concrete attack: (1) worker A reaches a gate, writes `status: blocked` and `blocked_question` into `<dir>/return-contract.yaml`, and settles `failed`; (2) the coordinator, which candidate:73 does not require to read the contract first, starts worker B with the same brief plus the answer; (3) B writes the same path, so A's `blocked_question` and status are lost. WC-6 forbids corruption but no rule makes the coordinator read or copy the first contract. Severity: MAJOR (ambiguous under attack). Finding: F-15.
- W-2 (Sentinel collision, Medium). I can break this specification by **Sentinel Collision Attack**. The invariant at **candidate:63 (WC-5)** fails when **a contract says `partial` while Orca receives `succeeded`**. Concrete attack: (1) worker writes `status: partial` (usable deliverable, one required section missing); (2) WC-5 sends `--outcome succeeded`; (3) Orca settles the Task `completed`, and CAPS:88-90 unblock its dependents; (4) the dependent consumes the incomplete deliverable. The spec distinguishes `partial` from `succeeded` only in the body and the contract. Severity: MAJOR. Finding: F-14.
- W-3 (Divergence attack, Medium). I can break this specification by **Divergence Attack**. The invariant at **candidate:88 (reflect `--remediate` under `--unattended`)** fails when **the remediation set contains both auto-fixable items and items that need a human decision**. Concrete attack: reflect follows "the existing headless auto-accept rule" (candidate:88), which the spec does not restate; the worker either auto-accepts all items (including the human-decision ones) or stops on the first (the outcome is then unspecified). The branch is decided by a rule the spec defers to `remediation-handoff.md`, which is UNVERIFIED here. Severity: MAJOR as written; graded Medium as F-30.
- W-4 (Accumulation attack, Medium). I can break this specification by **Accumulation Attack**. The invariant at **candidate:61 and :64 (WC-3, WC-6)** fails when **a coordinator re-dispatches one blocked worker without limit**. Concrete attack: a blocked tdd Task is re-run 20 times with `--retry-of`; each run starts cleanly and settles `failed` with a blocked contract. The breaker counts failed `worker-start` attempts, not a worker's own `failed` report (CAPS:80, CAPS:120-122), so it never trips, and nothing in the spec caps the loop. Severity: MAJOR. Finding: F-15.
- W-5 (Sequence attack, Medium). I can break this specification by **Sequence Attack**. The invariant at **candidate:61 (WC-3, `ask` resumes by message ID)** fails when **the coordinator stops answering while the worker waits in `ask`**. Concrete attack: the worker waits in `ask`; the timeout leaves the question pending (CAPS:60); the default timeout is UNVERIFIED (CAPS:68); absence never authorizes stop (CAPS:125); no rule in the spec ends the wait. Severity: MAJOR. Finding: F-27.

---

## Guard Condition Boundary Table (hard gate; triggered by candidate:59-70, :121, :172-176)

Input classes: rows are the classes that apply. Classes left out, with reasons: "Sentinel value match" is covered where a flag or status value is a sentinel (WC-5, AC-C5); "Maximum/overflow" is covered by the circuit breaker row because the spec has no counter other than retries; "One/minimal" is covered by the WC-2 row. Blank Specified Behavior cells: none (FR-9 satisfied). GAP rows are graded under FR-8 and the grading check; the blocking ones are the B-n findings they cite.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-1 fallback timer | candidate:59 | Typical | fallback at 30 s, limit 60 s | fallback fires | "well inside the readiness limit", no number | GAP (F-13) |
| WC-1 fallback timer | candidate:59 | Maximum | fallback at 55 s | fires in time | unspecified whether 55 s is "well inside" | GAP (F-13) |
| WC-2 gate resolution | candidate:60 | Zero/Empty (no default, no flag) | none | blocked (c) | write contract `blocked`, stop | OK |
| WC-2 gate resolution | candidate:60 | Default present | (a) default | not blocked | documented default applies | OK for the rule; conflicts with AC-2.2 (B-6) |
| WC-4 contract path | candidate:62 | Zero/Empty | `--output` absent (research, workflow, cleanup-audit, load) | no directory | write on every outcome, but no directory exists | GAP (B-5) |
| WC-4 contract path | candidate:62, :90, :87 | Shape | `--output <file>` (tdd, init-lite) | a file, not a directory | WC-4 needs a directory | GAP (B-5) |
| WC-4 contract path | candidate:62, :83 | Typical | adversarial `<output>` | path differs | WC-4 says `<output-dir>/...`; row says `<output>/adversarial/...` | GAP (B-5) |
| WC-5 outcome | candidate:63 | Legitimate edge | status `partial` | `succeeded` sent | dependents unblock; not stated | GAP (F-14) |
| WC-5 outcome | candidate:63 | Zero/Empty | no report file | `failed` sent | defined | OK |
| WC-6 retry | candidate:64 | Typical | `--retry-of` with the same output directory, no resume flag | new run overwrites | fresh directory required; who creates it unstated | GAP (F-15, W-1) |
| WC-10 wait | candidate:68 | Maximum | one Agent-tool call of 5 min or more | no heartbeat | splitting covers Bash waits only | GAP (F-21) |
| WC-10 wait | candidate:68 | Typical | Bash poll of 4 min | no split needed | defined | OK |
| Re-dispatch cap | candidate:61, :64; CAPS:116-122 | Maximum | repeated blocked settlements of one Task | no breaker trip (CAPS:80) | no cap stated | GAP (F-15, W-4) |
| Confidence gate | candidate:121 | Boundary | 0.70 and 0.69 | 0.70 proceeds; 0.69 blocked | "below 0.70" stated; source UNVERIFIED | OK |
| AC-C5 additive test | candidate:176 | Sentinel | removed line `- item` (diff `-- item`) | not matched | must fail as a deletion | GAP (F-1) |
| AC-C1 pattern | candidate:172 | Typical | positive control pasted verbatim | no match | must match | GAP (F-2) |
| 7.2 step 2 | candidate:181 | Sentinel | worker in `ask` | `agentWait` unknown | step fails on non-null | GAP (F-7) |

---

## Acceptance criteria and live-check steps, one by one

Each line states whether the item can pass as written for every command and phase it covers. "Yes" means it can; "Partly" means it can for some commands; "No" means it cannot, and the finding is listed.

| Item | Candidate line | Can pass as written? | Finding |
|---|---|---|---|
| AC-C1 | :172 | No (B-1 for core files; F-2 for verbatim copy) | B-1, F-2 |
| AC-C2 | :173 | Yes for the sync it checks; plugin mirror not covered | F-3 |
| AC-C3 | :174 | Yes as an executable check; scope is `tests/skills/` only | F-3 |
| AC-C4 | :175 | Yes (passes trivially when nothing is staged) | none |
| AC-C5 | :176 | Partly: false pass on removed `--` lines; a flag on an existing Usage line fails it | F-1, F-4 |
| AC-0.1 | :191 | Yes | none |
| AC-0.2 | :192 | Yes for HOW-WE-WORK; level-table test not named | F-3 |
| AC-0.3 | :193 | Yes; mirror not checked | F-3 |
| AC-0.4 | :194 | No (P0 cannot pass steps 1, 3, 4) | B-2 |
| 7.2 step 1 | :180 | No in P0 (brief needs `--unattended`); Yes in P1-P4 | B-2 |
| 7.2 step 2 | :181 | Partly (a legitimate `ask` may trip it) | F-7 |
| 7.2 step 3 | :182 | No in P0 (WC-4 path); Partly in P1-P4 (path undefined for file-valued and no-directory commands) | B-2, B-5, F-8 |
| 7.2 step 4 | :183 | No in P0; Partly in P1-P4 (no `blocked_question` check; path per B-5) | B-2, B-5, F-6 |
| 7.2 step 5 | :184 | No (matches the contract text and any gate description) | B-3, F-8 |
| 7.2 step 6 | :185 | Partly (artifacts undefined for P0 runs with no `--output`) | F-9 |
| 7.2 step 7 | :186 | Yes (the `--run` id source is unstated; minor) | note N-1 |
| AC-1.1 | :195 | No (brainstorm and init-lite have no flag or section under :79) | B-4 |
| AC-1.2 | :196 | No for load, cleanup-audit, index-repo, workflow (no output flag in the spec) and init-lite (file-valued); Yes for analyze, build, business-panel, design, document, explain, index, test, adversarial | B-5, B-4 |
| AC-1.3 | :197 | Yes (checks one file only) | F-11 |
| AC-1.4 | :198 | No for workflow (pre-creation STOP has no path) | B-5 |
| AC-2.1 | :199 | Yes (text assertions; behaviour not tested) | F-25 |
| AC-2.2 | :200 | No (B-6 for six commands; B-5 for tdd `--output <file>`; no blocked_question check) | B-6, B-5, F-6 |
| AC-2.3 | :201 | No for cli-portify (B-7); Partly for the rest (required flags undefined) | B-7, F-5 |
| AC-2.4 | :202 | Yes (checks posting only; the offer is not counted) | none |
| AC-2.5 | :203 | Yes as a manual check; not automatable | none |
| AC-3.1 | :204 | Yes (either option in the "or" passes) | none |
| AC-3.2 | :205 | Partly (roadmap output flag and resume design unfixed) | F-12 |
| AC-3.3 | :206 | Yes (either target fix passes) | none |
| AC-3.4 | :207 | Partly (same-second collision; per-session naming) | F-10 |
| AC-4.1 | :208 | Yes (both D2 options end `failed` with a ledger halt) | none |
| AC-4.2 | :209 | Partly (no install check) | F-10 |
| AC-4.3 | :210 | Partly (heartbeat measurement undefined; conditional on D3) | F-10 |

Note N-1 (minor). Step 7 uses `--run <run_id>`, and the spec does not say where the run id comes from. Note N-2 (minor). The spec's own UNVERIFIED #14 (candidate:285) says a fresh evidence-validator re-read about 340 citations; that check is not reproducible here (its files are outside the workspace).

---

## Expert panel summary

- Requirements: Wiegers finds B-1, B-4, B-6, B-8 and F-5, F-12, F-18. Adzic finds B-2, B-3, B-7 and F-1 to F-12. Cockburn: the actor for the blocked path (the coordinator) is not named in WC-2 or WC-3 (candidate:60-61); follow-up under F-15.
- Architecture: Fowler finds B-5, F-4, F-25, F-27. Newman finds F-22, F-23. Hohpe finds F-24. Nygard finds F-21, F-26, and his note on F-27.
- Adversarial (Whittaker): W-1 to W-5, mapped to F-14, F-15, F-27.
- Quality metrics are not scored in critique mode.

## Pipeline and mandatory artifacts

- Guard Condition Boundary Table: produced above (hard gate met for all guards listed; GAP rows graded).
- Pipeline Dimensional Analysis: not triggered (no count-changing multi-stage data flow).
- Quantity Flow Diagram: not triggered.
- State Variable Registry: not triggered.

## Grading record for the blocking findings

Every blocking finding carries its grading sentence above (B-1 to B-8). Each one holds from the stated text with no added assumption: contradictions between two stated texts (B-1, B-4, B-8), an AC whose stated outcome is contradicted by its own rows (B-6, B-7), and a check that fails on a conforming worker (B-2, B-3, B-5).

## Reviser brief

Blocking finding ids: B-1, B-2, B-3, B-4, B-5, B-6, B-7, B-8.

Restated rule (`command.md:263`): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not part of this brief (`command.md:259`, `:264`).

verdict: FAIL
