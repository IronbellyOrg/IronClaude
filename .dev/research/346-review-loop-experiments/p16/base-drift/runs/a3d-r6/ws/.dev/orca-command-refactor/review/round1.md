review: 1 of 3

# Spec-panel critique, round 1: orca-worker-contract-spec.md

## Header
- Command run: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (acted out from `command.md`; no slash command available in the sandbox).
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full).
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: not applicable (first review; no `--re-review`, no `--baseline`)
- reviewer model actually used: claude-sonnet-5-5
- Mode: critique; focus: requirements, architecture. Not `--unattended`; not `--improve`, so no improved specification is written and the candidate is untouched.
- Binding context read first: `.dev/orca-command-refactor/README.md` (lines 1-38).

## Coverage
Read in full: the candidate (285 lines), `README.md`, `inventory/commands-a.md` (120 lines), `inventory/commands-b.md` (323 lines), `inventory/orca-capabilities.md` (188 lines).

Citation check. The inventories under `.dev/orca-command-refactor/inventory/` are the only evidence checkable here. I resolved every `INV-A:N`, `INV-B:N` and `CAPS:N` reference in sections 1-4 of the candidate, plus `README.md:6,11-17,30,31`, against those files. Each pointed at the content the candidate attributes to it. The per-command row mapping (section 3.1 and 3.2 to inventory rows) and the counts (10 ready / 27 needs-change / 6 coordinator-only = 43; 21 + 22) match the inventories. I also recounted the phase assignment: P1 9 + P2 11 + P3 4 + P4 3 = 27 for section 3.2, and 4 + 4 = 8 of the 10 ready commands get a phase (brainstorm and init-lite get none); no command is dropped or double-counted.

UNVERIFIED, because the file is not inside the sandbox: every citation to `src/superclaude/...` (`cmd/`, `sk/`, `install_core.py`, `Makefile`, `pyproject.toml`), `CLAUDE.md:N`, `src/superclaude/core/HOW-WE-WORK.md:N`, `src/superclaude/core/CLAUDE.md:N`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/...`, the grep results quoted in E5, the 11 locations the candidate says it re-read (line 11), and its closing claim of an independent 340-citation check (UNVERIFIED item 14). I rely on the inventories' quotations of these only where the candidate itself cites the inventory.

Not covered: correctness focus (not requested), so no State Variable Registry; no live Orca behaviour.

## Panel (review order)
Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Findings below are attributed to the expert who raised them.

=== REQUIREMENTS ANALYSIS ===

### F1 (BLOCKING, CRITICAL) Acceptance check AC-1.1 cannot pass for `/sc:load`
- Expert: Wiegers (testability), Adzic.
- Grading sentence: An implementer who follows the stated text as written builds a `## Unattended mode` section naming `return-contract.yaml` in `/sc:load` (because AC-1.1 asserts it for every command in sections 3.1-3.2), and that is wrong because the same spec says `/sc:load` gets no report file and a contract would be "an unrequested addition".
- Evidence:
  - AC-1.1 (`specs/orca-worker-contract-spec.md:195`): "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - `/sc:load` is a section 3.2 row (`:112`): Report "none (see note)", Resume "n/a", Other change "use it as a step inside another worker's brief, not as its own Task", phase "P1 (usage line only)".
  - Decisions table (`:265`): "Use it inside a brief: its only output is context for the current session ... a report file would be an unrequested addition. Only its usage-line defect is fixed."
  - P1 scope (`:159`) lists `load (usage line only)` and also says the flag is accepted by "every command in sections 3.1 and 3.2".
  - AC-1.2 (`:196`) runs the live check on each P1 command, and 7.2 step 4 (`:183`) requires a `return-contract.yaml` that passes the status check; `/sc:load` cannot satisfy it either.
- Why blocking: an acceptance criterion the stated text cannot pass; two stated texts (AC-1.1 and the load row plus its Decision) contradict.
- Recommendation: exclude `/sc:load` from the AC-1.1 and AC-1.2 sets in one clause, or state that it gets the section with "no contract, no-op".
- Priority: High. Quality impact: removes a gate that fails on first run, about 0.3 of a Testability point.

### F2 (BLOCKING, MAJOR) Phase 1 requires the unattended mode on commands whose rules the spec defers to Phases 2-4 and to user decisions
- Expert: Wiegers (requirements consistency), Cockburn (who decides what, when), Fowler (phase boundaries).
- Grading sentence: An implementer who follows the stated text as written builds, in Phase 1, an accepted `--unattended` flag and `## Unattended mode` section on `implement`, `post-release`, `pr-submit` (and on the gated Phase 2 commands such as `auggie-review` and `task`) with no gate resolution behind it, and that is wrong because WC-2/WC-9 say that under `--unattended` no prompt waits and no outward default fires, and section 6 says the gate rows land in P2 and P4 after D2-D4.
- Evidence:
  - P1 scope (`:159`): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)". Section 3.1-3.2 includes the P2 and P4 commands.
  - AC-1.1 (`:195`) makes the P1 test assert the section for every one of those commands.
  - Section 6 intro (`:154`): "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4". The P4 commands' unattended behaviour is exactly what D2 (`:232-236`), D3 (`:238-242`), D4 (`:244-247`) decide.
  - D3 recommends (a), "no pr-submit changes in Phase 4" (`:240`), and section 4 (`:139`) makes `/sc:pr-submit` a worker candidate only if D3 is accepted. P1 as written still gives `pr-submit` the flag and the section.
  - WC-9 (`:67`) and the `auggie-review` row (`:100`): under `--unattended` the PR-posting default is off. In P1 the flag exists but (per the row's phase P2, `:100`) that behaviour does not yet, so a coordinator briefing `auggie-review --unattended` after P1 still posts to GitHub and waits on the remediation offer.
- Why blocking: two stated texts contradict (P1 scope and AC-1.1 against section 6's phase split and WC-2/WC-9), and the intermediate state they produce is the unsafe one the contract exists to prevent.
- Recommendation: narrow P1 and AC-1.1 to the commands whose section 3 row has phase P1 (plus the P1 fixes to ready commands); let each later phase add the flag and section together with its gate rows.
- Priority: High. Quality impact: about 0.5 of a Consistency point.

=== ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The central decision (Orca coordinates; commands stay units of work; section 1.3 rejects commands calling Orca) is supported by `CAPS:97-103`, `CAPS:145-150` and `INV-A:90`, and section 1.4 states the evidence gaps honestly (Phase 0 smoke runs close the main one).

## Follow-up candidates (Medium and minor; not in the Reviser brief)
Open an issue for these only if the user answers yes to the one question per loop (the session that runs this review asks it; this worker was told to reply with a path only, so the question is left to the coordinator and no issue was created).

Medium (concrete wrongness needs an assumption, or a requirement is never stated):
- M1 (MAJOR label, Medium, Wiegers/Fowler). WC-4 (`:62`) fixes the report at `<output-dir>/return-contract.yaml` with the directory "known before dispatch" (`:62`, `:73`), but the `workflow` row (`:92`) keeps `.dev/tasks/to-do/<id>/return-contract.yaml` (id generated at run time, no output flag in the brief) and asks for a contract on pre-creation STOPs (`:92`, AC-1.4 `:198`) without saying where it goes (no `<id>` yet). `troubleshoot` writes `return-contract.yaml` only with `--caller task-unified` (`INV-B:242`), while the spec lists `REPORT.md` as its report (`:91`). Each reading is plausible, so Medium.
- M2 (MAJOR label, Medium, Nygard/Fowler). WC-6 (`:64`) has a command "write each run into a fresh output directory" while WC-4 says the coordinator passes `<output-dir>` and the contract path is known before dispatch; WC-3 (`:61`) re-invokes the command after an answer. For the 20-odd "fresh dir" rows it is undefined whether the re-run uses the same dir (overwriting the blocked attempt's contract) or a new one (path no longer matches what the worker reports). No acceptance check exercises `--retry-of`, WC-3, WC-6 or WC-12 (section 7 has none), and WC-11 is exercised only for `save` (AC-3.4, `:207`).
- M3 (Medium, Cockburn/Nygard). WC-9 (`:67`) says outward defaults return "only through the command's own explicit flag", and D4(a) (`:245`) has the coordinator "pass the command's explicit flag". Such a flag is not named for `post-release` (row `:113`), `pr-submit` (`:114`), `task` commit/push (`:121`) and `auggie-review --post-pr` (`:100`), which `INV-A:38` does not list (only `--no-post-pr` exists). It is a new flag, not stated as one. AC-2.4 and AC-4.2 test only the "not authorized" case.
- M4 (Medium, Crispin). WC-10 (`:68`) requires a split only for calls longer than 5 minutes into waits of at most 4 minutes; AC-4.3 (`:210`) fails any single call over 240 s. A 270 s call passes WC-10 and fails AC-4.3. The 5-minute heartbeat leaves no margin for a wait of up to 5 minutes plus work.
- M5 (Medium, Whittaker/Nygard). WC-5 (`:63`) maps a missing report to `failed` but is silent on a report that exists and is malformed, empty, or has a `status` outside the four values. 7.2 step 4 (`:183`) rejects it as a test failure, not as a worker rule.
- M6 (Medium, Whittaker). `--unattended` combined with `--interactive` is refused for `cleanup`, `improve`, `roadmap` (`:103`, `:110`, `:118`) but for `adversarial`, `brainstorm`, `release-split` only the brief is told "never `--interactive`" (`:83`, `:84`, `:89`). The command-side rule for the combination is not stated.
- M7 (Medium, Fowler/Newman). `tasklist` row (`:122`) says reflect "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`". Worker, then a reflect subagent per phase, then reflect's own `root-cause-analyst` and (Tier 2) reviewers plus `sc:adversarial` agents is at least two layers below the worker's session, and `INV-B:209-210`, `INV-B:215` recommended dropping `--remediate` and running the reflect fan-out at top level; the spec instead passes `--unattended` so "the headless rule applies", which its own UNVERIFIED item 9 (`:280`) assumes does not hold for an Orca worker. The departure from the inventory's recommendation has no `## Decisions` entry.
- M8 (Medium, Hohpe). Gate resolution on a missing or unwritable `--output` directory under `--unattended` is unstated; WC-4 says "written on every outcome" but names no fallback location.
- M9 (Medium, Gregory/Nygard). WC-3 (`:61`) lets the worker `ask` and resume without a bound on repeats, and no heartbeat is sent while blocked; a coordinator that never replies leaves the worker waiting, which the spec itself notes is invisible (`:44`). The coordinator-side duty to poll `worker-show` is only in 7.2 (`:181`), not in section 2.3.
- M10 (Medium, Hightower). AC-C1 (`:172`) must print nothing for `src/superclaude/core`, while P0 (`:158`) adds a Orca section to `HOW-WE-WORK.md` and a coordinator brief template to `WORKER-CONTRACT.md` in that directory, and SA-2 (`:147`) allows Orca mentions in the contract file. The grep pattern only matches invocation forms, so the outcome depends on how the new text is worded.

Minor notes:
- E3 (`:23`) says "It has worked before" while section 1.4(1) (`:43`) says the evidence proves only the nested route; the weaker wording in 1.4 is the accurate one.
- Section 3.1 says ready commands run "now" with the stated flags (`:79`) while section 2.3 (`:73`) says every brief includes `--unattended`; P0 (`:158`, AC-0.4 `:194`) resolves it, but the sentence in 2.3 reads as unconditional.
- `.dev/orca-command-refactor/README.md:27` lists Task 5's output as `review/spec-panel.md`; this round writes `review/round1.md` as the brief directs.

## Guard Condition Boundary Table
Trigger: the spec contains conditional logic, numeric thresholds and sentinel values (`--unattended`, 60 s readiness, 5 min heartbeat, 4 min wait, depth 1, status vocabulary). Classes left out are given with a reason. Status "GAP" is graded by FR-8: a GAP that names a concrete wrong outcome or a safety-boundary risk is blocking, otherwise Medium (cross-referenced to the findings above).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` flag | WC-2, `:60` | Zero/Empty | flag absent | false | SA-1: behaviour unchanged (`:146`) | OK |
| `--unattended` flag | WC-2, `:60` | Typical | flag present, no gate hit | true | documented default or flag value | OK |
| `--unattended` flag | WC-2, `:60`; P1 `:159` | Legitimate Edge Case | flag present on a P2/P4 command before its phase | true | P1 says accept it (`:159`); WC-9 says outward defaults off; rows land later | GAP (F2, blocking) |
| `--unattended` + `--interactive` | `:83-84`, `:89` vs `:103`, `:110`, `:118` | Legitimate Edge Case | both flags | true | refused for 3 commands; for 3 others only the brief is told "never" | GAP (M6, Medium) |
| `<output-dir>` | WC-4, `:62` | Zero/Empty | not passed, or not writable | false | none stated | GAP (M8, Medium) |
| `<output-dir>` | WC-4, `:62` vs `:92` | Typical | passed | true | contract at `<output-dir>/return-contract.yaml`; `workflow` keeps `.dev/tasks/to-do/<id>/` | GAP (M1, Medium) |
| Report `status` | WC-5, `:63` | Zero/Empty | report file missing | n/a | `--outcome failed` | OK |
| Report `status` | WC-5, `:63` | Sentinel Value Match | `status` outside the four values, or file empty | n/a | none stated at the worker | GAP (M5, Medium) |
| Report `status` | WC-5, `:63` | Legitimate Edge Case | `partial`; audit verdict FAIL | n/a | `succeeded`; body states status/verdict | OK |
| Heartbeat / wait size | WC-10, `:68`; AC-4.3 `:210` | Maximum/Overflow | single call 4-5 min (e.g. 270 s) | WC-10 no split needed; AC-4.3 fails | conflicting limits | GAP (M4, Medium) |
| Heartbeat / wait size | WC-10, `:68` | Typical | waits at most 4 min | true | worker heartbeats between waits | OK |
| Readiness limit | WC-1, `:59` | Maximum/Overflow | prompt fallback above about 45 s | fails | "well inside the limit"; evidence says 30 s passes, over ~45 s fails (`:59`) | OK |
| Nesting depth | WC-8, `:66` | Maximum/Overflow | depth 1, command calls `worker-start` | refused | WC-8 forbids; `CAPS:97-101` | OK |
| `ask` wait | WC-3, `:61` | Maximum/Overflow | no reply, repeated timeouts | n/a | resume same ID; no bound | GAP (M9, Medium) |
| `/sc:load` report | AC-1.1, `:195` vs `:112`, `:265` | Zero/Empty | no report file by decision | n/a | AC-1.1 requires the contract name | GAP (F1, blocking) |
| Zero/One/Typical for `--deps`, counters | n/a | n/a | n/a | n/a | no counters or collections are specified in this document beyond phase counts, which reconcile (below) | left out: not applicable |

## Quantity Flow Diagram (Pipeline Dimensional Analysis, Fowler / Whittaker)
```text
[43 commands: INV-A 21 + INV-B 22]
   --> [classify] --> 10 ready (5+5) | 27 needs-change (13+14) | 6 coordinator-only (3+3)   (sum 43, matches :76)
   --> ready 10 --> phases: adversarial, cleanup-audit, index-repo, workflow (P1); reflect, release-split, tdd, troubleshoot (P2); brainstorm, init-lite (none)  = 10
   --> needs-change 27 --> P1 9 | P2 11 | P3 4 | P4 3 = 27
   --> consumers: AC-1.1 asserts a section for 37 commands (10 + 27)  <-- load (no contract) and P4 commands (deferred)  MISMATCH (F1, F2)
   --> section-4 test asserts 0 sections for 6 commands
```
No count is lost between the inventories, section 3, section 6 and section 4. The only mismatch is the consumer, AC-1.1, which assumes all 37 can carry a contract section in Phase 1.

## Whittaker attacks (reported only where a finding resulted)
- I can break this specification by **Sequence Attack**. The invariant at **section 6 P1 / AC-1.1 (`:159`, `:195`)** fails when **Phase 1 is finished and Phase 2 has not started**. Concrete attack: coordinator briefs `/sc:auggie-review <PR> --unattended --output d`; before P1 the flag is unknown, after P1 it is accepted and the section exists, but the PR-posting default is turned off only by the P2 row (`:100`); the review posts to the PR and the session then ends its turn on the remediation offer (`INV-A:62`) with no `worker_done`. (F2)
- I can break this specification by **Zero/Empty Attack**. The invariant at **AC-1.1 (`:195`)** fails when **the command has no report by design**. Concrete attack: add the load section without `return-contract.yaml`; the test asserts the name; it fails and the only way to pass is the "unrequested addition" the Decisions table rejects. (F1)
- I can break this specification by **Divergence Attack**. The invariant at **WC-10 versus AC-4.3 (`:68`, `:210`)** fails when **one tool call lasts 270 s**: compliant by the requirement, failing the acceptance check. (M4)

## Auto-suggestion
The spec introduces several numeric thresholds (60 s, 4 and 5 min, depth 1, 0.70) and phase-count pipelines; re-running with `--focus correctness` is recommended but advisory only.

## Reviser brief
Blocking finding ids: F1, F2.

Rules (restated from the command's Review Loop bullet 6, since the reviser reads this report, not the command):
- Revise only text a blocking finding names (F1: AC-1.1 and AC-1.2 coverage for `/sc:load`; F2: the P1 scope sentence at line 159 and AC-1.1's command set).
- Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id.
- Leave Medium findings (M1-M10) and minor notes alone; they do not fail the review and are not to be edited.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
