# Reviewer 2 — Correctness & Contradiction Lens (Tier-2 Pre-Execution Reflection)

**Persona:** qa / adversarial correctness
**Spec:** `.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-spec.md`
**Tasklist:** `.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260610-144537/TASK-RF-troubleshoot-hardening-20260610-144537.md`
**Scope:** Audit whether each tasklist item, as written, instructs the executor to produce a spec-FAITHFUL result — hunting STALE-ENUM, CONTRADICTION, STALE-LINE-NUMBER, INVARIANT-MISMATCH, QA-POLARITY-INVERSION, OPERATIONAL-BREAK, and POST-reflect-form defects.

---

## Method

Read both files in full (spec 444 lines; tasklist 389 items + log template). Cross-checked:

- Every `advisory` occurrence in the tasklist (grep) against the spec's removal of the verdict-context `advisory` token (§6.2 C3, line 112/127).
- Field-count assertions (header "~13 fields" vs Step 2.8a "5 non-gate" + Step 2.8b "4 status + 4 path") for internal consistency and against spec §6.2.
- The C2 verdict-invariant prose in Step 2.1 / 2.9 / 2.11b against spec §6.2 (lines 129-135).
- The §4 rejected-substitution→gate mapping asserted in Step 2.1 against spec §4 (lines 54-59).
- Phase-4/5 QA-lens prompts (Steps 4.3, 4.6, 4.7, 4.9, 5.1, 5.5a) for advisory polarity.
- The POST-reflect item (line 388) against spec/GF-3 form requirements and penultimate placement.
- Edit-anchor strategy (TEXT vs absolute line numbers) across Phase 1 + Phase 2.

---

## Findings

### Defect-class sweep results (the seven hunted classes)

| Class | Result |
|---|---|
| 1. STALE ENUM (`advisory` in verdict context / "add advisory") | **CLEAN** — see F1 |
| 2. CONTRADICTIONS (field counts, status field, etc.) | **CLEAN** — see F2 |
| 3. STALE LINE NUMBERS as primary anchor | **CLEAN** — see F3 |
| 4. C2 INVARIANT MISMATCH (vacuous-pass / pass predicate) | **CLEAN** — see F4 |
| 5. QA-GATE POLARITY (advisory-present vs advisory-absent) | **CLEAN** — see F5 |
| 6. OPERATIONAL BREAKS (make targets, anchors) | 1 MINOR — see F7 |
| 7. POST-reflect form | **CLEAN** — see F6 |

---

#### F1 — STALE ENUM: NO surviving verdict-context `advisory`. (severity: none / PASS)

- **Tasklist anchors checked:** every `advisory` token. The occurrences are:
  - OQ #2 (line 151): "...`advisory` was removed per adversarial critique C1/C3..." — this is a *removal* statement, correct.
  - Step 2.1 (line 184): "...the no-`advisory` note C3...", "...values exactly `pass | blocked | not_applicable` — NO `advisory`..." — correct, instructs ABSENCE.
  - Step 2.8a (line 224), Step 2.9 (line 232), Step 2.11b (line 244), Step 2.12 (line 254), Step 2.14 (line 264): all say "NO `advisory`" — correct.
  - QA prompts 4.3/4.6/4.7/4.9/5.1/5.5a: all treat a surviving `advisory` as a DEFECT — correct.
  - H1 blocking-rule "advisory as fatal" (referenced for Step 2.1/2.2) is the legitimate **E4-escape-mechanism description** (spec line 184), not a verdict token. Permitted by the reviewer's own carve-out.
- **Spec basis:** §6.2 C3 (lines 112, 127); acceptance #11 (line 414).
- **Verdict:** No item asserts the 4-token enum and no item instructs ADD `advisory`. The stale-enum class is fully clean.

#### F2 — CONTRADICTION: field counts are internally consistent. (severity: none / PASS)

- **Tasklist anchors:** header Key Objective #2 (line 72) "~13 fields: 5 non-gate ... the 4 per-gate `*_status` ... the 4 `*_card_path`"; Step 2.8a (line 224) appends the **5 non-gate** rows; Step 2.8b (line 228) appends **4 status + 4 path** rows. 5 + 4 + 4 = 13. The internal-consistency QA lens (4.3, line 300) and completeness lens (4.7) both enumerate exactly the same 5 non-gate / 4 status / 4 path names.
- **Spec basis:** §6.2 table (lines 111-123) has exactly 13 rows: `pipeline_hardening_applicable`, `pipeline_hardening_verdict`, 4×`*_status`, 4×`*_card_path`, `gate_na_rationale`, `off_path_review_decision`, `known_escapes_caught` = 2 + 4 + 4 + 3 = 13.
- **No "8 vs 13" contradiction exists.** The phrase "8-field" appears only inside QA prompts (4.6, 4.7-class) as a token-to-FLAG-as-defect, never as an assertion the executor should encode. The `status` field is present in every consumer (SKILL 2.8b, hub 2.1, report 2.12, remediation 2.14). Clean.

#### F3 — STALE LINE NUMBERS: TEXT-anchoring is mandated everywhere. (severity: none / PASS)

- **Tasklist anchors:** Key Constraints (line 118) "Anchor every Edit on exact TEXT, not absolute line numbers (line numbers in research are off-by-one trailing-newline artifacts — see GF-1)"; Phase 2 preamble (line 178) "Anchor every Edit on exact current TEXT from the discovery inventory ... NOT on absolute line numbers"; every read-spec instruction in Steps 2.2-2.14 repeats "section refs are authoritative; line numbers approximate — anchor on heading text". Phase 1 Step 1.4 (line 174) builds a TEXT-anchor discovery inventory.
- **Spec basis:** spec was adversarially rewritten/grew; absolute line cites would be stale. Tasklist correctly never uses a spec absolute line number as the primary edit anchor.
- **Verdict:** Clean — this is exactly the mitigation the lens demands.

#### F4 — C2 VERDICT INVARIANT: tasklist encoding matches the spec; vacuous-pass closed. (severity: none / PASS)

- **Tasklist anchors:** Step 2.1 `## Verdict invariant` instruction (line 184) reproduces all three branches: `not_applicable` **iff** `applicable=false` (legal only under zero-trigger skip); `pass` **iff** `applicable=true` (resolved) ∧ EVERY mandatory-set gate `status=PASS` with non-null path ∧ ZERO gates `NOT_PROVEN` ∧ `off_path_review_decision ∈ {performed, not_required, waived_with_rationale}`; `blocked` otherwise. It explicitly carries the **vacuous-pass-closed** property ("all `*_card_path = null`, all statuses `NA`, `known_escapes_caught = []` CANNOT emit `pass` while `applicable = true` — it is `blocked`") and the off-path→verdict invariant M2.
- **Cross-check:** Step 2.9 (line 232) and Step 2.11b (line 244) reference "the §6.2 C2 verdict invariant" for the Wave 4.5 verdict computation and the Wave 6 gate (`pipeline_hardening_verdict ∈ {pass, not_applicable}`), consistent with the apex definition.
- **Spec basis:** §6.2 C2 (lines 129-135), acceptance #12 (line 415).
- **Verdict:** Byte-aligned with the spec's total-function definition. The `off_path_review_decision ∈ {performed, not_required, waived_with_rationale}` set in the PASS predicate matches spec line 132 exactly. Clean.

#### F5 — QA-GATE POLARITY: lenses assert advisory-ABSENT = correct; no inversion. (severity: none / PASS)

- **Tasklist anchors:** Step 4.3 (line 300) "`advisory` MUST be ABSENT (its presence is a defect, per spec C3)"; Step 4.6 "verify the verdict enum is exactly the three tokens ... with `advisory` ABSENT ... flag any surviving `advisory` token ... as a defect"; Step 4.9 "Flag any rule that ... reintroduces `advisory`"; Step 5.1 "a surviving `advisory` token ... is a fidelity DEFECT per spec C3"; Step 5.5a "no `advisory` token reintroduced".
- **No lens requires advisory-PRESENT.** Every Phase-4/Phase-5 QA prompt treats advisory PRESENCE as the failure and ABSENCE as PASS — the correct, non-inverted polarity.
- **Spec basis:** §6.2 C3 (line 127), acceptance #11.
- **Verdict:** Clean. (This is the precise inversion class that bit prior runs per memory `feedback_sc_reflect_vs_inline_rfqa`; here it is correctly oriented.)

#### F6 — POST-reflect item: correct self-run form, merge-base working-tree diff, --spec, depth deep, penultimate. (severity: none / PASS)

- **Tasklist anchor:** line 388. Confirmed: `<BASE> = git merge-base HEAD <integration-branch>` with `<integration-branch>` resolved via `git symbolic-ref --short refs/remotes/origin/HEAD` (→ `origin/master`), "passed as a SINGLE ref so the diff is taken against the working tree" and explicitly "NOT `start_commit..HEAD`"; `--spec .dev/troubleshoot-meta/.../troubleshoot-pipeline-hardening-spec.md` set; `--depth deep`; `git add -A` before to capture untracked new refs; declared PENULTIMATE.
- **Penultimate verified:** line 388 is followed by exactly one item — the "Update ... status to '🟢 Done'" frontmatter item — so PENULTIMATE is factually true (not a stale claim against a missing successor).
- **Spec basis:** matches the project's corrected POST-reflect form (commit `10723863` "base POST-reflect --diff on merge-base working-tree, not start_commit") and memory `feedback_sc_reflect_vs_inline_rfqa`.
- **Verdict:** Clean.

#### F7 — MINOR (operational): Step 3.3 markdownlint invocation is fallback-described, not pinned. ([INFERRED])

- **Tasklist anchor:** Step 3.3 (line 280): "invoking the repo's configured markdownlint (e.g. via the pre-commit hook `pre-commit run markdownlint --files <the 9 paths>` ..., or the project's equivalent markdownlint command discovered from `.pre-commit-config.yaml`)".
- **Why it's a (minor) risk:** the item does not assert that a `markdownlint` pre-commit hook id actually exists; it hedges with "or the project's equivalent ... discovered from `.pre-commit-config.yaml`". If the hook id is named differently (e.g. `markdownlint-cli2`), the literal `pre-commit run markdownlint` token would no-op/error and the executor must fall back. The item DOES build in the fallback ("discovered from `.pre-commit-config.yaml`"), so this is self-healing, not a hard break — hence MINOR. [INFERRED: I did not read `.pre-commit-config.yaml` in this review; the hook id is unverified.]
- **Fix (optional):** before relying on the literal hook id, have Step 3.3 first `grep -n markdownlint .pre-commit-config.yaml` to resolve the exact hook id, then run it. The current "discovered from" clause already permits this, so no blocking change is required.
- **Not a correctness-of-result defect:** even if the first invocation form misses, the item's stated PASS condition is "the 9 source files are clean", which the fallback still achieves.

---

## Additional positive confirmations (no defect, worth recording)

- **§4 rejected-substitution→gate map** in Step 2.1 (`1→H1, 2→H4, 3→H1, 4→H3, 5→H2, 6→H4/H5`) is **correct** against spec §4 (lines 54-59): (1) command-string→H1, (2) artifact/PASS-report→H4, (3) edited-helper-tests→H1 runtime-evaluator-proof, (4) one-repro→H3, (5) generic-evaluator→H2, (6) off-path-empty/stale/foreign→H4/H5. No mis-mapping.
- **3-column Output Contract model** (Steps 2.8a/2.8b): the tasklist correctly detects the live `## Output Contract` table is 3-column `| Field | Type | Description |` with NO `Default` column, and folds §6.2's Default into the Description cell to avoid an MD056 column-count violation. This is a real operational hazard the tasklist pre-empts correctly.
- **NOT_PROVEN as first-class status forcing `blocked`** is encoded consistently in Step 2.1 (`## Closure verdict + NOT_PROVEN rule`), Step 2.13 (report-template post-EOF rule), Step 2.11a (completeness gate), and the QA lenses 4.9/5.1 — matching spec §8 (line 370) and acceptance #14.
- **H5 mandatory / off-path→blocked** is folded into the hub ref (Step 2.1 `## Rule H5`) and wired into the Wave 6 precondition (Step 2.11b), matching spec §6.2 M2 (line 137) and §7 Rule H5 (line 319). No "H5 is optional" language survives.
- **Scope guardrail** (line 120): correctly forbids editing PRD/pipeline/reflect source; names `PrdExecutor._evaluate_gate` / `pipeline.gates.gate_passed` as FROZEN EVIDENCE ONLY. Consistent with the spec's protocol-doc-only scope (§9).

---

## Verdict

**Are there any CRITICAL contradictions or inversions that would make execution produce a spec-INFIDEL result?**

**NO.**

The seven hunted defect classes are clean on the six that matter for fidelity (stale-enum, contradiction, stale-line-number, C2-invariant, QA-polarity, POST-reflect form). The single finding (F7) is a MINOR, self-healing operational hedge in the markdownlint invocation that does not affect the correctness of the produced output.

### Severity counts

| Severity | Count |
|---|---|
| CRITICAL | 0 |
| IMPORTANT | 0 |
| MINOR | 1 (F7) |

### Self-confidence

**0.88**

Basis for not scoring higher: I verified the spec and tasklist in full and grep-swept all `advisory`/field-count/enum tokens, but (a) F7's hook-id is [INFERRED] — I did not open `.pre-commit-config.yaml`; (b) I did not open the live edit-target files (`SKILL.md`, `report-template.md`, etc.) to confirm the Phase-1 discovery anchors will actually resolve — that is the correctness lens's residual blind spot, since a non-existent text anchor (defect class 6) can only be fully ruled out by reading the live targets. The tasklist's mitigation (Phase 1 Step 1.4 builds the anchor inventory from the live files at run time, and every edit item re-reads the inventory) structurally contains that risk, which is why I judge it non-CRITICAL rather than verifying each anchor here.
