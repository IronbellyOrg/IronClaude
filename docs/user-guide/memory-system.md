# Memory System Guide

SuperClaude includes an error-learning helper called **ReflexionPattern** (`src/superclaude/pm_agent/reflexion.py`). It stores error records in a local JSONL file and looks up an earlier record that resembles a new error.

This guide describes what the code does today. Where something is not implemented or not measured, it says so.

## Overview

- **Explicit API**: you (or code you write) call `get_solution()` and `record_error()`. Nothing in the framework calls `get_solution()`. The only automatic `record_error()` call is the opt-in pytest recorder described below.
- **Local file only**: records live in a JSONL file on disk. There is no database and no external backend.
- **No setup**: the constructor creates the memory directory and its sibling `mistakes/` directory if they are missing.
- **Exports**: `ReflexionPattern` is importable from `superclaude` and from `superclaude.pm_agent`.

## What is and is not automatic

| Behavior | Status |
|----------|--------|
| Loading `solutions_learned.jsonl` at session start | **Not implemented.** (The PM agent definition describes a separate Serena-memory restore and agent-written `docs/mistakes/` notes; neither uses this class.) |
| PM Agent capturing every error into this file or applying stored fixes | **Not implemented.** The PM agent definition does not reference `ReflexionPattern`. |
| MindBase semantic search | **Not implemented.** `_search_mindbase()` is a stub that always returns `None`. |
| Recording a failing test | **Implemented, opt-in.** A test marked `@pytest.mark.reflexion` whose call phase ends with an exception is recorded by the pytest plugin hook. |

## Storage

### Where files go

`ReflexionPattern` picks its directory in this order:

1. The `memory_dir` argument, if you pass one.
2. The `REFLEXION_OUTPUT_DIR` environment variable, if it is set and not empty.
3. `docs/memory/` under the current working directory.

Given a memory directory `M`, it uses:

```
M/solutions_learned.jsonl      # one JSON object per line, append-only
M/../mistakes/                 # sibling directory, default docs/mistakes/
```

The constructor creates both directories if they are missing. The file itself is created on the first `record_error()` call.

**Format**: [JSON Lines](https://jsonlines.org/), one JSON object per line.

### What `record_error()` writes

`record_error(error_info)` takes a dictionary from the caller and:

1. sets `timestamp` in that same dictionary to the current local time (ISO format), replacing any `timestamp` the caller supplied;
2. appends the dictionary to `solutions_learned.jsonl` as one JSON line;
3. if the dictionary has a non-empty `root_cause` or `solution`, also writes a Markdown file `<test_name>-YYYY-MM-DD.md` (`unknown` when there is no `test_name`) into the mistakes directory. The file name is built directly from `test_name`, and a second record for the same test on the same day overwrites that Markdown file (the JSONL row is still appended).

Fields the code reads: `error_type`, `error_message`, `test_name` (used for matching), and `solution`, `root_cause`, `prevention` (returned from a lookup). `traceback`, `why_missed` and `lesson` are used only when the mistake document is written (they are still stored in the JSONL row). Any other key is stored in the JSONL row and otherwise ignored. The recorder does not validate the dictionary.

**Example row** (synthetic, not a real record):

```json
{"error_type": "ValueError", "error_message": "invalid port value 8080 in config", "test_name": "test_load_config", "traceback": "synthetic traceback text", "solution": "Validate the port is an integer in 1-65535 before binding", "root_cause": "Config loader accepted any string for the port", "prevention": "Add a range check to the config schema", "timestamp": "2026-01-15T10:00:00.123456"}
```

`docs/memory/reflexion.jsonl.example` holds six synthetic rows in this layout. The first row is the example row above plus a `"synthetic": true` marker. The marker appears only in the sample file: the recorder does not write it and the lookup ignores it. The sample is a reference, not a schema: the recorder does not validate the dictionary it is given. Do not copy the file into `docs/memory/solutions_learned.jsonl`.

## Lookup

`get_solution(error_info)` works like this:

1. Build a signature from the keys that are present, joined with ` | `: `error_type`, then `error_message`, then `test_name`. In the message, every run of digits becomes `N` and only the first 100 characters are kept.
2. Read `solutions_learned.jsonl` from the top, in file order. Lines that are not valid JSON are skipped. Each stored row gets a signature built the same way.
3. Two signatures match when their word sets overlap enough. Words are the lowercase, whitespace-separated tokens of the signature (the ` | ` separator counts as one token). The test is `shared words / all distinct words >= 0.7`. Exactly 0.7 counts as a match.
4. The **first matching row** is returned as `{"solution", "root_cause", "prevention", "timestamp"}`. Missing fields come back as `None`.

What this means in practice:

- There is no ranking, no "best match", and no newest-first ordering. A row earlier in the file wins over a later one.
- A matching row with no `solution` is still returned (with `solution` set to `None`).
- No other field, such as `status` or a "deprecated" marker, affects whether a row matches.
- A row with none of `error_type`, `error_message` or `test_name` has an empty signature and never matches.
- If the error you look up has none of `error_type`, `error_message` or `test_name`, nothing matches.
- If nothing matches, the result is `None`.

**Worked examples** (all computed from the rules above; the fourth pair is `error_message` only, with no `error_type` or `test_name`):

```
Stored:   ValueError | invalid port value N in config | test_load_config
Current:  ValueError | invalid port value N in config file | test_load_config
Shared 9 words / 10 distinct words = 0.90  -> match

Stored:   ValueError | invalid port value N in config | test_load_config
Current:  ValueError | port value N in settings | test_load_config
Shared 7 words / 10 distinct words = 0.70  -> match (exactly 0.7 counts)

Stored:   ValueError | invalid port value N in config | test_load_config
Current:  ValueError | invalid timeout value N in settings | test_load_settings
Shared 6 words / 12 distinct words = 0.50  -> no match

Stored:   JWT validation failed secret not found
Current:  JWT token validation failed missing secret
Shared 4 words / 8 distinct words = 0.50  -> no match
```

Earlier versions of this guide called the fourth pair an 87.5% match; it is 50% and does not match.

Matching uses the whole signature, so a matching `error_type` and `test_name` raise the score, and a message that differs in a few words can still match.

## Using it

### Explicit API

```python
import tempfile
from pathlib import Path
from superclaude import ReflexionPattern

with tempfile.TemporaryDirectory() as tmp:
    # Nest the memory dir so the sibling "mistakes" folder also stays inside tmp.
    reflexion = ReflexionPattern(memory_dir=Path(tmp) / "docs" / "memory")

    error_info = {
        "error_type": "ValueError",
        "error_message": "invalid port value 9090 in config file",
        "test_name": "test_load_config",
    }

    known = reflexion.get_solution(error_info)   # None: the temporary store is empty
    if known is None:
        error_info["solution"] = "Validate the port before binding"
        error_info["root_cause"] = "Config loader accepted any string"
        reflexion.record_error(error_info)       # appends a row, adds "timestamp"
```

This example writes only inside the temporary directory: the JSONL row goes to `<tmp>/docs/memory/solutions_learned.jsonl`, the mistake document goes to the sibling `<tmp>/docs/mistakes/`, and everything is deleted when the `with` block ends. For real use, pass your own `memory_dir`.

`get_statistics()` returns the number of rows, the number of rows with a non-empty `solution`, and that share as a percentage under the key `solution_reuse_rate`. Despite the name it counts rows that have a solution; it does not measure how often a solution was reused.

### Pytest recorder (separate from the API above)

The pytest plugin (`src/superclaude/pytest_plugin.py`) records a test only when it carries `@pytest.mark.reflexion` and its call phase ends with an exception (`call.excinfo` is set). That covers an ordinary failure and can also cover a skip or xfail raised inside the test body. It builds a dictionary with `test_name`, `test_file`, `error_type`, `error_message` and `traceback`, and calls `record_error()`. It does not call `get_solution()` and does not add a solution, so no mistake document is written for these records.

Outside this repository's own test suite, that recorder writes to `docs/memory/` under the current directory unless `REFLEXION_OUTPUT_DIR` is set and not empty. The `reflexion_pattern` fixture sets that variable and `memory_dir` to a temporary directory.

In this repository, `tests/conftest.py` sets `REFLEXION_OUTPUT_DIR` for every test, so a `ReflexionPattern` built without `memory_dir` writes into that test's temporary directory, and it checks at the end of the session that no new `.md` files appeared in `docs/mistakes/` and that `docs/memory/solutions_learned.jsonl` kept the same byte size. Keep that guard in place; see `tests/unit/test_reflexion_pollution_guard.py`.

## Privacy

The recorder stores whatever the dictionary contains. It does **not** remove passwords, tokens, API keys or personal data, in either the JSONL row or the mistake document. The pytest recorder stores the raw exception message and traceback.

- Redact secrets in the dictionary **before** calling `record_error()`.
- If a secret is already stored: copy the file to a backup outside the repository, edit the row by hand, check the Markdown files in the mistakes directory for the same text, check your version-control history if the file was committed, then delete the backup, because it holds the secret too.
- Records are plain files in your project. Committing `docs/memory/` shares them with everyone who can read the repository.

## Inspecting and maintaining the data

These commands only read:

```bash
# View all rows
jq . docs/memory/solutions_learned.jsonl

# Count lines
wc -l docs/memory/solutions_learned.jsonl

# Find rows that mention a word
grep -i "port" docs/memory/solutions_learned.jsonl | jq .
```

Make a backup before any manual edit, and review the diff yourself:

```bash
cp docs/memory/solutions_learned.jsonl "$HOME/solutions_learned.jsonl.bak"
```

Keep the backup outside the repository so it is not committed by accident.

Do not delete, deduplicate, truncate or rotate this file with a script. It may hold rows you want to keep, including rows written for other purposes. Remove or fix a line by editing it by hand after you have read it. The lookup skips a line that is not valid JSON. A line that is valid JSON but not an object makes `get_statistics()` raise and can make `get_solution()` raise. A row with an `error_type`, `error_message` or `test_name` key whose value is not a string makes `get_solution()` raise when the lookup reaches it, unless an earlier row matched first.

## Performance

No token-savings, latency, file-size or error-recurrence figures have been measured for this system. Earlier versions of this guide quoted percentages and timings that no measurement in this repository supports; they have been removed. The lookup reads the file from the top on every call and stops at the first matching row, so a lookup with no match reads every line; how long that takes has not been measured.

## Troubleshooting

### The file does not exist

Normal until the first `record_error()` call.

### A stored row is not found

1. Check the signature: the row needs `error_type`, `error_message` or `test_name`.
2. Compare the word overlap by hand (see the worked example). It must reach 0.7.
3. Remember that the first matching row is returned, so an earlier row may be answering instead.

### Records appear in an unexpected directory

Check the directory order above: the `memory_dir` argument, then `REFLEXION_OUTPUT_DIR`, then the current working directory.

## Related files

- **Implementation**: `src/superclaude/pm_agent/reflexion.py`
- **Pytest plugin**: `src/superclaude/pytest_plugin.py`
- **Tests**: `tests/unit/test_reflexion.py`, `tests/unit/test_reflexion_pollution_guard.py`
- **Sample rows**: `docs/memory/reflexion.jsonl.example`
- **Architecture notes**: `docs/reference/pm-agent-autonomous-reflection.md`

---

**Questions?** Open an issue on GitHub (the former FAQ page, `docs/FAQ.md`, no longer exists).
