# QA Report — task-qualitative (qa-gate-sufficiency lens)

**Topic:** Differential Backtest/Eval Harness for sc:troubleshoot Pipeline Hardening Closure (E1-E5)
**Date:** 2026-06-11
**Phase:** task-qualitative / qa-gate-sufficiency
**Fix cycle:** N/A (report-only, fix_authorization: false)
**Task file:** /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-evals-20260611-160018/TASK-RF-troubleshoot-hardening-evals-20260611-160018.md

---

## Lens Scope

This review ONLY assesses QA-GATE SUFFICIENCY of the QA gates encoded inside the generated
task file. Structural correctness (numbering, item structure, TB-Add-*) is inherited PASS
from rf-qa A.10 + A.10.25 and is NOT re-verified. The mandate: enumerate every QA gate, COUNT
agents per gate, identify each lens, and apply the MDTM minimums as a REJECTION mechanism.

## BUILD_REQUEST stated intensity
QA_INTENSITY = standard, QA_GATE_REQUIREMENTS = PER_PHASE. Task Key Constraints (I22) declares:
"intermediate/phase gates = 3 agents; final/phase-gate lens QA = 7 agents (3 rf-qa structural +
3 rf-qa-qualitative content + 1 domain lens); fidelity gate = 2 agents; max 2 fix cycles; 2
verification agents." NOTE: this self-declared "intermediate = 3 agents" is BELOW the MDTM
intermediate-gate minimum of 5 — flagged below if any intermediate gate is encoded.

---

## Per-Gate Agent-Count Table

Agent counts are from DIRECT READS of each gate block (not grep guesses). For each phase gate the
agents are: N lens agents (report-only, fix_authorization:false) + 1 serialized fix agent
(fix_authorization:true) + 2 verification agents (1 rf-qa + 1 rf-qa-qualitative, report-only).

| Gate | Type | Lens agents (report-only) | Fix agent | Verify agents | TOTAL distinct agents | MDTM min | Verdict |
|------|------|---------------------------|-----------|---------------|-----------------------|----------|---------|
| Phase 1 | Setup-only (no buildable artifact) | — | — | — | 0 (correctly none) | n/a | OK (no gate required) |
| Phase 2 gate (L210-246) | Phase/final-document | 7 (3 rf-qa + 4 rf-qa-qualitative*) | 1 rf-qa | 2 (1+1) | 10 | 6 | PASS |
| Phase 3 gate (L280-316) | Phase/final-document | 7 (3 rf-qa + 4 rf-qa-qualitative*) | 1 rf-qa | 2 (1+1) | 10 | 6 | PASS |
| Phase 4 gate (L358-394) | Phase/final-document | 7 (3 rf-qa + 4 rf-qa-qualitative*) | 1 rf-qa | 2 (1+1) | 10 | 6 | PASS |
| Phase 5 gate (L420-456) | Phase/final-document | 7 (3 rf-qa + 4 rf-qa-qualitative*) | 1 rf-qa | 2 (1+1) | 10 | 6 | PASS |
| Final gate 6.2 (L468-490) | Final-document (complete harness) | 7 (3 rf-qa + 4 rf-qa-qualitative*) | 1 rf-qa | 2 (1+1) | 10 | 6 | PASS |
| Fidelity gate 6.3 (M4/I21, L494-500) | Source-fidelity (vs RELEASE-SPEC) | 2 rf-qa | 1 rf-qa | 2 (1+1) | 5 | 2 (intensity=standard fidelity) | PASS |
| POST reflect 6.4 (L504) | Self-run anti-bias (penultimate) | 1 (sc:reflect --mode post, self-run) | — | — | 1 | self-run | PASS |

*Lens composition note: the declared shape is "3 rf-qa structural + 3 rf-qa-qualitative content +
1 domain lens". In every phase the 1 domain lens is itself spawned as an `rf-qa-qualitative` agent,
so the realized split is 3 rf-qa + 4 rf-qa-qualitative = 7 lens agents. This SATISFIES (exceeds) the
MDTM phase-gate minimum of 6 (3 rf-qa + 3 rf-qa-qualitative). The domain lens being rf-qa-qualitative
is appropriate — domain/semantic differential-replay concerns are content judgments, not structural.

**No intermediate research/synthesis gates exist** (grep `rf-analyst` = 0). CORRECT: this is a BUILD
task; the research+synthesis gates already ran upstream in the task-builder pipeline (A.8). The
5-agent intermediate-gate minimum therefore does not apply to any gate inside this generated file.

---

## Findings

### Instruction 1 — Enumerate every gate, count agents, identify lenses → PASS

Six QA gates + one self-run reflect gate are encoded. Every phase gate (2,3,4,5 + final 6.2)
carries exactly 7 lens agents, well above the 6-agent phase-gate minimum. No gate is under-strength.

Per-gate lens identity (each lens is SPECIFIC, not generic "check everything"):
- **Phase 2:** (struct) G1-no-caret correctness; subprocess-seam+teardown integrity; G2/G3
  skip-guard+no-leaked-worktree. (content) actionability/executability; collision-boundary+path.
  (domain) git-replay differential semantics (E4 pin, no cross-escape worktree leak).
- **Phase 3:** (struct) backtest_status enum+derivation; run_report.py model-idiom; JSON-Schema
  Draft202012 fidelity. (content) separation-invariant+advisory-signoff; proxy-honesty no-oversell.
  (domain) ReplayExecutor seam fidelity vs LifecycleExecutor.
- **Phase 4:** (struct) §8.3 per-escape mapping completeness; skip-guard (no xfail/importorskip,
  parents[3]); aggregation+status wiring. (content) OLD=MISS real-negative-witness; collision+
  distinct-nodeids. (domain) E4 HEAD-drift + E3/E4 dual-evaluator pair.
- **Phase 5:** (struct) conftest+pollution-guard; test-green evidence (0 failed/0 errored);
  lint+format parity. (content) UV-only discipline; green-means-correct-skip semantics. (domain)
  end-to-end harness coherence chain.
- **Final 6.2:** (struct) template-conformance; internal-consistency; evidence-quality+collision.
  (content) actionability/non-vacuity; numbers/metrics; crossref-chain. (domain) NFR-1 fidelity+
  proxy-honesty.

Every lens differs from every other; no two lenses overlap into a generic catch-all. PASS.

### Instruction 2 — MDTM minimums + builder honored intensity → PASS

All five phase/final gates = 7 lens agents ≥ 6 minimum. The BUILD_REQUEST specified standard
PER_PHASE 6-7 agent gates; the builder encoded 7 per phase gate — at the top of the stated band,
NOT fewer. No REJECTION-RULE trigger fires (no final/phase gate < 6; no intermediate gate < 5
because there are no intermediate gates in a build task). The I22 self-declared "intermediate = 3
agents" line is a latent contradiction with the MDTM 5-agent intermediate minimum, BUT it is INERT
here: zero intermediate gates are actually encoded, so the weaker number is never applied. Noted as
MINOR latent-contradiction below; does not affect any encoded gate's strength.

### Instruction 3 — M3 lens-based flow + I20 serialized fix → PASS

Every gate follows M3 exactly: all lens agents fix_authorization:false IN PARALLEL → consolidate
(deduped, FAIL-if-ANY-issue-of-ANY-severity) → exactly ONE fix agent fix_authorization:true →
2-agent verification round → conditional proceed, max 2 fix cycles (standard intensity). Grep
cross-check: `fix_authorization: true` appears exactly 6 times = exactly one serialized fix agent
per gate (phases 2/3/4/5 + final 6.2 + fidelity 6.3). NEVER two simultaneous fix agents. I20 + M3
fully satisfied. Max-2-cycles (not 3) is correct for standard intensity per I22.

### Instruction 4 — specific lens + adversarial framing → PASS

Every lens and verification spawn carries an explicit ADVERSARIAL STANCE quote ("Assume … at least
N errors … Find them") and a binary PASS/FAIL verdict where ANY discrepancy = FAIL. Report-only
agents are constrained to cite file:line and modify no source. Adversarial framing is uniform and
report-only/fix separation is clean.

### Instruction 5 — I21 source-fidelity gate (M4) present + well-formed + correctly evaluated → PASS

The harness produces Python test code (a multi-file test package), NOT a >500-line document
transforming a source. The per-phase inventories (Steps *.QA.1) flag any single file >500 lines as
an I21 per-file trigger, and the final inventory (6.2.1) re-flags. SEPARATELY, the builder ADDED a
dedicated M4 source-fidelity gate at Step 6.3 (2 rf-qa fidelity agents in parallel) checking the
harness faithfully represents the RELEASE-SPEC: semantic coverage (every §8.3 oracle has a test that
actually asserts it), detail preservation (parent shas, waves, missing-IDs, separation invariant),
and phantom-coverage detection (no test merely names an escape ID without asserting its oracle) —
then consolidate → ONE serialized fix → 2-agent verify, max 2 cycles. This is the correct M4 shape.
I21 was correctly evaluated: code-not-document, so per-file >500-line trigger is conditional, AND a
spec-fidelity gate is additionally present because the harness IS a faithful transform of the
RELEASE-SPEC's §3.1/§8.3/§5.4 contracts. PASS.

### Instruction 6 — explicit checklist items with fully embedded lens prompts → PASS

Every gate agent is an explicit `- [ ]` checklist item with the full lens-specific prompt embedded
inline (adversarial stance string, exact files to read, exact assertions to verify, exact output
report path, binary verdict rule). No item delegates to "see SKILL.md" or uses prose-only framing.
Each item is independently executable by the F1 loop.

### Instruction 7 — POST reflect gate present, self-run, penultimate → PASS

Step 6.4 (L504) spawns `/sc:reflect --mode post --remediate` as a SELF-RUN check (explicitly "NOT a
human-handoff/HALT — record the verdict and proceed"), positioned penultimate (only Step 6.5
frontmatter Done-transition follows). It is executor-disjoint (substitutes `<EXECUTOR_CLASS>` to
exclude the executor's own model class from the heterogeneous reviewer panel), stages untracked
files with `git add -A` first, and diffs against `git merge-base HEAD origin/master` after a
mandatory `git fetch origin`. Records `{verdict, run_id, report}` into the `reflect_post`
frontmatter. Correct UC-2 anti-bias placement. PASS.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | L124 (Key Constraints, I22) | The Key-Constraints intensity line declares "intermediate/phase gates = 3 agents". MDTM intermediate-gate minimum is 5 (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative). This number is INERT (zero intermediate gates are encoded in this build task, so it is never applied), and all PHASE gates are correctly 7. But the bare "= 3 agents" phrasing is a latent contradiction that could mislead a future executor or a downstream task that copies this constraints block. | Clarify the line to read "phase gates = 7 lens agents; (no intermediate research/synthesis gates in this build task — N/A)". Non-blocking; no encoded gate is weakened. |

No CRITICAL or IMPORTANT issues. The single MINOR is a documentation-wording latent contradiction
in the constraints prose, not a weakness in any actual encoded gate. Per the qa-gate-sufficiency
rejection rule, NO gate is under-strength, so no CRITICAL gate-strength FAIL is triggered. However,
per the task-qualitative verdict rule (ANY issue of ANY severity = FAIL), the MINOR drives the
overall verdict to FAIL with a documented, low-cost remediation.

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items I skipped re-checking (Inherited Structural Verdict):**
- Relied on rf-qa A.10/A.10.25 PASS for item structure, numbering, B2, phase-structure,
  research-alignment, and all TB-Add-* — I did NOT re-verify `- [ ]` formatting, section numbering,
  or template conformance of the gate items.

**(b) Independent semantic checks (≥1 required, INV-019) — my own tool work:**
- COUNTED agents in every gate by DIRECT READ of each gate block (Read offsets L206-249, L276-318,
  L354-396, L416-458, L460-548) — not by relying on the gate-header label "7 lens agents". Confirmed
  each phase gate = 3 rf-qa + 4 rf-qa-qualitative lens + 1 fix + 2 verify by reading every spawn item.
- Cross-checked serialized-fix invariant with `grep -c "fix_authorization: true"` = 6, matching
  exactly one fix agent per gate (I20 — no simultaneous fix agents).
- Independently verified the G1 no-caret concern is NOT violated by the `^` occurrences: grep showed
  the only carets are `git cat-file -e <sha>^{commit}` (a peel-to-commit existence probe, correct git
  plumbing), NOT the `<sha>^` parent-decrement hazard; checkout targets use bare shas. This is a
  semantic check rf-qa's structural PASS does not cover.
- Verified `rf-analyst` count = 0 to confirm the absence of intermediate gates is intentional (build
  task), so the 5-agent intermediate minimum correctly does not apply.

## Confidence
Verified: 7/7 instruction-criteria | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 7 | Grep: 3 | Glob: 0 | Bash: 2 (grep cross-checks)
Tool calls (12) ≥ criteria (7) — engagement minimum satisfied; each call mapped to a specific check.

## Recommendations
- Apply the single MINOR fix to L124 (clarify the intensity-constraints wording) — non-blocking,
  ~1-line edit. No gate is under-strength; the harness's QA scaffolding is sound and rejection-grade.

---

VERDICT: FAIL (1 MINOR only — no gate under-strength; all 6 gates meet/exceed MDTM minimums; FAIL is
driven solely by the task-qualitative "ANY issue of ANY severity = FAIL" rule for the L124 latent
wording contradiction. This is NOT a CRITICAL gate-strength rejection.)
