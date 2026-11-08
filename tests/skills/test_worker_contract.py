"""Static checks for the Orca worker contract (~/.claude/WORKER-CONTRACT.md), Phases P0 to P2.

The contract file is read through the module-level CONTRACT_PATH and the command
files through COMMANDS_DIR, so the negative tests can point both at a tmp_path copy.
Each rule is pinned by phrases that carry its meaning, not only its label. The
phrases are copied here as data; the tests never read the plan's artifacts.
After P2 the commands that have an `## Unattended mode` section are exactly the
keys of UNATTENDED_EXPECT, and each section is checked against its entry there.
CI-safe, no network.
"""

import re
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
CONTRACT_PATH = _REPO / "src" / "superclaude" / "core" / "WORKER-CONTRACT.md"
COMMANDS_DIR = _REPO / "src" / "superclaude" / "commands"

_THIS = sys.modules[__name__]

# rule -> (identifier that must share a line with the first phrase, or None; phrases)
RULE_PHRASES = {
    # Terms
    "worker-run": (
        None,
        [
            "a session that received an Orca preamble carrying a Task ID and a Dispatch ID"
        ],
    ),
    "unattended-mode": (
        None,
        [
            "The mode is selected only by the flag (decision D1)",
            "No command detects Orca, its preamble or its environment",
        ],
    ),
    "flag-parse-rule": (
        None,
        ["counts only as a standalone argument token outside any quoted argument"],
    ),
    "person-mode-refusal": (
        None,
        ["every command refuses the flags that exist to involve a person"],
    ),
    "report-directory": (
        None,
        ["Passing neither, or both, is refused before any work"],
    ),
    "brief-guard-scope": (
        None,
        [
            "it applies only in a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs"
        ],
    ),
    "brief-guard-case-1": (
        None,
        [
            "(case 1) every existing copy has an `## Unattended mode` section and the line lacks a standalone `--unattended`",
            "guard refused: brief lacks --unattended",
        ],
    ),
    "brief-guard-case-2": (
        None,
        [
            "(case 2) no existing copy has the section and the line has the flag",
            "guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)",
        ],
    ),
    "brief-guard-copies-disagree": (
        None,
        [
            "the copies disagree",
            "guard refused: command copies disagree (stale copy): <paths>",
        ],
    ),
    "brief-guard-case-3": (
        None,
        [
            "(case 3) the command is on the never-as-worker list; the body still starts `guard refused:`"
        ],
    ),
    "brief-guard-prefix": (None, ["a body starting `guard refused:`"]),
    "never-as-worker": (
        "**Never-as-worker list**",
        [
            "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, "
            "plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers"
        ],
    ),
    "nested-propagation": (
        None,
        [
            "passes `--unattended` when the invoked command accepts it at this phase",
            "`<caller report-dir>/nested/<command>-<n>/`",
        ],
    ),
    # Command-side requirements
    "WC-2": ("WC-2", ["No person-blocking step in unattended mode"]),
    "WC-4": (
        "WC-4",
        [
            "One report file, known before dispatch, written on every outcome",
            '`worker_contract_version` (`"1"`), `worker_status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path`',
            "`artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed",
            "`artifacts` leaves out paths git ignores and paths outside the repository",
        ],
    ),
    "WC-4-mapping": (
        None,
        [
            "`success` → `succeeded`, `partial` → `partial`, `failed` → `failed`, `stopped-precondition` → `failed`"
        ],
    ),
    "WC-4-missing-directory-error": (
        None,
        [
            "unattended mode needs exactly one report directory: --report-dir <dir>, or this command's own directory output flag"
        ],
    ),
    "WC-8": ("WC-8", ["No Orca fan-out from inside a command"]),
    "WC-9": ("WC-9", ["No outward action from a worker; local commits only by grant"]),
    "WC-10": (
        "WC-10",
        ["at the cadence its preamble sets", "split into waits of at most 4 minutes"],
    ),
    "WC-11": ("WC-11", ["Two workers in one worktree must never write the same file"]),
    # Worker-session duties
    "WC-3": (
        "WC-3",
        [
            "Questions go to the coordinator, not to a local prompt",
            "The worker asks at most once per Task",
        ],
    ),
    "WC-5": (
        "WC-5",
        [
            "`--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists"
        ],
    ),
    "WC-5-P0-override": (
        "WC-5",
        [
            "a brief that states the AC-0.4 report file and outcome rule replaces this mapping for that Task"
        ],
    ),
    "WC-7": ("WC-7", ["Run at the top level, never inside a subagent"]),
    "WC-12": (
        "WC-12",
        ["Coordinator follow-ups are pulled, not pushed", "at natural checkpoints"],
    ),
    "WC-13": ("WC-13", ["No Orca fan-out from the worker session"]),
    "WC-14": (
        "WC-14",
        [
            "No turn ends between chain steps",
            "ends its turn only after `worker_done`, while blocked in the preamble's `ask`, or on `consumer_fenced`",
            "the next action in the same turn is the next `Command:` line",
            "The one exception is a coordinator interrupt that asks for a handoff (the S6 nudge, section 4)",
        ],
    ),
    "WC-15": (
        "WC-15",
        [
            "Context-safe reading and handoff files",
            "in pieces of at most 80 lines and never rereads a whole prior report",
            "writes `<report-dir>/handoff/<n>-<command>.md` (at most 40 lines",
        ],
    ),
    "heartbeats": (
        None,
        [
            "The worker session sends heartbeats at the cadence its preamble sets",
            "the dispatch preamble is the authority for the Orca verb syntax and for the heartbeat cadence",
        ],
    ),
    # Coordinator rules
    "WC-6": (
        "WC-6",
        [
            "WC-6. Every retry is a new Task",
            "the coordinator never uses `worker-start --retry-of`",
            "is never re-created after three failed starts",
            "A crashed or stalled attempt is settled by the coordinator",
        ],
    ),
    "wc6-live-attempt-settlement": (
        None,
        [
            "settles only when the person directs its cancellation and the coordinator has confirmed quiescence",
            "two reads 5 minutes apart that agree",
            "Context exhaustion, heartbeats and the coordinator's own nudges are not stall proofs",
            "is logged and shown to the person, never applied",
        ],
    ),
    "liveness-wait": (
        None,
        [
            "### Liveness supervision",
            "orca orchestration check --wait --types status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat --timeout-ms 300000",
            "A returned Delivery is the whole FIFO batch, replayed until `--ack`",
            "writes one run-notes line per message ID before it sends `--ack`",
            "After three empty waits in a row, the coordinator enumerates its workers with `worker-list`",
        ],
    ),
    "liveness-sweep-and-states": (
        None,
        [
            "at most once every 5 minutes, the coordinator runs one sweep",
            "A message arrival or a repeated identical read is not one",
            "| S9 finished but unreported | Contract present, the brief has no `Command:` line after the step that wrote it,",
            "Token unchanged for W while heartbeats arrive, or the S3 trigger fires;",
            "| S10 settled |",
            "| S11 unknown |",
        ],
    ),
    "liveness-acks": (
        None,
        [
            "The coordinator never resends a mailbox copy of an answer",
            "type ONE copy into the terminal",
            "A4, at 15 minutes: L5 report to the person",
        ],
    ),
    "liveness-ladder-and-restart": (
        None,
        [
            "Every sweep; at most 2 costly probes per triggered worker per sweep",
            "1 per rolling 60 minutes, 2 per lineage",
            "Nudges, asks, heartbeats, repeated identical reads and context exhaustion are never stall proofs",
            "the same class twice means no plain restart",
            "An L4 restart puts this note in the new Task's brief, after the guard line and before the `Command:` lines",
        ],
    ),
    "liveness-never-on-silence": (
        None,
        [
            "On silence, a passed deadline, `unverifiable` liveness or screen text alone, the coordinator never:",
            "Silence authorizes only L1, L2 and L3.",
        ],
    ),
    "liveness-unverified": (
        None,
        [
            "UNVERIFIED: what `check --wait` wakes on when `--types` is not given",
            "UNVERIFIED: the cause of case 5, answers a worker did not see",
            "UNVERIFIED: whether Orca has an attention category for a permission prompt or for compact thrashing",
            "UNVERIFIED: what Claude Code does with text typed while a tool call runs",
            "UNVERIFIED: whether two consumers on one mailbox both get a batch",
        ],
    ),
    "brief-contents": (
        None,
        [
            "The contract only works if the brief carries what the command would otherwise ask a person",
            "at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5)",
        ],
    ),
    "brief-layout": (None, ["so the Task text never starts with `/sc:`"]),
    "worktrees": (
        None,
        [
            "Every worktree is created by Orca at Orca's default location",
            "a child worktree created by Orca with `worker-start --worktree new-child --base-branch <feature branch>` when WC-11 requires one",
            "The coordinator keeps a placement map",
            "the coordinator merges the child branch into the feature branch, then removes the child",
            "It never removes a worktree or branch that holds unmerged commits",
        ],
    ),
    "child-setup": (
        "`--setup skip`",
        [
            "only when the user's instruction, in the coordinator's own conversation, names that step",
            "This holds in every repository, IronClaude included",
        ],
    ),
    "git-github-ownership": (
        None,
        [
            "Every such action targets `IronbellyOrg/IronClaude`",
            "PRs go only through `/sc:pr-submit --monitor 3`",
            "Before any push that would publish worker commits the person has not seen",
            "stages explicit paths plus `.dev/tasks` at every commit and again at the end of the run",
        ],
    ),
    "read-before-depend": (
        None,
        [
            "Reading a result before anything depends on it",
            "a brief-guard refusal; nothing ran",
        ],
    ),
    "dependents-after-settle": (
        None,
        ["Every dependent Task is created only after all its inputs have settled"],
    ),
    "implement-stop": (
        None,
        [
            "*Freeze.* A plan is frozen when",
            "*Lifting the freeze.* The freeze lifts only when",
            "dispatches only if all of the following hold",
            "*Placement.* The resume Task starts in the halted worktree by selector",
        ],
    ),
    "fan-in-max": (None, ["maximum of 10 inputs"]),
    "fan-in-min": (None, ["at least 2 inputs are admitted"]),
    "wc10-absence-not-death": (
        None,
        [
            "never as death",
            "never stops, retries or releases a worker because a heartbeat is late",
            "authorizes only read-only probes, a typed nudge and a direct question",
        ],
    ),
    "wc11-liveness-stat": (
        None,
        [
            "The coordinator's liveness `stat` reads only the worker's own contract path and report directory",
        ],
    ),
    "heartbeat-progress-token": (
        None,
        [
            "Each heartbeat carries a progress token, in the heartbeat's subject or phase text, or a `status` body line",
            "evidence that the process exists, not that the work is progressing",
        ],
    ),
    "wc12-ack-batch": (
        None,
        [
            "the worker handles every message in it before acknowledging the batch",
            "ack <message_id> applied|queued|refused",
            "applied (duplicate)",
        ],
    ),
    "wc3-ask-return-heartbeat": (
        None,
        [
            "When `ask` returns, the worker sends one heartbeat at once",
            "sends the WC-12 ack for that message ID at the first legal opportunity, before re-invoking the command",
        ],
    ),
    "wc5-closing-report-type": (
        None,
        [
            "The closing report is never sent as `status`, `handoff` or a reply",
        ],
    ),
    "wc7-skill-invocation": (
        None,
        [
            "A worker runs each chained `Command:` by invoking its Skill",
            "Reading the command file and following it from memory does not satisfy WC-7",
        ],
    ),
    "brief-template": (
        None,
        [
            "## 5. Coordinator brief template",
            '`--report-dir` is marked "from P1": no command accepts it at P0',
            "P0 only: Report file: <the command's report file under AC-0.4>.",
        ],
    ),
    "brief-chain-line": (
        None,
        [
            "Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).",
        ],
    ),
}

GUARD_LINE = (
    "Guard: before running anything, check every Command: line below under the brief guard in "
    "~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed "
    'with a body starting "guard refused:".'
)

NEVER_AS_WORKER = (
    "/sc:agent",
    "/sc:git",
    "/sc:help",
    "/sc:issue",
    "/sc:pm",
    "/sc:spawn",
    "/sc:swarm-wizard",
    "/sc:pr-submit",
)

# The sixteen commands that get an `## Unattended mode` section in P1, in the order
# of the spec's phase table.
P1_COMMANDS = (
    "adversarial",
    "brainstorm",
    "cleanup-audit",
    "graph",
    "impact",
    "index-repo",
    "init-lite",
    "workflow",
    "analyze",
    "build",
    "business-panel",
    "design",
    "document",
    "explain",
    "index",
    "test",
)

# The fifteen commands that get an `## Unattended mode` section in P2, in the order
# of the P2 static plan. UNATTENDED_EXPECT gains their entries one task at a time.
P2_COMMANDS = (
    "auggie-review",
    "cleanup",
    "improve",
    "cli-eval",
    "cli-portify",
    "recommend",
    "research",
    "review-translation",
    "spec-panel",
    "task",
    "tasklist",
    "reflect",
    "release-split",
    "tdd",
    "troubleshoot",
)

# command -> {"flags": tokens its section must contain (whole tokens),
#             "phrases": further text it must contain,
#             "nested": optional list of nested commands that receive --unattended}.
# Each command task adds its own entry in the task that converts the command.
UNATTENDED_EXPECT: dict = {
    "adversarial": {
        "flags": ["--output", "-o", "--interactive", "-i"],
        "phrases": ["<output>/adversarial/return-contract.yaml", "artifacts"],
        "nested": [],
    },
    "brainstorm": {
        "flags": ["--output", "-o", "--interactive", "-i"],
        "phrases": [
            "nested/research-",
            "research-deep is skipped",
            "exactly as passed",
            "never reused",
            "nested/analyze-",
            "nested/adversarial-",
            "dry-run",
            "writes no nested directory and no nested contract",
            "only by a `/sc:analyze` call",
        ],
        "nested": ["analyze", "adversarial", "research"],
    },
    "graph": {
        "flags": ["--output-dir"],
        "phrases": ["refuses init", "report_path"],
        "nested": [],
    },
    "impact": {
        "flags": ["--output-dir"],
        "phrases": ["explicit"],
        "nested": [],
    },
    "cleanup-audit": {
        "flags": ["--pass"],
        "phrases": [
            ".claude-audit/final-report.md",
            "progress.json",
            "only one audit at a time",
        ],
        "nested": [],
    },
    "index-repo": {
        "flags": [],
        "phrases": ["PROJECT_INDEX.md", "PROJECT_INDEX.json", "mode=update"],
        "nested": [],
    },
    "init-lite": {
        "flags": ["--output", "--dry-run"],
        "phrases": ["the one write besides the report", "Safety Invariants 2 and 3"],
        "nested": [],
    },
    "workflow": {
        "flags": ["--handoff"],
        "phrases": [
            "pre-creation",
            "--handoff implement",
            "does not stage",
            "nested/reflect-",
        ],
        "nested": ["reflect"],
    },
    "analyze": {
        "flags": ["--output"],
        "phrases": ["analyze-report.md", "no gate", "consent is never given"],
        "nested": [],
    },
    "build": {
        "flags": ["--output"],
        "phrases": ["build-report.md", "no gate"],
        "nested": [],
    },
    "design": {
        "flags": ["--output"],
        "phrases": ["design-report.md", "no gate", "consent is never given"],
        "nested": [],
    },
    "test": {
        "flags": ["--watch", "--output"],
        "phrases": ["test-report.md", "verdict", "destructive", "left out"],
        "nested": [],
    },
    "explain": {
        "flags": ["--format interactive", "--output"],
        "phrases": ["explain-report.md", "Write"],
        "nested": [],
    },
    "business-panel": {
        "flags": ["--mode socratic", "--output"],
        "phrases": ["adaptive", "business-panel-report.md"],
        "nested": [],
    },
    "document": {
        "flags": ["--output", "--type"],
        "phrases": ["every file edited", "inline"],
        "nested": [],
    },
    "index": {
        "flags": ["--output", "--type"],
        "phrases": ["knowledge-base mode", "index-report.md", "consent is never given"],
        "nested": [],
    },
    "cleanup": {
        "flags": ["--interactive", "--output"],
        "phrases": [
            "Approval Required",
            "not applied",
            "cleanup-report.md",
            "partial when changes were applied and a validation failed or did not run",
            "every changed file",
            "left out (WC-4)",
            'every item under "Approval Required" is listed as not applied',
        ],
        "nested": [],
    },
    "improve": {
        "flags": ["--interactive", "--force", "--output"],
        "phrases": [
            "Approval Required",
            "not applied",
            "improve-report.md",
            "partial when changes were applied and a validation failed or did not run",
            "every changed file",
            "left out (WC-4)",
            'every item under "Approval Required" is listed as not applied',
            "`--force` is refused",
        ],
        "nested": [],
    },
    "research": {
        "flags": ["--strategy planning"],
        "phrases": [
            "without clarification",
            "--strategy intent",
            "--strategy unified",
            "claudedocs/research_",
            "an explicit `--strategy intent` or `--strategy unified` is refused",
        ],
        "nested": [],
    },
    "spec-panel": {
        "flags": ["--target-release", "--improve", "--output"],
        "phrases": [
            "target_release",
            "blocked_question",
            "improved-spec.md",
            "spec-panel-report.md",
            "never modified",
            "a TDD input without `--target-release` resolves as blocked",
        ],
        "nested": [],
    },
    "recommend": {
        "flags": ["--eval"],
        "phrases": [
            "clarifying question",
            "blocked_question",
            "recommendation.md",
            ".claude/cache/",
            "the one clarifying question resolves as blocked",
        ],
        "nested": [],
    },
    "review-translation": {
        "flags": ["--context"],
        "phrases": [
            "context-summary.md",
            "(the path itself, never the pattern)",
            "blocked_question",
            "SKIP IMPLEMENTATION",
            "reports/localization/",
            "Phase 1 without `--context` resolves as blocked",
            "Phase 7 resolves to SKIP IMPLEMENTATION",
        ],
        "nested": [],
    },
    "release-split": {
        "flags": ["--output", "-o", "--interactive", "-i", "--r1-scope custom"],
        "phrases": [
            "blocked_question",
            "release-split-report.md",
            "split-with-remediation",
            "the tasklist-input warning resolves as blocked",
            "`--r1-scope custom` resolves as blocked",
            "both, or neither, is refused before any work",
        ],
        "nested": ["brainstorm", "adversarial"],
    },
    "cli-portify": {
        "flags": ["--resume", "--output"],
        "phrases": [
            "portify-analysis.md",
            "portify-spec.md",
            "portify-release-spec.md",
            "resume_phase",
            "resume_substep",
            "IronClaude checkout",
            "blocked_question",
            "each of the three approval gates resolves as blocked",
        ],
        "nested": [],
    },
    "auggie-review": {
        "flags": [
            "--output-dir",
            "--no-post-pr",
            "--no-remediation-offer",
            "--post-pr",
            "--remediation-offer",
        ],
        "phrases": [
            "REVIEW.md",
            "pr_review_url",
            "`--unattended` implies `--no-post-pr` and `--no-remediation-offer`",
            "`--post-pr` and `--remediation-offer` are refused",
            "map to the worker values `succeeded`, `partial` and `failed`",
        ],
        "nested": ["impact"],
    },
    "troubleshoot": {
        "flags": ["--output-dir", "--fix", "--depth deep", "--diagnosability-handoff"],
        "phrases": [
            "short input",
            "blocked_question",
            "REPORT.md",
            "the short input STOP resolves as blocked",
            "the `--fix` offer resolves as blocked",
        ],
        "nested": ["adversarial", "workflow"],
    },
    "task": {
        "flags": ["--compliance"],
        "phrases": [
            "0.70",
            "present to user",
            "FULL STOP",
            "EXEMPT",
            "tfep-incident-report.md",
            "not committed",
            "task-report.md",
            "every tier",
            "confidence below 0.70 resolves as blocked",
            "every FULL STOP resolves as blocked",
            "EXEMPT `commit` and `push` are refused",
        ],
        "nested": ["impact", "troubleshoot"],
    },
    "cli-eval": {
        "flags": ["--suite", "--output-dir"],
        "phrases": [
            "240 s",
            "blocked_question",
            "summary.json",
            "inside the run directory (run)",
            "never a bare file name",
            "the resolved set is the confirmed invocation",
            "empty-HOME workaround",
            "command-only",
            "technical-writer",
            "`run` without both `--suite` and `--output-dir` resolves as blocked",
            "an FR-G5 preflight failure resolves as blocked",
        ],
        "nested": ["spec-panel", "adversarial", "document"],
    },
    "tdd": {
        "flags": ["--output", "--resume"],
        "phrases": [
            "bare topic",
            "blocked_question",
            "its two ask-the-user points come back as a question",
            "does not stage",
            "reflect gate skipped (unattended)",
            "a bare topic resolves as blocked",
            "a TDD that is already complete resolves as blocked",
        ],
        "nested": [],
    },
    "reflect": {
        "flags": ["--output", "--remediate", "--no-promote"],
        "phrases": [
            "headless",
            "AUTO-FIXABLE",
            "stopped-precondition",
            "review snapshot",
            "task-builder",
            "the Wave 1B tech-research step is skipped",
            "the absolute path of the `REPORT.md` this run wrote",
            "`--remediate` is answered by the headless auto-accept rule",
        ],
        "nested": ["adversarial", "workflow", "impact"],
    },
    "tasklist": {
        "flags": ["--output", "--no-reflect"],
        "phrases": [
            "tasklist-index.md",
            "in the tasklist output directory, never a bare file name",
            "validation/ValidationReport.md",
            "validation/gate-results.txt",
            "validation/PatchChecklist.md",
            "blocked_question",
            "--compliance strict --unattended --report-dir <report-dir>/nested/task-<n>/",
            "the unresolved High or Medium HALT resolves as blocked",
            "the `needs_human_decision` HALT resolves as blocked",
        ],
        "nested": ["reflect", "task"],
    },
}

# Commands with an `## Unattended mode` section after P2 (./source.md section 6
# table). Later phases extend this set.
UNATTENDED_COMMANDS: frozenset = frozenset(UNATTENDED_EXPECT)

_TEMPLATE_HEADING = "## 5. Coordinator brief template"


def _contract() -> str:
    return Path(_THIS.CONTRACT_PATH).read_text(encoding="utf-8")


def _check_rule(text: str, rule: str) -> None:
    ident, phrases = RULE_PHRASES[rule]
    for phrase in phrases:
        assert phrase in text, f"{rule}: missing phrase {phrase!r}"
    if ident is not None:
        assert any(
            ident in line and phrases[0] in line for line in text.splitlines()
        ), f"{rule}: {ident} is not stated on the line carrying {phrases[0]!r}"


def _check_never_as_worker(text: str) -> None:
    lines = [ln for ln in text.splitlines() if "**Never-as-worker list**" in ln]
    assert len(lines) == 1, "the never-as-worker list must be one term line"
    for cmd in NEVER_AS_WORKER:
        assert re.search(rf"`{re.escape(cmd)}`", lines[0]), (
            f"{cmd} missing from the never-as-worker list"
        )


def _template_lines(text: str) -> list:
    assert _TEMPLATE_HEADING in text, "brief template section is missing"
    section = text.split(_TEMPLATE_HEADING, 1)[1]
    return section.splitlines()


def _check_guard_before_command(text: str) -> None:
    lines = _template_lines(text)
    guard = [i for i, ln in enumerate(lines) if ln.strip() == GUARD_LINE]
    command = [i for i, ln in enumerate(lines) if ln.startswith("Command:")]
    assert guard, "the brief template does not carry the guard line word for word"
    assert command, "the brief template has no Command: line"
    assert guard[0] < command[0], (
        "the guard line must come before the first Command: line"
    )


# A line names a step that runs repository-defined code when it carries an Orca setup flag
# that runs the repository's setup hooks (`--run-hooks` is the legacy alias of
# `--setup run`; `--setup inherit` follows the repository's own setup policy) or a code
# span that runs a program or script: a launcher or interpreter followed by arguments
# (`make <target>`, `bash ...`, `sh ...`, `uv ...`, `python ...`, `npm ...`, `node ...`
# and similar), `./...`, or a script file (`scripts/setup.sh`, `setup.py`).
_REPO_SETUP_FLAGS = ("--setup run", "--run-hooks", "--setup inherit")
_REPO_CODE_SPAN_RE = re.compile(
    r"`(?:make|bash|sh|zsh|uv|uvx|python3?|pip3?|pipx|npm|npx|pnpm|yarn|node|deno|bun"
    r"|cargo|ruby|perl|php|poetry|tox|nox)\s[^`]+`"
    r"|`\./[^`]+`"
    r"|`[^`\s]*\.(?:sh|py|js|ts|rb|pl)(?:\s[^`]*)?`"
)
_SETUP_SKIP_RE = re.compile(r"--setup <?skip\b")


def _runs_repo_code(line: str) -> bool:
    return any(f in line for f in _REPO_SETUP_FLAGS) or bool(
        _REPO_CODE_SPAN_RE.search(line)
    )


def _check_repo_setup_gated(text: str) -> None:
    """Every line naming a step that runs repository-defined code carries the user-instruction
    gate, and every new-child creation line asks for skipped setup (PR #368 review)."""
    _, phrases = RULE_PHRASES["child-setup"]
    hits = [ln for ln in text.splitlines() if _runs_repo_code(ln)]
    assert hits, "no contract line states the child setup rule"
    for ln in hits:
        for phrase in phrases:
            assert phrase in ln, (
                f"repository setup step without its gate {phrase!r}: {ln!r}"
            )
    for ln in text.splitlines():
        if "--worktree new-child" in ln:
            assert _SETUP_SKIP_RE.search(ln), (
                f"new-child creation without --setup skip: {ln!r}"
            )


def _check_no_unattended_sections() -> None:
    have = sorted(
        p.stem
        for p in Path(_THIS.COMMANDS_DIR).glob("*.md")
        if re.search(r"^## Unattended mode\s*$", p.read_text(encoding="utf-8"), re.M)
    )
    assert set(have) == set(UNATTENDED_COMMANDS), (
        f"unexpected `## Unattended mode` sections: {have}"
    )


# Python form of Check SCAN (the grep form's POSIX class means something else in re).
_ORCA_NAME_RE = re.compile(
    r"\borca(-ide)?\s+(orchestration|worktree|terminal|agent)\b", re.I
)


def _token_re(tok: str) -> re.Pattern:
    """A whole-token pattern: `-i` is not found inside `--interactive`."""
    return re.compile(rf"(?<![\w-]){re.escape(tok)}(?![\w-])")


def _unattended_section(name: str) -> str:
    """The text of `## Unattended mode` up to the next `## ` heading."""
    lines = (
        (Path(_THIS.COMMANDS_DIR) / f"{name}.md").read_text(encoding="utf-8")
    ).splitlines()
    start = next(
        (i for i, ln in enumerate(lines) if ln.rstrip() == "## Unattended mode"), None
    )
    assert start is not None, f"{name}: no `## Unattended mode` section"
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
        len(lines),
    )
    return "\n".join(lines[start:end])


def _check_unattended_section(text: str, expect: dict) -> None:
    for need in (
        "return-contract.yaml",
        "~/.claude/WORKER-CONTRACT.md",
        "--report-dir",
    ):
        assert need in text, f"section lacks {need!r}"
    for tok in expect.get("flags", []):
        assert _token_re(tok).search(text), f"section lacks flag {tok!r}"
    for phrase in expect.get("phrases", []):
        assert phrase in text, f"section lacks {phrase!r}"
    nested = expect.get("nested", [])
    for name in nested:
        assert f"nested/{name}-" in text, f"section lacks nested/{name}-"
    if not nested:
        assert "nested/" not in text, "section names a nested directory"
    assert "src/superclaude/" not in text, "section names a src/superclaude/ path"
    assert not _ORCA_NAME_RE.search(text), "section names an Orca command"


def _removals() -> list:
    """Every (command, kind, token) of UNATTENDED_EXPECT, for the removed-token tests."""
    out = []
    for cmd in sorted(UNATTENDED_EXPECT):
        entry = UNATTENDED_EXPECT[cmd]
        out += [(cmd, "flag", t) for t in entry.get("flags", [])]
        out += [(cmd, "phrase", t) for t in entry.get("phrases", [])]
        out += [(cmd, "nested", f"nested/{n}-") for n in entry.get("nested", [])]
    return out


def _remove(text: str, kind: str, tok: str) -> str:
    return _token_re(tok).sub("", text) if kind == "flag" else text.replace(tok, "")


# --- positive checks -------------------------------------------------------


@pytest.mark.parametrize("rule", sorted(RULE_PHRASES))
def test_contract_states_rule(rule):
    _check_rule(_contract(), rule)


def test_never_as_worker_list_names_all_seven_commands():
    _check_never_as_worker(_contract())


def test_brief_template_puts_guard_line_before_first_command_line():
    _check_guard_before_command(_contract())


# --- P2 coordinator brief and the nested-result rule (D-P2-20) -------------

P2_NEW_BRIEF_ROWS = (
    "auggie-review",
    "cli-eval",
    "cli-portify",
    "review-translation",
    "spec-panel",
)
NESTED_RESULT_PHRASES = (
    "the caller stops at that step",
    "prefixed with the nested command's name",
    "its own documented failure path for that step",
    "`succeeded` and `partial` count as the step completing",
)


def _name_pattern(name: str) -> str:
    return rf"(?<![\w-]){re.escape(name)}(?![\w-])"


def _p2_bullet(text: str) -> str:
    bullets = [ln for ln in text.splitlines() if ln.startswith("- From P2 ")]
    assert len(bullets) == 1, f"expected one 'From P2' bullet, found {len(bullets)}"
    return bullets[0]


def _check_p2_brief(text: str) -> None:
    assert "until P2" not in text, "the brief table still says 'until P2'"
    for name in P2_NEW_BRIEF_ROWS:
        assert re.search(rf"^\| `/sc:{re.escape(name)}` \|", text, re.M), (
            f"brief table lacks the {name} row"
        )
    bullet = _p2_bullet(text)
    for name in P2_COMMANDS:
        assert re.search(_name_pattern(name), bullet), f"P2 bullet lacks {name}"


def _check_nested_result_rule(text: str) -> None:
    lines = text.splitlines()
    at = [
        i
        for i, ln in enumerate(lines)
        if ln.startswith("- **Nested propagation rule**")
    ]
    assert len(at) == 1, "nested propagation rule line not found exactly once"
    assert at[0] + 1 < len(lines), "nothing follows the nested propagation rule"
    following = lines[at[0] + 1]
    for phrase in NESTED_RESULT_PHRASES:
        assert phrase in following, f"line after the nested rule lacks: {phrase}"


def test_p2_brief_table_rows_and_bullet():
    _check_p2_brief(_contract())


def test_nested_result_rule_follows_the_nested_propagation_rule():
    _check_nested_result_rule(_contract())


def test_p2_brief_check_fails_when_until_p2_is_back():
    with pytest.raises(AssertionError):
        _check_p2_brief(_contract() + "\nno `--depth deep` until P2\n")


@pytest.mark.parametrize("name", P2_NEW_BRIEF_ROWS)
def test_p2_brief_check_fails_when_a_row_is_removed(name):
    kept = [
        ln for ln in _contract().splitlines() if not ln.startswith(f"| `/sc:{name}` |")
    ]
    with pytest.raises(AssertionError):
        _check_p2_brief("\n".join(kept))


@pytest.mark.parametrize("name", P2_COMMANDS)
def test_p2_brief_check_fails_when_the_bullet_drops_a_command(name):
    text = _contract()
    bullet = _p2_bullet(text)
    cut = re.sub(_name_pattern(name), "x", bullet, count=1)
    assert cut != bullet
    with pytest.raises(AssertionError):
        _check_p2_brief(text.replace(bullet, cut))


@pytest.mark.parametrize("phrase", NESTED_RESULT_PHRASES)
def test_nested_result_check_fails_when_a_phrase_is_removed(phrase):
    with pytest.raises(AssertionError):
        _check_nested_result_rule(_contract().replace(phrase, ""))


def test_unattended_sections_match_the_listed_commands():
    _check_no_unattended_sections()


@pytest.mark.parametrize("cmd", sorted(UNATTENDED_EXPECT))
def test_unattended_section_content(cmd):
    _check_unattended_section(_unattended_section(cmd), UNATTENDED_EXPECT[cmd])


@pytest.mark.parametrize(
    ("cmd", "kind", "tok"),
    _removals(),
    ids=[f"{c}:{k}:{t}" for c, k, t in _removals()],
)
def test_unattended_section_check_fails_when_token_removed(cmd, kind, tok):
    text = _unattended_section(cmd)
    _check_unattended_section(text, UNATTENDED_EXPECT[cmd])
    with pytest.raises(AssertionError):
        _check_unattended_section(_remove(text, kind, tok), UNATTENDED_EXPECT[cmd])


def test_every_repo_setup_line_is_gated():
    _check_repo_setup_gated(_contract())


# --- negative checks: each assertion fails when its rule is removed --------


def _patched_copy(tmp_path, monkeypatch, text: str) -> None:
    copy = tmp_path / "WORKER-CONTRACT.md"
    copy.write_text(text, encoding="utf-8")
    monkeypatch.setattr(_THIS, "CONTRACT_PATH", copy)


@pytest.mark.parametrize("rule", sorted(RULE_PHRASES))
def test_rule_check_fails_when_rule_removed(rule, tmp_path, monkeypatch):
    text = _contract()
    for phrase in RULE_PHRASES[rule][1]:
        text = text.replace(phrase, "")
    _patched_copy(tmp_path, monkeypatch, text)
    with pytest.raises(AssertionError):
        _check_rule(_contract(), rule)


@pytest.mark.parametrize(
    "ungated",
    [
        "- If that setup does not run `make sync-dev`, the coordinator runs it before dispatch.",
        "- A child is dispatched only after its setup has succeeded (`--setup run`).",
        "- a child worktree created by Orca with `worker-start --worktree new-child --base-branch <feature branch>`.",
        "- a child created with `worker-start --worktree new-child`; skip nothing.",
        "- A child is created with `--run-hooks` before dispatch.",
        "- A child is created with `--setup inherit` before dispatch.",
        "- The coordinator runs `make install` in the child before dispatch.",
        "- The coordinator runs `./setup.sh` in the child before dispatch.",
        "- The coordinator runs `bash scripts/bootstrap.sh` in the child before dispatch.",
        "- In an IronClaude checkout the coordinator runs `make sync-dev` in the child.",
        "- The coordinator runs `uv run python scripts/setup.py` in the child before dispatch.",
        "- The coordinator runs `python scripts/x.py` in the child before dispatch.",
        "- The coordinator runs `npm run setup` in the child before dispatch.",
        "- The coordinator runs `node scripts/setup.js` in the child before dispatch.",
        "- The coordinator runs `scripts/setup.sh` in the child before dispatch.",
        "- The coordinator runs `uv sync` in the child before dispatch.",
    ],
)
def test_repo_setup_gate_check_fails_on_ungated_line(ungated, tmp_path, monkeypatch):
    _patched_copy(tmp_path, monkeypatch, _contract() + "\n" + ungated + "\n")
    with pytest.raises(AssertionError):
        _check_repo_setup_gated(_contract())


@pytest.mark.parametrize("cmd", NEVER_AS_WORKER)
def test_never_as_worker_check_fails_when_command_removed(cmd, tmp_path, monkeypatch):
    lines = _contract().splitlines()
    lines = [
        ln.replace(f"`{cmd}`", "") if "**Never-as-worker list**" in ln else ln
        for ln in lines
    ]
    _patched_copy(tmp_path, monkeypatch, "\n".join(lines))
    with pytest.raises(AssertionError):
        _check_never_as_worker(_contract())


def test_guard_order_check_fails_when_guard_follows_command(tmp_path, monkeypatch):
    head, section = _contract().split(_TEMPLATE_HEADING, 1)
    lines = section.splitlines()
    guard = next(i for i, ln in enumerate(lines) if ln.strip() == GUARD_LINE)
    moved = lines.pop(guard)
    command = next(i for i, ln in enumerate(lines) if ln.startswith("Command:"))
    lines.insert(command + 1, moved)
    _patched_copy(tmp_path, monkeypatch, head + _TEMPLATE_HEADING + "\n".join(lines))
    with pytest.raises(AssertionError):
        _check_guard_before_command(_contract())


def test_guard_order_check_fails_when_guard_line_removed(tmp_path, monkeypatch):
    head, section = _contract().split(_TEMPLATE_HEADING, 1)
    _patched_copy(
        tmp_path,
        monkeypatch,
        head + _TEMPLATE_HEADING + section.replace(GUARD_LINE, ""),
    )
    with pytest.raises(AssertionError):
        _check_guard_before_command(_contract())


def test_unattended_section_check_fails_on_unlisted_command(tmp_path, monkeypatch):
    cmds = tmp_path / "commands"
    cmds.mkdir()
    (cmds / "scratch.md").write_text(
        "# scratch\n\n## Unattended mode\n\nnone\n", encoding="utf-8"
    )
    monkeypatch.setattr(_THIS, "COMMANDS_DIR", cmds)
    with pytest.raises(AssertionError):
        _check_no_unattended_sections()


_SYNTHETIC_SECTION = (
    "## Unattended mode\n\n"
    "Read ~/.claude/WORKER-CONTRACT.md first. Report directory: --report-dir <dir>;\n"
    "the contract is <report-dir>/return-contract.yaml. Refuses --interactive.\n"
    "Nested: nested/analyze-<n>/ gets the flag. It has the gate phrase alpha-gate.\n"
)
_SYNTHETIC_EXPECT = {
    "flags": ["-i", "--interactive"],
    "phrases": ["alpha-gate"],
    "nested": ["analyze"],
}


def _synthetic_section(tmp_path, monkeypatch, body: str) -> str:
    cmds = tmp_path / "commands"
    cmds.mkdir(exist_ok=True)
    (cmds / "synthetic.md").write_text(
        "# synthetic\n\n"
        + body
        + "\n## Boundaries\n\nsrc/superclaude/ here is outside.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(_THIS, "COMMANDS_DIR", cmds)
    return _unattended_section("synthetic")


def test_unattended_section_helper_reads_only_its_own_section(tmp_path, monkeypatch):
    # `-i` is not listed in the synthetic section, and `--interactive` does not satisfy it.
    text = _synthetic_section(tmp_path, monkeypatch, _SYNTHETIC_SECTION)
    assert "src/superclaude/" not in text
    with pytest.raises(AssertionError):
        _check_unattended_section(text, _SYNTHETIC_EXPECT)
    ok = dict(_SYNTHETIC_EXPECT, flags=["--interactive"])
    _check_unattended_section(text, ok)
    _check_unattended_section(text + " -i\n", _SYNTHETIC_EXPECT)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda s: s.replace("return-contract.yaml", "the-file"),
        lambda s: s.replace("~/.claude/WORKER-CONTRACT.md", "the-contract"),
        lambda s: s.replace("--report-dir", "--dir"),
        lambda s: s.replace("alpha-gate", "beta"),
        lambda s: s.replace("nested/analyze-", "nested/other-"),
        lambda s: s + "See src/superclaude/skills/x.\n",
        lambda s: s + "Then run orca worktree create.\n",
    ],
    ids=[
        "no-contract-file",
        "no-contract-path",
        "no-report-dir",
        "no-phrase",
        "no-nested-name",
        "src-path",
        "orca-name",
    ],
)
def test_unattended_section_check_fails_on_synthetic_defects(
    tmp_path, monkeypatch, mutate
):
    ok = dict(_SYNTHETIC_EXPECT, flags=["--interactive"])
    good = _synthetic_section(tmp_path, monkeypatch, _SYNTHETIC_SECTION)
    _check_unattended_section(good, ok)
    with pytest.raises(AssertionError):
        _check_unattended_section(mutate(good), ok)


def test_cleanup_audit_names_final_report_and_contract_write_exception():
    paths = (
        Path(_THIS.COMMANDS_DIR) / "cleanup-audit.md",
        _REPO / "src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert ".claude-audit/final-report.md" in text, path.name
        assert re.search(
            r"Except under `--unattended`[^\n]*return-contract\.yaml", text
        ), path.name


def test_index_repo_output_format_states_where_the_files_land():
    text = (Path(_THIS.COMMANDS_DIR) / "index-repo.md").read_text(encoding="utf-8")
    section = text.split("## Output Format", 1)[1].split("\n## ", 1)[0]
    assert "root of the repository" in section


def test_init_lite_contract_exception_and_pass_through_are_documented():
    skill = (_REPO / "src/superclaude/skills/sc-init-lite-protocol/SKILL.md").read_text(
        encoding="utf-8"
    )
    invariants = skill.split("## 4. Safety Invariants", 1)[1].split("\n## ", 1)[0]
    assert "return-contract.yaml" in invariants
    assert "invariants 2 and 3" in invariants
    assert "never forwards" in skill
    command = (Path(_THIS.COMMANDS_DIR) / "init-lite.md").read_text(encoding="utf-8")
    activation = command.split("## Activation", 1)[1].split("\n## ", 1)[0]
    assert "--unattended" in activation and "--report-dir" in activation


def _artifacts_clause(text: str) -> str:
    """The rest of the line after the first `artifacts` key (backticked or YAML)."""
    line = next(
        ln for ln in text.splitlines() if re.search(r"`artifacts`|^artifacts:", ln)
    )
    return re.split(r"`artifacts`|^artifacts:", line, maxsplit=1)[1]


def test_wc4_states_the_ignored_path_exclusion():
    # The exclusion lives once in WC-4; command sections point at it.
    wc4 = _contract().split("- **WC-4.", 1)[1].split("\n- **WC-8.", 1)[0]
    for phrase in (
        "git ignores",
        "outside the repository",
        "every command's `artifacts` list",
    ):
        assert phrase in wc4, phrase


def test_init_lite_status_follows_the_tool_exit_code():
    # A partial scaffold exits non-zero, so it must never be `succeeded`.
    skill = (_REPO / "src/superclaude/skills/sc-init-lite-protocol/SKILL.md").read_text(
        encoding="utf-8"
    )
    status_line = next(ln for ln in skill.splitlines() if "`worker_status`" in ln)
    contract_line = next(
        ln
        for ln in _unattended_section("init-lite").splitlines()
        if ln.startswith("- **Contract.**")
    )
    for line in (status_line, contract_line):
        assert "`succeeded` when `superclaude init-lite` exited 0" in line, line
        assert "when the audit finished" not in line, line


def test_unattended_artifacts_list_only_files_the_run_wrote():
    # WC-4: `artifacts` is every other file written, so each list follows the run's
    # actual writes (PR #411 review: fixed lists over- and under-listed files).
    skill = (_REPO / "src/superclaude/skills/sc-init-lite-protocol/SKILL.md").read_text(
        encoding="utf-8"
    )
    for clause in (
        _artifacts_clause(_unattended_section("init-lite")),
        _artifacts_clause(skill),
    ):
        assert "`Scaffold:`" in clause and "`[]`" in clause and "--dry-run" in clause, (
            clause
        )
        assert "when `--scaffold` is set" not in clause, clause
        # A file written before a later scaffold write failed is still listed.
        assert "failed tool run" not in clause and "on a failed run" not in clause, (
            clause
        )
        assert "as each file is written" in clause or "as it is written" in clause, (
            clause
        )
    build = _artifacts_clause(_unattended_section("build"))
    assert "git check-ignore" in build and "paths git ignores are left out" in build, (
        build
    )
    assert "WC-4" in build and "git refuses" not in build, build
    assert not WRITE_VERB_RE.search(build), build
    test = _artifacts_clause(_unattended_section("test"))
    assert "paths git ignores are left out" in test and "WC-4" in test, test
    assert "`[]`" in test and not WRITE_VERB_RE.search(test), test
    cleanup = _artifacts_clause(_unattended_section("cleanup-audit"))
    assert "pass<N>-summary.md" in cleanup and "progress.json" in cleanup, cleanup
    for clause in (
        _artifacts_clause(_unattended_section("workflow")),
        _artifacts_clause(_WORKFLOW_RETURN_REF.read_text(encoding="utf-8")),
    ):
        assert "reflect" in clause and "deviation-patterns" in clause, clause
        assert "runs.jsonl" in clause and "left out" in clause, clause
        # The reason lives in WC-4; the clause only points at it.
        assert "WC-4" in clause and "git refuses" not in clause, clause


def test_explain_declares_write_under_tool_coordination():
    text = (Path(_THIS.COMMANDS_DIR) / "explain.md").read_text(encoding="utf-8")
    tools = text.split("## Tool Coordination", 1)[1].split("\n## ", 1)[0]
    # `TodoWrite` also contains "Write", so match the bullet itself.
    assert any(ln.startswith("- **Write**") for ln in tools.splitlines())


def test_business_panel_frontmatter_is_not_inside_a_code_fence():
    text = (Path(_THIS.COMMANDS_DIR) / "business-panel.md").read_text(encoding="utf-8")
    assert text.startswith("---\n")
    head = text.split("\n## ", 1)[0]
    assert not re.search(r"^```yaml", head, re.M)


def test_load_usage_line_declares_checkpoint_and_load_is_not_converted():
    text = (Path(_THIS.COMMANDS_DIR) / "load.md").read_text(encoding="utf-8")
    usage = text.split("## Usage", 1)[1].split("\n## ", 1)[0]
    assert "--checkpoint <name>" in usage
    assert "load" not in UNATTENDED_COMMANDS


def test_unattended_section_check_forbids_nested_text_without_a_nested_list():
    text = _SYNTHETIC_SECTION
    with pytest.raises(AssertionError):
        _check_unattended_section(text, {"flags": [], "phrases": []})


# --- full P1 set, AC-1.4 and nested propagation ----------------------------

# Commands that never get the section in P1 (later phases extend the converted set;
# the set-equality test above already fails for any other command with a section).
NOT_CONVERTED_IN_P1 = (
    "load",
    "pr-submit",
    "agent",
    "git",
    "help",
    "pm",
    "spawn",
    "swarm-wizard",
    "issue",
)

_ADVERSARIAL_SKILL = _REPO / "src/superclaude/skills/sc-adversarial-protocol/SKILL.md"
_WORKFLOW_RETURN_REF = (
    _REPO / "src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md"
)
_ADVERSARIAL_OWN_CONTRACT = "<output>/adversarial/return-contract.yaml"
_WORKER_CONTRACT_HEADING = "## Worker contract (`--unattended`)"


def _check_p1_set(commands, expect) -> None:
    assert len(commands) == 16, f"P1 lists {len(commands)} commands, not 16"
    assert len(set(commands)) == 16, "P1_COMMANDS has a duplicate"
    # The P2 entries arrive one task at a time, so `expect` may also hold any of
    # P2_COMMANDS; a name outside both sets, or a missing P1 name, fails.
    assert set(commands) <= set(expect) <= set(commands) | set(P2_COMMANDS), (
        f"UNATTENDED_EXPECT and P1_COMMANDS differ: {sorted(set(expect) ^ set(commands))}"
    )


def _check_no_section_in(names) -> None:
    for name in names:
        path = Path(_THIS.COMMANDS_DIR) / f"{name}.md"
        if path.exists():
            text = path.read_text(encoding="utf-8")
            assert not re.search(r"^## Unattended mode\s*$", text, re.M), (
                f"{name} has an `## Unattended mode` section"
            )


def _check_adversarial_skill(text: str) -> None:
    assert _ADVERSARIAL_OWN_CONTRACT in text, f"skill lacks {_ADVERSARIAL_OWN_CONTRACT}"


def _check_adversarial_section(section: str) -> None:
    assert "<output>/return-contract.yaml" in section, "section lacks the worker path"
    assert re.search(
        r"lists[^.\n]*`"
        + re.escape(_ADVERSARIAL_OWN_CONTRACT)
        + r"`[^.\n]*`artifacts`",
        section,
    ), "section does not say the worker contract lists the own contract in `artifacts`"


def _check_workflow_ref(text: str) -> None:
    assert _WORKER_CONTRACT_HEADING in text, "ref lacks the worker contract section"
    section = text.split(_WORKER_CONTRACT_HEADING, 1)[1].split("\n## ", 1)[0]
    assert "<report-dir>/return-contract.yaml" in section, "ref lacks the report path"
    assert "--report-dir" in section, "ref does not tie the file to --report-dir"
    assert re.search(r"pre-creation STOP\s*→\s*`failed`", section), (
        "ref does not cover pre-creation STOPs"
    )


def _check_brainstorm_research_nested(section: str) -> None:
    # P2 (D-P2-1): research-light runs /sc:research nested, research-deep is skipped.
    assert "nested/research-" in section, "section lacks the nested research directory"
    assert "research-deep is skipped" in section, "section lacks the research-deep skip"
    assert "research enrichment is off" not in section, "section keeps the P1 line"


def _check_nested_text(section: str, expect: dict) -> None:
    nested = expect.get("nested", [])
    for name in nested:
        assert f"nested/{name}-" in section, f"section lacks nested/{name}-"
    if not nested:
        assert "nested/" not in section, "section names a nested directory"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# (id, text getter, check, phrases whose removal must make the check fail)
_AC14_CASES = (
    (
        "adversarial-skill",
        lambda: _read(_ADVERSARIAL_SKILL),
        _check_adversarial_skill,
        [_ADVERSARIAL_OWN_CONTRACT],
    ),
    (
        "adversarial-section",
        lambda: _unattended_section("adversarial"),
        _check_adversarial_section,
        ["<output>/return-contract.yaml", "lists", "`artifacts`"],
    ),
    (
        "workflow-ref",
        lambda: _read(_WORKFLOW_RETURN_REF),
        _check_workflow_ref,
        [
            _WORKER_CONTRACT_HEADING,
            "<report-dir>/return-contract.yaml",
            "--report-dir",
            "pre-creation STOP",
        ],
    ),
    (
        "brainstorm-section",
        lambda: _unattended_section("brainstorm"),
        _check_brainstorm_research_nested,
        ["nested/research-", "research-deep is skipped"],
    ),
)
_AC14_REMOVALS = [
    (case, getter, check, phrase)
    for case, getter, check, phrases in _AC14_CASES
    for phrase in phrases
]


def test_p1_command_set_is_complete():
    _check_p1_set(P1_COMMANDS, UNATTENDED_EXPECT)
    for name in P1_COMMANDS:
        assert (Path(_THIS.COMMANDS_DIR) / f"{name}.md").exists(), name


def test_p1_set_check_fails_on_a_missing_extra_or_repeated_command():
    with pytest.raises(AssertionError):
        _check_p1_set(P1_COMMANDS[:-1], UNATTENDED_EXPECT)
    with pytest.raises(AssertionError):
        _check_p1_set(P1_COMMANDS + ("extra",), UNATTENDED_EXPECT)
    with pytest.raises(AssertionError):
        _check_p1_set(P1_COMMANDS[:-1] + (P1_COMMANDS[0],), UNATTENDED_EXPECT)
    without_test = {k: v for k, v in UNATTENDED_EXPECT.items() if k != "test"}
    with pytest.raises(AssertionError):
        _check_p1_set(P1_COMMANDS, without_test)
    with pytest.raises(AssertionError):
        _check_p1_set(P1_COMMANDS, dict(UNATTENDED_EXPECT, extra={}))
    # A P2 name is allowed beside the P1 names; a name in neither set is not.
    _check_p1_set(P1_COMMANDS, dict(UNATTENDED_EXPECT, **{P2_COMMANDS[0]: {}}))
    with pytest.raises(AssertionError):
        _check_p1_set(P1_COMMANDS, dict(UNATTENDED_EXPECT, **{"not-a-command": {}}))


@pytest.mark.parametrize("name", NOT_CONVERTED_IN_P1)
def test_unconverted_command_has_no_unattended_section(name):
    _check_no_section_in([name])


def test_no_section_check_fails_when_an_unconverted_command_has_one(
    tmp_path, monkeypatch
):
    cmds = tmp_path / "commands"
    cmds.mkdir()
    (cmds / "load.md").write_text(
        "# load\n\n## Unattended mode\n\nx\n", encoding="utf-8"
    )
    monkeypatch.setattr(_THIS, "COMMANDS_DIR", cmds)
    with pytest.raises(AssertionError):
        _check_no_section_in(["load"])
    # A command whose file does not exist is skipped.
    _check_no_section_in(["issue"])


@pytest.mark.parametrize(
    ("case", "getter", "check"),
    [(c[0], c[1], c[2]) for c in _AC14_CASES],
    ids=[c[0] for c in _AC14_CASES],
)
def test_ac_1_4_assertion_holds(case, getter, check):
    check(getter())


@pytest.mark.parametrize(
    ("case", "getter", "check", "phrase"),
    _AC14_REMOVALS,
    ids=[f"{c}:{p}" for c, _, _, p in _AC14_REMOVALS],
)
def test_ac_1_4_check_fails_when_phrase_removed(case, getter, check, phrase):
    text = getter()
    check(text)
    with pytest.raises(AssertionError):
        check(text.replace(phrase, ""))


def test_brainstorm_research_check_fails_on_the_p1_research_line():
    section = _unattended_section("brainstorm")
    with pytest.raises(AssertionError):
        _check_brainstorm_research_nested(section + "\nresearch enrichment is off\n")


@pytest.mark.parametrize("cmd", sorted(UNATTENDED_EXPECT))
def test_nested_propagation_text_matches_the_nested_list(cmd):
    _check_nested_text(_unattended_section(cmd), UNATTENDED_EXPECT[cmd])


# command -> nested commands that receive --unattended; each P2 task adds or extends
# its own key in the task that gives the command a nested call.
EXPECTED_NESTING = {
    "brainstorm": ["analyze", "adversarial", "research"],
    "workflow": ["reflect"],
    "release-split": ["brainstorm", "adversarial"],
    "auggie-review": ["impact"],
    "troubleshoot": ["adversarial", "workflow"],
    "task": ["impact", "troubleshoot"],
    "cli-eval": ["spec-panel", "adversarial", "document"],
    "reflect": ["adversarial", "workflow", "impact"],
    "tasklist": ["reflect", "task"],
}


def test_nested_lists_match_the_p2_nesting():
    listed = {c: e["nested"] for c, e in UNATTENDED_EXPECT.items() if e.get("nested")}
    assert listed == EXPECTED_NESTING


# --- the full P2 set, the nested pin, the gate sentences, the F1 clause (AC-2.1) ---


def _check_p2_set(p1, p2, expect) -> None:
    assert len(p2) == 15, f"P2 lists {len(p2)} commands, not 15"
    assert len(set(p2)) == 15, "P2_COMMANDS has a duplicate"
    assert set(p1).isdisjoint(p2), f"P1 and P2 share {sorted(set(p1) & set(p2))}"
    both = set(p1) | set(p2)
    assert set(expect) == both, (
        f"UNATTENDED_EXPECT differs from P1 + P2: {sorted(set(expect) ^ both)}"
    )
    assert len(expect) == 31, f"UNATTENDED_EXPECT has {len(expect)} entries, not 31"
    for name in (*p1, *p2):
        assert (Path(_THIS.COMMANDS_DIR) / f"{name}.md").exists(), f"{name}: no file"


def test_p2_command_set_is_complete():
    _check_p2_set(P1_COMMANDS, P2_COMMANDS, UNATTENDED_EXPECT)


_P2_SET_DEFECTS = {
    "missing": (P1_COMMANDS, P2_COMMANDS[:-1], UNATTENDED_EXPECT),
    "extra": (P1_COMMANDS, P2_COMMANDS + ("extra",), UNATTENDED_EXPECT),
    "repeated": (
        P1_COMMANDS,
        P2_COMMANDS[:-1] + (P2_COMMANDS[0],),
        UNATTENDED_EXPECT,
    ),
    "in-p1-too": (
        P1_COMMANDS,
        P2_COMMANDS[:-1] + (P1_COMMANDS[0],),
        UNATTENDED_EXPECT,
    ),
    "no-entry": (
        P1_COMMANDS,
        P2_COMMANDS,
        {k: v for k, v in UNATTENDED_EXPECT.items() if k != P2_COMMANDS[0]},
    ),
    "stray-entry": (P1_COMMANDS, P2_COMMANDS, dict(UNATTENDED_EXPECT, extra={})),
}


@pytest.mark.parametrize("defect", sorted(_P2_SET_DEFECTS))
def test_p2_set_check_fails_on_a_missing_extra_or_repeated_command(defect):
    with pytest.raises(AssertionError):
        _check_p2_set(*_P2_SET_DEFECTS[defect])


def test_p2_set_check_fails_when_a_command_file_is_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(_THIS, "COMMANDS_DIR", tmp_path)
    with pytest.raises(AssertionError):
        _check_p2_set(P1_COMMANDS, P2_COMMANDS, UNATTENDED_EXPECT)


def test_expected_nesting_is_the_spec_nesting():
    assert EXPECTED_NESTING == {
        "brainstorm": ["analyze", "adversarial", "research"],
        "workflow": ["reflect"],
        "tasklist": ["reflect", "task"],
        "reflect": ["adversarial", "workflow", "impact"],
        "release-split": ["brainstorm", "adversarial"],
        "task": ["impact", "troubleshoot"],
        "troubleshoot": ["adversarial", "workflow"],
        "auggie-review": ["impact"],
        "cli-eval": ["spec-panel", "adversarial", "document"],
    }


def _check_nested_lines(section: str, name: str) -> None:
    assert any(
        f"nested/{name}-" in ln and "--unattended" in ln for ln in section.splitlines()
    ), f"no line gives nested/{name}- together with --unattended"


_NESTED_PAIRS = [(c, n) for c, names in EXPECTED_NESTING.items() for n in names]


@pytest.mark.parametrize(
    ("cmd", "name"), _NESTED_PAIRS, ids=[f"{c}:{n}" for c, n in _NESTED_PAIRS]
)
def test_nested_call_passes_the_flag_and_a_nested_directory(cmd, name):
    section = _unattended_section(cmd)
    _check_nested_lines(section, name)
    stripped = "\n".join(
        ln.replace("--unattended", "") if f"nested/{name}-" in ln else ln
        for ln in section.splitlines()
    )
    with pytest.raises(AssertionError):
        _check_nested_lines(stripped, name)


def test_task_skill_returns_the_qa_halt_to_an_unattended_caller():
    # PR #422 review: the phase-gate QA halt and the unfixable-FAIL rule also ask a person.
    text = (_REPO / "src/superclaude/skills/task/SKILL.md").read_text(encoding="utf-8")
    para = next(
        p
        for p in text.split("\n\n")
        if p.startswith("The same applies to the two other")
    )
    for phrase in (
        "Phase-Gate QA step that halts after the second fix cycle",
        "Any step FAIL with unfixable issues",
        "returns the open blocking findings",
        "writes its blocked worker contract",
    ):
        assert phrase in para, phrase
        with pytest.raises(AssertionError):
            assert phrase in para.replace(phrase, "")


def test_reflect_skill_passes_the_nested_impact_directory():
    # Owner decision (2026-11-07): the UC-2 Step 1B.3 impact call is a nested call too.
    skill = (_REPO / "src/superclaude/skills/sc-reflect-protocol/SKILL.md").read_text(
        encoding="utf-8"
    )
    _check_nested_lines(skill, "impact")
    stripped = "\n".join(
        ln.replace("--unattended", "") if "nested/impact-" in ln else ln
        for ln in skill.splitlines()
    )
    with pytest.raises(AssertionError):
        _check_nested_lines(stripped, "impact")


# command, gate sentence (word for word), outcome words, the opposite words the
# reverse-outcome negative test substitutes. Built from the plan's Gate sentences.
_CLEANUP_GATE = 'every item under "Approval Required" is listed as not applied'
P2_GATES = [
    ("cleanup", _CLEANUP_GATE, "not applied", "applied"),
    ("improve", _CLEANUP_GATE, "not applied", "applied"),
    ("improve", "`--force` is refused", "refused", "honoured"),
    (
        "research",
        "an explicit `--strategy intent` or `--strategy unified` is refused",
        "refused",
        "honoured",
    ),
    (
        "spec-panel",
        "a TDD input without `--target-release` resolves as blocked",
        "blocked",
        "answered",
    ),
    (
        "recommend",
        "the one clarifying question resolves as blocked",
        "blocked",
        "asked",
    ),
    (
        "review-translation",
        "Phase 1 without `--context` resolves as blocked",
        "blocked",
        "confirmed",
    ),
    (
        "review-translation",
        "Phase 7 resolves to SKIP IMPLEMENTATION",
        "SKIP IMPLEMENTATION",
        "IMPLEMENT FIXES",
    ),
    (
        "release-split",
        "the tasklist-input warning resolves as blocked",
        "blocked",
        "prompted",
    ),
    (
        "release-split",
        "`--r1-scope custom` resolves as blocked",
        "blocked",
        "prompted",
    ),
    (
        "cli-portify",
        "each of the three approval gates resolves as blocked",
        "blocked",
        "approved",
    ),
    (
        "auggie-review",
        "`--unattended` implies `--no-post-pr` and `--no-remediation-offer`",
        "implies",
        "allows",
    ),
    (
        "auggie-review",
        "`--post-pr` and `--remediation-offer` are refused",
        "refused",
        "honoured",
    ),
    (
        "troubleshoot",
        "the short input STOP resolves as blocked",
        "blocked",
        "shown",
    ),
    (
        "troubleshoot",
        "the `--fix` offer resolves as blocked",
        "blocked",
        "shown",
    ),
    (
        "task",
        "confidence below 0.70 resolves as blocked",
        "blocked",
        "reported to the user",
    ),
    (
        "task",
        "every FULL STOP resolves as blocked",
        "blocked",
        "reported to the user",
    ),
    ("task", "EXEMPT `commit` and `push` are refused", "refused", "allowed"),
    (
        "cli-eval",
        "`run` without both `--suite` and `--output-dir` resolves as blocked",
        "blocked",
        "confirmed",
    ),
    (
        "cli-eval",
        "an FR-G5 preflight failure resolves as blocked",
        "blocked",
        "worked around",
    ),
    ("tdd", "a bare topic resolves as blocked", "blocked", "re-run"),
    (
        "tdd",
        "a TDD that is already complete resolves as blocked",
        "blocked",
        "re-run",
    ),
    (
        "tasklist",
        "the unresolved High or Medium HALT resolves as blocked",
        "blocked",
        "escalated",
    ),
    (
        "tasklist",
        "the `needs_human_decision` HALT resolves as blocked",
        "blocked",
        "escalated",
    ),
    (
        "reflect",
        "`--remediate` is answered by the headless auto-accept rule",
        "headless auto-accept rule",
        "yes/no prompt",
    ),
]


def _check_gate(section: str, sentence: str, outcome: str, opposite: str) -> None:
    assert sentence in section, f"section lacks the gate sentence: {sentence}"
    assert outcome in sentence, f"{outcome!r} is not in {sentence!r}"
    assert sentence.replace(outcome, opposite) not in section, (
        f"section also states the reversed gate: {opposite!r}"
    )


@pytest.mark.parametrize(
    ("cmd", "sentence", "outcome", "opposite"),
    P2_GATES,
    ids=[f"{g[0]}:{i}" for i, g in enumerate(P2_GATES)],
)
def test_p2_gate_resolution_is_stated(cmd, sentence, outcome, opposite):
    section = _unattended_section(cmd)
    _check_gate(section, sentence, outcome, opposite)
    reversed_gate = sentence.replace(outcome, opposite)
    # (1) the sentence removed; (2) the sentence kept with its outcome reversed;
    # (3) the reversed sentence added beside the right one.
    for broken in (
        section.replace(sentence, ""),
        section.replace(sentence, reversed_gate),
        section + "\n" + reversed_gate,
    ):
        with pytest.raises(AssertionError):
            _check_gate(broken, sentence, outcome, opposite)


F1_PHRASE = "paths git ignores are left out (WC-4)"


def _check_f1_clause(clause: str) -> None:
    assert F1_PHRASE in clause, f"artifacts clause lacks {F1_PHRASE!r}"
    assert "git add" not in clause, "artifacts clause names git add"
    assert "git refuses" not in clause, "artifacts clause names git refuses"


@pytest.mark.parametrize("cmd", P2_COMMANDS)
def test_p2_artifacts_clause_follows_f1(cmd):
    clause = _artifacts_clause(_unattended_section(cmd))
    _check_f1_clause(clause)
    for broken in (
        clause.replace(F1_PHRASE, ""),
        clause + " git refuses it",
        clause + " git add it",
    ):
        with pytest.raises(AssertionError):
            _check_f1_clause(broken)


def _check_workflow_reflect_wording(section: str) -> None:
    lines = section.splitlines()
    nested = next(ln for ln in lines if ln.startswith("- **Nested invocations.**"))
    contract = next(ln for ln in lines if ln.startswith("- **Contract.**"))
    assert "runs as today, without" not in nested, "old Nested invocations wording"
    assert "nested/reflect-" in nested and "--unattended" in nested, nested
    assert "`.dev/reflect/` run directory" not in contract, "old Contract wording"
    assert "`<report-dir>/nested/reflect-<n>/` run directory" in contract, contract


def test_workflow_section_passes_the_nested_reflect_directory():
    # P2 replaces the two P1 lines whose `.dev/reflect/` wording turns false under
    # --unattended (D-P2-22).
    section = _unattended_section("workflow")
    _check_workflow_reflect_wording(section)
    old_nested = (
        "- **Nested invocations.** The reflect step runs as today, without "
        "`--unattended` and without `--remediate`; in that form it has no gate."
    )
    pre_change_nested = re.sub(
        r"^- \*\*Nested invocations\.\*\*.*$",
        lambda _m: old_nested,
        section,
        flags=re.M,
    )
    with pytest.raises(AssertionError):
        _check_workflow_reflect_wording(pre_change_nested)
    with pytest.raises(AssertionError):
        _check_workflow_reflect_wording(
            section.replace(
                "`<report-dir>/nested/reflect-<n>/` run directory",
                "`.dev/reflect/` run directory",
            )
        )


_CLI_EVAL_RUN_REF = (
    _REPO / "src/superclaude/skills/sc-cli-eval-protocol/refs/run-pipeline.md"
)


def _check_eval_wait_limit(text: str) -> None:
    assert any("--unattended" in ln and "240 s" in ln for ln in text.splitlines()), (
        "no line names --unattended and a 240 s single-wait limit"
    )


def test_cli_eval_eval_wait_names_a_single_wait_limit_of_240_s():
    # spec AC-2.1: the eval wait step names a single-wait limit of at most 240 s.
    text = _read(_CLI_EVAL_RUN_REF)
    _check_eval_wait_limit(text)
    with pytest.raises(AssertionError):
        _check_eval_wait_limit(text.replace("240 s", ""))
    with pytest.raises(AssertionError):
        _check_eval_wait_limit(text.replace("--unattended", ""))


def test_nested_check_fails_on_nested_text_without_a_nested_list():
    # graph has an empty nested list, so any nested/ text in its section must fail.
    section = _unattended_section("graph")
    expect = UNATTENDED_EXPECT["graph"]
    _check_nested_text(section, expect)
    with pytest.raises(AssertionError):
        _check_nested_text(section + "\nnested/reflect-<n>/\n", expect)


# --- AC-0.9: git and GitHub write-verb audit -------------------------------
#
# Scans the installed primitives' source for git and gh write verbs. The hit
# unit is one matching line, keyed by repo-relative path, verb(s) and the
# stripped line text (never a line number). Every hit must be classified into
# exactly one category with a one-line reason:
#   wc9-allowed      allowed by WC-9 (/sc:implement's private-index snapshot, refs, revert)
#   deferred:<phase> the owning command is converted, or its write turned off under
#                    --unattended, in that phase of ./source.md section 6
#   never-worker     the owning command is on the never-as-worker list
#   no-command       no command converts this file; the reason says why
#   read-only        a read-only use or a false match (gh pr view/list/checks, a
#                    GET gh api call, or prose that forbids or describes the verb)
# WC-9's "a worker writes no git state" covers only the hits classified here.

AUDIT_ROOTS = (
    _REPO / "src" / "superclaude" / "skills",
    _REPO / "src" / "superclaude" / "commands",
    _REPO / "src" / "superclaude" / "agents",
)

# Whole words, not followed by a word character or "-", so `git merge-base`
# is not `git merge`. `git -C <path> <verb>` counts as `git <verb>`.
WRITE_VERB_RE = re.compile(
    r"\b(?:git(?:\s+-C\s+\S+)?\s+(?:add|commit|push|merge|stash|update-ref|worktree\s+(?:add|remove))"
    r"|gh\s+(?:pr|api))(?![\w-])"
)

_CATEGORY_RE = re.compile(
    r"^(?:wc9-allowed|deferred:P[1-4]|never-worker|no-command|read-only)$"
)

# A gh api call is a post when its method is not GET: an explicit non-GET
# method, or (no explicit GET and) a field flag or graphql, which make gh use POST.
_GH_API_METHOD_NOT_GET = re.compile(r"(?:--method|-X)\s+(?!GET\b)[A-Za-z]+")
_GH_API_METHOD_GET = re.compile(r"(?:--method|-X)\s+GET\b")
_GH_API_POST_HINT = re.compile(
    r"(?:^|\s)(?:-f|-F|--field|--raw-field|--input)(?=\s|=|$)|\bgh\s+api\s+graphql\b"
)


def _is_gh_api_post(line: str) -> bool:
    if not re.search(r"\bgh\s+api\b", line):
        return False
    if _GH_API_METHOD_NOT_GET.search(line):
        return True
    return not _GH_API_METHOD_GET.search(line) and bool(_GH_API_POST_HINT.search(line))


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(_REPO).as_posix()
    except ValueError:
        return path.relative_to(root.parent).as_posix()


def _scan_write_verbs() -> list:
    """Return (path, verb, stripped line, line number) for every hit line."""
    hits = []
    for root in map(Path, _THIS.AUDIT_ROOTS):
        for p in sorted(root.rglob("*")):
            if not p.is_file():
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for n, line in enumerate(text.splitlines(), 1):
                found = WRITE_VERB_RE.findall(line)
                if not found:
                    continue
                verbs = []
                for m in found:
                    verb = re.sub(r"\s+", " ", re.sub(r"\s+-C\s+\S+", "", m))
                    if verb not in verbs:
                        verbs.append(verb)
                hits.append((_rel(p, root), "+".join(verbs), line.strip(), n))
    return hits


def _check_all_classified() -> None:
    missing = sorted(
        {(path, verb, line) for path, verb, line, _ in _scan_write_verbs()}
        - set(WRITE_VERB_CLASSIFICATION)
    )
    assert not missing, "unclassified git/gh write-verb hits:\n" + "\n".join(
        f"{p} [{v}] {ln[:120]}" for p, v, ln in missing
    )


# (repo-relative path, verb(s), stripped line) -> (category, one-line reason)
WRITE_VERB_CLASSIFICATION = {
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "gh pr",
        '- **Wave 0 (all ordinals):** resolve the target repo once from the origin remote (`REPO="$(git remote get-url origin | sed -E \'s#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\\.git$##\')"`; only if origin has no URL, fall back to `gh repo view --json nameWithOwner -q .nameWithOwner` — never prefer it, because gh picks an `upstream` remote over `origin`) and the base branch (`gh repo view "$REPO" --json defaultBranchRef -q .defaultBranchRef.name`, overridable via `--base`). BEFORE creating anything: confirm `git remote -v` shows origin = `$REPO` and rebase if behind `origin/<base>` only at L0 (at L1+ the create path does not rebase and does not halt: the branch is already published when `gh pr create` runs, so report how many commits it is behind, a Tier 0 result; with `--pr <N>`, at any level, do not rebase: the PR head is already published, so report how many commits it is behind instead). At L1+, also before creating or attaching, run `scripts/probe-merge.sh --ops-only --repo "$REPO"`: a non-null `foreign_op` (a merge, rebase, cherry-pick, revert or sequencer operation in progress) → HALT before Wave 1 with status `terminal_halted`, reason `foreign_op_in_progress`, nothing created (on `--resume`, `conflict_resume_plan` in `refs/conflict-mechanical.md` decides first). Then open the PR with `gh pr create --repo "$REPO" --base <base> --head <head> --title "..." --body "..."` and verify the returned URL\'s `owner/repo` equals `$REPO` (a misroute → HALT). With `--pr <N>`, skip `gh pr create` and attach to that PR instead, checking the URL from `gh pr view <N> --repo "$REPO" --json url`. Pass `--repo "$REPO"` to every poll/reply/retrigger script too. At **L0 (`--monitor 0`)** the FSM never leaves `S0_IDLE` — open the PR and return, byte-for-byte identical to today (AC-1).',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "gh pr",
        '- **Wave 0 conflict check (L1+ only; L0 skips it):** after the head binding, read `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus` (re-read an `UNKNOWN` up to 3 times, 10 s apart) and normalise it with `superclaude.pr_submit.conflicts.mergeability_hint`. Only `conflicting` or a persistent `unknown` loads `refs/conflict-mechanical.md` and runs `scripts/probe-merge.sh`; follow that ref to classify, print the plan before any edit, and route with `conflict_action(hook="wave0")` (Tier 3 at L3 halts here: `terminal_halted`, reason `conflict_tier3`, nothing touched). Any other hint is Tier 0: report "<N> commits behind, no conflicts" (or the `BLOCKED` reason) and continue; no ref is loaded.',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "gh pr",
        "- **Wave 0 head binding (L1+ only; L0 skips it):** after `gh pr create`, or on `--pr <N>` attach, read the PR head with `gh pr view <N> --repo \"$REPO\" --json headRefName,headRefOid,isCrossRepository` (a failed or unparsable read → HALT) and the checkout with `git branch --show-current` and `git rev-parse HEAD`. Require `superclaude.pr_submit.fsm.pr_head_ok(local_branch, local_sha, headRefName, headRefOid, isCrossRepository, allow_cross_repo=(ordinal < 3))`; a head on a fork is allowed only below L3, where nothing is pushed. False → HALT before Wave 1 with status `terminal_halted`, reason `pr_head_mismatch` (appended to the run-log when one exists), and tell the operator: \"PR #<N>'s head `<headRefName>`@<headRefOid> does not match your checkout `<local_branch>`@<local_sha>. Do not close the PR. Check out `<headRefName>` and make it equal the PR head (push if you are ahead; `git pull --ff-only` if you are behind; this skill never rewrites a published branch), then re-run with `--pr <N>`.\" True → bind `HEAD_BRANCH := headRefName` and `pre_push_sha := headRefOid` for the whole run; every push targets `HEAD_BRANCH`, never the checkout's branch name. `--resume` repeats this binding against the live PR: when crash recovery finds a dangling `push_initiated`, check only the branch (`pr_branch_ok(local_branch, headRefName, isCrossRepository, allow_cross_repo=(ordinal < 3))` and `pr_branch_ok(<the record's target_branch>, headRefName, False)`), leave the SHA to `resolve_crash_window` (local HEAD may already be the fix commit), and set `pre_push_sha` from that record: its `target_sha` when the push landed (Branch A), its `pre_push_sha` when the push is re-driven (Branch B: skip the Wave 6 fix commit, set `target_sha` from the record, and the re-driven push first runs the Wave 6 pre-push head guard with the record's `pre_push_sha`; after Branch A, the guard's parent check stops the next push if local commits were made since the landed push); otherwise require the full `pr_head_ok` and set `pre_push_sha := headRefOid`.",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "gh pr",
        '- **Wave 8a (L1+, conflict act before the CI wait; same entry outcomes as Wave 8):** read `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,isCrossRepository` (same `UNKNOWN` re-reads). Only `conflicting` or a persistent `unknown` loads `refs/conflict-mechanical.md`, re-probes and acts on `conflict_action(hook="wave8a", entering=<review outcome>)`: at L3 a Tier 1 conflict becomes one sync merge commit pushed fast-forward (no round, no re-trigger, no reply, no resolve; the one push a wait-only path allows), then the CI wait runs on the new head with `expect_checks`; L2 leaves it resolved and validated but uncommitted (`halt_before_push`, only after `clean` / `REPORT_ONLY`); L1 proposes (also only after `clean` / `REPORT_ONLY`). A PR still conflicting with nothing pushed skips the CI wait with reason `pr_conflicting` (GitHub runs no `pull_request` checks on it) and ends with the status `conflict_action` returns. When any hook this run read `conflicting`, re-read `mergeable` before sending `transition(clean)`; `CONFLICTING` → `terminal_halted`, reason `late_conflict` (the Wave 8 late trigger re-enters this step).',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "git add+git commit+gh pr+git push+gh api",
        '- **Wave 6 (L3 only):** load `refs/thread-reply.md`. **Fix commit:** when the cycle applied edits (`applied_edits > 0`) and VAL is green, commit all of them as exactly one commit (one per cycle, never one per finding; VAL has already passed, so a validation retry never adds a second commit), staging only the files those edits changed (`git add -- <paths>`, never `git add -A` or `git add .`, which would sweep in run artifacts and other untracked files) and committing with `git commit --only -- <paths>` so nothing else already in the index is committed, and set `target_sha := git rev-parse HEAD`; every thread replied to in this cycle cites that one SHA. Before staging anything (before the `git add` above), if a path to commit is in `OPERATOR_PENDING`, append `terminal_halted` (reason `fix_commit_failed`), HALT with nothing committed or pushed, and tell the operator: "The fix touched files that had your own uncommitted changes: <paths>. Nothing was committed or pushed. Those files now hold both your changes and the fix: separate them by hand (do not discard the files), then re-run with `--pr <N>`." Otherwise, if the commit fails (for example a pre-commit hook rejects it) or HEAD did not advance, append `terminal_halted` (reason `fix_commit_failed`), HALT with nothing pushed, and tell the operator: "The fix commit failed (<error>). Nothing was pushed; the edits, and any changes a hook made, are in your working tree. Fix the cause, then either commit and push the fix yourself or discard it, and re-run with `--pr <N>`." A halted cycle replies to and resolves no thread. A crash re-drive (Branch B) skips this step and pushes the record\'s `target_sha`. **Pre-push head guard, before `push_decision`:** re-read `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` and require `pr_head_ok(<local branch>, pre_push_sha, headRefName, headRefOid, isCrossRepository)` and `headRefName == HEAD_BRANCH`. Compare the stored `pre_push_sha`, never local HEAD (local HEAD is the new fix commit). False → append `terminal_halted` (reason `pr_head_mismatch`), HALT with nothing pushed, write no push record, and tell the operator: "PR #<N>\'s head moved from <pre_push_sha> to <headRefOid> (or its branch is no longer `<HEAD_BRANCH>`) during the run. Nothing was pushed. Review the new PR commits, make your checkout equal the new PR head, then re-run with `--pr <N>`." When this cycle made a fix commit, the message adds: "This cycle\'s fixes are in local commit <target_sha>: drop it, or rebase it onto the new head and push it yourself." Next, when the cycle applied edits (a zero-edit cycle has no fix commit; INV-016 predicate 5 blocks its push and still records `push_decision`), read the parents of the commit to push (`git rev-list --parents -n 1 <target_sha>`, dropping the first id) and require `superclaude.pr_submit.fsm.push_parent_ok(<parents>, pre_push_sha)`: a fast-forward push publishes every commit between the PR head and `target_sha`, so the push may carry only this cycle\'s fix commit. False → append `terminal_halted` (reason `push_range_mismatch`), HALT with nothing pushed and no push record, and tell the operator: "Nothing was pushed. The fix commit <target_sha> sits on top of local commits that are not on PR #<N>: <`git log --oneline <pre_push_sha>..<target_sha>^`>. Publish those commits yourself if you want them on the PR, otherwise drop them; make your checkout equal the PR head, then re-run with `--pr <N>` (the open review threads are fixed again)." Then set `target_branch := HEAD_BRANCH`. The deterministic core DECIDES (evaluates the INV-016 conjunction, records the write-ahead push triad `push_decision` → `push_initiated` (fsynced BEFORE the push) → `push_completed`, keyed on the PRE-push idempotency key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>`); the SKILL performs the actual `git push origin <target_sha>:<target_branch>` (never an upstream parent remote, never the repo\'s default/protected branch, never a force push) ONLY when the conjunction holds, then set `pre_push_sha := target_sha`, then reply (citing `applied_edits` status — `applied_edits==0` says "no code change applied", never "resolved") and resolve via `scripts/reply-resolve-thread.sh` (reply FIRST, then resolve; the script finds the thread by its root comment id, so an Augment or a Codex root works the same). In a dedup group, **every verified member\'s thread** is replied to and resolved, all citing the cycle\'s one fix SHA; an unverified or Low/Nit member gets no reply and no resolve, and the report lists the group once with "flagged by: augment, codex". **S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT auto-trigger a re-review by either bot — AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`), post **one re-trigger comment per present reviewer** BEFORE re-entering the S5 poll: for each reviewer in `pending_retriggers(<run-log events>, cycle_id, <present reviewers>)` (the present reviewers that have no `rereview_requested` for this `cycle_id` yet), run `scripts/retrigger-review.sh --pr <N> --repo "$REPO" --body "<retrigger_phrase(contract, reviewer)>"` (`auggie review` for Augment, `@codex review` for Codex). The core decides whether/when to re-trigger (`do_retrigger` seam, INV-R1: at most once per push cycle, `rereview_request_count <= max_rounds`, counted per cycle, not per comment); the script does the `gh api` issue-comment POST (NFR-6). Right after each reviewer\'s successful POST, take that reviewer\'s UTC watermark and append a **`rereview_requested{cycle_id, reviewer, timestamp}`** run-log event with that time (the INV-R1 producer — folded into `rereview_request_count` by distinct `cycle_id` in `rebuild_state`, and consumed by crash recovery\'s OQ-1 resume decision: a landed-push crash with NO `rereview_requested` for its cycle resumes at `S5a_RETRIGGER_REVIEW` to re-post; one WITH it resumes at `S5_AWAITING_REREVIEW`). **Resume of a re-triggered cycle:** reuse the `cycle_id` of the dangling push record (never a new one); on every resume at `S5a_RETRIGGER_REVIEW` or `S5_AWAITING_REREVIEW`, first call `pending_retriggers` and post the reviewers still missing (a crash between the Augment and the Codex post neither skips Codex nor re-posts Augment), then take each reviewer\'s watermark from the `timestamp` of its latest `rereview_requested` for the cycle before the S5 poll. The `round_counter` ticks only when the subsequent poll attributes the re-review to our pushed SHA (the relocated INV-001 increment) — a timed-out re-trigger does NOT advance the counter.',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md",
        "gh api",
        "gh api repos/<owner/repo>/commits/<sha>/check-runs --jq .total_count",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md",
        "gh api",
        "gh api repos/<owner/repo>/commits/<sha>/status --jq .total_count",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md",
        "gh pr",
        "No `conclusion` field — `gh pr checks --json` does not emit it. Empty, malformed, or multiple-document stdout is **not** a parsed empty array. A valid nonempty required list takes precedence; otherwise a valid all-checks list is used. If the chosen list is empty and either query failed to parse, emit `state:polling`, `checks:[]`; only two parsed empty arrays, with `expect_checks` false, justify `clean`; with `expect_checks` true an empty chosen list is `polling` (see Expected checks after a push). Pending exit 8 may still contain valid JSON — keep it.",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md",
        "git add",
        "git add -- <path>",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh api",
        'gh api "repos/${REPO}/commits/<base_sha>/check-runs" --jq \'.check_runs[] | "\\(.name) \\(.conclusion)"\'',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh pr",
        'gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh pr",
        'gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,isCrossRepository',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh pr",
        'gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh pr",
        'gh pr view <N> --repo "$REPO" --json mergeStateStatus',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh pr",
        'gh pr view <N> --repo "$REPO" --json mergeable',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "gh pr",
        '| `resume_unrepresentable` (row 4b\') | `--resume` with an open conflict cycle whose dangling push no crash record matches | The merge commit `<target_sha>` of cycle `<cycle_id>` may or may not be on the PR. Nothing more was pushed. If the PR head (`gh pr view <N> --repo "$REPO" --json headRefOid`) equals it, re-run with `--pr <N>`; otherwise push or drop it yourself, then re-run. |',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "git add",
        "- Tier 2: follow `refs/conflict-intent.md` (Tier 2 only), one file at a time (J-40), staging each finished path with `git add -- <path>` or `git rm -- <path>` (J-56); then any `regen:*` path by its rule above, after the precheck. A Tier 2 halt condition: abort, `sync_tier3`.",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "git add",
        "git add -- uv.lock",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "git commit+git merge",
        '**Step 8. L2 stops here** (`resolve_local`): append `sync_concluded{left_in_progress}`, status `halt_before_push`, and print: "The merge of `origin/<base>`@<base_sha> is resolved and validated but not committed. Review it, then run `git commit` yourself and push; or `git merge --abort`."',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "git merge",
        "git merge --abort",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md",
        "git push",
        "git push origin <target_sha>:<HEAD_BRANCH>",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh",
        "git commit",
        'if ! git commit -F "$MESSAGE_FILE" >"$TMP/commit.out" 2>&1; then',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh api",
        'RUNS="$(gh api "repos/${REPO}/commits/${EVIDENCE_SHA}/check-runs?per_page=1" --jq .total_count 2>/dev/null)" || RUNS=""',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh api",
        'STATUSES="$(gh api "repos/${REPO}/commits/${EVIDENCE_SHA}/status" --jq .total_count 2>/dev/null)" || STATUSES=""',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        "#           repo, or `gh pr checks --json` support, which evidence mode skips).",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "| **PR** | `<PR-num>` or `<PR-URL>` | `gh pr view <id> --json number,headRefName,baseRefName,headRepository,headRepositoryOwner,title,body,files` |",
    ): ("read-only", "gh pr view/diff reads the PR; no write"),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "| `pr_review_url` | string | URL of the posted `gh pr review` comment (empty if `--no-post-pr` or non-PR target) |",
    ): (
        "deferred:P2",
        "auggie-review PR posting (gh pr review --comment, inline gh api comments) is off under --unattended (WC-9); the deferral is in force",
    ),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "- PR: fetch `gh pr view <id> --json number,headRefName,baseRefName,title,body,files,url,headRepositoryOwner,headRepository` and the merge-base diff range",
    ): ("read-only", "gh pr view/diff reads the PR; no write"),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "- PR: `gh pr diff <id>` → `<output-dir>/diff.patch`",
    ): ("read-only", "gh pr view/diff reads the PR; no write"),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "- PR: from the `files` field of `gh pr view`",
    ): ("read-only", "gh pr view/diff reads the PR; no write"),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "- Summary comment: `gh pr review <PR> --comment --body-file <output-dir>/REVIEW.md`",
    ): (
        "deferred:P2",
        "auggie-review PR posting (gh pr review --comment, inline gh api comments) is off under --unattended (WC-9); the deferral is in force",
    ),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh api",
        "gh api repos/<owner>/<repo>/pulls/<PR>/comments \\",
    ): (
        "deferred:P2",
        "auggie-review PR posting (gh pr review --comment, inline gh api comments) is off under --unattended (WC-9); the deferral is in force",
    ),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "- Capture the review URL from `gh pr view <PR> --json reviews -q '.reviews[-1].url'` and record it.",
    ): ("read-only", "gh pr view/diff reads the PR; no write"),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "- Use `gh pr review --approve` or `--request-changes` — strictly `--comment`",
    ): (
        "read-only",
        "false match: forbids gh pr review --approve/--request-changes; no write",
    ),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/SKILL.md",
        "gh pr",
        "| `gh pr review` post fails | Save the body to `<output-dir>/REVIEW.md`, surface the path to the user, status `partial` | None |",
    ): (
        "deferred:P2",
        "auggie-review PR posting (gh pr review --comment, inline gh api comments) is off under --unattended (WC-9); the deferral is in force",
    ),
    (
        "src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md",
        "gh pr",
        "This recommendation is the report's first-paragraph verdict. It does NOT translate into a `gh pr review --approve` or `--request-changes` — those decisions belong to the human. The report is always posted as a `--comment` review.",
    ): (
        "read-only",
        "false match: states the report never becomes gh pr review --approve/--request-changes",
    ),
    (
        "src/superclaude/skills/sc-crash-recovery/SKILL.md",
        "git stash",
        "allowed-tools: Read, Glob, Grep, Bash(ls *), Bash(find *), Bash(wc *), Bash(cat *), Bash(head *), Bash(tail *), Bash(stat *), Bash(git status *), Bash(git diff *), Bash(git log *), Bash(git stash *), Bash(git branch *), Bash(git ls-files *), Bash(~/.claude/skills/sc-crash-recovery/scripts/*), Bash(~/workspace/IronClaude/.claude/skills/sc-crash-recovery/scripts/*), Task",
    ): (
        "no-command",
        "sc-crash-recovery has no /sc: command to convert; this is its tool allowlist (Bash(git stash *)), used for read-only stash inspection",
    ),
    (
        "src/superclaude/skills/sc-crash-recovery/SKILL.md",
        "git commit",
        '- **No artifacts found anywhere**: say so plainly. "No in-flight pipeline state detected. Most recent activity: <last git commit / last session log timestamp>." Don\'t fabricate work.',
    ): (
        "read-only",
        "false match: prose naming the last git commit as a timestamp source",
    ),
    (
        "src/superclaude/skills/sc-crash-recovery/refs/investigators.md",
        "git stash",
        "- git -C <PROJECT_PATH> stash list",
    ): ("read-only", "git stash list only reads the stash"),
    (
        "src/superclaude/skills/sc-implement-protocol/SKILL.md",
        "git stash",
        "Else snapshot HEAD + tracked diffs + untracked (non-ignored) files **without** staging in the user index (`git stash create` omits untracked):",
    ): (
        "wc9-allowed",
        "/sc:implement private-index snapshot or refs/superclaude/implement/ ref, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/SKILL.md",
        "git add",
        '`idx=$(mktemp); GIT_INDEX_FILE="$idx" git read-tree HEAD && GIT_INDEX_FILE="$idx" git add -A && start=$(GIT_INDEX_FILE="$idx" git write-tree); rm -f "$idx"`',
    ): (
        "wc9-allowed",
        "/sc:implement private-index snapshot or refs/superclaude/implement/ ref, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/SKILL.md",
        "git update-ref",
        '`git update-ref "refs/superclaude/implement/<slug>/T<id>" "$start"` (managed: `<slug>` is the package id)',
    ): (
        "wc9-allowed",
        "/sc:implement private-index snapshot or refs/superclaude/implement/ ref, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/SKILL.md",
        "git update-ref",
        "On task `complete`, delete the Q0 pin `git update-ref -d \"refs/superclaude/implement/<slug>/T<id>\"` and the task's checkpoint refs (`refs/retry.md`); keep its sweep refs. The final summary lists each kept sweep ref with one `git update-ref -d <ref>` line for the operator. The task's reviewed-tree refs `retry/T<rid>/r<k>-<j>` (`refs/qa.md`) are deleted at `complete` once `first=` and `origin=` are written; sweep refs are kept.",
    ): (
        "wc9-allowed",
        "/sc:implement private-index snapshot or refs/superclaude/implement/ ref, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/SKILL.md",
        "git add",
        'Untracked files in the touched set are part of the review package: if the path exists in `$start`, diff vs `git show "$start:<path>"`; else include full new-file contents (`git diff --no-index -- /dev/null <file>` or Read). Do not `git add` to the user index for this snapshot (that is not the `.dev/tasks/` rule: `.dev/tasks/` is always staged, `git add .dev/tasks`). An empty `git diff` with new untracked writes is not `cannot-verify`.',
    ): (
        "deferred:P4",
        "/sc:implement is converted in P4; under --unattended its .dev/tasks staging defers to the coordinator (WC-9)",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/ledger.md",
        "git add",
        "One markdown file per run. Append-only. UTF-8, `\\n` endings, no wrapping of record lines. Do not `git add` a legacy ledger under `.dev/implement/`. A managed package's ledger (`<pkg>/progress.md`) sits under `.dev/tasks/`, which is always staged (`git add .dev/tasks`).",
    ): (
        "deferred:P4",
        "/sc:implement is converted in P4; under --unattended its .dev/tasks staging defers to the coordinator (WC-9)",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md",
        "git add",
        '- `.dev/tasks/` is always staged (`git add .dev/tasks`): the package, its `progress.md` ledger and `artifacts/` included. Never gitignore it, never leave it untracked, and never write "do not stage" about it in a ledger note or report. Staging is not committing. After the helper moves a package to `done/`, the new path needs `git add .dev/tasks` again.',
    ): (
        "deferred:P4",
        "/sc:implement is converted in P4; under --unattended its .dev/tasks staging defers to the coordinator (WC-9)",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
        "git update-ref",
        "1. **Procedure step 1, checkpoint.** From `$top` (Names), snapshot the worktree with the Q0 temp-index sequence (Q0 in `SKILL.md`) into tree `c`. Append `T<id>: retry n=<k+1> step=open checkpoint=<c> tier=<tier>`. Then `git update-ref <checkpoint ref> <c>`. No commit object is made, no git identity is needed, and no branch or index changes. The `step=open` record is written **before** `update-ref`, so a failed ref write never leaves the k = 2 failure without its feature marker (Resume row P in `refs/ledger.md`).",
    ): (
        "wc9-allowed",
        "/sc:implement retry ladder: private-index snapshot, checkpoint and sweep refs, and revert, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
        "git update-ref",
        "The checkpoint ref only pins the failed attempt's tree for recovery and for `attempt-<k>.diff`; it never drives the revert. On any resume into this escalation, re-run `git update-ref <checkpoint ref> <recorded sha>`. Every `r<k>-<j>` ref of the task is also re-pinned from its recorded tree (review header or repair `applied tree=` line, `refs/qa.md`). If the ref held another value (another linked worktree with the same slug), print `checkpoint ref moved; re-pinned to the recorded tree <sha>` and continue. If `update-ref` fails, STOP `E-RESUME-NEEDED reason=ref-failed` with no ledger line; the `step=open` record already exists, so resume retries. Halt messages print the recorded sha, not only the ref name (Halts and transient stops).",
    ): (
        "wc9-allowed",
        "/sc:implement retry ladder: private-index snapshot, checkpoint and sweep refs, and revert, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
        "git add",
        '&& GIT_INDEX_FILE="$idx" git -C "$1" add -A 2>/dev/null \\',
    ): (
        "wc9-allowed",
        "/sc:implement retry ladder: private-index snapshot, checkpoint and sweep refs, and revert, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
        "git update-ref",
        'git -C "$top" update-ref "$ref" "$now" "" || { echo "sweep ref write failed: $ref" >&2; return 4; }',
    ): (
        "wc9-allowed",
        "/sc:implement retry ladder: private-index snapshot, checkpoint and sweep refs, and revert, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
        "git update-ref",
        'Before restoring, pin `now` as `refs/superclaude/implement/<slug>/retry/T<rid>/sweep-<k>-<seq>` with `git update-ref <ref> <now> ""` (create-only; `<seq>` is the next free integer). On a resumed revert, if a `sweep-<k>-*` ref exists, keep it and take a new `<seq>` only when `now` differs from it. Print the sweep ref at every revert.',
    ): (
        "wc9-allowed",
        "/sc:implement retry ladder: private-index snapshot, checkpoint and sweep refs, and revert, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
        "git update-ref",
        "At `complete`, delete the Q0 pin and the task's checkpoint refs `a<k>`, but keep its sweep refs: they are the only copy of bytes a revert replaced. The final summary lists them with one `git update-ref -d <ref>` line each for the operator. The task's reviewed-tree refs `retry/T<rid>/r<k>-<j>` (`refs/qa.md`) are also deleted at `complete` once `first=` and `origin=` are written; sweep refs are kept.",
    ): (
        "wc9-allowed",
        "/sc:implement retry ladder: private-index snapshot, checkpoint and sweep refs, and revert, allowed by WC-9",
    ),
    (
        "src/superclaude/skills/sc-post-release-protocol/SKILL.md",
        "git worktree add+git worktree remove",
        "**Anchor the scan to the tagged commit.** Once the tag is resolved, read the release's code surface **at that tag** — e.g. `git show <tag>:<path>`, `git ls-tree <tag>`, or a `git worktree add` / `git archive` checkout of the tag — rather than the current working tree. Such a checkout is made in a temporary directory and removed with `git worktree remove` after the scan. Confirm the tag actually belongs to the release lineage (`git merge-base --is-ancestor <tag> <default-branch>`); if it is **not** an ancestor of the mainline, or the tree's version metadata disagrees with the tag, treat that as a release-integrity finding and report it before proceeding. **Auto-detect the default branch** (e.g. `git symbolic-ref refs/remotes/origin/HEAD`) — do not assume `main`/`master`.",
    ): (
        "deferred:P4",
        "/sc:post-release is converted in P4 with every outward and git-writing step off under --unattended (decision D4)",
    ),
    (
        "src/superclaude/skills/sc-post-release-protocol/SKILL.md",
        "git add",
        "- **Never stage machine-generated / sync-output dirs** — respect whatever the host repo marks as generated or vendored (check its `.gitignore` and docs) and don't `git add` those paths. Note the convention varies: some repos gitignore such dirs, others commit them — follow the host repo's actual practice, don't assume.",
    ): (
        "deferred:P4",
        "/sc:post-release is converted in P4 with every outward and git-writing step off under --unattended (decision D4)",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "gh pr",
        'unless both hold: (1) `gh pr checks --repo "$REPO" --help` lists `--json` (probe the installed CLI;',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "gh pr",
        "Wave 0: Open PR + verify target   ← (no ref; gh pr create --repo, pre-PR checks)",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md",
        "git add",
        "- `git add` any `.claude/` path except `.claude/settings.json`.",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md",
        "gh api",
        "(`scripts/poll-augment-review.sh`) performs a single `gh`/`gh api` poll and emits one JSON line; the",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md",
        "gh api",
        "> Every `gh`/`gh api` call below pins the RESOLVED `--repo <owner/repo>` (origin's `owner/repo`,",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md",
        "gh pr",
        "gh pr view <N> --repo <owner/repo> --json number,url,headRefName,headRefOid,baseRefName",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md",
        "gh api",
        "gh api repos/<owner/repo>/pulls/<N>/reviews --method GET -F per_page=100 -F page=1",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md",
        "gh api",
        "gh api repos/<owner/repo>/issues/<N>/comments --method GET -F per_page=100 -F page=1",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md",
        "gh api",
        "gh api repos/<owner/repo>/pulls/<N>/comments --method GET -F per_page=100 -F page=1",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md",
        "gh pr",
        "gh pr view <N> --repo <owner/repo> --json number,url,headRefOid,mergeable,mergeStateStatus",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md",
        "gh pr",
        "gh pr checks <N> --repo <owner/repo> --required --json name,state,bucket,link,workflow",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md",
        "gh pr",
        "gh pr checks <N> --repo <owner/repo> --json name,state,bucket,link,workflow",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md",
        "gh api",
        "> **NOTE (core-purity boundary, NFR-6 / T-104, NOT T-N50).** This ref documents a `gh api …",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md",
        "gh api",
        "> seam); the `gh api` I/O lives in `scripts/retrigger-review.sh`.",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md",
        "gh api",
        'gh api --method POST repos/<owner/repo>/issues/<N>/comments -f body="auggie review"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md",
        "gh api",
        "`gh api .../comments` or an upstream-parent path is a **T-104-class defect**. `gh api` takes no",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md",
        "gh pr+gh api",
        "(`--repo <owner/repo>` for `gh pr`; `repos/<owner/repo>/...` path for `gh api`; the GraphQL",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md",
        "gh api",
        'gh api --method POST repos/<owner/repo>/pulls/<N>/comments/<COMMENT_ID>/replies -f body="<reply-text>"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md",
        "gh api",
        "gh api graphql -f query='",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md",
        "gh api",
        "comment via `gh api --method POST repos/<owner/repo>/issues/<N>/comments -f body=...`),",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh",
        "gh pr",
        'if ! gh pr view "$PR" --repo "$REPO" \\',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh",
        "gh api",
        'issue) gh api "repos/${REPO}/issues/${PR}/comments" --method GET -F per_page=100 -F page="$page" ;;',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh",
        "gh api",
        'inline) gh api "repos/${REPO}/pulls/${PR}/comments" --method GET -F per_page=100 -F page="$page" ;;',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh",
        "gh api",
        'reviews) gh api "repos/${REPO}/pulls/${PR}/reviews" --method GET -F per_page=100 -F page="$page" ;;',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh",
        "gh api",
        "gh api graphql -f query='",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh",
        "gh pr",
        'if ! gh pr view "$PR" --repo "$REPO" --json headRefOid > "$_tmp/head.json" 2>/dev/null \\',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        'CHECKS_HELP="$(gh pr checks --repo "$REPO" --help 2>/dev/null || true)"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        "*) die \"installed gh lacks 'gh pr checks --json' (see 'gh --version'); upgrade gh and confirm via 'gh pr checks --help' before CI wait\" 2 ;;",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        'PR_JSON="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid,mergeable,mergeStateStatus 2>/dev/null || true)"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        "# gh pr checks exits 8 on pending while still printing JSON. Do not `|| echo '[]'`",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        'REQUIRED_JSON="$(gh pr checks "$PR" --repo "$REPO" --required --json "$JSON_FIELDS" 2>/dev/null || true)"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        'ALL_JSON="$(gh pr checks "$PR" --repo "$REPO" --json "$JSON_FIELDS" 2>/dev/null || true)"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
        "gh pr",
        'PR_AFTER="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid,mergeable,mergeStateStatus 2>/dev/null || true)"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh",
        "gh api",
        "#           isolated here (NFR-6). gh api paths pin the RESOLVED repos/${REPO}/...",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh",
        "gh api",
        "gh api graphql -f query='",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh",
        "gh api",
        'gh api --method POST "repos/${REPO}/pulls/${PR}/comments/${COMMENT_ID}/replies" \\',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh",
        "gh api",
        "#           All gh I/O is isolated here (NFR-6). The gh api path pins the RESOLVED",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh",
        "gh api",
        "gh api --method POST \\",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh",
        "gh pr",
        'answer="$(gh pr view "$PR" --repo "$REPO" --json state,isDraft,headRefOid,autoMergeRequest 2>/dev/null)" || return 1',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh",
        "gh api",
        'if count="$(gh api --paginate "repos/${REPO}/issues/${PR}/timeline" --jq \'.[] | select(.event=="convert_to_draft" or .event=="ready_for_review") | .event\' 2>/dev/null | wc -l | tr -d \' \')"; then',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh",
        "gh pr",
        'gh pr ready "$PR" --repo "$REPO" --undo >/dev/null 2>&1 || { emit_to false false mutation_failed; exit 1; }',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh",
        "gh pr",
        'gh pr ready "$PR" --repo "$REPO" >/dev/null 2>&1 || { emit_to false false mutation_failed; exit 1; }',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md",
        "gh pr",
        'gh pr ready <N> --repo "$REPO"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/commands/pr-submit.md",
        "gh pr",
        'gh pr ready <N> --repo "$REPO"',
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git worktree add",
        "2. **STOP-on-non-committable predicate (COR-1)** — `committable = base resolves AND HEAD resolves AND not audit_tree_dirty`. If NOT committable, the wrapper STOPs with `status: stopped-precondition` (verdict BLOCKED, exit 2 — the fail-closed contract is unchanged) and `reason ∈ {dirty, no-committable-ref, head-moved-precondition, snapshot-precleanup-failed, worktree-add-failed}` (any non-zero `git worktree add` exit STOPs with the captured stderr, never falling back to the live tree). It never points reviewers at a committed-ref snapshot that omits the uncommitted target.",
    ): (
        "deferred:P2",
        "/sc:reflect review-snapshot worktree; the snapshot is created only by the superclaude reflect run --isolate-reviewers CLI wrapper and never under /sc:reflect --unattended; the deferral is in force",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git worktree add",
        "3. **Snapshot creation (COR-2 / A-2)** — on the committable path, pre-clean a leftover `<output>/_review-snapshot`, re-resolve HEAD immediately before `git worktree add --detach <output>/_review-snapshot <ref>` and STOP `head-moved-precondition` on drift (the parallel-session HEAD-moved hazard), then create a REAL worktree checkout (NOT an archive, so auggie stays indexed).",
    ): (
        "deferred:P2",
        "/sc:reflect review-snapshot worktree; the snapshot is created only by the superclaude reflect run --isolate-reviewers CLI wrapper and never under /sc:reflect --unattended; the deferral is in force",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git worktree remove+git stash",
        "5. **`finally` teardown (A-3)** — the snapshot is always removed via `git worktree remove --force` (never `rm -rf` / `git stash`), on success / STOP / exception, while the always-write sidecar still emits inside the try.",
    ): (
        "deferred:P2",
        "/sc:reflect review-snapshot worktree; the snapshot is created only by the superclaude reflect run --isolate-reviewers CLI wrapper and never under /sc:reflect --unattended; the deferral is in force",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git commit+git push+git stash+git merge",
        "**No-mutation gate.** Independently of (b)/(c), any command matching the mutation denylist (`git commit`/`git push`, the read-but-forbidden working-tree git verbs `git reset` / `git stash` / `git checkout` / `git clean` / `git rebase` / `git merge` / `git worktree` / `git restore` — i.e. `git <any mutation>` as a broad backstop — `pip install`, `rm`, or any redirect to a repo path outside `<output>/`) is rejected with `verify_blocked_reason: \"mutation-denied\"` and never invoked. In-test side effects (a test that writes fixtures within its own scope) are best-effort only (OQ-M7) — the gate governs the *command*, not the test internals. **(L3 defense-in-depth — NOT the incident vector.)** These git verbs are enumerated as a backstop only: control (b)'s verb allowlist is a CLOSED set (`{pytest, ruff, mypy, make, uv, npm, tsc, cargo}`) that already rejects EVERY git verb because `git` is absent from it, so no git command can reach this gate through the orchestrator's verification call. The reflect-reviewer mutation incident vector traveled the **reviewer-persona Bash-tool / L1** path (all-tools reviewer personas), which L1 + L2 close; §6.1.1 governs only the orchestrator-driven verification call, so this denylist extension is strictly defense-in-depth and does not by itself close the incident vector.",
    ): ("read-only", "false match: lists git verbs the no-mutation gate denies"),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git add",
        "**Git status.** Reflect does NOT `git add` moved files. Operator stages and commits. The `task` adapter moves folders under `.dev/tasks/`, which is always staged (`git add .dev/tasks`): re-stage it after the move.",
    ): (
        "read-only",
        "false match: states reflect does not run git add or must stop on git add -f; staging is the operator's",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git add",
        "- **`git add` after promotion.** Filesystem-level move only; the operator stages and commits.",
    ): (
        "read-only",
        "false match: states reflect does not run git add or must stop on git add -f; staging is the operator's",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
        "git add",
        "**The `-f` rule (CLAUDE.md ABSOLUTE).** If `git add` requires `-f` on any `.claude/` path (except `.claude/settings.json`), that `-f` is the violation siren. STOP. Move the change to `src/superclaude/`, run `make sync-dev`, stage only the `src/` side. See memory `feedback_claude_dir_gitignored.md`.",
    ): (
        "read-only",
        "false match: states reflect does not run git add or must stop on git add -f; staging is the operator's",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git add",
        "If `git add` requires `-f` on **any** `.claude/` path (except `.claude/settings.json`), STOP. The `-f` is the violation siren — it means you are about to commit `.claude/{skills,commands,agents,hooks,templates}/*` content, which is **gitignored sync-dev output** of `src/superclaude/`.",
    ): (
        "read-only",
        "false match: the -f staging prohibition for .claude/ paths; no write",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git add",
        "1. STOP the `git add -f` attempt. Do not retry with `-f` removed against the same path.",
    ): (
        "read-only",
        "false match: the -f staging prohibition for .claude/ paths; no write",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git add",
        "**Why the `-f` is the signal:** A successful `git add` against a `.claude/` path means the file was either (a) already tracked from before the gitignore landed, or (b) staged with `-f`. Case (a) is grandfathered; case (b) is the violation. The `-f` flag is the only signal that distinguishes the two at staging time, which is why this rule lives at the CLAUDE.md level and not just in a pre-commit hook — the hook catches commits, not stages, and the human eye must catch the `-f` before it gets that far.",
    ): (
        "read-only",
        "false match: the -f staging prohibition for .claude/ paths; no write",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git add",
        "- Task-file instructions that name `.claude/` staging steps. If a task file says `git add .claude/skills/foo/`, the task file itself is wrong — escalate to fix the task file, do not follow it.",
    ): (
        "read-only",
        "false match: the -f staging prohibition for .claude/ paths; no write",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git add",
        "- **`.gitignore`** — catches any workspace that bypassed the hook (e.g., out-of-band file creation). Such a workspace cannot be staged without `git add -f`, which then triggers the `-f` rule above.",
    ): (
        "read-only",
        "false match: the -f staging prohibition for .claude/ paths; no write",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git add",
        "5. **Stage ONLY `src/` and `.dev/` paths.** NEVER stage `.claude/` paths. If `git status` shows `.claude/skills/sc-reflect-protocol/` changes after step 2, that is expected sync output — leave it unstaged. If `git add` ever requires `-f` for a `.claude/` path, apply the `-f` rule above.",
    ): (
        "no-command",
        "maintainer pre-commit procedure for editing the reflect skill in this repo; no command runs it",
    ),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md",
        "git commit",
        '**`mutation-denied` (FR-4.5).** Trigger: a verification command matched the no-mutation denylist (`git commit`/`push`, `pip install`, `rm`, repo-path redirect). Emits `verify_blocked: true` + `verify_blocked_reason: "mutation-denied"`; the command is never invoked.',
    ): ("read-only", "false match: lists commands the no-mutation denylist blocks"),
    (
        "src/superclaude/skills/sc-reflect-protocol/refs/promotion-adapters.md",
        "git add",
        "Reflect does NOT `git add` moved files. Operator stages and commits both the original promotion and any subsequent rollback. A `task` adapter move or rollback changes paths under `.dev/tasks/`, which is always staged (`git add .dev/tasks`).",
    ): (
        "read-only",
        "false match: states reflect does not git add moved files; the operator stages",
    ),
    (
        "src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md",
        "gh api",
        "- **Verdict source**: only when the failing arm is an identified CI job, fetch the failing arm's job log to `<output-dir>/job-<id>.log` *before* reading any verdict; the verdict is the last line in that log matching the harness's result marker, never the workflow- or job-level conclusion; no marker line ⇒ `verdict: unobservable`, `status: blocked` (not a fabricated failing test result). Non-CI artifacts retain their source/run provenance and use their own result format; an absent verdict is unknown, not FAIL, and requires no job-log download. Worked example only (not a mandatory tool): `gh run view <run-id> --json jobs --jq '.jobs[]|[.databaseId,.name,.conclusion]'` then `gh api repos/<owner>/<repo>/actions/jobs/<id>/logs > <output-dir>/job-<id>.log`; marker `^RESULT:` (a `--log-failed` view is empty under continue-on-error). Validator A8 checks the log exists at finalize.",
    ): (
        "read-only",
        "gh api fetch of a CI job log or raw source file; a read, no -f/-F and no write method",
    ),
    (
        "src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md",
        "gh api",
        "- Fetch verbatim: `mcp__context7__query-docs` → remote URL fetch → raw source fetch (e.g. `gh api`); paste the returned lines into `tier1-observation.md` under `## Behaviour definitions` with source coordinates; Status `fetched:<source>`",
    ): (
        "read-only",
        "gh api fetch of a CI job log or raw source file; a read, no -f/-F and no write method",
    ),
    (
        "src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md",
        "gh api",
        "| `mcp__context7__query-docs` | Conditional behaviour-definition fetch before S1.6.4 pairs and Tier 1 calibration; same fallback chain as Tier 2 | ✓ when framework/library named; behaviour-definition fetch (Wave 3 step 1; fallback `WebFetch` → raw source fetch, e.g. `gh api`) | — |",
    ): (
        "read-only",
        "gh api fetch of a CI job log or raw source file; a read, no -f/-F and no write method",
    ),
    (
        "src/superclaude/skills/sc-workflow-protocol/SKILL.md",
        "git add",
        '`.dev/tasks/` is always staged (`git add .dev/tasks`): the package and its `artifacts/` included. Never gitignore it, never leave it untracked, and never write "never stage" about it in a generated plan (Constraints included). Staging is not committing.',
    ): (
        "deferred:P1",
        "/sc:workflow is converted in P1; under --unattended the deferral of its .dev/tasks staging to the coordinator is in force (WC-9)",
    ),
    (
        "src/superclaude/skills/task/SKILL.md",
        "git add",
        "Under the centralized path convention, each task file lives inside its own folder: `.dev/tasks/to-do/TASK-[ID]/TASK-[ID].md`. All intermediate artifacts (research, synthesis, QA reports) go into typed subfolders within that folder. The task folder is the self-contained workspace for the entire execution. `.dev/tasks/` is always staged (`git add .dev/tasks`); never gitignore it or leave it untracked. Staging is not committing.",
    ): (
        "deferred:P2",
        "the MDTM task skill runs as tdd's nested /task, converted in P2; under --unattended its .dev/tasks staging is left to the coordinator (WC-9); the deferral is in force",
    ),
    (
        "src/superclaude/skills/task-builder/SKILL.md",
        "git add",
        "Compute `<subject>` from the goal slug of the user's request using the rules in the Subject Derivation section. If no clean subject is derivable, use `general`. Create the task folder: `.dev/tasks/to-do/TASK-RF-<subject>-YYYYMMDD-HHMMSS/` with subfolders `research/` and `qa/`. For multi-track: `.dev/tasks/to-do/TASK-RF-track-T-YYYYMMDD-HHMMSS/` per track. `.dev/tasks/` is always staged (`git add .dev/tasks`); never gitignore it or leave it untracked. Staging is not committing.",
    ): (
        "deferred:P2",
        "task-builder is reached through tdd, reflect --remediate and troubleshoot --fix, converted in P2; under --unattended its staging is left to the coordinator and its CLI-mode reflect gate (git add -A, --fix, --promote) is skipped (WC-9); the deferral is in force",
    ),
    (
        "src/superclaude/skills/task-builder/SKILL.md",
        "git add",
        '- **Action**: Ensure new task artifacts are staged so the working-tree diff is complete (`git add -A`, because the wrapper\'s audit omits never-`git add`-ed files). Then emit the recursion-breaker-guarded wrapper shell-out as a single Bash command: first the §3.2 skip guard `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi`, then `superclaude reflect run {TASK_FILE} --depth deep --fix --promote`. `{TASK_FILE}` is the absolute tasklist path (the wrapper absolutizes its positional). NO `--base` is passed: the wrapper resolves the audit base from frontmatter `start_commit` as a SINGLE ref diffed against the working tree (so uncommitted task edits ARE audited; this is why a single-ref base is correct where a `start_commit..HEAD` range would not be). Base precedence is `--base` > frontmatter `start_commit` > `git merge-base HEAD master` (contract §6). `--depth deep` is fixed (O4 (CLI mode) fixes the POST depth at `deep`, forcing Tier-2 fan-out); `--fix` runs the bounded auto-fix loop; `--promote` lets the `task` adapter move the tasklist dir to `done/` on a clean/auto-fixed PASS. Emit NO `--reflect`, NO `--max-turns`, NO `<base>..HEAD` range, and no agent-spawn directive of any kind (the gate is a flat shell-out, never a subagent, per NFR-7 it carries none of the nesting tokens). Consume the EXIT CODE: only `0` completes the gate (clean OR auto-fixed-and-verified); `10` (halted: human-required deviations / non-convergent fix loop), `11` (degraded: audit untrustworthy), and `2` (blocked: child crash / missing-or-bad contract) all FAIL -> surface the wrapper report and HALT before Update-status-to-Done. The gate uses `superclaude reflect run` and never `/sc:task`; any re-execution uses `/task`.',
    ): (
        "deferred:P2",
        "task-builder is reached through tdd, reflect --remediate and troubleshoot --fix, converted in P2; under --unattended its staging is left to the coordinator and its CLI-mode reflect gate (git add -A, --fix, --promote) is skipped (WC-9); the deferral is in force",
    ),
    (
        "src/superclaude/commands/auggie-review.md",
        "gh pr",
        "- **Remote PR**: `<PR-number>` or `<PR-URL>` (resolved via `gh pr view`)",
    ): ("read-only", "gh pr view/diff reads the PR; no write"),
    (
        "src/superclaude/commands/auggie-review.md",
        "gh pr+gh api",
        "| `--post-pr` | `true` when target is a PR | Auto-post the markdown report as a `gh pr review --comment`. Inline comments for `Critical` and `High` findings via `gh api`. **No confirmation prompt — the user opted in by invoking the command on a PR.** |",
    ): (
        "deferred:P2",
        "auggie-review PR posting (gh pr review --comment, inline gh api comments) is off under --unattended (WC-9); the deferral is in force",
    ),
    (
        "src/superclaude/commands/git.md",
        "git commit",
        "/sc:git commit --smart-commit",
    ): (
        "never-worker",
        "/sc:git is on the never-as-worker list; its commit and merge examples run only in the coordinator or person session",
    ),
    (
        "src/superclaude/commands/git.md",
        "git merge",
        "/sc:git merge feature-branch --interactive",
    ): (
        "never-worker",
        "/sc:git is on the never-as-worker list; its commit and merge examples run only in the coordinator or person session",
    ),
    (
        "src/superclaude/commands/pr-submit.md",
        "gh pr",
        "**STOP** if `--monitor >= 1` and the CI-wait preflight fails: `gh pr checks --repo <owner/repo> --help` must list `--json`, and the runtime must import `superclaude.pr_submit.ci`. The skill's CI-wait preflight is authoritative.",
    ): (
        "never-worker",
        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
    ),
    (
        "src/superclaude/agents/issue-worker-t1.md",
        "gh pr+gh api",
        '- **Read-only GitHub access.** You make read-only `gh` calls only, always with the `--repo <R>` the orchestrator gave you (for example `gh issue view <N> --repo <R> --json body,comments` or `gh pr list --repo <R> --state merged --limit 200 --json number,files`); a `gh api` call reads the path `user` or a path that starts with `repos/<R>/`, never a brace placeholder. You never write to GitHub or ClickUp: never `gh issue edit <N> --repo <R>`, `gh issue comment <N> --repo <R>`, `gh issue create --repo <R>`, `gh label create "<name>" --repo <R>`, a `gh api` call with `-X`/`--method` other than `GET`, or any ClickUp request. The orchestrator makes every write.',
    ): (
        "read-only",
        "the /sc:issue worker agents make read-only gh calls (gh issue view, gh pr list, a GET gh api); the line describes or forbids writes, it makes none",
    ),
    (
        "src/superclaude/agents/issue-worker-t2.md",
        "gh pr+gh api",
        '- **Read-only GitHub access.** You make read-only `gh` calls only, always with the `--repo <R>` the orchestrator gave you (for example `gh issue view <N> --repo <R> --json body,comments` or `gh pr list --repo <R> --state merged --limit 200 --json number,files`); a `gh api` call reads the path `user` or a path that starts with `repos/<R>/`, never a brace placeholder. You never write to GitHub or ClickUp: never `gh issue edit <N> --repo <R>`, `gh issue comment <N> --repo <R>`, `gh issue create --repo <R>`, `gh label create "<name>" --repo <R>`, a `gh api` call with `-X`/`--method` other than `GET`, or any ClickUp request. The orchestrator makes every write.',
    ): (
        "read-only",
        "the /sc:issue worker agents make read-only gh calls (gh issue view, gh pr list, a GET gh api); the line describes or forbids writes, it makes none",
    ),
    (
        "src/superclaude/agents/issue-worker-t3.md",
        "gh api",
        '- **Read-only GitHub access.** You make read-only `gh` calls only, always with the `--repo <R>` the orchestrator gave you; a `gh api` call reads the path `user` or a path that starts with `repos/<R>/`, never a brace placeholder. You never write to GitHub or ClickUp: never `gh issue edit <N> --repo <R>`, `gh issue comment <N> --repo <R>`, `gh issue create --repo <R>`, `gh label create "<name>" --repo <R>`, a `gh api` call with `-X`/`--method` other than `GET`, or any ClickUp request. The orchestrator makes every write.',
    ): (
        "read-only",
        "the /sc:issue worker agents make read-only gh calls (gh issue view, gh pr list, a GET gh api); the line describes or forbids writes, it makes none",
    ),
    (
        "src/superclaude/agents/issue-worker-t3.md",
        "gh api+gh pr",
        '1. **Claim lookup (claim Wave 1).** Run `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author` and `gh api user -q .login`. List pull requests merged since `createdAt` with `gh pr list --repo <R> --state merged --search "merged:>=<createdAt date>" --limit 200 --json number,title,mergedAt,files,url`, and record whether the result reached the 200 limit. Run `git fetch origin`, then `git log --since=<createdAt> --name-only origin/<default branch>`. Find this user\'s earlier comments whose body contains `<!-- sc:issue:claim -->` or `<!-- sc:issue:accuracy-check -->` and record each comment ID. Write `<D>/scout.md` from the claim section of the `scout-report.md` template: state, `url`, `is_pull_request` (true when `url` contains `/pull/`), assignees, current login, earlier comment IDs, merged pull requests and changed files since creation, whether that list was truncated, and a first complexity guess (`simple|medium|complex`) and type guess (`feature|bug`), each with a one-line reason.',
    ): (
        "read-only",
        "a read: gh issue view, gh pr list or a GET gh api user call",
    ),
    (
        "src/superclaude/skills/sc-issue-protocol/SKILL.md",
        "gh api",
        "- Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or spells `repos/<R>/...`, never a brace placeholder.",
    ): (
        "read-only",
        "prose: every gh call passes --repo and every gh api path is user or repos/<R>/; it names no write",
    ),
    (
        "src/superclaude/skills/sc-issue-protocol/SKILL.md",
        "gh api",
        "- The orchestrator (this skill) is the only place that writes to GitHub or ClickUp: `gh issue edit <N> --repo <R> --add-assignee @me`, `gh issue comment <N> --repo <R> --body-file <file>`, `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<file>`, `gh issue create --repo <R> ...` and `scripts/clickup_claim.py`. Workers never write to either.",
    ): (
        "never-worker",
        "/sc:issue is on the never-as-worker list; its assign, comment and issue writes run only in the coordinator or person session",
    ),
    (
        "src/superclaude/skills/sc-issue-protocol/SKILL.md",
        "gh api",
        "| `gh issue comment <N> --repo <R>` or the `gh api -X PATCH repos/<R>/issues/comments/<id>` edit fails | STOP `E-POST-FAILED`; files stay in `.dev/issues/<N>/`; a re-run edits rather than duplicates because of the markers |",
    ): (
        "never-worker",
        "/sc:issue is on the never-as-worker list; its assign, comment and issue writes run only in the coordinator or person session",
    ),
    (
        "src/superclaude/skills/sc-issue-protocol/refs/claim.md",
        "gh api",
        "- runs `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author` and `gh api user -q .login`;",
    ): (
        "read-only",
        "a read: gh issue view, gh pr list or a GET gh api user call",
    ),
    (
        "src/superclaude/skills/sc-issue-protocol/refs/claim.md",
        "gh api",
        "2. Claim comment: write `<D>/claim-comment.md` from `templates/claim-comment.md`: who claimed it, the ClickUp result from `clickup.json`, the summary overview, effort estimate, complexity, accuracy verdict, the first next step, and repo-relative links to `<D>/issue-summary.md`, `<D>/next-steps.md` and `<D>/analysis/` with the one-line note that they open on GitHub only after someone commits and pushes the files (default D9). It ends with `<!-- sc:issue:claim -->`. Edit the earlier claim comment with `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/claim-comment.md`, or post it with `gh issue comment <N> --repo <R> --body-file <D>/claim-comment.md`.",
    ): (
        "never-worker",
        "/sc:issue is on the never-as-worker list; its assign, comment and issue writes run only in the coordinator or person session",
    ),
    (
        "src/superclaude/skills/sc-issue-protocol/refs/claim.md",
        "gh api",
        "Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or starts with `repos/<R>/`, never a brace placeholder. Only the orchestrator writes to GitHub or ClickUp.",
    ): (
        "read-only",
        "prose: every gh call passes --repo and every gh api path is user or repos/<R>/; it names no write",
    ),
    (
        "src/superclaude/skills/sc-issue-protocol/refs/claim.md",
        "gh api",
        "`gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/accuracy-check.md`",
    ): (
        "never-worker",
        "/sc:issue is on the never-as-worker list; its assign, comment and issue writes run only in the coordinator or person session",
    ),
    (
        "src/superclaude/skills/sc-issue-protocol/refs/claim.md",
        "gh pr",
        '- lists pull requests merged since `createdAt` with `gh pr list --repo <R> --state merged --search "merged:>=<createdAt date>" --limit 200 --json number,title,mergedAt,files,url` (gh\'s default limit is 30) and records in `scout.md` whether the result reached the 200 limit;',
    ): (
        "read-only",
        "a read: gh issue view, gh pr list or a GET gh api user call",
    ),
    (
        "src/superclaude/skills/sc-issue-protocol/refs/create.md",
        "gh api",
        "Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or starts with `repos/<R>/`, never a brace placeholder. Only the orchestrator writes to GitHub. Create mode makes no ClickUp call and no self-assignment (B6).",
    ): (
        "read-only",
        "prose: every gh call passes --repo and every gh api path is user or repos/<R>/; it names no write",
    ),
    (
        "src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md",
        "gh pr",
        "1. Check that no pull request is already open or merged for this branch: `gh pr list --repo <R> --head <branch> --state all`. If one exists, stop and report it; do not commit or push.",
    ): (
        "read-only",
        "a read: gh pr list on the fork, run by the launched agent before it commits",
    ),
    (
        "src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md",
        "git commit",
        "2. Commit with `git commit` and a conventional-commit message. Stage `.dev/tasks` and the files you changed; never anything under `.claude/` and never `.dev/issues/`.",
    ): (
        "never-worker",
        "/sc:issue is on the never-as-worker list; this instruction is rendered into the launched agent's prompt only when the owner passes --submit, and no worker runs it",
    ),
    (
        "src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md",
        "git commit+git push",
        "Level: worktree. Follow the steps of `next-steps.md` up to the line `Plan boundary: after step <K>` (the number after `after step` is the last step you may run before a human approves). If the line reads `Plan boundary: before step 1`, there is nothing to run yet. Do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`.",
    ): (
        "read-only",
        "prose that forbids the verbs: the worktree level never commits or pushes",
    ),
    (
        "src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md",
        "git push",
        "3. Push the current feature branch with `git push origin <branch>`, never `master` or `main`.",
    ): (
        "never-worker",
        "/sc:issue is on the never-as-worker list; this instruction is rendered into the launched agent's prompt only when the owner passes --submit, and no worker runs it",
    ),
}


def test_every_write_verb_hit_is_classified():
    _check_all_classified()


def test_classification_table_has_no_stale_entries():
    live = {(path, verb, line) for path, verb, line, _ in _scan_write_verbs()}
    stale = sorted(set(WRITE_VERB_CLASSIFICATION) - live)
    assert not stale, "classified lines no longer present:\n" + "\n".join(
        f"{p} [{v}] {ln[:120]}" for p, v, ln in stale
    )


@pytest.mark.parametrize(
    "key", sorted(WRITE_VERB_CLASSIFICATION), ids=lambda k: f"{k[0]}:{k[1]}"
)
def test_each_classification_has_one_category_and_a_reason(key):
    category, reason = WRITE_VERB_CLASSIFICATION[key]
    assert _CATEGORY_RE.match(category), f"bad category {category!r}"
    assert reason.strip() and "\n" not in reason, "each hit needs a one-line reason"


def test_read_only_entries_are_not_gh_api_posts():
    posts = [
        k
        for k, (cat, _) in WRITE_VERB_CLASSIFICATION.items()
        if cat == "read-only" and _is_gh_api_post(k[2])
    ]
    assert not posts, f"gh api posts classified read-only: {posts}"


def test_write_verb_regex_matches_whole_words_only():
    assert not WRITE_VERB_RE.search("git merge-base master HEAD")
    assert not WRITE_VERB_RE.search("git add-on")
    assert WRITE_VERB_RE.search("git merge feature")
    assert WRITE_VERB_RE.search('git -C "$top" update-ref "$ref" "$now"')
    assert WRITE_VERB_RE.search("gh pr view 12")


def test_gh_api_post_detection():
    assert _is_gh_api_post(
        'gh api --method POST repos/o/r/issues/1/comments -f body="x"'
    )
    assert _is_gh_api_post("gh api graphql -f query='")
    assert _is_gh_api_post('gh api repos/o/r/issues/1/comments -f body="x"')
    assert not _is_gh_api_post(
        "gh api repos/o/r/pulls/1/reviews --method GET -F per_page=100"
    )
    assert not _is_gh_api_post("gh api repos/o/r/actions/jobs/1/logs")


def test_audit_fails_on_unclassified_write_verb(tmp_path, monkeypatch):
    scratch = tmp_path / "skills" / "scratch-skill"
    scratch.mkdir(parents=True)
    (scratch / "SKILL.md").write_text(
        "# scratch\n\nRun `git push origin main` when done.\n", encoding="utf-8"
    )
    monkeypatch.setattr(_THIS, "AUDIT_ROOTS", (tmp_path / "skills",))
    assert _scan_write_verbs() == [
        (
            "skills/scratch-skill/SKILL.md",
            "git push",
            "Run `git push origin main` when done.",
            3,
        )
    ]
    with pytest.raises(AssertionError, match="unclassified"):
        _check_all_classified()
