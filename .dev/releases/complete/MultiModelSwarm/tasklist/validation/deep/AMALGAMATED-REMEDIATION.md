---
title: MultiModelSwarm — Amalgamated Remediation (deep reflect, phases 1–9)
generated: 2026-06-04
source_reports: validation/deep/{1,2,3,5,6,7,8,9}/REPORT.md
execution_cwd: /config/workspace/IronClaude/.claude/worktrees/SwarmPost   # feat/multimodel-swarm
status: draft — to be validated
validity_note: >
  Phase 8 report is INVALID (ran from main worktree where swarm code is absent;
  its findings are false negatives). Phase 6 is clean. Phases 1,2,3,5,7,9 valid.
line_number_caveat: >
  file:line citations are as-of the reflect run (2026-06-04) against the SwarmPost
  worktree; re-confirm at fix time before editing.
---

# Amalgamated Remediation — MultiModelSwarm

Consolidated, de-duplicated fix set from the 8 per-phase deep (`/sc:reflect --mode post/pre --depth deep`)
reports. All fixes are to be applied in the **SwarmPost worktree**
(`/config/workspace/IronClaude/.claude/worktrees/SwarmPost`, branch `feat/multimodel-swarm`),
where the swarm code lives. Paths below are worktree-relative unless absolute.

## 0. Validity triage (read first)

| Phase | Report status | Grounded against real code? | Verdict | Action |
|---|---|---|---|---|
| 1 (M1) | failed | ✅ cites SwarmPost src + runtime probes | VALID | fix F-P1-* |
| 2 (M2) | failed | ✅ cites SwarmPost src + runtime probe | VALID | fix F-P2-* |
| 3 (M3) | failed | ✅ 18 src citations + targeted suite run | VALID | fix F-P3-* |
| 5 (M5) | partial | ✅ 196/196 tests, full re-read | VALID (checkpoints only) | RW-6 |
| 6 (M6) | success | ✅ 91 tests, real citations | VALID — **no fixes** | none |
| 7 (M7) | partial | ✅ 211 tests, real citations | VALID | F-P7-1 (+ carry-forwards) |
| 8 (M8) | ~~INVALID~~ → **re-audited** | ✅ now grounded in SwarmPost (`8-rerun/REPORT.md`) | **partial ~85%** | F-P8-* |
| 9 (M9) | success (pre) | ✅ plan-only, greps real code | VALID — plan edits | F-P9-* |

**Phase 8 RESOLVED (2026-06-04):** the original `8/REPORT.md` ran from `main` (code absent) and was a false
negative — it claimed `SKILL.md=221 lines`, `tests/swarm/ does not exist`, `~25% complete`. The corrected
re-audit (`validation/deep/8-rerun/REPORT.md`, run from SwarmPost) shows **Phase 8 ~85% complete**: SKILL.md
migrated (59 lines), legacy scripts retired, IMM suite 79-pass, A/B parity green, CP1/CP2 present. Real M8
gaps captured as **F-P8-*** below; the original `8/REPORT.md` is superseded.

---

## 1. Cross-cutting / repo-wide fixes (unblock multiple phase gates)

These root causes each surface in ≥2 phase reports. Fix once.

### RW-1 — `make verify-sync` fails (sc-bare-review mirror drift)
- **Hits:** P1 F2, P2 R4 (both HIGH; block M1 & M2 exit gates T01.05/T01.29/T02.29).
- **Cause:** legacy `t2_*.sh/.py` deleted from `src/superclaude/skills/sc-bare-review/scripts/` (intended T08.07 migration), but the `.claude/` mirror is out of sync → `verify-sync` reports `Only in src/...: scripts`.
- **Fix:** `make sync-dev && make verify-sync` (in SwarmPost). Do **not** stage `.claude/` mirrors.
- **Verifier:** `make verify-sync` exits 0.

### RW-2 — `test_concurrency_python_only.py` fails (INV-002 vs M7 tmux subprocess)
- **Hits:** P3 R2 (regression, 2 failures), P2 (out-of-scope note), P7 D-3 (OQ-7.1 carry-forward).
- **Cause:** `src/superclaude/cli/swarm/tmux.py:64-68,128-138,198-201` imports/calls `subprocess`/`shlex`; the INV-002 Python-only scanner scans the whole swarm package and flags M7 tmux lifecycle code.
- **Fix:** narrow `tests/swarm/test_concurrency_python_only.py` (lines ~221-258) to the M3 dispatch/transport surface, explicitly allow-listing `tmux.py` lifecycle (the documented OQ-7.1 exemption). Keep the guard strict on `dispatch.py`/transports.
- **Verifier:** `uv run pytest tests/swarm/test_concurrency_python_only.py -q` green.

### RW-3 — `test_uv_enforcement.py` fails (`python -m` in commands.py) — OQ-7.2
- **Hits:** P1 F1 (regression, AC-001), P2 (out-of-scope), P7 D-3 (OQ-7.2).
- **Cause:** detached-launch doc comment at `src/superclaude/cli/swarm/commands.py:782-784` spells the forbidden `python -m`; argv built at `commands.py:879-886` uses `sys.executable, -m, superclaude.cli.main`.
- **Fix (decision):** (a) reword the comment and switch detached re-entry to a UV-safe launcher (`uv run superclaude swarm run ...`); **or** (b) document an explicit AC-001 exception for detached re-entry and update the guard test to allow it. Pick (a) unless detached mode genuinely needs raw `sys.executable`.
- **Verifier:** `uv run pytest tests/swarm/test_uv_enforcement.py -v` green.

### RW-4 — `detect-secrets` flags test fixtures + release-notes (blocks per-phase commits)
- **Hits:** confirmed directly during commit attempt; P8 GAP-001 (inferred).
- **Cause:** "Secret Keyword" hits in `tests/swarm/test_crash_recovery_e2e.py:127`, `test_openai_compat.py:53`, `test_validate_cmd.py:86`, `test_injection_guard_all_paths.py:108`, `test_swarm_run_inputs.py:115` (+1 more); plus `docs/swarm/release-notes-v1.md` `sk-redacted`. Almost certainly false positives (fake fixture keys).
- **Fix:** add `# pragma: allowlist secret` to each flagged line (or `<!-- ... -->` in md), **or** refresh `.secrets.baseline` via `detect-secrets scan --baseline .secrets.baseline` after auditing.
- **Verifier:** `pre-commit run detect-secrets --all-files` (or the commit) passes.

### RW-5 — `markdownlint` fails (28×MD024, 1×MD040, possible MD013)
- **Hits:** confirmed directly during commit attempt; P8 GAP-002 (inferred), P7 notes transport-limits.md clean.
- **Cause:** duplicate headings (MD024) in `docs/dev/lens-contribution-policy.md`, `docs/swarm/oq-resolutions.md`, `docs/swarm/runbook.md`; missing fence language (MD040) at `docs/swarm/oq-resolutions.md:280`; possible MD013 long lines in `docs/dev/migration-skill.md`, `docs/swarm/release-notes-v1.md`.
- **Fix:** dedup/disambiguate repeated headings; add a language to the bare ``` fence; for MD013 either hard-wrap or add a project `.markdownlint.*` disabling MD013 (consistent with spec-doc style).
- **Verifier:** `pre-commit run markdownlint --all-files` (or the commit) passes.

### RW-6 — Missing / stale per-phase checkpoint reports
- **Hits:** P1 F4 (CP5 stale — generated in BareReview worktree), P2 R3 (phase-2-cp5.md missing), P5 D1/D2/D3 (phase-5-cp1/cp2/cp3 missing).
- **Cause:** checkpoints were authored in a prior worktree or skipped; admin artifacts, but P1/P2 list CP5 as an exit-gate requirement.
- **Fix:** after the functional fixes land + gates pass, regenerate the missing/stale checkpoints **from SwarmPost** with current command outputs embedded: `phase-1-cp5.md` (regen), `phase-2-cp5.md`, `phase-5-cp1.md`, `phase-5-cp2.md`, `phase-5-cp3.md`.
- **Verifier:** files exist; metadata (`pwd`, `git rev-parse HEAD`) matches SwarmPost; embedded test/verify-sync output is green.

---

## 2. Phase-specific functional fixes

### Phase 1 (M1) — VALID
- **F-P1-1 (= RW-3)** UV enforcement — see RW-3.
- **F-P1-2 (= RW-1)** verify-sync — see RW-1.
- **F-P1-3 — DM dataclasses are NOT frozen** · **regression, HIGH** · tasks T01.10/T01.13–T01.29 / DM-001..020.
  - Evidence: `src/superclaude/cli/swarm/models.py:87-88` uses plain `@dataclass` for `JobSpec`; runtime probe reports `__dataclass_params__.frozen == False` for all 20 DM classes. Phase-1 goal + T01.29 require "all 20 data models frozen + round-trip serializable"; CP5 falsely claims frozen.
  - **Fix (decision):** either add `frozen=True` to all 20 DM dataclasses (and fix any mutation-dependent helpers/tests) **or** amend the tasklist/roadmap/CP5 to drop the frozen requirement. Note `SwarmConfig` is already frozen; the 20 DM records are not.
  - **Verifier:** `uv run python -c "from superclaude.cli.swarm import models; ...; print([getattr(models,n).__dataclass_params__.frozen for n in NAMES])"` all `True`; model round-trip lanes green.
- **F-P1-4 (= RW-6)** regenerate CP5 from SwarmPost — see RW-6.
- *F5 (LensEntry.normalizer_strategy 14th field) = authorized early adoption — document in CP5, no code change. F6 (CI uses bare `pytest` not `uv run`) = LOW drift, optional.*

### Phase 2 (M2) — VALID
- **F-P2-1 — `custom_prompt_dir` not wired into production preflight/run** · **regression, HIGH** · T02.05/T02.07/T02.29.
  - Evidence: `commands.py:1132-1136` drops the auto-inject/custom-prompt wiring; `preflight.py:1670-1683` guards only `job.prompt.system`, never reads `job.custom_prompt_dir` / calls `read_custom_prompt_dir`. Runtime probe: a spec with `lens=custom`, `custom_prompt_dir=/missing` returns `preflight_ok` instead of failing.
  - **Fix:** in `run_preflight`, when `lens == "custom"` and `custom_prompt_dir` set, call `read_custom_prompt_dir(..., required_substring=..., auto_inject_guard=...)`, populate `job.prompt.{system,user_template}` + vars/meta, and raise structured `PreflightError` on missing files or missing §11.5 substring.
  - **Verifier:** custom lens + missing dir → failed contract; add a regression test.
- **F-P2-2 — resolved `CallerMetadata` not captured in Manifest** · **regression, MEDIUM** · T02.25.
  - Evidence: `preflight.py:252-266` has `PreflightResult.caller_metadata`, but `models.py:1335-1405` `Manifest` has only `contract_version/job_id/resolved_lens_entry/preflight`. A manifest-only rehydrate can't audit a caller override.
  - **Fix:** add `Manifest.caller_metadata: CallerMetadata` (versioned), stamp resolved value in `run_preflight` before writing `manifest.json`; add a manifest JSON round-trip test for override persistence.
  - **Verifier:** round-trip test asserts caller override persists.
- **F-P2-3 (= RW-6)** phase-2-cp5.md — see RW-6. **F-P2-4 (= RW-1)** verify-sync — see RW-1.

### Phase 3 (M3) — VALID
- **F-P3-1 — `swarm run --transport stub` dispatches ZERO workers (silent no-op)** · **regression, CRITICAL** · T03.01/T03.08/T03.10/T03.22.
  - Evidence: `commands.py:1029-1039` exposes `--transport stub`, but `commands.py:1264-1266` always calls `dispatch_wave1(preflight_result, transport=None, logger=logger)`; `dispatch.py:386-392` returns `[]` when `transport is None`. Smoke run prints `workers=3, results=0` and writes only `manifest.json`.
  - **Fix:** construct the resolved `Transport` from `preflight_result.manifest.preflight.transport_kind` / resolved `JobSpec.transport.kind` before `dispatch_wave1`; pass `StubTransport` for `stub`, `OpenAICompatTransport` for `openai_compat`.
  - **Verifier:** stub smoke → `results == workers`, worker artifacts + dispatch log events exist.
- **F-P3-2 (= RW-2)** concurrency Python-only test — see RW-2.
- **F-P3-3 — run path never persists `.swarm-state.json`** · **drift** · T03.03/T03.16/T03.22.
  - Evidence: `preflight.py:1790-1797` builds `SwarmState(state="preflight_ok")` but `:1799-1802` writes only `manifest.json`; `commands.py:1264-1266` dispatches without `write_state`.
  - **Fix:** persist state immediately after manifest emit and transition (`dispatching`→terminal) via `write_state(confined_path, state)` in the run path.
  - **Verifier:** after a stub run, `<out>/.swarm-state.json` exists with terminal state.
- **F-P3-4 — retry policy honors on_4xx/on_timeout despite "never" matrix** · **drift** · T03.09.
  - Evidence: `dispatch.py:250-256` (`should_retry=True` on 4xx when `retry.on_4xx`), `:259-260` (timeout). Tests bless this; tasklist says `4xx→0`, `timeout/network→0`.
  - **Fix:** remove 4xx/timeout retry from Phase-3 default behavior **or** update tasklist/roadmap to explicitly authorize configurable overrides + safe defaults.
  - **Verifier:** policy matches the documented matrix under defaults.
- **F-P3-5 — OpenAI transport loses model identity on network error** · **drift** · T03.02/T03.05/T03.09.
  - Evidence: `transports/openai_compat.py:322-337` catches only `httpx.TimeoutException`; `_build_result` (`:366-383`) stamps `model_id/model_label`; `dispatch.py:180-187` returns synthetic `proxy_error` WorkerResult without model identity.
  - **Fix:** catch `httpx.RequestError` in `send` and return `_build_result(status="proxy_error", http_code=None, ...)`, or make dispatch's fallback preserve slot model metadata.
  - **Verifier:** simulate `httpx.RequestError`; assert `WorkerResult.model_id/model_label` preserved.
- **F-P3-6 — Logger confinement bypassed at run call site** · **drift** · T03.10/T03.17.
  - Evidence: `logging_.py:101-115` applies `confine_path` only when `output_dir` set; `commands.py:1259-1263` builds `Logger` without `output_dir`.
  - **Fix:** pass `output_dir=manifest_dir` to `Logger(...)` in `run_cmd`.
  - **Verifier:** `Logger` construction includes `output_dir`.
- **F-P3-7 — output-confinement test is substring-only** · **drift** · T03.17.
  - Evidence: `tests/swarm/test_output_confinement.py:280-301` asserts only that the substring `confine_path` appears in writer modules.
  - **Fix:** replace with AST/call-site assertion per writer (`write_state`, `write_manifest`, `emit_env_missing_contract`, `Logger.__init__`).
  - **Verifier:** mutating a writer to drop the call fails the test.

### Phase 7 (M7) — VALID
- **F-P7-1 — prescribed `tests/swarm/test_detached_mode.py` absent** · **drift, LOW** · T07.11.
  - Evidence: T07.11 AC#4/Validation prescribe `test_detached_mode.py` (absent); coverage is via `test_tmux_detached.py` (13p/6s) + `test_tmux_fallback.py` (4p), no rationale recorded.
  - **Fix (decision):** (a) backfill `test_detached_mode.py` as a thin wrapper over existing detached tests, **or** (b) amend T07.11 to authorize the current test distribution.
  - **Verifier:** named file exists green, or tasklist authorizes substitution.
- *Carry-forwards OQ-7.1 (= RW-2) and OQ-7.2 (= RW-3) are owned here per CP4; land under M8 hardening.*

### Phase 8 (M8) — RE-AUDITED (corrected; ~85% complete) — see `8-rerun/REPORT.md`
Migration core (T08.01–T08.13, T08.15, T08.16) done + green. Real remaining gaps:
- **F-P8-1 — TEST-005 `tests/swarm/test_subprocess_caller.py` missing** · drift/gap, MEDIUM · T08.14. Author it, or reconcile/rename vs existing `tests/swarm/test_non_claude_caller.py` (T08.02) if intent duplicates. **Verifier:** file exists + green.
- **F-P8-2 — TEST-008 `tests/swarm/integration/conftest.py` missing** · drift/gap, MEDIUM · T08.17. Wire the deterministic-fixture (stub) transport into the integration suite. **Verifier:** integration conftest present; fixture-transport integration tests collect.
- **F-P8-3 (= RW-6) — `phase-8-cp3.md` + `phase-8-cp4.md` (end-of-phase exit) missing** · admin, LOW. Regenerate from SwarmPost after gaps close.
- **F-P8-4 (= RW-2) — INV-002 2 failures (TEST-002 / T08.10)** — `test_concurrency_python_only.py` tmux-subprocess; M8 is the designated home to harden OQ-7.1. See RW-2.
- *Refuted false-negatives from the invalid run (SKILL.md unmigrated, tests/swarm absent, boundary-guard broken, release-notes false-state) — no action.*

### Phase 5 (M5) — VALID, code complete
- Only **RW-6** (missing `phase-5-cp1/cp2/cp3.md`). All 10 code deliverables pass (196/196). No functional fixes.

### Phase 6 (M6) — VALID, clean
- **No fixes.** All T06.01–T06.10 success, 91 tests pass.

---

## 3. Phase 9 (M9) — plan edits BEFORE executing (pre-mode)

Phase 9 was never executed; these harden the plan prior to a `sprint run --start 9`.

- **F-P9-1 — deliverable path duplication (do first)** · MEDIUM. Plan declares `docs/swarm/operator-runbook.md` but `docs/swarm/runbook.md` already exists; plan declares `docs/swarm/lens-contribution-policy.md` but `docs/dev/lens-contribution-policy.md` already exists. **Fix:** pick one path per artifact and update T09.01 + T09.06 (avoid duplicate-doc divergence).
- **F-P9-2 — human-gated sign-offs need explicit HALT** · MEDIUM. T09.01 (ops-reviewer exercise), T09.04/T09.08 (sign-off capture), T09.05 (tabletop rehearsal + sign-off) must HALT + write PENDING rather than auto-fill a date/sign-off line (per `feedback_human_decision_items_must_halt`). **Fix:** mark those items human-gated HALT.
- **F-P9-3 — OPS-003 4-vs-5 monitoring surfaces** · MEDIUM. Roadmap OPS-003 description names 5 surfaces incl. `return-contract.yaml`; AC says 4; plan implemented 4. **Fix:** decide whether OPS-003 or OPS-001 owns the `return-contract.yaml` troubleshooting recipe; reconcile the roadmap AC.
- **F-P9-4 (optional, LOW)** drop no-op `make sync-dev` completion step from doc/script-only tasks (T09.01/02/03/05/06/07). **F-P9-5 (optional, LOW)** add an explicit M9 entry-gate assertion (A/B parity + TEST-001..007 green) to T09.04.

---

## 4. Priority-ordered execution sequence

1. **F-P3-1 (CRITICAL)** — fix stub transport no-op; without it `swarm run` does nothing.
2. **RW-4, RW-5, RW-1** — clear commit gates (detect-secrets, markdownlint, verify-sync) so per-phase commits stop failing (likely the original Phase-7 exit-1 cause).
3. **RW-2, RW-3** — INV-002 + UV-enforcement test scoping (OQ-7.1/7.2).
4. **F-P1-3** (frozen decision) · **F-P2-1** (custom_prompt_dir) · **F-P2-2** (CallerMetadata).
5. **F-P3-3..7** (state persist, retry, model-identity, logger confine, confinement test).
6. **F-P7-1** (detached test decision).
7. **RW-6** — regenerate all missing/stale checkpoints from SwarmPost.
8. **§5 re-run** Phase 8 reflect from SwarmPost; act on its *real* findings only.
9. **F-P9-*** — plan edits, then execute Phase 9 (`sprint run --start 9 --end 9` from SwarmPost).

---

## 5. Re-run / re-validation matrix

| Phase | Re-run reflect? | Why |
|---|---|---|
| 8 | ✅ **DONE** (`8-rerun/REPORT.md`) | re-audited from SwarmPost → partial ~85%; fixes F-P8-* |
| 1,2,3 | after fixes (rerun post) | confirm regressions cleared |
| 5 | after RW-6 | confirm checkpoints present |
| 7 | after F-P7-1 | confirm drift resolved |
| 6 | no | already clean |
| 9 | after F-P9-* (rerun pre) | confirm plan edits |

**Phase 8 re-run command (cwd = SwarmPost):**
```
/sc:reflect --mode post --depth deep --diff HEAD --tasklist /config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-8-tasklist.md --spec /config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/roadmap.md --output /config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/validation/deep/8-rerun
```

## 6. Aggregate deviation tally (valid reports incl. Phase-8 re-audit)

| Class | Count | Items |
|---|---|---|
| Regression (HIGH/CRITICAL) | 6 | F-P1-1, F-P1-2(RW-1), F-P1-3, F-P2-1, F-P3-1, F-P3-2(RW-2) |
| Regression (MEDIUM) | 1 | F-P2-2 |
| Drift | 6 | F-P3-3, F-P3-4, F-P3-5, F-P3-6, F-P3-7, F-P7-1 |
| Drift/gap (P8 re-audit) | 2 | F-P8-1 (TEST-005), F-P8-2 (TEST-008) |
| Commit-gate (repo) | 2 | RW-4, RW-5 |
| Admin (checkpoints) | 1 group | RW-6 (P1/P2/P5 = 5 files + P8 cp3/cp4 = 2) |
| Plan edits (P9) | 5 | F-P9-1..5 |
| Authorized / Necessary | — | P5 checkpoints, P7 carry-forwards, P1 F5, P8 refuted-false-negatives — no code change |

> Phase 8 is **~85% complete** (not 25%) — migration core done; only TEST-005, TEST-008, CP3/CP4, and the
> shared RW-2 remain. The original `8/REPORT.md` is superseded by `8-rerun/REPORT.md`.
