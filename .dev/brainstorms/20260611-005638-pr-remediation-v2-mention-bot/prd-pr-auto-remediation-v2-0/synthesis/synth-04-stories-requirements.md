<!--
SYNTHESIS FRAGMENT — PRD Sections 13, 21.1, 21.2
Product: PR Auto-Remediation V2.0 (Mention-Triggered Headless Bot) — `superclaude remediate` CLI group
Source: research/01-08 (codebase verification) + web-01-03 (market/security best practices)
Evidence convention: [CODE-VERIFIED] = confirmed against current source; [NEW] = greenfield, no current capability.
Per rule 10, only [CODE-VERIFIED] anchors are presented as existing capability; all V2.0 components are [NEW] to-build.
-->

## 13. Open Questions

> Sourced from the merged-requirements Open Decisions (OD-1…OD-4) plus code-grounded gaps surfaced by the parallel codebase investigation (research 01–08). Status legend: 🔴 Urgent (build-blocking) / 🟡 Researching / 🟢 Resolved.

| # | Question | Owner | Target Date | Status | Resolution |
|---|----------|-------|-------------|--------|------------|
| 1 | **Runner secret-isolation mechanism (INV-001/SC-7/AC-7).** `ClaudeProcess.build_env()` (`cli/pipeline/process.py:145-160`) is **additive-only** — `env = os.environ.copy()` then `env.update(env_vars)`; passing `env_vars` can add/override but **cannot strip** an inherited `GH_TOKEN`/push token/`ANTHROPIC_*`. How is "no push credential in the Runner env" achieved: (a) new `base_env`/`env_mode="allowlist"` param on the shared primitive, (b) a Runner-owned env built from `{}`, or (c) a secret-free sandbox parent whose `os.environ` is already minimal? | Engineering (TDD) | Pre-build | 🔴 Urgent | Leaning (c) sandbox-level minimal environ as the primary guarantee (cleanest, aligns with §6 "no host home mount"); if (a) chosen, the edit touches a primitive shared by sprint/roadmap/swarm and must stay back-compatible (default keep current behaviour) with its own regression test. [CODE-VERIFIED additive-only across research 01/02/03/05/06/07/08] |
| 2 | **Reconcile V2.0 against the in-flight `src/superclaude/pr_submit/` V1.0 decision core.** The package (`fsm.py`, `severity_router.py`, `classifier.py`, `detection.py`, `models.py`; tested under `tests/pr_submit/`) is being landed today and overlaps V2's H1/H2/S1/D3/D6 **near 1:1** (e.g. `DEFAULT_MAX_ROUNDS=2`, `HARD_CAP_MAX_ROUNDS=5`, `MIN_POLL_INTERVAL=30`, `evaluate_push_decision` 5-predicate conjunction, `should_halt_rounds`, `remap_severity`/`route`, `DetectionContractLocked`). Does `cli/remediate/` **import-and-extend** `pr_submit` (reuse the brain) or fork it? | Eng Lead + Product | Pre-build | 🔴 Urgent | Strong recommendation across research 01/03/04/05/06: **import the pure decision core, build only the I/O+host layer** (Dispatcher/Runner/gh). Coordinate so V2 work does not race the untracked in-flight V1 build. [CODE-VERIFIED] |
| 3 | **OD-1 — Runner sandbox technology.** Container vs microVM (Firecracker/gVisor/Kata/libkrun) vs kernel-LSM (Landlock + seccomp-BPF). Zero in-repo execution-sandbox precedent (`eval/isolation.py` gives scratch-root *filesystem* confinement only, not network/process isolation). | DevOps + Security | Pre-build (gates R4/S2/§15) | 🔴 Urgent | External consensus (Northflank, CSA, awesome-agent-runtime-security): shared-kernel containers are **insufficient** for untrusted-comment-driven code; production pattern is microVM or kernel-LSM. `microsandbox`/`brood-box`/`cplt` are build-vs-buy references. Genuinely open; gates the largest greenfield surface. |
| 4 | **OD-2 — Host-side push-token mechanism.** GitHub App installation token vs fine-grained PAT vs OIDC/STS-minted short-lived token, scoped to the single fork repo. | DevOps + Security | Pre-build | 🟡 Researching | Industry direction of travel (GitHub docs, StepSecurity, AWS, Sysdig): short-lived OIDC/per-run tokens over static PATs; "keep tokens off the runner." Token lives host-side with the Dispatcher only. |
| 5 | **OD-3 — Per-PR push-budget default & cap.** Provisional `default 2, cap 5` pending the §21.3 probe's measurement of real Augment re-review cadence. | Product | Post-probe | 🟡 Researching | Partly **pre-decided** in code: V1 `pr_submit/fsm.py` already sets `DEFAULT_MAX_ROUNDS=2`/`HARD_CAP_MAX_ROUNDS=5`. Confirm against observed re-review timing in the probe before freezing. |
| 6 | **OD-4 — `patch` autonomy-level semantics.** What `patch` (between `propose` and `fix` on the lattice) is allowed to do vs `fix`. | Product | Pre-build | 🟡 Researching | Lattice is `propose < patch < fix < push < resolve`, default `propose`. The distinct capability ceiling of `patch` is unresolved. |
| 7 | **GitHub reply/resolve API shapes (INV-010).** `databaseId` vs node `id`, `reviewThreads` pagination, `in_reply_to_id` reliability, Augment bot login — **no committed/tracked precedent**; a reference reply→resolve bash flow has since landed in the untracked parallel V1 `sc-pr-submit-protocol` skill (`scripts/reply-resolve-thread.sh`, `refs/augment-poll.md`), but the real byte shapes must still be locked before parser/H4 code. | Engineering | §21.3 probe (hard gate) | 🔴 Urgent | The §21.3 throwaway-fixture-PR probe is a **non-optional hard gate**; captured shapes become committed config constants/fixtures (mirrors V1's `DetectionContractLocked`). The untracked bash flow is a shape reference, not a locked contract. |
| 8 | **`needs_human_decision` populator.** The §8 HALT guarantee rests on a flag that **no Python code sets today** — `Finding.needs_human_decision` is *consumed* in 5+ places in `pr_submit/fsm.py` but `grep 'needs_human_decision = True'` across `src/` returns nothing; the populating taxonomy (ambiguous intent / security trade-offs / API-contract changes / multiple valid fixes) is skill/agent-driven prose. Does V2's autonomous Dispatcher build a **deterministic populator**, or trust the in-sandbox agent to self-report? | Eng Lead + Security | Pre-build | 🔴 Urgent | For an autonomous daemon this is a concrete safety gap: a HALT that nothing triggers does not gate. Recommend a deterministic classifier or an explicit, documented agent-self-report dependency. [CODE-VERIFIED no Python setter] |
| 9 | **Source-home & stale placeholder.** Feature SoT is `src/superclaude/cli/remediate/` (absent today). A top-level `remediation/` dir exists but is **empty** (stale placeholder). | Eng Lead | Pre-build | 🟡 Researching | Confirm feature lives under `cli/remediate/`; delete/ignore the empty `remediation/` to avoid confusion. [CODE-VERIFIED] |
| 10 | **`main.py` group registration step.** D1 needs a deferred-import + `main.add_command(remediate_group, name="remediate")` pair in `cli/main.py:400-438` carrying the mandatory `# noqa: E402,I001` annotation — omitted from the build sequencing. Without it the group is dead; wrong annotation trips `make lint` (E402). | Engineering | Build (D1) | 🟢 Resolved | Add the registration pair with `name="remediate"` explicitly (majority pattern; `cli_portify` omits `name=` — do not copy that). [CODE-VERIFIED convention at `main.py:400-438`] |
| 11 | **Reuse-Map citation correction (`cli/swarm/commands.py:2269`).** Cited as a "monotonic, disk-authoritative, survives-restarts" round counter; the line is actually an **in-memory `swarm status --watch` iteration cap** (resets every run, never persisted). | Tech writer / Eng | Pre-TDD doc fix | 🟢 Resolved | Re-point: durable persistence idiom → `swarm/state.py` `write_state` (tmp + `os.replace`); bounded-counter idiom → `pr_submit/fsm.py::should_halt_rounds`. Spec §10 says `os.rename`; code uses `os.replace` — align wording. [CODE-CONTRADICTED at `:2269`] |
| 12 | **Two-phase append-only ledger concurrency model.** §10 needs `O_APPEND` + per-PR `flock` for intent/outcome records; only **whole-file** atomic-replace precedent exists (`install_hooks.py:443`, `swarm/state.py`, `recommend/cache.py`). No `fcntl.flock` in any Python module — only bash freshness hooks, which **fail-open**. | Engineering | Build (H1) | 🟡 Researching | H1's push serializer must **fail-closed** (invert the bash hooks' fail-open). Budget the append-only ledger as greenfield borrowing only the atomicity idiom. [CODE-VERIFIED] |
| 13 | **Optional `offer-pr-review.sh` hook touchpoint.** Could surface the mention-trigger path, but the distributable `src/superclaude/hooks/hooks.json` lacks the registration (SoT drift); it is registered only project-local in `.claude/settings.json`. | Eng (optional) | Backlog | 🟡 Researching | Low priority; do not depend on it being distributed until the hooks.json drift is reconciled. |

---

## 21. Implementation Plan

### 21.1 Epics, Features & Stories

> **Format:** Each epic contains user stories in the format "As a [persona], I want [goal] so that [benefit]". Personas: **Maintainer/On-call Reviewer** (the human who replies `@bot fix`), **Authorized Collaborator** (write-permission replier = the sole action authority), **Operator** (deploys/runs the systemd service), **Security Owner** (accountable for the secret/injection boundary). Components map to the merged-requirements inventory: D = Dispatcher, R = Runner, H = Host-side, S = Shared, T = Test.

#### 21.1.1 Epic Summary

| Epic # | Epic Name | Features | Stories | Priority | Phase |
|--------|-----------|----------|---------|----------|-------|
| 1 | Probe-First De-Risking & Test Harness (T1, §21.3) | 2 | 3 | P0 | Phase 1 |
| 2 | Mention Detection, Grammar & Authorization (D3, D4, D5, D6) | 4 | 6 | P0 | Phase 1–2 |
| 3 | Secure Headless Execution — Sandbox, Envelope, Executor (R2, R3, R4) | 3 | 5 | P0 | Phase 2 |
| 4 | Autonomy & Loop-Safety Governance (H1, H2) | 2 | 5 | P0 | Phase 2 |
| 5 | GitHub Write-Back — Push, Reply, Resolve, `--repo` Injector (H3, H4, H5) | 3 | 5 | P0/P1 | Phase 2–3 |
| 6 | Severity-Based Depth Routing (S1) | 1 | 2 | P1 | Phase 2 |
| 7 | Host Platform & Deployment (D1, D2, S2) | 3 | 4 | P0/P1 | Phase 1 & 3 |

---

#### Epic 1: Probe-First De-Risking & Test Harness

**Description:** Lock the unknown GitHub-API and detection constants from a real throwaway-fixture PR **before** any parser/threading code is written, and stand up an adversarial injection corpus as a release gate. This is the §21.3 hard prerequisite — research 02/04/05/06/08 all confirmed (at research time) that reply/resolve threading, `in_reply_to_id`, `databaseId`, and the Augment bot login had **no in-repo precedent**; a reference bash flow has since landed in the untracked parallel V1 `sc-pr-submit-protocol` skill, but the real byte shapes still cannot be safely inferred without the live probe.

**US-1.1: Lock detection constants from a live probe PR**

- **As a** Maintainer
- **I want** the bot's detection constants (`in_reply_to_id` shape, `databaseId` pagination, `resolveReviewThread` GraphQL shape, Augment bot login) captured from a real throwaway PR and committed as config/fixtures
- **So that** the parser and thread-resolver are built against real bytes, not guesses, and cannot resolve the wrong thread (INV-010)

**Acceptance Criteria:**

- ✅ A throwaway-fixture PR run captures every reply/resolve API shape into committed constants/fixtures (mirrors V1's `DetectionContractLocked` "locked-contract" vessel)
- ✅ No H4 (reply/resolve) or D6 (parent resolution) parser code merges before the probe constants are locked — enforced as a build-sequencing gate
- ✅ Captured Augment bot login is a config constant; a different login is treated as "not detected" (T-211 discipline)

**Success Metrics:**

- Probe completes and locks 100% of the four unknown shapes before parser work begins

---

**US-1.2: Adversarial prompt-injection corpus as a release gate**

- **As a** Security Owner
- **I want** an explicit adversarial injection test suite (hidden `-- Additional instruction --` blocks, `gh issue edit $TOKEN` exfil attempts, white-on-white text, fake "authorized/urgent" framing) run against the Runner envelope
- **So that** "Runner contains injection X" is a release-blocking test, matching the OWASP/CSA recommendation that injection red-teaming be a standard deployment gate

**Acceptance Criteria:**

- ✅ Public PoC payloads (from the "Comment and Control" / Aikido "PromptPwned" corpus) are encoded as test cases
- ✅ A passing injection test asserts the opComment never escapes the DATA envelope and no secret leaves the sandbox
- ✅ The suite is wired as an acceptance gate, not an optional unit test

**Success Metrics:**

- 0 injection payloads escape the envelope; suite blocks release on any escape

---

**US-1.3: Secret-scrape regression test (AC-7)**

- **As a** Security Owner
- **I want** a regression test asserting `GH_TOKEN`, push token, and `ANTHROPIC_*` token values are absent from the Runner's `/proc/<pid>/environ`
- **So that** the Runner secret-isolation invariant (INV-001/SC-7) is mechanically verified, not assumed

**Acceptance Criteria:**

- ✅ Test reads the spawned Runner's environ and asserts `"GH_TOKEN" not in runner_env` and no push/Anthropic-auth token values present
- ✅ Test fails today against the unmodified `build_env()` additive-merge path (proving it is load-bearing)

**Success Metrics:**

- Secret-scrape test green only after the allowlist/sandbox-environ mechanism is in place

---

#### Epic 2: Mention Detection, Grammar & Authorization

**Description:** The trigger pipeline — poll GitHub for `@bot` mention replies (rate-limit-aware), parse the whitelisted flag grammar, run a **live per-trigger authorization gate on the replier**, and resolve the parent comment as the `opComment`. The replier is the sole authority; the parent author supplies only data.

**US-2.1: Rate-limit-aware mention polling (D3)**

- **As an** Operator
- **I want** the Dispatcher to poll GitHub for new `@bot` mention replies using ETag/`If-None-Match` 304 conditional requests, `since=` cursors, and `X-RateLimit`/`Retry-After` backoff, at a ≥30s floor
- **So that** the bot detects triggers promptly without exhausting the API rate limit

**Acceptance Criteria:**

- ✅ Conditional requests return 304 when nothing changed (no quota burn on idle polls)
- ✅ Poll interval is enforced at a ≥30s minimum (mirrors V1 `MIN_POLL_INTERVAL=30`)
- ✅ `Retry-After`/`X-RateLimit-Remaining` headers drive backoff
- ✅ Dual-shape login parsing handled (`{"author":{"login"}}` vs `{"user":{"login"}}` — reuse `pr_submit/classifier._login_of`, already tested)

**Success Metrics:**

- Idle polling consumes 0 rate-limit quota via 304s; trigger detected within one poll interval

---

**US-2.2: Whitelisted mention grammar (D4)**

- **As an** Authorized Collaborator
- **I want** to control the bot with a tiny whitelisted comment grammar — autonomy level (`propose|patch|fix|push|resolve`), `--depth`, `--scope`, `--rounds` — defaulting to `propose` when no level is given
- **So that** I have a simple, predictable control surface with the safest possible default

**Acceptance Criteria:**

- ✅ Only whitelisted tokens are parsed; unknown tokens are ignored or rejected, never executed
- ✅ A mention with no autonomy flag resolves to `propose` (safest)
- ✅ Grammar parsing is independent of the untrusted parent-comment body

**Success Metrics:**

- 100% of no-flag mentions default to `propose`; 0 non-whitelisted tokens reach execution

---

**US-2.3: Live authorization gate on the replier (D5)**

- **As a** Maintainer
- **I want** the bot to check the *replier's* live collaborator permission (`collaborators/{login}/permission`) at trigger time and reject-by-default anyone without write access
- **So that** only authorized humans can cause action, and a `read`-permission user gets a polite ack-reject with zero action (AC-1)

**Acceptance Criteria:**

- ✅ The replier (not the parent author) is the sole action authority
- ✅ A `read`-permission mention produces an ack-reject comment and performs no file write, push, or resolve
- ✅ Authorization is evaluated **outside** the LLM, on the Dispatcher (external-policy enforcement, per OWASP/CSA)
- ✅ Unknown/unfetchable permission → safe default (reject)

**Success Metrics:**

- 0 actions taken on behalf of non-write-permission users across the test corpus

---

**US-2.4: Parent comment resolution as opComment (D6)**

- **As a** Maintainer
- **I want** the bot to resolve the parent review comment (via `in_reply_to_id`) and treat its body as the `opComment` data input
- **So that** the issue flagged in the original review comment is what gets remediated

**Acceptance Criteria:**

- ✅ Parent resolution uses the probe-locked `in_reply_to_id` shape (US-1.1)
- ✅ The resolved `opComment` is carried as DATA only, never as instructions
- ✅ Resolution failure halts the trigger with an explanatory reply rather than guessing

**Success Metrics:**

- Correct parent resolved for 100% of probe-fixture trigger shapes

---

**US-2.5: At-most-once trigger claiming**

- **As an** Operator
- **I want** each detected trigger claimed in the on-disk ledger before dispatch, keyed on `(trigger_comment_id, parsed_flag_hash)`
- **So that** a restart or overlapping poll never double-executes the same mention

**Acceptance Criteria:**

- ✅ A trigger already claimed in the ledger is skipped (idempotency)
- ✅ Claim is written atomically before any Runner is dispatched
- ✅ Claim key is distinct from the cross-round content-dedup `fix_key=sha256(path+line+body)`

**Success Metrics:**

- 0 double-executions across simulated restart/overlap tests

---

**US-2.6: Conservative intent handling (competitive wedge)**

- **As a** Maintainer
- **I want** the bot to never take a consequential action on an ambiguous or "don't do anything" mention
- **So that** it avoids the market leader's #1 documented complaint (GitHub Copilot Coding Agent unconditionally opens a child PR even when told not to — Community Discussion #190027)

**Acceptance Criteria:**

- ✅ Default `propose` + authorization gate together constitute the "middle ground / confirmation step" users request
- ✅ No path reaches `push`/`resolve` without an explicit flag AND write permission AND passing validation

**Success Metrics:**

- 0 unsolicited child-PR / push actions on no-op or question-only mentions

---

#### Epic 3: Secure Headless Execution — Sandbox, Envelope, Executor

**Description:** The reasoning layer. An ephemeral, sandboxed, disposable per-trigger Runner checks out PR-head, runs `claude -p` against a CONTROL/DATA envelope (opComment as JSON DATA via stdin), and emits a diff (propose) or sandbox-branch commit (fix). This is the CSA-prescribed "reasoning layer that holds no credentials" half of the split.

**US-3.1: opComment-as-DATA envelope (R3, SC-2/AC-3)**

- **As a** Security Owner
- **I want** the parent comment delivered to `claude -p` inside a JSON CONTROL/DATA envelope on stdin — **never** shell-interpolated as `/sc:troubleshoot "${opComment}"`
- **So that** attacker-controlled comment text cannot be executed as instructions (the seed-brief's literal interpolation is explicitly superseded by §6)

**Acceptance Criteria:**

- ✅ opComment is JSON-encoded as DATA and delivered via stdin (leveraging `ClaudeProcess` stdin delivery — chunked 64 KiB, EINTR-retry, 16 MiB `PROMPT_MAX_BYTES` guard — [CODE-VERIFIED at `process.py:221-258`])
- ✅ No code path interpolates opComment into an argv or shell string
- ✅ Over-large opComment raises the typed `PromptTooLargeForArgv` before spawn (used for SC-2 length-capping)

**Success Metrics:**

- 0 injection escapes from the DATA boundary (gated by US-1.2)

---

**US-3.2: Credential-free sandboxed Runner (R4, INV-001/INV-015)**

- **As a** Security Owner
- **I want** the Runner to execute in an ephemeral sandbox with a minimal environment (no host home mount, no `~/.aienv` secrets, no `GH_TOKEN`/push token), `cwd` = the disposable PR-head checkout, and deny-by-default egress allowlisting only `:4000/cli` (Anthropic proxy) + `api.github.com` + the single-repo git endpoint
- **So that** even a successful injection cannot exfiltrate secrets or reach the network broadly (blast-radius minimization)

**Acceptance Criteria:**

- ✅ Runner env contains no push/Anthropic-auth token values (AC-7, verified by US-1.3)
- ✅ Runner `cwd` is the PR-head checkout — note `ClaudeProcess` has **no `cwd` parameter** today ([CODE-CONTRADICTED at `process.py:192`]); resolved by a new `cwd` kwarg or a Runner-side `os.chdir()` (TDD)
- ✅ Egress is deny-by-default with the §6 allowlist; the Anthropic proxy host must be reachable from the chosen sandbox topology (OD-1)
- ✅ Runner only edits files inside the sandbox workspace (write-scope confinement; mechanism ports from `roadmap/remediate_executor.py::enforce_allowlist`, policy widens from named files to "inside the sandbox")
- ✅ `--dangerously-skip-permissions` (the `ClaudeProcess` default, [CODE-VERIFIED at `process.py:93`]) is safe **only because** of the sandbox boundary — the safety is in the sandbox, not the flag

**Success Metrics:**

- Secret-scrape (US-1.3) green; 0 writes outside the workspace; egress blocked to all non-allowlisted hosts

---

**US-3.3: Headless remediation executor (R2)**

- **As a** Maintainer
- **I want** the Runner to spawn `claude -p` via the `ClaudeProcess` primitive with caller-set `max_turns` per autonomy level (≈30 propose / ≈60 fix), `output_format="stream-json"`, and process-group kill on teardown
- **So that** the remediation runs headlessly, streams progress, and is cleanly killable / timeout-bounded

**Acceptance Criteria:**

- ✅ Executor wraps `ClaudeProcess` ([CODE-VERIFIED at `process.py:72`; `build_command()` flag string verified at `:121-143`]); `roadmap/remediate_executor.py` (which already runs `ClaudeProcess` for remediation with snapshot/rollback/retry/diff-size guards) is the primary executor reuse reference
- ✅ `max_turns` is passed explicitly per level (default 100 is too high for propose — caller must override)
- ✅ Process-group kill (`os.setpgrp` → `os.killpg`) and `timeout_seconds`→124 are honoured for sandbox teardown / `StuckRun` alerting
- ✅ Lifecycle hooks (`on_spawn`/`on_signal`/`on_exit`) feed the §14 audit events

**Success Metrics:**

- Runner spawns, streams, and tears down cleanly; stuck runs alert at `timeout_seconds`

---

**US-3.4: Validation before any commit/diff**

- **As a** Maintainer
- **I want** the Runner to validate its own change (tests/coherence) and emit a diff (propose/patch) or sandbox-branch commit (fix) only when validation passes
- **So that** a failed remediation never advances toward push

**Acceptance Criteria:**

- ✅ Validation-fail short-circuits before push (push-decision predicate 2, reused from `fsm.evaluate_push_decision`)
- ✅ Propose/patch emit a patch bundle; fix emits a sandbox-branch commit (no host-side push from the Runner)

**Success Metrics:**

- 0 pushes proceed on validation failure

---

**US-3.5: Snapshot / rollback discipline**

- **As a** Maintainer
- **I want** per-file snapshot + rollback around Runner edits
- **So that** a partial or incoherent remediation can be reverted within the sandbox

**Acceptance Criteria:**

- ✅ Snapshot/restore reuse the atomic read→tmp→`os.replace` discipline (`roadmap/remediate_executor.py` `create_snapshots`/`restore_from_snapshots`)
- ✅ Cross-file coherence checked before emitting the change

**Success Metrics:**

- Incoherent multi-file fixes rolled back, not emitted

---

#### Epic 4: Autonomy & Loop-Safety Governance

**Description:** The execution-layer policy. A two-phase intent/outcome ledger and an autonomy gate that caps effective autonomy at the lattice-min and HALTs on off-lattice conditions (`needs_human_decision`, exhausted push budget).

**US-4.1: Effective-autonomy lattice cap (H2, §8)**

- **As a** Security Owner
- **I want** effective autonomy computed as the minimum over the lattice of {requested flag, authorization projection, validation status}, then short-circuited to HALT on off-lattice conditions
- **So that** the bot can never act above the most restrictive applicable ceiling

**Acceptance Criteria:**

- ✅ Effective level = `min` over the lattice; e.g. a `push`-flag from a write-collaborator whose validation failed cannot reach push
- ✅ Reuses/extends V1 `fsm.evaluate_push_decision` (5-predicate G-push conjunction, tested) — predicates 2–5 (validated / no-human-decision / under-budget / real-work) carry over verbatim; predicate 1 (`monitor_ordinal>=3`) drops out under the mention-triggered model; a new authorization-projection predicate is added
- ✅ Structurally impossible to construct a push for a `needs_human_decision` item (subject to Open Question #8 — the populator)

**Success Metrics:**

- 0 actions above the computed effective ceiling

---

**US-4.2: `needs_human_decision` HALT (inherited V1.0 FR-4.4)**

- **As a** Maintainer
- **I want** any item classified `needs_human_decision` to HALT and post a PENDING reply — even at the top autonomy level — never auto-applying a default
- **So that** ambiguous-intent / security-trade-off / API-contract / multiple-valid-fix items are escalated to a human, not shipped

**Acceptance Criteria:**

- ✅ HALT short-circuits before push regardless of requested level (the flag is consumed in `pr_submit/fsm.py` pre-gate at `:204`/`:353` and push predicate 3 at `:158`)
- ✅ A deterministic populator sets the flag, OR the agent-self-report dependency is explicitly documented (Open Question #8)

**Success Metrics:**

- 100% of `needs_human_decision` items HALT to PENDING; 0 auto-applied

---

**US-4.3: Per-PR push budget with SHA-correlation (H1, §9)**

- **As a** Maintainer
- **I want** a per-PR push budget (default 2, cap 5) where a re-review counts as the next round **only if** the PR head SHA equals the bot's recorded push SHA
- **So that** the bot cannot enter an infinite remediation loop

**Acceptance Criteria:**

- ✅ Monotonic budget counter with `>=` fence-post (reuse `fsm.should_halt_rounds` semantics, not swarm `:2269`)
- ✅ Round increments only on exact SHA-match between re-review and recorded push
- ✅ Budget exhaustion posts a cap-summary and stops

**Success Metrics:**

- 0 unbounded loops; budget enforced across SHA-correlation tests

---

**US-4.4: Two-phase intent/outcome ledger (H1, §10)**

- **As an** Operator
- **I want** a durable, disk-authoritative, restart-surviving ledger that writes an intent record before each consequential action and an outcome record after
- **So that** a crash mid-action is recovered as RESUME (re-verify), never as silent re-execute

**Acceptance Criteria:**

- ✅ Atomic writes via tmp + `os.replace` (idiom from `swarm/state.py` / `recommend/cache.py` / `install_hooks.py:443`); append-only JSONL via `O_APPEND`
- ✅ Per-PR `flock` serializes tree mutations and **fails-closed** (inverting the fail-open bash freshness hooks)
- ✅ Intent-without-matching-outcome on startup ⇒ RESUME/re-verify path; the ledger is SoT and the counter is derived from it on startup (not the reverse)
- ✅ Tolerates a truncated last line on replay

**Success Metrics:**

- 100% of simulated crash windows recover as RESUME; 0 silent re-executions

---

**US-4.5: Tamper-evident audit log (§14)**

- **As a** Security Owner
- **I want** an immutable audit log (distinct from the state ledger) recording every poll, authz check, mention parse, intent, process spawn, validation, push, reply, and round outcome with the exact triggering input
- **So that** every action is traceable for governance/compliance (NIST AI RMF / ISO 42001 evidence)

**Acceptance Criteria:**

- ✅ Closed-enum event taxonomy, started from `pr_submit/models.py::EventType` (~70–80% overlap) and extended with authz/mention/intent/`claude_process_spawn` events; in-session-only events dropped
- ✅ Dual-format jsonl+md writer (idiom from `cli_portify/logging_.py`); logs forwarded/persisted before Runner teardown

**Success Metrics:**

- 100% of consequential actions have a matching audit event with the triggering input

---

#### Epic 5: GitHub Write-Back — Push, Reply, Resolve, `--repo` Injector

**Description:** The credential-holding side-effects, performed host-side by the Dispatcher (never the Runner). Push with a short-lived token, reply to the review thread with a summary + SHA, resolve the thread at the `resolve` level — all through a single `gh` chokepoint that unconditionally pins the fork repo.

**US-5.1: Fork-only `--repo` injector chokepoint (H5, C5/SC-4)**

- **As a** Security Owner
- **I want** every GitHub-mutating call to route through a single `gh_call()` that unconditionally injects `--repo IronbellyOrg/IronClaude`, with no code path able to omit it
- **So that** autonomous pushes/replies can never land on the public upstream (the prose-only discipline that previously misfired)

**Acceptance Criteria:**

- ✅ This is the **first code-level enforcement** of C5 — today `--repo` is enforced only by CLAUDE.md prose ([CODE-VERIFIED: 0 Python `gh` callers in the repo]); the injector is net-new [NEW]
- ✅ A unit test asserts no constructed `gh` argv can lack `--repo IronbellyOrg/IronClaude`
- ✅ Optional CI grep-guard forbids raw `subprocess([... "gh" ...])` outside `gh.py`

**Success Metrics:**

- 0 `gh` invocations without `--repo`; 0 actions on the upstream repo

---

**US-5.2: Host-side push with short-lived token (H3)**

- **As an** Operator
- **I want** the validated change pushed host-side by the Dispatcher using a short-lived, narrowly-scoped token — never from inside the Runner
- **So that** the push capability lives entirely outside the untrusted-text-processing layer (CSA "fundamental mitigation")

**Acceptance Criteria:**

- ✅ Push occurs only after the autonomy gate authorizes it (Epic 4) and validation passed (Epic 3)
- ✅ Token is short-lived/revocable (OD-2); never written into the sandbox
- ✅ Never modifies merge state — strictly no `--approve`/`--request-changes`/merge (inherited from the auggie-review `--comment`-only discipline; §20 "humans merge")

**Success Metrics:**

- 100% of pushes are host-side with a scoped token; 0 merge-state mutations

---

**US-5.3: Reply-to-thread + resolve (H4, §12, INV-010)**

- **As a** Maintainer
- **I want** the bot to reply to the originating review thread with a summary + pushed SHA, and at the `resolve` level resolve the thread via GraphQL `resolveReviewThread` matched on `databaseId`
- **So that** the conversation is closed on the exact thread that triggered it, with no mis-resolution

**Acceptance Criteria:**

- ✅ Reply uses the `pulls/<N>/comments/<parent_id>/replies` endpoint (templated from auggie-review's posting precedent; reply/resolve are net-new in Python — a reference bash flow exists in the untracked parallel V1 `sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`, but no committed/tracked Python caller exists) [NEW]
- ✅ Resolve matches the correct thread by `databaseId` (probe-locked shapes from US-1.1); never resolves a sibling thread (INV-010)
- ✅ Resolve only at the `resolve` autonomy level

**Success Metrics:**

- 100% correct-thread resolves on probe fixtures; 0 mis-resolutions

---

**US-5.4: Summary reply with provenance**

- **As a** Maintainer
- **I want** each bot reply to carry clear AI provenance and the pushed SHA
- **So that** reviewers can trace what the bot did and why (market demand for source traceability)

**Acceptance Criteria:**

- ✅ Reply includes pushed SHA, autonomy level used, and AI provenance marker
- ✅ Provenance is explicit (not a silent commit)

**Success Metrics:**

- 100% of bot replies carry SHA + provenance

---

**US-5.5: Ack-reject reply for unauthorized triggers**

- **As an** Authorized Collaborator
- **I want** a polite ack-reject reply when a non-write-permission user mentions the bot
- **So that** unauthorized users get clear feedback while zero action is taken (AC-1)

**Acceptance Criteria:**

- ✅ Ack-reject posts a comment and performs no file write / push / resolve
- ✅ The event is audit-logged

**Success Metrics:**

- 100% of unauthorized mentions get an ack-reject with 0 side-effects

---

#### Epic 6: Severity-Based Depth Routing

**Description:** Re-grade each finding through the auggie-review severity rubric and route remediation depth accordingly — Augment severity is a hint, not authoritative.

**US-6.1: Severity-to-depth routing (S1, §17)**

- **As a** Maintainer
- **I want** each finding re-graded via the severity rubric and routed by tier — Critical/High → `--depth deep --fix`, Medium → `--fix`, Low/Nit → report-only, unknown → Medium fail-safe
- **So that** remediation effort matches the real severity, not the raw Augment hint

**Acceptance Criteria:**

- ✅ Routing reuses `pr_submit/severity_router.remap_severity()` + `route()` **by import** ([CODE-VERIFIED]: pure, encodes the rubric's category floor/ceiling table, never emits the `--depth quick --fix` conflict) rather than re-parsing `severity-rubric.md`
- ✅ Augment `severity_hint` is treated as a starting point and remapped (the rubric's own stated contract)
- ✅ Unknown severity defaults to Medium (fail-safe)

**Success Metrics:**

- 100% of findings routed by remapped (not raw) severity; 0 depth/flag conflicts

---

**US-6.2: No merge-state changes from severity verdicts**

- **As a** Security Owner
- **I want** severity verdicts to never translate into `gh pr review --approve`/`--request-changes`
- **So that** merge decisions remain with humans (a code-enforced cultural invariant the rubric already states)

**Acceptance Criteria:**

- ✅ No severity tier maps to a merge-state mutation

**Success Metrics:**

- 0 approve/request-changes actions

---

#### Epic 7: Host Platform & Deployment

**Description:** The operational shell — a `superclaude remediate` CLI group, a long-lived supervised Dispatcher daemon, and the systemd + sandbox-image deploy story. Entirely greenfield (no `deploy/` dir, no service/long-lived-daemon precedent in the repo).

**US-7.1: `superclaude remediate` CLI group (D1)**

- **As an** Operator
- **I want** the bot delivered as a `superclaude remediate` CLI group (not a skill), mirroring sprint/swarm/pipeline
- **So that** it runs headless outside any Claude session and composes with existing tooling

**Acceptance Criteria:**

- ✅ `remediate_group` registered in `cli/main.py` via the deferred-import + `main.add_command(remediate_group, name="remediate")` idiom with the mandatory `# noqa: E402,I001` annotation ([CODE-VERIFIED convention at `main.py:400-438`]) — omitting it ships a dead command (Open Question #10)
- ✅ Package decomposed under `cli/remediate/` (structural template: `swarm/`, `prd/`); test home `tests/cli/remediate/`
- ✅ The empty stale `remediation/` dir is removed/ignored (Open Question #9)

**Success Metrics:**

- `superclaude remediate` is discoverable and runnable; registration test green

---

**US-7.2: Supervised Dispatcher daemon (D2)**

- **As an** Operator
- **I want** a long-lived Dispatcher that runs the poll → detect → authz → claim → dispatch loop under supervision (watchdog, rate-limit awareness, restart)
- **So that** the bot survives crashes and runs 24/7 (the core reason V2 exists vs V1's in-session host)

**Acceptance Criteria:**

- ✅ Dispatcher composes D3/D4/D5/D6 + H1/H2 into a supervised loop (new operational shape — no `Restart=always`/`sd_notify` precedent in the repo; warrants a spike)
- ✅ Counter/state derived from the ledger (SoT) on startup, surviving restart

**Success Metrics:**

- Daemon recovers from kill/restart with no lost or double-processed triggers

---

**US-7.3: systemd deploy + sandbox image (S2)**

- **As an** Operator
- **I want** systemd unit(s) + a non-root sandbox image under `deploy/remediate-bot/`, with secrets sourced via `EnvironmentFile=` (chmod-600, owner-scoped) and hardening (`NoNewPrivileges`, `WatchdogSec`)
- **So that** the bot deploys as a hardened on-prem service

**Acceptance Criteria:**

- ✅ `deploy/` tree is net-new [NEW] (0 `.service`/`WatchdogSec`/`EnvironmentFile=`/`NoNewPrivileges` in the repo today)
- ✅ Secret files are chmod-600 (note: the `~/.aienv` cited exemplar is **644 on disk** — [CODE-CONTRADICTED]; cite the chmod-600 `EnvironmentFile=` requirement on its own merits / as a content-sourcing model only)
- ✅ Sandbox image is non-root with deny-by-default egress (depends on OD-1)

**Success Metrics:**

- Service starts under systemd, survives reboot, secrets not world-readable

---

**US-7.4: Latency & cost targets**

- **As an** Operator
- **I want** explicit latency/cost targets — trigger-to-action within the poll interval, large-diff handling via compression/chunking
- **So that** the bot is competitive with the established bar (PR-Agent "~30s single call"; Copilot criticized for 90s+ cold-start)

**Acceptance Criteria:**

- ✅ Trigger detected within one ≥30s poll interval; Dispatcher is daemon-resident (warm) while Runners are ephemeral
- ✅ Large diffs handled as a first-class concern (compression/chunking), within the 16 MiB stdin budget

**Success Metrics:**

- p95 trigger-to-Runner-spawn within one poll interval; large-diff triggers complete without prompt-size failure

---

### 21.2 Product Requirements

#### 21.2.1 Core Features

> Each feature maps to merged-requirements components. **Reuse anchors** carry [CODE-VERIFIED] provenance; everything else is greenfield [NEW]. Priority uses MoSCoW: P0 = Must Have, P1 = Should Have, P2 = Could Have.

##### Feature 1: Split-Host Architecture (Dispatcher + ephemeral Runner)

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Component(s)** | D2 (Dispatcher daemon), R1–R4 (Runner) |
| **Description** | A long-lived credential-holding Dispatcher (systemd daemon) splits from an ephemeral, sandboxed, tokenless per-trigger Runner (`claude -p`). The Dispatcher reasons over policy and holds secrets; the Runner reasons over untrusted text and holds none. |
| **User Value** | Even a successful prompt injection in the Runner cannot exfiltrate secrets or push code — the exact "fundamental mitigation" CSA Labs prescribes (reasoning layer / credential-holding execution layer separation). |
| **Dependencies** | `ClaudeProcess` [CODE-VERIFIED `process.py:72`]; OD-1 (sandbox tech); secret-isolation mechanism (Open Question #1). |

**Acceptance Criteria:**

- Runner holds no `GH_TOKEN`/push token/`ANTHROPIC_*` (AC-7, verified by secret-scrape test US-1.3)
- Dispatcher performs all GitHub I/O and policy; Runner performs only reasoning + sandboxed edits
- Runner is disposable per trigger (no state carried between triggers)

**Success Metrics:** 0 secrets in Runner environ; 0 pushes originating inside the Runner.

---

##### Feature 2: Mention-Triggered Authorization Pipeline

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Component(s)** | D3 (ingest), D4 (grammar), D5 (authz), D6 (parent resolution) |
| **Description** | Rate-limit-aware polling detects `@bot` mention replies; a whitelisted flag grammar is parsed; a live collaborator-permission gate on the *replier* (reject-by-default) authorizes; the parent comment is resolved as the `opComment`. |
| **User Value** | Only authorized humans cause action; the replier is the sole authority and the parent author supplies only data — directly answering Copilot's #1 complaint (unconditional trigger / ignored intent). |
| **Dependencies** | ETag/304 polling [NEW]; `collaborators/{login}/permission` authz [NEW]; `in_reply_to_id` parent resolution [NEW, probe-locked]; `classifier._login_of` dual-shape parser (reuse). |

**Acceptance Criteria:**

- `read`-permission mention → ack-reject, zero action (AC-1)
- No-flag mention defaults to `propose`
- Idle polling consumes 0 rate-limit quota via 304s; poll floor ≥30s
- Unknown permission → safe default (reject)

**Success Metrics:** 0 actions for non-write users; 100% no-flag defaults to propose.

---

##### Feature 3: Prompt-Injection-Contained Execution Envelope

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Component(s)** | R3 (envelope), R2 (executor) |
| **Description** | The opComment is delivered to `claude -p` as JSON DATA inside a CONTROL/DATA envelope via stdin — never shell-interpolated. Backed by `ClaudeProcess` stdin delivery + 16 MiB guard. |
| **User Value** | Attacker-controlled comment text cannot be executed as instructions — neutralizes the "Comment and Control" CVE class (Claude Code/Gemini/Copilot all leaked secrets via comment injection in 2026). |
| **Dependencies** | `ClaudeProcess` stdin delivery [CODE-VERIFIED `process.py:221-258`]; supersedes seed-brief's `"${opComment}"` interpolation (§6). |

**Acceptance Criteria:**

- opComment JSON-encoded as DATA, delivered via stdin; never in argv/shell
- Over-large opComment raises `PromptTooLargeForArgv` before spawn (SC-2 capping)
- Adversarial injection corpus (US-1.2) passes as a release gate

**Success Metrics:** 0 injection escapes from the DATA boundary.

---

##### Feature 4: Autonomy Lattice & needs_human_decision HALT

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Component(s)** | H2 (autonomy gate) |
| **Description** | Effective autonomy = min over the lattice {flag, authorization-projection, validation}, with off-lattice HALT short-circuits (`needs_human_decision`, exhausted budget). Lattice: `propose < patch < fix < push < resolve`, default `propose`. |
| **User Value** | The bot can never act above the most restrictive applicable ceiling, and escalates genuinely ambiguous/high-stakes items to a human instead of shipping a default. |
| **Dependencies** | Extends V1 `fsm.evaluate_push_decision` (5-predicate conjunction, tested) — predicates 2–5 carry over, predicate 1 drops, authz-projection predicate added; `needs_human_decision` populator (Open Question #8). |

**Acceptance Criteria:**

- Effective level = lattice-min; structurally impossible to exceed it
- `needs_human_decision` item HALTs to PENDING even at top level; never auto-applied
- A deterministic populator sets the flag, or the agent-self-report dependency is documented

**Success Metrics:** 0 actions above effective ceiling; 100% of HALT items escalated.

---

##### Feature 5: Loop-Safe Two-Phase Ledger & Push Budget

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Component(s)** | H1 (ledger) |
| **Description** | Durable, disk-authoritative, restart-surviving ledger: intent record before each consequential action, outcome record after; per-PR push budget (default 2, cap 5) with exact-SHA round correlation; per-PR fail-closed `flock`. |
| **User Value** | No infinite remediation loops; a crash mid-action recovers as RESUME (re-verify), never silent re-execute; at-most-once trigger claiming across restarts. |
| **Dependencies** | Atomic-write idiom (reuse `swarm/state.py`/`recommend/cache.py`/`install_hooks.py:443`); counter semantics `fsm.should_halt_rounds` (NOT swarm `:2269`); append-only `O_APPEND`+`flock` [NEW]. |

**Acceptance Criteria:**

- tmp+`os.replace` atomic writes; `O_APPEND` JSONL; per-PR `flock` fails-closed
- Round increments only on exact head-SHA == recorded-push-SHA match
- Intent-without-outcome on startup ⇒ RESUME; ledger is SoT for the counter
- Budget exhaustion posts a cap-summary and stops

**Success Metrics:** 0 unbounded loops; 0 double-executions; 100% crash-window RESUME.

---

##### Feature 6: GitHub Write-Back with Fork-Only `--repo` Chokepoint

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Component(s)** | H3 (push), H4 (reply/resolve), H5 (gh wrapper) |
| **Description** | Host-side push with a short-lived scoped token; reply-to-thread with summary + SHA; GraphQL `resolveReviewThread` (databaseId-matched) at `resolve` level; every `gh` call routed through a single `gh_call()` that unconditionally injects `--repo IronbellyOrg/IronClaude`. Never modifies merge state. |
| **User Value** | Autonomous writes can never land on the public upstream; threads close on the exact triggering thread; merge decisions stay with humans. |
| **Dependencies** | First Python `gh` caller in the repo [CODE-VERIFIED 0 existing Python callers]; reply/resolve net-new in Python (reference bash flow now in untracked `sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`); posting template from auggie-review SKILL; OD-2 (token). |

**Acceptance Criteria:**

- No constructed `gh` argv can omit `--repo IronbellyOrg/IronClaude` (unit-tested)
- Push host-side only, after authz + validation; token never in the sandbox
- Resolve matches correct thread by `databaseId` (probe-locked); never a sibling (INV-010)
- Strictly `--comment`; no `--approve`/`--request-changes`/merge (§20)

**Success Metrics:** 0 `gh` calls without `--repo`; 0 mis-resolutions; 0 merge-state mutations.

---

##### Feature 7: Severity-Based Depth Routing

| Attribute | Value |
|-----------|-------|
| **Priority** | P1 (Should Have) |
| **Component(s)** | S1 |
| **Description** | Each finding is re-graded through the auggie-review severity rubric and routed: Critical/High → `--depth deep --fix`, Medium → `--fix`, Low/Nit → report-only, unknown → Medium fail-safe. |
| **User Value** | Remediation effort matches real severity; Augment's `severity_hint` is treated as a hint, not gospel. |
| **Dependencies** | Reuse-by-import `pr_submit/severity_router.remap_severity()`+`route()` [CODE-VERIFIED, pure, rubric-faithful]. |

**Acceptance Criteria:**

- Routing uses the imported router, not a re-parse of `severity-rubric.md`
- Unknown severity defaults to Medium
- Never emits the `--depth quick --fix` conflict

**Success Metrics:** 100% routed by remapped severity; 0 depth/flag conflicts.

---

##### Feature 8: Hardened systemd Deployment

| Attribute | Value |
|-----------|-------|
| **Priority** | P1 (Should Have) |
| **Component(s)** | D1 (CLI group), S2 (deploy) |
| **Description** | `superclaude remediate` CLI group + systemd unit(s) + non-root sandbox image under `deploy/remediate-bot/`, secrets via `EnvironmentFile=` (chmod-600), hardened with `NoNewPrivileges`/`WatchdogSec`. |
| **User Value** | A hardened, restart-surviving on-prem service — the textbook hardened-self-hosted-runner pattern (GitHub docs / StepSecurity / AWS / Sysdig). |
| **Dependencies** | `main.py` registration with `# noqa: E402,I001` [CODE-VERIFIED convention `main.py:400-438`]; `deploy/` tree net-new [NEW]; OD-1. |

**Acceptance Criteria:**

- `remediate_group` registered with `name="remediate"`; `superclaude remediate` discoverable
- Secret files chmod-600 (do not rely on the 644 `~/.aienv` as the exemplar)
- Service survives reboot

**Success Metrics:** registration test green; service restarts cleanly; secrets not world-readable.

---

#### 21.2.2 Feature Prioritization Matrix

> **Framework:** RICE — (Reach × Impact × Confidence) / Effort. Reach = relative share of triggers/operators touched (1–10). Impact = 3 (massive) / 2 (high) / 1 (medium). Confidence = % (driven by code-verified reuse vs greenfield/probe-dependent surfaces). Effort = person-weeks (greenfield surfaces with no prior art cost more; reuse-by-import costs less).

| Feature | Reach | Impact | Confidence | Effort (pw) | RICE Score | Priority |
|---------|-------|--------|------------|-------------|------------|----------|
| F3 Injection-contained envelope | 10 | 3 | 90% (ClaudeProcess stdin [CODE-VERIFIED]) | 2 | 13.5 | P0 |
| F4 Autonomy lattice & HALT | 10 | 3 | 80% (extends tested `fsm`; populator open) | 3 | 8.0 | P0 |
| F7 Severity depth routing | 8 | 2 | 95% (reuse-by-import [CODE-VERIFIED]) | 1 | 15.2 | P1 |
| F2 Mention authz pipeline | 10 | 3 | 60% (ETag/authz/parent all [NEW], probe-dependent) | 5 | 3.6 | P0 |
| F1 Split-host architecture | 10 | 3 | 70% (env-isolation mechanism open #1; OD-1) | 4 | 5.25 | P0 |
| F5 Loop-safe ledger & budget | 9 | 3 | 70% (atomicity idiom reuse; append/flock [NEW]) | 4 | 4.7 | P0 |
| F6 Write-back + `--repo` chokepoint | 9 | 3 | 50% (first Python `gh`; reply/resolve [NEW], probe-gated) | 5 | 2.7 | P0 |
| F8 Hardened systemd deploy | 6 | 2 | 55% (registration verified; sandbox/deploy [NEW], OD-1) | 5 | 1.3 | P1 |

**RICE Formula:** (Reach × Impact × Confidence) / Effort. Lower-confidence/higher-effort scores (F6, F8, F2) concentrate on the greenfield GitHub-I/O + sandbox/deploy surfaces with no in-repo prior art — consistent with the build-accounting finding that the Dispatcher half is the cost/risk center while the decision core is largely reusable.

---

#### 21.2.3 Competitive Feature Comparison Matrix

> Evidence-based (web research 01–03). **Our Product** = PR Auto-Remediation V2.0 (target capability, [NEW]). Legend: ✅ Full · ⚠️ Partial/Limited · ❌ Not supported.

| Feature | Our Product (V2.0) | GitHub Copilot Coding Agent | Claude Code GitHub Action (`@claude`) | Devin | CodeRabbit / PR-Agent |
|---------|--------------------|-----------------------------|---------------------------------------|-------|------------------------|
| Mention-triggered (`@bot`) | ✅ | ✅ | ✅ | ⚠️ (PR-event) | ✅ |
| Implements fixes (writes commits) | ✅ | ✅ | ✅ | ✅ | ⚠️ (mostly review/suggest) |
| On-prem / self-hosted | ✅ | ❌ (GitHub-Actions cloud) | ❌ (GitHub-Actions cloud) | ❌ (SaaS) | ⚠️ (some self-host) |
| Propose-only default | ✅ | ⚠️ (draft PR, but over-triggers) | ⚠️ | ✅ (human-in-loop) | ✅ |
| Live per-trigger authorization gate | ✅ | ⚠️ (org policy enable) | ❌ (workflow `if` convention) | ⚠️ | ❌ |
| opComment as untrusted DATA envelope | ✅ | ❌ (leaked secrets via comment injection, 2026) | ❌ (same CVE class) | ⚠️ | ❌ |
| Runner holds no push/secret token | ✅ | ❌ (`pull_request_target` injects secrets) | ❌ | ⚠️ | ❌ |
| Tamper-evident audit/trigger ledger | ✅ | ⚠️ | ⚠️ | ⚠️ | ❌ |
| Sidesteps GitHub-Actions supply-chain surface | ✅ | ❌ | ❌ | n/a | ⚠️ |

**Positioning Statement:** For maintainers on regulated/air-gapped forks who need autonomous PR remediation but cannot send code to cloud runners, PR Auto-Remediation V2.0 is an on-prem, mention-triggered remediation bot that treats the triggering comment as untrusted data inside a credential-free sandbox. Unlike GitHub Copilot Coding Agent (cloud-only, over-triggers, secrets in the runner) and the public `@claude` action (cloud Actions, no live authz), our split Dispatcher/Runner design holds the only differentiated position at the **on-prem × mention-triggered-remediation** intersection — a gap no incumbent occupies.

---
