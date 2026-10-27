# Refactor Plan — Layered Fix

## Overview
- **Base RCA:** RCA #2 (skill-creator plugin convention, SKILL.md L167)
- **Strengths incorporated from:** RCA #3 (governance — full R1–R5), RCA #1 (defensive guard subset — Edits 1+2)
- **Total layered actions:** 11 (3 in L1, 6 in L2, 2 in L3)
- **Risk level:** LOW–MEDIUM (no breaking changes; one risk around hook precision)

## Planned Changes

### Layer 1 — Stop Occurrence (RCA #2)

| ID | Change | Source | Target | Integration | Rationale | Risk |
|---|---|---|---|---|---|---|
| L1.1 | Add PreToolUse hook rejecting `Write`/`Edit` to `.claude/skills/*-workspace/**` and rewriting to `.dev/eval-workspaces/<skill-name>/<remainder>` | RCA #2 Option D | `.claude/settings.json` | Insert | Enforcement-by-config; only layer not dependent on Claude obedience | Medium (R-01 — must not break legit `.claude/skills/<skill>/` file edits) |
| L1.2 | CLAUDE.md addendum overriding skill-creator's "sibling to skill directory" convention | RCA #2 Option C | `/config/workspace/IronClaude/CLAUDE.md` | Append section | Documents the rule for human readers; high-priority instruction for Claude | Low |
| L1.3 | `make eval-skill SKILL=<name>` target — pre-creates `.dev/eval-workspaces/<name>/` and prints absolute path | RCA #2 Option B | `Makefile` | Append target | Convenience nudge; reduces chance of hand-typed wrong paths | Low |

### Layer 2 — Stop Persistence (RCA #3)

| ID | Change | Source | Target | Integration | Rationale | Risk |
|---|---|---|---|---|---|---|
| L2.1 | Replace `verify-sync`'s `"MISSING in src/superclaude/skills/: <name> (not distributable!)"` with context-aware variant: when missing entry has no `SKILL.md`, emit `"<name> has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/<name>/."` | RCA #3 R2 | `Makefile:179-187` | Modify | Stops the misleading-message anti-fix | Low |
| L2.2 | Wire `make verify-sync` and `make lint-architecture` into `quick-check.yml` | RCA #3 R3 | `.github/workflows/quick-check.yml` | Append steps | **HIGHEST PRIORITY** — closes INV-002 (dormant detection) | Low |
| L2.3 | Add `*-workspace` blocklist with explicit suffix message | RCA #3 R4 | `Makefile` (verify-sync or lint-architecture) | Add check | Belt-and-suspenders for the suffix attractor (F11) | Low |
| L2.4 | Add `.dev/README.md` documenting all 11 subdirectories; explicit rule: *"Workspaces, fixtures, harness code, and iteration outputs go under `.dev/`, never under `.claude/skills/`"* | RCA #3 R1 | `.dev/README.md` (new) | Create | Closes the discoverability gap | Low |
| L2.5 | Repair or remove broken `PLANNING.md`/`TASK.md`/`KNOWLEDGE.md` references in project CLAUDE.md | RCA #3 R5 | `CLAUDE.md` (project) | Modify | Stops governance corrosion | Low |
| L2.6 | Add `.gitignore` entry `.claude/skills/*-workspace/` | New (informed by all three RCAs) | `.gitignore` | Append | Prevents re-occurrence under same skill subtree directly | Low |

### Layer 3 — Defense in Depth (RCA #1)

| ID | Change | Source | Target | Integration | Rationale | Risk |
|---|---|---|---|---|---|---|
| L3.1 | Add output-path policy guard in `sc-release-split-protocol/SKILL.md` Prerequisites step 2a — refuse `.claude/skills/...`, `.claude/agents/...`, `.claude/commands/...` outputs. Document policy in `release-split.md` Options table. | RCA #1 Edits 1+2 | Skill + command files | Modify | Catches the rare case where a SuperClaude skill receives a `.claude/skills/...` `--output` directly | Low |
| L3.2 | (Optional) Apply the same guard to `sc-adversarial-protocol` and `sc-cleanup-audit-protocol` for consistency | RCA #1 Edit 3 | Two SKILL.md files | Modify | Generalizes the protection | Low |

## Changes NOT Being Made (rejected from non-base)

| Diff Point | Non-base Approach | Rejection Rationale |
|---|---|---|
| Cause attribution | RCA #1 claim "skill spec is cause" | Author self-rejected at 0.95 confidence; debate consensus |
| Cause attribution | RCA #3 framing "governance is THE dominant cause" | Superseded by RCA #2 smoking gun; relegated to systemic-cause role (still adopted as fix layer) |
| `.dev/eval-workspaces/` vs prior art | RCA #3 noted divergence from `.dev/releases/complete/v2.15-cli-portify/` | Documentation decision deferred to L2.4 (.dev/README.md); new convention adopted forward-only |

## Risk Summary

| Risk ID | Description | Layer | Mitigation |
|---|---|---|---|
| R-01 | PreToolUse hook breaks legitimate `.claude/skills/<skill>/` writes | L1 | Pattern must match `*-workspace/**` precisely; test positive (skill file edit) and negative (workspace write) cases |
| R-02 | CI lengthens PR time | L2 | `verify-sync` runs in seconds; concurrent with existing checks |
| R-03 | New `.dev/eval-workspaces/` convention diverges from prior art | L2 | L2.4 explicitly documents new rule; backwards-compatible (prior workspace stays where it is) |
| R-04 | Skill-creator plugin updates upstream → L167 reference goes stale | L1 | L1.2 cites behavior not file path |
| R-05 | Future skill *should* legitimately have a workspace inside `.claude/` | L1, L2 | Hook + Makefile checks emit override-able errors |

## Review Status
- **Default:** Auto-approved (pipeline non-interactive)
- **Recommendation:** Land L2.2 first (closes INV-002 HIGH-severity unaddressed invariant), then L1.1+L1.2, then remaining items can ship in any order
- **Approval timestamp:** 2026-05-08
