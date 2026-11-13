# Merged Findings Verdict — reflect Tier-2 shadow run 14

Panel: 3 reviewer cards (analyzer/sonnet 0.63, qa/haiku 0.69, refactorer/opus 0.59; cluster_agreement 1.0, 13/13 calibrated).
Merge: sc-adversarial Mode A, depth=standard. Base: Card 1 (analyzer/sonnet, combined 0.83).
Convergence: 0.96 (8/9 diff points at threshold 0.80; D3 category resolved by rule with dissent recorded).
Result: 10 merged findings (MF-1..MF-10) from 13 originals; provenance per finding. All MINOR, none blocking.

**Evidence-validator flag (applies to every finding below):** per adopted assumption A-003 (REJECT — no card re-verified any cited line) and probe IP-2, ALL citations are unverified pending the downstream evidence-validator gate. This merge adjudicated the cards' claims, not the repository.

**Provenance key:** C1 = reviewer-1 card, C2 = reviewer-2 card, C3 = reviewer-3 card.

---

## MF-1 | Task-2 AC3 escape hatch — unpassable-check | MINOR | blocking: no | conf 0.80 | L3

Task 2 AC3 accepts the check if "any failure is shown in ./artifacts/t2-checks.log and is not attributable to `design.md`". That judgment call means the AC cannot fail mechanically against spec AC6 as written ("The related tests pass"). The recorded run was green (1167 passed, rc=0), so the weakness is latent.
Provenance: carrier C1-F1 (quoted plan:46 + spec:62); corroborated C2-F3 (green-run detail); C3-F3's AC3 half dropped as mis-bundled (advocate-3 conceded Round 2). Wording guard per A-002: "cannot fail mechanically as written", not "cannot ever fail".

## MF-2 | design.md:65 conditional codegraph_impact — contradiction (+ deviation tag: Drift, unamended plan) | MINOR | blocking: no | conf 0.80 | L2

Shipped design.md line 65 adds "`codegraph_impact` only if it was not already run for the same symbol in Plan or Design" to Validate. Spec 3.2 item 4 and the tasklist require "callers and impact" unconditionally, so the shipped text is narrower than the plan, and the plan was never amended to allow the refinement.
Provenance: carrier C3-F1 (quoted spec:31 + design.md:65, plus tasklist:28); C1-F4 folded in (author raised .65 to .70 and accepted .80 in Round 2; its "not a plan defect" advisory framing superseded). Execution deviation, tagged Drift per A-004.

## MF-3 | No before-state baseline for archived package — unpassable-check | MINOR | blocking: no | conf 0.70 | L2

Task 2 AC1 depends on `git diff src/superclaude/commands/design.md` showing no edit inside Usage, Unattended mode or Boundaries. The archived done/ package has no before-state baseline, so the check cannot be re-run or mechanically verified from the review vantage.
Provenance: carrier C1-F2 (quoted plan:44 + spec:7); C3-F3's AC1 half folded in as corroboration. Category set to unpassable-check by the panel's tightened A-005 rule (`other` only where no category fits); recorded dissent: advocates 1 and 2 held this is advisory-vantage, not a plan defect, while advocate 3 held the missing baseline is itself a plan defect. Severity MINOR unanimous.

## MF-4 | Spec item 7 unchecked by any AC — other (acceptance-coverage gap) | MINOR | blocking: no | conf 0.70 | L3

Task 1 ACs check only the readiness check, fresh-only rule, fallback and tool map. Nothing mechanically checks the Grounding line, the SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off rule, or the leads/empty-not-absence rules (spec items 5-7), so those requirements are unchecked — narrowed per Round 2 from "could be dropped" to "unchecked requirements" (not proof of omission).
Provenance: carrier C2-F4. Cross-linked to MF-5 (same spec item 7, plan-side cause vs shipped-side result) and to MF-6/MF-8 (overlapping unchecked-requirement surface). No confidence inflation from convergence (same requirement, no model-independent corroboration; probe IP-3 recorded).

## MF-5 | Shipped absence of SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off — missing-requirement (+ deviation class: Drift) | MINOR | blocking: no | conf 0.70 | L3

Task 1 and spec item 7 require the section to state that SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off yields graph:disabled. The shipped design.md has no mention of that variable; the token `graph:disabled` is still listed, so the mapping's enabling condition is unstated.
Provenance: carrier C3-F2 (quoted plan:28-32 + spec:34; design.md:57 bare ref). Cross-linked to MF-4 (cause) and MF-10 (same shipped fallback collection; per probe IP-6, MF-10's drop-guard does not alter this finding's framing). Carries a deviation class per A-004.

## MF-6 | Spec item 5 "no re-check" tail omitted — missing-requirement | MINOR | blocking: no | conf 0.80 | L2

Spec 3.2 item 5 ends "Design is read-only against the index, so no re-check after writing the design document." Task 1 lists the other item-5 rules but omits this one, and the coverage matrix has no row for it.
Provenance: carrier C2-F1 (quoted spec:32). Uncontested by the other cards from Round 1 through Round 2; advocates 1 and 3 both called it the panel's cleanest coverage finding.

## MF-7 | Coverage matrix grounds INF-007 at Task-1 AC lines — other (traceability defect) | MINOR | blocking: no | conf 0.65 | L3

The matrix grounds INF-007 (Tool Coordination names the tools as reflect.md does) at tasklist:31-33, which are Task 1 acceptance criteria, but that work is Task 2 (line 41). No AC mechanically checks that the bullet names the tools; Task 2 AC1 only checks that the section "refers to" the rules.
Provenance: carrier C2-F2. Advocate-1's Round-1 critique (bookkeeping slip, not a requirement gap) was narrowed in Round 2 to: traceability defect stands; the defensible criticism is only that "refers to" does not explicitly check tool naming.

## MF-8 | Spec 3.2-6 degraded-list conditional unverified + Grounding placement unspecified — missing-requirement | MINOR | blocking: no | conf 0.65 | L3

Spec 3.2 item 6 makes the return-contract degraded list conditional on the field existing. The plan copies the condition but has no step to check it, and design.md silently chose "no new field" for the worker contract. The plan also omits where the Grounding line goes for --format code or diagram.
Provenance: carrier C1-F3 (quoted spec:33, plan:28, design.md:74); C3-F4a's "worker contract gets no new field" folded in. The Grounding-placement gap for --format code/diagram is covered by no other card.

## MF-9 | Task-2 AC4 attribution check inadequate — other | MINOR | blocking: no | conf 0.60 | L2

Task 2 AC4 checks via `git status --short` that design.md is the only source file modified by the plan. Spec risk 7 says other sessions edit the same checkout, so status alone is insufficient to attribute changes to this plan; no baseline or scoped diff is given. (Reworded in Round 2 from "cannot be attributed" — an inadequate check, not an impossible one.)
Provenance: carrier C1-F5 (quoted plan:47 + spec:66). Rests on spec risk 7 as a hypothetical, not an observed misattribution — hence the panel's floor confidence.

## MF-10 | Extra shipped fallback tokens — candidate Authorized expansion (validator drop-guard) | MINOR | blocking: no | conf 0.45 | L2

The shipped fallback paragraph defines extra tokens (graph:empty, graph:truncated, graph:unresolved) beyond Task 1's seven. Round 2 downgraded this from a Drift-tagged gap to a CANDIDATE authorized expansion: Task 1 says "add to the existing degraded list if one exists", which may authorize the additions, but the card never established the seven-token list was exhaustive.
Provenance: carrier C3-F4b. Drop-guard: the evidence validator should DROP this finding if the shipped degraded list already existed (making the expansion authorized); otherwise classify Authorized vs Necessary expansion — do not default to Drift. Cross-linked to MF-5 (same shipped fallback collection, probe IP-6).

---

## Card self-reports (preserved verbatim)

- C1: claude-gw-tier1b (analyzer persona, reviewer-1); brief named claude-sonnet-5-5
- C2: claude-gw-tier1b (Claude, per the runtime environment; the brief names claude-haiku-5-5)
- C3: claude-opus-5-5 (opus class), operating as reviewer-3 refactorer persona

Note: C1 and C2 report the same observed runtime model (claude-gw-tier1b), so their agreement on D1 is not model-independent corroboration; this informed the no-inflation rule for MF-4/MF-5 and is recorded here per probe IP-3.

## Merge summary

13 originals → 10 merged: 10 carriers/corroborations, 1 dropped duplicate (C3-F3 AC3 half), 3 half-folds (C3-F3 AC1 half, C3-F4a, C3-F4b). All MINOR, none blocking, overall verdict: plan passed with 10 latent check-design and coverage weaknesses, none observed to have caused a failure in the recorded green run.
