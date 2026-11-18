# Round 1 statement: advocate for Variant 3 (proposal C, GitHub is the only authority)

Written 2026-11-14. Advice only. Sources read: `00-state-machine-and-failure-modes.md`, `variant-1-original.md`, `variant-2-original.md`, `variant-3-original.md`, `diff-analysis.md`, `src/superclaude/cli/issue_watch/predicates.py` (lines 160 to 280), `src/superclaude/cli/issue_watch/github.py` (lines 50 to 110), grep hits in `docs/designs/issue-watcher.md` (D2, NG-2, NG-3) and `~/.claude/skills/sc-issue-protocol/templates/launch-prompt.md` (line 23). Not read, so UNVERIFIED here: `launch.py`, `WORKER-CONTRACT.md`, the rest of `issue-watcher.md`, GitHub's event lag and duplicate-label behaviour.

## 1. Position summary

The owner offered two ways out: safeguards and checks, or "the final instructions that trigger anything of consequence can only come from a single source and all others are ignored". Proposal C is the only variant that takes the second option literally: one authority (a GitHub label event, read back), one actuator (the coordinator), and every other channel, Orca and the TUI included, is reduced to a way of writing that one record. Its price is latency on Orca approvals and an internal conflict over accounts (X-002) that I concede below.

## 2. Steelman of the opposing variants

**Variant 1 (A), steelmanned.** A is the only design in which no single process is a point of failure: "Strength: progress does not depend on any single process being up." A GitHub approval made at night still starts work through the watcher handler (F2), and the person keeps every way of approving they have today, including typing in the agent's own session, which is the only approval path that exists now (`launch-prompt.md` line 23: "A human approves by replying `approved` in this session"). It reuses a discipline already proven in the watcher, the write-ahead `pending` entry with fsync (`issue-watcher.md` 7.4, T-4), so its core lock is not new invention. It is also the most candid about its limits: "Across two stores (two hosts, or a restored backup) only the marker comment protects", and "a forged marker also suppresses".

**Variant 2 (B), steelmanned.** B gets the same single-actuator safety as C with fewer moving parts and no dependency on GitHub for Orca approvals. Its strongest ideas are mechanical: "a small CLI helper that takes a per-issue lock and refuses a second row for the same (issue, stage, plan version)", and its own warning that "the coordinator is an LLM session, so the helper must enforce the one-row rule mechanically rather than by instruction." It leaves the watcher exactly as built ("None; the watcher stays as built (WA-01 to WA-05 unchanged)"), handles the coordinator being down without losing Orca approvals ("Orca approvals wait in the Run mailbox (replayed until acknowledged)"), works whether or not the owner adds a second GitHub account, and alone names the real delivery alternative of making the agent "a supervised worker started by the coordinator (redesign; SW-13)". Its ack protocol (`ack <approval-id> applied|refused`) closes the loop that C leaves implicit.

## 3. Strengths claimed for C

1. **It is the owner's second option, stated as an invariant.** "A stage starts only after the coordinator has read back from GitHub an approval label event, by an allowed account, later than the unedited plan reply for that exact plan version, and has recorded that event id as consumed." In B, two sources can create the truth (an Orca message and a GitHub label both create rows; "A GitHub approval with no row is accepted as new"). In C, Orca input is never acted on: "it never acts on the Orca input itself."
2. **No echo problem by construction (C-007).** "the write-through and the read-back are the same record." A needs a marker token and admits forged markers suppress; B needs a row id carried in the mirror comment and a match rule. C has nothing to match, because there is only one record.
3. **A server-assigned idempotency key (U-004).** GitHub gives every label event an `id`; the watcher already projects it (`github.py` line 55: `EVENTS_JQ = "[.[] | {id, event, label: .label.name, actor_id: .actor.id, actor_login: .actor.login, actor_type: .actor.type, created_at}]"`). A key minted by GitHub cannot collide between two local stores, which is exactly A's unresolved "two-store duplicates" case.
4. **The actor is readable on the signal C uses.** `approval_of` already rejects an approval unless `approval.actor_type == "User"`, the login does not end in `[bot]`, and `approval.actor_id in approvers` (`predicates.py` lines 216 to 223). C uses that same signal for revocation too: "Removing the label (actor readable) is the revocation". B's backward-move trigger is less specific about which signal, with which readable actor, starts the revoke.
5. **Public, durable, single audit trail.** "The audit trail is public and in one place, which is its main strength." If the host dies, every approval ever given is still on the issue; under B the truth is a local ledger row and GitHub is only a mirror that may lag or fail.
6. **The watcher stays write-free (X-001).** "The watcher stays a claim trigger. It gains no post-claim logic." This keeps D2 ("The poller never assigns, comments or moves Project items", `issue-watcher.md` line 44) and NG-2 intact, unlike A.
7. **Checks are code, not prose (U-008).** "The coordinator may reuse the watcher's read functions through a new read-only verb (for example a stage-status read), so the label and edit checks are the same code." B says the coordinator reuses "the watcher's `approval_of` and `unchanged_since` rules" but does not say how an LLM coordinator runs them; C names the mechanism.
8. **Stale TUI is harmless (F9).** "a second write-through of the same label is a no-op for the coordinator." No record version needs to travel with the TUI message.

## 4. Weaknesses identified in A and B

**In A:**
1. **Three actuators is the opposite of what the owner asked to consider.** "Each channel keeps the right to start the next stage itself: the coordinator ..., a new stage handler in the watcher ..., and the governed agent". Every actuator must implement the protocol perfectly; one bug is a double start.
2. **It reverses recorded owner decisions.** "reverses design decision D2 and non-goal NG-2 (the watcher would post comments and type into sessions)". NG-2 is enforced by tests ("A test asserts no query constant contains `mutation` (NG-2)", `issue-watcher.md` line 556), so A also breaks shipped safety tests.
3. **Self-approval is built in.** "In-session: whoever types in the agent session, including text the agent itself produces." With permission checks off and issue text controlled by anyone who can edit the issue (`00-state...` row "Permission mode"), this makes the steerable agent an approver of its own plan.
4. **Its lock is local but its world is not.** "Across two stores ... two actors can both post within one polling window"; "GitHub comments have no conditional write, so it is not a lock."
5. **Highest cost.** "Highest build cost: three actors implementing one protocol".

**In B:**
1. **Two places can mint the truth, and they can disagree.** "The ledger row is the truth; the issue and the TUI are views of it." After an Orca approval B instructs the agent first and mirrors second ("writes the row, delivers the line to the agent, then mirrors to GitHub"). If the mirror write fails, the public record says "in review" while work is running, which is the owner's duplicate-work worry in another form: a second person sees "in review" on GitHub and approves.
2. **A GitHub approval without a row is new.** "A GitHub approval with no row is accepted as new." If the ledger is lost or the coordinator is restarted against a fresh ledger, a GitHub approval already acted on is accepted again. C has the same exposure for its consumed list (concession 4 below), so this is a shared gap, but B's design makes the local ledger the authority, which raises the stakes of losing it.
3. **The check mechanism is unspecified.** "reusing the watcher's `approval_of` and `unchanged_since` rules" with no verb named; an LLM restating those rules in prose is the risk B itself warns about for the one-row rule.
4. **Echo handling depends on a match rule.** "any GitHub state that matches a row is a no-op" requires the coordinator to parse its own mirror comments correctly every time; C has no such rule to get wrong.

## 5. Concessions (genuine weaknesses of C)

1. **X-002 is real and I cannot fully resolve it.** C says both "the coordinator applies the label on GitHub as the host's `gh` login" and "C is only safe with a separate approver account whose token the host's sessions do not hold, which also means the coordinator could not write through for the person". On today's single login, write-through works but a forged label from the permission-free agent looks identical. With a separate approver account, forgery is closed but the Orca channel can no longer write through, so C collapses to "GitHub only". The owner asked for both channels; C can honestly give both only by accepting the forgery risk, which B and A also carry.
2. **Orca approvals are slower and can fail to take.** "Orca approvals appear to 'not take' until GitHub returns the event"; GitHub lag is UNVERIFIED. While the coordinator is down, "An Orca approval cannot be made", whereas B queues it in the Run mailbox.
3. **The watcher code does not drop in as is.** `approval_of` orders the approval against a trigger **label** (`predicates.py` lines 226 to 229), not against a plan reply comment, and `unchanged_since` deliberately skips comments by `own_login` (line 254: `if comment.author_login != own_login`). The coordinator's plan reply is posted as `own_login`, so the existing check would not see an edit to it. The read-only verb needs new predicates; it is reuse of the read plumbing and the actor checks, not of the whole rule. The agent's hash check still protects the plan file itself.
4. **The consumed list is local.** If the coordinator's ledger is lost, an already-consumed label event looks new. C should also post a consumed marker on the issue (or check for the agent's own progress) before acting; the proposal as written does not.
5. **Key ambiguity.** C names "that id plus the plan version" as the key but in F7 consumes "per (issue, stage, plan version)". The second must be the rule, or a remove-and-reapply of the label (a new event id) would restart finished work. Whether GitHub records a second `labeled` event for an already-present label is UNVERIFIED.
6. **Total dependence on GitHub reachability.** "Every approval depends on GitHub being reachable and readable."
7. **No ack.** C does not define the agent's acknowledgement; B's `ack <approval-id> applied|refused` should be adopted.

## 6. Shared assumptions

- **A-001: QUALIFY.** C cannot run without a coordinator that owns each claimed issue, and none exists (WA-07, SW-13 deferred). The owner must decide who opens it and how many issues one coordinator holds before any variant is buildable.
- **A-002: QUALIFY.** All three type a line into a session they did not start, and whether Orca allows that is UNVERIFIED. B's supervised-worker alternative (SW-13) is the fallback every variant should name.
- **A-003: QUALIFY.** The plan may be a `/sc:workflow` package, not one file, so "plan version" must be defined over a named file or a manifest of the package and computed by one shared helper on both sides.
- **A-004: QUALIFY.** The owner said the Status move is the approval; no code reads who moved Status (`github.py` `PROJECT_ITEMS_QUERY` reads only `fieldValueByName(name: "Status")`), so the label substitute is needed unless that actor is proven readable. The owner must accept it explicitly.
- **A-005: ACCEPT.** C needs the same writes (plan reply, mention, label, Status) as B; a standing per-issue grant for pipeline issues is unavoidable, though its shape in the 6.8 grant table is new.
- **A-006: QUALIFY.** Under C the approval is durable on GitHub, so a dead session loses no approval, but none of the variants defines how a relaunched agent resumes at the plan boundary without redoing finished work.

## 7. Per-point verdict table

| Point | Superior | Reason |
|---|---|---|
| S-001 | none/owner | Identical skeleton by brief; nothing to decide. |
| C-001 | V3 | B and C both have one actuator; C alone also has one authority, matching the owner's "single source" wording. |
| C-002 | V3 | A GitHub event with a server id survives host loss and cannot collide across stores; B's local row is the truth only on one host. |
| C-003 | V3 | Both keep the watcher write-free; C names a code path for the checks, though it needs new predicates (concession 3). |
| C-004 | V2/V3 tie | Both remove the self-approvable in-session path with the same id-and-hash line. |
| C-005 | V2 | B queues Orca approvals in the Run mailbox while the coordinator is down; C cannot accept them at all. |
| C-006 | V2 | B's Orca path works on one login or two and has no GitHub lag; C's write-through breaks with a separate approver account (X-002). |
| C-007 | V3 | One record means no echo to suppress and no match rule to get wrong. |
| C-008 | V3 | Label removal is a revocation with a readable actor; B's revoke-and-ask behaviour should be kept on top. |
| C-009 | V2 | B names the supervised-worker alternative if typing into a session is not allowed. |
| C-010 | V2 | B changes nothing in the watcher and needs no second account. |
| X-001 | V2/V3 tie | Both keep D2 and NG-2; A reverses them. |
| X-002 | V2 | B has no internal contradiction; C's two halves cannot both hold. |
| X-003 | none/owner | All three substitute a label; only the owner can accept it. |
| A-001 | none/owner | No coordinator exists; the owner must define it. |
| A-002 | V2 | Only B names a fallback delivery path. |
| A-003 | none/owner | Plan identity for a package must be defined for all variants. |
| A-004 | none/owner | Owner acceptance of the label substitute. |
| A-005 | none/owner | Same grant need in all three. |
| A-006 | none/owner | No variant defines resume after the agent session dies. |

## 8. Neutral recommendation

Recommend a merge with B as the base and three parts of C added: the coordinator is the only actuator and records Orca approvals directly in B's locked ledger (no write-through dependency), GitHub approvals are accepted only as a label event whose server id and plan version go into the row through C's read-only stage-status verb, and label removal is the revocation signal; adopt B's ack and mailbox queueing, and post a consumed marker on the issue so a lost ledger cannot restart work. Confidence 70 percent, because B is robust whether or not a second account exists while C's pure form forces the owner to choose between two channels and forgery protection.
