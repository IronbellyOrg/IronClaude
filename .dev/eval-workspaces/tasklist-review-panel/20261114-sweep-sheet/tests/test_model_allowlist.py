"""K2: reviewer models are exactly four; the judge model appears only in bin/judge-one.sh."""

from helpers import REVIEWERS, SW, sh

JUDGE = "claude-opus-5-5"


def test_reviewer_models():
    for m in REVIEWERS:
        assert sh(f"sw_assert_model {m}").returncode == 0, m
    # exact match only
    for m in (
        "claude-sonnet-5-5-x",
        "claude-sonnet-5",
        "GPT-6-LUNA",
        "muse-ember-1.0 gpt-6-luna",
        "gpt-6-luna ",
        "",
    ):
        assert sh(f"sw_assert_model '{m}'").returncode == 1, m


def test_opus_only_in_judge():
    r = sh(f"sw_assert_model {JUDGE}")
    assert r.returncode == 1 and "E_MODEL" in r.stderr
    hits = set()
    for sub in ("bin", "sweep", "scaffold"):
        for p in (SW / sub).rglob("*"):
            if p.is_file() and "__pycache__" not in p.parts:
                if JUDGE in p.read_text(encoding="utf-8", errors="replace"):
                    hits.add(str(p.relative_to(SW)))
    assert hits <= {"bin/judge-one.sh"}, hits


def test_fable_and_tier0_refused():
    for m in (
        "claude-fable-1",
        "fable",
        "Qwen3.8-max",
        "qwen3-coder",
        "glm-5.3",
        "gpt-6.1-sol",
        "grok-4.7",
    ):
        r = sh(f"sw_assert_model '{m}'")
        assert r.returncode == 1 and "E_MODEL" in r.stderr, m


def test_nofallback_guard():
    assert sh("NOFALLBACK=1 sw_assert_nofallback").returncode == 0
    r = sh("sw_assert_nofallback")
    assert r.returncode == 1 and "NOFALLBACK" in r.stderr
    assert sh("NOFALLBACK=0 sw_assert_nofallback").returncode == 1
