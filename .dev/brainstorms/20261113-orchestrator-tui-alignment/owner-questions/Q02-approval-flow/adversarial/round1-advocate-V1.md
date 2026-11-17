# Round 1: advocate statement for Variant 1 (proposal A)

Written 2026-11-14 by the Variant 1 advocate. Advice only. Sources read: `00-state-machine-and-failure-modes.md`, the three variant files, `diff-analysis.md`. Code checked: `src/superclaude/cli/issue_watch/predicates.py` (functions `is_intended_owner` line 162, `approval_of` line 185, `unchanged_since` line 237, `project_check` line 262 exist), `src/superclaude/cli/issue_watch/record.py` (exclusive non-blocking `fcntl.flock` at line 403, directory fsync at lines 310 to 313 and 378), `docs/designs/issue-watcher.md` (D2 at line 44, NG-2 and NG-3 at line 70, T-4 at line 482), `src/superclaude/core/WORKER-CONTRACT.md` (sweep "at most once every 5 minutes" at line 109; A3 `orca terminal send` at line 134), `~/.claude/skills/sc-issue-protocol/templates/launch-prompt.md` line 23. `github.py` `PROJECT_ITEMS_QUERY` and `EVENTS_JQ` contents: UNVERIFIED by me (taken from the shared facts file). Whether GitHub exposes the actor of a Project Status move: UNVERIFIED.

## 1. Position summary

The real duplicate-work guard in every one of the three designs is the same thing: one exclusive, write-ahead claim per (issue, stage, plan version), taken before any instruction is sent. Proposal A states that guard as the design itself, reuses the watcher's already-built `flock` plus fsync store discipline to enforce it mechanically, and is the only variant where a GitHub approval still makes progress when no coordinator is running.

## 2. Steelman of the opposing variants

**Variant 2 (B), at its strongest.** B answers the owner's second option literally: "the final instructions that trigger anything of consequence can only come from a single source and all others are ignored." It has one actuator ("Exactly one process may send the instruction ... the coordinator that owns that issue"), so F1 and F7 are prevented "by structure", not by a race between peers. It leaves the built watcher untouched ("None; the watcher stays as built (WA-01 to WA-05 unchanged)"), which honours the owner's recorded D2 ("The poller never assigns, comments or moves Project items", `issue-watcher.md` line 44). It closes the self-approval hole in the agent's own session by accepting only `approved <approval-id> plan-sha256=<hex>`. It recognises that an LLM coordinator cannot be trusted to keep a one-row rule by instruction: "the helper must enforce the one-row rule mechanically rather than by instruction." Its revocation is conservative ("It never restarts by itself"). Its cost of a coordinator outage is delay, not harm: "Cost: delay".

**Variant 3 (C), at its strongest.** C makes the single source of truth public and server-stamped: "GitHub gives the label event a unique id; that id plus the plan version is the idempotency key." An id assigned by GitHub cannot be duplicated by two local stores, which is the one failure A admits it cannot close ("Across two stores ... only the marker comment protects"). Because an Orca approval is written to GitHub and then read back, there is "No echo problem by construction (the write-through and the read-back are the same record)". The audit trail is in one place anyone can read. It proposes a read-only verb so the coordinator runs the same `approval_of` and `unchanged_since` code the watcher runs, instead of re-describing those checks in prose.

## 3. Strengths claimed for Variant 1 (A)

1. **The claim is enforced by code that already exists, not by an LLM.** A says "take the file lock, look for the key, and if absent write the entry as `pending` and fsync it before doing anything else (the watcher's write-ahead rule, `issue-watcher.md` 7.4 transition T-4)". That discipline is built: `record.py` takes an exclusive `fcntl.flock` (line 403) and fsyncs the state directory (lines 310 to 313, 378). B's "small CLI helper that takes a per-issue lock" is the same mechanism with one caller; A specifies it as "A small CLI helper does this so all three actors share one implementation."
2. **Progress without a single point of failure.** "GitHub approvals still progress: the watcher handler starts the stage alone. The coordinator, when it returns, finds the key and adopts the state" (F2). Neither B nor C can start anything while the coordinator is down, and no coordinator is attached to watcher or claim sessions today (shared facts, "Coordinator ... Not built (WA-07 and SW-13 are DEFERRED")).
3. **The invariant is stated as a checkable property.** "For each (issue, stage, plan version), at most one `stage.json` entry leaves `pending`, and no actor starts a stage before that entry is fsynced." This is testable with the same style of tests the watcher already has for T-4.
4. **It is honest about its scope.** "The guarantee has the same scope as the watcher's own: one intact store per host and login", and it names the forged-marker weakness itself (U-006: "a forged marker also suppresses").
5. **It keeps today's human path.** The launch prompt today says "A human approves by replying `approved` in this session" (`launch-prompt.md` line 23). A keeps that path and puts it behind the same claim, so no existing user habit is removed.
6. **Stale views cannot double-approve.** "A TUI approval must carry the record version it showed; the claim fails if the key already exists" (F9).
7. **Plan drift is covered by the key, not by a separate rule.** "Key includes the plan version; a changed plan is a new key that needs a new approval" (F4).

## 4. Weaknesses identified in B and C

**In B:**

1. **Everything stops when the coordinator stops.** B admits "Nothing starts" (F2) and "Progress stops while the coordinator is down." The coordinator is a person-opened LLM session that does not exist for this flow yet (A-001). A night-time GitHub approval waits until a person reopens it.
2. **B depends on a component that is not designed.** B's own unresolved list includes "how the coordinator discovers a newly claimed issue (it can read `.dev/issues/<N>/worktree.json` or Orca's worktree list; which one is UNVERIFIED as reliable)" and the delivery path is either typing into a session it did not start or "a redesign; SW-13", which is DEFERRED.
3. **Instruct before mirror leaves a window.** B's Orca flow is "writes the row, delivers the line to the agent, then mirrors to GitHub". A crash between delivery and mirror leaves GitHub showing "In review" while work runs; reconciliation repairs it only at the next wake, which needs the coordinator up again.
4. **It removes a working path.** "A person who types in the agent session is told to approve through Orca or GitHub" changes current behaviour in `launch-prompt.md` line 23. That is a safety gain, but it is a regression in convenience the owner has not been asked about.
5. **The single source is still forgeable on one login.** B concedes "on a single shared login a permission-free agent can apply that label too" and that same-host typing into the coordinator terminal "stays a residual risk". Single actuator does not mean single authoriser.

**In C:**

1. **C contradicts itself (X-002).** "the coordinator applies the label on GitHub as the host's `gh` login" versus "C is only safe with a separate approver account whose token the host's sessions do not hold, which also means the coordinator could not write through for the person". With one login the write-through works and the authority is forgeable; with two logins the authority holds and the Orca channel stops working.
2. **The Orca channel becomes a slow proxy.** "If the read-back does not show the event yet (GitHub lag), it waits for the next wake; it never acts on the Orca input itself." So an Orca approval waits up to one wake plus GitHub's lag (UNVERIFIED duration). The owner asked for two real channels; C keeps one and routes the other through it.
3. **Every approval needs GitHub up.** "Every approval depends on GitHub being reachable and readable." A local outage of GitHub API access blocks even an approval typed by the person at the coordinator's terminal.
4. **Key correctness rests on unverified GitHub behaviour.** "whether GitHub records a second `labeled` event is UNVERIFIED" (F7). C does consume per (issue, stage, plan version), which is in effect A's key, so the event id is evidence rather than the real guard.
5. **Same single point of failure as B.** "An Orca approval cannot be made while the coordinator is down unless the person goes to GitHub."

## 5. Concessions (genuine weaknesses of A)

1. **A breaks an owner decision.** "reverses design decision D2 and non-goal NG-2 (the watcher would post comments and type into sessions)". D2 and NG-2 are recorded and tested (`issue-watcher.md` lines 44, 70, 555 to 556). This is the biggest cost and needs an explicit owner decision (X-001).
2. **Three actuators means three places to get the protocol wrong.** "Highest build cost: three actors implementing one protocol". A shared helper reduces this but every actor must still call it before acting, and the coordinator and agent are LLM sessions that can skip a step.
3. **The permission-free agent becomes an actuator.** "In-session path: the permission-free agent is itself an actuator and can approve itself. Not solved." This is worse than B and C, which remove the in-session path. On a host where launched sessions run with permission checks off and read issue text anyone can edit, this is a real prompt-injection route to an unauthorised start (F8).
4. **The local claim is per host.** "Across two stores (two hosts, or a restored backup) only the marker comment protects, and two actors can both post within one polling window." C's server-assigned id is stronger across hosts.
5. **Echo suppression is forgeable.** "A marker written by any session on the host's login is trusted, so a forged marker also suppresses" (F3).
6. **It does not satisfy the owner's "single source" option**; it is the "safeguards and checks" option. If the owner prefers single source, A is the wrong shape.

## 6. Shared assumptions

- **A-001 (a coordinator exists and owns each issue's agent): QUALIFY.** A needs a coordinator to post the plan and serve the Orca channel, but a GitHub-approved stage can run without it; B and C cannot run any stage without it. Who opens it and how many issues it holds must be decided before any variant is built.
- **A-002 (something other than the person may type into the waiting session): ACCEPT.** All three deliver this way; `WORKER-CONTRACT.md` line 134 shows `orca terminal send` used for workers the coordinator supervises, but typing into a session the coordinator did not start is UNVERIFIED.
- **A-003 (one stable plan file, hashed identically): QUALIFY.** True and load-bearing for F4 in all three; the plan path and the hash routine must live in one shared helper and be recorded in the plan reply, not recomputed by prose instructions.
- **A-004 (owner accepts a label event as the approval signal): QUALIFY.** The substitution is forced because no code reads who moved the Status (per the shared facts; the GitHub API question is UNVERIFIED); the owner must accept it or someone must prove the Status actor is readable.
- **A-005 (standing issue-write grant for the coordinator): ACCEPT.** All three need it and the grant shape is new; A needs more, because the watcher also writes.
- **A-006 (the agent waits alive for hours or days): QUALIFY.** All three assume it; a dead session must lead to escalation to the person, never an automatic relaunch, and a write-ahead `pending` entry (A) or row (B) is what stops a relaunch from becoming a second run.

## 7. Per-point verdict table

| Point | Superior | Reason |
|---|---|---|
| S-001 | none/owner | Identical section skeleton in all three by brief. |
| C-001 | V2 | One actuator is the owner's "single source" option and removes the agent and watcher as actuators. |
| C-002 | V2 | A locked, write-ahead local row is enforced mechanically and does not wait for GitHub; C's event id is better stored as evidence inside that row. |
| C-003 | V3 | Watcher stays write-free (honours D2) and the coordinator reuses `approval_of` and `unchanged_since` code through a read-only verb instead of prose. |
| C-004 | V2 | Removing the bare `approved` closes self-approval and B explicitly redirects the person; A keeps the F8 hole. |
| C-005 | V1 | Only A lets a GitHub approval progress with no coordinator running. |
| C-006 | V2 | Row then instruct does not depend on GitHub reachability or lag; C's read-back adds delay for no added safety on one login. |
| C-007 | V3 | No echo by construction is cleaner than tokens or row ids, though equally forgeable on one login. |
| C-008 | V2 | One stop, ask the person, never auto-restart is the safest rule; A lets every actor send stops. |
| C-009 | V2 | Only B names the supervised-worker redesign, which would replace typing into an unowned session. |
| C-010 | V2 | Smallest footprint: coordinator protocol, one helper, one template change; watcher untouched. |
| X-001 | V2 | B and C both keep D2 and NG-2; A needs the owner to reverse a recorded, tested decision. B listed as the representative. |
| X-002 | V2 | B has no internal contradiction on this point; C's write-through and verifiable actor cannot both hold. |
| X-003 | none/owner | All three substitute a label for the Status move; only the owner can accept that. |
| A-001 | V1 | A depends least on the unbuilt coordinator (GitHub path runs without it). |
| A-002 | V2 | B offers a path (supervised worker) that removes the dependence on typing into an unowned session. |
| A-003 | none/owner | All three rest equally on one stable, identically hashed plan file. |
| A-004 | none/owner | All three make the same substitution. |
| A-005 | V2 | B and C need the same coordinator grants; A also needs watcher write rights. B listed as representative of the smaller need. |
| A-006 | V2 | B's ack protocol (`ack <approval-id> applied|refused`) detects a dead session before a row is marked done; A and C have no ack. |

## 8. Neutral recommendation

Setting advocacy aside: recommend Variant 2 (B) as the base, merged with C's label event id recorded as evidence in the approval row and C's read-only stage-status verb, and with B's helper built on the watcher's existing `flock` plus fsync store code that A proposed reusing. Confidence 75%, because B is the only variant that gives the owner a single actuator without breaking D2 or contradicting itself, and its main cost (no progress while the coordinator is down) is delay rather than duplicate work.
