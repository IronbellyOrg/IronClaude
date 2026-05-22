# Synthesis 10 — Conditional Sections (§9, §10, §11, §16, §17)

**Component:** Task-Builder Convergence v3.9 — internal-framework generation-time skill
**Status:** Complete
**Date:** 2026-05-14
**Inputs:** research/00-prd-extraction.md, research/14-invariant-preservation.md, qa/research-gate-consolidated.md

> **NO N/A rule (rf-qa-qualitative.md:564 Adaptation Guidance):** Every section below
> carries content. Sections that do not apply to this component are marked N/A *with a
> brief rationale*, never omitted.

---

## §9 State Management *(N/A for this component)*

**Rationale:** This component is a generation-time skill executed at MDTM task-file
emission. It has no persistent client-side state, no global state, no URL state, and no
form state. The closest analog to "state" is the on-disk MDTM task file itself, which is
documented in §7 Data Models (Entity 4 — Per-Item Checklist Schema, PRD §25.4) and the
persistent-`.dev/tasks/`-artifact invariant (NFR-CONV.8). The only inter-process datum
that crosses an agent boundary — the `## Inherited Structural Verdict` block (FR-CONV.3,
PRD §25.2) — is a single-cycle, at-most-once-per-cycle message governed by the
freshness/reinjection rule (INV-002), not durable state; see §14.1 Logging and §5 API
Specs (Phase Contract 25.5).

| State concern | Disposition for this TDD |
|---|---|
| Server State | N/A — no server; generation-time skill, not a service (NFR-CONV.5) |
| Global Client State | N/A — no client UI |
| Local Component State | N/A — single-process subagent execution per spawn |
| URL State | N/A — no routing |
| Form State | N/A — no forms |
| Persistent task-file state | Documented in §7 Data Models (PRD §25.4) and §14.1 Logging — governed by NFR-CONV.8 |
| Inter-cycle verdict carryover | Explicitly **forbidden** as durable state — INV-002 reinjection rule forces a fresh verdict every fix cycle (FR-CONV.3 Negative Criterion) |

---

## §10 Component Inventory *(N/A for this component)*

**Rationale:** This component has no frontend UI. The only "user" is an agent-operator
inspecting spawn-logs and the generated MDTM file. There are no pages, routes, or shared
UI components. The structural decomposition that *does* exist — the rf-* agent topology
(rf-task-builder, rf-qa, rf-qa-qualitative, rf-analyst, rf-team-lead) — is documented in
§6.2 Component Diagram, not here. See §11 for the agent-operator interaction model.

| Frontend concern | Disposition |
|---|---|
| Page / Route Structure | N/A — no routing, no pages |
| Shared Components | N/A — no UI components |
| Component Hierarchy | The *agent* hierarchy (rf-* agents) is documented in §6.2 Component Diagram; the rf-qa → rf-qa-qualitative phase contract is §5 API Specs (PRD §25.5) |
| Design System / Tokens | N/A — output surfaces are plain-text logs and Markdown |
| State-bound components | N/A — see §9 |

---

## §11 User Flows & Interactions *(Reduced — agent-operator only)*

**Reduction rationale:** The sole interaction surface is an agent-operator invoking the
task-builder skill via the Skill tool (Claude Code) and inspecting the resulting MDTM
file plus QA reports. There is no end-user UI flow. One primary flow is documented below.

### §11.1 Primary Agent-Operator Flow: Generating an MDTM task file

```mermaid
sequenceDiagram
    participant U as Agent-Operator
    participant TBS as task-builder Skill
    participant TBA as rf-task-builder Agent
    participant Q as rf-qa (task-integrity)
    participant QQ as rf-qa-qualitative (task-qualitative)
    participant TL as rf-team-lead (escalation)

    U->>TBS: Invoke /task-builder with BUILD_REQUEST
    TBS->>TBA: Spawn with BUILD_REQUEST + Execution Context REQs (FR-CONV.2)
    TBA->>TBA: Emit MDTM file with ## Execution Context header (after frontmatter)
    TBA-->>TBS: Return task file path
    TBS->>Q: Spawn task-integrity QA on MDTM file
    Q->>Q: Run 20-item + 8 TB-Add (FR-CONV.1) checklist
    Q-->>TBS: Emit verdict table
    alt Verdict PASS
        TBS->>QQ: Spawn task-qualitative with ## Inherited Structural Verdict block (FR-CONV.3)
        QQ->>QQ: Run 15-item + Five Adversarial Axes overlay (FR-CONV.4) + Self-Audit (INV-019)
        QQ-->>TBS: PASS verdict + Self-Audit listing
        TBS-->>U: Return MDTM file path + QA reports
    else Verdict FAIL within I16 cycle limit
        TBS->>TBA: Fix-cycle (FR-CONV.5 monotonicity + regression guards)
        TBA->>TBA: Apply fixes; re-emit
        Note over TBA,Q: Repeat until PASS or [HALT-MONOTONICITY] / [HALT-REGRESSION] / I16 cap
    else Partition exhaust (FR-CONV.6)
        Q-->>TBS: Emit synthetic-dnsp HIGH finding (5 fixed fields)
        Note over TBS: N-1 partitions continue (NFR-CONV.10); manual review per recommendation field
    else All-partitions exhaust
        Q-->>TL: Activate rf-team-lead.md:417 escalation (3 fix cycles per phase)
        TL->>U: HALT and ask user after 3 cycles — NO synthetic-dnsp emitted
    end
```

### §11.1 Steps (textual narrative)

1. Agent-operator invokes the task-builder skill with a BUILD_REQUEST.
2. task-builder spawns rf-task-builder with the BUILD_REQUEST + Execution Context
   requirements (FR-CONV.2).
3. rf-task-builder emits the MDTM file with the `## Execution Context` header at the top
   (References / Source areas / Key constraints — strictly **no specific file paths** in
   the header; per-item Context fields still carry file:line citations per
   evidence-bound-item / NFR-CONV.7).
4. task-builder skill spawns rf-qa task-integrity on the MDTM file.
5. rf-qa runs the 20-item structural checklist + the new 8 TB-Add checks (FR-CONV.1);
   TB-Add-2 emits `[ADVISORY]` and does not block, TB-Add-1/3..8 block on failure.
6. rf-qa emits a PASS/FAIL verdict table under zero-trust semantics — any gap of any
   severity = FAIL (NFR-CONV.9, rf-qa.md:144-146).
7. If PASS: task-builder spawns rf-qa-qualitative with the `## Inherited Structural
   Verdict` block (FR-CONV.3, PRD §25.2) injected verbatim into the spawn prompt.
8. rf-qa-qualitative runs the 15-item checklist + Five Adversarial Axes overlay
   (FR-CONV.4) + Self-Audit mandate (INV-019) and emits its verdict.
9. If both PASS: agent-operator receives the task-file path + QA reports.
10. If FAIL: fix-cycle activates with FR-CONV.5 monotonicity + regression guards; the
    cycle terminates on `[HALT-MONOTONICITY]`, `[HALT-REGRESSION]`, or the per-gate I16
    cap (research-gate 3 / synthesis-gate 2 / report-validation 3 / task-integrity 2 /
    qualitative 3, per rf-task-builder.md I16 — SC-4).
11. If a partition agent exhausts its escalation ladder: a synthetic-dnsp HIGH finding
    emits (FR-CONV.6, PRD §25.3); the remaining N-1 partitions continue to completion
    per NFR-CONV.10 / INV-021 parallel-research preservation.
12. If zero partitions succeeded: the existing rf-team-lead.md:417 escalation (3 fix
    cycles per phase) activates instead of DNSP — these two paths are mutually exclusive
    (SC-2).

### §11.1 Success Criteria

- Generated MDTM file passes 20-item structural + 8 TB-Add + 15-item qualitative +
  5-axis overlay + Self-Audit.
- No `[HALT-MONOTONICITY]` or `[HALT-REGRESSION]` triggered on a legitimate slow-shrink
  fix cycle (`|F|` shrinking even by 1 must continue — FR-CONV.5 Negative Criterion).
- Token cost ≤10% above pre-merge baseline (NFR-CONV.4).
- `## Execution Context` header contains no file paths; per-item Context fields retain
  file:line citations (TB-Add-7 / TB-Add-8 cross-validation).

### §11.1 Error Scenarios

- TB-Add-1..8 fires on a structural defect (placeholder scan, item-count bounds,
  clarification adjacency, circular dependency, granularity, format consistency,
  Execution-Context source-area reappearance, per-item file:line citation) → fix-cycle.
- Self-Audit shows zero independent semantic checks → K-003 audit FAIL (the first 5
  rf-qa-qualitative runs after FR-CONV.3 lands are audit targets).
- `|F_{n+1}| >= |F_n|` → `[HALT-MONOTONICITY] |F|=<n>` and loop exit.
- Item X.Y was PASS at cycle N, FAIL at cycle N+1 → verbatim regression halt message,
  exits **before** the monotonicity check (regression > monotonicity precedence).
- Partition agent escalation ladder exhausts → synthetic-dnsp emission with 5 fixed
  fields; identical dedup-key collapses with a `found N times` note.

---

## §16 Accessibility Requirements *(N/A for this component)*

**Standard:** WCAG 2.1 AA is the project standard for user-facing UI components; this
component has no UI.

**Rationale:** Internal-framework component with no user-facing UI. All observable
surfaces are plain-text spawn-logs and Markdown files (the MDTM task file and QA
reports). Agent-operator interaction occurs via the Skill tool inside Claude Code, which
inherits its accessibility properties from the Claude Code parent application. Markdown
output is screen-reader-compatible by default and requires no additional accessibility
engineering by this component.

| Requirement | Disposition |
|---|---|
| Keyboard Navigation | N/A — no UI |
| Screen Reader Support | N/A — Markdown/plain-text output is screen-reader-compatible by default |
| Color Contrast | N/A — plain text, no color-encoded information |
| Focus Management | N/A — no UI |
| Alternative Text | N/A — no images in generated artifacts |
| Form Labels | N/A — no forms |
| ARIA Roles | N/A — no markup surface |

---

## §17 Performance Budgets *(Reduced — token-cost only)*

**Reduction rationale:** No frontend and no backend service exist, so the only meaningful
performance dimension is token cost (NFR-CONV.4). NFR-CONV.5 forbids new external
dependencies and synchronous network calls, so wall-clock is dominated by LLM inference
time rather than by any FR addition.

### §17.1 Frontend Performance
N/A — no frontend. No bundle size, no render budget, no Core Web Vitals apply.

### §17.2 Backend Performance
N/A — generation-time skill, not a long-running service. No request latency, no
throughput, no connection-pool budgets apply.

### §17.3 Token Cost Performance (NFR-CONV.4)

**Budget:** ≤10% token-cost increase over the pre-merge task-builder baseline per
equivalent BUILD_REQUEST. **Measurement:** sample 5 representative BUILD_REQUESTs; record
pre-merge and post-merge token counts; the ratio must be ≤1.10 (NFR-CONV.4, OPEN-TOKEN).

| Contributor | Pre-merge baseline | Post-merge target | Notes |
|---|---|---|---|
| Per-BUILD_REQUEST total token cost | Baseline | ≤110% (ratio ≤1.10) | Hard ceiling — NFR-CONV.4 |
| FR-CONV.3 Inherited Structural Verdict block | N/A | ~1–3% per run | Largest single contributor; verbatim verdict table can be **summarised** rather than copied if the ceiling is breached (K-010 contingency / §19 rollback option) |
| FR-CONV.2 Execution Context header | N/A | <1% per run | 3 labeled lines + header markdown; degrades to References-only on minimal BUILD_REQUEST |
| FR-CONV.4 Five Adversarial Axes overlay | N/A | <1% per run | One `axis` column added per Items-Reviewed row + a short axes subsection |
| FR-CONV.1 TB-Add checklist additions | N/A | <1% per run | 8 append-only checklist lines in rf-qa.md / SKILL.md |
| FR-CONV.5 / FR-CONV.6 (monotonicity + DNSP) | N/A | <2% per run | Stop-conditions + synthetic-finding emission; only materialises on retry/exhaust paths |

### §17.4 Wall-Clock

No new external network calls and no new dependencies (NFR-CONV.5) — all gate operations
use existing local tools (Read, Grep, Glob, Bash). Per-run wall-clock is dominated by LLM
inference time; the FR additions add a small, bounded number of additional local checks
(TB-Add-1..8, monotonicity comparison, dedup-key check) that are negligible against
inference cost. The parallel-research cohort (NFR-CONV.10) is preserved, so partition QA
does not serialize.

---

## Cross-References

- §9 persistent task-file state → §7 Data Models (PRD §25.4), §14.1 Logging, NFR-CONV.8
- §10 agent hierarchy → §6.2 Component Diagram; phase contract → §5 API Specs (PRD §25.5)
- §11 flow guards → §14 Invariant Preservation (INV-002, INV-012, INV-019, INV-021),
  SC-2 / SC-4 (research-gate-consolidated.md)
- §17 token ceiling → NFR-CONV.4, K-010, OPEN-TOKEN

**Status:** Complete
