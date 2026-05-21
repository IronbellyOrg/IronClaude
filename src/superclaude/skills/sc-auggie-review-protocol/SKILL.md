---
name: sc:auggie-review-protocol
description: "Auggie-powered code review protocol for PRs, local diffs, and file snapshots — orchestrates Auggie's deep retrieval pass, validates findings against real files, posts to PR, and offers a remediation handoff chain"
allowed-tools: Read, Grep, Glob, Bash(auggie *), Bash(gh *), Bash(git *), Bash(jq *), Bash(wc *), Bash(find *), Bash(mkdir *), Bash(cat *), Bash(mv *), Bash(cp *), Bash(date *), TodoWrite, Task, Write, Edit, Skill
---

<!-- Extended metadata (for documentation, not parsed):
category: quality
complexity: advanced
mcp-servers: [sequential, serena, auggie]
personas: [analyzer, architect, security, qa, refactorer]
-->

# Auggie Review Protocol

## Purpose

Run an evidence-based code review of a Pull Request, local diff, or file snapshot. The review must catch **both** narrow bugs (off-by-one, null-deref, leaked resources, race conditions, untyped boundaries) **and** higher-level concerns (architectural drift, layering violations, anti-patterns, coupling smells, missing abstractions, performance regressions, security exposure).

**Token-efficiency contract**: The Auggie CLI does the heavy retrieval and pattern-matching work using its already-indexed codebase context. Claude orchestrates, validates, dedupes, and synthesizes. This split exists because Auggie is free or near-free for codebase-retrieval workloads, while Claude's tokens are the constrained resource. Lean on Auggie wherever you can; use Claude for reasoning, file:line validation, and final synthesis.

**Hallucination contract**: Every finding emitted in the final report must cite a `file:line` that exists in the repo at the time of review. Findings that cannot be grounded are dropped, not downgraded. This is non-negotiable — a "review" full of imaginary line numbers is worse than no review.

## Required Input (STOP if missing)

The skill receives one of three target modes from `/sc:auggie-review`:

| Mode | Required | Resolved Form |
|------|----------|---------------|
| **PR** | `<PR-num>` or `<PR-URL>` | `gh pr view <id> --json number,headRefName,baseRefName,headRepository,headRepositoryOwner,title,body,files` |
| **Diff** | `--diff <base>...HEAD` | `git diff <base>...HEAD` (validate refs exist) |
| **Snapshot** | `--snapshot <path>` | `find <path> -type f` (validate path exists) |

**STOP** if:
- Target cannot be resolved (PR not found, ref doesn't exist, path missing)
- `auggie` is not on PATH (`command -v auggie` fails)
- For PR mode, `gh auth status` reports unauthed
- `--depth deep` requested but the diff exceeds 5000 lines without `--force` (too large to be useful)

**WARN (proceed)** if:
- Diff exceeds 1500 lines (Auggie may need chunking — emit a chunking-mode notice)
- More than 30 files changed (recommend `--focus` to scope down)
- The PR base branch is not the repo's default branch (mention in report header)

## Output Contract

The skill returns:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success`, `partial` (some findings dropped for hallucination), `failed` |
| `report_path` | string | Absolute path to the markdown report |
| `audit_log_path` | string | Absolute path to the audit log (auggie raw JSON, validation results, decisions) |
| `pr_review_url` | string | URL of the posted `gh pr review` comment (empty if `--no-post-pr` or non-PR target) |
| `findings_count` | object | `{critical: N, high: N, medium: N, low: N, nit: N}` |
| `dropped_count` | int | Findings dropped because file:line could not be validated |
| `remediation_offered` | boolean | Whether the remediation chain was offered |
| `remediation_accepted` | boolean | If offered, whether the user accepted |

## Wave Structure

The protocol runs in five waves. Each wave has explicit entry/exit criteria. Refs are loaded **per-wave**, never pre-loaded.

```
Wave 0: Resolve & Validate Target
Wave 1: Collect Inputs (diff, metadata, file list)
Wave 2: Auggie Deep Pass     ← loads refs/auggie-prompts.md
Wave 3: Validate & Synthesize ← loads refs/severity-rubric.md
Wave 4: Post & Handoff       ← loads refs/remediation-handoff.md
```

---

### Wave 0: Resolve & Validate Target

**Preconditions**: command flags parsed; one of `target`, `--diff`, `--snapshot` provided.

**Steps**:

1. Classify target mode (`pr`, `diff`, `snapshot`).
2. Validate environment:
   - `command -v auggie` (STOP if missing)
   - `git rev-parse --is-inside-work-tree` (STOP if not in repo)
   - For PR mode: `gh auth status` (STOP if unauthed)
3. Resolve target details:
   - PR: fetch `gh pr view <id> --json number,headRefName,baseRefName,title,body,files,url,headRepositoryOwner,headRepository` and the merge-base diff range
   - Diff: validate `<base>` ref exists (`git rev-parse <base>`)
   - Snapshot: validate path exists and is readable
4. Compute `target_slug` (`pr-62`, `diff-master-HEAD`, `snapshot-src-superclaude-cli`) and create `--output-dir` (default `.dev/reviews/<target-slug>-<YYYYMMDDHHMMSS>/`).
5. Emit machine-readable header to the audit log:

```
<!-- SC:AUGGIE-REVIEW:TARGET
mode: <pr|diff|snapshot>
slug: <target_slug>
focus: <comma-list>
depth: <quick|standard|deep>
output_dir: <abs-path>
auggie_version: <version>
gh_authed: <bool>
-->
```

**Exit criteria**: Target resolved, output dir created, audit log opened. Emit "Wave 0 complete: target=<slug> mode=<mode>".

---

### Wave 1: Collect Inputs

**Preconditions**: Wave 0 complete.

**Steps**:

1. Collect the **diff body** (skip if `--snapshot`):
   - PR: `gh pr diff <id>` → `<output-dir>/diff.patch`
   - Diff: `git diff <base>...HEAD` → `<output-dir>/diff.patch`
2. Collect the **changed-file list** (skip if `--snapshot`):
   - PR: from the `files` field of `gh pr view`
   - Diff: `git diff --name-only <base>...HEAD`
3. For snapshot mode, build the file list via `find <path> -type f` (excluding obvious binaries: `.png`, `.jpg`, `.pdf`, `.lock`).
4. Collect PR metadata if PR mode (`title`, `body`, `baseRefName`, `headRefName`, `url`).
5. Compute diff size: total lines, files-changed count. Emit `WARN` to audit log if thresholds exceeded.
6. Determine chunking strategy:
   - ≤ 1500 diff lines OR ≤ 15 files: single Auggie invocation
   - 1500-5000 lines OR 16-30 files: chunk by directory (one Auggie call per top-level dir)
   - > 5000 lines: STOP unless `--force`; report "diff too large"

**Exit criteria**: `diff.patch` (if applicable), `files.txt`, and `metadata.json` saved under `<output-dir>/inputs/`. Chunking strategy decided.

---

### Wave 2: Auggie Deep Pass

**Preconditions**: Wave 1 complete. **Load `refs/auggie-prompts.md`** for the structured prompt templates.

**Concept**: Shell out to `auggie --print --output-format json --ask --workspace-root <repo>` with a carefully-constructed prompt that:
- Describes the review target (PR title/body, diff, or file list)
- Provides the focus areas (from `--focus`)
- Specifies the JSON output schema Auggie must return
- Tells Auggie to ground every finding in a real `file:line` and to flag uncertainty

The `--ask` flag restricts Auggie to retrieval/non-editing tools — exactly what we need for a review.

**Steps**:

1. Read `refs/auggie-prompts.md` (NOT before now — lazy loading).
2. Construct the Auggie instruction from the appropriate template:
   - PR/diff: `pr-review-prompt` template (interpolate title, body, diff path, focus areas)
   - Snapshot: `snapshot-review-prompt` template (interpolate file list, focus areas)
3. Invoke Auggie (one call per chunk if chunking). **Use this exact invocation pattern** — common mistakes are called out below.

```bash
auggie --print \
       --output-format json \
       --ask \
       --workspace-root <repo-root> \
       --max-turns <8 quick | 16 standard | 24 deep> \
       ${AUGGIE_MODEL:+--model "$AUGGIE_MODEL"} \
       --instruction-file <output-dir>/auggie-prompt-<chunk>.txt \
       > <output-dir>/auggie-raw-<chunk>.json 2>> <output-dir>/auggie-stderr.log
```

> **Common pitfalls (read before invoking)**:
>
> - **Flag name**: the correct flag is `--output-format json`, NOT `--json`. The latter is not a real auggie flag and will cause `exit 1`.
> - **JSON unwrapping (full pipeline)**: even with `--output-format json`, Auggie wraps its response in an outer envelope (`{"type":"result","result":"<fenced-json-string>",...}`), prepends a `--max-turns` preamble line when `--max-turns N` is passed (`Applying --max-turns override: N over agentMaxIterations=500`), and the inner `.result` string is itself wrapped in a ```json ...``` markdown fence. The complete unwrap pipeline is:
>
>   ```bash
>   tail -n +2 auggie-raw.json | jq -r '.result' | sed -n '/^```json$/,/^```$/p' | sed '1d;$d' | jq '.'
>   ```
>
>   Steps: `tail -n +2` strips the `--max-turns` preamble line; `jq -r '.result'` unwraps the outer envelope; `sed -n '/^```json$/,/^```$/p'` extracts the fenced inner block; `sed '1d;$d'` drops the opening and closing fence markers; final `jq '.'` validates and pretty-prints. If `jq` parse fails, save the raw response and downgrade status to `partial`.
> - **`--instruction-file` requires a real path**: `mkdir -p <output-dir>` before writing the prompt file. Auggie reads the file from disk, not stdin.
> - **`--workspace-root` matters**: must point to the repo root (`git rev-parse --show-toplevel`), not the diff path or PR subtree. Auggie's index is scoped to this directory.
> - **Indexer cold-start**: if `auggie-stderr.log` mentions "indexing" or "not ready", retry with `--wait-for-indexing` once before treating as a failure.

4. For `--depth deep`, after the initial pass spawn one **per-persona Auggie call** for each focus area not adequately covered (security, architecture, performance), reusing the same diff but a persona-specialized prompt. Aggregate the per-persona JSON outputs alongside the main pass.
5. For `--depth deep` **only**, additionally spawn the `auggie-reviewer` agent via the `Task` tool to run an independent Claude-side review pass that does not see Auggie's findings yet — this provides a cross-check used in Wave 3.

**Exit criteria**: One or more `auggie-raw-*.json` files under `<output-dir>/`, all containing structured findings. Audit log notes any non-zero exit codes, retries, or chunk failures.

**Failure handling**:

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Auggie exits non-zero on a chunk | Retry once with `--max-turns +50%` | If still failing, log chunk as `chunk_skipped`, continue |
| Auggie returns non-JSON output | Parse what's parseable; log unparseable tail | Mark `partial` status |
| Auggie indexer not ready | Pass `--wait-for-indexing` and retry | Same as above |
| Auggie not on PATH (post-Wave-0) | STOP with clear message | None |

---

### Wave 3: Validate & Synthesize

**Preconditions**: Wave 2 complete, ≥ 1 raw Auggie JSON file. **Load `refs/severity-rubric.md`** for the consistent severity grading scheme.

**Steps**:

1. Read `refs/severity-rubric.md`.
2. Parse all `auggie-raw-*.json` files. Each finding from Auggie should carry at least: `title`, `file`, `line` (or `line_range`), `severity`, `category`, `evidence`, `recommendation`. Findings missing `file` and `line` go to a `needs-grounding` bucket (not auto-dropped — see step 4).
3. **File:line validation pass** (non-negotiable):
   - For each finding, `Read` the cited file at the cited line range. Confirm the line exists and (where possible) confirm the cited snippet actually appears on that line.
   - For PR/diff mode, additionally confirm the line is within the diff hunks (a finding citing a line nowhere near the changes is downgraded to "context" or dropped, depending on severity).
   - For `needs-grounding` findings, attempt to ground them using `mcp__auggie__codebase-retrieval` or `Grep`. If grounding succeeds, promote; if not, drop and log.
4. **Dedupe pass**:
   - Findings on the same `file:line` with similar titles → merge, keep the higher severity and union the evidence.
   - Findings that are restatements of the PR description's own caveats → drop with a note in the audit log.
5. **Severity remap** using `refs/severity-rubric.md`. Auggie's self-reported severity is a hint, not authoritative — apply the rubric uniformly.
6. **Persona cross-check** (`--depth deep` only):
   - Compare the `auggie-reviewer` agent's independent findings against the deduped Auggie findings. Findings present in only one source are marked accordingly (`source: auggie-only | claude-only | both`) and given a slight confidence adjustment in the rubric.
7. Compose the final markdown report at `<output-dir>/REVIEW.md` using this structure:

```markdown
# Code Review: <target>

**Target**: <PR #N | diff range | snapshot path>
**Reviewer**: /sc:auggie-review (depth=<depth>, focus=<focus>)
**Generated**: <YYYY-MM-DD HH:MM TZ>
**Source PR**: <URL if applicable>
**Base ↔ Head**: <baseRef> ↔ <headRef>
**Stats**: <N> files, <N> lines, <N> findings (<N> dropped during grounding)

---

## Summary

<2-4 sentence executive summary: top 2-3 risks, overall sentiment, recommendation (block | request-changes | nits-only | approve-ish).>

## Findings

### 🔴 Critical (block merge)

#### C1. <Short title>
- **File**: `path/to/file.ext:LINE`
- **Category**: security | data-integrity | correctness | …
- **Source**: auggie | claude | both
- **Evidence**:
  ```<lang>
  <real code excerpt from the cited lines>
  ```
- **Why this matters**: <one paragraph>
- **Recommendation**: <concrete change>

(repeat per finding)

### 🟠 High (should fix before merge)
(same structure)

### 🟡 Medium (fix in this PR if cheap, otherwise file followup)
(same structure)

### 🟢 Low (nice-to-have)
(same structure)

### 💬 Nits (style, naming, comments)
(condensed list)

## Architectural / Cross-Cutting Observations

<Anything that isn't anchored to a single file:line — layering concerns, missing abstractions, coupling smells, anti-pattern clusters. Each item still cites the files where the pattern manifests.>

## Audit

- Auggie chunks: <N> (succeeded: <N>, retried: <N>, skipped: <N>)
- Findings dropped during grounding: <N> (see `audit.log`)
- Persona cross-check: <enabled|disabled>
- Token cost: Claude ≈ <N> (orchestration), Auggie ≈ <N> (deep pass)
```

8. Write `<output-dir>/audit.log` with: every Auggie invocation (cmd + duration + exit), every finding with grounding result, every dedupe decision, every severity remap, dropped findings with reasons.

**Exit criteria**: `REVIEW.md` and `audit.log` written. Audit log includes the machine-readable summary header:

```
<!-- SC:AUGGIE-REVIEW:SUMMARY
status: <success|partial>
critical: <N> high: <N> medium: <N> low: <N> nit: <N>
dropped: <N>
auggie_chunks: <N>
duration_sec: <N>
-->
```

---

### Wave 4: Post & Handoff

**Preconditions**: Wave 3 complete. **Load `refs/remediation-handoff.md`** for the exact phrasing and command sequence used in the remediation offer.

**Steps**:

1. **Post to PR** (only if target is PR AND `--post-pr` AND `findings_count > 0`):
   - Summary comment: `gh pr review <PR> --comment --body-file <output-dir>/REVIEW.md`
   - Inline comments for each Critical and High finding (in `--depth deep` mode also for Medium):
     ```bash
     gh api repos/<owner>/<repo>/pulls/<PR>/comments \
        -f body="<finding-body>" \
        -f commit_id="<head-SHA>" \
        -f path="<file>" \
        -F line=<LINE> \
        -f side=RIGHT
     ```
   - Capture the review URL from `gh pr view <PR> --json reviews -q '.reviews[-1].url'` and record it.
   - **Never** use `--approve` or `--request-changes`; this is a `--comment` review only. The human merges; the skill advises.
2. **Surface results to the user** in the chat:
   - Counts by severity
   - Path to `REVIEW.md`
   - Review URL (if posted)
3. **Offer the remediation chain** (only if `--remediation-offer` AND `findings_count.critical + findings_count.high > 0`):
   - Read `refs/remediation-handoff.md` and use the exact prompt template there.
   - The offer must list the four phases and ask one yes/no question.
4. If the user accepts:
   - **Phase A**: Invoke `/sc:design <REVIEW.md path> --type architecture --format spec --output <output-dir>/remediation-spec.md`
   - **Phase B**: Invoke the `task-builder` skill with a BUILD_REQUEST citing the remediation spec (file path passed as input)
   - **Phase C**: After task-builder returns, invoke `/sc:reflect --type task --analyze` against the new task file
   - If reflect-analyze flags issues, surface them and ask the user whether to refactor the tasklist or accept-as-is
   - **Phase D (execution)**: Wait for explicit user sign-off, then execute the task file (the user runs `/task <path>` or equivalent — the skill does NOT auto-execute)
   - **Phase E**: After execution completes, invoke `/sc:reflect --type task --validate` BEFORE the user commits. Block on validation failures, do not proceed to commit suggestion.
5. Return the structured output contract.

**Exit criteria**: Report posted (if applicable), remediation chain offered (if applicable), output contract returned.

---

## Will Do

- Run Auggie as the primary review engine; lean on its indexed-codebase strength
- Validate every finding's file:line before including it in the report
- Catch narrow bugs **and** architectural/anti-pattern risks (the rubric in `refs/severity-rubric.md` defines both categories explicitly)
- Post the markdown report to the PR automatically (per the user's stated default — they opted in by running the command on a PR)
- Attach inline comments for Critical/High findings, anchored to real lines in the diff
- Offer a deterministic remediation chain (`/sc:design` → `task-builder` → `/sc:reflect`-analyze → execute → `/sc:reflect`-validate) and wait for explicit user acceptance before starting
- Persist the full audit (raw Auggie JSON, validation results, dedupe decisions, severity remaps) for traceability

## Will Not Do

- Activate from conversational keywords — explicit `/sc:auggie-review` invocation or PR-creation hook only
- Use `gh pr review --approve` or `--request-changes` — strictly `--comment`
- Include findings whose file:line cannot be validated against a real file
- Modify code under review (advisory only)
- Auto-trigger the remediation chain — that step is always user-gated
- Auto-commit after the remediation chain — `/sc:reflect --type task --validate` is the final gate before the user commits manually
- Run on diffs > 5000 lines without `--force` (no useful signal at that scale; recommend scoping down)
- Trust Auggie's self-reported severity — always remap via the rubric

## Error Handling

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| `auggie` missing | STOP at Wave 0 with install hint | None |
| `gh` unauthed for PR mode | STOP at Wave 0 with `gh auth login` hint | None |
| Auggie chunk fails after retry | Continue with remaining chunks; status `partial`; note in audit and report header | Findings from successful chunks still produced |
| Findings all fail file:line grounding | Emit `REVIEW.md` with empty findings sections and a clear "review inconclusive — Auggie findings could not be grounded" notice; status `partial` | Do not post to PR in this case |
| `gh pr review` post fails | Save the body to `<output-dir>/REVIEW.md`, surface the path to the user, status `partial` | None |
| Task-builder skill not available | Surface the remediation spec path and stop; do not fail the whole review | None |
| User declines remediation offer | Return success; report still posted | None |
| Diff > 5000 lines without `--force` | STOP at Wave 1 with "diff too large; rerun with `--focus` or `--force`" | None |

## Token Cost Profile

| Depth | Auggie tokens (offloaded) | Claude tokens (orchestration) | Wall clock |
|-------|---------------------------|-------------------------------|-----------|
| quick | ~5-15k | ~2-4k | 2-4 min |
| standard | ~15-40k | ~5-10k | 5-8 min |
| deep | ~40-100k | ~12-20k | 10-15 min |

The Auggie tokens are billed to Auggie's free/low-cost retrieval tier; Claude tokens are the constrained resource. The skill's value proposition is the ~5x-10x ratio: most of the work happens in Auggie, while Claude does only what it must (validation, synthesis, posting, handoff).
