# How much may the PR review tool do on PR #539?

## Question in one sentence
May the automated PR review tool `/sc:pr-submit` work on PR #539, and if so, when and with how much freedom?

## Why you are being asked
PR #539 holds an open security finding that waits for your ruling. At its highest level, the tool fixes review findings by itself, then pushes, replies and resolves threads. On #539 it could design and push its own fix for that security finding and bypass your ruling. Merging #539 needs a decision on whether the tool helps or a person does everything by hand.

## Background you need
- PR #539 adds the read-only `superclaude sweep` command. It has 1003 files and is open, not a draft, with merge state UNSTABLE (read 2026-11-14).
- The security finding: the sweep's `git status` call can run commands that a repository's git settings define. You rule on it (Q1); then the PR author applies your ruling (work item SW-02).
- Tool levels: level 1 proposes fixes only; level 2 applies fixes on the local machine and stops; level 3 also commits, pushes, replies on review threads and resolves them.
- The tool ignores a review thread only once it is marked resolved; a reply alone is not enough (checked in the tool's rules).
- With `--merge-guard off`, the tool's check that the PR is still open before pushing may not run (its own documents disagree). A push after a mid-cycle merge has happened before (PR #368).

## Your options

### 1. Nothing until the ruling lands and Codex's next review is clean; then the full tool (recommended)
- If you pick this: the PR author pushes by hand until your ruling is applied, the security thread is marked resolved, and the automated Codex reviewer has checked the ruling's push with no new git-settings finding. After that the author runs the tool at level 3 without the draft toggle, under a list of approved actions you write. The tool never merges, stops on any git-settings finding, and checks the PR is open before every push.
- Upside: the risky moment passes under human control; after it, the tool's verification and push checks help on a very large PR.
- Downside: the stop on git-settings findings is a written instruction, not a switch in the tool; hand work until Codex reports back.

### 2. After the ruling, level 2 only: the tool fixes locally and a person pushes
- If you pick this: the tool verifies and applies fixes on the local machine; the PR author reads each one and pushes, replies and resolves by hand.
- Upside: a person sees every change before it leaves the machine.
- Downside: slower, hand pushes lose the tool's checks, and the tool may still post one report comment if the other automated reviewer, Augment, declines the PR as too large.

### 3. Never use the tool on #539
- If you pick this: the PR author handles every finding, failing check, push, reply and resolve by hand until you merge.
- Upside: no automated action on the PR that carries the security finding.
- Downside: much hand work on a 1003-file PR, no automatic check that a finding is real, and no later point to relax the rule.

## What the debate found
- The three advocates split: each kept its own option, and none agreed on how much freedom the tool should have after the ruling.
- All agreed: no tool at all before the ruling (the spec's optional "propose only" level would still draft a fix for the security finding); the thread must be marked resolved, not just replied to; check the PR is open before every push.
- The newest risk is Codex's review of the ruling's own push, because that push changes the same git code.

## Recommendation and confidence
Option 1. Confidence 55 percent.

## If you do not answer
Option 3 applies: no tool on #539 at any level, and the author pushes by hand.

## What this answer does not authorize
A merge; any issue post; your ruling reply on the security thread; any fix of the security finding designed by the tool; or the tool on any other PR.

## How to answer
"Q28: option 1, with `--merge-guard off`" (or "option 1 with the draft toggle", "Q28: option 2", "Q28: option 3").
