# Extension-Point Contracts — `/task`

**Task:** T03.02 — Document extension-point contracts
**Roadmap Item:** R-009
**Generated:** 2026-05-15
**Inputs:** `recipient-extension-points.md` (T01.01), INV-01..INV-05 (sprint spec § "Load-bearing invariants")
**Source of truth (R-RULE-10):** All `file:line` evidence resolves against `src/superclaude/skills/task/SKILL.md`; the `.claude/` mirror is byte-identical and is *not* the attach target.

## Invariant Reference (anchor labels, pending T03.01 expansion)

| Label | Behavioral rule (sprint spec § "Load-bearing invariants") |
|---|---|
| **INV-01** | F1 loop semantics — READ first unchecked `- [ ]`, EXECUTE exactly as written, UPDATE to `- [x]`, REPEAT. No skipping, reordering, or out-of-band substitution. |
| **INV-02** | Prohibited-actions catalog (F2) — no working from memory, no modifying checklist items mid-execution, no delegating the F1 loop itself. |
| **INV-03** | Phase-gate `rf-qa` between phases (Phase 2+); post-completion `rf-qa` + `rf-qa-qualitative` validation. |
| **INV-04** | Resumability — progress recoverable from disk after context compression / session restart. |
| **INV-05** | Refusal-of-definition — `/task` does not decide *what* to do; the MDTM file does. The F1 loop only *executes*. |

> When `invariant-bounds.md` (T03.01) lands, each `INV-NN` reference below resolves to a worked-example-backed section; the labels and rules are stable in the sprint spec and used here verbatim.

## Complementarity Bands

| Band | Meaning | Phase 4 anchor |
|---|---|---|
| **C5** | Native fit — donor feature attaches at an existing extension surface with no schema change; admit criteria are met directly. |
| **C3** | New field / hook required — extension surface exists but must be widened (new roster entry, new field, new heuristic). No F1 change. |
| **C1** | Requires an F1 change — attaching the feature would mutate loop control flow, the F2 prohibited-actions catalog, the F4 modification restrictions, or the F5 lifecycle map in a way that violates an INV. **Auto-REJECT (R-RULE-05).** |

## Summary Table

| # | Extension point | C-band | Primary INVs protected by reject criteria |
|---|---|---|---|
| 1 | Task File Validation gate | C5 | INV-01, INV-05 |
| 2 | First Item Protocol (pre-loop status init) | C5 | INV-01, INV-05 |
| 3 | Session Resumption | C5 | INV-01, INV-04 |
| 4 | F1 EXECUTE item-type dispatch | C3 (C1 if loop semantics change) | INV-01, INV-02, INV-05 |
| 5 | "ensuring…" clause verification hook | C5 | INV-01, INV-02, INV-04 |
| 6 | UPDATE step — Phase Findings logging | C5 | INV-01, INV-02, INV-04 |
| 7 | Parallel Agent Spawning — batch detection | C3 | INV-01, INV-03, INV-04 |
| 8 | Error Handling / blocker logging | C5 / C3 | INV-01, INV-02, INV-04 |
| 9 | Incremental Writing Protocol | C5 | INV-04 |
| 10 | Phase-Gate QA Verification | C3 | INV-03, INV-04 |
| 11 | Post-Completion Validation | C5 / C3 | INV-03, INV-04 |
| 12 | Frontmatter Update Protocol (F5) | C5 | INV-01, INV-05 |
| 13 | Required frontmatter schema slot | C5 | INV-01, INV-05 |
| 14 | DYNAMIC CONTENT MARKER sections | C3 | INV-01, INV-02, INV-05 |
| 15 | Subagent dispatcher — type selection | C3 | INV-01, INV-02, INV-05 |
| 16 | Subagent dispatcher — Agent Prompt Handling | C5 / C3 | INV-02, INV-05 |
| 17 | Subagent dispatcher — Agent Mode | C5 | INV-01, INV-02 |
| 18 | Subagent dispatcher — Background vs Foreground | C5 | INV-02, INV-04 |
| 19 | Subagent dispatcher — Agent Results handling | C5 / C3 | INV-02, INV-03, INV-04 |
| N1 | Prohibited Actions (F2) — negative-space | **C1** (admits nothing) | INV-02 (primary), INV-01, INV-03, INV-04 |
| N2 | Task File Modification Restrictions (F4) — negative-space | **C1** (admits nothing) | INV-02, INV-01, INV-04 |
| N3 | F1 loop is non-delegable (Critical Rule 12) — negative-space | **C1** (admits nothing) | INV-01, INV-02 |

---

## Positive-Space Extension Points (detail)

### 1. Task File Validation gate — `src/superclaude/skills/task/SKILL.md:64-73` (`src/`)

- **Admit:** Pre-loop well-formedness checks — new frontmatter-schema validators, B2-pattern lints, checklist-presence checks, Task Log section presence. The validator runs before loop entry, produces a user-facing diagnostic, and writes nothing to the task file beyond a refusal message when malformed.
- **Reject:**
  - Validators that mutate the task file mid-loop (would corrupt the READ source-of-truth). → **INV-01**, **N2/F4**.
  - Validators that interpret items to decide *what* work to do (e.g., synthesizing missing items). → **INV-05**.
  - Validators that run inside the EXECUTE step rather than pre-loop. → **INV-01**.
- **C-band:** **C5** — pre-loop slot, append-only.

### 2. First Item Protocol (pre-loop status init) — `src/superclaude/skills/task/SKILL.md:100-102` (`src/`)

- **Admit:** Session-init / environment-prep actions that run once before the loop's first iteration — frontmatter writes to flip status to "🟠 Doing", set `start_date`, ensure subfolders (`research/`, `reviews/`, `synthesis/`, `qa/`) exist.
- **Reject:**
  - Init actions that consume a checklist item before the loop sees it (would steal IDENTIFY's first-item ownership). → **INV-01**.
  - Init actions that compute *what* the loop will execute (e.g., dynamic checklist generation outside DYNAMIC CONTENT MARKER sections). → **INV-05**.
- **C-band:** **C5**.

### 3. Session Resumption — `src/superclaude/skills/task/SKILL.md:268-283` (`src/`)

- **Admit:** Resume-state reconstruction routines that read disk to (a) locate the task file, (b) find the first unchecked `- [ ]`, (c) read prior outputs from `research/`, `reviews/`, `synthesis/`, `qa/`. Pure-read context rehydration.
- **Reject:**
  - Resume routines that re-execute already-checked items (`- [x]` is durable). → **INV-01**, **INV-04**.
  - Resume routines that work from compressed/summarized in-context state rather than re-reading the file. → **INV-04** (file-as-truth is the resumability guarantee).
  - Resume routines that skip ahead by inferring intent from prior outputs (effectively reordering items). → **INV-01**.
- **C-band:** **C5**.

### 4. F1 EXECUTE item-type dispatch — `src/superclaude/skills/task/SKILL.md:89-96` (`src/`)

- **Admit:** A new item-action verb whose meaning is fully encoded inside a single item, executed one-at-a-time, with verifiable on-disk evidence (file written, output produced, frontmatter mutated) before UPDATE.
- **Reject:**
  - Action verbs that operate on multiple items at once outside the parallel-spawn exception. → **INV-01**, **INV-02** (F2 "Executing multiple items simultaneously").
  - Action verbs whose completion is unverifiable (no disk artifact, no command output). → **INV-02** (F2 "Assuming completion").
  - Action verbs that decide *which item* to execute next (override IDENTIFY). → **INV-05**, **INV-01**.
  - Action verbs that complete asynchronously without a synchronous re-read at completion. → **INV-04**.
- **C-band:** **C3** — adding a verb to an existing enumerated dispatch. Becomes **C1** (auto-reject) if the verb changes EXECUTE-step ordering or completion semantics.

### 5. "ensuring…" clause verification hook — `src/superclaude/skills/task/SKILL.md:96` (`src/`)

- **Admit:** Per-item post-condition evaluators that read item-local outputs and pass/fail before UPDATE. Failure routes to Error Handling (existing slot, row 8).
- **Reject:**
  - Gate logic that decides the *next* item (would override IDENTIFY). → **INV-01**, **INV-05**.
  - Gates that modify the item being verified. → **INV-02** (F4 "rewrite/rephrase items").
  - Gates whose verdict is reached without reading the produced artifact (memory-based verification). → **INV-02** (F2 "Working from memory"), **INV-04**.
- **C-band:** **C5** — "ensuring…" is the native attachment surface.

### 6. UPDATE step — Phase Findings logging — `src/superclaude/skills/task/SKILL.md:97` (`src/`)

- **Admit:** Structured per-item evidence capture appended to `## Task Log / Notes` (Execution Log / Phase Findings / Follow-Up Items). Append-only, incremental (Critical Rule 2 ZERO TOLERANCE).
- **Reject:**
  - Logging that mutates checklist items (e.g., rewrites an item to record its outcome inline). → **INV-02** (F2/F4).
  - Logging that rewrites prior log entries (destroys the evidence trail). → **INV-04**.
  - Logging that batches across multiple items before flushing (loses partial progress on session end). → **INV-01**, **INV-04** (incremental writing IS the resumability mechanism).
- **C-band:** **C5**.

### 7. Parallel Agent Spawning — batch detection — `src/superclaude/skills/task/SKILL.md:119-142` (`src/`)

- **Admit:** Batch-identification and partitioning heuristics that (a) only group items within a single phase, (b) only group items with no inter-item output dependency, (c) mark each item `- [x]` as its agent returns, (d) re-read the task file after the batch.
- **Reject:**
  - Heuristics that group items across phase boundaries. → **INV-03** (phase-gate is mandatory), **INV-01** (Critical Rule 11).
  - Heuristics that delegate the loop itself ("subagent, please process items 3–7"). → **INV-01**, **INV-02** (N3 / Critical Rule 12).
  - Batch handlers that do not re-read after batch completion (mental-model drift). → **INV-04**.
- **C-band:** **C3** — widening the partition-threshold table is an enumerated extension.

### 8. Error Handling / blocker logging — `src/superclaude/skills/task/SKILL.md:170-179` (`src/`)

- **Admit:** New blocker classification (recoverable vs unrecoverable), recovery strategies, and blocker-logging formats that preserve the "items NEVER left unchecked" rule and log to Task Log / Notes. Failure-routing policy may select a recovery strategy per blocker type.
- **Reject:**
  - Recovery that re-executes already-checked items. → **INV-01**.
  - Recovery that defers items for later in the run (effectively reordering). → **INV-01**, **INV-02** (F2 "Skipping items").
  - Recovery that marks items complete without disk-evidence. → **INV-02** (F2 "Assuming completion").
  - Blocker classification that depends on remembered prior state rather than re-reading. → **INV-04**.
- **C-band:** **C5** for new failure-routing policies inside the existing taxonomy; **C3** if the taxonomy itself is widened.

### 9. Incremental Writing Protocol — `src/superclaude/skills/task/SKILL.md:252-264` (`src/`)

- **Admit:** New write-safety / chunking policies that maintain "Write (header) → Edit (section) → Edit (section) → …" — token-budget-aware chunking, subagent write-discipline rules, append-cadence policies.
- **Reject:**
  - Policies that permit single-large-Write of accumulated context (the #1 failure mode; loses all in-progress work on overflow). → **INV-04** (the incremental rule is the primary mechanism enforcing disk-as-truth).
  - Policies that buffer in memory before flush (defeats resumability). → **INV-04**.
- **C-band:** **C5**.

### 10. Phase-Gate QA Verification — `src/superclaude/skills/task/SKILL.md:182-211` (`src/`)

- **Admit:** Between-phase gate logic that runs `rf-qa` with **ADVERSARIAL STANCE**, extracts "ensuring…" clauses as acceptance criteria, persists report to `${TASK_DIR}reviews/qa-phase-[N]-report.md`, supports max-3 fix cycles, halts on unfixable. Partitioning extensions for >6 output files. Additional verdict-processing taxonomy entries.
- **Reject:**
  - Gates that bypass `rf-qa` invocation. → **INV-03**.
  - Gates that downgrade adversarial stance to "summarize what was done" (no zero-trust). → **INV-03** (the adversarial stance is the gate's binding power).
  - Gates that allow Phase N+1 to begin before Phase N's gate passes. → **INV-03**, **INV-01** (Critical Rule 11).
  - Gates whose verdict is decided in-context without writing the report. → **INV-04** (evidence trail), **INV-03**.
- **C-band:** **C3** — widening the gate is admissible, replacing the gate is not.

### 11. Post-Completion Validation — `src/superclaude/skills/task/SKILL.md:213-248` (`src/`)

- **Admit:** New whole-task validation capability layered on top of the existing `rf-qa` structural + `rf-qa-qualitative` operational pair — cross-phase consistency analyzers, qualitative-checklist extensions, partitioning for >15 outputs.
- **Reject:**
  - Replacement of `rf-qa-qualitative` with a lighter-weight validator (degrades zero-leniency rule at `SKILL.md:248`). → **INV-03**.
  - Validation that runs before all phase gates have passed. → **INV-03** (ordering).
  - Marking the task "🟢 Done" without persisting both report files. → **INV-04**.
- **C-band:** **C5** for additive analyzers; **C3** if a new validator type joins the post-completion pair.

### 12. Frontmatter Update Protocol (F5) — `src/superclaude/skills/task/SKILL.md:159-168` (`src/`)

- **Admit:** New lifecycle event → field mappings appended to the F5 table (e.g., new optional metadata events). Side-channel writes that respect F4 modification restrictions.
- **Reject:**
  - Fields whose semantics override the existing status taxonomy (🟡 To Do / 🟠 Doing / ⚪ Blocked / 🟢 Done) or rewrite `start_date` / `completion_date`. → **INV-01** (status flip is the loop's lifecycle anchor).
  - Fields whose value gates loop control flow (frontmatter is a side-channel per F4, not a control surface). → **INV-01**.
  - Fields encoding *what work to do* at runtime. → **INV-05**.
- **C-band:** **C5**.

### 13. Required frontmatter schema slot — `src/superclaude/skills/task/SKILL.md:69` (`src/`)

- **Admit:** New required-metadata fields validated by row 1's pre-loop validator (style: `id`, `title`, `status`, `created_date`). Schema rules are evaluated before loop entry.
- **Reject:**
  - Required fields whose values *define the work* (e.g., a `tasks: [...]` field consumed instead of the checklist body). → **INV-05** (work definition lives in the checklist; frontmatter is metadata).
  - Required fields validated mid-loop. → **INV-01** (validation is pre-loop).
- **C-band:** **C5**.

### 14. DYNAMIC CONTENT MARKER sections — `src/superclaude/skills/task/SKILL.md:114, 150, 156` (`src/`)

- **Admit:** Self-extending / generative-task content that injects new `- [ ]` items *inside* marked sections. Injected items must follow the B2 self-contained pattern (so IDENTIFY picks them up unmodified) and respect ZERO TOLERANCE incremental writing.
- **Reject:**
  - Content injection outside marked sections. → **INV-02** (F4 "Add new checklist items outside DYNAMIC CONTENT MARKER sections" is prohibited).
  - Injection that mutates already-checked items. → **INV-01**, **INV-02** (F4).
  - A generator whose injected items themselves decide further injection criteria with no checklist trail. → **INV-05** (work definition leaking out of the file).
- **C-band:** **C3** — markers are an existing slot, but the injecting generator is new mechanism.

### 15. Subagent dispatcher — type selection — `src/superclaude/skills/task/SKILL.md:291-299` (`src/`)

- **Admit:** A new agent type added to the roster (`general-purpose`, `rf-analyst`, `rf-qa`, `rf-qa-qualitative`, `rf-assembler`, `rf-task-builder`, `rf-task-researcher`, `Explore`, …). The new type must be invocable from a single checklist item, accept a verbatim B2 prompt, and return verifiable output.
- **Reject:**
  - Agent types whose contract requires multi-item ownership ("loop-driver" agents). → **INV-01**, **INV-02** (N3 / Critical Rule 12).
  - Agent types that decide what work to execute next on the executor's behalf. → **INV-05**.
- **C-band:** **C3**.

### 16. Subagent dispatcher — Agent Prompt Handling — `src/superclaude/skills/task/SKILL.md:301-302` (`src/`)

- **Admit:** Prompt-construction policies that preserve verbatim pass-through. Additive context-injection (e.g., a stable environment-context preamble prepended before the embedded prompt body) where the body itself is unmodified.
- **Reject:**
  - Policies that summarize, abbreviate, paraphrase, or "improve" the embedded prompt. → **INV-02** (F2 "Modifying items" + Critical Rule 4 "Execute items as written").
  - Policies whose preamble reinterprets the work the item defines. → **INV-05**.
- **C-band:** **C5** for additive preamble; **C3** for a new prompt-transformation policy layer.

### 17. Subagent dispatcher — Agent Mode — `src/superclaude/skills/task/SKILL.md:304-305` (`src/`)

- **Admit:** Mode-selection refinements (e.g., per-agent-type defaults). Must default to `bypassPermissions` or be explicitly overridden by the item itself.
- **Reject:**
  - Modes that introduce interactive permission prompts inside subagents (would freeze EXECUTE indefinitely). → **INV-01** (progress guarantee).
  - Modes that elevate privileges without item authorization. → **INV-02** (evidence-only, item-as-written).
- **C-band:** **C5**.

### 18. Subagent dispatcher — Background vs Foreground — `src/superclaude/skills/task/SKILL.md:307-309` (`src/`)

- **Admit:** Scheduling refinements (concurrency caps, background promotion when the item allows it). Must preserve per-agent `- [x]` marking as each returns.
- **Reject:**
  - Schedulers that mark items complete before the agent's output file exists. → **INV-02** (F2 "Assuming completion").
  - Schedulers that fire background agents whose completion the loop never re-reads. → **INV-04** (the file must reflect reality on resume).
- **C-band:** **C5**.

### 19. Subagent dispatcher — Agent Results handling — `src/superclaude/skills/task/SKILL.md:314-319` (`src/`)

- **Admit:** New verdict-processing / output-verification policies that read the agent's output file, capture PASS/FAIL, mark `- [x]`, route failures to row 8. Zero-trust enforcement for QA-type agents.
- **Reject:**
  - Handlers that trust the agent's in-chat summary instead of reading the produced file. → **INV-02** (F2 "Assuming completion"), **INV-03** (zero-trust is the QA-gate guarantee).
  - Handlers that re-issue work to the same agent without first re-reading the produced artifact. → **INV-04**.
- **C-band:** **C5** for an additive verdict-routing policy; **C3** if the verdict taxonomy itself is widened.

---

## Negative-Space Rows (admit nothing — constraint surfaces)

### N1. Prohibited Actions (F2) — `src/superclaude/skills/task/SKILL.md:104-117` (`src/`)

- **Admit:** Nothing. F2 is a constraint surface; "absorbing" here means *removing* a prohibition, which is structurally a contract weakening.
- **Reject:**
  - Features whose mechanism requires *working from memory*. → **INV-02** (primary), **INV-04**.
  - Features that execute multiple items simultaneously outside the parallel-spawn exception. → **INV-02**, **INV-01**.
  - Features that skip / reorder / defer items. → **INV-02**, **INV-01**.
  - Features that assume completion without disk evidence. → **INV-02**.
  - Features that invent unverified file paths. → **INV-02**.
  - Features that rewrite / reinterpret items. → **INV-02**, **INV-05**.
  - Features that add items outside DYNAMIC CONTENT MARKER sections. → **INV-02** (F4).
  - Features that delegate a subagent across phase boundaries. → **INV-02**, **INV-03**.
  - Features that skip phase-gate QA or post-completion validation. → **INV-03**.
- **C-band:** **C1 — auto-REJECT (R-RULE-05)**. Any donor feature whose attachment requires relaxing F2 is rejected regardless of value score.

### N2. Task File Modification Restrictions (F4) — `src/superclaude/skills/task/SKILL.md:144-158` (`src/`)

- **Admit:** Nothing. F4 is a write-discipline constraint.
- **Reject:**
  - Features that rewrite / rephrase existing checklist items. → **INV-02** (F4), **INV-05** (definition refusal).
  - Features that add items outside DYNAMIC CONTENT MARKER sections. → **INV-02**.
  - Features that delete or reorder existing items. → **INV-01**, **INV-02**.
  - Features that modify Task Overview / Key Objectives / Variables sections. → **INV-04** (corrupts the disk-as-truth READ source).
  - Features that change the task file's structure or headings. → **INV-04**.
- **C-band:** **C1 — auto-REJECT (R-RULE-05)**.

### N3. F1 loop is non-delegable (Critical Rule 12) — `src/superclaude/skills/task/SKILL.md:349` (`src/`)

- **Admit:** Nothing. Loop ownership is non-transferable by construction.
- **Reject:**
  - Features that delegate the READ-IDENTIFY-EXECUTE-UPDATE-REPEAT loop to a subagent. → **INV-01** (loop ownership is the integrity guarantee), **INV-02** (catalogued prohibition).
  - Features whose contract spans more than one checklist item per subagent dispatch outside the parallel-spawn exception. → **INV-01**, **INV-02**.
- **C-band:** **C1 — auto-REJECT (R-RULE-05)**.

---

## Coverage Check (Acceptance Criteria)

| AC | Statement | Evidence |
|---|---|---|
| AC1 | One row per Phase 1 extension point | 19 positive-space rows + 3 negative-space rows = 22 total, matching `recipient-extension-points.md` (positive rows 1–19 + N1–N3). |
| AC2 | Every row has explicit admit + reject criteria | Every section above contains both **Admit:** and **Reject:** subsections. Negative-space rows N1–N3 explicitly state **Admit: Nothing** (the contractually correct answer for constraint surfaces). |
| AC3 | Every reject criterion cross-references the INV-NN it protects | Each reject bullet ends with `→ **INV-NN**` (and the F2/F4/Critical-Rule label when applicable). |
| AC4 | Every row carries a Complementarity band (C5/C3/C1) | See **Summary Table** and per-section `**C-band:**` lines. |

**1:1 coverage check vs. `recipient-extension-points.md`:** rows 1–19 of the positive-space inventory each have a section above; rows N1–N3 of the negative-space inventory each have a section above. No row from the Phase 1 inventory is missing.

**Phase 4 wiring:** the per-row C-band anchors `R-RULE-05` (invariant gate) and the Complementarity component of the Phase 4 score: a feature mapped to a C1 surface is auto-REJECTed regardless of value; a feature mapped to a C5 surface enters debate with native-fit baseline; C3 features enter debate with the explicit "new field/hook required" coupling cost surfaced.
