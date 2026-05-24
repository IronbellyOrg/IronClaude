# Feature Characterization — Test Failure Escalation Protocol (TFEP)

**Task:** T02.02 — Characterize TFEP & per-tier flow branching
**Roadmap Item:** R-005
**Donor Catalog Anchor:** D19, D20, D21, D22, D23, D24, D25 (TFEP sub-rows) — see `donor-feature-catalog.md` lines 70-76
**Side of Truth (R-RULE-10):** `src/superclaude/skills/sc-task-protocol/SKILL.md` (canonical) — byte-identical to `.claude/skills/sc-task-protocol/SKILL.md`
**Generated:** 2026-05-15

---

## 1. What It Is

TFEP is a **prohibition-plus-procedure protocol** that intercepts test failures during the Verification Phase of a STANDARD or STRICT `/sc:task` execution and routes them to a *forensic* sub-pipeline instead of allowing the agent to ad-hoc-patch the failing code. It is the donor's structural answer to "what should an agent do the moment a test goes red?", and its answer is *not* "fix it" — it is "halt, freeze, snapshot, escalate, adjudicate, insert remediation tasks, resume under stricter compliance."

TFEP comprises seven coupled sub-features (D19-D25): prohibition rules, permitted exceptions, a pre-implementation test baseline, escalation-trigger detection, a six-step execution flow that invokes an external `/sc:forensic` skill, per-incident reporting, and a three-step escalation budget terminating in FULL STOP.

## 2. How It Works (Mechanism + Entry/Exit Conditions + `file:line` Evidence)

**Mechanism (seven coupled steps):**

1. **Pre-implementation baseline capture** — `src/superclaude/skills/sc-task-protocol/SKILL.md:144-153` (`src/`).
   - Before implementation begins, capture *all existing test files and test function names* via `uv run pytest --collect-only -q` or directory listing; store in memory for the duration of the task. On any failure, classify each failing test as **Pre-existing** (in baseline) or **New** (added by the agent during the task). This classification is the gate for MUST-escalate vs MAY-fix-directly.

2. **Prohibition rules (VIOLATION-level)** — `src/superclaude/skills/sc-task-protocol/SKILL.md:129-142` (`src/`).
   - Three prohibitions apply to STRICT and STANDARD tiers (line 131 explicit): (a) no fixing code in response to test failures without completing TFEP; (b) no modifying test expectations to make failures pass without adversarial validation; (c) no ad-hoc patches derived from test output (the agent must not read a traceback and immediately edit code). Plus a presentation rule (line 142): "Test expectations are wrong" is a *legitimate* adversarial conclusion, but it must be presented to the user — the agent must NOT auto-edit tests.
   - Three carve-outs (lines 137-140) where the agent MAY fix directly without TFEP: single `ImportError`/`NameError` in test scaffolding the agent just wrote (≤2 tests), lint/formatting failures, deprecation warnings.

3. **Escalation trigger detection** — `src/superclaude/skills/sc-task-protocol/SKILL.md:155-168` (`src/`).
   - MUST-escalate triggers (lines 157-160): any pre-existing test fails (primary trigger — indicates regression), 3 or more new tests fail simultaneously (indicates systemic issue), or runtime exceptions in implementation code (TypeError/AttributeError/KeyError outside test scaffolding).
   - Six-row escalation gradient (lines 162-168): repeated failure of the same test cluster after a fix attempt, multi-file blast radius, low-confidence root cause from adversarial debate, unresolved adversarial outcome, second failed retest, cross-domain regression.

4. **Six-step execution flow** — `src/superclaude/skills/sc-task-protocol/SKILL.md:170-218` (`src/`).
   - **Step 1 (lines 174-176):** Halt and freeze — STOP testing, FREEZE implementation, no further code changes.
   - **Step 2 (lines 178-189):** Construct `failure_context` YAML containing `test_names`, `test_files`, `error_output`, `expected_behavior`, `actual_behavior`, `changes_made`, `task_description`, `test_baseline`, `escalation_count`; write to `{output_dir}/context.yaml`.
   - **Step 3 (lines 191-197):** Determine forensic tier from escalation count (1→light/triage, 2→standard, 3→FULL STOP), then invoke `/sc:forensic --tier {tier} --intent triage --caller task-unified --context {context_path} --output {output_dir} --depth quick`.
   - **Step 4 (lines 199-205):** Read `return-contract.yaml`; branch on status: `test_is_wrong==true` → present to user (no auto-fix); `status=="success"` → proceed; `status=="partial"` or `recommended_escalation != "none"` → increment count and return to Step 3; `status=="failed"` → halt and report.
   - **Step 5 (lines 207-212):** Read `tasklist_insertion_path` from contract; insert a `## Failure Remediation Plan (Adjudicated)` heading and tasks BEFORE existing test/verification tasks; preserve original structure (append, do not replace).
   - **Step 6 (lines 214-218):** Resume with `--compliance strict` starting from the inserted remediation tasks; re-run the original test suite; on pass → resolved; on fail → increment `escalation_count` and return to Step 2.

5. **Escalation budget (FULL STOP at trigger 3)** — `src/superclaude/skills/sc-task-protocol/SKILL.md:238-244` (`src/`).
   - Hard bound: 1st trigger → `/sc:forensic --tier light --intent triage` (~5-8K tokens); 2nd → `/sc:forensic --tier standard` (~15-20K tokens); 3rd → **FULL STOP**, report to user, no further fix attempts. This is the same FULL STOP that Step 3 references; redundant statement is intentional.

6. **TFEP incident reporting (escalation artifact)** — `src/superclaude/skills/sc-task-protocol/SKILL.md:220-236` (`src/`).
   - After every TFEP resolution (success OR escalation), produce `tfep-incident-report.md` containing **Trigger, Escalation count, Failing tests, Root cause, Solution, Outcome, Forensic artifacts** (path to `{output_dir}`). Committed to git alongside other forensic artifacts (line 236).

**Entry conditions:**
- The task has been classified STRICT or STANDARD (TFEP rule prefix at `src/superclaude/skills/sc-task-protocol/SKILL.md:131`, `src/`: "These rules apply to ALL compliance tiers that run tests (STRICT, STANDARD)" — LIGHT and EXEMPT skip verification entirely, see Verification Routing table at `src/superclaude/skills/sc-task-protocol/SKILL.md:114-119`, `src/`).
- Execution has reached the Verification Phase (`src/superclaude/skills/sc-task-protocol/SKILL.md:110-119`, `src/`) and at least one test has failed.
- At least one of: a pre-existing test failure, ≥3 new test failures, or a runtime exception in implementation code (`src/superclaude/skills/sc-task-protocol/SKILL.md:157-160`, `src/`). Otherwise the failure is either inside the permitted-exception carve-out or below the threshold, and TFEP does not engage.

**Exit conditions (three terminal states):**
- **Resolved:** Step 6 re-runs the original test suite and all tests pass → produce `tfep-incident-report.md` (Outcome: success), continue task execution (`src/superclaude/skills/sc-task-protocol/SKILL.md:217`, `src/`).
- **Escalated to next budget tier:** Step 4 returned `partial` or `recommended_escalation != "none"`, OR Step 6 re-test still failed → increment `escalation_count` and re-enter Step 3 (`src/superclaude/skills/sc-task-protocol/SKILL.md:204, 218`, `src/`).
- **FULL STOP:** `escalation_count == 3` → halt execution, report to user, produce `tfep-incident-report.md` (Outcome: failed) (`src/superclaude/skills/sc-task-protocol/SKILL.md:195, 243`, `src/`).

## 3. What It Produces (Escalation Artifacts)

TFEP produces five distinct artifacts; each is named and pathed in the donor source:

1. **`{output_dir}/context.yaml`** — failure-context package written in Step 2 (`src/superclaude/skills/sc-task-protocol/SKILL.md:189`, `src/`). Schema: nine fields (test_names, test_files, error_output, expected_behavior, actual_behavior, changes_made, task_description, test_baseline, escalation_count).

2. **`{output_dir}/return-contract.yaml`** — consumed in Step 4 (`src/superclaude/skills/sc-task-protocol/SKILL.md:200`, `src/`). Produced by `/sc:forensic`, NOT by TFEP itself. Carries `status`, `test_is_wrong`, `recommended_escalation`, `tasklist_insertion_path` fields.

3. **Tasklist mutation — `## Failure Remediation Plan (Adjudicated)` block** — inserted in Step 5 (`src/superclaude/skills/sc-task-protocol/SKILL.md:210-212`, `src/`). Located inside the *current tasklist* (the running task file); positioned BEFORE existing test/verification tasks.

4. **`tfep-incident-report.md`** — per-incident markdown report (`src/superclaude/skills/sc-task-protocol/SKILL.md:222-234`, `src/`). Schema: seven fields (Trigger, Escalation count, Failing tests, Root cause, Solution, Outcome, Forensic artifacts). Committed to git (`src/superclaude/skills/sc-task-protocol/SKILL.md:236`, `src/`).

5. **In-memory test baseline** — produced in Step 0 / pre-implementation (`src/superclaude/skills/sc-task-protocol/SKILL.md:144-149`, `src/`). Schema: a list of `(test_file, test_function_name)` tuples. Persists for the duration of the task; consumed at every failure classification (`src/superclaude/skills/sc-task-protocol/SKILL.md:150-152`, `src/`).

## 4. What Invokes It

- **Primary trigger:** test failure during the Verification Phase. Per the routing table at `src/superclaude/skills/sc-task-protocol/SKILL.md:114-119` (`src/`), STRICT routes to sub-agent (quality-engineer) and STANDARD routes to direct test execution — both produce test results that, on failure, can engage TFEP. LIGHT and EXEMPT skip verification, so TFEP cannot engage on those tiers.
- **Engagement is conditional on triggers** (`src/superclaude/skills/sc-task-protocol/SKILL.md:155-160`, `src/`) — a single failing new test below the 3-test threshold and outside the permitted-exception carve-out does NOT engage TFEP; the agent proceeds normally.
- **`/sc:forensic` (external skill)** is the downstream invokee, not the invoker. The donor names it but never defines it; verification (`find /config/workspace/IronClaude/src/superclaude -name "*forensic*"`) confirms no `sc-forensic` skill directory exists in the repo as of 2026-05-15.
- **The command-side dispatch (D10)** at `src/superclaude/commands/task.md:99-100` (`src/`) is the upstream invocation of the skill that *contains* TFEP — only STANDARD/STRICT cases reach `Skill sc:task-protocol`, so TFEP is implicitly gated by the command's tier branching.
- **The command-side Boundaries list** at `src/superclaude/commands/task.md:160-161` (`src/`) names TFEP explicitly: "Enforce TFEP (Test Failure Escalation Protocol) when test failures meet escalation thresholds; Block ad-hoc fixes when pre-existing tests fail during task execution." The Boundaries list is doc-spec; the binding semantics live in the skill.

## 5. What It Depends On

- **The tier classification model (D09) and per-tier branching (D10/D15).** TFEP applies only to STRICT and STANDARD, so it depends on a classifier that produces those tier labels and a dispatch that routes them into the protocol skill (`src/superclaude/skills/sc-task-protocol/SKILL.md:131`, `src/`).
- **The Verification Phase routing table** at `src/superclaude/skills/sc-task-protocol/SKILL.md:114-119` (`src/`). Without verification running, no test failure can be detected, and TFEP has no entry point.
- **An external `/sc:forensic` skill.** TFEP Step 3 invokes `/sc:forensic --tier {tier} --intent triage --caller task-unified --context {context_path} --output {output_dir} --depth quick` (`src/superclaude/skills/sc-task-protocol/SKILL.md:196`, `src/`). This skill does **not exist in the repo** — verified by absence of `src/superclaude/skills/sc-forensic/` and absence of `src/superclaude/commands/forensic.md`. TFEP is partially unimplemented today; the donor side runs the prohibition + halt + report steps but the forensic invocation has no callee.
- **A writable tasklist with insertable structure.** Step 5 inserts `## Failure Remediation Plan (Adjudicated)` (`src/superclaude/skills/sc-task-protocol/SKILL.md:210`, `src/`). On `/task`, the only sanctioned insertion slot is DYNAMIC CONTENT MARKER sections at `src/superclaude/skills/task/SKILL.md:114, 150, 156` (`src/`); F4 modification restrictions at `src/superclaude/skills/task/SKILL.md:144-158` (`src/`) prohibit inserting headings elsewhere.
- **A pytest collection runtime.** Baseline capture uses `uv run pytest --collect-only -q` (`src/superclaude/skills/sc-task-protocol/SKILL.md:148`, `src/`). Projects without pytest, or where the suite is collected differently, must adapt this step.
- **An `output_dir` convention.** Both `context.yaml` and `return-contract.yaml` paths assume a per-task output directory (`src/superclaude/skills/sc-task-protocol/SKILL.md:189, 200`, `src/`). The `/sc:task` donor relies on the conversation transcript and the protocol skill's emission discipline to define this path; no explicit `output_dir` constant is defined in the donor source.

## 6. Standalone Value Claim

**Claim:** TFEP converts the *most common* failure mode of agentic code change — "test goes red, agent reads traceback, agent patches code, traceback changes, agent patches again, repeat until tests are green or context exhausted" — into a *halt-snapshot-adjudicate-resume* loop with a hard three-strike budget. The value is bounded specifically by these mechanisms:

1. **Prevents test-overfitting regressions.** The prohibition on modifying test expectations to make failures pass (`src/superclaude/skills/sc-task-protocol/SKILL.md:134, 142`, `src/`) closes the most expensive failure mode where an agent "fixes" a failing test by weakening its assertion, masking a real regression. For a STRICT change in `auth/` or `migrations/`, this is the difference between a green CI run that hides a security regression and a halt with a forensic report.
2. **Bounds runaway escalation.** The three-step budget (`src/superclaude/skills/sc-task-protocol/SKILL.md:238-244`, `src/`) caps total fix-loop spend at ~25-30K tokens before FULL STOP. Without this bound, the same agent loop can spend the entire context window cycling through ad-hoc patches.
3. **Produces a per-incident artifact.** `tfep-incident-report.md` (`src/superclaude/skills/sc-task-protocol/SKILL.md:220-234`, `src/`) creates an auditable trail committed to git — postmortem evidence that a halt happened, what triggered it, what was decided. Without this, the conversation transcript is the only record.
4. **The Pre-existing vs New classification turns a heuristic ("was this a regression?") into a deterministic decision.** Baseline + classification at `src/superclaude/skills/sc-task-protocol/SKILL.md:144-152` (`src/`) means an agent cannot rationalise away a regression as "a flaky test."

For a session with 5 STRICT-tier changes that each touch test code, the value is the 5 averted ad-hoc-patch loops, multiplied by the cost-per-loop saved (~10-50K tokens) — i.e. 50-250K tokens of avoided overspend per session, *if and only if* test failures actually occur and at least one of them would have triggered an ad-hoc patch.

**Non-value condition (R-RULE-04, concrete, not boilerplate):**

The value claim does NOT hold under any of these specific conditions:

- **`/sc:forensic` does not exist in the repo today.** Verified by absence: no `src/superclaude/skills/sc-forensic/` directory, no `src/superclaude/commands/forensic.md` file. TFEP Steps 3-6 (`src/superclaude/skills/sc-task-protocol/SKILL.md:191-218`, `src/`) all depend on the forensic invocation returning a `return-contract.yaml`. With no callee, the protocol halts at Step 3 indefinitely or produces nothing — every "TFEP-engaged" run today either silently degrades to the prohibition-and-halt subset (Steps 1-2) or invokes a non-existent skill. The full-loop value claim above requires `/sc:forensic` to be authored first; until then, TFEP delivers prohibition + baseline + halt + incident-report only, which is *less* than half of its stated capability.
- **Sessions where verification doesn't run.** TFEP applies only to STRICT and STANDARD (line 131); LIGHT and EXEMPT skip verification (`src/superclaude/skills/sc-task-protocol/SKILL.md:118-119`, `src/`). For a 10-item tasklist of LIGHT typo fixes and EXEMPT explanations, TFEP delivers zero value because no test ever runs.
- **Sessions where every test failure falls into the permitted-exception carve-out.** Lines 137-140 list three carve-outs (single ImportError/NameError in just-written scaffolding ≤2 tests, lint/formatting, deprecation warnings). For a refactoring session that only triggers import or lint failures, TFEP never engages — and the value claim about preventing ad-hoc patches is irrelevant because the agent is *permitted* to fix directly.
- **Sessions without a writable tasklist or without an `output_dir` convention.** Step 5 tasklist insertion (`src/superclaude/skills/sc-task-protocol/SKILL.md:207-212`, `src/`) requires a tasklist that can be appended to with a new heading; the donor `/sc:task` invocation surface is prompt-driven and has no persistent tasklist — meaning even the donor side currently relies on an undefined tasklist context. On `/task`, the F4 restrictions at `src/superclaude/skills/task/SKILL.md:144-158` forbid heading insertion outside DYNAMIC CONTENT MARKER sections, so direct port of Step 5 is structurally impossible.

## 7. Coupling Cost Claim

**Claim:** Attaching TFEP to `/task` requires the recipient to take on **all six** of the following concrete burdens; partial adoption (e.g. taking the prohibition rules without the forensic loop) collapses the protocol's value to the non-value-condition subset above.

1. **A pre-EXECUTE baseline-capture step that hooks into `/task`'s First Item Protocol.** `/task`'s First Item Protocol at `src/superclaude/skills/task/SKILL.md:100-102` (`src/`) only flips status to "🟠 Doing" and sets `start_date` — it does not snapshot tests. TFEP requires adding a step that runs `uv run pytest --collect-only -q` (or equivalent) before the first F1 iteration and persists the result for the task's duration. The recipient must extend the First Item Protocol *and* invent in-memory or on-disk persistence for the baseline (the donor stores "in memory for the duration of the task," `src/superclaude/skills/sc-task-protocol/SKILL.md:149`, `src/`).

2. **A test-failure interception point that hooks into `/task`'s Error Handling.** `/task`'s Error Handling at `src/superclaude/skills/task/SKILL.md:170-179` (`src/`) classifies blockers as recoverable vs unrecoverable and logs them — it does NOT distinguish "test failure" from other blockers. TFEP requires extending the Error Handling extension point with a `is_test_failure` branch that pulls the baseline and classifies each failing test as Pre-existing/New, then evaluates the three MUST-escalate triggers (`src/superclaude/skills/sc-task-protocol/SKILL.md:157-160`, `src/`). The recipient must add a new classification dimension to its blocker model.

3. **A `/sc:forensic` skill must be authored.** The forensic skill does not exist (verified by directory absence). TFEP Step 3 (`src/superclaude/skills/sc-task-protocol/SKILL.md:191-197`, `src/`) cannot be ported without authoring a callee that accepts the `--tier/--intent/--caller/--context/--output/--depth` flag set and produces a `return-contract.yaml` with the fields Step 4 expects (`status`, `test_is_wrong`, `recommended_escalation`, `tasklist_insertion_path`). This is a new skill of unspecified size; it is *not* a recipient burden in the strict sense, but the recipient cannot benefit from TFEP without it.

4. **Tasklist-insertion capability that fits inside `/task`'s F4 restrictions.** F4 at `src/superclaude/skills/task/SKILL.md:144-158` (`src/`) permits adding items only inside DYNAMIC CONTENT MARKER sections (`src/superclaude/skills/task/SKILL.md:114, 150, 156`, `src/`); inserting a top-level `## Failure Remediation Plan (Adjudicated)` heading is **prohibited by F4** as currently written. The recipient must either (a) author a DYNAMIC CONTENT MARKER convention for remediation blocks, (b) extend F4 to permit a single named heading insertion, or (c) re-shape Step 5 to insert remediation items *inside* an existing marker section rather than as a new heading. Each choice changes the recipient's mutation contract.

5. **An `output_dir` convention for `context.yaml` and `tfep-incident-report.md`.** TFEP writes `{output_dir}/context.yaml` (`src/superclaude/skills/sc-task-protocol/SKILL.md:189`, `src/`) and the per-incident report (`src/superclaude/skills/sc-task-protocol/SKILL.md:222`, `src/`) — both presume a per-task output directory. `/task` has no `output_dir` field in its required frontmatter schema (`src/superclaude/skills/task/SKILL.md:69`, `src/`) and no convention for where per-task artifacts land. The recipient must extend the schema OR adopt a convention (e.g. `<task-file-parent>/tfep/`) that is currently unwritten.

6. **A FULL-STOP and resume-under-strict semantic compatible with `/task`'s F1 loop control.** Step 6 (`src/superclaude/skills/sc-task-protocol/SKILL.md:214-218`, `src/`) "Resume execution with `--compliance strict` starting from the inserted remediation tasks." On `/task`, there is no `--compliance` flag and no per-item tier upgrade — the F1 loop is single-track. The recipient must either (a) ignore the strict-resume directive (lose the value claim about safety on remediation), (b) invent a per-item tier annotation that escalates Phase-Gate QA stance, or (c) couple TFEP to the per-tier branching donor feature (D10/D15) so that the recipient inherits a tier model alongside TFEP. Option (c) is the only one preserving the donor's semantic — meaning TFEP cannot be transferred in isolation; it inherits a *transitive* coupling to D09/D10/D15.

**Net coupling cost:** the recipient must extend its First Item Protocol (1), its Error Handling extension point (2), accept a missing-skill dependency (3), reshape its F4 mutation contract (4), invent an `output_dir` convention (5), and inherit a tier model to support FULL-STOP-and-resume-under-strict (6) — six distinct extensions, with the third creating an external authoring blocker and the sixth creating transitive coupling to three other donor features.

---

## Cross-Reference

- D19, D20, D21, D22, D23, D24, D25 in `donor-feature-catalog.md` — primary anchor sub-rows.
- D10 (command-side per-tier dispatch) — transitively required for TFEP entry, since LIGHT/EXEMPT skip verification.
- D15 (skill-side per-tier execution workflows) — `Verification Phase` (`src/superclaude/skills/sc-task-protocol/SKILL.md:110-119`, `src/`) is where TFEP attaches.
- D16 (verification routing table) — defines which tiers run tests at all, gating TFEP applicability.
- D17 (Critical Path Override) and D18 (Trivial Path Override) — affect verification routing and therefore affect whether TFEP can engage.
- `recipient-extension-points.md` row 8 (Error Handling at `src/superclaude/skills/task/SKILL.md:170-179`) — primary attach surface on the recipient side.
- `recipient-extension-points.md` row 10 (Phase-Gate QA at `src/superclaude/skills/task/SKILL.md:182-211`) — alternate attach surface for the verification-failure interception step.
- `recipient-extension-points.md` rows N1 (F2 Prohibited Actions) and N2 (F4 Task File Modification Restrictions) — the negative-space constraints that Step 5 tasklist insertion currently violates.
