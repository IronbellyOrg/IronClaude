# Feature Characterization — Tier Classification Model

**Task:** T02.01 — Characterize tier classification model & classification header emission
**Roadmap Item:** R-004
**Donor Catalog Anchor:** D09 (priority-ordered tier rules) — see `donor-feature-catalog.md` line 55
**Side of Truth (R-RULE-10):** `src/superclaude/commands/task.md` (canonical) — byte-identical to `.claude/commands/sc/task.md`
**Generated:** 2026-05-15

---

## 1. What It Is

A four-tier priority-ordered classification model that maps an incoming `/sc:task` invocation to one of `{STRICT, STANDARD, LIGHT, EXEMPT}` plus a numeric confidence score. The tiers are not equal categories — they are a *priority cascade* with deterministic precedence (STRICT > EXEMPT > LIGHT > STANDARD) and an explicit low-confidence escape hatch at <0.70.

It is the routing brain of the `/sc:task` command surface: it is the only mechanism that decides whether the command terminates inside itself (EXEMPT, LIGHT), invokes the protocol skill (STANDARD, STRICT), or stalls for user override.

## 2. How It Works (Mechanism + Entry/Exit Conditions + `file:line` Evidence)

**Mechanism (priority cascade, first-match-wins):**

1. **STRICT (Priority 1, safety-critical)** — `src/superclaude/commands/task.md:71-75` (`src/`)
   - Keyword trigger set: `security, authentication, authorization, database, migration, refactor, breaking change, encrypt, token, session, oauth`
   - Context boosters: `>2 estimated files (+0.3)`, security paths `auth/`, `security/`, `crypto/` `(+0.4)`
   - Compound phrases handled: `"fix security"`, `"add authentication"`, `"update database"`, `"change api"`
   - Trump rule: `"quick security" → still STRICT (security always wins)`; `"minor auth change" → still STRICT` (line 75)

2. **EXEMPT (Priority 2, non-code)** — `src/superclaude/commands/task.md:77-80` (`src/`)
   - Keyword trigger set: `explain, search, commit, push, plan, discuss, brainstorm, what, how, why`
   - Context boosters: `is_read_only (+0.4)`, `is_git_operation (+0.5)`, all doc files `(+0.5)`
   - Pattern triggers: starts with `"what/how/why/explain"`; docs-only paths `*.md`, `docs/`

3. **LIGHT (Priority 3, trivial)** — `src/superclaude/commands/task.md:82-85` (`src/`)
   - Keyword trigger set: `typo, comment, whitespace, lint, docstring, formatting, spacing, minor`
   - Context boosters: single file `(+0.1)`, `<=50 lines estimated`
   - Compound phrases: `"quick fix"`, `"minor change"`, `"fix typo"`, `"refactor comment"`

4. **STANDARD (Priority 4, default)** — `src/superclaude/commands/task.md:87-89` (`src/`)
   - Keyword trigger set: `implement, add, create, update, fix, build, modify, change`
   - Behavior: fallback tier when no higher-priority match occurs.

**Entry conditions:**
- The user invokes `/sc:task <prompt> [--compliance X]`.
- The command parser checks `--compliance` first — if present, override path is taken (`src/superclaude/commands/task.md:69` says: "check `--compliance` override first").
- Otherwise classification runs over the prompt text.

**Exit conditions:**
- A tier is selected (the first-matching rule wins) AND a confidence score is computed.
- If `confidence < 0.70` → exit branch (B): prompt user to `"Override with --compliance [tier]"` (`src/superclaude/commands/task.md:91`).
- Otherwise → exit branch (A): proceed to header emission and dispatch.

**Auxiliary references:**
- The protocol skill repeats a stripped tier-keyword reference (for context only, NOT to re-classify) at `src/superclaude/skills/sc-task-protocol/SKILL.md:53-57` (`src/`).
- The protocol skill's `Behavioral Flow → 0. Classification (Already Performed)` section at `src/superclaude/skills/sc-task-protocol/SKILL.md:49-51` (`src/`) confirms classification runs at the *command* layer, before skill invocation — the skill itself does NOT re-classify.

## 3. What It Produces

- A tier label ∈ `{STRICT, STANDARD, LIGHT, EXEMPT}` (no other values valid — see `src/superclaude/commands/task.md:55`).
- A confidence score in `[0.00, 1.00]`.
- A keyword-match list (the matched substrings that drove the decision).
- A one-line rationale.
- An `OVERRIDE` flag (`true` if `--compliance` was supplied, else `false`).

These five values populate the classification header (feature D08, see `feature-classification-header.md`) and drive the dispatch decision at `src/superclaude/commands/task.md:93-101`.

## 4. What Invokes It

- The `/sc:task` command's `Classification (MANDATORY FIRST OUTPUT)` section is the sole invocation point — `src/superclaude/commands/task.md:50-91` (`src/`).
- It is invoked **exactly once per command invocation**, before any tool call (Critical Rule 1, `src/superclaude/commands/task.md:53`: "TEXT-ONLY: Do NOT invoke ANY tools (Skill, Read, Grep, etc.) for classification. Tool invocation begins AFTER classification.").
- The `auto-trigger` heuristic surface at `src/superclaude/commands/task.md:29-36` (`src/`) — Complexity Score, Multi-file Scope, Security Domain, Refactoring keywords — is the *upstream* surface that *brings the user to* `/sc:task`; once inside, the priority-cascade is what fires.

## 5. What It Depends On

- **Static keyword tables** — embedded inline in `src/superclaude/commands/task.md:72,78,83,88` (`src/`). Externalized targets at `config/tier-keywords.yaml` are *referenced* (`src/superclaude/skills/sc-task-protocol/SKILL.md:361`) but the file does NOT exist in the repo (see D32 in catalog).
- **Compound-phrase recognition** — implicit in the LLM's prompt-interpretation (the model recognises `"fix security"` as a compound rather than as `"fix"` ∪ `"security"`). There is no separate tokenizer.
- **Context booster signals** — file count, path patterns, line estimates. These require the LLM to *estimate* prior to any tool call (Critical Rule 1's text-only constraint forbids reading the filesystem to confirm).
- **The `--compliance` flag parser** — must run before classification so override-path can pre-empt (`src/superclaude/commands/task.md:69`).
- **The escalation philosophy** — `"Better false positives than false negatives"` (`src/superclaude/commands/task.md:27`) — informs how tie-breaks resolve when two tiers' keyword sets overlap.

## 6. Standalone Value Claim

**Claim:** The tier classification model adds a *deterministic, priority-ordered cost-routing decision* to a recipient that currently has no such routing. Without it, every task pays the same execution overhead regardless of risk (a typo fix pays the same as a security migration). With it, the recipient can branch: skip verification on EXEMPT/LIGHT (`src/superclaude/skills/sc-task-protocol/SKILL.md:118-119`), run direct test execution on STANDARD, spawn a verification sub-agent on STRICT (`src/superclaude/skills/sc-task-protocol/SKILL.md:114-117`). For a 10-item tasklist mixing typos and security-domain changes, this is the difference between paying STRICT cost (3-5K tokens, 60s) on all 10 vs. on the 2 that need it — a 4-5× token-budget reduction *if and only if* the tier mix is heterogeneous.

**Non-value condition (R-RULE-04, concrete, not boilerplate):**

The value claim does NOT hold when the recipient's task mix is homogeneous within a session — specifically:

- If every task in a session is STANDARD (the default when no higher-priority match occurs, `src/superclaude/commands/task.md:87-89`), classification produces a constant output and adds *only* the cost of running the classifier (token spend for the priority cascade + header emission, ~150-300 tokens per task) without any branching benefit. For a 20-task tasklist where every item is "add", "update", "implement" (which all map to STANDARD per line 88), the classifier costs ~3-6K tokens cumulatively and changes zero routing decisions vs. a single hard-coded "always run STANDARD verification" rule.
- Additionally: the model trusts the LLM's *unverified* estimate of file count and path patterns at classification time (Critical Rule 1 forbids tool calls — `src/superclaude/commands/task.md:53`). If the LLM's estimate is wrong (e.g. it classifies a 12-file refactor as LIGHT because the prompt said "minor"), classification confidently routes the task to the wrong tier and the value inverts into harm.

## 7. Coupling Cost Claim

**Claim:** Attaching the tier classification model to `/task` requires the recipient to take on **all five** of the following concrete burdens; partial adoption is shape-incompatible.

1. **A pre-loop classification step inside `/task`'s session lifecycle.** `/task`'s entry point is the Task File Validation gate at `src/superclaude/skills/task/SKILL.md:64-73` (`src/`), which checks frontmatter and well-formedness — *not* prompt classification. Adding classification here requires inventing a new step that runs *before* the F1 loop entry, OR pushing classification up to the `task-builder` skill (which builds the task file from a request) at the `task-builder/SKILL.md` boundary. Either way, the recipient must extend its lifecycle.

2. **A `Tier:` field in the per-item or per-task schema.** `/task`'s required frontmatter schema slot at `src/superclaude/skills/task/SKILL.md:69` (`src/`) requires only `id, title, status, created_date`. Tier-driven dispatch depends on the tier being attached *somewhere* on the task file — either as task-level frontmatter or as per-item annotation. The recipient must extend the schema and the validation logic that reads it.

3. **Resolution of the compound-phrase / context-booster non-determinism.** The donor model relies on the LLM to recognise compound phrases (`"fix security"`) and to *estimate* context boosters (`>2 files`, security paths) without tool calls. `/task` operates from a task file produced upstream — file paths and scope are *already known* by the time `/task` runs, so the booster signals can either be (a) re-computed deterministically from the task file (eliminating the LLM-estimation risk but requiring new logic) or (b) inherited from a prior classification step (creating a cross-skill data-flow contract that `/task` currently does not have).

4. **A keyword-table location decision.** Donor keeps the tables inline (`src/superclaude/commands/task.md:72,78,83,88`); the protocol skill references `config/tier-keywords.yaml` (`src/superclaude/skills/sc-task-protocol/SKILL.md:361`) which does not exist. The recipient must decide: inline duplication, externalized YAML, or hand-off via a producer (task-builder) — each choice imposes a different maintenance contract on the recipient. `/task` currently has no YAML/configuration externalization pattern.

5. **A confidence-threshold concept and a low-confidence stall path.** `/task` has no confidence-threshold model anywhere (confirmed by D30 partial-match note in the donor catalog and by absence in the recipient extension points file). The donor's <0.70 stall behavior (`src/superclaude/commands/task.md:91`) requires inventing a user-facing override prompt path inside `/task`'s otherwise non-interactive F1 loop. This is a behavioral surface area extension, not a code addition.

**Net coupling cost:** the recipient must extend its lifecycle (1), schema (2), data-flow contract (3), configuration discipline (4), and interactive-surface (5) — five distinct extensions, not a single drop-in.

---

## Cross-Reference

- D09 in `donor-feature-catalog.md` (tier classification model) — primary anchor.
- D08 in `donor-feature-catalog.md` (classification header emission) — output sink for this feature; see `feature-classification-header.md`.
- D14 (human-readable confidence display) — downstream consumer; depends on this feature existing.
- D10/D15 (per-tier dispatch / per-tier execution workflows) — downstream consumer; the *reason* this feature has value.
- D04 (Compliance axis) — partial match against `/task`'s tasklist-layer `Tier:` field; net-upgrade question logged for Phase 4.
