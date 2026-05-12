# TASKLIST INDEX -- Context Freshness System (IronClaude Distribution)

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | Context Freshness System (CFS) — IronClaude global feature |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-05-12 |
| TASKLIST_ROOT | `/config/workspace/IronClaude/.dev/releases/current/freshness-system/` |
| Total Phases | 5 |
| Total Tasks | 20 |
| Total Deliverables | 26 |
| Complexity Class | MEDIUM-HIGH |
| Primary Persona | devops |
| Consulting Personas | security, architect, quality, refactorer |
| Predecessors | InfraDocs `phase5.1-context-refresh-design.md`, `claudedocs/research_hooks_consolidated.md`, `claudedocs/research_hooks_community-patterns.md`, `claudedocs/research_hooks_adjacent-ecosystems.md`, `phase5.1-token-budget-check.md`; IronClaude `docs/analysis/hooks-json-relative-path-issue.md` |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `TASKLIST_ROOT/tasklist-index.md` |
| Phase 1 Tasklist | `TASKLIST_ROOT/phase-1-tasklist.md` |
| Phase 2 Tasklist | `TASKLIST_ROOT/phase-2-tasklist.md` |
| Phase 3 Tasklist | `TASKLIST_ROOT/phase-3-tasklist.md` |
| Phase 4 Tasklist | `TASKLIST_ROOT/phase-4-tasklist.md` |
| Phase 5 Tasklist | `TASKLIST_ROOT/phase-5-tasklist.md` |
| Execution Log | `TASKLIST_ROOT/execution-log.md` |
| Checkpoint Reports | `TASKLIST_ROOT/checkpoints/` |
| Evidence Directory | `TASKLIST_ROOT/evidence/` |
| Artifacts Directory | `TASKLIST_ROOT/artifacts/` |
| Validation Reports | `TASKLIST_ROOT/validation/` |
| Feedback Log | `TASKLIST_ROOT/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Pre-cleanup and source layout | T01.01-T01.03 | LIGHT: 1, STANDARD: 2 |
| 2 | phase-2-tasklist.md | Hook script implementation | T02.01-T02.06 | STRICT: 6 |
| 3 | phase-3-tasklist.md | hooks.json registration + CLAUDE.md | T03.01-T03.02 | STRICT: 1, STANDARD: 1 |
| 4 | phase-4-tasklist.md | install_hooks.py + CLI wiring + packaging | T04.01-T04.05 | STRICT: 2, STANDARD: 3 |
| 5 | phase-5-tasklist.md | Local install + validation + baseline | T05.01-T05.04 | STANDARD: 2, EXEMPT: 2 |

## Source Snapshot

- Source design: `InfraDocs:configurations/jenkins/artifacts/phase5.1-context-refresh-design.md` (10 sections; pseudocode, JSON shapes, sequence diagrams, NFR matrix, failure modes).
- Source requirements: `InfraDocs:configurations/jenkins/artifacts/phase5.1-context-refresh-requirements.md` (FR-1 through FR-7, NFR-1 through NFR-12, Q1-Q7 resolved 2026-05-12).
- Token-budget sanity: `InfraDocs:configurations/jenkins/artifacts/phase5.1-token-budget-check.md` (worst-case envelope ~520 chars; truncation logic specced at 9000-char threshold; v1 cap is 10K chars).
- Pre-existing IronClaude defect: `IronClaude:docs/analysis/hooks-json-relative-path-issue.md` — `./scripts/session-init.sh` relative path is fragile; folded into T01.01 as a pre-cleanup task.
- Research basis: `InfraDocs:claudedocs/research_hooks_consolidated.md` (official mechanics + community patterns + adjacent-ecosystem lessons + 30+ pattern catalog).
- Trigger: §5.1 chat session 2026-05-12 surfacing stale-fact-reuse failure mode. System designed global from the start; this tasklist re-roots execution from InfraDocs (where the work surfaced) to IronClaude (where SuperClaude framework sources live).

## Deterministic Rules Applied

- Source-of-truth path convention from CLAUDE.md global rules: `src/superclaude/` is canonical, `plugins/superclaude/` is the distribution mirror (until v5.0 unifies), `~/.claude/` is the install destination.
- Tier classification: hook scripts touching auth boundary or system-wide config = STRICT; `install_hooks.py` (merges into user's settings.json, OAuth-theft-vector risk per NFR-6) = STRICT; CLAUDE.md source edits = STANDARD (auto-distributed by existing install_core); Makefile changes = STANDARD; documentation = EXEMPT; LIGHT for trivial pre-cleanups.
- Critical Path Override applied to T03.01 (hooks.json registration), T04.01 (install_hooks.py implementation), T05.01 (live install smoke), T05.02 (regression test 1).
- Dependency chain: Phase 1 (pre-cleanup) → Phase 2 (hook bodies) → Phase 3 (registration JSON + CLAUDE.md source) → Phase 4 (install pipeline) → Phase 5 (validation against installed system).
- Confidence calibration: design has detailed pseudocode and JSON shapes → most tasks ≥0.85; tasks reliant on undocumented Claude Code internals (FileChanged stdin shape, settings.json merge semantics for user/project/local chain) flagged 0.70-0.80 with probe-handler workarounds or prior-art references.
- Settings.json merge strategy: pure-Python with atomic write (read → in-memory deep-merge → temp-write → rename) following the prior art of `decider/claude-hooks` and Glenn Matlin's uv hooks gist. NO shell-out to jq.
- Hook command paths in `src/superclaude/hooks/hooks.json`: use `~/.claude/hooks/freshness-X.sh` (tilde expands per Claude Code rules) — NEVER relative paths (the existing `./scripts/session-init.sh` is migrated out as part of T01.01).
- Existing `hooks/session-init.sh` is preserved and its path is rewritten as part of T01.01 (two-bird fix).
- Each task references at least 1 roadmap item; each deliverable has artifact path `TASKLIST_ROOT/artifacts/D-####/`.
- v2-deferred items (TaskList active-count, every-Nth-turn refreshes, PostToolBatch, PreCompact snapshot) explicitly NOT in this tasklist — see design §9 "DEFERRED to v2" block.

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Phase 1 | Rewrite existing session-init.sh path from relative to absolute under ~/.claude/hooks/ |
| R-002 | Phase 1 | Create src/superclaude/hooks/scripts/ source-tree directory |
| R-003 | Phase 1 | Mirror new scripts/ directory into plugins/superclaude/hooks/scripts/ |
| R-004 | Phase 2 | Implement SessionStart hook with startup vs resume branching per design §3.1 |
| R-005 | Phase 2 | Implement UserPromptSubmit hook with conditional-contents envelope per design §3.2 |
| R-006 | Phase 2 | Implement PreToolUse Edit-class freshness gate per design §3.3 |
| R-007 | Phase 2 | Implement PostToolUse(Read) tracker per design §3.4 |
| R-008 | Phase 2 | Implement FileChanged tracker per design §3.5 with probe-stage verification |
| R-009 | Phase 2 | Implement SubagentStart/Stop counter pair per design §3.6 |
| R-010 | Phase 3 | Merge 7 freshness registrations into src/superclaude/hooks/hooks.json |
| R-011 | Phase 3 | Append Context Freshness Discipline section to src/superclaude/core/CLAUDE.md |
| R-012 | Phase 4 | Implement src/superclaude/cli/install_hooks.py with atomic additive-merge |
| R-013 | Phase 4 | Wire install_hooks into superclaude install orchestrator (main.py) |
| R-014 | Phase 4 | Update Makefile sync-dev to also sync hooks for local dev |
| R-015 | Phase 4 | Update MANIFEST.in / setup.py to include hooks/scripts/*.sh in wheel |
| R-016 | Phase 4 | Update README.md / CHANGELOG.md with freshness feature announcement |
| R-017 | Phase 5 | Run make sync-dev && superclaude install -f locally |
| R-018 | Phase 5 | Run regression test 1 smoke check from freshness-regression.md |
| R-019 | Phase 5 | Run regression tests 2-5 |
| R-020 | Phase 5 | Capture telemetry baseline and write tuning rationale to Serena memory |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | session-init.sh hooks.json path rewritten to ~/.claude/hooks/ | STANDARD | jq parse + path-content grep | `TASKLIST_ROOT/artifacts/D-0001/diff.md` | XS | Low |
| D-0002 | T01.02 | R-002 | src/superclaude/hooks/scripts/ directory with 7 stub scripts | LIGHT | ls + chmod check | `TASKLIST_ROOT/artifacts/D-0002/stubs.txt` | XS | Low |
| D-0003 | T01.03 | R-003 | plugins/superclaude/hooks/scripts/ mirror | STANDARD | diff src vs plugins | `TASKLIST_ROOT/artifacts/D-0003/mirror-diff.txt` | XS | Low |
| D-0004 | T02.01 | R-004 | freshness-session-start.sh complete | STRICT | sub-agent quality-engineer review | `TASKLIST_ROOT/artifacts/D-0004/spec.md` | M | Medium |
| D-0005 | T02.02 | R-005 | freshness-user-prompt.sh complete | STRICT | sub-agent + 3 dry-runs | `TASKLIST_ROOT/artifacts/D-0005/spec.md` | L | Medium |
| D-0006 | T02.03 | R-006 | freshness-pre-edit.sh complete (the gate) | STRICT | sub-agent + 4 dry-runs | `TASKLIST_ROOT/artifacts/D-0006/spec.md` | L | High |
| D-0007 | T02.04 | R-007 | freshness-post-read.sh complete | STRICT | sub-agent + concurrency test | `TASKLIST_ROOT/artifacts/D-0007/spec.md` | S | Low |
| D-0008 | T02.05 | R-008 | freshness-file-changed.sh complete + probe report | STRICT | sub-agent + probe artifact | `TASKLIST_ROOT/artifacts/D-0008/spec.md` | M | Medium |
| D-0009 | T02.06 | R-009 | freshness-subagent-{start,stop}.sh complete | STRICT | sub-agent + concurrency test | `TASKLIST_ROOT/artifacts/D-0009/spec.md` | S | Low |
| D-0010 | T03.01 | R-010 | src/superclaude/hooks/hooks.json updated; plugins mirror in sync | STRICT | sub-agent + jq schema validate | `TASKLIST_ROOT/artifacts/D-0010/diff.md` | S | High |
| D-0011 | T03.02 | R-011 | src/superclaude/core/CLAUDE.md appended | STANDARD | Manual diff review | `TASKLIST_ROOT/artifacts/D-0011/diff.md` | S | Low |
| D-0012 | T04.01 | R-012 | install_hooks.py implementation | STRICT | sub-agent security review + unit test | `TASKLIST_ROOT/artifacts/D-0012/spec.md` | L | High |
| D-0013 | T04.01 | R-012 | install_hooks.py unit tests | STRICT | pytest pass | `TASKLIST_ROOT/artifacts/D-0013/test-output.txt` | M | Medium |
| D-0014 | T04.02 | R-013 | main.py wires install_hooks into install flow | STANDARD | pytest + manual cli invocation | `TASKLIST_ROOT/artifacts/D-0014/diff.md` | XS | Low |
| D-0015 | T04.03 | R-014 | Makefile sync-dev hook entries | STANDARD | make sync-dev → diff .claude/hooks vs src | `TASKLIST_ROOT/artifacts/D-0015/diff.md` | XS | Low |
| D-0016 | T04.04 | R-015 | MANIFEST.in / setup.py hooks inclusion | STANDARD | sdist build + tar inspection | `TASKLIST_ROOT/artifacts/D-0016/sdist-listing.txt` | XS | Low |
| D-0017 | T04.05 | R-016 | README.md + CHANGELOG.md updates | EXEMPT | manual scan | `TASKLIST_ROOT/artifacts/D-0017/diffs.md` | XS | Low |
| D-0018 | T05.01 | R-017 | make sync-dev && superclaude install -f executed; result captured | STANDARD | jq settings.json + ls hooks dir | `TASKLIST_ROOT/artifacts/D-0018/install-output.txt` | XS | Medium |
| D-0019 | T05.01 | R-017 | settings.json before/after backup pair | STANDARD | diff comparison | `TASKLIST_ROOT/artifacts/D-0019/settings-pair/` | XS | High |
| D-0020 | T05.02 | R-018 | Test 1 result | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0020/test-1-result.md` | S | Medium |
| D-0021 | T05.02 | R-018 | Telemetry sample (block decision) | STANDARD | jq parse log | `TASKLIST_ROOT/artifacts/D-0021/log-sample.jsonl` | XS | Low |
| D-0022 | T05.03 | R-019 | Tests 2-5 results | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0022/test-2to5-results.md` | M | Medium |
| D-0023 | T05.04 | R-020 | Telemetry baseline summary | EXEMPT | read logs | `TASKLIST_ROOT/artifacts/D-0023/baseline.md` | XS | Low |
| D-0024 | T05.04 | R-020 | Serena memory: freshness/tuning/window-size.md | EXEMPT | read_memory | `TASKLIST_ROOT/artifacts/D-0024/memory-content.md` | XS | Low |
| D-0025 | T05.04 | R-020 | Auto-memory: feedback_freshness_system_live.md (project: IronClaude) | EXEMPT | filesystem ls | `TASKLIST_ROOT/artifacts/D-0025/memory-content.md` | XS | Low |
| D-0026 | T05.04 | R-020 | MEMORY.md index entry (project: IronClaude) | EXEMPT | grep | `TASKLIST_ROOT/artifacts/D-0026/diff.md` | XS | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001 | STANDARD | 90% | `TASKLIST_ROOT/artifacts/D-0001/` |
| R-002 | T01.02 | D-0002 | LIGHT | 95% | `TASKLIST_ROOT/artifacts/D-0002/` |
| R-003 | T01.03 | D-0003 | STANDARD | 95% | `TASKLIST_ROOT/artifacts/D-0003/` |
| R-004 | T02.01 | D-0004 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0004/` |
| R-005 | T02.02 | D-0005 | STRICT | 85% | `TASKLIST_ROOT/artifacts/D-0005/` |
| R-006 | T02.03 | D-0006 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0006/` |
| R-007 | T02.04 | D-0007 | STRICT | 95% | `TASKLIST_ROOT/artifacts/D-0007/` |
| R-008 | T02.05 | D-0008 | STRICT | 75% | `TASKLIST_ROOT/artifacts/D-0008/` |
| R-009 | T02.06 | D-0009 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0009/` |
| R-010 | T03.01 | D-0010 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0010/` |
| R-011 | T03.02 | D-0011 | STANDARD | 95% | `TASKLIST_ROOT/artifacts/D-0011/` |
| R-012 | T04.01 | D-0012, D-0013 | STRICT | 80% | `TASKLIST_ROOT/artifacts/D-0012/`, `TASKLIST_ROOT/artifacts/D-0013/` |
| R-013 | T04.02 | D-0014 | STANDARD | 90% | `TASKLIST_ROOT/artifacts/D-0014/` |
| R-014 | T04.03 | D-0015 | STANDARD | 90% | `TASKLIST_ROOT/artifacts/D-0015/` |
| R-015 | T04.04 | D-0016 | STANDARD | 85% | `TASKLIST_ROOT/artifacts/D-0016/` |
| R-016 | T04.05 | D-0017 | EXEMPT | 95% | `TASKLIST_ROOT/artifacts/D-0017/` |
| R-017 | T05.01 | D-0018, D-0019 | STANDARD | 85% | `TASKLIST_ROOT/artifacts/D-0018/`, `TASKLIST_ROOT/artifacts/D-0019/` |
| R-018 | T05.02 | D-0020, D-0021 | STANDARD | 85% | `TASKLIST_ROOT/artifacts/D-0020/`, `TASKLIST_ROOT/artifacts/D-0021/` |
| R-019 | T05.03 | D-0022 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0022/` |
| R-020 | T05.04 | D-0023, D-0024, D-0025, D-0026 | EXEMPT | 95% | `TASKLIST_ROOT/artifacts/D-0023/` through `D-0026/` |

## Execution Log Template

**Intended Path:** `TASKLIST_ROOT/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run | Result | Evidence Path |
|---|---:|---|---:|---|---|---|---|

## Checkpoint Report Template

- `# Checkpoint Report -- <Checkpoint Title>`
- `**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/<deterministic-name>.md`
- `**Scope:** <tasks covered>`
- `## Status` -- `Overall: Pass | Fail | TBD`
- `## Verification Results` (exactly 3 bullets)
- `## Exit Criteria Assessment` (exactly 3 bullets)
- `## Issues & Follow-ups`
- `## Evidence`

## Feedback Collection Template

**Intended Path:** `TASKLIST_ROOT/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|

## Generation Notes

- **Settings.json merge semantics are partially documented.** The `managed-settings.d` drop-in directory has explicit merge rules (scalars last-wins, arrays concat+dedupe, objects deep-merge). The user/project/local precedence chain is documented as scope-precedence not merge — except for specific array-typed keys (`allowedHttpHookUrls`, `httpHookAllowedEnvVars`, sandbox arrays, MCP allowlists) which are explicitly stated to merge across sources. The `hooks` object's merge behavior across user/project/local is NOT explicitly documented; T04.01 implements additive merge for the hooks key specifically, following prior art from `decider/claude-hooks` and Glenn Matlin's uv hooks gist. **Implementer must add a TEST** that exercises this against a multi-event existing settings.json to confirm behavior.
- **T02.05 FileChanged stdin schema** is the lowest-confidence item (0.75); probe-handler approach preserved from InfraDocs tasklist.
- **T04.01 confidence is 0.80** despite high risk because prior art exists. The unit test deliverable (D-0013) is required to lift confidence empirically.
- **Hooks live at user-scope (~/.claude/settings.json) per NFR-12** — repo-local hooks silently bypassed on `--add-dir`. install_hooks.py MUST default to user scope; `--target` flag supports custom paths for testing.
- **Backup convention:** Claude Code documents "timestamped backups, retain 5 most recent" but does not document the exact path/naming. install_hooks.py creates its own backup at `~/.claude/settings.json.bak.<ISO-8601>` before any write to be safe, regardless of Claude Code's internal backup mechanism.
- **CLAUDE.md auto-distribution:** existing `install_core_files` already handles `core/*.md` → `~/.claude/`, so T03.02's source edit auto-distributes via existing pipeline. No new install module needed for that piece.
- **v2-deferred items** (TaskList active-count, every-Nth-turn refresh, PostToolBatch, PreCompact) are not in this tasklist by design — see `InfraDocs:phase5.1-context-refresh-design.md` §9 explicit deferral block. Do NOT pull these into scope without a separate design-pass cycle.
