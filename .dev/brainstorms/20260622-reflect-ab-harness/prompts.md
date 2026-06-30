# Reflect A/B Harness — paste-ready prompts (BLINDED / role-split)

Read `blinding-protocol.md` first. Roles: **Builder knows · Auditor blind · Scorer knows.**

Canonical paths:
- DESIGN = `/config/workspace/IronClaude/.dev/brainstorms/20260622-reflect-ab-harness/`
- EXP    = `/config/workspace/IronClaude/.dev/experiments/reflect-ab/`
- BRANCH = `exp/reflect-ab` ; frozen base SHA → `EXP/base.sha` ; task file path → `EXP/task-path.txt`

Order: Prompt 1 (once) → then the inference arm (5× Prompt 2A in fresh chats, then Prompt 2B once) and the cli arm (Prompt 3 once) in either order.

---

## PROMPT 1 — Builder (knows everything): build + execute to the gate, freeze a clean sample (+ nested diagnostic)

```
Read /config/workspace/IronClaude/.dev/brainstorms/20260622-reflect-ab-harness/design.md, blinding-protocol.md, report-template.md, scoring-framework.md first.

GOAL: produce a frozen, ground-truthed 10-file sample for repeated reflect POST-gate runs, with NO experiment/meta leakage into the audited artifacts, plus a one-shot nested fan-out diagnostic.

1. /task-builder builds an MDTM task under /config/workspace/IronClaude/.dev/experiments/reflect-ab/sample-task/ with POST_REFLECT_GATE: ENABLED in DEFAULT skill mode (no --cli). Deliverable = the 10-file mini-package in design.md §2 under EXP/sample/ (EXP=/config/workspace/IronClaude/.dev/experiments/reflect-ab/), each planted deviation implemented EXACTLY (the flaws ARE the deliverable; executor must NOT fix divide(), NOT remove unmapped fns). The "Authorized expansion" item explicitly approves file #8's extra feature. Set start_commit frontmatter = pre-execution HEAD.
2. REALISM RULE: plants must be as subtle as real production defects — NO giveaway names/comments (no `drift_helper`, no `# intentional bug`, no "test"/"reflect"/"experiment" anywhere in sample/ or the task body). The task must read like a normal feature task and the sample like normal code.
3. Author EXP/ground-truth.yaml OUTSIDE EXP/sample/ (auditors never see it): {id,file,line,class,severity,detect_signal} per plant. Write EXP/prereg.md: the outcome you EXPECT and the decision rule, before any run.
4. Branch exp/reflect-ab off master. start_commit=`git rev-parse HEAD` BEFORE sample work → EXP/base.sha. Task path → EXP/task-path.txt.
5. Run /task TOP-LEVEL, executing every item UP TO BUT NOT INCLUDING the post_reflect_gate item (leave gate + Done unchecked).
6. LEAK-SCAN GATE (must pass before freezing): `grep -riE 'experiment|ground.?truth|planted|reflect|inference|cli|drift|regression test|for testing|fan.?out' <task-file> EXP/sample/` must return nothing meta. Fix any leak, then commit ONLY EXP/sample/ + the task file on exp/reflect-ab → EXP/sample.sha. This frozen commit is the shared input.
7. NESTED DIAGNOSTIC (isolated): `git worktree add /config/workspace/IronClaude/.dev/worktrees/reflect-ab-diag exp/reflect-ab`; there, run /task continuing into the post_reflect_gate item ONLY (skill-mode gate). Record whether the POST subagent spawns ≥2 reviewer cards on disk (fanned-out) or degrades to a single-agent/fixture, with evidence (card count, tier) → EXP/diagnostic-nested.md. Remove that worktree.
8. Report existence of EXP/{base.sha,sample.sha,task-path.txt,ground-truth.yaml,prereg.md,sample/,diagnostic-nested.md} and print the nested verdict.

CONSTRAINTS: edits under EXP/ only; never stage .claude/; do not run any gate on the frozen sample except the step-7 diagnostic.
```

---

## PROMPT 2A — Inference AUDITOR (BLIND). Paste into a FRESH chat once per run, i = 01..05.

> Contains the reflect command and nothing else. Do NOT add context. base/task come from two
> files that reveal only a SHA and a path. Replace <i> with 01..05.

```
Read the single-line value in /config/workspace/IronClaude/.dev/experiments/reflect-ab/base.sha (call it BASE) and the single-line path in /config/workspace/IronClaude/.dev/experiments/reflect-ab/task-path.txt (call it TASK). Then:
  git worktree add /config/workspace/IronClaude/.dev/worktrees/reflect-ab-inf-<i> exp/reflect-ab
From that worktree, run TOP-LEVEL and let it complete:
  /sc:reflect --mode post --diff BASE..HEAD --tasklist TASK --depth deep --no-promote --output /config/workspace/IronClaude/.dev/experiments/reflect-ab/runs/inference-<i>
When it finishes, print ONLY the absolute output dir path. Do not summarize, grade, or open any other files.
```

## PROMPT 2B — Inference SCORER (knows ground truth). One chat, after all 5 runs.

```
Read /config/workspace/IronClaude/.dev/brainstorms/20260622-reflect-ab-harness/{report-template.md,scoring-framework.md} and /config/workspace/IronClaude/.dev/experiments/reflect-ab/ground-truth.yaml.
Spawn ONE read-only sub-agent (Task) to score the inference arm:
  For i in 01..05: read runs/inference-<i>/return-contract.yaml + REPORT.md, count runs/inference-<i>/reviewer-cards|reviewer-briefs/*.md (fanned_out, degraded_to_fixture), and re-read each cited file:line to set citation_resolves; write runs/inference-<i>/run-report.md from report-template.md (pure transcription + mechanical re-read — the auditor never did this).
  Then match every reported deviation against ground-truth.yaml and compute G1–G9, Q_run, and consistency index C exactly per scoring-framework.md → WRITE runs/inference/matrix.md and runs/inference/scorecard.md.
NEUTRALITY: emit metrics only. Do NOT recommend flip-vs-keep, do NOT mention HD-1. If consistency C is suspiciously high (≈1.0 set-stability), note possible residual leakage and recommend re-checking blinding. Print the scorecard headline.
```

---

## PROMPT 3 — CLI arm: AUDITOR is a subprocess (already blind) → one prompt runs 5× + spawns SCORER

> Safe as a single prompt because each `superclaude reflect run` audits inside an isolated
> `claude --print` subprocess; the orchestrating session's knowledge cannot reach it.

```
Read /config/workspace/IronClaude/.dev/experiments/reflect-ab/{base.sha,task-path.txt} (BASE, TASK).
For i in 01..05:
  git worktree add /config/workspace/IronClaude/.dev/worktrees/reflect-ab-cli-<i> exp/reflect-ab
  From that worktree (single line): env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE superclaude reflect run TASK --base BASE --depth deep --no-promote --no-fix --output /config/workspace/IronClaude/.dev/experiments/reflect-ab/runs/cli-<i>
  Record the CLI exit code (0/10/11/2) for that run.
After all 5: read /config/workspace/IronClaude/.dev/brainstorms/20260622-reflect-ab-harness/{report-template.md,scoring-framework.md} + EXP/ground-truth.yaml, then spawn ONE read-only scoring sub-agent (Task):
  For i in 01..05: build runs/cli-<i>/run-report.md from the run's return-contract.yaml + REPORT.md (reviewer-card count, mechanical citation re-read, verdict, exit code); match vs ground-truth.yaml; compute G1–G9, Q_run, C → WRITE runs/cli/matrix.md and runs/cli/scorecard.md.
NEUTRALITY: metrics only; no flip-vs-keep, no HD-1 mention.
FINALLY, if runs/inference/scorecard.md exists, the scoring sub-agent also writes runs/comparison.md: per-metric cli−inference deltas ONLY (no recommendation). Print both headlines.
```

---

### What changed vs the first draft (and why)
- Inference auditor is now a **blind fresh-chat unit** (Prompt 2A) — reflect runs in-session, so the only safe blinding is an isolated chat containing just the command. The old "run 5× in one session that read design.md" fed the plant table into the auditor's context.
- **All grading moved to a separate scorer** (2B / Prompt 3's subagent) — the only role that opens `ground-truth.yaml`. Auditors produce raw artifacts only.
- CLI stays one orchestrated prompt — subprocess isolation makes the orchestrator's knowledge harmless.
- Scoring is **neutral** (no HD-1 / flip-vs-keep); interpretation is a separate human step against `EXP/prereg.md`.
- Prompt 1 gained a **realism rule + leak-scan gate + pre-registration** so the audited task/sample carry no meta tells.
