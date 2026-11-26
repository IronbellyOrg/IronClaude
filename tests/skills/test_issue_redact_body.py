"""Tests for ``scripts/redact_body.py`` (the credential check of ``/sc:issue --create``)."""

from __future__ import annotations

import base64
import importlib.util
import time
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
B64_TWO = (
    "IQoJb3JpZ2luX2VjEJr/AbCdEfGhIjKlMnOpQrStUv12/wXyZ0987654321abcdEFGH"  # two slashes
)
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
        f"session {B64_TWO} end",
        f"the token is {B64_TWO}.",
        "db.example.com:5432:app:bob:remaining-secret123",
        "*:*:*:bob:remaining-secret123",
        "127.0.0.1:5432:app:bob:remaining-secret123",
        "Cookie: |\n    session=remaining-secret123",
        'password = """\nfirst-part\nremaining-secret123\n"""',
        "password = '''\nfirst-part\nremaining-secret123\n'''",
        'Cookie: "theme=dark\n  session=remaining-secret123"',
        'Cookie: "session=abc123"; theme=opaqueSecret123456',
        "password: |\n  correct horse battery staple",
        "password: 'prefix''remaining-secret123'",
        'password: "first-line\n  remaining-secret123"',
        'password: "first-line\\\n  remaining-secret123"',
        "password: | # production password\n  remaining-secret123",
        '"password": |\n  remaining-secret123',
        "password: first-line\n  remaining-secret123",
        "password: $PASSWORD\n  remaining-secret123",
        "machine example.com login bob password remaining-secret123",
        'machine example.com login bob password "first remaining-secret123"',
        'password "first remaining-secret123"',
        '{"headers":{"Cookie":"session=remaining-secret123; theme=dark"}}',
        "machine example.com\n  login bob\n  password remaining-secret123\n",
        "password:\n  first-part\n  remaining-secret123",
        'password: "' + "ab12" * 700 + '\n  tail-secret99"',
        "password: <Secret1234567890>",
        'password = """prefix\\"""remaining-secret123\n"""',
        "REDIS_URL=redis://:correcthorsebatterystaple@host/0",
        'Cookie: "theme=dark\n  session=remaining-secret123" # note',
        "a" * 100 + "_password: remaining-secret123",
        '{"auths":{"registry.example.com":{"auth":"dXNlcjpwYXNz"}}}',
        "auth: dXNlcjpwYXNzd29yZA==",
        '{"auth": "dTph"}',
        '{"auth": "abcdefghijklmnop"}',
        "auth: 'secretvalueonly'",
        "MYSQL_PWD=remaining-secret123",
        "DB_PASS=remaining-secret123",
        "export DB_PASS='remaining-secret123'",
        "passphrase: remaining-secret123",
        "<settings><server><password>remaining-secret123</password></server></settings>",
        "<apiKey>remaining-secret123</apiKey>",
        "<db-pass>\n  remaining-secret123\n</db-pass>",
        '<password type="plain">remaining-secret123</password>',
        "<password><![CDATA[remaining-secret123]]></password>",
        "<password>\n  <![CDATA[first\nremaining-secret123]]>\n</password>",
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
        "tail-secret99",
        "correcthorsebatterystaple",
        "dXNlcjpwYXNz",
        "dTph",
        "abcdefghijklmnop",
        "secretvalueonly",
        "opaqueSecret123456",
        B64_TWO,
        B64,
        B64_SLASH,
    ):
        assert secret not in out


@pytest.mark.parametrize(
    "line",
    [
        "key: ArrowUp",
        "token: Identifier",
        "auth: required",
        '{"auth": "none"}',
        "auth: 'required'",
        "auth: none",
        "author: Bobby123",
        "<password>${env.DB_PASSWORD}</password>",
        "<title>Password reset</title>",
        "PWD=/home/coder/project",
        "pass: 3 tests",
        "bypass: true",
        "the build finished at 10:30:15:00:05 local time",
        "press key=Enter to continue",
        "password: <your password>",
        "password: ${PASSWORD}",
        "API_KEY=$API_KEY",
        "the token expired after an hour",
        "password reset emails are sent by the mailer",
        "login page shows a password field",
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


def test_a_plain_multiline_value_is_redacted_and_the_next_key_is_kept():
    out, _ = rb.redact("password: first-line\n  remaining-secret123\nuser: bob\n")
    assert "first-line" not in out and "remaining-secret123" not in out
    assert out.endswith("user: bob\n")


def test_a_quoted_cookie_keeps_the_json_around_it():
    text = '{"headers":{"Cookie":"session=abc123; theme=dark","Accept":"x"}}'
    out, count = rb.redact(text)
    assert count == 1
    assert out == '{"headers":{"Cookie":"<REDACTED>","Accept":"x"}}'


def test_a_quoted_netrc_password_never_swallows_later_prose():
    text = 'login bob password "first second"\nWe said "hello" later.\n'
    out, count = rb.redact(text)
    assert count == 1
    assert out.endswith('We said "hello" later.\n')
    assert "first second" not in out


@pytest.mark.parametrize(
    "unit",
    ["a", "ab1", "a-", "a.b", "x_y1", "-", "- ", " -", "--\n"]
    + [
        "password",
        "cookie",
        "api_key",
        "token",
        "Cookie ",
        "secret:",
        "<a",
        "<password",
    ],
)
def test_a_long_uninterrupted_string_is_scanned_in_linear_time(unit):
    text = unit * (200_000 // len(unit))
    started = time.monotonic()
    out, count = rb.redact(text)
    assert time.monotonic() - started < 5
    assert count <= 1  # a long base64-looking run may be redacted once


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
