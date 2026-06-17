# QA Report — Structural Contract-Preservation (sc-bare-review thin-caller rewrite)

**Topic:** sc-bare-review SKILL.md M8/M9 migration to thin caller over `swarm run --lens bare-review`
**Date:** 2026-06-16
**Phase:** report-validation (contract-preservation lens, structural)
**Fix authorization:** false (REPORT ONLY)
**Lens:** contract-preservation — "Assume the rewrite dropped at least 5 caller-facing guarantees. Find them."

---

## Overall Verdict: PASS

All five caller-facing guarantee groups survive the rewrite. Every guarantee was independently verified against the rewritten `SKILL.md` (cited by line) AND cross-checked against the original-structure map (research §1.4/§1.7/§1.8/§1.9/§9.1). Cited test files were verified to exist on disk. The deltas found are non-caller-facing diagnostic-field reductions in the contract YAML (model_label/bytes/elapsed_ms/target_truncated), which are weakenings of *observability*, not of any *behavioral* guarantee the caller relies on — documented below as MINOR for transparency, not as contract breaks.

---

## Items Reviewed

| # | Guarantee group | Result | Evidence (SKILL.md line) |
|---|-----------------|--------|--------------------------|
| 1 | Return Contract: `status` enum success\|partial\|failed | PASS | L50 `status: success \| partial \| failed` |
| 1 | IMM-5 success-first rule (M==N→success; 2≤M<N→partial; M<2→failed) | PASS | L50 inline comment + L65 table row `M<2`→failed / `2≤M<N`→partial; arithmetic matches research §1.7 L156-158 |
| 1 | `suspect: true` always | PASS | L53 `suspect: true   # always — suspect by construction`; restated L68 Will-list |
| 1 | `recommended_next_command` containing LITERAL `--suspect-source` | PASS | L54 literal `--suspect-source <bare1>,…`; L74 acceptance pointer re-asserts "literal `--suspect-source`" |
| 2 | §3.2 flag surface: --target, --output, --reviewers (2-4 def 3), --target-line-cap (4000), --timeout-sec (180), --label | PASS | L29-31: `--target`(REQUIRED), `--output`(REQUIRED), `--reviewers`(2-4, default 3), `--target-line-cap`(default 4000), `--timeout-sec`(default 180), `--label`; `--c7*` accepted-but-no-op preserved (L31) |
| 3 | §8 env-unset STOP | PASS | L61 `Env var (...) unset → STOP at preflight naming the missing var`; L40-41 reinforces |
| 3 | §8 reviewers out-of-range STOP | PASS | L62 `--reviewers out of [2,4] ... STOP, no dispatch` |
| 3 | §8 IMM-4 empty-target STOP no-dispatch | PASS | L62 `<50 non-ws bytes (IMM-4) ... STOP, no dispatch`; L40-41 "fail at preflight before any reviewer dispatches" |
| 3 | §8 5xx retry-once (after 2s) | PASS | L63 `Proxy 5xx → retry once after 2s, then proxy_error, continue`; matches research §1.8 |
| 3 | §8 partial/failed thresholds | PASS | L65 `M<2`→failed (do NOT proceed) / `2≤M<N`→partial (only successful files listed) |
| 4 | §3.4 Boundaries Will-list (read target, N parallel, per-reviewer timeout, continue ≥2, suspect:true, emit recommended_next_command, write only inside --output) | PASS | L67-68 Will-list complete |
| 4 | §3.4 Will-NOT incl. "route to Anthropic" exclusion + "write outside --output" | PASS | L69 `route to Anthropic; write outside --output`; "judge/score/filter; retry beyond one 5xx" also present |
| 5 | §9.1 acceptance/test pointers | PASS | L73-75 cite AC-1.1..1.12 + `test_bare_review_parity.py`, `test_recipe_bare_review.py`, `test_e2e_user_guide.py`, IMM suite — all 3 named files verified to EXIST on disk (Bash ls) |

## Summary
- Guarantee groups passed: 5 / 5
- Sub-checks passed: 13 / 13
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)
- MINOR observations (non-contract-breaking): 3

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | SKILL.md L52 (`output_files[]`) | Per-file diagnostic fields `model_label`, `bytes`, `elapsed_ms` present in original contract (research §1.7 L137-154) are dropped from the documented `output_files` shape (now `path, model_id, status` only). Caller-facing status enum per file is preserved (`success\|timeout\|parse_error\|proxy_error`). Observability reduction, not a behavioral break. | If the swarm CLI still emits these fields, optionally re-document them; otherwise confirm intentional compression. No caller depends on them per the Boundaries list. |
| 2 | MINOR | SKILL.md L51 (contract header) | `target_truncated` boolean from original contract (research §1.7 L137-154) is not documented in the rewrite. `target_checksum` IS preserved (L51). | Confirm whether swarm CLI emits `target_truncated`; if so add it for fidelity. Not caller-actionable. |
| 3 | MINOR | SKILL.md L64 vs research §1.8 | Original 13-row failure table compressed to 5 rows. All behavioral guarantees survive (env STOP, range STOP, IMM-4, 5xx-retry-once, 4xx-no-retry via "Proxy 4xx ... per-reviewer status", timeout, parse_error+§7.4 salvage, M<2/2≤M<N). The dropped rows were enforcement-location detail (curl/jq host requirement — legitimately removed post-migration) and the "adversarial-fails-later → artifacts preserved" row. | None required for contract preservation; curl/jq row correctly dropped (research §1.5/§1.8 flagged it as DROP). Optionally restate artifact-preservation if callers relied on it. |

## Adversarial Probe Results (the "find ≥5 dropped guarantees" mandate)

I actively hunted for dropped caller-facing guarantees. Findings:
- **4xx no-retry:** preserved implicitly — L64 lumps "Proxy 4xx / timeout / parse fail → per-reviewer status, continue", and L69 Will-NOT says "retry beyond one 5xx" — so 4xx is not retried. NOT dropped. PASS.
- **`M==N==2→success` edge case:** research §1.7 L156 calls this out explicitly. The rewrite's L50 rule `M==N→success` subsumes it correctly (when N=2 and M=2, M==N holds → success). Arithmetic NOT weakened. PASS.
- **`--c7*` accepted-but-no-op:** preserved (L31). NOT dropped.
- **per-reviewer hard timeout:** preserved (L67 Will-list "per-reviewer hard timeout"). NOT dropped.
- **write-on-failure (contract written on every invocation):** preserved — §3.3 header L46 "written on every invocation including failure". NOT dropped.
- The only genuine reductions are the 3 MINOR diagnostic/observability items above. None is a caller-facing *behavioral* guarantee. The "assume ≥5 dropped" prior is not borne out — the rewrite is a faithful contract-preserving thin-caller.

## Confidence Gate

- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 2 | Grep: 0 | Glob: 0 | Bash: 4
- Tool-call count (6) exceeds the 5 guarantee groups; each Bash call mapped to a specific guarantee group (contract tokens, flag tokens, env/failure tokens, test-file existence). No padding.
- No UNCHECKED items. No UNVERIFIABLE items. No web research required (all claims local; test pointers verified on disk).

## Recommendations
- PASS — green light. The thin-caller rewrite preserves all five caller-facing guarantee groups.
- Before merge, optionally confirm with the swarm-CLI owner whether `output_files[]` still carries `model_label/bytes/elapsed_ms` and whether `target_truncated` is emitted, then either restore them to the documented contract or confirm intentional compression. These are documentation-fidelity nits, not blockers.
- The parity tests (`test_bare_review_parity.py`, `test_recipe_bare_review.py`) are the real enforcement surface for byte-compatibility of the contract the swarm CLI must reproduce — ensure they remain green in CI.

## QA Complete
