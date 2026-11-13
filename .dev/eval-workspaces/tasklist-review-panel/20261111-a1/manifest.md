# Evaluation manifest

- EVAL: .dev/eval-workspaces/tasklist-review-panel/20261111-a1
- UTC date: 2026-11-11
- Worktree branch: ironbelly/eval-tasklist-review-panel (local, never pushed)
- git fetch origin done; HEAD sha: ec259f1b718ccdb9f08bba0237bfa47b2b7601a2
- origin/master sha: ec259f1b718ccdb9f08bba0237bfa47b2b7601a2
- Precondition 1 (coordinator reading): HEAD == origin/master: YES
- superclaude review --help: works; T2bModel01=gpt-6.1-terra; @live7 resolves 7 reviewers (run-id probe)
- Reviewer sandbox: /tmp/evalsb/repo = git archive of HEAD without .dev/tasks/done, .dev/eval-workspaces, .dev/research (so reviewers cannot read implement history or ground truth). Own throwaway git repo for the snapshot only.
- Dispatch method (Stage 0, probe/probe.json): Bash `claude -p --model <raw gateway model id>`; observed model = assistant message.model in JSON output. Tier aliases serve only the first model of a tier, so they are NOT used.

## Ground-truth hashes (sha256)
- designSpec-20261107-075614: 3e56551dc0046c9ff3f2e3f49fb2ccb82da8c63a8a781dbe13b0631ba8cb47e4
- makeTheAliasOnly-20261105-051649: 79e3205775deace4a9b02810f16abecca0fe3c11e256e8d79b6893df45f5eb1e
- design-20261108-041415: e3585b8e6bf11241cdaafbf2faf5e52fd4c6dfed2176b1e7269b6a54c97d5a3c
