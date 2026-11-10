review: 1 of 3

# /sc:spec-panel critique, round 1: Orca worker-contract spec

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: not applicable (first review; neither `--re-review` nor `--baseline` given)
- reviewer model actually used: claude-sonnet-5-5
- review_date: 2026-11-10
- mode: critique; focus: requirements, architecture (Whittaker active in every panel)
- format: standard layout in markdown, grouped by analysis bucket
- review panel: `superclaude review panel resolve` and `superclaude review merge` were not run (the sandbox has no loop id or ledger). One reviewer, as the fallback in the prompts file allows.
- brief clauses overridden: none.

Citation shorthand: `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = line N of `.dev/orca-command-refactor/README.md`. `cmdmd:N` = line N of the `command.md` I act as (context only; not graded as evidence about the candidate).

## Coverage (what was and was not checked)

Covered: the whole candidate, sections 1-9, Decisions and the UNVERIFIED list. Every `INV-A:`, `INV-B:` and `CAPS:` citation in sections 1, 2 and 4 and in the "Evidence" column of every row of sections 3.1 and 3.2 was resolved against the inventory files. Each pointed at the intended row or bullet and I found no wrong line. The command counts reconcile: 21 + 22 = 43; 10 + 27 + 6 = 43; phase assignment 13 (P1) + 15 (P2) + 4 (P3) + 3 (P4) + 2 (no change) = 37 workers (spec:76-125, spec:156-162).

Not covered, therefore UNVERIFIED: every citation into `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `.dev/codegraph-migration/...` and `.dev/evals/.../EVIDENCE.md` (not in the workspace; EVIDENCE.md lines are only checkable through the quotes in CAPS:49). That includes the 11 "re-read" locations at spec:11, the grep results at spec:25 and the claim that the pr-submit skill's top-level rule sits at `sk/sc-pr-submit-protocol/SKILL.md:37-39`. I did not run `superclaude` or any Orca command.

Panel coverage: Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Newman, Hohpe (architecture); Whittaker (adversarial). Crispin, Gregory and Hightower are outside both focus areas; their testing concerns are raised only where Adzic or Wiegers reach them (F10).

Advisory: the spec has numeric thresholds (60 s, 5 min, 4 min, 0.70) and a staged pipeline, so the panel recommends re-running one later review with `--focus correctness`. This is a suggestion only.

## What the spec gets right (so the revision does not disturb it)

- The decision "Orca coordinates, commands stay the units of work" is backed by checkable inventory lines: depth 1 (`CAPS:97-103`), standalone failure without Orca (`CAPS:147-149`), `worker_done` bound to the dispatched pane (`CAPS:76,150`).
- Section 1.4 states three evidence gaps plainly (spec:41-45), and Phase 0 smoke runs test the decision before anything else is built (spec:158).
- Section 4's six coordinator-only commands match the inventory verdicts exactly (INV-A:36,49,50; INV-B:32,42,44).
- The open decisions D1-D5 are self-contained with a recommendation each (spec:224-253).

=== REQUIREMENTS ANALYSIS ===

### F1 - CRITICAL, blocking: Phase 1 scope and AC-1.1 contradict the per-command phase assignment
- Expert: Wiegers (lead), Cockburn; Fowler's count annotation (see Quantity Flow Diagram). Pipeline Dimensional Analysis grades a count mismatch CRITICAL (FR-19).
- Grading sentence: An implementer who follows the stated text as written builds Phase 1 as "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" with a `## Unattended mode` section naming `return-contract.yaml` in each (spec:159, spec:195, anchor texts below). That is 37 commands. Section 3 assigns the same sections and contracts to later phases, and the P1 Commands column lists 13. The implementer therefore cannot satisfy both. If P1 stays at 13, AC-1.1 fails, and "Later phases do not start until the earlier phase's checks in section 7 pass" (spec:154) stops the rollout. If P1 covers all 37, Phase 1 writes contract sections for `implement`, `post-release` and `pr-submit` before the user answers D2-D4 (spec:154 says Phases 1-3 need no user decision; spec:162 says Phase 4 needs them), and it changes `pr-submit` although the recommended D3(a) says "no pr-submit changes in Phase 4" (spec:240) and spec:139 says it is a worker candidate only if D3 is accepted.
- Evidence of the two sides:
  - P1 scope: spec:159. AC-1.1: spec:195, whose second clause says no section-4 command has the section. P1 Commands column: spec:159 (analyze, build, business-panel, design, document, explain, index, test, load, plus fixes to adversarial, cleanup-audit, index-repo, workflow).
  - Row phases: auggie-review, cleanup, cli-eval, cli-portify, improve, recommend, research, review-translation, spec-panel, task, tasklist = P2 (spec:100,103-105,110,115-117,120-122); roadmap, save, validate-roadmap, validate-tests = P3 (spec:118-119,124-125); implement, post-release, pr-submit = P4 (spec:109,113,114). The four 3.1 commands reflect, release-split, tdd, troubleshoot are P2 (spec:88-91, spec:160). brainstorm and init-lite have "None" and no phase (spec:84,87).
  - `load`: its row says report "none (see note)" and "use it as a step inside another worker's brief, not as its own Task" (spec:112), and Decisions say "a report file would be an unrequested addition" (spec:265). AC-1.1 still demands a `## Unattended mode` section that names `return-contract.yaml` for it, and section 3's preface says every changed command gains the section (spec:76). WC-4 then has the section's command write the contract (spec:62).
  - Interim state: a P1 flag accepted by a gated command (cli-eval, task, implement, post-release) while its gate still prompts breaks WC-2 ("Under `--unattended` the command never calls `AskUserQuestion`", spec:60). It is exactly the silent stall the spec exists to prevent (spec:44), and nothing tells the coordinator not to dispatch such a command yet.
- Recommendation: delete the clause "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" from the P1 scope (narrow, do not add), and make each command's `--unattended` flag, section and contract land in the phase its row names. Rewrite AC-1.1 to assert only over the commands whose Phase is P1 (the 13 listed) and keep its "no section-4 command has one" clause. Name `load`, `brainstorm` and `init-lite` as having no section, or say in which phase they get one. Keep `pr-submit` out of every phase until D3 is answered.
- Rationale: one phase table and one acceptance check must describe the same set of commands.
- Priority: High. Quality impact: Consistency +2, Testability +1.

### F2 - MAJOR label, Medium: WC-4 names a directory, but several output flags are files
- Expert: Wiegers, Adzic.
- Issue: WC-4 puts the contract at `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (spec:62). The same spec has the coordinator pass a file for `tdd` ("`--output <file>`", spec:90; the report is "the TDD at `--output`", spec:90, INV-B:222), for `init-lite` (spec:87) and for `spec-panel` ("add `--output`", spec:120; INV-B:182 says the report is a single document). For these there is no `<output-dir>`.
- Why Medium: the implementer must guess between the file's parent folder and a sibling file. With the first reading, two `tdd` workers writing into the same `docs/<domain>/` folder share one contract file, which breaks WC-11 (spec:69). The text never states which reading holds.
- Context, not graded: the command definition I act as already handled this with a separate directory flag, because `--output` is file-valued (cmdmd:460-461).
- Recommendation: state one rule for file-valued output flags, for example "a command whose output flag names a file takes a separate `--report-dir` for the contract". Narrow WC-4's wording to match.
- Priority: Medium. Quality impact: Clarity +1.

### F4 - MAJOR label, Medium: the WC-5 outcome mapping has an unstated "report exists but unusable" state, and the contract carries no verdict
- Expert: Wiegers, Whittaker (zero/empty and sentinel attacks).
- Issue: WC-5 sends `--outcome failed` for `failed`, `blocked` or "no report exists", and `--outcome succeeded` "otherwise, including `partial` and including an audit whose verdict is FAIL" (spec:63). A report file that exists but is empty, truncated by a killed worker, or carries a `status` outside the four values (for example an older command's own vocabulary) falls into "otherwise" and is reported as succeeded. The contract's minimum fields (spec:62) also have no `verdict`, although WC-5 tells the worker to state the verdict and treats FAIL as succeeded; a coordinator reading only the contract cannot branch on a FAIL audit (reflect, spec-panel, validate-roadmap, cli-eval).
- Concrete attack (Whittaker): a worker is killed after creating `return-contract.yaml` with 0 bytes. State before: file absent, Task dispatched. State after: file present, size 0. WC-5 branch "no report exists" is false and `failed`/`blocked` is not read, so the worker sends `succeeded`. Orca marks the Task completed and dependents unblock (`CAPS:88-90`). The 7.2 step 4 check (`test -s`, spec:183) catches this only in a test, not as a worker rule.
- Recommendation: replace "no report exists" with "no valid report exists (missing, empty, unparseable, or `status` not one of the four values)" and add `verdict` (optional) to the minimum fields.
- Priority: Medium. Quality impact: Testability +1.

### F5 - MAJOR label, Medium: AC-0.4 step 3 cannot pass in Phase 0 as written
- Expert: Adzic, Wiegers.
- Issue: AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" (spec:194). Step 3 of 7.2 still requires "its report path is the WC-4 contract path" and an `--outcome` that "matches the contract's status under WC-5" (spec:182). None of the three Phase 0 commands produces a WC-4 file at that point: troubleshoot reports `REPORT.md` (spec:91, INV-B:242), adversarial's contract path is not yet fixed (spec:83) and workflow's contract sits in its package folder (spec:92). A failure at this step "reopens section 1" (spec:194), so a false failure would send the central decision back for review.
- Why Medium: the intent is obvious (apply the step 4 substitution to step 3), but the text names only step 4.
- Recommendation: extend the substitution in AC-0.4 to say "steps 3 and 4 use the command's existing report file and its own status".
- Priority: Medium. Quality impact: Testability +1.

### F7 - MAJOR label, Medium: WC-3 lets the worker ask instead of ending, which AC-2.2 does not allow for
- Expert: Adzic, Nygard.
- Issue: WC-3 says that when a gate would resolve as blocked "the session may instead ask the coordinator once" and wait (spec:61). AC-2.2 passes only with "`worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`" and no `agentWait` (spec:200). A worker that takes the permitted `ask` path sends no `worker_done` and shows a waiting worker (`CAPS:52`, `CAPS:129`), so the gate-trigger check fails on allowed behaviour. The brief template (spec:73) does not say whether `ask` is allowed. "Once" is also undefined for a second gate after the first answer, and an unanswered `ask` waits without a bound ("healthy, not failed", `CAPS:129`).
- Recommendation: make the choice a field of the brief (for example "ask allowed: yes/no") and have AC-2.2 run with "no".
- Priority: Medium. Quality impact: Testability +1.

### F9 - MAJOR label, Medium: WC-9 authorisation switches are undefined for several commands
- Expert: Wiegers, Cockburn.
- Issue: WC-9 says an outward default "turns on only through the command's own explicit flag written in the brief" (spec:67). Several rows rely on that without naming a flag: `task` "EXEMPT `commit`/`push` refused unless authorized (WC-9)" (spec:121; those are keywords in the task text, INV-B:204, not flags); `post-release` "VM, real-target install, commit and PR off unless the brief authorizes them" with no flag (spec:113); AC-4.2 tests "no authorization flags" (spec:209). The term "paid external run" is undefined, and `research`, `review-translation` and `recommend` search the web by default (INV-B:134,144,104), so WC-9 read literally would switch off their core function.
- Why Medium: it is a missing definition, not a text that does harm. Phase 4 and D4 will have to settle it.
- Recommendation: add one sentence to WC-9 listing the commands that have such a flag, and for the others say "refused, no authorising flag exists" until D4 is answered; define "paid external run" or drop it.
- Priority: Medium. Quality impact: Clarity +1.

### F10 - MAJOR label, Medium: several requirements have no acceptance check
- Expert: Adzic (lead), Wiegers.
- Issue: spec:167 says a phase passes when every check in its block passes, but section 7 holds no check for WC-3 (ask path), WC-6 (resume or safe re-run), WC-12 (`check` before `worker_done`, `consumer_fenced`) or WC-1 (launch prompts; only 7.2 step 1 touches it, and the launcher fallback evidence is `EVIDENCE.md:45,56` via CAPS:49). WC-10 is tested only for pr-submit (AC-4.3), not for cli-eval, which has its own WC-10 split (spec:104). WC-11 is tested only for `save` (AC-3.4). SA-1 is tested only by two manual runs (AC-2.5, spec:203) although many skills change; AC-C5 (spec:176) looks at command files only.
- Recommendation: add one check per untested WC, or mark it "not checked in this plan" in section 7; do not add mechanisms.
- Priority: Medium. Quality impact: Testability +2.

### F12 - MAJOR label, Medium: no requirement on tool-permission prompts in a worker
- Expert: Cockburn (the primary actor is a worker with no person), Wiegers.
- Issue: WC-1 and WC-2 cover launch prompts and command gates (spec:59-60). A worker session can also stop on Claude Code's own tool-approval prompt for Bash, Write or `gh`, which stalls exactly like `AskUserQuestion` and shows only as `agentWait` (`CAPS:129`). The inventories mention only Orca's pre-accepted trust prompt (`CAPS:50`). Nothing in section 2 says what permission mode or allowlist a worker runs under, and the live check only detects the stall afterwards (spec:181).
- Why Medium: a requirement the document never states; I could not verify whether Orca's launch already sets a permission mode (UNVERIFIED).
- Recommendation: add one line to section 2.3 (what the coordinator owes) stating the permission mode the brief must ensure, or state that it is out of scope.
- Priority: Medium. Quality impact: Completeness +1.

### F14 - MINOR: unverifiable flag names and a stale "nothing calls Orca" premise
- Expert: Wiegers.
- Issue: the `cli-eval` row requires `--suite` and "the safety flags in the brief" (spec:104), and the `auggie-review` row relies on an explicit `--post-pr` (spec:100). Neither flag appears anywhere in the inventories (only `--no-post-pr`, INV-A:38); the inventories describe a suite menu and safety confirmations without naming a `--suite` flag (INV-A:44). If the flags do not exist, the gate has nothing to key on. Separately, E5 (spec:25) says no command, skill, agent or core file calls Orca "today" from a grep dated 2026-11-02. The skill list visible to this review session names `sc:issue`, `sc:graph` and `sc:impact`, which appear in neither inventory, and describes `sc:issue` as creating an Orca worktree. UNVERIFIED either way; the 43-command scope (spec:76) and E5 need a re-check on the current tree.
- Recommendation: mark the flags UNVERIFIED in the rows or define them in the P2 plan; re-run the E5 grep and the command count at the start of Phase 0.
- Priority: Low.

### F17 - MINOR: small notes
- Phase 1 is titled "commands with no gate" (spec:159) but lists `business-panel`, `explain`, `index` and `test`, whose rows each resolve a gate by refusing a mode (spec:102,108,111,123).
- WC-9 and the `/sc:git` row cite `README:31` (spec:67,133), which is a rule for this planning run's workers (README:31), not a product rule; the product reason is the user's authorisation rule, which is not cited in a checkable place.
- Section 3 counts `pr-submit` among the 27 commands that need a change (spec:76) although the recommended D3(a) makes it coordinator or person only (spec:240).

=== ARCHITECTURE ANALYSIS ===

### F3 - MAJOR label, Medium: the adversarial contract path contradicts the WC-4 definition
- Expert: Fowler (lead), Newman.
- Issue: section 3 says "Contract" means the WC-4 file `<output-dir>/return-contract.yaml` (spec:76). The adversarial row fixes it at `<output>/adversarial/return-contract.yaml` (spec:83), because the skill writes its artifacts under `<output>/adversarial/` (INV-A:35). AC-1.4 checks only that adversarial "names one fixed path" (spec:198). A coordinator or worker that derives the path from WC-4 and spec:73 looks one directory too high, finds "no report", and under WC-5 reports `failed` for a successful run.
- Why Medium: the row is the more specific text, so most implementers will follow it, but 7.2 step 4 and the brief template use the generic path.
- Recommendation: state in WC-4 that the contract path is "given per command in section 3" and let the coordinator brief carry the exact path, or write the contract at `<output-dir>/return-contract.yaml` for adversarial as well (narrowing). Add the exception to the section 3 preface.
- Priority: Medium. Quality impact: Consistency +1.

### F6 - MAJOR label, Medium: retry and re-run can overwrite the first attempt, and a stale contract can be read as new
- Expert: Nygard (lead), Whittaker (sequence attack).
- Issue: WC-6 says a retry worker "must not corrupt the first attempt's output" and offers two cases: resume flag given, or no resume flag so a fresh directory (spec:64). It does not cover a command that has a resume flag when the brief omits it, and it does not say who creates the "fresh directory". WC-4 says the contract path is known before dispatch (spec:62), which a command-created fresh directory would break. Rows that start "fresh" in the same directory: AC-3.2 has `roadmap` with an existing `.session-memory.md` and no resume flag "starts fresh" (spec:205), which discards the earlier waves. The same hole exists for tdd, brainstorm, release-split and pr-submit whenever the retry brief omits the flag (spec:83-90,114). The 2.3 template does not make the coordinator pass the resume flag on retry (spec:73).
- Concrete attack (Whittaker): attempt 1 of a `roadmap` Task writes `return-contract.yaml` with `status: succeeded` for an earlier run, or `partial`, then the worker dies. State before: contract present. Retry worker starts in the same directory and crashes before writing. State after: the old contract is still there, WC-5's "no report exists" branch is false, and the coordinator reads a stale `succeeded`. Nothing requires a command to reset or remove the contract at start.
- Recommendation: add to WC-6 one sentence: "a retry brief names either the resume flag or a new output directory chosen by the coordinator", and to WC-4 "the command removes any older contract in its output directory before doing other work". Keep each to one line (no new mechanism beyond what the finding calls for).
- Priority: Medium. Quality impact: Completeness +1.

### F8 - MAJOR label, Medium: section 1.4 point 2 asserts what it cannot show
- Expert: Nygard, Fowler.
- Issue: the spec says a command's own `AskUserQuestion` comes "*after* readiness, so it does not fail `worker-start`" (spec:44). The inventory says that for Claude the task is passed on the command line, not typed (`CAPS:47`), and readiness waits for a fresh input box (`CAPS:47`). A command given as the startup argument starts running before that box may appear, and an `AskUserQuestion` dialog replaces it, so the same readiness failure could occur. The only run evidence is a trivial prompt that was accepted (`CAPS:49`). This is not listed in the UNVERIFIED section (spec:271-285).
- Why Medium: the contract does not depend on the answer, since spec:44 says section 2 covers both cases, so the design survives either way.
- Recommendation: add one line to the UNVERIFIED list and say the Phase 0 smoke run should include a gated command that is expected to block.
- Priority: Medium. Quality impact: Consistency +1.

### F11 - MAJOR label, Medium: WC-11 says "never", but rows accept shared fixed paths
- Expert: Fowler, Whittaker (accumulation attack).
- Issue: WC-11 says "Two workers in one worktree must never write the same file" and that default output paths carry a timestamp or the coordinator's slug (spec:69). Rows accept the opposite: `cleanup-audit` has a fixed output directory, "so one audit per worktree at a time (WC-11)" (spec:85); `index-repo` writes a fixed `PROJECT_INDEX.md` (spec:86, INV-A:53); `reflect` writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` and moves the work-unit folder by default (INV-B:114), which no row or WC-9 addresses. The constraint "one at a time" is placed on the coordinator but does not appear in section 2.3 (spec:73). `save` per-session keys use "`<session-or-timestamp>`" (spec:119, INV-B:165); two workers started in the same second with a timestamp key collide.
- Recommendation: add the one-at-a-time constraint to section 2.3 for the fixed-path commands, and state the timestamp resolution used for `save`.
- Priority: Medium. Quality impact: Consistency +1.

### F13 - MINOR: contract vocabulary, versioning and name collisions
- Expert: Newman, Hohpe.
- Issue: WC-4 says commands with a contract "keep their fields and add the missing ones" (spec:62), while Decisions fix a four-value `status` and reject copying each command's own (spec:262); if an existing contract already uses a `status` word outside the four, both cannot hold (workflow's contract has a `status`, INV-B:272; the values were not inventoried). WC-4 has no version field, so the coordinator cannot detect a changed shape. The contract value `blocked` is also an Orca Task status word with a different meaning (`CAPS:89`), and `partial` is mapped to a completed Task, which unblocks dependents (spec:263, `CAPS:88-90`); both are documented but easy to misread. Context, not graded: the implemented spec-panel section leaves git-ignored paths out of `artifacts` (cmdmd:461), while WC-4 says "every other file written" (spec:62); which one is intended is UNVERIFIED.
- Recommendation: list the existing `status` values per command before P1, add `contract_version`, and say in WC-5 that `blocked` here is not an Orca Task status.
- Priority: Low.

### F15 - MINOR: AC-C1 scope and form
- Expert: Fowler, Hohpe.
- Issue: AC-C1 greps `src/superclaude/core` and expects "prints nothing (SA-2, WC-8)" (spec:172), but SA-2 covers command, skill and agent files and permits an Orca mention in the contract file (spec:147), and Phase 0 adds an Orca section to the core routing guide and a coordinator template (spec:158). A natural coordinator section would contain `orca orchestration ...` and fail the check. In the table the regex is written with `\|` escapes (spec:172); copied as-is into `grep -E` that matches a literal pipe, and the check passes vacuously. The pattern is also lowercase only, while the spec writes `ORCA` for the executable (spec:167).
- Recommendation: restrict AC-C1 to commands, skills and agents, and give the pattern in a code block with a plain `|`.
- Priority: Low.

### F16 - MINOR: wait thresholds differ between WC-10 and AC-4.3
- Expert: Nygard.
- Issue: WC-10 requires splitting only a call that blocks "longer than 5 minutes" into waits "of at most 4 minutes" (spec:68); AC-4.3 fails any "single tool call" over 240 s (spec:210). A call of 270 s obeys WC-10 and fails AC-4.3; at exactly 5 minutes the 5-minute heartbeat is already due. The 5-minute cadence itself is read from one worker preamble, not a guide (spec:68, `CAPS:130`).
- Recommendation: use one number, 4 minutes, in both places.
- Priority: Low.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

Template per finding: I can break this specification by [attack]. The invariant at [location] fails when [condition]. Concrete attack: [trace]. Severity uses the panel scale.

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (spec:63)** fails when **the contract file exists with zero bytes**. Concrete attack: worker killed after file creation; before: no file, after: 0-byte file; WC-5 branch "no report exists" is false and the "otherwise" branch sends `succeeded`. MAJOR (ambiguous under attack) -> F4, graded Medium.
2. I can break this specification by **Sequence Attack**. The invariant at **WC-4/WC-6 (spec:62,64)** fails when **a retry worker crashes before writing, in a directory that holds a previous contract**. Concrete attack: old `status: succeeded` remains; no removal step; coordinator reads it as the retry's result. MAJOR -> F6, graded Medium.
3. I can break this specification by **Divergence Attack**. The invariant at **WC-3 versus AC-2.2 (spec:61,200)** fails when **the worker takes the permitted `ask` path instead of ending**. Concrete attack: gate hit; worker asks; no `worker_done`; AC-2.2 expects `failed` + `blocked`; check fails on allowed behaviour. MAJOR -> F7, graded Medium.
4. I can break this specification by **Accumulation Attack**. The invariant at **WC-11 (spec:69) and the `save` row (spec:119)** fails when **two workers start in the same timestamp unit or two fixed-path commands run in one worktree**. Concrete attack: workers A and B both write `<key>-<same timestamp>.md`; the second write replaces the first. MAJOR -> F11, graded Medium.
5. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4/WC-5 status words (spec:62-63)** fails when **a legacy contract `status` value is outside the four or collides with an Orca Task word**. Concrete attack: an existing command writes `status: complete`; WC-5 treats it as "otherwise", sends `succeeded`; for `blocked` the coordinator may confuse the contract word with Task status. MINOR -> F13.
6. I can break this specification by **Divergence Attack**. The invariant at **P1 scope versus phase column (spec:159 vs spec:99-125)** fails when **the implementer reads the two texts literally**. Concrete attack: P1 completes 13 commands; AC-1.1 asserts 37; check fails; rollout rule at spec:154 stops all later phases. CRITICAL (the specification contradicts itself) -> F1, blocking.

## Guard Condition Boundary Table

Guards identified: GB-1 WC-5 outcome mapping; GB-2 WC-10 wait split; GB-3 WC-6 resume or fresh run; GB-4 WC-3 ask once; GB-5 WC-9 outward default off; GB-6 `task` confidence below 0.70 resolves as blocked; GB-7 WC-11 parallel-safe writes. Construction: Nygard; completeness check: Crispin's rule applied by the panel (the "six classes are a menu" rule); adversarial entries: Whittaker.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| GB-1 WC-5 mapping | spec:63 | Zero/Empty | report file present, 0 bytes or empty `status` | "no report exists" false; failed/blocked false | falls to "otherwise": `succeeded` (not stated as intended) | GAP (F4) |
| GB-1 WC-5 mapping | spec:63 | One/Minimal | report with only `status: succeeded` | otherwise branch | `succeeded`; WC-4 "at least" fields not re-checked by WC-5 | GAP (F4) |
| GB-1 WC-5 mapping | spec:63 | Typical | `status: failed` / `blocked` / `succeeded` | true / true / false | `failed` / `failed` / `succeeded` | OK |
| GB-1 WC-5 mapping | spec:63 | Sentinel Value Match | `status: partial`; or a legacy word such as `complete` | otherwise branch | `partial` -> `succeeded` (stated, spec:263); legacy word -> `succeeded` (not stated) | GAP (F4, F13) |
| GB-1 WC-5 mapping | spec:63 | Legitimate Edge Case | audit verdict FAIL | otherwise branch | `succeeded`, verdict only in the body (stated); no `verdict` field in WC-4 | GAP (F4) |
| GB-2 WC-10 split | spec:68 | Zero/Empty | no blocking call in the step | false | nothing to split | OK |
| GB-2 WC-10 split | spec:68 | Typical | one 3-minute call | false | not split | OK |
| GB-2 WC-10 split | spec:68 | Maximum/Overflow | eval wait up to 3600 s (spec:68, INV-A:65) | true | split into waits of at most 4 minutes | OK |
| GB-2 WC-10 split | spec:68, spec:210 | Legitimate Edge Case | call of 270 s, or exactly 5 minutes | false (not longer than 5 min) | WC-10 allows it; AC-4.3 rejects any call over 240 s; heartbeat due at 5 min | GAP (F16) |
| GB-3 WC-6 resume | spec:64 | Zero/Empty | resume flag given, state file missing or empty | n/a | unspecified | GAP (F6) |
| GB-3 WC-6 resume | spec:64, spec:205 | Typical | flag given with valid state; or no flag and no state | true / false | resumes; fresh start | OK |
| GB-3 WC-6 resume | spec:64, spec:205 | Legitimate Edge Case | command has a resume flag, brief omits it, state exists | false | neither branch of WC-6 applies; AC-3.2 says "starts fresh" in the same directory | GAP (F6) |
| GB-3 WC-6 resume | spec:62, spec:64 | Sentinel Value Match | old `return-contract.yaml` from an earlier attempt | n/a | nothing says it is reset at start | GAP (F6) |
| GB-4 WC-3 ask once | spec:61 | Zero/Empty | coordinator reply has an empty body | n/a | unspecified | GAP (F7) |
| GB-4 WC-3 ask once | spec:61 | Typical | one blocked gate, one answer, command re-invoked with a flag | true | resumes | OK |
| GB-4 WC-3 ask once | spec:61 | Maximum/Overflow | second gate after the first answer; repeated `ask` timeouts | "once" exceeded | unspecified; unanswered `ask` is "healthy" without bound (`CAPS:129`) | GAP (F7) |
| GB-5 WC-9 outward off | spec:67 | Zero/Empty | no authorising flag in the brief | off | off | OK |
| GB-5 WC-9 outward off | spec:67, spec:100 | Typical | explicit `--post-pr` (UNVERIFIED flag) | on | on | OK |
| GB-5 WC-9 outward off | spec:67, spec:113, spec:121 | Legitimate Edge Case | action has no explicit flag (`task` commit/push, `post-release` steps) | n/a | "authorized" with no named switch | GAP (F9) |
| GB-6 task confidence | spec:121, INV-B:199 | Zero/Empty | confidence 0 | below 0.70: true | blocked | OK |
| GB-6 task confidence | spec:121, INV-B:199 | Typical | 0.85 | false | proceeds | OK |
| GB-6 task confidence | spec:121, INV-B:199 | Legitimate Edge Case | exactly 0.70 | false ("below 0.70") | proceeds | OK |
| GB-7 WC-11 writes | spec:69, spec:119 | One/Minimal | two workers, same timestamp unit, same per-session key | true | collision; resolution not stated | GAP (F11) |
| GB-7 WC-11 writes | spec:69, spec:85-86 | Sentinel Value Match | fixed paths (`.claude-audit/`, `PROJECT_INDEX.md`) | true | WC-11 says "never"; rows say "one at a time" | GAP (F11) |
| GB-7 WC-11 writes | spec:69 | Typical | distinct slugs from the brief | false | separate files | OK |

Classes left out, one line each:
- GB-1 Maximum/Overflow: a single scalar status has no accumulation.
- GB-2 One/Minimal and Sentinel: the rule is one threshold on elapsed time; no sentinel value exists.
- GB-3 One/Minimal and Maximum: the rule is a binary flag-or-not decision; no count is involved.
- GB-4 One/Minimal and Sentinel: covered by Typical; the rule has no reserved values.
- GB-5 One/Minimal, Maximum/Overflow, Sentinel: a flag is present or absent; the both-flags case (`--post-pr` with `--no-post-pr`, precedence unstated) is Minor and folded into F9.
- GB-6 One/Minimal, Maximum/Overflow, Sentinel: a numeric threshold; 1.0 behaves as Typical, and EXEMPT-tier tasks skip the skill (INV-B:204).
- GB-7 Zero/Empty and Maximum/Overflow: no counter or collection is involved.

Every GAP row above is graded in the findings (none of them names a security or data-loss risk without a guess, so all are Medium or Minor). The table is complete, so synthesis may proceed.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, FR-17 to FR-21)

Trigger: a staged pipeline in which one stage's output count differs from its input count (classification, then phase assignment, then acceptance checks). Fowler annotated counts; Whittaker attacked the divergence.

```text
[Source: 43 commands (21 INV-A:3 + 22 INV-B:3)] --> [Stage 1: classify, spec:76-139]
      --> [37 worker candidates = 10 ready (spec:81-92) + 27 need a change (spec:97-125)]
      --> [6 coordinator-only (spec:130-137)]  (excluded from the contract)
                                              |
                                              v
                       [Stage 2: assign phase, spec:99-125 and spec:156-162]
                       P1 = 13 (9 from 3.2 + adversarial, cleanup-audit, index-repo, workflow)
                       P2 = 15 (11 from 3.2 + reflect, release-split, tdd, troubleshoot)
                       P3 = 4   P4 = 3   no change = 2 (brainstorm, init-lite)   13+15+4+3+2 = 37
                                              |
                                              v
   [Consumer A: P1 scope (spec:159) and AC-1.1 (spec:195): expects 37]        <-- MISMATCH (Stage 2 gives 13 in P1)
   [Consumer B: AC-1.2 "each P1 command" (spec:196): expects 13]              OK
   [Consumer C: AC-1.1 second clause "no section-4 command": expects 6 out]   OK
   [Consumer D: D3(a) "no pr-submit changes in Phase 4" (spec:240): expects pr-submit out of the 37]  <-- MISMATCH (spec:76 counts it; P1 scope includes it)
```

Severity under FR-19: CRITICAL. It is reported once, as F1.

## Consensus and disagreements

- Consensus: the decision, the section 4 list, the open decisions and the evidence-gap statement are sound; the inventory citations I resolved are accurate. The weak parts are internal consistency of the rollout (F1) and a set of unstated edge states in the contract rules (F2, F4, F6, F7).
- Disagreement (simulated): Fowler would keep one early skeleton section in all 37 commands as a single seam; Wiegers prefers phase-local changes because the skeleton for `implement`, `post-release` and `pr-submit` depends on D2-D4. The recommendation under F1 follows Wiegers because it deletes rather than adds.

## Quality metrics (0-10)

| Dimension | Score | Reason |
|-----------|-------|--------|
| Clarity | 7 | Tables are consistent and each row names its evidence; WC-4's directory wording is the main unclear spot (F2). |
| Completeness | 6 | Edge states of WC-3, WC-5, WC-6, WC-9 are open; permission prompts unaddressed (F12). |
| Testability | 6 | Section 7 is concrete, but WC-3, WC-6, WC-12 are unchecked and two checks conflict with the text (F1, F5, F10). |
| Consistency | 5 | The Phase 1 scope contradicts the phase column and AC-1.1 (F1); smaller conflicts in F3, F11, F16. |

## UNVERIFIED items from this review

1. Every citation into `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `.dev/codegraph-migration/` and `.dev/evals/` (spec:11, spec:25, spec:52, spec:150, spec:164, spec:183 and the "Evidence" cells that cite them).
2. Whether `--suite` and `--post-pr` exist as flags (F14).
3. Whether the current command set still has exactly 43 members and whether any command now calls Orca (F14).
4. Whether Orca's launch sets a worker permission mode (F12).
5. Whether a command passed as the startup argument can fail readiness at its first `AskUserQuestion` (F8).
6. Which `status` words existing contracts use (F13).

## Follow-up candidates (Medium and minor; none triggers a revision)

I could not ask the user whether to open an issue for these (no user channel in this run), so I created none; the list is recorded only.

- Medium: F2 (file-valued output flag vs WC-4 directory), F3 (adversarial contract path), F4 (WC-5 empty/unknown report, no verdict field), F5 (AC-0.4 step 3), F6 (retry overwrite, stale contract), F7 (WC-3 ask vs AC-2.2), F8 (readiness assumption in 1.4), F9 (WC-9 switches undefined), F10 (acceptance traceability), F11 (WC-11 vs fixed paths), F12 (permission prompts).
- Minor: F13 (contract vocabulary and version), F14 (unverified flags, stale E5), F15 (AC-C1 scope and form), F16 (wait thresholds), F17 (small notes).

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)", "anchor2": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`", "refs": ["AC-1.1", "section 6 P1", "section 3.2 Phase column", "D2-D4", "D3(a)"], "claim": "P1 scope and AC-1.1 require the flag, section and contract in all 37 commands while the phase column and P1 command list give P1 only 13, so AC-1.1 cannot pass or P1 pre-empts the D2-D4 decisions."}
{"id": "F2", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", "anchor2": "a precise component prompt, not a bare topic; `--output <file>`", "refs": ["WC-4", "WC-11", "section 3.1 tdd"], "claim": "WC-4 places the contract in a directory but tdd, init-lite and spec-panel take a file as output, so the contract location is a guess and two workers can share one file."}
{"id": "F3", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)", "anchor2": "means the WC-4 file `<output-dir>/return-contract.yaml`", "refs": ["WC-4", "AC-1.4", "section 3.1 adversarial"], "claim": "A worker or coordinator that derives the adversarial contract path from WC-4 looks one directory too high and reports a successful run as failed."}
{"id": "F4", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "`--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL", "refs": ["WC-5", "WC-4"], "claim": "An empty, truncated or unknown-status contract falls into the otherwise branch and is reported succeeded, and the contract has no verdict field for FAIL audits."}
{"id": "F5", "severity": "MAJOR", "blocking": false, "category": "unpassable-check", "anchor": "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1", "anchor2": "its report path is the WC-4 contract path", "refs": ["AC-0.4", "7.2 step 3"], "claim": "In Phase 0 step 3 still demands a WC-4 contract path that none of the three smoke commands writes, and a failure there reopens section 1."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output.", "anchor2": "starts fresh, no `[Y/n]` in the transcript, contract written", "refs": ["WC-6", "WC-4", "AC-3.2"], "claim": "A retry in the same directory without a resume flag starts fresh over the earlier output, and an old contract that is never reset can be read as the retry's result."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "the session may instead ask the coordinator once with the preamble's `ask` command", "anchor2": "`worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`", "refs": ["WC-3", "AC-2.2", "section 2.3"], "claim": "A worker that takes the permitted ask path sends no worker_done, so AC-2.2 fails on allowed behaviour, and the limit 'once' is undefined."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "A command's own `AskUserQuestion` or chat question comes *after* readiness, so it does not fail `worker-start`", "refs": ["section 1.4", "CAPS:47", "CAPS:49"], "claim": "The claim is asserted although the task is passed as a startup argument, and it is missing from the UNVERIFIED list."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "It turns on only through the command's own explicit flag written in the brief.", "anchor2": "EXEMPT `commit`/`push` refused unless authorized (WC-9)", "refs": ["WC-9", "AC-4.2", "D4"], "claim": "Several rows rely on an authorising flag that does not exist, and 'paid external run' is undefined, so WC-9 cannot be applied as written."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "A phase passes only when every check in its block and every common check passes.", "refs": ["section 7", "WC-1", "WC-3", "WC-6", "WC-12", "SA-1"], "claim": "WC-1, WC-3, WC-6 and WC-12 have no acceptance check, and WC-10, WC-11 and SA-1 are checked for one or two commands only."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "Two workers in one worktree must never write the same file.", "anchor2": "output dir is fixed, so one audit per worktree at a time (WC-11)", "refs": ["WC-11", "section 2.3", "section 3.1", "section 3.2 save"], "claim": "WC-11 forbids shared files while rows accept fixed paths and timestamp keys, and the one-at-a-time constraint is missing from what the coordinator owes."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Nothing in the launch path (wrapper, hook, startup command) may wait on a person before Claude's input box is ready.", "refs": ["WC-1", "WC-2", "CAPS:129"], "claim": "No requirement covers the worker's own tool-permission prompts, which stall like AskUserQuestion and show only as agentWait."}
{"id": "F13", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Commands that already write a contract keep their fields and add the missing ones.", "anchor2": "mapped to Orca's two outcomes in WC-5", "refs": ["WC-4", "WC-5"], "claim": "Existing status words may conflict with the fixed four-value set, there is no contract version, and blocked shares a word with Orca's Task status."}
{"id": "F14", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "`run` requires `--suite` and the safety flags in the brief, else blocked", "anchor2": "posting returns only with an explicit `--post-pr` in the brief", "refs": ["section 3.2 cli-eval", "section 3.2 auggie-review", "E5"], "claim": "The --suite and --post-pr flags are not shown to exist in the inventories, and the no-command-calls-Orca premise and the 43-command scope need a re-check."}
{"id": "F15", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "prints nothing (SA-2, WC-8)", "anchor2": "add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies", "refs": ["AC-C1", "SA-2", "P0"], "claim": "AC-C1 scans core files that Phase 0 must fill with Orca text, and its escaped pipes make the grep pattern match nothing when copied."}
{"id": "F16", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "must be split into waits of at most 4 minutes so the session can heartbeat between them", "anchor2": "no single tool call exceeds 240 s", "refs": ["WC-10", "AC-4.3"], "claim": "A 270 s call obeys WC-10 and fails AC-4.3."}
{"id": "F17", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "P1. Report files and commands with no gate", "anchor2": "per-command outward actions in column (f) of the inventories", "refs": ["section 6", "WC-9", "section 4"], "claim": "P1 is labelled no-gate yet lists commands that refuse a mode, and run-scoped README rule 31 is cited as a product reason."}
```

Reviser brief: blocking finding ids: F1. Revise only text that F1 names. Add no rule, mechanism or section that no blocking finding calls for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size of the candidate before and after, with the bytes added and deleted per finding id. Leave minor and Medium findings (F2-F17) alone; they never trigger a revision. Do not award yourself a PASS.

verdict: FAIL
