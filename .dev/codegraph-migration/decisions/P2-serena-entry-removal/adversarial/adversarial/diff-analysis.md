# Diff Analysis: P2 decision (who removes the current-pin Serena registration)

## Metadata
- Generated: 2026-10-29
- Variants compared: 3 (V1 = option-a, V2 = option-b, V3 = option-c)
- Hard constraint (context.md): after `./update.sh` on an existing workspace, Serena and codebase-memory are completely absent.
- Total differences found: 18 debate points (S 2, C 8, X 3, A 5) plus 5 unique contributions
- Categories: structural (2), content (8), contradictions (3), unique (5), shared assumptions (6 found, 5 promoted)
- Facts checked by the orchestrator for this analysis: `/etc/aidev02/ironclaude-provenance` EXISTS on this workspace (the user's own existing workspace, which has an IronClaude checkout that runs `./update.sh`); `src/superclaude/cli/install_codebase_memory.py:25` downloads the upstream `install.sh` (so "kind B" `~/.local/bin/codebase-memory-mcp` installs exist wherever no baked binary was found); `research/install-update-flow.md` 4.3 and handoff §4 state slug order `ironclaude` before `mcp-bundle-core` (`startup.sh:1182`) and the bundle re-adds an absent `serena` (`install.sh:67-119`); research 5.2 row C says Coder removing Serena from the bundle before the pin bump is safe for IronClaude.

## Structural Differences

| # | Area | V1 (A) | V2 (B) | V3 (C) | Severity | Level |
|---|---|---|---|---|---|---|
| S-001 | Section layout | IronClaude / Coder / When / Acceptance / Strengths / Weaknesses | same plus a failure-branch bullet | same as A | Low | L1 |
| S-002 | Acceptance detail | one shell expression set | three layers (unit, sandbox, Coder) | three layers, two-branch unit tests | Low | L1 |

## Content Differences

| # | Topic | V1 (A) | V2 (B) | V3 (C) | Severity | Level |
|---|---|---|---|---|---|---|
| C-001 | Who removes the current-pin `serena` user entry | Coder only (startup migration) | IronClaude retire step, every machine | IronClaude off Coder; Coder on Coder | High | L3 |
| C-002 | Guard condition for IronClaude removal | none (Tier K kept) | codegraph phase succeeded in the same run | codegraph succeeded AND provenance file absent | High | L3 |
| C-003 | When Coder's bundle stops re-adding `serena` | handoff step 5 (after pin bump) | in the Coder change the pin bump depends on (before or with step 4) | step 5 | High | L3 |
| C-004 | Coder one-time exact-argv removal migration | yes | no | yes | Medium | L2 |
| C-005 | "Absent" on non-Coder after `./update.sh` | never automatically | yes, immediately | yes, immediately | High | L3 |
| C-006 | "Absent" on Coder | first restart on step-5 image | registration removed by install; re-added by bundle until Coder stops it; binaries at new image | first restart on step-5 image | High | L3 |
| C-007 | Acceptance checks | `jq -e` on both names, `! command -v serena`, `! command -v codebase-memory-mcp` | unit test (kept on failure), layer-2 seeded sandbox, Coder checks | unit tests both branches, Coder checks, layer-2 | Medium | L2 |
| C-008 | Change to Phase 1 provenance rule | none | Tier K row 1 promoted to removed when codegraph is ready | same, off Coder only | Medium | L2 |

## Contradictions

| # | Point of Conflict | Position | Counter-evidence | Impact | Level |
|---|---|---|---|---|---|
| X-001 | V2 intra: "Coder: registration gone after `./update.sh` or the slug run" vs "a Coder workspace flips back to Serena at boot" | V2 bullet 4 vs bullet 3 | At the pin-bump boot the `ironclaude` slug runs before `mcp-bundle-core`, so the bundle re-adds `serena` in the same boot; later boots do not rerun `superclaude install` (SHA unchanged), so the re-added entry persists until Coder stops re-adding AND something removes it again | High | L3 |
| X-002 | V1 vs hard requirement | "On non-Coder machines: never automatically" | context.md requirement: absent after `./update.sh` | High | L3 |
| X-003 | V3 vs hard requirement on the user's own workspace | Coder branch keeps the entry after `./update.sh` | provenance file exists here, and this workspace runs `./update.sh` from a checkout | High | L3 |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V2 | Move "bundle stops registering Serena" earlier than the pin bump so IronClaude's removal is not undone (research 5.2 row C: safe) | High |
| U-002 | V2 | Explicit failure branch: codegraph not ready means Serena is kept (never leave neither) | Medium (V3 shares the guard) |
| U-003 | V1/V3 | Coder one-time, idempotent startup migration removing only the exact bundle argv | Medium (backstop) |
| U-004 | V3 | Environment signal `/etc/aidev02/ironclaude-provenance` to avoid churn | Low (cross-repo path coupling; fails X-003) |
| U-005 | V1 | Single `jq -e` acceptance expression covering both names | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | all leave `~/.serena`, `~/.cache/codebase-memory-mcp`, uv cache, project `.serena/` | "Completely absent" means registrations and installed programs, not user data | UNSTATED | yes |
| A-002 | all say Phase 1 removes the codebase-memory registration | Phase 1 removes it on every machine | CONTRADICTED (Phase 1 §3.2 binary gate keeps a `~/.local/bin/codebase-memory-mcp` entry while that binary exists; `install_codebase_memory.py:25` created such installs) | yes |
| A-003 | V2/V3 removal rationale | Only IronClaude (registry, docs) and Coder's declared mirror write the current-pin argv | STATED (context.md) | no |
| A-004 | V2/V3 removal is repeated on every install | A user who wants Serena back will not re-register the same argv | UNSTATED (Phase 1 §3.4 prints a re-register hint with exactly this argv) | yes |
| A-005 | all discuss Coder timing | Slug order and rerun rule (ironclaude before bundle; install reruns only on SHA change) | UNSTATED | yes |
| A-006 | V1/V3 treat Coder as image-restart only | Users do not run `./update.sh` on Coder workspaces | UNSTATED (this workspace does) | yes |

## Summary
- Structural 2, content 8, contradictions 3, unique 5, shared assumptions 6 (UNSTATED 4, STATED 1, CONTRADICTED 1); 5 promoted (A-001, A-002, A-004, A-005, A-006; A-003 is STATED and not promoted; IDs are kept as listed, not renumbered).
- Debate denominator: S 2 + C 8 + X 3 + A 5 = 18.
- Highest severity: C-001, C-002, C-003, C-005, C-006, X-001, X-002, X-003, A-002.
- Similarity check: well above 10% difference; debate proceeds.
