---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-issueSummary-20261126-115114
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Recognize everyday performance descriptions

Source: ./source.md
Goal: Everyday loading-delay and hang descriptions select the existing performance type, with the required observed result and synchronization evidence recorded.

## Constraints

- Follow ./source.md and the original acceptance criteria of issue 610. Nothing to decide: build what the issue asks for, within its own scope.
- No Jev call, preflight component, gateway change, or changes to other keyword rows beyond the leak decision. Do not redesign the classifier or force Tier 2 escalation.
- Edit canonical source only. Generated .claude/ copies are never staged; .dev/issues/ is not staged. Stage .dev/tasks/, including its artifacts. Commit, push and pull request work remain outside this plan and follow the story's later steps.
- Add or extend a test only if existing repository coverage tests this table; otherwise preserve manual evidence instead of inventing a new matcher or test system.
- Do not change the installed user-wide skill just to make a check pass. The manual run must consume the changed checkout skill, not silently exercise the old installed row.

## Phase 1: Keep the existing classifier and fill its keyword gap

## Task 1: Extend the performance row and explain leak ambiguity

In src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md, Wave 0 step 2, append the exact phrases "too long to load", "takes forever" and "hangs" to the existing performance row. Retain "leak" in both existing rows and add a short rationale next to the ambiguity rule: a leak may mean resource leakage or disclosure, so an ambiguous report must remain untyped rather than silently discard security candidates. Keep the existing command and Wave 3 specialist selection unchanged. Inspect existing coverage under tests/ before deciding whether its conditional test requirement applies. Run make sync-dev and make verify-sync after the edit; record their actual outcomes under ./artifacts/ without staging generated mirrors.

Acceptance criteria:
- The performance row contains all three new phrases and keeps its existing cues.
- Both leak listings remain; the written reason preserves the existing leave-type-unset ambiguity rule, including security candidates for Tier 2. Other keyword rows and escalation behavior are unchanged.
- The command src/superclaude/commands/troubleshoot.md still supports auto-detection and explicit --type; Wave 3 still uses performance-engineer and root-cause-analyst for performance, and security-engineer for security. No command-file change is required.
- Coverage inspection records where it searched and what it found. Existing phrase/table coverage is extended only if found; otherwise no new test framework is introduced.
- make sync-dev and make verify-sync run after the edit, and verify-sync exits zero. Their output is retained in ./artifacts/; only canonical source and task-package evidence are staged.

## Phase 2: Deliver the observed classification and synchronization evidence

## Task 2: Record the manual acceptance results required by the issue

Depends on: Task 1

Deliver the manual acceptance evidence required by ./source.md and issue 610. Exercise the updated troubleshooting skill through a fresh headless session (claude --print --output-format stream-json --verbose --no-session-persistence --max-budget-usd, with --plugin-dir pointing at a temporary plugin under ./artifacts/). MF-1: that plugin, for example named issue610-check, holds .claude-plugin/plugin.json and a byte-identical copy of the Task 1 skill directory as skills/sc-troubleshoot-protocol/; it is verification evidence, not a shipped plugin, and the user-wide installation is not touched. MF-1: the child must call the Skill tool for issue610-check:sc-troubleshoot-protocol on the exact input "ccsession is taking too long to load", with no --type, run all of Wave 0 including creating the real audit file, emit the Wave 0 completion line and stop there; the launch prompt must not state the expected type. Retain under ./artifacts/ the stream transcript with the Skill tool call and consumed path, sha256 of the plugin copy and of the checkout skill, the audit header and the completion line. MF-1: label the run a namespaced checkout-skill, Wave 0-only run, not proof that the default /sc:troubleshoot name resolves to the changed copy or that diagnostic agents ran; a source-text assertion or table reading is not runtime evidence. Also check "takes forever", "hangs" and ambiguous "leak" wording against the updated Wave 0 instructions and distinguish these bounded classification checks from a full diagnostic run. Use the existing audit/evidence formats rather than adding product logic. Run the related existing tests under tests/troubleshoot/ and retain their observed result. Post the exact sample's observed type and the leak rationale as an issue comment on IronbellyOrg/IronClaude issue 610, with the source change and verification result; do not stage .dev/issues/.

Acceptance criteria:
- The exact sample run, with no --type override, shows an actual Skill tool call for the plugin copy in the transcript, a real audit file, and the child's own Wave 0 complete: type=performance with a matching audit header. Evidence, consumed path and hashes are under ./artifacts/. A failed load, missing audit file or static table comparison is not a pass (MF-1).
- Bounded checks record performance for "takes forever" and "hangs"; an ambiguous leak report remains unset and does not exclude security. State their scope honestly, without claiming all specialist agents ran.
- Related tests under tests/troubleshoot/ have an observed result recorded under ./artifacts/. A failure is investigated and reported, not hidden or called a pass.
- A comment on https://github.com/IronbellyOrg/IronClaude/issues/610 records the exact sample's observed result, leak rationale, and successful synchronization check. Its comment URL is retained under ./artifacts/.
