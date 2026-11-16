# Tasklist review panel evaluation: where things stand, open questions and decisions left (2026-11-15)

> **UPDATE 2026-11-16:** the owner **stopped the Sweep Sheet**. Its recall gate failed twice (7 of 34 independently seeded defects located, 21%, against 80% required); see `20261114-sweep-sheet/results/freeze-check-20261115-rerun.md` and the status box in `20261114-sweep-sheet/OPEN-ITEMS.md`. Rows below that concern the Sweep Sheet freeze, its parity test, hold-out author or format-forgiveness build are void for it. Still live: the Recipe Ledger (`20261114-recipe-ledger/`, its own open decisions are in `OPEN-DECISIONS-20261115.md`), the shared control for the Recipe Ledger against Z0, and the model-policy hook (#546, #551). The table below is otherwise the 2026-11-15 13:50 UTC state.

> **UPDATE 2026-11-16 (evening), three things changed since the box above:**
> 1. **The Recipe Ledger was run after all** (owner order "run the recipe ledger experiment 3 times", then "run 6 more"). 9 replicates x 3 arms (plain panel Z0, plain-words K, Recipe Ledger RL) x 3 study packages = 81 panel runs on the ember panel, judged blind. On the two defect-rich packages RL found 2.00 of 14 per replicate against 0.67 for Z0 and 0.56 for K (two-sided p about 0.012 and 0.013, computed after seeing the data); wrong blockers fell from 14 and 16 to 5 over the 9 replicates; real blocking finds did not differ. **But** RL's median panel time is 1.46 x Z0 on `designSpec` and 1.60 x on `design` (cap 1.35), and the format check would fail 58% of RL reports if nothing were forgiven (it passes only with the owner-approved allowances). Exploratory: never frozen, study packages only, one panel. Details: `20261114-recipe-ledger/results/derivation-3x/SUMMARY.md` (first 3 replicates) and `SUMMARY-9reps.md` (pooled). This answers the old question 3 below ("3 tests each on the study packages"): it was run, as a derivation check, not as adoption evidence.
> 2. **Owner answers of 2026-11-16 were recorded** (documentation only; no code, tests, issues, merges or deployment authorised). *Model-usage policy:* for the first release, model-usage compliance infractions must NOT halt work: log the incident and report warnings after the fact. This supersedes every earlier answer that favoured blocking forbidden, unknown, out-of-list or wrong-stage models; strict verification of the served model is not a v1 gate. The exception is narrow: actual blocking findings still go through the established refactor-and-review process, and quality gates and platform safety stay in force. The full record, 11 decisions and what stays open, is in `../../brainstorms/20261114-jev-model-validation-hook/OPEN-QUESTIONS.md` (row 10 below is therefore answered in principle; its remaining open parts are listed there). *Shared directions:* the active workflow is `/sc:workflow` and `/sc:implement`; `sprint run` in its current form is obsolete and is not to be tested as the current workflow; `/sc:task` and task-builder are to be retired (a retirement decision, not a claim that removal happened, and not to be evaluated); only the Sprint run CLI tool suite is to be evaluated for measurable benefit against retirement, and any return of it must be refactored around workflow/implement and evaluated properly. Future agents must not revive obsolete-command testing as if it were the current workflow. *Session handling:* acknowledge an answer once, briefly, and move to the next applicable question; do not repeat the answer or invent questions.
> 3. **Recommended next steps** (not yet ordered by the owner): (a) hold-out documents with answers written by fresh sessions after a freeze, then a frozen Z0-against-RL comparison; (b) decide whether RL's 46 to 60% time overrun on two packages is acceptable; (c) if RL continues, decide whether to keep or tighten the format allowances (the result depends on them); (d) an evaluation plan for the Sprint run CLI tool suite, as the owner directed.

## Read this first (context for someone arriving with no history)

**What this is.** IronClaude is a framework of commands for Claude Code. One command, `/sc:workflow`, writes an implementation plan (a "tasklist") and then has a group of AI reviewer models, called a **panel**, review that plan before anyone builds it. The owner is evaluating **which cheap reviewer models, and which ways of running the panel, find the most real defects**, because the cheap panels miss many of them. This folder (`.dev/eval-workspaces/tasklist-review-panel/`) holds that evaluation.

**Branch and repository.** Branch `ironbelly/eval-tasklist-review-panel` in the worktree `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel`. The only remote is `origin` = `https://github.com/IronbellyOrg/IronClaude` (the owner's fork).

**Hard rules that apply to anyone working here (owner rules, repeated in `CLAUDE.md` and `~/.claude/`):**
- Push only to the fork `origin`, and only when the owner asks. Never push to, fetch from, comment on or open anything at `SuperClaude-Org/SuperClaude_Framework`. Pull requests are opened only with `/sc:pr-submit --monitor 3`.
- Never stage or commit anything under `.claude/` (except `.claude/settings.json`). `.dev/tasks/` is always staged (`git add .dev/tasks`), never gitignored. Staging is not committing; commit only when asked.
- Python only through `uv` (`uv run ...`), never `python script.py`.
- Models: Sonnet and Haiku for everything. Opus (`claude-opus-5-5`) only for the blind scoring judge. Never Fable or any Tier 0 model; Qwen3.8-max and glm are excluded from the evaluation. Check what model actually answered: on this gateway the Haiku alias has answered as `gpt-6.1-sol`.
- At most 2 `claude` sessions at once across everyone. Take a slot with `.dev/eval-workspaces/tasklist-review-panel/20261114-collab-process/with-slot.sh <label> <command>`; `--status` shows who holds one.
- Keep intermediate files: quarantine, never delete. Raw model transcripts, `runs/` folders and files over 400 KB are not committed.
- Never read ground-truth files (the known-defect answer keys, `ground-truth*.json`) unless your task says so: a model or author that has seen them contaminates the result.

**Words you will meet.**
- **ember** = model `muse-ember-1.0`; **luna** = `gpt-6-luna`. The default cheap panel ("ember panel") is ember + 2 x luna. Other panels: haiku + 2 x luna, sonnet + 2 x luna.
- **Study packages** = three finished plans used as test material: `TASK-WF-designSpec-20261107-075614`, `TASK-WF-makeTheAliasOnly-20261105-051649`, `TASK-WF-design-20261108-041415`. **Ground truth (GT)** = the list of known real defects in each. **Found of 14** = how many of the 14 known defects (in two of the packages) a panel run reported; the third package is a control. Judging is blind: an Opus session scores anonymised reports against GT.
- **Z0** = the control arm: the plain panel with harness fixes H1-H4 and brief edits CB-1 to CB-5, no redesign. **SS** = Sweep Sheet redesign. **RL** = Recipe Ledger redesign. **K** = a plain-words control for SS.
- **Hold-out documents (HO-1 to HO-6)** = fresh plans and specs, not study packages, used to test generality. Their GT must be written only after the designs are frozen.
- **Freeze** = tag and hash the cards, extractors, recipes and briefs so they cannot be tuned after seeing answers.

**Files to read next, in order:** this file; `20261114-collab-process/PROCESS.md` (how the two redesign sessions work together and the owner-decision table); `20261114-sweep-sheet/OPEN-ITEMS.md`; `20261113-collab/RESULTS-20261114.md` (the earlier collaboration experiment); `20261111-a1/COMBO-REPORT.md` (the first panel evaluation); `20261114-recipe-ledger/IMPLEMENTATION-REPORT.md` section 5.1 (what the other redesign has not met). This file was written from the state on disk at about 13:50 UTC on 2026-11-15; check `git log` and `git status` before relying on it.

## What has been done

| Stage | Outcome |
|---|---|
| Panel combinations (`20261111-a1/`) | Many reviewer-model combinations scored against the study packages. Recommended default then: ember + 2 x luna, 64k tokens, about 6 minutes, 1.83 of 14 found (6 runs). Likely inflated: see "Open questions" 7. |
| Five collaboration designs (`20261113-collab/`) | Five ways to let panel members exchange messages were designed, built and run on three panels. Result: no reliable gain. Design 4 looked best at 6 runs per arm (+1.17 found, 10% chance by luck) and fell to +0.50 at 12 runs (27% by luck, +13% time). Design 1 showed none. Recommendation recorded: stop that line. Written up in `20261113-collab/RESULTS-20261114.md`; committed. |
| Two process redesigns (brainstorm) | `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md`: Sweep Sheet (a script pulls up to 12 typed items from a plan and cheap reviewers judge one item at a time) and Recipe Ledger (written class recipes and a forced list-then-judge ledger). Not yet tested on any model. |
| Sweep Sheet build (`20261114-sweep-sheet/`) | Designed, planned (33 tasks) and built: 33 of 33 tasks complete, 749 tests pass (4 "freeze" tests deselected). Tests use a fake `claude` only; no live model run has ever been done with its launcher. Package archived at `.dev/tasks/done/TASK-WF-implementHomeCod-20261114-200449/` and staged, not committed. The build files are untracked. |
| Sweep Sheet defaults (owner order 2026-11-15) | Three adversarial debates: act bands FAIL then refactored (`DESIGN.md` 15.1a); CB-2 verbatim PASS; K-arm lead-in PASS. Floor for the offline selection-recall gate G0 = 0.45. All recorded in `20261114-sweep-sheet/results/owner-decisions.md`; the numbers are in `20261114-sweep-sheet/config/owner-values.json` (not committed). |
| Recipe Ledger build (`20261114-recipe-ledger/`, another session) | 20 of 20 tasks complete per that session; 547 tests pass, 3 fail by design (two need real GT; one needs a second-author review). Its report lists requirements not met. Verified by this file's author: not independently. |
| Two-session process | `20261114-collab-process/PROCESS.md`: both sessions agreed; the owner confirmed it in both sessions on 2026-11-15. |
| Model-policy hook (IronClaude issues #546 and #551) | After an incident where Opus was used for non-scoring work (about 4.2 million output tokens), a version 1 design for a hook that rejects any model not requested or defined was brainstormed (`.dev/brainstorms/20261114-jev-model-validation-hook/merged-requirements.md`, 63 requirements). Committed and pushed. Not implemented. |
| Host fault | Coder issue #505 (sysbox FUSE mounts return "Transport endpoint is not connected"). Not fixed by this work. |

## Owner decisions already made (do not re-ask)

- Time rule: the +35% elapsed-time cap may be exceeded for the collaboration designs (2026-11-14).
- Replicates for designs 1 and 4, and the final batch of 12 runs per arm for design 4 (done). Designs 3 and 5 dropped.
- Process file confirmed; hold-out documents; one shared control gated by a brief-parity check; go on the freeze of both designs (2026-11-15, in both sessions).
- G0 floor 0.45 pooled; per-class act bands with the 15.1a registration text; CB-2 left verbatim; K-arm lead-in approved as drafted.
- Freeze helpers may be fresh Sonnet **sessions** instead of people (SS: 2026-11-15; RL: approved in its session). This weakens the independence the design asks for; the files must say "session", not "person".
- Recipe Ledger: seven recommended defaults of its `DESIGN.md` 13.1 approved; two model spikes (5-run compliance, 10-run luna timing) approved, run one at a time under the slot lock.

## Open questions and decisions left

Numbers refer to who must act. "Owner" = the user. "SS" and "RL" = the two redesign sessions.

| # | Question or decision | Who | Needed before | Notes |
|---|---|---|---|---|
| 1 | Who writes the **hold-out ground truth** (HO-1 to HO-5 answers) and attests they have not seen the cards, recipes or extractors? | Owner (decision), then an author session | any live experiment arm | Must happen after the freeze tag. The hold-out documents are not identified in any file I checked; the brainstorm (`merged-requirements.md` section 5.1) only describes them as HO-1 to HO-6 and points to an investigation file I did not open. |
| 2 | **Freeze tag and hash list** for SS (and RL) | SS, RL | any live arm, RL's copy of shared files | SS needs the second-author fixtures first (a session is running), then its files committed, then `bin/freeze.sh`, then the printed `git tag` run. Tagging is a repository write; the owner said go. |
| 3 | **Parity test** of the shared control: Z0 brief, sandbox build, model and flags, retry/fallback rules, judge script, anonymiser and merge command identical for every document | SS and RL | the shared control run | If any item differs, each session runs its own control. Not run yet. |
| 4 | **Shared control run**: one Z0 run on the hold-out documents, written by RL into `20261114-shared-control/` | RL, owner approval of the document list | Stage 1 | Document list = hold-out documents (answered); the exact list is not written. |
| 5 | Wrap every `claude -p` in the SS launcher and judge scripts in `with-slot.sh` | SS | any SS live run | Commitment made in PROCESS.md O3; not done. |
| 6 | Spikes for SS (compliance, timing) | Owner go-ahead per part | Stage 1 | `20261114-sweep-sheet/TESTING.md` section 5. Not started. |
| 7 | **Was the old 1.83 baseline inflated?** Two earlier reviewers' reports say the old shared checkout `/tmp/evalsb/repo` already held the finished work ("post-implementation"), which makes defects easier to find. The folder is gone, so it cannot be confirmed. | Owner | none, but it changes how earlier numbers are read | Option offered and not taken: rebuild a post-implementation sandbox and run 6 plain-panel rows as an estimate. |
| 8 | Commit and push of the Sweep Sheet build, owner-values file, debates and this documentation | Owner (order), then one session | any freeze | Nothing from `20261114-sweep-sheet/` is committed yet. The RL session's folder is committed or not by that session. |
| 9 | Whether the 3 failing/deselected "freeze" tests and the 19 open manual checks may be closed by sessions | Owner | freeze | See `20261114-sweep-sheet/OPEN-ITEMS.md`. |
| 10 | Model-policy hook (#546, #551): decisions on 11 restrictions (see #551), the unverified facts (does the prompt event fire for `/model`, hook environment, hook timeout behaviour, whether hook stderr reaches the person), then a design document and checked plan | Owner | any implementation | Version 2 (dynamic routing, may use the Jev judgment model) has no issue yet. A comment on #546 records a second Opus-class use found on 2026-11-15. |
| 11 | Design 2 (Idle-Shift Sweeper) re-audit and the earlier collaboration-line rows | none | none | Closed per `RESULTS-20261114.md`; the line is stopped. |
| 12 | Host fault (Coder #505) | Platform owner | none for the evaluation | Can recur and empties logs of headless runs. |

## Things that could mislead you

- **Single runs are noise.** On the ember panel the same-harness baseline alone scored 0, 2, 3, 1 and 1 across five designs. Do not read a one-run gap.
- **Estimates are not measurements.** The Sweep Sheet floor, act bands and time table rest on estimates from the brainstorm. The 0.45 floor passes a design at its estimated lower-end recall only about 63 to 70% of the time (binomial calculation, assumes 20 to 40 hold-out issues).
- **Sessions are not people.** Where the design asks a person (second author, hold-out author, tag), a session stands in by owner order; the files must say so.
- **Agreement between sessions is not owner approval.** Only the owner's own messages count. The peer sessions relay and record; they cannot approve.
- **Not independently verified:** the Sweep Sheet build's own "compliant" ledger lines, the Recipe Ledger session's reported test counts, and the debates' verdicts (scored by one Sonnet session each).
