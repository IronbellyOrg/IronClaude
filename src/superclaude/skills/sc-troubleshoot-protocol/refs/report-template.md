# REPORT.md Template

The final deliverable of every `/sc:troubleshoot` invocation, regardless of tier. Loaded only in Wave 5.

## Template

````markdown
# Troubleshoot Report

**Target**: <one-line: the symptom or scope as given>
**Type**: <bug|performance|security|build|deployment|test|auto>
**Tier reached**: <1|2|3>
**Confidence**: <0.0–1.0>
**Status**: <success|partial|blocked|failed> <!-- Same final merged status as audit footer and TFEP: failed > blocked > partial > success. -->
**Escalation reason**: <none|low_confidence|multi_domain|forced_by_depth_deep|intermittent|not_reproducible|security_caution|source_only_dynamic_claim|split_pending>
**Test is wrong**: <true|false> <!-- See "Test-is-wrong rule" below. When true, surface `Test file to update` on its own line and DO NOT recommend code changes as the primary fix. -->
**Test file to update**: <absolute or repo-relative path when test_is_wrong=true, otherwise omit this line>
**Behavior is documented**: <true|false|n/a> <!-- See "Behavior-is-documented rule" below. When true, the observed behavior matches the documented contract AND the recommended remediation is a SPEC/DOCS change (not a test change — that's the test_is_wrong=true case). Mutually exclusive with `Test is wrong: true` by construction (3-case decomposition: see SKILL.md derivation rule). `n/a` when --no-doc-discovery suppressed Wave 1.5. -->
**Doc context card**: <repo-relative path to <output-dir>/doc-context.md when Wave 1.5 ran (path is present even if the card's sections all read "None found"); `null` ONLY when `--no-doc-discovery` was set>
**Diagnosability audit**: SKIPPED (--no-diagnosability-audit, user-bypassed) <!-- Render this line ONLY when --no-diagnosability-audit was set. Omit the line entirely when Wave 1.6 ran (the result lands in the Diagnosability Context section instead). -->
**Duration**: <seconds>
**Date**: <ISO 8601>

---

> ⚠ **Diagnosability Caveat**: Your hypothesis depth was constrained by insufficient evidence. See
> Diagnosability Context and pending evidence in Next Steps below. Execution remains subject to
> capability, authorization, transport and round-cap restrictions.

<!-- Render the Diagnosability Caveat banner ONLY when `--depth deep` AND `diagnosability_verdict ∈ {insufficient, partial}`. Otherwise omit the banner block entirely. -->

## Summary

2–4 sentences. State the symptom and the evidence-supported conclusion. When Diagnosis is UNDETERMINED/inconclusive, say no unique cause is established, name the missing observation and next discriminating action; do not present a candidate as the answer or recommend a causal fix. Otherwise state the supported diagnosis and proposed fix. Lead with limitations for partial, blocked or failed status, preserving the blocking/failure reason and execution restrictions.

## Documentation Context

Wave 1.5 documentation grounding result. ≤6-line summary of the Documentation Context Card.

- **Relevant refs**: <comma-separated doc paths from Branch A + Branch B + Branch C, or "None found">
- **Documented behavior**: <one-line summary of what the docs say about the affected surface>
- **Restrictions honored**: <one-line list of doc-cited constraints the chosen fix respects>
- **Restrictions overridden**: <one-line list of doc-cited constraints the chosen fix violates; cite the doc-update + fix bundle if applicable, otherwise "None">
- **Card path**: <output-dir>/doc-context.md

If `--no-doc-discovery` was set, omit this section entirely and add a line to **Grounding Gaps**: "Documentation grounding skipped by `--no-doc-discovery`."

## Diagnosability Context

Wave 1.6 diagnosability audit result. Always rendered when Wave 1.6 ran (omit only when `--no-diagnosability-audit` was set — then add the bypass line to **Grounding Gaps** instead).

**Verdict**: <sufficient | partial | insufficient | unknown>
**Complexity classification**: <trivial | non-trivial>
**Captured-bytes (failing run)**: <bytes-or-n/a>

<≤6-line summary of the Diagnosability Context Card. Names the existing instrumentation in 1 line, names the gap in 1 line, names the implication for diagnosis confidence in 1 line.>

(Full card: <abs path to <output-dir>/diagnosability-context.md>)
(Tasklist (informational): <abs path to <output-dir>/diagnosability-tasklist.md>, if emitted)

When `diagnosability_hard_stop=true`, render the halt explanation from the **Hard-stop variant** here, retaining card/tasklist pointers. Keep Diagnosis in its UNDETERMINED form, root_cause_summary empty, and all pending rows in Next Steps; the halt explanation replaces neither section.

## Diagnosis

The single chosen hypothesis — or the UNDETERMINED form below when the headline-confidence coupling fires. The word "probable" before an enum value is forbidden anywhere in this section. Format:

**Root cause**: <one-line>

**Cause class**: <from the triage checklist>

**Detailed explanation**: 1–2 paragraphs. Why this code produces the observed symptom. Reference the evidence section, don't restate it.

**UNDETERMINED form** (mandatory on hard-stop or whenever evidence has not distinguished a unique cause, including both-consistent outcomes; also mandatory when calibrated confidence < 0.5 — missing or non-numeric counts as 0.0 — OR the headline value is absent from captured failing-run output spans with run/arm/command provenance; use Wave 5's `observation_paths` corpus, never generated producer tables, cards, drafts or definition prose, even if embedded in an observation file; `root_cause_summary` is then the empty string and stays empty in TFEP):

**Root cause**: UNDETERMINED — among {<every `surviving=yes` row of `<output-dir>/producers.md`, as `file:line`, comma-separated; `indistinguishable: <a>,<b>` from the tasklist header when present>}

With no producer menu (including audit bypass), use `UNDETERMINED — producer menu unavailable`; other applicable forms are `UNDETERMINED — no comparator` and `UNDETERMINED — CI verdict unobserved`. Never fabricate rows or a unique cause.

**Cause class**: <from the triage checklist, unchanged>

**Falsifiers** (one line per `## Discriminator rows` entry of `<output-dir>/diagnosability-tasklist.md`; copy predictions and consistent/refuted/inconclusive mapping without strengthening them; absent tasklist ⇒ explicitly state that discriminator evidence is missing):
- Core `<row>`: <observed/pending + reason>; predictions <true/false cells or justified unknown>; outcomes <preregistered mapping>; <missing observation needed to distinguish the relevant claim>.
- Optional `<row>`: informational <observed/pending + reason>; <preregistered outcomes>; not a diagnosis decision or status prerequisite.

Only relevant unresolved core evidence contributes partial, never lowering blocked/failed. Equal predictions are non-discriminating; unobserved is not false, and consistent is not confirmed. Do not declare a claim true merely because one compatible value was captured. Enabling tasks reference these measurement IDs and operational verification, not invented causal predictions.

**Detailed explanation**: which rows were run this round (captured spans in `tier1-observation.md`) and which remain; no mechanism narrative for a producer that has not been discriminated.

## Evidence

A numbered list of evidence items, each a `file:line` citation with a quoted snippet OR a command + actual output. **Every item in this list will be validated in the Wave 5 file:line check** — unfounded items are dropped before the report ships.

1. `path/to/file.py:142` — `result = Path(scratch_root) / "foo"` (no `pathlib.Path` import in the file)
2. Command: `uv run pytest tests/path/to/test_eval_run.py::test_basic -x` → output shows `NameError: name 'Path' is not defined`
3. ...

If a citation in a hypothesis card could not be validated, it does not appear here — it appears in **Grounding Gaps** below.

## Proposed Fix

For an established diagnosis, describe the proposed change concretely (files and diff). For UNDETERMINED/inconclusive diagnosis, write `No causal fix established`, identify the next discriminating observation, and optionally describe a clearly conditional proposal with its validation prerequisite; omit causal Files to change/Test to verify/Apply with recommendations. Do not promote that proposal into TFEP's solution_summary; use the missing-observation/next-action description there, or empty when blocked/failed.

**Files to change**:
- `path/to/file.py` — <one-line summary of change>

**Files that MUST NOT change** (REQUIRED when `Test is wrong: true` OR `Behavior is documented: true` in the header; OMIT this subsection otherwise):
- `path/to/production_file.py` — <one-line on why this is the wrong file to modify; cite the asymmetric cost — typically "regresses documented behavior at <spec ref>" or "breaks contract relied on by <consumer>">

**Test to verify**:
- `path/to/test_file.py::test_name` should pass after the fix
- (or, "add new test: ...")

**Apply with**: `/sc:troubleshoot --fix ...` (re-run with `--fix` to authorize the Tier 3 task-builder chain), or apply manually.

## Alternative Fixes Considered

**Tier 1 only**: omit this section.

**Tier 2 (Wave 4 ran)**: list the losing fix proposals from the adversarial debate. For each:

- **Fix N — `<one-line>`** (from `<agent-name>`)
  - Rejected because: <one-line — typically "weaker evidence", "higher risk", or "fails edge case X">

This section documents the road not taken so the user can re-litigate if they disagree with the chosen fix.

## Risk + Rollback

What to watch after applying the fix:

- **Likelihood of regression**: <low|medium|high> in <which area>
- **Test coverage of the changed code**: <good|partial|none> — if partial/none, the user should add a regression test before merging
- **Rollback**: <one-line on how to revert if the fix turns out wrong>

For security and performance fixes, this section is mandatory and must be specific. For typos and import fixes, "single-line change, revert with `git revert`" is sufficient.

## Follow-up tasks

Optional section for non-blocking secondary recommendations that are NOT the primary fix. Use when the diagnosis surfaces work worth tracking but separate from the chosen fix — e.g., hardening a related code path, adding observability, updating documentation, deleting dead code. When `Test is wrong: true`, this is where any production-code hardening recommendation goes (the primary fix stays test-only).

Each item should be:

- One-line summary
- (optional) `Suggested type`: `bug` | `refactor` | `docs` | `observability` | `test`
- (optional) Cited evidence pointer to the line that motivated the follow-up

If there are no follow-ups, write "None."

## Grounding Gaps

What the skill could **not** verify. If status ≠ success (partial, blocked, or failed), the items here explain why. Examples:

- "Reproducer not available in sandbox — relied on user-pasted stack trace"
- "MCP `auggie` was unavailable; grounding used `Grep`/`Glob` only"
- "Hypothesis card from `quality-engineer` cited line 88 of test_foo.py but that file is only 60 lines long — citation dropped"
- "Documentation grounding skipped by `--no-doc-discovery` — diagnosis is not weighted against documented behavior or restrictions; consumer should re-run without `--no-doc-discovery` if doc-alignment matters."
- "Wave 1.5 documentation discovery ran but found no relevant docs for the affected surface — `consistency_with_docs` set to `no_docs_found` across all hypothesis cards; downstream weighting fell back to correctness/risk/test-coverage alone."

If there are no gaps, write "None."

## Next Steps

Pick the line(s) that apply:

- Hard-stop (`diagnosability_hard_stop=true`), one line per unexecuted `## Discriminator rows` row of `diagnosability-tasklist.md`: "The report stays `partial` until `<row>=<value-if-true>` (then `<claim>` holds) or `<row>=<value-if-false>` (then it is refuted)." — Wave 5 renders every unexecuted row here; validator A2 checks the line is present.
- Whenever a tasklist was emitted, including a hard-stop (`diagnosability_hard_stop=true`), later sufficient verdict, or Wave 3 creation after audit bypass, render one line per unexecuted `## Discriminator rows` row of `diagnosability-tasklist.md`, using the Core/Optional forms in Falsifiers above with the pending reason and unchanged outcome semantics. Include linked enabling-task operational actions. A2 checks row linkage/publication, not a claim that every pending row gates status. Optional budget-exhausted cells remain informational and cannot force partial or prove a cause. If no tasklist exists, explain missing discriminator evidence rather than invent rows. Blocked/failed reports retain all pending rows and the external action needed, but suppress inapplicable rerun/fix/bypass advice.
- Apply the following advice only when the final status, established diagnosis, round cap, transport and authorization permit it; an audit bypass or counter reset never grants execution authorization. Inconclusive reports recommend evidence gathering, not causal remediation. Hard-stops use the conditional advice in the variant below rather than ordinary tier remediation.

- Tier 1, high confidence: "Apply the fix manually, or re-run with `/sc:troubleshoot --fix <args>` to generate an MDTM task."
- Tier 1, low confidence (but `--no-escalate`): "Re-run without `--no-escalate` (or with `--depth deep`) to enable Tier 2 fan-out."
- Tier 2 without `--fix`: "Re-run with `--fix` added to your previous invocation to enter the remediation chain."
- Tier 2 with `--fix`, awaiting user accept: "Reply **yes** to proceed to the task-builder remediation chain, or apply the fix manually."
- Tier 3 chain completed (post-`/task`): "Run `/sc:reflect --type task --validate <task-file>` before committing."

## TFEP Consumer

Emitted ONLY when `caller=task-unified`. This block is the report-rendered echo of the `return-contract.yaml` adapter fields the task-protocol TFEP consumer reads (see `sc:troubleshoot-protocol` Wave 5 step 4.5 and the Output Contract adapter rows). Omit this section entirely for non-TFEP callers.

```yaml
status: <success|partial|blocked|failed>
test_is_wrong: <bool>
recommended_escalation: <none|retry|escalate_depth|halt>
tasklist_insertion_path: <abs-path|null>
remediation_target: <test|code|docs|none>
root_cause_summary: <text>
solution_summary: <text>
```

### Hard-stop variant (when `diagnosability_hard_stop=true`)

When Wave 1.6 hard-stops, render the following halt explanation in Diagnosability Context. Retain the UNDETERMINED Diagnosis (empty root_cause_summary), evidence actually available, and all pending Next Steps rows. Proposed Fix states no causal fix established; omit inapplicable alternatives and fix-specific risk prose, not the evidence/blocking reasons. No exclusive replacement of Diagnosis or Next Steps occurs.

```text
Wave 1.6 Diagnosability Audit — HALT

The reported symptom looks non-trivial (signals: <list>), and the existing instrumentation around
<failing_component> is insufficient to triangulate it: <1-line specific gap, e.g. "no thread-correlation
fields in any log call within the suspect function; intermittent symptom requires when/why traceability">.

Hypothesizing harder against blind code at this point produces low-confidence answers. The protocol will
halt the deep-debugging pipeline and emit an instrumentation tasklist instead. No hypothesis work happens
in the same turn as the instrumentation patch — once you've implemented the tasklist and re-run, the
re-entry starts fresh with new evidence.

  Diagnosability Context Card:  <abs path>
  Instrumentation Tasklist:     <abs path>
  Diagnostic REPORT.md:         <abs path>
  Round:                        <N> of 3

```

Next Steps always preserves the pending measurement/enabling rows first. When final status is neither blocked nor failed, the round cap has not fired, and the relevant authorization/transport permits the action, recommend reviewing/applying the invocation-site tasklist (NOT production-source instrumentation) and rerunning with fresh captured evidence. Task packaging via `--diagnosability-handoff` remains opt-in. Audit bypass via `--no-diagnosability-audit` may be described only as bypassing audit, never as lifting capability, counter or execution-authorization blocks; log any bypass. Otherwise describe the external prerequisite to resolve the block/failure, without an automatic rerun, fix or bypass recommendation.

When the 3-round cap is reached for a counter key (`<branch>:<repro-venue-id>`, authoritative `<repo-root>/.dev/troubleshoot/diagnosability-rounds.json`; `<output-dir>/diagnosability-rounds.json` is a per-run snapshot), append a cap-specific paragraph: "Wave 1.6 has reached the 3-round diagnosability cap for this venue; the tasklist is still written and the cap contributes blocked to the final status (failed remains failed). Further instrumentation iteration is unlikely to yield new evidence — escalate to structural change (a different repro harness, a different test scope, or a redesign of the failing component's observability). Automatic reruns and their recommendation are suppressed until `--reset-diagnosability-rounds` is set for the current branch/venue key." The reset preserves other keys and does not grant execution authorization. Retain `failed` if the run also errored; the cap's blocked contribution cannot lower a higher-precedence status.

## Audit

- **Hypothesis cards**: <list of paths>
- **Adversarial artifacts** (Tier 2 only): <path to artifacts dir, or "Not invoked — single proposal" / "Not invoked — consensus">
- **Self-review** (Tier 2 only): <result>
- **Task file** (Tier 3 only): <path>
- **Audit log**: <path>

## Pipeline Hardening Closure

First check for `pipeline_hardening_verdict=blocked-on-authorization`: render that verdict, the tasklist/refusal evidence and `Authorization blocker — diagnostic rerun refused`, regardless of applicability. If HC0 did not run, render `HC0 not run — applicability unassessed`; do not label default false a justified skip or invent HC cards/statuses. Otherwise render the full closure below when applicable=true; only an actual HC0 false decision with reason and boundary scan collapses to `Pipeline hardening not applicable: <reason>`.

**Applicable**: <true|false>
**Closure verdict**: <pass|blocked|advisory|not_applicable|blocked-on-authorization>
**Waiver status**: <none|latched>
**Backtest status**: <not_run|partial|complete>
**Off-path review**: <required|performed|waived_with_rationale|not_required>

**Wave statuses**:

- **HC0 Applicability + Boundary Scan**: <PASS|FAIL|N/A> — <one-line>
- **HC1 Runtime-Entrypoint Verification**: <PASS|FAIL|N/A> — <one-line>
- **HC2 Contract Enumeration**: <PASS|FAIL|N/A> — <one-line>
- **HC3 Unmask + Sweep**: <PASS|FAIL|N/A> — <one-line>
- **HC4 Effective-Input Proof**: <PASS|FAIL|N/A> — <one-line>
- **HC5 Off-Path Reviewer + Waiver**: <PASS|FAIL|N/A> — <one-line>

**Evidence cards** (render the path when the wave ran, otherwise `—`):

- Runtime-entrypoint card: <runtime_entrypoint_card_path>
- Contract ledger: <contract_ledger_path>
- Unmask/sweep card: <unmask_sweep_path>
- Effective-input card: <effective_input_card_path>

**Known escapes caught**: <list of {escape_id, wave, card_path, status}, or "None claimed">

**Closure blockers** (omit when `Closure verdict` is `pass`; render only the line(s) that apply, verbatim):

- NOT PROVEN — failed hardening wave: <wave>
- NOT PROVEN — mandatory runtime proof waived or absent
- NOT PROVEN — unrationalized N/A: <wave>
- ADVISORY — closure relies on waived/substituted proof
- ADVISORY — scoped closure with rationalized N/A
````

## Rendering rules

- **No trailing emoji or decorative headers.** The report is a working document, not a marketing brief.
- **Cite or drop.** Every `file:line` in the report must survive the Wave 5 validation pass.
- **No reuse of the original error message in the Summary.** Summarise it in the user's own framing if possible — a verbatim stack trace at the top adds noise without information.
- **Status `partial` is honest.** Marking `partial` with a clear "Grounding Gaps" section is far better than marking `success` and being wrong.
- **Timestamps come from command output only.** Every timestamp written into the report or any artifact is copied from a `date -u +%Y-%m-%dT%H:%M:%SZ` Bash result in the same turn or from `git log --format=%cI`; no other source. Any `Timestamp`/`Date`/`pushed_at` later than the artifact's mtime + 5 min, or equal to `T00:00:00Z`, is dropped by the validator (A3) / calibrator (C5) with reason `timestamp_invalid`.

## Test-is-wrong rule

Set the `Test is wrong` header field to `true` when **all** of these apply:

1. The chosen diagnosis names a test file (not production code) as the file requiring change.
2. One of:
   - The test asserts an invariant that the cited spec / requirements doc explicitly contradicts (e.g., test claims policy rejects X but the policy doc allows X)
   - The test was authored before a feature change that legitimately altered the asserted behavior, and was not updated alongside the feature
   - The test mis-models the requirement (typo'd assertion, wrong fixture, wrong expected value)

When `test_is_wrong=true`:

- The **Summary** section MUST open with a single sentence naming the test as the bug (e.g., "The test is the bug, not the code"). No hedging.
- The **Proposed Fix** section's `Files to change` list MUST contain ONLY the test file — not the production code. If the diagnosis also recommends a hardening change to production code, that goes under the `## Follow-up tasks` section (template provides it; treat as a separate ticket), not the primary fix.
- An explicit **`## Files that MUST NOT change`** subsection MUST appear under Proposed Fix, listing every production-code file a careless remediation might touch. (The same subsection is also required when `behavior_is_documented=true` — see the Behavior-is-documented rule below. trigger union: `test_is_wrong=true OR behavior_is_documented=true`.)
- The **Alternative Fixes Considered** section MUST include "fix the code to make the test pass" with the rejection reason "**This is the DANGEROUS wrong answer** — would regress documented behavior. See evidence."

The asymmetric cost of this flag is the entire reason it exists: a downstream automation chain that "fixes" the code to satisfy a wrong test will silently break documented behavior. The rendering rules above are the human-readable side of that safety net; the `test_is_wrong` flag in the output contract is the machine-readable side.

If the test is wrong AND the code is also missing a defensive guard, keep `test_is_wrong=false` and surface both in `Files to change` — the production-code fix is the load-bearing change and the test update is incidental.

## Behavior-is-documented rule

Set `Behavior is documented: true` (and `behavior_is_documented=true` in the output contract) when ALL three conditions hold:

1. Wave 1.5 produced a Documentation Context Card with a populated `Documented behavior` entry that matches the observed symptom (not the user's expected behavior).
2. The chosen hypothesis card's `consistency_with_docs` field is `aligned` (the bug IS the documented behavior).
3. The fix would require a change to either the documented behavior (spec/docs update) or a stakeholder-level discussion about whether the doc should change.

Mutually exclusive with `Test is wrong: true` **by construction, not by tiebreaker**. The 3-case decomposition (see SKILL.md `behavior_is_documented` derivation rule): Case A (user expectation diverges) → `behavior_is_documented=true`; Case B (test contradicts docs+code consensus) → `test_is_wrong=true`; Case C (code violates docs) → both false. Only one can be true.

### Rendering rules when `Behavior is documented: true`

- The Summary section MUST open with "The reported issue is the documented behavior — a code change would regress the documented contract."
- The Proposed Fix section's `Files to change` list MUST contain ONLY the doc/spec file(s) — not code.
- A `## Files that MUST NOT change` subsection MUST appear listing every code file a careless remediation might touch. (Same subsection required when `test_is_wrong=true`; trigger union: `test_is_wrong=true OR behavior_is_documented=true`.)
- Alternative Fixes Considered MUST include "modify the code to change the documented behavior" with rejection reason "**This is the DANGEROUS wrong answer** — would silently break the documented contract for downstream consumers."

### Rendering rules when `Behavior is documented: false` (docs side with the user)

- Proceed with normal code remediation; the Documentation Context section still surfaces the relevant docs as evidence supporting the fix.
- If Wave 1.5's Branch C surfaced semantic restrictions the proposed code fix would violate, surface those restrictions in the `Risk + Rollback` section.

### Rendering rules when `Behavior is documented: n/a` (--no-doc-discovery)

- Omit the Documentation Context section entirely.
- Surface "Documentation grounding skipped by `--no-doc-discovery` — diagnosis is not weighted against documented behavior or restrictions" in Grounding Gaps.

## Pipeline Hardening Closure rule

The **Pipeline Hardening Closure** section (inside the template block) renders the Pipeline Hardening Closure mode's verdict and evidence. It is governed by `refs/hardening-output-contract.md` (the §5.4 verdict-aggregation truth table and §5.5 field schema). Rendering rules:

- **Authorization precedes applicability rendering.** Always render `blocked-on-authorization` and its tasklist/refusal evidence with `Authorization blocker — diagnostic rerun refused`, even before HC0. In that case state `HC0 not run — applicability unassessed`, not a fabricated boundary scan or HC status. Otherwise collapse to `Pipeline hardening not applicable: <reason>` only for an actual HC0 false decision with its boundary scan (truth-table row 1); never infer closure from the default false.
- **Closure verdict is the five-token enum** `pass | blocked | advisory | not_applicable | blocked-on-authorization` (the fifth value is set by the Wave 1.6 S1.6.4 precedence rule, never by §5.4 aggregation). `advisory` is a first-class outcome and MUST appear in the enum — a three-token Closure verdict is a defect.
- **Emit `NOT PROVEN` blockers for absent required proof.** When the verdict is `blocked` (any HC1–HC5 `FAIL`, a latched waiver with a mandatory probe absent/waived without an accepted substitute, or an unrationalized `N/A`), render the matching `NOT PROVEN — …` line from the §5.4 truth table verbatim. `NOT PROVEN` is stronger than ordinary confidence language and is reserved for absent/failed required proof (FR-13 AC3).
- **`advisory` differs from `blocked`.** `advisory` (truth-table rows 5 and 6) means closure relies on waived/substituted proof or a rationalized `N/A` with no hard failure — render the matching `ADVISORY — …` line, NOT a `NOT PROVEN` blocker. `blocked` is a hard failure; `advisory` is a rationalized or accepted-substitute closure. Neither may be rendered as a plain `success`.
- **Downstream may not re-green.** A `blocked`/`advisory` closure verdict is rendered as `success_with_hardening_blocker` / `success_with_hardening_advisory` by any downstream stage that has its own success enum; downstream `task-builder` / `sc:reflect` / `sc:adversarial` / report-rendering stages may append findings but may NOT convert `blocked`/`advisory` into `pass`/`success` (§5.4 downstream no-override rule). Independently of aggregation/applicability, downstream consumers must also preserve `blocked-on-authorization` and its authorization blocker; if they render a separate success enum, use `success_with_hardening_blocker` with the original fifth verdict/refusal reason, never plain pass/success. Diagnostic status retains blocked or higher-precedence failed.
- **Backtest status is separate from the verdict.** `not_run`/`partial` keep the production-facing pipeline-health signoff `advisory` even when the run-level `Closure verdict` is `pass`; only `complete` may mirror the verdict.
