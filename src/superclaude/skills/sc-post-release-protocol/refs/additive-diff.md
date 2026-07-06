# Additive-Diff Procedure

How the **additive** run mode works — the incremental path taken when a prior `post-release-manifest.json` exists. The goal is simple and worth protecting: **touch only what changed since the last release.** Rewriting unchanged docs and re-running unchanged installs wastes effort, churns diffs, and invites regressions. The manifest is what makes "only the delta" possible.

## When this path runs

Mode detection (in SKILL.md) found a prior manifest. Read it. It tells you the last release's `version`/`tag`, the `install_surface_class`, and — per workstream — the files touched/created, the feature inventory, and the coverage checklist. That prior state is your baseline.

## Step 1 — Establish the delta

Compute what changed between the previous release and this one from two sources:

1. **Code diff:** `git diff <prev_tag>..<this_tag>` (name-only first to scope, then per-file where a workstream needs detail). This is the ground truth for "what actually changed."
2. **Release intent:** the new version's PRD/TDD/spec under the release directory, plus the `<version>` section of `CHANGELOG.md`. This tells you *why* it changed and which changes are user- vs. sysop- vs. internally-facing.

Cross the two: the code diff catches changes the PRD forgot to mention; the PRD catches intent the diff can't express. Build a **delta feature list** — new capabilities, changed capabilities, removed capabilities — each tagged with the audience(s) it touches (user / sysop / implementer / installer).

## Step 2 — Map the delta onto workstreams

For each delta item, decide which workstreams it touches, using the manifest's coverage checklist to find the *existing* artifacts that now need attention:

| Delta item type | Workstreams to touch |
|---|---|
| New user-facing capability | A (document it), D (test guide), maybe C (if install/config changed) |
| Changed user-facing behavior/flag | A (update), D (update guide) |
| Removed capability | A/D (remove or mark deprecated — don't leave dangling docs/guides) |
| New/changed sysop capability | B and/or E |
| Implementation/architecture change | B (update the affected ADR/runbook/reference) |
| Install/deploy/packaging change | C (update scripts + **re-run e2e** for the changed path) |
| No external-surface effect | none — record as "internal only" so the next run knows it was considered |

Anything in the code diff that maps to **no** workstream should be explicitly logged as "internal-only, no surface impact" — that record is what stops a future run from re-investigating the same change.

## Step 3 — Incremental update (not rewrite)

For each touched artifact, make the **surgical** change the delta requires. Do not regenerate a whole doc because one flag changed. The prior manifest's per-workstream file lists tell you exactly which files the last release wrote, so you can target edits instead of re-scanning the entire surface. Still verify every edited claim against current code — surgical does not mean unverified.

For **created** artifacts (a new capability with no existing doc/guide), follow the ground-up create path for just that item.

## Step 4 — Workstream C in additive mode

Only re-run the e2e install if the install/deploy/packaging surface actually changed in `<prev_tag>..<this_tag>` (or if the prior manifest recorded C as red/incomplete). If nothing install-related changed, you may carry forward the prior green result **but must say so explicitly** in the report ("install surface unchanged since `<prev_tag>`; prior green transcript carried forward, not re-run"). Never imply a fresh run happened when it didn't — that's the same honesty rule as everywhere else. If the version number changed, at minimum re-verify the entry point reports `<version>`.

## Step 5 — Reconcile the manifest

Produce the new `post-release-manifest.json` for `<version>` by evolving the prior one:

- Carry forward unchanged entries (so the manifest stays a complete picture of the surface, not just this release's delta).
- Update entries for artifacts you touched.
- Add entries for artifacts you created.
- Mark removed capabilities so their now-deleted docs/guides aren't flagged as gaps next time.
- Set `previous_version`/`previous_tag` to the baseline you diffed against, `run_mode: "additive"`, and refresh `generated_at`.

The report still summarizes all five workstreams, but each section leads with the delta ("since `<prev_tag>`: 2 new user features, 1 changed flag, install unchanged") so a reader sees at a glance what this release moved.

## Guard against silent drift

Two failure modes to watch:

- **Missed delta** — a code change that had surface impact but wasn't mapped to a workstream. Mitigation: every diff entry must be explicitly categorized (touched-a-workstream **or** internal-only). An uncategorized diff entry is a bug in the run.
- **Stale carry-forward** — an unchanged-looking doc that's actually wrong because a *dependency* changed. Mitigation: when a delta item changes a shared surface (a flag, a default, a path), grep the carried-forward artifacts for references to it before trusting them.
