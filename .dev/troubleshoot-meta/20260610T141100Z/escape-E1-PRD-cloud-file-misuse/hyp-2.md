# Why-it-escaped hypothesis card: E1-PRD-cloud-file-misuse

## Lens

Verification-artifact / off-path-review lens. This card intentionally analyzes the review and evidence artifacts, not the PRD runtime implementation path.

## Escape

`E1-PRD-cloud-file-misuse`: Headless `superclaude prd run --spec` crashlooped at `scope-discovery` because PRD passed local filesystem paths to Claude CLI `--file`, which is a cloud-download/session-token mechanism.

## Hypothesis

The defect escaped because the verification artifacts were optimized for local source-level proof and narrow task closure, while the failing behavior lived at an off-path process boundary: the headless CLI subprocess invocation with no Claude session token. Reviews saw that PRD command construction existed and that the fix later removed `--file`, but the pre-escape review surface did not require a live or faithfully modeled headless runtime replay, nor a sibling-pipeline contract ledger comparing PRD against roadmap/tasklist/validate file-delivery rules.

In short: review volume existed, but the artifacts proved the wrong surface.

## Evidence chain

1. The defect table classifies PRD-E04 as a runtime-entrypoint and sibling-contract miss: PRD emitted `claude --file` while roadmap/tasklist/validate already forbade it, and tests inspected command construction without running the headless subprocess path. The expected catcher was a headless PRD `--spec` e2e with no session token plus a cross-pipeline no-local-path-via-`--file` guard. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` line 10.

2. The PR #151 summary shows the later fix task's evidence was deterministic but post hoc: it removed `--file`, added inline-content tests, and validated `grep -rn '"--file"' src/superclaude/cli/prd/` returned zero matches. That is strong remediation evidence, but it also implies the earlier verification set did not have this grep/contract guard before the escape. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` lines 2-16.

3. The broader chronology shows `--spec` was introduced to solve `--where` eviction, then the cloud-file crash was discovered the next day. The sequence suggests review attention was anchored on deterministic spec binding and prompt survival, not on whether the delivery mechanism crossed a cloud/session-token boundary in headless operation. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` lines 1-13 and 49-63; `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` lines 14 and 19.

4. The pipeline artifact audit directly labels the relevant artifact family as source/test-surface focused: prior remediation improved contracts but did not runtime-execute the headless PRD entrypoint; older E2E/adversarial reviews were marked `RUBBER-STAMPED` for E3 because their mock/subprocess surfaces did not test headless local-file behavior. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md` lines 23-33 and 38-45.

5. The same audit identifies the generalized failure mode as review surface mismatch, not lack of review volume: many artifacts checked intended code edits, prompt schemas, or markdown outputs while escapes sat at production entrypoint vs helper path, subprocess CLI semantics vs local paths, and mocked output vs runtime artifacts. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md` lines 74-84.

## Why review missed it

- The review artifacts treated command construction as sufficient evidence, but the failure required observing Claude CLI's runtime interpretation of `--file` under a no-session-token environment.
- The cross-pipeline invariant was available but not encoded as a verification artifact: roadmap/tasklist/validate already used inline delivery and forbade the local-path `--file` pattern, while PRD remained the outlier.
- Earlier PRD artifacts had a recurring pattern of mock or helper-path validation. The artifact audit calls out mock/subprocess surfaces that bypassed the real failing interface, so PASS signals did not cover the process boundary that mattered.
- Off-path review existed elsewhere in the saga, but for this escape the off-path surface was either absent or too narrow until the post-fix local-file task and post-reflect report.

## Confidence

High. Multiple independent artifacts converge on the same explanation: the missing verification was not another unit assertion in PRD code, but a runtime/off-path artifact proving the real headless subprocess contract and a sibling-pipeline sweep proving `claude --file` was never used for local filesystem delivery.

## Preventive verification artifact

For future PRD/CLI pipeline changes, require a small verification card before review closure:

- Runtime command replay: exact CLI command, environment assumptions, process boundary, and expected terminal behavior.
- Contract ledger entry for every file-delivery mechanism: local inline content, local path reference, cloud file token, persisted path, or artifact path.
- Sibling-pipeline grep/contract guard for shared CLI mechanisms.
- Explicit statement whether tests execute the same process boundary as production; if not, mark the review incomplete or justify why the mock is faithful.
