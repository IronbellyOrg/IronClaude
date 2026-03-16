# Phase 7 -- Release Spec Synthesis

Produce the release-ready spec from prior artifacts with placeholder elimination and structured gap capture via 3-persona brainstorm. **Amendment**: `--file` passthrough is removed; inline `-p` embedding only (OQ-008 resolved).

---

### T07.01 -- Load Release Spec Template and Create Working Copy

| Field | Value |
|---|---|
| Roadmap Item IDs | R-048 |
| Why | The template provides the 13-section skeleton and {{SC_PLACEHOLDER:*}} sentinels; a working copy prevents template corruption and enables safe iterative population |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution 30s |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0044 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0044/spec.md`

**Deliverables:**
- Template loader in `prompts.py` reading `src/superclaude/examples/release-spec-template.md` (AC-009, D-007); working copy created at `workdir/release-spec-working.md`

**Steps:**
1. **[PLANNING]** Review roadmap AC-009/D-007: template at `src/superclaude/examples/release-spec-template.md` with 13 sections and `{{SC_PLACEHOLDER:*}}` sentinels
2. **[EXECUTION]** Implement `load_release_spec_template(project_root: Path) -> str` in `prompts.py`
3. **[EXECUTION]** Raise `PortifyValidationError(failure_type=INVALID_PATH)` if template file absent
4. **[EXECUTION]** Implement `create_working_copy(template_content: str, workdir: Path) -> Path` writing to `workdir/release-spec-working.md`
5. **[EXECUTION]** Verify template has all 13 sections (count `{{SC_PLACEHOLDER:` occurrences ≥ 13)
6. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "release_spec_template or working_copy" -v`
7. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0044/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "release_spec_template"` exits 0
- `load_release_spec_template()` raises `PortifyValidationError` when template absent
- Working copy at `workdir/release-spec-working.md` is byte-identical to source template
- Template has ≥13 `{{SC_PLACEHOLDER:*}}` sentinels confirmed

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "working_copy" -v` passes; template INVALID_PATH case verified
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0044/spec.md` produced

**Dependencies:** T06.04 (portify-spec.md must exist before synthesis begins)
**Rollback:** Delete working copy from workdir; template file is read-only

---

### T07.02 -- Implement 4-Substep Release Spec Synthesis (3a–3d)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-049 |
| Why | The 4-substep synthesis (working copy creation, 13-section population, 3-persona brainstorm, finding incorporation) is the core of the release spec; each substep must complete before the next |
| Effort | XL |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0045 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0045/spec.md`

**Deliverables:**
- Release synthesis step in `executor.py` implementing substeps 3a–3d: (3a) working copy confirmed, (3b) 13-section population via Claude, (3c) 3-persona brainstorm (architect/analyzer/backend) with `{gap_id, description, severity, affected_section, persona}` findings, (3d) finding incorporation — actionable to body, unresolvable to Section 11 (FR-027)

**Steps:**
1. **[PLANNING]** Review roadmap FR-027: 4 substeps; SKILL.md notation uses 3a–3d
2. **[EXECUTION]** Substep 3a: confirm working copy exists (from T07.01)
3. **[EXECUTION]** Substep 3b: implement `build_section_population_prompt(working_copy, portify_spec, analysis_report) -> str`; execute Claude; write populated draft to `workdir/release-spec-draft.md`
4. **[EXECUTION]** Substep 3c: implement `build_brainstorm_prompt(draft_content) -> str` for each of 3 personas (architect, analyzer, backend); execute Claude 3 times; collect `BrainstormFinding(gap_id, description, severity, affected_section, persona)` objects
5. **[EXECUTION]** Substep 3d: implement `incorporate_findings(draft, findings) -> str`; CRITICAL/MAJOR findings → body; unresolvable → Section 11
6. **[EXECUTION]** Write final output to `workdir/portify-release-spec-draft.md`
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "synthesis_3a or brainstorm or finding_incorporation" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0045/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "brainstorm"` exits 0
- 3 persona Claude calls produce distinct findings with `{gap_id, description, severity, affected_section, persona}` structure
- CRITICAL findings incorporated into body (not Section 11)
- Unresolvable findings routed to Section 11
- `BrainstormFinding` dataclass importable from `superclaude.cli.cli_portify.models`

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "finding_incorporation" -v` — severity routing verified
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0045/spec.md` produced

**Dependencies:** T07.01 (working copy), T06.04 (portify-spec.md), T05.02 (analysis-report.md)
**Rollback:** Remove synthesis substeps from executor; draft remains in workdir

---

### T07.03 -- Validate Zero Placeholders and Emit portify-release-spec.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-050 |
| Why | Placeholder leakage into the final release spec is a high-severity risk; the placeholder scan must run before G-010 gate and before the file is emitted as the final artifact |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution 30s |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0046 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0046/spec.md`

**Deliverables:**
- `executor.py` placeholder scan (zero `{{SC_PLACEHOLDER:*}}`); Section 12 presence check; `portify-release-spec.md` emission with frontmatter `{title, status, quality_scores}` (FR-028, FR-029, SC-008)

**Steps:**
1. **[PLANNING]** Review roadmap FR-028/FR-029: zero placeholder validation; Section 12 required; frontmatter required
2. **[EXECUTION]** Implement `scan_for_placeholders(content: str) -> list[str]` returning list of remaining `{{SC_PLACEHOLDER:X}}` names
3. **[EXECUTION]** If any placeholder found: raise `PortifyValidationError` listing remaining placeholder names
4. **[EXECUTION]** Verify Section 12 (Brainstorm Gap Analysis) exists in draft content
5. **[EXECUTION]** Add YAML frontmatter `{title, status: draft, quality_scores: {}}` to draft
6. **[EXECUTION]** Write to `workdir/portify-release-spec.md`
7. **[EXECUTION]** Apply G-010 gate: confirms zero placeholders + Section 12 present + EXIT_RECOMMENDATION
8. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "placeholder_scan or release_spec_emit" -v`
9. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0046/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "placeholder_scan"` exits 0
- Content with `{{SC_PLACEHOLDER:INTRO}}` raises `PortifyValidationError` naming the placeholder
- Content with zero placeholders and Section 12 passes; `portify-release-spec.md` emitted
- G-010 gate (SC-008) passes on emitted file

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "release_spec_emit" -v` — G-010 gate integration verified
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0046/spec.md` produced

**Dependencies:** T07.02 (synthesis draft), T04.01 (G-010 gate)
**Rollback:** Remove placeholder scanner; `portify-release-spec.md` not emitted

---

### T07.04 -- Implement Inline Embed Guard and 900s Timeout (OQ-008 Amendment)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-051 |
| Why | --file is broken (confirmed v2.24.5); inline -p embedding is the only safe mechanism; content >120KB must raise an explicit error rather than silently passing truncated content to Claude |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0047 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0047/spec.md`

**Deliverables:**
- `prompts.py` `build_release_spec_prompt()`: if `len(template_content) > _EMBED_SIZE_LIMIT` (120 * 1024 bytes) raise `PortifyValidationError(failure_type=CONTENT_TOO_LARGE)`; else pass inline via `-p` (amended from `--file`); 900s timeout in STEP_REGISTRY (NFR-001)

**Steps:**
1. **[PLANNING]** Review OQ-008 resolution in `oq-resolutions.md`: `--file` broken; use inline `-p` only; limit = 120 * 1024
2. **[EXECUTION]** Define `_EMBED_SIZE_LIMIT = 120 * 1024` in `prompts.py` (or import from `cli/roadmap/executor.py`)
3. **[EXECUTION]** Implement guard in `build_release_spec_prompt()`: `if len(template_content) > _EMBED_SIZE_LIMIT: raise PortifyValidationError(failure_type=CONTENT_TOO_LARGE, message=f"Template size {len(template_content)} exceeds {_EMBED_SIZE_LIMIT} byte inline limit")`
4. **[EXECUTION]** For content under limit: pass inline via `-p` (standard PortifyProcess mechanism)
5. **[EXECUTION]** Set `timeout_s = 900` in STEP_REGISTRY for release-spec-synthesis step
6. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "embed_guard or content_too_large or timeout_900" -v`
7. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0047/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "embed_guard"` exits 0
- Content of 121 * 1024 bytes raises `PortifyValidationError(failure_type=CONTENT_TOO_LARGE)`
- Content of 100 * 1024 bytes passes inline via `-p` (no `--file` call anywhere)
- `timeout_s = 900` confirmed in STEP_REGISTRY for release-spec-synthesis
- `--file` flag does NOT appear anywhere in `PortifyProcess.build_command()` output

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "content_too_large" -v` — >120KB raises correctly
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0047/spec.md` produced

**Dependencies:** T01.03 (CONTENT_TOO_LARGE in failure_type enum, OQ-009 resolution)
**Rollback:** Remove embed guard; template passed without size check (unsafe but recoverable)
**Notes:** `--file` mechanism confirmed broken by v2.24.5 empirical testing; see `oq-resolutions.md` OQ-008. This task implements the roadmap amendment.

---

### Checkpoint: End of Phase 7

**Purpose:** Verify the release spec synthesis produces a clean `portify-release-spec.md` with zero placeholders and Section 12 present, and that the inline embed guard is enforced before Phase 8 panel review begins.
**Checkpoint Report Path:** `.dev/releases/current/v2.25-cli-portify-cli/checkpoints/CP-P07-END.md`

**Verification:**
- `uv run pytest tests/cli_portify/ -k "release_spec or placeholder_scan or embed_guard or brainstorm" -v` exits 0
- SC-008 (G-010 passes on release-spec.md: zero placeholders, Section 12 present) verified
- `CONTENT_TOO_LARGE` error fires correctly for template >120KB

**Exit Criteria:**
- All 4 Phase 7 tasks complete with D-0044 through D-0047 artifacts
- Milestone M6: Step 10 produces release spec passing G-010
- No `--file` subprocess calls anywhere in codebase
