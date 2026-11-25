<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Feature Summary

Add the model `muse-ember-1.0` as a Tier 04 (`tier4`) model in the ccsession tier system, registered the same way the sibling Muse models (`muse-wonder-1.0`, `muse-wonder-full-1.0`, `muse-spark-1.3`) are registered today.

## Problem Statement

Tier 4 currently lists GPT-6 Luna, Claude Haiku 5.5 and Grok 4.7. muse-ember-1.0 is not present anywhere in this repo (no profile, picker entry, display override or docs mention), so it cannot be resolved, shown or used through ccsession. Not known yet: who needs it or why (not stated in the description).

## User Story

As a Coder workspace user, I want muse-ember-1.0 available in Tier 4, so that ccsession can resolve, show and fall back to it like the tier's other models.

## Proposed Solution

Follow the existing muse-wonder-1.0 pattern, adjusted to whatever the Coder workspace env actually serves:

- In `src/superclaude/skills/ccsession-tag/ccsession-models.json`: the tier4 `models_env` slot list names slots (`T4Model01`-`T4Model03`), not models. Per the owner decision below, muse-ember-1.0 takes position 2. ccsession orders a tier by the order of the slot names in `models_env` (`models.py:661`, `for slot in t["models_env"]`), not by slot number, so the change is additive: the Coder env adds a new slot `T4Model04=muse-ember-1.0` and leaves `T4Model01`-`T4Model03` untouched, and this repo sets `tiers.tier4.models_env` to `["T4Model01", "T4Model04", "T4Model02", "T4Model03"]` (Luna, Ember, Haiku, Grok). Tier 3 stays unchanged. The slot numbers then read out of order; document that in the README. The picker surface needs `muse-ember-1.0` in `picker.show`, a `picker.display_overrides` entry ("Muse Ember 1.0", matching the "Muse Wonder 1.0" style), and an entry in `picker.one_million_context` because its own window is 1,000,000.
- Update `src/superclaude/skills/ccsession-tag/README.md` (tiers and any alias tables) and `MODEL-TIERS.md` (Tier 4 row and model tables; score and price stay "not scored / not priced" unless known — Not known yet).
- Update tests that pin tier membership (`tests/unit/test_ccsession_tiers.py` tier4 slot env fixtures, `tests/skills/test_model_alias_policy.py`, `tests/review/` where model lists are pinned) and the CHANGELOG `[Unreleased]`.
- The per-workspace slot values (`T4Model0N`, `T4_WINDOW`) come from the Coder workspace env file (`/etc/aidev02/aienv.d/defaults.sh`, IronbellyOrg/Coder, outside this repo). This change depends on a matching Coder release (see "Coder dependency" below). Because `ccsession-models.json` is downloaded from master at launch (per CoderOrchestrator's read of `models.py` on 2026-11-12), the new slot `T4Model04` must exist in the Coder defaults before this repo's JSON change reaches master, or tier-mode launches stop with "slot is not set".

## Acceptance Criteria

- [ ] `muse-ember-1.0` appears in tier4 in this repo's data and docs at position 2 of the list, with its own window of 1,000,000 recorded, and Tier 4 then reads: GPT-6 Luna, Muse Ember 1.0, Claude Haiku 5.5, Grok 4.7 (`tiers.tier4.models_env` is `["T4Model01", "T4Model04", "T4Model02", "T4Model03"]`). Tier 3 remains GLM 5.3 and Qwen3.8-max.
- [ ] The picker (`/model`) shows Tier 4 including muse-ember-1.0 with its display name (style of "Muse Wonder 1.0").
- [ ] `tests/unit/test_ccsession_tiers.py` (and any other test pinning tier4 membership) covers the new model and the full suite passes.
- [ ] `MODEL-TIERS.md`, the skill `README.md` tier section and the CHANGELOG `[Unreleased]` mention the change; no score, price or window is invented where unknown.
- [ ] On a workspace whose Coder env serves the model, `ccsession --tier tier4` resolves muse-ember-1.0 through the tier.

## Owner decisions (2026-11-12)

- muse-ember-1.0 has a context window of 1,000,000. The owner is fine with Tier 4's 500,000 window (`T4_WINDOW` stays 500000). Per the proxy rule recorded in #488 (`local-gateway-alias-proxy.py:720-722`, not re-checked here), a model is skipped only when its own window is lower than its tier's, so 1,000,000 against 500,000 is allowed.
- Position: Tier 04, model 02, second position. Tier 4 becomes GPT-6 Luna, Muse Ember 1.0, Claude Haiku 5.5, Grok 4.7. Claude Haiku 5.5 moves down one place in the list.
- The owner cancelled the proposed move of Grok to Tier 3 and confirmed that Grok stays in Tier 4. Tier 3 remains unchanged at a 900,000-token window; Tier 4 remains at 500,000.

## Coder dependency

Read-only check of `IronbellyOrg/Coder` `defaults.sh` at release 20261110-1 (2026-11-12): Tier 4 holds `T4Model01=gpt-6-luna`, `T4Model02=claude-haiku-5-5`, `T4Model03=grok-4.7` with `T4_WINDOW=500000`; there is no `T4Model04`, and `muse-ember-1.0` appears nowhere in `CCSESSION_MODEL_ORDER`. The Coder half is tracked in https://github.com/IronbellyOrg/Coder/issues/503 (filed by CoderOrchestrator, who also confirmed the values above). It is additive: Coder only adds `T4Model04=muse-ember-1.0` (`T4Model04_WINDOW=1000000`), adds `muse-ember-1.0` to `CCSESSION_MODEL_ORDER`, and bumps `VERSION`, `defaults.sha256` and the changelog; `T4Model01`-`T4Model03` stay as they are. Grok remains in Tier 4; no Tier 3 slot or window change is required by this issue. Coder main is at release 20261110-1, and a draft Coder release B (PR #502, release 20261112-1, member rule plus Tier 2b) edits the same files, so version and checksum order matters (details in Coder#503).

Why additive, not renumbered (verified in `src/superclaude/skills/ccsession-tag/models.py:661` on master): the tier order is the order of `models_env`, so renumbering slots in Coder would change what the current list resolves (Grok silently dropped from Tier 4, Haiku shifted) until this repo's JSON merges. With the additive layout the Coder release changes nothing for anyone until this repo's JSON names `T4Model04`.

Merge order: Coder release first and distributed to workspaces, then this repo's JSON change. A list that names `T4Model04` before the env sets it makes `_all_tiers` raise "T4Model04 is not set" (`models.py:663-664`), which stops every tier request. Workspaces download the JSON from master at launch (per CoderOrchestrator's read of `models.py`), so merging to master is the release.

Gateway: CoderOrchestrator listed the live gateway's models read-only on 2026-11-12 and `muse-ember-1.0` is listed (a completion call was not made, so serving it is not proven). Proposed position in `CCSESSION_MODEL_ORDER`: right after `muse-spark-1.3`; the owner may override. Coder test-56 pins only the member-rules string, so no Coder test pins the Tier 4 slots.

## Out of Scope

- Any change to other tiers, other models, aliases (e.g. the `muse`/`wonder` profiles) or the tier structure.

## Components Affected (from `/sc:analyze`)

- `src/superclaude/skills/ccsession-tag/ccsession-models.json` — `tiers.tier4.models_env` (slot list `T4Model01`-`T4Model03`), `picker.show`, `picker.one_million_context`, `picker.display_overrides` (muse-wonder-1.0 pattern: profiles.wonder, picker.show, one_million_context, display_overrides "Muse Wonder 1.0").
- `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` — Tier 4 row (line 46) and model tables.
- `src/superclaude/skills/ccsession-tag/README.md` — tiers section (~line 440).
- `tests/unit/test_ccsession_tiers.py` — tier4 slot env fixtures (lines 86-91), tier slot assertions (line 222).
- `tests/skills/test_model_alias_policy.py`, `tests/review/` — model-list pins.
- `CHANGELOG.md` `[Unreleased]`.
- `docs/reference/model-aliases.md` — currently names no muse or tier4 models; may not need a change.
- Coder workspace env (`defaults.sh`, IronbellyOrg/Coder, outside this repo) — supplies the actual slot values; to check, not verified.

## Related Issues/PRs

- #488 — parent (tier restructure that set the current Tier 4)
- #518 — sibling (merged PR that applied #488 to Tier 4)
- #489 — related (follow-up tier-data update)
- #517 — related (tier failover behavior that would apply to the new model)

<!-- sc:issue:create template=issue-feature-simple -->
