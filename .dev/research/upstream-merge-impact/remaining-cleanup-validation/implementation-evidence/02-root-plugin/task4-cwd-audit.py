"""Recognize shell directory transitions and audit exact persisted native cwd values."""

import re
import shlex
from pathlib import Path


def shell_transitions(command):
    """Ignore heredoc data and inspect command words, not quoted prose arguments."""
    kept = []
    pending = []
    for line in command.splitlines():
        if pending:
            if line.strip() == pending[0]:
                pending.pop(0)
            continue
        kept.append(line)
        pending.extend(re.findall(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?", line))
    lexer = shlex.shlex("\n".join(kept), posix=True, punctuation_chars=";&|()\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = "#"
    result = []
    boundary = True
    wrapper = False
    for token in lexer:
        if token and all(character in ";&|()\n" for character in token):
            boundary = True
            wrapper = False
            continue
        if token in ("then", "do", "else", "{", "}"):
            boundary = True
            wrapper = False
            continue
        if not boundary:
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", token):
            continue
        if token in ("command", "builtin", "exec"):
            wrapper = True
            continue
        if wrapper and token.startswith("-"):
            continue
        if token in ("cd", "pushd", "popd"):
            result.append(token)
        boundary = False
        wrapper = False
    return result


def persisted_cwd_allowed(cwd, launch, audit_root):
    return Path(cwd).resolve() in {Path(launch).resolve(), Path(audit_root).resolve()}


def self_check():
    assert shell_transitions("O=/tmp/out; cd $O; pwd") == ["cd"]
    assert shell_transitions('cd "/tmp/out" && pwd') == ["cd"]
    assert shell_transitions("for x in a; do builtin cd $x; done") == ["cd"]
    assert shell_transitions("pushd /tmp; popd") == ["pushd", "popd"]
    assert not shell_transitions("printf '%s' 'cd /tmp'")
    assert not shell_transitions("cat <<'EOF'\ncd example\nEOF\npwd")
    assert persisted_cwd_allowed("/tmp/exact-launch", "/tmp/exact-launch", "/fixture")
    assert persisted_cwd_allowed("/fixture", "/tmp/exact-launch", "/fixture")
    assert not persisted_cwd_allowed("/tmp/other", "/tmp/exact-launch", "/fixture")
    assert not persisted_cwd_allowed("/fixture/artifacts", "/tmp/exact-launch", "/fixture")


if __name__ == "__main__":
    self_check()
    print("cwd guard regression self-check PASS")
