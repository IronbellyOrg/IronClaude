52d91b4f4e7deb8d52877f8cb67cb359519e008a
## family=l2-install-state-config (from r1-1 F1.1, blocking; F1.2 same family)

- Defect form: a precondition failure that FR-033 / OC-10 route to `unsupported` (git config unreadable, git rev-parse failed) is reported by `install_l2` as `unavailable`, because `_l2_preconditions` returns `absent` and `_l2_as_install` maps `absent` to `unavailable`.
- Command: `grep -n -E "_l2_as_install\(state, why\)|L2_WHY_CONFIG, None|L2_WHY_GIT, None|FR-033 item 1" src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-present-unverified.md`
- Before:
  - orca_worktree.py:1293: which ``install_l2`` reports as ``unavailable`` (FR-033 item 1). Only
  - orca_worktree.py:1304: return "absent", L2_WHY_CONFIG, None
  - orca_worktree.py:1313: return "absent", L2_WHY_GIT, None
  - orca_worktree.py:1345: return _l2_as_install(state, why)
  - t7-present-unverified.md:11: FR-033 item 1: ... `install_l2` returns `unavailable` (was `unsupported` in T6).
- Coupled sites: orca_worktree.py:1304 and :1313 (the two `absent` sources; `l2_status` keeps `absent` for them), :1345 (the only install_l2 site that maps a preconditions result; S2 :1351 and S6 :1389 map `l2_status` results after preconditions already passed), :1293 (docstring), t7-present-unverified.md:11 and Divergence 1 (:17).
- after: orca_worktree.py:1304: return "absent", L2_WHY_CONFIG, None (kept: l2_status reports absent, FR-041; install_l2 maps it to unsupported at :1347)
- after: orca_worktree.py:1313: return "absent", L2_WHY_GIT, None (kept, same reason)
- after: no hit for `_l2_as_install(state, why)` or `FR-033 item 1`; install_l2:1347 returns `"unsupported" if state == "absent" else state`; smoke not-a-repo gives install=unsupported, status=absent.
