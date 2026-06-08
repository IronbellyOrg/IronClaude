# QA Report — Research Gate

**Topic:** BRV-MG sibling skill creation against IronClaude repo
**Date:** 2026-05-31
**Phase:** research-gate
**Fix cycle:** 1
**Fix authorization:** false
**Adversarial stance:** assume errors exist; verify every claim

---

## Files in Scope
- `01-sibling-skill-template-and-reflect-cmd.md` (R1)
- `02-workflow-evalworkspace-refs.md` (R2)
- `research-notes.md` (parent)

## Verification Log — Spot Checks (all 10 from prompt)

| # | Spot check | Tool | Result | Evidence |
|---|---|---|---|---|
| 1 | Flat commands path layout | `ls /config/workspace/IronClaude/src/superclaude/commands/` | PASS | Output: `auggie-review.md, reflect.md, ...` flat — no `sc/` subdir at source-of-truth (R1 §0 correction is correct) |
| 2 | reflect.md line 258 = `## Related Commands` | `Read commands/reflect.md L255-265` | PASS | Line 258 is `## Related Commands`; 6 bullets at 260-265 verbatim match R1 §3.2 |
| 3 | auggie SKILL.md = 376 LOC | `wc -l` | PASS | Exactly 376 LOC |
| 4 | readme-quality-check.yml = closest pattern | `Read .github/workflows/readme-quality-check.yml L1-30` | PASS | Has `permissions:` block (L12-15: `contents: read, pull-requests: write, issues: write`) and uses implicit `GITHUB_TOKEN` |
| 5 | No workflow installs claude CLI | `grep -in "claude\|anthropic" .github/workflows/*.yml` | PASS | All hits are substring matches inside `superclaude`/`SuperClaude` framework refs; zero `claude` CLI install/invoke; zero `anthropic` references |
| 6 | grader.py ~21 KB, PyYAML-only | `wc -c` + `head -30 grader.py` | PASS | 20,939 bytes ≈ 21 KB; imports: `json, re, sys, functools.reduce, pathlib.Path, yaml` — yaml is only third-party dep |
| 7 | Makefile reflect-eval at L493-505 | `sed -n '490,510p' Makefile` + grep | PASS | `reflect-eval:` at L493, `reflect-eval-quick:` at L501; recipe block spans L493-L506 (R2's "493-505" close enough) |
| 8 | MERGED-PROPOSAL exists, 6,464 words | `wc -w` | PASS | Exactly 6,464 words |
| 9 | R2 blockers (claude CLI install + ANTHROPIC_API_KEY) encoded | Read R2 §2 + §8 | PASS-with-caveat | R2 §2 blueprint YAML omits the explicit `claude` CLI install step (jumps from `uv pip install` to `claude --skill ...`); R2 §8 flags both as Blocker/Open-Question. Sufficient for builder to add as Phase 5 prerequisite items, but task file MUST encode both as concrete checklist items. |
| 10 | Per-amendment/per-file granularity for 50-70 items | Read research-notes.md §SUGGESTED_PHASES + R1 §6 + R2 §§2-7 | PASS | R1 §6 provides Phase 2 step-by-step skill-build breakdown (Steps 2.1-2.2 + 16 enumerated skeleton items); R2 provides 6 distinct artifacts (workflow / eval-workspace tree / grader.py copy+strip / falsifier YAML / refs YAML / Makefile targets). 7 phases × granular sub-items easily yields 50-70 atomic items. |

## Checklist (10-item Research-Gate)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | File inventory: each file has Status: Complete + Summary | PASS | R1 frontmatter "Status: Complete" + §7 Summary; R2 "Status: Complete" + tail Summary. research-notes.md present (at task root, not in research/). |
| 2 | Evidence density (>80% claims cited file:line) | PASS | R1 cites SKILL.md line numbers throughout (1-12, 47-61, 62-73, 258, 487-576, etc.); R2 cites workflow files with line numbers (publish-pypi.yml:21-22, readme-quality-check.yml:12-15, Makefile:493-505). Density >80% on both. |
| 3 | Scope coverage of EXISTING_FILES | PASS | All 6 files-to-create + 1 file-to-amend covered. R1: SKILL.md, command file, reflect.md amendment, __init__.py question. R2: workflow, eval-workspace, refs YAML, Makefile. |
| 4 | Doc-cross-validation tags | N/A — minimal | No doc-only architecture claims requiring [CODE-VERIFIED]/[CODE-CONTRADICTED] tags; both researchers cite source files directly. |
| 5 | Contradiction resolution | PASS | One real contradiction: research-notes.md says `commands/sc/reflect.md` and `__init__.py needed for parity`; R1 corrects to flat `commands/reflect.md` (§0) and finds parity is NOT required (§5.1 — mixed pattern, primary template lacks it). R1 explicitly surfaces the correction. |
| 6 | Gap severity | PASS-with-1-MINOR | All 5 gaps in research-notes.md addressed: Gap 1 RESOLVED in §0; Gap 2 covered by R2 §1 + §2; Gap 3 covered by R1 §5.1; Gap 4 covered by R2 §4; Gap 5 (cost-profile mirror) is partially covered — R2 §6 documents the cost-profile.yaml pattern source, but neither researcher explicitly anchors §15 cost-profile derivation. MINOR: builder should add a checklist item to populate the cost-profile-equivalent. |
| 7 | Depth appropriateness (Standard tier) | PASS | Standard tier requires file-level coverage; both researchers provide file-level + line-number coverage. R1 §6 traces the full skill-creation data flow Phase-by-Phase. |
| 8 | Integration-point coverage | PASS | R1 documents reflect SKILL.md §9 → new sibling §9 contract reuse; R2 documents grader.py copy+extend; both document the sync-dev / verify-sync boundary between src/ and .claude/. |
| 9 | Pattern documentation | PASS | R1 enumerates the 2-block frontmatter pattern (YAML + HTML comment), wave-anatomy pattern (Preconditions/Steps/Exit-criteria), error-handling matrix shape. R2 enumerates the ref-file YAML header pattern, falsifier-suite skeleton shape, Makefile target pattern. |
| 10 | Incremental writing compliance | PASS | Both files show iterative structure (R1 §0 path correction was clearly appended after main body when divergence was discovered; R2 §1 inventory table built up). No one-shot signatures. |

## Cross-File Issues / Latent Risks

1. **MINOR — research-notes.md uses obsolete `commands/sc/` paths.** §EXISTING_FILES and §RECOMMENDED_OUTPUTS still list `src/superclaude/commands/sc/pr-bot-validate.md` and `src/superclaude/commands/sc/reflect.md`. R1 §0 correctly identifies that source-of-truth is FLAT (`src/superclaude/commands/`). Builder MUST use R1's corrected paths in the task file, not research-notes.md's paths. Risk if missed: executor creates a `commands/sc/` subdir that doesn't exist in source-of-truth and breaks `make sync-dev`.

2. **MINOR — R2 workflow YAML lacks explicit `claude` CLI install step.** R2 §2 blueprint shows `setup-python`, `Install UV`, `Install dependencies`, then jumps to `Invoke sc:pr-bot-validate-protocol` with `claude --skill ...` invocation — but no step installs the `claude` CLI on the runner. R2 §8 flags this as a "Blocker / open question" but the blueprint YAML in §2 should also have a placeholder step. Builder must encode this as a Phase 5 checklist item.

3. **MINOR — ANTHROPIC_API_KEY secret provisioning not encoded as a checklist item.** R2 §8 says "ANTHROPIC_API_KEY secret will need to be configured in repo settings — flag for the executor to verify before workflow is enabled." Builder should add an explicit pre-flight item in Phase 1 or Phase 5 to verify/create this secret in IronClaude repo settings (manual gh CLI step or operator verification).

4. **MINOR — `__init__.py` decision contradicts between research files.** research-notes.md §RECOMMENDED_OUTPUTS line 71 lists `__init__.py` as a required output. R1 §5.1 recommends OMITTING it (match primary template). Builder must pick R1's resolution and update the task file's outputs list accordingly.

5. **MINOR — Cost-profile / §15 derivation from merged §3.2 (research-notes Gap 5)** not explicitly addressed by either researcher. The merged proposal §3.2 says cost ≈ §15 T2-midpoint ÷ 6 parallel PRs ≈ 8.7 turns/PR. Neither researcher anchors this to a specific section of the new sibling skill. Builder should add a placeholder checklist item to populate §15 (Cost Profile) of the new SKILL.md per merged §3.2 derivation.

## Confidence Gate

- **Verified:** 10/10 checklist items + 10/10 spot-checks (all checked with independent tool calls)
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100% (10/10 = 100.0%)
- **Tool engagement:** Read: 5 | Bash/Grep: 3 (multi-check bash batches) | Glob: 0 | Total tool calls verifying assigned items: 8 — each bash batch validates 3-4 independent spot-checks, so effective verification count >= checklist count.

## Summary

- Checks passed: 10 / 10
- Spot-checks passed: 10 / 10
- Critical issues: 0
- Important issues: 0
- Minor issues: 5 (all enumerated above; ALL must be encoded in the task file before/during execution per zero-tolerance policy)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | MINOR | research-notes.md §EXISTING_FILES + §RECOMMENDED_OUTPUTS | Uses obsolete `commands/sc/` subdir paths; source-of-truth is flat per R1 §0 | Task file MUST use `src/superclaude/commands/{reflect,pr-bot-validate}.md` (no `sc/`) for ALL Edit/Write operations against IronClaude source-of-truth |
| 2 | MINOR | R2 §2 workflow YAML blueprint | No explicit `claude` CLI install step in the runner blueprint | Task file Phase 5 MUST include a dedicated checklist item: install Claude CLI on runner (pinned version) before the invocation step |
| 3 | MINOR | R2 §8 (Blocker) | ANTHROPIC_API_KEY secret provisioning is flagged but not encoded as actionable item | Task file Phase 1 MUST include an operator pre-flight item to verify/create the `ANTHROPIC_API_KEY` secret in IronClaude repo settings before workflow is enabled |
| 4 | MINOR | research-notes.md §RECOMMENDED_OUTPUTS L71 vs R1 §5.1 | research-notes lists `__init__.py` as required; R1 recommends OMITTING | Task file MUST adopt R1's resolution (omit `__init__.py`) and explicitly NOT list it in outputs |
| 5 | MINOR | Both research files | research-notes Gap 5 (cost-profile §15 derivation from merged §3.2 ≈ 8.7 turns/PR) not explicitly anchored to a SKILL.md §15 section | Task file Phase 2 MUST include a checklist item to populate §15 (Cost Profile) of the new SKILL.md per merged §3.2 derivation |

## Actions Taken

None — `fix_authorization: false`. All issues documented; no in-place edits.

## Recommendations

- Builder MUST encode all 5 MINOR issues as concrete checklist items in the task file before the task is ready to execute. Per research-gate FAIL-on-ANY-gap policy, this gate is FAIL until builder confirms encoding.
- Substance is sound otherwise — research is dense, evidence-based, and structurally complete. R1's corrections (flat `commands/` path; `## Related Commands` lives in command file not SKILL.md §16) are correct and load-bearing.
- Strong recommendation: build Phase 2 (skill scaffold) incrementally — multi-thousand-line SKILL.md is the highest-risk artifact; one-shot write WILL truncate at output-token limits.

## QA Complete

**VERDICT: FAIL** (5 MINOR issues — all must be resolved before task-file execution per zero-tolerance policy). Substance is sound; failures are mechanical encoding gaps the builder must fix in the produced task file.

