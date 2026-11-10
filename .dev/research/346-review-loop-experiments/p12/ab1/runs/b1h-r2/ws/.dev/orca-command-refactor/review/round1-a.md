# Spec-panel critique: Orca worker contract spec (round 1)

review: 1 of 3
candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
candidate sha256: d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
baseline: missing (first review; no `--re-review`)
reviewer model: claude-haiku-5-5 (Haiku 5.5), single session
mode: critique, focus `requirements,architecture`
prompt: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full)

## Coverage and limits

- Read: `command.md`; `.dev/orca-command-refactor/README.md` (binding context); the candidate in full; `inventory/commands-a.md` (120 lines), `inventory/commands-b.md` (323 lines), `inventory/orca-capabilities.md` (188 lines) in full.
- Checked: the candidate's citations to `INV-A:N`, `INV-B:N`, `CAPS:N` against the inventory lines; the command-count arithmetic (43 = 10 + 27 + 6; 21 in A, 22 in B); the 3.1 and 3.2 rows against the inventory verdicts; the phase and acceptance-check cross-references.
- UNVERIFIED: every citation to `src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `plugins/superclaude/...` and `~/.claude/...`. None of these is in the sandbox. Where a finding rests on such a citation, it says so.
- Not run in this session: the three first reviews and the MERGE rule (this session is one reviewer, with no fresh-context sub-reviewers), and the VERIFY pass. The six blocking findings below are therefore unconfirmed by a fresh verifier. The coordinator must run VERIFY before any revision, as the review-loop prompts require.
- Follow-up candidates (Medium and minor) are listed, not acted on. The coordinator asks the user once whether to open issues for them; this report creates none.

Grading note: each finding is graded by consequence (review-loop rule 2). A finding is blocking when the spec's stated text leads an implementer to a concrete wrong build, when two stated texts contradict each other in a way that changes what gets built, when an acceptance criterion cannot pass as written, or when the text opens a safety boundary.

---

## === REQUIREMENTS ANALYSIS ===

### REQ-1 (blocking): the common acceptance check AC-C1 cannot pass in the phase that adds the contract

- Severity: MAJOR. Expert: Wiegers (testability), Adzic (acceptance examples).
- Location: `specs/orca-worker-contract-spec.md:172` (AC-C1 greps `src/superclaude/core` for Orca verbs and excludes only `ccsession-tag`). `:158` (P0 adds `src/superclaude/core/WORKER-CONTRACT.md` and an Orca section to `HOW-WE-WORK.md`). `:147` (SA-2 allows an Orca mention "inside the contract file" as an example of the question channel). `:150` (SA-5, routing-guide Orca section).
- Issue: AC-C1 is a common check that every phase must pass (`:169-176`, "A phase passes only when every check in its block and every common check passes"). Its grep covers `src/superclaude/core`. P0 puts the contract file and an Orca section in that directory, and SA-2 expects the contract file to name the Orca question channel. Both produce `orca orchestration ...` text that AC-C1 matches. AC-C1 therefore fails at P0 by design.
- Grading check: "An implementer who follows the stated text as written builds the P0 contract file and the routing-guide Orca section, runs AC-C1, and gets a match, so P0 cannot pass; this is wrong because the common check is a stated pass condition for every phase." Blocking: an acceptance criterion cannot pass.
- Recommendation: exclude `WORKER-CONTRACT.md` (and the Orca section, or name its file) from AC-C1, or change AC-C1 to forbid Orca verbs in command and skill files only, matching SA-2's wording. State the exclusion in one place.
- Priority: High. Quality impact: testability 6 to 8 once fixed.

### REQ-2 (blocking): AC-0.4 step 4 cannot pass for `/sc:troubleshoot`

- Severity: MAJOR. Expert: Adzic (acceptance examples), Wiegers.
- Location: `specs/orca-worker-contract-spec.md:194` (AC-0.4: "step 4 uses the command's existing report file"), `:183` (step 4: `test -s <contract>` and a YAML parse asserting `d['status']` and `d['command']`), `:91` (troubleshoot row: today's report is `REPORT.md` (`report_path`)). `inventory/commands-b.md:49` and `:242` (troubleshoot writes `REPORT.md`; `return-contract.yaml` only with `--caller task-unified`).
- Issue: step 4 requires a YAML file with `status` and `command`. For troubleshoot the existing report is a Markdown `REPORT.md` with no such keys, and the contract exists only under `--caller task-unified`, which the P0 brief does not pass. The check fails on a correct run.
- Grading check: "An implementer who runs AC-0.4 as written on troubleshoot builds a correct run, runs step 4, and the YAML parse fails; this is wrong because the criterion checks a file type the command does not write." Blocking: an acceptance criterion cannot pass.
- Recommendation: define step 4 per command for P0 (troubleshoot checks that `REPORT.md` exists and is non-empty, with `status` from the worker's `worker_done` instead), or replace troubleshoot in the P0 set with a command that writes the YAML contract today (adversarial or workflow).
- Priority: High. Quality impact: testability 5 to 7.

### REQ-3 (medium, follow-up): Section 1.4 contradicts evidence E3 about whether a direct-route run exists

- Severity: MAJOR label, Medium by consequence. Expert: Wiegers (stated evidence), Nygard (evidence strength).
- Location: `specs/orca-worker-contract-spec.md:43` ("The only end-to-end proof is the PR #329 run, and its brief told workers to run `/sc:adversarial` through an Agent-tool subagent"). `:23` (E3 cites `return-contract.yaml:10` with `invocation_method: "skill-direct"` as support). `:272` (UNVERIFIED 1: "no such run was observed"). `inventory/commands-a.md:13` and `:35` (a `skill-direct` Orca-worker run is recorded as "proven as a direct Orca-worker skill call").
- Issue: the spec says the only end-to-end proof is nested, then cites a `skill-direct` run as evidence in E3. The inventory supports the `skill-direct` run. The spec does not reconcile the two.
- Grading check: "An implementer who follows section 1.4 still runs Phase 0 smoke tests (AC-0.4), so no wrong build follows; the defect is in the evidence record." Medium by consequence, because Phase 0 runs regardless.
- Recommendation: state the `skill-direct` run in 1.4 with its path, say what it does and does not prove (for example, whether it ran the Task fan-out inside the top-level session), and keep AC-0.4 as the test of the direct route.
- Priority: Medium. Quality impact: consistency 4 to 6.

### REQ-4 (medium, follow-up): WC-7, WC-10 and WC-12 have no acceptance check; the AC-0.4 claim is not supported by its own steps

- Severity: MAJOR label, Medium by consequence. Expert: Adzic, Wiegers.
- Location: `specs/orca-worker-contract-spec.md:65` (WC-7 "never wraps the command in an Agent-tool subagent"), `:68` (WC-10 heartbeat every 5 minutes), `:70` (WC-12 `check` before `worker_done`). `:194` (AC-0.4 says "verified in the step-5 transcript" that the run was direct). `:184` (step 5 only searches the transcript for `AskUserQuestion`).
- Issue: AC-0.4 claims the step-5 transcript verifies no Agent-tool wrapper, but step 5's pass condition checks only for `AskUserQuestion`. WC-10's heartbeat cadence and WC-12's `consumer_fenced` handling have no pass condition at all.
- Grading check: "An implementer who follows section 7.2 builds the live check as written; a run that wraps the command in a subagent, or that sends no heartbeat, passes every step." Medium by consequence: the spec's own text is incomplete, and no decision is wrong.
- Recommendation: add to step 5 a search for `Agent`/`Task` tool calls that wrap the command, and to step 2 a check that heartbeats arrive at most 5 minutes apart (from `worker-read` or `worker-show`). Give WC-12 a test or drop the claim.
- Priority: High. Quality impact: testability 5 to 7.

### REQ-5 (medium, follow-up): step 6 (`git status --short` limited to the output directory) cannot pass for commands that edit source

- Severity: MAJOR label, Medium by consequence. Expert: Adzic, Cockburn (actor and artifact).
- Location: `specs/orca-worker-contract-spec.md:185` (step 6: "only files under the brief's output directory (and the command's documented artifacts) appear"). `:103` (cleanup edits code), `:109` (implement edits product files), `:123` (test `--fix` edits), `inventory/commands-a.md:51` ("Edits product files"), `inventory/commands-b.md:48` (`--fix` applies fixes).
- Issue: the phrase "documented artifacts" is not defined per command. Implement, cleanup, improve and test `--fix` legitimately change source files, so step 6 fails on a correct run unless each command's documented artifacts are listed. The spec does not list them.
- Grading check: "An implementer who runs step 6 on implement builds a correct run, and step 6 fails because product-file edits are not in the allowed set." Medium by consequence, since the fix is a list.
- Recommendation: add a per-command list of allowed changed paths to section 3, or change step 6 to compare against the set of files the contract's `artifacts` field names.
- Priority: Medium. Quality impact: testability +1.

### REQ-6 (medium, follow-up): the readiness fallback has no number, and the owner of WC-1 is not assigned

- Severity: MAJOR label, Medium by consequence. Expert: Nygard (failure modes), Wiegers (measurability).
- Location: `specs/orca-worker-contract-spec.md:59` (WC-1: "fall back on its own well inside the readiness limit (default 60 s)"; owner "Launch setup, not commands"). `:158-162` (the six phases list no launch-setup change). `:81` (ten commands "run as workers now"). `inventory/orca-capabilities.md:49` (the `EVIDENCE.md:39,45,56` quotes: a 45-second limit failed, a 30-second fallback passed, above about 45 seconds fails again).
- Issue: "well inside" is not measurable. The evidence in the inventory gives a working value (30 s) and a failing one (above about 45 s). No phase or file implements the launch-side fallback, and the ten "ready today" commands depend on it.
- Grading check: "An implementer who follows WC-1 cannot choose a fallback value from the text, and no phase changes the launch wrapper; the ten ready commands can still stall at startup." Medium: the gap is undefined, not contradictory.
- Recommendation: state the fallback as 30 s, name the file that owns the launch path (or say it is out of scope and make the ready-today claim conditional on it), and add a phase or precondition for it.
- Priority: High. Quality impact: completeness 6 to 7.

### REQ-7 (medium, follow-up): WC-11's "timestamp or slug" rule conflicts with ready-today rows that use fixed output paths

- Severity: MINOR-MAJOR label, Medium by consequence. Expert: Fowler (shared state), Wiegers.
- Location: `specs/orca-worker-contract-spec.md:69` (WC-11: "Default output paths carry a timestamp or the slug the coordinator passes"). `:85` (cleanup-audit: output dir fixed at `.claude-audit/`). `:86` (index-repo: `PROJECT_INDEX.md`, no flag). `:116` (research: `claudedocs/research_*`, generated).
- Issue: three ready-today commands have fixed or generated default paths. WC-11 says defaults must carry a slug or timestamp. The spec handles cleanup-audit with "one audit per worktree at a time", a coordinator rule that WC-11 does not state.
- Grading check: "An implementer who applies WC-11 to index-repo either renames its output (a standalone change the spec does not list) or leaves two workers able to write the same file; the text does not say which." Medium.
- Recommendation: restate WC-11 as "a coordinator must not run two workers on the same fixed output path in one worktree", and say which commands need a path change.
- Priority: Medium. Quality impact: consistency +2.

### REQ-8 (medium, follow-up): WC-9 states a coordinator-written flag is enough to turn on outward actions, but D4 is open

- Severity: MAJOR label, Medium by consequence. Expert: Cockburn (who authorizes), Nygard (safety boundary).
- Location: `specs/orca-worker-contract-spec.md:67` (WC-9: outward defaults "turn on only through the command's own explicit flag written in the brief"). `:244-247` (D4: option (a) recommended, "Only when the user's own instruction to the coordinator names that action"; option (b) never).
- Issue: under WC-9 as written, a coordinator can authorize a push or PR on its own. D4, which the spec leaves to the user, asks whether that is allowed. The requirement is already decided before the decision is taken.
- Grading check: "An implementer who builds WC-9 as written lets the coordinator enable posting even if the user picks D4 option (b)." Medium: the outcome depends on a decision the spec says is open; it does not change until D4 is answered.
- Recommendation: make WC-9 read "subject to D4" and list the option chosen for each command after the user answers.
- Priority: Medium. Quality impact: consistency +2.

### REQ-9 (medium, follow-up): the status vocabulary has no rule for unknown values or for choosing `partial`

- Severity: MINOR-MAJOR label, Medium by consequence. Expert: Wiegers, Whittaker (zero and divergence attacks).
- Location: `specs/orca-worker-contract-spec.md:62` (`status` one of four values; no rule for another value), `:63` (WC-5 maps only `failed`, `blocked`, missing report to `failed`), `:263` (`partial` maps to `succeeded`; no rule for when a command reports `partial`).
- Issue: a contract with an unlisted status, or a malformed file, is not mapped. The implementer picks a mapping. `partial` is defined by its outcome mapping but not by when a command must emit it.
- Grading check: "An implementer who meets `status: done` has no rule; the coordinator may read it as success or failure." Medium.
- Recommendation: state that any other value or unparseable contract maps to `failed`, and define `partial` by one example.
- Priority: Medium. Quality impact: completeness +1.

### REQ-10 (minor): the pr-submit 600-second reading is the spec's own reinterpretation

- Severity: MINOR. Expert: Nygard.
- Location: `specs/orca-worker-contract-spec.md:114` (pr-submit: the 600 s default is "a cumulative per-wait budget over poll-then-sleep iterations, so the session can already heartbeat between iterations"). `:283` (UNVERIFIED 12: poll-script runtime unknown). `inventory/commands-b.md:91` and `:299` (the poll loop "waits up to `--timeout` 600 s per wait over several rounds"; heartbeats needed).
- Issue: the spec turns the inventory's "per wait" into "cumulative" and draws the conclusion that heartbeats are already possible. That conclusion depends on UNVERIFIED 12, and the inventory lists heartbeats as a change needed.
- Grading check: "An implementer who trusts row 114 leaves pr-submit without the heartbeat change; the run can then go silent for longer than 5 minutes if one poll iteration is long." Minor, because pr-submit is open under D3 and the change applies only if D3 chooses worker.
- Recommendation: mark the "already heartbeats" claim as conditional on UNVERIFIED 12.
- Priority: Low. Quality impact: consistency +1.

### REQ-11 (minor): pr-submit is counted in the worker totals, though D3 recommends coordinator-only

- Severity: MINOR. Expert: Cockburn.
- Location: `specs/orca-worker-contract-spec.md:114` (pr-submit in section 3.2, counted in the "27 needing a change"). `:139` (pr-submit "stays a worker candidate only if the user accepts open decision D3"). `:240` (D3 recommended (a): coordinator or person only).
- Issue: the totals (`:76`) count pr-submit as a worker candidate while the recommended decision removes it.
- Recommendation: add "(if D3 = worker)" to the pr-submit row and to the totals in `:76`.
- Priority: Low.

### REQ-12 (minor): AC-1.1 requires the `## Unattended mode` section in every command in 3.1 and 3.2, though section 3 says only changed commands get it

- Severity: MINOR. Expert: Adzic.
- Location: `specs/orca-worker-contract-spec.md:195` (AC-1.1: every command in sections 3.1-3.2 has the section). `:76` ("Every changed command also gains the `## Unattended mode` section"). `:84` and `:87` (brainstorm and init-lite: "None" for the small fix).
- Issue: the test and the prose disagree for commands whose row says no change.
- Recommendation: state that the section is added to every 3.1 and 3.2 command, which is what P1 says (`:159`), and drop "changed" from `:76`.
- Priority: Low.

---

## === ARCHITECTURE ANALYSIS ===

### ARCH-1 (blocking): WC-4's `<output-dir>/return-contract.yaml` rule cannot be applied to the rows that define their own output

- Severity: MAJOR. Expert: Fowler (interface), Hohpe (message contract between worker and coordinator).
- Location: `specs/orca-worker-contract-spec.md:62` (WC-4: contract at `<output-dir>/return-contract.yaml`, "known before dispatch"). `:73` (section 2.3: the brief names the output directory "so the report path is known before dispatch"). `:83` (adversarial: "Fix the contract filename to `<output>/adversarial/return-contract.yaml`"). `:87` (init-lite: `--output <file>`). `:90` (tdd: `--output <file>`; "the TDD at `--output`"). `:92` (workflow: `.dev/tasks/to-do/<id>/return-contract.yaml`; no output flag). `:116` (research: "contract naming the generated `claudedocs/research_*.md` path"). `inventory/commands-b.md:47` (tdd `--output` is a file). `inventory/commands-b.md:52` (workflow contract location).
- Issue: WC-4 defines the contract as a file in a directory named by `--output`. Four rows contradict that: adversarial puts it in a subdirectory, init-lite and tdd treat `--output` as a file, workflow has no output directory, and research generates its path at run time. The coordinator follows section 2.3 and opens a path that does not exist, or writes into a file path.
- Grading check: "An implementer who follows WC-4 and section 2.3 for tdd passes `--output <file>` as a directory, so the contract path is `<file>/return-contract.yaml`, which cannot be written; for adversarial the coordinator opens `<output-dir>/return-contract.yaml`, which does not exist." Blocking: two stated texts contradict, and the coordinator reads the wrong file.
- Recommendation: define the contract path per command in section 3 (one column), keep `<output-dir>/return-contract.yaml` only for commands whose `--output` is a directory, and say how the coordinator learns the path for workflow and research before dispatch (for example, the brief passes `--contract <path>`).
- Priority: High. Quality impact: consistency 4 to 7.

### ARCH-2 (blocking): the P1 change to workflow writes a contract in standalone mode, which SA-3 forbids

- Severity: MAJOR. Expert: Fowler, Nygard (partial-run safety).
- Location: `specs/orca-worker-contract-spec.md:148` (SA-3: "The new contract file and report files are written only in unattended mode or when the caller passes the new output flag"). `:92` (workflow row: "Write the contract for pre-creation STOPs too (WC-4 'every outcome') (P1)"). `:62` (WC-4 applies "In unattended mode"). `inventory/commands-b.md:52` and `:272` (workflow writes no contract for pre-creation STOPs today; the contract is written only after the package exists).
- Issue: SA-3 says standalone runs write no new contract files. The P1 workflow change writes one on a pre-creation STOP, which is standalone behaviour. Because the STOP happens before the package exists, the spec also gives no location for the file.
- Grading check: "An implementer who builds the P1 workflow change writes `return-contract.yaml` in a person's tree on a plain `/sc:workflow` STOP, and cannot choose a directory for it; SA-3 says that must not happen." Blocking: it violates a hard requirement stated as holding in every phase (`:141`).
- Recommendation: gate the pre-creation contract on `--unattended` (and a `--output` directory), name its location, or drop it from P1.
- Priority: High. Quality impact: consistency +3.

### ARCH-3 (blocking): P1 accepts `--unattended` on commands whose outward defaults stay on until P2 or P4

- Severity: MAJOR. Expert: Nygard (safety boundary), Newman (interface evolution).
- Location: `specs/orca-worker-contract-spec.md:159` (P1: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"). `:100` (auggie-review: posts to the PR by default; the change is phase P2). `:121` (task: commit and push by default; phase P2). `:113-114` (post-release and pr-submit: phase P4). `:67` (WC-9: under `--unattended`, outward defaults "are off"). `inventory/commands-a.md:38` (auggie-review posts by default with no prompt). `inventory/commands-b.md:94`, `:297` (pr-submit and task outward actions).
- Issue: the "no-op" caveat applies only to commands with no gate. auggie-review has gates and an outward default, so in P1 `/sc:auggie-review <PR> --unattended` is accepted and still posts to GitHub. WC-9 says it must not.
- Grading check: "An implementer who ships P1 and runs `/sc:auggie-review <PR> --unattended` as the brief allows gets a posted review on the PR, which WC-9 forbids; the phase text says the flag is accepted with no change in behaviour." Blocking: outward action from a flag the spec says is safe.
- Recommendation: in P1, reject `--unattended` with an error for every command that has an outward default until its P2 or P4 change lands, or move the outward-default change for auggie-review and task into P1.
- Priority: High. Quality impact: consistency +3.

### ARCH-4 (blocking): the P2 reflect change makes a worker self-approve code remediation, which D2 forbids for implement

- Severity: MAJOR. Expert: Nygard, Fowler (who decides).
- Location: `specs/orca-worker-contract-spec.md:88` (reflect, P2: "Under `--unattended`, make `--remediate` follow the existing headless auto-accept rule instead of the `[yes / no]` prompt"). `:122` (tasklist: "Stage 10.5 passes `--unattended` to each reflect so the headless rule applies"). `:151` (SA-6: the headless rule keys on `claude --print` and "`--unattended` reuses it and does not replace it"). `:232-236` (D2: an agent must not approve its own work; "the rule exists to stop an agent approving its own work"). `:280` (UNVERIFIED 9: an Orca worker is "assumed" not headless). `inventory/commands-b.md:109`, `:310` (the headless rule keys on `claude --print` with no TTY).
- Issue: the spec applies the headless auto-accept to a worker, which is not headless by the spec's own assumption (`:280`). Either the trigger is re-keyed to `--unattended` (which the spec says it does not do, `:151`) or the prompt stalls (contrary to WC-2). If it fires, a worker auto-accepts remediation that may edit code, which D2 forbids for implement. The spec does not say whether Stage 10.5 still passes `--remediate`.
- Grading check: "An implementer who follows row 88 either stalls the reflect worker at the prompt or re-keys the headless rule, and in the second case a worker applies code remediation without a person, which D2 says must not happen." Blocking: safety-boundary risk stated in the spec's own rationale.
- Recommendation: state the trigger for `--unattended` explicitly, state that remediation is never auto-accepted under `--unattended` (the gate resolves as blocked, per WC-2 (c)), and state whether Stage 10.5 drops `--remediate`.
- Priority: High. Quality impact: consistency +3.

### ARCH-5 (medium, follow-up): the WC-3 question hand-off has no mechanism

- Severity: MAJOR label, Medium by consequence. Expert: Hohpe (message routing), Nygard.
- Location: `specs/orca-worker-contract-spec.md:60` (WC-2 (c): a gate that cannot resolve writes `status: blocked` and stops). `:61` (WC-3: "the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag"). `:198` (AC-1.4 and P1 contract checks). `inventory/orca-capabilities.md:58-61` (`ask` blocks; timeout leaves the question pending).
- Issue: WC-2 says the command stops at a blocked gate. WC-3 says the session may then ask and re-invoke the command with the answer as a flag. The spec does not say who reads `blocked_question`, which flag carries each answer, or whether every gate has a flag. Each of the 27 needs-change commands would need its own answer flag, and the spec does not list them.
- Grading check: "An implementer who builds WC-3 cannot tell whether the session reads `blocked_question` and re-invokes, or whether a command asks directly; the text permits both." Medium: the text is incomplete, not contradictory.
- Recommendation: state the hand-off as a three-step protocol (read `blocked_question`, `ask` once, re-invoke with `--<gate>-answer`), and list the answer flag per gate in section 3, or say WC-3 is out of scope for phase 1.
- Priority: Medium. Quality impact: completeness +2.

### ARCH-6 (medium, follow-up): retries and resumes write into the same output, and the coordinator has no rule to avoid it

- Severity: MAJOR label, Medium by consequence. Expert: Fowler, Whittaker (sequence attack).
- Location: `specs/orca-worker-contract-spec.md:64` (WC-6: a retry "must not corrupt the first attempt's output"; a command resumes or uses a fresh directory). `:73` (section 2.3 lists the brief's contents; no retry rule). `:116` (`--resume` commands: brainstorm, release-split, pr-submit reuse their run state). `inventory/orca-capabilities.md:116` (`worker-start --retry-of`).
- Issue: a resuming command writes into the directory it already used, so a `--retry-of` worker overwrites the contract the coordinator has not yet read. Section 2.3 does not require the coordinator to pick a new directory for a retry.
- Grading check: "An implementer who writes the brief from section 2.3 reuses the output directory on retry; the first attempt's `return-contract.yaml` is replaced before the coordinator reads it." Medium: the spec states the goal in WC-6 but not the coordinator duty that meets it.
- Recommendation: add to section 2.3, for a retry: a new output directory, or a contract copy taken before the retry.
- Priority: Medium. Quality impact: completeness +1.

### ARCH-7 (medium, follow-up): the tasklist row overrides inventory B's required change and relies on nested fan-out the inventory calls unverified

- Severity: MAJOR label, Medium by consequence. Expert: Fowler, Newman.
- Location: `specs/orca-worker-contract-spec.md:122` (tasklist: "Other required change: none (its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`)"). `inventory/commands-b.md:215` (needs-change: "Stage 10.5 should call reflect without `--remediate`... the per-phase reflect fan-out must run at the worker's top level, not inside subagents"). `:295` (needs-change row: "Remove a nested fan-out"). `:210` and `:314` (UNVERIFIED: whether nested spawning works). `inventory/commands-a.md:14` (nesting is allowed "up to three layers" per documentation, with the depth-limit warning).
- Issue: the spec drops the change inventory B requires and cites inventory A's general statement about the documentation as if it settled this case. Inventory B marks the nested spawn UNVERIFIED. The decisions table (`:268`) says verdicts were kept, but the required change was dropped without a decision entry.
- Grading check: "An implementer who follows row 122 leaves Stage 10.5 running reflect in subagents, which B says is unverified and which may lose the Agent tool at the depth limit." Medium: a dropped requirement without a recorded decision.
- Recommendation: record the decision in the Decisions table, and either keep B's change or verify nesting first (an AC).
- Priority: Medium. Quality impact: consistency +2.

### ARCH-8 (medium, follow-up): the plugin mirror is not in any phase or check

- Severity: MINOR-MAJOR label, Medium by consequence. Expert: Fowler (single source of truth).
- Location: `specs/orca-worker-contract-spec.md:279` (UNVERIFIED 8: "How `plugins/superclaude/commands/` ... is kept in step with `src/superclaude/commands/` ... was not read. Each phase's plan must resolve this before editing"). `:158-162` (phases edit `src/superclaude/commands/` and `core/` only). `:172-176` (common checks run `make verify-sync` only).
- Issue: the spec admits a mirror exists and that its update rule is unknown, but no phase or check covers it. Phases 1 to 4 would leave the mirror stale, and `make verify-sync` (`:173`) may not cover it.
- Grading check: "An implementer who follows P1 through P4 edits the source commands and leaves the plugin copies behind, and no check fails." Medium: the rule is not stated, but the gap is.
- Recommendation: add a check that the plugin mirror matches the source for every changed command, or state that the mirror is out of scope.
- Priority: Medium. Quality impact: completeness +2.

### ARCH-9 (minor): the boundary between standalone and unattended behaviour depends on parsing a flag that a person can type

- Severity: MINOR. Expert: Whittaker (sentinel collision).
- Location: `specs/orca-worker-contract-spec.md:228` (D1 (a): "cannot misfire on a person"). `:51` (`--unattended` as a flag in the brief).
- Issue: a person's request that contains the literal `--unattended` inside quoted content (for example a topic about this feature) switches on unattended behaviour, including the ARCH-4 path. The spec says the flag cannot misfire.
- Recommendation: state how the flag is parsed (a standalone argument outside quotes), and remove "cannot misfire" unless the parsing rule is stated.
- Priority: Low.

### ARCH-10 (minor): E2 and E4 state more than the cited evidence shows

- Severity: MINOR. Expert: Fowler.
- Location: `specs/orca-worker-contract-spec.md:22` (E2: "has the same tools as a command a person runs"; the cited `CAPS:161` says only that a worker is a top-level Claude session; "and answered" is not in the `CAPS:45` quote). `:24` (E4: subagents "are not counted by Orca's nesting limit", without the UNVERIFIED mark that `inventory/orca-capabilities.md:155` gives).
- Recommendation: mark both as partly verified, as `CAPS:155` and section 1.4 (`:45`) already do.
- Priority: Low.

### ARCH-11 (minor): WC-2 calls a stall invisible, while section 1.4 and step 2 say it is visible

- Severity: MINOR. Expert: Nygard.
- Location: `specs/orca-worker-contract-spec.md:60` ("a worker waiting on a prompt is 'healthy', so a stall is invisible"). `:44` and `:181` (the coordinator sees it through `agentWait`).
- Recommendation: change "invisible" to "not reported as a failure; visible only through `agentWait` or a missing report".
- Priority: Low.

---

## === ADVERSARIAL ANALYSIS (Whittaker, active in every panel review) ===

- I can break this specification by **FR-2.3 Sentinel Collision**. The invariant at `specs/orca-worker-contract-spec.md:228` (D1 "cannot misfire on a person") fails when a person's quoted request contains the literal `--unattended`. Concrete attack: `/sc:tdd "design the --unattended contract" --output x.md` switches the run into unattended mode; prompts become blocked results, and under ARCH-4 a reflect `--remediate` auto-accepts. Severity: MAJOR (ambiguous under attack). Follow-up with ARCH-9.
- I can break this specification by **FR-2.4 Sequence**. The invariant at `specs/orca-worker-contract-spec.md:64` (WC-6, a retry must not corrupt the first attempt's output) fails when the coordinator retries with `--retry-of` and the same output directory. Concrete attack: a first attempt writes `return-contract.yaml` with `status: partial`; the retry resumes into the same directory and overwrites the file before the coordinator opens it. Severity: MAJOR (incomplete under attack). Follow-up with ARCH-6.
- I can break this specification by **FR-2.1 Zero/Empty**. The invariant at `specs/orca-worker-contract-spec.md:62` (WC-4 contract on every outcome) fails for a pre-creation STOP where the output directory does not exist yet. Concrete attack: `/sc:workflow` with an empty description stops before it creates `.dev/tasks/to-do/<id>/`; there is no directory to hold the contract. Severity: CRITICAL-by-ARCH-1 (contract cannot be placed); see ARCH-1 and ARCH-2.

---

## Guard Condition Boundary Table

Triggered: the specification contains conditional logic (WC-2 gate resolution, WC-5 status mapping, WC-6 resume-or-fresh, WC-10 threshold, WC-1 readiness fallback). The table covers the four guards with boundary behaviour. Entries marked GAP are propagated as high-priority invariant candidates for `sc:adversarial` AD-1, as the Downstream Propagation rule requires.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | `specs/...-spec.md:63` | Zero/Empty (no report) | `null` | true (failed) | `--outcome failed` | OK |
| WC-5 outcome mapping | `:63` | Typical | `status: succeeded` | false | `--outcome succeeded` | OK |
| WC-5 outcome mapping | `:63` | Minimal (partial) | `status: partial` | false | `--outcome succeeded`; body says partial (`:263`) | OK |
| WC-5 outcome mapping | `:62-63` | Unlisted value | `status: done` or unparseable file | undefined | No rule stated | GAP (REQ-9) |
| WC-5 outcome mapping | `:63` | Sentinel (blocked, no question) | `status: blocked`, `blocked_question` absent | true (failed) | Maps to failed; AC-2.2 needs a question (`:200`) | GAP (REQ-9, minor) |
| WC-4 contract on every outcome | `:62` | Zero/Empty (pre-creation STOP) | no output directory | cannot place file | "stops before any other output exists" with no location | GAP (ARCH-1, ARCH-2) |
| WC-10 heartbeat threshold | `:68` | Boundary (call of exactly 5 min) | 300 s | not "longer than 5 minutes", so unsplit | heartbeat cadence is also 5 min; a 300 s call may miss one | GAP (Medium, follow-up) |
| WC-1 readiness fallback | `:59` | Boundary (fallback near limit) | "well inside" 60 s | undefined | evidence: 30 s passed, above about 45 s failed (`inventory/orca-capabilities.md:49`) | GAP (REQ-6) |
| WC-2 gate, no flag and no default | `:60` | Zero/Empty (flag absent) | no value | true | (c) blocked, stop | OK |

Classes left out: for WC-10 the "Maximum" and "Overflow" classes do not apply, because a tool call has no stated upper bound and the spec does not state one (recorded as GAP at the boundary row). For WC-2 the "Sentinel" class does not apply, because the gate has no sentinel value.

## Pipeline Dimensional Analysis

Not triggered. The flows in the specification are a single worker-to-coordinator hop per Task and a fixed phase sequence. No stage filters, aggregates or fans out the count of items, so no Quantity Flow Diagram is required.

---

## Quality metrics (0-10, requirements and architecture focus)

- Clarity: 6 (defined terms are good; "well inside", "unattended-safe" and "partial" are not measurable).
- Completeness: 6 (the four-phase model is clear; the contract-path, retry, launch-owner and plugin-mirror rules are missing).
- Testability: 5 (most checks are concrete; AC-C1, AC-0.4 step 4 and step 6 cannot pass as written; WC-7, WC-10, WC-12 have no check).
- Consistency: 4 (the contract path, the workflow contract and the outward-default phase conflict with other sections).

---

## Follow-up candidates (Medium and minor; not revised)

- REQ-3 (Section 1.4 vs E3 on the direct route), REQ-4 (no check for WC-7, WC-10, WC-12), REQ-5 (step 6 for source-editing commands), REQ-6 (readiness value and launch owner), REQ-7 (WC-11 vs fixed paths), REQ-8 (WC-9 vs open D4), REQ-9 (status vocabulary), REQ-10 (pr-submit reinterpretation), REQ-11 (pr-submit totals vs D3), REQ-12 (AC-1.1 vs section 3 prose).
- ARCH-5 (WC-3 hand-off mechanism), ARCH-6 (retry directory), ARCH-7 (tasklist row vs inventory B), ARCH-8 (plugin mirror), ARCH-9 (flag parsing), ARCH-10 (E2 and E4 wording), ARCH-11 (WC-2 "invisible").
- Guard table boundary row for WC-10 (exactly 5 minutes).

## Blocking findings (open)

ARCH-1, ARCH-2, ARCH-3, ARCH-4, REQ-1, REQ-2.

## Reviser brief

Blocking finding ids: ARCH-1, ARCH-2, ARCH-3, ARCH-4, REQ-1, REQ-2.

Restated rule (review-loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not to be revised.

Specific instructions:
- ARCH-1: make the contract path a per-command column in section 3, and keep `<output-dir>/return-contract.yaml` only for directory outputs.
- ARCH-2: remove the standalone pre-creation contract from the workflow row at `:92`, or gate it on `--unattended` and name its location.
- ARCH-3: make `--unattended` an error for outward-default commands until P2 or P4 lands, at `:159`.
- ARCH-4: state that remediation is never auto-accepted under `--unattended` at `:88` and `:122`, and state whether Stage 10.5 drops `--remediate`.
- REQ-1: narrow AC-C1 at `:172` so that `WORKER-CONTRACT.md` and the routing-guide Orca section are excluded.
- REQ-2: give AC-0.4 step 4 a per-command form at `:183` and `:194`, or swap troubleshoot out of the P0 set.

## Coverage statement

Covered: the whole candidate; all three inventories; every row of sections 3.1, 3.2 and 4 against its inventory verdict; the phase table and the acceptance checks; the decisions and UNVERIFIED lists. Not covered: any file outside the inventories (see the limits above), the fresh-context reviewers and the VERIFY pass.

verdict: FAIL
