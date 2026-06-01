# R2 Research: GitHub Workflow + Eval-Workspace + Ref File Patterns

**Researcher:** R2
**Date:** 2026-05-31
**Status:** Complete
**Scope:** `.github/workflows/`, `.dev/eval-workspaces/sc-reflect/`, `sc-reflect-protocol/refs/`, `Makefile`

---

## 1. Existing workflow inventory + closest-pattern selection

Files under `/config/workspace/IronClaude/.github/workflows/`:

| File | Trigger | Permissions | Runner | Token | Status-check post? |
|---|---|---|---|---|---|
| `publish-pypi.yml` | `release.published`, `workflow_dispatch` | `contents: read` (lines 21-22) | `ubuntu-latest` (line 28) | `secrets.PYPI_API_TOKEN` (line 110) | no |
| `pull-sync-framework.yml` | `schedule cron`, `workflow_dispatch` (lines 3-6) | `contents: write` (line 11) | `ubuntu-latest` (line 10) | implicit `GITHUB_TOKEN` (push) | no |
| `quick-check.yml` | `pull_request: branches: [master, integration]` (lines 3-5) | implicit/default | `ubuntu-latest` (line 9) | none | no |
| `test.yml` | `push`, `pull_request: branches: [master, integration]`, `workflow_dispatch` (lines 3-9) | implicit | `ubuntu-latest` matrix py 3.10-3.12 (lines 14, 17-19) | none (codecov optional) | no |
| `readme-quality-check.yml` | `pull_request: paths:`, `push: branches:`, `workflow_dispatch` (lines 3-10) | `contents: read`, `pull-requests: write`, `issues: write` (lines 12-15) | `ubuntu-latest` (line 21) | implicit `GITHUB_TOKEN` for PR comments | no (posts PR comment, not status) |

**Critical findings:**

1. **No existing workflow uses `gh api .../statuses/<sha>`.** Confirmed by `grep -rn "gh api\|statuses" .github/workflows/` returning only references in `publish-pypi.yml` to unrelated string literals (`from superclaude import __version__`) — no workflow today posts a commit-status check via `gh api`. This is a greenfield pattern for IronClaude. (Evidence: grep run 2026-05-31; only `auggie-review-protocol/SKILL.md:305` documents the `gh api` pattern, in a non-Actions context.)
2. **No workflow today invokes the `claude` CLI.** No workflow imports the Anthropic CLI. The `pr-bot-validate.yml` would be the first.
3. **Closest pattern** for trigger-shape + permissions: `readme-quality-check.yml` (lines 1-15) — runs on `pull_request`, has an explicit `permissions:` block, is the only existing workflow that interacts with the PR comment surface. It does NOT use `pull_request_review`, but its `pull_request: paths:` trigger and explicit permissions block are the closest template.
4. **Closest pattern** for `gh api` token usage (in skill docs, not in a workflow): `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:305` (`gh api repos/<owner>/<repo>/pulls/<PR>/comments ...`). This is documentation, not an Actions-runnable workflow.
5. **Runner choice:** all existing workflows use `ubuntu-latest` (no self-hosted runners). New workflow should match.
6. **Token usage:** workflows that mutate (write-permissions) use `${{ secrets.GITHUB_TOKEN }}` implicitly via `gh` (which auto-reads `GITHUB_TOKEN` from env). For `gh api .../statuses/<sha>`, the same auto-auth applies *provided* the workflow declares `permissions: statuses: write`.

---

## 2. New `pr-bot-validate.yml` workflow blueprint

The new workflow MUST:
- Trigger on `pull_request_review` (any review submission, comment, edit) AND `pull_request: types: [synchronize, opened]`.
- Declare `permissions: statuses: write, pull-requests: read, contents: read` — `statuses: write` is the load-bearing permission for posting commit-status checks.
- Run `ubuntu-latest`.
- Use `${{ secrets.GITHUB_TOKEN }}` (auto-injected; no PAT needed when `statuses: write` is granted).
- Invoke `claude --skill sc:pr-bot-validate-protocol` (passing the PR ref + diff context).
- Post a commit-status check `sc-pr-bot-validate / merge-gate` via `gh api repos/${{ github.repository }}/statuses/${{ github.event.pull_request.head.sha }} -f state=<success|failure|pending> -f context='sc-pr-bot-validate / merge-gate' -f description='...'`.

**Draft YAML (the executor will write this):**

```yaml
name: PR Bot Validate

on:
  pull_request_review:
    types: [submitted, edited]
  pull_request:
    types: [synchronize, opened, reopened]

permissions:
  contents: read
  pull-requests: read
  statuses: write

jobs:
  pr-bot-validate:
    name: Validate Bot Reviews (merge-gate)
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout PR head
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install UV
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH

      - name: Install dependencies
        run: |
          uv pip install --system -e ".[dev]"

      - name: Post pending status
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh api repos/${{ github.repository }}/statuses/${{ github.event.pull_request.head.sha }} \
            -f state=pending \
            -f context='sc-pr-bot-validate / merge-gate' \
            -f description='Validating bot reviews…'

      - name: Invoke sc:pr-bot-validate-protocol
        id: validate
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude --skill sc:pr-bot-validate-protocol \
            --pr ${{ github.event.pull_request.number }} \
            --head-sha ${{ github.event.pull_request.head.sha }} \
            --output /tmp/pr-bot-validate-output.json
          # script writes verdict (pass|fail) to GITHUB_OUTPUT
          echo "verdict=$(jq -r .verdict /tmp/pr-bot-validate-output.json)" >> "$GITHUB_OUTPUT"
          echo "summary=$(jq -r .summary /tmp/pr-bot-validate-output.json)" >> "$GITHUB_OUTPUT"

      - name: Post final commit-status
        if: always()
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          STATE=${{ steps.validate.outputs.verdict == 'pass' && 'success' || 'failure' }}
          gh api repos/${{ github.repository }}/statuses/${{ github.event.pull_request.head.sha }} \
            -f state=$STATE \
            -f context='sc-pr-bot-validate / merge-gate' \
            -f description="${{ steps.validate.outputs.summary }}"
```

**Rationale anchors:**
- `permissions.statuses: write` matches the GitHub REST API `POST /repos/{owner}/{repo}/statuses/{sha}` requirement (the same surface the auggie-review skill documents at `sc-auggie-review-protocol/SKILL.md:305`).
- `${{ secrets.GITHUB_TOKEN }}` is auto-issued by GitHub Actions; no PAT or stored secret needed for status posting once `statuses: write` is declared. (Confirmed by README/test.yml/readme-quality-check.yml never declaring a separate token for `gh` calls.)
- The `claude --skill sc:pr-bot-validate-protocol` invocation assumes the Claude CLI is installed on the runner. The Makefile / setup steps in `test.yml:31-37` install UV first; `claude` CLI installation may need an extra step (`curl -fsSL https://claude.ai/install | sh` or equivalent). **Blocker to confirm with executor:** how `claude` CLI is provisioned in the runner. (Existing workflows do not install `claude`.)

---

## 3. New eval-workspace directory layout — `.dev/eval-workspaces/sc-pr-bot-validate/`

Mirrors `sc-reflect/` 1:1. Source: `ls -la /config/workspace/IronClaude/.dev/eval-workspaces/sc-reflect/`.

```
.dev/eval-workspaces/sc-pr-bot-validate/
├── SPEC.md                              # full skill spec (mirror of sc-reflect/SPEC.md shape)
├── README.md                            # workspace usage notes
├── aggregate_iteration.py               # iteration aggregator (copy from sc-reflect)
├── grader.py                            # case grader (see §4 for reuse strategy)
├── evals/
│   └── evals.json                       # eval registry (case ids, modes, assertions)
├── cases/
│   ├── falsifier-suite/
│   │   ├── README.md                    # falsifier-suite sufficiency contract
│   │   ├── fixtures/                    # placeholder fixture content
│   │   │   └── pr-bot-validation-mixed-buckets.md   # iteration-3 fixture stub
│   │   └── pr-bot-validation-mixed-buckets.yaml    # canonical falsifier YAML
│   └── <pilot-case-dirs>/               # e.g. pr-clean-bot-aligned/, pr-mixed-buckets/
│       ├── expected.yaml
│       └── input/
│           ├── pr-diff.patch
│           └── bot-reviews.json
├── iterations/                          # populated by `make pr-bot-validate-eval-quick`
└── skill-snapshot/
    └── pr-bot-validate-v1.md            # frozen skill snapshot for eval
```

Evidence: this mirrors `sc-reflect/` layout (`aggregate_iteration.py`, `cases/`, `evals/`, `grader.py`, `iterations/`, `skill-snapshot/`, `SPEC.md`) confirmed at `.dev/eval-workspaces/sc-reflect/` listing (Bash output line: `total 208 ... aggregate_iteration.py cases evals grader.py iterations skill-snapshot SPEC.md`).

---

## 4. `grader.py` reuse strategy

**Recommendation: COPY + extend** (the same pattern sc-reflect used relative to sc-brainstorm).

**Evidence:** `grader.py:13-22` self-describes the inheritance pattern:

> "Inherits the 8 sc-brainstorm baseline assertion types (file_exists, frontmatter_field, section_present, section_enumerated, yaml_field, yaml_field_min, yaml_substring, dir_count) and extends with 10 new types per refs/grader-extensions.md"

And `SKILL.md:904`:

> "All semantic types live in `.dev/eval-workspaces/sc-reflect/grader.py` (copy from sc-brainstorm's `grader.py` and extend per `refs/grader-extensions.md`)."

**Why copy not import:**
1. Each eval workspace is self-contained — no inter-workspace Python imports exist today (no `sys.path` hacks, no shared package).
2. `grader.py` is a standalone script invoked via `uv run python .dev/eval-workspaces/sc-reflect/grader.py <iteration-dir>` (Makefile lines 496, 504-505). The script reads `evals/evals.json` and per-case `eval_metadata.json` from its own workspace.
3. The new skill adds **new assertion types** (e.g., `bot_review_attributed`, `merge_decision_correct`, `bot_class_canonicalised`) that sc-reflect's grader does not know about. Copying lets us extend without touching sc-reflect's grader.

**Plan:**
- Copy `sc-reflect/grader.py` → `sc-pr-bot-validate/grader.py` (~21 KB).
- Strip the 10 sc-reflect-specific extensions (`citation_resolves`, `matrix_covers_items`, `checkpoint_logged`, `deviation_class_matches`, `falsifier_skeleton_present`, etc.) — keep the 8 baseline types.
- Add the new assertion types the BRV-MG skill requires (defined in the skill's own `refs/grader-extensions.md`).

**Module-level imports of sc-reflect's grader:** `import json, re, sys, functools.reduce, pathlib.Path, yaml`. No third-party imports beyond `yaml`; copy works cleanly.

---

## 5. Falsifier YAML shape (verbatim from `T2-judge-class-collision.yaml`)

```yaml
# SKELETON — iteration-3 follow-up authors full fixture and flips status to active.
# Spec §12.5 line 1011 (Khan ICML 2024 violation case) + W-A8 spec-panel fix.
id: T2-judge-class-collision
status: skeleton-pending-iteration-3-fixture
description: "Tests that the judge-class-collision-detector in the reviewer rotation logic ... refuses to seat a reviewer whose model class matches the calibrator's model class — the Khan ICML 2024 disjoint-set rule."
expected_behavior: "The reviewer-seating algorithm MUST reject the colliding seat ..."
expected_grader_emission:
  skeleton_present: true
iteration_3_fixture_path: cases/falsifier-suite/fixtures/judge-class-collision-config.yaml
canonical_assertion_for_iteration_3: "convergence_score < 0.75 OR verdict == regression_present"
related_spec_references:
  - "§7.1 reviewer composition rules ..."
  - "§11.3 blind calibration disjoint-set ..."
  - "refs/reviewer-spec.md (rotation table + seating algorithm)"

TODO_ITERATION_3:
  - "Promote status field to `active` (byte-exact replacement)."
  - "Add canonical fields: `type`, `fixture`, `expected`, `assertion` per §12.5."
  - "Author the fixture content at `fixtures/judge-class-collision-config.yaml` ..."
  - "Run the reviewer-seating algorithm against the fixture ..."
  - "If the algorithm silently seats the collider, escalate per the falsifier-suite README ..."
```

**Top-level keys (REQUIRED for skeleton):** `id`, `status`, `description`, `expected_behavior` (optional but recommended), `expected_grader_emission` (must include `skeleton_present: true`), `iteration_3_fixture_path`, `canonical_assertion_for_iteration_3`, `related_spec_references` (list of `§<section> ...` strings), `TODO_ITERATION_3` (list of operator steps).

**Adapt for `pr-bot-validation-mixed-buckets.yaml`:**

```yaml
# SKELETON — iteration-3 follow-up authors full fixture and flips status to active.
id: pr-bot-validation-mixed-buckets
status: skeleton-pending-iteration-3-fixture
description: "Tests that the BRV-MG bucket attribution logic correctly classifies a PR with mixed bot signals (1 must-fix from CodeRabbit + 2 nice-to-haves from sourcery-ai + 1 hallucinated alert from Greptile) into the correct merge-gate verdict."
expected_behavior: "BRV-MG MUST tag the CodeRabbit must-fix as 'blocking', the sourcery suggestions as 'advisory', and the Greptile hallucination as 'discarded-hallucination'. Verdict: merge-gate=fail."
expected_grader_emission:
  skeleton_present: true
iteration_3_fixture_path: cases/falsifier-suite/fixtures/mixed-buckets-pr-diff.patch
canonical_assertion_for_iteration_3: "verdict == fail AND blocking_count == 1 AND hallucination_dropped_count == 1"
related_spec_references:
  - "§<X> bucket-attribution rules"
  - "refs/bot-review-sources.yaml (canonical bot class table)"
TODO_ITERATION_3:
  - "Promote status field to `active`."
  - "Add canonical fields: `type`, `fixture`, `expected`, `assertion`."
  - "Author the fixture at `fixtures/mixed-buckets-pr-diff.patch` and a sibling `bot-reviews.json`."
  - "Run `make pr-bot-validate-eval-quick` and confirm verdict == fail."
  - "If the verdict is silently 'pass', escalate per the falsifier-suite README."
```

---

## 6. Ref file shape — `bot-review-sources.yaml`

**Pattern source:** `src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml` (lines 1-40 read directly). It is the only YAML-format ref in the reflect skill; all other refs are `.md`. Its shape:

```yaml
# <skill> <topic name>
# ---------------------------------------------------------------------------
# Mirrors §<X> of the merged requirements spec (single source of truth).
# Consumed PRE-INVOCATION by ... (or AT_WAVE_N by ...)
#
# Schema (top-level keys, all REQUIRED):
#   - <key_1>       <description>
#   - <key_2>       <description>
#   - ...
#
# Units: ...
# ---------------------------------------------------------------------------

<schema_version_key>: "1.0.0"
sync_source: ".dev/<spec-path> §<X>"
sync_method: "make <sync-target>"

<top_level_block_1>:
  <field_a>: <value>
  notes: "<...>"

<top_level_block_2>:
  <entity_1>:
    description: "<...>"
    <field>: <value>
    ...
  <entity_2>:
    ...
```

**Where SKILL.md cites refs:** the reflect skill body uses two citation idioms:
1. Inline parenthetical: `(See refs/<file>.md for ...)` — e.g., SKILL.md:87, :100, :118, :211, :247, :289, :420, :759, :821.
2. Wave-binding table at end of skill: SKILL.md:1391-1397 lists each ref + the wave that consumes it + a one-line "what it provides" column. **The new BRV-MG skill body should adopt this same wave-binding table for `refs/bot-review-sources.yaml`**, e.g., row: `| refs/bot-review-sources.yaml | Wave 1 (bot identification) | Canonical bot class registry: name, signature heuristics, default trust posture |`.

**"Load-on-demand per wave" semantics:** per spec §16 (mentioned in SKILL.md:1088 `"Full adapter table lives in refs/promotion-adapters.md (load-on-demand at Wave 7)"`) — refs are NOT loaded at skill activation; they are loaded only when the wave that needs them executes. This keeps the skill's at-load token budget low (~50 tokens per skill at session start per global CLAUDE.md).

**Adapt for `bot-review-sources.yaml`:**

```yaml
# sc-pr-bot-validate-protocol — bot review sources registry
# ---------------------------------------------------------------------------
# Mirrors §<X> of the merged requirements spec (single source of truth).
# Consumed AT_WAVE_1 (bot identification) by the BRV-MG skill to canonicalise
# each PR review-bot signature into a stable bot_class identifier.
#
# Schema (top-level keys, all REQUIRED):
#   - bot_sources_version       semver string for downstream consumer pinning
#   - sync_source                pointer back to the spec section this mirrors
#   - sync_method                make target that regenerates this file
#   - bots                       list of canonical bot entries
#
# Per-bot schema:
#   - name                       canonical lower-kebab identifier
#   - display_name               human-readable name as it appears in PR UI
#   - github_login               GitHub account login(s) — list (one bot may
#                                post under multiple bot accounts over time)
#   - signature_heuristics       list of regex patterns matched against comment
#                                body or review summary to identify this bot
#   - default_trust_posture      'high' | 'medium' | 'low' — used by bucket
#                                attribution as a prior
#   - default_bucket_mapping     mapping from this bot's native severity labels
#                                to BRV-MG canonical buckets
#                                (blocking | advisory | nit | hallucination)
# ---------------------------------------------------------------------------

bot_sources_version: "1.0.0"
sync_source: ".dev/<spec-path> §<X>"
sync_method: "make sync-bot-sources"

bots:
  - name: augment-code
    display_name: "Augment Code"
    github_login: ["augmentcode-bot", "augment-code-bot"]
    signature_heuristics:
      - "Powered by Augment Code"
      - "augmentcode\\.com"
    default_trust_posture: high
    default_bucket_mapping:
      blocker: blocking
      important: advisory
      info: nit

  - name: coderabbit
    display_name: "CodeRabbit"
    github_login: ["coderabbitai", "coderabbitai[bot]"]
    signature_heuristics:
      - "CodeRabbit"
      - "coderabbit\\.ai"
    default_trust_posture: high
    default_bucket_mapping:
      _potential_issue: blocking
      _refactor_suggestion: advisory
      _nitpick: nit

  - name: sourcery-ai
    display_name: "Sourcery AI"
    github_login: ["sourcery-ai[bot]"]
    signature_heuristics:
      - "Sourcery"
      - "sourcery\\.ai"
    default_trust_posture: medium
    default_bucket_mapping:
      issue: advisory
      suggestion: advisory
      comment: nit

  - name: github-copilot-review
    display_name: "GitHub Copilot Review"
    github_login: ["copilot-pull-request-reviewer[bot]"]
    signature_heuristics:
      - "Copilot Pull Request Reviewer"
      - "github\\.com/features/copilot"
    default_trust_posture: medium
    default_bucket_mapping:
      issue: advisory
      suggestion: nit

  - name: greptile
    display_name: "Greptile"
    github_login: ["greptile-apps[bot]", "greptileai[bot]"]
    signature_heuristics:
      - "Greptile"
      - "greptile\\.com"
    default_trust_posture: medium
    default_bucket_mapping:
      issue: advisory
      observation: nit

  - name: codiumai-pr-agent
    display_name: "Qodo Merge (formerly CodiumAI PR-Agent)"
    github_login: ["CodiumAI-Agent", "qodo-merge-pro[bot]"]
    signature_heuristics:
      - "PR-Agent"
      - "Qodo Merge"
      - "codium\\.ai"
    default_trust_posture: medium
    default_bucket_mapping:
      bug: blocking
      enhancement: advisory
      maintainability: advisory
```

---

## 7. Makefile target gap — does `pr-bot-validate-eval-quick` need adding?

**Yes, it needs adding.** Confirmed by:

```
grep -nE "pr-bot-validate|pr_bot_validate" Makefile
(no output)
```

The Makefile pattern is set by `Makefile:493-505` (reflect-eval + reflect-eval-quick). The new targets MUST follow the same shape — also add to the `.PHONY` line at `Makefile:1`.

**Recipe sketch (mirror of `reflect-eval` / `reflect-eval-quick` at lines 493-505):**

```makefile
# Full pr-bot-validate eval — runs all pilot + falsifier cases.
# Budget: ~2 min on RC branches; CI cadence: every PR touching the BRV-MG skill/command.
# Output: .dev/eval-workspaces/sc-pr-bot-validate/iterations/<timestamp>/
pr-bot-validate-eval:
	@mkdir -p .dev/eval-workspaces/sc-pr-bot-validate/iterations/$(shell date +%Y%m%d-%H%M%S)
	@uv run python .dev/eval-workspaces/sc-pr-bot-validate/grader.py \
		.dev/eval-workspaces/sc-pr-bot-validate/iterations/$(shell date +%Y%m%d-%H%M%S)

# Quick pr-bot-validate eval — runs only the pilot cases.
# Budget: <30s; CI cadence: every PR touching the BRV-MG skill/command.
pr-bot-validate-eval-quick:
	@mkdir -p .dev/eval-workspaces/sc-pr-bot-validate/iterations/$(shell date +%Y%m%d-%H%M%S)-quick
	@uv run python .dev/eval-workspaces/sc-pr-bot-validate/grader.py \
		.dev/eval-workspaces/sc-pr-bot-validate/iterations/$(shell date +%Y%m%d-%H%M%S)-quick
	@echo "Note: pilot-subset filtering is iteration-2 follow-up; this target currently runs the full eval set in a -quick-suffixed iteration dir."
```

**.PHONY update at `Makefile:1`:** prepend `pr-bot-validate-eval pr-bot-validate-eval-quick` to the existing `.PHONY:` list.

**Parameterising `reflect-eval` to run the new workspace is rejected** because the recipe hard-codes `.dev/eval-workspaces/sc-reflect/grader.py` (line 495, 504). Refactoring it to take a SKILL parameter would require touching the existing target's recipe — out of scope for the BRV-MG implementation; copy + rename is cleaner.

---

## 8. Auth + permissions note for `gh api .../statuses/<sha>`

**No special PAT needed.** GitHub's auto-injected `${{ secrets.GITHUB_TOKEN }}` works for `POST /repos/{owner}/{repo}/statuses/{sha}` *provided* the workflow declares `permissions: statuses: write`. This is the default behaviour for GitHub-issued tokens in Actions when the `statuses` permission is explicitly granted.

**Confirmed by:** `pull-sync-framework.yml:11` (`permissions: contents: write`) and `readme-quality-check.yml:12-15` (`permissions: contents: read, pull-requests: write, issues: write`) — both rely on `GITHUB_TOKEN` auto-injection. No workflow today uses a PAT (no `secrets.GH_PAT` or similar referenced).

**Required for BRV-MG workflow:**
```yaml
permissions:
  contents: read           # checkout
  pull-requests: read      # read PR metadata + reviews
  statuses: write          # post commit-status check  <-- LOAD-BEARING
```

`gh` CLI auto-reads `GITHUB_TOKEN` from env; set it via `env: GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` on the step that invokes `gh api`. (Pattern shown in §2 blueprint.)

**Blocker / open question:** `claude` CLI provisioning on the runner is NOT covered by existing workflows. The executor must either (a) add an install step (e.g., `curl -fsSL https://claude.ai/install.sh | sh`) before invocation, or (b) use a pre-built action image. Recommend (a) with a pinned version for reproducibility; document in TDD.

---

## Summary

- New workflow `pr-bot-validate.yml` triggers on `pull_request_review` + `pull_request.synchronize/opened/reopened`, declares `permissions: {contents: read, pull-requests: read, statuses: write}`, runs `ubuntu-latest`, uses `${{ secrets.GITHUB_TOKEN }}` (no PAT). Closest existing pattern: `readme-quality-check.yml` (explicit permissions block + PR trigger). **No existing workflow uses `gh api /statuses` today — this is greenfield**, but the auth pattern is identical to other write-permission workflows.
- Eval-workspace `.dev/eval-workspaces/sc-pr-bot-validate/` mirrors `sc-reflect/` 1:1 (SPEC.md, README.md, aggregate_iteration.py, grader.py, evals/evals.json, cases/falsifier-suite/{README.md, fixtures/, *.yaml}, iterations/, skill-snapshot/).
- **grader.py strategy: COPY + extend** sc-reflect's grader; strip the 10 reflect-specific assertion types, keep the 8 baseline types, add new BRV-MG-specific types. Same pattern reflect used to bootstrap from sc-brainstorm (`SKILL.md:904`).
- Falsifier YAML shape verbatim from `T2-judge-class-collision.yaml`: top-level `id`, `status: skeleton-pending-iteration-3-fixture`, `description`, `expected_grader_emission.skeleton_present: true`, `iteration_3_fixture_path`, `canonical_assertion_for_iteration_3`, `related_spec_references` list, `TODO_ITERATION_3` list.
- Ref-file YAML shape verbatim from `refs/cost-profile.yaml`: top-of-file comment header describing schema + Units, then `<thing>_version`, `sync_source`, `sync_method`, and topic blocks. Skill body cites refs both inline (`(See refs/X)`) and in a wave-binding table at end of SKILL.md (reflect lines 1391-1397).
- **Makefile gap: `pr-bot-validate-eval` + `pr-bot-validate-eval-quick` MUST be added.** No existing target covers it. Recipe sketch provided (mirror of lines 493-505). `.PHONY` line at `Makefile:1` must be updated.
- **Blocker:** `claude` CLI install step for the runner is not in any existing workflow. Executor must add one explicit install step (recommend `curl`-based pinned install) and document in TDD. ANTHROPIC_API_KEY secret will need to be configured in repo settings — flag for the executor to verify before workflow is enabled.

**File paths (all absolute):**
- Research file: `/config/workspace/Coder/.dev/tasks/to-do/TASK-RF-BRV-MG-IMPLEMENT-20260531-184500/research/02-workflow-evalworkspace-refs.md`
- Workflow source dir: `/config/workspace/IronClaude/.github/workflows/`
- Eval-workspace pattern source: `/config/workspace/IronClaude/.dev/eval-workspaces/sc-reflect/`
- Refs pattern source: `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/refs/`
- Makefile: `/config/workspace/IronClaude/Makefile` (target pattern at lines 493-505; `.PHONY` at line 1)
