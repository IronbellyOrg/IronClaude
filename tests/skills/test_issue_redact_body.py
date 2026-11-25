"""Tests for ``scripts/redact_body.py`` (the credential check of ``/sc:issue --create``)."""

from __future__ import annotations

import base64
import importlib.util
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "superclaude"
    / "skills"
    / "sc-issue-protocol"
    / "scripts"
    / "redact_body.py"
)


def _load():
    spec = importlib.util.spec_from_file_location("redact_body_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rb = _load()

# Fake values built from fragments: none is a real credential.
GH = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3"
PEM = "-----BEGIN RSA PRIVATE KEY-----\nMIIBOg\n-----END RSA PRIVATE KEY-----"
B64 = base64.b64encode(GH.encode()).decode()  # an encoded token, no known prefix
B64_SLASH = "Qk9nVXN0cmluZ0RhdGEx" + "/" + "bmV3ZXJ0eXVpb3BhZGZnaGprbA9"  # one slash


@pytest.mark.parametrize(
    "line",
    [
        f"token is {GH} here",
        "password: hunter22",
        "PASSWORD=hunter22",
        "API_KEY=abcd1234efgh",
        "api-key: abcd1234efgh",
        "ACCESS_TOKEN: abcdef1234567890abcd",
        "refresh_token = abcdef1234567890abcd",
        '"client_secret": "s3cr3tvalue"',
        "Authorization: Bearer abcdef1234567890abcdef",
        "Authorization: Basic dXNlcjpwYXNzd29yZA==",
        "db at postgres://admin:pa55w0rd@db.example/app",
        "jwt eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIx.SflKxwRJSMeKKF2QT4",
        "sk-" + "a1B2c3D4e5F6g7H8i9J0k1L2",
        "AKIA" + "ABCDEFGHIJKLMNOP",
        "Cookie: session_id=abcdef123456",
        "Cookie: theme=dark; session=zz9876543210",
        "password: $ecret1234",
        "password: correct horse battery staple",
        'password = "correct horse"',
        "password: {{template}} actual-secret",
        '{"password":"prefix\\"remaining-secret123"}',
        "access_token: abcdefghijklmnopqrstuvwxyz",
        "auth_token: a1b2c3d4",
        f"encoded: {B64}",
        f"encoded: {B64_SLASH}",
        "password: |\n  correct horse battery staple",
        "password: 'prefix''remaining-secret123'",
        'password: "first-line\n  remaining-secret123"',
        'password: "first-line\\\n  remaining-secret123"',
        "password: | # production password\n  remaining-secret123",
        '"password": |\n  remaining-secret123',
        "password: <Secret1234567890>",
        PEM,
    ],
)
def test_credentials_are_redacted(line):
    out, count = rb.redact(line)
    assert count >= 1
    assert rb.REDACTED in out
    for secret in (
        GH,
        "hunter22",
        "abcd1234efgh",
        "pa55w0rd",
        "s3cr3tvalue",
        "MIIBOg",
        "zz9876543210",
        "abcdef123456",
        "ecret1234",
        "staple",
        "horse",
        "actual-secret",
        "remaining-secret123",
        "abcdefghijklmnopqrstuvwxyz",
        "a1b2c3d4",
        "Secret1234567890",
        B64,
        B64_SLASH,
    ):
        assert secret not in out


@pytest.mark.parametrize(
    "line",
    [
        "key: ArrowUp",
        "token: Identifier",
        "press key=Enter to continue",
        "password: <your password>",
        "password: ${PASSWORD}",
        "API_KEY=$API_KEY",
        "the token expired after an hour",
        "commit 0123456789abcdef0123456789abcdef01234567 fixed it",
        "https://github.com/IronbellyOrg/IronClaude/blob/a6fec24480e8cc65abbb16b194625e2ea52238c7/SECURITY.md#L484",
        "see .dev/tasks/done/TASK-WF-issueSummary-20261125-190451/artifacts/README-run.md",
    ],
)
def test_harmless_text_is_left_alone(line):
    assert rb.redact(line) == (line, 0)


def test_a_strong_name_redacts_the_rest_of_the_line():
    out, count = rb.redact("password=hunter22 and api_key=abcd1234efgh")
    assert count == 1
    assert "hunter22" not in out and "abcd1234efgh" not in out


def test_a_block_scalar_is_redacted_and_the_next_key_is_kept():
    out, count = rb.redact("password: |\n  hunter22\n  more words\nuser: bob\n")
    assert count == 1
    assert "hunter22" not in out and "more words" not in out
    assert out.endswith("user: bob\n")


def test_one_value_per_line_counts_once_each():
    _, count = rb.redact("password=hunter22\napi_key=abcd1234efgh\n")
    assert count == 2


def test_redaction_is_idempotent():
    once, _ = rb.redact(f"password=hunter22 {GH}")
    assert rb.redact(once) == (once, 0)


def test_main_edits_in_place_and_prints_only_the_count(tmp_path, capsys):
    body = tmp_path / "issue-body.md"
    notes = tmp_path / "draft-notes.md"
    body.write_text(f"Use password=hunter22 and {GH}\n", encoding="utf-8")
    notes.write_text("nothing secret\n", encoding="utf-8")
    assert rb.main([str(body), str(notes)]) == 0
    out = capsys.readouterr().out
    assert out == "redacted: 2\n"
    assert "hunter22" not in body.read_text(encoding="utf-8")
    assert notes.read_text(encoding="utf-8") == "nothing secret\n"


def test_main_never_prints_a_value_when_a_file_is_missing(tmp_path, capsys):
    assert rb.main([str(tmp_path / "missing.md")]) == 2
    assert "redact_body: cannot process" in capsys.readouterr().out
