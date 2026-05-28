# Feature Characterization — Triggering Surface (`/sc:task` invocation vs `/task` invocation)

**Task:** T02.03 — Characterize MCP declarations, persona activation, allowed-tools, compliance gating, triggering surface
**Roadmap Item:** R-006
**Donor Catalog Anchors:** D06 (Auto-trigger heuristics table), D13 (Auto-Suggest Keywords hint table) — see `donor-feature-catalog.md` lines 52, 64
**Side of Truth (R-RULE-10):** `src/superclaude/commands/task.md` and `src/superclaude/skills/sc-task-protocol/SKILL.md` (canonical for donor); `src/superclaude/skills/task/SKILL.md` (canonical for recipient) — byte-identical to `.claude/` mirrors
**Generated:** 2026-05-15

---

## 1. What It Is

The **triggering surface** is the set of conditions and pathways through which a user causes `/sc:task` (donor) or `/task` (recipient) to fire. The two have fundamentally different shapes:

- **Donor (`/sc:task`):** Triggered by a **free-text prompt** in conversation. Activation is either (a) explicit (user types `/sc:task <prompt>`) or (b) heuristic-driven by upstream auto-trigger logic that watches for complexity, multi-file scope, security-domain paths, or refactoring keywords in *any* user prompt and offers `/sc:task` as a suggested command.
- **Recipient (`/task`):** Triggered by a **task-file path** plus a verbal phrase. Activation is either (a) explicit (user types `/task <path>` or invokes the Skill tool with `name: task` and a path argument) or (b) phrase-driven via the skill description's trigger phrases ("execute this task file", "run this task", "process this task", "resume the task", etc.) which the Claude Code skill loader matches against the user's natural language.

The two surfaces share the *word* "task" but otherwise share almost nothing — the donor takes a prompt-string and infers what to do; the recipient takes a structured-file-path and executes a pre-built work plan.

## 2. How It Works (Mechanism + Entry/Exit Conditions + `file:line` Evidence)

### Donor side — `/sc:task` triggering

**Mechanism (heuristic surface + explicit command):**

The donor advertises four auto-trigger heuristics at `src/superclaude/commands/task.md:29-36` (`src/`):

```
| Trigger Type         | Condition                                       | Confidence |
| Complexity Score     | Task complexity >0.6 with code modifications    | 90%        |
| Multi-file Scope     | Estimated affected files >2                     | 85%        |
| Security Domain      | Paths contain `auth/`, `security/`, `crypto/`   | 95%        |
| Refactoring Scope    | Keywords: refactor, remediate, multi-file       | 90%        |
```

And the protocol skill adds an Auto-Suggest Keywords table at `src/superclaude/skills/sc-task-protocol/SKILL.md:33-35` (`src/`):

```
High confidence: "implement feature", "refactor system", "fix security",
                 "add authentication", "update database schema"
Moderate confidence: "add new", "create component", "update service", "modify API"
```

- **Entry condition (explicit):** User types `/sc:task <prompt>` or `/sc:task <prompt> --compliance <tier>`.
- **Entry condition (heuristic):** An upstream surface — the command-routing layer or auto-suggest engine — watches user prompts for matches against the four heuristic rows or the auto-suggest keyword list. On a match, it surfaces `/sc:task` as a recommended invocation.
- **Mechanism:** The user is the gating decision-maker — heuristics surface recommendations, the user accepts/rejects. There is no auto-execution. Once the user types `/sc:task <prompt>`, control transfers to the command body which begins with classification (see `feature-tier-classification.md`).
- **Exit condition:** Either the user invokes `/sc:task` (control passes into the command) or declines (the heuristic surface had no further effect).

### Recipient side — `/task` triggering

**Mechanism (skill-loader trigger phrases + explicit invocation):**

The recipient's trigger surface lives in the skill's frontmatter description at `src/superclaude/skills/task/SKILL.md:3` (`src/`):

```
description: "Execute an MDTM task file — process checklist items sequentially
with the F1 execution loop ... Trigger on phrases like 'execute this task file',
'run this task', 'process this task', 'resume the task', 'pick up where we left
off', 'continue the task', or when the user provides a path to a .md file in
.dev/tasks/ and wants it executed. Also trigger when the user says '/task'
followed by a file path or task identifier."
```

The skill defines five strong-input examples at `src/superclaude/skills/task/SKILL.md:37-40` (`src/`):

```
- `execute .dev/tasks/to-do/TASK-SKILL-TRANSFORM-20260308-tech-reference/...`
- `resume the tech-reference transformation task`
- `/task .dev/tasks/to-do/TASK-SKILL-TRANSFORM-20260308-tech-reference/...`
```

And a discovery protocol at `src/superclaude/skills/task/SKILL.md:46-51` (`src/`) for the weak-input case (no path):

```
1. Search .dev/tasks/to-do/ for TASK-*/ folders with status "🟠 Doing"
2. If exactly one found, resume it
3. If multiple found, list candidates and ask
4. If none found, search for status "🟡 To Do" and list candidates
5. If still none, inform the user
```

- **Entry condition (explicit-path):** User provides a task-file path explicitly (typed as `/task <path>` or "execute this task file <path>").
- **Entry condition (identifier):** User provides an identifier substring; the skill searches `.dev/tasks/to-do/` to resolve.
- **Entry condition (no path):** User says a generic trigger phrase ("continue the task", "resume"); the skill auto-discovers in-progress task folders.
- **Mechanism:** The Claude Code skill loader matches the user's prompt against the skill's description's trigger phrases. On match, the skill is invoked via the Skill tool. The skill then resolves the task-file path (or auto-discovers) and enters the F1 loop.
- **Exit condition:** Skill is invoked → task-file resolved → F1 loop begins, or the skill reports "no task files found" and exits.

### Explicit contrast — `/sc:task` invocation vs `/task` invocation

| Dimension | `/sc:task` (donor) | `/task` (recipient) |
|---|---|---|
| **Input type** | Free-text prompt describing work to do | Task-file path (or identifier) |
| **First action** | Emit classification header (`src/superclaude/commands/task.md:50-67`, `src/`) | Validate task-file well-formedness (`src/superclaude/skills/task/SKILL.md:64-73`, `src/`) |
| **Trigger surface** | Heuristic auto-trigger table + auto-suggest keywords (`src/superclaude/commands/task.md:29-36`, `src/`; `src/superclaude/skills/sc-task-protocol/SKILL.md:33-35`, `src/`) | Skill-description trigger phrases (`src/superclaude/skills/task/SKILL.md:3`, `src/`) + path/identifier resolution |
| **Producer of work plan** | Inferred from prompt during classification (work-plan is implicit) | Read from disk (task file is the work plan) |
| **Iteration model** | Single command turn produces single classification → dispatch → execute | F1 loop iterates over checklist items; one task-file invocation can span many turns and sessions |
| **Resumability** | Stateless — each `/sc:task` invocation is fresh | Stateful — task file on disk is the source of truth; resumption protocol at `src/superclaude/skills/task/SKILL.md:268-283` (`src/`) reads first unchecked item |
| **Multi-item model** | One prompt → one task | One task file → many `- [ ]` items, executed sequentially |
| **Cross-session continuity** | None (each turn independent) | Survives compression and session restart (Three Guarantees, `src/superclaude/skills/task/SKILL.md:18-21`, `src/`) |
| **User-visible first output** | The classification header (`src/superclaude/commands/task.md:56`, `src/` — "MUST be your very first output") | A validation report and a status flip to "🟠 Doing" |
| **Surface for command flags** | Yes — 8 documented flags (`src/superclaude/commands/task.md:44-48`, `src/`) | No — invocation is path-based, not flag-based |

The two surfaces are **non-substitutable**: a user with a free-text prompt cannot trivially invoke `/task` (they would need to first build a task file via `task-builder`); a user with a pre-built task file cannot trivially invoke `/sc:task` (the command would attempt to re-classify the prompt rather than execute the file).

## 3. What It Produces

- **Donor produces:** a routing decision ("does the user actually invoke `/sc:task`?") at heuristic time, and at invocation time the donor immediately produces the classification header (D08) before any tool call.
- **Recipient produces:** a skill-invocation decision ("does the user's phrase trigger the `task` skill?") at the skill-loader, and at invocation time the recipient produces (a) a discovered task-file path or list of candidates, (b) a task-file validation report, (c) a status flip to "🟠 Doing".
- **Neither produces a persistent telemetry artifact for the trigger event** — the auto-trigger heuristics and the skill description's trigger phrases both fire transiently. There is no log file recording "auto-trigger row matched at 12:34Z."

## 4. What Invokes It

- **Donor side:** The Claude Code prompt-input pipeline. When the user submits a prompt, the framework checks for the literal `/sc:task` token (or for the auto-trigger heuristics, which run upstream as part of command recommendation). On match, control transfers to the donor's command body.
- **Recipient side:** The Claude Code skill loader. The loader scans the available skills' frontmatter descriptions at each user prompt and selects the best-matching skill. The `task` skill's description (`src/superclaude/skills/task/SKILL.md:3`, `src/`) is long and contains many trigger phrases — it is specifically tuned to be matched on common task-execution requests.
- **Neither has an internal invoker** — both are user-triggered or framework-triggered, never invoked by other commands/skills in this repo (verified by `grep -r "Skill task" src/superclaude/` returning only references, not internal invocations from other commands/skills).

## 5. What It Depends On

**Donor depends on:**
- An upstream auto-trigger / command-recommendation surface that recognizes the four heuristic conditions. This surface is NOT in this repo — the donor file *advertises* the heuristics but does not implement the matcher.
- The user knowing to type `/sc:task` explicitly. Without the auto-trigger surface working, the donor is invoked only on explicit typing.
- A prompt that the classifier can reasonably tier. If the prompt is ambiguous, classification confidence drops below 0.70 and the user is asked to override (`src/superclaude/commands/task.md:91`, `src/`).

**Recipient depends on:**
- The Claude Code skill loader matching trigger phrases. The skill's description at `src/superclaude/skills/task/SKILL.md:3` (`src/`) is the *only* recipient-side trigger declaration.
- A pre-built task file existing at the cited path, OR an in-progress task folder discoverable in `.dev/tasks/to-do/` (per `src/superclaude/skills/task/SKILL.md:46-51`, `src/`).
- The `task-builder` skill (or equivalent) having previously built the task file. The recipient does NOT build task files itself — `src/superclaude/skills/task/SKILL.md:12` (`src/`) explicitly states "It does not create task files (use `rf:task-builder` for that)."
- A path convention that locates task files in `.dev/tasks/to-do/TASK-[ID]/TASK-[ID].md` (the centralized path convention at `src/superclaude/skills/task/SKILL.md:35`, `src/`).

## 6. Standalone Value Claim

**Claim:** The two triggering surfaces serve distinct, complementary value propositions:

- **Donor (`/sc:task`) value:** Low-friction entry from free-text. A user mid-conversation can invoke `/sc:task "fix the SQL injection in login.py"` and the system handles classification, dispatch, MCP routing, verification, TFEP — without the user first authoring a task file. For ad-hoc work, this is order-of-magnitude faster than building a task file via `task-builder` then invoking `/task`. Heuristic auto-triggering further lowers friction by surfacing the command when the user's prompt already smells like one of the four trigger conditions.

- **Recipient (`/task`) value:** Survives context compression and session restart. The task file is the durable work plan; the recipient is the durable executor. For multi-phase, multi-session, multi-item work — anything where a single conversation turn is insufficient — `/task` is the only path. The user spends upfront cost on building the task file (via `task-builder`) and earns durability + auditability + resumability in return. The triggering surface is naturally narrower because the invocation is a deliberate "execute this plan" action, not an ad-hoc request.

The complementarity argues that **both triggering surfaces should exist** — they cover non-overlapping use cases. A unified-surface argument would have to deprecate one shape (lose either prompt-driven ad-hoc work OR pre-built-plan execution).

**Non-value condition (R-RULE-04, concrete, not boilerplate):**

The value claim does NOT hold under these specific conditions:

- **Donor heuristic surface is unverifiable from this repo.** The auto-trigger heuristics at `src/superclaude/commands/task.md:29-36` (`src/`) describe four conditions and confidence levels — but no file in this repo implements the matcher. `grep -r "Complexity Score" src/superclaude/` finds the table and references but no executable rule. If the heuristic layer is not provided by Claude Code core, the donor's "low-friction entry" reduces to "user must remember to type `/sc:task`," which is no friction reduction over typing `/task <path>`. The value is contingent on infrastructure not present here.
- **Recipient trigger phrases overlap with non-task work.** Phrases like "continue the task" and "run this task" are common in conversational programming work that has nothing to do with MDTM task files. The skill loader may either (a) over-trigger (invoke `task` on prompts that meant something else) and force the user into the discovery protocol unnecessarily, or (b) under-trigger if a phrase like "let's keep working on this" doesn't match. Without telemetry on actual trigger accuracy (which this repo does not collect), the value claim is unfalsifiable.
- **Both surfaces fail when the user uses the *other* shape.** A user with a task file in `.dev/tasks/to-do/` who accidentally types `/sc:task "execute this task"` will trigger classification on the prompt-text "execute this task" (probably classifies EXEMPT or LIGHT) rather than executing the file. Conversely, a user with a free-text request who says "/task fix the bug" will trigger the skill loader on `/task`, which will then search for a "fix the bug" task file, fail to find one, and offer the discovery menu. The two surfaces are not gracefully interoperable.
- **`/sc:task`'s value depends on the entire donor stack (D08-D27) working.** If classification miscategorizes, MCP gates misfire, verification routing skips when it shouldn't — the low-friction entry has delivered the user to an unsafe execution. The friction-reduction value is gated by every downstream gate's value (see `feature-compliance-gating.md`). `/task`'s value is more localized — its trigger surface delivers the user to the F1 loop, which has been proven robust independently.

## 7. Coupling Cost Claim

**Claim:** Adopting any portion of the donor's triggering surface into `/task` requires the recipient to take on **all four** of the following concrete burdens:

1. **A free-text prompt-handling layer on a path-driven skill.** `/task` consumes a task-file path or identifier (`src/superclaude/skills/task/SKILL.md:30-33`, `src/`). The donor's heuristic surface assumes a free-text prompt. Adding heuristic auto-triggering to `/task` requires either (a) extending `/task` to accept free-text prompts (and inferring a task-file from them, which duplicates `task-builder`), or (b) routing the heuristic to `task-builder` instead (which forces an upstream tooling change). Neither preserves `/task`'s current shape.

2. **Heuristic-matcher implementation.** The donor's four heuristic conditions (`src/superclaude/commands/task.md:29-36`, `src/`) are advertised but not implemented. If the recipient wants the value, it must implement the matcher itself: tokenize the prompt, count "estimated affected files," detect security-domain paths, recognize refactoring keywords. None of these matchers exist in this repo on the recipient side; building them adds a new responsibility area entirely.

3. **Reconciliation with the existing skill-description trigger phrases.** `/task`'s description at `src/superclaude/skills/task/SKILL.md:3` (`src/`) is already a sophisticated trigger surface (multiple phrases, path-detection, identifier-detection). Adding donor-style heuristics on top creates two layered trigger systems — one based on phrases ("execute this task"), one based on content heuristics (security keywords). When both fire on the same prompt, which wins? The recipient must define precedence, document it, and verify the Claude Code skill loader honors the rule.

4. **A non-substitutability disclaimer at the trigger boundary.** The two surfaces are fundamentally non-substitutable (free-text vs file-path). If `/task` is augmented to accept free-text, the recipient must either (a) build the task-file inline (becomes `task-builder` + `/task` fused), (b) reject free-text with a clear message ("`/task` requires a path or identifier — did you mean `/sc:task`?"), or (c) silently fall through to the discovery protocol on a free-text input (the current behavior — but with heuristics enabled, this is misleading). The recipient must commit to disambiguation behavior at the trigger boundary.

**Net coupling cost:** the recipient must build a prompt-handling layer where none exists (1), implement four heuristic matchers (2), reconcile with the existing trigger-phrase system (3), and commit to a non-substitutability disambiguation rule (4) — four extensions, with the central issue that the donor and recipient have *fundamentally incompatible* input shapes (prompt vs path) and adopting donor-side triggering on the recipient side dissolves the recipient's input-shape invariant.

The honest answer to the Phase 4 net-upgrade question is likely "the triggering surface should NOT transfer" — instead, the donor's heuristics belong upstream of `task-builder`, where they can decide whether to *build a task file* (which then triggers `/task`) rather than trigger `/task` directly. This is recorded here for adversarial debate in Phase 4 rather than asserted as a final position.

---

## Cross-Reference

- D06 in `donor-feature-catalog.md` (Auto-trigger heuristics table) — primary anchor for the donor's heuristic surface.
- D13 in `donor-feature-catalog.md` (Auto-Suggest Keywords hint table) — adjunct keyword-driven trigger; tagged NON-TRANSFERABLE in the donor catalog because `/task` is not surfaced via prompt-auto-suggest.
- D07 in `donor-feature-catalog.md` (Flag set) — adjacent surface (flags are post-trigger configuration); see `feature-compliance-gating.md` coupling cost #6 for flag-encoding burdens.
- `feature-tier-classification.md` — describes what happens *after* the donor's triggering surface fires.
- `feature-compliance-gating.md` — describes the gates the donor's trigger leads into.
- Recipient skill description (`src/superclaude/skills/task/SKILL.md:3`, `src/`) — the recipient's analogous (but shape-different) trigger surface.
- Recipient discovery protocol (`src/superclaude/skills/task/SKILL.md:46-51`, `src/`) — the recipient's fallback when no path is provided.
- `task-builder` skill (referenced at `src/superclaude/skills/task/SKILL.md:12`, `src/`) — the producer of the task files that `/task` consumes; a candidate alternative landing site for the donor's heuristic surface.
