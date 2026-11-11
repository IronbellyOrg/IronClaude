# Design: codegraph in /sc:implement (issue #504, implement slice)

Type: component. Format: spec. Target: `src/superclaude/commands/implement.md` and `src/superclaude/skills/sc-implement-protocol/` (SKILL.md, refs/qa.md, refs/retry.md).
Usage guide: `~/.claude/CODEGRAPH.md` (installed copy of core/CODEGRAPH.md). Pattern copied in spirit: sc-troubleshoot-protocol and sc-reflect-protocol (one readiness check, run state in every sub-agent brief, codegraph only when `index_state: fresh`, permanent Grep/Read floor, `graph:*` note, never halt).

## 1. Constraints (must hold)

- C1. Keep every flag, STOP code, ledger line format, evidence token, QA severity model (blocking/minor/note, four checklist answers, verdict order), retry ladder and managed-package rule of /sc:implement. No new `E-*` code.
- C2. The reviewer template in `refs/qa.md` stays closed with exactly seven slots (pinned by tests/skills/test_implement_severity_static.py and compared by FINAL). Codegraph context reaches the reviewer only through the existing `{diff}` slot content, never by editing the template.
- C3. The ledger `notes` file is not used for graph notes (a non-empty notes file changes the inline-review rule and adds a `notes@` token). Graph notes go to one run file.
- C4. Installed primitives never name `src/superclaude/...` as a read target; the guide is `~/.claude/CODEGRAPH.md`.
- C5. Allowlist names exact tools, no `mcp__codegraph__*` wildcard. Never call `codegraph_explore`, `codegraph init`, `index`, `sync`, or CLI `status` during an init (CODEGRAPH.md section 7).

## 2. Readiness check: exactly one per run (Wave 0 step 9)

After Wave 0 step 8 (optional auggie), before the first Q0, run the CODEGRAPH.md section 2 check once and keep the result as the **run state**: `index_state`, `access`, `checked_at`, `worktree_root`, `projectPath`.

- Resume starts a new run and does its own single check.
- No re-check after the first product write. The state stays as recorded at `checked_at`; graph rows about files this run changed are leads, confirmed by Grep/Read (CODEGRAPH.md section 2 step 7 and rules 1 and 3). If a later codegraph call reports not indexed, foreign index or an error, add the matching token, stay on the floor for the rest of the run, and do not re-check.
- `index_state` other than `fresh`, or `access: none`: no codegraph call this run; floor only; add the `graph:*` token from CODEGRAPH.md section 3.
- Print one line: `codegraph: index_state=<state> access=<access> checked_at=<ts>` plus the token when degraded.
- Record the state and every `graph:*` token in `codegraph.md` in the ledger directory (legacy `.dev/implement/<slug>/codegraph.md`; managed `<pkg>/artifacts/codegraph.md`). Append one line per later token. Never a halt, never a STOP.
- The existing `sc:impact-protocol` delegation at Q1 (rename/delete/signature tasks) and Q6 (advisory tests) is unchanged. It runs its own readiness inside that skill; this protocol does not count that as a second check of its own and does not copy its readiness into the run state.

## 3. Tool to step map (only when `index_state: fresh` and `access: mcp`)

| Step | Job | Tools (exact names, `projectPath` on every call) | Floor that always follows or replaces it |
|---|---|---|---|
| Q1a pre-edit context (new, before Q1 edits) | definitions, callers and blast radius of up to 5 symbols the task names or touches | `codegraph_search` to locate; `codegraph_node {symbol, file, includeCode:true}` for the definition; `codegraph_node {file, symbolsOnly:true}` for a file outline; `codegraph_callers` and `codegraph_impact depth 1` for who depends on it | Grep for the definition, Read the range, Grep `\b<symbol>\b` for references, Read each call site. Read before every Edit regardless |
| Q1 rename/delete/signature | unchanged | `sc:impact-protocol` as today | unchanged |
| Q2b dependents (new, after Q2 diff, before Q3) | did the change reach every dependent: for up to 5 symbols whose definition, signature or behaviour the diff changed, list dependents whose file is not in the task's touched set | `codegraph_callers`, `codegraph_impact depth 1`, `codegraph_callees` when the change moved a call | Grep `\b<symbol>\b` over the repo and Read the hits |
| Q3 REVIEW | reviewer sees the Q2b list as part of the `{diff}` slot | none added to the template | the reviewer still works from diff and AC |
| Q6 advisory tests | unchanged | `sc:impact-protocol` as today | unchanged |

Rules for rows: every row confirmed by the CS1-CS5 call-site procedure or a Grep plus Read before it is cited or drives an edit; at most 5 rows per symbol and 20 per run; empty graph answer is never "no dependents" (CODEGRAPH.md rule 3); a `shown/total` truncation re-queries once then records `graph:truncated`. A Q2b entry is informational context for the reviewer. It becomes a finding only through the existing checklist (for example an AC that requires the dependent to change), so the severity model is untouched. Q2b never edits and never widens the touched set.

## 4. Run state in every sub-agent brief

Every sub-agent prompt this protocol writes carries `index_state`, `checked_at`, `worktree_root` and `projectPath` from the run state:

- Per-task reviewer (inline text or Task subagent, `refs/qa.md`): the Q2b block heads the `{diff}` slot content with those four fields and the standing line "call codegraph only when index_state: fresh, never to widen scope". The seven-slot template and its saved-prompt comparison are untouched.
- Managed FINAL reviewer prompt (`refs/qa.md`) and the retry advisers (`refs/retry.md`, `implement-retry-adviser`): same four fields in the prompt. The adviser definition lists only Read, Grep and Glob, so it has no codegraph tools; its prompt states that and tells it to use Grep/Read, and to treat the state as context only.
- Saved prompts keep line 1 as the start sha; the state is inside slot/prompt body text, so FINAL's non-slot comparison is unchanged.

## 5. Frontmatter and command file

- SKILL.md `allowed-tools`: append the exact names `mcp__codegraph__codegraph_status`, `_search`, `_node`, `_callers`, `_callees`, `_impact` (same set sc-reflect-protocol uses). Add the "Extended metadata" comment block with `mcp-servers: [codegraph]`.
- SKILL.md gets one pointer line to `~/.claude/CODEGRAPH.md` (read once per run).
- implement.md frontmatter gains `mcp-servers: [codegraph]`; body gets a short "Codegraph" section: one readiness check per run, fresh-only use, Grep/Read floor with a recorded note, never a STOP, pointer to the protocol skill and `~/.claude/CODEGRAPH.md`. Boundaries gain: will not call `codegraph init`/`index`/`sync`.

## 6. Acceptance mapping

- (a) one check per run, tools named per step: sections 2 and 3, written in SKILL.md Wave 0 step 9, Q1a, Q2b and in implement.md.
- (b) fresh-only, floor with recorded note, no halt: sections 2 and 3.
- (c) briefs carry run state: section 4 in SKILL.md, qa.md, retry.md.
- (d) frontmatter lists the codegraph tools and server: section 5.
- (e) no new `src/superclaude` read-instruction hit: guide referenced as `~/.claude/CODEGRAPH.md` only.
- (f) `make sync-dev` and `make verify-sync` pass; (g) related tests pass: tests/skills/test_implement_*.py, test_review_severity_rule.py, tests/commands/test_impact_command.py, tests/commands/test_workflow_command.py.

## 7. Non-goals

No new tests required unless an existing pin breaks; no change to other commands, skills, agents, CODEGRAPH.md, `.claude/`; no commit, push or PR.
