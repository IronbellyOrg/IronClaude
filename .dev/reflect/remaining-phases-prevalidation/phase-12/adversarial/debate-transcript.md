# Phase 12 Pre-Validation — Adversarial Debate Transcript (Mode B, inline)

**Generated:** 2026-06-02
**Source under debate:** TASK-RF-20260531-042405 §Phase 12 (Steps 12.1–12.5, PG12.1, PG12.2), lines 669–702.
**Authority:** master:§Flaw 5 (L522–532); BUILD-REQUEST §Scope (skill alignment); task objective 11 (L100); actual skill at `src/superclaude/skills/sc-roadmap-protocol/`.
**Method:** Sub-agent spawn unavailable in validation context → INLINE adversarial. Three advocate lenses steelmanned per item: **opus:architect** (necessity, sequencing, substrate-correctness), **sonnet:scribe** (prose specificity, citation accuracy, no-aspirational-content), **haiku:qa** (src/-not-.claude rule, sync gate, overturned-framing checks). Verdicts merged.

## Ground-truth facts established before debate (grep/Read verified)

| Fact | Evidence |
|---|---|
| SKILL.md is **529L**, not 1094L as task claims | `wc -l src/superclaude/skills/sc-roadmap-protocol/SKILL.md` |
| extraction-pipeline.md **531L** (task says 700L); templates.md **426L** (task says 519L); validation.md **343L** (task says 474L); scoring.md **263L** (task says 322L) | `wc -l refs/*.md` |
| SKILL.md currently has **0** occurrences of PipelineEnvelope / superclaude.contracts / code_assertions / verify-implementation / envelope | `grep -c` returned 0 → prose genuinely lags; Phase 12 necessary |
| `superclaude.contracts` exposes ID_PATTERNS, CONVERGENCE_THRESHOLDS, GATE_FIELD_NAMES, RETURN_CONTRACTS, THRESHOLDS | `contracts/__init__.py:64,86,97,122` + docstring L11–28 |
| **No `superclaude.contracts.parsers` submodule exists** | `ls contracts/parsers*` → none; only `__init__.py` |
| Frontmatter parser lives in `envelope.py`; legacy `gates.py:_parse_frontmatter` (roadmap) still present (R1.6 target) | `grep def *frontmatter`: envelope.py owns parse; pipeline/gates.py:125 `_check_frontmatter`; roadmap/gates.py:178 `_parse_frontmatter` |
| `PipelineEnvelope` class + `POST_EXTRACTORS` dispatch live in `envelope.py:128,688` | grep |
| `GateCriteria.code_assertions` slot + `CodeAssertion` live at `cli/pipeline/models.py:91,121,142` | grep |
| R1.4 tool-write surface real: `tool_writer.py`, `templates/tool_schemas/*.schema.json` (extract/extract_tdd/generate/diff/debate/score/merge), `templates/extract.md.j2` | `ls`/grep |
| **R1.3 CodeAssertion is runtime-INERT in production** (certify runs outside `execute_pipeline`; CERTIFY_GATE never evaluated; envelope-None fail-open shim) | `.dev/reflect/r1-3-uc2-validation/REPORT.md:30–53,82–83` (DEV-R13-001 HIGH, DEV-R13-002 runtime-dormant) |
| `CONVERGENCE_THRESHOLDS["sc:roadmap"] = (0.7, 0.5)` is the **adversarial convergence** high/low pair | `contracts/__init__.py:86–89` |
| Actual `refs/scoring.md` is about **complexity scoring + PRD/TDD input-type detection + milestone counts + persona confidence** — NOT adversarial convergence thresholds | Read scoring.md: thresholds are `<0.4/0.4-0.7/>0.7` complexity tiers, `≥5` detection scores — none map to CONVERGENCE_THRESHOLDS |
| `refs/adversarial-integration.md` exists (506L); Phase preamble L671 + OQ#4 L208 say PRESERVE per MVR | Read; task L671 |
| **Objective 11 (L100) lists adversarial-integration.md among the 5 files to update** — contradicts the PRESERVE directive | task L100 vs L671/L208 |

---

## Item 12.1 — Update SKILL.md

**opus:architect (KEEP):** Necessary and correctly sequenced. SKILL.md has zero new-vocabulary occurrences; this is the master:§Flaw 5 prose-drift surface (A9:F-A9-004 "skill described 5 waves, CLI ships 14 steps"). The item enumerates exactly which stale models to replace (markdown-as-substrate, gate=None bypass, fail-open fidelity_checker, return-True stubs, missing verify-implementation/contracts/tool-write) and ties each to a concrete R-delivery. The ≥4-Edit-pass instruction (precedent A) is sound for a 529L file. Sequencing-after-R1.6 is enforced by PG11.2's "proceed to Phase 12" gate.

**sonnet:scribe (REFACTOR-minor):** Two prose hazards. (a) The item cites SKILL.md as "1094L per research/01 §D" — the real file is 529L. A worker reading "1094L" then opening a 529L file may suspect a truncated/wrong file and stall, or hunt for a phantom larger file. The stale line count should be dropped (it's decorative, not load-bearing) or corrected. (b) The item says "the absence of `verify-implementation` (R1.5 added)". R1.5's verify-implementation status must be checked against R1.6 reality before the prose asserts it is "live and wired" — Step 12.1 should cite it as a defined terminal step, not over-claim runtime behavior. Otherwise specificity is strong.

**haiku:qa (KEEP):** src/-not-.claude rule is explicitly and correctly stated ("edits go to `src/superclaude/skills/` FIRST, NEVER directly to `.claude/skills/`... Never `git add .claude/skills/...`"). make sync-dev + verify-sync gate present. No overturned-framing risk in 12.1's enumerated list itself (it lists deletions R1.6 made, which is correct). PASS.

**MERGE → KEEP (with scribe's line-count caveat noted as advisory, not blocking).** The item is necessary, correctly sequenced, src-correct, and specific. The "1094L" stale citation is a documentation-hygiene nit the executor will self-correct on Read; not a structural defect.

---

## Item 12.2 — Update refs/extraction-pipeline.md (R1.4 tool-write)

**opus:architect (KEEP):** The R1.4 tool-write substrate is real (`tool_writer.py`, `tool_schemas/extract.schema.json`, `extract.md.j2` all verified present). The item names concrete targets: replace embedded `build_extract_prompt` examples with references to the schema + j2 template, cite tool-write-vs-markdown dual-write dispatch, cite Contract #3 generator-side `roadmap_ids ⊆ envelope.spec_ids`. This is exactly the master:§Flaw 2 (generator/validator asymmetry) prose alignment. Specific and grounded.

**sonnet:scribe (KEEP):** Names the file, the section concern ("how build_extract_prompt is structured"), the concrete replacement artifacts, and the dispatch model. No aspirational content — every cited artifact exists. Good citation discipline.

**haiku:qa (KEEP):** src-only + sync gate present. One watch-item: the prose must say dual-write (markdown rendered FROM tool output), not "markdown path deleted" — R1.4 cadence is ≥3 release cycles side-by-side per L186/L97 before deletion. The item correctly says "tool-write vs markdown dual-write", so it does not overstate. PASS.

**MERGE → KEEP.** Necessary, specific, grounded, src-correct, dual-write framing accurate.

---

## Item 12.3 — Update refs/templates.md (R0.3/R1.1 registry + R1.2 envelope)

**opus:architect (KEEP):** This is the strongest-specified item. It already carries a REMEDIATION annotation (sc:reflect C1 downstream 2026-05-31) that **resolves the parsers question correctly**: it explicitly states "no `superclaude.contracts.parsers` submodule exists; the parser is owned by the envelope module" — which matches ground truth (`ls contracts/parsers*` → none; parse lives in `envelope.py`). It cites the real registry names (ID_PATTERNS / CONVERGENCE_THRESHOLDS / GATE_FIELD_NAMES / RETURN_CONTRACTS) and the PipelineEnvelope shape from §MVR §1. Substrate-correct.

**sonnet:scribe (KEEP):** Precise, names every vocabulary token and the §MVR §1 anchor. The "frontmatter parsed exactly once by the PipelineEnvelope post-step extractor (in envelope.py)" statement is accurate and forestalls the very drift that produced A11:F-A11-010 (two disagreeing frontmatter parsers). Excellent — this item models what 12.1/12.4 should aspire to.

**haiku:qa (KEEP):** src-only + sync gate present. The parsers-submodule correction means this item will NOT perpetuate the Step 13.3 phantom (`superclaude.contracts.parsers.parse_frontmatter`, which does not exist) — in fact 12.3 is the antidote. PASS.

**MERGE → KEEP.** Best-specified item in the phase; resolves the parsers ambiguity correctly against ground truth.

---

## Item 12.4 — Update refs/validation.md (R1.6 fail-closed, R1.5 verify-implementation, R1.3 code_assertions)

**opus:architect (REFACTOR):** Necessary, but contains the phase's single substantive correctness hazard. The item instructs prose to describe "R1.3 `GateCriteria.code_assertions` slot" alongside "R1.6 deletion of fail-open defaults (now ALL gates fail-closed)". The R1.3 UC-2 audit (`.dev/reflect/r1-3-uc2-validation/REPORT.md:43,82–83`) establishes that the headline CodeAssertion is **runtime-inert in production** through R1.3 — certify runs outside `execute_pipeline`, CERTIFY_GATE is never evaluated, and an envelope-None fail-open shim keeps the assertion dormant (DEV-R13-001 HIGH gate-bypass + DEV-R13-002 runtime-dormant). R1.6 was the intended cutover that deletes the shim and plumbs the envelope. So the item must NOT let prose claim "code_assertions fire at runtime" as a flat present-tense capability. The correct framing depends on R1.6's actual landing: if R1.6 closed DEV-R13-001/002, prose may say code_assertions are evaluated at gate time; if R1.6 only partially closed them, prose must describe code_assertions as a CI-validated slot (dispatch-reachability test) whose runtime evaluation is gated on the certify-through-execute_pipeline wiring. The item as written ("the R1.3 GateCriteria.code_assertions slot") is under-specified on this axis — it does not instruct the executor to verify the R1.6 runtime state before asserting runtime firing.

**sonnet:scribe (REFACTOR):** Agrees. Add explicit instruction: "Verify against `.dev/reflect/r1-3-uc2-validation/` + R1.6 closure whether code_assertions are runtime-evaluated or CI-only as of the prose-writing moment; describe the actual state, not the design intent. Do NOT write 'code_assertions fire at runtime' for source-tree assertions unless R1.6 demonstrably wired certify through execute_pipeline." Also: "convergence-aware SPEC_FIDELITY_GATE (R1.6 cutover)" must be checked to have actually landed (L187 ties the gate=None deletion to making SPEC_FIDELITY_GATE convergence-aware) — prose should not assert it if R1.6 deferred it.

**haiku:qa (REFACTOR):** src-only + sync gate present (PASS on that axis). But this is exactly the "watch for prose claiming behaviors the corrected R1.3 framing overturned" trap from the validation brief. The item needs the anti-overclaim guard injected. REFACTOR.

**MERGE → REFACTOR.** Add a runtime-vs-CI verification clause and an explicit anti-overclaim guard (see verdict file replacement text).

---

## Item 12.5 — Update refs/scoring.md (Contract #8 cross-link only)

**opus:architect (REFACTOR / near-DISCARD):** The item's premise is built on a **phantom file description**. It says scoring.md is "scoring rubric prose for adversarial layer; ... numeric thresholds (Contract #8 — no duplicated literals)" and instructs replacing each threshold-literal with `(see superclaude.contracts.CONVERGENCE_THRESHOLDS["sc:roadmap"])`. Ground truth: the real `refs/scoring.md` (263L, not the claimed 322L) is about **complexity scoring** (`complexity_score` weighted formula), **PRD/TDD input-type detection** (5-signal `≥5` scorers), **milestone-count classification** (`<0.4` LOW / `0.4–0.7` MEDIUM / `>0.7` HIGH), and **persona confidence**. NONE of these thresholds are convergence thresholds. `CONVERGENCE_THRESHOLDS["sc:roadmap"] = (0.7, 0.5)` is the adversarial debate high/low pair — semantically unrelated to complexity tiers or input-type detection. Cross-linking the complexity `>0.7` tier to `CONVERGENCE_THRESHOLDS` would be a **factual error that creates new drift** (the exact failure class master:§Flaw 5 / A10:F-A10-003 warns against). The item must NOT mechanically rewrite these literals.

**sonnet:scribe (REFACTOR):** Agrees the literal-replacement instruction is wrong-targeted. If Contract #8 ("no duplicated threshold literals in skill prose") has any ripple into scoring.md at all, it would be limited to literals that genuinely duplicate a `superclaude.contracts` entry — and after inspection there are none (complexity tiers and detection scores are scoring-engine constants, not contract-registry entries). The honest refactor is: the cross-link is conditional ("if Contract #8 ripples" per objective 11 L100), and inspection shows it does NOT ripple — so the correct action is a no-op/verify, possibly DISCARD. At most, add a one-line note that scoring.md's thresholds are complexity/detection constants owned by the scoring engine, distinct from CONVERGENCE_THRESHOLDS, to prevent a future maintainer from wrongly hoisting them.

**haiku:qa (REFACTOR):** src-only rule fine. But mechanically executing "replace each threshold-literal with CONVERGENCE_THRESHOLDS cross-link" would inject false references — a regression. The item also asserts "`refs/adversarial-integration.md` remains untouched (PRESERVE)" which is correct and good. The defect is purely the mis-scoped cross-link target. REFACTOR to a verify-and-likely-noop.

**MERGE → REFACTOR.** Reframe from "mechanically cross-link every threshold literal" to "verify whether any scoring.md literal genuinely duplicates a `superclaude.contracts` entry; ground truth says none do (complexity/detection constants ≠ CONVERGENCE_THRESHOLDS), so the expected outcome is a no-op or at most a one-line disambiguation note." Preserve the adversarial-integration.md PRESERVE assertion.

---

## Item PG12.1 — Spawn rf-qa-qualitative (documentation-alignment)

**opus:architect (KEEP):** Correct gate. ADVERSARIAL STANCE + fix_authorization:true matches the project's rf-qa pattern (memory feedback_rfqa_adversarial_pattern). Checks (a)–(f) are well-chosen: sample-5-citations-and-grep, no stale refs to deleted code, adversarial-integration.md untouched, verify-sync PASS, zero .claude/ staging refs, Contract #8 cross-links present in scoring.md.

**sonnet:scribe (REFACTOR-minor):** Check (f) "Contract #8 cross-links present in scoring.md" inherits 12.5's defect — if 12.5 correctly results in a no-op (no valid cross-links exist), then PG12.1 check (f) would FALSE-FAIL a correct outcome and force a wasted fix cycle. Check (f) must be softened to "Contract #8 disposition recorded for scoring.md (cross-link IF AND ONLY IF a literal duplicates a contract entry; no-op otherwise)". Check (b) is excellent (greps for `_cross_refs_resolve`, fail-open `found=True`, `gate=None` — all R1.6 deletions).

**haiku:qa (KEEP):** Check (e) "zero references to .claude/ paths in commit/staging instructions" directly enforces the CLAUDE.md ABSOLUTE RULE — strong. Aggregation path is under the task's phase-outputs tree (not .claude/). Spawn-fail fallback present. PASS modulo the 12.5-coupled check (f).

**MERGE → REFACTOR (minor, scoped to check (f)).** Soften check (f) to match the corrected 12.5 disposition so a correct no-op cannot false-fail the gate.

---

## Item PG12.2 — Act on Phase 12 QA verdict

**opus:architect (KEEP):** Standard conditional-action gate. PASS→proceed-decision + Phase 13; FAIL→fix in src/ only, re-sync, re-spawn, max 3 cycles, HALT+escalate. Halt-precedence correct.

**sonnet:scribe (KEEP):** "edit `src/superclaude/skills/` only — NEVER `.claude/skills/`" reiterated. No prose defects.

**haiku:qa (KEEP):** src-only rule + sync gate + cycle cap + escalation all present. PASS.

**MERGE → KEEP.**

---

## Convergence summary

| Item | architect | scribe | qa | MERGED |
|---|---|---|---|---|
| 12.1 | KEEP | REFACTOR(nit) | KEEP | **KEEP** |
| 12.2 | KEEP | KEEP | KEEP | **KEEP** |
| 12.3 | KEEP | KEEP | KEEP | **KEEP** |
| 12.4 | REFACTOR | REFACTOR | REFACTOR | **REFACTOR** |
| 12.5 | REFACTOR | REFACTOR | REFACTOR | **REFACTOR** |
| PG12.1 | KEEP | REFACTOR(minor) | KEEP | **REFACTOR (check f only)** |
| PG12.2 | KEEP | KEEP | KEEP | **KEEP** |

Convergence: 7/7 items reach unanimous or strong-majority merged verdict. No DISCARDs (every item targets a real master:§Flaw 5 surface). Two substantive REFACTORs (12.4 overturned-framing guard; 12.5 mis-scoped cross-link target) + one minor gate-coupling REFACTOR (PG12.1 check f). Cross-cutting finding: **objective 11 (L100) lists adversarial-integration.md among files to update, contradicting the PRESERVE directive at L671/L208** — flagged as a task-level inconsistency (the Phase 12 STEPS are correct; the objective text is stale).
