# Adversarial Operational-Correctness QA — TASK-RF-prd-local-file-20260609-005242

**Lens:** Operational correctness (would the task FAIL if executed?). Read-only.
**Reviewer stance:** Assume the task breaks on execution; find the breakages.
**Target repo:** `/config/workspace/IronClaude`
**Date:** 2026-06-09

Verified the ACTUAL target source files, not just the task file's claims.

---

## Item-by-item operational verification

### (1) Will removing `_build_file_args` + `extra_args=file_args` leave `PrdClaudeProcess.__init__` valid? — PASS

Read `src/superclaude/cli/prd/process.py:138-206` and the base
`src/superclaude/cli/pipeline/process.py:37-95`.

- `__init__` wiring confirmed at the cited anchors:
  - `:154-155` comment `# Build --file args from phase-allowed refs` + `file_args = self._build_file_args(config, step_id)`
  - `:166` `extra_args=file_args` inside `super().__init__(...)`
- Base `ClaudeProcess.__init__` (`pipeline/process.py:48`) declares
  `extra_args: list[str] | None = None`; `:63` `self.extra_args = extra_args or []`;
  `build_command()` `:94` `cmd.extend(self.extra_args)`. With no `extra_args` passed,
  this extends with `[]` → genuine no-op, **no `--file` token emitted**. Target end-state holds.
- The remaining `super().__init__` kwargs (prompt, output_file, error_file, max_turns,
  model, permission_flag, timeout_seconds, output_format) are all still supplied and valid.
- **Caller safety (Decision 4):** the SOLE `PrdClaudeProcess` constructor at
  `executor.py:714-721` passes ONLY `config, step_id, prompt, output_file, error_file,
  timeout_seconds` — NO `extra_args`. Repo-wide grep for `_build_file_args` shows refs only
  in process.py (def+call) and test_spec_flag.py. Removing the internal wiring breaks no caller.

Verdict: removing the method + the `extra_args=file_args` kwarg leaves a valid constructor.

### (2) Does the prompts.py Phase-3 guard produce non-raising code that inlines real content? — PASS (design is sound)

Read `prompts.py:34, 42-47, 120-138, 247-249, 919` and the refs-inline idiom `:507-573`.

- `_read_file(path, max_bytes=50_000)` (`:42-47`) does `path.read_text(...)` with NO existence
  guard → raises `FileNotFoundError` on a missing path. Decision 1's premise is REAL: an
  *unguarded* `_read_file` inside `_authoritative_specs_block` would raise on a stale SPECS path.
- Confirmed the executor catches only `MissingArtifactError` (a `FileNotFoundError` *subclass*,
  `prompts.py:50-64`) at the `_build_prompt` site (`executor.py:~695-707` HALT path). A *bare*
  `FileNotFoundError` from `_read_file` is NOT that subclass, so it would escape as an uncaught
  traceback / re-crash `scope-discovery` on resume. The MANDATORY `Path(p).is_file()` guard the
  task prescribes is therefore genuinely load-bearing, not decorative.
- The existing literal refs-inline pattern (`:514-518` + `---`-fenced sections `:546-573`) gives
  the executor a concrete, working idiom to mirror for the per-spec header + content fence.
- Empty-input contract (`if not spec_paths: return ""`, `:130-131`) and the required substrings
  (`AUTHORITATIVE SPECIFICATIONS`, `MUST Read each one IN FULL`, `:134-135`) are present in the
  current code and the task explicitly preserves them. Both call sites (`:247-249`, `:919`) pass
  `list[str]`/`list[str]|None` and are left unchanged — signature `spec_paths: list[str] | None`
  is compatible.

Verdict: the Phase-3 design, if implemented as written (guard EVERY path, reuse `_read_file`),
produces code that inlines real content and never raises on missing paths. No operational defect
in the *instructions*. (Caveat: correctness depends on the executor actually wrapping each path in
`Path(p).is_file()`; Step 3.1 states this as MANDATORY for EVERY path.)

### (3) Will the inverted `TestSpecFileAttach` assertions pass against post-fix code? — PASS

Read `tests/cli/prd/test_spec_flag.py:459-516`. The current class matches the task's description
EXACTLY:
- `test_scope_discovery_attaches_each_spec` (:478-487) asserts `args == ["--file", str(a), "--file", str(b)]`
- `test_investigation_numbered_step_attaches_specs` (:489-498) asserts `"--file" in args`
- three `== []` tests (:500-515) all call `PrdClaudeProcess._build_file_args(...)`

Post-fix, `_build_file_args` is DELETED. The task correctly prescribes:
- (a) rewrite the banner comment (:459-462 still says "via the existing --file mechanism" — stale);
- (b) INVERT the two hard-asserting tests to assert `"--file" not in <argv>`;
- (c) DELETE the three `== []` tests (they reference the removed staticmethod and would raise
  `AttributeError`, NOT fail-soft). Deletion is the correct operational call.

The inversion as described will pass against the post-fix surface (build the command via
`PrdClaudeProcess(...).build_command()` / the base `build_command`, which extends with an empty
`extra_args` → no `--file`). No operational flaw in the test plan.

### (4) Does `grep -rn '"--file"' src/superclaude/cli/prd/` return 0 post-fix? — PASS

Ran the guard NOW: returns EXACTLY two hits — `process.py:199` and `process.py:204` — both removed
by Phase 2 (Steps 2.2/2.3). A broader `grep -rn -- '--file'` shows the only OTHER occurrences are
docstring/comment prose (`process.py:4,11,94,115,119,133,154,171,175,181,183`) and one comment in
`executor.py:1344` ("repeated --file attachments"). NONE of those match the QUOTED `"--file"`
pattern, so the acceptance guard is unaffected by them. Step 2.6 additionally rewrites the
process.py docstring/comment prose, but that is cosmetic w.r.t. the guard.

Confirmed: after Phase 2 removes lines 199 & 204, the exact guard returns 0 matches (PASS).
No stray `"--file"` quoted string elsewhere in `cli/prd/`.

### (5) Is `make verify-sync` genuinely clean for a cli-only change? — PASS

Read the `sync-dev` and `verify-sync` Makefile target bodies (Makefile :109-164, :166-353).
Both targets operate EXCLUSIVELY on:
- `src/superclaude/skills/` ↔ `.claude/skills/`
- `src/superclaude/agents/` ↔ `.claude/agents/`
- `src/superclaude/commands/` ↔ `.claude/commands/sc/`
- `src/superclaude/hooks/scripts/` ↔ `.claude/hooks/` (+ `_FRESHNESS_SCRIPTS` registration)
- `src/superclaude/templates/` ↔ `.claude/templates/`
- hooks.json ↔ auggie-flag-clear.sh cross-consistency

NOTHING under `src/superclaude/cli/` is touched or diffed. A change confined to
`cli/prd/{process.py,prompts.py}` + `tests/cli/prd/` produces ZERO drift signal. `verify-sync`
exits 0 (clean). The task correctly frames this as a no-op drift guard, NOT a propagation step,
and warns NOT to expect cli files under `.claude/`. Operationally accurate.

### (6) Command-precondition failures? — PASS (no blocking precondition failures)

- `uv` present at `/config/.local/bin/uv` → `uv run pytest tests/cli/prd/ -q` is runnable.
- `tests/cli/prd/` exists and contains `test_spec_flag.py` (+ siblings).
- `git rev-parse HEAD` works → returns `ac80f176...`. (NOTE: frontmatter `start_commit:` is empty
  `""`; Step 1.3 captures the live SHA into it — no precondition failure, the empty value is the
  intended-to-be-filled slot. The Post-Completion reflect command has a documented
  `git merge-base HEAD main` fallback if unset.)
- Step 2.1 pre-deletion grep verified live: the three constants
  (`_PHASE_ALLOWED_REFS`/`_FILE_SIZE_THRESHOLD`/`_SPEC_FILE_STEPS`) have refs ONLY inside
  process.py (defs + uses inside `_build_file_args` + docstring `:180`); ZERO test/external refs →
  Step 2.5's CONFIRMED-DEAD gate will pass and the deletes are safe.
- prompts.py inlines refs by LITERAL filename (`:514-518`), NOT via `_PHASE_ALLOWED_REFS` →
  Step 2.1's prompts.py literal-name check is satisfied.

No command in the task hits a hard precondition failure.

---

## Anchor drift check (load-bearing line numbers)

Spot-checked the task's cited anchors against the LIVE files. All resolve at/near the cited lines:
- process.py: `:199` refs emission ✔, `:204` spec emission ✔, `:169-170` def ✔, `:154-155` call ✔,
  `:166` `extra_args=file_args` ✔, `:95/:115/:121` constants ✔, docstrings `:4/:11/:133` ✔.
- prompts.py: `:120` def ✔, `:130-131` early return ✔, `:34` `_TRUNCATION_MARKER` ✔, `:42` `_read_file` ✔,
  call sites `:247-249`/`:919` ✔, `:128` stale "Phase 1 (paths-only)" docstring line ✔.
- test_spec_flag.py: `:459-515` `TestSpecFileAttach` ✔, `:36` import ✔, `:310-312` empty-input lock ✔,
  `:465-474` `_spec_config` helper ✔.

The Phase-1 anchor-reverify step is genuinely satisfiable; no anchor is MISSING or materially DRIFTED.

---

## Minor / non-blocking observations (not breakages)

- O1 (cosmetic): Step 3.1 instructs the executor to also keep the "Read in full" imperative as the
  instruction for truncated/path-only entries. The current substring is `MUST Read each one IN FULL`
  — an executor must preserve that EXACT casing/substring (tests assert it). Instructions say so;
  flagged only as an easy-to-fumble detail, not a task defect.
- O2 (cosmetic): `executor.py:1344` comment still says "repeated --file attachments" post-fix; the
  task scopes it OUT (comment-only, not matched by the guard). Leaving it is acceptable but it is
  now mildly stale prose. Non-blocking.
- O3 (process): `start_commit:` empty in frontmatter is by design (Step 1.3 fills it); not a defect.

None of these would cause execution to FAIL.

---

## VERDICT: PASS

All six operational checks pass. The task's wiring claims match the live source:

1. Removing `_build_file_args` + the `extra_args=file_args` kwarg leaves a valid
   `PrdClaudeProcess.__init__` (base defaults `extra_args` → `[]`; sole caller `executor.py:714`
   passes none). — PASS
2. The Phase-3 `Path(p).is_file()` guard is genuinely load-bearing (unguarded `_read_file` raises a
   bare `FileNotFoundError` the executor does NOT catch) and the inline design reuses real
   primitives. — PASS
3. The `TestSpecFileAttach` inversion (invert two, delete three) is correctly specified against the
   real `:459-515` test class and will pass post-fix. — PASS
4. The acceptance grep returns exactly the two expected hits now (`process.py:199,204`) and 0 after
   Phase 2; no other quoted `"--file"` in `cli/prd/`. — PASS
5. `make verify-sync` never inspects `cli/`; a cli-only change is genuinely clean. — PASS
6. No command hits a blocking precondition (uv present, test dir present, git rev-parse works,
   dead-const grep confirms CONFIRMED-DEAD). — PASS

No concrete breakages found that would cause the task to FAIL on execution. Only three cosmetic,
non-blocking observations (O1-O3).
