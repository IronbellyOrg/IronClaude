# Round 1: Variant 2 QA Position

## Position Summary

Variant 2 provides the strongest evidence that the tasklist cannot be executed correctly as written. Its three calibrated HIGH findings identify an owner-decision deadlock, a model-name check that rejects required type references, and a live-capture check that rejects commands its own Action requires (R2-G7, R2-G5 and R2-G3; variant-2-original.md:240-259). These are pre-execution plan defects, not claims of observed implementation failures.

I defend those three findings, not the original seven-HIGH total or the 0.96 self-confidence. The calibrated result is 3 HIGH, 5 MEDIUM, 2 LOW and confidence 0.85. Variant 1 contributes the better cross-folder test-traceability finding; Variant 3 contributes the better substantive owner-approval finding (diff-analysis.md:18-24,49,83-91).

Citation key: card and diff basenames refer to the files in this document's parent directory. `TL` means `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`; `DESIGN` means `docs/designs/orchestrator-mode.md`, both relative to the repository root. Findings are identified by their original card IDs. A position attributed to a variant below includes that card's attached calibration, which outranks its self-assessment (diff-analysis.md:12).

## Steelman

### Variant 1

Variant 1 has the broadest requirement-and-step audit: 76 rows, compared with Variant 2's 51 and Variant 3's 24. Its strength is separating a matrix's apparent match from the actual delivery item. For example, it maps FR-023 to items 12.1 to 12.3 rather than treating a design-edit match as delivered code (variant-1-original.md:36; diff-analysis.md:30-31,58).

Its R1-G3 is an independently valuable MEDIUM finding that my card missed. Item 14.11 searches only two locations even though the trace sends FR-023 and FR-024 into other test folders. Building those tests does not prevent the final reviewer from falsely reporting them missing (TL:2509; variant-1-original.md:306-309). Its R1-G5 also correctly recognises documented extra gates as an explanatory refinement rather than a defect (variant-1-original.md:314-317).

### Variant 3

Variant 3 best distinguishes design-fix work from delivery work. It correctly identifies item 2.16 as a report-only SPEC-fidelity lens, where Variant 1 calls it a design edit (variant-3-original.md:25; diff-analysis.md:66). This matters because neither a lens nor a design edit proves delivery.

Its R3-G4 identifies a separate approval defect: asking the owner to choose WC-16 versus WC-1 does not ask them to approve the revised rule text and cadence. The calibration sustains MEDIUM while noting that the merged-master precedent limits the substantive risk (variant-3-original.md:171-174). Its reuse analysis also prevents unnecessary extraction: the existing link and atomic-write precedents do not together provide the required publication behaviour (variant-3-original.md:191-194). That accurate confirmation belongs outside the defect count.

## Strengths Claimed

1. **Variant 2 checks whether correct work can pass the plan's checks.** R2-G5 has a direct counterexample: the required `ClassifiedRow.row: SessionRow` annotation adds a second line containing `SessionRow`, while Verification demands one grep match per model name. This does not depend on a dirty checkout or speculative implementation choice (TL:1431-1434; variant-2-original.md:248-251). Class declarations, not all references, are the appropriate count target.

2. **Variant 2 tests both sides of an owner gate.** R2-G7 finds that item 6.1 creates PENDING, Branch 1 in 6.2 stops on PENDING, and only Branch 2 resolves it. An authentic owner reply does not by itself change that file status. The same resume defect appears in item 7.4 and item 14.7, so the merge should address the shared procedure rather than only one occurrence (TL:982-989,1165,2481; diff-analysis.md:45,64). Variant 3's positive account of the halt is incomplete because a gate must also resume.

3. **Variant 2 compares the Action with its own evidence rule.** R2-G3 finds that item 7.16 requires path discovery with `echo` and `ls`, then accepts only eight Orca templates or file reads. It also expects a forbidden-list sentence that the Action never requires recording. Correct capture therefore fails Verification even before considering hostile text in captured output (TL:1258-1260; variant-2-original.md:240-243).

4. **Variant 2 distinguishes missing evidence from proof of failure when calibrated.** R2-G8 remains MEDIUM because normal verbose test output does not establish that the subprocess guard rejects actual calls. This warrants an explicit negative guard test, not a claim that subprocesses already escaped (variant-2-original.md:260-263). R2-G6 likewise remains MEDIUM: six aggregate matches cannot prove one PASS per gate, but the false-pass case requires an abnormal distribution of matches (variant-2-original.md:252-255).

5. **Variant 2 follows some false matches through to their consequence.** INF-001 is not merely relabelled: item 7.26 does not carry the required count-citation and REPORT-protection rule. The diff analysis verifies the previously incomplete absence claim, while preserving MEDIUM severity (variant-2-original.md:51,67-74; diff-analysis.md:48). Its D3, D4 and D5 rows also distinguish unrelated owner-decision matches from real delivery (variant-2-original.md:30-32).

## Weaknesses Identified (in the other variants)

- **Variant 1 establishes delivery more often than verification soundness.** Its NFR-013 coverage verdict does not address whether item 8.9 can demonstrate that the guard works. R2-G8 supplies that narrower missing check; the distinction is construction versus demonstrated behaviour (variant-1-original.md:52; diff-analysis.md:51).
- **Variant 1's M2 claim and remedy overreach.** Item 7.17 explicitly inherits DESIGN's behaviour until closed, and DESIGN open item 3 already routes a JSON need to the owner. Its recommendation incorrectly names open item 2. The surviving issue is explicitness, not absence of any owner route (TL:1265; DESIGN:971; variant-1-original.md:298-301).
- **Variant 3's R3-G10 treats stopping as a complete approval mechanism.** The owner-word requirement is real, but it does not repair the PENDING resume branch. Its calibration did not test that branch logic, so the positive finding does not rebut R2-G7 (diff-analysis.md:64; variant-3-original.md:195-198).
- **Variant 3 sometimes stops at a false matrix match.** INF-005 and INF-014 need two answers: whether the matched item is wrong and whether another item delivers the requirement. Variant 2 supplies alternate delivery mappings; Variant 3 supplies only the first answer (variant-2-original.md:55,64; variant-3-original.md:37-38; diff-analysis.md:73).
- **Variant 3's seam-extraction preference is not a demonstrated defect.** Its cited precedent also replaces the whole `_git`, so it does not support the claimed contrast. The calibration explicitly calls R3-G7 a design preference, not a defect; a new helper is not justified by that precedent alone (variant-3-original.md:183-186).

## Concessions

- Four of my seven HIGH findings were overstated. R2-G1, R2-G2, R2-G6 and R2-G8 are MEDIUM. R2-G4 and R2-G9 also fall from MEDIUM to LOW. The calibrated total, not my original count, must drive prioritisation (variant-2-original.md:231-271; diff-analysis.md:23).
- R2-G2 is weak authorization evidence, not demonstrated gate bypass. The executor is still told to wait for the person. I withdraw the `gate-bypass` label for this finding while retaining the missing quoted-source condition (variant-2-original.md:236-239).
- My `covered` verdict for INF-013 and `covered-in-substance` verdict for GQ-106 fail to separate construction coverage from verification adequacy clearly enough. They should state that distinction, rather than leaving readers to reconcile them with G8 and G4 (variant-2-original.md:20,63,187-192).
- R2-G9 mixes a traceability issue with a design critique. DESIGN itself claims that the import test enforces B2. A stronger path-method check could improve that design, but it is not automatically a tasklist deviation. The matrix-omission portion is the narrower surviving LOW claim, and I did not independently reopen the matrix here (DESIGN:216; variant-2-original.md:264-267).
- R2-G10 is a before-release deliverable gap, not a present execution blocker. DESIGN permits the proposed limits meanwhile. Its whole-file absence claim remains less fully established than the count-rule absence established by the diff analysis (DESIGN:987; variant-2-original.md:268-271; diff-analysis.md:48,52).
- R2-G4 is conditional on pre-existing changes, and my 9.2 citation was off by two lines. It is LOW, not a guaranteed failure on the specified clean path (variant-2-original.md:227-230,244-247).
- None of the three cards supplies the required deviation category in addition to `gap_class`. My higher clarity score is not evidence of compliance, because only Variant 1's calibrator penalised this shared omission. The merge must classify consistently and separate confirmations from defects (diff-analysis.md:36-37,131).
- My overall grade 2 is not independently calibrated. It usefully signals the proven execution blockers, but cannot be treated as an objectively superior overall grade to the other cards' grade 4 (diff-analysis.md:72).

## Shared Assumption Responses

| Assumption | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | Delegation covers a requirement only if the revised target still carries it and the referring item identifies that target. The Phase 2 to 6 edits make this a preservation check, not a blanket rejection of delegation; R3-G1 survives only as LOW ambiguity (diff-analysis.md:46,112; variant-3-original.md:159-162). |
| A-002 | QUALIFY | Literal execution is the right test for a written acceptance rule, but an executor may identify a contradiction and seek a correction. That possible recovery does not make an impossible check sound or authorize silently rewriting it; R2-G3, G5 and G7 remain HIGH plan defects, not inevitable runtime incidents (diff-analysis.md:83-85,113). |
| A-007 | REJECT | No review can guarantee that master or numeric anchors remain stable until execution. The tasklist already instructs relocation by section heading after design edits, so use that mitigation and refresh external anchors rather than assuming frozen line numbers (TL:1414; diff-analysis.md:118). |

## Per-Point Positions

These positions concern the exact difference, not a blanket ranking of the cards. A calibrated position is explicitly identified where it corrects its own original card.

| Point | Superior position | One-line reason |
|---|---|---|
| S-001 | V1 | It audits the broadest FR, NFR and implementation-step set, although 76 rows do not prove whole-plan completeness (diff-analysis.md:30). |
| S-002 | V1 | Mapping to actual Phase 7 to 14 delivery is stronger for implementation coverage than mapping only to design fixes (diff-analysis.md:31). |
| S-003 | V2 | File paths with ranges preserve the local context needed to examine multi-branch checks (diff-analysis.md:32). |
| S-004 | V2, calibrated | Three HIGH execution-contract defects survive calibration; four other original HIGH ratings do not (diff-analysis.md:23,33). |
| S-005 | V2 | Its explicit recommended action and not-checked fields better bound what the review establishes (diff-analysis.md:34). |
| S-006 | V3 | Zero failed citations among 40 checks is the cleanest reported grounding result, not proof of broader coverage (diff-analysis.md:35). |
| S-007 | V2 | Every finding requests a change instead of inflating the defect list with positive confirmations (diff-analysis.md:36). |
| S-008 | tie | All omit the required deviation category, and unequal calibration penalties cannot establish superiority (diff-analysis.md:37). |
| S-009 | tie | The three cards cover complementary Tier-1 findings and jointly touch F1 to F9 (diff-analysis.md:38). |
| C-001 | V2 | R2-G3 proves a required discovery command is rejected by the same item's Verification (diff-analysis.md:44). |
| C-002 | V2 | Its resume deadlock is the strongest blocker, while V3's wrong-question finding remains a separate necessary addition (diff-analysis.md:45). |
| C-003 | V3, calibrated | LOW wording ambiguity is better supported than either a lost rule or unqualified coverage (diff-analysis.md:46). |
| C-004 | V1 | Its direct delivery-label repair better distinguishes real coverage from traceability without V2's design-critique overreach (diff-analysis.md:47). |
| C-005 | V2, calibrated | The mandatory count-citation and REPORT rule is absent, now independently checked, but remains MEDIUM (diff-analysis.md:48). |
| C-006 | V1 | R1-G3 identifies the exact folder restriction that can make the final reviewer falsely block valid tests (diff-analysis.md:49). |
| C-007 | V2 | The model-name counterexample establishes an unavoidable false failure, beyond the lower-severity brittle checks (diff-analysis.md:50). |
| C-008 | V2, calibrated | Lack of a negative guard test is MEDIUM false assurance, stronger than coverage alone or a helper preference (diff-analysis.md:51). |
| C-009 | V2, calibrated | The before-release rationale obligation survives without V1's inaccurate assertion that pipx installs nothing (diff-analysis.md:52,69). |
| C-010 | V1, calibrated | A final handoff reminder adds value while recognising that grouping is already documented and commits are not authorized (diff-analysis.md:53). |
| C-011 | tie | Both documented extra gates and heading-based relocation are valid confirmations, not new defects (diff-analysis.md:54). |
| C-012 | V3 | It identifies the unbounded command Trigger while distinguishing planned renumbering from current text (diff-analysis.md:55). |
| C-013 | V3, calibrated | It catches extra R8 scope but properly keeps the harmless CHANGELOG addition LOW (diff-analysis.md:56). |
| C-014 | V3, calibrated | Its verified non-reuse explanation is useful, while the extra architecture check is LOW and the confirmation is not a defect (diff-analysis.md:57). |
| C-015 | V2 | It follows INF-001 to a missing obligation and re-maps unrelated D3 to D5 hits to real delivery (diff-analysis.md:58). |
| X-001 | V2 | The PENDING branch prevents the resolving branch from running; requiring the owner's words alone does not fix resume (diff-analysis.md:64). |
| X-002 | V3, calibrated | The surviving claim is ambiguous wording, not loss of the single-row transcript rule (diff-analysis.md:65). |
| X-003 | V3 | Item 2.16 is a report-only QA lens, not the edit Variant 1 calls it (diff-analysis.md:66). |
| X-004 | V1 | Following DESIGN's stated import-test mechanism is coverage; V2's stronger enforcement proposal is a design critique (diff-analysis.md:67). |
| X-005 | V1, calibrated | Inherited behaviour supplies an owner route for open item 3, leaving only an explicitness improvement (diff-analysis.md:68). |
| X-006 | V1, calibrated | Its own calibration correctly withdraws the claim that temporary pipx execution installs nothing (diff-analysis.md:69). |
| X-007 | tie | V2's coverage and verification judgments can coexist, but the card fails to explain that distinction consistently (diff-analysis.md:70). |
| X-008 | V2, calibrated | The calibration correctly lowers four HIGH ratings and rejects the bypass interpretation of G2 (diff-analysis.md:71). |
| X-009 | tie | Uncalibrated overall grades cannot settle whether broad compliance outweighs a few concrete blockers (diff-analysis.md:72). |
| X-010 | V2 | It preserves the false-match observation and also supplies actual delivery for INF-005 and INF-014 (diff-analysis.md:73). |
| X-011 | V1 | For live-capture delivery, its Phase 7 mapping is more relevant than a Phase 2 design edit, without denying that edit's coverage (diff-analysis.md:74). |
| X-012 | V3, calibrated | Its calibration correctly treats seam extraction as a preference after rejecting the claimed precedent contrast (diff-analysis.md:75). |
| A-001 | tie | All need to check delegated content after revision; V3's calibrated ambiguity is a warning, not proof delegation generally fails (diff-analysis.md:112,65). |
| A-002 | V2 | It supplies three concrete contradictions under literal checks without requiring faith that executors cannot recover (diff-analysis.md:113,83-85). |
| A-007 | tie | None establishes future anchor stability, and the existing heading-relocation instruction is the defensible mitigation (diff-analysis.md:118; TL:1414). |
