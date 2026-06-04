# Adversarial Debate Transcript

## Metadata
- Depth: standard (Round 1 parallel + Round 2 sequential + Round 2.5 invariant probe + convergence check; Round 3 skipped per default unless convergence < threshold)
- Rounds completed: 2.5 (R1 + R2 + invariant probe; R3 not triggered — convergence met)
- Convergence achieved: 0.91 (21 of 23 diff points resolved; 2 unresolved by formulation but not by content)
- Convergence threshold: 0.80 (default per `--depth standard`)
- Focus areas: structural-coherence, generalizability, mechanism-concreteness, backward-compat-honesty, falsifier-quality
- Advocate count: 2 (Advocate-A for Proposal A "OVM"; Advocate-B for Proposal B "OVL")
- Debate executed inline by orchestrator (analytical synthesis); per-point steelman + critique applied to each Medium-severity diff point + each High-value unique contribution + each promoted shared-assumption

## Round 1: Advocate Statements

### Variant 1 Advocate (Proposal A — OVM)

**Position summary.** OVM is the right name because the central concern is **declaring claims** (what the diff is asserting about behavior, upstream artifacts, runtime state, cross-system contracts), not recording them post-hoc. The manifest pattern matches how the orchestrator actually works: extract claims from spec/tasklist/diff in Wave 1B, verify them in Wave 5, drop or defer per the seat tag. The four-seat axis ("who can verify, from where") is more honest than mode-based axes because it answers the question the user actually has: *can the orchestrator verify this from where it sits?* The toolkit enumeration in §3.2 is what makes this proposal downstream-executable rather than aspirational.

**Steelman of OVL.** Proposal B's "Ledger" name captures the append-only quality and mirrors §10.6's metaphor more cleanly. B's V-Deferred-Logical mode is a real gap A explicitly punted on — second-order reasoning ("does this rebuild change the install-list?") is a category-2 failure that A's seat-based system genuinely cannot represent. B's `outcome_verified` derived field is a clean convenience for consumers that route on a single boolean. B's "artifact shape is the contract" cross-skill approach is lighter-weight than A's new shared-refs directory.

**Strengths claimed (citations from proposal-A.md):**
1. **Concrete external-spec toolkit** (§3.2 lines 107-114): explicit Bash + Skill + WebFetch enumeration with cache directory and 24h staleness rule. B leaves "pick a tool that resolves the contract" to the implementer — A names exactly which tools, in which order, with which fallbacks. Downstream-executable.
2. **Diff-implicit claim extraction with regenerable pattern table** (§3.1 lines 73-74, refs/claim-extraction-patterns.yaml): apt-get / pip / npm / gem / cargo / go get / gh api / aws / terraform patterns. Operators add patterns without SKILL.md edits — extensibility without protocol-text changes.
3. **Per-claim deferred-outcomes file** (§3.2 lines 119-122): `<output>/deferred-outcomes/<claim_id>.yaml` with promotion-alongside semantics. Directly answers preamble §5's "runbook a fresh agent can pick up by ID" requirement.
4. **External-spec cache directory** (§3.2 line 113): handles rate limits, repeatability, network failures with content-sha + timestamp + 24h re-fetch rule. B has no equivalent; relies on per-call memoization that doesn't persist across runs.
5. **Falsifier active in iteration-1** (§7 line 327): the docker miss is a real-world incident, not a hypothetical. Deserves immediate eval coverage, not skeleton-pending-iteration-3 staging.

**Weaknesses identified in OVL (citations from proposal-B.md):**
1. **Toolkit abstraction risk** (§3.3 line 113): "the protocol's allowed-tools surface contains a tool that resolves the artifact's contract" — leaves implementer to pick. Different implementers will pick differently → behavioral drift across runs.
2. **No staleness rule for upstream lookups** (§3.3 entire): memoization is per-call within a run, not across runs. Cached results never freshen, meaning a stale Stripe doc fetched a week ago is treated as authoritative today.
3. **Falsifier deferred** (§7 line 369): docker miss is real; skeleton-pending-iteration-3 delays the empirical proof point that the OVL closes the docker case.

**Concessions (own weaknesses acknowledged):**
- A's seat-based taxonomy genuinely lacks the V-Deferred-Logical concept; this is a gap, not a stylistic choice. Logical-fidelity failures (preamble §2 category 2) need a representational home OVM does not currently provide.
- A's shared-refs directory introduces new infrastructure that has no precedent in the existing skill structure. B's "artifact shape is the contract" approach is simpler.
- A's contract has ~10 new fields vs B's 8+1-derived. The marginal field count is real surface growth.

---

### Variant 2 Advocate (Proposal B — OVL)

**Position summary.** OVL is the right name because the central concern is **representational gap closure** — giving the protocol somewhere to write the unverified-outcome surface so it stops conflating with implementation. The "ledger" metaphor matches the existing §10.6 grounding-gaps pattern exactly (parallel append-only artifact for a representational gap). The four-mode axis ("what verification mode applies") is structurally cleaner because each mode answers a distinct question with distinct downstream implications: V-Repo → already done; V-Upstream-Available → invoke tool now; V-Deferred-Outcome → emit runbook; V-Deferred-Logical → tier-escalation signal. The V-Deferred-Logical mode is the structural answer to category-2 logical fidelity, which OVM punts on.

**Steelman of OVM.** Proposal A's "Manifest" name correctly emphasizes the *declarative* nature of claim extraction (Wave 1B builds the manifest before Wave 5 verifies). A's toolkit enumeration is genuinely more concrete and more downstream-executable than B's classifier-picks abstraction. A's cache directory closes a real freshness/rate-limit gap B glosses over. A's diff-implicit pattern table is a clean extensibility primitive. A's falsifier is more aggressive, which the docker case warrants.

**Strengths claimed (citations from proposal-B.md):**
1. **V-Deferred-Logical mode** (§3.1 line 69, §3.2 line 82): explicit verification mode for "second-order reasoning the audit declines at current tier" with tier-escalation routing. The docker case's mechanism-reasoning gap ("does triggering a rebuild change the install-list?") is exactly this mode. A's seat-based taxonomy has no equivalent.
2. **`outcome_verified` derived field** (§3.5 line 148): single-axis boolean consumers can route on. Reduces consumer-side parsing — `sc-troubleshoot` Wave 6 doesn't need to add up four counts to decide whether to escalate.
3. **"Artifact shape is the contract" cross-skill approach** (§3.9 line 207): no new shared-refs directory; sibling skills participate by writing valid `outcome-verification.yaml`. Lighter, more honest, mirrors how §10.6 grounding-gaps already propagates (no shared-refs directory there either).
4. **Recursive verification handoff** (§4.5 line 256): `next_actor: downstream-agent, next_action: run sc:reflect --mode post against the consumer repo` — turns cross-repo contract verification into a structured handoff, not prose recommendation. Novel pattern.
5. **§19.2 INV-023 hardening integration** (§6 line 314, §6 line 359): OVL strengthens the existing v1.1 sufficiency-claim hardening trajectory — connects this proposal to the deferred-hardening roadmap rather than creating a parallel one.
6. **Empty-runbook policing via cond 10** (§3.7 line 175): runbook with no `next_action` / `expected_witness` fails cond 10 directly. A's evidence-validator extension achieves similar enforcement, but B's gate-level check is more visible and harder to bypass.

**Weaknesses identified in OVM (citations from proposal-A.md):**
1. **Punts on category-2 logical fidelity** (§5 line 261, §8 line 386): A's own trade-off section admits "Category-2 (logical fidelity) failures — OVM does not extract reasoning chains." This is the exact failure mode of the docker case at the mechanism layer (rebuild trigger ≠ install-list change). Punting it is honest but it's the gap OVL specifically closes via V-Deferred-Logical.
2. **New shared-refs directory** (§3.7 line 188): creates a new directory under `/config/.claude/skills/_shared/outcome-verification/` with no precedent. The existing skill structure doesn't have shared-refs; introducing one for one proposal is heavyweight.
3. **Promotion-action enum vs new field** (§3.5 line 143): A keeps `promotion_action` enum stable by adding a parallel field `promotion_deferred_outcomes_count`. This is structurally fine but creates two fields consumers must read to understand "what actually happened in promotion."

**Concessions (own weaknesses acknowledged):**
- OVL's toolkit abstraction (classifier-picks) is less concrete than OVM's enumeration. An implementer reading B alone might not know exactly which tools to invoke for which artifact class.
- OVL has no upstream-cache directory or 24h staleness rule. Cross-run staleness is a real gap.
- OVL's falsifier is skeleton-pending — the docker case is real and could be active immediately.

---

## Round 2: Rebuttals

### Variant 1 Advocate (OVM) responds

**On the V-Deferred-Logical gap:** *Concession reaffirmed.* OVM does not represent category-2 logical fidelity. B's V-Deferred-Logical is the correct representational home for this mode. The merged proposal should adopt it. **Specifically: add V-Deferred-Logical as a fifth seat (or recategorize the four seats as five modes), preserving OVM's seat-based "who-can-verify-from-where" framing for the four runtime/upstream/repo/cross-system axes, with V-Deferred-Logical added orthogonally as a tier-escalation signal.**

**On shared-refs directory:** *Concession.* B's "artifact shape is the contract" is lighter-weight. The merged proposal should drop the new shared-refs directory. Patterns can live in `sc-reflect-protocol/refs/claim-extraction-patterns.yaml` (existing pattern); sibling skills consume the artifact shape, not the patterns ref.

**On promotion-action enum stability:** Standing — A's approach is correct. Keeping the enum stable preserves consumer-side backward-compat. The `promotion_deferred_outcomes_count` companion field is the right additive route.

### Variant 2 Advocate (OVL) responds

**On toolkit abstraction:** *Concession.* A's enumerated toolkit is more downstream-executable. The merged proposal should adopt A's explicit toolkit (apt-cache show, dpkg -L, pip show, npm view, gh api, WebFetch, context7, tavily) as §3.2's verification mechanism, replacing B's classifier-picks abstraction.

**On staleness rule:** *Concession.* A's 24h cache + content-sha + re-fetch is a real upgrade. Merged proposal adopts.

**On falsifier maturity:** *Concession.* Docker case is real; skeleton-pending-iteration-3 staging is unnecessary delay. Merged proposal: falsifier is `status: active` (iteration-1 fixture), retains B's §7 supplementary `outcome-verification-deferred-runtime-config.yaml` skeleton case for the V-Deferred-Outcome mode coverage.

**On `outcome_verified` derived field:** Standing — B's derived boolean is a clean consumer-side convenience and doesn't conflict with A's four-counter fields. Merged proposal: keep all of A's counters AND add B's derived boolean.

---

## Round 2.5: Invariant Probe (fault-finder)

Six-category boundary-condition scan against the emerging consensus (merged proposal direction).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|-----------|--------|----------|----------|
| INV-001 | state_variables | Outcome-claims state persists in `<output>/outcome-claims.yaml` between Wave 1B.4 write and Wave 5 read; no concurrent mutation | ADDRESSED | LOW | A §3.1 + B §3.3 both specify single-writer; reflect is single-process per audit |
| INV-002 | guard_conditions | `--no-install-recommends` is statically detectable from the Dockerfile line `apt-get install -y --no-install-recommends ...` (the orchestrator's parser splits the flag from the package list) | UNADDRESSED | **MEDIUM** | Neither proposal proves the parser handles multi-line `\`-continuations or alternative flag spellings (`--no-install-suggests`, `-o APT::Install-Recommends=false`). Real production Dockerfiles use all three forms. |
| INV-003 | count_divergence | "One implicit claim per matched line" rule (A §3.1) won't duplicate claims when a single `RUN` block has multiple `apt-get install` invocations or when a single install line names multiple packages | UNADDRESSED | LOW | A's pattern table doesn't specify per-package vs per-line granularity; conservative interpretation is per-package, but the proposal doesn't say |
| INV-004 | collection_boundaries | Empty `outcome-claims.yaml` (no claims surfaced) should NOT fail cond 10 (preserves backward-compat with trivial diffs that have no outcome claims) | ADDRESSED | LOW | A §3.5 implicitly: `outcome_claims_failed == 0` is vacuously true when total claims is 0. B §3.7: `outcome_verified == true` is vacuously true when total findings is 0 (no actionable finding lacking verification). |
| INV-005 | interaction_effects | The merged 5-mode taxonomy (4 OVM seats + B's V-Deferred-Logical) cleanly partitions; no claim could be both `V-Deferred-Outcome` AND `V-Deferred-Logical` | UNADDRESSED | **MEDIUM** | A claim like "the rebuild changes the install-list outcome" has BOTH a logical-fidelity question (does the mechanism propagate?) AND a runtime outcome (post-rebuild, is /usr/bin/docker present?). Merged proposal needs a precedence rule: V-Deferred-Logical wins because it's a tier-escalation signal that, if resolved, may collapse the runtime claim to V-Upstream-Available. |
| INV-006 | sufficiency_challenge | Does the merged proposal alone close the docker-cli miss? Concretely: with WebFetch + apt-cache toolkit + 1B.4 extraction + 5.x verification + cond 10 + falsifier eval, would PR #67's audit have failed instead of clean-shipping? | ADDRESSED | LOW | Trace: 1B.4 extracts implicit claim `docker.io_provides_docker_cli` from the `apt-get install ... docker.io` line (A's pattern table); 5.x runs `apt-cache show docker.io` → Recommends shows docker-cli with --no-install-recommends comment; verification_status: failed; promoted to §10.4 Regression; cond 10 fails; promotion blocked. **The sufficiency argument is grounded in A's §4.1 worked example which traces exactly this chain.** |

**Invariant-probe gate verdict:** Two MEDIUM UNADDRESSED items (INV-002, INV-005). No HIGH UNADDRESSED items.

Per §convergence_detection.invariant_probe_gate: **MEDIUM items do NOT block convergence; they are logged as warnings**. The merged proposal must address them in its mechanism text or list them as known limitations in §5 trade-offs.

**Warnings appended to merge contract:**
- INV-002: Merged proposal §3.2 must specify the `--no-install-recommends` detection scope (which flag spellings; multi-line handling) OR list as out-of-scope.
- INV-005: Merged proposal §3.1 must specify the precedence rule for claims that satisfy multiple modes (V-Deferred-Logical > V-Deferred-Outcome when the logical question, if resolved, collapses the runtime claim).

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|-----------|--------|------------|-----------------|
| C-001 (naming) | B | 70% | "Ledger" mirrors §10.6 metaphor; "Manifest" emphasizes declarative side. Both valid; ledger wins on §10.6 alignment |
| C-002 (taxonomy axis) | **MERGE** | 90% | Adopt 5-mode taxonomy: A's 4 seats (in-repo / external-spec / runtime / cross-system) + B's V-Deferred-Logical added orthogonally |
| C-003 (Wave 1B placement) | Either | 100% | Identical |
| C-004 (Wave 5 toolkit) | A | 90% | A's enumerated toolkit with cache directory is downstream-executable; B's abstraction is aspirational |
| C-005 (contract field count) | **MERGE** | 80% | Keep A's per-seat counters AND B's derived `outcome_verified` boolean |
| C-006 (status enum handling) | Either | 80% | Same pattern; B's derived field is the only material delta and already covered in C-005 merge |
| C-007 (promotion-gate cond 10) | **MERGE** | 85% | Cond 10 = `outcome_claims_failed == 0 AND (outcome_verified == true OR deferred_outcomes_runbook_present == true)`. A's failure-floor + B's deferred-with-runbook-pass, both apply |
| C-008 (evidence-validator extension) | **MERGE** | 85% | A's runbook schema validation AND B's row-presence check — complementary, not exclusive |
| C-009 (contradiction routing) | Either | 100% | Same effect, different naming. Merged proposal uses A's `evidence_source` field naming + B's "synthetic Regression candidate" terminology |
| C-010 (cross-skill propagation) | B | 80% | "Artifact shape is the contract" is lighter; no new shared-refs directory. A's ref-driven pattern table stays in `sc-reflect-protocol/refs/` (single-skill) |
| C-011 (allowed-tools) | Either | 100% | Identical |
| C-012 (falsifier maturity) | A | 80% | docker miss is real; `status: active` immediately. Retain B's supplementary V-Deferred-Outcome falsifier as a sibling case |
| U-001 (verifier_tool field) | Take from A | 75% | Useful for audit/debug |
| U-002 (per-claim deferred files + promotion-alongside) | Take from A | 95% | High value; directly answers preamble §5 |
| U-003 (external-spec cache + 24h staleness) | Take from A | 95% | High value; handles real network/rate-limit failures |
| U-004 (diff-implicit pattern table) | Take from A | 90% | High value; extensible without SKILL.md edits |
| U-005 (V-Deferred-Logical mode) | Take from B | 95% | High value; closes the category-2 gap A explicitly punts on |
| U-006 (next_actor: downstream-agent recursive handoff) | Take from B | 80% | Novel; useful for cross-repo |
| U-007 (`outcome_verified` derived field) | Take from B | 80% | Convenience; reduces consumer parsing |
| U-008 (bonus shape) | Take from B | 60% | Generalization bonus; not load-bearing |
| U-009 (§19.2 INV-023 integration) | Take from B | 85% | Connects to existing hardening trajectory |
| A-001 (WebFetch addable without further gate) | Surface in §5 trade-offs | 70% | Both proposals assume; merged proposal should explicitly document the assumption AND a fallback if WebFetch is gated |
| A-002 (operator executes deferred runbooks) | Surface in §5 trade-offs | 75% | Both proposals assume; merged proposal §5 must list as a known limitation |
| A-003 (apt-cache parser robustness) | Surface in §3 mechanism | 75% | INV-002 caught this; merged proposal §3.2 must specify scope |

## Convergence Assessment

- Points resolved: 21 of 23 (12 content + 9 unique; 0 structural — all Low — auto-resolved; 0 contradictions; 2 shared-assumption diffs A-001+A-002 resolved by §5 trade-off documentation; A-003 resolved by §3 mechanism specification)
- Unresolved: 0 hard contentions; both Medium-severity items (INV-002, INV-005) require mechanism-text additions in merged proposal but do not block convergence
- Alignment: **91%** (21/23)
- Threshold: 80%
- Status: **CONVERGED**
- Taxonomy coverage gate: L1 (naming, status enum) covered; L2 (taxonomy axis, contract fields, cross-skill propagation) covered; L3 (state mechanics — gate cond, validator scope, classification precedence) covered. **All levels covered.**
- Invariant-probe gate: 0 HIGH UNADDRESSED. Convergence permitted.
- Round 3 not triggered (convergence ≥ threshold).
