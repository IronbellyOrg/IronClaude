```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 1
confidence_calibrated: 0.85
citations_total: 24
citations_revalidated: 24
citations_dropped: 0
citations_inferred: 3
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 24` of 24, so the sample is the whole population.
> - `citations_dropped: 0`; `citations_dropped_extrapolated: 0`.
> - The extrapolated value is telemetry, not a verdict.

# Reflect pre-execution report: TASK-WF-implementGitHubI-20261119-133641

**Verdict: the plan covers every requirement of the live issue body (updated 2026-11-19T13:36:41Z), with 0 blocking findings, 3 Medium follow-ups and 2 Notes. The run is `partial` because the rubric requires Tier 2 and Tier 2 was not run.**

Spec: `.dev/tasks/to-do/TASK-WF-implementGitHubI-20261119-133641/source.md`. Tasklist: `.dev/tasks/to-do/TASK-WF-implementGitHubI-20261119-133641/TASK-WF-implementGitHubI-20261119-133641.md` (6 tasks, 2 phases, quick depth).

## Tier decision

- The spec carries no labeled requirement IDs, so Pass 1 found 0 and Pass 2 found 22 (Step 1B.2b parse-density guard: `coverage_degraded: parsed-sparse`). That guard forbids a Tier 1 stop, and rule 4 (three domains: script, tests, operations file) also escalates (`artifacts/tier_decision.yaml`).
- Tier 2 needs heterogeneous reviewer subagents. This session's launch rules forbid starting subagents, so Tier 2 did not run. What ran is Tier 1 by the orchestrator alone, with `calibration: inline-fallback` (a self-grade, weaker than the blind calibration the protocol wants) and no evidence-validator agent (all 24 citations were re-Read inline instead). Treat this verdict as a single-reader review.

## Coverage (union of parsed and inferred rows)

- Parsed rows: 0, so `coverage_pct: null` (parsed-only semantics) and `unmapped_requirements: []`.
- Inferred rows: 22. Mapped to a task or constraint: 22 of 22, so `coverage_pct_union: 1.0` and `unmapped_requirements_union: []`, `S_dev_density: 0.0`. [INFERRED] The match was a manual containment read, not the scripted 0.6 word-containment rule.
- One row (INF-020, finish with `/sc:pr-submit --monitor 3`) maps to a Constraints line, not a task, on purpose: the session owner runs it after `/sc:implement`.
- The six test cases the issue requires (human, bot from a person's branch, wholly by a bot, merged by someone else, no-merge repo, repo added later) are all named in the plan: no-merge repo and added repo in Task 1, the other four in Task 2.

| INF id | Plan location that covers it | Match |
|---|---|---|
| INF-001 | Constraints "Adapt, do not rewrite" (plan line 21); Tasks 1 to 4 | covered |
| INF-002 | Task 1 (`list_repos`) | covered |
| INF-003, INF-005 | Constraints "Credit rule" (plan line 25); Task 2; Task 3 | covered |
| INF-004 | Task 2 (no-person list); Task 3 ("No person" line) | covered |
| INF-006, INF-007 | Task 2 (`LOGIN_TO_PERSON`, unmapped login shown) | covered |
| INF-008 | Constraints (drop list); Task 3 acceptance (no issue section, calendar link or allowlist legend) | covered |
| INF-009 | Task 1 (`DIGEST_TZ`, `DIGEST_LOOKBACK_DAYS`); Task 2 (time-zone test) | covered |
| INF-010 | Tasks 3 and 4 (`index.html`, `digest.md`, PR links) | covered |
| INF-011 | Constraints "Independence"; Task 6 | covered |
| INF-012 | Constraints "Scope"; Task 6 | covered |
| INF-013 | Task 5 | covered |
| INF-014, INF-021 | Task 1 (`token`); Task 4 (variable check); Constraints "Secrets"; Task 6 | covered |
| INF-015 | Constraints "Scope" (three deliverables only) | covered |
| INF-016 | Task 4 (`publish_clickup`) | covered |
| INF-017 | Task 4 (`--dry-run`) | covered, see Note N-1 |
| INF-018 | Tasks 1 and 2 | covered |
| INF-019 | Task 5 (human steps) | covered |
| INF-020 | Constraints (plan line 29) | covered by a constraint |
| INF-022 | no task (GitHub Actions scheduling is out of scope) | correctly absent |

## Inferred requirements (Pass 2)

All citations are into `source.md` (the live body section). Every quote was re-Read against the cited line.

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | "by ADAPTING Jay Wedgeworth's existing generator" ... "Do not write a new one from scratch." | source.md:36 | matched (Constraints, Tasks 1-4) |
| INF-002 | "List every repo, public and private, fresh on each run so a new repo is included with no edit. Skip archived repos." | source.md:57 | matched (Task 1) |
| INF-003 | "Credit goes to the PERSON WHO MADE THE BRANCH AND SUBMITTED THE PR (Clay's ruling, 2026-11-19), not whoever merged it." | source.md:58 | matched (Constraints, Task 2) |
| INF-004 | "A PR made wholly by a bot with no person behind it (such as a dependency bump) is counted on its own "no person" line, never credited to anyone." | source.md:58 | matched (Tasks 2, 3) |
| INF-005 | "Show people by name, NEVER an agent or "Claude Code"" | source.md:58 | matched (Constraints, Task 3), see M-1 |
| INF-006 | "Login to person table: `clayphi` is Clay, `ironbelly` is Ryan, `IBC-ChrisG` is Chris, `IB-Lea` is Leandro, `swill-ib` is William." | source.md:59 | matched (Task 2) |
| INF-007 | "A login that is not in the table and is not a bot is shown as the login." | source.md:59 | matched (Task 2) |
| INF-008 | "Drop: issues, the calendar feed, the public allowlist, reading the agent from PR titles." | source.md:60 | matched (Constraints, Task 3) |
| INF-009 | "day buckets in a fixed time zone (default America/Chicago, its own setting), a 21-day lookback" | source.md:54 | matched (Tasks 1, 2) |
| INF-010 | "a web page and a markdown digest, and a link to every PR." | source.md:54 | matched (Tasks 3, 4) |
| INF-011 | "It must not import from, read the config of, or be installed through either, and it must not live in IronFlow." | source.md:63 | matched (Constraints, Task 6) |
| INF-012 | "It belongs in IronClaude but must be OPT-IN." | source.md:64 | matched (Constraints, Task 6) |
| INF-013 | "Write the definition for Clay to switch on; do not switch it on. The automation name must NOT start with `coordinator-`" | source.md:65 | matched (Task 5) |
| INF-014 | "the script refuses to run without it instead of falling back to `gh`'s stored login" | source.md:66 | matched (Tasks 1, 4) |
| INF-015 | "A single script plus tests is the target. Do not plan more than the work needs." | source.md:67 | matched (Constraints) |
| INF-016 | "a ClickUp Doc whose page is rewritten in place by the script (`PUT /v3/workspaces/{workspace_id}/docs/{doc_id}/pages/{page_id}`, replace mode)" | source.md:75 | matched (Task 4) |
| INF-017 | "Settle it with a dry run that prints `gh api rate_limit` before and after." | source.md:81 | matched (Task 4), see N-1 |
| INF-018 | "Tests use recorded GitHub responses and cover: a human author, a bot opening a PR from a person's branch, a PR made wholly by a bot, a PR merged by someone other than its author, a repo with no merges, and a repo added after the first run." | source.md:93 | matched (Tasks 1, 2), see M-2 |
| INF-019 | "Human steps are listed, including creating the ClickUp Doc (a human step) and switching on the Orca automation." | source.md:94 | matched (Task 5) |
| INF-020 | "Finished with `/sc:pr-submit --monitor 3`." | source.md:95 | matched (Constraints, plan line 29) |
| INF-021 | "Credentials are read only from the environment, no secret value appears in any file, and the script fails clearly when a variable is missing." | source.md:91 | matched (Tasks 1, 4, 6) |
| INF-022 | "GitHub Actions scheduling." (Out of Scope) | source.md:99 | matched (no task, correctly absent) |

Postscript: 0 INF rows dropped by the citation re-Read.

## Findings

No Blocking finding: nothing named by a decision, a required deliverable or a safety boundary is wrong or missing. Verdict for the plan: PASS with notes (the run status is `partial` only because Tier 2 did not run). The five findings below are recorded as follow-up candidates and never edit the plan.

### M-1 (Medium): PR titles are shown as written, which may show an agent name

- **Location:** plan line 25 (Constraints, "PR titles are PR text and are shown as written") against source.md:87 ("No agent name or "Claude Code" appears anywhere.").
- **Evidence:** the plan limits the "never an agent" rule to credit, columns, legends and labels. The acceptance criterion says "anywhere". Jay's generator strips agent tags from titles; the issue only says to drop "reading the agent from PR titles" (source.md:60), which does not say to strip them.
- **Consequence:** a merged PR whose title carries an agent tag (for example a bracketed tool name) shows that text in the digest, and Clay may read the criterion as broken.
- **Classification rationale:** a real weakness with nothing named resting on it, so Medium, not Blocking. [INFERRED] Clay may intend the literal reading; the issue does not say.

### M-2 (Medium): fixtures are hand-written, the criterion says "recorded"

- **Location:** plan line 27 against source.md:93 ("Tests use recorded GitHub responses").
- **Evidence:** the plan says to write fixtures by hand unless an authorized capture already exists and to say so in the test module docstring. It is disclosed, but it is not literally what the criterion asks for. The credit-rule fixtures (bot-opened PRs, commit lists) are the ones where real response shape matters most.
- **Consequence:** a reviewer applying the criterion literally may reject hand-written fixtures, and a wrong guess about a response field (for example `user.type` or a null commit `author`) would pass the tests and fail on live data.

### M-3 (Medium): ClickUp page size is unconfirmed and a failed run is not announced

- **Location:** plan line 81 (Task 4: any error ends the run non-zero and the old page stays) with hosting research line 32 and source.md:65.
- **Evidence:** the research states the maximum size of a Doc page "not confirmed" (hosting research line 32). The automation name must not start with `coordinator-` (source.md:65), so a failed run does not appear in the daily work report either. [INFERRED] The generation time in the page header would show staleness, but nothing alerts anyone.
- **Consequence:** if a 21-day digest across both orgs exceeds ClickUp's limit, every scheduled run fails silently and the Doc quietly goes stale.

### N-1 (Note): the dry run does not "settle the search limit"

- **Location:** plan line 81 ("which settles the open question about the search limit") against source.md:81.
- **Evidence:** the planned script reads pull requests through the REST `pulls` endpoint, not `gh pr list --search`, so it never calls the search API. The dry run still proves the request budget (core and graphql counts) but does not test the search budget.
- **Consequence:** wording only; the dry-run output is still the right check.

### N-2 (Note): one Task 6 criterion cannot be checked mechanically

- **Location:** plan line 117 ("no occurrence of an agent name as a credit").
- **Evidence:** "as a credit" has no test form beyond what Tasks 2 and 3 already check (credited names come only from the table or a login).
- **Consequence:** wording only; Tasks 2 and 3 already carry the real checks.

## Inferred-claim audit

- `citations_inferred: 3`
- Inferred-fraction: `3 / 24` = 0.13

## Recommendations

### Recommendation R-001: Ask Clay one question about titles, then record the answer in the PR body

- **File:** `scripts/merged_pr_log.py` (title rendering in `build_markdown` and `build_html`, Task 3)
- **Change:** Ask Clay whether a PR title that contains an agent name should be shown as written (current plan, recommended: it is the real PR text) or have the agent name removed. Put the answer in the PR description.
- **Verifier:** the Task 3 test renders a fixture title containing "Claude Code" and asserts the behavior Clay chose.
- **Linked deviation(s):** M-1
- **Priority:** P1

### Recommendation R-002: Prefer captured responses for the credit-rule fixtures when a token is available

- **File:** `tests/merged_pr_log/fixtures/`
- **Change:** if the implementing session already has an authorized read token in its environment, capture trimmed real `pulls` and `commits` responses for the bot-opened cases; otherwise keep the hand-written shape and say so in the PR body.
- **Verifier:** the test module docstring states which fixtures are captured and which are hand-written.
- **Linked deviation(s):** M-2
- **Priority:** P2

### Recommendation R-003: Add a size check and a staleness note to the human steps

- **File:** `scripts/merged_pr_log_orca_automation.md` (Task 5 human steps)
- **Change:** add two steps: after the first `--dry-run`, compare the size of `digest.md` with what the ClickUp page accepts; and tell the team that the "generated at" line in the page header is the only sign of a failed run.
- **Verifier:** both steps appear in the human-steps list of that file.
- **Linked deviation(s):** M-3
- **Priority:** P2

### Recommendation R-004: Reword two plan sentences (optional)

- **File:** the plan, Task 4 last sentence (line 81) and Task 6 third acceptance criterion (line 117)
- **Change:** say the dry run shows request-budget headroom rather than "settles the search limit", and drop "as a credit" from the Task 6 criterion.
- **Verifier:** re-Read both lines.
- **Linked deviation(s):** N-1, N-2
- **Priority:** P2

Reflect never edits the plan; these are for the person or session that runs `/sc:implement`.

## Not run

- Tier 2 reviewers and the adversarial merge: not run (session rule against subagents). `adversarial_unavailable` is `false` because the Wave 5 probe was never needed; `merge_method` does not apply.
- Independent evidence-validator and confidence-calibrator agents: not run; inline re-Read and inline self-grade instead.
- Verification run, reachability gate and promotion: not applicable to a pre-execution pass.
