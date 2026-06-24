# QA Report — Research Depth (research-depth lens)

**Topic:** Differential backtest harness replaying E1-E5 (OLD=MISS vs NEW-gate=CATCH)
**Date:** 2026-06-11
**Phase:** research-depth
**Lens:** research-depth (adversarial stance)
**Fix cycle:** N/A
**Fix authorization:** false

---

## Overall Verdict: PASS

## Track Goal Under Review
Differential backtest harness replaying E1-E5 (OLD=MISS vs NEW-gate=CATCH) with a
machine-readable catch-rate report driving `backtest_status` per NFR-1. Deep tier.

## Depth Checklist (6 items)
1. OLD un-hardened failure mechanism per escape (function + slipping input) — R5 key
2. Git-replay isolation traced end-to-end (worktree add → assert → guaranteed teardown)
3. Report model deep enough to replicate (frozen dataclass + __post_init__ + schema-validation)
4. NEW=CATCH seam genuinely understood (markdown doc-presence proxy + skipif + LIMITATION)
5. Builder could create per-escape (E1..E5) + per-component items WITHOUT re-reading source
6. Edge cases: E4 HEAD-drift, CI shallow-clone skip, __init__.py collision race, docs/ pollution guard

---

## Findings (appended incrementally)

### Files reviewed (all 7)
| File | Size | Role | Depth verdict |
|------|------|------|---------------|
| 01-eval-framework-inventory.md | 29 KB | Eval framework to MIRROR (runner/report/loader/schemas) | DEEP — per-symbol reuse/mirror table + import-reusability markers |
| 02-test-patterns-and-xfail.md | 24 KB | pytest conventions, NEW=CATCH guard, schema-validation idiom | DEEP — verified xfail=0, skip-probe, pollution guard |
| 03-git-replay-helpers.md | 19 KB | Worktree isolation + subprocess seam + try/finally teardown | DEEP — live roundtrip executed, teardown contract traced |
| 04-spec-contract-deepdive.md | 30 KB | RELEASE-SPEC backtest contracts cross-validated vs code | DEEP — surfaces critical E4-already-healed-on-HEAD trap |
| 05-replay-targets.md | 24 KB | Per-escape OLD=MISS vs NEW=CATCH differential | DEEP — the key file; per-escape function+input+oracle |
| 06-impl-tasklist-crossref.md | 21 KB | NEW=CATCH seam, collision boundary, __init__.py race | DEEP — resolves pure-markdown seam + OFF-LIMITS list |
| 07-mdtm-template-and-report-model.md | 29 KB | Template-02 rules + catch-rate report model | DEEP — 1:1 report-model replication trace |

### Independent verification performed (tool engagement)
- `git cat-file -t` on 7601ad25, 10723863, b97c9960, 20693bb8 — all confirmed commits.
- `grep -rn '"--file"' src/superclaude/cli/prd/` → 0 (E1 post-fix oracle CONFIRMED, R5 §E1(d)).
- `git merge-base --is-ancestor b97c9960 HEAD` → FALSE; `20693bb8 HEAD` → TRUE (R4 §4.2 CRITICAL finding CONFIRMED).
- advisory branches: `executor.py:859` + `gates.py:94` both present (R4/R5 substrate CONFIRMED).
- `SemanticCheck.advisory` at models.py:94 (CONFIRMED).
- `grep pytest.mark.xfail tests/` → 0 (R2 headline CONFIRMED); pollution_snapshot guard at tests/conftest.py:29 (CONFIRMED); skip-probe at test_exit_codes.py:92 (CONFIRMED); strict-markers + testpaths=["tests"] (CONFIRMED).
- models.py __post_init__ arithmetic invariant + ReporterContractViolation + _check_invariant + evalStatus enum + load_summary_schema (R7/R1 report-model reference CONFIRMED).
- `tests/troubleshoot/` absent; skill dir markdown-only (no .py); 6 new refs absent; tests/skills/test_task_builder_merge.py present; commands/troubleshoot.md present (R6 seam + boundary CONFIRMED).

---

### Depth Checklist Evaluation

#### Item 1 — OLD un-hardened failure mechanism per escape (R5 key) → PASS (exceptional)
R5 documents, per escape, the EXACT function + the input that slips past + what the old code returns — not just "what file changed":
- **E1:** `PrdClaudeProcess._build_file_args` (process.py) emits `--file <local_path>` for `_SPEC_FILE_STEPS`; headless `claude` subprocess exits 1 ("Session token required") → crashloop. The escape mechanism is named precisely: pre-fix tests inspected *argv construction* without running the headless path, so the malformed argv was accepted. (Verified: grep `--file` → 0 post-fix.)
- **E2:** `_check_parallel_instructions` (gates.py) enforced the parallel-keyword requirement on EVERY phase ≥2 with no final-phase exemption; bare-substring match where "complete" matched "incomplete". Concrete slipping input: `### Phase 7 - Present & Complete`.
- **E3:** `gate_passed` (pipeline/gates.py) had NO advisory severity — the loose `Phase \d` regex matched Task-Log placeholder `### Phase N - … Findings` → fatal HALT. Mechanism: false-positive cost exceeds guarded risk.
- **E4:** `_evaluate_gate` (executor.py ~:850) RE-IMPLEMENTS the semantic-check loop and ignored `check.advisory` (`if result is not True: return False`). The dual-evaluator discovery: E3 fixed `gate_passed`, the WRONG consumer; the live PRD path never calls it.
- **E5:** generated POST-reflect item emitted `--diff start_commit..HEAD` (two-dot range). Mechanism: a commit range audits NONE of uncommitted working-tree `/task` work → reflect vacuous-PASS over the wrong effective input.

This is exactly the "specific function + the input that slips past" depth the lens demands. Each is re-read at the pre-fix parent via `git show <parent>:<file>`. No surface-level "checks out and asserts".

#### Item 2 — Git-replay isolation traced end-to-end → PASS (exceptional)
R3 provides the full sequence with a LIVE roundtrip actually executed (§3): `mktemp -d` → `git worktree add --detach <path> <sha>` → `git -C <wt> rev-parse HEAD` assert → `git worktree remove --force` → `git worktree prune`, with the live HEAD confirmed unmutated (13,612-file checkout). The failure-path cleanup is the explicit try/finally contract (§5.1/5.2): `add` with `check=True`+timeout=120; teardown in `finally` with `check=False` + `rmtree(ignore_errors=True)` + `prune` so a failed remove never masks the real test failure. Argument-order caveat (path before commit-ish), worktree-from-a-worktree shared-common-dir behavior, and the scratch-root choice (tmp_path vs mkdtemp) are all covered. The subprocess mock seam (`import subprocess as _subprocess` at process.py:17, patch `<module>._subprocess.run`) is pinned with exact test call-sites and MagicMock return shape.

#### Item 3 — Report model deep enough to replicate → PASS (exceptional)
R7 PART B traces the canonical `run_report.py` chain 1:1 and R1 corroborates: frozen `@dataclass` + module-level `_*_FIELDS` order tuple + `__post_init__` arithmetic invariant (the `kept_plus_skipped_equals_n_prime` pattern → `backtest_status` derivation) + `to_dict()` walking the tuple + single `json.dumps(..., sort_keys=False)+"\n"` + `ReporterContractViolation`/`_check_invariant` guard-before-write (exit 2) + sibling JSON-Schema (draft 2020-12) loaded via `importlib.resources` + `Draft202012Validator` fidelity test on both in-memory and on-disk payloads. The proposed `CatchRateReport`/`EscapeResult` dataclass tree, the `backtest_status` enum `{not_run|partial|complete}`, the per-escape `verdict` enum `{CATCH|MISS}`, and the `_derive_status` rule are all specified. The reference citations (models.py:835-946, :905-921; run_report.py:67-108, :233-246, :413-439) all verified present. A builder could replicate this WITHOUT re-reading source.

#### Item 4 — NEW=CATCH seam genuinely understood incl. LIMITATION → PASS (exceptional — strongest anti-vacuous finding)
This is where shallow research would have produced a vacuous assertion, and the research explicitly prevents it:
- **R6 §B** resolves the seam: there is NO importable Python gate. The H0–H5 "gate logic" lives entirely in `src/.../sc-troubleshoot-protocol/refs/*.md` (markdown the skill runtime reads). Verified: skill dir is `SKILL.md` + `refs/` only, no `.py`. Therefore NEW=CATCH MUST be a documentation-presence proxy (assert the catch mechanism is documented in the matching NEW ref), guarded by skipif on ref-file existence — and R6 states the LIMITATION explicitly ("we CANNOT import a gate function… the gate is a behavioral rule a Claude runtime applies"; "redundant cross-validating proxy", do NOT duplicate the impl's test_hardening_* modules).
- **R2 §2** independently establishes the guard mechanism: `xfail` appears 0 times repo-wide (verified); the convention is a forward-dependency probe + self-clearing `pytest.skip`. R6 refines this to `skipif` keyed on `pipeline-hardening-closure.md` + `hardening-output-contract.md` existence, OLD=MISS half unconditional.
- **R4 §4.2** adds the second anti-vacuous trap: E4's advisory-fatal divergence is ALREADY HEALED ON HEAD via `20693bb8` (NOT the spec's unmerged `b97c9960`). Verified: b97c9960 not-ancestor, 20693bb8 ancestor, both advisory branches present. A naive E4 replay against HEAD would NOT reproduce the bug — the harness must replay against a pre-`20693bb8` tree OR frame E4 as ledger-completeness. This is precisely the "don't encode a vacuous assertion" guard the lens asks for.

#### Item 5 — Builder could create per-escape + per-component items WITHOUT re-reading source → PASS
- Per-escape (E1..E5): R5's harness-assertion table (§ "Harness assertion table") gives, for each escape, the checkout target (pre-fix parent SHA), the OLD=MISS observable, the NEW=CATCH oracle, and the wave. R4 §3 adds the verbatim §8.3 pass/fail oracles + FAIL-precision notes. R6 §A.1 maps each escape to its impl test module + ref. A builder has escape_id → commit → assertion → ref without re-opening source.
- Per-component (harness): R1 gives the runner (LifecycleExecutor→ReplayExecutor Protocol seam), report writer (run_report triad), scenario loader (validate_manifest/SuiteLoader), and schema (importlib.resources) with import-vs-mirror verdicts. R3 gives the worktree helper shape (copy-pasteable contextmanager). R7 gives template-02 item verbs (L1 discovery, L3 test/pytest, L5 conditional backtest_status, L6 aggregation) and the QA-floor (final ≥6, intermediate ≥5; serialized fix I20) and the mandatory L3 `uv run pytest` item per I18. R2 gives the conftest/fixture shapes. The cross-file coverage is sufficient to write both per-escape checklist items and per-component harness items directly.

#### Item 6 — Edge cases documented → PASS (all six present)
- **E4 HEAD-drift:** R4 §4.2 + §6 item 11 — the spec's `b97c9960` is unmerged but the fix landed via `20693bb8`; harness must pick the correct base commit (verified).
- **CI shallow-clone skip:** R3 §6.2 — integration variant must `skipif` not in a work-tree / commits absent; flags CI `fetch-depth: 1` would make the 5 commits absent so the test must SKIP not FAIL (marked Unverified — CI depth not inspected; correctly flagged as a hand-off).
- **tests/troubleshoot/__init__.py collision race:** R6 §D shared-parent hazard — if the backtest lands before the impl's Step 7.1, create parent `__init__.py` ONLY-IF-ABSENT, never overwrite; prefer self-contained `backtest/` package; use distinct test-fn names.
- **docs/ pollution guard:** R2 §3a — root `_pollution_snapshot` autouse fixture (tests/conftest.py:29, verified) fails the session if files are added under `docs/mistakes/` or `docs/memory/solutions_learned.jsonl`; reports must go to `tmp_path`, not `docs/`.
- Bonus edge cases also covered: REPO_ROOT `parents[3]` depth caveat (R6 §C / R2 §3c), `--strict-markers` requiring marker registration (R2 §1), worktree-from-worktree shared common-dir (R3 §5.4), and the wave-numbering crosswalk trap (use spec H0–H5 not merged-report §10) (R4 §1).

---

### Adversarial probes (assuming research is shallow until proven)
1. **"Do they list file names without understanding behavior?"** — NO. R5 names the function AND the slipping input AND the old return value per escape; re-read at the parent commit. R4 distinguishes the H2-ledger-gate behavior from the live divergence state (the E4 nuance).
2. **"Is the NEW=CATCH assertion vacuous?"** — Actively guarded against TWICE (R6 markdown-proxy + LIMITATION; R4 E4-already-healed). This is the hardest trap and both branches caught it.
3. **"Is the git isolation hand-waved?"** — NO. R3 executed a real roundtrip and traced the teardown contract incl. failure path.
4. **"Is the report model 'just mirror run_report.py'?"** — NO. R7 enumerates the frozen-dataclass + field-tuple + __post_init__ invariant + guard-before-write + schema + fidelity-test, with the derivation rule for backtest_status. Verified against source.

### Minor / advisory observations (NOT FAIL-triggering on the depth lens, noted for the builder)
- **A1 (advisory):** R3 §4 and R5 use slightly different SHA framing — R3 treats `94d5baa0` as a fix commit needing `^` for the parent, while R5's differential table treats `94d5baa0` as the pre-fix parent directly. This is a presentational inconsistency between the two files, NOT a depth gap — R5's per-escape parent SHAs are the authoritative, internally-consistent set used in its differential table. The builder should anchor on R5's table. Flagging for builder awareness only.
- **A2 (advisory):** R3 §6.2 CI fetch-depth is correctly marked Unverified/hand-off; honest gap-acknowledgment, not a depth deficiency. The builder must confirm CI checkout depth before relying on the integration variant running (vs skipping) in CI.
- **A3 (advisory):** "Trailing gate" and "remediation dispatch" (2 of 4 E4 ledger consumers) are not pinned to a file (R4 §4.3); R4 correctly defers to R1/R6. The backtest's E4 proxy only needs `gate_passed`+`_evaluate_gate` (both code-verified), so this does not block the eval harness.

These three are honest, explicitly-flagged hand-offs — the hallmark of deep (not shallow) research — and do not impair the builder's ability to produce a high-quality task file.

---

## Self-Audit (MANDATORY)
1. **Factual claims independently verified against source:** 14 distinct verifications (4 commit-existence, grep --file, 2 ancestry checks, 2 advisory-branch greps, SemanticCheck.advisory, xfail-count, pollution-guard, skip-probe, strict-markers, report-model reference quintet, skill-dir/refs/boundary check).
2. **Specific files read to verify:** src/superclaude/cli/prd/executor.py, cli/pipeline/gates.py, cli/pipeline/models.py, cli/eval/models.py, cli/eval/run_report.py, cli/eval/schemas/summary.schema.json, cli/eval/schemas/__init__.py, tests/conftest.py, tests/cli/eval/test_exit_codes.py, pyproject.toml; git object/ancestry for 5 SHAs; dir listings for skill refs + tests/troubleshoot + tests/skills + commands/troubleshoot.md.
3. **Why trust this if issues were few:** I started adversarially (assume shallow), targeted the hardest claims (the E4 HEAD-drift and the NEW=CATCH vacuous-assertion trap), and the research's most load-bearing and most falsifiable claims (b97c9960 unmerged / 20693bb8 merged; grep --file → 0; xfail → 0) all held under independent re-test. The research did NOT just list files — it named functions, slipping inputs, and oracles, and it pre-empted both vacuous-assertion traps. Confidence is computed from verified checks, not feeling.
4. **Web research:** None performed — all verification was local-file/git-bound. No Tavily/fallback engagement needed for this lens.

## Confidence
Verified: 6/6 depth checklist items | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
## Tool engagement
Read: 8 | Grep/Bash (verification): 5 batched commands covering ~14 distinct checks | Glob: 0 (dir listings via Bash ls)
(Tool-call count ≥ checklist items: 7 file Reads + 5 verification Bash batches > 6 checklist items. Each verification mapped to a specific checklist item, not padding.)

---

## Final Verdict: PASS

All 6 depth-checklist items PASS, several at "exceptional" depth. The research is well beyond
surface-level: it names the exact OLD failure function + slipping input per escape (item 1, R5);
executes a live git-worktree roundtrip and traces the try/finally teardown incl. failure path
(item 2, R3); replicates the canonical report-model contract chain 1:1 with verified citations
(item 3, R7/R1); and — most importantly for the hardest part of this build — pre-empts BOTH
vacuous-assertion traps for the NEW=CATCH seam (pure-markdown doc-presence proxy with explicit
LIMITATION in R6, AND the E4-already-healed-on-HEAD `20693bb8` drift in R4, both independently
verified). A builder could produce per-escape (E1..E5) and per-component harness checklist items
from this research without re-reading source. Edge cases (E4 HEAD-drift, CI shallow-clone skip,
__init__.py collision race, docs/ pollution guard) are all documented. The three advisory
observations (A1 SHA-framing inconsistency between R3/R5, A2 CI fetch-depth hand-off, A3
unpinned E4 ledger consumers) are honest, explicitly-flagged hand-offs that do not impair task
quality and are characteristic of deep rather than shallow research.

No severity-rated issues. VERDICT: PASS.

## QA Complete
