# Reviewer brief (common part): sc:reflect UC-1 pre-execution, run 4, Tier 2

You are one of three heterogeneous, independent reviewers. You are READ-ONLY (Read, Grep, Glob and code-search tools; no Bash, Edit, Write). You cannot write files: return your complete card as your final message in the format below. Assume the plan is wrong until the files prove otherwise. Do not trust any summary, earlier verdict or sign-off; run 3's findings are CLAIMS to verify, not facts. Do not coordinate with the other reviewers.

Repository root: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode. Shorthand: P=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653; R1=P/revisions/chat-output-exception-20261109-133150; R2=P/revisions/plan-defect-fixes-20261110; TL=P/TASK-RF-sweep-phase1-20261108-072653.md (the plan under review, 3020 lines, 355 items, sha256 eb291f0bdd1a787131a3b5295150b0f109b46943a1c43c638fd2ad4652d29f99); DESIGN=docs/designs/orchestrator-mode.md (the spec, 1051 lines, frozen, sha256 e4a06d0c...); ADD=R1/design-addendum.md (resolved normative addendum); STYLE=src/superclaude/output-styles/pragmatic.md; BASE=R2/baseline/task-before-rev2.md (the plan before the edits).

## What is being reviewed

The plan (TL) was edited a second time (revision R2, owner-authorized "Fix the plan first"): 73 changed lines in 64 of 85 allowed unfinished items, each edit line-stable (line count 3020 before and after; only Context/Action/Output/Verification/Completion-gate lines of unfinished items). `diff BASE TL` shows every change. The intent of the edits is in R2/BUILD-REQUEST.md (ten-fix table) and R2/delta-manifest.md; R2/qa/preservation-check.json is the machine check of scope. Authoritative text of the ten defects and their recommended fixes: R1/reflect/pre/adversarial/merged-verdict.yaml (F-01..F-10) and R1/reflect/pre/adversarial/invariant-probe.md (INV-001..INV-026). Three earlier R2 gates passed with only MINOR notes: R2/qa/A10-verify1.md (structural), R2/qa/qa-task-research-alignment-report.md, R2/qa/qa-qualitative-operational-report.md and R2/qa/qa-qualitative-sufficiency-report.md. Do NOT repeat their findings; look for what they missed, and judge whether any of their MINOR notes (N-1..N-8, M-1..M-7) is really blocking in a correct run.

The coverage matrix R2/reflect/pre/coverage-matrix.yaml (127 parsed + 77 inferred requirements, coverage 1.0 parsed / 0.985 union) was rebuilt mechanically and is identical to run 3's.

## Key question

Will the EDITED plan, if executed in order, deliver the spec (DESIGN plus ADD) without self-deadlock, lost checks, weakened QA or invented work? Two sub-questions: (a) is each of F-01..F-10 fixed correctly and completely; (b) do the 73 changed lines introduce a NEW defect (a check that fails on a correct run, a check with no expected value, a contradiction between items, an instruction the executor cannot follow, a weakened gate, or text that misstates the spec).

## Rules for findings

- Severity: HIGH = a correct run fails or a required check is lost; MEDIUM = real impact with a workaround; LOW = minor. Do not inflate; do not invent findings to meet a quota. If you find nothing in your lens, show in a Self-Audit what you checked.
- Every finding needs: id (your prefix + number), severity, tag `Grounded` or `[INFERRED]`, a one-sentence claim, evidence as `path:line` plus a VERBATIM quote of the cited line(s) (quotes are re-read mechanically; a quote that does not match its cited range is dropped), the smallest fix, and a one-line verifier (a command or check with its expected value).
- Cite lines as TL:<n>, DESIGN:<n>, ADD:<n>, STYLE:<n>, BASE:<n>, or a full path with line.
- A finding that is only a MINOR already listed in the R2 qa reports counts only if you show it is blocking.

## Return format (your final message, exact)

```
# Reviewer card
reviewer: <n>   persona: <name>   model: <your actual model name>
findings:
- id: <R?-F1>  severity: <HIGH|MEDIUM|LOW>  tag: <Grounded|[INFERRED]>
  claim: <one sentence>
  evidence:
    - ref: <TL:123>   quote: "<verbatim>"
  fix: <smallest fix>
  verifier: <command or check with expected value>
f_closure:   # one line per run-3 finding
  F-01: <fixed|partial|not fixed|fixed with new defect> - <one sentence + ref>
  ... F-10
self_audit: <what you actively checked, what you could not check>
confidence: <0.00-1.00 self-reported>
```
