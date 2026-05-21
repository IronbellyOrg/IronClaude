# Research: Target Files Inventory

**Topic type:** File Inventory + Patterns & Conventions
**Scope:** offer-pr-review.sh, SKILL.md L150-180, evals.json
**Status:** Complete
**Date:** 2026-05-20
---

## File 1: offer-pr-review.sh

- **Full relative path:** `src/superclaude/hooks/scripts/offer-pr-review.sh`
- **Absolute path:** `/config/workspace/IronClaude/src/superclaude/hooks/scripts/offer-pr-review.sh`
- **Total line count:** 70 lines
- **Purpose:** PostToolUse(Bash) hook that surfaces an offer to run `/sc:auggie-review` after a successful `gh pr create`.

### Current state of lines being modified (Fix 1 — M2)

User specifies Fix 1 must be inserted **between line 17 and line 20** (i.e., as a new prefilter that exits early when the payload is clearly not a `gh pr create` invocation, before any `jq` work).

VERBATIM current content of lines 15-24:

```bash
15: set -u
16:
17: INPUT="$(cat 2>/dev/null || true)"
18:
19: # Pull the tool name and the bash command out of the hook payload.
20: TOOL_NAME="$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)"
21: [ "$TOOL_NAME" = "Bash" ] || exit 0
22:
23: CMD="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)"
24: [ -z "$CMD" ] && exit 0
```

### Exact replacement (Fix 1 — M2: cheap prefilter)

User-provided literal snippet to insert at the new line 19 (between current L17 and current blank line on L18 stays; the prefilter goes after the blank line, before the comment on current L19). The exact one-liner from the user:

```bash
case "$INPUT" in *'"command"'*'gh'*'pr'*'create'*) ;; *) exit 0;; esac
```

PROPOSED new lines 15-26 after Fix 1 applied (preserves comment style and blank-line cadence already established in the file):

```bash
15: set -u
16:
17: INPUT="$(cat 2>/dev/null || true)"
18:
19: # Cheap prefilter: bail out immediately if the payload doesn't even mention `gh pr create`.
20: # Saves three jq invocations on every non-matching Bash tool call.
21: case "$INPUT" in *'"command"'*'gh'*'pr'*'create'*) ;; *) exit 0;; esac
22:
23: # Pull the tool name and the bash command out of the hook payload.
24: TOOL_NAME="$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)"
25: [ "$TOOL_NAME" = "Bash" ] || exit 0
26: ...
```

### Adjacent patterns to preserve (constraints on the fix)

1. **`set -u` on L15** is active — unbound variables would crash. However the user's snippet uses only `$INPUT` (already set on L17), so `set -u` is satisfied. Confirmed safe.
2. **Fail-open exit-0 pattern**: every guard in this file uses `exit 0` (never exit 1 or exit 2), per the hook contract comment at L7. The new prefilter follows this exact pattern (`*) exit 0;;`).
3. **`INPUT="$(cat 2>/dev/null || true)"` on L17** intentionally fails open to empty string. With an empty `$INPUT`, the `case` statement will not match `*'"command"'*'gh'*'pr'*'create'*` and will hit the `*) exit 0` branch — correct fail-open behavior preserved.
4. **Comment style**: existing comments use `#` with sentence-case prose and end with period. Backticks for code identifiers. New comment must match (proposed text above uses this style).
5. **Blank-line cadence**: file separates logical blocks with single blank lines (L16, L18, L22, L25, L32, L36, L42, L55). The new prefilter is its own block, so it should be flanked by blank lines.
6. **No `[[` bash regex prefilter**: the existing regex match on L29 uses `[[ "$CMD" =~ ... ]]` AFTER `jq` has extracted `$CMD`. The new prefilter is intentionally simpler — a POSIX `case` against raw JSON — to be the cheap pre-jq gate. Do not replace with a `[[`-regex form.
7. **Quoting in `case` patterns**: the user's snippet uses `*'"command"'*` (single-quoted literal containing double-quote) which is intentional — it matches the JSON key `"command"` substring. This is correct shell quoting; do not "fix" the apparent escaping.

---

## File 2: SKILL.md (lines 150-180 focus)

- **Full relative path:** `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`
- **Absolute path:** `/config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`
- **Total line count:** 362 lines
- **Purpose:** The on-disk SKILL.md for the `sc-auggie-review-protocol` skill — defines the multi-wave Auggie-powered PR-review pipeline, including the literal `auggie` CLI invocation template and a "Common pitfalls" blockquote.

### Current state of lines being modified (Fix 2 — M1)

User specifies Fix 2 targets **SKILL.md lines 163-170**, and the required final pipeline is:

```
tail -n +2 auggie-raw.json | jq -r '.result' | sed -n '/^```json$/,/^```$/p' | sed '1d;$d' | jq '.'
```

VERBATIM current content of lines 163-170 (the "Common pitfalls" blockquote, second-bullet through last-bullet, where the recommended pipeline appears):

```
163: > **Common pitfalls (read before invoking)**:
164: >
165: > - **Flag name**: the correct flag is `--output-format json`, NOT `--json`. The latter is not a real auggie flag and will cause `exit 1`.
166: > - **JSON wrapping**: even with `--output-format json`, Auggie usually wraps its response in a ```json ...``` markdown fence and may include preamble/postamble prose. **Always strip fences and extract the JSON object** before parsing. Recommended: `sed -n '/^```json$/,/^```$/p' auggie-raw.json | sed '1d;$d' | jq '.'` or equivalent. If `jq` parse fails, save the raw response and downgrade status to `partial`.
167: > - **`--max-turns` preamble**: when `--max-turns N` is passed, Auggie prints `Applying --max-turns override: N over agentMaxIterations=500` as the **first stdout line** before the JSON envelope. This breaks `jq` if not stripped. Pipe through `tail -n +2` (or `grep -v '^Applying --max-turns'`) before extracting `.result` and stripping the inner ```json fence. The outer envelope (`{"type":"result","result":"<fenced-json-string>",...}`) is then parsed normally.
168: > - **`--instruction-file` requires a real path**: `mkdir -p <output-dir>` before writing the prompt file. Auggie reads the file from disk, not stdin.
169: > - **`--workspace-root` matters**: must point to the repo root (`git rev-parse --show-toplevel`), not the diff path or PR subtree. Auggie's index is scoped to this directory.
170: > - **Indexer cold-start**: if `auggie-stderr.log` mentions "indexing" or "not ready", retry with `--wait-for-indexing` once before treating as a failure.
```

### The bug (per PR #64 M1)

Lines 166 and 167 describe **two separate pipelines that contradict each other**:

- L166 recommends `sed -n '/^```json$/,/^```$/p' auggie-raw.json | sed '1d;$d' | jq '.'` — this operates on the raw file and does NOT first `tail -n +2` to strip the preamble, NOR does it `jq -r '.result'` to unwrap the outer envelope.
- L167 then says you must `tail -n +2` and "extract `.result` and stripping the inner ```json fence" — but never shows the actual one-liner.

A reader following L166 verbatim will fail on the `--max-turns` preamble (L167's case). The fix consolidates into a single, complete pipeline.

### Exact replacement (Fix 2 — M1)

PROPOSED replacement of L166-L167 (merging the two bullets into one authoritative bullet that shows the full pipeline the user mandated):

```
> - **JSON unwrapping (full pipeline)**: even with `--output-format json`, Auggie wraps its response in an outer envelope (`{"type":"result","result":"<fenced-json-string>",...}`), prepends a `--max-turns` preamble line when `--max-turns N` is passed (`Applying --max-turns override: N over agentMaxIterations=500`), and the inner `.result` string is itself wrapped in a ```json ...``` markdown fence. The complete unwrap pipeline is:
>
>   ```bash
>   tail -n +2 auggie-raw.json | jq -r '.result' | sed -n '/^```json$/,/^```$/p' | sed '1d;$d' | jq '.'
>   ```
>
>   Steps: `tail -n +2` strips the `--max-turns` preamble line; `jq -r '.result'` unwraps the outer envelope; `sed -n '/^```json$/,/^```$/p'` extracts the fenced inner block; `sed '1d;$d'` drops the opening and closing fence markers; final `jq '.'` validates and pretty-prints. If `jq` parse fails, save the raw response and downgrade status to `partial`.
```

This replaces both L166 and L167 with one consolidated bullet. L168-L170 remain unchanged. The replacement is **two original bullets → one new bullet (with a code-fenced pipeline)**, so the bullet count of the blockquote drops by one (from 6 to 5) — this is intended and is the structural change.

### Adjacent patterns to preserve

1. **Blockquote prefix**: every line in the L163-L170 block starts with `>` (greater-than + space). The replacement must keep this prefix on every line, INCLUDING the indented code fence and inner blank lines (which currently are `>` alone with no trailing space, e.g., L164).
2. **Bullet marker**: `> - **<term>**: <prose>` is the established pattern (see L165, L166, L167, L168, L169, L170). The new consolidated bullet keeps this `**<term>**:` opening.
3. **Code-fenced bash inside blockquote**: there is precedent for fenced code blocks inside markdown blockquotes (used elsewhere in this SKILL.md, but the L163-L170 block as-is uses only inline-backtick code). Embedding a fenced bash block inside a blockquote is standard markdown and renders correctly. Each fence line must start with `>` to remain inside the blockquote.
4. **Bullet for "**Flag name**"** (L165), bullets L168-L170: must remain verbatim. Only L166 and L167 are merged.
5. **Surrounding context** (L150-L162, L171+): the L152-L161 fenced `bash` block (the `auggie --print ...` invocation template) is the structure the pitfalls bullets exist to explain; the pipeline in the new bullet must be consistent with the redirect on L160 (`> <output-dir>/auggie-raw-<chunk>.json`) — note `auggie-raw-<chunk>.json` per-chunk vs. plain `auggie-raw.json` used as the example in the pitfall. The example name `auggie-raw.json` already in L166 is intentionally short for readability; preserve that convention.

---

## File 3: evals.json

- **Full relative path:** `src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json`
- **Absolute path:** `/config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json`
- **Total line count:** 29 lines
- **Purpose:** Skill-evaluation manifest in skill-creator format — three scenarios (`pr-by-number-merged`, `local-diff-vs-master`, `snapshot-cli-module`) that exercise the three input modes of `/sc:auggie-review`. Currently every `assertions` array is empty (`[]`), which means no automated pass/fail signal.

### Current state of lines being modified (Fix 3 — M4)

User specifies Fix 3 targets the three `assertions` arrays at **lines 10, 18, 26**.

VERBATIM current content of the three assertions lines:

```
L10:       "assertions": []
L18:       "assertions": []
L26:       "assertions": []
```

Each is the last key in its eval object (no trailing comma).

### Eval object shape (shared across all three scenarios)

Each eval object has exactly these keys, in this order:

- `"id"` (integer)
- `"name"` (string, kebab-case)
- `"prompt"` (string, the user-facing prompt that exercises the skill)
- `"expected_output"` (string, prose description of what success looks like)
- `"files"` (array — currently `[]` for all three; reserved for input fixtures)
- `"assertions"` (array — currently `[]` for all three; this is what Fix 3 populates)

Top-level shape: `{ "skill_name": "<string>", "evals": [<eval-object>, ...] }`.

Indentation: 2-space JSON (confirmed: outer keys at col 0+2, inner keys at col 0+4, array elements at col 0+6 when populated).

### Proposed assertion DSL (no harness yet exists, so this is a forward-looking but lint-stable schema)

User mandated three assertion **types** but did not specify JSON shape. Proposed discriminated-union shape (matches common eval-harness conventions, e.g., promptfoo/inspect-ai, and stays valid JSON whether or not a runner exists):

```json
{ "type": "file_exists", "path": "<absolute-or-relative-path>" }
{ "type": "report_contains", "report": "<path-to-report>", "markers": ["<string>", ...] }
{ "type": "no_hallucinated_citations", "report": "<path-to-report>", "repo_root": "<absolute-path>" }
```

Semantics:

- `file_exists`: passes iff `path` resolves to a regular file post-run.
- `report_contains`: passes iff every string in `markers` appears as a substring (or line) in the file at `report`.
- `no_hallucinated_citations`: scans `report` for `file:line` citations (regex: `[\w./\-_]+:\d+`), verifies each resolves to an actual file under `repo_root` AND that the line number is within the file's line count. Passes iff all citations resolve.

### Exact replacement text — scenario 1 (id=1, pr-by-number-merged)

Replace L10 `"assertions": []` with:

```json
      "assertions": [
        { "type": "file_exists", "path": "/tmp/eval-pr62/REVIEW.md" },
        { "type": "report_contains", "report": "/tmp/eval-pr62/REVIEW.md", "markers": ["# Code Review:", "## Findings", "## Audit"] },
        { "type": "no_hallucinated_citations", "report": "/tmp/eval-pr62/REVIEW.md", "repo_root": "/config/workspace/IronClaude" }
      ]
```

### Exact replacement text — scenario 2 (id=2, local-diff-vs-master)

Replace L18 `"assertions": []` with:

```json
      "assertions": [
        { "type": "file_exists", "path": "/tmp/eval-diff/REVIEW.md" },
        { "type": "report_contains", "report": "/tmp/eval-diff/REVIEW.md", "markers": ["# Code Review:", "## Findings", "## Audit"] },
        { "type": "no_hallucinated_citations", "report": "/tmp/eval-diff/REVIEW.md", "repo_root": "/config/workspace/IronClaude" }
      ]
```

### Exact replacement text — scenario 3 (id=3, snapshot-cli-module)

Replace L26 `"assertions": []` with:

```json
      "assertions": [
        { "type": "file_exists", "path": "/tmp/eval-snapshot/REVIEW.md" },
        { "type": "report_contains", "report": "/tmp/eval-snapshot/REVIEW.md", "markers": ["# Code Review:", "## Findings", "## Audit"] },
        { "type": "no_hallucinated_citations", "report": "/tmp/eval-snapshot/REVIEW.md", "repo_root": "/config/workspace/IronClaude" }
      ]
```

### Adjacent patterns to preserve

1. **JSON validity**: each replacement keeps the `"assertions": ...` key as the **last** key of its eval object — DO NOT add a trailing comma after the closing `]`. The next non-whitespace character in the source file after each assertions value is either `}` (end of eval object) followed by `,` (between objects) or `}` (last object, no trailing comma at L27/L28).
2. **2-space indentation**: assertions array elements at column 8, object keys inside each assertion at column 10 (consistent with `"id": 1` etc. inside each eval).
3. **Inline vs. multi-line objects**: I have written each assertion object on a single line (inline JSON), which is the cleanest readable form and matches how empty arrays were inlined. Alternative is fully-pretty (each key on its own line), but inline-per-assertion keeps the file compact and lint-clean.
4. **Marker strings exactly as the user specified**: `"# Code Review:"`, `"## Findings"`, `"## Audit"`. Note the trailing colon on `# Code Review:` is intentional (the report template uses `# Code Review: PR #N` or `# Code Review: <target>` so the colon is the discriminator).
5. **Path values**: the three `prompt` strings already specify `/tmp/eval-pr62/`, `/tmp/eval-diff/`, `/tmp/eval-snapshot/` as `--output-dir`, so `REVIEW.md` lives directly inside each. Confirmed by reading L7, L15, L23.
6. **`repo_root`**: set to the project root `/config/workspace/IronClaude` for now; if the harness ever runs from a different worktree the assertion engine can override. This is a defensible default.
7. **`files`**: stays `[]` for all three (no fixture inputs needed — each scenario operates on the real repo).

---

## Summary

Three files, three targeted fixes:

| Fix | File | Line(s) | Change |
|---|---|---|---|
| M2 (Fix 1) | `src/superclaude/hooks/scripts/offer-pr-review.sh` | Insert new prefilter between L17 and L19 (becomes new L19-L21) | Add `case "$INPUT" in *'"command"'*'gh'*'pr'*'create'*) ;; *) exit 0;; esac` with a 2-line comment header. Fail-open `exit 0` matches existing pattern; `set -u` safe because `$INPUT` is set on L17. |
| M1 (Fix 2) | `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` | Replace L166-L167 (two contradictory bullets) | Consolidate into one bullet titled **JSON unwrapping (full pipeline)** that shows the full `tail -n +2 auggie-raw.json \| jq -r '.result' \| sed -n '/^```json$/,/^```$/p' \| sed '1d;$d' \| jq '.'` pipeline in a fenced bash block inside the existing blockquote. Bullet count drops 6 → 5. |
| M4 (Fix 3) | `src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json` | Replace L10, L18, L26 (three empty `"assertions": []`) | Populate each with a 3-element assertions array using a discriminated-union DSL: `file_exists`, `report_contains` (markers `# Code Review:`, `## Findings`, `## Audit`), and `no_hallucinated_citations`. Each path matches the scenario's `--output-dir` from its prompt. |

All three fixes preserve their file's existing conventions (shell fail-open style, markdown blockquote+bullet format, 2-space JSON indentation respectively). No structural ripple effects beyond the bullet-count reduction on Fix 2 (intended).
