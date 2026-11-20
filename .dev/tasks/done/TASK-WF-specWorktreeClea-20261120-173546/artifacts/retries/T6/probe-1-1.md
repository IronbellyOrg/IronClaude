ecb11d4e9bd0ff8c6a0a18828c506d3204b88c82
family: missing-folder-reason
defect form: a rule reads a fact that a missing folder leaves empty before it checks that the folder is missing
command: grep -n -E "age is not None|f\.present|git_dir|facts\.origin|f\.origin" scripts/worktree_cleanup.py
before:
973:    git_dir: str | None = None
1061:        facts.git_dir = os.path.normpath(os.path.join(wt.path, out.strip()))
1063:    facts.origin = parse_origin(out) if out is not None else None
1074:    if facts.git_dir is not None:
1076:            _mtime(os.path.join(facts.git_dir, name))
1081:        facts.created_ts = _mtime(os.path.join(facts.git_dir, "gitdir")) or _mtime(
1087:            if os.path.exists(os.path.join(facts.git_dir, m))
1605:    if f.origin is None or not f.origin.is_ours:
1611:    if not f.present:
1725:    if age is not None and age < floor:
coupled sites: _rule1 origin test at 1605 and missing test at 1611; test_rules.py case missing (origin set, so it hid the defect)

family: fail-open-unread-fact
defect form: a rule passes when the fact it needs was left unset by a failed read
command: same as above
before: same as above
coupled sites: _rule7 age test at 1725; _rule6 operations check (git_dir None leaves operations empty); the good fixture in test_rules.py leaves git_dir unset and must set it; rules 3, 4, 5 and idle already fail closed on None
after:
973:    git_dir: str | None = None
1061:        facts.git_dir = os.path.normpath(os.path.join(wt.path, out.strip()))
1063:    facts.origin = parse_origin(out) if out is not None else None
1074:    if facts.git_dir is not None:
1076:            _mtime(os.path.join(facts.git_dir, name))
1081:        facts.created_ts = _mtime(os.path.join(facts.git_dir, "gitdir")) or _mtime(
1087:            if os.path.exists(os.path.join(facts.git_dir, m))
1605:    if not f.present:
1608:    if f.origin is None or not f.origin.is_ours:
1714:    if f.git_dir is None or any("could not be read" in x for x in f.failures):
1726:    if age is None:
