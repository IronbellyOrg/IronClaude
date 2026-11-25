# Position CLAY (D16): the lightest change, a written team agreement plus one or two files

Written 2026-11-20 for debate D16. Advocate for Clay's line.

## Claim
The incident was a people problem: a question to a named person (Clay's comment on issue 450, 2026-11-18 17:00:32, "What do you think?") got no written answer, and nobody had defined who "the owner" is. The lightest fix that would have prevented it is one agreed paragraph plus one template line, both in files that already exist, costing under an hour and needing no admin setting. Everything heavier adds gates to a team that works on trust today, would slow the owner's own PRs, and most of it would not have found the owner's unpushed work, which is what was actually missed.

## Mechanism
One edit to CONTRIBUTING.md (it already holds team conventions that are "social convention, NOT a CI-enforced gate", line 77) with four sentences:
1. Roles by login: the owner of the repository and of design rulings is `ironbelly`; maintainers are `clayphi` and `IB-JonathanB`.
2. A question to a named person is answered in writing; silence is never a yes. A design or a deletion of someone else's merged work waits for that person's written yes.
3. A design PR, and a PR that deletes code merged in the last 30 days, is merged by someone other than its author.
4. Work that others could collide with is pushed as a draft PR or an issue comment within a day.
Plus one line in `.github/PULL_REQUEST_TEMPLATE.md`: "Reverses: none, or the PR or decision this replaces, with the author's yes." Finish issue 290 (open, assigned to Clay) with the same text, so the rule has an owner who wrote it.

## Cited facts
1. The team runs on trust and bot review, by design: of the last 60 merged PRs, 51 were merged by their own author (29 `clayphi`, 22 `ironbelly`) and none has a human APPROVED review (`gh pr list --repo IronbellyOrg/IronClaude --state merged --limit 60`). A gate on every PR changes how the owner works as much as Clay.
2. Both maintainers' accounts exist and the third, `IB-JonathanB`, has maintain (`gh api .../collaborators`); there are three people. A lightweight written agreement is how this repo already governs: CONTRIBUTING.md:77-79 states a rule as "a social convention agreed by maintainers, NOT a CI-enforced gate".
3. The miss was not a search miss. Issue 655 cites 13 related items (#331, #450, #447, #448, #485, #548, #584, #591, #339, #423, #444, #442, Coder 477) and says "replaces #450" (FULL-REPORT.md section 8 and section 9). A "Related work" section or a stop-on-overlap check in `/sc:issue` would have been filled in and passed.
4. What was missed was unpushed or in another repository: the zero-setup plan (local), Coder issues 515 and 516, the owner's decisions in memory files (FULL-REPORT.md section 1 item 3). No search, scan or template section reaches those; only the owner publishing them does. An overlap scan (`/sc:overlap`) that the coordinator ran by hand took eight analyst files (FULL-REPORT.md "Source files").
5. The login `ironbelly` is shared by the owner and every session on the owner's host (FULL-REPORT.md section 1 item 7). A CODEOWNERS approval by `ironbelly` therefore does not prove a person approved. The enforcement the package promises is weaker than it looks.
6. Claim already stops on the one thing it can check: `refs/claim.md:42` "Assigned to anyone other than the current login -> STOP". Issue 450 was assigned to `ironbelly`; Clay did not claim it.
7. The 2026-10-22 onboarding rule (issue 290) says "not to create new skills or commands yet". A new `/sc:overlap` command (section 11 item 8) contradicts it.
8. CODEOWNERS paths in section 11 item 3 (`issue_watch/`, `docs/designs/`, the sc-issue skill) are exactly the paths of open work now (PRs 686, 690, issue 689); one admin as sole approver makes the owner the queue for that work. A 24 hour timer (item 7) is not something GitHub can enforce.
9. Issue 290 is open and assigned to `clayphi`: the natural home for the written rule, and it gives its author ownership of it.

## Cost
Estimates (mine; none measured): one CONTRIBUTING.md paragraph and one PR template line, 30 to 45 minutes in one PR; finishing issue 290 with the same text, 1 hour; no admin setting, no new command, no CI job, no recurring step except one line per PR.

## Risk
- An agreement can be ignored; nothing stops a self-merge (master stays unprotected, `gh api .../protection` 404). The 2026-10-22 verbal rule (issue 290) shows a rule can sit unwritten for a month.
- Silence is covered only by a sentence. If the named person does not answer, the author again has no written way to proceed or to stop.
- The owner's unpushed work stays invisible unless the owner pushes it; the agreement asks the owner to, and a rule on the owner is easy to skip.
- No audit trail of rulings beyond the issue comments they happen in.

## What it gets right
- It fixes the two causes the evidence supports: no definition of "owner" (FULL-REPORT.md section 10 item 3) and no rule that silence is not consent (item 4 of section 1).
- It is proportionate: three maintainers, 51 of 60 merges self-merged, no gate today. Gates added to the area under active build (`issue_watch/`, `docs/designs/`) would slow the work they are meant to protect.
- It does not claim to detect what no check can see (local plans, other repositories).
- It avoids a new command that the 2026-10-22 rule says not to build, and avoids a CODEOWNERS approval whose value is undermined by the shared login.
