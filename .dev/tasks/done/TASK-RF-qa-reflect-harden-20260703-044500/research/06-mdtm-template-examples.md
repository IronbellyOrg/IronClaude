# Research: MDTM template & examples

Status: Complete
Date: 2026-07-03
Researcher: R6 (Template & Examples)

Scope: MDTM Template 02 (PART 1 rules + PART 2 task-file structure) and existing
task-folder examples, oriented to a Template-02, Deep-tier, QA_INTENSITY:full,
POST_REFLECT_GATE:ENABLED task (5 additive fixes across contract_setup Python +
cli/reflect + RF agent briefs).

## Primary sources (all under worktree root `/config/workspace/IronClaude/.dev/worktrees/pr209-harden/`)

- **Template 02:** `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`
  (1516 lines; PART 1 = lines 63-1131 instructions, PART 2 = lines 1155-1516 task-file template).
  (Note: task requested `.claude/templates/...`; that dev-copy does not exist in this worktree —
  the source-of-truth file above is canonical. Resolved, not Unverified.)
- **task-builder skill (POST/PRE gate + frontmatter contract):**
  `src/superclaude/skills/task-builder/SKILL.md` (esp. lines 41, 282, 1073-1078, 1729,
  2155-2168, 2204-2207, 2263, 2322).
- **Concrete Template-02 example (Deep, full QA, POST gate ENABLED):**
  `.dev/tasks/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/TASK-RF-uc2-reachability-gate-20260620-043410.md`
  (342 lines). Closest analogue to our target task (reflect + cli/reflect + Python + RF QA gates +
  POST reflect wrapper).

---

## 1. Required task-file sections + frontmatter fields

### 1a. Frontmatter (PART 2 template lines 1-61; example lines 1-70)

Baseline template fields: `id`, `title`, `description`, `version`, `status`, `type`,
`priority`, `created_date`, `updated_date`, `assigned_to`, `autogen`, `autogen_method`,
`coordinator`, `parent_doc`, `parent_task`, `depends_on`, plus the gate-specific fields below,
then `related_docs`, `related_prd`, `related_tdd`, `tags`, `template_schema_doc`, `estimation`,
`sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`,
`model_settings`, `review_info`, `task_type: static`.

**Gate / reflect-specific fields the builder MUST populate (task-builder SKILL, grounded):**

| Field | Rule (source) |
|---|---|
| `spec_path: ""` | Driving spec/PRD/TDD path (template line 23). Priority: explicit `--spec` -> `@file` in GOAL -> `SPEC:`/`PRD:`/`TDD:` in BUILD_REQUEST -> none (SKILL L41, L282). Threaded into the PRE gate `--spec` only; the POST wrapper does NOT take `--spec`. |
| `start_commit: "<sha>"` | **O1 wrapper's audit base.** Builder captures at build time as `git merge-base HEAD <integration-branch>` (SKILL L2155, L2168). Single ref (not a range) — diffed against the working tree so uncommitted task edits ARE audited. **[G7 CORRECTION — task-specific]** For THIS task the integration branch is **`origin/DetectionContractBranch`** (PR #209's target), **NOT `origin/master`** — `contract_setup` is absent from master, so `git merge-base HEAD origin/master` would drag the POST-reflect audit back before the package existed (diff-scope footgun swamping the gate). Resolve `<integration-branch>` = `origin/DetectionContractBranch`; at build time `git merge-base HEAD origin/DetectionContractBranch = 46a787da` (= current worktree HEAD). Capture `start_commit: "46a787dac39c75753a6da4ca483dc6b5d2581bb0"`. |
| `executor_model_class: "<alias>"` | Executor model-class alias (e.g. `sonnet`); passed to reflect as `--executor-model` so the executor class is excluded from the reviewer panel (anti-self-confirmation) (SKILL L2156, L2168). |
| `reflect_pre:` block | PRE gate sign-off (template lines 24-31): `verdict` (pass\|fail\|skipped), `coverage_pct`, `depth` (quick\|standard\|deep), `tcs`, `run_id`, `report`, `reviewed_at`. Populated by builder at A.10.7. |
| `reflect_post: ""` | **Room comment / empty string ONLY.** Written back by the `superclaude reflect run` wrapper at execution time. Builder MUST NOT hand-author or lock it (template line 32; SKILL L2157, L2168). |

Example real values (uc2 task lines 19-33): `spec_path` = the pre-reflect REPORT.md path;
`start_commit: "63f1a8153d2375e48369059c253dc2a76f73c063"`; `executor_model_class: "sonnet"`;
full populated `reflect_pre` block with real `run_id`; `reflect_post: ""`. The example also adds
(non-template but harmless) `template: "02"` and a `tracks:` list.

### 1b. Body sections (PART 2 template + example, in order)

1. `# [Task Title]`
2. `## Task Overview`
3. `## Key Objectives`
4. `## Prerequisites & Dependencies` (Parent Task & Dependencies; Previous Stage Outputs — INFORMATIONAL, no checklist items)
5. **`## Execution Context`** — REQUIRED, builder-populated (template lines 1193-1231). Sub-sections:
   - `### References` — governing docs/specs/workflow files (example lines 94-99 use `R-001...` IDs)
   - `### Source Areas` — codebase dirs/modules read or modified (example lines 100-106)
   - `### Key Constraints` — QA intensity, scope limits, blockers, prohibitions (example lines 108-113)
   - `### Handoff File Convention` — points at `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/`
   - `### Frontmatter Update Protocol`
6. `## MANDATORY WORKFLOW COMPLIANCE` (informational; example line 115)
7. `## Cross-Stage Integration Requirements` (informational; example line 123)
8. `## Detailed Task Instructions` -> `### Phase 1: Preparation and Setup` (Step 1.1 status->Doing;
   Step 1.2 create handoff dirs) -> `### Phase 2...N` -> `### Phase Gate: Quality Verification (M3)` ->
   `### Phase N: Testing & Verification` (I18) -> review/aggregation phases.
9. `## Post-Completion Actions` (I13/I17 validation items, POST reflect item, status->Done item)
10. `## Task Log / Notes` (Task Summary, Execution Log, per-Phase Findings, Phase Gate Findings,
    Follow-Up Items, Deviations).

**D3 CRITICAL RULE:** NO checklist items before Phase 1. Frontmatter -> informational sections ->
Phase 1 (first executable). Status->Doing is the FIRST checklist item (I11).

---

## 2. B2 five-field (six-element) self-contained item format

Template lines 159-166 (restated PART 2 lines 1249-1255). Every checklist item = ONE full
paragraph (B3), single `- [ ]` checkbox, embedding all six elements:

1. **Context Reference + WHY** — which file(s) to read and why needed for THIS action.
2. **Action + WHY** — what to do and why.
3. **Output Specification** — exact output file name, location, content, template to follow.
4. **Integrated Verification** — an "ensuring..." clause (no fabrication; 100% source-derived;
   document negative evidence on failure). NOT a separate verification item (C3, I12).
5. **Evidence on Failure Only** — log a blocker to the `### Phase [N] Findings` section of
   `## Task Log / Notes` ONLY if blocked; the output file itself is success evidence (B4, J1).
6. **Explicit Completion Gate** — "This item cannot be marked as done until the actions are
   completed in their entirety exactly as described. Once done, mark this item as complete."

**Canonical example (template B4, lines 173-174):**
> `- [ ] Read the file component-spec.md at docs/specs/component-spec.md to extract the API
> interface requirements ... then read the file BaseHandler.ts at src/handlers/BaseHandler.ts ...
> then create the file ApiHandler.ts at src/handlers/ApiHandler.ts containing a TypeScript class
> that implements all methods ... ensuring the file includes the standard header comment block,
> exports the class as default, all methods from the spec are implemented ..., no content is
> fabricated ..., and no placeholder or TODO comments remain. If unable to complete due to missing
> information, file access issues, or unclear requirements, log the specific blocker using the
> templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of
> this task file, then mark this item complete. Once done, mark this item as complete.`

**Forbidden (B5):** standalone "read context" items with no output; missing context reference;
multi-line/bulleted items; separate verification/confirmation items; overly granular items
(bare "create directory"); separate REMINDER blocks between items.

**Handoff patterns (Section L, lines 928-1000):** L1 Discovery (write to `phase-outputs/discovery/`),
L2 Build-from-Discovery, L3 Test/Execute (capture raw + summary to `test-results/` — **use for the
Python `uv run pytest` items per I18**), L4 Review/QA, L5 Conditional-Action, L6 Aggregation.

**I18 (code-modifying tasks, lines 688-697):** Since our task edits `contract_setup` Python +
cli/reflect (source code, not docs), the builder MUST include >=1 testing item using the L3 pattern,
specifying the test command (`uv run pytest tests/...`), pass criteria (0 failures, no regressions),
and where results are captured (`phase-outputs/test-results/...`).

---

## 3. QA-gate encoding rules (QA_INTENSITY: full, Deep tier)

I22 (lines 793-840) maps **Deep/Heavyweight -> full**, and full = "all current I19, I20, I21 rules
apply without modification" (lines 834-836). So the exact floors below come from I19/I16.

### 3a. Exact minimum agent counts

**FINAL / assembled-output gate (M3 lens-based), full intensity** — I19 table lines 706-711,
by output size (FLOORS, exceed when warranted):

| Output size | rf-qa (structural) | rf-qa-qualitative (content) | Total minimum |
|---|---|---|---|
| <500 lines | 3 | 3 | **6** |
| 500-1500 | 4 | 4 | **8** |
| 1500-3000 | 5 | 5 | **10** |
| >3000 | 6 | 6 | **12** |

Absolute floor for ANY final/assembled-output gate is **6 agents** (3 structural + 3 content) —
I15 line 638; gates below this are REJECTED at validation. Domain-specific lenses are added ON TOP
of these minimums (line 713).

**INTERMEDIATE gates (research / synthesis / task-integrity), full intensity** — I19 lines 731-743
and I15 line 638: absolute minimum **5 agents**. Per-gate composition:
- Research gate: 2 rf-analyst (completeness + cross-validation) + 2 rf-qa (evidence-quality +
  gap-detection) + 1 rf-qa-qualitative (research-depth).
- Synthesis gate: 2 rf-analyst (synthesis-accuracy + source-tracing) + 2 rf-qa (structure +
  content-quality) + 1 rf-qa-qualitative (synthesis-coherence).
- task-integrity gate: 2 rf-qa (structure + evidence-quality) + 2 rf-qa-qualitative (actionability
  + domain-accuracy) + 1 rf-analyst (completeness).

(For contrast — NOT our setting — standard final = 7 agents, lite = 3; I22 lines 802-803.)

### 3b. M3 lens-based QA sequence (lines 1059-1096) — the mandatory pattern

Every gate uses M3 (M1 single-agent is DEPRECATED, lines 1034-1045). Steps, each an explicit
`- [ ]` item:
1. **Aggregation (L6):** collect preceding-phase outputs into a summary/inventory (Glob dynamic).
2. **Structural lens agents (PARALLEL):** N rf-qa, one lens each, `fix_authorization: false`.
   Standard structural lenses (lines 715-720): template-conformance, internal-consistency,
   evidence-quality, completeness. Reports -> `${TASK_DIR}qa/qa-structural-[lens]-report.md`.
3. **Content lens agents (PARALLEL):** N rf-qa-qualitative, one lens each, `false`. Standard
   content lenses (lines 721-726): actionability, numbers-metrics, crossref-chain, domain-accuracy.
   (Steps 2+3 MAY share one parallel batch — line 1080.)
4. Domain-specific lens agents (if any), PARALLEL.
5. **Findings consolidation:** read ALL reports -> `${TASK_DIR}qa/qa-consolidated-findings.md`,
   deduplicated, severity + originating lens noted.
6. **Fix agent:** exactly ONE rf-qa with `fix_authorization: true` applies ALL fixes.
7. **Verification round (PARALLEL):** min 2 agents (1 rf-qa + 1 rf-qa-qualitative), `false`.
8. **Conditional proceed (L5):** both PASS -> proceed; either FAIL -> repeat 5-7.

Adversarial framing MANDATORY in every lens prompt (line 729): "Assume this document has at least N
errors focused on [lens]. Find them." N scales: 5 (<500), 10 (500-1500), 15 (1500-3000), 20 (>3000).

### 3c. I20 serialized fix authorization (lines 745-757)

Any gate with 3+ agents on the same file MUST serialize fixes: (1) all lens agents report
`fix_authorization: false`; (2) consolidate -> `${TASK_DIR}qa/qa-consolidated-findings.md`;
(3) ONE fix agent `fix_authorization: true` applies ALL fixes; (4) verification round (min 2:
1 rf-qa + 1 rf-qa-qualitative, `false`); (5) if verification finds new issues, repeat from
consolidation. Parallel fix authorization is PROHIBITED (churn). Every step = explicit `- [ ]` item.

### 3d. I16 fix-cycle caps (lines 653-673)

Binary verdict: any issue of ANY severity (CRITICAL/IMPORTANT/MINOR) = FAIL. Max fix cycles by gate:
research-gate 3 (then HALT+escalate), synthesis-gate 2 (unresolved->Open Questions),
report-validation 3 (HALT), task-integrity 2 (Open Questions), any qualitative gate 3 (HALT),
source-fidelity 3 (HALT). Full-intensity verification agents = 2 (I22 line 804).

### 3e. I21 / M4 source-fidelity applicability (lines 759-789, 1098-1121)

Fidelity gate is MANDATORY when outputs are derived from source documents (PRD, TDD, roadmap,
tech-reference, README, tech-research, repo-cleanup, "any task where the orchestrator reads source
docs to produce output" — lines 762-771). NOT required for pure mechanical transformations (rename
ops) or config-only tasks (lines 773-775).

**Applicability to OUR task:** a **code-modifying task** implementing 5 additive fixes across Python
+ cli/reflect + RF agent briefs against a driving spec (`spec_path`). Per M2 line 1052:
"Code-modifying tasks ... Fidelity gate ONLY if code was derived from spec documents." Because a spec
drives the fixes, an M4 source-fidelity gate SHOULD be included (semantic coverage, detail
preservation, phantom-coverage detection — each spec requirement/FR must map to an implemented item).
Full intensity -> per I21: min 2 fidelity agents, partition to 3-4 if source docs >1000 lines total;
runs AFTER the M3 lens gate (line 788); reports -> `${TASK_DIR}qa/qa-source-fidelity-report-[N].md`.
If the builder judges the fixes purely mechanical, it MUST record "Fidelity gate not applicable —
[reason]" (template line 1437). **R6 recommendation: INCLUDE the fidelity gate** given a resolved
`spec_path`; leave the not-applicable escape only if R1-R5 confirm the fixes carry no spec semantics.

### 3f. Where gates go (I15, F2, M2)

- I15 (line 635): every task with 2+ phases needs >=1 phase-gate between the primary execution phase
  and any dependent phase. Every QA step = explicit `- [ ]` item; "No QA is implicit. No QA lives
  only in prose" (line 651).
- I17 (lines 675-686): **post-completion lens-based QA is MANDATORY** on the final output(s) — IN
  ADDITION to any phase-gate QA — plus the fidelity gate when applicable, BEFORE frontmatter->Done.
- F2 (lines 428-429): proceeding to the next phase without a passing QA gate is PROHIBITED; skipping
  post-completion structural + qualitative validation before Done is PROHIBITED.

---

## 4. POST reflect wrapper shell-out item (penultimate final-phase item)

### 4a. Canonical form (task-builder SKILL lines 2204-2207, 2322; template lines 32, 2155-2157)

When `POST_REFLECT_GATE: ENABLED`, the builder MUST emit — as the **penultimate item of the final
phase, immediately before the `Update status to Done` item** (SKILL lines 1729, 2263, 2322) — a
FLAT wrapper shell-out (NOT a reflect subagent). The single Bash command:

```
if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi; superclaude reflect run {TASK_FILE} --depth deep --fix --promote
```

- `{TASK_FILE}` = absolute tasklist path (wrapper absolutizes its positional).
- **NO** `--base` (wrapper resolves audit base from frontmatter `start_commit`, a single ref diffed
  vs the working tree). **NO** `--reflect`, **NO** `<base>..HEAD` range, **NO** `--spec`,
  **NO** `--max-turns`, **NO** agent-spawn / nesting tokens (NFR-7 clean; flat shell-out).
- `--depth deep` fixed (O1 forces Tier-2 fan-out); `--fix` runs the bounded auto-fix loop;
  `--promote` lets the `task` adapter move the dir to `done/` on a clean/auto-fixed PASS.
- **Exit-code consumption:** ONLY `0` completes the gate (clean OR auto-fixed-and-verified).
  `10` (halted — human-required deviations / non-convergent loop), `11` (degraded — audit
  untrustworthy), `2` (blocked — child crash / bad contract) all FAIL -> surface the wrapper report
  and HALT **before** the Update-status-to-Done item.
- The wrapper writes `reflect_post: {verdict, run_id, report}` back to frontmatter itself; the item
  MUST NOT hand-author/lock `reflect_post`, MUST NOT halt for a human, MUST NOT defer to another
  session. Re-execution uses `/task` (never `/sc:task`).
- Staging: item should first ensure new artifacts are staged (`git add -A`) so the working-tree diff
  is complete (the wrapper's audit omits never-`git add`-ed files) — SKILL line 2205.

**MALFORMED if:** omitted when ENABLED; not penultimate; emits the legacy self-run reflect-subagent
form; emits a human-handoff/HALT form; passes `--base`/`--reflect`/`<base>..HEAD`; or hand-authors
`reflect_post` (SKILL lines 2263, 2322).

### 4b. Real B2-wrapped instance (uc2 example line 248 — imitate this)

The example encodes it as a full B2 paragraph: reads the task file + a `staged-files-for-reflect.md`
report + a `post-completion-readiness.md` report, then runs the guard + `superclaude reflect run
<abs-task-file> --depth deep --fix --promote` from the repo root, "ensuring no `--base`, no
`--reflect`, no `<base>..HEAD` range, no `/sc:task`, and no agent-spawn directive is used; only
wrapper exit code `0` permits proceeding, while exits `10`, `11`, or `2` must be surfaced with the
wrapper report and logged before halting the Done update," with the standard blocker-log-and-STOP
clause and completion gate. The very next item (line 250) is the `status -> "🟢 Done"` item, gated
on "the POST reflect wrapper item exited `0` or was legitimately suppressed by the recursion guard."

---

## 5. Concrete Template-02 example folder to imitate

**`.dev/tasks/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/`**
(main file `TASK-RF-uc2-reachability-gate-20260620-043410.md`, 342 lines).

Why it is the best analogue and what to imitate:
- **Same domain:** implements a reflect gate touching `src/superclaude/skills/sc-reflect-protocol/`,
  `src/superclaude/commands/reflect.md`, `src/superclaude/cli/reflect/` (Python), plus tests and
  evals — structurally identical to our contract_setup Python + cli/reflect + RF briefs.
- **Frontmatter to copy:** populated `spec_path`, `start_commit` (single SHA),
  `executor_model_class: "sonnet"`, full `reflect_pre` block, and `reflect_post: ""` (lines 19-33).
- **Execution Context (lines 92-113):** References use `R-00N` IDs -> path -> one-line purpose;
  Source Areas list each dir with "what it contains / why relevant"; Key Constraints encode the
  safety/validation bar (incl. `make sync-dev`/`make verify-sync`/`uv run pytest`/`ruff format
  --check` — mirror these for our Python edits).
- **Full-intensity M3/I20 gate (lines 218-232):** each lens agent is a B2 paragraph naming the agent
  type (`rf-qa` / `rf-qa-qualitative`), a `QA_MODE:`/`QA_PHASE:` + `LENS:` label,
  `fix_authorization: false`, explicit input files, explicit `${TASK_DIR}qa/...report.md` output,
  and an inline adversarial stance ("assume this change has at least five ... violations and find
  them"); then a consolidation item, a single `fix_authorization: true` fix item (line 232, gated on
  FAIL), and a verification round.
- **POST reflect item (line 248) then Done item (line 250):** the exact penultimate-then-final
  ordering and the guard+wrapper command described in section 4.

Secondary examples (also Deep, POST gate ENABLED, similar surface):
`.dev/tasks/to-do/TASK-RF-fr-drs-runtime-surface-20260622-000600/` and
`.dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/` (the task that WIRED the POST
gate — useful for guard/contract wording).

---

## Summary (for rf-task-builder)

- Build from `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` PART 2; copy the
  frontmatter and populate `spec_path`, `start_commit` (= `git merge-base HEAD <integration-branch>`),
  `executor_model_class`, `reflect_pre` (at A.10.7); leave `reflect_post: ""` untouched.
- Every checklist item = one B2 paragraph with all 6 elements; code items use L3 test pattern
  (`uv run pytest ...`) per I18; no checklist items before Phase 1; status->Doing is item 1.
- **QA_INTENSITY: full (Deep tier)** => I19/I20/I21 unmodified. **Final/post-completion M3 gate floor
  = 6 agents** (3 rf-qa structural + 3 rf-qa-qualitative content) for a <500-line output, scaling
  8/10/12 by size, +domain lenses on top. **Intermediate gate floor = 5 agents** with the fixed
  compositions in 3a. Serialized fix (I20): report(false)->consolidate->ONE fix(true)->verify(2).
  Include an M4 source-fidelity gate (min 2 agents) because a spec drives the fixes — else record the
  not-applicable note.
- POST gate: penultimate final-phase item = flat guard `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}"
  = "1" ]; ...exit 0; fi; superclaude reflect run {TASK_FILE} --depth deep --fix --promote`; consume
  exit code (only 0 proceeds); no `--base`/`--spec`/`--reflect`/range/subagent; never hand-author
  `reflect_post`. Model it on uc2 line 248 -> line 250.

### Unverified / caveats
- The requested `.claude/templates/...` dev-copy path does not exist in this worktree; the
  source-of-truth `src/superclaude/templates/...` file was used instead (canonical; not a gap).
- Exact final-output line count (which sets the 6/8/10/12 tier + adversarial N) depends on the built
  task file's size — the builder resolves this at build time; <500 lines => 6-agent floor.
- Whether the M4 fidelity gate is strictly mandatory hinges on R1-R5's judgment of whether the 5
  fixes carry spec-semantic content (they appear to). Flagged "INCLUDE unless proven mechanical."
