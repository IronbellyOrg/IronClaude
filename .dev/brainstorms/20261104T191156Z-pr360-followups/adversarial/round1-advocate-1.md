# Round 1 Advocate Statement: Variant 1 (opus, architect)

Source checked: `src/superclaude/cli/install_user_setup.py` (lines 47-54, 283-414 read this turn) and `tests/cli/test_install_user_setup.py` (grep of lines 366, 397-398, 544).

## Position Summary

The two variants agree on every structural decision: the same three edit sites (292, 317, 392), option C, the catalog staying put, and project-only meaning "not installed". Variant 1's lasting contribution is the architecture argument for why C is right (one root, `home`, resolved at 303, and the subprocess env at 392 is the only leak) and a finding-3 test that proves the seed's actual success criterion. Variant 2 is better on finding 1 (the `ValueError` escape and a real-input test), and the merged spec should take those from it.

## Steelman of Variant 2

The strongest form of Variant 2's argument: a fix spec is only as good as its regression tests and its exception coverage, and Variant 2 verified both against real interpreters instead of reasoning about them.

- It found a second, reachable escape from line 292 that Variant 1 missed. `known_marketplaces.json` is JSON, so `"path": "/x/\u0000y"` passes the `isinstance(path, str)` and `is_absolute()` guards at 290 (neither touches the filesystem) and then raises `ValueError` inside `resolve()`. The orchestrator confirmed this on CPython 3.11.15 (diff-analysis Metadata). Variant 1's tuple `(OSError, RuntimeError)` would let it escape `install_plugins` through the unguarded call at 343, breaking the "never fatal" constraint.
- It ran Python 3.13.5 and showed a loop does not raise there, which turns Variant 1's unverified doc reading into a fact and explains why a loop-only test cannot fail on 3.13.
- Its finding-1 test uses two real bad inputs (a NUL path that fails on every version, a self-loop that fails on 3.10-3.12, and CI runs 3.10 per the Metadata) and no pathlib monkeypatch. That tests the code the user will hit, not a mock.
- Its finding-3 test checks that the rest of the environment survives (`SENTINEL`) and that `CLAUDE_CONFIG_DIR=""` is handled, which are the two ways the new env block could be wrong that Variant 1's test does not catch.
- Its `e.get("scope", "user")` default keeps today's behaviour for any record shape without `scope`, which is the conservative choice for a minimal-diff fix.

What it gets right: everything above on finding 1, and the env-preservation check. Those points should win.

## Strengths Claimed

1. **The root-of-truth argument for option C** (Variant 1, "Decision: Option C", lines 110-114, and "Convergence point", line 143). Every plugin-state read already derives from `home` (settings 311, `plugins_dir` 315, records 316-317, catalog via `_CATALOG_DIR` 47 used at 292, 349, 352). The one place state escapes is `env` at 392, which is `None` for every command except `plugin update` (verified at 392 this turn). Variant 1 frames C as "remove the divergence where it enters", and adds the long-term point Variant 2 lacks: a future whole-installer `CLAUDE_CONFIG_DIR` decision can then be made in one place (`install_user_setup`) by passing a different `home`, with no change inside `install_plugins`. Option A would bake a second, plugin-only root into the function that such a change would have to undo (Variant 1, line 112).
2. **A finding-3 test that proves the seed's success criterion, not a proxy for it** (U-003, rated High). Seed brief criterion 3: "With `CLAUDE_CONFIG_DIR` pointing at a profile whose `known_marketplaces.json` holds a foreign `ironclaude`, no `ironclaude` command runs against a profile that was not validated." Variant 1's test builds exactly that profile (`tmp_path/"cfg"/"plugins"/"known_marketplaces.json"` with a foreign `ironclaude`) and asserts both the command list and, for every call, `"CLAUDE_CONFIG_DIR" not in env` and `env["HOME"] == str(home)` (Variant 1, lines 137-139). Variant 2's test reuses the move-pin fixture with no foreign profile, so it proves the env shape but never stages the scenario the criterion names.
3. **Strict scope filter matches the invariant the fix exists to enforce.** Finding 2 is "a record of another scope was counted as evidence about the user copy". Variant 1 counts only records that say `"scope": "user"` (line 64). A record without `scope` triggers at most one `plugin install --scope user -y`, after which the real CLI writes a scoped record, so the state heals itself in one run; a failure is a reported warning (409-413).
4. **Narrow catch, explicitly justified as a security guard** (lines 27, 31). Lines 286-291 cannot raise; only 292 touches the filesystem. Both variants agree here, but Variant 1 names why a broad `except Exception` is wrong in this function: it decides which marketplace may install a pinned plugin.
5. **Honest flagging of the 3.13 contradiction with the seed brief** (line 29), stated as unverified rather than asserted.

## Weaknesses Identified in Variant 2

1. **Its finding-3 test does not stage the required scenario.** It sets `CLAUDE_CONFIG_DIR` to an empty `other-profile` path and `""` (Variant 2, lines 193-195). No foreign `ironclaude` exists anywhere, so the test cannot show the property the seed's criterion 3 demands. A future regression that, say, reads `known` from `$CLAUDE_CONFIG_DIR` while still stripping the variable from the env would pass Variant 2's test and fail Variant 1's command-list assertion.
2. **`e.get("scope", "user")` reintroduces the class of guess finding 2 removes.** A record that does not state its scope is not evidence about the user-scope copy. Variant 2 justifies the default as preserving "older record shape" (line 89), but the only older shape it could mean is unverified; the seed brief's real-CLI proof shows every record carries `scope`. Low impact either way (X-001), but the strict filter is the one that matches the stated invariant.
3. **Its claim about crash hardening is partly overstated.** Variant 2, line 90, says a non-list record value "currently" makes lines 327-329 raise. Line 329 iterates `installed[p]` and filters `isinstance(e, dict)`; a string value iterates characters and is filtered, and only non-iterables (int, None) raise. The guard is still correct and both variants include it, so this is a framing point, not a defect in the code.
4. **The `OSError` member is kept "defensive, not evidenced"** (line 248). That is fine, but Variant 2 does not name a concrete `OSError` source; Variant 1 does (a permission error on `readlink` during non-strict resolve, line 29). Minor.

## Concessions

1. **C-001: Variant 2 is right and Variant 1 is wrong.** `ValueError` from an embedded NUL is a real, reachable escape from line 292 (orchestrator-verified on 3.11.15). Without it, Variant 1's fix leaves finding 1 open for a hand-edited or malicious `known_marketplaces.json`. The tuple must be `(OSError, RuntimeError, ValueError)`.
2. **C-002: Variant 2's test design is better.** Variant 1's wrapper monkeypatches `pathlib.Path.resolve` for the whole process (since `setup.Path` is `pathlib.Path`), keyed on `self.name == "loop"`. It tests a mock of the failure rather than the input that causes it, and it is fragile if anything else resolves a path named `loop` during the call. The NUL path gives Variant 1's goal (red on every interpreter) with a real input.
3. **Variant 1's 3.13 point was unverified; Variant 2 verified it** (3.13.5 returns without raising on a loop).
4. **Variant 1 overstated "not a regression of anything that worked"** (line 178). Before the fix, a `CLAUDE_CONFIG_DIR` user with no `ironclaude` registration in `~/.claude/plugins` got `marketplace add` and `plugin install` run inside their `CLAUDE_CONFIG_DIR` profile (env inherited at 392), so plugins did land in the profile they run, if inconsistently (non-pinned plugins re-installed every run because `installed` at 317 read the other profile). After C they land in `~/.claude` instead. That is a user-visible change, which bears on A-003.
5. **C-005: Variant 2's assertion set is a strict superset** (adds `CLAUDE_CONFIG_DIR` absent). `GIT_CONFIG_COUNT` and `GIT_CONFIG_VALUE_0` are both keys of `_HTTPS_GITHUB` (lines 50-54), so either absence check works; asserting `CLAUDE_CONFIG_DIR` absent is the extra value.
6. **The `SENTINEL` and `""` iterations in Variant 2's finding-3 test catch real failure modes** Variant 1's test misses (an env block that drops the rest of `os.environ`, and empty-string handling).

## Per-Point Verdicts

| Point | Winner | Evidence |
|---|---|---|
| S-001 | merge: Variant 2's frontmatter and risk table, Variant 1's prose rationale for option C | Shape is Low severity; the table scans faster, the prose carries the long-term argument (V1 lines 110-114) |
| C-001 | Variant 2 | NUL path passes the guards at 290 and `resolve()` raises `ValueError` (verified 3.11.15); V1's tuple lets it escape via 343 |
| C-002 | Variant 2 | Real inputs, no pathlib monkeypatch; NUL case is red on every interpreter, loop case red on CI's 3.10 |
| C-003 | Variant 1 | Strict `scope == "user"` matches the finding-2 invariant; worst case is one self-healing install, non-fatal (409-413) |
| C-004 | merge: Variant 1's foreign-`ironclaude` `CLAUDE_CONFIG_DIR` profile and command-list assertion, plus Variant 2's `""` iteration and `SENTINEL` check | V1 proves seed criterion 3 directly (U-003); V2 proves the rest of the env survives |
| C-005 | Variant 2 | Superset: also asserts `CLAUDE_CONFIG_DIR` absent; `GIT_CONFIG_COUNT` is an `_HTTPS_GITHUB` key (line 51) |
| X-001 | Variant 1 | Same as C-003: a scopeless record is not evidence about the user copy; seed proof shows real records always carry `scope` |

## Shared Assumption Responses

- **A-002 (no plugin command needs auth from the user's `CLAUDE_CONFIG_DIR` profile): QUALIFY.** True for what this step installs: the orchestrator ran `marketplace add` and `plugin install` against a throwaway profile with no login, the pinned catalog is a local directory, and `plugin update` clones public GitHub over HTTPS (`_HTTPS_GITHUB`, 50-54). Not proven for a private marketplace added through `extraKnownMarketplaces`; if one needs a login stored only in the `CLAUDE_CONFIG_DIR` profile, its command fails as a reported warning (403-413), never fatal. The spec should state this as a known limit.
- **A-003 (the behaviour change for `CLAUDE_CONFIG_DIR` users needs no user-facing note): REJECT.** Per Concession 4, plugins for such users move from the profile they run to `~/.claude`, which is a visible change, and `CHANGELOG.md` exists at the repo root. One CHANGELOG line ("`superclaude install` now installs plugins into `~/.claude` even when `CLAUDE_CONFIG_DIR` is set, matching every other install step") costs nothing and is outside the 5-edit source limit (a docs file, not a source file).
