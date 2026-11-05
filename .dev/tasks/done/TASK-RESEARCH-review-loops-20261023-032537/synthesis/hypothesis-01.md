# Technical Research Report: Checks Prove Less Than the Requirement

**Date:** 2026-10-23  
**Depth:** Deep, inherited investigation scope; this operation is format-only  
**Research files read:** Six case reports, five screening summaries, one evidence deck and one rule map; supporting inputs are inventoried in Section 10  
**Scope:** Presentation of the existing first causal candidate, without changing its argument, evidence, limits or identity  
**Presentation status:** Post-debate format-only presentation. The actual debated source is the immutable `variant-1-original.md` identified in Section 10 at its recorded SHA-256.  
**Authorship and delivery:** Format-only synthesis worker, returned as text because report-file writes are prohibited. No file was created or modified, including no on-disk skeleton. Parent persistence and independent preservation checking remain required.

The numbered chapters below follow the governing Report Structure. Original substantive text is retained verbatim, once per original body section. Added text supplies presentation boundaries, reasoned N/A entries and provenance only. Original historical source paths remain recorded evidence anchors, not newly certified live objects.

## Table of Contents

1. Problem Statement
2. Current State Analysis
3. Target State
4. Gap Analysis
5. External Research Findings
6. Options Analysis
7. Recommendation
8. Implementation Plan
9. Open Questions
10. Evidence Trail

---

## 1. Problem Statement

*Presentation note, added after the debate and not part of the debated text:* the template's question, why-it-matters and trigger bullets are reasoned N/A for a single candidate card. The shared research question, its impact and the user-reported trigger belong to the whole package and are stated in Section 1 of `synthesis/synth-01-problem-current-state.md` (sources `BUILD-REQUEST.md:12,14`). The original hypothesis follows verbatim.

### Original Hypothesis

Repeated discovery is partly caused by checks that establish format, labels or presence while leaving the required behavior unproved. A later reviewer then exercises another already-existing failure path. Large units and deferred lasting tests amplify this gap; they are not independently proven universal causes.

---

## 2. Current State Analysis

This chapter preserves the original candidate's historical mechanism and support. “Current State Analysis” is the required report heading, not a claim that historical implementation files were freshly inspected during this presentation pass.

### Exact Mechanism

1. A behavioral requirement is represented by a weaker check: parsing, a keyword, a count, a marker, or the presence of a validation step.
2. Implementation and early review accept that narrower evidence without establishing execution order, semantic inputs, cross-component use, or exceptional paths.
3. The fix closes the demonstrated example but does not make the whole behavioral requirement executable at the current task boundary.
4. A later review finds another preexisting counterexample. This explains new discoveries without assuming the prior fix caused them.

### Supporting Incidents and Primary Evidence

**Counting:** Multiple examples within one incident are not independent session observations.

Paths below are primary-source locations recorded and checked in the linked case reports; historical raw anchors mean physical JSONL records, not current product-file lines.

| Incident | Observed mechanism | Research and primary anchors |
|---|---|---|
| Oracle semantics | Family counts, labels and one-field differences pass while known/unknown author and default-path security meanings are wrong. Initial67/78 tests pass despite four valid defects. | [Oracle case](../research/02-session-a9b88895.md), sections4-5; `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/a9b88895-5374-4cae-8ebb-cac03a97aff1.jsonl:291`; preserved reviews under its task package `artifacts/t12-review-1.md:20-22` and `t12-review-2.md:20-40`, absolute package path in the case evidence register. |
| Orca monitor task | One640-line workflow combines three jobs and many behaviors; current acceptance checks are structural while lasting behavior tests are deferred to Task14. Later checks find originally present range, summary and size defects. | [Monitor case](../research/05-session-e002bed2.md), sections2-5; `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/e002bed2-7877-42c1-8665-8cb8595587b6.jsonl:585`, `:804`, `:906`, `:1021`; plan `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/tasks/to-do/TASK-WF-designSpec-20261022-132541/TASK-WF-designSpec-20261022-132541.md:209-232`. |
| Orca plan coverage | Coverage credits an up-to-date state that original tasks do not name; validation exists after the fetch that uses its input. Presence is mistaken for correct wiring or timing. | [Planning case](../research/01-session-ac2cd1fd.md), section4; first review `artifacts/coverage-matrix.yaml:1749-1757` under `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-20261022133138/`; second merged findings in sibling `pre-designSpec-v2-20261022150856/adversarial/merged-verdict.yaml:39-47`. |
| CI search and advisory checks | PR creation arguments are asserted, but the search stub ignores search filters; stronger phrase blacklists still accept contradictory advisory wording. | [CI planning case](../research/04-session-43582de1.md), sections6 and final-outcome supplement; `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-specR1-20261023-031725/TASK-WF-specR1-20261023-031725.md:117-129`; original plan and final probe comparisons are preserved in that case. |

---

## 3. Target State

The target of this operation is a ten-section presentation of the already-debated candidate, not a changed product or newly selected explanation.

- **Desired behavior:** Preserve the existing candidate's complete substantive text while placing it under the required report chapters.
- **Success criteria:** Every original body section appears once, verbatim; the support table retains its four data rows and citations; the original proposed test remains unexecuted; historical pre-debate wording is explicitly scoped to its original input state.
- **Constraints:** No new causal argument, counterexample, ranking, probability or change in evidentiary support. Preserve the original debate inputs and history. This presentation does not certify current production state or complete an independent quality gate.

Product requirements and implementation success criteria are **N/A** because this is a causal hypothesis card undergoing presentation-only restructuring.

---

## 4. Gap Analysis

A newly authored substantive gap analysis is **N/A**. Creating one would extend the original candidate rather than preserve its argument. Its original research gaps and stale-documentation assessment are retained in Section 9.

| Gap | Current State | Target State | Severity | Notes |
|-----|---------------|--------------|----------|-------|
| Presentation structure only | The preserved debated input uses its original research-card headings. | The same substantive bodies appear under the ten required report chapters. | N/A: no new defect-severity assessment | This is a formatting difference, not an additional causal finding or production defect. The old-to-new mapping is in Section 10. |

No remediation task, product-scope decision or new historical interpretation is created by this chapter.

---

## 5. External Research Findings

**N/A for this format-only causal card.** The original candidate contains no external-research findings to relocate. Adding external sources, relevance ratings or advice would introduce material outside the preserved argument.

No external lookup or publication was performed for this presentation. This N/A entry does not replace or revise the wider investigation's external-research component.

---

## 6. Options Analysis

Implementation options, effort estimates, implementation-risk ratings, code-reuse assessments and a new options-comparison table are **N/A**. This document presents one existing causal candidate, not a product implementation decision or a new comparison among the five candidates. Its original opposition and nonexclusive alternatives follow unchanged.

### Counterevidence

- The oracle's three permitted repairs worked; its second failure repeats the one deliberately frozen input defect. Weak checks explain initial escape, not the authorization barrier that prolonged that specific finding ([oracle case](../research/02-session-a9b88895.md), sections4-6).
- Smaller monitor Tasks10/11 converged after one repair using the same general arrangement. Task size/deferred testing is an amplifier here, not proof that independent review cannot converge ([monitor case](../research/05-session-e002bed2.md), section6).
- New plan defects and the stdout-trap regression have actual repair introductions. They cannot all be explained as earlier undetected behavior.

### Scope, Overlap and Competing Explanations

This candidate explains why previously wrong behavior survives apparently successful verification. Candidate two explains a different event: the repair introduces an interaction or fails to cover sibling paths. Candidate three explains changing judgments, not the missing original behavior itself.
Frozen fixtures, unavailable render tools and defective evidence pointers are competing immediate blockers. They may coexist with weak verification, but do not become instances of this hypothesis merely because a review fails again.

---

## 7. Recommendation

**Presentation-only recommendation:** Retain this candidate's existing identity and stated evidentiary limits. This card makes no new ranking recommendation and does not amend the completed debate's conclusions or endorsements.

### Provisional Evidence Strength and Limits

Strong case-specific support across oracle, monitor and both planning examples: concrete bad states satisfy weaker predicates or remain outside scheduled tests. The monitor size and deferred-test contribution is observational, not a controlled size experiment.
The sample is clustered and selected by recent file modification. No causal rate, probability, model comparison or claim that every new finding was missed initially is established.

### Key Takeaways

- A passing check can be genuine yet too weak for the requirement; validation presence is not validation timing, and fixture labels are not fixture meaning.
- Discovery of another old counterexample is not evidence that the preceding repair introduced it.

### Original Summary, Quoted as Historical Input State

The following paragraph is quoted verbatim from the original input. Its final sentence records that input's pre-debate state; it is **not** a current claim that the actual debate remains unfinished.

The evidence supports a recurring gap between what checks prove and what the task requires. That gap permits progressive discovery of old defects, particularly when lasting behavioral tests are deferred. Its relative likelihood against the other four candidates remains for the actual debate.

---

## 8. Implementation Plan

**UNEXECUTED. No execution authority is granted.** A production implementation plan, migration plan, rollback procedure and integration checklist are **N/A** for this format-only causal card. The complete original proposed discriminating test is retained below, without executing or extending it.

### Discriminating Test

Use preserved historical versions, not mutable current files, and keep original acceptance criteria and review policy fixed.
- For each later finding, construct its minimal counterexample on the version that first passed the existing checks.
- Run the described check against the counterexample and ask whether it still passes; separately verify whether the relevant behavior test was deferred or absent.
- If the original checks reject these wrong behaviors and were actually used, this mechanism weakens. If examples pass weak checks but fail a criterion-derived behavioral check, it strengthens.
This is a proposed bounded test, not a run performed for this card; it must not relax valid criteria or replace independent final review.

---

## 9. Open Questions

The original gap and staleness bodies are preserved below. No new question, resolution claim or causal explanation is added.

### Gaps and Questions

Why particular reviewers missed some counterexamples remains unknown. The contribution of task size versus the number of behavioral paths is not isolated. Historical tests were inspected, not rerun here.

### Stale Documentation Found

Historical coverage rows over-credit some behavior, and source test inventories omit requirements described elsewhere. These are specific historical findings in the case reports, not proof current production documentation is stale.

---

## 10. Evidence Trail

### 10.1 Preserved Original Input Identity

| Item | Exact identity or handling |
|---|---|
| Intended canonical presentation path | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/hypothesis-01.md` |
| Immutable actual debated source | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/variant-1-original.md` |
| Actual debated source SHA-256 | `3f39f065ffb13efad680694e9e699fb04456a03a93cabab75be90bee3d2dbac9` |
| Original invocation manifest | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/input-manifest.json` |
| Manifest's first-input record | Original canonical path, the source SHA-256 above, and 7,548 bytes. These describe the original invocation, not future formatted canonical bytes. |
| Observed manifest SHA-256 | `ecfa519d0ea0d95558ad53d38112c272ec75b0d5e5a0e096606e3dd46b6b72fc` |
| Pre-persistence byte check | The existing canonical file and preserved variant both returned the original source SHA-256 above during this pass. |
| Expected presentation identity | Persisting this report changes the canonical bytes and therefore its hash. That is an expected presentation change, not a newly authored hypothesis argument. No formatted-canonical hash is claimed in this text-only return. |
| Future original-source guards | Bind the original-input hash to the immutable preserved variant. Do not require formatted canonical bytes to equal the old input hash, and do not rewrite the old manifest to make that comparison pass. |
| Immutable history | No preserved variant, manifest, debate, scoring, merge or historical artifact was modified. No prior QA verdict, debate endorsement or broader synthesis inventory was updated. |

The original title was `# Research: Checks Prove Less Than the Requirement`. The original header metadata below is retained verbatim as a quotation of the **historical original-input state**, not as the current presentation's status or governing format:

```markdown
**Investigation type:** Evidence-backed causal hypothesis
**Scope:** Six selected historical sessions; candidate one, not a final rank
**Status:** Complete, hypothesis for debate; not ranked or independently approved
**Date:** 2026-10-23
**Governing template:** tech-research/SKILL.md, Codebase Research Agent Prompt
```

### 10.2 Original-Heading to New-Chapter Preservation Map

Original line ranges in this table refer only to the immutable debated source, not the formatted presentation.

| Original heading | Original body lines | New chapter and subsection | Body units retained verbatim | Required occurrence count |
|---|---:|---|---|---:|
| Hypothesis | 10 | 1, Original Hypothesis | One paragraph | 1 |
| Exact Mechanism | 13-16 | 2, Exact Mechanism | Four numbered items | 1 |
| Supporting Incidents and Primary Evidence | 19-28 | 2, Supporting Incidents and Primary Evidence | Counting paragraph; historical-anchor paragraph; complete table with four data rows and original citations | 1 |
| Counterevidence | 31-33 | 6, Counterevidence | Three bullets | 1 |
| Scope, Overlap and Competing Explanations | 36-37 | 6, Scope, Overlap and Competing Explanations | Two original text lines, unchanged and contiguous | 1 |
| Discriminating Test | 40-44 | 8, Discriminating Test | Opening line; three bullets; closing line | 1 |
| Provisional Evidence Strength and Limits | 47-48 | 7, Provisional Evidence Strength and Limits | Two original text lines, unchanged and contiguous | 1 |
| Key Takeaways | 51-52 | 7, Key Takeaways | Two bullets | 1 |
| Gaps and Questions | 55 | 9, Gaps and Questions | One paragraph | 1 |
| Stale Documentation Found | 58 | 9, Stale Documentation Found | One paragraph | 1 |
| Summary | 61 | 7, Original Summary, Quoted as Historical Input State | One paragraph, with its original pre-debate wording explicitly scoped as historical | 1 |

**Preservation inventory:** Eleven original substantive body sections are mapped to ten required report chapters. All four mechanism items, four supporting table rows, three counterevidence bullets, three test bullets and two takeaway bullets are retained. The original header metadata is quoted once separately. These are the intended exact-preservation counts for parent checking, not an independent QA verdict or a machine-verified comparison against a persisted formatted file.

### 10.3 Sources Actually Read for This Presentation

All package-local paths in the table resolve beneath:

`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`

| File | Role in this operation | Read and authorship boundary |
|---|---|---|
| `/config/.claude/skills/tech-research/SKILL.md` | Governing Report Structure and synthesis instructions | Read, including the actual ten-section structure before composing this presentation. |
| `TASK-RESEARCH-review-loops-20261023-032537.md` | Actual first-hypothesis assignment | Read the actual Step 5.6 and surrounding task context; no task-state changes made. |
| `research/research-notes.md` | Exact six-case assignment map | Read; used to identify the assigned empirical reports, not as a substitute for reading them. |
| `research/01-session-ac2cd1fd.md` | Orca planning case | Read in full, including conclusions and supplements. The file records main-session persistence of a restricted analyst's return. |
| `research/02-session-a9b88895.md` | Oracle case | Read in full, including conclusions and supplements. The file records main-session persistence of a restricted analyst's return. |
| `research/03-session-6f744b87.md` | Rendering and baseline case | Read in full, including its current-location qualification. The file records main-session persistence of a restricted analyst's return. |
| `research/04-session-43582de1.md` | CI planning case | Read in full, including the completed-outcome and corrected-disposition supplements. The file records main-session persistence of a restricted analyst's return. |
| `research/05-session-e002bed2.md` | Monitor case | Read in full, including the historical-prefix, acceptance and reviewer-identity qualifications. The file records main-session persistence of a restricted analyst's return. |
| `research/06-session-0690ee9f.md` | Credential final-review case | Read in full, including the eight-observation supplement. The file records main-session persistence of a restricted analyst's return. |
| `research/evidence-deck.md` | Complete cross-case evidence assembly | Read in full; treated as assembled research with its recorded provenance and limits, not as a new independent primary investigation. |
| `research/scope-rules.md` | Current-versus-historical protocol qualifications | Read in full; current instruction-source observations were not promoted to proof of historical execution. |
| `research/scope-01.md` | Screening indexes 01-06 | Read in full; screening is selection evidence, not a replacement for the case reports. |
| `research/scope-02.md` | Screening indexes 07-12 and controls | Read in full; successful controls and non-executed final review remain screening qualifications. |
| `research/scope-03.md` | Screening indexes 13-18 and controls | Read in full; separate package incidents and hidden historical review remain distinguished. |
| `research/scope-04.md` | Screening indexes 19-24 | Read in full; provisional screening counts were not used to rewrite the candidate. |
| `research/scope-05.md` | Screening indexes 25-30 | Read in full; retained frozen-fixture finding remains distinct from a fix-introduced defect. |
| `gaps-and-questions.md` | Existing uncertainty and temporal limits | Read in full; no gap was silently resolved or incorporated as new causal meaning. |
| `synthesis/hypothesis-01.md` | Existing canonical candidate | Read in full before any contemplated presentation change; unchanged on disk during this pass. |
| `reviews/adversarial/adversarial/variant-1-original.md` | Preserved actual debated argument | Read in full; used as the immutable verbatim source. |
| `reviews/adversarial/input-manifest.json` | Original invocation paths and hashes | Read in full. An initial lookup under the nested artifact directory returned “File does not exist”; directory inspection located the actual manifest at this path. Neither that failed lookup nor the corrected location changed any artifact. |

**Read inventory:** Six of six case reports, five of five screening summaries and the complete evidence deck were read. Twenty distinct source files are listed above. No primary historical log, product source, test or external source was newly investigated for this formatting operation.

### 10.4 Boundaries and Handoff State

The additional readings supplied qualifications for handling the original argument, not authority to rewrite it. Original primary citations are carried forward as historical recorded anchors. No claim is made that every historical target remains available at its old path.

Exactly the existing five candidate identities are preserved: this operation returns a presentation of candidate one only and does not create, replace or revise another candidate. No adversarial rerun, independent review, test execution, production action, staging, archive, move, deletion or external publication occurred.

| Status | Result |
|---|---|
| DONE | Returned the requested ten-section, format-only presentation with original substantive bodies and explicit historical-state framing. |
| DONE | Read every assigned case, the complete evidence deck, all five screening summaries, rule map, gap log, original candidate, preserved variant and actual manifest. |
| NEXT | Parent checks exact body preservation and preserved-source immutability before persisting this text at the intended canonical path. This return alone does not complete an independent quality gate or authorize another task item. |

### 10.5 Parent Persistence Record (2026-10-24)

The parent persisted this exact restricted return from current session subagents/agent-aformat-hypothesis-01-619825db3ba86fee.jsonl. Before writing, a mechanical check against the immutable debated source found all 30 non-heading original body lines present exactly once and none missing; the presentation has the ten required numbered chapters and no active placeholders. Saved body before this record: 22,587 UTF-8 bytes, SHA-256 `cd72eab0190a449b75a5b09e6991ce6df74a817636bfdc20ebb36bec7f6af4cf`. The preserved debated source remained `3f39f065ffb13efad680694e9e699fb04456a03a93cabab75be90bee3d2dbac9` after persistence. The worker's earlier "parent checks before persisting" NEXT row is its original handoff state, resolved by this record. Added text is presentation, N/A rationale and provenance only; this record is not an independent synthesis-gate verdict.

**Amendment receipt (2026-10-24, synthesis-gate fix cycle 2):** This receipt is appended below the original record above, which is not edited. At Task Step 5.24 (synthesis-gate fix cycle 1, finding P5-28) one presentation note, marked as added after the debate and not part of the debated text, was inserted in chapter 1 between `## 1. Problem Statement` and `### Original Hypothesis` (`qa/qa-synthesis-fix-log.md`, P5-28). That insertion added 439 UTF-8 bytes, so the saved-body figures in the record above (22,587 bytes, SHA-256 `cd72eab0…`) describe the body before Task Step 5.24. Measured the same way (every byte before the `### 10.5` heading except the two newline characters that precede it), the body now measures 23,026 UTF-8 bytes, SHA-256 `0e24ce0e180c888f16a3b55c3d240936f755c871ca8dcecb072dc66906e2f340`. A re-run exact-once check against the immutable `reviews/adversarial/adversarial/variant-1-original.md` (SHA-256 `3f39f065ffb13efad680694e9e699fb04456a03a93cabab75be90bee3d2dbac9`, unchanged) found each of its 34 distinct non-blank, non-heading lines other than the table separator exactly once in this card. The generic table separator line appears 1 time in the variant and 2 times in this card, both before and after Task Step 5.24; it is markdown syntax, not identity text. This receipt states or implies no synthesis-gate verdict.
