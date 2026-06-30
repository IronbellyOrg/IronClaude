<!--
SYNTHESIS FRAGMENT — PRD Sections 9-12 (Competitive Analysis, Assumptions & Constraints,
Dependencies, Scope Definition) for PR Auto-Remediation V2.0 (Mention-Triggered Headless Bot).
Source: research/01-08 (codebase reuse verification) + research/web-01..03 (market/ecosystem).
NOTE: cli/remediate/ is greenfield (CODE-VERIFIED absent). V2.0 capabilities below are TARGET
design requirements, not current product capabilities. Only the reuse anchors (ClaudeProcess,
pr_submit/ decision core, severity rubric, swarm atomic-write) are CODE-VERIFIED as existing.
-->

## 9. Competitive Analysis

> **Scope note:** PR Auto-Remediation V2.0 competes directly with the standalone "mention →
> autonomous PR fix" product category, so a full competitive landscape is warranted. All
> capabilities attributed to **Our Product (V2.0)** are *target design requirements* — the
> `cli/remediate/` group is greenfield (CODE-VERIFIED absent today); only the underlying reuse
> primitives (`ClaudeProcess`, `pr_submit/` decision core, severity rubric) exist in code.

### 9.1 Competitive Landscape

| Competitor | Type | Target Market | Key Strengths | Key Weaknesses |
|------------|------|---------------|---------------|----------------|
| **GitHub Copilot Coding Agent** | Direct | GitHub-hosted teams | Category leader (GA Sep 2025); `@copilot` mention → autonomous draft PR in an ephemeral GitHub-Actions env; runs tests/linters; never auto-merges; trigger-er's approval doesn't count toward required review | **GitHub-hosted only — not self-hostable** (Copilot Enterprise "cloud-dependent"); **unconditionally opens a child PR even when the comment says "don't"** — #1 documented complaint (GitHub Community #190027: "intent ignored, no conversational mode, no middle ground"); inherits `pull_request_target` secret-injection exposure |
| **Claude Code GitHub Action (`@claude`)** | Direct | GitHub-hosted teams using Claude | Same `claude -p` lineage as our Runner; `@claude` mention → analyze/fix in isolated env; multi-agent code review with severity markers + `file:line` citations; <1% findings marked incorrect (vendor internal) | Runs as a **GitHub-Actions cloud job** with repo read/write; `@claude` is a workflow-`if` convention, not a hardened untrusted-comment envelope; secrets live in the runner |
| **Devin (Cognition)** | Direct | Enterprise (Goldman Sachs, Santander, Nubank) | Autonomous PR review/fix; clones repo, runs code to verify; ~5–10 min/PR; explicit pre-push git-hook guard against agent pushes; positioned "extra set of eyes, not a replacement" | Cloud SaaS — **not on-prem**; full-autonomy end of the spectrum; ~$10.2B valuation pricing tier |
| **CodeRabbit / PR-Agent (Qodo) / Ellipsis** | Indirect (review tier) | Broad GitHub/GitLab | CodeRabbit: 40+ analyzers + interactive PR-comment chat; PR-Agent: open-source, model-agnostic, self-hostable, `/review` `/improve` commands; Ellipsis: "automated fix implementation" ($20/user/mo) | Mostly **review/suggest-only** (CodeRabbit, PR-Agent stop at proposing); thin or absent untrusted-input/secret-separation story; the fix-implementing ones run cloud-Action-hosted |
| **Tabnine / Windsurf / Qodo (air-gapped tier)** | Substitute | Regulated (defense, finance, healthcare, gov) | Lead the on-prem/air-gapped segment with compliance certs (SOC2 Type II, FedRAMP High, DoD IL5, ITAR, zero-retention) | Ship **inline / IDE assistants**, NOT mention-triggered autonomous PR-remediation bots — different product shape; do not occupy the remediation-bot category |

### 9.2 Feature Comparison Matrix

| Feature | Our Product (V2.0, target) | Copilot Coding Agent | Claude `@claude` Action | Devin | CodeRabbit / PR-Agent |
|---------|---------------------------|----------------------|-------------------------|-------|-----------------------|
| Mention-triggered (`@bot` in PR comment) | ✅ | ✅ | ✅ | ⚠️ (PR-event, not mention) | ⚠️ (slash-command) |
| On-prem / self-hosted (no cloud runner) | ✅ | ❌ | ❌ | ❌ | ⚠️ (PR-Agent only) |
| Headless (no IDE, no GitHub-Actions host) | ✅ | ❌ | ❌ | ❌ | ⚠️ |
| File-write + git-push remediation | ✅ | ✅ | ✅ | ⚠️ (review-centric) | ⚠️ (Ellipsis only) |
| Propose-only **default** + intent evaluation | ✅ | ❌ (over-triggers) | ❌ | ✅ | ✅ |
| Live per-trigger authorization gate (collaborator-permission) | ✅ | ⚠️ (org policy) | ❌ (workflow `if`) | ❌ | ❌ |
| Untrusted-comment injection containment (data-in-envelope) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Secret separation (Runner holds no push token) | ✅ | ❌ (`pull_request_target` exposure) | ❌ | ⚠️ | ❌ |
| Never auto-merge (humans merge) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Reply-to-thread + thread resolve | ✅ | ⚠️ | ⚠️ | ⚠️ | ✅ (review chat) |

**Legend:** ✅ Full support | ⚠️ Partial/Limited | ❌ Not supported

### 9.3 Competitive Positioning

**Our Unique Differentiation:**

1. **On-prem × mention-triggered remediation — an empty market intersection.** Copilot / Amazon Q / Cursor lead mention-triggered or autonomous coding but are cloud-only / not self-hostable; Tabnine / Windsurf / Qodo lead air-gapped/on-prem but ship inline/IDE assist, not autonomous PR-remediation bots. **No incumbent occupies both axes** — the regulated segments (defense, finance, healthcare, telecom, government) that are structurally locked out of cloud-hosted agents are addressable only by an on-prem bot.
2. **The split-host architecture is the industry-prescribed injection mitigation.** CSA Labs names "architectural separation of the agent's reasoning layer from the credential-holding execution layer" as *the fundamental mitigation* for prompt injection — a 1:1 description of our tokenless Runner (reasoning) + credential-holding Dispatcher (policy/execution). Independently mirrored by Simon Willison's Dual-LLM pattern, the Anthropic/ETH/DeepMind design-patterns paper, and AWS AgentCore's "never put the token in the VM."
3. **Propose-only default + authorization gate answers the market leader's #1 complaint.** Copilot Coding Agent unconditionally opens a child PR even when the comment says "don't"; our live authorization gate + conservative propose-only default is the "middle ground / confirmation step" users explicitly ask for — and aligns with the universal safe default (draft-PR, human-approves, agent-cannot-self-merge) across Copilot, Continue ("Level 2 Continuous AI"), Devin, and Anthropic's 2026 trends report.

**Positioning Statement:**
"For repo maintainers and on-call reviewers on regulated, self-hosted code who cannot send their source to cloud-hosted runners, **PR Auto-Remediation V2.0** is an on-prem, mention-triggered remediation bot that turns an authorized `@bot` reply into a sandboxed, propose-by-default fix. Unlike GitHub Copilot Coding Agent and the `@claude` GitHub Action, our product runs headless on-prem with a split Dispatcher/Runner host that treats the triggering comment as untrusted data and keeps push credentials out of the agent's reach."

### 9.4 Competitive Response Plan

| If Competitor Does... | Our Response |
|-----------------------|--------------|
| Copilot/GitHub ship a self-hosted-runner variant of the Coding Agent | Lead with the secret-separation + untrusted-comment-envelope story (sidesteps the `pull_request_target` exposure underlying 2026 GitHub-Actions agent CVEs) and the live per-trigger authorization gate, which a GitHub-Actions host does not provide natively |
| Copilot adds an "evaluate intent before acting" confirmation step | Emphasize the deeper differentiation — on-prem deployment, propose-only-by-default lattice, and architectural injection containment — not just the intent check |
| An air-gapped IDE vendor (Tabnine/Windsurf/Qodo) adds a mention-triggered PR-remediation bot | Compete on the governance posture: two-phase audit ledger, deterministic loop-guard (push budget 2/cap 5), fork-only `--repo` code enforcement, and OWASP-LLM-Top-10-aligned-by-construction design as procurement evidence for the EU AI Act (Aug 2026) high-risk deadline |

---

## 10. Assumptions & Constraints

### 10.1 Technical Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| TA-1 | `ClaudeProcess` (`cli/pipeline/process.py:72`) is reusable as the Runner's headless `claude -p` executor — `build_command()` flags, chunked-stdin prompt delivery (bypasses 128KB argv limit), 16 MiB `PROMPT_MAX_BYTES` guard, process-group kill, and `timeout_seconds=6300` all behave as the spec relies on | Runner cannot spawn `claude -p` reliably; large `opComment` envelopes fail or deadlock | CODE-VERIFIED across research 01-08 (exact line, byte-accurate flag string, stdin delivery, size guard) |
| TA-2 | `ClaudeProcess.build_env()` can be given an allowlist/replace mode (or the Runner spawned from a pre-scrubbed parent) so the Runner env excludes `GH_TOKEN`/push token/`ANTHROPIC_*` | INV-001/SC-7/AC-7 secret-isolation fails silently — push credential leaks into the untrusted-comment-processing Runner | CODE-CONTRADICTED as-is: `build_env()` is additive-merge over `os.environ.copy()` and **cannot subtract** inherited keys; requires a `base_env`/`env_mode="allowlist"` code change + an `assert "GH_TOKEN" not in runner_env` regression test (AC-7 `/proc/<pid>/environ` scrape) |
| TA-3 | `ClaudeProcess` can run the child in the sandbox PR-head checkout via a new `cwd` parameter or a Runner-side `os.chdir()` | Runner edits the wrong working tree | CODE-CONTRADICTED: `Popen` at `process.py:192` passes no `cwd=`; needs a small code change or `os.chdir()` in the one-shot Runner |
| TA-4 | The V1.0 `pr_submit/` pure decision core (`fsm.evaluate_push_decision`, `should_halt_rounds`, `severity_router`, `classifier`, `detection.DetectionContractLocked`, `models`) is import-and-extend reusable for the autonomy gate, round counter, severity routing, and probe-lock | V2.0 rebuilds tested logic from scratch — drift risk, divergent severity grading vs the `sc:pr-submit` skill, double-maintenance | CODE-VERIFIED present + tested (`tests/pr_submit/*`); **landing in parallel today** (still git-untracked) — `loop_guard.py`/`run_log.py`/`recovery.py` have since landed built + tested (`test_loop_guard.py`/`test_run_log.py`/`test_crash_recovery.py`); coordinate so V2 work doesn't race the in-flight V1 build |
| TA-5 | The real GitHub-API shapes for the trigger surface — `in_reply_to_id`, comment `databaseId`, `reviewThreads` pagination, the Augment bot login — can be locked from a throwaway-PR probe before parser code is written | Parser built against guessed bytes; "resolved the wrong thread" (INV-010) class bug | Probe-first gate (§21.3); no committed/tracked precedent, but a reference reply→resolve bash flow has since landed in the untracked parallel V1 `sc-pr-submit-protocol` skill (`scripts/reply-resolve-thread.sh` covers `in_reply_to`/`reviewThreads`/`resolveReviewThread`) — crib its shape, but the live probe still must lock the real `in_reply_to_id`/`databaseId` bytes |
| TA-6 | ETag/304 conditional polling + rate-limit (`If-None-Match`/`Retry-After`/`X-RateLimit-Remaining`) discipline can be built net-new for the Dispatcher ingest | Polling either rate-limit-bans the bot or misses triggers | CODE-VERIFIED no in-repo precedent (grep = 0); D3 is greenfield |
| TA-7 | A container or microVM sandbox can run `claude --dangerously-skip-permissions` safely with deny-all egress + an endpoint allowlist that still reaches the Anthropic proxy (`~/.aienv` `:4000/cli`) and `api.github.com` | Untrusted-comment-driven code execution escapes isolation; or the proxy is unreachable and the Runner cannot call the model | OD-1 open decision; shared-kernel containers flagged insufficient by external consensus (Firecracker/gVisor/Kata/libkrun or Landlock+seccomp recommended); proxy reachability must be confirmed against the chosen topology |

### 10.2 Business Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| BA-1 | "Autonomous pull request resolution / security vulnerability remediation" is an emerging high-value, not-yet-commoditized use case worth occupying | Effort spent on a saturating category | Analyst-named emerging high-value use case (marketintelo); fast-growing agentic-dev market (varied estimates ~$10.4B 2025 / CAGR ~39.5%; ~$12.6B by 2028 / CAGR 24%) |
| BA-2 | The on-prem/governed segment (~29% of market, security-driven) is real and under-served by cloud-first incumbents | Differentiation axis is illusory | Mordor: cloud-hosted held 71.3% (2025), self-hosted the explicitly under-served minority; VDF/TrueFoundry/Greptile name governed on-prem as the hard, under-served problem |
| BA-3 | A conservative propose-only, safety-first posture wins more trust than raw autonomy in a trust-constrained market | Product perceived as a capability-limited laggard | 84% adoption vs ~3–33% trust AI output; "auto-post → muted bots within months"; Anthropic 2026: "collaborative, not delegated" |

### 10.3 User Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| UA-1 | The `@bot` mention-in-a-review-reply trigger is idiomatic and low-adoption-risk for maintainers | Users don't discover or trust the trigger | Established UX standard: `@claude`, `@copilot`, `@review-bot`, `/gs review` — mention-as-command is the de-facto convention |
| UA-2 | A 4-token mention grammar (autonomy level + `--depth` + `--scope` + `--rounds`), default `propose`, is the entire control surface users need | Users want richer control or are confused by defaults | Mirrors incumbents' minimal command surfaces; default-propose is the market-validated safe posture |
| UA-3 | The *replier* (authorized write-collaborator) is the sole authority; the *parent comment author* supplies only data | An unauthorized or read-only user triggers consequential action | Live per-trigger collaborator-permission gate (D5/C4); read-permission mention → polite ack-reject, zero action (AC-1) |

### 10.4 Constraints

| Type | Constraint | Impact on Product | Mitigation |
|------|------------|-------------------|------------|
| **Technology** | No Python `gh` subprocess wrapper exists anywhere in the repo; all `gh` I/O today is skill-markdown/bash | H5 (`gh_call()` with unconditional `--repo` injection) is foundational net-new, the first *code* enforcement of fork-only `--repo` — must be built and tested before any `gh`-calling code | Build H5 first (§21.3 sequencing); unit test asserting no argv can omit `--repo IronbellyOrg/IronClaude`; optional CI grep-guard against raw `gh` outside `gh.py` |
| **Technology** | No execution sandbox, no systemd/`deploy/` precedent in-repo (OD-1 unresolved: container vs microVM) | The 24/7 daemon, sandbox image, and `deploy/remediate-bot/` units are the largest greenfield surface and gate R4/S2 | Resolve OD-1 early; `eval/isolation.py` scratch-root model is partial prior art for filesystem confinement only |
| **Security/Regulatory** | Prompt injection is OWASP's #1 LLM/agentic risk and is effectively unsolved (no fool-proof prevention); EU AI Act high-risk compliance deadline Aug 2026 | Forces defense-in-depth (envelope + secret separation + propose-only + bounded scope), not a single filter; injection red-teaming becomes a release gate | opComment as untrusted DATA in a CONTROL/DATA envelope delivered via stdin (never `/sc:troubleshoot "${opComment}"` interpolation); align to OWASP LLM01:2025, OWASP Top 10 for Agentic Apps (Dec 2025), NIST AI RMF, ISO 42001 |
| **Process / SoT** | Fork-only PR target: `origin = IronbellyOrg/IronClaude`, never upstream `SuperClaude-Org`; `.claude/` is gitignored sync-dev output | Autonomous pushes to the wrong repo = exposure of private fork work (historically burned the operator); careless staging breaks `verify-sync` | C5 fork-only `--repo` invariant enforced in H5 code; secret-source `~/.aienv` proxy contract (`:4000/cli` + `T2Model*` only) is the sole credential allowed into the sandbox |
| **Operational** | Poll interval floor ≥30s; per-PR push budget default 2, hard cap 5 | Bounds GitHub API load and remediation-loop blast radius | Reuse `pr_submit` `MIN_POLL_INTERVAL=30`, `DEFAULT_MAX_ROUNDS=2`, `HARD_CAP_MAX_ROUNDS=5` (V1.0 already chose these); disk-authoritative ledger is SoT, counter derived on startup |
| **Resource** | V1.0 `pr_submit/` decision core is landing in parallel; `~/.aienv` secret file is 644 (not the 600 the spec cites as exemplar) | Risk of two teams building overlapping ledger/round-counter logic; false secret-hygiene provenance | Sequence/own V1-core completion vs V2-host build; require `chmod 600` + systemd `EnvironmentFile=` on its own merits, don't cite `.aienv` as the permissions exemplar |

---

## 11. Dependencies

### 11.1 External Dependencies

| Dependency | Type | Owner | Risk Level | Contingency |
|------------|------|-------|------------|-------------|
| GitHub REST + GraphQL API (comment polling, `pulls/<N>/comments`, `pulls/<N>/comments/<parent>/replies`, `reviewThreads`, `resolveReviewThread`) | API | GitHub | High | Reply/resolve GraphQL has no committed Python precedent (a reference bash flow now exists in the untracked `sc-pr-submit-protocol` skill); lock real shapes via §21.3 probe before parser code; reply-only fallback if `resolveReviewThread` proves unreliable |
| `gh` CLI (host-side GitHub I/O, invoked via the H5 wrapper) | Tool | GitHub | Medium | All calls routed through `H5.gh_call()` with unconditional `--repo IronbellyOrg/IronClaude`; no raw `subprocess(["gh", …])` permitted |
| Anthropic model access via the `~/.aienv` proxy (`:4000/cli` base + `T2Model*` model ids) | API | Internal proxy / Anthropic | High | The **only** credential class allowed into the sandbox; sandbox egress allowlist must reach the proxy host; `PromptTooLargeForArgv` (16 MiB guard) bounds envelope size |
| `claude` CLI (`claude --print …`, spawned by the Runner via `ClaudeProcess`) | Tool | Anthropic | Medium | Pinned flags via `build_command()`; `--dangerously-skip-permissions` safe **only** inside the sandbox boundary |
| Sandbox runtime (container or microVM — Firecracker/gVisor/Kata/libkrun, or Landlock+seccomp) | Infrastructure | Operator (OD-1) | High | OD-1 open decision; shared-kernel containers flagged insufficient for untrusted-code execution; build-vs-buy refs: microsandbox, brood-box, cplt |
| `systemd` (Dispatcher daemon supervision: `Restart=always`, `WatchdogSec`, `EnvironmentFile=`) | Infrastructure | Operator | Medium | No existing daemon precedent in the CLI; spike `sd_notify`/`WatchdogSec` integration; `deploy/remediate-bot/` is greenfield |
| Augment review bot (the upstream producer of the review comments the bot remediates) | Service | Augment | Medium | Bot login locked as a config constant via the §21.3 probe; unknown login → not-detected (safe default) |

### 11.2 Internal Dependencies

| Dependency | Type | Owner | Status | Target Date |
|------------|------|-------|--------|-------------|
| `ClaudeProcess` (`cli/pipeline/process.py:72`) — shared headless-spawn primitive | Component | Pipeline/CLI | Built (needs back-compat `base_env`/`cwd` additions) | Before R2/R4 |
| `pr_submit/` decision core (`fsm`, `severity_router`, `classifier`, `detection`, `models`) | Package | pr_submit (V1.0) | ~60% built + tested; landing in parallel | Coordinate before H1/H2/S1 |
| `pr_submit/` `loop_guard.py` / `run_log.py` / `recovery.py` (write-ahead JSONL, crash recovery) | Module | pr_submit (V1.0) | Built + tested (untracked, landing in parallel) | Build the durable two-phase ledger here, not a forked `remediate/ledger.py` |
| `sc-auggie-review-protocol/refs/severity-rubric.md` (5-tier rubric) | Reference | auggie-review skill | Built; already encoded in `pr_submit.severity_router` | Import the router, don't re-parse the markdown |
| `swarm/state.py` `write_state` (atomic tmp + `os.replace`) + `models.py:1141` `SwarmState` | Pattern | swarm | Built | Borrow the atomicity idiom for the ledger; append-only `O_APPEND`+`flock` model is net-new |
| `cli/main.py` deferred-import group registration (`# noqa: E402,I001`) | Wiring | CLI | Built | Add `remediate_group` + `add_command(name="remediate")`, else the command is dead |
| `roadmap/remediate_executor.py` (existing `ClaudeProcess`-driven remediation: allowlist, snapshot/rollback, diff-size guard, patch-apply) | Component | roadmap | Built | Mirror-shape analog for R2/R4 executor + patch-emit/rollback path |

### 11.3 Cross-Team Dependencies

| Team | Dependency | What We Need | When Needed | Status |
|------|------------|--------------|-------------|--------|
| V1.0 `pr_submit` build | Decision-core completion + module layout | Settled `fsm`/`severity_router`/`models` APIs and the (now-landed but untracked) `loop_guard`/`run_log`/`recovery` ownership, so V2 imports rather than forks | Before H1/H2/S1 build | In flight (landing today) — race risk |
| Pipeline/CLI (shared primitive owners) | `ClaudeProcess` env-allowlist + `cwd` changes | Back-compatible `base_env`/`env_mode` and `cwd` additions, re-tested against sprint/roadmap/swarm callers | Before R2 at propose-only | Open design decision |
| Security / operator | OD-1 sandbox tech + OD-2 push-token mechanism | Chosen isolation tier (container vs microVM) and token type (GitHub App vs fine-grained PAT) — both gate R4/H3 | Early (gates largest greenfield surface) | Open (OD-1, OD-2) |

---

## 12. Scope Definition

### 12.1 In Scope (Phase 1 / MVP)

| Category | Included | Notes |
|----------|----------|-------|
| **CLI host (D1)** | New `superclaude remediate` CLI group under `src/superclaude/cli/remediate/`, registered in `cli/main.py` via the deferred-import `# noqa: E402,I001` idiom | Mirrors `sprint`/`swarm`/`pipeline`; runs headless outside any Claude session. Feature home is `cli/remediate/`; the empty top-level `remediation/` placeholder is to be deleted/ignored |
| **Dispatcher (D2–D6, S2)** | systemd daemon: poll (≥30s floor) → ETag/304 ingest → `@bot` mention grammar parse → live collaborator-permission authz gate → parent-comment (`opComment`) resolution → trigger claim in the ledger | The replier is the sole authority; read-permission mention → polite ack-reject (AC-1). D5/D6/D3 are greenfield (no in-repo prior art) |
| **Mention grammar (D4)** | Whitelisted tokens: autonomy level (`propose\|patch\|fix\|push\|resolve`), `--depth`, `--scope`, `--rounds`; **default = `propose`** | The entire end-user control surface — a 4-token comment; no GUI/web/new slash command |
| **Runner (R1–R4)** | Ephemeral, sandboxed, disposable per-trigger `claude -p` against an isolated PR-head checkout; `opComment` delivered as JSON DATA in a CONTROL/DATA envelope via stdin (never `"${opComment}"` interpolation); emits diff (propose) or sandbox-branch commit (fix) | Runner holds NO long-lived push/GitHub secret (INV-001/SC-7); only the `~/.aienv` proxy credential is allowed in |
| **Severity routing (S1/§17)** | Re-grade each Augment finding through the reused rubric (`pr_submit.severity_router`): Critical/High → `--depth deep --fix`; Medium → `--fix`; Low/Nit → report-only; unknown → Medium fail-safe | Augment severity is a hint, not authoritative |
| **Autonomy gate (H2)** | Effective level = lattice-min over {mention flag, authz projection, validation} then off-lattice HALT short-circuits (`needs_human_decision`, push-budget==0); structurally impossible to reach `push` without explicit flag AND write-permission AND passing validation | Extends `pr_submit.evaluate_push_decision` (4 of 5 predicates carry over); `needs_human_decision` HALT inherited verbatim from V1.0 FR-4.4 |
| **Loop-guard + two-phase ledger (H1, §9/§10)** | Disk-authoritative, atomic-write (tmp + `os.replace`), append-only JSONL with per-PR `flock` (fail-closed); per-PR push budget default 2, hard cap 5; SHA-correlated round counting; intent-without-outcome ⇒ RESUME, never silent re-execute | Genuinely net-new durable state core; borrows swarm's atomicity idiom |
| **Host-side push + reply (H3, H4-reply)** | Dispatcher pushes with a short-lived host-side token; replies to the review thread with summary + pushed SHA | Reply-to-thread templates off auggie-review posting precedent |
| **gh wrapper (H5)** | A single `gh_call()` chokepoint that unconditionally injects `--repo IronbellyOrg/IronClaude`; no code path can call `gh` without it | First *code* enforcement of the fork-only C5 invariant; build + test first |
| **Audit log (§14)** | JSONL event stream (poll, trigger_seen, authz_check, parse_mention, intent, `claude_process_spawn`, validation, push, reply_posted, round_outcome) distinct from the state ledger, surviving Runner teardown | Start from `pr_submit.models.EventType` and extend; surface as a first-class queryable audit artifact |

### 12.2 Out of Scope (Phase 1 / MVP)

| Item | Reason | Target Phase |
|------|--------|--------------|
| ❌ Thread **resolve** (`resolveReviewThread` GraphQL, `resolve` autonomy level) | Highest-risk net-new GitHub surface; no committed Python precedent (a reference bash flow exists in the untracked `sc-pr-submit-protocol` skill); `databaseId` pagination shape unverified until the §21.3 probe | Phase 2 (after probe locks the GraphQL shape) |
| ❌ Dual-LLM hardening of `opComment` (quarantined LLM pre-normalizes the parent comment into structured intent before the acting Runner) | Defense-in-depth enhancement atop the envelope; not required for the propose-only MVP | Phase 2 |
| ❌ Auto-apply / auto-push as a non-default | Trust data says auto-apply is a retention liability; ships only as opt-in, per-repo, gated behind the same authorization layer | Phase 2+ (opt-in only) |
| ❌ Multi-repo / multi-PR / multi-branch per trigger | Matches incumbent guardrail (single-repo, single-branch, one PR); bounds blast radius for MVP | Phase 3 |
| ❌ `offer-pr-review.sh` hook integration as a distributed touchpoint | Depends on reconciling the `src/superclaude/hooks/hooks.json` SoT drift first | Deferred / optional |

### 12.3 Permanently Out of Scope

| Item | Reason |
|------|--------|
| ❌ Modifying merge state (`gh pr review --approve` / `--request-changes`, auto-merge) | Humans merge — inherited non-goal, reinforced by the severity rubric's code-enforced "the verdict does NOT translate into approve/request-changes" invariant |
| ❌ V1.0's in-session Monitor-tool host | Fully replaced by the split Dispatcher(systemd)+Runner(sandbox) headless host (the entire reason V2.0 exists); the V1.0 *decision core* is reused, the *host* is not |
| ❌ Long-lived push/GitHub credentials inside the Runner | Architectural invariant — the Runner processes untrusted comment text and must never hold an exfiltratable consequential credential (the precondition that produced the 2026 "Comment and Control" CVEs) |
