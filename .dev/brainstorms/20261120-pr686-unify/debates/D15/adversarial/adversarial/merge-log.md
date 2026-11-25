<!-- Provenance: merge-log.md for debate D15, written 2026-11-20 by merge-executor. Records execution of refactor-plan.md Changes #1 to #5 against the base variant-1-original.md. -->

# Merge log: D15 Clay strengths bundle

## Inputs and output

- Base: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/adversarial/adversarial/variant-1-original.md` (Variant 1, OURS)
- Other variant: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/adversarial/adversarial/variant-2-original.md` (Variant 2, CLAY)
- Plan: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/adversarial/adversarial/refactor-plan.md`
- Other sources read: base-selection.md, debate-transcript.md, diff-analysis.md, invariant-probe.md, rounds/round1-advocate-1-ours.md, rounds/round1-advocate-2-clay.md, rounds/round2-rebuttal-1-ours.md, rounds/round2-rebuttal-2-clay.md (all in the same folder as the base)
- Merged output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/adversarial/merged-d15-position.md`
- Plan risk: Low overall; Change #4 Medium. Approval: auto-approved (unattended), as stated in the plan.

## Per-change log

### Change #1: Build order (incorporate CLAY substrate)

- Status: APPLIED
- Plan risk: Low
- Source: `rounds/round2-rebuttal-2-clay.md` A3.1 (substrate: runner, `refuse`, JSON contract, state lock; merge path as one tested unit; other verbs separable). Merge-path member list from `rounds/round2-rebuttal-1-ours.md` A1 W1. The state-folder path map comes from INV-006 and the unnamed merge verb from INV-010 in `invariant-probe.md`, as the plan names INV-006 in Change #1.
- Target section in merged file: (c) Build order. Provenance tag in file: `<!-- Source: Variant 2, round2-rebuttal-2-clay.md A3.1 ... merged per Change #1 -->`
- Integration point: after (b), as the build home that the base's Mechanism paragraph ("rules and doc fixes first, then code Clay already built, then unbuilt verbs, then live tests") leaves open. The base chain is kept as Stage 0 and Stage 4; the Variant 2 substrate is inserted as Stage 1, the merge path as Stage 2, the separable verbs as Stage 3.
- Before: base had a one-sentence order with no unit definition. After: five stages with the substrate parts tabled and the merge-path members listed.
- Validation: every substrate part and merge-path member traced to a line in the two Round 2 files or the design lines they cite (D:140, D:318, D:613, D:767, D:1117, D:1141). The unproven items stay marked (60 minutes reviewer re-trigger UNVERIFIED). Nothing contributed that is not in the sources. One wording fix applied during the merge: the rename is tied to D08 action 8 and the other doc fixes are tied to the base's own chain, so the text does not claim a source it lacks.

### Change #2: Test plan (incorporate CLAY T1 to T13)

- Status: APPLIED
- Plan risk: Low
- Source: Variant 2 `variant-2-original.md` fact 3 and `rounds/round1-advocate-2-clay.md` Strengths 2 (T1 to T13, U register, K register); `rounds/round2-rebuttal-2-clay.md` A3.2 (setup step on rows that start a worker); `rounds/round2-rebuttal-1-ours.md` A1 W3 (six logic rewrites) and G-3, G-8, G-9; counts and the T12 rewrite from `invariant-probe.md` INV-009.
- Target section in merged file: (d) Test plan. Provenance tag in file: `<!-- Source: Variant 2 (CLAY) T1 to T13 ... merged per Change #2 ... -->`
- Integration point: after (c); the base paper had no test plan, so this is an addition, not a replacement.
- Before: base named the plan only as "adopt as skeleton, rewrite T1 to T3". After: row-by-row table, counts 13 T, 60 U, 28 K (101), six logic rewrites plus T12, nine setup-step rows, reasons-table pin rewrite.
- Deviation from the base: the base said "rewrite T1 to T3"; the Round 2 rebuttal replaced it with six named rows (T1, T3, T4, T8, T10, T11), which the merge follows. The base's "80 rows" figure is dropped for INV-009's 101.
- Validation: counts match INV-009 (13 + 60 + 28 = 101). Rows T2, T5, T6, T7 and T9 are described only as "rename plus setup step" because no source says what they test; this is stated in the table. One inference is marked as such in the file: the "no recorded merge go" reason has to enter the T13 pin. The setup-step count stays UNVERIFIED as CLAY states.

### Change #3: Gap decisions G-1 to G-9

- Status: APPLIED
- Plan risk: Low
- Source: `rounds/round2-rebuttal-1-ours.md` Task B and `rounds/round2-rebuttal-2-clay.md` Task B (one paragraph each per gap; both files read in full).
- Target section in merged file: (e) Decisions on gaps G-1 to G-9. Provenance tag in file: `<!-- Source: Variant 1 ... and Variant 2 ..., merged per Change #3 ... -->`
- Integration point: after the test plan. Open owner decisions from this change are collected in (h) as OD-1 (G-2), OD-2 (G-3), OD-3 (G-4), OD-5 and OD-6 (G-9), OD-7 (G-6), OD-8 (G-1), OD-9 (G-7); OD-4 comes from INV-013 and attaches to G-4.
- Where the two Round 2 files disagree, both positions are stated with the recommended default:
  - G-2: OURS dropped `plan_tier`; CLAY replaced it with `plan_depth`. Merged per the plan: plain `plan_depth` key (CLAY). The default value is not given by any source; the merge records "unset, behaves as `quick`" as a recommendation of the merge and says so in the file. Flagged for review: it is the only recommended default that has no source.
  - G-3: OURS chat go per round with a `handback_awaiting_go` step; CLAY approval re-application, or body left alone. Merged per the plan: the start gate decides, owner picks (a) or (b), default (a).
  - G-9 part 1: OURS report line only; CLAY entry lines plus the notice step. Merged per the plan: the notice step, cap key at default 0.
  - G-6 (outcome agreed, one reason differs): both reasons stated.
  - G-9 AU5: the seven-equals line at `tmux.py:9` is called a banner by OURS and a reStructuredText underline by CLAY; both labels stated.
- Not carried: OURS' "new chat go per hand-back round" (plan: rejected); `plan_tier` as a tier-to-depth table (plan: not kept); report-line-only audit escalation (plan: replaced). These are the plan's "Changes NOT Being Made" items 2, 3 and 4. Item 1 (adopt the Clay set "as built") is also not present.
- Validation: each gap paragraph has outcome, reason, change and owner decision status. Two statements were trimmed during the merge because they were not in the sources in that form (a remark about a fixture file in G-7, and "templates and skills contain none" in G-4, replaced by OURS' actual grep wording).

### Change #4: Invariant conditions

- Status: APPLIED, with one structural deviation (below)
- Plan risk: Medium (new requirements, no source rule)
- Source: `invariant-probe.md`, HIGH items INV-001 to INV-004 and MEDIUM items INV-005 to INV-014, INV-016, INV-017 (INV-009 is rated LOW in the probe and is carried because the dispatch brief names the range).
- Target section in merged file: (f) Mandatory conditions. Provenance tag in file: `<!-- Source: invariant-probe.md ... merged per Change #4 ... -->`
- Integration point: after the gap decisions. Condition IDs: C-INV-1 = INV-001, C-INV-2 = INV-002, C-INV-3 = INV-003, C-INV-4 = INV-004.
- Deviation from the plan: the plan text groups INV-001 and INV-002 under one condition C-INV-1 and gives INV-003 to C-INV-2 and INV-004 to C-INV-3 (three conditions). The dispatch brief for this merge asks for C-INV-1 to C-INV-4, one per HIGH item. The merge follows the brief. No content is lost: the plan's C-INV-1 wording ("a hand-back waiting step is excluded from the in-flight count or has an expiry, and something wakes the coordinator after a re-approval") is split across C-INV-1 and C-INV-2. Flag for the orchestrator: any other file that cites the plan's three-condition numbering must be mapped (plan C-INV-1 = C-INV-1 and C-INV-2 here; plan C-INV-2 = C-INV-3 here; plan C-INV-3 = C-INV-4 here).
- Marked as recommendations: yes. The file says these are the fault-finder's recommendations with no Clay or owner source, as the plan's risk note requires.
- Testable statements: each HIGH condition carries one, plus a second test for C-INV-1. The test wording is the merge's formulation of what the probe says is missing; the facts inside them (line numbers, defaults, ranges) are quoted from the probe. The expiry length for a waiting hand-back is not given by any source and is left as an owner question (OD-13).
- Validation: 12 table rows (INV-005 to INV-014, INV-016, INV-017) each carry a spec line, a check and a decision status. Where the probe offers two ways out (INV-003, INV-004, INV-011, INV-012, INV-013, INV-014) the file lists the ways and does not choose; the choice appears as an owner question or a spec decision.

### Change #5: Wording rule

- Status: APPLIED
- Plan risk: Low
- Source: Base (original) wording ("narrows, never closes", base "What it gets right" and Round 1 A-004 REJECT); `rounds/round1-advocate-2-clay.md` A-004 ACCEPT as a limit; D06 item 10 as cited in both; falsifiers from `invariant-probe.md` INV-015, INV-016, INV-018, INV-019.
- Target section in merged file: (g) Wording rule. Provenance tag in file: `<!-- Source: Base (original) ... with the falsifiers of INV-015, INV-016, INV-018, INV-019 ..., merged per Change #5 -->`
- Integration point: after the invariant conditions, because the C-INV-3 and INV-014 references in the INV-016 row need (f) to exist first.
- Added to the plan's four falsifier sets: three extra rows (`refuse(argv)`, `E-NO-GRANT`, hand-back loop) taken from the same sources (D:769, K22, U42; D06 INV-011; D04 INV-006; INV-017) so the rule covers every control the base lists. No new fact is introduced; each row cites its origin.
- Note on numbering: the INV-018 row quotes the probe's references to D05's own finding numbers (INV-034, INV-019, INV-003). These are D05's numbers, not this probe's. The file labels them "D05's own" to avoid a clash with this probe's INV-019 (the `plan_check` finding).
- Validation: INV-015, INV-018 and INV-019 are ADDRESSED in the probe (limits already stated); INV-016 is UNADDRESSED and its four falsifiers are listed in full. The spec-wide grep check is declared "not run here" because the spec does not exist yet.

### Sections required by the dispatch brief that are not numbered plan changes

| Section in merged file | Origin | Note |
|---|---|---|
| (a) Merged position in 8 lines | Summary of (b) to (i); each line traces to the sections below it | Exactly 8 numbered lines. |
| (b) Rules that stay OURS | Base (original) claim, "What it gets right" and per-element outcomes; both Round 2 files confirm (C-006, C-009, X-002) | Rule list only; the per-element Clay table is not written here, as instructed (VERDICT.md is its single authoring location). |
| (h) Open owner decisions | "Owner decision" lines of both Round 2 files plus open choices from the probe | 13 questions, one line per answer. OD-1 carries one recommended default that no source gives (see Change #3). |
| (i) Unresolved points and Unverified list | `debate-transcript.md`, `base-selection.md`, the "could not verify" lists of both Round 2 files, UNVERIFIED marks in the probe and Round 1 files | No invented items. |

## Post-merge validation

Checks run on `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/adversarial/merged-d15-position.md` after the last section was written.

### 1. Heading hierarchy

- One H1 (line 3). H2 sections in the required order: (a) line 11, (b) 24, (c) 46, (d) 81, (e) 125, (f) 149, (g) 189, (h) 207, (i) 270.
- H3 headings appear only inside (f) ("HIGH conditions", "MEDIUM items as spec lines") and (i) ("Unresolved points", "Unverified list"). No H4. No skipped levels.
- Result: PASS.

### 2. Internal references

- Owner questions OD-1 to OD-13: each is defined in (h) (lines 213 to 266) and every reference elsewhere points to one of them (OD-1 in (e) G-2; OD-2 in G-3; OD-3 and OD-4 in G-4; OD-5 and OD-6 in G-9; OD-7 in G-6; OD-8 in G-1; OD-9 in G-7; OD-10 and OD-11 in (b) and (f); OD-12 and OD-13 in (f)). No dangling OD reference. The count "13" in (a) line 8 matches.
- Conditions C-INV-1 to C-INV-4: each defined once in (f) and referenced from (a), (b), (c), (e), (g), (h), (i). No dangling reference.
- Section references "(c)", "(d)", "(e)", "(f)", "(g)", "(h)" inside the file all resolve to the headings above.
- Counts: 13 T, 60 U, 28 K, 101 total appear identically in (a), (d) and the INV-009 row of (f).
- PR numbers: PR 686 (Clay's branch that carries the coordinator code) and PR 690 (adds `--plan` and `--remaining` to `/sc:issue`) are explained at first use in the merged file (notation paragraph, line 9); PR 682 (Clay's merged deletion of the owner's issue pipeline) is explained at first use in (c) (line 52); PR 681 (Clay's merged design text) is explained at first use in (i) (line 296). No issue numbers appear in the file.
- Style: a search for em dashes and en dashes in both output files finds none.
- Result: PASS.

### 3. Contradiction rescan

| Check | Finding |
|---|---|
| (b) row 4 says the only standing grants are four entries; (f) INV-012 and OD-11 leave the fresh-install default open (empty or four) | Not a contradiction: (b) states the four-entry limit from D04 item 5 and flags the default as unsettled in its note column. Left as is. |
| (a) says six logic rewrites and "T12 is rewritten"; (d) says six plus T12 as a seventh | Consistent. |
| (e) G-3 says the plan rejects the chat go; (h) OD-2 offers only (a) and (b) | Consistent. |
| (e) G-9 channel: notice step with cap default 0; (f) INV-014 notes default 0 means no cap | Consistent: the cost is stated, the choice stays with the owner (OD-5). |
| (b) row 10 and (e) G-9 part 2 say the coordinator never tags or publishes; (h) OD-6 asks the owner to confirm | Consistent: default yes, confirmation requested. |
| (c) Stage 2 includes the post-merge close authority; (f) C-INV-4 and (h) OD-10 hold the choice | Consistent. |
| (g) wording rule against base text | The base says "narrows, never closes" in its Claim and "What it gets right"; no merged line claims a control closes a risk. |
| Plan "Changes NOT Being Made" | None of the four rejected items is adopted in the merged file: no "as built" base, no `plan_tier` tier table, no chat go per hand-back round, no report-line-only audit escalation as the outcome. |
| New contradictions introduced | None found. |

Result: PASS, with these items flagged for the orchestrator (not defects):
1. Condition numbering differs from the plan (Change #4 deviation).
2. OD-1 carries a recommended default (`quick`) that no source gives; it is labelled as the merge's tie-break recommendation in the file.
3. The four HIGH conditions are labelled as recommendations without a Clay or owner source, as the plan's risk note requires.
4. The test statements inside C-INV-1 to C-INV-4 are the merge's formulation of what the probe says is missing; they were not reviewed by an independent agent.

## Summary

- Plan changes applied: 5 of 5 (#1 build order, #2 test plan, #3 gap decisions, #4 invariant conditions, #5 wording rule). None skipped. One structural deviation (Change #4 condition numbering), documented above.
- Changes NOT made, as the plan requires: 4 of 4 absent from the merged file.
- Merged file: 9 sections (a) to (i), 1 H1, 9 H2, 4 H3; provenance comment on the file and on every section; the per-element Clay table is deliberately absent and referred to VERDICT.md.
- New content beyond the sources: none in facts. Recommendations marked as the merge's own: OD-1 tie-break default, test statements of C-INV-1 to C-INV-4, the T13 pin note for the new gate reason.
- Escalation to orchestrator: none required; items 1 to 4 above are for awareness.

