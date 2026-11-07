d7997c8df7f1c257d366942ecabcbc9cd41c0aac
family ac-selector: a test the AC runs with -k <word> has no <word> in its name
command: grep -n -E "^def test_(pr[0-9_]|arg1_prompt)" tests/skills/test_issue_orca_worktree.py
before:
850:def test_pr1_levels_keep_only_their_own_block(tmp_path: Path) -> None:
867:def test_pr2_submit_adds_the_submit_block(tmp_path: Path) -> None:
878:def test_pr3_submit_with_worktree_level_is_a_bad_argument(tmp_path: Path) -> None:
884:def test_pr4_no_pr_tokens_outside_the_worktree_prohibition_and_submit(
898:def test_pr_unusable_template_is_reported_not_raised(tmp_path: Path) -> None:
910:def test_arg1_prompt_bad_arguments_exit_2(tmp_path: Path) -> None:
coupled sites: Task 6 AC uses -k launch (name the LA tests with launch); Task 1 -k preflight and Task 2 -k "FO or worktree" already match (module name holds worktree)
after:
850:def test_pr1_prompt_levels_keep_only_their_own_block(tmp_path: Path) -> None:
867:def test_pr2_prompt_submit_adds_the_submit_block(tmp_path: Path) -> None:
878:def test_pr3_prompt_submit_with_worktree_level_is_a_bad_argument(tmp_path: Path) -> None:
884:def test_pr4_prompt_no_pr_tokens_outside_the_worktree_prohibition_and_submit(
898:def test_prompt_unusable_template_is_reported_not_raised(tmp_path: Path) -> None:
910:def test_arg1_prompt_bad_arguments_exit_2(tmp_path: Path) -> None:
