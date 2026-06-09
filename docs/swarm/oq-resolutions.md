# MultiModelSwarm — Open Question Resolutions

> 📚 Part of the [swarm documentation](./README.md). This is a maintainer-facing
> design-rationale record; for usage start with the [User Guide](./user-guide.md).

This file records resolutions to the OQ rows tracked in
`.dev/releases/Current/MultiModelSwarm/roadmap.md`. Each entry pins the
chosen branch, the rationale, the implementation surface, and the
tasklist row that landed the resolution. New OQ entries append here in
roadmap order so the file stays diff-friendly.

## OQ-007 — Workers > configured T2Models guard (INV-005)

| Field | Value |
|---|---|
| Roadmap row | `.dev/releases/Current/MultiModelSwarm/roadmap.md` line 108 |
| Question | Workers > configured T2Models guard (INV-005): warn-on-exceed-with-defaults (V1) or STOP (V2)? |
| Resolution branch | **V1 — warn-on-exceed-with-defaults** (project default) |
| Selectable | Yes — `pool_policy="stop"` callers get V2 semantics on demand |
| Resolved at | M1 exit (carried into M2 / Phase 2) |
| Owner | architect |
| Landed in tasklist row | T02.10 |
| Implementation | `src/superclaude/cli/swarm/preflight.py::check_pool_size`, `workers_exceed_pool`, `run_preflight(..., pool_policy=...)` |
| Tests | `tests/swarm/test_inv005_pool_guard.py` (both branches) |

### Resolution

**V1 warn-on-exceed-with-defaults** is the project-default behavior for
the INV-005 worker-count vs model-pool guard. When `workers.count`
exceeds the size of the configured (non-empty) model pool at preflight,
the orchestrator:

1. Logs a `WARNING` on the `superclaude.cli.swarm.preflight` logger
   identifying the original count, the pool size, the clamped value,
   and the `job_id`.
2. Mutates the in-flight `JobSpec` so `workers.count = len(pool)` —
   the pool size becomes the effective worker count for the rest of
   the run (manifest emit, dispatch, reduce).
3. Continues Wave 0 without raising; downstream phases see a coherent
   pool/worker ratio.

The `PreflightSummary.workers_requested` field stamped onto the
manifest reflects the **clamped** value so the artifact records the
count that actually fanned out, not the pre-clamp request. The `clamp`
event is recoverable from logs (canonical phrasing:
`"INV-005 / OQ-007 V1 warn-with-defaults: workers.count=N exceeds
configured pool size=K; clamping workers.count to K for job_id=..."`).

### V2 STOP — selectable

`pool_policy="stop"` (passed to `run_preflight`) opts into V2 semantics:
the overage is reported as a `PreflightFailure` carrying
`RULE_WORKERS_EXCEED_POOL` and `reason="workers-exceed-pool"`, and
preflight raises `PreflightError`. This is the strict branch — useful
for CI gates, integration smoke tests, and any caller that prefers a
hard fail over a silent clamp. The direct-call helper
`check_pool_size(workers, pool, policy="stop")` defaults to V2 so
ad-hoc validation scripts get strict-by-default semantics.

### Rationale

The roadmap row recommends `warn` (line 108: "M1 exit (W2) — recommended:
warn"). Adopting V1 as the project default:

- Matches the spec recommendation.
- Avoids tripping operators on a benign mismatch — clamping to the
  pool is always safe (you cannot dispatch to more models than exist).
- Preserves dispatch determinism: workers fan out 1:1 against the pool
  even when callers ask for more than is available.
- Keeps the strict branch one parameter away for callers that want it.

### Empty-pool interaction

`workers_exceed_pool` returns `False` for an empty pool; INV-007
(`check_empty_pool`) is the authoritative guard for that case and
emits its own structured `env-missing` failure. The two guards never
double-report.

### Adjacent OQ rows

- **OQ-008** (empty-pool failure path / INV-007) — resolved below.
- **OQ-010** (`swarm validate-lenses` failure semantics) — resolution
  lands in tasklist row T02.20.

## OQ-008 — Empty-pool failure contract (INV-007)

| Field | Value |
|---|---|
| Roadmap row | `.dev/releases/Current/MultiModelSwarm/roadmap.md` line 185 (OQ-008) / line 143 (INV-007) |
| Question | Empty-pool failure path: write `failed`/`env-missing` contract OR pre-output-dir abort? |
| Resolution branch | **Hybrid — write `failed`/`env-missing` contract when output dir is creatable; bare abort otherwise** |
| Selectable | No — branch selection is automatic, driven by whether `job.output.dir` can be created |
| Resolved at | M2 (Phase 2 — INV-007 is the resolution mechanism per roadmap line 185) |
| Owner | architect |
| Landed in tasklist row | T02.11 |
| Implementation | `src/superclaude/cli/swarm/preflight.py::emit_env_missing_contract`, `check_empty_pool`, `run_preflight` (wiring) |
| Tests | `tests/swarm/test_inv007_empty_pool.py` (both branches) |

### Resolution

The INV-007 empty-pool guard fires when `job.workers.models` resolves
to an empty pool (or a pool with only empty strings). When detected at
preflight, `run_preflight` calls `emit_env_missing_contract(job,
failures=...)` *before* raising `PreflightError`. The emitter picks
one of two branches based on whether `job.output.dir` can be created:

1. **Output dir creatable** — `Path(job.output.dir).mkdir(parents=True,
   exist_ok=True)` succeeds. The emitter writes a YAML envelope to
   `<job.output.dir>/return-contract.yaml` atomically (write-to-tmp +
   `os.replace`) and returns the absolute path. The envelope carries:

   - `contract_version: "1.0"` — DM-012 alignment.
   - `status: "failed"` — IMM-5 alignment (`M < 2` → failed; here
     `M == 0` because no dispatch occurred).
   - `reason: "env-missing"` — INV-007 / OQ-008 classifier token,
     mirrored from `PreflightFailure.reason` populated by
     `check_empty_pool`. Operators (OPS-002 readiness check, M9) grep
     this token to distinguish env-missing from other `failed` states.
   - `preflight_failures: [...]` — structured `PreflightFailure` list
     so callers see every failing rule in one pass.
   - Standard ResultContract fields (`job_id`, `caller`, `lens`,
     `target`, `workers_requested`, `workers_succeeded=0`,
     `workers_failed=0`, `output_files=[]`, `merged_path=null`,
     `caller_metadata`, `recommended_next_command`, `artifacts`,
     `started`, `finished`, `elapsed_ms`, `lens_source`,
     `amalgamation_mode`) mirroring the job spec / dataclass defaults
     so the contract is grep-compatible with a successful contract
     emitted at M5 reduce.

2. **Output dir NOT creatable** — `job.output.dir` is empty, or
   `mkdir` raises `OSError` / `NotADirectoryError` /
   `PermissionError` (e.g. a parent path is a regular file, or the
   directory is on a read-only filesystem). The emitter returns
   `None`; no file is written. The `PreflightError` still carries
   `RULE_EMPTY_POOL` so callers see the failure mode through the
   exception even though no on-disk artefact exists.

### Rationale

The merged spec recommendation (`merged-requirements.compressed.compressed.md`
L690) explicitly endorses this hybrid:

> Empty-pool failure path: write `failed`/`env-missing` contract OR
> pre-output-dir abort? (INV-007) Recommend write-on-failure when
> output dir is creatable; pre-output-dir abort otherwise.

The hybrid is the right resolution because:

- **Write-on-failure preserves operator diagnostics.** A creatable
  output dir is a sign the caller has set up a sensible workspace; a
  structured `return-contract.yaml` carrying `reason: env-missing`
  gives downstream tooling (OPS-002 readiness check, `done.json`-style
  pollers, CI gates) a single artefact to read, identical in path to
  the M5 success / partial contracts.
- **Bare abort respects path-confinement (NFR-013).** When the output
  dir cannot be created — empty path, hostile filesystem, or a parent
  that is a regular file — fabricating state on disk would violate
  the "we do not invent paths the caller never asked for" principle.
  The `PreflightError` still carries the failure rule so the caller
  has full diagnostic visibility without touching the filesystem.
- **Single-source classifier.** `ENV_MISSING_REASON = "env-missing"`
  is the canonical token, mirrored between the in-memory
  `PreflightFailure.reason` and the on-disk `reason` envelope key.
  Operators and tests grep one string, not two.

### ResultContract field interaction

`ResultContract` (DM-012) does not currently carry a typed `reason`
field — its 19-field surface is pinned by
`tests/swarm/test_result_contract.py::test_result_contract_top_level_key_count_is_19`.
T02.11 emits the `reason` token as an envelope-level YAML key
alongside the 19 ResultContract fields. A future M9 task (OPS-002
readiness work) may promote `reason` to a typed `ResultContract`
field; until then the envelope key preserves the classifier without
altering the contract dataclass surface.

### Wiring in run_preflight

`run_preflight` checks the collected failures for `RULE_EMPTY_POOL`
before raising. When present, it calls
`emit_env_missing_contract(job, failures=failures)` and attaches the
returned path (or `None` for bare abort) to the raised
`PreflightError.env_missing_contract_path`. Non-INV-007 failures
(IMM-4 target-too-small, INV-005 workers-exceed-pool, schema
rejections) never trigger env-missing emission — those have their own
structured-failure surfaces emitted later in the pipeline.

### INV-005 interaction

`check_empty_pool` reports the empty-pool failure on its own;
`workers_exceed_pool` returns `False` for an empty pool so the
INV-005 guard never double-reports. The two guards have disjoint
domains: INV-007 owns "pool size 0", INV-005 owns "workers > pool
size when pool is non-empty".

## OQ-010 — `swarm validate-lenses` failure semantics

| Field | Value |
|---|---|
| Roadmap row | `.dev/releases/Current/MultiModelSwarm/roadmap.md` line 187 (OQ-010) / line 150 (FR-008) |
| Question | `validate-lenses` failure semantics — exit code, blocking vs warning? |
| Resolution branch | **Hybrid — BLOCKING by default (exit 1), selectable WARNING mode via `--warning-mode` (exit 0 with warnings on stderr)** |
| Selectable | Yes — `--warning-mode` flag opts into the non-blocking branch on demand |
| Resolved at | M2 (Phase 2 — landed by T02.20) |
| Owner | devops |
| Landed in tasklist row | T02.20 |
| Implementation | `src/superclaude/cli/swarm/commands.py::validate_lenses_cmd`, `_run_validate_lenses`, `_emit_lens_failures` |
| Tests | `tests/swarm/test_validate_lenses_cmd.py` (both branches + diagnostic format parity) |

### Resolution

`swarm validate-lenses` defaults to **blocking** semantics: when one
or more entries in the bundled `LENSES` registry fail the COMP-023
five-assertion validator (`cli/swarm/lenses/_validate.py::validate_all`),
the command emits a structured per-entry diagnostic block on stderr
and exits with `EXIT_INVALID` (1). The header line is
`validate-lenses: N lens entry/entries failed validation` and each
failing entry adds a grep-friendly line of the form
`- <rule> @ <path>: <message> (lens=<lens_name>)`. The `lens=`
suffix satisfies the FR-008 acceptance criterion "reports first
failure with entry name otherwise" by tagging every failure with the
`LensValidationFailure.lens_name` field.

The `--warning-mode` flag opts into the **warning branch**: the same
diagnostic block is printed on stderr, but the header prefix flips to
`validate-lenses: WARNING:` and the command exits 0. Per-entry lines
are byte-identical to the blocking branch so log consumers can grep
the rule identifier without inspecting exit codes; the test
`test_warning_mode_diagnostic_lines_match_blocking_mode` pins the
parity property.

Exit-code legend:

- `0` — registry passes the validator (every non-custom entry passes
  its five COMP-023 assertions), OR `--warning-mode` is set and
  failures are surfaced as warnings rather than errors.
- `1` — one or more entries failed validation and `--warning-mode`
  is not set (default blocking branch).
- `2` — reserved for future usage errors (no path argument is
  accepted today; the reservation keeps `validate-lenses` mirroring
  `validate_cmd`'s exit-code surface so operators learn one mental
  model for both subcommands).

### Rationale

The roadmap row (R-046 / FR-008) describes the gate as the
authoritative lens-registry validator wired into CI. Defaulting to
blocking matches the spirit of the FR-008 acceptance criterion
"exits 0 when registry passes; reports first failure otherwise" —
"reports" in a CI context means a non-zero exit so the pipeline
stops on a real regression.

The hybrid is the right resolution because:

- **Blocking default matches CI reality.** A registry regression
  (e.g. a contributor removes the §11.5 substring from a lens body)
  is a release-blocker by spec. A non-zero exit is the lingua franca
  every CI runner already understands; warn-only would force every
  pipeline integrator to parse stderr to decide whether to fail.
- **Warning-mode honors OQ-001 / pre-commit hook UX.** Contributors
  iterating on a lens entry locally benefit from a fast advisory loop
  — `--warning-mode` lets a `pre-commit` hook print the diagnostic
  without blocking the commit, while CI still rejects the change at
  PR time. This matches how `prettier --check` vs `prettier --write`
  feels to most contributors: one mode is advisory, the other is
  authoritative.
- **AC-literal compliance.** The T02.20 acceptance criterion says
  "Supports `--warning-mode` flag if OQ-010 resolves to
  warning-mode". Treating warning-mode as opt-in honors that wording
  literally (the flag exists) without flipping the strict default
  most operators expect from a validator.
- **Exit-code parity with `validate`.** Both `validate` and
  `validate-lenses` use the same `EXIT_OK`/`EXIT_INVALID`/`EXIT_USAGE`
  constants exported from `commands.py`. A future task that adds a
  `--registry-path` argument can map "missing file / bad JSON" to
  `EXIT_USAGE` (2) without renumbering the existing branches.

### Diagnostic format

The per-entry format is a single line, two-space indent, in this
shape:

```text
  - <rule> @ <path>: <message> (lens=<lens_name>)
```

Where:

- `<rule>` is one of the stable `_validate.RULE_*` constants
  (`lens.file_ref_unresolved`, `lens.recipe_unregistered`,
  `lens.suspect_files_coupling`, `lens.name_duplicate`,
  `lens.injection_substring_missing`,
  `lens.normalizer_strategy_unmatched`). Tests grep on the rule
  identifier, not the message phrasing, so copy edits don't break
  the suite. The sixth rule (`lens.normalizer_strategy_unmatched`,
  the COMP-023 normalizer-strategy assertion added under
  FR-LENSREG.NS / T02.21) is enforced alongside the prior five; see
  `docs/dev/lens-contribution-policy.md` §1.
- `<path>` is the dotted path to the offending field on the
  `LensEntry` (e.g. `system_prompt_fragment`,
  `output_template_path`). Empty paths render as `<root>` for parity
  with the `validate_cmd` diagnostic surface.
- `<message>` is the human-readable diagnostic produced by the
  validator. Already includes the lens name in the prose; the
  trailing `(lens=<lens_name>)` is the structured token that log
  scrapers grep for.
- `<lens_name>` is `LensValidationFailure.lens_name` — the
  `LensEntry.name` of the failing entry.

### Bundled-registry behavior today

Until T02.23 lands, the bundled `LENSES` carries the T02.14
placeholder entries (every non-custom entry has empty
`output_template_path`). `superclaude swarm validate-lenses` against
the placeholder registry therefore exits 1 by default with seven
`lens.file_ref_unresolved` failures (one per non-custom entry). That
is expected: T02.23 fills in the real entry bodies and T02.17
ratifies "7 of 8 pass" on the populated set. The T02.20 end-to-end
test pins the M2-exit surface using a passing fixture registry and a
permissive file resolver, so the CLI wiring is verified independent
of the placeholder ↔ populated transition.

### Adjacent OQ rows

- **OQ-001** (pre-commit hook for `validate-lenses`) — resolution
  depends on OQ-010 (this row) and the lens-contribution policy
  landed by T02.27. With warning-mode available, OQ-001's natural
  resolution is "install the hook in warning-mode for fast local
  feedback, and let CI run the default blocking mode at PR time".

## OQ-009 — `caller_metadata.suspect` propagation (DM-020)

| Field | Value |
|---|---|
| Roadmap row | `.dev/releases/Current/MultiModelSwarm/roadmap.md` line 186 (OQ-009) / line 160 (DM-020) |
| Question | `caller_metadata.suspect` propagation — lens-only or caller-overridable precedence? |
| Resolution branch | **Caller-overridable** (lens defaults; caller-supplied override wins field-by-field) |
| Selectable | No — the precedence rule is invariant; callers opt in by supplying an override at preflight |
| Resolved at | M2 (Phase 2 — landed by T02.25) |
| Owner | architect |
| Landed in tasklist row | T02.25 |
| Implementation | `src/superclaude/cli/swarm/models.py::CallerMetadata`, `src/superclaude/cli/swarm/preflight.py::resolve_caller_metadata`, `run_preflight(..., caller_metadata_override=...)` |
| Tests | `tests/swarm/test_caller_metadata.py` (field set, both precedence branches, Wave-0 wiring, INV-001 recoverability) |

### Resolution

`CallerMetadata` (DM-020) is **caller-overridable** per the §4.2 /
FR-LENS-004 rule "caller-supplied values override lens defaults".
Resolution happens at Wave 0 preflight via
`preflight.resolve_caller_metadata(source, *, override=None)`:

1. **No override (default)** — the lens entry supplies both fields
   verbatim: `CallerMetadata(suspect=lens.suspect, tier=lens.tier)`.
   This is the path the bundled lenses (`bare-review` carries
   `suspect=True / tier="T2"`; the others carry the conservative
   defaults) exercise out of the box.
2. **Override supplied** — every field on `override` wins field-by-field
   regardless of the lens value. `resolve_caller_metadata` returns a
   fresh `CallerMetadata` instance copied from `override`, so mutation
   of the caller's payload after the call cannot retroactively change
   the resolved value.

The resolved metadata is attached to `PreflightResult.caller_metadata`
so the executor can stamp it onto `ResultContract.caller_metadata` at
Wave 3 reduce (M5 / COMP-009) without re-resolving.

### Source acceptance — `LensEntry` and `ResolvedLensEntry`

`resolve_caller_metadata` accepts either a live `LensEntry` (used at
preflight, where the registry binding is in scope) or a
`ResolvedLensEntry` snapshot (used at reduce time, where the executor
reads `manifest.resolved_lens_entry` rather than re-resolving against
LENSES). Both records expose `suspect` and `tier` with identical
semantics, so the executor calls the same helper at both surfaces
without branching on input type. This keeps INV-001 / INV-016 intact:
the lens-side contribution to `caller_metadata` is recoverable from
`manifest.json` alone via the snapshot.

### Manifest capture

The roadmap DM-016 row pins the `Manifest` field set
(`contract_version`, `job_id`, `resolved_lens_entry`, `preflight`); the
`caller_metadata` resolution does **not** add a new top-level
manifest field. Instead, the lens-side inputs flow through
`ResolvedLensEntry` (DM-011) — its `suspect` and `tier` fields are
exactly the values `resolve_caller_metadata` reads when the executor
re-resolves at reduce time. Caller overrides supplied at Wave 0 are
preserved in-memory on `PreflightResult.caller_metadata` and stamped
onto `ResultContract.caller_metadata` at reduce; persisting the
override across executor restart is future work for M6 resume (an
optional caller-override payload could be added under
`runtime`-adjacent fields without altering the DM-016 surface).

### Rationale

The architect column on the roadmap haiku-architect spec
(`.dev/releases/Current/MultiModelSwarm/roadmap-haiku-architect.md`
line 335) records the resolution: "Implied yes (caller overrides per
§4.2)". The caller-overridable branch is the right resolution because:

- **§4.2 / FR-LENS-004 consistency.** Every other field-level
  expansion (`workers.count`, `target.truncation.line_cap`,
  `output.filename_template`, …) honours "caller wins" already; a
  lens-only carve-out for `caller_metadata` would be a special case
  with no operator-visible upside.
- **No lens-contract violation.** The lens validator (COMP-023) does
  not assert any global invariant on `suspect` / `tier` against the
  caller record; the values are advisory metadata stamped onto the
  contract for downstream consumers (e.g. `sc-reflect` reads
  `caller_metadata.suspect` to decide whether the §FR-020 / NFR-012
  review discipline applies). Letting a caller flip the bit on a
  one-off run does not corrupt the lens definition.
- **Single source-of-truth resolver.** `resolve_caller_metadata` is
  the only code path that produces a `CallerMetadata` instance for the
  contract; mutating it breaks both branches simultaneously, which is
  the property the precedence tests pin.

### Adjacent OQ rows

- **OQ-007** (INV-005 workers-vs-pool) — independent; resolved above.
- **OQ-008** (INV-007 empty-pool failure) — independent; resolved above.
