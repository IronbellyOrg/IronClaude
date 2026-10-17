---
title: "PRD pipeline — remove `--file` local-path misuse (session-token crash fix)"
status: draft
type: bug-fix design spec
created: 2026-06-09
repo: IronbellyOrg/IronClaude
branch: fix/prd-local-file-no-session-token
scope: src/superclaude/cli/prd/{process.py,prompts.py} + tests
owner: prd-pipeline
---

# PRD pipeline — remove `--file` local-path misuse

## 1. Summary

The PRD CLI pipeline passes **local filesystem paths** to the `claude` CLI's
`--file` flag. `--file` is a **cloud download mechanism** (`file_id:relative_path`)
that (a) requires `CLAUDE_CODE_SESSION_ACCESS_TOKEN` and (b) per IronClaude's own
sibling-pipeline contracts "does not inject local file content". In a headless run
(no session token) the `claude` subprocess exits 1 in ~0.3 s with
`Error: Session token required for file downloads. CLAUDE_CODE_SESSION_ACCESS_TOKEN
must be set.`, crashlooping the pipeline at `scope-discovery`.

This spec removes the `--file` misuse and delivers local content the way every
other pipeline already does — **inline in the prompt** — eliminating the
session-token dependency. No pipeline redesign.

## 2. Root cause (evidence)

| Fact | Evidence |
|------|----------|
| PRD emits `--file <local_path>` for refs >50 KB | `src/superclaude/cli/prd/process.py:198-199` (`file_args.extend(["--file", str(ref_path)])`) |
| PRD emits `--file <local_path>` for every `--spec` file, unconditionally, on `scope-discovery`/`investigation` | `process.py:201-204` + `_SPEC_FILE_STEPS` (`process.py:121`) |
| `extra_args` (= these file_args) is appended verbatim to the claude argv | `src/superclaude/cli/pipeline/process.py:94` (`cmd.extend(self.extra_args)`) |
| `--file` is cloud-only: `File resources to download at startup. Format: file_id:relative_path` | `claude --help` |
| Sibling pipelines deliberately pass **no** `--file` and say why | `roadmap/executor.py:8-9`, `tasklist/executor.py:10`, `roadmap/validate_executor.py:11` ("--file is a cloud download mechanism and does not inject local file content"; FR-003/FR-023) |
| The crash | `.dev/releases/scp-run-2/prd-octodive/scope-discovery-error.txt` (octodive repo); exit 1, 0.27 s, 3× crashloop |
| Older run with **no** `--spec` never hit this | `scp-run` (`parsed-request.json` has no `SPECS`); ran `scope-discovery` 153 s, failed only a content gate |

**Why only PRD is affected:** it is the only pipeline that passes `--file`.

## 3. Existing machinery (reused, not reinvented)

- `prompts.py:42` `_read_file(path, max_bytes=50_000)` + `_TRUNCATION_MARKER` (`prompts.py:34`) — inline-with-cap.
- `prompts.py:120` `_authoritative_specs_block(spec_paths)` — Phase-1 paths-only block ("AUTHORITATIVE SPECIFICATIONS … You MUST Read each one IN FULL"), called at `prompts.py:247` (scope-discovery) and `prompts.py:919` (investigation).
- Per-step refs are **already inlined** by name via `_read_file` (e.g. `prompts.py:514-518`), independent of `_build_file_args`.

**Measured:** all PRD refs are <50 KB (largest `agent-prompts.md` = 22.8 KB), so the
refs `--file` branch is **dead in practice** — those refs are already inlined in
full. Removing it is a no-op for current content.

## 4. Options considered

### Option A — paths-only (minimal)
Delete both `--file` branches; rely on the existing paths-only
`_authoritative_specs_block` (specs) and the prompt builder's existing refs inline.
- ➕ Smallest diff; restores the originally-designed token-safe Phase-1 behavior.
- ➖ Specs reach the model **only if the agent chooses to Read the path** — the
  documented #1 risk in the original `--spec` brainstorm ("agent under-reads the path").

### Option B — inline-with-cap (RECOMMENDED)
Delete both `--file` branches **and** upgrade `_authoritative_specs_block` to embed
each spec's **content** verbatim (capped via `_read_file`), keeping the imperative
"Read in full" instruction as a fallback for any truncated spec.
- ➕ Spec content is **guaranteed in-context**, token-free, no reliance on agent Read behavior.
- ➕ Realizes the "Phase 2 inline-with-cap" the original `--spec` design deferred
  (`.dev/brainstorms/20260604-121050-prd-spec-flag-refactor/merged-requirements.md` §R4).
- ➕ Reuses existing `_read_file`/`_TRUNCATION_MARKER`; refs need no change (already inlined).
- ➖ Slightly larger diff (one function body) — acceptable.

**Decision: Option B.** Specs are the operator's ground truth; deterministic
in-context delivery is the entire purpose of `--spec`. Current specs are all
<50 KB, so they inline in full.

## 5. Changes

### 5.1 `src/superclaude/cli/prd/process.py`
- Remove the refs `--file` branch (`:198-199`) and the spec `--file` branch (`:201-204`).
- `_build_file_args` now has no `--file` to emit. **Remove the method and its
  `extra_args=file_args` wiring** (`:154-155`, `:166`), passing no `extra_args`
  (matching the sibling pipelines), **OR** retain it returning `[]` if the implementer
  prefers a smaller diff — verdict left to implementation, but no `--file` may remain.
- Remove now-dead module constants **only after confirming no other references**:
  `_FILE_SIZE_THRESHOLD` (`:115`), `_SPEC_FILE_STEPS` (`:121`), and `_PHASE_ALLOWED_REFS`
  (`:95-113`) if used solely by `_build_file_args`. (Grep before deleting; refs inlining
  in `prompts.py` uses literal names, not this map.)
- Update the class docstring (`:132-135`) and module docstring (`:4,11`) that advertise
  "Phase-aware `--file` arg construction" to reflect inline delivery.

### 5.2 `src/superclaude/cli/prd/prompts.py`
- Upgrade `_authoritative_specs_block(spec_paths)` (`:120-138`): for each path, embed
  `_read_file(Path(p))` content under a clearly-delimited per-spec header, retaining the
  "AUTHORITATIVE … MUST Read IN FULL (if truncated)" instruction. Preserve the empty-input
  contract (return `""` when no specs → byte-identical no-spec prompts). Signature unchanged;
  callers at `:247` and `:919` unchanged.
- **MANDATORY missing-path guard (per research gate GAP-2/GAP-3).** The block is invoked
  with paths from the persisted `parsed-request.json` `SPECS` array (`prompts.py:247-249`,
  `:919`; `_bind_specs` at `executor.py:1437`), NOT the Click-validated `config.spec_files`.
  On **resume** those paths can be missing/stale and `_bind_specs` tolerates them
  (`executor.py:1357-1360`). Therefore, for each path: **if `Path(p).is_file()` → inline
  `_read_file` content; else → fall back to the current path-only line (never call
  `_read_file` on it).** An unguarded read raises bare `FileNotFoundError` inside
  `build_scope_discovery_prompt`, which the executor only catches as `MissingArtifactError`
  → it would re-introduce a crash on the *same* `scope-discovery` step (token crash traded
  for a file-read crash). The guard also keeps the existing fake-path injection tests green
  (missing paths still render as a path).

### 5.3 No other call sites
`grep -rn '"--file"' src/superclaude/cli/prd/` must return **zero** matches after the change.

## 6. Backward-compatibility & regression

- **Runs without `--spec`**: `_authoritative_specs_block` returns `""` on empty input →
  prompts byte-identical to today. No behavior change.
- **Refs**: already inlined by the prompt builder; all current refs <50 KB → no truncation,
  no loss. Any future >50 KB ref is inlined truncated-at-50 KB with `_TRUNCATION_MARKER`
  (same cap the prompt builder already applies) — not silently dropped.
- **Determinism of `--spec`**: force-bind is unchanged (specs are still bound into
  `SPECS`/`WHERE` by `_bind_specs`); Option B strengthens it (content, not just a path).
- **Env**: no dependency on `CLAUDE_CODE_SESSION_ACCESS_TOKEN` anywhere in the PRD path.

## 7. Test plan (`uv run pytest`)

1. **No `--file` emitted** — invert/replace `tests/cli/prd/test_spec_flag.py::TestSpecFileAttach`
   (:459-515, the ONLY `--file` test): for `scope-discovery` and `investigation` with
   `config.spec_files=[tmp_spec]`, assert the built argv / `extra_args` contains **no** `"--file"`.
   Remove the `== []` cases that name the deleted `_build_file_args` symbol.
2. **Spec content reaches the prompt (Option B)** — real `tmp_path` spec with a UNIQUE_MARKER →
   `_authoritative_specs_block([str(p)])` output contains the marker (content inlined) AND
   `AUTHORITATIVE SPECIFICATIONS`; a >50 KB `tmp_path` spec → output contains `_TRUNCATION_MARKER`.
3. **Missing-path guard** — `_authoritative_specs_block(["/nope/missing.md"])` returns a block
   containing the path string and does **NOT** raise (Decision 1 / GAP-2/3).
4. **No-spec parity** — `_authoritative_specs_block(None)` and `([])` return `""` (existing lock
   at `test_spec_flag.py:310-312` stays green); no-spec scope-discovery prompt unchanged.
5. **Keep green (do NOT migrate/delete)** — the prompt-injection tests that bind non-existent
   paths and assert the path appears stay valid via the Decision 1 fallback. Leave
   `tests/pipeline/test_process.py:78-81` (base-class `--file` support) untouched — out of scope.
6. **No dead `--file`** — grep guard: `grep -rn '"--file"' src/superclaude/cli/prd/` → 0 matches.
7. **Acceptance (manual/integration)** — `superclaude prd run "…" --spec … --output …` in a
   shell with `CLAUDE_CODE_SESSION_ACCESS_TOKEN` **unset** advances past `scope-discovery`
   (no "Session token required" error in `scope-discovery-error.txt`).

## 8. Acceptance criteria

- [ ] `grep -rn '"--file"' src/superclaude/cli/prd/` → 0 matches.
- [ ] New/updated unit tests (§7.1–7.4) pass under `uv run pytest`.
- [ ] `make sync-dev && make verify-sync` clean.
- [ ] A headless PRD run with `--spec` and no session token reaches `research-notes`
      (i.e. clears `scope-discovery`) — verified against the octodive repro.
- [ ] No change to prompts for runs that use neither `--spec` nor a >50 KB ref.

## 9. Out of scope

- Executor fail-fast / crashloop hardening on `scope-discovery` exit≠0 (separate follow-up).
- Any change to sibling pipelines.
- Raising the 50 KB inline cap or adding a digest for >50 KB specs (the deferred
  "Phase 2 heuristic digest"); current specs/refs are all <50 KB.

## 10. Rollout

Edit `src/superclaude/cli/prd/` → `make sync-dev` → `make verify-sync` →
`uv run pytest` → single PR on `fix/prd-local-file-no-session-token` →
`IronbellyOrg/IronClaude`.
