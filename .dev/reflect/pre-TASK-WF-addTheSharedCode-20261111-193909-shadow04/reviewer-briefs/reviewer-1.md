# Reviewer Brief 1 — persona: analyzer (model class: sonnet, reviewer_id t1b-1)

You are a Tier-2 reflection reviewer (UC-1, pre-execution coverage audit). Audit ONLY the evidence in this brief plus what you can Read/Grep from your grounding root (/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel). You are read-only: no edits, no writes, no shell execution. Classify every finding you report and give a confidence per finding.

## T1 card excerpt

From <output>/t1-card.md — findings section (analyzer slice):

- **F1 (medium, coverage-fidelity): the wording claim is inaccurate.** Constraints:19 asserts the mandated rule text "is the wording of the rule in src/superclaude/agents/reflect-reviewer.md, reuse-auditor.md, auggie-reviewer.md and troubleshoot-analyst.md". Grounded comparison of all four files shows every one conditions codegraph use on `index_state: fresh` + `projectPath` ONLY; none mentions `checked_at` or `worktree_root`, none covers "callees and impact", and none carries "say so in your reply". The tasklist text is a stricter NEW variant (four-field gate), consistent with the spec's own parenthetical (source.md:1 names all three fields) but not with the four files. Execution risk low (Constraints text is self-contained and authoritative for an executor), but the claim is false as written and the four files cannot serve as wording precedent for the text an executor must paste.
- **F2 (low, AC strength): Tasks 1-10 acceptance criteria are grep-count based** (`grep -c codegraph` and `grep -c index_state` each >= 1). They do not verify the pasted text matches the Constraints rule verbatim; an executor could satisfy the AC with materially different text. Task 11's `make verify-sync` compares src/ to .claude/ mirrors (internal consistency), not against the Constraints text. Recommendation: add an exact-text check (`grep -F "<full rule sentence>"` per file) to the ACs.
- **F3 (low, spec-pointer): the spec's list source is unresolvable in this worktree.** `.dev/issues/504/` exists only in the main checkout; it is absent here. Mitigated: the tasklist enumerates the ten files inline and the enumeration matches the main-checkout list exactly.
- **F4 (positive): constraints match repo discipline.** No tools-line change (verified: all ten files have `tools:` count 0), no src/superclaude path references inside agent files, the four already-carrying agents and core/CODEGRAPH.md untouched, Task 11 runs `make sync-dev` + `make verify-sync` + agent-file tests.
- **F5 (note): sanctioned wording variant for technical-writer (Task 10)** — "worded to apply only when looking up a code fact"; consistent with Constraints:19 "identical in the nine engineering agents". Task 9 correctly targets self-review.md's `## How to Operate` section (verified present) in its own list style.

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T23:57:23Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### spec: .dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/source.md:1

```text
Add the shared codegraph rule (use codegraph only when the caller passes index_state: fresh with checked_at, worktree_root and projectPath; otherwise Grep/Glob/Read) to the ten general-purpose agent files listed in .dev/issues/504/issue-summary.md, following the wording in troubleshoot-analyst.md, reflect-reviewer.md, reuse-auditor.md and auggie-reviewer.md
```

### plan: .dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/TASK-WF-addTheSharedCode-20261111-193909.md:19 (Constraints, rule text)

```markdown
- Rule text, identical in the nine engineering agents: "For symbols, callers, callees and impact use the codegraph tools per `~/.claude/CODEGRAPH.md`: only when the caller's brief says `index_state: fresh` together with `checked_at`, `worktree_root` and the `projectPath` to pass on every call, and Read every row before citing it. Otherwise use Grep, Glob and Read, and say so in your reply." It is the wording of the rule in src/superclaude/agents/reflect-reviewer.md, reuse-auditor.md, auggie-reviewer.md and troubleshoot-analyst.md.
```

### src/superclaude/agents/troubleshoot-analyst.md:27 (wording source 1)

```markdown
1. Read the actual source before making a claim. Use native search and the individually allowed read-only retrieval tools. For symbols and callers use the codegraph tools per `~/.claude/CODEGRAPH.md`: only when the brief says `index_state: fresh`, passing the brief's `projectPath`, and Read every row before citing it. When codegraph is not usable or returns nothing, use the native floor: for a symbol, Grep for its definition (`def name`, `class name`, `function name`) and Read the range; for references, Grep with a word-boundary pattern and Read the call sites. Index misses do not prove absence. Compiler, linter and type-checker diagnostics are not available to this worker; the orchestrator's verification leg covers diagnostics and supplies their captured output with provenance.
```

### src/superclaude/agents/reflect-reviewer.md:64 (wording source 2)

```markdown
2. **Verify each unit against the real source.** Read the cited files at the cited ranges in the grounding root; cross-check the diff against the spec's intent. For symbols and callers use the codegraph tools per `~/.claude/CODEGRAPH.md`: only when the brief says `index_state: fresh`, passing the brief's `projectPath`; a codegraph row is a lead you Read before citing, and when codegraph is not usable or returns nothing, Grep for the definition or a word-boundary reference and Read it.
```

### src/superclaude/agents/reuse-auditor.md:50 (wording source 3)

```markdown
For symbols and callers use the codegraph tools per `~/.claude/CODEGRAPH.md`: "when usable" below means the caller's brief says `index_state: fresh` (pass its `projectPath` on every call); otherwise use the Grep floor of each row. A codegraph row is a lead you Read before using it.
```

### src/superclaude/agents/auggie-reviewer.md:79 (wording source 4)

```markdown
- **`codegraph_search` / `codegraph_callers`**: where a symbol is defined and who calls it (`codegraph_node` for one symbol's body or a file outline). For symbols and callers use the codegraph tools per `~/.claude/CODEGRAPH.md`: only when the brief says `index_state: fresh`, passing the brief's `projectPath`; Read a row before citing it, and fall back to the Grep floor above when codegraph is not usable or returns nothing. Do not run the `codegraph` CLI through Bash
```

### /home/coder/workspaces/IronClaude/.dev/issues/504/issue-summary.md:12,24 (external main checkout; list source, NOT in grounding root)

```markdown
Ten general-purpose agent files also get the shared rule "use Codegraph only when the caller passes `index_state: fresh`, otherwise Grep/Read".
| `src/superclaude/agents/{system-architect,root-cause-analyst,refactoring-expert,security-engineer,performance-engineer,python-expert,backend-architect,quality-engineer,self-review,technical-writer}.md` | The ten agents that need the `index_state: fresh` rule; none has it today. |
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001 wording-fidelity of the rule text vs the four cited agents | F1 | finding (medium) | tasklist:19 vs the four hunks above |
| INF-002 ten-file list matches issue-summary.md:24 | — | covered | tasklist:26-94 vs issue-summary:24 |
| INF-003 AC strength (grep-count only) | F2 | finding (low) | tasklist:31,38,45,52,59,66,73,80,87,94 |
