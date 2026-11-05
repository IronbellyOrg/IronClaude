# Merged Findings: Phase 1 Removal Plan Review

<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (reviewer-1 card) -->
<!-- Merge date: 2026-10-29 -->

```yaml
merged_from: ["reviewer-1-card.yaml (C=0.75)", "reviewer-2-card.yaml (C=0.77)"]
method: "sc:adversarial Mode A, depth standard"
convergence: 0.947
verdict: refactor
counts: {kept: 12, dropped: 0, important: 3, minor: 9}
findings:
  # Source: Variant 1 (reviewer-1 card) R1-F3, refactor-plan change 3
  - id: R1-F3
    decision: keep
    merged_severity: IMPORTANT
    deviation_class: spec-inherited
    class: plan-defect
    claim: "Task 4 says the new remover replaces `_cleanup_user_native_registration` (spec §3.5, source.md:334 \"replaces\"), but that function is still called by `uninstall_codebase_memory_mcp` (install_mcp.py:993, :999), which is kept until Task 5 and which the tavily tests at about :888-1050 exercise; Task 4's acceptance runs the whole tavily file. Deleting the helper breaks `uninstall_codebase_memory_mcp`; rewiring it to the direct-exec remover (source.md:335) bypasses the patched run function the tavily tests record through (tests/cli/test_install_mcp_tavily.py:426-430, via install_mcp.py:766-769), so the call-list assertions at :926-929 and :943-945 fail."
    evidence: ["src/superclaude/cli/install_mcp.py:916", "src/superclaude/cli/install_mcp.py:993", "src/superclaude/cli/install_mcp.py:999", "src/superclaude/cli/install_mcp.py:766-769", "tests/cli/test_install_mcp_tavily.py:426-430", "tests/cli/test_install_mcp_tavily.py:888", "tests/cli/test_install_mcp_tavily.py:926-929", "tests/cli/test_install_mcp_tavily.py:943-945", "tests/cli/test_install_mcp_tavily.py:1050", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:334", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:335"]
    grounded: true
    fix: "Task 4: add `_remove_exact_user_entry` alongside the old helper and leave `_cleanup_user_native_registration` untouched. Task 5 deletes it together with `uninstall_codebase_memory_mcp` (row C2)."
    provenance: "Variant 1 F3 (IMPORTANT kept); strengthened with test mechanics per C-003 Round 2; the 'add to Task 5 rg' sub-fix dropped (C-003, `_native_` already matches)."

  # Source: Variant 1 (reviewer-1 card) R1-F4, refactor-plan change 4
  - id: R1-F4
    decision: keep
    merged_severity: IMPORTANT
    deviation_class: spec-inherited
    class: plan-defect
    claim: "Task 18's sandbox fresh/existing checks (DoD-2, source.md:268; spec T14 steps 4-5, source.md:780-781) cannot work as written. (a) `rg -n -i '...' $T/fresh` passes vacuously, because rg skips the hidden `.claude/`, `.claude.json` and `.local/` under the root it is given (orchestrator check: 0 vs 2 `.serena/` hits without and with `--hidden`). (b) `rg -n -i 'serena|codebase-memory' $T/old/.claude` (an explicit root) cannot print nothing, because installed allowlisted text matches (ccsession-tag/install.sh:41; sc-cleanup-audit-protocol/SKILL.md:57; Task 11's `load.md` legacy sentence; install_skill.py:52 copytree with no ignore), and because both installers back up the seeded `settings.json` to `settings.json.bak.<%Y%m%dT%H%M%SZ>` (install_hooks.py:293-297, :491-494; install_user_setup.py:81-89), which keeps the `mcp__serena__*` matcher."
    evidence: ["src/superclaude/skills/ccsession-tag/install.sh:41", "src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:57", "src/superclaude/commands/load.md:27", "src/superclaude/cli/install_skill.py:52", "src/superclaude/cli/install_hooks.py:293-297", "src/superclaude/cli/install_hooks.py:491-494", "src/superclaude/cli/install_user_setup.py:81-89", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:156", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:247", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:248", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:268", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:621", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:780-781"]
    grounded: true
    fix: "Task 18: use `rg -n -i --hidden --no-ignore` for both searches; pipe the output through a line-level filter for installed paths, `rg -v -e '/\\.claude/skills/ccsession-tag/install\\.sh:' -e '/\\.claude/commands/sc/load\\.md:[0-9]+:.*\\.serena/memories' -e '/\\.claude/skills/sc-cleanup-audit-protocol/SKILL\\.md:[0-9]+:.*\\.serena/' -e '/\\.claude/settings\\.json\\.bak\\.[0-9]{8}T[0-9]{6}Z:'` (do not reuse ALLOW, which is anchored to repo paths, source.md:621); exclude `claude-calls.log` for `$T/fresh`; assert separately that at least one `settings.json.bak.*` exists and never delete it."
    provenance: "Variant 1 F4 (IMPORTANT kept), claim and fix rewritten per X-001, INV-001, INV-002, INV-003."

  # Source: Variant 1 (reviewer-1 card) R1-F5, refactor-plan change 5
  - id: R1-F5
    decision: keep
    merged_severity: IMPORTANT
    deviation_class: spec-inherited
    class: plan-defect
    claim: "Task 18's sandbox commands set only HOME and omit CLAUDE_CONFIG_DIR; `read_user_mcp_entry` reads CLAUDE_CONFIG_DIR first and the stub's jq edit targets `${CLAUDE_CONFIG_DIR:-$HOME}`, so an executor environment that sets it would read and mutate the real user config. DoD-2 says \"temp HOME and CLAUDE_CONFIG_DIR\" (source.md:268) but the spec T14 steps omit it. The defect is latent here: `CLAUDE_CONFIG_DIR` is unset in this environment and only install_mcp.py:731 reads it; the plan's Task 4 (plan:80) already sets it."
    evidence: ["src/superclaude/cli/install_mcp.py:731", "src/superclaude/cli/install_mcp.py:735", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:268", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:80", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:247"]
    grounded: true
    fix: "Task 18: add `CLAUDE_CONFIG_DIR=\"$T/fresh\"`, `\"$T/old\"` and `\"$T/ci\"` (equal to the sandbox HOME, never `$HOME/.claude`, never empty) to every `env` call, including `./update.sh`, the `--force` fallback with doctor, the Tier K repeat and the no-CLI robustness run."
    provenance: "Variant 1 F5 (IMPORTANT kept), extended per C-005 and INV-004."

  # Source: Variant 1 (reviewer-1 card) R1-F1, refactor-plan change 1
  - id: R1-F1
    decision: keep
    merged_severity: MINOR
    deviation_class: spec-inherited
    class: plan-defect
    claim: "Task 12 already deletes rule-M8 calls \"in these files\" (plan:167; source.md:421). The repo-wide memory-name rg still fails at Task 12 on exactly two lines outside the Task 11/12 files: src/superclaude/cli/reflect/contract.py:30 (`get_current_config` in a comment) and src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:127 (Task 13 row P84). The identical rg is in the spec T10b acceptance."
    evidence: [".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:167", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:172", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:421", "src/superclaude/cli/reflect/contract.py:30", "src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:127"]
    grounded: true
    fix: "Task 7: drop `get_current_config` from the contract.py:28-34 comment and check for it. Task 12: either pull the rubric :127 deletion forward (logging it) or exclude that file from its rg."
    provenance: "Variant 1 F1 (IMPORTANT to MINOR), narrowed by C-001 and INV-008; the 'many more files / T1 fix too narrow' sub-claim dropped."

  # Source: Variant 1 (reviewer-1 card) R1-F2, refactor-plan change 2
  - id: R1-F2
    decision: keep
    merged_severity: MINOR
    deviation_class: spec-inherited
    class: plan-defect
    claim: "Task 10's third acceptance command (rg 'mcp-servers:.*serena' across src/superclaude, plugins, commands and agents) fails at Task 10. Task 10 edits only the T9 rows, but there are 49 `mcp-servers:` lines, many in files whose rows are spec T10/T11 (P2, P33, P49, P62, P65, P6/P15/P43/P50, save/load/pm). The spec T9 acceptance has the same rg."
    evidence: [".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:145", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:150", "src/superclaude/commands/troubleshoot.md:6", "src/superclaude/commands/validate-roadmap.md:7", "src/superclaude/commands/auggie-review.md:6", "src/superclaude/commands/save.md:6", "src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:15", "src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:6", "commands/sc-brainstorm.md:6", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:392"]
    grounded: true
    fix: "Task 10: explicitly drop `serena` from every `mcp-servers:` line in `src/superclaude`, `plugins/superclaude`, `commands` and `agents` (rule G5: \"simply drop\", source.md:392; all lists are single-line). The frontmatter parts of later rows become no-ops."
    provenance: "Variant 1 F2 (IMPORTANT to MINOR), per C-002 and INV-008."

  # Source: Variant 1 (reviewer-1 card) R1-F6, refactor-plan change 6
  - id: R1-F6
    decision: keep
    merged_severity: MINOR
    deviation_class: spec-inherited
    class: plan-defect
    claim: "Task 13 deletes reflection-rubric.md lines 124-127, but line 128 (`find_implementations`) and line 130 (`type_hierarchy`) still match the SER pattern, and Task 13's own acceptance runs `acceptance-search.sh serena` over the whole sc-reflect-protocol directory; line 130 is in no row (spec row P84 lists 124,126-128 and deletes 124-127). Other reflect-ref SER-token lines are also missing from the row line lists: cost-profile.yaml:74 (`execute_shell_command`), coverage-mapping.md:195 (`type_hierarchy`), deviation-taxonomy.md:79,80,83, reviewer-spec.md:14,55."
    evidence: ["src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:127", "src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:128", "src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:130", "src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml:74", "src/superclaude/skills/sc-reflect-protocol/refs/coverage-mapping.md:195", "src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:79", "src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:80", "src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:83", "src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md:14", "src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md:55", "tests/cli/reflect/test_verify_denylist_git_mutations.py", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:179", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:235"]
    grounded: true
    fix: "Task 13: give the rubric per-line actions (124 reword the \"V3 Serena adoptions\" heading; 126-127 delete, since `onboarding_status` dies with M8 Step 0.7; 128 reword to the G2 Grep floor; 129 keep, retitling its step reference if the 6.1.1 heading changes; 130 delete, step 4.5 gone, G8). Name the INV-005 lines: delete the `type_hierarchy` lines; rewrite `execute_shell_command` to Bash under the retitled envelope, keeping the \"No-mutation gate.\" paragraph pinned by tests/cli/reflect/test_verify_denylist_git_mutations.py. Add a G8 note for `onboarding_status`."
    provenance: "Variant 1 F6 (IMPORTANT to MINOR), extended per INV-005 and INV-006."

  # Source: Variant 1 (reviewer-1 card) R1-F7, refactor-plan change 7
  - id: R1-F7
    decision: keep
    merged_severity: MINOR
    deviation_class: plan-introduced
    class: plan-defect
    claim: "Task 8's real.yaml comment list misses line 721 (`Edit|Write|mcp__serena__*`), so Task 8's own rg over src/superclaude/cli/eval would fail."
    evidence: ["src/superclaude/cli/eval/suites/real.yaml:721", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:121"]
    grounded: true
    fix: "Task 8: add real.yaml:721 to the comments to reword."
    provenance: "Variant 1 F7, unchanged."

  # Source: Variant 1 (reviewer-1 card) R1-F8, refactor-plan change 8
  - id: R1-F8
    decision: keep
    merged_severity: MINOR
    deviation_class: plan-introduced
    class: plan-defect
    claim: "Task 12 `git mv`s into docs/memory/reflect/, which does not exist, and Tasks 1 and 18 tee into $PKG/artifacts/baseline/ and final/ without creating them."
    evidence: [".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:167", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:37", "docs/memory/README.md", "docs/memory/reflect/ (absent today, INV-009)", "$PKG/artifacts/ (absent today, INV-009)"]
    grounded: true
    fix: "Add `mkdir -p docs/memory/reflect` (Task 12), `mkdir -p $PKG/artifacts/baseline` (Task 1), `mkdir -p $PKG/artifacts/final` (Task 18)."
    provenance: "Variant 1 F8, evidence extended per INV-009."

  # Source: Variant 1 (reviewer-1 card) R1-F9, refactor-plan change 9
  - id: R1-F9
    decision: keep
    merged_severity: MINOR
    deviation_class: plan-introduced
    class: plan-defect
    claim: "Task 12 edits reflect refs, SKILL.md and commands but runs no tests/cli/reflect; tests/cli/reflect/test_remediation_route_table.py reads remediation-handoff.md directly."
    evidence: ["tests/cli/reflect/test_remediation_route_table.py:13", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:170"]
    grounded: true
    fix: "Task 12 acceptance: add `tests/cli/reflect` to the pytest list."
    provenance: "Variant 1 F9, unchanged."

  # Source: Variant 1 (reviewer-1 card) R1-F10, refactor-plan change 10
  - id: R1-F10
    decision: keep
    merged_severity: MINOR
    deviation_class: plan-introduced
    class: plan-defect
    claim: "The slots ledger and Phase 2 handoff notes live under untracked .dev/codegraph-migration/ and the plan stages only .dev/tasks, so they are never committed."
    evidence: [".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:21", "session git status: `?? .dev/codegraph-migration/` (untracked, not ignored)"]
    grounded: true
    fix: "Tasks 13, 14, 15 and 19: `git add` the exact ledger/handoff file paths they create (not the folder), or the plan states they stay untracked."
    provenance: "Variant 1 F10, trimmed to the ledger half per C-010 and INV-007; grounded set true; the main.py 'Codebase Memory' half dropped (Task 6's cbm acceptance search catches main.py:292, :313)."

  # Source: Variant 2 (reviewer-2 card) R2-F1, refactor-plan change 11
  - id: R2-F1
    decision: keep
    merged_severity: MINOR
    deviation_class: plan-introduced
    class: coverage-gap
    claim: "Two Phase 1 scope limits stated by the spec (source.md:261 and §2.3) are carried by no plan task and no Constraint: 'Historical `.dev/` artifacts stay untouched' and the §2.3 table of leftovers IronClaude does not own (Coder image binary, `serena-agent` uv tool, bundle markers, upstream companions, `~/.local/bin/install.sh`). plan:26 already blocks real-HOME installs, user-data deletion and other-repo edits; what is missing is the historical-`.dev/` limit and the Coder-owned leftovers."
    evidence: [".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:26", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:19-30", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:261", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:279-291"]
    grounded: true
    fix: "Add a Constraints bullet: \"Existing `.dev/` files outside `$PKG` are not edited; the only other `.dev` writes are new files in `.dev/codegraph-migration/handoffs/`. No task uninstalls the `serena-agent` uv tool or removes `~/.local/bin/{serena,serena-agent,serena-hooks}`, the Coder `/usr/local/bin/codebase-memory-mcp` binary, bundle markers, upstream companions or `~/.local/bin/install.sh` (./source.md §2.3).\""
    provenance: "Variant 2 F1 (MINOR), narrowed per C-011; fix wording from INV-007."

  # Source: Variant 2 (reviewer-2 card) R2-F2, refactor-plan change 12
  - id: R2-F2
    decision: keep
    merged_severity: MINOR
    deviation_class: spec-inherited
    class: plan-defect
    claim: "Task 18 claims DoD-1 to DoD-6, but its 'existing' sandbox seeds only `.claude.json` and `.claude/settings.json`, not the old core files and installed primitives with Serena rows that DoD-3 (source.md:269) says the sandbox is seeded with. Once the rg is filtered (R1-F4), the 'existing' check proves nothing about stale core files and installed primitives being overwritten by a forced install. The plan copies this gap from spec T14 step 5 (source.md:781)."
    evidence: [".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:243", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:248", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:269", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:781", "src/superclaude/cli/install_core.py:65-70", "src/superclaude/cli/install_commands.py:55-61"]
    grounded: true
    fix: "Task 18: before `./update.sh`, also seed a stale `$T/old/.claude/CLAUDE.md` and a stale `$T/old/.claude/commands/sc/reflect.md`, each with one `serena` row; after the run, the filtered rg of R1-F4 prints nothing (the files are overwritten under `--force`, install_core.py:65-70, install_commands.py:55-61)."
    provenance: "Variant 2 F2 (MINOR); 'can therefore pass' dropped per X-001 (the unfiltered rg fails)."

spec_errata:
  - spec_location: "T9 acceptance rg"
    finding: R1-F2
  - spec_location: "T10b repo-wide rg"
    finding: R1-F1
  - spec_location: "§3.5 \"replaces\" (source.md:334)"
    finding: R1-F3
  - spec_location: "DoD-2 / T14 steps 4-5 (source.md:268, :780-781)"
    finding: [R1-F4, R1-F5]
  - spec_location: "P84 line range and the missing ref lines"
    finding: R1-F6
  - spec_location: "DoD-3 vs T14 step 5 (source.md:269, :781)"
    finding: R2-F2

dropped_subclaims:
  - diff_point: C-001
    proposal: "R1-F1's \"many more files ... T1's fix too narrow\""
    rationale: "Refuted: plan:167 and M8 give those deletions to Task 12; only 2 lines remain (INV-008)"
  - diff_point: C-003
    proposal: "Add `_cleanup_user_native_registration` to Task 5's rg"
    rationale: "Redundant: `_native_` already matches (plan:91)"
  - diff_point: C-010
    proposal: "Task 5 rg for \"Codebase Memory\" in main.py"
    rationale: "Redundant: Task 6's cbm acceptance search catches it"
  - diff_point: C-004
    proposal: "Exclude `claude-calls.log` from the `$T/old` search"
    rationale: "Not needed: the log is at `$T/old/claude-calls.log`, outside the `$T/old/.claude` root"
  - diff_point: S-002
    proposal: "Change the citation style"
    rationale: "Cosmetic, unresolved, no effect on findings"

process_notes:
  - "One subagent constraint breach: `mkdir -p /tmp/x` by the V2 advocate, outside the repo, left in place."
```
