# Hypothesis: #478's BMAD "create directories on first use" ask is an unruled per-project feature gap, not a reversal of the 2026-09-25 owner decision; separately, a failed Ponytail plugin install is invisible and never retried; neither is shown to be the reporter's cause

**Agent**: root-cause-analyst (lens only; dispatched as troubleshoot-analyst, read-only), independent second pass
**Tier**: 2
**Timestamp**: 2026-11-07T07:43:28Z
**Cause class**: Other (unruled request) plus Missing verification (success reported without proof of the plugin)
**Claim class**: `mixed`
**Evidence class**: `source_static`
**Verdict direction**: `REFUTE` (of the Tier 1 sub-claim "BMAD half = reversal of a documented decision, no defect"; the no-code-fix outcome for the reported symptom still stands)
**Consistency with docs**: aligned (matches SPEC.md and the owner decisions; README is silent on BMAD scope)
runs-in=unknown

## Claim

OD-1 cancels BMAD "globally or at user level". It does not rule on creating `_bmad/` inside the current project on first use. That ask is per-project, so it fits OD-1. SPEC.md calls it a non-goal "today" and lists it as an open question, so it is an unanswered feature request. The "global" ask is still declined by OD-1, and no later document supersedes it. Independently, nothing verifies Ponytail after `superclaude install`, and nothing retries a failed plugin step on later boots. This has not been shown to have caused the report.

## Evidence

- `_bmad-output/specs/spec-orca-bundle-gap-closure/owner-decisions.md:5`: "OD-1 ... **Cancelled.** BMad is installed per project only, never globally." `.memlog.md:32-33`: "never globally or at user level"; the BMad slug keeps #207's per-project seed behaviour. This forbids global and user-level install; it says nothing about first-use creation in a project.
- `_bmad-output/specs/spec-orca-catalogue-bundle/SPEC.md:141`: BMad in later clones and worktrees is a non-goal because the excluded `_bmad/` is untracked. `:174`: "Should BMad later reach Orca worktrees ... That is a scope expansion; today it is a non-goal." An open question, not a decision.
- Search for later statements, all negative: `CHANGELOG.md` has one BMad hit (line 232, SpecStory removal); `docs/` has no placement statement; the post-2026-09-25 files in `_bmad-output/` that were checked mention BMad only in passing (`spec-specstory-removal/SPEC.md:79`, the 2026-10-26 brainstorm, `micro-first-owner-questions-brief-2026-11-02.md`). Closed issues #204 and #216 appear only in `.dev/issues/478/scout-create.md:32,37`; their bodies were not read.
- Seedless BMAD is reported honestly: `bmad/install.sh:21-26,57-60` logs "nothing to configure" and still writes the marker; `test-57-catalogue-configure.sh:449-452` pins "writes nothing" and `Installed-not-Configured`; the welcome text (`bmad/manifest.yaml:12-14`) is conditional ("If this workspace has a seed repo"), not a false promise; `startup.sh:1184` prints "installed." for a seedless run (cosmetic).
- Ponytail, re-derived: `install_user_setup.py:384` runs `plugin install ... --scope user`; `:322-327` ignores project-scope copies; observed `/home/coder/.claude/plugins/installed_plugins.json:64-71` has `ponytail@ironclaude` at scope user v5.3.3. Failure path `:426-431`: failed plugin steps are reported but the function returns True, and `main.py:236` does not turn that into an exit code. `ironclaude/install.sh:26-29` (`configured()`) and `:140-151` never check the plugin. `spec2-health.sh:76,88-97` requires only command, hook and provenance. Static reading only.
- behaviour-definition: rows 1 and 2 (behaviour-definitions.md). Row 2 leaves user-scope BMAD capability UNVERIFIED.
- Producer-citation check: skipped (producers.md header-only).

## Proposed Fix

Add one section, "Where BMAD and Ponytail are available", to `templates/VSCode-AIDev02/README.md` (BMad appears there only at lines 241 and 308, so BMAD scope is undocumented). It would state: BMAD is configured automatically in the seed repo only, any other repo needs the one-command `bmad install`, first-use auto-creation is not built; Ponytail arrives user-wide through the `ironclaude` slug in the Default profile only, not in Minimal. This documents behaviour already in code and manifest, so it needs no owner gate. The same issue comment should split #478 into three: the global ask is declined per OD-1; per-project first-use bootstrap is a new decision on SPEC.md:174; a Ponytail install check is conditional on the measurements below.

Files to change: `templates/VSCode-AIDev02/README.md` only. Test to verify: the `markdownlint` workflow; check the text against `test-57`.

## Confidence

Self-reported confidence: 0.55 (below the 0.65 cap for static, unlocated evidence).

Per-dimension self-assessment:
- Evidence grounding: 1.0: every cited range read in this pass.
- Runtime check: 0.5: nothing executed; `runs-in=unknown`.
- Symptom coverage: 0.5: reporter's profile, seed repo and boot outcome unknown.
- Reproducibility fit: 0.5: no repro, no failing boot.
- Fix directness: 0.5: documents; delivers none of the three asks.
- Domain coherence: 0.5: owner-decision policy plus plugin and health path.

## Risks

- If the owner wants first-use bootstrap, docs-only leaves #478 open.
- The README text must not contradict the `Installed-not-Configured` semantics in `test-57`.
- Calling Ponytail "delivered" is wrong if the reporter's Default workspace hit the silent plugin failure.

## If I'm wrong, it's probably because...

The reporter was on Minimal, or on a Default workspace where the plugin step failed, so Ponytail was never installed. Then the real fix is code in the `ironclaude` path and health, which is more than five edits and needs a written plan.

## Falsification standard

On an affected Default workspace, a captured read finds no user-scope `ponytail@ironclaude` in `installed_plugins.json` while `~/.aidev/installed/ironclaude.configured` equals the provenance sha: that confirms the independent defect and falsifies "Ponytail delivered under Default". The doc claim is falsified by a dated post-2026-09-25 owner statement that forbids per-project auto-creation or supersedes OD-1.

Inert read-only probes for the parent (run/arm/command provenance to be recorded): `~/.claude/plugins/installed_plugins.json` key `ponytail@ironclaude`; `~/.aidev/installed/ironclaude.configured`; `/tmp/catalogue-ironclaude.log` for a "Plugins: not installed" line.

## Evidence classification

- **Claim class**: mixed (BMAD part documented contract; Ponytail part static code path).
- **Evidence class**: source_static.
- **Runtime check performed?**: no.
- **If REFUTE verdict, coverage statement**: Searched `CHANGELOG.md`, `docs/`, `_bmad-output/` and `.dev/` for BMad statements dated after 2026-09-25. Not inspected: bodies of #204, #216 and #432 on GitHub, `Dockerfile.coder`, and whether bmad 6.9.0 can install at user scope (`global_target_dir` declared, no consumer found: UNVERIFIED). Any of these could flip the verdict.

## Alternatives considered

- Tier 1's owner-decision gate for the README text: rejected; documenting current behaviour needs no decision, and the first-use ask is not covered by OD-1.
- A fix to the ironclaude `configured()` check and health requirements: not chosen; a real static gap with no failing-run evidence, spanning `ironclaude/install.sh`, `spec2-health.sh` and several tests.
- A user-level BMAD install: rejected per OD-1, and BMAD skills read `{project-root}/_bmad` (tier1-observation.md), so a user-level install would not help another project.

## Grounding gaps

- Diagnosability verdict: partial (diagnosability-context.md). No failing boot captured.
- The reporter's profile and seed repo are unknown.
- This session shows a Ponytail mode banner in a non-seed worktree: weakly suggests the user-scope plugin loads; mechanism UNVERIFIED.
- auggie unavailable; codegraph does not index shell or Dockerfiles.
