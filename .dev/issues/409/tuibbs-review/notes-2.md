# TUIBBS review notes 2: identity, messaging, write-back (issue 409)

Scope: read-only review of /tmp/tuibbs-review (IronbellyOrg/TUIBBS-scp, shallow clone) and the installed Orca CLI help. Paths are repo-relative for TUIBBS.

## B. Identity and governance

### B1. SSH-key identity
- Authentication is public-key only. Password and keyboard-interactive callbacks are nil, so the transport never offers them; the `none` method is refused; at most 6 auth tries per connection (internal/ssh/README.md:69-73, :115-122).
- The auth decision core is `auth.Provider`: it fingerprints each offered key (SHA256), resolves fingerprint -> key binding -> user identity, and admits (authenticated or anon) or refuses (internal/auth/README.md:12-20; internal/auth/provider.go:615-628).
- Two interchangeable resolver backings: the SQLite `users`/`user_keys` tables (internal/auth/repobind.go, per internal/auth/README.md:38-39) and the TOML `[auth].allowlist` "dogfood" resolver that gives each entry a synthetic one-based user id (internal/auth/README.md:40-48). The user guide says allowlist changes need a restart (docs/user/account-and-identity.md:16).
- The resolved principal is stashed on the SSH connection context and lifted into the per-session context, so every later ACS check and audit emit reads that binding (internal/session/README.md:237-251).
- The principal carries only SessionID, UserID, Role, Groups and an Anonymous flag (internal/auth/principal.go:78-91). There is no email, no external account link, no team field.
- Rate limiting: per-subject sliding window on the fingerprint (fallback the SSH username) plus a per-source-IP throttle on the refusal log line only; the durable `auth.ratelimited` audit row is not throttled (internal/auth/provider.go:575-586, :625-627).

### B2. Roles
- Closed set of five roles, strict ladder anon(0) < regular < validated < op < sysop(4) (internal/auth/role.go:87-110, :122-130). User-facing labels: sysop, moderator, member, guest, new (internal/auth/role.go:60-64).
- A key that authenticates but has no role row is admitted at the anon level with Anonymous=true, keeping the user id for audit (internal/auth/provider.go:491-510).
- Roles are assigned by the operator (allowlist or DB); users cannot change roles from the TUI (docs/user/account-and-identity.md:69-89).

### B3. Registration modes
- `open` (v1 default): an unknown key is admitted as anon. `closed`: an unknown key is refused during the SSH handshake (internal/auth/provider.go:121-128, :517-535; docs/user/account-and-identity.md:20-25).
- Any write-back feature must assume `open` hosts exist, so it must gate on more than "can log in".

### B4. ACS, in plain words
- ACS = Access Control System: a small rule language. Each menu route, module or feature carries a short text rule such as `LV>0` ("level above anon", i.e. a known user) or `LV>3` ("sysop only"), and the server evaluates that rule against the logged-in person to say yes or no (internal/acs/README.md:3-5).
- Vocabulary is frozen at six building blocks plus a rate-limit extension: GM[group] group membership, LV>N/<N/=N level, AF[N] affiliation flag, AI[provider] AI-provider grant, MOD[name] module loaded, AGE>N account age in days, and RL:n/window rate limit (internal/acs/atoms.go:11-31, :95-137). Operators `&`, `|`, `!` (internal/acs/atoms.go:59-61). Unknown atom or syntax error = deny and log (internal/acs/atoms.go:49-53).
- LV evaluates as Role.Level() > N, with an unknown role at -1 so it denies (internal/acs/engine/atom_eval.go:17-18, :275-281).
- Where evaluated: one shared engine bound process-wide in `internal/serve/acsbind.go` (internal/serve/acsbind.go:16-20), called at two points per feature, once to hide/show the menu row and again at invoke time (defence in depth), e.g. Message Base re-checks `LV>0` when opened (internal/serve/menu.go:704-711), AI watch re-checks `AI[claude]` (internal/ailink/watch_gate.go:85-105).
- Live grant today: `AI[claude]` is granted only to sysop by a hard-coded "dogfood" facts source (internal/serve/acsbind.go:22-31, :57-66). So only sysops can spawn or watch AI sessions in the shipped build.
- The designed per-channel Message Base gate (ACS AND Mattermost channel permission, more-restrictive-wins) is library code with zero production callers; only the route-level `LV>0` half is live (docs/acs-intersection-technical-reference.md:159-161, :232). The doc's own line references to menu.go are stale: the check is now at internal/serve/menu.go:697-711.

### B5. Audit chain
- Single-writer, append-only `audit_log` table; each row sealed as HMAC-SHA256(key, canonical JSON of the event including prev_hmac), plus an `audit_chain_head` pointer row (internal/audit/README.md:3-8; internal/audit/verifier.go:29-31; internal/audit/sink.go:7, :114-116).
- Verification: `tuibbs audit verify` recomputes the chain forward and cross-checks the head pointer, reporting the first break; `tuibbs audit replay` lists every break; `tuibbs audit export` copies rows as JSON-Lines without a verdict (internal/audit/README.md:15-42). These are host CLI commands, not a BBS screen.
- Tamper-evident only against someone without the key. A key holder, or a truncation that also rewrites the head pointer, is explicitly out of scope; no external anchor in v1 (internal/audit/verifier.go:31-33, :50-62).
- Key custody: the HMAC key is a file `audit_hmac.key` in the same data directory as the audit database, provisioned on first boot (internal/serve/audit.go:40-45, :98, :161). Path named only, not opened. Consequence: anyone with the host data dir can forge the chain.
- Redaction runs before sealing, so the chain only covers redacted payloads; always-on key-substring redaction includes `password`, `secret`, `token`, `key` (internal/audit/README.md:44-58).

### B6. Multi-tenancy
- The README calls TUIBBS "multi-tenant" (README.md:4), but the code has no tenant, team or organisation concept: a search for tenant/team_id/org_id/organisation in internal Go code finds only the Mattermost `team_id` setting (one Mattermost team per host) and an unrelated render match (internal/config/config.go:106-107). UNVERIFIED beyond that grep.
- The closest primitive is `Principal.Groups` read by `GM[group]`, but v1 installs a resolver that always returns an empty set and ships no group table (internal/auth/provider.go:244-257). So `GM[...]` rules are always false today.

### B7. Mapping "human staff managing agent teams"
- Per-user view: feasible today. Every principal has a stable UserID; AI sessions record an owner principal (internal/ailink/session_manager.go:165-166, :448-485).
- Per-team view: not feasible without new work. It needs a real group store behind GroupResolver (seam exists, internal/auth/provider.go:244-251) and a mapping from Orca orchestrator/run to a TUIBBS group.
- Who may see worker content: today the AI watch roster shows every AI session to every principal holding `AI[claude]` (sysop only), because spawned sessions register with empty Visibility = public (internal/serve/spawn_handler_unix.go:215-227; internal/hub/presence.go:331-334; internal/ailink/watch_command.go:54-89). A per-session Visibility ACS expression exists as a field but is never set. For an Orca observer, message bodies should default to owner-only (Visibility = an owner rule) and a staff-wide view should be a separate, explicit grant.

## C. Messaging and agent links

### C1. Message Base (messagebase, msgbase, mattermost)
- Layering: a neutral four-method seam (ListChannels, ReadMessages, Post, Subscribe) in internal/messagebase; the TUI-facing model in internal/msgbase; the only Mattermost SDK importer is internal/mattermost, enforced by a script (docs/message-base-technical-reference.md:236-241).
- Co-residency: yes. Mattermost plus PostgreSQL run beside the BBS on the same host per ADR-X9 and are the source of truth for messages; native Mattermost clients see the same channels (docs/message-base-technical-reference.md:161-163, :167).
- Implemented today: REST list/read/post are production-wired; live Subscribe now dials a WebSocket in source but is covered only by fake-dial tests (it was a stub at the v1.4.1 tag); the per-channel permission gate is not wired (docs/message-base-technical-reference.md:177-184). `canPost` is hard-coded true (internal/msgbase/model.go:150).
- Bot attribution: every BBS post goes out as one shared Mattermost bot account (docs/message-base-technical-reference.md:262). The BBS identity is carried two ways: a `tuibbs_principal` post property and a visible "[stamp] " text prefix (internal/mattermost/translate.go:36, :206, :220-223). On read, the author shown is the property when it is non-empty, else the Mattermost user id (internal/mattermost/translate.go:107-112). A native Mattermost user who can set post properties could therefore appear as any BBS user (inference, UNVERIFIED).
- Audit: `msg.post` is emitted only after a successful post and carries metadata only (message id, channel, length), never the body; the emit error is discarded (internal/msgbase/model.go:228-244; internal/audit/events_msg.go:112-130). Connect/disconnect are also audited (internal/serve/menu.go:761, :784).
- Tests: msgbase 1 test file, mattermost 4, messagebase 0 (file count from this review).

### C2. internal/hub and internal/hubaudit
- hub is a single-goroutine in-process broker with three backpressure classes (Interactive, Coalescible, Bulk) (internal/hub/README.md:3-13). It carries presence, direct messages to one session (ACS-checked at publish time, default-deny when the target has no ACS rule or no evaluator is wired), pages, announcements and notifications (internal/hub/direct.go:4, :33-55). 18 test files.
- hubaudit is the bridge that turns hub seam events into audit rows: `hub.publish`, `hub.acs_denied`, `hub.page_rate_limited`, `hub.notify`, `hub.bulk_drop`, `hub.slow_subscriber`; emission is non-blocking and the error is discarded by design (internal/hubaudit/hubaudit.go:1-60).
- Production gap: the live server builds the broker as plain `hub.NewBroker()` without `hubaudit.Options` (internal/serve/serve.go:118-126); the only `hubaudit.Options` call found outside tests is the doc example (internal/hubaudit/hubaudit.go:23). So hub events appear not to reach the audit chain in the shipped build (UNVERIFIED: grep-based).
- hub is in-process only; it is not a network bus and has no Orca link.

### C3. internal/ailink (AI sessions)
- Spawn: a sysop (only `AI[claude]` holder) can spawn a Claude Code PTY session from the menu; it runs via os/exec plus a pty behind the FR-X-10 ship gate (internal/ailink/ailink.go:1-67; internal/ailink/spawn_gate.go:59). The spawner interacts with that PTY directly, so it is a human-to-own-agent terminal, not a message channel.
- Watch: another `AI[claude]` holder can watch a session read-only; the watch sink never writes to the child and closing it never signals the child (internal/ailink/watch_command.go:1-9, :95-120). The design rule is explicit (internal/serve/menu.go:637-640):
  > FR-X-13: no write-back
- `{observe}` is a separate capability that confers no write path; a `{control}` capability is reserved for the future but not implemented (internal/ailink/watch_gate.go:10-24, :47; internal/ailink/spawn_gate.go:17-26). A sysop-only lifecycle overlay is also read-only (internal/ailink/lifecycle_overlay.go:5, :30). Audit actions `ai.watch.open` / `ai.watch.close`. 13 test files.

### C4. internal/mcp (plus docs/mcp-tools.md)
- Direction: MCP lets an AI agent call INTO the BBS, not the BBS reach an agent. Three fixed tools: `list_sessions` (GM[sysop]), `send_message_to_session` (LV>0, "agent-driven paging" of a BBS session), `query_audit` (GM[sysop]) (docs/mcp-tools.md:42-48).
- Built as library code with tests (12 test files): fail-closed principal translator (`MCP_PRINCIPAL_UNMAPPED`), argument sanitiser that rejects control characters, embedded ACS text and SQL fragments and audits `mcp.injection_attempt`, per-tool ACS gate, consent gate that treats being in a session as consent in v1, and an SSH subsystem named `mcp` (internal/mcp/README.md:51-62, :74-84, :110-130, :132-152; internal/mcp/sanitise.go:1-30; docs/mcp-tools.md:66-87).
- Not wired: the README says binding the gates into the live dispatch chain and registering the subsystem on the SSH server are still pending (internal/mcp/README.md:173-177). No non-test Go file outside internal/mcp imports it except a lint analyzer. Also, the two sysop tools use `GM[sysop]`, which is always false today because the group resolver is empty (see B6).

### C5. internal/ftn
- Contract-only: no parser, encoder or runtime code in the v1 build; the package holds only CONTRACT.md and README.md (internal/ftn/README.md:3-7). 0 Go files.

### C6. Is there any BBS user -> AI agent path today?
- Yes, one, and only for sysops: spawn gives the sysop a live PTY to a Claude Code session the BBS itself started. Authentication is the SSH key; authorization is `AI[claude]` checked at menu build and again at invoke; audit covers spawn/watch lifecycle, not the keystrokes.
- No path exists from a BBS user to an agent the BBS did not spawn (such as an Orca worker). Watch is read-only by explicit rule, MCP is the reverse direction and unwired, the Message Base talks only to Mattermost, and FTN is a contract. Any Orca write-back is net-new.

## D-facts (Orca)

Source: installed `orca` CLI help only (it resolved to the Orca CLI, not the GNOME screen reader). No message was sent. The skill file is a 68-line discovery stub: it says the real guide is printed by `orca skills get orchestration` (/home/coder/.claude/skills/orchestration/SKILL.md:16-18, :49-61). That guide was not loaded, because the brief allowed `--help` only. A grep of the stub for reply/ask/question/authority hits only its description lines (/home/coder/.claude/skills/orchestration/SKILL.md:5, :21-25).

### Df1. What unblocks a worker blocked in `ask`
- `ask` sends a question to the coordinator and blocks until it is answered. From an active Dispatch it goes to the owning Run mailbox. It accepts `--options <csv>` for fixed choices. Each wait lasts 1 ms to 30 min (default 10 min). A timeout leaves the question pending, and the worker resumes with `--resume <message_id>` (orca orchestration ask --help).
- An answer is `reply --id <msg_id> --body <text>` against that exact question message id. `send` repeats the rule: "To answer a worker question, use orchestration reply --id <msg_id>" (orca orchestration reply --help; orca orchestration send --help). So yes: the unblock is a reply to the exact question message id, with free text in `--body`. The help does not say whether `--options` is enforced on the reply body (UNVERIFIED).
- Separate mechanism: decision gates. `gate-create --task --question --options <json_array>` blocks a task, and `gate-resolve --id <gate_id> --resolution <text>` releases it (orca orchestration gate-create --help; orca orchestration gate-resolve --help). A gate is a structured, task-scoped confirm point, which fits "confirm or correct" better than free text.

### Df2. Who may reply
- The help does not say who may reply. `--from <handle>` is a caller-supplied handle on reply, send, ask and gate-resolve. For `worker_done` only, the help says that without stable pane identity the sender handle must exactly match the dispatch assignee (orca orchestration send --help). That suggests `--from` is a claim, checked only in some paths. Whether a reply from an arbitrary handle is accepted is UNVERIFIED.
- Remote callers reach an Orca server with `--pairing-code` or `--environment`, on every command (orca orchestration reply --help). Anyone holding a pairing code is therefore a potential replier. That code is a credential.

### Df3. Authority Orca and the coordinator keep
- The coordinator owns its Run. Workers' questions and unaddressed mail go to the Run mailbox. Run groups exclude the owning coordinator. `--to dispatch:<id>` lets the coordinator send attempt-specific guidance, which Orca durably relays (orca orchestration send --help).
- Orca keeps lifecycle authority through worker-start/stop/abandon/release, task-update, gate-resolve and reset (orca orchestration --help). None of these belong in a BBS stage-1 surface.
- Delivery and idempotency: mutations take `--retry-request <id>`. `request-show --request <id>` is read-only and returns completed, pending or absent. The help warns that absent "is not proof that nothing happened" (orca orchestration request-show --help). `check` delivers FIFO batches that replay until `--ack`, and `--peek`/`--all` do not drain (orca orchestration check --help). This is at-least-once, so a receiver must deduplicate.

## D-threat-model

| Threat | What is needed | TUIBBS provides | Missing |
|---|---|---|---|
| Identity binding (BBS user -> human owner of the orchestrator) | An explicit, operator-set mapping from TUIBBS UserID (key fingerprint) to the Orca Run/coordinator that person owns | Stable key-based UserID and role (B1, B2); AI sessions record an owner principal (B7) | Any mapping to Orca; no group/team store (B6); Orca's own `--from` is a claim (Df2) |
| Authorization | Only the owner of the Run that asked may answer; staff-wide answer is a separate grant | ACS engine, default-deny, checked at menu and invoke (B4); `AI[provider]` atom pattern | An owner-only atom or Visibility rule; `{control}` capability is reserved, not built (C3); GM[...] always false (B6) |
| Tamper-evident audit | Who answered which question id with what text, before and after the send | HMAC chain with verify/replay CLI (B5); metadata-only post audit pattern (C1) | Key sits beside the DB, no external anchor (B5); hub audit seams not wired in production (C2); no event type for an agent reply |
| BBS text as untrusted input to an agent (prompt injection) | Treat every reply as data: fixed choices first, free text labelled as untrusted, length and control-character limits | MCP sanitiser design: reject control chars, embedded ACS and SQL shapes, audit `mcp.injection_attempt` (C4), reusable as a pattern | Orca reply body is free text (Df1); nothing frames it for the agent; the sanitiser is unwired |
| Rate limits | Per user and per question: one answer, a small number of attempts per window | `RL:n/window` ACS atom (B4); auth rate limiter (B1); hub page rate gate (C2) | Nothing applied to an Orca path |
| Replay | A BBS-side nonce per answer, one accepted answer per question id | Orca `--retry-request` and `request-show` (Df3) | A TUIBBS-side record of "question id already answered"; a binding of the retry id to the audit row |
| Delivery confirmation | Show sent, delivered or unknown honestly | Orca request-show completed/pending/absent (Df3) | Any TUIBBS client of it; the Mattermost write path is fire-and-forget audited only on success (C1) |
| Unknown delivery display | The UI must never claim success it cannot prove | (none) | A three-state status: "delivered (Orca receipt completed)", "pending", "unknown: Orca has no receipt; do not resend, ask the coordinator". Absent must not be shown as "not sent" (Df3) |
| Spoofed authorship via Mattermost | Write-back must not travel through Mattermost posts | (none) | The `tuibbs_principal` property is trusted on read (C1). Do not use the Message Base as the transport |
| Co-resident blast radius | The BBS host must not hold a broad Orca credential | (none) | A narrowly scoped pairing; Df2 suggests a pairing code is broad (UNVERIFIED) |

## D-proposed-first-stage

Stage 1, "answer my own agent's pending question". Design only.

- Scope: the BBS shows only pending `ask` questions, or decision gates, from Runs that the operator has mapped to the logged-in user. That user can answer only by picking one of the question's own `--options`, or a fixed "Confirm" / "Decline". No free text, and no send, spawn, stop, retry, merge or gate-resolve on tasks.
- Transport: TUIBBS does not call `reply` straight into the worker's mailbox. It submits the choice to the owning coordinator, which stays the authority. The coordinator turns it into the `reply --id <question msg id>`. This keeps Orca's coordinator model intact (Df3) and puts one agent with its own judgement between BBS text and the worker.
- Gates before shipping:
  1. Identity gate: an operator-maintained mapping table from TUIBBS UserID to Orca Run, read-only to users, with every change audited. With no mapping there is no button.
  2. Authorization gate: a new ACS capability (the reserved `{control}`, or `AI[orca-answer]`) granted per user, plus an owner check that the question's Run maps to this UserID. Default-deny when either is missing. Checked when the row is built and again at submit.
  3. Input gate: the answer is an enum taken from the question's options. Anything else is refused. The relayed text carries a fixed label such as "human answer via TUIBBS, user X, option N".
  4. Replay and rate gate: one accepted answer per question id, stored in TUIBBS. A TUIBBS nonce is used as Orca `--retry-request`. An `RL` rule limits submissions per user.
  5. Audit gate: an `orca.answer.submit` row before the send and an `orca.answer.result` row after, each with question id, run id, option, nonce and result. Wire `hubaudit.Options` into the production broker at the same time. Move the HMAC key off the DB volume, or add a periodic external head anchor, before staff rely on it.
  6. Delivery-state gate: the UI shows pending until `request-show` (or the coordinator's ack) returns completed. Absent is shown as "unknown, do not resend". The question stays answerable only by the coordinator after that.
  7. Credential gate: the BBS host holds the narrowest Orca credential available. If pairing codes cannot be scoped to "answer questions in mapped Runs", stage 1 waits on Orca.
- Explicitly deferred: free-text corrections (stage 2, after injection framing is tested), staff/team views (needs a group store), any lifecycle control, and any route through the Message Base.

## Verdict

TUIBBS gives a solid identity, role, ACS and HMAC-audit base, but by explicit rule (FR-X-13) it has no write path to any agent and no link to Orca at all.
The smallest safe write-back is an owner-mapped, enum-only answer to a pending Orca question, relayed through the coordinator, audited before and after, rate-limited, nonce-deduplicated, with an honest three-state delivery display.
Blockers before even that: no owner mapping or team store, no owner-only ACS rule, hub audit unwired in production, an audit key beside the DB, and an Orca replier identity that is not proven.

## UNVERIFIED

- Mattermost authorship spoofing through the `tuibbs_principal` property (inference from internal/mattermost/translate.go:107-112; Mattermost permission model not checked).
- No tenant/team concept: based on a grep of internal Go code only (B6).
- Live behaviour of Message Base WebSocket Subscribe (only fake-dial tests seen).
- Exposure of the audit HMAC key: inferred from its path in the data dir; file not opened.
- Hub audit not reaching the chain in production: based on internal/serve/serve.go:118-126 and a grep for `hubaudit.Options`; other wiring sites could exist.
- MCP unwired: based on the README pending note and an importer grep.
- Who Orca accepts a `reply` from, whether `--from` is authenticated, whether `--options` is enforced on reply bodies, and how a pairing code can be scoped: the version-matched guide (`orca skills get orchestration`) was not loaded.
- Test counts are file counts; no tests were run.
