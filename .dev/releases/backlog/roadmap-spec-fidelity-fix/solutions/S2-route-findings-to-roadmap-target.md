# Solution S2 — Route Manifest Findings to Roadmap Target (Refactored)

## Target root cause
Every active finding in the failing run has `files_affected=[]`.
The `_make_finding(...)` helper in `structural_checkers.py` does **not** even
accept a `files_affected` argument — though the `Finding` dataclass has the
field with a `default_factory=list`. Net effect: every structural finding is
emitted with `files_affected=[]`.

Downstream:

- `enforce_allowlist` (`remediate_executor.py:173`) SKIPS findings with empty
  `files_affected`. If filtering were the only failure mode, the remediation
  step would short-circuit with no edits.
- But the convergence executor path (used in the failing run) still groups by
  `files_affected` and falls back to the spec file as the only loaded text
  available. Agents therefore rewrote the TDD (`TDD_TASK_BUILDER_CONVERGENCE.md`),
  generating the 71.3% / 38.1% diffs that the 30%-per-file guard rejected.

The fix: structurally-derived "missing in roadmap" findings describe a
**roadmap defect** — the right edit target is the roadmap file, not the
TDD spec. This refactor adds explicit, per-mismatch routing rules with
defensible fallbacks, plus the prompt-template changes needed to make the
agent's edits actionable (not just point at a file).

## Proposal

### 1. Threading `files_affected` through `_make_finding`

Extend `_make_finding(...)` (and the parallel `Finding(...)` call in
`semantic_layer.py:514`) to accept `files_affected: list[str]` and forward it
to the `Finding` dataclass. The basename check in `enforce_allowlist`
(`_basename(f)` against `EDITABLE_FILES`) means we can pass either the full
roadmap path or just `"roadmap.md"` — we pass the **full path** so the
remediation executor's snapshot/rollback machinery works directly.

### 2. Per-dimension routing rules

Add a routing table keyed on `(dimension, mismatch_type)` with three classes:

| Dimension | Mismatch type | Edit target | Rationale |
|-----------|---------------|-------------|-----------|
| data_models | file_missing | `[roadmap_path]` | roadmap manifest gap |
| data_models | path_prefix_mismatch | `[roadmap_path]` | roadmap copied wrong prefix |
| data_models | enum_uncovered | `[roadmap_path]` | roadmap must cover spec literals |
| data_models | field_missing | `[roadmap_path]` | roadmap must reference field |
| signatures | phantom_id | `[roadmap_path]` | roadmap invented a non-spec ID |
| signatures | function_missing | `[roadmap_path]` | roadmap missing spec function |
| signatures | param_arity_mismatch | `[roadmap_path]` | roadmap signature drifted |
| signatures | param_type_mismatch | `[roadmap_path]` | roadmap signature drifted |
| gates | frontmatter_field_missing | `[roadmap_path]` | roadmap gate gap |
| gates | step_param_missing | `[roadmap_path]` | roadmap gate gap |
| gates | ordering_violated | `[roadmap_path]` | roadmap ordering wrong |
| gates | semantic_check_missing | `[roadmap_path]` | roadmap gate gap |
| cli | mode_uncovered | `[roadmap_path]` | roadmap missing CLI surface |
| cli | default_mismatch | `[roadmap_path]` | roadmap default drifted |
| nfrs | threshold_contradicted | `[roadmap_path]` | roadmap value contradicts spec |
| nfrs | security_missing | **`[]` → AMBIGUOUS** | could be spec over-claim — see §3 |
| nfrs | dep_direction_violated | `[roadmap_path]` | roadmap arrow reversed |
| nfrs | coverage_mismatch | `[roadmap_path]` | roadmap weaker than spec |
| nfrs | dep_rule_missing | `[roadmap_path]` | roadmap missing rule |

Rule is sourced from a single dict `MISMATCH_FILE_ROUTING: dict[tuple[str,str], str]`
in `structural_checkers.py` with literal values `"roadmap"` or `"ambiguous"`.
`_make_finding` resolves `"roadmap"` to the actual `roadmap_path` argument
(threaded in from each checker), so the source of truth is one table.

### 3. Ambiguous-case fallback (issue (c): spec-defect mis-routing)

The adversarial review identified `nfrs/security_missing` as a real risk: a
finding "spec mentions 'encryption' but roadmap doesn't" can be either
(i) a roadmap gap (add an encryption-at-rest NFR) **or** (ii) a spec over-claim
(strip the unsupported security primitive from the TDD).
Adversarial finding: in the failing run the spec is fixed-input to the
roadmap pipeline; agents have no warrant to edit the TDD anyway. So:

- Routing `"ambiguous"` results in `files_affected=[roadmap_path]` **plus** a
  `deviation_class="AMBIGUOUS"` tag and an annotated `fix_guidance` that
  reads: *"If this primitive is in scope, add NFR to roadmap; if the spec
  over-claims, raise a deviation note in `extraction.md` — do NOT modify the
  spec file."* This keeps the spec immutable while letting the agent record
  a defensible alternative in `extraction.md` (already in `EDITABLE_FILES`).

### 4. Prompt-template adjustments (issue (a): agent doesn't know HOW to fix)

Adversarial finding: even with correct routing, the current
`build_remediation_prompt` only emits `fix_guidance="Address {mismatch_type}
in {dimension} dimension"` — useless boilerplate. The agent receives no
instruction to "add a row to the File Manifest table" or "remove the phantom
SC-001 reference." This is precisely why the agent regenerated whole sections
and tripped the diff guard.

Fix (two-part):

1. **In `_make_finding`**: replace the generic `fix_guidance` with a
   per-mismatch action template, e.g.:

   | Mismatch type | Templated fix_guidance |
   |---|---|
   | file_missing | "Add a row referencing `{spec_quote}` to the File Manifest section of the roadmap. Do not modify other rows." |
   | phantom_id | "Remove the reference to `{roadmap_quote}` from the roadmap (the ID is not defined in the spec)." |
   | security_missing | "Add an NFR line covering `{spec_quote}` to the Non-Functional Requirements section of the roadmap, OR if out-of-scope, document the deviation in extraction.md." |
   | threshold_contradicted | "Update the roadmap threshold to match the spec value `{spec_quote}` (currently `{roadmap_quote}`)." |
   | step_param_missing | "Add parameter `{spec_quote}` to the corresponding Step(...) call in the roadmap's gates section." |
   | … (one per mismatch_type) … | |

2. **In `build_remediation_prompt`**: append a single line to the Constraints
   block: *"Prefer additive edits. If a fix requires more than ~5 changed
   lines to a section, split into multiple smaller edits across separate
   agent runs."* This nudges the agent toward small patches, reducing the
   chance of tripping the 30% diff guard.

### 5. Chunking strategy (issue (b): single-file bottleneck + diff bloat)

Adversarial finding: routing all 10 findings to `roadmap.md` collapses the
ThreadPoolExecutor (`max_workers=len(all_target_files)`) to a single worker
and stacks 10 fixes into one prompt. Probability of >30% diff rises sharply
on small roadmaps.

Mitigation, layered:

- **Layer A — Diff guard already enforces per-patch**: `check_patch_diff_size`
  (`remediate_executor.py:311`) evaluates patches individually when
  `RemediationPatch` objects are produced. The legacy `_check_diff_size` is
  whole-file. The convergence path currently uses the legacy guard — leave
  that alone for this release.
- **Layer B — Cap findings per agent invocation**: in `group_findings_by_file`
  (or a new helper in `remediate_prompts.py`), if a single file group exceeds
  `MAX_FINDINGS_PER_AGENT = 5`, split into multiple sequential agent calls
  against the same file. Each call snapshots → applies → if guard passes,
  re-snapshots for the next. This requires a small change to
  `execute_remediation` to loop on file groups instead of one-shot
  ThreadPoolExecutor submit. **Out of scope for the minimum fix** — keep as a
  Phase 2 follow-up; document in the release notes.
- **Layer C — Minimum-fix bound**: for this release, just route correctly and
  rely on the templated `fix_guidance` (§4.1) to keep edits small. The
  failing case has 10 HIGHs; if the agent produces small additive rows, even
  a 30-line roadmap survives (~10 added lines / 40 max lines = 25%).

### 6. Test updates

- `tests/roadmap/test_structural_checkers.py`: assert each checker returns
  findings whose `files_affected == [roadmap_path]` for the
  `roadmap`-routed mismatch types and `files_affected == [roadmap_path]` +
  `deviation_class == "AMBIGUOUS"` for `security_missing`.
- `tests/roadmap/test_remediate_executor.py`: add a regression case where 10
  findings all route to `roadmap.md`; assert `enforce_allowlist` allows all,
  and `group_findings_by_file` produces one group with 10 findings (or
  multiple if §5 Layer B lands).
- `tests/roadmap/test_remediate_prompts.py`: assert templated `fix_guidance`
  appears in the prompt for at least one of each mismatch_type.

## Risks / residual concerns (post-refactor)

1. **All-on-one-file serial execution**: with 10 findings on a single agent,
   if that one agent fails after 1 retry, every finding is marked FAILED in
   one shot. Mitigation: §5 Layer B as a follow-up. Acceptable for the
   minimum fix because the alternative (current state) is 100% failure rate.
2. **Templated `fix_guidance` quoting**: `spec_quote` for `file_missing` is
   the raw file path, which is safe to interpolate. For `step_param_missing`
   it's the matched regex group `Step(name=foo`, which includes
   parens/equals — fine in markdown but verify no f-string injection of
   stray braces. Add a `_safe_fmt` helper if needed.
3. **`security_missing` AMBIGUOUS path**: the agent might still try to add a
   nonsense NFR to satisfy the finding. The `deviation_class="AMBIGUOUS"`
   tag plus the bi-conditional fix_guidance is a soft control, not a hard
   one. A stricter fix would require user prompt-in-the-loop, out of scope.
4. **Phantom-ID removal can cascade**: removing `SC-001` from roadmap may
   leave orphan references elsewhere in the roadmap (broken anchors). The
   agent prompt should say "and update any references to it" — add to the
   `phantom_id` template.

## Expected impact on the failing case

- All 10 active HIGHs gain `files_affected=[<roadmap_path>]` → pass
  `enforce_allowlist`.
- Templated `fix_guidance` tells the agent exactly what to add/remove →
  additive edits dominate, diff stays under 30%.
- Run 1 should drop 10 HIGHs → 0–2 (a couple may still trip the diff guard
  if the roadmap is unusually small).
- Run 2 cleans up any stragglers. Convergence at Run 2.

## Estimated effort

- `_make_finding` signature + routing table: ~25 LOC
- Per-mismatch `fix_guidance` templates: ~30 LOC
- Plumbing `roadmap_path` into each checker's `_make_finding` calls: ~20
  edits across `structural_checkers.py` (mechanical)
- `semantic_layer.py` Finding(...) call: ~5 LOC
- Tests: ~80 LOC across three files
- **Total**: ~160 LOC, 1.5–2 hours including test runs

## Files touched

- `src/superclaude/cli/roadmap/structural_checkers.py` — routing table,
  `_make_finding` signature, per-mismatch `fix_guidance` templates, thread
  `roadmap_path` into every `_make_finding` call site
- `src/superclaude/cli/roadmap/semantic_layer.py` — add
  `files_affected=[roadmap_path]` to the `Finding(...)` constructor on
  line 514
- `src/superclaude/cli/roadmap/remediate_prompts.py` — append the
  "prefer additive / split large fixes" line to Constraints
- `tests/roadmap/test_structural_checkers.py`,
  `tests/roadmap/test_remediate_executor.py`,
  `tests/roadmap/test_remediate_prompts.py`

## Out of scope (Phase 2 follow-up)

- §5 Layer B (`MAX_FINDINGS_PER_AGENT` chunking with sequential agent calls
  on the same file). Documented as a known limitation for this release.
- Switching the convergence path to `check_patch_diff_size` (per-patch) from
  `_check_diff_size` (whole-file). Tracked separately because it changes
  remediation semantics for non-convergence callers.
