# Issue 722 live-read extracts

## Provenance
Producer-transcribed extracts, not a fresh reviewer fetch or a raw tool log. Source: successful `gh issue view 722 --repo IronbellyOrg/IronClaude --json number,title,body,comments,state,labels,url` on 2026-11-24. Returned metadata: OPEN, comments [], labels [], URL https://github.com/IronbellyOrg/IronClaude/issues/722. A later related-issue tool result emitted a shared GitHub rate-limit warning. This file cannot substitute for the required independent live-source check if that check is unavailable.

## Quoted completion and pick-up criteria
> The owner records in chat which solution is chosen (or a new one). Then either the dependent items (merge automation, coordinator autostart, real-repo watcher switch-on, the worker-binding flip) are unblocked with the chosen mechanism built and tested, or they are confirmed to stay off. If solution 1 is chosen: the agent account exists and is cut over on one host, the throwaway tests in the debate file pass (the login prints the agent account in a fresh shell and in an Orca session; an unapproved agent PR cannot merge; `gh pr merge --admin` and a push to master are refused; both review bots review an agent-authored PR; the claim writes work).

> Parked for human debate. Do not build anything yet. The owner decides whether any of this is wanted; there is no deadline. Read `X05/FINAL.md` for the full order of steps, the owner's one-sentence approval, and what an agent would do after it.

## Other observed evidence
Issue body describes one shared GitHub login, ironbelly, and proposes either two approval tiers plus a separate agent account, chat-only checks without a new account, continued manual merges with automation off, or an unevaluated GitHub App. It says nothing is decided or built and directly relates issues #717 (watcher) and #716 (coordinator). Local references are `.dev/brainstorms/20261120-pr686-unify/` and `.dev/brainstorms/20261122-owner-actions-debate/X05/`.

The successful PR #686 read returned CLOSED, mergedAt null and mergeCommit null. Its closing comment by ironbelly at 2026-11-23T01:45:37Z says: "Closing on the owner's go (2026-11-23). The merged issue watcher (PR 707) is the design; see the decision note on https://github.com/IronbellyOrg/IronClaude/issues/655. The branch is kept and nothing is deleted. Features of issue 655 that the merged plan does not cover are tracked in issues 716, 717 and 718."

These are extracts, not a claim of complete independent source coverage.
