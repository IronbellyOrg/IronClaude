# Evidence validation (Wave 5 final gate)

Validator: evidence-validator agent (read-only; it has no Write tool, so the orchestrator persisted its returned result verbatim below).
Policy: sampled. Sample = every file:line citation of D-01..D-05 (the P1 findings), every Inferred-requirements row, and every third citation of D-06..D-31 in document order.

## Counts

- citations_total: 184 (154 deviation evidence entries + 30 INF rows)
- citations_revalidated: 108 (39 from D-01..D-05, 30 INF rows, 39 from the every-third sample of D-06..D-31)
- citations_dropped: 3
- citations_dropped_extrapolated: 5 (round(3 x 184 / 108))
- dropped INF rows: none

## Dropped

| # | Deviation/row | Citation | Verdict | Note |
|---|---|---|---|---|
| 1 | D-03 | `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:137-139` | DROPPED | Cited for "carry no 'safety' label"; line 138 reads "the safety flags from the digest (`--no-pty`, `--no-mcp`, `--json`, `--junit`, `--timeout-mult`, `--keep-home`, `--max-disk-mb`, `--output-dir`)", which contradicts the claim. |
| 2 | D-04 | `src/superclaude/commands/troubleshoot.md:148` | DROPPED | Line 148 is a closing code fence; `diagnosability-handoff` does not appear in commands/troubleshoot.md. The flag is at `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:148` and `:645`, and the packaging at `refs/diagnosability-audit.md:245,247` (claim true, file wrong). |
| 3 | D-20 | `plan:46` | DROPPED | plan:46 is D-P2-1 (brainstorm research); the cleanup Safety Threshold clause is at plan:53 and plan:97. |

## Kept with notes

| # | Deviation/row | Citation | Verdict | Note |
|---|---|---|---|---|
| 1 | D-01 | `sc-task-protocol/SKILL.md:61` | KEPT | Only the EXEMPT keyword list; the committed-report claim is supported by :266. |
| 2 | D-01 | `sc-task-protocol/SKILL.md:94` | KEPT | The impact call is on :94; the `.dev/impact/task-<slug>` path is on :95. |
| 3 | D-02 | `sc-cli-eval-protocol/SKILL.md:30-33` | KEPT | Weak support (core objective only); the substance is at :128-153. |
| 4 | D-03 | `adversarial/diff-analysis.md:64` | KEPT | The A-001 row asserts no option is labelled a safety flag; that upstream assertion is contradicted by SKILL.md:138. |
| 5 | D-03 | `adversarial/rounds/round2-advocate-3.md:46,56` | KEPT | :46 is the C-001 position, :56 the A-001 "qualify"; neither contains the words "owner decision". |
| 6 | D-12 | `refs/diagnosability-audit.md:245,250,252` | KEPT | :252 is blank; the step that reads `return-contract.yaml` is at :251. |
| 7 | D-14 | `adversarial/variant-3-original.md:25-26` | KEPT | Supports the nested `--report-dir`; `--compliance strict` is on :11. |

All 30 INF rows matched source.md verbatim at the cited lines; the other sampled citations were kept with no issue.

Out-of-sample observation (no verdict): D-06 says the plan keeps the clause "(plan:306)"; that text is at plan:303, and plan:306 is the cmp acceptance criterion.

## Self-audit (validator)

All three drops come from reading the cited lines, not from upstream claims. A line within about 3 lines of the true content counts as moved and is kept with a note; anything further off or contradicted is dropped. No command was re-executed. The ~90 clean KEPT rows are tallied, not itemised.
