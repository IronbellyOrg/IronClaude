<!--
SYNTHESIS FRAGMENT — Business & Market sections for the PR Auto-Remediation V2.0 PRD.
Produced from the research/ corpus (agents 01–08 + web-01..03) against template
.claude/templates/workflow/05_prd_template.md. Sections: 5 Business Context, 6 JTBD,
7 User Personas, 8 Value Proposition Canvas.

Evidence convention:
- [CODE-VERIFIED] = confirmed against current source by a research agent.
- All market/competitive facts carry their source per the web-research reliability ledgers.
- The product (`superclaude remediate`, src/superclaude/cli/remediate/) is GREENFIELD —
  not yet built [CODE-VERIFIED: agents 1/4/7/8, `ls` returns "No such file or directory"].
  Capabilities below are DESIGNED/INTENDED, not current, except where marked [CODE-VERIFIED].
-->

## 5. Business Context

> **Scope note:** PR Auto-Remediation V2.0 is a **feature/component** of the SuperClaude /
> IronClaude framework, delivered as a self-hosted `superclaude remediate` CLI group + systemd
> service — not a commercially-sold SaaS product. There is no standalone pricing or ARR model.
> The market sizing below is **category context** (it sizes the AI-code-remediation space the
> feature competes in), not a revenue forecast for this feature. All KPIs are owned by
> **Section 19 (Success Metrics & Measurement)** — this section forward-references them and does
> not duplicate targets.

### 5.1 Why This Feature Matters to the Business

**The strategic bet:** the SuperClaude framework already automates the *review* side of the PR
loop (the `sc:auggie-review` protocol posts severity-graded findings via `gh`). PR
Auto-Remediation V2.0 closes the loop — turning a flagged review comment into a proposed (or,
at higher authority, applied) fix — **without requiring a live Claude Code session to stay open**.
This is the explicit reason V2.0 exists: V1.0 hosted the monitor inside an in-session Monitor
tool that "dies on session close" (V1 Red-Team R3); V2.0 re-hosts it as a headless systemd
daemon so remediation survives session and machine restarts [CODE-VERIFIED: agents 1, 3, 5].

**Three business-level justifications, each grounded in the 2026 market record:**

| Justification | Evidence | Source |
|---------------|----------|--------|
| **Neutralizes the dominant agentic-AI attack class of 2026.** Running an LLM agent with file-write + git-push authority on untrusted PR comment text is *exactly* the precondition that produced real CVEs and in-the-wild exploits. The split Dispatcher/Runner design is the architecture an independent research body prescribes as "the fundamental mitigation." | "Comment and Control" (JHU, Apr 2026) hijacked Claude Code, Gemini CLI **and** GitHub Copilot Agent via PR/issue comments into leaking `ANTHROPIC_API_KEY`/`GITHUB_TOKEN`; "Clinejection" (Feb 2026) chained an issue-title injection into a live npm supply-chain compromise. CSA Labs: *"separate the reasoning layer … from the credential-holding execution layer."* | web-01 §3.1–3.2, web-02 §2, web-03 §2.2 |
| **Answers the market leader's #1 documented complaint.** GitHub Copilot Coding Agent (GA Sep 2025) unconditionally opens a child PR even when the comment says "don't" — "intent ignored, no middle ground." A conservative propose-only default + live authorization gate is the confirmation step users explicitly ask for. | GitHub Community Discussion #190027 | web-01 §1.2 |
| **Occupies open whitespace: on-prem × mention-triggered remediation.** Cloud incumbents (Copilot, Amazon Q, Cursor) cannot be self-hosted; on-prem leaders (Tabnine, Windsurf, Qodo) ship inline/IDE assist, not autonomous PR-remediation bots. No incumbent occupies both axes. | Copilot Enterprise "cloud-dependent"; Cursor 3/10 self-host; Mordor: self-hosted ≈29% of market, explicitly under-served | web-01 §2.2, §4.4; web-03 §4.2 |

**Cost drivers (feature-specific, for platform-level usage accounting):**

- **LLM token consumption** — each trigger spawns a `claude -p` Runner (`ClaudeProcess`, default
  `max_turns=100`; build sets `propose≈30 / fix≈60`) [CODE-VERIFIED: agents 7, 8].
- **Sandbox compute** — one ephemeral, disposable PR-head checkout + isolated runtime per trigger
  (greenfield; OD-1 container-vs-microVM decision is unresolved) [CODE-VERIFIED greenfield: agents 4, 5, 8].
- **Bounded by design** — a per-PR push budget (default 2, hard cap 5) and a poll floor (≥30s)
  cap runaway spend [CODE-VERIFIED: `pr_submit/fsm.py` `DEFAULT_MAX_ROUNDS=2`, `HARD_CAP_MAX_ROUNDS=5`, `MIN_POLL_INTERVAL=30`, agents 4, 6].

### 5.2 Market Opportunity (Category Context)

> ⚠️ **Reliability caveat (carried from web-01 §4.1):** AI-coding market figures diverge **100×+**
> by analyst scope. Treat **trend direction and the named use case** as the reliable signal, never
> a single headline dollar figure.

| Market | Size | Notes |
|--------|------|-------|
| **Total Addressable Market (TAM)** — agentic / AI-code tooling | Agentic AI frameworks: **$2.99B (2025) → $19.32B (2031), 36.3% CAGR** (Mordor); AI code tools: **$4.3B (2023) → $12.6B (2028), 24% CAGR** (MarketsandMarkets); broader agentic-dev: **$10.4B (2025), ~39.5% CAGR** (marketintelo) | Fast-growing; estimates vary by scope. 84% developer adoption; PR-stage AI is operational infrastructure, not experiment (web-01 §4, web-03 §4.1) |
| **Serviceable Addressable Market (SAM)** — self-hosted / governed agentic coding | **≈29% of the market is self-hosted/on-prem** (Mordor: cloud-hosted held 71.3% in 2025) — the explicitly under-served, security-driven segment | Regulated sectors named: defense, government, finance, healthcare, telecom — structurally locked out of cloud-only incumbents (web-01 §2.2, web-03 §4.2) |
| **Serviceable Obtainable Market (SOM)** — mention-triggered PR auto-remediation, on-prem | **No dollar figure — internal/framework-scoped.** Initial target = the `IronbellyOrg/IronClaude` fork + SuperClaude self-hosted users needing autonomous remediation | "Autonomous pull request resolution + security vulnerability remediation" is an **analyst-named emerging high-value use case**, not yet commoditized (web-01 §4.2) |

### 5.3 Business Objectives

> This feature has **no commercial revenue model** (internal/self-hosted capability). The
> template's ARR-style objectives are reframed as strategic/capability objectives.

1. **Close the review→remediation loop** safely: deliver a headless bot that converts an
   authorized `@bot` reply into a proposed fix, surviving session/machine restarts (the core V2.0
   bet over V1.0's session-bound host) [CODE-VERIFIED lineage: agents 1, 3].
2. **Establish governance-by-construction** as the differentiator: secret separation, live
   per-trigger authorization, immutable trigger ledger, and propose-only default — the controls
   NIST AI RMF / ISO 42001 / OWASP now reference as table-stakes (web-02 §2.4, web-03 §4.3).
3. **Own the on-prem × mention-triggered intersection** — the documented market whitespace
   (web-01 §2.2).
4. **Harden a previously prose-only safety rule into code**: the fork-only
   `--repo IronbellyOrg/IronClaude` invariant (H5) becomes the *first* machine-enforced GitHub
   target guard — today it lives only in CLAUDE.md prose and has previously failed (PR mis-routed
   to upstream) [CODE-VERIFIED: agents 3, 4, 5, 6].

**Capability Milestones (replacing revenue milestones):**

- **Phase 1:** propose-only Runner behind the probe-gated GitHub-I/O surface and the live authz gate.
- **Phase 2:** host-side push (`fix`/`push` autonomy) with short-lived tokens + per-PR push budget.
- **Phase 3:** thread reply + GraphQL resolve (`resolve` autonomy) — the highest-novelty surface.

### 5.4 Key Performance Indicators (KPIs)

> **KPIs are owned by Section 19 (Success Metrics & Measurement).** To avoid drift, this section
> does not restate targets. The category-level success signals the design is measured against:

| Category | Signal | Source / Rationale |
|----------|--------|--------------------|
| **Security** | Adversarial prompt-injection suite passes as a release gate (Runner cannot exfiltrate secrets or push unauthorized code) | CSA recommends injection red-teaming as a standard deployment gate (web-02 §2.4, web-03 §2.2) → see §19 |
| **Trust / adoption** | Propose-only default upheld; authorized-replier-only action; zero unauthorized pushes | 84% adoption vs ~3–33% trust; auto-posting bots get muted within months (web-01 §4.3, web-02 §4) → see §19 |
| **Latency / cost** | Bounded round/budget (default 2, cap 5); poll floor ≥30s; benchmarked against "single LLM call ~30s" (PR-Agent) and Copilot's criticized 90s+ cold start | web-01 §1.3, §5; [CODE-VERIFIED budgets: agents 4, 6] → see §19 |

---

## 6. Jobs To Be Done (JTBD)

> **Framework:** Jobs To Be Done focuses on the underlying motivation and desired outcome, not the
> solution. Format: "When [situation], I want to [motivation], so I can [expected outcome]."

### 6.1 Primary Jobs

**Job 1: Turn a flagged review comment into a fix without opening a coding session**

- **When**: an AI reviewer (Augment/`sc:auggie-review`) or a human leaves a review comment flagging
  an issue on a PR, and I (an authorized collaborator) want it remediated.
- **I want to**: reply to that specific comment with a short directive — e.g. `@bot fix --depth deep`
  — and have a headless agent check out PR-head, run `/sc:troubleshoot` against the comment, and
  propose a diff.
- **So I can**: clear review findings without context-switching into a live IDE/Claude session or
  babysitting a long-running tool.
- **Current alternatives**: manually open an editor and fix it; or run the V1.0 in-session monitor
  (which dies when the session/laptop closes — V1 R3).
- **Pain with alternatives**: the in-session host is fragile (no 24/7 survival); manual fixing is
  the toil the whole framework exists to remove [CODE-VERIFIED lineage: agents 1, 3, 5].

**Job 2: Delegate the fix but stay in control of what lands**

- **When**: I trust an agent to *draft* a fix but not to silently push or merge it.
- **I want to**: keep the bot at **propose-only by default**, and have it reach `push`/`resolve`
  only when I explicitly raise the autonomy flag, I hold write permission, validation passes, and
  the push budget is unspent — a lattice-minimum cap, with `needs_human_decision` items hard-halting.
- **So I can**: get leverage from automation without inheriting its mistakes (the "middle ground"
  the market is asking for).
- **Current alternatives**: GitHub Copilot Coding Agent, which unconditionally opens a child PR
  even when told not to.
- **Pain with alternatives**: over-action erodes trust; auto-posting/auto-acting bots get muted
  within months (84% adoption vs ~3–33% trust) [web-01 §1.2, §4.3; web-02 §4; CODE-VERIFIED gate
  logic: `pr_submit/fsm.py` 5-predicate `evaluate_push_decision`, agents 5, 6].

**Job 3: Run autonomous remediation on untrusted comment text without getting owned**

- **When**: the bot must process attacker-influenceable GitHub text (the parent `opComment`) while
  the system holds push credentials.
- **I want to**: ensure the credential-holding layer (Dispatcher) never ingests the untrusted text
  as instructions, the reasoning layer (Runner) holds no exfiltratable secrets, and the comment is
  delivered as JSON **DATA inside a trusted envelope** — never interpolated as
  `/sc:troubleshoot "${opComment}"`.
- **So I can**: avoid the "Comment and Control" credential-theft class that hit Claude Code, Gemini
  CLI, and Copilot Agent in 2026.
- **Current alternatives**: cloud GitHub-Actions agents using `pull_request_target` (which injects
  secrets into the runner that sees untrusted text).
- **Pain with alternatives**: that exact pattern produced the 2026 CVEs and supply-chain exploits;
  detection/prompting alone is not a defense (>85% adaptive attack success across 78 studies)
  [web-01 §3, web-02 §2, web-03 §2; CODE-VERIFIED envelope requirement: agent 8].

**Job 4: Operate PR auto-remediation where the cloud can't go**

- **When**: I run a regulated, firewalled, or air-gapped shop and cannot send code to GitHub-hosted
  runners.
- **I want to**: deploy the whole bot on-prem as a systemd service against my fork, with a
  deny-by-default egress allowlist and host-side-only credentials.
- **So I can**: get mention-triggered remediation that cloud-only incumbents (Copilot, Amazon Q,
  Cursor) structurally cannot provide.
- **Current alternatives**: on-prem inline/IDE assistants (Tabnine, Windsurf, Qodo).
- **Pain with alternatives**: they assist in the editor; none offer autonomous mention-triggered PR
  remediation — the whitespace V2.0 targets [web-01 §2.2, web-03 §4.2].

### 6.2 Related Jobs

| Job | Frequency | Importance | Satisfaction with Current Solutions |
|-----|-----------|------------|-------------------------------------|
| Operate a 24/7 headless service that survives restarts (operator) | Continuous | Critical | 2/10 — V1.0 in-session host dies on session close (agents 1, 3) |
| Prove who triggered what, with an immutable audit trail | Per trigger | High | 3/10 — governance/audit is the "missing link" for 25% of leaders (web-03 §4.3) |
| Prevent the bot from ever pushing to the wrong (upstream) repo | Per push | Critical | 2/10 — fork-only `--repo` is prose-only today, has already failed once (agents 3–6) |
| Keep remediation cost/latency bounded on large diffs | Per trigger | Medium | 4/10 — PR-Agent sets the ~30s/low-cost bar; Copilot criticized for 90s+ cold start (web-01 §1.3) |

---

## 7. User Personas

### 7.1 Primary Persona: Maya — Authorized Reviewer / Repo Maintainer

| Attribute | Details |
|-----------|---------|
| **Demographics** | Senior engineer / maintainer with **write (or admin) permission** on the `IronbellyOrg/IronClaude` fork; lives in PRs and the terminal; high familiarity with the `superclaude` CLI surface (agent 8 §3) |
| **Goals** | Clear review findings fast; delegate routine fixes to an agent while controlling what lands; never trust the bot blindly |
| **Pain Points** | Context-switching into a coding session to apply a one-line fix; the V1.0 monitor dying on session close; incumbent agents over-acting on intent |
| **Technical Proficiency** | High |
| **Budget Authority** | Influences (sets autonomy level per trigger via the mention grammar) |
| **Success Metrics** | Findings remediated per PR with zero unauthorized pushes; time-to-proposed-fix; trust that propose-only holds |

**Quote:** "I want to reply `@bot fix` on a review comment and get a clean diff to look at — not a child PR I never asked for, and definitely not a push I didn't approve."

**A Day in Their Life:**
Maya is the **sole authority** on a trigger — she replies to an AI/human review comment with a tiny
whitelisted directive (`propose|patch|fix|push|resolve` + `--depth`/`--scope`/`--rounds`); the
parent comment is data, not a command (agent 8 §3). Default with no flag = `propose` (safest). She
reviews the bot's proposed diff and decides what merges — humans always merge (web-01 §5.1).

### 7.2 Secondary Persona: Devraj — Platform / DevOps Operator

| Attribute | Details |
|-----------|---------|
| **Demographics** | DevOps/SRE responsible for standing up and running the headless service on-prem; manages systemd, secrets, and the sandbox runtime |
| **Goals** | A 24/7 service that survives restarts; secrets held host-side only; deny-by-default egress; an immutable audit trail |
| **Pain Points** | No existing daemon/long-lived-service pattern in the CLI to copy; `deploy/` + systemd units are fully greenfield (OD-1 sandbox tech unresolved) [CODE-VERIFIED greenfield: agents 2, 4, 6] |
| **Technical Proficiency** | High |
| **Budget Authority** | Yes (owns deployment, token issuance, sandbox/compute footprint) |
| **Success Metrics** | Uptime / restart survival; zero secret leakage into the Runner env (AC-7); zero pushes to the wrong repo |

**Quote:** "It has to run as a service I can `systemctl restart` and walk away from — and I need proof that `GH_TOKEN` never makes it into the box that reads the untrusted comment."

### 7.3 Tertiary Persona: Sofia — Security / Governance Engineer

| Attribute | Details |
|-----------|---------|
| **Demographics** | AppSec/governance owner accountable for safe adoption of autonomous coding agents; tracks OWASP LLM01, CSA guidance, NIST AI RMF / ISO 42001 |
| **Goals** | Verify the bot cannot be weaponized by a crafted comment; confirm reasoning/execution separation, least-privilege, and tamper-evident audit |
| **Pain Points** | The "Comment and Control" / "Clinejection" attack class; cloud `pull_request_target` secret injection; detection/prompting alone proven insufficient (web-01 §3, web-02 §2) |
| **Technical Proficiency** | High |
| **Budget Authority** | Influences (sign-off / release gate) |
| **Success Metrics** | Adversarial injection suite passes as a release gate; quantified injection-resistance; immutable trigger ledger covers every trigger + exact input + decision |

**Quote:** "Show me the architecture separates the layer that reads the comment from the layer that holds the token — and show me the red-team suite that proves it."

### 7.4 Anti-Personas (Who This Is NOT For)

| Anti-Persona | Why Not Target |
|--------------|----------------|
| Read-only / external (fork) contributors who @-mention the bot | The live authorization gate rejects them by default; the *replier* is the sole authority, a `read`-permission user gets a polite ack-reject, zero action (AC-1, agent 8 §3) |
| Teams wanting fully-autonomous auto-merge / "delegate and forget" | Propose-only is the deliberate default; humans merge — the design explicitly refuses to modify merge state (web-01 §5.1, web-03 §1; severity rubric forbids `--approve`/`--request-changes`, agent 8 §4) |
| Cloud-only teams happy on GitHub-hosted runners | The product's reason to exist is on-prem/air-gapped self-hosting; teams with no self-host requirement are better served by Copilot Coding Agent / `@claude` Action (web-01 §1.1, web-03 §1.1) |

---

## 8. Value Proposition Canvas

> **Framework:** Maps customer pains and gains to product pain relievers and gain creators.
> **Note:** the `superclaude remediate` host is greenfield (not yet built); the value map below
> describes **designed** capabilities. Items grounded in already-built code are marked
> [CODE-VERIFIED].

### 8.1 Customer Profile: Maya (Primary Persona — Authorized Reviewer / Maintainer)

**Customer Jobs:**

1. (Functional) Convert a flagged review comment into a proposed fix without opening a coding session.
2. (Functional) Control the autonomy level per trigger — propose vs. push — and keep humans on the merge.
3. (Social) Adopt agent automation that the team trusts rather than mutes.
4. (Emotional) Delegate routine remediation without fear of an unauthorized push or a leaked secret.

**Pains:**
| Pain | Severity (1-10) | Frequency |
|------|-----------------|-----------|
| Context-switching into an IDE/session to apply small review fixes | 7 | Every review cycle |
| Remediation host dies on session/laptop close (V1.0) | 9 | Every long-running monitor attempt |
| Incumbent agents over-act / ignore intent (unwanted child PRs) | 8 | Per Copilot trigger (web-01 §1.2) |
| Untrusted comment → secret theft / unauthorized push ("Comment and Control") | 10 | Latent on every trigger (web-01 §3, web-02 §2) |
| Bot pushing to the wrong (upstream) repo | 9 | Per push — has happened once (agents 3–6) |

**Gains:**
| Gain | Importance (1-10) | Current Satisfaction |
|------|-------------------|---------------------|
| Mention → headless proposed fix, no session needed | 9 | 2/10 (V1.0 session-bound) |
| Stay in control: propose-only default, lattice-min autonomy, human merges | 10 | 3/10 (incumbents over-act) |
| Provable safety on untrusted input (secret separation, sandbox) | 10 | 2/10 (cloud agents leak) |
| Runs on-prem / air-gapped | 8 | 3/10 (incumbents cloud-only) |

### 8.2 Value Map

**Pain Relievers:**
| Pain | How We Relieve It | Measurement |
|------|-------------------|-------------|
| Session-bound, fragile host | Split **Dispatcher (systemd daemon) + ephemeral Runner**; survives session/machine restart; ledger is SoT, counter derived on startup | Restart-survival test; uptime (see §19) |
| Over-action / ignored intent | **Propose-only default**; effective autonomy = lattice-min over {flag, authz, validation, budget}; `needs_human_decision` hard-halt [CODE-VERIFIED 5-predicate gate: `pr_submit/fsm.py`, agents 5, 6] | Zero unauthorized pushes; authorized-replier-only action (AC-1) |
| Untrusted-comment secret theft | Reasoning/execution **split**: Runner holds no push/Anthropic secrets, opComment delivered as JSON **DATA via stdin envelope**, never interpolated; Dispatcher (credential layer) never ingests untrusted text | Adversarial injection suite as release gate; AC-7 `/proc/<pid>/environ` scrape = 0 secrets |
| Wrong-repo push | **H5 `gh` wrapper** unconditionally injects `--repo IronbellyOrg/IronClaude` — first *code* enforcement of a today-prose-only rule [CODE-VERIFIED no Python `gh` caller exists: agents 3–6] | Unit test: no argv can omit `--repo`; verified target owner |
| Cloud lock-out | **On-prem** systemd deployment, deny-by-default egress allowlist, host-side-only short-lived tokens | Runs air-gapped; sidesteps `pull_request_target` exposure |

**Gain Creators:**
| Gain | How We Create It | Measurement |
|------|------------------|-------------|
| Frictionless mention→fix | `@bot <level> --depth/--scope/--rounds` grammar → sandboxed Runner runs `/sc:troubleshoot` on PR-head, emits diff (propose) or sandbox-branch commit (fix) [CODE-VERIFIED executor reuse: `ClaudeProcess`, `roadmap/remediate_executor.py`, agents 1, 5, 8] | Time-to-proposed-fix; findings remediated per PR |
| Control + trust | Conservative default + severity→action routing (reuse rubric/`severity_router`) [CODE-VERIFIED: agents 2, 3] + immutable trigger ledger for provenance | Propose-only adherence; audit completeness |
| Governance-by-construction | Live per-trigger collaborator-permission authz gate (reject-by-default); two-phase intent/outcome ledger; bounded push budget (default 2, cap 5) | Authz coverage; ledger replay correctness |
| On-prem assurance | Whole bot self-hosted; no third-party GitHub Action in the trust path | Compliance posture (OWASP/CSA/NIST-aligned) |

### 8.3 Fit Assessment

| Fit Type | Score (1-10) | Evidence |
|----------|--------------|----------|
| **Problem-Solution Fit** | 9 | The exact threat (untrusted-comment + tool-bearing agent) produced named 2026 CVEs; CSA Labs prescribes reasoning/execution separation as "the fundamental mitigation" — a 1:1 description of the Runner/Dispatcher split (web-01 §3.2, web-02 §2, web-03 §2.2). The decision core is ~40–80% already built and tested in `pr_submit/` [CODE-VERIFIED: agents 3–6] |
| **Product-Market Fit** | 7 | Mention-trigger UX is idiomatic and validated by the platform owner (Copilot, `@claude`); propose-only is the universal safe default; on-prem × mention-triggered remediation is documented open whitespace. Tempered by: greenfield host (sandbox/systemd/GraphQL net-new, agents 4–8) and narrow initial audience (fork-scoped) |

---
