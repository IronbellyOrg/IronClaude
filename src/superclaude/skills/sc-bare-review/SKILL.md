---
name: sc-bare-review
description: Infrastructure skill that dispatches 2-4 bare (unscaffolded) reviews of a target file in parallel to diverse EXTERNAL models, normalizes each into a compressed-markdown template carrying suspect:true, and returns a contract handing the files to /sc:adversarial --suspect-source. Delegate-only — no slash command. Thin caller over `superclaude swarm run --lens bare-review`.
allowed-tools: Bash, Read
model: sonnet
---

# sc-bare-review — T2 Bare-Reviewer Adjunct (thin caller)

Spec: `.dev/brainstorms/20260528030000-t2-bare-reviewer-adjunct/merged-requirements.md` (v1.3.0-draft). Roadmap: M9 / R-135 / FR-029 / COMP-033 — thin caller over `--lens bare-review`.

## Purpose

Delegate to `superclaude swarm run --lens bare-review` and relay its return contract verbatim. Preflight, parallel dispatch, normalize, merge, and contract emission live in the CLI's `bare_review_v1` recipe — **no orchestration logic here**. `/sc:bare-review` does not exist. Entry point is `Skill sc-bare-review …` from caller pipelines (`/sc:troubleshoot`, `/sc:reflect`, `/sc:auggie-review`, `/sc:code-review`, `/sc:adversarial`). Every output is `suspect: true` by construction; consumers MUST flow them into `/sc:adversarial --suspect-source`.

## Required Input

```text
Skill sc-bare-review
  --target <path>          # REQUIRED — file to review
  --output <dir>           # REQUIRED — output directory
  --reviewers <N>          # 2-4 (default 3)
  --target-line-cap <N>    # truncate target to N lines (default 4000)
  --timeout-sec <N>        # per-reviewer hard timeout (default 180)
  --label <string>         # optional prompt context label
```

## Behavioral Protocol

Issue a single Bash call. The CLI owns preflight, parallel dispatch (IMM-3), timeouts (AC-1.6), partial-success handling (AC-1.7 / IMM-5), atomic writes (IMM-6), and contract emission (FR-036).

```bash
superclaude swarm run --lens bare-review \
  --target "<target>" --output "<output-dir>" --transport openai_compat
```

Forward `--reviewers`, `--target-line-cap`, `--timeout-sec`, `--label` only when the caller supplied them. Resume with `--resume <job_id>` against the same `--output` directory (INV-001). After the command exits, `Read <output-dir>/return-contract.yaml` and relay it as the skill's result — never transform, score, or filter; the CLI is the source of truth.

## Return Contract

CLI emits `return-contract.yaml` (FR-036 / DM-003). Status: `success` when `M == N`; `partial` when `2 ≤ M < N`; `failed` when `M < 2` (IMM-5, success-first). `suspect: true` is always set. `recommended_next_command` carries the literal `/sc:adversarial --suspect-source …` invocation — surface it, never auto-execute (AC-015).

## Failure Modes

Relay CLI stderr verbatim. The CLI STOPs cleanly on missing env (`T2ProxyUrl` / `T2ProxyKey`), out-of-range `--reviewers`, unreadable target, empty target (IMM-4, ≥50 non-whitespace bytes), and missing `curl`/`jq`. Per-reviewer failures (timeout, proxy_error, parse_error) do not abort siblings; a `failed` contract is still written.

## Boundaries

**Will:** forward arguments to `swarm run --lens bare-review`; relay `return-contract.yaml`; preserve the user-facing flag surface.
**Will NOT:** dispatch reviewers; parse model output; score/filter/rank; route to Anthropic; write outside `--output`; embed prompts or recipe logic (those live in `cli/swarm/lenses/bare_review.py` + `cli/swarm/recipes/bare_review_v1.py`).

## Acceptance Pointers

- **AC-1.x / IMM-3/4/5/6 / §11.5** — enforced in `swarm run`; covered by `tests/swarm/test_imm_suite.py`.
- **R-135 / FR-029 / COMP-033** — thin caller; orchestration in CLI.
- **SC-001 / MIG-003** — legacy `scripts/*.sh` retired (T08.07); `tests/swarm/test_bare_review_parity.py` auto-skips post-retirement.

---
*v2.0 — Phase 8 / M9 thin caller. Source of truth: `src/superclaude/`; run `make sync-dev` after edits — never edit the `.claude/` mirror directly.*
