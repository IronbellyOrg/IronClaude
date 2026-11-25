```yaml
contract_version: 1.9.0
status: partial                      # one citation dropped by the evidence validator (A14); no grounding-gaps file; no human decision pending
mode: pre
tier_reached: 2
confidence_calibrated: 0.81          # blind calibration of the Tier 1 card; reviewer cards calibrated at 0.84 (analyzer) and 0.79 (qa)
citations_total: 62
citations_revalidated: 62
citations_dropped: 1
citations_inferred: 1
citation_budget_policy: full_reread  # more than 20 citations, so the policy allows sampling; every citation was re-read instead
coverage_degraded: parsed-sparse
finding_counts: {blocking: 2, label_high: 0, medium: 2, note: 10}
```

# Pre-execution reflection: plan for issue 848 (stop /sc:issue --claim while a blocked-by issue is open)

- Spec: `.dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/source.md`
- Plan: `.dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/TASK-WF-addTheGitHubBloc-20261125-201412.md`
- Mode: UC-1 (pre-execution coverage and gap audit). Tier 2 ran because the spec has no labeled requirement IDs (the sparse-labeling guard forbids a Tier 1 stop) and the Tier 1 calibrated confidence was 0.81, below 0.85 (`artifacts/tier_decision.yaml`).
- Reviewers: opus class (analyzer) and haiku class (qa); the session model (sonnet class) is the executor of the plan, so it was excluded from the reviewer pool and used as calibrator and judge. Single-vendor note: all aliases are gateway names; one reviewer reported itself as GPT-5.2, the other as claude-gw-tier1a.
- Merge: adversarial debate, convergence 0.91 (threshold 0.80), base variant opus:analyzer; full merged card with every citation: `adversarial/merged-reviewer-card.md`.

## Verdict

The plan covers the whole request (5 of 5 requirement rows matched, `coverage_pct_union` 1.0), but it has **2 blocking gaps** that would make its own acceptance checks fail or break a required outcome, and 2 Medium weaknesses. The plan can be repaired on a copy (route: surgical).

## Coverage matrix

| ID | Source | Requirement (verbatim) | Matched task | Ratio |
|---|---|---|---|---|
| INF-001 | inferred | Add the GitHub blocked-by check to /sc:issue --claim | Task 1 | 1.00 |
| INF-002 | inferred | read repos/<R>/issues/<N>/dependencies/blocked_by in Wave 2 before Wave 3 | Task 1 | 1.00 |
| INF-003 | inferred | stop with E-BLOCKED naming each open blocker | Task 1 | 1.00 |
| INF-004 | inferred | continue as today when none or all closed | Task 1 | 1.00 |
| INF-005 | inferred | continue and say so in the final output when the list cannot be read | Task 2 | 0.86 |

Parsed requirement IDs: 0 (`coverage_pct` is null). The union fields are `coverage_pct_union` 1.0 and `unmapped_requirements_union` empty. The source also names `.dev/issues/848/issue-summary.md`; its extra requirements are covered by plan lines 19, 30, 33 and Tasks 2 to 6 (finding A11).

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | Add the GitHub blocked-by check to /sc:issue --claim | source.md:1 | Task 1 (containment 1.00) |
| INF-002 | read repos/<R>/issues/<N>/dependencies/blocked_by in Wave 2 before Wave 3 | source.md:1 | Task 1 (1.00) |
| INF-003 | stop with E-BLOCKED naming each open blocker | source.md:1 | Task 1 (1.00) |
| INF-004 | continue as today when none or all closed | source.md:1 | Task 1 (1.00) |
| INF-005 | continue and say so in the final output when the list cannot be read | source.md:1 | Task 2 (0.86) |

The evidence validator confirmed all five quotes verbatim at source.md:1; none was dropped.

## Findings

### Finding A1: Blocking (Missing): no task adds the classification entry for the new `gh api` line
- Location: plan Task 1 (plan line 30) and Task 6 acceptance (plan line 91); `tests/skills/test_worker_contract.py:1886-1897, 1951-1958, 3167-3176`
- Evidence: the test scans every line under `src/superclaude/skills`, `commands` and `agents` for `gh pr` or `gh api` and fails for any line whose exact stripped text is not a key of `WRITE_VERB_CLASSIFICATION`. Task 1 adds such a line to `refs/claim.md`; no task edits the table.
- Consequence: `test_every_write_verb_hit_is_classified` fails after Task 1, and Task 6's check that the other readers still pass cannot be met without an edit no task owns.
- Fix: add one `read-only` entry for the final text of the new line (same edit as the line or after it; in Python the jq text `\(` must be `\\(`), keep `gh api` out of SKILL.md, command and guide wording, and widen Task 6's lint criterion to the worker-contract test file.

### Finding A2: Blocking (Decision): Task 1 does not say which outcome rule wins on a failed blocker read
- Location: plan line 30 (Task 1) and line 86 (Task 6 helper)
- Evidence: Task 1 says "Any output line is an open blocker" and "A failed call (non-zero exit ...) means continue" with no order. Verified on 2026-11-25 with gh 2.103.0: a failed read exits 1, prints the raw error JSON on stdout (the `--jq` filter is skipped) and `gh: Not Found (HTTP 404)` on stderr; a read of issue 612 exits 0 with `#611 https://github.com/IronbellyOrg/IronClaude/issues/611`; issue 590 exits 0 with no output. A failing later page of a paginated read prints earlier pages' lines, then exits 1.
- Consequence: read literally, a failed read stops the claim with E-BLOCKED, which the spec forbids; every acceptance check still passes.
- Fix: state the order in Task 1 and pin it in Task 6: any line matching `^#[0-9]+ https://` stops the claim with E-BLOCKED whatever the exit status; otherwise a non-zero exit or any non-matching output means "could not run" and the claim continues; otherwise there are no open blockers.

### Finding A3: Medium: the "could not run" line is not guaranteed to print when a later STOP ends the claim
- Location: plan line 30; `src/superclaude/skills/sc-issue-protocol/refs/claim.md:138-150`, `SKILL.md:150`
- Fix: add one sentence to Task 1 (a later STOP prints the held line before the STOP message) and one Task 6 assertion.

### Finding A10: Medium (Missing): Task 6's ordering check does not pin the order against the assignee checks
- Location: plan lines 33 and 86; `claim.md:41-43`
- Fix: make the helper check the blocker item is after the assignee items too, and add a mutation test that moves it ahead of them.

### Notes (grade Note, no fix pass)
A4 wording near a phrase an existing test forbids; A5 `## Final output` split trap; A6 `--repo` banned in `issue.md`; A7 Wave 2 heading; A8 no `make sync-dev` / `make verify-sync` plan step (Note by orchestrator ruling: final verification is executor-owned); A9 `git diff --stat` wording; A11 coverage record cites only source.md:1; A12 guide row must be ASCII; A13 two acceptance wordings that cannot be evaluated and two readers omitted from plan line 91; A14 issue watcher may re-launch a blocked issue (out of scope, inference). Details and evidence: `adversarial/merged-reviewer-card.md`.

## Dropped citations (evidence validator)

One citation was dropped, not downgraded: finding A14 cited `src/superclaude/cli/issue_watch/launch.py:1-5` for "the issue watcher launches `/sc:issue --claim N --pipeline none`"; those lines are only the module docstring, and `launch.py:34-35` shows the watcher also allows `worktree` and `full`. The claim and citation were removed from A14. One offset was corrected (A10 range now `claim.md:41-43`); A1's quoted lines sit at 1953-1954 (its cited range 1953-1956 holds). A dropped citation forces `status: partial`.

## Recommendations

### Recommendation R-001: Add the read-only classification entry
- **File:** tests/skills/test_worker_contract.py
- **Change:** one `WRITE_VERB_CLASSIFICATION` entry keyed by the final stripped text of the new `claim.md` Wave 2 line, category `read-only`, one-line reason.
- **Verifier:** `uv run pytest tests/skills/test_worker_contract.py -q` passes after Task 1.
- **Linked finding(s):** A1
- **Priority:** P0

### Recommendation R-002: Pin failure precedence
- **File:** src/superclaude/skills/sc-issue-protocol/refs/claim.md (Wave 2 item) and tests/skills/test_issue_protocol.py (Task 6)
- **Change:** state "a line matching `^#[0-9]+ https://` stops the claim; otherwise non-zero exit or non-matching output is could-not-run; otherwise none" and assert it.
- **Verifier:** the new Task 6 test passes; `gh api` of a missing issue in a read-only check yields "could not run" under the written rule.
- **Linked finding(s):** A2
- **Priority:** P0

### Recommendation R-003: Report the skipped check on a later STOP
- **File:** src/superclaude/skills/sc-issue-protocol/refs/claim.md
- **Change:** one sentence in Wave 2 and Final output that a later STOP prints the held line first; one Task 6 assertion.
- **Verifier:** the Task 6 helper reports a problem when the sentence is removed.
- **Linked finding(s):** A3
- **Priority:** P1

### Recommendation R-004: Pin the order against the assignee checks
- **File:** tests/skills/test_issue_protocol.py
- **Change:** extend the planned helper and add a mutation test that moves the blocker item between Wave 2 items 2 and 3.
- **Verifier:** the mutation test fails for the moved item and passes for the real file.
- **Linked finding(s):** A10
- **Priority:** P1

## Inferred-claim audit

- `citations_inferred: 1`
- Inferred-fraction: `1 / 62` = 0.02
