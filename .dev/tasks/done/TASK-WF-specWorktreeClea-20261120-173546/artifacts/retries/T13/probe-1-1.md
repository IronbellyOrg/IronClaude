4c265e9d8a2941c5952c5fff53f3340b866aa510
family: recorder-verbs
defect form: a verb and flag combination that the recorder test never runs, so the commands of that path are never checked
command: grep -n "rec.run(" tests/worktree_cleanup/test_safety.py
before: test_safety.py:168-180 (retire with --apply only against rows that are not removable; no archive or list with --apply)
coupled sites: run_every_verb, test_a_dry_run_records_no_removal_and_apply_removes_only_removable_rows, test_the_clear_and_the_terminal_close_come_after_the_verified_save

family: bare-substring-assertion
defect form: a verb-level test asserts a folder name or a word that is in every output, so it cannot fail when the reason is wrong
command: grep -n '" in capsys.readouterr().out\|in shown' tests/worktree_cleanup/test_pipeline.py
before: test_pipeline.py:195 ("later"), the squash test (failed 0 only)
coupled sites: the commit after the pull request test, the squash and branch test
after:
tests/worktree_cleanup/test_safety.py:168:    rec.run("list", expect=0)
tests/worktree_cleanup/test_safety.py:169:    rec.run("prune", expect=0)
tests/worktree_cleanup/test_safety.py:174:    rec.run("archive", "done", expect=0)
tests/worktree_cleanup/test_safety.py:175:    rec.run("retire", "done", expect=0)  # a dry run
tests/worktree_cleanup/test_safety.py:176:    rec.run("archive", "open", expect=64)
tests/worktree_cleanup/test_safety.py:177:    rec.run("archive", "edited", expect=64)
tests/worktree_cleanup/test_safety.py:178:    rec.run("retire", "open", "--apply", expect=64)
tests/worktree_cleanup/test_safety.py:179:    rec.run("retire", "edited", "--apply", expect=64)
tests/worktree_cleanup/test_safety.py:180:    rec.run("retire", "main", "--apply", expect=64)
tests/worktree_cleanup/test_safety.py:182:    rec.run("list", "--apply", expect=0)
tests/worktree_cleanup/test_safety.py:183:    rec.run("archive", "done", "--apply", expect=0)
tests/worktree_cleanup/test_safety.py:185:    rec.run("retire", "done", "--apply", expect=0)
tests/worktree_cleanup/test_safety.py:187:    rec.run("prune", "--apply", expect=0)
tests/worktree_cleanup/test_safety.py:188:    rec.run("list", expect=0)
tests/worktree_cleanup/test_safety.py:189:    rec.run("prune", "--apply", expect=0)
tests/worktree_cleanup/test_pipeline.py:196:    assert row.endswith("| kept | 1 commit after the pull request |")
tests/worktree_cleanup/test_pipeline.py:225:        "| removed | branch kept (not fully merged, as after a squash merge) |"
tests/worktree_cleanup/test_pipeline.py:227:    assert rows["done"].endswith("| removed | branch removed |")
