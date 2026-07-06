# Swarm CLI — Verified Ground Truth (for docs + E2E)

Captured 2026-06-09 against live `.venv/bin/superclaude` (editable reinstall) + source reads.
This is the authoritative basis for `docs/swarm/` docs and `tests/swarm/` E2E.

## Invocation
- Works: `uv run superclaude swarm ...` and `/config/workspace/IronClaude/.venv/bin/superclaude swarm ...`
- The `VIRTUAL_ENV=/lsiopy` warning line is benign noise; filter with `grep -v VIRTUAL_ENV`.
- Env was broken on resume (stale `site-packages/superclaude/{_plugins,_src}` shadow + empty editable .pth);
  fixed via `rm -rf` of the shadow + `uv pip install -e ".[dev]"`.

## Command surface (8 subcommands)
attach, kill, logs, run, scaffold, status, validate, validate-lenses
Wired: `swarm_group.add_command(...)` in `cli/swarm/__init__.py:172-179`; `main.add_command(swarm_group,...)` `cli/main.py:430`.

## EXIT-CODE + ARTIFACT MATRIX (E2E assertion spec)
| Flow | Exit | Output / artifacts |
|---|---|---|
| scaffold --lens X (stdout) | 0 | valid JSON spec (~2768 bytes for bare-review) |
| scaffold --lens X --output F | 0 | "swarm scaffold: wrote starter spec for lens 'X' to F" |
| scaffold --lens custom | 2 | rejected (no registry defaults) |
| validate (good spec) | 0 | "validate: <path> OK" on stdout |
| validate (missing file) | 2 | usage error |
| validate (malformed json) | 2 | usage error |
| validate (schema-invalid spec) | 1 | structured per-rule diagnostic on stderr |
| validate-lenses | 0 | "validate-lenses: registry OK (8 entries inspected, 7 validated)" |
| run --lens X --target T --output O --transport stub | 0 | "swarm run: dispatched job (mode=lens, workers=N, results=N)"; 4 artifacts; state=terminal |
| run SPEC --output O --transport stub | 0 | "...(mode=spec-file, workers=N, results=N)" |
| run --lens X --transport openai_compat (env unset) | 1 | LIVE-VERIFIED. stderr: "swarm run: cannot construct 'openai_compat' transport -- T2 proxy env contract incomplete; missing: T2ProxyUrl, T2ProxyKey, T2Model01..9. ..."; writes manifest.json + .swarm-state.json ONLY; NO return-contract.yaml, NO execution-log (fails before Wave 1). NOTE: corrects research claim — CLI --lens route does NOT hit emit_env_missing_contract; it fails at transport construction. |
| run SPEC (no --output) | 0 | dispatched, but NO on-disk artifacts (observability keys off --output FLAG, not spec.output.dir) |
| run --target tiny (<50 nonws bytes) | 1 | "swarm run: preflight FAILED (1 rule(s))" + "imm4.target_too_small"; output dir NOT created |
| run --lens nope (unknown) | 2 | usage error |
| status --output O (terminal) | 0 | "status: phase=terminal job_id=... updated=..." |
| status --output O (non-terminal) | 0 | phase=<phase> |
| status --output O (terminal+partial/failed) | 1 | per docstring (needs return-contract.yaml present) |
| status --output nodir (missing) | 2 | usage error |
| logs --output O (md) | 0 | dumps execution-log.md |
| logs --output O --jsonl | 0 | dumps execution-log.jsonl |

## Artifacts after a successful stub run (--output given)
PRODUCED (4): execution-log.jsonl, execution-log.md, manifest.json, .swarm-state.json (state=terminal)
NOT produced today: merged.md, return-contract.yaml, done.json, per-worker *.md, *.meta.json

## CRITICAL ACCURACY CORRECTIONS (do not get these wrong in docs)
1. `swarm run` is DISPATCH-ONLY today (Wave 0 preflight + Wave 1 dispatch). The M5 ResultContract
   writer (merged.md + return-contract.yaml via Wave 2/3 reduce) is PENDING. run docstring says so:
   commands.py:1454 "M5 replaces this with the full ResultContract writer". Do NOT claim a normal run
   emits merged.md/return-contract.yaml/done.json.
2. The `--output` FLAG (not spec.output.dir) wires observability artifacts. spec-file run without
   --output produces no on-disk artifacts.
3. On-disk log filenames are execution-log.jsonl / execution-log.md (what the run path writes and what
   `swarm logs` reads). The logging_ module's internal default constant is event-log.* but the run path
   uses execution-log.* — document execution-log.* (live-observed + what logs reads).
4. Lens validator runs 6 assertions (file_ref, recipe_registered, suspect_coupling, name_unique,
   injection_substring, normalizer_strategy). Docstrings/`validate-lenses --help` still say "five" —
   T02.21 added the 6th. Registry = 8 entries; 7 validated (custom skipped).
5. schema.py (used by `swarm validate`) has NO IMM-4 target-size rule. IMM-4 (>=50 nonws bytes),
   INV-005, INV-007 live in preflight.py. So `validate` passes a spec whose target is too small;
   `run` preflight is what rejects it (exit 1).
6. return-contract.yaml is currently written ONLY by preflight INV-007 env-missing path
   (preflight.py:987-1051), status="failed", reason="env-missing".
7. done.json terminal sentinel is described in monitoring-patterns.md but is NOT emitted by the current
   dispatch-only run path. Document it as the intended terminal marker; flag that current runs don't emit it.
8. SwarmState values: preflight_ok, dispatching, normalizing, reducing, terminal (models.py:72-77).
   "dispatched" appears only as a wave_transition payload label, NOT a state value.

## Lenses (7 validated + custom). All default_target_line_cap=4000.
| Lens | workers | recipe | stability | tier | suspect | next-command |
|---|---|---|---|---|---|---|
| bare-review | 3 | bare-review-v1 | stable | T2 | TRUE | /sc:adversarial --compare {compare_files} --suspect-source {suspect_files} |
| refactor-find | 3 | findings_table_v1 | experimental | T2-code | false | /sc:code-review --apply {compare_files} |
| edge-case-hunt | 4 | findings_table_v1 | experimental | T2-edge | false | /sc:adversarial --compare {compare_files} |
| spec-completeness | 3 | verdict_only_v1 | experimental | T2-spec | false | /sc:reflect --merge {compare_files} |
| feasibility-probe | 3 | verdict_only_v1 | experimental | T2-feas | false | /sc:research --extend {compare_files} |
| troubleshoot-hypothesis | 4 | hypothesis_table_v1 | experimental | T2-tshoot | false | /sc:troubleshoot --merge-hypotheses {compare_files} |
| doc-completeness | 3 | findings_table_v1 | experimental | T2-doc | false | /sc:document --apply {compare_files} |

## Recipes (6) — all normalize-only, none judge/score/dedup/reorder (AC-011)
- bare-review-v1: findings table | ID | Sev | Claim | Cite | SelfConf | + Verdict + Notes
- findings_table_v1: | ID | Locator | Finding | Detail | Action | (shared: refactor-find, edge-case-hunt, doc-completeness)
- hypothesis_table_v1: | ID | Cause | Evidence | Confidence | Next Step |
- verdict_only_v1: ## Verdict (yes/no/uncertain) + ## Rationale + ## Notes (shared: spec-completeness, feasibility-probe)
- passthrough: byte-for-byte raw (raw amalgamation mode)
- custom: custom-py:<module>:<callable> dynamic loader; dispatcher.normalize() raises if called directly

## Transports
- stub: in-process, no network. body = f"stub:{model_id}:{sha256(prompt)[:16]}\n". Always success/200/attempts=1.
  Safe quick-dispatch; default for `--lens`/scaffold. Use in CI/tests/docs.
- openai_compat: httpx -> <base_url>/chat/completions, payload {model,messages,temperature},
  Authorization: Bearer. Status map: success/parse_error/proxy_error/timeout. Real T2 proxy.
- Phase-1 EXCLUDED: streaming, function-calling/tools, vision.

## Env contract (T2 proxy) — config.py:51-63
- T2ProxyUrl (base URL), T2ProxyKey (bearer)
- Per-slot models: T2Model01 .. T2Model09 (prefix "T2Model0" + 1-based idx; max 9 slots)
- Missing -> INV-007: empty pool -> RULE "inv007.env_missing", reason="env-missing";
  if output.dir creatable, writes return-contract.yaml (status=failed). Else bare abort.

## Retry policy (dispatch.py) defaults
on_5xx=True (retry once), on_5xx_backoff_sec=2, on_4xx=False, on_timeout=False. Network/other (http=None) never retried.

## IMM-4 target floor
>=50 non-whitespace bytes AFTER truncation; else "imm4.target_too_small @ target.path ... STOP before dispatch" (exit 1).

## Detached / tmux (tmux.py)
- --detached -> tmux new-session -d -s swarm-<job_id>. Refuses if session exists; errors if tmux absent (exit 2, no silent inline fallback).
- attach JOB_ID -> tmux attach-session -t swarm-<job_id> (graceful no-op if no session).
- kill JOB_ID [--output O] -> tmux kill-session; --output flips state=terminal + writes done.json terminal_status=killed. Idempotent.
- is_tmux_available: which(tmux) AND not nested (TMUX unset).
