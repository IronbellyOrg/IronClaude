<!-- Provenance: This document was produced by /sc:adversarial via /sc:brainstorm -->
<!-- Base: Proposal B (Sibling Skill `sc:pr-bot-validate`) -->
<!-- Merge date: 2026-05-31T18:40:00Z -->
<!-- Non-base sources incorporated: Proposal A (Third Mode) for changes INC-01 through INC-05 -->

# Bot-Review-Validated Merge Gate (BRV-MG) via the Sibling Skill `sc:pr-bot-validate`

> **Provenance:** Merged unified proposal produced by `/sc:adversarial` from two independently-authored brainstorm variants. **Base variant:** Proposal B "Sibling Skill `sc:pr-bot-validate`" (4,498 words, structurally-correct architecture per X-001 adjudication). **Incorporated variant:** Proposal A "Third Mode" — five downstream-executable refinements ported into B's contract surface (contract field family, budget composition, status-check semantics, CLI flag enumeration, multi-bot deferral). **Change count:** 10 applied (5 incorporations from A + 4 invariant-probe mechanism-text additions + 1 reflect-§16 discoverability cross-reference). **Debate convergence score:** 0.84 (threshold 0.80). **Key debate-decisive moment:** the X-001 architectural contradiction was adjudicated to Variant B at 95% confidence after Advocate-A's explicit Round-2 concessions on (i) `sc-reflect-protocol/SKILL.md` §17.7 Kill #3 (identity dilution), (ii) PR-layer vs work-unit-layer separation, and (iii) the `--recursive` anti-pattern in reflect §17 "Will Not" #1.
>
> **Unresolved conflicts:** 0. The X-001 architectural contradiction was adjudicated to Variant B (sibling skill) at 95% confidence after Advocate-A's explicit Round-2 concessions on §17.7 Kill #3, PR-vs-work-unit layer separation, and the `--recursive` anti-pattern. Two shared-assumption diff points (A-001 `gh` CLI stability + Round 2.5 INV-002 idempotency) are surfaced as documented assumptions in §5 with fallback runbooks.

---

<!-- Source: Base (original) -->
## 1. Problem framing — why a third mode in `sc:reflect` is the wrong shape

The BRV-MG preamble §9 leaves an explicit exception open: *"Don't propose a new top-level skill unless you can prove `sc:reflect` is the wrong home."* The strong default would be a third mode (e.g., `--mode pr-bot-validation`) sitting alongside `--mode pre` (UC-1) and `--mode post` (UC-2). I take the exception seriously and argue from first principles that the right home is **not** inside `sc:reflect`. The instinct is wrong for four converging reasons:

**1. Identity dilution against the protocol's own kill-list.** `sc-reflect-protocol/SKILL.md` §17.7 Kill #3 rejects streaming/interactive reflection dialogue with the rationale: *"Adding interactive dialogue would duplicate brainstorm's Wave 1 and dilute reflect's identity as a validation tool."* The same logic applies here. The 6-way pipeline in preamble §3 is not a *verification*; it is a **PR-scoped lifecycle orchestration** — discover PRs, fan out across PRs, cross-validate bot critiques against current HEADs, amalgamate, *then* call reflect's existing `--mode pre` on the aggregated proposals (Phase 4), *then* hand off to `task-builder` + `/task` + reflect's `--mode post` (Phase 5). Reflect is **already called twice as a sub-step** inside this pipeline. The pipeline is structurally an **orchestrator over reflect**, not a peer mode of it. Putting the orchestrator inside the thing it orchestrates inverts the dependency arrow and creates a recursion surface reflect's `--recursive` flag (§17 "Will Not" #1) explicitly guards against.

**2. Scope mismatch in the verification unit.** Reflect's UC-1 and UC-2 are **work-unit-scoped**: spec + tasklist (UC-1), or tasklist + diff against HEAD (UC-2). The promotion mutation in §14.5 moves a *single work-unit folder* (`.dev/tasks/to-do/TASK-NNN/` → `.dev/tasks/done/TASK-NNN/`). The 6-way pipeline is **PR-scoped**: it discovers up to 6 PRs from `gh pr list`, spawns one subagent per PR, and produces a single aggregated `PROPOSALS-normalized.md` covering 6 distinct PRs whose tasklists may not even exist. Reflect's adapter table in §14.5.1 has no PR-level adapter and shouldn't grow one — promotion semantics for a PR (merge / close / request-changes) are categorically different from `mv` of a tasklist folder.

**3. Layer collision with OVM's promotion gate.** OVM (the v1.0 → v1.1 proposal landing in the same release) adds *condition 10* to the §14.5.2 promotion gate at the **work-unit layer** (`outcome_claims_failed == 0 AND (outcome_verified == true OR deferred_outcomes_runbook_present == true)`). A "condition 11" for bot-review at the same layer would conflate two distinct lifecycles. The right composition is a **separate gate at the PR layer**, surfaced as a GitHub branch-protection status check, not a row in `promotion-log.yaml`. OVM gates `mv` of a tasklist folder; this proposal gates `gh pr merge` of a PR. Both are merge gates, but they merge different things.

**4. The pipeline already names reflect as a sub-step.** Preamble §3 Phase 4 says verbatim: `/sc:reflect --mode pre --spec <aggregated PROPOSALS-normalized.md>`. Phase 5 Variant A says verbatim: `/sc:reflect --mode post --diff <pre-task-ref>..HEAD --tasklist <mdtm-file>`. Both are existing reflect modes used unmodified. If reflect's existing two-mode surface is **already sufficient** to be the audit primitive that the orchestrator calls, the orchestrator doesn't need to *become* a reflect mode — it needs to *invoke* reflect modes. That is the literal definition of a sibling skill in the SuperClaude protocol surface (cf. `sc:troubleshoot` Wave 6 Phase B/D, which invokes reflect twice as a sub-step per `sc-reflect-protocol/SKILL.md:53-54`).

The structural fix is therefore a **sibling skill `sc:pr-bot-validate`** that owns the 6-way pipeline as a first-class protocol surface, composes with OVM through reflect's existing return contract, and surfaces its verdict as a **GitHub status check** that branch protection consumes — the canonical first-class merge gate on GitHub.

---

<!-- Source: Base (original) -->
## 2. Proposed integration — `sc:pr-bot-validate` as PR-layer audit sibling

**Named central design:** *Bot-Review-Validated Merge Gate via the Sibling Skill `sc:pr-bot-validate`* — a new audit-class skill peer to `sc:reflect`, `sc:auggie-review`, `sc:cleanup-audit`, and `sc:troubleshoot`, that owns the 6-way PR-bot-validation pipeline end-to-end and emits a GitHub commit-status check (`sc-pr-bot-validate / merge-gate`) that GitHub branch protection consumes. The skill **consumes reflect's v1.1 (OVM) return contract** as its grounding primitive at Phase 4 and Phase 5; reflect itself gains zero new modes, zero new gate conditions, zero new wave steps. The sibling skill is invoked by a thin `/sc:pr-bot-validate` command and is auto-triggerable by a `.github/workflows/pr-bot-validate.yml` GitHub Action.

The skill lives at `src/superclaude/skills/sc-pr-bot-validate-protocol/SKILL.md` per the established skill layout. Its return contract is **versioned independently** (`pr_bot_validate_contract_version: 1.0`) and is *additively* coupled to OVM's `outcome_verified` derived boolean via a single read of reflect's return-contract.yaml during Phases 4 and 5. There is no two-way binding: reflect knows nothing about this skill.

This direction commits explicitly to:

- **Zero new modes in `sc:reflect`** — reflect ships as v1.1-OVM, full stop.
- **One new sibling skill** — `sc-pr-bot-validate-protocol`, modeled on `sc-auggie-review-protocol`'s shape (frontmatter + 4-wave pipeline + return contract).
- **One new GitHub Actions workflow** — `.github/workflows/pr-bot-validate.yml` that is the actual mechanism that gates merge via branch protection.
- **One new ref file in the new sibling skill** — `refs/bot-review-sources.yaml` enumerating the bot detection patterns (per preamble §9 "Don't propose maintaining the bot-detection pattern table in SKILL.md prose").

---

## 3. Mechanism — concrete protocol-text amendments

<!-- Source: Base (original) -->
### 3.1 New skill: `sc-pr-bot-validate-protocol`

Created at `src/superclaude/skills/sc-pr-bot-validate-protocol/SKILL.md`. Synced to `.claude/skills/` via `make sync-dev` per CLAUDE.md global rule 6. Frontmatter (modeled on `sc-auggie-review-protocol/SKILL.md` lines 1-10):

```yaml
---
name: sc:pr-bot-validate-protocol
description: "Validate external bot-review signal (Augment Code, CodeRabbit, etc.) against current PR HEAD via the 6-way parallel cross-validation pipeline; emit a GitHub status check that branch protection consumes as a first-class merge gate."
allowed-tools: Read, Grep, Glob, Bash(gh *), Bash(git *), Bash(jq *), Bash(mkdir *), Bash(date *), Bash(wc *), TodoWrite, Task, Write, Edit, Skill
---
```

The skill is invoked ONLY by the `/sc:pr-bot-validate` command or by the GitHub Action (§3.4). It is NEVER invoked by `sc:reflect` (cf. preamble §9 anti-recursion stance: reflect should not call this skill back).

<!-- Source: Base (modified) — Change 8: append empty-PR-set behavior per INV-004 -->
### 3.2 The 4-wave pipeline (verbatim mapping of preamble §3's 5 phases)

The pipeline in preamble §3 has 5 phases. They map onto 4 waves in the new skill (Phase 5 belongs in a downstream skill — see §3.6):

| Pipeline Phase (preamble §3) | sc:pr-bot-validate Wave | Behavior |
|---|---|---|
| Phase 1 — Discover PR set | **Wave 1 — PR discovery** | `gh pr list --state open --limit <N> --json number,title,headRefName,author,reviews`; filter by `refs/bot-review-sources.yaml` patterns; cap at `--max-prs` (default 6). |
| Phase 2 — Spawn 6 parallel agents | **Wave 2 — Parallel cross-validation** | One `Task` agent per discovered PR; each invokes `Skill sc-auggie-review-protocol` with `--no-post-pr --no-remediation-offer --depth standard --output-dir /tmp/pr-<N>-auggie-fresh/`; each writes `/tmp/remediation-pr-<N>.md` and returns the ≤120-word summary verbatim. |
| Phase 3 — Amalgamate | **Wave 3 — Aggregation** | Read each `/tmp/remediation-pr-<N>.md`; write `<output>/PROPOSALS.md` and `<output>/PROPOSALS-normalized.md` per the §3 templates verbatim. |
| Phase 4 — Validate proposals | **Wave 4 — Reflect-grounded validation** | `Skill sc-reflect-protocol --mode pre --spec <output>/PROPOSALS-normalized.md --depth standard`. Read the returned `return-contract.yaml`; promote/reject based on the §3.3 gate. |
| Phase 5 — Execute remediation | *out-of-scope for this skill* | Phase 5 is operator-driven (per preamble §9 "Don't propose auto-execution of remediation"). The skill's return contract surfaces the remediation handoff target; the operator runs `task-builder` + `/task` themselves. See §9. |

Wave 0 (parse + validate) is implicit and mirrors `sc-auggie-review-protocol`'s prereq pattern.

<!-- Source: Proposal A INV-004 — merged per Change 8 -->
**Empty-PR-set behavior.** If `gh pr list` returns zero PRs matching the `refs/bot-review-sources.yaml` patterns, the skill exits cleanly with `status: success`, `prs_processed: 0`, `merge_gate_decision: not_applicable`. No status check is posted (there is no PR target). Audit log records the empty-set verdict. This is the explicit operational success state — distinct from `status: failed`.

<!-- Source: Proposal A INV-003 + Wave 0 budget — merged per Change 2 and Change 7 -->
**Wave 0 budget composition.** Wave 0 routes per the same table OVM defines in `§4.0 Step 0.9` (reflect's existing budget pre-flight semantics, with `T1-midpoint=6` and `T2-midpoint=52`). When `--budget-remaining` is provided (per `sc:reflect §4.0 Step 0.9`), the skill derives per-PR turn cost as `§15 T2-midpoint (52 turns) ÷ 6 parallel PRs ≈ 8.7 turns/PR` (the `[INFERRED]` derivation from A's budget composition analysis). If `--budget-remaining` is provided AND the sum of estimated turns for `--max-prs` exceeds `--budget-remaining`, the skill degrades `--max-prs` to `floor((--budget-remaining - 5) / 8.7)` with a WARN message; the skill NEVER errors silently. Floor of 5 turns reserves headroom for Wave 0 + Wave 3 + Wave 4. If the degraded value is 0 (budget < 14 turns), the skill HALTs with `status: failed`, `failure_reason: budget-insufficient`. Emit `budget_forced_pr_set_clamp: true` in telemetry when degradation fires.

<!-- Source: Base (modified) — Change 3: replace status semantics block with A's three-state PASS/FAIL/PENDING verbatim -->
### 3.3 The PR-layer merge gate (the load-bearing structural addition)

This is **the** new mechanism. It is *not* a row in OVM's §14.5.2 9+1-condition gate. It is a **GitHub commit-status check** named `sc-pr-bot-validate / merge-gate` posted via `gh api repos/{owner}/{repo}/statuses/{sha}` after Wave 4 completes.

<!-- Source: Proposal A §3 status check semantics block — merged per Change 3 (verbatim three-state with explicit PENDING-initial-state clarity) -->
The check's conclusion semantics are:

```
PASS    (status: success)   — Wave 4 reflect verdict is one of:
                              (a) status == success AND
                                  outcome_verified == true (OVM derived boolean) AND
                                  confirmed_count + still_valid_count == 0
                           OR (b) status == success AND
                                  confirmed_count + still_valid_count > 0 AND
                                  every CONFIRMED/STILL_VALID finding has a passing
                                  acceptance criterion verified by a downstream
                                  task-builder + /task + reflect --mode post run
                                  whose contract reference is recorded in
                                  <output>/post-remediation-receipts/

FAIL    (status: failure)   — Wave 4 reflect verdict surfaces structural gaps
                              (citations_dropped > 0, grounding_gaps_path non-empty,
                               outcome_claims_failed > 0) OR
                              confirmed_count + still_valid_count > 0 AND no
                              post-remediation receipts present.

PENDING (status: pending)   — Wave 4 has not yet run for the PR's current HEAD SHA.
                              Posted at Wave 0 as the initial state (explicit
                              PENDING-initial-state transition); flips to PASS/FAIL
                              upon Wave 4 completion. A persistent PENDING after
                              workflow completion indicates a `gh api` post failure
                              and SAFELY blocks merge (see §5 PENDING masquerading risk).

NEUTRAL (status: success+description="no-bot-reviews") — PR has zero bot reviews
                              attached; gate vacuously passes (the pipeline did not need
                              to run). This branch keeps the gate non-blocking on the
                              common case where no bot is configured for the repo.
```

GitHub branch protection on `main` is configured to require `sc-pr-bot-validate / merge-gate` to be passing. This is the **first-class merge gate** that the preamble explicitly asks for (§5 constraint "Bot-review validation IS a first-class merge gate"), implemented via the canonical GitHub mechanism rather than a SuperClaude-internal one.

<!-- Source: Proposal A §3 / §9.1 — merged per Change 1 (port pr_bot_validation_* family verbatim with sibling-skill prefix rename pr_bot_validate_*) -->
The sibling skill's return contract carries the enumerated field family (ported from Proposal A's well-thought-out contract design, namespace-renamed to `pr_bot_validate_*` for sibling-skill consistency with the skill name `sc:pr-bot-validate`):

```yaml
# sc-pr-bot-validate-protocol/return-contract.yaml — contract_version: "1.0"
pr_bot_validate_contract_version: "1.0"

# Enumerated field family (A's U-001 ported verbatim, prefix renamed)
pr_bot_validate_path: <abs path> | null      # path to merge-gate-decision.yaml
pr_bot_validate_pr_count: <int>              # accepted_count from pr-set discovery
pr_bot_validate_buckets:
  confirmed: <int>
  still_valid: <int>
  false_positive: <int>
  out_of_scope: <int>
pr_bot_validate_prs_blocking_merge: [<int>, ...]
pr_bot_validate_complete: <bool>             # true iff every PR's per-agent run returned a remediation file
pr_bot_validate_status_check_conclusion: success | failure | neutral | pending | skipped | null
pr_bot_validate_pre_gate_passed: <bool>      # mirrors Wave 4 reflect pre verdict

# Derived single-axis convenience (mirrors OVM's `outcome_verified` pattern from sc-reflect-protocol MERGED-PROPOSAL.md §3.3)
pr_bot_validated: <bool>                     # derived: pr_bot_validate_complete AND prs_blocking_merge == [] AND pre_gate_passed
```

**All fields are additive top-level on the sibling skill's own contract.** They do NOT extend `sc-reflect-protocol`'s contract (which is the X-001-adjudicated architectural invariant: reflect ships unchanged beyond OVM's own bump). Existing consumers ignore per the contract's own unknown-field-tolerance rule (mirrored from reflect's §9.4 evolution-discipline). The derived `pr_bot_validated` field gives downstream consumers (the CI workflow, branch protection check, future sprint integration) a single-axis routing handle paralleling OVM's `outcome_verified` semantics.

**Namespace separation from OVM.** All sibling-skill field names use the `pr_bot_validate_*` prefix (NOT `pr_bot_validation_*`, which would be A's reflect-mode-prefix). Reflect's OVM-extended contract continues to use its own `outcome_*` and `outcome_claims_*` prefixes. The two field families coexist across two different contracts (reflect's `return-contract.yaml` vs sibling's own `return-contract.yaml` + `merge-gate-decision.yaml`) without prefix collision and without contract surface coupling. See §4 below for the explicit composition table.

The mapping from reflect's contract to the status check is deterministic and is captured in `<output>/merge-gate-decision.yaml`:

```yaml
pr_number: <int>
head_sha: <git sha at validation time>
reflect_contract_path: <abs path to reflect's return-contract.yaml at Phase 4>
reflect_status: success | partial | failed
reflect_outcome_verified: <bool>          # composed from OVM
confirmed_count: <int>
still_valid_count: <int>
false_positive_count: <int>
out_of_scope_count: <int>
post_remediation_receipts: [<list of paths>] | []
gate_conclusion: pass | fail | pending | neutral
gate_reason: <short string>
posted_to_github: <bool>
github_status_url: <url> | null
```

<!-- Source: Base (modified) — Change 4: adopt A's manual-invocation flag enumeration -->
### 3.4 New GitHub Actions workflow + manual CLI flag enumeration

Created at `.github/workflows/pr-bot-validate.yml`. Triggers on `pull_request_review` types `[submitted]` (when any bot leaves a review — gated by `github.event.review.user.type == 'Bot'`) and `pull_request` types `[synchronize, opened]` (so force-push invalidates the prior verdict). Per project CLAUDE.md "Validation should be done via the .github actions" — this is the workflow that operationalizes the gate. The job needs `permissions: { contents: read, pull-requests: write, statuses: write }`. It checks out `fetch-depth: 0`, runs `claude --skill sc-pr-bot-validate-protocol -- --pr ${{ github.event.pull_request.number }} --output .dev/reviews/pr-bot-validate-${{ github.run_id }}/`, then posts the status via `gh api repos/${{ github.repository }}/statuses/${{ github.event.pull_request.head.sha }}` reading `gate_conclusion` from `merge-gate-decision.yaml`. Load-bearing details: (a) `pull_request_review` trigger ensures each new bot review re-runs the gate; (b) `synchronize` ensures force-push/rebase re-runs against the new HEAD SHA; (c) the `gh api` POST against the head SHA is what GitHub branch protection actually consumes.

<!-- Source: Proposal A §3 trigger spec — merged per Change 4 (A's enumerated flag set ported into sibling-skill CLI) -->
**Manual CLI invocation flags.** Invoke as `/sc:pr-bot-validate [flags]`. The enumerated flag set (ported from Proposal A's well-thought-out trigger spec):

- `--pr <N>` — single GitHub PR number to validate. Required when `--prs` is absent and discovery is not desired.
- `--prs <N1,N2,...>` — explicit PR set (1-6 PRs). When absent AND `--pr` absent, the Wave 1 discovery sub-step is auto-run.
- `--max-prs <N>` — cap on auto-discovered PR set. Default 6 (matches preamble §3 §5 cost-envelope guidance). Hard ceiling 10 per OVM §15 "≤T2" budget envelope.
- `--bot-source-filter <id>` — restrict discovery to a single bot integration id (e.g., `--bot-source-filter augment`). Defaults to all enabled entries in `refs/bot-review-sources.yaml`.
- `--bot-sources <path>` — override path to `refs/bot-review-sources.yaml`.
- `--depth standard|deep` — passed through to `Skill sc-auggie-review-protocol` at Wave 2. Default `standard`.
- `--output-dir <path>` — override `<output>` root for artifacts (default `.dev/reviews/pr-bot-validate-<ts>/`).
- `--budget-remaining <int>` — number of remaining turn-budget units; routes Wave 0 degradation per §3.2 budget composition.
- `--no-post-status-check` — suppress the GitHub status check publication. Default off (status check is published when CI invokes; suppressed by default when invoked from a local shell so dev runs don't spam PRs).

If `--budget-remaining` is provided AND the sum of estimated turns for `--max-prs` exceeds `--budget-remaining`, the skill degrades `--max-prs` per the §3.2 Wave 0 budget composition rule and emits the WARN message. The skill NEVER errors silently on budget mismatch.

<!-- Source: Base (original) -->
### 3.5 New ref file: `refs/bot-review-sources.yaml`

Lives at `src/superclaude/skills/sc-pr-bot-validate-protocol/refs/bot-review-sources.yaml` (per preamble §9 — operators add bots without protocol-text changes). Each entry: `integration_login` (e.g., `augment-code[bot]`), `name`, `review_authorship_pattern`, `enabled`. Default entries: `augment-code[bot]` (enabled), `coderabbitai[bot]` (enabled), `github-copilot[bot]` (opt-in), `sourcery-ai[bot]` (opt-in), `greptile-apps[bot]`, `codiumai-pr-agent[bot]`. Mirrors OVM's `refs/claim-extraction-patterns.yaml` shape (per preamble §1 OVM precedent). The ref lives **inside the new sibling skill**, not in reflect — preserving reflect's single-skill ref home per OVM Change 5.

<!-- Source: Base (original) -->
### 3.6 Composition with `task-builder` + `/task` + reflect `--mode post`

When `confirmed_count + still_valid_count > 0`, the sibling's return contract writes a `remediation_handoff` block with `next_actor: operator`, `next_command: "Skill task-builder --build-request <output>/PROPOSALS-normalized.md"`, `followup_command: "/task .dev/tasks/to-do/<slug>/<file>.md"`, `validation_command: "Skill sc-reflect-protocol --mode post --diff <pre-task-ref>..HEAD --tasklist <mdtm-path>"`, and `receipt_directory: <output>/post-remediation-receipts/`. The operator runs each command in turn; the validation_command's reflect output lands in `receipt_directory` for the next sibling re-run (triggered by the `synchronize` event after the operator pushes the remediation commit). At that point the §3.3 gate (b) branch is satisfied by receipt presence, and the merge gate flips from FAIL to PASS.

<!-- Source: Base (original) -->
### 3.7 Reflect's contract is consumed read-only

The sibling reads from reflect's v1.1 return-contract.yaml: `status`, `coverage_pct`, `coverage_undefined`, `unmapped_requirements` (UC-1 fields at Phase 4); `citations_dropped`, `grounding_gaps_path`, `needs_human_decision` (hallucination guards); `outcome_verified` (OVM derived bool — primary structural input); `outcome_claims_failed`, `outcome_claims_deferred`, `deferred_outcomes_runbook_present` (OVM fields routing gate (a) vs (b)); `input_drift_detected` (forces re-run on HEAD change). This mirrors `sc:troubleshoot` Wave 6 Phase D's read of reflect's UC-2 verdict (`sc-reflect-protocol/SKILL.md:53-54, :462`) — established skill-composition pattern.

<!-- Source: Proposal A's discoverability concession — merged per Change 10 (one-line cross-reference addition to sc-reflect-protocol §16 Related Commands) -->
### 3.8 One-line discoverability cross-reference in `sc-reflect-protocol` §16

The merged proposal includes **one** small documented change to `sc-reflect-protocol/SKILL.md` outside the sibling skill itself: a single-line addition to §16 "Related Commands". This is **NOT** a contract change, **NOT** a behavior change, and **NOT** a mode addition — it is purely a discoverability bridge that addresses Advocate-A's operator-cognitive-load argument without re-opening the X-001 architectural adjudication.

The downstream task-builder applies this edit verbatim to `sc-reflect-protocol/SKILL.md` §16 "Related Commands" list:

> **`/sc:pr-bot-validate`** — PR-layer audit sibling skill; consumes reflect's return contract read-only at its Wave 4 to validate external bot-review signal as a first-class merge-gate input. Use when the work-unit you'd reflect on is *spread across multiple PRs with bot reviews attached*.

**Surface impact on reflect:** zero. §16 is the existing cross-reference home; adding a new related-command bullet does not change reflect's contract, modes, waves, gate, refs, or allowed-tools. The single-line addition mirrors how `sc:troubleshoot` and `sc:auggie-review` are already cross-referenced in §16 today. CI lint asserting `sc-reflect-protocol/SKILL.md` does not invoke `sc-pr-bot-validate` remains satisfied (a `Related Commands` mention is not an invocation).

---

<!-- Source: Base (original) -->
## 4. Composition with OVM — explicit table

OVM lands in v1.1 of `sc-reflect-protocol`. This proposal lands in v1.0 of the new `sc-pr-bot-validate-protocol` skill, plus **zero** changes to OVM (and one §16 Related-Commands one-line cross-reference, per §3.8). The composition surface is the boundary between the two contracts.

| OVM contract field | sc:pr-bot-validate consumption | Collision? |
|---|---|---|
| `contract_version: 1.0 → 1.1` (reflect side, OVM bump) | Read at Phase 4 by sibling skill; sibling pins `reflect_contract_version_required: ">= 1.1"` in its own frontmatter | None — sibling reads, never writes reflect's contract |
| `outcome_claims_path`, `outcome_claims_total`, `outcome_claims_by_seat` (OVM §3.3) | Surfaced in sibling's `merge-gate-decision.yaml` as a passthrough `reflect_outcome_claims_summary` field; not gate-load-bearing | None |
| `outcome_verified` (OVM Change 2 derived bool) | **Primary structural input** to the §3.3 gate (a) branch; the bot-validation skill treats it as the source of truth for "the work is verifiable from reflect's seat" | None — sibling reads only |
| `outcome_claims_failed > 0` (OVM §3.3) | Routes the sibling's gate to FAIL with `gate_reason: "reflect surfaced failed outcome claim"`; this is OVM's `§14.5.2` cond 10 surfacing at the PR layer rather than the work-unit layer | **Resolved by layer separation** — OVM blocks `mv` of the tasklist; sibling blocks `gh pr merge`. The same root cause surfaces at both layers because both consult reflect's return contract; the propagation is correct, not collisional. |
| `deferred_outcomes_runbook_present` (OVM Change 4) | Honored by the sibling: if true AND `outcome_claims_failed == 0`, the gate may PASS without post-remediation receipts (gate (a) branch). The runbook is moved with the work-unit per OVM §3.5; the PR-layer gate trusts OVM's "deferred-with-runbook is honest success" semantics. | None — proposals are **strictly stacking**, not contradictory |
| `promotion_deferred_outcomes_count`, `promotion_deferred_runbook_paths` (OVM §3.3) | Surfaced in the sibling's `merge-gate-decision.yaml` for operator visibility; not gate-load-bearing | None |
| OVM new `refs/claim-extraction-patterns.yaml` | Lives in `sc-reflect-protocol/refs/`; sibling has its **own** ref at `sc-pr-bot-validate-protocol/refs/bot-review-sources.yaml`. Per OVM Change 5 (no shared-refs directory), the two ref files coexist with disjoint scope. | None |
| OVM Change 3 cond 10 (`§14.5.2`) | Work-unit-layer; sibling adds **no condition 11** at this layer. The sibling's gate is a different artifact (GitHub status check), not a row in `promotion-log.yaml`. | **Layer-separated, no row added** to `§14.5.2` |
| OVM allowed-tools addition (WebFetch, WebSearch) | Inherited transitively when sibling invokes `Skill sc-reflect-protocol` at Phase 4 (reflect's own allowed-tools apply during that call); sibling itself does not need WebFetch in its frontmatter — its toolset is `gh`, `git`, `Task`, `Skill` | None |
| OVM v1.1 deferred-hardening §19.2 INV-023 (sufficiency claim) | Composes orthogonally; sibling does not touch reflect's sufficiency framing. The sibling's *own* sufficiency claim is documented in its own §11.0 equivalent (drafted to mirror reflect's §11.0 conditional structure). | None |

**Versioning composition:** OVM bumps `sc-reflect-protocol` from contract_version 1.0 → 1.1. This proposal introduces `sc-pr-bot-validate-protocol` at its own contract_version 1.0. The two version bumps are **independent**. The OVM release notes need only mention "see also: new sibling skill sc-pr-bot-validate-protocol v1.0 ships in the same release window." No back-references in OVM are required; reflect remains ignorant of the sibling per preamble §9 anti-recursion stance, with the single §16 Related-Commands one-line cross-reference per §3.8 as the only reflect-side touch.

**Zero collisions found.** The composition is clean by layer separation: OVM is work-unit-layer; this proposal is PR-layer; both consult reflect's return contract as the audit primitive, but neither modifies the other's surface.

---

<!-- Source: Base (original) -->
## 5. How it answers the 10 structural questions from preamble §4

**Q1 — Where does this live?** *Sibling skill `sc:pr-bot-validate`* (argued in §1): the pipeline orchestrates *over* reflect (calls reflect twice as sub-steps); putting it inside reflect inverts the dependency arrow. The sibling consumes reflect's return contract read-only, mirroring `sc:troubleshoot` Wave 6 Phase D's pattern (`sc-reflect-protocol/SKILL.md:53-54, :462`).

**Q2 — Trigger?** GitHub Actions workflow on `pull_request_review` (any bot leaves a review) + `pull_request.synchronize` (HEAD changes). Manually triggerable via `/sc:pr-bot-validate <PR-num>` (full flag set enumerated in §3.4). Not always-on per PR — PRs with no bot reviews resolve NEUTRAL and don't block. Not opt-in — branch protection configures once.

**Q3 — First-class merge gate?** GitHub branch protection requires the `sc-pr-bot-validate / merge-gate` commit-status check (§3.3). Conclusions: PASS (`status: success`) allows merge; FAIL (`status: failure`) blocks; PENDING (`status: pending`) blocks (and is the explicit Wave-0 initial state); NEUTRAL (`status: success` + description `no-bot-reviews`) allows. Uses GitHub's canonical primitive rather than inventing one. Contract field: `gate_conclusion` in `<output>/merge-gate-decision.yaml`.

**Q4 — Contract shape?** Sibling's `merge-gate-decision.yaml` (§3.3) + its own versioned `return-contract.yaml` carrying the enumerated `pr_bot_validate_*` field family (§3.3 ported from A's well-thought-out U-001 contract design, namespace-renamed). **Zero additive fields in reflect's contract.** Bucket counts (`confirmed_count`, `still_valid_count`, `false_positive_count`, `out_of_scope_count`) come from Wave 3 aggregation; per-PR finding paths are `/tmp/remediation-pr-<N>.md`; aggregated proposal is `<output>/PROPOSALS-normalized.md`; pre-validation report is reflect's Phase 4 contract path; post-execution receipts live in `<output>/post-remediation-receipts/`. OVM's `outcome_verified` and `deferred_outcomes_runbook_present` are *consumed*, not redefined.

**Q5 — Compose with 9+1-condition gate?** Does **not** add condition 11. Different layer: §14.5.2 gates `mv` of `.dev/tasks/to-do/TASK-NNN/` → done; the PR gate gates `gh pr merge`. Connected via reflect's return contract (sibling reads what OVM wrote at cond 10) but gates share no rows. §14.5.2 remains a 10-condition gate; sibling's gate is a separate artifact.

**Q6 — Force-push / rebase?** Workflow triggers on `pull_request.synchronize` (fires on every force-push and additional commit). Wave 4 re-runs against the new HEAD SHA; the CONFIRMED/STILL_VALID/FALSE_POSITIVE/OUT_OF_SCOPE bucketing from preamble §3 Phase 2 Step 3 is preserved verbatim inside Wave 2. `AUGMENT_SHA_OBSERVED` is captured per-run in `merge-gate-decision.yaml.head_sha`; the prior verdict is invalidated by GitHub's per-SHA status-check semantics. Force-push invalidation happens as a side effect of GitHub's own gating, which is the right place.

**Q7 — Scale?** `--max-prs` flag (default 6) caps fan-out in the **manual** path. The **CI** path runs against exactly 1 PR per trigger — concurrent multi-PR validation is the GitHub Actions matrix's job, not the skill's. The 6-cap is a budget guard mirroring reflect's §15 T2 envelope (6 parallel `sc:auggie-review` calls hit the team's pain threshold). Configurable via flag; `--budget-remaining` accepted (mirrors reflect §4.0 Step 0.9); too-low budget routes through the §3.2 Wave 0 degradation rule (`floor((--budget-remaining - 5) / 8.7)`), and HALTs with `failure_reason: budget-insufficient` when the floor is 0.

**Q8 — Other bots?** `refs/bot-review-sources.yaml` (§3.5). Each entry: `integration_login` (GitHub canonical bot identifier), `name`, `review_authorship_pattern`, `enabled`. Adding a new bot = one-line ref edit; no protocol-text changes per preamble §9. Auto-detection by `user.type == "Bot"` on review objects.

**Q9 — Interaction with `/sc:auggie-review`?** Sibling **calls** `Skill sc-auggie-review-protocol` at Wave 2, once per PR, exactly as preamble §3 Phase 2 Step 2 prescribes. No factor-out — auggie-review is already the validation primitive; reuse it as-is. Invocation passes `--no-post-pr --no-remediation-offer --depth standard --output-dir /tmp/pr-<N>-auggie-fresh/`.

**Q10 — Interaction with `task-builder` + `/task`?** Sibling **does not invoke** them — both are operator-driven per preamble §9 anti-auto-execution. Sibling's return contract exposes `remediation_handoff.next_command` and `.followup_command` (§3.6) as copy-paste handoff. The post-remediation reflect `--mode post` verdict is the receipt that closes the FAIL → PASS loop on the next `synchronize` event. Honors `sc-reflect-protocol/SKILL.md:1436` "Will Not — Auto-execute a Tier 3 remediation task" by analogy.

---

<!-- Source: Base (modified) — Change 6 (INV-002), Change 7 (INV-003 routed via §3.2; risk surfaced in §5), Change 9 (A-001 promotion) -->
## 6. Trade-offs and risks (and what proposal-A almost certainly does better)

**Honest accounting of what this direction costs:**

**Cost 1: Two skills instead of one.** Operators have to know both `sc:reflect` and `sc:pr-bot-validate`. Proposal-A surfaces a single discoverable `/sc:reflect --mode pr-bot-validation`, which is genuinely easier for new operators. **Mitigation:** the new `/sc:pr-bot-validate` command is named after its job and lists next to `/sc:reflect` in `/sc:help`. The §3.8 one-line cross-reference addition to `sc-reflect-protocol/SKILL.md` §16 "Related Commands" closes the discoverability gap without re-opening the architectural debate.

**Cost 2: Skill-installation surface grows.** The SuperClaude installer ships a new skill directory; `make sync-dev` copies it; CI lints it. ~+800-1200 lines of SKILL.md, +1 ref, +1 workflow YAML. Additive on top of OVM.

**Cost 3: Cross-skill contract drift risk.** If reflect's v1.1 → v1.2 changes any field the sibling reads, the sibling must bump in lockstep. Mitigation: the sibling pins `reflect_contract_version_required: ">= 1.1"` in frontmatter and STOPs on major bump. §9.4 unknown-field-tolerance covers additive minor bumps.

**Cost 4: The "but reflect is the natural home" intuition.** Proposal-A leaned on this in Round 1: reflect is the validation skill, and bot-validation is a validation. Honest concession (Advocate-A's Round 2): the *naming* makes the third-mode pitch sympathetic. The counter is structural, not nominal — the pipeline orchestrates *over* reflect; the layer differs (PR vs work-unit); the gate differs (GitHub status vs `mv`). The third-mode answer is easier to motivate but harder to defend at the boundary; Advocate-A conceded this in Round 2 under §17.7 Kill #3, the PR-vs-work-unit layer separation, and the `--recursive` anti-pattern.

**Where this direction is structurally stronger:** (i) **Identity preservation** — reflect's §17.7 Kill #3 already names "dilute reflect's identity" as load-bearing; a mode that owns PR fan-out + bot detection + `gh pr list` + status-check posting + GitHub Actions integration is dilution. (ii) **GitHub-native gate primitive** — the merge gate is a commit-status check posted via `gh api .../statuses/...`, the canonical GitHub mechanism; branch protection consumes it without SuperClaude awareness. (iii) **CI-trigger cleanliness** — the workflow's `claude --skill sc-pr-bot-validate-protocol` is a one-skill invocation; the third-mode equivalent `--skill sc-reflect-protocol -- --mode pr-bot-validation` conflates the workflow's intent.

**Token / wall-clock cost:** T2 band per reflect's §15. Manual 6-PR mode: ~35-70k Claude orchestration tokens, 10-15min wall-clock. CI mode (1 PR per trigger): ~6-12k tokens, 2-4min — within typical PR-CI latency budgets. The per-PR turn-cost derivation `T2-midpoint (52) ÷ 6 parallel PRs ≈ 8.7 turns/PR` (ported from Proposal A's U-002 budget composition) drives the Wave 0 degradation rule documented in §3.2.

**Risk: bot disagreement.** Augment vs CodeRabbit on the same line: each bucketed independently; adjudication deferred to sibling v1.2 per preamble §6 and merged §9. `merge-gate-decision.yaml` surfaces per-bot raw counts. **Risk: `gh` CLI surface drift.** `gh pr view --json reviews` and `gh api .../statuses/...` are stable as of May 2026; Wave 0 includes a `gh` version probe and STOPs on major-version mismatch. **Risk: PENDING masquerading as PASS.** If status post fails (token scope wrong), gate stays PENDING and merge is blocked — safe failure mode. `permissions: { statuses: write }` is mandatory per §3.4.

<!-- Source: Round 2.5 invariant probe INV-002 — merged per Change 6 -->
**Assumption (INV-002):** `gh api repos/{owner}/{repo}/statuses/{sha}` writes to the same `(sha, context)` are idempotent in effect — branch protection consumes only the most recent status. Cited from GitHub REST API spec (sha:refs/statuses endpoint). If this changes (rate-limit imposed, write-once semantics added), the sibling skill must track its own `last-posted-status.json` cache and skip redundant writes. **Fallback runbook:** on a 422/429 response from `gh api .../statuses/<sha>`, the workflow logs the response body, sets `gate_conclusion: pending` in `merge-gate-decision.yaml`, and exits 0 so the workflow doesn't mask the underlying issue with a green CI run. A persistent PENDING is the safe failure mode (merge stays blocked) and signals operator attention.

<!-- Source: Round 2.5 invariant probe INV-003 — merged per Change 7 (cross-reference; primary spec lives in §3.2 Wave 0) -->
**Risk (INV-003) — `--max-prs` + `--budget-remaining` interaction.** The Wave 0 degradation rule is documented in §3.2 and §3.4 (`floor((--budget-remaining - 5) / 8.7)` with WARN message; HALT with `status: failed, failure_reason: budget-insufficient` when degraded to 0). The risk surfaced here is operator surprise: a `--max-prs 6` invocation may silently degrade to `--max-prs 2` under a tight budget. **Mitigation:** the WARN message names the original and degraded values explicitly; telemetry field `budget_forced_pr_set_clamp: true` is persisted to `<output>/merge-gate-decision.yaml`; the operator sees the degradation in the report.

<!-- Source: Shared-assumption A-001 promotion — merged per Change 9 -->
**Assumption (A-001):** `gh api repos/{owner}/{repo}/statuses/<sha>` remains the canonical GitHub merge-gate primitive consumed by branch protection (verified against GitHub REST API v2026.5 docs at proposal-authoring time). If a future GitHub change deprecates this endpoint or migrates branch-protection-status-check-binding to a different primitive (e.g., GitHub Checks API), the skill must update §3.3 mechanism and the workflow at §3.4 — but the protocol surface (a sibling skill emitting merge-gate verdicts) is unchanged. **Fallback for transient `gh api` failures:** post a retry after exponential backoff (max 3 retries: 2s, 8s, 32s); on persistent failure, emit `status: partial` with `merge_gate_decision: error` and surface to operator via WARN. The status check itself remains PENDING, which safely blocks merge.

---

<!-- Source: Base (original) -->
## 7. Backward-compat — v1.0 → v1.1 composition with OVM

**`sc-reflect-protocol`**: unchanged by this proposal beyond OVM's own bump, with the single exception of the §3.8 one-line cross-reference addition to §16 "Related Commands" (purely a discoverability bridge; not a contract, mode, wave, gate, or behavior change). OVM ships as reflect v1.1; this proposal ships entirely outside reflect's contract surface. Therefore reflect's v1.0 → v1.1 transition is **fully owned by OVM**, and this proposal adds zero rows to reflect's `§9.4` contract evolution surface, zero rows to its `§14.5.2` gate, zero refs to `sc-reflect-protocol/refs/`, zero modes to `§3.2`. Consumers of reflect's contract (`sc:troubleshoot` Wave 6, `superclaude sprint`, `sc:task-protocol`) see exactly the OVM-induced changes and no more.

**`sc-pr-bot-validate-protocol`**: new skill, contract_version 1.0. Pinning `reflect_contract_version_required: ">= 1.1"` in its frontmatter. Migration window per `sc-reflect-protocol/SKILL.md` §9.4: the sibling skill consumes OVM fields, so it cannot ship before OVM lands; the BRV-MG preamble §5 commits both to the "same v1.1 release," which is satisfied if the sibling skill ships in the same release tag as OVM. **Ordering constraint**: OVM merges first (or simultaneously); the sibling can be tagged in the same release. The release notes need only mention the pairing.

**Downstream consumers:**

- **`sc:reflect` itself**: zero contract or behavior changes; one §16 Related-Commands line added per §3.8.
- **`superclaude sprint`**: zero required changes. Optional: the sprint executor *may* read `merge-gate-decision.yaml` to defer a phase that depends on a PR-merged dependency, mirroring its optional consumption of OVM's `promotion_deferred_outcomes_count > 0`. This is opt-in.
- **`sc:task`**: zero required changes. Operators run the `remediation_handoff.followup_command` themselves.
- **`sc:troubleshoot` Wave 6**: zero changes. The sibling does NOT call sc:troubleshoot, and sc:troubleshoot does NOT call the sibling — they are peers under the audit-class umbrella.
- **GitHub branch protection**: one-time configuration change to require the new status check. Documented in the sibling's `refs/branch-protection-setup.md`.

**Anti-collision invariant:** `sc-pr-bot-validate-protocol` MUST NOT be invoked from inside `sc-reflect-protocol` (any wave, any mode). This is the structural invariant that prevents recursion (the sibling calls reflect at Phase 4; if reflect called back, the audit would loop). Encoded as a `Will Not` row in the sibling's protocol text and as a CI lint that greps for `sc-reflect-protocol/SKILL.md` references to `sc-pr-bot-validate` *as an invocation* (a §16 Related-Commands mention is allowed; a `Skill sc-pr-bot-validate-protocol` invocation is forbidden).

---

<!-- Source: Base (original) -->
## 8. Falsifier — eval case modeled on `sc-reflect-protocol/SKILL.md` §12.5

Lives at `.dev/eval-workspaces/sc-pr-bot-validate/cases/falsifier-suite/bot-validation-mixed-buckets.yaml`. Modeled on reflect's `§12.5` T2-converges-on-wrong skeleton and on OVM's §7.1 `outcome-verification-docker-cli-miss` shape; **same fixture shape as A** (per task instructions) but routed through a sibling-skill verdict path.

```yaml
id: bot-validation-mixed-buckets
type: held-out adversarial
status: active
fixture: fixtures/bot-validation-mixed-buckets/
setup: |
  Mocked PR #999 in IronbellyOrg/Coder with 3 findings:
    1. CONFIRMED-target: Augment at src/foo.py:42 ("leaked file handle") — current
       diff still has leaked open() with no with-block; auggie-fresh also surfaces;
       file:line resolves → bucket CONFIRMED.
    2. FALSE_POSITIVE-target: Augment at src/foo.py:80 ("untyped boundary") — line 80
       exists with different content (function was replaced) → bucket FALSE_POSITIVE.
    3. STILL_VALID-target: NO Augment finding, but fresh sc:auggie-review surfaces
       src/baz.py:17 ("missing None-guard") → bucket STILL_VALID.
  HEAD SHA: 0xdeadbeef; AUGMENT_SHA_OBSERVED: 0xdeadbeef (no force-push).
  Mocked reflect Phase 4: status=success, outcome_verified=true,
    citations_dropped=0, grounding_gaps_path=null.

expected:
  pipeline_completed_waves: [1, 2, 3, 4]
  per_pr_buckets.pr_999: {confirmed: 1, still_valid: 1, false_positive: 1, out_of_scope: 0}
  reflect_phase4_outcome_verified: true
  merge_gate_decision:
    gate_conclusion: fail
    gate_reason: matches "confirmed.*still_valid.*no.*receipts"
    post_remediation_receipts: []
    posted_to_github: true
    github_status_url: matches "repos/.+/statuses/0xdeadbeef"
  remediation_handoff.next_command: matches "Skill task-builder.*PROPOSALS-normalized.md"
  remediation_handoff.validation_command: matches "Skill sc-reflect-protocol --mode post"

assertion: |
  confirmed == 1 AND still_valid == 1 AND false_positive == 1 AND
  gate_conclusion == "fail" AND posted_to_github == true

severity: AUTO-FAIL if gate_conclusion == "pass" OR posted_to_github == false
  OR if confirmed + still_valid == 0 OR if false_positive == 0
  (the gate would have allowed a broken-handle PR to merge → proposal disproven)

passing_run_followup: |
  Add post-remediation receipt under <output>/post-remediation-receipts/
    pr-999-reflect-post.yaml with status=success, outcome_verified=true,
    deviation_count_by_class.regression=0. Re-run; expected: gate_conclusion ==
    "pass" (gate (b) branch satisfied by receipt presence); merge unblocked.
```

A passing run proves correct routing through Waves 1-4 with the right `merge-gate-decision.yaml` and GitHub status post. Auto-fail falsifies the proposal.

**Divergence from A's expected routing:** Same fixture shape (mixed-bucket inputs) per task instructions; expected output routing differs by design. A's proposal asserted a row in reflect's `promotion-log.yaml` or a new field in reflect's `return-contract.yaml`; this fixture asserts a separate `<output>/merge-gate-decision.yaml` artifact plus a GitHub status-check post via `gh api`. The X-001 architectural adjudication makes B's routing the authoritative shape.

---

<!-- Source: Base (modified) — Change 5: add multi-bot disagreement v1.2-defer bullet -->
## 9. Out-of-scope items (deliberately includes things A would have done)

1. **Embedding the bot-validation logic in reflect** (third-mode approach, condition 11 in §14.5.2, or new fields in reflect's §9.1 contract). Deliberately out — that is the structural disagreement with A; this proposal leaves reflect's contract untouched (with one cosmetic §16 Related-Commands cross-reference per §3.8) and the merge gate lives at the PR layer.
2. **Auto-execution of remediation.** Per preamble §9 + reflect's "Will Not" boundary. Operator runs `task-builder` + `/task`; sibling's `remediation_handoff` is paste-and-run only.
3. **Bot disagreement adjudication.** Per preamble §6. Each bot bucketed independently; conflicts surface in raw counts. Deferred to sibling v1.1.
4. **Non-GitHub PR platforms (GitLab MR, Bitbucket PR, Gerrit).** Per preamble §6. Sibling is GitHub-specific (`gh` CLI dependency); a GitLab equivalent would be a separate sibling sharing the bucket logic via `refs/`.
5. **Cross-PR cross-bot correlation.** Out — each PR independent; a finding on PR #100 is not propagated to PR #101 even if the file is shared.
6. **Auto-rerun on bot re-review of the same SHA.** Out — `pull_request_review` fires only on `submitted` (not edited/dismissed); re-runs require new review or new push.
7. **Mid-pipeline cancellation.** Out — Wave 2's parallel agents run to completion; cancellation is left to the workflow timeout.
8. **A new logical-fidelity layer.** Out — sibling consumes OVM's `V-Deferred-Logical` rows transparently through `outcome_claims_by_seat.v_deferred_logical`; routes through gate (a) branch the same way other deferred-with-runbook rows do.
9. **The `sc-auggie-review-protocol`'s remediation-offer chain.** Sibling invokes auggie-review with `--no-remediation-offer` (per preamble §3 guardrail); the sibling owns the remediation handoff, not auggie-review.
<!-- Source: Proposal A §6 brief mention + invariant probe INV-005 — merged per Change 5 -->
10. **Multi-bot disagreement adjudication** (e.g., Augment says CONFIRMED + CodeRabbit says FALSE_POSITIVE on the same `foo.py:42`) — deferred to sibling v1.2. v1.0 processes each bot independently and emits per-bot finding rows in `merge-gate-decision.yaml`, leaving the operator to adjudicate. The aggregate `blocks_merge` derivation in v1.0 is the OR across bots: any bot's CONFIRMED or STILL_VALID bucket on the PR contributes to the gate's FAIL routing. A future v1.2 may add an adversarial-merge step here using `sc:adversarial-protocol` (Mode A `--compare`) per the same architectural pattern that resolved this proposal's own A-vs-B contradiction.

---

**End of merged proposal.** This document is the BUILD_REQUEST input to `task-builder` for the downstream MDTM tasklist that implements the sibling skill, the GitHub Actions workflow, the ref file, the §16 Related-Commands one-line addition, the falsifier eval case, and the post-merge consistency lint. Composed with OVM's `sc-reflect-protocol/MERGED-PROPOSAL.md`, the pair lands in the same v1.1 release window with reflect ending at contract_version 1.1 and the new sibling at its own contract_version 1.0.
