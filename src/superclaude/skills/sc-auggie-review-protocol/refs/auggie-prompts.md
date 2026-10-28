# Review Prompt Templates

These are the prompt templates the skill passes to the `auggie-reviewer` agent via `Task`. Each template ends with a strict JSON-output contract — the agent returns findings as parseable JSON in its final message, not free-form markdown.

Every finding category asks the agent to cross-reference the repo, not to reason only from the diff in isolation. The agent can still mis-cite a line or grade severity inconsistently; the skill's Wave 3 validation step compensates.

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
Head matches the local checkout: {HEAD_MATCH}. If false, cite only the new side of the diff; do not Read the local file as evidence and do not query Serena.
Read the diff, then investigate with Read, Grep and Serena.

## Focus areas

You MUST cover every focus area listed below. For each focus area, search for the patterns described — do not just react to what's visible in the diff. Use Grep and Serena to find related call sites, similar patterns elsewhere, and prior conventions in the repo.

{FOCUS_AREA_BLOCK}

## Output contract (STRICT — your response must match this exactly)

Your final message is a single JSON object. A ```json ...``` fence is tolerated and stripped before parsing. Do not include explanatory prose outside it. Do not write files. The shape is:

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
      "confidence": "<high | medium | low>",
      "claim": {
        "observed": "<what the code does, stated as fact>",
        "observed_at": ["<repo-relative path:line you have Read>"],
        "expected": "<what the requirement, contract or convention says should happen>",
        "violated_requirement": "<path:line of the requirement, contract, doc or convention the code violates; empty if you found none>",
        "intent_sources": ["<path:line of comments, docs, tests or decision records that state the intent>"],
        "intent_finding": "<none_found | supports_claim | contradicts_claim | deliberate_policy | documented_prerequisite>",
        "reachability": {
          "entrypoint": "<path:line of a production entrypoint, or of the instruction that prescribes the step, that reaches observed_at; null if none>",
          "producer": "<path:line of the producer, schema or contract that supplies the triggering input; null if none>",
          "guards_checked": ["<path:line of each guard on the path that you Read>"],
          "caller_search": "<the Grep pattern and roots you searched when you found no entrypoint; otherwise null>"
        },
        "harm": "<the single consequence you consider best supported; null if you cannot show one>",
        "consequences": ["<each distinct consequence you claim, one string each>"],
        "counterevidence": ["<path:line or short note for anything that argues against the claim>"],
        "evidence_kind": "<runtime_reproduced | static_traced | protocol_literal | speculative>",
        "qualification": "<null, or {\"scope\": \"<documented supported configuration under which the claim holds>\", \"scope_citation\": \"<path:line of that documentation>\"}>",
        "disposition_hint": "<defect | unproven | rejected | intentional_limitation | documented_prerequisite>"
      }
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
      "confidence": "<as above>",
      "claim": {
        "observed": "<as in findings[]>",
        "observed_at": ["<as in findings[]>"],
        "expected": "<as in findings[]>",
        "violated_requirement": "<as in findings[]>",
        "intent_sources": ["<as in findings[]>"],
        "intent_finding": "<none_found | supports_claim | contradicts_claim | deliberate_policy | documented_prerequisite>",
        "reachability": {"entrypoint": "<as in findings[]>", "producer": "<as in findings[]>", "guards_checked": ["<as in findings[]>"], "caller_search": "<as in findings[]>"},
        "harm": "<as in findings[]>",
        "consequences": ["<as in findings[]>"],
        "counterevidence": ["<as in findings[]>"],
        "evidence_kind": "<runtime_reproduced | static_traced | protocol_literal | speculative>",
        "qualification": "<as in findings[]>",
        "disposition_hint": "<defect | unproven | rejected | intentional_limitation | documented_prerequisite>"
      }
    }
  ],
  "notes_for_orchestrator": "<optional free-form notes — chunking signals, scope you couldn't cover>"
}

## Claim block

Every entry of `findings` and `cross_cutting_observations` carries a `claim` object with exactly the keys shown above.

- `consequences` lists each distinct consequence you claim as its own string, so the orchestrator can admit or exclude each one. `harm` is the single consequence you consider best supported, or null.

## Quality bar

- Every finding must cite a real file:line you have Read. A Serena or index result is a hint, never evidence, and a miss never proves absence; only a Grep or Read citing its pattern and root does.
- For every behavioral claim, trace a production entrypoint or prescribing instruction that reaches the cited line.
- Search for intent and documented prerequisites (comments, docs, tests, decision records) and record what you found in `intent_sources` and `intent_finding`. If you found nothing, say `none_found` and give the Grep pattern and roots you searched.
- Express doubt as `disposition_hint: unproven` or `harm: null`, never as a lower `severity_hint`.
- Never claim live frequency.
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

Read these files, then investigate with Grep and Serena.

## Focus areas

{FOCUS_AREA_BLOCK}

(... same Output contract and Quality bar as the pr-review-prompt ...)
```

When `in_diff` is irrelevant (snapshot mode), the agent should set every finding's `in_diff` to `false` and the orchestrator will ignore the field.

In snapshot mode the orchestrator records `introduced_in: not_applicable_snapshot` for every candidate, and snapshot output never says "introduced", "regression" or "this PR".

---

## Persona-specialized prompts (used only in `--depth deep`)

For deep reviews the skill also spawns four persona runs of the agent (security, architect, performance, qa), once each on the whole diff, not once per chunk. Each persona prompt is the main `pr-review-prompt` with a single-area focus block and an additional preamble:

```text
You are running a specialized {PERSONA} pass. A general pass covers general issues. Your job is to find what the main pass might have missed within {PERSONA}'s domain. Be deeper, more skeptical, and willing to chase indirect/long-range concerns.
```

Where `{PERSONA}` is one of: `security`, `architect`, `performance`, `qa`.

---

## Anti-patterns in prompt writing (avoid)

- Don't ask the agent to "evaluate code quality" without specifying patterns. It will return a smoothed-over generic checklist.
- Don't allow free-form markdown output. Parser breakage is silent and pernicious.
- Don't put severity caps in the prompt ("only return high-severity findings") — let the agent surface everything and let the rubric handle grading.
- Don't ask the agent to make merge/approve recommendations. That decision belongs to the orchestrator and ultimately the human reviewer.
