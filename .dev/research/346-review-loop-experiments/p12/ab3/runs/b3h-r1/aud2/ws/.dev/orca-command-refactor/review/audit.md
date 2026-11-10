review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines, sha256 `060d1fb59804955f83e92638dceec3c2655f94b7c59c399f7112f8a8c9bfd1d2`
- Baseline: none given (first review of the full document; this is not a re-review)
- Reviewer model actually used: claude-sonnet-5-5
- Brief clauses overridden: none
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full)
- Citation key: `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`. Every `src/...`, `~/.claude/...`, `CLAUDE.md` and `EVIDENCE.md` line the spec cites directly is UNVERIFIED here (no such file is in the sandbox). Where I rely on one, I take it through the inventory line that quotes it.

## Coverage
Read in full: the command definition, the review-loop prompts file, the README, the candidate (S:1-285), and all three inventories (INV-A 1-120, INV-B 1-323, CAPS 1-188).

Checked:
- Every `INV-*`/`CAPS:` cross-reference in S:19-70 and S:128-139 against the inventory lines.
- The 10/27/6 split and the per-phase command lists (S:76, S:158-162) against the two inventories' verdicts.
- Each WC requirement against the section 3 rows and the section 7 acceptance checks.
- The standalone-use rules SA-1 to SA-6 against the phase table.

Not checked (UNVERIFIED):
- Any path:line into `src/superclaude/**`, `CLAUDE.md`, `HOW-WE-WORK.md`, `EVIDENCE.md`, the codegraph-migration files and Orca's installed JS.
- Nothing was run (no Orca, no repo).

Scope of this audit: requirements and architecture. Testing, compliance and correctness focus areas were not requested. The State Variable Registry (correctness-only) is therefore not produced. The Guard Condition Boundary Table and the Quantity Flow Diagram are produced because the spec contains threshold guards and a counted multi-stage flow.

## Panel (review sequence, focus-selected)
Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Whittaker (adversarial, always active), Newman, Hohpe. Crispin and Gregory contribute only to the Guard Condition Boundary Table completeness check.

## Grading statement
No CRITICAL finding and no other blocking finding is open. Each finding below passed the grading check: "An implementer who follows the stated text as written builds X, and X is wrong because Y." Every one of them needs either a guess about which of two allowed readings the implementer picks, or is a requirement the document never states. They are therefore Medium (warnings) or minor, and all sit under `follow-up candidates`. Labels in the expert text (MAJOR) do not change that.

---

=== REQUIREMENTS ANALYSIS ===

### Overall assessment (Wiegers, Adzic, Cockburn)
The spec states one decision, gives evidence for it, and states its own evidence gaps plainly (S:41-45). It lists 12 requirements with owner and evidence (S:57-70). It assigns every worker-capable command a row (S:81-125). It gives numbered acceptance checks (S:167-210) and puts the open decisions to the user with recommendations (S:224-253). The counts reconcile: 21 + 22 = 43, and 10 + 27 + 6 = 43 (S:76) against INV-A:73 (5/13/3) and INV-B:278 (5/14/3). The cross-references I could check against the inventories all land on the cited lines (for example S:21 to CAPS:92, S:33 to CAPS:97-103, S:34 to CAPS:147-149, S:37 to INV-A:90 and INV-B:285-286).

The findings are about places where a requirement is silent or where two sections disagree about scope.

### F-01 [Medium] `--unattended` is accepted from P1 on, but gates and outward defaults are converted only in P2 and P4
- Expert: Wiegers. Priority: High.
- Location: S:73 ("`--unattended` (from P1 on; P0 briefs omit it ...)"), S:159 ("the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"), S:160-162 (gate conversion P2, outward actions P4), S:67 (WC-9), S:100, S:113-114, S:121.
- Issue: S:73 tells the coordinator to put `--unattended` into every brief from P1. S:159 makes the flag accepted by all of sections 3.1 and 3.2 at P1. S:159 says "no-op where a command has no gate", which implies that for a command that has a gate the flag is not a no-op, but the gate resolutions and WC-9 switch-offs for those commands arrive in P2 (auggie-review, task, cleanup, cli-eval) or P4 (post-release, pr-submit, implement). The spec never says what a P1-era `--unattended` does on those commands, and never says the coordinator must not pass the flag to a command before its own phase.
- Wrong outcome, only under the worse reading: auggie-review accepts `--unattended` in the P1-to-P2 window, keeps posting to the PR with no confirmation (S:100 says the post-off behaviour is P2, and the default posts per INV-A:38), and WC-9 (S:67) is broken by a flag whose name promises otherwise.
- Why Medium: the text allows the reading "P1 adds the flag and the `## Unattended mode` section with its gate text per command" (S:52, S:76), under which no wrong outcome arises. It also contradicts nothing explicitly.
- Recommendation: add one sentence to S:73 or S:154: the coordinator passes `--unattended` to a command only from that command's own phase (the Phase column of S:97-125); before that phase the flag is refused by the command, or is not documented.

### F-02 [Medium] No general rule that `--unattended` propagates to nested `/sc:` invocations; only tasklist to reflect is specified
- Expert: Wiegers. Priority: High.
- Location: S:122 (tasklist passes `--unattended` to each reflect); S:114 (pr-submit row has no nested pass-through); S:104 (cli-eval row); S:118 (roadmap row); section 2.2 WC-2 (S:60).
- Evidence the nesting exists: pr-submit runs a `/sc:auggie-review` fallback and a troubleshoot per finding (INV-B:91). cli-eval create runs `/sc:spec-panel` and adversarial (INV-A:44). roadmap writes memory through `sc:save` at every wave (INV-B:154). task's TFEP calls `/sc:troubleshoot` (INV-B:201). brainstorm calls adversarial and can hand off to tasklist or task-builder (INV-A:39). auggie-review defaults post to GitHub with no confirmation and then wait on a plain-chat offer (INV-A:38, INV-A:62).
- Issue: WC-2 says "the command never calls `AskUserQuestion`, never ends its turn on a chat question" (S:60). Each row handles only the command's own gates. For one nesting case only (tasklist to reflect) the spec states the pass-through. Every other nested call into a gate-bearing command is silent, and `## Unattended mode` sections list "only its own gate resolutions" (S:52).
- Wrong outcome under the worse reading: a pr-submit worker (if D3(b) is chosen) calls auggie-review without `--no-post-pr --no-remediation-offer`, posts a review and then ends its turn on the remediation offer, which is the silent stall of S:44 (2). A cli-eval create run that reaches spec-panel on a TDD input stops on the `target_release` question.
- Why Medium: the outcome appears only if the implementer reads "its own gate resolutions" literally and nobody adds the pass-through; WC-2 as a whole can also be read to cover nested runs.
- Recommendation: add one WC-2 clause: under `--unattended` a command passes `--unattended` (or the nested command's equivalent switches) to every `/sc:` command or skill it invokes, and the row of that nested command applies. Then list the nested cases above in the affected rows.

### F-03 [Medium] WC-4 requires a report directory known before dispatch, but several rows give the command no such flag or location
- Expert: Wiegers and Cockburn. Priority: High.
- Location: S:62 (WC-4: "the directory the brief names for it ... A run whose brief omits that flag is refused"), rows S:104 (cli-eval: "contract for both pipelines"), S:105 (cli-portify: "file location unnamed"), S:109 (implement: "contract beside the ledger `progress.md`"), S:115 (recommend: "write the handoff envelope to a file; contract"), S:119 (save: "contract naming the file written"), S:121 (task: "contract on every tier"), S:112 (load: none).
- Issue: for these rows the spec states neither a directory flag, nor a file flag, nor a derivable path. WC-4's refusal rule and §2.3 ("the output directory, so the report path is known before dispatch") cannot be applied. For implement the ledger path comes from a slug the command derives (INV-A:51 "`.dev/implement/<slug>/progress.md` or managed `<pkg>/progress.md`"), so the coordinator can only guess it. save has no output flag (INV-B:165).
- Wrong outcome under the worse reading: the implementer picks a default location (for example the current directory) for the contract; the coordinator's brief names another; `test -s <contract>` in §7.2 step 4 (S:183) fails, or reads a stale file from a previous Dispatch.
- Why Medium: it is a requirement the document never states (the location rule per row), not a stated text that does harm.
- Recommendation: for each listed row either name the new flag (as S:100, S:102, S:106 do with "add `--output`") or state the derivable path, in the same table cell.

### F-04 [Medium] Four requirements have no acceptance check, and one acceptance check cannot pass for most P2 commands
- Expert: Wiegers (traceability), Crispin. Priority: Medium.
- Location: S:61 (WC-3), S:68 (WC-10), S:69 (WC-11), S:70 (WC-12) against S:167-210; AC-2.2 at S:200.
- Issue (a): no check in section 7 exercises the WC-3 `ask` path, the WC-12 `check`/`consumer_fenced` behaviour, WC-10 for cli-eval (AC-4.3, S:210, covers pr-submit only), or WC-11 for index-repo and cleanup-audit (AC-3.4, S:207, covers save only). The phase table promises these in P1 and P2 (S:159-160).
- Issue (b): AC-2.2 (S:200) reads "Gate-trigger run per P2 command ... `worker_done --outcome failed`; contract `status: blocked`". Several P2 rows resolve their gate by a default or a switch-off, not by blocking: auggie-review (S:100), cleanup and improve (S:103, S:110, list-only), research (S:116, pinned strategy), reflect (S:88, auto-accept), tasklist (S:122). For those commands the stated pass condition (blocked, failed) cannot occur.
- Why Medium: the sentence "for example `/sc:tdd ...`" gives a reasonable reading (only commands whose gate resolves as blocked). It is a missing statement, not a contradiction.
- Recommendation: restrict AC-2.2 to the rows whose resolution is (c) "blocked", and add one check each for WC-3, WC-10 (cli-eval) and WC-11 (index-repo, cleanup-audit), or state that WC-12 is covered by the coordinator's own guide.

### F-05 [Medium] WC-10 and its own decision row disagree with AC-4.3 about the wait size
- Expert: Nygard (feeds Guard Condition Boundary Table, row WC-10). Priority: Medium.
- Location: S:68 (WC-10: a step that blocks one tool call "for longer than 5 minutes ... must be split into waits of at most 4 minutes"), S:266 (decision: "4 minutes leaves a margin under the 5-minute heartbeat cadence"), S:210 (AC-4.3: "no single tool call exceeds 240 s"), S:114 (pr-submit: "stays under 4 minutes").
- Issue: a single blocking call of 4 to 5 minutes (241-300 s) needs no splitting under WC-10, yet fails the 240 s limit that the decision row and AC-4.3 apply. The rule leaves a 60 s band where the requirement and the check disagree.
- Wrong outcome: an implementer who keeps a 280 s poll in a step other than pr-submit meets WC-10 and leaves the heartbeat margin the decision row wanted.
- Why Medium: only pr-submit has the stricter check, and its own row (S:114) already says 4 minutes; for other commands the 5-minute text is merely looser than the rationale.
- Recommendation: state the trigger as "a single call that can block for 4 minutes or more" and keep "waits of at most 4 minutes".

### F-06 [Medium] roadmap's nested `sc:save` writes and the "fresh start" check can clobber shared or earlier state
- Expert: Wiegers and Nygard. Priority: Medium.
- Location: S:118 (roadmap row), S:69 (WC-11: "single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode"), S:205 (AC-3.2), INV-B:154 ("writes memory through `sc:save` at every wave"), INV-B:165 (save overwrites `pm_context`, `last_session`, `next_actions` whole).
- Issue (a): the roadmap row says nothing about its `sc:save` calls. P3 fixes `/sc:save` (S:119) but nothing makes roadmap pass `--unattended` to it (see F-02), so two parallel roadmap workers in one worktree can still write the single-owner keys.
- Issue (b): AC-3.2 runs roadmap with `--unattended --output <dir>` against a directory that already holds `.session-memory.md` and expects it to "start fresh". S:118 replaces the resume prompt with "resume only when passed", so the default is a fresh start in the same directory, which overwrites the earlier partial roadmap files. The prompt that protected them is removed with no replacement guard, and the spec's own WC-6/WC-11 (S:64, S:69) ask for a fresh directory per run.
- Why Medium: (a) is the same silence as F-02; (b) needs the assumption that the earlier partial output is worth keeping, and the coordinator can avoid it by naming a new directory.
- Recommendation: add roadmap to the nested-pass-through list (F-02). Make AC-3.2 use a fresh directory, or state that an unattended run into a non-empty `--output` directory without the resume flag is blocked.

### F-07 [Medium] `/sc:pr-submit`: an existing "Will Not: run headless" is not addressed, and D3(a) conflicts with the P1 and AC-1.1 scope
- Expert: Cockburn and Wiegers. Priority: Medium.
- Location: S:114 (pr-submit row), S:139 and S:240-242 (D3), S:159 and S:195 (P1 flag scope; AC-1.1), INV-B:90 ("Will Not: run headless / imply a daemon" at `cmd/pr-submit.md:85`, `SKILL.md:225`), INV-B:95 ("attended poll loop").
- Issue (a): the pr-submit row adds an `--unattended` mode, but its own file says "Will Not: run headless" (INV-B:90). The spec's evidence cell for the row (S:114) cites `cmd/pr-submit.md:25,39,49,55-56` and never mentions line 85. The spec neither reconciles the two nor treats "attended poll loop" as a conflict.
- Issue (b): D3(a), the recommendation, says pr-submit stays with the coordinator or person and gets "no pr-submit changes in Phase 4" (S:240). S:73 says phases 0-3 proceed on the recommendations (S:225). Yet S:159 and AC-1.1 (S:195) give pr-submit the P1 flag and an `## Unattended mode` section naming the contract file, and section 4 (S:139) says it is a worker candidate only if D3 is accepted.
- Wrong outcome under the worse reading: P1 adds an `## Unattended mode` section to a command that the recommended D3(a) says no worker will run, and which states "Will Not: run headless". AC-1.1 would then fail or pass depending on the unresolved D3.
- Why Medium: the text allows reading D3(a) as "no P4 changes" only, and an implementer can pick it either way.
- Recommendation: either move pr-submit out of AC-1.1 and P1 until D3 is answered, or state in the row that "Will Not: run headless" is narrowed to "unattended means no person at the keyboard but the session stays attended by the coordinator".

### F-08 [Medium] The phase table's command lists do not cover everything that P1's scope sentence and AC-1.1 require
- Expert: Wiegers and Fowler (count conservation; see the Quantity Flow Diagram below). Priority: Medium.
- Location: S:159 (P1 Commands column), S:195 (AC-1.1), S:76 ("Every changed command also gains the `## Unattended mode` section"), S:112 (load row), S:84 and S:87 (brainstorm and init-lite: "Small fix: None").
- Issue: S:159 gives the scope as the flag "accepted by every command in sections 3.1 and 3.2" and AC-1.1 as "every command in sections 3.1-3.2 except `load`". That is 36 commands. The P1 Commands column and the P2-P4 Commands columns together name 34 commands that gain the section (35 names, of which `load` gets only a usage-line fix). `brainstorm` and `init-lite` appear in no Commands column, and their rows say "None". Conversely S:76 says only a "changed" command gains the section, so `brainstorm` and `init-lite` (unchanged) and `load` (usage line only) would not.
- Wrong outcome: an implementer who builds P1 from the Commands column leaves `brainstorm` and `init-lite` without the section, then AC-1.1 fails; one who reads S:76 gives `load` a section and AC-1.1 fails the other way.
- Why Medium: the failing check will catch it, and the scope sentence in S:159 is explicit about which reading wins.
- Recommendation: list `brainstorm` and `init-lite` in the P1 Commands column (flag and section only), and change S:76 to "Every command in sections 3.1 and 3.2 except `load` gains ...".

### F-09 [Medium] The unattended switch has no stated parsing rule
- Expert: Whittaker (sentinel collision attack). Priority: Medium.
- Location: S:51 and S:227-230 (D1(a): "Explicit `--unattended` flag in the brief ... cannot misfire on a person"), SA-1 (S:146).
- Attack: I can break this specification by **Sentinel Collision Attack**. The invariant at **S:229 (D1(a)) / S:146 (SA-1)**, that a person's run never goes unattended, fails when **the literal text `--unattended` appears inside a quoted argument**. Concrete attack: a person runs `/sc:tdd "document how --unattended works for troubleshoot"`. The spec defines no rule saying the flag counts only as a standalone token outside quoted text. The command mis-reads the topic as the switch. Before: interactive, one clarifying question allowed. After: no questions, `blocked` contract or default resolutions, and the report files appear in the working tree, against SA-1 and SA-3.
- Why Medium: "cannot misfire" is an assertion the text makes (S:229), and a careful implementer would write the token rule; the spec does not require it.
- Recommendation: add to S:51: the switch applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing in the unattended mode applies.

### F-10 [Medium] WC-9 says outward actions turn on "only through the command's own explicit flag", but `task` has no such flag
- Expert: Wiegers and Whittaker. Priority: Medium.
- Location: S:67 (WC-9), S:121 (task row: "EXEMPT `commit`/`push` refused unless authorized (WC-9)"), S:245 (D4(a)), INV-B:204 (EXEMPT keywords `commit` and `push` are words in the prompt that "run immediately with no skill", `cmd/task.md:80,99`).
- Issue: the commit/push path in `/sc:task` is selected by a keyword in the request text, not by a flag. WC-9 and D4(a) say authorization is "the command's own explicit flag written in the brief", which does not exist for task. The row does not define one.
- Wrong outcome under the worse reading: the implementer refuses `commit`/`push` always (so D4(a) is unreachable for task) or never (so WC-9 is broken); the spec text supports both.
- Recommendation: either add a named flag for task (for example `--allow-commit`) in the row, or remove task from the D4 list and make the refusal unconditional.

### F-11 [Medium] reflect writes outside the brief's directory by default; tasklist's remediation and HALT path is not mapped
- Expert: Nygard and Wiegers. Priority: Medium.
- Location: S:88 (reflect row), S:122 (tasklist row), S:69 (WC-11), S:185 (7.2 step 6), INV-B:114 (reflect writes the tracked `docs/memory/reflect/deviation-patterns-<slug>.md` and, in UC-2, moves the work-unit folder by default), INV-B:209 (tasklist Stage 10.5: "`needs_human_decision` items HALT" at `SKILL.md:1631`), INV-B:295 (inventory recommends dropping `--remediate`).
- Issue (a): the reflect row mentions `--no-promote` only "when the coordinator owns folder moves". It does not say the tracked memory file is written to a fixed place outside the brief's directory, which is the pattern WC-11 (S:69) forbids ("each Dispatch writes under the directory its brief names"). S:185 step 6 tolerates "the command's documented artifacts" without limiting them.
- Issue (b): the tasklist row (S:122) makes Stage 10.5 pass `--unattended` to reflect so the headless auto-accept applies. The inventory instead recommended dropping `--remediate` (INV-B:295). Auto-accept means each of N reflect runs creates remediation work, and the row does not say what a `needs_human_decision` HALT (INV-B:209) resolves to under WC-2 (default, flag or blocked). The headless rule itself is UNVERIFIED for an Orca worker (S:280, item 9).
- Why Medium: both are missing statements.
- Recommendation: add the reflect memory-file write to the WC-11 list of "documented artifacts" with its path rule. In the tasklist row, say which of WC-2 (a), (b) or (c) applies to the HALT and whether auto-accepted remediation is wanted.

=== ARCHITECTURE ANALYSIS ===

### Fowler (interfaces, bounded contexts) and Newman (versioning)
The central choice is sound as written. Coordinator-level orchestration stays outside the commands (S:16, S:28-39). The commands share one narrow interface: a flag, a report file and a status vocabulary (S:62-63). The shared rules live in one installed document, with each command adding only its own gates (S:52). Each rejection reason R1-R5 in S:31-37 traces to a CAPS line that I checked.

### F-12 [minor] WC-4's contract has no schema version
- Location: S:62 (field list), S:263 (decisions), INV-B:272 ("contract 1.1" for workflow).
- Issue: workflow already versions its contract (INV-B:272). WC-4 defines a shared contract for 30-odd commands but names no `contract_version` field, so a later field change gives the coordinator no way to tell which shape it reads (Newman). The existing contracts' own fields (brainstorm, reflect, workflow, adversarial) were not compared with the WC-4 field list: S:62 says "keep their fields and add the missing ones", yet the §3.1 rows for brainstorm, reflect and init-lite list no additions (S:84, S:87, S:88) and AC-1.2 step 4 (S:183) asserts `d['command']` and the four-value `status` for all of them.
- Recommendation: add `contract_version` to WC-4's minimum fields, and list per existing contract which WC-4 fields are missing.

### F-13 [minor] Refusals are not mapped to a contract status
- Location: S:100, S:102, S:104, S:108, S:110, S:114, S:123, S:62 (WC-4 "written on every outcome"; "refused ... writes nothing"), S:60 (WC-2 lists three resolutions only).
- Issue: rows say a flag is "refused under `--unattended`" (auggie `--post-pr`, business-panel socratic, explain interactive, test `--watch`, pr-submit `--monitor 1`). WC-2 has three resolutions (default, caller flag, blocked); "refused" is a fourth, and WC-4 says both "written on every outcome" and, for a missing directory flag, "writes nothing". WC-5 turns a missing report into `failed`, so the outcome is the same either way and no wrong result follows.
- Recommendation: add "refused" to WC-2 as a case of (c) with `status: failed` and the reason in `blocked_question` or a `reason` field.

### F-14 [minor] SA-1 and SA-3 disagree on how many standalone changes exist
- Location: S:146 ("the two standalone file changes that SA-3 names (F-03)"), S:148 (SA-3: adversarial's fixed name; "the workflow pre-creation STOP contract is written only under `--unattended`"), S:92.
- Issue: only the adversarial rename changes what a standalone run writes. The workflow pre-creation contract is written only under `--unattended`, so it is not a standalone change. An implementer reading S:146 may look for a second standalone change that does not exist. Harmless either way.
- Recommendation: S:146 should say "the one standalone file change SA-3 names".

### F-15 [minor] The section 4 rationale for `/sc:git` borrows a rule that applies only to this run's workers
- Location: S:133 ("need the user's authorization in this repo"; evidence `README:31`), INV-A:49, INV-A:91.
- Issue: `README:31` ("No git commits, pushes, PRs or GitHub comments") is a rule for the workers of this planning run, not a repository policy, and the spec cites it as if it were. D4(a) (S:245) accepts outward actions for post-release and pr-submit when the user names them, so the same logic would allow an authorized `/sc:git` Task; the spec does not say why git differs. The verdict (coordinator-only) is defensible, but the reason given is not supported by the cited line.
- Recommendation: cite the repository rule that requires user authorization for commits, or say plainly that git is excluded to keep every commit with the coordinator.

### F-16 [minor] The claim that a command's own question does not fail `worker-start` is an inference stated as a fact
- Location: S:44 (§1.4 gap 2: "comes *after* readiness, so it does not fail `worker-start`"), CAPS:47 (for Claude "the task is passed on the command line, not typed"; readiness waits for the fresh input box), CAPS:49 (evidence that Orca "never typed into" the unanswered question).
- Issue: with the task in argv, the command can start running before Orca decides readiness. No run was observed (S:43, S:272 item 1), and the spec does not mark the claim UNVERIFIED. WC-2 forbids the prompt anyway, so the design does not depend on the answer.
- Recommendation: mark the sentence UNVERIFIED and add it to the AC-0.4 smoke run.

### Nygard (failure modes), Hohpe (message flow)
- The failure modes the spec names (silent stall, missing report, `consumer_fenced`, circuit breaker, release rules) are all tied to CAPS lines (S:44, S:70, S:263, S:186).
- Open and acknowledged as UNVERIFIED: no Orca bound on a Dispatch's total run time (S:282, item 11), the `ask` default timeout (S:281, item 10), whether Orca checks the `--report-path` file (S:274, item 3). Each is carried as a stated assumption with a fallback (coordinator opens the file, S:73).
- Message flow is unidirectional and bounded: brief in, one `worker_done` out, `ask` for questions, pull-only follow-ups (S:61-63, S:70). The one ordering gap is F-01 (flag acceptance before behaviour).

### Whittaker (adversarial), remaining attacks
- **Zero/Empty Attack**: `--output ""`, or a directory flag whose value is empty. WC-4 refuses only an omitted flag (S:62). Empty value: not specified. Covered by the table row `WC-4 flag present`.
- **Divergence Attack**: `partial` versus `blocked` at the same gate. A command that finishes half its work and reaches a gate has no stated rule for choosing between them (S:62-63). Low consequence because WC-5 maps `partial` to succeeded and `blocked` to failed, so a coordinator can mistake a half-finished run for a good one; S:73 (coordinator opens the report) is the mitigation.
- **Sequence Attack**: F-01 (flag before behaviour); retry after `blocked`: re-invoking into the same output directory restarts a command that has only "fresh dir" as resume (for example task, S:121), so a mid-run block loses the work done.
- **Accumulation Attack**: repeated `--retry-of` after `blocked` counts toward Orca's three-failure breaker only for failed starts, not for the worker's own failed reports (CAPS:80), so repeated blocked reports do not trip it; the spec records that (S:263).

---

## Guard Condition Boundary Table
Format: structured markdown, 7 columns (NFR-5). The table is complete: every guard enumerated, every cell filled, every omitted input class given a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` standalone token | S:51, S:229, S:146 | Zero/Empty | no flag | false | interactive behaviour unchanged (SA-1) | OK |
| `--unattended` standalone token | S:51, S:229 | Sentinel Value Match | `--unattended` inside a quoted topic | ? | unspecified (F-09) | GAP |
| `--unattended` before the command's own phase | S:73, S:159-162 | Legitimate Edge Case | flag passed to auggie-review at P1 | ? | unspecified (F-01) | GAP |
| WC-4 directory flag present | S:62 | Zero/Empty | flag omitted | true (refuse) | refused before any work, writes nothing; WC-5 maps to `failed` | OK |
| WC-4 directory flag present | S:62 | Zero/Empty | flag given with empty value `""` | ? | unspecified (Whittaker, Zero/Empty) | GAP |
| WC-4 directory flag present | S:62, S:104-105, S:109, S:115, S:119, S:121 | Legitimate Edge Case | command has no such flag | n/a | unspecified (F-03) | GAP |
| WC-4 directory flag present | S:62 | Typical | `--output <dir>` | false (proceed) | contract `<dir>/return-contract.yaml` | OK |
| WC-10 wait split (`> 5 min` to waits `<= 4 min`) | S:68, S:210, S:266 | Typical | 2 min wait | false | no split, heartbeat between calls | OK |
| WC-10 wait split | S:68 | Legitimate Edge Case | single call of 4.5 min (270 s) | false | not split; fails the 240 s limit of AC-4.3 (F-05) | GAP |
| WC-10 wait split | S:68 | Maximum/Overflow | cli-eval run up to 3600 s | true | split into waits `<= 4 min`; no AC for cli-eval (F-04) | GAP |
| WC-5 outcome mapping | S:63 | Zero/Empty | no report exists | true | `--outcome failed` | OK |
| WC-5 outcome mapping | S:63 | Legitimate Edge Case | `partial`; audit verdict FAIL | true | `--outcome succeeded`; status in body's first sentence | OK |
| WC-6 retry / fresh directory | S:64, S:73 | Typical | `--retry-of` with a new directory | true | fresh directory, no corruption | OK |
| WC-6 retry / fresh directory | S:118, S:205 | Legitimate Edge Case | unattended roadmap into non-empty `--output` without resume flag | ? | starts fresh, overwriting (F-06) | GAP |
| WC-9 outward action off | S:67, S:100, S:113 | Typical | no authorizing flag | true | action off, skipped step listed in the contract | OK |
| WC-9 outward action off | S:67, S:121 | Legitimate Edge Case | task `commit`/`push`, no flag exists | ? | unspecified (F-10) | GAP |
| Nesting depth 1 (WC-8) | S:66, S:33 | Maximum/Overflow | command calls `worker-start` at depth 1 | true | refused by Orca (`nested_worker_depth_exceeded`); command forbidden to try | OK |
| Nesting depth 1 (WC-8) | S:66 | Zero/Empty | depth setting absent or malformed | n/a | Orca falls back to 1 (CAPS:100) | OK |
| Readiness limit (WC-1) | S:59 | Maximum/Overflow | launch prompt with fallback above ~45 s | true | fails at `agent_readiness` (EVIDENCE.md:56 via CAPS:49) | OK |
| Readiness limit (WC-1) | S:59 | One/Minimal | fallback of 30 s | false | passes (CAPS:49) | OK |
| WC-2 gate resolution (a)/(b)/(c) | S:60 | Legitimate Edge Case | flag "refused" (auggie `--post-pr`, socratic, `--watch`) | ? | fourth case, status not mapped (F-13) | GAP |
| WC-2 gate in a nested command | S:60, S:122 | Legitimate Edge Case | pr-submit to auggie-review; cli-eval to spec-panel | ? | unspecified except tasklist (F-02) | GAP |

Input classes left out, with reasons: "One/Minimal" and "Maximum/Overflow" for the `--unattended` token and for WC-5 do not apply because the guard is boolean/enumerated; "Sentinel Value Match" for WC-5 does not apply because `status` takes four fixed strings and the command writes them itself.

GAP rows are carried into the findings above. Their grading is Medium or minor per the consequence rule: FR-8/FR-9 findings are blocking only when they name a concrete wrong outcome an implementer would produce or a safety-boundary risk. None of the GAP rows needed no further assumption.

## Quantity Flow Diagram
```text
[Source: 43 commands in cmd/ (S:76: 21 in INV-A:3 + 22 in INV-B:3)]
   --> [Stage 1: classify by inventory verdict]
        --> 10 ready + 27 needs-change + 6 coordinator-only = 43   (conserved; matches INV-A:73 5/13/3 and INV-B:278 5/14/3)
   --> [Stage 2: worker-capable = 10 + 27 = 37]
        --> [Stage 3: assign to phase, Commands column S:159-162]
             P1: 9 listed + 4 fixes (adversarial, cleanup-audit, index-repo, workflow) = 13
             P2: 15   P3: 4   P4: 3                         = 35 named
             not named in any Commands column: brainstorm, init-lite = 2   <-- MISMATCH (37 vs 35)
   --> [Consumer: AC-1.1, S:195: "every command in 3.1-3.2 except load" = 36 must carry the section]
        Commands column gives 34 that gain it (35 minus load)             <-- MISMATCH (36 expected, 34 named)
   --> [Consumer: S:76 "every changed command": excludes unchanged brainstorm, init-lite]  <-- disagrees with AC-1.1
```
The mismatch is F-08 (Medium: AC-1.1 catches it, scope sentence S:159 decides).

---

## Expert consensus
- The decision (Orca on top, commands stay units of work) and its rejected alternative are well argued and cross-referenced.
- The weak points are in scope bookkeeping and in places where a requirement stops short of the behaviour it needs: nesting, report location, authorization flag, phase ordering.
- None of those is a stated text that produces a wrong result without a further guess, so none is blocking.

## Follow-up candidates (Medium and minor; none triggers a revision)
Medium: F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11.
Minor: F-12, F-13, F-14, F-15, F-16.

Question for the user (recorded here; the coordinator asks once per loop and no issue is created without an answer): open a single issue listing the Medium follow-ups F-01 to F-11? This run was not `--unattended`, but it is a worker sandbox with no person present, so no issue was opened and the list is only recorded.

Reviser brief: none. There is no blocking finding, so the report carries no revise list and no Reviser contract applies.

verdict: PASS
