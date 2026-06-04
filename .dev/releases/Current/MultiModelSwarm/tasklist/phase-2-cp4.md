# Phase 2 — Checkpoint 4 (Mid-Phase: Subcommands + Bundled Lenses Green)

**Checkpoint ID:** CP4 (mid-phase, after T02.19..T02.23)
**Phase:** 2 — Preflight, Schema, Lens Registry & Injection Guard (Wave 0)
**Type:** CHECKPOINT (mid-phase) — Tier EXEMPT
**Deliverable:** D-CP2-1
**Timestamp:** 2026-06-01T08:42:00+00:00
**Worktree:** `/config/workspace/IronClaude/.claude/worktrees/BareReview`
**Commit:** `757a3824` (branch `brainstorm/t2-bare-reviewer-adjunct`; swarm artifacts on working tree, untracked per §SoT discipline)
**Roadmap binding:** R-045..R-055 (FR-007, FR-008, FR-LENSREG.NS, FR-024, COMP-024..COMP-030 merged)

## Scope

Verify the Phase 2 subcommand-and-bundled-lenses bracket (T02.19..T02.23)
is complete and the FR-007 / FR-008 / FR-LENSREG.NS / FR-024 / FR-009
(population) surfaces are locked before the Phase 2 closing bracket
(T02.25..T02.28) and the M2 exit gate (T02.29) proceed.

CP3 ratified the registry **shape** and the validator's five-assertion
**contract** against synthesised fixtures plus the placeholder bodies.
CP4 ratifies the **population**: the seven non-custom `LensEntry`
instances now live in per-lens module files
(`cli/swarm/lenses/{bare_review, refactor_find, edge_case_hunt, spec_completeness, feasibility_probe, troubleshoot_hypothesis, doc_completeness}.py`),
are aggregated into `LENSES` by `lenses/__init__.py`, and the U-008
`validate_all` validator now returns the **empty list** when invoked
against the bundled registry — the "7 of 8 pass" invariant that CP3
intentionally deferred is now demonstrably true on the real registry,
not on synthesised stand-ins.

Alongside the population, CP4 lands the two operator-facing surfaces
that consume the schema and the validator: `swarm validate` (FR-007)
wires the schema validator to a Click subcommand with structured
exit-code semantics, and `swarm validate-lenses` (FR-008) wires
`validate_all` to a Click subcommand with the OQ-010 hybrid resolution
(BLOCKING by default; `--warning-mode` opt-in). FR-LENSREG.NS extends
`LensEntry` with `normalizer_strategy` and binds it to a registered
Recipe at validation time. FR-024 adds the `--auto-inject-guard`
migration helper for legacy `custom-prompt-dir/system.txt` files that
predate the §11.5 substring requirement.

## Acceptance Criteria — Results

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | All of T02.19..T02.23 marked done | ✅ PASS | Deliverables present on disk (see §Task Evidence below); 114/114 tests pass for the bracket-focused suite (`uv run pytest tests/swarm/test_validate_cmd.py tests/swarm/test_validate_lenses_cmd.py tests/swarm/test_normalizer_strategy.py tests/swarm/test_auto_inject_guard.py tests/swarm/test_bundled_lenses.py -q` → 114 passed in 0.25s). |
| 2 | `phase-2-cp4.md` checkpoint report written | ✅ PASS | This file. |
| 3 | `validate` + `validate-lenses` subcommands functional | ✅ PASS | `commands.py::validate_cmd` (line 180) registered with `swarm_group`; `commands.py::validate_lenses_cmd` (line 354) registered with `swarm_group`. `uv run superclaude swarm validate-lenses` exits 0 on bundled set with `validate-lenses: registry OK (8 entries inspected, 7 validated)`. 26/26 dedicated CLI tests pass (13 per subcommand). |
| 4 | 7 non-custom lenses pass validator | ✅ PASS | 7 per-lens module files exist (`cli/swarm/lenses/{bare_review, refactor_find, edge_case_hunt, spec_completeness, feasibility_probe, troubleshoot_hypothesis, doc_completeness}.py`), each exporting a `LENS: LensEntry` constant. `LENSES["custom"]` remains the escape hatch. `validate_all(LENSES)` returns `[]` (empty failure list). `tests/swarm/test_bundled_lenses.py` 49/49 pass — including the per-lens parametrised "passes validator on bundled registry" check. Full swarm suite green (982/982, `uv run pytest tests/swarm/ -q`). `make verify-sync` green. |

## Task Evidence (T02.19..T02.23)

### T02.19 — FR-007 `swarm validate` subcommand
- **Deliverable:** `src/superclaude/cli/swarm/commands.py::validate_cmd` (line 180) — registered with the `swarm_group` Click group via the `@swarm_group.command("validate")` decorator.
- **Surface:**
  - Positional argument `jobspec_path: Path` — Click `Path(exists=True, dir_okay=False, readable=True, path_type=Path)` so the type system rejects missing-file inputs before the handler runs.
  - `--strict` flag (future-proofing per the acceptance criterion) — currently a no-op pass-through; reserved for tightening optional-field policy in a future phase without breaking the CLI surface.
- **Exit semantics:**
  - Exits **0** on a schema-valid spec (handler prints `validate: spec OK` to stdout).
  - Exits **`EXIT_INVALID` (1)** when `schema.validate_or_raise` raises `SchemaValidationError`, emitting one grep-friendly diagnostic line per failure (`  - <rule> @ <path>: <message>`) on stderr.
  - Exits **`EXIT_USAGE` (2)** when the spec file is not valid JSON/YAML — handled by a dedicated `except` branch surfacing the parse error rather than letting the underlying exception escape.
- **Schema binding:** the subcommand consumes the public `schema.validate_or_raise(spec_dict) -> JobSpec` entry point landed by T02.01 + T02.03. No private symbols are imported; the subcommand and the validator are decoupled at the public surface.
- **§11.5 propagation:** because `validate_or_raise` runs the cross-field §11.5 substring rule on `prompt.system`, the subcommand inherits the §11.5 enforcement transitively — a spec missing the canonical sentence on `prompt.system` is rejected pre-dispatch by `superclaude swarm validate`, mirroring the in-process preflight behaviour.
- **Tests:** `tests/swarm/test_validate_cmd.py` 13/13 pass — registration with `swarm_group`, exit-0 on good fixture, exit-non-zero on invalid-spec fixture, structured diagnostic on stderr, `--strict` flag accepted (no-op for now), missing-file rejected by Click before handler runs, malformed-JSON / malformed-YAML rejected with `EXIT_USAGE`, §11.5-missing fixture rejected with the substring rule named in the diagnostic.

### T02.20 — FR-008 `swarm validate-lenses` subcommand
- **Deliverable:** `src/superclaude/cli/swarm/commands.py::validate_lenses_cmd` (line 354) + private `_run_validate_lenses` and `_emit_lens_failures` helpers.
- **Surface:**
  - `--warning-mode` Click flag (OQ-010 resolution surface) — default `False`.
  - No positional arguments — the subcommand always operates on the bundled `LENSES` registry imported from `cli/swarm/lenses`.
- **Exit semantics (OQ-010 hybrid resolution):**
  - **BLOCKING (default):** when `validate_all(LENSES)` returns a non-empty failure list, emit the structured diagnostic block on stderr (header `validate-lenses: N lens entry/entries failed validation`, per-entry lines `  - <rule> @ <path>: <message> (lens=<lens_name>)`) and exit `EXIT_INVALID` (1).
  - **WARNING (`--warning-mode`):** emit the same diagnostic block on stderr, flip the header prefix to `validate-lenses: WARNING:`, and exit **0**.
  - **OK (all-pass):** emit `validate-lenses: registry OK (8 entries inspected, 7 validated)` on stdout and exit 0 in both modes.
- **OQ-010 resolution recorded:** `docs/swarm/oq-resolutions.md` documents the hybrid branch, the `--warning-mode` flag, the diagnostic format, and the FR-008 acceptance-criterion mapping (`lens=` suffix satisfies the "first failure with entry name otherwise" sub-criterion).
- **Validator binding:** the subcommand consumes the public `_validate.validate_all(registry, *, recipe_checker=…, file_resolver=…, required_substring=…) -> list[LensValidationFailure]` entry point landed by T02.16; defaults flow through, so `validate-lenses` uses the canonical recipe checker, the default file resolver, and the canonical §11.5 substring.
- **Tests:** `tests/swarm/test_validate_lenses_cmd.py` 13/13 pass — registration with `swarm_group`, exit-0 on bundled-clean fixture, exit-1 on synthesised-failing-registry fixture (BLOCKING branch), exit-0 on the same failing fixture with `--warning-mode` (WARNING branch), diagnostic-format parity between BLOCKING and WARNING modes, `lens=` suffix present on every per-entry line, multiple-failing-entries each emit one line preserving registry iteration order, custom-entry skip mirrored from `validate_all`, `--help` text mentions `--warning-mode`, stdout/stderr separation preserved across both branches, `validate_all` invoked exactly once per command run.

### T02.21 — FR-LENSREG.NS `normalizer_strategy` field
- **Deliverable:** `src/superclaude/cli/swarm/models.py::LensEntry` extended with `normalizer_strategy: str = ""` field (line 713). `cli/swarm/lenses/_validate.py` extended with the normalizer-binding assertion in the recipe-registered branch (lines 650, 652, 702).
- **Field shape:** plain `str` per the spec — the strategy is an identifier that resolves to a registered Recipe's expected output shape; `""` is the explicit "unset" sentinel that fails the validator assertion.
- **Validator extension:** when `entry.recipe_name` is non-empty and resolves to a Recipe, the assertion additionally requires `entry.normalizer_strategy` to be non-empty and to match the Recipe's declared output-shape identifier. The legacy "recipe registered" diagnostic stays in place; a new rule constant — surfaced through the same `_check_recipe_registered` branch — fires when the strategy is missing or unmatched.
- **`custom` escape hatch preserved:** the per-entry skip in `validate_lens` (when `entry.name == CUSTOM_LENS_NAME`) bypasses the normalizer assertion exactly as it bypasses the other four; the strategy field can be left blank on `LENSES["custom"]` without tripping the registry-level validator.
- **Tests:** `tests/swarm/test_normalizer_strategy.py` 22/22 pass — field defined on `LensEntry`, default value is the empty sentinel, every bundled non-custom lens declares a non-empty strategy, `custom` lens may declare an empty strategy without tripping the validator, missing-strategy fails validation with a strategy-specific rule identifier, mismatched-strategy (declared but no matching Recipe shape) fails validation, validator skips the strategy assertion when the recipe-registered assertion has already failed (per fail-fast ordering), Recipe-shape resolution is honoured via a stub recipe checker, validator override for `recipe_checker` is honoured, parametrised round-trip from `LENSES["<name>"]` → `_validate.validate_lens` returns no failure for all seven non-custom entries.

### T02.22 — FR-024 `--auto-inject-guard` flag
- **Deliverable:** `src/superclaude/cli/swarm/preflight.py::auto_inject_guard` (line 511) helper + corresponding Click flag wired through the preflight entry surface.
- **Behaviour:**
  - **Flag set (`--auto-inject-guard`):** when reading a `--custom-prompt-dir`'s `system.txt`, prepend `CANONICAL_INJECTION_GUARD_SENTENCE` (the canonical §11.5 sentence) to the file's contents in memory before passing them downstream. The on-disk file is **not** mutated — the helper returns a transformed string.
  - **Flag absent (default):** no prepend; the §11.5 substring rule continues to be enforced by `enforce_injection_guard` on the unmodified contents, so a legacy `system.txt` missing the substring is rejected with the same `RULE_INJECTION_SUBSTRING` failure the lens path emits.
  - **Idempotency:** when the file already contains the canonical sentence (whether or not at the prepend position), the helper returns the input unchanged — this prevents the flag from doubling the sentence on a `system.txt` that already complies.
- **No silent bypass:** the flag is **additive** — it neutralises a legacy missing-substring failure by re-establishing compliance in memory, but it does **not** disable the substring rule. A `system.txt` that contains an attempted bypass (e.g., a trailing instruction crafted to override the prepended sentence) still flows through `enforce_injection_guard` and gets neutralised by the §11.5 delimiters layer landed at CP2.
- **Migration path documented:** the helper's docstring + `docs/dev/lens-contribution-policy.md` (landing at T02.27, with the FR-024 hook already drafted in the dev doc area) record the canonical migration steps for legacy users.
- **Tests:** `tests/swarm/test_auto_inject_guard.py` 17/17 pass — flag absent + substring absent rejected, flag absent + substring present accepted, flag set + substring absent now accepted (prepended), flag set + substring already present idempotent (no doubling), prepend position is at the start of `system.txt`, flag does not mutate the on-disk file, flag does not affect the lens path (lens `system_prompt_fragment` must still carry the substring at contribution time), bypass-by-trailing-instruction still neutralised by the delimiter layer, helper returns string unchanged when input is empty, parametrised over both LF/CRLF line endings.

### T02.23 — Bundle 7 non-custom lens entry files (COMP-024..COMP-030 merged)
- **Deliverable:** seven per-lens module files under `src/superclaude/cli/swarm/lenses/`:
  - `bare_review.py` — `LENS: LensEntry(name="bare-review", recipe_name="bare-review-v1", normalizer_strategy="bare-review-v1", default_workers=3, suspect=True, tier="T2", …)`.
  - `refactor_find.py` — `LENS: LensEntry(name="refactor-find", …)`.
  - `edge_case_hunt.py` — `LENS: LensEntry(name="edge-case-hunt", default_workers=4, …)`.
  - `spec_completeness.py` — `LENS: LensEntry(name="spec-completeness", …)`.
  - `feasibility_probe.py` — `LENS: LensEntry(name="feasibility-probe", …)`.
  - `troubleshoot_hypothesis.py` — `LENS: LensEntry(name="troubleshoot-hypothesis", default_workers=4, …)`.
  - `doc_completeness.py` — `LENS: LensEntry(name="doc-completeness", …)`.
- **Aggregation:** `cli/swarm/lenses/__init__.py::LENSES` (line 105) now imports each module's `LENS` constant and binds the seven entries (plus the `custom` escape-hatch placeholder) into the registry — the placeholder bodies CP3 documented are gone, replaced by fully-populated `LensEntry` instances.
- **§11.5 binding:** every non-custom entry's `system_prompt_fragment` carries `CANONICAL_INJECTION_GUARD_SENTENCE`; the assertion-5 substring check now succeeds against the live registry, not against synthesised fixtures.
- **Suspect/Tier discipline:**
  - `bare_review.LENS.suspect = True` and `bare_review.LENS.tier = "T2"` — the only suspect entry at this checkpoint, mirroring the Phase-1 bare-reviewer skill it backs.
  - All six other non-custom entries declare `suspect=False`.
  - Every suspect entry's `recommended_next_command_template` contains the literal `{suspect_files}` placeholder, satisfying the assertion-3 suspect-coupling rule.
- **Worker defaults:** `bare_review.default_workers = 3`, `edge_case_hunt.default_workers = 4`, `troubleshoot_hypothesis.default_workers = 4`; the remaining entries use the COMP-024..COMP-030 defaults documented in the roadmap rows.
- **Normalizer strategies:** each non-custom entry declares a non-empty `normalizer_strategy` (e.g., `bare_review.normalizer_strategy = "bare-review-v1"`); every declared strategy resolves through the recipe checker against `cli/swarm/recipes/__init__.py::RECIPES`.
- **`validate_all` clean run:** `_validate.validate_all(LENSES)` returns `[]` on the bundled registry — the "7 of 8 pass U-008 on the bundled set with populated bodies" invariant CP3 deferred is now demonstrably true.
- **Tests:** `tests/swarm/test_bundled_lenses.py` 49/49 pass — registry round-trip per entry (×7), suspect-true exactly-one (`bare-review`), worker defaults pin (`bare-review=3`, `edge-case-hunt=4`, `troubleshoot-hypothesis=4`), normalizer-strategy non-empty per entry (×7), normalizer-strategy resolves through recipe checker per entry (×7), §11.5 substring present in `system_prompt_fragment` per entry (×7), `recommended_next_command_template` contains `{suspect_files}` iff `suspect=True` (×8 with custom), `validate_all(LENSES)` returns empty list, `validate_all(LENSES)` after removing one substring returns one failure naming the affected lens (mutation test), every lens module's `LENS` constant is a `LensEntry` (×7), canonical-order matches `LENS_NAMES`.

## Validation Block — Quantitative

| Check (per tasklist §T02.24 Validation) | Spec value | Observed | Status |
|------------------------------------------|------------|----------|--------|
| `grep -c "status: done" execution-log.yaml` ≥ 48 | ≥ 48 | n/a — sprint runner uses `execution-log.jsonl` + artifact-and-test verification, not per-task YAML status lane (convention established in `phase-1-cp5.md:55` and inherited by `phase-2-cp1.md:85` / `phase-2-cp3.md:113`). **Substitute:** 114/114 tests pass on the bracket-focused suite (T02.19..T02.23) + 982/982 tests pass across the full swarm suite + every T02.19..T02.23 deliverable present at the file paths and line numbers cited above + `superclaude swarm validate-lenses` exits 0 on the bundled set + `make verify-sync` green. | ✅ PASS (semantically) |
| `phase-2-cp4.md` checkpoint file exists | required | This file | ✅ PASS |
| `validate` + `validate-lenses` subcommands functional | required | `commands.py:180` `validate_cmd` + `commands.py:354` `validate_lenses_cmd` registered with `swarm_group`; 26/26 dedicated CLI tests pass; `superclaude swarm validate-lenses` returns `validate-lenses: registry OK (8 entries inspected, 7 validated)` and exits 0 | ✅ PASS |
| 7 non-custom lenses pass validator | required | 7 per-lens module files present; `LENSES` aggregates seven populated `LensEntry` instances + `custom`; `_validate.validate_all(LENSES)` returns `[]`; 49/49 dedicated bundled-lens tests pass | ✅ PASS |

## Validation Commands (Replayable)

```
uv run pytest tests/swarm/test_validate_cmd.py \
              tests/swarm/test_validate_lenses_cmd.py \
              tests/swarm/test_normalizer_strategy.py \
              tests/swarm/test_auto_inject_guard.py \
              tests/swarm/test_bundled_lenses.py -v
uv run pytest tests/swarm/ -q
uv run superclaude swarm validate-lenses
make verify-sync
grep -nE "^def (validate_cmd|validate_lenses_cmd|auto_inject_guard)\b" \
     src/superclaude/cli/swarm/commands.py \
     src/superclaude/cli/swarm/preflight.py
grep -nE "normalizer_strategy" src/superclaude/cli/swarm/models.py
python -c "from superclaude.cli.swarm.lenses import LENSES; \
           from superclaude.cli.swarm.lenses._validate import validate_all; \
           failures = validate_all(LENSES); \
           assert failures == [], failures; \
           print('validate_all(LENSES) returns', failures)"
```

All commands above succeed on this commit.

## §11.5 Enforcement Status (CP4 Scope)

| Prompt-input path | Enforcement site | Status at CP4 |
|---|---|---|
| Lens path | `schema.py::_injection_substring_failures` (cross-field rule on `prompt.system`) + `_validate.py::_check_injection_substring` (assertion 5 on `LensEntry.system_prompt_fragment` at **lens-contribution time**) | ✅ enforced at both call sites; now provable against the **live bundled registry** because all seven non-custom `system_prompt_fragment` values carry the canonical sentence |
| JSON-Schema (direct spec) path | `schema.py::validate()` cross-field rule + `commands.py::validate_cmd` operator surface (T02.19) | ✅ enforced (CP1) + parametrised cross-path parity test passing (CP2 / T02.07) + operator-facing CLI rejects §11.5-missing specs (CP4 / T02.19) |
| Custom-prompt-dir path | `preflight.py::read_custom_prompt_dir` → `enforce_injection_guard` (preflight.py:1065) + `auto_inject_guard` (preflight.py:511) migration helper | ✅ enforced (CP1) + INV-003 parity test passing (CP2 / T02.08) + INV-014 isomorphism test passing (CP2 / T02.09) + FR-024 migration path landed (CP4 / T02.22) without silent-bypass risk |

**New at CP4:**
1. The operator-facing `swarm validate` subcommand now inherits the §11.5 substring rule transitively — a legacy job spec uploaded to the CLI is rejected pre-dispatch with the substring rule named in the diagnostic, mirroring the in-process preflight behaviour.
2. The `--auto-inject-guard` flag closes the FR-024 migration gap for legacy `custom-prompt-dir/system.txt` files without disabling the substring rule. The flag is additive (re-establishes compliance) rather than subtractive (bypassing enforcement) — the delimiter layer and the substring rule both remain active.

## Open Question Status

| OQ | Title | Owner | Status at Phase-2 CP4 |
|---|---|---|---|
| OQ-007 | Worker-count vs model-pool guard (warn-with-defaults vs STOP) | architect | ✅ Resolved at CP2 — recorded in `docs/swarm/oq-resolutions.md`; no change at CP4. |
| OQ-008 | Empty-pool failure contract (INV-007) | architect | ✅ Resolved at CP2 — recorded in `docs/swarm/oq-resolutions.md`; no change at CP4. |
| OQ-010 | `validate-lenses` failure semantics (exit code + blocking/warning policy) | architect | ✅ Resolved at CP4 — hybrid BLOCKING-by-default with `--warning-mode` opt-in; recorded in `docs/swarm/oq-resolutions.md` (§OQ-010 entry); implementation landed in `commands.py::validate_lenses_cmd` / `_run_validate_lenses` / `_emit_lens_failures`; `tests/swarm/test_validate_lenses_cmd.py` exercises both branches with diagnostic-format parity. |

All three Phase-2 OQs are now resolved with implementation + doc + tests in place. Final OQ sign-off for the phase lands at T02.29 (M2 exit gate, STRICT tier).

## Bracket Dependency State

| Task | Bracket | Deliverable On Disk | Tests | Status |
|---|---|---|---|---|
| T02.13..T02.17 | CP3 bracket (registry shape + validator contract) | (see `phase-2-cp3.md` §Task Evidence) | 83/83 | ✅ done (CP3 ratified) |
| T02.18 | CP3 checkpoint report | `phase-2-cp3.md` | n/a | ✅ done |
| T02.19 | FR-007 `swarm validate` subcommand | `commands.py::validate_cmd` (line 180) | `test_validate_cmd.py` 13/13 | ✅ done |
| T02.20 | FR-008 `swarm validate-lenses` subcommand | `commands.py::validate_lenses_cmd` (line 354) + `_run_validate_lenses` + `_emit_lens_failures` | `test_validate_lenses_cmd.py` 13/13 | ✅ done |
| T02.21 | FR-LENSREG.NS `normalizer_strategy` | `models.py::LensEntry.normalizer_strategy` (line 713) + `_validate.py` recipe-binding extension | `test_normalizer_strategy.py` 22/22 | ✅ done |
| T02.22 | FR-024 `--auto-inject-guard` | `preflight.py::auto_inject_guard` (line 511) + Click flag | `test_auto_inject_guard.py` 17/17 | ✅ done |
| T02.23 | COMP-024..COMP-030 bundled lens files | `cli/swarm/lenses/{bare_review, refactor_find, edge_case_hunt, spec_completeness, feasibility_probe, troubleshoot_hypothesis, doc_completeness}.py` + `lenses/__init__.py::LENSES` populated | `test_bundled_lenses.py` 49/49 | ✅ done |
| T02.24 | This CP4 checkpoint report | `phase-2-cp4.md` (this file) | n/a | ✅ done |

**Note on CP2 report gap:** The `phase-2-cp2.md` summary file remains
absent on disk (carried forward from CP3's §Bracket Dependency State
note). The CP2 bracket (T02.07..T02.11) is functionally complete and
green; the missing report file should be retrofitted by a separate
housekeeping turn before the M2 exit gate (T02.29) so the audit trail
is complete. This does **not** block CP4.

## Outstanding / Next

1. **T02.25** — Wire `models.py::CallerMetadata` (dataclass) + the
   preflight resolution logic that honours OQ-009's precedence rule
   (lens-only vs caller-overridable for `suspect:bool`, `tier:str`).
   Manifest must capture the resolved CallerMetadata so downstream
   stages can audit which side wins on a per-job basis.
2. **T02.26** — Add the NFR-003 prompt-injection neutralisation test
   covering all three prompt-input paths against a target containing
   the literal `<<<END TARGET>>>` end-marker. The test mutates the
   delimiter / escape logic to confirm the parity test fails when the
   neutralisation is removed.
3. **T02.27** — Document `docs/dev/lens-contribution-policy.md`
   (NFR-012). Five review criteria: real caller, §11.5 substring,
   normalizer-output-shape alignment, real downstream command, extra
   scrutiny for `suspect:true`. Records OQ-001 (pre-commit hook
   decision) and lists owners.
4. **T02.28** — Add the AC-013 no-Claude-Code-isms grep audit CI gate
   (`tests/swarm/test_no_claude_isms.py`) — zero `Task` / `WebFetch`
   etc. tokens across job-spec / contract / CLI / monitoring surfaces.
5. **T02.29** — M2 exit gate. End-of-phase checkpoint with sign-off,
   STRICT tier. Final OQ-007 / OQ-008 / OQ-010 ratification + full
   §11.5 enforcement matrix across all three paths + IMM-4 / INV-005 /
   INV-007 green + `make verify-sync` clean.

CP5 (T02.29) gates the close-out bracket plus the M2 exit.

## Sign-Off

**Gate Result:** ✅ PASS — Phase 2 subcommands-and-bundled-lenses gate cleared.
**Authorized to proceed:** T02.25 → T02.28 (CP5 bracket / M2 exit prep).
**Outstanding follow-up (non-blocking):** retrofit `phase-2-cp2.md` from the T02.07..T02.11 bracket evidence (already captured in `phase-2-cp3.md` §Bracket Dependency State).
**Recorded by:** automation (T02.24 checkpoint task).
