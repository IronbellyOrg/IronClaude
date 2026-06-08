# R2: MDTM Template & Project Conventions Research

**Topic:** Template & Examples + Patterns & Conventions
**Scope:** MDTM template 02, project CLAUDE.md (project + global), Makefile, prior STRICT-tier task examples
**Status:** Complete
**Track Goal:** Build MDTM task file for OVM proposal implementation (skill amendment to sc-reflect-protocol)

---

## Critical Context Note: Two Repo Confusion Avoided

The user's global `/config/.claude/CLAUDE.md` (lines 14-30) describes the **SuperClaude framework repo** project structure with `src/superclaude/` → `.claude/` sync via `make sync-dev` / `make verify-sync`. This is **NOT** the current working repo.

- `/config/workspace/Coder/` (the cwd) is an IronClaude / Coder.com templates repo. Verified: **no Makefile, no `src/superclaude/` directory** (Bash `test -d /config/workspace/Coder/src/superclaude` returned `NO superclaude src`).
- The OVM proposal target file `sc-reflect-protocol/SKILL.md` lives at `/config/.claude/skills/sc-reflect-protocol/SKILL.md` — a user-global skill, NOT inside the Coder repo. Verified: `ls /config/.claude/skills/sc-reflect-protocol/` shows `SKILL.md`, `refs/`, `__init__.py`.
- The Coder repo's project-level `/config/workspace/Coder/CLAUDE.md` (L7) states: **"Validation should be done via the .github actions. One off validation scripts should be avoided moving forward"** — i.e. validation runs via `.github/workflows/*.yml`, not via Makefile targets.

**Implication for the MDTM task:** The task amends a file outside the Coder repo tree. Any edit-then-validate loop must rely on either (a) `.github/workflows/markdownlint.yml` for prose checks on Coder-tracked files, or (b) a manual / agent-driven self-check since the skill file lives outside any CI-watched path. The "src → .claude sync" convention does NOT apply: `/config/.claude/skills/sc-reflect-protocol/SKILL.md` is the edit target directly.

---

## MDTM Template 02 Structure

Source: `/config/.claude/templates/workflow/02_mdtm_template_complex_task.md` (1205 lines total). Template has two parts inside a single HTML comment block.

### Frontmatter Fields (lines 1-44)
Verbatim field list with example values:
- `id: "TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"` (L2)
- `title:` (L3), `description:` (L4) — verbose multi-clause description expected
- `status: "🟡 To Do"` (L5) — emoji-prefixed states: 🟡 To Do, 🟠 Doing, 🟢 Done, ⚪ Blocked (see F5/I11 L450, L569)
- `type: "📝 Documentation"` (L6) — emoji-prefixed type tag (other observed: `"🛠️ CI / Test"`)
- `priority: "🔼 High"` (L7)
- `created_date:`, `updated_date:` (L8-9) — `YYYY-MM-DD`
- `assigned_to:` (L10) — typically `"rf-task-executor"` in prior tasks
- `autogen: false`, `autogen_method: ""` (L11-12)
- `coordinator: orchestrator` (L13)
- `parent_task:` (L14), `depends_on:` list (L15-17)
- `related_docs:` (L18-24) — list of `{path, description}` objects
- `tags:` (L25-29) — kebab-case list
- `template_schema_doc: ""` (L30) — prior tasks populate with `".claude/templates/workflow/02_mdtm_template_complex_task.md"` (e.g. TASK-FU-SC-REFLECT-DOC-HYGIENE-BATCH L33, TASK-FU-SC-REFLECT-PR73-1 L37)
- `estimation: ""` (L31) — observed: `"S"`, `"M"`
- `sprint:`, `due_date:`, `start_date:`, `completion_date:`, `blocker_reason:` (L32-36)
- `ai_model:`, `model_settings:` (L37-38)
- `review_info: {last_reviewed_by, last_review_date, next_review_date}` (L39-42)
- `task_type: static` (L43) — `static` or `dynamic` (I6 at L526-536)

**Notable absence:** No `compliance_tier:` / `task_tier:` / `tier:` frontmatter field exists. STRICT-tier is declared elsewhere (see "STRICT-Tier Encoding" section below).

### Mandatory Sections in PART 2 (lines 890-1204)
In order:
1. `# [Task Title]` (L890)
2. `## Task Overview` (L892) — comprehensive description
3. `## Key Objectives` (L896) — numbered list of concrete outcomes
4. `## Prerequisites & Dependencies` (L904)
   - `### Parent Task & Dependencies` (L906)
   - `### Previous Stage Outputs (MANDATORY INPUTS)` (L914) — informational, no checkboxes
   - `### Handoff File Convention` (L928) — declares `phase-outputs/` subdirs
   - `### Frontmatter Update Protocol` (L943) — checkpoint rules
5. `## Detailed Task Instructions` (L954) — wraps all phases
   - `### Phase 1: Preparation and Setup` (L1012) — Step 1.1 status update, Step 1.2 create handoff dirs
   - `### Task-Specific Context Files` (L1052) — informational
   - `### Phase 2: [Main Execution]` (L1063) — pattern items per L1-L6
   - `### Phase Gate: Quality Verification` (L1090) — `Step PG.1` QA gate item (per I15-I16)
   - `### Phase [N]: Testing & Verification` (L1098) — required if code-modifying (I18 L637)
   - `### Phase 3: [Review and Quality Assessment]` (L1106)
6. `## Post-Completion Actions` (L1118) — 4 standard items (verify outputs by Glob, run tests, create task summary, update frontmatter)
7. `## Task Log / Notes 📋` (L1128)
   - `### Task Summary` (L1130)
   - `### Execution Log` (L1156)
   - `### Phase 1 - [Phase Name] Findings` (L1166)
   - `### Phase 2 - [Phase Name] Findings` (L1176)
   - `### Phase 3 - [Phase Name] Findings` (L1185)
   - `### Phase Gate Findings` (L1187)
   - `### Follow-Up Items Identified` (L1191)
   - `### Deviations from Process` (L1197)

### Item Format (B2 Self-Contained Pattern, L142-149)
Every checklist item MUST be a single paragraph containing all 6 elements:
1. **Context Reference + WHY** — file paths and why context needed
2. **Action + WHY** — what to do and why
3. **Output Specification** — exact file name, location, content, template
4. **Integrated Verification** — `"ensuring..."` clause; no fabrication; document negative evidence
5. **Evidence on Failure Only** — log to task notes only when blocked
6. **Explicit Completion Gate** — boilerplate: `"This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."`

Canonical example: L157 (the spec quotes a full ~480-character single-paragraph item ending with `"...Once done, mark this item as complete."`).

### Completion-Gate Phrasing (verbatim)
Two related boilerplates appear together at the end of every item:
- Blocker clause (J1, L660-663): `"If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete."`
- Done clause: `"Once done, mark this item as complete."`

### L-Pattern Handoff Types (L711-836)
Template 02 EXTENDS template 01 with intra-task handoff patterns:
- **L1 Discovery** (L737) — Glob/Read scan, writes to `phase-outputs/discovery/`
- **L2 Build-from-Discovery** (L749) — reads discovery + source, creates deliverable
- **L3 Test/Execute** (L761) — Bash command, captures raw + summary to `phase-outputs/test-results/`
- **L4 Review/QA** (L773) — produces structured PASS/FAIL verdict to `phase-outputs/reviews/`
- **L5 Conditional-Action** (L785) — branches on prior result; MUST handle BOTH branches
- **L6 Aggregation** (L799) — Glob-discovers and consolidates all phase-outputs to `phase-outputs/reports/`
- Pattern selection guide at L811-836 with phase composition recipes (Discovery→Build→Review; Build→Test→Fix; Full Lifecycle).

### PER_PHASE QA Gate Encoding (I15-I16 + M1-M2, L599-624 + L843-860)
Every task with 2+ phases MUST include phase-gate QA between any phase and its dependent successor. Encoded as 2-3 items:
1. **Aggregation item** (L6 pattern) — collects phase outputs
2. **QA Agent Spawn item** — spawns `rf-qa` (structural) or `rf-qa-qualitative`; specifies agent name, phase type, input file paths, output report path, verdict handling, error clause
3. **Conditional Proceed item** (L5 pattern) — IF PASS → proceed; IF FAIL → fix cycle

Fix-cycle ceilings (I16 L612-620):
| Gate Type | Max Fix Cycles | After Max |
|-----------|----------------|-----------|
| research-gate | 3 | HALT + escalate to user |
| synthesis-gate | 2 | unresolved → Open Questions |
| report-validation | 3 | HALT |
| task-integrity | 2 | unresolved → Open Questions |
| Any qualitative gate | 3 | HALT |

### Anti-Patterns (FORBIDDEN)
From B5 (L164-184) and E2-E4 (L294-388):
- Standalone "read context" items with no output (L166-170)
- Multi-line / bulleted checklist items — must be single paragraph (L175-180)
- Parent checkboxes with child checkboxes (E2 L295, L327-333)
- Summary checkbox before its components (L335-341)
- Separate verification items — verification MUST be embedded as `"ensuring..."` clause (C3 L219, I12 L573)
- Backward references / "go back and update" (E3 L350-365)
- Checkboxes next to step numbers (E4 L368) — step numbers are bold headers
- REMINDER blocks between items (E4 L371) — worker agents only see batch items, not surrounding text

---

## Project Conventions

### Global User Rules (`/config/.claude/CLAUDE.md`)
- **UV only for Python** (L5) — never `python -m`, `pip install`, `python script.py`
- **Parallel by default** (Core Rules #2) — batch independent tool calls
- **Confidence check ≥90%** before any action-suggesting reply (Core Rules #3)
- **Feature branches only; never commit to main/master** (Core Rules #4)
- **Component edits source-of-truth rule:** "`src/superclaude/` → `make sync-dev` → `.claude/`; never reverse without syncing back" (Core Rules #6). **This applies to the SuperClaude framework repo, NOT to Coder. The OVM target `/config/.claude/skills/sc-reflect-protocol/SKILL.md` is edited directly since no SuperClaude `src/` mirror exists in this environment.**
- **Auggie first** (Core Rules #9) — call `codebase-retrieval` before significant edits
- **S1-S5 content-signal triggers** (`/config/.claude/CLAUDE.md` Context-freshness section) — mandatory re-Read before citing file:line, asserting cross-file claims, or quoting paths/IDs

### Project Rules (`/config/workspace/Coder/CLAUDE.md`)
- **L7: "Validation should be done via the .github actions. One off validation scripts should be avoided moving forward."** — explicit prohibition on bespoke validators; defer to CI workflows.
- **Shell / CWD Discipline** (L9-14): no `cd`; use `git -C`, `make -C`, `npm --prefix`, absolute paths. Subshell `( cd ... && ... )` if unavoidable.
- **Secrets discipline post-PR-#57** (L16-35): never write env captures to tracked paths; Read env-file diffs in FULL before commit (no grep-sweeps); don't merge with failing `P-7 secret scan` check.

### Source-of-Truth Rule for the OVM Target
Edit `/config/.claude/skills/sc-reflect-protocol/SKILL.md` directly. There is no Makefile sync step in this environment to invoke (no SuperClaude `src/` tree present at `/config/workspace/Coder/src/superclaude` — verified missing). The "no-edit-`.claude/`-directly" rule from the global CLAUDE.md presumes a SuperClaude framework checkout; that checkout is not present here, so the in-place edit is the only available path.

---

## Makefile Targets

**NO MAKEFILE EXISTS** in `/config/workspace/Coder/`. Verified:
- `test -f /config/workspace/Coder/Makefile && echo "EXISTS" || echo "MISSING"` → `MISSING`
- `find /config/workspace/Coder -maxdepth 3 -name "Makefile"` → empty

The global CLAUDE.md (L33-43) references SuperClaude-repo Makefile targets:

| Target (global CLAUDE.md ref) | Purpose | Available in Coder? |
|---|---|---|
| `make dev` | Install editable + dev deps | **No** |
| `make test` | Full test suite | **No** |
| `make sync-dev` | `src/superclaude/{skills,agents,commands}` → `.claude/` | **No (no src/ mirror)** |
| `make verify-sync` | Confirm src/ and .claude/ match | **No** |
| `make lint && make format` | Code style | **No** |
| `make reflect-eval` / `make reflect-eval-quick` | Reflect eval workspace check | **No** |
| `superclaude sprint run <tasklist-index.md>` | Sprint pipeline | **No (no superclaude CLI installed in Coder cwd)** |

### Validation Surfaces Available in Coder
CI workflows under `/config/workspace/Coder/.github/workflows/`:
| Workflow | Trigger | Pass Signal | Fail Signal |
|---|---|---|---|
| `markdownlint.yml` | PR with `.md` changes, push to main | markdownlint-cli2 exits 0 with config at `.markdownlint-cli2.yaml` (L13 of workflow) | non-zero exit; structural MD issues (broken fences, heading skips, link errors) |
| `gitleaks.yml` (P-7) | every PR + push to main | `gitleaks detect` exits 0; **release-blocker** per workflow L3 | non-zero exit; secret detected; blocks merge per branch protection (project CLAUDE.md L32-35) |
| `coder-ci-validate.yml` | workflow_call from detect/push workflows | dind-sidecar arm passes (REQUIRED merge gate); sysbox-runc informational | dind-sidecar arm fail → blocks merge |
| `coder-ci-aidev02-contract.yml` | PR/push affecting AIDev02 template | all `test-*.sh` contract tests exit 0 | any T1-T17 (plus pending T18 per PR73-1) script exits non-zero |
| `coder-ci-detect.yml` | PR/push entry point | dispatches push + validate jobs based on changed paths | dispatch failure |
| `coder-template-main.yml` | main-branch template smoke | template deploys clean | deploy failure |

**Implication for OVM task validation:** since the edit target lives outside `/config/workspace/Coder/`, none of these CI workflows will lint or check `/config/.claude/skills/sc-reflect-protocol/SKILL.md`. The MDTM task MUST embed its own verification (per template B2/C3) — likely an L3 (Test/Execute) item invoking `markdownlint-cli2` directly on the edited file, or a manual structural self-check item (Read-and-verify checklist) since CI cannot enforce.

---

## STRICT-Tier Encoding

**KEY FINDING: STRICT is NOT a frontmatter field.** It is declared via an HTML comment classification block emitted by the `/sc:task` command at execution time.

Source: `/config/.claude/commands/sc/task.md`:
- L56: `"VALID TIERS ONLY: The ONLY valid TIER values are: STRICT, STANDARD, LIGHT, EXEMPT"`
- L62-68 — emit verbatim at task execution start:
  ```text
  <!-- SC:TASK-UNIFIED:CLASSIFICATION -->
  TIER: [STRICT|STANDARD|LIGHT|EXEMPT]
  CONFIDENCE: [0.00-1.00]
  KEYWORDS: [matched keywords or "none"]
  OVERRIDE: [true|false]
  RATIONALE: [one-line reason]
  <!-- /SC:TASK-UNIFIED:CLASSIFICATION -->
  ```
- L73-77: STRICT triggers — security, authentication, authorization, database, migration, refactor, breaking change, encrypt, token, session, oauth. Context boosters: >2 files (+0.3), security paths (+0.4).
- L101-102: For STANDARD/STRICT, execution invokes `> Skill sc:task-protocol` (full protocol).
- L169: `"Spawn verification agents for STRICT tier tasks"`

### How STRICT manifests in prior task files
Observed in `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-CI-GATE-REMEDIATION-20260529-190118/TASK-RF-CI-GATE-REMEDIATION-20260529-190118.md` (grep):
- L394: `"Task started: ... via /sc:task STRICT execution with --persona-devops --persona-qa --serena --seq"`
- L441, L486, L520: `"Owner-recorded ... via /sc:task STRICT execution interactive decision"`

So STRICT-tier tasks document the tier in the **Execution Log** of the Task Log / Notes section as freeform prose, not in YAML frontmatter. The classification HTML block is emitted at runtime by the worker agent.

### QA Gate Item Template (B2-compliant, per I15 L599-608)
A QA gate item is a single self-contained checklist item that MUST include:
- Agent to spawn (`rf-qa` or `rf-qa-qualitative`)
- Phase type (research-gate | synthesis-gate | report-validation | task-integrity | qualitative)
- Input file paths
- Output report path under `phase-outputs/reviews/`
- Verdict handling (proceed on PASS; fix cycle on FAIL with max-cycles from I16 table)
- Error-handling blocker clause

Example skeleton from template L1096:
```
- [ ] [QA GATE ITEM — Replace with actual QA agent spawn item following B2 pattern.
  Example: "Spawn rf-qa in [phase-type] mode to verify all Phase 2 outputs at [paths],
  ensuring the agent writes its report to [output-path] and returns a PASS/FAIL verdict.
  If FAIL, read the report, address all findings in the relevant Phase 2 output files,
  then re-spawn rf-qa in fix-cycle mode (max [N] cycles per I16). If unable to complete
  due to agent spawn failure, log the blocker in ### Phase Gate Findings below, then
  mark this item complete."]
```

### Per-Phase Verification Pattern (I17 L626-635)
**Post-Completion Validation Protocol** items appear in `## Post-Completion Actions` BEFORE the frontmatter status update:
1. Verify all `- [ ]` items marked `- [x]` (no skips)
2. Verify all output files exist on disk via Glob
3. Blocker entries in Task Log have resolution notes
4. If source code modified: relevant tests pass

Template lines 1120-1126 ship four standard Post-Completion items: Glob output verification, test-suite re-run, Task Summary creation, frontmatter Done update.

### Testing Requirements for Code-Modifying Tasks (I18 L637-646)
If a task modifies source code (not docs, not config), the orchestrator MUST include ≥1 testing item that:
1. Specifies the test command
2. Defines pass criteria
3. Specifies test-results capture path under `phase-outputs/test-results/`
4. Follows B2 self-contained pattern (use L3 Test/Execute pattern)

**Application to OVM task:** `SKILL.md` is documentation, not source code — so I18 does not strictly require unit tests. But the OVM proposal's substance is *operational verification gap closure* in the reflect protocol, so the MDTM task SHOULD include an L3 item that exercises the amended SKILL.md against a known-good test case (e.g. run `/sc:reflect` on a fixture) to confirm the amendment behaves as intended.

---

## Prior-Task Examples

### Example 1: `TASK-FU-SC-REFLECT-DOC-HYGIENE-BATCH-20260531-040140`
Path: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-FU-SC-REFLECT-DOC-HYGIENE-BATCH-20260531-040140/TASK-FU-SC-REFLECT-DOC-HYGIENE-BATCH-20260531-040140.md`

What it does: Applies 13 doc-hygiene fixes across 6 source PRs after they merge. Each fix has a `change:` directive + `acceptance:` grep command embedded verbatim from a normalized proposals spec.

Item structure observations (L1-118 read):
- Frontmatter follows template 02 exactly (L1-47)
- `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"` (L33)
- `task_type: static` (L46)
- `depends_on:` list encodes PR-merge gating with synthetic IDs `"PR-68-MERGED"` etc. (L15-22) — pattern for upstream-dependency tasks
- `related_docs:` (L23-26) cites the normalized proposals spec and the reflect-pre REPORT.md
- Tags include `"sc-reflect"`, `"follow-up"`, `"post-merge"`, `"batch-13"` (L28-32)
- `## Task Overview` (L51-58) is multi-paragraph, explaining the precondition gate and exclusion criteria
- Handoff subdirs map per-fix outputs to `discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/` (L100-105) consistent with template L933-939
- Strict precondition encoded as Step 1.3 PR-merge gate (referenced L57) using `gh pr view <n> --json state`

### Example 2: `TASK-FU-SC-REFLECT-PR73-1-DOCKER-CLI-CI-GATE-20260531-040153`
Path: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-FU-SC-REFLECT-PR73-1-DOCKER-CLI-CI-GATE-20260531-040153/TASK-FU-SC-REFLECT-PR73-1-DOCKER-CLI-CI-GATE-20260531-040153.md`

What it does: Adds a CI contract test asserting docker CLI presence in built AIDev02 image. This IS a STRICT-tier task by topic (CI gate / contract test addition).

Frontmatter observations:
- `type: "🛠️ CI / Test"` (L7) — different emoji-type than DOC-HYGIENE's `📝 Documentation`
- `priority: "🔼 High"` (L8)
- `depends_on:` uses free-text marker `"PR-73 (must be merged to main before this task runs)"` (L18) — variant style of dependency gating
- `related_docs:` (L19-30) includes a **pattern-reference** doc (`test-1-tool-floor.sh`) — pattern: when a task creates a new file modeled on an existing one, cite the model in related_docs
- `tags:` include `"remediation"`, `"ci-gate"`, `"pr73-1"` (L31-37)
- `estimation: "S"` (L40)
- `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"` (L38)

**Pattern takeaway for OVM:** Both tasks follow template 02 frontmatter verbatim, declare `template_schema_doc` pointing to the template path, use emoji-prefix `type:` and `status:`, and gate execution via `depends_on:` either with synthetic IDs (PR-X-MERGED style) or free-text caveats. **Neither uses a `tier:` / `compliance_tier:` frontmatter field** — confirming STRICT is purely a runtime classification.

---

## Sync Semantics for the OVM Edit Target

Resolved precisely:
- **Edit target:** `/config/.claude/skills/sc-reflect-protocol/SKILL.md`
- **No sync source available:** No `/config/workspace/Coder/src/superclaude/skills/sc-reflect-protocol/SKILL.md` exists (Bash check returned `NO superclaude src`). The "src → .claude" rule in the global CLAUDE.md presumes a SuperClaude framework checkout that is not present in `/config/workspace/Coder`.
- **No sync command available:** No Makefile exists, so neither `make sync-dev` nor `make verify-sync` can run.
- **Direct-edit path:** The MDTM task should edit `/config/.claude/skills/sc-reflect-protocol/SKILL.md` directly. Cite the global CLAUDE.md Component-edits rule (#6) as the rule and document the exception: "no `src/superclaude/` checkout present in this environment; direct edit of `.claude/skills/` is the only available path."

If the task-builder discovers a SuperClaude `src/` tree exists elsewhere on disk (e.g. `/config/.claude/` is not the canonical location, or there is a `~/dev/superclaude/` checkout), the L1 Discovery item should detect this and short-circuit to the proper sync workflow. Recommended Phase-1 step: `Bash find / -maxdepth 5 -path "*/src/superclaude/skills/sc-reflect-protocol/SKILL.md" 2>/dev/null` — record result to `phase-outputs/discovery/sync-source-locator.md`.

---

## Summary

- **Template path:** `/config/.claude/templates/workflow/02_mdtm_template_complex_task.md` (1205 lines, Parts 1+2 inside one HTML comment block).
- **Frontmatter:** ~25 fields including `id`, `title`, `description`, `status` (emoji-prefixed), `type`, `priority`, dates, `depends_on`, `related_docs`, `tags`, `template_schema_doc`, `task_type`. **No `tier` / `compliance_tier` field exists.**
- **STRICT tier** is declared at runtime via the `/sc:task` HTML classification block (`<!-- SC:TASK-UNIFIED:CLASSIFICATION -->`), documented in `/config/.claude/commands/sc/task.md` L62-68. Prior STRICT tasks (e.g. TASK-RF-CI-GATE-REMEDIATION L394) annotate Execution Log entries with `"via /sc:task STRICT execution"` as freeform prose.
- **Item format:** Single-paragraph 6-element B2 self-contained pattern (Context+WHY, Action+WHY, Output, "ensuring..." clause, blocker handling, "Once done, mark this item as complete").
- **L1-L6 patterns** available for discovery/build/test/review/conditional/aggregation; phase-gate QA inserted via M1 between dependent phases (I15-I16, M1-M2).
- **No Makefile in Coder repo.** `make sync-dev`, `make verify-sync`, `make lint`, `make test`, `make reflect-eval` from global CLAUDE.md are SuperClaude-repo targets unavailable here.
- **Coder validation surface:** `.github/workflows/markdownlint.yml`, `gitleaks.yml` (P-7, release-blocker), `coder-ci-aidev02-contract.yml`, `coder-ci-validate.yml`, `coder-ci-detect.yml`, `coder-template-main.yml`. None of these will lint files outside `/config/workspace/Coder/`.
- **OVM edit target lives outside Coder repo:** `/config/.claude/skills/sc-reflect-protocol/SKILL.md`. Direct in-place edit is the only path (no `src/` mirror exists; no `make sync-dev` available). Task validation must be embedded in L3 items, not delegated to CI.
- **Project CLAUDE.md rules to honor:** validation via `.github actions` (L7) — but moot for the OVM target since CI does not see the file; shell discipline (no `cd`, absolute paths); secrets discipline (Read env-files in full before commit; never merge with failing P-7).
- **Prior STRICT tasks** (TASK-FU-SC-REFLECT-DOC-HYGIENE-BATCH, TASK-FU-SC-REFLECT-PR73-1-DOCKER-CLI-CI-GATE, TASK-RF-CI-GATE-REMEDIATION) confirm: template_schema_doc populated, emoji-prefixed `status`/`type`, `depends_on` gating, no tier frontmatter field, STRICT noted in Execution Log prose.
