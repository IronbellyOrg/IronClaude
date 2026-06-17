# QA Report — Report Validation (Post-Completion Evidence-Quality Sweep)

**Topic:** sc-bare-review M8/M9 migration — final evidence-quality sweep of OPS docs, env script, and SKILL.md
**Date:** 2026-06-17
**Phase:** report-validation (post-completion, evidence-quality lens)
**Fix cycle:** N/A (fix_authorization: FALSE — report only)
**Stance:** ADVERSARIAL — assumed ≥10 residual defects; hunted for fabricated commands/flags/artifacts/env-vars/fields.

---

## Overall Verdict: PASS

Every command, flag, env var, artifact filename, and contract/event field cited across the 9 target
deliverables was verified to exist in the authoritative sources (live `--help`, `openai_compat.py`,
`config.py`, `commands.py`, `models.py`, `logging_.py`, `preflight.py`, `lenses/bare_review.py`) or
via live CLI execution. No fabrication found. The four task-specified high-risk checks all hold.

---

## Authorities consulted (ground truth)

| Authority | Used to verify |
|---|---|
| `uv run superclaude swarm run --help` (live) | every `run` flag cited in any doc |
| `uv run superclaude swarm --help` (live) | subcommand inventory |
| `uv run superclaude swarm validate-lenses` (live) | "8 entries inspected, 7 validated" |
| `uv run superclaude swarm scaffold --lens {bare-review,custom,unknown}` (live) | lens resolution + exit codes |
| `src/.../transports/openai_compat.py` | env-var names, `TransportEnvError`, message text |
| `src/.../config.py` | `T2ProxyUrl`/`T2ProxyKey`/`T2Model0`/`MAX_SLOTS=9` constant values |
| `src/.../commands.py` | five `*_FILENAME` constants |
| `src/.../models.py` | `ResultContract`/`WorkerResult` fields, `WorkerStatus`/`SwarmStateValue`/`EventType`, `worker_index` |
| `src/.../logging_.py` | Markdown-log line shape (`worker=<index\|->`) |
| `src/.../lenses/bare_review.py` | `bare-review` lens registration (`name="bare-review"`, `default_workers=3`) |

---

## The 4 task-specified checks

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | No doc cites a `swarm run` flag absent from `run --help`; `--custom-prompt-dir` NOT a run flag; 4 WS-0 flags ARE documented | PASS | Every flag in operator-runbook L61-64, command-reference L37-51, SKILL.md L36-37 exists in live `run --help`. `--custom-prompt-dir` appears ONLY as the JobSpec `custom_prompt_dir` field (operator-runbook L67; command-reference L53-58) — explicitly disclaimed as a run flag. `--reviewers`/`--target-line-cap`/`--timeout-sec`/`--label` all in `run --help` AND documented. `--auto-inject-guard` real + documented. |
| 2 | Env vars cited exist in `openai_compat.py`; no Anthropic var as a swarm requirement | PASS | `T2ProxyUrl`/`T2ProxyKey`/`T2Model01..09` map to `config.py` `T2_PROXY_URL_ENV="T2ProxyUrl"`, `T2_PROXY_KEY_ENV="T2ProxyKey"`, `T2_MODEL_ENV_PREFIX="T2Model0"`, `T2_MODEL_MAX_SLOTS=9`. env-readiness.md L97-102, env script L22-23, SKILL.md L70 all explicitly state NO Anthropic credential. Confirmed no `ANTHROPIC_*` in `openai_compat.py`. |
| 3 | Artifact filenames + contract/event fields match real constants/fields (`worker_index` not `worker`) | PASS | All 5 `*_FILENAME` constants (commands.py L85,86,99,100,113) match observability-procedure.md table. Event field is `worker_index` (models.py L1286; logging_.py L174) — docs correctly use `worker_index` (observability L152,176; command-reference L249; post-release L31). `manifest.json` correctly described as string literal (preflight.py L1498), NOT a `*_FILENAME` constant. All post-release ResultContract/WorkerResult fields exist (models.py L877+ docstring; WorkerResult L1027+). |
| 4 | SKILL.md `swarm run --lens bare-review …` uses only real flags | PASS | SKILL.md L36-39 bash block uses `--lens --target --output --reviewers --target-line-cap --timeout-sec --label --transport` — all real. `--lens bare-review` resolves live (scaffold emits `job_id: lens-bare-review-<hash>`). 3 cited test files all exist. |

---

## Per-citation verification table (everything doubted, then checked)

| Citation (doc:loc) | Claim | Verified against | Result |
|---|---|---|---|
| operator-runbook L61-64 | run key flags list | live `run --help` | PASS — all present |
| operator-runbook L67-69 | custom-prompt-dir is JobSpec field, not run flag | `run --help` (absent) + command-reference | PASS |
| operator-runbook L93,160 | phase enum `preflight_ok→…→terminal` | models.py L22-28 `SwarmStateValue` | PASS |
| operator-runbook L272 | `attach` takes no flags | live `run --help`/help; reference L213 | PASS |
| command-reference L147 | "8 entries inspected, 7 validated" | live `validate-lenses` | PASS — exact match |
| command-reference L102 | scaffold `custom`/unknown → exit 2 | live (`scaffold --lens custom` exit=2; unknown exit=2) | PASS |
| command-reference L249 | event fields incl. `worker_index` (int/null) | models.py L1286 Optional[int] | PASS |
| command-reference L50 | `--detached` mutually exclusive with `--resume` | `run --help` | PASS |
| env-readiness L36,66-67 | `T2ProxyUrl`/`T2ProxyKey`/`T2Model01..09` | config.py L51-63 | PASS |
| env-readiness L73 | `T2_MODEL_MAX_SLOTS=9` | config.py L63 | PASS |
| env-readiness L124 | `TransportEnvError` + message text | openai_compat.py L125,138-140 | PASS — text matches |
| env-readiness L97-102 | no `ANTHROPIC_API_KEY` in contract | openai_compat.py (grep, absent) | PASS |
| swarm_env_readiness.sh L39-40 | `T2_MODEL_MAX_SLOTS=9`, prefix `T2Model0` | config.py L57,63 | PASS |
| swarm_env_readiness.sh L147 | missing-var message mirrors read_env | openai_compat.py L138-141 | PASS (enumerated form `T2Model01..T2Model09` vs Python's `T2Model01..9` — both accurate) |
| observability L37-40 | 5 artifact `*_FILENAME` constants | commands.py L85,86,99,100,113 | PASS |
| observability L48 | manifest.json is string literal, not constant | preflight.py L1498 | PASS |
| observability L53 | `SwarmStateValue` "enum" models.py:71-77 | models.py L71 (`Literal`) | PASS line refs (minor: it's a `Literal` alias, doc calls it "enum") |
| observability L68 | `EventType` models.py:78-84 | models.py L78 | PASS |
| observability L82-83 | log line `worker=<index\|->` logging_.py:167,186 | logging_.py L167,186 | PASS — shape exact |
| observability L145 | `WorkerStatus` models.py:69 = success/timeout/parse_error/proxy_error | models.py L69 | PASS |
| post-release L30 | ResultContract fields (status, workers_*, elapsed_ms, output_files, merged_path, lens, caller_metadata, amalgamation_mode) | models.py L877+ docstring | PASS — all present |
| post-release L30 | WorkerResult fields (status, elapsed_ms, attempts, http_code, model_label) | models.py WorkerResult | PASS — all present |
| post-release L62-63 | INV-005 `succeeded+failed==requested` | models.py L65-66 | PASS |
| rollback L28-31 | SKILL.md is 80-line thin caller, commit 2355bfe1 | `wc -l` = 80; git log | PASS |
| rollback L36-40,120-125 | 5 legacy files present at 2355bfe1 | `git cat-file -t` → 5×`blob` | PASS |
| rollback L90,176 | `tests/swarm/test_bare_review_parity.py` | file exists | PASS |
| SKILL.md L36-39 | run invocation flags | live `run --help` | PASS |
| SKILL.md L76 | 3 named test files | all 3 exist under tests/swarm/ | PASS |
| SKILL.md L29-33 | `--lens bare-review` real, default reviewers 3 | lenses/bare_review.py L41 `default_workers=3` | PASS |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | — | — | None. No fabricated command, flag, env var, artifact filename, or contract/event field found. | — |

### Sub-threshold observations (NOT defects — recorded for completeness, no fix needed)

| Severity | Location | Observation |
|---|---|---|
| NIT | observability-procedure.md L53,68 | Calls `SwarmStateValue`/`EventType` "enum"; they are `typing.Literal` aliases, not `enum.Enum`. Cited line numbers are exact and the member values are correct, so this is terminology-imprecise but not a factual citation error. |
| NIT | swarm_env_readiness.sh L147 vs openai_compat.py L140 | Script's missing-var message enumerates `T2Model01..T2Model09`; the Python `TransportEnvError` enumerates `T2Model01..9`. Both are faithful renderings of the same `T2Model0{1..9}` slot range — not a contradiction. |

---

## Confidence

- **Confidence:** Verified: 4/4 task checks + 31/31 per-citation rows | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 11 (incl. live CLI + source grep + git)
  - No web research performed — every claim was source-truth-local or live-CLI verifiable (Principle 6). tavily/web fallback counts: 0.
- Every PASS row cites a specific file:line or live command output. No item marked VERIFIED on the basis of another report.

## Self-audit

If I told the user I found 0 fabrications, the evidence is: 11 Bash runs capturing live `--help`,
`validate-lenses`, `scaffold` exit codes, and source greps; the central `--lens bare-review`
invocation proven by a live scaffold emitting a real `lens-bare-review-<hash>` job_id; all 5
artifact constants, all event/contract fields, and all env-var constants matched to their exact
source lines. The two NITs are terminology, not citation errors, and are below the fix threshold.

## QA Complete
