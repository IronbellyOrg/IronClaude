---
title: "PRD pipeline — document-step gate failures (output capture + contamination)"
type: bug
status: success
tier_reached: 2
confidence: 0.95
escalation_reason: forced_by_depth_deep
created: 2026-06-05
repo: IronbellyOrg/IronClaude @ master (SuperClaude v4.2.0)
---

# REPORT — `superclaude prd run` document steps fail their line-count gates

## Summary

Every document-producing step of `superclaude prd run` (`scope-discovery`, `research-notes`, …) fails its line-count gate even though the agent's underlying work is high quality. The agent writes its real document to disk at a path the executor doesn't look in, so the pipeline's gate evaluates the ~24-line NDJSON *commentary* instead of the real ~200-line document. `scope-discovery` (STANDARD gate) logs `validation_fail` and continues degraded; `research-notes` (STRICT gate) then halts the run. A second, compounding defect: when the parsed `WHERE` points at a writable source dir (`.dev/specs/`), agents write their outputs *into* it, and later steps ingest those generated files as if they were source specs — a contamination loop.

This was reproduced across two independent runs and root-caused directly in source (confidence 0.95). Three competing fixes have been developed for debate (see Proposed Fix).

## Diagnosis (root cause)

The recovery mechanism that is *supposed* to find the agent's written document fails on two independent mismatches:

1. **Filename mismatch.** `_resolve_step_content` (executor.py:266-365) recovers a step's output by `rglob`-ing the **exact** canonical filename from `_STEP_ARTIFACT_FILES` (executor.py:252-263) — for scope-discovery that is `scope-discovery-raw.md`. The step prompt only says *"Write a markdown document with these sections"* (prompts.py ~:156) with **no pinned path or filename**, so the agent invented `scope-discovery.md` (no `-raw`). `rglob("scope-discovery-raw.md")` never matches `scope-discovery.md`.

2. **Location mismatch.** The recovery search roots are only `task_dir` and `task_dir.parent` (executor.py:345-349). The agent wrote to `.dev/specs/` — outside that tree — because the parsed `WHERE` directed scope work there. Even `research-notes` (whose canonical name `research-notes.md` *does* match what the agent wrote) was missed purely on location.

With both misses, `_resolve_step_content` falls back to `ndjson_text` (executor.py:365) — the assistant's commentary, which the code itself documents as *"only … the assistant's commentary"* (executor.py:271). The gate counts those ~24 lines.

**Cascade:** `build_research_notes_prompt` reads `config.task_dir / "scope-discovery-raw.md"` (prompts.py, research-notes builder ~:196) — i.e. the thin recovered artifact — so research-notes is also built on degraded input, then its STRICT gate (min_lines=100) halts the pipeline.

**Why `assembly` doesn't hit this:** the `assembly` step has a bespoke robust recovery (executor.py:309-336) that searches `[task_dir/results, task_dir, task_dir.parent]` for `*.md` containing "prd". The document steps lack an equivalent — they rely on brittle exact-name matching.

**Contamination (second defect):** nothing isolates the subprocess working context from the writable `WHERE` dirs, so agents treat `.dev/specs/` as scratch space and write step outputs there ("wrote to `.dev/specs/research-notes.md` for consistency with the existing scope-discovery.md"). Subsequent steps re-read those generated files as source material.

## Evidence (cited, verified against source this session)

- `_STEP_ARTIFACT_FILES` static canonical names — `executor.py:252-263` (`scope-discovery` → `scope-discovery-raw.md`).
- Exact-name rglob over `task_dir` + `task_dir.parent`, NDJSON fallback — `executor.py:339-365`.
- Code's own admission stdout is commentary-only — `executor.py:266-278`.
- Robust contrast pattern (assembly) — `executor.py:309-336`.
- Subprocess output captured to `{step_id}-output.txt`, read back as `raw_output` — `executor.py:580-605`; artifact persisted via `_persist_step_artifact` — `executor.py:1149-1166`.
- Subprocess launched with `output_format="stream-json"` — `process.py:159`.
- scope-discovery prompt: "Write a markdown document …", no pinned path — `prompts.py ~:143-156` (`build_scope_discovery_prompt`).
- research-notes prompt reads `task_dir/scope-discovery-raw.md`; "Produce a research-notes.md file" with no dir — `prompts.py ~:194-210`.
- Gates: `scope-discovery` min_lines=50 STANDARD — `gates.py:323-328`; `research-notes` min_lines=100 STRICT + frontmatter[Date,Scenario,Tier] + semantic section checks — `gates.py:329-345`.
- Live reproduction artifacts (Octodive run): captured 24-line `scope-discovery-raw.md` vs the agent's real 197-line doc preserved at `/config/workspace/Octodive/.dev/releases/scp-run/recovered-artifacts/scope-discovery.md`; gate log `"Min lines: 25/50"` then `"Min lines: 24/100"` (research-notes, result=halt) in `/config/workspace/Octodive/.dev/releases/scp-run/prd-octodive/execution-log.jsonl`.

## Proposed Fix — three competing approaches (for debate)

A deep solution-development pass produced three distinct, self-contained designs. Each is a standalone doc in this directory:

| # | Approach | File | Fixes capture? | Fixes contamination? | Blast radius |
|---|----------|------|----------------|----------------------|--------------|
| 1 | Executor-side robust recovery (flexible glob + broader roots + tiebreak) | `solution-1-executor-recovery.md` | Yes (after-the-fact) | No (recovers, doesn't prevent) | Low (1 function) |
| 2 | Prompt-side path pinning (agent writes to `task_dir/<canonical>`) | `solution-2-prompt-path-pinning.md` | Yes (at source) | Yes (output leaves `.dev/specs`) | Low–med (prompt builders + shared helper) |
| 3 | Stdout/result-contract capture (+ cwd isolation) | `solution-3-stdout-contract.md` | Yes (reliable channel) | Yes (cwd=task_dir) | High (shared capture path, all 15 steps) |

**Recommendation (non-binding — this is for your debate):** Solutions **2 + 1 combined** — pin the output path in the prompts (Solution 2) to fix capture *and* contamination at the source, and harden `_resolve_step_content` (Solution 1) as a defense-in-depth backstop for agent non-compliance. This pairs the lowest-risk fixes and covers each other's primary weakness (Sol 2's reliance on agent compliance ↔ Sol 1's backstop recovery). Solution 3 is the most architecturally correct but carries the widest blast radius (touches every step's capture, incl. parse-request JSON and the 800-line assembly PRD) — better as a follow-up than a hotfix.

## Alternative fixes considered (one-line each)

- **Solution 1 only** — recovers but never stops `.dev/specs` pollution; risk of selecting a stale longer file from a prior run.
- **Solution 2 only** — clean at the source but depends on agent compliance with the pinned path; no backstop if the agent deviates.
- **Solution 3 only** — most correct contract, but a regression here breaks *every* step's capture; needs feature-flagged rollout + full 15-step test matrix.

## Risk + rollback

- All three are additive to a pre-build pipeline; rollback = revert the touched function(s)/prompt strings.
- Source-of-truth discipline (IronClaude CLAUDE.md): implement in `src/superclaude/cli/prd/`, then `make sync-dev` && `make verify-sync`; never edit the installed venv copy.
- Verify with `uv run pytest tests/cli/prd/` (relevant: `test_resolve_step_content.py`, `test_executor.py`, `test_gates.py`, `test_prompts.py`, `test_prompt_builders_dual_mode.py`, `test_e2e.py`).

## Next steps

1. Debate the three solution docs (they are written for exactly this).
2. To turn the chosen approach into an executable task, re-invoke with `--fix` (Tier 3 builds an MDTM task file you run via `/task`).
3. Independent of the fix: this defect blocks the original octodive PRD-comparison goal — once fixed, re-run `superclaude prd run` (with `--output` a clean dir, not a `.md`) to produce a clean `PRD_octodive.md` for the `/sc:adversarial` compare.
