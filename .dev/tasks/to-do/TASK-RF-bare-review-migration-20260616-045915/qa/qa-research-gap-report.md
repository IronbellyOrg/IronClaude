# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** Corrective MDTM tasklist for sc-bare-review M8/M9 migration (WS-0..WS-E)
**Date:** 2026-06-16
**Phase:** research-gate
**Lens:** gap-detection
**Fix cycle:** N/A
**Fix authorization:** false

---

## Scope

Assigned files (verifying ONLY these):
- 01-skill-and-scripts-inventory.md
- 02-swarm-cli-thin-caller-surface.md
- 03-parity-test-and-swarm-test-conventions.md
- 04-docs-and-release-notes-staleness.md
- 05-mdtm-template-and-sync-discipline.md

[PARTITION NOTE: This appears to be the full research set, not a partition. Cross-file checks applied across all 5 assigned files.]

---

## Lens Focus Questions (from spawn prompt)

1. WS-0 CLI-completion concreteness (wire normalize/reduce/emit_contract + 4 flags) — functions, call sites, --resume path?
2. Frozen-golden mechanism concreteness (location, regenerate, permanent test load w/o legacy scripts)?
3. R1 orphan disposition for refs/prompts.md + output-template.md — resolved or open?
4. WS-0 test/verification details (how to test inline path produces return-contract)?
5. §11.5 injection-guard / suspect:true behavior preservation (lens carries identical prompt text)?
6. Missing integration points: anything else import/invoke the 3 scripts (CI, other skills, docs) that WS-C deletion breaks?

---

## Overall Verdict: FAIL

Five research files are individually high quality (dense evidence, file:line citations, accurate cross-validation). But the gap-detection lens surfaces **3 CRITICAL + 3 IMPORTANT + 2 MINOR** coverage gaps that would cause the builder to write an INCOMPLETE migration tasklist that breaks green tests and silently drops parity coverage. Per the research-gate rule, ANY gap = FAIL.

---

## Items Reviewed (lens-focus questions)

| # | Lens question | Result | Evidence |
|---|---------------|--------|----------|
| L1 | WS-0 CLI-completion (B-5 wiring + 4 flags) specified concretely? | PARTIAL (gap G-4) | R2 §"Net findings" B-1..B-5 give per-flag spec_dict targets + anchors (commands.py:1304-1454, :789, :775; dispatch.py:341,:393) AND the B-5 inline-wiring fix with working ref (commands.py:1930-1977). Concrete. BUT no research file says WS-0 must DELETE/INVERT the test that pins the old behavior (see G-4). Verified commands.py:1554-1578 is the stub. |
| L2 | Frozen-golden mechanism concrete? | YES | R3 §4.2-4.7: location `tests/swarm/fixtures/bare_review_v1/golden/<scenario>/`, regen via env-gated human-approved step (§4.6), permanent CLI gate loads golden w/o legacy script (§4.2). Verified fixtures dir exists. |
| L3 | refs/prompts.md + output-template.md orphan disposition resolved? | PARTIAL (gap G-5) | R1 §3.1/§3.2/§5 flag both as orphaned-post-migration and say "builder must decide cross-link vs delete" + "must verify the swarm lens carries identical prompt text" — but leaves it OPEN, not resolved. R4 (docs scope) does not touch prompts.md/output-template.md at all (grep: 0 hits). |
| L4 | WS-0 inline-path test (proves inline emits return-contract)? | NO (gap G-3) | No research file specifies a test asserting the FRESH `swarm run --lens bare-review` path emits `return-contract.yaml`. R3 only designs the golden parity gate (which it says is BLOCKED on the same M5/B-5 wiring) and explicitly defers to R2. |
| L5 | §11.5 injection-guard / suspect:true preservation covered? | PARTIAL (gap G-2) | R2 §2 confirms the lens APPENDS `CANONICAL_INJECTION_GUARD_SENTENCE` (bare_review.py:51; schema.py:133) and `suspect=True` (bare_review.py:63). Verified. BUT no file asserts the lens prompt text is BYTE-IDENTICAL to refs/prompts.md §11.5 — R1 flags this as an unresolved parity risk; nobody closes it. |
| L6 | Other importers/invokers of the 3 scripts (CI/skills/docs)? | NO — MISSED (gap G-1) | Verified `grep -rn` over .github/, Makefile, .pre-commit: ZERO CI refs (good). BUT two test files import the scripts via importlib: `test_bare_review_parity.py` (R3 covered) AND `test_recipe_bare_review.py` (NOT analyzed by any file — see G-1). The MIG-001 pre-commit hook also fires on the deletion commit. |

## Checklist (research-gate 10-item)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory / Status: Complete | PASS (1 caveat) | R1/R2/R4/R5 all "Status: Complete". R3 header says "In Progress" (L3) but footer says "Status: Complete" (L205) — inconsistent self-status, MINOR (G-7). |
| 2 | Evidence density | PASS | All 5 files Dense (>80% file:line). Spot-verified: SKILL.md=231 lines ✓, scripts present ✓, commands.py:1554-1578 stub ✓, bare_review.py:51 guard ✓, schema.py:133 ✓. |
| 3 | Scope coverage | FAIL | `test_recipe_bare_review.py` (an in-scope parity test cited by R1 §1.11/§4) is examined by NO file (G-1). |
| 4 | Doc cross-validation tags | PASS | R4 tags every doc claim [CODE-VERIFIED]/[CODE-CONTRADICTED]. Verified the contradiction: release-notes-v1.md "is now ~60-line thin caller" false (SKILL.md=231). |
| 5 | Contradiction resolution | PASS | No inter-file contradictions; R4 explicitly defers SKILL.md size to R1; figures agree (231). |
| 6 | Gap severity | FAIL | Gaps exist (below). All severities = FAIL per gate rule. |
| 7 | Depth appropriateness | PASS | R2 traces inline run_cmd end-to-end (steps 1-12); R3 traces normalize/reduce seam. |
| 8 | Integration point coverage | FAIL | Script-deletion integration points incompletely mapped: 2nd importlib test + pinning test missed (G-1, G-4). |
| 9 | Pattern documentation | PASS | R5 documents MDTM template rules, sync discipline, L1-L7 + M3 patterns thoroughly. |
| 10 | Incremental-writing compliance | PASS | Files show iterative section growth, not one-shot. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| G-1 | **CRITICAL** | R1 §1.11/§4, R3 §1 (whole file), R5 §3.2 | **Second legacy-importing parity test missed entirely.** `tests/swarm/test_recipe_bare_review.py` (TEST-003 / M8 byte-identity gate, cited by R1 as the M8 milestone) imports `t2_normalize.py` via importlib AND — unlike `test_bare_review_parity.py` which `skipif`s — it does `assert LEGACY_SCRIPT.exists()` (test_recipe_bare_review.py:89-90). When WS-C deletes `t2_normalize.py`, this test **FAILS HARD (collection/assertion error), it does NOT skip.** R3 analyzes ONLY `test_bare_review_parity.py` and disclaims the other ("R3's domain to confirm it passes" — R2 file 02 L148). No file gives the builder a disposition for `test_recipe_bare_review.py`. Without this, WS-C turns a green suite red. | Add a research finding analyzing `test_recipe_bare_review.py`'s skip-vs-fail behavior on script deletion and prescribe its WS-C disposition (delete-with-script, OR convert to a frozen-golden gate like R3's §4 design). Builder must have an item covering BOTH legacy-importing tests, not one. |
| G-2 | **CRITICAL** | R1 §3.1/§5, R2 §2 | **§11.5 prompt byte-parity is asserted-as-risk but never closed.** R1 flags "must verify the swarm lens carries identical prompt text" (parity risk if `prompts.md` orphaned while lens duplicates) and R2 confirms the lens APPENDS the canonical guard sentence — but NO file verifies the lens `system_prompt_fragment` + `user_template` (bare_review.py:47-57) are byte-identical to `refs/prompts.md` §11.5 system/user text. The legacy scripts and the lens could carry divergent prompt wording, silently changing reviewer behavior post-migration. The frozen-golden gate (R3) compares NORMALIZED OUTPUT, not the dispatched PROMPT, so it would not catch prompt drift. | Add a finding that diffs `refs/prompts.md` (system L25-73, user L83-90, guard §11.5) against `bare_review.py` lens fragments + `schema.CANONICAL_INJECTION_GUARD_SENTENCE`, reporting whether they match byte-for-byte. If they diverge, that is itself a migration defect the tasklist must fix. This is the disposition R1 left open. |
| G-3 | **CRITICAL** | R2 §4 / R3 §3.3,§4.5 | **No test specified to prove the WS-0 inline path emits a return-contract.** B-5 is the headline fix (wire normalize/reduce/emit_contract onto the fresh `run_cmd` path). But no research file specifies the VERIFICATION that the fixed inline path actually produces `return-contract.yaml` + normalized `.md` on a fresh (non-resume) `swarm run`. R3's golden gate is explicitly "BLOCKED on R2/M5 landing" — i.e. the only proposed test depends on the fix but no file gives the builder the concrete inline-emission assertion (the L3 test item I18 requires). | Specify a concrete L3 test item: drive `runner.invoke(swarm_group, ["run","--lens","bare-review","--target",t,"--output",o,"--transport","stub"])` and assert `(out/"return-contract.yaml").exists()` + normalized bodies present — the inverse of today's `test_quickstart_does_not_emit_m5_artifacts`. |
| G-4 | **IMPORTANT** | R3 §3.3 (commands.py:1558-1577 / test_e2e_user_guide.py:104-114) | **Existing pinning test that WS-0 will break is not flagged for update.** `test_quickstart_does_not_emit_m5_artifacts` (test_e2e_user_guide.py:104-114) ASSERTS the fresh dispatch path does NOT emit `merged.md`/`return-contract.yaml`/`done.json`. Once WS-0/B-5 wires the pipeline onto the inline path, this currently-green test goes RED. R3 cites it only as evidence of the blocker, never says "WS-0 must delete or invert this assertion." Builder would land B-5 and break CI. | Add an explicit note: WS-0 must delete/invert `test_quickstart_does_not_emit_m5_artifacts` (and audit sibling assertions at test_e2e_user_guide.py:91-97 artifact-set list) as part of the same item that wires the inline pipeline. |
| G-5 | **IMPORTANT** | R1 §3.1/§3.2/§5; R4 (silent) | **refs/prompts.md + output-template.md orphan disposition left OPEN, and split across no owner.** R1 says "builder should decide cross-link vs delete" for both — a decision, not a resolution. R4 owns docs but never touches these two refs (grep: 0 hits in file 04). So the disposition falls in a seam between R1 (skill inventory) and R4 (docs) and is resolved by neither. Per gate item 6, an unresolved disposition is a gap. | Resolve explicitly: state whether each ref is (a) deleted with the scripts, (b) demoted/cross-linked to `refs/templates/bare-review-output.md` (the swarm-aware survivor), tied to the G-2 byte-parity outcome for prompts.md. Assign an owner. |
| G-6 | **IMPORTANT** | R2 §1 B-1 | **Worker-count validity-range divergence noted but not resolved.** R2 notes legacy `--reviewers` validates [2,4] while lens `default_workers=3`, and says "Mirror legacy [2,4] validation or document the divergence" — leaving the choice open. The skill's §3.2 contract and §8 failure-mode ("reviewers out of [2,4]→STOP") are caller-facing guarantees; if the new `--reviewers`/`--workers` flag does NOT enforce [2,4], that is a silent contract regression callers rely on. | Resolve: specify that WS-0's new flag MUST enforce the [2,4] range (preserving the §8 failure-mode contract) OR explicitly document+justify the divergence. Don't leave it as builder's choice. |
| G-7 | MINOR | R3 header L3 vs footer L205 | R3 self-status inconsistent: header "Status: In Progress", footer "Status: Complete". | Reconcile to "Complete". |
| G-8 | MINOR | R2 §1 / R5 §3.2 | `test_escape_hatch_guard_parity.py` (3rd bare-review parity test, listed by R5 L313) is unanalyzed. Verified it does NOT import the legacy script (clean — no skip/fail hazard), so this is informational, but the builder should be told it is unaffected so WS-C scope is complete. | One-line note that `test_escape_hatch_guard_parity.py` is legacy-script-independent and unaffected by WS-C. |

---

## Self-audit

Would the user believe a 0-issue verdict? No — and the evidence I checked proves real gaps:
- `grep -rn t2_normalize` surfaced `test_recipe_bare_review.py` (G-1) that R3 never analyzed; `grep -n "assert.*exists" test_recipe_bare_review.py` → line 89 confirms hard-fail-not-skip.
- `grep -n CANONICAL_INJECTION_GUARD` confirmed the lens APPENDS the sentence but no file diffs the surrounding prompt text (G-2).
- `sed -n 1554,1578p commands.py` confirmed the inline stub; `grep does_not_emit test_e2e_user_guide.py` confirmed the pinning test WS-0 breaks (G-3/G-4).
These are not subjective — each is a tool-verified gap the builder needs closed.

## Confidence

**Confidence:** Verified: 6/6 lens questions | Unverifiable: 0 | Unchecked: 0 | Confidence: 100% (all lens-focus questions resolved with tool evidence; verdict FAIL is high-confidence)
**Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 7 (each Bash mapped to a specific lens question/claim: SKILL/scripts inventory, script-importer sweep, 2nd-test skip behavior, guard schema, B-5 anchor, CI/pre-commit refs, pinning-test confirmation)

## Recommendations (before synthesis/tasklist build can proceed)

1. **Close G-1, G-2, G-3 (CRITICAL) before the builder writes WS-0/WS-B/WS-C items** — these three would otherwise produce a tasklist that (a) breaks `test_recipe_bare_review.py` on script deletion, (b) ships unverified prompt parity, (c) lands B-5 with no inline-emission test.
2. Close G-4, G-5, G-6 (IMPORTANT) — pinning-test update, ref disposition, [2,4] range decision.
3. Fold G-7/G-8 (MINOR) into the same gap-fill pass.
4. These can be resolved by spawning one gap-fill researcher with the 8-item list above; no full re-research needed — the existing files are otherwise dense and accurate.

## QA Complete
