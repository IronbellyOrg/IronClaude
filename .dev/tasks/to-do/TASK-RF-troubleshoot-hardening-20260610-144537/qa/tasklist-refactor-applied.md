# Tasklist Refactor — Change-Application Report

**Date:** 2026-06-10
**Agent:** Single serialized fix agent (I20)
**Target (edited in place):** `.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260610-144537/TASK-RF-troubleshoot-hardening-20260610-144537.md`
**Ledger applied:** `.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260610-144537/qa/tasklist-refactor-ledger.md`
**New source of truth:** `.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-spec.md`

All edits were surgical Edit calls anchored on quoted TEXT, never line numbers. The file structure (frontmatter, Execution Context, Task Log templates, anti-orphaning) is preserved.

---

## GLOBAL CORRECTIONS

### G-ENUM (CS-3) — obsolete 4-token verdict enum → 3-token
- **Anchor:** every occurrence of the verdict enum `pass | blocked | advisory | not_applicable` and `{pass, advisory}` in VERDICT/output-contract context.
- **Applied in:** Header OQ-2 (rewritten); Objective 2 ("append 8 fields" → full ~13-field set); hub-ref item (Step 2.1) output-contract + verdict-invariant; output-contract split 2.8a; Wave 4.5 emit line (Step 2.9); Wave 6 precondition (2.11b); report-template §8 block (Step 2.12); remediation-handoff gating set (Step 2.14, `{pass, advisory}`→`{pass, not_applicable}`); QA internal-consistency lens (Step 4.3); QA spec-fidelity lens (Step 4.6); QA blocking-rule-accuracy lens (Step 4.9); M4 fidelity-agent prompts (Steps 5.1, 5.2); fidelity verification agents (5.5a).
- **Result:** verdict enum is now exactly `pass | blocked | not_applicable` everywhere it appears as the output contract verdict.
- **Preserved (per ledger):** the THREE E4-escape-mechanism "advisory as fatal" phrases — H1 ref item (Step 2.2 negative-control bullet) KEPT. All remaining `advisory` tokens in the file are either (a) the OQ-2 explanation that advisory was removed, (b) "NO `advisory`" / "advisory ABSENT" polarity-correct instructions, or (c) the E4 example — none is an obsolete verdict value. Verified by grep (zero 4-token enum occurrences).

### G-LINES (A10-M3) — stale absolute spec line numbers demoted
- **Anchor:** items citing "spec lines 136-151", "171-180", "202-211", "241-253", "line 314", etc.
- **Applied in:** hub-ref item (Step 2.1); H1 (2.2); H2 (2.3); H3 (2.4); H4 (2.5); output-contract split (2.8a/2.8b); report-template NOT_PROVEN rule (2.13); M4 fidelity agent 2 (5.2). Each now keeps the § section ref + heading-text anchor and carries "section refs are authoritative; line numbers approximate — anchor on heading text". Verified by grep (zero stale absolute spec-line citations remain).

---

## ITEM-LEVEL CHANGES

| Ledger directive | Anchor text | How applied |
|---|---|---|
| Header OQ-2 rewrite | "Verdict-enum reconciliation (GF-5)" | Replaced with "Verdict enum reconciled in-spec (was GF-5)…`{pass, blocked, not_applicable}` (advisory removed per C1/C3). No build-time divergence remains." A10-M2 note NOT added (obsolete). |
| Objective 2 update | "append 8 output-contract fields" | Now "append the full §6.2 field set (~13 fields: 5 non-gate, 4 `*_status`, 4 `*_card_path`)". |
| Task Log OQ note | "verdict-enum reconciliation GF-5" | Updated to "verdict-enum reconciled in-spec to the three-token enum". |
| Phase 1 G1 back-ref (A10-M1) | "Read the driving spec … §5, §9 … §12" (Step 1.3) | Added "re-read **Open Question 1** (the G1 HALT CONDITION) … the user's `/task` invocation IS the human G1-approval signal". Remains a recorded acknowledgement, not a HALT. |
| **Hub ref rewrite (HEAVIEST)** | "create the file `pipeline-hardening-closure.md`" (Step 2.1) | Embedded content spec fully rewritten: `## Trigger` now the **T1–T9 trigger→gate map TABLE** + mandatory-gate rule + testable skip rule + **trigger-overrides-skip** precedence (CS-1/M6); `## Output contract fields` now the FULL field set (4 `*_status` `{PASS\|FAIL\|NA\|NOT_PROVEN}`, 4 `*_card_path`, `gate_na_rationale`, Default column, status/path rule M7, `known_escapes_caught` pattern `^E\d+$`/`E\d+\+`, 3-token verdict, NO advisory CS-7/CS-4/m1); NEW `## Verdict invariant` (C2 total-function, vacuous-pass-closed ⊇M8, off-path→blocked M2); `## Rule H5` now H5-MANDATORY + off-path→blocked (CS-2b/M2 ⊇m2); `## Closure verdict + NOT_PROVEN rule` (NOT_PROVEN first-class forcing blocked); `## Remediation gating` `{pass, not_applicable}` (was `{pass, advisory}`); §4 six-substitutions list and `## Index of gate refs` kept. |
| H1 ref (Step 2.2) | "create the file `runtime-entrypoint-verification.md`" | Substantively unchanged (advisory-as-fatal E4 example KEPT). Added one-line note that H1 emits its `status` token into `runtime_entrypoint_status` (§6.2). G-LINES applied. |
| H2 ref (CS-11) (Step 2.3) | "create the file `contract-enumeration.md`" | Added `## Consumer-discovery manifest` (exact search terms + symbol/reference queries + result sets) + blocking rule "absence ⇒ H2 `NOT_PROVEN`". Blocking rule now 4 bullets. |
| H3 ref (CS-9/CS-10) (Step 2.4) | "create the file `unmask-and-sweep.md`" | Added `## Completion criteria` (E3-style sibling-heading negative fixture as explicit completion criterion) + `## Fixpoint after discovery` (sweep-discovered boundary ⇒ re-trigger H0/H2 OR dispositioned follow-up). Blocking rule now 3 bullets. |
| H4 ref (CS-5) (Step 2.5) | "create the file `effective-input-proof.md`" | Added `## No-op vs empty` (no changes ⇒ `NA`+no-op proof+rationale; changes ∧ empty ⇒ `FAIL` fail-closed). Blocking rule now 3 bullets. |
| **Output-contract SPLIT (A10 + FM1)** | "**Step 2.8:** Append the 8 new output-contract fields" | SPLIT into **2.8a** (5 non-gate rows: `pipeline_hardening_applicable`, `pipeline_hardening_verdict` 3-token, `off_path_review_decision`, `known_escapes_caught` pattern-constrained, `gate_na_rationale` map; + Default column with CS-4 defaults) and **2.8b** (4 `*_status` `{PASS\|FAIL\|NA\|NOT_PROVEN}` rows DISTINCT from the 4 `*_card_path` rows + status/path rule M7). `advisory` dropped. |
| Wave 4.5 (Step 2.9) | "insert a new `### Wave 4.5: Pipeline Hardening Closure`" | "§6.1 Trigger bullet list" → **T1–T9 trigger→gate map**; gate set computed SOLELY from the map; Emit line `verdict=<pass\|blocked\|not_applicable>` (advisory dropped); references §6.2 C2 verdict invariant. |
| **Failure-wiring SPLIT (A10-I2)** | "**Step 2.11:** Wire the failure-state blocking rules" | SPLIT into **2.11a** (calibration-style completeness gate), **2.11b** (Wave 6 precondition tightened to `pipeline_hardening_verdict ∈ {pass, not_applicable}` + C2 invariant + off-path→blocked CS-2/CS-2b), **2.11c** (`## Will Not Do` bullet). |
| report-template §8 insertion (Step 2.12) | "insert a new `## Pipeline Hardening Closure` section" | Rewrote embedded §8 block: per-gate `PASS\|FAIL\|NA\|NOT_PROVEN — <path> — rationale (required if NA)` on each of 4 gate lines (M7/M3); `Firing triggers / mandatory gate set: T… → H…` line; off-path line gains "(if required and not performed/waived_with_rationale ⇒ verdict = blocked)" (M2/m2); `Closure verdict: pass \| blocked \| not_applicable` (advisory + GF-5 framing deleted); known-escapes pattern note. |
| report-template NOT_PROVEN rule (Step 2.13) | "append a new `## Pipeline Hardening Closure rule`" | Upgraded NOT_PROVEN from prose blocker to FIRST-CLASS gate status forcing `verdict = blocked` per §6.2 invariant. Header normalized to `NOT_PROVEN`. |
| remediation-handoff (Step 2.14) | "add a `## Pipeline-hardening precondition` subsection" | Gating `{pass, advisory}`→`{pass, not_applicable}`; references C2 verdict invariant; `NOT_PROVEN` spelling; failure-mode row keeps blocked-on-unproven behavior. |
| **Phase 4 polarity fix (CRITICAL)** | internal-consistency (4.3): "the FULL `pass \| blocked \| advisory \| not_applicable`"; spec-fidelity (4.6): "the §6.2 8-field table"; completeness (4.7) | INVERTED: enum assertion → `{pass, blocked, not_applicable}` (advisory ABSENT is correct, presence is a DEFECT); "8-field" → full ~13-field set; added verification of trigger map T1–T9, C2 verdict invariant (vacuous-pass closed), per-gate status/rationale + status/path rule, NOT_PROVEN→blocked, H2 manifest, H3 sibling-fixture+fixpoint, H4 no-op-vs-empty, H5-mandatory/off-path→blocked, acceptance 11–15. markdownlint lens (4.4) NOT changed. blocking-rule-accuracy (4.9) updated for C2 invariant + NOT_PROVEN spelling + no-advisory. |
| **Phase 5 M4 polarity + SPLIT (A10-I1)** | fidelity prompts (5.1, 5.2): "full enum … advisory (GF-5)" / "8-field"; "**Step 5.5:** Fidelity verification round + conditional control" | Polarity fixed to 3-token enum + full field set + new invariants. Step 5.5 SPLIT into **5.5a** (spawn 2 fidelity verification agents, `fix_authorization:false`), **5.5b** (consolidate + ONE serialized fidelity fix agent, `fix_authorization:true`), **5.5c** (loop-control, max 3 cycles, escalate/Open-Questions on exhaust). |
| **POST-reflect REORDER (A10-C1)** | "Run the independent POST-execution reflect gate" vs "Create a `### Task Summary`" | Swapped: order is now [verify outputs → no-testing rationale → re-confirm M3/M4] → [Task Summary] → [POST-reflect SELF-RUN, penultimate] → [Update status to Done, final]. POST-reflect command form (merge-base working-tree diff, --spec, depth deep, self-run) unchanged. |

### DO-NOT-CHANGE (confirmed untouched)
- Phase 3 validation items (sync-dev / verify-sync / markdownlint / staging) and markdownlint lens (4.4).
- H1 ref item's advisory-as-fatal E4 example.
- POST-reflect command form (only position moved).
- The 9 target files, anti-orphaning (final "Update status to Done" stays last), Execution Context, Task Log templates, frontmatter, the §4 six-substitutions list.

### OBSOLETE (NOT applied)
- A10-M2 (§8-vs-§6.2 divergence note) — the spec resolved the divergence; advisory removal supersedes. No divergence note added.

---

## FINAL SELF-CHECK (grep evidence)

- **Obsolete 4-token verdict enum (`pass | blocked | advisory | not_applicable`, `{pass, advisory}`):** `NONE` (0 occurrences).
- **`NOT PROVEN` (with space):** `NONE` (0 occurrences) — all normalized to first-class `NOT_PROVEN`.
- **Stale absolute spec-line citations (`spec line[s] N`, `lines NNN`, `line 31N`):** `NONE` (0 occurrences) — all demoted to advisory with § + heading-text anchors.
- **Splits present:** Step 2.8a, 2.8b, 2.11a, 2.11b, 2.11c, 5.5a, 5.5b, 5.5c — all 8 confirmed.
- **POST-reflect penultimate:** confirmed — POST-reflect item immediately precedes "Update task status to Done"; Task Summary immediately precedes POST-reflect.
- **`advisory` residual occurrences:** all legitimate — OQ-2 removal explanation, "NO advisory"/"advisory ABSENT" polarity instructions, and the H1 E4 negative-control example. No obsolete verdict-value `advisory` remains.
