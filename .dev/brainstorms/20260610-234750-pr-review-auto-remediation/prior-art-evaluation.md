---
artifact: prior-art-evaluation
topic: "Reuse evaluation: cc-plugins/git + Anthropic official plugins vs V1.0 PR auto-remediation monitor"
created: 2026-06-11
sources:
  - https://github.com/yanmxa/cc-plugins (MIT)
  - https://github.com/anthropics/claude-code/tree/main/plugins (official, dogfooded)
  - https://github.com/anthropics/claude-plugins-official (official marketplace)
  - https://code.claude.com/docs/en/github-actions (claude-code-action@v1)
---

# Prior-Art Evaluation — V1.0 PR Auto-Remediation Monitor

## TL;DR

**Fork nothing. Adopt patterns.** Neither cc-plugins nor the official plugins solve V1.0's
core problem (consume an *external async* Augment-App review → route by severity → auto-remediate
→ reply-to-thread → loop). Every prior-art PR tool either *creates* PRs (thin, rail-less) or
runs its *own local* review (synchronous, in-process). But the official `code-review` plugin
encodes four review-orchestration best practices that V1.0 should bake in, and
`claude-code-action@v1` is the reference host for V2.0.

## Coverage matrix (does prior art cover V1.0's 7 components?)

| V1.0 need | cc-plugins/git | official `commit-commands` | official `code-review` / `pr-review-toolkit` |
|---|---|---|---|
| C1 open PR | ⚠️ cross-fork→upstream model | ⚠️ minimal, no rails | ❌ |
| C2 poll external Augment review | ❌ | ❌ | ❌ (runs its *own* review) |
| C3 severity→troubleshoot router | ❌ | ❌ | ⚠️ has confidence-filter *pattern* |
| C4 reply-to-thread + resolve | ❌ | ❌ | ⚠️ has inline-post *pattern* |
| C5 hook | ❌ | ❌ | ❌ |
| arm in-session Monitor | ❌ | ❌ | ❌ |
| loop-guard | ❌ | ❌ | ❌ |

The 90% that's hard (the async consume-and-remediate loop) has **no prior art** in any of them.

## What each PR-creation front-end teaches

- **cc-plugins `03-create-pr.sh`** — solid idioms (dup-PR detection via `gh pr list --head`,
  `--force-with-lease`, idempotent fork setup) **but** hard-wired to push-origin / PR-to-`$UPSTREAM_REPO`
  with a cross-fork `user:branch` head. That is the *opposite* of this fork's absolute rule
  (same-repo PR to `IronbellyOrg/IronClaude`, never upstream). Adopting it re-introduces the
  PR#558 misfire. No rebase. DCO `-s` (this repo uses `Co-Authored-By`).
- **Official `commit-commands /commit-push-pr`** — *intentionally minimal*: no `--repo` pin, no
  existing-PR check, no rebase, no `--force-with-lease`, no conventional-commit/title-body
  template. Anthropic explicitly "leaves those conventions to the operator or surrounding
  orchestration." **Key lesson:** even Anthropic's own PR command is a thin convenience and
  deliberately omits the safety rails — because the rails are project-specific.

> **Conclusion for C1:** There is no safe generic PR-creation wheel to reuse. The fork-only
> pin + rebase-onto-origin/master + `Co-Authored-By` + dup-detection rails **are** the value of
> `sc:submit-pr`. Build fresh; crib the 3 cc-plugins idioms as reference. This is now confirmed
> by *two* independent prior-art sources, not a preference.

## Best practices to EXTRACT from official `code-review` (bake into V1.0)

1. **Two-wave verify (false-positive filter).** Primary scanners find defects → a **secondary
   wave of independent validators cross-checks each finding before publishing**; only validated
   findings survive. → **V1.0:** before spending a `/sc:troubleshoot --fix` session on an Augment
   finding, run a cheap *grounding/verification* gate (does it reproduce / ground in real code?).
   Don't auto-remediate an unverified external finding. (Reinforces the repo's own
   `sc-troubleshoot` adversarial fix-debate and `sc-auggie-review` grounding pass.)
2. **Certainty over volume.** Act only on concrete, reproducible problems (compile failures,
   definite logic flaws); ignore style/linter-detectable/hypothetical. → **V1.0:** route on
   *severity × confidence*, not severity alone. The reused severity-rubric already drops a tier
   on low confidence — keep that; additionally suppress remediation on subjective Augment nits.
3. **Posting hygiene.** Inline comment on the *relevant source line*, include a **ready-to-apply
   patch (GitHub suggestion block)** for trivial fixes, single summary thread when clean,
   **never duplicate annotations.** → **V1.0 FR-6.1 + NFR-1:** post each fix reply as a GitHub
   *suggestion* where trivial; track replied comment IDs to guarantee idempotency.
4. **Parallel fan-out + atomic batching.** 4–5 specialized reviewers run simultaneously;
   "do all of the above in a single message." → **V1.0:** when multiple Augment findings exist,
   fan out verification + troubleshoot diagnosis in parallel; batch independent `gh`/Read calls.

Plus from `pr-review-toolkit/comment-analyzer`: a **4-tier classification + 5-section structured
report** (overview / critical-with-locations-and-fixes / enhancements / deletions / positive).
→ Template for V1.0's per-run report and reply structure.

## What NOT to adopt

- The official review plugins **run their own review** (5 parallel Sonnet agents in-process).
  V1.0's differentiator is consuming the **external Augment App** review. Running a second local
  reviewer is V1.0's *optional* "Both" mode (deferred), not the core.
- v5 `.claude-plugin/plugin.json` packaging — this repo is v4.2 `src/superclaude/` SoT +
  `make sync-dev`. Note for eventual v5.0 migration; do not restructure now.

## Pointer for V2.0 (headless host)

The official `code-review` plugin is designed to run **in CI** via
`anthropics/claude-code-action@v1` on `pull_request: [opened, synchronize]`, installing the
plugin through `plugin_marketplaces` + `plugins` and invoking a skill from the `prompt` input.
**That is the exact reference architecture for V2.0's headless `claude -p` / GitHub-Actions
host** (mention-triggered remediation). The V2.0 brainstorm should start from
`claude-code-action@v1` rather than designing a bespoke daemon.
