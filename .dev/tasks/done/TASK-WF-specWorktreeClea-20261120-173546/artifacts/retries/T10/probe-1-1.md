feef03e3aed612bd5efb11ae0a546ecf0836bff5
family: secret-clone-scope
defect form: a secret test reads only part of the evidence clone, or none of it
command: grep -n -E "\.git\" not in|rglob\(\"\*\"\)|secret not in" tests/worktree_cleanup/test_archive.py
before:
101:        for p in sorted(folder.rglob("*"))
128:    n = sum(1 for p in folder.rglob("*") if p.is_file())
439:    assert secret not in result.reason and secret not in " ".join(case.notes)
441:    assert secret not in out.out and secret not in out.err
445:    for p in Path(case.clone).rglob("*") if Path(case.clone).exists() else []:
675:    assert all(secret not in text for text in shown)
678:        if p.is_file() and ".git" not in p.parts
coupled sites: the first secret test at 430 (the clone does not exist there) and the existing-clone test at 665

family: committed-token-literal
defect form: a whole token-shaped literal committed in one piece
command: grep -n -E "AKIA|sk-|ghp_" tests/worktree_cleanup/test_archive.py
before:
602:        "mask-AKIA<REDACTED>\n"
coupled sites: lines 464 to 470 and 609 already build their strings from two pieces
after:
430:def assert_value_in_no_clone_file(secret: str, clone: str) -> int:
462:    assert assert_value_in_no_clone_file(secret, case.clone) > 4
478:    "prefix", ["github" + "_pat_", "sk" + "-", "AKIA", "xox" + "b-"]
484:        if prefix != "AKIA"
616:        "mask-AKIA" + "0123456789ABCDEF\n"
623:        "key=sk" + "-" + "A1b2C3d4" * 4 + "\nid: AKIA" + "0123456789ABCDEF\n",
691:        assert_value_in_no_clone_file(secret, case.clone) > 4
