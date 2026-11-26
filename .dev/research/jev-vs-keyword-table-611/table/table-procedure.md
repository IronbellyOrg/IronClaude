# Table procedure: how the keyword table is applied (issue 611)

**This is a procedure to be followed by a person or session. It is not evidence, and it holds no filled-in prompt, label or answer.**
The evidence it produces is `.dev/research/jev-vs-keyword-table-611/table/table-answers.jsonl` and the filled
`.dev/research/jev-vs-keyword-table-611/table/table-provenance.md`.

## The table, as it stands

The keyword table is step 2 of the Steps of `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`. Its six cue rows (lines 153 to 158 of that
file) and its ambiguity rule (line 159) are quoted here exactly:

```text
   - Stack trace, exception name, `undefined`/`null`/`NameError` → `bug`
   - "tsc", "ts(", "compiled", "lint", "build", `make`, CI log fragments → `build`
   - "slow", "latency", "p99", "memory", "leak", "too long to load", "takes forever", "hangs", profiler output → `performance`
   - "production", "deploy", "container", "env var", "service won't start" → `deployment`
   - "auth", "token", "leak", "exposed", "CVE", "vulnerab" → `security`
   - "pytest", "jest", "flake", "intermittent", "passing locally" → `test`
   - On ambiguity, leave `--type` unset and treat all agent specialties as candidates for Tier 2. Keep "leak" in both rows: it can mean resource leakage or sensitive-data disclosure, so ambiguous leak reports must not discard security candidates.
```

The right-hand word of each cue row is the type (`bug`, `build`, `performance`, `deployment`, `security`, `test`).

## How it is applied: as written, nothing more

1. A row matches a prompt when the prompt holds at least one cue of that row as written. The structural cues (a stack trace, an exception
   name, CI log fragments, profiler output) match when the prompt visibly holds one.
2. Exactly one row matches: the answer is that row's type.
3. No cue of any row matches: the answer is unset (`null`).
4. Cues from two or more rows match: the answer is unset (`null`). The word "leak" stays in both the `performance` row and the `security`
   row, so a prompt whose only cue is "leak" matches two rows and is unset.
5. There is no first-match parser: the order of the rows decides nothing.
6. There is no extra inference: nothing outside the quoted cues, no guess about what the prompt "really" means.

## Before the table is applied

1. **Reading step, before `gate.py freeze-corpus`.** A person reads the six definitions in `.dev/research/jev-vs-keyword-table-611/questions.py`
   once and records that with:
   `uv run python .dev/research/jev-vs-keyword-table-611/harness/events.py owner-input --evidence .dev/research/jev-vs-keyword-table-611/questions.py --note "<who read the six definitions>"`
2. **Gate 1 first.** The corpus and its labels are frozen (`uv run python .dev/research/jev-vs-keyword-table-611/harness/gate.py freeze-corpus`) and `uv run python .dev/research/jev-vs-keyword-table-611/harness/gate.py gate1` prints `PASS`. The table is applied
   only after that, and every answer is stored before any call to Jev is made.
3. **Prompts only.** The applier receives each prompt's id and text and nothing else: never a label, never the labeller's notes, never any
   Jev answer.
4. **A different applier.** The applier is a different person or session from the labeller.

## What is recorded

One JSON object per line in `.dev/research/jev-vs-keyword-table-611/table/table-answers.jsonl`, one line per corpus prompt:

| Field | Holds |
|---|---|
| `prompt_id` | the `id` of the corpus row |
| `answer` | one of the six types, or `null` for an unset answer |
| `cues` | the cue phrases found in the prompt (a list, empty when none) |
| `rows` | the names of the rows those cues belong to (a list, empty when none) |
| `method` | how the table was applied: `person reading the prose` or `skill execution` |

Then fill `.dev/research/jev-vs-keyword-table-611/table/table-provenance.md`.

## Freezing

Run `uv run python .dev/research/jev-vs-keyword-table-611/harness/gate.py freeze-table`. It refuses unless Gate 1 passes at that moment and both the answers file and the provenance file exist, and it
refuses to replace a frozen table.
