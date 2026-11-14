"""bin/anon.sh (design 5.1 step 4; R-29)."""

import json
import re

from r4help import EVAL, R4, run

HEAD = f"""review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /tmp/evalsb-collab-r4/cand/P/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report {R4}/runs/row/P/reviews/t2b-1.final.md, block ok true
- t4-1: report {R4}/runs/row/P/reviews/t4-1.final.md, block ok true
- t3-1: report {R4}/runs/row/P/reviews/t3-1.final.md, block ok true
"""


def anon(tmp_path, text):
    i, o = tmp_path / "merged-1.md", tmp_path / "scoring" / "merged-anon.md"
    i.write_text(text)
    r = run([R4 / "bin" / "anon.sh", i, o])
    return r, (o.read_text() if o.exists() else None)


FORBIDDEN = ['"origin":', "panel card", "evalsb-collab", "/tmp/jdg", "r4-flag", "20261113-collab", "t2b-1", "t4-1", "t3-1"]


def test_strips_everything(tmp_path):
    body = HEAD + f"""
| L1 | open | yes | t4-1, t3-1 |
see {EVAL}/P/candidate.md and /tmp/evalsb-collab-r4/sb/P/repo/x.py
{{"id":"F1","origin":"peer","anchor":"abc"}}
[panel card c1] was settled; card c0: passed by grep
Card c1 asks for the finite check; t2b-1 agreed with t4-1.
"""
    r, out = anon(tmp_path, body)
    assert r.returncode == 0, r.stderr
    low = out.lower()
    for s in FORBIDDEN:
        assert s.lower() not in low, s
    assert not re.search(r"\bcards? c[0-9]+\b", low)
    assert "<EVAL>" in out and "report <redacted>" in out and "candidate: <candidate file> sha256 71d4a745" in out
    key = json.load(open(tmp_path / "scoring" / "label-key.json"))["reviewer_labels"]
    assert sorted(key) == ["t2b-1", "t3-1", "t4-1"] and sorted(key.values()) == ["R1", "R2", "R3"]
    assert f"| {key['t4-1']}, {key['t3-1']} |" in out  # same label everywhere


def test_peer_reviewer_phrase_rewritten(tmp_path):
    r, out = anon(tmp_path, HEAD + "claim: a peer reviewer flagged this\n")
    assert r.returncode == 0 and "a reviewer flagged this" in out


def test_uppercase_id_fails(tmp_path):
    r, _ = anon(tmp_path, HEAD + "claim: T4-1 said so\n")
    assert r.returncode == 1 and "anon_failed" in r.stderr
