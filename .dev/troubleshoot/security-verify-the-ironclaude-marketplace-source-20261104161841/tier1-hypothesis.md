# Hypothesis: install_plugins trusts any marketplace named `ironclaude` (D1, :332) and queues the commands that depend on it before knowing whether `marketplace add/update` worked (D2, :347-374)

**Agent**: root-cause-analyst (lens), run by troubleshoot-analyst
**Tier**: 1
**Timestamp**: 2026-11-04T16:23:22Z (parent receipt time)
**Cause class**: Security
**Claim class**: `static_defect`
**Evidence class**: `runtime_repro`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: conflicts
runs-in=src/superclaude/cli/install_user_setup.py:332 @ local superclaude install/update process (throwaway HOME, fake claude CLI)

## Claim

Two separate defects. (a) D1: install_plugins checks only whether the name `ironclaude` is in known_marketplaces.json, never that its source is the IronClaude catalog directory; when the name is registered it skips `marketplace add` and runs `marketplace update ironclaude` and `plugin install ponytail@ironclaude` against whatever source owns that name, bypassing the sha pin. (b) D2: every `plugin install`/`plugin update` is queued before anything runs, and the loop only records failures, so a plugin command still runs after its marketplace command failed.

## Evidence

| # | Kind | Source | Content |
|---|------|--------|---------|
| E1 | `source_citation` | `src/superclaude/cli/install_user_setup.py:332-337` (D1) | `if name not in known:` queues the add; else `elif changed or stale:` queues `marketplace update`; nothing reads `known[name]["source"]`. |
| E2 | `source_citation` | `install_user_setup.py:347-352, 356-374` (D2) | installs/updates queued at :347-352; at :371-374 a non-zero exit only does `failed.append(name)` and the loop continues. |
| E3 | `executed_reproducer` | tier1-observation.md (parent capture, run=local repro, arm=failing @50123581) | case 1: foreign ironclaude → `ran: plugin marketplace update ironclaude`, `ran: plugin install ponytail@ironclaude`, report `✅ Plugins: installed ponytail@ironclaude`; case 2: add fails, `plugin install ponytail@ironclaude` still runs. |
| E4 | `documentation` | doc-context.md (installation.md:370-379; merged-requirements.md:36) | Ponytail only from IronClaude's pinned marketplace; "No other repo is accepted". |

Producer-citation check skipped: producers.md has no producer rows (trace observation); D1/D2 cited by file:line. No behaviour-definition row needed (relies only on the parent-measured entry shape and on non-zero exit codes, as :371 already does).

## Proposed Fix

One source file plus its test file.

1. D1, verify and refuse: helper `_is_our_catalog(entry, home)` true only when `entry["source"] == {"source": "directory", "path": <path resolving to home/_CATALOG_DIR>}`. If `ironclaude` is known and not ours, report `ironclaude (registered from another source; Ponytail not installed)`, drop the pinned plugins from `wanted`, clear `stale`; never remove or overwrite the user's marketplace. Otherwise keep add/update as today.
2. D2, skip dependents: commands carry their marketplace; when a `marketplace` command exits non-zero or raises, later commands for that marketplace are skipped and reported by name. The function still returns True on every path.

Tests: update `_pinned_home` to seed the real directory source; new `test_plugins_refuse_a_foreign_ironclaude_marketplace` (no ironclaude call, warning names the mismatch, known_marketplaces.json unchanged); new `test_plugins_skip_dependents_of_a_failed_marketplace` (fresh HOME with failing add: no ponytail install; pinned HOME with failing update: no plugin update); existing failure/time-limit test still passes.

## Confidence

Self-reported confidence: 0.9 (grounding 1.0, runtime check 1.0, symptom coverage 1.0, reproducibility 1.0, fix directness 0.5: several edit blocks plus a fixture change, domain coherence 1.0).

## Risks

- If Claude Code stored a differently normalized path, a real registration would look foreign; Ponytail is then skipped with a warning (fails closed).
- installation.md:370-379 does not mention the refusal; one sentence is optional.

## If I'm wrong, it's probably because...

Some Claude Code version writes a different source shape for directory marketplaces, so the strict check refuses real registrations.

## Falsification standard

After the fix, the repro's case 1 must not run `marketplace update ironclaude` or `plugin install ponytail@ironclaude`, and case 2 must not run `plugin install ponytail@ironclaude` after the failed add; on a real HOME after `claude plugin marketplace add <home>/.claude/ironclaude-marketplace`, `_is_our_catalog(known["ironclaude"], home)` must be True.

## Evidence classification

Claim class static_defect; evidence class runtime_repro (parent capture); runtime check by the parent; AFFIRM.

## Alternatives considered

- Rebind (remove then add): rejected, removal uninstalls the user's plugins and deletes their data.
- Stop the whole loop on the first failure: rejected, it blocks unrelated marketplaces.

## Grounding gaps

- What a real foreign ironclaude registration writes was not observed; the fix refuses anything that is not our directory.
- Proposed tests not yet run.
