"""EPIC-01 Release 2 prep. Data only."""
from plan_common import (COORD, DEV, GOAL, L409, L726, L727, LCODE, LPLAN, LRELATED, MAINT, OWNER, S)

SRC = 'owner text, paragraph "Release 2 prep" and "Deliverable 1"'


def epic():
    feats = [
        dict(
            slug="baseline-and-usage-evaluation",
            title="Release 2 prep: evaluate the current dashboard and set the BMAD project baseline",
            source=SRC + " (first step: usage and evaluation of the current version)",
            why="The owner wants the evaluation of the current version first, so the two-way design starts from observed facts, not from assumptions.",
            links=[L727, LCODE, "User guide on origin/master: `docs/user-guide/observer.md` (states the dashboard never approves, retries, terminates, dispatches, merges or messages)", L409],
            done=[
                "`project-context.md` exists, points to CLAUDE.md for house rules instead of copying them, and lists only what BMAD workflows need (UV only, fork-only PR rule, `.dev/tasks/` staged, no `.claude/` staging).",
                "A case file from `/bmad-investigate` grades each finding Confirmed, Deduced or Hypothesis and records where the current dashboard stops short of a two-way platform.",
                "The owner has used the current version for a recorded session and the notes are attached (what helped, what was missing for making decisions).",
            ],
            who=f"{OWNER}, with a BMAD session (analyst persona Mary is available as `/bmad-agent-analyst`).",
            seeds=[
                f"As {OWNER}, I want a written evaluation of using `superclaude observe` today, so that the two-way design starts from facts.",
                f"As {MAINT}, I want a lean project-context file, so that every later BMAD workflow loads the house rules without re-asking.",
            ],
            steps=[
                S("/bmad-generate-project-context", "brownfield project IronClaude; focus on `src/superclaude/cli/observe/`; point to CLAUDE.md for house rules, do not copy them", "`project-context.md` under `_bmad-output/`", "file exists and lists no rule that contradicts CLAUDE.md"),
                S("/bmad-investigate", "map what `superclaude observe` does today and where it falls short of a two-way decision platform (read-only rule, no database, questions in process memory)", "case file under `_bmad-output/implementation-artifacts/`", "every finding carries a grade and a path:line or command output"),
            ],
            handoff="none",
            human="yes (usage session by the owner; BMAD menus)",
            cx="Medium",
        ),
        dict(
            slug="research-requirements-and-similar-projects",
            title="Release 2 prep: research requirements, best approaches and similar GitHub projects",
            source=SRC + " (research of requirements, best approaches and any similar github projects)",
            why="The owner asked to learn from overlapping GitHub projects before building voting and responding from the dashboard.",
            links=[L727, L726, "Licence rule carried over from the 409 packet: no AGPL code is copied, linked or imported (TUIBBS licence question stayed open in `.dev/issues/409/bmad/final-review/workflow-input.md`)"],
            done=[
                "A research document lists each similar project with: link, what overlaps (voting, approving, answering agent questions, decision queues), what to take, what not to take, licence.",
                "A short list of best approaches for turning agent questions into binary or multiple-choice decisions, with the source of each.",
                "Every claim is labelled verified (source read) or UNVERIFIED.",
            ],
            who=f"{OWNER}; research is done by the BMAD session and may use IronClaude research tools in the same session.",
            seeds=[
                f"As {OWNER}, I want to know which existing projects already solve voting and responding for agent sessions, so that we reuse what works and avoid their mistakes.",
                f"As {OWNER}, I want the best approaches for reducing a coordinator question to a binary or multiple-choice decision, so that most interactions are one key press.",
            ],
            steps=[
                S("/bmad-market-research", "comparable open-source projects for a two-way terminal or web dashboard over AI coding-agent sessions: voting, approvals, answering questions", "research document under `_bmad-output/planning-artifacts/research/`", "each project has link, overlap, take, avoid, licence"),
                S("/bmad-technical-research", "approaches and libraries for decision queues, approval flows and reducing free-text questions to choices", "`technical-<slug>-research-<date>.md` under `_bmad-output/planning-artifacts/research/`", "approaches are ranked with sources; web search was available (the skill aborts without it)"),
            ],
            handoff="none",
            cx="Medium",
        ),
        dict(
            slug="two-way-requirements-and-ux",
            title="Release 2 prep: requirements and UX of the two-way dashboard (decisions, demands, notices)",
            source=SRC + " and the goal paragraph (binary or multiple choice; demands to the coordinator when that fails)",
            why="The product goal changes from showing information to making decisions. The PRD, the UX contract and the read-only rule must change together, and that needs the owner's recorded decision.",
            links=[L727, L726, L409, "Existing spec companion on origin/master: `.dev/issues/409/bmad/spec-orca-observer/write-back-future-stage.md`"],
            done=[
                "The PRD (Update of the 409 PRD) has feature groups with globally numbered FR ids for: decision cards (binary and multiple choice), demands to the coordinator (more context, better explanation, debate of several proposals, extra validation, research, fact checking, use of named plugins or tools such as ponytail), and the notice that the person is needed in a coordinator session.",
                "The UX pair (DESIGN.md, EXPERIENCE.md) covers those screens at the terminal widths the 409 package fixed (160, 116 and 80 columns).",
                "The decision to relax the read-only rule is recorded by the owner in a dated record (house pattern: `.dev/issues/409/owner-decisions-<date>.md`); issue #726 is told.",
                "An independent review of the PRD and UX passed before anything is handed to IronClaude (the 409 review needed 63 blocking fixes).",
            ],
            who=f"{OWNER}; BMAD product manager (John, `/bmad-agent-pm`) and UX designer (Sally, `/bmad-agent-ux-designer`) personas are available.",
            seeds=[
                f"As {OWNER}, I want each coordinator question shown as a decision I can answer with one key, so that I stop typing answers in the coordinator terminal.",
                f"As {OWNER}, when a question cannot be reduced, I want one-key demands to the coordinator (more context, better explanation, debate, validation, research, fact check, run a named plugin), so that the coordinator does the work before I decide.",
                f"As {DEV}, I want a notice that I am needed in the coordinator session for a longer conversation, so that I do not miss it.",
            ],
            steps=[
                S("/bmad-forge-idea", "pressure-test this idea: the dashboard is where decisions are made; coordinator questions become binary or multiple choice; the fallback is a demand to the coordinator", "optional `forged-idea.md`; sessions are interactive only", "assumptions that did not survive are written down"),
                S("/bmad-prd", "update the PRD copied from `.dev/issues/409/bmad/prd-orca-observer/` for the two-way dashboard to release 2.0; change signal: the owner text of issue 727", "`prd.md`, `addendum.md`, `.memlog.md` in a new run folder", "feature groups and FR ids exist; open questions triaged; validation report written"),
                S("/bmad-ux", "two-way screens: decision card, demand menu, 'you are needed' notice; extend the 409 DESIGN.md and EXPERIENCE.md", "`DESIGN.md` and `EXPERIENCE.md` under `_bmad-output/planning-artifacts/ux-designs/`", "screens render as text mockups at 160, 116 and 80 columns"),
                S("/bmad-review-adversarial-general", "review the new PRD and UX at their paths; report only concrete defects with consequences", "review report next to each document", "blocking findings fixed or recorded; independent review passes (then `/sc:spec-panel @<prd path>` once, first on one file; a folder is not known to work)"),
            ],
            handoff="none",
            cx="Complex",
        ),
        dict(
            slug="state-persistence-and-storage-evaluation",
            title="Release 2 prep: evaluate state persistence and data storage for a two-way dashboard",
            source=SRC + " (evaluate needs for state persistence and data storage; deliverable 1: /sc:brainstorm --depth deep)",
            why="Today the dashboard keeps nothing but an export record and a snapshot. A platform where decisions are made must keep questions, votes, answers and an audit trail, and several coordinators and developers will read and write the same state.",
            links=[L727, LCODE, L726, "Brainstorm output folder convention: `.dev/brainstorms/<date>-<topic>/`"],
            done=[
                "A list of what must persist (questions, votes from #726, answers, demands to the coordinator, escalations, audit trail, snapshots), who writes and reads each item, and the consistency each needs.",
                "A deep brainstorm result on architecture, data storage and database needs for releases 1.1 to 2.0, with the options considered and the rejected ones recorded.",
                "The decision is in the architecture spine as `AD-n` entries (new ids only, existing ids not renumbered) with Binds, Prevents and Rule.",
            ],
            who=f"{OWNER} decides; BMAD architect (Winston, `/bmad-agent-architect`) and an IronClaude brainstorm contribute.",
            seeds=[
                f"As {OWNER}, I want to know exactly what the dashboard must remember, so that storage is sized to real needs and not guessed.",
                f"As {COORD}, I want questions and answers stored where the dashboard and I both reach them, so that an answer given in the dashboard arrives without copying text.",
            ],
            steps=[
                S("/bmad-technical-research", "state persistence and data storage options for a bidirectional dashboard over agent sessions (files, SQLite, Postgres), consistency and concurrency", "technical research document under `_bmad-output/planning-artifacts/research/`", "options compared with sources; web search available"),
                S("/sc:brainstorm \"architecture, data storage and database needs of dashboard releases 1.1 to 2.0 incl. a Postgres database per project and organised session and decision history @.dev/issues/727/issue-body.md\" --depth deep --research deep --codebase --blind --output .dev/brainstorms/<date>-dashboard-storage/", "owner's deliverable 1 asks for exactly this deep brainstorm; run it ATTENDED in a person's own session (under --unattended the Socratic dialogue and deep research are skipped); pass the research document too", "brainstorm package under the output folder", "package has proposals, merged result and the open decisions; BMAD decides from it"),
                S("/bmad-architecture", "update the existing spine (keep AD ids stable) with the persistence decisions; coaching path", "updated `ARCHITECTURE-SPINE.md`, `.memlog.md`", "lint and reviewer gate of the skill pass; new `AD-n` have Binds, Prevents, Rule"),
            ],
            handoff="none",
            cx="Complex",
        ),
        dict(
            slug="postgres-database-per-project",
            title="Release 2 prep: a Postgres database per project (schema, provisioning, lifecycle)",
            source=SRC + " (creation of a postgres database per project)",
            why="The owner's stated direction: one Postgres database per project, so decisions and sessions of all coordinators in a project survive restarts and can be read by every coordinator and developer of that project.",
            links=[L727, "Storage evaluation: sibling feature `state-persistence-and-storage-evaluation` (this feature builds on its decision)", "Not known yet: where the database runs (Coder workspace, local, shared host) and how credentials are provided; never print or store a credential in an issue"],
            done=[
                "An epic-altitude architecture spine covers: where the database runs, how it is created per project without manual steps, schema ownership and migrations, backup and restore, local fallback when no database is reachable, credentials handling, and what happens when the database is down.",
                "Each open point is decided, deferred with a revisit condition, or an open question, as the architecture skill requires; nothing is invented.",
                "After the owner says go: stories exist for provisioning and the first schema (tables created only by the story that needs them, BMAD rule) and are handed to IronClaude.",
            ],
            who=f"{OWNER} and {MAINT}; BMAD architect session; IronClaude executes the stories after the owner's go.",
            seeds=[
                f"As {DEV}, I want a project database created for me without manual setup, so that the dashboard works the first time.",
                f"As {MAINT}, I want schema changes made by migrations owned by one story each, so that no story creates tables it does not need.",
                f"As {OWNER}, I want a clear fallback when the database is unreachable, so that the dashboard still shows the current coordinator questions.",
            ],
            steps=[
                S("/bmad-architecture", "epic altitude: scope the run folder to this feature; inherit the program spine as binding constraints; decide database placement, provisioning, schema ownership, migrations, backup, fallback", "`ARCHITECTURE-SPINE.md` in an epic-scoped run folder", "reviewer gate passes; no whole structural dimension left silent (deployment and operations included)"),
                S("/bmad-spec", "adopt the spine as a companion and derive the SPEC kernel for the database capability", "`SPEC.md` and companions in `_bmad-output/specs/spec-<slug>/`", "capabilities have intent and success; non-goals explicit"),
                S("/bmad-create-epics-and-stories", "stories for provisioning and the first schema only, after the owner's go", "story entries in the epic file for this release", "each story passes the BMAD story rules; readiness check passes"),
            ],
            handoff_extra="Only the provisioning and schema stories go to IronClaude, and only after the owner records a go. The packet must carry the credential rule: no secret is read, printed or committed.",
            cx="Complex",
        ),
        dict(
            slug="session-and-decision-history-across-coordinators",
            title="Release 2 prep: organise session and decision history across coordinators and developers",
            source=SRC + " (vectorized, or organized in whatever way provides most benefit for least work)",
            why="The owner wants every coordinator in a project, across all human developers, to know what the other coordinators did and decided. The method (vector search or something simpler) is to be chosen by benefit for the least work.",
            links=[L727, "Related open issue: #725 (coordinators must ask the peer project's coordinator, read-only, before asking a human)", LRELATED],
            done=[
                "The candidate ways of organising history are compared on retrieval quality, effort, running cost and fit with a per-project Postgres database, with the evidence for each (vector search is one candidate, plain tables and text search are others).",
                "One way is chosen for the first release that needs it, with the reason, and a revisit condition for the others.",
                "The choice is an `AD-n` in the spine and a story set is ready, or the decision is deferred with an owner-visible reason.",
            ],
            who=f"{OWNER} decides; BMAD architect session with an IronClaude deep brainstorm.",
            seeds=[
                f"As {COORD}, I want the recorded decisions and sessions of the other coordinators of my project, so that I do not ask a human something a peer already settled.",
                f"As {DEV}, I want to see what other developers' coordinators decided, so that my coordinator does not repeat or contradict it.",
            ],
            steps=[
                S("/bmad-technical-research", "ways to organise session and decision history for retrieval by agents: vector search, full-text search, structured tables; cost and effort of each", "research document under `_bmad-output/planning-artifacts/research/`", "each option has evidence and effort noted; UNVERIFIED claims labelled"),
                S("/sc:brainstorm \"organising session and decision history across coordinators and developers of one project: most benefit for least work\" --depth deep --research deep --codebase --blind --output .dev/brainstorms/<date>-history-organisation/", "run ATTENDED in a person's own session; pass the research document and the storage decision", "brainstorm package", "merged proposal with the rejected options recorded; BMAD decides from it"),
                S("/bmad-architecture", "update the spine with the chosen organisation (new AD ids, nothing renumbered)", "updated spine and memlog", "reviewer gate passes"),
            ],
            handoff_extra="No code is built in this feature unless the owner records a go; the first stories land in the release the owner schedules.",
            cx="Complex",
        ),
        dict(
            slug="release-plan-review-and-program-epics",
            title="Release 2 prep: review the release list and plan the program epics and stories",
            source='owner text, "Deliverable 1: Review of release plan below, breaking down the main changes and features"',
            why="Deliverable 1 asks for a written review of the release list that breaks out the main changes and features of each step. The same planning run produces the epics and stories for the first releases and proves that BMAD can plan several releases in sequence.",
            links=[L727, LPLAN, "Release map: `agent1/RELEASE-PLAN.md` section S2 (15 epics)", "Epic file risk R1 (second `bmad-create-epics-and-stories` run may overwrite the first): trial in this feature"],
            done=[
                "A written review of the release list: for each release the main changes and features, the inputs it needs, and its exit check.",
                "A SPEC (or PRD plus spine) that passes an independent review, then `epics` with stories for EPIC-01 and EPIC-02 and `sprint-status.yaml` created.",
                "The multi-release recipe (one epic per run, sharded `epics/` folder, epic number fixed by a `persistent_facts` line) is tried once and the result is recorded: it works, or what failed.",
                "The owner has recorded in chat which releases are scheduled (condition from issue 727: Deliverable 1 is finished and the owner has recorded which releases are scheduled).",
            ],
            who=f"{OWNER} approves; BMAD session; the coordinator files the scheduled epics.",
            seeds=[
                f"As {OWNER}, I want a review of the release list with the main changes of each step, so that I can decide which releases to schedule.",
                f"As {MAINT}, I want stories for the first two releases in the BMAD ledger, so that the first hand-off can be rehearsed.",
            ],
            steps=[
                S("/bmad-spec", "distill the two-way PRD, UX and architecture into the SPEC kernel plus companions", "`SPEC.md` and companions", "self-validate coherence and preservation passes recorded in the memlog"),
                S("/bmad-review-edge-case-hunter", "run on the SPEC folder path for orthogonal coverage next to the adversarial review", "review report", "blocking findings fixed"),
                S("/bmad-create-epics-and-stories", "create epic 1 and epic 2 only (EPIC-01 and EPIC-02); number epics by EPIC number; write to a sharded epics folder", "epic file(s) under `_bmad-output/planning-artifacts/epics/`", "FR coverage map complete; trial of the multi-release recipe recorded"),
                S("/bmad-check-implementation-readiness", "", "readiness report", "no blocking gap"),
                S("/bmad-sprint-planning", "", "`_bmad-output/implementation-artifacts/sprint-status.yaml`", "keys `epic-1`, `1-1-...`, `epic-1-retrospective` exist; file validates with `/bmad-sprint-status` validate mode"),
            ],
            handoff_extra="First rehearsal of the hand-off: pick one ready story, build its packet and run the IronClaude chain on it once the owner says go.",
            cx="Complex",
        ),
    ]
    return dict(
        n=1,
        slug="release-2-prep",
        version="2-prep",
        release="Release 2 prep",
        title="Release 2 prep: evaluate the dashboard and decide the architecture, storage and Postgres database for a two-way platform",
        schedule="OWNER MARKED FIRST (precedence over the release list); file when the owner says go",
        owner_item=(
            "First step is usage and evaluation of current version and evaluation and research of requirements, best approaches and any "
            "similar github projects ... Evaluate needs for state persistence and data storage related to the dashboard becoming a central "
            "bidirectional communication platform ... This architectural and prelim eval takes precedence over the release 2 roadmap below. "
            "Priority is evaluating the needs and validating or building/changing what is needed to support those and future needs, "
            "including the creation of a postgres database per project with the eventual goal of having current and past sessions and "
            "decisions vectorized (or organized in whatever way provides most benefit for least work) of all coordinators within a project, "
            "across all human developers."
        ),
        links=[L727, L726, LRELATED, L409, LPLAN],
        done=[
            "Deliverable 1 of issue 727 is finished: the written review of the release list, and the `/sc:brainstorm --depth deep` result on architecture, data storage and database needs.",
            "Release 2 prep items are done: use and evaluation of the current version; research of requirements, best approaches and similar GitHub projects; the state and storage needs of a two-way dashboard.",
            "The owner has recorded in chat which releases are scheduled; each scheduled release has its own epic issue (this epic closes when they exist or the owner drops them).",
        ],
        pickup="The architecture and preliminary evaluation come first (owner's order). The program-level BMAD run (project context, investigate, research, PRD update, UX, architecture update, spec, review, epics, readiness, sprint planning) happens in this epic once, with the owner in the session; later releases reuse its outputs. Planning only until the owner says go; the Postgres provisioning and schema stories are the first code and need an explicit go.",
        features=feats,
        progress_extra=["Program PRD, UX and architecture spine reviewed and final", "SPEC and companions derived and reviewed", "Epics for EPIC-01 and EPIC-02 and sprint-status.yaml created"],
        cx="Complex",
        loop=False,
        loop_text=(
            "Program run order (details in agent1/RELEASE-PLAN.md S4.1): `/bmad-help`, `/bmad-generate-project-context`, `/bmad-investigate`, "
            "`/bmad-market-research` and `/bmad-technical-research`, `/bmad-forge-idea`, `/bmad-prd` (Update), `/bmad-ux`, `/bmad-architecture` (Update) "
            "with `/sc:brainstorm ... --depth deep`, `/bmad-spec`, an independent review, `/bmad-create-epics-and-stories` (EPIC-01 and EPIC-02 only), "
            "`/bmad-check-implementation-readiness`, `/bmad-sprint-planning`."
        ),
    )
