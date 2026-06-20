# QA Report — Structural OPS Docs Evidence-Quality Lens (Phase Gate 6)

**Topic:** MultiModelSwarm Phase-9 OPS docs — CLI/env/artifact/metrics citation existence verification
**Date:** 2026-06-16
**Phase:** report-validation (evidence-quality lens)
**Fix authorization:** FALSE (report only — no files modified)
**Adversarial stance:** Assumed ≥5 fabricated citations; verified every command/flag/env-var/artifact/metric against source-of-truth.

---

## Overall Verdict: FAIL

**One-line justification:** The designated CLI flag authority (`command-reference.md`) AND `operator-runbook.md` both present `--custom-prompt-dir` as a `swarm run` CLI flag, but it exists on **no** swarm subcommand and is registered as **zero** Click options in the entire swarm package — it is a JobSpec field (`custom_prompt_dir`), not a CLI flag. This is a fabricated CLI citation in the authority file itself, propagated to a second doc.

**Citations checked (raw data tool result): 71** — 36 CLI command/flag tokens (across 8 subcommands, verified vs live `--help` + `commands.py`), 8 env-var tokens (vs `openai_compat.py`/`config.py`), 5 artifact-filename constants (vs `commands.py` `*_FILENAME`), 22 contract/log/enum field references (vs `models.py`/`logging_.py`).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `swarm run` flags (operator-runbook + command-reference) vs live `--help` + `commands.py` | **FAIL** | Live run flags = `--stdin,--lens,--resume,--target,--output,--transport,--reviewers,--target-line-cap,--timeout-sec,--label,--force-relens,--detached,--auto-inject-guard`. `--custom-prompt-dir` is NOT among them (`grep "--custom-prompt-dir"` over `commands.py` = 0 registered options; `swarm run --help` = 0 matches). |
| 2 | `swarm status/logs/attach/kill/scaffold/validate/validate-lenses` flags vs live `--help` | PASS | scaffold `--lens`, validate `--strict`, validate-lenses `--warning-mode`, status `--output/--job/--watch/--watch-interval/--watch-max-iterations`, logs `--output/--job/--jsonl/--md/--follow(-f)/--tail/--lines/--watch-interval/--watch-max-iterations`, kill `--output`, attach (no flags) — all confirmed against live help. |
| 3 | `logs --follow` / `-f` short alias (operator-runbook L143) | PASS | `commands.py:2889-2891` registers `"--follow","-f"`; live help shows `-f, --follow`. |
| 4 | Env vars vs `openai_compat.py` / `config.py` | PASS | `T2ProxyUrl`/`T2ProxyKey` = `T2_PROXY_URL_ENV`/`T2_PROXY_KEY_ENV` (config.py:51-52); `T2Model01..09` = prefix `"T2Model0"` (config.py:57) + index 1..`T2_MODEL_MAX_SLOTS=9` (config.py:63). All doc + script values exact-match. |
| 5 | No Anthropic var presented as swarm requirement | PASS | Every `ANTHROPIC`/`non-Anthropic` mention across all 6 docs + script is an explicit NEGATION (env-readiness L97-99 "no `ANTHROPIC_API_KEY`"; script L22-23). `read_env` reads only T2* (confirmed openai_compat.py:177-202). |
| 6 | `TransportEnvError` message text (env-readiness L126-127) | PASS | Doc quotes "…at least one T2Model01..9 slot." Source renders `f"…one {T2_MODEL_ENV_PREFIX}1..{T2_MODEL_MAX_SLOTS} slot."` = "…one T2Model01..9 slot." (openai_compat.py:134-141). Exact match. |
| 7 | Artifact filenames vs `commands.py` `*_FILENAME` constants | PASS | `.swarm-state.json`=`SWARM_STATE_FILENAME` (:85), `execution-log.jsonl`=`EXECUTION_LOG_JSONL_FILENAME` (:99), `execution-log.md`=`EXECUTION_LOG_MD_FILENAME` (:100), `done.json`=`DONE_SENTINEL_FILENAME` (:113), `return-contract.yaml`=`RESULT_CONTRACT_FILENAME` (:86). observability + rollback + metrics docs all cite these exactly. |
| 8 | Stale `event-log.*` variant NOT used by any OPS doc | PASS | `grep -rE 'event-log\.(jsonl\|md)'` over all 6 docs + script = 0 hits. (Stale `event-log.*` exists only in `logging_.py`/`models.py` docstrings; run_cmd actually writes `execution-log.*` — commands.py:1724-1725. Docs correctly use the emitted name.) |
| 9 | `ResultContract` metric fields (post-release-metrics M1-M7) vs `models.py` | PASS | `status,workers_requested,workers_succeeded,workers_failed,elapsed_ms,output_files,merged_path,lens,amalgamation_mode,caller_metadata` all confirmed ResultContract fields (models.py:996-1014). |
| 10 | Per-worker `WorkerResult` fields (metrics M3/M4) | PASS | `status,elapsed_ms,attempts,http_code,model_label` all confirmed (models.py WorkerResult). |
| 11 | `caller_metadata.suspect` + `tier` (metrics M5) | PASS | `CallerMetadata.suspect: bool`, `tier: str` confirmed (models.py:1634+). |
| 12 | `SwarmStateValue` phase enum (observability L56) | PASS | `preflight_ok,dispatching,normalizing,reducing,terminal` exact (models.py:71-77). |
| 13 | `EventType` enum (observability L71) | PASS | `worker_start,worker_progress,worker_done,wave_transition,terminal` exact (models.py:78-84). |
| 14 | `WorkerStatus` enum (observability L145-146) | PASS | `success,timeout,parse_error,proxy_error` exact (models.py:69). |
| 15 | `DoneSentinel` fields `terminal_status`+`contract_path` (observability L40/90) | PASS | Confirmed (models.py DoneSentinel: `terminal_status:str; contract_path:str`). |
| 16 | Markdown-log line shape (observability L82) | PASS | `- [<timestamp>] <event_type> worker=<index\|->: <payload_summary>` exact-matches logging_.py:167. |
| 17 | EventRecord JSONL field name `worker_index` | **MINOR** | observability uses `worker_index` correctly; post-release-metrics L31 says "`worker` index" — the real field is `worker_index` (models.py EventRecord), `worker` is a loose paraphrase. |
| 18 | command-reference run Options completeness | **MINOR** | Omits 4 real run flags `--reviewers/--target-line-cap/--timeout-sec/--label` (B-1..B-4, present in live help). Incompleteness, not fabrication. |

## Summary
- Checks passed: 14 / 18
- Checks failed: 1 (CRITICAL fabrication)
- Minor accuracy issues: 2
- Citations verified: 71

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | **CRITICAL** | `command-reference.md:48` (and `:47`) | Lists `--custom-prompt-dir DIR` as a `swarm run` Click option, and `--auto-inject-guard` as "Only relevant with `--custom-prompt-dir`". `--custom-prompt-dir` is registered as **0** Click options in the entire swarm package and appears on **0** subcommands' `--help`. It is the JobSpec field `custom_prompt_dir` (read from the spec file at preflight, preflight.py:551), not a CLI flag. Because this is the *authority* doc, the fabrication is load-bearing. | Remove the `--custom-prompt-dir` row. Reword `--auto-inject-guard` to reference the spec-file `custom_prompt_dir` field / `system.txt` reader, not a CLI flag. |
| 2 | **CRITICAL** | `operator-runbook.md:63` | Same fabrication propagated: lists `--custom-prompt-dir` in the run "Key flags" line (`…--detached, --custom-prompt-dir, --auto-inject-guard`). | Drop `--custom-prompt-dir` from the Key-flags enumeration. `--auto-inject-guard` is real; keep it. |
| 3 | MINOR | `command-reference.md:35-48` | run Options table omits the 4 real B-1..B-4 flags `--reviewers`, `--target-line-cap`, `--timeout-sec`, `--label` (all in live `swarm run --help`). | Add the four rows so the authority matches the live surface. |
| 4 | MINOR | `post-release-metrics.md:31` | EventRecord field described as "`worker` index"; the actual field is `worker_index`. | Rename to `worker_index` to match the JSONL field operators will `jq`. |

## Per-citation existence table (the doubted items)

| Cited token | Doc(s) | Exists? | Source-of-truth check |
|---|---|---|---|
| `swarm run --custom-prompt-dir` | command-reference:48, operator-runbook:63 | **NO** | 0 Click options in swarm pkg; 0 in `run --help` |
| `swarm run --auto-inject-guard` | command-reference:47, operator-runbook:63 | YES | commands.py:154 `auto_inject_guard_option`; live help |
| `logs -f` (alias of `--follow`) | operator-runbook:143 | YES | commands.py:2889-2891 `"--follow","-f"` |
| `run --reviewers/--target-line-cap/--timeout-sec/--label` | live help only (NOT in command-reference table) | YES (flags exist) | `swarm run --help` B-1..B-4; command-reference omits |
| `T2ProxyUrl`/`T2ProxyKey`/`T2Model01..09` | env-readiness, script | YES | config.py:51-52,57,63; openai_compat.read_env |
| `ANTHROPIC_API_KEY` as requirement | (negated only) | N/A (correctly absent) | read_env reads no Anthropic var |
| `execution-log.jsonl`/`.md` | observability, rollback, metrics | YES | commands.py:99-100 + run_cmd:1724-1725 (emitted) |
| `event-log.*` (stale) | none | not cited | docs correctly avoid the stale variant |
| `.swarm-state.json`/`done.json`/`return-contract.yaml` | observability, rollback, metrics | YES | commands.py:85,113,86 |
| `caller_metadata.suspect`/`tier` | metrics M5 | YES | models.py CallerMetadata:1634+ |
| EventRecord `worker_index` | observability (ok) / metrics ("worker", loose) | field=YES | models.py EventRecord |

## Recommendations
- **Blocker:** Resolve issues #1 and #2 before this OPS-doc set can pass Phase Gate 6. A fabricated flag in the *authority* doc means operators who paste `swarm run … --custom-prompt-dir <dir>` will hit a Click "no such option" error. Both fixes are 1-2 line edits; recommend a single corrective pass on `command-reference.md` + `operator-runbook.md`.
- Address minors #3/#4 in the same pass (cheap, improves authority fidelity).
- env-readiness.md, the env script, observability-procedure.md, rollback-procedure.md, and post-release-metrics.md (apart from the one minor field-name slip) are evidence-clean and source-grounded.

## Confidence
**Verified:** 18/18 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence: 100.0%**

## Tool engagement
Read: 7 | Grep/Bash-grep: 14 | Glob: 0 | Bash(uv run --help): 9 (each call mapped to a specific subcommand's flag-surface verification or a specific source-constant check; no padding)

## QA Complete
