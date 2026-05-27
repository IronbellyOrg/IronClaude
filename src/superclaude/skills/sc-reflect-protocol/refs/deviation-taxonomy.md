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

**Gold-standard reference.** Inline documentation (comment, commit body, task log) + spec acceptance-criteria check (no contradictions).

**Default remediation.** Surface in report with `Documentation note` recommendation — propose updating the spec/tasklist so future runs match reality. No Tier 3 task unless `--remediate-docs` is set.

## Drift

**Definition.** A silent change not in the original spec/tasklist with no inline rationale. The work *happened* without explicit authorization and without recorded justification.

**Detection signals.**

- Diff hunk does NOT map to any tasklist item.
- No commit-body rationale, no inline comment, no task-log entry explaining the change.
- Does NOT contradict any acceptance criterion (this is what distinguishes drift from regression).

**Gold-standard reference.** Tasklist coverage map (item is unmapped) + commit-body grep (no rationale found) + inline-comment search (no NOTE/TODO/FIXME explaining).

**Default remediation.** Surface in report with `Authorize-or-revert decision required`. If `--remediate`, offer Tier 3 task to either (a) backfill spec to authorize, or (b) revert the drift.

## Regression

**Definition.** A change that *contradicts* an acceptance criterion, an explicit constraint in the spec, or a previously-passing test. The work undoes or violates a documented commitment.

**Detection signals.**

- Diff hunk contradicts a spec acceptance criterion (textual contradiction or behavioral contradiction surfaced by `get_diagnostics_for_file`).
- A test that previously passed now fails after the diff (detect via task log or by re-running tests if `--rerun-tests` set).
- A documented invariant in the spec or in a `@invariant` comment is violated.

**Gold-standard reference.** Spec acceptance-criteria section + test-suite state pre/post (from task log or re-run) + invariant comments.

**Default remediation — unconditional Tier 3 escalation.** Regression is the **only class** that *unconditionally* triggers a Tier 3 remediation offer in Wave 6 when `--remediate` is set. It also **unconditionally forces escalation to Tier 2** per §5.3 rule 3 — the regression is debated by ≥2 reviewers before the report ships. No other deviation class carries an unconditional escalation; for Drift/Necessary/Authorized the escalation gate depends on other rule-set conditions.

## Classification precedence

When multiple signals match, precedence is:

**Regression > Drift > Necessary > Authorized**

Worked examples:

- A diff hunk that contradicts a spec criterion but has an inline TODO rationale is still a **Regression** — rationale does not authorise contradiction.
- A diff hunk with no tasklist mapping AND no rationale AND no contradiction is **Drift**, not Necessary.
- An authorized scope addition that also happens to contradict a spec criterion is a **Regression** — explicit authorization does not override an acceptance-criteria contradiction.

This precedence is also the union rule for the per-file aggregation mode (see *Aggregation* above): a file's class is the max-precedence class across its hunks.

## Grounding-gaps parallel artifact

The taxonomy is **4 categories**, not 5. There is no `unknown` deviation class.

When a hunk **cannot be classified due to insufficient evidence** (distinct from multi-signal ambiguity, which is resolved by precedence above), the orchestrator does NOT add it to `deviation-ledger.yaml`. Instead, it writes a row to `<output>/grounding-gaps.yaml`.

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
