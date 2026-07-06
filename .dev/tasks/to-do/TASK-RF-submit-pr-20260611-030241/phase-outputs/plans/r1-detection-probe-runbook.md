# R1 Augment Detection Probe — Operator Runbook

**Generated:** 2026-06-11 11:19
**Step:** 2.0 (`needs_human_decision` HALT — operator item)
**Status:** ⏸️ PENDING — CANNOT run autonomously. See HALT note at bottom.
**Spec:** §7 (merged-spec.md lines 473–500) + R06 §1.1
**Contract file:** `src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md` (ships `locked: false`)

## What this probe does

Replaces every `<PROBE-LOCKED>` / `<placeholder>` constant in `detection-contract.md`
with **observed empirical data** from a real Augment Code GitHub App review on a live PR
of `IronbellyOrg/IronClaude`, then flips `locked: false → true`. The build DAG (spec §3
step 0) mechanically BLOCKS arming (T-210) until `locked == true`. The bot login and
emission shape are UNKNOWN and **must NOT be hard-guessed** (§7 consequence 1).

## Preconditions (operator must confirm first)

1. The **Augment Code GitHub App** is installed on `IronbellyOrg/IronClaude`
   (verify: `gh api repos/IronbellyOrg/IronClaude/installation`).
2. A real PR exists that the Augment app has **already reviewed** (an Augment-authored
   review/comment is visible on the PR). Substitute its number for `<N>` and its head
   SHA for `<headSHA>` below.

## The 5 captures (single-line, absolute-path, `--repo`-pinned)

**Capture 1 — bot login + author_association + app slug** (fills `augment_bot_login`, `augment_author_association`, `augment_app_slug`):

`gh pr view <N> --repo IronbellyOrg/IronClaude --json reviews -q '.reviews[] | {author: .author.login, association: .authorAssociation, state: .state}'`

`gh api repos/IronbellyOrg/IronClaude/pulls/<N>/reviews -q '.[] | {id, user: .user.login, type: .user.type, association: .author_association, state}'`

**Capture 2 — emission_shape + findings_locus** (which gh surface carries findings; observe which is non-empty for the Augment author):

`gh api repos/IronbellyOrg/IronClaude/pulls/<N>/reviews`

`gh api repos/IronbellyOrg/IronClaude/pulls/<N>/comments`

`gh api repos/IronbellyOrg/IronClaude/issues/<N>/comments`

`gh api repos/IronbellyOrg/IronClaude/commits/<headSHA>/check-runs`

**Capture 3 — severity_field_path** (does Augment self-report a severity, and where? JSONPath or `null` if prose-only; a hint, never authoritative — re-graded via the reused rubric, FR-3.1):

`gh api repos/IronbellyOrg/IronClaude/pulls/<N>/reviews -q '.[0]'`

**Capture 4 — review_completeness_signal** (the marker that the review is finished not mid-stream; `state == "COMMENTED"` or a summary marker in the body — so the poller never classifies a partial emission as "clean"):

`gh pr view <N> --repo IronbellyOrg/IronClaude --json reviews -q '.reviews[] | {state: .state, hasBody: (.body | length > 0)}'`

**Capture 5 — persist probe_evidence** (write the raw captured JSON to an absolute path and record it in the contract as provenance for the lock):

`gh api repos/IronbellyOrg/IronClaude/pulls/<N>/reviews > /config/workspace/IronClaude/.dev/pr-monitor/probe/augment-review-<N>.json`

## After capture — lock the contract

1. Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md`:
   set each YAML field to its observed value, set `probe_evidence:` to the absolute path
   from Capture 5, and flip `locked: false` → `locked: true`.
2. Run `make sync-dev` then `make verify-sync` (mirror to `.claude/`, src/-only edit).
3. Regenerate the synthetic fixtures from the real captured shape (§18.4 parity contract).
4. Verify: `grep -q '^locked: true' src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md`.

## ⏸️ HALT — `needs_human_decision: PENDING`

This probe **cannot be run autonomously by this task**:

- The Augment GitHub App installation on `IronbellyOrg/IronClaude` is **unconfirmed**.
- There is **ZERO captured Augment GitHub-App review JSON** anywhere in `.dev/`
  (`find .dev -iname '*augment*'` → empty; only brainstorm/spec prose mentions it). The
  in-repo `/sc:auggie-review` is a *different* thing (in-session Augment retrieval, not
  the GitHub App that posts a review *on* the PR).
- Per `feedback_human_decision_items_must_halt` + §7 "NOT hard-guessed": this item writes
  PENDING and HALTs the **lock path only**. It NEVER auto-locks the contract and NEVER
  hard-guesses `augment_bot_login`.

`detection-contract.md` therefore ships with `locked: false`. Arming is mechanically
blocked by **T-210** until an operator runs the 5 captures above and flips `locked: true`
with a real `probe_evidence` path. **All other build steps proceed now on synthetic
fixtures (§18.4)** — the FSM, severity router, loop-guard, run-log, recovery, reply, and
the entire test suite are internal-pure and need no network. This HALT does NOT block the
remaining (internal-pure) phases.
