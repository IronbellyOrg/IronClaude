# Research: Hooks architecture for issue 322

- **Topic type:** Quick static architecture analysis
- **Scope:** src/superclaude/hooks, with installer and test integration checks
- **Status:** Completed static analysis; no source changes
- **Date:** 2026-11-23
- **Template:** /home/coder/.claude/templates/modularization-template-review/codebase-research_template.md
- **Command:** /sc:analyze src/superclaude/hooks --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/322/analyze

Codegraph: index_state=fresh, checked_at=2026-11-23T22:46:25Z; degraded: graph:empty, graph:ambiguous

## Findings
### High: General write boundary not registered

[CODE-VERIFIED] The complete PreToolUse block has five entries: freshness, Python command policy, Orca agent presence, launch-level restrictions and Bash job identity. There is no all-tool fixed-root admission or failure-blocking boundary registration. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/hooks.json:84-135. This is an unbuilt feature, not a regression introduced by this review.

[CODE-VERIFIED] The project workspace guard extracts only file_path, blocks the skill-creator workspace naming pattern, and permits missing paths and every other destination. It does not bind writes to the session checkout. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/reject-workspace-writes.sh:19-39 and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.claude/settings.json:3-13.

### Medium: Adjacent safeguards are not confinement

[CODE-VERIFIED] The launch-level guard only governs claim-launched sessions, leaving ordinary sessions unblocked by that guard. The Orca creation hook expressly enforces only agent presence, not checkout ownership. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/launch-level-guard.sh:2-9 and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/require-orca-worktree-agent.sh:2-14.

[CODE-VERIFIED] Freshness checks read history, permits inputs without file_path, and writes framework state/log destinations. A future confinement design must distinguish trusted framework writes from agent writes. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/freshness-pre-edit.sh:4-31.

[CODE-VERIFIED] Existing swarm confine_path provides prior art for component-aware path checks but only confines particular outputs; its trusted-filesystem model expressly excludes concurrent symlink swapping. It is not whole-session isolation. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/state.py:65-119.

### Integration and metrics

[CODE-VERIFIED] Reuse the existing installer, which loads canonical hook JSON and backs up existing settings. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_hooks.py:301-345. Graph impact/callers identify the production install_hooks integration and an experimental duplicate; the duplicate is not production evidence.

[CODE-VERIFIED] Glob returned 21 hook-tree files; hooks.json:84-135 contains five PreToolUse registrations. Codegraph indexed only two code files in this shell/JSON-heavy target, so native Glob/Grep/Read supplied the analysis floor. Security and performance runtime metrics were not measured.

### Recommendations

[UNVERIFIED] Proposed next work, not existing capabilities: revise the retired-tool inventory and private temp/cache exception policy, choose a supported containment backend, and decide the Git mutation policy before implementation planning. Require real-tool denial and failure-injection checks before advertising enforcement.

## Gaps
- UNVERIFIED: runtime enforcement, deployed client compatibility, hook failure precedence, OS containment and concurrent filesystem races. This command is static analysis only; no compilation, dynamic security tests or source changes were performed.
- Negative verification: proposed boundary filenames are absent from Glob under src and tests. Broad Grep found only adjacent controls and swarm output confinement; semantic Augment search on master likewise returned adjacent safeguards, not the proposal's implementation. Search is corroboration, not a proof of universal absence.
- First Augment attempt used its default main branch and failed BRANCH_NOT_FOUND; retried successfully with master. Codegraph returned an empty shell-target outline and an ambiguous installer definition with an experimental duplicate; these were resolved by reading current source.
- GitHub timeline events beyond the exposed issue discussion/dependency/closure fields are UNVERIFIED because the brief permits only issue/pr view/list, not timeline API calls.

## Key Takeaways
Issue 322 remains a live design-refresh request. Existing hooks enforce narrower policies, and reusable path-checking code is not whole-process confinement. Reuse the canonical installer, but finish the design and platform proof before any implementation claim or activation.
