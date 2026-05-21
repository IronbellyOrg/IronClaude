# REPORT.md Template

The final deliverable of every `/sc:troubleshoot` invocation, regardless of tier. Loaded only in Wave 5.

## Template

```markdown
# Troubleshoot Report

**Target**: <one-line: the symptom or scope as given>
**Type**: <bug|performance|security|build|deployment|test|auto>
**Tier reached**: <1|2|3>
**Confidence**: <0.0–1.0>
**Status**: <success|partial>
**Escalation reason**: <none|low_confidence|multi_domain|forced_by_depth_deep|intermittent|not_reproducible|security_caution>
**Test is wrong**: <true|false> <!-- See "Test-is-wrong rule" below. When true, surface `Test file to update` on its own line and DO NOT recommend code changes as the primary fix. -->
**Test file to update**: <absolute or repo-relative path when test_is_wrong=true, otherwise omit this line>
**Duration**: <seconds>
**Date**: <ISO 8601>

---

## Summary

2–4 sentences. State the symptom, the chosen diagnosis, and the recommended fix. No hedging — the report's job is to give the user a direct answer.

If `status: partial`, lead with the limitation (e.g. "diagnosis is most likely X, but Y could not be verified — see Grounding Gaps").

## Diagnosis

The single chosen hypothesis. Format:

**Root cause**: <one-line>

**Cause class**: <from the triage checklist>

**Detailed explanation**: 1–2 paragraphs. Why this code produces the observed symptom. Reference the evidence section, don't restate it.

## Evidence

A numbered list of evidence items, each a `file:line` citation with a quoted snippet OR a command + actual output. **Every item in this list will be validated in the Wave 5 file:line check** — unfounded items are dropped before the report ships.

1. `path/to/file.py:142` — `result = Path(scratch_root) / "foo"` (no `pathlib.Path` import in the file)
2. Command: `uv run pytest tests/path/to/test_eval_run.py::test_basic -x` → output shows `NameError: name 'Path' is not defined`
3. ...

If a citation in a hypothesis card could not be validated, it does not appear here — it appears in **Grounding Gaps** below.

## Proposed Fix

The recommended change. Be concrete — name the files, describe the diff in plain language. If the fix is short, include the literal diff. Otherwise describe the change and let the user (or Tier 3) write the diff.

**Files to change**:
- `path/to/file.py` — <one-line summary of change>

**Files that MUST NOT change** (REQUIRED when `Test is wrong: true` in the header; OMIT this subsection otherwise):
- `path/to/production_file.py` — <one-line on why this is the wrong file to modify; cite the asymmetric cost — typically "regresses documented behavior at <spec ref>" or "breaks contract relied on by <consumer>">

**Test to verify**:
- `path/to/test_file.py::test_name` should pass after the fix
- (or, "add new test: ...")

**Apply with**: `/sc:troubleshoot --fix ...` (re-run with `--fix` to authorize the Tier 3 task-builder chain), or apply manually.

## Alternative Fixes Considered

**Tier 1 only**: omit this section.

**Tier 2 (Wave 4 ran)**: list the losing fix proposals from the adversarial debate. For each:

- **Fix N — `<one-line>`** (from `<agent-name>`)
  - Rejected because: <one-line — typically "weaker evidence", "higher risk", or "fails edge case X">

This section documents the road not taken so the user can re-litigate if they disagree with the chosen fix.

## Risk + Rollback

What to watch after applying the fix:

- **Likelihood of regression**: <low|medium|high> in <which area>
- **Test coverage of the changed code**: <good|partial|none> — if partial/none, the user should add a regression test before merging
- **Rollback**: <one-line on how to revert if the fix turns out wrong>

For security and performance fixes, this section is mandatory and must be specific. For typos and import fixes, "single-line change, revert with `git revert`" is sufficient.

## Follow-up tasks

Optional section for non-blocking secondary recommendations that are NOT the primary fix. Use when the diagnosis surfaces work worth tracking but separate from the chosen fix — e.g., hardening a related code path, adding observability, updating documentation, deleting dead code. When `Test is wrong: true`, this is where any production-code hardening recommendation goes (the primary fix stays test-only).

Each item should be:

- One-line summary
- (optional) `Suggested type`: `bug` | `refactor` | `docs` | `observability` | `test`
- (optional) Cited evidence pointer to the line that motivated the follow-up

If there are no follow-ups, write "None."

## Grounding Gaps

What the skill could **not** verify. If `status: partial`, the items here explain why. Examples:

- "Reproducer not available in sandbox — relied on user-pasted stack trace"
- "MCP `auggie` was unavailable; grounding used `Grep`/`Glob` only"
- "Hypothesis card from `quality-engineer` cited line 88 of test_foo.py but that file is only 60 lines long — citation dropped"

If there are no gaps, write "None."

## Next Steps

Pick the line(s) that apply:

- Tier 1, high confidence: "Apply the fix manually, or re-run with `/sc:troubleshoot --fix <args>` to generate an MDTM task."
- Tier 1, low confidence (but `--no-escalate`): "Re-run without `--no-escalate` (or with `--depth deep`) to enable Tier 2 fan-out."
- Tier 2 without `--fix`: "Re-run with `--fix` added to your previous invocation to enter the remediation chain."
- Tier 2 with `--fix`, awaiting user accept: "Reply **yes** to proceed to the task-builder remediation chain, or apply the fix manually."
- Tier 3 chain completed (post-`/task`): "Run `/sc:reflect --type task --validate <task-file>` before committing."

## Audit

- **Hypothesis cards**: <list of paths>
- **Adversarial artifacts** (Tier 2 only): <path to artifacts dir, or "Not invoked — single proposal" / "Not invoked — consensus">
- **Self-review** (Tier 2 only): <result>
- **Task file** (Tier 3 only): <path>
- **Audit log**: <path>
```

## Rendering rules

- **No trailing emoji or decorative headers.** The report is a working document, not a marketing brief.
- **Cite or drop.** Every `file:line` in the report must survive the Wave 5 validation pass.
- **No reuse of the original error message in the Summary.** Summarise it in the user's own framing if possible — a verbatim stack trace at the top adds noise without information.
- **Status `partial` is honest.** Marking `partial` with a clear "Grounding Gaps" section is far better than marking `success` and being wrong.

## Test-is-wrong rule

Set the `Test is wrong` header field to `true` when **all** of these apply:

1. The chosen diagnosis names a test file (not production code) as the file requiring change.
2. One of:
   - The test asserts an invariant that the cited spec / requirements doc explicitly contradicts (e.g., test claims policy rejects X but the policy doc allows X)
   - The test was authored before a feature change that legitimately altered the asserted behavior, and was not updated alongside the feature
   - The test mis-models the requirement (typo'd assertion, wrong fixture, wrong expected value)

When `test_is_wrong=true`:

- The **Summary** section MUST open with a single sentence naming the test as the bug (e.g., "The test is the bug, not the code"). No hedging.
- The **Proposed Fix** section's `Files to change` list MUST contain ONLY the test file — not the production code. If the diagnosis also recommends a hardening change to production code, that goes under the `## Follow-up tasks` section (template provides it; treat as a separate ticket), not the primary fix.
- An explicit **`## Files that MUST NOT change`** subsection MUST appear under Proposed Fix, listing every production-code file a careless remediation might touch.
- The **Alternative Fixes Considered** section MUST include "fix the code to make the test pass" with the rejection reason "**This is the DANGEROUS wrong answer** — would regress documented behavior. See evidence."

The asymmetric cost of this flag is the entire reason it exists: a downstream automation chain that "fixes" the code to satisfy a wrong test will silently break documented behavior. The rendering rules above are the human-readable side of that safety net; the `test_is_wrong` flag in the output contract is the machine-readable side.

If the test is wrong AND the code is also missing a defensive guard, keep `test_is_wrong=false` and surface both in `Files to change` — the production-code fix is the load-bearing change and the test update is incidental.
