# Summary: #758 [FEATURE] Assume the user is coming in blind when asking a decision or question

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/758
- Type: feature
- Complexity: simple (rubric: `refs/claim.md`, up to 4 hours in one area; this changes one output style and its regression/delivery checks, not the installer or another subsystem)
- Effort estimate: 3 hours
- spec-route: design — Simple feature with explicit acceptance criteria for concise context, implications, risk, existing-file links, no-file fallback and preservation of existing question rules.

## What the issue asks for

Make Pragmatic questions and decision requests understandable to someone who has not followed the session: briefly explain context, implications and risks before asking. Link an existing file containing more detail when available, never create a file solely to link it, and say when no such file exists. Keep one question at a time, self-contained options and the existing answer lines. The feature remains missing, but the issue is out_of_date because its Makefile-based style-delivery assumption and master-base instruction are wrong; plan against integration and verify actual delivery in an isolated home.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/output-styles/pragmatic.md` | Primary edit target: Decision requests section. Existing general self-sufficiency, reader-familiarity and answer-line guidance already exists; add the missing question-specific context/implications/risk and existing-file-only rule without duplicating or weakening it. |
| `tests/commands/test_pragmatic_plain_english.py` | Existing pure file-content tests provide uniqueness, order and section-placement patterns. Extend coverage to the new guidance and preserved older rules. |
| `tests/cli/test_install_user_setup.py` | Existing isolated-home style-install test checks only the header. Use its pattern to verify exact shipped content and the existing keep/forced-refresh behavior without changing real user configuration. |
| `src/superclaude/cli/install_user_setup.py` | `install_output_styles(home=..., force=...)` delivers packaged styles to the selected home's `.claude/output-styles`; `_copy_tree` keeps existing files without force and backs up differing files on forced replacement. Inspection target only; no installer behavior change is needed. |
| `Makefile` | Neither sync-dev nor verify-sync handles output styles. Retain the requested sync check as a separate regression gate, not proof of delivery; do not add a style-sync mechanism for this issue. |
| `src/superclaude/core/RULES.md` | The issue's optional Verification Before Recommendation location governs evidence before advice, not question context. Keep core-rule changes outside the smallest complete solution, consistent with the backlog comment. |
| `src/superclaude/core/WORKER-CONTRACT.md` and AskUserQuestion tooling | Explicitly outside this user-facing style change. Do not alter worker communication or question UI. |
| `CLAUDE.md` and live repository default branch | Current policy uses integration. PR #824 supersedes the issue's old master-base instruction. |
| `.dev/iterations/iteration-3/stories/758.md` | Current story record tracks the work as a simple enhancement on integration. It does not implement the feature. |
| Earlier PRs #608 and #284 | Established plain-English/answer-line and multi-question guidance respectively; neither implements this feature. Recent installer PRs #768/#778 are browser-only and do not change style delivery. |

The 3-hour estimate allocates approximately 0.5 hour to precise rule wording, 1 hour to focused content and isolated-home delivery checks, 0.5 hour to sample-question review with and without detail files, and 1 hour to regression checks and review. This assumes no changes to installer behavior, core rules, tooling or worker contracts; broader changes require re-estimation. Content tests check shipped instructions, not a guarantee that every live model response obeys them.

## Analysis

- [Pragmatic output-style and delivery analysis](analysis/analyze-output-styles.md): four gaps cover the missing rule, missing coverage, incorrect delivery assumption and stale base-branch instruction. The analysis followed the installed `/sc:analyze` command without a depth override, using the installed gap-analysis template because issue-protocol provides no analyze-specific template.
- [Accuracy check](accuracy-check.md): claim-by-claim evidence and relevance checks for all 23 scout PRs, including paginated checks for the six capped file lists.

No tests, lint, sync or installation were executed during this read-only claim pass. Their results and real-session effectiveness are Not known yet. MCP codegraph and Augment/auggie tools were not exposed to this worker; analysis used Grep, Glob and Read after the guarded codegraph CLI readiness check, as documented in the analysis file.

## Decided for this work (iteration 3)

- Nothing to decide: build what the issue asks for, within its own scope.
