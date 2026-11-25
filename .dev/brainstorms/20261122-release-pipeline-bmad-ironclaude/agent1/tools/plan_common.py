"""Shared helpers and link strings for the issue-draft data. No em dashes."""


def S(cmd, say, out, done):
    """One BMAD (or IronClaude) invocation step."""
    return {"cmd": cmd, "say": say, "out": out, "done": done}


L727 = "Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)"
L726 = "Related: #726 (a vote on each question, kept as a local record; the owner ruled in chat on 2026-11-22 that the read-only rule is relaxed and the dashboard is meant to become two-way; the vote waits for the architecture and storage evaluation in #727)"
L409 = (
    "BMAD precedent on origin/master: `.dev/issues/409/bmad/` (prd-orca-observer, ux-orca-observer, "
    "architecture-orca-observer, spec-orca-observer with SPEC.md and 11 companions, final-review, "
    "handoff-step1.md to handoff-step5.md, `final-review/workflow-input.md`)"
)
LPLAN = (
    "Plan and pipeline text: `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md` "
    "and `shared/CONSENSUS.md`"
)
LCODE = (
    "Observer code on origin/master: `src/superclaude/cli/observe/` (view.py, questions.py, commands.py, "
    "export.py, adapter.py, collector.py, keys.py, snapshot.schema.json), tests in `tests/observe/`, "
    "guide `docs/user-guide/observer.md`"
)
LCI = "CI workflows today: `.github/workflows/test.yml`, `boundary-guard.yml`, `contract3-generator-constraint-lint.yml`"
LRELATED = "Related open issues: #409 (TUI dashboard), #706 (observer follow-up), #604 (observer remote fleet), #716 (coordinator next release), #717 (issue watcher), #718 (dashboard items from the 655 split)"

GOAL = (
    "owner goal: the dashboard replaces talking to the coordinator sessions directly; it is the one place "
    "where the person reads and answers everything the coordinators need (release 1.8 is where responses "
    "and answers start going through the dashboard to the coordinator); decisions are made there, with as "
    "many coordinator questions as possible reduced to binary or multiple-choice questions, and when that "
    "fails, demands to the coordinator for more context, a better explanation, a debate of several "
    "proposals, extra validation, research, fact checking, or use of specific plugins or tools (for "
    "example ponytail)"
)

OWNER = "the owner (supervises the coordinators and makes the decisions)"
DEV = "a developer who runs coordinator sessions and uses the dashboard"
COORD = "a coordinator agent"
MAINT = "the maintainer of IronClaude"
