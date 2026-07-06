<!--
SYNTHESIS NOTE: Sections 14-15 of the PR Auto-Remediation V2.0 PRD, synthesized from
research files 01-08 (codebase reuse verification) + web-01..03 (market/security best practice).

Verification tags carried from research:
- [CODE-VERIFIED] = the cited primitive/file exists today and behaves as stated (a REUSE anchor).
- [CODE-CONTRADICTED] = the spec's cited mechanism does NOT hold as written (a required modification).
- [NET-NEW] = no in-repo precedent; must be built. The `superclaude remediate` CLI group
  (src/superclaude/cli/remediate/) does NOT exist yet, so the bot itself is greenfield;
  only the reuse anchors below are current product capability.
-->

## 14. Technical Requirements

> **WHAT:** Cross-cutting technical requirements for the `superclaude remediate` mention-triggered headless PR auto-remediation bot — a split Dispatcher (systemd daemon) + ephemeral sandboxed Runner (`claude -p`) architecture.
> **Scope note:** This is a feature/component PRD. The `cli/remediate/` package is greenfield [CODE-VERIFIED absent]; requirements below state what to build. Reuse anchors (`ClaudeProcess`, `pr_submit`, severity rubric) are [CODE-VERIFIED] as existing primitives, not new product capability.

### 14.1 Architecture Requirements

| Requirement | Description | Rationale |
|-------------|-------------|-----------|
| **Split-host: reasoning/execution separation** | Long-lived **Dispatcher** (systemd daemon, holds credentials, runs authz + push) + ephemeral per-trigger **Runner** (`claude -p`, sandboxed, no secrets, processes the untrusted comment). | CSA Labs prescribes this verbatim as "the fundamental mitigation" for prompt injection: a reasoning layer that cannot execute + a credential-holding execution layer that never processes untrusted input. Directly neutralizes the 2026 "Comment and Control" CVE class. |
| **CLI group, not a skill** | New `superclaude remediate` Click group under `src/superclaude/cli/remediate/`, registered in `cli/main.py` via deferred import + `main.add_command(remediate_group, name="remediate")` carrying `# noqa: E402,I001`. | Host runs headless outside any Claude session; mirrors existing `sprint`/`swarm`/`pipeline` groups. Registration idiom is [CODE-VERIFIED] at `cli/main.py:400-438`; omitting the `# noqa` trips `make lint` (E402), omitting the edit ships a dead group. |
| **Reuse the pure decision core; build only the I/O layer** | Import V1.0's tested decision core from `src/superclaude/pr_submit/` (`fsm`, `severity_router`, `classifier`, `detection`, `models`); build new only the Dispatcher/Runner host + GitHub I/O. | `pr_submit/` is [CODE-VERIFIED] built+tested and already embodies the pure-core / dirty-I-O split (NFR-6: zero `gh`/`git` tokens in the core). V2.0's autonomy gate, round counter, severity routing, push-decision, and detection-contract lock have a near-1:1 ancestor there. Rebuilding under `remediate/` would duplicate tested logic and risk divergent severity grading. |
| **opComment as DATA inside a trusted envelope** | The parent review comment is JSON-encoded into a CONTROL/DATA envelope delivered via Runner stdin — **never** interpolated as `/sc:troubleshoot "${opComment}"`. | The hardened design supersedes the seed-brief's literal interpolation; OWASP LLM01:2025 + CSA both mandate structurally delimiting untrusted content from instructions. Re-introducing interpolation re-opens the exact injection vuln (SC-2/AC-3). |
| **Ephemeral, disposable Runner** | One sandboxed Runner per trigger against an isolated PR-head checkout; torn down after the run; no state carried between triggers. | GitHub's own self-hosted-runner guidance: ephemerality "limits exposure of sensitive resources from previous jobs." Blast-radius minimization (Willison "limit the blast radius"). Logs/ledger must survive teardown. |
| **Conservative propose-only default** | Autonomy lattice `propose < patch < fix < push < resolve`; default `propose` with no flag. Effective level = min over {flag, authz-projection, validation}, then off-lattice HALT (`needs_human_decision`, exhausted push budget). | Market consensus (Copilot draft-PR, Continue "Level 2 Continuous AI", Anthropic 2026 report) + the #1 incumbent complaint (Copilot over-triggers, ignores intent). Reaching `push` must require explicit flag AND write-permission AND passing validation. |
| **Two-phase intent/outcome state ledger** | On-disk ledger records `intent` before any side-effect and `outcome` after; intent-without-outcome on restart = RESUME (re-verify), never silent re-execute. | Survives Dispatcher restart (the core reason V2.0 leaves V1.0's in-session host). Borrows swarm's atomic-write discipline; the append-only two-phase model is [NET-NEW]. |
| **Single `gh` chokepoint** | Every GitHub-mutating call routes through one `gh_call()` wrapper that unconditionally injects `--repo IronbellyOrg/IronClaude`; no raw `subprocess(["gh", ...])` outside that module. | Fork-only `--repo` is [CODE-VERIFIED] enforced today by prose only (CLAUDE.md); no Python in the repo calls `gh`. A headless daemon cannot rely on prose — a single un-wrapped call re-introduces the upstream-PR-misroute hazard. First code-level enforcement of C5. |

### 14.2 Performance Requirements

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Mention-detection latency (poll → trigger seen) | ≤ 30–60s | Dispatcher poll interval; `MIN_POLL_INTERVAL = 30` floor [CODE-VERIFIED in `pr_submit/fsm.py`]. Conditional `If-None-Match`/304 polling keeps cost low between changes. |
| Runner spawn → first action | < 5s after dispatch (sandbox cold-start dependent) | Sandbox cold-start ~90–150ms for microVM (Firecracker/libkrun) per external best practice; measured via audit-log `claude_process_spawn` event timestamp. |
| Runner max wall-clock per trigger | `propose` ≈ 30 turns / `fix` ≈ 60 turns; hard ceiling `timeout_seconds` (default 6300 ≈ 105 min) | `ClaudeProcess.timeout_seconds` [CODE-VERIFIED `process.py`]; `wait()` returns `124` on timeout (bash-compatible). `StuckRun` alert keys on this attribute. Caller MUST pass low `max_turns` (default 100 ≫ propose-30). |
| Large opComment handling | Up to `PROMPT_MAX_BYTES` (16 MiB default, env-overridable) delivered via stdin | Prompt via stdin in 64 KiB chunks, bypassing the 128 KB argv (`MAX_ARG_STRLEN`) ceiling [CODE-VERIFIED `process.py:221-258`]; `PromptTooLargeForArgv` raised pre-spawn for over-cap envelopes. |
| Poll API efficiency under rate limits | Zero secondary-rate-limit trips at steady state | `If-None-Match`/`ETag`/304 conditional requests + `Retry-After`/`X-RateLimit-Remaining` backoff [NET-NEW — 0 in-repo precedent]. |
| Round/push budget convergence | ≤ default 2 rounds per PR (hard cap 5) | `DEFAULT_MAX_ROUNDS = 2`, `HARD_CAP_MAX_ROUNDS = 5` [CODE-VERIFIED `pr_submit/fsm.py`]; round counts as next round only if PR head SHA == bot's recorded push SHA (exact-SHA correlation). |

### 14.3 Security Requirements

| Requirement | Implementation | Compliance |
|-------------|----------------|------------|
| **Prompt-injection containment** | opComment delivered as JSON CONTROL/DATA envelope on stdin, never instruction-interpolated; reasoning Runner holds no secrets and cannot push. | OWASP LLM01:2025; OWASP Top 10 for Agentic Apps (Dec 2025); CSA "delimit untrusted content + minimize tools" — a reviewer/proposer "does not need push." Defends the "Comment and Control" (JHU, Apr 2026) CVE class. |
| **Runner secret isolation (INV-001 / SC-7 / AC-7)** | Runner env built from an empty/allowlist base — **not** `os.environ.copy()`. No `GH_TOKEN`, no push token, no `ANTHROPIC_*` host token in the Runner. Only minimal Claude proxy auth (`~/.aienv` `:4000/cli` base + `T2Model*` ids) enters the sandbox. | ⚠️ **Required code change:** `ClaudeProcess.build_env()` is [CODE-CONTRADICTED] — additive-only `os.environ.copy()` + `env.update(env_vars)` cannot *strip* inherited secrets. Must add an allowlist/`base_env` mode OR build the Runner env from a pre-scrubbed sandbox parent. Gate: `/proc/<pid>/environ` secret-scrape test = 0 hits. |
| **Live per-trigger authorization gate (D5 / C4)** | The **replier** (not the parent-comment author) must hold write/maintain permission, checked live at trigger time via `gh api repos/{owner}/{repo}/collaborators/{login}/permission`. Reject-by-default; unknown/insufficient → polite ack-reject, zero action (AC-1). | [NET-NEW] — 0 in-repo GitHub-authz precedent. Replier is the sole authority; parent author supplies only data. External authz evaluated *outside* the LLM (Teleport: injection "steers systems with legitimate access," so authz must not be model-self-policed). |
| **Fork-only push target (C5 / H5)** | `gh_call()` unconditionally injects `--repo IronbellyOrg/IronClaude`; unit test asserts no argv path can omit it; optional CI grep-guard against raw `gh` outside `gh.py`. Never `--approve`/`--request-changes`; humans merge. | First code-level enforcement of the CLAUDE.md fork-only rule (today prose-only). Severity rubric already forbids merge-state changes — reinforces §20 non-goal. |
| **Short-lived host-side push tokens** | Long-lived read+comment credential lives only in the Dispatcher; push uses a short-lived, narrowly-scoped token minted host-side at push time (OD-2: GitHub App vs fine-grained PAT — open). Secret files `chmod 600`, owner-scoped, sourced via systemd `EnvironmentFile=`. | AWS AgentCore "never put the token in the VM; short-lived scoped token, rotatable/revocable"; GitHub/StepSecurity/Sysdig hardening: short-lived OIDC-style over static PATs; keep secrets off the runner. (Note: `~/.aienv` is content-sourcing model; on-disk it is 644, so cite the chmod-600 discipline on its own merit.) |
| **Sandbox network egress** | Deny-by-default egress; allowlist only the Anthropic proxy (`:4000/cli`), `api.github.com`, and single-repo git. No host home mount; `--dangerously-skip-permissions` is safe **only** because of this boundary. | Coder "Agent Firewall / default-deny egress" (DoD-used); microsandbox/brood-box/cplt deny-all + domain allowlist; GitHub runner guidance "restrict runner network access." |
| **Per-PR mutation lock (fail-closed)** | Per-PR `fcntl.flock(LOCK_EX)` serializes tree mutations and push; a failed lock acquisition for a push **fails closed** (the only in-repo flock precedent — freshness bash hooks — fails *open* and must NOT be copied). | [NET-NEW] in Python. Prevents the "parallel sessions share git index" hazard the repo has hit before. |
| **Immutable audit trail** | Append-only JSONL audit log (closed `EventType` enum) distinct from the state ledger, written atomically, forwarded/persisted before Runner teardown. | NIST AI RMF / ISO 42001 reference audit + injection controls; tamper-evidence (exploits "revert the title and delete the PR to erase evidence"). |

### 14.4 Scalability Requirements

| Dimension | Current Target | Future Target | Approach |
|-----------|----------------|---------------|----------|
| Concurrent PRs / triggers | 1 Runner per trigger, serialized per-PR via `flock` | Bounded concurrent Runner pool across distinct PRs | Disposable per-trigger Runner; per-PR lock prevents tree-mutation races; Dispatcher schedules dispatch. |
| Repositories | Single fork (`IronbellyOrg/IronClaude`) | N/A (fork-scoped by design) | `gh_call()` hard-pins `--repo`; single-repo egress allowlist. Cross-repo is explicitly out of scope. |
| Poll volume vs GitHub rate limits | Steady-state polling within primary rate limit | Backoff-aware adaptive polling | ETag/304 conditional requests + `Retry-After`/`X-RateLimit-Remaining` honoring; ≥30s poll floor. |
| State/ledger growth | Append-only JSONL with truncated-last-line replay tolerance | Periodic compaction/rotation | Atomic `os.replace` snapshot + `O_APPEND` event stream; ledger is SoT, in-memory counters derived from it on startup. |

### 14.5 Data & Analytics Requirements

| Data Type | What to Collect | Why | Storage/Retention |
|-----------|-----------------|-----|-------------------|
| Trigger ledger | `(trigger_comment_id, parsed_flag_hash)` claim key, intent record, outcome record, recorded push SHA | At-most-once trigger claiming; two-phase RESUME after restart; idempotency/dedup across rounds (also keep content `fix_key = sha256(path+line+body)`) | On-disk JSONL, atomic-write; durable across restarts (SoT) |
| Audit event log | Closed `EventType` taxonomy: `poll`, `trigger_seen`, `authz_check`, `parse_mention`, `intent`, `claude_process_spawn`, `validation`, `push`, `reply_posted`, `thread_resolved`, `round_outcome`, terminal states | Tamper-evident provenance; debugging; NIST AI RMF / ISO 42001 evidence; "every trigger + exact opComment input + decision" | Append-only JSONL (distinct from ledger); dual `jsonl`+`md` writer; forwarded before Runner teardown |
| Probe-locked detection constants | Augment bot login, `in_reply_to_id` shape, `databaseId` shape (captured from a throwaway fixture PR before parser code) | §21.3 probe-first gate; locks unknown GitHub-API shapes against real bytes via `DetectionContractLocked` | Committed config constants/fixtures |
| Runner run logs | `claude -p` stream-json output, exit code, applied-edits count, validation status | StuckRun detection (timeout→124); push-decision predicate inputs; round correlation | Per-trigger log file; persisted before sandbox teardown |
| Adversarial injection test corpus | Public PoC payloads (hidden `-- Additional instruction --` blocks, `gh issue edit $TOKEN` exfil, white-on-white text, fake "authorized/urgent" framing) | Release-blocking injection-containment acceptance gate (OWASP #7 / CSA red-team gate) | Test fixtures under `tests/cli/remediate/` |

**Analytics Tools:** Native JSONL ledger + audit log queried via `gh`/`jq`-style tooling and the `superclaude remediate` status surface; no external analytics dependency. Provenance/audit is surfaced as a first-class queryable artifact (governance-by-design positioning).

---

## 15. Technology Stack

### 15.1 Backend

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| Language | Python | ≥ 3.10 | Project standard; all ops via UV ([CODE-VERIFIED] `pyproject.toml`, `>=3.10`). |
| CLI framework | Click | ≥ 8.0.0 | `remediate_group` registered in `cli/main.py` via deferred-import idiom [CODE-VERIFIED at `:400-438`]; pin `name="remediate"`. |
| Agent executor | `ClaudeProcess` wrapping `claude --print` (`claude -p`) | reuse (`cli/pipeline/process.py:72`) | Headless spawn: stdin prompt delivery (chunked 64 KiB, EINTR-retry, BrokenPipe-safe), 16 MiB pre-spawn guard, process-group kill (`os.setpgrp`→`os.killpg`), `timeout_seconds`, `stream-json` output, lifecycle hooks. **Required mods:** allowlist `build_env()` + `cwd`/`os.chdir` for sandbox checkout. |
| Decision core | `superclaude.pr_submit` (`fsm`, `severity_router`, `classifier`, `detection`, `models`) | reuse (built+tested) | Import the pure brain; supply real I/O hands. Provides autonomy gate, 5-predicate push conjunction, `should_halt_rounds` (`>=` fence-post), severity remap, `DetectionContractLocked`, `EventType` enum, dual-shape login parser. |
| LLM models | Claude via `~/.aienv` proxy | `:4000/cli` base, `T2Model*` ids | Only credential class allowed into the sandbox; all GitHub creds stay host-side. Default to most-capable Claude for the reasoning Runner. |
| Severity routing | `sc-auggie-review-protocol/refs/severity-rubric.md` + `pr_submit.severity_router` | reuse | 5 tiers (Critical/High/Medium/Low/Nit); Augment severity is a hint, re-graded. Routes Critical/High→`--depth deep --fix`, Medium→`--fix`, Low/Nit→report-only, unknown→Medium fail-safe. |
| State store | JSONL ledger + audit log | — | Atomic write via `os.replace` (not `os.rename`) + randomized same-dir tmp + `finally` cleanup (precedent: `cli/recommend/cache.py`, `swarm/state.py`); `O_APPEND` event stream; `fcntl.flock` (fail-closed) [NET-NEW in Python]. |
| GitHub I/O | `gh` CLI (REST + GraphQL via `gh api graphql`) | — | Polling/ingest (ETag/304), `in_reply_to_id` parent resolution, reply-to-thread (`pulls/<N>/comments/<id>/replies`), `resolveReviewThread` + `reviewThreads`/`databaseId` pagination [NET-NEW in Python; a reference bash flow exists in the untracked parallel V1 `sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`, no committed Python caller]. All routed through `gh_call()` `--repo` injector. |

### 15.2 Frontend / Control Surface

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| User interface | GitHub PR review-comment `@bot` mention grammar | N/A | **No GUI / web / new slash command.** The entire user-facing control surface is a ~4-token comment grammar: autonomy level (`propose\|patch\|fix\|push\|resolve`), `--depth`, `--scope`, `--rounds`. Default (no flag) = `propose`. |
| Operator surface | `superclaude remediate` CLI + systemd | N/A | Operator-facing only; status/ledger inspection. End users never touch the CLI. |

### 15.3 Infrastructure

| Component | Technology | Notes |
|-----------|------------|-------|
| Long-lived host | systemd service (Dispatcher) | `Restart=always`, `WatchdogSec`/`sd_notify` supervision; `EnvironmentFile=` for chmod-600 secrets. `deploy/remediate-bot/` [NET-NEW — no `deploy/` dir, no `.service` units in repo today]. |
| Execution sandbox (Runner) | Container or microVM — **OD-1 open** | External consensus: shared-kernel containers insufficient for untrusted-comment-driven code; production pattern is Firecracker/gVisor/Kata/libkrun microVM or Landlock+seccomp (cplt-style). Refs: microsandbox, brood-box, cplt. Deny-by-default egress; no host home mount; ephemeral PR-head checkout. |
| Containerization (MCP only, not Runner) | Docker (existing, MCP-gateway only) | [CODE-VERIFIED] the only in-repo Docker usage is `install_mcp.py` for the MCP gateway — NOT a code-execution sandbox. Runner sandbox is greenfield. |
| Secret management | systemd `EnvironmentFile=` + short-lived push tokens | Long-lived read+comment creds in Dispatcher; push token minted host-side, narrowly scoped, rotatable (OD-2: App vs fine-grained PAT). |
| CI/CD | GitHub Actions (existing project CI) + UV | `make lint` (ruff check) + `ruff format --check` + `make verify-sync` + `uv run pytest`. Doc⇆CLI parity test for the `remediate` group. |
| Monitoring / alerting | Audit-log events + `StuckRun` alert | Keys on `ClaudeProcess.timeout_seconds` (timeout→124); `claude_process_spawn`/`exit` lifecycle hooks emit audit events. |
| Logging | Dual-format JSONL + Markdown writer | Precedent: `cli_portify/logging_.py` (`execution-log.{jsonl,md}`). Audit log distinct from state ledger; forwarded before Runner teardown. |
| Testing | pytest (via UV) | `tests/cli/remediate/` [NET-NEW]; mirror `tests/cli/test_cli_registration.py`; release-blocking adversarial injection suite. |
| Build system | hatchling (PEP 517) | Project standard; package `superclaude`. |

---

> **Open technical decisions carried into TDD (from research):**
> 1. **OD-1 — Sandbox tech** (container vs microVM): gates R4/S2/§15; largest greenfield surface; resolve early.
> 2. **`build_env()` allowlist mechanism**: add `env_mode="allowlist"`/`base_env` to the shared `ClaudeProcess` primitive (touches sprint/swarm/pipeline — needs regression gate) vs. scrub env in the sandbox parent. Gated by AC-7 secret-scrape test.
> 3. **`ClaudeProcess` `cwd`**: add a `cwd` kwarg vs. `os.chdir` in the one-shot Runner entrypoint.
> 4. **OD-2 — Push-token mechanism**: GitHub App vs fine-grained PAT.
> 5. **§21.3 probe-first gate** (hard prerequisite): lock `in_reply_to_id`/`databaseId`/Augment-bot-login + `resolveReviewThread` GraphQL shape against a throwaway fixture PR before any parser/threading code — the #1 build-blocking unknown no existing code can resolve.
> 6. **Citation corrections** (pre-TDD doc fixes): swarm `commands.py:2269` is a `--watch` iteration cap, not a durable counter — re-point round counter to `pr_submit/fsm.py:should_halt_rounds` and persistence to `swarm/state.py:write_state`; `os.rename`→`os.replace`.

EXIT_RECOMMENDATION: CONTINUE
