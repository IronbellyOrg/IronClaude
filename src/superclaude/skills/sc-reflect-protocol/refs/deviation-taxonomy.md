# Deviation Taxonomy

Reference for Wave 1B (UC-2 deviation detection) and Wave 5 (synthesis classification).

Reflection's defining contribution beyond a generic verification protocol is *classifying* every divergence between expected and actual work into a concrete, decision-driving category. The taxonomy is **4 categories** — `evidence-insufficient` findings route to a parallel artifact (see *Grounding-gaps parallel artifact* below), not a 5th category.

The **gold-standard reference** for "what was expected" is the **driving spec/tasklist** (the artifact the agent was instructed to fulfil) — not the executor's commit message, which is reviewer-side narrative.

Each category has: definition, detection signals, gold-standard reference, default remediation.

## Aggregation

When the diff under audit contains **more than 100 hunks**, taxonomy classification runs on **aggregated-by-file summaries** (one deviation entry per file) rather than per-hunk.

**Per-file union rule.** A file's `deviation_class` is the highest-precedence class observed across its hunks under the precedence ordering defined in *Classification precedence* below (Regression > Drift > Necessary > Authorized). One file may contribute exactly one row to `deviation-ledger.yaml` in per-file mode.

**Per-hunk evidence is preserved** as an auxiliary artifact at `<output>/per-hunk-evidence.yaml`. This file is **not consumed by the gate** — it exists so the operator can drill down from a per-file summary to the originating hunks.

**Telemetry.** The orchestrator emits:

- `deviation_aggregation_mode: per-file | per-hunk` — always set.
- `hunk_count: <int>` — emitted only when `per-file` mode fires, so the operator can see which run triggered aggregation.

**Threshold rationale.** The 100-hunk threshold is a heuristic to keep `deviation-ledger.yaml` bounded for human review. It is **NOT** a budget-policy decision and does not interact with the §11.5 citation budget.

## Authorized

**Definition.** A scope addition that was *explicitly* approved by an authoritative artifact (an updated tasklist, a referenced spec amendment, a PR description with explicit reviewer sign-off, or a directly-cited user instruction in the task log).

**Detection signals.**

- Diff hunk maps to a tasklist item AND that tasklist item was added (not original) AND the addition has a commit/timestamp predating the diff.
- Task log contains explicit "user approved scope expansion to include X" or equivalent.
- Spec doc has a revision-history entry adding the relevant requirement.

**Gold-standard reference.** Updated tasklist file + revision-history of spec + task log explicit-approval lines.

**Default remediation.** None. Document in the report. No Tier 3 task.

## Necessary

**Definition.** A divergence forced by a technical constraint discovered during execution, documented inline (commit message body, code comment, or task log entry) with a clear rationale, but *not* pre-authorized.

**Detection signals.**

- Diff hunk includes a TODO / NOTE / FIXME explaining why the original plan could not be followed.
- Commit message body (not subject) contains the rationale.
- Task log contains "blocked by X, deviated to Y" entry.
- The deviation does NOT contradict any acceptance criterion in the spec.
- A `third_party_api_verified` flag (FR-4): the divergence resolves to a verified external-API constraint — `find_symbol(search_deps:true)` confirmed the upstream third-party behavior the work conforms to — supporting classification as Necessary (forced by a real upstream constraint) rather than Drift.

**Gold-standard reference.** Inline documentation (comment, commit body, task log) + spec acceptance-criteria check (no contradictions).

**Default remediation.** Surface in report with `Documentation note` recommendation — propose updating the spec/tasklist so future runs match reality. No Tier 3 task unless `--remediate-docs` is set.

## Drift

**Definition.** A silent change not in the original spec/tasklist with no inline rationale. The work *happened* without explicit authorization and without recorded justification.

**Detection signals.**

- Diff hunk does NOT map to any tasklist item.
- No commit-body rationale, no inline comment, no task-log entry explaining the change.
- Does NOT contradict any acceptance criterion (this is what distinguishes drift from regression).
- A `serena_summary_corroboration: disagree` (FR-5): the Serena change-summary contradicts the supplied diff, reinforcing the Drift classification. (`agree` / `partial` / `unavailable` do NOT boost Drift — `unavailable` is the cross-session no-signal default.)

Runtime-surface note (FR-RSR): unmapped is not the same signal as unreached. A decided runtime-surface `UNREACHED` finding is governed by SKILL.md §10.9 and maps onto the existing taxonomy by evidence; an unmapped-but-not-contradictory UNREACHED maps here to Drift, while contradiction maps to Regression.

**Gold-standard reference.** Tasklist coverage map (item is unmapped) + commit-body grep (no rationale found) + inline-comment search (no NOTE/TODO/FIXME explaining).

**Default remediation.** Surface in report with `Authorize-or-revert decision required`. If `--remediate`, offer Tier 3 task to either (a) backfill spec to authorize, or (b) revert the drift.

## Regression

**Definition.** A change that *contradicts* an acceptance criterion, an explicit constraint in the spec, or a previously-passing test. The work undoes or violates a documented commitment.

**Detection signals.**

- Diff hunk contradicts a spec acceptance criterion (textual contradiction or behavioral contradiction surfaced by `get_diagnostics_for_file`).
- **A test that previously passed now fails after the diff — detected by the default-on §6.1 step 5.5 verification triangle (`execute_shell_command`), not the task-log self-report.** A non-zero exit that the exit-code mapping (below) classifies as Regression sets `verification_regressions_detected += 1` → `regression_present: true`. `--no-verify` is the opt-out; `--rerun-tests` is a deprecated alias for "verification on". When verification is unavailable, this degrades to the task-log claim with a Grounding Gap entry.
- A documented invariant in the spec or in a `@invariant` comment is violated.

**Gold-standard reference.** Spec acceptance-criteria section + **verified test-suite state pre/post (from the §6.1 step 5.5 `execute_shell_command` exit codes, falling back to the task-log claim only when verification is unavailable)** + invariant comments.

**Default remediation — unconditional Tier 3 escalation.** Regression is the **only class** that *unconditionally* triggers a Tier 3 remediation offer in Wave 6 when `--remediate` is set. It also **unconditionally forces escalation to Tier 2** per §5.3 rule 3 — the regression is debated by ≥2 reviewers before the report ships. No other deviation class carries an unconditional escalation; for Drift/Necessary/Authorized the escalation gate depends on other rule-set conditions.

## Classification precedence

When multiple signals match, precedence is:

**Regression > Drift > Necessary > Authorized**

Worked examples:

- A diff hunk that contradicts a spec criterion but has an inline TODO rationale is still a **Regression** — rationale does not authorise contradiction.
- A diff hunk with no tasklist mapping AND no rationale AND no contradiction is **Drift**, not Necessary.
- An authorized scope addition that also happens to contradict a spec criterion is a **Regression** — explicit authorization does not override an acceptance-criteria contradiction.

This precedence is also the union rule for the per-file aggregation mode (see *Aggregation* above): a file's class is the max-precedence class across its hunks.

## Verification exit-code → deviation-class mapping (FR-4)

A non-zero exit from the §6.1 step 5.5 verification triangle is **NOT** uniformly a Regression. Each invocation's exit code is classified per-tool; an unmapped exit defaults to **Grounding Gap** (conservative — never silently a Regression). This mapping feeds the precedence union above *by evidence*, not by assignment — only the rows mapped to Regression set `regression_present`.

| Tool / exit | Class | Effect |
|-------------|-------|--------|
| `pytest` exit 1 (test failed) | **Regression** | `verification_regressions_detected += 1`; `regression_present: true` |
| `pytest` exit 2/3 (collection / internal error) | **Grounding Gap** | NOT a regression; `needs_human_decision` |
| `pytest` exit 5 (no tests collected) | **Drift / coverage** | claimed-added test absent; NOT a regression |
| `ruff` / `mypy` exit 1 (lint / type finding) | `S_dev_density` signal | feeds the rubric; NOT `regression_present` |
| any tool exit 124 (timeout) | **Grounding Gap** | `verify_timeout_hit: true`; NOT a regression |
| flaky (single retry-on-failure flips result) | **Grounding Gap** + `verify_flaky_suspected: true` | retry once BEFORE classifying as Regression |
| any unmapped exit code | **Grounding Gap** | conservative default |

(Full per-tool table including `make`/`cargo`/`npm`/`tsc` is enumerated during eval-authoring, OQ-M9.)

## Contracted-sink reachability / oracle-admissibility → deviation-class mapping (FR-RH1)

The §6.1 step-5.6 contracted-sink reachability & oracle-admissibility gate (UC-2) feeds the same precedence union *by evidence, not by assignment*, and adds **no 5th category** — `unreachable` routes to the existing **Regression** class and `unproven` routes to the existing **Grounding Gap** parallel artifact below. This is a sibling finding-modifier to the Runtime-surface UNREACHED note (FR-RSR, SKILL.md §10.9) above: both map onto the same 4 classes, neither is a new class, and neither subsumes the other (FR-RSR governs the static runtime-surface sweep; FR-RH1 governs the real-boot contracted-sink gate, keyed on `reachability_unreachable` / `reachability_unproven` counters).

| Reachability / oracle evidence | Class | Effect |
|---|---|---|
| Real boot ran and observed the contracted sink **absent** | **Regression** | `reachability_unreachable += 1`; `verification_regressions_detected += 1`; `regression_present: true` |
| Blocking annotated (`durable_sink:` / `@sink`) sink present, but no real-boot proof (static binding absence / discarded emitter result / unresolved sink identity / oracle mismatch / real-boot-unavailable) | **Grounding Gap** | `reachability_unproven += 1`; `needs_human_decision: true`; Tier-1 preserved |
| Binding present, emitter result checked, oracle observes the contracted sink | **none / reachable** | clean |

**Skip / fallback are NOT deviations.** `--no-reachability`, `spec-and-tasklist-absent`, and `no-side-effect-requirements` are telemetry-only skips, and semantic-only classification without an explicit `durable_sink:` / `@sink` annotation is advisory telemetry only: none of these may create a Grounding Gap, increment `reachability_unproven`, set `needs_human_decision`, or change `status`. There is no `deviation_count_by_class.reachability` counter.

## Grounding-gaps parallel artifact

The taxonomy is **4 categories**, not 5. There is no `unknown` deviation class.

When a hunk **cannot be classified due to insufficient evidence** (distinct from multi-signal ambiguity, which is resolved by precedence above), the orchestrator does NOT add it to `deviation-ledger.yaml`. Instead, it writes a row to `<output>/grounding-gaps.yaml`.

Runtime-surface UNREACHED-by-evidence (SKILL.md §10.9 / FR-RSR) follows the same structural separation: degraded, comment-ambiguous, oracle-routed, or rootwalk-incomplete reachability findings have no decided `UNREACHED` verdict to classify, so they route here as Grounding Gaps and remain outside `deviation-ledger.yaml`. Decided UNREACHED findings are not a 5th class; they map to Regression or Drift by evidence.

**Required fields (byte-exact schema from spec §10.6):**

```yaml
- hunk_ref: <file:line-range>
  evidence_missing: <what is missing — e.g., "no commit body, no inline comment, no task-log entry, spec section ambiguous">
  why_not_classifiable: <one-sentence reason>
  next_evidence_needed: <what would resolve — e.g., "ask user whether feature X was authorized">
  owner: user             # default; can be `reviewer` if a reviewer round can resolve
  decision_needed_by_user: true | false
```

**Non-empty consequences.** When `grounding-gaps.yaml` is non-empty:

- `status: partial` is **forced** in the return contract (cannot be `complete`).
- `needs_human_decision: true` is emitted to the return contract.
- The REPORT.md Grounding Gaps section enumerates each row with the missing-evidence rationale.

**Structural separateness.** `grounding-gaps.yaml` is a **distinct artifact** from `deviation-ledger.yaml`. The two files never share rows. This separation absorbs V4's `unknown`-class semantics (with V4's required-field rigor) while preserving V2's Grounding Gap routing mechanism. The 5th deviation category was explicitly rejected in §17.7 Kill List; see that section for the rationale.
