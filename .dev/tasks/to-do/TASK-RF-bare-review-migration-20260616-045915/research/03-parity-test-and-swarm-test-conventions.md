# R3 — Parity Test & Swarm Test Conventions (sc-bare-review M8/M9 migration)

**Status: Complete**

Scope: `tests/swarm/test_bare_review_parity.py` and `tests/swarm/` conventions; design an end-to-end CLI-vs-legacy A/B gate that survives legacy-script deletion (WS-C).

All paths absolute under `/config/workspace/IronClaude/`. Every claim carries file:line evidence.

---

## 1. What `test_bare_review_parity.py` compares TODAY

**File:** `/config/workspace/IronClaude/tests/swarm/test_bare_review_parity.py` (795 lines).

### 1.1 It composes LIBRARY surfaces, NOT the CLI — the module says so explicitly

The module docstring has a whole section titled **"Why not drive the actual CLI subprocess"**:

- `test_bare_review_parity.py:38-51` — *"The thin-caller path -- `swarm run --lens bare-review` -- is itself a wrapper... The bytes a real CLI invocation produces are the same bytes the library pipeline produces... Driving the library composition directly keeps the gate fast, deterministic, and free of the env-var dance... the recipe + reducer composition is the real per-byte surface either lane will emit."*

So the "thin-caller" side is **not** a subprocess / CliRunner invocation. It is a direct in-process call to the recipe class plus the reducer function:

- Imports: `test_bare_review_parity.py:97-100` —
  `from superclaude.cli.swarm.lenses import LENSES`,
  `from superclaude.cli.swarm.models import StatusPolicy, WorkerResult`,
  `from superclaude.cli.swarm.recipes.bare_review_v1 import BareReviewV1`,
  `from superclaude.cli.swarm.reduce import determine_status`.
- Thin-caller driver `_run_thin_caller`: `test_bare_review_parity.py:384-457`. It instantiates `recipe = BareReviewV1()` (`:394`), calls `result = recipe.normalize(raw_text, args)` per reviewer (`:428`), and reduces with `determine_status(workers_succeeded=…, workers_requested=…, policy=StatusPolicy())` (`:452-456`). **No `swarm run`, no `CliRunner`, no `JobSpec`, no preflight, no transport.**

### 1.2 The LEGACY side imports the standalone script via importlib

- `test_bare_review_parity.py:53-64` (docstring "Legacy path") — *"We import the standalone `t2_normalize.py`... via importlib and run `t2_normalize.main` against a hand-staged manifest... The dispatcher (`t2_dispatch.sh`) is bypassed because it requires a live proxy; we stage the per-reviewer `.raw` + `.meta.json` sidecars directly."*
- Loader: `_load_legacy()` at `test_bare_review_parity.py:232-240` uses `importlib.util.spec_from_file_location(...).exec_module(module)` against `LEGACY_SCRIPT`.
- `LEGACY_SCRIPT` path: `test_bare_review_parity.py:111-119` =
  `<repo>/src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py`.
- Legacy driver `_run_legacy`: `:352-374` — monkeypatches `legacy.iso_now` to `FIXED_GENERATED` (`:360`), sets `sys.argv` to `["t2_normalize.py", "--manifest", <path>]` (`:361-363`), calls `legacy.main()` (`:364`), then reads the contract YAML back off disk (`:370-373`).

**Conclusion:** today's gate compares **`t2_normalize.py` (legacy lib) vs `BareReviewV1` recipe + `determine_status` (new lib)**. Both halves are library-level; neither drives `superclaude swarm run`. The audit's characterization is correct, with the test's own docstring admitting it (`:38-51`).

### 1.3 The `skipif(LEGACY_SCRIPT.exists())` guard

- `test_bare_review_parity.py:217-224`:
  ```python
  pytestmark = pytest.mark.skipif(
      not LEGACY_SCRIPT.exists(),
      reason=( f"Legacy t2_normalize.py missing at {LEGACY_SCRIPT}. "
               f"This is expected post-T08.07 / MIG-003 legacy retirement; "
               f"until then the file's presence is the migration sequencer." ),
  )
  ```
- Docstring "Skip semantics" `:76-82` — *"Post-T08.07 (legacy retirement) the gate will be removed wholesale; until then the file's presence is the migration sequencer -- if it's gone, we're past the gate."*

**This is the core migration hazard.** When WS-C deletes `t2_normalize.py`, this entire module **self-deactivates silently** (whole-module skip) — it does not fail, it just stops asserting anything. The parity gate evaporates exactly when the legacy reference it compares against disappears. There is no permanent post-deletion gate. That is the gap R3 must fill.

### 1.4 Fixtures, pinned determinism, and assertions

- Fixture corpus: `FIXTURES_DIR = Path(__file__).parent / "fixtures" / "bare_review_v1"` (`:108`). On-disk files (verified): `/config/workspace/IronClaude/tests/swarm/fixtures/bare_review_v1/{basic_findings.raw.txt, verdict_only.raw.txt, odd_cites.raw.txt, salvage.raw.txt, freeform_fallback.raw.txt}`.
- Determinism pins: `FIXED_GENERATED = "2026-06-01T17:59:55Z"` (`:124`), `FIXED_CHECKSUM = "abcd1234efef"` (`:125`), `CALLER_LABEL = "parity-gate"` (`:126`), `ELAPSED_MS = 12345` (`:127`). The `generated` timestamp is the **only** wall-clock-dependent frontmatter field; both sides consume `FIXED_GENERATED` so the byte comparison is mechanical (`:19-22`, `:490-497`, `:725-754`).
- 3 scenarios (`SCENARIOS`, `:149-182`): `all-success` (M==N==3 → success), `partial-with-timeout` (M=2,N=3 → partial), `salvage-promoted` (parse_error body that parses → success).
- 7 tests (all but two parametrized over the 3 scenarios):
  1. `test_legacy_vs_thin_caller_byte_identical_markdown` (`:483-524`) — per-reviewer normalized `.md` byte-equality: legacy reads `final_path` off disk (`:512-515`), new reads `new_rec["text"]` (`:516`), asserts `new_text == legacy_text` (`:517`).
  2. `test_legacy_vs_thin_caller_aggregate_status` (`:537-562`) — `legacy_contract["status"] == new_status == expected_status` (`:558`).
  3. `test_legacy_vs_thin_caller_per_reviewer_status` (`:575-612`) — per-slot status list equality (`:599`) + M-count agreement (`:606`, `:611`).
  4. `test_legacy_contract_carries_suspect_true_and_adversarial_handoff` (`:625-674`) — legacy contract `suspect is True` (`:647`) + `/sc:adversarial --suspect-source` in `recommended_next_command` (`:651`,`:655`); new side asserts on `LENSES["bare-review"].suspect` (`:665`) + `recommended_next_command_template` (`:668-673`).
  5. `test_legacy_vs_thin_caller_output_file_count` (`:687-715`) — `len(output_files) == len(new_records) == len(plan)` (`:711`).
  6. `test_deterministic_generated_threads_through_both_pipelines` (`:725-754`) — both stamp `generated: "<FIXED_GENERATED>"` (`:744`,`:751`).
  7. `test_thin_caller_records_round_trip_through_worker_result` (`:764-794`) — record dict maps onto `WorkerResult`.

**Note (assertion #4 asymmetry):** the legacy side checks the *rendered contract*; the new side checks the *lens registry template*, not a CLI-emitted contract (`:660-664` explains this decouples from "the M5 substitution wiring"). That asymmetry is exactly what an end-to-end CLI gate would close.

---

## 2. tests/swarm/ conventions — how to drive the actual CLI

Other swarm tests **do** drive the CLI, via Click's `CliRunner` against the registered `swarm_group`. This is the canonical pattern R3 should reuse.

### 2.1 The reusable hermetic e2e pattern: `test_e2e_user_guide.py`

**File:** `/config/workspace/IronClaude/tests/swarm/test_e2e_user_guide.py` — *"the `swarm_group` is invoked through click's `CliRunner` so the full Wave 0 preflight -> Wave 1 dispatch -> artifact write path runs for real. Every runnable example uses `--transport stub` (in-process, deterministic, no network)... hermetic and CI-safe."* (`:1-16`).

- Imports: `from click.testing import CliRunner` (`:24`); `from superclaude.cli.swarm import swarm_group` (`:26`).
- Runner fixture: `:56-58`. Target fixture (`>=50` non-ws bytes to clear IMM-4): `:61-65`.
- **Invocation helper (the pattern to reuse):** `test_e2e_user_guide.py:68-70`:
  ```python
  def _run(runner, *args, **kwargs):
      return runner.invoke(swarm_group, list(args), **kwargs)
  ```
- **Bare-review stub run, verbatim:** `test_e2e_user_guide.py:80-97`:
  ```python
  result = _run(runner, "run", "--lens", "bare-review",
      "--target", str(target), "--output", str(out), "--transport", "stub")
  assert result.exit_code == EXIT_OK, result.output
  assert "dispatched job (mode=lens, workers=3, results=3)" in result.output
  ```
- Exit-code symbols imported from `superclaude.cli.swarm.commands`: `EXIT_OK, EXIT_INVALID, EXIT_USAGE` (`:27-37`).

### 2.2 The live-proxy variant (NOT for the gate): `test_e2e_real_proxy.py`

- `/config/workspace/IronClaude/tests/swarm/test_e2e_real_proxy.py:146-160` — `_run_lens` calls `runner.invoke(swarm_group, ["run","--lens",lens,"--target",...,"--output",...,"--transport","openai_compat"])`.
- Gated/skipped unless `SWARM_REAL_E2E=1` + `T2ProxyKey` + `T2ProxyUrl` (`:65-73`). **Spends real tokens.** Do NOT use this for a CI parity gate; it's the openai_compat counterpart.

### 2.3 Other CliRunner users (registration/surface only)

- `test_cli_registration.py:18,100-131` — `runner.invoke(main, ["swarm","--help"])` and per-subcommand `--help`.
- `test_attach_cmd.py:29,58+` — `runner.invoke(swarm_group, ["attach", …])`.
- `test_commands_run.py`, `test_swarm_run_inputs.py` — also import `swarm_group`/`CliRunner` for `run` input handling (grep-confirmed). These pin registration + preflight handshake (the parity-test docstring cites `test_commands_run.py` at `:50-51`).

**Reuse verdict:** mirror `test_e2e_user_guide.py::_run` exactly — `runner.invoke(swarm_group, ["run","--lens","bare-review","--target",<t>,"--output",<o>,"--transport","stub"])`.

---

## 3. Determinism — making `swarm run --lens bare-review` reproducible

### 3.1 `--transport stub` is hermetic by construction

- `StubTransport` body is a **pure function of `(model_id, prompt)`**: `test_stub_transport.py:57-84` (same inputs → byte-identical body; distinct model/prompt → distinct body). No clock, no network — `test_send_makes_no_socket_calls` guards `socket.socket` (`:138-152`).
- Constructor accepts an explicit `fixtures=(...)` corpus served in lock order with modular wrap-around: `test_stub_transport.py:92-98`. This is the lever to feed **canned reviewer bodies** deterministically instead of the hash-generated default body.
- Source: `/config/workspace/IronClaude/src/superclaude/cli/swarm/transports/stub.py`.

### 3.2 The deterministic frontmatter pin

Both pipelines must stamp a fixed `generated` timestamp or the markdown diverges by wall-clock. Today's library gate threads `FIXED_GENERATED` through `args["generated"]` (`:426`) on the new side and monkeypatches `legacy.iso_now` (`:360`) on the legacy side. A CLI gate must inject the same fixed timestamp into the recipe args the CLI builds — see §4.4 for the wiring risk.

### 3.3 ⚠️ BLOCKER: fresh `swarm run` is dispatch-only — it does NOT normalize/reduce or persist worker content

This is the single most important finding for the design, and it breaks the naive "CLI output vs golden" approach:

- `commands.py:1558-1577` — after `dispatch_wave1`, the comment states *"Wave 1 is the terminal wave for this T03.01 run body (the M5 normalize/reduce pipeline is wired separately)"*, flips state to terminal, and emits only a stdout stub line `swarm run: dispatched job (mode=…, workers=…, results=…)` (`:1573-1577`). No contract, no per-worker `.md` written.
- `test_e2e_user_guide.py:104-114` (`test_quickstart_does_not_emit_m5_artifacts`) **pins** that the dispatch path does NOT produce `merged.md` / `return-contract.yaml` / `done.json`. Artifact set is exactly `{swarm-state, execution-log.jsonl, execution-log.md, manifest.json}` (`:91-97`).
- `test_e2e_real_proxy.py:28-32` confirms the same: *"`swarm run` is dispatch-only today: it writes execution-log.{jsonl,md}, manifest.json, .swarm-state.json. Worker *content* is not persisted to disk in this mode."*
- The normalize+reduce stages (which produce final `.md` bodies + `return-contract.yaml`) are wired **only into the `--resume` path**: `commands.py:1949-1977` calls `normalize_wave2(...)` then `reduce_wave3(...)`; the resume orchestrator docstring `:1582-1592` says it *"drives dispatch + normalize + reduce directly."* The fresh `run_cmd` body does not.
- `normalize_wave2` IS the seam that writes normalized bodies to disk: `src/superclaude/cli/swarm/normalize.py:482-483` — `if worker.final_path and result.text: bytes_written = _atomic_write_text(Path(worker.final_path), result.text)`. So the content the golden would compare exists only after `normalize_wave2` runs.

**Implication:** Until R2's CLI-surface work lands the M5 normalize/reduce stage onto the fresh `swarm run` path (or the gate drives `--resume`), `swarm run --lens bare-review --transport stub` produces NO per-reviewer normalized markdown and NO contract to compare against a golden. A CLI-vs-golden gate is **blocked on M5 wiring** (coordinate with R2). See §4.5 for the sequencing.

---

## 4. DESIGN — frozen-golden CLI parity gate (survives WS-C deletion)

### 4.1 Problem restated

WS-C deletes `t2_normalize.py`. Today's gate (§1.3) then whole-module-skips — silently losing all parity coverage. We need a **permanent** gate that needs NO live legacy script and drives the **actual CLI**.

### 4.2 Recommended approach: capture a FROZEN legacy golden BEFORE deletion

Two artifacts, committed to the repo, become the permanent reference:

1. **Frozen legacy golden** — run the legacy `t2_normalize.py` path (the exact `_stage_legacy_manifest` + `_run_legacy` machinery already in `test_bare_review_parity.py:268-374`) against the fixed fixtures **once, before WS-C deletes the script**, and serialize the produced per-reviewer `.md` bodies + the `return-contract.yaml` to committed golden files. This freezes the legacy bytes the migration must preserve.
2. **Permanent CLI gate** — a new test drives `superclaude swarm run --lens bare-review --transport stub` (§2.1 pattern) with fixtures fed via `StubTransport(fixtures=…)` and the fixed `generated` pin, reads the CLI's on-disk normalized `.md` + contract, and asserts **byte-equality against the frozen golden**. No legacy script needed at run time → survives deletion.

### 4.3 Where the golden fixtures should live

Co-locate under the existing swarm fixtures tree (consistent with `FIXTURES_DIR` at `test_bare_review_parity.py:108`):

```
/config/workspace/IronClaude/tests/swarm/fixtures/bare_review_v1/golden/
    all-success/            # one dir per SCENARIOS entry (:149-182)
        bare-review-01-<slug>.md
        bare-review-02-<slug>.md
        bare-review-03-<slug>.md
        return-contract.yaml
    partial-with-timeout/
        ...
    salvage-promoted/
        ...
```

Reuse the existing `.raw.txt` canned bodies in `tests/swarm/fixtures/bare_review_v1/` as the StubTransport corpus, so input and golden live side by side. The scenario IDs and reviewer-slot naming already exist in the test (`_slug_model` at `:189-201`, `_model_id` at `:204-205`).

### 4.4 Wiring the deterministic `generated` into the CLI run

The byte comparison hinges on a fixed `generated` (§3.2). Options, in order of preference:
- **Preferred:** a CLI/JobSpec field that threads a fixed `generated` into recipe args (so the same injection point exists for real runs at debug time). Confirm with R2 whether such a flag/spec field exists; if not, it must be added as part of M5.
- **Fallback:** monkeypatch the recipe's timestamp source the same way the legacy gate monkeypatches `iso_now` (`:360`). Find the new-path equivalent in `BareReviewV1.normalize` / `normalize.py` (the recipe consumes `args["generated"]` at `test_bare_review_parity.py:426`, so a fixed-`generated` arg is already supported at the recipe layer — the question is only whether the CLI lets a test inject it).

### 4.5 Sequencing (hard dependency on R2 / M5)

1. **Gate-capture step (must run BEFORE WS-C):** add a one-shot regen script/marker that runs the legacy `_run_legacy` machinery and writes the golden tree (§4.3). Commit the golden. This is the "freeze the reference" moment.
2. **M5 dependency:** the permanent CLI gate can only assert on CLI-produced markdown once `swarm run --lens bare-review --transport stub` actually runs normalize+reduce on the fresh path and persists `final_path` bodies + `return-contract.yaml`. Per §3.3 that is NOT true today on the fresh path (only `--resume`). **Coordinate with R2 (swarm CLI surface):** either (a) M5 lands normalize/reduce on the fresh `run` path, or (b) the gate drives the documented `--resume` flow, or (c) the gate asserts at the `normalize_wave2`/`reduce_wave3` library seam fed by a stubbed dispatch — but option (c) regresses to "library, not CLI," which is the exact flaw being fixed.
3. **Cutover:** once the CLI gate is green against the frozen golden, WS-C deletes `t2_normalize.py`; the new gate keeps asserting (no `LEGACY_SCRIPT.exists()` skip), and the old `test_bare_review_parity.py` is removed wholesale (its docstring already says it should be — `:80-82`).

### 4.6 How to regenerate the golden

Provide a `pytest`-skippable regen entry (e.g. an env-gated test or a `scripts/` helper, mirroring `test_e2e_real_proxy.py`'s `SWARM_REAL_E2E` gating at `:65-73`) that, when explicitly invoked, re-runs the legacy machinery (while the script still exists) OR — post-deletion — re-runs the CLI and re-blesses the golden. Document that regeneration is a deliberate, reviewed act (golden updates must be human-approved, not auto-blessed), consistent with the project's "human-decision items must HALT" discipline.

### 4.7 What the permanent gate asserts (carry forward from §1.4)

Keep the 5 substantive invariants, now CLI-driven vs frozen golden:
1. Per-reviewer normalized `.md` byte-equality (CLI on-disk `final_path` body vs golden `.md`).
2. Aggregate IMM-5 status (`return-contract.yaml` `status`) — success/partial/failed across the 3 scenarios.
3. Per-slot status set + M/N counts (contract `output_files[].status`, `reviewers_succeeded`, `reviewers_requested`).
4. `suspect: true` + `recommended_next_command` containing `/sc:adversarial --suspect-source` — now from the **CLI-emitted contract**, closing the §1.4 asymmetry where the new side only checked the lens template (`:660-673`).
5. `output_files` length == requested workers.

---

## Summary for the tasklist author

- **Today's gate is library-vs-library, self-admittedly** (`test_bare_review_parity.py:38-51`), comparing `t2_normalize.py` (importlib) against `BareReviewV1.normalize` + `determine_status`. It is **whole-module skipped** the instant `t2_normalize.py` is deleted (`:217-224`) — so WS-C silently destroys parity coverage. This is the gap.
- **Reuse the CliRunner pattern from `test_e2e_user_guide.py:68-70` + `:80-97`** (`runner.invoke(swarm_group, ["run","--lens","bare-review","--target",…,"--output",…,"--transport","stub"])`). `swarm_group` import at `:26`.
- **Determinism:** `--transport stub` is pure-function/no-network (`test_stub_transport.py:57-84,138-152`); feed canned bodies via `StubTransport(fixtures=…)` (`:92-98`); pin `generated` (§4.4).
- **HARD BLOCKER:** fresh `swarm run` is **dispatch-only** — no normalized `.md`, no `return-contract.yaml` (`commands.py:1558-1577`; pinned by `test_e2e_user_guide.py:104-114`). Normalize/reduce + on-disk `final_path` writes (`normalize.py:482-483`) run **only on `--resume`** (`commands.py:1949-1977`). The CLI golden gate is therefore **dependent on R2/M5 landing normalize+reduce on the fresh path** (or driving `--resume`). Flag this dependency explicitly in the tasklist.
- **Design:** freeze a legacy golden under `tests/swarm/fixtures/bare_review_v1/golden/<scenario>/` (per-reviewer `.md` + `return-contract.yaml`) BEFORE WS-C deletes the script; permanent gate = CLI output vs frozen golden; golden regen is a deliberate, human-approved, env-gated step.

**Status: Complete**
