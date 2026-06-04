# Proposal B — The Outcome-Verification Ledger (OVL)

> Agent B, brainstorm pipeline 20260531. Independent of Agent A. Built from
> `/config/workspace/IronClaude/.dev/brainstorm/reflect-verification-gap-20260531/PREAMBLE.md`
> and `/config/.claude/skills/sc-reflect-protocol/SKILL.md` (v1.0).

## 1. Problem framing

The reflect protocol's `status: success` verdict conflates **two distinct
verifications** that the literature, the protocol surface, and the docker-cli
miss all show are independent. *Implementation fidelity* — "code matches spec at
the cited file:line" — is the verification the entire v1.0 contract is built
around: evidence-validator drops, citation re-Read window, the §11.3 disjoint-set
calibrator, the §11.4 heterogeneous reviewer ensemble, the §12 grader rubric, the
§14.5.2 9-condition promotion gate. *Outcome fidelity* — "the change produces
its claimed effect in the live system, including against external upstream
artifacts the diff depends on" — has zero first-class representation. Reflect
ships `status: success` whenever implementation verification clears, regardless
of whether outcome verification was attempted, deferred, or even articulated as a
distinct surface. The docker miss is the natural consequence: Action 3 "rebuild
the image" was implemented faithfully (PR #67's SHA bump correctly fires
`triggers.dockerfile_sha256`), so reflect cleared at C=0.91; the *outcome* claim
— "after rebuild, `/usr/bin/docker` will exist" — was never separately tracked
and never separately verified. The protocol could not even *represent* the gap,
so it could not flag it. This is structural conflation, not a missing check.

## 2. Proposed structural fix — The Outcome-Verification Ledger (OVL)

Introduce a **third parallel artifact** that sits beside the §10 deviation
register and the §10.6 grounding-gaps register, and a corresponding
**outcome-verification taxonomy** that classifies every actionable finding in
the report by *who can verify the outcome, with what instrument, from what
seat*. The OVL is the durable home for the verification surface the v1.0
contract currently has nowhere to write to.

Crucially, the OVL is **not a checklist of external-artifact lookups**. It is
a **mode-of-verification recategorization** applied to every actionable finding
the report already contains: for each finding, the orchestrator must declare its
verification mode (one of four — see §3) and, when the mode is anything other
than `Verified-In-Repo`, emit a structured *runbook entry* — next-actor,
next-instrument, next-action, expected-witness — that a downstream agent, CI
gate, or operator can execute without re-reading prose.

The name centers the mechanism: a **ledger** (machine-readable, append-only,
mirrors §10.6's proven pattern) for **outcome verifications** (the second axis
of the conflation), with explicit modes that route deferred work to a
**next-actor** rather than burying it under `status: success`.

The structural insight is that the gap is **representational**, not procedural.
The reflect protocol already has the right machinery for "we cannot verify this
from here" — `cannot_validate_without_user_input`, `needs_human_decision`,
`grounding-gaps.yaml`. What it lacks is the *predicate* that triggers these
fields when the unverifiable thing is *outcome*, not *evidence*. OVL is that
predicate, made first-class.

## 3. Mechanism — concrete protocol-text amendments

### 3.1 New verification-mode taxonomy (§10.7-bis — new sub-section)

Every actionable finding in REPORT.md — every Action item, every recommendation,
every Authorized/Necessary/Drift/Regression deviation that ships with a remediation
— is tagged with exactly one of four **verification modes**:

| Mode | Definition | Can the audit-class skill verify it from the orchestrator's seat? |
|------|-----------|--------------------------------------------------------------------|
| **V-Repo** (Verified-In-Repo) | The claim is fully checkable by Read + diff + symbol tools against on-disk state, and was so checked by Wave 5 evidence-validator. | Yes; already done by v1.0. |
| **V-Upstream-Available** | The claim depends on an external artifact (package, OS API, third-party schema, doc URL) the orchestrator *has tools to reach* (WebFetch / WebSearch / context7 / `apt-cache show` / `gh api`) and that lookup completed cleanly. | Yes, when the toolchain is present and the lookup succeeds. |
| **V-Deferred-Outcome** | The claim is about the *post-deploy state* of a live system the orchestrator has no shell on — runtime config, container filesystem, deployed binary presence, performance under load, downstream consumer health. | No, structurally. Must produce a runbook. |
| **V-Deferred-Logical** | The claim depends on second-order reasoning the audit declines to perform at this tier (e.g., "will this rebuild change the install-list output?"). The reasoning is in-bounds for Tier 2 but skipped at Tier 1. | Not at the current tier; tier-escalation can resolve it. |

Findings that cannot be placed in any mode are dropped per §11.1's
Grounded/Inferred binary — the OVL does not add a fifth bucket.

### 3.2 New parallel artifact: `outcome-verification.yaml`

Written to `<output>/outcome-verification.yaml`. Mirrors §10.6 grounding-gaps
pattern exactly:

```yaml
- finding_ref: <action-id-or-recommendation-id-from-REPORT.md>
  finding_text: <one-line summary>
  verification_mode: V-Repo | V-Upstream-Available | V-Deferred-Outcome | V-Deferred-Logical
  evidence_anchor: <file:line OR URL OR command-line OR null>
  next_actor: orchestrator | operator | ci-gate | downstream-agent | none
  next_instrument: WebFetch | WebSearch | context7 | bash:<cmd> | shell-on-deploy-target | tier-2-reescalate | none
  next_action: <one-line imperative — e.g., "Run `which docker` on the workspace and confirm /usr/bin/docker exists">
  expected_witness: <what success looks like — e.g., "stdout matches /usr/bin/docker">
  deferral_reason: <why this mode and not a stricter one — e.g., "orchestrator has no shell on the deploy target">
  blocks_promotion: true | false
```

`blocks_promotion: true` is the field that propagates the gap into the §14.5.2
gate. The default for `V-Deferred-Outcome` is `blocks_promotion: false` (most
deferred outcomes are post-deploy and cannot block ship), but
`V-Upstream-Available` entries that resolved to a *contradiction* MUST set
`blocks_promotion: true` and `status` is forced to `partial`.

### 3.3 Wave 1B addition: §4.1 Step 1B.4 — verification-mode classification

A new step inserted after the existing 1B.3 cross-task interaction scan:

> **Step 1B.4 (verification-mode classification, both modes).** For each
> actionable finding identified in Wave 1B (recommendation, Action, or
> deviation), classify under the §10.7-bis taxonomy. The classification is
> mechanical, not investigative:
>
> 1. If the finding's claim is fully resolvable by Read + diff + symbol tools
>    against the on-disk repo state → `V-Repo`.
> 2. Else, if the finding names an external artifact (package name, library
>    version, OS API, URL, registry identifier) AND the protocol's allowed-tools
>    surface contains a tool that resolves the artifact's contract — `V-Upstream-Available`.
>    Invoke the tool **once per distinct artifact** (memoized to bound cost). On
>    cleanly-resolved contract, attach the result as `evidence_anchor`. On lookup
>    failure or contradiction, route per §3.4 below.
> 3. Else, if the finding claims a property of post-deploy runtime state →
>    `V-Deferred-Outcome` with a mandatory runbook entry (next_actor=operator
>    OR ci-gate, next_instrument=shell-on-deploy-target, with concrete
>    next_action and expected_witness).
> 4. Else, the finding requires reasoning the current tier did not perform →
>    `V-Deferred-Logical`. At Tier 1, this is a tier-escalation signal; at
>    Tier 2 with adversarial debate already complete, it is a runbook for the
>    operator OR a Wave 6 remediation candidate.

Emit `outcome_verification_classified: true` in the contract when this step runs.

### 3.4 Wave 1B step 1B.4.b — contradiction routing

When `V-Upstream-Available` lookup returns a contradiction (the upstream artifact
does NOT provide what the diff assumes — e.g., `apt-cache show docker.io` on
Debian 13 shows no `Depends: docker-cli`), the finding is **promoted to a
synthetic Regression candidate** (§10.4) AND added to the deviation register
with `evidence_anchor` pointing at the lookup output. This routes contradictions
into the existing §5.3 rule-3 escalation path: any Regression candidate forces
T2. The pre-merge docker miss would have surfaced here.

### 3.5 New top-level contract fields (§9.1 additions)

```yaml
# Outcome verification (new in 1.1)
outcome_verification_classified: <bool>          # 1B.4 ran
outcome_ledger_path: <abs path> | null
outcome_v_repo_count: <int>
outcome_v_upstream_available_count: <int>
outcome_v_deferred_outcome_count: <int>
outcome_v_deferred_logical_count: <int>
outcome_contradictions_found: <int>              # V-Upstream-Available lookups that disagreed with the diff
outcome_verified: bool                           # derived: true iff every actionable finding is V-Repo OR (V-Upstream-Available AND no contradiction)
deferred_outcomes_runbook_present: bool          # true iff every V-Deferred-* row has a complete runbook (next_actor, next_action, expected_witness)
```

`outcome_verified` is the **derived single-axis field** consumers can route on
without parsing the four counts.

### 3.6 §11.2 evidence-validator extension

The mandatory final gate is extended by **one assertion**: every actionable
finding in REPORT.md MUST correspond to exactly one row in
`outcome-verification.yaml`. Findings without a row are dropped per §11.1's
"third bucket" rule. The validator does **not** re-resolve upstream lookups
(too expensive); it asserts presence and shape, not freshness.

### 3.7 §14.5.2 promotion-gate amendment (Condition 10, additive)

The 9-condition gate becomes a **10-condition gate**. New condition:

> **10. `outcome_verified == true` OR `deferred_outcomes_runbook_present == true`.**
> Promotion fires when every actionable finding is either fully verified
> in-repo / against a resolved upstream, OR explicitly deferred with a
> machine-readable runbook a downstream actor can execute. A finding that is
> tagged `V-Deferred-Outcome` without a runbook fails this condition. Tagged as
> `gate_evaluation.outcome_verified_or_deferred_with_runbook`.

This is the **honesty downgrade** the preamble §5 requires: a `status: success`
that ships with unverified outcomes is permitted *only* when those outcomes are
explicitly named and explicitly handed off. A `V-Deferred-Outcome` row with no
runbook is the structural equivalent of `needs_human_decision: true` and
forces `status: partial`.

### 3.8 Allowed-tools frontmatter additions

The reflect frontmatter `allowed-tools` list (line 5 of SKILL.md) gains
`WebFetch, WebSearch`. These are required only for `V-Upstream-Available`
lookups and are fail-open per §6.5: when the tool is unavailable, the
classification falls through to `V-Deferred-Outcome` with a runbook entry of
`next_actor: operator, next_instrument: <the missing tool>, next_action:
<re-run the lookup>` — i.e., the deferral itself is a runbook.

### 3.9 Sibling-skill propagation

OVL is wired into reflect first because reflect is the most-evolved audit-class
protocol. Once landed, the other audit-class skills inherit the pattern by
*delegating* their own outcome-verification surface to reflect's contract:

- `sc:auggie-review` already calls reflect-style heuristics; its
  PR-comment formatter renders the OVL summary block.
- `sc:troubleshoot` Wave 6 Phase D already invokes reflect under
  `--type task --validate`; the runbook entries become part of the
  troubleshoot REPORT's "Next steps" section automatically (the docker case
  would have had a `next_action: which docker` row visible at this hop).
- `sc:cleanup-audit` adopts the same `outcome-verification.yaml` artifact
  name without further plumbing.
- `sc:validate-roadmap` treats coverage gaps that depend on upstream
  artifacts (e.g., "this requirement needs library X v2+") as
  `V-Upstream-Available` rows.

The point is that the *artifact shape* is the contract, not the producer-side
plumbing. Any skill that writes a valid `outcome-verification.yaml` participates.

## 4. How it generalizes — five bug shapes

Each shape is a real failure mode the OVL would have caught structurally.

**4.1 OS-level package-split (the docker case).** Wave 1B.4 sees Action 3's
claim "rebuilding will install `/usr/bin/docker`" as depending on the named
package `docker.io`. `V-Upstream-Available` is selected because Debian's
package metadata is reachable (`apt-cache show docker.io` or
WebFetch `packages.debian.org/trixie/docker.io`). The lookup returns
`Depends: containerd, runc, ...` with no `Depends: docker-cli` and no `docker`
binary in the file list. §3.4 promotes the finding to a Regression candidate;
§5.3 rule 3 forces T2; the report ships with `regression_present: true` and
the 10-condition gate blocks promotion. Pre-merge catch.

**4.2 Performance regression (preamble §3 example: worker-pool 4→16).** No
external artifact is named; classification routes to `V-Deferred-Outcome`
because the claim "throughput will not exceed the downstream rate limit" is a
post-deploy property the orchestrator cannot witness. The 1B.4 runbook
entry: `next_actor: ci-gate, next_instrument: bash:k6 run loadtest.js,
expected_witness: p99 < 200ms`. The 10-condition gate passes only if the
runbook is present; the report explicitly hands the verification off rather
than burying it. Operator catches the regression at the next CI run instead
of at the post-deploy 3am page.

**4.3 Third-party API drift (e.g., Stripe Webhook v2025 schema change).** The
diff calls `stripe.events.construct_event(raw, sig, secret)`. Wave 1B.4
classifies as `V-Upstream-Available` with `next_instrument: context7,
next_action: query Stripe SDK 'construct_event signature'`. The context7
lookup returns the current method signature; if it differs from the diff's
call shape, §3.4 contradiction routing fires. No human had to know in advance
to look at Stripe docs — the named-artifact ("stripe") and named-method
("construct_event") trigger the lookup mechanically.

**4.4 Runtime-config integration failure (e.g., new env var X needs to be set
in three places).** The finding "set `RATE_LIMIT_REDIS_URL` in coder agent
config" is V-Repo for the code change (the agent reads the var) but
`V-Deferred-Outcome` for the deployed-config claim. Runbook entry:
`next_actor: operator, next_instrument: shell-on-deploy-target,
next_action: kubectl get configmap coder-agent -o yaml | grep RATE_LIMIT_REDIS_URL,
expected_witness: matches the new URL`. Without OVL, this ships as
`status: success`; with OVL, the deployed-config check is named and tracked.

**4.5 Cross-service contract drift (caller updates API; downstream consumer
still on old contract).** Wave 1B.4 catalogs the API surface change as V-Repo
(the diff itself is clean) but adds a `V-Deferred-Outcome` row for "downstream
consumer service Y still passes the v1 payload shape." `next_actor:
downstream-agent, next_instrument: tier-2-reescalate, next_action: run
sc:reflect --mode post against the consumer repo at HEAD,
expected_witness: consumer's outcome-verification.yaml shows V-Repo for the
new payload field`. This is the structural answer to multi-repo contract
verification — the runbook *names the next reflect run*.

**(Bonus shape.)** Test-suite invariant-violation: a diff that grows test
count but loses an invariant's coverage is V-Repo for the count and
`V-Deferred-Logical` for the invariant question. OVL turns "we did not
check" into a *named* "we did not check," which is the difference.

## 5. Trade-offs and risks

**Token cost.** Step 1B.4 adds an inline classification pass over the
existing finding list — bounded by `len(findings)`, typically 5-20 entries.
The cost is dominated by `V-Upstream-Available` lookups; each is one WebFetch
or context7 call, capped by memoization (`one lookup per distinct artifact`).
For a typical UC-2 reflect with ≤3 external artifacts named, this adds
~1-2k tokens to T1 — inside the preamble §5 envelope. Lookups for
`V-Deferred-*` modes are explicitly skipped (the whole point is that the
orchestrator cannot do them), so there is no runaway tail.

**Wall-clock cost.** WebFetch is the slowest tool (~5-15s per call). With ≤3
artifacts, the added latency is bounded at ~30-45s. Lookups can be batched in
parallel where the orchestrator supports it.

**False-positive risk on `V-Upstream-Available`.** A poorly-disambiguated
artifact name (e.g., "redis" without version) returns a generic doc that
doesn't contradict the diff but also doesn't validate it. Mitigated by
requiring the `evidence_anchor` to be a *specific section* of the upstream
artifact (e.g., a docs URL with anchor, an `apt-cache show` line); failures
fall through to `V-Deferred-Outcome` rather than masquerading as verification.

**Risk: the runbook becomes a "we wrote a TODO" graveyard.** Mitigated by the
10-condition gate: a `V-Deferred-Outcome` row with no `next_action` /
`expected_witness` fails condition 10. Empty runbooks block promotion. The
field schema is enforced at evidence-validator time (§3.6).

**Bug classes OVL still misses.**

1. *Outcome verifications the orchestrator forgets to articulate.* If the
   model fails to identify a finding's outcome axis at all, OVL has nothing
   to classify. Mitigated partially by the §12 grader rubric adding a new
   dimension (see §6 below) and by §4.4's structural pattern (the named
   artifact triggers the classification), but adversarial debate at T2
   remains the ultimate guard.
2. *Runtime-fidelity failures the operator cannot observe with named
   instruments* (e.g., subtle race conditions that need controlled load tests
   the operator doesn't have). OVL surfaces the gap as a runbook with
   `next_actor: operator, next_instrument: <unspecified>`; the operator must
   still do the engineering work to *build* the witness.
3. *Drift in the OVL classifier itself.* If the model class running 1B.4
   systematically under-classifies findings as V-Repo, the gap re-opens. The
   `T2-converges-wrong-answer` falsifier (§12.5) plus a new falsifier case
   (§7 below) operationalize this risk.

**Risk to the §11.0 sufficiency claim.** OVL *strengthens* the conditional
language: post-OVL, the sufficiency claim covers implementation fidelity
*and* upstream-resolvable outcome fidelity, with deferred outcomes explicitly
named. This is a tightening, not a loosening, and slots into §19.2's v1.1
hardening path naturally.

## 6. Backward-compat with existing protocols

**Contract version bump: minor (1.0 → 1.1) per §9.4 rules.** All changes are
additive:

- 8 new top-level fields, all defaulting to documented "absent" values
  (`null`, `0`, `false`) so existing consumers tolerating unknown fields
  (§9.4 forward-compat) are unaffected.
- One new gate condition (cond 10) on the §14.5.2 list. Per §9.3 field-deletion
  guard: this is *additive* and therefore a minor bump. Consumers in the §9.3
  map that read `promotion_gate_passed` continue to work; the new condition
  participates in that boolean automatically. No consumer needs to know about
  cond 10 specifically.
- One new wave step (1B.4) under an existing wave. Wave count unchanged
  (still 7). The per-step audit row format (§4) accommodates it without
  schema change.
- Two new allowed-tools entries (WebFetch, WebSearch). Adding tools is
  additive; existing tool calls unaffected.

**Consumer impact (§9.3 Consumer Field Map).**

- `sc-troubleshoot-protocol` Wave 6: gains `outcome_verified` as an
  optional load-bearing field. If false AND `deferred_outcomes_runbook_present`
  is false, troubleshoot's "next steps" section becomes mandatory. Backward-compat:
  unaware consumers read the legacy fields and miss the runbook, but do not break.
- `superclaude sprint run` executor.py: gains optional sensitivity to
  `outcome_verified == false`. Sprint may choose to halt the phase even when
  `status: success` if a runbook is open. Backward-compat: ignoring the field
  preserves v1.0 sprint behavior.
- `sc:task` end-of-task hook: as above. Existing task-builder Wave 6
  remediation can now consume `outcome-verification.yaml` as a BUILD_REQUEST
  input — the runbook entries map mechanically to MDTM checklist items.
- `sc:roadmap` / `sc:tasklist` validation gates: outcome-verification is
  not load-bearing here; no consumer change.
- Wave 7 promotion adapters: cond 10 added internally. Adapter logic
  inherits.

**Kill-list implication.** §17.7's "5th deviation category was rejected"
entry remains intact — OVL is a *parallel artifact* (the §10.6 pattern), not
a 5th deviation category. The kill list already accepted the
"parallel-artifact-for-representational-gap" pattern once.

**v1.1 deferred-hardening integration.** OVL folds naturally into §19.2's
INV-023 path: the iteration-2 evidence for the
`T2-converges-on-wrong-answer` case can now include outcome-verification
classification accuracy as a sub-criterion, and the v1.1 tightening from
"conditional" to "demonstrated" gains a *broader* sufficiency surface.

## 7. Falsifier (eval case modeled on §12.5)

```yaml
id: outcome-verification-os-package-split
type: held-out adversarial
status: skeleton-pending-iteration-3-fixture   # promoted to active in iteration-3
fixture: fixtures/spec-debian13-docker-install.md
setup: |
  Spec: "Coder workspace must run Docker-in-Docker. Action 3: rebuild
  AIDev02 image so docker.io is installed."
  Diff: Dockerfile.coder adds a 42-line comment block to force
  triggers.dockerfile_sha256 to change. The APT install line already
  contains `docker.io \` and `--no-install-recommends`.
  Tasklist marks Action 3 complete.
  Synthetic prior in reviewer-brief: "the Dockerfile already has
  docker.io in the APT layer; rebuilding will install the docker CLI."

verification_mode_expected:
  - finding_ref: action-3-rebuild
    verification_mode: V-Upstream-Available
    next_instrument: WebFetch | bash:apt-cache show docker.io
    next_action: "Verify Debian 13 docker.io package contains /usr/bin/docker"
    expected_witness: "Package file list contains /usr/bin/docker"

expected_lookup_result: |
  packages.debian.org/trixie/docker.io: file list does NOT contain
  /usr/bin/docker; /usr/bin/docker is in package docker-cli; docker.io
  does not Recommend docker-cli; --no-install-recommends suppresses
  Recommends.

expected_routing: |
  §3.4 contradiction routing fires. Finding promoted to synthetic
  Regression candidate. §5.3 rule 3 forces T2. regression_present: true.
  10-condition gate condition 4 fails (regression > 0). Promotion blocked.

assertion: |
  outcome_contradictions_found >= 1 AND
  regression_present == true AND
  promotion_action == skipped AND
  outcome_ledger_path is not null AND
  outcome_verified == false

severity: |
  AUTO-FAIL if outcome_contradictions_found == 0 OR
  if status == success without a V-Upstream-Available row touching docker.io
  (the OVL is supposed to make the gap representable; missing the row is the
  failure mode the case tests).
```

This case is the **operationalisation of the docker miss** as an eval. It
proves OVL catches the originating bug; it falsifies the proposal if the
classifier under-classifies the finding to V-Repo.

A companion falsifier
`outcome-verification-deferred-runtime-config.yaml` covers §4.4 above —
the V-Deferred-Outcome mode with a mandatory runbook — and asserts that
cond 10 fails when the runbook is empty.

## 8. Out-of-scope items

1. **Live shell-on-deploy-target integration.** The preamble §5 explicitly
   forbids requiring runtime access. OVL surfaces deferred-outcome runbooks;
   it does NOT execute them. Building a `sc:runtime-verify` skill that
   consumes the ledger is a separate proposal.

2. **Auto-rollback on a contradicting upstream lookup.** Cond 10 blocks
   promotion but does not undo a prior promotion. The §19.3 v1.1
   auto-rollback path remains the home for that capability.

3. **Cross-vendor verification of LLM artifact-classifier output.** OVL
   relies on the model classifying a finding's verification mode correctly.
   Hardening this against single-model bias slots into §19.1's INV-021 path
   (vendor heterogeneity); not solved here.

4. **A separate `status` axis (`implementation_status × outcome_status`).**
   Considered and rejected — it would be a major version bump on every
   consumer in §9.3, and `outcome_verified` as a derived boolean carries
   the same routing information at minor-bump cost.

5. **Streaming OVL emission.** §19.4 already defers streaming
   `per_task_verdicts`; OVL inherits the same batch-emit posture. A real
   consumer demanding streaming OVL is the trigger.

6. **External-spec coverage of *every* third-party reference in a diff.**
   The preamble §3 explicitly rejects "fan a tavily query for every package
   named." OVL only invokes `V-Upstream-Available` lookups for findings the
   wave already produced — at most ~5-20 per audit, bounded by memoization.
   The expansion to every imported library is whack-a-mole and out of scope.

7. **Backfilling OVL classification on historical reflect runs.** The
   contract bump is additive; old runs simply emit the new fields as
   absent/zero. Meta-eval (§15.1) treats `outcome_verification_classified:
   false` rows as legitimate pre-1.1 runs.

8. **A new agent class.** §7.2's "no new agents required" posture is
   preserved. The 1B.4 classification is inline orchestrator logic against
   a taxonomy; if eval shows the inline pass is fragile, a future
   `outcome-classifier` agent can be added under the §7.2 extract-on-fragility
   rule, but it is not introduced now.

---

**Word count target check.** This proposal is concrete-first, cites
`/config/.claude/skills/sc-reflect-protocol/SKILL.md` §10.6, §11.0, §11.2,
§14.5.2, §17.7, §19.2 directly, and lands inside the 1500-3500 word band.
