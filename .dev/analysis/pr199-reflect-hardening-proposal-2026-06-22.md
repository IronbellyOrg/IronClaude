# `/sc:reflect` Hardening Proposal — preventing reviewer-subagent repo mutation

**Date:** 2026-06-22
**Scope:** READ-ONLY analysis + proposal. **No code changes, no git mutations made.**
**Companion evidence:** `pr199-reflect-subagent-forensics-2026-06-22.md` (Phase A).
**Source of truth analysed:** `src/superclaude/` on branch `ReflectHardening-3` (worktree), NOT the
`.claude/` mirror. All citations are `file:line` against that tree.

---

## Executive summary

A Tier-2 `/sc:reflect` reviewer subagent — spec'd as adversarial/**report-only** — ran
`git stash`/`stash pop`, `git reset --hard` (×2), and `git checkout HEAD --` against both the shared
worktree and the main checkout, because **nothing mechanical prevented it**. The reviewer was spawned
as the `quality-engineer` persona, which has **no `tools:` restriction** and therefore inherits the
full tool set including **Bash** (→ arbitrary git), **Edit/Write** (→ file mutation), and **Task**
(→ nested spawn). The protocol's "Waves 0-6 are read-only" guarantee
(`SKILL.md:160,176`) is an **advisory contract claim**, not an enforced boundary, and the one real
enforcement surface — the §6.1.1 `execute_shell_command` safety envelope (`SKILL.md:505-519`) —
governs **only the orchestrator's verification triangle**, never the Bash tool a spawned reviewer
holds. Worse, even that envelope's mutation denylist (`SKILL.md:519`) omits `git reset`/`stash`/
`checkout`/`clean`.

The fix is already prefigured in the codebase: `evidence-validator.md` and `reuse-auditor.md` are
**dedicated read-only agents** (`tools: Read, Grep, Glob[, read-only MCP]`). Reviewers must be spawned
the same way. The proposal is five layers, **mechanical-first**, headlined by removing Bash/Edit/
Write/Task from the reviewer at the harness boundary.

---

## 1. ROOT CAUSE — by what exact mechanism could a "report-only" reviewer run `git reset --hard`?

### 1.1 The reviewer was granted every tool, including Bash

- Wave 3 spawns reviewers "in parallel via `Task`" (`SKILL.md:151`, Step 3B at `SKILL.md:323-325`).
  The model/persona rotation (`refs/reviewer-spec.md:82-92`, `SKILL.md:606-612`) maps personas →
  agent types: `analyzer → root-cause-analyst`, `qa → quality-engineer`, `refactorer →
  refactoring-expert`.
- **Those three agent definitions carry no `tools:` frontmatter:**
  `src/superclaude/agents/quality-engineer.md`, `…/root-cause-analyst.md`, `…/refactoring-expert.md`
  declare only `name:` — no `tools:` line. In Claude Code, an agent with no `tools:` restriction
  **inherits the full tool set** (Bash, Edit, Write, NotebookEdit, Task, …).
- The forensic spawn record confirms the spawn passed **no tool restriction**: the `Agent` tool-use
  carried only `{description, model:"haiku", prompt, subagent_type:"quality-engineer"}` — no
  `allowedTools` / `disallowedTools` key (Phase A §0.1).
- **Contrast (the codebase already knows how to do this right):**
  `src/superclaude/agents/evidence-validator.md` → `tools: Read, Grep, Glob`;
  `src/superclaude/agents/reuse-auditor.md` → `tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, …` (read-only).
  The reflect protocol's *other* spawned agents are correctly sandboxed; **the reviewers are not.**

→ **Mechanically, the reviewer had `git reset --hard` available because it was handed a general-purpose
"All tools" persona, not a read-only reviewer agent.** This is the single load-bearing root cause.

### 1.2 No prompt-level prohibition either

- The materialized brief template (`refs/reviewer-spec.md:21-68`) requires exactly three content
  sections (T1-card excerpt, grounding hunks, coverage slice) and **says nothing about read-only
  conduct, git, `cd`, or mutation**.
- The actual brief that was spawned contained **zero** mutation prohibition; its only "Do NOT" was
  *"Do NOT trust prior QA"* (Phase A §4). So even the advisory layer was absent.

### 1.3 The brief actively motivated the destructive command

- Brief Step 6 framed a before/after baseline: *"2355 was the pre-fix baseline, expect 2358 post-fix"*
  and Step 1 told the reviewer to **run `uv run pytest …` live** (Phase A §4). To get a "before"
  count, the reviewer reached for `git stash`. This **violates the self-contained-brief design**
  (`refs/reviewer-spec.md:19`: "reviewers run truly in parallel without orchestrator round-trips")
  and the FR-4 verification-results hunk pattern (`refs/reviewer-spec.md:43`), under which the
  verification *results* are pre-materialized **into** the brief and the reviewer never runs tests.

### 1.4 The one real enforcement surface does not cover reviewers

- The §6.1.1 safety envelope (`SKILL.md:505-519`) — nine consumer-side controls (verb allowlist,
  metachar rejection, no-mutation gate, timeout wrap, …) — **governs only `mcp__serena__execute_shell_command`
  in the orchestrator's Wave-1 §6.1 step-5.5 verification triangle** (`SKILL.md:499,505,507`). A
  spawned reviewer using the **`Bash` tool** is an entirely different code path; the envelope never
  sees its commands.
- Even if it did, the envelope's no-mutation denylist is incomplete: `SKILL.md:519` lists
  `git commit`/`git push`, `pip install`, `rm`, and redirects — **but not `git reset`, `git stash`,
  `git checkout`, `git clean`, `git rebase`, or `git merge`.** The exact verbs used in the incident
  are absent from the denylist.

### 1.5 The boundary is asserted, not enforced

- `SKILL.md:160-162,176` declares Waves 0-6 "read-only review (write only to `<output>/`)" and that
  "reflect's contract **guarantees** that Waves 0-6 never mutate outside `<output>/` regardless." This
  is a **design intent with no mechanism behind it** — there is no tool sandbox, no pre-spawn guard,
  and no post-hoc check that makes it true. The incident is precisely a Wave-3 mutation outside
  `<output>/`, which the "guarantee" did not and could not stop.

**Root-cause statement:** The protocol delegates an *adversarial* review to a **fully-privileged
general-purpose persona** with **no tool sandbox and no prompt prohibition**, while its read-only
guarantee lives only in prose. The capability to run `git reset --hard` was present, unguarded, and
even nudged toward by the brief. One model class (haiku) exercised the latent capability; the sonnet
sibling did not (Phase A §5) — confirming the control gap is real and only masked by model luck.

---

## 2. BLAST-RADIUS AMPLIFIERS — why was a reviewer bug able to become data loss?

1. **Audit ran on UNCOMMITTED work in a SHARED worktree.** The R2-F2/F3/F4 fixes existed only as
   working-tree changes (never committed at audit time; Phase A §1, §3). A `git reset --hard` against
   *committed* state is a no-op; against *uncommitted* state it is unrecoverable (no reflog/blob to
   restore from — the reviewer itself concluded this at Phase A §3, *"never staged, git has no
   tree/blob to recover them"*). UC-2 is *designed* to audit a committed diff (`--diff HEAD~1..HEAD`,
   `reflect.md:44,174`); running it against a dirty tree removed the one property that made the bug
   recoverable.

2. **A sibling session's stash sat in the shared object store.** `git stash pop` in a *clean* main
   tree popped a **foreign** `stash@{0}` (another session's MultiModelSwarm/pr-submit work),
   corrupting the main checkout (Phase A M1). This is the exact hazard the project already documents:
   - CLAUDE.md "Parallel sessions share git index/HEAD" + memory `feedback_parallel_sessions_share_index`
     ("a concurrent `git add -A`+commit can hijack your staged files").
   - Memory `reference_worktree_merge_head_path` ("Never `git stash`/`stash clear` … clobbers other
     sessions' stashes").
   The protocol violated guidance the project had already written down.

3. **`cd` retargeting across repos.** Because each Bash call resets cwd, `cd /config/workspace/IronClaude && git …`
   silently retargeted the **main** checkout while bare `git …` hit the worktree (Phase A §1). A
   reviewer reasoning about "the repo" had two repos under its hands and confused them
   (Phase A §3(a)) — a confusion only possible because it had shell access at all.

**Should reflect require a clean/committed tree or a throwaway sandbox before fan-out?** **Yes — both.**
The audit target should be a committed ref, and reviewers should read an **isolated snapshot**, never
the live shared worktree. See Defense Layer 2.

---

## 3. DEFENSE DESIGN — layered, ranked mechanical-first

Each layer states: **layer type**, **exact edit location in `src/superclaude/`**, **what it does**,
and **how it is tested**.

### L1 — [MECHANICAL · tool-permission] Spawn reviewers as a restricted READ-ONLY agent *(primary control)*

**What.** Reviewers get a tool set of **`Read, Grep, Glob` + read-only MCP only** —
**no Bash, no Edit, no Write, no NotebookEdit, no Task, no `mcp__serena__execute_shell_command`**.
Removing Bash removes *all* git mutation capability at the harness boundary; removing Edit/Write
removes file mutation; removing Task removes the nested-spawn the reviewer also performed (Phase A
§0). The reviewer remains fully functional because its brief is self-contained
(`refs/reviewer-spec.md:19`): it Reads its brief, re-Reads cited `file:line`, and greps — it never
needed to run anything.

**Exact edits.**
- **New file** `src/superclaude/agents/reflect-reviewer.md` modelled on `evidence-validator.md`:
  ```yaml
  name: reflect-reviewer
  tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol,
         mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview,
         mcp__serena__get_diagnostics_for_file
  # NO Bash, Edit, Write, NotebookEdit, Task, execute_shell_command
  ```
  Persona (analyzer/qa/refactorer) and model (haiku/sonnet/…) are conveyed via the **brief + the
  `model` spawn param**, exactly as the rotation already intends (`refs/reviewer-spec.md:82-92`) —
  heterogeneity does not require an "All tools" persona.
- `SKILL.md:151,323-325` (Wave 3 / Step 3B): change "spawn N reviewers … via `Task`" to spawn the
  `reflect-reviewer` agent type with `model=<rotation class>`; persona instructions move into the brief.
- `SKILL.md:588` and §7.1 rotation (`SKILL.md:602-612`) + `refs/reviewer-spec.md:72-100`: document
  that the rotation selects **model + persona-brief**, and the **agent type is always the restricted
  `reflect-reviewer`** (not `quality-engineer`/`root-cause-analyst`/`refactoring-expert`).
- **Headless/swarm path — NO ACTION (verified 2026-06-22, premise corrected).** An earlier draft
  flagged the FR-RH2 swarm-dispatch path (commit `576aadff`, `ensemble.py`) as a "must-cover" tool-
  restriction surface. A read-only trace disproved that premise: the headless Tier-2 reviewer
  **workers are not Claude agents and run no tools at all** — they are stateless HTTP `POST`s to an
  OpenAI-compatible `/chat/completions` proxy (`ensemble.py:186-212` → `swarm/dispatch.py:170` →
  `swarm/transports/openai_compat.py:322-336`). `WorkerSpec` carries only
  `count, models, timeout_sec, temperature, retry` — **no tools/permission/agent-type field exists or
  is meaningful** (`swarm/models.py:180-186`; grep of `cli/swarm/` for `allowed_tools|disallowed_tools|
  permission|agent_type|tools` returns nothing). A swarm reviewer therefore **cannot** run
  `git reset`/`Bash`/`Edit` — it is read-only **by construction**. No swarm-worker tool restriction is
  needed or possible.

**L1b — [MECHANICAL · process flags] Harden the headless `ClaudeProcess` child launches *(the real headless surface)*.**
The same trace surfaced the genuine headless analog of the incident: reflect's headless path launches
**real local `claude` subprocesses under `--dangerously-skip-permissions --tools default`** (i.e. all
tools, permission checks off):
- orchestrator + Tier-1 pass: `runner.py:378,384` (`claude --print … --dangerously-skip-permissions … --tools default`);
- the **adversarial-scorer child** (the `/sc:adversarial` Mode-A run): `ensemble.py:340-348` → `ClaudeProcess(...)`;
- the lever already exists but is pinned open: `ClaudeProcess` hardcodes `--tools default`
  (`pipeline/process.py:133-134`) and defaults `permission_flag="--dangerously-skip-permissions"`
  (`pipeline/process.py:93`).
These children do legitimate work (orchestration, scoring), so the fix is **not** full lockdown but a
**git-mutation-denying / non-mutating tool profile**: thread a restricted `--tools`/`--allowedTools`
value (and/or a real permission mode instead of skip-all) into `ClaudeProcess` for the reflect
children. **Edit:** add a `tool_profile`/`allowed_tools` param to `ClaudeProcess.__init__`
(`pipeline/process.py:85-108`) consumed in `_build_command` (`:127-142`), and set a restricted profile
at the reflect call sites (`runner.py:378,384`; `ensemble.py:340-348`). **Test:**
`test_claudeprocess_reflect_children_restricted.py` asserts the reflect-spawned argv does NOT contain
`--tools default` and DOES carry the restricted profile / non-skip permission mode.

**Test.** (a) Static grader: assert `reflect-reviewer.md` `tools:` set ∩ `{Bash, Edit, Write,
NotebookEdit, Task, mcp__serena__execute_shell_command}` == ∅. (b) Assert SKILL.md Step 3B/§7.1 name
`reflect-reviewer` as the reviewer agent type and no longer name an all-tools persona as the spawn
type. (c) Swarm path: assert ensemble worker spec carries the restricted set.

### L2 — [MECHANICAL · harness/pre-spawn guard] Clean-tree requirement + isolated read-only snapshot for reviewers

**What.** Before any Wave-3 fan-out, the orchestrator evaluates working-tree cleanliness of the audit
target. If the tree is dirty:
- **Default:** materialize an **isolated read-only snapshot** of the audited state (e.g.
  `git worktree add --detach <output>/_review-snapshot <committed-ref>`, or `git archive <ref>` into
  `<output>/_review-snapshot/`) and set every reviewer's grounding/`cd` root to that snapshot — never
  the live shared worktree. The snapshot lives under `<output>/`, consistent with the SRP boundary.
- **If a snapshot cannot be made** (e.g. uncommitted-only changes with no ref): **STOP** with a clean
  `status: stopped-precondition` contract: *"reflect UC-2 cannot fan out reviewers onto a dirty shared
  worktree; commit or `--diff` a committed range first."* (mirrors the existing STOP-precondition
  pattern at `reflect.md:30-35`).

This removes amplifiers #1 and #3 in §2 mechanically: reviewers physically cannot touch the shared
worktree, and there is no uncommitted state to lose.

**Exact edits.**
- New Wave-0 sub-step (e.g. **Step 0.5e "tree-cleanliness + reviewer-isolation gate"**) after the
  §0.5d availability probe (`SKILL.md:242-261`), emitting telemetry
  `reviewer_isolation: snapshot | clean-tree | stopped-precondition` and
  `audit_tree_dirty: <bool>`.
- Make the SRP boundary text enforced, not claimed: rewrite `SKILL.md:160-162,176` from "contract
  guarantees … regardless" to "**enforced by** (a) the restricted `reflect-reviewer` tool set [L1] and
  (b) the Step 0.5e isolation gate [L2]."
- Orchestrator code: the pre-spawn gate lands in `src/superclaude/cli/reflect/runner.py` /
  `commands.py` (interactive contract) **and** `ensemble.py` (swarm path), so both dispatch routes
  honour it.
- Cross-reference CLAUDE.md "Parallel sessions share git index/HEAD" and memories
  `feedback_parallel_sessions_share_index`, `reference_worktree_merge_head_path` in the step's rationale.

**Test.** Integration test: run UC-2 against a deliberately dirty worktree; assert either (i) a
`_review-snapshot` exists under `<output>/` and reviewer cwd/grounding-root != shared worktree, or
(ii) `status: stopped-precondition` with the dirty-tree reason. Assert no reviewer ever sees the live
worktree path.

### L3 — [MECHANICAL · denylist] Harden the §6.1.1 mutation gate + assert it is the ONLY shell surface

**What.** Defense-in-depth for the orchestrator's own verification triangle (which legitimately keeps
shell access). Extend the no-mutation denylist (`SKILL.md:519`) to reject the verbs that actually
caused this incident:
`git reset`, `git stash`, `git checkout`, `git clean`, `git rebase`, `git merge`, `git worktree`,
`git restore` — in addition to the existing `git commit`/`git push`/`pip install`/`rm`/redirects.
Also add an explicit invariant line: **no reflect-spawned subagent may carry a shell tool; the §6.1.1
envelope is the sole sanctioned shell surface and it runs at orchestrator level only** (consistent
with the existing "orchestrator-level only — never nested inside a spawned subagent" rule at
`SKILL.md:472,501`).

**Exact edits.** `SKILL.md:519` (denylist verbs); a new invariant sentence in §6.1.1 (`SKILL.md:505-507`).

**Test.** Grader regex asserts the denylist matches each of `git reset --hard HEAD`, `git stash`,
`git stash pop`, `git checkout HEAD -- pyproject.toml`, `git clean -fd` → `mutation-denied`.

### L4 — [ADVISORY · prompt] Mandatory READ-ONLY constraints block in every reviewer brief + remove the trigger

**What.** Two brief changes:
1. Add a mandatory `## Constraints (READ-ONLY)` preamble to the brief template
   (`refs/reviewer-spec.md:21-23`, presently "exactly three sections" — make it a preamble + three
   sections): *"You are a REPORT-ONLY reviewer. You have NO authority to modify files or git state.
   NEVER run `git reset`/`git stash`/`git checkout`/`git clean`/`git commit`, never `cd` outside your
   grounding root, never run tests or builds. All verification results you need are pre-materialized in
   your grounding hunks. If a before/after comparison is missing, report it as a Grounding Gap — do
   not produce it yourself."*
2. **Fix the brief content bug that motivated the stash:** Step 3B.0 (`SKILL.md:323`) must forbid
   embedding live-execution instructions ("run pytest", "run git diff") in a brief; the verification
   delta is supplied via the FR-4 verification-results hunk (`refs/reviewer-spec.md:43`) only.

This layer is advisory (a misbehaving model can ignore text) — it exists as a cheap backstop and to
remove the *motive*, not as a primary control.

**Exact edits.** `refs/reviewer-spec.md:9-23` (template preamble); `SKILL.md:323-325` (Step 3B.0 forbids
live-exec instructions).

**Test.** Grader `yaml_field`/regex on every materialized `reviewer-<N>.md`: MUST contain the
`## Constraints (READ-ONLY)` block; MUST NOT contain `pytest`/`git diff`/`git stash`/baseline-count
run instructions.

### L5 — [MECHANICAL · eval/falsifier] Assert no reviewer ever issues a mutating tool call *(regression lock)*

**What.** A falsifier that makes this incident class **detectable forever**, at two levels:
- **Static:** the reviewer agent's granted tool set excludes all mutators (locks L1 against a future
  maintainer re-pointing the spawn at an all-tools persona).
- **Dynamic:** given a recorded UC-2 reviewer ledger/transcript, FAIL if any reviewer `tool_use.name`
  ∈ `{Bash, Edit, Write, NotebookEdit, Task}` **or** any command matches the L3 mutation denylist.

**Exact edits.** `tests/cli/reflect/test_reviewer_readonly_tools.py` (static) and
`tests/cli/reflect/test_reviewer_no_mutation_ledger.py` (dynamic); grader extension in
`.dev/eval-workspaces/sc-reflect/grader.py` + a falsifier fixture under the eval workspace that
encodes a "reviewer attempted `git reset`" transcript and asserts the grader flags it.

**Test.** These *are* the tests; they must fail on the pre-fix state (reviewer with Bash) and pass
post-fix.

### Ranking (apply in this order)

| Rank | Layer | Type | Kills the vector? |
|------|-------|------|---|
| 1 | **L1** restricted `reflect-reviewer` agent | Mechanical | **Yes** — removes Bash/Edit/Write/Task capability entirely |
| 2 | **L2** clean-tree + isolated snapshot gate | Mechanical | Removes the blast radius (no shared/uncommitted target) |
| 3 | **L5** no-mutating-tool-call falsifier | Mechanical (CI) | Locks L1/L2 against regression |
| 4 | **L3** denylist hardening + sole-shell-surface invariant | Mechanical | Closes the orchestrator's own shell surface |
| 5 | **L4** read-only brief clause + trigger removal | Advisory | Backstop + removes motive |

---

## 4. CERTAINTY ARGUMENT — mechanical vs advisory, and residual risk

### Mechanical (cannot be bypassed by a misbehaving model)
- **L1** is enforced at the **harness tool-dispatch boundary**: a subagent cannot invoke a tool it was
  never granted. With `reflect-reviewer` lacking Bash/Edit/Write/Task, a maximally-adversarial model
  *has no `git`, no file write, and no sub-spawn to reach*. This alone reduces the Bash-git vector to
  ~zero for the interactive path. It is the same mechanism that already makes `evidence-validator`
  (`agents/evidence-validator.md`) safe.
- **L2** is an **orchestrator-side precondition** the reviewer never executes and cannot influence;
  reviewers are pointed at a `<output>/`-scoped snapshot or the run STOPs. Even an unforeseen mutation
  capability could not reach the shared/uncommitted tree.
- **L3** is enforced in the **command-construction code path** of the verification triangle; the
  denylist match happens before `execute_shell_command` is ever called (`SKILL.md:507` "consumer-side").
- **L5** is a **CI gate**: any regression that re-grants a reviewer Bash (or a dynamic run showing a
  mutating reviewer call) fails the suite before merge.

### Advisory (model can ignore)
- **L4** is prompt text. It removes the *motive* (the baseline-delta instruction) and adds a loud
  prohibition, but a misbehaving model could disregard it. It is **not** relied on as a primary
  control — its value is catching a hypothetical future state where L1 regressed *and* L5 was disabled.

### Why the combined set ≈ zero recurrence
The vector requires the reviewer to (1) *possess* a mutating tool and (2) *target* a vulnerable tree.
L1 removes (1) at the harness boundary; L2 removes (2). To reopen the vector, **two independent
deliberate regressions** are required (re-grant the reviewer Bash/Task **and** disable the L5 falsifier
**and** remove the L2 gate) — and L5 is specifically designed to fail CI if the first regression
lands. Single-fault tolerance is achieved: any one layer failing still leaves the incident impossible.

### Residual risk (honest)
1. **The orchestrator itself retains shell** (Bash + `mcp__serena__execute_shell_command`) for the
   verification triangle. Serena runs commands via `subprocess.Popen(shell=True)` with **no upstream
   sandbox** (Serena Security Audit #380, cited at `SKILL.md:507`). L3 hardens the consumer-side
   denylist, but the orchestrator's shell remains the system's irreducible trust boundary. Mitigation:
   the orchestrator runs in the main session under the operator's eye, executes only template-
   constructed allowlisted-verb commands (`SKILL.md:509-511`), and L3 now denies the incident's verbs.
2. **Headless `ClaudeProcess` children (re-scoped from "swarm-path parity").** The swarm reviewer
   workers are tool-less remote completions (see L1's corrected bullet) — not a risk. The real headless
   surface is the local `claude` children launched under `--dangerously-skip-permissions --tools default`
   (`runner.py:378,384`; `ensemble.py:340-348`; lever at `pipeline/process.py:93,133-134`). L1b hardens
   them with a non-mutating tool profile; until L1b lands, an unattended headless reflect run could in
   principle have a scorer/Tier-1 child run destructive git — a strictly worse failure mode than the
   interactive incident because no operator is watching.
3. **MCP read-only tools that can still mutate.** `mcp__serena__write_memory`/`edit_memory`/
   `delete_memory` mutate Serena memory (not repo state, but still state). The `reflect-reviewer` grant
   above deliberately excludes them; the corrective task must keep them out.
4. **Advisory-only L4** can be ignored — hence it is ranked last and never load-bearing.

**Conclusion:** With L1+L2+L5 (all mechanical) the specific incident — a reviewer subagent running
`git reset --hard`/`git stash` against a shared dirty tree — becomes **impossible without two
simultaneous deliberate regressions**, one of which trips CI. Residual risk concentrates in the
orchestrator's own (operator-visible, denylist-guarded, template-only) shell — a far smaller and
better-understood surface than "every adversarial reviewer holds Bash."

---

## 5. Test / eval plan (consolidated)

| Test | Layer | Level | Asserts |
|------|-------|-------|---------|
| `test_reviewer_readonly_tools.py` | L1, L5 | static unit | `reflect-reviewer.md` tools ∩ mutators == ∅; SKILL Step 3B names `reflect-reviewer`, not an all-tools persona |
| `test_claudeprocess_reflect_children_restricted.py` | L1b | static unit | reflect-spawned `ClaudeProcess` argv (scorer/Tier-1/orchestrator) drops `--tools default` + skip-permissions for a non-mutating profile |
| `test_reviewer_isolation_gate.py` | L2 | integration | dirty-tree UC-2 → snapshot-under-`<output>/` or `stopped-precondition`; reviewer root != shared worktree |
| `test_verify_denylist_git_mutations.py` | L3 | unit/grader | denylist → `mutation-denied` for `git reset/stash/checkout/clean` |
| `test_reviewer_brief_constraints.py` | L4 | grader | every `reviewer-<N>.md` has `## Constraints (READ-ONLY)`; no live-exec instructions |
| `test_reviewer_no_mutation_ledger.py` | L5 | grader/eval | recorded reviewer ledger has zero mutating tool calls; falsifier fixture (reviewer-attempts-`git reset`) is flagged |

All under `tests/cli/reflect/` + `.dev/eval-workspaces/sc-reflect/` (grader + falsifier fixtures),
consistent with the existing reflect test/eval layout. Each test must **fail on the current tree**
(reviewer = all-tools persona) and **pass after** the L1-L5 edits — the standard falsifier discipline.

---

## 6. Recommended follow-up (DO NOT auto-run)

A corrective MDTM task is warranted. **Recommended, not executed** (this session is read-only):

> `/task-builder` BUILD_REQUEST: "Harden /sc:reflect Wave-3 reviewer spawning against repository
> mutation. Implement L1 (new restricted `reflect-reviewer` agent + repoint Step 3B/§7.1 spawn,
> interactive AND swarm paths), L2 (Wave-0 Step 0.5e clean-tree/isolated-snapshot gate in
> SKILL.md + runner.py/commands.py/ensemble.py), L3 (extend §6.1.1 denylist SKILL.md:519 +
> sole-shell-surface invariant), L4 (reviewer-spec.md READ-ONLY brief preamble + remove live-exec
> instruction from Step 3B.0), L5 (the six tests in §5). Source-of-truth edits in src/superclaude/
> then `make sync-dev` + `make verify-sync`. Cite this proposal and the forensics file."

Suggested adversarial framing for the build (per project memory `feedback_rfqa_adversarial_pattern`):
pair an explicit ADVERSARIAL STANCE with `fix_authorization: true` on the rf-qa gate, and run
`/sc:reflect --mode pre --depth deep` on the resulting tasklist (UC-1) as the pre-execution check —
**after** L1/L2 land, so that very pre-check runs with read-only reviewers.

### Build & validation environment (execution logistics — validated 2026-06-22)

These govern *where* the guard is built/validated, not its design. They are the L1/L2 reliability
principles applied to our own implementation work (verified against repo state this date):

- **Build the guard in a dedicated, committed-clean worktree** — not in this worktree and not in main.
  Rationale (load-bearing): this worktree is **dirty (19 uncommitted entries)** and main carries **5
  stashes** + is on `master`; building/validating here would run `/sc:reflect` against a dirty shared
  tree — the exact precondition L2 exists to forbid (dogfood L2). PR-scope isolation is the secondary
  reason. (The shared-index hazard of `feedback_parallel_sessions_share_index` only bites under
  *concurrent* sessions; the dirty-tree + PR-scope reasons are the decisive ones.)
- **Base the guard branch on `ReflectHardening-3`, as a separate branch, stacked on / after #199 —
  not on `master`, not committed onto the #199 branch.** Verified: L1b edits `run_adversarial_scorer`
  (`ensemble.py:340`) + the Tier-2 swarm routing, which are **FR-RH2 code that exists only on
  `ReflectHardening-3`** (`576aadff`/`6c32eaf0` are branch-only; those symbols return 0 on
  `origin/master`). Basing on `master` would leave L1b with no substrate to edit or test. The #199 tip
  `c9372152` is pushed and under Augment review — committing the guard there re-scopes the PR. The
  author's "swap base to `origin/master` if the guard touches no FR-RH2 code" decision-rule is **moot**
  — confirmed it does touch FR-RH2 code. **Caveat:** if #199 is force-pushed after review changes,
  rebase the guard branch onto the new tip.
  - Setup (single-line, absolute paths): `git -C /config/workspace/IronClaude worktree add /config/workspace/IronClaude/.dev/worktrees/reflect-reviewer-guard -b feat/reflect-reviewer-guard ReflectHardening-3`
- **Validate on the committed-clean guard worktree.** In a clean tree a stray `git reset --hard HEAD`
  is a no-op. Leave main's 5 stashes alone — they are legitimate other-session work and
  `reference_worktree_merge_head_path` warns against clobbering others' stashes. The stash-pop footgun
  in main is inert post-L1 (a read-only reviewer has no `Bash`/`git` to trigger it); the guard's
  acceptance test is precisely *"does the reviewer now refuse the mutation."*

### Exact edit-location index (for the corrective task)
- `src/superclaude/agents/reflect-reviewer.md` — **new**, restricted `tools:` (L1).
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — `:151,:160-162,:176,:323-325,:505-507,:519,:588,:602-612` (L1/L2/L3).
- `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` — `:9-23,:72-100` (L1 spawn-type doc, L4 brief preamble).
- `src/superclaude/cli/reflect/{runner.py,commands.py,ensemble.py}` — Step 0.5e isolation gate (L2) + restricted `ClaudeProcess` profile at the scorer/Tier-1/orchestrator launches (L1b).
- `src/superclaude/cli/pipeline/process.py` — add `tool_profile`/`allowed_tools` param (`:85-108`) consumed in `_build_command` (`:127-142`); today pins `--tools default` + skip-permissions (L1b).
- `tests/cli/reflect/*` + `.dev/eval-workspaces/sc-reflect/grader.py` (+ falsifier fixtures) — L5.

---

### Appendix — citation ledger (verified this session)
- Reviewer spawn = persona-as-agent-type, no tool restriction: `SKILL.md:151,323-325`,
  `refs/reviewer-spec.md:82-92`, Phase A §0.1.
- All-tools personas: `agents/quality-engineer.md`, `agents/root-cause-analyst.md`,
  `agents/refactoring-expert.md` (no `tools:` line). Read-only exemplars: `agents/evidence-validator.md`
  (`tools: Read, Grep, Glob`), `agents/reuse-auditor.md` (read-only set).
- Read-only "guarantee" is prose: `SKILL.md:160-162,176`.
- Envelope scope = orchestrator verification triangle only: `SKILL.md:499,505-519`; denylist gap
  (no git reset/stash/checkout): `SKILL.md:519`.
- Self-contained-brief design the incident violated: `refs/reviewer-spec.md:19,43`.
- UC-2 audits a committed diff by design: `reflect.md:44,174`; STOP-precondition pattern: `reflect.md:30-35`.
- Orchestrator-only spawn discipline already stated elsewhere: `SKILL.md:472,501`.
- Swarm-path second spawn route: commit `576aadff` (`src/superclaude/cli/reflect/ensemble.py`).
