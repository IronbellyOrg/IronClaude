# Reviewer Card — REFACTORER (structural integrity lens)

**Run:** pre-fr-rh1-uc2-reachability-20260620-053500
**Tier:** 2 (forced by --depth deep)
**Persona:** refactorer / structural integrity
**Mode:** UC-1 pre-execution coverage/gap audit
**Spec:** `.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md` (patched FR-RH1 R1-R9)
**Tasklist:** `.dev/tasks/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/TASK-RF-uc2-reachability-gate-20260620-043410.md`

## Verification performed (evidence-grounded, not asserted)

- Confirmed `src/superclaude/cli/reflect/` contains `models.py`, `config.py`, `commands.py`, `runner.py`, `contract.py` — all five wrapper surfaces the tasklist targets exist.
- Confirmed the `--promote/--no-promote` pattern is the live structural precedent: `models.py:76 promote: bool`, `commands.py:90 "--promote/--no-promote"`, `config.py:132/231 promote`, `commands.py:279 _build_inner_command` + `:299` tmux forward, `runner.py:341 _build_prompt` + `:346-347` conditional append. The tasklist's R5 plumbing mirrors this exactly.
- Confirmed `SKILL.md:660/663` is currently `contract_version: "1.5.0"` D13-only (`coverage_pct_union`, `coverage_degraded`, `unmapped_requirements_union`). R4's bump-to-1.6.0 target is real and correctly located.
- Confirmed **no `runtime_surface_*` strings exist** anywhere under `src/superclaude/skills/sc-reflect-protocol/` — the FR-RSR-leakage starting point is clean (so the non-goal is about not re-introducing it, which the tasklist handles).
- Confirmed the **stale merged-requirements.md DOES contain every unsafe clause** R1-R9 supersedes: `binding unambiguously absent AND oracle_mismatch ⇒ unreachable/Regression` (×3, lines 92/131/235), `--no-reachability` "records the skip in Grounding Gaps" (×2, lines 138/191), "spec absent" → Grounding Gap (line 236), `reachability_gate_added_tokens/turns: 0` (lines 257-258), `contract_version: "1.5.0"` (lines 270/274/309). This makes Phase 2 patch-first load-bearing and correctly targeted.
- Confirmed all 7 Phase-2 search strings (item 144) hit the merged artifact; the `runtime_surface_` search returns 0 (correct negative).
- Confirmed item 154 preserves R7's "UC-1 may omit the reachability block."
- Confirmed frontmatter `reflect_pre.notes` (line 30) explicitly disclaims spec-run carry-forward: "a separate UC-1 audit of the tasklist, not a carry-forward of the spec's own original run."

## Per-obligation coverage table

| Obl | Requirement | Implement item(s) | Verify item(s) | Coverage | Notes |
|---|---|---|---|---|---|
| R1 | Regression real-boot-only; static signals → `unproven` max | 152, 156, 158 (SKILL/taxonomy mapping) | 196 (proxy/oracle cannot satisfy real-boot proof), 222/224 adversarial QA | COVERED | Mapping mirrored across SKILL + deviation-taxonomy ref → no single-file drift. Strong. |
| R2 | `--no-reachability` telemetry-only; no gap/HD/partial | 152, 160, 164, 174, 184 | 194, 196, 202, 226 | COVERED | Skip invariant (null ledger, zero counters) propagated to fixtures (194) + tests (196). |
| R3 | spec-and-tasklist-absent telemetry-only | 152, 160 | 194, 196 | COVERED | Distinct skip_reason token threaded through fixture + test items. |
| R4 | contract 1.6.0; 1.5.0 stays D13-only | 154, 160, 164(header), 192 | 220 (QA), 196 | **PARTIAL** | Bump + preservation asserted everywhere; **additive-minor diff is never mechanically verified** — see GAP-1. |
| R5 | wrapper plumbing (5 sub-parts) | 174 (cmd.md), 176 (models config field), 178 (config.py), 180 (Click+tmux), 182 (_build_prompt exactly-once), 184 (docs) | 198 (help/prompt/tmux tests + docs parity), 226 | COVERED | All five sub-parts present and each isolated to one file/surface. tmux forwarding (180) + exactly-once (182, 198) both explicit. Best-decomposed phase. |
| R6 | producer eval fixture distinct from consumer | 200 (active eval cases in `.dev/eval-workspaces/sc-reflect/`), 204 (run producer eval) | 206, 222 (producer/consumer falsifiability) | COVERED | Item 200 explicitly "producer fixture that exercises Step 5.6 output rather than only a consumer contract fixture"; 192 base fixture kept separate. |
| R7 | exact 7 `reachability_*` fields + consistency invariants | 154 (fields+rules), 160(report), 192(fixture) | 196, 220 | COVERED w/ caveat | All 7 fields enumerated verbatim. UC-1-omit preserved (154). Consistency invariants present but see GAP-2 (arithmetic invariant `verification_regressions_detected >= reachability_unreachable` not explicitly carried into any verify item). |
| R8 | bounded cost, not zero | 164 (cost-profile.yaml: tool_classes 0, turns 1-3, cap 12/36, boot cap 1) | 220, 224 | COVERED | Explicit "no zero-token or zero-turn claim remains." Numeric bands match spec R8 exactly. |
| R9 | advisory-only semantic fallback; explicit durable_sink/@sink only blocking trigger | 152, 156, 158, 174 | 196 (semantic fallback not DEGRADED/HALTED by itself), 224 | COVERED | Blocking-eligibility gated on explicit annotation across SKILL+taxonomy+cmd; advisory non-gating asserted in test 196. |

**Coverage_pct: 0.92** (9/9 obligations mapped to implement+verify; R4 and R7 each carry one un-verified sub-invariant that is asserted but not mechanically checked — counted as partials.)

## best_practice_grade: 4 / 5

Strengths: patch-stale-artifact-before-implement (Phase 2) is correctly sequenced and the search strings provably hit the stale clauses; one-file-per-item decomposition; deviation mapping mirrored across SKILL + taxonomy + report so no surface can silently re-open a gap; producer/consumer fixtures explicitly distinguished; reflect_pre frontmatter explicitly disclaims spec-run conflation; no FR-RSR `runtime_surface_*` leakage in the current tree and a dedicated no-leakage QA lens (228). Deduction is for the two un-mechanized invariants below — a structural-integrity reviewer wants the additive-minor and arithmetic-consistency claims *tested*, not only *asserted* and *adversarially eyeballed*.

## Gaps / risks (severity-ranked)

- **GAP-1 (MEDIUM) — additive-minor invariant is asserted, never mechanically verified.** The tasklist repeats "fields are additive under 1.6.0; 1.5.0 remains D13-only" (lines 74, 111, 154, 220) and item 220 spawns a report-only adversarial QA on "D13-only 1.5.0 preservation." But **no item performs a field-level diff** proving no existing 1.5.0 field (`coverage_pct`, `unmapped_requirements`, `coverage_pct_union`, `coverage_degraded`, `unmapped_requirements_union`, etc.) was renamed/removed/retyped during the 1.6.0 edit. A minor bump that silently retypes or drops a pre-existing field would pass every current item (the consumer fixture 192/196 only proves the *new* fields are *tolerated*; it does not pin the *old* field set). Recommend an explicit verify item: assert the 1.6.0 stable-field set is a strict superset of the 1.5.0 set with unchanged types (e.g. a `regex_present` per pre-existing field, or a diff check in test_verdict_mapping). Self-contained, low cost.
- **GAP-2 (LOW-MEDIUM) — R7 arithmetic consistency invariant not carried into a verify item.** Spec R7 requires `if reachability_unreachable > 0: verification_regressions_detected >= reachability_unreachable` and `reachability_real_boot_ran: true`. Item 154 says "consistency rules for ... unreachable" (implement side) and 196 asserts proxy/oracle cannot satisfy real-boot proof, but no test/fixture pins the *arithmetic* relation between `reachability_unreachable` and `verification_regressions_detected`. Since the real-boot-proven Regression fixture is explicitly optional ("if implementable in the harness", item 200), this invariant may ship with zero executable coverage. Recommend adding it to the consumer-test assertions (196) even if driven by a hand-authored fixture, so the counter-coupling is falsifiable without a live boot.
- **RISK-1 (LOW) — Phase 2 "amendment-instead-of-patch" branch can leave two sources of truth.** Item 142 permits creating `FR-RH1-v1-amendment.md` "if direct patching is intentionally avoided." If that branch is taken, the stale clauses *remain* in merged-requirements.md and a later reader/automation could still pick them up. Item 144's verdict requires remaining occurrences be "justified as negative/backcompat prose," which mitigates but does not eliminate the dual-source hazard. Acceptable given the explicit verdict gate, but flag: prefer in-place patch over companion amendment for this artifact.
- **RISK-2 (LOW) — semantic-fallback advisory telemetry has implement coverage but thin negative-test coverage.** R9's "advisory candidate MUST NOT set reachability_unproven / write a gap / affect status" is asserted in 152/156/174 and tested at 196 ("semantic fallback does not route to DEGRADED/HALTED by itself"). But there is no fixture asserting an advisory candidate leaves `reachability_unproven == 0` while still being *recorded* as advisory telemetry — i.e. the test proves it doesn't gate, not that the advisory signal is actually emitted. Minor; the producer eval (200) could absorb this. Not blocking.

## Conflation / leakage checks (lens-specific)

- Stale-artifact-before-implementation: **PASS** — Phase 2 patches/amends merged-requirements.md before any `src/` edit, and Phase 3+ consume the Phase-1 requirements-map + Phase-2 verdict, not the raw stale text. Sequencing verified against the Cross-Stage Integration Requirements section.
- reflect_pre frontmatter conflation: **PASS** — line 30 explicitly separates this tasklist-audit gate from the spec's own original reflect run.
- FR-RSR `runtime_surface_*` semantics leakage: **PASS** — none in current tree; non-goal stated in Prerequisites (line 90) + Source Areas + dedicated QA lens (228). The `promote` plumbing (not `runtime_surface`) is the cited structural precedent, which is correct.
- R7 UC-1-omit preservation: **PASS** — item 154 carries "UC-1 may omit the reachability block"; no item forces reachability fields into UC-1 contracts.

## Verdict

Structurally sound, well-decomposed, and correctly sequenced (patch-first). No fatal hole. The single recurring structural weakness is that the **additive-minor (GAP-1)** and **arithmetic-consistency (GAP-2)** invariants are asserted in prose and left to adversarial QA judgment rather than pinned by a mechanical/test assertion — exactly the class of regression a refactorer expects to be enforced, not eyeballed. Both are MEDIUM/LOW and fixable with self-contained verify items; neither blocks proceed. Recommend proceed with the two added verification items.

SELF_CONFIDENCE: 0.86
