"""Validation-cycle and tests-cycle templates (the roadmap repeats them). Data only."""
from plan_common import (COORD, DEV, L409, L727, LCI, LCODE, LPLAN, MAINT, OWNER, S)

SEVERITY = (
    "Severity rule proposed for the owner to confirm (the owner said 'high/medium' without defining them): "
    "High = a wrong decision shown, a lost or hidden question, a crash or data loss; "
    "Medium = wrong or unclear display or behaviour with a workaround; Low = cosmetic. UNVERIFIED until the owner confirms."
)


def _validation(n, version, under_test, owner_item, with_feedback, first):
    src = f'owner text, item for release {version}'
    feats = []
    feats.append(dict(
        slug="human-test-pass",
        title=f"Release {version}: human test pass of {under_test}",
        source=src,
        why=f"The owner validates every feature and desired behaviour by hand. A written guide makes the pass repeatable and gives each finding evidence." + (" This is the first pass, so the guide is built from the existing SPEC acceptance tests and the user guide." if first else " The guide is the previous cycle's guide plus rows for what changed."),
        links=[L727, "Acceptance tests and live guide on origin/master: `.dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md`, `.dev/issues/409/live-test-guide.md`, `docs/user-guide/observer.md`", LCODE, LPLAN],
        done=[
            "Every capability and every FR of this release has a row in the guide: what to do, expected result, pass or fail, evidence (screenshot or text export).",
            "The owner (or a named tester) ran the whole guide against " + under_test + "; each failure is a finding with steps to reproduce.",
            "Rows that cannot be tested by hand are listed as such with the reason.",
        ],
        who=f"{OWNER} or a tester the owner names; a BMAD session writes the guide.",
        seeds=[
            f"As {OWNER}, I want a step-by-step guide that covers every feature, so that no feature is validated by memory.",
            f"As {OWNER}, I want each failed row to carry evidence, so that bug filing needs no second session.",
        ],
        steps=[
            S("/bmad-agent-tech-writer", f"Write Document (menu WD): a human validation guide for {under_test}, from the SPEC acceptance tests, the user guide and the FRs of this release; one row per capability", "validation guide next to the SPEC", "every capability and FR has a row"),
            S("/bmad-checkpoint-preview", "walk through what changed since the last validated release, from purpose into details (optional, for changed areas)", "walkthrough notes", "changed areas have extra guide rows"),
            S("Run the guide by hand (no command)", f"against {under_test}, record pass or fail with evidence per row", "filled guide", "no row left blank"),
        ],
        handoff="none",
        human="yes (the pass itself is manual)",
        cx="Medium",
    ))
    if with_feedback:
        feats.append(dict(
            slug="feedback-and-feature-requests",
            title=f"Release {version}: capture feedback and feature requests from the test pass",
            source=src + " (feedback/feature requests)",
            why="The owner wants feedback and feature requests collected during validation of the first write and respond features, so release 2.0 is built from them.",
            links=[L727, "Feedback intake: the previous feedback release (EPIC-04) defines the place and the format"],
            done=[
                "Every feedback item and feature request is recorded once with: who, what, where in the dashboard, how often it matters, and a proposed class (bug, change, new feature, question).",
                "The list is the input of EPIC-15 (release 2.0), already sorted for `/bmad-correct-course`.",
            ],
            who=f"{OWNER} and each tester.",
            seeds=[f"As {OWNER}, I want feedback and feature requests collected in one list during validation, so that nothing said in passing is lost before release 2.0."],
            steps=[
                S("/bmad-brainstorming", "session to turn raw feedback from the test pass into a clean list of requests (Facilitator stance; the person supplies the ideas)", "brainstorming session under `_bmad-output/brainstorming/`", "each item has class and evidence"),
                S("/bmad-correct-course", "assess the list's impact on PRD, epics and architecture; produce the change proposal", "`sprint-change-proposal-<date>.md` in `planning-artifacts`", "proposal names what moves into release 2.0 and what waits"),
            ],
            handoff="none",
            cx="Medium",
        ))
    feats.append(dict(
        slug="bug-filing-and-triage",
        title=f"Release {version}: file and triage bugs from the test pass",
        source=src + " (bug filing)",
        why="Findings from the pass become GitHub issues with a severity, so that only high and medium bugs block the release and the rest are recorded.",
        links=[L727, SEVERITY, "Bug issue creation: `/sc:issue --create \"<description>\" --mode bug` (flags read in `~/.claude/commands/sc/issue.md`); the coordinator files, BMAD does not"],
        done=[
            "Every failed guide row is either a filed bug (with severity, steps to reproduce, evidence) or marked not-a-bug with the reason.",
            "Each high or medium bug has a case file (what happens, evidence grade, suspected area) so the fix story can be written without a second investigation.",
            "The bug list is attached to this feature as sub-issues; the count per severity is posted as a comment.",
        ],
        who=f"{OWNER} confirms severity; BMAD investigates; the coordinator files the issues.",
        seeds=[
            f"As {OWNER}, I want each failure filed with a severity and steps to reproduce, so that the fix needs no questions back.",
            f"As {MAINT}, I want an evidence-graded case file for each high or medium bug, so that stories are written from facts.",
        ],
        steps=[
            S("/bmad-investigate", "one case per high or medium finding: the finding text, the build, the evidence; area exploration of `src/superclaude/cli/observe/` as needed", "case files under `_bmad-output/implementation-artifacts/`", "each case file grades its claims Confirmed, Deduced or Hypothesis"),
            S("/sc:issue --create \"<bug description>\" --mode bug --type cli --depth standard", "run by the coordinator, one bug at a time, using the case file as the description (`@path` works for a file)", "GitHub issue and `.dev/issues/<N>/` folder", "issue has the Bug type and the `bug` label; the URL is recorded in the case file"),
        ],
        handoff="none",
        human="yes (severity confirmation by the owner); filing by the coordinator",
        cx="Medium",
    ))
    feats.append(dict(
        slug="fix-high-and-medium-bugs",
        title=f"Release {version}: fix the high and medium bugs",
        source=src + " (bug fixing)",
        why="Only high and medium bugs are fixed in this release; each fix is a story with acceptance criteria that reproduce the bug, plus a regression test.",
        links=[L727, "The bug issues filed by the sibling feature `bug-filing-and-triage`", LCODE],
        done=[
            "One story (or one tight cluster) per high or medium bug, each with Given the reproduction, When the fix is in, Then the correct result; plus an acceptance criterion that a regression test exists.",
            "All stories are done through the IronClaude chain and their bug issues are closed by `/sc:closeout`.",
            "No high or medium bug is open when the release is cut, or the owner has recorded an exception.",
        ],
        who=f"{OWNER} approves the story set; IronClaude workers do the fixes.",
        seeds=[
            f"As {OWNER}, I want every high and medium bug fixed with a test, so that it cannot return unseen.",
            f"As {DEV}, I want the fix released without new surprises, so that I can keep using the dashboard.",
        ],
        steps=[
            S("/bmad-correct-course", "only if a bug shows that a requirement or an architecture invariant was wrong; skip otherwise", "change proposal", "proposal approved or step skipped with a note"),
            S("/bmad-create-epics-and-stories", "stories for the high and medium bugs of this release only; epic number fixed to this EPIC number; Given/When/Then reproduces the bug; one acceptance criterion requires a regression test", "story entries in this release's epic file", "FR coverage map shows every bug covered"),
            S("/bmad-check-implementation-readiness", "", "readiness report", "no blocking gap"),
            S("/bmad-sprint-planning", "", "refreshed `sprint-status.yaml`", "story keys present as `backlog`"),
        ],
        handoff_extra="IronClaude may start a bug story with `/sc:troubleshoot` before `/sc:workflow` (agent 2 decides in shared/CONSENSUS.md); the packet must include the bug's case file.",
        cx="Medium",
    ))
    feats.append(dict(
        slug="release-cut-and-retrospective",
        title=f"Release {version}: cut the release and run the retrospective",
        source=src,
        why="A release is only real when it is recorded, its ledger is closed and the lessons feed the next cycle.",
        links=[L727, "How a dashboard release is recorded (tag, document, version string) is not known yet; the package version in pyproject.toml is 5.0.0, so the dashboard 1.x numbers are a separate scheme (open question Q3 in agent1/RELEASE-PLAN.md S5.2)"],
        done=[
            "`/bmad-sprint-status` (data mode) shows every story of this epic `done` and no `review` or `in-progress` left.",
            f"Release {version} is recorded where the owner decides, with the list of changes.",
            "The retrospective is done; its action items are in `sprint-status.yaml` and are inputs of the next cycle.",
        ],
        who=f"{OWNER}; BMAD facilitates the retrospective.",
        seeds=[f"As {OWNER}, I want the release recorded with what changed, so that the next validation cycle knows what to test."],
        steps=[
            S("/bmad-sprint-status", "data mode: counts and risks for this epic", "status summary", "all stories of this epic `done`"),
            S("/bmad-retrospective", f"retro the epic of release {version}", "retrospective document and action items", "action items have owners"),
        ],
        handoff="none",
        cx="Simple",
    ))
    return dict(
        n=n,
        slug=f"release-{version.replace('.', '-')}-human-validation-and-bug-fixes",
        version=version,
        release=f"Release {version}",
        title=f"Release {version}: human validation, bug filing and fixes",
        schedule="UNSCHEDULED (file only when the owner schedules this release)",
        owner_item=owner_item,
        links=[L727, LPLAN, "Cycle template: validation cycle (agent1/RELEASE-PLAN.md S3.4)", L409],
        done=[
            f"{under_test.capitalize()} is validated by hand against a written guide; every failure is filed or dismissed with a reason.",
            "No high or medium bug is open (or the owner recorded an exception); every fix has a regression test.",
            f"Release {version} is recorded and the retrospective is done.",
        ],
        pickup="Starts only after the owner schedules this release. Inputs: the build under test and the previous cycle's retrospective action items. The next tests cycle uses this epic's bug list.",
        features=feats,
        cx="Complex",
    )


def _tests(n, version, prev_version, prev_epic, owner_item):
    src = f"owner text, item for release {version}"
    feats = [
        dict(
            slug="gap-map",
            title=f"Release {version}: map each escaped bug to the automated check that would have caught it",
            source=src,
            why=f"The owner wants automated tests or CI that would have caught the high and medium bugs of {prev_version} without human validation.",
            links=[L727, f"Input: the high and medium bug list of EPIC-{prev_epic:02d} (release {prev_version})", LCODE, LCI],
            done=[
                "A table: bug, root cause area, the check that would have caught it (unit, golden render, terminal key test, schema test, CI job), why the present suite missed it.",
                "Every high or medium bug of the previous cycle has a row, none is skipped.",
                "Gaps are grouped so each group becomes one story.",
            ],
            who=f"{MAINT} with a BMAD session.",
            seeds=[f"As {MAINT}, I want each escaped bug traced to the missing check, so that new tests target real gaps and not guesses."],
            steps=[
                S("/bmad-investigate", f"area exploration of `tests/observe/` and `.github/workflows/` against the bug list of release {prev_version}", "case file with the gap table", "each row cites path:line or test output"),
                S("/bmad-review-edge-case-hunter", "run on the SPEC and the acceptance tests paths to find paths no test covers", "review report", "findings merged into the gap table"),
            ],
            handoff="none",
            cx="Medium",
        ),
        dict(
            slug="new-automated-tests",
            title=f"Release {version}: add the automated tests the gap map names",
            source=src,
            why="Each gap group becomes tests that fail on the build that contained the bug and pass on the fixed build.",
            links=[L727, LCODE, "Test conventions: `uv run pytest`, `tests/observe/` (golden files, fake runner seam); house rule: UV only, never bare pip"],
            done=[
                "For each gap group, a test exists that fails on the buggy build and passes on the fixed build (shown once, recorded in the story).",
                "The new tests run in the normal suite and in CI.",
            ],
            who=f"IronClaude workers; stories written in a BMAD session.",
            seeds=[f"As {MAINT}, I want a failing-then-passing test for each gap group, so that the same bug cannot return unseen."],
            steps=[
                S("/bmad-create-epics-and-stories", "one story per gap group of the gap map; acceptance criteria: Given the buggy build, When the new test runs, Then it fails; Given the fixed build, Then it passes", "story entries in this release's epic file", "FR coverage map covers every gap group"),
                S("/bmad-check-implementation-readiness", "", "readiness report", "no blocking gap"),
                S("/bmad-sprint-planning", "", "refreshed `sprint-status.yaml`", "story keys present"),
            ],
            handoff_extra="Whether `/bmad-qa-generate-e2e-tests` writes any of these tests or IronClaude's own test conventions do is open (question Q6 in agent1/RELEASE-PLAN.md S5.2); default in these drafts: IronClaude conventions.",
            cx="Medium",
        ),
        dict(
            slug="ci-additions",
            title=f"Release {version}: add the CI checks the gap map names",
            source=src + " (automated tests or CI)",
            why="Some gaps are not tests but missing CI jobs (a check that never runs on a pull request cannot catch anything).",
            links=[L727, LCI, "Gap map from the sibling feature"],
            done=[
                "Each CI gap has a job or an added step in the existing workflows, with the rule it enforces.",
                "A pull request that reintroduces a covered bug fails CI (shown once on a throwaway branch, recorded in the story).",
            ],
            who=f"IronClaude workers; the owner approves any new required check.",
            seeds=[f"As {MAINT}, I want CI to run the checks that catch dashboard regressions on every pull request, so that review does not depend on memory."],
            steps=[
                S("/bmad-create-epics-and-stories", "one story per CI gap; acceptance criteria name the workflow file and the failing case", "story entries", "each story names its workflow file"),
                S("/bmad-check-implementation-readiness", "", "readiness report", "no blocking gap"),
            ],
            cx="Medium",
        ),
        dict(
            slug="regression-set",
            title=f"Release {version}: one regression test per fixed bug, as a standing rule",
            source=src + " (regression tests)",
            why="The owner asked for regression tests as well as new coverage: every fixed bug leaves a named test behind.",
            links=[L727, "Bug issues of the previous cycle"],
            done=[
                "Every high or medium bug fixed in the previous cycle has a regression test whose name or docstring carries the issue number.",
                "The rule 'a bug fix includes its regression test' is written where workers read it (project-context.md and the packet template), not only in an issue.",
            ],
            who=f"IronClaude workers; BMAD records the rule.",
            seeds=[f"As {MAINT}, I want each bug fix to carry its regression test, so that fixed bugs stay fixed."],
            steps=[
                S("/bmad-generate-project-context", "update mode: add the rule 'a bug fix includes a regression test named by its issue number'", "updated `project-context.md`", "rule present once, not duplicated"),
                S("/bmad-create-epics-and-stories", "stories only for fixed bugs that still lack a regression test", "story entries", "each story names its bug issue"),
            ],
            cx="Simple",
        ),
        dict(
            slug="release-cut-and-retrospective",
            title=f"Release {version}: cut the release and run the retrospective",
            source=src,
            why="The release is recorded and lessons feed the next validation cycle.",
            links=[L727, "Where a dashboard release is recorded is not known yet (question Q3 in agent1/RELEASE-PLAN.md S5.2)"],
            done=[
                "Every story of this epic is `done` in `sprint-status.yaml`.",
                f"Release {version} is recorded where the owner decides.",
                "Retrospective done; action items filed as inputs of the next cycle.",
            ],
            who=OWNER,
            seeds=[f"As {OWNER}, I want the tests release recorded with its coverage gains, so that the next validation cycle knows what is now automatic."],
            steps=[
                S("/bmad-sprint-status", "data mode", "status summary", "all stories `done`"),
                S("/bmad-retrospective", f"retro the epic of release {version}", "retrospective", "action items have owners"),
            ],
            handoff="none",
            cx="Simple",
        ),
    ]
    return dict(
        n=n,
        slug=f"release-{version.replace('.', '-')}-automated-tests-and-ci",
        version=version,
        release=f"Release {version}",
        title=f"Release {version}: automated tests and CI that would have caught the high and medium bugs, plus regression tests",
        schedule="UNSCHEDULED (file only when the owner schedules this release)",
        owner_item=owner_item,
        links=[L727, LPLAN, "Cycle template: tests cycle (agent1/RELEASE-PLAN.md S3.4)", LCI],
        done=[
            f"For every high and medium bug of release {prev_version}, an automated check exists that would have caught it without human validation.",
            "Every fixed bug has a regression test.",
            f"Release {version} is recorded and the retrospective is done.",
        ],
        pickup=f"Starts only after the owner schedules this release and EPIC-{prev_epic:02d} has its bug list. Input: the bug list and the case files of release {prev_version}.",
        features=feats,
        cx="Complex",
    )


def cycle_epics():
    return [
        _validation(2, "1.1", "the current version", "Human validation of all features and desired functionality. Filing and fixing bugs for a version 1.1 with any high/medium issues.", False, True),
        _tests(3, "1.105", "1.1", 2, "1.105 release: Additional automated tests or ci needed to have caught any high/medium bugs without needing human validation as well as regression tests"),
        _validation(7, "1.5", "the release 1.4 build", "Human testing, bug filing and fixing for 1 (line break) 5 release (read as 1.5).", False, False),
        _tests(8, "1.505", "1.5", 7, "1.505 release: Additional automated tests or ci needed to have caught any high/medium bugs without needing human validation as well as regression tests"),
        _validation(10, "1.7", "the release 1.6 build", "Human testing, Bug filing a fixing for version 1.7.", False, False),
        _tests(11, "1.705", "1.7", 10, "1.705: Additional automated tests or ci needed to have caught any high/medium bugs without needing human validation as well as regression tests"),
        _validation(13, "1.9", "the release 1.8 build", "Human testing, feedback/feature requests, validation, bug filing and fixing for 1.9 release.", True, False),
        _tests(14, "1.905", "1.9", 13, "1.905: Additional automated tests or ci needed to have caught any high/medium bugs without needing human validation as well as regression tests"),
    ]
