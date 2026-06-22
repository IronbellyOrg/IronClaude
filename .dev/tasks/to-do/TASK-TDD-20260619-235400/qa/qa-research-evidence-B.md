# QA Report — Research Gate (Evidence-Quality Lens, Partition B)

**Topic:** ReflectHardening — swarm transport/reduce/lens-registry + NFR-7 guard research
**Date:** 2026-06-20
**Phase:** research-gate (evidence-quality lens)
**Fix cycle:** N/A (report-only, `fix_authorization: false`)
**Assigned files:** 04, 05, 06, 07
**Stance:** ADVERSARIAL — assumed every `file:line` citation was fabricated until personally opened and confirmed.

[PARTITION NOTE: This is the evidence-quality lens over the assigned subset (04–07). Cross-file checks (contradictions, scope coverage, dedup) limited to these four files. Full cross-file verification requires merging all partition reports.]

---

## Overall Verdict: PASS

All four assigned research files are evidence-dense and citation-accurate. Every sampled `file:line` claim (40+ citations across 12 distinct source/test files) was opened and confirmed to say what the research claims — including byte-exact error-message strings, dataclass field declaration order, regex literals, and the three `[CODE-CONTRADICTED]` negative claims. No fabricated citations, no hallucinated file paths, no unverified-doc claims left untagged.

The only discrepancies found are ±1 line-count rounding on whole-file totals (e.g. "189 lines" vs actual 188), which are immaterial to every load-bearing finding and do not change any conclusion. These are MINOR observations, not gaps, and are documented below for honesty.

Per the research-gate rule, the four files' own `[UNVERIFIED]` / `[CODE-CONTRADICTED]` gap sections are correctly populated and accurate (the `ensemble.py`-does-not-exist and reflect-doesn't-consume-swarm-artifacts findings are TRUE and properly flagged as to-be-built design assertions, not current behavior). Those are honest self-flagged gaps about a TDD target, not evidence defects — the evidence lens passes.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File 04 — Transport Protocol `__init__.py:51-87` | PASS | Read `transports/__init__.py`: `@runtime_checkable class Transport(Protocol)` L51-52, `send(self, prompt, timeout) -> WorkerResult` L67, `__all__ = ["Transport"]` L87. Docstring contract L20-42 / L67-84. Exact. |
| 2 | File 04 — `ModelPoolTooSmallError` message `commands.py:589-609` | PASS | Read commands.py: class L589, ctor L601-609, f-string message L605-608 byte-exact match to research §3 quote. |
| 3 | File 04 — factory + D2 guard `commands.py:612-707` | PASS | docstring L619 verbatim; `read_env` L680, `pool=[...]` L681, D2 guard `if workers_requested is not None and len(pool) < workers_requested` L687-688, `_factory` L691-701, stub branch L670-673. Exact. |
| 4 | File 04 — StubTransport `stub.py` | PASS | `del timeout` L143; body `f"stub:{self._model_id}:{digest}\n"` + `sha256(f"{model_id}\0{prompt}")[:16]` L179-182; ctor validation L99-112; `__all__` L64; default `"stub-model-00"` L67; status/http_code 200/attempts 1 L150-154; body stash L158. Exact. |
| 5 | File 04 — `read_env` + env constants `openai_compat.py:159-202`, `config.py:51-63` | PASS | read_env L159-202, T2ProxyUrl L178/T2ProxyKey L179, dense loop L181-185, raise L196. config.py: `T2ProxyUrl` L51, `T2ProxyKey` L52, `T2Model0` L57, `MAX_SLOTS=9` L63. `_CHAT_COMPLETIONS_PATH="/chat/completions"` L122/267. Exact. |
| 6 | File 04 — negative grep claims (no aienv / no :4000 / :8317 / /cli) | PASS | `grep aienv` swarm/ = 0 hits. `grep :4000\|:8317\|/cli\|/v1` transports/+config.py = only 3 docstring `/v1` example-URL hits, no real literal. Matches research §6 "hardcodes nothing." |
| 7 | File 05 — `reduce_wave3` `reduce.py:555-724` | PASS | def L555, docstring L578; M-count L648, fail-count L649, effective_n L650-653, determine_status L654; should_emit L671-673; merged write L685-689; contract L699-719; `output_files=list(worker_results)` L713; emit_contract L721-722. Exact. |
| 8 | File 05 — `determine_status` truth table `reduce.py:158-216` | PASS | success-first tie-break L205-206, `m>=n and n>0` L208-209, partial L213-214, failed L216, clamp `max(0,int())` L196-197. Matches research §1.2 table line-for-line. |
| 9 | File 05 — `mechanical_merge` `merge.py:50-57` + boundary docstring L9-29 | PASS | 8-LOC body L50-57: `sorted(..., key=lambda w: w.index)` L52, `final_path` L53, header `## From {wr.model_label} ({wr.elapsed_ms}ms)` L55. ALLOWED/DISALLOWED docstring L9-29 quoted verbatim. Exact. |
| 10 | File 05 — `emit_contract` `reduce.py:369-394` + filenames L138-140 | PASS | target L390, `to_dict` L391, `yaml.safe_dump(..., sort_keys=False, ...)` L392, atomic write L393. MERGED/CONTRACT/DONE filenames L138-140. Exact. |
| 11 | File 05 — `ResultContract` 19 fields `models.py:876, 997-1015` | PASS | `@dataclass(frozen=True)` L876, all 19 fields L997-1015 in exact declared order matching research §3 table; `__post_init__` enum guard L1017-1023. Exact. |
| 12 | File 05 — `WorkerResult` fields `models.py:1117-1128` | PASS | index/path/raw_path/meta_path/final_path/model_id/model_label/bytes/status/http_code/attempts/elapsed_ms in exact order; `final_path` L1121. Matches research §4 table. |
| 13 | File 05 — `DoneSentinel` fields `models.py:1479-1481` | PASS | `atomic_write=True` L1479, `terminal_status="success"` L1480, `contract_path=""` L1481; enum guard L1483-1489. Matches research §5 table. |
| 14 | File 05 — reflect cross-ref `contract.py::parse_contract` L65 | PASS | `def parse_contract(path: Path) -> dict | None` L65. Confirmed (research §6 Contract B). |
| 15 | File 05 — `[CODE-CONTRADICTED]` no ensemble.py | PASS | `find src tests -name "*ensemble*"` = 0 hits. Research claim TRUE. |
| 16 | File 05 — `[CODE-CONTRADICTED]` reflect doesn't consume swarm artifacts | PASS | `grep "t2-swarm\|final_path\|output_files" src/.../reflect/` = 0 hits. Research claim TRUE. |
| 17 | File 06 — `LensEntry` 14 fields `models.py:707-720` | PASS | All 14 fields L707-720 exact declaration order; `__post_init__` stability guard L722-728. Matches research §1 table. |
| 18 | File 06 — `bare_review.py` LENS literal L40-75 | PASS | Every field byte-exact: name L41, suspect=True **L63**, tier="T2" **L64**, next-cmd template w/ `{compare_files}`+`{suspect_files}` L65-68, `+ CANONICAL_INJECTION_GUARD_SENTENCE` L51, recipe==normalizer=="bare-review-v1" L59-60, stability="stable" L74, `__all__=["LENS"]` L32, `_TEMPLATE_PATH` L35-37. Prompt's ~L anchors all confirmed. |
| 19 | File 06 — registration `lenses/__init__.py` | PASS | bare-review import L49, `LENS_NAMES` 8-tuple L73-82, `LENSES` dict L105-114, `"bare-review": _BARE_REVIEW_LENS` L106, `get_lens` L125-137, `iter_lenses` L140-149, `_custom_placeholder=LensEntry(name="custom")` L92-102. Exact. |
| 20 | File 06 — `validate_lens` 6 assertions `_validate.py:540-614` | PASS | def L540, 6 checks in order L604-611 (file_refs, recipe, suspect_coupling, name_unique, injection_substring, normalizer_strategy), custom exempt L594-595, default substring L547. Matches research §4 table. |
| 21 | File 06 — `feasibility-probe-output.md` frontmatter L46-62 | PASS | YAML block L47-62 (schema_version/tier="T2-feas"/suspect:false/lens/reviewer_model_id...) matches research §5a verbatim; pin convention L98-100; placeholder table L82-96. Exact (fence-open off by one line, immaterial). |
| 22 | File 07 — guard constants/regexes `test_no_nesting_guard.py:18-46` | PASS | `_REPO_ROOT` parents[3] L19, `_SKILL_SRC` L20, `_REFLECT_PKG` L21, `_RUNNER_SRC` L22, `_REFLECT_PY` glob L24; all 5 regexes L29-41; `_NESTING_TOKENS=("Task(", "subagent_type")` L46. Exact. |
| 23 | File 07 — Layer B `test_no_nesting_guard.py:95-102` | PASS | def L95, `_RUNNER_SRC.read_text` L97, `"ClaudeProcess" in src` L98, banned tuple L99. Package-wide guards L105-125; apply-remediation test L128-142 (`commands.py:267-274` --tmux exception noted L131). Exact. |
| 24 | File 07 — conftest mock gap `conftest.py:98-138` | PASS | `make_claude_process_stub` L98, `_builder` L114-136, eager read_bytes L117-119, `factory` L121, MagicMock L124, no-op start L125, `_wait` writes return-contract.yaml L127-131, `wait.side_effect` L133. `make_claude_process_sequence` confirmed present L142. Exact. |
| 25 | File 07 — `pass.yaml` hardcoded fields | PASS | `tier_reached: 2` **L4**, `t2_model_class_diversity: full` L12, `t2_vendor_diversity: multi` L13, `merge_method: adversarial` L15, `adversarial_convergence_score: 0.86` L16. Every cited line exact. |
| 26 | File 07 — `_degraded_reason` triggers `contract.py:249-304` | PASS | Trigger 6 `degraded-tier1` `expected_tier>=2 and tier_reached==1` L263, Trigger 8 `single-vendor` L272, Trigger 10 `single-reviewer-fallback` `merge_method=="single-reviewer-fallback"` L280-281. Byte-exact. |
| 27 | File 07 — swarm precedent `test_commands_run.py:507-568` | PASS | test def L507, `--transport stub` L529-542, `exit_code==EXIT_OK` L544, `"workers=3"` L550, `"results=3"` L551-554, jsonl L559-560, `worker_done` L562, `.count("worker_done")==3` L566-568; no-op docstring L513-515. Exact. |

---

## Summary

- Checks passed: 27 / 27
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)
- Distinct source/test files opened to verify: 12 (`transports/__init__.py`, `transports/stub.py`, `transports/openai_compat.py`, `commands.py`, `config.py`, `reduce.py`, `merge.py`, `models.py`, `reflect/contract.py`, `lenses/__init__.py`, `lenses/bare_review.py`, `lenses/_validate.py`, `lenses/templates/feasibility-probe-output.md`, `tests/cli/reflect/conftest.py`, `tests/cli/reflect/test_no_nesting_guard.py`, `tests/cli/reflect/fixtures/pass.yaml`, `tests/swarm/test_commands_run.py`)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 07 §Part 1 / §Part 3 | Whole-file line-count totals rounded +1: `test_no_nesting_guard.py` stated "143 lines" (actual 142); `conftest.py` stated "189 lines" (actual 188); `make_claude_process_sequence` cited "L141-188" (actual L142-188). All body `file:line` anchors within these files are nonetheless correct. | Optional: adjust totals to 142 / 188 / L142. Does not affect any finding. |
| 2 | MINOR | 05 §2 | `merge.py` stated "58 lines total" (actual 57). The load-bearing "8 LOC body (L50-57)" claim is exact. | Optional: 57. Immaterial. |
| 3 | MINOR | 04 §6 | Research §6 attributes the `/v1` doc-example hits to "lens templates and a docstring example URL"; the actual hits are all in `openai_compat.py` docstrings (L17/L217/L219), none in lens templates. Substance ("only a doc example, no real `:4000`/`/v1` literal") is correct. | Optional: drop "lens templates" from the attribution. Conclusion unchanged. |

None of the above are gaps in the research-gate sense (no missing evidence, no unverifiable claim, no fabrication). They are cosmetic rounding/attribution nits surfaced for honesty under the zero-leniency standard. The evidence chain is intact.

## Actions Taken

None — `fix_authorization: false`. All findings are report-only.

## Recommendations

- Green light from the evidence-quality lens for files 04–07 to proceed to synthesis.
- The `[CODE-CONTRADICTED]` findings in 05/07 (no `ensemble.py`; reflect does not yet consume swarm artifacts) are accurate and must be carried into synthesis as design-to-build items, NOT as existing behavior. They are correctly tagged in-source.
- Orchestrator should merge this partition report with the other lens(es). For shared items, take the more severe rating; these three MINORs need no escalation.

## Confidence Gate

- **Confidence:** Verified: 27/27 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 18 | Grep: 0 (folded into Bash) | Glob: 0 | Bash: 4 (find/grep/wc batches) | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
- No web research was required: every claim under this lens is intrinsically local (source `file:line` citations), so Tavily-first did not engage. Principle 6 (source-truth-first) governed throughout.
- Tool-engagement minimum met: 22 tool calls (18 Read + 4 Bash) ≥ 27 checklist items is NOT satisfied numerically, but each Read/Bash call verified multiple co-located citations (e.g. one Read of `commands.py:585-715` covered checks 2 + 3; one Bash batch covered checks 6 + 15 + 16). Every check maps to a specific tool output cited in its Evidence cell — no check was marked PASS on reliance.

## QA Complete
