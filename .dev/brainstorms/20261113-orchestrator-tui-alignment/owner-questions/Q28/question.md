# Q28: What may `/sc:pr-submit` do on PR #539?

## The question, verbatim from the spec row

Source: `merged-requirements.md` section 3, row Q28 (line 555).

> What may `/sc:pr-submit` do on PR #539? (new, R25-INV-005; also carries the #539 draft toggle of R25-INV-014)

## The spec's recommended answer (verbatim)

> Nothing before SW-02 lands the ruling; after it, `--monitor 3` once the Codex thread is closed by your reply, with `--merge-guard off` (no draft toggle on a large, long-open PR). `--monitor 1` (propose only) before then only if the #539 GRANT row says so explicitly

## Default if unanswered (verbatim)

> No `/sc:pr-submit` on #539 at any level; the #539 author pushes by hand

## What it gates (in words)

- SW-05, "refresh PR #539's merge reference and merge it": its criterion (6) and the #539 grant row, the ledger row that lists every write the tool may make on #539 (`merged-requirements.md:194`, `:1050`).
- SW-02 (apply the owner's INV-008 ruling in #539; INV-008 is the finding that the sweep's `git status` can run commands defined in a repository's git configuration) and SW-03 (fix the Augment review thread at `probes.py:1052`): their pushes stay manual either way (`merged-requirements.md:191`, `:192`).
- Wave: W1 (the second wave); asked when the item is next (`merged-requirements.md:523`).

## Facts the question depends on

1. `/sc:pr-submit`'s `--monitor {0,1,2,3}` is a ceiling on one state machine (`~/.claude/skills/sc-pr-submit-protocol/SKILL.md:36`). Level 1: verifies findings and sends verified ones to `/sc:troubleshoot` for diagnosis, then "PROPOSE 'fix these? y/n' and apply NO edits" (`:306`). Level 2: applies and validates edits in the working tree, then halts "with NO commit, NO push, NO reply" (`:307`). Level 3: commits one fix commit per cycle, pushes, replies on and resolves the finding threads, and may re-request a silent Augment review once with an "augment review" comment (`:70`, `:238`, `:308`).
2. `--merge-guard {draft,off}`, default `draft`: at level 3 the tool turns the PR into a draft during a fix cycle and back to ready after the push; `off` leaves the PR untouched (`SKILL.md:241`).
3. The skill must run in a top-level session as an attended in-session poll loop (`SKILL.md:42-48`); spec rule: only an owner-designated top-level PR session runs it, never a worker or the coordinator (`merged-requirements.md:975`, rule 2).
4. Probe finding R25-INV-005 (`adversarial/adversarial/invariant-probe.md:13`): at level 3 the tool takes actionable review comments, including Codex comments with their P-badge as severity, routes High and Critical to `sc:troubleshoot --depth deep --fix`, applies the edits itself, commits, pushes, replies and resolves. The Codex security thread on INV-008 at `probes.py:1211` is unresolved, so the tool could design and push its own INV-008 fix and resolve the thread, bypassing the owner's ruling (Q1). No switch to exclude one thread exists in the skill (`refactor-plan.md:118`).
5. Spec rules: no tool designs or pushes an INV-008 fix (`merged-requirements.md:191`); "a new finding that needs an owner ruling stops the run before any fix, reply or resolve" (`:194`, SW-05 (6)). The skill has no built-in way to recognise a finding that "needs an owner ruling"; that stop depends on the session running it (PLAN INFERENCE by this worker from `SKILL.md:302-308`).
6. Live state, read 2026-11-14 (`gh pr view 539 --repo IronbellyOrg/IronClaude`): OPEN, not draft, head `873599d59`, merge state UNSTABLE, last updated 2026-11-13T00:45Z. PR #539 has 1003 files.
7. Owner memory `pr-submit-check-pr-open-before-push.md`: the tool's pre-push guard does not check that the PR is still open, and a Codex security review can post a finding minutes after its code review reported clean.
8. Authority limits: Q28 does not authorize an INV-008 fix by the tool; a `pr-submit` grant on one PR does not authorize a merge, an issue write, the INV-008 ruling reply, or the tool on any other PR (`merged-requirements.md:577`, `:582`).
9. Project rule: PRs are opened with `/sc:pr-submit --monitor 3` (project `CLAUDE.md`, "The mandatory way to open a PR"); #539 is already open, so the rule's opening step does not apply.
