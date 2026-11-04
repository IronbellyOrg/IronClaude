# Refactor Plan

## Overview

- Base: Variant 2 (sonnet:refactorer), `variant-2-sonnet-refactorer.md`
- Incorporated: Variant 1 (opus:architect), plus two orchestrator additions grounded in this session's verified facts
- Planned changes: 6
- Overall risk: Low (all additive to a spec document; no code is changed by this plan)

## Planned Changes

### Change 1: Finding-3 regression test uses Variant 1's scenario and a profile-aware fake

- Source: Variant 1, "Finding 3 / Regression test"; Variant 2, same section; orchestrator addition
- Target: base "Finding 3 / Regression test (new ...)"
- Approach: replace
- New content: test `test_plugins_run_claude_against_the_validated_home`. Setup: `CLAUDE_CONFIG_DIR` points at `tmp_path/"cfg"`, whose `plugins/known_marketplaces.json` holds a foreign `ironclaude` (`{"source": {"source": "github", "repo": "someone/ironclaude"}}`); `home = _plugin_home(tmp_path/"home", {"ponytail@ironclaude": True})` with no registry; `SENTINEL=kept` set. The fake `subprocess.run` resolves the profile the way the real CLI does (proven this session): `env = kwargs["env"] or os.environ`; `profile = env.get("CLAUDE_CONFIG_DIR") or env["HOME"] + "/.claude"`; it records `(command[1:], profile, env)`. Loop over `CLAUDE_CONFIG_DIR` = `cfg` and `""`. Assert: commands are `marketplace add <home>/.claude/ironclaude-marketplace` then `plugin install ponytail@ironclaude --scope user -y`; every recorded profile equals `str(home/".claude")`; `"CLAUDE_CONFIG_DIR" not in env`; `env["SENTINEL"] == "kept"`. Fails today: env is `None`, the fake sees `CLAUDE_CONFIG_DIR=cfg`, so the profile is the unvalidated foreign one.
- Rationale: debate C-004 (both advocates proposed this merge, 90%); Advocate 2's critique that a faked `subprocess.run` never reads the foreign profile is answered by making the fake resolve the profile like the real CLI.
- Risk: Low

### Change 2: Add Variant 1's rationale for option C

- Source: Variant 1, "Decision: Option C" (root of truth at `home`, line 303; the subprocess env at 392 is the only leak; a later whole-installer `CLAUDE_CONFIG_DIR` decision stays in one place)
- Target: base "Finding 3 / Decision: C", as an added rationale point
- Approach: append
- Rationale: Advocate 2 adopted it (round1-advocate-2.md, Concessions)
- Risk: Low

### Change 3: Docs and CHANGELOG (A-003 rejected by both advocates)

- Source: debate A-003; orchestrator read of docs/getting-started/installation.md:494-498 and CHANGELOG.md:18-29
- Target: base "Out of scope" (remove "Docs changes; none") and a new "Docs and CHANGELOG" subsection under "Convergence point and edit count"
- Approach: replace + insert
- New content: (a) one sentence added to the `CLAUDE_CONFIG_DIR` note at docs/getting-started/installation.md:494-498 saying the default plugins are installed with `claude plugin` commands run against `$HOME/.claude` too, so a Claude Code profile in `CLAUDE_CONFIG_DIR` does not get them; (b) a new `[Unreleased]` CHANGELOG entry (a separate `### Install: ... (#360 follow-ups)` section with `#### Fixed`) covering the three fixes and that behaviour. Docs and the CHANGELOG are not source files, so the code change stays at 3 edits in one source file plus its test file (direct change).
- Risk: Low

### Change 4: State A-002 as a known limit

- Source: debate A-002 (both QUALIFY)
- Target: base "Risks and edge cases", replace the "Auth stored under the user's CLAUDE_CONFIG_DIR" row
- New content: holds for the default plugins (local directory catalog, public GitHub marketplaces; proven with the real CLI in a throwaway profile with no login); a private marketplace needing a login kept only in the `CLAUDE_CONFIG_DIR` profile fails as a reported warning, never fatal.
- Risk: Low

### Change 5: Correct the base's overstatements and record verified facts

- Source: Advocate 1 weaknesses 3; orchestrator verification
- Target: base "Finding 2 / Rationale" and "Finding 3 / Decision" point 4, "Risks" pre-merge check
- New content: a non-list record value raises at line 329 only when it is not iterable (int, None); strings iterate and are filtered. Replace "I did not run claude" and the "Pre-merge manual check" with the orchestrator's real-CLI proofs (with `CLAUDE_CONFIG_DIR` removed and `HOME` pinned, the CLI wrote only under `HOME/.claude` and left the other profile untouched; a user-scope install beside a project copy succeeded and both records coexist).
- Risk: Low

### Change 6: Keep `GIT_CONFIG_*` absence checks deterministic

- Source: Advocate 2, C-005 note
- Target: base "Existing test impact", `test_plugins_move_ponytail_to_a_new_pin` row
- New content: add `monkeypatch.delenv("GIT_CONFIG_COUNT", raising=False)` before the run so the absence assertion does not depend on the developer's shell.
- Risk: Low

## Changes NOT Being Made

| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-002 | V1: monkeypatch `setup.Path.resolve` to raise | Patches `pathlib.Path` process-wide and tests a synthetic exception; the NUL input is red on every interpreter with no double (90%, conceded by Advocate 1) |
| C-003 / X-001 | V1: strict `scope == "user"` | Real records always carry `scope`, so finding 2 is covered either way; the default keeps today's behaviour for older record shapes and cannot cause a repeated install. Unresolved in debate (50%); decided in base-selection.md |
| S-001 | V1 prose layout | No effect on the fix |
| (none) | An `OSError`-forcing test case | The `OSError` arm stays as a documented defensive catch; adding a pathlib monkeypatch only to cover it reintroduces the rejected C-002 pattern |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 | Low | Test only | Revert test |
| 2-5 | Low | Spec text only | Revert text |
| 3 (applied later to docs/CHANGELOG) | Low | Docs only | Revert docs lines |
| 6 | Low | Test only | Revert one line |

## Review Status

Auto-approved (non-interactive), 2026-11-04T19:25:00Z.
