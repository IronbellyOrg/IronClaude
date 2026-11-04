# Refactoring Plan: Merge into Base (Variant 1)

## Overview
- Base variant: Variant 1 (reviewer-1, sonnet:analyzer), `adversarial/variant-1-original.md` (selected in `base-selection.md`, score 0.7550).
- Incorporated variants: Variant 2 (reviewer-2, haiku->glm-5.3:qa) and Variant 3 (reviewer-3, opus:refactorer); the shared-assumption points A-002..A-007 of `diff-analysis.md`; the Round 2.5 invariant probe (`invariant-probe.md`).
- Output: `../merged-verdict.yaml` (the `adversarial/` folder of the reflect run), schema as round 1's merged verdict: `merge_method`, `verdict`, `convergence_score`, `convergence_status`, `base_variant`, `source_cards`, `citation_legend`, `round1_fix_check`, `findings` (8 keys each: `id`, `severity`, `category`, `claim`, `evidence`, `recommendation`, `source_cards`, `debate_ruling`), `authorized_expansions`, `notes`, `rejected_findings`, `unresolved`, `unaddressed_invariants`, `severity_rule`.
- Planned changes: see below. Overall risk: Low (the debate converged on every point; the merge regrades and combines findings, it does not invent new ones beyond the probe's).
- Drafted by the orchestrator (debate-orchestrator role) on resume; reviewed by an independent analytical agent (Review Status).

## Citation rules for the merge
- `plan:N` = line N of `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md`; `source.md:N` = line N of `source.md` in the same folder; other paths are repo-relative.
- Every evidence entry below was taken from the Round 2 position tables (`.work/round2-v{1,2,3}.md`), `.work/evidence-sheet.md` or the probe, and its line was re-read in this pipeline. The merge executor copies evidence lists exactly; it adds none.
- Severity rule (binding): blocking only for wrong behaviour, a false claim, a missing required deliverable, or a security/data-loss risk. Everything else is minor.

## Planned Changes

### Change 1: Restructure the base card into the merged-verdict schema
- Source: base top-level keys. Target: `merged-verdict.yaml` top level.
- Approach: restructure. `verdict: PASS` (with notes; X-001), `merge_method: adversarial`, `convergence_score` and `convergence_status` from `debate-transcript.md` "Convergence Assessment", `base_variant: "variant-1 (reviewer-1, sonnet:analyzer)"`, `source_cards: [reviewer-1, reviewer-2, reviewer-3]`. Keep `round1_fix_check: {F-01: fixed, F-02: fixed}` from the base. Drop `self_reported_confidence` and `self_audit`.
- Rationale: X-001 unanimous in Round 2 (round2-v1.md:101, round2-v2.md:111, round2-v3.md:136). Risk: Low.

### Change 2: F-01 (minor, top priority): Task 17 item 4 runs a live claim exempted from approval by intent (base A-1, regraded; + A-005)
- Source: base A-1; V1/V2/V3 Round 2 fix; diff point A-005; V3 refactorer additions (round2-v3.md:63-74). Approach: modify.
- Claim: plan:26 exempts the item-4 run from approval because it "stops before any GitHub or ClickUp write", which is the behaviour under test; plan:254 runs `/sc:issue --claim https://github.com/octocat/Hello-World/issues/1` live; the URL-vs-origin comparison has no deterministic test (Task 1 tests parsing only), so plan:259 is hoped for, not guaranteed. An escape needs a Wave 0 fault plus a missed Wave 2 inference and lands reversibly on the user's own fork (origin #1 is a merged pull request), so it is minor under the binding rule.
- Evidence: plan:26, plan:254, plan:259, plan:32-38, plan:111, plan:116, source.md:142-143, source.md:151, source.md:155, source.md:159, source.md:162, source.md:336, source.md:361, source.md:470, `.work/evidence-sheet.md` E4 and E6.
- Recommendation: (1) item 4 uses a foreign URL whose repo and issue number cannot exist on origin and that has no digits outside the `/issues/<N>` segment, e.g. `https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999` (AC 4 needs only "any repo other than origin"); the debate's example `.../issue302-no-such-repo/...` is NOT used, because its `302` is the real origin issue (INV-001); (2) add a pure URL-vs-origin check (or `--check-url` mode) to `origin_repo.py` that prints `E-FOREIGN-REPO` with an exit code distinct from `E-NO-ORIGIN`, pinned in Task 1 by tests for a same-repo URL, a foreign owner, the same owner with a different repo, a repo-name prefix (`IronClaude` vs `IronClaudeX`), a `/pull/<N>` URL, fragment and trailing `/`, and digits in the owner or repo name never becoming N (INV-001, INV-002); require in Task 6 (text and AC) that Wave 0 calls it; record it as a disclosed addition justified by source.md:361; (3) rewrite plan:26's carve-out by target ("a run whose URL names a repository and issue that do not exist may run without asking"); (4) split Task 17's item-4 row: clause 1 (E-FOREIGN-REPO) from the real run; clause 2 ("no `gh` call is made without `--repo <origin repo>`") points at the Task 7 fork-safety test and the F-10 `repos/<R>/` assertion and notes that `gh auth status` and `gh api` carry no `--repo` flag (INV-003); (5) fallback: if (1) and (2) are not applied, item 4 stays pending.
- Evidence additions from the probe: source.md:66, source.md:144, source.md:148, source.md:178, plan:32, plan:258 (INV-001, INV-002, INV-003).
- Debate ruling: C-001 minor, unanimous after Round 2 (V3 conceded from blocking, round2-v3.md:3); winner V1, 95%. A-005 minor, unanimous (new). The minor grade holds only with a URL that has no stray digits (INV-001, INV-012).
- Risk: Low.

### Change 3: F-02 (minor): Task 15 offers two exits for a stale session (base A-2 + V3 S-2, regraded)
- Approach: merge. Evidence: plan:233, plan:236, src/superclaude/skills/sc-implement-protocol/SKILL.md:108-115, src/superclaude/skills/sc-implement-protocol/refs/ledger.md:155, src/superclaude/skills/sc-implement-protocol/refs/ledger.md:161.
- Claim: plan:233 says "stop here and ask the user to start a new session ... it resumes at this task" while plan:236 accepts a pending row; resume does work (a stop before review leaves only a start line, and Row S re-runs the task), so the defect is the choice of exit, not impossibility.
- Recommendation: state one exit, and make it pending: the executor may not stop to ask the user (src/superclaude/skills/sc-implement-protocol/refs/qa.md:288; its allowed-tools at SKILL.md:4 have no AskUserQuestion), and the session that ran Tasks 1-14 always started before Task 13, so on the first pass Task 15 writes a pending row with the reason. End Task 17's artifact with a short post-restart runbook in source order (export the ClickUp variables, start a new session, run Task 15's spawns, Task 16, item 4) so the scheduled checks are not dropped (INV-005). Remove "it resumes at this task". Keep "after Task 13" (it is the agent-load condition, not the dependency).
- Evidence addition: src/superclaude/skills/sc-implement-protocol/SKILL.md:4, src/superclaude/skills/sc-implement-protocol/SKILL.md:97, src/superclaude/skills/sc-implement-protocol/refs/qa.md:288.
- Debate ruling: C-002 and X-002 minor, unanimous; V3 withdrew "resume cannot work" (round2-v3.md:24-25). Winner V1, 95%. The debate's "stop and ask the user to restart" exit is replaced by pending per INV-005.

### Change 4: F-03 (minor): Task 6's mandated error-table rows trip Task 7's fork-safety scan (V3 S-1 + base A-5)
- Approach: merge. Evidence: plan:111, plan:131, plan:136, source.md:336, source.md:340.
- Recommendation: define the scan once and use it in both Task 3's test (plan:58) and Task 7's test (plan:131): every code span or fenced line that starts with `gh issue|pr|label` carries `--repo`, prohibitions included. Tasks 3, 5 and 6 then write every such mention with `--repo <R>`: the section-14 table cells (source.md:336, :340), the orchestrator write list (source.md:320) and the workers' "never run ..." prohibition (plan:56). They write the placeholder rule of source.md:319 without the literal token (for example "never a brace placeholder"), so plan:131's ban holds (INV-004).
- Evidence addition: plan:56, plan:58, source.md:319, source.md:320.
- Debate ruling: C-003 minor; V1 handed the better instance to V3 (round2-v1.md:26); winner V3, 95%.

### Change 5: F-04 (minor): Task 16 live comparison has no method or safe presence check (base A-3 + V3 S-6)
- Approach: merge. Evidence: plan:23, plan:243, plan:246.
- Recommendation: name one key-paths-only method (or accept the two status results as the shape check); ban `curl -v/-i/--trace` and header-printing options; check presence with `test -n "${CLICKUP_API_TOKEN:-}"`; accept `already_assigned` on the first run with a note.
- Debate ruling: C-004 minor, unanimous; winner V1, 90%.

### Change 6: F-05 (minor): ClickUp environment hygiene (base A-4 + V3 S-4)
- Approach: merge. Evidence: plan:23, plan:43, plan:45, plan:50.
- Recommendation: every test clears all four `CLICKUP_*` variables; plan:23 says "no command that prints it; `env -u` to unset it is allowed".
- Debate ruling: C-005 minor, unanimous; V3 handed it to V1 (round2-v3.md:106); winner V1, 90%.

### Change 7: F-06 (minor): "approval at that moment" has no trigger (V2 Q-4)
- Approach: insert. Evidence: plan:15, plan:26, plan:254, src/superclaude/skills/sc-implement-protocol/refs/qa.md:274, src/superclaude/skills/sc-implement-protocol/refs/qa.md:288.
- Recommendation: the executor cannot prompt (refs/qa.md:288; SKILL.md:4), so the debate's "add one explicit ask" is not available inside `/sc:implement` (INV-005). Instead: items 1, 2, 3, 6 and 8 are recorded pending, and Task 17's artifact ends with the explicit request to the user, in the runbook of F-02, to pre-approve one scratch test issue so those items can be run by hand; plan:26's "approval at that moment" is reworded to "only in a later, user-started session with the user's explicit approval".
- Evidence addition: src/superclaude/skills/sc-implement-protocol/SKILL.md:4.
- Debate ruling: C-006 minor; winner V2, 90%; mechanism amended by INV-005.

### Change 8: F-07 (minor): Task 17 dependency metadata (V3 S-3)
- Evidence: plan:252, plan:254. Recommendation: "Depends on: Task 14, Task 15, Task 16". Debate ruling: C-007 minor; winner V3, 90%. Metadata only for this executor (src/superclaude/skills/sc-implement-protocol/SKILL.md:79, :97).

### Change 9: F-08 (minor): AC 5's first half is unplaced (A-002)
- Evidence: source.md:471, plan:50, plan:254. Recommendation: name it in the Task 17 record as pending (it needs a live claim); do not mark it run on Task 2's script-only `no_token` output. Ruling: minor, unanimous (new).

### Change 10: F-09 (minor): AC 8's `/model` first line is unasserted (A-003)
- Evidence: source.md:474, plan:77, plan:81-85, plan:123-132. Recommendation: add a Task 4 AC (or Task 7 test) that `templates/next-steps.md` starts with the `/model` tier line; in Task 17, describe this static check as covering the template and default rows only and keep item 8 pending until a live claim, because `/sc:recommend` output can carry other flags (source.md:438; INV-011). Ruling: minor, unanimous (new).

### Change 11: F-10 (minor): no check that `gh api` paths spell `repos/<R>/` (A-004)
- Evidence: source.md:319, plan:131. Recommendation: extend Task 7's fork-safety test: every `gh api` path in the skill and agents starts with `repos/<R>/`. Ruling: minor, unanimous (new).

### Change 12: F-11 (minor): Task 16's PUT target is chosen by a workspace-wide match, not the named task (A-006)
- Evidence: plan:243, plan:246, source.md:298, source.md:304-309. Recommendation: Task 16 runs only when the user has, before the session, exported `CLICKUP_LIST_IDS` set to the test task's list (narrowing the search before the PUT; INV-007) and supplied the test issue URL and task ID up front (the executor cannot ask mid-run, INV-005); otherwise it is pending. After the first run compare the reported `task_id` with the named one; on a mismatch make no second run, record the wrong `task_id`, and tell the user to remove the assignment. Ruling: minor; winner V2, 90%; amended by INV-005 and INV-007.

### Change 13: F-12 (minor): Task 17 item 4 needs a post-Task-13 session with no check (A-007)
- Evidence: plan:233, plan:254, plan:258. Recommendation: state the same session precondition as Task 15; on the first pass item 4 is pending and goes into the F-02 runbook (INV-005); a read-through or simulated run is not evidence, and the item-4 row quotes the real output when it is run. Ruling: minor, unanimous after V2 changed (round2-v2.md:72).

### Change 14: F-13 (minor): invalid `CLICKUP_MAX_PAGES` behaviour is unbounded (base A-6)
- Evidence: plan:43, source.md:310. Recommendation: fix the rule: fall back to 20 (or print an error status) and exit 0, since exit 2 is reserved for bad arguments. Ruling: V1 Round 1 kept it as low-value minor (round1-v1.md:77).

### Change 15: F-14 (minor): copying evidence-validator.md frontmatter carries `permissionMode: plan` (V3 S-5)
- Evidence: plan:56, src/superclaude/agents/evidence-validator.md:8. Recommendation: Task 3 sets no `permissionMode: plan`, and its test asserts that. Ruling: verified by V1 and V3 Round 1 (round1-v1.md:21, round1-v3.md:13).

### Change 16: F-15 (minor): served-model evidence may name a tier member, not the picker ID (V3 S-7)
- Evidence: plan:233, plan:236, src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:17-21. Recommendation: accept the picker ID or a model from that tier's mapping as "served", and name where the evidence is read. Ruling: verified by V1 and V3 Round 1 (round1-v1.md:22, round1-v3.md:14). Tagged [INFERRED] in the card for the transcript side.

### Change 17: F-16 (minor): Task 7's inventory "every file in refs/, templates/, scripts/" includes `__pycache__` (V3 S-8)
- Evidence: plan:125, plan:132. Recommendation: limit the inventory to `refs/*.md`, `templates/*.md`, `scripts/*.py`. Ruling: minor (round1-v3.md:18).

### Change 18: F-17 (minor): the D26 sentence has no fixed wording (V3 S-10)
- Evidence: plan:111, plan:146. Recommendation: state the exact sentence once in Task 6 and reference it from Task 8 and its test. Ruling: minor (round1-v3.md:18).

### Change 19: authorized_expansions and notes
- `authorized_expansions`: Q-2 `--limit 200` on the merged-PR query (plan:92, plan:105) and Q-3 source-only flag check (plan:129): round-1-directed, disclosed; no action (round2-v2.md:17-19).
- `notes`: S-9 interim red tests between Tasks 1/8 and Task 9 are `unrelated-red` and change no verdict (src/superclaude/skills/sc-implement-protocol/SKILL.md:152-154); S-12 heading backticks at plan:197 vs docs/user-guide/commands.md:236 (style).

### Change 20: rejected_findings
- S-001, S-002 (format only; verdict basis settled by X-001), A-001 (source.md:391 defines the static test as phrase presence; plan:126 matches), A-008 (pytest is a main dependency, pyproject.toml:34-43), Q-1 (duplicates plan:25), S-11 (withdrawn by V3, round2-v3.md:15-16).

### Change 21: invariant-probe amendments (filled after Round 2.5)
- INV-001 (HIGH) and INV-002, INV-003 (MEDIUM): folded into F-01 (Change 2).
- INV-004 (MEDIUM): folded into F-03 (Change 4).
- INV-005 (MEDIUM): folded into F-02 (Change 3), F-06 (Change 7), F-11 (Change 12) and F-12 (Change 13): the item-4 run is pending on the first pass and goes into the runbook.
- INV-006 (MEDIUM): new finding F-18 (Change 23).
- INV-007 (MEDIUM): folded into F-11 (Change 12).
- INV-008 (MEDIUM): satisfied by Changes 14-18, which carry A-6, S-5, S-7, S-8 and S-10 as explicit minor findings; F-14 (S-5) matters most among them because a copied `permissionMode: plan` would make every worker spawn fail (source.md:335).
- INV-011 (LOW): folded into F-09 (Change 10).
- INV-009, INV-010, INV-012 (ADDRESSED): no change.
- `unaddressed_invariants: [INV-001]` (the only HIGH UNADDRESSED item); `convergence_status: BLOCKED_BY_INVARIANTS`; the adversarial return contract status is `partial`.

### Change 23: F-18 (minor): Wave 2 cannot see that a number is a pull request (INV-006)
- Source: invariant probe INV-006 (no card raised it). Approach: insert.
- Claim: Wave 2 decides from scout.md alone (source.md:154); the scout claim section the plan defines (plan:78) has no `url` or pull-request field although Wave 1 fetches `url` (source.md:148); an open pull request reports `OPEN`, so a user who types an open PR number reaches the assign and two comments (source.md:162, :178-179) without any fault. `E-NOT-AN-ISSUE` (source.md:159) is only checked for presence (plan:116).
- Evidence: plan:78, plan:116, source.md:148, source.md:154, source.md:159, source.md:162.
- Recommendation: Task 4 adds `url` and `is_pull_request` (true when `url` contains `/pull/`) to the scout claim section, with an AC; Task 5's claim.md makes the Wave 2 STOP read that field. Record it as a disclosed addition (the same kind as the "whether that list was truncated" field at plan:78).
- Severity: minor (no deliverable is missing and no plan statement is false; plan:92 already requires the pull-request STOP), but fix before any live claim.

### Change 22: provenance and severity rule
- Header comment block naming base, sources, merge date; `severity_rule` copied from the binding rule above.

## Changes NOT Being Made (with rationale)
- V3's blocking grades on S-1 and S-2 and V1's blocking grade on A-1: all conceded to minor under the binding rule (round2-v1.md:13, round2-v3.md:3, :12, :25).
- V1's original A-1 URL `.../issue302-no-such-repo/issues/1`: replaced by the non-existent issue number, because with only the repo changed an escaped run still targets origin #1 (reviewer-1-calibration.yaml; round2-v1.md:21-24).
- S-11 per-task lint: withdrawn; Q6 extras already run `make lint` (src/superclaude/skills/sc-implement-protocol/SKILL.md:132, :146).

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 | Low | schema only | regenerate from base |
| 2-18 | Low | regrade/merge of debated findings | drop the finding entry |
| 19-20 | Low | classification only | move entry back to findings |
| 21 | Low-Medium | depends on probe output | revert to Round 2 recommendations |

## Change 24: reviewer amendments (binding on the merge; they override the text of the changes they name)
From `.work/refactor-plan-review.md` (VERDICT: APPROVE, 8 minor changes, no blocking finding):
1. F-10 (Change 11): the assertion becomes "every `gh api` path in the skill and agents other than `user` (the login lookup of source.md:148) starts with `repos/<R>/`; none uses the brace placeholder". Add `source.md:148` and `plan:92` to F-10's evidence.
2. Change 20: add to `rejected_findings`: "U-019 (V1 A-1: read the implemented SKILL.md before the live run): superseded by F-01 (2), a tested URL check that Wave 0 must call, pinned by a Task 6 AC, and by F-12 (a read-through is not evidence)". Evidence: diff-analysis.md:63.
3. F-01 (Change 2) part (5) reads "fallback: if (1) and (2) are not applied, item 4 stays pending (INV-005: the executor cannot ask for approval, refs/qa.md:288, SKILL.md:4; the debate's 'else approval' is replaced)"; the debate ruling line adds "; fallback amended by INV-005".
4. F-11 (Change 12) adds: "Remove plan:243's 'Ask the user only for the test issue URL and task ID'; the user supplies them before the session in `./artifacts/t16-input.md` (or the `/sc:implement` invocation text)". F-06 (Change 7): "plan:26's and plan:254's 'approval at that moment' clauses are reworded". F-02 (Change 3) adds: "plan:233's 'delete it afterwards only with the user's approval' moves into the runbook". Add plan:233, plan:243, plan:254 to the respective evidence lists.
5. F-06: the pre-approval request covers "items 1, 2, 3, 5 (first half), 6 and 8". F-02's runbook step reads "export `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID` and `CLICKUP_LIST_IDS` (the test list, F-11) and have the test issue URL and task ID ready", plus one line saying the runbook results are recorded in a new note next to the archived package under `.dev/tasks/done/` because the package is archived after Task 17 (src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:47-54). F-02 and F-12 state the pending outcome as the rule to follow, not as a fact about Claude Code (whether a skill hot-loads mid-session is UNVERIFIED).
6. F-01 (2): after "a `/pull/<N>` URL" add "(on origin: rejected, not parsed as an issue number, with a stated code)".
7. F-03 (Change 4) adds: "plan:136's negative case writes its `gh issue view` line as a code span or fenced line".
8. Labels: the INV-008 line of Change 21 reads "would leave every worker unable to write its file, so every claim or create ends `E-WORKER-NO-OUTPUT` (source.md:335) [INFERRED]"; F-18's claim appends "[INFERRED: an open PR's `state` reads `OPEN`; `gh issue edit` on a PR number is UNVERIFIED]"; F-01 (1) appends "(that this repo does not exist is UNVERIFIED; no gh was run)". Every finding carries `category` and `source_cards`: A-00x findings (F-08 to F-12) use `source_cards: []` with the calibration that named them in the debate ruling; F-18 uses `source_cards: []` and names the invariant probe; F-13 `[reviewer-1]`; F-14 to F-17 `[reviewer-3]`. Overview provenance sentence reads "taken from the Round 2 position tables, the reviewer cards, the round-1 statements, `.work/evidence-sheet.md` or the probe".

Risk Summary additions: Change 22 (Low, header/provenance), Change 23 (Low, new minor finding), Change 24 (Low, wording and scope corrections).

## Review Status
- Independent analytical review: `.work/refactor-plan-review.md`, VERDICT: APPROVE with 8 minor amendments (Change 24). Auto-approved for merge (non-interactive mode) on 2026-11-04 after that review; approval status: auto-approved.
