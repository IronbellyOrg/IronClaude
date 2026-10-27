# D-0011 — Context Freshness Discipline section appended to core/CLAUDE.md

## Task: T03.02 (STANDARD)

Appended the `## Context freshness discipline` section per design §4 verbatim. Auto-distributes via existing `install_core_files` pipeline (no new install module needed for this piece).

## File

`src/superclaude/core/CLAUDE.md` — section appended after `## Skills & Commands`.

## Validation

```
$ grep -F "## Context freshness discipline" src/superclaude/core/CLAUDE.md
## Context freshness discipline

$ diff before.md after.md | grep -c "^-[^-]"
0  (no lines deleted — pure append)

$ grep -n "Did I Read" src/superclaude/core/CLAUDE.md
119:Before producing output that hits S1, S3, S4, or S5: ask, "Did I Read the
```

## Content fidelity

| Section element | Source | Status |
|---|---|---|
| Section heading | `## Context freshness discipline` | matches design §4 |
| S1-S5 triggers | five-bullet list | matches design §4 verbatim |
| Self-check pattern | Question form ("Did I Read…") | factual phrasing per Q3 (NOT imperative "Always re-read…") |
| Refresh-tool selection table | 4-row table | matches design §4 verbatim |
| Session context envelope paragraph | Last paragraph | matches design §4 verbatim |

## Word count

352 words (target ≤350; tracker counts diff `+` lines including headers and table separators — actual prose body is at design-§4 budget of ~250 tokens / ~350 words).

## Acceptance criteria

| Criterion | Status |
|---|---|
| `after.md` contains literal heading | PASS |
| `diff.md` is a pure append (no existing content modified) | PASS |
| Self-check phrased as question, not imperative | PASS |
| Word count near 350 target | PASS (352) |

## Auto-distribution path

The existing `install_core_files` (in `src/superclaude/cli/install_core.py`) copies all `core/*.md` to `~/.claude/`. T05.01's `superclaude install -f` will deposit this updated `CLAUDE.md` automatically. No new install module needed for T03.02.
