Review 1-1 of T195 (fresh subagent, prompt-1-1.md): T195.AC1 unmet behind F1.1.
F1.1 ac=T195.AC1 at=src/superclaude/cli/sweep/commands.py:174 anchor="Write, fsync or close fails (for example a full disk) | Unlink this run's temp file, exit 1" chk=y,n,n,n family=publish-temp-cleanup: text.encode("utf-8") runs inside the try after os.open created the temp file; a UnicodeEncodeError is not an OSError, so the temp file is never unlinked (confirmed with _publish("ok \ud800 bad", ...)).
F1.2 note commands.py:75-84 chk=n,n,n,n: an empty --root string is accepted when the current folder holds .git.
F1.3 note commands.py:129-134 chk=n,n,n,n: _sweeps_base takes the deepest folder named sweeps under .dev, so a nested .dev/sweeps/.dev/sweeps output compares against the nested folder (logged choice 5; _check_output already enforces the real bound).
F1.4 note commands.py:113-137 chk=n,n,n,n: the overlap check against the input folders is almost always redundant after the .dev/sweeps containment check.
Review 2-1 of T195 (fresh subagent, prompt-2-1.md): T195.AC1 met. F1.1 resolved. No blocking findings.
