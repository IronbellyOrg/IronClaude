# Research Completeness Verification (Partition 1 of 2)

**Topic:** Build `superclaude reflect run` thin CLI wrapper
**Date:** 2026-06-08
**Files analyzed:** 4 (research/01–04)
**Depth tier:** Deep
**Spec:** .dev/brainstorms/20260608-182553-reflect-cli-wrapper/merged-requirements.md

> [PARTITION NOTE: Cross-file checks (contradictions, scope-coverage audit, cross-references) limited to assigned subset (research/01–04). Full cross-file analysis requires merging both partition reports.]

---

## Verdict: PASS (0 gaps blocking synthesis; 5 spot-checks all confirmed; partition-scoped open questions correctly flagged, not skipped)

---

## Spot-Check Verification (5 citations opened against live source; required minimum was 3)

| # | Claim (research file) | Cited source:line | Opened & confirmed? | Notes |
|---|---|---|---|---|
| 1 | `ClaudeProcess.__init__` is keyword-only (`*` at line 39); `timeout_seconds: int = 6300`; `model: str = ""`; `build_command` order; `build_env` pops only `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT` (R01) | process.py:37-54, 73-95, 97-112 | YES — EXACT | `*` at :39, `timeout_seconds=6300` at :46, `model=""` at :44, build_command order :79-94, build_env pops both CLAUDECODE vars :108-109. Every cited line supports the claim verbatim. |
| 2 | `contract_version: "1.3.0"` (quoted) is authoritative; report-template.md:14 shows stale `1.2.0` (DRIFT) (R02) | SKILL.md ~654/:791; report-template.md:14 | YES — EXACT | SKILL.md §9.1 header "Stable contract (contract_version: 1.3.0)" + `contract_version: "1.3.0"` confirmed; closing "Contract version is `v1.3.0`" near :791 confirmed; report-template.md:14 = `contract_version: 1.2.0` (unquoted) confirmed. Drift is real. |
| 3 | main.py registration = deferred import + `# noqa: E402,I001` + `main.add_command(group, name=...)`; init-lite is last before `if __name__`; cli_portify omits `name=` (R03) | main.py:400-437 | YES — EXACT | All groups present (sprint/roadmap/cleanup-audit/tasklist/cli_portify/prd/eval/recommend/init-lite); `main.add_command(cli_portify_group)` omits name (confirms R03's main.py:418 claim); init-lite last before `if __name__ == "__main__":`. Insertion point is correct. |
| 4 | `launch_in_tmux` = `new-session -d -s <name> *argv` → `attach-session` → read `.sprint-exitcode`; fail-OPEN swallow assumes success (R04) | tmux.py:50-61, 81-108, 162-173 | YES — EXACT | `is_tmux_available` TMUX-env guard, `session_name`=`sc-sprint-`+sha1[:8], detached new-session w/ argv splice, attach-session, `.sprint-exitcode` read with `except (OSError, ValueError): pass # assume success`. The fail-open posture R04 flags for inversion is verbatim-present. |
| 5 | `git merge-base` exists ONLY as prose in task-builder/SKILL.md:1996, no Python helper; drift.py `_git` is the reusable shape (R04 headline) | task-builder/SKILL.md:1996; drift.py:266-288 | YES — EXACT | `grep -rn 'merge-base\|merge_base' src/` → only SKILL.md:1996 (and an unrelated gh-context mention in auggie-review SKILL.md:88, not Python). drift.py `_git` at :266, `["git","-C",cwd,*args]` :268, `@{upstream}` :277. Headline finding is sound. |

**Spot-check conclusion:** 5/5 confirmed exact. No fabricated or drifted citations detected in this partition. Evidence quality is the strongest tier — line-precise and re-verifiable.

---

## Per-Criterion Assessment (9 criteria from spawn brief)

### 1. Source files identified with paths and exports? — PASS
- R01: `ClaudeProcess` import paths both confirmed (process.py:24 direct; pipeline/__init__.py:74 re-export), full kwargs table with per-param source lines, every public method (build_command/build_env/start/wait/terminate/validate_tool_write_output) cataloged.
- R02: exact file (`<output>/return-contract.yaml`), 60+-field §9.1 block quoted verbatim, every load-bearing field has a `SKILL.md:NNN` citation; correctly distinguishes return-contract.yaml from promotion-log.yaml (gate_evaluation struct) and runs.jsonl (run_id).
- R03: 6-file package map (`__init__/commands/config/models/runner/contract`) each anchored to a prd/roadmap precedent file:line; `__init__.py` re-export pattern confirmed against live prd/__init__.py.
- R04: tmux.py + drift.py + process.py + executor.py reuse sources each cited with line ranges; reuse/adapt/fresh-write matrix is exhaustive.

### 2. Output paths and formats clear or reasonably inferred? — PASS
- Pinned `--output` dir (FR-4) referenced consistently across R01/R02/R04. R02 fixes the parse target (`return-contract.yaml`) and the contract shape. R04 derives `.reflect-exitcode` sentinel location (under pinned `--output`) by analogy to sprint's `.sprint-exitcode` under state_dir, with the desync footgun (forward the dir to the inner invocation) explicitly flagged.

### 3. Logical breakdown of phases/steps present? — PASS
- R03 §5 gives the thin runner flow: derive → launch ClaudeProcess → parse return-contract.yaml (via contract.py) → derive verdict → write frontmatter → return result. R01 gives the lifecycle trio (start/wait/terminate) and exit-code contract (124→timeout). R04 separates foreground-default vs `--tmux` additive path. Builder has a clear per-module step decomposition.

### 4. Patterns and conventions documented with examples? — PASS
- R03 §7 is a full conventions table (`from __future__ import annotations`, lazy imports in command body, `ValueError`→`click.echo(err=True)`+`sys.exit(1)`, `click.Choice(case_sensitive=False)`, `is_flag=True`, `--dry-run` short-circuit) each with prd/roadmap evidence. Verbatim Click idiom blocks quoted. R04 gives copy-ready subprocess shapes.

### 5. MDTM template notes present with rule references? — PARTIAL/PASS (scoped)
- These four files are CODE-RESEARCH files (primitive, schema, CLI pattern, reuse idioms); MDTM template/frontmatter mechanics are the explicit scope of research/05-frontmatter-writeback.md and 06-taskbuilder-template-integration.md (partition 2). Within partition 1, R04 correctly cites the canonical `start_commit` frontmatter field name (FR-3) and task-builder/SKILL.md:1996 as the behavioral spec for base-resolution. No MDTM gap is attributable to this partition's files — the topic lives in p2. [PARTITION NOTE: full MDTM-template coverage must be confirmed against research/05-06 in partition 2's report.]

### 6. Granularity sufficient for per-file/per-component checklist items? — PASS (strongest dimension)
- R03 maps EACH of the 6 `cli/reflect/*.py` modules to its responsibilities + precedent. R01 enumerates every constructor kwarg + the two MUST-override defaults (`timeout_seconds=3600` not 6300; non-empty `model`). R02 classifies every contract field load-bearing/optional with fail-loud-vs-tolerate guidance. R04 gives a verbatim/adapt/fresh-write disposition per capability. The builder can author one item per module with item-level acceptance criteria directly from these.

### 7. Documentation cross-validation — doc-sourced claims tagged? — PASS
- R01: every architectural claim is CODE-sourced (process.py line cites); `build_env` purity explicitly marked "Verified" by reading the function; doc/spec claims (FR-10/11) cross-checked against code mechanism. Unverified items explicitly labeled "Unverified" (cwd/chdir, serena-session impact → R08).
- R02: the headline is a doc-vs-doc DRIFT surfaced and resolved (§9.1 `1.3.0` authoritative vs report-template.md `1.2.0` stale) — exactly the staleness-detection the checklist wants. Also flags an internal line-ref drift in promotion-adapters.md:154 (cites L1213-1224; actual 1468-1481) as non-load-bearing.
- R03/R04: every "verified"/"unverified" boundary is explicit; R04 marks the fail-open→fail-closed inversions "Verified from source, not assumed."
- No doc-sourced claim is presented as fact without a code anchor or an explicit Unverified tag.

### 8. If new implementation: solution research evaluated approaches? — PASS
- R03 §6 evaluates `contract.py` against the closest analogues (roadmap parser modules) and justifies the isolated-pure-module choice per Risk §10. R03 §5 weighs reuse of PrdExecutor machinery and explicitly rejects the heavy pipeline (gates/convergence/monitor/prompts) as out-of-scope for a thin wrapper. R04 §2d evaluates two options for the `<integration>` token (configurable-default-master vs dynamic origin/HEAD) and recommends, deferring the final pick to the author. R01 evaluates plain ClaudeProcess vs HomeIsolation/ClaudeProcessAdapter and rejects the hermetic-HOME path as FR-10-breaking.

### 9. Unresolved ambiguities documented (not silently skipped)? — PASS
- R01: chdir-to-repo-root need (no `cwd=` param); `--no-session-persistence` serena impact (→R08); slash-invocation surface (→R08) — all flagged.
- R02: `gate_evaluation` struct location, `citations_dropped_extrapolated` recording-only trap, `serena_summary_corroboration: unavailable` is benign-not-halt, promotion-adapters line-ref drift — all surfaced.
- R04: the **FR-3 `<integration>` literal** is the most consequential open question (master vs integration; unencoded in code) and is explicitly flagged as an Open Question for the task with a recommended default. The fail-open→fail-closed posture inversions (sentinel readback; git fallback) are called out as required adaptations, not silent reuses.

---

## Cross-File Consistency (within partition 1 only)

No contradictions among R01–R04. They interlock cleanly and cross-reference deliberately:
- R01 defers reflect's slash-invocation surface and serena-session impact to R08 (partition 2) — correct boundary, no overlap claimed.
- R03 §4 flags "does reflect need the PipelineConfig base?" as Unverified and routes confirmation to R01/R04 — R01 confirms the plain `ClaudeProcess` primitive is self-sufficient (no pipeline base needed for the process layer), consistent.
- R02 and R04 agree the wrapper writes its OWN frontmatter verdict and does NOT use reflect's internal promotion (R02 §6.3 marks promotion_* informational; R04 confirms foreground path returns the derived exit code directly).
- R01's `timeout_seconds` 6300-vs-3600 override and R04's foreground `proc.start(); rc=proc.wait()` default agree on the lifecycle contract.

> [PARTITION NOTE: Cross-file checks (contradiction detection, scope-coverage audit, cross-reference completeness) are limited to the assigned subset R01–R04. Claims that R01/R03/R04 defer to "R08"/"R05"/"R06" (partition 2 files) are correctly-scoped deferrals here but their RESOLUTION must be verified when partition 2's report is merged. Full cross-file analysis requires the merged report.]

---

## Compiled Gaps

### Critical Gaps (block synthesis) — NONE in this partition

### Important Gaps (affect quality) — NONE attributable to R01–R04
All ambiguities the files raise are correctly flagged AS open questions for the builder/author rather than left as silent holes. They are research OUTPUTS, not research gaps.

### Minor / Carry-forward items (must still be tracked, not failures)
1. **FR-3 `<integration>` literal is unencoded** (R04 §2d) — the builder MUST surface this as an Open Question item in the task (recommended: configurable, default `master` = origin/HEAD), since it changes base-resolution behavior. Source-confirmed: origin/HEAD→master, integration branch exists, PR target master.
2. **Two ClaudeProcess defaults must be overridden** (R01) — `timeout_seconds=3600` (default is 6300) and non-empty `model=` (default `""` omits `--model`). The builder should encode these as explicit acceptance criteria on the runner/config items so they are not silently inherited.
3. **Fail-open→fail-closed inversions** (R04 §1c/§2b) — sentinel readback and git base fallback both fail-OPEN in their sprint/drift sources; the wrapper MUST invert to fail-closed (`blocked`/exit 2). Builder should make this an explicit item-level requirement, since copying the source verbatim would violate FR-8/NFR-4.
4. **`degraded_components` HALT-subset matching** (R02 §3) — must match the FR-11 set `{serena, auggie, env-aliases, evidence-validator, serena:context-excluded}` precisely, NOT "any non-empty list" (benign fail-open tokens appear there). Builder should encode the exact predicate (and note R08 owns final routing).

None of items 1–4 are research deficiencies — they are precisely the load-bearing constraints the builder needs, and the research surfaced every one of them.

---

## Depth Assessment

**Expected depth:** Deep (data-flow traces, integration-point mapping, pattern analysis).
**Actual depth achieved:** Meets/exceeds Deep for all 4 files.
- Data-flow traces: R01 traces the full start()→wait()→terminate() lifecycle and the env-build chain line by line; R04 traces the full sentinel write/read cycle end-to-end across two files (tmux.py reader + executor.py writer).
- Integration-point mapping: R03 maps the exact main.py insertion point and the 6-module package; R02 maps which artifact carries which field (return-contract vs promotion-log vs runs.jsonl).
- Pattern analysis: R03 §7 conventions table; R04 §3 reuse/adapt/fresh-write matrix.
**Missing depth elements:** None within partition scope.

---

## Recommendations
1. **Proceed to synthesis** for the partition-1 surface — R01–R04 are synthesis-ready with line-precise evidence.
2. **Carry forward the 4 minor items** above as explicit task acceptance criteria / Open Questions (especially FR-3 `<integration>` and the fail-closed inversions — both are behavior-changing and easy to get wrong by verbatim copy).
3. **At merge time**, confirm partition 2 (R05 frontmatter-writeback, R06 taskbuilder-template, R08 reflect-invocation/degradation routing) resolves the deferrals R01/R03/R04 hand off — particularly R08's value→verdict routing (R02 fixes the data shape only) and R05/R06's MDTM-template mechanics (criterion 5).

---

## Original status header (superseded by Verdict above)
