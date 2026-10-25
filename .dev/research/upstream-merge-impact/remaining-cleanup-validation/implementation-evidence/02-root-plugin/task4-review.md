# Research: Native root-plugin reflection proof

- **Topic type:** Fresh independent full-plan and runtime acceptance review
- **Scope:** Task 4 root reflection behavior, real isolated audits and preservation
- **Status:** FAIL (initial PASS withdrawn by the same reviewer before ledger acceptance)
- **Closed verdict:** `missing`
- **Persistence:** Superseding independent correction controls; original findings below are retained as historical, not acceptance.
- **Date:** 2026-10-24
- **Template:** src/superclaude/templates/modularization-template-review/codebase-research_template.md

## Findings

### Superseding final correction: FAIL / missing

[CODE-VERIFIED] The reviewer withdrew the initial PASS after directly rechecking a MINOR runtime source-guard violation. Unmet criteria: T4.AC1 and T4.AC5. extra_scope=[]; misunderstood=[]; cannot_verify=[]. No global assistance was observed, but that separate fact cannot satisfy an explicitly violated guard. Task4 remains incomplete; no complete or FINAL ledger record was written.

[CODE-CONTRADICTED] `commands/sc-reflect.md:39-47`, especially `:45-46`, requires shell cwd to remain at launch or selected audit root. Current forced-case raw `stdout.jsonl:1497-1498` successfully executes parent `cd $O` into artifacts, and the final validator inherits that cwd (`config/projects/-tmp-ironclaude-reflect-runtime-764r-aaf/e1eca8d8-d832-49b8-85cc-3ef2da1daf0d/subagents/agent-aa315d0ed235b7f21.jsonl:1-4`). An advocate also successfully enters output/adversarial at `stdout.jsonl:857-858`. Neither is a permitted cwd. The checker tests startup cwd and Read confinement, not this runtime invariant.

[CODE-VERIFIED] AC2 real roles/calibration/merge/final citation evidence, AC3 degraded/unavailable behavior, AC4 preservation and Tasks1-3 end-state findings remain met. The invariant-004 fixture-provenance facts and disclosed E-13/E-13a correction remain accurately interpreted. The failure is not missing resources, fake merge, package assistance or fixture provenance; it is actual execution violating the delivered cwd rule.

[CODE-VERIFIED] Required next step is one scoped Task4 fix pass: make real execution honor the existing cwd guard using absolute artifact paths, record bounded runtime evidence, and require fresh independent review. Do not retrofit old records, weaken the guard to match observed violations, or count this cohort as satisfying it. Reviewer made no changes/new audit runs. Their initial zero-finding conclusion was wrong because absence of global assistance was treated as sufficient despite the cwd violation; this focused recheck supersedes it.

All short raw paths above are under `task4-runtime-bounded/runs/post-tier2-attempt-1/` in this evidence directory.

### Historical initial review (WITHDRAWN)

[CODE-VERIFIED] **Initial PASS. Closed verdict at that time: compliant (WITHDRAWN).** extra_scope=[]; misunderstood=[]; missing=[]; cannot_verify=[]. Fresh independent Task4 and full-plan/source-guard/runtime review, not acceptance of producer booleans. Reviewer changed no product, fixture, report, config, index or commit.

- **T4.AC1 compliant:** `commands/sc-reflect.md:20-28` binds the actual bundled protocol; `:58-86` preserves pre/post/range guards and legacy task mapping; `:88-104` preserves fail-closed output guards. All 14 command lines, inventories and raw terminal results inspected. Refusals occur before audit roles, unsafe output never created, log-only post works. Complete current command body, with only plugin-root variable expansion, appears in both persisted core native prompts at main transcript line 4; this is real root dispatch, not manually reimplemented wrapper behavior.
- **T4.AC2 compliant:** Current forced-case `artifacts/adversarial/merged-verdict.yaml:1-20` and `artifacts/evidence-validation.yaml:1-22` corroborate real merge and final gate. Raw dispatch/returns/nested tools show Sonnet5.5 + Grok4.7 fixed restricted reviewers, only Read/Grep/Glob on frozen audit data and exact current procedural refs; three independent Opus calibrators with actual cited-source Reads and matching five-score means. Real adversarial skill, coordinators, advocates/rebuttals/invariant probe, forward/reverse 30-criterion CEV scoring, merge-executor and disk outputs ran. New final validator follows merge/draft, reads real anchors and returns 25 revalidations/one drop. Corrected recitation explicitly an orchestrator re-Read, not fake second validation.
- **T4.AC3 compliant:** `commands/sc-reflect.md:166-197`; remediation case `artifacts/return-contract.yaml:95-104`. MCP inventories empty; reports disclose native-only/degraded verification rather than inventing reachability. Missing builder returns false acceptance/null handoffs; no corrective builder/executor in raw traces. Readiness stops for absent separate package executable. All honor no-promote.
- **T4.AC4 compliant:** `task4-check-output.json:204-246` preservation/inventory/index/head/copy checks independently recomputed. All 2,281 non-reflection baseline assets match. Other 25 commands reproduce approved transforms, 15 unavailable occurrences and two help deletions; all nine Availability passages retained. All 22 additions exactly replay canonical hashes and ordered adaptations. All 2,233 originally protected non-command/non-manifest assets match, including canonical/package/alternate, original 21 agents, confidence and unmatched commands. Exactly 74 product files, authorized delta 49 paths; retired producer/cursor/commands absent, empty index, unchanged HEAD.
- **T4.AC5 compliant:** Read full revised plan/ledger/current and canonical commands, guards/adaptations/helpers/fixtures, every native execution/init/raw return/role trace and eligible output. `task4-check-output.json:199-202` require-all/no missing cases independently checked. Fourteen native exits zero are NOT fourteen audit successes: two pre successes, seven partial audits, three failed-precondition contracts, one readiness stopped-precondition and one unsafe-output inline refusal.

[CODE-VERIFIED] Tasks1-3 remain compliant at end state. Actual filename-derived loader mappings resolve all required local names. Manifest change is exactly empty-homepage deletion. Read-only tools, independent five-dimensional mean/anchors/thresholds, all input/tree/output drift guards, actual merge/MALFORMED/fallback guards, field remap/null handling and unavailable-package/no-execution boundaries remain intact. No new mandatory edge or unapproved product delta found.

[CODE-VERIFIED] INV-004 is fixture/audit uncertainty, not a product workflow defect: widening/regenerating a patch in a zero-commit/all-untracked fixture would invent test-change provenance. Merged card/report reject that closure, retain BLOCKED_BY_INVARIANTS, partial/human-decision flags despite agreement .947, and do not promote. The final citation drop likewise exercises honest partial handling; no false application success is claimed.

[CODE-VERIFIED] Isolation checked from live help/actual commands, restricted file policy, isolated HOME/config/external startup cwd, narrow add-dirs, UV-only binary, absent package executable and MCP[]. Real probe allows fixture Read and denies real pyproject Read. This is file-tool confinement, NOT an OS Bash sandbox. Successful shell traces/interpreter inputs inspected: wave0/finalize match raw heredocs, extracted snapshot code matches bundled recipe; independent read-only verification validates all eight source/copy rows, pinned selection and scoped membership.

[CODE-VERIFIED] Prepared fixture hashes, current source/fixture and post-run integrity agree. Older execution records lack later-added launch-hash fields; none were fabricated. Executed current wiring is independently established by full persisted command payloads and matching raw resource Reads. One final validator started in output/artifacts cwd with enclosing checkout Gitroot, but attached session_context is empty, no real CLAUDE markers/foreign reads, and actual tools/evidence remain in allowed roots. Other built-ins did not supply missing framework dependencies. Rejected old global-read/timeout/bad-calibration attempts excluded.

Product paths are repository-relative. Short evidence paths are relative to this evidence directory. Forced-case artifact paths are under `task4-runtime-bounded/runs/post-tier2-attempt-1/`; remediation paths under its named bounded run. This is the parent-persisted independent reviewer result.

## Gaps

[CODE-CONTRADICTED] Current unmet gap is T4.AC1/T4.AC5: actual successful shell transitions violate the delivered launch/audit-root cwd rule. No Task4 acceptance is authorized. The no-global-assistance findings remain true but do not waive this MINOR source-guard failure.

[UNVERIFIED] Positive valid-commit-range runtime is explicitly NOT claimed: synthetic fixture has no commits. Actual source guards and invalid-ref refusal were checked. No full Python suite or new native audits were run by the reviewer. Per-launch hash fields added later are not historical proof; file confinement is not OS Bash sandboxing. Partial fixture audit outcomes and one citation drop remain in the raw/final records, not waived or rewritten.

## Key Takeaways

[CODE-VERIFIED] **Current verdict is FAIL / missing. Keep Task4 incomplete.** Fix actual working-directory execution within the already approved command/harness scope, preserve the existing guard and failure history, then require matching runtime evidence and a fresh independent review. Initial PASS and zero-findings conclusion are withdrawn, not an eligible completion/ruling. The focused recheck found the literal guard violation after initially treating absence of global assistance as sufficient.
