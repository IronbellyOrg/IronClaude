# Feature Characterization — Classification Header Emission

**Task:** T02.01 — Characterize tier classification model & classification header emission
**Roadmap Item:** R-004
**Donor Catalog Anchor:** D08 (classification header emission — exact-format rule) — see `donor-feature-catalog.md` line 54
**Side of Truth (R-RULE-10):** `src/superclaude/commands/task.md` (canonical) — byte-identical to `.claude/commands/sc/task.md`
**Generated:** 2026-05-15

---

## 1. What It Is

A **machine-parseable telemetry sentinel** emitted as the very first textual output of `/sc:task`, consisting of an HTML comment-bracketed block carrying five fields: `TIER`, `CONFIDENCE`, `KEYWORDS`, `OVERRIDE`, `RATIONALE`. The header is *text only* — no tool call accompanies it — and is bounded by `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` open and `<!-- /SC:TASK-UNIFIED:CLASSIFICATION -->` close markers.

It is the *contract surface* between classification (an LLM-internal decision) and any downstream consumer (telemetry pipeline, A/B test framework, dispatch logic, human reader). Without the header, classification is unobservable; with it, classification becomes auditable post-hoc by simple regex.

## 2. How It Works (Mechanism + Entry/Exit Conditions + `file:line` Evidence)

**Mechanism — four CRITICAL RULES (`src/superclaude/commands/task.md:50-67`, `src/`):**

1. **TEXT-ONLY** (`src/superclaude/commands/task.md:53`, `src/`): "Do NOT invoke ANY tools (Skill, Read, Grep, etc.) for classification. Tool invocation begins AFTER classification." This rule binds the entire pre-header span — the model may not call Read to verify file counts, may not call Grep to confirm path patterns; classification is whatever the model infers from the prompt text alone.

2. **EXACT FORMAT** (`src/superclaude/commands/task.md:54`, `src/`): "Use the HTML comment block below EXACTLY. Do NOT use `**CLASSIFICATION: ...**` or any other format." The HTML-comment delimiter is the parser anchor.

3. **VALID TIERS ONLY** (`src/superclaude/commands/task.md:55`, `src/`): "The ONLY valid TIER values are: `STRICT`, `STANDARD`, `LIGHT`, `EXEMPT`. Values like 'ITERATIVE', 'SIMPLE', 'IMPLEMENT', 'COMPLEX' are INVALID and MUST NOT be used." The closed enumeration is enforced by re-statement in the worked-examples preamble at `src/superclaude/commands/task.md:104` (`src/`).

4. **FIRST OUTPUT** (`src/superclaude/commands/task.md:56`, `src/`): "This header MUST be your very first output, before any other text." This rule makes the header positionally deterministic — a downstream parser does not need to scan further than the first non-empty line block.

**Header template (`src/superclaude/commands/task.md:58-67`, `src/`):**

```
<!-- SC:TASK-UNIFIED:CLASSIFICATION -->
TIER: [STRICT|STANDARD|LIGHT|EXEMPT]
CONFIDENCE: [0.00-1.00]
KEYWORDS: [matched keywords or "none"]
OVERRIDE: [true|false]
RATIONALE: [one-line reason]
<!-- /SC:TASK-UNIFIED:CLASSIFICATION -->
```

**Entry conditions:**
- The `/sc:task` command has been invoked. Classification (D09) has completed and produced the five values needed to populate the header.
- No prior text or tool call has occurred in the current command turn (Critical Rule 4).

**Exit conditions:**
- The seven-line header block has been emitted as text. The model is now permitted to invoke tools and emit further text.
- Downstream branches (`src/superclaude/commands/task.md:93-101`, `src/`) consume the `TIER` value to dispatch: EXEMPT/LIGHT execute inline; STANDARD/STRICT invoke `Skill sc:task-protocol`.

**Auxiliary references:**
- Four worked examples follow the rules (`src/superclaude/commands/task.md:106-148`, `src/`) — STRICT, EXEMPT, LIGHT, STANDARD — each rendering the full header with realistic values; these serve as few-shot scaffolding for the model.
- The protocol skill carries a non-emission guard (`src/superclaude/skills/sc-task-protocol/SKILL.md:7-9`, `src/`): "Classification has already been performed... The classification header has already been emitted. Do NOT emit it again." This prevents double-emission when the skill is invoked.
- The protocol skill also carries a *fallback emission rule* (`src/superclaude/skills/sc-task-protocol/SKILL.md:9`, `src/`): "If for any reason no classification header was emitted before this skill was invoked, emit one now using ONLY the tier values STRICT, STANDARD, LIGHT, or EXEMPT" — i.e. the skill is the failsafe emitter if the command layer failed.

## 3. What It Produces

A seven-line block of text matching the template at `src/superclaude/commands/task.md:58-67`. Example actual outputs from `src/superclaude/commands/task.md:108-148` (`src/`):

```
<!-- SC:TASK-UNIFIED:CLASSIFICATION -->
TIER: STRICT
CONFIDENCE: 0.95
KEYWORDS: security, vulnerability, auth
OVERRIDE: false
RATIONALE: Security-critical change in authentication module
<!-- /SC:TASK-UNIFIED:CLASSIFICATION -->
```

The output is **terminal stdout text** in the user's conversation transcript — not a file, not a structured artifact. Persistence relies on whatever captures the conversation (the transcript itself, or a downstream telemetry collector that scans transcripts for the sentinel).

## 4. What Invokes It

- **Primary:** the `/sc:task` command's Classification section (`src/superclaude/commands/task.md:50-67`, `src/`) — invoked exactly once per `/sc:task` turn, as the first output.
- **Failsafe:** the `sc:task-protocol` skill (`src/superclaude/skills/sc-task-protocol/SKILL.md:9`, `src/`) — invoked only if the command layer skipped emission (defensive backstop).
- **Reader/parser:** the dispatch logic at `src/superclaude/commands/task.md:93-101` (`src/`) reads the `TIER` field to branch; A/B testing and telemetry pipelines are *intended* downstream readers (no implementation exists in the repo — confirmed by the donor catalog's "consumed by A/B testing" framing in D08 and the absence of a parser binary or pipeline file).
- **Worked examples** (`src/superclaude/commands/task.md:106-148`, `src/`) are reference scaffolding read by the LLM at prompt time, not at runtime by a parser.

## 5. What It Depends On

- **The tier classification model (D09)** — must have produced the five field values before the header can be populated. See `feature-tier-classification.md`. The header is the *sink* for that model's output; without the model the header is unfillable.
- **The HTML-comment delimiter convention** — `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` and its closer. These are string literals; any change breaks downstream parsers silently.
- **The closed tier enumeration** (`STRICT, STANDARD, LIGHT, EXEMPT`) at `src/superclaude/commands/task.md:55,61` (`src/`). The header's TIER field is union-typed across exactly these four values; downstream branching at `src/superclaude/commands/task.md:97-100` (`src/`) hard-codes the four-way dispatch on these values.
- **The model's discipline to emit text-first** — there is no enforcement mechanism. If the model decides to call a tool first (e.g. Read a file to "make sure"), the header position rule silently fails. The only safeguard is the worked examples at `src/superclaude/commands/task.md:106-148` (`src/`) as prompt-time scaffolding.
- **No external file or library dependency** — the header is a pure text emission, no parser library, no schema file.

## 6. Standalone Value Claim

**Claim:** The classification header turns an *internal LLM decision* (which tier did this prompt match?) into an *observable, auditable, machine-parseable artifact*. This has three concrete uses:

1. **Telemetry / A/B testing of the classifier** — by grepping conversation transcripts for `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` and parsing the five fields, a downstream system can measure tier-mix, override rates, confidence distribution, keyword-match patterns — without re-running the classifier or asking the LLM to self-report.
2. **Dispatch contract** — the `TIER` value drives the two-track branch (`src/superclaude/commands/task.md:97-100`, `src/`): EXEMPT/LIGHT terminate inline; STANDARD/STRICT invoke the protocol skill. Without the header as the contract surface, the command would have to carry the tier as in-memory state through to the dispatch step.
3. **Audit trail** — after-the-fact debugging of "why did this task run STRICT?" or "why did the model skip verification on a security change?" becomes a transcript grep rather than an inference re-run.

For a session producing 100 `/sc:task` invocations, headers enable answering "what is our tier-mix?" in a single grep; without them, the answer requires either model self-reporting (unreliable) or re-running every task with instrumentation (expensive).

**Non-value condition (R-RULE-04, concrete, not boilerplate):**

The value claim does NOT hold under any of these specific conditions:

- **No downstream parser exists in the repo.** The headers are emitted but no telemetry collector, A/B test harness, or transcript-scanner is checked in (verified: `grep -r "SC:TASK-UNIFIED:CLASSIFICATION" src/` finds the emission sites and worked examples, but no consumer). Until a parser is written, the headers are write-only artifacts — they consume tokens (~80-120 tokens per emission) and add no information beyond what the command's subsequent behavior already reveals.
- **Sessions that don't go through `/sc:task`.** If the user invokes `/task` directly (which is the recipient's invocation path — task-file driven, not prompt-driven), the header never emits because classification never runs. For a workflow that operates entirely on pre-built task files (the `task-builder` → `/task` pipeline), the header is irrelevant.
- **Single-turn ad-hoc usage.** If a developer uses `/sc:task "fix typo"` once and forgets it, the header has no audit value — it is not aggregated, not stored, not queried. Telemetry value requires aggregation across many invocations, and there is no aggregation infrastructure (see first bullet).

## 7. Coupling Cost Claim

**Claim:** Attaching classification header emission to `/task` requires the recipient to take on **all four** of the following concrete burdens:

1. **A first-output discipline before the F1 loop.** `/task`'s first output today is whatever the task-file processing produces (e.g. the validation-gate report at `src/superclaude/skills/task/SKILL.md:64-73`, `src/` — frontmatter check, schema check, B2 conformance). Inserting the header as a *true* first output requires either (a) the recipient to suppress its existing validation report, (b) re-order so header emits before validation, or (c) accept that the "FIRST OUTPUT" rule from D08 (`src/superclaude/commands/task.md:56`, `src/`) cannot be honored on the recipient side and weaken it to "first output before F1 entry." Each choice has cost — (a) loses observability, (b) requires moving the validation gate, (c) silently breaks the donor's contract.

2. **A header emission path *per task file* (not per command invocation).** Donor emits one header per `/sc:task` turn. Recipient invokes via Skill on a task file that may contain many items, each potentially of a different tier. The recipient must decide: emit one header per task file (loses per-item granularity), emit one header per F1 iteration (changes loop output discipline at `src/superclaude/skills/task/SKILL.md:83-98`, `src/`), or emit one header per phase (matches the recipient's phase structure but diverges from the donor's per-turn semantic). None of these match the donor's shape directly.

3. **A tier-source data path.** `/task` does not produce tier values itself — it would consume them. The header's five fields (`TIER, CONFIDENCE, KEYWORDS, OVERRIDE, RATIONALE`) must be sourced from somewhere: the task file (requires schema extension — see `feature-tier-classification.md` coupling cost #2), the task-builder (requires cross-skill data-flow contract), or an inline mini-classifier (duplicates the donor's tier classification model). The recipient must commit to one source.

4. **A non-emission guard plus a fallback emission rule.** The donor protocol skill has both (`src/superclaude/skills/sc-task-protocol/SKILL.md:7-9`, `src/`) — Do NOT re-emit; emit as failsafe if the command layer didn't. On the recipient side, where there is no command layer above the skill, the guard logic must be re-designed: when *should* the recipient emit, and how does it know whether classification was already performed upstream (e.g. by task-builder)? The recipient must define and document this contract — there is no analog today.

**Net coupling cost:** the recipient must extend its output discipline (1), commit to a granularity (2), commit to a data source (3), and invent a non-emission/fallback contract (4) — four distinct extensions, plus all of the upstream tier-classification-model dependencies (see `feature-tier-classification.md`).

---

## Cross-Reference

- D08 in `donor-feature-catalog.md` (classification header emission) — primary anchor.
- D09 in `donor-feature-catalog.md` (tier classification model) — upstream producer; see `feature-tier-classification.md`.
- D11 (classification output examples) — supporting few-shot scaffolding; tagged NON-TRANSFERABLE because it has no shape independent of D08/D09.
- D14 (human-readable confidence display) — human-facing counterpart that follows the machine header (`src/superclaude/skills/sc-task-protocol/SKILL.md:59-74`, `src/`); has its own characterization scope but depends on this feature.
- D10 (per-tier dispatch) — primary downstream consumer; reads the header's `TIER` field.
