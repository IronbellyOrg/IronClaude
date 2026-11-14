# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Agent: fault-finder-r25 (general-purpose, independent, not an advocate). Input: emerging consensus after Round 2 (25 of 29 points agreed), Round 1 and Round 2 transcripts, diff-analysis.md. Categories probed: the 5 boundary-condition categories plus `sufficiency_challenge` (6 categories). No `branch-trace.md` exists for this task, so category 6 evidence is an inline source-file enumeration. The fault-finder read code and skill text and ran no tests or dispatches. Orchestrator re-verified the two HIGH items against `SKILL.md:336-342` and `document_review_loop_prompts.md:66-74`: both confirmed.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | `launch_binding` and `parent_model` are a mechanical record of the env at run time | UNADDRESSED | MEDIUM | `manifest_cmd.py:141-172` takes `--payload` as a JSON file the skill writes; no code computes it. `parent_model` has no process source (`ANTHROPIC_MODEL` empty, `CLAUDE_CODE_SUBAGENT_MODEL` unset). Binding is read at Wave 0, Agent calls happen at Wave 3 (`SKILL.md:1507` covers only a re-resolve). |
| INV-002 | state_variables | Adding a key to the `resolved` payload is safe for in-flight runs | ADDRESSED | LOW | `manifest.py:292-299` hashes the whole payload, `Conflict` on a different payload. Round 2: B proposes a legacy-replay test and moving derived values out of the hash; A proposes mapping `Conflict` to `alias_set_changed_mid_run`. Neither is in consensus item 1. |
| INV-003 | guard_conditions | "A null or out-of-set launch is a dispatch error" is enforced somewhere | UNADDRESSED | MEDIUM | Only code check is `_check_reflect_resolution` (`panel.py:137-157`), run only for `reflect-` templates (`:588`, `:682`). For `default` and `live7`, `validate_tiers` accepts any launch string (`:364-368`); the error is prose only. The anthropic-only map includes `fable` (`review-tiers.default.json:35`), `_REFLECT_LAUNCH` excludes it (`panel.py:72`). |
| INV-004 | guard_conditions | Dropping the `T3Model01` rule is enough; `SUPERCLAUDE_REVIEW_ENV=gateway` is a rare path | UNADDRESSED | MEDIUM | `select_env` precedence (`panel.py:485-494`): after the flip, exporting `SUPERCLAUDE_REVIEW_ENV=gateway` gives `launch: null` again. Reflect has D4; the loop prompt (`document_review_loop_prompts.md:70`) has no D4 equivalent, only "if superclaude is not installed, run one reviewer". |
| INV-005 | count_divergence | `reviewers[i]` maps one-to-one onto dispatched Agent calls | UNADDRESSED | MEDIUM | `SKILL.md:321` `N_eff = min(--reviewers, alias count, 3)`; `SKILL.md:340` says resolve does not apply `N_eff`. The rule does not say which reviewers drop when `N_eff < len(reviewers)`. `advance_stage` raises when `reviewers_resolved > reviewers_requested` (`manifest.py:312-315`); the skill does not say which count `reviewers_requested` is. |
| INV-006 | count_divergence | A "max 3 distinct classes" test is a meaningful ceiling | UNADDRESSED | MEDIUM | Under anthropic-only `default` resolves 4 reviewers on 2 classes and 2 models; `live7` 7 reviewers on 2 classes (1 sonnet + 6 haiku) (`panel-golden-default-live7.json`). Class count is bounded at 3 by construction; the test counts classes, not served models. "Warn when two classes bind the same model" misses N same-class reviewers. Real floor is at least 2 distinct eligible classes (D3, `SKILL.md:319`). |
| INV-007 | collection_boundaries | Empty `fallbacks` lists under anthropic-only are acceptable | ADDRESSED | LOW | Goldens show `"fallbacks":[]` for every anthropic-only reviewer. Advocate A accepted "no fallbacks" (Round 1 concession 5); reflect covers it through D4. The loop has no equivalent (see INV-004). |
| INV-008 | collection_boundaries | Duplicate slots, single-reviewer re-review and zero-reviewer templates are handled | ADDRESSED | LOW | B Round 2 requires set comparison because live T3 lists `Qwen3.8-max` twice (`T3Model02`, `T3Model04`). Re-review resolves to the anchor only (golden). Exhausted fixed anchor is fatal (`panel.py:647-649`); `@reflect-pre-x2` recovers. |
| INV-009 | interaction_effects | The dispatch rule "every Agent call carries `model == launch`" can be added to the reflect skill without breaking shadow mode | UNADDRESSED | HIGH | `SKILL.md:342`: "Dispatch is the legacy dispatch"; shadow steps "change no verdict" and the legacy path stays authoritative (`:336`); `:341` `panel_parity` compares `resolution.json` with "the legacy rotation as it ran". If dispatch is forced to follow `launch`, parity is true by construction and shadow measurement stops comparing two independent things. The rule fits only Stage 3 (`engine=panel`), which is not shipped. |
| INV-010 | interaction_effects | The `select_env` flip changes what gets dispatched | UNADDRESSED | MEDIUM | Reflect passes `--env anthropic-only` explicitly (`SKILL.md:340`, pinned at `test_shadow_skill_contract.py:245`), so the flip is a no-op for reflect. The only no-`--env` caller is the loop prompt via `panel_cmd.py:96`. On a `T3Model01` machine a `live7` loop run changes from 7 distinct gateway models with null launch to 1 sonnet + 6 haiku. |
| INV-011 | interaction_effects | Goldens stay valid with no tier-file byte change | ADDRESSED | LOW | Goldens keyed `template|env|kind`; `tiers_sha256` unchanged without tier-file edits. Both advocates move provenance (byte change, golden regeneration) into PR 2. |
| INV-012 | interaction_effects | Editing skill and prompt text is a single-file change | UNADDRESSED | LOW | `test_review_rules_text.py:21` pins the loop-prompt sentence (`E_FIRST`); a mirror exists at `plugins/superclaude/rules/prompts/document_review_loop_prompts.md` (needs sync); new SKILL.md step-1 text must fit needles in `tests/cli/reflect/test_shadow_skill_contract.py`. |
| INV-013 | sufficiency_challenge | PR 1 alone makes every dispatched reviewer launch with a valid class | UNADDRESSED | HIGH | Falsifying condition 1: the loop prompt has no instruction to pass `model` from `launch` (`document_review_loop_prompts.md:70`); after the flip the loop prints different names and dispatches as before (X-003 defect). Condition 2: reflect never reaches the flip (INV-010) and its dispatch is legacy (INV-009). Gate enumeration: select_env flip reached only by the loop, not shown to reach a dispatch consumer; resolve anthropic-only map complete, shown to pass; loop consumer has no reader, reflect step 3 is legacy dispatch, no gate passed; Agent tool family-alias rule: sonnet benign on this machine (parent `claude-gw-tier1b[1m]` equals the SONNET binding), haiku and opus UNVERIFIED; binding to served model passes only through the unverified "alias serves its first model" rule. |
| INV-014 | sufficiency_challenge | The record is honest enough to act on once `launch_binding` is added | UNADDRESSED | MEDIUM | Card headers copy `model:` from `resolution.json` (`SKILL.md:341`); parity maps ids to classes through the tier file. The Stage 2 aggregator recomputes parity from card headers and the resolution, not from the manifest payload. Nothing reads `launch_binding`; `telemetry.py:49` names the group only; nothing writes `observed`. Three reviewers named "Claude Haiku 5.5" would be served by `gpt-6.1-sol` here. |

## Summary

- **Total findings**: 14
- **ADDRESSED**: 4 (INV-002, INV-007, INV-008, INV-011; all LOW)
- **UNADDRESSED**: 10
  - HIGH: 2 (INV-009, INV-013)
  - MEDIUM: 7 (INV-001, INV-003, INV-004, INV-005, INV-006, INV-010, INV-014)
  - LOW: 1 (INV-012)

## Invariant probe gate (AD-1)

CONVERGENCE BLOCKED: 2 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-009, INV-013
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.

WARNING: 7 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-001, INV-003, INV-004, INV-005, INV-006, INV-010, INV-014
These items do not block convergence but should be reviewed.

Orchestrator disposition: the run is `--depth standard`, which has no Round 3, so no further debate round is run and the gate stays BLOCKED_BY_INVARIANTS. The two HIGH items are not accepted as risk silently: Step 4 turns each into a mandatory merge condition and the merged proposal lists them as open items for the owner (they are in `unaddressed_invariants` of the return contract).


## Appendix: fault-finder report (verbatim)

**Round 2.5 invariant probe: fault-finder report**

Verdict: the consensus claim that PR 1 alone achieves the outcome does not hold as worded. The two HIGH items (INV-009, INV-013) are textual contradictions I verified in `SKILL.md` and `document_review_loop_prompts.md`. I read code and skill text and ran no tests or dispatches. The docs facts about family aliases come from the advocates' fetches, not from me.

- **INV-001**
  - CATEGORY: state_variables
  - ASSUMPTION: `launch_binding` and `parent_model` are a mechanical record of the env at the time of the run.
  - STATUS: UNADDRESSED
  - SEVERITY: MEDIUM
  - EVIDENCE:
    - Nothing in code computes the payload. `manifest_cmd.py:141-172` takes `--payload` as a JSON file, and the skill writes that file. The existing test writes only `{"reviewers_requested":3,"reviewers_resolved":3}` (`test_shadow_skill_contract.py:124`).
    - `parent_model` has no source in the process env. `ANTHROPIC_MODEL=` is empty in my env dump and `CLAUDE_CODE_SUBAGENT_MODEL` is unset.
    - The only way to get it is for the model to report its own id, which nothing checks.
    - The binding is also read when the `resolved` stage is written (Wave 0), while Agent calls happen at Wave 3. `SKILL.md:1507` only covers a re-resolve, not a dispatch after an env change.

- **INV-002**
  - CATEGORY: state_variables
  - ASSUMPTION: Adding a key to the `resolved` payload is safe for runs already in flight.
  - STATUS: ADDRESSED
  - SEVERITY: LOW
  - EVIDENCE:
    - `advance_stage` hashes the whole payload and raises `Conflict` on a different payload (`manifest.py:292-299`).
    - B-r2 proposes a legacy-replay test and A-r2 proposes mapping `Conflict` to `alias_set_changed_mid_run` (transcript, Round 2).
    - Neither is listed in consensus item 1. B-r2 also moves derived values out of the hashed payload.

- **INV-003**
  - CATEGORY: guard_conditions
  - ASSUMPTION: "A null or out-of-set launch is a dispatch error" is enforced somewhere.
  - STATUS: UNADDRESSED
  - SEVERITY: MEDIUM
  - EVIDENCE:
    - The only code-level launch check is `_check_reflect_resolution` (`panel.py:137-157`), and it runs only for `reflect-` templates (`panel.py:588`, `:682`).
    - `default` and `live7` are not reflect templates. For them `validate_tiers` accepts any string as a launch value (`panel.py:364-368`) and `resolve` passes it through (`:679`).
    - The "dispatch error" exists only as prose.
    - The set is also undefined. The anthropic-only launch map includes `fable` (`review-tiers.default.json:35`), while `_REFLECT_LAUNCH` excludes it (`panel.py:72`).

- **INV-004**
  - CATEGORY: guard_conditions
  - ASSUMPTION: Dropping the `T3Model01` rule is enough, and `--env` or `SUPERCLAUDE_REVIEW_ENV=gateway` is a rare path.
  - STATUS: UNADDRESSED
  - SEVERITY: MEDIUM
  - EVIDENCE:
    - `select_env` precedence is `--env`, then `SUPERCLAUDE_REVIEW_ENV`, then the `T3Model01` rule (`panel.py:485-494`). After the flip, anyone who exports `SUPERCLAUDE_REVIEW_ENV=gateway` gets `launch: null` again.
    - For reflect that falls under D4 (legacy rotation), and the reflect check makes `resolve` raise `ValueError` rather than print null (`panel.py:682-687`).
    - The loop prompt has no D4 equivalent. Its only fallback is "if the `superclaude` command is not installed, run one reviewer" (`document_review_loop_prompts.md:70`).
    - So a dispatch error in the loop has no defined recovery.

- **INV-005**
  - CATEGORY: count_divergence
  - ASSUMPTION: `reviewers[i]` maps one-to-one onto the Agent calls that are dispatched.
  - STATUS: UNADDRESSED
  - SEVERITY: MEDIUM
  - EVIDENCE:
    - `SKILL.md:321` sets `N_eff = min(--reviewers, alias count, 3)`.
    - `SKILL.md:340` says `resolve` has no count option and does not apply `N_eff`, so the legacy run and the resolution can differ.
    - A rule "every Agent call carries `model == reviewers[i].launch`" does not say which reviewers are dropped when `N_eff < len(reviewers)`.
    - `advance_stage` also raises `Invalid` when `reviewers_resolved > reviewers_requested` (`manifest.py:312-315`). The skill never says whether `reviewers_requested` is the legacy `N_eff` or the resolution count.

- **INV-006**
  - CATEGORY: count_divergence
  - ASSUMPTION: A "max 3 distinct classes" test is a meaningful ceiling.
  - STATUS: UNADDRESSED
  - SEVERITY: MEDIUM
  - EVIDENCE:
    - Under anthropic-only, `default` resolves to 4 reviewers on 2 classes and 2 models. `live7` resolves to 7 reviewers on 2 classes and 2 models (1 sonnet plus 6 haiku). Both are in the golden fixtures (`panel-golden-default-live7.json:2` and `:6`).
    - The class count is bounded at 3 by construction (opus, sonnet, haiku), so the test is close to vacuous. It also counts classes, not distinct served models.
    - Three or six reviewers of one class share one bound model by construction. A's "warn when two classes bind the same model" does not catch this. B-r2's single-model warning is not in the consensus.
    - The off-by-one risk is `<=3` versus `<3`. The real floor is "at least 2 distinct eligible classes" (D3, `SKILL.md:319`).

- **INV-007**
  - CATEGORY: collection_boundaries
  - ASSUMPTION: Empty `fallbacks` lists under anthropic-only are acceptable.
  - STATUS: ADDRESSED
  - SEVERITY: LOW
  - EVIDENCE:
    - Every anthropic-only reviewer has `"fallbacks":[]` in the goldens, including `t4-*` (`panel-golden-default-live7.json:6`).
    - Advocate A accepted "no fallbacks" (Round 1, concession 5), and reflect covers the failure through D4.
    - The loop has no equivalent, which is INV-004.

- **INV-008**
  - CATEGORY: collection_boundaries
  - ASSUMPTION: Duplicate slots, single-reviewer re-review and a zero-reviewer template are handled.
  - STATUS: ADDRESSED
  - SEVERITY: LOW
  - EVIDENCE:
    - B-r2 requires a set comparison because live T3 lists `Qwen3.8-max` twice. My env dump confirms `T3Model02` and `T3Model04` are both `Qwen3.8-max`.
    - A re-review resolves to the fixed anchor only (golden `default|anthropic-only|re-review`).
    - An exhausted fixed anchor is fatal (`panel.py:647-649`), and `@reflect-pre-x2` is the recovery for it.

- **INV-009**
  - CATEGORY: interaction_effects
  - ASSUMPTION: The dispatch rule "every Agent call carries `model == launch`" can be added to the reflect skill without breaking shadow mode.
  - STATUS: UNADDRESSED
  - SEVERITY: HIGH
  - EVIDENCE:
    - `SKILL.md:342` says "Dispatch is the legacy dispatch". The shadow-mode intro says the steps "change no verdict" and that the legacy path stays authoritative (the intro of the shadow-mode steps near `:336`).
    - `SKILL.md:341` has `panel_parity` compare `resolution.json` with "the legacy rotation as it ran". Step 1 forbids rewriting the resolution to match the legacy rotation.
    - If dispatch is forced to follow `launch`, parity becomes true by construction. The shadow measurement then stops comparing two independent things.
    - The rule would only fit in Stage 3 (`engine=panel`, `SKILL.md:319`), which is not shipped.
    - Advocate A cited `:342` only as proof that nothing reads `launch`, not as a contradiction of the proposed rule.
    - PR 1 therefore has to pick one of two things: edit step 3, step 2 and the parity semantics, or leave the rule with no executing site.

- **INV-010**
  - CATEGORY: interaction_effects
  - ASSUMPTION: The `select_env` flip changes what gets dispatched.
  - STATUS: UNADDRESSED
  - SEVERITY: MEDIUM
  - EVIDENCE:
    - The reflect shadow step passes `--env anthropic-only` explicitly (`SKILL.md:340`, pinned at `test_shadow_skill_contract.py:245`), so the flip is a no-op for reflect.
    - The only no-`--env` caller is the loop prompt (`document_review_loop_prompts.md:70`), through the one production caller `panel_cmd.py:96`.
    - On a `T3Model01` machine, a loop run using `live7` (selectable by env var, per `test_review_panel_live7.py:168`) changes from 7 distinct gateway models with null launch to 1 sonnet plus 6 haiku.
    - B-r2 raised the loop-prompt gap (C-001, unresolved). The reflect no-op and the live7 behaviour change are not in the debate.

- **INV-011**
  - CATEGORY: interaction_effects
  - ASSUMPTION: Goldens stay valid with no tier-file byte change.
  - STATUS: ADDRESSED
  - SEVERITY: LOW
  - EVIDENCE:
    - The goldens are keyed by `template|env|kind`, and the flip adds no new key.
    - `tiers_sha256` is unchanged without tier-file edits.
    - Both advocates agree that provenance, which changes bytes and regenerates the packaged-tier golden, goes into PR 2.

- **INV-012**
  - CATEGORY: interaction_effects
  - ASSUMPTION: Editing skill and prompt text is a single-file change.
  - STATUS: UNADDRESSED
  - SEVERITY: LOW
  - EVIDENCE:
    - `test_review_rules_text.py:21` pins the loop-prompt sentence as `E_FIRST`, so a new loop line must not alter it.
    - The loop prompt has a mirror at `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`. Editing `src` needs a sync.
    - Any new `launch_binding` text in `SKILL.md` step 1 has to fit the needles in `tests/cli/reflect/test_shadow_skill_contract.py` (lines 175 and 285).

- **INV-013**
  - CATEGORY: sufficiency_challenge
  - ASSUMPTION: PR 1 alone makes every dispatched reviewer launch with a valid class.
  - STATUS: UNADDRESSED (the debate leaves C-001 open, and the claim is still worded as sufficient)
  - SEVERITY: HIGH
  - EVIDENCE: no branch-trace.md exists, so this is an inline source enumeration. For each gate between the fix site and the assertion site, I say whether the fix's input was shown to pass.
    - **Falsifying condition 1.** The loop prompt does not read `launch`. `document_review_loop_prompts.md:70` has no `model` instruction, and PR 1 as described edits only the reflect skill. After the flip the loop prints "sonnet plus 3× haiku" and dispatches exactly as before. The record then describes something that did not run, which is the X-003 defect. (Verified.)
    - **Falsifying condition 2.** Reflect never reaches the flip (INV-010). Its dispatch is legacy (`SKILL.md:342`), and the rule conflicts with that (INV-009).
    - **Gate 1, `select_env` flip.** `panel_cmd.py:96` is the only caller. It is reached only by the loop prompt, not by reflect. Not shown to reach the dispatch consumer.
    - **Gate 2, resolve.** The anthropic-only launch map is complete (`review-tiers.default.json:35`) and the goldens show launch set for every reviewer. Shown to pass.
    - **Gate 3, consumer.** The loop has no reader. Reflect step 3 is the legacy dispatch. No gate passed (A-001 admits this).
    - **Gate 4, Agent tool.** The docs say a family alias resolves to the parent's exact model when the parent is in that family. The parent is `claude-gw-tier1b[1m]`, equal to the SONNET binding, so sonnet is benign here. Haiku and opus are UNVERIFIED, and no in-session observation exists (`SKILL.md:348`, `requested-pinned`).
    - **Gate 5, binding to served model.** `HAIKU=claude-gw-tier2[1m]` leads to `gpt-6.1-sol` only through the unverified "alias serves its first model" rule.

- **INV-014**
  - CATEGORY: sufficiency_challenge
  - ASSUMPTION: The record is honest enough to act on, once `launch_binding` is added.
  - STATUS: UNADDRESSED
  - SEVERITY: MEDIUM
  - EVIDENCE:
    - Card headers copy `model:` verbatim from `resolution.json` (`SKILL.md:341`). Parity maps ids to classes through the tier file's `classes`, so `claude-haiku-5-5` stays "haiku".
    - The Stage 2 aggregator recomputes parity from card headers and the resolution, not from the manifest payload. Nothing reads `launch_binding`. `telemetry.py:49` only names the group, and A-r2 confirms nothing writes `observed`.
    - On this machine three reviewers named "Claude Haiku 5.5" would be served by `gpt-6.1-sol`. The record is more honest than null launch only for a human who opens the manifest.
    - This is falsified for "act on" unless PR 1 adds a reader (the report or aggregator) or labels those cards `requested-pinned`.

**Summary**
- By status: 14 entries, 4 ADDRESSED (INV-002, 007, 008, 011) and 10 UNADDRESSED.
- By severity: 2 HIGH (INV-009, INV-013), 7 MEDIUM (INV-001, 003, 004, 005, 006, 010, 014) and 5 LOW. Both HIGH items are verified textual contradictions, not guesses.
- Not verified: whether the haiku and opus family aliases bind as documented (nobody has observed an in-session dispatch). I did not read the plugin mirror of `sc-reflect-protocol`.

| Status | Result |
|---|---|
| DONE | Probed all 6 categories against `panel.py`, `manifest.py`, the tier and template data, `SKILL.md`, the loop prompt and the tests. No files were edited. |
| NEXT | Team lead decides whether PR 1 must (a) edit the loop prompt and add a binding reader, and (b) choose between a dispatch rule and the "dispatch is legacy" contract (INV-009). |