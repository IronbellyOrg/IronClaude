# QA Report — Research Gate (Evidence-Quality Lens, Partition A)

**Topic:** FR-RH2 Headless Ensemble Fix — research evidence verification
**Date:** 2026-06-20
**Phase:** research-gate (evidence-quality lens)
**Fix cycle:** N/A (fix_authorization: false — report-only)
**Assigned files (Partition A):** `00-prd-extraction.md`, `01-reflect-runner-seam.md`, `02-reflect-contract-verdict.md`, `03-swarm-dispatch.md`

[PARTITION NOTE: This is the evidence-quality lens over 4 assigned research files. Cross-file checks (contradictions, scope coverage) limited to this subset. Full cross-file verification requires merging with other partition reports.]

---

## Overall Verdict: PASS

Every sampled `file:line` citation across all four research files was independently verified against the actual source by opening the cited file and confirming the cited line says what the research claims. Adversarial stance applied — I assumed citations were hallucinated and tried to break them. They held. I found **zero** fabricated, wrong, or materially-drifted citations. One trivial off-by-one in a prose line-count (not a citation) is noted as MINOR and does not affect any claim.

---

## Verification Method

For each file I sampled 3–7 load-bearing citations that name a file path + line number, opened the cited source (`runner.py`, `contract.py`, `models.py`, `commands.py`, `swarm/dispatch.py`, `swarm/models.py`, `swarm/commands.py`, `swarm/reduce.py`, `execution/parallel.py`, `transports/openai_compat.py`, and the spec) and confirmed the cited line/range matches the claim byte-for-content. I also verified the two existence claims (`ensemble.py` absent; spec present) and the file line-count assertions.

---

## Per-Claim Verification Results

### File 00 — `00-prd-extraction.md` (spec transcription)

| # | Claim (research) | Cited location | Actual | Result |
|---|---|---|---|---|
| 1 | feature_id FR-RH2, complexity 0.82 HIGH, release 4.4.0 | spec frontmatter | spec L6/L9-10/L11 exact | PASS |
| 2 | exit-code map `pass→0, halted→10, degraded→11, blocked→2` | spec | spec L438 `verdict_map_unchanged` + L303 verbatim | PASS |
| 3 | (M,N) guard table: M==0→blocked/2/`ensemble-empty`; M==1→degraded/11/`single-reviewer-fallback`; M≥2<2cls→degraded/11/`degraded-model-diversity` | spec §5.3 | spec L448-450 verbatim | PASS |
| 4 | `dispatch.dispatch_wave1 (dispatch.py:334)`, `_resolve_run_transport_factory (commands.py:612)` | spec FR-RH2.1 deps | spec L195/L97/L100/L156/L159 AND confirmed against real source (def at dispatch.py L334, commands.py L612) | PASS |
| 5 | FR sequence is .1,.2,.3,.4,**.9**,.5,.6,.7,.8 | spec | spec L182-309 headings in exactly that order | PASS |
| 6 | worker-status→M: only `success` counts; `parse_error` "salvage may promote per swarm §7.4" | spec §5.3 | spec L454-458 verbatim | PASS |
| 7 | OI-1 BLOCKING GATE = swarm ResultContract→reflect contract correspondence table, resolve before FR-RH2.3 | spec §11 | spec L586 verbatim | PASS |
| 8 | path-confinement: two `return-contract.yaml`; reflect MUST NOT parse `t2-swarm/` subdir | spec §5.3 | spec L441-444 verbatim | PASS |

File 00 is a faithful, non-fabricated transcription. No invented FR/NFR/OI IDs; the spec's own internal citations (`dispatch.py:334`, `commands.py:612`) are themselves correct against source.

### File 01 — `01-reflect-runner-seam.md` (code tracer)

| # | Claim (research) | Cited location | Actual | Result |
|---|---|---|---|---|
| 1 | `_MODEL_ALIAS_ENV_VARS` 3-tuple (corrected from spec ~L38-40) | runner.py L37-41 | exact, contents match | PASS |
| 2 | `_WRAPPER_MARKER = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` | runner.py L53 | exact | PASS |
| 3 | `_audit_once`; seam block proc/start/wait/parse/derive | runner.py L392, L405-427 (env_vars L416, start L418, wait L419, parse L420, derive L421-426, contract_path L427) | every line exact | PASS |
| 4 | `expected_tier = 2 if depth in {standard,deep} else 1` | runner.py L403 | exact | PASS |
| 5 | `_build_prompt` flag sequence (`/sc:reflect --mode post …`) | runner.py L341-366 | flag order matches exactly | PASS |
| 6 | `count_model_aliases` body `sum(... if (env.get(var) or "").strip())` | runner.py L254/L261 | exact | PASS |
| 7 | re-audit loop opens L536; `_audit_once()` w/ NFR-4 comment | runner.py L536-537 | exact (comment verbatim) | PASS |
| 8 | `write_reflect_post` L117, `write_sidecar` L188, `_child_env` L238, `run` L453 | runner.py | all four exact | PASS |
| 9 | commands.py docstring "so Tier 2 fans out" | commands.py L49-61 | verbatim quote correct | PASS |
| 10 | CLI `run()` spans L148-249 | commands.py | L148 `def run(`, L249 `sys.exit(exit_code)` ✓ | PASS |
| 11 | `ensemble.py` does NOT exist | reflect/ pkg | `find . -name ensemble.py` → no hit | PASS |
| 12 | `dispatch_wave1` L334 / `_resolve_run_transport_factory` L612 / `reduce_wave3` L555, all sync | swarm | all three at cited lines, plain `def`, grep for async/await → none | PASS |
| 13 | `[CODE-CONTRADICTED]` correction: NO public factory; `_resolve_run_transport` L510 + `_resolve_run_transport_factory` L612 both private; `read_env` L159 public | swarm/commands.py, openai_compat.py | both private at cited lines; `read_env` at L159 ✓ | PASS — self-correction is accurate |
| 14 | `ResultContract` L877, `WorkerResult` L1027 (located, not Read — tagged `[UNVERIFIED]`) | swarm/models.py | class ResultContract L877, WorkerResult @dataclass L1026/class L1027 ✓ | PASS (and the `[UNVERIFIED]` tag is honest) |

File 01 is exemplary: line numbers re-verified, drift from the task's `~L` hints corrected inline, and a genuine `[CODE-CONTRADICTED]` self-correction (the "public equivalent" caveat) confirmed accurate.

### File 02 — `02-reflect-contract-verdict.md` (data model analyst)

| # | Claim (research) | Cited location | Actual | Result |
|---|---|---|---|---|
| 1 | `Verdict` enum + exit_code map `{PASS:0,HALTED:10,DEGRADED:11,BLOCKED:2}` | models.py L26-54 (map L44-49) | exact | PASS |
| 2 | `is_promotable` ⇔ PASS | models.py L51-54 | exact | PASS |
| 3 | `derive_verdict` first-match ordering blocked→degraded→halted→pass | contract.py L130-246, docstring L139 | exact | PASS |
| 4 | BLOCKED stage: timeout L148-159, child-crash F0 L156-159, contract-missing L160-164, version L166-181, degraded_components list-guard L184-193, tier_reached L195, F2 bool-guard L200-209 | contract.py | every range exact | PASS |
| 5 | `_LOAD_BEARING_BOOL_FIELDS` (7 booleans) | contract.py L47-57 | exact, all 7 names match | PASS |
| 6 | `_DEGRADED_COMPONENTS_HALT_SET` = {serena, auggie, env-aliases, evidence-validator, serena:context-excluded} | contract.py L31-33 | exact verbatim | PASS |
| 7 | `_VERIFICATION_SKIP_EXEMPTIONS` = {read-only-project, tool-unavailable, --no-verify} | contract.py L36-38 | exact | PASS |
| 8 | `_degraded_reason` 14 triggers — every cited trigger line (T7 mcd L267-269, T10 single-reviewer L280-281, T11 null-conv L284-285, T12 verification L288-291, T13 citations L294-298, T14 drift L301-302) | contract.py L249-304 | every cited trigger line exact | PASS |
| 9 | `_halted_reason` status L311-314, regression L315-316, deviations L323-327 | contract.py L307-328 | exact | PASS |
| 10 | PASS gate L235 (`status=="success" AND tier_reached==expected_tier`); tier-mismatch fall-through L241-246 | contract.py | exact | PASS |
| 11 | `classify_fix` carve-out L331-366 | contract.py | def at L331, semantics match | PASS |
| 12 | `parse_contract` returns None when missing/unparseable/non-mapping | contract.py L65-82 | exact | PASS |
| 13 | Self-noted "line-number drift now corrected" against task brief `~L` hints | — | the brief's `~L249/~L267-269/~L280-281` confirmed correct as the research states | PASS |

File 02's trigger-by-trigger field-correspondence table is the most citation-dense of the four and was the highest hallucination risk. Every one of the 14 degraded triggers and every BLOCKED/HALTED/PASS line citation is exact. The honest `[UNVERIFIED]` tags on producer-side emission and enum domains are appropriate.

### File 03 — `03-swarm-dispatch.md` (API surface mapper)

| # | Claim (research) | Cited location | Actual | Result |
|---|---|---|---|---|
| 1 | `dispatch_wave1` full kw-only signature | dispatch.py L334-343 | verbatim match | PASS |
| 2 | Early-exit L409-410; `workers_requested` L412; `executor.quiet=True` L425 | dispatch.py | exact | PASS |
| 3 | Synthetic `proxy_error` backstop `WorkerResult(index=index, status="proxy_error", attempts=1)` | dispatch.py L487-490 | block at L485-490; synthetic at L490 — within cited range | PASS |
| 4 | success predicate `sum(1 for r in results if r.status=="success")` (dispatch's own success_count) | dispatch.py L496 | exact verbatim | PASS |
| 5 | `_DEFAULT_TIMEOUT_SEC=180` L124; `_classify_http_code` L127; `_send_once` L143; `retry_policy` L195; `_run_worker` L279 | dispatch.py | all exact | PASS |
| 6 | `RetryPolicy` defaults on_5xx=True, backoff=2, on_4xx=False, on_timeout=False | swarm/models.py L149-152 | exact | PASS |
| 7 | `WorkerStatus` Literal 4 values L69; `ResultStatus` L68 (distinct enum) | swarm/models.py | both exact verbatim | PASS |
| 8 | `WorkerResult` 12 fields with types/defaults | swarm/models.py L1117-1128 | every field/type/default exact | PASS |
| 9 | `__post_init__` raises ValueError on bad status | swarm/models.py L1130-1136 | exact | PASS |
| 10 | `ResultContract.output_files: list[WorkerResult]` L1010; count triple L1007-1009; INV-005 | swarm/models.py | exact | PASS |
| 11 | `ParallelExecutor` class L80, quiet L100, plan L105, execute L173, _execute_group L214, ThreadPoolExecutor L219 | execution/parallel.py | all exact | PASS |
| 12 | StatusPolicy IMM-5 matrix M==N→success / 2≤M<N→partial / M<2→failed | swarm/models.py L535-539 | exact verbatim (incl. tie-break L539) | PASS |
| 13 | `ensemble.py` absent (find → no hit; grep dispatch_wave1 → only def site + commands/normalize/logging) | swarm/ | confirmed absent | PASS |

File 03's `[UNVERIFIED]` caveat (the M-vs-N rule is a design obligation since `ensemble.py` doesn't exist) is correctly scoped and honest.

---

## Confidence Gate

Per-checklist categorization (all VERIFIED items cite specific tool output above):

- **Confidence:** Verified: 4/4 files (47/47 sampled citations) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 0 | Glob: 0 | Bash: 5 (each Bash batched multiple `sed -n`/`grep` line-confirmations directly mapping to specific citations; Read calls targeted the exact cited ranges)
- No web research performed (all claims are local source-truth; Tavily not required).

Tool-call count (16 Read+Bash invocations covering ~47 distinct line confirmations) comfortably exceeds the per-file checklist size; no padding.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `01-reflect-runner-seam.md` line 15 + line 254/269 | Prose states `runner.py` is "598 lines"; actual file is 597 lines (off by one). This is a prose count, NOT a citation — every actual `file:line` citation in the file is correct. | Change "598 lines" → "597 lines". Cosmetic; does not affect any verdict or downstream synthesis. |

No CRITICAL or IMPORTANT issues. No fabricated paths, no wrong line numbers, no off-by-many citations, no doc-only claims masquerading as code-verified.

## Cross-File Consistency (within partition)

No contradictions between the four files. They agree on: exit-code map, `derive_verdict` ordering, the seam location (`_audit_once` L405-419 branched on `expected_tier` L403), the three reuse-by-import swarm symbols and their line numbers (`dispatch_wave1` L334 / `_resolve_run_transport_factory` L612 / `reduce_wave3` L555), the M-over-N (succeeded vs requested) diversity rule, and `ensemble.py`'s non-existence. File 01 and File 02 both cite `ReflectResult` at `models.py L94-121` — consistent and correct.

## Notable Strengths (adversarial findings that held up)

- Every `[CODE-VERIFIED]` tag in Files 01–03 is backed by a citation that actually checks out. The tag is not decorative.
- File 01's `[CODE-CONTRADICTED]` self-correction (no public transport-factory API) is itself correct — both resolvers are genuinely private at L510/L612.
- `[UNVERIFIED]` tags are used honestly for things not Read this turn (swarm `ResultContract` field schema, producer-side emission, `ensemble.py` design obligations) rather than papered over.

## Recommendations

- Apply the one MINOR prose fix (598→597) if/when File 01 is next edited; not blocking.
- The honest `[UNVERIFIED]` items (swarm `ResultContract` field schema vs reflect contract fields; producer-side `/sc:reflect` emission) are the real open work flagged by OI-1 — these are correctly surfaced as gaps, not silently assumed. They belong in the synthesis Gap Analysis / Open Questions, not in this evidence-quality verdict.

## QA Complete
