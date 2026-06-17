# QA Report — Research Depth Review

**Phase:** research-depth (qualitative)
**Date:** 2026-06-16
**Lens:** Is the research DEEP enough to produce a high-quality, per-deliverable tasklist WITHOUT re-reading source?
**Track Goal:** Corrective MDTM tasklist for sc-bare-review M8/M9 migration.
**Adversarial stance:** Assume research is superficial until proven otherwise.

**Assigned files:**
- 01-skill-and-scripts-inventory.md
- 02-swarm-cli-thin-caller-surface.md
- 03-parity-test-and-swarm-test-conventions.md
- 04-docs-and-release-notes-staleness.md
- 05-mdtm-template-and-sync-discipline.md

---

## Overall Verdict: PASS

The research is DEEP enough to produce a high-quality, per-deliverable corrective tasklist
without re-reading source. All five files go well beyond "list file names": they trace
behavior, carry precise `file:line` anchors, and supply executable plans. Every load-bearing
claim I spot-checked against actual source matched. This is the opposite of the shallow
"name-dropping" research the adversarial stance assumes by default.

---

## Independent Source Verification (adversarial — assume claims are wrong until checked)

| Claim (research) | Verified against source | Result |
|---|---|---|
| SKILL.md = 231 lines (R1/R4/R5) | `wc -l SKILL.md` → 231 | ✓ MATCH |
| 3 scripts still present (R1/R4/R5) | `ls scripts/` → t2_dispatch.sh, t2_normalize.py, t2_preflight.sh | ✓ MATCH |
| script line counts 219/112/316 (R1) | `wc -l` → 219/112/316 | ✓ MATCH |
| recipe + lens exist (R1/R2) | both files present | ✓ MATCH |
| parity test ~794-795 lines (R1/R3) | `wc -l` → 794 | ✓ MATCH (R3 said 795, off-by-1, immaterial) |
| **R2 B-5: inline `run_cmd` is dispatch-only** | `dispatch_wave1` inline @1554; `normalize_wave2`/`reduce_wave3` ONLY in resume branch (1781/1788/1952/1977); stub line "dispatched job" @1574; `emit_contract` never called from commands.py | ✓ MATCH — headline confirmed |
| **R2 B-1..B-4: 4 flags have no CLI option** | negative grep for `--label/--timeout-sec/--reviewers/--workers/--target-line-cap` → EMPTY | ✓ MATCH |
| R2 lens defaults 3 / 4000 | bare_review.py:61-62 `default_workers=3`, `default_target_line_cap=4000` | ✓ MATCH |
| R2 spec anchors: workers_count / invocation_label / timeout_sec:180 / line_cap | all present in `_build_spec_from_lens` body | ✓ MATCH |
| R2 dispatch.py `prompt: str = ""` @339, `worker_spec` @341 | confirmed | ✓ MATCH |
| R2 preflight 527-528 override `<=0 or ==4000` | confirmed verbatim (incl. the "4000 is replaced" nuance) | ✓ MATCH |
| R3 skipif guard `not LEGACY_SCRIPT.exists()` @217-218 | confirmed | ✓ MATCH |
| R3 CliRunner pattern `_run`@68-70 + stub invocation @86-89 | confirmed | ✓ MATCH |
| R4 false claim release-notes-v1.md:16 "is now a ~60-line thin caller" | confirmed present-tense @16 | ✓ MATCH |
| R5 template 02 exists (src + mirror) | both present | ✓ MATCH |
| R5 hooks AC11 @104 + MIG-001 @119 + both scripts | confirmed | ✓ MATCH |
| R5 B2 6-element completion-gate verbatim @165; I18 @688; M3 gate | confirmed | ✓ MATCH |
| R5 phase-9 OPS-001/005 paths (operator-runbook / lens-contribution-policy) | confirmed @20/187 | ✓ MATCH |
| R4 docs/swarm/ has NO operator-runbook.md (naming collision w/ runbook.md) | `ls docs/swarm/` → runbook.md present, operator-runbook.md absent | ✓ MATCH |
| R4 lens-contribution-policy.md = 515 lines at docs/dev/ | `wc -l` → 515 | ✓ MATCH |

**Zero contradictions found across 20 independent checks.** The one micro-discrepancy
(R3 "795" vs actual 794 lines) is a trailing-newline off-by-one with no bearing on the plan.

---

## Depth Checklist (the 6 lens questions)

**Q1 — Does R2 explain HOW the inline `run_cmd` path differs from `--resume` (enough to scope the wiring fix)? → YES (exemplary).**
R2 §4 traces the inline path step-by-step (12 numbered steps, commands.py:1304-1578), names
exactly what IS emitted (manifest.json, execution-log.{jsonl,md}, .swarm-state.json) vs what is
NOT (return-contract.yaml, merged.md, normalized `.final.md`), proves it with a grep matrix
(`dispatch_wave1` inline @1554 vs `normalize_wave2`/`reduce_wave3` resume-only), AND contrasts
the fully-wired resume path (1930→1952→1977) as the working reference. B-5 even names the exact
fix: pass `prompt`+`worker_spec` to `dispatch_wave1`, then call normalize/reduce/emit_contract.
A builder can scope the wiring fix line-for-line. **Verified independently — accurate.**

**Q2 — Does R3 give a concrete, executable golden-baseline design? → YES.**
R3 §4 is a complete design: (1) capture frozen legacy golden BEFORE WS-C deletion using the
existing `_run_legacy` machinery (test_bare_review_parity.py:268-374); (2) exact golden tree
layout (`tests/swarm/fixtures/bare_review_v1/golden/<scenario>/bare-review-NN-<slug>.md` +
`return-contract.yaml`); (3) reuse `.raw.txt` corpus as StubTransport input; (4) the CLI driver
verbatim (`runner.invoke(swarm_group, ["run","--lens","bare-review","--target",…,"--output",…,"--transport","stub"])`);
(5) determinism pins (FIXED_GENERATED injection, two options); (6) regen procedure (env-gated,
human-approved); (7) the 5 invariants the permanent gate asserts. **Crucially, R3 flags its own
hard blocker** (§3.3): the golden gate is dependent on R2/M5 landing normalize+reduce on the
fresh path — honest gap-acknowledgment, not over-claiming.

**Q3 — Does R1 give a concrete keep/drop line budget for the ~60-line rewrite? → YES.**
R1 §1.11 is a quantified per-region KEEP/DROP table (frontmatter 1-6 KEEP; Behavioral Protocol
72-133 ~62 lines DROP → one `swarm run` block; Return Contract 135-160 KEEP verbatim; etc.) with
the net statement that the ~62-line Wave A-E protocol is THE deletion target. It identifies the
single line that is the migration headline (L35-37 "three bundled scripts" → "swarm CLI lens").
A builder can write the rewrite from this budget alone.

**Q4 — Does R4 give per-OPS-doc target paths + the exact false-claim line + the don't-rename caution? → YES.**
R4 §4 has the full per-OPS table (target path / NET-NEW|EXTEND|RELOCATE / rationale) for all 6
OPS docs. The exact false-claim line is pinned: `release-notes-v1.md:16` with the verbatim quote
and both falsification proofs (231 lines; scripts present). The don't-rename caution is explicit
twice: "do NOT rename `runbook.md`" and "do NOT rename" `monitoring-patterns.md` (both linked from
README map). OPS-005 RELOCATE-vs-cross-ref decision hinge (inbound links) is spelled out.

**Q5 — Does R5 give the specific MDTM rules + the exact sync commands a STRICT item runs? → YES.**
R5 §1 enumerates the binding rules by ID with line refs: A3 (108-112), A4 (114-133), B2 6-elements
(159-165), B5 forbidden patterns, D3 ordering (286-289), E1-E4, F1/F2, I8/I12/I18 (688-697),
L1-L7 (esp. L3 test, L5 conditional-action for gated deletion), M3 lens-QA gate. The exact sync
commands are given: `make sync-dev && make verify-sync` as the [COMPLETION] step for any
sc-bare-review src edit, with BOTH pre-commit hooks (AC11 + MIG-001) traced. R5 §4 adds the STRICT
gate caveat (gate on `uv run pytest tests/swarm/` + `make verify-sync` + path-scoped ruff; NOT
`make lint`, which exits 2 independently).

**Q6 — Could a builder create per-file checklist items from this research alone? → YES.**
Each deliverable has: target path, classification, exact source anchors, the specific fix,
sequencing dependencies (L5 gate: delete scripts only IF parity passes, mirroring T08.07-after-
T08.11), and the validation that catches the prior failure mode (verify outputs exist ON DISK,
not merely "step performed"). R5 §3.2 even diagnoses WHY the prior phase-8 tasklist failed
(tasks marked done without the deliverable existing) and prescribes the I17 on-disk validation
counter-measure. This is builder-ready.

---

## Cross-File Coherence (partition note)

All 5 assigned files were in my partition, so I performed full cross-file coherence:
- **R1↔R2:** R1 says "R2 owns target flag names"; R2 delivers the full flag-mapping table and
  the B-5 wiring gap. Consistent, no double-ownership.
- **R1↔R3:** R1 points at parity test `test_bare_review_parity.py`; R3 owns it and confirms it is
  library-vs-library + self-skips on deletion. Consistent.
- **R2↔R3:** R3 explicitly flags its golden gate as BLOCKED on R2/M5 (normalize/reduce on fresh
  path). R2's B-5 is exactly that blocker. **The two files agree on the same gap from both sides**
  — strong coherence, not contradiction.
- **R1↔R4:** R4 cites 231-line SKILL.md as cross-validation and correctly defers authoritative
  SKILL.md sizing to R1 ("R1 owns SKILL.md/scripts"). No turf conflict.
- **R4↔R5:** R4's OPS-004 HALT-for-sign-off and R5's I-rule HALT discipline align with the
  `human_decision_items_must_halt` memory. Consistent.

No contradictions across files. The dependency graph (R3 depends on R2/M5; deletion depends on
parity) is consistently represented in every file that touches it.

---

## Minor observations (NOT blocking — research is PASS)

These are quality notes for the builder, not depth failures. None rise to CRITICAL/IMPORTANT
because each is already flagged by the research itself or is immaterial to the plan:

- **M-1 (MINOR, self-flagged by R1/R2):** R1 §3.1 flags an open parity risk — whether the swarm
  lens carries identical prompt text or reads `refs/prompts.md` (orphan-vs-duplicate). R2 §2 shows
  the lens DOES carry its own `system_prompt_fragment` + `user_template` (bare_review.py:47-57),
  which means `refs/prompts.md` becomes orphaned post-deletion and prompt-text parity is NOT
  currently gated by any test. The research surfaces this but neither file fully closes it — the
  builder should add a prompt-text parity check item. (Depth is sufficient: the risk is named with
  anchors; this is a plan-input, not a missing fact.)
- **M-2 (MINOR):** R3's golden-gate design has a real, honestly-disclosed hard dependency on
  R2/B-5 landing first. The builder must sequence R3's permanent gate AFTER B-5, or the gate has
  nothing to assert on. The research states this; just ensure the tasklist encodes the ordering.
- **M-3 (MINOR, informational):** e2e:187 shows `workers=4` runs are reachable via spec-file mode,
  confirming R2's "escape hatch is spec-file mode" point — the lens itself isn't pinned at 3, only
  the CLI surface lacks a `--reviewers` flag. R2 states this correctly; no correction needed.

---

## Self-Audit

**(a) Reliance list — items where structural correctness was assumed (none inherited; standalone run):**
- This was a standalone research-depth review with no Inherited Structural Verdict in the spawn
  prompt. I relied on NOTHING from a prior rf-qa pass — all structural and semantic checks were
  performed first-hand.

**(b) Independent semantic checks (≥1 required, INV-019):**
- **Pipeline-gap claim (R2 B-5):** independently grep-verified `dispatch_wave1` inline @1554 vs
  `normalize_wave2`/`reduce_wave3` resume-only, and that `emit_contract` is never called from
  commands.py. Tool evidence: Bash grep over commands.py.
- **Flag-gap claim (R2 B-1..B-4):** independently ran the negative grep for the 5 missing flags →
  empty result, confirming the gap. Tool evidence: Bash grep over commands.py.
- **Preflight 4000-override nuance (R2 B-2):** independently read preflight.py:525-530 to confirm
  the `<=0 or ==4000` replacement semantics R2 claims. Tool evidence: Bash sed.
- **False-claim line (R4):** independently grep'd release-notes-v1.md:16 to confirm the
  present-tense "is now a ~60-line thin caller" against actual SKILL.md=231. Tool evidence: Bash.
- **MDTM template binding rules (R5):** independently grep'd the template for B2 6-element
  completion gate verbatim @165, I18 @688, M3 gate. Tool evidence: Bash grep.

**Self-audit answers:**
1. Independently verified ~20 factual claims against source (see verification table).
2. Files read/grepped: SKILL.md, scripts/, recipe, lens, commands.py, dispatch.py, preflight.py,
   bare_review.py, test_bare_review_parity.py, test_e2e_user_guide.py, release-notes-v1.md,
   02_mdtm_template_complex_task.md, .pre-commit-config.yaml, phase-9-tasklist.md, docs/swarm/,
   docs/dev/lens-contribution-policy.md.
3. Why trust a PASS with no blocking issues: 20 independent source checks, zero contradictions,
   and every depth question answered with cited evidence. The research's own self-flagged risks
   (M-1, M-2) prove it is honest about gaps rather than over-claiming — a strong positive signal.
4. No web research was required (all checks were local-file-bound); Tavily not invoked.

---

## Confidence

**Verified:** 6/6 depth-checklist items + 20/20 source claims | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence: 100%**

**Tool engagement:** Read: 6 | Grep: 0 (via Bash) | Glob: 0 | Bash: 6 (grep/wc/ls/sed)

---

## Summary
- Depth-checklist items passed: 6 / 6
- Source claims verified: 20 / 20 (zero contradictions)
- Critical issues: 0
- Important issues: 0
- Minor observations: 3 (all self-flagged by research or informational; none block)
- Issues fixed in-place: 0 (fix_authorization: false)

## VERDICT: PASS

The research is deep, accurate, and builder-ready. A task-builder can produce per-deliverable
MDTM checklist items for the SKILL.md rewrite (R1 budget), the B-1..B-5 swarm CLI wiring fix
(R2 anchors), the frozen-golden parity gate (R3 design), the 6 OPS docs + release-notes
reconciliation (R4 classification), and the MDTM/sync discipline (R5 rules) WITHOUT re-reading
source. The three minor observations are plan-inputs the builder should fold in (notably M-1
prompt-text parity and M-2 R3→B-5 sequencing), not depth deficiencies.

---
