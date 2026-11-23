# Write-back stage: confirmations and corrections from the BBS to agents (design sketch)

Owner requirement recorded 2026-11-08 (`.dev/issues/409/owner-decisions-20261108.md` item 3). This departs from issue 409's read-only boundary and needs an explicit boundary change before any build. Design only.

Boundary change needed in two places: issue 409's observer is read-only and its operational list keeps reply out of scope (merged-requirements.md:183), and TUIBBS's AI surfaces carry the rule "FR-X-13: no write-back" (internal/serve/menu.go:637-640). Neither moves without an owner decision. Detailed evidence: notes-2.md sections C, D-facts, D-threat-model, D-proposed-first-stage.

## What Orca provides

- **Unblocking a worker.** `ask` blocks a worker until the coordinator answers; it accepts fixed choices with `--options`. The answer is `reply --id <question message id> --body <text>` (Orca CLI help, notes-2 Df1). Whether `--options` is enforced on the reply body is UNVERIFIED.
- **Structured confirm points.** `gate-create --task --question --options` blocks a task; `gate-resolve --id --resolution` releases it (notes-2 Df1). This fits "confirm or correct" better than free text.
- **Delivery state and idempotency.** Mutations accept `--retry-request <id>`; `request-show` returns completed, pending or absent, and absent "is not proof that nothing happened". `check` replays batches until acknowledged, so delivery is at least once and receivers must deduplicate (notes-2 Df3).
- **Authority.** The coordinator owns its Run; worker questions go to the Run mailbox; lifecycle commands (start, stop, abandon, release, reset) stay with Orca and the coordinator (notes-2 Df3).
- **Not provided or not proven.** `--from` is a caller-supplied claim, checked against the assignee only for `worker_done` (notes-2 Df2). Who Orca accepts a `reply` from is UNVERIFIED: the installed orchestration guide (`orca skills get orchestration`, 215 lines) was read in this review and its reply section gives usage only, no sender rule. Remote access uses a pairing code, which acts as a broad credential; whether it can be scoped is UNVERIFIED.

## Threat model

| Threat | Control needed |
|---|---|
| Wrong person answers (identity) | Operator-set mapping from TUIBBS UserID (SSH key fingerprint) to the Orca Run that person owns; no mapping, no button. |
| Answering someone else's agent (authorization) | Owner-only rule: the question's Run must map to this user, plus a per-user grant; default deny; checked when the row is drawn and again on submit. |
| Denial after the fact (audit) | Tamper-evident record of who answered which question id with which option, before and after the send. |
| BBS text steering the agent (prompt injection) | Stage 1 sends only a choice from the question's own options; the relayed text carries a fixed "human answer via TUIBBS, user X, option N" label. No free text. |
| Flooding (rate) | One accepted answer per question id; a per-user submission limit. |
| Replay and double send | A TUIBBS nonce per answer, used as Orca's `--retry-request`; a stored "question already answered" record. |
| False success shown (delivery) | Three states only: delivered (Orca receipt completed), pending, unknown ("do not resend, ask the coordinator"). Absent is never shown as "not sent". |
| Spoofed author via chat | Never route write-back through the Message Base: it trusts the `tuibbs_principal` post property on read (internal/mattermost/translate.go:107-112; spoofing itself UNVERIFIED). |
| Stolen BBS host (blast radius) | The BBS host holds the narrowest Orca credential possible; if pairing codes cannot be narrowed, the stage waits on Orca. |
| Forged audit trail | The HMAC key file sits beside the audit database (path `audit_hmac.key` named only, not opened; notes-2 B5), so a host compromise can rewrite the chain; move the key or anchor the chain head externally. |

## What TUIBBS already provides and what is missing

| Need | Provided today | Missing |
|---|---|---|
| Identity | Stable key-based UserID per principal (internal/auth/principal.go:78-91); AI sessions record an owner (notes-2 B7) | Any link from a TUIBBS user to an Orca Run |
| Authorization | Default-deny ACS engine, checked at menu build and at invoke (notes-2 B4); `RL:n/window` rate atom | An owner-only rule; the `{control}` capability is reserved, not built (internal/ailink/watch_gate.go:10-24); `GM[...]` is always false because the group resolver is empty (internal/auth/provider.go:244-257); `AI[claude]` is granted to sysop only |
| Audit | HMAC-chained append-only log with verify and replay commands (notes-2 B5) | An answer event type; hub audit not wired into the production broker (notes-2 C2, UNVERIFIED by grep); key stored beside the database |
| Input hygiene | MCP argument sanitiser design that rejects control characters and audits injection attempts (notes-2 C4) | It is unwired; nothing applies it to an Orca path |
| Agent link | Sysop-only PTY spawn and read-only watch of agents TUIBBS itself started (notes-2 C3, C6) | Any path to an agent TUIBBS did not start, such as an Orca worker; any Orca client |
| Teams | None | A group store and a Run-to-group mapping before any staff-wide answering |

## Smallest safe first stage

**"Answer my own agent's pending question", enum only, relayed through the coordinator.**

- **Shows:** only pending `ask` questions or decision gates from Runs the operator has mapped to the logged-in user.
- **Allows:** picking one of the question's own options, or a fixed Confirm / Decline. Nothing else: no free text, no send, spawn, stop, retry, merge or gate-resolve.
- **Transport:** TUIBBS does not reply into the worker's mailbox. It hands the choice to the owning coordinator, which issues the `reply --id <question message id>` itself. The coordinator stays the authority and an agent with its own judgement sits between BBS input and the worker.
- **Where it lives:** inside the later Go TUIBBS screen (architecture-options.md option d), where ACS, user identity and audit exist. Not in the Python observer, and not in the snapshot, which stays one-way.
- **Deferred:** free-text corrections (stage 2, only after injection framing is tested), team-wide answering (needs a group store), any lifecycle control, any route through the Message Base.

Where the Python observer stands: R1, Attention Ledger and Decision Desk stay read-only. Decision Desk may show a pending question and the exact `orca orchestration reply` command for the human to run themselves; that keeps the read-only boundary because the observer never sends anything.

## Gates

All must pass before stage 1 ships; each is a go or no-go, not a score.

0. **Boundary gate.** The owner records the boundary change for issue 409 (merged-requirements.md:183) and the TUIBBS owner amends FR-X-13 (internal/serve/menu.go:637-640) for this one capability.
1. **Identity gate.** Operator-maintained UserID-to-Run mapping, read-only to users, every change audited. No mapping, no button.
2. **Authorization gate.** A new capability (the reserved `{control}` or a new `AI[orca-answer]` grant) per user, plus the owner check; default deny; checked at row build and at submit.
3. **Input gate.** Answer must be one of the question's options or Confirm / Decline; anything else refused; fixed provenance label on the relayed text.
4. **Replay and rate gate.** One accepted answer per question id, stored in TUIBBS; TUIBBS nonce used as `--retry-request`; an `RL` rule per user.
5. **Audit gate.** `orca.answer.submit` before the send and `orca.answer.result` after (question id, run id, option, nonce, result); hub audit wired into the production broker; HMAC key moved off the database volume or the chain head anchored externally.
6. **Delivery-state gate.** Pending until `request-show` or the coordinator's acknowledgement says completed; absent shown as "unknown, do not resend".
7. **Credential gate.** The BBS host holds the narrowest Orca credential available; if a pairing code cannot be scoped to answering mapped Runs, stage 1 waits on Orca.
8. **Orca sender gate.** Confirm with the Orca owner how `reply` authenticates its sender (currently UNVERIFIED); relaying through the coordinator is required until that is answered.
