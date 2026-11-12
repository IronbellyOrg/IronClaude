35576615952ec5268d515168d0200d6b0733ab5d
Review one task for spec compliance.

Task brief: ## Task 4: Edit the design command in src/superclaude/commands/design.md

Depends on: Task 1

Make these edits, each a clause or one sentence:
- Item 1: in "Readiness check, once per run", add one clause for the wait on a running `init`/`index` (pgrep, up to 60 s, then `graph:stale`), still one status call.
- Item 4: in the same paragraph, say `checked_at` is taken with one `date -u +%Y-%m-%dT%H:%M:%SZ` (Bash) immediately after the status call.
- Item 2: in the Analyze table row for `codegraph_files`, write `{format:"grouped", maxDepth:2, path?}` and add that `path` is set to the target's directory when it is narrower than the repo.
- Item 6: in the Validate row, change "then `codegraph_callers` and `codegraph_impact` for the consumers" so `codegraph_impact` runs at Validate only if it was not already run for the same symbol in Plan or Design.
- Item 7: in the sentence "A single lookup that fails or returns nothing falls back to the floor for that lookup in the same way", add that the matching lookup-level token (`graph:empty`, `graph:truncated` or `graph:unresolved`, all in the guide's section 3) is recorded in the Grounding line.
- Item 8: in "Grounding line", say that for `--format code` or `--format diagram` the line is the first comment line or a caption line of the output; for `spec` it stays a line of the document.
- Item 9: the first sentence of "Code-graph grounding" already says "read ... before the first codegraph call"; keep it, and make the Tool Coordination bullet's pointer say the same ("guide `~/.claude/CODEGRAPH.md`, read before the first codegraph call").

Acceptance criteria:
- `src/superclaude/commands/design.md` contains the pgrep/wait clause, the `date -u +%Y-%m-%dT%H:%M:%SZ` source, `path` on the `codegraph_files` row, the "only if not already run for the same symbol" Validate wording, the lookup-level token sentence, the code/diagram Grounding placement and the "before the first codegraph call" wording.
- The file still states one readiness check per run, the `fresh`-only rule, the floor and "never stops and never asks"; `uv run pytest tests/skills/test_codegraph_adoption.py -q` passes for this file.

AC ids:
T4.AC1: `src/superclaude/commands/design.md` contains the pgrep/wait clause, the `date -u +%Y-%m-%dT%H:%M:%SZ` source, `path` on the `codegraph_files` row, the "only if not already run for the same symbol" Validate wording, the lookup-level token sentence, the code/diagram Grounding placement and the "before the first codegraph call" wording.
T4.AC2: The file still states one readiness check per run, the `fresh`-only rule, the floor and "never stops and never asks"; `uv run pytest tests/skills/test_codegraph_adoption.py -q` passes for this file.
Global constraints: - Edit only `src/superclaude/commands/analyze.md`, `src/superclaude/commands/design.md`, `src/superclaude/core/CODEGRAPH.md`, `plugins/superclaude/core/CODEGRAPH.md` (a test pins it byte-identical to the source), `tests/skills/test_codegraph_adoption.py` and `tests/core/test_codegraph_guide.py`. The plugin twins of analyze.md and design.md already differ from the source (no codegraph text, `mcp-servers: []`) and no test pins them, so they stay untouched. `scripts/eval_workflow_vs_task_builder.py` pins skill tool lists, which this plan does not change, so it stays untouched unless a test run shows otherwise.
- Do not change behaviour, flags, the one-check-per-run rule, the fresh-and-`access: mcp` rule, the Grep/Read floor or the never-halt rule. Every fix is a clause or one sentence.
- `src/superclaude/core/CODEGRAPH.md` is shared by every primitive: additive clarifications only; it stays at 120 lines or fewer, names no `src/superclaude/` path, adds no `graph:*` token outside the closed list of its section 3 (which already holds `graph:empty` and `graph:truncated`), and names `explore` and the mutating verbs only in its Never section. Each phrase changed is grepped across `src/superclaude` first so no other primitive contradicts it.
- Reference the smoke report only through `./source.md`; never add a `src/superclaude` read path to an installed primitive. Never stage `.claude/`; no commit, no push, no PR.
- All nine report quotes were re-verified against the worktree before planning: the quotes sit at the stated lines of analyze.md (30, 32, 36, 63, 67), design.md (55, 57, 61, 65, 74) and CODEGRAPH.md (13, 22, 50, 74). None is rebutted.
Start sha: 35576615952ec5268d515168d0200d6b0733ab5d
Diff against the start snapshot: 
diff --git a/src/superclaude/commands/design.md b/src/superclaude/commands/design.md
index 7f18cd56b..44c3b1a3c 100644
--- a/src/superclaude/commands/design.md
+++ b/src/superclaude/commands/design.md
@@ -44,7 +44,7 @@ Key behaviors:
 
 - **Read**: Requirements analysis and existing system examination
 - **Grep/Glob**: Pattern analysis and system structure investigation (the floor for every step)
-- **codegraph** (`mcp__codegraph__codegraph_status`, `_search`, `_node`, `_callers`, `_callees`, `_impact`, `_files`): one readiness check, then symbol, caller and impact lookups above the Grep/Glob/Read floor when `index_state` is `fresh` (guide `~/.claude/CODEGRAPH.md`)
+- **codegraph** (`mcp__codegraph__codegraph_status`, `_search`, `_node`, `_callers`, `_callees`, `_impact`, `_files`): one readiness check, then symbol, caller and impact lookups above the Grep/Glob/Read floor when `index_state` is `fresh` (guide `~/.claude/CODEGRAPH.md`, read before the first codegraph call)
 - **Write**: Design documentation and specification generation
 - **Bash**: External design tool integration when needed
 
@@ -52,17 +52,17 @@ Key behaviors:
 
 Rules: read `~/.claude/CODEGRAPH.md` before the first codegraph call. Glob, Grep and Read stay the floor for every step; codegraph is a tier above that floor, never a replacement.
 
-**Readiness check, once per run.** At the start of Analyze, run the readiness check of that guide (its section 2) exactly once. Record `index_state`, `checked_at`, `worktree_root` and the `projectPath` to pass on every codegraph call. No later step repeats the check: the run reads code and writes only the design document.
+**Readiness check, once per run.** At the start of Analyze, run the readiness check of that guide (its section 2) exactly once: on the MCP path it first waits up to 60 s for a running `init` or `index` (guide step 3), and `checked_at` comes from one `date -u +%Y-%m-%dT%H:%M:%SZ` Bash run right after the single `codegraph_status` call. Record `index_state`, `checked_at`, `worktree_root` and the `projectPath` to pass on every codegraph call. No later step repeats the check: the run reads code and writes only the design document.
 
-**Use codegraph only when `index_state` is `fresh`** and the lookup tools are listed. For any other state (`stale`, `not_initialized`, `foreign_index`, `absent`, `disabled`, `error`, or lookup tools not listed), continue every step on Glob, Grep and Read and record the matching token from the guide's section 3 (`graph:stale`, `graph:not_initialized`, `graph:foreign_index`, `graph:absent`, `graph:disabled`, `graph:unlisted`, `graph:parse_failed`) in the Grounding line below. The run never stops and never asks the user because of codegraph. A single lookup that fails or returns nothing falls back to the floor for that lookup in the same way.
+**Use codegraph only when `index_state` is `fresh`** and the lookup tools are listed. For any other state (`stale`, `not_initialized`, `foreign_index`, `absent`, `disabled`, `error`, or lookup tools not listed), continue every step on Glob, Grep and Read and record the matching token from the guide's section 3 (`graph:stale`, `graph:not_initialized`, `graph:foreign_index`, `graph:absent`, `graph:disabled`, `graph:unlisted`, `graph:parse_failed`) in the Grounding line below. The run never stops and never asks the user because of codegraph. A single lookup that fails or returns nothing falls back to the floor for that lookup in the same way, and the matching token (`graph:empty`, `graph:truncated` for a short caller list, or `graph:unresolved` for a row you could not confirm) goes in the Grounding line.
 
 | Step | Design question | Codegraph tool (each call passes `projectPath`) |
 |------|-----------------|--------------------------------------------------|
-| Analyze | What structure already exists? | `codegraph_files {format:"grouped", maxDepth:2}` |
+| Analyze | What structure already exists? | `codegraph_files {format:"grouped", maxDepth:2, path}` with `path` set to the target's directory when it is narrower than the repo |
 | Analyze | Which existing interfaces, types and symbols should the design reuse? | `codegraph_search {query, kind?}`, `codegraph_node {symbol, includeCode:true}`, `codegraph_node {file, symbolsOnly:true}` for a file outline |
 | Plan, Design | Who uses the component or API being designed or changed, and what does it use? | `codegraph_callers {symbol, limit:20}`, `codegraph_callees {symbol}` |
 | Plan, Design | What does a change to an existing interface reach (blast radius)? | `codegraph_impact {symbol, depth:2}` before the design proposes the change |
-| Validate | Do the names, layering and signatures in the design exist and match the current structure, and does no consumer break? | `codegraph_search`, `codegraph_node`, then `codegraph_callers` and `codegraph_impact` for the consumers |
+| Validate | Do the names, layering and signatures in the design exist and match the current structure, and does no consumer break? | `codegraph_search`, `codegraph_node`, then `codegraph_callers` for the consumers, and `codegraph_impact` only if it was not already run for the same symbol in Plan or Design |
 
 Rules for graph answers:
 
@@ -71,7 +71,7 @@ Rules for graph answers:
 - Caller rows give the caller's definition line; confirm the call site (guide section 5) before citing it.
 - Never call `codegraph_explore`, never use `codegraph_node` in file mode without `symbolsOnly:true`, and never run a mutating codegraph verb or `codegraph init`.
 
-**Grounding line.** The design document carries one `Grounding:` line: `index_state: fresh` with the codegraph tools used, or the `graph:*` token that sent the run to the floor. Under `--unattended` the line stays in the design report and the worker contract gets no new field.
+**Grounding line.** The design document carries one `Grounding:` line: `index_state: fresh` with the codegraph tools used, or the `graph:*` token that sent the run to the floor; with `--format code` or `--format diagram` it is the first comment line or a caption line of the output. Under `--unattended` the line stays in the design report and the worker contract gets no new field.
 
 ## Key Patterns
 

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
