# Design: `superclaude prd run --spec FILE` (deterministic spec ingestion)

**Status:** Phase 1 implementation (paths-only binding)
**Branch:** `feature/prd-spec-flag`
**Source of truth:** `src/superclaude/cli/prd/` → `make sync-dev` → `.claude/`
**Origin:** 3-agent adversarial brainstorm (convergence ≈ 0.85), verified 1:1 against current source on 2026-06-04.

---

## Problem statement & root cause (verified against source)

`--where` (repeatable dirs) is the only source-location input and is **effectively inert** for the
steps that decide what gets read:

- `--where` → stored in `PrdConfig.where` (`models.py:182`) but **never injected into the
  parse-request prompt**. `build_parse_request_prompt` (`prompts.py:60`) builds from
  `config.user_message` + `context_summaries` only; it instructs the LLM to *invent its own*
  `WHERE` list (`prompts.py:101-102`).
- `build_scope_discovery_prompt` (`prompts.py:110`) does
  `parsed = _load_json(task_dir/"parsed-request.json")` (`prompts.py:116`) and uses
  `parsed["WHERE"]` (`prompts.py:117-119`) — **not** `config.where`.
- `config.where` only resurfaces as a late fallback for investigation-agent file lists
  (`prompts.py:670`).

**Observed failure:** a run with `--where _bmad-output/...` had its WHERE silently replaced by an
LLM-guessed `[".dev/specs/", ".dev/research/", ".dev/historical/"]`; scope-discovery then produced a
40-line doc that tripped the `min_lines=50` STANDARD gate (`gates.py:324-327`) — non-fatal, so the
run continued on a thin foundation.

---

## R1 — Flag semantics

- Add `--spec / -s` to `prd run`: `multiple=True`,
  `type=click.Path(exists=True, dir_okay=False, resolve_path=True)`. (`--where` has no `type=` — part
  of why it is inert.)
- Repeatable; each value = one authoritative spec file. Composes with `--where`. `--spec` softly
  implies a `--where` of its parent dir (never the reverse). Empty default ⇒ fully backward
  compatible.

## R2 — Config / data contract

- `PrdConfig` gains `spec_files: list[str] = field(default_factory=list)` (near `models.py:182`).
- `resolve_config` (`config.py:46-144`) accepts `spec`, validates+resolves each to absolute, and
  populates `spec_files`. Click already enforces existence/file-ness via `Path(exists=True,
  dir_okay=False)`; `resolve_config` resolves to absolute defensively for direct (non-CLI) callers.
- `parsed-request.json` gains a Python-owned `SPECS` array (objects: `path`, `size`, `inlined`,
  `truncated`) AND the executor force-prepends spec parent dirs into the existing `WHERE` array.
- Phase 2 only: optional `spec_digest: str | None` on `PrdConfig`.

## R3 — Binding point (the crux)

- New executor helper `_bind_specs(parsed: dict) -> dict`, called **after** parse-request persists
  `parsed-request.json` (`executor.py:636-637`) and **before** scope-discovery loads it
  (`prompts.py:116`). It writes `SPECS` + merges spec parent dirs into `WHERE`, then re-persists.
  Deterministic: pure-Python, post-LLM, pre-consumer. The seam is the Stage-A loop in
  `PrdExecutor.run` (`executor.py:457-480`): after the `parse-request` iteration returns, before the
  `scope-discovery` iteration runs.
- Rejected: `context_summaries` seam (broadcasts to all builders). Runner-up (defer): a dedicated
  `ingest-spec` Stage-A step for verbatim content embedding.

## R4 — Content flow (PHASED)

- **Phase 1 — paths only (implemented):** when `SPECS` non-empty, amend scope-discovery +
  investigation prompts with an imperative block: "These are AUTHORITATIVE specs — you MUST Read each
  in full: <paths>".
- **Phase 1.5 — `--file` content delivery (implemented):** for the spec-consuming steps
  (`_SPEC_FILE_STEPS = {scope-discovery, investigation}`) the executor's subprocess **attaches each
  spec via the existing `--file` mechanism** so the agent receives the spec *content*, not merely a
  path it is told to Read. This **reuses** `PrdClaudeProcess._build_file_args`
  (`process.py:163-205`) rather than introducing a parallel attach path, and directly mitigates the
  ranked under-read risk (#2). Paths-only framing (Phase 1) + content delivery (Phase 1.5) compose:
  the prompt names the files as authoritative AND the bytes are present.
- **Phase 2 — inline/size-aware delivery (deferred, MUST reuse `process.py`):** when spec content
  should be *inlined into the prompt* (not just attached), route the inline-vs-attach decision through
  the **existing** `_FILE_SIZE_THRESHOLD` (`process.py:115`) / `_build_file_args` machinery — do NOT
  build a second size-threshold engine in `executor.py`/`prompts.py`. The heuristic-digest step (H1 +
  first paragraph + promoted tables/code-fences/bold requirement lines, no extra LLM call) and the
  `inlined`/`truncated` flag population layer on top of that shared cutoff. Rationale: an
  `/sc:analyze` review found the original Phase 2 plan would duplicate `process.py`'s threshold logic,
  guaranteeing future drift between two cutoffs.

## R5 — Gate implications

- Keep scope-discovery `min_lines=50` STANDARD (`gates.py:324-327`); do NOT make it STRICT on
  `--spec` — risks halting legit runs. Authoritative spec content should clear 50 lines naturally.
- Make silent degradation louder: when `SPECS` non-empty AND scope-discovery still `VALIDATION_FAIL`s
  (non-fatal STANDARD path), emit a prominent WARN naming the specs.

## R6 — Backward compatibility & resume

- `spec_files == []` ⇒ zero behavioral change (no prompt deltas, no artifact mutation). Bare-request
  and `--where`-only runs identical to today — protected with tests (byte-identical prompt lock).
- Phase 1: do NOT add `--spec` to `prd resume`. Post-parse, the binding lives in persisted
  `parsed-request.json`, so resume past parse carries it; pre-parse interruption ⇒ re-run
  `prd run --spec`. Revisit in Phase 2.

## R7 — Source-of-truth workflow (MANDATORY)

- Edit `src/superclaude/cli/prd/` → `make sync-dev` → `make verify-sync` → `uv run pytest`.

---

## Implementation surface (file → change)

| File | Change |
|------|--------|
| `commands.py` | Add `--spec/-s` option to `run` (after `--where`, ~`:46`); pass `spec` to `resolve_config` (~`:104`). |
| `config.py` | `resolve_config` gains `spec` param; validate/resolve each to absolute; populate `PrdConfig.spec_files`. |
| `models.py` | `spec_files: list[str]` field (near `:182`); Phase 2 `spec_digest`. |
| `executor.py` | `_bind_specs()`; call between parse-request persist and scope-discovery load. Phase-1 loud-WARN path on SPECS-present VALIDATION_FAIL. |
| `prompts.py` | Conditional AUTHORITATIVE-SPECS block in `build_scope_discovery_prompt` (`:110`) and the investigation builder (`:653-672` / `_render_investigation_prompt:736`) when `SPECS` present. |
| `process.py` | **Phase 1.5:** `_SPEC_FILE_STEPS` constant + `_build_file_args` appends `--file <spec>` for each `config.spec_files` entry on spec-consuming steps. Reuses the existing `--file`/`_FILE_SIZE_THRESHOLD` mechanism (the consolidation point for Phase 2). |
| `gates.py` | Thresholds unchanged. |

## SPECS object schema (in `parsed-request.json`)

```json
{
  "SPECS": [
    {"path": "/abs/path/SPEC.md", "size": 4096, "inlined": false, "truncated": false}
  ]
}
```

- `path`: absolute resolved path to the spec file.
- `size`: byte size on disk (0 if unreadable).
- `inlined`: Phase 1 always `false` (paths-only). Phase 2 sets `true` when content embedded.
- `truncated`: Phase 1 always `false`. Phase 2 sets `true` when content was capped.

Schema is **additive-only**; downstream readers use `.get("SPECS", [])`.

---

## Top risks (ranked)

1. Editing the venv copy instead of `src/superclaude/` → mitigate via R7 + `make verify-sync`.
2. Agent under-reads a bound path (gate non-fatal → silent quality drop) → **mitigated in Phase 1.5**
   by `--file` content delivery (`process.py`); R5 WARN as backstop; Phase 2 inline for the rest.
3. Digest drops acceptance criteria / API signatures (Phase 2) → promote tables/code/bold; flag truncation.
4. Token blowup from large/many specs (Phase 2) → caps + truncation order.
5. `parsed-request.json` schema drift breaks downstream readers → additive-only; `.get("SPECS", [])`.

---

## Test plan (acceptance criteria → concrete tests)

1. **CLI parse** (`test_cli_smoke.py`): `prd run` accepts repeated `--spec a.md --spec b.md`; rejects a
   directory and a nonexistent path (Click `Path(exists=True, dir_okay=False)`); `--help` lists `--spec`.
2. **Config** (`test_config.py`): `resolve_config(..., spec=("a.md",))` populates `PrdConfig.spec_files`
   with absolute resolved paths; empty when omitted.
3. **Model** (`test_models.py`): `PrdConfig.spec_files` defaults to `[]`.
4. **Binding** (`test_executor.py`): `_bind_specs({...})` adds a `SPECS` array (with
   `path/size/inlined/truncated`) and prepends spec parent dirs into `WHERE`; idempotent; safe when no specs.
5. **Prompt injection** (`test_prompts.py`): with `SPECS` present, `build_scope_discovery_prompt` contains
   the imperative AUTHORITATIVE-SPECS block + the exact paths; with no specs, the prompt is **byte-identical
   to today** (backward-compat lock).
6. **Gate behavior** (`test_gates.py`): scope-discovery gate threshold unchanged (`min_lines=50`, STANDARD);
   WARN emitted when `SPECS` present and gate fails.
7. **Backward compat** (`test_integration.py` / `test_e2e.py`): a `--where`-only run and a bare-request run
   produce unchanged `parsed-request.json` shape (no `SPECS` key, or `SPECS: []`) and unchanged prompts.
8. **Resume** (`test_resume_skip.py`): resuming after parse-request carries the bound `SPECS`/`WHERE` from
   the persisted artifact without `--spec`.
9. **Phase 1.5 `--file` attach** (`test_spec_flag.py::TestSpecFileAttach`): `_build_file_args` appends
   `--file <spec>` for each `spec_files` entry on `scope-discovery` and `investigation-N`; none on
   `parse-request`; empty when no specs; missing spec files skipped.

All tests above live in `tests/cli/prd/test_spec_flag.py` (cohesive feature suite, 27 tests) rather than
scattered across the per-surface files; the parenthetical file names indicate the acceptance surface each
maps to.

**Definition of done:** `uv run pytest tests/cli/prd/ -v` green; `make verify-sync` clean; `--spec
./SPEC.md` demonstrably forces that file's path into `parsed-request.json` `SPECS` + `WHERE` regardless of
LLM behavior; `--where`-only and bare runs provably unchanged.
