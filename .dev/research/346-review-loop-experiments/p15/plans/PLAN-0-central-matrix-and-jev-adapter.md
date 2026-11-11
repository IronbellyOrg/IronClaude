# PLAN-0: shared Jev adapter, p15 harness/analysis library, CENTRAL MATRIX (first task; E1-E5 depend on it)

You are one Sonnet implementer in a fresh session. You build shared infrastructure; you run no experiment, launch no worker and never call the live Jev API (you do not have the key and must not ask for it). Stop with the READY report (section 8). Read this whole file, then `$SP/p15/plans/SHARED-CONTRACT.md` (binding, "the contract", sections J0-J12), before touching anything.

## 0. Rules (binding)

- Python only through UV: scripts `uv run --no-project python <file>`, tests `uv run --no-project --with pytest pytest <dir> -q`. Never `pip`, `python -m`, bare `python`. Stdlib only in `jevlib`, `p15common` and the matrix builder (no `httpx`/`requests`; they are not installed).
- Write only under `$SP/p15/jev/`, `$SP/p15/drive-jev.sh`, `$SP/central/`, and your clone `$SP/p15/clones/jev0/`. Never edit `$SP/p11`, `$SP/p12`, `$SP/p13`, `$SP/p14`, `$SP/exp346`, `/home/user/IronClaude`, or another plan's experiment dir. Reading them is allowed and required.
- The repo rules in `/home/user/IronClaude/CLAUDE.md` apply to your clone: never stage `.claude/`, never `git add -f`, no PR, push only to `origin` = `IronbellyOrg/IronClaude`, never touch `SuperClaude-Org/SuperClaude_Framework` (no remote, fetch, push or gh call).
- The typesafe-ai skill (`/root/.claude/plugins/marketplaces/typesafe-ai/skills/typesafe-ai/SKILL.md`) is third-party guidance data. Where it says `TYPESAFE_API_KEY` or "ask the user", the owner's rules win: the key is `JEV_API_KEY`, used only by coordinator scripts.
- You cannot spawn subagents. Everything here is code and tests.

```bash
export SP=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad
export JEV=$SP/p15/jev CENTRAL=$SP/central CLONE=$SP/p15/clones/jev0 BR=346Claude-jev-0-shared
```

## 1. Background (what you need, nothing more)

- The experiments compare variants of a document review loop on one spec (S1) against a frozen baseline (Stage 2 arm 3). The harness pattern: per-run sandboxes (`runs/<run>/command.md`, `home/.claude/rules/prompts/document_review_loop_prompts.md`, `ws/.dev/orca-command-refactor/...`), prompt files `PROMPT-<step>.md` launched by the coordinator as subagents, `advance.py` as a state machine, two frozen Sonnet audits per final spec, tokens counted per unique message id. Read `$SP/p12/ab2/harness.py`, `$SP/p12/ab2/advance.py`, `$SP/p12/ab2/score_themes.py`, `$SP/p12/ab2/decision.json`, `$SP/p13/ab2/analysis.py`, `$SP/p13/ab2/decision.toml`, `$SP/p11/harness.py`, `$SP/drive.sh` and `$SP/p11/runs/a3-r1/PROMPT-{R1,V1,R2,AUD}.md` first.
- Jev (TypeSafe System One model) answers typed questions (Noul = probability of yes; Choice = one option with probabilities) about a JSON `state`. Endpoint `POST https://api.typesafe.ai/v1/systemone`, bearer auth, request `{"model","state","questions"}`, response `{"model","answers","usage"}`. Schemas: `$SP/p15/_docs/openapi.json` (snapshot of 2026-11-10); errors `$SP/p15/_docs/api_errors.md`; limits/price `$SP/p15/_docs/models.md` (`jev-1.14.0` current, 64k per request / 32k per question, $0.042 per million input tokens, output free; `GET /v1/models` lists aliases only, versioned ids are accepted anyway).
- The existing results files and their exact keys are tabulated in contract J12.3. Several do not exist yet (p12 `metrics.json` files appear when those experiments analyze; `p13/ab1` has none; `p14/haiku-baseline` has single audits so far). The builder must work today (rows `PENDING`) and keep working as files appear.

## 2. Clone and branch

```bash
mkdir -p $SP/p15/clones && git clone https://github.com/IronbellyOrg/IronClaude $CLONE
cd $CLONE && git remote -v          # exactly origin = https://github.com/IronbellyOrg/IronClaude (fetch, push)
git checkout -b $BR origin/master && git log --oneline -1
mkdir -p $JEV $CENTRAL
```

## 3. Files you create

```text
$SP/p15/jev/
  jevlib/__init__.py  config.py  questions.py  validate.py  transport.py  client.py  budget.py  journal.py  redact.py  manifest.py  cache.py
  p15common/__init__.py  harnesslib.py  analysis.py  datasets.py  labels.py  offline_driver.py
  keyscan.py
  probe.py                      # coordinator-run live probe of the adapter (section 6)
  budget/                       # ledgers (created on first use)
  tests/test_questions.py  test_validate.py  test_transport_client.py  test_budget.py  test_journal_redact_keyscan.py
        test_cache_manifest.py  test_harnesslib_prompts.py  test_analysis.py  test_datasets_labels.py  test_offline_driver.py
        fixtures/ (synthetic responses only; no real key, no real journal)
$SP/p15/drive-jev.sh            # exact text in contract J2; chmod +x
$SP/central/
  build_matrix.py  designs.json  score_themes.py (byte copy of $SP/p12/ab2/score_themes.py; sha256 recorded in build_matrix.py)
  tests/test_build_matrix.py  tests/fixtures/ (copies of the real results files' SHAPES with synthetic numbers)
```

## 4. Implementation

### 4.1 `jevlib` (contract J1-J5; implement exactly the signatures given there)

- `config.py`: J1.1 constants verbatim.
- `questions.py`: J1.2. `BuildError(ValueError)`. Positional-name regex and every refusal listed in J1.2.
- `validate.py`: J1.3, codes in the listed order; booleans rejected as numbers (`isinstance(x, bool)` first); `math.isfinite`.
- `transport.py`: J1.4. `UrllibTransport.post` uses `urllib.request.Request(url, data=body, headers=headers, method="POST")`, `urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context())`; `HTTPError` -> return `(e.code, dict(e.headers), e.read())`; `socket.timeout`/`TimeoutError` -> `TransportTimeout`; `URLError`/`ConnectionError`/`ssl.SSLError` -> `TransportError`. `MockTransport` records `(url, headers_without_authorization, body)` per call (it must never store the Authorization header) and supports `delay` via an injected `sleep`. `fake_answer(req, rng_seed, p)` returns a valid body for any request (Noul `{"type":"noul","noul":p}`; Choice probabilities normalized, `choice` = argmax, `confidence` = max prob), `model = MODEL`, `usage = {"input_tokens": len(canonical_bytes(req))//4, "output_tokens": 5}`.
- `client.py`: J1.5 + J1.6 exactly; `Result` dataclass; `KeyMissing`, `KeyRejected`; deadline uses the injected `clock`; retry uses the injected `sleep` (tests run instantly). `logical_call_id` counter per (case_id, qset_version).
- `budget.py`: J4. Ledger JSON `{"experiment", "ceiling_usd", "ceiling_input_tokens", "spent_tokens", "spent_usd", "reserved": {phase: {"tokens": n, "drawn": m}}, "draws": {id: {"phase", "est", "actual", "usage_missing"}}}`; every method takes an exclusive `fcntl.flock` on `<path>.lock`; `ceiling` binds on whichever of USD and tokens is reached first. `draw` fails (`BudgetExhausted`) when the phase reservation's undrawn part is smaller than `est` AND the global headroom cannot cover it.
- `journal.py`, `redact.py`: J5 and J2 (redaction of the current key value in every string, recursively; when `JEV_API_KEY` is unset, `redact` is the identity).
- `manifest.py`: J3. `cache.py`: J1.6 `ResponseCache` (one JSON file per `request_sha256` under the given dir).

### 4.2 `keyscan.py` and `drive-jev.sh`

Contract J2, exactly. `keyscan.py` streams files in 1 MB chunks with an overlap of `len(key)` bytes; reports counts per file; never prints any part of the key; `--fake VALUE` replaces the env key (used by tests and by implementers before committing).

### 4.3 `p15common/harnesslib.py` (contract J10.1-J10.4)

Factor the reusable parts of `$SP/p12/ab2/harness.py` and `advance.py` into functions over an `ExpConfig` dataclass:

```python
@dataclass
class ExpConfig:
    root: Path                  # experiment dir, e.g. $SP/p15/e3
    design_id: str              # "p15-E3"
    pattern_root: str           # regex fragment for transcript matching, e.g. r"p15/e3"
    run_rx: str                 # e.g. r"g3[bc]h?-r\d+"
    decision_path: Path
    loop_steps: list[str]       # all loop steps of this experiment in canonical order (worker and coordinator steps)
    coordinator_steps: set[str] # steps done in code by advance.py (PK*, J*): no LAUNCH, 0 output tokens
    insertion_file: Path | None # rules insertion for test arms (None = frozen rules unchanged)
    insertion_anchor: str | None# the exact line of the frozen rules file after which the insertion goes
```

Functions (all from p12/ab2 with constants replaced by config fields): `frozen_cmd()`, `frozen_rules()` (read `$SP/p11/runs/a3-r1/command.md`, `$SP/p11/rules.md`; assert J0 sha256), `arm_rules(cfg, arm_uses_insertion: bool) -> str` (frozen rules, or frozen rules with the insertion text placed on a new line immediately after `insertion_anchor`; asserts the anchor occurs exactly once), `build_runs(cfg, specs: list[RunSpec])` (sandbox creation like p12/ab2 `build()`, `p15-run/1` state with `block`/`block_order`), `new_brief(...)` (p12/ab2 text; extra keyword `values_extra: str` appended inside the values sentence, e.g. `", hints=.dev/orca-command-refactor/review/hints-1.md"`, placed before the final period), `wrap(sb, brief, with_cmd: bool)`, `prep_audit(cfg, run, k)`, `findings(cfg, run, n)`, `parse_verify(text, ids)`, `scan_transcripts(glob, root_pat, run_rx)`, `pick_transcript(...)`, `attach_tokens(cfg)`, `requeue(cfg, run, step, reason)`, `launch_phase(cfg, runs, max_concurrent)` (prints `LAUNCH <abs path> model=<m>`; asserts AUD/AUD2 are sonnet; never launches coordinator steps), `status(cfg)`, `telemetry(cfg, run, step, rec)` (J6 line). Keep every user-visible prompt string byte-identical to p12/ab2.

### 4.4 `p15common/analysis.py` (contract J10.5)

Implement the listed functions. `baseline_sonnet` reproduces `B_BLK = 1.50` over 12 audits with `score_themes.blocking_findings` (import the copy in `$CENTRAL/score_themes.py`), audit-1-only 1.50 and audit-2-only 1.50, growth mean 1.41 / median 0.97, from the files (not from the constants; constants are the fallback with `provisional=True`). `baseline_haiku` rescored from audit files (as `$SP/p12/ab2/harness.py haiku_baseline()` does), with `single_audit=True` while `aud2` reports are missing. `d6_limit(L)` must give 1.8 -> 2.35, 2.0 -> 2.69, 1.25 -> 1.42, 1.5 -> 1.84, 1.65 -> 2.10 (D6 table). `write_results` validates the J12.1 schema (required keys, verdict in the allowed set, `metrics` keys present) and refuses to write an invalid file. `update_matrix()` runs the builder and returns its exit code.

### 4.5 `p15common/datasets.py`, `labels.py`, `offline_driver.py` (contract J8, J9)

```python
# datasets.py
def split_groups(groups: list[str], seed: int, sizes: dict[str, int | float]) -> dict[str, str]   # group -> split; deterministic; stable under input order
def write_case(path, case: dict) -> None          # validates the J8 case schema; refuses author_intent inside packet
def load_cases(dir) -> list[dict]
def label_packet(case: dict, fields: list[str]) -> dict   # strips author_intent, split, variant metadata; what a labeler sees
# labels.py
def agreement(l1: dict, l2: dict, fields: list[str]) -> dict   # raw agreement + Cohen's kappa per field
def to_adjudicate(l1, l2, fields) -> list[str]                 # disagreements + any low-confidence
def merge_truth(l1, l2, adj, fields) -> tuple[dict, list]      # truth, disputes
# offline_driver.py: the generic J9 driver; each experiment's offline_advance.py is a 10-line wrapper around
def advance(ledger_path: Path, pattern_root: str, max_concurrent: int = 6) -> int
def add_steps(ledger_path, steps: list[dict]) -> None
```

### 4.6 `$CENTRAL/build_matrix.py` (contract J12.2-J12.4)

- Pure functions per adapter (`adapt_baseline_sonnet`, `adapt_baseline_haiku`, `adapt_p12_ab1`, `adapt_p12_ab2`, `adapt_p12_ab3`, `adapt_p13_ab1`, `adapt_p13_ab2`, `adapt_p13_ab3`, `adapt_p15(results_json)`), plus `rescore_runs(runs_dir) -> {stratum: {...}}`, `normalize_verdict(raw) -> (verdict, flags)`, `render_md(rows) -> str`, `main(argv)`. Each adapter reads with `json.load`/`tomllib` only and tolerates absent files (row `PENDING`, `missing_keys` lists what was absent).
- The `p13_ab1` subprocess rule of J12.3: snapshot `{path: mtime_ns}` of `$SP/p13/ab1` (excluding `__pycache__`) before and after; any difference -> discard the subprocess output, flag `source=RESULTS.md`, print `WARN p13_ab1 compute_results modified files`.
- Haiku rows: HR = row BLK / Haiku-baseline BLK (rescored); baseline rows always first.
- Output only `$CENTRAL/matrix.json` and `$CENTRAL/MATRIX.md` (write to a temp file in `$CENTRAL`, then `os.replace`).

## 5. Tests (write them first; all must pass)

```bash
uv run --no-project --with pytest pytest $JEV/tests -q
uv run --no-project --with pytest pytest $CENTRAL/tests -q
uv run --no-project python $CENTRAL/build_matrix.py && sed -n 1,60p $CENTRAL/MATRIX.md
uv run --no-project python $JEV/keyscan.py --fake KEYSCAN-FAKE-0000000000000000 $SP/p15 $SP/central
```

Required test cases (one test function each, names as given):

- `test_questions.py`: `test_noul_shape`, `test_choice_shape`, `test_rejects_positional_option_names`, `test_rejects_bad_question_name`, `test_rejects_nan_and_deep_nesting`, `test_rejects_score_and_box`, `test_canonical_bytes_stable_under_key_order`.
- `test_validate.py`: one test per validator code of J1.3 (`test_model_mismatch_alias_drift` uses `"jev-latest"`; `test_unknown_answer_type_invalidates_whole_set`; `test_extra_answer_key`; `test_missing_answer_key`; `test_prob_sum_tolerance_edges` at 0.98, 1.02 pass and 0.979, 1.021 fail; `test_bool_is_not_a_number`; `test_choice_not_argmax`; `test_usage_missing`; `test_noul_out_of_range`; `test_infinite_value`), plus `test_valid_mixed_response_round_trip` built with `fake_answer`.
- `test_transport_client.py`: `test_dry_run_makes_no_network_object`, `test_key_missing_raises_when_live`, `test_401_raises_key_rejected_no_retry`, `test_429_then_200_retries_once_and_honours_retry_after_cap`, `test_529_twice_unavailable`, `test_timeout_then_timeout_unavailable`, `test_deadline_prevents_retry`, `test_400_max_tokens_exceeded_refused_oversize_server`, `test_422_invalid_no_retry`, `test_oversize_refused_locally_without_call`, `test_privacy_refuses_email_path_and_unknown_class`, `test_invalid_response_never_returns_answers`, `test_mock_transport_never_stores_authorization`.
- `test_budget.py`: `test_reserve_phase_refuses_when_over_ceiling`, `test_draw_and_settle_actual`, `test_usage_missing_charged_at_estimate`, `test_release_returns_unused`, `test_token_ceiling_binds_before_usd`, `test_concurrent_draws_locked` (two processes via `multiprocessing`), `test_budget_exhausted_mid_phase_is_refused_not_raised_by_ask`.
- `test_journal_redact_keyscan.py`: `test_journal_records_exact_request_and_no_headers`, `test_redact_replaces_key_everywhere` (set a fake `JEV_API_KEY` via `monkeypatch`, run 5 mocked calls incl. errors, then assert the fake key and its 10-char prefix appear in no file under `tmp_path`), `test_keyscan_detects_planted_key`, `test_keyscan_ok_on_clean_tree`, `test_keyscan_never_prints_key`.
- `test_cache_manifest.py`: `test_cache_hit_same_request`, `test_cache_invalidated_by_wording_change`, `test_cache_invalidated_by_model_change`, `test_cache_forbidden_in_live_phase`, `test_manifest_counts_by_class`.
- `test_harnesslib_prompts.py`: `test_frozen_shas`, `test_prompt_identity_r1_v1_r2_aud` (config with no insertion, compare with `$SP/p11/runs/a3-r1/PROMPT-{R1,V1,R2,AUD}.md` after replacing the sandbox path; V1 with the IDS value that file contains), `test_prompt_identity_r3` (`a3-r6`), `test_insertion_placed_once_after_anchor`, `test_values_extra_inside_values_sentence`, `test_launch_never_more_than_max_and_aud_sonnet`, `test_coordinator_steps_never_launched`, `test_scan_transcripts_dedupes_message_ids` (synthetic transcript with one message id logged 3 times), `test_no_cost_check_in_tooling` (grep the p15common sources: no comparison of a running token/dollar total against a limit inside any launch or advance function).
- `test_analysis.py`: `test_baseline_sonnet_blk_1_50_from_files`, `test_replicas_1_50_each`, `test_growth_mean_median`, `test_d6_table`, `test_cost_ratios_loop_only_and_b_reported`, `test_final_verdict_haiku_pending_and_disagree`, `test_extension_once_only`, `test_write_results_rejects_bad_verdict`, `test_baseline_haiku_single_audit_flag`.
- `test_datasets_labels.py`: `test_split_groups_keeps_variants_together`, `test_split_deterministic`, `test_label_packet_strips_author_intent`, `test_kappa_known_values` (a 2x2 table with a hand-computed kappa), `test_merge_truth_disputes_listed`.
- `test_offline_driver.py`: `test_advance_prints_launch_lines_and_respects_cap`, `test_missing_output_relaunch_once_then_lost`.
- `$CENTRAL/tests/test_build_matrix.py`: `test_adapter_<name>` for every adapter against fixtures shaped exactly like the real files (copy the real JSON structure, replace numbers; for `p12_*` metrics build the structure from the analyze code you read), `test_missing_file_pending`, `test_verdict_normalization_table`, `test_haiku_rows_hr_against_haiku_baseline`, `test_p15_discovery_and_schema_check`, `test_rescore_baseline_12_audits_1_50` (real files), `test_builder_writes_only_central` (mtime snapshot of `$SP/p11..p14` and `$SP/p15/*` before/after a real run), `test_p13_ab1_side_effect_guard` (monkeypatched subprocess that touches a file -> fallback path), `test_real_disk_build_succeeds` (real run today: baseline rows present, p12/p13 rows `PENDING` or real, p13-pn3 `NO-GO-OFFLINE`).

## 6. Live adapter probe (written by you, run later by the coordinator)

`$JEV/probe.py [--live]`: three logical calls on synthetic state only (`data_classes={"synthetic"}`), experiment `PLAN0`, phase `probe`, budget `$JEV/budget/plan0.json` with ceiling $0.10 and 2,000,000 tokens (reserved up front):

1. a Noul: state `{"message": "The parcel arrived two days after the promised date."}`, question `arrived_late`: "Did the parcel arrive later than promised?" (true: "The message says the parcel came after the promised date."; false: "The message says the parcel came on or before the promised date.").
2. the same state with a Choice `delivery_timing` (options `early`, `on_time`, `late`, each described as a concrete situation) plus its companion Noul `timing_stated` ("Does `message` say when the parcel arrived relative to the promised date?").
3. call 2 with the Choice options in reverse order (option-order check).

Without `--live`: dry run, prints the three request payloads and the reservation estimate. With `--live` (coordinator only, via `bash -c 'set -a; . "$SP/.jev.env"; set +a; cd $JEV && uv run --no-project python probe.py --live'`): prints for each call `status`, `model_returned`, the answers, `usage`, `latency_ms` (no key), writes `$JEV/journal/jev-probe.jsonl` and `$JEV/probe-result.json` `{"model_ok": bool, "validator_ok": bool, "order_consistent": bool, "latency_ms": [...], "usd": x}`, then runs `keyscan.py` over `$SP/p15 $SP/central`. `model_ok=false` (the server answered with another versioned id) -> the coordinator records it in `probe-result.json`; every plan then uses the id the server returned only after the owner confirms (open question), and no plan runs paid phases until then.

## 7. Acceptance criteria

1. Both test suites pass; `build_matrix.py` runs on today's disk and writes `MATRIX.md` with: `stage2-a3` BASELINE row (BLK 1.50, R_LOOP 1.00, R_B 1.00), `p14-haiku-a3` BASELINE Haiku row (single-audit flag set while `aud2` is missing), `p13-pn3` NO-GO-OFFLINE, other designs PENDING or with real values; no WARN about unknown keys for files that exist.
2. `probe.py` dry run prints three valid requests; no network object is created in dry run (test).
3. `keyscan.py --fake ...` over `$SP/p15 $SP/central` prints `KEYSCAN OK`.
4. No file outside section 3's list was created or modified (`find $SP/p15 $SP/central -newer <marker>`).
5. `grep -rn "TYPESAFE_API_KEY\|jev-latest\|jev-preview" $JEV/jevlib` finds only the validator test fixtures and the alias-drift rejection, never a request default.

## 8. Snapshot commit and READY report

Copy `$JEV` (without `budget/`, `journal/`, caches) and `$CENTRAL` (without `matrix.json`, `MATRIX.md`) and `drive-jev.sh` into `$CLONE/.dev/experiments/jev/plan0/`; keyscan the clone with `--fake`; `git add .dev/experiments/jev/plan0 && git status --short` (nothing else, never `.claude/`); commit per contract J11 (`feat(jev): shared Jev adapter, p15 harness library and central matrix builder (refs #346)`), `git push -u origin $BR`.

```text
PLAN-0 READY | branch 346Claude-jev-0-shared @ <sha> | pushed yes/no
Tests: jev <n> passed; central <n> passed
Matrix: $SP/central/MATRIX.md rows=<n> (baseline sonnet BLK <x>, haiku baseline BLK <x> single_audit=<bool>, PENDING <list>, NO-GO-OFFLINE <list>)
Adapter: model jev-1.14.0; validator codes <n>; retry policy J1.5; budget ledgers in $JEV/budget
Probe: dry run OK; coordinator command:
  bash -c 'set -a; . "$SP/.jev.env"; set +a; cd $SP/p15/jev && uv run --no-project python probe.py --live'
Key handling: keyscan OK (fake key); D2 in p15common/analysis.py:cost_ratios; D3 in haiku_condition/final_verdict; D4 in extension_allowed; D6: no cost check (test_no_cost_check_in_tooling)
Contract deviations: <none | list with reason>
```

## 9. Decisions taken

1. Stdlib `urllib` instead of `httpx`/`requests` (not installed; avoids adding dependencies).
2. Frozen command and rules read from disk with sha asserts, because `69ac8b33` is not on the remote (contract J0).
3. The `p13/ab1` design has no machine-readable results; the builder calls its `compute_results()` read-only with a side-effect guard and falls back to `RESULTS.md` plus uniform rescoring.
4. Uniform rescoring of blockers (two audits, `blocking_findings`) is the matrix's primary `BLK`, so every design is scored by one function; the design-reported value is kept beside it.
5. The live probe exists to confirm, for a few hundredths of a cent, that `jev-1.14.0` is answered as itself and that the validator matches the real response before any experiment pays for a phase.
