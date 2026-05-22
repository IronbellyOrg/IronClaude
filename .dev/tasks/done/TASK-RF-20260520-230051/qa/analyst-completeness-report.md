# Research Completeness Verification

**Topic:** PR #64 remediation Track 1 (M1/M2/M4 fixes on feature/sc-auggie-review-protocol)
**Date:** 2026-05-20
**Files analyzed:** 3
**Depth tier:** Quick
**Analyst mode:** Single instance (no partition)

---

## Verdict (preliminary — see end-of-file)

Pending checklist application below.

---

## Files Inventory

| # | File | Status (frontmatter) | Lines | Scope |
|---|------|----------------------|-------|-------|
| 01 | research/01-target-files-inventory.md | Complete | 241 | File Inventory + Patterns & Conventions for the 3 target files (offer-pr-review.sh, SKILL.md, evals.json) |
| 02 | research/02-template-and-eval-dsl.md | Complete | 484 | MDTM Template 02 elements + prior exemplars + eval-harness DSL design |
| 03 | research/03-verification-and-sync.md | Complete | 368 | Makefile, pre-commit, CI, per-file verification one-liners, full post-edit chain |

All three files declare `Status: Complete` and a 2026-05-20 date matching today.

---

## Checklist Application

### Criterion 1 — Source files identified with paths AND before/after text for each fix

**PASS.**

Evidence:

- File 01 §"File 1" gives absolute path (`/config/workspace/IronClaude/src/superclaude/hooks/scripts/offer-pr-review.sh`), 70-line total, and provides VERBATIM current L15-L24 (the "Current state of lines being modified" block) AND a proposed L15-L26 after the fix. Both before and after snippets are byte-explicit and contain the exact one-liner `case "$INPUT" in *'"command"'*'gh'*'pr'*'create'*) ;; *) exit 0;; esac` with its two-line comment header.
- File 01 §"File 2" gives absolute path for `sc-auggie-review-protocol/SKILL.md`, 362-line total, and quotes VERBATIM L163-L170 (the current blockquote bullets) and provides an exact replacement block for L166-L167 (consolidated bullet with fenced bash pipeline). The pipeline string `tail -n +2 auggie-raw.json | jq -r '.result' | sed -n '/^\`\`\`json$/,/^\`\`\`$/p' | sed '1d;$d' | jq '.'` matches the user's mandated string verbatim.
- File 01 §"File 3" gives absolute path for `evals.json`, 29-line total, identifies L10/L18/L26 as the three empty `"assertions": []` arrays, and provides full per-scenario replacement JSON for all three (with `file_exists`, `report_contains`, `no_hallucinated_citations`).

All three fixes have both a before-snippet (verbatim, line-numbered) and an after-snippet (proposed, paste-ready). Builder has byte-exact strings to embed in checklist items per B1 self-containment.

---

### Criterion 2 — Output paths and formats clear (task file location, post-edit verification commands)

**PASS.**

Evidence:

- File 02 §1.1 lists the task `id: "TASK-RF-20260520-230051"` matching the spawn directory; the task file path is implied at `.dev/tasks/to-do/TASK-RF-20260520-230051/TASK-RF-20260520-230051.md` (standard MDTM location, consistent with prior exemplar `TASK-RF-20260517-183817/TASK-RF-20260517-183817.md`).
- File 02 §5 explicitly tells the builder to pre-create `phase-outputs/{discovery,test-results,reviews,plans,reports}` subdirs.
- File 03 §5 provides per-file verification one-liners (`bash -n`, `shellcheck --severity=warning`, `jq -e ...`, `grep -F`, `diff src/ .claude/`) with copy-paste commands. File 03 §6 supplies the full sequential post-edit chain (8 steps from per-file gates through `pre-commit run --files`).

Minor caveat (not a fail): File 02 does not state the literal output filename, only `id`. The convention from the exemplar (`<task-id>/<task-id>.md`) is well-established in this repo so the builder cannot reasonably miss it, but the report would be more bullet-proof if it explicitly said "Write task file to `${TASK_DIR}/TASK-RF-20260520-230051.md`". Flagging as a minor caveat, not a gap.

---

### Criterion 3 — Logical breakdown of phases/steps present (per-fix phase + sync/validate phase)

**PASS.**

Evidence:

- File 02 §1.2 enumerates the mandatory section order from Template 02 PART 2 (with line citations to the template at L896, 898-900, 902-908, 912-944, 1014, 1062, 1088, 1096, 1104, 1115, 1125).
- File 02 §2.2 supplies a concrete phase ordering from the recommended exemplar TASK-RF-20260517-183817: Phase 1 (setup) → optional drift-fix → per-file edits → sync → verify → phase-gate QA → post-completion.
- File 02 §5 (builder quick-reference) tells the builder to "Mimic TASK-RF-20260517-183817 phase ordering: setup → optional drift-fix → per-file edits (one item per file) → sync (`make sync-dev`) → verify (`make verify-sync` + `pre-commit run --files <files>`) → phase-gate QA → post-completion."
- File 02 §1.6 explicitly mandates a phase-gate QA item between edits and verify, citing I15 line 599-607.

The per-fix structure is unambiguous: each of the 3 target files becomes its own Phase 2.X checklist item (per A3 granularity, §1.4). The sync/verify is a downstream phase.

---

### Criterion 4 — Patterns and conventions documented with examples (bash style, markdown blockquote, JSON indent)

**PASS.**

Evidence:

- File 01 §"Adjacent patterns to preserve" (under File 1) enumerates 7 bash conventions: `set -u` safety, fail-open `exit 0` pattern, `INPUT="$(cat ...)"` fail-open, comment style (`#` + sentence-case + period + backticks for identifiers), blank-line cadence, no `[[`-regex prefilter, intentional `case` quoting `*'"command"'*`.
- File 01 §"Adjacent patterns to preserve" (under File 2) enumerates 5 markdown blockquote conventions: `>` prefix on every line, `**term**:` bullet marker pattern, code-fenced bash inside blockquote with `>` prefix on fence lines, preservation of L165/L168-L170, surrounding context (the L152-L161 invocation template informs the pipeline example name).
- File 01 §"Adjacent patterns to preserve" (under File 3) enumerates 7 JSON conventions: validity (no trailing comma after last key), 2-space indent (col 8 array elements, col 10 inner keys), inline-per-assertion (matches empty-array inline style), exact marker strings preserving the trailing colon on `# Code Review:`, path values matching `--output-dir` from prompts, `repo_root` default, `files: []` unchanged.

All three "patterns" sections cite specific lines or quote verbatim from the file. Builder has everything needed to preserve style.

---

### Criterion 5 — MDTM template 02 notes present with rule references (A3 granularity, B2 self-containment, mandatory sections)

**PASS — STRONG.**

Evidence:

- File 02 §1.1 enumerates required frontmatter fields with concrete values, citing template lines 1-44.
- File 02 §1.2 enumerates the 7 mandatory body sections in order with line-by-line citations into the template (L896, L898-900, L902-908, L912-944, L1014, L1062, L1088, L1096, L1104, L1115, L1125).
- File 02 §1.3 lists the 6-element checklist item schema (B2.1 through B2.6) with template line citations (L143-148). Includes critical structural rules (B3 L152-154, B5 L175-180, E1 L280/L283, E2 L296/L297, E3 L350).
- File 02 §1.4 quotes A3 (L91-95) verbatim and applies it to PR #64: "each of the three target files gets its own individual checklist item for the edit. Do NOT collapse into a single 'fix all three files' item."
- File 02 §1.5 quotes B1 self-containment (L134-140) and applies: "the literal before-text and after-text for each file MUST be embedded directly in the relevant checklist item."
- File 02 §1.6 quotes I15-I16 (L599-625) — phase-gate requirements.
- File 02 §1.7 cites I18 (L637-646) and CORRECTLY concludes I18 doesn't strictly apply (docs/config edits) — but still mandates `make verify-sync` + `pre-commit` because of CLAUDE.md project rules. Phase named `Verification & Sync` not `Testing & Verification`.
- File 02 §1.8 cites I17 (L626-635) and I13 (L580) for post-completion validation; cites template L1117-1123 for the 4 canonical post-completion items.

Per-rule citation is thorough. The depth tier is "Quick" but this section reaches Standard depth — over-delivery.

Minor adversarial note (not a fail): the report does not include the literal byte-exact text of A3 / B1 / I15 / I17 from the template — only quotations and references. For a Quick-tier task this is acceptable, and a builder can re-read those exact lines via the cited line numbers. Not a gap.

---

### Criterion 6 — Granularity sufficient for per-fix checklist items (each fix gets read + apply + verify items)

**PASS.**

Evidence:

- File 01 provides for each of the 3 files: (a) full path, (b) verbatim current text to read, (c) exact replacement text to apply, (d) adjacent patterns to preserve.
- File 02 §1.3 specifies the 6-element checklist-item schema (context-ref + action + output-spec + verification + evidence-on-failure + completion-gate). A builder can map: "read source lines" → context-ref; "apply replacement" → action + output-spec; "verify pre-commit gates pass" → integrated verification (with File 03 §5 supplying the actual verification commands).
- File 03 §5 supplies per-file verification one-liners that fit cleanly into the integrated-verification clause of each Phase 2.X item.
- File 02 §5 explicitly says "Embed the file:line evidence inline in each per-file checklist item ... DO NOT defer to 'read the research file' — that violates B1 self-containment."

Three fixes × (read + apply + verify) = 9 implied items minimum. The research supplies enough material for each. Granularity is sufficient for A3 compliance.

---

### Criterion 7 — Documentation cross-validation tags (`[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]`) on claims about Makefile, pre-commit, CI

**FAIL (minor severity).**

Evidence:

- File 03 makes many claims about Makefile/pre-commit/CI behaviors with **line-number citations** (e.g., "Makefile:138–143", ".pre-commit-config.yaml:9", ".github/workflows/test.yml line 88"). These citations function like soft `[CODE-VERIFIED]` tags because the researcher inspected the actual files to extract the lines.
- HOWEVER, no claim in File 03 carries the explicit `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]` tags that the analyst checklist asks for.
- File 03 §1 even calls out the venv install copy as "do NOT edit; reinstalled by `uv pip install -e .`" — this is doc-sourced behavior that should be tagged.
- File 03 §3 table claims `markdownlint --fix` is at "line 68" of `.pre-commit-config.yaml` and `shellcheck` is at "line 88" — these are precise line citations but lack a verification tag.
- File 02 §3.3 makes a strong negative claim: "Does any eval-runner code currently read `evals.json` and execute the assertions? **NO.**" — this is a doc/code search claim that strictly should be tagged `[CODE-VERIFIED]` with evidence ("search of `src/` and `scripts/` shows no harness consumes the skill-creator-shape `evals.json`"). Evidence is given but the tag is absent.
- File 02 §3.1 cites the Anthropic mintlify mirror and GitHub URL — external doc claim. No `[UNVERIFIED]` or freshness tag.

**Impact assessment:** the line-number citations are robust enough that a builder/executor can trace any claim back to its source file in seconds. The missing tags are a documentation-hygiene gap, not a content gap. The depth tier is "Quick" which generally relaxes the verification-tag requirement; nonetheless the checklist asks for tags explicitly, so this is flagged as FAIL with **minor severity** (not blocking).

Specific claims that would benefit from explicit tags:

1. File 03 §2.1: hooks loop at Makefile:138–143 — `[CODE-VERIFIED]` (line citation present but tag absent).
2. File 03 §2.2: verify-sync Makefile:166–353 — `[CODE-VERIFIED]`.
3. File 03 §3 table: every pre-commit hook line citation — `[CODE-VERIFIED]`.
4. File 03 §4: every CI line citation — `[CODE-VERIFIED]`.
5. File 02 §3.1 Anthropic skill-creator schema published `type` values (`file_exists`, `custom`) — `[UNVERIFIED]` against the mintlify mirror unless the researcher actually fetched the URL today (depth tier "Quick, no web" suggests they did not).
6. File 02 §3.3 "no eval-runner currently consumes evals.json" — `[CODE-VERIFIED]` (search outcome).

---

### Criterion 8 — Solution research: assertion DSL JSON shape proposed with full schemas for all three assertion types

**PASS — STRONG.**

Evidence:

- File 02 §4.1 supplies a design-rationale paragraph (suitable for the OQ-1 table).
- File 02 §4.2 specifies SCHEMA #1 `file_exists` with required fields table (text, type, path), optional fields table (min_size_bytes, must_be_readable), paste-ready JSON example, and placement example.
- File 02 §4.3 specifies SCHEMA #2 `report_contains` with required fields (text, type, report, markers), optional fields (case_sensitive, markers_mode), AND-vs-OR semantics note, paste-ready JSON.
- File 02 §4.4 specifies SCHEMA #3 `no_hallucinated_citations` with required fields (text, type, report, citation_regex), optional fields (repo_root, allow_external_paths, verify_line_in_range, ignore_patterns), failure-mode behavior, rationale paragraph, paste-ready JSON.
- File 02 §4.5 provides the combined three-assertion block (paste-ready into Phase 2 checklist item).
- File 02 §4.6 provides the resolved OQ-1 wording for the task file's OQ table.
- File 01 §"Exact replacement text" provides per-scenario JSON for all three evals (scenarios 1, 2, 3), each with the three assertion types.

All three assertion types are documented with: human prose rationale, JSON schema, required fields, optional fields, failure-mode semantics, and paste-ready examples. Coverage is complete.

**One adversarial observation — non-blocking contradiction between researchers:**

File 01 uses a **simpler** discriminated-union shape (NO `text` field):

```json
{ "type": "file_exists", "path": "..." }
{ "type": "report_contains", "report": "...", "markers": [...] }
{ "type": "no_hallucinated_citations", "report": "...", "repo_root": "..." }
```

File 02 uses the **Anthropic-canonical** shape with `text` field as the first key:

```json
{ "text": "Output file ... exists ...", "type": "file_exists", "path": "..." }
```

These are inconsistent. File 02 explicitly aligns with the published Anthropic skill-creator schema (where `text` is a canonical field — §3.1 cites the public docs showing `{"text": "...", "type": "file_exists"}`). File 01 omits `text`, which would diverge from the upstream schema.

**Recommendation for builder:** use File 02's shape (with `text` field) because it aligns with the documented Anthropic schema and the file being remediated already follows skill-creator convention. The marker lists ALSO differ:

- File 01 markers: `["# Code Review:", "## Findings", "## Audit"]`
- File 02 markers: `["## Critical Findings", "## High Findings", "## Medium Findings", "## Low Findings", "## Summary"]`

These two marker sets are RADICALLY different. The builder MUST resolve this before drafting the Phase 2 checklist item. Without resolution, the task file would embed contradictory replacement text.

This contradiction is flagged separately in §"Contradictions Found" below — it is **NOT** a Criterion-8 failure (both researchers DID propose full schemas for all three types) but it IS a critical disambiguation the builder must perform.

---

### Criterion 9 — Unresolved ambiguities documented (or none-with-justification)

**PASS (with caveat).**

Evidence:

- File 02 §3.3 explicitly answers "is there a harness?" with **NO** and tells the builder to note in Phase 2 prose that "Fix 3 assertion entries are 'harness-ready' but not currently runtime-enforced."
- File 02 §4.6 supplies OQ-1 (assertion JSON shape) RESOLVED.
- File 03 §8 ("Gaps / caveats") explicitly enumerates 5 caveats: (1) CI does not enforce src/↔.claude/ parity, (2) `make lint-architecture` not in CI, (3) `/sc:reflect` is a slash command not a CLI, (4) shellcheck may not be installed locally — pre-commit pins v0.9.0.6, (5) markdownlint --fix may rewrite SKILL.md.
- File 03 §8 also explicitly flags the eval-shape uncertainty: "evals.json assertion-count `jq` query is shape-dependent. Researcher-02 is delivering the eval-harness DSL definitive shape; if it's `.evals[].assertions` instead of `.scenarios[].assertions`, swap the jq path."

**Caveat — the cross-researcher contradiction (File 01 vs File 02 on JSON shape and markers) is NOT explicitly called out as an unresolved ambiguity in any of the three files.** File 01 simply states its shape; File 02 simply states its shape (different); neither cross-references the other. The contradiction surfaces only on cross-file analysis (this report).

This is a documentation hygiene issue — neither researcher knew what the other was producing in the same Quick-tier sprint. Not a failure of Criterion 9 per se (both researchers did document their own ambiguities), but it's a coordination gap that the builder must resolve at task-creation time.

---

## Contradictions Found

### Contradiction 1 — Assertion JSON shape (HIGH severity for builder)

**Files:** 01 vs 02.

**File 01 §"Proposed assertion DSL" (line 173-176):**

```json
{ "type": "file_exists", "path": "<path>" }
{ "type": "report_contains", "report": "<path>", "markers": [...] }
{ "type": "no_hallucinated_citations", "report": "<path>", "repo_root": "<path>" }
```

**File 02 §4 (lines 304-316, 343-358, 382-392):**

```json
{ "text": "<prose>", "type": "file_exists", "path": "<path>" }
{ "text": "<prose>", "type": "report_contains", "report": "<path>", "markers": [...] }
{ "text": "<prose>", "type": "no_hallucinated_citations", "report": "<path>", "citation_regex": "...", "repo_root": "<path>" }
```

**Why this matters:** File 01 supplies "Exact replacement text" for each of the three scenarios (lines 187-217) using the **no-`text`-field** shape. If the builder copies File 01's replacement blocks verbatim into the Phase 2 checklist item, the resulting `evals.json` will diverge from the Anthropic-canonical skill-creator schema (which File 02 §3.1 cites authoritatively).

**Recommendation:** the builder MUST use File 02's shape (with `text` field) and File 02's `citation_regex` field for the third assertion type. File 01's "Exact replacement text" blocks need to be re-templated through File 02's schema before being embedded in the task file's Phase 2 checklist item.

### Contradiction 2 — Report-contains markers (HIGH severity for builder)

**Files:** 01 vs 02.

**File 01 (lines 190, 202, 214):** `["# Code Review:", "## Findings", "## Audit"]`

**File 02 §4.3 and §4.5 (lines 351-356, 427-432):** `["## Critical Findings", "## High Findings", "## Medium Findings", "## Low Findings", "## Summary"]`

**Why this matters:** these are completely different marker sets. They imply different report structures. Neither researcher explains the chosen markers by reading the actual report-template format used by the sc-auggie-review skill.

**Critical adversarial point:** **Neither researcher verified the markers against the actual REVIEW.md template structure produced by the skill.** A correct marker list would come from reading the SKILL.md's report-template section (which is the file being edited for M2 anyway). Without that verification, both marker lists are speculative.

**Recommendation:** the builder must either (a) read the skill's REVIEW.md template structure before drafting the Phase 2 item, OR (b) embed a resolved-OQ in the task file acknowledging the marker set is best-effort and may need adjustment after the first eval run.

### Contradiction 3 — `repo_root` value (LOW severity)

**File 01 (line 191):** `"repo_root": "/config/workspace/IronClaude"`
**File 02 §4.4 default:** `"repo_root": "."` (with `/config/workspace/IronClaude` in the paste-ready example at line 390).

These are reconcilable (File 02's default is `.` but its example uses the absolute path matching File 01). Not blocking, but a builder should pick one and apply consistently.

### Contradiction 4 — `citation_regex` field presence (MEDIUM)

**File 01:** No `citation_regex` field on the `no_hallucinated_citations` assertion (line 175).
**File 02 §4.4:** `citation_regex` is a **REQUIRED** field with a paste-ready default value (line 389, 400).

If the builder uses File 02's required-fields specification, File 01's replacement JSON (which omits `citation_regex`) would be schema-invalid against File 02's DSL. The builder MUST include `citation_regex` in the final replacement.

---

## Compiled Gaps

### Critical Gaps (block synthesis / builder)

None. All three fixes have actionable before/after text, line citations, verification commands, and template references. The contradictions above are NOT gaps — both researchers DID supply complete material; the builder simply must pick one of two presented shapes.

### Important Gaps (must be addressed before builder finalizes)

1. **Assertion JSON shape contradiction (File 01 vs File 02).** Builder must choose File 02's shape (with `text`, `citation_regex`) for Anthropic-schema alignment. Recommend the builder embed File 02 §4.5 verbatim and DISCARD File 01's three per-scenario replacement JSON blocks.
2. **Marker-list contradiction.** Builder must either resolve via reading the actual report template, or document the marker list as a "best-effort, may need first-run adjustment" item.
3. **Documentation verification tags absent.** All claims about Makefile/pre-commit/CI in File 03, and the "no harness exists" claim in File 02 §3.3, should carry `[CODE-VERIFIED]` tags. Line-citations partially compensate but the tags would make traceability explicit.

### Minor Gaps

1. File 02 §3.1 cites external Anthropic mintlify and GitHub URLs without indicating whether the researcher actually fetched them in this Quick-tier sprint (no-web). If the URLs were not fetched, the claims about "`file_exists` and `custom` are the only published types" are `[UNVERIFIED]`. The builder should treat these as plausible-but-unfetched.
2. File 02 does not explicitly state the output task filename `TASK-RF-20260520-230051.md` (only the `id` field). Builder cannot reasonably miss this given exemplar conventions, but explicit is better than implicit.
3. File 03 §8 flags the eval-shape uncertainty (`.scenarios[]` vs `.evals[]`) but does not resolve it. File 01 §"File 3" line 138 confirms the shape is `{ "skill_name": ..., "evals": [...] }` so the correct jq path is `.evals[].assertions`. Builder should apply that correction to File 03's §5.3 jq one-liners (lines 234, 238).

---

## Depth Assessment

**Expected depth:** Quick tier (3 researchers, no web).
**Actual depth achieved:** Standard tier in places.

- File 01 over-delivered: byte-exact before/after text for all 3 fixes including line-by-line line numbers and 5-7 patterns-to-preserve per file. This is Standard/Deep tier.
- File 02 over-delivered: ~1200-line template fully cited with section/line references; full assertion DSL with required+optional fields, failure modes, design rationale; prior exemplar identified and structurally mapped. This is Standard/Deep tier.
- File 03 met Quick tier: per-file commands + post-edit chain + gap list. Adequate.

**Missing depth elements:** None for Quick tier. The contradictions are coordination misses, not depth misses.

---

## Recommendations for Builder

1. **Use File 02's assertion JSON shape verbatim** (with `text` field, `citation_regex` field). DISCARD File 01's per-scenario replacement JSON blocks at lines 187-217 — they are missing the `text` field and `citation_regex` field required by File 02 §4.2/§4.4.
2. **Pick a single marker list and embed it in OQ-2.** Recommend reading the actual REVIEW.md template structure inside `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` (specifically the report-template section) before choosing. If unable to read in advance, document marker list as "best-effort, first-run-adjustable" and prefer File 02's `## Critical Findings / ## High Findings / ## Medium Findings / ## Low Findings / ## Summary` set as it matches typical PR-review report structure.
3. **Apply the jq path correction** in File 03 §5.3: replace `.scenarios[]` with `.evals[]` (confirmed by File 01 §"File 3" line 164 which states the top-level shape is `{"skill_name": "<string>", "evals": [<eval-object>, ...]}`).
4. **Embed File 02 §4.6 OQ-1 wording verbatim** in the task file's Open Questions table. Add a new OQ-2 for the marker-list resolution.
5. **Use TASK-RF-20260517-183817 as the structural exemplar** as File 02 §2.2 recommends. Phase ordering: Phase 1 setup → Phase 2 per-file edits (3 items) → Phase Gate QA → Phase 3 Verification & Sync → Post-Completion.
6. **Name the verification phase `Verification & Sync`, not `Testing & Verification`** (per File 02 §1.7).
7. **Spawn `rf-qa-qualitative` for the SKILL.md edit** (max 3 fix cycles, text-content gate) and `rf-qa` for the evals.json edit (max 2 cycles, structural JSON gate). Source: File 02 §1.6.
8. **Forbid `git commit --no-verify`** explicitly in the task file (File 03 §8 caveat 1: CI does not enforce src/↔.claude/ parity; only the pre-commit verify-sync hook does).

---

## VERDICT: PASS

The three research files collectively supply the builder with enough material to draft a high-quality MDTM Template 02 task file for PR #64 remediation. All checklist criteria except Criterion 7 (verification tags) PASS, and Criterion 7 fails only on documentation-hygiene grounds (line citations are present and traceable — the missing element is the explicit `[CODE-VERIFIED]` tag string).

The contradictions between File 01 and File 02 on assertion JSON shape and markers are **critical to resolve at build time**, but they are NOT a research-completeness failure — both researchers produced complete, internally-consistent designs. The builder must pick File 02's design (per the recommendations above).

**Gate verdict: PASS with 3 important gaps surfaced for builder resolution.** Builder may proceed to draft the task file, applying the recommendations in §"Recommendations for Builder" above.
