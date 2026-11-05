---
name: sc:index-repo
description: Repository Indexing - 94% token reduction (58K → 3K)
---

# Repository Index Creator

📊 **Index Creator activated**

## Problem Statement

**Before**: Reading all files → 58,000 tokens every session
**After**: Read PROJECT_INDEX.md → 3,000 tokens (94% reduction)

## Index Creation Flow

### Phase 1: Analyze Repository Structure

**Parallel analysis** (5 concurrent Glob searches):

1. **Code Structure**

   ```
   src/**/*.{ts,py,js,tsx,jsx}
   lib/**/*.{ts,py,js}
   superclaude/**/*.py
   ```

2. **Documentation**

   ```
   docs/**/*.md
   *.md (root level)
   README*.md
   ```

3. **Configuration**

   ```
   *.toml
   *.yaml, *.yml
   *.json (exclude package-lock, node_modules)
   ```

4. **Tests**

   ```
   tests/**/*.{py,ts,js}
   **/*.test.{ts,py,js}
   **/*.spec.{ts,py,js}
   ```

5. **Scripts & Tools**

   ```
   scripts/**/*
   bin/**/*
   tools/**/*
   ```

### Phase 2: Extract Metadata

For each file category, extract:

- Entry points (main.py, index.ts, cli.py)
- Key modules and exports
- API surface (public functions/classes)
- Dependencies (imports, requires)

### Phase 3: Generate Index

Create `PROJECT_INDEX.md` with structure:

```markdown
# Project Index: {project_name}

Generated: {timestamp}

## 📁 Project Structure

{tree view of main directories}

## 🚀 Entry Points

- CLI: {path} - {description}
- API: {path} - {description}
- Tests: {path} - {description}

## 📦 Core Modules

### Module: {name}
- Path: {path}
- Exports: {list}
- Purpose: {1-line description}

## 🔧 Configuration

- {config_file}: {purpose}

## 📚 Documentation

- {doc_file}: {topic}

## 🧪 Test Coverage

- Unit tests: {count} files
- Integration tests: {count} files
- Coverage: {percentage}%

## 🔗 Key Dependencies

- {dependency}: {version} - {purpose}

## 📝 Quick Start

1. {setup step}
2. {run step}
3. {test step}
```

### Phase 4: Validation

Quality checks:

- [ ] All entry points identified?
- [ ] Core modules documented?
- [ ] Index size < 5KB?
- [ ] Human-readable format?

---

## Usage

**Create index**:

```
/index-repo
```

**Update existing index**:

```
/index-repo mode=update
```

**Quick index (skip tests)**:

```
/index-repo mode=quick
```

**Worker mode (no person at the keyboard)**:

```
/index-repo --unattended --report-dir <dir>
```

---

## Token Efficiency

**ROI Calculation**:

- Index creation: 2,000 tokens (one-time)
- Index reading: 3,000 tokens (every session)
- Full codebase read: 58,000 tokens (every session)

**Break-even**: 1 session
**10 sessions savings**: 550,000 tokens
**100 sessions savings**: 5,500,000 tokens

---

## Output Format

Creates two files:

1. `PROJECT_INDEX.md` (3KB, human-readable)
2. `PROJECT_INDEX.json` (10KB, machine-readable)

`PROJECT_INDEX.md` and `PROJECT_INDEX.json` are written at the root of the repository being indexed.

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/index-repo` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only: the command has no directory flag, and its two files stay at the root of the repository. Without `--report-dir` the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is `PROJECT_INDEX.md` and `artifacts` lists `PROJECT_INDEX.json`. The run is succeeded when both files were written, and failed otherwise.
- **Resume.** `mode=update` refreshes an existing index; a retry uses a fresh report directory.
- **Gates.** None, and no person-mode flag. Nested invocations: none.
- **Outward actions.** It pushes, commits and stages nothing.

---

**Index Creator is now active.** Run to analyze current repository.
