# QA Report: Applicability Citation Corrections

**Topic:** Correction of factual-source citation precision  
**Date:** 2026-10-23  
**Phase:** Full Task Phase 4 gate  
**Fix cycle:** 1 of 3  
**Status:** Exact corrections prepared and validated in memory; no files modified  
**Governing template:** Task Standard QA Report Output Format and Serialized Fix Protocol

| Status | Result |
|---|---|
| DONE | Prepared 30 exact replacements covering all 18 inventory rows, six attributed historical-attempt rows, the decision-evidence paragraph and five evidence-trail entries. |
| NEXT | Parent applies the replacements through the dedicated editor, records actual application results and obtains fresh structural and content verification. |

## Overall Verdict

**FAIL: the existing finding remains unresolved on disk.** The complete correction proposal follows. This return is not application evidence or independent quality-gate approval.

Higher-priority instructions prohibit writing report files. Neither the applicability artifact nor the prepared fix-log skeleton was edited.

**Target:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md`

**Intended fix log:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-phase-4-fix-log.md`

## Items Reviewed

These are correction-preparation checks, not a replacement for either independent verifier.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Finding, scope and governing instructions inspected | PASS | Read the complete consolidation, originating evidence-quality report, target and prepared fix log; read actual Step 4.1, evidence-quality requirement, Standard QA format, Serialized Fix Protocol and Web Research template. |
| 2 | All 18 factual inventory rows receive specific support | PASS | Read the actual source passages listed below. In-memory validation confirmed a citation addition in each existing inventory row. |
| 3 | Additional assertions with the same citation defect addressed | PASS | Added precise support for six attributed historical-attempt rows and the decision-evidence paragraph; replaced four whole-file references and the supplementary oracle entry’s undifferentiated range. |
| 4 | Replacements are unique and sequentially applicable | PASS | Successful UV inspection asserted exactly one match for each of 30 replacements against the progressively modified in-memory text. |
| 5 | Protected content and physical layout preserved | PASS | Mechanical comparisons confirmed all 18 questions and handling cells unchanged, provider accounting unchanged, persistence receipt unchanged and the original 182 LF-terminated records retained. |
| 6 | Actual and prospective identities distinguished | PASS | Measured the original SHA-256, computed the prospective SHA-256 and confirmed actual disk bytes remained equal to the original after the simulation. |

## Summary

- Preparation checks passed: **6 / 6**
- Preparation checks failed: **0**
- Existing unresolved findings on disk: **1 MINOR**
- Replacements prepared: **30**
- Replacements applied: **0**
- Findings independently closed: **0**
- New findings established: **0**
- Independent verification: **not performed**
- Current gate counter: **Phase 4 correction cycle 1 of 3 only**

**Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

Confidence covers the preparation checks above, not application, independent acceptance or historical certainty.

**Tool engagement:** Read: 25 attempts, including one unchanged-file freshness response | Grep: 0 | Glob: 0 | Bash: 4

Dedicated Grep and Glob tools were unavailable. One focused `rg` inspection located supporting passages; dedicated Reads inspected their actual contents. No external lookup was needed or performed. Graph coverage warnings were not treated as evidence; the proposal relies on direct Reads.

**Unchecked preparation items:** None.  
**Unverifiable preparation items:** None.  
**Outstanding execution:** Actual application and both independent verifications remain parent-owned.

## Issues Found

| Severity | Location | Issue | Required correction |
|---|---|---|---|
| MINOR | Applicability artifact, factual inventory and supporting evidence references | Existing assertions lack sufficiently precise claim-to-source bindings. Stable identity: `phase4-applicability-citation-precision`. | Apply the exact replacements below without changing historical conclusions, uncertainty or external-research applicability. |

## Actions Taken

- Read the complete assigned finding records and actual target before preparing corrections.
- Read supporting passages directly rather than treating the consolidation’s examples as proof.
- Examined the documentation case’s actual account to check rendering and acceptance details, then bound the proposed citation to the already-listed evidence deck’s corresponding passage.
- Prepared only additions or replacements of source references. No factual inventory question or external handling cell changes.
- Validated the complete patch sequence in memory.
- The first simulation stopped because its validation incorrectly expected 183 physical records. A bounded byte inspection established **182 LF-terminated records**; the corrected simulation passed. No file was modified during either attempt.
- All UV inspections reported the inherited environment-path warning; the final simulation completed successfully.
- Performed no writes, child-agent launches, tests, Git operations, production/configuration changes, historical-source changes, moves, archives, deletions or publication.

### Actual and prospective target identities

| Identity | SHA-256 |
|---|---|
| Actual original bytes | `68c6776dc388d5959ffe451e1ea4def82d2705454dea08ba9d9a21db007fe952` |
| Expected bytes after exactly these 30 replacements | `86f0703346beb06755a16d3866d4e245bab4f9b8d396e31e50e86f5014126e94` |

Each replacement has **one sequential match**. Both actual original and prospective text contain **182 LF-terminated records**. The expected-after hash is not a claim about current disk state.

## Exact Source-Backed Patches If Direct Writes Are Prohibited

Apply in array order. These are literal substring replacements within existing physical lines, not whole-file rewrites.

```json
[
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "**Evidence:** The live task’s Step 4.1; the complete gap register; the evidence deck’s Gaps and Questions section; and the rule map’s historical-version and enforcement limitations, listed under Evidence Trail.",
    "repl": "**Evidence:** The live task’s Step 4.1 at `TASK-RESEARCH-review-loops-20261023-032537.md:253-259`; gap-register limits at `gaps-and-questions.md:11-13`, `:33-35` and `:55-59`; individual deck questions at `evidence-deck.md:831-845`; and historical-version/enforcement limits at `scope-rules.md:66-77` and `:88`. Inline citation filenames resolve through the absolute paths in Evidence Trail.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Other individual miss reasons remain unknown.",
    "repl": "Other individual miss reasons remain unknown. Sources: `evidence-deck.md:585-598` and `evidence-deck.md:831`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Update authorship and uncaptured versions remain unknown.",
    "repl": "Update authorship and uncaptured versions remain unknown. Sources: `scope-rules.md:66-77` and `evidence-deck.md:832`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "No controlled same-input, same-rubric comparison was observed.",
    "repl": "No controlled same-input, same-rubric comparison was observed. Sources: `scope-rules.md:73` and `evidence-deck.md:833`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "The final amendment has no subsequent independent semantic review in the recorded incident.",
    "repl": "The final amendment has no subsequent independent semantic review in the recorded incident. Sources: `evidence-deck.md:834`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "The gap register retains the no-op versus patch-check tension and the pre-fetched-input versus before-any-upstream-call tension.",
    "repl": "The gap register retains the no-op versus patch-check tension and the pre-fetched-input versus before-any-upstream-call tension. Sources: `gaps-and-questions.md:33-35` and `gaps-and-questions.md:59`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "No implementation execution was observed within its declared windows.",
    "repl": "No implementation execution was observed within its declared windows. Sources: `evidence-deck.md:835`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Local/static traces and reviewer reproductions do not establish the corresponding live-runner outcomes.",
    "repl": "Local/static traces and reviewer reproductions do not establish the corresponding live-runner outcomes. Sources: `evidence-deck.md:836` and `gaps-and-questions.md:58`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Static resubmission did not satisfy the rendering condition; the criterion was accepted as unverified.",
    "repl": "Static resubmission did not satisfy the rendering condition; the criterion was accepted as unverified. Sources: `evidence-deck.md:240-247` and `evidence-deck.md:837`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "No eighth Task 12 review establishes repair.",
    "repl": "No eighth Task 12 review establishes repair. Sources: `evidence-deck.md:838` and `gaps-and-questions.md:44`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "The quoted platform body limit was not independently certified.",
    "repl": "The quoted platform body limit was not independently certified. Sources: `evidence-deck.md:839`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Deterministic fixture and assertion evidence does not establish live-model behavior.",
    "repl": "Deterministic fixture and assertion evidence does not establish live-model behavior. Sources: `evidence-deck.md:840`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Preserved fixture evidence supports a narrower comparison; the historical reviewer lacked a separately preserved complete earlier oracle snapshot.",
    "repl": "Preserved fixture evidence supports a narrower comparison; the historical reviewer lacked a separately preserved complete earlier oracle snapshot. Sources: `evidence-deck.md:841`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Screening covers observed top-level invocations and selected linked reviewers, not every possible nested log.",
    "repl": "Screening covers observed top-level invocations and selected linked reviewers, not every possible nested log. Sources: `evidence-deck.md:842`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "The credential cases demonstrate that distinction.",
    "repl": "The credential cases demonstrate that distinction. Sources: `evidence-deck.md:843` and `evidence-deck.md:557-563`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "It does not inspect or execute every helper.",
    "repl": "It does not inspect or execute every helper. Sources: `scope-rules.md:88` and `evidence-deck.md:844`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Separately timed continuations and fingerprints retain their own boundaries.",
    "repl": "Separately timed continuations and fingerprints retain their own boundaries. Sources: `evidence-deck.md:20`, `evidence-deck.md:845` and `gaps-and-questions.md:27`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "All thirty membership slots were screened, but synthetic exclusions, clustered work families and differing incident types prevent treating them as comparable independent runs.",
    "repl": "All thirty membership slots were screened, but synthetic exclusions, clustered work families and differing incident types prevent treating them as comparable independent runs. Sources: `gaps-and-questions.md:11`, `evidence-deck.md:49-58`, `evidence-deck.md:74-105` and `evidence-deck.md:162`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "The gap register distinguishes the earlier seven-pair agreement from a later three-equal/four-different observation.",
    "repl": "The gap register distinguishes the earlier seven-pair agreement from a later three-equal/four-different observation. Sources: `gaps-and-questions.md:56`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "These establish failure at those requested historical locations, not credential-case unavailability or absent rendering everywhere.",
    "repl": "These establish failure at those requested historical locations, not credential-case unavailability or absent rendering everywhere. Sources: `qa-phase-3-fix-log.md:95-116`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "The gap register records a canonical archived-package mapping and three independently checked artifact hashes.",
    "repl": "The gap register records a canonical archived-package mapping and three independently checked artifact hashes. Sources: `gaps-and-questions.md:55`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Graph absence is not repository absence.",
    "repl": "Graph absence is not repository absence. Sources: `02-session-a9b88895.md:61-71`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "The rule map records two actual nested reviewer Read results and retains their decoded texts in the historical-rule capture.",
    "repl": "The rule map records two actual nested reviewer Read results and retains their decoded texts in the historical-rule capture. Sources: `scope-rules.md:66-77`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "It does not establish exhaustive absence of every arbitrary nested invocation, statistical independence or prevalence.",
    "repl": "It does not establish exhaustive absence of every arbitrary nested invocation, statistical independence or prevalence. Sources: `evidence-deck.md:74-105`, `evidence-deck.md:58` and `evidence-deck.md:842`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Later observation does not retroactively create an original-time byte snapshot.",
    "repl": "Later observation does not retroactively create an original-time byte snapshot. Sources: `gaps-and-questions.md:27`, `gaps-and-questions.md:43-44` and `evidence-deck.md:845`.",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Complete file; especially Evidence Gaps, Process Limitations, Unresolved Contradictions and Current Verification and Remaining Research Limits",
    "repl": "Selection/history: lines 11-13; failed attempts/live growth: 21-27; source contradictions: 33-35; later CI/monitor endpoints: 43-44; navigation, protocol comparison, causal/runtime/specification limits: individual rows 55-59",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Complete file; especially Historical and Current-State Qualifications",
    "repl": "Named-gate-only acceptance: lines 12-13 and 48; historical/current protocol comparison: 72; population, unknowns and accepted-unverified rendering: 74; later synthesis/ranking not certified: 78",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Complete file; especially Method and Counting Rules, Source Inventory and Traceability, and Gaps and Questions",
    "repl": "Membership versus bytes: line 20; incident/population limits: 49-58, 74-105 and 162; rendering/acceptance: 240-247; credential-pointer examples: 557-563; checked-versus-required properties and unknown misses: 585-598; source inventory: 749-772; fifteen individual remaining questions: 831-845",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "Complete file; especially Recovered historical loaded-rule mapping and Gaps and Questions",
    "repl": "Captured historical load provenance: line 66; two loaded versions: rows 70-71; policy/evidence confounding: 73; unknown versions/authorship: 77; helper-inspection and historical-compliance limits: 88",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  },
  {
    "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/web-01-gap-applicability.md",
    "mode": "literal",
    "needle": "| Lines 1-110 | Oracle evidence inventory, graph-coverage limitation and bounded historical chronology |",
    "repl": "| Evidence inventory: lines 30-67; graph-coverage limitation: 71; repair chronology: individual rows 79-102 | Oracle evidence inventory, graph-coverage limitation and bounded historical chronology |",
    "expected_count": 1,
    "finding_ids": ["phase4-applicability-citation-precision"]
  }
]
```

## Source Bindings and Preservation

### Actual source-read and citation map

All passages below were inspected through dedicated Reads before preparing their citation replacements. This records inspection of the supporting research, not a rerun of its historical investigation.

| Actual source | Inspected support used |
|---|---|
| `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/TASK-RESEARCH-review-loops-20261023-032537.md` | Lines 253-259: actual conditional external-research assignment and permitted reasoned N/A. |
| `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/evidence-deck.md` | Line 20: membership versus bytes. Lines 49-58, 74-105 and 162: differing incidents, complete screening dispositions and population limits. Lines 240-247: notice output, unsuccessful static resubmission and acceptance without rendering proof. Lines 557-563: credential evidence-pointer examples. Lines 585-598: concrete checked-versus-required mismatches and unknown miss reasons. Lines 749-772: source inventory. Each individual row at 831-845: corresponding remaining question. |
| `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-rules.md` | Line 66: captured-load provenance. Rows 70-71: two actual historical rubric texts. Line 73: policy/evidence confounding. Line 77: unknown versions and authorship. Line 88: helper-inspection and historical-compliance limits. |
| `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/gaps-and-questions.md` | Lines 11-13: selection, reconstruction and historical-rule limits. Lines 21-27: failed attempts and growing sources. Lines 33-35: both specification contradictions. Rows 43-44: separately timed CI/monitor endpoints. Rows 55-59: recovered navigation, dated protocol comparison, causal unknowns, runtime limits and unresolved specification interpretation. |
| `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/phase-outputs/plans/research-gate-decision.md` | Lines 12-13 and 48: named-gate-only scope. Line 72: dated protocol comparisons. Line 74: population and accepted-unverified rendering qualifications. Line 78: later synthesis and rankings not certified. |
| `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/02-session-a9b88895.md` | Lines 30-67: evidence inventory. Line 71: excluded graph coverage and actual alternative evidence basis. Individual rows 79-102: repair and review chronology. |
| `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-phase-3-fix-log.md` | Lines 95-116: canonical documentation-package attribution, exact failed request/result mapping and interpretation limits. |
| `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/03-session-6f744b87.md` | Additional direct check of rendering, static resubmission and acceptance details. No new citation to this file is needed because the listed evidence deck already supplies precise supporting passages. |

### Preservation established by the proposal

- All **18 original inventory questions** remain unchanged.
- All **18 external-applicability handling cells** remain unchanged.
- All **15 evidence-deck questions** remain represented; none is closed or replaced.
- Unknown individual miss causes, update authorship and uncaptured historical versions remain unknown.
- The separate effects of policy change and evidence correction remain confounded.
- Original criteria, authority boundaries, accepted-but-unverified rendering and runtime/sampling limitations remain unchanged.
- Provider nonuse, zero external-query counts, untested availability and N/A fallback remain unchanged.
- The original producer’s activity descriptions and separate parent persistence receipt remain intact.
- No original review, consolidation, task, source, gap register, decision, synthesis, hypothesis, debate or historical capture was changed.
- This proposal does not advance the phase or evaluate regression, strict-shrink or cap guards for an unapplied correction.

## Recommendations

Parent should first confirm the target still has the recorded original hash, apply the 30 literal replacements through the dedicated editor and compare the actual result with the expected-after hash. Record the actual application outcome in the prepared fix log, preserving this proposal’s distinction between simulated and applied state.

Then obtain the parent-owned fresh structural and content reviews. Do not treat this author’s preparation checks as either independent review.

## QA Complete

Correction preparation is complete. **Applied: 0. Unresolved on disk: 1 MINOR.** The Full Task Phase 4 gate remains **FAIL**, with correction cycle **1 of 3** awaiting application and independent verification.