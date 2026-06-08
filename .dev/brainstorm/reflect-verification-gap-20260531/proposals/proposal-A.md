# Proposal A — Outcome-Verification Manifest with Seat-Tagged Claims (OVM)

> **Author:** Brainstorm Agent A
> **Date:** 2026-05-31
> **Framing:** Structural fix to the verification-gap class exemplified by the docker-cli
> miss in `sc:reflect`. Pre-merge audit emitted `status: success` for a change that
> shipped a broken `apt-get install --no-install-recommends docker.io` line; the operator
> caught the breakage post-merge with one `which docker`. Root cause was not a missing
> check — it was a missing **contract** distinguishing what the orchestrator verified
> from what it cannot verify from its seat.

---

## 1. Problem framing

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

**Named central idea:** Every audit run produces, in addition to the existing
`deviation-ledger.yaml` (`§10`) and `grounding-gaps.yaml` (`§10.6`), a third
peer-grade artifact — **`outcome-claims.yaml`** — that enumerates the **outcome
claims** the change makes (assertions about behavior, upstream artifacts, runtime
state, or cross-system contracts that go beyond `code == spec`). Each claim is tagged
with one of four **verification seats**:

| Seat | Definition | Who can verify | Reflect's responsibility |
|------|------------|----------------|--------------------------|
| **`in-repo`** | Verifiable by reading repo files, running diagnostics, or symbol queries | Reflect orchestrator (existing toolkit) | MUST verify; failure → drop the claim and force `status: partial` per `§11.2` semantics |
| **`external-spec`** | Verifiable by querying an upstream artifact: package registry, OS package manager, vendor API docs, OpenAPI schema, source-of-truth changelog | Reflect orchestrator using `WebFetch` / `WebSearch` / `context7` / `tavily` / read-only `Bash` (`apt-cache show`, `pip show`, `npm view`, `gh api`) | MUST verify when claim surfaces; on failure, treat as **Regression** (per `§10.4`) and force escalation per `§5.3` rule 3 |
| **`runtime`** | Verifiable only against the running deployed system (process state, kernel state, network reachability, live load behavior) | Operator (or future runtime-hooked agent) | MUST emit a structured **deferred-verification runbook** with concrete `next_actor`, `next_command`, `success_criterion`, `fail_criterion`; reflect ships `outcome_verification_complete: false` |
| **`cross-system`** | Verifiable only by orchestrating multiple live systems (downstream service load, third-party webhook delivery, distributed-trace propagation) | Operator + named downstream system | Same as `runtime`, with the `next_actor` field naming the specific other system |

The conflation is resolved not by recategorizing failure shapes (whack-a-mole) but
by recategorizing **who can answer the verification question**. Any future bug shape
— performance regression, integration drift, OS package split, runtime config
violation, API contract change — falls under exactly one of these four seats by its
nature. The protocol gains a contractual home for "this orchestrator from this seat
cannot answer this question" that is honest, machine-readable, and pickup-able.

This is the **`grounding-gaps.yaml` pattern from `§10.6` applied to outcome
verification** — exactly analogous. Grounding-gaps surfaces "evidence insufficient
to classify a deviation"; OVM surfaces "evidence insufficient to verify an
outcome." Both are parallel artifacts with required fields; OVM forces `status:
partial` only when verification *failed*, not when it was deferred — deferral with
a valid runbook is honestly success-with-deferrals, not partial.

---

## 3. Mechanism — concrete protocol-text amendments

### 3.1 New wave step: 1B.4 Outcome-claim extraction (UC-2; also UC-1 in coverage-claim mode)

Inserted in `§4.1 Wave 1` immediately after Step 1B.3 (cross-task interaction-effects
scan) and before Wave 1C reflection. Behavior:

1. Parse **three claim sources**, in priority order:
   - **Spec acceptance criteria** (`§10` gold-standard reference) — every "MUST", "WILL", "EXPECTS", or bulleted success-criterion statement becomes a candidate claim.
   - **Tasklist success criteria / task description body** — every "verifies that …" or "expected to …" statement.
   - **Diff's implicit upstream-artifact claims** — for every line matching the patterns `apt-get install`, `apt install`, `pip install`, `npm install`, `gem install`, `cargo add`, `go get`, `gh api`, `aws <service>`, `terraform apply -target=<resource_type>.<name>`, a single implicit claim "<package/api/resource> provides <required-symbol-or-endpoint>" is extracted. The pattern list is **regenerable from `refs/claim-extraction-patterns.yaml`** (new ref); operators add patterns without editing SKILL.md.

2. Each candidate claim is tagged with a `verification_seat` per a small classifier rubric (also in `refs/claim-extraction-patterns.yaml`):
   - Spec/tasklist claim mentioning files, symbols, configs in-repo → `in-repo`
   - Claim mentioning a third-party package, API, or external schema → `external-spec`
   - Claim mentioning live processes, kernel state, deployed behavior, latency, error rate → `runtime`
   - Claim mentioning a named downstream service or cross-process invariant → `cross-system`
   - Ambiguous → tag as `runtime` (most-conservative; runtime is the seat reflect cannot verify, so over-tagging here surfaces honest deferrals rather than false-pass)

3. Write `<output>/outcome-claims.yaml` with required fields:

   ```yaml
   - claim_id: <slug>
     claim_text: <one-line assertion>
     source: spec_section:<id> | tasklist_item:<id> | diff_hunk_implicit:<file>:<line>
     verification_seat: in-repo | external-spec | runtime | cross-system
     verification_status: pending           # filled in Wave 5
     verifier_tool: <set in Wave 5>
     evidence_ref: <set in Wave 5>
     deferral_runbook: null                 # filled in Wave 5 for runtime/cross-system seats
   ```

4. Token cost: **~400-1200 tokens per run** depending on diff size and spec density.
   Within the ≤2k T1 envelope from `§5` constraint.

### 3.2 New wave step: 5.x Outcome-verification pass

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

3. **For every `runtime` or `cross-system` claim:** synthesize a `deferral_runbook` with
   **all four required fields** (`next_actor`, `next_command`, `success_criterion`,
   `fail_criterion`). Schema validation enforced by `evidence-validator` (§3.4 below).
   Status: `deferred`. Write the runbook to both `outcome-claims.yaml` and a
   per-claim file at `<output>/deferred-outcomes/<claim_id>.yaml` so a downstream
   consumer (or fresh agent) can pick up a single runbook by ID.

4. Token cost: ~500-1500 tokens when external-spec claims exist; near-zero otherwise.

### 3.3 New contract fields (`§9.1` additive — minor bump 1.0 → 1.1)

```yaml
# Outcome verification (additive — minor bump 1.1)
outcome_claims_path: <abs path> | null
outcome_claims_total: <int>
outcome_claims_by_seat:
  in_repo: <int>
  external_spec: <int>
  runtime: <int>
  cross_system: <int>
outcome_claims_verified: <int>
outcome_claims_deferred: <int>      # all have valid runbooks
outcome_claims_failed: <int>        # >0 forces status: partial AND becomes §10.4 Regression
outcome_verification_complete: <bool>   # true ONLY when deferred==0 AND failed==0
outcome_verification_summary_path: <abs path> | null

# Promotion-gate companion (additive — does NOT change existing promotion_action enum)
promotion_deferred_outcomes_count: <int>     # surfaced separately to keep promotion_action enum stable
promotion_deferred_runbook_paths: [<list>]   # one path per deferred runbook moved alongside the work-unit
```

All fields are **purely additive top-level**; existing consumers ignore them per
the §9.4 unknown-field-tolerance rule. The `status` enum is **not changed** — to keep
backward compatibility, the explicit signal for "implementation verified, outcome
deferred" is the boolean pair (`status: success` AND `outcome_verification_complete:
false`). Consumers that want to gate on deferred outcomes opt in by reading the new
field.

### 3.4 Evidence-validator extension (`§11.2`)

`evidence-validator` gains a second responsibility: **runbook schema validation**.
For every row in `outcome-claims.yaml` with `verification_status: deferred`, the
validator checks that `deferral_runbook` has all four required non-empty fields and
that `next_command` is a single, executable command (not a paragraph). Runbooks
failing schema validation are **dropped** the same way unfounded citations are
dropped — and force `status: partial` per the existing `§11.2` semantics.

This is the structural reason runbook quality cannot rot: it's policed by the
same gate that policies citations, on the same drop-not-downgrade rule.

### 3.5 Promotion gate (`§14.5.2`) — new condition 10

```
10. outcome_claims_failed == 0
```

When `outcome_claims_deferred > 0` AND all 10 conditions otherwise pass:
- Promotion fires (`promotion_action: moved` — enum unchanged).
- The per-claim files under `<output>/deferred-outcomes/` are **moved alongside
  the work-unit** to the destination (e.g., into `.dev/tasks/done/TASK-NNN/deferred-outcomes/`).
- `promotion_deferred_outcomes_count` is non-zero in the contract, telling downstream
  automation that an operator (or a future runtime-hooked agent) still has work to do.

### 3.6 Allowed-tools frontmatter (`§ frontmatter`)

Add `WebFetch, WebSearch` (currently NOT in the reflect protocol's allowed-tools per
§6.4 of the preamble's catalog). These are the load-bearing tools for external-spec
verification; gating their addition is the only frontmatter change required.

### 3.7 Generalizes to other audit skills via a shared ref

The `refs/claim-extraction-patterns.yaml` and the OVM schema (`outcome-claims.yaml` +
the four-seat tagging) ship as a **shared ref** under
`/config/.claude/skills/_shared/outcome-verification/` (new shared-refs directory; or
under `sc-reflect-protocol/refs/` and symlinked). `sc:auggie-review`,
`sc:validate-roadmap`, `sc:troubleshoot` Wave 6, and `sc:cleanup-audit` consume the
same ref. Each audit skill's existing wave architecture gains one parallel step
("outcome-claim extraction") and one parallel artifact ("outcome-claims.yaml"). The
mechanism is identical across skills; only the trigger waves differ.

---

## 4. How it generalizes — five bug shapes

### 4.1 OS-level package split (the docker case itself)

- **Claim extraction:** Diff line `apt-get install -y --no-install-recommends docker.io \` matches the `apt-get install` pattern. Implicit claim emitted: `docker.io_provides_docker_cli` — "the `docker.io` package on Debian trixie provides the `/usr/bin/docker` binary."
- **Seat tag:** `external-spec` (verifiable against `apt-cache show docker.io` or `packages.debian.org/trixie/docker.io`).
- **Wave 5 verification:** orchestrator runs `apt-cache show docker.io 2>/dev/null | grep -E '^(Conflicts|Provides|Depends|Recommends):'` (read-only Bash). Output shows `Recommends: docker-cli` (the trixie split). Implicit claim contradicted: docker.io does NOT directly provide `/usr/bin/docker`; with `--no-install-recommends`, docker-cli is skipped.
- **Outcome:** `verification_status: failed`; claim becomes a §10.4 Regression in `deviation-ledger.yaml`; `outcome_claims_failed: 1`; `status: partial`; `§14.5.2` condition 10 fails; **promotion blocked pre-merge**.

### 4.2 Performance regression (worker pool 4 → 16)

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

- **Claim extraction:** Diff replaces `import providerA` → `import providerB` and changes webhook handler signature parsing. Two implicit claims: (a) `providerB_webhook_signature_uses_hmac_sha256` from spec acceptance criterion; (b) `providerB_signature_header_name_is_X-B-Sig` from diff hunk.
- **Seat tag:** `external-spec` for both (verifiable against Provider B's API docs).
- **Wave 5 verification:** orchestrator runs `Skill context7` for "Provider B webhook signature scheme" OR `WebFetch <providerB-docs-url>`. Discovers Provider B actually uses HMAC-SHA512 in v2 (silent change). Claim (a) contradicted.
- **Outcome:** Regression; `status: partial`; promotion blocked. Catches an integration drift **pre-merge** that would otherwise surface as silent webhook-signature-verification failures in prod.

### 4.4 Third-party API drift (OpenAI v1 → v2 silent param removal)

- **Claim extraction:** Diff line `openai.chat.completions.create(model=..., temperature=0.7, top_p=0.9)` matches an API-call pattern. Implicit claims: `openai_chat_completions_accepts_temperature`, `openai_chat_completions_accepts_top_p`.
- **Seat tag:** `external-spec`.
- **Wave 5 verification:** orchestrator queries `Skill context7 query-docs libraryId=/openai/openai-python query="chat completions temperature top_p parameters"`. If context7's most-recent indexed docs say `top_p` was removed in v2: claim contradicted.
- **Outcome:** Regression; status downgrade; promotion blocked. Catches an API contract drift **before** the live call fails.

### 4.5 Runtime config (`MAX_CONNECTIONS=1000`)

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

---

## 5. Trade-offs and risks

**Token cost:** ~400-1200 tokens for claim extraction (Wave 1B.4) + ~500-1500 for
external-spec verification (Wave 5.x) when claims surface. Both within the §5
constraint ("≤2k T1"). When no claims surface (trivial diff), both steps are
near-zero. The cost scales with the change's actual external-surface area, not with
diff size — which is the right scaling property.

**Wall-clock cost:** +30-90s per audit when WebFetch/context7 is invoked; near-zero
otherwise. Acceptable inside the existing 1-3 min T1 envelope.

**Bugs still missed:**

1. **Category-2 (logical fidelity) failures** — "force a rebuild" → "does rebuilding *change* anything?" The OVM does not extract reasoning chains; it extracts assertions. A diff that rebuilds an image without changing the install line passes implementation verification (the rebuild was triggered) AND any OVM claims about the install line (they're the same broken claims as before — but the *outcome* claim is the install line's outcome, which the OVM does catch in 4.1 above). The genuinely-missed shape: a multi-step mechanism whose intermediate steps each "work" but whose composition doesn't achieve the goal. Mitigation: out-of-scope; tracked separately.
2. **Operator-ignored runbooks** — if the operator never runs the deferred runbook, the gap reopens. The fix is structurally explicit (runbook is on disk; `promotion_deferred_outcomes_count > 0` in the contract; CI/sprint executors can gate on it) but ultimately depends on a downstream actor.
3. **Claim-extraction false negatives** — the extractor might miss a claim. Mitigation: claim sources are layered (spec, tasklist, diff) so a missed diff-pattern is still caught if the spec mentions it. The cost ceiling on the extractor (small rubric, not an LLM-heavy step) means false negatives are bounded by the rubric quality, which is itself ref-driven and improvable without protocol changes.
4. **Stale external-spec content** — cached WebFetches >24h old re-fetched. WebFetches that fail (network, rate-limit) fall back to "verification deferred" rather than "verification skipped," forcing the runbook path. Honest degradation.

**Mechanism risk: claim-extractor non-determinism.** Different runs might extract
different claim sets. Mitigation: extraction is driven from spec/tasklist literals
(regex/AST against the document) as primary source; only the diff-implicit branch
uses model judgement, and its pattern list is ref-driven, so the extracted set is
deterministic for a given pattern table.

**Surface growth:** one ref, one wave step in each of two waves, one artifact, ~8
contract fields, one promotion condition, one allowed-tool entry. High end of
"minor amendment" but well below structural rewrite. All additions reuse existing
patterns (parallel-artifact like grounding-gaps; required-field schema like the
deviation taxonomy; drop-not-downgrade like evidence-validator).

---

## 6. Backward-compat with existing protocols

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
- `evidence-validator` gains a second responsibility (runbook schema validation);
  the existing citation-validation behavior is unchanged.
- `WebFetch`, `WebSearch` are added to allowed-tools frontmatter; no other
  frontmatter changes.

**Consumer updates per `§9.3` map:**

- **`sc-troubleshoot` Wave 6:** no required change; can opt in to read
  `outcome_verification_complete` to gate Phase D escalation.
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

---

## 7. Falsifier — eval case `outcome-verification-docker-cli-miss`

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
  gate_evaluation.outcome_claims_failed_zero: fail   # new field in promotion-log

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

---

## 8. Out-of-scope items

1. **Category-2 logical-fidelity failures** (mechanism reasoning) — OVM extracts
   assertions, not reasoning chains. Pure mechanism-reasoning bugs need a separate
   logical-fidelity layer; tracked separately.
2. **Operator-ignored deferred runbooks** — OVM produces machine-readable runbooks;
   execution is workflow policy, not audit protocol. `promotion_deferred_outcomes_count`
   is on the contract so CI/sprint can gate, but enforcement is out of scope.
3. **Live runtime hooks** — OVM does not introduce shell access on deploy targets.
   The runtime seat exists *because* the orchestrator cannot reach runtime; excluded
   by §5 constraint "should not require live runtime access."
4. **Historical-regression detection** — comparing against previous successful runs
   is a separate feature; OVM verifies forward against spec/upstream-artifact only.
5. **Auto-execution of deferred runbooks** — even given shell-capable downstream
   agents, OVM does not auto-execute. Same rationale as §17's "Will Not —
   Auto-execute a Tier 3 remediation task."
6. **Cross-skill ref sync tooling** — shared `refs/claim-extraction-patterns.yaml`
   needs a `make verify-shared-refs` target; build-system change, not protocol.
7. **Revisiting `§17.7` Kill-List item 6** (5th deviation category) — OVM routes
   around this kill: `outcome-claims.yaml` is a third *parallel* artifact peer to
   `deviation-ledger.yaml` and `grounding-gaps.yaml`, NOT a 5th deviation class.
   The 4-category taxonomy is preserved; failed external-spec verifications become
   §10.4 Regressions via the existing taxonomy. The Kill is respected.
8. **v1.1 deferred-hardening (`§19`)** — OVM does not fold into INV-021 (vendor
   heterogeneity) or INV-023 (sufficiency claim); different structural gap. Can
   ship in the same v1.1 release but is independent.

---

**End of proposal.**
