# Stage Value Review — task-builder

Output root: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z`
Stage reviewed: `task-builder`
Date: 2026-06-10

## Net value estimate

**Estimated net defect-catching value: 35%.**

Interpretation: task-builder added real value as a structure-and-routing layer, especially once `/sc:reflect` PRE/POST review was wired in, but for the canonical escape set its value was mostly indirect. It produced remediation task files and later encoded better reflect gates, yet it also rubber-stamped or miswired some of the exact off-path checks that should have caught the escapes earlier. The stage was more effective at making work auditable and executable than at proving runtime-entrypoint correctness.

Breakdown:

| Dimension | Score | Rationale |
|---|---:|---|
| Caught defects before merge/runtime | 25% | It did catch reflect/tasklist emitted-output and TCS issues through the #138/#142 dogfood/e2e path, but none of E1-E4 were caught before escaping; E5 was a task-builder-generated reflect wiring flaw caught later while auditing #151. |
| Routed remediation | 55% | Stronger: the stage produced concrete task/remediation surfaces, e.g. the PRD local-file task encoded zero-`--file` grep, inverted tests, inline-content tests, and missing-path guards. |
| Avoided theatre/rubber-stamps | 25% | Weak: #144 had four PASS QA passes while still changing POST reflect semantics; #138's off-path review existed but #153 proved its diff target could exclude actual uncommitted work. |
| Runtime/contract coverage | 30% | Weak-to-mixed: artifacts improved task schemas and reflect gates, but did not require runtime-entrypoint replay or consumer enumeration across PRD-specific evaluators, subprocess args, and generated task execution semantics. |

## What this stage actually caught

1. **Reflect emitted-output hygiene and TCS normalization (#142).** The live Stage 10.5/post-reflect e2e sweep found two real defects after #138: emitted guard prose with a literal `/sc:task` token, and TCS S6 failure to normalize quoted-emoji type values. This is the strongest evidence that task-builder can catch defects when it runs generated tasklists through the actual downstream scanner/sprint surface. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` lines 129-141 and `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row REFLECT-E02.

2. **Carry-forward drift was noticed, but not fully de-risked (#144).** The convergence branch explicitly carried forward #138 reflect wiring and documented semantic changes: POST reflect changed from halt-for-human to self-run subagent/remediate/log behavior, frontmatter schemas were mirrored into templates, and four independent QA passes returned PASS. That is useful routing/traceability, but the PASS evidence did not prevent the later wrong-diff escape. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` lines 169-181 and `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` line 18.

3. **Later remediation tasking for E1-style runtime bugs was concrete.** The PRD local-file remediation task encoded the actual symptom and verification expectations, including zero `--file` grep, inverted tests, inline-content tests, and missing-path guards. This is routing value, not early detection. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md` lines 29-31 and 42-45.

## What escaped despite this stage

1. **E1 / PRD cloud-file misuse escaped runtime-entrypoint verification.** The task-builder/reflect ecosystem did not force a headless `superclaude prd run --spec` e2e with no session token before #151. The saga evidence says tests inspected command construction without exercising the headless subprocess path, and roadmap/tasklist/validate already forbade `--file` while PRD still emitted it. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row PRD-E04; `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` line 19.

2. **E2 and E3 / parallel gate false positives escaped parser-surface sweeps.** The heavyweight generated task-file gate halted on a sequential final completion phase (#154), then halted again on Task-Log placeholder headings (#155). Task-builder should have been the natural owner of generated MDTM phase semantics, but the real check still lacked a full generated-file parser fixture. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` rows PRD-E05 and PRD-E06; `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` lines 21-22.

3. **E4 / advisory semantic-check divergence remained off-path.** The contract cartography shows normal PRD runtime does not call the generic evaluator changed by #155; it calls `PrdExecutor._evaluate_gate()`, which still treats any non-True semantic check as fatal and ignores `SemanticCheck.advisory`. Task-builder did not require a consumer inventory for semantic checks before declaring the advisory-gate change safe. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/contract-implementations.md` lines 14-18 and 56-63.

4. **E5 / POST-reflect wrong diff was introduced or preserved by the task-builder-generated review path.** Reflect was wired into task-builder, but generated POST-reflect used `/sc:reflect --mode post --diff <start_commit>..HEAD`; with uncommitted task work it audited none of the actual work, and with unrelated commits it could audit foreign work. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row REFLECT-E01; `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` line 20.

## Theatre vs value diagnosis

The stage's ceremony was not empty: task-builder gave the work durable structure, research/QA artifacts, frontmatter schemas, PRE/POST reflect hooks, and concrete remediation checklists. However, for this saga much of that ceremony sat one layer above the defect surfaces. The canonical escapes were concentrated at seams:

- generated task text vs real parser boundaries;
- source-level command construction vs headless subprocess behavior;
- generic gate evaluator vs PRD-specific evaluator;
- start-commit diff ranges vs uncommitted `/task` runtime semantics;
- QA PASS matrices vs runtime-entrypoint replay.

So the stage was valuable as a **routing and auditability layer**, but underpowered as a **defect-catching gate**. Its strongest successful pattern was when it dogfooded the generated output through the actual downstream runner/scanner (#142). Its weakest pattern was accepting PASS from same-frame or source-surface QA without proving that the generated task, reflect, or PRD command would exercise the same runtime boundary later used by operators.

## Single highest-leverage improvement

**Add a mandatory Generated-Task Runtime Contract Card to every task-builder output that mutates or validates a pipeline.**

The card should be a required section in the generated MDTM task and a required POST-reflect input. It must name, in one compact table:

1. the exact operator entrypoint to replay, e.g. `superclaude prd run --spec <file>` or `superclaude sprint run <index>`;
2. whether the proof crosses a subprocess, filesystem, resume-state, or generated-markdown parser boundary;
3. every contract producer and consumer touched by the change, including sibling evaluators and generated templates;
4. the actual e2e/smoke command or fixture that proves the generated artifact is consumed by the same runtime path;
5. a `NOT PROVEN` line for any boundary not executed, which blocks PASS unless explicitly accepted by a human decision item.

This one change targets all five canonical escapes: it would have forced headless PRD `--spec` replay for E1, generated full-task parser fixtures for E2/E3, semantic-check consumer enumeration for E4, and uncommitted working-tree diff proof for E5.
