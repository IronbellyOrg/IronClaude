---
round: 1
advocate: 2
variant: variant-2-sonnet-refactorer
persona: refactorer
model: sonnet
---

# Round 1 advocate statement: Variant 2 (refactorer)

## Position Summary

The two variants agree on the architecture (three edits; Option C; user-scope-only records; catalog stays put), so the debate is about whether the fix is complete on real inputs. Variant 2 is more complete where it matters: it catches the `ValueError` that an embedded NUL byte raises from line 292 and tests it with real inputs. Variant 1 has the better finding-3 test scenario, and both variants miss that the docs describe the behaviour Option C changes.

## Steelman of Variant 1

Variant 1 is the more disciplined statement of why Option C is right. Its strongest points:

- It frames the three findings as one root. `home` at `install_user_setup.py:303` is the single root of truth, and only the subprocess environment (line 392) escapes it. It also notes that C keeps a later whole-installer decision about `CLAUDE_CONFIG_DIR` in one place. That is a real long-term argument against A, which would bake a plugin-only root into this function.
- It argues for a narrow catch: lines 286-291 cannot raise, and a catch-all in a function that guards "which marketplace may install a pinned plugin" would hide programming errors. Variant 2 agrees.
- Its finding-3 test (U-003) follows the seed brief's success criterion 3 word for word. `CLAUDE_CONFIG_DIR` points at a profile whose `known_marketplaces.json` holds a foreign `ironclaude`. The test asserts that no recorded command can see that profile.
- Its strict `scope == "user"` rule matches the proven record format, in which every record carries `scope`.
- Its test-forcing wrapper makes the finding-1 test red on every interpreter, including 3.13.

None of this is wrong. The disagreement is about what is missing from it.

## Strengths Claimed

1. **The `ValueError` escape (C-001, U-001).** A JSON registry can hold `"path": "/x/\u0000y"`. `Path(path).is_absolute()` accepts it and `.resolve()` raises `ValueError`. The orchestrator confirmed this on CPython 3.11.15 (diff-analysis.md Metadata), and Variant 2 probed 3.13.5 as well. With `(OSError, RuntimeError)` alone, finding 1 stays open on every Python version for this input. The loop case is only open on 3.10 to 3.12.
2. **A finding-1 test that cannot go green by accident (C-002, U-002).** Variant 2 drives real bad inputs through the unmodified `pathlib`: a NUL path (red on every interpreter) and a self-symlink loop (red on 3.10 to 3.12). CI runs 3.10 (`.github/workflows/test.yml:22`), so both cases are red there. No test double stands between the input and the code under test.
3. **Verified rather than assumed.** Variant 2 probed 3.13.5 and recorded that a loop does not raise there. The seed brief says `OSError` on 3.13+, so it was wrong. Variant 1 left the 3.13 claim unverified ("no 3.13 interpreter in this workspace").
4. **Scopeless records keep today's behaviour (C-003, X-001).** `e.get("scope", "user")` makes the fix change only what the findings require. Behaviour for any other record shape stays as it is.
5. **Fuller proof for finding 3 (C-004, C-005).** The test loops over `CLAUDE_CONFIG_DIR` set and `""`, and a `SENTINEL` variable proves the rest of `os.environ` survives the filter. The updated test at line 397 also asserts the variable is removed.
6. **Honest risk accounting.** The risk table marks each UNVERIFIED row and states the user-visible cost of C: plugins go into `~/.claude`, not the profile the user runs.

## Weaknesses Identified in Variant 1

1. **Its own precedent contradicts its tuple.** Variant 1 justifies `(OSError, RuntimeError)` as "the tuple the repo's only other `CLAUDE_CONFIG_DIR`-aware reader already uses ... (install_mcp.py:739)". I read that line: it is `except (OSError, ValueError, RuntimeError):`. The cited convention includes `ValueError`. Following it would have given Variant 2's tuple.
2. **The finding-1 test setup is partly dead weight.** Variant 1 builds a real two-link loop, then monkeypatches `setup.Path.resolve` to raise whenever `self.name == "loop"`. The real loop is never resolved, because the wrapper intercepts first. The test therefore checks the response to a synthetic exception, not to any input the registry can hold. It also patches a method of the `pathlib.Path` class itself, which couples the test to implementation details.
3. **Its finding-3 test scenario is narrative, not coverage.** `subprocess.run` is faked, so nothing ever reads the foreign `known_marketplaces.json` in `cfg`. The assertions that carry the test are `env is not None`, `CLAUDE_CONFIG_DIR not in env` and `env["HOME"] == str(home)`. That is the same contract Variant 2 asserts. The test also never checks the empty-string case or that the rest of the environment is preserved.
4. **It understates the user-visible change.** Variant 1 says C is "not a regression of anything that worked". Today the commands inherit `CLAUDE_CONFIG_DIR`, so for those users plugins do land in the profile they run (validation is the part that is wrong). After C they land in `~/.claude` instead. Variant 2's risk table says this plainly; Variant 1 does not.
5. **Strict scope handling has a churn risk.** If any record shape without `scope` exists (UNVERIFIED either way), strict handling queues `plugin install` on every run for a plugin that is already present. That would produce a repeated warning if the CLI rejects an install over an existing install. Defaulting to user scope avoids this.
6. **The 3.13 claim is unverified.** Variant 1 states the 3.13 behaviour from the documentation and says it was not reproduced. Variant 2 reproduced it.

## Concessions

- **U-003 is a real strength of Variant 1.** Its test setup maps one-to-one onto success criterion 3 in the seed brief. Variant 2's test checks the env contract only and never mentions the foreign-marketplace scenario. A reviewer tracing the criterion to a test will find it faster in Variant 1.
- **Variant 2's "Docs changes; none" is wrong.** `docs/getting-started/installation.md:478-479` says "Ponytail keeps its files under `CLAUDE_CONFIG_DIR` when that variable is set, while the installer always writes to `$HOME/.claude`". Lines 494-498 give the `CLAUDE_CONFIG_DIR` note. The `[Unreleased]` CHANGELOG entry for #330 (CHANGELOG.md:18-29) describes the plugin install. After C the plugin commands act on `$HOME/.claude`, so the wording at line 478 needs rechecking. Variant 1 skipped this too, but I should have caught it.
- **The `OSError` arm is unevidenced and untested in Variant 2.** Variant 2 says it is "defensive, not evidenced", and neither of its two test inputs exercises it. Variant 1's monkeypatch does.
- **Variant 2 is long.** It has a 12-row risk table where several rows are UNVERIFIED. A persona that preaches minimal change should be shorter.
- **Variant 1's long-term argument for C** (a later whole-installer root decision needs no change inside `install_plugins`) is better stated than Variant 2's, and I adopt it.

## Per-Point Verdicts

| Point | Winner | Evidence |
|---|---|---|
| S-001 | Variant 2 (low weight) | Frontmatter matches the brainstorm artifacts (seed-brief.md); the risk table is easier to review than prose bullets. Length is Variant 2's cost. |
| C-001 | Variant 2 | A NUL path raises `ValueError` from line 292 (orchestrator-verified on 3.11.15; Variant 2 also on 3.13.5). `install_mcp.py:739`, the precedent Variant 1 cites, catches `(OSError, ValueError, RuntimeError)`. |
| C-002 | Variant 2, merge one case | Real inputs are red on 3.10 to 3.12 (loop) and on all versions (NUL); Variant 1's real loop is never resolved because its wrapper intercepts. Add Variant 1's monkeypatched `OSError` case only if the `OSError` arm is kept untested otherwise. |
| C-003 | Variant 2 | `e.get("scope", "user")` preserves current behaviour for any unverified record shape; strict risks a repeated install attempt per run. Severity is low. |
| C-004 | Merge | Take Variant 1's setup (`CLAUDE_CONFIG_DIR` profile with a foreign `ironclaude`, no registry in `home`; maps to success criterion 3) plus Variant 2's `""` iteration and `SENTINEL` check. Under a faked `subprocess.run`, the foreign file is never read; the env assertions carry the test. |
| C-005 | Variant 2 (marginal) | It also asserts `CLAUDE_CONFIG_DIR` is absent from the marketplace-update env. Both pin that `plugin update`-only HTTPS settings do not leak. Both absence checks fail if the developer's shell exports `GIT_CONFIG_*`; add `monkeypatch.delenv` for those. |
| X-001 | Variant 2 | The real CLI always writes `scope`, so the outcome is non-fatal either way. The default-to-user choice keeps the diff to what the findings require; strict changes behaviour for an unproven shape. Low severity. |

## Shared Assumption Responses

- **A-002: QUALIFY.** The orchestrator's proof ran the real CLI with `CLAUDE_CONFIG_DIR` removed and `HOME` pinned in a throwaway home with no stored login, and the add and install succeeded. That is direct evidence that directory-source `marketplace add` and `plugin install` need no credentials from the user's profile. It does not cover `plugin update` on a GitHub-source plugin with credentials the user keeps in their own profile, or enterprise-managed marketplaces. The default marketplaces are public, `HOME` is unchanged in production so git credential helpers are unaffected, and every failure is reported without aborting (install_user_setup.py:403-413). The assumption holds for the default plugins; do not state it more broadly.
- **A-003: REJECT.** `docs/getting-started/installation.md:478-479` and `494-498` describe how the installer relates to `CLAUDE_CONFIG_DIR`, and the `[Unreleased]` #330 entry in `CHANGELOG.md` describes the plugin install. Option C changes where the plugin commands act for users who set the variable, so the doc sentence at line 478 and the note at 494 need a one-line update. Since #330 is still `[Unreleased]`, the update can amend that entry rather than add a release note. A code warning stays out of scope. If the docs edits count toward the edit limit, the change set passes 5 edits and the routing rule would send it through `/sc:workflow`; the planner should decide that explicitly.
