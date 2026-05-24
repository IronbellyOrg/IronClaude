# Checkpoint Report — CP-P03-END

**Phase:** Phase 3 — Recipient Integration Surface & Invariant Bound
**Task:** T03.04 — Checkpoint: End of Phase 3
**Tier:** LIGHT
**Roadmap Items:** R-008, R-009, R-010
**Source Tasks:** T03.01, T03.02, T03.03
**Generated:** 2026-05-15

---

## Purpose

Confirm the invariant bounds and extension-point contracts are precise enough to serve as hard constraints in the Phase 4 adversarial debate.

## Artifact Presence

| Artifact | Path | Present |
|---|---|---|
| Invariant bounds (INV-01..INV-05) | `artifacts/invariant-bounds.md` | **NO — missing** |
| Extension-point contracts | `artifacts/extension-point-contracts.md` (22,320 bytes, 277 lines) | Yes |
| Task-builder adjacency analysis | `artifacts/task-builder-adjacency.md` (18,471 bytes, 350 lines) | Yes |

**Gap:** `invariant-bounds.md` — the deliverable of T03.01 (R-008) — does not exist under `artifacts/`. T03.02 and T03.03 ran (their dependency on T03.01 was effectively satisfied by the INV-01..INV-05 labels carried verbatim from the sprint specification — see `extension-point-contracts.md:9-19` which anchors the labels and explicitly notes "When `invariant-bounds.md` (T03.01) lands, each `INV-NN` reference below resolves to a worked-example-backed section"), but the worked-example-backed invariant evidence file required by AC1+AC2 of this checkpoint was never produced.

## Checkpoint Table

| Acceptance Criterion | Source Task | Verification | Status |
|---|---|---|---|
| `invariant-bounds.md` has one evidenced section per INV-01..INV-05 | T03.01 | File does not exist under `artifacts/`. `ls artifacts/` enumerated; `find … -name "invariant*" -o -name "*bound*"` returns nothing. The labels INV-01..INV-05 are present *as anchor references* in `extension-point-contracts.md:9-19` and `task-builder-adjacency.md:8-15`, but neither file carries the per-INV section structure (precise rule + side-tagged `file:line` + worked failure example + violating-feature typology) required by T03.01 AC1–AC4. | **Fail** |
| Each invariant section has a worked failure-mode example | T03.01 | Cannot evaluate — source file does not exist. The reject-criterion bullets in `extension-point-contracts.md` (e.g., lines 260–261, 64–66, 73–74) describe failure *typologies* of donor features that would violate each INV-NN, but they are not worked examples of the invariant's failure mode in the sense T03.01 specifies (which calls for a concrete scenario demonstrating *what breaks* when the invariant is removed). | **Fail** |
| `extension-point-contracts.md` has admit + reject criteria per extension point | T03.02 | 22 rows present (19 positive-space at §60–225 + 3 negative-space at §230–263), matching 1:1 with the 19+N1+N2+N3 inventory in `recipient-extension-points.md` (T01.01). Every section contains explicit **Admit:** and **Reject:** subsections; spot-checked rows 1 (lines 60–67), 7 (114–122), 14 (177–185), and N1 (230–243) confirm structure. Negative-space rows N1–N3 correctly state `Admit: Nothing` (contractually correct for constraint surfaces). AC2 self-attestation at line 271 confirmed. | **Pass** |
| Every reject criterion cross-references an INV-NN | T03.02 | Spot-check of reject bullets: line 65 (`→ **INV-05**`), line 66 (`→ **INV-01**`), line 90 (`→ **INV-01**, **INV-02**`), line 260 (`→ **INV-01**`), line 261 (`→ **INV-01**, **INV-02**`) — pattern `→ **INV-` appears consistently. AC3 self-attestation at line 272 confirmed. Summary table at lines 33–54 also maps every row to one-or-more INV-NN labels. | **Pass** |
| `task-builder-adjacency.md` states an unambiguous definition-vs-execution routing rule | T03.03 | §2 (line 164 "The Definition-vs-Execution Routing Rule") states the rule as a single quoted block at line 168: features shaping *what* work is defined route to `task-builder`; features shaping *how* work executes route to the `/task` executor. INV-05 cross-reference present at §3 (lines 252, 256, 261–267) with explicit identification of routing-rule violation as "exactly the failure mode INV-05 prevents" (line 267). Routing-Outputs-for-Phase-4 table at §4 (line 313+) applies the rule to candidate donor features. | **Pass** |

## Verification Methodology

1. **Artifact presence:** `ls artifacts/` enumerated; `find … -name "invariant*" -o -name "*bound*"` confirmed `invariant-bounds.md` is absent. `extension-point-contracts.md` and `task-builder-adjacency.md` confirmed present with non-trivial size and structure.
2. **Extension-point contract structure:** `grep '^### ' extension-point-contracts.md` returned 22 section headers (19 positive + 3 negative); spot-check confirmed every section has explicit `**Admit:**` and `**Reject:**` subsections.
3. **INV-NN cross-reference:** spot-check at lines 64–66, 73–74, 90–91, 260–261 confirmed each reject bullet ends with `→ **INV-NN**` references; summary table at lines 33–54 maps every row to its protected INV labels.
4. **Routing rule:** `grep -n 'Routing Rule\|definition.*execution\|INV-05' task-builder-adjacency.md` returned hits at the expected §2/§3 anchors (lines 164, 168, 252, 256, 261–267).

## What's Missing and Why It Matters

The missing `invariant-bounds.md` is **load-bearing for Phase 4**. The sprint specification frames INV-01..INV-05 as hard constraints in the adversarial debate; Phase 4 needs:

- A precise testable rule per INV-NN (not just the one-line labels in `extension-point-contracts.md:13-17`),
- A `file:line` enforcement/statement citation per INV-NN inside `task/SKILL.md` (and `task-builder/SKILL.md` where applicable),
- A worked failure-mode example per INV-NN (so a debater can demonstrate *what concretely breaks* if the invariant is loosened),
- A violating-feature typology per INV-NN (so Phase 4 can pattern-match donor features to invariant violations).

Phase 4's R-RULE-05 invariant gate auto-REJECTs C1 features, and `extension-point-contracts.md` already classifies surfaces by C-band — so the contracts side of the input is intact. But debaters cannot defend a REJECT verdict with only the one-line sprint-spec labels; they need the worked-example evidence T03.01 was scoped to produce.

## Acceptance Criteria (T03.04)

1. `CP-P03-END.md` exists and contains `Overall: Pass`. — **NOT MET** (Overall: Fail; see remediation below)
2. All five checkpoint-table rows are marked Pass. — **NOT MET** (rows 1–2 are Fail)
3. Report confirms Phase 4 has both its hard-constraint inputs (invariant bounds, extension-point contracts). — **NOT MET** for invariant bounds; **MET** for extension-point contracts and task-builder adjacency.

## Remediation Required Before Phase 4

**Required action:** Execute T03.01 (`Define invariant bounds INV-01..INV-05`) to produce `artifacts/invariant-bounds.md` with the four-part section structure (precise testable rule, side-tagged `file:line` evidence, worked failure-mode example, violating-feature typology) for each of INV-01..INV-05. Then re-run T03.04 to re-evaluate rows 1–2; expected outcome on re-run is Pass for rows 1–2 and Overall: Pass.

**Effort estimate:** M (per the original T03.01 sizing in `phase-3-tasklist.md:13`). MCP requirement: auggie MCP `mcp__auggie-mcp__codebase-retrieval` against `task/SKILL.md` and `task-builder/SKILL.md` source-of-truth copies under `src/superclaude/skills/` (R-RULE-10).

**Phase 4 readiness:** Phase 4 must NOT begin until `invariant-bounds.md` exists. The two artifacts that did land (`extension-point-contracts.md`, `task-builder-adjacency.md`) are usable as-is and require no rework; T03.01's output slots in beside them without retroactive changes to either file (the INV-NN labels they cite are stable and sourced from the sprint specification).

## Net-Upgrade Questions Forwarded to Phase 4 (cumulative, from prior checkpoints)

From T01.03 (Phase 1):
- **D01** — Add declarative `allowed-tools` frontmatter slot to `/task` skill?
- **D04** — Promote donor's Compliance axis into `/task` task-file schema?
- **D15** — Do donor pre-flight checks belong on `/task` or on task-builder?
- **D21** — Should per-phase/per-item test-baseline snapshot attach to First Item Protocol?

From T02.05 (Phase 2):
- **D26** — Should `/task` grow a feedback/calibration store at Post-Completion Validation to capture tier-override events and completion-quality signals?

(No new net-upgrade questions surfaced during Phase 3; the invariant-bounds and extension-point-contracts work is constraint-side, not capability-side.)

---

**Overall: Fail**

Phase 3 is incomplete. Two of three Phase 3 artifacts (`extension-point-contracts.md`, `task-builder-adjacency.md`) are present, well-structured, and satisfy their per-task acceptance criteria. The third — `invariant-bounds.md` (T03.01 / R-008) — was not produced; the file does not exist under `artifacts/`. Phase 4 cannot proceed until T03.01 runs and produces the worked-example-backed invariant evidence file, because Phase 4's adversarial debate uses the invariant bounds as hard constraints and the one-line sprint-spec labels carried in `extension-point-contracts.md:13-17` are insufficient evidence for a debater to defend a C1 auto-REJECT verdict. Re-execute T03.01, then re-run T03.04.
