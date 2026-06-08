# Variant 3 — haiku:qa — Phase 9 Unchecked-Item Review

**Stance:** Testability, completion-criteria concreteness, fail-isolation, regression risk, "can a worker actually finish this and prove it?" Edge cases.

**Checkbox reality:** Unchecked = 9.11, 9.12, PG9.1, PG9.2 (9.7–9.10 already `[x]`). QA reviews those four.

---

## Step 9.11 — secondary migrations

**Testability:** Each sub-migration has a concrete, runnable parity test target (`test_tool_write_step_<name>.py`) and a single `tee`'d command. The completion command is given verbatim. GOOD — a worker can run it and produce evidence.

**Edge case — fail-isolation (H4):** H4 says "FAIL on sub-action (b) certify does NOT block (a)/(c)." The item body says "log the blocker per-step … then mark this item complete." That *allows* partial completion, which is the right behavior, BUT the body is a single checklist item — if certify's tool-write fails, the worker marks the WHOLE item complete with a logged blocker, losing the per-sub-action green/deferred granularity H4 wants. The test surface needs **per-sub-action pass/defer tracking**, not one item-level checkbox. REFACTOR to a/b/c/d/e so each has its own completion proof. (Concurs with architect + analyzer.)

**Regression risk:** Migrating certify must not break the R1.3 CodeAssertion path or `test_certify_prompts.py` / `test_certify_gates.py`. The "Ensuring" clause names this ("test_certify_prompts.py / test_validate_*.py / test_remediate_prompts.py unchanged"). Good guard. Validate-reflect must keep `test_validate_*.py` green. The byte-identical-default-path test (proven for prior steps) is the regression sentinel — the item should require it per sub-action.

**The remediate trap (QA angle):** A parity test for tool-write remediation would compare "rendered markdown from tool JSON" vs "current markdown prompt." But `build_remediation_prompt` outputs an **instruction-to-edit-a-file**, not a renderable artifact — there is no markdown *artifact* to diff, only a prompt string. So a "parity test" for remediate is ill-defined: what are you comparing? This is concrete evidence the remediate migration doesn't fit the established parity-test mold. REFACTOR: if remediate is migrated at all, the parity test compares prompt-string equivalence under flag=False (byte-identical), and there is NO roadmap_ids / Contract #3 assertion (nothing to assert). Better: defer remediate or mark it parity-only.

**Verdict: REFACTOR** — split into a/b/c/d/e with per-sub-action proof; remediate parity is prompt-string-only with no Contract #3 obligation.

---

## Step 9.12 — cutover criterion

**Completion-criteria concreteness — FAILS the QA bar.** The item's own completion depends on "≥3 release cycles" that have not happened and will not happen before this task closes. "Mark this item complete" while the substantive criterion (3 green release cycles) is unmet means the checkbox lies about reality. A QA gate cannot certify "done" when the acceptance condition is structurally in the future. REFACTOR: redefine "done" as "initial cutover-decision doc written, all 13 yaml entries at 0 cycles / not-eligible, R1.4 readiness = NOT READY, markdown remains default" — a state that IS verifiable now. Defer the actual cutover to R1.6.

**Testability of the readiness verdict:** "ALL 12 steps ready OR documented exception" — testable IF the source is the yaml (iterate entries, assert eligible). Currently the source is ambiguous prose. Pin to yaml. Also: yaml has 13 entries (incl. remediation) + the item says "12 sub-step validation summaries" + glob is `r1-4-*-validation.txt`. The COUNTS don't line up (12 vs 13 vs 11-genuine). A worker globbing `r1-4-*-validation.txt` today finds 9 files (extract, extract_tdd, generate, diff, debate, score, merge, spec-fidelity, wiring) — the 4 secondary validation txts don't exist yet (9.11 not run). So 9.12 as written would read an incomplete set. REFACTOR: 9.12 must run AFTER 9.11 produces the secondary validation txts, and the readiness verdict must reconcile to 11 genuine + wiring-exempt.

**Verdict: REFACTOR** — completion criterion must be a now-verifiable initial-state doc; source the yaml; reconcile the 11/12/13 counts; sequence after 9.11.

---

## Step PG9.1 — aggregate + rf-qa-qualitative

**Testability of the gate:** The aggregation glob + spawn is concrete. The adversarial-stance checks (a)–(h) are each verifiable against artifacts. GOOD.

**The false-FAIL edge case (QA's core concern):** Check (a) "12 sub-steps all have schema + template + dual-write + parity test." QA simulation: an rf-qa agent globs `templates/tool_schemas/` and finds 8 (soon 11) schemas, NOT 12 — wiring has none (by design, 9.10), and remediate's "schema" has no roadmap_ids (and may be a prompt-only parity). Strict check (a) → **FAIL on a correct, by-design state.** This is a textbook false-positive gate. The 9.10 finding mitigated it by writing `r1-4-wiring-validation.txt` with the exemption rationale so the glob+aggregation surfaces it — but check (a)'s *text* still demands 12. REFACTOR check (a) to "11 genuine migrations have all 4 artifacts; wiring deterministic-exempt; remediate parity-only (no roadmap_ids)." (Unanimous with architect + analyzer.)

**Coverage of failure signatures:** The gate checks both over-constraint (schemas blocking valid LLM output — (b) implicit, and the explicit "over-constrain schemas blocking valid LLM outputs" in the stance) AND under-constraint (phantom-ID rejection (c)). Two-sided. Good QA coverage.

**Verdict: REFACTOR (light)** — only check (a) count/exemption wording.

---

## Step PG9.2 — act on verdict

**Testability:** Binary IF PASS/FAIL on the verdict file, with concrete proceed-decision path and max-3-cycle HALT. Fully verifiable. Matches every prior PG. No new test risk.

**Edge case — what if wiring-exemption causes a spurious FAIL upstream in PG9.1?** Then PG9.2's FAIL branch ("address findings, re-run failing parity tests, re-spawn") could loop on a non-defect (the wiring exemption) up to 3 times then HALT+escalate — wasted cycles. This is downstream of the PG9.1 check (a) fix; once (a) encodes the exemption, PG9.2 is clean. So PG9.2 itself is fine; its quality depends on PG9.1 being fixed.

**Verdict: KEEP** — standard, fully testable; no change needed to PG9.2 itself.

---

## QA phase-coherence summary

From a "can a worker finish and prove it" lens:
- **9.12 is the worst-formed item:** its completion criterion (≥3 release cycles) is structurally unsatisfiable within the task, and its input glob (12 validation txts) doesn't match reality (9 today, 11 after 9.11, 13 in the yaml). Must be re-scoped to a now-verifiable initial-state decision + deferral, sequenced after 9.11, sourced from the H5 yaml.
- **9.11 needs a/b/c/d/e split** so each migration has independent pass/defer proof (H4), and remediate's "parity test" is ill-defined for a file-edit prompt (no artifact to diff, no roadmap_ids to assert).
- **PG9.1 check (a)** will false-FAIL the by-design wiring exemption; fix the count/wording.
- **PG9.2** is clean once PG9.1 is fixed.
No DISCARDs. **Highest-impact QA finding:** the "12 has all 4 artifacts" predicate is false-by-design and will manufacture a phantom gate failure unless the wiring exemption + remediate-parity-only nature are encoded into PG9.1 check (a) and 9.12's readiness verdict.
