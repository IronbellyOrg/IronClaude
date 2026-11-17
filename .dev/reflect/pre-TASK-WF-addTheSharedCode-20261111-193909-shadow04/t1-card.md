# Tier 1 Reflection Card — UC-1 pre-execution coverage audit

run: pre-TASK-WF-addTheSharedCode-20261111-193909-shadow04
spec: .dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/source.md (1 line)
tasklist: .dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/TASK-WF-addTheSharedCode-20261111-193909.md (11 tasks)
tier pin: --tier 2 (hard override, §5.1); engine: shadow (measurement-only; legacy rotation authoritative)

## Extraction summary (Step 1B.0)

- Pass 1 (ID_REGEX): 0 labeled requirement IDs (spec carries no SPEC-/T- IDs).
- Pass 2 (inference): 3 valid INF rows (each quote-pinned below).
- parsed_count=0 < inferred_count=3 → `coverage_degraded: parsed-sparse` (Step 1B.2b pre-filter; T1 stop forbidden).
- coverage_pct (parsed-only): null (0/0 parsed denominator; union fields authoritative here).

## Inferred requirements (Pass 2)

| id | verbatim quote (source.md:1) | citation |
|----|------------------------------|----------|
| INF-001 | "Add the shared codegraph rule (use codegraph only when the caller passes index_state: fresh with checked_at, worktree_root and projectPath; otherwise Grep/Glob/Read)" | source.md:1 |
| INF-002 | "to the ten general-purpose agent files listed in .dev/issues/504/issue-summary.md" | source.md:1 |
| INF-003 | "following the wording in troubleshoot-analyst.md, reflect-reviewer.md, reuse-auditor.md and auggie-reviewer.md" | source.md:1 |

## Coverage matrix (union set)

| Requirement | Tasklist coverage | Status | Grounding |
|-------------|-------------------|--------|-----------|
| INF-001 shared codegraph rule | Constraints:19 verbatim rule text; Tasks 1-10 add it per file | covered | tasklist:19,26-94 |
| INF-002 ten target files | Tasks 1-10 enumerate exactly the ten files of issue-summary.md:24 (verified: system-architect, root-cause-analyst, refactoring-expert, security-engineer, performance-engineer, python-expert, backend-architect, quality-engineer, self-review, technical-writer) | covered | tasklist:26-94; /home/coder/workspaces/IronClaude/.dev/issues/504/issue-summary.md:24 |
| INF-003 wording fidelity | Constraints:19 quotes a full rule text and claims it "is the wording of the rule in" the four reference agents | covered-with-finding (F1) | troubleshoot-analyst.md:27; reflect-reviewer.md:64; reuse-auditor.md:50; auggie-reviewer.md:79 |

Union: 3/3 mapped → coverage_pct_union: 1.0; unmapped_requirements_union: [].

## Findings

- **F1 (medium, coverage-fidelity): the wording claim is inaccurate.** Constraints:19 asserts the mandated rule text "is the wording of the rule in src/superclaude/agents/reflect-reviewer.md, reuse-auditor.md, auggie-reviewer.md and troubleshoot-analyst.md". Grounded comparison of all four files shows every one conditions codegraph use on `index_state: fresh` + `projectPath` ONLY; none mentions `checked_at` or `worktree_root`, none covers "callees and impact", and none carries "say so in your reply". The tasklist text is a stricter NEW variant (four-field gate), consistent with the spec's own parenthetical (source.md:1 names all three fields) but not with the four files. Execution risk low (Constraints text is self-contained and authoritative for an executor), but the claim is false as written and the four files cannot serve as wording precedent for the text an executor must paste.
- **F2 (low, AC strength): Tasks 1-10 acceptance criteria are grep-count based** (`grep -c codegraph` and `grep -c index_state` each ≥ 1). They do not verify the pasted text matches the Constraints rule verbatim; an executor could satisfy the AC with materially different text. Task 11's `make verify-sync` compares src/ to .claude/ mirrors (internal consistency), not against the Constraints text. Recommendation: add an exact-text check (`grep -F "<full rule sentence>"` per file) to the ACs.
- **F3 (low, spec-pointer): the spec's list source is unresolvable in this worktree.** `.dev/issues/504/` exists only in the main checkout (/home/coder/workspaces/IronClaude/.dev/issues/504/issue-summary.md:24); it is absent here. Mitigated: the tasklist enumerates the ten files inline and the enumeration matches the main-checkout list exactly, so the executor is never blocked.
- **F4 (positive): constraints match repo discipline.** No tools-line change (verified: all ten files have `tools:` count 0), no src/superclaude path references inside agent files, the four already-carrying agents and core/CODEGRAPH.md untouched, Task 11 runs `make sync-dev` + `make verify-sync` + agent-file tests per CLAUDE.md component-sync workflow.
- **F5 (note): sanctioned wording variant for technical-writer (Task 10)** — "worded to apply only when looking up a code fact"; consistent with Constraints:19 "identical in the nine engineering agents". Task 9 correctly targets self-review.md's `## How to Operate` section (verified present) in its own list style.

## Structural signals

- S_scope = 11 (tasklist items); S_domains = 2 (agent .md sources + build/sync); S_dev_density (union) = 0/3 = 0.0.
- No polymorphic surface, no runtime-surface tags, no verification run (UC-1: §6.1 steps 4b'/4b/5.5/5.6 do not fire; Bash diagnostics limited to read-only grep/survey).

## Self-assessed confidence (pre-calibration)

Citation grounding 0.9 / Coverage completeness 0.85 / Deviation-classification clarity 0.85 / Risk surface coverage 0.8 / Recommendation actionability 0.9 → mean 0.86.
