# Refactoring Plan

## Overview
- Base variant: Variant 1 (`variant-1-original.md`, reviewer-1 card)
- Incorporated: Variant 2 (`variant-2-original.md`) findings R2-F1 and R2-F2, plus Round 2.5 invariants INV-001, INV-002, INV-005, INV-006 and INV-007
- Target: `../merged-findings.md` (one level above this folder), a single deduplicated finding set in the card schema, extended with `decision`, `merged_severity`, `deviation_class`, `provenance`
- Planned changes: 14. Rejected: 4 sub-claims. Overall risk: Low (text-only merge, no source files touched).
- Every finding below has been checked against real files (see `diff-analysis.md` ground-truth table, `debate-transcript.md` and `invariant-probe.md`).

## Output schema (each finding)
```yaml
- id: <original id>
  decision: keep | drop
  merged_severity: IMPORTANT | MINOR
  deviation_class: plan-introduced | spec-inherited
  class: plan-defect | coverage-gap
  claim: "<corrected claim>"
  evidence: [<file:line>, ...]
  grounded: true
  fix: "<merged fix>"
  provenance: "<variant + debate points>"
```
Header fields: `merged_from: [reviewer-1-card.yaml (C=0.75), reviewer-2-card.yaml (C=0.77)]`, `method: sc:adversarial Mode A, depth standard`, `convergence: 0.947`, `verdict: refactor`, `counts`, plus a `dropped_subclaims` list and a `spec_errata` list.

## Planned Changes

1. **R1-F1, modify (Medium):** severity IMPORTANT to MINOR; plan-introduced (the identical rg is in spec T10b acceptance, so mark it spec-inherited). Corrected claim: Task 12 already deletes rule-M8 calls "in these files" (plan:167; source.md:421). The repo-wide rg still fails at Task 12 on exactly two lines outside the Task 11/12 files: `src/superclaude/cli/reflect/contract.py:30` (`get_current_config` in a comment) and `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:127` (Task 13 row P84). Fix: Task 7 drops `get_current_config` from the contract.py:28-34 comment (and checks for it); Task 12 either pulls the rubric :127 deletion forward (logging it) or excludes that file from its rg. Provenance: V1 F1, narrowed by C-001 and INV-008.
2. **R1-F2, modify:** IMPORTANT to MINOR; spec-inherited (spec T9 acceptance has the same rg). Claim unchanged in substance: 49 `mcp-servers:` lines, many in files whose rows are spec T10/T11 (P2, P33, P49, P62, P65, P6/P15/P43/P50, save/load/pm). Fix: Task 10 explicitly drops `serena` from every `mcp-servers:` line in `src/superclaude`, `plugins/superclaude`, `commands`, `agents` (rule G5: "simply drop", source.md:392; all lists are single-line). The frontmatter parts of later rows become no-ops. Provenance: V1 F2, C-002, INV-008.
3. **R1-F3, modify (keep IMPORTANT):** spec-inherited (source.md:334 "replaces"). Strengthen the claim with the test mechanics: deleting the helper breaks `uninstall_codebase_memory_mcp` (`install_mcp.py:993`, `:999`); rewiring it to the direct-exec remover (source.md:335) bypasses the patched run function the tavily tests record through (`tests/cli/test_install_mcp_tavily.py:426-430`, via `install_mcp.py:766-769`), so the call-list assertions at :926-929 and :943-945 fail. Fix: Task 4 adds `_remove_exact_user_entry` alongside the old helper and leaves `_cleanup_user_native_registration` untouched; Task 5 deletes it with `uninstall_codebase_memory_mcp` (row C2). Drop the "add to Task 5's rg" sub-fix (`_native_` already matches). Provenance: V1 F3, C-003 Round 2.
4. **R1-F4, rewrite (keep IMPORTANT):** spec-inherited (DoD-2 source.md:268; T14 steps 4-5 at :780-781). Corrected claim: (a) `rg -n -i '...' $T/fresh` passes vacuously, because rg skips the hidden `.claude/`, `.claude.json` and `.local/` under the root it is given (orchestrator check: 0 vs 2 `.serena/` hits without and with `--hidden`); (b) `rg -n -i 'serena|codebase-memory' $T/old/.claude` (an explicit root) cannot print nothing, because installed allowlisted text matches (`ccsession-tag/install.sh:41`; `sc-cleanup-audit-protocol/SKILL.md:57`; Task 11's `load.md` legacy sentence; `install_skill.py:52` copytree with no ignore), and because both installers back up the seeded `settings.json` to `settings.json.bak.<%Y%m%dT%H%M%SZ>` (`install_hooks.py:293-297`, `:491-494`; `install_user_setup.py:81-89`), which keeps the `mcp__serena__*` matcher. Fix: in Task 18 use `rg -n -i --hidden --no-ignore` for both searches; pipe through a line-level filter for installed paths, `rg -v -e '/\.claude/skills/ccsession-tag/install\.sh:' -e '/\.claude/commands/sc/load\.md:[0-9]+:.*\.serena/memories' -e '/\.claude/skills/sc-cleanup-audit-protocol/SKILL\.md:[0-9]+:.*\.serena/' -e '/\.claude/settings\.json\.bak\.[0-9]{8}T[0-9]{6}Z:'` (do not reuse ALLOW, which is anchored to repo paths, source.md:621); exclude `claude-calls.log` for `$T/fresh`; assert separately that at least one `settings.json.bak.*` exists and never delete it. Provenance: V1 F4, X-001, INV-001, INV-002, INV-003.
5. **R1-F5, modify (keep IMPORTANT):** spec-inherited (DoD-2 says "temp HOME and CLAUDE_CONFIG_DIR", source.md:268; T14 steps omit it). Add: latent here (`CLAUDE_CONFIG_DIR` is unset in this environment; only `install_mcp.py:731` reads it); the plan's Task 4 (plan:80) already sets it. Fix: add `CLAUDE_CONFIG_DIR="$T/fresh"`, `"$T/old"`, `"$T/ci"` (equal to the sandbox HOME, never `$HOME/.claude`, never empty) to every Task 18 `env` call, including `./update.sh`, the `--force` fallback with doctor, the Tier K repeat and the no-CLI robustness run. Provenance: V1 F5, C-005, INV-004.
6. **R1-F6, modify:** IMPORTANT to MINOR; spec-inherited (row P84 lists 124,126-128 and deletes 124-127; :130 is in no row). Extend the claim with INV-005: other reflect-ref SER-token lines missing from row line lists: `cost-profile.yaml:74` (`execute_shell_command`), `coverage-mapping.md:195` (`type_hierarchy`), `deviation-taxonomy.md:79,80,83`, `reviewer-spec.md:14,55`. Fix: Task 13 gives the rubric per-line actions (124 reword the "V3 Serena adoptions" heading; 126-127 delete, since `onboarding_status` dies with M8 Step 0.7; 128 reword to the G2 Grep floor; 129 keep, retitling its step reference if the 6.1.1 heading changes; 130 delete, step 4.5 gone, G8), names the INV-005 lines (delete `type_hierarchy` lines; rewrite `execute_shell_command` to Bash under the retitled envelope, keeping the "No-mutation gate." paragraph pinned by `tests/cli/reflect/test_verify_denylist_git_mutations.py`), and adds a G8 note for `onboarding_status`. Provenance: V1 F6, INV-005, INV-006.
7. **R1-F7, keep MINOR** unchanged (plan-introduced: real.yaml:721). Provenance: V1 F7.
8. **R1-F8, keep MINOR** (plan-introduced); add the evidence that `docs/memory/reflect/` and `$PKG/artifacts/` are absent today. Provenance: V1 F8, INV-009.
9. **R1-F9, keep MINOR** unchanged (plan-introduced). Provenance: V1 F9.
10. **R1-F10, trim:** keep MINOR, the ledger half only; set `grounded: true` (evidence: session git status `?? .dev/codegraph-migration/`; not ignored). Fix: Tasks 13, 14, 15 and 19 `git add` the exact ledger/handoff file paths they create (not the folder), or the plan states they stay untracked. Drop the main.py "Codebase Memory" half (Task 6's `acceptance-search.sh cbm src tests` catches `main.py:292`, `:313`). Provenance: V1 F10, C-010, INV-007.
11. **R2-F1, incorporate (MINOR)**, plan-introduced (the spec states the limit at source.md:261 and §2.3). Narrowed claim: plan:26 already blocks real-HOME installs, user-data deletion and other-repo edits; missing are the historical-`.dev/` limit and the Coder-owned leftovers. Fix (INV-007 wording): add a Constraints bullet: "Existing `.dev/` files outside `$PKG` are not edited; the only other `.dev` writes are new files in `.dev/codegraph-migration/handoffs/`. No task uninstalls the `serena-agent` uv tool or removes `~/.local/bin/{serena,serena-agent,serena-hooks}`, the Coder `/usr/local/bin/codebase-memory-mcp` binary, bundle markers, upstream companions or `~/.local/bin/install.sh` (./source.md §2.3)." Provenance: V2 F1, C-011, INV-007.
12. **R2-F2, incorporate (MINOR)**, spec-inherited (DoD-3 at source.md:269 vs T14 step 5 at :781). Corrected claim: drop "can therefore pass" (X-001: the unfiltered rg fails); the gap is that, once filtered (change 4), the "existing" check proves nothing about stale core files and installed primitives being overwritten. Fix: before `./update.sh`, also seed a stale `$T/old/.claude/CLAUDE.md` and `$T/old/.claude/commands/sc/reflect.md`, each with one `serena` row; after the run, the filtered rg of change 4 prints nothing (the files are overwritten under `--force`, `install_core.py:65-70`, `install_commands.py:55-61`). Provenance: V2 F2, X-001.
13. **Header:** add `spec_errata` listing the spec-inherited defects so the spec can be corrected too: T9 acceptance rg (R1-F2); T10b repo-wide rg (R1-F1); §3.5 "replaces" (R1-F3); DoD-2 / T14 steps 4-5 (R1-F4, R1-F5); P84 line range and the missing ref lines (R1-F6); DoD-3 vs T14 step 5 (R2-F2).
14. **Header:** add `dropped_subclaims` (see below) and `process_notes`: one subagent constraint breach (`mkdir -p /tmp/x` by the V2 advocate, outside the repo, left in place).

## Changes NOT Being Made

| Diff point | Proposal | Rationale |
|---|---|---|
| C-001 | R1-F1's "many more files ... T1's fix too narrow" | Refuted: plan:167 and M8 give those deletions to Task 12; only 2 lines remain (INV-008) |
| C-003 | Add `_cleanup_user_native_registration` to Task 5's rg | Redundant: `_native_` already matches (plan:91) |
| C-010 | Task 5 rg for "Codebase Memory" in main.py | Redundant: Task 6's cbm acceptance search catches it |
| C-004 | Exclude `claude-calls.log` from the `$T/old` search | Not needed: the log is at `$T/old/claude-calls.log`, outside the `$T/old/.claude` root |
| S-002 | Change the citation style | Cosmetic, unresolved, no effect on findings |

No whole finding is dropped: all 12 original findings are kept.

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1-14 | Low | Text-only merged card | Re-run the merge from this plan |

## Review Status
Auto-approved (non-interactive), 2026-10-29.
