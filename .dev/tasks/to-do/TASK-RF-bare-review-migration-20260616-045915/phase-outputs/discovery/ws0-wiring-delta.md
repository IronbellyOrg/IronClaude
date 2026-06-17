# WS-0 Wiring-Delta Inventory (inline `swarm run` vs `--resume`)

**Status: Complete**
**Author:** task executor (Step 2.1, L1 discovery)
**Date:** 2026-06-16
**Source-of-truth:** every claim below carries a `file:line` anchor read directly from source on 2026-06-16. No fabrication.

Purpose: extract the exact current inline `run_cmd` call shape, the resume-branch
pipeline it must mirror, the real signatures of `dispatch_wave1` / `normalize_wave2` /
`reduce_wave3` / `emit_contract`, and where the assembled prompt + worker_spec + the
per-worker output paths come from — so WS-0 (Steps 2.2–2.10) wires the inline path
through the full Wave 1→2→3 pipeline correctly.

## (a) Current inline `run_cmd` call + the stub it emits

`run_cmd` is defined at `commands.py:1304-1578`. The non-resume, non-detached body
runs preflight → constructs the transport factory → dispatches → **stops**.

- **Dispatch call (the only wave it runs):** `commands.py:1554-1556`
  ```py
  worker_results = dispatch_wave1(
      preflight_result, transport_for_slot=run_transport_factory, logger=logger
  )
  ```
  Note: NO `prompt=`, NO `worker_spec=` keyword is passed — both default
  (`prompt=""`, `worker_spec=None`). See dispatch signature in §(c).
- **State flip to terminal (premature):** `commands.py:1562-1567`
  ```py
  if state_output_dir is not None:
      _write_swarm_state(state_output_dir, "terminal", preflight_result.manifest.job_id)
  ```
- **Stub stdout line + exit:** `commands.py:1573-1578`
  ```py
  click.echo(
      f"swarm run: dispatched job (mode={mode}, "
      f"workers={preflight_result.manifest.preflight.workers_requested}, "
      f"results={len(worker_results)})"
  )
  raise click.exceptions.Exit(EXIT_OK)
  ```
  The docstring at `commands.py:1348-1349` explicitly calls this the "return-contract
  stub … M5 replaces this with the full ResultContract writer", and `commands.py:1558-1561`
  comments that "Wave 1 is the terminal wave for this T03.01 run body (the M5
  normalize/reduce pipeline is wired separately)". **It was never wired.** → no
  `normalize_wave2`, no `reduce_wave3`, no `return-contract.yaml`, no per-reviewer
  `.final.md` bodies for a fresh (non-resume) run.

## (b) Resume-branch call sequence the inline path must replicate

`_run_resume_branch` at `commands.py:1714-1998`. The full pipeline it runs:

1. **Dispatch (remaining slots):** `commands.py:1930-1934`
   ```py
   raw_redispatched = dispatch_wave1(
       synthetic_preflight, transport_for_slot=_resume_slot_transport, logger=None,
   )
   ```
   Again NO `prompt=`/`worker_spec=` — relies on the transport (stub returns canned
   fixtures; openai_compat would send `prompt=""` — a latent gap on the real path,
   out of WS-0 scope but noted for Step 2.6).
2. **Reindex** returned slots back onto original positions: `commands.py:1939-1947`.
3. **Normalize:** `commands.py:1950-1962`
   ```py
   redispatched = normalize_wave2(redispatched, recipe_name=recipe_name)
   ```
   where `recipe_name = rehydrated_spec.normalization.recipe` (`commands.py:1866`).
4. **Combine + sort by slot index:** `commands.py:1964-1974`.
5. **Reduce (emits contract internally):** `commands.py:1977-1985`
   ```py
   reduce_wave3(
       combined, mode=amalgamation_mode, output_dir=output_path,
       workers_requested=workers_requested, status_policy=rehydrated_spec.status_policy,
       job_id=manifest_obj.job_id, resume=True,
   )
   ```
   `amalgamation_mode = rehydrated_spec.amalgamation_mode` (`commands.py:1865`).
   The resume branch calls ONLY `reduce_wave3` — it does NOT call `emit_contract`
   separately (reduce emits it internally; see §(c)). **WS-0 must mirror this: call
   reduce_wave3 only, do NOT add a redundant explicit `emit_contract`.**
6. **State terminal + stdout:** `commands.py:1990-1998`.

## (c) Exact signatures (parameter names)

- **`dispatch_wave1`** — `dispatch.py:334-343`:
  ```py
  def dispatch_wave1(
      preflight_result: PreflightResult,
      transport: Optional[Transport] = None,
      *,
      transport_for_slot: Optional[Callable[[int], Transport]] = None,
      prompt: str = "",                       # dispatch.py:339 — verbatim to transport.send
      parallel_executor: Optional[ParallelExecutor] = None,
      worker_spec: Optional[WorkerSpec] = None,   # dispatch.py:341 — timeout + RetryPolicy
      logger: Optional[Logger] = None,
  ) -> list[WorkerResult]:
  ```
  `prompt` flows: `dispatch_wave1` → `_run_worker(index, transport, prompt, spec, logger)`
  (`dispatch.py:457-459`) → `retry_policy(transport, prompt, spec)` (`dispatch.py:309`)
  → `transport.send(prompt, timeout_sec)` (`dispatch.py:170`). The StubTransport
  ignores `prompt` and returns canned fixture bodies, so for `--transport stub`
  (the WS-0 presence test + WS-B parity gate) the prompt content is **moot**.
  `_run_worker` stamps ONLY `result.index = index` (`dispatch.py:310`); it does NOT
  stamp `final_path`/`meta_path`/`raw_path`.

- **`normalize_wave2`** — `normalize.py:500-507`:
  ```py
  def normalize_wave2(
      worker_results: list[WorkerResult],
      recipe_name: str,
      *,
      schema_version: str = "1.0",
      recipe_args: Optional[dict[str, Any]] = None,
      salvage_enabled: bool = True,
  ) -> list[WorkerResult]:
  ```
  **REQUIRES each worker carry `final_path` + `meta_path`** (docstring `normalize.py:512-516`).
  The atomic body write is gated on it: `if worker.final_path and result.text:`
  (`normalize.py:482-483`). If `final_path` is empty, NO body is written to disk.

- **`reduce_wave3`** — `reduce.py:555`, with internal contract emission at
  `reduce.py:722` (`emit_contract(contract, Path(output_dir))`).
- **`emit_contract`** — `reduce.py:369`; writes `output_dir / CONTRACT_FILENAME`
  where `CONTRACT_FILENAME = "return-contract.yaml"` (`reduce.py:139`, target build
  `reduce.py:390`). `reduce_wave3` normalize-mode keeps each worker's `final_path`
  as the artifact (`reduce.py:243`); `output_files=list(worker_results)` (`reduce.py:713`).

## (d) Where prompt + worker_spec + the per-worker PATHS come from

- **prompt / worker_spec:** the resume branch obtains NEITHER via a reusable
  assembly helper — it rehydrates spec state (`resume_mode`, `commands.py:1832`) and
  passes neither to `dispatch_wave1`. There is **no shared lens-prompt→target_content
  assembly helper** in a non-resume path to call. So for Step 2.6 the inline path
  must assemble the worker prompt directly from the resolved lens
  (`lenses/bare_review.py:47-57`: `system_prompt_fragment` + `user_template` with the
  `<<<TARGET>>>`/`<<<END TARGET>>>` delimiters and preflight's truncated target
  content). For `--transport stub` this is cosmetic (stub ignores prompt); it matters
  only for `openai_compat` real runs.

- **PER-WORKER OUTPUT PATHS — THE HEADLINE GAP (drives Step 2.7):**
  Nothing stamps `final_path`/`meta_path`/`raw_path` on freshly-dispatched workers.
  - `dispatch_wave1` does not (only `result.index`, `dispatch.py:310`).
  - The transports do not (`grep final_path src/superclaude/cli/swarm/transports/*.py`
    → no matches).
  - The ONLY place `final_path` is ever populated today is the **resume** path's
    `discover_succeeded_slots` (`commands.py:1700-1709`), which READS sidecars
    (`*.meta.json` + sibling `*.final.md` / `*.raw.md`) that a PRIOR successful run
    wrote to disk. Since the only prior run is the inline stub (which writes nothing),
    those sidecars never exist for a fresh bare-review run.
  - Filename convention: `CANONICAL_FILENAME_TEMPLATE = "{lens}-{index:02d}-{model_slug}.md"`
    (`preflight.py:414`; also `OutputSpec.filename_template` default `models.py:508`;
    set in `_build_spec_from_lens` at `commands.py:847`). The resume reader derives the
    sibling `*.final.md` / `*.raw.md` / `*.meta.json` from the `*.meta.json` stem
    (`commands.py:1687-1689`); the slot index is parsed from the `-NN-` segment via
    `_META_SLOT_INDEX_RE` (`commands.py:1669`), and the model_slug tail at
    `commands.py:1694`. There is **no** `.format()`-style render helper for the template
    anywhere (`grep` of all swarm `*.py` for a template renderer → none).

  **Implication for Step 2.7:** the inline path must, BETWEEN dispatch and normalize,
  stamp each returned `WorkerResult` with `final_path` (and `meta_path`, `raw_path`)
  built under the `--output` dir from the resolved lens name + `{index:02d}` +
  `model_slug` (the transport stamps `model_id`/`model_label` per slot, so the slug is
  available post-dispatch), so that `normalize_wave2` actually writes the per-reviewer
  `.final.md` bodies and `reduce_wave3` populates `output_files`. This is more than a
  mechanical "mirror the resume branch" — it is net-new path-stamping logic. The
  meta/final/raw suffix convention to honor is the one the resume reader expects
  (`commands.py:1687-1689`): `<stem>.meta.json`, `<stem>.final.md`, `<stem>.raw.md`
  where `<stem>` renders the canonical template (minus the trailing `.md`).

## (e) Spec-dict fields WS-0 flags must reach (cross-ref for Steps 2.2–2.5)

- `_build_spec_from_lens` builds the inline spec: worker count derivation
  `workers_count = max(1, int(entry.default_workers or 1))` (`commands.py:767`),
  `workers.models` list sized to `workers_count` (`commands.py:788`),
  `workers.timeout_sec` (`commands.py:789`), `caller.invocation_label`
  (`commands.py:775`), `output.line_cap` from `entry.default_target_line_cap`
  (`commands.py:817`), `output.filename_template` (`commands.py:847`).
- Override block (where CLI `--target`/`--output`/`--transport` already mutate
  spec_dict): `commands.py:1449-1454`. The 4 new flags thread here / into spec_dict.
- `expand_lens_defaults` reset traps in `preflight.py` (the `count==4` / `line_cap==4000`
  / `<=0` substitution) — to be confirmed at the exact lines during Steps 2.2/2.3.
- INV-005 model-pool guard in `preflight.py` (clamps/rejects when `workers.count`
  exceeds the model-pool size) — Step 2.2 must resize `workers.models` to `--reviewers N`.
- bare-review lens defaults: `lenses/bare_review.py` — `default_workers=3` (:61),
  `default_target_line_cap=4000` (:62), `system_prompt_fragment` (:47-52),
  `user_template` (:53-57). (Anchors to re-confirm when each flag item runs.)
