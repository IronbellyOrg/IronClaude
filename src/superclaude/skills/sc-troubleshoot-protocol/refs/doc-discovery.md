# Documentation Grounding Rules

Wave 1.5 of the sc:troubleshoot protocol. Loaded on demand by Wave 1.5 only.

This ref defines the three parallel discovery branches (A: release-doc, B: architectural-doc with currency validation, C: semantic-restriction), the per-branch structured-output schemas, and the synthesised Documentation Context Card template that Waves 1, 3, 4, and 5 consume.

---

## Section 1: Auggie query templates per branch

Each branch issues ONE `mcp__auggie__codebase-retrieval` call (single message, fan-out via parallel Task spawns from the Wave 1.5 orchestrator). The placeholders `<issue_description>`, `<scope>`, and `<component_paths>` are filled by the Wave 1.5 orchestrator from the parsed Wave 0 input.

### Branch A — Release-doc lookup

Query target: `.dev/releases/current/` and `.dev/releases/complete/` for prior release artifacts (PRDs, TDDs, specs) that scope the symptom's component.

```
In the .dev/releases/ tree (both current/ and complete/), find any PRD, TDD, spec, or roadmap artifact that scopes <component_paths> or names <issue_description>'s subject area. For each hit, return the artifact path, a 2-3 sentence summary of how the artifact constrains the behavior of <component_paths>, and a confidence score (0.0-1.0) reflecting how directly the artifact addresses the symptom.
```

### Branch B — Architectural-doc lookup (with currency validation)

Query target: `docs/reference/`, `docs/developer-guide/`, `docs/analysis/`, `docs/troubleshooting/`, and any top-level architectural markdown (`PLANNING.md`, `CLAUDE.md`, `KNOWLEDGE.md`).

```
In the docs/ tree (especially reference/, developer-guide/, analysis/, troubleshooting/) and the repo-root architecture files (PLANNING.md, CLAUDE.md, KNOWLEDGE.md), find any document that describes the architecture, contract, or expected behavior of <component_paths> as it relates to <issue_description>. For each hit, return the doc path, a 2-3 sentence summary of the documented behavior, and a currency verdict per the procedure in Section 2.
```

### Branch C — Semantic-restriction extraction

Query target: any file under `<scope>` or referenced from `<component_paths>` that contains explicit MUST / MUST NOT / SHALL / forbidden-pattern language.

```
In the source tree under <scope> (or in <component_paths> if scope is unset), find every file or section that contains explicit MUST, MUST NOT, SHALL, REQUIRED, FORBIDDEN, or NEVER language constraining the behavior of <component_paths>. For each hit, return the source file, the file:line, the quoted constraint text, and which surface (function / class / module / contract) the constraint applies to.
```

---

## Section 2: Branch B currency-check procedure

For every doc Branch B surfaces, the branch agent runs a currency check before recording a `current` verdict. The check has two signals: filesystem mtime and explicit doc-header status markers.

### Step 1 — Filesystem mtime

```
stat -c '%Y' <doc_path>
```

Compare the returned epoch seconds against the mtime of the most recent file in the directory listed in `<component_paths>` (i.e., the code surface the doc claims to describe). Rule: if `mtime(doc) < mtime(code) - (90 days)`, the doc is at least 3 months staler than the code it describes — emit verdict `stale`.

### Step 2 — Explicit doc-header status markers

```
grep -E '^(Last reviewed|Status|Owner|Updated):' <doc_path> | head -5
```

If the doc declares `Status: deprecated`, `Status: archived`, or `Last reviewed: <date older than 6 months>`, emit verdict `stale` regardless of mtime.

### Verdict combination rule

| Step 1 mtime | Step 2 marker | Verdict |
|---|---|---|
| fresh (< 90 days behind code) | no markers OR "Status: current" / "Last reviewed: < 6 months" | `current` |
| fresh | "Status: deprecated/archived" OR "Last reviewed: > 6 months" | `stale` |
| stale (≥ 90 days behind code) | any | `stale` |
| mtime unobtainable | any | `unknown` |

Both `stale` and `unknown` verdicts surface in the Documentation Context Card with a CAUTION note; only `current`-verdict docs are weighted as authoritative by downstream waves.

---

## Section 3: Structured-output schema per branch

Each branch agent writes ONE structured-output file at `<output-dir>/wave1_5-branch-<A|B|C>.md`. The schemas:

### Branch A schema

Either a single object:

```json
{
  "release_slug": "<slug from .dev/releases/...>",
  "artifact_paths": ["<absolute path 1>", "<absolute path 2>"],
  "summary": "<2-3 sentence summary>",
  "confidence": 0.85
}
```

Or, on no-hit, the literal:

```json
{ "hit": false }
```

### Branch B schema

An array of objects (zero or more):

```json
[
  {
    "doc_path": "<absolute path>",
    "summary": "<2-3 sentence summary of the documented behavior of <component_paths>, per the Section 1 Branch B query template>",
    "currency_verdict": "current",
    "reason": "<one-line rationale for the currency_verdict, tied to Section 2 procedure>"
  }
]
```

`currency_verdict` ∈ `{current, stale, unknown}`. Empty array means no relevant docs found.

### Branch C schema

An array of objects (zero or more):

```json
[
  {
    "source_file": "<absolute path>",
    "file_line": 42,
    "quoted_text": "<verbatim MUST/MUST NOT clause>",
    "applies_to": "<surface name: function / class / module / contract>"
  }
]
```

Empty array means no semantic restrictions found.

---

## Section 4: Documentation Context Card template

After all three branches complete, the Wave 1.5 orchestrator synthesises a single Documentation Context Card at `<output-dir>/doc-context.md`. The card has 4 sections matching the consumption pattern downstream waves expect:

```markdown
# Documentation Context Card

**Generated**: <ISO 8601 timestamp>
**Wave**: 1.5
**Scope**: <scope used by Wave 1.5; or "(none)" if --scope was unset>

## Release context

Findings from Branch A (release-doc lookup). Format:

- **Release**: <slug or "None found">
- **Artifacts**: <comma-separated absolute paths>
- **Summary**: <2-3 sentence summary of how the release constrains the affected surface>
- **Confidence**: <0.0-1.0>

## Architectural docs consulted

Findings from Branch B (architectural-doc lookup), with currency verdicts. Format (one bullet per doc, or "None found"):

- `<doc_path>` — verdict: `<current | stale | unknown>` — <one-line summary derived from the schema `summary` field>

Docs with `stale` or `unknown` verdicts surface a CAUTION line:

> CAUTION: <doc_path> is <stale|unknown> per the Section 2 currency check; treat its claims as advisory, not authoritative.

## Restrictions / decisions that constrain the fix

Findings from Branch C (semantic-restriction extraction). Format (one bullet per constraint, or "None found"):

- `<source_file>:<file_line>` (<applies_to>) — "<quoted_text>"

## Re-frame signals

A 1-3 bullet synthesis derived from the three sections above. Each bullet names a way the documented evidence reframes the bug-as-stated. Examples:

- "The reported symptom IS the documented behavior — recommend a spec change or stakeholder discussion, not a code change."
- "The release artifact for <slug> says <component> MUST <behavior>; the bug report describes a deviation from this contract."
- "Branch C found a MUST NOT clause at `<source_file>:<file_line>` that the proposed fix would violate."

If no signals reframe the bug-as-stated, write the literal: "No documentation-derived reframing applies — proceed with normal hypothesis generation."
```

---

## Loading discipline

This ref is loaded only by Wave 1.5. Do not pre-load. The three branch agents receive their query templates from Section 1 by quotation in the Wave 1.5 brief; they do NOT load this entire ref. The synthesised Documentation Context Card from Section 4 is the only artifact consumed by downstream waves (Waves 1, 3, 4, 5).
