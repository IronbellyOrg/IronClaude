# Documentation Context Card

**Generated**: 2026-11-07T07:33:00Z
**Wave**: 1.5
**Scope**: (none)

## Release context

- **Release**: orca-catalogue-bundle-2026-09-24 (issue #204), plus owner decisions of 2026-09-25 in spec-orca-bundle-gap-closure
- **Artifacts**: _bmad-output/specs/spec-orca-catalogue-bundle/SPEC.md, _bmad-output/specs/spec-orca-catalogue-bundle/slug-configuration.md, _bmad-output/specs/spec-orca-catalogue-bundle/.memlog.md, _bmad-output/planning-artifacts/architecture/architecture-Coder-orca-catalogue-bundle-2026-09-24/ARCHITECTURE-SPINE.md, _bmad-output/specs/spec-orca-bundle-gap-closure/owner-decisions.md, _bmad-output/specs/spec-orca-bundle-gap-closure/.memlog.md, _bmad-output/specs/spec-orca-bundle-gap-closure/SPEC.md, _bmad-output/planning-artifacts/prds/prd-Coder-orca-bundled-catalogues-2026-09-24/prd.md
- **Summary**: BMAD is deliberately a per-project install. The seed repo is configured at boot; every other repo is a manual one-command install; BMAD in other clones or worktrees is an explicit non-goal (SPEC.md:141, :174). An earlier requirement for user-level BMAD (#205 PRD FR-6, OD-1=A) was cancelled by the owner on 2026-09-25: "BMad is installed per project only, never globally" (owner-decisions.md:5; .memlog.md:32). No document in this repo governs Ponytail as a product beyond docs/operations/upstream-monitor.md:62.
- **Confidence**: 0.9 (worker) ; parent re-read SPEC.md:65,141,174, .memlog.md:50,95-96, owner-decisions.md:5, gap-closure .memlog.md:27,32-34, SPEC.md:77

## Architectural docs consulted

- `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml` (code/manifest, read directly) — documents seed-repo-only setup and the manual command for other repos.
- `templates/VSCode-AIDev02/image/catalogue/ironclaude/manifest.yaml` — IronClaude is user-global (~/.claude).
- `docs/operations/upstream-monitor.md` — verdict: `unknown` — only doc naming Ponytail: a plugin pinned in IronClaude's own marketplace (line 62).
- `docs/operations/aidev02-operator.md`, `templates/VSCode-AIDev02/README.md`, `templates/VSCode-AIDev02/image/catalogue/README.md`, `docs/diagrams/startup-sections.md`, `docs/architecture.md`, `docs/component-inventory.md` — verdict: `unknown` — profiles and boot order; silent on BMAD seed-only scope and on Ponytail.

> CAUTION: every doc above is `unknown` per the Section 2 currency check (no mtime metadata collected, no header markers); treat their claims as advisory. The owner decisions in `_bmad-output/specs/` were read directly with line citations.

## Restrictions / decisions that constrain the fix

- `_bmad-output/specs/spec-orca-bundle-gap-closure/owner-decisions.md:5` (BMAD placement) — "OD-1 BMad placement | **Cancelled.** BMad is installed per project only, never globally."
- `_bmad-output/specs/spec-orca-bundle-gap-closure/SPEC.md:77` (non-goal) — "Any BMad change ... BMad stays a per-project seed install, exactly as #207 built it."
- `_bmad-output/specs/spec-orca-catalogue-bundle/SPEC.md:141,174` (scope) — BMAD in later clones/worktrees is a non-goal and "a scope expansion".
- `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:22-25,36-53` — seed repo only; existing `_bmad` untouched; git status must be unchanged.
- `.github/contract-tests/test-57-catalogue-configure.sh:450,452` and `test-startup-boot.sh:2209-2224` — "no seed: bmad writes nothing"; seedless BMad is `Installed-not-Configured`.
- `templates/VSCode-AIDev02/image/scripts/startup.sh:1062-1066` and `catalogue/profiles.yaml:7` — a slug installs only in-profile; profile mapping lives only in profiles.yaml.
- `templates/VSCode-AIDev02/image/catalogue/ironclaude/install.sh:40-66,100-135` — user-global `~/.claude` writes must preserve CLAUDE.md and settings.json hooks.

## Re-frame signals

- The BMAD half of the report IS the documented, owner-decided behavior: BMAD is per-project and never global; a code change toward global-by-default would reverse a documented owner decision (2026-09-25), so the route is an owner decision and spec change, not a silent code change.
- The second ask (BMAD creating its directories on first use in any project) is not user-level, but it is also not covered by any spec: the spec treats BMAD outside the seed repo as a non-goal and the installer, health check and contract tests assume nothing is created without a seed. It would be a scope expansion needing an owner decision.
- The Ponytail half is not governed by any document in this repo; by code it is delivered user-globally through IronClaude's defaults whenever the `ironclaude` slug installs (Default profile, not Minimal); whether it loads on a given boot is UNVERIFIED.
