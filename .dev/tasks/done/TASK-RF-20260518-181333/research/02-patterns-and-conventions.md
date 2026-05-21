# Research 02 — Patterns & Conventions

**Researcher:** R2 of 7
**Topic:** Commit-message style + branch naming + .gitignore patterns + prior release-artifact commit conventions
**Scope:** Branch QA + commits + branching strategy + PR plan for `feat/hook-sync-and-matcher-fix`
**Status:** In Progress

---

## 1. Commit-Message Style — Conventional Commits in Practice

### 1.1 Format observed on the current branch (`master..HEAD`, 15 commits)

`type(scope): subject` — strict Conventional Commits. Source: `git log --oneline master..HEAD`:

| Commit  | Type    | Scope         | Subject pattern                                                                                       |
|---------|---------|---------------|-------------------------------------------------------------------------------------------------------|
| efaa33d | chore   | hooks         | `resolve OQ-2 (archive+delete bash-gate orphan) and OQ-3 (register reject-workspace-writes.sh)`       |
| 87c8254 | feat    | task-builder  | `MIG-006 land FR-CONV.6 Synthetic-DNSP on Partition Exhaust (M6)`                                     |
| 5439ea1 | feat    | hooks         | `widen auggie-flag-clear matcher to mcp__auggie-mcp__; add verify-sync hook coverage and cross-consistency checks` |
| edd3ddd | docs    | task-builder  | `D-0067 T05.16 MIG-005 evidence + FF governance entry`                                                |
| db6166e | feat    | task-builder  | `MIG-005 land FR-CONV.5 Retry Monotonicity + Regression Halts (M5)`                                   |
| 0dcc947 | test    | task-builder  | `D-0066 T05.15 TEST-024 sequencing inversion fixture (K-007 mitigation)`                              |
| c9e2b12 | test    | task-builder  | `D-0065 T05.14 TEST-017 + TEST-022 slow-shrink + cross-cycle dedup fixtures`                          |
| 20b58f6 | test    | task-builder  | `D-0064 T05.13 TEST-015 + TEST-016 monotonicity + regression halt fixtures`                           |
| 487e76b | feat    | task-builder  | `MIG-004 land FR-CONV.4 Five Adversarial Axes overlay (M4)`                                           |
| 8b7fe5f | docs    | task-builder  | `D-0039 T03.16 MIG-003 evidence + FF governance entry`                                                |
| ad083b6 | feat    | task-builder  | `MIG-003 land FR-CONV.3 Inherited Structural Verdict + Self-Audit (M3)`                               |
| de7829d | test    | task-builder  | `D-0038 T03.15 TEST-010 dynamic enumeration INV-010 fixture`                                          |
| bb5d751 | test    | task-builder  | `D-0037 T03.14 TEST-009 Self-Audit INV-019 fixture`                                                   |
| 79644fa | docs    | task-builder  | `D-0025 T02.11 MIG-002 evidence + FF governance entry`                                                |
| 2648be8 | feat    | task-builder  | `MIG-002 land FR-CONV.2 Execution Context header (M2)`                                                |

Type frequencies on this branch (evidence: `git log --pretty | grep -oE '^[a-z]+\(' | sort | uniq -c`):

```
5 test(task-builder)
5 feat(task-builder)
3 docs(task-builder)
1 feat(hooks)
1 chore(hooks)
```

### 1.2 Repo-wide scope vocabulary (top scopes, all branches)

Evidence: `git log --all --pretty=format:"%s" | grep -oE '^[a-z]+\([^)]+\)' | sort | uniq -c | sort -rn`:

```
11 feat(task-builder)        ← convergence work scope
 7 feat(sprint)               ← SPRINT RUNNER scope — confirmed precedent
 7 feat(roadmap)
 6 chore(releases)            ← plural "releases" for archive ops
 5 test(task-builder)
 4 fix(roadmap)
 3 feat(hooks)
 3 feat(commands)
 3 docs(task-builder)
 3 chore(tasks)               ← MDTM task archival
 2 fix(hooks)
 2 fix(tests)
 2 fix(ci)
 2 feat(skills)
 2 feat(pipeline)
 2 chore(release-artifacts)
 2 chore(release)             ← singular "release" for close-out commits
```

**Composite scopes are accepted** (comma-separated, no spaces):
- `feat(spawn,adversarial)` — db824c4
- `test(roadmap,sprint)` — 7e0b647
- `test(pipeline|roadmap|sprint)` — uses `|` separator (one outlier)
- `refactor(commands,skills)` — de04670

### 1.3 Subject-line conventions

**Deliverable IDs embedded in subject (no separator needed):**
- `MIG-NN` prefix for migration steps: `MIG-002 land FR-CONV.2 Execution Context header (M2)`
- `D-NNNN` prefix for deliverable-level work: `D-0067 T05.16 MIG-005 evidence + FF governance entry`
- `T0N.NN` for tasklist task IDs: `D-0066 T05.15 TEST-024 sequencing inversion fixture`
- `TEST-NNN` for test-fixture IDs: `TEST-024 sequencing inversion fixture`
- `INV-NNN` for invariant IDs: `INV-019 fixture`, `INV-010 fixture`
- `FR-CONV.N` for functional-requirement convergence items

**Milestone tags as parenthesized suffix:**
- `(M2)`, `(M3)`, `(M4)`, `(M5)`, `(M6)` — appended at end of subject for MIG landings
- Wave tags from sprint scope: `(v3.7 Wave 3)`, `(v3.7)`

**Resolution markers:**
- `resolve OQ-N (...)` for resolving open questions (e.g. efaa33d resolves OQ-2/OQ-3)
- `close out <release-name>` for chore(release) commits
- `land <FR-id>` for migration step landings

**Length:** subjects range 50–253 chars; soft max is roughly **120 chars** for clean log lines but the repo tolerates longer when deliverable IDs are stacked. **No hard 72-char rule.** Median is ~80.

### 1.4 Sprint runner precedent (for C1–C4 work)

Evidence: `git log --all -- src/superclaude/cli/sprint/`:

```
2c4730e fix(sprint): match Wave-4 checkpoint heading form in path/recovery parsers (v3.7)
de04670 refactor(commands,skills): Naming consolidation — /sc:task canonical (v3.7)
08addac feat(sprint): TUI v2 Wave 4 — tmux 3-pane + summary fanout (v3.7)
5115dfa feat(sprint): TUI v2 Wave 3 — summary + retrospective infrastructure (v3.7)
430a1c9 feat(sprint): TUI v2 Wave 1 — data model + monitor extraction (v3.7)
965213b feat(sprint): Phase 3 — checkpoint manifest, CLI verify-checkpoints, auto-recovery (v3.7 Wave 3)
2a60667 feat(sprint): Phase 2 — post-phase checkpoint enforcement gate (v3.7 Wave 2)
183f8f8 feat(sprint): Phase 1 — prompt-level checkpoint enforcement (v3.7 Wave 1)
```

**Recommendation for C1–C4 sprint runner fixes:** use scope `sprint` (singular, no prefix). If a fix touches both sprint runner AND tests, prefer `feat(sprint)` or `fix(sprint)` and let `test(sprint)` follow in a separate commit; or use composite `fix(sprint,tests)` if atomically grouped. Precedent example: `fix(sprint): complete sprint runner/TUI wiring updates` (from 4e5e375 body).

### 1.5 Co-Authored-By signoff convention

Evidence: `git log --all --pretty=format:"%B" | grep -iE "co-authored-by"`:

**Canonical form (use this verbatim):**
```
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
```

Variants seen historically (do NOT use — model version is now 4.7):
- `Co-Authored-By: Claude Opus 4.5/4.6 <noreply@anthropic.com>` (legacy)
- `Co-authored-by: Claude <noreply@anthropic.com>` (legacy lowercase)
- `Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>` (one-off variant)

**Conventions for commit body:**
- Single blank line between subject and body.
- Body uses prose paragraphs + `## H2` section headings for multi-part commits (e.g. efaa33d uses `## OQ-2`, `## OQ-3`, `## Test updates`, `## Verification`).
- Trailing `Co-Authored-By:` line preceded by a blank line.
- Inline shell verification blocks indented 2 spaces: `  $ make verify-sync   →   EXIT=0  ✅`
- "Unblocks X" and "Forward: X" trailers are used to indicate downstream task gating (evidence: `Unblocks T06.18`, `Forward: T03.16`).

---

## 2. Branch Naming

### 2.1 Active local branches (`git branch`)

```
chore/task-cleanup-20260517
chore/task-merge-consolidate-roadmap-to-release
feat/hook-sync-and-matcher-fix       ← current
feat/mig-002-execution-context-header
fix/auggie-flag-clear-mcp-prefix
master
```

### 2.2 Remote branches — full pattern catalogue (`git branch -a`)

**Prefixes observed:**
- `feat/` — most common, for new features (28+ branches)
- `fix/` — bug fixes (several CI-rot examples)
- `chore/` — housekeeping (task cleanup, archival)
- `feature/` — legacy spelling (only 1: `origin/feature/skills-drop`); **prefer `feat/`**
- `docs/` — referenced in CLAUDE.md global rules; no active examples right now

**Naming styles:**

1. **Topic-kebab** (most common): `feat/recommend-v2`, `feat/freshness-system`, `feat/install-auggiemcp`, `fix/auggie-flag-clear-mcp-prefix`
2. **Versioned topic**: `feat/v3.65-prd-tdd-Refactor`, `feat/v3.67-prd-skill-portify`, `feat/3.7-task-unified-v2`
3. **Deliverable-ID suffix**: `feat/mig-002-execution-context-header` — uses `mig-002` (lowercase) + descriptive tail
4. **Date suffix** `-YYYYMMDD`: `chore/task-cleanup-20260517` — used for chore/cleanup branches where the date is the most stable identifier
5. **PR-rot pattern**: `fix/ci-rot-pr1-ruff-autofix`, `fix/ci-rot-pr2-ruff-format`, ..., `fix/ci-rot-pr5-contributing-and-pullsync` — sequential PR-split branches with consistent prefix

### 2.3 When to use which suffix style

- **Date suffix `-20260518`**: for chore/cleanup branches with no semantic anchor. Example: `chore/task-cleanup-20260517`.
- **Deliverable-ID suffix `-mig-NNN` or `-d-NNNN`**: for branches landing a specific tracked deliverable. Lowercase. Example: `feat/mig-002-execution-context-header`.
- **`-prN-<topic>` sequential split**: when an oversized PR is sliced into N child PRs. Example: `fix/ci-rot-pr1-ruff-autofix`, `fix/ci-rot-pr2-ruff-format`.

### 2.4 Recommended sub-branch names for PR split

If splitting `feat/hook-sync-and-matcher-fix` into multiple PRs, follow the `prN-<topic>` precedent:

| Recommended branch                                              | Purpose                                                       |
|-----------------------------------------------------------------|---------------------------------------------------------------|
| `feat/sprint-runner-c1-c4-fixes` OR `fix/sprint-c1-c4-runner`   | Sprint runner C1-C4 reliability fixes                         |
| `feat/audit-test-suite` OR `test(audit)` on the same branch     | New audit test coverage                                       |
| `chore/release-task-builder-merge`                              | If committing `.dev/releases/current/task-builder-merge/`     |
| `chore/cleanup-untracked-20260518`                              | If sweeping repo-root garbage (`0.20`, `prd-test-product/`)   |
| `fix/hook-sync-and-matcher-pr1-...` (sequential split)          | Strict precedent match — exactly the `ci-rot-prN` pattern     |

**Caution:** the existing branch is already named `feat/hook-sync-and-matcher-fix`. If splitting, **do not abandon** it — base the split branches off it and PR them sequentially, OR rebase the cohesive subset onto fresh branches from master.

---

## 3. Prior Release Artifact Convention — CRITICAL

### 3.1 Releases directory layout

`ls .dev/releases/complete/` returned 60+ historical release directories spanning `v1.0-mcp-installer` through `v3.7-turnledger-integration`. Notable examples adjacent to current work:

- `unified-audit-gating-v1.2.1`
- `v3.7-turnledger-integration`
- `v3.7-task-unified-v2`
- `auggie-first`
- `freshness-system`
- `cleanup-audit-v2-UNIFIED-SPEC`

### 3.2 Are per-deliverable artifacts in git? **YES.**

Evidence: `git ls-tree -r HEAD .dev/releases/complete/unified-audit-gating-v1.2.1/`:

- **146 files tracked** in that single release directory.
- Per-deliverable evidence files ARE committed: 50+ `tasklist/artifacts/D-NNNN/evidence.md` paths confirmed in the tree (D-0001 through D-0030+ enumerated).
- Adversarial artifacts ARE committed: `adversarial/base-selection.md`, `adversarial/debate-transcript.md`, `adversarial/merge-log.md`, etc.
- Execution logs ARE committed: `tasklist/execution-log.jsonl` AND `tasklist/execution-log.md`.
- State files ARE committed: `.roadmap-state.json`, `tasklist/.sprint-exitcode`.

`git ls-tree -r HEAD .dev/releases/complete/v3.7-turnledger-integration/` returned **150 tracked files**, including the `ValidationGPT/` deep-validation artifacts (00-decomposition-plan.md, 01-agent-CC1-*.md, etc.).

### 3.3 How were they committed? Single sweeping commit, NOT incremental

Evidence: `git log --oneline --all -- .dev/releases/complete/<release>/`:

- **unified-audit-gating-v1.2.1**: 3 commits ever touched it — `6a25e19 feat(roadmap): unify v3.05, v3.1, and v3.2 fidelity gate releases`, `f7ea213 Roadmap gaps`, `8ac5eb7 2.16 complete and cleanup`. Most artifacts arrived in one sweep.
- **v3.7-turnledger-integration**: **1 commit only** — `c5a874e refactor(cli): resolve unwired components P1-P4 with gate enforcement and audit cleanup`. All 150 files landed atomically.
- **v3.7-task-unified-v2**: **1 commit** — `f79b1bd feat(workspace-rca): layered remediation for skill-creator workspace misplacement`. (Note: a sibling chore-style precedent exists in `chore(releases): archive v3.75 RigorflowMerger`.)

Per-deliverable D-NNNN/evidence.md files were **NOT** committed incrementally as they were produced — they were folded into a single sweeping commit when the release closed out.

### 3.4 Commit-message pattern for release-artifact sweeps

Evidence: `git log --all --pretty=format:"%s" | grep -E '^chore\(release'`:

```
chore(release): close out freshness-hook-fix + auggie-first (#35)
chore(releases): archive v3.75 RigorflowMerger and add current backlog/releases
chore(release-artifacts): archive v3.65 outputs and relocate tdd-spec analysis research
chore(releases): archive v2.10 roadmap-v4 artifacts
chore(releases): archive v2.08 roadmap-cli artifacts
chore(releases): archive v2.0 task-unified legacy docs
```

**Recommended pattern for the 105 untracked task-builder-merge artifacts:**

```
chore(releases): archive task-builder-merge artifacts (D-0053–D-0100, M5–M7)
```

OR if the release is closing out:

```
chore(release): close out task-builder-merge (#NN)
```

### 3.5 ANSWER: Do we commit `.dev/releases/current/task-builder-merge/**`?

**YES — commit them.** Three independent lines of evidence:

1. **Prior precedent**: Every prior `complete/` release dir contains its full artifact tree in git (146/150 files for sampled releases). The pattern is consistent across 60+ releases.
2. **No `.gitignore` rule excludes `.dev/releases/`**. Only `.dev/eval-workspaces/` (via the `.claude/skills/*-workspace/` rule on line 205) and Python build artifacts are ignored.
3. **In-flight evidence on this branch**: the most recent merged work landed D-NNNN evidence files (`8b7fe5f docs(task-builder): D-0039 T03.16 MIG-003 evidence`, `edd3ddd docs(task-builder): D-0067 T05.16 MIG-005 evidence`) and they ARE in git history with the `docs(task-builder)` scope.

**Two acceptable shapes:**
- **Shape A (sweep)**: single `chore(releases): archive task-builder-merge artifacts` commit with all 105 files.
- **Shape B (incremental, more in line with this branch's pattern)**: per-deliverable `docs(task-builder): D-NNNN <work-item> evidence` commits, mirroring how D-0025, D-0038, D-0039, D-0064, D-0065, D-0066, D-0067 were already committed. **This is the precedent on the active branch and is recommended for the in-flight deliverables.** Use Shape A only for the close-out sweep at release-completion time.

### 3.6 What about `.dev/releases/current/hook-sync-and-matcher-fix/`?

This is a separate untracked release directory (untracked, evidence: `git status --porcelain | grep hook-sync`). It belongs to THIS branch's own work. Recommend the same treatment: commit alongside the matcher-fix changes with scope `chore(release)` or `docs(hooks)` depending on whether it's release-process artifacts or evidence.

---

## 4. .gitignore Patterns

### 4.1 What IS ignored (key lines from `.gitignore`)

| Line       | Pattern                              | Effect                                                              |
|------------|--------------------------------------|---------------------------------------------------------------------|
| L2         | `__pycache__/`                       | Python bytecode dirs                                                |
| L3         | `*.py[cod]`                          | `.pyc`, `.pyo`, `.pyd` files                                        |
| L21        | `*.egg-info/`                        | Editable-install metadata                                           |
| L37–48     | `htmlcov/`, `.coverage*`, `.pytest_cache/`, `.hypothesis/` | Test/coverage artifacts                  |
| L51–56     | `venv/`, `.venv/`, `env/`, `ENV/`    | Virtualenvs                                                          |
| L78–82     | `logs/`, `*.log`                     | Log files (note: this would catch `*.log` even in `.dev/`)          |
| L102–104   | `.claude/history/`, `.claude/cache/`, `.claude/*.lock` | Claude Code per-session state              |
| L117       | `.claude/`                           | **WARNING: blanket rule on L117 ignores `.claude/` entirely** — overrides the surgical L102–L104 rules above. Likely a bug, see §4.3. |
| L107       | `.serena/`                           | Serena MCP session data                                              |
| L113       | `Tests/`                             | Capital-T (legacy) test dir                                          |
| L121       | `*.tar.gz`                           | Tarballs                                                             |
| L149       | `uv.lock`                            | UV lockfile                                                          |
| L156–158   | `.mypy_cache/`, `.ruff_cache/`, `.black/` | Linter caches                                                   |
| L205       | `.claude/skills/*-workspace/`        | **Skill eval-workspace override** — enforces .dev/eval-workspaces/  |

### 4.2 What is NOT ignored (but probably should be)

Evidence: `ls /config/workspace/IronClaude/ | grep -iE 'prd-test|prd-dry|0\.'` shows these exist at repo root:

```
0.20                    ← stray version-string file/dir
prd-dry-run-test/       ← prd skill test output
prd-test-product/       ← prd skill test output
```

`.dev/eval-runs/` is also untracked (per `git status` output) but has **no .gitignore rule**. **Recommend adding:**

```gitignore
# Plugin/skill test scratch outputs at repo root
prd-test-*/
prd-dry-run-*/
0.[0-9]*                    ← careful: too broad; consider /0.[0-9]* anchored to root

# Skill eval runs (sibling to .dev/eval-workspaces/)
.dev/eval-runs/
```

**Caution on `0.*`**: a bare `0.*` glob would also match `0.tar.gz`, `0.md`, anything starting with `0.`. Anchor to repo root with leading `/`: `/0.[0-9]*`.

### 4.3 .gitignore bug — `.claude/` blanket on line 117

Line 117 says `.claude/` which would ignore the entire `.claude/` working tree, contradicting:
- Line 102 `.claude/history/` (surgical rule made redundant)
- The whole project workflow where `.claude/` is dev copy of skills/agents/commands.

This isn't relevant to the immediate branch QA, but flag for R1/R3 follow-up: `.gitignore:117` should likely be removed or commented out — it's working only because tracked files are listed in the index and `.gitignore` only affects untracked files. **Do not fix in this PR**; capture as a follow-up finding.

### 4.4 Pyc files in the working tree (related to efaa33d cleanup)

The recently merged efaa33d commit body mentions cleaning `tests/hooks/__pycache__/test_auggie_bash_gate.cpython-312-pytest-9.0.3.pyc` — this is correctly covered by `.gitignore` L2 (`__pycache__/`) and L3 (`*.py[cod]`). No gap.

---

## 5. CLAUDE.md & Global Rules

### 5.1 Project CLAUDE.md (`/config/workspace/IronClaude/CLAUDE.md`)

**Branch structure (line 222 area):**
> `master` (production) ← `integration` (testing) ← `feature/*`, `fix/*`, `docs/*`

**Note:** The project doc says `feature/*` (long form), but the live convention is `feat/*` (short form) — see §2.2 evidence. **Use `feat/` to match what's actually on origin/`.** The doc is stale on this point.

**Standard workflow (project CLAUDE.md):**
1. Create branch from `integration`: `git checkout -b feature/your-feature` (but origin uses feat/)
2. Develop with tests: `uv run pytest`
3. Commit: `git commit -m "feat: description"` (conventional commits)
4. Merge to `integration` → validate → merge to `master`

**Current state:** `feat/hook-sync-and-matcher-fix` is branched from master (not integration) — evidence: most recent merges and `git log` lineage show direct master-targeting PRs (`#41`, `#42`, `#43`, `#44`, `#45`, `#46`). The `integration` branch model is **largely abandoned in practice**. PRs go straight to `master`.

### 5.2 Global CLAUDE.md (`/config/.claude/CLAUDE.md`)

**Rule 4:** "Git — feature branches only; never commit directly to master/main" — confirmed.

**Rule 1:** UV only — relevant for any commit that runs tests/lint locally for verification.

**Rule 9:** "Auggie first — call codebase-retrieval before significant edits to load relevant context" — applies to implementation phase, not directly to commit/PR mechanics.

**No explicit signoff requirement in CLAUDE.md** — Co-Authored-By convention is inferred from git history (see §1.5).

---

## 6. Synthesis — Concrete Style Guides for the Builder

### 6.1 Commit-message templates per category

**Feature work (sprint runner C1–C4):**
```
feat(sprint): C1-C4 reliability fixes — <one-line summary>

<paragraph body: what was broken, what changed, why>

## Verification

  $ uv run pytest tests/sprint/ -v   →   <N> passed
  $ make verify-sync                  →   EXIT=0

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
```

**Test additions:**
```
test(sprint): add audit-test-suite coverage for C1-C4 reliability paths

<what's covered, which fixtures>

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
```

**Bug fix (hooks):**
```
fix(hooks): <symptom> — <root-cause one-liner>

<body>

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
```

**Release artifact sweep:**
```
chore(releases): archive task-builder-merge artifacts (D-0053–D-0100, M5–M7)

105 deliverable artifacts + checkpoints + execution-log under
.dev/releases/current/task-builder-merge/, mirroring prior release archival
(see unified-audit-gating-v1.2.1 precedent: 146 tracked files).

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
```

**Per-deliverable docs (preferred for in-flight work, matches branch pattern):**
```
docs(task-builder): D-NNNN T0X.YY <work item> evidence + FF governance entry

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
```

### 6.2 Branch-naming guide

- New feature work: `feat/<topic-kebab>` or `feat/<topic>-<deliverable-id>` (lowercase)
- Bug fix: `fix/<topic-kebab>`
- Chore/cleanup with date: `chore/<topic>-YYYYMMDD`
- Sequential PR split: `<type>/<base-topic>-prN-<sub-topic>`
- Target master directly (integration model abandoned)

### 6.3 Release-artifact commit decision

**Commit them. Two acceptable shapes:**
1. **Per-deliverable incrementally** (`docs(task-builder): D-NNNN ...`) for in-flight evidence — matches this branch's existing 5 docs commits.
2. **Single sweep** (`chore(releases): archive <release-name>`) for close-out — matches 60+ prior `complete/` releases.

For the **105 untracked files under `.dev/releases/current/task-builder-merge/`** specifically: since the release is still `current/` (not `complete/`), use Shape 1 (per-deliverable). When the release is promoted to `complete/`, Shape 2 sweep is appropriate.

---

## 7. Open Items / Caveats for the Builder

1. **`.gitignore` L117 `.claude/` blanket** is a latent bug — not in scope for this PR; flag for follow-up. Do NOT touch it as part of the branch QA.
2. **`integration` branch convention is stale in CLAUDE.md** — actual practice is direct-to-master PRs. Confirm with maintainer before flagging this as a doc-fix task.
3. **`prd-test-product/` and `prd-dry-run-test/` and `0.20` at repo root** are untracked but unignored — recommend adding gitignore entries (anchored to root) before commits to avoid future contamination. Out of scope for this PR's content but in scope for branch hygiene.
4. **`.dev/eval-runs/`** is untracked and has no gitignore rule — same recommendation. Sibling concern to the skill-creator workspace override on `.gitignore:205`.
5. **Sprint scope precedent (§1.4)**: 8 prior `feat(sprint):` / `fix(sprint):` commits make `sprint` the unambiguous scope for C1–C4 runner work. Do not invent a new scope.

---

## Status: COMPLETE

### Summary of Findings (one-paragraph for orchestrator)

The repo uses strict Conventional Commits (`type(scope): subject`) with established scopes `task-builder`, `sprint`, `roadmap`, `hooks`, `tests`, `ci`, `releases`, `commands`, `skills`, `pipeline`, and composite scopes (`feat(spawn,adversarial)`). Subjects embed deliverable IDs (MIG-NN, D-NNNN, T0X.YY, TEST-NNN, INV-NNN) and milestone tags `(M3)`. Co-author signoff is `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>` (canonical capitalization). Branches use `feat/`, `fix/`, `chore/` prefixes with optional date suffix (`-20260517`) for cleanup or deliverable suffix (`-mig-002`) for tracked work; sequential PR splits use `-prN-<topic>` (precedent: `fix/ci-rot-pr1` through `pr5`). For the 105 untracked `.dev/releases/current/task-builder-merge/**` files: **YES, commit them** — prior `complete/` releases tracked 146–150 files each, mostly via a single sweeping `chore(releases): archive ...` commit, but in-flight branches commit per-deliverable evidence files with `docs(task-builder): D-NNNN ...` (this branch already has 3 such commits). Recommend Shape 1 (per-deliverable) for in-flight work, Shape 2 (sweep) only at release close-out. `.gitignore` covers Python build artifacts, virtualenvs, IDE files, and skill eval-workspaces (line 205 override); gaps: `prd-test-product/`, `prd-dry-run-test/`, `0.20` at repo root, `.dev/eval-runs/`. The project's documented `integration` branch model is stale — practice is direct-to-master PRs.
