# Merge Log

## Metadata

- Base: Variant 2 (sonnet:refactorer), `variant-2-sonnet-refactorer.md`
- Incorporated: Variant 1 (opus:architect), `variant-1-opus-architect.md`; orchestrator additions named in `refactor-plan.md`
- Executor: merge-executor (Step 5 of /sc:adversarial)
- Plan: `refactor-plan.md` (6 planned changes, auto-approved 2026-11-04T19:25:00Z)
- Changes applied: 6 of 6
- Status: SUCCESS
- Output: `merged-output.md`
- Timestamp: 2026-11-04T19:26:04Z

## Changes Applied

### Change 1: Finding-3 regression test (Variant 1 scenario, profile-aware fake)

- Status: APPLIED
- Target: "Finding 3 / Regression test (new, after `test_plugins_move_ponytail_to_a_new_pin`)", replaced
- Before: `test_plugins_pin_claude_commands_to_the_validated_home`, built on `_pinned_home(... old, old)`; the fake recorded `kwargs.get("env")`; asserted `env is not None`, no `CLAUDE_CONFIG_DIR`, `HOME == str(home)`, `SENTINEL` kept, at least two calls.
- After: `test_plugins_run_claude_against_the_validated_home`. `cfg/plugins/known_marketplaces.json` holds a foreign `ironclaude`; `home = _plugin_home(tmp_path / "home", {"ponytail@ironclaude": True})`; `SENTINEL=kept`; the fake resolves `profile` from `kwargs["env"] or os.environ` like the real CLI and records `(command[1:], profile, env)`; loop over `CLAUDE_CONFIG_DIR` = `cfg` and `""`. Asserts the exact `marketplace add` + `plugin install` commands, every profile `== str(home / ".claude")`, no `CLAUDE_CONFIG_DIR`, `SENTINEL` kept. Fails today because `env=None` lets the fake see `CLAUDE_CONFIG_DIR=cfg`.
- Provenance: `<!-- Source: Variant 1, "Finding 3 / Regression test" ... + Base (SENTINEL and "" checks) + orchestrator addition (profile-aware fake), merged per Change #1 -->`

### Change 2: Variant 1 rationale for option C

- Status: APPLIED
- Target: "Finding 3 / Decision: C", appended as rationale point 5
- Before: four rationale points.
- After: point 5, "It keeps `home` the only root of truth": every read and write derives from `home` (line 303), the env at line 392 is the only leak, and a later whole-installer `CLAUDE_CONFIG_DIR` decision stays in one place (`install_user_setup`, lines 417-427, from Variant 1).
- Provenance: `<!-- Source: Variant 1, "Finding 3 / Decision: Option C" (root of truth and long-term view), merged per Change #2 -->`

### Change 3: Docs and CHANGELOG

- Status: APPLIED
- Target: "Out of scope" (bullet removed) and new H3 "Docs and CHANGELOG" under "Convergence point and edit count"
- Before: Out of scope listed "Docs changes; none of the three fixes alters a documented flag or command."
- After: that bullet removed. New subsection: (a) one sentence added to the `CLAUDE_CONFIG_DIR` note at docs/getting-started/installation.md:494-498; (b) a new `[Unreleased]` CHANGELOG entry, a separate `### Install: ... (#360 follow-ups)` section with `#### Fixed`; closing line that the code change stays at 3 edits in one source file plus its test file. The section title placeholder `...` is kept as the plan wrote it.
- Provenance: `<!-- Source: debate A-003 ... merged per Change #3 -->` on the subsection; `<!-- Source: Base (original, modified) — "Docs changes; none" bullet removed per Change #3 -->` on Out of scope

### Change 4: A-002 as a known limit

- Status: APPLIED
- Target: "Risks and edge cases", row "Auth stored under the user's `CLAUDE_CONFIG_DIR`"
- Before: Notes said it was UNVERIFIED whether the commands need a login.
- After: Notes say "Known limit": holds for the default plugins (local directory catalog, public GitHub marketplaces; proven with the real CLI in a throwaway profile with no login); a private marketplace needing a login kept only in the `CLAUDE_CONFIG_DIR` profile fails as a reported warning, never fatal. The Case and Behaviour cells and the base's line references (403-408, 409-413) are kept.
- Provenance: `<!-- Source: debate A-002 (both QUALIFY), merged per Change #4 -->` inside the row

### Change 5: Overstatements corrected, verified facts recorded

- Status: APPLIED (three sites)
- Site a, "Finding 2 / Decision" last rationale bullet. Before: a non-list record value "makes `installed[p]` raise `TypeError`/`KeyError`-class errors at lines 327-329". After: the non-dict `plugins` clause is kept; a non-list record value raises at line 329 only when it is not iterable (int or `None`), a string iterates and is filtered.
- Site b, "Finding 3 / Decision: C" point 4. Before: "I did not run `claude` (forbidden); a pre-merge throwaway-`HOME` check ... is listed under Risks." After: the orchestrator ran the real CLI with `CLAUDE_CONFIG_DIR` removed and `HOME` pinned; it wrote only under `HOME/.claude` and left the other profile untouched.
- Site c, "Risks and edge cases" closing paragraph. Before: "Pre-merge manual check (not run here ...)". After: "Real-CLI verification" listing the two proofs (HOME pin; user-scope install beside a project copy succeeded and both records coexist).
- Provenance: `<!-- Source: Base (original, modified) — ... per Change #5 -->` on sites a and b; `<!-- Source: orchestrator real-CLI verification this session, replacing the base's "Pre-merge manual check" per Change #5 -->` on site c

### Change 6: Deterministic `GIT_CONFIG_*` absence check

- Status: APPLIED
- Target: "Existing test impact", row `test_plugins_move_ponytail_to_a_new_pin`
- Before: three replacement assertions, no environment setup.
- After: adds `monkeypatch.delenv("GIT_CONFIG_COUNT", raising=False)` before the run so the absence assertion does not depend on the developer's shell.
- Provenance: `<!-- Source: Base (original, modified) — test_plugins_move_ponytail_to_a_new_pin row extended per Change #6 -->`

### Changes NOT made (per plan)

- C-002 (pathlib `Path.resolve` monkeypatch), C-003 / X-001 (strict `scope == "user"`), S-001 (Variant 1 prose layout), and an `OSError`-forcing test case: not applied, as the plan's table requires.
- `base-selection.md` also lists Variant 1's "narrow-catch security rationale" as a strength to incorporate. The plan schedules no change for it, so it was not added. Reported here for the orchestrator; no improvisation.

### Other merge-level edits

- Frontmatter replaced with `topic: pr360-followups`, `type: merged-spec`, `base: variant-2-sonnet-refactorer`, `convergence: 0.78`.
- Provenance header added (Provenance, Base, Merge date) and a `<!-- Source: ... -->` comment on every H2/H3 section and every changed block.
- H1 kept verbatim from the base (no plan change covers it).

## Post-Merge Validation

### Heading hierarchy

PASS. One H1, then 8 H2 sections in the base order (Summary; Finding 1; Finding 2; Finding 3; Convergence point and edit count; Existing test impact; Risks and edge cases; Out of scope). Every H3 sits under an H2; the only new heading is H3 "Docs and CHANGELOG" under H2 "Convergence point and edit count". No level is skipped.

### Internal references

PASS.
- Edits 1, 2, 3 are each defined once (Change headings in Findings 1-3) and match the edit table rows 1-3.
- Rationale "point 4 of the finding-3 rationale" (Risks paragraph) resolves to Decision: C point 4; "recorded under Risks and edge cases" (point 4) resolves to the Real-CLI verification paragraph.
- "see Finding 2" and the "Project-scope-only record" row reference resolve.
- New test names appear once each and are unique: `test_plugins_refuse_an_unresolvable_ironclaude_registration`, `test_plugins_judge_the_pin_by_the_user_scope_record`, `test_plugins_run_claude_against_the_validated_home`. The replaced name `test_plugins_pin_claude_commands_to_the_validated_home` has no remaining occurrence. "New tests: 3 (one per finding)" still holds.
- Helpers and anchor tests the spec names exist in `tests/cli/test_install_user_setup.py`: `_plugin_home`, `_pinned_home`, `_recording_run`, `test_plugins_move_ponytail_to_a_new_pin`, `test_plugins_keep_ponytail_at_its_pin`, `test_plugins_refuse_a_foreign_ironclaude_marketplace`, `test_plugins_skip_already_installed`.

### Contradiction re-scan

PASS: no new contradiction introduced by the merge.
- Edit count: "3 blocks" (Summary), "Total: 3 edits" (edit table), "stays at 3 edits" (Docs and CHANGELOG), "1 block (line 392)" for option C: consistent. Docs and CHANGELOG are stated as non-source, so the level-2 claim stands.
- Except tuple: `(OSError, RuntimeError, ValueError)` everywhere; Variant 1's `(OSError, RuntimeError)` tuple was not imported. The Finding 1 H3 title "catch only OSError/RuntimeError" is the base's open-question wording, not a tuple.
- Scope default: only `e.get("scope", "user")`, and the "Record without a `scope` key" row says "Counted as user scope": consistent. Variant 1's strict rule was not imported.
- Finding-3 test name: one name, `test_plugins_run_claude_against_the_validated_home`, used in one place.
- Checked, not contradictions: (1) the "User who runs `claude` with `CLAUDE_CONFIG_DIR`" row says "A user-visible note would be new behaviour", and Out of scope keeps "A user-visible warning when `CLAUDE_CONFIG_DIR` is set"; both refer to runtime output, while Change 3 adds a documentation sentence. (2) The Options row "One test; 1 assertion update" for C still matches: Change 6 adds a setup line, not an assertion. (3) Change 5 site a keeps the base's non-dict `plugins` clause, which the plan did not ask to correct.

### Observation outside the merge

The spec's line numbers cite commit 605da2ff. The worktree now has uncommitted edits to `src/superclaude/cli/install_user_setup.py` and `tests/cli/test_install_user_setup.py` (132 insertions, 5 deletions against 605da2ff), so line numbers in the working tree no longer match the spec (for example `test_plugins_move_ponytail_to_a_new_pin` is now at line 379, `test_plugins_refuse_a_foreign_ironclaude_marketplace` at 497). This is not caused by the merge and was not changed.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 6 | 6 | 0 | 0 |

Post-merge validation: PASS (heading hierarchy, internal references, contradiction re-scan). One item for the orchestrator: the base-selection strength "narrow-catch security rationale" from Variant 1 is not in the plan and was not merged.
