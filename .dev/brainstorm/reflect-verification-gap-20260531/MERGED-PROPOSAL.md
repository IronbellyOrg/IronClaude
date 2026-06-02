<!-- Provenance: This document was produced by /sc:adversarial via /sc:brainstorm -->
<!-- Base: Proposal A (OVM) -->
<!-- Merge date: 2026-05-31T03:55:00Z -->
<!-- Non-base sources incorporated: Proposal B (OVL) for changes INC-01 through INC-09 -->

# Merged Proposal — Outcome-Verification Manifest with Seat-Tagged Claims (OVM)

> **Provenance**: Adversarial merge of Proposal A (OVM, base) and Proposal B (OVL,
> incorporated) per `/config/.claude/skills/sc-adversarial-protocol/SKILL.md`.
> Debate completed at Round 2.5 with convergence 0.91 (21 of 23 diff points
> resolved). 14 changes applied: 9 incorporations from Proposal B + 5
> mechanism-text additions driven by Round 2.5 invariant-probe warnings.
> Base author: Brainstorm Agent A. Non-base author: Brainstorm Agent B. Merge
> date: 2026-05-31. Downstream consumer: `task-builder` (this document is the
> BUILD_REQUEST).

> **Unresolved conflicts register.** Two shared assumptions remain
> unresolved by formulation but not by content. Both are surfaced explicitly
> in §5 (trade-offs and risks) per Changes 13 and 14:
>
> - **A-001**: WebFetch/WebSearch can be added to allowed-tools (see §5).
> - **A-002**: Operator / CI executes deferred runbooks (see §5).
>
> Downstream `task-builder` should decide whether each warrants a corresponding
> follow-up task. No other unresolved conflicts.

<!-- Source: Base (original) — author preamble retained from Proposal A -->

> **Author:** Brainstorm Agent A (base) + Brainstorm Agent B (incorporations via merge)
> **Date:** 2026-05-31
> **Framing:** Structural fix to the verification-gap class exemplified by the docker-cli
> miss in `sc:reflect`. Pre-merge audit emitted `status: success` for a change that
> shipped a broken `apt-get install --no-install-recommends docker.io` line; the operator
> caught the breakage post-merge with one `which docker`. Root cause was not a missing
> check — it was a missing **contract** distinguishing what the orchestrator verified
> from what it cannot verify from its seat.

---

## 1. Problem framing

<!-- Source: Base (original) -->

`sc:reflect` ships `status: success` when **implementation verification** passes —
"code on disk matches the literal asks in spec and tasklist" — regardless of whether
**outcome verification** ("the change produces its intended behavior in the deployed
system") was performed, deferred, or attempted. Every structural mechanism
(evidence-validator `§11.2`, calibrator `§11.3`, reviewer ensemble `§7.1`, the
9-condition gate `§14.5.2`) is anchored to the first. The docker miss was findable
with one `apt-cache show docker.io`; the protocol never mandated it because the
contract never named "this APT line provides `/usr/bin/docker`" as an assertion
distinct from "diff content matches the tasklist ask." The structural fix is not
"check more things" — it is to make the protocol explicit about which seat each
claim can be verified from, mandate verification from in-repo and external-spec
seats, and emit a machine-readable deferred-verification runbook for runtime and
cross-system seats that downstream automation or a fresh agent can pick up.

---

## 2. Proposed structural fix — Outcome-Verification Manifest (OVM) with seat-tagged claims

<!-- Source: Base (modified) — Change 1: added 5th row (V-Deferred-Logical) per Proposal B §3.1 -->

**Named central idea:** Every audit run produces, in addition to the existing
`deviation-ledger.yaml` (`§10`) and `grounding-gaps.yaml` (`§10.6`), a third
peer-grade artifact — **`outcome-claims.yaml`** — that enumerates the **outcome
claims** the change makes (assertions about behavior, upstream artifacts, runtime
state, or cross-system contracts that go beyond `code == spec`). Each claim is tagged
with one of five **verification modes** (four OVM seats plus a fifth tier-escalation
mode merged in from Proposal B):

| Mode | Definition | Who can verify | Reflect's responsibility |
|------|------------|----------------|--------------------------|
| **`in-repo`** | Verifiable by reading repo files, running diagnostics, or symbol queries | Reflect orchestrator (existing toolkit) | MUST verify; failure → drop the claim and force `status: partial` per `§11.2` semantics |
| **`external-spec`** | Verifiable by querying an upstream artifact: package registry, OS package manager, vendor API docs, OpenAPI schema, source-of-truth changelog | Reflect orchestrator using `WebFetch` / `WebSearch` / `context7` / `tavily` / read-only `Bash` (`apt-cache show`, `pip show`, `npm view`, `gh api`) | MUST verify when claim surfaces; on failure, treat as **Regression** (per `§10.4`) and force escalation per `§5.3` rule 3 |
| **`runtime`** | Verifiable only against the running deployed system (process state, kernel state, network reachability, live load behavior) | Operator (or future runtime-hooked agent) | MUST emit a structured **deferred-verification runbook** with concrete `next_actor`, `next_command`, `success_criterion`, `fail_criterion`; reflect ships `outcome_verification_complete: false` |
| **`cross-system`** | Verifiable only by orchestrating multiple live systems (downstream service load, third-party webhook delivery, distributed-trace propagation) | Operator + named downstream system | Same as `runtime`, with the `next_actor` field naming the specific other system |
| **`V-Deferred-Logical`** | The claim depends on second-order reasoning the audit declines to perform at this tier (e.g., "will this rebuild change the install-list output?"). The reasoning is in-bounds for Tier 2 but skipped at Tier 1. | Not at the current tier; tier-escalation can resolve it. | MUST emit a tier-escalation signal at T1; at T2, becomes a runbook for the operator OR a Wave 6 remediation candidate |

<!-- Source: Base (original) — conflation-recategorization framing retained -->

The conflation is resolved not by recategorizing failure shapes (whack-a-mole) but
by recategorizing **who can answer the verification question**. Any future bug shape
— performance regression, integration drift, OS package split, runtime config
violation, API contract change, logical-fidelity regression — falls under exactly one
of these five modes by its nature. The protocol gains a contractual home for "this
orchestrator from this seat cannot answer this question" that is honest,
machine-readable, and pickup-able.

This is the **`grounding-gaps.yaml` pattern from `§10.6` applied to outcome
verification** — exactly analogous. Grounding-gaps surfaces "evidence insufficient
to classify a deviation"; OVM surfaces "evidence insufficient to verify an
outcome." Both are parallel artifacts with required fields; OVM forces `status:
partial` only when verification *failed*, not when it was deferred — deferral with
a valid runbook is honestly success-with-deferrals, not partial.

---

## 3. Mechanism — concrete protocol-text amendments

### 3.1 New wave step: 1B.4 Outcome-claim extraction (UC-2; also UC-1 in coverage-claim mode)

<!-- Source: Base (modified) — Change 1 (5th classification rule), Change 11 (INV-003 per-package granularity), Change 12 (INV-005 multi-mode precedence) -->

Inserted in `§4.1 Wave 1` immediately after Step 1B.3 (cross-task interaction-effects
scan) and before Wave 1C reflection. Behavior:

1. Parse **three claim sources**, in priority order:
   - **Spec acceptance criteria** (`§10` gold-standard reference) — every "MUST", "WILL", "EXPECTS", or bulleted success-criterion statement becomes a candidate claim.
   - **Tasklist success criteria / task description body** — every "verifies that …" or "expected to …" statement.
   - **Diff's implicit upstream-artifact claims** — for every line matching the patterns `apt-get install`, `apt install`, `pip install`, `npm install`, `gem install`, `cargo add`, `go get`, `gh api`, `aws <service>`, `terraform apply -target=<resource_type>.<name>`, a single implicit claim "<package/api/resource> provides <required-symbol-or-endpoint>" is extracted. The pattern list is **regenerable from `refs/claim-extraction-patterns.yaml`** (new ref); operators add patterns without editing SKILL.md.

   **Claim granularity (Change 11 — INV-003):** One implicit claim per `(package, install-line)` pair. Example: `apt-get install -y --no-install-recommends docker.io git curl` emits 3 separate claims (one per package). Multi-line installs across `\` continuations are concatenated first.

2. Each candidate claim is tagged with a `verification_seat` per a small classifier rubric (also in `refs/claim-extraction-patterns.yaml`):
   - Spec/tasklist claim mentioning files, symbols, configs in-repo → `in-repo`
   - Claim mentioning a third-party package, API, or external schema → `external-spec`
   - Claim mentioning live processes, kernel state, deployed behavior, latency, error rate → `runtime`
   - Claim mentioning a named downstream service or cross-process invariant → `cross-system`
   - Claim that depends on second-order reasoning the audit declines to perform at the current tier (e.g., "rebuild changes install-list outcome") → `V-Deferred-Logical`
   - Ambiguous → tag as `runtime` (most-conservative; runtime is the seat reflect cannot verify, so over-tagging here surfaces honest deferrals rather than false-pass)

   **Multi-mode precedence (Change 12 — INV-005):** when a claim satisfies multiple modes, apply this order: `V-Deferred-Logical > runtime > cross-system > external-spec > in-repo`. Rationale: `V-Deferred-Logical` signals tier-escalation; if Tier 2 resolves the logical question, the claim collapses to a stricter mode. Example: "rebuild changes the install-list outcome" is `V-Deferred-Logical` at T1 (does the mechanism propagate?); if T2 traces the logical chain and confirms the install line is unchanged, the claim becomes `external-spec` (verify against `apt-cache show`).

3. Write `<output>/outcome-claims.yaml` with required fields:

   ```yaml
   - claim_id: <slug>
     claim_text: <one-line assertion>
     source: spec_section:<id> | tasklist_item:<id> | diff_hunk_implicit:<file>:<line>
     verification_seat: in-repo | external-spec | runtime | cross-system | V-Deferred-Logical
     verification_status: pending           # filled in Wave 5
     verifier_tool: <set in Wave 5>
     evidence_ref: <set in Wave 5>
     deferral_runbook: null                 # filled in Wave 5 for runtime/cross-system/V-Deferred-Logical seats
   ```

4. Token cost: **~400-1200 tokens per run** depending on diff size and spec density.
   Within the ≤2k T1 envelope from `§5` constraint.

### 3.2 New wave step: 5.x Outcome-verification pass

<!-- Source: Base (modified) — Change 10 (INV-002 --no-install-recommends parser scope) -->

Inserted in `§4.5 Wave 5` between Step 5.0 (sc-adversarial pre-invocation probe) and
the existing synthesis substeps. Behavior:

1. **For every `in-repo` claim:** verify using the existing Serena symbol-chain from
   `§6.1` plus the citation re-Read window from `§11.5`. Drop on failure per `§11.2`.

2. **For every `external-spec` claim:** verify using the new external-spec toolkit:
   - `apt-cache show <pkg>` / `dpkg -L <pkg>` for Debian/Ubuntu packages.
   - `pip show <pkg>` / `npm view <pkg>` for Python/Node packages.
   - `gh api <endpoint>` for GitHub-resident schemas.
   - `WebFetch <upstream-doc-url>` for vendor docs (URL derived from `claim_text` by a small template, e.g., `packages.debian.org/<dist>/<pkg>` for the debian case).
   - `Skill context7` / `Skill tavily` for library/framework references.
   - Cache fetched content + content-sha + timestamp in `<output>/external-spec-cache/`. Treat cached fetches >24h old as stale; re-fetch.
   - On verification failure (claim contradicted by upstream artifact): record `verification_status: failed`, set `evidence_ref` to the cached fetch path, and **route the failed claim into `deviation-ledger.yaml` as a §10.4 Regression** with `gold_standard: external-spec` and a new `evidence_source: outcome-verification-pass` field. This reuses the existing Regression-handling path (forces `§5.3` rule 3 escalation, blocks `§14.5.2` condition 4).

   **Parser scope for `--no-install-recommends` detection (Change 10 — INV-002):** The orchestrator detects `--no-install-recommends` by literal-substring match on the install command line. Variants handled: `--no-install-recommends`, `--no-install-suggests`. Variants currently NOT handled (listed as known limitations in §5): `-o APT::Install-Recommends=false`, `Dpkg::Options::='--force-confdef'` overrides. Multi-line continuation: parser concatenates lines ending in `\` before flag detection.

3. **For every `runtime` or `cross-system` claim:** synthesize a `deferral_runbook` with
   **all four required fields** (`next_actor`, `next_command`, `success_criterion`,
   `fail_criterion`). Schema validation enforced by `evidence-validator` (§3.4 below).
   Status: `deferred`. Write the runbook to both `outcome-claims.yaml` and a
   per-claim file at `<output>/deferred-outcomes/<claim_id>.yaml` so a downstream
   consumer (or fresh agent) can pick up a single runbook by ID.

4. **For every `V-Deferred-Logical` claim (Change 1):** at Tier 1, emit a
   tier-escalation signal (the claim is logged with `verification_status: deferred`
   and `verifier_tool: tier-2-reescalate`). At Tier 2 (when adversarial debate is
   already complete), the claim is materialized as a runbook for the operator OR a
   Wave 6 remediation candidate, with the same four required runbook fields.

5. Token cost: ~500-1500 tokens when external-spec claims exist; near-zero otherwise.

### 3.3 New contract fields (`§9.1` additive — minor bump 1.0 → 1.1)

<!-- Source: Base (modified) — Change 2: added outcome_verified derived boolean from Proposal B §3.5 -->

```yaml
# Outcome verification (additive — minor bump 1.1)
outcome_claims_path: <abs path> | null
outcome_claims_total: <int>
outcome_claims_by_seat:
  in_repo: <int>
  external_spec: <int>
  runtime: <int>
  cross_system: <int>
  v_deferred_logical: <int>
outcome_claims_verified: <int>
outcome_claims_deferred: <int>      # all have valid runbooks
outcome_claims_failed: <int>        # >0 forces status: partial AND becomes §10.4 Regression
outcome_verification_complete: <bool>   # true ONLY when deferred==0 AND failed==0
outcome_verification_summary_path: <abs path> | null

# Derived single-axis convenience field (Change 2, incorporated from Proposal B §3.5)
outcome_verified: <bool>            # derived: true iff every actionable finding is in-repo OR (external-spec AND no contradiction)
deferred_outcomes_runbook_present: <bool>   # true iff every deferred row has a complete runbook (next_actor, next_command, success_criterion, fail_criterion)

# Promotion-gate companion (additive — does NOT change existing promotion_action enum)
promotion_deferred_outcomes_count: <int>     # surfaced separately to keep promotion_action enum stable
promotion_deferred_runbook_paths: [<list>]   # one path per deferred runbook moved alongside the work-unit
```

All fields are **purely additive top-level**; existing consumers ignore them per
the §9.4 unknown-field-tolerance rule. The `status` enum is **not changed** — to keep
backward compatibility, the explicit signal for "implementation verified, outcome
deferred" is the boolean pair (`status: success` AND `outcome_verification_complete:
false`). Consumers that want to gate on deferred outcomes opt in by reading the new
field. The `outcome_verified` derived boolean (Change 2) gives consumers a
single-axis routing handle without parsing the per-seat counters — `sc:troubleshoot`
Wave 6 and the sprint executor are the primary downstream beneficiaries.

### 3.4 Evidence-validator extension (`§11.2`)

<!-- Source: Base (modified) — Change 4: added presence-check responsibility from Proposal B §3.6 -->

`evidence-validator` gains two additional responsibilities:

1. **Runbook schema validation**: For every row in `outcome-claims.yaml` with
   `verification_status: deferred`, the validator checks that `deferral_runbook` has
   all four required non-empty fields and that `next_command` is a single,
   executable command (not a paragraph). Runbooks failing schema validation are
   **dropped** the same way unfounded citations are dropped — and force `status:
   partial` per the existing `§11.2` semantics.

2. **Finding-row presence check (Change 4, incorporated from Proposal B §3.6)**:
   Every actionable finding from REPORT.md MUST correspond to exactly one row in
   `outcome-claims.yaml`. Findings without a row are dropped per §11.1's
   third-bucket rule. The validator does **not** re-resolve upstream lookups
   (too expensive); it asserts presence and shape, not freshness.

Both responsibilities are policed by the same gate that polices citations, on the
same drop-not-downgrade rule. This is the structural reason runbook quality and
claim-coverage cannot rot.

### 3.5 Promotion gate (`§14.5.2`) — new condition 10

<!-- Source: Base (modified) — Change 3: merged cond 10 formulation per Proposal B §3.7 -->

```
10. outcome_claims_failed == 0 AND (outcome_verified == true OR deferred_outcomes_runbook_present == true)
```

This is the **merged formulation** per Change 3 (debate point C-007). It combines
A's strict-on-failure floor (`outcome_claims_failed == 0`) with B's
permissive-on-deferred-with-runbook clause (`outcome_verified == true OR
deferred_outcomes_runbook_present == true`). Neither alone is sufficient: A alone
would allow promotion of unverified-but-not-failed claims with no runbook; B alone
would allow promotion of failed claims that happen to have a runbook. The merge is
strictly safer than either: it blocks promotion only when a base-A or a base-B
formulation would also have blocked.

The condition is tagged
`gate_evaluation.outcome_claims_failed_zero_AND_verified_or_runbook_present`.

When `outcome_claims_deferred > 0` AND all 10 conditions otherwise pass:
- Promotion fires (`promotion_action: moved` — enum unchanged).
- The per-claim files under `<output>/deferred-outcomes/` are **moved alongside
  the work-unit** to the destination (e.g., into `.dev/tasks/done/TASK-NNN/deferred-outcomes/`).
- `promotion_deferred_outcomes_count` is non-zero in the contract, telling downstream
  automation that an operator (or a future runtime-hooked agent) still has work to do.

A `V-Deferred-Outcome` or `V-Deferred-Logical` row with no runbook is the structural
equivalent of `needs_human_decision: true` and forces `status: partial`.

### 3.6 Allowed-tools frontmatter (`§ frontmatter`)

<!-- Source: Base (original) -->

Add `WebFetch, WebSearch` (currently NOT in the reflect protocol's allowed-tools per
§6.4 of the preamble's catalog). These are the load-bearing tools for external-spec
verification; gating their addition is the only frontmatter change required. Fallback
semantics on addition-blocked are documented in §5 (Assumption A-001).

### 3.7 Generalizes to other audit skills via the artifact-shape contract

<!-- Source: Proposal B §3.9 — merged per Change 5 (replaces base's shared-refs directory approach) -->

OVM is wired into reflect first because reflect is the most-evolved audit-class
protocol. Once landed, the other audit-class skills inherit the pattern by
**writing a valid `outcome-claims.yaml` artifact** — the *artifact shape* is the
contract, not the producer-side plumbing. No new shared-refs directory is
introduced; `refs/claim-extraction-patterns.yaml` stays in
`sc-reflect-protocol/refs/` (single-skill home), mirroring `§10.6`
grounding-gaps which has no shared-refs directory either.

Sibling-skill propagation (any skill that writes a valid `outcome-claims.yaml`
participates):

- `sc:auggie-review` already calls reflect-style heuristics; its
  PR-comment formatter renders the OVM summary block.
- `sc:troubleshoot` Wave 6 Phase D already invokes reflect under
  `--type task --validate`; the runbook entries become part of the
  troubleshoot REPORT's "Next steps" section automatically (the docker case
  would have had a `next_action: which docker` row visible at this hop).
- `sc:cleanup-audit` adopts the same `outcome-claims.yaml` artifact
  name without further plumbing.
- `sc:validate-roadmap` treats coverage gaps that depend on upstream
  artifacts (e.g., "this requirement needs library X v2+") as
  `external-spec` rows.

---

## 4. How it generalizes — bug shapes

### 4.1 OS-level package split (the docker case itself)

<!-- Source: Base (original) -->

- **Claim extraction:** Diff line `apt-get install -y --no-install-recommends docker.io \` matches the `apt-get install` pattern. Implicit claim emitted: `docker.io_provides_docker_cli` — "the `docker.io` package on Debian trixie provides the `/usr/bin/docker` binary."
- **Seat tag:** `external-spec` (verifiable against `apt-cache show docker.io` or `packages.debian.org/trixie/docker.io`).
- **Wave 5 verification:** orchestrator runs `apt-cache show docker.io 2>/dev/null | grep -E '^(Conflicts|Provides|Depends|Recommends):'` (read-only Bash). Output shows `Recommends: docker-cli` (the trixie split). Implicit claim contradicted: docker.io does NOT directly provide `/usr/bin/docker`; with `--no-install-recommends`, docker-cli is skipped.
- **Outcome:** `verification_status: failed`; claim becomes a §10.4 Regression in `deviation-ledger.yaml`; `outcome_claims_failed: 1`; `status: partial`; `§14.5.2` condition 10 fails; **promotion blocked pre-merge**.

### 4.2 Performance regression (worker pool 4 → 16)

<!-- Source: Base (original) -->

- **Claim extraction:** Tasklist says "increase concurrency to handle peak load." Spec mentions p99 latency budget. Diff line changes `WORKER_POOL_SIZE = 4` → `16`. Implicit claim emitted: `worker_pool_size_change_preserves_latency_budget` — "downstream services handle 4× concurrency at the existing p99 budget."
- **Seat tag:** `runtime` + `cross-system` (latency is runtime; downstream service capacity is cross-system).
- **Wave 5 verification:** orchestrator cannot verify from its seat. Emits deferred runbook:
  ```yaml
  next_actor: operator
  next_command: "cd ops/loadtest && ./run.sh --pool 16 --duration 5m --target staging"
  success_criterion: "p99 latency ≤ 250ms AND error_rate < 0.1% AND no downstream-503"
  fail_criterion: "any threshold breach OR downstream-503 in run logs"
  ```
- **Outcome:** `verification_status: deferred`; `outcome_claims_deferred: 1`; `outcome_verification_complete: false`; `status: success` (deferral is honest, not partial); promotion fires WITH `promotion_deferred_outcomes_count: 1`; runbook file moved to `.dev/tasks/done/TASK-NNN/deferred-outcomes/worker_pool_size_change.yaml`. **Operator (or a future runtime-hooked agent) has a concrete next action.**

### 4.3 Integration failure (switch payment provider A → B)

<!-- Source: Base (original) -->

- **Claim extraction:** Diff replaces `import providerA` → `import providerB` and changes webhook handler signature parsing. Two implicit claims: (a) `providerB_webhook_signature_uses_hmac_sha256` from spec acceptance criterion; (b) `providerB_signature_header_name_is_X-B-Sig` from diff hunk.
- **Seat tag:** `external-spec` for both (verifiable against Provider B's API docs).
- **Wave 5 verification:** orchestrator runs `Skill context7` for "Provider B webhook signature scheme" OR `WebFetch <providerB-docs-url>`. Discovers Provider B actually uses HMAC-SHA512 in v2 (silent change). Claim (a) contradicted.
- **Outcome:** Regression; `status: partial`; promotion blocked. Catches an integration drift **pre-merge** that would otherwise surface as silent webhook-signature-verification failures in prod.

### 4.4 Third-party API drift (OpenAI v1 → v2 silent param removal)

<!-- Source: Base (original) -->

- **Claim extraction:** Diff line `openai.chat.completions.create(model=..., temperature=0.7, top_p=0.9)` matches an API-call pattern. Implicit claims: `openai_chat_completions_accepts_temperature`, `openai_chat_completions_accepts_top_p`.
- **Seat tag:** `external-spec`.
- **Wave 5 verification:** orchestrator queries `Skill context7 query-docs libraryId=/openai/openai-python query="chat completions temperature top_p parameters"`. If context7's most-recent indexed docs say `top_p` was removed in v2: claim contradicted.
- **Outcome:** Regression; status downgrade; promotion blocked. Catches an API contract drift **before** the live call fails.

### 4.5 Runtime config (`MAX_CONNECTIONS=1000`)

<!-- Source: Base (original) -->

- **Claim extraction:** Diff config change `MAX_CONNECTIONS=1000`. Spec says service must handle bursts. Implicit claim: `os_kernel_allows_1000_socket_connections_per_process`.
- **Seat tag:** `runtime`.
- **Wave 5 verification:** orchestrator cannot verify (no shell on deploy target). Deferred runbook:
  ```yaml
  next_actor: operator
  next_command: "ssh prod-app-01 'ulimit -n; sysctl net.core.somaxconn; sysctl net.ipv4.tcp_max_syn_backlog'"
  success_criterion: "ulimit -n >= 1000 AND somaxconn >= 1000 AND tcp_max_syn_backlog >= 1000"
  fail_criterion: "any value < 1000"
  ```
- **Outcome:** Deferred; runbook moved with work-unit; operator has one paste-and-run check.

### 4.6 Cross-service contract drift (caller updates API; downstream consumer still on old contract)

<!-- Source: Proposal B §4.5 — incorporated per Change 6 -->

- **Claim extraction:** Wave 1B.4 catalogs the API surface change as `in-repo` (the diff itself is clean) but adds a `cross-system` row for "downstream consumer service Y still passes the v1 payload shape."
- **Seat tag:** `cross-system`.
- **Wave 5 verification:** orchestrator cannot verify from its seat. Emits deferred runbook with `next_actor: downstream-agent`:
  ```yaml
  next_actor: downstream-agent
  next_command: "sc:reflect --mode post against the consumer repo at HEAD"
  success_criterion: "consumer's outcome-claims.yaml shows in-repo verification for the new payload field"
  fail_criterion: "consumer's outcome-claims.yaml shows missing or contradicted claim for new payload field"
  ```
- **Outcome:** This is the structural answer to multi-repo contract verification — the runbook *names the next reflect run*. Deferred; runbook moved with work-unit; the consumer-side audit becomes the witness.

### 4.7 Bonus shape — test-suite invariant violation (V-Deferred-Logical example)

<!-- Source: Proposal B §4 final bullet — incorporated per Change 8 -->

A diff that grows test count but loses an invariant's coverage is `in-repo` for the
test count and `V-Deferred-Logical` for the invariant question. OVM turns "we did
not check" into a *named* "we did not check," which is the difference. At Tier 1,
the `V-Deferred-Logical` row signals tier-escalation; at Tier 2, the invariant
question is resolved by either logical-fidelity tracing or a Wave 6 remediation
candidate. The tier-escalation signal is what prevents the test-count growth from
masking the invariant-coverage loss as a silent `status: success`.

---

## 5. Trade-offs and risks

<!-- Source: Base (modified) — Change 13 (A-001 assumption), Change 14 (A-002 assumption) appended -->

**Token cost:** ~400-1200 tokens for claim extraction (Wave 1B.4) + ~500-1500 for
external-spec verification (Wave 5.x) when claims surface. Both within the §5
constraint ("≤2k T1"). When no claims surface (trivial diff), both steps are
near-zero. The cost scales with the change's actual external-surface area, not with
diff size — which is the right scaling property.

**Wall-clock cost:** +30-90s per audit when WebFetch/context7 is invoked; near-zero
otherwise. Acceptable inside the existing 1-3 min T1 envelope.

**Bugs still missed:**

1. **Category-2 (logical fidelity) failures** — "force a rebuild" → "does rebuilding *change* anything?" The OVM does not extract reasoning chains; it extracts assertions. The new `V-Deferred-Logical` mode (Change 1) gives these failures a *named* home: a finding that depends on second-order reasoning is tagged as such and routed to tier-escalation, rather than being silently absorbed into the `in-repo` bucket. Tier-1 still cannot resolve them; the structural improvement is that they are now representable.
2. **Operator-ignored runbooks** — if the operator never runs the deferred runbook, the gap reopens. The fix is structurally explicit (runbook is on disk; `promotion_deferred_outcomes_count > 0` in the contract; CI/sprint executors can gate on it) but ultimately depends on a downstream actor. See Assumption A-002 below.
3. **Claim-extraction false negatives** — the extractor might miss a claim. Mitigation: claim sources are layered (spec, tasklist, diff) so a missed diff-pattern is still caught if the spec mentions it. The cost ceiling on the extractor (small rubric, not an LLM-heavy step) means false negatives are bounded by the rubric quality, which is itself ref-driven and improvable without protocol changes.
4. **Stale external-spec content** — cached WebFetches >24h old re-fetched. WebFetches that fail (network, rate-limit) fall back to "verification deferred" rather than "verification skipped," forcing the runbook path. Honest degradation.
5. **APT-flag parser scope limitations (Change 10 — INV-002):** The `--no-install-recommends` detector currently handles the literal flag and `--no-install-suggests`. It does NOT currently handle `-o APT::Install-Recommends=false` or `Dpkg::Options::='--force-confdef'` overrides. A Dockerfile that suppresses recommends via the `-o` form would slip past the parser and ship as `in-repo`-verified rather than `external-spec`-flagged. Mitigation: tracked as a known limitation; pattern table is ref-driven and can be extended without protocol changes.

**Mechanism risk: claim-extractor non-determinism.** Different runs might extract
different claim sets. Mitigation: extraction is driven from spec/tasklist literals
(regex/AST against the document) as primary source; only the diff-implicit branch
uses model judgement, and its pattern list is ref-driven, so the extracted set is
deterministic for a given pattern table.

**Surface growth:** one ref, one wave step in each of two waves, one artifact, ~10
contract fields, one promotion condition, one allowed-tool entry. High end of
"minor amendment" but well below structural rewrite. All additions reuse existing
patterns (parallel-artifact like grounding-gaps; required-field schema like the
deviation taxonomy; drop-not-downgrade like evidence-validator).

**Assumption (A-001): WebFetch/WebSearch can be added to allowed-tools.** Both this
proposal and v1.0's allowed-tools-frontmatter pattern assume the addition is purely
a frontmatter edit. If a future policy gate (security review, capability scope)
blocks the addition, the fallback is to route all `external-spec` claims to
`runtime` (deferred) with a runbook `next_actor: operator, next_instrument: <Bash
with internet access>`. Honest degradation, no silent regression.

**Assumption (A-002): operator / CI executes deferred runbooks.** The
"deferred-with-runbook = honest success" semantics depends on a downstream actor
actually running the runbook. Reflect emits the runbook and exposes
`promotion_deferred_outcomes_count > 0` in the contract; enforcement (CI gate that
blocks subsequent merges until the count is reconciled, sprint phase that halts on
open runbooks, etc.) is out of scope for the audit protocol. Operator-ignored
runbooks remain a downstream-workflow responsibility. Recommendation: pair OVM
landing with a separate proposal for CI/sprint enforcement hooks.

---

## 6. Backward-compat with existing protocols

<!-- Source: Base (modified) — Change 7: v1.1 deferred-hardening integration paragraph appended from Proposal B §6 -->

**Version bump:** **minor 1.0 → 1.1** per `§9.4`.

- All new contract fields are additive top-level; existing consumers ignore per
  the unknown-field-tolerance rule.
- `status` enum is **unchanged**. The new signal "implementation verified, outcome
  deferred" is conveyed by the boolean pair (`status: success` AND
  `outcome_verification_complete: false`).
- `promotion_action` enum is **unchanged**. The new "moved-with-deferred-outcomes"
  case is conveyed by the new `promotion_deferred_outcomes_count` field.
- Promotion gate gains a 10th condition. Existing 9 conditions are unmodified.
  Old consumers reading 9 conditions still see correct routing; new consumers
  reading 10 see tighter gating.
- `evidence-validator` gains two additional responsibilities (runbook schema
  validation and finding-row presence check); the existing citation-validation
  behavior is unchanged.
- `WebFetch`, `WebSearch` are added to allowed-tools frontmatter; no other
  frontmatter changes.

**Consumer updates per `§9.3` map:**

- **`sc-troubleshoot` Wave 6:** no required change; can opt in to read
  `outcome_verification_complete` or the new `outcome_verified` derived boolean
  to gate Phase D escalation.
- **`superclaude sprint run` (executor.py):** opt-in. A new TurnLedger consumer
  field can elect to halt the phase when `promotion_deferred_outcomes_count > 0`
  AND the next phase declares it requires runtime-verified state.
- **`sc-task-protocol` end-of-task hook:** opt-in. Can surface
  `promotion_deferred_runbook_paths` to user.
- **`sc:roadmap` / `sc:tasklist`:** unaffected.
- **`task-builder`:** opt-in. Can ingest a deferred runbook to materialize a
  runtime-verification follow-up task automatically.

**Migration window per `§9.4`:** one full minor release cycle before any of the new
fields become load-bearing for any consumer. No deprecations needed (purely
additive).

**v1.1 deferred-hardening integration (Change 7, incorporated from Proposal B §6).**
OVM folds naturally into §19.2's INV-023 path: the iteration-2 evidence for the
`T2-converges-on-wrong-answer` case can now include outcome-verification
classification accuracy as a sub-criterion, and the v1.1 tightening from
"conditional" to "demonstrated" gains a broader sufficiency surface. The post-OVM
sufficiency claim covers implementation fidelity *and* upstream-resolvable outcome
fidelity, with deferred outcomes explicitly named. This is a tightening, not a
loosening.

---

## 7. Falsifier — eval cases

### 7.1 Iteration-1 active fixture — `outcome-verification-docker-cli-miss`

<!-- Source: Base (original) -->

Modeled on `§12.5`'s `T2-converges-on-wrong.yaml` skeleton. Lives at
`.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/outcome-verification-docker-cli-miss.yaml`.

```yaml
id: outcome-verification-docker-cli-miss
type: held-out adversarial
status: active   # iteration-1 fixture (this miss is already in the wild — no skeleton stage)
fixture: fixtures/docker-cli-miss/
setup: |
  Fixture contents:
  - spec.md states: "AIDev02 base image MUST include the docker CLI for
    agentcontainers.dockercli.List to succeed at startup."
  - tasklist.md Action 3: "Rebuild AIDev02 image so docker.io is installed."
  - Dockerfile.coder contains line:
      RUN apt-get install -y --no-install-recommends \
        docker.io \
        git \
        curl
  - Image base: debian:trixie (declared in Dockerfile FROM line)
  - Mocked apt-cache: `apt-cache show docker.io` on trixie returns:
      Package: docker.io
      Recommends: docker-cli, docker-buildx, docker-compose
      (NOTE: docker-cli is in Recommends, not Depends; --no-install-recommends skips it)

pre_seeding_mechanism:
  delivery_channel: fixture   # the fixture IS the test; no anchoring seed needed
  rationale: |
    Mirrors the 2026-05-30 production miss. Tests whether the OVM pipeline catches
    the docker.io/docker-cli split as an outcome-claim failure before promotion.

expected:
  outcome_claims_total: >= 1
  outcome_claims_by_seat.external_spec: >= 1
  outcome_claims:
    - claim_id matches "docker.io_provides_docker_cli" (or close slug)
      claim_text contains "docker.io" AND
                  ("provides" OR "/usr/bin/docker" OR "docker CLI")
      verification_seat: external-spec
      verification_status: failed
      evidence_ref: matches "<output>/external-spec-cache/apt-cache-show-docker.io.*"
  outcome_claims_failed: >= 1
  outcome_verification_complete: false
  deviation_count_by_class.regression: >= 1   # failed external-spec → Regression
  status: partial                              # forced by outcome_claims_failed > 0
  promotion_action: skipped                    # §14.5.2 condition 10 fails
  promotion_skip_reason: gate-failed
  gate_evaluation.outcome_claims_failed_zero_AND_verified_or_runbook_present: fail   # new field in promotion-log

assertion: outcome_claims_failed >= 1 AND status == partial AND promotion_action == skipped

severity: AUTO-FAIL if status: success
  OR if outcome_verification_complete == true
  OR if promotion_action == moved
  (any of these means the OVM did NOT catch the docker miss → the structural fix
   does NOT solve the docker-class verification gap → proposal disproven)
```

A passing run on this fixture is the empirical proof that the OVM closes the
verification gap on the exact incident in the preamble. A failing run (auto-fail
severity met) falsifies the proposal: the fix is insufficient and a different
structural mechanism is needed.

### 7.2 Sibling falsifier — `outcome-verification-deferred-runtime-config`

<!-- Source: Proposal B §7 companion falsifier — incorporated per Change 9 -->

Lives at
`.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/outcome-verification-deferred-runtime-config.yaml`.
Covers the `runtime` (V-Deferred-Outcome) mode with mandatory-runbook semantics,
modeled on base §4.5's sysctl-tuning runbook.

```yaml
id: outcome-verification-deferred-runtime-config
type: held-out adversarial
status: skeleton-pending-iteration-2-fixture   # sibling to docker case; promoted at next iteration
fixture: fixtures/deferred-runtime-config/
setup: |
  - spec.md states: "Service must handle 1000 concurrent connections."
  - tasklist.md: "Set MAX_CONNECTIONS=1000 in service config."
  - Diff: config file gains `MAX_CONNECTIONS=1000`.
  - No spec or tasklist line addresses kernel-level limits.

expected:
  outcome_claims_total: >= 1
  outcome_claims_by_seat.runtime: >= 1
  outcome_claims:
    - claim_id matches "os_kernel_allows_1000.*"
      verification_seat: runtime
      verification_status: deferred
      deferral_runbook:
        next_actor: operator
        next_command: contains "ulimit -n" AND "somaxconn"
        success_criterion: contains ">= 1000"
        fail_criterion: contains "< 1000"
  outcome_claims_deferred: >= 1
  deferred_outcomes_runbook_present: true
  outcome_verification_complete: false
  status: success                              # deferral is honest, not failure
  promotion_action: moved                      # cond 10 passes (verified-or-runbook-present)
  promotion_deferred_outcomes_count: >= 1
  promotion_deferred_runbook_paths: not empty

assertion_pass: |
  outcome_claims_deferred >= 1 AND
  deferred_outcomes_runbook_present == true AND
  promotion_action == moved AND
  promotion_deferred_outcomes_count >= 1

assertion_fail_runbook_empty: |
  When runbook is intentionally empty in the fixture,
  cond 10 MUST fail and promotion_action MUST equal skipped.

severity: AUTO-FAIL if deferred_outcomes_runbook_present == true with empty runbook
  OR if cond 10 passes with an empty runbook
  OR if status == partial when runbook is complete
  (deferred-with-runbook is honest success, not partial — failing here means
   the mode-routing is broken)
```

This sibling case proves OVM correctly distinguishes "deferred with runbook"
(honest success) from "deferred without runbook" (must force partial), per the
Change 3 merged cond 10 formulation.

---

## 8. Out-of-scope items

<!-- Source: Base (original) -->

1. **Category-2 logical-fidelity failures** (mechanism reasoning) — OVM extracts
   assertions, not reasoning chains. The `V-Deferred-Logical` mode (Change 1)
   gives these failures a *named* representational home but does not resolve them
   at Tier 1; tier-escalation is the resolution path. A separate logical-fidelity
   layer is tracked separately.
2. **Operator-ignored deferred runbooks** — OVM produces machine-readable runbooks;
   execution is workflow policy, not audit protocol. `promotion_deferred_outcomes_count`
   is on the contract so CI/sprint can gate, but enforcement is out of scope. See
   Assumption A-002 in §5.
3. **Live runtime hooks** — OVM does not introduce shell access on deploy targets.
   The runtime seat exists *because* the orchestrator cannot reach runtime; excluded
   by §5 constraint "should not require live runtime access."
4. **Historical-regression detection** — comparing against previous successful runs
   is a separate feature; OVM verifies forward against spec/upstream-artifact only.
5. **Auto-execution of deferred runbooks** — even given shell-capable downstream
   agents, OVM does not auto-execute. Same rationale as §17's "Will Not —
   Auto-execute a Tier 3 remediation task."
6. **Cross-skill ref sync tooling** — superseded by Change 5: there is no shared
   refs directory; sibling skills participate by writing a valid
   `outcome-claims.yaml`. The `make verify-shared-refs` target is no longer needed.
7. **Revisiting `§17.7` Kill-List item 6** (5th deviation category) — OVM routes
   around this kill: `outcome-claims.yaml` is a third *parallel* artifact peer to
   `deviation-ledger.yaml` and `grounding-gaps.yaml`, NOT a 5th deviation class.
   The 4-category taxonomy is preserved; failed external-spec verifications become
   §10.4 Regressions via the existing taxonomy. The Kill is respected. The
   `V-Deferred-Logical` mode (Change 1) is a 5th *verification* mode, not a 5th
   *deviation* category.
8. **v1.1 deferred-hardening (`§19`)** — OVM does not fold into INV-021 (vendor
   heterogeneity) but does integrate with INV-023 (sufficiency claim) per Change 7
   in §6 above. Can ship in the same v1.1 release.

---

**End of merged proposal.**
