# QA Report: Task-Research Alignment

**QA mode:** task-integrity
**Lens:** task-research-alignment
**Date:** 2026-11-07
**Task file:** TASK-RESEARCH-orchestrator-supervision-20261107-073942.md (445 lines)
**Research dir contents (actual, on disk):** research-notes.md (306), scope-01-contract.md (146), scope-02-orca-recovery.md (219), scope-03-cli-patterns.md (196), scope-04-409-layout.md (330)

Note: the spawn prompt listed 05-orca-row-schema.md, 06-orca-open-questions.md, web-01 and web-02 as present. None of those files exist on disk. That is expected, not a defect: research-notes.md `:215-218` marks them "MISSING, planned", and the task creates them in Steps 2.5, 2.6, 4.1 and 4.2. This review checks the task items that will produce them against what the research asks them to deliver.

Also read: BUILD-REQUEST.md (all 227 lines), because several task claims come from it rather than from the research.

Grading: BLOCKING means a load-bearing research finding is dropped, an action is not grounded in the research, or a claim is wrong. MINOR means wording, citation or other nits.

---

## Findings

### Finding 1 (BLOCKING): option A4 is labelled CODE-CONTRADICTED as a whole and rejected in advance, but the research leaves it open

**Task claim.** Execution Context `:90` says "options A1-A4 (A4 is CODE-CONTRADICTED)". Every synthesis prompt (`:202`, `:206`, `:210`, `:214`, `:218`, `:222`, `:226`) says "Option A4 (extend sc-crash-recovery) is [CODE-CONTRADICTED] and may appear only as a rejected option with its reason". Step 5.4 `:218` tells synth-04 to show A4 "as rejected because it is [CODE-CONTRADICTED]". The Step 5.7 gate `:234` checks that A4 is shown only as rejected. The feasibility lens `:294` checks that "A4 is not recommended". The fidelity gate `:322` lists "option A4 rejected" among "every decision the sources fix". Task Log `:429` says A4 "is CODE-CONTRADICTED by the research notes".

**What the research says.**
- research-notes.md `:160` (A4 row): the tag "[CODE-CONTRADICTED for this host]" covers one claim, the 72 h default and `~/workspace/` path (`SKILL.md:25-27`). The same row lists other cons (bootstrap_scan.sh `:31`/`:73`, allowed-tools is not read-only, mixed concerns). Those are disadvantages of the option, not a contradiction of it.
- research-notes.md `:162`: "Leaning from the scopes: A1, keeping the report shape and SAFE/REVIEW vocabulary from crash-recovery (A4) without its scripts. The decision is still open (seed brief open question `:77`)."
- research-notes.md `:277`, AMBIGUITIES_FOR_USER item 1: where the logic lives (A1/A2/A3/A4) is an open owner question.
- C3 and C4 (`:295-296`) contradict two claims about sc-crash-recovery ("is read-only", "`--all` scans `~/workspace/`"), not option A4.
- None of scope-01..04 contains "A4". scope-03 does not mention the option at all. scope-02 has CODE-CONTRADICTED only on two crash-recovery claims: the "read-only" allowed-tools (`:119`) and the `~/workspace/` path (`:121`). Its Summary (`:218`) lists what can be reused from sc-crash-recovery: the SAFE/REVIEW labels, the "could not determine" section, the report template and `parse_session_log.py`. So BUILD-REQUEST.md `:21` ("option A4 is CODE-CONTRADICTED by scope-03") cites a source that has no such finding. The task copies that wrong claim and then says it comes from "the research notes" (`:429`).

**Why it blocks.**
1. The task presents an owner decision that is still open (AMBIGUITY 1) as a decision the sources have made (`:322`). The fidelity gate would then fail a report that correctly says the decision is open.
2. Step 2.2 `:126` tells the verify agent to "Keep option A4 ... tagged [CODE-CONTRADICTED]" in scope-02, but scope-02 has no A4 tag. The agent can only fail the instruction or write a new tag into a research file, which is a fabricated action.
3. "May appear only as a rejected option" pushes synth-04 to drop the research's own recommendation (`:162`): reuse A4's report shape and SAFE/REVIEW vocabulary within A1.
4. Step 5.4 also says "Do not assume A1 wins", while A4 is fixed as rejected in advance. The options analysis is therefore pre-decided on the one option the research could not settle.

**Remedy.**
- Replace the A4 sentence in `:90`, `:202-226`, `:218`, `:234`, `:294`, `:322` and `:429` with this: "Option A4 (extend sc-crash-recovery) has code-contradicted premises: the 72 h default and the `~/workspace/` path (research-notes `:160`, C4), allowed-tools that are not read-only (C3), and the bootstrap_scan.sh bugs at `:31`/`:73`. Assess it like A1-A3. Where to put the logic is an open owner decision (AMBIGUITY 1). The research leans to A1 and reuses A4's report shape and SAFE/REVIEW vocabulary (research-notes `:162`)."
- Remove the "Keep option A4 tagged" clause from Step 2.2.
- The wrong claim comes from BUILD-REQUEST.md `:21`. If the owner really decided to reject A4, record that decision and its source in the task file. Otherwise, escalate the conflict between the build request and the research to the user. Do not leave it as an unattributed "research" fact.

### Finding 2 (BLOCKING): Step 2.6 drops half of what critical gap G-B must deliver (the fallback signals)

**What the research asks for.** research-notes.md `:216` defines what `06-orca-open-questions.md` must deliver: "A read-only, non-consuming way to list pending `ask` questions for the needs-person class, **or a stated fallback (`agentWait`, `blocked_question`, Ruling halt, frozen plan)**". G-B is rated Critical (`:245`). scope-04 open question 2 (`:314`) adds what happens if questions cannot be fully listed: the header must say messages coverage is partial or unavailable (`PKG/DESIGN-CONTRACT.md:11`). #409 also notes that complete non-consuming enumeration "beyond a 100-row CLI view" is not established (scope-04 `:257`).

**Task item.** Step 2.6 `:142` asks how questions reach the coordinator, whether reading consumes them, how peer sessions appear and what a frozen worker looks like. Per question it asks for "the answer, the evidence, whether reading is destructive, and the consequence for a read-only sweep". It never names the fallback set, and it never asks the agent to judge whether `agentWait`, `blocked_question` or a Ruling halt can stand in for a non-consuming read. The "frozen worker" question covers only "frozen plan". The Phase 3 gate `:166` checks only "whether G-B is now answered ... including whether reading Orca messages consumes them". A file that says "no non-consuming read exists" therefore passes the gate, and the needs-a-person class (the one the sweep exists for) is left with no source.

**Why it blocks.** The fallback list is the part of the G-B finding that keeps the design workable when the main answer is "no". It is load-bearing for the classifier (the needs-person row of the class table in research-notes SOLUTION_RESEARCH C) and for the feasibility lens `:294(a)`.

**Remedy.** Add to Step 2.6: "If no read-only, non-consuming read of pending `ask` questions exists, evaluate each fallback named in research-notes `:216` (`agentWait` on a worker-list row, `blocked_question`, a Ruling halt, a frozen plan). For each, state whether it is readable without changing or consuming state, which session class it can support, and what it misses. Also state the messages-coverage value (complete, partial or unavailable) the report header must print (scope-04 `:314`, the `:257` 100-row limit)." Mirror this in the gate check `:166`.

### Finding 3 (MINOR): the 6 h "bounds activity only" window is given to every synthesis agent as fixed scope, though research marks it DERIVED and open

**Evidence.** research-notes.md `:195` calls this a "DERIVED point for the design". AMBIGUITY 2 (`:278`) leaves both the 6 h vs 72 h default and whether the window applies only to activity open. The shared research-question context in Steps 5.1-5.6 (`:202-226`) says "over a default 6 h window that bounds activity only" as a fixed requirement. BUILD-REQUEST.md `:12` says "a default 6-hour window" and nothing about "bounds activity only". Step 5.6 `:226` does route AMBIGUITIES 1-11 into Section 9. So the question is not lost, but synth-02/04/05 are told to design to one answer while synth-06 lists it as open, which invites a cross-section inconsistency. ("stalled (proved)" IS grounded: research-notes `:188`.)

**Remedy.** In the shared context, write "a default 6 h window (issue #339; AMBIGUITY 2 is open on the default and on whether it bounds activity only, the research's DERIVED leaning, research-notes `:195`)".

### Finding 4 (MINOR): Steps 2.1 and 2.3 edit the scope files although the research says "verify only" and puts the summary in the gaps log

**Evidence.** research-notes.md `:231` says Phase 2 is "verify only, no re-investigation". For scope-01 and scope-03, `:235`/`:237` say "no 'Summary' heading (accept, or add a one-paragraph summary in the gaps log, not in the file)". Task Steps 2.1 `:122` and 2.3 `:130` tell the agent to append a `## Summary` to the scope file itself, and to add tags and fix line numbers in place. The task follows BUILD-REQUEST.md `:98`, which authorizes this, and the Phase 3 gates `:152`/`:154` need a `## Summary` in every file. So it is grounded in the build request, but the departure from the research notes is not recorded.

**Remedy.** Add one line to the Task Log: "Steps 2.1/2.3 append `## Summary` in-file per BUILD-REQUEST `:98`, overriding research-notes `:235`/`:237`."

### Finding 5 (MINOR): the #409 "proposed only, unmerged" caveat is not passed to the synthesis agents that design the report

**Evidence.** scope-04 `:249-262` says the #409 field names, ID formats, source ids, timeline buckets and the 08:00 clock are proposed only, not an Orca contract. The package is unmerged at 495eb96d (`:260`). Open question 8 (`:320`) recommends pinning the commit. scope-04 also records two CODE-CONTRADICTED layout facts a static report must correct: there is no sort in code, so it must sort oldest first explicitly (`:93`), and the wide views have no omission count (`:247`). The task keeps the DERIVED label (`:134`, `:320`) and mentions omission counts in web-02 (`:196`). But the shared synthesis context only says "a dated static report on the #409 layout". It does not tell synth-04/05 which #409 parts are reusable (semantic rules) and which are not (field names), and it does not mention the explicit oldest-first sort. Step 3.2 does carry scope-04's open questions into the gaps log, which partly covers this.

**Remedy.** Add to the Step 5.4/5.5 prompts: "Reuse only the #409 semantic rules (scope-04 `:262`). Field names and IDs are proposed only, so pin 495eb96d. Sort needs-a-human oldest first explicitly and print `<shown>/<total>` omission counts (scope-04 `:93`, `:247`)."

### Finding 6 (MINOR): the read-only exclusions of data sources are given only to synth-04

**Evidence.** research-notes.md `:178` excludes `orca open`, `check --wait`, `ccsession --list` (it writes, `:175`) and `bootstrap_scan.sh` as-is. scope-02 open question 8 (`:210`) adds excluding `git stash *` from allowed-tools, allowing only `git stash list` (`:119`). Only Step 5.4 receives SOLUTION_RESEARCH A-D. Step 5.5 (`:222`), which names the Phase 1 files and allowed tools, gets scope-02 but no instruction to honor the exclusion list. The feasibility lens `:294(a)` checks read-only only in general.

**Remedy.** Add to the Step 5.5 prompt and the `:294` checklist: "Phase 1 steps must not use any source excluded in research-notes `:178` or allow `git stash *`."

### Finding 7 (MINOR): `template_schema_doc` points to a copy the research says is missing

**Evidence.** Task `:34` gives `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"`. research-notes.md `:268` and BUILD-REQUEST.md `:222` both say the project `.claude/templates/workflow/` copy is MISSING in this worktree and name `~/.claude/templates/workflow/...` or `src/superclaude/templates/workflow/...` instead.

**Remedy.** Point the field at `~/.claude/templates/workflow/02_mdtm_template_complex_task.md`.

### Finding 8 (MINOR): Step 2.1 does not pass contradiction C1 to its verify agent

**Evidence.** research-notes.md `:293` (C1): scope-01 uses the outdated F1-F12 numbering. The current analysis file has F1-F14 and S1-S5 (`.dev/issues/339/analysis/analyze-worker-contract.md:30-55`). Step 2.1 `:122` tells the agent to re-check scope-01's citations but does not mention C1, so the renumbering may survive verification. Step 3.1 cross-validation does list C1-C12 as known conflicts, which is a later partial catch.

**Remedy.** Add to Step 2.1: "Renumber scope-01's analysis-finding references to the current F1-F14/S1-S5 (C1), marking each `(re-verified 2026-11-07)`."

---

## Checks that passed (evidence)

| Check | Result | Evidence |
|---|---|---|
| Each SUGGESTED_PHASES item has a matching task item | PASS | 2.1-2.4 verify items `:122-134`; 2b.1/2b.2 as Steps 2.5/2.6 `:138`/`:142`; web-01/web-02 `:192`/`:196`; synth-01..06 Steps 5.1-5.6 |
| The four non-critical gaps get no agent and go to the gaps log | PASS | research-notes `:247`; task Step 3.2 gaps-and-questions item `:182` |
| G-A deliverables (projection, liveness values, agentWait shape, paging, cost) | PASS | research-notes `:215`; Step 2.5 `:138` |
| Read-only limits on the gap-fill agents | PASS | `:138`, `:142`: only `--help`/`orca-ide skills get`; 495eb96d via `git show` to stdout only |
| Web agents map each pattern to WC-10 and read-only | PASS | research-notes `:249`; task `:192`, `:196` |
| Synthesis inputs match research-notes `:253-260` | PASS | 5.1-5.4 and 5.6 match. 5.5 `:222` takes a grounded superset (adds scope-02, 05, 06, synth-02, synth-04, gaps log) |
| synth-05 keeps the phase split | PASS | research-notes `:262`; task `:222` |
| AMBIGUITIES 1-11 and C1-C12 carried forward | PASS | Step 3.2 `:182`; Step 5.6 `:226` (Section 9) |
| `reviews/` folder in Step 1.2 | PASS (grounded) | BUILD-REQUEST `:94` |
| Phase ordering reflects dependencies | PASS | 05/06 produced before the Phase 3 gate; gaps log before web research and synthesis; 5.5 only after 5.2 and 5.4 exist (`:222`); assembly after the synthesis gate |

---

## VERDICT: FAIL

Blocking issues: 2. Minor issues: 6.

| # | Severity | Issue | Location |
|---|---|---|---|
| 1 | BLOCKING | Option A4 is called CODE-CONTRADICTED as a whole and rejected in advance; the research tags only its path premise and leaves the choice open (AMBIGUITY 1). The claim comes from BUILD-REQUEST `:21`, which cites scope-03, and scope-03 never mentions A4 | task `:90`, `:126`, `:202-226`, `:234`, `:294`, `:322`, `:429` |
| 2 | BLOCKING | Step 2.6 drops the G-B fallback set (`agentWait`, `blocked_question`, Ruling halt, frozen plan) and the messages-coverage consequence | task `:142`, `:166` |
| 3 | MINOR | The 6 h "bounds activity only" window is framed as fixed scope, though it is DERIVED and AMBIGUITY 2 is open | task `:202-226` |
| 4 | MINOR | The in-file `## Summary` departs from the research notes' "verify only" without a note | task `:122`, `:130` |
| 5 | MINOR | The #409 "proposed only / unmerged" caveat and the explicit oldest-first sort are not passed to synth-04/05 | task `:222` |
| 6 | MINOR | The data-source exclusion list is not given to synth-05 or the feasibility lens | task `:222`, `:294` |
| 7 | MINOR | `template_schema_doc` points to the missing `.claude/` copy | task `:34` |
| 8 | MINOR | C1 renumbering is not passed to Step 2.1 | task `:122` |

