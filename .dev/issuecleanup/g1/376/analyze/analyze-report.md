# Cross-Validation Report

- **Date:** 2026-11-23
- **Claims verified:** 3 verified; 1 closure check unverified.
- **Scope:** Architecture, quick depth, adversarial scoring protocol, checkout HEAD a7ae3dd30fcf88aaab655c37e94e58e121c2d863.
- **Template:** /home/coder/.claude/templates/modularization-template-review/analyst-cross-validation_report_template.md, extended with the analyze command's required assessment sections.
- Codegraph: index_state=fresh, checked_at=2026-11-23T23:05:09Z; degraded: graph:empty. Access=mcp. Markdown is not indexed; the scoped layout returned only the empty Python initializer, so protocol analysis used the required Glob/Grep/Read floor. Pending sync concerned other workers' report contracts, not this target.

## Validation Results

| # | Claim | Source | Code Path Checked | Verdict | Notes |
|---|-------|--------|-------------------|---------|-------|
| 1 | Both evaluation passes still request 25 criteria. | Issue 376 and its 2026-11-17 comment | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-adversarial-protocol/SKILL.md:1743-1776 | VERIFIED | The formula divides by 30, but lines 1756 and 1759 request 25 criteria. Reconciliation is per evaluated criterion, so the omitted five need not reach the disagreement log. |
| 2 | The base-selection template has only five dimensions, divides by 25 and lacks the invariant eligibility check. | Issue 376 | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:167-234 | VERIFIED | Five dimension sections and five summary rows; line 201 divides by 25; the remainder goes directly through comparison, totals and base selection with no eligibility section. |
| 3 | The scoring output contract requires six dimensions, 30 verdicts and per-variant floor eligibility. | Issue 376 | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-adversarial-protocol/refs/scoring-protocol.md:221-233 | VERIFIED | The referenced output requirements explicitly require the information missing from the template. |
| 4 | A dedicated scoring-consistency regression test already enforces the issue's acceptance criteria. | Closure check, not a claim made by the issue | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests | UNVERIFIED | Targeted searches for qual_score, total_criteria_met, scoring-protocol, 25-criterion and edge-case-floor terms found installer packaging or unrelated tests, not a scoring validator or the requested fixtures. This is bounded negative evidence, not proof that no differently named check exists. |

## Severity-rated findings

1. **High, selection correctness:** Competing definitions of the scoring record remain on the active base-selection path. Validation rows 1-3 show the canonical 30-item output and two 25-item evaluation prompts feeding a five-dimension template. A candidate with 25 original criteria met and zero invariant criteria met scores 25/30 under the intended rule but 25/25 in the stale template, potentially changing which candidate becomes the merge base. This is static arithmetic, not an observed model outcome.
2. **Medium, duplicated protocol drift:** The separate debate summary also requests 25 criteria at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md:192. Updating only the two pass prompts and the template leaves an active stale consumer. Criterion identities, dimension counts, totals and eligibility need an agreement check, not just a global text replacement.

## Code quality metrics

- Target inventory: five Markdown files and one empty Python initializer. Four Markdown files contain the scoring contract, passes, summary and template; the remaining reference describes agents.
- Stale criterion count: three active `25-criterion` instructions in two files.
- Stale denominator: one template row containing two `/25` cells.
- Required dimensions/criteria: six/five per dimension, totaling 30. Template summary: five dimensions, totaling 25.
- Targeted test search found packaging, worker-contract and lookup checks, but did not locate the requested score/floor/criterion-completeness regressions. No test suite was run in this static analysis.

## Security vulnerabilities

No security vulnerability was established by this scoped scoring-contract inspection. This was not a security audit, and no broader safety guarantee is implied.

## Performance issues

No measured performance finding. No debate, model call, build or benchmark was run; two-pass evaluation cost and runtime are UNVERIFIED.

## Recommendations

1. Keep the six-dimension, 30-criterion design. Align both pass prompts and the debate summary; add the sixth evidence table, subtotal, `/30` total and per-variant eligibility/suspension record to the base-selection template.
2. Give the canonical criteria stable unique identities and check that both passes, reconciliation and the report cover the same complete set. Validate subtotals and normalized totals; reject missing/duplicate criteria and incorrect denominators instead of inferring a pass.
3. Add deterministic acceptance fixtures: 30 met, zero met, 25 met plus five invariant failures with an eligible competitor, all-zero invariant suspension, incomplete/duplicate records, wrong subtotal/denominator and invariant disagreement reconciliation. Preserve the current all-zero warning policy.
4. Inspect distribution and evaluation consumers, then use the repository's normal source-to-development-copy sync after an authorized fix. Do not edit or stage generated command/skill mirrors as source.
5. Run one separately authorized debate after the checks pass and keep its fixture, source revision, generated record and eligibility result. This task authorizes analysis only, not that run.

## Verification limits

- Inspection establishes contradictory instructions, not a reproduced production selection failure.
- No source edits, test execution, live debate, new dependency or outward GitHub action occurred.
- Graph lookup yielded no usable Markdown symbols; this is not evidence of missing callers. The scoped directory and textual source/test searches are the evidence.
- The issue's complete event timeline is UNVERIFIED: the allowed `gh issue view/list` and `gh pr view/list` interfaces expose body, comments, state, closure and selected relationships but no complete timeline field. No API or browser route was used because the brief forbids it.
- Initial combined `gh issue view --comments --json` failed because these flags are mutually exclusive; the successful retry requested the JSON comments field. The missing project-local analyze command copy was skipped under the brief guard; the installed copy contains the unattended section.
