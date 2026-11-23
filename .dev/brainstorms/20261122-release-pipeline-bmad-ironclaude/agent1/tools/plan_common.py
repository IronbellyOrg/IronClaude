"""Shared helpers and link strings for the issue-draft data. No em dashes."""


def S(cmd, say, out, done):
    """One BMAD (or IronClaude) invocation step."""
    return {"cmd": cmd, "say": say, "out": out, "done": done}


L727 = "Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)"
L726 = "Related: #726 (a vote on each question, kept as a local record; its open decision is whether the read-only rule may be relaxed)"
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
    "owner goal: the dashboard does not replace talking to the coordinator sessions; it is where "
    "decisions are made, with coordinator questions reduced to binary or multiple choice where possible"
)

OWNER = "the owner (supervises the coordinators and makes the decisions)"
DEV = "a developer who runs coordinator sessions and uses the dashboard"
COORD = "a coordinator agent"
MAINT = "the maintainer of IronClaude"
