# Analyst Cross-Validation Report — PR #197 reduce-then-merge research

**Analysis type:** completeness-verification
**Lens:** cross-validation (claims BETWEEN research files)
**Date:** 2026-06-28
**Track goal:** MDTM tasklist executing the PR #197 reduce-then-merge plan on `feat/rf-harness-sync`.
**Files analyzed (4):** 01-git-disposition.md (R1), 02-reflect-skill-hunk-surface.md (R2), 03-taskbuilder-clause-flip.md (R3), 04-template-tests-validation.md (R4)

**Scope of this lens:** Cross-validate claims BETWEEN research files. Flag contradictions, conflicting counts, divergent descriptions of the same artifact. This report does NOT re-verify each file against code (that is a separate cross-validation pass); it checks internal coherence ACROSS the four files against the 5 assigned focus questions.

---

## Focus-question findings

### Q1 — R2/R3 coherence of the reflect-skill exclusion model — COHERENT (with one reconciliation the tasklist MUST encode)

**The core question:** Does R2's restore-to-exclusion produce a contract that R3's CLI clause-flip can truthfully assert against? R3 itself flagged this as THE single most important cross-researcher dependency (R3 lines 187–193, "Residual tension").

**R2's established post-merge reflect contract (what is RESTORED to exclusion):**
- §7.1 executor-class exclusion rule restored (R2 H2 / §2.2): executor MUST NOT appear in reviewer pool; resolves class at Wave 0 step 0.5b; emits `executor_class_source: flag|env|log-heuristic|unknown`; removes the class; `executor_exclusion_degraded: true` on collision → T1+WARN.
- §9.3 telemetry restored (R2 H8 / §2.4): the 3 fields `executor_class_source`, `executor_class_resolved`, `executor_exclusion_degraded` RE-INSERTED as real telemetry.
- §11.3 grader assertion restored (R2 H9 / §2.5): `executor_model_class NOT IN reviewer_model_classes` asserted whenever `executor_class_resolved == true`.
- metrics.json restored (R2 H11(a)): `executor_class_resolved`, `executor_exclusion_degraded` re-added to ensemble block.
- `--executor-model` (R2 H1 / §2.1): the #197 "accepted-and-ignored, no class-exclude" input-resolution line is DELETED; master has NO such line. Master's only `--executor-model` mentions live in §7.1 rule prose where the flag drives exclusion.

**R3's CLI-cluster flip asserts (A-narrow, clauses 1–7 + L2170/L2276/L2389):**
- Clause 2: `executor_model_class` forwarded to `--executor-model`; reflect EXCLUDES that class. ✓ matches R2 §7.1.
- Clause 4: `--executor-model <class>` EXCLUDES the class; emits `executor_exclusion_degraded` if exclusion can't be honored. ✓ matches R2 §7.1 + §9.3 (`executor_exclusion_degraded` is a real restored field).
- Clause 5: `--cli` POST contract DOES emit `executor_class_resolved` and `executor_exclusion_degraded`. ✓ matches R2 H8 + H11(a) — both fields are restored as real telemetry/metrics. **R3's clause-5 CAVEAT (R3 L91) is RESOLVED by R2:** R3 explicitly warned "if master's contract does NOT emit these fields, soften clause 5" and "do not invent contract field names not confirmed by R2." R2 CONFIRMS these exact field names are restored. So R3 clause 5 may assert them as written — **no softening needed.** This is the key reconciliation: R3's worst-case branch (reflect stays instance-level → flip incoherent, R3 L191) does NOT obtain. R2 flips reflect to exclusion, so R3's "If R2 flips reflect to exclusion too → CLI cluster flip is coherent" branch (R3 L190) is the live one.

**VERDICT Q1: COHERENT.** R3's CLI POST cluster asserts only contract fields/behaviors that R2 actually restores. No clause asserts a field R2 leaves un-restored. The reconciliation R3 flagged HOLDS because R2's disposition is restore-to-exclusion, not retain-instance-level.

**MANDATORY tasklist encoding (not a contradiction, but a sequencing + truth dependency the tasklist must make explicit):**
1. The clause-5 field names (`executor_class_resolved`, `executor_exclusion_degraded`) are truthful ONLY because R2's H8 + H11(a) restores them. The tasklist MUST order R2's reflect-SKILL restore (Step 3) and R3's task-builder flip (Step 4) such that BOTH land, and SHOULD note in the Step-4 item that clause 5's field names depend on Step-3 H8/H11(a). If Step 3 were ever descoped, clause 5 would assert phantom fields. **Encode the dependency.**
2. Field-name exactness: R2 restores the literal tokens `executor_class_source`, `executor_class_resolved`, `executor_exclusion_degraded`. R3 clauses 4/5 use `executor_exclusion_degraded` and `executor_class_resolved` — exact-match. R3 clause 5 does NOT reference `executor_class_source` (R2's third field), which is fine (it is provenance, not a POST-contract emit the wrapper consumes). No mismatch.

### Q2 — "two families" boundary / A.10.7 PRE-gate left instance-level — A LIVE RESIDUAL TENSION the tasklist MUST surface (not a blocker, but NOT silent)

**R3's boundary claim:** Family A (CLI POST cluster: L2170, L2244–2252, L2276, L2382–2383, L2389) flips to exclusion; Family B (A.10.7 PRE gate L1668/L1678, skill-mode runner L2218/L2223–2224, Rule 20 L2371, validation checklist L2310) stays instance-level and "byte-for-byte untouched" (clause 7, R3 L40/L99). R3 recommends A-narrow.

**Cross-check against R2's reflect model — THIS IS WHERE THE TENSION IS REAL:**
R3's A-narrow rests on the premise (R3 L69, L189–191) that Family B is "governed by what the reflect skill actually does" and is correct as-is ONLY IF reflect stays instance-level. **But Q1 establishes that R2 flips reflect to executor-class EXCLUSION.** So:
- Family B text (e.g. R3 L64 quoting task-builder L1678: *"The skill no longer excludes any model class in any case; reviewer-panel independence is guaranteed at the instance level"*; L65 runner prompt L2223 *"the skill no longer excludes any model class from its reviewer panel… guarantees independence at the instance level"*; L66 Rule 20 L2371 *"the skill no longer excludes any model class"*) describes the reflect skill as NON-excluding / instance-level.
- After R2, the reflect skill DOES exclude (master executor-class exclusion restored). **So Family B's prose becomes factually STALE about the very skill R2 restored.** task-builder L1678/L2223/L2371 would assert "the skill no longer excludes any model class" about a skill that, post-R2, excludes by class.

**This is a genuine cross-file contradiction surface, NOT orthogonality.** R3 is internally consistent under ITS stated assumption (reflect stays instance-level), but that assumption is FALSIFIED by R2. A.10.7 is NOT genuinely orthogonal: it is a PRE gate (no executor has run, so no class to exclude at PRE — R3 L64/L178 is correct that the PRE-gate ACTION is unaffected), but its DESCRIPTIVE PROSE about the skill's general exclusion behavior ("the skill no longer excludes any model class **in any case**") is a blanket claim that R2 contradicts.

**Distinction the tasklist must make (the resolution):**
- A.10.7's *operational behavior* at PRE (do NOT pass `--executor-model`; no executor class exists at PRE) is genuinely orthogonal and correct regardless of R2 — leaving the PRE *action* untouched is fine.
- A.10.7's *descriptive justification clause* ("the skill no longer excludes any model class in any case; …guaranteed at the instance level") is FALSE post-R2 and, if left byte-for-byte, ships a self-contradiction: task-builder telling the reader the reflect skill is instance-level while the reflect skill it invokes is exclusion-model.

**VERDICT Q2: NOT a fatal contradiction, but R3's "A.10.7 byte-for-byte untouched" recommendation, taken literally, leaves stale instance-level prose that R2 contradicts.** The tasklist MUST resolve this explicitly rather than silently shipping A-narrow as if Family B were truly orthogonal. Two acceptable resolutions for the tasklist author (this is a `needs_human_decision` candidate):
1. **A-narrow-plus (minimal-truthful):** keep A.10.7's PRE *action* untouched, but reword ONLY the blanket "the skill no longer excludes any model class in any case" descriptive clauses in Family B (L1678, L2223–2224, L2371) so they do not assert a global instance-level property of a now-exclusion skill. This is slightly wider than R3's pure A-narrow but is the minimum needed to avoid shipping a stale claim. Note: this re-entangles the reflect-skill disposition R3 deliberately fenced off, so it IS scope-creep relative to R3's recommendation — flag for human decision.
2. **Accept-and-document:** keep byte-for-byte A-narrow (as R3 recommends) and explicitly log the residual stale-prose tension in the tasklist's Open Questions, accepting that Family B prose lags reflect's restored behavior. R3 itself flags this exact tension at L187–191 and says it "does not own this reconciliation."

Either way: **the contradiction R3 raised at L189–191 ("a CLI POST gate that forwards `--executor-model` to exclude a class would be handing an exclusion flag to a skill that 'no longer excludes any model class' — a live contradiction") is RESOLVED for the CLI cluster by R2 (reflect DOES exclude → forwarding is coherent), but the SAME sentence's instance-level prose survives in Family B.** The tasklist cannot treat A.10.7 as orthogonal without addressing the descriptive-clause staleness.

### Q3 — Validation-command / file-path agreement across R1, R2, R3, R4 — AGREE (one cross-file path-set check, no typos found)

**Target file paths — cross-checked for byte-identity across files:**
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — R1 line 61/82 (HUNK-SURGERY), R2 line 3 (target). **Identical.** ✓
- `src/superclaude/skills/task-builder/SKILL.md` — R1 line 64/83 (HUNK-SURGERY), R3 line 4 (target), R4 line 118 (test ref). **Identical.** ✓
- `src/superclaude/cli/reflect/runner.py` — R1 line 57/98 (DROP restore-master). R2/R3 do not touch it; R4 does not list it. No conflict. ✓
- `src/superclaude/skills/sc-reflect-protocol/refs/{reviewer-spec.md,reflection-rubric.md}` — R1 lines 62–63/110 (REJECT restore-master). R2 explicitly does NOT touch refs (R2 scope is SKILL.md only). **Consistent** — R1 owns the refs full-restore, R2 owns SKILL.md hunk-surgery; no overlap, no double-disposition. ✓
- `tests/cli/reflect/test_no_nesting_guard.py` — R1 line 69/98 (DROP restore-master), R4 line 110 (PRESENT, collected). **Consistent:** R1 restores it to master; R4 confirms it currently exists and is collectible. No path mismatch. ✓
- `tests/cli/reflect/test_inline_directive.py` — R1 line 68/104 (`git rm`, new-in-197), R4 line 110 (PRESENT). **Consistent:** R4 confirms the file exists now (so `git rm` has a target); R1 removes it. No conflict. ✓

**Critical anti-overlap check (R1 ↔ R2 HUNK-SURGERY guard):** R1 line 120 issues a HARD WARNING that the two HUNK-SURGERY files (sc-reflect-protocol/SKILL.md, task-builder/SKILL.md) MUST NOT appear in any `git checkout origin/master` one-liner. R2 line 13 independently issues the identical FORBIDDEN warning for sc-reflect-protocol/SKILL.md. **R1 and R2 AGREE — no file appears in both a restore command AND a surgery scope.** R1's two `git checkout origin/master --` one-liners (lines 98, 110) list exactly: runner.py, test_no_nesting_guard.py, reviewer-spec.md, reflection-rubric.md — and NONE of the two surgery targets. ✓ This is the single most dangerous cross-file overlap possibility and it is clean.

**Validation-command agreement:**
- R2 post-surgery greps (V1–V6, R2 §5) target `sc-reflect-protocol/SKILL.md`; R3 flip greps (R3 §TASK 6) target `task-builder/SKILL.md`. Disjoint targets, no command collision. ✓
- R4's `make verify-sync` (the user-mandated Step-4 validation, R4 line 92) is consistent with R3's recommendation to ALSO add a semantic grep (R3 line 149) — R3 explicitly says verify-sync "does NOT confirm the flip's semantic content," matching R4's note that verify-sync only checks src↔.claude parity. **No conflict; R3 ADDS to R4, does not contradict.** ✓
- R1's git commands (`git checkout origin/master --`, `git rm`), R4's git commands (`git rev-list`, `git push origin feat/rf-harness-sync`, `gh pr view/comment 197`) operate on disjoint surfaces. R1 line 22 and R4 line 129 both assert origin = IronbellyOrg/IronClaude fork. **Agree.** ✓
- **One syntax note R1 surfaces that the tasklist must honor (R1 line 113–115):** `--source=origin/master` form is INVALID git syntax; only the positional `<tree-ish> -- <paths>` form works. This does not conflict with any other file; it is a standalone correction the tasklist must embed. ✓

**VERDICT Q3: AGREE.** No path typos, no mismatched expectations, no double-disposition of any file across R1/R2/R3/R4. The restore/surgery boundary is clean.

### Q4 — `merge_method legal` grep footgun (R2) vs the user's stated step-3 validation command — CONFIRMED CONFLICT; tasklist MUST broaden the alternation

**R2's finding (R2 line 110, 126, 178, 184):** The literal substring `merge_method legal` does NOT appear verbatim in §9.2 of the reflect SKILL.md. §9.2 (branch L810) and the metrics.json mirror (L1738) say **"LEGAL VALUES ARE EXACTLY {adversarial, single-reviewer-fallback}"** — the token sequence is `merge_method:` … `LEGAL VALUES`, never the contiguous string `merge_method legal`. The only place the contiguous phrase `merge_method legal-values` appears is the REWORDED changelog line (R2 §4 draft, "EV-2 merge_method legal-values guard").

**Why this is a footgun:** R2's own draft V2 grep (R2 §5) initially writes `grep -n "ORCHESTRATOR-VERIFIES-ON-DISK\|merge_method legal\|merged-verdict.yaml"`. The middle alternative `merge_method legal` would FALSE-NEGATIVE against §9.2 (which has `LEGAL VALUES ARE EXACTLY`, not `merge_method legal`). R2 self-catches this at line 178/184 and recommends broadening to `ORCHESTRATOR-VERIFIES-ON-DISK\|LEGAL VALUES ARE EXACTLY\|merged-verdict.yaml`.

**Cross-check against the user's step-3 validation command (per the lens prompt: "the user's stated step-3 validation command"):** If the user's step-3 validation greps for the literal `merge_method legal` substring to confirm EV-2 retention, that grep WILL false-negative even though EV-2 IS correctly retained — because the on-disk text is `LEGAL VALUES ARE EXACTLY`, not `merge_method legal`. **This is a real conflict between the naive validation phrasing and the actual retained text.**

**VERDICT Q4: CONFLICT CONFIRMED.** The tasklist MUST NOT validate EV-2 retention with a bare `merge_method legal` grep. It must broaden the alternation to include the literal on-disk tokens: `LEGAL VALUES ARE EXACTLY` (the §9.2 + metrics.json EV-2 text) and/or `ORCHESTRATOR-VERIFIES-ON-DISK` (EV-1) and `merged-verdict.yaml`. Recommended exact alternation (from R2 line 178): `ORCHESTRATOR-VERIFIES-ON-DISK\|LEGAL VALUES ARE EXACTLY\|merged-verdict.yaml`. **This must be embedded verbatim in the step-3 validation item, otherwise a correct surgery reports FAIL.**

### Q5 — Counts reconciliation (R4 test-collection counts ↔ R1 18-file disposition) — RECONCILE (no cross-file count conflict)

**R4's test-collection counts (R4 §3):** `tests/cli/reflect` = 163 collected (line 109); `tests/swarm` = 2272 collected (line 113); `tests/skills/test_task_builder_merge.py` = 68 (line 119). These are TEST-SUITE collection counts (pytest `--co`), an orthogonal axis to file disposition.

**R1's 18-file disposition (R1 §"18-file name-status" + matrix):** 18 changed files between origin/master...HEAD; counts ACCEPT=11, DROP-restore=2, REJECT-restore=2, RM=1, HUNK-SURGERY=2, total=18 (R1 line 71, arithmetic verified: 11+2+2+1+2 = 18 ✓).

**Cross-reconciliation — the two count systems intersect at exactly 2 test files, and they agree:**
- R1's 18-file set includes exactly TWO `tests/cli/reflect/` files: `test_inline_directive.py` (RM) and `test_no_nesting_guard.py` (DROP restore). R4 line 110 independently confirms BOTH are PRESENT in `tests/cli/reflect/` right now. **No conflict:** R4's "163 collected" is the CURRENT branch collection (includes test_inline_directive.py's tests). After R1's `git rm test_inline_directive.py` + restore of test_no_nesting_guard.py to master, the 163 count WILL change — and that is expected, not a contradiction. **Tasklist note:** the post-surgery `tests/cli/reflect` collection count will NOT be 163 (test_inline_directive.py removed; test_no_nesting_guard.py reverted to master's version which may have a different test count). Any validation item that re-runs `uv run pytest tests/cli/reflect` must NOT assert "expect 163" as a post-merge gate — 163 is a pre-surgery baseline only. R4 line 109 reports it as a current collect, not a post-state target; this is consistent but the tasklist must not freeze 163 as an expected post-value.
- `tests/swarm` (2272) and `tests/skills/test_task_builder_merge.py` (68) touch NONE of R1's 18 files (no swarm or skills/test_task_builder file is in the diff). They are reference baselines only. R4 line 119 explicitly marks the 68-count as "reference only" since step-4 validation is `make verify-sync`. **No disposition-count interaction; no conflict.** ✓

**VERDICT Q5: RECONCILE.** R4's collection counts and R1's 18-file disposition operate on orthogonal axes and intersect cleanly at the 2 `tests/cli/reflect` files, where they agree (both present now; R1 disposes them). The ONLY tasklist caveat: 163 is a pre-surgery baseline, not a post-merge expected value — do not freeze it as a gate threshold.

---

## Compiled cross-file findings (severity-ranked)

### Critical (must be addressed before the tasklist is authored / executed)
- **CF-1 (Q2 — stale Family-B prose).** R3's literal "A.10.7 byte-for-byte untouched" A-narrow recommendation leaves Family-B descriptive prose ("the skill no longer excludes any model class in any case … guaranteed at the instance level"; task-builder L1678/L2223–2224/L2371) that R2's restore-to-exclusion FALSIFIES. The tasklist MUST either (a) reword the blanket descriptive clauses [A-narrow-plus, scope-creep flag → human decision] or (b) accept-and-document in Open Questions. It must NOT silently ship A-narrow as if A.10.7 were fully orthogonal — the PRE *action* is orthogonal, the PRE *justification prose* is not. **This is a `needs_human_decision` item per the project rule that human-decision items HALT rather than auto-default.**

### Important (must be embedded in tasklist items to avoid false gate results)
- **CF-2 (Q4 — merge_method grep footgun).** Step-3 EV-2 validation MUST use the broadened alternation `ORCHESTRATOR-VERIFIES-ON-DISK\|LEGAL VALUES ARE EXACTLY\|merged-verdict.yaml`, NOT a bare `merge_method legal` substring grep (which false-negatives against the actual on-disk `LEGAL VALUES ARE EXACTLY` text).
- **CF-3 (Q1 — R2→R3 field-name dependency).** R3 clause-5 field names (`executor_class_resolved`, `executor_exclusion_degraded`) are truthful ONLY because R2 H8/H11(a) restores them. Tasklist MUST sequence Step 3 (reflect restore) before/with Step 4 (task-builder flip) and note the dependency so clause 5 never asserts phantom fields.
- **CF-4 (Q5 — 163 is a baseline, not a gate).** Any post-surgery `pytest tests/cli/reflect` validation must NOT assert "expect 163 collected"; test_inline_directive.py is removed and test_no_nesting_guard.py is reverted, so the post-state count differs by design.

### Minor (correctness notes the tasklist should carry)
- **CF-5 (Q3).** Embed only the positional `git checkout <tree-ish> -- <paths>` form; the `--source=origin/master` form is invalid git syntax (R1 line 113–115).
- **CF-6 (Q3).** The two HUNK-SURGERY files (sc-reflect-protocol/SKILL.md, task-builder/SKILL.md) MUST NEVER appear in any `git checkout origin/master --` one-liner (R1 line 120 + R2 line 13 agree). Verified clean in R1's command set.

---

## Cross-file consistency summary

| Focus question | Verdict | Cross-file status |
|----------------|---------|-------------------|
| Q1 — R2/R3 exclusion-model coherence | COHERENT | R3 asserts only fields R2 restores; dependency must be sequenced |
| Q2 — two-families / A.10.7 orthogonality | TENSION (not fatal) | A.10.7 PRE *action* orthogonal; Family-B *prose* contradicts R2 → human decision |
| Q3 — validation-command / path agreement | AGREE | No typos; restore/surgery boundary clean; refs disposition non-overlapping |
| Q4 — merge_method grep footgun | CONFLICT | Broaden alternation; bare `merge_method legal` false-negatives |
| Q5 — counts reconciliation | RECONCILE | Orthogonal axes; agree at 2 test files; 163 is baseline not gate |

---

## VERDICT: FAIL

**Rationale:** Per the rf-analyst standard ("any gap regardless of severity = FAIL", and the project rule that `needs_human_decision` items must HALT rather than auto-default), the cross-validation surfaces ONE Critical unresolved cross-file contradiction (CF-1) plus two Important false-gate risks (CF-2, CF-3) that the tasklist must explicitly encode before it can be authored safely. None of these are research-quality defects — R1–R4 are individually thorough, evidence-backed, and mutually consistent on every path/count axis (Q3, Q5 PASS; Q1 COHERENT). The FAIL is specifically that the **A.10.7 Family-B stale-prose reconciliation (CF-1) is an unresolved human-decision item**, and the tasklist cannot silently default it.

**Structured contradiction list (the FAIL items):**
1. **CF-1 [CONTRADICTION, Critical, human-decision].** R3 A-narrow ("A.10.7 byte-for-byte untouched") vs R2 (reflect flipped to executor-class EXCLUSION): Family-B descriptive prose asserting the reflect skill "no longer excludes any model class in any case / instance-level" (task-builder L1678, L2223–2224, L2371) is FALSE once R2 restores exclusion. Resolution required: reword blanket clauses (A-narrow-plus, scope-creep) OR accept-and-document in Open Questions. MUST HALT for human decision; MUST NOT auto-default.
2. **CF-2 [VALIDATION CONFLICT, Important].** Bare `merge_method legal` grep (naive step-3 EV-2 check) vs actual on-disk text `LEGAL VALUES ARE EXACTLY` → false-negative. Resolution: broaden alternation to `ORCHESTRATOR-VERIFIES-ON-DISK\|LEGAL VALUES ARE EXACTLY\|merged-verdict.yaml`.
3. **CF-3 [SEQUENCING DEPENDENCY, Important].** R3 clause-5 field names depend on R2 H8/H11(a) restore. Resolution: order Step 3 before/with Step 4; annotate the dependency.

**What PASSES (for the assembler's confidence):** Q1 reflect-exclusion-model coherence (R3 asserts only what R2 restores), Q3 path/command agreement (zero typos, clean restore/surgery boundary), Q5 counts reconciliation. The research corpus is internally sound on every factual axis; the FAIL is about decision-resolution and validation-phrasing the tasklist must encode, not about defective research.

**Report path:** `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/tasks/to-do/TASK-RF-pr197-reduce-merge-20260628-205943/qa/analyst-cross-validation-report.md`
