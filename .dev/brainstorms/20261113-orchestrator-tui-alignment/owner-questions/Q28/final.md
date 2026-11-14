# Q28 final: what may `/sc:pr-submit` do on PR #539?

Terms used here: `/sc:pr-submit` is the project's PR review tool; its `--monitor` level sets how far it may act (level 1 proposes fixes only, level 2 applies fixes locally and stops, level 3 also commits, pushes, replies on review threads and resolves them). PR #539 is the open pull request that adds the read-only `superclaude sweep` command. INV-008 is the finding that the sweep's `git status` can run commands defined in a repository's git configuration; the owner rules on it (question Q1), and work item SW-02 applies that ruling in #539. The Codex security thread is the review thread on `probes.py:1211` that raised INV-008. A grant row is the ledger line in which the owner lists exactly which outward actions are approved.

## Debate result

Winner: proposal A (no tool before the ruling, then level 3 with `--merge-guard off`), amended with three gates, after a split debate. Confidence 55 percent.

Advocate agreement: split. Each advocate kept its own variant as its overall pick (A, B and C), and the central point, which tool level after the ruling (diff point C-001), stayed unresolved. The other 10 points converged (91 percent). Scoring put C and A inside the 5 percent tie band (0.834 against 0.797); the tiebreaker on debate points chose A (`adversarial/base-selection.md`).

Unanimous findings that change the spec's recommended answer:
- No tool before the ruling. Level 1 still sends the verified Codex INV-008 finding to `sc:troubleshoot` for diagnosis and proposes a fix (`~/.claude/skills/sc-pr-submit-protocol/SKILL.md:306`), which conflicts with "no tool designs or pushes an INV-008 fix" (`merged-requirements.md:191`). The spec's optional pre-ruling level 1 should go.
- The gate must be "the Codex thread is resolved", not "closed by your reply". The tool excludes resolved Codex threads and keeps unresolved ones visible (`~/.claude/skills/sc-pr-submit-protocol/refs/detection-contract.md:132-136`, verified).
- A check that the PR is still open before each push. With `--merge-guard off`, the skill text loads the open-PR check only for `--merge-guard draft` (`SKILL.md:309`), while its reference file says the check always runs (`refs/merge-guard.md:94-97`). The two disagree, and a push after a mid-cycle merge has happened before (owner memory `pr-submit-check-pr-open-before-push.md`, PR #368).

Proposal A, strengths and weaknesses: it is the spec's answer and the project's standard loop, and it keeps the tool's push checks (head binding, one-commit parent check, named-path staging, `SKILL.md:299`, `:308`) and verification. Weakness: at level 3 the stop on a finding that needs an owner ruling rests on the session's judgment, and SW-02 changes exactly the git-status code, while the tool re-triggers Codex after each push.

Proposal B, strengths and weaknesses: level 2 stops before any commit, push, reply or resolve by design (`SKILL.md:307`), so a person sees every change on a security-sensitive PR. Weaknesses: hand pushes lose the tool's push checks; the tool cannot re-request reviews; and level 2 can still post one PR comment, the `/sc:auggie-review` report when Augment declines a PR as too large (`refs/auggie-fallback.md:35`, verified), which the proposal did not list.

Proposal C, strengths and weaknesses: no tool ever acts on the PR that carries the INV-008 thread, so both spec rules hold by construction. Weaknesses: every finding and red check on a 1003-file PR, merge state UNSTABLE on 2026-11-14, is handled by hand without verification, and it has no point at which to relax.

## Final recommendation

No `/sc:pr-submit` on PR #539 at any level until three things hold: SW-02 has landed your ruling; the Codex security thread is marked resolved; and Codex's review of the SW-02 push has come back with no new finding about git configuration. After that, the #539 author runs it at level 3 with `--merge-guard off`, under a grant row that lists every write the tool makes (including the possible `/sc:auggie-review` report comment), never merges, stops before any edit on a git-configuration finding, and checks that the PR is open and its head unchanged before every push. Confidence 55 percent.

Strongest reason: the real risk is the first Codex review after SW-02 changes the git-status code; waiting for it to come back clean removes that risk, after which the tool's checks are safer than hand pushes.

Equals the spec's recommended answer: partly. Same levels (nothing before, level 3 after), but it drops the pre-ruling level 1 option, requires "resolved" instead of "replied", adds the wait for Codex's review of the SW-02 push, and writes the stop rule and open-PR check into the grant row.

## What would change the answer

If Codex's review of the SW-02 push raises a new git-configuration finding, or if the owner wants a person to see every push on this PR, proposal B (level 2) or C (never) becomes the better answer.

## Criticality rating

- Security or trust boundary: high
- Reversibility: costly
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: yes
- Cost if the answer is wrong: medium
- Does it grant authority or accept a risk in writing: yes
- Debate: split
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The answer is a written grant that lets an automated tool push, reply and resolve on the PR that carries an open security ruling, and the advocates split on how much autonomy is safe. How much risk to accept on that PR is the owner's call.

## Debate record

- Folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q28/adversarial/` (merged answer: `../merged-output.md`)
- fallback_mode: false (three advocate agents spawned in parallel; diff analysis, scoring, plan and merge done by this worker in-context, recorded in `return-contract.yaml`)
