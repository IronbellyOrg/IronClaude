# Research Completeness Verification

**Topic:** Existing solutions and design inputs for a GitHub issue watcher (issue #331, IronbellyOrg/IronClaude)
**Date:** 2026-11-07
**Status:** Complete
**Analysis type:** completeness-verification (report-only, fix_authorization: false)
**Depth tier:** Standard
**Files analyzed:** research-notes.md (scope + two ADDENDUM sections), 01-claim-flow-and-session-launch.md, 02-github-surface-and-cli-patterns.md, 03-governance-and-security-surface.md (web-01 and web-02 are out of scope for this gate)

Binding context applied from research-notes.md ADDENDUM 2: owner decided option A (workspace-side poller), claim-only, integer-only prompt; Coder#477 was filed assuming a push design.

Method: read research-notes.md and all three research files in full; then independently re-checked a sample of their load-bearing claims against the worktree and, for two repo-state facts, against GitHub (read-only `gh` calls with an explicit repo). Re-check evidence is cited per section. Nothing was modified outside this report.

---

## Checklist 1: Coverage audit

Every EXISTING_FILES row and every file named in the Files column of agents 01-03 (SUGGESTED_PHASES) was matched to a research file.

| Scope item | Covered by | Status |
|---|---|---|
| `src/superclaude/commands/issue.md` | 01 section 1 | COVERED |
| `sc-issue-protocol/SKILL.md` | 01 section 2 | COVERED |
| `refs/claim.md` | 01 section 3 (wave table), 02 section 2b | COVERED |
| `refs/labels.md` | 01 section 4, 02 section 2b | COVERED |
| `scripts/origin_repo.py` | 01 sections 5, 13; 02 section 3.2 | COVERED |
| `scripts/clickup_claim.py` (agent 01 Files list, not in EXISTING_FILES) | 01 section 6 | COVERED |
| `core/WORKER-CONTRACT.md` | 01 section 7, 03 section 5 | COVERED |
| `skills/ccsession-tag/README.md` | 01 section 12 (and `ccsession-orca` script itself), 03 section 2.2 | COVERED |
| `core/CLAUDE.md` ("Orca session launches") | 01 section 12 | COVERED |
| `docs/designs/sc-issue-launch-level-hook.md` | 03 section 1; 01 section 11 | COVERED |
| `hooks/scripts/launch-job-identity.sh` | 03 sections 1.2, 2 | COVERED |
| `.claude/settings.json` hook registrations (agent 03 Files) | 03 section 2.1 | COVERED |
| `.github/workflows/*` + README | 02 section 1 | COVERED |
| `.github/ISSUE_TEMPLATE/*.yml` | 02 section 2 | COVERED |
| `pr_submit/ci.py` (corrected claim) | 02 section 3.1 | COVERED |
| `cli/main.py` | 02 section 4.1 | COVERED |
| `tests/` layout, `tests/pr_submit/` | 02 sections 3.4, 5 | COVERED |
| `docs/designs/sc-issue-command.md` | 02 section 7 | COVERED |
| `Makefile` targets (agent 02 Files) | 02 section 6 | COVERED |

Assigned-question coverage (the list in the gate prompt), each answered with evidence:

| Assigned question | Answered in | Verdict |
|---|---|---|
| Claim waves | 01 section 3 (table with file:line for waves 0-6) | ANSWERED |
| `@me` identity / "meant for this login" | 01 section 9 (four candidates, race analysis); 03 section 4.3 | ANSWERED |
| Idempotency | 01 section 10; 03 section 7 (at-most-once row) | ANSWERED |
| Entry points for starting a session | 01 section 12 (five entry points plus `orca agent launch` argument contract) | ANSWERED (live behaviour flagged UNVERIFIED) |
| Never-as-worker | 01 section 7; 03 section 5 | ANSWERED |
| Workflow triggers | 02 section 1 | ANSWERED |
| `gh` wrapper | 02 section 3 (whole-`src` search, tests searched separately) | ANSWERED (claim contradicted) |
| CLI registration | 02 section 4 | ANSWERED |
| Tests / how `gh` is mocked | 02 sections 3.4, 5 | ANSWERED |
| Trust boundaries | 03 sections 3, 6, 7 | ANSWERED |
| Designed-versus-implemented hook | 03 section 1.2 (per-claim table) | ANSWERED |
| Owner rule: how `--claim <N>` validates its argument and whether a launch prompt can be that single line | 01 sections 5 and 13; 03 section 3.1 | ANSWERED: validation traced to `origin_repo.py:74,102-153` plus prose STOP rules `issue.md:45-51`; single-line prompt is possible on the files read, live slash-command execution UNVERIFIED and flagged |

Result: no coverage gap. No scope item lacks a research file.

### Independent re-checks supporting this section
- `.github/workflows/` contains exactly 4 entries (README.md, boundary-guard.yml, contract3-generator-constraint-lint.yml, test.yml); `grep -c 'schedule:'` returns 0 for all three YAML files (matches 02 section 1).
- `.github/ISSUE_TEMPLATE/` contains bug_report.yml, config.yml, feature_request.yml, other.yml (matches 02 section 2).

## Checklist 2: Evidence quality

Counts are approximate (claims are mostly cited inline, so "unsupported" counts statements that carry no file, line, command or function reference and are not explicitly marked as inference).

| Research file | Evidenced claims | Unsupported claims | Rating |
|---|---|---|---|
| 01-claim-flow-and-session-launch.md | very high; nearly every bullet carries file:line (`claim.md:41`, `origin_repo.py:74`, `WORKER-CONTRACT.md:23`, asar paths `specs/agent-launch.js:9-33`) | about 4, each marked "[inference]" or UNVERIFIED (tabs accumulate; ClickUp identity vs `gh` login; multi-assignee) | Strong |
| 02-github-surface-and-cli-patterns.md | very high; file:line, grep patterns and result counts for every section (workflow trigger lines, 21-file `subprocess` list, Makefile line anchors) | about 3, marked "suggestion" or UNVERIFIED (Project scope, `issueType` field, `events` endpoint) | Strong |
| 03-governance-and-security-surface.md | high; per-claim tables with file:line, plus live `gh api` observations dated 2026-11-07 | about 5, marked UNVERIFIED (Project permissions, who edits issue bodies, org-owner label rights, GitHub role rows taken from a search summary) | Strong |

### Independent re-verification of the load-bearing claims (all matched)
| Claim (source) | What I checked | Result |
|---|---|---|
| `_NUMBER = ^#?(?P<n>[1-9][0-9]*)$` at `origin_repo.py:74`; `check_claim` at 102; `read_origin` at 156; `main` at 177 (01 s5, 03 s3.1) | Grep of the file | MATCH |
| Exit codes 1/3/4 and `E-FOREIGN-REPO` / `E-NOT-AN-ISSUE` strings (01 s5) | Grep, docstring lines 28-50 | MATCH |
| `claim.md` Wave 0 lines 13-18, Wave 1 line 26 and 29, Wave 2 lines 39-43, Wave 3 line 47, Wave 4 line 56, Wave 5 line 80, Wave 6 line 90 (01 s3) | Read of `refs/claim.md` lines 10-91 | MATCH on every cited line |
| `WORKER-CONTRACT.md:11` (worker run definition), `:16` (brief guard), `:23` (never-as-worker list contains `/sc:issue`), `:39` (WC-8), `:40` (WC-9), `:61` (WC-13) (01 s7, 03 s5) | Read of lines 9-64 | MATCH on every cited line |
| `ci.py` imports only `re`, `.classifier`, `.models`; no `subprocess` (02 s3.1) | Grep `^import|^from|subprocess` over `ci.py` | MATCH (lines 10, 12, 14, 15; no subprocess hit) |
| 21 files under `src/superclaude` import `subprocess`, and the list names (02 s3.2) | Grep count | MATCH (21 files, names agree) |
| `mock_gh` appears in 3 test files, 6 occurrences (02 s3.1) | Grep count | MATCH |
| `conftest.py:3-4` calls `mock_gh` a "gh-wrapper seam ... recording argv to assert the `--repo` pin" but code at 38-59 patches `detection._fetch_payload` and records `pr_num` (02 s3.1 STALE DOC) | Read of `tests/pr_submit/conftest.py` 1-62 | MATCH, the stale-doc finding is real |
| `main.py` registrations, last at `:561` (`reflect_group`), `swarm` at 549, `cli_portify_group` with no `name=` (02 s4.1) | Grep `add_command` | MATCH (lines 521, 525, 529, 533, 537, 541, 545, 549, 553, 557, 561) |
| `EXPECTED_TOP_LEVEL_COMMANDS` is described as a "frozen snapshot" but omits `swarm` and `reflect` (02 s4.3) | Grep of test file (comment at line 29, set at 31; no `"swarm"` or `"reflect"` hit in the test file) | MATCH |
| `hooks.json` registers `launch-job-identity.sh` and has no `launch-level-guard` entry (03 s1.2) | Grep `hooks.json` (one hit, line 101) | MATCH |
| `launch-level-guard.sh` stated in present tense at design line 23 and "proposed" at line 40; file absent (03 s1.2) | Grep of design doc, plus Glob `**/launch-level-guard*` returned no files | MATCH |
| `launch-job-identity.sh` not installed in `/home/coder/.claude/hooks/` (03 s2.1) | `ls` of that directory (14 files, none of that name) | MATCH |
| Repository is PUBLIC although project `CLAUDE.md` calls it a private fork (03 stale-doc finding) | `gh repo view IronbellyOrg/IronClaude --json visibility,isPrivate,isFork` returned `{"isFork":true,"isPrivate":false,"visibility":"PUBLIC"}` | MATCH, the stale-doc finding is real and important |
| Live label list is the 9 GitHub defaults (02 s2, 03 s4.1) | `gh label list --repo IronbellyOrg/IronClaude` | MATCH (bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix) |
| No Project code in the claim skill (01 s3, 03 s4.1) | Grep `gh project|projectV2|graphql` over `sc-issue-protocol/`: 0 matches | MATCH |
| `issue-worker-t3` tools include Bash (01 s13, 03 s3.2) | Grep `tools:` in `agents/issue-worker-t3.md` line 5: `Read, Grep, Glob, Write, Bash` | MATCH |

Not independently re-verified by me (taken on the agents' evidence, all tagged or sourced by them): the `/opt/Orca/.../out/cli/*` line citations and `orca agent launch --help` output (01 s12), `ccsession-orca` line numbers, `ccsession:136-141` default flags, `gh auth status` scopes and `gh project list` scope failure (03 s4.2), branch-protection 404 and collaborator role counts (03 s2.3, s4.2), the GitHub roles table fetched from docs.github.com. These are marked [OBSERVED] or UNVERIFIED in the files; I found nothing that contradicts them.

Result: evidence quality Strong on all three files. No fabricated claim found in the sample (about 25 claims re-checked, 0 mismatches).

## Checklist 3: Documentation staleness

Every doc-sourced claim I found carries a tag, and each file has a "Stale Documentation Found" section. The research notes' own mistaken claim (`ci.py` as a `gh` wrapper) was caught and corrected by 02.

| Claim | Source doc | Tag | Status |
|---|---|---|---|
| `/sc:issue --claim` kicks off the full orchestration path (issue text) | #331 issue text | [CODE-CONTRADICTED] by `issue.md:15,79,83`, `claim.md:80` (01 s1, Gaps) | OK |
| `ci.py` is a mockable `gh` subprocess wrapper | earlier research note | [CODE-CONTRADICTED] (02 s3.1; re-verified above) | OK |
| `mock_gh` patches a "gh-wrapper seam" and asserts the `--repo` pin | `tests/pr_submit/conftest.py:3-4` | [STALE DOC] (02 s3.1; re-verified above) | OK |
| `EXPECTED_TOP_LEVEL_COMMANDS` is a frozen snapshot forcing updates | `tests/cli/test_cli_registration.py:28-30` (actual comment line 29) | [CODE-CONTRADICTED] (02 s4.3; re-verified above) | OK |
| `launch-level-guard.sh` enforces levels (present tense) | `docs/designs/sc-issue-launch-level-hook.md:23` | [CODE-CONTRADICTED] / present-tense overstatement (03 s1.2, Stale section; re-verified above) | OK |
| `--claim --pipeline <level>` exists | same design, line 23 | [CODE-CONTRADICTED], doc admits at line 34 (01 s11, 03 s1.2) | OK |
| `hooks.json` registers the identity adapter, installer ships it | `hooks.json:96-105`, `install_hooks.py:87` | [CODE-CONTRADICTED on this host] (03 s2.1; re-verified: hook file absent in `~/.claude/hooks/`) | OK |
| `origin` is "the user's private fork" | project `CLAUDE.md` PR-target section | [STALE DOC] (03 Stale section; re-verified: PUBLIC) | OK |
| `hooks/README.md:3-19` says directory holds only config | `src/superclaude/hooks/README.md` | [STALE DOC] (03) | OK |
| Orca pull-only message semantics | `.dev/orca-command-refactor/inventory/orca-capabilities.md:66` | Cross-checked against Orca guide text, tagged CODE-VERIFIED with a stale-risk note (01 s12, Stale section) | OK |
| Design doc (`sc-issue-command.md`) claims about repo files | `docs/designs/sc-issue-command.md` | Mixed CODE-VERIFIED / UNVERIFIED (picker-ID table not opened) (02 s7) | OK |
| `.dev/issues/331/analysis/analyze-sc-issue-protocol.md` F3, F4, F5, F7 | analysis file | Each tagged (01 s8) | OK |

No doc-sourced claim without a tag was found. No `[CODE-CONTRADICTED]` item is presented as current fact.

Minor notes (non-blocking):
- 02 s2b uses `[CODE-CONTRADICTED]` for a code-versus-live-GitHub-state gap (the fork lacks the `type:*` and `complexity:*` labels that `labels.md` assumes). The finding is correct; the tag is stretched beyond its documentation-versus-code meaning, and 02 says so itself.
- 03 s4.2 lists the "Create, edit, delete labels: Write" role row as taken from a search summary and "not separately fetched" but does not give it a formal UNVERIFIED tag. Low impact.

## Checklist 4: Completeness

| Research file | Status line | Summary | Gaps and Questions | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 01-claim-flow-and-session-launch.md | `Status: Complete` (line 4) | Y (line 285) | Y (line 255, 8 numbered items plus tagged-claims list) | Y, one block per numbered section (13 blocks) | Complete |
| 02-github-surface-and-cli-patterns.md | `Status: Complete` (line 4) | Y (line 209) | Y (line 190, 10 numbered items) | Y, one block per section (1, 2, 2b, 3, 4, 5, 6, 7) | Complete |
| 03-governance-and-security-surface.md | `Status: Complete` (line 4) | Y (line 229) | Y (line 203, 14 numbered items) | Y, one block per section (1-7) | Complete |
| research-notes.md | `Status: Complete` (line 6) | n/a (scope file) | n/a | n/a | Complete |

Minor note (non-blocking): the three files have no single end-of-file "Key Takeaways" heading; the takeaways are given per section and the Summary closes each file. The per-section form satisfies the intent of the check.

## Checklist 5: Cross-reference check

Cross-cutting concerns covered by more than one agent, and whether they line up:

| Concern | Files | Cross-referenced? |
|---|---|---|
| Never-as-worker list, worker run versus ordinary session | 01 s7, 03 s5 | Consistent. Both conclude a poller-launched `orca agent launch` session is an ordinary session; both rely on `WORKER-CONTRACT.md:11,23`; 03 adds WC-8, WC-9, WC-13. 01 flags the reading as UNVERIFIED as owner intent. Acceptable. |
| Integer-only prompt and what it does not protect | 01 s13, 03 s3 | Consistent and complementary. 01: the claim reads issue text via `gh issue view` (claim.md:26) and the accuracy-check worker (claim.md:56). 03: confirms with `issue-worker-t3.md:5` tools and adds the PUBLIC-repo fact. |
| `gh` `--repo` convention versus the fork rule | 02 s3.3, 01 s2 | Consistent. 02 adds the fallback hazard in pr-submit scripts (Convention B). |
| Label model (no trigger/approval label; live list is the 9 defaults) | 01 s4, 02 s2, 03 s4.1 | Consistent; the live list is identical in 02 and 03 (and in my re-check). |
| Orca `--worktree` selector and Orca link-flag hazard | 01 s12 (recommends `path:<abs>`), 03 s5 and Gap 12 (recommends `path:` or `name:`) | Consistent recommendation; 01 does not mention the link-flag hazard. Minor. |
| Project/Backlog filter and token scope | 01 s9 and Gap 5, 02 Gaps 2 and 9, 03 s4.2 and Gap 8 | Not reconciled between files. 01 and 02 say the scope requirement is UNVERIFIED; 03 observed that `gh project list` fails on this workspace for lack of `read:project` and that the token scopes are `gist, read:org, repo, workflow`. Not a contradiction, but the synthesis must carry 03's observation into the 01/02 gap items. |
| "Who approved" signal (label events) | 02 s2 (UNVERIFIED, "not exercised"), 03 s4.2 (OBSERVED: events on #331 include `labeled`, `assigned`, `project_v2_item_status_changed` with actor) | Same pattern: 03 closes the item 02 left open. Synthesis must use 03's observation. |
| At-most-once design | 01 s9-s10, 02 Gap 10, 03 s7 and Gap 11 | Consistent that the claim gives no mutual exclusion. 03 proposes the rule "assigned to my login and no claim marker comment of mine"; 01 s10 shows the claim comment is a late record (Wave 6) and a claim failing after Wave 3 leaves the issue selected on every cycle. The two views are complementary and not reconciled in one place; synthesis should combine them (own durable record plus retry cap). |

Result: no blocking cross-reference defect. Two notes for the synthesis agent (the Project-scope item and the label-event item).

## Checklist 6: Contradiction detection

Compared every statement made about the same component by more than one agent.

| Topic | Versions | Finding |
|---|---|---|
| Permission posture of an Orca-launched session | 01 s11: local Orca `agentDefaultArgs.claude` is `--dangerously-skip-permissions`, `agentCmdOverrides` is `{}`. 03 s2.2: ccsession default is `--dangerously-skip-permissions --allowedTools=Grep` unless `CCSESSION_PERMISSIONS=default`. | Not a contradiction. Both say bypass is the default; they describe two different mechanisms. Both mark the Coder workspace value UNVERIFIED. |
| Whether `--prompt` reaches Claude as submitted text | 01 s12: request.js turns `--prompt` into `{text, delivery: 'submit'}` (submitted); delivery mechanism argv versus paste UNVERIFIED. 03 s3.1 and Gap 4: argv positional versus `--prefill` UNVERIFIED. | Consistent. 01 has the stronger evidence (`delivery: 'submit'`); 03's open question is partly narrowed by it. Synthesis should state 01's evidence and keep the live test. |
| `ci.py` role | research notes (initial): "gh wrapper"; 02: pure classifier | Resolved by 02; research-notes.md was already corrected in-place (EXISTING_FILES row, PATTERNS section). |
| `docs/designs/sc-issue-launch-level-hook.md` length | 01 s11 table cites design lines up to 565; 03 header says 566 lines; `wc -l` gives 565 | Trivial (a trailing-line counting difference). Note only. |
| Other line-count headings | 01 headings give issue.md 101, SKILL.md 156, claim.md 91, labels.md 46, origin_repo.py 196, clickup_claim.py 271; `wc -l` gives 100, 155, 90, 45, 195, 270. 02 gives `sc-issue-command.md` 477 (matches `wc -l`) while research-notes.md says ~600. | Every heading is off by one in the same direction (consistent with a Read-tool trailing blank line), and no cited line number I checked was wrong. Note only. The research-notes "~600" is an approximate scope-stage figure that 02 corrected. |
| `/sc:issue` claim stops after `next-steps.md` versus the issue text's full-pipeline expectation | 01 (CODE-CONTRADICTED) and 03 (mitigating fact) agree | No conflict. |
| Dispatch marker: assignee as marker | 01 s9: assignment persists, cannot be the marker; 03 s7: "assigned to my login and no claim marker comment" | Not a contradiction; see cross-reference table. |

No substantive contradiction between the files.

## Checklist 7: Compiled gaps (deduplicated across 01, 02, 03)

Severity scale for the gate: Critical = blocks synthesis; Important = affects report quality or the plan and must be carried as an explicit open item; Minor = note. None of the items below is a defect in the research (each is honestly tagged UNVERIFIED or OPEN DECISION and several can only be settled by a live run that this research was forbidden to do). They are gaps the report must carry forward, not reasons to block synthesis.

### Critical gaps (block synthesis)
- None.

### Important gaps (carry into the report as open items or live-plan prerequisites)
1. **Does a leading `/sc:issue --claim <N>` given as `orca agent launch --prompt` run as a slash command and get submitted?** (01 Gaps 1-2, 03 Gap 4). Not shown by any file; needs one owner-run live test in the live-plan phase. The whole claim-only design depends on it. 01 s12 gives partial evidence (`delivery: 'submit'`; Claude `promptInjectionMode: 'argv'`).
2. **Launched-session permission posture on the Coder workspace** (01 Gap 4, 03 Gap 5 and s2.3): stalled in default mode, unrestricted under ccsession's bypass default; no allow-list exists in the repo. The security section of the report must state this.
3. **Claim reads untrusted issue title, body and comments live, on a PUBLIC repository** (03 s3.2-3.3, Gap 6; 01 s13). Integer-only protects the prompt, not the session. Open decision: accepted-risk statement, `author_association` filter, conversation lock, or a claim-side change. Re-verified: the repo is PUBLIC and the project `CLAUDE.md` text calling it private is stale.
4. **Approver authority and approver allow-list** (03 Gaps 9-10, 02 Gap 3): only GitHub roles gate who can label (Triage or higher; 3 accounts counted); the events API supplies the actor (observed on #331). The rule and where the allow-list lives are undecided.
5. **Dispatch record and retry cap** (01 s9-s10, 02 Gap 10, 03 Gap 11): the claim has no mutual exclusion; same-login multi-workspace race; a claim failing after Wave 3 leaves the issue assigned and selectable every cycle; the claim does not move Project status. The poller needs its own durable record written before launch, plus `--retry-launch` handling for a lost reply (01 s12).
6. **Project/Backlog filter feasibility** (01 Gap 5, 02 Gaps 2 and 9, 03 Gap 8): this workspace's token lacks `read:project` (observed by 03); label-only selection avoids the problem. The label names and the Project mapping are undefined (02 Gap 8).
7. **Trigger and approval labels do not exist** (02 s2, 03 s4.1; re-verified live): the deliverable must include `gh label create` instructions in the `labels.md:22-42` style (already part of the owner-decided deliverable).
8. **Workspace prerequisites unknown on Coder** (01 Gap 4): Orca runtime reachable by the poller, `ccsession-orca` configured, `claude-gw-tier*` picker IDs served (else `E-TIER-UNAVAILABLE` at Wave 1 with no GitHub write, so the poller would re-dispatch), `gh` login, `uv`, installed skills and agents, ClickUp variables.
9. **Installed hook set can be stale on a host** (03 Gap 3): the identity adapter is registered in `hooks.json` but absent from this workspace. Relevant to any claim that "hooks constrain the session".

### Minor gaps (notes, do not block synthesis)
- Whether tests pin the claim-stops-after-`next-steps.md` text (01 Gap 6; `tests/skills/test_issue_protocol.py` unread).
- Whether `<D>` already existing is tolerated on re-run (01 Gap 7; `claim.md:18` says only "Create `<D>`").
- Whether `--claim` works under `claude --print` (01 Gap 8; only relevant for a headless route).
- JSON key nesting of `orca agent launch --json` and the real error body (01 Gap 2).
- Native `issueType` field name for `gh issue list --json`; `labeled` events as a trustworthy signal; whether a post-approval body edit is detectable (02 Gaps 2-3, 03 Gap 7).
- Whether `--worktree issue:<n>` triggers Orca's GitHub linking (03 Gap 12; use `path:`).
- Unread items: bodies of `freshness-pre-edit.sh`, `sc-recommend-phase0.sh`, `issue-worker-t1/t2.md`, `tests/cli/test_install_hooks.py` (03 Gap 13).
- The fork lacks the `type:*` and `complexity:*` labels that `/sc:issue --create` expects (02 Gap 7); an owner decision, not research.
- Coder-side tie between workspace and GitHub account (03 Gap 14): out of scope under option A.

## Checklist 8: Depth assessment

**Expected depth (Standard):** file-level understanding with key function documentation.
**Actual depth achieved:** above Standard in places. Includes a wave-by-wave trace with file:line (01 s3), argument-validation trace with accepted and rejected forms (01 s5), a launch-argument contract table and mock specification (01 s12), a four-candidate routing analysis with a derived race scenario (01 s9), a per-claim designed-versus-implemented table for the hook (03 s1.2), a capability inventory of what an injected session can do (03 s6), a Makefile and CI gate table (02 s6), and full test-layout and `gh`-mocking evidence (02 s3.4, s5). Data-flow tracing for the Deep tier is not required here and not needed.
**Missing depth elements:** none required for Standard. The only shortfall is that live behaviours could not be run (correctly out of scope).

## Findings

Grading: blocking = Critical or Important defect in the research (false claim, missing required deliverable, unanswered assigned question). Minor = wording, format, nit.

### Blocking findings
None. No false claim was found in about 25 re-checked claims, no scope item is uncovered, and every assigned question has an evidenced answer or an honestly flagged UNVERIFIED with a stated reason.

### Minor findings (notes only; never fail the gate)
| # | Note | Source | Suggested action for the synthesis stage |
|---|---|---|---|
| M1 | Off-by-one line-count headings in 01 (101/156/91/46/196/271 versus `wc -l` 100/155/90/45/195/270); 01 and 03 disagree by one on the launch-level design (565 versus 566) | 01 section headings, 03 s1 heading | Do not quote these totals in the report; cite line anchors, which were all correct in the sample |
| M2 | 01 and 02 leave the `read:project` scope and the "who approved" event signal UNVERIFIED while 03 observed both on this workspace | 01 Gap 5, 02 Gaps 2-3, 03 s4.2 | Synthesis should use 03's observations and mark them as observed on one workspace only |
| M3 | 02 uses `[CODE-CONTRADICTED]` for a code-versus-live-GitHub-state gap | 02 s2b | Describe as "repo state gap" in the report |
| M4 | 03 GitHub-role rows partly rest on a search summary without a formal UNVERIFIED tag; the web provenance (Tavily unavailable, WebSearch/WebFetch used) is recorded in the file header | 03 s4.2 and header | Mark the "create labels: Write" row UNVERIFIED if the report cites it |
| M5 | `tests/cli/test_cli_registration.py` stale comment is at line 29 (02 cites 28-30) | 02 s4.3 | None |
| M6 | 01 does not mention the Orca link-flag hazard that 03 raises | 01 s12 versus 03 s5 | Report should state the hazard once, citing 03 |
| M7 | research-notes.md EXISTING_FILES still gives approximate line counts (`~600` for `sc-issue-command.md`, actual 477) | research-notes.md line 33 | None; the research files hold the corrected figures |

## Recommendations
- Proceed to web research and synthesis; no remediation of the research files is required.
- Synthesis must carry forward the nine Important gaps above as explicit open items or live-plan prerequisites, in particular gaps 1 (live slash-command test), 3 (public repo, claim reads untrusted text) and 5 (dispatch record).
- Synthesis must preserve the three corrected claims (`ci.py` not a wrapper; `mock_gh` not an argv recorder; frozen-set comment false) and the stale "private fork" statement, and must not repeat the original notes' wrong claims.
- Treat observations made on this workspace (token scopes, missing identity hook, `agentCmdOverrides: {}`) as single-host observations, not Coder-wide facts.

## Summary

- Files analyzed: 4 (research-notes.md plus research files 01, 02, 03).
- Checklist results: 1 Coverage PASS; 2 Evidence quality PASS (Strong x3); 3 Staleness PASS; 4 Completeness PASS; 5 Cross-reference PASS (two notes); 6 Contradictions PASS (none substantive); 7 Gap compilation done (0 Critical, 9 Important carried forward, 9 Minor); 8 Depth PASS (meets or exceeds Standard).
- Independent re-verification: about 25 load-bearing claims re-checked against the worktree and two read-only `gh` calls; 0 mismatches. Three of the research files' own corrections (ci.py, mock_gh, frozen-set comment) and the "private fork is actually PUBLIC" finding were confirmed real.
- Blocking findings: 0. Minor findings: 7 (M1-M7), notes only.
- Limits of this gate: the Orca `/opt/Orca` code citations, `orca agent launch --help` output, `ccsession` flag lines, token-scope output, branch-protection and collaborator-count observations, and the GitHub docs roles table were not independently re-run; they are tagged OBSERVED or UNVERIFIED by the authors and nothing found contradicts them.

VERDICT: PASS

