# Round 1 Advocate Statement — Variant 2

## Position

V2 provides the strongest literal brief-compliance audit, not proof of a runtime failure. Retain its per-correction checks and small fidelity repairs, but reduce R2-01, R2-03 and R2-06 to P3. E-3 defeats the shared claim that short acceptance checks let an executor freely paraphrase explicit exact-copy instructions. No finding currently warrants P1; after calibration, none needs P2.

Citation aliases denote these absolute files; `alias:N` means line N of that file.

- `plan`: `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/TASK-WF-brainstormFixBri-20261106-113538.md`
- `source`: `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/source.md`
- `spec`: `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- `analyze`: `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/src/superclaude/commands/analyze.md`
- `qa`: `/home/coder/.claude/skills/sc-implement-protocol/refs/qa.md`
- `diff`: `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-113538-20261106113956/adversarial/diff-analysis.md`
- `matrix`: `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-113538-20261106113956/artifacts/coverage-matrix.yaml`
- `lc10`: `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc10-result.md`

## Steelman of V1

V1 probes the decision rule instead of merely checking its presence. The refusal concern has a real source: analyze:97 says refusal is printed in chat only, whereas plan:128 makes non-refusal part of the required-directory trigger. A checker that mistakes an unknown refusal status for confirmed non-refusal can produce a false FAIL. That deserves an owner-facing verification note, even though no such faulty checker was demonstrated.

V1 also correctly separates the command under test from its nested calls. Spec:296 requires the former to run at top level, while plan:128 explicitly permits the analyze invocation in a subagent file. Those rules can coexist; a checker that extends the former to all nested calls would break that coexistence. V1's formal concern about “only when” identifies a real necessary-versus-sufficient distinction in the owner text, not a miscopy by this plan.

## Steelman of V3

V3 offers the most concrete whole-text verification approach and extends it consistently across the three primitives and two spec sentences. It correctly notices that plan:143-145 checks selected strings and edit shape rather than all decision clauses in plan:128. Its distinction between a whole-excerpt equality check and the prescribed short substring pins is useful, subject to making that distinction explicit rather than declaring it automatically authorized.

V3 also checks the failure quality of verification recipes, not just their green path. Its HEAD-path guard concern and exit-status recording suggestion can improve evidence reliability. Its warning about step-4 extras versus the step-5 not-verifiable rule is a useful question to ask, even though it does not establish that the existing, narrowly scoped risk-4 sentence is false.

## Strengths claimed

1. **Separate literal compliance from substantive correctness.** A forbidden phrase quoted inside a negative check is not the failed-call contract bug returning. Likewise, a useful extra negative pin is still an unapproved departure from an exact pin list. These should be low-priority fidelity findings, not runtime regressions.
2. **Preserve owner-supplied wording until authorized otherwise.** Source:213 explicitly says “copy exactly, do not paraphrase”; source:237 says to record the risks, not remove them. Plan:134-138 preserves the five meanings but drops references and changes wording from source:240-244. R2-05 remains a sound P3 fidelity finding.
3. **Keep conflicting instructions visible.** Source:161 literally quantifies over every F-3 pin, but source:234-235 includes the independent analyze-only pin. The right response is to record a source contradiction and preserve both intended pins, not silently weaken F-3 or claim unqualified literal compliance.
4. **Keep deviation classification narrow.** Plan:131 already records the owner-required Necessary deviation in live-check placement and wording. That does not authorize unrelated changes to the exact pin set or residual-risk text. Conversely, proposals to change the owner's live-check semantics are owner notes, not plan-authored regressions.

## Weaknesses identified in V1 and V3

- **Both overstate the whole-text gap at P2.** Plan:119 and :125 explicitly require character-for-character copying. E-3 is independently confirmed by qa:9, :15-17 and :21: the reviewer receives task text and checks explicit instructions as well as acceptance criteria. Missing a mechanical equality check is weaker automation, not permission to paraphrase.
- **V1's “known false FAIL” needs qualification.** Analyze:97 supports the lack of a formal refusal marker, but plan:128 excludes refused calls. A correct checker can inspect chat or decline to claim a verified predicate. A missed refusal is a plausible checker failure, not a demonstrated contradiction in the trigger itself. Claims about Skill-call completion timing were not independently established here.
- **V1-F7 and V3-8 overgeneralize risk 4.** Plan:137 and source:243 specifically say the session file is missing or ambiguous. Spec:300 explicitly blocks the overall live-check PASS in exactly those cases through step 5. The extra is located at step 4, but the same run must also pass step 5. A readable session with an unrecognized analyze call is a different case, already discussed in risk 2; it does not disprove risk 4. I drop the proposed risk-4 correction as a current defect.
- **Do not weaken checks because hypothetical baseline failures might occur.** E-1 and E-2 settle today's clean-target and lint questions. Enlarging the allowed status namespace or accepting any out-of-scope lint finding is not justified by those observations. V3's stronger baseline comparison is preferable to V1's broad outside-six-files exception if baseline handling is later needed.
- **V3's Task 7 wording repair is not a complete logical repair.** Keeping “writes only the logs” and following it with “Besides the logs” still leaves a literal exception. Plan:153 already identifies the snapshot and generated dev copies, and source:169 requires the otherwise awkward sentence. This is inherited wording with explicit qualifications, not an undisclosed mutation.

## Concessions

- R2-03 was overstated at P2. The F-12 quantifier is a brief defect, while the plan preserves the intended two independent pins. Recommend P3 clarification, not an implementation gate.
- R2-06 was overstated at P2. A containment matrix can omit verifier provenance without proving omitted implementation behavior. Recommend P3 audit-artifact repair, not a plan correctness blocker.
- R2-01 also becomes P3 after E-3. Keep exact-copy automation as a useful additional check, but withdraw the assertion that compliant per-task QA necessarily accepts the example paraphrase.
- My checked-clean row established that plan:128 retains the refusal, timeout and tool-error qualifications. It did not establish that every future checker will interpret them correctly or that the sentence has zero false-FAIL risk. V1 supplies better edge-case coverage here.
- Whole-text equality should supplement, not replace, the prescribed substring pins. If an added equality acceptance criterion is thought to widen F-7's exact AC list, record or obtain clarification instead of silently claiming no interpretive question exists.

## Per-point positions

The table addresses all 22 scored points. “Superior” means the strongest supported position, not automatic agreement with its original severity.

| Point | Superior | One-line reason |
|---|---|---|
| S-001 | V2 | Its explicit F-1–F-17 results distinguish literal failures from otherwise-correct applied text; the other cards do not provide that completeness. |
| S-002 | V1 | Its separate unverified list is clearer, though E-1/E-2 now resolve the git and lint unknowns (diff:14-15). |
| C-001 | V2 | It covers all five exact-copy excerpts while preserving prescribed pins, but E-3 reduces the issue from P2 to P3 (diff:16; qa:17). |
| C-002 | V2 | Source:111 says exactly these pins; plan:144 adds a negative pin, so useful intent does not erase literal noncompliance. |
| C-003 | V2 | Source:161's universal quantifier conflicts with the independent pin required by source:68-69; clarify at P3. |
| C-004 | V2 | Plan:45 quotes the literal source:181 forbids anywhere in Task 1; this is a harmless verifier-scope failure, not the original bug. |
| C-005 | V2 | Source:213 and :237 require exact recorded risks; plan:134-138 paraphrases them without authorization. |
| C-006 | V2 | Matrix:10-54 omits the Verifier-line rows; retain this as P3 provenance repair rather than evidence of absent behavior. |
| C-007 | V1 | Necessary-versus-sufficient ambiguity exists in source:219 itself; only an owner clarification may change the prescribed sentence. |
| C-008 | V1 | Analyze:97 provides real evidence for the chat-only refusal edge case; classify it as an inferred checker risk, not a demonstrated false FAIL. |
| C-009 | none/all equal | E-1 says the six targets are clean today; a future guard is optional hardening, not a present infeasibility (diff:14). |
| C-010 | V3 | E-2 removes the claimed current lint blocker, but V3's explicit exit-status recording remains useful and avoids V1's overbroad lint waiver. |
| C-011 | V1 | Lc10:13 actually extended condition 2 to nested calls, so clarifying its scope is worthwhile despite spec:296's narrower wording. |
| C-012 | V2 | Risk 4 is expressly conditioned on a missing/ambiguous file; spec:300 already blocks overall PASS for those cases. |
| C-013 | none/all equal | V3's own void condition is satisfied by E-1; do not broaden the allowed task paths (diff:14). |
| C-014 | V3 | The missing Task 3 shape check is a genuine consistency observation, but plan:66 already instructs appending to the bullet and E-3 enforces instructions. |
| C-015 | V3 | Plan:111 lacks Task 4's path-existence guard; distinguish that small reliability issue from Task 4's broader “pins” claim at plan:95. |
| C-016 | none/all equal | Source:169 mandates the awkward sentence and plan:153 immediately states both exceptions; V3's rewrite does not remove the literal “only” issue. |
| X-001 | V2 | Preserve risk 4 verbatim: its actual missing/ambiguous-file premise is covered by spec:300; other step-4-only gaps need separate owner notes. |
| X-002 | V2 | Preserve the exact short-pin set and distinguish equality evidence explicitly; neither silent expansion nor an unexplained “not a pin” assertion settles source:111. |
| X-003 | V1 | Its edge-case probing is stronger than my checked-clean wording, but neither a missed-refusal checker nor a resulting false FAIL was reproduced. |
| A-001 | none/all equal | All three original P2 arguments share an assumption that E-3 contradicts; none has the superior original position (diff:16, :74). |

## A-001 response

**REJECT.** Per-task QA is not limited to acceptance criteria. Its input includes the task text (qa:9), its comparisons include explicit task instructions (qa:17), and its Missing label includes absent instructions (qa:21). The plan's character-for-character directions therefore remain enforceable without a separate whole-text AC.

**Qualification:** A machine equality check is more reproducible than asking a reviewer to compare a long sentence. Also, source:34 separately asks for AC checks equivalent to each correction's verifier. Those support a P3 verification-strength/fidelity improvement; they do not establish that a paraphrase must pass the existing executor. Reclassify the shared C-001 family accordingly.

## Priority table

Every finding from every card is included. P3 means retain as a minor repair, clarification or owner note; drop means do not carry it as a current defect. State guards and baseline observations are scoped to E-1/E-2's observed tree, not guaranteed for future trees.

| Card finding | Original | Recommended | Reason / scope |
|---|---|---|---|
| R1-F1 | P2 | P3 | Merge with R2-01/R3-2; E-3 refutes automatic paraphrase acceptance, while equality evidence still helps. |
| R1-F2 | P3 | P3 | Owner-note ambiguity in approved “only when”; no unilateral plan or spec rewrite. |
| R1-F3 | P3 | P3 | Keep the chat-only refusal and path-normalization verification questions; label false-FAIL behavior inferred, not reproduced. |
| R1-F4 | P3 | drop | E-1 establishes clean target files; no current shape-check failure, optional guard only. |
| R1-F5 | P3 | drop | E-2 establishes lint success; do not weaken the exit-zero criterion for hypothetical unrelated findings. |
| R1-F6 | P3 | P3 | Owner clarification is justified by lc10:13's historical overextension; the spec itself can already be read consistently. |
| R1-F7 | P3 | drop | Risk 4 already has the missing/ambiguous-file condition and spec:300 blocks overall PASS then. |
| R2-01 | P2 | P3 | Exact-copy checks improve verification but explicit instructions already bind under E-3. |
| R2-02 | P3 | P3 | Useful extra negative pin is still outside source:111's exact set; move to a review note or authorize it. |
| R2-03 | P2 | P3 | Source contradiction, not broken owner-rule coverage; preserve the independent analyze-only pin. |
| R2-04 | P3 | P3 | Rephrase the negative AC without quoting the forbidden literal; do not alter the correct applied sentence. |
| R2-05 | P3 | P3 | Restore exact residual-risk text, including references and INFERRED label; no functional claim is lost today. |
| R2-06 | P2 | P3 | Add verifier provenance/aliases to the audit matrix; do not treat containment coverage as literal equality. |
| R3-1 | P2 | drop | E-1 satisfies the card's void condition; widening exemptions would be unnecessary scope. |
| R3-2 | P2 | P3 | Merge with R2-01; concrete equality method is useful, severity premise is defeated by E-3. |
| R3-3 | P3 | P3 | Optional matching shape check for Task 3; E-3 still enforces the existing append-to-bullet instruction. |
| R3-4 | P3 | P3 | Keep the missing path guard and narrow Task 4's “pins fail” evidence claim; Task 5 already says singular “new phrase”. |
| R3-5 | P3 | P3 | Retain explicit exit-status recording only; E-2 defeats the current lint-baseline blocker and does not justify mandatory baseline machinery. |
| R3-6 | P3 | drop | Duplicate clean-start hypothesis; E-1 resolves it for this plan's current tree. |
| R3-7 | P3 | drop | Mandated source wording plus immediate explicit exceptions; proposed change does not eliminate the literal contradiction. |
| R3-8 | P3 | drop | Step-4 placement does not defeat step 5's independent PASS block when the same session file is missing/ambiguous. |

Recommended next action: carry the retained P3 findings into the synthesis as fidelity repairs or owner notes, merge duplicate whole-text-check findings, and remove the E-1/E-2-disproved blockers. Do not change the owner-prescribed live-check sentence or weaken test/lint/status checks on this debate's authority.

| DONE | NEXT |
|---|---|
| Compared all cards; verified cited source text; addressed all 22 points and all 21 findings. | Orchestrator synthesizes the calibrated findings; no implementation was performed. |

Limits: no tests, live worker, checker implementation or session-encoding experiment was run by this advocate. E-1/E-2 are the orchestrator's recorded observations; future tree changes require fresh state evidence.
