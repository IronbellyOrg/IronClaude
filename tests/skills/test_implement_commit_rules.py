"""Static pins for the `/sc:implement --commit-tasks` rules (Task 34).

Enforcement type: STATIC (the text of `commands/implement.md`, `sc-implement-protocol/SKILL.md`
and its refs, with the byte-identical plugin copies), plus one behavior check that runs the
read-only `vcs reconcile` verb on a throwaway repository.

Covers T-09, T-10 (sidecar part), T-15, T-16, T-24, T-25 and FR-050 to FR-053, FR-070, FR-072
and FR-079 of the git/PM workflows requirements. The wiring pins of Task 26 stay in
`test_implement_commit_option.py`; this file pins the rules of `refs/commit-step.md`.

Every pin reads the text as it is now. Two cases do not hold today and are marked
`xfail(strict=True)` with the reason, because the requirement is in the task text and the
earlier text lacks it (see `test_no_sc_git_protocol_file_contains_the_flag` and
`test_legacy_whole_list_review_names_the_current_delivery_files`).
"""

import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src/superclaude"
PLUGIN = ROOT / "plugins/superclaude"
PROTOCOL = SRC / "skills/sc-implement-protocol"
COMMAND = SRC / "commands/implement.md"
SKILL = PROTOCOL / "SKILL.md"
REF = PROTOCOL / "refs/commit-step.md"
LEDGER_REF = PROTOCOL / "refs/ledger.md"
QA_REF = PROTOCOL / "refs/qa.md"
MANAGED_REF = PROTOCOL / "refs/managed-workspace.md"
HELPER = SRC / "skills/sc-git-protocol/scripts"
PLUGIN_REF = PLUGIN / "skills/sc-implement-protocol/refs/commit-step.md"

REF_LINE_CAP = 250
PART_ONE = "# Commit step, part one: Reconcile and settle"
PART_TWO = "# Commit step, part two: Commit procedure"

# FR-052: the only primitive files that may hold the string `--commit-tasks`.
FLAG = "--commit-tasks"
PRIMITIVE_ROOTS = (
    SRC / "commands",
    SRC / "skills",
    SRC / "agents",
    SRC / "core",
    SRC / "hooks",
    SRC / "templates",
    PLUGIN,
)
ALLOWED_FILES = {
    "src/superclaude/commands/implement.md",
    "src/superclaude/core/HOW-WE-WORK.md",
    "src/superclaude/core/WORKER-CONTRACT.md",
    "plugins/superclaude/commands/implement.md",
    "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md",
}
ALLOWED_PREFIXES = (
    "src/superclaude/skills/sc-implement-protocol/",
    "plugins/superclaude/skills/sc-implement-protocol/",
)
# The helper's own docstrings and one `--flag` help string name the flag in the two scripts
# below (vcs.py lines 83 and 730; vcs_plan.py lines 839 and 2564). FR-052 says no
# `sc-git-protocol` file holds it, so these are a known gap that Task 34 does not edit.
KNOWN_HELPER_FILES = {
    "src/superclaude/skills/sc-git-protocol/scripts/vcs.py",
    "src/superclaude/skills/sc-git-protocol/scripts/vcs_plan.py",
    "plugins/superclaude/skills/sc-git-protocol/scripts/vcs.py",
    "plugins/superclaude/skills/sc-git-protocol/scripts/vcs_plan.py",
}


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _has(text: str, *fragments: str) -> None:
    for fragment in fragments:
        assert fragment in text, f"missing text: {fragment!r}"


def _line_starting(text: str, prefix: str) -> str:
    return next(x for x in text.splitlines() if x.startswith(prefix))


def _part_one() -> str:
    text = _text(REF)
    return text[: text.index(PART_TWO)]


def _part_two() -> str:
    text = _text(REF)
    return text[text.index(PART_TWO) :]


def _primitive_files(roots):
    for base in roots:
        for path in sorted(base.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                yield path


def _holders(roots) -> set:
    return {
        path.relative_to(ROOT).as_posix()
        for path in _primitive_files(roots)
        if FLAG.encode() in path.read_bytes()
    }


# --- implement.md: Options row, argument-hint, Will Not (FR-050, FR-053, T-09) -------------
def test_command_options_row_hint_and_will_not_text():
    text = _text(COMMAND)
    hint = re.search(r'^argument-hint: "(.*)"$', text, re.M).group(1)
    assert hint.endswith("[--commit-tasks]")
    rows = [x for x in text.splitlines() if x.startswith("| `--commit-tasks`")]
    assert len(rows) == 1
    _has(
        rows[0],
        "| off |",
        "only when typed by the person in the option prefix",
        "refs/commit-step.md",
    )
    will_not = (
        "- Commit without `--commit-tasks` on the invocation line, push, open PRs, or "
        "release (a managed archive is not any of these)"
    )
    assert will_not in text.splitlines()
    assert "- Auto-commit, open PRs, or release" not in text


# --- STOP rows and the closed-list sentence (FR-070, T-09) ----------------------------------
def test_two_new_stop_rows_and_the_revised_closed_list_sentence():
    skill = _text(SKILL)
    rows = {
        m.group(1): m.group(0)
        for m in re.finditer(r"^\| `(E-[A-Z-]+)` \|.*\|$", skill, re.M)
    }
    width = rows["E-HALT-QA"].count("|")
    for code in ("E-COMMIT-PRECONDITION", "E-COMMIT-REFUSED"):
        assert rows[code].count("|") == width, code
    _has(rows["E-COMMIT-PRECONDITION"], "reason=<token>", "`--commit-tasks` only")
    _has(rows["E-COMMIT-REFUSED"], "reason=<token>", "refs/commit-step.md")
    sentence = _line_starting(skill, "No other `E-*` codes")
    _has(
        sentence,
        "`E-RESUME-NEEDED` being the only one the retry ladder and the commit step's "
        "transient stops add",
        "`E-COMMIT-PRECONDITION` and `E-COMMIT-REFUSED` apply only with the flag or a "
        "`commits.md`",
    )


# --- the ref: size, load rule, the two parts (T-09, NFR-012, NFR-018) -----------------------
def test_commit_step_ref_exists_and_stays_within_250_lines():
    assert REF.is_file()
    assert len(_text(REF).splitlines()) <= REF_LINE_CAP


def test_load_rule_loads_the_ref_for_the_flag_or_a_sidecar_and_otherwise_never():
    rule = _line_starting(_text(SKILL), "Also load `refs/commit-step.md`")
    _has(
        rule,
        "when `--commit-tasks` is present or a `commits.md` exists",
        "otherwise never.",
    )
    intro = _text(REF).splitlines()[2]
    _has(
        intro,
        "Loaded when `--commit-tasks` is on the invocation line or a `commits.md` exists",
        "A run with neither adds no Bash call and writes no file (NFR-018).",
    )


def test_without_the_flag_only_part_one_applies_and_it_makes_no_commit_call():
    text = _text(REF)
    assert text.startswith(PART_ONE) and text.count(PART_TWO) == 1
    one, two = _part_one(), _part_two()
    _has(one, "Nothing in this part makes a commit.")
    for call in ("git commit", "git add", "commit_argv", "add_argv", "--only"):
        assert call not in one, call
    _has(
        two,
        "Nothing in this part runs without `--commit-tasks`, typed by the person in the "
        "option prefix of this invocation (Wave 0 step 5b). An unflagged run uses part "
        "one only and never commits.",
    )
    # inside part one, the actions that make a boundary are for a flagged run only
    _has(one, "`prepare`, `retry`: flagged run only", "(flagged only; no commit)")
    # an unflagged run may only record what git already proves, or append nothing
    _has(one, "An unflagged run appends nothing here.", "(an unflagged run may)")


def test_skill_step_6b_loads_part_one_for_an_unflagged_run_with_a_sidecar():
    step = _line_starting(_text(SKILL), "6b. ")
    _has(step, "Flag present or `commits.md` exists", "`vcs reconcile`")


# --- the protocol never invokes /sc:git (FR-072, T-09) --------------------------------------
INVOCATION_FORMS = (
    re.compile(r"^\s*>\s*Skill\s+sc:git", re.M),
    re.compile(r"\bSkill\s+sc:git-protocol\b"),
    re.compile(r"\bSkill\s*\(\s*['\"]?sc:git"),
    re.compile(r"\b(?:run|invoke|call|execute|type|use)\s+`?/sc:git\b", re.I),
    re.compile(r"^\s*`?/sc:git\b", re.M),
)


@pytest.mark.parametrize(
    "path",
    [COMMAND, SKILL, *sorted((PROTOCOL / "refs").glob("*.md"))],
    ids=lambda p: p.name,
)
def test_protocol_files_never_invoke_sc_git(path):
    text = _text(path)
    for form in INVOCATION_FORMS:
        assert not form.search(text), (path.name, form.pattern)


def test_the_only_mentions_of_sc_git_are_the_known_prose_ones():
    # SKILL.md and implement.md name the command as an optional next step or as out of
    # scope; commit-step.md names it only to contrast `vcs verify` with a plain commit.
    allowed = {
        (SKILL, "optional next steps, not gates"),
        (SKILL, "as required steps"),
        (COMMAND, "optional next steps"),
        (REF, "Unlike a plain commit through `/sc:git`"),
    }
    seen = set()
    for path in (COMMAND, SKILL, *sorted((PROTOCOL / "refs").glob("*.md"))):
        for line in _text(path).splitlines():
            if "/sc:git" in line or "sc:git-protocol" in line:
                matches = [a for a in allowed if a[0] == path and a[1] in line]
                assert matches, (path.name, line[:120])
                seen.update(matches)
    assert seen == allowed


# --- `--commit-tasks` appears only in the FR-052 files (T-15) -------------------------------
def test_flag_string_is_confined_to_the_fr052_files():
    unexpected = {
        name
        for name in _holders(PRIMITIVE_ROOTS)
        if name not in ALLOWED_FILES
        and name not in KNOWN_HELPER_FILES
        and not name.startswith(ALLOWED_PREFIXES)
    }
    assert not unexpected, sorted(unexpected)


def test_no_workflow_issue_task_or_git_text_file_holds_the_flag():
    # `/sc:workflow`, `/sc:issue`, `/sc:task` and `sc-git-protocol` markdown (FR-052)
    holders = _holders(PRIMITIVE_ROOTS)
    for needle in (
        "sc-workflow-protocol/",
        "sc-issue-protocol/",
        "sc-task-protocol/",
        "commands/workflow.md",
        "commands/issue.md",
        "commands/task.md",
        "commands/git.md",
        "sc-git-protocol/SKILL.md",
        "sc-git-protocol/refs/",
    ):
        assert not [h for h in holders if needle in h], needle


def test_the_allowed_files_that_exist_are_the_ones_listed():
    holders = _holders(PRIMITIVE_ROOTS)
    assert holders & ALLOWED_FILES == {
        "src/superclaude/commands/implement.md",
        "src/superclaude/core/WORKER-CONTRACT.md",
        "plugins/superclaude/commands/implement.md",
    }
    assert any(h.startswith(ALLOWED_PREFIXES[0]) for h in holders)
    assert any(h.startswith(ALLOWED_PREFIXES[1]) for h in holders)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "FR-052 and the Task 34 text say no sc-git-protocol file holds the flag, but the "
        "helper scripts vcs.py (docstring line 83, --flag help line 730) and vcs_plan.py "
        "(docstrings, lines 839 and 2564) name it, in src and in the plugin copy. Not "
        "edited in Task 34; remove this mark when those mentions go."
    ),
)
def test_no_sc_git_protocol_file_contains_the_flag():
    holders = {h for h in _holders(PRIMITIVE_ROOTS) if "sc-git-protocol/" in h}
    assert not holders, sorted(holders)


# --- sidecar regexes equal the helper parser table (T-10, FR-100) ---------------------------
def _documented_regexes() -> dict:
    """The backticked `^...$` strings of the Sidecar section, keyed by the form name."""
    names = {
        "- run:": "run",
        "- prepared:": "prepared",
        "- sha or recovered:": "commit",
        "- skipped:": "skipped",
        "- refused or uncertain:": "refused",
        "- abandoned:": "resolved_abandoned",
        "- adopted:": "resolved_adopted",
    }
    found = {}
    section = _text(REF).split("## Sidecar")[1].split("## Segments")[0]
    for line in section.splitlines():
        for head, form in names.items():
            if line.startswith(head):
                match = re.search(r": `(\^.*\$)`$", line)
                assert match, line[:80]
                found[form] = match.group(1)
    return found


def test_documented_sidecar_regexes_equal_sidecar_forms_in_the_helper(monkeypatch):
    documented = _documented_regexes()
    monkeypatch.syspath_prepend(str(HELPER))
    helper = importlib.import_module("vcs_plan")
    assert set(documented) == set(helper.SIDECAR_FORMS)
    for form, pattern in helper.SIDECAR_FORMS.items():
        assert documented[form] == pattern.pattern, form


def test_ref_says_its_regex_strings_are_the_helper_strings():
    sidecar = _text(REF).split("## Sidecar")[1].split("## Segments")[0]
    _has(
        sidecar,
        "Six line forms, one regex each (the same strings as `SIDECAR_FORMS` in the helper)",
        "The two `resolved` forms (owner resolution below), also copied from the helper",
    )


def test_ledger_reference_line_127_is_unchanged():
    # Recorded base: 862384852 holds this text at line 127 of refs/ledger.md.
    lines = _text(LEDGER_REF).splitlines()
    assert lines[126] == (
        "if last line does not match header|start|verdict|ruling|retry|halt|FINAL "
        "regex → E-LEDGER-CORRUPT"
    )


# --- FINAL and the whole-list review judge current delivery files (FR-079, T-24) ------------
def test_managed_final_judges_the_current_contents_of_every_delivery_file():
    qa = _text(QA_REF)
    final = qa[qa.index("## Managed FINAL review (archive gate)") :]
    _has(
        final,
        "Input: the current full plan, the full ledger, and the current contents of every "
        "delivery file the helper's `--print-state` lists",
        "taken from the current files and the package's `./artifacts/` logs, not copied "
        "from the ledger",
    )
    managed = _text(MANAGED_REF)
    _has(
        managed,
        "the current contents of each listed delivery file",
        "the reviewer must read the real current files",
    )


def test_both_finals_judge_the_end_state_and_no_text_routes_through_git_diff_head():
    qa = _text(QA_REF)
    _has(
        qa,
        "This is the single statement for both FINALs (the managed archive FINAL and the "
        "legacy Whole-list review).",
        "FINAL judges the end state, not those lines.",
    )
    for path in (SKILL, QA_REF, MANAGED_REF, REF):
        assert "git diff HEAD" not in _text(path), path.name


def test_commit_position_l0_sits_before_the_whole_list_review_and_the_final():
    _has(
        _part_two(),
        "**L0** after the last task's `complete`, before the whole-list review, the "
        "legacy all-complete stop or the managed FINAL",
    )
    _has(
        _part_one(),
        'do not return "all complete", write no FINAL and do not enter the archive gate',
    )


@pytest.mark.xfail(
    strict=True,
    reason=(
        "T-24 and FR-079 want the legacy whole-list review to judge the current delivery "
        "files, but the 'Legacy sources' paragraph of Whole-list review in SKILL.md says "
        "only 'one reviewer pass vs the full spec + full ledger'; refs/qa.md states it for "
        "the managed FINAL only. Not edited in Task 34."
    ),
)
def test_legacy_whole_list_review_names_the_current_delivery_files():
    skill = _text(SKILL)
    legacy = skill[
        skill.index("**Legacy sources.**") : skill.index("**Managed packages.** Not")
    ]
    _has(legacy, "current", "delivery file")


# --- grant provenance (FR-050, T-25) --------------------------------------------------------
def test_flag_counts_only_when_the_person_typed_it_and_not_person_stops():
    skill = _text(SKILL)
    known = _line_starting(skill, "1. Tokenize")
    _has(
        known,
        "a standalone option-prefix token of a message the person typed that starts with "
        "`/sc:implement`",
    )
    step = _line_starting(skill, "5b. ")
    _has(
        step,
        "`not-person`",
        "`unattended`",
        "STOP `E-COMMIT-PRECONDITION reason=<token>`",
    )


def test_grant_covers_the_ruling_continuation_and_ends_with_the_run():
    grant = _part_two().split("## Grant and positions")[1].split("## Procedure")[0]
    _has(
        grant,
        "The grant covers the later turns of the same run, including the in-chat Ruling "
        "that continues to the next task and context compaction (re-read the ledger and "
        "`commits.md` from disk, never from memory).",
        "It ends with the run; a resume needs the flag again.",
        "A Ruling neither grants nor revokes it, and the executor never types "
        "`--commit-tasks` for the person.",
    )


def test_grant_revocation_appends_a_revoked_off_run_line_and_words_never_widen():
    grant = _part_two().split("## Grant and positions")[1].split("## Procedure")[0]
    _has(
        grant,
        "If the person says in plain words to stop committing, append a `run` line with "
        "`commit-tasks=off reason=revoked` before the next attempt.",
        "Words narrow the grant, never widen it.",
    )
    assert "reason=revoked" in _part_one()


def test_a_stored_on_line_is_evidence_of_what_was_typed_not_proof_of_who_typed_it():
    _has(
        _part_two(),
        "A stored `on` line is evidence of what was typed, not proof of who typed it.",
    )
    _has(
        _part_one(),
        "Every line is appended and flushed before the side effect it announces",
    )


# --- rules the ref states (FR-064, FR-065, FR-122, NFR-014, T-04, T-16, T-21) ---------------
def test_off_run_line_is_appended_once_and_only_when_commits_md_exists():
    step = next(
        x for x in _part_one().splitlines() if x.startswith("3. Append the `run`")
    )
    _has(
        step,
        "Append the `run` line (flagged, or `commits.md` exists)",
        "A run without the flag appends one `off` line, exactly once per invocation and "
        "only when `commits.md` already exists; the first unflagged run with no "
        "`commits.md` creates none.",
    )


def test_refused_line_and_no_retry_in_the_same_run_rule():
    one, two = _part_one(), _part_two()
    _has(one, "There is no automatic retry in the same run.")
    _has(
        two,
        "append `T<ids>: commit refused key=<key> attempt=<n> reason=<reason>`",
        "It never retries in the same run.",
        "`uncertain` (`reason` names the missing proof)",
        "STOP `E-COMMIT-REFUSED reason=uncertain`, never retry.",
        "A later flagged run retries only when reconcile names `retry` (FR-065)",
    )


def test_refusal_output_is_cut_to_the_first_40_lines_and_saved():
    _has(
        _part_two(),
        "It shows at most the first 40 lines of the refusal output, saves them to "
        "`<run-dir>/commit-refused-<n>.log` (legacy) or "
        "`<pkg>/artifacts/commit-refused-<n>.log` (managed)",
    )
    _has(
        _part_one(),
        "a bounded change summary",
        "cut after 40 lines with a count of the rest",
    )


def test_credential_and_auth_prompts_stop_the_run_and_nothing_is_typed():
    _has(
        _part_two(),
        "Stop rather than wait on a signing-credential or authentication prompt "
        "(NFR-014): type no secret, ask for none in chat, never disable signing to avoid it.",
    )


def test_skipped_settlement_is_a_line_and_no_commit():
    two = _part_two()
    _has(
        two,
        "**Skipped settlement.**",
        "`T<ids>: commit skipped key=<key> reason=empty` or `reason=mixed-authorization`",
        "No commit, no other write.",
    )


def test_pins_are_kept_while_a_boundary_is_unsettled_and_an_outside_changed_pin_stays():
    one = _part_one()
    _has(
        one,
        "While a boundary is unsettled, on every run flagged or not, keep all of them for "
        "every member, with its `q0-head` and `q0-branch`",
        "neither the cleanup at `complete` nor the resume cleanup deletes them",
        "A `boundary-wt` pin behind an outstanding `outside-changed` report stays, through "
        "archive, until the owner releases it. A failed delete never undoes a settlement.",
        "Pins are create-once: another target is `pin-conflict`.",
    )


def test_crash_after_the_append_and_two_resumes_give_one_settlement():
    _has(
        _part_one(),
        "Cleanup starts only after the append. A crash after the append is completed by "
        "the next resume",
        "records nothing twice and finishes the cleanup",
        "Two resumes give one settlement, and a repeated reply adds no line and makes no "
        "commit.",
    )


def test_single_key_exception_is_exactly_one_displayed_key():
    one = _part_one()
    _has(
        one,
        "A reply that names no key is a resolution only when exactly one key was displayed "
        "in that STOP; it then means that key.",
        "When two or more keys were displayed, a reply naming no key is ambiguous and is "
        "not a resolution: record nothing, list the displayed keys and show the STOP again.",
        "A unique prefix of a displayed key (at least 12 characters) selects that key.",
        "Only the person's own reply, typed after that STOP in the same conversation, and "
        "it must state an offered choice, `abandon` or `adopt`.",
    )


def test_changed_facts_or_a_busy_worktree_redisplay_the_stop_and_record_nothing():
    _has(
        _part_one(),
        "If `head`, `basis`, `differs` or `choices` differ from what was displayed, or "
        "`quiescent` is not true, record nothing, redisplay the STOP and ask again.",
        "The executor records neither answer while `quiescent` is not true",
    )


# --- the two new transient reasons are listed in the commit ref only (T-09, FR-116) ---------
@pytest.mark.parametrize("reason", ["commit-interrupted", "index-locked"])
def test_new_transient_reason_appears_only_in_the_commit_ref(reason):
    full_form = f"E-RESUME-NEEDED reason={reason}"
    # the grep is on the full form: SKILL.md legitimately carries
    # `E-COMMIT-PRECONDITION reason=index-locked` in step 5b.
    holders = set()
    for path in _primitive_files(PRIMITIVE_ROOTS):
        if path.suffix == ".md" and full_form in _text(path):
            holders.add(path.relative_to(ROOT).as_posix())
    assert holders == {
        "src/superclaude/skills/sc-implement-protocol/refs/commit-step.md",
        "plugins/superclaude/skills/sc-implement-protocol/refs/commit-step.md",
    }
    transient = (
        _part_one()
        .split("## Transient stops (listed here only)")[1]
        .split("## Pins")[0]
    )
    assert f"- `{full_form}`:" in transient


def test_skill_step_5b_keeps_the_precondition_form_of_index_locked():
    step = _line_starting(_text(SKILL), "5b. ")
    assert "`index-locked`" in step and "E-RESUME-NEEDED" not in step


def test_retry_ref_points_at_the_commit_ref_without_naming_the_new_reasons():
    retry = _text(PROTOCOL / "refs/retry.md")
    assert (
        "E-RESUME-NEEDED reason=<reviewer-down|erase-incomplete|ref-failed|adviser-missing>"
        in retry
    )
    for reason in ("commit-interrupted", "index-locked"):
        assert f"reason={reason}" not in retry
    _has(retry, "`refs/commit-step.md` lists them, with the code each one prints")


def test_plugin_copy_of_the_commit_ref_is_byte_identical():
    assert PLUGIN_REF.read_bytes() == REF.read_bytes()


# --- no-flag regression: no `commits.md` is created (T-16), driven through the helper -------
GIT_ENV = {
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.invalid",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.invalid",
    "GIT_TERMINAL_PROMPT": "0",
}


def _git(cwd: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", *args],
        cwd=cwd,
        env={**os.environ, **GIT_ENV},
        capture_output=True,
        text=True,
        check=True,
    )
    return done.stdout.strip()


def _scene(tmp_path: Path, managed: bool):
    """A throwaway repo with one finished task and a ledger in the legacy or managed place."""
    work = tmp_path / "work"
    work.mkdir()
    _git(work, "init", "-q", "-b", "feature/x")
    (work / "a.txt").write_text("a\n", encoding="utf-8")
    _git(work, "add", "a.txt")
    _git(work, "commit", "-q", "-m", "first")
    head = _git(work, "rev-parse", "HEAD")
    header = "# implement ledger — source: ./x.md — created: 2026-10-01T06:30:00Z\n"
    body = (
        f"T1: start sha={head}\n"
        "T1: complete verdict=compliant ac=T1.AC1 evidence=a.txt:1,T1.AC1 "
        "extras=lint:skip,typecheck:skip,test:skip files=a.txt\n"
    )
    if managed:
        slug = "TASK-WF-x-20261001-063000"
        run_dir = work / ".dev/tasks/to-do" / slug
        (run_dir / "artifacts").mkdir(parents=True)
        plan, source = run_dir / f"{slug}.md", run_dir / "source.md"
        plan.write_text("the plan\n", encoding="utf-8")
        source.write_text("the source\n", encoding="utf-8")
        pin = (
            f"PLAN: sha256={hashlib.sha256(plan.read_bytes()).hexdigest()} "
            f"source_sha256={hashlib.sha256(source.read_bytes()).hexdigest()}\n"
        )
        ledger_text = header + pin + body
        sidecar = run_dir / "artifacts/commits.md"
        extra = ["--package", str(run_dir)]
    else:
        run_dir = work / ".dev/implement/x-0a1b2c3d"
        run_dir.mkdir(parents=True)
        ledger_text = header + body
        sidecar = run_dir / "commits.md"
        extra = []
    ledger = run_dir / "progress.md"
    ledger.write_text(ledger_text, encoding="utf-8")
    return work, run_dir, ledger, sidecar, extra


def _reconcile(work, ledger, sidecar, run_dir, extra, flag):
    done = subprocess.run(
        [
            sys.executable,
            str(HELPER / "vcs.py"),
            "reconcile",
            "--cwd",
            str(work),
            "--ledger",
            str(ledger),
            "--sidecar",
            str(sidecar),
            "--run-dir",
            str(run_dir),
            *extra,
            "--flag",
            flag,
        ],
        capture_output=True,
        text=True,
        env={**os.environ, **GIT_ENV, "PYTHONDONTWRITEBYTECODE": "1"},
        timeout=120,
    )
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout)


@pytest.mark.parametrize("managed", [False, True], ids=["legacy", "managed"])
def test_a_run_without_the_flag_and_without_commits_md_creates_none(tmp_path, managed):
    work, run_dir, ledger, sidecar, extra = _scene(tmp_path, managed)
    before = sorted(
        p.relative_to(tmp_path) for p in tmp_path.rglob("*") if ".git" not in p.parts
    )
    ledger_bytes = ledger.read_bytes()
    result = _reconcile(work, ledger, sidecar, run_dir, extra, "off")
    assert (result["status"], result["flag"], result["boundaries"]) == ("ok", "off", [])
    assert result["runs"] == [] and result["managed"] is managed
    assert not sidecar.exists()
    after = sorted(
        p.relative_to(tmp_path) for p in tmp_path.rglob("*") if ".git" not in p.parts
    )
    assert after == before
    assert ledger.read_bytes() == ledger_bytes
