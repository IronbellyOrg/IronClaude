# Hypothesis: a plan-time-only source check trusts a successful `marketplace add` as proof of binding, and a refused workspace may keep a foreign-sourced ponytail@ironclaude without an accurate report

**Agent**: security-engineer (lens), run by troubleshoot-analyst
**Tier**: 2
**Timestamp**: 2026-11-04T16:27:59Z (parent receipt time)
**Cause class**: Security
**Claim class**: `mixed`
**Evidence class**: `source_static`
**Verdict direction**: `AFFIRM` (extends Tier 1)
**Consistency with docs**: conflicts (installation.md:370-376)
runs-in=src/superclaude/cli/install_user_setup.py:332 @ local superclaude install/update process (throwaway HOME, fake claude CLI)

## Claim

Agree with D1 and D2. The Tier 1 check runs once against the snapshot read at :305; on the add path it records `known[name] = {}` (:335) and trusts that the add bound ironclaude to our directory. If the add exits 0 while a different source keeps the name, the pin is bypassed with no failure for D2 to catch. Separately, when the check refuses, an already-installed foreign-sourced ponytail@ironclaude stays enabled, so "Ponytail not installed" would be false.

## Evidence

| # | Kind | Source | Content |
|---|------|--------|---------|
| E1 | source_citation | install_user_setup.py:305, 332-335 | registry read once; `known[name] = {}` placeholder; no re-read after add |
| E2 | source_citation | install_user_setup.py:266-271 | unreadable registry reads as {} |
| E3 | source_citation | install_user_setup.py:304 vs install_mcp.py:721-726 | plugin registry path hard-coded to home/.claude/plugins while CLAUDE_CONFIG_DIR is honoured elsewhere |
| E4 | source_citation | install_user_setup.py:312-319, 353-354; user_settings_defaults.json:36 | refusal drops ponytail from wanted; an existing foreign install stays active |

behaviour-definition: row 2 (add on a taken name, observed this run by the parent after the card was returned).

## Proposed Fix

Tier 1 refusal + dependent-skip, plus a post-add/post-update re-read gate before pinned plugin commands, and a refusal message that names an already-installed copy.

## Confidence

Self-reported confidence: 0.55 (runtime 0.5: CLI behaviour on a taken name not observed by the worker; coverage 0.5; reproducibility 0.5).

## Risks

- Gate refuses a real registration if paths resolve differently (fails closed).
- With CLAUDE_CONFIG_DIR set the gate still reads home/.claude.

## If I'm wrong, it's probably because...

`marketplace add <dir>` always exits non-zero or rebinds when the name is taken, so the post-add gate adds nothing.

## Falsification standard

Discriminator: post-add binding of ironclaude. A: add exits 0 while the entry stays foreign. B: add exits non-zero or rebinds to our directory. Observable: `add_exit == 0 AND source.path != <home>/.claude/ironclaude-marketplace`. Reference-context value: n/a (first instrumented run). Outcome: true → A consistent, B refuted; false → A refuted, B consistent.

**Parent probe result (tier1-observation.md, Discriminator probe)**: add exited 0 and the entry now points at `<home>/.claude/ironclaude-marketplace` → observable false → A refuted for Claude Code 2.1.318, B consistent (rebinds).

## Evidence classification

mixed; source_static; no runtime check by the worker.

## Alternatives considered

- TOCTOU as an attack boundary: rejected (needs ~/.claude write access).
- extraKnownMarketplaces.ironclaude takeover: would appear in known_marketplaces.json and be caught by the source check.

## Grounding gaps

- CLAUDE_CONFIG_DIR plugin-state location not verified.
