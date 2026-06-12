# Root cause: E1-PRD-cloud-file-misuse

## Merged claim

The defect escaped because verification stopped at PRD's intended local-file delivery abstraction instead of validating the actual headless Claude subprocess contract, and because no sibling-pipeline contract sweep flagged PRD as the only pipeline still delivering local filesystem paths through `claude --file`.

PRD treated `--file <local_path>` as a local content attachment mechanism. The Claude CLI interpreted `--file` as a cloud-download/session-token mechanism. In the production headless `superclaude prd run --spec` path, that mismatch only becomes visible after `PrdExecutor` hands PRD-specific extra arguments to the shared Claude subprocess and runs without `CLAUDE_CODE_SESSION_ACCESS_TOKEN`.

## Adversarial comparison

### Surviving claims from hyp-1

- The strongest root-cause claim is the runtime-entrypoint miss: tests and review validated config storage, prompt visibility, and argv construction, but did not execute the same headless subprocess boundary that failed in production.
- The invalid contract lived after command construction. A unit assertion that `_build_file_args()` returns `['--file', path]` could pass while the real `claude --print --no-session-persistence` subprocess immediately exits with a session-token error.
- The sibling-pipeline mismatch is material, not incidental: roadmap/tasklist/validate already forbade the local-path `--file` pattern, while PRD remained the outlier.

### Surviving claims from hyp-2

- The broader verification-artifact diagnosis is valid: review volume existed, but much of it proved local source/test surfaces rather than the off-path process boundary where the failure occurred.
- The missing artifact was not simply another PRD unit test. It was a faithful runtime replay or e2e of headless `prd run --spec` with no session token, plus a shared contract ledger/grep proving local paths are never sent via `claude --file`.
- The generalized failure mode is review surface mismatch: local proof, narrow task closure, or mocks can rubber-stamp behavior when the real failure sits at a subprocess, persisted-state, or producer/consumer contract seam.

## Refuted or narrowed claims

- Hyp-2's phrasing that the analysis is "not the PRD runtime implementation path" is too narrow for root-cause validity. The runtime implementation path is necessary evidence because it identifies the exact boundary where the false `--file` contract became observable.
- Hyp-1's detailed implementation reconstruction is useful but should not be over-generalized into a code-path-only cause. The escape was not only that one subprocess path lacked an e2e; it also required failure to compare PRD's file-delivery contract against sibling pipelines that had already rejected `--file` for local files.
- Post-fix grep/test evidence proves the remediation direction and the missing pre-escape guard, but it is post hoc. It supports the root cause only when paired with pre-escape evidence that tests had inspected construction rather than executing headless runtime behavior.

## Evidence chain

1. `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` line 10 classifies PRD-E04 as a headless `--spec` crash at `scope-discovery`, caused by local paths sent to `claude --file`, and names the missed catchers: runtime-entrypoint verification plus a sibling-pipeline no-local-path-via-`--file` guard.
2. `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` lines 2-16 records the concrete failure and fix evidence: `claude --file` required `CLAUDE_CODE_SESSION_ACCESS_TOKEN`, the headless subprocess exited quickly with `Session token required for file downloads`, PRD was the only pipeline emitting `--file`, and the fix removed `--file` while adding inline-content tests and a zero-match grep.
3. `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` lines 49-63 independently repeats the same root cause and ties it to PR #151's remediation: remove `--file` emissions from `src/superclaude/cli/prd/process.py`, inline spec content in prompts, and align with roadmap/tasklist/validate.
4. `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` lines 14-19 shows the sequence: deterministic `--spec` ingestion was added after a `--where` failure, then the cloud-file/session-token crash appeared in the next PR cycle. That supports the review-anchor explanation: attention moved to deterministic binding, not to whether the delivery mechanism was valid at the headless subprocess boundary.
5. `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md` lines 38-45 states runtime-entrypoint verification failed until late, and `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md` lines 74-84 generalizes the pattern as review surface mismatch: source/test surfaces and mocks passed while escapes sat at seams such as subprocess CLI semantics vs local paths.

## Final root cause

The root cause was a false file-delivery contract left untested at the only boundary that could reject it: PRD's headless Claude subprocess invocation. Review and tests validated that PRD preserved spec paths and constructed the expected `--file` argv, but they did not validate that Claude CLI accepts local filesystem paths via `--file` in `--print`/no-session operation. A cross-pipeline contract sweep would also have exposed PRD as inconsistent with roadmap/tasklist/validate, which already avoided `--file` for local file delivery.

## General prevention rule

For CLI pipeline changes, review closure must prove both dimensions:

1. Runtime-entrypoint fidelity: at least one test or recorded verification must execute or faithfully model the same subprocess/environment boundary used in production, including relevant environment absences such as no session token.
2. Shared-contract consistency: any file-delivery mechanism must be enumerated across sibling pipelines, with a guard that prevents local filesystem paths from being routed through cloud/session-token-only mechanisms.

No product fix is proposed here; PR #151 already addressed the implementation by removing PRD `--file` emissions and inlining specs/refs.
