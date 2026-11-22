# Round 2 rebuttal: OURS (Variant 1) on D10

M = /home/coder/.cache/ic-snap-20261120/master, A = .../pr-a, W = /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb. "D:n" = line n of M/docs/designs/orchestrator.md. All citations re-read this round.

## (1) Responses to Clay's Round 1 criticisms

1. Clay strength 1 (the poll reaches a claim session, not the coordinator): CONCEDED in substance. In OURS the poll never signals the coordinator; the coordinator pulls. Partial counter: the coordinator's own loop is `orca orchestration check --wait ... --timeout-ms 300000` (M WORKER-CONTRACT.md:101) and runs a sweep "after every wake or timeout" (:110). So the pull already fires every 5 minutes at most. What is missing is one written rule: "on each timeout, read `dispatch.json` for new `claimed` entries". The adoption bullet says only "at each gate or wake" (W WORKER-CONTRACT.md:295, 299). UNVERIFIED that the master text reads the store on a timeout; I read the sweep bullet and it lists `worker-list`, the prompt-wait listing and contract `stat`s, not the claim store.
2. Clay strength 2 (mailbox reaches a busy session) and the A-001 claim that a loop in `check --wait` cannot see a file: TRUE that a file cannot wake the wait. FALSE as a conclusion. The wait is bounded: 300000 ms for the coordinator (WC:101) and "at most 240000" for Clay's own orchestrator (D:572, D:748). Clay's wave 5 already lists "the state files" among its inputs (D:571). Reading `wakes/` or `dispatch.json` on a timeout costs at most 4 to 5 minutes of latency. That is the same order as the poll cadence `*/5 * * * *` (D:120), so the mailbox buys little where the poll itself is slow. D:112's sentence "a typed line cannot reach a session busy for hours" is right, but it does not prove the mailbox is needed; the bounded wait already is a second channel.
3. Strength 3 (checkable delivery): CONCEDED. OURS has no ack. Clay's ack and unread mark (D:112; A `wake.py:964-981`) is the best single idea in the paper.
4. Strength 4 (typed line is existing practice): CONCEDED for an idle report session. It remains unproven for the orchestrator (D:1233, D:1263) and every fixture for it is `_assumed_shape` and UNVERIFIED (A tests/issue_watch/fixtures/_assumed_shape/).
5. Strength 5 (rule on every channel): CONCEDED as an improvement. D:155 and D:234 widen D3.
6. Strength 6 and 7 (no tokens, starts a down coordinator): CONCEDED. OURS spends a model session per claim and nothing starts while the coordinator is down.
7. Weakness 2 (decision 6 overreach): CONCEDED already (Round 1). Weakness 4 (Q36 is approval latency): CONCEDED; the orchestrator confirmed it. Weakness 5 (`orca_term.py:3` is an in-file note, not a repo rule): CONCEDED as a rule, but it still states the design intent of the file's owner.
8. Weakness 3 and 6 (both lines have UNVERIFIED fresh-terminal behaviour and both are unproven live): CONCEDED. Not a differentiator.
9. Clay's process note: Clay ran `gh issue view 516` against `IronbellyOrg/Coder`, outside the stated `--repo IronbellyOrg/IronClaude` rule. Read-only, no harm; flagged for the record only.

## (2) Updated assessment

- Move C-001 to Clay (65%), C-006 to Clay (55%). Keep C-004 and C-005 with OURS (65%, 75%). C-002, C-007, C-008, U-003, U-004: Clay as before.
- A new fact changes the picture: PR 686's poll does not call `build_claim_prompt` (grep of A `src/superclaude/cli/issue_watch/*.py` returns nothing for it). In Clay's line the poll claims nothing and the orchestrator claims. So D10 is partly entangled with the "who claims" decision; the transport can only be chosen cleanly if the wake carries issue numbers and leaves the claim to the receiver.
- A-001 final: QUALIFY. Push is needed only for latency below the 4 to 5 minute wait and for an idle person-opened session that is not inside any loop. For a looping session, a read of the file on timeout is enough.

## HYBRID: is it the best outcome, and what is separable

Proposal: durable wake file as truth; mailbox and typed line as optional nudges; integer-only launch for session start; no listener.

- I support it as the best outcome, with two conditions. (a) The file plus ack plus unread mark are required; the nudges are optional and can be dropped without losing a wake (A `wake.py:964-981`). (b) The loop must read the wake directory on every timeout, written into the orchestrator skill and the coordinator duties.
- Typed line: keep only as a nudge to an idle prompt, because a person-opened session sitting at its prompt is not in any `check --wait`. For a looping session it adds risk without benefit. Mailbox: keep optional behind U5.
- Integer-only launch for start: partly workable. `launch_argv` accepts only `PROMPT_PATTERN` (`/sc:issue --claim <n> --pipeline none`, M `launch.py:33`, :94-118). A hybrid start would need a second fixed pattern for `/sc:orchestrator --wake <wake_id>`, which is an edit to the one code path I praised. UNVERIFIED whether `orca agent launch --agent claude` produces a session with the ccsession tag that Clay's lookup needs (`orchestrator-<short>-<n>`, U25, D:1283). If it does not, Clay's `terminal create` plus `ccsession` start stays.
- Separable from the contested trigger and plan-hold rules: the envelope (`schema`, `wake_id`, `target`, `poll.*`, `attempt`; D:167-184), atomic write and mode 0600, the ack file and its three item buckets (D:229), `build_wake_line` and the mailbox subject, the resend and unread logic, the session lookup. Not separable: `assigned[]` (it encodes the assignment-only trigger, D:188), `plan_requests[]` and its `missing` tokens (D:185, the plan hold), `target.resume` and routing (D:318, section 5.7). A hybrid should ship the envelope with `assigned[]` as a plain list of numbers and defer `plan_requests[]`.

## (3) New evidence not used in Round 1

1. Bounded waits: M WORKER-CONTRACT.md:101, :110; D:571, D:572, D:748.
2. PR 686 claims nothing in the poll (no `build_claim_prompt` call in A issue_watch), which shows the two lines differ on who claims, not only on transport.
3. The adoption bullet (W WORKER-CONTRACT.md:295) reads the claim files only through `dispatch.json` and the issue folder "in the checkout that ran the claim", so a coordinator in another checkout reads a different tree. UNVERIFIED how it finds that checkout; a wake file under the orchestrator repo (D:151) avoids that question.
