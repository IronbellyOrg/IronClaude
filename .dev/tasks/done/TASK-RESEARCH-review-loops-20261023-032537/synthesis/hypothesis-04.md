# Technical Research Report: Brittle evidence and provenance handoffs

**Date:** 2026-10-24 (presentation date; the original input's own date is quoted in Section 10)  
**Depth:** Deep, inherited investigation scope; this operation is format-only  
**Research files read:** Six case reports, five screening summaries, one evidence deck, one rule map and one gap log; all inputs are inventoried in Section 10  
**Scope:** Presentation of the existing fourth causal candidate, without changing its argument, evidence, limits or identity  
**Presentation status:** Post-debate format-only presentation. The actual debated source is the immutable `variant-4-original.md` identified in Section 10 at its recorded SHA-256.  
**Authorship and delivery:** Format-only synthesis worker, returned as text because report-file writes are prohibited for this worker. No file was created or modified, including no on-disk skeleton. Parent persistence and independent preservation checking are still required.

The numbered chapters below follow the governing Report Structure. Every original non-heading body line appears verbatim, once, in its original order within its original section. Only headings and grouping change. Added text provides presentation boundaries, reasoned N/A entries and provenance, nothing else. Original historical source paths remain recorded evidence anchors. This pass does not certify them as live objects.

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

The conversion of verified work into durable proof sometimes loses meaning or provenance. A later reviewer then rejects missing, wrong or misleading evidence even when the delivered files did not regress.
This candidate explains evidence-only final failures and a false attribution of extra work; it does not explain every semantic defect in the sample.
**Key takeaway:** Proof can become the failing work product independently of the delivered implementation.

---

## 2. Current State Analysis

This chapter keeps the original candidate's historical mechanism and support. "Current State Analysis" is the required report heading. It does not claim that historical implementation files, ledgers or transcripts were inspected again during this presentation pass.

### Exact Mechanism

- Temporary test proof is replaced by an unrelated source-line citation when task QA becomes a ledger entry.
- A blank or incomplete evidence range survives the first final audit and is found by the next reviewer; repairing it changes proof, not delivery.
- Reconstructing the task baseline after editing from HEAD erases preexisting dirty work from the baseline, falsely making that work appear task-created.
- A missing checkpoint is classified by a guard as head-moved; that label does not itself prove HEAD changed.
**Key takeaway:** The common failure is an invalid connection between claim, evidence and historical state, not simply an inaccurate line number.

### Supporting Incidents

Case reports: [documentation and baseline case](../research/03-session-6f744b87.md), sections4-5; [credential final reviews](../research/06-session-0690ee9f.md), sections3-5.
Primary transcript root: `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/`.
The table's physical JSONL anchors are under that root, not line numbers in an extracted summary.

| Incident | Primary evidence | Discriminating observation |
|---|---|---|
| Initial credential package | `0690ee9f-c2f6-40ef-96be-1a0913a37866.jsonl:332,390,411,435`; nested `0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-abd76ef5e5d22848f.jsonl:36` | Genuine temporary lint proof became a README separator citation. Durable proof and pointer correction produced a pass without delivery changes. |
| Credential follow-up package | Same parent `:1425,1932,1968,2012,2015,2036`; nested `0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-af349dd52cae648a5.jsonl:16` | Task10's blank line10 existed before the first final repair. Second final found the old pointer error; first evidence repair also missed one row. |
| Dirty-baseline dispute and checkpoint | `6f744b87-6508-4d3e-9e71-c1193fd2162d.jsonl:188,204,217,234,485-486` | Explicit post-edit HEAD substitution created false extra hunks. Investigation recovered the truthful earlier Git tree; the render task separately lacked its start-HEAD file. |

**Key takeaway:** The strongest controls are unchanged delivery digests and historical-before/after evidence, not the mere sequence of verdicts.

---

## 3. Target State

The target of this operation is a ten-section presentation of the already-debated candidate. It is not a changed product or a newly selected explanation.

- **Desired behavior:** Keep the existing candidate's complete substantive text and place it under the required report chapters.
- **Success criteria:** All 29 original body lines appear once, verbatim and in original order. The support table keeps its header, separator and three data rows with their original citations. The original proposed falsification comparison stays unexecuted. Original pre-debate wording is explicitly scoped to the original input state.
- **Constraints:** No new causal argument, evidence, counterexample, rank, confidence or probability. The original debate inputs and history stay intact. This presentation does not certify current production state or complete an independent quality gate.

Product requirements and implementation success criteria are **N/A**, because this is a causal hypothesis card being restructured for presentation only.

---

## 4. Gap Analysis

A newly written substantive gap analysis is **N/A**. Writing one would extend the original candidate instead of preserving its argument. The original card's own gaps and stale-documentation assessment are kept in Section 9.

| Gap | Current State | Target State | Severity | Notes |
|-----|---------------|--------------|----------|-------|
| Presentation structure only | The preserved debated input uses its original research-card headings. | The same substantive bodies appear under the ten required report chapters. | N/A: no new defect-severity assessment | This is a formatting difference, not an additional causal finding, unwired capability or production defect. The heading-to-chapter map is in Section 10.2. |

This chapter creates no remediation task, product-scope decision or new historical interpretation.

---

## 5. External Research Findings

**N/A for this format-only causal card.** The original candidate contains no external research findings to move. Adding external sources, relevance ratings or advice would bring in material from outside the preserved argument.

No external lookup or publication was done for this presentation. This N/A entry does not replace or revise the wider investigation's external-research component.

---

## 6. Options Analysis

Implementation options, effort estimates, implementation-risk ratings, code-reuse assessments and a new options-comparison table are **N/A**. This document presents one existing causal candidate. It is not a product implementation decision or a new comparison among the five candidates. The original opposing evidence, scope and competing explanations follow unchanged.

### Counterevidence

The initial final-review evidence rejection was valid under its loaded rule; proof repair was real required work, not necessarily reviewer error. The follow-up also had a genuine literal lint-condition failure, so evidence weakness alone is incomplete.
The third final pass followed both pointer corrections and a changed rubric. Current `src/superclaude/skills/sc-implement-protocol/refs/qa.md:82` already says a moved line alone is never issues; these historical failures cannot prove that rule is still absent.
**Key takeaway:** This candidate explains historical avoidable repeats, not permission to ignore unsupported evidence or present policy as unchanged.

### Scope and Overlap

Direct support is concentrated in two selected sessions and three package/task contexts, not independent random samples. It overlaps changed review policy, incomplete first-pass checking and execution-record discipline.
The missing checkpoint contributes a halt mechanism, not proof that it caused either initial rendering failure or an actual repository movement.

### Competing Explanations

A strict evidence contract may intentionally demand durable proof even for correct delivery. Different review focus explains late detection of an old blank pointer; why the first final reviewer missed it is unknown. Changed policy partly explains the last verdict and prevents isolating the effect of pointer fixes.

---

## 7. Recommendation

**Presentation-only recommendation:** Keep this candidate's existing identity and stated evidentiary limits. This card makes no new ranking recommendation and does not amend the completed debate's conclusions, scoring or merge.

### Provisional Evidence Strength and Limits

Strong within the named historical evidence failures: actual ledger writes, nested tool output, unchanged delivery digests and independently recovered Git trees support the mechanisms. Breadth is limited; digests exclude evidence artifacts and policy. No fleet-wide frequency, numerical probability or new-versus-old-version effect follows.

### Original Summary, Quoted as Historical Input State

The paragraph below is quoted verbatim from the original input. Its final sentence records that input's state **before the debate**. It is **not** a current claim that the actual adversarial debate is still pending, and it does not assign or deny any rank.

Brittle proof handoffs explain repeat rejections without new delivery defects in the named cases. Correct baselines, durable proof and meaningful citation checks address different mechanisms and must not be conflated. The historical rubric change limits attribution of the final pass. This remains an unranked candidate for the requested debate.

---

## 8. Implementation Plan

**UNEXECUTED. No execution authority is granted.** A production implementation plan, migration plan, rollback procedure and integration checklist are **N/A** for this format-only causal card. The complete original proposed falsification comparison is kept below. It has not been executed, extended or authorized.

### Falsification Test (UNEXECUTED)

For each evidence-only repeat, reconstruct the true pre-task state, retain the original proof and check every cited range under a fixed rubric. The candidate weakens if repeated failures persist despite complete valid proof, correct baseline and unchanged delivered requirements, or if the supposed proof-only interval contains a necessary delivery correction.
This comparison is proposed, not executed here; it must not waive semantic support just because a cited line exists.

---

## 9. Open Questions

The original gap and staleness bodies are kept below. No new question, resolution claim or causal explanation is added.

### Gaps and Questions

The actor changing the rubric and the exact reason the first audit missed the blank pointer remain unknown. A fresh Read of the formerly archived `TASK-WF-issue358FollowUp-20261022-193837/artifacts/t10-markdownlint.log` under the recorded Coder worktree returned file does not exist. The original nested transcript still preserves that log body; this card does not claim the archived file survives now.

### Stale Documentation Found

Historical pointers include an unrelated README separator, blank log line and a later-task line shift. The current managed FINAL rule already distinguishes moved pointers from unmet end-state criteria. Preserved old and new rule text is in [historical rule evidence](../research/historical-review-rules.json); current matching source copies do not erase that historical change.

---

## 10. Evidence Trail

### 10.1 Preserved Original Input Identity

| Item | Exact identity or handling |
|---|---|
| Intended canonical presentation path | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/hypothesis-04.md` |
| Immutable actual debated source | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/variant-4-original.md` |
| Actual debated source SHA-256 | `fe15dc657c4e6ee11e9d60ce655d2b61d364e5c6055e090abd58e87395f36117`, 6,790 bytes, measured in this pass |
| Original invocation manifest | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/input-manifest.json` |
| Manifest's fourth-input record | The original canonical path `synthesis/hypothesis-04.md`, the source SHA-256 above, and 6,790 bytes. These describe the original invocation, not future formatted canonical bytes. |
| Observed manifest SHA-256 | `ecfa519d0ea0d95558ad53d38112c272ec75b0d5e5a0e096606e3dd46b6b72fc`, measured in this pass |
| Pre-persistence byte check | During this pass, the existing canonical `synthesis/hypothesis-04.md` and the preserved variant both returned the original source SHA-256 above. |
| Merge-base role | The assignment states that this original was the selected writing base of the merge. This pass did not re-read the base-selection artifact. It records the role as reported, without verifying it again, and does not alter it. |
| Expected presentation identity | Persisting this report changes the canonical bytes and therefore its hash. That is an expected presentation change, not a newly written hypothesis argument. This text-only return claims no formatted-canonical hash. |
| Future original-source guards | Bind the original-input hash to the immutable preserved variant `variant-4-original.md`. Do not require the formatted canonical bytes to equal the old input hash, and do not rewrite the old manifest to make that comparison pass. |
| Immutable history | No preserved variant, manifest, debate, scoring, merge, other candidate card or historical artifact was modified. No prior QA verdict, debate endorsement or broader synthesis inventory was updated. |

The original title was `# Hypothesis: Brittle evidence and provenance handoffs`. The original header metadata below is kept verbatim as a quotation of the **historical original-input state**. It is not the current presentation's status, rank or governing format. In particular, its two "pending" entries describe the input before the actual debate ran.

```markdown
**Investigation type:** Evidence-backed candidate cause
**Date:** 2026-10-23
**Status:** Complete candidate card; debate and independent validation pending
**Scope:** Evidence-only failures and incorrect change attribution in selected sessions01/15
**Template:** tech-research/SKILL.md, Codebase Research Agent Prompt, adapted as hypothesis card
**Rank:** Unassigned; actual adversarial debate pending
**Counting unit:** Incident-level evidence; repeated reviewer messages are not independent cases.
```

### 10.2 Original-Heading to New-Chapter Preservation Map

Original line numbers in this table refer only to the immutable debated source, not to the formatted presentation.

| Original heading | Original body lines | New chapter and subsection | Body units retained verbatim | Line count | Required occurrences |
|---|---:|---|---|---:|---:|
| Hypothesis | 12-14 | 1, Original Hypothesis | Two paragraph lines; one key-takeaway line | 3 | 1 each |
| Exact Mechanism | 17-21 | 2, Exact Mechanism | Four bullets; one key-takeaway line | 5 | 1 each |
| Supporting Incidents | 24-26, 28-32, 34 | 2, Supporting Incidents | Three introductory lines; table header, separator and three data rows with original citations; one key-takeaway line | 9 | 1 each |
| Counterevidence | 37-39 | 6, Counterevidence | Two paragraph lines; one key-takeaway line | 3 | 1 each |
| Scope and Overlap | 42-43 | 6, Scope and Overlap | Two paragraph lines | 2 | 1 each |
| Competing Explanations | 46 | 6, Competing Explanations | One paragraph line | 1 | 1 |
| Falsification Test | 49-50 | 8, Falsification Test (UNEXECUTED) | Two paragraph lines | 2 | 1 each |
| Provisional Evidence Strength and Limits | 53 | 7, Provisional Evidence Strength and Limits | One paragraph line | 1 | 1 |
| Gaps and Questions | 56 | 9, Gaps and Questions | One paragraph line | 1 | 1 |
| Stale Documentation Found | 59 | 9, Stale Documentation Found | One paragraph line | 1 | 1 |
| Summary | 62 | 7, Original Summary, Quoted as Historical Input State | One paragraph line; its pre-debate final sentence explicitly scoped as historical | 1 | 1 |
| Header metadata (not a section) | 3-9 | 10.1, quoted block | Seven metadata lines, quoted as historical input state | 7 | 1 each |

**Preservation inventory:** The source has 48 non-blank lines: 12 headings (the title plus 11 section headings) and 36 non-heading lines. Those 36 are 29 body lines across eleven original sections, mapped to chapters 1, 2, 6, 7, 8 and 9, plus 7 header metadata lines quoted once in 10.1. The title is kept as a quoted identity in 10.1, and only its heading level and wording changed in the new report title. These are the intended exact-preservation counts for the parent's check. They are not an independent QA verdict or a machine-verified comparison against a persisted formatted file.

### 10.3 Sources Actually Read for This Presentation

All package-local paths in the table resolve beneath:

`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`

| File | Role in this operation | Read and authorship boundary |
|---|---|---|
| `/config/.claude/skills/tech-research/SKILL.md` | Governing Report Structure | The actual ten-section Report Structure (lines 1311-1487) was read before this presentation was written. |
| `TASK-RESEARCH-review-loops-20261023-032537.md` | Actual fourth-hypothesis assignment | Step 5.9 and surrounding Phase 5 steps were read. No task-state changes were made. |
| `research/research-notes.md` | Six-case assignment map | Read in full. Used to identify the assigned case reports, not as a substitute for reading them. |
| `research/01-session-ac2cd1fd.md` | Orca planning case | Read in full, including the original-repair supplement and identifiers. |
| `research/02-session-a9b88895.md` | Oracle case | Read in full, including the traceability supplement. |
| `research/03-session-6f744b87.md` | Rendering and baseline case | Read in full, including the current-evidence-location mapping. |
| `research/04-session-43582de1.md` | CI planning case | Read in full, including the separately timed outcome and reviewer dispositions. |
| `research/05-session-e002bed2.md` | Monitor case | Read in full, including the continuation and reviewer-identity mapping. |
| `research/06-session-0690ee9f.md` | Credential final-review case | Read in full, including the rubric-change section and the eight-observation disposition. |
| `research/evidence-deck.md` | Cross-case evidence assembly | Read in full, all 901 lines in two pages. Treated as an assembly with its recorded provenance, not as new primary investigation. |
| `research/scope-rules.md` | Current versus historical rule map | Read in full. Current rule text was not treated as proof of historical execution. |
| `research/scope-01.md` | Screening indexes 01-06 | Read in full. |
| `research/scope-02.md` | Screening indexes 07-12 and controls | Read in full. |
| `research/scope-03.md` | Screening indexes 13-18 and controls | Read in full. |
| `research/scope-04.md` | Screening indexes 19-24 | Read in full. |
| `research/scope-05.md` | Screening indexes 25-30 | Read in full. |
| `gaps-and-questions.md` | Existing uncertainty and temporal limits | Read in full. No gap was silently resolved or added to the candidate. |
| `synthesis/hypothesis-01.md` | Presentation pattern only | Read in full. Its structure was followed and none of its content was imported. |
| `synthesis/hypothesis-04.md` | Existing canonical fourth candidate | Read in full. It has the same hash as the preserved variant and was unchanged during this pass. |
| `reviews/adversarial/adversarial/variant-1-original.md` | Immutable card 01, read for distinctness | Read in full. No content was imported, and no new comparative argument was written. |
| `reviews/adversarial/adversarial/variant-2-original.md` | Immutable card 02, read for distinctness | Read in full instead of the canonical file, which may be mid-format. No content was imported. |
| `reviews/adversarial/adversarial/variant-3-original.md` | Immutable card 03, read for distinctness | Read in full instead of the canonical file, which may be mid-format. No content was imported. |
| `reviews/adversarial/adversarial/variant-4-original.md` | Preserved actual debated argument | Read in full. It is the only verbatim source for every body line above. |
| `reviews/adversarial/input-manifest.json` | Original invocation paths and hashes | Read in full. Its fourth input matches the hash and byte count in 10.1. |

**Read inventory:** Six of six case reports, five of five screening summaries, the complete evidence deck, the rule map, the gap log, the four immutable variants and the manifest were read. Twenty-four distinct files are listed above. No primary historical transcript, product source, test or external source was newly investigated for this formatting operation. Read-only commands measured hashes, byte counts and line counts. The distinctness reading confirmed only that this presentation keeps candidate four's own identity. The original card's existing overlap statements are the only overlap claims carried forward.

### 10.4 Boundaries and Handoff State

The additional readings informed how the original argument is handled. They gave no authority to rewrite it. Original primary citations are carried forward as historical recorded anchors. No claim is made that every historical target is still available at its old path. The original card already records one such absence itself.

This operation returns a presentation of candidate four only. It does not create, replace or revise any other candidate. No new cause was selected and no research was redone. No adversarial rerun, independent review, test execution, production action, Git action, staging, archive, move, deletion or external publication occurred. No material causal change was needed, so no blocker was raised.

| Status | Result |
|---|---|
| DONE | Returned the requested ten-section, format-only presentation. All 29 original body lines are kept verbatim once, and the 7 header metadata lines are quoted once as historical input state. |
| DONE | Read every assigned case report, the full evidence deck, all five screening summaries, the rule map, the gap log, the canonical card, all four immutable variants and the actual manifest, and measured the source and manifest hashes. |
| NEXT | The parent checks exact line preservation and preserved-source immutability, then persists this text at `synthesis/hypothesis-04.md`. This return alone does not complete an independent quality gate or authorize Step 5.9 to be checked. |

### 10.5 Parent Persistence Record (2026-10-24)

The parent persisted this exact restricted return from current session subagents/agent-aformat-hypothesis-04-edaa13f994c6198b.jsonl. Before writing, a mechanical check against the immutable debated source found all 29 non-heading body lines present exactly once and none missing, ten numbered chapters and no active placeholders. Saved body before this record: 23,307 UTF-8 bytes, SHA-256 `3069f94f43528a65fa110e6887e3311030477d4eb31b7f36938bf45288d4238b`; the preserved variant remained `fe15dc657c4e6ee11e9d60ce655d2b61d364e5c6055e090abd58e87395f36117`. The merge-base role noted in 10.1 matches the recovered return contract, which names `variant-4-original` as the writing base; that is document-quality selection, not likelihood. The worker's "parent persistence still required" wording is its original handoff state, resolved here. This record is not an independent synthesis-gate verdict.

**Amendment receipt (2026-10-24, synthesis-gate fix cycle 2):** This receipt is appended below the original record above, which is not edited. At Task Step 5.24 (synthesis-gate fix cycle 1, finding P5-28) one presentation note, marked as added after the debate and not part of the debated text, was inserted in chapter 1 between `## 1. Problem Statement` and `### Original Hypothesis` (`qa/qa-synthesis-fix-log.md`, P5-28). That insertion added 439 UTF-8 bytes, so the saved-body figures in the record above (23,307 bytes, SHA-256 `3069f94f…`) describe the body before Task Step 5.24. Measured the same way (every byte before the `### 10.5` heading except the two newline characters that precede it), the body now measures 23,746 UTF-8 bytes, SHA-256 `39509e9b38f8bc42935509b7aac8fc5bff4cdbfe200cfe86f742b8dc29f3c179`. A re-run exact-once check against the immutable `reviews/adversarial/adversarial/variant-4-original.md` (SHA-256 `fe15dc657c4e6ee11e9d60ce655d2b61d364e5c6055e090abd58e87395f36117`, unchanged) found each of its 35 distinct non-blank, non-heading lines other than the table separator exactly once in this card. The generic table separator line appears 1 time in the variant and 2 times in this card, both before and after Task Step 5.24; it is markdown syntax, not identity text. This receipt states or implies no synthesis-gate verdict.
