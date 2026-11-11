# Write-back: future stage (never R1)

Owner requirement recorded 2026-11-08 (owner-decisions-20261108.md item 3): users send confirmations or corrections from the BBS to their agents. This departs from issue 409's read-only boundary. It is a FUTURE stage, design only, and never part of R1.

**Boundary change needed in two places before any build:** issue 409 (merged-requirements.md:183, reply kept out of scope) and TUIBBS FR-X-13 "no write-back" (internal/serve/menu.go:637-640). Neither moves without an owner decision. Source: tuibbs-review/write-back-stage.md.

## What Orca provides (from Orca CLI help, as reported in the source)

- `ask` blocks a worker until the coordinator answers, with fixed `--options`; answered by `reply --id <question message id> --body <text>`. Whether `--options` is enforced on the reply body is UNVERIFIED.
- `gate-create --task --question --options` blocks a task; `gate-resolve --id --resolution` releases it.
- Mutations accept `--retry-request <id>`; `request-show` returns completed, pending or absent ("absent is not proof that nothing happened"). `check` replays until acknowledged: at-least-once delivery, receivers deduplicate.
- The coordinator owns its Run; lifecycle commands stay with Orca and the coordinator.
- **Not provided or not proven:** `--from` is a caller claim, checked against the assignee only for `worker_done`. Who Orca accepts a `reply` from is UNVERIFIED. The remote pairing code acts as a broad credential; whether it can be scoped is UNVERIFIED.

## Threat model (controls required)

| Threat | Control |
|---|---|
| Wrong person answers (identity) | Operator-set mapping from TUIBBS UserID to the Orca Run that person owns; no mapping, no button |
| Answering someone else's agent (authorization) | Owner-only rule plus per-user grant; default deny; checked at row build and at submit |
| Denial after the fact (audit) | Tamper-evident record of who answered which question id with which option, before and after the send |
| BBS text steering the agent (prompt injection) | Only a choice from the question's own options; fixed provenance label; no free text |
| Flooding | One accepted answer per question id; per-user limit |
| Replay, double send | Per-answer nonce used as `--retry-request`; stored "already answered" record |
| False success shown | Three states only: delivered, pending, unknown ("do not resend, ask the coordinator"); absent never shown as "not sent" |
| Spoofed author via Message Base | Never route write-back through the Message Base (spoofing itself UNVERIFIED) |
| Stolen BBS host | Narrowest Orca credential possible; if pairing codes cannot be narrowed, the stage waits on Orca |
| Forged audit trail | Move the HMAC key off the audit database volume or anchor the chain head externally |

## Smallest safe first stage: "Answer my own agent's pending question"

- **Shows:** only pending `ask` questions or decision gates from Runs mapped to the logged-in user.
- **Allows:** one of the question's own options, or a fixed Confirm / Decline. No free text, send, spawn, stop, retry, merge or gate-resolve.
- **Transport:** relayed to the owning coordinator, which issues `reply --id` itself; the coordinator stays the authority.
- **Where:** inside the later Go TUIBBS screen (architecture option d), where ACS, identity and audit exist. Not in the Python observer, not in the snapshot (which stays one-way).
- **Deferred:** free-text corrections (stage 2, after injection framing is tested), team-wide answering (needs a group store), any lifecycle control, any Message Base route.

**Python observer stance:** R1, Attention Ledger and Decision Desk stay read-only. Decision Desk may show a pending question and the exact `orca orchestration reply` command for the human to run themselves; the observer never sends anything.

## Gates (all go/no-go before stage 1 ships)

0. **Boundary:** owner records the issue 409 boundary change; TUIBBS owner amends FR-X-13 for this one capability.
1. **Identity:** operator-maintained UserID-to-Run mapping, read-only to users, every change audited.
2. **Authorization:** a new per-user capability (reserved `{control}` or a new `AI[orca-answer]` grant) plus the owner check; default deny.
3. **Input:** answer is one of the question's options or Confirm / Decline; anything else refused; fixed provenance label.
4. **Replay and rate:** one accepted answer per question id; nonce as `--retry-request`; per-user rate rule.
5. **Audit:** `orca.answer.submit` before the send and `orca.answer.result` after (question id, run id, option, nonce, result); hub audit wired into the production broker; HMAC key moved or chain head anchored.
6. **Delivery state:** pending until `request-show` or the coordinator says completed; absent shown as "unknown, do not resend".
7. **Credential:** narrowest Orca credential; if a pairing code cannot be scoped, stage 1 waits on Orca.
8. **Orca sender:** confirm with the Orca owner how `reply` authenticates its sender (UNVERIFIED); relaying through the coordinator is required until answered.
