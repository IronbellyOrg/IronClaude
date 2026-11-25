# X07 (OA-11) Which standing grants the coordinator may have. Final proposal (recommendation only until the owner says so)

Checked 2026-11-22 on origin/master after fetch. SPEC = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md. A "grant" is a standing permission for one kind of GitHub write. S13 = coordinator base stage, S14 = merge path and grant checks, S15c = hand-back re-plan, S17 = live test on a throwaway repository.

## 1 Unified proposal
Two grants now, one repository at a time, only after the code that checks them exists. Nothing is active today.
1. Grant `issue.comment` and `issue.status.move` (Status to In review only, from allowed Statuses, never Done). They are exactly what FR-83 needs (SPEC line 243).
2. `issue.body.append_plan_sections` waits for S15c, its own sentence, and only after the owner has read one posted plan section on that repository.
3. `issue.assign` is withheld until some coordinator code needs it (the claim session assigns). `pr.merge` and `issue.close` are never grantable (SEC-06); `issue.hold` was removed (Q03). One per-PR go on the head sha covers merge and that PR's issue close (OD-10).
4. Scope: one `owner/repo` per grant, adopted issues only, no wildcard, never global. A repository added later starts empty.
5. Expiry: an end date is always stored. Default 90 days, longest 90, no "forever". After it, writes refuse and say "expired on <date>". The owner may name a shorter number.
6. Where it lives: a separate grants file next to the approvers file, not a key in the watcher config, with its path protected under SEC-10. Every write re-reads it. Missing, unreadable, malformed, unknown entry, wrong repo, past end date, repo not enabled or issue not adopted means no grant. Each use is logged with the grant id in `grants-use.jsonl`.
7. Revoke: "Revoke <entry> on <repo>" or "Revoke all on <repo>". Newest line wins, a revoke wins a tie, it bites at the next write, and it needs no accepted-record check because it only narrows. S13 adds a `repos revoke` verb (none exists in the plan). An agent may suspend an entry at once after a wrong write if it says so in chat; only the owner turns it back on.
8. Completion rule: a succeeded run needs both entries; a failed, blocked or partial run needs only `issue.comment`, so a failure is never hidden. If that comment is refused, the local escalation shows the failure.
9. Refusal (printed before any `gh` call, no issue text echoed): `Refused: no standing permission "<entry>" for <owner/repo> (none recorded, expired on <date>, or revoked). Nothing was written to issue <N>. To allow it the owner says in chat: "Grant <entry> on <owner/repo> for adopted issues, <N> days." A local escalation was recorded.`
10. Order: (a) owner says the design sentence in section 7 (decision only); (b) spec and contract edits land; (c) S13, S14 built; (d) OA-19 names the throwaway repository; owner says the activation sentence; (e) after the S17 run passes, same sentence for `IronbellyOrg/IronClaude`; (f) body entry when S15c lands.

## 2 Context
Master has no code that reads or refuses a grant. A grep of origin/master under `issue_watch` and `issue_pipeline` finds only two text mentions (`issue_pipeline/complete.py:3`, `issue_pipeline/cli.py:252`). QG3 OD-11 and D15 set the default: empty, fail closed. SPEC SEC-07 (line 296) allows four entries; OD-11, OA-11, R-4 and X-1 (lines 107, 580, 598, 602) say three or four, which is an inconsistency to fix. The repository is public and the login `ironbelly` is shared by the owner and agents.

## 3 Implications
Changes: SEC-07 and OA-11 narrow to two entries now and one later; SPEC line 243 gets the per-outcome rule; the grants file gets one home (SPEC line 176 says state folder, line 299 says config key); SEC-10 protects that path; `WORKER-CONTRACT.md` lines 302-303 ("only under that issue's grant row", "without that issue's grant row") become "the repository's standing grant, on an adopted issue", and line 57 (grant row "still written by the owner") is brought in line with the chat rule (OA-7). A `repos revoke` verb and an adopted-issue check are new build items.
Stays blocked: no live coordinator write until S14 exists and OA-19 names a repository; every merge and close stays one per-PR go; OA-6 (who counts as "the owner" on the shared login) still limits merge goes.

## 4 Benefits
The coordinator posts the result and moves the issue to In review with no owner round trip. Each permission has a repository, a user, an end date, a use log and a one-line off switch. A typo in grants cannot stop the poll. Merge, close, hold and assign stay out.

## 5 Risks (contain)
- Shared login: only our verbs check grants; any shell with the login can run `gh` directly (SEC-13, SEC-18, D15). Word it "narrows", never "closes". Keep the verb refusal and the Write/Edit hook.
- Any session on this host can claim the owner said it (SEC-09, OA-6). Record the quoted words and recorder so it shows afterwards; only a session the owner opened and types in records.
- Public repository: comments and Status moves are world-readable and show as the owner. FR-83 limits text to an outcome word, validated paths and a PR number; keep that test. A comment can be deleted and a Status moved back; a body edit's history survives revoke, hence the sample-first rule.
- Before S14 nothing refuses a write. Contain: no real-repository sentence until the checking verb exists; the interim ledger line (SEC-14) says "decision only, not an active grant".
- A forgotten renewal makes writes refuse. Safe, but the message must say "expired".
- Contract wording mismatch: a literal worker could read a standing grant as not enough. Contain: amend lines 302-303 with the owner's chat approval before S14.

## 6 Costs (estimates, not measured; neither agent read Clay's parser)
- Owner: about 1 minute per sentence (one message).
- Agent recording: about 15 minutes per grant (one ledger line or one verb call plus read-back).
- Spec and contract edits: about 1.5 hours (about eight table rows plus two contract lines).
- Build over what S14 already includes: about 5 to 8 hours (grants-file loader 1, revoke verb 1 to 2, about eight small tests 2 to 3, adopted-issue check 1, contract review 0.5). Counting the whole grant feature: 8 to 12 hours. SEC-07 already requires one `E-NO-GRANT` test per entry.

## 7 The sentence the owner says in chat
Now (the decision): "OA-11 approved: the coordinator's standing grants are issue.comment and issue.status.move only, one repository at a time, adopted issues only, 90 days at most, revocable in chat; the plan-body grant waits for S15c; assign is withheld; merge and close are never standing."
Later (activation, per repository, after S14 exists): "Grant issue.comment and issue.status.move on <owner/repo> for adopted issues, 90 days."

## 8 What an agent does after it
Replies "Received" once. Before S14: appends one line to the interim ledger in the unification task package (SEC-14, staged): date, repo or "design only", entries, end date, the owner's quoted words, recorder, marked "decision only, not enforced by code, not an active grant". Starts the spec and contract edits (contract edit shown to the owner for chat approval, OA-7). From S14: `repos grant` writes the same fields to the grants file after the activation sentence, then reads it back and says what is now granted. On "Revoke ...": removes or ends the entry the same turn and records the words. The owner writes no file.

## 9 Consensus
Full on design (both agents sign the same ten points; A accepted a 90-day cap, B accepted two entries now and the body entry later). Residual owner choice, small and safe either way: length for the throwaway repository. Default (my pick): 90 days, one rule; renewal is proved by a fake-clock test and the refusal text carries the renewal sentence. Answer "30 days": one extra sentence in the first month and a real renewal rehearsal, at the cost of a second number to remember; this only rehearses renewal if the throwaway is still in use after 30 days, which is not certain. Safety is the same.

## 10 What could not be verified
- Whether S14 includes an adopted-issue check (none found on master; treated as a build item).
- The `repos grant` flags and the grants file's exact folder (not designed; the approvers file is a configured path, `cycle.py` lines 67 and 280).
- Clay's parser (`repos.py:295-299`, cited by SPEC R-4) was not opened.
- Which repository OA-19 will pick; the hour counts are estimates.
- Visibility and branch protection facts come from the agents' own `gh` reads, which I did not repeat.
- Checked by me: no grant code on master; `cycle.py` rejects unknown config keys (lines 59, 223); SPEC lines 176, 243, 296, 299; `WORKER-CONTRACT.md` lines 57 and 303 on master.
