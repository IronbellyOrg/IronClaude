# Web Research: Adversarial-Axis Taxonomies + Multi-Stage QA Gate Design Patterns

**Status:** Complete
**Date:** 2026-05-14
**Topic:** External prior art for 5-axis adversarial QA overlay (drift / contradictions / omissions / weakened-criteria / invented-content) and multi-stage QA gate design patterns
**Codebase context:** task-builder skill v3.9 inverse-direction merge from sc-tasklist

---

## 1. Sources surveyed

All URLs accessed 2026-05-14.

### Software-engineering / specification-review prior art

| # | URL | 1-line relevance |
|---|---|---|
| S1 | https://www.cs.toronto.edu/~sme/CSC340F/2005/assignments/inspections/reqts_checklist.pdf | Wiegers' canonical SRS review checklist — categories include Correctness, Completeness, Consistency (maps to contradictions/omissions). |
| S2 | https://ranger.uta.edu/~huber/cse4316/Docs/IEEEStd1233-1998.pdf | IEEE Std 1233-1998 (System Requirements Specification guide) — requires inspections to identify inconsistencies and verify completeness. |
| S3 | http://www.math.uaa.alaska.edu/~afkjm/cs401/IEEE830.pdf | IEEE Std 830-1998 (Software Requirements Specifications recommended practice) — defines Internal Consistency and Completeness as primary SRS qualities. |
| S4 | https://en.wikipedia.org/wiki/Fagan_inspection | Fagan inspection — original defect-categorization process (major vs minor defects) per IBM 1976. |
| S5 | https://www.ida.liu.se/~TDDC90/literature/lab-papers/doolan91.pdf | Doolan 1991 ("Experience with Fagan's Inspection Method") — explicitly catalogues "major omissions on the author's part" as a defect class. |
| S6 | https://thescipub.com/pdf/jcssp.2017.470.495.pdf | Systematic review: "Defect Types and Software Inspection Techniques" — Travassos et al. 2001 taxonomy of SRS defects: **Omission, Incorrect Fact, Inconsistency, Ambiguity, Extraneous Information** (this is the most direct prior-art match — see §3 below). |
| S7 | https://webspace.science.uu.nl/~dalpi001/papers/dalp-scha-luca-18-refsq.pdf | Dalpiaz et al. (REFSQ 2018) — frames RE defects as "ambiguity, unclarity, inconsistency, and incompleteness". |

### Adversarial / red-team / multi-stage-gate prior art

| # | URL | 1-line relevance |
|---|---|---|
| S8 | https://dev.to/druid628/the-case-for-red-teaming-your-design-j0c | "The Case for Red Teaming Your Design" — explicit red-team-of-TDD pattern from defense engineering (Navy N6 walkthroughs). |
| S9 | https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs | Pragmatic Engineer on RFC/Design Doc tiered review processes (Big Tech adoption pattern). |
| S10 | https://briansigafoos.com/design-docs/ | Google-style design-doc template (lists "Alternatives considered" as required section, matching TDD §21). |
| S11 | https://arxiv.org/html/2604.19049v1 | Refute-or-Promote (arXiv 2604.19049) — explicit "Adversarial Stage-Gated Multi-Agent Review" with mandatory empirical gate after adversarial endorsement (directly analogous to FR-CONV.3 inherited-verdict pattern). |
| S12 | https://www.freecodecamp.org/news/how-to-apply-gan-architecture-to-multi-agent-code-generation/ | "GAN architecture for multi-agent code generation" — describes Plan Review → Implementation Review → Final GO/NO-GO 3-stage adversarial topology. |
| S13 | https://www.sonarsource.com/resources/library/quality-gate/ | SonarQube canonical "Quality Gate" definition — pass/fail checkpoint enforcement. |
| S14 | https://www.dynatrace.com/news/blog/what-are-quality-gates-how-to-use-quality-gates-with-dynatrace/ | Dynatrace "Quality Gates" — fail-closed enforcement ("if even one of the key metrics receives a failing score…the software cannot progress further"). |
| S15 | https://www.perforce.com/blog/sca/what-quality-gates | Perforce quality-gate definition — "blocks substandard code from deployment". |
| S16 | https://www.stage-gate.com/blog/the-stage-gate-model-an-overview/ | Cooper's Stage-Gate® model (multi-stage gating for innovation processes — origin of the term). |

### LLM-hallucination / faithfulness prior art (for invented-content axis)

| # | URL | 1-line relevance |
|---|---|---|
| S17 | https://dl.acm.org/doi/10.1145/3703155 | ACM Computing Surveys: "A Survey on Hallucination in LLMs" — taxonomy: factuality vs faithfulness; faithfulness subdivided into instruction-inconsistency, context-inconsistency, logical-inconsistency. |
| S18 | https://arxiv.org/html/2510.06265v2 | "Large Language Models Hallucination: A Comprehensive Survey" — "Faithfulness hallucination occurs when the generated output **drifts** from the original input or context". |
| S19 | https://layerlens.ai/blog/llm-hallucination-detection-in-production | LayerLens production-LLM taxonomy: Fabrication, Misattribution, **Citation Drift**, Speculative Completion (close conceptual match to invented-content + drift axes). |
| S20 | https://agility-at-scale.com/ai/architecture/hallucination-detection-and-context-lineage/ | Intrinsic vs extrinsic hallucination distinction — intrinsic = "contradicts your own organizational data" (≈ contradictions axis). |
| S21 | https://www.bugraptors.com/blog/llm-output-evaluation-hallucination-detection | LLM-output evaluation: lists "tangential hallucinations" / drift, internal contradictions, fabrication — exact 3 of our 5 axes. |
| S22 | https://arxiv.org/html/2510.22944v2 | "Is Your Prompt Poisoning Code?" — quality-level rubric for prompts as spec: "L1 preserves full coverage and clarity while allowing a small number of well-scoped omissions. L2 is defined by multiple ambiguities and evident **under-specification with mild requirement creep**" (close cognate to weakened-criteria). |

---

## 2. Key external findings

### Finding A — Travassos et al. 2001 SRS-defect taxonomy is the most direct prior art (HIGH relevance)

**Source:** Travassos et al. 2001 taxonomy, summarized in the systematic review at S6.

**Verbatim quote:** "The Travassos et al. (2001) taxonomy of defect types was adopted: **Omission, Ambiguity, Incorrect Fact, Inconsistency and Extraneous Information**."

**Mapping to task-builder 5-axis:**

| Travassos 2001 | task-builder 5-axis | Match strength |
|---|---|---|
| Omission | omissions | **Exact** |
| Inconsistency | contradictions | **Exact (semantic)** |
| Incorrect Fact | invented-content (partial) | Partial — invented-content also covers fabricated references with no source. |
| Extraneous Information | invented-content (partial) | Partial — "extraneous" overlaps with content the BUILD_REQUEST never asked for. |
| Ambiguity | — (not directly mapped) | task-builder doesn't have a dedicated ambiguity axis. |
| — (no Travassos counterpart) | drift | task-builder-specific (closer to LLM-faithfulness drift). |
| — (no Travassos counterpart) | weakened-criteria | Newer concept tied to acceptance-criteria erosion / scope creep. |

**Relevance to our codebase:** The {omissions, contradictions} pair is **canonical 1976-onward SE practice** going back to Fagan inspections and IEEE 830/1233. We are not inventing this — we are re-applying a 30+ year tradition. {drift, invented-content} are newer (LLM-era) but well-supported by the 2023-2025 hallucination-detection literature. {weakened-criteria} is the most novel axis and is most clearly grounded in agile/PM scope-creep literature (see Finding D).

### Finding B — Multi-stage adversarial gating with fail-closed semantics is established practice (HIGH relevance)

**Source S11 (Refute-or-Promote, arXiv 2604.19049):** "The most instructive failure: ten dedicated reviewers unanimously endorsed a non-existent Bleichenbacher padding oracle in OpenSSL's CMS module; it was killed only by a single empirical test, motivating the **mandatory empirical gate**."

**Source S14 (Dynatrace):** "If even one of the key metrics receives a failing score…the software cannot progress further. Adjustments must be made accordingly." — verbatim "fail-closed" semantics matching FR-CONV.* gates.

**Source S12 (GAN-architecture multi-agent):** Three-stage adversarial loop: "Planning (Planner and Plan Reviewer in a GAN loop, max 3 iterations), Implementation (Implementer and Reviewer in a GAN loop, max 3 iterations), and Final Review (GO or NO-GO gate)" — directly analogous to our research-gate → synthesis-gate → report-validation → task-integrity 4-stage topology.

**Relevance to our codebase:** Our 4-stage gate topology (research → synthesis → report-validation → task-integrity) is a **direct instance** of recognized engineering practice. The "fail-closed = any gap = FAIL" semantic is verbatim from Dynatrace's quality-gate definition.

### Finding C — LLM-faithfulness literature establishes "drift" and "invented-content" as axes (HIGH relevance)

**Source S17 (ACM CSUR Survey on LLM Hallucination):** Categorizes faithfulness hallucinations into "instruction inconsistency, where the content **deviates** from the user's original instruction; context inconsistency, highlighting discrepancies from the provided context; and logical inconsistency."

**Source S18 (arXiv 2510.06265):** "Faithfulness hallucination occurs when the generated output **drifts from the original input or context**, violating the user's instructions or violating the logical consistency within the response."

**Source S19 (LayerLens):** Names "**Citation Drift**: Common in retrieval systems. The answer is grounded in retrieved material, but the cited sentence does not support the claim." and "Fabrication: The model generates content not grounded in training distribution or provided context" — matching task-builder's invented-content axis.

**Relevance to our codebase:** "drift" is established LLM-era terminology with formal definition matching task-builder usage (deviation from GOAL/instruction). "invented-content" maps to Fabrication / non-grounded content in production-LLM evaluation tooling.

### Finding D — "Weakened criteria" maps to PM/agile "acceptance-criteria erosion" + "scope creep" prior art (MEDIUM relevance)

**Source (medium.com/@acaygoren acceptance-criteria article):** "Scope Creep and Changing Requirements: One of the common challenges with acceptance criteria is scope creep, where stakeholders attempt to add new requirements or **change existing ones** after the criteria have been defined."

**Source (Tuskr-cited 7-ways article, in S2 search):** "Acceptance criteria often become outdated as products evolve, leading to misalignment between specifications and actual functionality. This **documentation drift** creates subtle bugs."

**Relevance to our codebase:** The exact phrase "weakened criteria" is not directly mirrored in canonical SE literature, but the concept — acceptance-criteria erosion, criteria becoming less stringent than the originating spec — is well-attested in agile/PM scope-creep discourse. The task-builder axis is a domain-specific name for a recognized phenomenon.

### Finding E — Red-team / blue-team applied to design docs is documented practice (MEDIUM relevance)

**Source S8 (druid628):** "If you've ever had a TDD red-teamed and absolutely shredded by the Navy's N6…" — describes red-teaming as separate-session pressure-test on top of standard design walkthrough. Blue team = "the group responsible for the design itself…the people building the architecture, writing the technical design document"; red team = "exists to challenge how that problem is being solved."

**Relevance:** Supports the "adversarial overlay" framing of axes — they are red-team challenge categories applied to QA reports, structurally parallel to design-doc red-teaming.

### Finding F — "Anti-inflation" / "RELIANCE ≠ VERIFICATION" prior art in Fagan inspections (MEDIUM-HIGH relevance)

**Source S4 (Fagan inspection Wikipedia):** "Any failure of the low-level document to satisfy the high-level requirements specified in the high-level document are called defects." Fagan inspection is **evidence-based** — inspectors must independently re-derive defects from artifacts, not rely on author summaries.

**Source S5 (Doolan 1991):** Major defects "can be identified very simply: had the software been produced according to the uncorrected specification, the 'major defect' would have resulted in a fault report." — i.e., defects must be **independently testable**, not asserted.

**Source S11 (Refute-or-Promote):** "ten dedicated reviewers unanimously endorsed a non-existent Bleichenbacher padding oracle…it was killed only by a single **empirical test**" — this is direct prior art for the "RELIANCE on consensus ≠ VERIFICATION" anti-inflation rule.

**Source (Datadog hallucination LLM-as-judge):** LLM-as-judge faithfulness scoring explicitly distinguishes "white-box methods inspect the LLM directly, whereas black-box methods can be applied without access" — analogue to our distinction between reading-a-report (reliance) vs reading-the-source (verification).

**Relevance to our codebase:** rf-qa-qualitative.md:766-775's verbatim rule ("NEVER mark an item VERIFIED if you only read about it in another report — that is RELIANCE, not VERIFICATION") is **directly supported** by the Refute-or-Promote 2026 finding that consensus among adversarial reviewers can endorse non-existent defects, and by classical Fagan inspection's requirement for independent defect re-derivation.

---

## 3. Prior-art for the 5-axis taxonomy

**Verdict:** The exact 5-tuple `{drift, contradictions, omissions, weakened-criteria, invented-content}` is **task-builder/sc-tasklist-internal naming**, but each individual axis has documented prior art:

| Axis | Closest external prior art | Tradition |
|---|---|---|
| **omissions** | Travassos 2001 "Omission"; Doolan 1991 "major omissions"; Fagan inspection major-defect class; Wiegers SRS checklist "Is any necessary information missing?" | **Canonical SE since 1976** |
| **contradictions** | Travassos 2001 "Inconsistency"; IEEE 830 §4.3.4 "Internal Consistency"; Wiegers "Do any requirements conflict with…other requirements?" | **Canonical SE since IEEE 830-1984** |
| **invented-content** | LLM-hallucination "Fabrication" (LayerLens, S19); Travassos 2001 "Extraneous Information" (partial); ACM CSUR S17 "factuality hallucination" | **Mixed: classical (extraneous info) + LLM-era (fabrication)** |
| **drift** | LLM-faithfulness "drift from original input" (arXiv 2510.06265, S18); LayerLens "Citation Drift" (S19); "tangential hallucinations" (S21) | **LLM-era 2023+** |
| **weakened-criteria** | Acceptance-criteria erosion / scope-creep literature (Atlassian, monday.com); "under-specification with mild requirement creep" (arXiv 2510.22944 L2 rubric, S22) | **Agile/PM tradition 2010s+** |

The 5-tuple is therefore **not** a recognized industry taxonomy under that name, but is a **legitimate synthesis** combining (a) classical Fagan/IEEE inspection categories with (b) modern LLM-faithfulness categories with (c) agile scope-creep concepts. This is the right reading for TDD §21 (Alternatives Considered) — the choice is between (i) using only the classical 3-axis Travassos taxonomy, (ii) using only the LLM-faithfulness taxonomy, or (iii) the hybrid 5-axis we adopt.

---

## 4. Prior-art for multi-stage QA gates

The 4-stage gate topology (research-gate → synthesis-gate → report-validation → task-integrity) is **well-supported** by external practice:

| Stage analogue | External prior art |
|---|---|
| Stage-gated decision points with fail-closed semantics | Stage-Gate® (Cooper, S16); SonarQube Quality Gate (S13); Dynatrace Quality Gates (S14); Perforce Quality Gates (S15) |
| Multi-stage adversarial review | Refute-or-Promote arXiv 2604.19049 (S11) — adversarial stage-gated multi-agent review with mandatory empirical gate |
| 3-stage GAN-style adversarial loop | freeCodeCamp multi-agent GAN architecture (S12) — Planning / Implementation / Final-Review topology |
| Tiered design-doc review (Big Tech) | Pragmatic Engineer (S9); Google design docs (S10) — tiered review by criticality |

**Key insight for TDD §6.4:** Our 4-stage gate is **not novel** as a topology — it's an instance of a well-established stage-gate pattern with adversarial overlay. What is more distinctive is the **inherited-verdict / verdict-passthrough** semantic (FR-CONV.3), which has direct prior art in:

- Refute-or-Promote (S11): adversarial endorsement is **not sufficient** alone; the empirical gate inherits/overrides earlier verdicts. "Ten dedicated reviewers unanimously endorsed a non-existent…oracle; it was killed only by a single empirical test." This is structurally identical to FR-CONV.3 inherited-structural-verdict: earlier-stage verdicts feed into the next gate but cannot override its independent finding.

---

## 5. Anti-inflation rule prior art

The "VERIFIED requires evidence / RELIANCE ≠ VERIFICATION" rule (rf-qa-qualitative.md:766-775) has strong external grounding:

1. **Fagan inspection (S4, S5):** Defects must be independently re-derived, not asserted; major defects are those that "would have resulted in a fault report" — i.e., independently testable.

2. **Refute-or-Promote (S11):** Most-cited concrete failure mode of multi-reviewer adversarial review is consensus on non-existent defects. The paper's resolution is the "mandatory empirical gate" — exactly the structural pattern rf-qa-qualitative enforces.

3. **LLM-faithfulness QA-based metrics (S17, fig 3):** Faithfulness detection methods explicitly distinguish "Fact-based Metrics: Measures the overlap of extracted facts between the generated content and the source content" — facts must trace to source, not to another fact-extraction.

4. **Datadog LLM-as-judge guidance:** Faithfulness assessment requires comparing answer to source context, not to another LLM judgment.

**Recommendation:** Cite Refute-or-Promote (arXiv 2604.19049) in TDD §6.4 as direct external prior art for the anti-inflation rule. The OpenSSL/Bleichenbacher example is a perfect concrete illustration.

---

## 6. Recommendations for TDD §6.4 and §21

### For TDD §6.4 (Key Design Decisions)

Suggested decision row:

> **Decision:** Adopt 5-axis adversarial taxonomy `{drift, contradictions, omissions, weakened-criteria, invented-content}` as an **overlay** on rf-qa-qualitative's existing 15-item checklist, rather than as a replacement.
>
> **Rationale:**
> - Axes synthesize three established traditions: classical Fagan/IEEE SRS-inspection taxonomy (omissions, contradictions, extraneous-info → invented-content), LLM-faithfulness literature (drift, fabrication), and agile scope-creep discourse (weakened-criteria / acceptance-erosion).
> - Overlay-rather-than-replace preserves the 15-item structural checklist that has codebase-validated provenance, while adding adversarial dimensionality only where each item has a natural axis.
> - The "fail-closed any-axis-fails = FAIL" semantic matches industry quality-gate practice (SonarQube, Dynatrace, Perforce).
>
> **Citations:** Travassos 2001 SRS taxonomy (S6); ACM CSUR LLM hallucination survey (S17); arXiv 2604.19049 Refute-or-Promote (S11).

### For TDD §21 (Alternatives Considered)

Suggested Alternative 1 (bulk-port of all 17 sc-tasklist checks):

> **Alternative 1:** Bulk-port the entire 17-item sc-tasklist adversarial check list verbatim into rf-qa-qualitative, replacing the existing 15-item structural checklist.
>
> **Why rejected:**
> - Per-check classification (CB-3 codebase analysis) shows that of the 17 sc-tasklist items, only the 5-axis taxonomy carries forward cleanly; the remaining items are tasklist-bundle-specific (e.g., Sprint-CLI compatibility checks, manifest validation) and don't map to MDTM task-file QA.
> - The 15-item rf-qa-qualitative checklist has its own codebase-validated provenance and removing it would lose information.
> - Prior art (Travassos 2001, IEEE 830, Fagan inspection) supports treating the adversarial axes as a **classification dimension** layered onto the existing checklist, not as a wholesale replacement. This is how the LLM-faithfulness literature (ACM CSUR S17) layers faithfulness sub-types onto QA-evaluation methods.
>
> **Citations:** S6 (Travassos 2001), S17 (ACM CSUR survey), S4 (Fagan).

Suggested Alternative 2 (use only classical 3-axis Travassos taxonomy):

> **Alternative 2:** Use only the classical 3-axis Travassos taxonomy `{omissions, contradictions, extraneous-information}`.
>
> **Why rejected:** Misses LLM-era failure modes (drift, fabrication) that are critical for QA of agent-generated reports. ACM CSUR 2024 (S17) and 2025 LLM-hallucination literature (S18, S19) document these as distinct, prevalent failure modes in agent-generated artifacts.

Suggested Alternative 3 (use only LLM-faithfulness taxonomy):

> **Alternative 3:** Use only LLM-faithfulness taxonomy (instruction-inconsistency / context-inconsistency / logical-inconsistency) per ACM CSUR 2024.
>
> **Why rejected:** Misses scope-creep / acceptance-criteria-erosion failure mode (weakened-criteria axis), which is a recognized agile-PM concern (Atlassian, monday.com scope-creep literature). Also loses the long-standing SE-inspection grounding for omissions/contradictions which is more rigorous and testable than the LLM-faithfulness sub-categories.

### For TDD §6.4 (Inherited-Verdict pattern — FR-CONV.3)

Suggested decision row:

> **Decision:** Adopt inherited-structural-verdict pattern — earlier-stage adversarial verdicts feed into later gates as inputs but cannot override the later gate's independent finding.
>
> **Rationale:** Direct prior art in Refute-or-Promote (arXiv 2604.19049, S11): "ten dedicated reviewers unanimously endorsed a non-existent Bleichenbacher padding oracle…it was killed only by a single empirical test, motivating the mandatory empirical gate." This is the exact failure mode the inherited-verdict pattern prevents — consensus among adversarial reviewers becoming a false-positive endorsement.

---

## 7. Codebase remains source of truth

**Explicit reminder:** None of the external sources surveyed contradict the verified code in `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` lines 1112-1117 or `src/superclaude/agents/rf-qa-qualitative.md` lines 527-583, 766-775. The external prior art is **supportive context** for TDD §6.4 and §21 narrative, not a competing specification.

If any future external claim contradicts the verified code, the code wins and the discrepancy is flagged for human review per the freshness-discipline directive in user CLAUDE.md.

---

## Summary

- The 5-axis `{drift, contradictions, omissions, weakened-criteria, invented-content}` is **task-builder-specific naming** but every axis has published external prior art across three traditions: classical SE inspection (Fagan/IEEE/Travassos), LLM-faithfulness literature (ACM CSUR 2024, arXiv 2510), and agile scope-creep discourse.
- The 4-stage fail-closed gate topology is a direct instance of recognized stage-gate engineering practice (Stage-Gate®, SonarQube, Dynatrace, Refute-or-Promote 2026).
- The anti-inflation rule (RELIANCE ≠ VERIFICATION) has strong prior art in Fagan inspections and most directly in Refute-or-Promote (OpenSSL Bleichenbacher consensus-false-positive case study) — recommend citing this in TDD §6.4.
