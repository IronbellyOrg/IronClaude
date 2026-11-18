# Round 1: advocate for Variant 2 (proposal B, one actuator)

Written 2026-11-14. Advice only. Sources read: `00-state-machine-and-failure-modes.md`, the three variant files, `diff-analysis.md`, and in code: `src/superclaude/cli/issue_watch/predicates.py` (`approval_of`, `unchanged_since`, lines 185 to 259), `github.py` (grep: `EVENTS_JQ` line 54, `fieldValueByName(name: "Status")` line 95), `docs/designs/issue-watcher.md` (grep: D2 line 44, NG-2 line 70), `src/superclaude/core/WORKER-CONTRACT.md` (lines 128 to 137 and grep for WC-16), `~/.claude/skills/sc-issue-protocol/templates/launch-prompt.md` (grep: line 23). Not read, so UNVERIFIED where relied on: `merged-requirements.md` (sections 2.3 and 6.8), `observe/` code, the `#409` release gates.

## 1. Position summary

The owner offered two ways out: "safeguards and checks" or "the final instructions that trigger anything of consequence can only come from a single source and all others are ignored". B is the second option taken literally: every channel, GitHub or Orca, only produces an input, and one process, the coordinator that owns the issue, is the only thing that ever tells the governed agent to proceed, after a locked helper has written one approval record. That removes double start by structure rather than by every actor agreeing on a shared claim, and it leaves the built watcher untouched.

## 2. Steelman of the opposing variants

**Variant 1 (A), the strongest form.** A is the only design in which no single process is a point of failure: "Strength: progress does not depend on any single process being up." It honours the owner's "approval can happen either on GitHub or in Orca" most literally, because each channel can act by itself, and it even keeps the in-session `approved` the launch prompt offers today (`launch-prompt.md` line 23: "A human approves by replying `approved` in this session"). Its core mechanism is not invented: it reuses the watcher's proven write-ahead rule, "write the entry as `pending` and fsync it before doing anything else (the watcher's write-ahead rule, `issue-watcher.md` 7.4 transition T-4)". It is also the most candid variant about its limits ("Not solved", "a forged marker also suppresses").

**Variant 3 (C), the strongest form.** C puts the authority in the one place that is durable, public, server-timestamped and already parsed by tested code: a GitHub label event, whose id is unique. The existing `approval_of` already checks exactly what an approval needs: `approval.actor_type != "User"`, bot logins, `approval.actor_id not in approvers`, and ordering (`predicates.py` lines 216 to 229). Because Orca writes through and then reads back, "the write-through and the read-back are the same record", so GitHub and Orca can never disagree about whether approval happened. Revocation is a label removal, whose actor is readable, which is stronger than any Status move. Its audit trail "is public and in one place". And its proposed read-only stage-status verb (U-008) means the coordinator runs the same code as the watcher instead of re-describing it in a prompt.

## 3. Strengths claimed for B

1. **Single source, literally what the owner asked for.** "Exactly one process may send the instruction that moves the governed agent past the plan boundary or starts any later stage: the coordinator that owns that issue. Every approval, from any channel, is only an input the coordinator validates." A duplicate needs two senders; B has one.
2. **The watcher is out of the race and stays as built.** "It never messages the coordinator or the agent. The coordinator reads GitHub itself at each wake, so the watcher is out of the race entirely." This keeps the owner's recorded decision D2: "The poller never assigns, comments or moves Project items" (`issue-watcher.md` line 44) and NG-2 "no GitHub write" (line 70). Neither D2 nor NG-2 needs reopening.
3. **The one-record rule is enforced by code, not by an LLM instruction.** "through a small CLI helper that takes a per-issue lock and refuses a second row for the same (issue, stage, plan version)", and "the helper must enforce the one-row rule mechanically rather than by instruction." This is the same write-ahead shape A borrows from the watcher, applied to one writer instead of three.
4. **The bare `approved` is removed, closing the self-approval hole.** "the agent continues only on a line `approved <approval-id> plan-sha256=<hex>`, recomputes its plan file's hash, refuses a mismatch and a bare `approved`". Today any text in the session, including text the permission-free agent produces, can satisfy `launch-prompt.md` line 23. A keeps that path open; B and C close it.
5. **Both channels are treated alike.** A GitHub approval and an Orca approval each become one row with `channel`, `approver` and `evidence (label event id, Orca message id or typed line)`. Unlike C, an Orca approval does not depend on GitHub being reachable or on GitHub's event lag (C: "how long GitHub's events list lags is UNVERIFIED").
6. **Echo is a no-op by matching, not by trusting a marker.** "A GitHub change that matches an existing row is a no-op." The row lives in a local locked store; a forged GitHub marker cannot make the coordinator skip a real approval it has not yet recorded, and cannot create a start by itself.
7. **Stale views are rejected by version.** "The TUI message carries the plan version and record version; the coordinator rejects a stale one", and "an approval made against the stale view is rejected by version, never doubled."
8. **Backward moves never auto-restart.** "It never restarts by itself; a later forward move needs a new row."
9. **Smallest change to built code.** "the watcher and observer stay untouched until the TUI release."

## 4. Weaknesses identified in A and C

**A (Variant 1)**

1. **Three actuators, one of them the agent itself.** A says so: "In-session path: the permission-free agent is itself an actuator and can approve itself. Not solved." With permission checks off and issue text steering the agent, this is the worst F8 outcome of the three.
2. **It reopens a recorded owner decision.** "Watcher stage handler ... reverses design decision D2 and non-goal NG-2 (the watcher would post comments and type into sessions)" against D2 line 44 and the NG-2 test "over every argv and GraphQL constant".
3. **The lock only works inside one store.** "Across two stores (two hosts, or a restored backup) only the marker comment protects, and two actors can both post within one polling window." A's guarantee is "one intact store per host and login", and it is shared by three writers.
4. **Echo suppression is forgeable.** "A marker written by any session on the host's login is trusted, so a forged marker also suppresses." A forged marker can block a real approval.
5. **Many stoppers.** "Every actor sees the level disagree and may send a stop; stops must be idempotent." Three actors deciding to stop is three more chances to disagree.
6. **Highest cost.** "three actors implementing one protocol, the watcher gaining GitHub writes and session typing".

**C (Variant 3)**

1. **It contradicts itself on accounts (X-002).** "the coordinator applies the label on GitHub as the host's `gh` login" versus "C is only safe with a separate approver account whose token the host's sessions do not hold, which also means the coordinator could not write through for the person". Either the Orca channel works or the authority is verifiable; not both.
2. **Orca approvals are hostage to GitHub.** "If the read-back does not show the event yet (GitHub lag), it waits for the next wake" and "Every approval depends on GitHub being reachable and readable". The owner asked for Orca as an equal channel.
3. **Write-through is indistinguishable from forgery.** "the record's actor is the host's login, so a write-through approval cannot be told apart from a forged one." Since GitHub is the sole authority, this is, as C admits, "sharper here than in B".
4. **No Orca approval while the coordinator is down.** "An Orca approval cannot be made while the coordinator is down unless the person goes to GitHub."
5. **Unverified GitHub behaviour carries the design.** "whether GitHub records a second `labeled` event is UNVERIFIED"; events lag UNVERIFIED.

## 5. Concessions (genuine weaknesses of B)

1. **B stops when the coordinator stops.** "Progress stops while the coordinator is down." And the coordinator is not built: no coordinator is attached to watcher or claim sessions, and WA-07 and SW-13 are deferred (shared facts table; `merged-requirements.md` UNVERIFIED by me). B leans on A-001 harder than C and much harder than A.
2. **B's F2 claim about the Orca mailbox is overstated.** B says "Orca approvals wait in the Run mailbox (replayed until acknowledged)". An approval typed in the coordinator session cannot be made while that session is down, so only a future TUI message could wait in a mailbox, and whether such a message reaches a Run mailbox at all is UNVERIFIED.
3. **The delivery path B cites may forbid itself.** B says "type one line into its waiting prompt (WC A3 rules)". WC A3 is the rule for re-typing a coordinator answer to a supervised worker, and its input veto says "never answer a person prompt" (`WORKER-CONTRACT.md` line 136). The governed agent is not a supervised worker, and its `Waiting for approval` prompt is addressed to a person. So either the A3 rules need a stated exception for this case, or B must take its second option, making the agent a supervised worker (SW-13, a redesign). This also hits A and C, which type into the session too.
4. **Reusing `unchanged_since` does not check what B says it checks.** B says the coordinator checks "that the plan comment was not edited after the label (reusing the watcher's `approval_of` and `unchanged_since` rules)". But `unchanged_since` checks "every comment not authored by ``own_login``" (`predicates.py` lines 245 to 255). The coordinator posts the plan comment as the host's login, so the plan comment is skipped entirely. The plan hash still protects the file the agent runs, but the comment text the reviewer read is not checked. A new check is needed. `approval_of` also requires a trigger label event and a `store_created_at`, so it needs a stage variant before reuse. Both points apply equally to A and C.
5. **B's revocation trigger is weak.** B's F5 is triggered by "moved backwards", which in practice is a Status move whose actor no code reads (`github.py` reads only `fieldValueByName(name: "Status")`). C's "Removing the label (actor readable) is the revocation" is better, and B should adopt it.
6. **F8 is not solved on one login.** "on a single shared login a permission-free agent can apply that label too", and "A GitHub approval with no row is accepted as new". A forged label by the agent becomes a real row. B's mitigation needs a second account or switching the GitHub channel off until FU-6.
7. **The record is private.** B's truth is a local ledger; GitHub is a mirror. C's public, single audit trail is a real advantage for anyone reviewing later.
8. **The coordinator is an LLM.** The helper enforces one row, but the reading, matching and delivering around it are prompt behaviour. B's correctness depends on that protocol being followed.
9. **Discovery of a newly claimed issue is open** (`worktree.json` or Orca's worktree list, UNVERIFIED which is reliable).

## 6. Shared assumptions

- **A-001: ACCEPT.** Every design needs an owning coordinator, and B needs it most because it is the only actuator; it is not built and must be scoped (who opens it, how many issues it holds) before any of this is built.
- **A-002: QUALIFY.** Typing one line into the agent session is the shared delivery path, but WC A3's input veto ("never answer a person prompt") and its supervised-worker scope mean it is not covered by existing rules; it needs an explicit exception, a verified Orca permission, or the SW-13 supervised-worker route.
- **A-003: QUALIFY.** It holds only if each next-step chain names one fixed plan file and the launch prompt states exactly which bytes are hashed; the plan reply on GitHub must carry the same hash so the reviewer, the coordinator and the agent agree.
- **A-004: QUALIFY.** The substitution is forced by the code: the watcher reads label event actors (`EVENTS_JQ`) but only the current Status value, never who set it; the owner must accept the label as the signal or someone must prove the Status actor is readable.
- **A-005: ACCEPT.** B needs standing `issue-write` grants for plan reply, mention, label and Status on every pipeline issue; the per-item grant table shape in section 6.8 is UNVERIFIED by me and will need a pipeline-wide form.
- **A-006: QUALIFY.** No design survives a dead waiting session; B should treat a dead or missing session as "approval recorded, not delivered" and report it to the person, never relaunch by itself, and the durable fix is the supervised-worker route.

## 7. Per-point verdict table

| point | superior | one-line reason |
|---|---|---|
| S-001 | none/owner | All three share the same section skeleton by brief. |
| C-001 | V2 | One actuator answers the owner's "single source" directly; V3 also has one, but gates it on GitHub read-back. |
| C-002 | V2 | A locked local row works for both channels without GitHub lag; it should carry C's label event id as its evidence key. |
| C-003 | V3 | Same as B (watcher unchanged) plus a read-only verb so the coordinator runs the watcher's tested code, not prose. |
| C-004 | V2 | Removing bare `approved` closes self-approval; V3 does the same, V1 keeps the hole (tie V2 and V3). |
| C-005 | none/owner | V1 keeps progress alive with no coordinator; V2 and V3 trade that for safety; this is the owner's liveness versus duplicate-risk call. |
| C-006 | V2 | Record, instruct, then mirror needs no GitHub round trip and has no account contradiction, unlike V3's write-through. |
| C-007 | V3 | No echo by construction is cleanest; V2's row match is equally effective in practice; V1's marker is forgeable. |
| C-008 | V3 | Label removal has a readable actor; V2's backward-Status trigger does not, though V2's never-auto-restart rule should be kept. |
| C-009 | V2 | Only V2 names the supervised-worker alternative, which the WC A3 person-prompt veto may require. |
| C-010 | V2 | Fewest changes to built code; no watcher writes, no required second account. |
| X-001 | V2 | V2 and V3 keep D2 and NG-2; V1 needs the owner to reverse a recorded decision. |
| X-002 | V2 | V2 has no write-through, so it avoids V3's account contradiction (it still shares the single-login forgery limit). |
| X-003 | none/owner | All three substitute a label for the Status move; only the owner can accept that. |
| A-001 | none/owner | Shared and unbuilt; V1 depends on it least, but no design is complete without it. |
| A-002 | V2 | Shared risk; V2 at least offers the supervised-worker route that avoids typing into a person prompt. |
| A-003 | none/owner | Shared; the plan-file definition is an owner or design decision. |
| A-004 | none/owner | Shared substitution; owner decision. |
| A-005 | none/owner | Shared grant shape; all three need it. |
| A-006 | none/owner | Shared; no variant handles a dead session, and V1's multiple actors make a restart riskier. |

## 8. Neutral recommendation

Recommend a merge with B as the base: B's single actuator, locked approval-record helper and hash-only launch line, plus C's read-only stage-status verb (U-008), C's label removal as the only revocation signal, and the label event id as the row's evidence key, with the GitHub channel limited to a second approver account or switched off until FU-6. Confidence 70 percent, because it is the only shape that meets the owner's single-source wording without reopening D2 or depending on GitHub for Orca approvals, but it rests on an unbuilt coordinator and an unconfirmed delivery path (A-001, A-002).
