64543aeb313326b3ff49f862f8c1ea2f7d7b8375
family=fixture-recipe
defect form: a recipe step uses a repo-relative path after the recipe has cd'ed into the scratch repository
command: grep -n -F -e 'tests/pr_submit/fixtures' -e 'cd ' -- tests/pr_submit/test_conflicts_core.py
before:
9:#   cd "$S" && git init -q -b main repo && cd repo
19:#   cp "$S/out.z" tests/pr_submit/fixtures/merge_tree_conflict.z
20:#   cd / && rm -rf "$S"
coupled sites: line 2 (copy out.z next to this file), line 9 (cd into the scratch repo), line 20 (cd / and cleanup)
after: 11:#   cd "$S" && git init -q -b main repo && cd repo
after: 21:#   cp "$S/out.z" "$R/tests/pr_submit/fixtures/merge_tree_conflict.z"
after: 22:#   cd / && rm -rf "$S"
