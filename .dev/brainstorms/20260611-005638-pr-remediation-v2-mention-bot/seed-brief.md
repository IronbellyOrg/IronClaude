---
topic: "V2.0 PR auto-remediation — mention-triggered headless remediation bot"
domain: architecture
strategy: enterprise
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-06-11T00:56:38Z
v1_spec: ../20260610-234750-pr-review-auto-remediation/merged-requirements.md
---

# Seed Brief: PR Auto-Remediation V2.0 — Mention-Triggered Headless Bot

## Problem Statement

V1.0 built an **in-session, automatic** Augment-review monitor (`sc:submit-pr --monitor`)
hosted by the Monitor tool — it dies when the terminal closes (V1.0 §R3). V2.0 replaces the
trigger model entirely: a **headless, on-prem process** watches the fork's PRs and activates
**only when an authorized collaborator @-mentions the bot in a reply** to a PR review comment.
On trigger it extracts the **parent comment body** as `opComment` and runs a headless
`claude -p` session executing `/sc:troubleshoot "${opComment}" --depth deep --fix`, then
(per autonomy level) replies to the thread and resolves it.

The core engineering risk is **executing an LLM agent with file-write + git-push authority in
response to untrusted GitHub comment text**. The design must make that safe: authorization,
injection containment, a conservative autonomy default, and bounded loop-safety.

## Known Context (established facts)

- **Trigger shape:** authorized user replies to a PR review-comment thread and @-mentions the
  bot. Detection extracts the **parent** comment (the one being replied to) as `opComment`.
- **Execution primitive:** `/sc:troubleshoot "${opComment}" --depth deep --fix` run headless.
- **Reuse — headless executor:** `src/superclaude/cli/pipeline/process.py` `ClaudeProcess`
  (line 72) already runs `claude --print --verbose --dangerously-skip-permissions
  --no-session-persistence --tools default --max-turns N`. Prompt delivered via **stdin**
  (not argv — bypasses Linux 128KB `MAX_ARG_STRLEN`). Auth inherits `os.environ.copy()` minus
  `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT`. **V2.0 should reuse this class as the headless host.**
- **Reuse — severity rubric:** `src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md`
  (5 tiers: Critical/High/Medium/Low/Nit; remap algorithm lines 63-101). Carried from V1.0.
- **Reuse — fork-only target:** every `gh` call MUST pin `--repo IronbellyOrg/IronClaude`
  (CLAUDE.md ABSOLUTE RULE; gh defaults to upstream parent = the trap).
- **Auth contract:** headless process inherits `ANTHROPIC_BASE_URL` (`:4000/cli` proxy),
  `ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_API_KEY` from env (`~/.aienv` sourced into the daemon's
  environment; `ccsession.env` chmod-600 precedent). Plus a separate `GH_TOKEN`/PAT for the
  GitHub API surface.
- **Greenfield gaps (NOT in repo today):**
  - Reply-to-thread + resolve: no `pulls/<N>/comments/<id>/replies`, no GraphQL
    `resolveReviewThread` anywhere. **Must build.**
  - Collaborator-permission gating: no `gh api .../collaborators/{user}/permission` usage
    anywhere. **Must build.**
  - GitHub event ingress: no webhook listener / `issue_comment` polling / `X-GitHub-Event`
    handling. **Must build.**
- **Loop-guard prior art:** swarm `--watch-max-iterations` bounded-counter pattern
  (`cli/swarm/commands.py:2269`) is the model for the remediation round-counter.

## Constraints (user-prescribed — NOT open for debate)

- **C1 — Autonomy ceiling = mention-flag selectable, default PROPOSE-ONLY.** The @-mention
  grammar carries the level (e.g. `@bot propose` vs `@bot fix`). **Default when no flag = the
  safest level (propose-only: run troubleshoot in an ephemeral checkout, post the patch/diff,
  never push).** Authorized users explicitly opt into push-level autonomy per-invocation.
  Push/reply/resolve are higher levels gated behind explicit flags.
- **C2 — Execution host = self-hosted on-prem. GitHub Actions is OUT.** On-prem infra is
  available for anything (one-shot invoked runner, persistent daemon, or webhook service). The
  **sub-choice among those three is the primary adversarial axis** — debate and pick the best.
- **C3 — Mention text = trigger + whitelisted parsed flags ONLY.** The free-form mention reply
  yields only a small whitelisted grammar (autonomy level, depth override, scope-to-file). The
  **parent comment body is the sole `opComment`** fed to troubleshoot. Tightest injection
  surface — mention text is never passed as free prose to the agent.
- **C4 — Authorization = live GitHub write-permission check.** Gate on
  `gh api repos/IronbellyOrg/IronClaude/collaborators/{commenter}/permission` requiring
  admin/write at trigger time. Always-current; no static allowlist drift.
- **C5 — Reuse V1.0 severity rubric, fork-only `--repo`, reply-to-thread+resolve semantics.**
- **C6 — Out of scope:** V1.0's in-session Monitor-tool host (fully replaced); reviewing/
  replying to non-Augment human comments unless the mention explicitly targets them; modifying
  merge state (`--approve`/`--request-changes`).

## Success Criteria

- **SC-1** An unauthorized commenter's mention is rejected at the authz gate with **zero**
  agent invocation and zero repo mutation (logged).
- **SC-2** Untrusted `opComment` / mention text cannot escape the troubleshoot prompt envelope
  to execute arbitrary shell, exfiltrate secrets, or alter the bot's own control flow
  (injection containment is demonstrable).
- **SC-3** Default (no autonomy flag) invocation makes **zero** pushes — propose-only.
- **SC-4** Push-level invocations validate locally (`make lint` + `ruff format --check` +
  targeted tests) before any push; fork-only `--repo` on every `gh` call.
- **SC-5** Remediation rounds are bounded by a monotonic counter; a bot-push-triggered
  re-review cannot cause unbounded looping.
- **SC-6** A trigger is processed **at most once** (mention de-duplication / idempotency under
  concurrent or restarted hosts).
- **SC-7** Headless secrets (`ANTHROPIC_*`, `GH_TOKEN`) are never logged, never exposed to the
  agent's tool surface, and are scoped to least privilege.

## Open Questions (resolved by the adversarial debate)

- **OQ-A (primary axis):** one-shot invoked runner vs persistent daemon vs webhook listener —
  which on-prem host best balances latency, idempotency, restart-safety, secret-exposure
  window, and operational simplicity?
- **OQ-B:** mention detection — webhook `issue_comment` event vs API polling (`gh api
  .../issues/comments`)? How is the parent comment reliably resolved from a reply, given GitHub
  review-comment threading (`in_reply_to_id`) vs issue-comment flatness?
- **OQ-C:** the injection containment boundary — is `--dangerously-skip-permissions` acceptable
  inside an isolated ephemeral checkout/container, or must the headless agent run under a
  restricted tool/permission profile? Where is the sandbox boundary drawn?
- **OQ-D:** autonomy-flag grammar — exact whitelist tokens, parse/reject rules, and how an
  unknown/garbled flag degrades (to propose-only, never to push).
- **OQ-E:** idempotency/state store — where does "trigger already processed" + round-counter
  state live so it survives host restarts (on-disk ledger vs GitHub reactions/labels as state)?

## Enrichment Context

**Codebase reconnaissance (Auggie/Explore, 2026-06-11):**

- **Headless executor to reuse:** `ClaudeProcess` @ `cli/pipeline/process.py:72` — stdin prompt
  delivery, env-inherited auth, `--max-turns` cap, `--output-format stream-json` available for
  structured monitoring. This is the spawn primitive; V2.0 wraps it, doesn't replace it.
- **Severity rubric to reuse:** `sc-auggie-review-protocol/refs/severity-rubric.md` (5 tiers +
  remap). Severity→action mapping at lines 163-172.
- **gh patterns present:** inline-comment + summary-review posting (`sc-auggie-review-protocol/
  SKILL.md:304-313`). **Reply-to-thread + resolve absent → net-new.**
- **Authz absent:** no collaborator-permission check anywhere → net-new (C4).
- **Ingress absent:** no webhook/issue_comment handling anywhere → net-new (OQ-B).
- **Hook:** `hooks/scripts/offer-pr-review.sh` exists but is **not wired into hooks.json**;
  fail-open, one-shot-per-session, never auto-invokes. V2.0 may add a mention-path mention here.
- **Loop-guard pattern:** swarm `--watch-max-iterations` (`cli/swarm/commands.py:2269`) —
  bounded integer, configurable, `break` on ceiling. Model for the round-counter (SC-5).
