# Findings: issue 781 (contact agents beside the dashboard)

Checked 2026-11-24 against checkout a7ae3dd30 (branch ironbelly/Issuecleanup) and the live issue (open, created 2026-11-24T20:01Z, label enhancement, no comments, no sub-issues, no blockedBy or blocking links, no closing PRs).

## Verdict

**still-relevant.** Nothing in the issue is built or started, and it is a design question plus an offer, so it is neither done nor in progress.

Evidence:
- No file under `src/`, `docs/` or `tests/` mentions "contact agent" (searched with grep, no hits). No PR search hit for it either.
- `src/superclaude/cli/observe/adapter.py:32-48` forbids the verbs `send`, `ask`, `reply`, `dispatch`, `run-use`, so the observer cannot carry a person's message. This confirms the issue's step 2: any relay has to sit outside the observer.
- `docs/user-guide/observer.md:154` (local host only), `:156` (never approves, retries, terminates, dispatches, merges or messages) and `:154-156` "Not built" list match the issue's quotes.
- `src/superclaude/core/WORKER-CONTRACT.md:294` still says each project has one coordinator that owns every watcher-claimed issue, the rule the issue says it respects.
- `src/superclaude/cli/observe/export.py:101-102,158-159` keeps question text out of stored output (ids, times, counts only). Whether that feed can answer "where does this stand?" is untested. UNVERIFIED.
- Every issue the body depends on is still OPEN today: 727 (two-way dashboard, backlog), 757 (sweep outside the session), 770 (watcher hands claim to coordinator), 409, 604, 725, 706, 726, 777, 761.
- UNVERIFIED: the contents of the 727 routing design. The 727 body has no routing section yet, and the contact-agent comment (727 comment of 2026-11-24T18:14Z) only proposes the idea.
- UNVERIFIED: whether the wake path in 757 and 770 can carry a person's message. Both are open and unbuilt.
- UNVERIFIED: whether Ryan accepts the idea; the issue grants no approval and says so.

## Complexity and size

Complexity: medium. Size: M. The code is small (one skill and its tests), but the real work is an open design decision on routing, relay and ownership with several unfinished issues.

## Priority

P2. The issue itself says Medium (set by Clay); it blocks nothing shipped, and it cannot start before the 727 routing design and the 757/770 wake-path answer exist.

## Concrete next steps

1. Run `/sc:brainstorm` with Ryan on routing, relay, skill-or-agent, grouping and ownership; also decide whether to fold this into 727.
2. Read the 727 routing design once written, and check whether the 757/770 wake path can carry a person's message.
3. Specify the feed from `src/superclaude/cli/observe/adapter.py`, `collector.py`, `export.py` with the relay kept outside the observer.
4. Only after approval: `/sc:workflow` for a small trial plan, then `/sc:implement`, then a one-project comparison.

## Dependencies

Needs: 727 (routing design), 757 and 770 (message-carrying wake path), and a decision from Ryan. Blocks: nothing found. No formal GitHub dependency links exist.

## Related issues

727, 409, 604, 606 (closed per the issue body; UNVERIFIED here), 706, 726, 725 (separate scope), 777, 770, 757, 761, and IronbellyOrg/PrivateRepoF#515 (UNVERIFIED: not opened from this worker).

## Related PRs

PR 707 (merged issue watcher and standing coordinator, per the issue body; UNVERIFIED here). No open or merged PR addresses 781 itself.
