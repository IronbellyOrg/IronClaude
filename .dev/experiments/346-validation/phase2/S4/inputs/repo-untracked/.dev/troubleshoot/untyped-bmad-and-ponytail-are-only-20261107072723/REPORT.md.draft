# Troubleshoot Report

**Target**: Issue #478: BMAD and Ponytail are only accessible on projects where the user installed them earlier, are not installed by default on all projects or global to the user, and BMAD used in a never-installed project should create the directories it needs
**Type**: auto (deployment and config signals)
**Tier reached**: 2
**Confidence**: 0.58 (highest of four independently calibrated cards: Tier 1 0.58; Tier 2 root-cause 0.58, system-architect 0.58, devops 0.30)
**Status**: partial
**Escalation reason**: low_confidence
**Test is wrong**: false
**Behavior is documented**: true (BMAD half only; the Ponytail half is not established)
**Doc context card**: .dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/doc-context.md
**Duration**: 1627 seconds (from Wave 0 at 2026-11-07T07:27:23Z)
**Date**: 2026-11-07T07:54:30Z

---

## Summary

The reported issue is the documented behavior: a code change would regress the documented contract (BMAD half; the Ponytail half is not established). The owner decided on 2026-09-25 that BMAD is installed per project only, never globally or at user level, and the first-use creation of BMAD's directories inside a project has no owner ruling and sits next to documented non-goals (BMad in later clones and Orca worktrees; any BMad change under the gap-closure spec), so only the owner can change it. No unique cause of the reporter's Ponytail gap is established: no failing boot was captured, so whether the reporter used the Minimal profile or hit a failed plugin step is unobserved. This report does not fix any of the three asks; it recommends an owner decision plus documentation and keeps #478 open.

## Documentation Context

- **Relevant refs**: _bmad-output/specs/spec-orca-bundle-gap-closure/owner-decisions.md, _bmad-output/specs/spec-orca-bundle-gap-closure/.memlog.md, _bmad-output/specs/spec-orca-bundle-gap-closure/SPEC.md, _bmad-output/specs/spec-orca-catalogue-bundle/SPEC.md, templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml, docs/operations/upstream-monitor.md
- **Documented behavior**: BMAD is installed per project only; boot configures the seed repo; any other repo is a manual one-command install; no document governs Ponytail beyond docs/operations/upstream-monitor.md:62.
- **Restrictions honored**: no user-global BMAD, no BMAD change, offline install, git-clean install, profile gating.
- **Restrictions overridden**: None.
- **Card path**: .dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/doc-context.md

## Diagnosability Context

**Verdict**: partial
**Complexity classification**: trivial
**Captured-bytes (failing run)**: n/a

Existing instrumentation is an ephemeral /tmp log plus a health record that says Installed-not-Configured. The gap: no persistent record says which repo, profile or branch applied, and nothing records Ponytail activation. Consequence: the diagnosis rests on static code and owner-decision documents; runtime claims about the reporter's workspace stay UNVERIFIED.

(Full card: .dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/diagnosability-context.md)
(Tasklist (informational): .dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/diagnosability-tasklist.md)

## Diagnosis

**Root cause**: UNDETERMINED — producer menu unavailable (the symptom is a missing capability, not a value emitted by code, so no producer table exists)

**Cause class**: Other (the request conflicts with a documented owner decision); Ponytail residual: Config / env drift (profile gating), unconfirmed

**Established from direct reads (not a causal claim about the reporter):**
- BMAD is configured only in the seed repo at boot; with no seed repo the installer logs "nothing to configure" and still writes its marker.
- BMAD skills read their config from the project's own `_bmad/` directory.
- Ponytail has no code of its own in this repo; it arrives user-wide through IronClaude's plugin step, which the `ironclaude` slug runs; that slug is in the Default profile and not in Minimal.
- A failed or timed-out plugin step is reported but does not fail `superclaude install`, and the slug's "configured" check never looks at the plugin, so a later boot would not retry it (static reading only).

**Falsifiers** (copied from the tasklist; all pending, none executed: no access to the reporter's workspace):
- Optional E-1: reporter's `~/.aidev/status/seed-repo-outcome`; predictions: `skipped` or other (consistent with "BMAD never configured anywhere") versus `cloned` / `preserved-valid` (the seed repo was configured); informational, not a status prerequisite.
- Optional E-2: `configured_state` in `~/.aidev/status/spec2-health/bmad.health.v1`; `Installed-not-Configured` versus `Configured`; informational.
- Optional E-3: a user-scope `ponytail@ironclaude` entry in `~/.claude/plugins/installed_plugins.json`; present versus absent (then check the profile and `~/.aidev/installed/ironclaude`); informational. Absent plus `ironclaude.configured` equal to the provenance sha would confirm the sticky-marker defect for that workspace.

**Detailed explanation**: No discriminating run was captured this round, so no mechanism is asserted for the reporter's Ponytail gap.

## Evidence

1. `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:23` — `echo "[${SLUG}] no seed repo recorded; nothing to configure"` (no seed repo: nothing is configured, and the script still writes its marker at :58-60)
2. `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:42` — the only `bmad install` call targets `--directory "${D}"`, the seed repo path
3. `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml:12-14` — "If this workspace has a seed repo, BMad is already set up there ... For any other repo, run from its root:"
4. `_bmad-output/specs/spec-orca-bundle-gap-closure/owner-decisions.md:5` — "OD-1 BMad placement | **Cancelled.** BMad is installed per project only, never globally."
5. `_bmad-output/specs/spec-orca-bundle-gap-closure/.memlog.md:32` — "Owner 2026-09-25: BMad integration work is CANCELLED, because BMad must be installed per project and never globally or at user level."
6. `_bmad-output/specs/spec-orca-bundle-gap-closure/SPEC.md:77` — "Any BMad change (FR-6 and the BMad installer's marker and timeout). BMad stays a per-project seed install, exactly as #207 built it."
7. `_bmad-output/specs/spec-orca-catalogue-bundle/SPEC.md:174` — "Should BMad later reach Orca worktrees, through a tracked install or a worktree-create hook? That is a scope expansion; today it is a non-goal."
8. `templates/VSCode-AIDev02/image/catalogue/profiles.yaml:18` — `slugs: [claude-code, orca, ironclaude, bmad, mcp-bundle-core]`; `:21` — `slugs: [claude-code]` for Minimal
9. `templates/VSCode-AIDev02/image/scripts/startup.sh:1169` — `echo "[§9] slug=${aidev_cat_slug} out of profile '${aidev_profile}' — skipping install"`
10. `/opt/uv/tools/superclaude/lib/python3.13/site-packages/superclaude/cli/user_settings_defaults.json:36` — `"ponytail@ironclaude": true`
11. `/opt/uv/tools/superclaude/lib/python3.13/site-packages/superclaude/cli/install_user_setup.py:384` — `["plugin", "install", p, "--scope", "user", "-y"]`; `:398-399` — a plugin step is marked "time limit" when under 2 s remain
12. `/home/coder/.claude/plugins/installed_plugins.json:64-68` — `"ponytail@ironclaude"` recorded with `"scope": "user"` and version `5.3.3` on the diagnosing workspace
13. `templates/VSCode-AIDev02/image/catalogue/ironclaude/install.sh:26-29` — `configured()` tests only the git sha, the help file and the hooks, never the plugin; `:143-146` writes the `.configured` marker afterwards
14. `templates/VSCode-AIDev02/image/Dockerfile.coder:139` — `&& npm install -g bmad-method@6.9.0 \` (only the BMAD command-line tool is image-wide)
15. `.claude/skills/bmad-help/SKILL.md:25-26` — the BMAD help skill reads `{project-root}/_bmad/_config/bmad-help.csv` and runs `{project-root}/_bmad/scripts/resolve_config.py` (one skill; the other BMAD skills were not individually read)
16. `/opt/uv/tools/superclaude/lib/python3.13/site-packages/superclaude/cli/install_user_setup.py:426-431` and `:444` — failed plugin steps are reported but the step returns True, and the combined result is `all(ok ...)`, so `superclaude install` does not fail on a plugin shortfall (the `install.sh` exit-code path was not traced)
17. `docs/operations/upstream-monitor.md:62` — the only repository document naming Ponytail: a plugin pinned in IronClaude's own marketplace; `templates/VSCode-AIDev02` has no Ponytail code (every grep hit there is a `# ponytail:` comment tag)

## Proposed Fix

No causal fix is established for the reporter's Ponytail gap; next discriminating observation: E-3 (and E-1, E-2) on an affected workspace. Proposed handling of #478, documentation and decision only (it does not deliver any of the three asks):

1. Post this diagnosis on #478, split into three asks: global BMAD is declined by OD-1; first-use creation of BMAD directories in a project is an open owner decision (closely related to the catalogue-bundle SPEC.md:141,174 non-goal and scope-expansion text and to the gap-closure SPEC.md:77 non-goal "Any BMad change"; any decision superseding them should cite gap-closure SPEC.md:77 and `.memlog.md:32-33`); the Ponytail gap stays open pending E-1 to E-3. Ask the reporter for profile, whether a seed repo was set, and the boot outcome. Keep #478 open.
2. After the owner decides, add a short BMAD-scope note to `templates/VSCode-AIDev02/README.md` (for the Default profile, BMAD is configured automatically at boot only in the seed repo when the workspace has one; Minimal excludes BMad; any other repo needs the one-command install shown in `catalogue/bmad/manifest.yaml:12-14`, which the note should state by name because the image build context is not visible to workspace users) and reconcile README line 241, which lists BMad in the Default profile without saying where it is configured (line 308 is only a directory name and is left alone). Make no Ponytail delivery claim in the README until E-3 is observed. Keep the "upstream GitHub CLI release v" anchor listed at `.github/upstream-monitor/releases.json:113`, and keep the edit markdownlint-clean.

**Files to change**:
- `templates/VSCode-AIDev02/README.md` — BMAD-scope note and line 241 (after the owner decision only; leave the line 100 text "upstream GitHub CLI release v" untouched)

**Files that MUST NOT change** (documented behavior, asymmetric cost):
- `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh` and `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml` — changing BMAD toward global or any-repo setup reverses the 2026-09-25 owner decision (OD-1) and the related non-goals (gap-closure SPEC.md:77; catalogue-bundle SPEC.md:141,174)
- `.github/contract-tests/test-57-catalogue-configure.sh` and `.github/contract-tests/test-startup-boot.sh` — their oracles pin "no seed: bmad writes nothing" and `Installed-not-Configured`

**Test to verify**:
- The repo's `markdownlint` workflow on the README edit; read the three pending rows E-1 to E-3 on an affected workspace.

**Apply with**: the owner decision first, then the README edit by hand. No automatic remediation is offered because the status is partial.

## Alternative Fixes Considered

- **Modify the BMAD code to install globally or on first use** (from the architect card, Design 2: a user-level `bmad-init` skill). Rejected because **this is the DANGEROUS wrong answer** — it would silently reverse OD-1 and the related non-goals (gap-closure SPEC.md:77; catalogue-bundle SPEC.md:141,174) and break the "writes nothing" oracles; it is conditional on an owner decision and its user-level shell behaviour is UNVERIFIED.
- **Extend `configured()` in `catalogue/ironclaude/install.sh` so a missing user-scope Ponytail plugin triggers a retry** (devops card, calibrated 0.30). Not chosen: a real static gap, but no failing-run evidence it affected the reporter; kept as a conditional follow-up.
- **Add `ironclaude` to the Minimal profile.** Rejected: Minimal is defined as Claude Code only (`profiles.yaml:20-21`).

## Risk + Rollback

- **Likelihood of regression**: low in documentation. Medium if the README states mechanisms not yet observed (Ponytail), hence the instruction to omit that claim.
- **Test coverage of the changed code**: none for README prose (markdownlint only).
- **Rollback**: `git revert` of the README edit.

## Follow-up tasks

- Conditional on E-3 showing the plugin absent while `ironclaude.configured` equals the provenance sha: plan a change to `configured()` in `catalogue/ironclaude/install.sh` plus a contract-test case (more than five edits across several files; needs a written plan). Suggested type: bug.
- Make a repo-less BMAD boot visible: install.sh prints "install ok" and startup.sh:1184 prints "installed." even when nothing was configured, and the log in /tmp is truncated each boot. Suggested type: observability.

## Grounding Gaps

- No failing boot was captured; the reporter's profile, seed repo and boot outcome are unknown; E-1 to E-3 are pending.
- The auggie MCP was unavailable; grounding used Grep and Read, and codegraph does not index shell scripts or the Dockerfile.
- Documentation currency was not checked: every documentation file except the directly read owner decisions has verdict `unknown`.
- Whether bmad 6.9.0 can install skills at user scope is UNVERIFIED: `platform-codes.yaml` declares a `global_target_dir` for Claude Code but no consumer was found (behaviour-definitions row 2). User-level skill shell execution is UNVERIFIED (row 3).
- Validator rule A5 fired (consensus stated on a dynamic claim, "not retried on later boots", from static-only evidence); the claim is labelled static reading only, the consensus is limited to a documentation-only sequence, and the status stays partial.
- The independent review of fix F1 returned FAIL once (self-review.md); its blocking findings were applied to F1's wording before this report was drafted; see the Audit section for the re-review result.

## Next Steps

- Pending rows (all informational, none executed): read E-1, E-2, E-3 on an affected workspace and record the values with provenance; E-3 absent plus `ironclaude.configured` equal to the provenance sha would confirm the sticky-marker defect for that workspace (then plan the `configured()` change).
- Owner decision needed: confirm that global BMAD stays declined and decide whether first-use creation in a project should become a new requirement.
- Remediation offer not made: the report status is partial and the remediation chain is offered only for a success report.

## Audit

- **Hypothesis cards**: .dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/tier1-hypothesis.md, tier2-devops-architect-hypothesis.md, tier2-root-cause-analyst-hypothesis.md, tier2-system-architect-hypothesis.md
- **Adversarial artifacts** (Tier 2 only): Not invoked: no two strong competing fixes (see candidate-fixes.md)
- **Self-review** (Tier 2 only): review 1 FAIL (blocking findings applied to F1), see self-review.md; review 2 returned FAIL with two minor wording findings (the line 308 reading and the unconditional "seed repo only" wording, both applied), see self-review-2.md; no third review run
- **Evidence validation**: .dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/evidence-validation.md (29 citations verified, 0 dropped; rule A5 fired; suggested status partial)
- **Audit log**: .dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/audit.log

## Pipeline Hardening Closure

Pipeline hardening not applicable: HC0 decided applicable=false. Boundary scan: CLI or subprocess (startup.sh runs the slug installer; `superclaude install` runs the `claude` CLI) was read as evidence only and no fix at it is established; file, stdin or prompt delivery: none; generated-artifact parser: none; gate or severity enum: none; duplicated evaluator: none; persisted state (the `.configured` marker): read only; review or audit selector: none; sibling pipeline: none. Revisit if the sticky-marker follow-up is adopted.
