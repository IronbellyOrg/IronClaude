# Hypothesis: install_plugins trusts the `ironclaude` marketplace by name alone (:332) and cannot stop a plugin command once that plugin's marketplace command has failed (:321, :347-374)

**Agent**: root-cause-analyst (lens), run by troubleshoot-analyst
**Tier**: 2
**Timestamp**: 2026-11-04T16:27:01Z (parent receipt time)
**Cause class**: Security (missing source check plus missing dependency check)
**Claim class**: `static_defect`
**Evidence class**: `runtime_repro`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: conflicts
runs-in=src/superclaude/cli/install_user_setup.py:332 @ local superclaude install/update process (throwaway HOME, fake claude CLI)

## Claim

One root cause behind both halves: the command list does not record which marketplace each command depends on (:321) and the trust decision at :332 looks only at the key. A marketplace named ironclaude pointing anywhere gets `marketplace update` and `plugin install ponytail@ironclaude`, bypassing the pin; the loop at :356-374 has no link from a failed marketplace command to its dependent plugin commands.

## Evidence

| # | Kind | Source | Content |
|---|------|--------|---------|
| E1 | source_citation | install_user_setup.py:332-337 | `if name not in known:` add, else `elif changed or stale:` update; nothing reads `known[name]["source"]` |
| E2 | source_citation | install_user_setup.py:321, 347-352, 371-374 | commands hold no marketplace; installs/updates queued first; non-zero exit only `failed.append(name)` |
| E3 | executed_reproducer | tier1-observation.md (run=local repro, arm=failing @50123581) | case 1 foreign ironclaude → update + install, report ✅; case 2 add fails, install still runs |
| E4 | source_citation | install_user_setup.py:266-271 | `_read_json` returns {} on unreadable/unparsable file, so an unreadable known_marketplaces.json makes the add fail against an existing name and the install proceeds; only the dependency check closes this |

behaviour-definition: row 1 (directory source shape, observed this run).

## Proposed Fix

Agree with Tier 1 (helper `_is_our_catalog` + per-marketplace broken set) with four details: (a) compare resolved paths; (b) refusal branch before add/update; (c) carry the marketplace in each command tuple, check time limit first, then broken set, so `(time limit)` labels stay; (d) the dependency check must be at run time. Refusal message should say the user's own ironclaude marketplace blocks Ponytail (not "rerun to retry"). Tests: fixture `_pinned_home` seeds the real directory source; new refuse test (github source and `{}` entry; no ironclaude command; known file byte-identical); new skip-dependents test (add exits 1; update exits 1; add raises OSError); existing failure/time-limit test unchanged except the dependent label.

## Confidence

Self-reported confidence: 0.9 (grounding 1.0, runtime 1.0, coverage 1.0, reproducibility 1.0, fix directness 0.5, coherence 1.0).

## Risks

- Different path form or source shape in another Claude Code version → real registration refused (fails closed).
- Third-party marketplaces now report dependents as skipped instead of failing; report text changes, outcome does not.

## If I'm wrong, it's probably because...

Claude Code itself refuses to update/install from a marketplace whose source differs from settings, so only the second half would matter.

## Falsification standard

Repro case 1 must run no ironclaude command; case 2 no ponytail install after the failed add; on a real HOME `_is_our_catalog(known["ironclaude"], home)` must be True after our add.

## Evidence classification

static_defect; runtime_repro (parent capture); AFFIRM.

## Alternatives considered

- Not queuing pinned commands on failure: impossible, commands are queued before running.
- Remove and re-add the foreign marketplace: rejected (uninstalls the user's plugins).
- ironclaude-only guard: same size, misses failures on other marketplaces.

## Grounding gaps

- What a real foreign registration writes, and symlink canonicalization, not observed.
- Proposed tests not run.
