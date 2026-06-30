# PR #144 Restoration Re-audit — Grounded Evidence Packet

Worktree: `/config/workspace/IronClaude-pr144-reflect` (HEAD = ddf209e4, `make sync-dev` applied so .claude mirror == src).

## Commits
- base/canonical = **54d4b4f5** (`fix(sprint): treat PASS_RECOVERED ... #139`)
- convergence head (dropped content) = **4f0a60fb** (`feat(task-builder): converge rigorflow ... incl. #138 sc:reflect`)
- restoration under audit = **ddf209e4** (`fix(task-builder): restore canonical invariant content dropped by convergence reformatting`)
- restoration diff `4f0a60fb..ddf209e4`: 4 files, +289/-168. Files: `src/superclaude/agents/{rf-analyst,rf-qa,rf-qa-qualitative}.md`, `src/superclaude/skills/task-builder/SKILL.md`.

## Verification triangle (run at HEAD ddf209e4, `uv run pytest`)
- `tests/audit/` → **1 failed, 1188 passed, 1 skipped**. The one failure = `test_invariant_preservation_NFR_6_through_10.py::TestInvariant3_PersistentArtifact::test_task_id_naming_pattern_preserved` — a `.dev/tasks/` directory-naming filesystem test (env state, unrelated to the 4 restored files). It is in the KNOWN pre-existing set per the audit brief.
- `tests/audit/test_severity_floor_unweakened.py` → **8/8 PASS** (severity-floor guard intact).
- `tests/skills/test_task_builder_merge.py` → **2 failed, 66 passed**. The 2 failures are EXACTLY the item-3 cluster:
  - `TestPR01ExecutionContextHeader::test_skill_documents_execution_context_block` — `assert "EXECUTION CONTEXT BLOCK" in skill_text` (literal renamed away).
  - `TestPR01ExecutionContextHeader::test_execution_context_optional_and_degrades_gracefully` — `assert "OPTIONAL" in skill_text` (OPTIONAL→REQUIRED).

## Item 1 — sha256 / recommendation grounding (the two pins)
- **`51725c0ffa...` (COMP-006-M6)** pins the `rf-team-lead's Fix Cycles rule` line. GUARD-ENFORCED by `tests/audit/test_dnsp_all_agents_fail_bypass.py` TEST-020:
  - `test_rf_team_lead_fix_cycles_sha256_pin_present_at_every_site` (pin string present at every site)
  - `test_fix_cycles_rule_present_and_byte_stable` (runtime hash of the live rule line == fixture bytes)
  - Both PASS at HEAD. base=`frozen at 51725...`; convergence=`OMITTED as bridge-stage` (BROKE the guard); restoration=`frozen at 51725...` RESTORED. → guard-required DRIFT correction, runtime-verified true.
- **`5ff2a1803b...`** pinned the INV-012 *subsection* (SKILL.md L1079-1093). The convergence STRUCTURALLY REFORMATTED that subsection (base mega-paragraph → condensed Path A/B/C). Base had it at all 4 sites; restoration did NOT restore it (stays `OMITTED as bridge-stage` in the 3 agent files; absent in SKILL.md). NO guard test references `5ff2a`. Re-asserting the old hash over reformatted bytes would be a FALSE pin → leaving it OMITTED is honest/correct, not under-restoration.
- recommendation string: base=`Manual review required — partition agent failed twice` (em-dash); convergence=`Manual review required, partition agent failed twice` (ASCII comma); restoration=em-dash RESTORED. This is a byte-exact fixed-value invariant (R-117/R-118).

## Item 2 — em-dash over-restoration scan
Em-dash (—) counts base/convergence/restoration: rf-analyst 71/37/40; rf-qa 134/86/88; rf-qa-qualitative 298/209/217; SKILL.md 348/220/250. Restoration stays NEAR convergence, FAR below base → surgical, NOT a broad ASCII-style revert. Sampled added em-dashes are all structural/guard labels (`Manual review required —`, `— Reliance Audit (PR-04, INV-019)`).

## Item 3 — Execution Context OPTIONAL→REQUIRED + rename (THE DEFERRED CALL)
- Merge test file `tests/skills/test_task_builder_merge.py` was NEVER modified (unchanged base→convergence→restoration).
- base SKILL.md: `## Execution Context (OPTIONAL — see EXECUTION CONTEXT BLOCK below)` + `EXECUTION CONTEXT BLOCK (OPTIONAL, TASK-LEVEL ROLL-UP):`.
- convergence SKILL.md: renamed to `EXECUTION_CONTEXT_INSTRUCTION:` (L1035) + `This section is REQUIRED in every task file (except GOAL-only...)` (L1198).
- restoration SKILL.md: STILL `EXECUTION_CONTEXT_INSTRUCTION` (L1066) + `REQUIRED in every task file` (L1229). The restoration did NOT revert this — it DEFERRED it (left the 2 tests RED). The literal `EXECUTION CONTEXT BLOCK` and `OPTIONAL, TASK-LEVEL` do NOT appear at HEAD.
- The convergence change is coherent/intentional: rename is consistent, REQUIRED rule has a documented GOAL-only exception, MDTM template now embeds the section.

## Item 4 — MD040 fence additions
28 `​```text` fence-language additions. All sha256/byte-stability guard tests PASS → no pinned block mutated.

## Item 5 — tests/audit base-parity
Only failure is the pre-existing filesystem `test_task_id_naming_pattern_preserved`. No NEW #144-introduced audit failure beyond the known set (task_id_naming; tests/cli/eval/*; test_install_hooks.py; test_zero_files_analyzed teardown).
