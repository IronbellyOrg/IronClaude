# Deep Troubleshoot Pipeline — QA/Reflect Blindspot (PR #209)

**Purpose:** BUILD-ONLY. Paste-ready prompts to run *in a fresh session* to (1) deepen the root cause beyond the 4 mechanisms already found, (2) propose concrete protocol fixes, (3) adversarially evaluate them — using the **`superclaude swarm` CLI** for the heterogeneous fan-out at every stage.

**Do not run from the current session.** Open a new Claude Code session and paste Prompt 0 (it drives the whole pipeline), or run the raw CLI commands in the Appendix.

---

## Context this pipeline builds on

Four real bugs (F1–F4) in `src/superclaude/pr_submit/contract_setup/` passed a 5-phase RF QA + a Tier-2 `/sc:reflect` audit (`verdict: pass, regression: 0`) and were caught only by Augment on PR #209. The post-mortem (`CONSOLIDATED-root-cause.md` + `agent-A..D`) found one meta-failure — **every gate measured the work against the spec or its own tests, never against external correctness** — via 4 mechanisms:
1. Cross-symbol blindspot (F1/F3) — no lens compares two code symbols to each other.
2. Tests encode the bug (F2/F4) — code+tests+QA share one mental model.
3. Spec-relative deviation taxonomy + unrun verification (`verification_ran: false`, `regression: 0` unearned).
4. Known quirk laundered into spec (F4 — the adversarial lens cited the bug as proof of correctness).

This pipeline pressure-tests those conclusions and turns them into an evaluated fix set.

## Prerequisites (state these to the fresh session)

- Repo root: `/config/workspace/IronClaude`. Branch: `docs/qa-reflect-postmortem-pr209` (PR #211) has the analysis.
- **Proxy contract — use ONLY `~/.aienv`:** `source ~/.aienv` first. Transport env: `T2ProxyUrl` / `T2ProxyKey`. Heterogeneous T2 models: `kimi-k2.7-code`, `qwen3.6-plus`, `glm-5.2`, `deepseek-v4-pro`. Never probe `:4000/v1` or query the proxy for models.
- Swarm CLI: `uv run superclaude swarm {scaffold,validate,run} …`. `run` takes a JobSpec JSON (`swarm run spec.json`) or `--lens NAME --target PATH --output DIR`. `custom` lens is rejected by scaffold — scaffold a real lens (`bare-review`) and override `prompt.*`, `target.path`, `output.dir`, `transport.kind`, `workers.{count,models}`. Drive real models with `transport.kind = "openai_compat"`.
- Key material to feed the swarm (targets): this analysis dir; the reflect audit under `.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/reflect/post/156f28292b4d/`; the QA gate prompts embedded in `…/TASK-RF-detection-contract-20260701-164700.md`; the pre-fix buggy code at `git show dc507305:src/superclaude/pr_submit/contract_setup/{diagnosis,candidate,questions}.py`.

---

## PROMPT 0 — top-level orchestration (paste this into the fresh session)

> You are running a 3-stage deep-troubleshoot pipeline over a QA/reflect process failure. Repo: `/config/workspace/IronClaude`. First `source ~/.aienv`. Read `.dev/analysis/qa-reflect-blindspot-pr209/CONSOLIDATED-root-cause.md` and `agent-A..D` for context. Use the **`superclaude swarm` CLI** (`transport.kind: openai_compat`, workers = the 4 `~/.aienv` T2 models: kimi-k2.7-code, qwen3.6-plus, glm-5.2, deepseek-v4-pro) as the heterogeneous fan-out engine at every stage. For each stage: assemble the target file, scaffold+edit a JobSpec (override prompt/target/output/transport/workers), `swarm validate` it, `swarm run` it, then read `<output>/merged.md` + the per-worker `*.final.md`. Do NOT let any worker see the spec/tests as ground truth — the whole point is spec-free correctness.
>
> **Stage 1 — deepen the root cause.** Target = concat of the 5 analysis files + the reflect `return-contract.yaml` + `t2-adversarial/reflect-review-consolidated.md` + the Phase-2/Phase-4/Step-5.3 QA gate prompts (grep them out of the task .md). Ask the swarm: "(a) find latent blindspots BEYOND the 4 named mechanisms; (b) audit whether the OTHER RF surfaces — `rf-qa`/`rf-qa-qualitative` agent briefs, `sc-tasklist`/`sc-task`/`task-builder` skills, the `reflect-reviewer` brief, the deviation taxonomy — share the same spec-anchored/tests-as-oracle patterns, with file:line; (c) rank the 4+N mechanisms by how load-bearing each is (which single fix prevents the most)." Save merged output to `.dev/analysis/qa-reflect-blindspot-pr209/pipeline/stage1-rootcause/`.
>
> **Stage 2 — design fixes.** Target = Stage-1 merged.md + the CONSOLIDATED "Prioritized additive fixes" section. Ask the swarm: "Propose concrete, ADDITIVE, implementable changes to the RF QA + `/sc:reflect` protocols that would have caught F1–F4 and the Stage-1 blindspots. For each fix: exact file/skill to edit, the new lens/check/rule text, the mechanism(s) it closes, and whether it is deterministic (static check/test) or LLM-lens. Prefer deterministic backstops where possible." Save to `…/pipeline/stage2-solutions/`.
>
> **Stage 3 — evaluate fixes.** Target = Stage-2 merged.md. Ask the swarm (adversarial): "Score each proposed fix 1–5 on: coverage (bugs prevented), false-positive/gate-thrash risk, token+time cost, implementation effort, regression risk to existing gates. Flag overlaps/conflicts. Output a minimal high-ROI subset that closes the most mechanisms for the least added gate cost, and name what it still misses." Save to `…/pipeline/stage3-eval/`.
>
> **Synthesis (you, not the swarm).** Merge Stage 1–3 into `…/pipeline/FINAL-remediation-plan.md`: ranked mechanisms, the chosen minimal fix subset with per-fix (mechanism closed / deterministic-or-lens / target file / effort), residual risk, and — if warranted — a paste-ready `rf:task-builder` BUILD_REQUEST to implement the top fixes as an MDTM task. Report the plan; do not implement.

---

## Appendix — raw swarm CLI per stage (for a no-Claude-Code run)

Run from `/config/workspace/IronClaude` after `source ~/.aienv`. Replace `<STAGE>` per stage.

```bash
# 1. assemble the stage target into one file (example: Stage 1)
mkdir -p .dev/analysis/qa-reflect-blindspot-pr209/pipeline/stage1-rootcause
T=".dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700"
cat .dev/analysis/qa-reflect-blindspot-pr209/CONSOLIDATED-root-cause.md \
    .dev/analysis/qa-reflect-blindspot-pr209/agent-?-*.md \
    "$T/reflect/post/156f28292b4d/return-contract.yaml" \
    "$T/reflect/post/156f28292b4d/t2-adversarial/reflect-review-consolidated.md" \
  > /tmp/stage1-target.md

# 2. scaffold a JobSpec (bare-review recipe) then EDIT it (see field overrides below)
uv run superclaude swarm scaffold --lens bare-review -o /tmp/stage1.json

# 3. In /tmp/stage1.json set:
#    workers.count = 4
#    workers.models = ["kimi-k2.7-code","qwen3.6-plus","glm-5.2","deepseek-v4-pro"]
#    transport.kind = "openai_compat"     (base_url_env stays T2ProxyUrl, api_key_env T2ProxyKey)
#    target.path = "/tmp/stage1-target.md"   (raise target.truncation.line_cap if the concat is long)
#    output.dir  = ".dev/analysis/qa-reflect-blindspot-pr209/pipeline/stage1-rootcause"
#    prompt.system   = "<spec-free correctness auditor system prompt — see Prompt 0 Stage 1>"
#    prompt.user_template = "<Stage-1 question>\n\n<<<TARGET>>>\n{target_content}\n<<<END TARGET>>>"
#      (keep the injection_guard.required_substring present in prompt.system)

# 4. validate + run
uv run superclaude swarm validate /tmp/stage1.json
uv run superclaude swarm run /tmp/stage1.json --transport openai_compat
#   (add --tui on a TTY to watch; --detached to background; --target-line-cap N to override truncation)

# 5. read results
cat .dev/analysis/qa-reflect-blindspot-pr209/pipeline/stage1-rootcause/merged.md
ls  .dev/analysis/qa-reflect-blindspot-pr209/pipeline/stage1-rootcause/*.final.md
```

Repeat for Stage 2 (target = stage1 `merged.md` + CONSOLIDATED fixes) and Stage 3 (target = stage2 `merged.md`), swapping `prompt.*`, `target.path`, and `output.dir`.

## Notes / gotchas (from prior swarm + reflect runs)

- **Spec-free is the point.** The reflect Tier-2 run used these SAME models and missed F1–F4 because the prompt was a spec-anchored deviation audit. Give the swarm a correctness/oracle prompt with NO spec and NO trust in the in-repo tests.
- **`--transport openai_compat` is mandatory** to reach real models; the default `stub` returns canned output (safe, but useless here). A missing `T2ProxyKey` → preflight EXIT_INVALID with an env-missing contract line on stderr.
- **Reviewer under-run is silent** — verify `merged.md` actually has 4 worker sections; a slot that produced nothing (as kimi did in the reflect run) will not always announce itself. Cross-check the per-worker `*.meta.json`.
- **Truncation:** JobSpec `target.truncation.line_cap` defaults to 4000; the Stage-1 concat may exceed it — raise it or split the target, else a worker silently reviews a truncated tail.
- **Don't commit** the raw proxy outputs blindly — machine YAML/JSON can trip the pre-commit `yamllint`; keep `pipeline/` markdown-only or exclude generated `*.json`/`*.yaml` when committing (as was done for the reflect run artifacts).
