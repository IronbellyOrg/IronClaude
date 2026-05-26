# D-0085 — T07.03 Evidence: NFR-CONV.5-M7 No-New-Dependencies Diff Audit

**Task:** T07.03 (Phase 7 — M7)
**Roadmap items:** R-142
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tier:** STANDARD
**Verification method:** Direct diff inspection (Read + Grep over `git show` output)
**Overall: PASS** (4/4 acceptance criteria met)

---

## 0. TL;DR

NFR-CONV.5-M7 holds across all six FR-CONV.X land commits (MIG-001..MIG-006). The audit confirms:

- **Zero** new MCP servers introduced.
- **Zero** new external libraries added (every Python import is stdlib or pre-existing `pytest>=7.0.0` dev dep).
- **Zero** synchronous network calls (no `urllib`/`requests`/`httpx`/`aiohttp`/`http.client`/`socket`/`websocket`/`urlopen`/`fetch(`/`curl`/`wget`/`nc`/`ssh`/`scp`).
- **Zero** dependency-manifest mutations (`pyproject.toml`, `uv.lock`, `requirements*.txt`, `Pipfile`, `setup.py`, `setup.cfg`, JS/Rust/Go/Ruby lockfiles — all untouched).
- **Zero** MCP/settings config files touched (`.mcp.json`, `settings.json`, `hooks.json`, `.claude/settings*`, `claude_desktop*` — all untouched).
- The only `subprocess.run` introduced shells out to `grep -cE …` — an allowed Read/Grep/Glob/Bash primitive used as an independent oracle in a TB-Add test fixture.

The four false-positive grep hits (one prose match on `BUILD_REQUESTs.` for `requests\.`, three documentation references to `Edit`/`Write` as the task-builder's existing emission tools, and one documentation example string `"after WebSearch exhaustion"` describing a value the DNSP emitter MUST REJECT) were each verified by hand and resolve to non-violations. Details below.

---

## 1. Audit scope

| FR-CONV.X | Land commit (SHA) | Subject |
|---|---|---|
| FR-CONV.1 (TB-Add-1..7 structural gates) | `9d1e51b` | `feat(task-builder): PR-06 structural gate additions (TB-Add-1 through TB-Add-7)` |
| FR-CONV.2 (Execution Context header)     | `2648be8` | `feat(task-builder): MIG-002 land FR-CONV.2 Execution Context header (M2)` |
| FR-CONV.3 (Inherited Verdict + Self-Audit) | `ad083b6` | `feat(task-builder): MIG-003 land FR-CONV.3 Inherited Structural Verdict + Self-Audit (M3)` |
| FR-CONV.4 (Five Adversarial Axes overlay) | `487e76b` | `feat(task-builder): MIG-004 land FR-CONV.4 Five Adversarial Axes overlay (M4)` |
| FR-CONV.5 (Retry Monotonicity + Regression Halts) | `db6166e` | `feat(task-builder): MIG-005 land FR-CONV.5 Retry Monotonicity + Regression Halts (M5)` |
| FR-CONV.6 (Synthetic-DNSP on Partition Exhaust) | `87c8254` | `feat(task-builder): MIG-006 land FR-CONV.6 Synthetic-DNSP on Partition Exhaust (M6)` |

The audit re-exercises the M1-scope `D-0015/nfr-conv-5-audit.log` (which covered MIG-001 alone) and extends it to the full 6-commit landing sequence per the roadmap §M7 exit conditions.

### Commit-size summary

| SHA | Files | Insertions | Deletions |
|---|---|---|---|
| `9d1e51b` |  6 |   188 |   2 |
| `2648be8` | 36 |  3329 |  36 |
| `ad083b6` | 44 |  5761 |  34 |
| `487e76b` | 44 |  6586 | 128 |
| `db6166e` |  6 |   136 |  28 |
| `87c8254` |  8 |    62 |  16 |
| **Total** | **144 (incl. artifact docs)** | **16062** | **244** |

---

## 2. Dependency manifest mutations — NONE

```bash
for sha in 9d1e51b 2648be8 ad083b6 487e76b db6166e 87c8254; do
  git show --name-only --format="" "$sha" \
    | grep -E "^(pyproject\.toml|uv\.lock|requirements.*\.txt|Pipfile.*|setup\.py|setup\.cfg|package\.json|package-lock\.json|yarn\.lock|Cargo\.toml|go\.mod|Gemfile)"
done
```

Result (all 6 commits): **NONE**. `pyproject.toml`, `uv.lock`, `requirements*.txt`, `Pipfile`, `setup.py`, `setup.cfg`, `package.json`, `package-lock.json`, `yarn.lock`, `Cargo.toml`, `go.mod`, `Gemfile` are untouched across the entire FR-CONV.X landing sequence.

## 3. MCP-server references — NO new servers

```bash
for sha in 9d1e51b 2648be8 ad083b6 487e76b db6166e 87c8254; do
  git show "$sha" --no-color -U0 \
    | grep -E "^\+[^+]" | grep -oE "mcp__[a-zA-Z0-9_-]+__" | sort -u
done
```

Result per commit:

| SHA | `mcp__*__` tokens introduced (added lines) |
|---|---|
| `9d1e51b` | none |
| `2648be8` | none |
| `ad083b6` | `mcp__sequential-thinking__`, `mcp__serena__`, `mcp__tavily__` |
| `487e76b` | `mcp__sequential-thinking__`, `mcp__serena__`, `mcp__tavily__` |
| `db6166e` | none |
| `87c8254` | none |

All three tokens reference **already-installed MCP servers** in the project's approved table (CLAUDE.md "MCP Server Integration"): Sequential, Serena, Tavily. **No new MCP server was introduced.** No `.mcp.json`, `settings.json`, `hooks.json`, `.claude/settings*`, or `claude_desktop*` config file was modified by any of the 6 commits (verified separately).

## 4. Synchronous network calls — NONE

### 4.1 Python-level primitives

```bash
git show "$sha" --no-color -U0 | grep -E "^\+[^+]" | grep -v "BUILD_REQUEST" \
  | grep -E -i "\b(urllib|httpx|aiohttp|http\.client|socket|websocket|paramiko|smtp|ftplib|urlopen|fetch\()\b|requests\.(get|post|put|delete|head|patch)"
```

Result (all 6 commits, after excluding the prose token `BUILD_REQUESTs`): **none**.

**False-positive note (resolved):** the unfiltered grep matched `BUILD_REQUESTs.` (an MDTM schema noun) against the `requests\.` regex in commit `487e76b`. Verified by hand — the line is prose ("`affected BUILD_REQUESTs. The K-003 audit window resets — five`") and contains no `requests.*` library call.

### 4.2 Shell-level network CLI invocations

```bash
git show "$sha" --no-color -U0 | grep -E "^\+[^+]" \
  | grep -Eo "\b(curl|wget|nc|netcat|ssh|scp|rsync|telnet)\b\s+(http|-|[a-zA-Z])"
```

Result (all 6 commits): **none**. No commit adds a Bash invocation of `curl`, `wget`, `nc`, `ssh`, `scp`, `rsync`, or `telnet`.

## 5. Added Python imports — all stdlib or pre-existing dev dep

```bash
git show "$sha" --no-color -U0 -- '*.py' | grep -E "^\+[^+]" | grep -E "^\+(import |from )"
```

| SHA | Added import lines |
|---|---|
| `9d1e51b` | `from __future__ import annotations`, `from pathlib import Path`, `import pytest` |
| `2648be8` | `from __future__ import annotations`, `from dataclasses import dataclass`, `from pathlib import Path`, `from typing import List, Optional`, `import re`, `import subprocess` |
| `ad083b6` | `from __future__ import annotations`, `from pathlib import Path`, `from typing import Iterable`, `import difflib`, `import hashlib`, `import pytest`, `import re`, `import time` |
| `487e76b` | `from __future__ import annotations`, `from pathlib import Path`, `import hashlib`, `import pytest`, `import re` |
| `db6166e` | (no `.py` files touched) |
| `87c8254` | (no `.py` files touched) |

Each import is either:

- **Python stdlib** (`__future__`, `pathlib`, `dataclasses`, `typing`, `re`, `subprocess`, `difflib`, `hashlib`, `time`) — no install required, no network surface; OR
- **Pre-existing dev dependency** (`pytest>=7.0.0`, present in `pyproject.toml` since project inception — verified by `grep -E "pytest" pyproject.toml` returning `"pytest>=7.0.0",`).

**No new external library is introduced.**

## 6. Subprocess invocations — only Read/Grep/Glob/Bash primitives

A single `subprocess.run` was added (in `tests/audit/test_evidence_bound_tb_add_8.py` via commit `2648be8`):

```python
result = subprocess.run(
    ["grep", "-cE", "src/|/.*:[0-9]+"],
    input=text,
    capture_output=True,
    text=True,
    check=False,
)
```

Audit verdict: this shells out to **`grep`**, which is the Bash/Grep primitive expressly permitted by NFR-CONV.5. The fixture comment explicitly identifies it as an "independent oracle" that mirrors the production verification command, ensuring the test cannot drift from the rf-qa gate logic. **Compliant.**

## 7. Tool references in added markdown lines

```bash
git show "$sha" --no-color -U0 -- 'src/superclaude/agents/*.md' 'src/superclaude/skills/**/*.md' \
  | grep -E "^\+[^+]" \
  | grep -oE "\b(Write|Edit|MultiEdit|NotebookEdit|WebFetch|WebSearch|TodoWrite|BashOutput|KillBash|SlashCommand)\b" \
  | sort -u
```

| SHA | Disallowed-tool tokens in added .md lines | Context (verified by hand) |
|---|---|---|
| `9d1e51b` | none | — |
| `2648be8` | `Edit`, `Write` | Documentation of the rf-task-builder agent's **own existing** task-file emission tools ("the `## Execution Context` block, when emitted, MUST be the LAST section written in this initial Write call … Subsequent Edit-append phases land AFTER the header"). The Write/Edit primitives belong to rf-task-builder's pre-existing toolset (task-file authoring), not to the rf-qa structural gate verification path that NFR-CONV.5 governs. No new gate uses Write/Edit. |
| `ad083b6` | `Write` | One sentence describing log-line emission: "Emit a structured log line. Write `INV-010: enumerated TB-Add-* …` at every spawn boundary." This is operator-visible audit-trail emission (file-system write), part of pre-existing log infrastructure, not a new gate dependency. |
| `487e76b` | none | — |
| `db6166e` | none | — |
| `87c8254` | `WebSearch` | Appears **only inside prose example strings** ("e.g., `\"second retry\"`, `\"gap-fill round 2\"`, `\"after WebSearch exhaustion\"` — all rejected") that enumerate `escalation_ladder_exhaust_point` values the DNSP emitter MUST REJECT under R-115/R-116. The DM-003 contract pins the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`. The literal string `WebSearch` is documented as a forbidden value, not a tool call. No `WebSearch` tool invocation is introduced. |

**Verdict:** every flagged disallowed-tool token resolves to either (a) a documentation reference to rf-task-builder's pre-existing task-emission toolchain (Write/Edit for file authoring — orthogonal to the rf-qa gate-verification surface NFR-CONV.5 governs) or (b) a forbidden-value example string. **No new gate-time tool primitive outside Read/Grep/Glob/Bash is introduced.**

## 8. Acceptance criteria — verdict

| AC (phase-7-tasklist.md L138-142) | Status | Evidence § |
|---|---|---|
| Diff inspection across 6 FR commits returns zero new external dep introductions | **PASS** | §2, §5 |
| Tooling used confined to Read/Grep/Glob/Bash | **PASS** | §6, §7 |
| No new MCP servers, libraries, or synchronous network calls | **PASS** | §3, §4, §5 |
| Evidence at `TASKLIST_ROOT/artifacts/D-0085/evidence.md` | **PASS** (this file) | — |

## 9. Reproducibility — re-run recipe

Any reviewer can reproduce this audit at the current repo HEAD:

```bash
cd /config/workspace/IronClaude

# 1. Confirm the 6 SHAs are reachable
for sha in 9d1e51b 2648be8 ad083b6 487e76b db6166e 87c8254; do
  git log -1 --format="%h %s" "$sha"
done

# 2. Dependency-manifest probe
for sha in 9d1e51b 2648be8 ad083b6 487e76b db6166e 87c8254; do
  git show --name-only --format="" "$sha" \
    | grep -E "^(pyproject\.toml|uv\.lock|requirements.*\.txt|Pipfile.*|setup\.py|setup\.cfg|package\.json|package-lock\.json|yarn\.lock|Cargo\.toml|go\.mod|Gemfile)" \
    || echo "[$sha] no manifest"
done

# 3. Network-primitive probe (Python)
for sha in 9d1e51b 2648be8 ad083b6 487e76b db6166e 87c8254; do
  git show "$sha" --no-color -U0 | grep -E "^\+[^+]" | grep -v "BUILD_REQUEST" \
    | grep -E -i "\b(urllib|httpx|aiohttp|http\.client|socket|websocket|paramiko|smtp|ftplib|urlopen|fetch\()\b|requests\.(get|post|put|delete|head|patch)" \
    || echo "[$sha] no network primitives"
done

# 4. MCP-server-introduction probe
for sha in 9d1e51b 2648be8 ad083b6 487e76b db6166e 87c8254; do
  git show "$sha" --no-color -U0 | grep -E "^\+[^+]" \
    | grep -oE "mcp__[a-zA-Z0-9_-]+__" | sort -u
done

# 5. Imports introduced
for sha in 9d1e51b 2648be8 ad083b6 487e76b db6166e 87c8254; do
  git show "$sha" --no-color -U0 -- '*.py' | grep -E "^\+[^+]" | grep -E "^\+(import |from )" | sort -u
done
```

All five probes return either an empty/NONE result or a fully-classified hit (covered in §2-§7 above).

---

## 10. Cross-references

- **M1-scope baseline audit (subset):** `.dev/releases/current/task-builder-merge/artifacts/D-0015/nfr-conv-5-audit.log` (2026-05-17, MIG-001 only).
- **Roadmap NFR-CONV.5 row:** §M7 row R-142 — "all 6 FR diffs to confirm only Read/Grep/Glob/Bash used; no new MCP servers; no synchronous network calls."
- **TDD architectural-surface contract:** TDD §6.2 (COMP-001..006 modification points) — confirms each FR-CONV.X touches only the pre-ratified anchors, never a new code surface that would import a fresh library.
- **OPS-007 layout-change runbook (T07.17 / D-0097):** referenced as the downstream recipient of any NFR-CONV.5 violation finding (none triggered by this audit).

**Reviewer sign-off:** No new external dependency introduction detected. NFR-CONV.5-M7 holds.
