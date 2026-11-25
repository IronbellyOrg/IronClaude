# Refactoring Plan: Merge into Base (Variant A)

## Overview
- Base: Variant A (OURS, `variant-1-original.md`)
- Incorporating strengths from: Variant B (CLAY, `variant-2-original.md`) and the 13 findings of the Round 2.5 invariant probe (`invariant-probe.md`)
- Planned changes: 9
- Risk level: Medium (changes 2, 5 and 6 define rules that touch WORKER-CONTRACT.md lines 23, 70, 244 and 245)
- Output of the merge: a merged position paper `merged-output.md` in the `--output` folder. It is the recommended authority model written as spec text, not a repository change. Nothing is applied to any repository file, GitHub or Orca.
- Rule for writing the merged text: state claims as "narrows" and not "closes" unless a named check exists (INV-012, INV-013); mark every unbuilt or UNVERIFIED gate as not shown to pass; no new facts beyond the two papers, the rebuttals and the probe.

## Planned Changes

### Change 1: Merge procedure with a read-only gate (from Variant B)
- **Source**: Variant B, "The mechanism" items 1 to 3, fact 1, fact 9; Round 2 A item 1 and B hybrid gaps (go window, restart)
- **Target**: Base, new section "Merge procedure" after "The mechanism" (insert)
- **Rationale**: C-001 (A wins who decides, 88%) with the gate adopted as a precondition (both advocates); U-005, U-010 High value. Closes INV-001: the gate runs again immediately before `gh pr merge`; the merge is refused if any gate reason, open thread, review state, base branch or draft state differs from what the person was shown; `--match-head-commit` is kept but is stated as covering only the head sha.
- **Integration point**: Steps: (1) the orchestrator runs the gate read-only; (2) it shows the output to the person; (3) the person types a go; (4) gate re-run; (5) `gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>`, never `--auto`, `--admin`, `--delete-branch`; (6) read back PR state; after a restart read PR state first. A passing gate never triggers a merge.
- **Risk**: Medium. The gate is unbuilt (design only); the spec must label it a requirement for a later build, not a present control.

### Change 2: What a go is, how long it lives, what it may override (from Variant A rebuttal, Variant B hybrid gaps, INV-002, INV-004, INV-006)
- **Source**: Round 2 A "Updated assessment" (go contents), Round 2 B "Hybrid gaps"
- **Target**: Base, new subsection under "Merge procedure" (insert)
- **Rationale**: Closes INV-002, INV-004, INV-006. The go names repo, PR, full 40-character head sha, merge method (checked against the repo's `merge_method` or `release_merge_method`), the word "merge" and the gate output it refers to; typed in live chat after the gate output; recorded as an entry (repo, PR, sha, time). It has a stated expiry (the number is an owner DECISION; no source gives it) and is void on any head change or any new gate reason. Reasons table: head_moved, draft, not_mergeable, snapshot_incomplete and changes_requested are never overridable by a go; merge_safety and checks_failing only by a go that carries that reason's own question key; review_stalled and review_none_present are not overridable (the owner sets `reviewers: none` for a repo with no review agent). Whether `changes_requested` is a hard refusal is stated as the recommended rule and listed as an owner DECISION.
- **Integration point**: One table with the 13 gate reasons and a column "go may override". The windows: the 2-minute window runs gate-to-merge (the second gate run), the 60-minute hold runs from the final head's checks finishing.
- **Risk**: Medium. Several numbers (expiry, 60 minutes) are UNVERIFIED defaults.

### Change 3: Merge-time reviewer hold with a final-head re-trigger (from Variant B, INV-005, INV-007, INV-008, INV-009)
- **Source**: Variant B facts 2 to 4; Round 1 A shared assumption A-001; Round 2 A item 2
- **Target**: Base, new section "Silent reviewer" (insert); the loop's skip rule stays as written in the base
- **Rationale**: C-004 and X-003 (B wins, 85%): the loop's absent state is sticky and clock-based (reviewers.py:390-391, SKILL.md:31-32), so one done plus one absent reads clean (:417-419). Closes INV-009 by making the hold an explicit step: request a review of the final head from each listed reviewer, then wait. Closes INV-005 by write-protecting `reviewers` (including `none`) on the owner's recorded word. States INV-007 (what a list naming an uninstalled reviewer does, and what `none` prints) and INV-008 (zero checks: the 60-minute clock has no anchor, so the hold falls back to the push time of the final head).
- **Integration point**: `/sc:pr-submit` is unchanged. The hold lives in the gate's `review_stalled` and `review_none_present` reasons.
- **Risk**: Medium. Whether Codex reviews on push or only on request is UNVERIFIED; that is why the re-trigger step is explicit.

### Change 4: `answer-check` as a stale-answer validator only (from Variant B)
- **Source**: Variant B mechanism item 4, fact 5; Round 2 A item 3; Round 2 B concession
- **Target**: Base, "The mechanism" item 5 (modify)
- **Rationale**: C-005 and X-004 (hybrid, 75% and 80%); INV-003 and INV-013. It checks entry, question key, head sha and freshness. It does not prove who typed the answer: the same terminal accepts `orca terminal send` (D:112), and a script knows the sha. The spec says so and lists spoofed typing as a residual risk; whether the harness marks sent text differently from typed text is UNVERIFIED.
- **Integration point**: Replace "approvals are given in chat and are checked as such" with the validator wording and the residual-risk sentence.
- **Risk**: Low. Wording only; no new control is claimed.

### Change 5: One-shot go versus `E-NO-GRANT` (from Variant B rebuttal item 4, INV-011)
- **Source**: Variant B Round 2 "Remaining dispute" item 4; Variant B fact 5 (grants keys)
- **Target**: Base, new section "Standing lists" (insert)
- **Rationale**: C-007 (A wins, 85%) keeping B's refusal: a verb refuses any GitHub write not on a list the owner recorded in chat, and the list never holds `pr.merge` or `issue.close`. INV-011: `E-NO-GRANT` sees only writes made through the orchestrator's own verbs, so the spec requires the merge to go through a verb that demands the go entry of Change 2 and refuses raw `gh pr merge` outside it. The go is a one-shot entry, not a grants row.
- **Integration point**: A two-column table: action, how it is authorized (standing list, per-issue go, per-PR go).
- **Risk**: Medium. Needs the verb to exist; marked as a requirement.

### Change 6: Script-started depth-0 coordinator and the contract lines to amend (from Variant B, INV-010)
- **Source**: Variant B fact 7; Round 2 A (c), (d); Variant A facts 7 and 8
- **Target**: Base, "The claim" and "Cited facts" 7 and 8 (modify) plus new section "Contract amendments" (insert)
- **Rationale**: C-002 and X-001 (hybrid; B wins the depth reading, 85%). A terminal plus `ccsession` start is depth 0; "person opened" (WORKER-CONTRACT.md:70) is a separate authority rule. INV-010: a launch-prompt authorization is self-attested because the script writes the prompt; the spec declares this and requires that the prompt cite the owner's recorded authorization (a record the owner gave in chat and an agent wrote down) and list only duties it names. Amendments, each needing the owner's chat approval first: :70 (person opened, or started at depth 0 by the owner's installed watcher under a recorded standing authorization), :245 (Full Submit per-issue go for a feature-branch push and PR only, never a merge, force push or branch deletion), and a note that :23 and :244 stay unchanged because the Full Submit launch is an ordinary top-level session.
- **Integration point**: A list of exact one-sentence amendments by line.
- **Risk**: Medium. Contract text changes are a DOC action for the owner; this plan applies none.

### Change 7: Nine-row "what reaches the person" list as a reasons inventory (from Variant B)
- **Source**: Variant B fact 6; Round 2 B "Remaining dispute" item 5
- **Target**: Base, new short section "Reasons to reach the person" (insert)
- **Rationale**: C-006 (A wins, 85%); U-007 Medium. Adopted only as an inventory for non-outward decisions; every outward action still waits for the person's go. Benefit not shown in use (UNVERIFIED), so the section is marked as an owner DECISION to adopt.
- **Integration point**: Three lines, with the owner DECISION flag.
- **Risk**: Low.

### Change 8: Risk register with residual risks and the admin-side control (from Variant B, A-004, INV-003, INV-012, INV-013)
- **Source**: Variant B risk habit (K12, AU4a, AU7); shared assumption A-004; probe INV-003, INV-012, INV-013
- **Target**: Base, "What it risks" (modify)
- **Rationale**: The base has risks without mitigations (R1 to R3 NOT MET). Adds a table: risk, mitigation, status (built, designed, UNVERIFIED). Residual risks stated: spoofed typing; self-attested launch prompt; go replay after restart (mitigated by Change 2 expiry and entry); `master` unprotected. A-004: branch protection, a ruleset, required review or a merge queue is a repo-admin action and is listed as an owner DECISION, not a consensus item. Claims are phrased as "narrows" (INV-012, INV-013).
- **Integration point**: Replace the two bullet lists under "What it costs" and "What it risks" with the table plus the original bullets kept.
- **Risk**: Low.

### Change 9: Post-merge audit kept (from Variant B)
- **Source**: Variant B Round 2 hybrid gap on AU4a and AU7 (D:812, D:601)
- **Target**: Base, "Merge procedure" last step (append)
- **Rationale**: B's point that an audit finds a merge the gate did not make remains useful even when a person gave the go. U-005 related.
- **Integration point**: One line after the read-back step.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-001 | Orchestrator merges when the gate passes, with no per-PR go | Master `IronClaude` is unprotected (D:118, K12); B's advocate agreed the benefit is only throughput, with no measured figure |
| C-003 | A `worker-start` worker with `Flow: orchestrated-issue` runs `/sc:pr-submit` (ADD1) | D3 stands; AC-4.3 never ran; ADD1 states no brief-guard route; pr-submit has no unattended mode (both advocates) |
| C-006 | Everything not on the nine-row list is decided by the orchestrator and recorded | Outward actions keep a named go (WORKER-CONTRACT.md:241); the list is adopted only as an inventory (Change 7) |
| C-007 | Repo-level standing `grants` including `pr.merge`, `issue.close` | Not shown to be better; conflicts with :245 (both advocates); only `E-NO-GRANT` is kept (Change 5) |
| C-004 (part) | ADD4's statement that a silent reviewer is no longer skipped | `/sc:pr-submit` keeps its skip rule in the loop; the hold lives at merge time (Change 3) |
| C-010 | Clay's rulings of 2026-11-19 as the authority for these rules | The owner's decisions D3, D4, D5, GIT of 2026-11-02 stand until the owner changes them in chat (APPROVED.md:10-13) |
| C-005 (part) | `answer-check` as evidence that a person answered | It cannot tell a person from a script (D:694); kept as a validator only (Change 4) |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | The gate is unbuilt; the section reads as a control that does not exist | Mark it "requirement, not built"; keep the person's go as the only control |
| 2 | Medium | An overridable reason lets a bad merge through | Make every reason non-overridable except by its own key |
| 3 | Medium | A dead 60-minute wait when a reviewer is never triggered | Owner sets `reviewers: none` for that repo, or shortens the wait |
| 4 | Low | Reader mistakes the validator for proof of a person | Residual-risk sentence stays |
| 5 | Medium | Raw `gh pr merge` bypasses the list | State that the merge goes through a verb; audit with Change 9 |
| 6 | Medium | A script supplies its own authorization | Declare it self-attested; require a cited owner record |
| 7 | Low | Table adopted without use evidence | Remove the section |
| 8 | Low | Table overstates a mitigation | Keep the status column honest (built, designed, UNVERIFIED) |
| 9 | Low | None | Remove the line |

## Review Status
- [x] Auto-approved (default; `--interactive` not set)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-20 (UTC)
