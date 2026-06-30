<!--
SYNTHESIS PARTIAL — PRD Sections 1–4 (Executive Summary, Problem Statement,
Background & Strategic Fit, Product Vision) for PR Auto-Remediation V2.0.
Source: research/01-08 (codebase reuse verification) + research/web-01..03 (market/security).
Grounding rule: cli/remediate/ is greenfield — every product behavior is PROPOSED, not current.
Only the reuse anchors (ClaudeProcess, pr_submit/, severity rubric) are [CODE-VERIFIED] as existing.
-->

## 1. Executive Summary

PR Auto-Remediation V2.0 is a `superclaude remediate` CLI group that runs a **mention-triggered, headless, on-prem pull-request remediation bot** for the `IronbellyOrg/IronClaude` fork. An authorized collaborator replies to a PR review comment with an `@bot` mention and a small whitelist of flags (e.g. `@bot fix --depth deep`); a long-lived **Dispatcher** (systemd daemon) detects the mention, runs a live authorization gate on the replier, claims the trigger in an on-disk ledger, and dispatches an **ephemeral sandboxed Runner** that runs `claude -p` against an isolated checkout of the PR head. The parent review comment ("opComment") is treated as **untrusted data inside a trusted prompt envelope** — never shell-interpolated — so a malicious comment cannot steer the agent into leaking secrets or pushing unauthorized code.

The product is a **host-architecture successor to V1.0** (the in-session `sc:pr-submit` Monitor, whose live-session dependency made it fragile when the session closed). V2.0 keeps V1.0's proven deterministic decision core — already built and tested in `src/superclaude/pr_submit/` (`fsm.py`, `severity_router.py`, `models.py`, `detection.py`) [CODE-VERIFIED] — and replaces only the *host*: in-session Monitor tool → systemd Dispatcher + disposable Runner. Execution leans on the existing `ClaudeProcess` headless-spawn primitive (`src/superclaude/cli/pipeline/process.py:72`) [CODE-VERIFIED], which delivers the prompt via stdin (bypassing the 128 KB argv limit) with a 16 MiB pre-spawn guard. The split-host design is a direct implementation of the mitigation that Cloud Security Alliance Labs (May 2026) prescribes as "the fundamental mitigation" for prompt injection in AI-powered GitHub automation: separate the credential-free *reasoning layer* (Runner) from the credential-holding *execution layer* (Dispatcher).

The bot defaults to the most conservative behavior — **propose-only** — and escalates only along an explicit autonomy lattice (`propose < patch < fix < push < resolve`) where the *effective* level is the minimum of the requested flag, the replier's repository permission, and validation outcome, with off-lattice `needs_human_decision` and push-budget HALT short-circuits inherited verbatim from V1.0. This posture answers the single loudest documented complaint about the market-leading incumbent (GitHub Copilot Coding Agent, which "unconditionally opens a child PR even when the comment says don't" — GitHub Community #190027) and occupies a documented market whitespace: no incumbent today serves the **on-prem × mention-triggered PR-remediation** intersection (cloud agents like Copilot/Amazon Q are not self-hostable; on-prem tools like Tabnine/Windsurf/Qodo ship inline/IDE assist, not autonomous remediation bots).

**Key Success Metrics:**

- **Injection containment:** Runner process environment contains **zero** `GH_TOKEN` / push credentials (AC-7: `/proc/<pid>/environ` scrape returns no secret) — 100% of runs.
- **Authorization correctness:** 100% of triggers from non-write-permission repliers are politely ack-rejected with zero file/git action (AC-1).
- **Loop safety:** No PR exceeds the per-PR push budget (default 2, hard cap 5) across any number of daemon restarts; counter is disk-authoritative.
- **Conservative default:** 100% of no-flag mentions resolve to `propose` (no code path can reach `push` without an explicit flag **and** write permission **and** passing validation).
- **Trigger latency:** Mention-to-acknowledgement within one poll interval (poll floor ≥30s, inherited from V1.0 `MIN_POLL_INTERVAL`).

---

## 2. Problem Statement

### 2.1 The Core Problem

**There is no safe way today to turn a reviewer's "@bot, fix this" comment into an actual, applied code change on the `IronbellyOrg/IronClaude` fork — every available path is either session-fragile, cloud-locked, or prompt-injection-exposed.**

When Augment (or a human reviewer) flags an issue on a pull request, closing the loop from *finding* to *fix* is still manual: a maintainer must read the comment, open a session, run a remediation tool, validate, push, and reply. The predecessor that automated this — V1.0's in-session `sc:pr-submit` Monitor — only runs while a Claude Code session stays open; when the session closes, the monitor dies (V1.0 Red-Team risk R3). That session-longevity fragility is the explicit reason a headless host is needed.

- **Current state:** Remediation is either fully manual, or driven by V1.0's in-session monitor that cannot survive session close. The deterministic decision core exists and is tested (`src/superclaude/pr_submit/`) [CODE-VERIFIED], but has no durable, unattended host.
- **Who is affected:** Repo maintainers and on-call reviewers on the fork, who must hand-shepherd every review-comment-to-fix cycle, and who cannot use cloud remediation agents for private fork work.
- **Impact / cost of not solving:** Review findings sit unactioned; the round-trip from comment to merged fix stays human-bound; and any naïve automation that *does* act on comment text inherits the dominant agentic-AI attack class of 2026 (see §2.2).
- **Barriers today:** (1) no headless execution host for `claude -p` remediation; (2) no live authorization gate to decide *who* may trigger an action; (3) no code-level enforcement of the fork-only `--repo` rule — it lives only in prose (`CLAUDE.md`) and was historically violated (a PR mis-landed on the public upstream); (4) the one shared spawn primitive (`ClaudeProcess.build_env`) inherits the full host environment, so secrets leak into any child by construction (see §2.2).

### 2.2 Why Existing Solutions Fall Short

**Cloud mention-triggered coding agents** (GitHub Copilot Coding Agent, Amazon Q, public `@claude` Action):

- **Cloud-locked:** Copilot Enterprise is "cloud-dependent, not supported natively" for air-gap; Amazon Q "cannot be self-hosted or run offline"; Cursor scores 3/10 on self-hosted deployment. None can run on a private fork behind a firewall.
- **Over-triggers / ignores intent:** Copilot Coding Agent unconditionally opens a child PR even when the comment says "don't" or is merely a question — the #1 documented user complaint (GitHub Community #190027): "no conversational mode, no middle ground."
- **Prompt-injection-exposed by construction:** these agents process untrusted PR/issue/comment text *while holding both a bash tool and secrets*. "Comment and Control" (Aonan Guan, Johns Hopkins, Apr 2026) hijacked Claude Code, Gemini CLI, **and** Copilot Agent into leaking `ANTHROPIC_API_KEY`/`GITHUB_TOKEN`/`GEMINI_API_KEY` into public PR comments with zero maintainer interaction.

**In-session / self-hosted assistants** (V1.0 `sc:pr-submit` Monitor; Tabnine, Windsurf, Qodo, Aider):

- **V1.0 Monitor is session-bound:** dies on session close (R3) — no 24/7 unattended operation.
- **On-prem peers are inline/IDE assistants, not remediation bots:** Tabnine/Windsurf/Qodo lead on air-gap compliance but offer inline completion or IDE review, *not* mention-triggered autonomous PR remediation that writes commits.
- **No untrusted-input boundary:** most tools do not treat the triggering comment as untrusted data; the parent-comment-as-data refinement is rarely explicit.

**"Better guardrails / sanitize the input" approaches:**

- **Empirically insufficient:** a synthesis of 78 studies found every tested coding agent vulnerable to prompt injection with adaptive attack success rates >85%; env-var passing stops string command-injection but not prompt injection (Aikido). OWASP LLM01:2025 names prompt injection the #1 risk with "no fool-proof prevention." The consensus root cause (OpenAI CISO, acknowledged unsolved): *LLMs cannot separate instructions from data.* → Defense must be **architectural** (isolation + least-privilege + propose-only), not prompt-level.

### 2.3 The Market Opportunity

Solving this unlocks a documented, under-served intersection. "Autonomous pull request resolution" and "security vulnerability discovery and remediation" are analyst-named **emerging high-value** use cases (not yet commoditized) inside a fast-growing agentic-dev market (Mordor Intelligence: agentic-AI frameworks USD 2.99B in 2025 → 19.32B by 2031, ~36% CAGR; self-hosted/on-prem is the explicitly under-served ~29% segment — treat *trend and named use case*, not absolute dollar figures, as the reliable signal). The crucial unlock is **whitespace at the on-prem × mention-triggered-remediation intersection**: cloud agents lead mention-triggering but cannot self-host; on-prem tools self-host but only assist inline. A headless, on-prem, mention-triggered remediation bot with explicit injection containment occupies an intersection no incumbent currently fills — and does so by implementing the exact reasoning/execution split that independent industry research (CSA Labs) prescribes as the fundamental mitigation, and that AWS AgentCore ("never put the token in the VM"), OSS sandboxes (microsandbox, cplt), and Simon Willison's Dual-LLM pattern have all independently converged on.

---

## 3. Background & Strategic Fit

### 3.1 Why Now?

1. **The decision core already exists and is tested.** V1.0's `src/superclaude/pr_submit/` ships the deterministic brain V2.0 needs — `fsm.evaluate_push_decision` (5-predicate G-push conjunction), `should_halt_rounds` (`>=` fence-post), the `propose<…` autonomy lattice, `severity_router.remap_severity`/`route`, the 3-state detection classifier, and the `Finding`/`SkillResult`/`PushDecision`/`EventType` models — with 4 passing test files [CODE-VERIFIED]. V2.0 reuses the brain and replaces only the hands (I/O + host), so the highest-risk logic is not greenfield.
2. **The headless execution primitive is mature.** `ClaudeProcess` (`cli/pipeline/process.py:72`) already does process-group-killed `claude --print` spawning with chunked stdin prompt delivery, a 16 MiB pre-spawn size guard, a 105-min default timeout, and lifecycle hooks [CODE-VERIFIED] — exactly what an unattended Runner needs. The CLI-group registration seam (`cli/main.py` deferred-import + `add_command`) is a proven one-line-pair pattern used by 10 sibling groups.
3. **The threat the design defends is the proven, named attack class of 2026.** "Comment and Control" (JHU, Apr 2026) and "Clinejection" (in-the-wild npm supply-chain compromise, Feb 2026), plus CVE-2025-66032 / CVE-2026-22708 / CVE-2026-21852, make untrusted-comment-driven agents the dominant agentic attack vector — and CSA Labs prescribes precisely this reasoning/execution split as the mitigation. Building now defends a live threat, not a hypothetical.
4. **Governance-by-design is the gating market constraint.** OWASP Top 10 for Agentic Apps (Dec 2025), NIST AI RMF, and ISO 42001 now reference prompt-injection + sandboxing controls; "governance-by-design" is the dominant 2026 enterprise narrative (HCL: governance the "missing link" for 25%). The propose-only default, authorization gate, and audit ledger are table-stakes, and the project's existing SoT/`--repo`-fork discipline gives a head start.

### 3.2 How This Fits Company Objectives

- **Mission Alignment:** Extends the `superclaude` CLI from interactive/invoke-and-exit tooling (sprint, swarm, roadmap) into the first *unattended, long-lived* surface, closing the review-comment-to-fix loop without a human in every step.
- **Quality & Safety Goal:** Hard-enforces, in code, the fork-only `--repo IronbellyOrg/IronClaude` invariant that is currently prose-only (`CLAUDE.md`) and was historically violated — converting a known operational hazard into a structural guarantee (H5 gh-wrapper chokepoint).
- **Market Position:** Targets the documented on-prem × mention-triggered-remediation whitespace; positions on *safety, control, and governance* (the trust deficit: 84% adoption vs ~3–33% trust) rather than raw autonomy.
- **Competitive Moat:** Secret separation means the Runner never holds an exfiltratable push/Anthropic credential — sidestepping the `pull_request_target` secret-injection exposure underlying most 2026 GitHub-Actions agent CVEs, a moat that cloud-Action incumbents structurally cannot match.

### 3.3 Strategic Bets

1. **Bet — the reasoning/execution split is sufficient containment:** isolating an untrusted-comment-processing Runner (no host secrets) from a credential-holding Dispatcher structurally prevents injection-driven credential theft and unauthorized push, per CSA Labs' "fundamental mitigation."
2. **Bet — propose-only-by-default wins the trust gap:** a conservative default that escalates only via the lattice-min of (flag ∧ permission ∧ validation) is the market-validated posture and directly remedies the incumbent's loudest complaint (Copilot's unconditional trigger).
3. **Bet — reuse the V1.0 brain, not rebuild it:** importing/extending `pr_submit/`'s pure decision core (vs. forking it under `cli/remediate/`) avoids divergent severity grading and double-maintenance, and lets the build concentrate effort on the genuinely net-new I/O surface.
4. **Bet — the net-new GitHub I/O is de-riskable by probe-first:** reply-to-thread + GraphQL `resolveReviewThread`, ETag/304 polling, and `in_reply_to_id`/`databaseId` shapes (zero in-repo precedent) can be locked against a throwaway fixture PR before any parser code is written, making the riskiest surface a bounded spike rather than an open-ended unknown.

---

## 4. Product Vision

**"A reviewer's `@bot` reply becomes a validated, attributable code change — applied with the least authority that the replier, the flags, and the validation jointly permit — without a human in the loop and without ever trusting the comment that triggered it."**

PR Auto-Remediation V2.0 turns the `IronbellyOrg/IronClaude` fork's review threads into a safe, unattended remediation surface. A maintainer no longer babysits the path from finding to fix: an authorized collaborator replies `@bot fix --depth deep` on a review comment, and within one poll cycle a systemd-resident Dispatcher authorizes the *replier*, claims the trigger at-most-once in a durable ledger, and dispatches a disposable sandboxed Runner that remediates the PR head with `claude -p` — treating the flagged comment as inert data, validating before it acts, and escalating only as far as the lattice-minimum of permission, flag, and validation allows. The default is always the safest thing (`propose`); reaching `push` or `resolve` requires an explicit flag, write permission, and a passing validation gate, with `needs_human_decision` and the per-PR push budget as hard HALTs.

When the product succeeds, the fork has a 24/7 governance-grade remediation bot that no cloud incumbent can offer for private work: it sits in the documented on-prem × mention-triggered whitespace, embodies the reasoning/execution separation that security researchers prescribe as the fundamental prompt-injection mitigation, and makes the fork-only `--repo` rule a structural guarantee rather than a discipline. Every trigger, decision, and push is captured in a tamper-evident ledger — provenance and auditability as first-class product surface, answering the 2026 enterprise demand for governed, injection-resistant autonomy. The bot is measured not by how much it does autonomously, but by how reliably it does the *right-scoped* thing safely: correct authorization, contained blast radius, bounded loops, and conservative-by-default behavior the team can trust enough not to mute.

---
