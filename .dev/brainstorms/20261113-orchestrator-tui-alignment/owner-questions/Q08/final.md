# Q8 final: write the owner's direction-selection record, or rewrite #409's first acceptance criterion

Q8 is owner question 8 of the alignment spec. Issue #409 is the observer dashboard issue (`superclaude observe`, the read-only terminal view of Orca workers). Its first acceptance criterion says "A human selects the visual direction before production integration." AC-S is the observer project's reviewer check for that criterion: it looks for the owner's own dated direction-selection record, which does not exist yet. OB-nn ids are the observer's work items in the spec: OB-02 is that record, OB-08 is the correction pass on the #409 issue text (BC-18 is its proposed line for this criterion), OB-09 is release 3 (Decision Desk).

## Debate result

- Winner: proposal C, extended (the owner writes the record now and it covers every field the gate checks). Confidence 68 percent (mean of the advocates' verdicts: 65, 70, 70).
- Agreement: 3 of 3. The advocates for A and for B both chose C over their own proposals. Every debate point had a majority; three were unanimous.
- Deciding evidence (checked on 2026-11-14): the gate rule on master requires "a dated selection record written by the owner, never an agent" (`release-gates.md:22`), and the reviewer check lists eleven fields and says "No agent writes the record" (`acceptance-tests.md:70`). The owner's 2026-11-08 decision file says it was "Recorded by an Orca worker" (`owner-decisions-20261108.md:3`), so it cannot serve as that record. The gate also says the meaning of "production integration" has two readings, "both UNVERIFIED", and "Until the owner confirms one in the selection record, the stricter reading applies" (`release-gates.md:28-34`): only the record can settle it.

Proposal A (do neither now; let #409 say "not met as recorded"; write the record when release 3 is next). Strength: near-zero owner effort, and the issue becomes honest at once; it would write the release-3 fields when they are known. Weakness: release 3 has no date (it is deferred), so the record may never be written, the strict "production integration" reading stays in force meanwhile, and the "not met" line itself depends on a reading nobody has confirmed. Its advocate voted C, keeping A's interim line as a fallback.

Proposal B (rewrite criterion 1 to describe the staged selection, citing earlier decisions). Strength: the decision did happen (2026-11-08, before release 1 merged on 2026-11-11), and the project did follow a staged model. Weakness: changing the issue text leaves the gate rule and the reviewer check on master unmet, so a second repository change would be needed; the record it cites was written by an agent; and rewriting the criterion after the fact reads as moving the bar. Its advocate conceded all three and voted C.

Proposal C (the owner writes a one-paragraph record now; criterion unchanged). Strength: it is the instrument the gate itself names, in the owner's words, and it settles "production integration". Weakness as drafted: a three-item paragraph misses most of the eleven fields, and "met by the record" overstated the order of events, since the record is written after releases 1 and 2 shipped. Both are fixed in the merged answer.

## Final recommendation

Write the record now (one dated paragraph in your own words) and keep #409's criterion 1 unchanged. The paragraph covers every field the reviewer check lists, in brief: date, option (the staged direction, which still stands), who decided, where the statement lives, the defaults before and after questions are observed, the post-link choice and fallback date (both may say "deferred to release 3"), the stack confirmation, the command name `superclaude observe`, and your reading of "production integration". #409 then says: direction selected 2026-11-08 (staged), confirmed in the owner's record of that date, written after releases 1 and 2 shipped. If the record is not ready when the #409 correction pass posts, the honest "not met as recorded" line posts instead. Confidence 68 percent.

Single strongest reason: the gate on master accepts only an owner-written record and names it as the only place the meaning of "production integration" is settled; neither amending the criterion nor waiting gets that.

Equals the spec's recommended answer: yes, with additions. The spec says "write the record (one paragraph)"; the merged answer keeps that and adds the full field list, the honest status wording and the interim fallback line.

## What would change the answer

If the owner wants the observer's acceptance rules themselves changed (dropping the selection-record gate because the staged model replaced it), proposal B becomes right, but then the gate rule and reviewer check on master must be amended in the same change.

## Criticality rating

- Security or trust boundary: none
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: yes
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences: The record must be written by the owner in the owner's own words, and its central content (whether the staged direction still stands and what "production integration" means) is the owner's intent, which no file holds. An agent can recommend writing it but cannot answer it, because the gate forbids an agent-written record.

## Debate record

- Folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q08/adversarial/`
- fallback_mode: false (three advocates spawned in parallel as separate agents; merge by a merge-executor agent; depth quick, Round 1 only)
