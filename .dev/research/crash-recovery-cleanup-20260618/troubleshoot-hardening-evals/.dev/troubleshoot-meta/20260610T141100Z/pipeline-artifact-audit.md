# Pipeline Artifact Audit — PRD Saga Troubleshoot/Debug Meta-Investigation

Generated: 2026-06-10
Role: A3 pipeline-artifact forensic
Scope: read-only audit of `.dev/troubleshoot/`, `.dev/reflect/`, and `.dev/tasks/` artifacts relevant to the PRD runtime/debug saga. Product/source code was not modified.

## Escape set used for classification

| Escape | Symptom | Pipeline principle tested | Fix / evidence reference |
|---|---|---|---|
| E1 | PRD stage artifact resolver missed runtime-written artifacts: `_STEP_ARTIFACT_FILES` lacked `build-task-file`; static map could not represent `TASK-PRD-{slug}.md`; stdout fallback concealed failures. | Runtime-entrypoint verification; contract-implementation enumeration | `.dev/eval-workspaces/prd-cli-audit/SEVERITY-RANKED-FINDINGS.md` F-01/F-02/F-04/F-10/F-27; remediation sequencing in Batch A. |
| E2 | PRD gate/prompt schema divergence: research-notes gate required old section names while prompt/skill emitted `EXISTING_FILES` schema. | Contract-implementation enumeration; unmask-and-sweep | `.dev/tasks/done/TASK-RF-20260520-050937/TASK-RF-20260520-050937.md` objectives 1-5. |
| E3 | PRD runtime local-file crash: PRD subprocess passed local filesystem paths via Claude CLI `--file`, requiring a session token and failing headless runs at `scope-discovery`. | Runtime-entrypoint verification; off-path review | `.dev/tasks/to-do/TASK-RF-prd-local-file-20260609-005242/TASK-RF-prd-local-file-20260609-005242.md`; `.dev/reflect/post-prd-local-file-20260609105644/REPORT.md`. |
| E4 | Resume/spec contract gaps: duplicate `--spec` binding and resume-path WARN gated on `config.spec_files`, which is empty on `prd resume`. | Runtime-entrypoint verification; contract-implementation enumeration | `.dev/troubleshoot/prd-spec-review-r140-20260606174115/REPORT.md`. |
| E5 | Pattern recurrence: dead knobs/unused monitors/static dispatch tables and tests that mock the wrong surface let PRD defects pass until later audit. | Unmask-and-sweep; heterogeneous off-path review | `.dev/eval-workspaces/prd-cli-audit/SEVERITY-RANKED-FINDINGS.md` pattern audit P1-P9 and F-27. |

Classification key: **CAUGHT** = artifact explicitly identified the escape or mandated a direct guard; **RUBBER-STAMPED** = artifact gave PASS/Done/clean signal while the escape class remained possible or was outside its verified surface; **N/A** = artifact targeted another subsystem or predates/does not touch the escape surface.

## Artifact-by-artifact classification

| Artifact | E1 | E2 | E3 | E4 | E5 | Notes |
|---|---:|---:|---:|---:|---:|---|
| `.dev/eval-workspaces/prd-cli-audit/SEVERITY-RANKED-FINDINGS.md` | CAUGHT | CAUGHT | RUBBER-STAMPED | PARTIAL | CAUGHT | Strongest artifact. It verified anchor bugs F-01/F-02/F-03, generalized to F-04 (13 missing Write-emitting steps), F-10 (NDJSON fallback concealment), and F-27 (mock harness structurally unable to catch F-01 class). It did not surface the later `--file` session-token runtime crash. |
| `.dev/tasks/done/TASK-RF-20260520-050937/TASK-RF-20260520-050937.md` | N/A | CAUGHT | N/A | N/A | PARTIAL | Explicitly fixed gate-vs-prompt schema divergence and added a prompt-to-gate round-trip integration test. This is a good contract-enumeration artifact for one contract pair, but not a whole PRD runtime sweep. |
| `.dev/tasks/done/TASK-RF-20260521133223/TASK-RF-20260521133223.md` | PARTIAL | N/A | RUBBER-STAMPED | RUBBER-STAMPED | PARTIAL | PR #71 remediation improved artifact-pattern sharing, Stage B detection, verdict regex, resume docstring, and direct coverage. However, it remained source/test-surface focused and did not runtime-execute the headless PRD entrypoint that later exposed E3. It also did not catch E4's resume-path persisted-SPECS issue. |
| `.dev/troubleshoot/build-anti-instinct-uncovered-contracts-20260525141717/REPORT.md` | N/A | N/A | N/A | N/A | CAUGHT for analogous class | Not PRD-specific; useful meta-evidence. It separated two similarly named gates, reran the actual deterministic integration-contract check, and identified extractor/coverage asymmetry. It models the desired contract-implementation enumeration behavior. |
| `.dev/troubleshoot/pr86-integration-contracts-20260526100600/REPORT.md` | N/A | N/A | N/A | N/A | CAUGHT for analogous class | Not PRD-specific; strong heterogeneous off-path review: Tier 2, adversarial debate, invariant probe, and staged remediation. Shows the troubleshoot pipeline can unmask invariant gaps when forced beyond Tier 1. |
| `.dev/troubleshoot/spec-fidelity-deep-dive-20260527045400/REPORT.md` | N/A | N/A | N/A | N/A | CAUGHT for analogous class | Not PRD-specific; strong unmask-and-sweep model. It identified comparator/extractor asymmetry, binary convergence failure, and missing fixability invariant instead of only the immediate halt. |
| `.dev/troubleshoot/prd-spec-review-r140-20260606174115/REPORT.md` | N/A | N/A | N/A | CAUGHT | PARTIAL | Correctly confirmed two PRD `--spec` defects and grounded them in runtime command differences between `prd run` and `prd resume`. Tier 1 was enough for this narrow surface. |
| `.dev/tasks/to-do/TASK-RF-prd-local-file-20260609-005242/TASK-RF-prd-local-file-20260609-005242.md` | N/A | N/A | CAUGHT | N/A | CAUGHT | Directly encodes the runtime-entrypoint failure: local paths passed to `--file` require `CLAUDE_CODE_SESSION_ACCESS_TOKEN` and crash headless PRD runs. It requires zero `--file` grep, inverted tests, content-inline tests, missing-path guard, and UV pytest. |
| `.dev/reflect/post-prd-local-file-20260609105644/REPORT.md` | N/A | N/A | CAUGHT | N/A | CAUGHT | Post-reflect audited the actual working-tree PRD diff rather than the wrong task `start_commit` range, a notable catch of a meta-pipeline diff-target trap. It verified grep zero `--file`, tests `160 passed`, and no drift/regression. |
| `.dev/tasks/done/TASK-E2E-20260327-prd-pipeline-e2e/reviews/*.md` | PARTIAL | PARTIAL | RUBBER-STAMPED | N/A | PARTIAL | These older adversarial/E2E reviews found PRD enrichment-chain and prompt issues, but their mock/subprocess surface predates the runtime crash and did not test headless CLI local-file behavior. Agent 11 caught merge-step no-PRD context; Agent 6 caught dead `tdd_file`; Agent 4 caught prompt size risk; none caught E3. |
| `.dev/tasks/done/TASK-E2E-20260327-prd-pipeline-e2e/research/02-prd-implementation-mapping.md` | PARTIAL | N/A | RUBBER-STAMPED | N/A | PARTIAL | Mapped 10 phases / 61 items to E2E scenarios and noted `--prd-file` wiring, but was implementation-mapping rather than runtime-entrypoint validation. |
| `.dev/reflect/*` non-PRD reports such as PR144 restoration, sprint-auto-resume, pre/post sprint recovery | N/A | N/A | N/A | N/A | N/A / analogous only | These are outside the PRD runtime dataset. They are useful only as examples of reflect tiering/evidence validation; they should not be counted as having cleared PRD bugs. |

## Findings against the four global principles

### 1. Runtime-entrypoint verification

Result: **failed until late in the saga**.

Evidence:
- E1 and E3 both escaped artifacts that reasoned over source/test surfaces but did not execute the production/headless runtime path. The PRD CLI audit later found the mock harness itself was defective: F-27 says the mock writes passing content to the stream file and is structurally unable to catch the F-01 class.
- The `prd-local-file` task finally states the runtime symptom plainly: the PRD pipeline passed local filesystem paths through Claude CLI `--file`, a cloud download mechanism requiring `CLAUDE_CODE_SESSION_ACCESS_TOKEN`, causing headless runs to exit at `scope-discovery`.
- Post-reflect then corrected the diff target from `ac80f176..HEAD` to the actual working-tree PRD diff, preventing another meta-level false audit.

### 2. Contract-implementation enumeration

Result: **strong in some troubleshoot artifacts, inconsistent in PRD task artifacts**.

Evidence:
- CAUGHT examples: PRD CLI audit F-04 enumerated Write-emitting steps missing from `_STEP_ARTIFACT_FILES`; F-07 found `--where` stored but unread; F-11 found `PrdMonitor` dead; F-08/F-22 found gate criteria fields declared but unevaluated.
- CAUGHT example: TASK-RF-20260520-050937 added a round-trip test tying prompt-instructed sections to gate checks.
- RUBBER-STAMP example: PR #71 remediation and older PRD E2E artifacts improved local contracts but did not enumerate the CLI process contract for `--file` semantics or `prd resume` durable persisted-SPECS semantics.

### 3. Unmask-and-sweep

Result: **eventually good, but mostly after an anchor bug forced wider audit**.

Evidence:
- The PRD CLI audit is the main successful sweep: 39 consolidated findings, 27 adjudicated, 3 critical, pattern audit P1-P9, and remediation batches A-F.
- The troubleshoot reports for integration contracts and spec fidelity show the healthier pattern: after identifying one failure, they searched for invariant-level recurrence rather than only the immediate symptom.
- Earlier artifacts tended to stop at local pass conditions, letting sibling defects persist (duplicate `--spec`, resume WARN blind spot, dead monitor, static dispatch tables, wrong mock surface).

### 4. Heterogeneous, off-path review

Result: **correlated with catches, absent or too narrow in rubber-stamps**.

Evidence:
- PR86 and spec-fidelity deep-dive both used Tier 2/adversarial debate and found invariant-level issues.
- PRD CLI audit used six parallel slice audits plus adjudication and caught the dispatch/static-map family.
- Post-prd-local-file stopped at Tier 1, but this was acceptable only because the task spec was narrow and the audit corrected its diff target and ran deterministic grep/tests. The broader lesson is not "always Tier 2"; it is "Tier 1 must include the actual runtime/off-path surface, not just source mapping."

## Meta-diagnosis

The recurring pipeline failure is not lack of review volume; it is **review surface mismatch**. Many artifacts checked intended code edits, prompt schemas, or markdown outputs, but the escapes sat at seams: production entrypoint vs helper path, subprocess CLI semantics vs local paths, persisted run state vs resume config, dynamic artifact names vs static dictionaries, and mocked stream output vs disk artifacts.

Artifacts that caught bugs had at least one of these properties:
1. Re-ran or modeled the same deterministic code path the runtime uses.
2. Enumerated producers and consumers of a contract, not just the edited function.
3. Treated one found bug as an anchor for a family sweep.
4. Used an off-path reviewer or adversarial invariant probe.

Artifacts that rubber-stamped had the opposite shape: local proof, narrow diff mapping, or mocks that bypassed the real failing interface.

## Recommendations for the troubleshoot/debug meta-pipeline

1. Add a mandatory **runtime-entrypoint replay card** for CLI pipeline bugs: command shape, environment assumptions, process boundary, artifact producer, artifact consumer, and whether tests/mocks use the same boundary.
2. Add a **contract ledger** to troubleshoot reports: every declared knob, filename pattern, gate criterion, CLI flag, persisted field, subprocess arg, and monitor must list at least one live consumer or be marked intentionally dead.
3. When an anchor bug is found, require an **unmask sweep query** over sibling patterns before closing: static maps, dynamic IDs, declared-but-unused fields, stdout-vs-disk artifacts, resume-vs-run asymmetries, and mock-vs-runtime divergence.
4. Preserve Tier 1 for narrow fixes, but require it to state why an off-path review is unnecessary. If the bug crosses CLI/subprocess/filesystem/runtime-state boundaries, escalate to heterogeneous review or run a targeted runtime smoke.

## Evidence paths

- `/config/workspace/IronClaude/.dev/eval-workspaces/prd-cli-audit/SEVERITY-RANKED-FINDINGS.md`
- `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260520-050937/TASK-RF-20260520-050937.md`
- `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260521133223/TASK-RF-20260521133223.md`
- `/config/workspace/IronClaude/.dev/troubleshoot/build-anti-instinct-uncovered-contracts-20260525141717/REPORT.md`
- `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/REPORT.md`
- `/config/workspace/IronClaude/.dev/troubleshoot/spec-fidelity-deep-dive-20260527045400/REPORT.md`
- `/config/workspace/IronClaude/.dev/troubleshoot/prd-spec-review-r140-20260606174115/REPORT.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-prd-local-file-20260609-005242/TASK-RF-prd-local-file-20260609-005242.md`
- `/config/workspace/IronClaude/.dev/reflect/post-prd-local-file-20260609105644/REPORT.md`
- `/config/workspace/IronClaude/.dev/tasks/done/TASK-E2E-20260327-prd-pipeline-e2e/reviews/adversarial-qa-agent11.md`
- `/config/workspace/IronClaude/.dev/tasks/done/TASK-E2E-20260327-prd-pipeline-e2e/reviews/adversarial-qa-agent6.md`
- `/config/workspace/IronClaude/.dev/tasks/done/TASK-E2E-20260327-prd-pipeline-e2e/reviews/adversarial-qa-agent4.md`
