<!--
SYNTHESIS PARTIAL — PRD Sections 1–4 (Executive Summary, Problem Statement,
Background & Strategic Fit, Product Vision)
Product: PR Auto-Remediation V2.0 — Mention-Triggered Headless Bot
Source: research/01–08 (codebase reuse verification) + web-01–03 (market/ecosystem)
Template: .claude/templates/workflow/05_prd_template.md
Evidence convention: [CODE-VERIFIED] = confirmed against current source; everything
describing the V2.0 bot itself is a forward-looking requirement (cli/remediate/ is greenfield).
-->

## 1. Executive Summary

PR Auto-Remediation V2.0 is a **mention-triggered, headless, on-prem pull-request remediation bot**, shipped as a new `superclaude remediate` CLI group. An authorized collaborator replies to a PR review comment with an `@bot`-style mention (e.g. `@bot fix --depth deep`); a long-lived **Dispatcher** (systemd daemon) detects the mention, runs a live authorization gate on the *replier*, claims the trigger in an on-disk ledger, and dispatches an ephemeral, sandboxed **Runner** that runs `claude -p` against an isolated PR-head checkout. The Runner treats the parent review comment (`opComment`) as **untrusted data inside a trusted prompt envelope**, never as instructions, and by default only *proposes* a fix.

The product exists because executing an LLM agent with file-write and git-push authority in response to untrusted GitHub comment text is the dominant agentic-AI attack class of 2026 — demonstrated in the wild against the market leaders ("Comment and Control," Johns Hopkins, Apr 2026; "Clinejection," Feb 2026) and assigned multiple CVEs. The Cloud Security Alliance's prescribed "fundamental mitigation" is an **architectural separation of the agent's reasoning layer from the credential-holding execution layer** — which is a one-to-one description of V2.0's split Dispatcher/Runner host. V2.0 is the headless successor to V1.0's in-session Monitor-tool host: it reuses V1.0's tested deterministic decision core (`src/superclaude/pr_submit/` — severity routing, autonomy gating, round/budget counter, `needs_human_decision` HALT) [CODE-VERIFIED] and rebuilds only the host, the secret-scoped execution boundary, and the GitHub I/O surface.

Strategically, V2.0 occupies a documented market whitespace: the intersection of **mention-triggered PR auto-remediation** (where GitHub Copilot Coding Agent leads but is cloud-only) and **on-prem / air-gapped self-hosted deployment** (where Tabnine/Windsurf/Qodo lead but ship inline/IDE assist, not autonomous remediation bots). No incumbent occupies both axes. Its conservative propose-only default directly answers the market leader's most-complained-about failure mode (Copilot's unconditional trigger that "ignores intent").

**Key Success Metrics:**

- **Runner secret isolation (AC-7):** 0 occurrences of `GH_TOKEN` / push credential / `ANTHROPIC_*` token values in the Runner's `/proc/<pid>/environ`
- **Authorization correctness (AC-1):** 100% of triggers from non-write-collaborators rejected with a polite ack, zero remediation action taken
- **Loop safety (SC-5/SC-6):** per-PR push budget enforced — default 2, hard cap 5 — surviving daemon restarts via the disk-authoritative ledger
- **Conservative default:** `propose` is the effective autonomy level whenever no level flag is supplied; reaching `push` requires explicit flag **AND** write-permission **AND** passing validation (lattice-minimum)
- **Injection containment:** adversarial prompt-injection corpus passes as a release-blocking acceptance gate (opComment never interpolated as instructions)

---

## 2. Problem Statement

### 2.1 The Core Problem

**There is no safe way to let an autonomous agent act on a PR review comment when that comment is untrusted text and the agent holds file-write and git-push authority.**

- **What is the current state?** When a reviewer (human or the Augment review bot) flags an issue on a PR, a maintainer must manually context-switch back into the PR, re-derive the fix, apply it, push, reply, and resolve the thread. The V1.0 predecessor automated this only *inside a live Claude session* hosted by the in-session Monitor tool — which dies the moment the session closes (V1.0 red-team risk R3), making 24/7 unattended remediation impossible.
- **Who is affected?** Repo maintainers and on-call reviewers on the `IronbellyOrg/IronClaude` fork, and more broadly any team that wants review findings remediated without a human babysitting a terminal session — especially regulated teams that cannot send code to cloud-hosted runners.
- **What is the impact/cost of not solving this?** The naive "just run the agent on the comment" approach is actively dangerous. In 2026 a single crafted PR title / issue body / review comment caused GitHub Copilot Agent, Claude Code, **and** Gemini CLI to leak their own API keys and `GITHUB_TOKEN` into publicly visible PR comments ("Comment and Control," Johns Hopkins, Apr 2026), with zero maintainer interaction beyond the automated trigger. "Clinejection" (Feb 2026) chained an issue-title injection into a live npm supply-chain compromise. The root cause is vendor-agnostic: *"any agent given both a bash execution tool and access to secrets while ingesting untrusted comment text"* is exploitable — and *"LLMs cannot tell the difference between instructions and data"* (OpenAI CISO: prompt injection is an acknowledged unsolved problem).
- **What barriers exist today?** (1) Host longevity — an in-session host cannot run unattended. (2) Secret blast radius — the existing `ClaudeProcess.build_env()` is additive-only (`os.environ.copy()` + merge), so it **cannot strip** an inherited `GH_TOKEN` from a spawned child [CODE-VERIFIED, `cli/pipeline/process.py:145-160`]. (3) No authorization concept — V1.0 had no notion of *who* is allowed to trigger an action. (4) Trust — only ~3–33% of developers trust AI output (SonarSource 2026: 66% refuse to merge without manual review), so any bot that over-acts erodes trust and gets muted within months.

### 2.2 Why Existing Solutions Fall Short

**Cloud-hosted mention-triggered agents (GitHub Copilot Coding Agent, public `@claude` Action, Devin):**

- Run in GitHub-Actions-hosted / SaaS cloud environments — structurally unavailable to air-gapped or regulated teams that cannot send code to cloud runners (Copilot Enterprise is "cloud-dependent, not natively self-hostable"; Cursor scores 3/10 on self-hosted deployment).
- Most rely on `pull_request_target`, which **injects secrets into the runner** — the exact exposure underlying most 2026 GitHub-Actions agent CVEs.
- Copilot Coding Agent **unconditionally opens a child PR even when the comment says "don't do anything"** — "intent is ignored, no conversational mode, no middle ground" (GitHub Community Discussion #190027), the market leader's #1 documented complaint.

**Third-party review/remediation bots (CodeRabbit, Ellipsis, Qodo Merge, Greptile, Sweep):**

- Most stop at *review/suggest* and deliberately avoid taking file-write + push authority; the ones that do implement fixes foreground little-to-no untrusted-input / secret-separation story.
- Configuration lives in-repo (`.github/workflows/`, `.toml`) and runs on the cloud platform — same data-residency and supply-chain surface (tj-actions, GhostAction, trivy-action tag-poisoning).

**V1.0 in-session Monitor-tool host (`sc:pr-submit`):**

- Hosted by the in-session Monitor tool; the live session must remain open (V1.0 FR-2.4) — dies on session close (V1.0 R3), so no unattended/24-7 operation.
- Triggered by an Augment review *landing* (poll-and-detect), with no authorization gate and no notion of a third-party `@`-mention triggering action on someone else's behalf.
- Its deterministic core (`pr_submit/`) is sound and reusable, but its **host** is the precise fragility V2.0 exists to eliminate.

### 2.3 The Market Opportunity

Solving this unlocks a documented, under-served segment. "Autonomous pull request resolution" and "security vulnerability discovery and remediation" are **analyst-named emerging high-value use cases** (not yet commoditized) inside a fast-growing agentic-development market (estimates vary by scope: ~$2.99B agentic-AI-frameworks 2025 → ~$19.32B by 2031 at 36.3% CAGR; ~$10.4B agentic-dev 2025 at ~39.5% CAGR — treat *trend direction*, not the absolute figure, as the reliable signal). Within it, the **on-prem × mention-triggered-remediation intersection is empty whitespace**: cloud incumbents lead the trigger UX but cannot self-host; on-prem leaders ship inline/IDE assist, not autonomous remediation bots. A governance-first posture (live authorization gate, immutable trigger ledger, secret separation, propose-only default) is exactly what 2026 enterprise buyers name as the *gating constraint* on agent adoption — "governance-by-design as critical as innovation-by-design" — and aligns with the EU AI Act high-risk compliance deadline of **August 2026**.

---

## 3. Background & Strategic Fit

### 3.1 Why Now?

1. **The threat is real, named, and exploited (not hypothetical).** Prompt injection against tool-bearing coding agents went from theory to in-the-wild supply-chain compromise in early 2026 (Comment-and-Control, Clinejection, CVE-2025-66032, CVE-2026-22708, CVE-2026-21852). A 78-study meta-analysis found **every tested coding agent vulnerable, with adaptive attack success >85%**, and OWASP named prompt injection the #1 risk in both LLM01:2025 and the new **OWASP Top 10 for Agentic Applications (Dec 2025)**. Building remediation *without* the split-host containment is no longer defensible.
2. **The industry has converged on the exact mitigation V2.0 implements.** The CSA Labs research note prescribes separating the reasoning layer (no credentials, processes untrusted text) from the credential-holding execution layer (evaluates a structured recommendation against policy, never touches untrusted input) — independently mirrored by Simon Willison's Dual-LLM pattern, the Anthropic/ETH/DeepMind "Design Patterns for Securing LLM Agents" paper, AWS AgentCore's "never put the token in the VM," and OSS sandboxes (microsandbox, brood-box, cplt). V2.0's Dispatcher/Runner split *is* this pattern.
3. **The reusable foundation already exists in-repo.** The headless spawn primitive `ClaudeProcess` (`cli/pipeline/process.py:72`) is verified — stdin prompt delivery bypassing the 128 KB argv limit, a 16 MiB pre-spawn guard, process-group kill, lifecycle hooks [CODE-VERIFIED]. V1.0's deterministic decision core (`pr_submit/` — `fsm.evaluate_push_decision`, `should_halt_rounds` with `DEFAULT_MAX_ROUNDS=2`/`HARD_CAP_MAX_ROUNDS=5`, `severity_router`, `DetectionContractLocked`) is built and tested [CODE-VERIFIED]. The severity rubric (`sc-auggie-review-protocol/refs/severity-rubric.md`) and the `gh` posting precedent are in place. The host is the only large greenfield surface — meaning the riskiest *logic* is already paid down.
4. **The market gap and the compliance clock are open simultaneously.** No incumbent occupies the on-prem × mention-triggered-remediation intersection; the most-adopted tools (Cursor 67% Fortune 500) score *lowest* on self-hosted deployment and enterprise governance. The EU AI Act high-risk deadline (Aug 2026) and NIST AI RMF / ISO 42001 referencing prompt-injection controls make a governed, auditable, self-hosted posture a near-term procurement requirement, not a future nicety.

### 3.2 How This Fits Company / Framework Objectives

- **Mission Alignment:** Extends the SuperClaude framework's existing operator-automation surface (`sprint`, `swarm`, `roadmap`, `pipeline` all wrap `ClaudeProcess`) with a 24/7 unattended remediation capability, while honoring the framework's hard invariants — fork-only `--repo IronbellyOrg/IronClaude` targeting, SoT/sync-dev discipline, and human-owned merge state.
- **Reuse / Cost Posture:** The build is "a mostly-new subsystem with a few sturdy anchors": reuse the V1.0 pure decision core and `ClaudeProcess`, build new only the I/O + host layer V1.0 deliberately externalized. This avoids duplicating ~3 tested modules of decision logic and prevents divergent severity grading between the `sc:pr-submit` skill and the daemon.
- **Market Position:** Targets the explicitly under-served governed/on-prem segment (~29% of the agentic-frameworks market by share, the security-driven minority) where cloud incumbents structurally cannot follow.
- **Competitive Moat:** The split-host secret-separation architecture is a credibility moat backed by named 2026 CVEs — "same `@mention` UX as `@claude`/Copilot, but architected so a malicious comment can't exfiltrate secrets or push unauthorized code."

### 3.3 Strategic Bets

1. **Architecture-as-mitigation beats guardrails.** Bet: because detection/prompting demonstrably *reduce but never eliminate* injection (>85% adaptive success), the durable defense is structural — secret separation + ephemeral sandbox + propose-only + external authorization — not a better filter. The whole split-host design rests on this.
2. **Conservative-by-default wins the trust deficit.** Bet: in a market with 84% adoption but ~3–33% trust, a bot that proposes and lets a human/authorization gate decide will be adopted and retained where auto-acting bots get muted. Reaching `push` must require explicit flag + write-permission + passing validation (lattice-minimum), and `propose` is the no-flag default.
3. **On-prem headless is a defensible niche, not a feature checkbox.** Bet: the unserved intersection of mention-triggered remediation and self-hostable deployment is large enough (regulated defense/finance/healthcare/gov/telecom) to justify the operational cost of a systemd daemon + sandbox over a cloud Action.
4. **The trigger model is the real novelty; the decision core is shared.** Bet: V2.0's genuine new surface is the mention grammar + parent resolution, live per-trigger authorization, the split host + sandbox, host-side short-lived-token push, and reply/resolve — while autonomy/round/severity/HALT logic is inherited from `pr_submit`. Mis-scoping this (rebuilding the core) would be the project's biggest avoidable cost and an SoT-duplication risk.

---

## 4. Product Vision

**"Any review comment can be safely remediated by an authorized mention — fixed, pushed, replied to, and resolved by a headless bot that treats every comment as untrusted and can never be talked into leaking a secret or pushing unauthorized code."**

When V2.0 succeeds, a maintainer on the `IronbellyOrg/IronClaude` fork no longer babysits a Claude session to act on review findings. They (or any write-collaborator) simply reply to a flagged comment with `@bot fix --depth deep`, and a 24/7 systemd-hosted Dispatcher takes it from there: it verifies the *replier* is authorized, claims the trigger exactly once in a durable ledger, hands the untrusted parent comment to an ephemeral sandboxed Runner as data-in-an-envelope, validates the result, and — only when the autonomy lattice, write-permission, and validation all permit — pushes host-side with a short-lived token, replies with the summary and SHA, and resolves the thread. By default it proposes; it never modifies merge state; humans still merge.

The end state is a governed, auditable remediation control plane that an independent security research body would recognize as the prescribed "fundamental mitigation" for the dominant agentic-AI threat of the era — delivered on-prem, where the cloud incumbents cannot go, and built into the SuperClaude CLI rather than bolted on. Every trigger, every authorization decision, and every exact opComment input is recorded in an immutable ledger, turning provenance and audit from internal plumbing into a first-class, queryable feature that answers the market's loudest demand: *show me what the agent did, why, and on whose authority.*

---
