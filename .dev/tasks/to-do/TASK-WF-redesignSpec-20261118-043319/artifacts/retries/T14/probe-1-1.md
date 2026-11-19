51649d9dad8b473ff104a7d86f14aeade6fcac35
family desk-worktree-note: the desk drops the full worktree note but nothing shows it elsewhere.
search: grep -n -F -e DESK_WORKTREE_NOTE src/superclaude/cli/observe/view.py src/superclaude/cli/observe/render.py
before: view.py definition and desk notes append; render.py import and desk filter
coupled sites: the inspector field list in view.py
after: view.py also lists it in the inspector field list when the questions are on
