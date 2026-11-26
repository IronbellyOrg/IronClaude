# PR-submit architecture analysis

Template: analysis structure registered in ../../362/report-template.md, adapted to the assigned source path.

## Scope and grounding

Command: `/sc:analyze src/superclaude/pr_submit --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/421/analyze`.

Target: the shared PR monitor package, the narrowest common source directory containing reviewer completion, merged outcomes and CI classification. Supporting reads followed its skill-level CI orchestration and existing Codex tests. This was a targeted static architecture check for issue #421, not a whole-package correctness audit.

Codegraph: index_state=stale, checked_at=2026-11-23T23:08:48Z; degraded: graph:stale

Readiness reported one modified report file in another task's directory. No graph lookup or mutating graph command was run after that result; Glob, Grep and Read supplied the evidence. Checkout: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`.

## Architecture and metrics

Discovery found 13 Python modules directly under the target directory. The relevant flow is bounded: marker parser -> Codex completion record -> thread selection -> clean/findings state -> per-reviewer wait outcome -> merged reviewer outcome. The protocol skill then changes the data source from reviews to CI checks.

The core already separates pure classification from external fetching. Preserve that boundary: the security-half gate belongs beside the existing Codex parser/completion logic, while fetching a final review snapshot belongs in the skill's CI orchestration. CI check classification alone cannot attest that a security review has finished.

Evidence locations:
- `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/pr_submit/reviewers.py:113-133`, `:141-207`, `:210-247`, `:367-419`.
- `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/pr_submit/ci.py:25-55`.
- `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:311-314`.

No runtime performance measurement, coverage percentage or numerical quality score was collected.

## Severity-rated findings

1. **High: a partial Codex completion can be treated as complete.** A valid completed code marker with no selected roots can return clean even if the sibling security activity remains running or refers to another head. The parser throws away that sibling; the wait outcome accepts clean/findings before its timeout branch. This can omit a security finding from the monitor's final result. The detection contract explicitly encodes the omission at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md:119-140`.
2. **High: final CI success carries forward an old reviewer decision.** The skill's CI phase permits final clean after clean checks without refreshing review state. A finding posted during that wait therefore has no mandatory observation point before final clean. Evidence is the CI phase's explicit clean transition, not a claim that CI check classification itself should query reviewers.
3. **Medium: existing tests do not distinguish the two activities.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/pr_submit/test_codex_reviews.py:139-159` covers completed snapshots; `:178-202` changes the first completed status, exercising code-review incompleteness rather than an independently running security half. Repository searches found security-half text in JSON fixtures, not tests targeting its independent transition. This leaves the two high-impact conditions unpinned by a dedicated regression.

These are existing defects/gaps, not changes introduced by this report. A failure scenario was traced statically; no dynamic reproduction is claimed.

## Recommendations and roadmap

Use the existing completion gate and orchestration seam, not a parallel monitor or a second reviewer identity. Implement the two-half completion rule and a post-CI review refresh together; preserve legacy markers, head binding, null security finding counts, bounded waits and round limits. Then add the focused regression matrix and update the single detection contract plus user guidance.

The issue verdict, effort/priority estimates, exact next steps, GitHub relationships and historical evidence are maintained in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/421/findings.md`, rather than independently duplicated here.

## Verification limits

Static quick analysis only: no tests, build, live monitor, source edits or external writes. Full GitHub event timelines, historical comment edits and original monitor logs were not independently verified under the brief's view/list-only restriction. The associated findings report labels those limitations explicitly. Stale graph access degraded evidence retrieval, not the analysis outcome; the required source paths were read directly.
