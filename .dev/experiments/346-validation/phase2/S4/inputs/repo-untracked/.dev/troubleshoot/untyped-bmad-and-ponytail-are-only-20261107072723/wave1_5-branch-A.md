# Wave 1.5 Branch A: release-doc lookup (returned by troubleshoot-analyst; persisted by parent, condensed; quotes as returned)

release_slug: orca-catalogue-bundle-2026-09-24 (issue #204; under _bmad-output/, not .dev/releases). Related: v2-m2 and v2-m3 under .dev/releases/current/.
confidence: 0.9
summary: The reported behaviour is the designed behaviour of the orca-catalogue-bundle spec (issue #204). BMad was scoped to the seed repo only, with no user-level or global install and no creation of directories on other projects. No artifact scopes a global Ponytail install.

artifact_paths (repo-relative):
- _bmad-output/specs/spec-orca-catalogue-bundle/SPEC.md (CAP-3 seed repo only; line 141 non-goal: "BMad in repos cloned after boot and in Orca-created worktrees"; line 174 open question; line 65 no seed repo -> exit 0, writes nothing)
- _bmad-output/specs/spec-orca-catalogue-bundle/slug-configuration.md (bmad section lines 48-50, 154-157 incl. "No seed" row)
- _bmad-output/specs/spec-orca-catalogue-bundle/.memlog.md (owner decisions: line 50 non-goal; line 66; lines 95-96 owner "may later ask")
- _bmad-output/planning-artifacts/architecture/architecture-Coder-orca-catalogue-bundle-2026-09-24/ARCHITECTURE-SPINE.md (AD-5 lines 100-114; AD-7 lines 133-141; line 228 deferred; line 63; lines 152-153)
- _bmad-output/implementation-artifacts/1-4-seed-repo-is-bmad-ready-and-git-clean.md
- _bmad-output/implementation-artifacts/1-3-ironclaude-configured-in-every-session.md
- .dev/releases/current/v2-m3/TDD_V2_M3.md (profile model; Appendix C line 1392 row appears stale vs story 1-4, unchecked)
- .dev/releases/current/v2-m2/tasks/T1-bmad.md
- _bmad-output/specs/spec-aidev02-v2/catalogue-slugs.md (line 19 earlier scope `project`, superseded by hybrid)
- docs/operations/upstream-monitor.md (line 62, only Ponytail doc)

Worker gaps/notes:
- No PRD/TDD/spec states a requirement that Ponytail be installed or enabled globally, or that BMad be user-level. Ponytail half has no governing doc in this repo.
- BMad installs per project only (`_bmad/` plus `.claude/skills/bmad-*`). Spec's route for other projects is the manual one-command path.
- The issue's second sentence contradicts SPEC.md line 141 and ARCHITECTURE-SPINE.md:228; fixing it needs an owner decision and updates to those documents, AD-5/AD-7, slug-configuration.md rows 154-157, and the bmad entries in test-19, test-52 and test-startup-boot.
- Not found: nothing in .dev/releases/current beyond v2-m2/v2-m3; .dev/tasks/to-do empty; no done package for BMAD/Ponytail install.
- Worker did not read profiles.yaml, README, startup.sh, Dockerfile.coder (parent did in Wave 1).

Parent verification of the load-bearing citations is recorded in tier1-observation.md addendum (below) once read.
