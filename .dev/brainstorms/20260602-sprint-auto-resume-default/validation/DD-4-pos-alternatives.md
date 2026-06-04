# Variant 2 — STRONGEST ALTERNATIVES to the design's tiered+sha approach

## Alt A — Pure git-diff-based drift
Use `git diff @{upstream} -- <phase files>` as the sole signal; classify hunks (whitespace-only via `git diff --ignore-all-space`, vs material).

- Strength: `--ignore-all-space` / `--ignore-blank-lines` give *free, correct* cosmetic-vs-material classification — directly satisfies AC-4 without bespoke normalization.
- Strength: characterizes *what* changed (FR-3.2), which the requirements explicitly want.
- Fatal weakness: tasklists are frequently untracked / dirty / detached-HEAD / no upstream. R-offline. Cannot be the *only* tier. FR-3.2 itself says "where a git remote is available."

## Alt B — Full-tasklist content-hash binary guard (today's rerun SHA-guard, unchanged)
Single hash equality; mismatch ⇒ refuse/low-confidence. This is literally what rerun-tasks does today (T8.1 mid-flight guard, rerun_tasks.py:1387).

- Strength: trivial, already implemented, zero new parsing.
- Fatal weakness: binary. A trailing space ⇒ mismatch ⇒ refuse. Directly VIOLATES AC-4 ("no full-phase redo for whitespace"). This is the exact brittleness FR-3.3 was written to kill ("not a brittle byte-hash").

## Alt C — mtime-based
Compare file mtime vs recorded run time.

- Fatal weakness: mtime changes on `touch`, checkout, rsync, editor save-without-change. No content signal. Cannot distinguish cosmetic from material. Strictly worse than hashing. Reject outright.

## Synthesis position
The design's *tiering* is correct and beats all three single-signal alternatives — but it must:
1. Borrow Alt A's `git diff --ignore-all-space` as the cosmetic classifier in Tier 1/2 (the missing whitespace normalization), rather than claiming Tier 0 already handles it.
2. Hash the per-phase file (Alt B's actual target), not index_path.
3. Treat git as an *annotator/booster*, never the sole tier (offline safety).
