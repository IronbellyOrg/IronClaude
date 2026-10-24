# Research: /sc:workflow recommendation refresh

- **Topic type:** Command history and routing-contract research
- **Scope:** Six-month command history, delegated protocol, recommendation surfaces, governing guide, plugin consequences and regression coverage
- **Status:** Research complete; returned directly for coordinator persistence. No files changed.
- **Date:** 2026-10-24

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/workflow.txt`, worker `a18027429bae4c3a1`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] The exact command changed five times during the inventory window. `89df2c11` (2026-05-22) only inserted Markdown whitespace; it introduced no semantic behavior. `b31111a9` (2026-09-30) replaced the broad multi-persona/MCP description with a thin command and delegated protocol, introduced `quick|standard|deep`, and rejected legacy parallel/validation flags. `6dc56b1a` (2026-10-03) replaced the earlier workflow output directory with portable `TASK-WF-*` packages and retired `--output`. `7c0eb528` (2026-10-09) added advisory pre-execution reflection. `5c6a7d91` (2026-10-22) changed the protocol-document reference to its installed location. These are verified patches for W, not inferred from commit subjects.

[CODE-VERIFIED] Relevant delegated changes include `bb4f0212` and `3f7c6553` (2026-09-30), which adopted the executable task-heading template and mapped every phase output into a producing task; `9207838c` (2026-10-17), which bundled that template for installed operation; and `c6009cd3` (2026-10-23), which explicitly required staging task-package evidence. Current text retains those contracts. (P:28,44-48)

### Current command contract

[CODE-VERIFIED] Input is exactly one existing file, optionally prefixed with `@`, or an inline prompt. Bare invocation stops. Supported flags are `--strategy systematic|agile|enterprise`, `--depth quick|standard|deep`, and `--handoff none|design|implement|tasklist`. Defaults are systematic, standard and none; enterprise selects deep when depth is omitted. `--parallel`, `--validate`, `--output`, and old depth values are rejected. (W:18-42)

[CODE-VERIFIED] Workflow creates a new package containing the directory-matching plan, a source snapshot and a return contract. Generation is planning, not product implementation or Sprint-bundle generation. Activation delegates to `Skill sc:workflow-protocol`. Depth supports 2-4, 4-8 or 6-12 phases; enterprise adds risk/operations treatment and rollout. (W:48-80; P:32-48; D:5-13)

[CODE-VERIFIED] After the plan passes its structural gate, workflow invokes advisory reflection before its contract and handoff. Failed or unavailable reflection does not invalidate an otherwise gated plan. The default prints the implement next step; explicitly selecting `--handoff implement` invokes implementation. Design/tasklist handoffs are text, not execution. Resume belongs to implement, whose matching ledger makes resume implicit. Managed execution keeps evidence beside the plan and requires fresh final review before safe archiving; this implies no commit, PR or release. (P:50-74; W:40; I:55-65)

### Comparison with recommendation surfaces

[CODE-VERIFIED] The principal mismatch is governing policy, not failure to discover the command. The guide restricts level 3 to a few files and one or two sessions, while level 4 matches many files, more than one session, or avoiding drift. Existing-system feature work directly uses task-builder; post-research implementation also defaults there. Its pair-comparison repeats that boundary. These conditions conflict with the user’s requested **new** workflow-first policy, although they accurately describe current guide instructions. (G:17-22,100-106,243,305-308)

[CODE-VERIFIED] Workflow already accepts a PRD/spec and deeper planning, while implement already supplies evidence-backed managed execution and implicit resume. Therefore an existing spec, need for an audit trail, or interrupted execution does not independently establish that MDTM is necessary. This establishes available contracts, not unlimited workload capacity. (W:18-40; P:40-58; I:55-65)

[CODE-VERIFIED] Changing only recommend’s prose would leave contradictory paths. Its no-match and missing-guide fallbacks repeat “larger, longer, or riskier” as the MDTM threshold. The delegation heuristic and condensed cold-worker runbook repeat it again. The classifier additionally defines generic spec/report-to-task-file requests as task-builder/task work, with no workflow distinction. (R:155-157; H:38; C:58-59,78-79,160-166)

[CODE-VERIFIED] Matched guide rows bypass both cache lookup and cold write-back, so correcting their conditions affects the answer before a cached target can intervene. The canonical guide’s bytes are already included in cache surface hashing. No new workflow-specific cache schema is required merely to apply this policy change. Plugin guide rows duplicate the current restrictive routing. (R:39-61; K:63-94; M:305-311)

### Proposed recommendation changes

[CODE-VERIFIED] **MUST, proposed policy:** Update G’s level table, hard-limit explanation, sections 3.2/3.3/3.4/3.7, pair comparison, and existing `simple-plan`, `task-file`, `feature-existing`, `research-first` and bug-routing conditions. Default planned implementation to workflow plus implement. Reserve MDTM generation for the most complex, long-running work where its phase-review/checklist machinery is actually needed, or where the user explicitly selects that format. Do not use file count, multiple sessions, spec availability, resume or “must not drift” alone as escalation tests. These are proposed replacements for the verified current conditions, not claims about existing policy. (G:17-22,100-117,243,305-311)

[CODE-VERIFIED] **MUST:** Change R’s fallback wording, H’s breadth rule and C’s cold-worker wording together. Narrow the classifier’s task-file description/example to intentional MDTM generation, allowing ordinary planning requests to use guide routing or live discovery rather than a task-builder-biased cache bucket. Keep the guide as the sole fixed routing source; do not add another keyword table. (R:155-157; H:38; C:58-59,78-79,160-166)

[CODE-VERIFIED] **SHOULD:** Stop making `--depth quick` mandatory for every workflow recommendation. Keep it for small checked plans, use the existing standard default for ordinary planned work, and offer deep or enterprise only when the requested planning detail warrants it. The command supports those choices; quick is not its default. Example handoff grounded in W:27-40:

```text
/sc:workflow "Plan the agreed CSV export feature, including implementation, tests and acceptance criteria. Do not implement yet." --depth standard --handoff none
```

Then read its actual printed plan and reflection result before `/sc:implement <printed-plan-path>`. Never fabricate the generated package identifier or add a destination flag.

[CODE-VERIFIED] **MUST:** Apply the corresponding guide update to M and the level-table copy in F. Preserve explicit execution identity: workflow packages go to implement, existing MDTM inputs remain `/task`, and report-only requests retain their dedicated commands rather than becoming implementation plans. Do not silently add `--handoff implement` to a planning-only request. (W:40,80; G:308,312-321; F:56-61)

### Acceptance/regression scenarios

[CODE-VERIFIED] Existing tests pin guide-first ordering, hard-limit protection and flag validity; workflow tests pin reflection ordering. These are useful structural protections, not evidence that recommendation behavior was executed. Add semantic cases alongside them. (T:35-80; U:286-311; V:221-231)

[UNVERIFIED] Proposed acceptance cases, not executed:

1. A clear feature spanning many files and several sessions still defaults to workflow/implement unless exceptional MDTM needs are stated.
2. A supplied PRD/spec does not force task-builder; standard/deep workflow remains eligible.
3. Existing workflow package resume selects implement, never `/task`.
4. Explicit MDTM execution remains `/task`; explicit task-builder selection is honored.
5. Research-only and diagnosis-only goals stop at their reports.
6. Planning-only requests omit executable handoff; advisory reflection failure is described honestly.
7. No recommendation emits retired workflow flags or historical output locations.
8. Checkout, missing-guide/cold-path and plugin-guide cases apply the same revised boundary.
9. Editing the governing guide invalidates old cached rows; matched workflow rows still bypass cache.

## Gaps

[CODE-VERIFIED] D:13 explicitly says deep planning is “still one session,” while implement supports persisted resume. The research does not establish unlimited planning/execution capacity or a measured upper workload bound. Reconcile this wording before claiming multi-session planning itself is guaranteed.

[CODE-VERIFIED] Literal searches found workflow references in the main recommendation skill and its heuristic, and in the cold runbook; no workflow-specific hook routing rule was found. Generic “workflow” mentions are not automatically `/sc:workflow` references. The hook is explicitly fail-open, so it cannot substantiate a claim of mechanical routing enforcement. (J:2-18)

[UNVERIFIED] No skills, inference evaluations or tests were executed. Historical changes and current behavior above are verified documentation contracts. Global legacy recommendation-protocol drift is outside this command-specific conclusion and should be consolidated by the recommendation analyst.

## Key Takeaways

**CHANGE. MUST:** Align the governing guide, recommendation fallbacks, classifier/runbook, core level-table copy and plugin mirror with the user’s workflow-first policy.

**SHOULD:** Surface standard/deep workflow planning and distinguish advisory reflection from a blocking success guarantee.

**NONE:** No workflow implementation rewrite, new keyword router or new cache schema is justified by this analysis.

### Evidence paths

All citation keys identify these absolute paths; suffixes are live line numbers.

- **W:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/workflow.md`
- **P:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-workflow-protocol/SKILL.md`
- **D:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-workflow-protocol/refs/phase-templates.md`
- **I:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/implement.md`
- **G:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md`
- **R:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md`
- **H:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md`
- **C:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py`
- **K:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py`
- **M:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`
- **F:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/CLAUDE.md`
- **T:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/skills/test_sc_recommend_routing_contract.py`
- **U:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py`
- **V:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/commands/test_workflow_command.py`
- **J:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh`
