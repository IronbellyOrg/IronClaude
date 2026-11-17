Release 2 of the Orca observer: coordinator questions list, one named Run, --types question, observer-side retention, 100-row cap disclosure, as in .dev/tasks/to-do/TASK-RESEARCH-phase2-gate-20261111-200400/RESEARCH-REPORT-phase2-gate.md and .dev/issues/409/owner-decisions-20261111.md. Code: the observe package (src/superclaude/) and tests/observe

---

Coordinator brief the prompt above summarises (pasted by the owner; the requirements the plan must cover):

TASK: Write the implementation plan for release 2 (phase 2) of the Orca terminal observer (`superclaude observe`, issue #409). Planning only. Branch 409-Phase2, based on origin/master 9e2608b03 (release 1 merged as PR #503).

INPUTS
- Gate research report: RESEARCH-REPORT-phase2-gate.md in the folder TASK-RESEARCH-phase2-gate-20261111-200400 under .dev/tasks/ (sections 7 to 9: what the plan must contain, integration checklist 8.1 to 8.7).
- Owner decisions: .dev/issues/409/owner-decisions-20261111.md (decision 8: only type `question` messages, labelled "coordinator questions", not "human"; decision 6: read permission granted for one named Run, `--types question`, never `run-use`).
- Spec folder .dev/issues/409/bmad/spec-orca-observer/ (release-gates.md, adapter-contract.md, acceptance-tests.md including T51, unverified-register.md, owner-decisions-and-risks.md) and the PRD .dev/issues/409/bmad/prd-orca-observer/prd.md (phase 2 section).
- The shipped release 1 code under src/superclaude/cli/observe/ and tests/observe/. The plan must fit the existing structure.

PLANNING BASIS (fixed by the owner and the evidence; not reopened)
- One named Run only. No rotation across Runs (a terminal bound to another Run is fenced with `consumer_fenced`). Never call `run-use`. The observer must run where it already holds the Run.
- Every read passes `--types question`: an unfiltered `check --all` returns only the newest 100 rows and on the coordinator's own Run 91 of those 100 were heartbeats; `--types question` returned 41 rows.
- Non-consuming reads: `check --all` and `check --peek` did not consume, tested as the Run's owner only. `--all` rows carry no read/acknowledged marker, so a handled question looks like a fresh one; `--peek` hides rows once acked. Plan observer-side retention accordingly (the spec's phase 2 retention).
- The 100-row cap is disclosed in the UI with the label "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost".
- Question identity is `message.id` (msg_...); never a worker dispatchId. Seen on probe and own-Run data only: keep it labelled UNVERIFIED for other Runs.
- Still UNVERIFIED and must appear in the plan as gated risks with a named verification task, not as assumptions: reading from an unbound observer terminal (Q-1), the effect of `run-use` on a live coordinator (Q-2, forbidden anyway), message rate on a Run other than the coordinator's own.

PLAN MUST INCLUDE: the gate-text rewrite tasks (release-gates.md, unverified-register.md, prd.md:106 per report 8.1), fake-runner tests for the new argv and the `consumer_fenced` and `no_active_terminal` responses, the 100-row cap fixture, the T51 quiet-scope test, recorded redacted samples of success, missing, stale, contradictory (data-gate rule in release-gates.md), and acceptance criteria per task.

SAFETY: no consuming read (`check` without --all/--peek, `check --ack`) or `run-use` against any Run other than a throwaway created for the purpose; UV only; fork only (every gh call passes --repo IronbellyOrg/IronClaude); never stage `.claude/` mirrors; no commit, push or PR.

Command options: --depth standard --handoff none.
