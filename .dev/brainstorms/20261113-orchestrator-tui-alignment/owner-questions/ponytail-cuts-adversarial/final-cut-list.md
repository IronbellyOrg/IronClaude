<!-- Provenance: produced by /sc:adversarial --depth quick (Mode B) -->
<!-- Base: Variant 2 (sonnet:security); merge date: 2026-11-16 -->

# Final cut list after the debate (2026-11-16)

Result of the debate in `adversarial/` (three variants, three advocates, 31 diff points, converged). **Recommendations from agents. Nothing here is an owner answer or a grant.** Read `open-decisions.md` in the parent folder for what each Q means. Source list: `source-cut-candidates.md` (C01 to C22).

## 1. Cuts that survived and need only a document edit (executed by the orchestrating session)
<!-- Source: Base (original) -->
| Cut | What changes in `open-decisions.md` | Default that applies (not an owner answer) |
|---|---|---|
| C16 | No new owner questions about the switched-off questions panel | The panel stays off |
| C04 Q13 | Card becomes one line. Keep: the observer's Orca finder needs an `orca-cli` topic, but the discovery probe runs the candidate program once (`/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/src/superclaude/cli/install_user_setup.py:259`) | The contract note records both rules as facts, no verdict |
| C05 Q15 | Card becomes one line plus a caveat: person-started sessions are never messaged (`WORKER-CONTRACT.md:288`), watcher-started sessions are not covered by that sentence | v2 reports only |
| C06 Q14 | Labelled default; options 2 and 3 dropped; never make a code change a start gate | The v2 rewrite sentence says "default" |
| C07 Q8, C08 Q22, C09 Q30, C10 Q20, C11 Q29 | Moved to "Deferred" with a named event each | Each card's own "if you do not answer" outcome |
| C03 Q41 | Not closed; kept as a one-line confirmation ("Q41: confirm A"), no card | Plan Task 19 already records A |

## 2. Cuts that survived in a smaller form and stay open for the owner today
<!-- Source: Variant 2 (sonnet:security), Section C01, C02 -->
- **Q7 (C01).** Shrunk to a local backup of `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp` with a sha256 list kept outside git. **No push and no commit.** A backup is not the owner's approval of the pass record. The owner writes the confirming line separately.
- **Q24 (C02).** Shrunk to two read-only captures (`orca-ide worktree ps --agent-wait --json`, `orca-ide orchestration worker-show --dispatch <one live id> --json`; both in the sweep allow list at `probes.py:52` and `:58-59`). The worker-id comparison and the message-write test are deferred, not erased: they answer different questions. The output file stays untracked unless the owner says otherwise (the owner accepted public artifacts for now).

## 3. New standing hold
<!-- Source: Variant 2 (sonnet:security), Section C23b -->
- **C23b.** Commits `1ae72e1a1` and `f104ca51a` (unpushed, in `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp`) do not go into any pull request or merge until the owner confirms the pass record. `1ae72e1a1` sets `QUESTION_GATE_PASSED = True` on a record its own message calls "typed by the executor from the owner's words"; `f104ca51a` repoints it to a first-person record headed "Written by the owner", which git cannot attribute.

## 4. Survived, but needs a code change or a new owner decision (NOT executed)
- **C19.** Add one line to the sweep report saying the `working` class is off. One source file and its test; needs a branch and a pull request through `/sc:pr-submit --monitor 3`. Not a cut. Not started.
- **C12.** The debate kept the GitHub approval input as decided (Decision 3). Only one advocate would ask whether the comment input (marked "ideally", its rules still unconfirmed) can wait until the label path has run live; the other two said keep it as decided. So it is **not raised as a question**; `open-decisions.md` section 3 item 12 mentions it as the one piece that could be dropped if you want less to build.
- **C14.** Recommendation to the route B plan: run the throwaway delivery test (`worker-start`, `ask`, `reply`) before the GitHub-reading tasks, and keep Task 16 first and unblocked. The plan lives in a separate worktree; not edited here.

## 5. Cuts that did NOT survive (kept as they are)
| Item | Why |
|---|---|
| C12 as a cut, C13 | Override your Decision 3 and your Q39 "remove now". C13 stays as planned |
| C15 delete `slo_numbers` | A documented operator step still calls it; deferred |
| C17 delete the questions panel, C21 delete the gate rule and constant | Reverses the staged direction; the rule and the pinned tests guard a live read of coordinator messages |
| C18 write the snapshot only with a flag | Alters a merged default; external readers not excluded |
| C20 | Deferred, not closed: no design effort, #423 stays open |
| C22 merge the Orca finders | Different policies; the sweep deliberately never uses a bare `orca` |
| C23a 30-day watcher deadline | Invented; route B depends on the watcher |
| C24 retire `/sc:task` | Outside this program; the owner's record authorizes no removal |

## 6. Conditions carried from the shared assumptions
- Evidence is from this host only; it justifies freezing or deferring, not deleting a control (A-002).
- Re-count before any code cut; the 2,500-line and 4,000-line figures stay UNVERIFIED (A-003).
- A default applies only where it is "do nothing" or "report only", always labelled as a default and never as an owner answer (A-004).
- Deletion is cheap to do and not cheap to undo: it needs a new security review and the docs and tests that cite it (A-005).
- An agent edits status and notes only. It writes no owner-answer row, marks no card answered, and does not edit while the owner edits the same file (A-006).
