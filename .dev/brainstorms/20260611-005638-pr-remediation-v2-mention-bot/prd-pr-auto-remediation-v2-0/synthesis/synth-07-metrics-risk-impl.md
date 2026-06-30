<!--
SYNTHESIS FRAGMENT — Sections 19, 20, 21.3, 21.4, 21.5
Product: PR Auto-Remediation V2.0 (Mention-Triggered Headless Bot)
Source: research/01-08 (codebase reuse verification) + web-01/02/03 (market & security)
Every claim traces to a research file. [CODE-VERIFIED] marks claims confirmed against live
source; all other items are requirements/targets for a greenfield (to-be-built) subsystem.
-->

## 19. Success Metrics & Measurement

> **Note:** PR Auto-Remediation V2.0 is a greenfield `superclaude remediate` CLI group (the
> `cli/remediate/` package does not exist today — [CODE-VERIFIED]). The metrics below are
> **targets for the built system**, not current measurements. Security-resistance and
> safety-gate metrics are release-blocking; latency/cost metrics are benchmarked against the
> external bar set by comparable products (PR-Agent "~30s, single LLM call"; Copilot cloud
> agent criticized for 90s+ cold-start stop-go UX).

### 19.1 Product Metrics

| Metric | Definition | Target | Measurement Frequency |
|--------|------------|--------|----------------------|
| Authorization-gate correctness | % of triggers where the **replier's** live collaborator permission is evaluated and a read-only/non-collaborator replier is ack-rejected with zero action (AC-1) | 100% | Per-trigger (audit log) |
| Propose-only default adherence | % of mention triggers with no autonomy flag that resolve to `propose` (safest level) | 100% | Per-trigger |
| Intent-respected rate | % of triggers where the bot does **not** act when the comment intent is non-actionable (directly answers Copilot's #1 documented complaint: unconditional child-PR creation even when the comment says "don't") | ≥ baseline (no false action) | Weekly |
| Time-to-first-response | Dispatcher poll-to-acknowledgement latency for a new mention (poll floor is ≥30s — `MIN_POLL_INTERVAL=30` [CODE-VERIFIED in `pr_submit/fsm.py`]) | ack within 1 poll cycle (≤30–60s) | Per-trigger |
| End-to-end remediation latency | Mention → proposed diff / sandbox-branch commit posted (benchmark bar: PR-Agent ~30s; Copilot cloud agent criticized at 90s+) | Set explicit target; large-diff path treated as first-class (compression/chunking) | Per-run |
| Round/loop convergence | % of PRs that terminate within the per-PR push budget (default 2, hard cap 5 — `DEFAULT_MAX_ROUNDS=2`/`HARD_CAP_MAX_ROUNDS=5` [CODE-VERIFIED]) without a runaway loop | 100% (budget never exceeded) | Per-PR |
| Provenance completeness | % of bot-authored replies/commits carrying clear AI provenance + triggering-SHA correlation | 100% | Per-action |

### 19.2 Business Metrics

| Metric | Definition | Target | Measurement Frequency |
|--------|------------|--------|----------------------|
| On-prem differentiation coverage | The bot operates fully headless/on-prem (systemd Dispatcher + `claude -p` Runner), sidestepping the `pull_request_target` secret-injection exposure that underlies most 2026 GitHub-Actions agent CVEs — a capability cloud-only incumbents (Copilot Enterprise "cloud-dependent"; Cursor 3/10 self-host) cannot match | On-prem operation with no third-party Action in the trigger path | Per-release |
| Trust-aligned posture | Default behavior is propose-only + human-approves + agent-cannot-self-merge — the market-validated safe default (Copilot draft-PR; Continue "Level 2 Continuous AI"; Anthropic 2026 "collaborative, not delegated"). Auto-publish bots get muted within months (trust data: ~3–33% trust AI output) | propose-only default; auto-apply opt-in only | Per-release |
| Audit/provenance availability | Trigger ledger + authorization-gate decisions + run logs are queryable, immutable audit artifacts (NIST AI RMF / ISO 42001 reference these controls; "governance-by-design" is the dominant 2026 enterprise narrative) | Immutable per-trigger audit record retained | Continuous |

### 19.3 Technical Metrics

| Metric | Definition | Target | Alerting Threshold |
|--------|------------|--------|--------------------|
| Runner secret-isolation (AC-7) | `/proc/<pid>/environ` of the Runner contains **no** `GH_TOKEN`, no push credential, no `ANTHROPIC_*` token value (INV-001/SC-7). Note: `ClaudeProcess.build_env()` is additive-only `os.environ.copy()` [CODE-VERIFIED] — this target requires an allowlist/replace env path, not the existing `env_vars` param | 0 secrets present | Any secret present → release-block |
| Prompt-injection resistance (AC-3) | Adversarial opComment corpus (hidden `-- Additional instruction --` blocks, `gh ... $TOKEN` exfil attempts, fake "authorized/urgent" framing) cannot cause secret exfiltration or unauthorized push; opComment is delivered as JSON envelope DATA via stdin, **never** interpolated as `/sc:troubleshoot "${opComment}"` (SC-2) | 100% containment on the suite | Any escape → release-block |
| Correct-thread resolution (INV-010) | Reply + GraphQL `resolveReviewThread` always targets the correct thread (matched on `databaseId`); never resolves the wrong thread. No committed Python precedent (a reference bash flow landed in the untracked parallel V1 `sc-pr-submit-protocol` skill); real shape locked by the §21.3 probe gate | 100% correct | Any mismatch → halt H4 |
| At-most-once trigger claiming | Idempotency: each `(trigger_comment_id, parsed_flag_hash)` is claimed exactly once via the two-phase ledger; intent-without-outcome ⇒ RESUME (re-verify), never silent re-execute | 100% exactly-once | Duplicate execution → alert |
| Counter durability (SC-5/SC-6/INV-002) | Round/push counter is disk-authoritative and survives daemon restarts (ledger is SoT; counter derived on startup). Atomic writes via temp + `os.replace` (idiom from `swarm/state.py` / `cache.py` [CODE-VERIFIED] — not the mis-cited `swarm/commands.py:2269` in-memory watch cap) | Survives restart with no loss/double-count | Counter reset on restart → alert |
| Fork-only `--repo` injection (SC-4) | Every `gh` invocation routes through the H5 wrapper that unconditionally injects `--repo IronbellyOrg/IronClaude`; no code path can construct a `gh` argv lacking it (first **code-level** enforcement of C5 — today prose-only in CLAUDE.md) | 0 un-pinned `gh` calls | Any raw `gh` outside `gh.py` → CI fail |
| Egress containment (INV-015) | Runner sandbox enforces deny-by-default network; allowlist limited to the Anthropic proxy (`:4000/cli`), `api.github.com`, and single-repo git | Only allowlisted endpoints reachable | Any other egress → alert |
| `needs_human_decision` HALT integrity | A finding flagged `needs_human_decision` is structurally prevented from shipping as a push (push-gate predicate 3). Risk: no Python code sets this flag today [CODE-VERIFIED] — the populator is agent/skill-driven, so HALT is only as strong as the populator | No `needs_human_decision` item ever auto-pushed | Auto-push of flagged item → release-block |

---

## 20. Risk Analysis

> Probability/Impact scored H/M/L. Risks are grounded in the codebase reuse verification
> (research 01–08) and the external security/market record (web 01–03). The single highest
> cross-cutting risk is prompt injection on untrusted comment text — the dominant agentic-AI
> attack class of 2026, with named CVEs and in-the-wild supply-chain exploits.

### 20.1 Technical Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| **Prompt injection via opComment** — untrusted PR comment steers the agent into exfiltrating secrets or pushing unauthorized code ("Comment and Control", JHU 2026, hijacked Claude Code + Gemini CLI + Copilot from a single crafted comment; "Clinejection" Feb 2026 → live npm supply-chain compromise; 78-study meta-analysis: every coding agent vulnerable, >85% adaptive success) | H | H | Architectural separation = CSA Labs' prescribed "fundamental mitigation": Runner is the credential-less reasoning layer; Dispatcher is the credential-holding execution/policy layer. opComment delivered as JSON envelope DATA via stdin (SC-2), never interpolated. Secret separation removes the "bash tool + secrets" precondition. Adversarial injection test suite as a release-blocking gate (AC-3) | Tighten envelope/tooling; add Dual-LLM quarantine pre-normalization of opComment; revoke push tokens; propose-only blast-radius cap holds |
| **Runner secret leak via additive `build_env()`** — `ClaudeProcess.build_env()` is `os.environ.copy()` + additive `env.update(env_vars)` [CODE-VERIFIED]; passing `env_vars` cannot *subtract* inherited `GH_TOKEN`/push/`ANTHROPIC_*`, so INV-001/SC-7/AC-7 are unsatisfiable as-cited | H | H | Treat R2 as **reuse-with-modification**: add an allowlist/replace env mode to `build_env()` (back-compat, re-tested against sprint/roadmap/swarm callers) OR build the Runner env from a secret-free sandbox parent (§6) — preferred. Gate with the AC-7 `/proc/<pid>/environ` secret-scrape test | If primitive edit regresses shared callers, fall back to sandbox-level minimal environ; never rely on `env_vars` for removal |
| **Wrong-thread resolution (INV-010)** — GraphQL `resolveReviewThread` + `databaseId` pagination has **no committed Python precedent** (a reference bash flow has since landed in the untracked parallel V1 `sc-pr-submit-protocol` skill); threading semantics unproven in Python | M | H | Hard probe-first gate (§21.3): lock `in_reply_to_id`/`databaseId`/Augment-bot-login against a throwaway fixture PR and commit them as config constants **before** any parser/resolve code | If shapes drift, fall back to reply-only (skip resolve); resolve stays behind the lattice `resolve` level |
| **`ClaudeProcess` has no `cwd` parameter** — `Popen` omits `cwd=` [CODE-VERIFIED]; §7's "cwd = sandbox checkout" cannot be met as-is | M | M | Add a `cwd` kwarg to the primitive, OR `os.chdir()` into the PR-head checkout in the one-shot Runner before spawn | Runner-side chdir is safe (disposable process) |
| **`needs_human_decision` has no code populator** — flag is consumed in 5+ FSM sites but **no Python sets it to True** [CODE-VERIFIED]; §8 HALT guarantee rests on an agent/skill self-report | M | H | Build a deterministic populator for the FR-4.4 taxonomy (ambiguous intent / security trade-off / API-contract change / multiple valid fixes), or explicitly document + test the agent-self-report dependency | If self-report unreliable, default ambiguous findings to HALT (fail-safe) |
| **Append-ledger concurrency (flock) net-new in Python** — only bash `flock` precedent exists and it **fails open** (`flock … \|\| true`) [CODE-VERIFIED] | M | M | H1 per-PR push serializer must `fcntl.flock(LOCK_EX)` and **fail-closed** (a failed lock for a push must abort, not fall through) | Serialize all pushes through a single ledger writer; reject on lock contention |
| **Duplication/divergence with in-flight `pr_submit/` core** — V1.0's tested decision core (`fsm`, `severity_router`, `models`, `DetectionContractLocked`) is landing in parallel and is **omitted from the Reuse Map**; rebuilding it under `remediate/` risks two divergent autonomy/severity machines (SoT violation) | M | M | Reconcile in design/TDD: `import superclaude.pr_submit` for the pure decision core, build only the I/O+host layer ("reuse the brain, replace the hands"). Coordinate so V2 host work doesn't race the V1 core landing | If forced to fork, pin a shared rubric/test contract to prevent severity drift |
| **Mis-cited reuse anchors mislead the build** — `swarm/commands.py:2269` is an in-memory `--watch` cap, not a disk-authoritative counter [CODE-CONTRADICTED]; `~/.aienv` is 644 not chmod-600 [CODE-CONTRADICTED] | M | M | Pre-build doc fix: repoint counter→`swarm/state.py`/`pr_submit.should_halt_rounds`, atomic-write→`os.replace`; drop `.aienv` as the chmod-600 exemplar | Treat citations as advisory until re-verified at build time |
| **ETag/304 rate-limit polling net-new** — no `If-None-Match`/`ETag`/`X-RateLimit` precedent in repo [CODE-VERIFIED 0 hits] | M | M | Build conditional-request ingest (D3) with `Retry-After`/`X-RateLimit-Remaining` backoff; poll floor ≥30s | Exponential backoff + jitter; degrade to longer poll interval under rate-limit pressure |

### 20.2 Business Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| **Incumbent dominance (GitHub Copilot Coding Agent)** — GA since Sep 2025; closed-loop review→fix→PR since Mar 2026; the dominant mention→PR-fix workflow | H | M | Differentiate on the open intersection no incumbent occupies: **on-prem × mention-triggered remediation** (Copilot/Amazon Q/Cursor are cloud-only / not self-hostable). Target regulated segments (defense, finance, healthcare, telecom, gov) structurally locked out of cloud runners | Lean into compliance signposting (SOC2/air-gap/zero-retention) as roadmap items |
| **Trust gap suppresses adoption** — 84% adoption vs ~3–33% trust; auto-publishing bots get muted within months; ~95% of GenAI tools "not production-ready" | M | M | Conservative propose-only default + authorization gate + provenance/audit ledger sells *safety and control*; workflow integration (systemd + ledger + existing `superclaude` CLI) is the differentiator, not raw model capability | Keep auto-apply opt-in, per-repo, behind the same authorization layer — never default |
| **Over-action erodes trust** — the market leader's #1 complaint is unconditional triggering / ignored intent | M | M | Live authorization gate + intent evaluation + propose-only is the "middle ground / confirmation step" users explicitly ask for | Add explicit ack-without-action mode for non-actionable comments |

### 20.3 Operational Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| **Sandbox runtime greenfield (OD-1)** — no container/microVM/Firecracker execution harness in repo [CODE-VERIFIED]; external consensus says shared-kernel containers are insufficient for untrusted-code execution (Firecracker/gVisor/Kata/libkrun or Landlock+seccomp recommended) | H | H | Resolve OD-1 early — it gates R4/S2/§15. Evaluate microVM (microsandbox/brood-box) or kernel-LSM (cplt-style `gh`/`git` command guards) as build-vs-buy references; `eval/isolation.py` scratch-root is partial prior art for filesystem confinement only | Start with strongest available isolation tier; propose-only caps blast radius while isolation hardens |
| **systemd/deploy fully greenfield (S2)** — no `deploy/` dir, no `.service`/`WatchdogSec`/`EnvironmentFile` in repo [CODE-VERIFIED]; CLI surfaces are all invoke-and-exit, no long-lived daemon precedent | M | M | Spike the systemd `WatchdogSec`/`sd_notify` integration in Python; chmod-600 `EnvironmentFile` secret-sourcing; external log/ledger forwarding before Runner teardown (ephemerality is "not a complete control" per GitHub's own guidance) | Run Dispatcher under a supervised `Restart=always` unit; forward logs off-host |
| **Probe-first unknowns block the build** — `in_reply_to_id`/`databaseId`/Augment-bot-login shapes are the #1 build-blocking unknown; no code can substitute for a live probe | H | M | Make the throwaway-fixture-PR probe a **hard prerequisite** gate (§21.3) before parser/resolve/authz code; commit captured shapes as fixtures/constants | If probe reveals unstable shapes, narrow scope to reply-only until stabilized |
| **Wrong-repo push (C5) in a headless daemon** — fork-only `--repo` is prose-only today (CLAUDE.md); the daemon is the first autonomous Python `gh` caller; a single un-pinned call re-introduces the upstream-PR hazard | M | H | H5 single-chokepoint `gh_call()` injecting `--repo IronbellyOrg/IronClaude`; unit test asserting no argv omits it; CI grep-guard forbidding raw `subprocess([...,"gh",...])` outside `gh.py`. Build+test H5 first (§21.3) | Disable push autonomy until H5 enforcement test passes |
| **Parallel sessions share git index/HEAD** — concurrent host-side git mutations can corrupt staged state | M | M | Per-PR `flock` (fail-closed) serializes tree mutations; host-side push from an isolated checkout; SHA-correlated round counting | Reject concurrent triggers on the same PR; queue them |
| **`remediation/` stale empty placeholder confused for the home** — top-level `remediation/` exists but is empty [CODE-VERIFIED]; the feature home is `cli/remediate/` | L | L | State explicitly that the feature lives under `src/superclaude/cli/remediate/`; recommend deleting/ignoring the stale `remediation/` dir | Document the canonical path in the TDD |

---

### 21.3 Implementation Phasing

> Phasing follows the spec's §19 build sequencing: front-load the highest-risk net-new
> surfaces behind a hard probe-first gate, build the credential/enforcement chokepoints in
> isolation before any autonomous `gh` I/O, then layer the Dispatcher ingest/authz, the
> sandboxed Runner, and finally the write actions (push/reply/resolve) gated by the autonomy
> lattice. The decision core is **reused, not rebuilt** (`import superclaude.pr_submit`).

| Phase | Components / Features | Rationale |
|-------|----------------------|-----------|
| **Phase 0 — Probe & Reconcile (hard gate)** | Throwaway-fixture-PR probe to lock `in_reply_to_id` / `databaseId` / Augment-bot-login as committed config constants; reconcile against in-flight `pr_submit/` decision core (decide import-and-extend vs fork); fix mis-cited reuse anchors (swarm `:2269`, `.aienv` 644, `os.replace`); resolve OD-1 (sandbox tech) and OD-2 (push-token mechanism) | The GitHub threading/resolve/authz shapes are the #1 build-blocking unknown — no code can substitute for a live probe. OD-1 gates the largest greenfield surface (R4/S2). Reconciliation prevents a duplicate autonomy/severity machine (SoT) |
| **Phase 1 — Credential & Enforcement Chokepoints** | D1 CLI-group registration in `main.py` (deferred-import + `# noqa: E402,I001`); H5 `gh_call()` fork-only `--repo` injector + injection test + CI grep-guard; H1 two-phase ledger (atomic `os.replace` + fail-closed `flock`, intent/outcome RESUME); the `build_env()` allowlist/secret-free-environ seam + AC-7 secret-scrape test | H5 is the first code-level enforcement of C5 (today prose-only) and must exist before any autonomous `gh` call. The env-allowlist seam is the load-bearing secret-isolation fix. Build and unit-test these in isolation |
| **Phase 2 — Dispatcher Ingest, Grammar & Authz** | D3 ETag/304 conditional polling (≥30s floor, rate-limit backoff); D4 mention grammar (whitelist: `propose\|patch\|fix\|push\|resolve`, `--depth`, `--scope`, `--rounds`); D6 parent-comment (`opComment`) resolution; D5 live collaborator-permission authz gate on the **replier** (reject-by-default; read-only replier → ack-reject, zero action) | These are the trust-boundary surfaces. Authz keys on the replier; the parent author supplies only data. All net-new GitHub I/O, dependent on Phase 0's locked shapes |
| **Phase 3 — Sandboxed Runner & Decision Core** | R4 ephemeral sandbox (PR-head checkout, deny-by-default egress allowlist, no host mounts); R2 Runner executor wrapping `ClaudeProcess` (propose-level `max_turns`, stdin envelope, `cwd`); R3 CONTROL/DATA envelope (opComment as JSON DATA, never interpolated); H2 autonomy gate + S1 severity routing reused from `pr_submit` (5-predicate push conjunction, `needs_human_decision` HALT, severity→depth) | The Runner is the credential-less reasoning layer (CSA "fundamental mitigation"). Severity routing and autonomy gating are reuse-by-import. Propose-only is the default and the first end-to-end happy path |
| **Phase 4 — Write Actions (lattice-gated)** | H3 host-side push with short-lived token (per-PR push budget default 2 / cap 5, SHA-correlated rounds); H4 reply-to-thread (`/replies`) + GraphQL `resolveReviewThread`; S2 systemd deploy (unit, `WatchdogSec`, chmod-600 `EnvironmentFile`, log forwarding) | Write authority is layered last and only reachable by explicit flag AND write-permission AND passing validation (lattice-min). Resolve sits behind the highest `resolve` level. Push budget and loop-safety enforced by the Phase-1 ledger |

> **Phase gating rule:** No phase may begin until the prior phase's release-blocking gates pass.
> Phase 0's probe is an absolute prerequisite for Phases 2–4; H5 (Phase 1) must pass its
> injection test before any Phase 2–4 code constructs a `gh` argv.

---

### 21.4 Release Criteria & Definition of Done

#### 21.4.1 Phase/Release Criteria

**MVP (propose-only) Release Criteria:**

| Category | Criterion | Validation Method | Status |
|----------|-----------|-------------------|--------|
| **Functionality** | Authorized replier `@bot` mention → opComment resolved → sandboxed Runner produces a proposed diff and posts a thread reply; read-only/non-collaborator replier is ack-rejected with zero action (AC-1) | Live fixture-PR e2e + authz unit tests | ⬜ |
| **Functionality** | Default with no flag resolves to `propose`; reaching `push`/`resolve` requires explicit flag AND write-permission AND passing validation (lattice-min) | Autonomy-gate unit tests (reuse `pr_submit` `evaluate_push_decision`) | ⬜ |
| **Security** | Runner `/proc/<pid>/environ` contains no `GH_TOKEN`/push token/`ANTHROPIC_*` value (INV-001/SC-7/AC-7) | Secret-scrape regression test | ⬜ |
| **Security** | Adversarial injection corpus (hidden instruction blocks, `$TOKEN` exfil, fake-authorized framing) achieves 0 escapes; opComment delivered as stdin JSON DATA, never interpolated (SC-2/AC-3) | Release-blocking red-team suite | ⬜ |
| **Security** | No `gh` argv can be constructed without `--repo IronbellyOrg/IronClaude` (SC-4); no raw `gh` subprocess outside `gh.py` | H5 injection unit test + CI grep-guard | ⬜ |
| **Safety** | Per-PR push budget (default 2, cap 5) never exceeded; counter is disk-authoritative and survives daemon restart (SC-5/SC-6/INV-002); `needs_human_decision` item never auto-pushed | Loop-guard + ledger restart tests | ⬜ |
| **Correctness** | Reply/resolve always targets the correct thread by `databaseId` (INV-010); each `(trigger_comment_id, flag_hash)` claimed at-most-once; intent-without-outcome ⇒ RESUME | Threading + idempotency tests against fixture PR | ⬜ |
| **Quality** | All reused `pr_submit` tests still pass; new `tests/cli/remediate/` registration + unit suite green; `make lint`, `ruff format --check`, `make verify-sync` clean | CI | ⬜ |
| **Operations** | Dispatcher runs as a supervised systemd unit; deny-by-default egress allowlist enforced (proxy `:4000/cli` + `api.github.com` + single-repo git, INV-015); run logs/ledger forwarded off-host before Runner teardown | Deploy smoke test + egress probe | ⬜ |
| **Documentation** | `cli/remediate/` documented as the SoT home; `--repo`/secret-separation/propose-only invariants and the mention grammar documented | Doc⇆CLI parity review | ⬜ |

#### 21.4.2 Definition of Done (Feature/Component Level)

A `remediate` component is considered "Done" when:

- [ ] All acceptance criteria met (AC-1, AC-3, AC-4, AC-7 as applicable)
- [ ] Unit tests written and passing; reused `pr_submit` contract tests unbroken
- [ ] Integration/e2e validated against a throwaway fixture PR (not just happy-path units)
- [ ] Security review: injection containment + secret isolation gates pass
- [ ] `gh` calls route only through H5 (`--repo` injection verified by test + grep-guard)
- [ ] Loop-safety: push budget + counter durability + `needs_human_decision` HALT verified
- [ ] `make lint` + `ruff format --check src/ tests/` + `make verify-sync` clean
- [ ] Code reviewed and approved; documentation updated (SoT path, invariants)
- [ ] No raw `gh`/secret leakage path introduced; product-owner acceptance

#### 21.4.3 Rollback & Contingency Plans

| Scenario | Detection Method | Rollback Procedure | Decision Maker |
|----------|------------------|-------------------|----------------|
| Injection escape or secret leak detected | Red-team suite / AC-7 scrape / audit log | Disable Runner dispatch (Dispatcher stops claiming triggers); revoke/rotate push tokens; revert to comment-only | Security owner |
| Wrong-thread resolution / wrong-repo push | INV-010 mismatch alert / `--repo` audit | Disable `resolve` + `push` levels (lattice cap to `propose`/`patch`); fall back to reply-only | Eng lead |
| Runaway remediation loop | Push budget exceeded / counter anomaly | Halt PR via ledger; cap rounds; require human re-arm | Eng lead |
| Rate-limit / API-shape drift | `X-RateLimit`/`Retry-After` / parse failures | Back off polling; freeze parser; re-run Phase-0 probe to relock shapes | On-call operator |
| Sandbox isolation failure | Egress-allowlist violation alert | Stop Runner; quarantine workspace; harden isolation tier before resume | Security owner |

---

### 21.5 Timeline & Milestones

> **Note:** The research inputs do not specify calendar dates, durations, or person-week
> estimates; this PRD is dated 2026-06-11. Milestones below are therefore **relative and
> dependency-ordered** (from the §19 build sequencing) with calendar dates marked TBD —
> set at kickoff. The one external anchor is the **EU AI Act high-risk compliance deadline
> (August 2026)**, a buyer-facing consideration for the on-prem/governed positioning.

#### 21.5.1 High-Level Timeline

```
[Phase 0: Probe & Reconcile] ─────────── [TBD] - [TBD]   (HARD GATE)
    ├── M0.1: GitHub shapes locked (in_reply_to_id / databaseId / bot-login)   [TBD]
    ├── M0.2: pr_submit reuse decision (import-and-extend) + citation fixes     [TBD]
    └── M0.3: OD-1 sandbox tech + OD-2 push-token mechanism resolved            [TBD]

[Phase 1: Credential & Enforcement Chokepoints] ── [TBD] - [TBD]
    ├── M1.1: D1 CLI group registered (superclaude remediate live)             [TBD]
    ├── M1.2: H5 --repo injector + injection test + CI grep-guard green        [TBD]
    └── M1.3: H1 ledger + build_env allowlist seam + AC-7 scrape test green    [TBD]

[Phase 2: Dispatcher Ingest, Grammar & Authz] ──── [TBD] - [TBD]
    ├── M2.1: D3 ETag/304 polling (≥30s floor) + backoff                       [TBD]
    ├── M2.2: D4 mention grammar + D6 parent (opComment) resolution            [TBD]
    └── M2.3: D5 live replier authz gate (AC-1: read-only → ack-reject)        [TBD]

[Phase 3: Sandboxed Runner & Decision Core] ────── [TBD] - [TBD]
    ├── M3.1: R4 sandbox (egress allowlist) + R2 executor + R3 envelope        [TBD]
    ├── M3.2: H2 autonomy gate + S1 severity routing (reused from pr_submit)   [TBD]
    └── M3.3: MVP propose-only e2e green (injection suite + secret scrape pass) [TBD]

[Phase 4: Write Actions (lattice-gated)] ───────── [TBD] - [TBD]
    ├── M4.1: H3 host-side push (budget 2/cap 5, SHA-correlated)               [TBD]
    ├── M4.2: H4 reply + GraphQL resolveReviewThread (INV-010 correct)         [TBD]
    └── M4.3: S2 systemd deploy (WatchdogSec, chmod-600 EnvironmentFile)       [TBD]
```

#### 21.5.2 Detailed Phase Breakdown

##### Phase 0: Probe & Reconcile (HARD GATE)

**Focus:** De-risk the #1 build-blocking unknowns before any parser/resolve/authz code.

**Deliverables:**

- [ ] Throwaway fixture-PR probe → `in_reply_to_id`/`databaseId`/Augment-bot-login committed as fixtures/constants
- [ ] Reuse decision: `import superclaude.pr_submit` (brain) vs fork; coordination with the in-flight V1 core landing
- [ ] Citation fixes (swarm `:2269`→`state.py`/`pr_submit.should_halt_rounds`; `os.replace`; drop `.aienv` chmod exemplar)
- [ ] OD-1 (sandbox tech) and OD-2 (push-token mechanism) resolved

**Success Criteria:** GitHub I/O shapes locked from real bytes; no parallel autonomy/severity machine; sandbox tech chosen.

**Target Completion:** TBD

---

##### Phase 1: Credential & Enforcement Chokepoints

**Focus:** Build the secret-isolation and `--repo` enforcement primitives that everything downstream depends on.

**Deliverables:**

- [ ] D1 group registered in `main.py` (`# noqa: E402,I001`)
- [ ] H5 `gh_call()` unconditional `--repo` injector; test asserting no argv omits it; CI grep-guard
- [ ] H1 two-phase ledger (atomic `os.replace`, fail-closed `flock`, intent/outcome RESUME)
- [ ] `build_env()` allowlist/secret-free-environ seam + AC-7 secret-scrape test

**Success Criteria:** `superclaude remediate` resolves; AC-7 passes; no un-pinned `gh` path exists.

**Target Completion:** TBD

---

##### Phase 2: Dispatcher Ingest, Grammar & Authz

**Focus:** The trust-boundary surfaces — detect mentions, resolve the parent, gate the replier.

**Deliverables:**

- [ ] D3 ETag/304 conditional polling (≥30s floor, rate-limit backoff)
- [ ] D4 mention grammar whitelist + D6 `opComment` parent resolution
- [ ] D5 live collaborator-permission authz gate on the replier (AC-1)

**Success Criteria:** Authorized replier triggers a claim; read-only replier ack-rejected with zero action.

**Target Completion:** TBD

---

##### Phase 3: Sandboxed Runner & Decision Core (MVP)

**Focus:** The credential-less reasoning layer and the reused decision core — first end-to-end propose-only path.

**Deliverables:**

- [ ] R4 ephemeral sandbox + R2 `ClaudeProcess` executor + R3 CONTROL/DATA envelope
- [ ] H2 autonomy gate + S1 severity routing (reuse-by-import from `pr_submit`)
- [ ] MVP propose-only e2e: mention → proposed diff → thread reply

**Success Criteria:** Injection suite 0 escapes; secret-scrape clean; propose-only happy path green.

**Target Completion:** TBD

---

##### Phase 4: Write Actions (lattice-gated)

**Focus:** Layer push/reply/resolve last, each reachable only by explicit flag + write-permission + validation.

**Deliverables:**

- [ ] H3 host-side push (budget 2/cap 5, SHA-correlated rounds)
- [ ] H4 reply-to-thread + GraphQL `resolveReviewThread` (INV-010)
- [ ] S2 systemd deploy (unit, `WatchdogSec`, chmod-600 `EnvironmentFile`, log forwarding)

**Success Criteria:** Lattice-min holds (no path to push without all gates); resolve targets correct thread; daemon supervised and auditable.

**Target Completion:** TBD

---
