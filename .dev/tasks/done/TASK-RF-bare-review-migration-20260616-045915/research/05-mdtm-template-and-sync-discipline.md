# R5 Research: MDTM Template Rules + Sync/Verify Discipline + Prior Example

Status: Complete

Scope: MDTM complex-task template rules the builder must encode, the sync/verify
gating discipline for skill edits, the prior MMS phase-8 tasklist as a structural
example, and the swarm test/lint/verify gate commands a STRICT item should run.

All claims carry file:line evidence. No team tools used.

---

## 1. MDTM Complex-Task Template — PART 1 mandatory rules

Source: `.claude/templates/workflow/02_mdtm_template_complex_task.md`
(mirror of `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`).
This is the COMPLEX (template 02) variant — use it because the bare-review
migration needs discovery/test/review/conditional/aggregation handoffs (L-patterns)
and phase-gate QA (lines 76-83, 902-927, I8 line 582-591).

### 1.1 Frontmatter shape (lines 1-61)

The builder MUST emit YAML frontmatter with these fields (lines 1-61). Key ones:

- `id: "TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"` (line 2)
- `status:` one of `🔵 Backlog | 🟡 To Do | 🟠 Doing | 🔴 Blocked | 🟢 Done | ⚪ Cancelled` (line 6); start at `🟡 To Do` (line 7)
- `type:` enum — for a code-migration corrective task use `🐛 BugFix` or `🧩 Integration` (line 8)
- `priority:` enum (line 10-11)
- `created_date` / `updated_date` (lines 12-13), `assigned_to` (14), `coordinator: orchestrator` (17)
- `parent_task` (19), `depends_on:` list (20-22)
- `spec_path: ""` — driving spec/PRD/TDD path, populated by task-builder at A.2 (line 23)
- `reflect_pre:` block — PRE reflect-gate sign-off populated by task-builder at A.10.7: `verdict` (pass|fail|skipped), `coverage_pct`, `depth` (quick|standard|deep), `tcs`, `run_id`, `report`, `reviewed_at` (lines 24-31)
- `reflect_post: ""` — POST reflect verdict recorded by executor after final-phase reflect subagent (line 32)
- `related_docs:` list of {path, description} (33-39), `tags:` (42-46)
- `task_type: static` (line 60) — set `static` for fixed content, `dynamic` only if workers add items at runtime (I6, lines 543-549)

### 1.2 A3 — COMPLETE GRANULAR BREAKDOWN (lines 108-112)

- "Break down EVERY workflow phase into atomic, verifiable checklist items" (109)
- "Create individual checklist item for EVERY file, component, or iteration" (110)
- "NO high-level or bulk operations allowed - everything must be granular" (111)
- "Include exact file paths, specific requirements, and measurable outcomes" (112)

**Implication for the corrective tasklist:** each incomplete deliverable (SKILL.md
rewrite, each `scripts/*.sh` deletion, each test file, each doc) gets its OWN
self-contained item with the exact path. No "migrate the skill" mega-item.

### 1.3 A4 — ITERATIVE PROCESS STRUCTURE (lines 114-133)

For ANY multi-item process: pre-enumerate ALL items in an initial step, create one
checklist item per item, require incremental updates after each, consolidate only
after all complete (115-119). The Step X.1 (scan/enumerate) → Step X.2 (process each
individually) → Step X.3 (consolidate) pattern is shown verbatim at lines 121-133.

### 1.4 B2 — SELF-CONTAINED CHECKLIST ITEMS (the CRITICAL section, lines 148-213)

WHY (B1, lines 151-157): Rigorflow executes in batches across sessions; context from
batch 1 is GONE by batch 3+. Therefore EVERY item must embed all context. Standalone
"read context" items are USELESS (155-157).

B2 (lines 159-165) — every item MUST be a complete self-contained prompt with all 6 elements:

1. **Context Reference with WHY** — what file(s) to read and why (line 160)
2. **Action with WHY** — what to do and why (161)
3. **Output Specification** — exact output file name, location, content, template (162)
4. **Integrated Verification** — an "ensuring..." clause; DO NOT assume/hallucinate; 100% derived from source; document negative evidence on failure (163)
5. **Evidence on Failure Only** — log to task notes ONLY if blocked; success is evidenced by the output file itself (164)
6. **Explicit Completion Gate** — verbatim: "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete." (165)

B3 (167-170): write each item as ONE FULL PARAGRAPH (not bullets/multi-line),
verbose, reads like a standalone prompt. Worked CORRECT example at lines 172-179.

B5 — FORBIDDEN PATTERNS (lines 181-200):
- Standalone "read context" items with no output (183-186)
- Missing context reference / no source-of-truth (187-191)
- Multi-line/bulleted items — must be single paragraph (192-197)
- Separate verification/confirmation items — integrate via "ensuring..." (198)
- Overly granular items (e.g. "create directory" alone) (199)
- Separate REMINDER blocks between items (200)

B7 key principles (206-213): item = complete prompt; context embedded IN the action;
verification embedded IN the action; output file = evidence; only log on FAIL;
one verbose paragraph; QA process handles inter-batch verification (do NOT create
separate verification items).

### 1.5 Section C — embed, don't separate (lines 216-247)

Outputs (C1), success criteria (C2), verification (C3), task-completion (C4) are
EMBEDDED into checklist items — never standalone sections. No "Outputs & Deliverables",
"Success Criteria", "Verification Checklist", or "Task Completion and Handoff Protocol"
sections in the output file (228, 234, 239, 246).

### 1.6 Section D — MANDATORY sections + CRITICAL ordering rule (lines 250-289)

D3 CRITICAL RULE (286-289): "NO CHECKLIST ITEMS may appear before Phase 1 begins."
Structure is: Frontmatter → Workflow Compliance (informational) → Prerequisites
(informational) → Phase 1 (first executable items). All context-review/previous-stage-input
items live IN Phase 1, Steps 1.2-1.4. D1/D2 (Workflow Compliance Declaration,
Cross-Stage Integration) are `[WORKFLOW-DEPENDENT]` and informational-only.

### 1.7 Section E — checklist structure rules (lines 292-405)

- E1 (295-309): every actionable item is a `- [ ]` checkbox; FLAT structure — NO
  nested checkboxes, NO parent checkboxes summarizing children; one atomic action
  per box; use `**Step X.Y:**` bold headers for grouping (not checkboxes); boxes in
  exact completion order.
- E2 (311-365): summary/parent checkboxes come AFTER their components, never before;
  CORRECT vs FORBIDDEN patterns shown (parent-before-children = WRONG, summary-in-middle
  = WRONG).
- E3 (367-382): sequential top-to-bottom only; FORBIDDEN: "mark item complete in
  section above", "see checklist below", any backward movement.
- E4 (384-405): never place checkboxes next to step numbers; step numbers are bold
  headings; no separate REMINDER blocks (worker agents only see batch items).

### 1.8 Section F — execution requirements (lines 408-468)

- F1 FIVE-STEP loop: READ → IDENTIFY → EXECUTE → UPDATE → REPEAT (411-420)
- F2 PROHIBITED (422-430): working from memory; executing multiple items at once;
  skipping phases; **delegating across phase boundaries** (a subagent receives work
  from a SINGLE checklist item only, line 427); **skipping phase-gate QA** (428);
  **skipping post-completion validation** (429).
- F2a (431-447): one-item-at-a-time discipline within a session; **Parallel spawning
  exception** (447) — consecutive same-phase INDEPENDENT subagents MAY be spawned in
  parallel via multiple Agent calls in one message, marking each individually.
- F5 frontmatter protocol (464-468): on start → `🟠 Doing` + start_date; on completion
  → `🟢 Done` + completion_date; if blocked → `⚪ Blocked` + blocker_reason.

### 1.9 Section I — guidelines the builder must apply (lines 510-840)

- I1 (516): use "YOU MUST" / "DO NOT" directive language.
- I8 (582-591): template 02 is MANDATORY for complex/handoff tasks; "create an MDTM
  task" ALWAYS means read template → replace placeholders → write to location.
- I12 (609-614): verification INTEGRATED into the action item, no separate verify items.
- **I18 — TESTING REQUIREMENTS FOR CODE-MODIFYING TASKS (688-697):** if a task
  creates/modifies SOURCE CODE (not docs/config), the orchestrator MUST include ≥1
  testing item that (1) specifies the test command, (2) defines pass criteria, (3)
  specifies where results are captured, (4) follows B2. For template-02, use the L3
  (Test/Execute) pattern (695). **This is the rule forcing `uv run pytest tests/swarm/...`
  items into every code-touching task in the corrective tasklist.**
- I15/I16/I19/I20/I21/I22 (635-840): phase-gate QA enforcement, verdict/fix cycles,
  lens-based minimum agent counts, serialized fix authorization, source-fidelity gate,
  and `qa_intensity` levels (lite/standard/full). For a code-migration corrective
  tasklist these govern the M3 lens-based QA gate at phase boundaries; agent floors
  scale with `qa_intensity` (I22 table, lines 800-804: lite=3 final / standard=7 final
  / full=6-12+ per I19).

### 1.10 Section L — intra-task handoff patterns (lines 902-1027) — the L1-L6 patterns

Handoff file convention (909-921): items write outputs to
`.dev/tasks/TASK-NAME/phase-outputs/` with subdirs `discovery/`, `test-results/`,
`reviews/`, `plans/`, `reports/`. Files persist across batches; later items read by path.

- **L1 Discovery** (928-938): explore codebase/env, write structured findings file
  that later items consume. The discovery file IS the deliverable.
- **L2 Build-from-Discovery** (940-950): read discovery file AND source file, produce
  deliverable. Always reference BOTH paths.
- **L3 Test/Execute** (952-962): run a command/test suite, capture BOTH raw output
  AND a structured summary. **This is the pattern for the `uv run pytest tests/swarm/`
  and `make verify-sync` gate items.** Worked example runs pytest and writes
  `pytest-output.txt` + `test-summary.md` (961).
- **L4 Review/QA** (964-974): assess a prior output vs source; produce structured
  PASS/FAIL verdict with specific findings (never "looks good").
- **L5 Conditional-Action** (976-988): branch on a prior result file; MUST handle BOTH
  success AND failure branches; output file always created. **This is the pattern that
  gates legacy `scripts/*.sh` deletion on the A/B parity test passing** (mirrors how
  prior T08.07 was sequenced AFTER T08.11).
- **L6 Aggregation** (990-1000): Glob to discover files dynamically, consolidate into
  a report. Used as the final item in a phase / QA-gate Step 1 aggregation.
- **L7 Pattern Selection Guide** (1002-1027): table mapping need→pattern; common phase
  structures (Discovery→Build→Review; Build→Test→Fix; Full Lifecycle with QA Gates).

### 1.11 Section M — phase-gate composite patterns (lines 1028-1121)

- M1 is LEGACY/DEPRECATED (single-agent) — MUST NOT be used in new task files (1034-1045).
- **M3 Lens-Based QA Sequence** (1059-1096) is the MANDATORY gate pattern: Step 1
  aggregation (L6) → Step 2 structural rf-qa lens agents (parallel, `fix_authorization:
  false`) → Step 3 content rf-qa-qualitative lens agents → Step 5 consolidation →
  Step 6 ONE fix agent (`fix_authorization: true`) → Step 7 verification round → Step 8
  conditional proceed. EVERY step is an explicit `- [ ]` item (1096).
- M4 source-document fidelity gate (1098-1121) runs AFTER M3 when output is derived
  from source docs.

### 1.12 PART 2 — Execution Context block rules (lines 1193-1231)

The builder MUST populate the `## Execution Context` section as a required build step
(1194-1195: "Every generated task file MUST have this section populated before the
task file is marked ready"). Subsections:

- **### References** (1197-1199): all governing docs/specs/workflow files, format
  `- [Document Name](path): purpose`.
- **### Source Areas** (1201-1203): codebase dirs/modules/file-sets read or modified,
  format `` - `path/`: what it contains ``.
- **### Key Constraints** (1205-1207): top constraints — QA intensity, scope limits,
  known blockers, standing prohibitions.
- **### Handoff File Convention** (1209-1221): points to `.dev/tasks/TASK-NAME/phase-outputs/`.
- **### Frontmatter Update Protocol** (1223-1231): the F5 checkpoints restated.

The `[placeholder: builder populates]` sentinels (1199, 1204, 1207) MUST be replaced —
remaining sentinels are an I-rule / QA failure (template-conformance lens, line 716).

---

## 2. Sync / verify discipline — what a SKILL.md edit MUST and MUST NOT do

### 2.1 The two pre-commit hooks (`.pre-commit-config.yaml` lines 98-124)

**AC11 — `block-claude-generated-mirrors`** (lines 102-109):
- `entry: scripts/precommit_block_claude_mirrors.sh`, `pass_filenames: false`
- TRIGGER (`files:` regex, line 109): `^\.claude/(skills|agents|commands|hooks|templates)/`
- The script (`scripts/precommit_block_claude_mirrors.sh:4-22`) runs
  `git diff --cached --name-only --diff-filter=ACMR` over `.claude/{skills,agents,
  commands,hooks,templates}`; if ANY such path is STAGED it prints
  "❌ Generated .claude mirrors must not be committed" and exits 1
  (lines 17-22). Allowed exception: `.claude/settings.json` only (line 21).

**MIG-001 — `verify-bare-review-mirror-matches-src`** (lines 117-124):
- `entry: scripts/precommit_verify_bare_review_sync.sh`, `pass_filenames: false`
- TRIGGER (`files:` regex, line 124): `^src/superclaude/skills/sc-bare-review/`
  — i.e. fires whenever ANY path under that src dir is STAGED.
- The script (`scripts/precommit_verify_bare_review_sync.sh`):
  - `SRC="src/superclaude/skills/sc-bare-review"`, `MIRROR=".claude/skills/sc-bare-review"` (15-16)
  - `diff -rq` SRC vs MIRROR excluding `__pycache__`, `*.pyc`, `__init__.py` (29-33)
  - On drift: prints the diff and "Run: make sync-dev && make verify-sync" and
    "Stage only `$SRC/` paths — never the .claude/ mirror." then exits 1 (35-43).

### 2.2 What the corrective tasklist MUST encode for any item editing `src/superclaude/skills/sc-bare-review/SKILL.md`

Because both hooks fire on the commit path, every code/skill item that touches
`src/superclaude/skills/sc-bare-review/` MUST, as its `[COMPLETION]` step, run:

    make sync-dev && make verify-sync

(This is exactly the pattern the prior phase-8 tasks used — e.g. T08.01 step 5
"`make sync-dev && make verify-sync`", phase-8-tasklist.md:28; T08.07:234.)

MUST NOT (CLAUDE.md "ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents"
reinforced by AC11): never `git add .claude/skills/...`, never `git add -f` any
`.claude/` path. Edit `src/` → `make sync-dev` regenerates the mirror → stage ONLY
the `src/` side. If `git add` needs `-f` on `.claude/`, STOP.

### 2.3 `make sync-dev` behavior (Makefile:109-163)

Copies `src/superclaude/{skills,agents,commands,hooks,templates}` → `.claude/`
(skills loop 112-125 skips `__*` dirs and copies every file except `__init__.py`
and `__pycache__`; agents 126-130; commands→`.claude/commands/sc/` 131-136; hooks
137-147; templates 148-157). Prints per-type counts (159-163). It is a one-way
src→mirror copy; it never writes back to `src/`.

### 2.4 `make verify-sync` behavior (Makefile:166-183+)

CI-friendly drift check (line 166, declared `.PHONY` at line 1). Iterates each
`src/superclaude/skills/*/` (skipping `__*`), and for each does
`diff -rq --exclude='__init__.py' --exclude='__pycache__'` SRC vs `.claude/skills/$name`.
Missing mirror → "❌ MISSING" + drift=1 (174-176); content diff → "⚠️ DIFFERS" +
drift=1 (178-184). On drift the target prints "❌ Drift detected! Run 'make sync-dev'…"
and exits 1 (Makefile:351). So `make verify-sync` exits 0 only when src and mirror
match — this is the authoritative gate (the MIG-001 hook is the narrowed fast path).

---

## 3. Prior example — MMS phase-8 tasklist (structural model)

Source: `.dev/releases/complete/MultiModelSwarm/tasklist/phase-8-tasklist.md`.
NOTE: this is a SPRINT-CLI roadmap-phase tasklist (T08.NN tables), NOT an MDTM
`- [ ]` checklist task file. It is a useful structural model for the MIGRATION
sequencing, but the corrective deliverable must be an MDTM template-02 task file
(self-contained `- [ ]` paragraph items), not a T08-style table tasklist.

### 3.1 Effective patterns to mirror

- **Phase goal statement** up top (line 3) — single paragraph stating the exit
  condition ("Exit when SKILL.md is migrated, `scripts/*.sh` removed only after A/B
  parity passes, non-Python caller produces identical contract, every TEST item green").
- **Per-task metadata table** (Roadmap / Deliverables / Effort / Risk / **Tier** /
  Confidence / Critical Path Override / MCP Tools / Sub-Agent / **Verification**) —
  e.g. T08.01 lines 7-18. The `Tier` and `Verification` fields are the load-bearing
  ones: STRICT tier + a concrete `uv run pytest tests/swarm/...` command.
- **Explicit `[PLANNING]/[EXECUTION]/[VERIFICATION]/[COMPLETION]` step labels**
  (T08.01:24-28). The `[COMPLETION]` step is always `make sync-dev` (+`make verify-sync`
  for skill/src edits).
- **Acceptance Criteria + Validation** split (T08.01:30-39) — Validation gives the
  literal command + expected exit (`make verify-sync` exits 0; `wc -l … ≤80 lines`).
- **Dependency + Rollback** line per task (T08.01:40).
- **Sequencing of destructive deletion behind a parity gate**: T08.07 (legacy
  `scripts/*.sh` retirement) `Dependencies: T08.11 (TEST-003 parity)` and
  `Notes: Gates MIG-003 legacy deletion` — deletion is explicitly sequenced AFTER the
  A/B parity test (T08.07:211-246, T08.11:356-393, esp. 392-393 "This gate sequences
  before T08.07"). The corrective tasklist MUST preserve this ordering as an L5
  conditional-action item: delete shells ONLY IF parity test passed.
- **Checkpoint tasks** (`Type: CHECKPOINT`, `Tier: EXEMPT`) at mid-phase and
  end-of-phase boundaries (T08.06:191-209, T08.12:395-413, T08.15a:524-541,
  T08.18:615-634). Each checkpoint asserts "all of T08.0X..0Y marked done in
  execution-log" + a checkpoint report file. The MDTM analogue is the M3 phase-gate
  QA checkpoint between phases.

### 3.2 Where it fell short (the audit found T08.01/07/11/17 INCOMPLETE)

Live evidence that the phase-8 migration was NOT completed despite the tasklist
marking these tasks:

- **T08.01 NOT done** — the tasklist claimed SKILL.md rewritten to ~60-line thin
  caller (line 21) with validation `wc -l … ≤80 lines` (line 37). Live:
  `wc -l src/superclaude/skills/sc-bare-review/SKILL.md` = **231 lines** (verified
  this session). The thin-caller migration was never landed.
- **T08.07 NOT done** — claimed deletion of `scripts/*.sh` after parity (line 227).
  Live: `src/superclaude/skills/sc-bare-review/scripts/` still contains
  `t2_dispatch.sh`, `t2_normalize.py`, `t2_preflight.sh` (verified this session).
  Legacy shell path was never retired.
- **T08.11 (A/B parity) / T08.17 (integration wiring)** — the parity test FILE exists
  (`tests/swarm/test_bare_review_parity.py`, collects 17 tests this session), but
  because T08.01 never produced a thin caller, the migration the parity gate was meant
  to protect was not actually executed end-to-end. Related bare-review test files
  present: `test_bare_review_parity.py`, `test_escape_hatch_guard_parity.py`,
  `test_recipe_bare_review.py`.

**Lesson for the corrective tasklist:** the prior tasklist's tasks were marked done
in execution-log without the deliverable actually existing on disk. The corrective
MDTM task MUST encode I17 post-completion VALIDATION items that verify outputs exist
ON DISK (e.g. `wc -l SKILL.md ≤ 80`, `ls scripts/*.sh` empty) and that tests pass —
not merely that a step was "performed". Embed the validation in the item's "ensuring…"
clause AND add an explicit L3 test/verify item (I17, template lines 675-686; I18 lines
688-697).

---

## 4. Gate commands a STRICT item should run

Confirmed this session:

- **Swarm test command:** `uv run pytest tests/swarm/` — `tests/swarm/` exists with a
  `conftest.py`, `fixtures/`, and many `test_*.py` files including
  `test_bare_review_parity.py` (collected 17 tests cleanly). Narrower selectors used
  by the prior tasklist: `uv run pytest tests/swarm/test_bare_review_parity.py`
  (T08.01:18, T08.11:369), `pytest tests/swarm/ -m imm` / `-m inv` (T08.03:93).
- **Sync gate:** `make verify-sync` (exits 0 only when src↔mirror match; Makefile:166,
  351). Pair with `make sync-dev` first.

### 4.1 IMPORTANT caveat — `make lint` is independently RED; do NOT gate on it

`make lint` exits **2** this session (verified) — it is broken independently of the
migration work. STRICT items MUST gate on:
- `uv run pytest tests/swarm/` (or the targeted bare-review file), AND
- `make verify-sync`,

and a TARGETED ruff check on only the files the item touched (e.g.
`uv run ruff check src/superclaude/skills/sc-bare-review/`), **NOT** the full
`make lint`. The pre-existing ruff F401 (unused-import) noise the brief cites as "127"
measured **15 F401 occurrences** in the full `uv run ruff check src/ tests/` this
session — the exact count is stale/drifting, which is precisely why a STRICT item must
NOT gate on the repo-wide lint. Gate on pytest + `make verify-sync` + a path-scoped
ruff check instead. (See also memory `make lint ≠ CI ruff format`: `make lint` runs
only `ruff check`; CI separately runs `ruff format --check src/ tests/`.)

---

## 5. Summary for the builder

1. Use **template 02** (complex). Emit full frontmatter (§1.1) including
   `spec_path`, `reflect_pre`, `reflect_post`, `task_type: static`.
2. Populate the **Execution Context** block (References / Source Areas / Key
   Constraints) — no leftover `[placeholder: builder populates]` sentinels (§1.12).
3. Every item is a **single self-contained paragraph** with B2's 6 elements; no
   standalone "read context" or separate verification items (§1.4). NO checklist
   items before Phase 1 (D3, §1.6). Flat `- [ ]` boxes, summaries last (E1/E2, §1.7).
4. Each item touching `src/superclaude/skills/sc-bare-review/SKILL.md` MUST end with
   `make sync-dev && make verify-sync` and MUST NOT stage `.claude/` (§2.2). Both the
   AC11 and MIG-001 pre-commit hooks fire on the commit path (§2.1).
5. Sequence destructive `scripts/*.sh` deletion behind the A/B parity test using an
   **L5 conditional-action** item (delete only IF parity passed) — mirroring the prior
   T08.07-after-T08.11 ordering (§3.1, L5 §1.10).
6. Because this modifies SOURCE CODE, include **L3 test/execute** items running
   `uv run pytest tests/swarm/` and capturing results (I18, §1.9), plus **I17
   post-completion validation** items that verify outputs EXIST ON DISK
   (`wc -l SKILL.md ≤ 80`, `ls scripts/*.sh` empty) — the prior tasklist's failure mode
   was marking tasks done without the deliverable existing (§3.2).
7. STRICT gate = pytest + `make verify-sync` + path-scoped `ruff check`; **NOT**
   `make lint` (exits 2, independently red) and NOT repo-wide ruff (§4.1).
8. Insert an **M3 lens-based QA gate** at the phase boundary and a post-completion M3
   gate; agent counts per `qa_intensity` (I15/I19/I22, §1.9, §1.11).
