# Research: rf-qa-qualitative Agent Topology

**Status:** In Progress
**Date:** 2026-05-14
**Agent type:** Code Tracer
**Source:** src/superclaude/agents/rf-qa-qualitative.md (794 lines)

---

## 1. All 7 Specialised QA Phases

The agent defines **8 QA phases** total — 7 specialised + 1 fallback (`doc-qualitative`). Each is structured identically: trigger ("When"), purpose, input contract, sized checklist, severity ratings, mandatory self-audit, verdict block.

### 1.1 prd-qualitative (file:99-194)

- **Trigger** (file:101): "After rf-qa structural verification passes (report-validation phase), before presenting to user."
- **Purpose** (file:102): Verify the PRD makes sense as a product document — correct scoping, logical content, realistic requirements, no red flags from product or engineering perspective.
- **Input contract** (file:106): "The assembled PRD + the PRD template (for scope notes and section expectations)" — agent must read **entire document end to end** (file:108).
- **Checklist size** (file:110): **23 items**, grouped as Scope Appropriateness (1-3), Content Quality (4-10), Logical Consistency (11-15), Red Flags (16-23).
- **Output report path:** Generic Output Format block (file:677-714) — supplied via spawn prompt `output_path` field (file:46).

### 1.2 report-qualitative (file:196-241)

- **Trigger** (file:198): "After rf-qa report-validation passes, before presenting to user."
- **Purpose** (file:199): Verify the research report makes sense as a technical investigation document.
- **Input contract** (file:203): "The final research report at `${TASK_DIR}RESEARCH-REPORT-*.md`"
- **Checklist size** (file:205): **12 items** — covers problem/findings fidelity, distinct options, evidence trail, no circular reasoning, proportionate conclusion.
- **Output report path:** Per Output Format block + spawn `output_path`.

### 1.3 tdd-qualitative (file:244-308) — **THE phase that validates our Phase-6 TDD**

- **Trigger** (file:246): "After rf-qa structural verification passes (report-validation phase), before presenting to user."
- **Purpose** (file:247): Verify the TDD makes sense as a technical design document — architecture decisions are sound, API contracts are consistent, implementation details are specific enough to code from, and the design faithfully translates PRD requirements without inventing or losing any.
- **Input contract** (file:251): "The assembled TDD + the TDD template (for section expectations) + the source PRD (if referenced)"; must read **entire document end to end** (file:253).
- **Checklist size** (file:255): **14 items**, grouped as PRD-to-TDD Fidelity (1-4), Internal Consistency (5-8), Specificity and Actionability (9-11), Red Flags (12-14).
- **Output report path:** Per Output Format block + spawn `output_path`.

### 1.4 tech-ref-qualitative (file:312-372)

- **Trigger** (file:314): "After rf-qa structural verification passes (report-validation phase), before presenting to user."
- **Purpose** (file:315): Verify the tech reference accurately documents the current implementation — not aspirational, not historical, but what actually exists and works right now.
- **Input contract** (file:319): "The assembled tech reference document + the template (for section expectations)".
- **Checklist size** (file:323): **12 items**, grouped as Code-to-Document Fidelity (1-4), Structural Accuracy (5-7), Completeness (8-10), Red Flags (11-12).
- **Output report path:** Per Output Format block + spawn `output_path`.

### 1.5 ops-guide-qualitative (file:376-440)

- **Trigger** (file:378): "After rf-qa structural verification passes (report-validation phase), before presenting to user."
- **Purpose** (file:379): Verify the operational guide would actually work if someone followed it step by step — correct ordering, complete prerequisites, parameterized values, and rollback coverage for destructive operations.
- **Input contract** (file:383): "The assembled operational guide + the template (for section expectations)".
- **Checklist size** (file:387): **14 items**, grouped as Procedural Correctness (1-5), Environment and Configuration (6-8), Monitoring and Recovery (9-11), Operational Hygiene (12-14).
- **Output report path:** Per Output Format block + spawn `output_path`.

### 1.6 readme-qualitative (file:444-504)

- **Trigger** (file:446): "After rf-qa structural verification passes (report-validation phase), before presenting to user."
- **Purpose** (file:447): Verify the README works as a navigational entry point — a new developer can go from zero to productive by following it.
- **Input contract** (file:451): "The assembled README + the template (for section expectations)".
- **Checklist size** (file:455): **12 items**, grouped as Getting Started Experience (1-4), Navigation and Links (5-7), Audience Appropriateness (8-10), Completeness and Freshness (11-12).
- **Output report path:** Per Output Format block + spawn `output_path`.

### 1.7 task-qualitative (file:508-603) — **FR-CONV.4 5-axis overlay insertion site**

- **Trigger** (file:510): "After rf-qa structural verification passes (task-integrity phase), before presenting to user."
- **Purpose** (file:511): Verify the task file would actually succeed if executed — not just that it's well-formed, but that the plan is operationally correct.
- **Input contract** (file:515-519): Task file path + Research directory + Target file list (ALL referenced source files, no spot-checking) + Project conventions. Must read entire task file end to end, then for each item that modifies code, read the actual target source file (file:525).
- **Checklist size** (file:527): **15 items**, grouped as Operational Simulation (1-3), Code Compatibility (4-6), Test and Verification Quality (7-8), Failure Mode Analysis (9-15).
- **Output report path:** Per Output Format block + spawn `output_path`.

### 1.8 doc-qualitative (file:607-634) — fallback

- **Trigger** (file:609): "After structural QA, before delivery."
- **Purpose** (file:610): Fallback qualitative review for document types without a dedicated phase. Prefer dedicated phases when available.
- **Checklist size** (file:614): **8 items**.

---

## 2. Self-Audit Requirement (per phase) — INV-019 driver

Every one of the 8 QA phases ends with the **same** Self-Audit block, repeated verbatim. This is the operational hook FR-CONV.3 / INV-019 relies on: the agent MUST list evidence beyond inherited verdicts.

**Verbatim quote** (e.g. prd-qualitative at file:183-187; identical at file:231-235, 299-303, 363-367, 431-435, 495-499, 590-594, 625-629):

```
### Self-Audit (MANDATORY before writing verdict)
Before issuing your verdict, answer these questions in your report:
1. How many factual claims did you independently verify against source code?
2. What specific files did you read to verify claims?
3. If you found 0 issues, why should the user trust that you checked thoroughly?
```

**Operational implication for FR-CONV.3 / INV-019:**
- Question 1 ("How many factual claims did you independently verify") demands a count of **own** verifications — a finding inherited from a prior structural verdict does not increment this count.
- Question 3 ("If you found 0 issues, why should the user trust that you checked thoroughly?") makes a bare PASS that cites only an inherited verdict facially insufficient.
- Together they mandate **≥1 semantic check beyond the inherited PASS** — which is precisely what INV-019 codifies.
- Anchored by the Adversarial Stance at file:84: "A review that finds 0 issues should be treated with suspicion, not satisfaction."

---

## 3. Anti-Inflation Rule (file:766-780 verbatim) — FR-CONV.3 negative criterion

**This rule MUST NOT be weakened by FR-CONV.3.** FR-CONV.3 inserts an Inherited Structural Verdict block but cannot relax the prohibition on inflated tool engagement.

**Verbatim (file:766-775, including the rule, the Tool Engagement Minimum, and a trailing Qualitative Adaptation):**

```
### Prohibited Behaviors
- NEVER adjust confidence based on subjective feeling — it is COMPUTED from the checklist
- NEVER report confidence without the raw numbers
- NEVER claim VERIFIED without citing specific tool output (file path, line number, grep result)
- NEVER mark an item VERIFIED if you only read about it in another report — that is RELIANCE, not VERIFICATION
- NEVER issue a PASS verdict without meeting the threshold
- NEVER make generic tool calls to inflate engagement counts — each tool call must directly verify a specific checklist item. A Read call must target the file being verified, a Grep must search for the specific claim being checked. Tool calls that don't map to specific verifications are padding, not evidence.

### Tool Engagement Minimum
If your total (Read + Grep + Glob) calls < TOTAL checklist items, the review is automatically suspect. You cannot have verified more items than you made tool calls. Flag this in your report.

### Qualitative Adaptation
For qualitative checks that involve judgment calls (e.g., "is the audience appropriate?"), the VERIFIED marker requires citing what specific content was read and what conclusion was drawn. The judgment itself counts as verified if the evidence trail is documented.
```

**Sed verification (file:766-780):** confirmed verbatim above. PRD assertion (current location 766-775) is correct: header at line 766, anti-inflation bullet at line 772; lines 776-780 carry Tool Engagement Minimum + Qualitative Adaptation.

**Critical relationship to FR-CONV.3 / INV-019:**
- The bullet at file:769 ("NEVER claim VERIFIED without citing specific tool output") and file:770 ("NEVER mark an item VERIFIED if you only read about it in another report — that is RELIANCE, not VERIFICATION") **already** establish that an inherited structural verdict cannot be cited as a substitute for the agent's own verification.
- INV-019 makes this *operationally provable* via Self-Audit listings: the report must list ≥1 semantic check the agent performed beyond reading the inherited verdict.
- FR-CONV.3's Inherited Structural Verdict block (insertion at file:794) must therefore be additive — it surfaces the structural verdict for context but cannot license a PASS that does not satisfy the Self-Audit's "independently verify" count.

---

## 4. Adversarial Axes Overlay Landing Site — Task-Qualitative Checklist (file:527-583 verbatim)

FR-CONV.4 will insert a "Five Adversarial Axes" header BEFORE this 15-item body. **The 15-item body MUST NOT be modified.**

**Verbatim (file:527-583):**

```
#### Checklist (15 items)

**Operational Simulation**

1. **Gate/command dry-run** — For every shell command, make target, or gate referenced in checklist items (`make verify-sync`, `make sync-dev`, `pytest`, grep checks, etc.), reason through whether it would succeed given the current repo state. Check preconditions: does the directory exist? Does the file the command operates on exist? Would the command's assertions pass? If a gate will always fail given the current state, that's CRITICAL — the task will halt at that point.

2. **Project convention compliance** — If the project has source-of-truth conventions (e.g., `src/` → `.claude/` sync, monorepo package boundaries, generated file patterns), verify every edit targets the correct side of the boundary. An item that edits a generated file directly instead of its source will be silently overwritten. An item that edits source without updating the generated counterpart will create drift. Check: "does this edit go to the right place given how the project's build/sync works?"

3. **Intra-phase execution order simulation** — Mentally execute each phase's items in order. At each item, ask: "do I have everything I need from previous items?" If item N reads a file that item N+2 creates, the phase will fail at item N. This goes beyond rf-qa's structural ordering check — it requires understanding what each item actually does, not just what files it references.

**Code Compatibility**

4. **Function signature verification** — For each item that modifies a function, read the actual function in the target source file. Verify: (a) the function exists at the described location, (b) the described modification is compatible with the actual signature (parameter names, types, return type), (c) the function's call sites won't break from the change. If the item says "add a conditional when TDD content is present" but the function never receives TDD content, the item is wrong.

5. **Module context analysis** — For each item that adds or modifies a function, read the full module (not just the function). Check for module-level constants, imports, decorators, and ambient dependencies that the new/modified function must interact with. If the module has `_OUTPUT_FORMAT_BLOCK` as a constant used by sibling functions and the new function doesn't reference it, that's likely an omission. The item should account for the module's patterns, not just the individual function.

6. **Downstream consumer analysis** — For each item that changes an output format, schema, or return value, trace all consumers of that output. If extraction adds 6 new fields but the generation step doesn't know about them, the new fields are extracted and then ignored — the change is incomplete. Check: "who reads the output of this change, and are they updated too?"

**Test and Verification Quality**

7. **Test validity** — Verification steps must test the actual artifact with representative input, not stubs. A test that writes `# Test` to a file and asserts against that 6-character placeholder is structurally present but operationally useless — it doesn't test the feature being built. Check: does the test exercise the real behavior with realistic input that would expose bugs?

8. **Test coverage of primary use case** — The task's tests should cover the primary use case end-to-end, not just individual functions in isolation. If the task builds a TDD extraction pipeline, at least one test should feed a real (or realistic) TDD file through the full pipeline and verify the output. Unit tests of individual functions are necessary but not sufficient.

**Failure Mode Analysis**

9. **Error path coverage** — For each new user-facing flag, input type, or configuration option, verify the task includes validation and meaningful error messages for misuse. What happens if the user passes the wrong file type? What happens if a required field is missing? Silent garbage output from bad input is worse than a crash — it produces plausible-looking wrong results.

10. **Runtime failure path trace** — Trace the execution path from entry point through pipeline to completion. Identify any step where the implemented changes produce output that a downstream gate, validator, or consumer cannot handle. If the task adds a new input type but doesn't update a format gate downstream, the pipeline will fail silently or with a confusing error. Draw the data flow: input → [step 1] → [step 2] → ... → output. Where does it break?

11. **Completion scope honesty** — Does the task honestly represent what it will accomplish? If the task has Open Questions flagging critical unknowns (e.g., "C-1: unclear if X is supported"), do the implementation items resolve those questions — or do they proceed as if the questions don't exist and then mark "done" anyway? A plan that ignores its own open questions is not a complete plan.

12. **Ambient dependency completeness** — For each new function or modified module, verify the task addresses ALL necessary touchpoints — not just the obvious ones. This includes: import statements, `__init__.py` exports, CLI argument parsers, configuration defaults, documentation references, and any registry/dispatch table the module participates in. A function that exists but isn't importable or callable from the entry point is dead code.
13. **Kwarg sequencing red flags** — Look for "add kwarg" items before "add parameter" items. Check deferred-action patterns have completion items. If an item passes a new argument to a function, verify that an earlier item updates the function signature to accept it.
14. **Function existence claims require verification** — "does not exist" and "exists at path X" claims must ALL be grep-verified against actual source code. No unverified existence claims. If the task says a function exists, grep for it. If it says one doesn't exist, grep to confirm.
15. **Cross-reference accuracy for templates** — Verify ALL template section references (§N, "Section X") per phase against actual template content. Read the actual template file and confirm the referenced section exists and contains what the item claims.

### Adaptation Guidance (NO check may be marked N/A — adapt instead)

| Item | Code Task | Doc Task Adaptation |
|------|-----------|-------------------|
| 1. Gate/command dry-run | Verify commands would succeed | Verify documented commands/values match source code |
| 2. Project convention compliance | Check sync boundaries | Check doc naming, placement, cross-refs follow conventions |
| 3. Intra-phase execution simulation | Check item dependencies | Check section dependencies and logical flow |
| 4. Function signature verification | Check actual signatures | Verify every documented value (ports, counts, paths, configs) against actual source |
| 5. Module context analysis | Read full module | Read surrounding doc sections for consistency |
| 6. Downstream consumer analysis | Trace call sites | Check cross-doc references — do other docs that cite these values need updating? |
| 7. Test validity | Check tests are real | Check verification steps are substantive, not rubber stamps |
| 8. Test coverage | Check primary use case | Check all acceptance criteria are actually verified |
| 9. Error path coverage | Check error handling | Check edge cases and limitations are documented |
| 10. Runtime failure path trace | Trace data flow | Trace doc changes — would a developer following this doc succeed? |
| 11. Completion scope honesty | Check open questions | Check whether all claimed fixes were actually applied |
| 12. Ambient dependency completeness | Check all touchpoints | Check frontmatter, TOC, cross-refs, history entries all updated |
| 13. Kwarg sequencing | Check execution order | Check that dependent edits are ordered correctly |
| 14. Function existence verification | Grep for functions | Grep for every claimed value, path, config against source |
| 15. Template cross-references | Read templates | Read every referenced template section and verify content |
```

**FR-CONV.4 insertion rule:** A "Five Adversarial Axes" header is to be added BEFORE the `#### Checklist (15 items)` line at file:527. The numbered 1-15 body and the Adaptation Guidance table at file:564-582 are immutable surfaces.

---

## 5. Items Reviewed Table Schema (file:675-714 verbatim)

FR-CONV.4 will add an `axis` column to this table. **Current 4-column schema:**

**Verbatim (file:675-714):**

```
## Output Format (All Phases)

```markdown
# QA Report — [Phase Name]

**Topic:** [topic]
**Date:** [today]
**Phase:** [prd-qualitative / tdd-qualitative / tech-ref-qualitative / ops-guide-qualitative / readme-qualitative / report-qualitative / task-qualitative / doc-qualitative / fix-cycle]
**Fix cycle:** [1 / 2 / 3 / N/A]

---

## Overall Verdict: [PASS / FAIL]

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | [check name] | PASS / FAIL | [what you verified and how] |

## Summary
- Checks passed: [count] / [total]
- Checks failed: [count]
- Critical issues: [count]
- Issues fixed in-place: [count] (if fix-authorized)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL / IMPORTANT / MINOR | [file:section] | [what's wrong] | [specific fix] |

## Actions Taken
[If fix-authorized, list every fix applied]
- Fixed [issue] in [file] by [action]
- Verified fix by [verification method]

## Recommendations
- [Actions needed before proceeding]

## QA Complete
```
```

**Current Items Reviewed columns** (file:690-693): `# | Check | Result | Evidence` (4 columns).

**FR-CONV.4 transformation:** add `Axis` column → `# | Check | Axis | Result | Evidence` (5 columns). The `Axis` value maps each task-qualitative check to one of the Five Adversarial Axes overlay headers introduced by Section 4.

---

## 6. Inherited Structural Verdict Block Insertion Site (file:790-794 — file ends at 794)

NOTE: The PRD's "790-798" range overshoots the file by 4 lines; the file is 794 lines long (confirmed by `wc -l`). The insertion site is the tail of the Critical Rules section.

**Verbatim (file:782-794):**

```
## Critical Rules

1. **NEVER one-shot your output file** — Create the file immediately with a header (Write), then append findings incrementally section by section (Edit). Never accumulate the entire report in context and write it in one shot. One-shotting hits max token output limits and freezes the process. This is the #1 failure mode for all agents.
2. **Read the ENTIRE document** — Do not skim. Qualitative issues hide in the details. Read every section, every table row, every acceptance criterion.
3. **Think like a stakeholder** — Would a PM approve this? Would an engineer be able to build from this? Would a VP present this to investors? If any answer is "no," that's a finding.
4. **Evidence for every verdict** — Never say "this seems fine" without explaining what you checked. Never say "this is wrong" without explaining what it should be.
5. **Fix then verify** — If authorized to fix, always verify the fix worked. A fix that doesn't verify = still failed.
6. **Contradictions are always IMPORTANT or CRITICAL** — If two sections say different things about the same topic, that's never minor. Always surface contradictions.
7. **Be specific about fixes** — "This section needs work" is useless. "S5.1 contains a KPI table with 11 metrics that duplicates S19 — replace with business justification prose and a forward reference to S19" is useful.
8. **Scope is the #1 issue** — The most common qualitative failure is content at the wrong scope level (platform content in feature PRDs, feature content in platform PRDs). Check this first and thoroughly.
9. **Report honestly** — A false PASS that lets a bad PRD reach stakeholders is worse than a false FAIL that triggers one more review cycle. When in doubt, fail it and explain why.
10. **Maximum 3 fix cycles** — After 3 rounds of fixes without resolution, HALT and escalate to the user. ALL findings regardless of severity must be resolved.
11. **You complement rf-qa, not replace it** — rf-qa checks structural correctness (section numbers, cross-references, evidence citations, template conformance). You check whether the content makes sense. Don't re-verify section numbering or file existence — focus on whether the content is correct, complete, logical, and appropriately scoped.
```

**FR-CONV.3 insertion semantics:** The "Inherited Structural Verdict" block is to be appended after line 794 (end of file). Critical Rule 11 at file:794 establishes the precondition: rf-qa-qualitative *complements* the structural rf-qa verdict and must not re-verify what rf-qa already did. The inherited verdict block surfaces the structural verdict in-context so the agent can:
- Cite "structural PASS" as inherited context **without** counting it as semantic verification.
- Apply INV-019 Self-Audit to add ≥1 of its own semantic checks beyond the inherited verdict.
- The anti-inflation rule at file:766-772 forbids citing the inherited verdict as evidence for any item.

---

## 7. NO N/A Rule (file:564 + file:93 verbatim)

**File:564** (the Adaptation Guidance header for task-qualitative):

```
### Adaptation Guidance (NO check may be marked N/A — adapt instead)
```

**File:93** (Verification Principle 9 — applies to ALL phases):

```
9. **Ban N/A**: NO CHECK MAY BE MARKED N/A. Every check must be adapted to the document type. If the literal check doesn't apply, reinterpret it for the context and document what the adapted check verified.
```

**Implication for our Phase-6 TDD:**
- When the TDD's `§9 State Management` is genuinely not applicable (the TDD describes a stateless framework convention with no client state), we **must not** omit the section or label it "N/A" without explanation.
- Instead, we must write a brief adapted rationale, e.g. *"N/A — internal framework convention; rf-qa-qualitative orchestrates ephemeral subagent invocations and holds no client-facing state. No state model required."*
- This satisfies both the agent-level Ban N/A rule (file:93) and the task-qualitative Adaptation Guidance table (file:564-582), which provides the literal "Code Task → Doc Task Adaptation" mapping.

---

## 8. Severity Ratings + Verdict Structure

Severity and verdict blocks are repeated in each phase with phase-specific severity examples. The structural pattern is identical:

**Severity tiers** (verbatim from tdd-qualitative file:295-297; pattern repeats across phases):

```
- **CRITICAL** — Design that would cause implementation failures, data loss, or security vulnerabilities (contradictory API contracts, missing migrations, invented requirements, incomplete security model)
- **IMPORTANT** — Design that would cause confusion, rework, or integration problems (vague implementation details, inconsistent data models, unclear component boundaries)
- **MINOR** — Design that is correct but could be improved (missing rationale for choices, implicit assumptions that should be explicit)
```

**Verdict block** (verbatim, identical across phases; e.g. tdd at file:305-308):

```
- **PASS** — All checks pass, no issues of any severity.
- **FAIL** — Any issues exist (CRITICAL, IMPORTANT, or MINOR). List each with specific remediation. ALL issues must be resolved before proceeding — no severity level is exempt.
```

**Severity floor** (file:789 — Critical Rule 6): *"Contradictions are always IMPORTANT or CRITICAL — If two sections say different things about the same topic, that's never minor. Always surface contradictions."* Per-phase severity examples vary (prd at file:179-181; report at file:225-227 — implicit; tech-ref at file:359-361; ops-guide at file:427-429; readme at file:491-493; task-qualitative at file:586-588).

**No exemption for MINOR:** every verdict block explicitly states "no severity level is exempt." A MINOR finding produces FAIL.

**Confidence Gate Protocol** (file:735-778) gates the verdict computationally:
- confidence = VERIFIED / (TOTAL - UNVERIFIABLE) × 100 (file:752)
- PASS requires confidence ≥ 95% AND UNCHECKED == 0 (file:755)
- Maximum 3 additional verification rounds (file:756); after 3 rounds still <95%: verdict is FAIL with documented limitations (file:757)
- Mandatory report fields (file:761-764): `Confidence:` line with raw counts; `Tool engagement:` line counting Read/Grep/Glob/Bash; every UNCHECKED and UNVERIFIABLE item listed.

---

## 9. Tool Engagement Minimum + Prohibited Behaviors (file:735-778 — covers PRD's 580-792 range across the spec)

**Prohibited Behaviors block** (verbatim file:766-772, quoted in full in Section 3 above). Six "NEVER" bullets enforce computed-not-felt confidence, raw-numbers reporting, tool-output evidence for VERIFIED claims, the reliance-vs-verification distinction, the threshold-or-no-PASS rule, and the no-inflation rule.

**Tool Engagement Minimum** (verbatim file:774-775):

```
### Tool Engagement Minimum
If your total (Read + Grep + Glob) calls < TOTAL checklist items, the review is automatically suspect. You cannot have verified more items than you made tool calls. Flag this in your report.
```

This is the floor that FR-CONV.4 must respect: adding the Five Adversarial Axes overlay multiplies *axes*, not *checks*. The TOTAL stays at 15 for task-qualitative; each axis labels groups of checks. Tool calls must remain ≥ TOTAL checklist items, not ≥ (TOTAL × number of axes).

**Qualitative Adaptation** (verbatim file:777-778):

```
### Qualitative Adaptation
For qualitative checks that involve judgment calls (e.g., "is the audience appropriate?"), the VERIFIED marker requires citing what specific content was read and what conclusion was drawn. The judgment itself counts as verified if the evidence trail is documented.
```

Adversarial Stance anchor (file:84): "Begin from adversarial position. Assume errors exist. … A review that finds 0 issues should be treated with suspicion, not satisfaction."

NO LENIENCY (file:92, Verification Principle 8): "Do not give the document the benefit of the doubt. If something is 'close enough' or 'probably fine' — it FAILS."

Exhaustive verification (file:94, Verification Principle 10): "Verify EVERY factual claim against actual source code using tools. No sampling, no spot-checking, no representative checks."

---

## 10. TDD-Qualitative Phase Detail (file:244-308) — verbatim

This is THE phase that will validate the TDD produced in Phase 6. Every check is quoted below verbatim.

**Phase metadata** (file:244-253):
- **When** (file:246): "After rf-qa structural verification passes (report-validation phase), before presenting to user."
- **Purpose** (file:247): "Verify the TDD makes sense as a technical design document — architecture decisions are sound, API contracts are consistent, implementation details are specific enough to code from, and the design faithfully translates PRD requirements without inventing or losing any."
- **Input** (file:251): "The assembled TDD + the TDD template (for section expectations) + the source PRD (if referenced)"
- **Read protocol** (file:253): "Read the entire document end to end. Then apply the checklist below."

**Checklist (14 items) — verbatim (file:255-291):**

```
#### Checklist (14 items)

**PRD-to-TDD Fidelity**

1. **Architecture decisions match PRD requirements** — Every functional requirement in the PRD should have a corresponding architectural component or design decision. If the PRD says "support offline mode," there must be an offline architecture somewhere in the TDD. Missing mappings = requirements that won't get built.

2. **No requirements invented that aren't in the PRD** — The TDD should implement what was specified, not add features. If the TDD introduces capabilities not in the PRD (e.g., a caching layer the PRD never mentioned), flag it. The TDD can propose technical approaches, but not new product requirements.

3. **No PRD content repeated verbatim** — The TDD should translate product requirements into engineering specifications, not copy-paste PRD sections. If a TDD section reads identically to a PRD section, it hasn't done its job. User stories belong in PRDs; data models and API contracts belong in TDDs.

4. **Performance targets match PRD targets** — If the PRD specifies "API response < 200ms at p95" and the TDD says "< 500ms," that's a contradiction. Check all quantitative targets across both documents.

**Internal Consistency**

5. **API contracts are internally consistent** — Request/response schemas in one section must match how they're referenced in other sections. If the auth endpoint returns `{ token, expires_at }` in the API section but the auth flow diagram shows `{ access_token, refresh_token }`, that's a contradiction.

6. **Data models match across ER diagrams, API contracts, and migration plans** — A field that exists in the ER diagram must appear in the API response. A table referenced in the migration plan must exist in the data model. Column types must be consistent across all representations.

7. **Component boundaries are well-defined** — Each component/service should have clear responsibilities. If two components both claim ownership of the same concern (e.g., both "handle user authentication"), that's an architectural ambiguity that will cause integration conflicts.

8. **Dependency graph is acyclic and complete** — Services that depend on each other should be explicitly documented. Circular dependencies are a red flag. Missing dependencies (service A calls service B but B isn't listed as a dependency) will break deployment ordering.

**Specificity and Actionability**

9. **Implementation details are specific enough to code from** — A developer reading the TDD should know what to build without guessing. "Use a queue for async processing" is too vague. "Use Redis Streams with consumer groups, 3 consumers per service instance, ACK after processing" is actionable.

10. **Error handling is specified, not hand-waved** — Each API endpoint and component interaction should define what happens on failure. "Handle errors gracefully" = FAIL. "Return 409 Conflict with retry-after header when optimistic lock fails" = PASS.

11. **Migration plan covers data and schema** — If the TDD changes data models, there must be a migration strategy that addresses: schema changes (ALTER TABLE), data backfill, rollback procedures, and zero-downtime requirements.

**Red Flags**

12. **Technology choices are justified** — If the TDD introduces a new technology (database, framework, library), there should be rationale. Unjustified technology additions create maintenance burden and onboarding friction.

13. **Scale assumptions are explicit** — If the design assumes "low traffic" or "eventually consistent is fine," those assumptions must be stated with thresholds. What happens when traffic exceeds the assumed level?

14. **Security model is complete** — Authentication, authorization, data encryption (at rest and in transit), input validation, and secrets management should all be addressed. Missing security sections in a TDD = security holes in the implementation.
```

**TDD-qualitative Severity Ratings** (file:295-297):

```
- **CRITICAL** — Design that would cause implementation failures, data loss, or security vulnerabilities (contradictory API contracts, missing migrations, invented requirements, incomplete security model)
- **IMPORTANT** — Design that would cause confusion, rework, or integration problems (vague implementation details, inconsistent data models, unclear component boundaries)
- **MINOR** — Design that is correct but could be improved (missing rationale for choices, implicit assumptions that should be explicit)
```

**Self-Audit** (file:299-303 — identical pattern from Section 2).

**Verdict** (file:305-308 — identical pattern from Section 8).

**Implication for Phase-6 TDD authoring:** to satisfy this gate, the TDD must (per item):

1. Trace every PRD FR/NFR to a §3 (architecture) or §4 (components) decision — fidelity matrix.
2. Not invent FRs absent from the PRD (FR-CONV.* IDs must match PRD).
3. Translate, not copy — TDD prose must be engineering-grade, not PRD prose.
4. Match every quantitative PRD target (this matters since FR-CONV.* may carry SLO-style thresholds).
5-6. Internal API/data-model consistency (item 6 has limited applicability to this framework-doc TDD).
7. Distinct ownership per component (e.g. rf-qa-qualitative agent vs. orchestrator).
8. Acyclic dependency graph (agent → template → orchestrator).
9. Specificity — checklist insertion points named with file:line.
10. Error handling — what happens when the inherited verdict block is absent or malformed.
11. Migration plan — relevant for changes to the agent file (versioned diff strategy).
12. Tech choices justified — md format, line-anchored inserts.
13. Scale assumptions — token budgets, partition counts.
14. Security — N/A adapted: framework convention, no auth surface; explicit rationale required (per Section 7).

---

## 11. Gaps and Questions

1. **PRD line-range drift for the Inherited Verdict insertion site.** PRD asserts "790-798" but the file ends at 794. The TDD must specify exact insertion line(s) — likely either replacing file:794 or appending a new section after file:794. CODE-CONTRADICTED: file:794 (last line) confirmed via `wc -l` (794) and Read.
2. **No existing axis taxonomy in the agent file.** FR-CONV.4's "Five Adversarial Axes" are not defined in `rf-qa-qualitative.md`. The TDD must specify the five axes themselves (likely defined elsewhere — possibly source PRD or a sibling spec) and how each maps onto the 15 task-qualitative checks.
3. **Output Format block is shared across all 8 phases (file:675-714).** Adding an `Axis` column to the Items Reviewed table affects every phase, not just task-qualitative. The TDD must clarify whether the Axis column is universal (filled "N/A" for non-task phases — but the Ban-N/A rule at file:93 would then apply) or conditional (task-qualitative only). This is a NON-TRIVIAL design decision.
4. **Confidence Gate's TOTAL definition under axis overlay.** Tool Engagement Minimum (file:774-775) uses "TOTAL checklist items." With 5 axes overlaid on 15 items, does TOTAL stay 15 (per Section 9 above), or does the overlay change the count? The TDD must lock this down.
5. **doc-qualitative (file:607-634) inherits no specialised axis overlay.** FR-CONV.4's scope (task-qualitative only? all phases?) must be clarified in the TDD.
6. **Inherited Structural Verdict block schema is undefined here.** The agent file does not currently know what an inherited verdict block looks like. The TDD must define the schema (fields, parser, validation).

---

## 12. Stale Documentation Found

| Claim | Evidence | Tag |
|------|----------|-----|
| Anti-inflation rule at lines 766-775 (PRD assertion) | `sed -n '766,780p'` confirms Prohibited Behaviors header at file:766, anti-inflation bullet at file:772 | CODE-VERIFIED |
| Inherited Structural Verdict insertion site at lines 790-798 (PRD) | `wc -l` reports 794 lines; file:794 is the last line. The 790-798 range overshoots by 4 lines | CODE-CONTRADICTED — file ends at 794 |
| 15-item Task-Qualitative checklist at lines 527-583 | Read confirms `#### Checklist (15 items)` at file:527, items 1-15 at file:531-562, Adaptation Guidance table at file:564-582 | CODE-VERIFIED |
| Items Reviewed Table at lines 675-714 | Read confirms `## Output Format (All Phases)` opens at file:675, Items Reviewed at file:689-693, closing fence at file:714 | CODE-VERIFIED |
| NO N/A rule at line 564 | Read confirms `### Adaptation Guidance (NO check may be marked N/A — adapt instead)` at file:564 | CODE-VERIFIED |
| NO N/A also enforced agent-wide at file:93 | Read confirms Verification Principle 9 "Ban N/A" at file:93 | CODE-VERIFIED — broader scope than PRD's single-line citation |
| Self-Audit "≥1 semantic check beyond inherited PASS" wording (INV-019) | The agent file does NOT contain the phrase "≥1 semantic check beyond inherited PASS"; the operational basis is the Self-Audit questions at file:185-187 (and parallels) plus Prohibited Behaviors at file:769-770 | UNVERIFIED — wording is derived, not literal |
| Severity floor at line 789 | Read confirms Critical Rule 6 (Contradictions always IMPORTANT/CRITICAL) at file:789 | CODE-VERIFIED |
| Inherited Structural Verdict block insertion site at line 794 | file:794 is Critical Rule 11; insertion must go after this line OR replace the Critical Rules trailer | CODE-VERIFIED (line 794 is real); insertion semantics UNVERIFIED in current source |
| FR-CONV.6 DNSP emission edit site at lines 72-78 | Read confirms file:72-78 is "Orchestrator Responsibilities" block under Parallel Partitioning. DNSP is NOT mentioned in this range or anywhere in the agent file | UNVERIFIED — no DNSP marker found; FR-CONV.6 edit must introduce the concept, not modify an existing one. (Bash grep would confirm; not run.) |
| Adversarial stance at lines 82-99 (Verification Principles) | Read confirms `## Verification Principles` at file:82, 12 principles numbered 0-11 at file:84-95. Adversarial stance is Principle 0 at file:84 | CODE-VERIFIED |

---

## 13. Summary

The `rf-qa-qualitative` agent (794 lines) defines **8 QA phases** (7 specialised + 1 fallback) each with an identical scaffold: phase trigger, input contract, sized checklist, severity tiers, mandatory Self-Audit, verdict block. The **tdd-qualitative phase (file:244-308) is the gate our Phase-6 TDD must pass**, with a **14-item checklist** structured as PRD-to-TDD Fidelity (1-4), Internal Consistency (5-8), Specificity (9-11), and Red Flags (12-14). The **task-qualitative phase (file:508-603) is the FR-CONV.4 overlay insertion site** — its **15-item body at file:527-562 is immutable**; only a "Five Adversarial Axes" header is to be added before it, with the Items Reviewed table at file:689-693 extended by an `Axis` column. The **anti-inflation rule and Prohibited Behaviors at file:766-772** are the FR-CONV.3 negative-criterion floor — INV-019's "≥1 semantic check beyond inherited PASS" is operationalized by the mandatory Self-Audit block (file:183-187 pattern, repeated in every phase) which forces the agent to count its OWN factual verifications and answer "if 0 issues, why trust this?"; the Inherited Structural Verdict block to be appended at file:794 must be additive and must not license citation of the inherited verdict as evidence. The **NO N/A rule (file:564 task-specific + file:93 agent-wide)** forbids skipping inapplicable checks — when our TDD's §9 State Management is non-applicable, an adapted rationale (e.g. "internal framework convention, no client state") is mandatory rather than omission.

---

**Status:** Complete

