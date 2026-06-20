# R1: Sibling-skill template + reflect command-file Related-Commands section

- **Topic**: Sibling-skill template + reflect command-file Related-Commands section
- **Scope**: `sc-auggie-review-protocol/SKILL.md`, `sc-reflect-protocol/SKILL.md` §9, `commands/reflect.md`, `commands/auggie-review.md`
- **Status**: Complete
- **Date**: 2026-05-31
- **Researcher**: R1

## 0. Path corrections (vs task brief)

The task brief referenced `commands/sc/reflect.md` and `commands/sc/auggie-review.md`. The **source of truth** at IronClaude is **flat** at `src/superclaude/commands/` (no `sc/` subdir). The `sc/` subdir only exists in synced `.claude/commands/sc/`. CLAUDE.md global rule 6: edit src/, then `make sync-dev`.

Source-of-truth paths the executor MUST edit:
- `/config/workspace/IronClaude/src/superclaude/commands/reflect.md` (265 LOC) — target of Change 10 §3.8 one-line addition
- `/config/workspace/IronClaude/src/superclaude/commands/auggie-review.md` (169 LOC) — template for new `pr-bot-validate.md` command file
- `/config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` (376 LOC) — primary skill template per MERGED-PROPOSAL §3.1
- `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md` (1585 LOC) — §9 contract-block shape source

**Critical terminology correction**: The proposal §3.8 says the discoverability bridge goes into `sc-reflect-protocol/SKILL.md` §16 "Related Commands". But reflect SKILL.md §16 is `## 16. Refs (loaded on-demand per wave)` (line 1387) — that is NOT a "Related Commands" section. The actual `## Related Commands` lives in the **command file** `commands/reflect.md:258`. Treat the proposal text "§16 Related Commands" as the executor's target = `commands/reflect.md:258`'s `## Related Commands` block. Executor should add **one bullet** there.

---

## 1. sc-auggie-review-protocol skill structure

### 1.1 Frontmatter (verbatim, SKILL.md:1-12)

```yaml
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
```

Note the **2-block frontmatter pattern**: real `---`-delimited YAML (3 fields only: `name`, `description`, `allowed-tools`) + an **HTML comment block** for extended/non-parsed metadata (`category`, `complexity`, `mcp-servers`, `personas`). The new sibling MUST adopt this pattern.

**MERGED-PROPOSAL §3.1 specifies the new sibling's frontmatter verbatim** (lines 54-60):
```yaml
---
name: sc:pr-bot-validate-protocol
description: "Validate external bot-review signal (Augment Code, CodeRabbit, etc.) against current PR HEAD via the 6-way parallel cross-validation pipeline; emit a GitHub status check that branch protection consumes as a first-class merge gate."
allowed-tools: Read, Grep, Glob, Bash(gh *), Bash(git *), Bash(jq *), Bash(mkdir *), Bash(date *), Bash(wc *), TodoWrite, Task, Write, Edit, Skill
---
```

Extended metadata block for sibling (derived from auggie pattern):
```
<!-- Extended metadata (for documentation, not parsed):
category: quality
complexity: advanced
mcp-servers: [sequential, serena]
personas: [analyzer, qa, architect]
-->
```

### 1.2 ## section headers in order (SKILL.md, with line numbers)

1. `# Auggie Review Protocol` (h1, line 14)
2. `## Purpose` (line 16)
3. `## Required Input (STOP if missing)` (line 24)
4. `## Output Contract` (line 47)
5. `## Wave Structure` (line 62)
6. `### Wave 0: Resolve & Validate Target` (line 76)
7. `### Wave 1: Collect Inputs` (line 110)
8. `### Wave 2: Auggie Deep Pass` (line 134)
9. `### Wave 3: Validate & Synthesize` (line 196)
10. `### Wave 4: Post & Handoff` (line 295)
11. `## Will Do` (line 334)
12. `## Will Not Do` (line 344)
13. `## Error Handling` (line 355)
14. `## Token Cost Profile` (line 368)

Total LOC: **376**. The new sibling SKILL.md should mirror this skeleton with 4 waves (Wave 0 + Waves 1-4 per MERGED-PROPOSAL §3.2 table at lines 67-77).

### 1.3 Output Contract block shape (lines 47-61) — verbatim shape

```markdown
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
```

NB: `sc-auggie-review-protocol` uses a **simple markdown table** for its contract — no `contract_version` field, no inline YAML block. The new sibling MUST instead adopt the **richer `sc-reflect-protocol` §9 pattern** (versioned contract block — see §2 below) because MERGED-PROPOSAL §3.3 mandates `pr_bot_validate_contract_version: "1.0"` and a verbatim YAML field family.

### 1.4 Wave structure preamble (lines 62-73) — exact shape

```
## Wave Structure

The protocol runs in five waves. Each wave has explicit entry/exit criteria. Refs are loaded **per-wave**, never pre-loaded.

(fenced block listing Wave 0..Wave 4 with the refs each wave loads)
```

Per-wave anatomy (consistent across Waves 0-4 in auggie SKILL.md):
- `### Wave N: <Name>` header
- `**Preconditions**: ...` line
- (optional) `**Concept**: ...` block for waves with non-obvious mechanism
- `**Steps**:` numbered list
- (optional) code fences for exact CLI invocations
- `**Exit criteria**:` line
- (optional) `**Failure handling**:` markdown table

### 1.5 Error Handling Matrix shape (lines 355-366)

A 3-column markdown table: `| Scenario | Behavior | Fallback |`. The new sibling should produce its own per MERGED-PROPOSAL §6 risk list (gh CLI drift, PENDING-masquerading, 422/429 on `gh api .../statuses/<sha>`, budget-insufficient, empty-PR-set).

### 1.6 Directory contents (sc-auggie-review-protocol/)

```
sc-auggie-review-protocol/
├── SKILL.md             (376 LOC)
├── evals/
│   └── evals.json
└── refs/
    ├── auggie-prompts.md
    ├── remediation-handoff.md
    └── severity-rubric.md
```

**No `__init__.py`** in auggie skill (see §5 below for parity check across all skills).

---

## 2. sc-reflect-protocol §9 patterns reusable for new sibling skill

### 2.1 §9 versioned contract block (SKILL.md:487-576)

```markdown
## 9. Output Contract (Versioned)

Two-block contract: stable + telemetry. Written to `<output>/return-contract.yaml` AND returned inline. (See `refs/report-template.md` for the human-facing REPORT.md skeleton that renders these fields.)

### 9.1 Stable contract (contract_version: 1.0)

```yaml
contract_version: "1.0"
status: success | partial | failed | dry-run
...
```
```

Key reusable patterns the new sibling SHOULD adopt (because MERGED-PROPOSAL §3.3 requires versioning):

1. **Top-level `## N. Output Contract (Versioned)` section** (replaces auggie's plain `## Output Contract`).
2. **Subsection `### N.1 Stable contract (contract_version: 1.0)`** with **YAML code fence** containing the exact `pr_bot_validate_*` field family from MERGED-PROPOSAL lines 130-149.
3. **Prose sentence**: "Two-block contract: ... Written to `<output>/return-contract.yaml` AND returned inline."
4. **Derived-boolean pattern** at the bottom of the YAML block (`outcome_verified` in reflect; mirrored as `pr_bot_validated` per MERGED-PROPOSAL line 148).
5. **`### N.4 Evolution discipline`** — reflect §9.4 documents minor/major bump rules + unknown-field-tolerance. MERGED-PROPOSAL §3.3 lines 150-153 references this pattern; the new sibling should include an equivalent §9.4 block.

### 2.2 Verbatim YAML field family from MERGED-PROPOSAL §3.3 (lines 131-149)

```yaml
# sc-pr-bot-validate-protocol/return-contract.yaml — contract_version: "1.0"
pr_bot_validate_contract_version: "1.0"

# Enumerated field family (A's U-001 ported verbatim, prefix renamed)
pr_bot_validate_path: <abs path> | null      # path to merge-gate-decision.yaml
pr_bot_validate_pr_count: <int>              # accepted_count from pr-set discovery
pr_bot_validate_buckets:
  confirmed: <int>
  still_valid: <int>
  false_positive: <int>
  out_of_scope: <int>
pr_bot_validate_prs_blocking_merge: [<int>, ...]
pr_bot_validate_complete: <bool>
pr_bot_validate_status_check_conclusion: success | failure | neutral | pending | skipped | null
pr_bot_validate_pre_gate_passed: <bool>

# Derived single-axis convenience
pr_bot_validated: <bool>
```

And the auxiliary `merge-gate-decision.yaml` shape (MERGED-PROPOSAL lines 156-172) — distinct artifact, lives at `<output>/merge-gate-decision.yaml`.

---

## 3. commands/reflect.md ## Related Commands — verbatim text + insertion guidance

### 3.1 Location

- **Source-of-truth path**: `/config/workspace/IronClaude/src/superclaude/commands/reflect.md`
- **Section header line**: `258`
- **Last bullet line**: `265`
- **Total file LOC**: `265` (the `## Related Commands` section is the **final** section in the file)

### 3.2 Verbatim current text (lines 258-265)

```markdown
## Related Commands

- **`/sc:troubleshoot`** — Invokes `/sc:reflect --type task --analyze` (Wave 6 Phase B) and `/sc:reflect --type task --validate` (Wave 6 Phase D); the legacy grammar is preserved for this caller.
- **`/sc:adversarial`** — Invoked by reflect Wave 4 to debate competing reviewer verdicts in Tier 2. Reflect consumes the producer's `artifacts_dir` field and remaps it into its own `adversarial_artifacts_dir` contract field (mechanical resolution; not user-facing).
- **`task-builder` skill** — Invoked by reflect Wave 6 when `--remediate` is accepted; consumes the M1-frozen BUILD_REQUEST schema documented in `refs/remediation-handoff.md`.
- **`/sc:task`** — May auto-trigger `/sc:reflect` as an end-of-task hook when configured (deferred per Open Question 2 in the rebuild task file).
- **`/sc:analyze`** — Complementary; use for read-only quality/security/architecture analysis when there is no spec or diff to reflect against.
- **`/sc:brainstorm`** — Upstream of `/sc:reflect` when the spec or tasklist itself is genuinely ambiguous and the user wants to scope it first.
```

### 3.3 Insertion guidance (executor's exact Edit operation)

Bullet list ordering is **NOT alphabetical** — it appears to be **role-based** (callers/consumers first → upstream/complementary last). The new entry is a **consumer** of reflect (per MERGED-PROPOSAL §3.7 "Reflect's contract is consumed read-only"), so semantically it slots **after `/sc:troubleshoot`** (both are downstream consumers reading reflect's return contract — `sc:troubleshoot` Wave 6 Phase D pattern is the precedent cited in MERGED-PROPOSAL §3.7 line 207).

Per MERGED-PROPOSAL §3.8 line 216, the **verbatim text** the executor inserts is:

```markdown
- **`/sc:pr-bot-validate`** — PR-layer audit sibling skill; consumes reflect's return contract read-only at its Wave 4 to validate external bot-review signal as a first-class merge-gate input. Use when the work-unit you'd reflect on is *spread across multiple PRs with bot reviews attached*.
```

**Recommended insertion point**: after the `/sc:troubleshoot` bullet (line 260), before the `/sc:adversarial` bullet (line 261). Both `/sc:troubleshoot` and the new `/sc:pr-bot-validate` describe **downstream callers that consume reflect's contract**; grouping them is consistent with the existing pattern. (Alt: append at end after `/sc:brainstorm` line 265 — also acceptable; less semantic but simpler diff.)

**Edit operation blueprint** (for executor):
```
old_string: "- **`/sc:troubleshoot`** — Invokes `/sc:reflect --type task --analyze` (Wave 6 Phase B) and `/sc:reflect --type task --validate` (Wave 6 Phase D); the legacy grammar is preserved for this caller.\n- **`/sc:adversarial`**"
new_string: "- **`/sc:troubleshoot`** — Invokes `/sc:reflect --type task --analyze` (Wave 6 Phase B) and `/sc:reflect --type task --validate` (Wave 6 Phase D); the legacy grammar is preserved for this caller.\n- **`/sc:pr-bot-validate`** — PR-layer audit sibling skill; consumes reflect's return contract read-only at its Wave 4 to validate external bot-review signal as a first-class merge-gate input. Use when the work-unit you'd reflect on is *spread across multiple PRs with bot reviews attached*.\n- **`/sc:adversarial`**"
```

### 3.4 Synced-destination follow-up

After editing src/, executor runs `make sync-dev` per CLAUDE.md global rule 6, which copies to:
- `/config/workspace/IronClaude/.claude/commands/sc/reflect.md`

Then `make verify-sync` confirms parity. The proposal references "sc-reflect-protocol/SKILL.md §16 Related Commands" but the **actual** discoverability surface is the **command file**, not the SKILL.md. Reflect SKILL.md §16 (line 1387) is `## 16. Refs (loaded on-demand per wave)` — wholly different content. Executor MUST edit `commands/reflect.md`, NOT `skills/sc-reflect-protocol/SKILL.md` §16.

---

## 4. commands/auggie-review.md command-file structure (template for pr-bot-validate.md)

### 4.1 Frontmatter (lines 1-9, verbatim)

```yaml
---
name: auggie-review
description: "Auggie-powered code review for PRs, local diffs, or file snapshots — narrow bugs + architectural risks + anti-patterns, with auto-posted PR review and optional remediation handoff"
category: quality
complexity: advanced
mcp-servers: [sequential, serena]
personas: [analyzer, architect, security, qa, refactorer]
argument-hint: "[<PR-num|PR-URL>|--diff <base>...HEAD|--snapshot <path>] [--focus security,architecture,quality,performance,all] [--depth quick|standard|deep] [--post-pr|--no-post-pr] [--remediation-offer|--no-remediation-offer]"
---
```

NB: The **command-file** frontmatter is **richer** than the SKILL.md frontmatter — it includes `category`, `complexity`, `mcp-servers`, `personas`, and `argument-hint` directly in the YAML (not in an HTML comment). The new `pr-bot-validate.md` command file should follow this pattern. Suggested:
```yaml
---
name: pr-bot-validate
description: "Validate external bot-review signal against current PR HEAD via the 6-way parallel cross-validation pipeline; emit a GitHub commit-status check that branch protection consumes as a first-class merge gate"
category: quality
complexity: advanced
mcp-servers: [sequential, serena]
personas: [analyzer, qa, architect]
argument-hint: "[--pr <N>|--prs <N1,N2,...>] [--max-prs <N>] [--bot-source-filter <id>] [--bot-sources <path>] [--depth standard|deep] [--output-dir <path>] [--budget-remaining <int>] [--no-post-status-check]"
---
```
Flags enumerated from MERGED-PROPOSAL §3.4 lines 182-190.

### 4.2 ## section headers in order (commands/auggie-review.md)

1. `# /sc:auggie-review - Auggie-Powered Code Review` (h1, line 11)
2. `## Triggers` (line 13)
3. `## Required Input` (line 23)
4. `## Usage` (line 33)
5. `## Options` (line 44) — markdown table
6. `## Behavioral Flow` (line 57) — 4-numbered-step summary; the **full protocol lives in the skill**
7. `## Activation` (line 66) — MANDATORY invocation of the skill via `> Skill <skill-name>`
8. `## MCP Integration` (line 73)
9. `## Tool Coordination` (line 80)
10. `## Examples` (line 90) — 4 fenced bash examples
11. `## Boundaries` (line 141) — bipartite `**Will:**` / `**Will Not:**` lists
12. `## Related Commands` (line 163) — final section

Total LOC: **169**.

### 4.3 Activation block pattern (lines 66-71, verbatim)

```markdown
## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:auggie-review-protocol

Do NOT proceed with protocol execution using only this command file. The full behavioral specification — Auggie invocation, finding validation, severity rubric, PR posting, remediation handoff — is in the protocol skill.
```

The new `commands/pr-bot-validate.md` MUST include an equivalent block invoking `Skill sc:pr-bot-validate-protocol`.

### 4.4 Where new pr-bot-validate.md should mirror auggie-review.md

| auggie-review.md section | Adaptation for pr-bot-validate.md |
|---|---|
| `## Triggers` | 3 paths: direct `/sc:pr-bot-validate`, GitHub Actions workflow (`.github/workflows/pr-bot-validate.yml`), programmatic invocation. **No conversational keyword activation** (per MERGED-PROPOSAL §3.1 line 62 "invoked ONLY by the `/sc:pr-bot-validate` command or by the GitHub Action"). |
| `## Required Input` | One of: `--pr <N>`, `--prs <N1,N2,...>`, or auto-discovery (no flags → Wave 1 discovers from `gh pr list`). |
| `## Usage` | Bash code fence with ~5 invocation examples (single PR, multi-PR, with `--bot-source-filter`, with `--budget-remaining`, with `--no-post-status-check`). |
| `## Options` | Markdown table with the 9 flags from MERGED-PROPOSAL §3.4. |
| `## Behavioral Flow` | 4-step summary: parse → validate env (`gh`, `git`, `jq`) → hand off via Activation → surface `merge-gate-decision.yaml` + status-check URL. |
| `## Activation` | `> Skill sc:pr-bot-validate-protocol` |
| `## MCP Integration` | Sequential (4-wave reasoning), Serena (no — sibling does no symbol nav). Likely just Sequential. |
| `## Tool Coordination` | `Bash(gh *)`, `Bash(git *)`, `Bash(jq *)`, `Read`/`Grep`/`Glob`, `Task` (per-PR fan-out at Wave 2), `Write` (artifacts), `Skill` (invokes `sc-auggie-review-protocol` at Wave 2 + `sc-reflect-protocol` at Wave 4). |
| `## Examples` | 4 fenced examples paralleling auggie's structure: single PR validate, multi-PR sweep, CI invocation, manual with `--budget-remaining`. |
| `## Boundaries` | `Will:` / `Will Not:` — Will Not includes: never call from inside `sc-reflect-protocol` (per MERGED-PROPOSAL §7 anti-collision invariant line 316); never auto-execute remediation; never use `--approve`/`--request-changes`. |
| `## Related Commands` | Bullets for `/sc:reflect` (consumed at Wave 4), `/sc:auggie-review` (invoked at Wave 2), `task-builder` skill (handoff target), `/sc:troubleshoot` (peer audit-class sibling). |

---

## 5. __init__.py + refs/ parity check

### 5.1 __init__.py audit across all `sc-*` skills

```
HAS __init__: sc-adversarial-protocol
NO   __init__: sc-auggie-review-protocol      ← primary template per §3.1
NO   __init__: sc-brainstorm-protocol
HAS __init__: sc-cleanup-audit-protocol
HAS __init__: sc-cli-portify-protocol
NO   __init__: sc-crash-recovery
NO   __init__: sc-pm-protocol
NO   __init__: sc-recommend-protocol
HAS __init__: sc-reflect-protocol             ← contract-shape source
HAS __init__: sc-release-split-protocol
NO   __init__: sc-review-translation-protocol
HAS __init__: sc-roadmap-protocol
HAS __init__: sc-tasklist-protocol
HAS __init__: sc-task-protocol
NO   __init__: sc-troubleshoot-protocol
NO   __init__: sc-validate-roadmap-protocol
HAS __init__: sc-validate-tests-protocol
```

**Verdict: mixed pattern (10 HAS / 7 NO), no clear convention.** Parity is **NOT** required. The primary template (`sc-auggie-review-protocol`) does NOT have one; the new sibling can omit it without breaking convention. If executor wants belt-and-suspenders, create an empty `__init__.py` to match `sc-reflect-protocol`'s pattern (the skill the sibling reads from). **Recommendation: omit** — match the primary template `sc-auggie-review-protocol` for minimum surprise.

### 5.2 refs/ directory presence

Both `sc-auggie-review-protocol/refs/` and `sc-reflect-protocol/refs/` exist. MERGED-PROPOSAL §3.5 requires the new sibling to create `refs/bot-review-sources.yaml`. So `refs/` directory is **mandatory** for the new sibling. R2 will detail the ref-file content.

### 5.3 evals/ directory presence

`sc-auggie-review-protocol/evals/evals.json` exists. MERGED-PROPOSAL §8 (line 323) places the falsifier suite at `.dev/eval-workspaces/sc-pr-bot-validate/cases/falsifier-suite/bot-validation-mixed-buckets.yaml` — **outside** the skill directory (under `.dev/`, not under `src/superclaude/skills/`). So the skill itself does NOT need an `evals/` subdir for the v1.0 ship. R2 should confirm; this is at the boundary of R1/R2 scopes.

---

## 6. Concrete "Per-step Edit operation" blueprints for the task file's checklist

These are the verbatim operations the executor performs in Phases 2-4 of the task file. (Phase 1 = pre-flight; Phase 5 = downstream eval/workflow which R2 covers.)

### Phase 2 — Create the new sibling skill directory + SKILL.md

**Step 2.1** — Create directory + refs/ subdir (Bash):
```bash
mkdir -p /config/workspace/IronClaude/src/superclaude/skills/sc-pr-bot-validate-protocol/refs
```

**Step 2.2** — Write SKILL.md (Write tool) at:
`/config/workspace/IronClaude/src/superclaude/skills/sc-pr-bot-validate-protocol/SKILL.md`

Skeleton (mirrors §1.2 + adopts §2 contract pattern):
1. Frontmatter from MERGED-PROPOSAL §3.1 lines 55-60 verbatim.
2. Extended-metadata HTML comment block (category, complexity, mcp-servers, personas).
3. `# PR Bot-Review Validate Protocol` h1.
4. `## Purpose` — paraphrase MERGED-PROPOSAL §2 + §1's argument.
5. `## Required Input (STOP if missing)` — table with `--pr`, `--prs`, auto-discovery modes; STOP conditions (no `gh` auth, no `git` repo, no `jq`).
6. `## Output Contract (Versioned)` — adopt reflect §9 versioned pattern; embed YAML from MERGED-PROPOSAL §3.3 lines 130-149 + merge-gate-decision.yaml shape lines 156-172.
7. `## Wave Structure` preamble: 4 waves + Wave 0 implicit per MERGED-PROPOSAL §3.2 line 77.
8. `### Wave 0: Parse & Validate Target` — gh version probe (MERGED-PROPOSAL §6 line 288), `--budget-remaining` parse + degradation (§3.2 lines 82-83), initial PENDING status-check post (§3.3 line 112-117).
9. `### Wave 1: PR Discovery` — `gh pr list ... --json number,title,headRefName,author,reviews`, filter by `refs/bot-review-sources.yaml`, cap at `--max-prs`. Empty-PR-set behavior (§3.2 line 80) returns `success / prs_processed: 0 / merge_gate_decision: not_applicable`.
10. `### Wave 2: Parallel Cross-Validation` — `Task` agent per PR, each invokes `Skill sc-auggie-review-protocol` with `--no-post-pr --no-remediation-offer --depth standard --output-dir /tmp/pr-<N>-auggie-fresh/`. Output: `/tmp/remediation-pr-<N>.md` per PR.
11. `### Wave 3: Aggregation` — read each `/tmp/remediation-pr-<N>.md`; write `<output>/PROPOSALS.md` + `<output>/PROPOSALS-normalized.md`.
12. `### Wave 4: Reflect-Grounded Validation + Status Post` — `Skill sc-reflect-protocol --mode pre --spec <output>/PROPOSALS-normalized.md --depth standard`. Read return-contract.yaml. Apply §3.3 gate (PASS/FAIL/PENDING/NEUTRAL). Post `gh api repos/{owner}/{repo}/statuses/{sha}`. Write `<output>/merge-gate-decision.yaml`.
13. `## Will Do` — bipartite list.
14. `## Will Not Do` — including: never invoked from `sc-reflect-protocol` (anti-collision invariant per §7 line 316); never auto-execute remediation; never use `--approve`/`--request-changes`; never silently fail on budget mismatch.
15. `## Error Handling` — matrix table covering: `gh` missing/unauthed (STOP Wave 0); `gh pr list` zero matches (success empty-set per §3.2 line 80); Wave 2 sub-agent failure on one PR (continue with remaining, partial status); Wave 4 reflect returns `status: failed` (gate FAIL with reason); `gh api ... statuses` 422/429 (retry 2s/8s/32s, persistent failure → PENDING + WARN per §6 line 297); budget-insufficient (HALT with `failure_reason: budget-insufficient`).
16. `## Token Cost Profile` — table per §6 line 286: Manual 6-PR ≈35-70k tokens, 10-15min; CI 1-PR ≈6-12k tokens, 2-4min.

### Phase 3 — Create the slash-command file

**Step 3.1** — Write at:
`/config/workspace/IronClaude/src/superclaude/commands/pr-bot-validate.md`

Skeleton mirrors §4 verbatim (frontmatter pattern; 12 sections from §4.2 in order). The `## Activation` block invokes `Skill sc:pr-bot-validate-protocol`.

### Phase 4 — Update commands/reflect.md ## Related Commands

**Step 4.1** — Edit `/config/workspace/IronClaude/src/superclaude/commands/reflect.md` with the Edit operation in §3.3 above (insertion after `/sc:troubleshoot` bullet).

### Phase 5 (handed to R2) — Sync + verify + workflow + ref file + eval case

After Phases 2-4:
```bash
make -C /config/workspace/IronClaude sync-dev
make -C /config/workspace/IronClaude verify-sync
```
This syncs both new files (SKILL.md, pr-bot-validate.md, edited reflect.md) into `.claude/`. R2 covers the GitHub Actions workflow at `.github/workflows/pr-bot-validate.yml`, the `refs/bot-review-sources.yaml` content, and the falsifier eval case under `.dev/eval-workspaces/sc-pr-bot-validate/`.

---

## 7. Summary

Research complete. Five concrete artifacts the executor needs:

1. **Primary skill template** — `sc-auggie-review-protocol/SKILL.md` (376 LOC) provides the 4-wave skeleton, frontmatter shape (3-field YAML + extended-metadata HTML comment), wave anatomy (Preconditions/Steps/Exit-criteria), and error-handling matrix shape. New sibling structurally mirrors this with the 4 waves enumerated in MERGED-PROPOSAL §3.2 lines 67-77.
2. **Contract block pattern** — `sc-reflect-protocol/SKILL.md` §9 (lines 487-576) provides the **versioned contract** pattern (`## N. Output Contract (Versioned)` → `### N.1 Stable contract (contract_version: 1.0)` → YAML fence → `### N.4 Evolution discipline`). The sibling MUST use this pattern (NOT auggie's simpler table) because MERGED-PROPOSAL §3.3 mandates `pr_bot_validate_contract_version: "1.0"` and the verbatim `pr_bot_validate_*` field family.
3. **Related Commands target** — `/config/workspace/IronClaude/src/superclaude/commands/reflect.md:258-265` contains the current 6-bullet list. The exact verbatim text of all 6 bullets is captured in §3.2 above. New bullet from MERGED-PROPOSAL §3.8 line 216 inserts after the `/sc:troubleshoot` bullet (between lines 260 and 261). Edit operation blueprint in §3.3 ready to execute. **Critical correction**: proposal text says "§16 Related Commands" but `sc-reflect-protocol/SKILL.md §16` is "Refs" (line 1387) — the actual `## Related Commands` lives in the **command file**, not the skill file.
4. **Slash-command file template** — `commands/auggie-review.md` (169 LOC, 12 sections) provides the shape for the new `commands/pr-bot-validate.md`. Frontmatter is richer than SKILL.md (includes `category`, `mcp-servers`, `personas`, `argument-hint` directly). `## Activation` block pattern (line 66-71) is mandatory.
5. **__init__.py + refs/ parity** — `__init__.py` is **mixed** across 17 sc-skills (10 HAS / 7 NO); the primary template (`sc-auggie-review-protocol`) has none — recommend omit. `refs/` directory is MANDATORY for `refs/bot-review-sources.yaml` (R2's domain).

**Blockers**: None. All source-of-truth paths exist and are readable. One terminology ambiguity in the merged proposal (§16 vs `## Related Commands`) resolved in §0 + §3.4 above.
