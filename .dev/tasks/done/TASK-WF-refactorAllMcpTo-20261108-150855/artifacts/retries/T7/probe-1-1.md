f89cc1825d4498ef8034c913d7b5e4b3e2a0f97e
# Family probe for review r1-1 (T7)

Scope (touched files): src/superclaude/skills/sc-brainstorm-protocol/SKILL.md, src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md, src/superclaude/skills/sc-auggie-review-protocol/SKILL.md, src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md, src/superclaude/skills/sc-pr-submit-protocol/SKILL.md

## family=readonly-wave-push (F7.1)

- Defect form: the added codebase-search text tells the agent to commit and push the PR head inside the C3a wave, which the same file declares read-only with no version-control mutation (finding-verify.md:9-11).
- Probe command: `grep -n -F -e 'commit and push' -- src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md`
- before:
  - 35:   commit and push the PR head before relying on it); if that tool is not available, call
- Coupled sites: finding-verify.md:9-11 (the NFR-6 read-only note); finding-verify.md:36 (unpushed changes go to codegraph or Grep).

## family=readonly-wave-shell-token (F7.2)

- Defect form: the NFR-6 note claims the wave "contains no shell command tokens", but the mandated AUG phrase names the read-only lookup `git remote get-url origin`.
- Probe command: `grep -n -F -e 'no shell' -e 'git remote get-url origin' -- src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md`
- before:
  - 10:> spawns a read-only validator agent. It performs NO version-control mutation and contains no shell
  - 34:   `git remote get-url origin`, `branch` = the PR head branch; it sees pushed commits only, so
- Coupled sites: finding-verify.md:11 (continuation of the note).

## family=aug-phrase-verbatim (F7.3)

- Defect form: the full AUG phrase is nested in a parenthetical and ". For uncommitted" was rewritten to "; for uncommitted", so it is not verbatim (plan line 20).
- Probe command: `grep -n -F -e '; for uncommitted' -- src/superclaude/skills/sc-brainstorm-protocol/SKILL.md src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md src/superclaude/skills/sc-auggie-review-protocol/SKILL.md src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`
- before:
  - src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:225
- Coupled sites: none in scope (handoff-routing.md:18 already holds the verbatim phrase; finding-verify.md:32-36 uses the plan's PR-head-branch variant with the verbatim closing sentence).

## after (fix pass for r1-1)

- after: readonly-wave-push: P1 returns no lines (rc=1); finding-verify.md:35-36 now ends "it sees pushed commits only); if that tool is not available, call `mcp__auggie__codebase-retrieval`."
- after: readonly-wave-shell-token: P2 returns 10, 11 (note now names the read-only `git remote get-url origin` lookup as the only shell token) and 35 (the lookup itself).
- after: aug-phrase-verbatim: P3 returns no lines (rc=1); sc-auggie-review-protocol/SKILL.md:225 refers to "codebase search (below)" and :226 holds the full AUG phrase verbatim. No other file cites sc-auggie-review-protocol/SKILL.md lines past 225.
