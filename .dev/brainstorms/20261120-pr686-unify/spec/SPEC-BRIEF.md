# Brief for the spec author

Write ONE specification: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md`. Title: "Unification spec: issue watcher, coordinator, dashboard and issue-claim-to-work pipeline". It states the local changes, the pull request dispositions (including reverts) and the other course corrections that remove the conflicts between the repository owner's line of work (login `ironbelly`, "OURS") and Clay's line (login `clayphi`, they/them, "CLAY"), and unifies the effort. It is a SPEC, not a plan of action: nothing in it is executed by the author or by this exercise.

## Inputs (read ALL of them in full before writing)
- Debate verdicts (binding decisions): /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/{D01..D16,Q01,Q02,Q03,QG1,QG2,QG3,QG4}/VERDICT.md. Owner order: the owner's line takes precedence; Clay's clearly better separable elements are folded in. A verdict is binding unless two verdicts contradict, in which case follow the resolution in /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/DECISIONS.md section "Where verdicts disagree" (20 contradictions; D15 resolved 7; for the rest pick one with a reason and state it in the spec's "Resolved contradictions" section: every one of the 20 must appear).
- The decision record: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/DECISIONS.md (owner actions section too).
- The unified design from the brainstorm: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/ (find the merged output and return contract; read the whole folder's merged document). If a brainstorm statement contradicts a debate verdict, the verdict wins; list it.
- Facts about what exists: techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md and techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md (same folder tree), inventory/clay-prs.md, and the earlier analysis /home/coder/workspaces/IronClaude/.dev/analyze/pr686-20261120/FULL-REPORT.md.
- Code (read-only exports): /home/coder/.cache/ic-snap-20261120/{master,pr-a,pr-p}. The owner's local, unpushed work lives in the worktree /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb (branch ironbelly/issue-watcher-zero-setup-plan; requirements at .dev/releases/backlog/issue-watcher-zero-setup/requirements.md). Read it; do not edit it. The state of its `/sc:implement` run is UNCLEAR (a progress log says "FINAL: pass", D14 and D15 say half-finished): state that it must be re-checked before the revert sequence starts.

## Required structure (use these headings, in this order)
1. `# Unification spec` header block: status DRAFT for spec-panel review, date 2026-11-20, owner `ironbelly`, sources.
2. `## 1. Purpose, scope and non-goals`. Include "built today" versus "not built" (separate what RUNS, what is STUBBED, what is NOT BUILT).
3. `## 2. Binding decisions` : a table `ID | decision | winner | source verdict | confidence`, one row per verdict entry (all 32 entries in DECISIONS.md).
4. `## 3. Target architecture` : plain-English description and a diagram (ASCII) of watcher, coordinator, dashboard and claim-to-work pipeline, with the interface table (files, verbs, names, schemas, who writes, who reads). Use the names the debates fixed: role "coordinator", command `/sc:coordinator`, session `COORD-<RepoName>`.
5. `## 4. Requirements` : numbered requirements `FR-nn` (functional), `NFR-nn`, `SEC-nn` (safety), each testable: "shall" sentence, the acceptance check (a command, test or observable), the source verdict, and the component. Group by: 4.1 watcher, 4.2 coordinator, 4.3 dashboard and observability, 4.4 claim-to-work pipeline, 4.5 authority and grants, 4.6 names and migration, 4.7 process and governance.
6. `## 5. Local changes` : a table of changes to make locally (files, what, which requirement, order), including what happens to the owner's local branch and what must be re-checked.
7. `## 6. Pull request and branch dispositions` : EVERY Clay PR and branch in the inventory and every open owner PR touched (686, 687, 689, 690, 693, 685, 683, 684, 682, 681, 661, 670 and the 6.x removal PRs), each with KEEP / KEEP-ADAPT / REVERT / CLOSE / DRAFT, the reason (verdict ID), preconditions, exact steps as a recommendation (for a revert: which commit, one new PR, which hand-applied fixes such as the "no `--to`" bullet), and the order. State that none is executed by this spec's author.
8. `## 7. Clay strengths adopted` : the D15 table condensed (adopt / adopt with change / defer / reject, carrier, order) with the merge or override strategy.
9. `## 8. Staged migration` : stages S0, S1, ... each with scope, preconditions, deliverables, tests, rollback, owner gate, and the PR lane. S0 is "owner decides in chat and holds the open PRs".
10. `## 9. Course corrections (process)` : the D16 package, costed, in order, marking admin-only items.
11. `## 10. Owner actions` : every action only the owner can take (chat confirmations, admin settings, token rotation), de-duplicated.
12. `## 11. Resolved contradictions` : all 20 from DECISIONS.md, each: the two verdicts, the choice, the reason.
13. `## 12. Risks, unverified items and open points` : each risk with a mitigation; every UNVERIFIED item from the verdicts that a requirement leans on, with the check that would settle it.
14. `## 13. Acceptance and test plan` : how each stage is shown to work (tests named by path where the tests exist, otherwise as to-be-written), including the live firing tests the verdicts require (precheck test, guard probe, worker binding).
15. `## Appendix A. Traceability` : requirement -> verdict -> source file.

## Rules
- Facts only from the inputs or from reading the code; mark UNVERIFIED anything else. Cite file paths with line numbers where a requirement depends on code.
- Every PR or issue number is followed by a few words saying what it is the first time it appears in each section.
- No em dashes or en dash ranges. Plain English; define each internal term once.
- Do not invent requirements without a source: a requirement without a verdict or code source is tagged `NEW (author)` and listed in section 12.
- Do not execute anything: no git write, no GitHub or Orca write, no edits outside the spec folder. Read-only on the repository, snapshots and worktrees. Any read-only `gh` call passes `--repo IronbellyOrg/IronClaude`.
- Create SPEC.md as a header stub with every heading and placeholders first, then fill each section in place (do not write it from memory in one go). A report that leaves a placeholder fails its gate.
- When finished, return only the path and a five-line summary (requirement count, PR rows, stages, contradictions covered, anything you could not resolve).
