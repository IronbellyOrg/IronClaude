# Diff Analysis: spec Comparison

## Metadata

- Generated: 2026-11-04T19:21:00Z
- Variants compared: 2 (variant-1-opus-architect.md, variant-2-sonnet-refactorer.md)
- Total differences found: 10
- Categories: structural (1), content (5), contradictions (1), unique (3), shared assumptions (3)
- Output-directory note: brainstorm passed `--output <brainstorm>/adversarial/`; artifacts are written there directly (no nested `adversarial/adversarial/`).

Orchestrator verification done before this analysis (Bash, this session): CPython 3.11.15 `Path('/tmp/nul\x00dir').resolve()` raises `ValueError: lstat: embedded null character in path`; a two-link loop raises `RuntimeError`; CI runs Python 3.10 (`.github/workflows/test.yml:22,60,86,149`), `requires-python = ">=3.10"` (pyproject.toml:16); real CLI with `CLAUDE_CONFIG_DIR` removed and `HOME` pinned wrote only under `HOME/.claude` and left the other profile untouched; a `--scope user` install beside an existing `--scope project` copy succeeded and both records coexist.

## Structural Differences

| # | Area | Variant 1 (architect) | Variant 2 (refactorer) | Severity |
|---|---|---|---|---|
| S-001 | Document shape | Same H2 set as requested; prose rationale lists | Same H2 set plus YAML frontmatter and a risk table | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Severity |
|---|---|---|---|---|
| C-001 | Finding 1 except tuple | `(OSError, RuntimeError)` | `(OSError, RuntimeError, ValueError)`: embedded NUL in a JSON path raises `ValueError` on 3.11 and 3.13 | Medium |
| C-002 | Finding 1 regression test mechanism | Real loop plus a monkeypatched `setup.Path.resolve` wrapper that raises, so it fails on every Python | Two real bad paths: a self-symlink loop (fails on 3.10-3.12) and a NUL path (fails on every version); no monkeypatching of pathlib | Medium |
| C-003 | Finding 2: record without a `scope` key | Strict: not user scope (one extra install at worst) | Default to user scope (`e.get("scope", "user")`), keeps today's behaviour for scopeless records | Low |
| C-004 | Finding 3 regression test setup | `CLAUDE_CONFIG_DIR` points at a profile holding a foreign `ironclaude`; home has no registry; asserts commands plus env (`HOME`, no `CLAUDE_CONFIG_DIR`) for every call | Move-pin fixture; loops over `CLAUDE_CONFIG_DIR` = other dir and `""`; adds `SENTINEL` env var to prove the rest of the environment is kept | Medium |
| C-005 | Existing test 397 update | `HOME == str(home)` and `GIT_CONFIG_VALUE_0` absent | Also asserts `CLAUDE_CONFIG_DIR` absent; `GIT_CONFIG_COUNT` absent | Low |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Impact |
|---|---|---|---|---|
| X-001 | Treatment of a record lacking `scope` | "Strict `scope == "user"` ... A record without it is not provably user scope" | "A record without a `scope` key is treated as user scope" | Low (the real CLI always writes `scope`; both outcomes are non-fatal) |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | 2 | `ValueError` from an embedded NUL byte is a second reachable escape from line 292 | High |
| U-002 | 2 | Real-input finding-1 test (no pathlib monkeypatch) | Medium |
| U-003 | 1 | Finding-3 test mirrors the spec's required scenario (foreign `ironclaude` in the `CLAUDE_CONFIG_DIR` profile) and checks the foreign profile is never acted on | High |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | Both pick option C | With `CLAUDE_CONFIG_DIR` removed and `HOME=home`, the CLI reads and writes `home/.claude` only | STATED (variant 2 flags it as unverified; the orchestrator proved it with the real CLI) | No |
| A-002 | Both pick option C | `marketplace add`, `plugin install`, `plugin update` need no credentials kept in the user's `CLAUDE_CONFIG_DIR` profile | UNSTATED in variant 1; UNVERIFIED in variant 2 | Yes |
| A-003 | Both keep the catalog at `home/.claude/ironclaude-marketplace` | Under C a user who runs Claude Code with `CLAUDE_CONFIG_DIR` gets no plugins in that profile; this user-facing change needs no CHANGELOG note | UNSTATED | Yes |
| A-004 | Both use a project-only record as "not installed" | The real CLI accepts a user-scope install beside a project copy | STATED (proved by the orchestrator) | No |

### Promoted

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-002 | No plugin command needs auth from the user's `CLAUDE_CONFIG_DIR` profile | Option C | Medium: if wrong, installs fail (non-fatal, reported) for `CLAUDE_CONFIG_DIR` users | Open |
| A-003 | The behaviour change for `CLAUDE_CONFIG_DIR` users needs no user-facing note | Option C | Low: documentation only | Open |

## Summary

- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 1
- Total unique contributions: 3
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-004, U-001, U-003
- Similarity check: 7 debatable points (S-001, C-001..C-005, X-001) plus 2 promoted assumptions; differences exceed 10%, so the debate runs (Round 1 only, depth quick).
