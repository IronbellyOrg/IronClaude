# Round 2 findings: #803 (C22) Per-repo tier defaults, validation and one recorded fallback

Checked 2026-11-24 against master f2894fc44 (worktree Realign). Parent: #716 (coordinator). Round 1: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/8/803/findings.md`. Static run: `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/7/analyze` (finding 3: no tier setting in the coordinator-side package). Plan paths are under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (SPEC = `spec/SPEC.md`, DEC = `DECISIONS.md`).

## Alignment with architectural decisions

- **R38, clause (C)** (owner 2026-11-21, `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`): the owner lists "tier keys" among the Clay elements that "are not adopted" (with on-demand orchestrators, registry, `repos.yaml`, in-flight cap, wake file, living report, merge gate, flags). The source of C22 is exactly that element: issue #655 body (line 10, "agents the orchestrator starts run on ccsession tiers named in `repos.yaml` ... per-repo override: `plan_tier`..."). **In conflict.** Round 1 did not cite R38 and called the item "keep open with changes"; that missed that the owner already rejected the item's core mechanism. The comparison file says the same (`.dev/releases/backlog/issue-watcher-zero-setup/design-comparison-655.md:3`: recommendations that adopt Clay's parts "are therefore void").
- **SPEC.md:455** (row "C6 tier settings: ADOPT+CHANGE ... requests until U28; `plan_depth`") and **D15 VERDICT:78**: the plan adopted tier keys as requests recorded in `launch.effective`. R38 supersedes the "Clay strengths adopted" rows of SPEC, so this row is void. **In conflict** (superseded, not live).
- **OD-1, FR-59** (`SPEC.md:97`, `:280`): `plan_depth`, no `plan_tier`. The item correctly omits plan tier. **Aligned** (and the only part of that row not tied to Clay's keys).
- **FR-12** (`SPEC.md:202`): a key gets loader support in the PR that first reads it; unknown-key rejection stays. Master rejects unknown keys (`src/superclaude/cli/issue_watch/cycle.py:59-72`, `:223-226`). **Aligned** as a build rule, relevant only if the owner reopens tier keys.
- **SEC-14** (`SPEC.md:303`): rulings are given in the owner's chat. The item says "defaults named by the owner" but the owner has not named them and "ruling 12" is not in the plan files (grep of `ruling 12` finds nothing): UNVERIFIED. **In conflict** with the item's own done-when premise.
- **Watcher design as merged** (PR #707; `src/superclaude/cli/issue_watch/launch.py:26-29`: the Orca agent id `claude` "is deliberately not configurable"): a launch-time model choice was kept out on purpose. **Partly aligned**: a per-repo tier key would reverse that stance.
- **WORKER-CONTRACT.md**: no rule names a tier (grep `tier` finds nothing). **None conflicts; none governs.** WC-8 and WC-13 keep Orca fan-out out of workers; worker tier would be applied only at the coordinator's own `worker-start`.
- **Architecture finding** (analyze finding 3): no tier key anywhere in `src/superclaude/cli/issue_pipeline/`.

## Complementary issues

- #788 C7 (worker start): where a worker tier would be applied (`worker-start`). Interface: C22 would hand C7 a tier request; C7's done-when has no tier. If tiers are ever wanted, they land with C7, not as a separate item.
- #782 C1 and #785 C4: no coordinator skill exists to read a config until they land.
- #770 (watcher hands each claim to the coordinator): same launch path and the Coder launch prompt that starts the coordinator (outside this repo).
- #517 (proxy fails on a tier whose first model rejects the default effort) and #489 (tier 2b rename in panels): tier names and refusals change under the config; a refused tier can be exactly the #517 failure. Not blockers.
- #716 backlog review (2026-11-24) asks to reconcile "C22's tier keys" before building.

## Closest overlap

**#788 C7, Worker start.** Shared: the point where a worker's model tier would be set. About 5 percent of C22's done-when (C7 has no tier or fallback line; its done-when is Task, Dispatch in `ready`, issue attached, Dispatch id stored). Next two: **#770** (about 5 percent: touches the same launch path) and **#517** (about 5 percent: the refused-tier failure C22's escalation line would handle). No open issue duplicates C22; the ccsession mechanisms it needs are already merged (below).

## Standalone or merge

**Stand alone is not the right question; the item should close.** Against #788: owner same, acceptance test differs (fake `ccsession --help` fallback test versus a worker-start fixture), files differ (config loader and ccsession probe versus coordinator skill), build phase differs (phase 3 versus phase 2), risk if merged: pulling an owner-rejected mechanism into the worker-start item that is a core phase-2 item. Merging is right only for the one part the owner might still want, a worker tier request at start, and then it belongs inside #788 after a new owner decision recorded in chat. As filed, C22 rests on a mechanism R38 (C) rejects, so it needs an owner reversal before any build; without one it should close.

## Closed issues and merged PRs checked

- #655 (closed as not planned): source of the tier keys; its closure and R38 reject them.
- #729 (merged): records R38 and the comparison that voids Clay's tier keys.
- #310 (merged, per-user start tier and tier list via `CCSESSION_ACCESS`): already validates a tier against an allowed list (`src/superclaude/skills/ccsession-tag/models.py:630-641`, `unavailable()`), so "validate against the installed ccsession" exists.
- #253 and #481 (merged; closed issue #392): ccsession fails over between models inside a tier and retries server errors; the "fall once to the next tier" step is not delivered (UNVERIFIED beyond `models.py` and the PR bodies).
- #318 and #518 (merged; closed #488): tier layout and names (2b, letters) that the item must not hard-code.
- #509 (merged): issue workers pinned to tiers by agent frontmatter, a separate mechanism.
- #546 (closed): model-policy hook after an Opus misuse incident; about enforcing the requested model, not per-repo defaults.
- #707 (merged watcher): no tier key; agent id fixed.

## Updated recommendation

**Close** (superseded by R38 clause C), unless the owner records in chat that per-repo tier requests are wanted; in that case **keep open with changes**: requests recorded as `launch.effective`, no hard-coded tier names, apply at #788, drop "defaults named by the owner", split the gateway-refusal escalation into the escalation-table work. Priority **P3**, complexity **medium**, size **M** (unchanged if kept). Changed from round 1: round 1 recommended "keep open with changes" without R38; the new evidence is the explicit "tier keys ... not adopted" in R38 (C) and the voided SPEC row. The close is a recommendation for the owner; nothing was changed on GitHub.

## Scan record

Read in full: open-issues.tsv (134 lines), closed-issues.tsv (157), merged-prs.tsv (508). Search terms: tier, ccsession, model, effort, launch, worker-start, fallback, failover, config, repos.yaml, Jev router, policy hook. Opened (body read with `gh`): open #716, #717, #788, #517, #489, #770, #818, #755, #352, #765, #782, #786, #761, #774; closed or merged #655, #488, #518, #253, #318, #481, #546, #509, #310, #707, #729. Plan and master files: requirements.md:64, design-comparison-655.md:3, SPEC.md 97, 202, 280, 303, 455, 710, D15 VERDICT:78, `cycle.py:59-72`, `launch.py:24-29`, `models.py:630-641`. UNVERIFIED: ruling 12; how the Coder image would read a coordinator tier; whether ccsession already moves a refused `--tier` to the next one.
