44528c1a9bf06a0446fcdb32934cd878168d1e49
Review one task for spec compliance.

Task brief: ## Task 3: Edit the analyze command in src/superclaude/commands/analyze.md

Depends on: Task 1

Make these edits, each a clause or one sentence:
- Item 1: in the paragraph before step 1, add one clause that on the MCP path the single check first waits for a running `init`/`index` as section 2 of the guide says (pgrep, up to 60 s, then `graph:stale`), still one status call.
- Item 4: in the same paragraph, say `checked_at` is taken with one `date -u +%Y-%m-%dT%H:%M:%SZ` (Bash) immediately after the status call.
- Items 2 and 3, Discover step: rewrite so that `codegraph_files {format:"grouped", maxDepth:2}` takes `path` set to the target's directory when the target is narrower than the repo; for a directory or package target use `codegraph_files` with `path` and then `codegraph_node` with `symbolsOnly:true` on its main files; use `codegraph_search` only when the target names a symbol.
- Item 3, Scan step: symbol bodies (`includeCode:true`) are taken only for symbols Discover found; file outlines (`symbolsOnly:true`) stay as they are.
- Item 5, "Leads, not citations" bullet: add one sentence: at `--depth quick` a line found by Grep need not be re-Read, but a graph row cited as a finding is still confirmed by Grep or Read.
- Item 7: in the same bullet or the Use-only bullet, say a single lookup that fails or returns nothing records `graph:empty` (or `graph:truncated` for a short caller list, `graph:unresolved` for an unconfirmed row) on the Codegraph line and falls back to the floor for that lookup.
- Item 8: in the Report step, say that with `--format json` the line goes in a top-level `"codegraph"` string field of the JSON, and in other formats it stays one line of the report.
- Item 9: change "(read it when you use codegraph)" to "(read it before the first codegraph call)".

Acceptance criteria:
- `src/superclaude/commands/analyze.md` contains the pgrep/wait clause, the `date -u +%Y-%m-%dT%H:%M:%SZ` source, `path` on the `codegraph_files` call, the directory-target wording, the quick-depth sentence, a lookup-level token sentence naming tokens from the guide's section 3, the `"codegraph"` JSON field rule and "read it before the first codegraph call".
- The file still holds the `index_state: fresh` with `access: mcp` rule, the "never halt, never ask" sentence and one readiness check per run; `uv run pytest tests/skills/test_codegraph_adoption.py -q` passes for this file.

AC ids:
T3.AC1: `src/superclaude/commands/analyze.md` contains the pgrep/wait clause, the `date -u +%Y-%m-%dT%H:%M:%SZ` source, `path` on the `codegraph_files` call, the directory-target wording, the quick-depth sentence, a lookup-level token sentence naming tokens from the guide's section 3, the `"codegraph"` JSON field rule and "read it before the first codegraph call".
T3.AC2: The file still holds the `index_state: fresh` with `access: mcp` rule, the "never halt, never ask" sentence and one readiness check per run; `uv run pytest tests/skills/test_codegraph_adoption.py -q` passes for this file.
Global constraints: - Edit only `src/superclaude/commands/analyze.md`, `src/superclaude/commands/design.md`, `src/superclaude/core/CODEGRAPH.md`, `plugins/superclaude/core/CODEGRAPH.md` (a test pins it byte-identical to the source), `tests/skills/test_codegraph_adoption.py` and `tests/core/test_codegraph_guide.py`. The plugin twins of analyze.md and design.md already differ from the source (no codegraph text, `mcp-servers: []`) and no test pins them, so they stay untouched. `scripts/eval_workflow_vs_task_builder.py` pins skill tool lists, which this plan does not change, so it stays untouched unless a test run shows otherwise.
- Do not change behaviour, flags, the one-check-per-run rule, the fresh-and-`access: mcp` rule, the Grep/Read floor or the never-halt rule. Every fix is a clause or one sentence.
- `src/superclaude/core/CODEGRAPH.md` is shared by every primitive: additive clarifications only; it stays at 120 lines or fewer, names no `src/superclaude/` path, adds no `graph:*` token outside the closed list of its section 3 (which already holds `graph:empty` and `graph:truncated`), and names `explore` and the mutating verbs only in its Never section. Each phrase changed is grepped across `src/superclaude` first so no other primitive contradicts it.
- Reference the smoke report only through `./source.md`; never add a `src/superclaude` read path to an installed primitive. Never stage `.claude/`; no commit, no push, no PR.
- All nine report quotes were re-verified against the worktree before planning: the quotes sit at the stated lines of analyze.md (30, 32, 36, 63, 67), design.md (55, 57, 61, 65, 74) and CODEGRAPH.md (13, 22, 50, 74). None is rebutted.
Start sha: 44528c1a9bf06a0446fcdb32934cd878168d1e49
Diff against the start snapshot: 
diff --git a/src/superclaude/commands/analyze.md b/src/superclaude/commands/analyze.md
index 78274ea70..af240e688 100644
--- a/src/superclaude/commands/analyze.md
+++ b/src/superclaude/commands/analyze.md
@@ -27,13 +27,13 @@ personas: []
 
 ## Behavioral Flow
 
-Before step 1, run the codegraph readiness check exactly once per run, as section 2 of `~/.claude/CODEGRAPH.md` describes. Keep `index_state`, `access`, `checked_at` and `worktree_root` for the whole run and do not repeat the check. Below, "`index_state: fresh`" means `index_state: fresh` with `access: mcp` (the lookup tools are listed); with `access: cli` or `access: none` every step stays on Glob, Grep and Read, and no codegraph tool, including `codegraph_files`, is called.
+Before step 1, run the codegraph readiness check exactly once per run, as section 2 of `~/.claude/CODEGRAPH.md` describes: on the MCP path it first waits up to 60 s for a running `init` or `index` (guide step 3), and `checked_at` comes from one `date -u +%Y-%m-%dT%H:%M:%SZ` Bash run right after the single `codegraph_status` call. Keep `index_state`, `access`, `checked_at` and `worktree_root` for the whole run and do not repeat the check. Below, "`index_state: fresh`" means `index_state: fresh` with `access: mcp` (the lookup tools are listed); with `access: cli` or `access: none` every step stays on Glob, Grep and Read, and no codegraph tool, including `codegraph_files`, is called.
 
-1. **Discover**: Categorize source files using language detection and project analysis. When `index_state: fresh`, first call `codegraph_files {format:"grouped", maxDepth:2}` for the layout and `codegraph_search` to locate the target's symbols
-2. **Scan**: Apply domain-specific analysis techniques and pattern matching. When `index_state: fresh`, first call `codegraph_node` (symbol body with `includeCode:true`, file outline with `symbolsOnly:true`), `codegraph_callers` and `codegraph_callees` for call paths (security: entry points to sinks; performance: hot-path callers)
+1. **Discover**: Categorize source files using language detection and project analysis. When `index_state: fresh`, first call `codegraph_files {format:"grouped", maxDepth:2, path}` for the layout, with `path` set to the target's directory when the target is narrower than the repo; for a directory or package target add `codegraph_node {file, symbolsOnly:true}` on its main files, and use `codegraph_search` only when the target names a symbol
+2. **Scan**: Apply domain-specific analysis techniques and pattern matching. When `index_state: fresh`, first call `codegraph_node` (symbol body with `includeCode:true` only for symbols Discover found, file outline with `symbolsOnly:true`), `codegraph_callers` and `codegraph_callees` for call paths (security: entry points to sinks; performance: hot-path callers)
 3. **Evaluate**: Generate prioritized findings with severity ratings and impact assessment. When `index_state: fresh`, use `codegraph_impact` and `codegraph_callers` as dependency and blast-radius evidence for architecture and quality findings (dead-code candidates are leads only)
 4. **Recommend**: Create actionable recommendations with implementation guidance
-5. **Report**: Present comprehensive analysis with metrics and improvement roadmap, with one line `Codegraph: index_state=<state>, checked_at=<UTC>; degraded: <graph:* tokens or none>` (a missing or stale graph leaves the run succeeded once the report is written)
+5. **Report**: Present comprehensive analysis with metrics and improvement roadmap, with one line `Codegraph: index_state=<state>, checked_at=<UTC>; degraded: <graph:* tokens or none>` (with `--format json` it is the top-level `"codegraph"` string field; a missing or stale graph leaves the run succeeded once the report is written)
 
 Key behaviors:
 
@@ -60,11 +60,11 @@ Key behaviors:
 
 ## Codegraph (optional)
 
-Full rules: `~/.claude/CODEGRAPH.md` (read it when you use codegraph). This section is the short form for `/sc:analyze`.
+Full rules: `~/.claude/CODEGRAPH.md` (read it before the first codegraph call). This section is the short form for `/sc:analyze`.
 
 - **Readiness**: the single check named before step 1 of the Behavioral Flow; never repeat it. `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` means `graph:disabled`.
 - **Use only when `index_state: fresh` and `access: mcp`.** Otherwise continue on Glob, Grep and Read, add the matching `graph:*` token to the report's Codegraph line, and go on: never halt, never ask. A missing, stale or failing graph never fails the run (it is succeeded once the report is written).
-- **Leads, not citations**: re-Read a `file:line` before citing it; an empty result is not a "no callers" finding; caller rows give the definition line, so confirm the call site (guide section 5) before citing; a caller list shorter than its total is `graph:truncated`.
+- **Leads, not citations**: re-Read a `file:line` before citing it (at `--depth quick`, a line found by Grep need not be re-Read, but a graph row cited as a finding is still confirmed by Grep or Read); an empty result is not a "no callers" finding; caller rows give the definition line, so confirm the call site (guide section 5) before citing; a caller list shorter than its total is `graph:truncated`; a single lookup that fails or returns nothing records `graph:empty` (or `graph:unresolved` for a row you could not confirm) on the Codegraph line and falls back to Glob, Grep and Read for that lookup.
 - **Read-only**: never run `codegraph init`, `index`, `sync`, `explore` or `context`.
 - **Names**: exact tool names `mcp__codegraph__codegraph_<tool>`, with `projectPath` set to `worktree_root` on every call.
 - **Subagents** (if the run fans out): the brief carries `index_state`, `checked_at` and `worktree_root`; they call codegraph only when `index_state: fresh`.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
