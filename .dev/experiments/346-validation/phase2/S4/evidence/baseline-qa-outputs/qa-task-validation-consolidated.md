# Consolidated task-file validation findings (A.10)

**Task file:** TASK-RESEARCH-bmad-first-use-20261107-075901.md
**Sources:** qa/qa-task-validation-b2-report.md (VERDICT FAIL: 4 IMPORTANT, 9 MINOR) and qa/qa-task-validation-structure-report.md (VERDICT FAIL: 5 IMPORTANT, 9 MINOR; transcribed by the orchestrator)
**Date:** 2026-11-07

## Items Reviewed
| Item | Verdict | Source lens |
|------|---------|-------------|
| Self-contained prompts | FAIL (B-1) | b2 |
| Phase structure and ordering | FAIL (S-1) | structure |
| Gate counts 3/3/7/2/2 | PASS | structure |
| No Ponytail items, no POST reflect gate | PASS | both |

## Blocking findings to fix (all IMPORTANT) 

| ID | Finding | Required fix |
|----|---------|--------------|
| F1 | 15 cycle-2 items (task-file lines about 250, 254, 258, 340, 344, 348, 401, 403, 405, 429, 431, 433, 457, 459, 461) say "EXACTLY the prompt embedded in Step X above" (B2 + structure #4). Builder note 3 defends it | Inline the full prompt text in each of the 15 items (the cycle-2 items repeat the cycle-1 prompt), and delete builder note 3 |
| F2 | Seven Gate 3 lens prompts say "at least N errors" with N defined only in prose outside the items (B2 #2, structure minor 7) | Replace N with the computed number or an in-item rule "N = report lines / 100, minimum 5, computed by the executor before spawning and written into the prompt" |
| F3 | Step 3.5 tells the fix agent to spawn gap researchers with the "full Staleness Protocol" but embeds none (B2 #3) | Embed the Documentation Staleness Protocol and Incremental File Writing Protocol text in that item |
| F4 | Step 7.2 stages `.dev/tasks` before Steps 7.3-7.5 create or edit files there (both reports) | Move the staging item after the last file-writing item (after 7.5); keep staging only, no commit |
| F5 | Step 2.1 "OBSERVED RUN" (bmad install in /tmp scratch with scratch HOME) contradicts "read and research only" and the no-one-off-probe rule; not tied to an Open Question (both reports) | Strike it. Replace with: read this worktree's existing `_bmad/`, `_bmad-output/` and `.claude/skills/bmad-*` as the observed output of a real `bmad install --modules bmm --tools claude-code`; mark what only a fresh install could show as UNVERIFIED. Update the Open Questions section and Key Constraints accordingly |
| F6 | TB-Add-7: Execution Context contains `Dockerfile.coder:133-144`; Source areas omits docs/, README.md, CHANGELOG.md, SECURITY.md, .github/workflows/ used by Steps 2.4-2.5 (structure #3) | Remove the file:line from the block; add the missing named areas |
| F7 | Gates 4 (fidelity) and 5 (anti-omission) fixed at 2 agents; SKILL.md requires 3-4 when input exceeds 1000 lines and test-startup-boot.sh alone is 3061 lines (structure #5) | Make each gate 3 agents (add one item per gate, with partitions covering all assigned files, and a verification item update) |

## Minor findings (notes, not sent to the fix agent)
Eight items lack a completion-gate sentence (lines about 176, 180, 476-496); fix agents lack ADVERSARIAL STANCE; two web prompts lack Staleness Protocol; relative paths in 34 of 44 prompts; unmeasurable sample sizes; Option B/C wording varies; git status guards assume untracked folder; verify-clause wording mixed; composite items 7.1 and 6.8; Step 6.8 edits report after gates; I22 mis-citation; missing Task-Specific Context Files subsection; Step 3.1 "three UNVERIFIED" vs line 129; Step 5.4 "if they exist"; Step 7.5 unconditional Done.

## A.10.25 research-alignment findings (cycle 1 of 1 allowed) 

Source: qa/qa-task-research-alignment-report.md (VERDICT FAIL: 3 IMPORTANT, 6 MINOR). The orchestrator confirmed F8 on disk: `_bmad/_config/manifest.yaml` says version 6.10.0, installDate 2026-04-18; `git ls-files` shows 17 files under `_bmad/`, 237 `.claude/skills/bmad-*` files and 577 under `_bmad-output/` all tracked; the history reads "sync bmad-* skills" and "upgrade BMad framework". F8 corrects the orchestrator's own wrong F5 instruction.

| ID | Finding | Required fix |
|----|---------|--------------|
| F8 | The task (about line 128 Step 2.1, Open Question 3, Builder Note 7 and the OBSERVED-FROM-EXISTING-INSTALL tag) says this worktree's `_bmad/`, `_bmad-output/`, `.claude/skills/bmad-*` are the output of a real `bmad install --modules bmm --tools claude-code`. They are a tracked 6.10.0 tree plus project documents, not 6.9.0 installer output | Reword everywhere: what a fresh 6.9.0 install creates is derived by READING the installer code (tools/installer/core/installer.js, install-paths.js, ide/_config-driven.js, manifest generator) and tagged CODE-VERIFIED when the code shows it. This worktree's tree is cited only as version-mismatched (6.10.0) corroboration, tagged accordingly. Anything only a real fresh 6.9.0 run could show is UNVERIFIED and goes to Open Questions. Rename the tag (for example OBSERVED-FROM-6.10.0-TRACKED-TREE) and fix Open Question 3, Key Constraints and Builder Note 7 |
| F9 | The edge cases (whole-HOME snapshot oracle test-57 lines 448-450, HOME persistence across boots, survival across reboot and `superclaude install`) appear only in research-agent prompts, never in the synth-03 comparison criteria, synth-04 plan or Step 6.8 checklist | Add them as explicit comparison rows (synth-03 prompt), as plan requirements (synth-04 prompt) and as Step 6.8 checklist lines |
| F10 | README edit constraints from the prior diagnosis dropped: markdownlint-clean edit, keep the "upstream GitHub CLI release v" anchor listed at `.github/upstream-monitor/releases.json:113`, README :241 reconcile (and :308 left alone) | Add them to agent 05's scope, the synth-04 plan prompt (document list) and the Step 6.8 checklist |
| F11 (minor, include) | Step 2.1 line about 192 says use `bmad install --help` while forbidding `bmad install` | Say plainly: `bmad install --help`, `--list-tools` and `--list-options` are allowed (read-only help); running an actual install is not |

## A.10.5 qualitative findings (round 1; verified F8-F10 PASS, F11 FAIL)

Sources: qa/qa-qualitative-operational-report.md (FAIL, 4 IMPORTANT; transcribed) and qa/qa-qualitative-sufficiency-report.md (FAIL, 5 IMPORTANT, 3 MINOR).

| ID | Finding | Required fix |
|----|---------|--------------|
| F12 | About 50 items make agents write .md; delegated agents may be unable to. Only fallback is "log blocker, mark complete", so a missing report can count as zero findings and gates can pass on absent reports (operational 1, sufficiency 1) | Add one shared FALLBACK rule and put a one-line pointer plus the rule text in every agent-spawning item: agent tries the .md path; if blocked it writes the same content to the same name with a .json extension; if that is blocked too it returns its findings inline (under 1500 chars) and the executor persists them verbatim to the .md path, labelled "transcribed by orchestrator". A report that is missing with no inline return is a FAILED agent: respawn once; if still missing, HALT and escalate; never treat it as zero findings and never as PASS. Relax "produced by the agent and not by you" to allow verbatim transcription |
| F13 | Task file is about 403 KB; Read caps at 256 KB; line 168's loop reads it per item | Tell executors to Grep `^- \[ \]` for the next unchecked item and Read with offset/limit around it; never full-read the file. Also reduce size if easy by making any long repeated text a single named block referenced by number only where the item still states its action and output (do NOT reintroduce "see above" for agent prompts) |
| F14 | F11 half-applied: line 192 contradictions; items 196, 204, 208 lack a `bmad install` ban; 196(a) asks what `bmad` does with no `_bmad/`; help flags run `npm view` | One consistent sentence in every research item that touches the CLI: only `bmad --version`, `bmad install --help`, `bmad install --list-tools`, `bmad install --list-options` are allowed, each run with `NPM_CONFIG_OFFLINE=true`; no other `bmad` subcommand and no actual install. Reword 196(a) as a code-reading question |
| F15 | A STOP-AND-RE-SCOPE report (no Section 8 plan) cannot pass Gate 3 actionability or Step 6.8 criteria 8, 21-23 | Add an explicit branch to Gate 3 actionability lens, Step 6.8 and synth-04: when Section 7 states STOP-AND-RE-SCOPE, Section 8 becomes "re-scope proposal" (what must change in which repo or decision) and criteria 8 and 21-23 apply to the re-scope proposal instead |
| F16 | The orchestrator regrades findings alone (lines about 229, 390, 452); the consolidated table records no reporter severity so downgrades are invisible | Require the consolidated findings table to carry the reporter's original severity and the orchestrator's final severity plus a one-line reason for every change; a downgrade of a reporter CRITICAL/IMPORTANT needs a cited reason and is listed in a "Severity changes" section; BLOCKING_COUNT is computed from final severity but the changes section must be non-empty-or-"none" |
| F17 | No gate re-checks web facts against their URLs; "skills created after session start" decides options B, C, D (sufficiency 3) | Add a web-source check to Gate 4 (or one extra fidelity item): every web finding that supports a ranked option or the recommendation is re-fetched or re-read from its URL by the fidelity agent; mismatch = blocking |
| F18 | Reproducibility lens samples 15 findings from Sections 2, 4, 6, 7 only; Section 8 pinned-assertion line numbers excluded (sufficiency 4) | Include Section 8 (every pinned test and doc line number named in the plan) in the reproducibility lens sample; treat a wrong line number on a pinned assertion as IMPORTANT |
| F19 | Zero-finding Self-Audit demand absent (sufficiency 5) | Add to every QA, analyst and lens prompt and to the lens output format: a "Self-Audit" section is mandatory, naming what was actively checked and why zero findings is believed; a bare zero-finding verdict is treated as suspect and re-run once |
| F20 | The feasibility correctness is judged only at Gate 2 (minor); pinned-test list hand-picked (line 204) while `.github/upstream-monitor/expected.txt` and `renovate-global.json5` also mention bmad (minor) | Add a feasibility-recheck line to Gate 3 domain-accuracy lens; add those two files to agent 05 scope for a documented-or-irrelevant decision |

Minor notes from this round are not sent to the fix agent: "build context not visible" hard-coded before agent 05 decides it (include if natural), Step 5.4 race, task-file ticks after `git add`, gap-researcher append-only conflict, Rule 14 vs standard table.

## A.10.5 verification round (review 2): FINAL fix cycle (fix cycle 2 of 2; after this a third review runs, then HALT and escalate if still failing)

Sources: qa/qa-fix-verification-a105.json (structure, FAIL, 1 IMPORTANT) and qa/qa-qualitative-verification-a105.md (content, FAIL, 3 IMPORTANT; transcribed).

| ID | Finding | Required fix |
|----|---------|--------------|
| F21 | F15 incomplete: the STOP-AND-RE-SCOPE branch is in synth-04 (304), Gate 3 lenses 371 and 379, Step 6.8 (475) but missing from Gate 2 (308, 312, 316), Gate 3 lenses at 373 and 383, and the consolidation items 320 and 391, so a re-scope report would HALT the gates | Add the one-sentence branch to each of those items: when Section 7 says STOP-AND-RE-SCOPE, judge Section 8 as a re-scope proposal and do not flag missing implementation steps |
| F22 | Research, synthesis, assembler and fix agents have no fallback beyond .md or .json; one refusal means HALT (content 1) | Extend the F12 rule for these agent types: if .md and .json writes are blocked, the agent returns the FULL file as its final message (no 1500-character cap for these types; unnamed agents are not truncated) and the executor writes it verbatim with a shell `cat` heredoc or the Write tool in chunks, labelled transcribed; fix agents return exact old/new edit pairs that the executor applies with Edit; a .json holds raw markdown (decode if wrapped). Missing everything = failed agent, respawn once, then HALT |
| F23 | The 1500-character inline cap with mandatory Self-Audit truncates QA findings (content 2); no outcome after the one re-run | Raise the inline cap for QA/analyst/lens agents to about 4000 characters: blocking findings first, severity counts, then Self-Audit; if still missing or truncated after the one re-run, HALT and escalate (never PASS, never zero findings) |
| F24 | Severity changes ledger written but never read (content 3) | Each decision file records the count of reporter CRITICAL/IMPORTANT findings downgraded by the orchestrator; Step 7.x (line about 488) lists every downgrade for the user in the final summary |
| F25 (minor, include) | `.addendum.json` for gap researchers has no merger; line 304 reads a task-file section with no offset; "Transcribed by orchestrator" first line displaces the report title; line 279 "web unavailable, mark complete" ambiguous vs the missing-file HALT; "never a PASS" missing at 230, 320, 391, 423, 453 and "or none" at 433, 463 | Name the owner (the Phase 3 fix agent merges addenda into the research file, otherwise Step 3.14 does); point 304 at lines 159-165 or the Key Constraints by grep; tell lenses to ignore a leading "Transcribed by orchestrator" line; make 279 say web-unavailable is allowed ONLY for web topics and only when the file exists with a stated reason; add the missing wording |

## Fix authorization
ONE fix agent (fix_authorization: true), task file only. Max 2 fix-verify cycles.
