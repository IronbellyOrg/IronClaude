bcbec7b3496ae617b63e13242967471cef806251
family: repeat-run-existing-folder-unverified
defect form: a folder counted as already saved is not checked against origin/main on the branch that writes a new folder
command: grep -n -E "_verify_folder\(|existing" scripts/worktree_cleanup.py
before: _verify_folder is called for existing folders only when nothing is new (line 2238) and for the new folder (line 2305)
coupled sites: the held digests built from existing folders; the every set returned to the caller; the repeat-run tests in test_archive.py

family: read-failure-not-failed-closed
defect form: a file read outside a try block can raise OSError instead of returning a saved copy failed result
command: grep -n -E "first_secret\(|_sha256\(os|open\(" scripts/worktree_cleanup.py
before: first_secret at 2200, _sha256 of worktree files at 2228 and 2233, all outside the try block
coupled sites: file_has_secret, check_save_paths, the write block try at 2255-2288 (also needs ValueError for odd names)

family: secret-pattern-over-broad
defect form: a token pattern without a left boundary matches inside ordinary words
command: grep -n -E "rb\"" scripts/worktree_cleanup.py
before: lines 1837 to 1844; sk-, AKIA and the gh prefix have no left boundary
coupled sites: test_other_token_shapes_are_found and test_ordinary_file_names_and_text_do_not_trip_the_check in test_archive.py
after:
1837:        rb"(?<![A-Za-z0-9_-])gh[pousr]_[A-Za-z0-9]{20,}",
1838:        rb"(?<![A-Za-z0-9_-])github_pat_[A-Za-z0-9_]{20,}",
1839:        rb"(?<![A-Za-z0-9_-])sk-(?:ant-)?[A-Za-z0-9_-]{20,}",
1840:        rb"(?<![A-Za-z0-9_-])AKIA[0-9A-Z]{16}",
1841:        rb"xox[abprs]-[A-Za-z0-9-]{10,}",
1842:        rb"AIza[0-9A-Za-z_-]{35}",
1843:        rb"-----BEGIN [A-Z ]*PRIVATE KEY-----",
1844:        rb"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
1877:    with open(path, "rb") as handle:
1887:    with open(path, "rb") as handle:
1896:def first_secret(worktree: str, rels: Sequence[str]) -> str | None:
1973:                self._handle = open(self._parts.pop(0), "rb")
2094:def _verify_folder(runner: Runner, clone: str, folder: str) -> str | None:
2201:        secret = first_secret(worktree, untracked + ignored)
2203:            p: _sha256(os.path.join(worktree, p)) for p in untracked + ignored
2233:        why = _verify_folder(runner, evidence_dir, folder)
2279:        sums[SAVED_PATHS_NAME] = _sha256(os.path.join(partial, SAVED_PATHS_NAME))
2304:    problem = _verify_folder(runner, evidence_dir, folder)
2339:        dest="verb", required=True, metavar="{" + ",".join(VERBS) + "}"
