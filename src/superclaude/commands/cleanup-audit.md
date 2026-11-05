---
name: cleanup-audit
description: "Multi-pass read-only repository audit producing evidence-backed cleanup recommendations"
category: utility
complexity: high
allowed-tools: Read, Glob, Grep, Bash, TodoWrite, Task, Write, Skill
mcp-servers: [codegraph, context7]
personas: [analyzer, architect, devops, qa, refactorer]
---

# /sc:cleanup-audit - Multi-Pass Repository Audit

## Repository Context

- Total tracked files: !`git ls-files | wc -l`
- In-scope after default excludes: !`git ls-files | grep -Ev '^(\.|.*/\.)|^_bmad/|^_bmad-output/|^_planning-input/|^\.claude-audit/' | wc -l`
- File breakdown: !`git ls-files | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -15`
- Repo size: !`du -sh . --exclude=.git --exclude=node_modules 2>/dev/null`
- Current branch: !`git branch --show-current`
- Last commit: !`git log --oneline -1`

## Target Scope

- Target: $ARGUMENTS
- Files in scope: !`find ${0:-.} -type f -not -path '*/.git/*' -not -path '*/node_modules/*' | wc -l`
- File types: !`find ${0:-.} -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10`

## Usage

```
/sc:cleanup-audit [target-path] [--pass surface|structural|cross-cutting|all] [--batch-size N] [--focus infrastructure|frontend|backend|all]
/sc:cleanup-audit --pass surface --unattended --report-dir DIR   # worker mode, see Unattended mode
```

### Arguments

- **target-path**: Directory to audit (default: `.` for entire repo)
- **--pass**: Audit pass to run (`surface` = Pass 1, `structural` = Pass 2, `cross-cutting` = Pass 3, `all` = sequential 3-pass)
- **--batch-size**: Files per agent batch (default: 50 for surface, 25 for structural, 30 for cross-cutting)
- **--focus**: Domain filter for targeted auditing (`infrastructure`, `frontend`, `backend`, `all`)
- **--unattended**: Worker mode: no step waits for a person; see Unattended mode
- **--report-dir**: With `--unattended`, the directory that holds the worker contract (required; the command has no other directory flag)

## Behavioral Summary

Spawns parallel subagents in 3 escalating passes: Pass 1 (Haiku surface scan classifying files as DELETE/REVIEW/KEEP), Pass 2 (Sonnet structural audit producing mandatory 8-field per-file profiles), Pass 3 (Sonnet cross-cutting comparison producing duplication matrices with overlap percentages). Each pass uses evidence-gated classification requiring grep proof for every recommendation. Quality validated via spot-check sampling (10%). Reports written to `.claude-audit/`. Incremental checkpointing enables resume-from-checkpoint on session interruption.

## Examples

### Full Repository Surface Scan

```
/sc:cleanup-audit
```

Runs Pass 1 surface scan on the entire repository. Uses Haiku agents to classify every file as DELETE/REVIEW/KEEP. Produces per-batch reports and a consolidated summary at `.claude-audit/pass1-summary.md`.

### Structural Audit of Source Directory

```
/sc:cleanup-audit src/ --pass structural --batch-size 25
```

Runs Pass 2 structural audit on `src/` directory only. Produces mandatory 8-field profiles for each file. Requires Pass 1 results as input context. Validates per-file evidence quality.

### Infrastructure Cross-Cutting Sweep

```
/sc:cleanup-audit --pass cross-cutting --focus infrastructure
```

Runs Pass 3 cross-cutting comparison on infrastructure files (Docker, CI/CD, deploy scripts, configs). Produces duplication matrix with overlap percentages. Groups similar files for comparative analysis.

### Complete 3-Pass Audit

```
/sc:cleanup-audit --pass all --focus all
```

Runs all 3 passes sequentially with quality gates between each pass. Pass 1 inventory feeds Pass 2 deep audit, which feeds Pass 3 cross-cutting sweep. Produces final consolidated report with executive summary, prioritized action items, and discovered issues registry.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:cleanup-audit-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill.

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:cleanup-audit` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only: the command has no directory flag, and its audit output stays in the fixed `.claude-audit/`. Without `--report-dir` the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is `.claude-audit/pass<N>-summary.md` for one pass (`surface` is 1, `structural` 2, `cross-cutting` 3) or `.claude-audit/final-report.md` for `--pass all`; `artifacts` lists `.claude-audit/progress.json` and the batch reports. A run that finishes every requested pass is succeeded; one that stops after a checkpoint is partial, and a rerun resumes from `.claude-audit/progress.json`.
- **Concurrency.** `.claude-audit/` is fixed, so only one audit at a time runs per worktree (WC-11 in `~/.claude/WORKER-CONTRACT.md`).
- **Write scope.** `.claude-audit/` plus `<report-dir>/return-contract.yaml`; the read-only rule for repository files is unchanged.
- **Gates.** None, and no person-mode flag. Nested invocations: none; its Agent-tool subagents are unchanged.
- **Outward actions.** It pushes, commits and stages nothing.

## Boundaries

**Will:**

- Analyze every file in scope with evidence-backed classification (DELETE/CONSOLIDATE/MOVE/FLAG/KEEP)
- Produce machine-checkable reports with mandatory per-file profiles and verifiable grep citations
- Track coverage metrics and transparently report what was and was not audited

**Will Not:**

- Modify, delete, move, or rename any repository file during the audit
- Make assumptions from filenames alone — every classification requires reading content and tracing references
- Mark files as DELETE without grep proof of zero references and confirmed absence of dynamic loading

## CRITICAL BOUNDARIES

**READ-ONLY AUDIT — NO REPOSITORY MODIFICATIONS**

**Explicitly Will NOT**:

- Edit, delete, move, or rename any existing repository file
- Execute cleanup recommendations — human review gate is mandatory
- Modify CI/CD pipelines, configs, or any operational infrastructure
- Make speculative deletions based on filename patterns without evidence

**Output**: Audit reports written to `.claude-audit/` directory only:

- Per-batch reports (one per agent invocation)
- Per-pass summary reports (consolidated findings)
- Final report (executive summary + prioritized actions)
- progress.json (checkpoint state for resume capability)

Except under `--unattended`: `<report-dir>/return-contract.yaml` is also written (see Unattended mode).

**Next Step**: Use `/sc:cleanup` to execute safe recommendations, then `/sc:test` to verify no regressions, then `/sc:git` to commit changes.
