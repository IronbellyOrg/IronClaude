"""K2 for RL: every model of the lens table is an allowed reviewer model, and the judge model is named only in the
judge script (TESTING 4: `grep -rn claude-opus-5-5 $RL/bin $RL/rl $RL/scaffold` hits only bin/judge-one.sh)."""

import json

from helpers import REVIEWERS, SW, sh

from rl import lens

JUDGE = "claude-opus-5-5"


def test_lens_models_are_allowed():
    table = json.loads((SW / "config" / "lenses.json").read_text(encoding="utf-8"))
    models = {r["model"] for p in table["panels"].values() for r in p["roles"].values()}
    assert models == set(REVIEWERS)
    for m in sorted(models):
        assert sh(f"sw_assert_model {m}").returncode == 0, m


def test_lens_module_allowlist_is_the_shell_allowlist():
    assert set(lens.allowed_models()) == set(REVIEWERS)
    assert sh(f"sw_assert_model {JUDGE}").returncode == 1


def test_opus_only_in_judge_script():
    hits = [
        str(p.relative_to(SW))
        for sub in ("bin", "rl", "scaffold")
        for p in sorted((SW / sub).rglob("*"))
        if p.is_file()
        and "__pycache__" not in p.parts
        and JUDGE in p.read_text(encoding="utf-8", errors="replace")
    ]
    assert hits == ["bin/judge-one.sh"]
