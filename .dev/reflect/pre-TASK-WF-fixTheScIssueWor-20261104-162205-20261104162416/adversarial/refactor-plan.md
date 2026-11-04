# Refactoring Plan: Merge into Base (Variant 3)

## Overview
- Base: Variant 3 (opus:refactorer), `variant-3-original.md`
- Strengths incorporated from: Variant 1 (sonnet:analyzer), Variant 2 (haiku:qa), and the Round 2.5 invariant probe as resolved in Round 2.6
- Output: `merged-verdict.yaml` in this directory. Its top-level keys are `merge_method`, `base_variant`, `convergence_score`, `verdict`, `findings` and `unresolved_conflicts`. Each finding has the fields `id`, `file_line`, `claim`, `class`, `severity`, `recommendation` and `source_variants`. Provenance goes in YAML `#` comments.
- Fixed values: `merge_method: adversarial`; `base_variant: "opus:refactorer (variant-3)"`; `convergence_score: 0.94`.
- Verdict rule: FAIL only if any merged finding is blocking. M-13 is blocking, so the verdict is **FAIL**.
- Planned changes: 13
- Risk level: Low (every change is a finding-level edit to a flat list)

File paths in `file_line` use the base's convention: the plan file name plus line, or a repo-relative path plus line.

## Planned Changes

### Change 1: M-01 early-section authority (base R3-F5, modified)
- **Source**: Base R3-F5, plus V1 R1-F1 (early-section part) and V2 R2-2. Debate: X-001 and C-001; the final class was unanimous in Round 2.
- **Target**: Replace R3-F5. Set `id: M-01`, `file_line: "TASK-WF-fixTheScIssueWor-20261104-162205.md:19,22-26 vs source.md:1"`, `class: grounding_gap`, `severity: minor`, `source_variants: [variant-1, variant-2, variant-3]`.
- **Claim**: "The early section goes beyond source.md:1, which names only the Rules section. Its placement rationale ('must ... sit early in each agent file, not only in Rules', plan:19) is the plan's own inference. Neither #365 nor the retry tested a Rules-only rule, and no package file stores the coordinator message."
- **Recommendation**: "Save the coordinator message under the package's artifacts/. State in the plan that early placement is the author's inference from the retry evidence."
- **Risk**: Low

### Change 2: M-02 SKILL.md line outside the spec's Files list (from V2 R2-1)
- **Source**: V2 R2-1, plus V1 R1-F1 (SKILL.md part). Debate: unanimous drift in Round 2. V1, V2 and V3 conceded their authorized and grounding_gap labels.
- **Target**: Insert after M-01. Set `id: M-02`, `file_line: "TASK-WF-fixTheScIssueWor-20261104-162205.md:20,68-77 vs source.md:1"`, `class: drift`, `severity: minor`, `source_variants: [variant-1, variant-2, variant-3]`.
- **Claim**: "Task 3 edits SKILL.md, which is not in the spec's Files list. Plan:20 calls it 'judged needed', which discloses it as the author's judgement. The quoted coordinator line authorizes naming files explicitly, not editing SKILL.md."
- **Recommendation**: "Record the requester's sign-off for the SKILL.md line, or descope Task 3."
- **Risk**: Low

### Change 3: M-03 pointer-style Rules bullet (from V2 R2-3 and V1 R1-F2)
- **Source**: V2 R2-3 and V1 R1-F2. Debate: C-002 and X-002, unanimous drift. Judged not a missing deliverable: the bullet carries the core rule, and the full statement sits once in the same file.
- **Target**: Insert. Set `id: M-03`, `file_line: "TASK-WF-fixTheScIssueWor-20261104-162205.md:27-29 vs source.md:1"`, `class: drift`, `severity: minor`, `source_variants: [variant-1, variant-2]`.
- **Claim**: "The Rules bullet points to the early section. It omits E-WORKER-NO-OUTPUT, the 'failure' wording, the consumers (gh --body-file, /sc:recommend) and the harness-note clause, all of which source.md:1 places in the Rules-section rule."
- **Recommendation**: "Add '(E-WORKER-NO-OUTPUT)', the 'is a failure' wording and the harness-note clause to the Rules bullet, so that it stands alone."
- **Risk**: Low

### Change 4: M-06 exact-text delimiters (base R3-F1, modified)
- **Source**: Base R3-F1, plus V1 R1-F5 and V2 R2-5. Debate: C-003, unanimous.
- **Target**: Replace R3-F1. Set `id: M-06`, `file_line: "TASK-WF-fixTheScIssueWor-20261104-162205.md:24-32"`, `class: grounding_gap`, `severity: minor`, `source_variants: [variant-1, variant-2, variant-3]`.
- **Claim**: "The four byte-identical texts sit in single-backtick spans that themselves contain backticks, with a two-space indent. The outer delimiter, the indent and the trailing-period boundary are ambiguous. A consistent mis-copy in both the test constant and the agent text would pass every check."
- **Recommendation**: "Put each exact text in a fenced block, or state that the module constants are the canonical bytes. Check that the inserted lines carry no stray outer backtick or indent."
- **Risk**: Low

### Change 5: M-07 verify-sync on unrelated drift (from V1 R1-F6)
- **Source**: V1 R1-F6. Debate: C-008, unanimous. Evidence is Makefile:188-200. INV-006 notes that verify-sync exits 0 today, so the risk is latent.
- **Target**: Insert. Set `id: M-07`, `file_line: "TASK-WF-fixTheScIssueWor-20261104-162205.md:72,77; Makefile:188-200"`, `class: grounding_gap`, `severity: minor`, `source_variants: [variant-1]`.
- **Claim**: "make verify-sync fails when .claude/skills/ holds a directory with no source (Makefile:188-200). The plan's 'exits 0' criterion gives no instruction for a failure caused by unrelated files."
- **Recommendation**: "Add: if verify-sync fails because of files outside this plan, record the failure in t3-verify-sync.log and do not fix it here."
- **Risk**: Low

### Change 6: M-09 report wording (base R3-F2, modified)
- **Source**: Base R3-F2, plus INV-008. Debate: C-006, unanimous. INV-008 folded in unanimously in Round 2.6.
- **Target**: Replace R3-F2. Set `id: M-09`, `file_line: "TASK-WF-fixTheScIssueWor-20261104-162205.md:26; src/superclaude/agents/issue-worker-t2.md:17; src/superclaude/agents/issue-worker-t1.md:17"`, `class: drift`, `severity: minor`, `source_variants: [variant-3]`.
- **Claim**: "'the reports under analysis/' repeats the harness note's trigger words ('report', 'analysis') in the sentence meant to defeat it. The unchanged job text in t1:17 and t2:17 ('save its report under <D>/analysis/') clashes with the new 'not a report' rule on the same file class."
- **Recommendation**: "Say 'the files under analysis/' in the early paragraph."
- **Risk**: Low

### Change 7: Remove R3-F3 (M-10)
- **Source**: Base R3-F3. Debate: C-005. V3 conceded in Round 1; all three dropped it in Round 2.
- **Target**: Delete from the findings list. List it under Changes NOT Being Made.
- **Rationale**: The parenthetical copies source.md:1 word for word.
- **Risk**: Low

### Change 8: M-11 "names each exact path" (base R3-F4, modified)
- **Source**: Base R3-F4, plus INV-007, which is subsumed. Debate: C-007, unanimous.
- **Target**: Replace R3-F4. Set `id: M-11`, `file_line: "TASK-WF-fixTheScIssueWor-20261104-162205.md:32; src/superclaude/skills/sc-issue-protocol/refs/claim.md:58"`, `class: drift`, `severity: minor`, `source_variants: [variant-3]`.
- **Claim**: "'names each exact path' cannot hold for analysis/. /sc:analyze chooses the file name, and it is written only when the verdict is out_of_date (claim.md:58), so the set can be empty."
- **Recommendation**: "Let the SKILL.md line name the analysis/ directory when the job may write there."
- **Risk**: Low

### Change 9: M-12 helper position check (base R3-F6, kept)
- **Source**: Base R3-F6. Debate: C-004, unanimous.
- **Target**: Keep it. Set `id: M-12`, `file_line: "TASK-WF-fixTheScIssueWor-20261104-162205.md:27,45,65"`, `class: drift`, `severity: minor`, `source_variants: [variant-3]`.
- **Claim**: "The helper checks that the Rules bullet is inside ## Rules. It does not check that the bullet directly follows the 'Writing only under .dev/issues/' bullet, which plan:27 requires, and the Task 2 criterion does not check this either."
- **Recommendation**: "The helper also checks that the line before the bullet starts with '- **Writing only under `.dev/issues/`.**'."
- **Risk**: Low

### Change 10: M-13 untracked targets make the diff criteria vacuous (from INV-001; blocking)
- **Source**: Invariant probe INV-001, HIGH. Round 2.6 voted it unanimously as grounding_gap and blocking. The orchestrator re-checked it: `git status --short` shows `??` on all five targets.
- **Target**: Insert. Set `id: M-13`, `file_line: "TASK-WF-fixTheScIssueWor-20261104-162205.md:53,65,75"`, `class: grounding_gap`, `severity: blocking`, `source_variants: [invariant-probe:INV-001, variant-1, variant-2, variant-3]`.
- **Claim**: "All five target files are untracked (git status '??'; git ls-files lists none): issue-worker-t1/t2/t3.md, sc-issue-protocol/SKILL.md and tests/skills/test_issue_worker_agents.py. git diff prints nothing for untracked files, so three criteria would pass on empty output: 'git diff on each file shows only those additions' (plan:65), 'SKILL.md gains exactly that one line ... and no other change' (plan:75) and 'no existing test is changed' (plan:53). That is a false completion claim, and the 'touch no other wording' rule (plan:34) goes unenforced."
- **Recommendation**: "Before any edit in Task 1, copy the five target files to ./artifacts/pre/. Restate the criteria at plan:53, plan:65 and plan:75 as 'git diff --no-index ./artifacts/pre/<f> <f>' showing only the specified added lines, with the output and exit code saved under ./artifacts/. Exit 1 means the files differ, which is the expected result."
- **Risk**: Low

### Change 11: M-14 behavioural sufficiency (from INV-002, A-001, A-003)
- **Source**: INV-002 (MEDIUM), with A-001 and A-003 (QUALIFY from all three). Round 2.6: unanimous grounding_gap, minor.
- **Target**: Insert. Set `id: M-14`, `file_line: "TASK-WF-fixTheScIssueWor-20261104-162205.md:12,15,72; src/superclaude/skills/sc-issue-protocol/SKILL.md:58-62"`, `class: grounding_gap`, `severity: minor`, `source_variants: [invariant-probe:INV-002, variant-1, variant-2, variant-3]`.
- **Claim**: "The tests pin text only. The plan does not show that a spawned worker now writes its files: the installed ~/.claude/agents/ copies are absent, a live re-claim is out of scope (plan:36), and the agent body's precedence over the harness line is untested. .dev/issues/365/ still has no summary.md."
- **Recommendation**: "State in the plan that it proves the text only. Record as the follow-up a live re-claim of #365 after superclaude install, in a new session."
- **Risk**: Low

### Change 12: M-15 the refs' spawn steps name no paths (from INV-003)
- **Source**: INV-003 (MEDIUM). Round 2.6 voted grounding_gap, minor, by a 2-of-3 majority (V2 voted drift).
- **Target**: Insert. Set `id: M-15`, `file_line: "TASK-WF-fixTheScIssueWor-20261104-162205.md:20,32; src/superclaude/skills/sc-issue-protocol/refs/claim.md:53-54; src/superclaude/skills/sc-issue-protocol/refs/create.md:20"`, `class: grounding_gap`, `severity: minor`, `source_variants: [invariant-probe:INV-003, variant-1, variant-2, variant-3]`.
- **Claim**: "The orchestrator builds spawn prompts from refs/claim.md and refs/create.md, which pass only the job, <R>, <N> and <D>, and those refs stay unchanged. By the plan's own 'nearest instruction' reasoning (plan:20), the new SKILL.md line may not govern the actual spawn prompt."
- **Recommendation**: "Word the SKILL.md line so that it explicitly covers the Wave spawns in refs/claim.md and refs/create.md (claim.md:57,59 already name the exact paths), and record that the refs stay unchanged on purpose."
- **Risk**: Low

### Change 13: Header, verdict and unresolved conflicts
- **Target**: Top of the file. Write a provenance header and the fixed keys, then `verdict: FAIL`. Write `unresolved_conflicts` as a list with one entry: `{id: X-001, topic: "winner label for the scope-expansion class conflict", status: "per-point winner split V1/V2/V3; governed classes M-01 grounding_gap and M-02 drift are unanimous"}`.
- **Order**: List the findings in the order M-01, M-02, M-03, M-06, M-07, M-09, M-11, M-12, M-13, M-14, M-15.
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point / Item | Non-Base Approach | Rationale |
|---|---|---|
| M-04 (V1 R1-F3) | Keep "flags-user.md omission grounded" as a finding | It confirms the plan is correct and is not a deviation. All three advocates chose keep=no (create.md:32). |
| M-05 (V1 R1-F4) | Negative tests could pass vacuously | The claim is false: a no-op removal fails the negative test. V1 conceded, and all three chose keep=no in Round 2. |
| M-08 (V2 R2-4) | Brief coverage slice lists only INF-004/005 | This concerns the audit record, not the plan. V2 conceded in Round 2. |
| M-10 (base R3-F3) | Consumer parenthetical incomplete | It copies source.md:1 word for word. V3 conceded. |
| INV-005 | Separate finding on heading-match weakness | The constant at plan:24 includes `## `. All three advocates chose drop. |
| INV-007 | Separate finding on an empty analysis/ set | Covered by M-11 |
| V1 Round 2.6 minority proposal | Fold per-piece negative tests and a line-anchored heading check into M-12 | Only 1 of 3 supported it. The other two advocates covered it as dropped (INV-005). |
| X-001 V1 Round 1 class "authorized" | Scope expansion is authorized | All three conceded in Round 2. |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1-9, 11-12 | Low | One finding misstated | Restore from the source card and this plan |
| 10 | Low | The verdict flips to PASS if this change is omitted | Re-apply; the evidence is in invariant-probe.md |
| 13 | Low | Schema mismatch for the caller | Re-write the header keys per the Overview |

## Review Status
- [x] Auto-approved (default; non-interactive)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-04T17:03:27Z
