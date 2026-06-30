<!--
SYNTHESIS BATCH 08 — Customer Journey, Error Handling, User Interaction, API Contracts
Source: research files 01-08 + web-01..03 in ../research/
Template: .claude/templates/workflow/05_prd_template.md (sections 22-25)
Product: PR Auto-Remediation V2.0 — Mention-Triggered Headless Bot (`superclaude remediate`)
Provenance legend:
  [CODE-VERIFIED]  — confirmed against current source (ClaudeProcess, pr_submit/, severity rubric, gh precedent)
  [SPEC]           — required behavior from merged-requirements spec; target, not yet built (cli/remediate/ is greenfield)
  [EXTERNAL]       — market/standards corroboration from web research
NOTE: `src/superclaude/cli/remediate/` does NOT exist yet [CODE-VERIFIED via ls in 01/04/07/08]; all V2.0
behavior below is PROPOSED product requirement, not current capability, unless tagged [CODE-VERIFIED].
-->

## 22. Customer Journey Map

> **Scope note (feature PRD):** The product has **no GUI and no web surface**. The end user is a **repo
> maintainer / on-call reviewer** on the `IronbellyOrg/IronClaude` fork; the entire control surface is a
> short `@bot` comment grammar plus an operator-run systemd service [Agent 8 §3]. The journey below maps
> the *authorized collaborator* (primary actor) and *operator* (deployer) experience for a
> mention-triggered remediation request.

### 22.1 Journey Stages

| Stage | User Goal | Actions | Touchpoints | Emotions | Pain Points | Opportunities |
|-------|-----------|---------|-------------|----------|-------------|---------------|
| **Awareness** | Learn that a headless `@bot` can fix flagged PR findings on-prem | Reads team docs / sees the bot reply on a prior PR; learns `@bot` grammar | `superclaude remediate` CLI docs; existing PR threads | Curious, cautiously hopeful | Distrust of AI auto-changes (only ~3–33% of devs trust AI output) [EXTERNAL web-02/03] | Position as the "middle ground / confirmation step" the market leader lacks [EXTERNAL web-01 §1.2] |
| **Consideration** | Decide whether to delegate a finding vs fix by hand | Compares effort; checks that propose-only is the default and a human still merges | Severity-rubric tiers (🔴/🟠/🟡/🟢/💬) [CODE-VERIFIED]; §20 "humans merge" non-goal | Skeptical but reassured by conservative default | Fear of over-action / unauthorized push (Copilot's #1 complaint) [EXTERNAL web-01 §1.2] | Propose-only default + live authz gate directly answers the incumbent gap |
| **Acquisition (Deploy)** | Stand up the bot for the repo | Operator installs systemd unit + sandbox image; sources secrets via `EnvironmentFile=` chmod-600 | `deploy/remediate-bot/` units [SPEC]; `~/.aienv` proxy contract (`:4000/cli`, `T2Model*` only) [memory] | Focused, security-conscious | `deploy/` + sandbox tech (OD-1) are fully greenfield, zero in-repo precedent [CODE-VERIFIED 04/08] | Ship hardened defaults (deny-all egress, no host mounts) as turn-key NFRs [EXTERNAL web-03 §3.2] |
| **Onboarding (First mention)** | Trigger the bot correctly the first time | Replies to an Augment/human review comment: `@bot fix --depth deep` | PR review-comment reply thread; `@bot` grammar (D4) [SPEC] | Tentative, watching for an ack | Unsure which flags are whitelisted; mention is app-level convention, not a GitHub primitive [EXTERNAL web-03 §1.2] | Bot acks the claim quickly (poll floor ≥30s) so the user knows it was seen |
| **First Value** | Get a usable proposed fix | Bot resolves the **parent** comment as `opComment`, runs `/sc:troubleshoot` in sandbox, replies with a diff/summary + SHA | Threaded reply with proposed patch; round-outcome summary | Relief / "it understood the issue" | Latency (cold-start; benchmark vs PR-Agent ~30s, Copilot 90s+) [EXTERNAL web-01 §5] | Stream progress; cap opComment length under the 16 MiB stdin guard [CODE-VERIFIED process.py] |
| **Engagement** | Iterate within a bounded budget | Re-reviews, replies again to refine; bot increments round only when PR head SHA == bot's recorded push SHA | Per-PR push budget (default 2, cap 5) [CODE-VERIFIED `pr_submit/fsm.py` DEFAULT_MAX_ROUNDS=2/HARD_CAP=5]; round-outcome replies | Confident, in control | Loop anxiety ("will it run forever?") | Bounded monotonic counter + HALT summary makes the ceiling visible and trustworthy |
| **Retention** | Rely on the bot across many PRs without surprises | Uses it routinely; trusts that a `read`-only user mentioning it does nothing | Live per-trigger authz gate (D5); trigger ledger (H1) [SPEC] | Trusting, low-friction | Trust erodes the moment an unwanted change lands | Immutable trigger ledger as a visible provenance/audit artifact [EXTERNAL web-02 R4] |
| **Advocacy** | Recommend the bot to other regulated/air-gapped teams | Shares the on-prem, injection-contained story internally | Audit log / ledger exports; security narrative | Proud of the safety posture | — | Lead with the "Comment and Control" threat the split-host design neutralizes [EXTERNAL web-01/02] |

### 22.2 Moments of Truth

| Moment | Description | Success Criteria | Failure Recovery |
|--------|-------------|------------------|------------------|
| **The authorization decision** | A user replies `@bot fix`; the Dispatcher runs a live collaborator-permission check on the *replier* (not the parent author) | Write-permission replier → trigger claimed; `read`-only replier → polite ack-reject, **zero action** (AC-1) [SPEC] | Reject is itself the safe outcome; post a one-line "not authorized" reply, log the attempt, take no remediation |
| **Parent-comment resolution (opComment capture)** | Dispatcher resolves the mentioned comment's *parent* via `in_reply_to_id` and treats its body as untrusted DATA | Correct parent body captured and JSON-encoded into the CONTROL/DATA envelope, delivered via stdin — **never** `/sc:troubleshoot "${opComment}"` interpolation (SC-2/AC-3) [CODE-VERIFIED seam; SPEC envelope] | If parent cannot be resolved, HALT and reply asking the user to mention directly on the finding; never guess |
| **The push gate** | After validation, the Dispatcher decides whether to push host-side with a short-lived token | Push only if effective autonomy ≥ `push` AND validation passed AND `needs_human_decision==false` AND under budget AND real edits exist (5-predicate conjunction) [CODE-VERIFIED `evaluate_push_decision`] | Any predicate false → fall back to propose (post diff, don't push); `needs_human_decision` → HALT with explanation |
| **Thread reply + resolve** | Bot replies to the review thread with the outcome and (at `resolve` level) resolves it | Reply lands on the correct thread (matched by `databaseId`); resolve targets the right `threadId` (INV-010) [SPEC] | Wrong-thread risk is the highest net-new GitHub surface — gated behind the §21.3 probe-first lock; on ambiguity, reply-only, do not resolve |

---

## 23. Error Handling & Edge Cases

> **Design principle:** The product exists to neutralize a *named, proven* attack class — "Comment and
> Control" (Johns Hopkins, Apr 2026) hijacked Claude Code, Gemini CLI, and Copilot Agent via PR/issue
> comments into leaking secrets, zero maintainer interaction [EXTERNAL web-01/02]. Error handling is
> therefore **fail-safe / fail-closed by construction**, not best-effort. Where a failure mode protects
> a security invariant, the safe outcome (reject, HALT, propose-not-push) **is** the recovery.

### 23.1 Error Categories

| Category | Examples | User Experience | Recovery |
|----------|----------|-----------------|----------|
| **Authorization Errors** | `read`-permission replier mentions `@bot`; non-collaborator sender; bot login spoofing attempt | Polite one-line "not authorized to trigger remediation" reply; no remediation runs (AC-1) | Reject-by-default; log the attempt to the trigger ledger; classifier keys only on the configured collaborator-permission + Augment-bot-login, unknown → safe default [CODE-VERIFIED `pr_submit/classifier.py` 3-state, T-211] |
| **Validation / Intent Errors** | Unparseable/unknown flag in the `@bot` grammar; ambiguous intent; `needs_human_decision` finding (security trade-off, API-contract change, multiple valid fixes) | Bot replies stating the item needs a human decision and HALTs; no push | `needs_human_decision` HALT short-circuit is honored before the push gate [CODE-VERIFIED consumed at `fsm.py:204/:353/:158`]; ⚠️ no Python code *sets* the flag today — V2.0 must build a deterministic populator or document the in-sandbox self-report dependency [CODE-VERIFIED gap, Agent 6] |
| **Prompt-Injection Attempts** | opComment contains hidden `-- Additional instruction --` blocks, `gh issue edit $TOKEN` exfil payloads, white-on-white "authorized/urgent" framing [EXTERNAL web-02 §2.3] | Transparent to user; injection cannot reach a consequential action | Architectural: opComment is JSON DATA in a CONTROL/DATA envelope via stdin, never interpolated (SC-2); Runner holds **no** push token / long-lived secret; propose-only blast-radius cap [CODE-VERIFIED stdin delivery; SPEC envelope + secret split] |
| **System / Process Errors** | Runner `claude -p` hangs; exceeds `timeout_seconds` (default 6300s ≈ 105 min); process tree must be killed | `StuckRun` alert raised; trigger marked failed; no partial push | `ClaudeProcess` returns rc `124` on timeout and kills the whole child tree via `os.setpgrp`→`os.killpg` [CODE-VERIFIED process.py]; ledger intent-without-outcome ⇒ RESUME/re-verify, never silent re-execute (§9) [SPEC] |
| **Secret-Leak (config) Errors** | Runner env inadvertently inherits `GH_TOKEN` / push token / `ANTHROPIC_AUTH_TOKEN` | Invisible to user but a release-blocking defect | `build_env()` is additive-only `os.environ.copy()` and **cannot** strip inherited secrets via `env_vars` [CODE-VERIFIED process.py:145-160]; AC-7 (`/proc/<pid>/environ` grep = 0) requires a new empty-base/allowlist seam OR a secret-free sandbox parent — gated by a named regression test [CODE-VERIFIED gap, all 8 agents] |
| **Integration / GitHub-API Errors** | Reply posts to wrong thread; `resolveReviewThread` targets wrong `threadId`; `in_reply_to_id` missing/unreliable | Risk of resolving an unrelated reviewer's thread (INV-010) | Reply/resolve are net-new GraphQL in Python — no committed Python caller; a reference bash flow has since landed in the untracked parallel V1 `sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`, but it is locked behind the §21.3 throwaway-PR probe that captures real `databaseId`/`in_reply_to_id` shapes as committed config before parser code; on mismatch, reply-only |
| **Rate-Limit / Timeout Errors** | GitHub primary/secondary rate limits; `429`/`Retry-After`; poll storms | Slower acks; no dropped triggers | ETag/`If-None-Match` conditional polling + `Retry-After`/`X-RateLimit-Remaining` backoff (§13); poll floor ≥30s [CODE-VERIFIED `MIN_POLL_INTERVAL=30`]; net-new (0 in-repo precedent) [CODE-VERIFIED] |
| **Concurrency Errors** | Two Dispatcher passes claim the same trigger; parallel git tree mutations on one PR | At-most-once execution per trigger | Two-phase ledger claim keyed on `(trigger_comment_id, parsed_flag_hash)` + per-PR `flock`; lock acquisition must **fail-closed** (the only in-repo flock precedent is bash + fail-open — wrong model to copy) [CODE-VERIFIED gap, Agent 4 F9] |
| **Push / Repo-Target Errors** | `gh` call omits `--repo`; PR lands on upstream parent instead of fork | Catastrophic if unguarded (historically burned the operator) | H5 `gh_call()` unconditionally injects `--repo IronbellyOrg/IronClaude`; today this is **prose-only** discipline (CLAUDE.md), never code-enforced — H5 is the first mechanical gate, with a test asserting no argv can omit `--repo` [CODE-VERIFIED 0 Python `gh` callers, C5] |

### 23.2 Edge Cases

| Scenario | Expected Behavior | Test Case |
|----------|-------------------|-----------|
| Replier has `read` permission only | Ack-reject reply, zero remediation (AC-1) | Mock collaborator-permission = `read`; assert no Runner spawn, ledger logs reject |
| opComment exceeds envelope length cap | Typed pre-spawn failure, no process started | `PromptTooLargeForArgv` raised before any handle opens when encoded prompt > `PROMPT_MAX_BYTES` (16 MiB default, env-overridable) [CODE-VERIFIED process.py:56-69,169-173] |
| Re-review arrives but PR head SHA ≠ bot's recorded push SHA | Does **not** count as a new round (prevents infinite loop) | Assert round increments only at the single FSM edge when `head_sha == recorded_push_sha` [CODE-VERIFIED `should_halt_rounds` `>=` fence-post, `fsm.py:129`] |
| Push budget exhausted (reached cap 5) | HALT with cap-summary reply; no further pushes | Drive 5 rounds; assert 6th transitions to `HALT_MAX_ROUNDS` [CODE-VERIFIED `HARD_CAP_MAX_ROUNDS=5`] |
| Parent comment unresolvable (`in_reply_to_id` null) | HALT; reply asking user to mention directly on the finding | Probe-locked `DetectionContract`; assert no opComment fabricated |
| Dual GitHub payload shapes (`author.login` vs `user.login`) | Both shapes parsed identically | `classifier._login_of` already handles both, tested [CODE-VERIFIED Agent 6 §D] |
| Dispatcher restart mid-trigger (crash window) | Resume from ledger; re-verify, never re-execute a recorded intent | Two-phase intent/outcome replay; intent-without-outcome ⇒ RESUME (§9) [SPEC; pattern from `sprint/recovery.py` JSONL replay, Agent 4/5] |
| `--dangerously-skip-permissions` default flag | Safe **only** because of the sandbox boundary (no host mounts, deny egress), not the flag itself | Assert flag present AND sandbox network deny-all + no host home mount [CODE-VERIFIED default `process.py:93`; SPEC sandbox] |
| Sandbox needs Anthropic proxy but deny-all egress | Proxy host (`:4000/cli`) must be on the egress allowlist alongside `api.github.com` + single-repo git | Assert egress allowlist includes proxy base from `~/.aienv`; GitHub creds stay host-side [INV-015, Agent 4 Q-1; memory] |
| Stale `remediation/` top-level dir (empty placeholder) | Feature lives under `cli/remediate/`; ignore/delete `remediation/` | Confirm source home is `cli/remediate/` [CODE-VERIFIED empty `remediation/`, Agent 8 §2] |

### 23.3 Graceful Degradation

| Component Failure | Degraded Experience | User Communication |
|-------------------|--------------------|--------------------|
| Runner sandbox unavailable / spawn fails | No remediation runs; trigger marked failed, not silently dropped | Threaded reply: "remediation could not start — retry later"; ledger records the failure |
| Validation step fails inside Runner | Falls back from `push`/`fix` to **propose**: posts the diff, does not push | Reply includes the proposed patch + "validation did not pass — proposing only, not pushing" |
| GitHub reply/resolve API errors after a successful push | Push (intent+outcome) is durable; reply retried; resolve skipped on ambiguity | Two-phase ledger ensures the push is recorded; reply-only fallback, never resolve the wrong thread |
| Rate-limit exhaustion | Polling backs off; acks delayed but no triggers lost | Longer ack latency; conditional-request polling resumes when budget returns |
| Short-lived push token mint fails | Degrades to propose-only (no host-side push) | Reply posts the diff; "could not obtain push credential — proposing only" |
| Dispatcher down (systemd) | Bot is unavailable; mentions queue in GitHub until restart | `Restart=always` watchdog; on restart, ledger replay resumes in-flight triggers (no double-execute) |

---

## 24. User Interaction & Design

> **No GUI, no web surface, no new slash command for end users.** The product's entire "interface" is a
> **4-token `@bot` comment grammar** (D4) plus an operator-run systemd service [CODE-VERIFIED product
> surface, Agent 8 §3]. There are no wireframes in the visual sense — the interaction is text in GitHub
> review threads and the bot's threaded replies. The sections below adapt the template to this CLI /
> conversational surface.

### 24.1 Interaction Surfaces (in lieu of Wireframes)

| Surface | Description | Status | Notes |
|---------|-------------|--------|-------|
| **`@bot` mention grammar** | A whitelisted comment grammar the authorized collaborator types as a reply to a review comment | Proposed (D4) [SPEC] | Tiny whitelist; everything else is config/operator-set |
| **Bot threaded reply** | The bot's response on the same thread: claim ack, proposed diff/summary + SHA, round-outcome, or HALT reason | Proposed (H4) [SPEC] | Reply endpoint is net-new; templated from auggie-review `gh` posting precedent [CODE-VERIFIED SKILL.md:304-314] |
| **Thread resolution** | At `resolve` autonomy, the bot resolves the review thread after a successful outcome | Proposed (H4) [SPEC] | GraphQL `resolveReviewThread` — net-new, §21.3-probe-gated |
| **`superclaude remediate` CLI group** | Operator entrypoint (start/status of the Dispatcher), mirroring `sprint`/`swarm`/`pipeline` | Proposed (D1) [SPEC] | Registers in `cli/main.py` via the deferred-import `# noqa: E402,I001` idiom [CODE-VERIFIED main.py:400-438] |
| **systemd service** | The deployment "screen" the operator manages | Proposed (S2) [SPEC] | `deploy/remediate-bot/` greenfield; `Restart=always`, `EnvironmentFile=` chmod-600 secrets |

### 24.2 The `@bot` Comment Grammar (Control Surface)

The control surface is a small, whitelisted token set. **Default with no flag = `propose`** (the safest
level) [Agent 8 §3]. Reaching `push` requires an explicit flag **AND** write-permission **AND** passing
validation (lattice-minimum) — it must be *structurally impossible* to reach `push` otherwise.

| Token | Values | Default | Meaning |
|-------|--------|---------|---------|
| **Autonomy level** | `propose` < `patch` < `fix` < `push` < `resolve` (lattice) | `propose` | Capability ceiling; effective level = min over (flag, authz projection, validation) [SPEC; generalizes V1 `--monitor {0,1,2,3}` ordinal, CODE-VERIFIED `pr_submit`] |
| **`--depth`** | `quick` \| `deep` | severity-routed | Troubleshoot depth; Critical/High → `deep --fix`, Medium → `--fix`, Low/Nit → report-only [CODE-VERIFIED severity rubric S1] |
| **`--scope`** | path/area hint | full PR-head | Narrows the remediation target |
| **`--rounds`** | integer ≤ cap | 2 (cap 5) | Per-PR push budget [CODE-VERIFIED `DEFAULT_MAX_ROUNDS=2`/`HARD_CAP_MAX_ROUNDS=5`] |

**Example invocation (happy path):** an authorized collaborator replies to an Augment review comment with
`@bot fix --depth deep` → Dispatcher authorizes the *replier*, claims the trigger, resolves the *parent*
comment as `opComment`, runs the sandboxed Runner, and replies with a diff (propose/patch) or a
sandbox-branch commit + SHA (fix/push) [Agent 8 §3].

### 24.3 Design Conventions & Invariants (in lieu of Design System)

- [ ] **Conservative default** — no flag ⇒ `propose` only; cannot reach `push` without explicit flag + write-perm + validation pass [SPEC]
- [ ] **Replier-is-authority** — the *replier* is the sole authorization subject; the *parent author* supplies only DATA (a `read` user mentioning the bot gets ack-reject, AC-1) [SPEC]
- [ ] **Untrusted-data envelope** — opComment is JSON DATA in a CONTROL/DATA envelope, never interpolated into the prompt (SC-2) [CODE-VERIFIED stdin seam]
- [ ] **Severity markers reused** — bot reply tiers follow the existing rubric (🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low / 💬 Nit) [CODE-VERIFIED severity-rubric.md]
- [ ] **Never modify merge state** — strictly `--comment`; never `--approve`/`--request-changes`; humans merge (§20) [CODE-VERIFIED auggie SKILL.md:349 + rubric decision-mode]
- [ ] **AI provenance** — generated commits/replies carry clear bot provenance (provenance, not authorship) [EXTERNAL web-03 §1.4]
- [ ] **Fork-only target** — every `gh` mutation pins `--repo IronbellyOrg/IronClaude` [CODE-VERIFIED C5]

### 24.4 Prototype / Reference Implementations

| Reference | Purpose | Link / Path |
|-----------|---------|-------------|
| `pr_submit/` (V1.0 decision core) | Tested FSM + severity router + autonomy gate the V2.0 interaction logic extends | `src/superclaude/pr_submit/` [CODE-VERIFIED] |
| auggie-review `gh` posting | Template for the bot's summary/inline reply | `sc-auggie-review-protocol/SKILL.md:304-314` [CODE-VERIFIED] |
| OSS "Architect" guardrail framing | External analog of Dispatcher-enforced guardrails the LLM cannot bypass | [EXTERNAL web-01 §2.1] |

---

## 25. API Contract Examples

> **Status:** All GitHub-facing contracts below are **net-new** — there is **no Python `gh` caller
> anywhere in the repo today** [CODE-VERIFIED 0 Python `gh` callers]; ETag/authz surfaces have
> zero in-repo precedent, and reply/resolve have only an untracked bash reference flow
> (`sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`), no committed Python caller. Concrete request/response *shapes* (especially `databaseId` and
> `in_reply_to_id`) MUST be locked by the §21.3 throwaway-PR probe before parser code is written. All
> `gh` calls route through `H5.gh_call()`, which unconditionally injects `--repo IronbellyOrg/IronClaude`.
> The minimal GitHub permission baseline is `contents`, `pull-requests`, `issues`, `id-token` [EXTERNAL
> web-03 §1.2].

### 25.1 Poll for `@bot` Mentions (D3 ingest — conditional request)

**Request (ETag/304 conditional polling, poll floor ≥30s):**

```http
GET /repos/IronbellyOrg/IronClaude/pulls/comments?since={cursor}
If-None-Match: "{etag_from_last_poll}"
Authorization: Bearer {read_comment_token}   # host-side Dispatcher credential, never in Runner
```

**Response (no change):**

```http
HTTP/1.1 304 Not Modified
X-RateLimit-Remaining: 4987
```

**Response (new mention found):** `200 OK` with new `ETag`; the comment whose `body` contains the `@bot`
mention becomes the *trigger comment*; its `in_reply_to_id` points at the *parent* (the `opComment`).
On `429`/secondary limit, honor `Retry-After`/`X-RateLimit-Reset` backoff (§13). *[SPEC; net-new]*

### 25.2 Resolve Parent Comment → opComment (D6)

**Request:**

```http
GET /repos/IronbellyOrg/IronClaude/pulls/comments/{in_reply_to_id}
Authorization: Bearer {read_comment_token}
```

**Response (Success):** the parent review comment; its `.body` is the **untrusted `opComment`**. Login is
read from either `author.login` or `user.login` (both shapes handled) [CODE-VERIFIED `classifier._login_of`].
If `in_reply_to_id` is null/unresolvable → HALT (do not fabricate an opComment). *[SPEC; net-new]*

### 25.3 Live Authorization Gate (D5)

**Request — check the *replier's* permission (not the parent author's):**

```http
GET /repos/IronbellyOrg/IronClaude/collaborators/{replier_login}/permission
Authorization: Bearer {read_comment_token}
```

**Response (Success):**

```json
{ "permission": "write", "user": { "login": "{replier_login}" } }
```

**Decision:** `permission ∈ {write, admin, maintain}` → claim the trigger. `read`/unknown → **ack-reject,
zero action** (AC-1). Reject-by-default; classifier keys only on configured constants, unknown → safe
default [CODE-VERIFIED `pr_submit/classifier` discipline]. *[SPEC; net-new — 0 in-repo precedent.]*

### 25.4 Internal opComment Envelope → Runner (R2/R3 — stdin, not argv)

The Dispatcher delivers a **CONTROL/DATA envelope** to the Runner over **stdin** — never as
`/sc:troubleshoot "${opComment}"` interpolation (SC-2/AC-3). This is the central injection containment.

```json
{
  "control": {
    "intent": "fix",
    "depth": "deep",
    "scope": null,
    "max_rounds": 2,
    "pr_head_sha": "{sha}",
    "trigger_comment_id": "{id}"
  },
  "data": {
    "op_comment_body": "<untrusted parent-comment text, JSON-encoded, treated as DATA only>"
  }
}
```

The Runner spawns via `ClaudeProcess` [CODE-VERIFIED process.py:72], whose command is:

```text
claude --print --verbose --dangerously-skip-permissions --no-session-persistence \
  --tools default --max-turns {30|60} --output-format stream-json [--model {T2Model*}]
```

Prompt (the envelope) is written to **child stdin in 64 KiB chunks** (bypasses the 128 KB argv limit),
with a pre-spawn `PROMPT_MAX_BYTES` guard (16 MiB default) raising `PromptTooLargeForArgv`
[CODE-VERIFIED process.py:121-258]. Runner env MUST exclude `GH_TOKEN`/push/`ANTHROPIC_AUTH_TOKEN`
(AC-7) — requires a new allowlist seam, since `build_env()` is additive-only [CODE-VERIFIED gap].

### 25.5 Post Threaded Reply (H4 — outcome)

**Request:**

```http
POST /repos/IronbellyOrg/IronClaude/pulls/{pr}/comments/{parent_comment_id}/replies
Content-Type: application/json
Authorization: Bearer {short_lived_token}

{ "body": "Proposed fix for this finding:\n\n```diff\n...\n```\nValidation: passed. Round 1/2." }
```

**Response (Success):** `201 Created`. Reply must land on the correct thread (matched by `databaseId`);
on ambiguity, reply-only and skip resolve. Strictly `--comment` semantics; never `--approve`/
`--request-changes` [CODE-VERIFIED auggie SKILL.md:349]. *[SPEC; reply endpoint net-new.]*

### 25.6 Resolve Review Thread (H4 — GraphQL, `resolve` autonomy only)

**Request:**

```http
POST /graphql
Authorization: Bearer {short_lived_token}

{ "query": "mutation { resolveReviewThread(input: {threadId: \"{thread_node_id}\"}) { thread { isResolved } } }" }
```

**Response (Success):**

```json
{ "data": { "resolveReviewThread": { "thread": { "isResolved": true } } } }
```

`{thread_node_id}` is obtained by paginating `reviewThreads` and matching on `databaseId` (INV-010). This
is the **highest-risk net-new surface — no committed Python GraphQL caller** (a reference bash flow exists in the untracked parallel V1 `sc-pr-submit-protocol` skill) [CODE-VERIFIED] — and is a hard
§21.3 probe dependency. On any thread-match ambiguity, do **not** resolve. *[SPEC; net-new.]*

### 25.7 Standard Error Envelope

```json
{
  "status": "error",
  "error": {
    "code": "NOT_AUTHORIZED | PARENT_UNRESOLVABLE | VALIDATION_FAILED | BUDGET_EXHAUSTED | NEEDS_HUMAN_DECISION | PROMPT_TOO_LARGE | RATE_LIMITED",
    "message": "Human-readable reason posted to the thread; full detail recorded in the trigger ledger."
  }
}
```

Every error code maps to a fail-closed outcome in §23.1 (reject / HALT / propose-not-push). All triggers,
exact opComment input, and decisions are written to the immutable **trigger ledger** as a queryable
provenance/audit artifact [EXTERNAL web-02 R4 / web-03 R8].

---

<!-- END SYNTHESIS BATCH 08 (sections 22-25) -->
