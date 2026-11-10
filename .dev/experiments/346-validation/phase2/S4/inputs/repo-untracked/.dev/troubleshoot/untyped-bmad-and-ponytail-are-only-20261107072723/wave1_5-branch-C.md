# Wave 1.5 Branch C: semantic-restriction extraction (returned by troubleshoot-analyst; persisted by parent, condensed to the load-bearing rows; quotes verbatim; paths relative to templates/VSCode-AIDev02/image/ unless starting .github)

Worker reported it read every row at the cited line. Parent re-verified the starred rows (*) during Wave 1.

- catalogue/bmad/install.sh:2-3 (applies_to BMAD install scope) "# Catalogue installer for bmad: verifies the image-baked `bmad` CLI and runs a per-repo / # `bmad install` into the seed repo (hidden via info/exclude). Run by startup in a subshell." *
- catalogue/bmad/install.sh:10 "SEED_PATH_FILE=\"${HOME}/.aidev/status/seed-repo-path\"   # AD-7: written only by startup §8" *
- catalogue/bmad/install.sh:20 "# Configure (AD-5), steps in order, stopping at the first exit." *
- catalogue/bmad/install.sh:22-25 no seed repo / non-git => "no seed repo recorded; nothing to configure"; existing `_bmad` or tracked bmad skills => "seed repo already has BMad ...; left untouched" *
- catalogue/bmad/install.sh:36 "# Snapshot after the excludes, so the check proves the install itself left git status alone"; lines 48-53 FAIL with exit 1 if git status changed *
- catalogue/bmad/install.sh:42 `NPM_CONFIG_OFFLINE=true timeout 120 bmad install --yes --directory "${D}" --modules bmm --tools claude-code --output-folder _bmad-output ...` (offline, 120 s cap, non-interactive; skills land in the repo's .claude/skills, not ~/.claude) *
- catalogue/bmad/manifest.yaml:7 "opt-in AI-driven agile-development scaffolder CLI"; :12-14 seed-repo-only welcome text with the manual command for other repos *
- catalogue/profiles.yaml:7 "Never hand-maintain the profile->slug mapping anywhere else"; :18 orca = [claude-code, orca, ironclaude, bmad, mcp-bundle-core]; :21 minimal = [claude-code] *
- catalogue/ironclaude/install.sh:3 "`superclaude install` into ~/.claude once per provenance git_sha"; :40-42 guards (git_sha, ~/.claude/CLAUDE.md must exist); :45-66 CLAUDE.md restored byte-for-byte; :100-135 settings.json hooks and symlink must survive; :139 "# ponytail: no lock against the parallel Orca settings.json writer (AD-3); a lost update self-heals next boot" (a code comment, not the plugin) *
- workspace_defaults/CLAUDE.md:5-9 ~/.claude/CLAUDE.md seeded copy-if-absent; only the SUPERCLAUDE_CODEGRAPH block is replaced every boot; :59-61 NFR12 secret rules take precedence
- scripts/startup.sh:192-195 per-user defaults seeded COPY-IF-ABSENT, user edits survive; :673-681 §8 only writer of seed-repo-path; :693-703 only `workspace` and `hybrid` scopes install at boot, project scope skipped; :705 and :1170 "BMad retains its original per-project installer invocation"; :1062-1066 a slug installs iff in-scope AND in the resolved profile set, set-but-unresolvable profile fails closed; :1114-1115 "BMad is an explicit owner-decision exception: its marker is never touched here" *
- scripts/lib/spec2-health.sh:99-112 BMAD health observes only the seed repo (`_bmad/_config/manifest.yaml` or tracked `.claude/skills/bmad-*`); :515-529 strict reader rejects a BMad row in the reprofile report; :539,562 deselected BMad is not-selected unconditionally
- Dockerfile.coder:133-144 BMad CLI baked image-wide, `bmad-method@6.9.0`; the runtime install is offline so anything BMAD needs at runtime must already be in the image; :284-312 IronClaude SHA is pinned only in the ARG (test-48 census)
- catalogue/README.md:119 `depends_on` MUST be empty at v1 (RAD-3, test-6); :171-185 every install.sh MUST (shebang/strict mode, tee to /tmp/catalogue-<slug>.log, marker only after verification, idempotent, subshell-safe, FAIL line); :297 "If any gate fails, fix the slug - do not relax the gate."
- catalogue/mcp-bundle-core/install.sh:32-61 precedent for user-global registration: never overwrites an existing user-scope entry; changes only via the claude CLI
- .github/contract-tests/test-57-catalogue-configure.sh:10-11 (bmad excluded, OD-1; runs offline `--network=none`), :324 clean seed git status stays empty, :335 second run byte-identical, :418 existing `_bmad/` leaves repo and info/exclude byte-unchanged, :450 "no seed: bmad writes nothing", :452 seedless BMad is healthy `Installed-not-Configured`
- .github/contract-tests/test-startup-boot.sh:2092 freshly cloned seed stays clean; :2209-2224 BMad with no seed expected `Installed-not-Configured`; :2482-2528 out-of-profile checks skip BMad
- .github/contract-tests/test-46-catalogue-health.sh:913-933 deselection never touches retained config, user project data or runtime artifacts ("bmad marker untouched")
- .github/contract-tests/test-19-catalogue-cli-presence.sh:198-204 verify-only vs runtime classifier for install.sh (a changed BMAD install.sh shape could be misclassified)

Worker conclusions (parent-checked against the rows above):
- A user-global-by-default install collides with: the profile gate (startup.sh:1062-1066 and profiles.yaml:7), the BMAD health/oracle design (seed repo only; test-57:450,452; test-startup-boot:2209-2224), and ~/.claude preservation rules (CLAUDE.md copy-if-absent; settings.json hook preservation).
- Creating BMAD directories in any repo on first use has no existing contract: install.sh targets only the seed path; git status must stay unchanged (needs exclude entries first); tests assert nothing is created without a seed.
- Ponytail: no slug, install script or constraint in scope; appears only as `# ponytail:` code comments.
- Not checked by worker: slug-configuration.md, test-48, full startup.sh. (Parent read slug-configuration/spec lines via Grep in Wave 1.5.)

Harness note: output tripped the instruction-shaped filter (settings-json); it held no directive to the parent; none followed.
