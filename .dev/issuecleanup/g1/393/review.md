# Independent evidence review

Template: ../362/report-template.md, Independent review template.

## Verdict
**PASS.** The two reports are supported by the source they cite, and the verdict, priority and recommendation follow from that source. I found no blocking defects.

## Scope checked
I read both reports in full, each under 80 lines. I read the cited source for every claim that can be checked locally:

- `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/refs/retry.md`, lines 55-80 and 155-194.
- `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/refs/ledger.md`, lines 90-115.
- `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/ccsession-tag/ccsession`, lines 1100-1124.
- `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/implement-retry-adviser.md`, lines 1-12.
- The three cited test files: `test_model_alias_policy.py`, `test_workflow_archive.py` and `test_implement_adviser_family.py`.
- The plugin mirror `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/plugins/superclaude/skills/sc-implement-protocol/refs/retry.md`. A grep found the same markers at lines 162, 172 and 183. I did not diff the full range 162-185 line by line.
- The required fields in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/362/report-template.md`.

Checks and results:

- **Primary ladder.** `retry.md:162` says the primary ladder is active only when the four rung variables (`T2bModel01`, `T2Model02`, `T1Model02`, `T1Model01`) are all set and non-empty. Otherwise the fallback ladder (`haiku`, `sonnet`, `opus`) applies. The claim that no spawn-capability check is stated also holds.
- **Selection versus launch alias.** Retry.md `185` says "The model tier comes from the Agent call's `model` parameter". The primary rungs are env-variable values, and the fallback rungs are aliases. The reports' distinction between selecting a rung and launching an alias is therefore grounded. The ledger `tier=` field records the executor's rung, not an adviser launch argument (`ledger.md:94,108,112`).
- **Launcher aliases.** `ccsession:1115-1117` exports `claude-gw-tier1a[1m]`, `claude-gw-tier1b[1m]` and `claude-gw-tier2[1m]` for the OPUS, SONNET and HAIKU defaults. Each export is conditional on that tier being usable, and only in tier mode. The reports' "access-aware" wording matches this.
- **Fallback scope.** The family-fallback sentence at `retry.md:181` is specified only for adviser B. The sentence "GPT spawn path: none verified; family-fallback applies" is at line 183. Critique uses adviser A's model (line 170). Escalation 2 uses two top-rung advisers (line 172). The line 169 rule that a GPT executor gets a GPT T1 adviser A has no stated fallback. The reports' "partial mitigation for B only" is accurate, and they correctly avoid claiming a universal failure.
- **Adviser agent.** `implement-retry-adviser.md:1-6` has `tools: Read, Grep, Glob` and `effort: high`, with no `model:` field.
- **Test coverage.**
  - `test_model_alias_policy.py:217-228` checks that no `T[0-4]_Model` spellings appear and that the four names are present.
  - `test_workflow_archive.py:798-830` checks that the regex accepts every rung token.
  - `test_implement_adviser_family.py:14-85` uses local reference functions and pins the GPT spawn-path line. Its line 14 comment reads "no GPT alias, no full-id path".
  - None of these calls Agent or validates launch arguments. The reports' "not the requested launch proof" claim is correct.
- **Required fields.** The findings report has all nine required sections. The analysis report has all five. Both give a verdict or severity, evidence, and a recommendation.

## Blocking findings
None.

The verdict "still-relevant", priority P2, size S and the recommendations (keep open, explicit alias rule per role, broader tests, a controlled launch before any fidelity claim) have concrete support in the cited prose. Neither report asserts a runtime crash. Both say runtime behavior is UNVERIFIED and that only the missing explicit mapping is shown statically.

## Follow-up candidates and notes
1. **Agent schema claim.** The claim that the Agent `model` argument accepts only `opus`, `sonnet`, `haiku` and `fable` rests on the authoring session's tool schema. It is not a source citation and I cannot probe it. Both reports label it as observed from "this session" and not a runtime probe, which is adequate. Analysis finding 1 states "cannot carry its arbitrary model IDs" more firmly than that provenance supports. Read it as "per this session's schema, not verified for a real retry run".
2. **GitHub facts I could not verify from files.** I did not check these, and I draw no conclusions from them:
   - PR merge SHAs and dates for #385, #391 and #518.
   - Issue dates, and the contents of #384, #488, #571, #572 and #392.
   - The statement that no blocked-by or blocking issues exist.
   - The statement that the last five commits on retry.md end at #518.
   - The claim that #391's probe did not exercise the Agent-call model parameter.
   - The claim that the original issue used `T3Model01`.

   These come from the authors' own observations. The reports mark the full timeline UNVERIFIED and #392's status UNVERIFIED, and they flag that no open PR search is proof of absence. The authors correctly decline to conclude beyond that.
3. **Priority rationale.** P2 is reasonable. Its "does not block #571" and "correct before #572 evaluation" statements are judgment calls built on the unverified issue bodies, not on checked evidence.
4. **Wording slip.** The findings report says the mismatch "can prevent the intended stronger or independent advice". That is a plausible static inference, and the reports elsewhere avoid asserting runtime effects.
5. **Analysis report scope.** The analysis report says it covered only the model-selection parts of retry.md and ledger.md. That scope is stated and acceptable.
6. **Related-issue claims.** The "related issues" and "related PRs" descriptions rest only on the authors' reading of `gh` output. The reports carry the right caveat that the search was incomplete.
