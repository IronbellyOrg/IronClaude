# S4 REPLAY runbook: BMAD first-use research report (incident I4), gate loops of a `tech-research` run

Status: complete. Written 2026-11-08 by the S4 recreation analyst. The analysis behind it is `ANALYSIS.md`; the baseline numbers are `baseline-metrics.json`. This runbook was not executed (no replay was started).

## 0. Read this first

1. **Does PR 427's spec-panel change reach this scenario? No.** The reviewers are `rf-analyst`, `rf-qa` and `rf-qa-qualitative` agents run from the `tech-research` and `task` skills (Claude Code `Agent` tool). `/sc:spec-panel` appears in neither the main log nor any of the 71 agent logs. PR 427 (`95f2c6e4`) edits only the spec-panel command text (and its plugin mirror), `HOW-WE-WORK.md` (and its mirror), two release guides, one design doc and one test. None is read by this pipeline, and the work repo is Coder, not IronClaude. Expect a delta of about zero by construction (DECISIONS.md D4, known limit). Use S4 as a control scenario (noise floor of a 3-review-cap loop), not as evidence for or against 427. Details: `ANALYSIS.md` section 5.
2. **What a replay is.** The original ran 5 gates over 8.5 hours with 71 agents; its first half (research and synthesis, with web search) cannot be repeated to the same text. So the replay unit is one gate, entered from the exact document state the original gate started from (`tools/make_gate_entry.sh 1|2|3`). Primary: **Gate 3** (7 lenses on one report, byte-exact stored end point). Secondary: Gate 2, Gate 1. Gates 4 and 5 have recovered inputs (`inputs/gate4-start/`, `inputs/gate5-start/`) but no validated runbook, and Gate 5's baseline round 1 is contaminated by brief errors (`ANALYSIS.md` section 8, finding 6).
3. **Do not touch the originals.** The original Coder worktree `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global` and `~/.claude` are read-only evidence. The script refuses to build into the original worktree.

## 1. Package map

| Path | What |
|---|---|
| `ANALYSIS.md` | round-by-round analysis with evidence pointers |
| `baseline-metrics.json` | M1 to M5 per gate and round, original run, each number with its source |
| `inputs/` | every input needed to rerun, `MANIFEST.sha256`, `SOURCES.md` (origin of each file) |
| `briefs/` | every prompt of the original run, verbatim, one file per agent call; `INDEX.md` |
| `evidence/` | `baseline-qa-outputs/` (the 80 review files of the original: results, do NOT show to a replay session), `m4-sizes.tsv`, `agent-costs.tsv` |
| `tools/` | `make_gate_entry.sh` (builds a gate entry), `reconstruct.py` and `reverse_notes.py` (document replay), `extract_briefs.py`, `census.py`, `agent_costs.py`, `build_metrics.py`, `check_pointers.sh` |

Check the package: `cd inputs && sha256sum -c MANIFEST.sha256` (must print only OK).

## 2. Versions and commits

| Item | Original run | Re-run |
|---|---|---|
| Work repo | `IronbellyOrg/Coder`, branch `ironbelly/bmad-ponytail-global`, HEAD `f1ac0c93ad5a64b03f0ed49866d3adfe140c28b1` (`BM` L23 and L868; the run committed nothing; `86c827af` came after, 2026-11-08T01:26Z) | same commit, in a fresh copy |
| Framework (skills, agents) | `~/.claude/skills/tech-research`, `.../task`, `~/.claude/agents/rf-*.md`, all dated 2026-11-05 13:13, i.e. IronClaude before PR 427 (427 = `95f2c6e4`, committed 2026-11-07T08:27:45-05:00, three minutes after the run started; the last master commit without it is `ec1babd9` per DECISIONS.md D3) | for the 427 arm: IronClaude master at or after `95f2c6e4`, then `make sync-dev` in the IronClaude checkout, as DECISIONS.md D4 says. Note: this scenario reads the skills and agents from the installed `~/.claude`, not from a project `.claude/`, so `make sync-dev` alone changes nothing for S4; installing master into `~/.claude` would modify the shared home and is the coordinator's decision (UNVERIFIED whether a throwaway `HOME` works). Since 427 touches no file this pipeline reads, the replay is valid either way |
| Claude Code | `2.1.319` (`version` field in `BM`) | whatever the coordinator runs; record it |
| Model | `claude-sonnet-5-5` for the main session and all agents (usage records) | the same model for both replicates; record it. A different model is a different experiment |
| Web tools | Tavily MCP absent; `WebSearch`/`WebFetch` used (`phase1/REPORT.md:235`) | same: do not add Tavily |
| Machine state read as evidence | `/opt/uv/tools/superclaude` (installed 2026-11-06), `/opt/nvm/.../bmad-method` and `bmad` 6.9.0, and the contents of `~/.claude` as the research agents listed them | same machine; these may differ now (UNVERIFIED), record `bmad --version` and the date |

## 3. Setup per replay session (repeat for each replicate; each replicate gets its own fresh copy)

1. **Fresh Coder copy at the original commit**, created the way the IronClaude rules prescribe, through Orca (not raw `git worktree add`, not `EnterWorktree`, no Orca link flags): `orca worktree create --name s4-g<N>-r<k> --repo <Coder selector> --base-branch f1ac0c93ad5a64b03f0ed49866d3adfe140c28b1` (the `<Coder selector>` is not known to me, UNVERIFIED; the coordinator has it). Check: `git -C <copy> rev-parse HEAD` prints `f1ac0c93ad5a64b03f0ed49866d3adfe140c28b1`.
2. **Untracked context the research read** (present in the original worktree before the run, not in git): `cp -r inputs/repo-untracked/.dev <copy>/` (12 files of `.dev/issues/478/` and the folder `.dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/`; their mtimes are all before 13:24Z). Do not copy the later `spec.md` / `spec-stage1.md`.
3. **Gate entry**: `tools/make_gate_entry.sh <N> <copy>/.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901` with N = 1, 2 or 3. It builds the task folder with `research/`, `synthesis/`, empty `qa/` and `reviews/`, `BUILD-REQUEST.md`, the report (Gate 3) and a copy of the task file in which every `- [ ]` before the gate's first step is ticked. Expected sha256 of the resulting task file: Gate 1 `d9f2a01f3122d6b2df544da1e1c935d8698cec71b9c1024eb747d6bb916abdb5`, Gate 2 `68ec150f145dd7200f1fa864d895e6fabb0bc629ac00f037a3a035f565795038`, Gate 3 `1f621e113b9bcbe3d4472d039a3335d8ba99b91522e55946e79708500dab5aba` (all 620,012 bytes). Every other file's sha256 printed by the script must equal its line in `inputs/MANIFEST.sha256`. The first unchecked box must be at task-file line 218 (Gate 1), 308 (Gate 2) or 371 (Gate 3).
4. **Stage and commit nothing.** The copy is throwaway. (The IronClaude rule to stage `.dev/tasks` applies to IronClaude, not to this Coder copy.)
5. Start a fresh Claude Code session with the Coder copy as working directory. The `qa/` folder must be empty; never copy `evidence/baseline-qa-outputs/` into it.

## 4. The instructions to give (same as the original, plus one stop rule)

The original instructions were: the coordinator brief (`briefs/S-user-resume-brief_L13.md`, `BM` L13), then `Skill tech-research` with the args in `briefs/S-skill-tech-research_L138.json`, then `Skill task` with the task file path (`briefs/S-skill-task_L156.json`). The `task` skill then executed the task file, whose steps hold every agent prompt (`briefs/taskfile-L*_embedded-prompt.md` are those prompts; `briefs/*_L<n>.md` are the short wrappers the executor wrote around them). The executor writes the wrappers itself; a fresh session will write its own, so the wrapper text will differ in wording but point at the same task-file lines. That is expected and is not a deviation to fix.

Replay message (verbatim, to the fresh session; replace `<N>` and the path):

```
REPLAY of a recorded run (experiment 346-validation, scenario S4, gate <N>). Do exactly what the task file says, from its first unchecked step, and nothing else.
Call the tech-research skill with: "Resume (do not rebuild) the existing task file .dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/TASK-RESEARCH-bmad-first-use-20261107-075901.md at the same depth it was built; execute it with the /task skill."
Then call the task skill with the path of that task file.
STOP RULE (this is the only difference from the original): when Gate <N> ends, either with a PASS decision or with GATE<N>_FINAL: FAIL - HALT after review 3, STOP. Do not ask the user or the coordinator for an exception to the 3-review limit, do not edit any file to clear open findings, do not start the next phase. Write replay-record.md in the task folder (template in REPLAY.md section 6) and report its path.
Make no change outside the task folder. No commit, push, PR or GitHub comment.
```

The original coordinator brief (`BM` L13) also asked for the Gate 4 sentence fix, three research answers, a spec and a plan; those are outside the gates and are not part of the replay.

## 5. Per gate: entry, review command, stop conditions

All reviews are `Agent` tool calls with only `subagent_type` and the prompt (no model or other option). Report-only agents carry `fix_authorization: false`; the one fix agent carries `true`. The severity rule is the task file's: only CRITICAL/IMPORTANT fail a gate, MINOR are notes never rechecked, at most 2 fix cycles (3 reviews), then HALT (`TF:130`, `TF:214`, `TF:361`).

| | Gate 1 | Gate 2 | Gate 3 |
|---|---|---|---|
| Entry (first step, task-file line) | 218 | 308 | 371 |
| Document under review | `research/01..05` | `synthesis/synth-01..04` | `RESEARCH-REPORT-bmad-first-use.md` |
| Review 1 | `rf-analyst` (TF:218), `rf-qa` (TF:222), `rf-qa-qualitative` (TF:226), in parallel | `rf-analyst` (308), `rf-qa` (312), `rf-qa-qualitative` (316) | 7 lenses in parallel: `rf-qa` x3 (371, 373, 375), `rf-qa-qualitative` x4 (379, 381, 383, 387) |
| Consolidation | the orchestrator (TF:230) | `rf-analyst` (320) | `rf-analyst` (391) |
| Fix | one `rf-qa`, `fix_authorization: true` (TF:234; may start gap researchers) | one `rf-qa` (324) | one `rf-qa` (393) |
| Review 2 (verification) | `rf-qa` structural (238) + `rf-qa-qualitative` (242) | (328, 332) | (397, 399) |
| Fix 2, review 3 | (254; 258, 262) | (344; 348, 352) | (405; 407, 409) |
| Stop | PASS at any review, or HALT after review 3 | same | same |
| Baseline | 9 / 6 / 1 blocking, HALT | 8 / 3 / 2, HALT | 18 / 5 / 2, HALT |
| Baseline cost (agents only) | 16 agents incl. 6 nested, 1,198 tool calls (incl. the gaps-log agent), 732k output tokens | 10 agents, 638 tool calls, 448k output tokens | 14 agents, 1,083 tool calls, 868k output tokens, 61 minutes |

Suggested safety cap (the coordinator may change it): abort a session and record `ABORTED-BUDGET` if it passes twice the baseline output tokens or twice the baseline wall time of its gate.

## 6. What to record per round (M1 to M5, DECISIONS.md D5)

Create `replay-record.md` in the task folder with one block per round (R1 = review 1, R2 = review after fix 1, R3 = review after fix 2):

```
Round R<k>
- start (UTC):, end (UTC):
- M1: review number k; verdict of each report (PASS/FAIL); gate decision line (first line of qa/qa-gate<N>-decision.md if the executor writes one)
- M2: per report: Critical / Important / Minor counts (copy the counts line of the report); consolidated BLOCKING_COUNT (first line of qa/qa-consolidated-findings-phase*.md); severity downgrades (SEVERITY_DOWNGRADES line)
- M3: for each blocking finding of R2 and R3: introduced by previous fix / exposed by previous fix / residual of previous fix / newly found in text the fix did not touch. Say whether the reviewer's own text gave the origin ("reviewer tag") or you decided ("re-derived"). Method used for the baseline: ANALYSIS.md section 7.
- M4: document size at the START of this review: sha256, bytes (wc -c), newline count (wc -l), summed over the gate's document set; and after the last fix
- M5: per agent: tool calls, output tokens, fresh input tokens (input + cache creation), wall seconds; and the orchestrator's own tool calls in the round. Source: the session's subagent logs under ~/.claude/projects/<project>/<session>/subagents/; the same extraction as tools/agent_costs.py (tokens counted once per message id)
```

Compare with `baseline-metrics.json` using the same definitions: lines = newline count; "blocking" = CRITICAL/IMPORTANT after consolidation. DECISIONS.md D6 then applies per scenario: last-round blocking <= 50 percent of the baseline's, or a clean pass in fewer rounds; growth over the gate <= 70 percent of baseline growth; effect larger than the spread of the two replicates. For S4 the baseline growth is +4.6 % (Gate 2) and +6.7 % (Gate 3) in bytes, +67.7 % (Gate 1).

## 7. Reconstructed parts (nothing hidden)

| Part | How it was obtained | Confidence |
|---|---|---|
| All briefs: the user brief (`BM` L13), 65 agent wrappers (writers: research, web, synthesis, assembler; reviewers; reviser/fix agents; consolidators), 64 embedded task-file prompts, the skill calls and skill texts | verbatim from the logs and file-history (`briefs/`, `inputs/skills/`); `briefs/INDEX.md` lists each with its jsonl line. **No brief is RECONSTRUCTED.** Not recovered, and why: (a) the prompts the Gate 1 fix agent wrote for its 6 gap researchers (agent-written, not coordinator briefs; each is the first user line of `SA/agent-<id>.jsonl`, ids in `evidence/agent-costs.tsv` rows `G1-F1-fix-nested-*`); (b) the text of the user's answers to the HALT questions (not found in the log; the decision files only report them); (c) the orchestrator's own reasoning between steps (not a brief). The Gate 1 consolidation had no agent: its instruction is `TF:230` | verbatim |
| Task file (what the executor read) | file-history `32d05845d5285d52@v2` (state at 2026-11-07T15:38:37Z; it contains the pre-start Gate 4 sentence fix, task-file log `TF:535`; `@v1` is the older state without it). The 61 agent-prompt lines equal the final file apart from checkbox state | verbatim |
| Task-file tick state and Task Log at each gate start | RECONSTRUCTED: every `- [ ]` before the gate's first step is ticked; the real ticks and log entries at that moment were not stored | high for the agents (they only read their own line); the log text differs |
| `research/01..05` at Gate 1 start; `synthesis/*` at Gate 2 start | RECONSTRUCTED by replaying every logged edit and heredoc append (`tools/reconstruct.py`); end of chain equals the stored file byte for byte; line counts match the reviewer's quoted counts | high, no stored copy |
| Report at Gate 3 start (and Gate 4, Gate 5 start) | RECONSTRUCTED by re-running the assembler's own `sed` commands on the stored synthesis files plus all logged edits; the Gate 3 end state equals file-history `ca7857aee503d1e6@v1` byte for byte | high |
| `research/research-notes.md` at Gate 1 start | derived by reversing 10 logged edits; a git object with the same hash exists in the Coder repo | exact |
| 8 + 12 research/synthesis/gaps states at Gate 2 and Gate 3 start | replay; all 20 hashes exist as git objects in the Coder repo | exact |
| Untracked context (`inputs/repo-untracked/`) | copied from the original worktree as it is now; all mtimes precede the run (13:24Z) | high, UNVERIFIED that they were not touched without a mtime change |
| Answers of the user to the HALT questions | not replayed (the stop rule replaces them) | n/a |

## 8. Known sources of difference you cannot remove

LLM non-determinism (findings differ per run, so two replicates will not match the baseline round by round; this is why D6 asks for two replicates and a spread); the 3-review cap ending in a HALT instead of the user exception; web access and machine state (section 2); the executor's wrapper wording (section 4); Gate 5 round 1 in the baseline (brief errors). The baseline is a single run: its own run-to-run spread is unknown.

## 9. Does PR 427 matter here? (plain statement, repeated from section 0)

No. The review tool is not `/sc:spec-panel`, so PR 427 cannot change the outcome of this scenario. A coordinator who needs scenarios where 427 can matter should not count S4 toward the "427 proven" test. That is a decision for the coordinator, not a gap in the recreation, so no `candidate-swap.md` is written (the grade is B).

## RECREATION GRADE

**B: minor reconstructed parts, listed.** Briefs and skill texts are verbatim and complete (A-quality), the tool is the same (`tech-research` and `task` skills, same agent types, same installed files, same model class), and every starting document needed for Gates 1 to 3 exists byte-exact (Gate 2 and 3 research and synthesis inputs, final files, research-notes) or is rebuilt by a deterministic replay whose end points match stored files byte for byte (Gate 1 research files, Gate 2 synthesis files, the report at Gate 3 start). The reconstructed parts are only: (1) the 12 replay-only starting states, (2) the task-file tick state and Task Log at gate start, (3) the replay unit is a gate entry, not the 8.5-hour pipeline (Gates 4 and 5 not packaged as runnable), (4) machine and web state, (5) the exception step replaced by a stop rule. It is not A because of (1) to (3) and not C because no input or brief is missing.

RECREATION GRADE: B
