# Refactoring Plan (base = V2 security)

## Overview

- Base: Variant 2 (sonnet:security). Incorporate: V1 architect (control-flow, inventory,
  parent-resolution, ledger discipline), V3 devops (systemd, rate-limit, audit schema, deploy).
- Changes planned: 8 incorporations + 4 HIGH invariant resolutions + 6 MEDIUM resolutions.
- Overall risk: Medium (security-critical; all HIGH items closed before merge).

## Planned incorporations

| # | Source | Into base | Approach | Risk |
|---|--------|-----------|----------|------|
| 1 | V1 §Component Inventory (A1–A15) | new §Component Inventory | append; relabel under `cli/remediate/` + split dispatcher/runner | Low |
| 2 | V1 §Control Flow | new §Control Flow | append the scan→claim→authz→parent→parse→execute→act→commit loop | Low |
| 3 | V1 parent resolution (`in_reply_to_id`, parentless-reject) | §Mention Detection | insert | Low |
| 4 | V3 systemd unit + hardening | §Process Lifecycle | append (dispatcher only) | Low |
| 5 | V3 ETag/304 + 403 backoff + rate headers | §Rate-Limit Safety | append | Low |
| 6 | V3 audit-ledger JSONL event schema | §Audit Ledger | append; merge with V2 forensic fields | Low |
| 7 | V3 deploy/rollback runbook | §Deploy & Rollback | append | Low |
| 8 | V2 effective-level-MIN | §Autonomy Model | keep but **reformulate** per INV-006 | Medium |

## HIGH invariant resolutions (gate-clearing)

- **INV-001 (credential delivery).** Adopt V2's "git actions host-side" fully and resolve the
  contradiction: the **runner never pushes**. The runner produces a *patch bundle* (or commits
  on a sandbox branch) written to a host-shared artifact path; the **dispatcher** performs the
  `git push` host-side using a **short-lived, repo+branch-scoped push token minted per trigger**
  (GitHub App installation token or fine-grained PAT), never present in the runner env. SC-7 +
  SC-4 hold; the "no GH_TOKEN in runner" invariant becomes true and consistent.
- **INV-002 + INV-011 (round commit order / stale-claim).** Replace single-commit-point with a
  **two-phase ledger record**: `intent{round=N, action, base_sha}` written BEFORE the act;
  `outcome{round=N, pushed_sha|none, result}` written AFTER. Scanner rule: `intent` without
  matching `outcome` = **RESUME** (re-verify GitHub side-effect state by querying the PR head/
  comments), never silent re-execute and never silent re-count. This satisfies SC-5 (bounded)
  AND "rounds do work" AND auto-recovers routine runner crashes without a human.
- **INV-003 (parent-body TOCTOU).** Re-fetch the parent comment immediately before any push;
  compare SHA-256 against the body used at plan time; on mismatch **HALT and require a fresh
  mention** (carried from V2 line 42). Log parent `id`, `updated_at`, body SHA-256.
- **INV-007 (propose-only hard guarantee).** Make SC-3 a **sandbox invariant**, not host
  discipline: the propose-level runner clones via a **read-only / credential-less remote**
  (anonymous HTTPS or a read-scoped token) so NO push-capable credential is reachable; a
  prompt-injected `git push` fails for lack of credential, not for lack of `--fix`.

## MEDIUM resolutions (recorded in merged spec)

- **INV-004 / INV-016 (residual mention text).** Replace hard-reject with **strip-known-flags →
  ignore a bounded trailing free-text remainder (≤N chars, logged)**; only reject if the
  remainder contains another `@`-mention or flag-like token. Tokenizer requires flags as
  whitespace-delimited tokens (no prose extraction). And: **always post a one-line ack/why reply
  on reject** (not silent) so the bot never looks dead — using a neutral message that is not a
  permission oracle (e.g. "couldn't parse a remediation request; reply `@bot fix`").
- **INV-005 (SHA correlation).** Round attribution uses **exact-SHA-match per round**, not
  "or descendant". Any non-bot head (human/force push) → drop to propose-only.
- **INV-006 (effective level).** Reformulate: `autonomy_cap = min over the autonomy lattice of
  {parsed_flag, authz→lattice-projection, validation→{pass:as-parsed, fail:propose}}`; THEN
  apply **off-lattice HALT short-circuits** (`needs_human_decision`, `loop_budget==0`). HALT ≠
  a lattice point — it stops, posting at most a proposal. Explicitly prevents the
  `needs_human_decision`-shipped-as-push failure (memory `feedback_human_decision_items_must_halt`).
- **INV-009 / INV-018 (round-key granularity).** Bound the count that matters: a **per-PR push
  budget** (default 2, cap 5) in addition to a per-thread round counter. Thread proliferation
  cannot exceed the per-PR push budget. Per-PR `flock` serializes tree mutations.
- **INV-010 (resolveReviewThread mapping).** Match on **`databaseId`** (not GraphQL node `id`);
  paginate `reviewThreads` + each thread's `comments` until the parent comment id is found;
  if not found after full pagination → **do not resolve**, post the reply only, log
  `thread_unmatched`.
- **INV-012 (24/7 PAT).** Acknowledge honestly: the dispatcher holds a long-lived GitHub
  credential. Minimize it — the long-lived credential is **read + comment scope only**; the
  **write/push token is short-lived and minted per trigger** (INV-001), so the 24/7 exposure is
  not repo-write.
- **INV-015 (egress scope).** Network allowlist = `:4000/cli` proxy + **`api.github.com` and the
  single repo's git endpoint only** (not `github.com` broadly). Blocks gist/other-repo exfil.
- **INV-017 (uv offline gate).** Sandbox image **pre-bakes a fully-synced venv**; pre-push gate
  runs `uv` with `--offline`/`--no-sync`. PyPI stays off the allowlist.

## Changes NOT made (base superior / rejected)

- V1 one-shot-for-everything and V3 daemon-runs-agent-in-process both rejected in favor of V2's
  split (X-001/X-003). V3's in-memory round state rejected for V1's ledger-as-SoT (X-004).
- V1 commit-after-act rejected for two-phase record (INV-002).
