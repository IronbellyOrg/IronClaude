# QA Report - Research-Depth Qualitative Review (research-gate-qualitative)

**Topic:** GitHub issue watcher research (issue #331, IronbellyOrg/IronClaude)
**Date:** 2026-11-07
**Phase:** research-gate-qualitative (lens: research-depth)
**Fix cycle:** N/A
**Status:** Complete
**Fix authorization:** false (report only)

---

## Scope read

Read in full: `research-notes.md` (including ADDENDUM and ADDENDUM 2, the owner decision for option A, claim-only, integer-only), `01-claim-flow-and-session-launch.md`, `02-github-surface-and-cli-patterns.md`, `03-governance-and-security-surface.md`. The `web-*.md` files do not exist yet (and are outside the prompt's scope); options B and C are therefore not judged here.

## Findings (appended incrementally)

### F1 - IMPORTANT (contradiction between files) - the poller's routing/dedupe rule is stated two incompatible ways
- `02-github-surface-and-cli-patterns.md` section 2b (line 57): "skip issues that already have an assignee"; line 63 repeats "pre-filter on assignees"; Gap 10 (line 200) says "assignee pre-filter".
- `01-claim-flow-and-session-launch.md` section 9 candidate 1 (lines 150, 162): select issues already assigned to this workspace's own login (`gh issue list --assignee "@me"`), called the "best fit". `03` section 4.3 and section 7 also treat "assignee equals my login" as the routing input.
- These are mutually exclusive filters. Skipping every assigned issue would never select an issue an approver assigned to the person; selecting only assigned-to-me is the opposite. Nothing in the three files reconciles them, and the owner decision (Q1/Q2/Q3) does not settle it. The synthesis has to pick one, and a reader of file 02 alone would build the wrong filter.
- Remediation: add one reconciling paragraph to file 02 sections 2b and 3.3 (or a cross-file resolution note in the synthesis brief) stating the single rule (for example: trigger label AND assigned to my login; unassigned issues are never auto-claimed) and why "skip assigned" applies only to other logins.
- Verified by: Read of 01 lines 148-164, 02 lines 57 and 63, 03 lines 132-142.

### F2 - IMPORTANT (omission / unacknowledged gap) - where the 5-minute poller runs and keeps its dispatch record is asserted, not researched, and is not listed as a gap
- `01` line 130 and `03` line 149 say the poller "must run as a plain process on the workspace (cron, systemd or a user loop)". No file checks that a Coder workspace has cron or systemd, that the process survives workspace autostop, or where durable state can live (`01` section 10 and Key Takeaways: the record "must survive a workspace restart"). A Grep for cron/systemd/schedule/state file/XDG/autostop over `01`-`03` found only those two assertions (plus the unrelated GitHub-Actions `schedule` lines in `02`).
- The "Gaps and Questions" lists (`01` items 1-8, `02` items 1-10, `03` items 1-14) cover the Orca runtime, ccsession, picker IDs, permission mode, `gh` auth and ClickUp in the workspace, but not the scheduler or the state location. Under the owner decision this is the whole of the "Coder-side listener", so the question the report must answer rests on an unverified premise.
- Remediation: add a gap entry that scheduler availability, autostop behaviour and a persistent state path in a Coder workspace are UNVERIFIED here and are to be covered by `web-02` (or an owner-run check in the live plan); tag the "cron, systemd, a shell loop" sentences `[UNVERIFIED]`.
- Verified by: Grep over `research/0*.md` (case-insensitive) for cron|systemd|schedule|loop|state file|XDG|autostop.

### Minor notes (never fail the gate)
- M1 (cross-file staleness): `03` Gap 4 and section 3.1 keep "does `orca agent launch --prompt` submit, or arrive as a `--prefill` waiting for Enter" fully open, while `01` section 12 already shows the CLI builds `{text, delivery: 'submit'}` (re-checked: `/opt/Orca/resources/app.asar.unpacked/out/cli/agent-launch-request.js:63-64`). What stays open is argv-versus-paste inside the host runtime. Align the wording.
- M2: the launch target is only a `--worktree` selector. Neither file weighs a dedicated watcher worktree against the person's active worktree, even though the claim writes `.dev/issues/<N>/` and runs `git fetch origin` there. Nothing is said about a per-cycle cap on launches when several issues are approved at once (N concurrent tier-1 sessions in one checkout).
- M3: `01` header says `issue.md` is 101 lines; Read shows 100. `03` section 2.1 says 14 scripts in `/home/coder/.claude/hooks/`; Glob `**/*.sh` found 13 (the absence of `launch-job-identity.sh` is confirmed).
- M4: `research-notes.md` body (SOLUTION_RESEARCH, AMBIGUITIES_FOR_USER) still reads as "A, B, C open" above the two addenda. The addenda state precedence, so this is cosmetic.
- M5: Gap 6 in `01` (do tests pin the claim-stops text) is cheaply closable: Grep of `tests/skills/test_issue_protocol.py` shows its two hits are about next-step chain flags, not the stop rule; `tests/commands/test_issue_command.py` has none. Record that.

## Verification performed (independent of the research files)
| Claim checked | Result | Evidence |
|---|---|---|
| `origin_repo.py` `_NUMBER` at L74, `check_claim` L102, `read_origin` L156, `main` L177, exit table L47-50 | confirmed | Grep of the file |
| `claim.md` waves, line numbers 13-15, 26-30, 37-43, 47, 78-80, 84-90 | confirmed | Read of `refs/claim.md` (91 lines) |
| `issue.md` L8, L15, L24, L37, L43, L45-51, L68, L71, L79-85, L89-93; no "pipeline" | confirmed | Read of `commands/issue.md`; Grep count 0 for `pipeline` |
| `SKILL.md` L4, L58-62, L70, L74, L88, L130 | confirmed | Grep of the file |
| `WORKER-CONTRACT.md` L11, L16, L23, L39, L40, L61, L93, L112 | confirmed | Read of the file |
| `main.py` 11 `add_command` registrations, last at L561, `cli_portify_group` without `name=` | confirmed | Grep |
| `tests/cli/test_cli_registration.py` frozen-snapshot comment; `swarm` and `reflect` absent from the set | confirmed (no match for either name in the set) | Grep |
| `ci.py` imports only `re`, `.classifier`, `.models` | confirmed | Grep L10-15 |
| `.github/workflows` has exactly 4 files | confirmed | Glob |
| `hooks.json` registers `launch-job-identity.sh` (L101); not installed under `~/.claude/hooks` | confirmed | Grep, Glob |
| Repo is PUBLIC and a fork; `master` has no protection; 9 default labels only | confirmed | `gh repo view`, `gh api .../branches/master/protection` (404), `gh label list` |
| Collaborators: 1 admin, 2 maintain, 8 read | confirmed | `gh api repos/IronbellyOrg/IronClaude/collaborators` |
| `ccsession` adds `--dangerously-skip-permissions --allowedTools=Grep` unless `CCSESSION_PERMISSIONS=default` | confirmed (lines 119-139) | Grep |
| `ccsession-orca` `-*` skipped (L110), positional sets `task_carried=1` (L119) | confirmed | Grep |
| `orca agent launch` needs an existing worktree; unknown agent refused; `delivery: 'submit'`; `incompatible_runtime` refusals | confirmed | Grep of Orca CLI `agent-launch-request.js`, `handlers/agent-launch.js` |

I found no factual error in the code citations I re-checked (about 45 individual claims across the files). The two blocking findings are an inter-file contradiction and an unacknowledged gap, not wrong citations.

## Seven evaluation criteria
1. Actionable findings: yes. Each file ends with Key Takeaways and numbered gaps; integration points are named (main.py after L561, `origin_repo.py` pattern, PATH-stub test pattern, `--worktree path:<abs>`).
2. Depth: strong. Data flow traced wave by wave, error paths and refusals listed, idempotency and the double-claim race derived from code and labelled as derived, identity behaviour (`@me`) traced.
3. Concrete integration points: yes, with file and line.
4. Gaps honest and specific: mostly (see F2 for the one important unlisted gap).
5. Doc-sourced architecture tagged: yes; `launch-level-guard.sh` and the `--pipeline` interface are tagged CODE-CONTRADICTED/UNVERIFIED, the stale `ci.py` claim is caught.
6. Security question inputs: present (approval authority, `author_association`, label-event actor, untrusted text reaching the claim's workers, readable `gh` token, public repo, unprotected master).
7. Proportionate conclusions: yes; UNVERIFIED tags used where nothing was run.

## Self-Audit
**(a) Reliance list:** no Inherited Structural Verdict was supplied in the spawn prompt; standalone behaviour applied, nothing relied on.
**(b) Independent semantic checks:** the line-level verification table above (Read, Grep, Glob and read-only `gh` calls); the cross-file comparison that produced F1; the Grep that produced F2.

Confidence: Verified: 7/7 criteria | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 8 | Grep: 15 | Glob: 3 | Bash: 2 (read-only `gh` and `ls`)
Web research: none performed (no Tavily or fallback call).

## Summary
Blocking findings: 2 (F1, F2), both IMPORTANT. Minor notes: 5. Critical: 0.
Remediation is small: one reconciling paragraph for F1 and one added gap entry for F2.

VERDICT: FAIL

**Status:** Complete

