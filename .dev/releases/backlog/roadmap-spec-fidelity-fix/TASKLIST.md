# Implementation Tasklist — Top 3 Spec-Fidelity Fixes

**Target**: Resolve the convergence failure documented at
`.dev/releases/current/task-builder-merge/roadmap/spec-fidelity.md`.

**Scope**: Implement S1, S2, S5 in dependency order. Defer S3, S4, S6.

**Validation**: After all three tasks complete, re-run
`superclaude roadmap run .dev/releases/current/task-builder-merge/TDD_TASK_BUILDER_CONVERGENCE.md --resume`
and confirm the `spec-fidelity` step transitions to PASS.

---

## TASK 1 — S1: Sanitize File-Path Extraction

**Why first**: Smallest blast radius; eliminates 4/10 phantom HIGHs at extraction.
Must precede S2 or S2 will route phantoms to the roadmap as nonexistent file rows.

**Files to edit**:
- `src/superclaude/cli/roadmap/spec_parser.py`
- `tests/cli/roadmap/test_spec_parser.py`

**Steps**:
1. In `spec_parser.py` (~line 397), add a module-level constant:
   ```python
   _URL_PRECEDING_RE = re.compile(r'(?:[A-Za-z0-9]|://)$')
   ```
2. Add helper `_looks_like_file_path(candidate: str, cell: str, start: int) -> bool` implementing the 5 reject rules from `solutions/S1-sanitize-file-path-extraction.md`:
   - Reject if candidate contains `{`, `}`, `*`, `?`, backtick, or whitespace.
   - Reject if candidate matches `:\d+` (line-number suffix).
   - Reject if candidate ends in `.`, `,`, `;`, `:`, `)` (after the existing strip).
   - Reject if preceded by `://` or alphanumeric in the source cell (URL embedment).
3. Modify `extract_file_paths_from_tables` (~line 407) to call `_looks_like_file_path(raw, cell, m.start())` before adding to the result set. Pass `cell` and `m.start()` from the existing `finditer` loop.
4. Modify `extract_file_paths` (~line 402) to also call the helper with `cell=text, start=match.start()`.

**Acceptance criteria**:
- [ ] `uv run pytest tests/cli/roadmap/test_spec_parser.py -v` passes.
- [ ] New negative-case tests reject: `docs/grouping-algorithm` inside a URL, `src/superclaude/{skills,agents}`, `src/x.py:88\``, `docs/error-grouping-best-practices` (no extension AND inside URL prose).
- [ ] New positive-case tests accept: `scripts/build` (extensionless infrastructure path), `docs/CHANGELOG`, `src/superclaude/cli/main.py`, `tests/cli/roadmap/test_spec_parser.py`.
- [ ] Re-running spec-fidelity on the `task-builder-merge` release shows ≤6 ACTIVE HIGHs after Run 1 (down from 15).

---

## TASK 2 — S2: Route Findings to Roadmap + Actionable Fix Guidance

**Why second**: Foundational schema change to `_make_finding`. Must precede S5
because S5's emission path uses the same helper.

**Files to edit**:
- `src/superclaude/cli/roadmap/structural_checkers.py`
- `src/superclaude/cli/roadmap/semantic_layer.py`
- `src/superclaude/cli/roadmap/remediate_prompts.py`
- `src/superclaude/cli/roadmap/models.py`
- `tests/cli/roadmap/test_structural_checkers.py`
- `tests/cli/roadmap/test_remediate_prompts.py`

**Steps**:
1. **Schema**: In `structural_checkers.py` extend `_make_finding(...)` signature to accept `files_affected: list[str] | None = None`; default to `[]` and forward into `Finding(files_affected=files_affected or [])`. Mirror the change in `semantic_layer.py:514`.
2. **Routing table**: In `structural_checkers.py`, add module-level:
   ```python
   MISMATCH_FILE_ROUTING: dict[tuple[str, str], str] = {
       ("data_models", "file_missing"): "roadmap",
       ("data_models", "path_prefix_mismatch"): "roadmap",
       ("data_models", "enum_uncovered"): "roadmap",
       ("data_models", "field_missing"): "roadmap",
       ("signatures", "phantom_id"): "roadmap",
       ("signatures", "function_missing"): "roadmap",
       ("signatures", "param_arity_mismatch"): "roadmap",
       ("signatures", "param_type_mismatch"): "roadmap",
       ("gates", "frontmatter_field_missing"): "roadmap",
       ("gates", "step_param_missing"): "roadmap",
       ("gates", "ordering_violated"): "roadmap",
       ("gates", "semantic_check_missing"): "roadmap",
       ("cli", "mode_uncovered"): "roadmap",
       ("cli", "default_mismatch"): "roadmap",
       ("nfrs", "threshold_contradicted"): "roadmap",
       ("nfrs", "security_missing"): "ambiguous",
       ("nfrs", "dep_direction_violated"): "roadmap",
       ("nfrs", "coverage_mismatch"): "roadmap",
       ("nfrs", "dep_rule_missing"): "roadmap",
   }
   ```
3. **Threading**: Add `roadmap_path` argument resolution into `_make_finding` (each checker already receives it as a parameter — just forward it). When routing resolves to `"roadmap"` set `files_affected=[roadmap_path]`. When `"ambiguous"`, set `files_affected=[roadmap_path]` AND `deviation_class="AMBIGUOUS"`.
4. **Fix guidance templates**: Add `FIX_GUIDANCE_TEMPLATES: dict[str, str]` keyed on `mismatch_type` (use the table in `solutions/S2-route-findings-to-roadmap-target.md` §4 part 1). In `_make_finding`, populate `fix_guidance` by interpolating `{spec_quote}`, `{roadmap_quote}` into the template.
5. **Prompt nudge**: In `remediate_prompts.py` `build_remediation_prompt`, append to the Constraints block:
   > *Prefer additive edits. If a fix requires more than ~5 changed lines to a section, split into multiple smaller edits across separate agent runs.*
6. **Models**: In `models.py`, ensure `deviation_class` is a recognized field and `"AMBIGUOUS"` is in `VALID_DEVIATION_CLASSES`.

**Acceptance criteria**:
- [ ] `uv run pytest tests/cli/roadmap/` passes.
- [ ] Findings emitted from `check_data_models` against the task-builder spec carry `files_affected=[<roadmap-abs-path>]`.
- [ ] `build_remediation_prompt` output contains the per-mismatch template, not the generic `"Address {mismatch_type} in {dimension} dimension"` boilerplate.
- [ ] Manual trace: with S1 already applied, the 2 LEGIT manifest-gap HIGHs (`prd_template.md`, `tdd_template.md`) now have non-empty `files_affected`.
- [ ] Existing tests that asserted `files_affected=[]` are updated; tests that asserted `fix_guidance="Address ..."` boilerplate are updated.

---

## TASK 3 — S5: Context-Aware NFR Severity

**Why third**: Depends on S2's `_make_finding` signature; needs to pass `severity` parameter through.

**Files to edit**:
- `src/superclaude/cli/roadmap/structural_checkers.py` (`check_nfrs` and helpers)
- `src/superclaude/cli/roadmap/models.py` (allowlist loader, if added)
- `tests/cli/roadmap/test_structural_checkers.py`

**Steps**:
1. **Per-section iteration**: In `check_nfrs` (~line 518), replace the `_section_text(spec_sections)` blob join. Iterate `for section in spec_sections:` and run the security-keyword and threshold regexes against `section.content`. Preserve `section.heading_path` and `section.heading` per match.
2. **Severity classifier**: Add helper `_classify_nfr_severity(dimension, mismatch_type, heading_path, heading) -> str`:
   ```python
   _STRONG_NFR_TOKENS = (
       "security", "critical", "must", "shall", "required",
       "p0", "nfr-", "compliance", "encryption", "audit",
   )
   def _classify_nfr_severity(dimension, mismatch_type, heading_path, heading):
       if mismatch_type not in ("security_missing", "threshold_contradicted"):
           return get_severity(dimension, mismatch_type)
       haystack = f"{heading_path}/{heading}".lower()
       return "HIGH" if any(tok in haystack for tok in _STRONG_NFR_TOKENS) else "MEDIUM"
   ```
3. **Stable ordering**: Before emission, sort findings by `(heading_path, term)` so `stable_id` allocation is deterministic across runs.
4. **(Optional, time-permitting)** YAML allowlist: load `<output_dir>/roadmap/fidelity-allowlist.yaml` once per run; for matching findings set `severity="LOW"` and `deviation_class="PRE_APPROVED"`.
5. **Registry migration shim**: When loading an existing `deviation-registry.json`, if a finding's `stable_id` matches but the severity has changed from HIGH→MEDIUM, treat it as a continuation (set `status` based on prior status; don't reset to ACTIVE).

**Acceptance criteria**:
- [ ] `uv run pytest tests/cli/roadmap/test_structural_checkers.py -v` passes.
- [ ] New tests confirm: strong-NFR heading (`## Security NFRs`) keeps `security_missing` at HIGH; generic heading (`## Non-Functional Requirements`) demotes to MEDIUM.
- [ ] New test confirms emission order is deterministic across two runs over identical input.
- [ ] Re-running spec-fidelity on `task-builder-merge` shows the 4 NFR HIGHs (`encryption`, `hash`, `<1%`, `<2%`) classified as MEDIUM if they appear under a generic heading; they continue to appear in the report under "Soft Deviations".

---

## End-to-End Validation (after all 3 tasks)

```bash
# 1. Run the full test suite
uv run pytest tests/cli/roadmap/ -v

# 2. Re-run the failed pipeline with --resume
superclaude roadmap run \
  /config/workspace/IronClaude/.dev/releases/current/task-builder-merge/TDD_TASK_BUILDER_CONVERGENCE.md \
  --resume

# 3. Verify spec-fidelity reaches 0 ACTIVE HIGHs
cat /config/workspace/IronClaude/.dev/releases/current/task-builder-merge/roadmap/spec-fidelity.md \
  | head -20
# Expect:
#   high_severity_count: 0
#   validation_complete: true
#   tasklist_ready: true
```

## Backup / Workaround (if validation still fails)

See `BACKUP-WORKAROUND.md` next to this file. Short version:
```bash
superclaude roadmap run <spec> --resume --allow-regeneration --max-runs 5
```
Use this to brute-force past the gate, accept the draft tasklist, and proceed to
the `/sc:tasklist` phase manually while a real fix is being investigated.

---

## Execution Order Recap

1. **TASK 1 (S1)** — independent; merge first (lowest risk, immediate wins).
2. **TASK 2 (S2)** — foundational schema change; merge second.
3. **TASK 3 (S5)** — depends on S2's `_make_finding` signature; merge last.

Each task should be a separate commit on the same feature branch
(`feat/roadmap-spec-fidelity-fix` recommended) so any individual change can be
reverted in isolation if it breaks tests.
