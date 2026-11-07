5356848cd02421cf5ba8b5a3e840f3bd3dcaf083
family stub-counter-location
defect form: the poll stub keeps its call counter outside the stub directory
command: grep -n -F -e gh-view-count -- tests/pr_submit/test_conflict_scripts.py
before:
1846:    counter = repos.root / "gh-view-count"
coupled sites: the counter path is used once to create the counter and once in the stub body (same line)
after:
1846:    counter = repos.bin_dir / "gh-view-count"
