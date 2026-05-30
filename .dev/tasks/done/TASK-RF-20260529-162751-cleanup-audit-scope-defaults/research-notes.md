# Research Notes: Bake hidden + BMAD scope exclusions into sc:cleanup-audit defaults

**Date:** 2026-05-29
**Scenario:** A (highly explicit — exact diffs in hand from prior session)
**Depth Tier:** Quick
**Track Count:** 1

---

## EXISTING_FILES

The 4 target files exist and their current line counts match the diff baselines drafted in the prior `/sc:cleanup-audit` 3-pass run on TUIBBS:

| Path | Lines | Role |
|---|---:|---|
| `/config/.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh` | 134 | Load-bearing discovery script — enumerates files via `git ls-files` (or `find` fallback). Single source of truth for inventory. |
| `/config/.claude/skills/sc-cleanup-audit-protocol/SKILL.md` | 155 | Protocol behavioral spec. `## Behavioral Flow` Discover step (L51) references repo-inventory.sh; `## Key Patterns` documents invariants. |
| `/config/.claude/skills/sc-cleanup-audit-protocol/rules/pass1-surface-scan.md` | 81 | Subagent contract for Pass 1. Read by `audit-scanner` agent. |
| `/config/.claude/commands/sc/cleanup-audit.md` | 118 | Command file. `## Repository Context` runs `git ls-files | wc -l` (cosmetic; reports pre-filter count). |

Relevant current state confirmed via grep:

- `repo-inventory.sh:21` — `FILE_LIST=$(git ls-files -- "$TARGET" 2>/dev/null)` (no scope filter)
- `repo-inventory.sh:23-38` — `find` fallback excludes node_modules / dist / build / vendor / etc., but NOT hidden or BMAD dirs
- `SKILL.md:51` — Discover step references `repo-inventory.sh` without documenting exclusion defaults
- `pass1-surface-scan.md:1-12` — no scope rule for subagents

## PATTERNS_AND_CONVENTIONS

- Protocol skill structure: `SKILL.md` + `rules/` + `scripts/` + `templates/`
- Discovery is single-source-of-truth at `scripts/repo-inventory.sh`; all downstream passes read `inventory.txt` produced by it
- Per-project override convention already in use: `.claude-audit/SCOPE.md` (codified during the 2026-05-29 TUIBBS audit at `/config/workspace/TUIBBS/.claude-audit/SCOPE.md`)
- Exit/error conventions: `set -e`; error messages to stderr with `>&2`; non-zero exit on validation failure

## GAPS_AND_QUESTIONS

None. The 4 file edits are fully specified with concrete diffs from the prior `/sc:cleanup-audit` session. No discovery required. No external research required.

## RECOMMENDED_OUTPUTS

A single MDTM Template 01 task file that encodes the 4 edits as sequential, self-contained checklist items with concrete diffs, verification commands, and rollback procedure.

## SUGGESTED_PHASES

Single-track, 5 phases:

1. **Pre-flight** — read current state of all 4 target files, snapshot for rollback
2. **Edit 1 — repo-inventory.sh (load-bearing)** — add `apply_scope` filter + per-project `SCOPE.md` ingestion
3. **Edit 2 — SKILL.md (documentation)** — document default exclusions + override mechanism in Behavioral Flow + Key Patterns
4. **Edit 3 — rules/pass1-surface-scan.md (subagent contract)** — add scope rule so subagents don't classify out-of-scope content
5. **Edit 4 — commands/sc/cleanup-audit.md (cosmetic)** — clarify the Repository Context label to distinguish tracked vs. in-scope
6. **Smoke test + completion** — run repo-inventory.sh against TUIBBS and confirm in-scope count is 389 (matches the 2026-05-29 audit's final post-amendment count)

## TEMPLATE_NOTES

- **Template 01 (Generic)** is correct: 4 sequential file edits with known inputs, known outputs, no discovery
- No QA gates in generated task file needed (the source-of-truth verification is the smoke test in Phase 6)
- No parallel subagent spawning needed
- Estimated batch size: 1 (sequential per phase)

## AMBIGUITIES_FOR_USER

None — intent is clear from the prior session's diff drafts. The user explicitly approved the suggested edits and requested implementation.
