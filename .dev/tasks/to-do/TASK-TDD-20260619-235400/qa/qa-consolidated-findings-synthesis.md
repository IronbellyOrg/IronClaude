# Consolidated Synthesis-Gate Findings — TASK-TDD-20260619-235400

**Date:** 2026-06-20
**Agents:** 8 (3 rf-analyst + 3 rf-qa + 2 rf-qa-qualitative), partitioned.
**Consolidated verdict: FAIL** (1 IMPORTANT contradiction + minors; fixes in Step 5.19).

## Per-agent verdicts
| Agent | Lens | Files | Verdict |
|-------|------|-------|---------|
| 5.10 analyst A | synthesis-review | 01,02,03 | PASS (3 minor advisories) |
| 5.11 analyst B | synthesis-review | 04,05,06 | PASS (OI-1 table COMPLETE 23 rows; (M,N) exact; D3 present) |
| 5.12 analyst C | synthesis-review | 07,08,09 | PASS (Alt 0 ✓, Q1 BLOCKING ✓, NFR-7 ✓, stub avoids mock gap ✓; 1 minor: Dn label collision) |
| 5.13 rf-qa structure A | structure | 01-04 | PASS (13/13; 3 minor cosmetic) |
| 5.14 rf-qa structure B | structure | 05-09 | PASS (13/13; 2 info) |
| 5.15 rf-qa content | content+paths | all | PASS (0 hallucinated paths; (M,N)+verdict map byte-consistent) |
| 5.16 rf-qa-qual coherence A | coherence | 01-05 | PASS (clean) |
| 5.17 rf-qa-qual coherence B | coherence | 06-09 | **FAIL** (1 IMPORTANT contradiction + 2 minor) |

## Issues (deduplicated, by severity)

### IMPORTANT (must fix in synth files)
- **S1 — 5xx retry contradiction (from 5.17).** synth-06 §12.4 (Retry & Recovery) labels the swarm 5xx retry as "**Immediate**"; synth-08 §17.2 correctly says "retry once with **+2s backoff**." Source `src/superclaude/cli/swarm/dispatch.py:46` = `on_5xx_backoff_sec=2` (and ~L195-276 retry_policy). **synth-06 is WRONG.** FIX: change synth-06 §12.4 to "retry once with 2s backoff (`on_5xx_backoff_sec=2`)."

### MINOR (fix in synth files)
- **S2 — wrong line cite for sanctioned tmux subprocess (from 5.17).** synth-08 §19.5/§19.6 NFR-7 OI-2 amendment cites the legit `subprocess.run` line imprecisely. FIX: the fix agent must VERIFY the actual location of the sanctioned `--tmux subprocess.run` (it is OUTSIDE the reflect no-nest scope — confirm whether it's in `swarm/tmux.py`/`swarm/commands.py` or `reflect/commands.py`) and correct the citation. The substantive claim (raw-subprocess ban stays scoped to runner.py+ensemble.py so the legit tmux call elsewhere is unaffected) is correct; only the line ref needs fixing.
- **S3 — D3 emphasis divergence (from 5.17).** synth-06 D3 Option A flags the FR-RH2.7 `derive_verdict`-out-of-scope tension; synth-09 Q6 option (ii) glosses it. FIX: align synth-09 Q6 to note the FR-RH2.7 tension consistently.

### ASSEMBLY DIRECTIVE (no synth-file edit; for rf-assembler in Phase 6)
- **S4 — internal "(Dn)" directive-label collision (from 5.12, 5.10-A1).** The synth files carry internal scaffolding labels ("(D1)".."(D7)" and per-file "Decision Dn") that collide across files (synth-08 D3=`max_fix_iterations` cap vs synth-09 D3=`ensemble-empty`; synth-09 banner mislabels the recipe directive). These are orchestration artifacts NOT present in spec.md. **ASSEMBLER MUST neutralize/strip the bare "(Dn)" research-gate-directive citations when assembling the final TDD** (keep the substantive content; remove the ambiguous label tokens) so the published TDD reads cleanly. The §6.4 Key Design Decisions table may keep its own self-contained Decision rows.
- **S5 — §6 numbering (from 5.10-A1).** synth-03 uses §6.6/§6.7; template §6 ends at §6.5 (Multi-Tenancy, correctly skipped). ASSEMBLER should renumber the reuse-audit subsection to avoid implying a missing §6.5 (e.g. fold under §6.4 or label "§6.5 Reuse & Consolidation Audit" replacing the skipped multi-tenancy slot).

### MINOR cosmetic (no fix required; report-validation/fidelity gates will catch anything material)
- Off-by-one citation nits: synth-03 `bare_review.py:66`→:67; dataclass `@dataclass`-line vs `class`-line ±1 in several models.py cites; synth-04 "19 top-level keys" aggregate count unverified; synth-08 ModelPoolTooSmallError L589-609 (class) vs L687-688 (raise). All named symbols exist at cited loci; immaterial.

## Fix plan (Step 5.19)
Spawn ONE rf-qa (fix_authorization: true) to fix S1 (synth-06 §12.4 backoff), S2 (synth-08 tmux line cite — verify actual location first), S3 (synth-09 Q6 alignment) in-place. Record S4 + S5 as binding ASSEMBLY directives in `phase-outputs/plans/synthesis-gate-verdict.md` for the rf-assembler. Cosmetic nits left as-is. Then Step 5.20 verify (max 2 cycles).
