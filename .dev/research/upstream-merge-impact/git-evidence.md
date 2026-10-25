# Local Git evidence

Snapshot HEAD: 053b75664c8979bf223b8040f68310dce882d05b
Window: 2025-10-23T00:00:00Z <= committer date < 2026-10-24T00:00:00Z.
Repository shallow: false

## Explicit upstream merge commits

Merge 0ceb29553c2ba42efc3c55d1ec9402f8087b7773; author date 2026-02-13T16:54:27-05:00; committer date 2026-02-13T16:54:27-05:00
Subject: Merge branch 'SuperClaude-Org:master' into master
First parent: f3ba7c21cb3fb68d2fae4f1be13cffbe88312555
Upstream second parent: 55c658c77f88c538cf9d90a3736c1b24f8f64f44
Newly reachable upstream commits: 55c658c77f88c538cf9d90a3736c1b24f8f64f44
Net files: src/superclaude/cli/install_mcp.py

Merge 1e8c6e1622e157f36f44792e41f667399edb2a79; author date 2026-03-06T10:22:09-05:00; committer date 2026-03-06T10:22:09-05:00
Subject: Merge branch 'SuperClaude-Org:master' into master
First parent: e60e844ed733069398516d00f4b0af5597fbf9ce
Upstream second parent: b061b2f7b00ca33d66c10b666c15016873b2e094
Newly reachable upstream commits: b061b2f7b00ca33d66c10b666c15016873b2e094
Net files: .github/workflows/pull-sync-framework.yml, scripts/sync_from_framework.py

## Base history and external author classification

External-author candidate 51a8e11840bdce59a41379bc0159ecc4f3765469 (Claude <noreply@anthropic.com>): NOT in either explicit upstream parent ancestry; subject: feat(skills): add sc-crash-recovery for post-crash work-state diagnosis
Full commit metadata follows:
commit 51a8e11840bdce59a41379bc0159ecc4f3765469
Author:     Claude <noreply@anthropic.com>
AuthorDate: Sun May 17 02:58:39 2026 +0000
Commit:     Claude <noreply@anthropic.com>
CommitDate: Sun May 17 02:58:39 2026 +0000

    feat(skills): add sc-crash-recovery for post-crash work-state diagnosis
    
    Fans parallel subagents across pipeline artifacts, recent Claude Code session
    logs, serena memory, git status, and auggie semantic sweeps to produce a
    structured "where was I, what's in-flight, what to resume" report.
    
    Built per Developer Guide patterns: allowed-tools safety boundary, refs/ for
    lazy-loaded reference material, STOP-on-invalid-input contract, and explicit
    tool-failure fallback matrix. Read-only diagnosis — proposes resume commands
    but never executes them.
    
    Pipeline knowledge covers PRD, TDD, spec/research, roadmap, tasklist, sprint,
    and MDTM task layouts with their canonical resume idioms.
    
    Supports single-project mode (default, current cwd) and fleet sweep across
    all /config/workspace/ projects with --all flag.
    
    Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>

External-author candidate 93cb9758e3638fe395663bcef255f6151bed0779 (Claude <noreply@anthropic.com>): NOT in either explicit upstream parent ancestry; subject: feat(commands): add review-translation command for localization QA
Full commit metadata follows:
commit 93cb9758e3638fe395663bcef255f6151bed0779
Author:     Claude <noreply@anthropic.com>
AuthorDate: Sun Feb 1 04:52:16 2026 +0000
Commit:     Claude <noreply@anthropic.com>
CommitDate: Sun Feb 1 04:52:16 2026 +0000

    feat(commands): add review-translation command for localization QA
    
    Adds comprehensive localization review command with:
    - Chain of thought context analysis (audience, use case, tone)
    - Parallel sub-agent deployment for multi-file review
    - Adversarial validation with research-backed evidence
    - Individual per-language reports with scoring matrix
    - Project summary with prioritized task list
    - Implementation path for applying fixes
    
    https://claude.ai/code/session_01JhPm26WEUV15d8rT1irmYZ

Upstream in-window commits already present before February merge: 45
Upstream in-window commits introduced by named February/March merges: 2

First eight fork-owned commits by Git reverse traversal:
9a38d894a0539743d7f2e7a38a36042957312dc0 2026-01-27T06:50:59+00:00 RyanW <ryan@ironbelly.com> Initial commit with IRonbelly Improvements
f33c41e1c46e077289a0da53823adc39454da304 2026-01-27T11:46:08+00:00 RyanW <ryan@ironbelly.com> IBv1.4 M1-M2
ef4dfd5fb8409438c01b08c180be6c4af51f4f58 2026-01-27T12:16:53-05:00 Ironbelly <ryan@ironbelly.com> Merge pull request #1 from ironbelly/Ironbelly/IBv1.4
034477824391041927e5fa14ba25ca8766c78efc 2026-02-01T04:56:23+00:00 RyanW <ryan@ironbelly.com> Monolithic roadmap skill
4ed8d70f264d5db9a0910e1270e2825cd51bb8e0 2026-02-01T05:15:15+00:00 RyanW <ryan@ironbelly.com> feat(commands): enhance review-translation with TQAS improvements
8eaa601da1cb2fe31dbe7e5ce415c8007bba77ea 2026-02-01T05:26:23+00:00 RyanW <ryan@ironbelly.com> test(review-translation): add unit test suite for localization QA command
a26ce4a3eacdfcee6f9f821fe71b22c818bb93a3 2026-02-01T00:34:58-05:00 Ironbelly <ryan@ironbelly.com> Merge pull request #3 from ironbelly/claude/review-steam-localization-9iy2K
b37b0cbfe0f738c2d803d801930ffccb1bbb5919 2026-02-13T20:18:00+00:00 RyanW <ryan@ironbelly.com> docs(v1.05): M1 foundation - dependency graph, validation baseline, token measurements

## Local remote refs and pending sync
refs/remotes/origin/HEAD b0bd8c8b8bbefbd6b9ca36fadc8ec9cba8f244d3
refs/remotes/origin/ReflectInTaskList e6ebacc5241e548dee38cbabca978772abb5b80e
refs/remotes/origin/brainstorm/t2-bare-reviewer-adjunct 757a382493440e77f71608dd135fbc48061614db
refs/remotes/origin/chore/ci-followup-sync-guard-readme 053b75664c8979bf223b8040f68310dce882d05b
refs/remotes/origin/chore/preserve-retired-worktree-artifacts 58b80aaeda3be4894c46780854652b39b30a7cf7
refs/remotes/origin/chore/sprint-progress-report-template 99bdf77d588a73dbf4cb84ec02095ec945e80f0b
refs/remotes/origin/claude/task-builder-template-review-rqaq63 ea581323a07a76b35656caa00aa0c0770c0ded0f
refs/remotes/origin/docs/ataraxy-labs-eval-plan-remediation 4f4a2134c82e032b1bdae789f4fca2676bfd17d1
refs/remotes/origin/docs/auggie-review-workflow-implement-plan afa3e16469cb932db7c4219dda2e303d7db1b77f
refs/remotes/origin/docs/ccsession-model-tiers 13d246ec9e0d5aad4b6ea70529bebd9496a776e5
refs/remotes/origin/docs/pr-submit-command-ci-preflight cd031eda272681c40f34db268dc93b5dd3b09a4b
refs/remotes/origin/docs/routing-consolidation 8694e3f19ed6a3454dfb4db662187113938841a1
refs/remotes/origin/feature/artifact-keeper f997863ea8ba0b902cf6d95e1955cd7760e6d1a4
refs/remotes/origin/feature/auggie-review-revagent 417d1ca21869464a6de9ddf8bc63fa5786caa9fb
refs/remotes/origin/feature/ccsession-native-install 06585002af47df46b31a5e81c5ffd644f05839a3
refs/remotes/origin/feature/implement-retry-ladder b542a9ff71cd4a73dfbd62aae6d4098aefe58db0
refs/remotes/origin/feature/pr-submit-ci-monitor 2bbb910d43b28897b303ca80e85663d0b9c00607
refs/remotes/origin/feature/prd-spec-flag ff1a3f10d864d8404807b44ee95295f988f671d7
refs/remotes/origin/fix/ccsession-auth-token c09a61c6c0442cf3ddbb2ab92cf465910f14c6e3
refs/remotes/origin/fix/ccsession-grok-4-7 123d8c1ea4d14417da44d96974932504c42a949e
refs/remotes/origin/fix/claude-process-stdin-large-prompts 2c2127940bdc6456dc881cde9522b034dd5ef0cb
refs/remotes/origin/fix/eval-doc-tests 9d62a723c98dc3b856ee04a9d319c8f4594abeea
refs/remotes/origin/fix/implement-session-confirmation 2a94c921d8b9bc2a7760ba0e62414b8d6904c5aa
refs/remotes/origin/fix/pr-submit-attended-ci-monitor d5200729eefd055467750dfa4a41b8c7a5aa09d1
refs/remotes/origin/fix/pr-submit-augment-no-response 4d383c9d6cf85656626ec3dc13a8cf7fe7a9961b
refs/remotes/origin/fix/restore-eval-docs 8b2cc3053629aa34d1bc097e7cd4650ffd4aba43
refs/remotes/origin/fix/troubleshoot-readonly-analysts 04e191962da52fd95c9532e173ea0cb462f4264e
refs/remotes/origin/master b0bd8c8b8bbefbd6b9ca36fadc8ec9cba8f244d3
refs/remotes/origin/reflectWrapper 879bb64f635b4244352549ec4cf9a19ab7326de0
refs/remotes/origin/sync/framework d3cf593808f5e5df12da7f0c3e506556fdc34e01
refs/remotes/pr270 74ead45033e02a98727d34b887d4f5599ad454f4

origin/master: b0bd8c8b8bbefbd6b9ca36fadc8ec9cba8f244d3; ancestor of HEAD=False; HEAD ancestor of ref=True
Commits unique to ref relative to HEAD:
b0bd8c8b8bbefbd6b9ca36fadc8ec9cba8f244d3 2026-10-23T01:39:57-04:00 Ironbelly Merge pull request #282 from IronbellyOrg/fix/troubleshoot-readonly-analysts
b41f32525c9065a6ff242135a3ed51a30629ca21 2026-10-23T01:25:29-04:00 Ironbelly Merge pull request #281 from IronbellyOrg/chore/ci-followup-sync-guard-readme
04e191962da52fd95c9532e173ea0cb462f4264e 2026-10-23T05:11:08+00:00 Ryan wiancko fix(troubleshoot): restrict native diagnostic workers

origin/sync/framework: d3cf593808f5e5df12da7f0c3e506556fdc34e01; ancestor of HEAD=False; HEAD ancestor of ref=True
Commits unique to ref relative to HEAD:
d3cf593808f5e5df12da7f0c3e506556fdc34e01 2026-10-23T05:26:18+00:00 github-actions[bot] chore: automated sync and namespace isolation from framework [2026-10-23 05:26]
b41f32525c9065a6ff242135a3ed51a30629ca21 2026-10-23T01:25:29-04:00 Ironbelly Merge pull request #281 from IronbellyOrg/chore/ci-followup-sync-guard-readme

## Author counts for in-window upstream ancestry
{"Baran Acar": 1, "BlackBear": 1, "Cedric Hurst": 1, "Gurdas Nijor": 1, "Sergei Frolov": 4, "Utakata": 3, "Yuxin Liu": 1, "kazuki": 2, "kazuki nakai": 5, "mithun50": 27, "smartdddlab": 1}

## Per-record unit and strict reverse check

### foundation-migration: Python architecture migration and legacy removal
3 records; 268 distinct paths

c733413d3c5dc0ea93822e93afbe3eae9a7f6fec | authored=2025-10-29T13:45:15+09:00 | committed=2025-10-29T10:15:15+05:30 | kazuki nakai | Proposal: Create `next` Branch for Testing Ground (89 commits) (#459) | strict_reverse_rc=1
10844490e2609a61ec201e073872428bac9f9470 | authored=2025-11-09T14:41:29+09:00 | committed=2025-11-09T14:41:29+09:00 | kazuki | Update Makefile and add uninstall script | strict_reverse_rc=1
ab0bb0f57dff3e1a751e72e8f0bf9b1ea9699211 | authored=2025-12-12T22:09:50+07:00 | committed=2025-12-12T22:09:50+07:00 | kazuki | fix: remove duplicate uppercase docs paths for macOS compatibility | strict_reverse_rc=0

### installer-packaging: Installer, update command, wheel resources and installation entry points
12 records; 76 distinct paths

8c0559ca9a99a14c7337b48e888959b47dc8acb8 | authored=2025-11-11T18:21:22+01:00 | committed=2025-11-11T18:21:22+01:00 | mithun50 | feat: add comprehensive test suite, CI/CD workflows, and install command | strict_reverse_rc=1
ad80f57f63eeae02af6b283ec35ae6f9aa68fcf0 | authored=2025-11-11T18:37:03+01:00 | committed=2025-11-11T18:37:03+01:00 | mithun50 | feat: Change installation directory to ~/.claude/commands/sc/ | strict_reverse_rc=1
25785363af21849898ca77624aac0b05fc780b94 | authored=2025-11-13T12:21:47+01:00 | committed=2025-11-13T12:21:47+01:00 | mithun50 | feat: add update command to CLI | strict_reverse_rc=1
c6e72825b4feb6ba37facabef868865e11c5ae45 | authored=2025-11-13T15:03:11+01:00 | committed=2025-11-13T15:03:11+01:00 | mithun50 | fix: include commands in package distribution | strict_reverse_rc=1
2847f7551871eb17d2821730be0adc39cba9666a | authored=2025-11-13T15:05:53+01:00 | committed=2025-11-13T15:05:53+01:00 | mithun50 | docs: explicitly include commands and skills in MANIFEST.in | strict_reverse_rc=1
81343a678bc6011ac8410b95b4f29a6d91749b3d | authored=2025-11-13T15:35:03+01:00 | committed=2025-11-13T15:35:03+01:00 | mithun50 | feat: include all plugin resources in package distribution | strict_reverse_rc=1
42946f8445f13f4444aa67ecb1f503ed6d91eb79 | authored=2025-11-13T15:37:56+01:00 | committed=2025-11-13T15:37:56+01:00 | mithun50 | fix: prioritize package location for commands path resolution | strict_reverse_rc=0
18c0e4e127dc352db19ae132a770019bf1f32d8a | authored=2025-11-14T11:33:04+09:00 | committed=2025-11-14T08:03:04+05:30 | BlackBear | Add missing install.sh script (#483) | strict_reverse_rc=1
fd8c67f6f0be47371fe9fffce0be0ffad73b3c72 | authored=2025-11-14T14:15:44+01:00 | committed=2025-11-14T14:16:19+01:00 | mithun50 | chore: bump version to 4.1.9 and add __init__.py to all packages | strict_reverse_rc=1
9ca48494021325defc117145a7f38634852b27b6 | authored=2025-11-14T14:22:48+01:00 | committed=2025-11-14T14:22:48+01:00 | mithun50 | fix: simplify wheel build configuration to prevent ZIP archive errors | strict_reverse_rc=1
074b99480db9ffe7f2f86a5cbd7a96f13843410c | authored=2025-11-14T14:34:23+01:00 | committed=2025-11-14T14:34:23+01:00 | mithun50 | feat: include plugins directory in wheel distribution | strict_reverse_rc=1
323137a9df985c17f221f559ccede9860d40cb23 | authored=2025-11-14T14:40:24+01:00 | committed=2025-11-14T14:40:24+01:00 | mithun50 | feat: include src and plugins folders in wheel package | strict_reverse_rc=0

### quality-ci: CI, publication, lint and formatting changes
5 records; 26 distinct paths

32c0086d0f916362fd4899212e8e714511ca4524 | authored=2025-11-12T17:59:29+01:00 | committed=2025-11-12T17:59:29+01:00 | mithun50 | fix: correct package paths in publish-pypi workflow | strict_reverse_rc=1
43bfa0aa0211ce2a7797a4e1748e92103d1d8f1a | authored=2025-11-12T18:09:37+01:00 | committed=2025-11-12T18:09:37+01:00 | mithun50 | fix: add --system flag to uv pip install in workflows | strict_reverse_rc=1
8da05a172063d16e062a0bfabf583debc9be385c | authored=2025-11-12T18:12:57+01:00 | committed=2025-11-12T18:12:57+01:00 | mithun50 | fix: use direct commands instead of uv run with --system | strict_reverse_rc=1
e2896335ba82f83a0b1a271cb872ff04b7ea884b | authored=2025-11-12T18:17:39+01:00 | committed=2025-11-12T18:17:39+01:00 | mithun50 | fix: resolve all ruff linting errors | strict_reverse_rc=1
b00547ad535ee638952c5e38b2a139888e50f496 | authored=2025-11-12T18:19:45+01:00 | committed=2025-11-12T18:19:45+01:00 | mithun50 | style: apply ruff formatting to all files | strict_reverse_rc=1

### docs-memory-releases: Memory documentation, translations, reference docs and release metadata
14 records; 30 distinct paths

bea4bfe289f298e790da4746212474d3ed2b0ed8 | authored=2025-10-30T22:14:35-05:00 | committed=2025-10-31T08:44:35+05:30 | Cedric Hurst | docs: Replace Mindbase References with ReflexionMemory (#464) | strict_reverse_rc=1
bec0b0c3e393cb5bc244e83b95fb2b006745eeb5 | authored=2025-11-12T01:30:49+09:00 | committed=2025-11-11T22:00:49+05:30 | Utakata | Claude/fix readme plugin docs 011 cv2 lk n gko6wzm tfn dmnrm (#478) | strict_reverse_rc=1
a3541f43c5e95cae669c0d666a6fc68808de8fde | authored=2025-11-12T17:37:27+01:00 | committed=2025-11-12T17:37:27+01:00 | mithun50 | feat: bump version to 4.1.7 across all files | strict_reverse_rc=1
16caa49442f477febd4b2a8e32dd1ded705d02d3 | authored=2025-11-12T18:04:34+01:00 | committed=2025-11-12T18:04:34+01:00 | mithun50 | fix: update package version and authors | strict_reverse_rc=1
58008c94446386718f036cc402f2dc4e99b3f007 | authored=2025-11-12T18:25:34+01:00 | committed=2025-11-12T18:25:34+01:00 | mithun50 | docs: fix broken links in translated READMEs | strict_reverse_rc=1
61591211ae99847130aed3e84737bfa63b3b6520 | authored=2025-11-13T12:36:38+01:00 | committed=2025-11-13T12:36:38+01:00 | mithun50 | chore: bump version to 4.1.8 | strict_reverse_rc=1
86a26333912b09a98fab1d9a81c0cd23e404f224 | authored=2025-11-13T12:45:17+01:00 | committed=2025-11-13T12:45:17+01:00 | mithun50 | fix: update __version__ in __init__.py to 4.1.8 | strict_reverse_rc=1
d2a3b58b6f62302a9d3e4c09d3d8cb26bd209d8d | authored=2025-11-13T12:46:52+01:00 | committed=2025-11-13T12:46:52+01:00 | mithun50 | chore: update VERSION file to 4.1.8 | strict_reverse_rc=1
d11abead403e4de8438f008a468f98ca10e5472e | authored=2025-11-13T14:24:00+01:00 | committed=2025-11-13T14:24:00+01:00 | mithun50 | docs: sync translated READMEs with main README structure | strict_reverse_rc=1
43ca81d1693b1ecfc6648531798e29224cb305c3 | authored=2025-11-14T14:45:58+01:00 | committed=2025-11-14T14:45:58+01:00 | mithun50 | docs: update test solutions and mistake logs | strict_reverse_rc=1
310136c16b95c9dd5c412c5e7b5d4ae76362dbf6 | authored=2025-12-02T16:57:20-08:00 | committed=2025-12-03T06:27:20+05:30 | Gurdas Nijor | Add "Run in Smithery" badge (#490) | strict_reverse_rc=1
208c66e1a781376a85132087b5a99767a9f13e31 | authored=2026-01-18T04:37:51+01:00 | committed=2026-01-18T09:07:51+05:30 | Sergei Frolov | docs: update commands.md - complete command reference (#512) | strict_reverse_rc=1
1bd92c91fd78cd528f2b0211460e3e1f9dedfcb5 | authored=2026-01-18T14:09:18+01:00 | committed=2026-01-18T18:39:18+05:30 | Sergei Frolov | chore: bump version to 4.2.0 (#514) | strict_reverse_rc=1
ad6b2e9982d978b02f301ce81ea3a89183cbb5c8 | authored=2026-01-18T15:20:16+01:00 | committed=2026-01-18T19:50:16+05:30 | Sergei Frolov | docs: update version references and fix CHANGELOG for v4.2.0 (#515) | strict_reverse_rc=1

### commands-framework: Recommendation command, restored primitives and explicit boundaries
4 records; 217 distinct paths

0ef8ea8139202acb17c5ffc938619f331c7184ab | authored=2025-11-09T16:37:20+03:00 | committed=2025-11-09T19:07:20+05:30 | Baran Acar | feat: new command sc:recommend add. (#477) | strict_reverse_rc=1
ab8904bc8cc2291b347a8641b913099f699f0c91 | authored=2025-11-13T15:54:16+01:00 | committed=2025-11-13T16:08:56+01:00 | mithun50 | feat: restore all 30 slash commands with comprehensive documentation | strict_reverse_rc=1
3762d6ab24508107dc794811d9b6b0c9def84707 | authored=2025-11-13T16:16:05+01:00 | committed=2025-11-13T16:16:05+01:00 | mithun50 | feat: restore complete SuperClaude framework from commit d4a17fc | strict_reverse_rc=1
e61aaba771055f65dd7c4f5de4d0e3e91ac928ec | authored=2026-01-18T13:53:50+01:00 | committed=2026-01-18T18:23:50+05:30 | Sergei Frolov | feat(commands): add explicit boundaries and handoff instructions (#513) | strict_reverse_rc=1

### mcp-installation: MCP gateway, server descriptors, encoding and February bug fix
9 records; 14 distinct paths

5a68595835256815c19b8fde256722f4dc687dd5 | authored=2025-10-25T19:42:47+09:00 | committed=2025-10-25T16:12:47+05:30 | kazuki nakai | fix: update airis mcp gateway installer (#460) | strict_reverse_rc=1
67449770c0157372f276c16f99f0a935de1b1125 | authored=2025-10-28T13:18:58+09:00 | committed=2025-10-28T09:48:58+05:30 | Utakata | docs: Confirm AIRIS MCP Gateway installation URL is correct (#463) | strict_reverse_rc=128
1b14d065378163809c027873454eaa38cc6a108b | authored=2025-11-13T16:29:10+01:00 | committed=2025-11-13T16:29:10+01:00 | mithun50 | added mcp command fixed some issues | strict_reverse_rc=1
202660b52451d0680969c3fbb1042cb52539d35a | authored=2025-12-13T11:00:18+09:00 | committed=2025-12-13T07:30:18+05:30 | kazuki nakai | feat(mcp): add Airis Agent and MindBase MCP servers (#497) | strict_reverse_rc=1
6ae5e9987736dab9908260d392f1a6c89b2dcde4 | authored=2025-12-16T00:48:01+09:00 | committed=2025-12-15T21:18:01+05:30 | kazuki nakai | docs: add AIRIS MCP Gateway as unified installation option (#499) | strict_reverse_rc=1
04c9b85cd0c2ed774f397bcc39f21a56178c7d49 | authored=2026-01-09T13:33:41+08:00 | committed=2026-01-09T11:03:41+05:30 | smartdddlab | fix: ensure UTF-8 encoding handling for MCP command output (#507) | strict_reverse_rc=0
3294a0ad941f299e8c997bbe88a718694e173a8f | authored=2026-01-10T21:45:12+09:00 | committed=2026-01-10T18:15:12+05:30 | kazuki nakai | feat(mcp): add AIRIS MCP Gateway as default installation option (#509) | strict_reverse_rc=1
55c658c77f88c538cf9d90a3736c1b24f8f64f44 | authored=2026-02-11T12:32:47+08:00 | committed=2026-02-11T10:02:47+05:30 | Yuxin Liu | Fix AIRIS MCP Gateway installer bugs (#525) | strict_reverse_rc=1
0ceb29553c2ba42efc3c55d1ec9402f8087b7773 | authored=2026-02-13T16:54:27-05:00 | committed=2026-02-13T16:54:27-05:00 | Ironbelly | Merge branch 'SuperClaude-Org:master' into master | strict_reverse_rc=1

### sync-protection: March upstream sync protection fix and merge
2 records; 2 distinct paths

b061b2f7b00ca33d66c10b666c15016873b2e094 | authored=2026-02-25T18:14:50+09:00 | committed=2026-02-25T14:44:50+05:30 | Utakata | fix: correct pull-sync workflow protection rules (#530) | strict_reverse_rc=1
1e8c6e1622e157f36f44792e41f667399edb2a79 | authored=2026-03-06T10:22:09-05:00 | committed=2026-03-06T10:22:09-05:00 | Ironbelly | Merge branch 'SuperClaude-Org:master' into master | strict_reverse_rc=1

### automated-sync-copies: Five merged bot syncs, namespace copies and sync pointer updates
5 records; 54 distinct paths

465797ad0d6157a3bb2ffc4a7e902f66f07ae942 | authored=2026-05-17T08:21:23+00:00 | committed=2026-05-17T08:21:23+00:00 | github-actions[bot] | chore: automated sync and namespace isolation from framework [2026-05-17 08:21] | strict_reverse_rc=1
ff5f73adf5d9a143228a02516b8ba7ae466acfdc | authored=2026-07-22T08:28:18+00:00 | committed=2026-07-22T08:28:18+00:00 | github-actions[bot] | chore: automated sync and namespace isolation from framework [2026-07-22 08:28] | strict_reverse_rc=1
ec9f066f2ebcf7511b28bac59182329b17b36f17 | authored=2026-08-21T06:44:16+00:00 | committed=2026-08-21T06:44:16+00:00 | github-actions[bot] | chore: automated sync and namespace isolation from framework [2026-08-21 06:44] | strict_reverse_rc=1
66d54204c24b65e4bf96e039a37ada94a761a7a3 | authored=2026-09-15T03:37:59+00:00 | committed=2026-09-15T03:37:59+00:00 | github-actions[bot] | chore: automated sync and namespace isolation from framework [2026-09-15 03:37] | strict_reverse_rc=1
f14f0ccafe8d86da2d32b3ce06d225c3c3f480a3 | authored=2026-09-27T16:29:46+00:00 | committed=2026-09-27T16:29:46+00:00 | github-actions[bot] | chore: automated sync and namespace isolation from framework [2026-09-27 16:29] | strict_reverse_rc=0

## Date boundary cross-check
Author/committer window disagreement among selected records:
End of evidence.
