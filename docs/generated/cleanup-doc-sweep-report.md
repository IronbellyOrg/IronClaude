# IronClaude Documentation Cleanup Sweep Report

**Status**: Complete (with inferential bulk classification for very large `.dev/` corpus)
**Date**: 2026-03-24
**Scope**:
- `/config/workspace/IronClaude/docs/**`
- `/config/workspace/IronClaude/plugins/superclaude/**`
- `/config/workspace/IronClaude/.dev/**`
- `/config/workspace/IronClaude/PROJECT_INDEX.md`
- `/config/workspace/IronClaude/AGENTS.md`
- `/config/workspace/IronClaude/SECURITY.md`
- `/config/workspace/IronClaude/README.md`

## Summary Stats

- **Total markdown files scanned in scope**: **3,908**
  - `docs/`: 193
  - `plugins/superclaude/`: 79
  - `.dev/`: 3,632
  - root targets: 4
- **Classification totals**
  - **ARCHIVE**: 3,783
  - **UPDATE**: 124
  - **KEEP**: 1

---

## Priority Ordering (highest-impact archives first)

1. **`/config/workspace/IronClaude/PROJECT_INDEX.md`** — stale project identity + deleted directories listed (`user-guide-jp/kr/zh`) and `SuperClaude_Framework` root naming.
2. **`/config/workspace/IronClaude/docs/generated/**` (64 files)** — generated/stale artifacts with extensive upstream naming/path leakage.
3. **`/config/workspace/IronClaude/docs/mistakes/**` (45 files)** — dated session artifacts, not onboarding docs.
4. **`/config/workspace/IronClaude/docs/research/**` (majority)** — historical research, includes upstream fork workflow docs (some Japanese).
5. **`/config/workspace/IronClaude/.dev/**` (3,632 files, INFERENTIAL bulk)** — release/research artifacts; not onboarding-facing canonical docs.

---

## Evidence Highlights (key citations)

- Upstream repo references:
  - `docs/getting-started/installation.md:209-210` → `github.com/SuperClaude-Org/SuperClaude_Framework`
  - `docs/developer-guide/README.md:150,172` → upstream GitHub links
  - `docs/troubleshooting/serena-installation.md:126` → "Report issues to SuperClaude Framework"
- Obsolete structure references:
  - `docs/developer-guide/contributing-code.md:59-67` → `superclaude/Core`, `superclaude/Agents`, `setup/`
  - `docs/user-guide/agents.md:38` → `superclaude/Agents/`
  - `docs/testing/procedures.md:13-14` → coverage target includes `setup/`
- Deleted translated docs still referenced:
  - `PROJECT_INDEX.md:89-91` → `user-guide-jp`, `user-guide-kr`, `user-guide-zh`
  - `docs/generated/repo-knowledge-base-readme.md:124` → localized guides still listed
- Unreleased v5/plugin-system-as-current patterns (flagged where framed as active roadmap state in old docs):
  - broad hits in legacy research/generated analysis corpus (see grep set in audit notes)
- Plugin command self-reference to upstream docs:
  - `plugins/superclaude/commands/sc.md:128` → `https://github.com/SuperClaude-Org/SuperClaude_Framework`

---

## Directory Inventory Tables

## 1) Root Files

| File | Class | Reason | Evidence |
|---|---|---|---|
| `README.md` | **KEEP** | Rebranded correctly to IronClaude while preserving package naming reality (`superclaude`). | `README.md:1-6, 21-31, 70-74` |
| `PROJECT_INDEX.md` | **ARCHIVE** | Generated as "Project Index: SuperClaude Framework"; contains deleted translated dirs and stale tree. | `PROJECT_INDEX.md:1, 15, 89-91` |
| `AGENTS.md` | **UPDATE** | Generic contributor guide content; includes potentially stale TS agent paths (`pm/`, `research/`, `index/`) and not IronClaude-facing. | `AGENTS.md:6, 37-38` |
| `SECURITY.md` | **UPDATE** | Still branded "SuperClaude Framework"; version/support table stale; command casing inconsistent with current CLI conventions. | `SECURITY.md:5, 42, 156-161` |

---

## 2) `/docs/` (193 files)

### 2.1 High-confidence ARCHIVE groups

| Path group | Count | Class | Reason | Evidence |
|---|---:|---|---|---|
| `docs/generated/**` | 64 | **ARCHIVE** | Generated artifacts, many stale/upstream path references, not canonical onboarding docs. | e.g. `docs/generated/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:1`; `docs/generated/repo-knowledge-base-readme.md:124` |
| `docs/mistakes/**` | 45 | **ARCHIVE** | Dated operational logs/journals (2025–2026), not onboarding documentation. | repeated date-stamped filenames; 24-line repetitive records |
| `docs/analysis/**` | 10 | **ARCHIVE** | Competitive comparison artifacts; upstream identity focus; not core product docs. | filenames `*-vs-superclaude-*` |
| `docs/testing/procedures.md` | 1 | **ARCHIVE** | Japanese legacy testing procedure referencing obsolete `setup/` + old toolchain (`black`, `mypy superclaude setup`, `pytest --cov=setup`). | `docs/testing/procedures.md:13-14, 38-54` |

### 2.2 UPDATE groups (useful but stale branding/structure)

| Path group | Count | Class | Reason | Evidence |
|---|---:|---|---|---|
| `docs/developer-guide/*.md` | 6 | **UPDATE** | Useful contributor content, but heavily references upstream repo and old structure (`superclaude/Agents`, `setup`). | `contributing-code.md:29-31, 59-67`; `testing-debugging.md:162,181,223` |
| `docs/getting-started/*.md` | 2 | **UPDATE** | Onboarding valuable, but install instructions include upstream clone path and old `SuperClaude` command casing. | `installation.md:209-210, 250-254`; `quick-start.md:3, 83-90` |
| `docs/reference/*.md` | 16 | **UPDATE** | Reference library still useful but "SuperClaude Framework" branding and upstream issue links persist. | `reference/README.md:1`; `examples-cookbook.md:160-161` |
| `docs/user-guide/*.md` | 8 | **UPDATE** | Valuable user docs but old naming/paths appear (`superclaude/Agents/`, upstream links). | `user-guide/agents.md:38, 682`; `user-guide/modes.md:564` |
| `docs/troubleshooting/*.md` | 1 | **UPDATE** | Useful troubleshooting; upstream reporting URL outdated. | `serena-installation.md:126` |
| `docs/agents/*.md` | 1 | **UPDATE** | Content useful but titled/positioned as SuperClaude. | `pm-agent-guide.md:1` |
| `docs/mcp/*.md` | 2 | **UPDATE** | Still relevant design/policy docs; branding/version normalization needed. | broad corpus evidence; no critical obsolescence detected |

### 2.3 Research subtree split (INFERENTIAL + evidence-backed exceptions)

| Path group | Count | Class | Reason | Evidence |
|---|---:|---|---|---|
| `docs/research/research_oss_fork_workflow_2025.md` | 1 | **ARCHIVE** | Japanese upstream fork workflow (`SuperClaude-Org`, `kazukinakai/SuperClaude_Framework`). | lines `26-29, 47-56` |
| `docs/research/research_python_directory_naming_20251015.md` | 1 | **ARCHIVE** | References deleted translated dirs and transitional rename state. | hits at `218-220, 280-282` |
| `docs/research/research_python_directory_naming_automation_2025.md` | 1 | **ARCHIVE** | Legacy migration script patterns for old tree + translated dirs. | hits around `492-494, 642+` |
| `docs/research/mcp-installer-fix-summary.md` | 1 | **ARCHIVE** | Hardcoded legacy local path under `.../SuperClaude_Framework/setup/...`. | `:95` |
| `docs/research/**` (remaining 25 files) | 25 | **ARCHIVE** *(INFERENTIAL)* | Historical research logs and analysis notes (dated 2025/early 2026), not onboarding docs; many upstream-context assumptions. | corpus characteristics + sampled files above |

### 2.4 Memory subtree

| Path group | Count | Class | Reason | Evidence |
|---|---:|---|---|---|
| `docs/memory/*.md` | 6 | **ARCHIVE** | Session/memory internals and historical logs; not onboarding docs; explicit SuperClaude framing. | `memory/README.md:3`; `memory/pm_context.md:3` |

---

## 3) `/plugins/superclaude/` (79 files)

| Path group | Count | Class | Reason | Evidence |
|---|---:|---|---|---|
| `plugins/superclaude/commands/*.md` | 31 | **UPDATE** | Active command docs but branding/version stale; at least one upstream doc URL. | `commands/sc.md:3,6,117,128` |
| `plugins/superclaude/agents/*.md` | 20 | **UPDATE** | Likely still functional asset definitions; rebrand and policy refresh needed. | sampled `agents/pm-agent.md` + corpus |
| `plugins/superclaude/core/*.md` | 6 | **UPDATE** | Core framework docs likely used, but naming/identity still SuperClaude. | sampled `core/RULES.md` |
| `plugins/superclaude/modes/*.md` | 7 | **UPDATE** | Functional mode docs; naming refresh needed. | corpus |
| `plugins/superclaude/mcp/*.md` | 8 | **UPDATE** | Functional MCP docs; branding and possibly server set/version updates needed. | corpus |
| `plugins/superclaude/templates/roadmaps/*.md` | 6 | **UPDATE** | Template content useful but identity refresh required. | corpus |
| `plugins/superclaude/skills/confidence-check/SKILL.md` | 1 | **UPDATE** | Keep skill but update naming/conventions. | corpus |
| `plugins/superclaude/examples/deep_research_workflows.md` | 1 | **UPDATE** | Example content likely useful; naming/version updates needed. | corpus |

---

## 4) `/.dev/` (3,632 files)

> **Classification approach**: INFERENTIAL bulk classification due corpus size; sampled representative files from backlog, complete releases, benchmarks, and research.
> **Conclusion**: for onboarding, these are overwhelmingly historical/generated release artifacts.

| Path group | Count | Class | Reason | Evidence |
|---|---:|---|---|---|
| `.dev/releases/**` | very large | **ARCHIVE** *(INFERENTIAL)* | Massive historical release/tasklist/adversarial artifacts; not user onboarding docs. | sample: `.../v1.4-roadmap-gen/SUPERCLAUDE-ROADMAP-GENERATOR-PROMPT.md:1` |
| `.dev/research/**` | 24 | **ARCHIVE** | Research snapshots include upstream comparisons and external analysis dumps. | sample: `.../research-results/.../github.md:31-37` |
| `.dev/benchmarks/**` | 87 | **ARCHIVE** | Benchmark output fixtures/results, not onboarding docs. | benchmark tree listing |
| `.dev/tasks/*.md` | 1 | **ARCHIVE** | Internal maintenance task note. | `.dev/tasks/fix-structural-audit-test-name-dedup.md` |

---

## Recommended Action Plan

1. **Immediately archive/move from onboarding surface**:
   - `PROJECT_INDEX.md`
   - `docs/generated/**`
   - `docs/mistakes/**`
   - `docs/analysis/**`
   - most/all `docs/research/**`
   - all `.dev/**` from onboarding navigation
2. **Update in place (high-value docs)**:
   - `docs/getting-started/*`
   - `docs/user-guide/*`
   - `docs/reference/*`
   - `docs/developer-guide/*`
   - `plugins/superclaude/**`
   - `SECURITY.md`, `AGENTS.md`
3. **Keep as-is**:
   - `README.md` (already aligned to IronClaude identity while preserving package reality)

---

## Notes on Evidence Quality

- **Direct-evidence items** include file+line citations above.
- **INFERENTIAL items** are explicitly labeled and based on:
  - directory purpose (`generated`, `mistakes`, `.dev/releases`, benchmark outputs),
  - sampled-file confirmation,
  - and repeated stale identity/structure patterns across the corpus.
