"""Hand-written epics other than EPIC-01 (feedback, Zellij review, build releases). Data only."""
from plan_common import (COORD, DEV, GOAL, L409, L726, L727, LCI, LCODE, LPLAN, LRELATED, MAINT, OWNER, S)
from plan_e01 import epic as epic01

CLOSE = lambda v: S("/bmad-retrospective", f"retro the epic of release {v}", "retrospective and action items", "action items have owners")
STATUS = S("/bmad-sprint-status", "data mode: counts and risks for this epic", "status summary", "all stories of this epic `done`")


def _cut(version, extra_why=""):
    return dict(
        slug="release-cut-and-retrospective",
        title=f"Release {version}: cut the release and run the retrospective",
        source=f"owner text, release {version}",
        why="A release is real when it is recorded, its ledger is closed and the lessons feed the next cycle. " + extra_why,
        links=[L727, "Where a dashboard release is recorded is not known yet (question Q3 in agent1/RELEASE-PLAN.md S5.2)"],
        done=[
            "Every story of this epic is `done` in `sprint-status.yaml`; none is `review` or `in-progress`.",
            f"Release {version} is recorded where the owner decides, with the list of changes.",
            "Retrospective done; action items are inputs of the next cycle.",
        ],
        who=OWNER,
        seeds=[f"As {OWNER}, I want release {version} recorded with what changed, so that the next cycle knows what to test."],
        steps=[STATUS, CLOSE(version)],
        handoff="none",
        cx="Simple",
    )


def e04():
    v = "1.2"
    src = "owner text, item 'Filing Feedback based on current usage with a version 1.2 release'"
    feats = [
        dict(
            slug="feedback-intake",
            title="Release 1.2: collect feedback from current usage in one place",
            source=src, why="The 1.2 release is built from feedback on real use, so the feedback needs one place and one format first.",
            links=[L727, LCODE],
            done=["One place and one format exist for usage feedback (who, what, where in the dashboard, how often it matters).", "At least the feedback the owner already has is entered; each item has a proposed class (bug, change, new feature, question)."],
            who=f"{OWNER} and the developers who use the dashboard.",
            seeds=[f"As {DEV}, I want to leave feedback in a fixed format while I use the dashboard, so that it is not lost in chat."],
            steps=[S("/bmad-brainstorming", "turn raw usage feedback into a clean list (Facilitator stance: the person supplies the ideas)", "brainstorming session under `_bmad-output/brainstorming/`", "each item has class and evidence")],
            handoff="none", cx="Simple"),
        dict(
            slug="feedback-triage-into-plan",
            title="Release 1.2: triage the feedback into the PRD and the release scope",
            source=src, why="Not all feedback belongs in 1.2. The triage decides what is built now, later or never, and records why.",
            links=[L727, LPLAN],
            done=["Each feedback item is: in 1.2, later (with the release), or declined (with the reason).", "The PRD is updated for requirement changes; a change proposal exists for epics and architecture impact."],
            who=f"{OWNER} decides; a BMAD session facilitates.",
            seeds=[f"As {OWNER}, I want each feedback item sorted into now, later or never with a reason, so that the 1.2 scope is deliberate."],
            steps=[S("/bmad-correct-course", "feedback list as the change trigger; assess impact on PRD, epics, architecture, UX", "`sprint-change-proposal-<date>.md`", "proposal approved by the owner"),
                   S("/bmad-prd", "update the PRD for the accepted requirement changes", "updated `prd.md`, `.memlog.md`", "changes logged with reasons")],
            handoff="none", cx="Medium"),
        dict(
            slug="build-the-accepted-feedback",
            title="Release 1.2: build the accepted feedback items",
            source=src, why="The accepted items become stories and are built by IronClaude.",
            links=[L727, LCODE],
            done=["Each accepted item is a story with Given/When/Then criteria and is done through the IronClaude chain.", "The PRD, UX or architecture changes the stories needed are in place before the stories are handed over."],
            who=f"{OWNER} approves the stories; IronClaude workers build.",
            seeds=[f"As {DEV}, I want the accepted feedback built, so that the dashboard fits how I really use it."],
            steps=[S("/bmad-create-epics-and-stories", "stories for the accepted feedback items only; epic number fixed to this EPIC number", "story entries in this release's epic file", "FR coverage map covers every accepted item"),
                   S("/bmad-check-implementation-readiness", "", "readiness report", "no blocking gap"),
                   S("/bmad-sprint-planning", "", "refreshed `sprint-status.yaml`", "story keys present")],
            cx="Medium"),
        _cut(v),
    ]
    return dict(n=4, slug="release-1-2-usage-feedback", version=v, release="Release 1.2",
                title="Release 1.2: feedback from current usage",
                schedule="UNSCHEDULED (file only when the owner schedules this release)",
                owner_item="Filing Feedback based on current usage with a version 1.2 release",
                links=[L727, LPLAN, LCODE], features=feats, cx="Complex",
                done=["Usage feedback is collected, triaged and the accepted items are built.", "Release 1.2 is recorded and the retrospective is done."],
                pickup="Starts after the owner schedules it. Input: the owner's and developers' feedback from using the current version, plus the retrospective of 1.105.")


def e05():
    src = "owner text, item 'Review porting dashboard to Zelij and accessing it directly from Coder Workspace canvas with a new button' (read as Zellij)"
    feats = [
        dict(
            slug="zellij-port-feasibility",
            title="1.3 slot: review porting the dashboard to Zellij",
            source=src, why="The owner wants a review, not a port yet. Issue #606 (closed) holds an earlier Zellij go or no-go, which must be read first.",
            links=[L727, "Prior decision record: issue #606 (visual parity, closed; holds the Zellij go or no-go, per issue 727)", LCODE,
                   "Not known yet: how the terminal dashboard would run inside Zellij (plugin, pane running the existing command, or a rewrite); to be researched, not assumed"],
            done=["A research document states what 'port to Zellij' can mean here (run the existing command in a pane, a Zellij plugin, a rewrite), with effort, benefits, risks and sources for each.", "The earlier go or no-go in #606 is quoted with its reasons and checked against today's facts."],
            who=f"{OWNER} decides; a BMAD research session informs.",
            seeds=[f"As {DEV}, I want the dashboard inside my Zellij layout, so that I see questions beside the coordinator session."],
            steps=[S("/bmad-technical-research", "porting a Python terminal dashboard to Zellij: plugin versus pane, effort, limits; read #606 first", "research document under `_bmad-output/planning-artifacts/research/`", "each option has sources; UNVERIFIED claims labelled")],
            handoff="none", cx="Medium"),
        dict(
            slug="coder-canvas-button",
            title="1.3 slot: review opening the dashboard from the Coder workspace canvas with a new button",
            source=src, why="The owner wants to reach the dashboard directly from the Coder Workspace canvas with a new button.",
            links=[L727, "Not known yet: how a Coder workspace canvas button is defined (template app, link, extension), where the Coder template for this workspace lives, and what the button should open (a web page, a terminal session)"],
            done=["A research document states how a button on the Coder workspace canvas can be added, what it can open, who changes which repository, with sources.", "The dependency between this button and the Zellij review is stated (the button opens what?)."],
            who=f"{OWNER} decides; a BMAD research session informs.",
            seeds=[f"As {DEV}, I want one button on my Coder workspace that opens the dashboard, so that I do not type the command."],
            steps=[S("/bmad-technical-research", "adding a button to a Coder workspace canvas that opens a terminal dashboard; Coder template and app options", "research document", "web search was available; sources listed")],
            handoff="none", cx="Medium"),
        dict(
            slug="go-no-go-record",
            title="1.3 slot: owner go or no-go record for Zellij and the canvas button, and the scope of 1.4",
            source=src + " and 'Planning testing and integration for a 1.4 release'",
            why="Release 1.4 plans testing and integration; its scope depends on this decision, so the decision is a recorded gate and not a chat remark.",
            links=[L727, "House pattern for owner decisions: `.dev/issues/409/owner-decisions-<date>.md`"],
            done=["A dated owner decision record: Zellij go, no-go or later; canvas button go, no-go or later; each with the reason.", "The scope of EPIC-06 is updated to match (features dropped or kept)."],
            who=OWNER,
            seeds=[f"As {OWNER}, I want one decision record, so that release 1.4 plans only what I approved."],
            steps=[S("/bmad-forge-idea", "pressure-test the go case and the no-go case using the two research documents", "optional `forged-idea.md`", "the strongest objection to the chosen option is written down"),
                   S("/bmad-correct-course", "update EPIC-06 scope from the decision (only if the decision removes or adds features)", "change proposal", "EPIC-06 draft matches the decision")],
            handoff="none", cx="Simple"),
    ]
    return dict(n=5, slug="release-1-3-slot-zellij-and-coder-canvas-review", version="1.3", release="Release 1.3 slot (unnumbered in the owner's list)",
                title="Zellij port and Coder workspace canvas button: review and go or no-go",
                schedule="UNSCHEDULED (file only when the owner schedules it)",
                owner_item="Review porting dashboard to Zelij and accessing it directly from Coder Workspace canvas with a new button",
                links=[L727, LPLAN, "#606 (closed; holds the Zellij go or no-go)"], features=feats, cx="Medium",
                done=["Zellij and the canvas button are reviewed with sources.", "The owner has recorded go, no-go or later for each, and EPIC-06 scope matches."],
                pickup="Review only. Nothing is built. The version number of this slot is the draft's reading (owner gave none).",
                loop=False,
                loop_text="Run order: `/bmad-help`, `/bmad-technical-research` (twice), `/bmad-forge-idea`, `/bmad-correct-course`. No stories or hand-off: the output is a decision.")


def e06():
    v = "1.4"
    src = "owner text, item 'Planning testing and integration for a 1.4 release'"
    feats = [
        dict(
            slug="test-and-integration-plan",
            title="Release 1.4: plan the testing and integration",
            source=src, why="The owner lists planning first for 1.4. The plan says what is integrated (Zellij, canvas button, per the go record), how it is tested and in what order.",
            links=[L727, "Input: the go or no-go record of EPIC-05", LCI],
            done=["A test and integration plan names each integration point, the check for each, and the order.", "Stories for the approved integrations exist, ready, with Given/When/Then criteria."],
            who=f"{OWNER} approves; a BMAD session plans.",
            seeds=[f"As {OWNER}, I want the integration and its tests planned before code, so that 1.4 does not discover its test needs late."],
            steps=[S("/bmad-architecture", "update the spine for the approved integration points (new AD ids only)", "updated spine", "reviewer gate passes"),
                   S("/bmad-create-epics-and-stories", "stories for the approved integrations and their tests; epic number fixed to this EPIC number", "story entries", "FR coverage map complete"),
                   S("/bmad-check-implementation-readiness", "", "readiness report", "no blocking gap"),
                   S("/bmad-sprint-planning", "", "refreshed `sprint-status.yaml`", "story keys present")],
            handoff="none", cx="Medium"),
        dict(
            slug="host-the-dashboard-in-zellij",
            title="Release 1.4: run the dashboard in Zellij (only if EPIC-05 says go)",
            source=src, why="Conditional on the owner's go record. If the record says no-go or later, this feature is dropped and its draft is not filed.",
            links=[L727, "Condition: EPIC-05 go record"],
            done=["The dashboard runs in Zellij in the form the go record chose, and its tests from the plan pass."],
            who=f"IronClaude workers after the owner's go.",
            seeds=[f"As {DEV}, I want the dashboard in my Zellij layout, so that questions sit beside the coordinator session."],
            steps=[S("/bmad-create-epics-and-stories", "stories only for the form the go record chose; skip this feature if the record says no-go", "story entries", "stories match the go record")],
            cx="Complex"),
        dict(
            slug="coder-canvas-button-build",
            title="Release 1.4: add the Coder workspace canvas button (only if EPIC-05 says go)",
            source=src, why="Conditional on the owner's go record. The button probably lives in a repository other than IronClaude (Coder templates); that is checked in the plan, not assumed.",
            links=[L727, "Condition: EPIC-05 go record", "Not known yet: which repository holds the Coder template and who may change it"],
            done=["The button opens the dashboard from the Coder workspace canvas; the repository that holds the change is named and the change is made there."],
            who=f"IronClaude workers or the Coder template owner, per the plan.",
            seeds=[f"As {DEV}, I want a button that opens the dashboard, so that I need not remember the command."],
            steps=[S("/bmad-create-epics-and-stories", "stories only for the button form the go record chose; name the repository for each story", "story entries", "each story names its repository")],
            handoff_extra="If the change belongs to another repository, the packet must say so and the coordinator must file the work there under that repository's own rules; this plan does not touch any other repository.",
            cx="Medium"),
        dict(
            slug="integration-tests",
            title="Release 1.4: integration tests for what 1.4 adds",
            source=src, why="The owner wants testing planned for 1.4; the tests are built with the features, not after.",
            links=[L727, LCI, LCODE],
            done=["Each integration point has an automated check, or a documented manual check where automation is not possible, with the reason."],
            who=f"IronClaude workers.",
            seeds=[f"As {MAINT}, I want each new integration covered by a test, so that 1.5 human testing finds fewer basic failures."],
            steps=[S("/bmad-create-epics-and-stories", "stories for the integration checks from the plan", "story entries", "each story names the integration point it covers")],
            cx="Medium"),
        _cut(v),
    ]
    return dict(n=6, slug="release-1-4-test-and-integration", version=v, release="Release 1.4",
                title="Release 1.4: testing and integration (Zellij and Coder canvas, per the EPIC-05 decision)",
                schedule="UNSCHEDULED; conditional on EPIC-05",
                owner_item="Planning testing and integration for a 1.4 release",
                links=[L727, LPLAN], features=feats, cx="Complex",
                done=["The testing and integration plan is written and approved.", "The integrations the owner approved are built and tested; release 1.4 is recorded."],
                pickup="Conditional features are dropped when the EPIC-05 record says no-go or later. The owner's wording names planning only; building is proposed here because a release needs it. Confirm with the owner when scheduling.")


def e09():
    v = "1.6"
    src = "owner text, item 'Review addition screens from initial tui mockups and Clays html dashboards, picking 2-4 more to recreate in TUI for version 1.6'"
    feats = [
        dict(
            slug="screen-review-and-pick",
            title="Release 1.6: review the mockups and Clay's HTML dashboards and pick 2 to 4 screens",
            source=src, why="The owner wants the unused screens from the first TUI mockups and Clay's HTML dashboards reviewed so that two to four are recreated in the TUI.",
            links=[L727, "Mockups on origin/master: `.dev/issues/409/attachments/` (attention-ledger, decision-desk, signal-bridge) and `.dev/issues/409/orca-observer-design-package.zip`; 20 synthetic designs on branch `docs/409-orca-dashboard-designs`", "Clay's HTML dashboards: location not known yet (owner's note); ask the owner", "Rendering rules: `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` (160, 116 and 80 columns)"],
            done=["A candidate list of screens with a screenshot or path each, what the screen shows, what data it needs, and whether the data exists today.", "The owner picked 2 to 4 and recorded the pick in a dated record."],
            who=f"{OWNER} picks; a BMAD UX session (Sally, `/bmad-agent-ux-designer`) supports.",
            seeds=[f"As {OWNER}, I want the candidate screens side by side with their data needs, so that I pick the ones that are worth recreating."],
            steps=[S("/bmad-ux", "review mode: score the candidate screens from the mockups and Clay's HTML dashboards; propose 2 to 4; owner decides", "UX notes and an updated `EXPERIENCE.md` section list", "pick recorded by the owner")],
            handoff="none", cx="Medium"),
        dict(
            slug="ux-contract-for-picked-screens",
            title="Release 1.6: UX contract and acceptance criteria for the picked screens",
            source=src, why="Each picked screen needs a text rendering at the three fixed widths and acceptance criteria before code.",
            links=[L727, "Rendering rules and golden fixtures from the observer visual parity work (#606, closed)"],
            done=["For each picked screen: DESIGN.md and EXPERIENCE.md sections, text mockups at 160, 116 and 80 columns, data fields and their source, empty and error states.", "An independent review passed."],
            who=f"{OWNER} approves; BMAD UX session.",
            seeds=[f"As {DEV}, I want each new screen to render correctly at 160, 116 and 80 columns, so that it works in any terminal width I use."],
            steps=[S("/bmad-ux", "update the UX pair for the picked screens", "`DESIGN.md` and `EXPERIENCE.md`", "text mockups at three widths exist"),
                   S("/bmad-review-adversarial-general", "review the UX pair at its path", "review report", "blocking findings fixed")],
            handoff="none", cx="Medium"),
        dict(
            slug="recreate-picked-screens-in-the-tui",
            title="Release 1.6: recreate the picked screens in the TUI (one story per screen)",
            source=src, why="Each picked screen is built in the existing TUI.",
            links=[L727, LCODE],
            done=["Each picked screen is in the TUI and renders per its mockups at 160, 116 and 80 columns, with golden tests."],
            who=f"IronClaude workers; stories in a BMAD session.",
            seeds=[f"As {OWNER}, I want each picked screen in the TUI, so that I see the information the mockups promised."],
            steps=[S("/bmad-create-epics-and-stories", "one story per picked screen; epic number fixed to this EPIC number; acceptance criteria from the UX contract", "story entries", "each screen has its story"),
                   S("/bmad-check-implementation-readiness", "", "readiness report", "no blocking gap"),
                   S("/bmad-sprint-planning", "", "refreshed `sprint-status.yaml`", "story keys present")],
            cx="Complex"),
        _cut(v),
    ]
    return dict(n=9, slug="release-1-6-more-tui-screens", version=v, release="Release 1.6",
                title="Release 1.6: recreate 2 to 4 more screens from the mockups in the TUI",
                schedule="UNSCHEDULED (file only when the owner schedules this release)",
                owner_item="Review addition screens from initial tui mockups and Clays html dashboards, picking 2-4 more to recreate in TUI for version 1.6",
                links=[L727, LPLAN, L409], features=feats, cx="Complex",
                done=["2 to 4 screens are picked by the owner, specified, and recreated in the TUI.", "Release 1.6 is recorded and the retrospective is done."],
                pickup="The location of Clay's HTML dashboards is not known yet; ask the owner before the first feature.")


def e12():
    v = "1.8"
    src = "owner text, item 'Planning, brainstorming and implementation of first write/Respond features for a 1.8 release'"
    feats = [
        dict(
            slug="coordinator-needs-as-decisions",
            title="Release 1.8: boil the coordinator's needs down to binary, multiple-choice or 'you are needed' decisions",
            source=src, why="The owner wants the coordinators' questions turned into digestible multiple-choice or binary decisions, or a notice that the person is needed in the session for a longer conversation.",
            links=[L727, "Question data today: `src/superclaude/cli/observe/questions.py` (origin/master); the Decision Desk shows questions but cannot answer them", "Owner goal: " + GOAL],
            done=["A catalogue of real coordinator question types taken from real sessions, each classified: binary, multiple choice, needs-the-session (with an example for each).", "For each class, the answer format and what the coordinator does with the answer.", "Questions that fit no class are listed with the reason."],
            who=f"{OWNER} with coordinators' history as evidence; brainstorm plus BMAD session.",
            seeds=[f"As {OWNER}, I want each question type reduced to the smallest answer possible, so that most decisions are one key.", f"As {COORD}, I want to state a question in a fixed shape (options, default, consequence of each), so that the dashboard can show it as a decision."],
            steps=[S("/sc:brainstorm \"turn coordinator questions into binary, multiple-choice or needs-the-session decisions for the dashboard\" --depth deep --research deep --codebase --blind --output .dev/brainstorms/<date>-decision-shapes/", "run ATTENDED in a person's own session; pass real question samples (redacted) and the owner goal", "brainstorm package", "catalogue and classification in the merged result"),
                   S("/bmad-forge-idea", "pressure-test the classification against the questions that fit no class", "optional `forged-idea.md`", "leftover questions have a stated route")],
            handoff="none", cx="Complex"),
        dict(
            slug="write-path-boundary-and-architecture",
            title="Release 1.8: change the read-only boundary: architecture and PRD for the write path",
            source=src + " (write/Respond)", why="The dashboard is read-only by design; two-way needs the rule changed on purpose, with the allowed writes named, not by accident. The 409 spec already holds a future-stage note on write-back.",
            links=[L727, L726, "`.dev/issues/409/bmad/spec-orca-observer/write-back-future-stage.md` (origin/master)", "Observer guide: `docs/user-guide/observer.md` (read-only statement to be changed)"],
            done=["The owner has recorded the boundary change (what writes are allowed: answers to coordinator questions, votes, demands) and what stays forbidden.", "PRD feature groups, the architecture spine (new `AD-n`: allowed writes, who may write, audit record) and the UX are updated and reviewed.", "Issue #726 and `docs/user-guide/observer.md` are on the update list."],
            who=f"{OWNER} decides; BMAD PRD and architecture sessions.",
            seeds=[f"As {MAINT}, I want the list of allowed writes explicit and tested, so that the dashboard can never do more than the owner approved.", f"As {OWNER}, I want every answer given in the dashboard recorded with who and when, so that a decision can be traced."],
            steps=[S("/bmad-prd", "update the PRD for the write path: decision answers, votes, demands, notices", "updated `prd.md`", "feature groups and FRs for the write path exist"),
                   S("/bmad-architecture", "update the spine: the write boundary, allowed writes, audit record (new AD ids)", "updated spine", "reviewer gate passes"),
                   S("/bmad-ux", "decision card and demand menu behaviour: states, errors, confirmation", "updated `EXPERIENCE.md`", "states covered"),
                   S("/bmad-review-adversarial-general", "review PRD, spine and UX at their paths; add `/bmad-review-edge-case-hunter` on the spine", "review reports", "blocking findings fixed")],
            handoff="none", cx="Complex"),
        dict(
            slug="decision-cards-in-the-dashboard",
            title="Release 1.8: decision cards: answer binary and multiple-choice questions in the dashboard",
            source=src, why="First write feature: a person answers a coordinator question with one key.",
            links=[L727, LCODE, L726],
            done=["A question shown as a decision card can be answered with one key; the answer is recorded and shown as answered.", "An answered question is not asked again; a wrong or late answer is handled (stale question, already answered elsewhere)."],
            who=f"IronClaude workers; stories in a BMAD session.",
            seeds=[f"As {OWNER}, I want to answer a binary question with one key, so that I do not open the coordinator terminal.", f"As {OWNER}, I want to choose among options on a card, so that multiple-choice questions are as fast."],
            steps=[S("/bmad-create-epics-and-stories", "stories for decision cards from the PRD feature group; epic number fixed to this EPIC number", "story entries", "FR coverage map complete"),
                   S("/bmad-check-implementation-readiness", "", "readiness report", "no blocking gap"),
                   S("/bmad-sprint-planning", "", "refreshed `sprint-status.yaml`", "story keys present")],
            cx="Complex"),
        dict(
            slug="answer-transport-to-the-coordinator",
            title="Release 1.8: deliver the answer to the coordinator session",
            source=src, why="An answer recorded in the dashboard must reach the coordinator that asked. How an answer is delivered is not known yet and must be researched, not assumed.",
            links=[L727, "Not known yet: the delivery channel (Orca message reply or another); handoff step 1 of the 409 BMAD run lists 'Orca reply sender rule (future stage)' as UNVERIFIED (`.dev/issues/409/bmad/handoff-step1.md`)"],
            done=["The delivery channel is chosen with evidence (a recorded trial), failure cases are handled (coordinator gone, answer too late), and the answer arrives without the person copying text."],
            who=f"IronClaude workers after the owner's go; a research story comes first.",
            seeds=[f"As {COORD}, I want the person's answer delivered to me in a form I can act on, so that the decision is applied without a second question."],
            steps=[S("/bmad-technical-research", "how a decision made outside the coordinator terminal can be delivered into the coordinator session reliably; evidence from the orchestration tool", "research document", "trial result recorded, UNVERIFIED items labelled"),
                   S("/bmad-create-epics-and-stories", "stories for the chosen channel and its failure cases", "story entries", "each failure case has a criterion")],
            handoff_extra="The first story is a trial in a scratch session, never against the owner's live coordinators.",
            cx="Complex"),
        dict(
            slug="you-are-needed-notice",
            title="Release 1.8: a notice when the person is needed in the coordinator session",
            source=src + " (notifications that the user is needed in the coordinator session for a q&a or longer conversation)", why="When a question cannot be reduced to a decision, the dashboard says so and points to the session.",
            links=[L727, LCODE],
            done=["A coordinator question that needs a conversation shows as 'you are needed' with the session to open and why.", "The notice clears when the conversation is done.", "The owner's open question from issue #727 (2026-11-25) is answered or deferred in the record: should longer conversations with a coordinator move into the dashboard too, and in which release."],
            who=f"IronClaude workers; stories in a BMAD session.",
            seeds=[f"As {DEV}, I want a clear notice with the session name when I am needed, so that I go straight there."],
            steps=[S("/bmad-create-epics-and-stories", "stories for the notice and its clearing; epic number fixed to this EPIC number", "story entries", "each state has a criterion")],
            cx="Medium"),
        dict(
            slug="decision-record-in-the-project-database",
            title="Release 1.8: keep decisions in the project database (builds on Release 2 prep)",
            source=src, why="Decisions and answers must persist. This uses the per-project database decided in EPIC-01 and the first schema.",
            links=[L727, "EPIC-01 features `state-persistence-and-storage-evaluation` and `postgres-database-per-project`"],
            done=["Questions, answers and the audit record are stored in the project database; the dashboard shows them after a restart.", "The dashboard still works, read-only and with a notice, when the database is down."],
            who=f"IronClaude workers; schema stories only for tables the story needs.",
            seeds=[f"As {OWNER}, I want my answers to survive a restart, so that no decision is lost."],
            steps=[S("/bmad-create-epics-and-stories", "stories for storing questions, answers and the audit record; each story creates only the tables it needs", "story entries", "readiness check passes")],
            cx="Complex"),
        dict(
            slug="vote-record-from-issue-726",
            title="Release 1.8: fold in the vote on each question (issue 726)",
            source=src, why="Issue #726 is the first small step of this roadmap (a vote on each question, kept as a record). It must be folded in or replaced, not built twice.",
            links=[L726, L727],
            done=["The owner decided whether #726 is built as written, folded into the decision card, or closed as superseded, and the issue says so."],
            who=OWNER,
            seeds=[f"As {OWNER}, I want to record whether an intervention was the right call, so that prompting can be tuned later."],
            steps=[S("/bmad-correct-course", "trigger: issue 726 versus the write-path PRD; decide fold-in or supersede", "change proposal", "owner decision recorded on #726")],
            handoff="none", cx="Simple"),
        _cut(v),
    ]
    return dict(n=12, slug="release-1-8-first-write-and-respond", version=v, release="Release 1.8",
                title="Release 1.8: first write and respond features (decision cards, notices, answer delivery)",
                schedule="UNSCHEDULED (file only when the owner schedules this release)",
                owner_item="Planning, brainstorming and implementation of first write/Respond features for a 1.8 release. This will involve boiling the coordinators needs into digestible multiple choice or binary decisions to the user or notifications that the user is needed in the coordinator session for a q&a or longer conversation",
                links=[L727, L726, LPLAN, LRELATED], features=feats, cx="Complex",
                done=["Coordinator questions are classified into binary, multiple-choice and needs-the-session.", "A person can answer a binary or multiple-choice question in the dashboard, the answer reaches the coordinator and is stored; a needed-in-session notice exists.", "Release 1.8 is recorded and the retrospective is done."],
                pickup="Planning, brainstorming and implementation are all in the owner's text; the first two features are planning and decision features and must pass an independent review before any code story is handed over.")


def e15():
    v = "2.0"
    src = "owner text, item 'Implement feedback from 1.9 and additional write/respond features for 2.0 release'"
    feats = [
        dict(
            slug="absorb-1-9-feedback",
            title="Release 2.0: absorb the feedback and feature requests of 1.9",
            source=src, why="2.0 is built from what 1.9 validation found.",
            links=[L727, "Input: feedback list of EPIC-13", LPLAN],
            done=["Each item of the 1.9 feedback list is in 2.0, later or declined, with the reason; PRD, architecture and epics are updated."],
            who=f"{OWNER} decides; BMAD session.",
            seeds=[f"As {OWNER}, I want 1.9 feedback sorted into the 2.0 scope, so that 2.0 fixes what testers really hit."],
            steps=[S("/bmad-correct-course", "the 1.9 feedback and feature-request list as the trigger", "change proposal", "approved by the owner"),
                   S("/bmad-prd", "update the PRD for accepted changes", "updated `prd.md`", "changes logged")],
            handoff="none", cx="Medium"),
        dict(
            slug="demands-to-the-coordinator",
            title="Release 2.0: demands to the coordinator (more context, explanation, debate, validation, research, fact check, plugins)",
            source=src + " and the goal paragraph", why="When a question cannot be reduced to a decision, the person can send a demand to the coordinator instead of switching terminals: more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of a named plugin or tool (for example ponytail).",
            links=[L727, "Candidate IronClaude commands behind each demand (agent 2 confirms in shared/CONSENSUS.md): `/sc:brainstorm` for a debate of proposals, `/sc:research`, `/sc:adversarial`, `/sc:reflect`; plugin invocation by name"],
            done=["Each demand type has a one-key action, a defined message to the coordinator, an expected result type and a time limit message.", "The result of the demand returns to the dashboard and can lead to the decision."],
            who=f"IronClaude workers; stories in a BMAD session.",
            seeds=[f"As {OWNER}, I want to ask the coordinator for more context with one key, so that I can decide without leaving the dashboard.", f"As {OWNER}, I want to demand a debate of several proposals, so that I see the options argued before I choose.", f"As {OWNER}, I want to demand research or a fact check, so that a claim is verified before I rely on it.", f"As {OWNER}, I want to ask for a named plugin or tool to be used (for example ponytail), so that the coordinator applies the method I trust."],
            steps=[S("/bmad-create-epics-and-stories", "one story per demand type; epic number fixed to this EPIC number", "story entries", "each demand type has a story and criteria"),
                   S("/bmad-check-implementation-readiness", "", "readiness report", "no blocking gap"),
                   S("/bmad-sprint-planning", "", "refreshed `sprint-status.yaml`", "story keys present")],
            cx="Complex"),
        dict(
            slug="cross-coordinator-context-in-the-dashboard",
            title="Release 2.0: show what other coordinators decided (project history in the dashboard)",
            source=src, why="The owner's long-term goal: coordinators and developers of one project see each other's sessions and decisions. This feature surfaces the history organised in EPIC-01.",
            links=[L727, "EPIC-01 feature `session-and-decision-history-across-coordinators`", "Related open issue: #725"],
            done=["A person can see the relevant decisions of other coordinators of the project next to a question, with who and when.", "The history source is the one chosen in EPIC-01."],
            who=f"IronClaude workers; stories in a BMAD session.",
            seeds=[f"As {DEV}, I want to see what another coordinator decided on the same topic, so that I do not answer differently by accident."],
            steps=[S("/bmad-create-epics-and-stories", "stories for showing project history next to a question; epic number fixed to this EPIC number", "story entries", "readiness check passes")],
            cx="Complex"),
        dict(
            slug="more-write-and-respond-features",
            title="Release 2.0: additional write and respond features from the 1.9 feedback",
            source=src + " (additional write/respond features)", why="Whatever write and respond features 1.9 feedback asks for, beyond the demands and history above.",
            links=[L727, "Input: accepted items of `absorb-1-9-feedback`"],
            done=["Each accepted write or respond request is a story and is done through the IronClaude chain."],
            who=f"IronClaude workers; stories in a BMAD session.",
            seeds=[f"As {OWNER}, I want the requests testers raised built, so that 2.0 fits how decisions are really made."],
            steps=[S("/bmad-create-epics-and-stories", "stories for the accepted requests only", "story entries", "FR coverage map complete")],
            cx="Complex"),
        dict(
            slug="release-cut-and-retrospective",
            title="Release 2.0: cut the release, run the retrospective and record what comes after 2.0",
            source=src + " and 'Release 2 and beyond: more user feedback systems used to gather data to fine tune when and how the user is prompted'",
            why="2.0 is recorded. The owner's note about what comes after 2.0 (feedback systems that gather data to tune when and how the person is prompted) is captured as input for the next plan, not planned here.",
            links=[L727, "Where a dashboard release is recorded is not known yet (question Q3 in agent1/RELEASE-PLAN.md S5.2)"],
            done=["Every story of this epic is `done`.", "Release 2.0 is recorded where the owner decides.", "Retrospective done; the beyond-2.0 note is filed as an input for the next roadmap."],
            who=OWNER,
            seeds=[f"As {OWNER}, I want 2.0 recorded and the next direction noted, so that planning continues from facts."],
            steps=[STATUS, CLOSE(v)],
            handoff="none", cx="Simple"),
    ]
    return dict(n=15, slug="release-2-0-feedback-and-more-write-respond", version=v, release="Release 2.0",
                title="Release 2.0: implement the 1.9 feedback and additional write and respond features",
                schedule="UNSCHEDULED (file only when the owner schedules this release)",
                owner_item="Implement feedback from 1.9 and additional write/respond features for 2.0 release",
                links=[L727, LPLAN, L726], features=feats, cx="Complex",
                done=["The accepted feedback of 1.9 is built.", "Demands to the coordinator and project history in the dashboard exist.", "Release 2.0 is recorded and the retrospective is done."],
                pickup="After 2.0 (owner's text): user feedback systems to gather data used to fine tune when and how the person is prompted. Not planned in this plan.")


def unique_epics():
    return [epic01(), e04(), e05(), e06(), e09(), e12(), e15()]
