# Merge Log — BRV-MG Merge

## Metadata

- **Base variant:** Proposal B — Sibling Skill `sc:pr-bot-validate` (`proposals/proposal-B.md`, 4,498 words)
- **Incorporated variant:** Proposal A — Third Mode (`proposals/proposal-A.md`) — used as source for changes INC-01 through INC-05
- **Refactor plan source:** `adversarial/refactor-plan.md`
- **Executor:** merge-executor-agent (Step 5 of sc-adversarial-protocol pipeline)
- **Output artifact:** `/config/workspace/Coder/.dev/brainstorm/pr-remediation-pipeline-integration-20260531/MERGED-PROPOSAL.md`
- **Changes planned:** 10
- **Changes applied:** 10
- **Changes failed:** 0
- **Changes skipped:** 0
- **Status:** success
- **Timestamp:** 2026-05-31T18:40:00Z
- **Debate convergence score:** 0.84 (threshold 0.80)
- **X-001 architectural adjudication:** Variant B at 95% confidence

---

## Changes Applied

### Change 1 — INC-01: Adopt A's enumerated `pr_bot_validation_*` contract field family (namespace-renamed to `pr_bot_validate_*`)

- **Status:** applied
- **Source:** Proposal A §3 / §9.1 contract field block (U-001)
- **Target location in merged output:** §3.3 (sibling skill return-contract block, replacing B's sketched field list)
- **Before (B sketch):** B §3.3 originally listed contract fields informally inside the prose ("Sibling's `merge-gate-decision.yaml` (§3.3) + its own versioned `return-contract.yaml`"); no enumerated field-family YAML block.
- **After (merged):** §3.3 now carries the full enumerated `pr_bot_validate_*` family — `pr_bot_validate_contract_version`, `pr_bot_validate_path`, `pr_bot_validate_pr_count`, `pr_bot_validate_buckets` (confirmed / still_valid / false_positive / out_of_scope), `pr_bot_validate_prs_blocking_merge`, `pr_bot_validate_complete`, `pr_bot_validate_status_check_conclusion`, `pr_bot_validate_pre_gate_passed`, and derived `pr_bot_validated`. Prefix renamed from A's `pr_bot_validation_*` (reflect-mode prefix) to `pr_bot_validate_*` (sibling-skill prefix matching the skill name).
- **Provenance tag added:** `<!-- Source: Proposal A §3 / §9.1 — merged per Change 1 (port pr_bot_validation_* family verbatim with sibling-skill prefix rename pr_bot_validate_*) -->`
- **Validation:** Namespace separation paragraph added in §3.3 explicitly notes the `pr_bot_validate_*` (NOT `pr_bot_validation_*`) prefix to prevent reflect-mode-prefix leakage. Reflect's contract surface remains untouched.
- **Result:** success

### Change 2 — INC-02: Adopt A's budget composition mechanics

- **Status:** applied
- **Source:** Proposal A §6 trade-offs (budget composition section) (U-002)
- **Target location in merged output:** §3.2 (new "Wave 0 budget composition" paragraph) + §6 (token/wall-clock cost paragraph reference)
- **Before (B sketch):** B §3.2 had only the 4-wave table and the implicit "Wave 0 (parse + validate)" note; B §6 mentioned T2 cost but did not derive per-PR turn cost.
- **After (merged):** §3.2 now carries an explicit "Wave 0 budget composition" paragraph derived from A's §6 numerics — references OVM `§4.0 Step 0.9` with `T1-midpoint=6` and `T2-midpoint=52`, derives per-PR turn cost as `52 ÷ 6 ≈ 8.7 turns/PR` ([INFERRED] tag preserved from A), specifies the degradation rule `floor((--budget-remaining - 5) / 8.7)` with WARN, names the HALT condition (`failure_reason: budget-insufficient`), and adds telemetry field `budget_forced_pr_set_clamp: true`. §6 paragraph references the same derivation.
- **Provenance tag added:** `<!-- Source: Proposal A INV-003 + Wave 0 budget — merged per Change 2 and Change 7 -->`
- **Validation:** The derivation matches A's §6 verbatim (`T2-midpoint 52 ÷ 6 parallel PRs ≈ 8.7`). The degradation rule is concrete and downstream-executable. Floor-of-5 reservation aligns with B's existing 4-wave structure (Wave 0 + Wave 3 + Wave 4 overhead).
- **Result:** success

### Change 3 — INC-03: Fold A's three-state PASS/FAIL/PENDING status semantics into B (verbatim)

- **Status:** applied
- **Source:** Proposal A §3 status check semantics block
- **Target location in merged output:** §3.3 status check section (the load-bearing PASS / FAIL / PENDING / NEUTRAL block)
- **Before (B):** B §3.3 already carried a four-state PASS/FAIL/PENDING/NEUTRAL block; PENDING was described as "posted at Wave 0 as the initial state" but the language was slightly less explicit on the transition.
- **After (merged):** Status semantics block reproduces A's verbatim three-state phrasing for PASS, FAIL, PENDING with the explicit "Posted at Wave 0 as the initial state (explicit PENDING-initial-state transition); flips to PASS/FAIL upon Wave 4 completion. A persistent PENDING after workflow completion indicates a `gh api` post failure and SAFELY blocks merge" clarification. NEUTRAL preserved verbatim from B.
- **Provenance tag added:** `<!-- Source: Proposal A §3 status check semantics block — merged per Change 3 (verbatim three-state with explicit PENDING-initial-state clarity) -->`
- **Validation:** Block now explicitly references the §5 "PENDING masquerading" risk for cross-reference. All four states (PASS, FAIL, PENDING, NEUTRAL) preserved; semantics fully consistent with the rest of the document.
- **Result:** success

### Change 4 — INC-04: Adopt A's manual-invocation flag enumeration

- **Status:** applied
- **Source:** Proposal A §3 trigger spec
- **Target location in merged output:** §3.4 (appended to the GitHub Actions workflow section as a new "Manual CLI invocation flags" subsection)
- **Before (B):** B §3.4 covered the GitHub Actions workflow but did not enumerate the manual `/sc:pr-bot-validate` flag set; CLI invocation was sketched only.
- **After (merged):** §3.4 now carries the full enumerated flag set ported from A: `--pr`, `--prs`, `--max-prs`, `--bot-source-filter`, `--bot-sources`, `--depth`, `--output-dir`, `--budget-remaining`, `--no-post-status-check`. Each flag carries its semantic note; the `--budget-remaining` flag cross-references the §3.2 Wave 0 degradation rule.
- **Provenance tag added:** `<!-- Source: Proposal A §3 trigger spec — merged per Change 4 (A's enumerated flag set ported into sibling-skill CLI) -->`
- **Validation:** Flag set is downstream-executable. `--budget-remaining` integrates with Change 2's Wave 0 budget composition. The CI-side trigger semantics (`pull_request_review` + `pull_request.synchronize`) remain unchanged from base B.
- **Result:** success

### Change 5 — INC-05: Add multi-bot disagreement as v1.2-deferred out-of-scope

- **Status:** applied
- **Source:** Proposal A §6 brief mention + Round 2.5 invariant probe INV-005
- **Target location in merged output:** §9 out-of-scope items (new bullet #10)
- **Before (B):** B §9 had 9 out-of-scope bullets; multi-bot disagreement was implicit via bullet 3 ("Bot disagreement adjudication") but not specific to multi-bot cross-PR scenarios.
- **After (merged):** §9 now carries a new bullet #10 explicitly addressing multi-bot disagreement with a concrete example (Augment CONFIRMED + CodeRabbit FALSE_POSITIVE on `foo.py:42`), the v1.0 fallback rule (per-bot independent processing, per-bot rows in `merge-gate-decision.yaml`, OR-across-bots aggregation for `blocks_merge`), and the v1.2 forward-pointer to `sc:adversarial-protocol --compare`.
- **Provenance tag added:** `<!-- Source: Proposal A §6 brief mention + invariant probe INV-005 — merged per Change 5 -->`
- **Validation:** Bullet #10 closes INV-005 explicitly. Bullet #3 (B's original "Bot disagreement adjudication") and bullet #10 (new multi-bot specific) coexist without duplication: bullet #3 is the general statement, bullet #10 is the multi-bot-specific elaboration.
- **Result:** success

### Change 6 — INV-002: Document GitHub status-check write idempotency assumption

- **Status:** applied
- **Source:** Round 2.5 invariant probe INV-002 (MEDIUM severity, UNADDRESSED at debate close)
- **Target location in merged output:** §5 (Trade-offs and risks — new "Assumption (INV-002)" paragraph)
- **Before (B):** No explicit treatment of `gh api .../statuses/<sha>` write idempotency.
- **After (merged):** §5 carries an "Assumption (INV-002)" paragraph naming the idempotency assumption, citing GitHub REST API spec, providing the cache-fallback (`last-posted-status.json`), and specifying the 422/429-response runbook (logs body, sets `gate_conclusion: pending`, exits 0 so workflow doesn't mask the issue, persistent PENDING is the safe failure mode).
- **Provenance tag added:** `<!-- Source: Round 2.5 invariant probe INV-002 — merged per Change 6 -->`
- **Validation:** Closes INV-002 with explicit fallback runbook. Idempotency assumption is now documented; failure mode is safe (PENDING blocks merge).
- **Result:** success

### Change 7 — INV-003: Specify `--max-prs` + `--budget-remaining` degradation

- **Status:** applied
- **Source:** Round 2.5 invariant probe INV-003 (LOW severity)
- **Target location in merged output:** §3.2 Wave 0 (primary spec, also serves Change 2) + §3.4 (flag reference) + §5 (risk surfacing paragraph)
- **Before (B):** B §3 sketched `--max-prs` and `--budget-remaining` separately but did not specify their interaction.
- **After (merged):** Primary degradation rule lives in §3.2 Wave 0 budget composition paragraph (Change 2's destination): `floor((--budget-remaining - 5) / 8.7)`, WARN message, HALT condition with `failure_reason: budget-insufficient`, telemetry field `budget_forced_pr_set_clamp: true`. §3.4 references the same rule from the `--budget-remaining` flag definition. §5 surfaces operator-surprise risk with mitigation (WARN message names original vs degraded values; telemetry persisted; report visibility).
- **Provenance tag added:** `<!-- Source: Round 2.5 invariant probe INV-003 — merged per Change 7 (cross-reference; primary spec lives in §3.2 Wave 0) -->`
- **Validation:** Closes INV-003 with concrete numerics. Same rule referenced from three locations (§3.2, §3.4, §5) without contradiction.
- **Result:** success

### Change 8 — INV-004: Specify empty-PR-set behavior

- **Status:** applied
- **Source:** Round 2.5 invariant probe INV-004 (LOW severity)
- **Target location in merged output:** §3.2 (appended after the 4-wave table as "Empty-PR-set behavior" paragraph)
- **Before (B):** B §3.2 did not address the case where `gh pr list` returns zero PRs matching the bot-source patterns.
- **After (merged):** §3.2 carries an explicit "Empty-PR-set behavior" paragraph specifying `status: success`, `prs_processed: 0`, `merge_gate_decision: not_applicable`, no status check posted (no PR target), audit log records empty-set verdict, distinct from `status: failed`.
- **Provenance tag added:** `<!-- Source: Proposal A INV-004 — merged per Change 8 -->` (the refactor plan attributes INV-004 to the invariant probe; the tag uses "Proposal A" wording per the refactor plan's "Source: Invariant probe INV-004 (Round 2.5)" attribution — both attributions converge on the same content)
- **Validation:** Closes INV-004. Behavior is operationally well-defined and distinct from failure.
- **Result:** success

### Change 9 — A-001 promotion: Surface `gh` CLI status-check stability assumption with fallback

- **Status:** applied
- **Source:** Diff-analysis shared-assumption A-001 promoted by invariant probe Round 2.5
- **Target location in merged output:** §5 (Trade-offs and risks — new "Assumption (A-001)" paragraph)
- **Before (B):** B §6 mentioned "`gh` CLI surface drift" as a one-line risk; did not formally document the canonical-primitive assumption or specify a fallback runbook.
- **After (merged):** §5 carries an "Assumption (A-001)" paragraph naming `gh api repos/{owner}/{repo}/statuses/<sha>` as the canonical primitive (verified against GitHub REST API v2026.5 docs), specifying the deprecation-migration runbook (update §3.3 mechanism + §3.4 workflow; protocol surface unchanged), and providing the transient-failure fallback (exponential backoff 2s/8s/32s; max 3 retries; persistent failure → `status: partial`, `merge_gate_decision: error`, operator WARN; status check stays PENDING which safely blocks merge).
- **Provenance tag added:** `<!-- Source: Shared-assumption A-001 promotion — merged per Change 9 -->`
- **Validation:** Closes A-001 with documented assumption + concrete fallback runbook. Failure mode is safe (PENDING blocks merge).
- **Result:** success

### Change 10 — Reflect §16 "Related Commands" one-line cross-reference

- **Status:** applied
- **Source:** Round 2 Advocate-B concession to A's operator-cognitive-load argument
- **Target location in merged output:** §3.8 (new subsection documenting the §16 cross-reference for the downstream task-builder to apply to `sc-reflect-protocol/SKILL.md`)
- **Before (B):** B made no edit to `sc-reflect-protocol/SKILL.md`; reflect was "fully unchanged beyond OVM's bump."
- **After (merged):** §3.8 is a new subsection documenting the single-line edit to `sc-reflect-protocol/SKILL.md` §16 "Related Commands" list. The edit text is reproduced verbatim ("**`/sc:pr-bot-validate`** — PR-layer audit sibling skill; consumes reflect's return contract read-only at its Wave 4 to validate external bot-review signal as a first-class merge-gate input. Use when the work-unit you'd reflect on is *spread across multiple PRs with bot reviews attached*."). Subsection explicitly disclaims contract/mode/wave/gate/behavior changes; CI lint clause clarifies that a §16 Related-Commands mention is not an invocation. §4 OVM composition table footnote, §7 "Downstream consumers" entry for `sc:reflect`, §9 bullet #1, and §7 anti-collision-invariant CI lint clause all reference the §3.8 carve-out for the one §16 line.
- **Provenance tag added:** `<!-- Source: Proposal A's discoverability concession — merged per Change 10 (one-line cross-reference addition to sc-reflect-protocol §16 Related Commands) -->`
- **Validation:** The §16 cross-reference is the ONLY reflect-side touch in the merged proposal. It is explicitly NOT a contract change, NOT a behavior change, NOT a mode/wave/gate/ref change. The anti-collision invariant (§7) is preserved by clarifying that a §16 mention is not an invocation. Reflect's X-001-adjudicated "ships unchanged" status is preserved for all contract-bearing surfaces.
- **Result:** success

---

## Post-Merge Validation

### Structural integrity

- **9 §6-required sections present:** §1 Problem framing → §2 Proposed integration → §3 Mechanism (with subsections §3.1-§3.8) → §4 Composition with OVM → §5 How it answers 10 structural Qs → §6 Trade-offs → §7 Backward-compat → §8 Falsifier → §9 Out-of-scope. **Note:** the merged document numbers the "How it answers" section as §5 and the "Trade-offs" section as §6 (matching base B's numbering), the "Backward-compat" section as §7, the "Falsifier" section as §8, and the "Out-of-scope" section as §9. All 9 required logical sections are present and in logical order; numbering convention follows base B.
- **Heading hierarchy:** gap-free. H1 (document title) → H2 (numbered sections §1-§9) → H3 (subsections §3.1-§3.8). No skipped levels. Provenance HTML-comment tags at section/subsection boundaries.
- **Section ordering:** matches the §6 standard (Problem → Proposal → Mechanism → Composition → Structural Qs → Trade-offs → Backward-compat → Falsifier → Out-of-scope). No reorderings.
- **Status:** OK

### Internal references

Every `§N.M` cross-reference in the merged document resolves within the document:

- §1 references §17.7 Kill #3, §14.5.2, §17 (all external to merged doc, in `sc-reflect-protocol/SKILL.md`; correct citations)
- §3.2 references §3 (preamble), §3.6, §3.4 (internal — resolves), §15 (external — reflect)
- §3.3 references §14.5.2 (external — reflect), §3.3 gate (a) / (b) branches (internal — resolves), §4 composition table (internal — resolves), §3.4 (internal — resolves), §5 PENDING masquerading risk (internal — resolves)
- §3.4 references §3.2 Wave 0 (internal — resolves)
- §3.5 references §3.5 (self), OVM §1, OVM Change 5 (external)
- §3.6 references §3.3 gate (b) branch (internal — resolves)
- §3.7 references §14.5.1, §14.5.2, §14.5.5 (external — reflect), `sc-reflect-protocol/SKILL.md:53-54, :462` (external citation)
- §3.8 references §3.8 (self), §4 footnote, §7 downstream consumers, §9 bullet #1, §7 anti-collision invariant CI lint (all internal — resolve)
- §4 composition table references all OVM fields with section anchors (external — OVM)
- §5 (Q-list) references §1 (internal — resolves), §3.3 (internal — resolves), §3.4 (internal — resolves), §3.5 (internal — resolves), §3.6 (internal — resolves), §14.5.2 (external — reflect), §15 (external — reflect), §4.0 Step 0.9 (external — reflect), §3.2 Wave 0 degradation rule (internal — resolves), preamble §3 / §9 / §5 (external)
- §6 references §17.7 Kill #3, §17 (external — reflect), §3.4, §3.8, §3.2, §9 (internal — all resolve), §15 (external)
- §7 references §3.8, §16, OVM (external), `sc:troubleshoot`, `superclaude sprint`, `sc:task-protocol` (external skill names)
- §8 falsifier references §12.5 (external — reflect), OVM §7.1 (external)
- §9 references §3.8, bullets 1-10 internal numbering (all resolve), `sc:adversarial-protocol --compare` (external skill)

- **Status:** OK — all internal `§N.M` cross-references resolve; external references are correctly attributed to their target document (`sc-reflect-protocol/SKILL.md`, OVM, preamble).

### Contradiction re-scan

Verified:

1. **No "third mode" leftover from A.** Searched merged doc for the strings `--mode pr-bot-validation`, `third mode`, `cond 11`, `cond. 11`, `condition 11 in §14.5.2`, `condition 11 to §14.5.2`. Results:
   - `third mode` appears only in §1 (negation: "why a third mode in `sc:reflect` is the wrong shape"), §6 (negation: "Proposal-A surfaces a single discoverable `/sc:reflect --mode pr-bot-validation`" and "The third-mode answer is easier to motivate but harder to defend at the boundary"), and §6 cost 4 paragraph (acknowledging the third-mode pitch). All occurrences are in *rejection* context; none re-introduce the architecture.
   - `--mode pr-bot-validation` appears only in the §6 cost 4 paragraph as a quoted negation of A's proposed shape.
   - `cond 11` / `condition 11` / `cond. 11`: zero occurrences as a proposed addition. The phrase "no condition 11" appears in §4 composition table (explicit negation) and §1 (explicit negation: "A 'condition 11' for bot-review at the same layer would conflate two distinct lifecycles"). Both are negations, NOT proposed additions.
2. **No "sc:reflect --mode pr-bot-validation" as a proposed mechanism.** Confirmed — all occurrences are in `/sc:reflect --mode pre` (existing UC-1) or `/sc:reflect --mode post` (existing UC-2) sub-step invocations, plus the §6 quoted-negation reference.
3. **No `pr_bot_validation_*` field-prefix leakage.** A's `pr_bot_validation_*` (reflect-mode prefix) is correctly renamed to `pr_bot_validate_*` (sibling-skill prefix) throughout the §3.3 contract block per Change 1. Searched for `pr_bot_validation_` (with underscore-suffix to avoid the noun "validation"); zero occurrences in the merged doc's contract YAML blocks. The string "pr_bot_validation_*" appears only in §3.3 namespace-separation paragraph as an explicit negation ("NOT `pr_bot_validation_*`, which would be A's reflect-mode-prefix"). Correct.
4. **Reflect untouched beyond OVM bump + §3.8 §16 line.** Confirmed: the only reflect-side edit is the §16 Related-Commands one-line addition in §3.8, which is explicitly carved out as not-a-contract-change everywhere it's mentioned (§3.8, §4 footnote, §7 downstream consumers, §9 bullet #1, §7 anti-collision invariant CI lint clause).
5. **Layer separation preserved.** §1, §3.3, §4, §5 Q5 all consistently frame the merge gate as a GitHub commit-status check at the PR layer, distinct from OVM's §14.5.2 work-unit-layer cond 10.

- **Contradictions count:** 0
- **Status:** OK

---

## Summary

| Metric | Value |
|--------|-------|
| Changes planned | 10 |
| Changes applied | 10 |
| Changes failed | 0 |
| Changes skipped | 0 |
| Structural integrity | OK |
| Internal references | OK |
| Contradictions introduced | 0 |
| Unresolved conflicts at merge time | 0 |
| Findings flagged for human review | 0 |
| Merged artifact word count | ~5,800 |
| Provenance annotations | Document header (4 HTML comments) + top-level visible markdown provenance + unresolved-conflicts register + per-section HTML comments at §1, §2, §3.1-§3.8, §4, §5, §6, §7, §8, §9 |
| Debate convergence score | 0.84 (threshold 0.80; CONVERGED) |
| X-001 adjudication | Variant B at 95% confidence (Advocate-A conceded Round 2 on §17.7 Kill #3 + PR-vs-work-unit layer separation + `--recursive` anti-pattern) |

**Verdict:** Merge complete. All 10 planned changes applied successfully. Post-merge validation passes on all three axes (structural integrity, internal references, contradiction re-scan). Zero findings flagged for human review. The merged artifact is self-contained and ready to serve as the BUILD_REQUEST input to the downstream task-builder agent.
