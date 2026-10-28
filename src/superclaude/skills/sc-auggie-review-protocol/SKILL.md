---
name: sc:auggie-review-protocol
description: "Code review protocol for PRs, local diffs, and file snapshots — the auggie-reviewer agent reviews a git/gh-defined diff, every finding is grounded by Read, the report posts to the PR, and a remediation handoff chain is offered"
allowed-tools: Read, Grep, Glob, Bash(gh *), Bash(git *), Bash(jq *), Bash(wc *), Bash(find *), Bash(mkdir *), Bash(cat *), Bash(mv *), Bash(cp *), Bash(date *), TodoWrite, Task, Write, Edit, Skill
---

<!-- Extended metadata (for documentation, not parsed):
category: quality
complexity: advanced
mcp-servers: [serena]
personas: [analyzer, architect, security, qa, refactorer]
-->

# Auggie Review Protocol

## Purpose

Run an evidence-based code review of a Pull Request, local diff, or file snapshot. The review must catch **both** narrow bugs (off-by-one, null-deref, leaked resources, race conditions, untyped boundaries) **and** higher-level concerns (architectural drift, layering violations, anti-patterns, coupling smells, missing abstractions, performance regressions, security exposure).

**Engine contract**: The `auggie-reviewer` agent does the review. `git` and `gh` define the diff. Serena may hint at callers and symbol ranges. A Read of the file on disk (or of `diff.patch` under the head-mismatch rule) is the only evidence that may appear in the report.

**Hallucination contract**: Every finding emitted in the final report must cite a `file:line` that exists in the repo at the time of review. Findings that cannot be grounded are dropped, not downgraded. This is non-negotiable — a "review" full of imaginary line numbers is worse than no review.

**Absence rule**: a miss from Serena or any index never proves absence. Only a Grep or Read that cites its pattern and root does.

## Required Input (STOP if missing)

The skill receives one of three target modes from `/sc:auggie-review`:

| Mode | Required | Resolved Form |
|------|----------|---------------|
| **PR** | `<PR-num>` or `<PR-URL>` | `gh pr view <id> --json number,headRefName,headRefOid,baseRefName,headRepository,headRepositoryOwner,title,body,files,url` |
| **Diff** | `--diff <base>...HEAD`, or implicit (dirty tree, no target) | explicit: `git diff <base>...HEAD`; implicit: `git diff $(git merge-base origin/<default-branch> HEAD)` |
| **Snapshot** | `--snapshot <path>` | `find <path> -type f` (validate path exists) |

**STOP** if:

- Target cannot be resolved (PR not found, ref doesn't exist, path missing)
- For PR mode, `gh auth status` reports unauthed

**WARN (proceed)** if:

- Diff exceeds 1500 lines (emit a chunking-mode notice)
- More than 30 files changed (recommend `--focus` to scope down)
- The PR base branch is not the repo's default branch (mention in report header)
- Implicit diff mode and `git ls-files --others --exclude-standard` lists untracked files: list them in the WARN. They are not review inputs.

## Output Contract

The skill returns:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success`, `partial` (some findings dropped for hallucination, or a chunk skipped), `failed` |
| `report_path` | string | Absolute path to the markdown report |
| `audit_log_path` | string | Absolute path to the audit log (findings JSON, validation results, decisions) |
| `pr_review_url` | string | URL of the posted `gh pr review` comment (empty if `--no-post-pr` or non-PR target) |
| `findings_count` | object | `{critical: N, high: N, medium: N, low: N, nit: N}`. Counts unmerged admitted defects only, keeps this shape, and equals the ledger's `findings_count` |
| `candidates_path` | string | Absolute path to `candidates.json`, the ledger of every grounded candidate and its disposition |
| `not_admitted_path` | string | Absolute path to `NOT-ADMITTED.md`, the local record of non-defect candidates (never posted) |
| `disposition_count` | object | `{defect: N, unproven: N, rejected: N, intentional_limitation: N, documented_prerequisite: N, merged: N}` |
| `remediation_count` | object | `{critical: N, high: N}`, from the unmerged, remediation-eligible Critical/High defects |
| `coverage_complete` | boolean | `false` when a chunk or persona pass was skipped, input was truncated, or any candidate was not fully admitted |
| `dropped_count` | int | Findings dropped because file:line could not be validated |
| `remediation_offered` | boolean | Whether the remediation chain was offered |
| `remediation_accepted` | boolean | If offered, whether the user accepted |

## Wave Structure

The protocol runs in five waves. Each wave has explicit entry/exit criteria. Refs are loaded **per-wave**, never pre-loaded.

```text
Wave 0: Resolve & Validate Target
Wave 1: Collect Inputs (diff, metadata, file list)
Wave 2: Review Agent Pass     ← loads refs/auggie-prompts.md
Wave 3: Validate & Synthesize ← loads refs/severity-rubric.md
Wave 4: Post & Handoff       ← loads refs/remediation-handoff.md
```

---

### Wave 0: Resolve & Validate Target

**Preconditions**: command flags parsed; one of `target`, `--diff`, `--snapshot` provided, or the implicit dirty-tree diff.

**Steps**:

1. Classify target mode (`pr`, `diff`, `snapshot`).
2. Validate environment:
   - `git rev-parse --is-inside-work-tree` (STOP if not in repo)
   - For PR mode: `gh auth status` (STOP if unauthed)
3. Resolve target details:
   - PR: fetch the `gh pr view` fields above. Compare `headRefOid` to `git rev-parse HEAD`; record `head_match`.
   - Record `local_sha` (`git rev-parse HEAD`) and `worktree_dirty` (whether `git status --porcelain` lists changes). `base` and `head` are the base and head refs of the target; snapshot mode records `base: null`.
   - Diff: validate `<base>` ref exists (`git rev-parse <base>`). Implicit mode: resolve `git merge-base origin/<default-branch> HEAD`.
   - Snapshot: validate path exists and is readable
4. Compute `target_slug` (`pr-62`, `diff-master-HEAD`, `snapshot-src-superclaude-cli`) and create `--output-dir` (default `.dev/reviews/<target-slug>-<YYYYMMDDHHMMSS>/`).
5. Emit machine-readable header to the audit log:

```text
<!-- SC:AUGGIE-REVIEW:TARGET
mode: <pr|diff|snapshot>
slug: <target_slug>
focus: <comma-list>
depth: <quick|standard|deep>
output_dir: <abs-path>
base: <base ref, or null for snapshot>
head: <head ref>
head_match: <true|false|n/a>
local_sha: <git rev-parse HEAD>
worktree_dirty: <true|false>
head_object_check: <match|mismatch|null>
evidence_source: <local_read|head_object|diff_new_side>
gh_authed: <bool>
-->
```

The rules for `evidence_source`, `head_object_check` and the committed reads of explicit `--diff` mode are in `refs/claim-gate.md`, section "Attribution". Snapshot mode records `introduced_in: not_applicable_snapshot` for every candidate and never says "introduced", "regression" or "this PR".

**Head mismatch** (PR mode, `head_match: false` — fork PRs and PRs not checked out): validate in-diff findings against the new side of `diff.patch`; do not Read the local file as evidence; do not query Serena; keep out-of-diff findings as candidates with `in_diff: false` (admission decides). Do not STOP and do not `gh pr checkout`.

**Exit criteria**: Target resolved, output dir created, audit log opened. Emit "Wave 0 complete: target=<slug> mode=<mode>".

---

### Wave 1: Collect Inputs

**Preconditions**: Wave 0 complete.

**Steps**:

1. Collect the **diff body** (skip if `--snapshot`):
   - PR: `gh pr diff <id>` → `<output-dir>/diff.patch`
   - Diff: `git diff <base>...HEAD` (implicit: `git diff <merge-base>`, which keeps uncommitted tracked edits) → `<output-dir>/diff.patch`
2. Collect the **changed-file list** (skip if `--snapshot`):
   - PR: from the `files` field of `gh pr view`
   - Diff: `git diff --name-only <base>...HEAD` (implicit: `git diff --name-only <merge-base>`)
3. For snapshot mode, build the file list via `find <path> -type f` (excluding obvious binaries: `.png`, `.jpg`, `.pdf`, `.lock`).
4. Collect PR metadata if PR mode (`title`, `body`, `baseRefName`, `headRefName`, `headRefOid`, `url`).
5. Compute diff size: total lines, files-changed count. Emit `WARN` to audit log if thresholds exceeded.
6. **Empty diff** (zero changed lines): write a short `REVIEW.md` (`# Code Review: <target>`, `## Findings` saying there is nothing to review, `## Audit`), return status `success` with all counts 0. Do not spawn agents. Do not post. Skip Waves 2-4.
7. Determine chunking strategy:
   - ≤ 1500 diff lines OR ≤ 15 files: one chunk
   - 1500-5000 lines OR 16-30 files: chunk by top-level directory
   - > 5000 lines: STOP unless `--force`, at every depth; report "diff too large; rerun with `--focus` or `--force`"

**Exit criteria**: `diff.patch` (if applicable), `files.txt`, and `metadata.json` saved under `<output-dir>/inputs/`. Chunking strategy decided.

---

### Wave 2: Review Agent Pass

**Preconditions**: Wave 1 complete. **Load `refs/auggie-prompts.md`** for the prompt templates and the findings JSON contract.

**Steps**:

1. Read `refs/auggie-prompts.md` (NOT before now — lazy loading).
2. Build the prompt from the appropriate template:
   - PR/diff: `pr-review-prompt` (interpolate title, body, diff path, file list, focus areas, `head_match`)
   - Snapshot: `snapshot-review-prompt` (interpolate file list, focus areas)
   - **Impact hints (optional; PR/diff mode, `standard`/`deep`, `head_match: true` only):** spawn one `codebase-memory-scout` agent via `Task`. Ask it for callers, up to 3 levels, of the functions the diff changes, as `file:line` lists. Append the result to the prompt under the heading "Caller hints (index may lag; Read before citing)". The scout's index can be minutes behind the working tree, so a hint is never evidence and a missing caller proves nothing. If the agent type is unavailable or errors, record `impact_hints: unavailable` in the audit log and continue without hints.
3. Spawn the `auggie-reviewer` agent via `Task`, at every depth, in batched messages, at most five runs in flight:
   - `quick` / `standard`: one general pass per chunk.
   - `deep`: the general pass per chunk, plus four persona passes (security, architect, performance, qa) **once each on the whole diff**, not once per chunk.
4. The agent returns the findings JSON as its **final message**; it writes no files. The orchestrator writes it to `<output-dir>/findings-<chunk>.json` (persona passes: `findings-<persona>.json`). On non-JSON output, retry that run once; if it still fails, log `chunk_skipped` and set status `partial`.

5. **jq preflight** (before Wave 3): run `jq --version`. If `jq` is not available, the status is `failed` with reason `invariant_check_unavailable`; `REVIEW.md` and `audit.log` are still written. `allowed-tools` is not a prerequisite check.

**Exit criteria**: One or more `findings-*.json` files under `<output-dir>/`, or every chunk skipped. Audit log notes retries and skipped chunks.

---

### Wave 3: Validate & Synthesize

**Preconditions**: Wave 2 complete. **Load `refs/severity-rubric.md`** for the consistent severity grading scheme. **Load `refs/claim-gate.md`** at step 3b: it holds every admission rule, the ledger schema and the invariant check.

**Steps**:

1. Read `refs/severity-rubric.md`.
2. Parse all `findings-*.json` files and mint an id `<findings-file-stem>#<n>` for every entry, with one `n` sequence across `findings[]` and `cross_cutting_observations[]` of the same file. Each finding should carry at least: `title`, `file`, `line` (or `line_range`), `severity`, `category`, `evidence`, `recommendation`, `claim`. Findings missing `file` and `line` go to a `needs-grounding` bucket (not auto-dropped — see step 3).
3. **File:line validation pass** (non-negotiable; the head-mismatch exception is in `refs/claim-gate.md`, section "Location grounding"):
   - For each finding, `Read` the cited file at the cited line range (under head mismatch: match the new side of `diff.patch` instead). Confirm the line exists and (where possible) confirm the cited snippet actually appears on that line. A line that fails this check is dropped into `dropped_ungrounded[]`, not downgraded.
   - For PR/diff mode, additionally note whether the line is within the diff hunks. A line outside the diff is kept as a candidate with `in_diff: false`; admission decides.
   - For `needs-grounding` findings, ground in this order: `Grep`, then Serena `find_symbol` / `find_referencing_symbols`, then `Read`. Serena output is never cited without that Read. If grounding succeeds, promote the finding into admission; if not, drop and log.
   - "Nothing calls this" is not a dead-code finding unless `Grep` under `src/`, `plugins/`, and `tests/` returns zero hits (cite the pattern and roots). Prose and Markdown findings are grounded by Read.
3b. **Admission**: read `refs/claim-gate.md`. Re-Read every line the `claim` cites, then give each grounded candidate exactly one disposition (`defect`, `unproven`, `rejected`, `intentional_limitation`, `documented_prerequisite`) by the sections "Claim classes", "Claim scope", "Admission table" and "Refutation record". Only a `defect` is graded and published.
3c. **Attribution**: record `introduced_in` and `current_status` for every candidate by the section "Attribution" of `refs/claim-gate.md`.
4. **Mechanism dedupe**: group candidates by `mechanism_key` by the section "Mechanism dedupe" of `refs/claim-gate.md`. This replaces the earlier same-line merge and the dropping of PR-caveat restatements; a restatement of a caveat is evaluated by admission and stays in the ledger.
5. **Severity remap** using `refs/severity-rubric.md`, for unmerged defects only; every other record has `severity: null`. The agent's self-reported severity is a hint, not authoritative — apply the rubric uniformly.
5b. **Write the ledger** `<output-dir>/candidates.json` by the section "Ledger schema" of `refs/claim-gate.md`, including `run_status`, `findings_count` and every candidate's `evidence_sources`. All three are written before step 6b.
6. Compose the final markdown report at `<output-dir>/REVIEW.md` and the local record `<output-dir>/NOT-ADMITTED.md`. `REVIEW.md` uses this structure and holds unmerged defects only:

````markdown
# Code Review: <target>

**Target**: <PR #N | diff range | snapshot path>
**Reviewer**: /sc:auggie-review (depth=<depth>, focus=<focus>)
**Generated**: <YYYY-MM-DD HH:MM TZ>
**Source PR**: <URL if applicable>
**Base ↔ Head**: <baseRef> ↔ <headRef>
**Stats**: <N> files, <N> lines, <N> findings (<N> dropped during grounding)

---

## Summary

<2-4 sentence executive summary: top 2-3 risks, overall sentiment, recommendation (block | request-changes | nits-only | approve-ish). Name findings only by id; cite no file:line here.>

Not admitted: <U> unproven, <R> rejected, <L> intentional limitations, <P> documented prerequisites, <M> merged (see NOT-ADMITTED.md)

## Findings

### 🔴 Critical (block merge)

#### C1. <Short title> (id: <id>)
- **File**: `path/to/file.ext:LINE`
- **Category**: security | data-integrity | correctness | …
- **Pass**: general | security | architect | performance | qa
- **Evidence kind**: runtime_reproduced | static_traced | protocol_literal
- **Evidence**:
  ```<lang>
  <real code excerpt from the cited lines>
  ```

- **Why this matters**: <one paragraph>
- Not established: <consequence> (<reason row>)
- **Qualification**: <scope> (<scope_citation>)
- **Recommendation**: <concrete change>

(repeat per finding; the `Not established` line appears once per excluded consequence and the `Qualification` line only when the defect is qualified)

### 🟠 High (should fix before merge)

(same structure; a High cross-cutting defect is also a heading entry here)

### 🟡 Medium (fix in this PR if cheap, otherwise file followup)

(same structure)

### 🟢 Low (nice-to-have)

(same structure)

### 💬 Nits (style, naming, comments)

- <!-- id: <id> --> <title> (`path/to/file.ext:LINE`) — **Evidence kind**: <kind>

## Architectural / Cross-Cutting Observations

<Only Medium and Low defects that are not anchored to a single file:line — layering concerns, missing abstractions, coupling smells, anti-pattern clusters. Each is one top-level list item, and each still cites the files where the pattern manifests. Critical and High cross-cutting defects are heading entries under `## Findings`, never list items here.>

- <!-- id: <id> --> <title> — **Evidence kind**: <kind>
  - `path/to/file.ext:LINE` <where the pattern manifests>

## Audit

- Agent runs: <N> (succeeded: <N>, retried: <N>, skipped: <N>)
- Findings dropped during grounding: <N> (see `audit.log`)
- Persona passes: <enabled|disabled>

````

   `REVIEW.md` rules (the tag grammar is in `refs/claim-gate.md`, section "Report tag grammar"):
   - `## Findings` and the Cross-Cutting section hold unmerged defects only. There is no separate section for non-defects; the one counts line in `## Summary` points to `NOT-ADMITTED.md`.
   - Every Critical and High defect, including a cross-cutting one, is a heading entry under `## Findings`. Nits, and Medium or Low cross-cutting defects, are top-level list items starting with `<!-- id: <id> -->`.
   - Every defect entry carries its `**Evidence kind**` line and, when present, its `Not established` lines and qualification.
   - The section headers `# Code Review:`, `## Findings` and `## Audit` are kept.

   `NOT-ADMITTED.md` is mandatory and is generated from the ledger: every non-defect record with its id, title, disposition, reason row and citation; merged members under "Merged into <id>"; and the excluded consequences of defects. It is never posted to a PR and never passed to `/sc:design`.
6b. **Invariant check**: run the single `jq` program from `refs/claim-gate.md`, section "Invariant check", as `jq -e -n --slurpfile ledger <output-dir>/candidates.json --rawfile review <output-dir>/REVIEW.md -f <extracted block>`. Record its exit code as `jq_exit` in `candidates.json` and in `audit.log`. A non-zero or missing `jq_exit`, or a missing `candidates.json`, makes the status `failed`. The reported status is the ledger's `run_status` when `jq_exit` is 0.
7. Write `<output-dir>/audit.log` with: every agent run (pass + duration + outcome), every finding with grounding result, every admission decision with its row ids, every dedupe decision, every severity remap, dropped findings with reasons, and `jq_exit`.

**Status rules**: `coverage.complete == false` never yields `success`. The empty-diff short-circuit in Wave 1 stays `success`. `REVIEW.md` and `audit.log` are written on every status, `failed` included.

**Exit criteria**: `REVIEW.md`, `NOT-ADMITTED.md`, `candidates.json` and `audit.log` written. Audit log includes the machine-readable summary header:

```text
<!-- SC:AUGGIE-REVIEW:SUMMARY
status: <success|partial|failed>
critical: <N> high: <N> medium: <N> low: <N> nit: <N>
unproven: <N> rejected: <N> intentional_limitation: <N> documented_prerequisite: <N>
coverage_complete: <true|false>
dropped: <N>
agent_runs: <N>
duration_sec: <N>
-->
```

---

### Wave 4: Post & Handoff

**Preconditions**: Wave 3 complete. **Load `refs/remediation-handoff.md`** for the exact phrasing and command sequence used in the remediation offer.

**Steps**:

1. **Post to PR** (only if target is PR AND `--post-pr` AND status is not `failed` AND `findings_count > 0`). Nothing is posted when the status is `failed`. Posting and inline comments read only the unmerged defects in `candidates.json`:
   - Summary comment: `gh pr review <PR> --comment --body-file <output-dir>/REVIEW.md`. The posted bytes are the `REVIEW.md` that passed the invariant check.
   - Inline comments for each unmerged Critical and High defect (in `--depth deep` mode also for Medium):

     ```bash
     gh api repos/<owner>/<repo>/pulls/<PR>/comments \
        -f body="<finding-body>" \
        -f commit_id="<headRefOid>" \
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
3. **Offer the remediation chain** (only if `--remediation-offer` AND status is not `failed` AND `remediation_count.critical + remediation_count.high >= 1`):
   - Read `refs/remediation-handoff.md` and use the exact prompt template there.
   - The offer must list the five phases, name the route (plan, or mdtm when `--depth deep` was requested), and ask one yes/no question.
4. If the user accepts, select the route from the review `--depth` the user requested: `quick`/`standard` → **plan route**; `deep` → **MDTM route** (see `refs/remediation-handoff.md`, "Route selection"):
   - **Phase A** (both routes): Invoke `/sc:design <REVIEW.md path> --type architecture --format spec --output <output-dir>/remediation-spec.md`
   - **Phase B**: plan route → build `remediation-workflow-source.md` (spec copy + `## References` + any `## Review Feedback` from `remediation-review-notes.md`, list syntax flattened with every line's text kept) and invoke `Skill sc:workflow-protocol` on THAT file (not the bare spec) with `--depth standard --handoff none` (never `--handoff implement`, never `--output`), yielding the tasklist package `.dev/tasks/to-do/<id>/<id>.md`; MDTM route → invoke the `task-builder` skill with a BUILD_REQUEST citing the remediation spec (file path passed as input)
   - **Phase C**: plan route → consume the pre-review `sc:workflow` already ran (`reflect_status` / `reflect_report_path` in its return contract; do not re-run `/sc:reflect --mode pre`); MDTM route → `/sc:reflect --type task --analyze` against the new task file
   - If the Phase C review flags issues, surface them and ask the user whether to refactor or accept-as-is
   - **Phase D (execution)**: Wait for explicit user sign-off, then the user runs `/sc:implement <pkg>/<id>.md` (plan route) or `/task <path>` (MDTM route) — the skill does NOT auto-execute
   - **Phase E**: After execution completes, invoke `/sc:reflect --mode post --spec <remediation-spec.md> --tasklist <pkg-now>/<id>.md --task-log <pkg-now>/progress.md --diff <baseline_ref>` (plan route; `<pkg-now>` = `to-do/<id>` or `done/<id>` after implement archives it) or `/sc:reflect --type task --validate` (MDTM route) BEFORE the user commits. Block on validation failures, do not proceed to commit suggestion.
5. Return the structured output contract.

**Exit criteria**: Report posted (if applicable), remediation chain offered (if applicable), output contract returned.

---

## Will Do

- Run the `auggie-reviewer` agent as the review engine at every depth
- Validate every finding's file:line before including it in the report
- Publish only admitted defects; keep unproven, rejected, intentional-limitation and documented-prerequisite records locally in `candidates.json` and `NOT-ADMITTED.md`
- Catch narrow bugs **and** architectural/anti-pattern risks (the rubric in `refs/severity-rubric.md` defines both categories explicitly)
- Post the markdown report to the PR automatically (per the user's stated default — they opted in by running the command on a PR)
- Attach inline comments for Critical/High findings, anchored to real lines in the diff
- Offer a deterministic remediation chain (`/sc:design` → `sc:workflow` → `/sc:reflect`-pre → user-run `/sc:implement` → `/sc:reflect`-post; with `--depth deep`, `task-builder` → `/task` replaces the workflow/implement pair) and wait for explicit user acceptance before starting
- Persist the full audit (findings JSON, validation results, dedupe decisions, severity remaps) for traceability

## Will Not Do

- Activate from conversational keywords — explicit `/sc:auggie-review` invocation or a programmatic skill call only
- Use `gh pr review --approve` or `--request-changes` — strictly `--comment`
- Include findings whose file:line cannot be validated against a real file
- Publish a non-defect candidate (unproven, rejected, intentional limitation or documented prerequisite) as a finding; those records stay in `candidates.json` and `NOT-ADMITTED.md`
- Modify code under review (advisory only)
- Auto-trigger the remediation chain — that step is always user-gated
- Auto-commit after the remediation chain — `/sc:reflect --type task --validate` is the final gate before the user commits manually
- Trust the agent's self-reported severity — always remap via the rubric

## Error Handling

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| `gh` unauthed for PR mode | STOP at Wave 0 with `gh auth login` hint | None |
| Agent run fails after retry | Continue with remaining runs; status `partial`; note in audit and report header | Findings from successful runs still produced |
| Findings all fail file:line grounding | Emit `REVIEW.md` with empty findings sections and a clear "review inconclusive — findings could not be grounded" notice; status `partial` | Do not post to PR in this case |
| `gh pr review` post fails | Save the body to `<output-dir>/REVIEW.md`, surface the path to the user, status `partial` | None |
| Task-builder skill not available | Surface the remediation spec path and stop; do not fail the whole review | None |
| User declines remediation offer | Return success; report still posted | None |
