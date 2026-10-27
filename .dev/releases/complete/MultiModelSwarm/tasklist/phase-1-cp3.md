# Phase 1 — Checkpoint 3 (Mid-Phase)

**Checkpoint ID:** CP3 (mid-phase, after T01.13..T01.17)
**Phase:** 1 — Foundation, Module Shape & Data Models
**Type:** CHECKPOINT (mid-phase) — Tier EXEMPT
**Deliverable:** D-CP1-1
**Timestamp:** 2026-06-01T05:03:58+00:00
**Worktree:** `/config/workspace/IronClaude/.claude/worktrees/BareReview`
**Commit:** `757a3824` (branch `brainstorm/t2-bare-reviewer-adjunct`; swarm artifacts untracked, working-tree state)
**Roadmap binding:** R-011..R-015 (DM-001 JobSpec, DM-002 WorkerSpec, DM-003 TargetSpec, DM-004 TransportSpec, DM-005 PromptSpec)

## Scope

Verify the Phase 1 dataclass-implementation bracket (T01.13..T01.17) is
complete and the first five schema-bearing DM-### records — `JobSpec`,
`WorkerSpec`, `TargetSpec`, `TransportSpec`, `PromptSpec` — are frozen,
type-checked, JSON round-trip lossless, and field-drift-free against
the roadmap DM-### rows before Phase 1 proceeds into the
output/policy/runtime/lens bracket (T01.19..T01.24).

## Acceptance Criteria — Results

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | T01.13..T01.17 done | ✅ PASS | All five dataclasses present in `src/superclaude/cli/swarm/models.py`; 117/117 tests pass across the five `test_jobspec.py`, `test_workerspec.py`, `test_targetspec.py`, `test_transportspec.py`, `test_promptspec.py` modules (see §Task Evidence). Per CP1/CP2 convention, sprint runner uses artifact + test checks rather than per-task `status: done` YAML lane. |
| 2 | `phase-1-cp3.md` checkpoint report exists | ✅ PASS | This file. |
| 3 | JobSpec round-trip green | ✅ PASS | `JobSpec` defined at `src/superclaude/cli/swarm/models.py:69`; `test_jobspec.py` covers field-completeness (all 14 sub-fields enumerated in DM-001), `amalgamation_mode` Literal enforcement (`raw`/`normalize`/`normalize+merge`), and JSON round-trip lossless via `to_dict`/`from_dict`. |
| 4 | WorkerSpec round-trip green | ✅ PASS | `WorkerSpec` at `models.py:137` with nested `RetryPolicy` (DM-002 retry sub-fields `on_5xx`, `on_5xx_backoff_sec`, `on_4xx`, `on_timeout`); `timeout_sec` defaults to 180 (NFR-010); negative `timeout_sec` raises `ValueError`. 21 tests pass. |
| 5 | TargetSpec round-trip green | ✅ PASS | `TargetSpec` at `models.py:236` with nested `Truncation`, `Delimiters`, `InjectionGuard`; `delimiters.open == "<<<TARGET>>>"`, `delimiters.close == "<<<END TARGET>>>"`; `truncation.line_cap=4000`, `byte_floor=50`. 30 tests pass. |
| 6 | TransportSpec round-trip green | ✅ PASS | `TransportSpec` at `models.py:278`; `kind` is `Literal['openai_compat','stub']`; empty `base_url_env` / `api_key_env` raise `ValueError`; invalid `kind` raises. 19 tests pass. |
| 7 | PromptSpec round-trip green | ✅ PASS | `PromptSpec` at `models.py:341` with verbatim-preserving `system`, `user_template`, `variables`; round-trip preserves leading/trailing whitespace, blank-line runs, and the canonical §11.5 sentence; substring enforcement deliberately deferred to T02.03 (schema layer). 22 tests pass. |
| 8 | No field drift vs roadmap DM-### rows | ✅ PASS | Field-by-field comparison against roadmap.md lines 88-92: JobSpec carries all 14 sub-fields (spec_version, job_id, created, caller, lens, custom_prompt_dir?, workers, transport, prompt, target, normalization, output, amalgamation_mode, status_policy, recommended_next_command_template, recommended_next_command_substitutions, runtime); WorkerSpec all 4 retry sub-fields + count/models/timeout_sec/temperature; TargetSpec all 8 dotted sub-fields; TransportSpec exact 3 fields; PromptSpec exact 3 fields. Field-count assertions live in each test module. |

## Task Evidence (T01.13..T01.17)

### T01.13 — `JobSpec` (DM-001) [STRICT]

- `src/superclaude/cli/swarm/models.py::JobSpec` declared with the
  full 14-sub-field set required by R-011: `spec_version`, `job_id`,
  `created`, `caller:CallerInfo`, `lens`, `custom_prompt_dir?`,
  `workers:WorkerSpec`, `transport:TransportSpec`, `prompt:PromptSpec`,
  `target:TargetSpec`, `normalization:NormalizationSpec`,
  `output:OutputSpec`, `amalgamation_mode:Literal['raw','normalize','normalize+merge']`,
  `status_policy:StatusPolicy`, `recommended_next_command_template`,
  `recommended_next_command_substitutions`, `runtime:RuntimeSpec`.
- `amalgamation_mode` Literal locks INV-008 at the dataclass layer.
- Default-factory wiring uses lambdas (`field(default_factory=lambda: WorkerSpec())`)
  to avoid mutable shared state across instances.
- JSON round-trip lossless verified by `tests/swarm/test_jobspec.py`.
- STRICT tier per §4.11 — schema-bearing root record.

### T01.14 — `WorkerSpec` (DM-002)

- `src/superclaude/cli/swarm/models.py::WorkerSpec` at line 137 with
  fields `count:int`, `models:list[str]`, `timeout_sec:int=180`
  (NFR-010 default), `temperature:float`, `retry:RetryPolicy`.
- Nested `RetryPolicy` carries the four required retry sub-fields:
  `on_5xx:bool`, `on_5xx_backoff_sec:int`, `on_4xx:bool`,
  `on_timeout:bool`.
- `__post_init__` rejects negative `timeout_sec` with a `ValueError`
  (acceptance-criterion line 464).
- 21/21 tests pass — covers field-typing, defaults, negative-timeout
  rejection, nested-retry standalone round-trip, populated-instance
  JSON round-trip.

### T01.15 — `TargetSpec` (DM-003)

- `src/superclaude/cli/swarm/models.py::TargetSpec` at line 236 with
  nested `Truncation`, `Delimiters`, `InjectionGuard` substructures.
- Defaults locked: `delimiters.open == "<<<TARGET>>>"`, `delimiters.close
  == "<<<END TARGET>>>"`, `truncation.line_cap == 4000`,
  `truncation.byte_floor == 50`, `injection_guard.enabled == True`.
- 30/30 tests pass — covers every dotted sub-field declared in DM-003,
  default-canonical-marker assertions, JSON round-trip, and the
  fresh-per-instance default-factory invariant for nested records.

### T01.16 — `TransportSpec` (DM-004)

- `src/superclaude/cli/swarm/models.py::TransportSpec` at line 278.
- `kind:Literal['openai_compat','stub']` enforced via `TRANSPORT_KIND_LITERAL`;
  invalid `kind` raises `ValueError`.
- `base_url_env` / `api_key_env` env-var-name validation rejects empty
  strings (acceptance-criterion line 532).
- Defaults: `kind="openai_compat"`, `base_url_env="T2_PROXY_URL"`,
  `api_key_env="T2_PROXY_KEY"`.
- 19/19 tests pass.

### T01.17 — `PromptSpec` (DM-005) [STRICT]

- `src/superclaude/cli/swarm/models.py::PromptSpec` at line 341 carries
  verbatim `system:str`, `user_template:str`, `variables:dict`.
- Whitespace preserved without normalization across `to_dict` /
  `from_dict` and `json.dumps` / `json.loads` round-trips, including
  leading/trailing whitespace, embedded newlines, blank-line runs, and
  the canonical §11.5 required-substring sentence.
- `test_no_substring_enforcement_at_dataclass_layer` confirms the §11.5
  substring rule is deliberately deferred to the schema layer (T02.03)
  per the planning step.
- 22/22 tests pass.
- STRICT tier per §4.11 — carries injection-guard substring downstream.

## Validation Commands (Replayable)

```
uv run pytest tests/swarm/test_jobspec.py tests/swarm/test_workerspec.py tests/swarm/test_targetspec.py tests/swarm/test_transportspec.py tests/swarm/test_promptspec.py -v
uv run pytest tests/swarm/ -q
uv run python -c "from superclaude.cli.swarm.models import JobSpec, WorkerSpec, TargetSpec, TransportSpec, PromptSpec; import json, dataclasses; assert json.loads(json.dumps(dataclasses.asdict(JobSpec()))) == dataclasses.asdict(JobSpec())"
make verify-sync
```

All commands succeed on this commit:
- 117/117 pass on the five CP3 dataclass test modules
- 272/272 pass across the full `tests/swarm/` suite
- `make verify-sync` returns "✅ All components in sync."

## Open Question Owners

| OQ | Title | Owner | Status at CP3 |
|---|---|---|---|
| OQ-006 | Concurrent `--output` dir protection | architect | Unchanged from CP2 — deferred for v1 per roadmap §Open Questions row 251; no blocker logged. |
| OQ-008 | Empty-pool failure contract (INV-007) | architect | Open; resolution scheduled by M2 exit via INV-007. No blocker at CP3. |
| OQ-009 | `caller_metadata.suspect` precedence (lens-only vs. caller-overridable) | architect | Open; blocks DM-020 precedence rule. Resolution required before M1 exit (T01.29). No blocker at CP3. |

Mid-phase requirement ("No blockers logged for OQ owners") remains
satisfied: owners are named, no blocking entries exist. Final
assignment + sign-off lands at T01.29 (end-of-phase, STRICT tier).

## Outstanding / Next

Phase 1 dataclass implementation continues into the policy/runtime/lens
bracket:

1. **T01.19** — `NormalizationSpec` (DM-006) — recipe/template_path/
   schema_version/recipe_args + `on_parse_error.salvage` /
   `retain_raw` defaults (`true`/`true`).
2. **T01.20** — `OutputSpec` (DM-007) — dir/filename_template/lens_name
   with `atomic_write=True` default (IMM-6 alignment).
3. **T01.21** — `StatusPolicy` (DM-008) — IMM-5 defaults
   (`floor=2`, `success_first=True`, `partial_threshold=2`).
4. **T01.22** — `RuntimeSpec` (DM-009) — mode `Literal['inline','detached']`
   with `inline` default; M7 detached-mode opt-in.
5. **T01.23** — `LensEntry` (DM-010) [STRICT] — 13-field record feeding
   Wave 0 preflight and the manifest snapshot.
6. **T01.24** — `ResolvedLensEntry` (DM-011) [STRICT] — INV-001 / INV-016
   immutable snapshot constructed via `ResolvedLensEntry.from_lens`.

CP4 (T01.24a) gates these.

## Sign-Off

**Gate Result:** ✅ PASS — Phase 1 mid-phase (tasks 13-17) cleared.
**Authorized to proceed:** T01.19 → T01.24 (CP4 bracket).
**Recorded by:** automation (T01.18 checkpoint task).
