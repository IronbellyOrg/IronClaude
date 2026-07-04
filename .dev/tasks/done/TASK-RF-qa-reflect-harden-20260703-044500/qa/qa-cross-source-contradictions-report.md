# QA Report — M4 Source-Document Fidelity / Cross-Source Contradiction Gate

**Topic:** PR #209 QA/Reflect blindspot additive hardening (FX1/FX2/FX3/FX5/FX7)
**Date:** 2026-07-03
**Phase:** report-validation (cross-source contradiction sub-gate)
**Fix cycle:** N/A (fix_authorization: false — REPORT ONLY)
**Adversarial hypothesis under test:** "The change set followed the plan's STALE text instead of the research override in at least 3 places."

---

## Overall Verdict: PASS

The adversarial hypothesis is **REFUTED**. Across all 6 enumerated plan-vs-research/code contradictions, the change set honored the RESEARCH/CODE resolution — **zero** instances of the driving plan's stale literal text being encoded. Two contradictions (FX7 verdict-degrade paths) were correctly routed to `needs_human_decision` PENDING markers rather than auto-applied, and one research claim (08 G6 "degrades without a consumer edit") was itself found CODE-CONTRADICTED and correctly superseded.

Source-of-truth precedence honored: **research/07 + research/08 (CODE-VERIFIED) > driving plan §2/§5 (stale prose).**

---

## Enumeration — Plan-vs-Research/Code Contradictions + Authoritative Resolution + Honored?

Each row: what the driving plan (`FINAL-remediation-plan.md`) literally says → why it is CODE-CONTRADICTED (source-doc citation) → the authoritative resolution → whether the change set honored it (spot-check evidence).

### C1 — Plan: "rename/augment the `internal-consistency` lens" (FX2) → CODE-CONTRADICTED

- **Plan text:** §2 line 46 + §5 line 88: "rename/augment the mis-scoped internal-consistency lens to check code function-to-function invariants."
- **Contradiction (source docs):** research/07 §Deliverable 6 (lines 125–153): the `internal-consistency` lens DOES exist in `rf-qa-qualitative.md` (lines 92, 307, 755) but is a **document-prose** consistency lens, NOT a "doc/CLI string parity" lens and NOT a code symbol-to-symbol lens. The plan's premise (that it is a string-parity lens to be renamed into a code lens) describes the PR #209 QA-RUN artifact, not the brief charter. research/08 G3 (decisive) confirms the correct home is the **task-qualitative "Code Compatibility" group, items 4-6** (`:670-676`), which already read source symbols — augmenting in place is an in-scope AX-2 sharpening, NOT a rename and NOT scope creep.
- **Authoritative resolution:** FX2 augments Code-Compatibility item(s) 4-6 IN PLACE, annotate `AX-2`, add NO AX-6, keep the "(15 items)" count (G1 Branch A). Do NOT rename any `internal-consistency` lens.
- **Honored? YES.** `git diff rf-qa-qualitative.md`: the ONLY substantive edit is to **item 5 "Module context analysis"** (`:674`), appending a "Cross-symbol input-shape invariant (annotate `axis: AX-2`)" clause citing the F1 `diagnose()`/`load_evidence()` example, plus the matching overlay-table row 5. Grep of the diff for `internal-consistency` / `rename` / `Checklist (1` → **empty**: no lens renamed, no count-header bumped, AX-2 vocab used (no AX-6). Matches G3/G1-Branch-A exactly.

### C2 — Plan: "add a 5th 'correctness-gap' dimension" (FX1) → CODE-CONTRADICTED

- **Plan text:** §2 line 47 + §5 line 89: "a 5th 'correctness-gap' dimension in `refs/deviation-taxonomy.md`."
- **Contradiction (source docs):** research/07 §"FX1's 5th dimension CONTRADICTS…" (lines 183–196): `deviation-taxonomy.md:5` explicitly states "The taxonomy is **4 categories** … **not a 5th category**"; the 4-class design + precedence is fixed. Resolution: route to a **parallel artifact** mirroring the `evidence-insufficient`/grounding-gaps pattern.
- **Authoritative resolution:** FX1 is an **advisory PARALLEL dimension** (`correctness-gaps.yaml`), non-gating; the taxonomy stays exactly 4 classes. No 5th class.
- **Honored? YES.** `git diff deviation-taxonomy.md`: adds a section titled **"Correctness-gap (advisory parallel dimension — no 5th class)"** that opens "Adds **no 5th category**," routes to a distinct `correctness-gaps.yaml` parallel artifact, explicitly does NOT set `regression_present` / force `status: partial` / `needs_human_decision`, and closes "preserves the four-class Kill-List invariant." `git diff reflect-reviewer.md`: adds a body-prose "Correctness gaps (advisory — non-gating)" section, explicitly "not a 5th deviation class," and does **NOT touch the `tools:` frontmatter line** (verified: grep for `^[-+]tools:` → empty, protecting `test_reviewer_readonly_tools`). Matches research/07 §FX1 + research/08 G2.

### C3 — Plan: fixes "live on master" → CODE-CONTRADICTED

- **Plan text:** §5 line 78: "contract_setup + tests/pr_submit … live on **master** … Build the task from a branch off `origin/master`."
- **Contradiction (source docs):** research/07 §HL-1 (lines 17–33): `git ls-tree origin/master | grep -c contract_setup` → **0**; the package exists only on this branch / `origin/DetectionContractBranch` (introduced by `dc507305`). A master base "would have no `contract_setup` package to target." Audit base = HEAD `46a787da` on `harden/qa-reflect-blindspot-pr209` off `DetectionContractBranch`, NOT master.
- **Authoritative resolution:** Build on THIS branch; frontmatter `start_commit` = `46a787da…`; integration branch = `origin/DetectionContractBranch`, NOT `origin/master`.
- **Honored? YES.** Task frontmatter line 19-21: `start_commit: "46a787dac39c75753a6da4ca483dc6b5d2581bb0"` with the comment "= git merge-base HEAD origin/DetectionContractBranch (PR #209's target branch — NOT origin/master; contract_setup is absent from master, a master base would swamp the reflect gate)." Phase-1 item (line 200) actively re-verifies both SHAs equal `46a787da…` and asserts branch = `harden/qa-reflect-blindspot-pr209`. `git rev-parse HEAD` confirms current HEAD = `46a787da…`. Matches HL-1.

### C4 — Plan: "Phase-2/Phase-4 pipeline gate" wiring (FX3/FX5) → CODE-CONTRADICTED

- **Plan text:** §2 lines 43-44 + §5 lines 85-86: "wire into RF Phase-2 as a gate prerequisite" / "Phase-4 FAIL rule."
- **Contradiction (source docs):** research/08 G4 (lines 192–238): the literal "Phase 2/4" tokens are **task-builder `SKILL.md`'s OWN internal phase/gate numbers** (§A.8 `:685` / §A.10 `:1307`), NOT a pytest attach point in `rf-qa-qualitative.md` (which defines NAMED phases, no numeric 2/4). Decisive: "There is NO SKILL.md §A.8/§A.10 edit required and none should be made." FX3/FX5 are standalone deterministic pytests running in CI/`make test` + as built-task L3 items; FX5's FAIL-rule mirrors the task-qualitative Verdict shape at `rf-qa-qualitative.md:732-735`.
- **Authoritative resolution:** Drop the "Phase-2/4 pipeline gate" framing; FX3/FX5 are ordinary CI + built-task pytests, no pipeline-gate wiring, no SKILL.md edit.
- **Honored? YES.** Change set contains NO `task-builder/SKILL.md` edit (`git status | grep SKILL.md` → empty). FX3/FX5 land as three standalone pytest files (`test_setup_questions_resolution.py`, `test_gate_helper_coverage.py`, `test_gate_helper_differentials.py`) under `tests/pr_submit/`, run via `uv run pytest` (task item line 216). No `pyproject.toml` marker edit (G5-compliant — `--strict-markers` active, marker-free parametrize). Task line 124/170 explicitly encodes "G4 drop 'Phase 2/4 pipeline gate' framing." Matches G4 option (c).

### C5 — Plan/research-08-G6: "populated `degraded_components` degrades WITHOUT a consumer edit" → CODE-CONTRADICTED (research self-corrected; verdict-degrade DEFERRED)

- **Plan/research text:** driving-plan §2 (FX7 row) implies shortfall degrades; research/08 G6 (lines 290-292) asserts populating `degraded_components` "degrades WITHOUT any consumer edit" via `contract.py:259-260`.
- **Contradiction (code, deeper than G6):** `contract.py:31-33` `_DEGRADED_COMPONENTS_HALT_SET = {"serena","auggie","env-aliases","evidence-validator","serena:context-excluded"}`; the FR-11 trigger at `contract.py:265` is `if any(token in _DEGRADED_COMPONENTS_HALT_SET for token in degraded_components)`. A bare `"reviewer-shortfall"` token is **BENIGN** — it is NOT a HALT_SET member, so it does NOT flip the verdict (proven by `test_benign_degraded_component_does_not_over_halt`, and `test_i3` requires a 2-of-3 shortfall stay PASS-eligible per FR-RH2.9). So G6's "degrades without a consumer edit" is itself CODE-CONTRADICTED: making it degrade would require ADDING the token to the HALT_SET (a consumer edit) AND would REVERSE FR-RH2.9/test_i3 (non-additive).
- **Authoritative resolution:** Ship ONLY the VISIBLE benign token + `reviewers_verified`; DEFER the verdict-DEGRADE-on-shortfall as a `needs_human_decision` PENDING (non-additive, reverses FR-RH2.9).
- **Honored? YES.** `git diff ensemble.py`: on genuine shortfall appends `"reviewer-shortfall"` to `degraded_components` with an explicit comment "BENIGN — intentionally NOT a `_DEGRADED_COMPONENTS_HALT_SET` member … does NOT flip the verdict … verdict-DEGRADE … DEFERRED as a needs_human_decision PENDING." PENDING marker exists: `phase-outputs/plans/fx7-degrade-on-reviewer-shortfall-DECISION.md` (Status: PENDING, NOT auto-applied; documents both the HALT_SET-gating and the FR-RH2.9/test_i3 reversal). Only the additive visibility (`reviewers_verified`, benign token) shipped. Matches the deferral contract.

### C6 — Plan: edit the exemption set / "degrade on unverified" (FX7) → CODE-CONTRADICTED (DEFERRED; exemption set byte-unchanged)

- **Plan text:** §2 line 45 + §5 line 87: "downgrade `status`→`degraded` when `verification_ran:false`."
- **Contradiction (source docs):** research/07 §"FX7 CONTRADICTS an existing deliberate exemption" (lines 159–181): `contract.py:35-38` `_VERIFICATION_SKIP_EXEMPTIONS = {"read-only-project","tool-unavailable","--no-verify"}` deliberately exempts the post-mortem's exact `tool-unavailable` smoking-gun; forcing degrade would remove `tool-unavailable` (NON-additive, reverses R2-F2, breaks `test_r2f2`/`test_i1`). research/08 G6 offers a builder-only additive path but flags a fail-safe HALT if the goal ever needs an exemption change.
- **Authoritative resolution:** Do NOT edit `_VERIFICATION_SKIP_EXEMPTIONS`; keep the exempt skip reason; surface vacuity via NEW `verification_verified: false` visibility field only. The aggressive "degrade on ANY unverified run" is DEFERRED as a `needs_human_decision` PENDING.
- **Honored? YES.** `git diff contract.py`: the ONLY change is additive `_make_result` mapping of the three new `*_verified` visibility fields; `_VERIFICATION_SKIP_EXEMPTIONS` (`:36-38`) is **BYTE-UNCHANGED** (not present in the diff; `sed` confirms the frozenset intact). `ensemble.py` still emits `verification_skip_reason: "tool-unavailable"` (unchanged) plus additive `verification_verified: false`. PENDING marker exists: `fx7-degrade-on-unverified-DECISION.md` ("What was auto-applied: ONLY Option A … `_VERIFICATION_SKIP_EXEMPTIONS` is BYTE-UNCHANGED"). Matches research/07 §FX7 + R2-F2.

---

## Items Reviewed

| # | Check (contradiction) | Result | Evidence |
|---|-----------------------|--------|----------|
| C1 | FX2 not a lens rename (augment items 4-6 in place) | PASS | `git diff rf-qa-qualitative.md` item 5 + overlay row 5 only; grep `internal-consistency`/`Checklist (1` → empty |
| C2 | FX1 no 5th category (advisory parallel dimension) | PASS | `git diff deviation-taxonomy.md` "no 5th class" section → `correctness-gaps.yaml`; reflect-reviewer body prose; `tools:` untouched |
| C3 | Branch base = DetectionContractBranch @ 46a787da, not master | PASS | frontmatter `start_commit` + comment (task L19-21); Phase-1 re-verify item L200; `git rev-parse HEAD`=46a787da |
| C4 | No Phase-2/4 pipeline-gate wiring (ordinary pytests) | PASS | no SKILL.md/pyproject edit in `git status`; 3 standalone `tests/pr_submit/` files; task L124/170 |
| C5 | degraded_components verdict-degrade DEFERRED (only visible token shipped) | PASS | `ensemble.py` benign token + comment; `fx7-degrade-on-reviewer-shortfall-DECISION.md` PENDING; not in HALT_SET (`sed` L31-33) |
| C6 | Exemption set byte-unchanged; degrade-on-unverified DEFERRED | PASS | `_VERIFICATION_SKIP_EXEMPTIONS` absent from `contract.py` diff; `fx7-degrade-on-unverified-DECISION.md` PENDING |

## Summary

- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report only)
- Adversarial hypothesis ("stale text followed in ≥3 places"): **REFUTED with per-item evidence.**

## Issues Found

None. Note per QA philosophy: a zero-issue verdict is treated as suspect. It is defended here by 6 independent diff/grep/sed spot-checks (see Tool engagement), each mapping to one contradiction, plus two PENDING decision markers proving the two hardest (non-additive) resolutions were *deferred* rather than silently followed or silently auto-applied. The adversarial hypothesis was actively pursued against the actual change set, not assumed absent.

## Notable robustness observation (not a defect)

C5 is the strongest fidelity signal: the change set out-performed its own upstream research. research/08 G6 asserted a populated `degraded_components` "degrades without a consumer edit" — the implementer found that claim itself CODE-CONTRADICTED (HALT_SET-gated at `contract.py:265`; degrading reverses FR-RH2.9/test_i3), shipped only the additive visible token, and deferred the verdict-degrade to a `needs_human_decision` PENDING. Source-truth-over-documentation was applied even against the research layer, not just the stale plan.

## Confidence Gate

- **Confidence:** "Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 4 | Grep: 6 | Glob: 0 | Bash: 8" (no web research performed — all claims are local source-doc + change-set intrinsic; Tavily not required)
- All checklist items VERIFIED with tool evidence (git diff / grep / sed / find / rev-parse). Tool-call count (18) ≥ 6 checklist items — not suspect.

## Recommendations

- Proceed. All 6 source-document contradictions resolved per the authoritative research/code layer; no stale plan text encoded.
- Downstream reviewers should treat the two `phase-outputs/plans/fx7-*-DECISION.md` PENDING markers as open `needs_human_decision` items (verdict-degrade-on-shortfall and degrade-on-unverified). They are correctly NOT auto-applied; a human must decide whether to accept the FR-RH2.9 / R2-F2 reversal + test churn if that behavior is ever wanted.

## QA Complete
