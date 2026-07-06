# Web Research — Topic 3: External Market & Ecosystem (PR Auto-Remediation V2.0)

> **Product:** PR Auto-Remediation V2.0 — Mention-Triggered Headless Bot
> **Topic:** External market and ecosystem research (competitive landscape, comparable
> products, best practices, technology trends) for the mention-triggered, headless,
> on-prem PR remediation bot.
> **Date:** 2026-06-11
> **Status:** ✅ COMPLETE — incremental writing
> **Note:** Codebase is source of truth for current capabilities. External research adds
> market context and competitive intelligence; it does not override verified behavior.

---

## Research Scope

The product is a `superclaude remediate` CLI group: a **split-host** bot where a long-lived
Dispatcher polls GitHub for `@bot` mentions in PR review-comment replies, runs a live
authorization gate, claims triggers in an on-disk ledger, and dispatches an ephemeral,
sandboxed Runner that runs `claude -p` against an isolated PR-head checkout — treating the
parent review comment as **untrusted data inside a trusted prompt envelope**.

External research therefore targets these market/ecosystem axes:

1. **Competitive landscape** — mention-triggered & autonomous PR/code-fix agents.
2. **Comparable products** — feature sets, trigger models, sandboxing, propose-only defaults.
3. **Best practices & standards** — prompt-injection containment for LLM-on-untrusted-input,
   GitHub automation security (token scoping, OIDC, ephemeral runners).
4. **Technology trends** — agentic coding, headless CLI agents, on-prem/self-hosted posture.

---

<!-- Findings appended incrementally below -->

## 1. Competitive Landscape — Mention-Triggered & Autonomous PR/Code-Fix Agents

**Relevance: HIGH.** This is the category our product directly competes in. The dominant
2025 pattern is "delegate-to-agent → agent opens/updates a PR," and our differentiator is
**on-prem, headless, split-host, propose-only-by-default** with explicit injection
containment around the untrusted parent comment.

### 1.1 GitHub Copilot coding agent (cloud agent) — the category leader

- **Source (official, HIGH):** GitHub press release, "GitHub Introduces Coding Agent For
  GitHub Copilot," May 19, 2025 — https://github.com/newsroom/press-releases/coding-agent-for-github-copilot
- **Source (official, HIGH):** GitHub Changelog, "Copilot coding agent is now generally
  available," Sept 25, 2025 —
  https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available
- **Source (official docs, HIGH):** "About GitHub Copilot cloud agent" —
  https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent

Key facts:
- **Trigger model:** assign a GitHub issue to Copilot, use the agents panel, or **`@copilot`
  mention in a PR comment to ask it to make changes**. Also supports scheduled / event-driven
  "Copilot automations." This is *very* close to our mention-trigger surface — confirming the
  product category is real and validated by the platform owner.
- **Execution model:** runs autonomously in an **ephemeral dev environment powered by GitHub
  Actions**, pushes commits to a **draft pull request**, then requests review. → Validates our
  ephemeral-Runner + propose-only posture. The market norm is *draft PR, human reviews*.
- **Scope guardrails (official):** "Copilot can only make changes in the repository specified
  when you start a task… cannot make changes across multiple repositories… can only work on
  one branch at a time and can open exactly one pull request." → Mirrors our single-PR,
  single-checkout isolation. Market-validated guardrail.
- **Enterprise gating:** Copilot Business/Enterprise admins must enable it via a Policies
  page. → Confirms enterprises expect an explicit org-level authorization gate (our live
  authorization gate is the on-prem analogue).

**How it relates / supports-vs-contradicts:** SUPPORTS our architecture strongly. The biggest
incumbent uses the *same* primitives (mention/assign trigger, ephemeral env, draft-PR /
propose-only, single-repo scope). **Contrast (our differentiator):** Copilot's environment is
GitHub-Actions cloud and tied to GitHub's control layer; **our product is on-prem / self-hosted
with a split Dispatcher/Runner host and short-lived host-side tokens** — a posture Copilot does
not offer for teams that cannot send code to GitHub-hosted runners.

### 1.2 Claude Code GitHub integration (`@claude` mention + Code Review)

- **Source (official docs, HIGH):** Claude Code Docs — Code Review —
  https://code.claude.com/docs/en/code-review
- **Source (tutorial, MEDIUM):** CodingNomads, "Claude GitHub Actions: Automate PR Reviews
  & Issues" — https://codingnomads.com/claude-github-actions-automate-pr-review

Key facts:
- **Trigger model:** `@claude` mention in issue/PR comments via GitHub Actions events
  (`issue_comment`, `pull_request_review_comment`, `issues`). Crucially, the doc notes **"the
  `@claude` mention pattern is a convention enforced in your workflow's `if` condition, not
  something GitHub handles natively"** (`contains(github.event.comment.body, '@claude')`). →
  Directly mirrors our Dispatcher polling + mention-detection design; confirms the trigger is
  an application-level convention we must implement, not a platform primitive.
- **Required minimal permissions:** `contents`, `pull-requests`, `issues`, `id-token`. →
  Useful baseline for our token-scope minimization.
- **Code Review feature:** multi-agent review leaving inline comments with severity markers
  (🔴 Important / 🟡 Nit / 🟣 Pre-existing) and `file:line` citations; triggers `@claude review`
  (subscribes to push) vs `@claude review once` (single). Anthropic reports <1% of findings
  marked incorrect in internal testing.
- **Secret handling:** store `ANTHROPIC_API_KEY` in repo secrets, never in workflow files. →
  Aligns with our secret-separation requirement.

**Relates:** SUPPORTS. Same `claude -p`/headless lineage as our Runner. **Differentiator:**
the public `@claude` action runs in GitHub-hosted Actions; our product is the **on-prem,
split-host** version with a hardened untrusted-comment envelope and an on-disk trigger ledger
for at-most-once claiming — concerns the GitHub-Actions convention does not address.

### 1.3 Devin (Cognition) — autonomous PR review/fix

- **Source (vendor, MEDIUM-HIGH):** Cognition, "Devin 101: Automatic PR Reviews with the
  Devin API" — https://cognition.ai/blog/devin-101-automatic-pr-reviews-with-the-devin-api

Key facts:
- GitHub Actions workflow triggers on PR open/update/reopen; Devin clones the repo, views
  diffs, optionally **runs the code locally to verify**, reads prior PR discussion, and posts
  inline comments. Takes ~5–10 min per PR.
- Notable security primitive in their own prompt: **a pre-push git hook that blocks any push
  from a "Devin AI" user / `devin-ai-integration` email** — an explicit guardrail to prevent
  the agent from pushing. → Reinforces that the market treats agent-initiated pushes as a
  controlled, gated action (our host-side-only push with short-lived tokens is the stronger
  analogue).
- Vendor explicitly recommends Devin as "an extra set of eyes, not a complete replacement for
  human oversight." → Market consensus on **human-in-the-loop / propose-only** defaults.

**Relates:** SUPPORTS propose-only + human oversight norm. Devin is cloud-SaaS; our on-prem
posture is the differentiator.

### 1.4 PR-Agent (Qodo/CodiumAI), Greptile, Macroscope, others — the broader ecosystem

- **Source (vendor blog, MEDIUM):** Metacto, "Automating Pull Request Workflows with PR-Agent"
  — https://www.metacto.com/blogs/automating-pull-request-workflows-with-pr-agent
- **Source (community, LOW-MEDIUM):** ITK Discourse, "AI generated pull requests overwhelming"
  — https://discourse.itk.org/t/ai-generated-pull-requests-overwhelming-hard-to-review-carefully/7728

Key facts:
- **PR-Agent (open source):** config via `.github/pr_agent.toml`, model-agnostic
  (`gpt-*`/`claude-*`), commands to generate descriptions, review, suggest improvements,
  answer questions. → An open-source comparable; our product is more security-hardened and
  remediation-focused (writes fixes), not just review/describe.
- **Greptile:** noted to "excel for teams on GitLab or with **self-hosting requirements**,"
  agent-style semantic search loop. → Confirms a real market segment that *demands self-hosting*
  — our exact on-prem niche.
- **Macroscope:** "auto-approval for safe PRs," custom rules without YAML, usage-based pricing.
- **Ecosystem pain signal:** maintainers report **AI-generated PRs are overwhelming and hard to
  review carefully**, and debate over `Co-Authored-By: Claude` attribution ("the AI doesn't get
  paged" — provenance, not authorship). → Reinforces that **propose-only with clear provenance
  and bounded scope** is a market necessity, not gold-plating. Validates our conservative default.

**Relates:** SUPPORTS. The self-hosting segment (Greptile) and the "review fatigue" pain both
argue for our on-prem, conservative-by-default, provenance-clear design.

## 2. Best Practices & Standards — Prompt-Injection Containment for LLM-on-Untrusted-Input

**Relevance: HIGH (CRITICAL).** This is the *central engineering risk* the product exists to
neutralize: executing an LLM agent with file-write + git-push authority in response to
untrusted GitHub comment text. External research converges strongly with the codebase design.

### 2.1 OWASP — prompt injection is the #1 LLM/agentic risk (authoritative)

- **Source (standards body, HIGHEST):** OWASP Gen AI Security Project, "LLM01:2025 Prompt
  Injection" — https://genai.owasp.org/llmrisk/llm01-prompt-injection
- **Source (standards body, HIGHEST):** OWASP **Top 10 for Agentic Applications** (published
  **December 2025**), cited as formally naming prompt injection the leading agentic risk.

Key facts / mitigations endorsed by OWASP:
1. **Constrain model behavior** — explicit role/capabilities/limits in the system prompt;
   instruct the model to ignore attempts to modify core instructions.
2. **Define and validate expected output formats.**
3. **No fool-proof prevention exists** — prompt injection is inherent to how models work;
   RAG/fine-tuning do **not** fully mitigate it. → Mandates *defense-in-depth*, not a single
   filter. **This is the strongest external validation of our layered design** (authorization
   gate + injection containment + propose-only default + secret separation + bounded scope).

**Relates:** SUPPORTS, authoritatively. Our untrusted-data-inside-trusted-envelope framing is
exactly OWASP's "clearly delimit untrusted content from instructions" guidance.

### 2.2 Cloud Security Alliance — Prompt Injection in AI-Powered GitHub Actions (direct hit)

- **Source (industry research, HIGH):** Cloud Security Alliance, "Prompt Injection in
  AI-Powered GitHub Actions," research note, May 2026 —
  https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_ai_github_actions_security_20260503-csa-styled.pdf

This source is almost a spec for our threat model. Key facts:
- **Foundational vulnerability:** the hazardous *combination* of (a) an AI agent processing
  **untrusted repository content** (PR titles, issue bodies, code comments, commit messages)
  and (b) that same agent holding **tools** — code execution, git operations, secret access.
  Each is fine alone; together they are dangerous. → **Exactly our risk statement.**
- **Mitigation — treat all repo content as untrusted input** at the same boundary as web app
  input. → Validates treating `opComment` as untrusted data.
- **Mitigation — structurally delimit untrusted content from instructions** in the prompt. →
  Validates our "trusted prompt envelope" wrapping the untrusted comment.
- **Mitigation — minimize the agent's tool set:** "An agent that reviews code for security
  issues does not need the ability to push commits; restricting available tools reduces the
  consequences of successful prompt injection." → **Directly validates propose-only default**
  and host-side-only push (the Runner should not hold push capability).
- **Process recommendation:** systematic prompt-injection red-teaming against *all* untrusted
  input channels should be "a standard gate in the deployment review process."

**Relates:** SUPPORTS, near 1:1. EXTENDS the codebase by recommending injection red-teaming as
a formal release gate — a testing-strategy input for our PRD/TDD.

### 2.3 Real-world exploit evidence — why the gate must hold

- **Source (vendor research, MEDIUM-HIGH):** Aikido Security, "PromptPwned: Prompt Injection
  Vulnerabilities in GitHub Actions Using AI Agents" —
  https://www.aikido.dev/blog/promptpwnd-github-actions-ai-agents
- **Source (vendor research, MEDIUM-HIGH):** Cequence, "Even the Best AI Agents Leak Secrets" —
  https://www.cequence.ai/blog/ai/even-the-best-ai-agents-leak-secrets-prompt-injection-is-why
- **Source (vendor, MEDIUM):** Teleport, "How to Prevent Prompt Injection" —
  https://goteleport.com/blog/prevent-prompt-injection
- **Source (vendor, MEDIUM):** MintMCP, "The Complete Guide to Prompt Injection Attacks" —
  https://www.mintmcp.com/blog/prevention-detection-ai-agents

Key facts:
- **Aikido PoC:** workflows that inject `${{ github.event.issue.title/body }}` straight into an
  AI prompt are exploitable even when passed via env vars — env vars stop *string command
  injection* but **not prompt injection**; the model still receives attacker text and can be
  steered. PoC agent had `gh issue comment/view/edit` + `echo` shell tools — enough to leak
  secrets. → Validates that **tool-restriction**, not just input-escaping, is the real control.
- **Cequence / academic:** a systematic analysis of **78 studies** found **every tested coding
  agent was vulnerable to prompt injection, with adaptive attack success rates >85%.** One
  demonstrated attack posted stolen credentials into a public PR comment, then the attacker
  reverted the title and deleted the PR to erase evidence. → Validates **secret separation**
  (the Runner must never hold exfiltratable long-lived credentials) and **audit/ledger** for
  tamper-evidence.
- **Teleport:** prompt injection "does not bypass infrastructure controls; it steers
  autonomous systems with legitimate access into committing the attack themselves." → Validates
  **least-privilege + external authorization** (our live authorization gate evaluated *outside*
  the LLM, on the Dispatcher) rather than trusting the model to self-police.
- **Industry stats (MintMCP, citing OWASP/IBM/McKinsey):** prompt injection = OWASP #1 LLM
  risk for 2025; attack success 50–88% depending on model/technique; IBM $4.4M average breach
  cost; defense requires layered technical + governance + monitoring controls.

**Relates:** SUPPORTS strongly + raises the stakes. CONTRADICTS any "just sanitize the input"
shortcut: the evidence says input filtering alone is insufficient. Our multi-layer design is
the correct posture; the research argues we must **not** weaken propose-only or secret
separation for convenience.

### 2.4 Defensive design patterns the product already embodies (or should cite)

- **Source (curated, MEDIUM-HIGH):** tldrsec/prompt-injection-defenses —
  https://github.com/tldrsec/prompt-injection-defenses
- **Source (vendor, MEDIUM):** OffSec, "How to Prevent Prompt Injection" —
  https://www.offsec.com/blog/how-to-prevent-prompt-injection

Patterns relevant to our architecture:
- **"Limit the blast radius"** (Simon Willison): assume injection is *unfixable*; design so that
  if untrusted text reaches the model, the damage is bounded. → Our ephemeral Runner +
  propose-only + no-push-from-Runner = blast-radius minimization.
- **Dual-LLM / Privileged vs Quarantined pattern:** a privileged LLM (trusted input, holds
  tools) paired with a quarantined LLM (untrusted content, **no tools**), passing tainted
  content by opaque token reference. → Conceptual cousin of our **split Dispatcher (trusted,
  holds auth + push) / Runner (handles untrusted comment, sandboxed)**. Worth citing in the
  TDD as prior art for the trust split.
- **NVIDIA AI Red Team:** treat all LLM output as potentially malicious; apply the *lowest*
  privilege across all entities that contributed to the prompt; parameterize all external calls.
- **Least privilege + zero-trust for agents** (Obsidian, OffSec, Teleport): never trust agent
  requests by default; grant minimum tools; segment data access; avoid passing full
  configs/env (`printenv`, `get_config`) into agents. → Validates secret separation and minimal
  Runner toolset.

**Relates:** SUPPORTS + provides citable prior art (Dual-LLM, blast-radius, NVIDIA red-team)
for the PRD/TDD security rationale.

## 3. Best Practices & Standards — Ephemeral Runners, Short-Lived Tokens, Secret Minimization

**Relevance: HIGH.** Our split-host design (ephemeral per-trigger Runner + Dispatcher pushing
with short-lived tokens + secret separation) maps almost exactly onto the consensus hardening
checklist for self-hosted CI runners. The market has *already standardized* these controls.

### 3.1 GitHub's own self-hosted runner guidance (authoritative)

- **Source (official docs, HIGH):** GitHub Docs, "Self-hosted runners reference" —
  https://docs.github.com/en/actions/reference/runners/self-hosted-runners

Key facts:
- **Ephemeral runners** (`--ephemeral`): GitHub auto-deregisters the runner after **one job**;
  you wipe the environment after. Purpose: "limit the exposure of any sensitive resources from
  previous jobs… mitigate the risk of a compromised runner receiving new jobs." → Validates our
  **disposable per-trigger Runner** (no state carried between triggers).
- **Caveat (important for our PRD):** GitHub warns there is **no hard guarantee** a self-hosted
  runner runs only one job — so ephemerality "raises the bar significantly" but is not a
  complete control; it must be combined with isolation. → Our PRD should not claim ephemerality
  alone is sufficient; pair it with sandboxing + least privilege.
- **Logging:** ephemeral runner logs must be **forwarded to external storage** before the env is
  destroyed. → Input for our audit/observability requirement (the trigger ledger + run logs must
  survive Runner teardown).

### 3.2 Industry hardening consensus (StepSecurity, AWS, LinuxSecurity, Sysdig)

- **Source (vendor, HIGH):** StepSecurity, "7 GitHub Actions Security Best Practices" —
  https://www.stepsecurity.io/blog/github-actions-security-best-practices
- **Source (cloud vendor, HIGH):** AWS DevOps Blog, "Best practices working with self-hosted
  GitHub Action runners at scale on AWS" —
  https://aws.amazon.com/blogs/devops/best-practices-working-with-self-hosted-github-action-runners-at-scale-on-aws
- **Source (vendor, MEDIUM-HIGH):** LinuxSecurity, "Efficiently Secure Your Self-Hosted GitHub
  Actions Runners On Linux" —
  https://linuxsecurity.com/howtos/learn-tips-and-tricks/github-actions-runner-security-linux
- **Source (vendor research, HIGH):** Sysdig, "How threat actors are using self-hosted GitHub
  Actions runners as backdoors" —
  https://www.sysdig.com/blog/how-threat-actors-are-using-self-hosted-github-actions-runners-as-backdoors

Converged hardening checklist (each item maps to a product requirement):
- **Replace long-lived credentials with short-lived OIDC tokens** ("one-build tokens that then
  die"). → Validates our **short-lived host-side push tokens**; suggests OIDC/STS-style minting
  over static PATs where the GitHub/host boundary allows.
- **Minimize sensitive data on runner machines:** "Keep secrets, SSH keys, and API tokens off
  runner infrastructure. Assume any user who can invoke workflows has access to the runner
  environment." → **Directly validates secret separation** — the Runner must not hold push
  creds or long-lived secrets; the Dispatcher holds and uses them host-side.
- **Restrict runner network access:** no cloud metadata services, no prod DBs; deny-all egress
  baseline, allowlist only essential endpoints. → Input for Runner sandbox network policy.
- **Enforce deny-all permission baseline / least privilege per repo** (IAM role assumption via
  OIDC, per-repo least-privilege). → Validates per-trigger least-privilege scoping.
- **Never use self-hosted runners with public repos** (fork-PR code execution risk). → A
  deployment-guidance constraint our docs should state explicitly.
- **Harden the runner image; isolate from prod networks & k8s control planes; mandatory review
  for `.github/workflows/` changes.**

**Relates:** SUPPORTS comprehensively. Our split-host + short-lived token + secret-separation +
sandbox design is the *textbook* hardened-self-hosted-runner pattern, applied to a
mention-triggered remediation bot. EXTENDS the codebase with concrete checklist items
(external log forwarding, deny-all egress, public-repo prohibition) worth lifting into the
PRD's non-functional/security requirements.

### 3.3 OIDC / short-lived token momentum (trend signal)

- **Source (community, MEDIUM):** r/devops, "Use cases for OIDC in GitHub Actions" —
  https://www.reddit.com/r/devops/comments/1iir0gv/use_cases_for_oidc_in_github_actions
- **Source (practitioner, MEDIUM):** David Dal Busco, "Building a GitHub Actions Integration
  with OIDC Authentication," Feb 2026 —
  https://daviddalbusco.com/blog/building-a-github-actions-integration-with-oidc-authentication

Key fact: practitioner consensus that **static secrets are an anti-pattern**; the direction of
travel is JWT-proven, per-run, auto-expiring tokens scoped to repo/branch/actor. → Reinforces
that "short-lived tokens" is not gold-plating but the expected 2026 baseline; our design is
on-trend, not ahead-of-need.

## 4. Technology Trends — Agentic Coding Market, On-Prem Demand, Governance-by-Design

**Relevance: MEDIUM-HIGH.** Sets the macro context: a fast-growing agentic-coding market where
the under-served, high-value segment is **governed, auditable, self-hosted/on-prem** deployment
— precisely our product's positioning.

### 4.1 Market size & growth (analyst data)

- **Source (analyst, HIGH):** Mordor Intelligence, "Agentic AI Frameworks Market" —
  https://www.mordorintelligence.com/industry-reports/agentic-artificial-intelligence-frameworks-market
  - Market USD **2.99B (2025) → 4.11B (2026) → 19.32B (2031)**, **36.3% CAGR**.
  - **Open-source frameworks led with 63.8% share (2025)** — developers favor "composability,
    auditability, broad integration." → Supports our open, CLI-composable, auditable approach.
  - **Cloud-hosted held 71.3% share (2025)** — meaning **self-hosted/on-prem is the minority
    (~29%) but is the explicitly under-served, security-driven segment** we target.
  - MCP had **>11,000 active public servers by early 2026** — integration layer maturing fast.
- **Source (analyst, HIGH):** Gartner, "Enterprise AI Coding Agent Market: 2026 Guide" —
  https://www.gartner.com/en/articles/enterprise-ai-coding-agent-market
  - Market expanding rapidly since mid-2025; shift from **seat-based to usage-based pricing**
    (agentic parallel/background execution drives consumption).
  - Vendors expanding from code-gen into **code review, testing, design** — i.e., toward the
    *remediation* part of the SDLC our product occupies.
  - **90% of engineering leaders report productivity improvements; net avg gain 19.3%.**
- **Source (analyst, MEDIUM):** AtScale citing Gartner — by end of 2026, **40% of business
  applications will embed task-specific AI agents (up from <5% in 2025)**; WEF projects a
  **$236B AI-agent market by 2034** —
  https://www.atscale.com/blog/best-agentic-ai-tools

### 4.2 On-prem / governed segment is the explicit gap

- **Source (vendor, MEDIUM):** VDF.AI, "Best Tools for Agentic Coding in 2026 (on-prem)" —
  https://vdf.ai/blog/best-tools-agentic-coding-on-prem-code-assistants
  - Surveys the field (Copilot, Codex, Claude Code, Cursor, Windsurf, Junie, Cody, Qodo) and
    finds most are **cloud-first**; flags **"governed on-premise enterprise coding assistance"**
    and **local-model control** as the hard, under-served problem. → Direct market validation of
    our on-prem niche.
- **Source (vendor, MEDIUM):** TrueFoundry, "10 Best Agentic AI Platforms in 2026" —
  https://www.truefoundry.com/blog/agentic-ai-platforms
  - Enterprises "demand role-based access, immutable audit logs, and policy enforcement to
    prevent data leaks, **prompt injection**, and unauthorized actions. Without those controls,
    autonomy becomes a compliance liability." Highlights **VPC / on-prem / air-gapped** as a key
    differentiator. → Validates our authorization gate + ledger/audit + injection containment as
    *table-stakes* enterprise requirements, not extras.

### 4.3 Governance-by-design is the dominant 2026 narrative

- **Source (vendor PR, MEDIUM):** HCLSoftware Tech Trends 2026 —
  https://www.prnewswire.com/news-releases/hclsoftware-tech-trends-2026-ai-autonomy-set-to-transform-the-self-driving-enterprise-302674843.html
  - **76% of leaders prioritize AI agents; 81% have live/pilot initiatives; but governance is
    the "missing link" for 25%.** Tagline: "autonomous by default… sovereign by design;
    governance-by-design as critical as innovation-by-design."
- **Source (vendor, MEDIUM):** Kore.ai, "7 best agentic AI platforms 2026" — lists "Governance,
  safety & observability" (audit logs, permissions, guardrails, compliance) as a core
  selection criterion; DIY agents "rarely have full auditability." —
  https://www.kore.ai/blog/7-best-agentic-ai-platforms

**Relates:** SUPPORTS. The macro trend — autonomous agents adopted fast, but **governance/
audit/injection-resistance is the gating constraint** — is exactly the problem our security-first,
on-prem, propose-only design solves. CONTRADICTS nothing in the codebase; EXTENDS it by
confirming the value proposition is the *governance posture*, not raw autonomy.

---

## Key External Findings

1. **The product category is real and validated by the platform owner.** GitHub Copilot cloud
   agent uses the *same* primitives we do — `@mention`/assign trigger, ephemeral execution env,
   **draft-PR / propose-only**, single-repo/single-branch scope, org-level enable gate. Claude
   Code's `@claude` action and Devin confirm the mention-trigger + human-oversight pattern.
   (Sources: GitHub press/changelog/docs, Claude Code docs, Cognition — all HIGH.)

2. **Our differentiator is on-prem / split-host / governed.** Every major comparable is
   cloud-first (Copilot on GitHub Actions, Devin SaaS, public `@claude` action). The
   self-hosted/governed segment (~29% of market, per Mordor) is explicitly named as the hard,
   under-served problem (VDF, TrueFoundry, Greptile). On-prem + auditability + injection
   resistance = our defensible position.

3. **Prompt injection is the #1 agentic risk, is effectively unsolved, and demands
   defense-in-depth — exactly our design.** OWASP LLM01:2025 + OWASP Top 10 for Agentic Apps
   (Dec 2025) name it the leading risk with no fool-proof fix. The CSA GitHub-Actions research
   note (May 2026) is a near-spec for our threat model: untrusted repo content + tool-bearing
   agent = the core hazard; mitigations are *delimit untrusted content*, *minimize tools*
   ("a reviewer doesn't need push"), and *red-team all input channels as a release gate*.
   (Sources: OWASP, CSA — HIGHEST/HIGH.)

4. **Empirical evidence raises the stakes.** A synthesis of 78 studies found **every tested
   coding agent vulnerable to prompt injection, >85% adaptive success**; real exploits leaked
   secrets into PR comments and erased evidence (Cequence, Aikido). Input filtering alone is
   insufficient. → Our **secret separation** (Runner holds no exfiltratable long-lived creds),
   **external authorization gate** (evaluated outside the LLM), and **tamper-evident ledger**
   are necessary, not optional.

5. **Our split-host + short-lived-token + secret-minimization design is the textbook hardened
   self-hosted-runner pattern.** GitHub's own docs + StepSecurity + AWS + Sysdig converge on:
   ephemeral disposable runners, short-lived OIDC tokens over static PATs, keep secrets/tokens
   *off* the runner, deny-all egress + endpoint allowlist, external log forwarding, never use
   self-hosted runners with public repos. These map 1:1 onto our architecture and add concrete
   checklist items. (Sources: GitHub docs, StepSecurity, AWS, Sysdig — HIGH.)

6. **Market timing is favorable and governance is the gating constraint.** 36% CAGR; agentic
   coding expanding into the review/test/remediation SDLC stage we occupy; "governance-by-design"
   is the dominant 2026 enterprise narrative (HCL: governance the "missing link" for 25%;
   Gartner: 90% report productivity gains). Our value proposition *is* the governance posture.

7. **Market consensus on conservative defaults & provenance.** Devin ("extra set of eyes, not a
   replacement"), maintainer "AI-PR review fatigue," and the `Co-Authored-By` provenance debate
   all argue for **propose-only by default + clear AI provenance + bounded scope** — our exact
   defaults. No external source advocates auto-merge as a safe default for untrusted-triggered
   changes.

## Recommendations from External Research

> **Codebase remains source of truth for current capabilities.** These are market-informed
> recommendations for the PRD/TDD; they do not assert current product behavior.

- **R1 — Position explicitly against cloud-first incumbents.** Lead the PRD's positioning with
  "on-prem / split-host / governed / injection-resistant," contrasting Copilot-cloud and
  GitHub-Actions `@claude`. The market gap (governed self-hosted) is documented; name it.

- **R2 — Cite OWASP + CSA as the security-requirements backbone.** Anchor the PRD/TDD threat
  model in OWASP LLM01:2025, OWASP Top 10 for Agentic Apps (Dec 2025), and the CSA GitHub-Actions
  note. Frame the untrusted-comment envelope, tool minimization, and propose-only default as
  *standards-aligned*, not bespoke.

- **R3 — Make injection red-teaming a formal release gate.** Per CSA, add systematic
  prompt-injection testing against the `opComment`/trigger channel to the PRD's testing strategy
  and acceptance criteria — not just unit tests of the happy path.

- **R4 — Keep the Runner tool-minimal and push-incapable.** External evidence is unanimous: a
  remediation agent processing untrusted text should not itself hold push/secret capability.
  Preserve host-side-only push with short-lived tokens (Dispatcher), and explicitly enumerate
  the Runner's minimal toolset in the TDD. Consider OIDC/STS-minted tokens over static PATs.

- **R5 — Adopt the self-hosted-runner hardening checklist as NFRs.** Lift concrete items into
  non-functional/security requirements: ephemeral disposable Runner (with the caveat that
  ephemerality is not a complete control), external log/ledger forwarding before teardown,
  deny-all egress + endpoint allowlist, no use with public repos, hardened Runner image.

- **R6 — Cite Dual-LLM / blast-radius / NVIDIA-red-team prior art in the TDD.** The trusted
  Dispatcher / untrusted-comment-handling Runner split has named academic/industry lineage
  (Willison's Dual-LLM, "limit the blast radius," NVIDIA AI Red Team least-privilege). Citing it
  strengthens the design rationale and review defensibility.

- **R7 — Hold the line on propose-only + provenance as defaults.** Market consensus and exploit
  evidence both reject auto-merge for untrusted-triggered changes. Keep propose-only the default;
  ensure clear AI provenance on generated PRs/commits (provenance, not `Co-Authored-By`
  authorship); make any auto-apply mode opt-in and gated.

- **R8 — Treat governance/audit as a headline feature, not plumbing.** Given the 2026
  "governance-by-design" narrative and enterprise demand for immutable audit logs, surface the
  trigger ledger, authorization-gate decisions, and run logs as first-class, queryable audit
  artifacts in the product story.

---

**Status:** ✅ COMPLETE — 4 research areas covered (competitive landscape, prompt-injection
standards, ephemeral-runner/token hygiene, market trends), 25+ sources cited with reliability
ratings and explicit support/extend/contradict mapping to codebase findings.

**EXIT_RECOMMENDATION: CONTINUE**
