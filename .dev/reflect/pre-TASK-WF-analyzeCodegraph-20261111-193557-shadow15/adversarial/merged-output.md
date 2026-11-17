<!-- Provenance: This document was produced by /sc:adversarial (Mode A, depth standard, compact single-agent execution) -->
<!-- Base: Variant 2 (qa / haiku / claude-haiku-5-5), combined score 0.816 -->
<!-- Merge date: 2026-11-13 -->
<!-- Adjudication note: analyze.md evolved after this package executed. Execution commit: 7764bb623 (PR #511). Post-execution: 930c5ebc8 (PR #513 wording tightening; added Discover path/symbolsOnly/search-restriction elaborations, the 60s-wait clause, the graph:empty/graph:unresolved tail) and PR #515 (mcp grants; no analyze.md change). Findings citing current-HEAD-only text were judged as post-execution evolution, not executor drift. -->

# Merged reflect-pre findings card — TASK-WF-analyzeCodegraph-20261111-193557 (shadow15)

persona: merged (analyzer + qa + refactorer) | mode: pre (UC-1) | depth: standard | convergence: 1.00 (compact single-agent debate; see debate-transcript.md metadata)

## Findings block

```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"R7's file-mode ban (no codegraph_node file mode without symbolsOnly:true) and the wildcard-allowlist ban appear in no tasklist AC; the tasklist pins symbolsOnly:true only as Scan usage text, so a later edit adding node file-mode elsewhere passes every check.","refs":["R7"],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":17,"line_end":17,"quote":"no `codegraph_node` file mode without `symbolsOnly:true`, no wildcard allowlist."},{"role":"plan","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md","line_start":33,"line_end":34}],"provenance":"V1-F1 (primary, C-001 winner 85%) + V2-F2 clause (corroboration); recurrence family per t1-card H1 (shadow06/shadow10)"}
{"id":"F2","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"R2 gates all lookup use on fresh AND access: mcp, but Tasks 1-2 and every AC name only index_state: fresh; the access: mcp half is enforced by no AC even though the shipped file (7764bb623) carries it.","refs":["R2"],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":12,"line_end":12},{"role":"plan","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md","line_start":43,"line_end":44}],"provenance":"V1-F3 (C-005 winner 85%); third instance of the F1 family in this package"}
{"id":"F3","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Spec 2.4 items 3 and 6 (graph rows are leads not citations; subagent briefs carry index_state) and the ~25-line section cap (spec section 4) are carried by Task 1/2 body text but by no AC; V2's original 'no visible matrix row' clause was refuted (t1-card INF-012 maps them).","refs":["R2"],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":43,"line_end":46,"quote":"Graph rows are leads, never citations"},{"role":"spec","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md","line_start":63,"line_end":63},{"role":"plan","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md","line_start":29,"line_end":34}],"provenance":"V2-F1 re-scoped (X-002 refutation of matrix clause) + V2-F2 residue (25-line cap); AC-level gap only"}
{"id":"F4","severity":"MINOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"Task 3 ACs carry escape clauses: verify-sync failures may be attributed to other sessions' files, and pytest failures 'not caused by' analyze.md are reported and left unfixed, so neither AC can mechanically fail.","refs":[],"citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md","line_start":56,"line_end":57,"quote":"any failure not caused by `src/superclaude/commands/analyze.md` is reported as such and left unfixed"}],"provenance":"V2-F3 verbatim (C-004 winner 90%, unanimous adoption); 'test set unnamed' clause re-scoped per INV-004 (Task 3 body defines the discovery procedure)"}
{"id":"F5","severity":"MINOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"Task 2 AC2 requires byte-identity 'apart from the intended additions' with no bound on what is intended, so the executor defines the exception set post hoc and the check cannot fail.","refs":["R5"],"citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md","line_start":44,"line_end":44,"quote":"apart from the intended additions"}],"provenance":"V2-F4 verbatim (C-004 winner 90%, unanimous adoption; highest-confidence finding of the debate)"}
{"id":"F6","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"Guide section 7 claims to be the only section naming the forbidden verbs, but analyze.md line 68 restates init/index/sync/explore/context, creating a two-site rule: a guide edit to that list must be mirrored in the command or they drift.","refs":["INF-005","INF-012"],"citations":[{"role":"plan","path":"src/superclaude/commands/analyze.md","line_start":68,"line_end":68,"quote":"never run `codegraph init`, `index`, `sync`, `explore` or `context`"},{"role":"spec","path":"src/superclaude/core/CODEGRAPH.md","line_start":87,"line_end":89,"quote":"The only section that names these:"}],"provenance":"V3-F1 (C-006 winner 75%); verified at both HEAD and execution commit 7764bb623"}
{"id":"F7","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"The Codegraph section's Leads bullet met the 25-line budget only by packing several rules into one long line; at the execution commit it already carried four rules partly duplicating guide sections 3 and 5, harming maintainability.","refs":["INF-012"],"citations":[{"role":"plan","path":"src/superclaude/commands/analyze.md","line_start":67,"line_end":67,"quote":"a caller list shorter than its total is `graph:truncated`"},{"role":"spec","path":"src/superclaude/core/CODEGRAPH.md","line_start":58,"line_end":64}],"provenance":"V3-F3 reduced scope (75%->reduced; PR #513 later extended this bullet with graph:empty/graph:unresolved, not attributable to this package); weakest finding, confidence 0.55"}
```

<!-- Source: Base (Variant 2) — F4, F5 kept verbatim; F1 re-scoped; F2 unbundled -->
<!-- Source: Variant 1 (analyzer) — F1, F2 incorporated per Changes 1-2 -->
<!-- Source: Variant 3 (refactorer) — F6 incorporated per Change 6; F7 reduced-scope per Change 7 -->

calibration:
  per_finding:
    F1: 0.65
    F2: 0.55
    F3: 0.6
    F4: 0.75
    F5: 0.7
    F6: 0.8
    F7: 0.55

calibration provenance: F1 = max(V1-F1 0.6, V2-F2 0.65) + cross-model corroboration uplift (+0.05, capped at family confidence); F2 = V1-F3 0.55 unchanged (single-source); F3 = V2-F1 0.6 / V2-F2 0.65 blended down to 0.6 for the refuted matrix clause (X-002); F4 = V2-F3 0.75 unchanged; F5 = V2-F4 0.7 unchanged; F6 = V3-F1 0.8 unchanged (verified at both commits); F7 = V3-F3 0.6 reduced to 0.55 for the post-#513 contamination of the current text.

## Refuted findings (recorded, not carried)

| Original | Refutation | Evidence |
|----------|-----------|----------|
| V1-F2 "Discover is mild unplanned elaboration" | Misattribution: at execution commit 7764bb623, Discover read exactly `codegraph_files {format:"grouped", maxDepth:2}` + `codegraph_search` per the tasklist; the `path` param, symbolsOnly-on-main-files and search-only-when-symbol restrictions all landed in 930c5ebc8 (PR #513, separate package). | `git diff 7764bb623 930c5ebc8 -- src/superclaude/commands/analyze.md` (Run this session) |
| V2-F1 clause "no visible matrix row" | Vantage artifact: the full t1-card matrix (INF-012) maps source.md:38-46 — containing §2.4 items 3 and 6 — to Task 1, matched, containment. Reviewer 2's brief excerpted only the matrix summary. AC-level half survives as merged F3. | t1-card.md:22; reviewer-briefs/reviewer-2.md:5-16 |
| V2-F2 clause "return-contract.yaml unchanged has no AC" | Transitively gated: Task 2 AC2 requires `## Unattended mode` byte-identical to HEAD; the return-contract wording lives inside that section. | TASK file line 44; analyze.md:112 |
| V3-F2 "60s wait stated unconditionally, dropping pgrep condition" | Misattribution: the 60s clause did not exist at 7764bb623 (PR #513 added it); and at HEAD the text says "(guide step 3)", explicitly pointing at the section carrying the pgrep condition. | `git show 7764bb623:...analyze.md` line 30 vs HEAD line 30 |

## Post-merge validation

- Structural integrity: findings-v2 block holds 7 findings, one JSON object per line, every required field present (id, severity, blocking, category, lens, claim <=300 chars, refs, citations with path/line_start/line_end, provenance). Document starts at H1; no heading-level gaps. PASS
- Claims length check: longest claim (F1) = 278 chars. PASS
- References: all 13 citation targets verified by Read this session (spec source.md, tasklist, analyze.md at HEAD; analyze.md and CODEGRAPH.md at execution state via git). F1 cites tasklist lines 33-34 (Task 1 AC block) — the AC-absence claim is over that block plus Task 2's; the citation is the closest anchor. PASS
- Contradiction re-scan: no new contradictions introduced. F3's claim text explicitly records its own refuted sub-clause as refuted, consistent with the refutation table. PASS
