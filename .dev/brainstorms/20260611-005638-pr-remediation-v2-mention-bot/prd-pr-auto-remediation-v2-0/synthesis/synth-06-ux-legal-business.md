<!--
SYNTHESIS NOTE (read before using these sections):
- Product: PR Auto-Remediation V2.0 — the `superclaude remediate` mention-triggered headless bot.
- Document type: FEATURE/COMPONENT PRD (a capability of the SuperClaude platform on the
  IronbellyOrg/IronClaude fork), NOT a standalone commercial product.
- Greenfield status: `src/superclaude/cli/remediate/` does NOT exist [CODE-VERIFIED absent,
  research 04/07/08]. Therefore every product behavior below is PROPOSED design, not current
  capability. Only reused primitives are marked [CODE-VERIFIED]: `ClaudeProcess`
  (cli/pipeline/process.py:72), the severity rubric (sc-auggie-review-protocol/refs/severity-rubric.md),
  and the `pr_submit/` decision core (fsm/severity_router/models).
- Per template SCOPE NOTEs: §17 keeps feature-specific data-handling + the platform/regulatory
  context the research supplies; §18 is largely N/A (internal tool, no independent pricing/GTM) —
  market data is included only as competitive-positioning / strategic-justification context.
-->

## 16. User Experience Requirements

> **Scope note:** This is a feature PRD. The product's entire "interface" is a four-token
> `@`-mention comment grammar plus an operator-facing systemd service — there is **no GUI, no web
> surface, and no new end-user slash command** [research 08 §3]. Accessibility (16.3) and
> localization (16.4) are therefore N/A for this feature and defer to the Platform PRD. The
> substance of this feature's UX lives in the core user flows (16.2).

### 16.1 Onboarding & Interaction Experience

The "user" splits into two roles, each with a distinct first-touch experience [research 08 §3]:

| Role | First-touch experience | Target | Source basis |
|------|------------------------|--------|--------------|
| **Repo maintainer / reviewer** (trigger-er) | Reply to a PR review comment with `@bot <level> [flags]` | Single comment; ≤4 whitelisted tokens to learn | research 08 §3 (control surface = mention grammar) |
| **Operator** (deploys the daemon) | Install the systemd Dispatcher unit + sandbox image (`deploy/remediate-bot/`) | Greenfield deploy; no `deploy/` precedent in-repo today [CODE-VERIFIED absent, research 04/08] | research 04 §6, 08 §2 |

**Time-to-first-value (proposed targets, latency-bound by design):**

| Metric | Proposed target | Rationale / source |
|--------|-----------------|--------------------|
| Mention → Dispatcher detection | ≤ 30–60 s (poll-bound) | `MIN_POLL_INTERVAL = 30` is [CODE-VERIFIED] in `pr_submit/fsm.py`; spec floors polling at ≥30 s [research 04/06/08] |
| Mention → first thread reply (propose) | Set an explicit target; benchmark bar is PR-Agent "single LLM call, ~30 s"; avoid Copilot's criticized 90 s+ cold-start stop-go UX | research web-01 Rec 5 |
| Tokens-to-learn the control surface | 4 (autonomy level + `--depth` + `--scope` + `--rounds`) | research 08 §3 |

> **Important:** The conservative **propose-only default** (no flag ⇒ `propose`) is the dominant
> UX decision [research 08 §3]. It directly answers the market leader's #1 documented complaint:
> GitHub Copilot Coding Agent unconditionally opens a child PR "even when the comment says don't…
> intent is ignored, no middle ground" (GitHub Community #190027) [research web-01 §1.2]. Every
> credible source converges on propose-by-default / human-approves / agent-cannot-self-merge
> [research web-01 §5.1, web-02 §4, web-03 §1].

### 16.2 Core User Flows

| Flow | Steps | Success Criteria | Source |
|------|-------|------------------|--------|
| **F1 — Happy path: authorized `fix`** | (1) Augment/human leaves a PR review comment flagging an issue → (2) authorized collaborator replies `@bot fix --depth deep` → (3) Dispatcher polls (≤30–60 s), runs live authz gate on the **replier**, claims the trigger in the ledger, resolves the **parent** comment as `opComment`, parses whitelisted flags → (4) sandboxed Runner checks out PR-head, runs `/sc:troubleshoot` against `OP_COMMENT_JSON.body` **as DATA**, validates, emits a diff (propose) or sandbox-branch commit (fix) → (5) Dispatcher pushes host-side with a short-lived token, replies to the thread with summary + pushed SHA | Authorized fix lands on the PR branch; thread reply carries the summary + SHA; no secret ever entered the Runner env (AC-7) | research 08 §3; web-01 §3.2; web-03 §1.1 |
| **F2 — Unauthorized trigger (read-only user)** | A `read`-permission user `@`-mentions the bot → Dispatcher's live per-trigger collaborator-permission gate rejects the **replier** | Polite ack-reject, **zero action** (AC-1); the parent author supplies only data, never authority | research 08 §3 (critical UX safety property) |
| **F3 — Escalation to `push`/`resolve`** | Trigger-er specifies an explicit higher autonomy flag | `push` is reachable **only** with: explicit flag **AND** write-permission **AND** passing validation (lattice-min); `resolve` additionally resolves the review thread | research 08 §3; lattice `propose<patch<fix<push<resolve` (research 01/05) |
| **F4 — `needs_human_decision` HALT** | Runner classifies the finding as needing a human decision (ambiguous intent / security trade-off / API-contract change / multiple valid fixes) | Item **HALTs**; never auto-pushed, even at higher autonomy levels (inherits V1.0 FR-4.4). ⚠️ The HALT machinery is [CODE-VERIFIED] consumed in `pr_submit/fsm.py`, but **no Python code sets the flag today** — the populator is agent/skill-driven [CODE-VERIFIED gap, research 06] | research 01/05/06 §8 |

**UX safety invariants (the experience is defined by what the bot will NOT do):**

- The **replier is the sole authority**; the parent comment author supplies only data [research 08 §3].
- The bot uses **`--comment` only — never `--approve`/`--request-changes`**; humans merge. This is an existing, [CODE-VERIFIED] cultural invariant in the severity rubric ("the verdict does NOT translate into a `gh pr review --approve`") [research 07/08].
- Clear **AI provenance** on generated commits/PRs is a market expectation; the `Co-Authored-By` debate is about provenance/accountability, not authorship [research web-03 §1.4].

### 16.3 Accessibility Requirements

| Requirement | Standard | Implementation |
|-------------|----------|----------------|
| GUI accessibility (WCAG, keyboard nav, screen reader, color contrast) | **N/A for this feature** | No GUI/web surface exists; the interface is a GitHub PR comment + a headless systemd service [research 08 §3]. Defer to the Platform PRD for any platform-level surface. |

### 16.4 Localization Requirements

| Requirement | Priority | Status |
|-------------|----------|--------|
| Multi-language UI | **N/A for this feature** | The control surface is a fixed-token English `@`-mention grammar; no localized UI strings [research 08 §3]. Defer to the Platform PRD. |

---

## 17. Legal & Compliance Requirements

> **Scope note:** This feature's primary compliance surface is **data handling of untrusted GitHub
> comment text** and the **audit trail** of autonomous actions. The broader regulatory frameworks
> below are included because the external research establishes them as table-stakes vocabulary for
> the on-prem / regulated segment this product targets — and because the feature's split-host
> architecture is what makes those postures attainable. Platform-level certification ownership
> (SOC 2 audit, formal DPA) defers to the Platform PRD.

### 17.1 Regulatory & Standards Compliance

| Regulation / Standard | Requirement | How this feature's design addresses it | Status / Source |
|-----------------------|-------------|-----------------------------------------|-----------------|
| **EU AI Act (high-risk)** | High-risk compliance obligations; deadline **August 2026** | On-prem split-host model sidesteps the `pull_request_target` secret-injection exposure entirely (secrets live with the Dispatcher, never in the Runner that sees untrusted text); procurement-grade differentiator | ⬜ Proposed positioning [research web-01 §3.4] |
| **OWASP LLM01:2025 Prompt Injection** + **OWASP Top 10 for Agentic Apps** (Dec 2025) | Prompt injection named the #1 LLM/agentic risk; "no fool-proof prevention exists" → mandates defense-in-depth | `opComment` treated as untrusted data inside a trusted prompt envelope; tool minimization (Runner cannot push); propose-only default; secret separation; bounded scope — each maps 1:1 to an OWASP control | ⬜ Standards-aligned by construction [research web-02 §2.4, web-03 §2.1] |
| **CSA GitHub-Actions research note** (May 2026) | "Architectural separation of the reasoning layer from the credential-holding execution layer" prescribed as **the fundamental mitigation** | Runner = reasoning layer (no host secrets, processes untrusted text); Dispatcher = credential-holding execution layer (holds tokens, evaluates structured output against policy, never processes untrusted input) — a 1:1 description of the design | ⬜ Architecture prescribed by industry body [research web-01 §3.2, web-03 §2.2] |
| **NIST AI RMF / ISO 42001** | Now reference specific prompt-injection prevention/detection + sandboxing controls | On-prem + sandbox + audit-ledger + least-privilege design satisfies referenced controls; trigger ledger provides evidence | ⬜ Compliance accelerant [research web-02 §4, web-03 §4.2] |
| **SOC 2 / GDPR / ISO 27001 / data residency** (FedRAMP, HIPAA) | Code/data cannot leave the VPC; certifications are table-stakes for regulated buyers | On-prem, no-third-party-Action posture keeps code behind the corporate firewall; sidesteps GitHub-Actions supply-chain surface (tj-actions, GhostAction, trivy-action) | ⬜ Roadmap signposting; segment competitors (Tabnine SOC2 Type II, Windsurf FedRAMP High/DoD IL5/ITAR) lead with these [research web-01 §2.2, web-02 §2/§3] |
| **Fork-only PR targeting (C5)** — internal governance | Every GitHub-mutating call must pin `--repo IronbellyOrg/IronClaude`; no push to upstream | H5 `gh_call()` chokepoint **unconditionally injects** `--repo`; first *code-level* enforcement of a rule that is **prose-only today** (CLAUDE.md + skill markdown), and which previously failed (PR mis-targeted to upstream) | ⬜ Net-new hardening [CODE-VERIFIED prose-only today, research 03/04/05/06] |

### 17.2 Data Privacy & Handling

| Data Type | Collection Purpose | Retention | Handling / User Rights |
|-----------|--------------------|-----------|------------------------|
| **`opComment` (parent review-comment body)** | Input to remediation; the issue to be fixed | Captured in the trigger ledger as the exact triggering input | Treated as **untrusted DATA**, JSON-encoded in a CONTROL/DATA envelope delivered via stdin — **never** shell-interpolated as `/sc:troubleshoot "${opComment}"` [research 08 §5, web-02 §2]. Length-capped (SC-2) under the 16 MiB `PROMPT_MAX_BYTES` guard [CODE-VERIFIED `process.py`, research 01/08] |
| **Trigger ledger record** (trigger id, exact `opComment`, replier identity, authz result, decision, outcome, pushed SHA) | At-most-once claim mutex + tamper-evident audit provenance | Append-only on-disk (atomic temp + `os.replace`; per-PR `flock`) | Immutable audit log; surfaces "every trigger + exact input + decision" for NIST AI RMF / ISO 42001 evidence and source-traceability [research web-02 R4, web-03 §4.2] |
| **GitHub credentials** (`GH_TOKEN`, short-lived push token, `ANTHROPIC_*`) | Host-side push + Claude auth | Held by Dispatcher only; never written into the Runner env | **Secret separation (INV-001/SC-7):** Runner `/proc/<pid>/environ` must contain no `GH_TOKEN`/push token/`ANTHROPIC_*` (AC-7). ⚠️ NOT achievable by `ClaudeProcess.env_vars` alone — `build_env()` is additive over `os.environ.copy()`; requires an allowlist/empty-base env path or a secret-free sandbox parent [CODE-VERIFIED gap, research 01/02/03/06/07/08] |
| **Runner network egress** | Reach Claude proxy + GitHub for the single repo only | Per-run; sandbox is disposable | Deny-by-default egress, allowlist `:4000/cli` proxy + `api.github.com` + single-repo git (INV-015); external log/ledger forwarding before Runner teardown [research web-03 §3, 04 Q-1/Q-6] |

### 17.3 Terms, Policies & Release Gates Required

- [ ] **Adversarial prompt-injection test suite as a release-blocking acceptance gate** — systematic red-teaming against the `opComment`/trigger channel (per CSA, "a standard gate in the deployment review process"); reuse public PoC payloads (hidden `-- Additional instruction --` blocks, `gh issue edit $TOKEN` exfil attempts, white-on-white text, fake "authorized/urgent" framing) [research web-02 R2/§2.3, web-03 R3].
- [ ] **Secret-scrape regression test** — assert `GH_TOKEN`/push-token ∉ Runner env (AC-7) [research 07/08].
- [ ] **`gh` `--repo` injection test** — assert no code path can construct a `gh` argv lacking `--repo IronbellyOrg/IronClaude` (AC-4); optional CI grep-guard against raw `gh` outside `gh.py` [research 03/04/06].
- [ ] **AI-provenance policy** on generated commits/PRs (provenance/accountability, not authorship) [research web-03 §1.4/R7].
- [ ] **Deployment-guidance constraint:** never run the self-hosted Runner against public repos (fork-PR code-execution risk) [research web-03 §3.2].
- [ ] Data Processing Agreement (DPA), Privacy Policy, Acceptable Use Policy — **defer to Platform PRD** (platform-level obligations).

---

## 18. Business Requirements

> **Scope note:** This is a feature of the SuperClaude framework running on the
> **IronbellyOrg/IronClaude** fork; the end user is a repo maintainer / on-call reviewer on that
> fork [research 08 §3]. It has **no independent pricing, monetization, or GTM** of its own —
> 18.1's pricing table is therefore **N/A**, replaced by feature-specific cost drivers. The market
> and competitive data below is included as **strategic justification and positioning context**
> (per the feature-PRD scope guidance), not as a revenue plan. ⚠️ Market-size figures vary 100×+ by
> analyst scope — treat **trend direction and the named use case**, not absolute dollars, as the
> reliable signal [research web-01 §4.1 caveat].

### 18.1 Monetization Strategy

**Pricing Model: N/A** — internal/on-prem capability of the platform; no per-feature pricing or GTM.

**Feature-specific cost drivers (the only "business" cost surface for this feature):**

| Cost driver | Notes | Source |
|-------------|-------|--------|
| **LLM token consumption** | Each trigger spawns a `claude -p` Runner; `max_turns` is the throttle — propose ≈ 30, fix ≈ 60 (default 100 is too high and must be overridden per autonomy level) [CODE-VERIFIED default, research 07/08] | research 07/08 |
| **Sandbox compute** | One ephemeral, disposable sandbox (container/microVM) per trigger; per-PR push budget (default 2, hard cap 5) bounds re-runs [CODE-VERIFIED `DEFAULT_MAX_ROUNDS=2`/`HARD_CAP=5` in `pr_submit/fsm.py`, research 03/04/06] | research 03/04/06 |
| **Daemon residency** | Long-lived Dispatcher (systemd) polling at ≥30 s floor; minimal steady-state cost between triggers | research 04/08 |
| **Industry pricing trend (context)** | Market moving seat-based → usage-based; outcome-based pricing (pay-per-resolved-issue) projected 2028–2030 — relevant if this is ever externalized | research web-01 §4.2, web-03 §4.1 |

### 18.2 Market & Strategic Justification (positioning context)

**Why this feature matters to the business — the competitive whitespace:**

1. **The named, emerging high-value use case.** Analysts explicitly name "**autonomous pull request resolution**" and "**security vulnerability discovery and remediation**" as *emerging high-value* (not yet commoditized) use cases inside a fast-growing agentic-dev market [research web-01 §4.2].
2. **The on-prem × mention-triggered intersection is empty whitespace.** Cloud incumbents (Copilot Coding Agent, Amazon Q, Cursor) lead mention-triggered/autonomous coding but are **cloud-only / not self-hostable** (Copilot Enterprise "cloud-dependent"; Cursor 3/10 self-host). Air-gap leaders (Tabnine, Windsurf, Qodo) ship **inline/IDE assist, not autonomous PR-remediation bots**. **No incumbent occupies both axes** [research web-01 §2.2/§4.4, web-03 §4.2].
3. **The product's value proposition IS the governance posture.** "Governance-by-design" is the dominant 2026 enterprise narrative; autonomy without audit/injection-resistance is "a compliance liability" [research web-03 §4.2/§4.3].

**Competitive landscape (feature-comparison context):**

| Product | Trigger model | Apply model | Self-hostable? | Source |
|---------|---------------|-------------|----------------|--------|
| **This feature (V2.0)** | `@bot` reply on review comment | **Propose-only default**; lattice up to push/resolve, gated | **Yes — on-prem split-host** | research 08, web-01/02/03 |
| GitHub Copilot Coding Agent | `@copilot` / issue assign | Draft PR, never auto-merge | No (GitHub-Actions cloud) | web-01 §1.1, web-03 §1.1 |
| Claude Code `@claude` action | `@claude` mention (Actions `if` convention) | Fix in isolated env / review | No (GitHub-Actions cloud) | web-02, web-03 §1.2 |
| Devin (Cognition) | PR open/update (Actions) | Review + optional fix; pre-push hook blocks agent pushes | No (SaaS) | web-03 §1.3 |
| CodeRabbit / Ellipsis / Qodo Merge / Greptile | Auto-on-PR or command | Review-centric; Ellipsis/Qodo implement fixes | Mostly cloud; Greptile self-host segment | web-01 §1.3, web-02 §1 |
| PR-Agent (Qodo OSS) | `/review` `/improve` tags + CLI | Suggestions, single LLM call ~30 s | Yes (CLI/Docker/Action) | web-01 §1.3, web-03 §1.4 |

**Positioning Statement** (derived from research, not aspirational):
"For **regulated/on-prem engineering teams** who are **structurally locked out of cloud-only PR-fix agents**, the `superclaude remediate` bot is a **mention-triggered, headless, on-prem remediation capability** that **proposes fixes by default and proves it cannot exfiltrate secrets or push unauthorized code**. Unlike GitHub Copilot Coding Agent and the public `@claude` action, it runs the reasoning layer with no host credentials and gates every consequential action on a credential-holding Dispatcher outside the LLM's reach" [research web-01 §1.1, web-02 §2, web-03 §1.1].

### 18.3 Adoption & Strategic Risks (the trust dynamics)

| Factor | Evidence | Implication for this feature |
|--------|----------|------------------------------|
| **Adoption-vs-trust gap** | 84% dev adoption but only ~29–33% trust AI output; SonarSource: 66% refuse to merge without manual review, only 3% trust AI output | Sells *safety & control*, not raw autonomy; propose-only default is the market-validated posture [research web-01 §4.3, web-02 §4] |
| **Over-action erodes trust** | "Every time an AI bot auto-posts a comment a team doesn't agree with, trust erodes… within months half the team mutes the bot"; Copilot's #1 complaint is unconditional triggering | Conservative default + authz gate + intent evaluation is the retention argument, not just safety [research web-01 §1.2/§4.3, web-02 §4] |
| **~95% of GenAI tools "not production-ready"** | Failure mode is poor *workflow integration*, not model capability | Differentiator is integration (systemd daemon + ledger + existing `superclaude` CLI surface), not model power [research web-01 §4.3] |
| **Detection/prompting is not a defense** | 78-study meta-analysis: every tested coding agent vulnerable, >85% adaptive attack success; guardrails reduce but never eliminate | Architecture (isolation + least-privilege + propose-only), not "better guardrails," is the only credible posture [research web-02 §2/§4] |

### 18.4 Go-to-Market & Support

**N/A for this feature** — it is an internal/on-prem platform capability with no independent GTM or
support tier. Any future externalization, support SLAs, and pricing tiers **defer to the Platform
PRD**. The research-supported GTM *direction* (lead with the proven "Comment and Control" threat
class; target regulated segments — defense, finance, healthcare, government, telecom — that are
structurally locked out of cloud-only agents) is recorded here as positioning input only [research
web-01 Rec 1–3, web-02 R1/R6, web-03 R1].

---

> **Cross-references:** All KPIs/success metrics → **§19 Success Metrics & Measurement** (single
> source of truth). Threat-model and security architecture → **§14 Technical Requirements** / **§20
> Risk Analysis**. Autonomy lattice, push budget, and HALT semantics → **§8/§9** of the spec.
