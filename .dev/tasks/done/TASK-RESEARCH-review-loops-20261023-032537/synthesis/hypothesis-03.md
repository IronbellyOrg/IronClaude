# Technical Research Report: Review Contracts Change During the Loop

**Date:** 2026-10-24  
**Depth:** Deep, inherited investigation scope; this operation is format-only  
**Research files read:** Six case reports, five screening summaries, one evidence deck, one rule map, the research notes and the gap log; supporting inputs are inventoried in Section 10  
**Scope:** Presentation of the existing third causal candidate, without changing its argument, evidence, limits or identity  
**Presentation status:** Post-debate format-only presentation. The actual debated source is the immutable `variant-3-original.md` identified in Section 10 at its recorded SHA-256.  
**Authorship and delivery:** Format-only synthesis worker, returned as text because report-file writes are prohibited for this worker. No file was created or modified, including no on-disk skeleton. Parent persistence and independent preservation checking remain required.

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

Review does not always preserve one operative contract across stages or attempts. Literal criteria are softened, useful hardening is treated as required compliance, conflicting source instructions are unresolved, or installed policy changes mid-run. This can create reversals and additional reviews even when delivery files do not change.

---

## 2. Current State Analysis

This chapter preserves the original candidate's historical mechanism and support. "Current State Analysis" is the required report heading. It does not claim that historical review rules, plans or implementation files were freshly inspected during this presentation pass.

### Exact Mechanism

1. The written requirement, the early review's interpretation and the later review's rule are not equivalent.
2. A local pass or claimed fix is judged under one interpretation, then a fresh reviewer applies another or a newly loaded policy.
3. The next verdict may reflect a real original violation, added checking scope, policy migration or a mixture, rather than new implementation damage.
4. Without recording the exact original criterion and loaded rules, evidence correction and changed acceptance are indistinguishable in the outcome.

### Supporting Incidents and Primary Evidence

**Counting:** Contract mechanisms in one run are not additional independent sessions or reviews.

Each row identifies a distinct contract mechanism; none establishes that all later findings were invented.

| Mechanism | Observed consequence | Research and primary anchors |
|---|---|---|
| Task QA relaxes a literal lint criterion | Task6 accepts unchanged preexisting lint findings as no-new-findings despite a no-finding-on-changed-line clause. FINAL applies the original clause; owner acceptance is obtained only later. | [Credential finals](../research/06-session-0690ee9f.md), section4; `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866.jsonl:1215,1230,1935,1938`; nested Task6 reviewer `agent-a6d8fbaf69a56dd14.jsonl:61` under that session. |
| FINAL rubric changes between reviewers | Old rule treats stale evidence as issues; later rule says moved line alone is not issues and changes acceptance handling. Final pass follows both evidence fixes and policy change. Their separate effects cannot be isolated. | [Credential finals](../research/06-session-0690ee9f.md), section5; exact captured texts in [historical-review-rules.json](../research/historical-review-rules.json). Original nested `agent-acf0a51e6992c50ee.jsonl:18` at20:26:30.085Z and `agent-a4bfff371c63a6c39.jsonl:18` at20:32:19.277Z, both beneath the credential session above. |
| Implementation migration adds a fresh review | Original reviewer returns compliant, but updated resume rules require a new operator review before completion. That review finds real earlier omissions. | [Monitor case](../research/05-session-e002bed2.md), section5.4; `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/e002bed2-7877-42c1-8665-8cb8595587b6.jsonl:42,58,849,874,893,902`. No adviser/revert ladder executed for this task. |
| Broader risk checking enters compliance review | Some monitor findings concern uncapped fields explicitly absent from the plan or case-insensitive matching not clearly required. Later user-authorized fixes do not make these retroactively original criteria. | [Monitor case](../research/05-session-e002bed2.md), sections4-5; same monitor log `:906`, `:1143`; per-review prompts require any defect of any severity to be noncompliant. |
| Source and review scope disagree | Orca prose and diagram conflict on up-to-date state and repository-check timing. CI boundary-file comparison is initially called an incomplete original repair, then conceded optional because the original finding names different files. | [Orca planning](../research/01-session-ac2cd1fd.md), section6, source `:142,285,382,402`; [CI planning](../research/04-session-43582de1.md), section6.3 and eight-entry addendum, regenerated debate `adversarial/round2-v1.md` under the exact review directory in that case. |

---

## 3. Target State

The target of this operation is a ten-section presentation of the already-debated candidate. It is not a changed product, a changed review rule or a newly selected explanation.

- **Desired behavior:** Preserve the existing candidate's complete substantive text while placing it under the required report chapters.
- **Success criteria:** Every original body section appears once, verbatim. The support table keeps its five data rows and citations. The original proposed test stays unexecuted. The original pre-debate wording is explicitly scoped to its original input state.
- **Constraints:** No new causal argument, counterexample, ranking, probability or change in evidentiary support. The original debate inputs and history are preserved. This presentation does not certify current production state, current installed rules or completion of an independent quality gate.

Product requirements and implementation success criteria are **N/A** because this is a causal hypothesis card being restructured for presentation only.

---

## 4. Gap Analysis

A newly written substantive gap analysis is **N/A**. Writing one would extend the original candidate rather than preserve its argument. The original research gaps and stale-documentation assessment are kept in Section 9.

| Gap | Current State | Target State | Severity | Notes |
|-----|---------------|--------------|----------|-------|
| Presentation structure only | The preserved debated input uses its original research-card headings. | The same substantive bodies appear under the ten required report chapters. | N/A: no new defect-severity assessment | This is a formatting difference, not an additional causal finding, unwired capability or production defect. The old-to-new mapping is in Section 10. |

This chapter creates no remediation task, product-scope decision or new historical interpretation.

---

## 5. External Research Findings

**N/A for this format-only causal card.** The original candidate contains no external-research findings to relocate. Adding external sources, relevance ratings or advice would introduce material outside the preserved argument.

No external lookup or publication was performed for this presentation. This N/A entry does not replace or revise the wider investigation's external-research component.

---

## 6. Options Analysis

Implementation options, effort estimates, implementation-risk ratings, code-reuse assessments and a new options-comparison table are **N/A**. This document presents one existing causal candidate. It is not a product implementation decision or a new comparison among the five candidates. The original opposing evidence and competing explanations follow unchanged.

### Counterevidence

- Oracle review retains exactly the original default-path requirement; no moving criterion explains its second failure. The limitation is frozen repair authority ([oracle case](../research/02-session-a9b88895.md), sections4/6).
- The manual-page reviewer twice requests the same real rendering proof. Static checks do not satisfy that unchanged criterion; acceptance is not repaired rendering ([documentation case](../research/03-session-6f744b87.md), sections2-4).
- The fresh monitor review finds genuine defects present before the policy change. Migration adds a review, but does not make those findings invalid or cause their original code.

### Scope, Overlap and Competing Explanations

This is a family of contract-consistency failures, not a claim that all reviewers invent requirements. Keep original source contradictions, unauthorized interpretation changes, justified operator decisions and live policy migrations individually attributed.
Weak checks and repair-induced defects remain competing explanations for the artifact's actual state. Contract instability primarily explains reversals, disagreement, extra review entry, and difficulty attributing final convergence. It is a proven amplifier in two runs, not a universal source of defects.

---

## 7. Recommendation

**Presentation-only recommendation:** Keep this candidate's existing identity and stated evidentiary limits. This card makes no new ranking recommendation and does not amend the completed debate's conclusions or endorsements.

### Provisional Evidence Strength and Limits

Direct captured tool results prove two rubric versions in the credential run; monitor records prove migration reopened a compliant check. Literal lint relaxation and later reapplication are also explicit.
Which actor changed the installed rubric, and whether policy change alone would pass the unrepaired package, remain unknown. Broader hardening findings vary in validity; do not combine them into a count of fabricated defects.

### Key Takeaways

- Record both the original acceptance contract and the exact review policy actually loaded; current installed rules cannot establish historical execution.
- A changed verdict can follow valid evidence repairs and changed rules together. That is not a controlled demonstration of repair effectiveness.

### Original Summary, Quoted as Historical Input State

The paragraph below is quoted verbatim from the original input. Its final sentence records that input's pre-debate state. It is **not** a current claim that the actual debate remains unfinished or still has to be held.

The sample contains genuine contract inconsistency and mid-run policy changes that explain extra reviews or reversals. These mechanisms amplify other defects but do not make every later finding invalid. Their relative importance must be debated alongside the stable-contract cases and independently traced implementation defects.

---

## 8. Implementation Plan

**UNEXECUTED. No execution authority is granted.** A production implementation plan, migration plan, rollback procedure and integration checklist are **N/A** for this format-only causal card. The complete original proposed discriminating test is kept below. It was not executed, extended or scheduled by this presentation, and it authorizes no historical replay, reviewer dispatch or rule change.

### Discriminating Test

Preserve original requirement text, accepted exceptions, exact loaded rubric bytes and artifact state for every reviewed attempt.
- Have independent reviewers adjudicate each disputed finding twice: once under the original fixed contract, once under the actually changed contract.
- Classify differences as original violation, authorized acceptance, explicitly added hardening, unresolved contradiction, or rule-version effect.
- If identical policy/criteria and artifact state still yield the same substantive failures, contract change does not explain those failures. If a verdict or required fresh review changes solely with the contract, the mechanism gains support.
No historical replay was run for this card. The experiment must not waive valid findings or treat an operator's accepted gap as compliant work.

---

## 9. Open Questions

The original gap and staleness bodies are kept below. No new question, resolution claim or causal explanation is added.

### Gaps and Questions

The effects of policy changes and evidence corrections are confounded in the credential final pass. Stable-criterion oracle/render failures remain counterexamples. No evidence establishes that all broad review demands were invalid, or that minimum reviewer counts caused the instability.

### Stale Documentation Found

The same installed rubric path returned materially different contents to consecutive reviewers. [Captured historical rule evidence](../research/historical-review-rules.json) preserves both versions; [current-rule map](../research/scope-rules.md) is explicitly not substituted for them. Source contradictions are disclosed rather than silently resolved.

---

## 10. Evidence Trail

### 10.1 Preserved Original Input Identity

| Item | Exact identity or handling |
|---|---|
| Intended canonical presentation path | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/hypothesis-03.md` |
| Immutable actual debated source | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/variant-3-original.md` |
| Actual debated source SHA-256 | `f20f7fd37114f1c3d529bd7eca97b2af748fe9c5b3c73559b78837a7dfb5a8e3` |
| Actual debated source size | 8,169 bytes, 62 physical lines |
| Original invocation manifest | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/input-manifest.json` |
| Manifest's third-input record | Original canonical path `synthesis/hypothesis-03.md`, the source SHA-256 above, and 8,169 bytes. These describe the original invocation, not future formatted canonical bytes. |
| Observed manifest SHA-256 | `ecfa519d0ea0d95558ad53d38112c272ec75b0d5e5a0e096606e3dd46b6b72fc` |
| Pre-persistence byte check | During this pass, the existing canonical file and the preserved variant both returned the original source SHA-256 above and the same 8,169-byte, 62-line size. |
| Expected presentation identity | Persisting this report changes the canonical bytes and therefore its hash. That is an expected presentation change, not a newly written hypothesis argument. No formatted-canonical hash is claimed in this text-only return. |
| Future original-source guards | Bind the original-input hash to the immutable preserved variant, `f20f7fd37114f1c3d529bd7eca97b2af748fe9c5b3c73559b78837a7dfb5a8e3`. Do not require the formatted canonical bytes to equal the old input hash. Do not rewrite the old manifest to make that comparison pass. |
| Immutable history | No preserved variant, manifest, debate, scoring, merge or historical artifact was modified. No prior QA verdict, debate endorsement, other candidate card or broader synthesis inventory was updated. |

The original title was `# Research: Review Contracts Change During the Loop`. The original header metadata below is kept verbatim as a quotation of the **historical original-input state**. It is not the current presentation's status or governing format. Its "hypothesis for debate" and "not a final rank" wording describes that pre-debate input only.

```markdown
**Investigation type:** Evidence-backed causal hypothesis
**Scope:** Six selected historical sessions; candidate three, not a final rank
**Status:** Complete, hypothesis for debate; not ranked or independently approved
**Date:** 2026-10-23
**Governing template:** tech-research/SKILL.md, Codebase Research Agent Prompt
```

### 10.2 Original-Heading to New-Chapter Preservation Map

Original line ranges in this table refer only to the immutable debated source, not the formatted presentation. "Non-heading lines" counts every original paragraph, list item and table line (including the table's header and separator rows) in that section.

| Original heading | Original body lines | New chapter and subsection | Body units retained verbatim | Non-heading lines | Required occurrence count per line |
|---|---:|---|---|---:|---:|
| Hypothesis | 10 | 1, Original Hypothesis | One paragraph | 1 | 1 |
| Exact Mechanism | 13-16 | 2, Exact Mechanism | Four numbered items | 4 | 1 |
| Supporting Incidents and Primary Evidence | 19-29 | 2, Supporting Incidents and Primary Evidence | Counting paragraph; row-scope paragraph; complete table with header, separator and five data rows with original citations | 9 | 1 |
| Counterevidence | 32-34 | 6, Counterevidence | Three bullets | 3 | 1 |
| Scope, Overlap and Competing Explanations | 37-38 | 6, Scope, Overlap and Competing Explanations | Two original text lines, unchanged and next to each other | 2 | 1 |
| Discriminating Test | 41-45 | 8, Discriminating Test | Opening line; three bullets; closing line | 5 | 1 |
| Provisional Evidence Strength and Limits | 48-49 | 7, Provisional Evidence Strength and Limits | Two original text lines, unchanged and next to each other | 2 | 1 |
| Key Takeaways | 52-53 | 7, Key Takeaways | Two bullets | 2 | 1 |
| Gaps and Questions | 56 | 9, Gaps and Questions | One paragraph | 1 | 1 |
| Stale Documentation Found | 59 | 9, Stale Documentation Found | One paragraph | 1 | 1 |
| Summary | 62 | 7, Original Summary, Quoted as Historical Input State | One paragraph, with its original pre-debate final sentence explicitly scoped as historical | 1 | 1 |
| Header metadata (not a body section) | 3-7 | 10.1, quoted block | Five metadata lines, quoted as historical input state | 5 | 1 |

**Preservation inventory:** Eleven original substantive body sections, totalling 31 non-heading body lines, are mapped to ten required report chapters. All four mechanism items, all five supporting table data rows, three counterevidence bullets, three test bullets and two takeaway bullets are kept. The five original header-metadata lines are quoted once separately, so 36 original non-heading lines in total should each appear exactly once. The original title line (line 1) and section headings are the only original lines replaced. These are the intended exact-preservation counts for parent checking. They are not an independent QA verdict or a machine-verified comparison against a persisted formatted file.

**Historical-state wording requiring framing:** Two original passages carry pre-debate wording. The Summary's final sentence and the header's "Status" and "Scope" lines are each framed above as historical original-input state. No other original line states that debate is pending.

### 10.3 Sources Actually Read for This Presentation

All package-local paths in the table resolve beneath:

`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`

| File | Role in this operation | Read and authorship boundary |
|---|---|---|
| `/config/.claude/skills/tech-research/SKILL.md` | Governing Report Structure | Read lines 1311-1510, covering the full ten-section Report Structure, before composing this presentation. |
| `TASK-RESEARCH-review-loops-20261023-032537.md` | Actual third-hypothesis assignment | Read lines 270-319, including the actual Step 5.8 and the neighbouring Steps 5.6, 5.7 and 5.11 for context. No task-state change made. |
| `research/research-notes.md` | Exact six-case assignment map | Read in full. Used to identify the assigned empirical reports, not as a substitute for reading them. |
| `research/01-session-ac2cd1fd.md` | Orca planning case | Read in full, including the complete original-repair supplement and identifier supplement. The file records main-session persistence of a restricted analyst's return. |
| `research/02-session-a9b88895.md` | Oracle case | Read in full, including the freeze-conflict and identifier sections. The file records main-session persistence of a restricted analyst's return. |
| `research/03-session-6f744b87.md` | Rendering and baseline case | Read in full, including the current-evidence-location mapping. The file records main-session persistence of a restricted analyst's return. |
| `research/04-session-43582de1.md` | CI planning case | Read in full, including the separately timed final outcome, the eight-entry disposition and the retained/withdrawn dispositions. The file records main-session persistence of a restricted analyst's return. |
| `research/05-session-e002bed2.md` | Monitor case | Read in full, including the protocol-migration section, the separately timed continuation and the reviewer identity mapping. The file records main-session persistence of a restricted analyst's return. |
| `research/06-session-0690ee9f.md` | Credential final-review case | Read in full, including the review-policy change section and the eight-observation disposition. The file records main-session persistence of a restricted analyst's return. |
| `research/evidence-deck.md` | Complete cross-case evidence assembly | Read in full, all 901 lines, in four bounded reads. Treated as assembled research with its recorded provenance and limits, not as a new independent primary investigation. |
| `research/scope-rules.md` | Current-versus-historical protocol map | Read in full. Its recovered historical rubric-load mapping was not promoted beyond its stated limits, and current rules were not treated as proof of historical execution. |
| `research/scope-01.md` | Screening indexes 01-06 | Read in full. Screening is selection evidence, not a replacement for the case reports. |
| `research/scope-02.md` | Screening indexes 07-12 and controls | Read in full. Controls and exclusions stay screening qualifications. |
| `research/scope-03.md` | Screening indexes 13-18 and controls | Read in full. The credential package distinctions and the session 17 control stay separate. |
| `research/scope-04.md` | Screening indexes 19-24 | Read in full. Provisional screening counts were not used to rewrite the candidate. |
| `research/scope-05.md` | Screening indexes 25-30 | Read in full. The retained frozen-fixture finding stays distinct from a changed criterion. |
| `gaps-and-questions.md` | Existing uncertainty and temporal limits | Read in full. No gap was silently resolved or added as new causal meaning. |
| `synthesis/hypothesis-01.md` | Presentation pattern only | Read in full. Used only for chapter layout and provenance conventions; none of its substantive content was copied into this card. |
| `synthesis/hypothesis-03.md` | Existing canonical candidate | Read in full and hashed before any contemplated presentation change. Unchanged on disk during this pass. |
| `reviews/adversarial/adversarial/variant-3-original.md` | Preserved actual debated argument | Read in full and hashed. Used as the immutable verbatim source. |
| `reviews/adversarial/adversarial/variant-1-original.md` | First debated candidate, distinctness check | Read in full; SHA-256 `3f39f065ffb13efad680694e9e699fb04456a03a93cabab75be90bee3d2dbac9`, matching its manifest record. Used only to confirm this presentation does not merge or alter candidate identities. |
| `reviews/adversarial/adversarial/variant-2-original.md` | Second debated candidate, distinctness check | Read in full; SHA-256 `e62a753c7b5c9df11d0a57469de1717e115f3166e2596342adf26ad3fa882ebc`, matching its manifest record. The canonical `synthesis/hypothesis-02.md` was deliberately not read because it may be mid-format by another worker. |
| `reviews/adversarial/input-manifest.json` | Original invocation paths and hashes | Read in full and hashed. Not modified. |

**Read inventory:** Six of six case reports, five of five screening summaries and the complete evidence deck were read. Twenty-three distinct source files are listed above. `research/historical-review-rules.json`, which the original card cites, was not reopened for this formatting operation; its citation is carried forward unchanged as a historical recorded anchor. No primary historical log, product source, current installed rule, test or external source was newly investigated.

### 10.4 Boundaries and Handoff State

The additional readings supplied qualifications for handling the original argument, not authority to rewrite it. Original primary citations, including nested reviewer paths and physical JSONL record numbers, are carried forward as historical recorded anchors. No claim is made that every historical target remains available at its old path.

Exactly the existing five candidate identities are preserved. This operation returns a presentation of candidate three only and does not create, replace or revise another candidate. No material causal change was found necessary, so no blocker is reported. No adversarial rerun, independent review, test execution, production action, Git operation, staging, archive, move, deletion or external publication occurred.

| Status | Result |
|---|---|
| DONE | Returned the requested ten-section, format-only presentation with all 31 original body lines and 5 header-metadata lines placed once, and the original pre-debate wording framed as historical input state. |
| DONE | Read every assigned case, the complete evidence deck, all five screening summaries, the rule map, research notes, gap log, the current canonical card, all three named preserved variants and the actual manifest; confirmed the canonical card and variant 3 share SHA-256 `f20f7fd37114f1c3d529bd7eca97b2af748fe9c5b3c73559b78837a7dfb5a8e3`. |
| NEXT | Parent checks exact line preservation against `variant-3-original.md` and the source's unchanged hash before persisting this text at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/hypothesis-03.md`. This return does not complete an independent quality gate or authorize another task item. |

### 10.5 Parent Persistence Record (2026-10-24)

The parent persisted this exact restricted return from current session subagents/agent-aformat-hypothesis-03-98c1aa194ff330cc.jsonl. Before writing, a mechanical check against the immutable debated source found all 31 non-heading body lines present exactly once and none missing, ten numbered chapters and no active placeholders. Saved body before this record: 26,363 UTF-8 bytes, SHA-256 `db587957865a6ab1bc9b71fc0f9d02bae9020dc8941c1957b53034dddc537d58`; the preserved variant remained `f20f7fd37114f1c3d529bd7eca97b2af748fe9c5b3c73559b78837a7dfb5a8e3`. The worker's "parent persistence remains required" wording is its original handoff state, resolved here. This record is not an independent synthesis-gate verdict.

**Amendment receipt (2026-10-24, synthesis-gate fix cycle 2):** This receipt is appended below the original record above, which is not edited. At Task Step 5.24 (synthesis-gate fix cycle 1, finding P5-28) one presentation note, marked as added after the debate and not part of the debated text, was inserted in chapter 1 between `## 1. Problem Statement` and `### Original Hypothesis` (`qa/qa-synthesis-fix-log.md`, P5-28). That insertion added 439 UTF-8 bytes, so the saved-body figures in the record above (26,363 bytes, SHA-256 `db587957…`) describe the body before Task Step 5.24. Measured the same way (every byte before the `### 10.5` heading except the two newline characters that precede it), the body now measures 26,802 UTF-8 bytes, SHA-256 `01026f904e52622266e870b23e126128799b0f9168179f2e0fc19abd801155c7`. A re-run exact-once check against the immutable `reviews/adversarial/adversarial/variant-3-original.md` (SHA-256 `f20f7fd37114f1c3d529bd7eca97b2af748fe9c5b3c73559b78837a7dfb5a8e3`, unchanged) found each of its 35 distinct non-blank, non-heading lines other than the table separator exactly once in this card. The generic table separator line appears 1 time in the variant and 2 times in this card, both before and after Task Step 5.24; it is markdown syntax, not identity text. This receipt states or implies no synthesis-gate verdict.
