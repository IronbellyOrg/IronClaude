# PREAMBLE — Verification-Gap Brainstorm Context

> **Audience:** You are a brainstorm agent invoking `/sc:brainstorm` to produce the best
> structural fix for a class of verification-gap defects in the SuperClaude/Claude-Code
> audit skills. This preamble is your entire context — you cannot ask the human follow-up
> questions. Where Socratic interaction in `/sc:brainstorm` would normally seek answers
> from a user, answer from this preamble; if the preamble doesn't cover a question,
> make an explicit `[INFERRED]`-tagged assumption and continue.

---

## 1. Triggering incident (the example, not the problem)

A `/sc:troubleshoot` REPORT diagnosed four startup-log patterns in a fresh Coder workspace.
One pattern was *"docker: command not found"* from `agentcontainers ... dockercli.List`.
The REPORT's Action 3 prescribed: rebuild the AIDev02 image so docker.io is installed
(the Dockerfile already had `docker.io \` in its APT layer; the running image apparently
predated that line).

`/sc:task` shipped two PRs:

- **PR #66** — dotfiles UX cleanup (relax `dotfiles_uri` to optional; CI-placeholder sentinel guard).
- **PR #67** — Dockerfile.coder SHA bump (42-line comment block) to force Terraform's
  `triggers.dockerfile_sha256` to fire on next `coder update`, prompting a fresh image build.

`/sc:reflect --mode post` audited the PRs. **Verdict: `status: success`, T1, C=0.91, all 3 actionable REPORT actions ✅**.
Audit shipped to `.dev/reflect/post-troubleshoot-implementation-20260530-230000/REPORT.md`.

After the operator merged both PRs and ran `coder update <wks>`, `which docker` still
returned **empty**. `locate docker` showed:

- `/usr/sbin/dockerd` ✓ — daemon binary present
- `/usr/sbin/docker-proxy` ✓ — present
- `/usr/bin/docker-init` ✓ — init helper present
- `/var/lib/dpkg/info/docker.io.list` ✓ — dpkg thinks `docker.io` is installed
- **`/usr/bin/docker` — MISSING** — the CLI client

Root cause: on **Debian 13 trixie**, the `docker.io` package was split. `docker.io` ships
the daemon only; `/usr/bin/docker` is in a separate package called `docker-cli`.
With `--no-install-recommends`, `docker-cli` was silently skipped. The image rebuild that
PR #67 forced re-ran the same broken install line and produced the same broken image.

**The reflect verdict was a false-positive clean-ship.** Action 3 was marked
`per_task_validation_strength: 0.88`, `evidence_validator_ran: false`, `status: success`.
The bug was findable from the operator's seat with one `which docker`. The bug was findable
from the orchestrator's seat with one `WebFetch packages.debian.org/trixie/docker.io`
that the protocol does not mandate.

---

## 2. The verification taxonomy (the framing the brainstorm should use)

Findings emerging from a post-mortem of the miss:

| Cat | Verification question | Tools available to a reflect-class orchestrator | Reflect handled it? |
|-----|----------------------|-------------------------------------------------|---------------------|
| **1. Implementation fidelity** | Does the code match the spec's literal asks? | Read, get_diagnostics, find_referencing_symbols, evidence-validator re-Read of cited `file:line` | ✅ Done; mature |
| **2. Logical fidelity** | Does the mechanism actually produce the claimed outcome under its own internal logic? (E.g., "trigger a rebuild" → does rebuilding *change* the install-list?) | Reasoning over the diff; `root-cause-analyst`-style hypothesis investigation | ⚠️ Possible but not mandated; missed here |
| **3. External-spec fidelity** | Does the upstream artifact (Debian package, npm dep, OS API, Terraform provider) actually provide what the diff assumes? | WebFetch, WebSearch, context7, tavily, Bash (`apt-cache show`, `dpkg -L`, `gh api`) | ❌ Not mandated; missed here |
| **4. Runtime fidelity** | Post-deploy, is the live system in the expected state? | None — orchestrator has no shell on the deploy target | ❌ Genuinely unverifiable without runtime hooks |

The docker miss is a **category-3 + category-4 compound failure**: the protocol didn't
mandate category-3 grounding (would have caught it pre-merge), and the protocol didn't
emit a structured deferred category-4 outcome runbook (would have caught it post-merge
via the operator's check).

---

## 3. Why the obvious patch is whack-a-mole (the rejected non-solution)

A naive proposal: *"Add a mandatory wave step that, for every package / API / binary the
diff names, fans a tavily/WebFetch query and verifies the named artifact's contract."*

The user explicitly rejected this:

> *"This will catch issues with enormous overlap only, you are playing whack-a-mole."*

Why it's whack-a-mole:

- The trigger ("the diff *names* a package") only catches cases where the diff explicitly
  references an upstream artifact by name. A change like "switch the worker pool size from
  4 to 16" doesn't name any upstream artifact but can have category-2/3/4 failures
  (rate-limit violation, downstream service overload, OOM at runtime).
- It only addresses *one shape* of the broader gap (named-package contract). Other shapes —
  performance regressions, behavioral contradictions surfaced only at runtime, integration
  failures across services, third-party API drift — are not caught.
- It's an additive list-of-checks, not a structural recategorization. The next bug will
  exit through whatever check the list didn't enumerate.

**The brainstorm should propose a structural fix that recategorizes the verification
contract, not an additive checklist.**

---

## 4. The real structural gap

Audit skills (`sc:reflect`, `sc:auggie-review`, `sc:validate-roadmap`, `sc:troubleshoot`'s
Wave-6 self-check, `sc:cleanup-audit`) currently treat *"code matches spec"* as equivalent
to *"this change achieves its intended outcome in the production system."* Those are
distinct verifications:

- **Implementation = spec ≡ code.** Verifiable from the repo.
- **Outcome = behavior ≡ intent.** Verifiable only against the running system, the
  upstream artifacts the change depends on, and the downstream consumers the change affects.

The protocols ship `status: success` when implementation verification passes, regardless of
whether outcome verification was even attempted, deferred, or surfaced as a known gap.
There is no first-class concept of *"this verification cannot be performed by this
orchestrator from this seat at this time"* with a structured handoff that any future
agent or operator can pick up and execute against.

The gap is **not** "we need more checks." The gap is **the contract conflates two
distinct verifications**, and the structural mechanisms (evidence-validator,
confidence-calibrator, heterogeneous reviewer ensemble) are all anchored to the first one.

---

## 5. Constraints on the proposed solution

- **Must address the structural conflation**, not enumerate failure shapes.
- **Must generalize across audit skills** — `sc:reflect` is the prompt, but `sc:auggie-review`,
  `sc:validate-roadmap`, `sc:troubleshoot` Wave 6, `sc:cleanup-audit`, and any future
  audit-class skill should benefit without per-skill amendments.
- **Must respect the existing protocol surface** — no rewriting the 4-category deviation
  taxonomy, the 9-condition promotion gate, the calibrator disjoint-set rule, or the
  evidence-validator drop semantics. Additive, not replacement.
- **Must be checkable by a downstream automation** — the verification surface needs to be
  machine-readable so sprint executors, CI gates, and future agents can pick up deferred
  verifications without re-reading prose REPORTs.
- **Must downgrade `status: success` honestly** when outcome verification was not performed.
- **Should integrate with the existing `cannot_validate_without_user_input` contract field**
  rather than introducing a parallel field for the same semantics.
- **Must define a clear next-actor / next-action** for deferred verifications — not just
  "we don't know"; a runbook a fresh agent in a new session can execute.
- **Should not require live runtime access** as a precondition for the audit to ship —
  audits must remain runnable from the orchestrator's seat, with deferred outcome
  verification as the explicit handoff.
- **Should keep token cost proportional** — solutions that add a parallel ensemble of
  external-spec reviewers to every audit are unlikely to be accepted; the ROI envelope
  should stay near the existing T1-only ~3-8k Claude band.

---

## 6. Available protocol surface (concrete affordances to build on)

Brainstorm proposals MAY (and probably should) reference these:

### 6.1 Skills in scope

- **`sc:reflect` / `sc-reflect-protocol`** — at
  `/config/.claude/skills/sc-reflect-protocol/SKILL.md` and
  `/config/.claude/commands/sc/reflect.md`. Two modes (UC-1 pre-execution, UC-2
  post-execution), three tiers (T1 grounded single-agent, T2 heterogeneous ensemble +
  adversarial merge, T3 remediation handoff), 7 waves. Stable v1.0 return contract with
  versioned evolution rules in §9.4.
- **`sc:auggie-review`** — PR/diff review with deep retrieval pass.
- **`sc:validate-roadmap`** — spec-to-roadmap fidelity validation.
- **`sc:troubleshoot`** Wave 6 — Phase B (pre-task analyze) and Phase D (post-task validate),
  both invoke `sc:reflect` under the legacy `--type task --analyze|--validate` grammar.
- **`sc:cleanup-audit`** — read-only multi-pass repo audit.
- **`sc:adversarial`** — Mode A `--compare`, Mode B `--merge` for multi-artifact debate.
- **`task-builder`** — produce MDTM task files from BUILD_REQUEST inputs.
- **`/task`** — execute MDTM task files via the F1 execution loop.

### 6.2 Agents in scope

- `root-cause-analyst`, `self-review`, `requirements-analyst`, `confidence-calibrator`,
  `rf-qa`, `rf-qa-qualitative`, `audit-validator`, `evidence-validator`,
  `socratic-mentor`, `system-architect`, `quality-engineer`, `devops-architect`,
  `backend-architect`, `incident-response:*`, plus any other in
  `/config/.claude/agents/` and
  `/config/.claude/projects/-config-workspace-Coder/agents/` if relevant.

### 6.3 Existing contract fields the solution can leverage or extend

(From `sc:reflect`'s `return-contract.yaml` §9.1, contract_version 1.0)

- `cannot_validate_without_user_input: bool`
- `regression_present: bool`
- `unauthorized_deviation_present: bool`
- `blocked_by_low_confidence: bool`
- `spec_is_wrong: bool`
- `user_decision_required: bool`
- `needs_human_decision: bool`
- `per_task_verdicts[].status`, `.deviation_class`, `.per_task_validation_strength`,
  `.evidence_anchor`
- `grounding_gaps_path` — parallel artifact for evidence-insufficient findings (§10.6)
- `deviation_register_path` — 4-category ledger

### 6.4 MCPs available in the protocol

- `auggie` — codebase retrieval (in-repo)
- `serena` — symbol navigation + project memory + checkpoint nudges
- `context7` — official library/framework docs (currently Tier-2 only)
- `tavily` — web search (currently Tier-2 only, rate-limited)
- `sequential` — multi-step reasoning
- WebFetch / WebSearch — currently NOT in the reflect protocol's allowed-tools
  frontmatter; would need to be added if a proposal depends on them

### 6.5 Cost envelope

Reflect's §15 Token Cost Profile:

- T1 only: ~3-8k Claude orchestration tokens, 1-3 min wall
- T2 (2-3 reviewers + adversarial debate): +~35-70k Claude, +8-15 min wall
- T3 (remediation handoff): +~20-40k Claude, +5-10 min wall

A proposal that adds >5k tokens to every T1 audit is likely uneconomic.
A proposal that adds 1-2k tokens to T1 with a structured handoff for deferred
outcome verification is in the right band.

---

## 7. What the proposal should contain

Output a single Markdown file (path is in your task instructions). Structure:

1. **Problem framing** — your one-paragraph restatement of the structural gap.
2. **Proposed structural fix** — the core idea, named and crisp. Not a checklist; a
   recategorization.
3. **Mechanism** — concrete protocol-text amendments, contract field additions,
   wave/step modifications, new artifacts, new agent roles, or new cross-skill
   integrations. Anchor to actual §section/§step numbers in the existing protocols
   wherever you propose modifications.
4. **How it generalizes** — explicit list of bug shapes the fix would catch beyond
   the docker case (at least: a performance regression, an integration-failure case,
   a third-party-API-drift case, an OS-level package-split case, a runtime-config
   case). For each, walk through how the proposed mechanism surfaces the gap.
5. **Trade-offs and risks** — what does the proposal cost (tokens, wall clock,
   complexity)? What classes of bug does it still miss? What could go wrong with
   the mechanism itself?
6. **Backward-compat with existing protocols** — concrete statement of what changes
   in the v1.0 stable contract; whether this is a minor or major version bump under
   §9.4; what consumers (`superclaude sprint`, `sc:task`, `sc:troubleshoot` Wave 6)
   need to update.
7. **Falsifier** — describe an empirical eval case (modeled on the existing §12.5
   `T2-convergence-wrong-answer` falsifier suite skeleton) that would prove or
   disprove that your proposed fix actually catches docker-class misses.
8. **Out-of-scope items** — what your proposal deliberately does NOT solve, with
   one-line reasoning per omission.

Keep your final markdown between 1500 and 3500 words. Concrete > verbose. Cite
concrete file paths, §section numbers, and field names rather than hand-waving.

---

## 8. Invocation requirements

When you invoke `/sc:brainstorm` (Skill `sc-brainstorm-protocol`):

- Brainstorm framing: *"Propose the best structural fix to the verification-gap class
  exemplified by the docker-cli miss in `sc:reflect`. The fix must address the
  conflation between implementation verification and outcome verification across
  audit-class skills, generalize without being whack-a-mole, and respect the existing
  protocol surface as documented in this preamble."*
- If the brainstorm skill asks Socratic questions: answer from this preamble. If a
  question's answer is not in the preamble, make a `[INFERRED]`-tagged assumption and
  proceed. Do NOT ask the human user — there is no human in this loop.
- If the brainstorm skill spawns its own parallel proposal generators internally, that
  is expected behavior. Let it run.
- At the end, write your final consolidated proposal to the markdown path your
  task instructions specify. Use the §7 structure verbatim.

---

## 9. The reflect-protocol full text (for direct reference)

The full v1.0 protocol is at `/config/.claude/skills/sc-reflect-protocol/SKILL.md`.
Read sections you need — particularly:

- §3 Required Input + Mode Selection
- §4 Wave / Tier Architecture (esp. Wave 1A, 1B, 1D)
- §5 Tier-Decision Rubric (esp. §5.3 priority table)
- §6 Modern Serena Tool Usage (esp. §6.1 "Mandatory" chain and §6.4 think_about_* checkpoints)
- §7 Agent Delegation Map (esp. §7.1 reviewer composition rules)
- §9 Output Contract (esp. §9.1 stable fields and §9.3 Consumer Field Map)
- §10 Deviation Taxonomy (esp. §10.6 Grounding Gaps parallel artifact pattern)
- §11 Hallucination Guardrails (esp. §11.0 sufficiency-conditional language)
- §14 Error Handling Matrix
- §14.5 Wave 7 Promotion Mutation (the 9-condition gate is the structural pattern your
  proposal will likely extend or parallel)
- §17.5 Ops Integration
- §17.6 Testability Map
- §17.7 Kill List (especially the "5th deviation category was rejected" entry — your
  proposal needs to either explicitly route around this kill, or justify revisiting it)
- §19 v1.1 Deferred Hardening (you may propose folding into INV-021/INV-023 hardening)

The full text is your authoritative reference — quote it when your proposal modifies it.

---

## 10. The reflect REPORT and audit log that contained the false-positive

For evidence and grounding, the actual artifacts that proved the gap exist at:

- `/config/workspace/IronClaude/.dev/reflect/post-troubleshoot-implementation-20260530-230000/REPORT.md`
- `/config/workspace/IronClaude/.dev/reflect/post-troubleshoot-implementation-20260530-230000/return-contract.yaml`
- `/config/workspace/IronClaude/.dev/reflect/post-troubleshoot-implementation-20260530-230000/audit.log`
- `/config/workspace/IronClaude/.dev/troubleshoot/coder-workspace-startup-20260530-060500/REPORT.md`
  (the upstream troubleshoot REPORT that contained the "Action 3" recommendation)

You may quote from these directly. The audit.log lists every skipped/run step in
the false-positive audit; cite it when your proposal addresses one of those steps.

---

**End of preamble. Invoke `/sc:brainstorm` now with the framing in §8 and produce your
proposal to the markdown path in your task instructions.**
