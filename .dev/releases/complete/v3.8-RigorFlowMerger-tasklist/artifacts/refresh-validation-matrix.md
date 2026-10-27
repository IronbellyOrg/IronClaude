---
title: RFMerger Refresh — Validation Matrix (Per-Output Gate Contract)
generated: 2026-06-18
status: refreshed-draft
task: TASK-RF-rfmerger-refresh-20260618-172224 (Step 2.2)
---

# RFMerger Refresh — Validation Matrix

**Purpose.** Per-output validation contract for the **five GATED deliverables** of the RFMerger
refresh: `spec.md`, `prd.md`, `tdd.md`, `artifacts/refresh-requirements-ledger.md`, and
`artifacts/refresh-validation-matrix.md`. Each row pins the gate obligations for one output file
(identified by its absolute path), across eight gate columns plus a halt condition.

**Deliverable taxonomy (resolves spec OQ-2 / the historical 5-vs-7 count).** The deliverable set is
classified as: (1) **5 GATED deliverables** — the five core documents listed above, each gated by a
per-output row here; (2) **2 DERIVED control artifacts** — `artifacts/review-checkpoint.md` and
`artifacts/downstream-task-builder-handoff.md`, which are review-gate / handoff control surfaces
derived from the gated deliverables (not gated content rows here); (3) **1 process report** —
`phase-outputs/reports/final-validation-evidence-report.md`. The historical "7" conflated the 5 gated
deliverables with 2 derived control artifacts; this matrix gates exactly the 5, and the derived
control artifacts + process report are not first-class gated deliverables.

This is a **refreshed-draft document only** — it
authorizes NO implementation tasklist generation, edits no source code, and edits no `.claude/`
mirror. The two human-decision items (P2, P5) are now RECORDED (2026-06-19): P2 =
`retain-with-full-set-revalidation-and-guards`, P5 = `retain-advisory-only` (explicit human choices,
not defaults). With both decisions recorded, downstream implementation-tasklist generation is now
UNBLOCKED; the decisions never blocked document QA/review.

**Integration-boundary rule (P3 DNSP — coherence-9).** Any `sc:tasklist`-specific DNSP surface MUST
reuse the existing `task-builder`-owned `synthetic-dnsp` / DM-003 contract
(`src/superclaude/skills/task-builder/SKILL.md:873-911`) via a **thin adapter** with **contract tests
asserted against task-builder's DM-003 fixtures** — NOT a forked / copied independent schema. A
divergent or copied schema is a halt condition for the P3 source-fidelity gate.

**Gate-execution model (per document).** Gates run serialized with single-cycle fix authorization:
(1) spawn all structural agents in one parallel batch `fix_authorization: false`; (2) spawn all
source-fidelity agents `fix_authorization: false`; (3) spawn all qualitative agents
`fix_authorization: false` with the five adversarial axes embedded; (4) consolidate findings under
`artifacts/qa/`; (5) if any report-only agent FAILs, spawn exactly **one** fix agent
`fix_authorization: true`; (6) spawn report-only verification agents `fix_authorization: false`;
**halt after one failed fix cycle** and record the blocker in the document's Open Questions.

> **Fix-cycle semantics (deliberate stricter override of the task-builder default — with rationale).**
> task-builder's general retry contract is **max-3** fix-verify cycles guarded by the FR-CONV.5/PR-02
> Retry Monotonicity Protocol (regression detection → monotonicity guard → 3-cycle hard cap;
> `task-builder/SKILL.md:1263-1303`). This document-QA matrix deliberately tightens that to a **single**
> fix cycle then HALT-and-record, because these are documents-only deliverables (no executable surface to
> oscillate against) and a second silent fix cycle on prose risks masking a substantive defect behind
> cosmetic churn. The monotonicity and regression guards still apply within the one cycle: a fix that
> introduces a regression (a previously-PASS check now FAIL) or fails to strictly shrink the finding set
> HALTs immediately rather than retrying. This is a stricter, not weaker, gate than the task-builder
> default; it never loosens the FR-CONV.5 guards.

> **Per-document QA agent counts (recomputed from output line counts per MDTM I19 final-document floors:
> <500 lines = 6 agents, 500-1500 = 8 (4+4), 1500-3000 = 10, >3000 = 12).** The per-output rows below pin
> the agent counts at or above these floors; the earlier 3+2+2 / 2+2+1 splits were below floor and are
> superseded:
>
> | Output | Line band | I19 floor | Pinned agent mix (structural + source-fidelity + qualitative) |
> |--------|-----------|-----------|----------------------------------------------------------------|
> | `spec.md` | 500-1500 | 8 | 3 + 3 + 2 = 8 |
> | `prd.md` | 500-1500 | 8 | 3 + 3 + 2 = 8 |
> | `tdd.md` | 500-1500 | 8 | 3 + 3 + 2 = 8 |
> | `refresh-requirements-ledger.md` | <500 | 6 | 2 + 2 + 2 = 6 |
> | `refresh-validation-matrix.md` | <500 | 6 | 2 + 2 + 2 = 6 |
>
> **QA-artifact paths + report schema.** Each gate's report-only and fix agents write to
> `artifacts/qa/phase-3-<lens>-<doc>.md`; the consolidator writes
> `artifacts/qa/phase-3-m3-document-qa-consolidated-findings.md` (this consolidation), and the fix agent
> writes `artifacts/qa/phase-3-m3-document-qa-fix-report.md`. Each report carries: Verdict (PASS/FAIL),
> Items-Reviewed table, deduplicated Findings table (ID · severity · axis · location · fix), and a
> Confidence line.

**Required runtime/sync command strings (UV only; disk-verified).** These exact strings appear in
the Runtime/test gate and Sync gate columns below:

- `uv run pytest tests/tasklist/ -v`
- `uv run pytest tests/tasklist/test_prd_cli.py tests/tasklist/test_prd_prompts.py tests/tasklist/test_autowire.py -v`
- `uv run pytest tests/cli/reflect/ -v`
- `make sync-dev`
- `make verify-sync`

## Per-Output Validation Matrix

Row identifiers are the absolute output paths. Columns are, in order: Structural gate ·
Source-fidelity gate · Qualitative gate · Runtime/test gate · Sync gate · Stale-token gate ·
Human-decision gate · Halt condition.

| Output (absolute path) | Structural gate | Source-fidelity gate | Qualitative gate | Runtime/test gate | Sync gate | Stale-token gate | Human-decision gate | Halt condition |
|---|---|---|---|---|---|---|---|---|
| `/config/workspace/IronClaude/.claude/worktrees/RFMerger-Tasklist/.dev/releases/current/v3.8-RigorFlowMerger-tasklist/spec.md` | 3 report-only structural agents: (a) frontmatter complete (title, version, status, feature_id, parent_feature, spec_type, complexity_score, complexity_class, target_release, authors, created, quality_scores) + **zero remaining template-placeholder sentinels** (the double-brace `SC_PLACEHOLDER` pattern — described here, not written literally, so a blunt grep does not false-positive); (b) FR/NFR IDs + acceptance criteria present; (c) output paths correct + required sections (problem, evidence, scope, solution, key decisions, workflow, FRs, architecture, interface/gate criteria, NFRs, risk, test plan, migration). Conforms to `src/superclaude/templates/documents/release-spec-template.md`. **Note**: the spec frontmatter `status` is a **bare enum** (`status: draft`) by template design (`release-spec-template.md:24`); the plainer frontmatter value vs the prose "🟡 Draft (reviewed-planning)" framing is intentional template conformance, NOT a structural defect. | **3** report-only source-fidelity agents (per I19 8-agent floor for this 500-1500-line doc) read `FINAL-REPORT.md`, `adversarial-validation.md`, `design-rfmerger-proposals.md`, the ledger, and the new `spec.md`; every canonical RFMerger P1-P5 row must be retained / revised / explicit non-goal, mapped to current `src/superclaude/...` evidence; current model is **11-stage with Stage 10.5 reflect gate** (not the stale 10-stage model); P3 synthetic-dnsp must be cross-checked against the existing owner `task-builder/SKILL.md:873-911` (reuse, not divergent contract). | 2 report-only qualitative agents: (a) responsibility boundaries among `sc:tasklist` / task-builder / reflect / CLI validate; (b) Stage 10.5 + `--no-reflect` coherence, no hidden tier mutation, no implementation-ready claim before review. Five adversarial axes embedded. | `uv run pytest tests/tasklist/ -v` — require task items to add/refresh tests for retained RFMerger behavior (P1 `## Execution Context`, P3 DNSP guard + `source: "synthetic-dnsp"`, P4 gate-results passthrough). | After source edits (none expected for spec.md itself), if any `src/superclaude/...` surface is touched downstream: `make sync-dev` then `make verify-sync`; artifacts must live under the release dir or `src/superclaude/...`; never stage `.claude/{skills,commands,agents,hooks,templates}`. | No stale `/config/.claude`, `/rf:*`, `.gfdoc`, `llm-workflows`, or `sc:task-unified` token may remain operative (i.e., as an edit target or current guidance); historical tokens permitted only as HISTORICAL-ONLY citations with a current rebase target named. | Spec must NOT auto-default P2 or P5; both are now RECORDED (2026-06-19) as explicit human `retain-*` choices (P2 `retain-with-full-set-revalidation-and-guards`, P5 `retain-advisory-only`), not defaults. With both recorded, downstream implementation-tasklist generation is UNBLOCKED; the decisions never blocked this spec's QA. | Any structural / source-fidelity / qualitative agent reports FAIL after one serialized fix cycle; or any P1-P5 row missing/unmapped; or any stale edit target remains operative; or product direction auto-defaults P2/P5; or an implementation-ready claim is made before the review checkpoint. |
| `/config/workspace/IronClaude/.claude/worktrees/RFMerger-Tasklist/.dev/releases/current/v3.8-RigorFlowMerger-tasklist/prd.md` | 3 report-only structural agents: (a) frontmatter + lifecycle fields (id, title, description, version, status, type, priority, related docs, tags, review info, `task_type: static`); (b) completeness checklist present; (c) dependencies / upstream-downstream / change-impact / review-cadence / living-document contract table. Conforms to `src/superclaude/templates/workflow/05_prd_template.md`; lifecycle positions PRD=Requirements. | **3** report-only source-fidelity agents (per I19 8-agent floor for this 500-1500-line doc) map product outcomes to current users + source-of-truth constraints from research; no claim weakens the `src/superclaude/...` SoT discipline; PR-3 synthetic-dnsp cross-checked against the existing owner `task-builder/SKILL.md:873-911`. | 2 report-only qualitative agents check non-goals: no hidden feedback-driven tier mutation (determinism preserved), no `.claude/` source edits, no duplicate RF runtime/session manager (R5/R6 non-goals), no implementation-ready claim before review. | Existing PRD/autowire suites must stay green: `uv run pytest tests/tasklist/test_prd_cli.py tests/tasklist/test_prd_prompts.py tests/tasklist/test_autowire.py -v`. | `make sync-dev` then `make verify-sync` if any `src/superclaude/...` surface is later touched; PRD itself writes only under the release dir; never stage `.claude/` mirrors. | No stale `/config/.claude`, `/rf:*`, `.gfdoc`, `llm-workflows`, `sc:task-unified`, or "10-stage-only" framing promoted to current guidance; historical mentions must be cited HISTORICAL-ONLY with current rebase target. | PRD records P2 = `retain-with-full-set-revalidation-and-guards` (from {`defer`, `retain-with-full-set-revalidation-and-guards`}) and P5 = `retain-advisory-only` (from {`defer`, `retain-advisory-only`}) as RECORDED (2026-06-19) explicit human choices, not defaults. With both recorded, downstream implementation-tasklist generation is UNBLOCKED. | Product direction auto-defaults P2 or P5; or claims implementation readiness before document review; or weakens source-of-truth constraints; or any structural/fidelity/qualitative agent FAILs after one serialized fix cycle. |
| `/config/workspace/IronClaude/.claude/worktrees/RFMerger-Tasklist/.dev/releases/current/v3.8-RigorFlowMerger-tasklist/tdd.md` | 3 report-only structural agents: (a) TDD frontmatter + self-check (`feature_id` ≠ `[FEATURE-ID]`, `spec_type` ∈ valid enum, `target_release` ≠ `[version]`, complexity fields populated); (b) component inventory; (c) test plan section. Conforms to `src/superclaude/examples/tdd_template.md`. | **3** report-only source-fidelity agents (per I19 8-agent floor for this 500-1500-line doc) map technical design to current `src/superclaude/...` files/tests and historical P1-P5 evidence; DNSP/guard (reusing the existing `task-builder/SKILL.md:873-911` `synthetic-dnsp` contract, not a new one), gate-results passthrough (20-check gate, not 17), and Execution Context block (no schema collision with `task-builder/SKILL.md:1066,1231`) trace to current surfaces or explicit non-goal. | 2 report-only qualitative agents check boundaries among `sc:tasklist`, task-builder, reflect, and CLI validate; reflect UC-2 P1-P5 kept strictly separate from canonical RFMerger P1-P5. | TDD test plan must add/refresh tests for `--no-reflect`, Stage 10.5, `sc:task` naming, stale-token prevention, and retained RFMerger features; reflect-guard suite verified via `uv run pytest tests/cli/reflect/ -v`. | `make sync-dev` then `make verify-sync` for any later `src/superclaude/...` change; TDD itself writes only under the release dir; never stage `.claude/{skills,commands,agents,hooks,templates}` mirrors. | No stale `sc:task-unified`, `/rf:*`, `.gfdoc`, `llm-workflows` edit target, or direct `.claude` mirror edit remains operative; historical tokens cited HISTORICAL-ONLY only. | TDD test plan for P2 and P5 is active: the human decisions are RECORDED (2026-06-19) as `retain-*`, so tests for the retained forms are active implementation requirements. Downstream implementation-tasklist generation is UNBLOCKED. | Any stale edit target remains operative; or a direct `.claude` mirror edit is proposed; or any agent FAILs after one serialized fix cycle. (P2/P5 decisions are recorded 2026-06-19, so authoring their test work is now permitted.) |
| `/config/workspace/IronClaude/.claude/worktrees/RFMerger-Tasklist/.dev/releases/current/v3.8-RigorFlowMerger-tasklist/artifacts/refresh-requirements-ledger.md` | 2 report-only structural agents ensure all five canonical P1-P5 rows present with the required columns (Historical proposal · Historical evidence · Adversarial/current revision · Current-source implication · Refresh disposition · Human decision status · Validation coverage). | 2 report-only source-fidelity agents verify every row cites BOTH its historical source AND its current-source verification state; each stale token is paired with a current rebase target. | **2** report-only qualitative agents (per I19 6-agent floor for this <500-line doc) ensure the canonical RFMerger P1-P5 taxonomy is kept strictly separate from the reflect UC-2 P1-P5 taxonomy (no semantic substitution, no `P<n>` label reuse), and that the P3 ownership note correctly attributes `synthetic-dnsp` to `task-builder`. | Reviewed together with `spec.md` before downstream handoff; covered by the refreshed test plan via `uv run pytest tests/tasklist/ -v`. | Ledger writes only under the release `artifacts/` dir; `make sync-dev` / `make verify-sync` apply only if a `src/superclaude/...` surface is later changed; never stage `.claude/` mirrors. | All `/rf:*`, `.gfdoc`, `llm-workflows`, `/config/.claude`, `sc:task-unified` mentions appear ONLY as HISTORICAL-ONLY citations, each paired with a current-source rebase target; none presented as a current edit target. | Ledger records P2 = `retain-with-full-set-revalidation-and-guards` and P5 = `retain-advisory-only` as RECORDED (2026-06-19) explicit human choices (not defaults). With both recorded, downstream implementation-tasklist generation is UNBLOCKED. | The RFMerger/reflect P1-P5 taxonomy collision is unresolved; or any row lacks historical source or current-source verification state; or any stale token is presented as a current edit target. |
| `/config/workspace/IronClaude/.claude/worktrees/RFMerger-Tasklist/.dev/releases/current/v3.8-RigorFlowMerger-tasklist/artifacts/refresh-validation-matrix.md` | 2 report-only structural agents ensure every output row carries all eight columns (Structural · Source-fidelity · Qualitative · Runtime/test · Sync · Stale-token · Human-decision · Halt) and one row exists per the five outputs. | 2 report-only source-fidelity agents ensure each gate maps to real validation evidence and that the exact runtime/sync command strings appear verbatim. | **2** report-only qualitative agents (per I19 6-agent floor for this <500-line doc) ensure the human-review checkpoint is explicit and blocking, that no implementation-tasklist generation is authorized inside this task, and that the recomputed I19 gate counts + decision-record references are internally consistent. | Must include the runtime commands verbatim: `uv run pytest tests/tasklist/ -v`; `uv run pytest tests/tasklist/test_prd_cli.py tests/tasklist/test_prd_prompts.py tests/tasklist/test_autowire.py -v`; `uv run pytest tests/cli/reflect/ -v`. | Must include the sync commands verbatim: `make sync-dev` then `make verify-sync`; matrix writes only under the release `artifacts/` dir; never stage `.claude/` mirrors. | No stale `/config/.claude`, `/rf:*`, `.gfdoc`, `llm-workflows`, or `sc:task-unified` token presented as a current edit target anywhere in the matrix. | Matrix reflects P2/P5 as RECORDED (2026-06-19) human decisions (P2 `retain-with-full-set-revalidation-and-guards`, P5 `retain-advisory-only`; explicit choices, not defaults) and states that, with both recorded, downstream implementation-tasklist generation is UNBLOCKED; matrix selects no default. | Any downstream implementation tasklist is generated before human review of refreshed `spec.md`/`prd.md`/`tdd.md`; or any output row is missing a required column; or any required command string is absent. |

## Sprint-compatible downstream conventions (DOWNSTREAM only — not generated here)

Any **future** implementation tasklist generated from the refreshed `spec.md`/`prd.md`/`tdd.md`
(in a separate, later step) MUST preserve Sprint parser conventions so the Sprint CLI can discover
and count its work:

- **Phase filenames** must be literal `phase-N-tasklist.md` (e.g. `phase-1-tasklist.md`), not
  path-prefixed. (CODE-VERIFIED: `src/superclaude/cli/sprint/config.py:15-32`, `134-146`.)
- **Task headings** must match `### T<PP>.<TT>` (e.g. `### T01.02`). (CODE-VERIFIED:
  `src/superclaude/cli/sprint/config.py:34-55`.)
- The optional `Execution Mode` column may use only `claude`, `python`, or `skip`. (CODE-VERIFIED:
  `src/superclaude/cli/sprint/config.py:73-124`.)

> **Scope note.** These are a DOWNSTREAM convention that constrains any FUTURE implementation
> tasklist. **This task generates NO such tasklist** — it records the convention so the later,
> separate `/task-builder` step honors it. The convention is documented here, not exercised here.

## Human-decision gate semantics (P2, P5)

- **P2 (Bounded Patch Loop)** and **P5 (Feedback-Driven Tier Calibration)** are now **RECORDED
  (2026-06-19)** as explicit human choices (not defaults): P2 = `retain-with-full-set-revalidation-and-guards`
  (from {`defer`, `retain-with-full-set-revalidation-and-guards`}); P5 = `retain-advisory-only`
  (from {`defer`, `retain-advisory-only`}). The canonical
  decision records are
  `.dev/tasks/to-do/TASK-RF-rfmerger-refresh-20260618-172224/phase-outputs/reviews/p2-human-decision-record.md`
  and `.../p5-human-decision-record.md`; each recorded decision is propagated to all four document
  carriers (`spec.md`, `prd.md`, `tdd.md`, `refresh-requirements-ledger.md`).
- The P2/P5 decisions gate **downstream implementation-tasklist generation ONLY**. They do
  **not** block document QA/review — structural, source-fidelity, and qualitative gates above run
  to completion regardless of P2/P5 state.
- With **both** decisions now recorded in the refreshed documents, implementation-tasklist generation is
  **UNBLOCKED** (subject to the review checkpoint passing). No gate in this matrix selects a default
  for P2 or P5; the recorded values are explicit human choices (auto-defaulting either would have been a halt condition).

## Authorization boundary — NO implementation tasklist generated in this task

This task authors **documents only**. **NO implementation tasklist generation is authorized inside
this task.** It does not invoke `task-builder` to generate implementation tasks, does not edit
source code, and does not edit `.claude/` mirrors. The actual `/task-builder` invocation from the
refreshed spec/PRD/TDD is a separate, later, non-blocking step that may run only after the review
checkpoint records both the P2 and P5 decisions.
