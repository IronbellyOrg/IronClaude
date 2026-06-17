# QA Report — crossref-chain content lens (POST-COMPLETION)

**Topic:** forensic→troubleshoot TFEP backend migration — end-to-end cross-file chain
**Date:** 2026-06-16
**Phase:** doc-qualitative (crossref-chain content lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Stance:** Adversarial — assumed ≥5 errors, focused on crossref-chain.

---

## Overall Verdict: FAIL

One CRITICAL dangling cross-reference on the consumer side of the wire contract, plus one MINOR
back-reference imprecision. The structural chain (tokens, paths, caller name) is otherwise intact.

---

## Chain Traced (link-by-link)

| # | Link | Result | Evidence |
|---|------|--------|----------|
| 1 | task-protocol TFEP §4.5 Step 3 dispatches `/sc:troubleshoot --caller task-unified` | PASS | task-protocol:215 emits `/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}`; no `--fix` (correct). |
| 2 | troubleshoot Wave 0 step 6 ingests `--caller`/`--context` + marks Wave 5 emit | PASS | troubleshoot:148 — "If `--caller` is set, record it… If `--context <path>` is set, read it… When `caller=task-unified`, mark Wave 5 to emit `return-contract.yaml`". `--context`/`--caller` parsed at :120; STOP-on-unreadable at :152. |
| 3 | troubleshoot Wave 5 step 4.5 emits `return-contract.yaml` with the 7 fields | PASS | troubleshoot:471 — writes `<output-dir>/return-contract.yaml` with `status`, `test_is_wrong`, `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`. Exactly 7. |
| 4 | §4.5 Step 4 consumer reads those exact fields | PARTIAL → see C-1 | task-protocol:219 reads the 7 fields by name; but the branch ladder at :225 also gates on `behavior_is_documented`, which is NOT in the 7-field wire set. |
| 5 | §4.5 Step 5 composes plan from `remediation_target`/`root_cause_summary`/`solution_summary` | PASS | task-protocol:236 composes the `## Failure Remediation Plan (Adjudicated)` body from exactly those 3 fields; all 3 are producer-emitted (:471). |
| 6 | report-template `## TFEP Consumer` block echoes the same 7 fields | PASS | report-template:160-167 yaml block lists exactly the 7 producer fields, byte-for-byte matching the Output Contract / Wave 5 step 4.5 wire set. |

**Token identity checks:**

- `--caller task-unified` — byte-identical on producer (troubleshoot:148, command:60) and consumer (task-protocol:215,239,268,269). PASS.
- `return-contract.yaml` path token — consumer reads `{output_dir}/return-contract.yaml` (:219); producer writes `<output-dir>/return-contract.yaml` (:471). Same `{output_dir}` base passed via `--output-dir {output_dir}` (:215). PASS.
- `{context_path}` — consumer writes `{output_dir}/context.yaml` and passes it as `--context {context_path}` (:205,215); producer ingests `--context <path>` (:148). PASS.
- `--depth {depth}` standard/deep mapping — consistent producer↔consumer (:215 vs :120). PASS.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| C-1 | CRITICAL | sc-task-protocol/SKILL.md:222, :225 | **Dangling consumer field — `behavior_is_documented` is read but never produced on the wire.** The Step 4 consumer branch ladder declares the asymmetric-cost gates as `(test_is_wrong, behavior_is_documented)` (:222) and branches on `behavior_is_documented == true` (:225) as a primary, first-match-wins gate. But the producer's `return-contract.yaml` (troubleshoot Wave 5 step 4.5, :471) emits a **7-field** wire set that does NOT include `behavior_is_documented`, and the report-template `## TFEP Consumer` echo block (:160-167) does NOT include it either. The consumer is reading a field that does not exist in the contract it was handed → the `behavior_is_documented == true` branch can never fire from wire data, so the "present to user for spec/stakeholder review; do NOT auto-insert a code remediation" safety gate is dead. The asymmetric-cost case (documented-behavior bug) would silently fall through to `status == "success"` → auto-insert + resume (Step 5), i.e. it would auto-remediate a documented-contract "bug" — the exact failure the flag exists to prevent. | Reconcile producer↔consumer. Either (a) add `behavior_is_documented` as an 8th field to the Wave 5 step 4.5 wire set (troubleshoot:471) AND the report-template echo block (:160-167); or (b) rewrite the consumer gate to key only on the emitted proxy `remediation_target == "docs"` and drop the bare `behavior_is_documented == true` test at :225 (the `(or remediation_target == "docs")` clause already present at :225 is the producer-backed half — make it the sole condition, and remove `behavior_is_documented` from the :222 gate description). Option (b) is the smaller, wire-faithful change. |
| C-2 | MINOR | sc-troubleshoot-protocol/refs/report-template.md:158 | Back-reference imprecision. The TFEP Consumer block cites "`sc:troubleshoot-protocol` Wave 5 **step 4.5**". The anchor exists (troubleshoot:471 is literally numbered `4.5.`), so this resolves — but the same sentence also says "and the Output Contract adapter rows," and the adapter rows in the Output Contract table use the canonical field names. No defect in resolution; flagging only that the prose leans on a bare "step 4.5" ordinal that is fragile to renumbering. Non-blocking. | Optional: change "Wave 5 step 4.5" to "Wave 5 — Emit TFEP return-contract" (anchor by heading text, not ordinal). |

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` section was present in the spawn prompt. Ran standalone (independent structural + content verification) per fallback behavior — relied on no inherited PASS items.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Wire-set cardinality + membership: grepped the 7 field names across producer (troubleshoot:471), consumer (task-protocol:219,224-236), and echo block (report-template:160-167); discovered `behavior_is_documented` present on the consumer branch ladder but absent from both producer wire set and echo block — tool evidence: Bash grep for `behavior_is_documented` returning task-protocol:222,225 with zero hits in the report-template yaml block and zero in the troubleshoot 7-field list at :471.
- Path-token resolution: traced `{output_dir}`/`{context_path}`/`return-contract.yaml` substitution chain across both files via grep; confirmed `--output-dir {output_dir}` (consumer :215) and `<output-dir>/return-contract.yaml` (producer :471) share a base. Not a structural section-number check — a semantic substitution-resolution check.
- Step-5 composition vs producer default: verified `tasklist_insertion_path` defaults to `null` (producer :471) and the consumer composes the plan body from the 3 content fields (`remediation_target`/`root_cause_summary`/`solution_summary`, :236) rather than from the null path — coherent, not a contradiction. Read of task-protocol:232-239.

---

## Confidence

Verified: 6/6 chain links + 4/4 token-identity checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 6 | Grep: 6 | Glob: 0 | Bash: 6

Every chain link and token-identity claim was grep-verified against the actual file content with cited line numbers. No sampling.

---

## Recommendations

1. **Resolve C-1 before this migration is considered complete.** It is the single load-bearing defect on the chain — the documented-behavior asymmetric-cost gate is non-functional as wired. Prefer option (b) (key the consumer on `remediation_target == "docs"`, drop the bare `behavior_is_documented` test) — it keeps the wire set at 7 and is the smallest safe change.
2. C-2 is cosmetic; fix opportunistically.

## QA Complete
