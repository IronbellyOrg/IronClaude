---
claim_class: mixed
evidence_class: runtime_repro
verdict_direction: AFFIRM
---
# Hypothesis: refactor-find emits a stale downstream handoff with an invalid report-list prefix
**Agent**: root-cause-analyst
**Tier**: 1
**Cause class**: Other: downstream handoff contract mismatch
**Consistency with docs**: conflicts
runs-in=src/superclaude/cli/swarm/reduce.py:672 @ local worktree .venv

## Claim
The refactor-find handoff does not match an available downstream command's complete input contract. Its lens supplies unavailable `/sc:code-review --apply`, while the CLI prepends literal `<existing-review>` to successful report paths. The production CLI with stub reviewers emitted both defects; changing only the command name would leave a nonexistent input in the recommendation.

## Evidence
- Producer P1, `src/superclaude/cli/swarm/lenses/refactor_find.py:53`: `recommended_next_command_template=("/sc:code-review --apply {compare_files}")`.
- `src/superclaude/cli/swarm/commands.py:2143`: `",".join(["<existing-review>", *succeeded_final_paths])`; `src/superclaude/cli/swarm/reduce.py:672-697` renders the substitution and stores it.
- `.dev/troubleshoot/bug-swarm-refactor-find-recommends-unavailable-20261123170314/stub-run/return-contract.yaml:64` contains `/sc:code-review --apply <existing-review>,` followed by three actual final report paths. `tier1-observation.md:18-37` captures CLI exit 0, literal prefix, three readable files and valid candidate input shape; :8-11 captures packaged/installed command absence.
- `docs/dev/lens-contribution-policy.md:287-292` requires an existing command; `/home/coder/.claude/skills/sc-adversarial-protocol/SKILL.md:60-62` accepts 2-10 existing readable files. behaviour-definition: row 1 in behaviour-definitions.md, fetched from the local installed governing contract and quoted in tier1-observation.md under Behaviour definitions. Input compatibility is declared/documented, not claimed as a completed replacement run.

## Proposed Fix
Recommend existing `/sc:adversarial --compare` with only successful final reports. Scope substitutions to refactor-find, preserve explicit caller substitutions and suspect=False, and emit no executable comparison suggestion when the default report count is outside 2-10. Proposal only, not applied or executed.
- `src/superclaude/cli/swarm/lenses/refactor_find.py`: replace stale template.
- `src/superclaude/cli/swarm/commands.py`: supply refactor-find-specific real list, leaving sibling handoffs unchanged.
- `docs/swarm/lens-catalog.md:25,49`: update duplicate recommendation.
- New regression checks in `tests/swarm/test_commands_run.py` and `tests/swarm/test_bundled_lenses.py`: command/flags, successful readable inputs, no placeholder, input count, caller precedence and unchanged sibling behavior. Include rejected default counts; not written or run.

## Confidence
Self-reported confidence: 0.50 at worker receipt, before parent behavior-definition binding. This historical self-score is not independent calibration; the required row is now bound. Defective output itself is reproduced.
- Evidence grounding: 1.0, live source and captured command agree.
- Runtime check: 1.0, captured production CLI ran with stub reviewers, exit 0.
- Symptom coverage: 1.0, explains unavailable command and invalid argument list.
- Reproducibility fit: 1.0, current local .venv and captured run.
- Fix directness: 0.5, candidate input checked, replacement and patch not executed.
- Domain coherence: 1.0, recommendation generation only.

## Risks
Global compare_files changes could alter bare-review and reflect handoffs. Preserve bodies, experimental status, suspect=False and suggestion-only execution. No downstream source modification is authorized.

## If I'm wrong, it's probably because...
An unobserved external provider implements the exact namespaced command and literal prefix, unlike the captured packaged/installed environment.

## Falsification standard
An unchanged-live-lens, production-CLI three-success run with no explicit substitution override would falsify the mechanism if its contract instead named an available command with supported flags and only the three actual report paths.

## Evidence classification
Claim class mixed: source-defined handoff, executed interpolation and documented input rules. Evidence class runtime_repro: parent-captured local-cli-stub-1, not execution by this worker. Runtime checked for original recommendation only, not replacement or fix.

## Alternatives considered
Missing installation alone does not explain absent packaged command plus literal prefix. No new command needed solely to preserve stale template.

## Grounding gaps
Diagnosability partial in diagnosability-context.md: event timing incomplete, actual disputed artifact captured. Behavior-definition row 1 is bound before calibration; it proves declared input requirements, not replacement execution. Original reporter environment, replacement execution, path quoting and failed-worker acceptance UNVERIFIED. Baseline 76 tests passed; no new test or paid review ran.
