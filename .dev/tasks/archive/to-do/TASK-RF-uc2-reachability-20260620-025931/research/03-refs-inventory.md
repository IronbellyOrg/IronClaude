# R3 — Integration Points + Doc Cross-Validator (refs/ inventory)

Status: Complete
Date: 2026-06-20
Researcher: R3 of 5 (Track 1)
Scope: `src/superclaude/skills/sc-reflect-protocol/refs/` — reviewer-spec.md, deviation-taxonomy.md, coverage-mapping.md, grader-extensions.md

---

## 1. reviewer-spec.md (10,294 bytes, 105 lines)

**File:** `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md`

### The "exactly three sections" invariant [CODE-VERIFIED]

The invariant declaration is at **reviewer-spec.md:23**:
> "A reviewer brief MUST contain exactly these three sections, in this order:"

The three top-level sections (verbatim, as `####` H4 headings in the ref that DOCUMENT the brief's H2 section names):

1. **`## T1 card excerpt`** — heading at **reviewer-spec.md:25**.
2. **`## Grounding hunks`** — heading at **reviewer-spec.md:31**.
3. **`## Coverage slice`** — heading at **reviewer-spec.md:49**.

NOTE on heading depth: in the ref the three section names are written as `#### \`## X\`` (lines 25, 31, 49) — the ref uses H4 to DOCUMENT a section whose name in the actual brief file is the H2 string (e.g. `## T1 card excerpt`). The invariant is about the brief's H2 sections, named verbatim above.

**TDD-claim verification:** The TDD asserted the invariant "at lines 23, 43, 45, 47."
- Line **23** = the invariant sentence itself. [CODE-VERIFIED — exact match]
- Lines **43, 45, 47** = NOT the section headings; they are the three "...the 'exactly three sections' invariant is unchanged." reassertion sentences inside the FR-4 (line 43), FR-RV3-MED.1 (line 45), and D13 (line 47) grounding-hunk entries. [CODE-VERIFIED — these lines reassert the invariant but are NOT section-heading lines]
- The actual section-HEADING lines are **25 / 31 / 49**, NOT 43/45/47. Builder must use 25/31/49 for the three section names and 23 for the invariant statement.

### `## Grounding hunks` H2 heading line [CODE-VERIFIED]

`## Grounding hunks` documented at **reviewer-spec.md:31**. Its shape description (H2 + one H3 per hunk, H3 = `file:line-range` ref, H3 body = language-tagged fenced block) is at **lines 33–37**.

### Existing FR-4 verify-log routing pattern — THE MODEL FR-RSR.9 MIRRORS [CODE-VERIFIED]

**reviewer-spec.md:43** is the canonical model. Text:
> "**FR-4 verification-results hunk.** When §6.1 step 5.5 ran the verification triangle, a grounding-hunk entry carrying the artifact-path ref `<output>/verify-logs/invocations.yaml` ... is injected into this `## Grounding hunks` block for the **`qa`-persona** reviewer (persona-filtered — the qa reviewer owns the coverage/acceptance/verification surface). The artifact ref is preserved verbatim so the Wave-5 evidence-validator can re-Read it. This is an entry under the existing `## Grounding hunks` section — NOT a fourth brief section; the 'exactly three sections' invariant is unchanged."

Pattern anatomy (what FR-RSR.9 must copy):
- A bolded `**FR-N name.**` entry/paragraph placed AFTER line 47 (D13, the last existing entry) and BEFORE line 49 (`#### \`## Coverage slice\``).
- Carries an **artifact-path ref** (`<output>/...yaml`) — verbatim-preserved for the Wave-5 evidence-validator re-Read.
- **Persona-filtered** to a named reviewer persona.
- Explicit reassertion: "...an entry under the existing `## Grounding hunks` section — NOT a fourth brief section; the 'exactly three sections' invariant is unchanged."

Two sibling precedents already follow this exact template:
- **FR-RV3-MED.1 hierarchy-slice hunk** at **reviewer-spec.md:45** — artifact `<output>/artifacts/hierarchy-slice.yaml`, persona-filtered to **`analyzer`/`architect`**.
- **D13 spec-body hunks (UC-1)** at **reviewer-spec.md:47** — persona-filtered to **`qa`**.

So the builder has THREE existing exemplars (43, 45, 47). FR-RSR.9 becomes the fourth, inserted between line 47 and line 49.

### qa-persona reference [CODE-VERIFIED]

- `qa` owns coverage/acceptance: **line 27** ("the `qa` reviewer receives the coverage / acceptance section"), reinforced at **line 43** and **line 47**.
- Reviewer rotation table: `qa` is persona #2 in all three rows (N=2, N=3 default, N=3 enterprise) at **lines 84–86** — present in EVERY composition, so it is the most reliable persona target for an FR-RSR.9 persona-filtered entry.

### What BREAKS the three-section invariant [CODE-VERIFIED via the ref's own repeated guardrails]

Breaks if FR-RSR.9 is authored as a **4th `## ` H2 section** in the brief (e.g. `## Reachability hunks` as a peer). The ref states three times (lines 43, 45, 47) the safe pattern is "an entry under the existing `## Grounding hunks` section — NOT a fourth brief section."
- SAFE: add FR-RSR.9 as a bolded `**FR-RSR.9 ...**` artifact-ref entry between line 47 and line 49, inside the Grounding hunks subsection, persona-filtered (qa is the natural target given runtime-surface/coverage framing).
- BREAKS: any new `#### \`## <name>\`` peer heading, or prose introducing a 4th `## ` section into the brief shape — that makes four `## ` sections and violates line 23.

### Contract emission [CODE-VERIFIED]
- `reviewer_briefs_materialized: <N>` emitted at Step 3B.0 completion — **line 66**. The FR-4 entry (line 43) notes this contract emission is UNCHANGED by a grounding-hunk entry; FR-RSR.9 must likewise leave this field unchanged.

---

## 2. deviation-taxonomy.md (10,496 bytes, 139 lines)

**File:** `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md`

### Overall structure — the 4 classes [CODE-VERIFIED]

The taxonomy is **4 categories**, asserted at **deviation-taxonomy.md:5** ("The taxonomy is **4 categories**") and reasserted at **line 117** ("The taxonomy is **4 categories**, not 5. There is no `unknown` deviation class."). The four `## ` class sections:

1. **`## Authorized`** — **line 26** (def at 28; remediation "None. Document in the report. No Tier 3 task." at 38).
2. **`## Necessary`** — **line 40** (def at 42).
3. **`## Drift`** — **line 56** (def at 58; "A silent change not in the original spec/tasklist with no inline rationale").
4. **`## Regression`** — **line 72** (def at 73; "A change that *contradicts* an acceptance criterion ... or a previously-passing test").

Supporting sections: `## Aggregation` (line 11), `## Classification precedence` (line 85, ordering `Regression > Drift > Necessary > Authorized` at line 89), `## Verification exit-code → deviation-class mapping (FR-4)` (line 99), `## Grounding-gaps parallel artifact` (line 115).

Each class carries: definition, detection signals, gold-standard reference, default remediation (stated at **line 9**).

### Where the §10.9 UNREACHED-by-evidence cross-reference should be inserted [CODE-VERIFIED context; insertion point is an analysis recommendation]

The contradiction-anchored framing the feature works around lives in **`## Drift`** and **`## Regression`** — both are defined by mapping/contradiction relations to the spec, NOT by runtime reachability:
- Drift detection signal at **line 62**: "Diff hunk does NOT map to any tasklist item." — this is the "missing sink" / unmapped framing.
- Regression detection at **lines 76–80**: contradiction of an acceptance criterion OR a previously-passing test (verification triangle), the contradiction anchor.

The new SKILL.md §10.9 "UNREACHED-by-evidence mapping" is a runtime-surface-reachability concept that is ADJACENT to but distinct from these. A cross-reference should be inserted so the taxonomy explicitly points to §10.9 as the home of the reachability dimension that the 4 classes do NOT cover. The most defensible anchor is the **`## Grounding-gaps parallel artifact`** section (**lines 115–138**), because:
- It already establishes the "this is NOT a 5th deviation class, it routes to a parallel artifact" pattern (line 117: "The taxonomy is **4 categories**, not 5").
- An UNREACHED-by-evidence finding is structurally a *grounding/evidence gap* (the evidence sink — a reaching runtime call path — is missing), which is exactly the "missing sink" framing this section already encodes via `grounding-gaps.yaml` (line 119: "cannot be classified due to insufficient evidence ... writes a row to `<output>/grounding-gaps.yaml`").
- Alternative/secondary anchor: a one-line cross-ref under `## Drift` (line 56) clarifying that "unmapped ≠ unreached; runtime-surface reachability escalation is governed by SKILL.md §10.9."

The cross-reference is **contradiction-anchored via the "missing sink" framing**: an UNREACHED requirement is one whose runtime evidence sink (the reaching call path) is absent — a missing sink, parallel to the missing tasklist-mapping in Drift. [CODE-VERIFIED that the missing-sink/unmapped framing is present at lines 62, 119; the §10.9 cross-ref is NEW and must be authored.]

### Lockstep-with-SKILL.md-§10 requirement [CODE-VERIFIED]

The taxonomy is explicitly slaved to spec §10:
- **line 121**: "**Required fields (byte-exact schema from spec §10.6):**" — the grounding-gaps schema is byte-exact to spec §10.6.
- **line 138**: "The 5th deviation category was explicitly rejected in §17.7 Kill List."
- **line 101**: exit-code mapping "feeds the precedence union ... by evidence."
The deviation-taxonomy.md must stay in lockstep with SKILL.md §10; any §10.9 addition in SKILL.md must be mirrored by the cross-reference here, and the "4 categories, not 5" invariant (lines 5, 117) must NOT be broken (UNREACHED-by-evidence is NOT a 5th class — it routes to grounding-gaps, same as evidence-insufficient findings per line 5).

---

## 3. coverage-mapping.md (14,080 bytes, 261 lines) — "FACT 3"

**File:** `src/superclaude/skills/sc-reflect-protocol/refs/coverage-mapping.md`

### CONFIRMED [CODE-VERIFIED]: coverage-mapping proves requirement→task/diff MAPPING, NOT reachability

The ref's own scope statement at **coverage-mapping.md:1–8**: it "defines the deterministic algorithm sc-reflect uses to compute spec-to-tasklist coverage" producing three contract fields: **`coverage matrix`, `coverage_pct`, `unmapped_requirements`** (lines 5–6). This is a MAPPING value space (does requirement R map to a tasklist item / diff hunk), NOT a reachability value space (is a runtime surface reached by an execution path).

**The value space is mapping-only [CODE-VERIFIED]:**
- `coverage_pct = matched_parsed_count / parsed_total_count` — **line 71** (a MATCH ratio).
- `unmapped_requirements = [parsed ids where match_method == none]` — **line 73** (UNMATCHED, i.e. no tasklist mapping).
- coverage matrix = per-requirement match records `{requirement_id, matched_task_ids, match_method: exact|fuzzy|containment|none, source}` — **lines 59–60, 61–66**.
- The matcher is pure string arithmetic (exact/fuzzy ID equality + containment), **lines 51–58, 89–124** — "no LLM in any matching path" (line 58).

**Reachability is NOT in the value space [CODE-VERIFIED by absence]:** Searched the full ref — the matching loop value space is exact|fuzzy|containment|none ID/quote matching only. There is NO notion of a runtime call path, reachable surface, or execution-trace sink anywhere in the algorithm. `S_dev_density` (lines 156–212) is a ratio of **unmapped** artifacts to total artifacts — still a mapping quantity, NOT reachability. This is exactly "fact 3" the feature works around: coverage-mapping answers "is requirement R mapped to a task/diff?" and structurally CANNOT answer "is the changed runtime surface actually reached?"

**The 5-stage stage list (cite) [CODE-VERIFIED] — coverage-mapping.md:19, body lines 21–80:**
1. **Parse spec (two-pass, SKILL.md Step 1B.0)** — line 21 (Pass 1 regex authoritative line 22; Pass 2 inference line 32).
2. **Parse tasklist** — line 46.
3. **Run bipartite matching** — line 50.
4. **Emit coverage matrix** — line 61.
5. **Compute summary fields (contract 1.5.0, additive)** — line 67.

None of the 5 stages computes reachability — all five are parse/match/emit/summarize over ID and quote MAPPING. The feature must add reachability as a NEW dimension outside this algorithm (SKILL.md §10.9), not as a modification to coverage_pct/unmapped_requirements (which retain pre-D13 mapping semantics, line 71/73 and the backward-compat invariant in grader-extensions.md line 311).

---

## 4. grader-extensions.md (19,333 bytes, 312 lines)

**File:** `src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md`

### CONFIRMED [CODE-VERIFIED]: this ref DEFINES the assertion types the eval FR uses

The ref specifies assertion types `grader.py` must implement BEYOND the 8 baseline types inherited from sc-brainstorm (**line 3**). Baseline 8 enumerated at **line 9**: `file_exists`, `frontmatter_field`, `section_present`, `section_enumerated`, `yaml_field`, `yaml_field_min`, `yaml_substring`, `dir_count`.

Per-assertion-type confirmation requested by the task:

- **`regex_absent`** [CODE-VERIFIED — DEFINED HERE]
  - Overview-table row #3 at **grader-extensions.md:15** ("Pattern absence (false clean-pass detection)").
  - Dedicated section `## regex_absent` at **line 83**; semantics at **lines 88–89** ("Inverse of `regex_present`. Used for false-clean-pass detection: e.g., assert that a regression-laden report does NOT contain the phrase `verdict: clean_pass`."); `check_regex_absent` impl sketch at **lines 91–102**.
  - This is a TRULY-NEW type (not in the baseline 8).

- **`yaml_field`** [CODE-VERIFIED — BASELINE, NOT newly defined here]
  - Listed in the BASELINE 8 at **grader-extensions.md:9** ("`yaml_field`"). It is INHERITED from sc-brainstorm's grader.py, NOT defined in this ref. The ref uses `yaml_field` in its D13 fixture contracts (lines 307, 308, 309) but does not re-define it. IMPORTANT for the builder: an FR using `yaml_field` relies on the inherited baseline implementation; only the new types below are defined in this ref.

- **`falsifier_skeleton_present`** [CODE-VERIFIED — DEFINED HERE]
  - Overview-table row #10 at **grader-extensions.md:22** ("`falsifier-suite/<case>.yaml` parses + meets skeleton-OR-active contract").
  - Dedicated section `## falsifier_skeleton_present` at **line 257**; semantics + §12.5 two-state contract at **lines 263–268** (`status: skeleton-pending-iteration-3-fixture` → pass; `status: active` AND `convergence_score < 0.75 OR verdict == regression_present` → pass; any other status fails); `check_falsifier_skeleton_present` impl at **lines 270–297** with `CANONICAL_FIELDS = {"id","type","fixture","expected","assertion"}` at line 274.

- **`yaml_field_min`** [CODE-VERIFIED — BASELINE, NOT newly defined here]
  - Listed in the BASELINE 8 at **grader-extensions.md:9** ("`yaml_field_min`"). Inherited from sc-brainstorm; NOT defined in this ref. Same caveat as `yaml_field`: an FR using `yaml_field_min` relies on the inherited baseline implementation.

### Full new-type roster (for builder reference) [CODE-VERIFIED]
Overview table at **lines 11–22**; the ref claims **9 truly-new types** (line 24 reconciliation: `regex_present`+`regex_absent` counted as one §12.4 bullet row). The 10 dedicated sections:
1. `citation_resolves` — line 26
2. `regex_present` — line 62
3. `regex_absent` — line 83
4. `yaml_list_contains` — line 104
5. `matrix_covers_items` — line 134
6. `checkpoint_logged` — line 161
7. `deviation_class_matches` — line 192 (canonical 4-class set `authorized/necessary/drift/regression`, line 198)
8. `path_exists` — line 216
9. `path_does_not_exist` — line 237
10. `falsifier_skeleton_present` — line 257

Wiring into `check_assertion` dispatcher: **lines 299–301** (append `elif a_type == "<name>"` branches after the 8 baseline; `import yaml` PyYAML required, baseline `parse_yaml_simple` insufficient for nested YAML — line 5, 301).

D13 coverage-hardening fixtures (3 fixtures: `sparse-labeled-spec`, `fabricated-inference`, `range-notation`) at **lines 303–311** — these demonstrate the assertion-type usage patterns (`yaml_field`, `matrix_covers_items`, `section_present`, `citation_resolves`, `regex_present`, `regex_absent`) the FR-RSR eval fixtures should mirror.

### Builder takeaway for the eval FR
- `regex_absent` and `falsifier_skeleton_present` are DEFINED in this ref (the FR can cite their semantics/impl directly: lines 83–102 and 257–297).
- `yaml_field` and `yaml_field_min` are BASELINE (inherited) — the FR uses them but they are NOT defined here; do NOT instruct the builder to "add" them to grader-extensions.md.
- If FR-RSR needs a NEW reachability assertion type (e.g. a reachability-specific YAML field check), it would be authored as an 11th dedicated section following the exact `## <name>` + semantics + `check_<name>(assertion, base_dir) -> tuple[bool,str]` impl-sketch template (lines 40, 73, 94, etc.) and registered in the dispatcher per lines 299–301. Whether a new type is needed vs. reuse of `yaml_field`/`regex_absent` is an R4/grader.py-code question (out of R3 scope).

---

## Summary for the builder (edit-instruction anchors)

| Ref file | FR-RSR touch | Exact anchor | Invariant guard |
|----------|--------------|--------------|-----------------|
| reviewer-spec.md | FR-RSR.9 grounding-hunk entry (NOT a 4th section) | Insert bolded `**FR-RSR.9 ...**` artifact-ref entry between **line 47** (D13 entry) and **line 49** (`## Coverage slice`), persona-filtered (qa). Mirror the FR-4 template at **line 43**. | "Exactly three sections" invariant at **line 23**; section headings at **25/31/49**. TDD's "43,45,47" are the reassertion sentences, NOT headings. Adding a 4th `## ` H2 BREAKS it. |
| deviation-taxonomy.md | Cross-ref to SKILL.md §10.9 UNREACHED-by-evidence | Insert in `## Grounding-gaps parallel artifact` (**lines 115–138**, primary) and/or a one-line note under `## Drift` (**line 56**). Contradiction-anchored "missing sink" framing (Drift unmapped at **line 62**; grounding-gap insufficient-evidence at **line 119**). | "4 categories, not 5" at **lines 5, 117**; byte-exact §10.6 schema at **line 121**. UNREACHED-by-evidence is NOT a 5th class — routes to grounding-gaps. Must stay lockstep with SKILL.md §10. |
| coverage-mapping.md | NONE (this is FACT 3 — the thing the feature works AROUND) | Value space = mapping only: `coverage_pct` (**line 71**), `unmapped_requirements` (**line 73**), match matrix (**lines 59–66**). 5-stage list at **line 19** (stages 1–5 at lines 21/46/50/61/67). | Reachability is NOT in the value space (verified by absence). Do NOT modify coverage_pct/unmapped semantics — they retain pre-D13 mapping meaning. |
| grader-extensions.md | DEFINES assertion types the eval FR uses | `regex_absent` DEFINED at **line 83** (impl 91–102); `falsifier_skeleton_present` DEFINED at **line 257** (impl 270–297). `yaml_field` + `yaml_field_min` are BASELINE (**line 9**) — inherited, NOT defined here. | New types follow `## <name>` + `check_<name>(assertion, base_dir)->tuple[bool,str]` template + dispatcher registration (**lines 299–301**). |

### Top correction the builder must apply
The TDD's reviewer-spec.md "three-section invariant at lines 23, 43, 45, 47" is IMPRECISE: **line 23** is the invariant; **lines 43/45/47** are the FR-4/FR-RV3-MED.1/D13 "invariant unchanged" REASSERTION sentences (the exemplar entries to mirror), NOT the section headings. The actual section-heading lines are **25 / 31 / 49**. FR-RSR.9 mirrors the line-43 FR-4 pattern and inserts between line 47 and line 49.
