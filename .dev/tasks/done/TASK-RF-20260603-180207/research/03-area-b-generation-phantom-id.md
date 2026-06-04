# Research R3 — Area B: Generator-Side Phantom-ID PREVENTION

- **Status:** Complete
- **Date:** 2026-06-03
- **Researcher:** R3
- **Topic:** Extend `render_step_tool_write_with_id_check` so generate/merge steps cannot EMIT roadmap_ids outside `envelope.spec_ids` AT GENERATION TIME, not merely catch them at the merge gate.
- **Scope:** `tool_writer.py`, `executor.py` (render dispatch / generate / merge), `envelope.py`, `id_registry.py`

---

## 1. `validate_id_subset` — the invariant primitive

`src/superclaude/cli/roadmap/tool_writer.py:344-370`. Full body:

```python
def validate_id_subset(
    roadmap_ids: list[str],
    spec_ids: set[str] | list[str],
    accepted_deviations: set[str] | list[str] | None = None,
) -> list[str]:
    allowed = set(spec_ids) | set(accepted_deviations or [])
    return [
        f"roadmap_id '{rid}' not in spec_ids ∪ accepted_deviations"
        for rid in roadmap_ids
        if rid not in allowed
    ]
```

- **Invariant:** `roadmap_ids ⊆ set(spec_ids) ∪ set(accepted_deviations)` (§MVR §3 / Contract #3).
- **Return shape:** `list[str]` — one error string per phantom id; **empty list == PASS**.
- **Error message (verbatim):** `roadmap_id '{rid}' not in spec_ids ∪ accepted_deviations`.
- Pure, deterministic, no I/O. This primitive is correct and reusable; it is NOT the gap.
- **Critical property:** if `spec_ids` AND `accepted_deviations` are both empty, `allowed == set()`, so EVERY `roadmap_id` is a violation. The caller never invokes it in that state because of the `if spec_ids:` guard (see §2/§5) — i.e. the emptiness is handled by SKIPPING the call, not by the primitive.

## 2. `render_step_tool_write_with_id_check` — the generator-side renderer

`src/superclaude/cli/roadmap/tool_writer.py:455-496`. Hot path:

```python
spec, parsed, errors = _parse_and_validate(step_id, json_text)
if errors:
    return errors

# Phantom-ID rejection: roadmap_ids ⊆ spec_ids ∪ accepted_deviations.
# Skip when spec_ids is empty/None (identity -- no universe to constrain to).
if spec_ids:                                                    # L487  <-- THE SHORT-CIRCUIT
    roadmap_ids = parsed.get("roadmap_ids", []) if parsed else []
    id_errors = validate_id_subset(roadmap_ids, spec_ids, accepted_deviations)
    if id_errors:
        return id_errors                                        # generation-time rejection

_persist_and_render(spec, parsed, output_path)
return []
```

- Order is: schema-validate → (if `spec_ids` truthy) subset-check → persist+render. A phantom id returns before any file is written. This IS true generation-time prevention — **when it runs**.
- **The `if spec_ids:` empty-skip (L487-493) is the documented hole.** The docstring (L474-477) says the skip is "acceptable when the upstream extract step is not itself in tool-write mode and therefore exposed no spec_ids sidecar." That rationale is exactly the gap: the spec's id universe is KNOWN (it exists in `spec_id_registry.json` / `envelope.spec_ids` regardless of extract's tool-write flag), but this renderer is only ever HANDED a non-empty `spec_ids` when `extraction.json` exists. When `spec_ids` is empty, the check is skipped and the step may emit ANY roadmap_ids.
- `roadmap_ids` is read flat from `parsed.get("roadmap_ids", [])`. Both `generate.schema.json:136` and `merge.schema.json:152` require a top-level `roadmap_ids` array (`required: [..., "roadmap_ids"]`), so the extraction site is correct for those two schemas.

## 3. `render_step_tool_write` (PLAIN, no id-check) — who uses it

`src/superclaude/cli/roadmap/tool_writer.py:421-452`. Identical to the id-check variant minus the subset gate. Used for **every tool-write step that is NOT generate/merge**: `extract`, `extract_tdd`, `diff`, `debate`, `score`, `spec-fidelity`, `test-strategy`, `certify`, etc.

Dispatch in `executor.py`:
- `executor.py:1269` — `if _tw_key in ("generate", "merge"):` → `render_step_tool_write_with_id_check` (L1290).
- `executor.py:1297-1300` — `else:` → plain `render_step_tool_write`.

So only `generate` and `merge` are routed to the id-checking renderer; that routing is deliberate and correct (those are the two primary phantom-ID surfaces per master:§Top-3 #3).

## 4. Current catch point — MERGE GATE (catches) vs generation (prevents)

There are **two independent enforcement points**, reading **two different sidecars**:

| | Generation-time PREVENTION | Merge-GATE CATCH |
|---|---|---|
| Where | `tool_writer.render_step_tool_write_with_id_check` via `executor.py:1290` | `gates._roadmap_ids_within_spec` (`gates.py:996-1059`), wired as `MERGE_GATE` SemanticCheck `roadmap_ids_within_spec` (`gates.py:1268-1269`) |
| Spec-id source | `config.output_dir/extraction.json` → `roadmap_ids` key (`executor.py:1282-1287`) — **only exists if `tool_write_extract=True`** | `config.output_dir/spec_id_registry.json` built by `build_id_registry()` from the spec directly (`executor.py:649`, `id_registry.py:135-177`) — **always written by extract step** (`executor.py:1368`) |
| Roadmap-id source | `parsed["roadmap_ids"]` from the LLM's structured JSON, BEFORE render | `extract_roadmap_ids(content)` regex-scans the FINAL rendered `roadmap.md` (`id_registry.py:180-194`) |
| When it fires | only when `tool_write_generate`/`tool_write_merge` True AND `extraction.json` present | ALWAYS at merge gate; **fail-shut** if sidecar missing/unreadable (`gates.py:1013-1031`) |
| On phantom | returns errors → no file written (StepResult FAIL, `executor.py:1301-1310`) | returns string → gate FAIL with up to 5 violations (`gates.py:1052-1058`) |

The MERGE GATE is the **catch-all backstop**: always-on, fail-closed, scans the final markdown. R1.4's wording — "catches phantom IDs at the merge gate (fail-closed, correct) but does not yet PREVENT them at generation for all steps" — refers exactly to this asymmetry: the gate runs unconditionally; the generation-time prevention does not.

## 5. THE PREVENTION GAP — defined precisely

Of the three candidate gaps in the brief, the **real** gap the follow-up means ("for all steps") is the compound **(a)+(b)**, with (a) being the central mechanism failure:

**Gap (a) — PRIMARY: the `if spec_ids:` skip is reachable in the default config.** The generation-time check's `spec_ids` is sourced ONLY from `extraction.json` (`executor.py:1282-1287`). `extraction.json` exists ONLY when `tool_write_extract=True` (`models.py:127`, default **False**). Therefore, in any run where extract uses the legacy markdown path but generate/merge are flipped to tool-write (a valid partial-cutover combination), `_spec_ids = set()` → `if spec_ids:` is falsy → the subset check is **skipped** → generate/merge can emit phantom roadmap_ids with no generation-time rejection. The id universe IS knowable (it lives in `spec_id_registry.json` / `envelope.spec_ids`), but the renderer is never handed it. **This is the "does not PREVENT for all steps" gap.**

**Gap (b) — SECONDARY/by-design: the default markdown path has no generation-time id-check at all.** All `tool_write_*` flags default `False` (`models.py:127-133`), so in production `generate`/`merge` run the legacy markdown path and the entire `if _tw_spec is not None and getattr(config, _tw_spec.config_flag, False):` block (`executor.py:1257`) is skipped. The ONLY phantom-ID enforcement on the default path is the merge GATE catch. This is the deliberate dual-write posture (markdown path is production for ≥3 release cycles per Vector A); closing it means making the markdown path id-aware too, OR accepting the gate-only backstop there. The follow-up most plausibly targets (a) (a real hole inside the tool-write path) rather than (b) (a known dual-write tradeoff), but a complete fix should state which surfaces are covered.

**Gap (c) — NOT a gap.** No generate/merge sub-path bypasses the id-check renderer; the `("generate", "merge")` routing (`executor.py:1269`) is exhaustive for the tool-write generate/merge steps.

**Root cause of (a):** the generation-time check and the merge-gate check derive `spec_ids` from **two different, divergent sources**. Merge gate uses `spec_id_registry.json.union_of_known()` (always present, built from the spec). Generation uses `extraction.json.roadmap_ids` (conditionally present, the extract LLM's self-reported id list). Even when both exist they are NOT guaranteed equal: `union_of_known()` is `fr ∪ nfr ∪ sc ∪ g ∪ d ∪ md ∪ accepted_deviations` (`id_registry.py:94-104`) parsed deterministically from the spec; `extraction.json.roadmap_ids` is whatever the extract step emitted. The generation-time gate is both **weaker** (skippable) and **less authoritative** (LLM-reported vs spec-parsed) than the gate it is meant to front-run.

## 6. Is `envelope.spec_ids` available at generation time?

**Yes.** `envelope.spec_ids` is a full `SpecIdRegistry` (`envelope.py:197`), content-identical to `spec_id_registry.json` (`envelope.py:146-151` R0.1 absorption note). The envelope is persisted at `<output_dir>/envelope.json` and loaded inside the executor in `_apply_post_step_envelope_update` (`executor.py:1440-1454`, via `load_envelope`). So the authoritative id universe IS reachable from the executor at the moment the generate/merge render dispatch runs — it is simply **not plumbed** into the `render_step_tool_write_with_id_check` call. The current call re-derives a weaker `_spec_ids` from `extraction.json` instead (`executor.py:1280-1289`). Generation-time prevention is therefore **wire-up-able without new plumbing of any new artifact** — the registry already sits next to the step. Either `spec_id_registry.json` (always written, `executor.py:650`/`1368`) or `envelope.json` can feed it.

## 7. Recommended fix shape (concrete, testable)

The fix has two halves: (1) feed the renderer the AUTHORITATIVE id universe, and (2) make the skip non-reachable when that universe is known.

### Fix 1 — executor: derive `_spec_ids` from the always-present authoritative registry

`executor.py:1280-1289`. Replace the `extraction.json` → `roadmap_ids` derivation with a read of `spec_id_registry.json` (always written by the extract step regardless of `tool_write_extract`) and use `union_of_known()`. Also pass `accepted_deviations` from the same registry instead of hard-coded `None` (`executor.py:1295`). Sketch (shape, not literal):

```python
_spec_ids: set[str] = set()
_accepted: set[str] = set()
try:
    _reg_path = config.output_dir / "spec_id_registry.json"   # always written
    if _reg_path.exists():
        from .id_registry import SpecIdRegistry
        _payload = json.loads(_reg_path.read_text(encoding="utf-8"))
        _reg = SpecIdRegistry(... from _payload ...)            # same construction as gates.py:1034
        _spec_ids = set(_reg.union_of_known())                 # spec-parsed, authoritative
        _accepted = set(_reg.accepted_deviation_ids)
except (OSError, ValueError):
    _spec_ids = set()
_tw_errors = render_step_tool_write_with_id_check(
    _tw_key, _json_text, step.output_file,
    spec_ids=_spec_ids, accepted_deviations=_accepted,
)
```

Effect: closes gap (a) — when extract ran markdown-only but generate/merge are tool-write, `spec_id_registry.json` STILL exists, so `_spec_ids` is non-empty and the subset check fires. Also collapses the divergence in §5 root-cause: generation-time and merge-gate now use the **same** id universe (`union_of_known()`), so a phantom rejected at the gate is now rejected at generation, and vice versa. Reuse the existing `SpecIdRegistry`-from-payload construction (mirror `gates.py:1034-1045`); factor it to a shared helper to honor Contract #8 (no duplicate parse logic).

### Fix 2 — tool_writer: make the skip a deliberate, narrow contract, not an accident

`tool_writer.py:487`. The `if spec_ids:` skip should remain ONLY as the legitimate identity case (extract step, where the inclusion is trivially true). For generate/merge, the universe is always knowable post-Fix-1, so the skip becomes unreachable in practice. Two options, in increasing strictness:

- **2a (minimal, recommended):** leave the `if spec_ids:` guard but rely on Fix 1 guaranteeing `spec_ids` non-empty for generate/merge. Add a callsite assertion / log at `executor.py` that `_spec_ids` is non-empty for `("generate","merge")` and surface a hard StepResult FAIL if `spec_id_registry.json` is missing — i.e. **fail-shut on a missing universe** for the two primary surfaces, matching the merge gate's fail-shut posture (`gates.py:1013-1018`). This makes "I couldn't find the id universe" a loud failure, not a silent skip.
- **2b (stricter, optional):** add a `require_spec_ids: bool = False` parameter to `render_step_tool_write_with_id_check`; when `True` (passed for generate/merge), an empty `spec_ids` returns a hard error string instead of skipping. Keeps the renderer self-defending even if a future caller forgets Fix 1.

**Recommendation:** Fix 1 + Fix 2a. Fix 1 is the load-bearing change (authoritative source + closes the skip in the realistic config); Fix 2a converts the residual "no universe" case into a fail-shut on the two primary surfaces without touching the renderer's signature.

### Deterministically testable vs prompt-only

- **Deterministic (no LLM):** ALL of the prevention is testable without a model. `render_step_tool_write_with_id_check("generate", json_with_FR99, out, spec_ids={"FR-1"})` must return a non-empty error list and write NO file. Feed `extraction.json`-absent + `spec_id_registry.json`-present fixtures to the executor dispatch and assert the subset check still fires (the regression for gap (a)). Assert `union_of_known()`-sourced `_spec_ids` equals the merge-gate universe for the same fixture (divergence-closure test).
- **Prompt-only:** nothing here depends on prompt wording. The schema `$comment` strings already advertise the runtime constraint; they are advisory, not load-bearing. R7 owns the test design — this section only states WHAT must hold.

## 8. PRESERVE constraints (do not break)

1. **Merge-gate catch must remain** (`gates._roadmap_ids_within_spec`, `gates.py:996`, wired `gates.py:1268`). Generation-time prevention is defense-in-depth ADDED IN FRONT of the gate, never a replacement. The gate's fail-shut on missing sidecar (`gates.py:1013-1031`) stays.
2. **Default markdown path must keep working.** Fixes 1-2 live entirely inside the `if _tw_spec is not None and getattr(config, _tw_spec.config_flag, False):` tool-write block (`executor.py:1257`). When `tool_write_generate`/`tool_write_merge` are False (production default), nothing changes; the merge gate alone enforces (gap (b) intentionally left to the gate per dual-write posture).
3. **`accepted_deviations` handling preserved.** Today the executor passes `accepted_deviations=None` (`executor.py:1295`); Fix 1 IMPROVES this by sourcing `accepted_deviation_ids` from the registry, matching the merge gate's `union_of_known()` which already folds accepted deviations in (`id_registry.py:94-104`). `validate_id_subset` already unions `accepted_deviations` (`tool_writer.py:365`) — keep that.
4. **Plain `render_step_tool_write` untouched** — non-generate/merge steps keep the no-id-check path (`executor.py:1297-1300`); extract is the SOURCE of the universe so a subset check there is the identity.
5. **Contract #8 (no duplicate regex/parse).** Reuse `SpecIdRegistry`/`union_of_known`/`build_id_registry` rather than re-deriving id sets; factor the sidecar→`SpecIdRegistry` construction shared by `gates.py:1034` and the new executor read into one helper.

---

- **Status:** Complete

## Summary

`validate_id_subset` (`tool_writer.py:344`) and `render_step_tool_write_with_id_check` (`tool_writer.py:455`) already implement correct generation-time phantom-ID rejection for the `generate` and `merge` steps (routed at `executor.py:1269/1290`). The defect is in HOW the executor sources `spec_ids` for that renderer and in the `if spec_ids:` skip.

### Prevention gap verdict

The gap is **(a) the skippable subset check**: the generation-time `spec_ids` is derived solely from `extraction.json` (`executor.py:1282-1287`), which exists only when `tool_write_extract=True` (default False, `models.py:127`). In a partial cutover (extract markdown, generate/merge tool-write) `_spec_ids` is empty, the `if spec_ids:` guard (`tool_writer.py:487`) is falsy, and the subset check is SKIPPED — so generate/merge can emit phantom roadmap_ids with no generation-time rejection, relying entirely on the always-on, fail-shut MERGE GATE (`gates._roadmap_ids_within_spec`, `gates.py:996`) to catch them downstream. Root cause: generation-time and merge-gate enforcement read two divergent, non-equal id sources (`extraction.json.roadmap_ids` — LLM-reported, conditional — vs `spec_id_registry.json.union_of_known()` — spec-parsed, always present). Candidate (b) (default markdown path has no generation-time check) is real but by-design under the dual-write posture; candidate (c) is not a gap (routing is exhaustive).

### Recommended fix shape

1. **executor (`executor.py:1280-1295`):** source `_spec_ids` (and `accepted_deviations`) from `spec_id_registry.json` via `SpecIdRegistry.union_of_known()` (always written, `executor.py:650/1368`; same universe the merge gate uses) instead of `extraction.json`. This closes the skip in the realistic config AND collapses the generation-vs-gate divergence.
2. **executor fail-shut:** for `("generate","merge")`, a MISSING `spec_id_registry.json` should be a hard StepResult FAIL (mirroring the gate's fail-shut, `gates.py:1013`), not a silent empty-set skip.
3. **tool_writer (optional, `tool_writer.py:455`):** add `require_spec_ids=True` for generate/merge so empty `spec_ids` errors instead of skipping (self-defending renderer).
4. Deterministically testable end-to-end (no LLM): phantom id → non-empty errors + no file written; `extraction.json`-absent/`spec_id_registry.json`-present fixture → check still fires; generation universe == gate universe. PRESERVE: merge-gate catch (defense-in-depth), default markdown path, `accepted_deviations` union, plain-renderer path for non-generate/merge steps, Contract #8 reuse.
