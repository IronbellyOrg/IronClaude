<!-- Provenance: produced by /sc:adversarial, merge-executor log -->

# Merge Log: OAG2

## Metadata

- Base: Variant 1 (OURS), /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG2/adversarial/adversarial/variant-1-original.md
- Other variant: Variant 2 (CLAY), /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG2/adversarial/adversarial/variant-2-original.md
- Refactoring plan: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG2/adversarial/adversarial/refactor-plan.md
- Merged artifact: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG2/adversarial/merged-oag2-sweep-observer-recommendation.md
- Executor: merge-executor
- Changes applied: 7 of 7 planned (1, 2, 3, 4, 5, 6, 7); 4 rejected changes (C-001, C-006, C-009, C-005 with X-001) not applied
- Status: COMPLETE, all validation checks passed
- Timestamp: 2026-11-20

## Changes Applied

All changes were applied in the order the plan states. The base was restructured into a recommendation document with seven H2 sections, as the plan Overview requires, so "before" below means the base text and "after" means the matching text in the merged artifact.

### Change 1: Reader selection rule, window shown on screen

- Status: applied
- Before: the Mechanism said the observer and the work report read the same file; the "window problem" risk bullet ended "The spec must say who passes which `--window`".
- After: OA-9 rules 4, 5 and 6 state the rule. The observer reads the newest `*-sweep.json` whose `scope.root` equals its own root and shows `window`, `observed_at` and the age. The work report does not read a file whose `window` is shorter than the time since its previous report; it runs `superclaude sweep run --window <that time>` itself, which also saves a file. The coordinator keeps WC-16. OA-9 Evidence 6 and 8 carry the window and root reasons.
- Provenance tag: `Variant 2, Section Cited facts 1 and Variant 2 advocate "newest file may be the report's" point - merged per Change #1`
- Validation: the base sentence "The spec must say who passes which `--window`" appears only inside the provenance comment that names it as replaced; the `classify.py:303-324` and `:922` citations survive in Evidence 6; no contradiction with WC-16.

### Change 2: Correct the premise that the file must record its window and root

- Status: applied
- Before: not in either paper (both advocates treated the fields as a gap).
- After: one sentence in the OA-9 Decision and rule 3: JSON v1 already holds `observed_at`, `scope.root` and `window`; no new field is needed; the missing part is the selection rule; the D11 fields `session_id` and `worktree_path` are a separate item. Citations `report.py:621-631` and `report.py:95-101` are included.
- Provenance tag: `Orchestrator verification after Round 1 - Change #2`
- Validation: the citations are the ones the plan gives; no rule asks for a new field.

### Change 3: Pair rule for the file and its Markdown

- Status: applied
- Before: "publish a second file with the same stem from the same `to_json` call".
- After: OA-9 rule 2: same stem and same suffix (`<UTC>-sweep.json` with `<UTC>-sweep.md`, `<UTC>-sweep-2.json` with `<UTC>-sweep-2.md`); the `.md` link stays the commit point; the contract note decides what happens when the JSON cannot be written; a test pins that a pair shares its suffix; `MAX_SUFFIX = 99` at `commands.py:182` is cited.
- Provenance tag: `Orchestrator verification after Round 1 - Change #3`. Note: the plan names the Variant 1 advocate's Round 1 concession as the source and its Overview groups this change with the Variant 2 items; the tag follows the merge brief, which treats changes 2 and 3 as orchestrator-origin.
- Validation: "the same stem" alone no longer appears in the Decision or rules; the Decision says the second file comes from the same `to_json` call and rule 2 sets the pairing.

### Change 4: Entry text allowlist, cap and fallback

- Status: applied
- Before: claim 2 "the observer shows entry text from the living report, always through `observe/sanitize.py`"; the entry-fields risk bullet said the spec must list which fields the observer shows.
- After: OA-17a Decision and rules 1 to 7: a named allowlist; `recommend` and `suggested` never shown; `how` held back until the owner reviews it (UNVERIFIED); every shown field is `rich.Text` built from data after `sanitize()`; a length cap on block fields; titles and links only while `superclaude orchestrator report-entry` is absent; three states kept distinct. The three tests (fixture with `recommend` and `suggested`, 5,000-character field, bracket markup) are in rules 2, 4 and 5. Evidence 3 to 5 carry `render.py:158-160,325` and `render.py:85`.
- Provenance tag: `Variant 2, Section Claim 2 and Cited facts 3, 4 and 5 - merged per Change #4`
- Validation: the full allowlist contents and the cap value are left as open items, as the plan does not decide them.

### Change 5: Label and follow-up for the questions exception

- Status: applied
- Before: claim 3 "labelled as an honest exception to 'one data source'"; cost line "A one-line label".
- After: OA-17b Decision and rules 2 to 4: the label reads "questions read from Orca directly; a question already handled can appear as open" (`questions.py:9-12`); the qualified sentence "one source for session facts (the sweep); the questions panel is the one exception"; a tracked follow-up for one shared question id (which also ends the two question channels of D11), with the owner named by the owner, not a precondition of release.
- Provenance tag: `Variant 2, Section Claim 3 and Cited facts 7 and 8 - merged per Change #5`
- Validation: the unqualified "one data source" survives only inside quotes that report what D11 said; the owner of the follow-up is left to the owner.

### Change 6: Qualify the 90 s argument

- Status: applied
- Before: "A sweep per observer cycle cannot fit its own budget".
- After: OA-9 Evidence 2: "is not guaranteed to fit"; `Budget(total_s=90.0)` is a cap, not a measured time; the case rests on cost and on WC-16, not on the 90 second figure. `probes.py:130` and `collector.py:28-29` are kept.
- Provenance tag: `Base (original, modified) - "cannot fit" replaced by "is not guaranteed to fit" per Change #6`
- Validation: "cannot fit" appears in the merged artifact only inside the provenance comment that names the replaced wording.

### Change 7: Gate on the entry writer and record the open claim about Clay's views

- Status: applied
- Before: the base Claim did not mention the entry writer or Clay's views.
- After: the OA-17a Decision says OA-17a text on screen is conditional on the entry writer landing; Evidence 7 cites the technical reference lines 805 and 820 as given in the debate; the Recommendation paragraph, the adoption table and "Open items and UNVERIFIED" state that Clay's own views on OA-9 and OA-17 are not on record (UNVERIFIED) and that the alternative was argued from TOPICS.md and the merged work.
- Provenance tag: `Variant 2, Section Cited facts 4 and 5, and the debate shared assumption A-001 - merged per Change #7`
- Validation: the claim is marked UNVERIFIED wherever it appears.

### Rejected changes (not applied, as the plan requires)

| Diff point | Where it shows in the merged artifact |
|---|---|
| C-001 (no sweep file) | Listed under "What stays from OURS" as not adopted, with the reason |
| C-006 (titles and links only for good) | Same; titles and links survive only as the fallback of Change 4 |
| C-009 (end the questions exception before release) | Same; the follow-up of Change 5 is not a precondition |
| C-005 and X-001 (second file breaches read-only) | Same; the Will Not line governs the skill session (`SKILL.md:61-62`) |

### Small elaborations to flag (not new facts, not decisions)

- OA-9 rule 1 adds a test line "a second run in the same second does not overwrite the first"; it restates the base's "never overwrite" as a test.
- OA-9 rule 7 and "Open items and UNVERIFIED" item 4 name "what age counts as old" as not set. The base said "a missing or old file is its own state" without a threshold.
- OA-17a Evidence 6 restates the debate outcome for shared assumption A-004 (low risk with a person reader; an allowlist and cap cost little).
- Open item 2 (multi-repo rule) cites `commands.py:99` and D07 from Variant 2 fact 2, because the debate records the root rule as open (diff point C-004) and the plan does not decide it.

## Post-Merge Validation

### Structural

- Result: pass.
- One H1 (line 6), then seven H2 sections in the required order: Recommendation in one paragraph; OA-9 where the sweep JSON lives; OA-17a what the observer may show; OA-17b the questions panel; What is adopted from CLAY; What stays from OURS; Open items and UNVERIFIED. The three argument sections each hold H3 sections Decision, What the spec must say and Evidence in that order. No heading level is skipped.
- 24 `<!-- Source: ... -->` tags cover every section and significant block; the document header comment has the provenance line, base, incorporated sources and the merge date 2026-11-20.

### References

- Total internal references: 22 (20 "rule N" references and 2 quoted heading references).
- Resolved: 22. Broken: 0.
- Each "rule N" reference was checked against the numbered list of the section it names (OA-9 rules 2, 4, 5, 7 and 8; OA-17a rules 1, 3, 5, 6 and 7; OA-17b rules 2, 3 and 4). Both quoted heading references point to the existing H2 "Open items and UNVERIFIED".
- Carried citations: every file:line of the base that survives the plan is present (checked by search): `commands.py:278`, `commands.py:153-193`, `probes.py:130`, `collector.py:28-29`, `WORKER-CONTRACT.md:287-289`, `adapter.py:29`, `SKILL.md:61`, `sanitize.py:1-7`, `common.py:139-141`, `adapter.py:32`, `adapter.py:111`, `adapter.py:34-50`, `observe/commands.py:67,70`, `report.py:613-640`, `classify.py:303-324` and `:922`, `docs/designs/observe-sweep-contract.md` and the D11 verdict file. Plan-added citations are also present: `report.py:621-631`, `report.py:95-101`, `commands.py:182`, `render.py:158-160,325`, `render.py:85`, `questions.py:9-12`.
- The citations were not reopened against the source tree (the hard rules make this run read-only and limited to the inputs); a pass-2 evaluator spot-checked 21 of them earlier and found none wrong.

### Contradictions

- Result: none found.
- Against the base: WC-16, the stateless read-only sweep, the "recommend nothing" rule and the sanitizer use are kept; each base sentence that the plan replaces (the "same stem" line, "who passes which `--window`", "always through sanitize.py", the one-line label, "cannot fit") no longer appears in its old form (the old wording remains only as quoted text inside provenance comments).
- Against the plan: all seven changes are present with the plan's wording; none of the four rejected changes is applied; the allowlist contents, the multi-repo rule, the cap value and the owner of the questions follow-up are left open, as the plan leaves them.
- Style checks: zero em dashes or en dashes, zero `{{PLACEHOLDER` strings, zero leftover build markers, only ASCII characters. First use of each id (OA-9, OA-17, WC-16, JSON v1, D11, issue 409, PR 684, PR 681, D07, S5, R4) carries a short explanation.

## Summary

- Planned: 7
- Applied: 7
- Failed: 0
- Skipped: 0
- Rejected by the plan and not applied: 4
- Escalations to the orchestrator: none. One note for the orchestrator: the plan lists change 3's source as the Variant 1 advocate's concession while its Overview counts it among the Variant 2 changes; the merged artifact tags it as orchestrator-origin per the merge brief.
