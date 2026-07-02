# Why the 5-phase RF QA + Tier-2 Reflect audit passed 4 real bugs (PR #209)

**Date:** 2026-07-02 · **Investigators:** 4 parallel agents (auggie-grounded) · **Subject:** `contract_setup` package, findings F1–F4 caught by Augment after full internal QA + a Tier-2 `/sc:reflect` audit returned `verdict: pass, regression: 0`.

The four investigations converge on **one meta-failure with four reinforcing mechanisms**: **every gate measured the work against the spec or against its own tests — nothing measured it against external correctness.** The bugs were spec-conformant and test-conformant, so they were invisible to a spec-and-test-conformant QA stack.

---

## The four bugs, by type

| Bug | File | Nature | Real severity |
|---|---|---|---|
| F1 | `diagnosis.py` | `diagnose()` file-only evidence guard ⟂ sibling `load_evidence()`/`_evidence_sha256()` accept a dir | false EVIDENCE_MISSING |
| F2 | `candidate.py`/`questions.py` | app-slug override in wrong bucket; no dedicated field; **no test at all** | operator can't select identity |
| F3 | `questions.py` | `probe_pr` question reads `answers.pr_number` (nonexistent) not `answers.probe_pr` → answer silently ignored | genuine bug |
| F4 | `candidate.py` | `_path_resolves()` treats all-None list as resolved → paths falsely observed | **lockability-affecting**; `findings_locus` ∈ `MUST_OBSERVE_FIELDS`, gated by `lockgate.py` |

---

## Mechanism 1 — QA is a spec-anchored STAR; no edges between code symbols (F1, F3)

Every RF lens audits **one symbol against the design in isolation**: template-conformance = names vs design; evidence-quality = behavior traces to design; no-side-effect = boundaries; domain-accuracy = state/rule vs design. This is a star topology — every spoke points at the design hub, **no spoke connects two code symbols**.

- F1 and F3 are *contradictions between two individually-correct symbols* (diagnose vs load_evidence; a question's answer-attr vs the real dataclass field). Each endpoint passes its own spec check; the contradiction lives on an edge no lens traverses.
- The lens literally named **`internal-consistency`** (Step 5.3) operated at **doc/CLI command-string parity**, not code function-to-function invariants — all its checks were "the command string is byte-identical across files." (`final-qa-internal-consistency.md`)
- template-conformance verified `SETUP_QUESTIONS` has "16 correctly-named IDs" (PASS) but **never that each question's `derive_default` reads a field that exists on `SetupAnswers` and flows through** `derive_candidate`. The probe_pr answer-flow test only exists because the *fix* added it.

## Mechanism 2 — Code, tests, and QA share one mental model; consistency was green *because* the bug was shared (F2, F4)

Code, tests, and in-context QA all derived from the same `design.md`/`merged-requirements.md`. So "code ⇔ test consistency" was maximally green **exactly when the shared blindspot was present**.

- **F4 smoking gun:** the pre-fix test authored a comment (`dc507305:test_contract_setup_validation.py:131-135`) that *reverse-engineered the buggy behavior from the code and froze it as the spec*: "`_path_resolves` treats a non-empty list of all-None as 'resolved' … That is the honest null case." The paired test then **asserted the bug's output** (`severity_field_path == "reviews[].severity"` when the correct answer was `comments[].severity`).
- **F2:** app-slug override read from `answers.decline_detection_fields[...]`; `SetupAnswers` had no field; **zero override-flow test existed.** acceptance-traceability's "16/16 IDs present" is satisfiable with no behavioral answer-flow test.
- The Phase-4 adversarial lenses (test-structure "assume 10 test-smells"; edge-case-completeness; acceptance-traceability) **PASSED over bug-pinning tests** because they check *is this a concrete behavioral assertion / is coverage present*, not *is the asserted value correct*. A precisely-wrong assertion passes a "concreteness" check.

## Mechanism 3 — Reflect's deviation taxonomy is spec-relative; regression=0 was vacuous *and* unrun (all four)

- Reflect classifies divergence as authorized / necessary / drift / regression — **all measured as distance from the driving spec** (`refs/deviation-taxonomy.md` names the spec the "gold-standard reference"). F1–F4 are 100% spec-conformant, so they generate **zero divergence to classify — invisible by construction.** Reflect asks "did they build what the spec said," never "is what they built correct."
- **Verification-triangle double failure** (`return-contract.yaml`): `verification_ran: false`, `verification_skip_reason: tool-unavailable` → **`regression: 0` was derived without running a single test**, from the task-log self-report — while `status: success` and `degraded_components: []` hid the degrade. Even had it run, the tests **encoded** the bugs (Mechanism 2), so pytest exit 0 would have *ratified* them.
- `regression: 0` is a **delta** metric (contradicts a previously-passing test). `contract_setup/` is brand-new — no baseline — so first-implementation correctness bugs are **outside the class's domain of definition.**
- Ensemble also silently under-ran: `reviewer_count: 2` (the kimi slot produced no review) yet `degraded_components: []`. The 3 heterogeneous reviewers + adversarial pass produced **zero findings touching F1–F4** — all findings were frontmatter/completion-gate bookkeeping (status Doing, Step 5.6 unchecked, `reflect_post: ""`).

## Mechanism 4 — A KNOWN quirk was laundered into a spec (F4)

F4 was **not missed — it was diagnosed, documented, and pinned as intended**, then survived every downstream gate:
1. Test comment turns the bug into an "API note / honest null case" and asserts it.
2. edge-case-completeness files only *adjacent* INFO notes, never names the quirk.
3. The explicitly **adversarial** domain-accuracy lens *reads `_path_resolves` directly* and cites it as **proof** that "no field is hardcoded observed without a payload-resolution predicate" — PASS. The adversarial reviewer used the buggy code as evidence of its own correctness.
4. Zero-tolerance consolidation ("FAIL on any issue of any severity") *did* fire — but on an unrelated redaction guard. F4 never entered the issue ledger **because it was pre-classified as accepted-API by its author.** The ability to articulate the quirk granted the authority to accept it.

---

## Prioritized protocol fixes (additive)

**P0 — Spec-independent correctness/oracle lens (fixes the class).** Add to both the RF QA lens set and the `reflect-reviewer` brief a reviewer whose prompt *sets the spec aside*: "ignore the requirements — does this function do the obviously-right thing on edge inputs (empty, all-None, dir-vs-file, missing key)?" This is exactly the reasoning Augment used. Without a spec anchor it cannot be fooled by spec-conformance.

**P0 — Rationalization-comment auto-escalation (fixes Mechanism 4).** Any test/source comment that *explains or justifies* non-obvious behavior ("API note", "quirk", "treats X as Y", "honest case", "X != Y", "resolves for") auto-creates a `needs_human_decision` correctness ticket that HALTS the phase gate until an isolated second lens confirms intent. An INFO finding about resolution/validation/lockability logic may **not** be self-closed by the authoring lens.

**P1 — Cross-symbol invariant lens (fixes F1/F3).** A code lens whose two operands are both code symbols in one package: "sibling functions consuming the same value agree on its shape (file vs dir)"; "every declarative answer-attr statically resolves to a real dataclass field and flows through." Cheap deterministic backstop: a test that asserts every `SETUP_QUESTIONS` deriver reads a real, flow-through `SetupAnswers` field.

**P1 — Mandatory property/differential negative test for every gate helper (fixes F2/F4).** Any helper that decides lockability / observed-provenance / resolution MUST ship a negative/property test (all-None, empty, missing key). A gate helper with only positive-resolution tests FAILs the Phase-4 test lens. This forces `test_severity_path_all_none_does_not_resolve` (added only *after* Augment) to exist up front.

**P1 — Never trust the author's own tests as reflect's oracle; treat skipped verification as a DEGRADE.** `verification_skip_reason: tool-unavailable` must set status DEGRADE, never a silent pass; `regression: 0` derived without a run is `regression: unknown`. Down-weight a green triangle when the audited diff includes the author's own tests; require an out-of-tree oracle for new-code correctness.

**P2 — Fix the honest-degrade accounting.** `reviewer_count < requested` must populate `degraded_components`; the ensemble cannot report a clean non-degraded pass while a reviewer slot silently produced nothing.

---

## One-line verdict

The stack was a **closed loop**: spec → code → tests → QA(vs spec & tests) → reflect(vs spec, tests unrun). Augment broke the loop only because it reviewed the code **against nothing but correctness.** Every recommendation above is a way to inject that same spec-free, out-of-tree adversarial correctness signal *inside* the loop.
