# Validation Checklists Reference

> Synthesis Quality Review, Assembly Process, Validation Checklist, and Content Rules, loaded during Stage A.7 by the builder subagent.

---

## Synthesis Quality Review Checklist

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

**This checklist is enforced by the rf-analyst and rf-qa agents** (see Phase 5 in the task phases). The rf-analyst applies these 9 criteria as its Synthesis Quality Review analysis type, and the rf-qa agent independently verifies the analyst's findings with its expanded 12-item Synthesis Gate checklist. The QA agent can fix issues in-place when authorized.

The 9 criteria (used by rf-analyst):

1. Template section headers match exactly (per `src/superclaude/examples/prd_template.md`)
2. Tables use the correct column structure from the template (competitive matrix, requirements table, KPI table, scope table, risk matrix, etc.)
3. No content was fabricated beyond what research files contain
4. Findings cite actual file paths and feature names (not vague descriptions)
5. User stories follow the As a / I want / So that format with testable acceptance criteria
6. Requirements use RICE or MoSCoW prioritization framework
7. Cross-section consistency (personas referenced in user stories, requirements have acceptance criteria, risks have mitigations)
8. **No doc-only claims in product capability or feature sections** — every feature described must be backed by code evidence. If a synth file describes a capability and the only evidence is a documentation file (no source code path), reject that claim and flag it as `[UNVERIFIED — doc-only]`
9. **Stale documentation discrepancies are surfaced** — any `[CODE-CONTRADICTED]` or `[STALE DOC]` findings should appear in Open Questions (Section 13) or Assumptions & Constraints (Section 10), not silently omitted

The rf-qa agent's Synthesis Gate adds 3 additional checks (10-12): content rules compliance, section completeness (no placeholders), and hallucinated file path detection. If synthesis QA fails, the QA agent fixes issues in-place (when authorized) and issues remaining unfixed trigger re-synthesis of the affected files.

---

## Assembly Process

### Step 8: Assemble the PRD

Read all synth files in order and assemble the final document:

1. **Start with the template frontmatter** — fill in all fields from the template. Set `status: "🟡 Draft"`, populate `created_date`, `depends_on`, `tags`, etc.

2. **Write the HOW TO USE blockquote** — follow the template's preamble format.

3. **Write the Document Information table** — Product Name, Product Owner, Engineering Lead, Design Lead, Stakeholders, Status, Target Release, Last Updated, Review Cadence.

4. **Assemble sections in template order** — paste each synth file's content into the correct position. Sections that weren't assigned a synth file get written directly during assembly from patterns observed in the synth files.

5. **Write the Table of Contents** — generate from actual section headers.

6. **Add Appendices** — Glossary, Acronyms, Technical Architecture Diagrams, User Research Data, Financial Projections as applicable.

7. **Add Document History** — initial entry.

8. **Add Document Provenance** — if the PRD was created by consolidating existing docs, add an `Appendix: Document Provenance` subsection documenting the source materials and creation method. Zero content loss: every piece of metadata from source documents must appear somewhere in the normalized PRD.

### Step 9: Validate the Output

Before presenting to the user, validate:

- [ ] All template sections present (or explicitly marked as N/A with rationale)
- [ ] Frontmatter has all required fields from the template
- [ ] Total line count within tier budget (Lightweight: 400-800, Standard: 800-1500, Heavyweight: 1500-2500)
- [ ] HOW TO USE blockquote present
- [ ] Document Information table has all 9 rows
- [ ] Numbered Table of Contents present
- [ ] User stories follow As a / I want / So that format
- [ ] Acceptance criteria are specific and testable for each story
- [ ] Feature prioritization uses RICE or MoSCoW framework
- [ ] Competitive analysis includes feature comparison matrix
- [ ] KPI tables have measurement methods defined
- [ ] No full source code reproductions
- [ ] All file paths reference actual files that exist
- [ ] Document History table present
- [ ] Tables use correct column structure from template
- [ ] No doc-sourced claims presented as verified without code cross-validation tags
- [ ] Web research findings include source URLs for every external claim
- [ ] Gaps and questions file exists at `${TASK_DIR}gaps-and-questions.md`

### Step 10: Present to User

Notify the user:
- Where the final document was written
- Line count and tier classification
- Number of sections populated vs skipped
- Where the research/synth artifacts live (for future reference)
- Any gaps or areas that need manual review

### Step 11: Clean Up Consolidation Sources

If the PRD was created by consolidating existing docs:
- Do NOT delete the source docs automatically
- Present the source docs to the user and confirm they can be archived
- Archive approved sources to `docs/archive/[appropriate-subdir]/`
- Update any references to the archived files in other documents
- Check off items in the stub's consolidation checklist if one exists

---

## Validation Checklist

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

Before presenting the PRD to the user, validate against this checklist (this is encoded in the task file's Assembly phase):

**Structural completeness:**

- [ ] All 32 numbered template sections present (or explicitly marked as N/A with rationale)
- [ ] Frontmatter has all required fields from the template (id, title, status, created_date, tags, depends_on)
- [ ] HOW TO USE blockquote present with document purpose and usage guidance
- [ ] Document Information table has all 9 rows (Product Name, Product Owner, Engineering Lead, Design Lead, Stakeholders, Status, Target Release, Last Updated, Review Cadence)
- [ ] Numbered Table of Contents present and matches actual section headers — no orphaned or missing entries

**Content quality:**

- [ ] Stakeholder segments clearly defined with structured persona attribute tables (Section 7)
- [ ] User journeys documented with As a / I want / So that format and testable acceptance criteria (Section 21.1)
- [ ] Feature scope bounded — In Scope, Out of Scope, and Permanently Out of Scope all populated with rationale (Section 12)
- [ ] Acceptance criteria are measurable and testable — no vague criteria like "works well" or "is fast"
- [ ] Competitive landscape analyzed with feature comparison matrix using status icons (Section 9)
- [ ] Success metrics quantified with specific targets and measurement methods (Section 19)
- [ ] Requirements use RICE or MoSCoW prioritization framework with scores/categories (Section 21.2)

**Evidence integrity:**

- [ ] No fabricated market claims — all TAM/SAM/SOM figures, market data, and competitive claims cite sources
- [ ] All feature descriptions verified against codebase — no doc-only claims without `[UNVERIFIED]` tags
- [ ] Web research findings include source URLs for every external claim
- [ ] All `[CODE-CONTRADICTED]` and `[STALE DOC]` findings surfaced in Open Questions (Section 13) or Assumptions & Constraints (Section 10)
- [ ] Gaps and questions file exists at `${TASK_DIR}gaps-and-questions.md`

**Format compliance:**

- [ ] Total line count within tier budget (Lightweight: 400-800, Standard: 800-1500, Heavyweight: 1500-2500)
- [ ] Tables use correct column structure from the template (KPI table, scope table, risk matrix, competitive matrix)
- [ ] No full source code reproductions in any section
- [ ] Document History table present with initial entry
- [ ] Document Provenance appendix present if consolidating existing docs

---

## Content Rules (From Template — Non-Negotiable)

These rules come from the template's structure and conventions. Every PRD must follow them.

| Rule | Do | Don't |
|------|-----|-------|
| **Product vision** | Concise vision statement with 1-2 paragraph expansion | Multi-page vision essays or vague aspirations |
| **User personas** | Structured attribute tables with representative quotes | Lengthy narrative character descriptions |
| **User stories** | Standard format: As a / I want / So that with acceptance criteria | Vague feature descriptions without user context |
| **Competitive analysis** | Feature comparison matrices with status icons (✅/⚠️/❌) | Prose-based competitor descriptions |
| **Requirements** | Prioritized tables with RICE scores or MoSCoW categories | Unprioritized feature lists or wish lists |
| **Market data** | TAM/SAM/SOM tables with sources and evidence | Unsourced market claims or guesses |
| **KPIs** | Table: Category / KPI / Target / Measurement Method | Vague success metrics without measurement methods |
| **Scope** | In/Out/Deferred tables with rationale for each decision | Unbounded scope descriptions or missing exclusions |
| **Risk analysis** | Probability/Impact matrices with mitigations and contingencies | Lists of concerns without assessment or mitigation |
| **Timeline** | ASCII timeline diagrams with milestones and phase breakdowns | Vague "Q3" or "soon" dates without structure |

---
