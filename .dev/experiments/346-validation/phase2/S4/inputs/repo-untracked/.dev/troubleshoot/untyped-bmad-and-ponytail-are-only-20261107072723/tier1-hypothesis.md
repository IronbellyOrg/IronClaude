# Hypothesis: #478 asks to reverse or extend a documented owner decision for BMAD (per-project only, never global) and, for Ponytail, hits a profile gate (delivered user-wide only through the ironclaude slug in the Default profile); no code defect is established

**Agent**: root-cause-analyst (lens only; dispatched as troubleshoot-analyst, read-only)
**Tier**: 1
**Timestamp**: 2026-11-07T07:37:35Z
**Cause class**: Other (request conflicts with a documented owner decision); Ponytail residual: Config / env drift (profile gating)
**Claim class**: `mixed`
**Evidence class**: `source_static`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned (BMAD half: matches owner decisions; Ponytail half: no governing document, `no_docs_found`)
runs-in=unknown

## Claim

BMAD is not installed globally and is not auto-created in unseen projects because the owner decided so on 2026-09-25 ("BMad is installed per project only, never globally"). The slug configures only the seed repo; any other repo needs the manual one-command install. Ponytail has no code of its own in this repo: it is delivered user-wide (`--scope user`) as a side effect of `superclaude install`, which the `ironclaude` slug runs; that slug is in the Default profile but not in Minimal. The BMAD half of the report therefore asks to reverse, or newly extend, a documented decision and needs an owner decision, not a code fix. The Ponytail half is a defect only for Minimal-profile workspaces or a failed or timed-out plugin step; neither is verified.

## Evidence

- E1 `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:21-26,40-42,57-60`: directory comes from `~/.aidev/status/seed-repo-path`; with none it logs "no seed repo recorded; nothing to configure" and still writes the marker; the only `bmad install` call is `--directory "${D}"`. `catalogue/bmad/manifest.yaml:12-14`: manual command for any other repo. `bmad-method/tools/installer/commands/install.js:14-37`: `--directory`, `--modules`, `--tools`, `--yes`; no user-scope option. behaviour-definition: row 2.
- E2 `_bmad-output/specs/spec-orca-bundle-gap-closure/owner-decisions.md:5`: "OD-1 BMad placement | **Cancelled.** BMad is installed per project only, never globally."; `.memlog.md:32` ("Owner 2026-09-25: BMad integration work is CANCELLED ... OD-1=A is void."); `_bmad-output/specs/spec-orca-catalogue-bundle/SPEC.md:141,174` (non-goal / scope expansion); `.github/contract-tests/test-57-catalogue-configure.sh:450,452` ("no seed: bmad writes nothing"; `Installed-not-Configured`).
- E3 `superclaude/cli/main.py:236` calls `install_user_setup`; `install_user_setup.py:437-443` runs `install_plugins`; `user_settings_defaults.json:36,52-70` enables `ponytail@ironclaude` pinned to `DietrichGebert/ponytail` v5.3.3; `install_user_setup.py:384` runs `claude plugin install <p> --scope user -y`. Observed outcome on this workspace: `/home/coder/.claude/plugins/installed_plugins.json:64-70` user scope v5.3.3; `/home/coder/.claude/settings.json:327`. behaviour-definition: row 1.
- E4 `catalogue/profiles.yaml:18` (Default includes ironclaude) and `:21` (Minimal = `[claude-code]`); `scripts/startup.sh:1158-1169` skips slugs outside the resolved profile; `catalogue/ironclaude/install.sh:88-90,143-146` skips `superclaude install` once the configured sha matches and records it; `install_user_setup.py:392-410` treats a plugin step as non-fatal and "time limit" when under 2 s remain of the 30 s budget. A failed plugin install is not retried on later boots (static reading only).
- Producer-citation check: skipped. `producers.md` has a header-only table and `producer-count: n/a` (symptom is a missing capability, not an emitted categorical value).

## Proposed Fix

One fix, no product-code change. Treat #478 as an owner-decision item: post this diagnosis on the issue and ask the owner to confirm OD-1 for the BMAD half, or to supersede it explicitly. If the owner wants first-use creation of BMAD directories, that needs a new spec because it is a scope expansion today. Once the owner confirms, add a short "Where BMAD and Ponytail are available" paragraph to `templates/VSCode-AIDev02/README.md`: BMAD: seed repo automatic, other repos by the one-command install; Ponytail: delivered through the `ironclaude` slug, Default profile only.

Files to change: `templates/VSCode-AIDev02/README.md` only.

Test to verify: the repo's `markdownlint` workflow on the doc edit. For Ponytail, read-only checks on an affected workspace: E-3 in `diagnosability-tasklist.md`, plus `/tmp/catalogue-ironclaude.log`.

## Confidence

Self-reported confidence: 0.6 (capped at 0.65: static evidence, run site unknown, `locus_unknown`).

Per-dimension self-assessment:
- Evidence grounding: 1.0. Every cited line was read in this pass.
- Runtime check: 0.5. Mixed claim, static evidence, `runs-in=unknown`, nothing executed.
- Symptom coverage: 0.5. Covers all three asks; which scenario the reporter hit is unknown.
- Reproducibility fit: 0.5. No repro; static diagnosis.
- Fix directness: 0.5. The fix is a decision plus docs; it does not deliver what the reporter asked for.
- Domain coherence: 1.0. Fits the owner decisions, profile gating and plugin scope.

## Risks

- If the owner wants BMAD to bootstrap on first use, this fix only documents the status quo and #478 stays open.
- The docs edit must not contradict `test-57` and the `Installed-not-Configured` semantics.
- Calling Ponytail "already delivered" would be wrong if the reporter's Default-profile workspace hit the plugin-step failure in E4.

## If I'm wrong, it's probably because...

The reporter was on a Default-profile workspace where the plugin step silently failed (network failure or the shared 30 s budget), and the sticky configured marker stopped any retry: a real defect in the `ironclaude` install path and a second candidate fix.

## Falsification standard

The "Ponytail is delivered under Default" half is falsified if, on an affected Default-profile workspace, `~/.claude/plugins/installed_plugins.json` lacks a user-scope `ponytail@ironclaude` entry while `~/.aidev/installed/ironclaude.configured` equals the provenance `git_sha` (a captured read with run, arm and command provenance). The "BMAD half is by design" half is falsified by a later owner statement that supersedes OD-1 (owner-decisions.md:5, .memlog.md:32).

## Evidence classification

- **Claim class**: mixed. BMAD half is a documented contract; Ponytail half depends on a profile config value and unverified runtime outcomes.
- **Evidence class**: source_static. Source and owner-decision documents were read; nothing executed.
- **Runtime check performed?**: no. The worker cannot execute; a fresh workspace boot cannot be driven from here.
- **If REFUTE verdict, coverage statement**: Inspected: `bmad/install.sh`, `bmad/manifest.yaml`, `profiles.yaml`, `startup.sh:1150-1184`, `ironclaude/install.sh:1-145`, `ironclaude/manifest.yaml`, `main.py:215-264`, `install_user_setup.py:1-70,285-445`, `user_settings_defaults.json:25-71`, the owner decisions and `SPEC.md:138-142,172-175`. Not inspected: `Dockerfile.coder:133-144,283-353` and `startup.sh` section 8 (parent read these in Wave 1); how Claude Code discovers `~/.claude/skills` for user-level BMAD; whether bmad 6.9.0 can install skills at user scope (declared `global_target_dir`, no consumer found: UNVERIFIED); whether the `/opt/uv` copy of superclaude matches the image's `IRONCLAUDE_GIT_SHA`; the Terraform `repo_url` and `profile` parameters.

## Alternatives considered

- User-level BMAD install (old OD-1=A): rejected; void per `.memlog.md:32`; `install.js:14-37` has no user-scope option (a `global_target_dir` key is declared in `platform-codes.yaml:57` with no consumer found: UNVERIFIED whether usable).
- User-global first-use bootstrap running `bmad install` in the current directory: not rejected on technical grounds, but outside the spec (`SPEC.md:141,174`) and contradicts the `test-57` "writes nothing" cases, so it needs an owner decision first.
- Ponytail as a code defect (sticky plugin-step failure): plausible, no failing-run evidence; kept as the "if I'm wrong" candidate. The reporter may also simply have used Minimal.
- Adding `ironclaude` to Minimal: rejected; Minimal is defined as "Claude Code only" (`profiles.yaml:20`).

## Grounding gaps

- Diagnosability verdict: partial (see `diagnosability-context.md`). No captured failing boot; which branch ran, which profile, and whether Ponytail loaded are UNVERIFIED; E-1 to E-3 in `diagnosability-tasklist.md` stay pending.
- The reporter's environment (Default or Minimal profile, seed repo or not) is unknown.
- Documentation currency was never checked: every doc except the directly read owner decisions is `unknown`.
- auggie MCP was unavailable in this session; grounding used Grep/Read.
