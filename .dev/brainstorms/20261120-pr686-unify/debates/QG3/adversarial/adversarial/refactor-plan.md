# Refactoring Plan: Merge into Base (Variant 1, OURS)

## Overview
- Base: Variant 1 (OURS) at `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG3/adversarial/adversarial/variant-1-original.md`
- Incorporating strengths from: Variant 2 (CLAY) at `.../variant-2-original.md`
- Planned changes: 6
- Risk level: Low (additive; two edits reword base text)
- The merged file is a position paper that states the winning answer to each of OD-6, OD-10, OD-11, OD-12 with sources, so wording keeps every file and line citation of both variants.

## Planned Changes

### Change 1: OD-12 layer 1 becomes "narrows", verb refusal named (from Variant 2)
- **Source**: Variant 2, Claim OD-12, Mechanism bullet 4, Cited facts 6 and 7 (D:688, D:758, D:765; `repos.py:227-259`)
- **Target**: Base, Claim OD-12 and Mechanism bullet 4 (restructure)
- **Rationale**: C-004 HYBRID 69 percent, X-003 HYBRID 58 percent; both advocates conceded layer 1 "out of reach" cannot be achieved as the same OS user (A-002); the `repos` verb refusal is the only named, testable mechanism for layer 1.
- **Integration point**: Layer 1 = the `repos` verbs refuse `reach_daily_max`, `grants`, `merge_safety_files` and `reviewers` (the last is an addition and is marked as a recommendation, not Clay's text) without an accepted answer record, plus a protective hook on Write and Edit; worded "narrows". Layer 2 = fail closed on weakening values (`merge_safety_files: []`, `reviewers: none`, bad `reach_daily_max`) unless an accepted answer record names the value.
- **Risk**: Low, wording only.

### Change 2: OD-10 merge go names the close, with the reopen guard (from Variant 2)
- **Source**: Variant 2, What it gets right bullet 1 (SKILL.md:114) and Cited fact 3 (D:799 (f))
- **Target**: Base, Claim OD-10 and Mechanism bullet 2 (append)
- **Rationale**: C-006 HYBRID 61 percent; reversibility lowers the cost of a go that names the close; closeout never closes an issue a person reopened.
- **Integration point**: The go names "merge PR N at sha X, then close issue M if closeout's verdict is done"; the go ends when both are done, the head moves, or the owner revokes it in chat. The `Fixes` line still closes at merge.
- **Risk**: Low.

### Change 3: OD-6 argv list with one refusal test per entry (from Variant 2)
- **Source**: Variant 2, Cited fact 1 (D:763)
- **Target**: Base, Claim OD-6 (append)
- **Rationale**: C-001 OURS 89 percent keeps the unconditional refusal; Clay's enumerated argv list and per-argv test (D:763 last column) is a separable strength.
- **Integration point**: N6 refuses `git tag`, `git push --tags`, `git push origin <tag>`, `gh release create`, `gh release edit`, `gh release delete`, `uv publish`, `twine upload`, `npm publish` with no `--answer-ref` pass; one denylist test per argv, and a test that an `--answer-ref` does not change the result. Merging a release pull request stays allowed on the per-PR go (D:763, D:118).
- **Risk**: Low.

### Change 4: OD-11 refusal text names the missing grant (from Variant 2)
- **Source**: Variant 2, Claim OD-11, Cited fact 5 (D:116), What it gets right bullet 4 (zero-setup)
- **Target**: Base, Claim OD-11 and What it costs (append)
- **Rationale**: C-007 OURS 63 percent; the one-chat-message cost is real; the benefit of a standing list (works at once, visible) is delivered without a standing authority.
- **Integration point**: The empty default stays. The `E-NO-GRANT` refusal names the missing entry and the sentence the owner can say in chat; the first run lists the three standing entries once for the owner to grant in one chat answer, which the agent records with its quoted words, date, scope and recorder (Q01 item 3).
- **Risk**: Low. The three entries are named from D15 (`issue.assign`, `issue.comment`, `issue.body.append_plan_sections`).

### Change 5: Surface the two promoted shared assumptions (A-001, A-002)
- **Source**: diff-analysis.md A-001, A-002; both advocates ACCEPT or QUALIFY
- **Target**: Base, new section "Conditions and limits" before "What it gets right" (insert)
- **Rationale**: A-001 (controls are design text, not built) and A-002 (the config is writable by the coordinator's shell) were UNSTATED in both papers and affect every answer; both advocates accepted them.
- **Integration point**: State both as limits with the wording rule: every control narrows and never closes.
- **Risk**: Low.

### Change 6: Per-sub-question winner table (new)
- **Source**: debate-transcript.md Scoring Matrix
- **Target**: Base, end (insert), "Result of the debate"
- **Rationale**: the caller reads one answer per sub-question with confidence and the points that stay open (C-006 and X-003 resolved as HYBRID).
- **Integration point**: Table OD-6 OURS 89, OD-10 OURS 77 with C-006 wording, OD-11 OURS 71, OD-12 HYBRID 69.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-001 | N6 pass path with `--answer-ref` | U57 open (D:1315); release irreversible (D:676); CLAY advocate conceded (OURS 90 percent) |
| C-002 | Standing `issue.close` | `E-NO-GRANT` does not bind closeout (D:696, SKILL.md:51); contract line 241; CLAY advocate conceded |
| C-003 | Standing entries (six) at install | Parser default is empty (`repos.py:295`); standing `pr.merge` on unprotected master (D:117); CLAY advocate conceded |
| C-007 | Zero-setup as a reason for standing entries | The zero-setup aim is cited from memory the CLAY advocate could not read (UNVERIFIED); one recorded chat message is the owner's rule |
| X-004 | Release treated as person-gated in row 5 while N6 passes | Rejected as inconsistent; base keeps one rule |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | Layer 1 reads stronger than it is | Restore "outside write reach" wording |
| 2 | Low | Close without a go | Remove the close clause |
| 3 | Low | Argv list incomplete | Add entries |
| 4 | Low | First-run message missing | Remove the message |
| 5 | Low | Limits read as defects | Drop the section |
| 6 | Low | None | Remove table |

## Review Status
- [x] Auto-approved (default)
- Approved by: auto
- Approval timestamp: 2026-11-20T09:20:00Z
