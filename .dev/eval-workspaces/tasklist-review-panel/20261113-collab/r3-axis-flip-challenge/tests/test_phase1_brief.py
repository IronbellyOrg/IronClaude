from conftest import (
    CONTROL,
    EVAL,
    R3,
    default_rules,
    launch,
    mini_sandbox,
    write_plan,
    write_values,
)

H1 = "Its source document is {SRC} (sha256 of the file: {SRC_SHA}); read the candidate and the source document in full before you review."


def test_brief_differs_from_rr_only_by_h1():
    rr = (EVAL / "tools/run-reviewer.sh").read_text().splitlines()[12:17]
    rebuilt = (
        "\n".join(rr)[len('BRIEF="') : -1]
        .replace("$CAND_SB", "{CAND}")
        .replace("$SHA", "{SHA}")
    )
    brief = (R3 / "config/phase1-brief.txt").read_text().rstrip("\n")
    assert brief.replace(" " + H1, "") == rebuilt
    assert brief.count(H1) == 1 and "review 1 of 3. " + H1 in brief


def test_rendered_brief_names_absolute_source(env):
    write_values(env)
    mini_sandbox(env)
    write_plan(env, default_rules(env))
    r, rd = launch(env, collab=0)
    assert r.returncode == 0, r.stderr
    b = (rd / CONTROL / "reviews/t4-1.brief.txt").read_text()
    src = f"{env['env']['R3_SB_ROOT']}/cand/{CONTROL}/source.md"
    assert src in b and "{" not in b.replace('{"', "")
