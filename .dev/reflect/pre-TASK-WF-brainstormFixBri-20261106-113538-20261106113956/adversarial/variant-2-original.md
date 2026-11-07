# Reviewer 2 card (qa lens, haiku slot = claude-gw-tier2), persisted verbatim by the orchestrator from the reviewer's reply.
reviewer: 2
persona: qa
model_slot: haiku
findings:
  - id: R2-01
    priority: P2
    claim: >-
      The acceptance criteria do not enforce the byte-for-byte replacement required
      by F-1 and F-3. The correct replacement text is present in the task bodies,
      but the acceptance checks only require selected substrings, placement and
      line counts.
    evidence:
      - ".dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/source.md:34"
      - ".dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/source.md:45"
      - ".dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/source.md:71"
      - "plan:45-46"
      - "plan:60-61"
      - "plan:75"
      - "plan:143-145"
    exact_change: >-
      Add acceptance checks comparing the three primitive replacement excerpts and
      both appended spec sentences with the corresponding source.md excerpts
      exactly. Preserve the prescribed substring-pin set rather than silently
      replacing it.
    verifier: >-
      [INFERRED] A change to an unpinned part of an approved excerpt must fail an
      acceptance check. For example, removing the command excerpt's explanation
      that enrichment_used does not show directory existence must not pass solely
      because its two shared pins remain.

  - id: R2-02
    priority: P3
    claim: >-
      F-7's literal verifier fails: Task 6 adds a negative substring check beyond
      the explicitly prescribed pin set. This is useful additional checking, but
      the source says the acceptance criteria list exactly those pins.
    evidence:
      - "source.md:109-111"
      - "plan:144"
    exact_change: >-
      Move the additional negative substring check into an explanatory review
      note, leaving the acceptance pin list exactly as F-7 prescribes, or obtain
      explicit authorization to extend that list.
    verifier: >-
      Task 6's acceptance pin list has the two companion-sentence pins and four
      live-check pins prescribed by source.md:109, without the additional
      negative pin unless that expansion is explicitly authorized.

  - id: R2-03
    priority: P2
    claim: >-
      F-12 cannot literally pass alongside F-3. Its verifier says every pin added
      under F-3 contains "no nested directory and no nested contract", but F-3 also
      expressly requires the independent "only by a `/sc:analyze` call" pin.
      The plan correctly includes that independent pin, so reporting F-12 as an
      unqualified literal PASS would conceal a contradiction in the brief.
    evidence:
      - "source.md:68-69"
      - "source.md:159-161"
      - "plan:87-88"
      - "plan:108"
    exact_change: >-
      Record the contradiction in the plan and request clarification that F-12
      applies to every no-directory/no-contract pin, not every F-3 pin.
      Do not remove or combine away the independently required analyze-only pin.
    verifier: >-
      An authorized clarification narrows F-12's quantifier; all no-directory
      pins contain the shared phrase, while the independent analyze-only pins
      remain. Until then, record the literal verifier as failed, not passed.

  - id: R2-04
    priority: P3
    claim: >-
      F-14's literal whole-task absence check fails because Task 1 quotes the
      forbidden wording inside its negative acceptance criterion. The applied
      skill text is correct; this is a verifier-scope defect, not a recurrence
      of conditional contract listing.
    evidence:
      - "source.md:181"
      - "plan:38"
      - "plan:45"
    exact_change: >-
      Rephrase the negative acceptance criterion without reproducing the forbidden
      literal, for example by requiring unconditional listing on failed outcomes.
      Keep the approved replacement sentence unchanged.
    verifier: >-
      The complete Task 1 text contains no occurrence of the literal prohibited
      by source.md:181, and its applied excerpt still ends with the approved
      failed-call listing sentence.

  - id: R2-05
    priority: P3
    claim: >-
      Part 4's "copy exactly, do not paraphrase" instruction is not fully followed
      for the residual-risk notes. Risks 1, 2 and 4 are paraphrased: the plan drops
      the INV-022 and INV-023 identifiers, removes the exact spec line references,
      and changes the explicit INFERRED label to lowercase prose. All five risks
      remain substantively represented.
    evidence:
      - "source.md:213"
      - "source.md:237-244"
      - "plan:134-138"
    exact_change: >-
      Copy the five residual-risk texts verbatim from source.md:240-244 into the
      plan notes, retaining their references and INFERRED label.
    verifier: >-
      Ignoring only list markers, each of the five risk texts equals its source
      counterpart exactly. The live-check and companion sentences already match
      and should remain unchanged.

  - id: R2-06
    priority: P2
    claim: >-
      The coverage matrix omits requirement-bearing verifier spans. It has rows
      for correction instructions but none for the 17 Verifier lines, which carry
      additional obligations such as exact pins, whole-task absence and the
      contradictory F-12 quantifier. It also omits the Part 4 exact-copy heading
      and the instruction to record, rather than remove, the residual risks.
      Therefore the reported coverage ratio does not measure all binding checks.
    evidence:
      - ".dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-113538-20261106113956/artifacts/coverage-matrix.yaml:1-54"
      - "source.md:45"
      - "source.md:111"
      - "source.md:161"
      - "source.md:181"
      - "source.md:213"
      - "source.md:237"
    exact_change: >-
      Add explicit verifier rows or documented clause-level aliases for source
      lines 45, 55, 71, 81, 91, 101, 111, 121, 131, 141, 151, 161, 171,
      181, 191, 201 and 211. Also represent lines 1, 5, 7, 213 and 237.
      Explicitly alias the repeated applied-text requirements at lines 65-69 to
      lines 231-235 instead of silently omitting their provenance. Distinguish
      semantic containment from literal equality.
    verifier: >-
      Every listed span has a coverage row or explicit alias; literal failures
      R2-02 through R2-05 remain visible even when their surrounding instruction
      obtains a high word-containment score. Recalculate coverage only after
      accounting for these spans.

self_reported_confidence: 0.93

per_correction:
  # plan = .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/TASK-WF-brainstormFixBri-20261106-113538.md; source = the package's source.md
  interpretation: >-
    Results below test each printed Verifier against the plan text.
    A textual PASS does not establish that its implementation acceptance
    criteria enforce the same obligation; R2-01 records that separate gap.
  rows:
    - {correction: F-1, result: pass, source_verifier_line: 45, plan_lines: [122, 128, 131], reason: "Both replacement sentences match; the Necessary deviation is recorded."}
    - {correction: F-2, result: pass, source_verifier_line: 55, plan_lines: [33, 44, 153, 158], reason: "Before/after snapshots are specified and Task 7 bullet 3 matches."}
    - {correction: F-3, result: pass, source_verifier_line: 71, plan_lines: [38, 54, 69, 87, 88, 108], reason: "Applied excerpts and both shared pins are present in the prescribed forms."}
    - {correction: F-4, result: pass, source_verifier_line: 81, plan_lines: [85, 87, 90, 93], reason: "Paragraph boundaries, three positive pins and the absence check are specified."}
    - {correction: F-5, result: pass, source_verifier_line: 91, plan_lines: [60, 85, 88, 93], reason: "Both anchored tier slices use the stated slicing pattern; smoke check remains."}
    - {correction: F-6, result: pass, source_verifier_line: 101, plan_lines: [153, 157], reason: "Both additional test files appear in the command and acceptance criterion."}
    - {correction: F-7, result: fail, source_verifier_line: 111, plan_lines: [119, 125, 131, 143, 144, 145], reason: "Placement and rationale pass, but the pin set has an extra negative check.", finding: R2-02}
    - {correction: F-8, result: pass, source_verifier_line: 121, plan_lines: [103, 109], reason: "Saved before-count plus two is required; no acceptance criterion fixes 18 or 19."}
    - {correction: F-9, result: pass, source_verifier_line: 131, plan_lines: [51, 61], reason: "Tier 1 quality_tier and Tier 2 Activation insertion points are distinguished."}
    - {correction: F-10, result: pass, source_verifier_line: 141, plan_lines: [85, 101, 105], reason: "The plan names lines 39 and 288 and explains why line 711 needs no change."}
    - {correction: F-11, result: pass, source_verifier_line: 151, plan_lines: [140], reason: "The preserved brainstorm row is correctly identified as section 3.1."}
    - {correction: F-12, result: fail, source_verifier_line: 161, plan_lines: [87, 88, 108], reason: "The independent analyze-only pin does not contain the no-directory phrase.", finding: R2-03}
    - {correction: F-13, result: pass, source_verifier_line: 171, plan_lines: [153], reason: "The exact source-file/log sentence is present, with the snapshot exception explained."}
    - {correction: F-14, result: fail, source_verifier_line: 181, plan_lines: [38, 45], reason: "Applied text passes, but Task 1 still contains the prohibited literal in its negative AC.", finding: R2-04}
    - {correction: F-15, result: pass, source_verifier_line: 191, plan_lines: [54], reason: "The routing bullet explicitly identifies analyze as the skill's other codebase action."}
    - {correction: F-16, result: pass, source_verifier_line: 201, plan_lines: [25], reason: "The required owner commit-and-merge qualification appears verbatim."}
    - {correction: F-17, result: pass, source_verifier_line: 211, plan_lines: [22], reason: "The plugin decision explicitly resolves spec open item 8."}

additional_part_checks:
  - part: 4
    result: fail
    source_lines: [213, 219, 223, 227, 231, 232, 233, 234, 235, 237, 240, 241, 242, 243, 244]
    plan_lines: [38, 54, 69, 87, 88, 108, 122, 128, 134, 135, 136, 137, 138]
    reason: >-
      Applied excerpts, pins and both spec sentences pass. All five risks are
      represented, but the exact-copy requirement fails for risks 1, 2 and 4.
    finding: R2-05
  - part: 5
    result: pass
    source_lines: [248, 249, 250, 251, 252]
    plan_lines: [21, 22, 23, 24, 26, 27, 33, 153, 158]
    reason: >-
      Research remains out of scope; the owner conflict, existing changes,
      six-file boundary, plugin exclusion, installed-text restrictions,
      UV/test settings and outward-action prohibitions are stated.

checked_clean:
  - {check: "The plan retains seven tasks in four phases.", evidence: ["plan:29-158"]}
  - {check: "The amended live-check trigger requires a Skill invocation of sc:analyze, not merely a Task or Agent prompt naming it; the approved timeout, refusal, tool-error and not-verifiable qualifications are retained.", evidence: ["plan:128", "source.md:219"]}
  - {check: "Existing assertions are preserved and the two routing tiers are pinned separately.", evidence: ["plan:85-95"]}
  - {check: "The baseline-aware final status criterion matches the approved replacement.", evidence: ["plan:158", "source.md:53"]}
  - {check: "Review was read-only. No commands, tests or implementation were run; runtime behavior and session-file encoding were not independently verified.", evidence: ["[INFERRED: reviewer tool-use record; only file reads were performed.]"]}
