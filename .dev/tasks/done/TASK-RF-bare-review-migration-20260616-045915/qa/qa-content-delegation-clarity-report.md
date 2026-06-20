# QA Report — doc-qualitative (delegation-clarity lens)

**Topic:** sc-bare-review SKILL.md M8/M9 migration to thin CLI caller
**Date:** 2026-06-16
**Phase:** doc-qualitative
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Target:** `src/superclaude/skills/sc-bare-review/SKILL.md` (80 lines)

---

## Overall Verdict: FAIL

Three substantiated content defects, all source-verified. Two are CRITICAL (would mislead an
agent into emitting an unexecutable command or expecting a STOP that never fires); one is an
internal contradiction (always IMPORTANT+). The four explicit verification targets resolve as:
T1 PASS-with-defect, T2 PASS, T3 PASS, T4 PASS.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| T1 | Invocation block concrete + executable | FAIL | Command shape valid (see I-2); `--c7*` claim makes it non-executable (I-2) |
| T2 | Old "thin orchestrator over three bundled scripts" framing GONE / replaced with CLI-delegation | PASS | grep for `thin orchestrator`/`bundled script` (positive framing) returns nothing; Purpose §IS now reads "thin caller over `superclaude swarm run --lens bare-review`" (L22-23). BUT see I-1: the *scripts themselves* are not retired |
| T3 | No orphaned Wave A-E / manifest.json read-step / single-message dispatch / `t2_*` script refs | PASS | grep `Wave [A-E]\|manifest\.json\|single-message dispatch` finds only negations ("no manual single-message dispatch", L43). No `t2_*` positive refs in prose |
| T4 | "Read return-contract.yaml and relay it" unambiguous | PASS | L42-44 names exact file `<output-dir>/return-contract.yaml`, the Read tool, and "relay it"; filename confirmed as `CONTRACT_FILENAME = "return-contract.yaml"` (reduce.py:139) |

## Summary
- Checks passed: 3 / 4 (T2,T3,T4); T1 FAIL
- Checks failed: 1 (plus 2 cross-cutting content defects surfaced during T1/T2)
- Critical issues: 2
- Important issues: 1
- Issues fixed in-place: 0 (REPORT ONLY)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I-1 | CRITICAL | L10 meta-comment: "legacy bundled scripts retired" | FALSE. `scripts/t2_preflight.sh`, `scripts/t2_dispatch.sh`, `scripts/t2_normalize.py` all still physically present under `src/superclaude/skills/sc-bare-review/scripts/`. The migration claim that scripts are retired is contradicted by the skill's own package contents. An agent (or maintainer) trusting "retired" may believe the bundled-script execution path is gone when it is not. | Either delete the `scripts/` directory as part of this migration, OR change "legacy bundled scripts retired" to an accurate status (e.g., "scripts retained but no longer invoked by this skill; pending removal"). |
| I-2 | CRITICAL | L31 (Invocation): "`--label <str>` (`--c7*` accepted but no-op)" | `swarm run` declares no `--c7` option (grep `c7` across `cli/swarm/` = 0 hits) and `run_cmd` does NOT set `ignore_unknown_options` (verified `@click.command("run")` decorator stack, commands.py:1299-1470). Passing `--c7` to the documented command would cause click to **error** ("No such option: --c7"), not no-op. An agent reading ONLY this skill and relaying a `--c7`-bearing flag would emit an unexecutable command — the exact delegation-clarity failure this review targets. | Remove the "`--c7*` accepted but no-op" claim entirely, OR (if c7 passthrough is genuinely intended) add `ignore_unknown_options=True` to `run_cmd` and document it. As written the skill describes behavior the CLI does not have. |
| I-3 | IMPORTANT (contradiction → never MINOR) | L32 vs L61 + config.py | **Internal contradiction + wrong contract.** L32 states swarm preflight requires the env contract `T2ProxyUrl/T2ProxyKey/T2Model0N/T2Timeout` (4 vars) and "STOPs naming any missing var." The Failure-Modes table at L61 lists only `T2ProxyUrl/T2ProxyKey/T2Model0N` (3 vars). The CODE agrees with L61, not L32: `SwarmConfig.missing_t2_env_vars()` (config.py:151-166) checks ONLY proxy-url, proxy-key, and `T2Model01..N` — `T2Timeout` is never read by `from_env` and can never appear in the missing-var STOP list. `T2Timeout` is a legacy `t2_preflight.sh` env var (t2_preflight.sh:74), not part of the swarm CLI preflight contract. So L32 both contradicts L61 and misstates which vars trigger the env-missing STOP. | Drop `T2Timeout` from the L32 env contract so it reads `T2ProxyUrl/T2ProxyKey/T2Model0N`, matching L61 and `missing_t2_env_vars()`. If `--timeout-sec`'s default-180 behavior needs documenting, state it as a flag default (CLI value, not a preflight-required env var). |

## Verification performed (source-grounded)
- **Command shape valid:** every flag in the L35-38 invocation block exists on `swarm run` —
  `--lens`/`--target`/`--output`/`--transport` (commands.py:1318,1352,1362,1374),
  `--reviewers`/`--target-line-cap`/`--timeout-sec`/`--label` (commands.py:1386,1399,1411,1423).
- `--reviewers` `[2,4]` validation real (commands.py:1640).
- `--transport` choices `("openai_compat","stub")` real (commands.py:489); "stub = hermetic dry
  run" matches transport stub (transports/stub.py present).
- IMM-4 `<50 non-whitespace bytes` real (`MIN_TARGET_NON_WHITESPACE_BYTES = 50`, preflight.py:136).
- IMM-5 status thresholds (M==N→success / 2≤M<N→partial / M<2→failed) consistent across L51 & L65.
- `recommended_next_command` literal `--suspect-source` (L54) coherent with §9.1 (L73-74).
- All three named tests exist: `tests/swarm/test_bare_review_parity.py`,
  `test_recipe_bare_review.py`, `test_e2e_user_guide.py`.
- `return-contract.yaml` filename confirmed (reduce.py:139).

## Self-Audit (MANDATORY)
1. **Factual claims independently verified against source:** ~14 — every invocation flag (8),
   `--reviewers` range, transport-kind choices, IMM-4 byte floor, env-var contract membership,
   the env-missing STOP mechanism (`missing_t2_env_vars`), return-contract filename, and existence
   of all 3 cited test files.
2. **Files read/grepped to verify:** `src/superclaude/skills/sc-bare-review/SKILL.md`;
   `cli/swarm/commands.py` (run_cmd decorator stack, flag options, reviewers validation, transport
   kinds); `cli/swarm/config.py` (T2 env contract, `missing_t2_env_vars`); `cli/swarm/preflight.py`
   (IMM-4 50-byte floor); `cli/swarm/reduce.py` (CONTRACT_FILENAME); `tests/swarm/` directory
   listing; `skills/sc-bare-review/scripts/` directory listing; `scripts/t2_preflight.sh`.
3. **Why trust this is thorough (not a rubber-stamp):** I did not accept the L10 "scripts retired"
   claim — I `ls`'d the scripts dir and found all three still present (I-1). I did not accept the
   L31 c7 no-op claim — I grepped the entire `cli/swarm/` tree for `c7` (0 hits) and read the
   `run_cmd` decorator to confirm no `ignore_unknown_options` (I-2). I cross-read L32 against L61
   AND the actual `missing_t2_env_vars()` implementation to prove the env contract is 3 vars, not 4
   (I-3). Three defects from an 80-line file the adversarial floor required ≥5 places be probed; I
   probed ~14 claims and the 3 that failed are each backed by a file:line.
4. **Web research:** none performed (all verification was local-file-bound). Tavily-first N/A.

## Confidence
**Verified:** 4/4 checklist targets resolved with tool evidence | **Unverifiable:** 0 |
**Unchecked:** 0 | **Confidence:** 100% (computed: all 4 review targets + 3 cross-cutting defects
backed by file:line). Eligible-threshold met; verdict is FAIL on defect presence, not on coverage.

**Tool engagement:** Read: 1 | Bash(grep/ls/sed): 8 | Glob: 0 | (tool calls ≥ checklist items: yes)

## Recommendations
Resolve all three issues before this migration ships — none is exempt:
1. (I-1) Delete `scripts/t2_*` or correct the "retired" claim.
2. (I-2) Remove the `--c7*` no-op clause (it describes nonexistent CLI behavior).
3. (I-3) Drop `T2Timeout` from the L32 env contract to match L61 and the code.

## QA Complete
