# Auggie Prompt Templates

These are the structured instruction templates the skill writes to a file and passes to Auggie via `--instruction-file`. Each template ends with a strict JSON-output contract — Auggie returns findings as parseable JSON, not free-form markdown.

## Why these prompts look the way they do

Auggie's strength is **indexed-codebase retrieval and cross-file reasoning** — it can answer "where is this function called?" and "is this pattern used consistently?" much more cheaply than Claude reading files one at a time. The prompts below explicitly invite Auggie to use that strength: every finding category asks Auggie to cross-reference against the indexed repo, not to reason only from the diff in isolation.

Auggie's weakness, relative to a careful Claude pass, is calibration — it can hallucinate file:line citations or grade severity inconsistently. The skill's Wave 3 validation step exists to compensate. Our job in these prompts is to maximize Auggie's signal and tag uncertainty explicitly, knowing Claude will second-pass it.

The `--ask` flag (set in the invocation, not the prompt) restricts Auggie to retrieval/non-editing tools, which is the right safety boundary for a review.

---

## Template: `pr-review-prompt`

Used for PR or diff targets. Interpolate the placeholders before writing the file.

```text
You are reviewing a code change for the repository at the workspace root. Your job is to identify problems — both narrow bugs and higher-level concerns — and report them as structured JSON.

## Context

Target: {TARGET_DESCRIPTION}
{PR_TITLE_LINE}
{PR_BODY_BLOCK}

Diff range: {BASE_REF}...{HEAD_REF}
Files changed ({N_FILES}):
{FILE_LIST}

The full diff is available at: {DIFF_PATH}
Read it with the `view` tool, then use your indexed codebase context to investigate.

## Focus areas

You MUST cover every focus area listed below. For each focus area, search for the patterns described — do not just react to what's visible in the diff. Use your codebase retrieval to find related call sites, similar patterns elsewhere, and prior conventions in the repo.

{FOCUS_AREA_BLOCK}

## Output contract (STRICT — your response must match this exactly)

Respond with a single JSON object. Even when the prompt asks for no markdown fences, Auggie in practice wraps the JSON in a ```json ...``` fence — that is fine and the orchestrator strips it before parsing. Do not include explanatory prose **outside** the fence. The shape is:

{
  "findings": [
    {
      "title": "<one-line summary, sentence case, no trailing period>",
      "category": "<one of: security | data-integrity | correctness | concurrency | resource-leak | error-handling | api-contract | performance | architecture | layering | coupling | anti-pattern | dead-code | tests | docs | logging | naming | style>",
      "severity_hint": "<one of: critical | high | medium | low | nit — your best guess; the orchestrator may remap>",
      "file": "<repo-relative path>",
      "line": <integer line number in the file at HEAD>,
      "line_range_end": <integer or null — set for multi-line findings>,
      "in_diff": <true|false — set true only if your cited line falls inside the diff hunks>,
      "evidence": "<the exact code excerpt at the cited line(s), verbatim. If you cannot copy the exact bytes, set this to null and confidence to 'low'>",
      "why": "<2-4 sentences explaining the concern in concrete terms>",
      "recommendation": "<1-3 sentences with a concrete change — what to do, not 'consider improving'>",
      "cross_references": ["<repo-relative path:line of related code you found while investigating, if any>"],
      "confidence": "<high | medium | low>"
    }
  ],
  "cross_cutting_observations": [
    {
      "title": "<for findings that span multiple files and aren't anchored to a single line>",
      "category": "<as above>",
      "severity_hint": "<as above>",
      "affected_files": ["<repo-relative path>", "..."],
      "why": "<as above>",
      "recommendation": "<as above>",
      "confidence": "<as above>"
    }
  ],
  "notes_for_orchestrator": "<optional free-form notes — chunking signals, areas where indexing seems stale, scope you couldn't cover>"
}

## Quality bar

- Every finding must cite a real file:line. If you can't verify the file:line, set confidence to "low" and the orchestrator will validate.
- Do not invent file paths. If you remember a file existing but can't read it, leave it out.
- For each focus area, aim for the highest-signal 3-5 findings, not an exhaustive list. The orchestrator will dedupe with other passes.
- It is OK to return zero findings in a focus area if the area is genuinely clean. Do not pad.
- For PR mode: prefer findings whose cited line is inside the diff (`in_diff: true`). Out-of-diff findings are allowed but only when the diff makes them newly relevant (e.g., a callsite added in the diff exposes a latent bug in a function the diff didn't touch).
- For higher-level findings (architecture, layering, anti-patterns, coupling): put them in `cross_cutting_observations`, not `findings`, since they don't have a single line.

Return only the JSON object. No additional text.
```

### Focus-area blocks

Substituted into `{FOCUS_AREA_BLOCK}` based on `--focus`:

- **security**: `Look for: hardcoded secrets, weak crypto, SQL/XSS injection sinks, deserialization sinks, authz/authn bypasses, path traversal, SSRF, missing rate-limits, sensitive data in logs, race conditions in auth paths, missing input validation at trust boundaries. Cross-reference: are similar patterns hardened elsewhere in the repo? Is the new code re-using a known-good helper or rolling its own?`

- **architecture**: `Look for: layering violations (a module reaching across boundaries that the repo conventions don't allow), business logic in transport/presentation layers, missing abstractions (the same conditional repeated 3+ times), god-objects, circular imports, leaky abstractions, modules with too many responsibilities. Cross-reference: how do other modules in this repo solve the same problem? Is the new code consistent?`

- **quality**: `Look for: off-by-one errors, null-deref / unwrap-on-None, untyped function boundaries, dead code, unused variables/imports, swallowed exceptions, broad except clauses, copy-pasted code, magic numbers, misleading names, comments that contradict code. Cross-reference: do similar helpers exist that the new code should reuse?`

- **performance**: `Look for: N+1 queries, missing indexes implied by query shape, synchronous calls in async paths, unbounded loops, large allocations in hot paths, repeated parsing/serialization, missing caching for expensive pure functions, accidentally quadratic algorithms. Cross-reference: does the repo have profiling notes or known-hot paths this change touches?`

- **anti-patterns**: `Look for: god functions (> 100 lines), god classes (> 20 methods), feature envy, primitive obsession, shotgun surgery (one change forces many distant edits), inappropriate intimacy, lazy class, speculative generality, refused bequest, message chains, middle-man classes. Cross-reference: are these patterns recurring (i.e., does the diff make an existing smell worse)?`

- **tests**: `Look for: new code with no tests, tests that don't actually exercise the new code path, tests asserting trivial things, tests with hardcoded credentials, missing edge-case tests (empty/null/max/concurrency), tests that rely on time/network/randomness without seeding. Cross-reference: are similar code paths in the repo tested? What pattern do those tests use?`

- **docs**: `Look for: new public API without docstrings, README that no longer matches code, comments that contradict code, missing migration notes for breaking changes, stale references in docs/. Cross-reference: does the repo have a docs convention this should follow?`

For `--focus all`, include every block above.

---

## Template: `snapshot-review-prompt`

Used for `--snapshot` targets (no diff baseline). Same JSON contract; the Context section becomes:

```text
You are reviewing files at the workspace root in their current state. There is no diff baseline — every line is in scope.

## Context

Target: snapshot of {SNAPSHOT_PATH}
Files to review ({N_FILES}):
{FILE_LIST}

Read these files via your file tools, then use your indexed codebase context to investigate.

## Focus areas

{FOCUS_AREA_BLOCK}

(... same Output contract and Quality bar as the pr-review-prompt ...)
```

When `in_diff` is irrelevant (snapshot mode), Auggie should set every finding's `in_diff` to `false` and the orchestrator will ignore the field.

---

## Persona-specialized prompts (used only in `--depth deep`)

For deep reviews, after the main pass the skill spawns additional Auggie calls — one per focus area not adequately covered by the main pass. Each persona prompt is the main `pr-review-prompt` with a single-area focus block and an additional preamble:

```text
You are running a specialized {PERSONA} pass. The main review has already covered general issues. Your job is to find what the main pass might have missed within {PERSONA}'s domain. Be deeper, more skeptical, and willing to chase indirect/long-range concerns.
```

Where `{PERSONA}` is one of: `security`, `architect`, `performance`, `qa`.

---

## Notes on tuning

- **`--max-turns`**: We set 8 for quick, 16 for standard, 24 for deep. Lower bounds force Auggie to be efficient; deep mode allows more multi-step retrieval.
- **`--workspace-root`**: Always passed explicitly so Auggie indexes the right tree. Without this flag, Auggie auto-detects from the working directory, which can drift if the skill is invoked from a subdirectory.
- **`--add-workspace`**: Not used by default. Add if the review needs to span multiple repos (rare).
- **`--rules`**: Not used by default. Could be a future extension to point Auggie at `RULES.md` or `PRINCIPLES.md` for repo-specific standards.

## Anti-patterns in prompt writing (avoid)

- Don't ask Auggie to "evaluate code quality" without specifying patterns. It will return a smoothed-over generic checklist.
- Don't allow free-form markdown output. Parser breakage is silent and pernicious.
- Don't put severity caps in the prompt ("only return high-severity findings") — let Auggie surface everything and let the rubric handle grading. Auggie underestimates severity more often than overestimates it.
- Don't ask Auggie to make merge/approve recommendations. That decision belongs to the orchestrator and ultimately the human reviewer.
