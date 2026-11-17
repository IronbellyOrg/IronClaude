# Refactoring Plan: Merge into Base (Variant 1)

## Overview
- Base: Variant 1 (Proposal A, `adversarial/variant-1-original.md`, default model, default persona). Selected in `base-selection.md`: 0.9302 against 0.8611, margin 6.91%, no tiebreaker.
- Incorporating strengths from: Variant 2 (Proposal B, `adversarial/variant-2-original.md`), plus the repairs both advocates agreed in Round 2 (hybrids H-C04 from the Variant 1 advocate and H-C04B from the Variant 2 advocate).
- Planned changes: 27
- Risk level: Medium overall (1 High: change 22; 13 Medium; 13 Low)

**Merged file and form.** The merge executor writes `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/reflect-tier2-engine-composition/merged-output.md` (`OUT/merged-output.md`). It is the position paper for slot C-04 (`reflect-tier2-engine-composition`) in the form of the debate's hybrid (H-C04 / H-C04B). It keeps the base's structure (sections 0-8 of Proposal A) and edits it per this plan. Two sections are added: a new 3.6 (single-engine decision, change 9) and a new section 9 (open items, open sub-disputes, unaddressed invariants, change 27).

**Inputs.** Debate: 42 of 45 points agreed (93.33%), converged. Unresolved labels: C-007, C-009, C-018. Invariant probe: 17 UNADDRESSED findings, 0 HIGH, 15 MEDIUM, 2 LOW.

**Rules for the merge executor.**
1. Add nothing the debate did not conclude. Where the advocates still disagree, write both positions as a two-sided entry marked OPEN and pick neither (section "Open Sub-Disputes" below).
2. Every UNADDRESSED invariant stays an open item in the merged file (section "Unaddressed invariants"); none is resolved by the merge.
3. The base's tags `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, `[UNVERIFIED]` stay. Claims taken from the debate carry the debate's own tag: `[V]` (an advocate read the line in the debate) or `[L]` (taken from the diff-analysis ledger); the executor does not re-read them. Add one line for this to section 0 (change 1).
4. Skill, ref and script edits that the merged paper describes are made under `src/superclaude/...` then `make sync-dev` (INV-K); the paper never tells a reader to stage `.claude/` paths.
5. Provenance of late items. The Variant 2 advocate's Round 2 (`round2-advocate-B.md`) ran after the Variant 1 advocate's and carries items R-1..R-7 and E-1..E-8 that the Variant 1 advocate never answered. Where this plan integrates one of them and the scoring matrix does not record it as agreed (E-4 step 0 of the measurement order, E-5 Stage 5 deadline, E-7 JSON-in serializer input, E-2 `read_committed` wiring, R-4 disclosure wording, the T5-gate trigger prong), the merged file marks it "Variant 2 Round 2, not answered by Variant 1" and does not present it as agreed.

**Strengths to Incorporate (base-selection) mapped to changes.**

| # | Strength to incorporate (Variant 2 unless noted) | Change(s) |
|---|---|---|
| 1 | Staging evidence (U-010) and Stage 5 deadline (B's E-5) | 15, 9 |
| 2 | No capability moves now; production T5 PASS disclosed with corrected sentence (U-014) | 1, 10 |
| 3 | Seam probe extended (U-011, N3), also against engine A's scorer child | 24 |
| 4 | Single-engine trigger with decision rule, minus the M4 prong (U-012). Only the owner-answer prong is written as agreed; the M4 prong, the T5-gate prong and the Stage 5 deadline are carried in open sub-dispute 1b | 9 |
| 5 | Edit-fence accounting (X-007, U-015) | 20, 12 |
| 6 | Complete CV-8 document correction (V-18) | 13 |
| 7 | `--t2-engine` no new value (C-014); `reviewer_briefs_materialized` on three ref lines (C-015) | 14 |
| 8 | INV-L at three points with siblings first (E-1); `publish_files` refusal and unwired `read_committed` (E-2); helper-owned stage advance for three stages (E-3); re-measurement of prose fixes (E-4). Integrated as Position B of open sub-disputes 5 (INV-L shape) and 4 (stage scope), not as decisions; E-4 as a marked Variant 2 Round 2 item | 18, 7, 22 |
| 9 | Retirement test-mass accounting (U-016), I1 witness replacement (R-5), kernel free of swarm (U-017), open-items list (U-018, S-007) | 16, 25, 27 |

## Planned Changes
### Change 1: Restate the position as the hybrid, "code-owned write side behind a gated shell; no engine moves now" (from the debate hybrids H-C04 / H-C04B)
- **Source**: Variant 1 advocate Round 2 "Final Position" (H-C04, components D1-D7); Variant 2 advocate Round 2 "Final Position" (H-C04B); Variant 2 section 1 (no capability moves now).
- **Target**: Base section 1 (replace); section 0 (append one line mapping the debate tags `[V]` and `[L]`).
- **Rationale**: C-001 Hybrid, 95% (scoring matrix). X-001 and X-002 went to Variant 2 at 90%: the Variant 1 advocate conceded that `runner.py:540` routes production Tier 2 to `run_tier2_ensemble` (W1) and that "unskippable" holds only under a Python parent (W2).
- **Integration point**: Replace the paragraph. Keep "the shell is engine A's, the data is engine B's" only as a description of the write side. State: engine A, `contract.py`, `ensemble.py`, `runner.py`, `fallback.py`, the 36-test verdict map and the headless lane are unchanged; the write-side helpers are additive; judgment steps stay LLM work (keep the base's last sentences on what the LLM keeps). Delete "becomes a code step that the orchestrator calls" as a guarantee and the claim that composition drops no capability. Point to 3.4 (grounded lane deferred) and 3.6 (engine decision).
- **Risk**: Medium - replaces the headline that sections 3.4, 5 and 8 cite; those sections must agree with it (changes 8, 10, 26).

### Change 2: Scope the consistency section to what the code supports (from Variant 2 section 0)
- **Source**: Variant 2 section 0 (C-01 row note and the weaker reading of INV-020); Variant 1 section 2 (kept).
- **Target**: Base section 2, C-01 row and point (a) (append and replace); C-02 condition and the three C-03 dependencies stay verbatim.
- **Rationale**: S-006 Variant 1, 90% (keep the lettered reopen conditions U-001). X-005 Variant 2, 90%: no import exists in either direction (V-01), so "reflect stays on the v2 kernel" describes only the skill panel (engine B). C-018 is unresolved at 55% (labels only).
- **Integration point**: Append one sentence to the C-01 row: the sentence holds for the skill panel only; engine A imports nothing from `cli/review`. Rewrite point (a): the merged plan adds new files and edits no existing engine-A behaviour, so the weaker reading of "no change to `cli/reflect`" is enough. Record the C-018 label disagreement as open sub-dispute 1c (change 27), not as a choice.
- **Risk**: Low - a text correction; no design effect.

### Change 3: Add a per-module "blast radius" table (from Variant 2 section 2)
- **Source**: Variant 2 section 2 (table "Under Position B"); S-002.
- **Target**: Base section 3.1 (insert a second table after the "what is kept" table).
- **Rationale**: S-002 Hybrid, 90%: keep Variant 1's per-step table (change 4) and add Variant 2's per-module table; neither alone gives both views.
- **Integration point**: Rows for the shared core, `runner.py`, `ensemble.py` / `fallback.py` / `_diversity.py`, `contract.py` / `panel_lint.py` / `models.py`, the helper command module, `scripts/reflect_shadow_exit.py`, the SKILL and refs, the tasklist and task-builder skills. Drop two sentences of that table: "engine A's own meaning" for CV-5 and "Reuse, not new logic". The helper-module row states the placement as two-sided (change 6).
- **Risk**: Low - additive table.

### Change 4: Rewrite the per-step write-side table: steps 1, 5, 7, 10 plus parity at publish; no step-2 helper (from the debate, D2)
- **Source**: Variant 1 section 3.2 (base, edited); Variant 1 advocate Round 2 D2 (a)(b)(c)(e) and N2; Variant 2 advocate Round 2 verdict on D2.
- **Target**: Base section 3.2 (replace rows 2, 5, 7 and the "existing code" column; keep row 1 and the combined last row "8 kept-ids, 6 clustering" with corrected wording; the table has no separate row 6).
- **Rationale**: C-004 Hybrid, 90%. C-020 Neither, 95%: V-29 (existing extractors cover one of six `merged-verdict.yaml` fields) and N2 (`recompute_parity` is in `scripts/reflect_shadow_exit.py:117`, outside the wheel per `pyproject.toml:78-87`, and reads the finished contract at `:154-162`). A-003 REJECT, 90%, both advocates.
- **Integration point**: Row 1: resolve-and-freeze also builds `--snapshot` and `--root`. Row 2: delete the helper; parity is recomputed at publish from the card headers the code wrote and the contract it serialized, with `recompute_parity`, `PERSONAS`, `tele`, `card_headers`, `_json_map` moved from `scripts/` into `src/`. Row 5: a card writer copies `model:` from `resolution.json` (both advocates agree on this part). Which file it writes is not settled and stays an open item under INV-015: the Variant 1 advocate's D2(b) names the legacy `reviewer-<N>-card.*` names; the Variant 2 advocate's step 5 names `panel/cards/reviewer-<N>.md`, with any legacy-named output written as a sibling under `panel/` first (change 18, open sub-dispute 5). Row 7: the `merged-verdict.yaml` finalizer is new mapping code for 5 of 6 fields. The combined last row (kept-ids, clustering) is the existing CLI calls (`SKILL.md:345, :347`), not "called by the wrapper". Header "Existing code to reuse" becomes "Existing code reused / new code". INV-015 attaches (card writer target).
- **Risk**: Medium - new code with new tests; every reuse claim in the base is rewritten.

### Change 5: Serializer contract: validate and refuse, never filter (from the debate, D2(d))
- **Source**: Variant 1 advocate Round 2 W4 and D2(d); Variant 2 advocate Round 2 serializer verdict and E-7.
- **Target**: Base section 3.2, row 10 "publish and key-set" (replace "the two constants as allowlist").
- **Rationale**: A-001 REJECT, 90% (both advocates): `contract.py:306` reads `adversarial_subrun_status`, emitted at `ensemble.py:793`, and it is in neither frozen list (V-11); a filtering serializer would stop trigger 11a. E-7: the 3 unparseable recorded contracts cannot be replayed (`reflect_shadow_exit.py:74-79`).
- **Integration point**: The serializer writes YAML with quoted `[1m]` model aliases (both advocates), validates the key set and refuses on a foreign key. Its input is JSON composed by the orchestrator, and code owns syntax and key validity, not content: that is the Variant 2 advocate's E-7, Variant 2 Round 2, not answered by Variant 1, and is marked so. The lint is a publish gate for the skill-run lane only (X-008). The accepted key set is a two-sided entry (open sub-dispute 3). INV-005, INV-007 and INV-008 attach here.
- **Risk**: Medium - touches the keys the verdict map reads; the coverage pin (change 23) is the guard.

### Change 6: Helper placement and registration, two-sided (from the debate, D2 placement)
- **Source**: Variant 1 advocate Round 2 N1, N6 and D2 placement; Variant 2 advocate Round 2 R-2 and "D2 placement" verdict.
- **Target**: Base section 3.3, first two bullets (replace); the "cli/review stays free of reflect (C-01)" sentence moves into Position A of the entry.
- **Rationale**: C-002 Hybrid, 95% on the label only; the two Round 2 placements differ. N1 holds in part for both: `reflect_group`'s callback exits 0 under `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` (`commands.py:53-79`; marker exported at `runner.py:560, :606`), so a command under it is a silent no-op in a wrapper child. N6: the review package imports nine modules on load (`cli/review/__init__.py:19-36`).
- **Integration point**: Common ground first: not under `reflect_group`; the frozen constants in `panel_lint.py` are never copied; no `src/superclaude/...` path in skill text (INV-F); one lazy import edge; `make lint-architecture` Check 11 reserved names avoided. Then open sub-dispute 2 as a two-sided entry (A and B text from section "Open Sub-Disputes"). Do not pick.
- **Risk**: Medium - a wrong placement makes the helpers silent in the marker lane; pin (iii) in change 23 covers it.

### Change 7: Helper-owned stage advance, scope two-sided, with preconditions (from Variant 2 E-3 and the debate, D2)
- **Source**: Variant 1 advocate Round 2 D2 and W2; Variant 2 advocate Round 2 E-3 and "D2 stage ownership" verdict.
- **Target**: Base section 3.2 (append a column "who advances the stage") and section 3.3 (append one bullet).
- **Rationale**: C-004 Hybrid, 90%. X-002 Variant 2, 90%: `advance_stage` refuses an out-of-order stage (`manifest.py:302-306`), so a skipped helper is detected, not prevented (A's W2 narrowing). Re-advance with a different payload raises `Conflict` (`manifest.py:293-299`).
- **Integration point**: A helper that owns a stage advances it in-process with output hashes; the skill text stops telling the orchestrator to advance that stage. Preconditions: the skill edit sits inside `### 4.3a`; `test_the_skills_manifest_recipe_runs_as_written` is rewritten (`test_shadow_skill_contract.py:133-134`); the exit script counts a non-published run without a recorded fallback as a failure (`reflect_shadow_exit.py:221-223, :288-289`); an identical re-advance is a no-op. Optional: a hash-versus-file check in `manifest_cmd` (`manifest.py:285-291` checks only hash format). The skill-text change and the `Conflict` reason are in both advocates' texts; the recipe-test rewrite, the identical-re-advance check and the exit-script rule come from the Variant 2 advocate's E-3 and R-3 (Variant 2 Round 2, not answered by Variant 1) and are marked so. Scope is a two-sided entry (open sub-dispute 4). State "a skip is detectable if the kernel verifies output hashes" (the Variant 1 advocate's W2 narrowing), never "unskippable": today `advance_stage` checks only that `outputs` values look like hashes (`manifest.py:285-291`), so the orchestrator can still advance with an invented hash, and the hash-versus-file check in `manifest_cmd` is optional. INV-002, INV-006, INV-013, INV-017 attach here.
- **Risk**: Medium - edits skill text and a test; a wrong payload raises `Conflict` in a real run.

### Change 8: Replace the grounded lane through the wrapper with a deferral (base fix X-001)
- **Source**: Variant 1 advocate Round 2 W1 (conceded in full) and D3; Variant 2 sections 3.2 E6-E10.
- **Target**: Base section 3.4, first bullet "Grounded lane" (replace); section 3.1 row "Tier-2 branch" (append a note on `runner.py:546-572`).
- **Rationale**: X-001 Variant 2, 90%; C-003 Variant 2, 90%; C-022 Variant 2, 90%. `runner.py:538-545` sends standard and deep to the ensemble; `--depth` accepts only `standard|deep` (V-22); the else-branch child also carries the marker (`runner.py:560`) and the restricted profile (`process.py:145-154`).
- **Integration point**: Delete "reached through the skill or through the `ClaudeProcess` else-branch". Write: the grounded lane through the wrapper is not built (status DEFERRED); the read-only `reflect-reviewer` agents remain the skill panel's reviewers in UC-1 shadow; the preconditions and the decision are in 3.6. Keep the base's tool-list facts for `reflect-reviewer`.
- **Risk**: Low - removes an unsupported claim.

### Change 9: Add 3.6 "single-engine step": one decision with a fork and a Stage 5 deadline (from the debate, D3 + D7)
- **Source**: Variant 2 section 5 (trigger paragraph) and section 1 (Option 3); Variant 1 advocate Round 2 D3, D7; Variant 2 advocate Round 2 E-5, E-8, R-5 and D7 verdict.
- **Target**: Base new section 3.6 (insert after 3.5).
- **Rationale**: C-008 Hybrid, 90%. U-012 (High value). E-8: D3 and Option 3 share routing, M3-ext, the reviewer-count rule and exclusion, so the record carries one decision with a fork. C-009 is unresolved at 55%: the M4 prong and the default direction are open (sub-disputes 1b, 6).
- **Integration point**: Status NAMED, NOT SCHEDULED. Trigger written as agreed: the owner answers "the wrapper switches to engine B" (both advocates' D7). The other trigger prongs are not written into the decision; they are carried two-sided in open sub-dispute 1b: the Variant 1 advocate's repaired M4 prong; the Variant 2 advocate's "the T5 gate must report deviations" prong and the Stage 5 deadline "recorded before Stage 5 enables UC-2" (`SKILL.md:87, :311`, `ensemble.py:797`), the deadline being Variant 2 Round 2 (E-5), not answered by Variant 1. M4 as written is dropped by both advocates (N4, R-4). Fork on the owner's headless answer: Option 3 (retire engine A's reviewer path; the write-side code is reused unchanged) or D3 (grounded lane through the wrapper). Shared preconditions: routing switch before `runner.py:540`; M3-ext passes (change 24); one reviewer-count rule (kernel cap 3 `panel.py:71-73` against clamp [2,4] `config.py:335`); exclusion via `review panel resolve --hard-exclude-class` (`panel.py:508-519`) and slot C-09. Option 3 also needs a replacement for the I1 fan-out witness (both advocates raise the loss; the replacement named is the Variant 2 advocate's, R-5) and, as Variant 2 Round 2 (E-2) adds, `read_committed` wired before `parse_contract` (change 16). An M-B failure with mechanical presence is not a retirement trigger; it is an owner escalation for a Python parent (both advocates). The default direction before the owner answers is open sub-dispute 6. Open invariants: INV-010 attaches here (also change 16).
- **Risk**: Medium - records a decision path the owner has not chosen; wording must stay conditional.
### Change 10: Headless lane unchanged, with the corrected disclosure sentence (from Variant 2 section 2 and the debate, D5)
- **Source**: Variant 2 section 2 ("what this position leaves as it is"), E11; Variant 1 advocate Round 2 W5, W8, D5; Variant 2 advocate Round 2 R-4 and D5 verdict.
- **Target**: Base section 3.4, second and third bullets (the headless lane and "The lane is a runtime property ..."; replace, including the sentence "Both lanes end in the same serializer"); section 3.5 (append a disclosure bullet).
- **Rationale**: C-005 Variant 2, 95% (the Variant 1 advocate conceded W8: lens change unmeasured; X-008: the lint reads `panel/manifest.json`, `adversarial/merged-verdict.yaml`, `reviewer-cards/`, `audit.log` at `panel_lint.py:252-282`, which the headless lane does not write). C-007 is unresolved at 55% on the label (open sub-dispute 1a); the disclosure content is agreed, the exact sentence is the Variant 2 advocate's (R-4).
- **Integration point**: Delete the findings-v2 lens change, the headless lint gate and "moves it into one place where a lint can see it". State `ensemble.py`, `fallback.py`, `reflect_review.py` and the output layout unchanged. Disclose in SKILL section 9.2 and the tasklist skill: the production T5 PASS is a convergence-and-diversity result with no deviation audit; `--fix` stays dormant and `sc-tasklist-protocol/SKILL.md:1162` keeps passing it. Use the sentence "a tested deviation seam exists with no production producer" (`build_reflect_contract` takes the counts as parameters, `ensemble.py:722-749`; test `test_ensemble_stub_integration.py:474-531`), marked as the Variant 2 advocate's R-4 wording, Variant 2 Round 2, not answered by Variant 1 (the Variant 1 advocate's own text says the contract "hard-codes zero deviations"); `verification_ran: False` stays described as hard-coded (`:808-809`). Revisit the lens only at a measured proxy-worker block compliance of at least 0.704 / 0.867 [UNVERIFIED figures].
- **Risk**: Medium - edits SKILL 9.2 inside the fence; the wording must not imply a deviation audit.

### Change 11: CV-5 recorded as "acknowledged non-conforming, change deferred" with release conditions (from the debate, D4)
- **Source**: Variant 1 section 3.5 first bullet (base, reworded); Variant 1 advocate Round 2 W3 and D4; Variant 2 advocate Round 2 R-1.
- **Target**: Base section 3.5, first bullet (replace).
- **Rationale**: C-011 Hybrid, 90%; X-003 Hybrid, 95%; X-009 Variant 1, 90%. The wording follows decided row `synth-06:190`. The edit at `ensemble.py:773` would turn the I1 witness `test_ensemble_stub_integration.py:141-168` (PASS, exit 0, no disk merge) into DEGRADED (V-10).
- **Integration point**: `ensemble.py:773` and the I1 witness are not edited. Record: slug effect `null-convergence` becomes `single-reviewer-fallback`, exit 11 unchanged (`contract.py:291-300`, V-09); `LEGAL_MERGE_METHODS` has two values (`panel_lint.py:184`), so only disk confirmation conforms; the label has no verdict effect today (`contract.py:295`). Release conditions: (a) the stub lane writes a disk merged output, or the I1 witness is rewritten under an explicit decision that headless PASS is not credit-free; or (b) engine A's reviewer path is retired. The conditions are also written in SKILL 9.2 next to the sentence.
- **Risk**: Medium - keeps a known wrong label; the conditions keep the deferral from becoming permanent.

### Change 12: Do-now document and script fixes, D1 (from Variant 2 sections 1(i), 2 and the debate, D1)
- **Source**: Variant 2 section 2 (SKILL row, exit-script row); Variant 1 advocate Round 2 D1.
- **Target**: Base section 3.5, second bullet (replace the "reconciled to the code" sentence); add status DO NOW.
- **Rationale**: Decided rows CV-1, CV-2, CV-3, CV-9. C-016 and X-007 Variant 2, 90%: the lines sit outside the fence allow-list. Both advocates accept D1 unchanged.
- **Integration point**: List: CV-1 0.80 and CV-2 single-vendor degrade prose at `SKILL.md:703, :1317, :1480-1481, :1755`; CV-3 one diversity word; CV-9 `scripts/reflect_shadow_exit.py:313` (empty baseline is "no baseline"); the CV-6 and CV-8 lines come from changes 14 and 13; `:838-839` stay as residue inside frozen 9.1 with the reconciling statement in `### 9.2`. The Variant 2 advocate adds that D1 is followed by the arm-A re-measure (change 22 step 0) before any helper is built (E-4, D1 verdict; Variant 2 Round 2, not answered by Variant 1); the merged file marks it so. INV-009, INV-012, INV-015 attach here.
- **Risk**: Medium - edits skill text and a script; needs the widened fence (change 20).

### Change 13: Complete CV-8 document correction (from Variant 2 section 2 and the debate, X-004 / C-012)
- **Source**: Variant 2 section 2 (document row); Variant 1 advocate Round 2 W12; V-18.
- **Target**: Base section 3.5, fourth bullet "Executor exclusion" (replace the correction sentence; keep the per-lane mechanics as the later route).
- **Rationale**: C-012 Hybrid, 90%; X-004 Hybrid, 90%. Both lists were incomplete (V-18); the base corrects no document now (Variant 1 concession 8).
- **Integration point**: Correct now, to what the code does: `sc-tasklist-protocol/SKILL.md:1141, :1152, :1165, :1170, :1177` and `task-builder/SKILL.md:2389`; describe `task-builder/SKILL.md:2247` as what it says (the POST subprocess resolves to `sc-reflect-protocol`), not as an ensemble. Keep Variant 1's exclusion mechanics (kernel `panel.py:508-519`; headless `T2Model0N` pool needs a model-to-class map and slot C-09) as the route in 3.6.
- **Risk**: Low - text corrections to a stated, complete line list. INV-009 says the list may still be incomplete; it stays open.

### Change 14: `--t2-engine` gets no new value; `reviewer_briefs_materialized` on three ref lines (from Variant 2 sections 2 and 4)
- **Source**: Variant 2 section 2 (`--t2-engine` row) and section 4 INV-A row; V-16, V-30.
- **Target**: Base section 3.5, third bullet (replace); section 3.1 (append one row).
- **Rationale**: C-014 Variant 2, 90%; C-015 Variant 2, 90%. CV-6 is decided (the lint is the behaviour). The key sits on three ref lines, not one: `refs/reviewer-spec.md:51, :57, :78`. The kernel `ENGINES` accepts `panel` (`manifest.py:51`) while `SKILL.md:87` rejects it.
- **Integration point**: The ref is the side that changes, on all three lines; the serializer (change 5) cannot emit the key. `--t2-engine` stays a skill flag with no new value; `panel` stays rejected until its stage. The INV-A condition becomes "ref edit first".
- **Risk**: Low - three line edits plus a statement.

### Change 15: Add staging evidence rows (from Variant 2 section 3.1, U-010)
- **Source**: Variant 2 section 3.1, E1-E5; U-010.
- **Target**: Base section 4.1 (insert rows E9-E13 after E8; append `commands.py:254-257` to E1).
- **Rationale**: U-010 (High value); C-008 Hybrid, 90%. The Variant 1 advocate accepted it in Round 2.
- **Integration point**: Rows: engine A's contract is `mode: post` (`ensemble.py:797`); the skill panel is UC-1 shadow only, `panel` rejected (`SKILL.md:87`) and UC-2 ignored until Stage 5 (`SKILL.md:311`); the panel has never run as the authoritative engine; no consumer passes `--t2-engine`; Stages 3 and 4 run in the skill and never reach the wrapper, so the engine collision starts at Stage 5 (E-5). The rows carry the Variant 2 advocate's E-5 claim that the engine collision starts at Stage 5 with the mark "Variant 2 Round 2, not answered by Variant 1"; it is the evidence behind the deadline entry of open sub-dispute 1b (change 9).
- **Risk**: Low - additive rows.

### Change 16: Retirement accounting and preconditions (from Variant 2 section 3.5 and the debate, R-5, A-004, A-005)
- **Source**: Variant 2 section 3.5 E21 and E22; Variant 2 advocate Round 2 R-5 and E-2; Variant 1 advocate Round 2 W6.
- **Target**: Base section 4.1, row E7 (append); section 4.3 (append one bullet).
- **Rationale**: U-016. C-006 Not material, 90%. A-004 and A-005 QUALIFY, 90% (both advocates). R-5: retiring engine A loses the only offline proof that Tier 2 fans out.
- **Integration point**: Add: test mass 507 matches in 44 files (`test_ensemble_fallback_stub.py` 97, `test_ensemble_stub_integration.py` 58); the I1 witness `test_i1_positive_witness_real_fanout` (`:141-171`); certification states `fallback.py:49-82`. Name the replacement for the witness as the Variant 2 advocate proposes it (R-5, E-2; Variant 2 Round 2, not answered by Variant 1): a recorded-run replay of a `published` manifest read through `read_committed` (`manifest.py:176-186`; no production caller today). That the I1 witness needs a named replacement is common to both advocates (the Variant 1 advocate's objection to Option 3). Survivors: `derive_verdict` and its 36 tests, `reflect_verdict_replay.py`, the manifest CLI recipe, the mocked-`ClaudeProcess` suite. `isolate_reviewers` is flag-gated, "PINNED OFF" (`models.py:94-100`). The reviewer-count rule is a recorded precondition of 3.6. INV-010 attaches.
- **Risk**: Low - additive accounting.

### Change 17: Evidence limits: allowlist, in-repo readers, reuse claims, GQ-067 (from the debate, A-001 to A-003, C-010)
- **Source**: Variant 1 advocate Round 2 shared-assumption table; Variant 2 section 8 (GQ-067 / OQ-8); V-12, V-32.
- **Target**: Base section 4.3 (append bullets; rewrite the GQ-067 sentence).
- **Rationale**: A-001, A-002, A-003 REJECT, 90% (both advocates). C-010 Variant 1, 90% and X-006 Variant 1, 90%: GQ-067 is the readers question (`synth-10` Q-08), not the wrapper-switch question (research/06 gap 1).
- **Integration point**: Keep "an analysis, not an observation". Add: by the advocates' counts of `contract.get("...")` keys, exactly one key `derive_verdict` reads is outside both frozen lists (`adversarial_subrun_status`); the key counts differ (A 19, B 18) and neither counts the alias reads in `_make_result` (`contract.py:112-134`), so the "exactly one" is qualified and stays open under INV-008; readers of engine-A-only keys exist inside `src/superclaude` (`sc-tasklist-protocol/SKILL.md:1171, :1179`, `phase-template.md:191, :199`, `task/SKILL.md:580`; matched by search, lines not read in full); so GQ-067 needs an in-repo reader inventory as well as the outside answer before any 1.0-shaped key is dropped. Delete "valid under either answer" (Variant 1 advocate Round 2 W10). INV-008 attaches here (also changes 5, 23).
- **Risk**: Low - corrections of stated evidence.

### Change 18: Rewrite the INV-L row: common ground plus a two-sided shape (from Variant 2 E-1, E-2 and the debate, D2a)
- **Source**: Variant 1 advocate Round 2 D2a; Variant 2 advocate Round 2 E-1, E-2 and the D2a verdict; Variant 2 section 4 INV-L row.
- **Target**: Base section 5, INV-L row (replace).
- **Rationale**: S-004 Variant 1, 90% (keep the 14-row table). C-017 Hybrid, 90%. E-1 (Variant 2 Round 2, not answered by Variant 1; Position B of sub-dispute 5): the helpers' targets split by authority; D2a and a "clean exit on 20 runs" cannot both hold unless the measure compares siblings. E-2: the kernel refuses `publish_files` in shadow (`manifest.py:496-500`) and `read_committed` has no production caller.
- **Integration point**: Keep "Endangered, HIGH". Written as common ground: helper output is a comparison artifact, not the authoritative file, until promotion; promotion is a separate decision after M-A and M-B pass and `reflect_verdict_replay.py` shows 0 verdict differences. The shape is not written as a decision. Position A (D2a): one comparison artifact `panel/contract.code.yaml` plus sibling files under `panel/`. Position B (E-1): three endangered points (`reviewer-cards/reviewer-<N>-card.*`, `adversarial/merged-verdict.yaml`, `return-contract.yaml`), each with a comparison sibling under `panel/` first. The owner question on how INV-L reads is open too (open sub-dispute 5, copied as written). INV-001, INV-014, INV-019 attach here.
- **Risk**: Medium - rewrites the highest-rated invariant row.

### Change 19: Correct the INV-A, INV-B, INV-I and INV-M rows (base fixes V-10, V-11, X-008, and the deferred headless finalizer)
- **Source**: Variant 1 advocate Round 2 W3, W4, W5 and "What I concede to V2" (headless finalizer deferred); Variant 2 section 4.
- **Target**: Base section 5, rows INV-A, INV-B, INV-I, INV-M (replace).
- **Rationale**: X-003 / V-10: the base rated the CV-5 pin collision MEDIUM and called the pins "[UNVERIFIED]"; its own advocate re-rated it HIGH. V-11: the allowlist wording. X-008: "headless output directories Preserved" contradicts the base's M4.
- **Integration point**: INV-A: "validates and refuses"; the condition is "ref edit first" (change 14); name `adversarial_subrun_status`. INV-B: preserved for the map and the 36 tests; the CV-5 edit is deferred (change 11); delete the "narrow effect" sentence and state the I1 witness collision, HIGH if the edit were made. INV-I: the base's "Preserved and extended" (a code finalizer that cannot write a lint-clean contract makes the run BLOCKED) no longer has an object while the headless finalizer is deferred (the Variant 1 advocate's Round 2 concession; changes 10, 26); write "Preserved"; the fail-closed property holds only where a Python parent exists, and it returns with a headless finalizer. INV-M: Preserved, now true because the headless layout and lens do not change (change 10).
- **Risk**: Medium - four invariant rows change rating text or condition.

### Change 20: Rewrite INV-K and the edit-fence accounting (from Variant 2 section 4, X-007, U-015)
- **Source**: Variant 2 section 4 (INV-A and INV-K rows); Variant 1 advocate Round 2 W11; V-15.
- **Target**: Base section 5, INV-K row (replace); section 3.5 skill-text bullet (append).
- **Rationale**: X-007 Variant 2, 90%; C-016 Variant 2, 90%. The allow-list at `test_shadow_skill_contract.py:65` covers only `### 3.1, ### 4.3a, ### 5.4, ### 9.2`; 9.1 is frozen (`:42-49`); `:703` is under `## 8`, `:1317` under `## 12`, `:1480-1481` under `## 14` (V-15); `:838-839` are inside 9.1 and only `:839` carries a comment.
- **Integration point**: Replace "edits stay under `### 4.3a`" with: the allow-list is widened in the same change for the `## 8`, `## 12`, `## 14` lines; `:838-839` are recorded residue with the reconciling statement in `### 9.2`. Keep the base's arch_lint finding; add the `test_no_new_src_superclaude_hit_in_the_skill_directory` note (`test_shadow_skill_contract.py:78-98`) from Variant 2's INV-K row, which the base row lacks (the base cites that test only in 3.3). INV-016 attaches.
- **Risk**: Medium - widening a fence test is a rule change; it must be done in the same change as the edits.
### Change 21: Add invariant rows for the recursion marker and the import chain (from the debate, N1 and N6)
- **Source**: Variant 1 advocate Round 2 N1, N6; Variant 2 advocate Round 2 verification table (both "HOLDS IN PART").
- **Target**: Base section 5 table (insert two rows after INV-N).
- **Rationale**: S-004 Variant 1, 90%, with the agreed note "add the INV-K row correction and the marker (N1) and import-chain (N6) rows". INV-004 (ADDRESSED) already rates both as covered by pins.
- **Integration point**: Row "recursion marker does not silence the new commands": Preserved only if the commands are not under `reflect_group` (`commands.py:53-79`), pinned by pin (iii). Row "import chain": the import-direction pin is two-sided (open sub-dispute 2: A's pin that `import superclaude.cli.reflect.runner` does not load `superclaude.cli.review`; B's pin, reversed, that `import superclaude.cli.review` does not load `superclaude.cli.reflect` at module load).
- **Risk**: Low - additive rows.

### Change 22: Restructure section 6 into the ordered measurement sequence (from the debate, D6)
- **Source**: Variant 1 section 6 (M1-M5, base); Variant 2 section 5 (counts-for and counts-against table); Variant 1 advocate Round 2 D6 and W9; Variant 2 advocate Round 2 E-1, E-4, E-7, R-3, R-4 and the D6 verdict.
- **Target**: Base section 6 (restructure): old M1 (pins) folds into step 2; old M2 is narrowed into step 1; old M3 (completeness) folds into step 3; old M4 (the stub-lane serializer and lint gate) is removed with the headless lint gate (change 10; W5, X-008), the engine-A pins staying untouched (change 23); old M5 (quality, a stated non-claim) is kept. Variant 2's M4 (seeded regressions) is a different item, treated in step 5.
- **Rationale**: C-019 Hybrid, 90%; S-005 Hybrid, 90%. E-4 (Variant 2 Round 2, not answered by Variant 1): the 13 recorded pilot runs straddle commits `9874d63fb` and `c2e3347d3` (directory modification times 2026-11-11 to 2026-11-13), while the 15 combo runs carry the stamp `20261107` and predate both; no file separates pre-fix from post-fix runs. R-3: the exit script drops non-published runs (`reflect_shadow_exit.py:209, :221-223`). All run counts stay unchecked (V-34).
- **Integration point**: Order: (0) arm A, marked Variant 2 Round 2 (E-4), not answered by Variant 1 and absent from the C-019 matrix label: exit script on existing runs and at least 20 fresh `--t2-engine shadow` runs after D1 only, no helper; the Variant 2 advocate reads a pass as "D2's Stage 2 value is small and helpers are justified by Stage 3", the merged file records that as his reading; (1) M-A offline replay, narrowed (both advocates): serializer on the 25 parseable recorded contracts (the 3 unparseable are covered by construction, E-7), the `merged-verdict` finalizer, the card writer only where raw reviewer output survived; pass = lint-clean, the stable-or-telemetry verdict-read keys plus `adversarial_subrun_status` value-equal where the orchestrator's contract was valid (the Variant 1 advocate counts 18 plus 1, the Variant 2 advocate 18 in all, and neither counts the alias reads in `_make_result`: the set is open under INV-008), then 0 verdict differences from `reflect_verdict_replay.py`; (2) pins (change 23); (3) M-B: at least 20 fresh `--t2-engine shadow` runs under the exit rule, presence read from code-written artifacts (manifest `outputs`, not `audit.log`), a non-published run without a recorded fallback counts as a failure, UC-1 only; only the EV-1 rate has the 3/39 = 0.077 tolerance (`reflect_shadow_exit.py:307-314`). The arms of M-B follow open sub-dispute 5: Position A (D2a, the Variant 1 advocate's M-B) applies the exit rule to the 20 fresh runs with the code-built output kept as a comparison artifact; Position B (E-1) makes it a comparison (legacy files as the baseline arm, code-built siblings as the helper arm, 20 of 20 clean); (4) M3-ext (change 24); (5) Variant 2's M4 as written is dropped by both advocates (N4, R-4); its repaired form and the trigger prong built on it are open sub-dispute 1b. Each step gets counts-for, counts-against and a decision rule. INV-003, INV-007, INV-011, INV-013, INV-014 attach here.
- **Risk**: High - restructures a whole section; five ordered steps depend on three open sub-disputes and four open invariants.

### Change 23: Add the four pins and the recipe-test rewrite (from the debate, N6 and D6 step 2)
- **Source**: Variant 1 advocate Round 2 N6 and D6 step 2; Variant 2 advocate Round 2 pins verdict.
- **Target**: Base section 6 (insert under step 2 of change 22).
- **Rationale**: N6 (accepted by both): nothing pins that the serializer's accepted set covers every key `derive_verdict` reads; B re-ran the check: 18 distinct `contract.get("...")` keys in `contract.py`, exactly one not in `panel_lint.py` (A counts 18 in the lists plus 1 outside, 19 in all; the count is open under INV-008).
- **Integration point**: (i) source-contract test: every key `derive_verdict` reads, including `_LOAD_BEARING_BOOL_FIELDS`, is in the serializer's verdict-read set (style of `test_marker_suppression.py:112-139`); (ii) the import-direction pin, two-sided; (iii) a helper run with `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` still executes and exits non-zero on bad input; (iv) a unit test of the moved parity function against the recorded runs now covered by `test_shadow_exit_script.py`; plus the rewritten recipe test and "identical re-advance is a no-op". Existing pins stay green untouched: the 36 verdict-map tests, the I1 witness, `test_panel_contract_lint.py:97, :107`, `test_shadow_skill_contract.py` with the widened allow-list. INV-008 attaches (alias reads in `_make_result`).
- **Risk**: Low - additive tests.

### Change 24: Replace M3 with M3-ext, the extended seam probe (from Variant 2 M3 and the debate, N3)
- **Source**: Variant 2 section 5 (M3, U-011); Variant 1 advocate Round 2 N3; Variant 2 advocate Round 2 N3 verdict.
- **Target**: Base section 6 (insert as step 4 of change 22; the base's old M3 "completeness" folds into step 3, as change 22 states).
- **Rationale**: C-022 Variant 2, 90%. Under `reviewer_profile=True` the child drops the permission-skip flag and `--tools default` (`process.py:145-154`); the production adversarial scorer is itself such a child and must write `adversarial/return-contract.yaml` (`ensemble.py:537-553`), so the write question is not specific to the grounded lane.
- **Integration point**: Probe with the marker set and `reviewer_profile=True`: agent calls complete, artifacts exist on disk, a `review` command is not suppressed. Run it also against engine A's own scorer child (the Variant 2 advocate's addition, N3 verdict; Variant 2 Round 2, not answered by Variant 1; marked so). State each outcome in advance: a spawning child weakens the "no verified seam" claim; a non-spawning child leaves only text-only reviewers for a shell design. It gates D3 and Option 3 (3.6) only.
- **Risk**: Low - a probe with stated outcomes; changes no code.

### Change 25: Update the PR and rf-qa effects section (from Variant 2 section 6)
- **Source**: Variant 2 section 6; Variant 1 advocate Round 2 W1, W9; V-03.
- **Target**: Base section 7: the `--fix` bullet (replace), the M13 bullet and the M10/M11 bullet (append).
- **Rationale**: C-007 unresolved at 55% (label only). C-021 Not material, 90% (V-03: the substance holds). U-017 (Low).
- **Integration point**: Replace "A makes a dormant path live" with: `--fix` stays dormant and no change here moves it; the grounded lane is the only mechanism that could supply deviation classes and is deferred (3.6). M13: the M-A replay corpus is reflect-shaped. Add: the kernel stays free of `cli/swarm`; swarm is imported by `ensemble.py`, `fallback.py` and `_diversity.py:5` (V-03), not only `ensemble.py`. State that the helpers' generality for PR review is not verified.
- **Risk**: Low - text edits.

### Change 26: Correct the strongest-objection answers (base fixes X-002, V-29)
- **Source**: Variant 1 advocate Round 2 W2, W7; Variant 2 section 7 answers 3 and 4.
- **Target**: Base section 8, answers 1, 2 and 4 (replace); answers 3 and 5 stay.
- **Rationale**: X-002 Variant 2, 90%. C-020 Neither, 95%: "write side only" (Variant 1) and "reuse, not new logic" (Variant 2) both overstate.
- **Integration point**: Answer 1: drop "the only option in which no capability on that list is dropped"; no capability moves now, so none is dropped, and the engine choice is the named later step (3.6). Answer 2: replace "The new code is the write side only. The readers exist" with the corrected claim (extractors cover one of six fields; `recompute_parity` is in `scripts/`; the finalizer and the moved parity function are new code with new tests). Answer 4: fail-closed holds only where a Python parent exists (headless lane; its finalizer is deferred); in the skill-run lane a skipped helper is detectable through manifest state if the kernel verifies output hashes (otherwise the orchestrator can advance with an invented hash, `manifest.py:285-291`) and through the exit rule, not prevented, and M-B measures it (INV-017 open).
- **Risk**: Medium - rewrites three of five answers to the base's central objection.

### Change 27: Add section 9: open items, open sub-disputes, unaddressed invariants (from Variant 2 section 8, U-018, S-007)
- **Source**: Variant 2 section 8; debate Convergence Assessment; `invariant-probe.md`; sections "Open Sub-Disputes" and "Unaddressed invariants" of this plan.
- **Target**: Base new section 9 (insert after section 8): 9.1 open items, 9.2 open sub-disputes (two-sided), 9.3 unaddressed invariants.
- **Rationale**: S-007 Variant 2, 90%. U-018 (Low). Invariant gate: 15 MEDIUM and 2 LOW UNADDRESSED are warnings, not blocking; they travel with the merged file as open items.
- **Integration point**: 9.1: GQ-067 (readers, change 17); OQ-20 (`refs/reflection-rubric.md:39` Aligned/Refinement/Drift/Regression against SKILL section 10; 5 against 6 calibrator dimensions); RE-4 carried [UNVERIFIED]; E9 closed only by M3-ext; the INV-L wording; the owner's headless answer; run counts unchecked (V-34). 9.2: the six entries below, copied as written. 9.3: the 17-row table below, each marked OPEN.
- **Risk**: Low - an additive section.

## Base Weaknesses to Fix
Each defect below was verified in the debate against code and conceded by the Variant 1 advocate (Round 2 response numbers W1-W12, or its Round 2 table entry for the point), except where marked (the INV-L row is the one marked "not conceded").

| Issue in Variant 1 | Debate evidence | Better variant | Fix approach | Change |
|---|---|---|---|---|
| Grounded lane "reached through the `ClaudeProcess` else-branch" has no routing (section 3.4) | X-001 and C-003, Variant 2, 90%; W1 conceded in full; `runner.py:538-545`, V-07 | Variant 2 (E6-E10) | Delete as a present design; status DEFERRED with preconditions in 3.6 | 8, 9 |
| "Unskippable" and "becomes a code step the orchestrator calls" (sections 1, 3.3, 8 answer 4) | X-002, Variant 2, 90%; W2 conceded: fail-closed only under a Python parent (`runner.py:573-580`) | Variant 2 (M1 helper-presence; section 7 answer 4) | Say "detectable if the kernel verifies output hashes"; scope fail-closed to the headless lane; measure presence in M-B | 1, 7, 26 |
| CV-5 pin collision rated MEDIUM, pins "[UNVERIFIED]" (INV-B, 3.5, M4) | X-003 / V-10, Hybrid, 95%; W3 conceded, re-rated HIGH; `test_ensemble_stub_integration.py:141-168` | Hybrid (Variant 2's "do not edit now", Variant 1's wording) | Record "acknowledged non-conforming, change deferred" with release conditions | 11, 19 |
| Allowlist wording drops `adversarial_subrun_status` (3.2 step 10, INV-A) | V-11; A-001 REJECT, 90%; W4 conceded; `contract.py:306`, `ensemble.py:793` | Neither original; the hybrid repairs it | Validate and refuse, never filter; pin the verdict-read set | 5, 19, 23 |
| Lint layout against headless layout (INV-M, M4) | X-008, Variant 2, 90%; W5 conceded; `panel_lint.py:252-282`, V-28 | Variant 2 | No lint gate on the headless lane; headless layout unchanged | 10, 19, 22 |
| INV-K row says edits stay under `### 4.3a` | X-007, Variant 2, 90%; W11 conceded; `test_shadow_skill_contract.py:65`, V-15 | Variant 2 | Widen the allow-list in the same change; `:838-839` recorded residue | 20 |
| "Write side only" and parity "reuse" overstated (3.2 row 2, section 8 answer 2) | C-020 Neither, 95%; V-29; N2; W7 conceded | Neither (correct claim is in the hybrid) | Corrected claim; parity at publish with the function moved into `src/` | 4, 26 |
| Headless lens change meets unmeasured compliance (3.4) | C-005, Variant 2, 95%; W8 conceded | Variant 2 | Remove the lens change; revisit on a measured block compliance | 10 |
| No trigger for a later single-engine step | C-009, unresolved 55%; W10 conceded | Variant 2 (U-012) | Add 3.6 with trigger and Stage 5 deadline; M4 prong stays open | 9 |
| Base corrects no document now | X-004, Hybrid, 90%; Variant 1 concession 8; V-18 | Variant 2 | Complete CV-8 list corrected now | 13 |
| Reviewer-count rules not reconciled (engine A [2,4] against kernel cap 3) | A-004 QUALIFY, 90%; W6 (right in substance); `config.py:335`, `panel.py:71-73` | Neither | Recorded precondition of 3.6 | 9, 16 |
| Headless PASS-eligibility declined, so headless PASS still rests on constants | C-005 / U-005; Variant 1 concession 9 | Variant 2 (disclosure) | Disclose with the corrected sentence; finalizer deferred | 10 |
| M2 assumes every recorded run is replayable | W9 half conceded: card-writer inputs may not exist; 3 contracts unparseable (E-7) | Hybrid | Narrow M-A | 22 |
| Helper registered where the recursion marker silences it (3.3 "exposed as `superclaude` subcommands") | New evidence N1, both advocates (HOLDS IN PART) | Neither original | Placement entry, two-sided; pin (iii) | 6, 21, 23 |
| 4.3 and E4: GQ-067 needs only an outside answer; "valid under either answer" | A-002 REJECT, 90% (both advocates); V-12; W10 conceded | Neither original | In-repo reader inventory added to the GQ-067 sentence; "valid under either answer" deleted | 17 |
| E7 lists "snapshot-grounded children" as a capability lost on retirement | A-005 QUALIFY, 90% (both advocates); `models.py:94-100` "PINNED OFF" | Neither original | Carry the snapshot as a flag-gated option in the loss list | 16 |
| Section 2 C-01 row: "reflect stays on the v2 kernel" | X-005 Variant 2, 90%; V-01 (no import either way) | Variant 2 | Scope the sentence to the skill panel | 2 |
| Section 3.5 / INV-A: `--t2-engine` silent; the `reviewer_briefs_materialized` conflict left "open" | C-014, C-015 Variant 2, 90%; CV-6 decided; V-16, V-30 | Variant 2 | No new `--t2-engine` value; ref edit first on three lines | 14, 19 |
| Section 7: "A makes a dormant path live" and section 8 answer 1 ("only option in which no capability is dropped") | W1 conceded in full (grounded lane deferred); C-001 Hybrid, 95%; C-007 open label | Variant 2 (disclosure) | `--fix` stays dormant; no capability moves now | 25, 26 |
| INV-I row "Preserved and extended" (a headless finalizer fails the run closed) | The Variant 1 advocate's Round 2 concession: the headless finalizer is deferred and has no object | Variant 2 | Row written as "Preserved"; the extension returns with a headless finalizer | 19 |
| INV-L row names one artifact (the contract) as the change of writer | Not conceded: the Variant 2 advocate's E-1 (three points) is Position B of open sub-dispute 5 | Open | Row rewritten as common ground plus a two-sided shape | 18 |

## Changes NOT Being Made (with rationale)
| Diff Point | Approach not taken | Rationale for not making the change |
|------------|--------------------|-------------------------------------|
| X-001, C-003 | Variant 1 section 3.4: the grounded lane through the `ClaudeProcess` else-branch as a present design | No routing exists (`runner.py:538-545`; `--depth` is `standard|deep`, V-22); the child would also get the marker (`runner.py:560`) and the restricted profile (`process.py:145-154`). The Variant 1 advocate conceded in full (W1). Kept only as the deferred option in 3.6. |
| C-005, X-008 | Variant 1 sections 3.4, 6 (M4): a headless lens change to findings-v2 and a lint gate on the headless contract | The lint reads `panel/manifest.json`, `adversarial/merged-verdict.yaml`, `reviewer-cards/`, `audit.log`, none of which the headless lane writes (V-28); proxy-worker block compliance is unmeasured; consolidating the constants edits `ensemble.py` for no verdict gain. Variant 2, 95%. |
| C-011, X-003 | Variant 1 section 3.5: edit `ensemble.py:773` so `merge_method: adversarial` follows a disk-confirmed merge | The edit turns the credit-free PASS witness (`test_ensemble_stub_integration.py:141-168`) into DEGRADED (V-10). Hybrid, 90%/95%: the wording is kept, the edit is deferred (change 11). |
| (step 2) N2 | Both variants: a step-2 parity helper (Variant 1 row 2 "computed and recorded by code"; Variant 2 "parity record computed by code, reuse") | At step 2 no contract exists (`SKILL.md:341`, contract written at step 10); `recompute_parity` is outside the wheel and reads the finished contract (`reflect_shadow_exit.py:154-162`). Both advocates dropped it. Parity is recomputed at publish (change 4). |
| X-003, X-009 | Variant 2 section 2: CV-5 resolved as "engine A's own meaning" | Reverses decided row `synth-06:190` and contradicts Variant 2's own section 1(i). Conceded by the Variant 2 advocate (R-1). |
| N4, R-4 | Variant 2 M4 as written (false-PASS rate on seeded regressions) and the trigger prong built on it | Engine A's reviewers see the tasklist body and a header, never the diff (`ensemble.py:604-630`), so the outcome is fixed by construction. Conceded (R-4). A repaired form is the Variant 1 advocate's side of sub-dispute 1b. |
| R-3 | Variant 2 M1: helper presence read from `audit.log` | `audit.log` is one of the legacy-written files (`manifest.py:54`; `SKILL.md:349`), so the orchestrator would be measured by the orchestrator. Conceded (R-3). |
| N5, R-3 | The reading that one skipped helper in 20 runs passes the exit gate (the "1/20 tolerance") | True only for the EV-1 class (`reflect_shadow_exit.py:307-314`, 3/39 = 0.077); parity, lint, leaked keys and malformed rows are zero tolerance (`:290-335`). Narrowed to the step-7 helper (change 22). |
| N1, C-002 | Helpers under `reflect_group` (Variant 1 section 3.3; Variant 2 Round 1 hybrid) | The group callback exits 0 under the marker (`commands.py:53-79`); both advocates dropped it (R-2). Root registration as a settled primary is also not recorded: it is Position A of open sub-dispute 2, and `cli/review/<name>_cmd.py` is Position B. |
| C-020 | "Reuse, not new logic" (Variant 2 section 2, E17) and "The new code is the write side only" (Variant 1 section 8, answer 2) | Neither, 95%: extractors cover one of six `merged-verdict` fields (V-29); `recompute_parity` is in `scripts/` (N2). Replaced by the corrected claim (changes 4, 26). |
| R-4 | Variant 2 E11 wording "engine A hard-codes zero deviations" | `build_reflect_contract` takes the counts as parameters (`ensemble.py:722-749`; `test_ensemble_stub_integration.py:474-531`); the production scorer never supplies them. The disclosure uses "tested seam, no production producer" (change 10). This is the Variant 2 advocate's own correction (R-4); the Variant 1 advocate's text (N4, base 3.4) still says "hard-codes" and did not respond, so the plan marks the new wording as Variant 2 Round 2 and does not call it agreed. |
| C-005, W8 | Variant 1 Strength 6: a headless finalizer that fails closed | With the headless lane unchanged it has no object. It returns when the write-side helpers are proven and the owner wants the headless contract on 1.8.0 (Variant 1 advocate's Round 2 concession). |
| C-008, R-5 | Option 3 (retire engine A's reviewer path) as an unconditional direction | Both advocates make it conditional on the owner's headless answer; whether Option 3 is also the default before that answer is open sub-dispute 6. |

## Open Sub-Disputes Carried as Two-Sided Entries
The merged file writes each entry below as two-sided and marked OPEN, in section 9.2. "Position A" is the Variant 1 advocate's Round 2 position; "Position B" is the Variant 2 advocate's. The merge picks neither. The agreed parts of each entry are the only text written without a side.

### Sub-dispute 1: unresolved labels (C-007, C-009, C-018; 55% each in the scoring matrix)

| Point | Position A | Position B | What the merged file carries |
|---|---|---|---|
| 1a. C-007 (disclose the production T5 PASS; what changes it) | Hybrid: disclose now; the grounded lane is the only mechanism that could change it and is gated on M3-ext; M4 as written cannot test it (N4) | Variant 2: disclose with the sentence "tested seam, no production producer"; the grounded lane is the only mechanism that could change it and is deferred | The agreed disclosure content (the production T5 PASS is a convergence-and-diversity result with no deviation audit; `--fix` stays dormant; the grounded lane is the only mechanism that could change it and is deferred) (changes 10, 25). The wording "a tested deviation seam exists with no production producer" is the Variant 2 advocate's (R-4, Variant 2 Round 2, not answered by Variant 1), carried with that mark. The label difference is recorded; no text depends on it. |
| 1b. C-009 (a stated trigger for the single-engine step) | Variant 2: adopt the trigger "owner answer, or M4 shows a gate failure"; M4 repaired per N4 (state the known outcome for diff-borne regressions, or measure tasklist-versus-spec defects engine A can see) | Hybrid: keep a stated trigger, "the owner answers that the wrapper switches to engine B or that the T5 gate must report deviations"; drop the M4 prong because M4 is vacuous (N4); add the deadline "recorded before Stage 5 enables UC-2" (E-5) | The owner-answer prong only, as agreed (change 9). The M4 prong (A keeps it repaired, B drops it), the T5-gate prong (B only) and the Stage 5 deadline (B only, E-5, not answered by A) are carried as open items. |
| 1c. C-018 (consistency with C-01/C-02/C-03) | Hybrid: take Variant 1's reopen conditions and Variant 2's note that engine A imports nothing from `cli/review` (V-01); additive files need only the weak reading | Variant 2: only the weak reading of "no change to `cli/reflect`" is needed; the C-01 record has no import-direction rule (`ADJUDICATION-RESULT.md:12`) | The reopen conditions, the V-01 note and the weak reading (change 2). The label difference is recorded. |

### Sub-dispute 2: placement of the helper code

- **Common ground**: not under `reflect_group` (N1); frozen constants stay in `panel_lint.py`, never copied; `cli.review` / `cli.reflect` imported lazily inside functions; skill text names commands, not `src/superclaude/...` paths.
- **Position A**: code in `src/superclaude/cli/reflect/` next to `panel_lint.py`; the click commands are registered onto `review_group` at the `cli/main.py` composition root (`cli/main.py:559-570`), which already imports both groups. A module inside `cli/review/` that imports `panel_lint` would create the review-to-reflect edge that C-01 forbids. Pin: `import superclaude.cli.reflect.runner` does not load `superclaude.cli.review`.
- **Position B**: `cli/review/<name>_cmd.py`, added to the tuple at `cli/review/__init__.py:19-29`, importing `STABLE_FIELDS_1_8_0`, `TELEMETRY_FIELDS`, `LOAD_BEARING_BOOLS` from `panel_lint.py` inside the function body (one lazy review-to-reflect edge). Evidence: `cli/main.py:521-574` has 14 `add_command` lines, each a whole group or command, so a cross-package attach is a third registration mechanism; the C-01 record has no import-direction rule; the kernel already carries reflect vocabulary (`card_convert.py:36-42`, `panel.py:71-145`). A's root registration is B's stated fallback if the adjudicator rules the edge out. Pin, reversed: `import superclaude.cli.review` does not load `superclaude.cli.reflect` at module load.
- **Evidence both rely on**: `commands.py:53-79`, `runner.py:560`, `cli/review/__init__.py:14-36`.

### Sub-dispute 3: the serializer's accepted key set

- **Common ground**: the serializer validates and refuses, never filters; one engine-A key, `adversarial_subrun_status`, is read by `derive_verdict` (`contract.py:306`) and lies outside both frozen lists (by the advocates' counts of `contract.get("...")` literals; alias reads in `_make_result`, `contract.py:112-134`, were not counted, INV-008).
- **Position A**: accepted set `STABLE_FIELDS_1_8_0 | TELEMETRY_FIELDS | {adversarial_subrun_status}`, with a pin that the verdict-read set is covered.
- **Position B**: exactly the lint's known set (`STABLE_FIELDS_1_8_0`, `TELEMETRY_FIELDS`, the `telemetry` key; `panel_lint.py:316-321`). The lint reports any other key as L2, so a serializer that accepted `adversarial_subrun_status` would emit a contract the lint fails; the key is an engine-A trigger and does not belong in a 1.8.0 skill contract. It appears as a named exemption (a list of one) in the coverage pin.

### Sub-dispute 4: scope of helper-owned stage advance

- **Common ground**: a helper that owns a stage advances it in-process; the skill text stops telling the orchestrator to advance a helper-owned stage; an optional hash-versus-file check in `manifest_cmd`.
- **Position A**: each helper that owns a stage advances its own manifest stage (`manifest.py:302-306` then refuses the next stage if a helper was skipped).
- **Position B**: only `resolved`, `calibrated`, `debated`, with payloads that carry `outputs` hashes. `clustered` and `validated` stay orchestrator-advanced because the skill documents a rerun of `review cluster` after fixing the cards (`SKILL.md:345`) and a changed output hash on rerun raises `Conflict` (`manifest.py:293-299`).

### Sub-dispute 5: the shape of INV-L, and the owner question on how it reads

- **Common ground**: INV-L stays "Endangered, HIGH"; helper output is a comparison artifact until promotion; promotion needs M-A and M-B to pass and `reflect_verdict_replay.py` at 0 verdict differences.
- **Position A (D2a)**: a comparison artifact `panel/contract.code.yaml` and sibling files under `<output>/panel/`; legacy writers stay authoritative (`SKILL.md:349`).
- **Position B (E-1)**: three endangered points (`reviewer-cards/*-card.*`, `adversarial/merged-verdict.yaml`, `return-contract.yaml`), each with a comparison sibling under `panel/` first; M-B is a comparison (legacy files as the baseline arm, siblings as the helper arm, 20 of 20 clean); promotion is Stage 3 work through `publish --publish-from`, which the kernel refuses in shadow (`manifest.py:496-500`).
- **Owner question (open, code cannot settle it)**: if arm A fails the exit after D1, how does INV-L read: strict (helpers write only under `panel/`) or "hygiene writers allowed"?

### Sub-dispute 6: which direction is the default in 3.6

- **Common ground**: the direction is conditional on the owner's answer on headless operation; the decision is one fork (Option 3 or D3) with the preconditions in change 9.
- **Position A**: Option 3 is the direction only on the owner's "switch" answer; D3 stays open if the owner wants headless kept, because Option 3 ends the credit-free CI lane with no stated replacement. No default is named before the owner answers.
- **Position B**: Option 3 is the named default direction on "switch and no headless"; D3 on "keep headless". Option 3 adds two preconditions: a stated replacement for the I1 fan-out witness (recorded-run replay of a `published` manifest through `read_committed`) and `read_committed` wired before `parse_contract` in `_audit_once`.

## Unaddressed invariants carried into the merged file
Source: `invariant-probe.md` (Round 2.5, one independent fault-finder). 17 UNADDRESSED findings: 0 HIGH, 15 MEDIUM, 2 LOW. The merge does not resolve any of them. Section 9.3 of the merged file copies this table with the column "Status in merged file" set to OPEN, and the merge executor adds the line "Open invariants: INV-nnn" at the end of each attached change's text in the merged file. INV-004, INV-018 and INV-020 are ADDRESSED in the probe and are not carried as open (they inform changes 21, 18 and 1).

| ID | Category | Assumption (one line) | Severity | Attaches to change | Status in merged file |
|---|---|---|---|---|---|
| INV-001 | state_variables | A helper writes a comparison sibling, not the legacy file, in shadow; the consensus never says where it reads the mode. | MEDIUM | 18 | OPEN |
| INV-002 | state_variables | `calibrated` is safe for a helper-owned stage advance (B's E-3: a pure function of saved inputs). | MEDIUM | 7 | OPEN |
| INV-003 | state_variables | Arm A and M-B can each be read off the exit script as a clean 20-run set. | MEDIUM | 22 | OPEN |
| INV-005 | guard_conditions | Name-only validation over the stable plus telemetry lists makes the serializer's contract read the same by `derive_verdict`. | MEDIUM | 5 | OPEN |
| INV-006 | guard_conditions | "Helper refuses", "helper advances its own stage" and shadow's "continue as legacy, record `panel_fallback_reason`" are compatible. | MEDIUM | 7 | OPEN |
| INV-007 | guard_conditions | M-A's "every recorded run yields a lint-clean contract" holds with a serializer that refuses on a foreign key and never filters. | MEDIUM | 22 (also 5) | OPEN |
| INV-008 | count_divergence | Exactly one verdict-read key lies outside the frozen lists; only the accepted-set dispute is open. | MEDIUM | 23 (also 5) | OPEN |
| INV-009 | count_divergence | D1's CV-8 and CV-1 line lists are complete. | MEDIUM | 12 (also 13) | OPEN |
| INV-010 | count_divergence | One reviewer-count rule plus a replacement for the I1 witness suffices as D3/D7 preconditions. | LOW | 16 (also 9) | OPEN |
| INV-011 | collection_boundaries | M-B can require zero parity failures over 20 runs. | MEDIUM | 22 | OPEN |
| INV-012 | collection_boundaries | D1's fix at `reflect_shadow_exit.py:313` closes the empty-baseline defect (CV-9). | MEDIUM | 12 | OPEN |
| INV-013 | collection_boundaries | The presence rule and a refusing finalizer fit every run shape (fallback, Tier 1, all-excluded panel). | MEDIUM | 7 (also 22) | OPEN |
| INV-014 | interaction_effects | The exit rule and `reflect_verdict_replay.py` can read code-built siblings with no change beyond line 313. | MEDIUM | 22 (also 18) | OPEN |
| INV-015 | interaction_effects | The card writer has one target and CV-9 is fully applied by the line-313 edit. | MEDIUM | 4 (also 12) | OPEN |
| INV-016 | interaction_effects | Widening the fence is bookkeeping and D1 leaves INV-L and the legacy baseline untouched. | LOW | 20 | OPEN |
| INV-017 | sufficiency_challenge | "Helpers that advance their own stage make skipping detectable." | MEDIUM | 7 | OPEN |
| INV-019 | sufficiency_challenge | "Comparison siblings let promotion be decided without risk." | MEDIUM | 18 | OPEN |

Check: 17 rows; 15 MEDIUM and 2 LOW (INV-010, INV-016).

## Risk Summary
| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | Sections 3.4, 5, 8 contradict the new headline | Revert section 1 to base; re-run the consistency check of sections 3.4, 5, 8 |
| 2 | Low | Stale C-01 reading stays | Revert the appended sentence in section 2 |
| 3 | Low | Extra table disagrees with 3.2 | Remove the inserted table |
| 4 | Medium | Helper spec says a step-2 helper or "reuse" again; the executor builds the wrong set | Revert rows 2, 5, 7 of 3.2 to base text, then re-apply with the corrected list |
| 5 | Medium | Serializer filters a key the verdict map reads; trigger 11a silently off | Revert row 10 of 3.2; keep pin (i) of change 23 |
| 6 | Medium | Helpers silent under the recursion marker, or a forbidden import edge | Revert 3.3 bullets; the two-sided entry is removed with it |
| 7 | Medium | `Conflict` on re-advance in a real run; recipe test describes a stale skill | Remove the 3.3 bullet and the column; revert the recipe-test note |
| 8 | Low | A deferred option is read as a present design | Restore base 3.4 bullet only if routing is shown |
| 9 | Medium | The record implies a decision the owner has not made | Remove section 3.6; the pointers from 3.4 and 8 go with it |
| 10 | Medium | Disclosure sentence implies a deviation audit | Revert the 3.4 bullet and the 3.5 disclosure bullet |
| 11 | Medium | Deferral treated as permanent; release conditions lost | Revert the 3.5 first bullet to base wording |
| 12 | Medium | A listed line is missed (INV-009) or the fence blocks the edit | Revert the 3.5 second bullet; the fence change (20) reverts with it |
| 13 | Low | A stale document line stays | Revert the 3.5 fourth bullet |
| 14 | Low | The ref key stays on one of three lines | Revert the 3.5 third bullet and the 3.1 row |
| 15 | Low | Additive; a wrong line citation | Remove rows E9-E13 |
| 16 | Low | Additive; a wrong count | Remove the appended E7 text and the 4.3 bullet |
| 17 | Low | A stale evidence claim stays | Revert the 4.3 edits |
| 18 | Medium | INV-L reads wrong; promotion judged on the wrong artifact | Revert the INV-L row to base text |
| 19 | Medium | Rating text hides the CV-5 pin collision or the allowlist hazard, or INV-I claims an extension that no longer exists | Revert the four rows to base text |
| 20 | Medium | The fence is widened without the matching edits, or the reverse | Revert the INV-K row and the 3.5 bullet together with change 12 |
| 21 | Low | Additive rows | Remove the two inserted rows |
| 22 | High | Measurement order is wrong; a run is read as a clean 20-run set when it is not (INV-003) | Revert section 6 to base M1-M5; changes 23 and 24 revert with it |
| 23 | Low | Additive pins | Remove the inserted pin list |
| 24 | Low | Additive probe | Remove step 4 of section 6 |
| 25 | Low | A stale claim stays | Revert the three section 7 edits |
| 26 | Medium | An overstated answer to the central objection stays | Revert answers 1, 2, 4 to base text |
| 27 | Low | Open items lost | Remove section 9 |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-14T17:03:05Z

## Plan Review Log
Reviewer: analytical reviewer of the Step 4 plan (slot C-04). Checked against `debate-transcript.md` (both Round 2 sections, scoring matrix, convergence assessment), `invariant-probe.md`, `base-selection.md`, `variant-1-original.md` and `variant-2-original.md`. Defects found and fixed in this file: 20.

1. Change 4, target: it named rows 6 and 8 of the 3.2 table, but the base table has no separate row 6 (the last row is the combined "8 kept-ids, 6 clustering"). Fixed the target and the integration text.
2. Change 4, row 5: it decided the card writer's target as the legacy `reviewer-<N>-card.*` names, but INV-015 (UNADDRESSED) records that the two advocates name different files. Rewritten so only the agreed part (copy `model:` from `resolution.json`) is stated and the target stays open.
3. Change 5: JSON-in serializer input and "code owns syntax and key validity, not content" were written as common ground; they are only the Variant 2 advocate's E-7, which the Variant 1 advocate never answered. Marked; INV-007 added to the attached invariants (the table said "also 5" but the change did not list it).
4. Change 7 (and change 26 answer 4, base-weakness row "Unskippable"): "skip is detectable" omitted the condition the Variant 1 advocate set in W2 (only if the kernel verifies output hashes; `manifest.py:285-291` checks hash format only), which is also the INV-017 falsifier. Added the condition in all three places; marked the recipe-test, identical-re-advance and exit-script preconditions as Variant 2 Round 2; renamed the change title, which implied the three-stage scope of sub-dispute 4.
5. Change 9 (and strengths row 4, sub-dispute 1b): the trigger text wrote the "T5 gate must report deviations" prong (Variant 2 only), the Stage 5 deadline (Variant 2 Round 2, never answered) and the exclusion of the M4 prong as decisions, while C-009 is unresolved at 55%. Only the owner-answer prong is now written as agreed; the other prongs and the deadline are carried in 1b as open, with 1b's Position B text completed.
6. Change 9 (and change 16): the I1-witness replacement and `read_committed` wiring were stated flat as Option 3 preconditions. Marked the replacement as Variant 2's (R-5, E-2), kept the common point that the witness needs a named replacement, added INV-010 to change 9 (the table said "also 9").
7. Change 10, sub-dispute 1a and the Not-Made row for R-4: "the sentence is agreed" was false for "a tested deviation seam exists with no production producer", which is the Variant 2 advocate's R-4 correction; the Variant 1 advocate's text still says "hard-codes". The agreed content is now separated from the wording, and the wording is marked.
8. Change 10, target: "headless bullet" of 3.4. The quoted text "moves it into one place where a lint can see it" and "Both lanes end in the same serializer" sit in the second and third bullets of 3.4. Target corrected.
9. Change 16, source: the certification states at `fallback.py:49-82` are E22, not E21. Source corrected to E21 and E22.
10. Change 17 (and sub-dispute 3 common ground): "exactly one verdict-read key is outside both lists" was stated flat; INV-008 records that A counts 19 and B 18 and that both miss the alias reads in `_make_result`. Qualified. Also the citation "Variant 1 concession 10" for deleting "valid under either answer" pointed at the wrong item; corrected to Round 2 W10.
11. Change 18 (and its rationale, strengths row 8): INV-L was rewritten as "three points, siblings first", a decision, although the INV-L shape is open sub-dispute 5. Rewritten as common ground plus Position A (D2a artifact) and Position B (three points); E-1 marked as Variant 2 Round 2.
12. Change 19 (and risk row): the base's INV-I row ("Preserved and extended", a headless finalizer fails closed) contradicts the plan's own deferral of the headless finalizer (Changes NOT Being Made, row C-005 / W8) and was not corrected. Added INV-I to the rows rewritten.
13. Change 20: it said to "keep" a `test_no_new_src_superclaude_hit_in_the_skill_directory` note in the base INV-K row; that note is in Variant 2's INV-K row only. Corrected to "add".
14. Change 22, target: it said old M3 is kept as a stated non-claim, while change 24 folds old M3 into step 3; "M4" meant both the base's stub-lane lint item and Variant 2's seeded-regression item. Replaced by an explicit mapping of old M1 to M5 and a statement that Variant 2's M4 is a different item.
15. Changes 22 and 23: the plan used "18 stable-or-telemetry keys plus `adversarial_subrun_status`" (A's count) in one place and "18 in all" (B's count) in another. Both now state that the count is open under INV-008.
16. Change 22, rationale: it said the 13 pilot runs and 15 combo runs both straddle commits `9874d63fb` and `c2e3347d3`. Per E-4 only the pilot runs straddle them; the combo runs carry the stamp `20261107` and predate both. Corrected.
17. Change 22 (and change 12, change 15, change 24): step 0 (arm A, E-4), the D1-then-re-measure sequence, the Stage 5 evidence rows and the scorer-child probe were integrated as agreed although they are Variant 2 Round 2 items the Variant 1 advocate never answered and the C-019 matrix label does not record; step 3's comparison arms depended on open sub-dispute 5 without saying so; INV-013 (table "also 22") was not listed. All marked or made two-sided; INV-013 added.
18. Base Weaknesses table: debate-verified Variant 1 defects were missing for A-002 / V-12 (in-repo readers, "valid under either answer"), A-005 (snapshot listed as a retirement loss), X-005 ("reflect stays on the v2 kernel"), C-014 / C-015 (`--t2-engine`, `reviewer_briefs_materialized`), section 7 "makes a dormant path live" with section 8 answer 1, INV-I, and INV-L (marked "not conceded"). Seven rows added; the table header sentence adjusted.
19. Rules for the merge executor: no rule told the executor how to treat Variant 2 Round 2 items that were never answered. Added rule 5 (mark them "Variant 2 Round 2, not answered by Variant 1"; do not present them as agreed).
20. Strengths-to-incorporate mapping (rows 4 and 8): rows said "integrated" without saying that INV-L three points, three-stage scope, the M4 prong, the T5-gate prong and the Stage 5 deadline enter only as Position B or open entries. Wording corrected.

Checked and found correct (no change): the 17 UNADDRESSED invariants and their severities (15 MEDIUM, 2 LOW) against `invariant-probe.md`; the risk counts (1 High, 13 Medium, 13 Low); the scoring-matrix labels and percentages cited by changes 1-26; the two-sided entries for C-007, C-009, C-018, helper placement, serializer accepted key set, stage-advance scope and Option 3 versus D3 default (each matches the advocates' Round 2 texts); all Proposal A target sections exist (0-8, 3.1-3.5, 4.1-4.3) except as corrected in items 1 and 8; the template sections (Overview, Planned Changes, Changes NOT Being Made, Risk Summary, Review Status) are present; the Variant 2 strengths of base-selection are each mapped to a change.
Not fixed: nothing outstanding. Residual note for the lead, not a defect in the plan: changes 22 and 23 still cite counts and line numbers taken from the debate, which no step re-reads (the plan labels them [V] or [L] per rule 3).
