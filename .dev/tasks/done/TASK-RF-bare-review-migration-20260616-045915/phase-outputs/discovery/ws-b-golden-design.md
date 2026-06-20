# WS-B Golden-Capture Design (Step 4.1) — grounded ground truth

**Status: Complete**

This note records the decisive ground truth gathered for Step 4.1 so a context
rollover cannot lose it. It reconciles the legacy golden with the **actual** CLI
stub output and defines the capture scheme Step 4.3's gate must mirror.

## Two ground truths (captured live, 2026-06-16)

### Legacy `t2_normalize.py` output (the parity test's machinery)
- `.md` frontmatter (in order): `schema_version, tier, suspect, reviewer_model_id,
  reviewer_model_label, target, target_checksum, target_truncated, generated,
  caller_label, elapsed_ms, finding_count`.
- Contract = **FLAT** legacy schema: `contract_version, status, target, target_checksum,
  target_truncated, reviewers_requested, reviewers_succeeded, output_files:[{path,
  model_id, model_label, bytes, status, elapsed_ms}], suspect, recommended_next_command`.
- The parity test fed FAKE pins: `model_id="parity-model-NN"`, `target_checksum="abcd1234efef"`,
  `caller_label="parity-gate"`, `elapsed_ms=12345`, 1-based filenames `bare-review-01-<slug>.md`.
- Legacy `main()` (`t2_normalize.py:272,215,238`) stamps the manifest's `target_checksum`
  **verbatim** and stamps `generated` from `iso_now()` (monkeypatchable).

### Real CLI `swarm run --lens bare-review --transport stub` output (post-WS-0)
- Files: `bare-review-00-<model-slug>.final.md` (**0-based**, `.final.md` suffix),
  `.meta.json`, `merged.md`, `return-contract.yaml`, plus observability artifacts.
- `.md` frontmatter: `reviewer_model_id: ""`, `reviewer_model_label: ""` (**empty** — the
  inline path does not thread model identity into recipe_args), `caller_label: ""` (empty
  unless `--label`), `elapsed_ms: 0`, `target_checksum: <real 64-char sha256>`,
  `generated: <real wall-clock>`, slug `lens-default-model-0`.
- Default stub body has **0 findings** — `--transport stub` serves a hash body, NOT the
  fixture corpus. There is **no CLI flag** to feed fixtures (`_resolve_dispatch_transport`
  / `_resolve_run_transport` build `StubTransport(model_id=...)` only, `commands.py:548-552,
  652-654`).
- Contract = **NESTED** schema (`emit_contract`/reduce): `job_id, caller:{}, lens,
  target:{path,checksum,truncated,truncation_line_cap}, workers_requested/succeeded/failed,
  output_files:[{index,path,raw_path,meta_path,final_path,model_id,model_label,bytes,status,
  http_code,attempts,elapsed_ms}], amalgamation_mode, merged_path, caller_metadata:{suspect,
  tier}, recommended_next_command, artifacts:{}`.

## Consequences for the gate

1. **Full-contract byte-equality is impossible** (flat legacy schema ≠ nested CLI schema).
   §4.7 invariants 2-5 must be **field extractions** from the CLI's nested contract compared
   to per-scenario EXPECTED values (status, per-slot status set, M/N counts,
   `caller_metadata.suspect==true`, `recommended_next_command` containing
   `/sc:adversarial --suspect-source`). The golden contract is a legacy-schema reference only.
2. **`.md` body byte-equality (§4.7 #1) IS achievable** because `BareReviewV1.normalize`
   is a byte-faithful port of legacy `t2_normalize` (parity-proven), SO legacy(args) ==
   CLI-recipe(args) for identical (raw body, args). Achieved by:
   - Capturing the golden with **CLI-aligned args**: `model_id=""`, `model_label=""`,
     `caller_label=""`, `elapsed_ms=0`, `target_checksum=<real sha256 of the committed
     target fixture>`, `generated=FIXED_GENERATED`, `target=<abs path>`.
   - The gate feeds the fixture corpus to the stub via **monkeypatch** of the transport
     factory → `StubTransport(fixtures=[scenario bodies])` (valid hermetic mechanism; still
     drives the full CLI through `runner.invoke(swarm_group, ["run", ...])`).
   - The gate pins `generated` (monkeypatch the recipe/normalize timestamp source the way
     the legacy gate monkeypatches `iso_now`).
   - **Path normalization sentinel:** the only non-portable body field is `target: "<abs>"`.
     The golden stores it as `target: "<<TARGET>>"`; the gate replaces the CLI body's actual
     resolved target path with `<<TARGET>>` before byte comparison (symmetric → cannot mask a
     real divergence).
3. **Slot mapping:** golden files are 1-based `bare-review-NN-<slug>.md`; CLI files are
   0-based `bare-review-NN-<slug>.final.md`. The gate pairs by **sorted index**, not filename.
4. **Fixture ordering determinism:** `StubTransport(fixtures=...)` serves
   `fixtures[counter % len]` in call order under a lock — the gate must guarantee slot↔fixture
   ordering (single-shared-stub dispatch preserves submission order; if flaky, compare the
   sorted multiset of bodies per scenario). Step 4.3 concern.

## Step 4.1 deliverables
- `tests/swarm/fixtures/bare_review_v1/golden/_review_target.py` — committed fixed target the
  gate passes to `--target` (its sha256 == the golden `target_checksum`).
- `tests/swarm/test_bare_review_golden_regen.py` — env-gated (`SWARM_REGEN_GOLDEN=1`) one-shot
  regen that drives the **real legacy `t2_normalize.py`** with CLI-aligned args + the fixture
  corpus, normalizes the target path → `<<TARGET>>`, and writes the golden tree.
- `tests/swarm/fixtures/bare_review_v1/golden/<scenario>/{bare-review-NN-<slug>.md,
  return-contract.yaml}` for `all-success`, `partial-with-timeout`, `salvage-promoted`.
- `tests/swarm/fixtures/bare_review_v1/golden/README.md` — human-approved-regen discipline +
  the normalization scheme.
