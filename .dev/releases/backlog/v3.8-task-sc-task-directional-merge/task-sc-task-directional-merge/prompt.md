# Directional Merge Sprint — Absorb `/sc:task` into `/task`

> **Usage**: Paste this entire prompt into a fresh Claude Code session opened at `/config/workspace/IronClaude`. It will generate a sprint-compatible tasklist that can be executed via `superclaude sprint run`.

---

## Context

You have access to **one repository** with **two overlapping task-execution surfaces**. The objective is **directional**, not neutral:

- **`/task`** is the **recipient** (base, retained, primary surface going forward)
- **`/sc:task`** is the **donor** (every valuable, unique, complementary feature is to be evaluated for absorption into `/task`; what is not absorbed will be deprecated)

This is **not** a comparison sprint. This is a feature-transfer sprint with adversarial gating.

### Surfaces

1. **`/task` — Recipient (MDTM Task File Executor)**

   | Component | Location | Role in this sprint |
   |-----------|----------|---------------------|
   | Skill package | `.claude/skills/task/SKILL.md` | **Base**. F1 execution loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT). All accepted donor features are integrated here. |
   | Source-of-truth | `src/superclaude/skills/task/` | Canonical edit target |
   | Companion builder | `.claude/skills/task-builder/SKILL.md` | Adjacent surface; transfers that affect work-definition may land here instead of the executor |
   | Phase-gate QA | inside `task/SKILL.md` | Mandatory `rf-qa` between phases; **load-bearing invariant** |
   | Subagent vocabulary | inside `task/SKILL.md` | `rf-analyst`, `rf-qa`, `rf-qa-qualitative`, `rf-assembler`, `rf-task-builder`, `rf-task-researcher`, `Explore`, `general-purpose` |
   | MDTM file consumers | `.dev/tasks/to-do/TASK-*/TASK-*.md` | Real-world usage evidence; compat constraint |

2. **`/sc:task` — Donor (Unified Task Command)**

   | Component | Location | Role in this sprint |
   |-----------|----------|---------------------|
   | Command file | `.claude/commands/sc/task.md` | Donor surface; declares MCP servers, personas, allowed tools |
   | Source-of-truth | `src/superclaude/commands/task.md` | Canonical donor reference |
   | Execution protocol | `.claude/skills/sc-task-protocol/SKILL.md` | Donor protocol; tier classification + TFEP live here |
   | Source-of-truth | `src/superclaude/skills/sc-task-protocol/` | Canonical donor reference |
   | Classification table | inside `sc-task-protocol/SKILL.md` | Candidate feature: STRICT/STANDARD/LIGHT/EXEMPT tier model |
   | TFEP (Test Failure Escalation Protocol) | inside `sc-task-protocol/SKILL.md` | Candidate feature: forensic-pipeline trigger |

### Load-bearing invariants of `/task` — these MAY NOT be broken by any absorbed feature

Any transfer proposal that requires breaking one of the following must be rejected regardless of its value score:

- **INV-01**: F1 loop semantics — READ first unchecked `- [ ]`, EXECUTE exactly as written, UPDATE to `- [x]`, REPEAT. No skipping, no reordering, no out-of-band substitution.
- **INV-02**: Prohibited actions catalog — no working from memory, no modifying checklist items mid-execution, no delegating the F1 loop itself.
- **INV-03**: Phase-gate `rf-qa` invocation between phases (Phase 2+); post-completion `rf-qa` + `rf-qa-qualitative` validation.
- **INV-04**: Resumability — progress recoverable from disk after context compression / session restart.
- **INV-05**: Refusal-of-definition — `/task` does not decide *what* to do; the MDTM file does. The F1 loop only *executes*.

## Your Task

Generate a complete sprint tasklist (index + phase files) in the format used by SuperClaude's sprint CLI. Write the files to:

```
.dev/releases/current/task-sc-task-directional-merge/
├── tasklist-index.md
├── phase-1-tasklist.md
├── phase-2-tasklist.md
├── phase-3-tasklist.md
├── phase-4-tasklist.md
├── phase-5-tasklist.md
├── phase-6-tasklist.md
├── phase-7-tasklist.md
└── phase-8-tasklist.md
```

### Sprint Format Requirements

**Index file** must contain a metadata table and phase file references in this pattern:
```markdown
| Phase N Tasklist | `TASKLIST_ROOT/phase-N-tasklist.md` |
```

**Phase files** must use this task format:
```markdown
### T{NN}.{NN} — {Task Title}
**Roadmap Item IDs**: {cross-refs}
**Tier**: {STRICT|STANDARD|LIGHT|EXEMPT}
**Effort**: {XS|S|M|L|XL}
**Steps**: numbered [VERB] steps
**Acceptance Criteria**: numbered list
**Validation**: numbered list
**Dependencies**: {task IDs or "None"}
```

Task IDs follow `T{phase}.{sequence}` pattern (e.g., T01.01, T04.03). Monitor regex: `T\d{2}\.\d{2}`.

### Sprint Structure (8 Phases)

Design the sprint with these 8 phases. Each phase should have 3–6 tasks. Every task must use the auggie MCP codebase-retrieval tool (`mcp__auggie-mcp__codebase-retrieval`) as the primary search mechanism, with `directory_path` set to `/config/workspace/IronClaude`.

---

#### Phase 1: Recipient & Donor Inventory
**Goal**: Build an asymmetric inventory — recipient extension points on one side, donor feature surface on the other.

Tasks should:
- Use auggie MCP to enumerate `/task`'s **extension points** (places where new capability can attach without disturbing the F1 loop): pre-loop hooks, per-item hooks, phase-gate hooks, post-completion hooks, MDTM frontmatter slots, prohibited-actions list (the negative space), subagent dispatcher
- Use auggie MCP to enumerate `/sc:task`'s **donor features** at concrete granularity (one row per feature, not one row per file): triggering surface, tier classification model, classification header emission, per-tier flow branching, TFEP, MCP server declarations, persona auto-activation, declared allowed-tools, compliance gating, ...
- For every donor feature, record: file:line evidence, current behavior, observable outputs, and a first-pass transferability tag (TRANSFERABLE | ADAPTABLE | NON-TRANSFERABLE | DUPLICATE-OF-EXISTING)
- Produce `recipient-extension-points.md` (one row per extension point)
- Produce `donor-feature-catalog.md` (one row per donor feature with transferability tag)
- Identify any feature in the donor catalog that **`/task` already has** in some form — flag as DUPLICATE-OF-EXISTING for special handling in Phase 4

---

#### Phase 2: Donor Feature Characterization
**Goal**: For every donor feature in the Phase 1 catalog, produce a structured characterization deep enough to debate.

Tasks should:
- Use auggie MCP + `/sc:analyze --focus architecture` patterns on each donor feature individually
- For each feature, document:
  - **What it is** (concise behavioral definition)
  - **How it works** (mechanism + entry/exit conditions + file:line evidence)
  - **What it produces** (artifact, header, side effect, escalation)
  - **What invokes it** (which classifier branch, which user input shape)
  - **What it depends on** (other features, MCP servers, agents, settings)
  - **Standalone value claim** (what capability gain a system would get from this feature — to be challenged in Phase 4)
  - **Coupling cost claim** (what a system has to take on to support it — to be challenged in Phase 4)
- Produce one `feature-{slug}.md` per donor feature
- Apply anti-sycophancy: every value claim must include the conditions under which it does NOT deliver value

---

#### Phase 3: Recipient Integration Surface & Invariant Bound
**Goal**: For each load-bearing invariant of `/task` (INV-01..INV-05), produce a precise definition that the adversarial debate can use as a hard constraint.

Tasks should:
- Use auggie MCP + `/sc:analyze --focus architecture` patterns on `/task` and `task-builder`
- For each invariant, document:
  - The behavioral rule (precise, testable)
  - The file:line where it is enforced or stated
  - The failure mode it prevents (with worked example)
  - The kinds of donor features that would violate it (typology, not enumeration)
- Document the **extension-point contract** for each Phase 1 extension point: what shape of donor feature it can absorb, what it cannot
- Produce `invariant-bounds.md` (one section per INV-NN with file:line evidence)
- Produce `extension-point-contracts.md` (one row per extension point, with admit/reject criteria)

---

#### Phase 4: Adversarial Debate & Stack Rank — `/sc:adversarial` (the core mechanism)
**Goal**: For every donor feature from Phase 1, run a structured `/sc:adversarial` debate to determine whether it should be absorbed, and stack-rank the survivors.

Tasks should:
- For each donor feature, **invoke `/sc:adversarial`** with the feature characterization (Phase 2 artifact) and the invariant bounds (Phase 3 artifact) as the two source documents
- The debate must produce:
  - **Position A — Steelman for inclusion**: the strongest case that `/task` is materially better with this feature absorbed. Must cite file:line evidence from Phase 2; must show the integration sketch (which extension point, what shape of change)
  - **Position B — Steelman against inclusion**: the strongest case for rejection. Must cite (a) invariant violation risk if any, (b) duplication with existing `/task` capability if any, (c) maintenance / cognitive cost, (d) at least one realistic failure mode introduced
  - **Evidence-based weighing**: each side must answer the other's strongest point directly; unanswered points count against that side
  - **Scored verdict** using the rubric below
- Score every feature with the rubric:
  - **V (Value, 1–5)** — capability gain for `/task` if absorbed
  - **C (Complementarity, 1–5)** — fit with F1 loop and phase-gate model. **5** = native fit (lives at an existing extension point with no F1 changes); **3** = lives at a recipient extension point but requires a new field or hook; **1** = requires changing F1 invariants (auto-REJECT)
  - **K (Cost, 1–5)** — integration + ongoing maintenance cost
  - **Net = (V × C) / K** — stack-rank descending
  - **Verdict thresholds**: **ADOPT** (Net ≥ 5), **ADAPT** (3 ≤ Net < 5; absorb with explicit modification), **DEFER** (1.5 ≤ Net < 3; revisit after a named precondition), **REJECT** (Net < 1.5 OR violates any INV-NN)
- Apply **anti-sycophancy gate** (R-RULE-04): any feature whose Position A lacks at least one trade-off acknowledgment is sent back for re-debate
- Apply **invariant gate** (INV-01..INV-05): any feature requiring an invariant break is auto-REJECTed regardless of V
- Produce one `debate-{feature-slug}.md` per feature
- Produce `stack-rank.md` — all features sorted by Net score with verdict column, links to debate artifacts, and the integration sketch for ADOPT and ADAPT features

---

#### Phase 5: Synthesis — Ranked Feature Transfer Manifest
**Goal**: Convert Phase 4 verdicts into a single, ordered feature transfer manifest that drives the merge.

Tasks should:
- Use `/sc:adversarial --depth deep` patterns to merge the Phase 4 per-feature verdicts into a coherent manifest, checking for inter-feature dependencies (a feature scored ADOPT might require another feature scored DEFER)
- For each ADOPT feature: lock in the integration sketch — exact extension point, shape of change, new fields / hooks introduced, observable post-condition
- For each ADAPT feature: define the explicit modification (what changes vs the donor implementation, what is dropped, what is retained)
- For each DEFER feature: define the precondition that would re-enable it (e.g., "after MDTM frontmatter gains a `tier:` field")
- For each REJECT feature: document the rationale terminally; this prevents re-litigation
- Reconcile inter-feature interactions: if ADOPT(A) implies REJECT(B) or vice versa, surface the conflict and resolve with explicit precedence
- Apply the **"absorb patterns, not implementation mass"** principle — extract control patterns, reject ceremony with no behavioral teeth
- Produce `transfer-manifest.md` (the ordered, locked manifest; the binding output of this sprint)
- Produce `rejected-features-ledger.md` (all REJECT and DEFER features with rationale, so they are not silently re-proposed)

---

#### Phase 6: Directional Merge Plan
**Goal**: Convert the transfer manifest into a concrete, sequenced refactoring plan that edits `/task` to absorb features and deprecates `/sc:task`.

Tasks should:
- Use `/sc:roadmap` patterns to convert the manifest into an implementation roadmap with dependency graph
- For every change implied by the manifest, produce a row with:
  - File path (must exist — verify via auggie before writing)
  - What changes (edit-in-place, add hook, add MDTM frontmatter field, rename, delete)
  - Which manifest feature this change implements (one-to-many traceability)
  - Priority tier (P0/P1/P2/P3)
  - Effort estimate (XS/S/M/L/XL)
  - Dependencies on other changes
  - Acceptance criteria (observable post-condition)
  - Risk assessment (invariant the change could violate if applied incorrectly; mitigation)
- Include the **deprecation plan for `/sc:task`**:
  - Soft-deprecation (command emits redirect to `/task` and exits) vs hard-deprecation (file removed) — pick one per artifact and justify
  - Treatment of `.claude/commands/sc/task.md` and `src/superclaude/commands/task.md`
  - Treatment of `.claude/skills/sc-task-protocol/` and `src/superclaude/skills/sc-task-protocol/`
  - Treatment of all references in `.dev/releases/backlog/*` to `sc:task`, `task-unified`, `sc-task-protocol`
  - Treatment of declared MCP servers and personas that were never load-bearing
- Include the **distribution surface refactor**: `superclaude install` behavior, `make sync-dev` filter rules, README rows
- Produce per-area `refactor-{area}.md` (areas: `/task` skill edits, `/sc:task` deprecation, MDTM frontmatter extensions, distribution, references, documentation)
- Produce `merge-master.md` — the unified plan with dependency graph and recommended execution order

---

#### Phase 7: Validation & Adversarial Re-Review
**Goal**: Validate the merge plan adversarially, with re-debate of any item where Phase 6 implementation drifted from the Phase 5 manifest.

Tasks should:
- Use `/sc:adversarial` to debate the merge plan itself with two roles:
  - **Invariant Defender**: scans every Phase 6 change for invariant impact; cites INV-NN evidence
  - **Manifest Auditor**: cross-checks every manifest feature against the Phase 6 plan; flags drops, unauthorized scope expansion, or implementation drift
- Use auggie MCP to re-verify every file reference in the plan
- Check **compat hazards**: does the plan break any in-flight MDTM file under `.dev/tasks/to-do/`? Does it break any sprint already in `.dev/releases/current/`? Does the `/sc:task` deprecation strand any documented workflow?
- Check **traceability gaps**: every ADOPT/ADAPT manifest feature must map to at least one Phase 6 change; every Phase 6 change must trace back to at least one manifest feature
- Check **invariant survival**: after the plan is applied, do INV-01..INV-05 still hold? Run a worked example through the merged `/task` to demonstrate
- Re-score any feature where the plan deviated from the manifest's integration sketch (the V/C/K rubric may now produce a different verdict)
- Produce `validation-report.md` with pass/fail per plan item and per manifest feature
- Produce `invariant-survival-walkthrough.md` — worked example showing the merged surface still honors INV-01..INV-05
- Produce `final-merge-plan.md` — the validated, corrected master plan

---

#### Phase 8: Sprint Checkpoint & Artifact Assembly
**Goal**: Assemble all artifacts into a navigable deliverable and validate sprint completeness.

Tasks should:
- Build `artifact-index.md` linking every artifact in Phases 1–7
- Verify traceability chain: each donor feature in Phase 1 catalog → has a Phase 2 characterization → has a Phase 4 debate with a scored verdict → appears in the Phase 5 manifest (ADOPT/ADAPT) or rejected-features ledger (DEFER/REJECT) → if ADOPT/ADAPT has a Phase 6 change-row → if scoped for change has a Phase 7 validation verdict
- Verify no orphaned artifacts or dead references
- Produce `sprint-summary.md` with: feature counts by verdict, top-ranked accepted features, top-rejected features with rationale, total estimated effort, recommended implementation order, and the rejected-features ledger as a permanent record (so deferred features are not silently re-proposed)
- Final quality gate: all artifacts pass structural validation

---

### Deterministic Rules

Apply these rules in the generated tasklist:

- **R-RULE-01**: Every task that reads code must use `mcp__auggie-mcp__codebase-retrieval` as the primary search tool, with `directory_path` set to `/config/workspace/IronClaude`.
- **R-RULE-02**: Phase sequencing is strict: no phase begins until the prior phase's checkpoint passes.
- **R-RULE-03**: All claims about either surface's behavior must cite specific `file:line` evidence from the repo — no unsupported behavioral claims.
- **R-RULE-04**: Anti-sycophancy gate — every "value" claim for a donor feature must include the conditions under which it does NOT deliver value; every "complementary" claim must include the integration cost. Position A in any debate is sent back for re-debate if it lacks a trade-off acknowledgment.
- **R-RULE-05**: Invariant gate — any donor feature requiring violation of INV-01..INV-05 is auto-REJECTed in Phase 4 regardless of value score. The debate must surface the violation, not paper over it.
- **R-RULE-06**: "Absorb patterns, not implementation mass" — Phase 6 integrations extract the *control pattern*, not the donor's surrounding ceremony. Ceremony without behavioral teeth is REJECTed in Phase 4.
- **R-RULE-07**: Scoring rubric is binding — V × C / K is the canonical Net score; verdict thresholds are ADOPT (≥5), ADAPT (3–5), DEFER (1.5–3), REJECT (<1.5 or invariant violation). Subjective overrides require an explicit "manifest exception" entry in `transfer-manifest.md` with a named justification.
- **R-RULE-08**: Artifacts are written to `.dev/releases/current/task-sc-task-directional-merge/artifacts/`.
- **R-RULE-09**: Each phase ends with a checkpoint table verifying all acceptance criteria.
- **R-RULE-10**: `src/superclaude/` is source of truth; `.claude/` is the dev copy. Every file claim must specify which side it cites. Drift between sides is itself a finding and must appear in Phase 6.
- **R-RULE-11**: The rejected-features ledger is **terminal** — features rejected or deferred in Phase 5 may not be silently re-proposed in Phase 6 or 7. Re-litigation requires explicit re-debate.

### Compliance Tiers

- **Phase 1**: EXEMPT (read-only inventory)
- **Phase 2**: EXEMPT (read-only characterization)
- **Phase 3**: EXEMPT (read-only invariant extraction)
- **Phase 4**: STANDARD (adversarial debate produces artifacts; the V/C/K scoring is binding and must be auditable)
- **Phase 5**: STANDARD (synthesis; produces the binding manifest)
- **Phase 6**: STRICT (refactoring plan that will drive code changes; must verify all file references)
- **Phase 7**: STRICT (adversarial validation of plan that will drive code changes)
- **Phase 8**: LIGHT (assembly and verification)

### MCP Requirements

Every task must specify MCP requirements. Recommended:
- **auggie MCP** (`mcp__auggie-mcp__codebase-retrieval`): Required for ALL code search tasks; `directory_path: /config/workspace/IronClaude`
- **Sequential**: Required for STRICT tier tasks (Phases 6, 7); required for adversarial debate tasks (Phase 4); recommended for synthesis (Phase 5)
- **Serena**: Optional for symbol-level analysis when auggie results need deeper resolution (locating every call-site of a renamed identifier, every reference to a deprecated skill name)
- **Context7**: Not required (no external library docs involved)

---

## Execution

After generating the tasklist files, the sprint can be executed with:

```bash
superclaude sprint run \
  .dev/releases/current/task-sc-task-directional-merge/tasklist-index.md \
  --permission-flag "--dangerously-skip-permissions"
```

Or phase-by-phase:
```bash
superclaude sprint run \
  .dev/releases/current/task-sc-task-directional-merge/tasklist-index.md \
  --start 1 --end 3 \
  --permission-flag "--dangerously-skip-permissions"
```

---

**Now generate the complete tasklist-index.md and all 8 phase files.**
