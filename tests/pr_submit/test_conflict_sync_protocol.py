"""Static protocol tests for the merge-conflict skill text (issue #305).

Covers the skill text of design section 8 (FR-4 to FR-10, FR-14, FR-18 to FR-21,
FR-27 to FR-31, FR-33, NFR-1, NFR-4, NFR-6, NFR-8, NFR-9, NFR-14): the pinned phrases
and order pins of the two new refs, the thirteen `SKILL.md` edits E1 to E13, Tier 2
labelling, repo-scoped `gh` lines, the one `git push` form, the FR-21
prohibited-operation scan, the allowed-tools check, the static call ceilings and the
byte-identical fragments of the spec (design section 12.2, last paragraph).

Skill text is pinned by literal substrings, never by line numbers.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from superclaude.pr_submit.conflicts import MECHANICAL_RULES
from tests.pr_submit.test_static_grep import _GH_CMD, _command_lines, _repo_scoped

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-pr-submit-protocol"
SKILL_MD = SKILL_DIR / "SKILL.md"
COMMAND_MD = REPO_ROOT / "src" / "superclaude" / "commands" / "pr-submit.md"
MECHANICAL_REF = SKILL_DIR / "refs" / "conflict-mechanical.md"
INTENT_REF = SKILL_DIR / "refs" / "conflict-intent.md"
STATE_MACHINE_REF = SKILL_DIR / "refs" / "state-machine.md"
PROBE_SCRIPT = SKILL_DIR / "scripts" / "probe-merge.sh"
FINISH_SCRIPT = SKILL_DIR / "scripts" / "finish-merge.sh"
EVIDENCE_SCRIPT = SKILL_DIR / "scripts" / "collect-conflict-evidence.sh"
POLL_CI_SCRIPT = SKILL_DIR / "scripts" / "poll-ci-checks.sh"

NEW_REFS = (MECHANICAL_REF, INTENT_REF)
NEW_SCRIPTS = (PROBE_SCRIPT, FINISH_SCRIPT, EVIDENCE_SCRIPT)
NEW_FILES = NEW_REFS + NEW_SCRIPTS

PUSH_LINE = "git push origin <target_sha>:<HEAD_BRANCH>"
ALLOWED_PROGRAMS = frozenset({"git", "gh", "uv", "make", "jq"})


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _prose(path: Path) -> str:
    """The file as prose: hand-wrapping and blockquote markers are not the contract."""
    return " ".join(_read(path).replace("\n> ", " ").split())


def _assert_in_order(text: str, needles: tuple[str, ...]) -> None:
    """Each needle is present and its first occurrence follows the previous one's."""
    positions = []
    for needle in needles:
        assert needle in text, f"missing {needle!r}"
        positions.append(text.index(needle))
    for (a, pa), (b, pb) in zip(
        zip(needles, positions), zip(needles[1:], positions[1:])
    ):
        assert pa < pb, f"{a!r} (at {pa}) must come before {b!r} (at {pb})"


# --- Pinned phrases and order pins (design sections 8.2 and 8.3) --------------

MECHANICAL_PINS = (
    "git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit "
    "--no-ff <base_sha>",
    PUSH_LINE,
    "git checkout --ours -- uv.lock",
    "uv lock --check",
    "git add -- uv.lock",
    "merge_parent_ok(<parents>, pre_push_sha, base_sha)",
    "git merge-base --is-ancestor <base_sha> origin/<base>",
    "The deterministic core DECIDES",
    "evaluate_sync_decision",
    "sync_started",
    "reason `pr_conflicting`",
    "--evidence-sha",
    "expect_checks",
    "push_rejected",
    "push_failed",
    "git revert -m 1 <merge_sha>",
    "Nothing was changed and nothing was pushed.",
    "never stash",
)


@pytest.mark.parametrize("phrase", MECHANICAL_PINS)
def test_conflict_mechanical_pinned_phrases(phrase):
    assert phrase in _read(MECHANICAL_REF), phrase


def test_conflict_mechanical_order_pins():
    """The head check and `merge_preflight_ok` come before `sync_started`, which comes
    before the merge command; the head re-read comes before `merge_parent_ok`, before
    `--is-ancestor`, before "The deterministic core DECIDES", before the push line."""
    text = _read(MECHANICAL_REF)
    merge_cmd = "merge --no-commit --no-ff <base_sha>"
    _assert_in_order(text, ("**Step 1. Head check.**", "sync_started", merge_cmd))
    _assert_in_order(text, ("merge_preflight_ok", "sync_started", merge_cmd))
    _assert_in_order(
        text,
        (
            "**Step 10(a). Head re-read.**",
            "merge_parent_ok(<parents>, pre_push_sha, base_sha)",
            "--is-ancestor",
            "The deterministic core DECIDES",
            PUSH_LINE,
        ),
    )


INTENT_PINS = (
    "scripts/collect-conflict-evidence.sh",
    "evidence-validator",
    "One revision pass",
    "one sentence",
    "dropped",
    "high-suspicion",
    "configured reviewers",
    "base_authored",
    "git add -- <path>",
    "git rm -- <path>",
)

RECORD_FIELDS = (
    "kind",
    "root_cause",
    "ours_intent",
    "theirs_intent",
    "resolution",
    "behavior_after",
    "dropped",
    "evidence",
)


@pytest.mark.parametrize("phrase", INTENT_PINS)
def test_conflict_intent_pinned_phrases(phrase):
    assert phrase in _read(INTENT_REF), phrase


def test_conflict_intent_record_fields_in_order():
    """Section 6 lists the record fields in the order the core parses them, and the
    example section follows the same order."""
    text = _read(INTENT_REF)
    section = text[text.index("## 6. The resolution record") :]
    section = section[: section.index("\n## 7.")]
    _assert_in_order(
        section, ("`## <path>`",) + tuple(f"`{f}:`" for f in RECORD_FIELDS)
    )
    example = section[section.index("> ## ") :]
    _assert_in_order(example, tuple(f"\n> {f}: " for f in RECORD_FIELDS))


# --- SKILL.md edits E1 to E13 (design section 8.1) ----------------------------

SKILL_EDITS = {
    "E1": (
        "| `--conflict-max-tier {0,1,2}` | No (default 1) | Highest merge-conflict tier "
        "the skill may act on: 0 detect and report only, 1 also regenerate a conflicted "
        "root `uv.lock` (Tier 1), 2 also resolve text conflicts by stated intent (Tier 2, "
        "off by default). Tier 3 never resolves. |",
    ),
    "E2": (
        "**STOP** if `--monitor >= 1` and the PR cannot be confirmed on the resolved "
        "target repo (origin's\n`owner/repo`, parsed from `git remote get-url origin`): "
        "a wrong origin, or a returned URL whose `owner/repo` ≠ the resolved target → "
        "HALT,\ninstruct the operator to close the misrouted PR. Being behind the base "
        "branch is not a STOP at L1+:\nWave 0 reports how many commits behind (Tier 0) "
        "and the conflict check below classifies any conflict.",
    ),
    "E3": (
        "| `push_count` | int | Landed fix, CI and Tier 2 merge pushes (`kind` on every "
        "push record; Tier 1 sync pushes are counted in `sync_push_count`); `<= "
        "max_rounds + 1` with the fallback's single push; 0 below L3. |",
        "| `sync_tier` | int or null | Highest merge-conflict tier seen this run (0 to 3; "
        "null when it could not be classified). |",
        "| `sync_outcome` | enum | `none` / `report_only` / `left_in_progress` / "
        "`pushed` / `aborted` / `halted`. |",
        '| `sync_push_count` | int | Landed Tier 1 sync pushes (`kind: "sync"`, at most '
        "`SYNC_CAP = 1`); never counted in `push_count`. |",
    ),
    "E4": (
        "Wave 0c: (L1+) conflict check + report      ← loads refs/conflict-mechanical.md "
        "ONLY when the probe runs",
        "C-initial: (L3, Tier 2) merge cycle before the first review poll ← loads "
        "refs/conflict-mechanical.md + refs/conflict-intent.md",
        "Wave 8a: (L1+) act on a conflict before the CI wait ← loads "
        "refs/conflict-mechanical.md ONLY when the probe runs",
    ),
    "E5": (
        "and rebase if behind `origin/<base>` only at L0 (at L1+ the create path does not "
        "rebase and does not halt: the branch is already published when `gh pr create` "
        "runs, so report how many commits it is behind, a Tier 0 result; with `--pr "
        "<N>`, at any level, do not rebase: the PR head is already published, so report "
        "how many commits it is behind instead). At L1+, also before creating or "
        'attaching, run `scripts/probe-merge.sh --ops-only --repo "$REPO"`: a non-null '
        "`foreign_op` (a merge, rebase, cherry-pick, revert or sequencer operation in "
        "progress) → HALT before Wave 1 with status `terminal_halted`, reason "
        "`foreign_op_in_progress`, nothing created (on `--resume`, "
        "`conflict_resume_plan` in `refs/conflict-mechanical.md` decides first).",
    ),
    "E6": (
        "- **Wave 0 conflict check (L1+ only; L0 skips it):** after the head binding, "
        'read `gh pr view <N> --repo "$REPO" --json '
        "baseRefName,mergeable,mergeStateStatus` (re-read an `UNKNOWN` up to 3 times, "
        "10 s apart) and normalise it with "
        "`superclaude.pr_submit.conflicts.mergeability_hint`. Only `conflicting` or a "
        "persistent `unknown` loads `refs/conflict-mechanical.md` and runs "
        "`scripts/probe-merge.sh`; follow that ref to classify, print the plan before "
        'any edit, and route with `conflict_action(hook="wave0")` (Tier 3 at L3 halts '
        "here: `terminal_halted`, reason `conflict_tier3`, nothing touched). Any other "
        'hint is Tier 0: report "<N> commits behind, no conflicts" (or the `BLOCKED` '
        "reason) and continue; no ref is loaded.",
    ),
    "E7": (
        "`--monitor 0` remains no-monitor. **C-initial (L3, Tier 2, only when Wave 0 "
        "planned it under `--conflict-max-tier 2`):** after arming and before the first "
        "review poll, load `refs/conflict-intent.md` and run the Tier 2 merge cycle of "
        "`refs/conflict-mechanical.md` through `transition(S2_CLASSIFY, "
        '"conflicting")`; its S5 wait is the run\'s first review wait.',
    ),
    "E8": (
        "AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) or "
        "is a Tier 2 merge cycle (push kind `merge`; "
        "`superclaude.pr_submit.fsm.should_retrigger`), post",
    ),
    "E9": (
        "load `refs/ci-poll.md`, then run Wave 8a (below) before the CI poll loop. "
        "These are",
        "classify_checks(payload, wait_sha=<sha at flip or last push>, "
        "expect_checks=<the value recorded for that push, else false>)",
        "without fetching logs, editing, or pushing a fix; the single Tier 1 sync push "
        "of Wave 8a (`SYNC_CAP = 1`) is the only push a wait-only path allows, and it is "
        "not a fix.",
        "so this push too carries only the cycle's one fix commit; its triad passes "
        '`push_kind="ci"`, `review_terminal` and `expect_checks=True`.',
        "Only parsed empty required **and** all-checks lists, with `expect_checks` "
        "false, prove there are no Actions; with `expect_checks` true an empty list is "
        "`polling`, and expiry is the CI timeout with reason `ci_not_started`, never "
        "clean.",
    ),
    "E10": (
        "- **Wave 8a (L1+, conflict act before the CI wait; same entry outcomes as Wave "
        '8):** read `gh pr view <N> --repo "$REPO" --json '
        "baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,"
        "isCrossRepository` (same `UNKNOWN` re-reads). Only `conflicting` or a "
        "persistent `unknown` loads `refs/conflict-mechanical.md`, re-probes and acts on "
        '`conflict_action(hook="wave8a", entering=<review outcome>)`: at L3 a Tier 1 '
        "conflict becomes one sync merge commit pushed fast-forward (no round, no "
        "re-trigger, no reply, no resolve; the one push a wait-only path allows), then "
        "the CI wait runs on the new head with `expect_checks`; L2 leaves it resolved "
        "and validated but uncommitted (`halt_before_push`, only after `clean` / "
        "`REPORT_ONLY`); L1 proposes (also only after `clean` / `REPORT_ONLY`). A PR "
        "still conflicting with nothing pushed skips the CI wait with reason "
        "`pr_conflicting` (GitHub runs no `pull_request` checks on it) and ends with the "
        "status `conflict_action` returns. When any hook this run read `conflicting`, "
        "re-read `mergeable` before sending `transition(clean)`; `CONFLICTING` → "
        "`terminal_halted`, reason `late_conflict` (late re-sync: #361).",
    ),
    "E11": (
        "- Detect merge conflicts at Wave 0 (L1+), report the tier and plan before any "
        "edit, and resolve only within `--conflict-max-tier` and the ordinal ceiling, "
        "publishing a resolution only as one merge commit of the recorded base tip, "
        "pushed fast-forward.",
        "- Rebase a published PR head (at L1+ the create path no longer rebases), stash, "
        "take one side for a whole tree, commit a merge without "
        "`scripts/finish-merge.sh`, or push a merge commit whose parents are not exactly "
        "the PR head and the recorded base tip (`merge_parent_ok`).",
    ),
    "E12": (
        "| Wrong origin / wrong-owner URL | HALT; instruct operator to close the "
        "misrouted PR (FM-11). |",
        '| Behind base branch (create path at L1+, or `--pr`) | Tier 0 report ("<N> '
        'commits behind"); no rebase, no halt. At L0 the create path still rebases. |',
        "| A merge, rebase, cherry-pick, revert or sequencer operation is in progress "
        "(L1+) | `terminal_halted`, reason `foreign_op_in_progress`, before anything is "
        "created; finish or abort that operation yourself, then re-run. |",
        "| Merge conflict that needs a human (Tier 3: submodule, symlink, mode change, "
        "protected or migration path, binary, lock or generated file without a rule, "
        "more than 8 text files, unclassifiable) | L3: `terminal_halted` at the end of "
        "Wave 0, reason `conflict_tier3`, nothing touched or pushed; L1/L2: reported and "
        "the run continues; HALT message from `refs/conflict-mechanical.md`. |",
        "| A conflict cycle stops (dirty tree, foreign merge, guard, finish gate, VAL, "
        "rejected or failed push) | `terminal_halted` with the reason from "
        "`refs/conflict-mechanical.md` (`merge_preflight_dirty`, `sync_*`, "
        "`push_rejected`, `push_failed`); nothing pushed unless the message says the "
        "push landed; never stash, never discard your files. |",
    ),
    "E13": (
        "(push if you are ahead; `git pull --ff-only` if you are behind; this skill "
        "never rewrites a published branch)",
    ),
}


@pytest.mark.parametrize("edit", sorted(SKILL_EDITS, key=lambda e: int(e[1:])))
def test_skill_edit_present(edit):
    text = _read(SKILL_MD)
    for fragment in SKILL_EDITS[edit]:
        assert fragment in text, f"{edit}: missing {fragment!r}"


def test_skill_edits_cover_e1_to_e13():
    assert sorted(SKILL_EDITS, key=lambda e: int(e[1:])) == [
        f"E{i}" for i in range(1, 14)
    ]


def test_skill_replaced_text_is_gone():
    """E5 and E13 replaced their old substrings; E13's force-push sentence is absent
    from the head-binding bullet."""
    text = _read(SKILL_MD)
    assert "and rebase if behind `origin/<base>` (with `--pr <N>`" not in text
    binding = text[text.index("**Wave 0 head binding (L1+ only") :]
    binding = binding[: binding.index("\n- **Wave 0 conflict check")]
    assert "needs a force-push" not in binding


def test_skill_keeps_one_python_block():
    fences = [
        line for line in _read(SKILL_MD).splitlines() if line.startswith("```python")
    ]
    assert len(fences) == 1


# --- Tier 2 labelling and where the evidence script is named -------------------

# Pre-existing SKILL.md lines that name `evidence-validator` for finding verification
# (Waves 2-3); they predate the conflict text and are not Tier 2 text.
_PRE_EXISTING_VALIDATOR_LINES = (
    "read-only evidence-validator before diagnosis or edits.",
    "- **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent",
)


def test_intent_and_validator_lines_say_tier_2():
    offenders = []
    for path in (SKILL_MD, MECHANICAL_REF):
        for lineno, line in enumerate(_read(path).splitlines(), 1):
            if "conflict-intent.md" not in line and "evidence-validator" not in line:
                continue
            if path == SKILL_MD and "conflict-intent.md" not in line:
                if any(old in line for old in _PRE_EXISTING_VALIDATOR_LINES):
                    continue
            if "Tier 2" not in line:
                offenders.append(f"{path.name}:{lineno}: {line.strip()}")
    assert not offenders, "lines without a Tier 2 label:\n" + "\n".join(offenders)
    # The pre-existing exemptions still match real lines (no stale exemption).
    skill = _read(SKILL_MD)
    for old in _PRE_EXISTING_VALIDATOR_LINES:
        assert old in skill, old


def test_evidence_script_named_only_in_conflict_intent():
    name = "collect-conflict-evidence.sh"
    assert name in _read(INTENT_REF)
    surfaces = [COMMAND_MD] + [
        p
        for p in sorted(SKILL_DIR.rglob("*"))
        if p.is_file() and p.suffix in {".md", ".sh"}
    ]
    offenders = [
        str(p.relative_to(REPO_ROOT))
        for p in surfaces
        if p not in (INTENT_REF, EVIDENCE_SCRIPT) and name in _read(p)
    ]
    assert not offenders, offenders


# --- gh scoping and the one push form ----------------------------------------

# A pre-existing error message in poll-ci-checks.sh (unchanged from master) quotes
# `gh pr checks` inside a `die` string; it is text printed to the operator, not a gh
# call. Exempted by exact content so any new unscoped gh line still fails.
_GH_MESSAGE_LINES = {
    POLL_CI_SCRIPT: (
        "*) die \"installed gh lacks 'gh pr checks --json' (see 'gh --version'); "
        "upgrade gh and confirm via 'gh pr checks --help' before CI wait\" 2 ;;",
    ),
}


def test_gh_command_lines_are_repo_scoped():
    offenders = []
    for path in NEW_REFS + (
        PROBE_SCRIPT,
        FINISH_SCRIPT,
        EVIDENCE_SCRIPT,
        POLL_CI_SCRIPT,
    ):
        exempt = _GH_MESSAGE_LINES.get(path, ())
        for lineno, line in _command_lines(path):
            if not _GH_CMD.search(line) or _repo_scoped(line):
                continue
            if line.strip() in exempt:
                continue
            offenders.append(f"{path.name}:{lineno}: {line.strip()}")
    assert not offenders, "unscoped gh command lines:\n" + "\n".join(offenders)
    for path, lines in _GH_MESSAGE_LINES.items():
        stripped = {line.strip() for _n, line in _command_lines(path)}
        for line in lines:
            assert line in stripped, f"stale exemption in {path.name}: {line!r}"


def test_every_git_push_in_new_files_is_the_one_form():
    seen = 0
    for path in NEW_FILES:
        for match in re.finditer(r"git push[^`\n]*", _read(path)):
            assert match.group(0).strip() == PUSH_LINE, (path.name, match.group(0))
            seen += 1
    assert seen >= 1


# --- FR-21 prohibited-operation scan -----------------------------------------

PROHIBITED_OPERATIONS = (
    r"\bgit\s+stash\b",
    r"--no-verify\b",
    r"--amend\b",
    r"\badd\s+(-A|--all|\.)(\s|$|`)",
    r"--(ours|theirs)\s+(--\s+)?\.(\s|$|`)",
    r"\bcheckout\s+--(ours|theirs)\s*(`|$)",
    r"-X\s*(ours|theirs)\b",
    r"-s\s+ours\b",
    r"\breset\s+--hard\b",
    r"\bcommit\s+--only\b",
    r"\bcommit\s+(-a|--all)\b",
    r"\bgit\s+config\b",
    r"\bgit\s+worktree\b",
    r"\bgit\s+rebase\b",
    r"rerere\.enabled=true",
)
_CHECKOUT_OR_SWITCH = re.compile(r"\bgit\s+(checkout|switch)\b")
_ONLY_CHECKOUT = "git checkout --ours -- uv.lock"


def prohibited_operation_hits(path: Path) -> list[str]:
    """Every FR-21 hit in ``path``: one entry per regex match, plus every
    `git checkout` / `git switch` that is not exactly the one lock-file checkout."""
    text = _read(path)
    hits = []
    for pattern in PROHIBITED_OPERATIONS:
        for match in re.finditer(pattern, text, flags=re.MULTILINE):
            lineno = text.count("\n", 0, match.start()) + 1
            hits.append(f"{path.name}:{lineno}: {pattern} -> {match.group(0)!r}")
    for match in _CHECKOUT_OR_SWITCH.finditer(text):
        if not text.startswith(_ONLY_CHECKOUT, match.start()):
            lineno = text.count("\n", 0, match.start()) + 1
            hits.append(f"{path.name}:{lineno}: checkout/switch -> {match.group(0)!r}")
    return hits


def test_prohibited_operation_patterns_catch_each_form():
    """Each regex catches its forbidden form and passes the allowed lock checkout."""
    forms = (
        "git stash push",
        "git commit --no-verify",
        "git commit --amend",
        "git add -A",
        "git checkout --theirs -- .",
        "`git checkout --ours`",
        "git merge -Xours main",
        "git merge -s ours main",
        "git reset --hard HEAD",
        "git commit --only -- f",
        "git commit -a",
        "git config user.name x",
        "git worktree add ../x",
        "git rebase main",
        "git -c rerere.enabled=true merge",
    )
    for pattern, form in zip(PROHIBITED_OPERATIONS, forms):
        assert re.search(pattern, form, flags=re.MULTILINE), (pattern, form)
    for pattern in PROHIBITED_OPERATIONS:
        assert re.search(pattern, _ONLY_CHECKOUT, flags=re.MULTILINE) is None, pattern
    assert _CHECKOUT_OR_SWITCH.search("git switch main")


@pytest.mark.parametrize("path", NEW_FILES, ids=lambda p: p.name)
def test_fr21_prohibited_operation_scan(path):
    hits = prohibited_operation_hits(path)
    assert not hits, "prohibited operations:\n" + "\n".join(hits)


def test_the_only_checkout_is_the_lock_file_seed():
    found = [
        (path.name, m.group(0))
        for path in NEW_FILES
        for m in _CHECKOUT_OR_SWITCH.finditer(_read(path))
    ]
    assert found == [("conflict-mechanical.md", "git checkout")]


# --- NFR-8: no source-tree paths in installed text ---------------------------


@pytest.mark.parametrize(
    "path", NEW_FILES + (SKILL_MD, COMMAND_MD), ids=lambda p: p.name
)
def test_no_src_superclaude_path(path):
    assert "src/superclaude" not in _read(path)


# --- Allowed tools -------------------------------------------------------------


def _fenced_first_words(path: Path) -> list[str]:
    return [line.split()[0] for _n, line in _command_lines(path) if line.strip()]


def test_allowed_tools_cover_every_program():
    """Every `MECHANICAL_RULES` argv[0] and the first word of every fenced command
    line in the two refs is git, gh, uv, make, jq or a `scripts/` path, and each of
    those programs is granted as `Bash(<prog> *)` in the SKILL front matter."""
    front = _read(SKILL_MD).split("\n---\n", 1)[0]
    tools_line = next(
        line for line in front.splitlines() if line.startswith("allowed-tools:")
    )
    granted = set(re.findall(r"Bash\((\S+) \*\)", tools_line))
    programs = set()
    for rule in MECHANICAL_RULES:
        programs.add(rule.regenerate[0])
        if rule.check:
            programs.add(rule.check[0])
    scripts = set()
    for path in NEW_REFS:
        for word in _fenced_first_words(path):
            if word.startswith("scripts/"):
                scripts.add(word)
            else:
                programs.add(word)
    assert programs <= ALLOWED_PROGRAMS, programs - ALLOWED_PROGRAMS
    assert programs <= granted, programs - granted
    for script in scripts:
        assert (SKILL_DIR / script).is_file(), script


# --- NFR-14 static call ceilings -------------------------------------------------


def test_static_call_ceilings_in_conflict_mechanical():
    """One probe command, one `finish-merge.sh` commit-mode command, one push."""
    lines = [line.strip() for _n, line in _command_lines(MECHANICAL_REF)]
    probes = [line for line in lines if "scripts/probe-merge.sh" in line]
    finish_commit = [
        line
        for line in lines
        if "scripts/finish-merge.sh" in line and "--precheck" not in line
    ]
    pushes = [line for line in lines if re.search(r"\bgit\s+push\b", line)]
    assert len(probes) == 1, probes
    assert len(finish_commit) == 1, finish_commit
    assert "--message-file" in finish_commit[0]
    assert pushes == [PUSH_LINE]


# --- Byte-identical spec fragments (design section 12.2, last paragraph) ---------


def test_spec_byte_identical_fragments_survive():
    skill = _read(SKILL_MD)
    assert "with `--pr <N>`, at any level, do not rebase" in skill
    assert "rebase if behind `origin/<base>`" in skill
    wave6 = skill[skill.index("- **Wave 6 (L3 only):**") :]
    wave6 = wave6[: wave6.index("\n- **Wave 6b")]
    for fragment in (
        "pr_head_ok(<local branch>, pre_push_sha,",
        "push_parent_ok(<parents>, pre_push_sha)",
        "The deterministic core DECIDES",
        "then set `pre_push_sha := target_sha`",
    ):
        assert fragment in wave6, fragment
    assert "push any commit besides the cycle's one fix commit" in _read(COMMAND_MD)
    machine = _prose(STATE_MACHINE_REF)
    assert "the commit to push must have exactly one parent, that same SHA" in machine
    assert "The parent check applies only when the cycle applied edits" in machine
