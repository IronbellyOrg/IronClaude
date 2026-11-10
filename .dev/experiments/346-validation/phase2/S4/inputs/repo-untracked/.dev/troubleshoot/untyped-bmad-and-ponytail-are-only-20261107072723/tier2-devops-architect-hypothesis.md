# Hypothesis: the ironclaude installer records "configured" even when the Ponytail plugin step failed or timed out, so no later boot retries it; BMAD stays an owner-decision item

**Agent**: devops-architect (lens only; dispatched as troubleshoot-analyst, read-only)
**Tier**: 2
**Timestamp**: 2026-11-07T07:43:28Z
**Cause class**: Config / env drift (boot-time install idempotency); BMAD half: Other (documented owner decision)
**Claim class**: `mixed`
**Evidence class**: `source_static`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned (BMAD half: OD-1 untouched; Ponytail: no governing document, `no_docs_found`)
runs-in=unknown

## Claim

Tier 1 is right that BMAD is a per-project owner decision; this card extends it on Ponytail. Under the Default profile, Ponytail reaches the user only through `superclaude install` inside the `ironclaude` slug. That step's plugin phase is non-fatal by design, but the installer still writes its `.configured` marker. The next boot takes the "already installed and configured; no-op" path, so a failed or timed-out plugin step is never retried while the image's git_sha is unchanged. The sticky marker is a real static defect; whether it caused this reporter's symptom is UNVERIFIED. Under Minimal, `ironclaude` is not selected, so Ponytail is absent by design.

## Evidence

- `/opt/uv/tools/superclaude/lib/python3.13/site-packages/superclaude/cli/install_user_setup.py:426-430` when any plugin failed, `install_plugins` returns `True, "...Plugins: not installed: ...; rerun superclaude install to retry"`; `:398-399` "time limit" when under 2 s remain; `:309` returns True and skips when `claude` is absent.
- `install_user_setup.py:436-444` one shared 30 s deadline (`_NETWORK_BUDGET`, :40) is spent first by `install_orca_skills`; on a first boot the plugin phase may get as little as about 5 s (UNVERIFIED that this happens).
- `superclaude/cli/main.py:269-280` exit code is 1 only if some step returned False; the plugin shortfall returns True, so `superclaude install` exits 0.
- `templates/VSCode-AIDev02/image/catalogue/ironclaude/install.sh:122-125` (non-zero exit is the only failure), `:140-141` (checks only help.md and hooks), `:143-149` (writes `.configured` = git_sha, then the marker), `:26-29` (`configured()` tests only the sha, help.md and hooks, never the plugin), `:32-35` (no-op exit 0 when configured), `:95-97`.
- `catalogue/ironclaude/manifest.yaml:24-25` health check is `superclaude --version`, which cannot see a missing plugin; `scripts/startup.sh:917-918` truncates `/tmp/catalogue-ironclaude.log` each boot, so the failure line is overwritten by the next boot's no-op line.
- A Grep of `.github/contract-tests` for `ponytail|plugin install|installed_plugins` found only `# ponytail:` code comments: no CI gate asserts Ponytail delivery. Producer-citation check: skipped (producers.md empty).
- behaviour-definition: row 1 (`claude plugin install --scope user`).

## Proposed Fix

In `catalogue/ironclaude/install.sh`, extend `configured()` with a plugin predicate that honours opt-out: true when `enabledPlugins["ponytail@ironclaude"]` in settings.json is not `true`, or when `~/.claude/plugins/installed_plugins.json` has a user-scope entry for it. With a missing plugin the next boot treats the install as not configured and runs a plain `superclaude install` (same sha, no `--force`); the plugin phase is idempotent and retries only what is missing.

Files to change:
- `templates/VSCode-AIDev02/image/catalogue/ironclaude/install.sh`: add the predicate to `configured()`.
- The ironclaude installer contract test: add one case "plugin missing, sha matches, installer reruns" (not located; `test-startup-boot.sh:2105,2136` handle the ironclaude marker).

Test to verify: the `.github` contract-test workflow for the new case. For the reporter's workspace: read `installed_plugins.json` and `/tmp/catalogue-ironclaude.log` (diagnosability-tasklist E-3).

BMAD (no code in this fix): an owner-approved first-use bootstrap would need: a user-level stub as trigger (boot section 9 only knows the seed repo, `bmad/install.sh:21-26`); the `info/exclude` plus before/after `git status` check (`bmad/install.sh:27-53`) and non-git handling; offline is satisfied (`Dockerfile.coder:139`, `install.sh:42`); `test-startup-boot.sh:2209,2223` stay green only if boot behaviour is unchanged. That decision is outside this fix.

## Confidence

Self-reported confidence: 0.55 (capped at 0.65: mixed, static, `runs-in=unknown`, no failing run captured).

Per-dimension self-assessment:
- Evidence grounding: 1.0: cited ranges read this pass, except test-57 lines.
- Runtime check: 0.5: nothing executed; "plugin step failed on the reporter's boot" is unverified.
- Symptom coverage: 0.5: Default-profile failure and Minimal explanation; BMAD documented, not fixed.
- Reproducibility fit: 0.5: control flow deterministic; failure trigger not observed.
- Fix directness: 0.5: direct for retry, cannot be shown to be the reporter's cause.
- Domain coherence: 0.5: boot idempotency plus separate policy domain.

## Risks

- Offline boots would rerun `superclaude install` (up to 60 s inside the 75 s bound, `startup.sh:1180`) on every boot; section 9 is a sequential loop (`startup.sh:1092`); whether it blocks the rest of startup is UNVERIFIED.
- Hardcoded plugin id: a rename (`_RENAMED_PLUGINS`, `install_user_setup.py:44`) would retry forever; derive ids from the defaults file or add a retry cap.
- The predicate must not break `test-startup-boot.sh` cases that stub `installed_plugins.json` as absent.

## If I'm wrong, it's probably because...

The reporter used the Minimal profile, or the plugin was installed and Claude Code did not load it in sessions that use a different config directory (e.g. Orca sessions). Both UNVERIFIED.

## Falsification standard

Read-only capture on an affected Default workspace with run/arm/command provenance: a user-scope `ponytail@ironclaude` entry in `~/.claude/plugins/installed_plugins.json` means the sticky marker did not cause the report (latent defect remains). Entry absent, `~/.aidev/installed/ironclaude.configured` equal to the provenance git_sha, and `ironclaude` in the resolved profile confirms the claim for that workspace. No preregistered outcome table exists.

## Evidence classification

- **Claim class**: mixed (control-flow defect is static; cause of the reporter's symptom is runtime/environment).
- **Evidence class**: source_static.
- **Runtime check performed?**: no.
- **If REFUTE verdict, coverage statement**: Not applicable (AFFIRM). Not inspected: the ironclaude installer contract test, `spec2-health.sh`, the Terraform `profile` parameter.

## Alternatives considered

- Tier 1's README-only fix: kept as complementary documentation; fixes no defect and does not deliver Ponytail.
- Adding `ironclaude` to Minimal: rejected (`profiles.yaml:19-21`, Minimal is Claude Code only).
- Raising `_NETWORK_BUDGET` or reordering Orca and plugins: rejected here; it changes upstream IronClaude, not this repo.

## Grounding gaps

- Diagnosability verdict: partial (see diagnosability-context.md). No failing boot captured; E-1 to E-3 pending.
- The reporter's profile and whether Ponytail loaded are unknown.
- The /opt/uv copy of superclaude may differ from the image's `IRONCLAUDE_GIT_SHA`; not checked.
- Not read: the ironclaude contract test, spec2-health.sh, test-57 lines.
