# Summary: #703 Follow-ups from the issue 624 review: five small items in surgical remediation

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/703
- Type: bug
- Complexity: medium (rubric: `refs/claim.md`)
- Effort estimate: 6 hours
- spec-route: design — Medium, with explicit five-item acceptance criteria and test/sync gates; use the documented wording-only option for recording rather than adding a new writer.

## What the issue asks for

Finish five bounded corrections in workflow's plan-repair feature: recognize only a real superseded warning, say repairs happen on a copy, describe all three routing thresholds, promise only the recording that actually happens, and directly test the existing rule that the old package must be archived before the new one is placed. All five remain relevant on `origin/integration` at `f6c2a870d83f2cd0d32434aec4b6daa2529daefd`; PR #705 restricted the reviser but did not complete these items. The parent feature in #624/#696 is already merged, so this is a follow-up, not implementation of the parent feature. The issue's master baseline is stale: the repository default is integration, and both new tests do not need to fail before the fix because the placement guard already exists.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` | `archive` starts at line 404; its whole-contract search at 434 suppresses warnings on unrelated mentions. `place` already refuses before archive at 608–609. `mark` and `place` supply the actual regenerate/surgical metadata writes. |
| `tests/skills/test_workflow_remediation.py` | Add the unrelated-mention regression and direct place-before-archive test. Preserve existing case-insensitive warning deduplication, list-form, byte-restoration and rollback tests. The marker regression should expose the old defect; the guard regression protects behavior that already exists. |
| `src/superclaude/skills/sc-workflow-protocol/SKILL.md` | Wave 4R's none-recording promise at 101 needs narrowing. Keep the restricted-reviser and copy-only rules. |
| `src/superclaude/skills/sc-workflow-protocol/refs/remediation.md` | Authoritative routing/copy lifecycle. Clarify forced-route output at 31; keep the #705 agent safeguards and coordinator-supplied diff rule, now at 73 rather than 72. |
| `src/superclaude/commands/workflow.md` | Actual command source, resolving the issue's shorthand `commands/workflow.md`. Lines 44 and 100 also repeat recording promises and must agree with the narrowed skill/ref wording. |
| `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` | Change “surgically in place” at 81 to “on a copy”; no reflection-engine or contract change. |
| `.dev/README.md` | Correct surgical/regenerate bullets at 63–64. Zero blockers must take none first; otherwise surgical requires B <= 3, HIGH <= 5 and Medium <= 9 together; otherwise regenerate. Point at the authoritative ref. |
| `plugins/superclaude/skills/sc-workflow-protocol/{scripts/remediate.py,SKILL.md,refs/remediation.md}` | Three existing skill mirrors must receive the corresponding updates. |
| `plugins/superclaude/commands/workflow.md` | Fourth existing mirror, necessary when correcting the duplicate command wording. All four scoped source/plugin pairs currently have matching hashes. No reflection handoff plugin mirror was found. |
| `docs/designs/surgical-remediation.md` | Historical feature design and acceptance context; not a new implementation target. |
| `.dev/tasks/to-do/TASK-WF-blockerStage4-20261117-170451/return-contract.yaml` | Real unrelated-mention example at 14. Evidence only: do not reproduce by modifying or moving this live package. |
| PR #696 / commit `f2904292e`; PR #705 / commit `1a6c8723f` | Parent implementation and subsequent restricted-reviser fix. The complete scoped integration history since issue creation contains these changes, not a later fix for the five items. Preserve their existing safeguards. |
| Default branch and toolchain | Use integration, not the issue's master baseline. #618 remains open as toolchain context, not a verified blocking dependency; the dev extra currently pins ruff. Validation-environment state was not changed or verified by executing installs. |

The estimate is 6 hours: 2 for warning detection and regression cases, 1 for documentation alignment, 1 for the guard test and mirrors, and 2 for review and validation. Medium follows the over-4/up-to-16-hour rubric within one remediation workflow; reflection is a documentation-only caller adjustment, not a second implementation subsystem. No new metadata writer, dependency, placement guard or contract version is required.

Acceptance remains all five corrections plus passing focused/skills tests, lint, formatting and dev synchronization checks, and matching existing plugin mirrors. These gates were not run in this read-only check. `make sync-dev` updates generated development copies, not plugin mirrors; never stage generated `.claude/` content. The previous backlog comment's three-mirror scope omits the existing command mirror, which also needs alignment.

## Analysis

- [Current-code remediation analysis](analysis/analyze-sc-workflow-protocol.md) — standard `/sc:analyze` flow, without a depth flag; static dependency, quality, preservation and validation guidance.
- [Accuracy check](accuracy-check.md) — verdict `out_of_date`, with current evidence for all five items, the resolved findings, comments and relevant merged PRs. The stale branch/merge instructions do not mean the five repairs are done.

Codegraph MCP lookup tools and Augment/Auggie were unavailable; the guarded CLI readiness check reported a fresh index and the analysis continued with Glob, Grep, Read and read-only Git/GitHub inspection. Tests and whole-checkout lint/format/sync results, full agent-driven runtime behavior and the unavailable original review file remain unverified. The historical findings linked in the issue were readable, but PR #861 is closed without merge and is not evidence of an implementation.
