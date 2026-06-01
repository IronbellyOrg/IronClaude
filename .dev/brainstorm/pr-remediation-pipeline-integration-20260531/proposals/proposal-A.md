<!-- Provenance: Produced by /sc:brainstorm via Skill sc-brainstorm-protocol (single-proposal mode per task spec) -->
<!-- Author: PR-Remediation-Integration Brainstorm Agent -->
<!-- Date: 2026-05-31 -->
<!-- Composes-with: /config/workspace/IronClaude/.dev/brainstorm/reflect-verification-gap-20260531/MERGED-PROPOSAL.md (OVM, v1.0 → v1.1) -->
<!-- Target: extends /config/.claude/skills/sc-reflect-protocol/SKILL.md v1.0 → v1.1 -->

# Bot-Review-Validated Merge Gate (BRV-MG) — Integrating the 6-Way Parallel PR-Remediation Pipeline into `sc:reflect`

## 1. Problem framing

`sc:reflect` v1.0 audits *one work-unit at a time* from the operator's seat: it consumes a tasklist (UC-2) or a spec (UC-1) and returns a verdict + 9-condition promotion gate (§14.5.2) scoped to that single unit. The Coder repo, however, operates on a different load-bearing artifact in the merge-gate dimension: an *open GitHub PR* against which external bot reviewers (Augment Code today; CodeRabbit, GitHub Copilot, sourcery-ai, Greptile, codiumai tomorrow) have left inline review comments. Those comments are currently (i) authored against a specific commit SHA and immediately stale on rebase/force-push, (ii) un-triaged free-form prose, (iii) disconnected from any remediation/execute/re-validate loop, and (iv) **advisory rather than gating** — branch protection on `main` checks CI + human approval, not bot-review reconciliation.

The team has empirically converged on a 6-way parallel orchestration script (preamble §3) that fans out one general-purpose subagent per PR, runs `/sc:auggie-review --no-post-pr --no-remediation-offer` as the validation primitive against the current diff, buckets each Augment finding into `CONFIRMED / STILL_VALID / FALSE_POSITIVE / OUT_OF_SCOPE`, aggregates per-PR remediation files into `.dev/reviews/aggregated-remediation-<ts>/PROPOSALS.md` + `PROPOSALS-normalized.md`, runs `/sc:reflect --mode pre` on the normalized spec, then hands off to `task-builder` → `/task` → `/sc:reflect --mode post` for execution. The artifacts at `/config/workspace/IronClaude/.dev/reviews/aggregated-remediation-20260531-034121/` (16 actionable issues across PRs #68-#73, 8 CONFIRMED + 8 STILL_VALID, 0 false positives, 1 High severity) are the proof-of-shape.

The gap is structural, not procedural: the pipeline is an orchestration script the team maintains by hand, not a protocol surface with a contract, an audit log, a falsifier, or a merge-gate hook. Worse, the pipeline is *adjacent to* `sc:reflect` but does not yet *compose with* its 9-condition gate — meaning bot-review reconciliation cannot today block a `gh pr merge`. This proposal closes that gap by extending `sc:reflect` with a third mode that subsumes Phases 1-4 of the pipeline, surfaces the result as a GitHub status check, and cleanly hands off Phase 5 to the existing `task-builder` → `/task` → `--mode post` chain.

This is **orthogonal to OVM**. OVM closes the "implementation-verified ≠ outcome-verified" gap at the audit's own seat by extracting outcome-claims and routing external-spec / runtime / cross-system / V-Deferred-Logical seats explicitly. BRV-MG closes the "external-reviewer signal ≠ merge-gate contract" gap at the PR boundary. The two land in the same v1.1 contract bump and reuse each other's primitives but operate on different layers (work-unit vs PR).

## 2. Proposed integration — Bot-Review-Validated Merge Gate (BRV-MG) via a third `sc:reflect` mode

**Named central design.** Add a third mode to `sc:reflect`: `--mode pr-bot-validation` (alongside `--mode pre` and `--mode post`). The mode subsumes the orchestration of preamble §3 Phases 1-4 (Discover PR set → 6-way parallel fan-out → Aggregate → Pre-validate) as a first-class wave architecture, emits a new audit-class artifact (`pr-bot-validation.yaml`) peer to `deviation-ledger.yaml` (§10) / `grounding-gaps.yaml` (§10.6) / OVM's `outcome-claims.yaml`, exposes a status check (`sc-reflect/pr-bot-validation`) consumable by GitHub branch protection, and hands off Phase 5 cleanly to the existing `task-builder` → `/task` → `--mode post` chain via the existing Wave 6 remediation surface — **not by subsuming it**.

Three structural choices distinguish BRV-MG from a sibling skill:

1. **It lives inside `sc:reflect` because the gate surface is `sc:reflect`'s gate surface.** A sibling skill would need to either re-implement the 9-condition gate (rejected: contract collision risk) or consume `sc:reflect`'s output (rejected: makes bot-review a *consumer* of audit, not a *participant* in it). The strong default in preamble §9 — "extend `sc:reflect` with a third mode" — is the right call.
2. **It is PR-scoped, not work-unit-scoped.** OVM's cond 10 in §14.5.2 promotes a work-unit folder when outcome-claims are verified or runbook-deferred. BRV-MG adds a *separate, peer* PR-level gate condition (cond 11) — work-unit promotion (cond 1-10) and PR merge eligibility (cond 11) are explicitly distinct.
3. **It calls `/sc:auggie-review` as a primitive, does not re-implement it.** Per preamble §10's reuse principle, and per `sc:reflect` §8's existing cross-skill integration table.

The mode is **opt-in by invocation** but **always-on by CI workflow** once landed: a new `.github/workflows/sc-reflect-pr-bot-validation.yml` (per CLAUDE.md "validation should be done via .github actions") fires on every PR `synchronize`, `opened`, `reopened`, and `review_submitted` event filtered to bot reviewers, invokes `sc:reflect --mode pr-bot-validation --pr <N>`, and publishes the status check that branch protection consumes.

## 3. Mechanism — concrete protocol-text amendments

All anchors below refer to either `sc:reflect` v1.0 (`/config/.claude/skills/sc-reflect-protocol/SKILL.md`) or OVM v1.1 (`/config/workspace/IronClaude/.dev/brainstorm/reflect-verification-gap-20260531/MERGED-PROPOSAL.md`). Numbering is preserved; every amendment is additive per `sc:reflect §9.4` minor-bump rules.

### 3.1 New input + mode-selection rule (§3.1, §3.2)

Add to `sc:reflect §3.1` inputs:

- `--mode pr-bot-validation` — third mode, parallel to `pre` / `post`.
- `--pr <N>` — single GitHub PR number to validate. Required when `--mode pr-bot-validation` AND `--prs` absent.
- `--prs <N1,N2,...>` — explicit PR set (1-6). When absent AND `--mode pr-bot-validation` set, the discovery sub-step (Wave 1B.5 below) is auto-run.
- `--bot-sources <path>` — override path to `refs/bot-review-sources.yaml` (new ref; see §3.7 below).
- `--max-prs <N>` — cap on auto-discovered PR set. Default 6 (matches preamble §3 §5 cost-envelope guidance). Hard ceiling 10 per OVM §15 "≤T2" budget envelope.
- `--no-post-status-check` — suppress the GitHub status check publication. Default off (status check is published when CI invokes; suppressed by default when invoked from a local shell so dev runs don't spam PRs).

Add **rule 0** to `§3.2 Mode selection` (first-match remains correct; this prepends rather than reordering):

- **`0. --mode pr-bot-validation`** present → **PR-Bot-Validation (third mode)**. STOP if `--pr` and `--prs` are both unset AND auto-discovery returns zero PRs.

Rules 1-6 from v1.0 follow unmodified.

Hard STOP conditions (§3.3) gain:

- `--mode pr-bot-validation` AND `gh` CLI unavailable → STOP `"PR-bot-validation requires the gh CLI."`
- `--mode pr-bot-validation` AND auto-discovery returns zero PRs AND no `--pr`/`--prs` → STOP `"No PRs with bot reviews found in --max-prs window; pass --pr <N> or --prs <N1,N2,...> explicitly."`

### 3.2 New wave architecture additions (§4 wave map)

Insert two new sub-steps in Wave 1 (single insertion point, mode-conditional) and a new Wave 1.5 (parallel fan-out, mode-conditional). The 7-wave structural count (0-6 review + 7 mutation) per §4 is preserved; PR-bot-validation does NOT add a wave, it slots into Wave 1's existing architecture and uses sub-step numbering.

**Step 1B.5 — Discover PR set (UC-PR-Bot-Validation only).** Inserted in `§4.1 Wave 1` after Step 1B.4 (OVM outcome-claim extraction; see OVM §3.1) and before existing Step 1C (single-agent reflection). Behavior:

1. If `--prs` provided: parse, validate every PR exists via `gh pr view <N> --json number,state`. STOP if any PR doesn't exist or is not `OPEN`.
2. Else if `--pr` provided: single-PR set.
3. Else: auto-discover via `gh pr list --state open --limit 20 --json number,title,headRefName,author,reviews`, filter to PRs where any review's author login matches a pattern in `refs/bot-review-sources.yaml` (see §3.7). Clamp to `--max-prs` (default 6).
4. If discovered set > `--max-prs`: emit WARN with the full list and the trimmed set; do NOT STOP.
5. If discovered set is empty AND no explicit `--pr`/`--prs`: STOP per §3.3.

Output: `<output>/pr-set.yaml` with `{discovered_count, accepted_count, prs: [...], discovery_source: auto|explicit}`. Token cost: ~200 tokens.

**Wave 1.5 — 6-way parallel PR fan-out (UC-PR-Bot-Validation only).** Inserted between Wave 1 and Wave 2 (tier decision). Mode-conditional — never runs in UC-1/UC-2. Behavior:

For each PR in the accepted set, spawn one `Task` agent with `subagent_type: general-purpose` (no new agent class per OVM §7.2 constraint inherited) and the verbatim per-agent prompt from preamble §3 (substituting `<N>`). The orchestrator dispatches **all N agents in a single message** (preamble §3 explicit constraint; matches `sc:reflect` Wave 3B materialize-then-spawn pattern in §4.3). Each agent:

1. Fetches Augment's existing review via `gh pr view <N> --json reviews,comments,title,body,headRefOid` and persists raw payload at `/tmp/pr-<N>-augment-original.json`. Captures `AUGMENT_SHA_OBSERVED`.
2. Invokes `Skill sc-auggie-review-protocol` with `--no-post-pr --no-remediation-offer --depth standard --output-dir /tmp/pr-<N>-auggie-fresh/`.
3. Cross-references each Augment finding against the fresh auggie pass and the current diff, bucketing into `CONFIRMED / STILL_VALID / FALSE_POSITIVE / OUT_OF_SCOPE` per the preamble §3 logic.
4. Writes `/tmp/remediation-pr-<N>.md` in the preamble §3 Step-5 schema (PR_TITLE, AUGMENT_SHA_OBSERVED, FRESH_AUGGIE_OUTPUT_DIR, Confirmed/Still-Valid issues with Issue PR<N>-<seq> entries, Appendix: dropped findings).
5. Returns a ≤120-word summary to the orchestrator (PR_NUMBER, OUTPUT_PATH, CONFIRMED count, STILL_VALID count, FALSE_POSITIVES count, OUT_OF_SCOPE count, TOP_SEVERITY).

Each subagent gets its own `--output-dir`; `--no-post-pr` and `--no-remediation-offer` are enforced (per preamble §3 Guardrails). The orchestrator does NOT modify code in this wave.

After all N agents return: aggregate to `<output>/PROPOSALS.md` (human-readable) AND `<output>/PROPOSALS-normalized.md` (Issue PR<N>-<seq> stable IDs, file path, severity, acceptance criteria — the shape `sc:reflect --mode pre` consumes per the artifact at `.dev/reviews/aggregated-remediation-20260531-034121/PROPOSALS-normalized.md`).

Token/wall-clock cost: dominated by 6 parallel `/sc:auggie-review` calls. Per OVM §15: ~T2 band (~35-70k Claude orchestration + ~10-25k auggie offloaded). Wall-clock ~10-20 min for 6 PRs per preamble §5 ("the team's pain threshold"). When `--max-prs <= 3`: drops to ~T1.5 band (~20-40k Claude).

**Step 5.x — pre-validation pass and bot-review-validation report (UC-PR-Bot-Validation only).** Inserted in `§4.5 Wave 5` after OVM's Step 5.x (outcome-verification pass; OVM §3.2). Behavior:

1. Re-invoke `Skill sc-reflect-protocol --mode pre --spec <output>/PROPOSALS-normalized.md --depth standard --output <output>/reflect-pre-bot-validation/`. This is the same recursive-invocation pattern guarded by `--recursive` in §17 Boundaries; the third mode is whitelisted as a recursive-call source because pre-validation is structurally necessary.
2. Consume the pre-validation report's `coverage_pct`, `unmapped_requirements`, `best_practice_grade`, `status`. If pre-validation surfaces structural gaps (e.g., missing acceptance criteria, unclear scope, unverified file paths), patch `PROPOSALS-normalized.md` to address them and re-run pre-validation once (matching preamble §3 Phase 4's "If reflect surfaces structural gaps, patch ... and re-run reflect once" loop). After two attempts, give up and mark `pre_validation_gate: failed`.
3. Aggregate per-PR buckets into `<output>/pr-bot-validation.yaml` (see §3.3).
4. Synthesize the human-facing `REPORT.md` with sections: Executive summary, Per-PR results (with bucket counts + top-severity), Cross-PR themes, Pre-validation gate result, Status check publication summary.
5. Token cost: ~T1 (~3-8k Claude) for the synthesis pass alone; total mode T2-band.

### 3.3 New artifact: `pr-bot-validation.yaml` (peer to `outcome-claims.yaml`, `deviation-ledger.yaml`, `grounding-gaps.yaml`)

```yaml
contract_version: "1.0"
mode: pr-bot-validation
pr_set:
  discovered_count: <int>
  accepted_count: <int>
  prs: [<int>, ...]
  discovery_source: auto | explicit
  truncated: <bool>           # accepted_count < discovered_count
per_pr_results:
  - pr_number: <int>
    pr_title: <string>
    augment_sha_observed: <hex>
    head_sha_current: <hex>
    sha_changed: <bool>       # AUGMENT_SHA_OBSERVED != head_sha_current
    fresh_auggie_output_dir: <abs path>
    remediation_file_path: <abs path>
    bot_source: augment | coderabbit | copilot | sourcery | greptile | codiumai | other
    buckets:
      confirmed: <int>
      still_valid: <int>
      false_positive: <int>
      out_of_scope: <int>
    top_severity: critical | high | medium | low | none
    blocks_merge: <bool>      # true iff (confirmed + still_valid) > 0 AND top_severity >= medium
aggregate:
  total_confirmed: <int>
  total_still_valid: <int>
  total_false_positive: <int>
  total_out_of_scope: <int>
  prs_blocking_merge: [<int>, ...]
  cross_pr_themes: [<string>, ...]  # e.g., "citation drift" appearing in ≥3 PRs
pre_validation_gate:
  status: passed | failed | not_run
  proposals_normalized_path: <abs path>
  reflect_pre_report_path: <abs path>
  iterations: <int>           # 1 or 2 per §3.2 Step 5.x
status_check:
  name: sc-reflect/pr-bot-validation
  conclusion: success | failure | neutral | skipped
  posted: <bool>              # false when --no-post-status-check OR not in CI
  posted_url: <string> | null
```

### 3.4 New contract fields (`§9.1` additive — minor bump 1.0 → 1.1, composes with OVM's bump)

Add to `§9.1`:

```yaml
# PR-Bot-Validation (additive, minor bump 1.1 — composes with OVM)
pr_bot_validation_path: <abs path> | null    # the new artifact
pr_bot_validation_pr_count: <int>            # accepted_count
pr_bot_validation_buckets:
  confirmed: <int>
  still_valid: <int>
  false_positive: <int>
  out_of_scope: <int>
pr_bot_validation_prs_blocking_merge: [<int>, ...]
pr_bot_validation_complete: <bool>           # true iff every PR's per-agent run returned a remediation file
pr_bot_validation_status_check_conclusion: success | failure | neutral | skipped | null
pr_bot_validation_pre_gate_passed: <bool>    # mirrors aggregate.pre_validation_gate.status == passed

# Derived single-axis convenience (mirrors OVM's `outcome_verified` pattern from §3.3)
pr_bot_validated: <bool>                     # derived: pr_bot_validation_complete AND prs_blocking_merge == [] AND pre_gate_passed
```

**All fields are additive top-level.** Existing consumers ignore per `§9.4` unknown-field-tolerance. The `status` enum is unchanged. The derived `pr_bot_validated` field gives downstream consumers (the CI workflow, branch protection check, future sprint integration) a single-axis routing handle paralleling OVM's `outcome_verified` semantics from MERGED-PROPOSAL.md §3.3.

**Composition with OVM.** All new field names are namespaced with the `pr_bot_validation_*` prefix to avoid collision with OVM's `outcome_claims_*` and `outcome_*` prefixes. The two field families coexist in the same return contract without overlap. See §4 below for the explicit composition table.

### 3.5 Evidence-validator extension (`§11.2`) — peer to OVM's runbook schema check

Per OVM §3.4 (which already extends evidence-validator with runbook schema validation and finding-row presence check), add a third responsibility:

3. **Bot-finding row presence check.** For every per-PR result in `pr-bot-validation.yaml` with `buckets.confirmed + buckets.still_valid > 0`, the validator checks that:
   - The cited `remediation_file_path` exists on disk.
   - Each Issue PR<N>-<seq> entry in that file has all required fields (per the §3 Step-4 schema: Source, File:Line, Severity, Validity verdict, Issue, Proposed remediation, Acceptance).
   - File:line citations in confirmed/still-valid entries are re-Read against the current diff (re-uses the existing citation re-Read window from §11.5).
   - Failed validations are **dropped** per §11.1's third-bucket rule (forces `status: partial`).

The validator does NOT re-run the bucketing logic (too expensive); it asserts presence and shape, matching OVM §3.4's "does not re-resolve upstream lookups" cost-discipline pattern.

### 3.6 Promotion gate (`§14.5.2`) — new condition 11 (composes with OVM's cond 10)

Add condition 11 to the §14.5.2 gate:

```
11. mode != pr-bot-validation OR pr_bot_validated == true
```

The condition is **vacuously true** for UC-1 / UC-2 runs (`mode != pr-bot-validation`). It actively gates only when reflect ran in the third mode. This preserves OVM's cond 10 semantics for work-unit promotion (which fires when `mode == post`) and adds a parallel gate for the PR layer.

**Distinction from cond 10 (work-unit layer):**

| Cond | Layer | Mode | Effect |
|------|-------|------|--------|
| 10 (OVM) | Work-unit | `post` | Promotes `.dev/tasks/to-do/TASK-*` → `.dev/tasks/done/TASK-*` when outcome-claims verified/runbook-deferred |
| 11 (BRV-MG) | PR | `pr-bot-validation` | Publishes status check `sc-reflect/pr-bot-validation` as `success`; CI consumer (branch protection) unblocks `gh pr merge` |

The two gates run at **different layers** (preamble §10 last bullet — "Don't conflate per-PR-level gating with per-work-unit-level gating"). A single reflect invocation runs in exactly one mode and therefore evaluates exactly one of cond 10 (when `mode == post`) or cond 11 (when `mode == pr-bot-validation`). Both are vacuous in the other mode.

Gate-evaluation field added to `promotion-log.yaml` §14.5.6 (one new row in the existing 11-row gate_evaluation map):

```yaml
gate_evaluation:
  ...
  pr_bot_validated: pass | fail | n/a    # cond 11; "n/a" when mode != pr-bot-validation
```

Mutation in `--mode pr-bot-validation` is **not a `mv`** — it is a `gh api` POST to the status-check endpoint. Wave 7 remains the *only* wave that mutates outside `<output>/`; for the third mode, Wave 7 step 7.4 publishes the status check (the mutation) instead of moving a folder. The §14.5.5 atomicity discipline maps cleanly: the status-check POST is a single HTTP call (atomic from the GitHub API's perspective); on failure, the promotion-log entry's `pending: true` survives and the next invocation re-posts (idempotent — GitHub deduplicates by `name + sha`).

### 3.7 New ref: `refs/bot-review-sources.yaml`

Per preamble §9 (third bullet — "Don't propose maintaining the bot-detection pattern table in SKILL.md prose"), bot identification is ref-driven:

```yaml
bot_sources:
  - id: augment
    login_patterns: ["augment-*", "augmentcode[bot]"]
    review_author_kind: bot
    inline_comment_kind: review_comment
    detection_priority: 1
  - id: coderabbit
    login_patterns: ["coderabbitai[bot]", "coderabbit-ai"]
    review_author_kind: bot
    inline_comment_kind: review_comment
    detection_priority: 2
  - id: copilot
    login_patterns: ["copilot-pull-request-reviewer[bot]"]
    review_author_kind: bot
    inline_comment_kind: review_comment
    detection_priority: 3
  # operators add bots here without protocol-text changes
```

Loaded on-demand at Wave 1 Step 1B.5 per the §16 refs table; mirrors OVM's `refs/claim-extraction-patterns.yaml` pattern from MERGED-PROPOSAL.md §3.1 ("operators add patterns without editing SKILL.md").

### 3.8 New CI workflow: `.github/workflows/sc-reflect-pr-bot-validation.yml`

Per CLAUDE.md ("Validation should be done via the .github actions") and preamble §5 constraint ("Your proposal must say what new workflow gates the merge"):

```yaml
name: sc-reflect PR bot-review validation
on:
  pull_request:
    types: [opened, synchronize, reopened]
  pull_request_review:
    types: [submitted]
jobs:
  bot-validate:
    if: github.event.review.user.type == 'Bot' || github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      statuses: write
      checks: write
    steps:
      - uses: actions/checkout@v4
      - name: Run sc:reflect --mode pr-bot-validation
        run: sc-reflect --mode pr-bot-validation --pr ${{ github.event.pull_request.number }} --post-status-check
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ANTHROPIC_AUTH_TOKEN: ${{ secrets.ANTHROPIC_AUTH_TOKEN }}
```

Branch protection on `main` requires the `sc-reflect/pr-bot-validation` check to be `success` before merge. (Out of scope for this proposal: the branch-protection configuration itself, which is a repo-admin task — but the proposal names the exact check name to configure.)

## 4. Composition with OVM (explicit mapping)

| BRV-MG element | OVM equivalent / interaction | Collision? | Resolution |
|----------------|-----------------------------|------------|------------|
| **New artifact** `pr-bot-validation.yaml` | OVM `outcome-claims.yaml` (MERGED-PROPOSAL.md §3.1) | No | Distinct artifact names, both peers to `deviation-ledger.yaml` / `grounding-gaps.yaml` |
| **New wave step** 1B.5 (PR discovery) | OVM Step 1B.4 (outcome-claim extraction) | No | 1B.4 (OVM) runs first in UC-2; 1B.5 (BRV) runs only in `--mode pr-bot-validation`; never both in same run |
| **New wave** 1.5 (6-way fan-out) | None — OVM has no inter-wave insert | No | 1.5 is mode-conditional; UC-1/UC-2 runs skip it entirely |
| **New step** 5.x (pre-validation pass) | OVM Step 5.x (outcome-verification pass; MERGED-PROPOSAL.md §3.2) | No | OVM's 5.x runs in UC-2; BRV's 5.x runs in `--mode pr-bot-validation`. Both numbered "5.x" but different modes; numbering convention matches `sc:reflect §4`'s sub-step idiom |
| **Contract fields** `pr_bot_validation_*` prefix | OVM `outcome_claims_*` / `outcome_*` prefix (MERGED-PROPOSAL.md §3.3) | No (namespaced) | Disjoint prefixes by construction; no field overlap |
| **Derived boolean** `pr_bot_validated` | OVM `outcome_verified` (MERGED-PROPOSAL.md §3.3 Change 2) | No | Same pattern, different domain — single-axis routing handles for downstream consumers |
| **Promotion gate cond** 11 | OVM cond 10 (MERGED-PROPOSAL.md §3.5) | No (vacuous-on-other-mode) | Cond 10 vacuous when `mode == pr-bot-validation`; cond 11 vacuous when `mode == post`. A reflect run evaluates only the cond matching its mode; the other is `n/a` |
| **Gate-evaluation field** `pr_bot_validated: pass\|fail\|n/a` | OVM's 11-row gate_evaluation map | Additive | One new row; preserves OVM's a/b sub-split convention; `n/a` mirrors cond 9's vacuous-on-T1 pattern |
| **Evidence-validator responsibility** #3 (bot-finding row presence) | OVM #1 (runbook schema), #2 (finding-row presence) (MERGED-PROPOSAL.md §3.4) | No | Three distinct responsibilities, all policed by the same drop-not-downgrade rule |
| **New ref** `refs/bot-review-sources.yaml` | OVM `refs/claim-extraction-patterns.yaml` (MERGED-PROPOSAL.md §3.1) | No | Distinct ref files; both live under `sc-reflect-protocol/refs/` (no shared-refs directory per OVM §3.7 / Change 5) |
| **Allowed-tools frontmatter** addition | OVM adds `WebFetch, WebSearch` (MERGED-PROPOSAL.md §3.6) | None (additive) | BRV adds `Bash` (already present) and relies on `gh` being available; no new frontmatter entry required |
| **Recursive `Skill sc-reflect-protocol --mode pre` call** in Step 5.x | OVM is not recursive | No | `§17 Boundaries` rule "Will Not — Run reflection on its own intermediate output without explicit `--recursive` flag" requires whitelisting: §3.2 Step 5.x is named as the single legitimate recursion site, gated by `--mode pr-bot-validation` + token-budget envelope |
| **v1.0 → v1.1 contract bump** | Same bump as OVM (MERGED-PROPOSAL.md §6) | None | Both proposals ride the same minor bump; no separate version negotiation needed |
| **Falsifier** (§8 below) | OVM iteration-1 active falsifier `outcome-verification-docker-cli-miss.yaml` (MERGED-PROPOSAL.md §7.1) | No | New falsifier `pr-bot-validation-mixed-buckets.yaml` lives in `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/`; parallel artifact directory |

**No unresolved composition conflicts.** Every BRV-MG addition is either namespaced (contract fields, artifact names), mode-conditional (waves, steps, gate condition), or additive (evidence-validator responsibility, ref file, gate-evaluation row). The two proposals coexist in the same v1.1 release without contract-version conflict.

## 5. How it answers the 10 structural questions (preamble §4)

**Q1: Where does this live?** Inside `sc:reflect-protocol` as a third mode (`--mode pr-bot-validation`). A sibling skill would either re-implement the 9-condition gate (collision risk) or consume reflect's output (relegating bot-review to a *consumer* rather than a *participant* in the gate). The OVM precedent — adding a wave step and gate condition inside reflect rather than splitting off — applies directly.

**Q2: What's the trigger?** Three triggers: (a) explicit `--mode pr-bot-validation` invocation by an operator; (b) CI workflow `.github/workflows/sc-reflect-pr-bot-validation.yml` on every PR `synchronize` / `opened` / `reopened` and on `pull_request_review` when the reviewer is a bot; (c) future `sc:troubleshoot` Wave 6 Phase E (deferred to v1.2; not in this proposal).

**Q3: How does it become a first-class merge gate?** Status check name: `sc-reflect/pr-bot-validation`. Conclusion semantics: `success` (PASS — no PRs blocking merge AND pre-validation gate passed), `failure` (FAIL — ≥1 PR with `blocks_merge: true` OR pre-validation gate failed), `neutral` (DRY-RUN / `--no-post-status-check`), `skipped` (mode != pr-bot-validation). The contract field gating merge is `pr_bot_validated: <bool>` AND `pr_bot_validation_status_check_conclusion: success`. Branch protection on `main` requires the status check to be `success` before `gh pr merge` succeeds.

**Q4: What's the contract shape?** Twelve new fields under the `pr_bot_validation_*` namespace + one derived boolean `pr_bot_validated` (see §3.4 above). Bucket counts (CONFIRMED / STILL_VALID / FALSE_POSITIVE / OUT_OF_SCOPE) per the preamble §3 logic. Per-PR finding paths, aggregated proposal path, pre-validation report path, status-check publication summary all exposed. Reuses OVM's `cannot_validate_without_user_input` / `outcome_verified` semantic patterns by deriving `pr_bot_validated` the same way.

**Q5: How does it compose with the 9+1 (cond 10 from OVM)-condition gate?** Adds **cond 11**, vacuous when `mode != pr-bot-validation`. Distinct layer from cond 10 (work-unit promotion vs PR merge eligibility). A single reflect run evaluates exactly one of {cond 10, cond 11} depending on mode; the other is `n/a`. See §3.6 table above.

**Q6: How does it handle force-pushes / rebases?** Per the preamble §3 bucket logic, which BRV-MG inherits verbatim. The `AUGMENT_SHA_OBSERVED` (captured at per-agent Step 1) is compared against `head_sha_current` (captured at the same step from `gh pr view --json headRefOid`); the `sha_changed` boolean is surfaced in `per_pr_results[].sha_changed`. The CONFIRMED / STILL_VALID / FALSE_POSITIVE / OUT_OF_SCOPE bucketing **is** the re-grounding mechanism: a force-pushed PR re-runs the entire validation against the new HEAD; stale Augment findings that no longer ground get bucketed as OUT_OF_SCOPE (rebased away) or FALSE_POSITIVE (don't ground in current code). The CI workflow's `on: synchronize` trigger ensures every push re-runs the mode.

**Q7: How does it scale?** `--max-prs` flag (default 6, hard ceiling 10). For larger PR sets, the operator partitions across multiple invocations. The default-6 matches preamble §3's empirical pain threshold and the OVM §15 cost envelope (6 parallel `/sc:auggie-review` calls dominate at the T2 band midpoint). When `--budget-remaining` is provided (per `sc:reflect` §4.0 Step 0.9), the mode auto-degrades by clamping `--max-prs` proportionally: `max_prs = min(--max-prs, floor(budget_remaining / 9))` (9 turns per PR is an `[INFERRED]` estimate derived from the §15 T2-midpoint of 52 turns ÷ 6 parallel PRs ≈ 8.7 ≈ 9). Emit `budget_forced_pr_set_clamp: true` in telemetry when this fires.

**Q8: What about other bots?** Configuration via `refs/bot-review-sources.yaml` (see §3.7). New bots are added to the ref without protocol-text changes, mirroring OVM's `refs/claim-extraction-patterns.yaml`. Detection is by GitHub integration login pattern matched against the ref's `login_patterns` list. Per-PR `bot_source` field records which bot produced the original review.

**Q9: How does it interact with `/sc:auggie-review`?** BRV-MG **calls** `sc-auggie-review-protocol` as a Skill (per `sc:reflect §8` integration table) for each per-PR agent, passing `--no-post-pr --no-remediation-offer --depth standard --output-dir /tmp/pr-<N>-auggie-fresh/`. It does not re-implement `/sc:auggie-review` — the validation primitive (every file:line re-grounded against the current diff) is sc-auggie-review's existing contract. BRV-MG adds the *fan-out + aggregation + bucketing + pre-validation* layer on top.

**Q10: How does it interact with `task-builder` + `/task`?** BRV-MG hands off **cleanly, not subsumes**. The third mode terminates at the pre-validation gate result + status-check publication (Phase 4 of the preamble pipeline). Phase 5 (execute remediation) remains an explicit operator step: the `REPORT.md` recommends `Skill task-builder` with `BUILD_REQUEST` pointing at `<output>/PROPOSALS-normalized.md`, then `/task <generated-mdtm-path>`, then `/sc:reflect --mode post --diff <pre-task-ref>..HEAD --tasklist <mdtm-path>`. Per `§17 Will Not` ("Auto-execute a Tier 3 remediation task — task-builder produces a file, the user runs /task"), this boundary is preserved. The handoff is wired via Wave 6 (existing) when `--remediate` is set on the third-mode invocation; default off.

## 6. Trade-offs and risks

**Token cost.** Solidly T2 band (~35-70k Claude orchestration + ~10-25k auggie offloaded) per OVM §15. Six parallel `/sc:auggie-review` calls dominate. At `--max-prs 3`, drops to ~T1.5 (~20-40k Claude). At `--max-prs 1`, drops to T1+ (~10-15k Claude). The cost scales linearly with `--max-prs`, which is the right scaling property.

**Wall-clock cost.** ~10-20 min for 6 PRs (preamble §3 empirical band). The 6-way parallelism is load-bearing per preamble §5 constraint; serializing would push to ~60-120 min, well past the team's pain threshold. The CI workflow's runner timeout MUST be set to ≥30 min.

**False-positive risk on bot-finding cross-validation.** The bucketing logic produces FALSE_POSITIVE only when the cited file:line doesn't ground in current code. The bigger risk is the inverse — false-negative CONFIRMED: a bot finding that fresh-auggie missed AND that the per-agent didn't ground via Read. Mitigation: STILL_VALID bucket explicitly catches "current code still has the issue, but fresh auggie missed it" via a Read of the cited file:line per preamble §3 Step 3. This is the same drop-not-downgrade rigor as §11.2.

**What happens when bots disagree.** Out of scope for v1.1 (per preamble §9 — "bot disagreement adjudication (defer to v1.2)"). If a PR has both Augment and CodeRabbit reviews, BRV-MG runs the bucketing logic against each bot's findings independently (one per_pr_results entry per bot per PR), and the aggregate `blocks_merge` is the OR across bots. v1.2 may add an adversarial-merge step here using `sc:adversarial-protocol` (Mode A `--compare`).

**Drift in the `gh` CLI surface.** Per OVM §5 ("`gh` CLI is available — treat as first-class tool"), this is a shared assumption. If `gh pr view --json` schema changes (e.g., GitHub renames `headRefOid` → `headOid`), the per-agent prompt breaks. Mitigation: pin `gh` version in CI; document the expected schema in `refs/bot-review-sources.yaml` as `gh_schema_version: 2.40.0+` with a one-line freshness check in Wave 1 Step 1B.5 (`gh --version | head -1` parsed against minimum).

**Mechanism risk: per-agent non-determinism.** Different per-agent runs against the same PR might bucket differently (LLM judgement variance). Mitigation: bucketing is grounded in deterministic primitives (file existence, line existence, diff hunk membership); the only LLM-judgement component is the CONFIRMED-vs-STILL_VALID distinction, which is a soft signal anyway (both block merge identically). Eval rubric (§12.5 falsifier in §8 below) catches systematic bucket drift.

**Recursive `--mode pre` invocation cost.** Step 5.x invokes `Skill sc-reflect-protocol --mode pre` on `PROPOSALS-normalized.md`. This is a T1-band recursive cost (~3-8k Claude), bounded at 2 iterations per Step 5.x. Total added cost ~6-16k Claude in the worst case. Tracked in telemetry as `recursive_reflect_invocations: <int>`.

**CI cost.** Per-PR-push run cost is the load-bearing concern. At ~$0.50-$1.50 per T2 reflect run (rough Anthropic billing midpoint per `[INFERRED]` estimate from §15 token bands), 10+ PRs/week × 3+ pushes each = ~$15-$45/week. Acceptable per preamble §2 ("10+ PRs / week with bot reviews" pain threshold) but the operator should know.

## 7. Backward-compat (v1.0 → v1.1, composed with OVM's bump)

**Version bump:** minor 1.0 → 1.1, same bump as OVM (MERGED-PROPOSAL.md §6). Both proposals ship in the same release.

**All new contract fields are additive top-level** per `§9.4` unknown-field-tolerance rule. Existing consumers (`sc:troubleshoot` Wave 6, `superclaude sprint run`, `sc:task` end-of-task hook, `sc:roadmap`, `sc:tasklist`, `task-builder`, Wave 7 promotion adapters, eval CI, meta-eval per `§9.3` consumer field map) ignore the new fields unless they opt in.

**`status` enum unchanged.** A PR-bot-validation run emits `status: success` when the mode completed (regardless of bucket outcomes); the merge-blocking signal is `pr_bot_validated: false`, not `status: failed`. This mirrors OVM's "deferred-with-runbook = honest success" pattern (MERGED-PROPOSAL.md §2).

**`promotion_action` enum unchanged.** The third mode's Wave 7 mutation is a status-check POST, not a folder move. The promotion-log records `action: moved` for the status-check publication; the destination is a GitHub status URL rather than a filesystem path. The `promotion_destination` field carries the URL.

**Consumer updates per `§9.3` map:**

- **`sc-troubleshoot` Wave 6:** no required change. Can opt in to `pr_bot_validated` to gate Phase D escalation on a PR that hasn't passed bot-review validation.
- **`superclaude sprint run` (executor.py):** opt-in. A new TurnLedger consumer field can halt the phase when a sprint touches a PR with `pr_bot_validated: false`.
- **`sc-task-protocol` end-of-task hook:** unaffected.
- **`sc:roadmap` / `sc:tasklist`:** unaffected.
- **`task-builder`:** opt-in. Can ingest `pr_bot_validation_path` to materialize a remediation follow-up task automatically (BUILD_REQUEST from the normalized proposals file).
- **CI:** new workflow `.github/workflows/sc-reflect-pr-bot-validation.yml` added; existing workflows unaffected.

**Migration window per `§9.4`:** one full minor release cycle. No deprecations needed (purely additive).

**Composes with OVM's v1.1 deferred-hardening** (MERGED-PROPOSAL.md §6 / §19.2): BRV-MG's falsifier (§8 below) is a peer to OVM's `outcome-verification-docker-cli-miss` and `outcome-verification-deferred-runtime-config` cases. The v1.1 sufficiency claim per §11.0 is strengthened by both proposals (broader sufficiency surface).

## 8. Falsifier — eval case `pr-bot-validation-mixed-buckets`

Modeled on `§12.5`'s `T2-converges-on-wrong.yaml` skeleton and OVM's iteration-1 active falsifier (`outcome-verification-docker-cli-miss.yaml`, MERGED-PROPOSAL.md §7.1). Lives at `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/pr-bot-validation-mixed-buckets.yaml`.

```yaml
id: pr-bot-validation-mixed-buckets
type: held-out adversarial
status: active   # iteration-1 fixture per preamble §6 (3-finding fixture is concrete)
fixture: fixtures/pr-bot-validation-mixed-buckets/
setup: |
  Fixture contents:
  - One mocked open PR #999 against a synthetic Coder fork.
  - One Augment review with three inline findings:
    F1: file=src/foo.py, line=42, claim="missing null check"
        Ground truth: CONFIRMED — fresh auggie pass also surfaces it AND line 42 resolves.
    F2: file=src/bar.py, line=88, claim="off-by-one in loop bound"
        Ground truth: FALSE_POSITIVE — line 88 doesn't ground (claim references non-existent code path).
    F3: file=src/baz.py, line=15, claim="None"  (no Augment finding here; ADDED by fresh-auggie pass)
        Ground truth: STILL_VALID (different line from any Augment finding) — fresh auggie surfaces
        a regex injection at src/baz.py:15 that Augment missed; line 15 resolves to current code.
  - Mocked AUGMENT_SHA_OBSERVED matches current HEAD (no force-push complication).
  - bot-source: augment (login matches refs/bot-review-sources.yaml augment pattern).

pre_seeding_mechanism:
  delivery_channel: fixture   # the fixture IS the test; no anchoring seed needed
  rationale: |
    Mirrors the preamble §6 falsifier shape exactly: 1 CONFIRMED + 1 FALSE_POSITIVE
    + 1 STILL_VALID. Tests whether BRV-MG's bucketing logic correctly routes each
    finding to its expected bucket AND whether the merge gate blocks until remediation.

expected:
  pr_set.accepted_count: 1
  per_pr_results[0].pr_number: 999
  per_pr_results[0].bot_source: augment
  per_pr_results[0].buckets.confirmed: 1       # F1
  per_pr_results[0].buckets.still_valid: 1     # F3
  per_pr_results[0].buckets.false_positive: 1  # F2
  per_pr_results[0].buckets.out_of_scope: 0
  per_pr_results[0].top_severity: medium       # any severity ≥ medium triggers blocks_merge
  per_pr_results[0].blocks_merge: true         # CONFIRMED + STILL_VALID > 0 AND severity ≥ medium
  aggregate.total_confirmed: 1
  aggregate.total_still_valid: 1
  aggregate.total_false_positive: 1
  aggregate.prs_blocking_merge: [999]
  pre_validation_gate.status: passed           # PROPOSALS-normalized.md is well-formed
  pr_bot_validated: false                      # derived: prs_blocking_merge != [] → false
  status_check.conclusion: failure             # PR cannot merge until remediation
  status: success                              # the mode completed cleanly (merge-block is via status_check, not status)
  pr_bot_validation_complete: true

assertion_pass: |
  per_pr_results[0].buckets.confirmed == 1 AND
  per_pr_results[0].buckets.still_valid == 1 AND
  per_pr_results[0].buckets.false_positive == 1 AND
  pr_bot_validated == false AND
  status_check.conclusion == "failure"

severity: AUTO-FAIL if pr_bot_validated == true
  OR if status_check.conclusion == "success"
  OR if any bucket count is wrong by ≥1
  (any of these means BRV-MG either let a blocking finding through (false-clean-ship)
   OR misclassified a finding (bucketing rot) → the structural fix does NOT close
   the bot-review-validation merge-gate gap → proposal disproven)

follow_on_assertion: |
  After fixture re-run with the F1 and F3 findings remediated (file edits applied
  via a test-only patch step), re-run BRV-MG. Expected:
    per_pr_results[0].buckets.confirmed: 0
    per_pr_results[0].buckets.still_valid: 0
    pr_bot_validated: true
    status_check.conclusion: success
  This is the round-trip: blocked → remediated → unblocked, end-to-end.
```

A passing run on this fixture is the empirical proof that BRV-MG closes the bot-review-validation merge-gate gap. A failing run (auto-fail severity met) falsifies the proposal: the bucketing logic OR the status-check semantics is broken, and a different structural mechanism is needed. The follow-on assertion proves the round-trip works (the operator-driven Phase 5 remediation actually flips the gate).

## 9. Out-of-scope items

1. **Auto-execution of remediation** — per `§17 Will Not` ("Auto-execute a Tier 3 remediation task — task-builder produces a file; the operator runs `/task` themselves"). The third mode terminates at the pre-validation gate + status-check publication. Phase 5 of the preamble pipeline is operator-driven.
2. **Bot disagreement adjudication** — deferred to v1.2 per preamble §6 §9. When multiple bots review the same PR, BRV-MG aggregates per-bot independently; conflict resolution between bot findings is not addressed here. A future v1.2 may add a `sc:adversarial-protocol --compare` step here.
3. **Non-GitHub PR platforms** — out of scope per preamble §9. GitLab MRs, Bitbucket PRs, Gerrit changesets are not supported. The `gh` CLI assumption is load-bearing.
4. **Branch-protection configuration** — the proposal names the exact status-check name (`sc-reflect/pr-bot-validation`) but does not configure branch protection on `main`. That's a one-time repo-admin task per CLAUDE.md secrets discipline (the same issue tracker entry as the `P-7 secret scan` check).
5. **Live runtime hooks** — per OVM §5 ("No live runtime hooks") inherited; all grounding is via `gh` CLI + filesystem reads.
6. **Cross-tasklist deviation-pattern memory across PRs** — deferred per OVM §19.5. Existing per-project memory namespace is sufficient for v1.0.
7. **Auto-rollback of a PR merge** — out of scope. Once the status check passes and the operator merges, the PR is merged. Reverting is a separate `gh pr create` flow.
8. **PR comments in addition to status check** — the per-agent invocations use `--no-post-pr` per preamble §3 Guardrails ("we do not want 6 duplicate review comments hitting GitHub"). The mode publishes a status check, not inline review comments. A future v1.2 may add a single consolidated PR comment summarizing the bucketed result, but not 6 separate comments.

---

**End of proposal.** This document is the v1.1 amendment surface for `sc:reflect`; composed with OVM's MERGED-PROPOSAL.md, the pair lands in the same minor bump as additive contract fields, namespaced artifacts, and disjoint gate conditions. No unresolved conflicts.
