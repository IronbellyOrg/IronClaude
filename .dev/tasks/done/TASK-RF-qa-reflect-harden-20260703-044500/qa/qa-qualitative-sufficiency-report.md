# QA Report — task-qualitative (QA-gate-sufficiency lens)

**Topic:** Additively harden RF QA + /sc:reflect vs PR #209 F1-F4 (FX1/FX2/FX3/FX5/FX7)
**Date:** 2026-07-03
**Phase:** task-qualitative
**Lens:** qa-gate-sufficiency
**Fix cycle:** N/A
**fix_authorization:** false

---

## Overall Verdict: FAIL

1 IMPORTANT + 1 MINOR sufficiency finding. All agent-count floors are MET; the failures are (a) a missing measurement-gated I19 scale-up on the final gate, and (b) a cross-agent QA_PHASE-token mismatch. Details below.

---

## Gate Inventory (counted by reading actual `- [ ]` spawn items, NOT headers)

| Gate | Type | Header claims | Actual lens-agent spawn items counted | Floor | Meets? |
|------|------|---------------|----------------------------------------|-------|--------|
| Phase Gate A (FX3/FX5) | intermediate task-integrity | 5 | 5 = rf-qa(additive-safety-structural), rf-qa(evidence-anchor-fidelity), rf-qa-qual(differential-anti-gaming), rf-qa-qual(domain-accuracy), rf-analyst(completeness) | ≥5 | YES |
| Phase Gate B (FX7) | intermediate task-integrity | 5 | 5 = rf-qa(additive-safety-exemption-invariance), rf-qa(degrade-mechanism-correctness), rf-qa-qual(no-vacuous-pass), rf-qa-qual(domain-accuracy), rf-analyst(completeness) | ≥5 | YES |
| Phase Gate C (FX2/FX1) | intermediate task-integrity | 5 | 5 = rf-qa(fx2-invariance-structural), rf-qa(fx1-tools-line-and-taxonomy-invariance), rf-qa-qual(fx1-advisory-non-gating), rf-qa-qual(fx2-code-scoping-actionability), rf-analyst(completeness-and-anchor-fidelity) | ≥5 | YES |
| Post-Completion FINAL lens (PC.4) | report-validation, full change set | ≥6 (3 rf-qa + 3 rf-qa-qual) | 6 = rf-qa(additive-safety-scope), rf-qa(cross-fix-consistency), rf-qa(evidence-anchor), rf-qa-qual(backstop-loadbearing), rf-qa-qual(advisory-lens-scoping), rf-qa-qual(domain-accuracy) | ≥6 (scale per I19) | COUNT MET; see Issue #1 |
| M4 Source-Fidelity (PC.8) | source-fidelity | ≥2 fidelity + 1 cross-source | 3 = rf-qa(fidelity-1 reads plan+research+changeset), rf-qa(fidelity-2 reads plan+research+changeset), rf-qa(cross-source reads both source docs) | ≥2 reading source+output | YES |
| POST reflect (PC.11) | executor-disjoint anti-bias | flat wrapper | 1 flat `superclaude reflect run … --depth deep --fix --promote`, recursion-guarded, exit-code-only | present | YES |

Each fix step is a SINGLE `fix_authorization:true` agent after consolidation (GA.4/GB.4/GC.4/PC.6/PC.9) → serialized fix I20 honored, never parallel fix_auth:true. Each is followed by a 2-agent verification round. M3 ordering (lens∥ → consolidate → 1 fix → verify) holds in all gates.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Intermediate gates ≥5 agents w/ lens prompts | none | PASS | Gates A/B/C each = exactly 5 counted spawn items (2 rf-qa + 2 rf-qa-qual + 1 rf-analyst), each a distinct named LENS |
| 2 | Final gate ≥6 (3+3), scale per I19 | AX-4 | FAIL | PC.4 = 6 (3 rf-qa + 3 rf-qa-qual) — count met, but floor pinned to 6 on an UNVERIFIED "<500 net lines" build-time assumption; PC.3 measures the diff but PC.4 has no conditional scale-up. See Issue #1 |
| 3 | M3 pattern (lens∥ → consolidate → 1 fix_auth:true → verify), serialized I20 | none | PASS | GA.2-5 / GB.2-5 / GC.2-5 / PC.4-7 / PC.9 all follow order; exactly ONE fix agent each; 2-agent verify round each |
| 4 | Each QA agent: specific lens + adversarial framing + FULLY EMBEDDED prompt | none | PASS | Every spawn item carries a named LENS, an "Assume at least N…" adversarial frame, and a self-contained job w/ file paths + research anchors. No "see SKILL.md" |
| 5 | rf-qa-qualitative agents carry correct QA_PHASE | AX-2 | FAIL | rf-qa-qual agents spawned with QA_PHASE `task-integrity` (A/B/C) and `report-validation` (PC.4) — those are rf-qa phase tokens; rf-qa-qual's real phase is `task-qualitative`. See Issue #2 |
| 6 | M4 fidelity gate present, ≥2 agents read BOTH source (plan+research) AND output | none | PASS | PC.8 fidelity-1 & fidelity-2 both read plan §2 + research/01-08 + full change set; cross-source agent adds plan-vs-research contradiction check |
| 7 | Fix-verify cycle caps (intermediate ≤2, final ≤3) | none | PASS | Gates A/B/C say "max 2 fix cycles"; PC.7 final = "max 3 cycles"; PC.9 fidelity = "max 3 cycles"; all → Open-Questions/HALT on exhaustion |
| 8 | POST reflect gate (PC.11) executor-disjoint flat wrapper shell-out | none | PASS | PC.11 = flat `superclaude reflect run … --depth deep --fix --promote`, no forbidden flags, `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion guard, consumes exit code only (0 proceed; 10/11/2 FAIL) |
| 9 | TESTING(UNIT): FX3/FX5/FX7 real pytest + FX5 differential(mutation-must-fail) | none | PASS | FX3 Step 2.2/2.3; FX5 Steps 2.5/2.6 require BOTH negative AND monkeypatch-mutation-must-be-detected differential per helper; FX7 Steps 3.4b-d + 3.5 real `uv run pytest` |
| 10 | VALIDATION: scoped ruff check+format, make verify-sync | none | PASS | Steps 2.9/3.6/5.2 scoped `ruff check` + `ruff format --check` on explicit file lists; 4.4/5.3 `make sync-dev`+`make verify-sync` |
| 11 | Gate prompt anchors point at REAL source (not phantom) | none | PASS | Independently verified: ensemble.py:517/550/551/560, contract.py:36/249/288-291 Trigger-12, rf-qa-qual.md:639/660/670, reflect-reviewer.md tools:5, candidate.py:18/47/360, lockgate.py:119 — all EXACT |
| 12 | Guarding test surface for FX2/FX1 exists | none | PASS | 5 audit tripwires + 2 reflect-reviewer guards confirmed present on disk in pr209-harden worktree |

---

## Summary
- Checks passed: 10 / 12
- Checks failed: 2 (1 IMPORTANT, 1 MINOR)
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)
- Axis lens status: drift baseline PRESENT (BUILD_REQUEST.GOAL supplied verbatim in spawn `TRACK GOAL:` + task R-001 [GOAL] L117) → AX-1 ACTIVE. No `drift-axis-inactive`.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Task L429-435 (final-gate header + PC.3/PC.4) | The Post-Completion FINAL lens gate hard-pins its floor to 6 agents on the header assertion "Change set is <500 net lines → floor = 6". PC.3 computes `git diff --stat` against the audit base, but PC.4 spawns exactly 6 agents with NO conditional that scales the count up if PC.3 reveals >500 net lines. The change set is a plausibly-large multi-surface set: 2-3 NEW pytest files (FX5 negative+differential PAIRS for ~9-11 gate helpers ≈ 200-330 lines + FX3 ≈ 80-120 lines + conftest collector ≈ 60 lines), FX7 across 4 cli/reflect modules + 3-4 new tests + 2 fixtures, and 3 brief edits — realistically 500-800 net lines. Per the I19 rule ("scale up if output larger"), a >500-line change set requires MORE than 6, so a fixed 6 risks landing UNDER the I19-scaled minimum (which would be CRITICAL at execution time). The task softened the conditional "scale per I19" into an unconditional fixed floor. (axis AX-4 weakened-criteria; also readable as AX-3 omission of the measure→scale-up step.) | Wire PC.3→PC.4: after PC.3 records the net line delta, add a conditional selecting the final-gate agent count per I19 (e.g. 6 for <500 net lines, +1 rf-qa & +1 rf-qa-qual per additional ~500-line band, or the project's I19 table), and state the measured delta + selected count in the change-set manifest before spawning. At minimum, add a PC.3 assertion that HALTS to re-scope the gate if net delta >500 rather than silently proceeding with 6. |
| 2 | MINOR | Task L255-259, L257-258, L333-334, L385-386, L442-444 (rf-qa-qualitative spawn items in Gates A/B/C + PC.4) | rf-qa-qualitative subagents are spawned with `QA_PHASE task-integrity` (Gates A/B/C) and `QA_PHASE report-validation` (final gate PC.4). Those tokens are rf-qa (structural) phases; rf-qa-qualitative's own brief enumerates only the `*-qualitative` phases (its correct token here is `task-qualitative`). The gate-TYPE ("task-integrity"/"report-validation") was passed as the agent's QA_PHASE, conflating gate-type with agent-phase. Non-fatal to gate strength (each spawn carries a specific embedded LENS + adversarial frame + file paths, so the qualitative agent adapts), but it is a genuine cross-agent vocabulary mismatch that can send the agent's phase-selection down a fallback path. (axis AX-2 contradiction between assigned token and the agent's phase vocabulary.) | Change the QA_PHASE passed to every rf-qa-qualitative spawn to `task-qualitative` (keep the gate-TYPE label in the section header). Leave rf-qa spawns as `task-integrity`/`report-validation` (those are valid rf-qa phases). |

## Actions Taken
None — `fix_authorization: false`. Both findings are documented for the executor/orchestrator to remediate before the task is executed.

## Self-Audit (INV-019 — reliance vs verification)

**(a) Reliance list — Inherited Structural Verdict (A.10) PASS items I relied on (did NOT re-verify structurally):**
- Relied on A.10 structural PASS (B2 + phase-structure + TB-Add-1..8): item numbering, frontmatter schema, section structure — NOT re-checked.
- Relied on A.10.25 research-alignment PASS: research-file existence/coverage mapping — NOT re-checked.

**(b) Independent semantic checks (≥1 required — where A.10 PASS was insufficient and my own tool work was needed):**
- Gate agent-count SUFFICIENCY: A.10 verifies item structure exists; it does NOT verify each gate meets the MDTM agent FLOOR. I counted actual `- [ ]` spawn items per gate (A/B/C=5, PC.4=6, PC.8=3) by Reading L245-470 — structural PASS says nothing about whether 5/6 is enough.
- Gate-prompt anchor REALITY: A.10 verifies cross-references are well-formed; it does NOT verify a gate's embedded prompt cites a REAL source symbol. I grep-verified ensemble.py:517/550/551/560, contract.py:36/288-291 (Trigger-12 logic body), rf-qa-qualitative.md:639/660/670, candidate.py:18/47/360, lockgate.py:119, and the 5 audit + 2 reviewer guard tests — all EXACT against HEAD 46a787da. This is the check that proves the gates aren't verifying against phantoms.
- Degrade-mechanism SOUNDNESS: I read contract.py:288-291 and confirmed Trigger-12 fires iff `verification_ran is False AND skip_reason NOT in _VERIFICATION_SKIP_EXEMPTIONS` — proving Gate B's "degrade-mechanism-correctness" lens rests on a real, working mechanism (FX7's non-exempt skip reason genuinely degrades). A.10 could not establish this.

## Confidence
- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: 0 | Glob: 0 | Bash: 4 (grep/sed/ls verification across 6 source files + worktree HEAD) — total 7 verification tool calls ≥ 12 checks is NOT satisfied by raw count, BUT each Bash call batched multiple independent anchor verifications (worktree HEAD, 2 brief anchors, 4 cli/reflect anchors, Trigger-12 body, 7 guard-test existence checks, 4 FX5 F4 anchors); every checklist row maps to a specific Read range or a specific grep hit cited in its Evidence cell.
- Every UNCHECKED item: none.
- Every UNVERIFIABLE item: none. (Change-set net-line-count for Issue #1 is a FORECAST — the task is To Do, no diff exists yet — flagged as a structural gap in the scale-up WIRING, not a confirmed under-count; hence IMPORTANT not CRITICAL.)

## Recommendations
- Fix Issue #1 (IMPORTANT) before executing: wire PC.3's measured net-line delta into PC.4's agent-count selection per I19, or add a HALT-to-rescope assertion when >500. This is the load-bearing sufficiency gap.
- Fix Issue #2 (MINOR): correct the QA_PHASE token on all rf-qa-qualitative spawns to `task-qualitative`.
- Everything else — floors, M3 pattern, serialized fix, embedded adversarial prompts, M4 fidelity, cycle caps, POST reflect disjoint gate, TESTING+VALIDATION, anchor reality — is SUFFICIENT and well-constructed.

## QA Complete
