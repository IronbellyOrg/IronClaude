---
needs_human_decision: true
status: RESOLVED
---

# Step 1.29 pipx check decision (OQ-10)

## Question

How should step 1.29 put the branch code under pipx?

## Options

(A) from /tmp, first run `pipx run --spec <worktree path> superclaude --version` with no time limit, which only builds and caches pipx's own temporary environment, then run `pipx run --spec <worktree path> superclaude sweep --help` with a 30 s limit on the help run only (REPORT:1300); the installed superclaude is not changed; that a local path works as --spec is UNVERIFIED.

(B) the coordinator runs `pipx install --force <worktree path>`, runs `superclaude sweep --help` from /tmp, then reinstalls from `git+https://github.com/IronbellyOrg/IronClaude`; this changes the person's installed tool and needs owner approval (D4).

Builder recommendation: (A), because it changes no installed tool. This recommendation does NOT authorize adoption.

OPERATOR DECISION: Run option (A).
Chosen: (A)
Decided by: the owner (the person running this session)
Decision source: the owner's message in this session on 2026-11-12 (a human-origin message sent by accepting the reply I suggested, 'say "go with A"'), answering the question of how to run the step 1.29 pipx check (options A and B put to them): "go with A"
