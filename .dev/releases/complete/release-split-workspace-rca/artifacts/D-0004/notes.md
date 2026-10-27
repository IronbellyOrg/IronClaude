# D-0004 -- Implementation notes

## Edit location

The target reverse-loop (`.claude/skills/*/` → check absence in `src/superclaude/skills/`) was previously a 7-line block. After the edit it is 12 lines: the inner branch now tests `[ ! -f "$$skill_dir/SKILL.md" ] && [ ! -f "$$skill_dir/skill.md" ]` and emits one of two messages.

The task description cited "lines 179-187"; the actual loop was at lines 176-182 in the current Makefile (line numbers had shifted slightly since the phase tasklist was generated). The target block was unambiguous — the only reverse-loop iterating `.claude/skills/*/` that emits the "(not distributable!)" message — so the edit applied cleanly.

## Defensive change

Added `[ -d "$$skill_dir" ] || continue;` at the top of the loop. Without it, the loop expands to the literal glob `.claude/skills/*/` when the directory is empty, which would feed `.claude/skills/*` as a name into the SKILL.md branch and emit a confusing message. The guard is a no-op when the directory has content.

The same guard pattern is *not* present in the forward-loop (`src/superclaude/skills/*/`) above it, but that loop has stronger structural guarantees (the source tree is the canonical input) and was out of scope for this task.

## Message formatting

The new message uses an em-dash (U+2014, `—`) as specified by FR-L2.1 verbatim. The acceptance criterion explicitly notes "em-dash exact"; a hyphen-minus (`-`) or en-dash (`–`) would fail review.

## SKILL.md vs skill.md

The `sync-dev` target accepts either `SKILL.md` or `skill.md` as a marker for a real skill directory. The new branch mirrors that tolerance so a legitimate lowercase-named skill does not get mis-classified as a workspace.

## Tie-breaker note (Section 4.9)

T02.01 is scoped to `verify-sync` only; no tie-breaker applies. The `*-workspace/` suffix blocklist (T02.02) lands in `lint-architecture` per the Section 4.9 tie-breaker rationale recorded in the phase tasklist.
