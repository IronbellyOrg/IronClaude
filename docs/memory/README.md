# Memory Directory

This directory holds memory and learning data used by the SuperClaude Framework's PM Agent tooling, plus the documents that describe it.

## Overview

1. **ReflexionPattern** - explicit error-learning API (`src/superclaude/pm_agent/reflexion.py`). Stores error records in `solutions_learned.jsonl` and returns the first stored row that resembles a new error. It is not loaded at session start and the PM Agent does not call it for you. See the [user guide](../user-guide/memory-system.md) for the exact contract.
2. **Workflow Metrics** - documented design for performance tracking; no tracked code writes the file (see below)
3. **Pattern Learning** - legacy pattern records; no tracked code adds to them (see below)

## Files

### solutions_learned.jsonl

**Purpose**: Error-learning storage read and appended by `ReflexionPattern`
**Format**: [JSON Lines](https://jsonlines.org/)
**Written by**: `ReflexionPattern.record_error()` (explicit calls, and the pytest recorder for `@pytest.mark.reflexion` tests whose call phase raises an exception)

The location depends on how `ReflexionPattern` is constructed: the `memory_dir` argument, else a non-empty `REFLEXION_OUTPUT_DIR`, else `docs/memory/` under the current working directory. Detailed mistake write-ups go to the sibling `mistakes/` directory (default `docs/mistakes/`).

The lookup compares lowercase, whitespace-separated word sets built from `error_type`, `error_message` (each run of digits replaced by `N`, then cut to the first 100 characters) and `test_name`. A stored row matches when shared words divided by all distinct words is 0.7 or higher (exactly 0.7 matches). Rows are read in file order and the first matching row is returned. There is no ranking and no newest-first order, and no other field, such as `status`, affects matching.

Storage is this local file only. `get_solution()` first calls a MindBase hook, but that hook is a stub that always returns `None`; no MindBase backend is implemented.

This file in the repository already contains legitimate records that use a different layout (pattern-style rows). Leave them in place. Rows without `error_type`, `error_message` or `test_name` simply never match a lookup.

**Example row** (synthetic):

```json
{"error_type": "ValueError", "error_message": "invalid port value 8080 in config", "test_name": "test_load_config", "traceback": "synthetic traceback text", "solution": "Validate the port is an integer in 1-65535 before binding", "root_cause": "Config loader accepted any string for the port", "prevention": "Add a range check to the config schema", "timestamp": "2026-01-15T10:00:00.123456"}
```

**User Guide**: See [docs/user-guide/memory-system.md](../user-guide/memory-system.md)

### reflexion.jsonl.example

**Purpose**: Six synthetic sample rows in the layout shown above (`error_type`, `error_message`, `test_name`, `traceback`, `solution`, `root_cause`, `prevention`, `timestamp`), each marked `"synthetic": true`
**Status**: Reference file only

The `synthetic` marker appears only in the sample file; the recorder does not write it and the lookup ignores it. The sample is a reference, not a schema: the recorder does not validate the dictionary it is given. Do not copy it into `solutions_learned.jsonl`.

### workflow_metrics.jsonl (documented design; nothing writes it)

**Purpose**: Task performance tracking (design intent)
**Format**: JSON Lines
**Written by**: no tracked code in this repository (the two analysis scripts only read it). Any records already in the file came from outside this repository's tracked code.

Designed to track token usage, execution time, and success rates for workflow optimization. This is separate from error learning (`solutions_learned.jsonl`).

**Example entry**:

```json
{
  "timestamp": "2025-10-17T01:54:21+09:00",
  "session_id": "abc123",
  "task_type": "bug_fix",
  "complexity": "light",
  "workflow_id": "progressive_v3_layer2",
  "layers_used": [0, 1, 2],
  "tokens_used": 650,
  "time_ms": 1800,
  "success": true
}
```

**Schema**: See [WORKFLOW_METRICS_SCHEMA.md](WORKFLOW_METRICS_SCHEMA.md)

### patterns_learned.jsonl (existing records; nothing writes it)

**Purpose**: Successful implementation patterns
**Format**: JSON Lines
**Written by**: no tracked code in this repository. Treat the existing rows as legacy records and leave them in place.

Holds reusable implementation patterns that were recorded earlier. Nothing here adds to it automatically.

### Documentation Files

#### WORKFLOW_METRICS_SCHEMA.md

Complete schema definition for workflow metrics data, including field types, descriptions, and examples.

#### pm_context.md

Historical 2025-10-17 design notes on the PM Agent's context management (progressive loading and token efficiency). Its figures are unmeasured estimates.

#### token_efficiency_validation.md

A historical 2025-10-17 validation note. Its figures are unmeasured estimates, not current results.

#### last_session.md

Session notes and context from previous work sessions.

#### next_actions.md

Planned improvements and next steps for the memory system.

## File Management

### Files nothing in this repository writes

No tracked code creates or appends to these files. They exist only as records already in the repository:

- `workflow_metrics.jsonl` - documented design; see the schema note
- `patterns_learned.jsonl` - legacy pattern records

Do not delete, rewrite or seed them. Back up before any manual change.

### When Files Are Missing

If `solutions_learned.jsonl` does not exist in a project, that is normal: it is created on the first `record_error()` call. Do not create it by hand and do not seed it with sample data.

### Backup and Maintenance

**Back up first**:

```bash
# Archive the learning files
tar -czf "$HOME/memory-backup-$(date +%Y%m%d).tar.gz" docs/memory/*.jsonl
```

Keep the archive outside the repository so it is not committed by accident.

There is no supported command for truncating, deduplicating or repairing `solutions_learned.jsonl`. If it has grown too large or contains a bad line, open it, read the rows, and edit it by hand against the backup. Do not pipe it through a command that overwrites it.

## Git and Version Control

### What to Commit

✅ **Should be committed**:

- `reflexion.jsonl.example` (sample rows)
- `patterns_learned.jsonl` (shared patterns)
- Documentation files (*.md)

❓ **Optional to commit**:

- `solutions_learned.jsonl` (error records; the repository tracks it today)
- `workflow_metrics.jsonl` (performance data)

**Recommendation**: Add `solutions_learned.jsonl` to `.gitignore` if learnings are developer-specific.

Records may contain error text from your own code. Review them before committing. Ignoring a file that Git already tracks (this repository tracks `docs/memory/solutions_learned.jsonl`) does not untrack it.

### Gitignore Configuration

If you want personal memory (not shared with team):

```bash
# Add to .gitignore
echo "docs/memory/solutions_learned.jsonl" >> .gitignore
echo "docs/memory/workflow_metrics.jsonl" >> .gitignore
```

If you want shared team memory (everyone benefits):

```bash
# Keep files in git (current default)
# All team members learn from each other's mistakes
```

## Privacy and Security

### What's Stored

`record_error()` writes the dictionary it is given as one JSON line, after setting `timestamp` to the current time (a caller-supplied `timestamp` is replaced). That can include error messages, tracebacks, task descriptions and solution text.

The recorder does **not** filter or redact anything. It will store passwords, API keys, personal data or production data if they are in the dictionary or the exception text. The pytest recorder stores the raw exception message and traceback. When `root_cause` or `solution` is non-empty, a Markdown file in the `mistakes/` directory also receives the test name, error type, error message, traceback, root cause, solution, prevention, `why_missed` and `lesson` text.

**Callers must redact before recording.**

### If a secret was already recorded

1. Back up the files outside the repository.
2. Edit the row in `solutions_learned.jsonl` by hand to remove the secret.
3. Check the matching Markdown file in the `mistakes/` directory for the same text.
4. Check your version control history if the file was committed.
5. Delete the backup once the edit is checked; it still holds the secret.

**Example** (edit by hand, keeping the rest of the row):

```json
// Before (contains secret)
{"error_message": "Auth failed with key abc123xyz"}

// After (redacted)
{"error_message": "Auth failed with invalid API key"}
```

## Performance

### File Sizes

No file-size figure has been measured. Earlier text quoted 0.5-1 KB per metrics entry and 2-5 KB per pattern; treat those as unverified estimates.

### Search Performance

No size or search-time figure has been measured for `solutions_learned.jsonl`. The lookup reads the file from the top on every call and stops at the first matching row, so a lookup that finds no match reads every line.

## Troubleshooting

### File Permission Errors

If you get `EACCES` errors, look at the owner and mode of the files (read-only):

```bash
ls -l docs/memory/*.jsonl
```

Fix the ownership or permissions by hand, after making a backup, and only on the file that failed.

### Corrupted JSON

There is no repair command. The lookup skips a line that is not valid JSON. A line that is valid JSON but not an object makes `get_statistics()` raise and can make `get_solution()` raise. A row with an `error_type`, `error_message` or `test_name` key whose value is not a string makes `get_solution()` raise when the lookup reaches it, unless an earlier row matched first. To fix any of these, back up the file, read it, and correct or remove the line by hand.

### Duplicate Entries

There is no deduplication command. After a backup, read the file and decide by hand which rows to keep. The lookup returns the first matching row in file order, so an earlier duplicate answers before a later one.

## Related Documentation

- **User Guide**: [docs/user-guide/memory-system.md](../user-guide/memory-system.md)
- **Implementation**: `src/superclaude/pm_agent/reflexion.py`
- **Pytest plugin**: `src/superclaude/pytest_plugin.py`
- **Architecture notes**: [docs/reference/pm-agent-autonomous-reflection.md](../reference/pm-agent-autonomous-reflection.md)
- **PM Agent definition**: [src/superclaude/agents/pm-agent.md](../../src/superclaude/agents/pm-agent.md)

## Quick Commands

```bash
# View all learnings
jq . docs/memory/solutions_learned.jsonl

# Count entries
wc -l docs/memory/solutions_learned.jsonl

# Search for specific topic
grep -i "auth" docs/memory/solutions_learned.jsonl | jq .

# Last 5 entries
tail -5 docs/memory/solutions_learned.jsonl | jq .
```

---

**Last Updated**: 2025-10-30
**Maintained by**: SuperClaude Framework Team
