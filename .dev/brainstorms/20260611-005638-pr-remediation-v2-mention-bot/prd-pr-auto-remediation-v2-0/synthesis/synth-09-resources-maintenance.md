<!--
SYNTHESIS FRAGMENT — PRD Sections 26–28 (Contributors, Related Resources, Maintenance & Ownership)
Product: PR Auto-Remediation V2.0 (Mention-Triggered Headless Bot) — `superclaude remediate` CLI group
Source: synthesized from research/01-08 (codebase reuse investigators) + research/web-01-03 (market/ecosystem)
Verification convention: [CODE-VERIFIED] = confirmed against live source; greenfield = not yet built.
-->

## 26. Contributors & Collaboration

### 26.1 Document Contributors

> **Note:** This PRD was synthesized from a parallel research fan-out (8 codebase-investigator passes + 3 web/market-research passes) against the V2.0 merged-requirements spec. Human owner assignments are **unassigned** as of this Draft (frontmatter `status: 🟡 Draft`, `assigned_to: product-team`); the table records the evidenced contribution streams and reserves the named human roles for sign-off.

| Role | Name | Contribution |
|------|------|--------------|
| Product Owner | [TBD — product-team] | Product vision, scope, autonomy-lattice and propose-only-default decisions |
| Engineering Lead | [TBD] | Split-host (Dispatcher/Runner) architecture, reuse-vs-build accounting, TDD hand-off |
| Security Lead | [TBD] | Prompt-injection threat model, secret-separation (INV-001/SC-7), authorization gate (D5) |
| QA Lead | [TBD] | Acceptance criteria (AC-7 secret-scrape, AC-4 `--repo` injection), §21.3 probe-first gate, injection red-team corpus |
| Codebase Reuse Investigation (research/01–08) | 8 parallel investigator passes | Verified every reuse anchor against live source — `ClaudeProcess` (`process.py:72`), `pr_submit/` decision core, swarm state/atomic-write, severity rubric, `gh`-posting precedent; surfaced the `pr_submit` Reuse-Map omission, the `build_env()` allowlist gap, and the `swarm:2269` mis-citation |
| Web / Market Research (research/web-01–03) | 3 parallel ecosystem passes | Competitive landscape, prompt-injection incident record (2026 CVEs), security-standards alignment (OWASP/CSA), on-prem market sizing and positioning |

### 26.2 How to Contribute

- **Comment inline** for questions, suggestions, or clarifications on specific requirements (especially the open decisions OD-1…OD-4).
- **Tag relevant leads** using @ mentions; route security-invariant changes (INV-001/SC-7, C5 `--repo` pin) to the Security Lead.
- **Update the Open Questions table** when an open decision (sandbox tech OD-1, push-token mechanism OD-2, push-budget default OD-3, `patch` semantics OD-4) is resolved.
- **Re-verify code citations before editing** — multiple reuse citations in the source spec were found stale (`swarm/commands.py:2269`, the `~/.aienv` chmod-600 exemplar, `build_env()` allowlist mechanism). Treat any `file:line` claim as needing a fresh Read before it is relied upon.
- **Coordinate with the in-flight V1.0 `pr_submit` build** — that package is landing in parallel; link decisions that touch the shared decision core rather than forking it.
- **Review quarterly** and flag outdated sections (see Section 28.2).

---

## 27. Related Resources

### 27.1 Customer / Market Research

> Competitive and ecosystem research gathered to position the on-prem, mention-triggered remediation bot. Codebase remains source of truth for capabilities; these sources add market context only.

| Resource | Link | Description |
|----------|------|-------------|
| Web Research — Topic 1 (Market & Ecosystem) | `research/web-01-web-research-topic-1.md` | Competitive landscape, 2026 prompt-injection incident record, market sizing, propose-only positioning |
| Web Research — Topic 2 (Comparable Products & Secure-Agent Best Practices) | `research/web-02-web-research-topic-2.md` | Comparable products, "Comment and Control" threat class, sandbox tooling, OWASP alignment |
| Web Research — Topic 3 (Ecosystem & Standards) | `research/web-03-web-research-topic-3.md` | Mention-trigger UX precedent, ephemeral-runner/token hygiene, governance-by-design trends |
| GitHub Copilot Coding Agent (primary incumbent) | https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available | GA Sep 2025; mention→draft-PR in ephemeral Actions env; #1 documented complaint = unconditional trigger / ignored intent (GitHub Community #190027) |
| Claude Code GitHub Action (`@claude`) | https://code.claude.com/docs/en/code-review | Closest `claude -p` lineage analog; `@mention` is an app-level `if`-condition convention, not a platform primitive |
| Devin (Cognition) — autonomous PR review/fix | https://cognition.ai/blog/devin-101-automatic-pr-reviews-with-the-devin-api | Cloud SaaS; pre-push git hook blocks agent pushes; "extra set of eyes, not a replacement" |
| Comparable bots (CodeRabbit, Ellipsis, Qodo Merge, Greptile, Sweep) | `research/web-02-web-research-topic-2.md` (§Area 1) | Review-vs-fix market split; Greptile 82% bug-catch benchmark; Ellipsis closest commercial fix-implementing peer |
| Market sizing (treat trend, not absolute $) | `research/web-01-web-research-topic-1.md` (§4) | Agentic-dev market estimates diverge 100×; "autonomous pull request resolution" named an emerging high-value use case |

### 27.2 Technical Documentation

> Source specs and **verified** in-repo reuse anchors. The `superclaude remediate` feature is greenfield (`src/superclaude/cli/remediate/` does not exist [CODE-VERIFIED]); anchors below are the existing primitives it builds on.

| Document / Anchor | Link / Path | Description |
|----------|------|-------------|
| V2.0 Merged-Requirements Spec | `../merged-requirements.md` (this brainstorm) | The driving specification this PRD documents |
| V1.0 Predecessor Spec | `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-requirements.md` | "PR Review Auto-Remediation Monitor (V1.0)"; V2.0 is a **host swap** (in-session → headless), not a logic rewrite [CODE-VERIFIED lineage] |
| `ClaudeProcess` headless executor | `src/superclaude/cli/pipeline/process.py:72` | Runner's load-bearing reuse anchor; `build_command()` + stdin prompt delivery (64 KiB chunked, 16 MiB guard) [CODE-VERIFIED]. **Gaps:** no `cwd` param; `build_env()` is additive-only (`os.environ.copy()`) — cannot satisfy INV-001/SC-7 allowlist without a code change |
| `pr_submit/` V1.0 decision core | `src/superclaude/pr_submit/` (`fsm.py`, `severity_router.py`, `classifier.py`, `detection.py`, `models.py`) | Tested decision core (autonomy gate, round counter `DEFAULT_MAX_ROUNDS=2`/`HARD_CAP=5`, severity routing, `DetectionContractLocked`) — **omitted from the spec's Reuse Map**; landing in parallel (git-untracked). `loop_guard.py`/`run_log.py`/`recovery.py` have since landed **built + tested** (`test_loop_guard.py`/`test_run_log.py`/`test_crash_recovery.py`) [CODE-VERIFIED] |
| `remediate_executor.py` (closest R2/R4 analog) | `src/superclaude/cli/roadmap/remediate_executor.py` | Existing `ClaudeProcess`-driven remediation orchestrator: file allowlist, atomic snapshot/rollback, retry, diff-size guard, patch-apply [CODE-VERIFIED] |
| Severity rubric (S1 / §17) | `src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md` | 5-tier rubric; "severity_hint is a hint, not authoritative" — already compiled into `pr_submit.severity_router` [CODE-VERIFIED] |
| `gh`-posting precedent (H4 template) | `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:304–315,349` | Summary/inline comment posting + strict `--comment` (never `--approve`/`--request-changes`). Reply-to-thread + GraphQL `resolveReviewThread` are **net-new in Python** (no committed Python caller; a reference bash flow has since landed in the untracked parallel V1 `sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`) [CODE-VERIFIED] |
| Atomic-write / state persistence reuse | `src/superclaude/cli/swarm/state.py` (`write_state`), `cli/install_hooks.py:443`, `cli/recommend/cache.py` | tmp + `os.replace` atomic-write idiom for the §10 ledger (spec says `os.rename`; code uses `os.replace`) [CODE-VERIFIED]. Per-PR Python `flock` is net-new (only fail-open bash precedent exists) |
| CLI-group registration seam | `src/superclaude/cli/main.py:400–438` | Deferred-import + `main.add_command(..., name="remediate")` with `# noqa: E402,I001` — required wiring step (omitting it ships a dead group) [CODE-VERIFIED] |
| Fork-only `--repo` rule (C5 / H5) | project `CLAUDE.md` + memory `feedback_pr_target_fork_only.md` | `--repo IronbellyOrg/IronClaude` enforced today by **prose only**; no Python `gh` caller exists in the repo — H5 is the first code-level enforcement [CODE-VERIFIED] |

### 27.3 Design Assets

> **N/A for this feature.** The product surface is a `superclaude remediate` CLI group + a systemd service + a ~4-token `@bot` mention grammar (autonomy level, `--depth`, `--scope`, `--rounds`). There is no GUI, web surface, or new slash command for end users (`research/08-agent-8.md` §3). No wireframes/mockups/component-library apply.

### 27.4 Standards, Security & Business References

> External standards and incident evidence that anchor the threat model and the on-prem/governance positioning.

| Document | Link | Description |
|----------|------|-------------|
| OWASP LLM01:2025 — Prompt Injection | https://genai.owasp.org/llmrisk/llm01-prompt-injection | #1 LLM risk; no fool-proof prevention → mandates defense-in-depth (our layered design) |
| OWASP Top 10 for Agentic Applications (Dec 2025) | `research/web-03-web-research-topic-3.md` (§2.1) | Names prompt injection the leading agentic risk |
| OWASP AI Agent Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html | Least-privilege tools, untrusted-data segregation, human approval for high-risk actions, immutable audit logs — design is aligned by construction |
| CSA Labs — Prompt Injection in AI-Powered GitHub Actions (May 2026) | https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-github-actions-security-20260503-csa-st | Prescribes "architectural separation of reasoning layer from credential-holding execution layer" — a 1:1 description of the Runner/Dispatcher split |
| "Comment and Control" (Aonan Guan, JHU, Apr 2026) | https://oddguan.com/blog/comment-and-control-prompt-injection-credential-theft-claude-code-gemini-cli-github-copilot | PR/issue comments leaked secrets from Claude Code, Gemini CLI, and Copilot Agent — the exact threat class the product neutralizes |
| Design Patterns for Securing LLM Agents (Anthropic/ETH/DeepMind) | https://arxiv.org/html/2506.08837v2 | Dual-LLM, blast-radius minimization — theoretical foundation for the split host |
| AWS AgentCore — hosting coding agents | https://aws.amazon.com/blogs/machine-learning/its-safe-to-close-your-laptop-now-hosting-coding-agents-on-amazon-bedrock-agentcore | "Never put the token in the VM"; short-lived scoped tokens — independent convergence on the split-host model |
| GitHub self-hosted runner reference | https://docs.github.com/en/actions/reference/runners/self-hosted-runners | Ephemeral-runner guidance + caveat that ephemerality is not a complete control (pair with sandbox) |
| Anthropic 2026 Agentic Coding Trends Report | https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf | "Collaborative, not fully delegated" — supports propose-only default |
| EU AI Act high-risk compliance deadline | `research/web-01-web-research-topic-1.md` (§3.4) | August 2026 — a buyer-facing positioning anchor for the on-prem posture |

---

## 28. Maintenance & Ownership

### 28.1 Document Ownership

> **Note:** Human owners are unassigned in this Draft (frontmatter `assigned_to: product-team`, `coordinator: product-manager`). Roles below reserve the responsibilities; assign before approval.

| Role | Name | Responsibility |
|------|------|----------------|
| **Primary Owner** | [TBD — product-team] | Overall PRD accuracy, scope, autonomy-lattice/propose-only decisions, Open-Questions resolution |
| **Technical Owner** | [TBD — Engineering Lead] | Split-host architecture, reuse anchors (`ClaudeProcess`, `pr_submit/`, severity rubric), accuracy of all `file:line` citations |
| **Security Owner** | [TBD — Security Lead] | Secret-separation (INV-001/SC-7), `--repo` chokepoint (C5/H5), injection-containment requirements |
| **Backup Owner** | [TBD] | Coverage when primary unavailable |

> **CRITICAL — cross-build coordination:** The V1.0 `pr_submit/` decision core is **landing in parallel** with this PRD (untracked, ~60% built, on branch `fix/prd-advisory-gate`). Ownership MUST coordinate so V2.0's `cli/remediate/` host layer **extends** `pr_submit`'s pure core (FSM, severity router, models) rather than forking a divergent autonomy/round/severity machine — shipping two decision cores would be a Source-of-Truth/duplication violation (`research/04-agent-4.md` G-1, `research/06-agent-6.md` §C).

### 28.2 Review Schedule

> **Note:** High-level review cadence is defined in the Contract Table (Completeness Status section). This section captures detailed scheduling for each review type.

| Review Type | Next Date | Participants |
|-------------|-----------|--------------|
| **Full Review** | [TBD — before TDD hand-off] | Product, Engineering, Security, QA leads |
| **Technical Review** | [TBD] | Engineering + Security; re-verify reuse citations against live source |
| **Security Review** | [TBD — gate before any `gh`-calling code] | Security Lead; validate INV-001/SC-7, C5/H5 `--repo` chokepoint |
| **§21.3 Probe Gate** | [TBD — hard prerequisite before parser/H4 code] | Engineering; lock `in_reply_to_id` / `databaseId` / Augment bot login from a throwaway fixture PR |
| **Ad-Hoc Review** | - | Triggered by major changes (e.g., an Open Decision OD-1…OD-4 resolving) |

### 28.3 Update Process

1. **Propose Changes**: Comment on the specific section or open an issue.
2. **Re-verify code citations**: Before relying on any `file:line` anchor, perform a fresh Read — the source spec carried stale citations (`swarm/commands.py:2269`, `~/.aienv` chmod-600, `build_env()` allowlist mechanism). Mark capability claims `[CODE-VERIFIED]` only when confirmed against live source.
3. **Review with Stakeholders**: Route to the relevant lead; security-invariant changes require the Security Owner.
4. **Coordinate with the `pr_submit` build**: For any change touching the shared decision core, confirm with the V1.0 owner before editing.
5. **Update Document**: Incorporate approved changes; keep Source-of-Truth discipline (`src/superclaude/` → `make sync-dev`).
6. **Increment Version**: Update version number and Document History.
7. **Notify Team**: Announce changes with a summary; flag any change to the autonomy lattice, push budget, or secret boundary.
8. **Archive Old Version**: Retain previous versions for reference.

---

<!-- END SYNTHESIS FRAGMENT — Sections 26–28 -->
