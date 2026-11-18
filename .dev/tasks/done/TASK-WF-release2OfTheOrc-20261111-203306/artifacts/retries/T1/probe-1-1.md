4ebf9de17a892b2a3ee7d55809187ea87e2297d7
family: identity-overclaim (message.id attributed to own-Run data)
cmd: grep -n -F -e 'own-Run data' -e 'own Run' -- .dev/issues/409/bmad/spec-orca-observer/release-gates.md
coupled sites: release-gates.md Question identity bullet only
before:
38:**Status line: QUESTION-OBSERVATION: not passed.** Rewritten 2026-11-11 to match the gate research (`RESEARCH-REPORT-phase2-gate.md`, "REPORT" below, in `.dev/tasks/to-do/TASK-RESEARCH-phase2-gate-20261111-200400/`, evidence files 01 to 27 in its `research/evidence/` folder) and the owner's answers (`.dev/issues/409/owner-decisions-20261111.md`, "OWNER" below). Everything stated as observed below was seen only on the two probe Runs or on the coordinator's own Run, as the owner of that Run. Nothing here is verified for any other Run.
44:- **Proof (c), UNVERIFIED (REPORT 2.1).** The real message rate is not measured on any Run other than the coordinator's own. Measured facts only: the read is bounded at 100 rows; `--all` returns the newest 100 first and `--peek` returns the oldest 100 first (probe Run B, 104 messages, evidence files 14 and 15); there is no total, `hasMore` or truncation field; about 0.2 s per call on a probe Run (evidence file 16). The coordinator's own Run, as the owner measured it (OWNER, "Coordinator measurement"): 100 rows with `check --all` and no type filter (91 heartbeat, 8 worker_done, 1 question), and 41 rows with `--types question`, so the cap applies after the type filter. A measured rate does not prove completeness, so the label stays `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost` after the gate.
46:- **Question identity: `message.id` (`msg_...`), seen on probe data and own-Run data (REPORT 2.1 and 2.2, OWNER), UNVERIFIED for any other Run.** A worker `dispatchId` is never a question's identity.
after:
38:**Status line: QUESTION-OBSERVATION: not passed.** Rewritten 2026-11-11 to match the gate research (`RESEARCH-REPORT-
44:- **Proof (c), UNVERIFIED (REPORT 2.1).** No real message rate is recorded for any Run (REPORT: "the real message rat
46:- **Question identity: `message.id` (`msg_...`), seen on the probe Runs only (REPORT 2.2 and gap G-8, "identity candi
