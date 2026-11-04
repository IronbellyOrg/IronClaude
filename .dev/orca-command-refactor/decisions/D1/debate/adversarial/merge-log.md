# Merge Execution Log

## Metadata
- Base: Variant 3 (option c)
- Executor: merge-executor agent
- Changes applied: 24 of 24
- Status: success (merge execution). Separately, the pipeline's return contract stays `status: partial` with all five HIGH invariants listed under `unaddressed_invariants`, as the plan's "Invariant Coverage" section requires; the merged text records them as accepted risks.
- Timestamp: 2026-11-02T18:19Z

## Changes Applied

Method: the merged output was filled section by section, in document order. Within each section the plan's changes were applied in plan order, and where a later change revises an earlier one (for example change 18 on change 9, change 22 on change 15), the later, revised text is the one kept. Each entry below is written when its change is applied; an entry still marked pending has not been applied yet. Keys are the plan's (`refactor-plan.md`, citation key).

### Change 1: Outward defaults turn off only under the flag
- **Status**: Applied
- **Source**: Variant 1, Safety (V1:10); U-002, C-002
- **Target**: Base, Safety (append)
- **Before**: The base did not state the WC-9 link.
- **After**: New Safety bullet: WC-9 (`SPEC:73`) applies only under `--unattended`, so a person in an Orca tab keeps auggie-review's posting default (`SPEC:169`).
- **Provenance tag**: `<!-- Source: Variant 1, Safety (V1:10), merged per Change #1 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 2: Phase gating stated explicitly
- **Status**: Applied
- **Source**: Variant 1, Reliability (V1:15); U-003, C-013
- **Target**: Base, Reliability (append)
- **Before**: Not stated.
- **After**: Two bullets: a command accepts the flag only once its gates are converted (`SPEC:187-195`), marked by its section, which AC-1.1 ties to the phase table (`SPEC:257`); hence the guard is inert in P0 and never refuses `/sc:load` (`SPEC:191`, `SPEC:197`, from change 9's rationale).
- **Provenance tag**: `<!-- Source: Variant 1, Reliability (V1:15), merged per Change #2; consequence for the guard from Change #9 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 3: Quoted-argument example and its live check
- **Status**: Applied
- **Source**: Variant 1, Safety (V1:8); C-001
- **Target**: Base, Safety (insert into the first bullet)
- **Before**: First Safety bullet stated SA-1 without the quoted-argument case.
- **After**: The first bullet is kept, followed by a bullet naming `/sc:troubleshoot "the worker ignores --unattended"` as a person's run, checked by AC-2.8 (`SPEC:55`, `SPEC:269`). Split into two bullets to keep one claim per bullet.
- **Provenance tag**: `<!-- Source: Base (original, modified): first bullet kept from V3:11; the quoted-argument example and its live check inserted per Change #3 (Variant 1, Safety, V1:8) -->`
- **Validation**: Structural integrity ✅ | References ✅ (`SPEC:55`, `SPEC:269` re-read) | Contradictions ✅

### Change 4: Honest wording that the parse and the guard are applied by a model
- **Status**: Applied
- **Source**: Variant 1, Implementation cost (V1:22); X-003
- **Target**: Base, Reliability first bullet (replace "Deterministic")
- **Before**: "Deterministic: a string check on the brief's command line, decided before anything runs."
- **After**: "The brief text can be checked by text tools; at run time both the command and the guard are a model applying a written rule." The base's "decided before anything runs" is kept as its own bullet, now true by change 20.
- **Provenance tag**: `<!-- Source: Base (original, modified): "Deterministic" replaced per Change #4 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (no remaining "deterministic" claim; grep in post-merge validation)

### Change 5: Named "Known weaknesses" section
- **Status**: Applied
- **Source**: Variant 1, "Known weakness" (V1:19); S-002
- **Target**: Base, new section after "How a person works day to day"
- **Before**: Section did not exist (V3 had no self-critique).
- **After**: "Known weaknesses (accepted risks)" with nine bullets: template-less brief (change 17); pre-conversion stalls (`invariant-probe.md:28`, INV-021); incomplete gate lists (INV-022); skill copies (change 18 (v)); command precedence UNVERIFIED (change 18 (i)); re-invocation dropping the token (change 23, INV-018, REVIEW M12); the two UNVERIFIED points of change 20; case 3's dependence on D3 (change 19); the five HIGH amendments being planned, not debated (plan, "Invariant Coverage").
- **Provenance tag**: `<!-- Source: Variant 1, "Known weakness" (V1:19), adapted per Change #5 ... -->`
- **Validation**: Structural integrity ✅ (placed between "How a person works day to day" and "Implementation cost", as planned) | References ✅ | Contradictions ✅

### Change 6: Guard trigger is Orca's role table
- **Status**: Applied
- **Source**: Variant 2, Strongest case (V2:8); U-004, C-010
- **Target**: Base, Position and "Why a third option" (now "Why this option")
- **Before**: The worker session was "the top-level agent that received Orca's preamble" (`SPEC:61`), and Orca's telling it so was cited as `[G]` lines 38, 78-82.
- **After**: Position defines the worker session as only a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs (`[G]` 38, 41; `CAPS:148`; `SPEC:53`). "Why this option" cites the role table (dispatched worker vs ordinary terminal agent) in place of `[G]` 78-82. The same trigger is restated in "What the guard checks and when" for INV-008 (change 23).
- **Provenance tag**: `<!-- Source: Base (original, modified): the identity citation `[G]` 78-82 is replaced by Orca's role table per Change #6 (conceded at R2-V3 #5) -->`; Position block tag lists Change #6.
- **Validation**: Structural integrity ✅ | References ✅ (`[G]` 38, 41 not re-run; carried via `CAPS:148`, which quotes them) | Contradictions ✅

### Change 7: Reflect's `claude --print` precedent supports an explicit switch
- **Status**: Applied
- **Source**: Variant 2, Reliability (V2:19); U-006, C-012
- **Target**: Base, "Why this option" (append after the (b) critique)
- **Before**: Not present.
- **After**: One bullet: the `claude --print` precedent is assumed not to fire for an Orca worker, marked UNVERIFIED with `SPEC:391` item 9 (REVIEW M2); either way a worker needs an explicit switch.
- **Provenance tag**: `<!-- Source: Variant 2, Reliability (V2:19), merged per Change #7 -->`
- **Validation**: Structural integrity ✅ | References ✅ (`SPEC:391` re-read: item 9, "assumed not") | Contradictions ✅

### Change 8: `ORCA_TERMINAL_HANDLE` marks any live Orca terminal
- **Status**: Applied
- **Source**: R2-V2 New evidence 2; `CAPS:149`, `CAPS:151`
- **Target**: Base, "Why this option" (replace the `worker-list` observation as the main reason)
- **Before**: The base's environment-route objection rested on the 2026-11-02 `worker-list` observation alone.
- **After**: The main reason is that the variable marks any live Orca terminal, stated as inferred from `CAPS:149` plus `CAPS:151`, with item 13 (`SPEC:395`) "not directly resolved" (REVIEW M3). The observation follows as "supporting observation only", attributed to V3:8.
- **Provenance tag**: `<!-- Source: Variant 2, Round 2 New evidence 2, merged per Change #8 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ (`CAPS:149`, `CAPS:151` re-read) | Contradictions ✅

### Change 9: Key the guard to the command's `## Unattended mode` section
- **Status**: Applied
- **Source**: R1-V3:16-21; X-005; INV-006
- **Target**: Base, Position (replace "if the command line in its Task has no standalone `--unattended`")
- **Before**: The guard refused every flagless brief (V3:3), including P0 smoke runs and `/sc:load` steps.
- **After**: Case 1 refuses only when every existing copy of the command file has an `## Unattended mode` section and the `Command:` line lacks the flag (Position; "What the guard checks and when", Order of the checks, step 4). A flagless line for an unsectioned command passes (step 6 there, citing `SPEC:191`, `SPEC:197`). The key is the copies actually present (change 18 wording supersedes the plan's earlier "copy actually loaded").
- **Provenance tag**: Position tag and `<!-- Source: Debate refinements (R1-V3:16-21; R2-V3 #11) and invariant probe INV-001, INV-005, merged per Changes #9, #10, #18, #19, #20 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (checked against change 18: both use "every existing copy")

### Change 10: Symmetric check
- **Status**: Applied
- **Source**: R2-V1:35 (New evidence 3); R2-V3 #11; INV-007
- **Target**: Base, Position (append guard case 2)
- **Before**: One-way check only.
- **After**: Case 2 refuses a flagged line when no existing copy has the section; its reason text is the change 18 (iii) text. The rationale (pre-P2 auggie-review would ignore the token and post) is placed in Safety.
- **Provenance tag**: Position tag; Order-of-checks tag (both name Change #10); Safety tag (see change 1 entry)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 11: Ship the guard in P1, not P0
- **Status**: Applied
- **Source**: R1-V3:21; R2-V3 New evidence 1
- **Target**: Base, Implementation cost (replace "one live check in P0 or P1")
- **Before**: "One sentence in the worker-session part of `WORKER-CONTRACT.md` plus one live check in P0 or P1."
- **After**: "The guard ships with P1, the first phase with flag-accepting commands (`SPEC:182`)." Position also says "from P1". The base's "Removing the guard later is a one-line change" is replaced by the plan's rollback list (C-007 row, REVIEW M4), which names every guard part.
- **Provenance tag**: `<!-- Source: Base (original, modified): "one live check in P0 or P1" replaced per Change #11; ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (no "P0 or P1" left)

### Change 12: Guard text travels in the brief template and in `WORKER-CONTRACT.md`
- **Status**: Applied
- **Source**: R2-V1 #5; R2-V2 critique 2; R2-V3 #3
- **Target**: Base, Reliability second bullet (replace "one rule in one file")
- **Before**: "it is one rule in one file (`WORKER-CONTRACT.md`, `SPEC:58`), not 35 command edits."
- **After**: Four bullets: the rule is model-read prose; it travels in the template guard line and in `WORKER-CONTRACT.md`; both are needed because nothing loads the contract file automatically (`SPEC:58` names only the install location; inference cited to R2-V3 #3, REVIEW M11); a template-less brief falls back to (a).
- **Provenance tag**: `<!-- Source: Base (original, modified): "one rule in one file" replaced per Change #12 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ ("not 35 command edits" dropped because change 22 adds command-side section edits; the guard itself still needs none, stated in Implementation cost)

### Change 13: Amend `SPEC:79`
- **Status**: Applied
- **Source**: R1-V1 A-005; R2-V1 #10; A-005
- **Target**: Base, new section "Spec wording changes"
- **Before**: Section did not exist.
- **After**: New "Spec wording changes" section (W1-W16). This change supplies W4 (`SPEC:79`: "including `--unattended` where the command accepts it at this phase") and W9 (`SPEC:329`: same qualifier; REVIEW M7). W1 (`SPEC:54` no longer open) and W11 (`SPEC:329-331`, recommendation now option (c) as amended) follow from it and the base position.
- **Provenance tag**: `<!-- Source: Change #13 (Round 1 and Round 2 debate, A-005) -->`; `<!-- Source: Change #13 (REVIEW M7) -->`
- **Validation**: Structural integrity ✅ | References ✅ (`SPEC:54`, `SPEC:79`, `SPEC:329-331` re-read) | Contradictions ✅

### Change 14: The flag crosses the Agent-tool boundary; the preamble does not
- **Status**: Applied
- **Source**: R2-V1:33 (New evidence 1); R2-V2 New evidence 1; `SPEC:71`, `SPEC:145`
- **Target**: Base, "Why this option" (append, as a further reason against (b))
- **Before**: Not present.
- **After**: One bullet: a command's own subagents get the command line, never the preamble, so detection inside commands could not reach nested fan-out while the token can.
- **Provenance tag**: `<!-- Source: Round 2 debate (R2-V1:33, New evidence 1; R2-V2 New evidence 1), merged per Change #14 -->`
- **Validation**: Structural integrity ✅ | References ✅ (`SPEC:71` and `SPEC:145` re-read; the "preamble does not cross" half rests on the R2 rounds, as in the plan) | Contradictions ✅

### Change 15: Guard scope is the Task's own command line
- **Status**: Applied (as revised: superseded for nested commands by change 22, per the plan)
- **Source**: R2-V3 New evidence 2; INV-014
- **Target**: Base, new section "What the guard checks and when"
- **Before**: Section did not exist.
- **After**: Merged with change 21 into the "Scope" subsection: the guard checks only the brief's own `Command:` lines; nested commands (Skill tool or Agent tool) are never checked and are governed by the propagation rule. The phrase "relies on AC-2.1" is not carried, because change 22 supersedes it (REVIEW M13).
- **Provenance tag**: `<!-- Source: Invariant probe INV-016, INV-009, INV-013, merged per Changes #21 and #23; Change #15 (R2-V3 New evidence 2, INV-014) merged here and superseded for nested commands by Change #22 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 16: Checks for the guard
- **Status**: Applied (merged-position part here; spec section 7.3 text under Spec wording changes, recorded in this entry when written)
- **Source**: R2-V3 New evidence 1; R2-V3:86-89
- **Target**: Base, Reliability (replace the one-run test)
- **Before**: "Testable live with one extra 7.2 run whose brief omits the flag (pass: `worker_done --outcome failed`, no contract written, no `agentWait`)."
- **After**: A "Checks" subsection: static assertion in `test_worker_contract.py`; AC-1.2 for false refusals; one P1 live run per refusal case (1, 2, 3) with AC-1.5's pass conditions (change 23, INV-010); case 3 with `/sc:help` (REVIEW M5); the discriminating P2 bare-topic tdd run (meaning taken from R2-V3 New evidence 1: flag omitted, otherwise stalls on tdd's gate); the AC-1.3 coordinator-session manual run (change 23); P2 nested-invocation assertions (change 22); 7.2 step 1 copy confirmation (change 18 (iv)).
- **Provenance tag**: `<!-- Source: Base (original, modified): the base's one-run test replaced per Change #16 ..., extended per Changes #18, #20, #22, #23 ... -->`
- **Spec part (written later)**: W15 gives the section 7.3 and 7.4 text: AC-1.1 extension (static assertion), AC-1.3 extension (coordinator-session manual run), new AC-1.7 (one P1 run per refusal case, case 3 with `/sc:help`), AC-2.1 extension (P2 nested-invocation assertions), new AC-2.9 (the P2 bare-topic tdd run), two traceability rows. New IDs AC-1.7 and AC-2.9 were chosen because they are unused in the spec (AC-2.7 is also unused; AC-2.9 avoids any reading as a renumbering).
- **Validation**: Structural integrity ✅ | References ✅ (`SPEC:257-269` re-read) | Contradictions ✅

### Change 17: A brief written without the template falls back to (a)
- **Status**: Applied
- **Source**: R2-V3 #3; INV-019
- **Target**: Base, Known weaknesses (change 5)
- **Before**: Not present.
- **After**: First Known-weaknesses bullet: the guard catches "template used, flag wrong", never "no template". Cross-referenced from Reliability (change 12).
- **Provenance tag**: Known-weaknesses section tag (names Change #17)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 18: The guard reads the command file that will actually be loaded (INV-001)
- **Status**: Applied (as revised for REVIEW B1)
- **Source**: INV-001; R2-V3 #7; K1 and K4 (`CR01:24`, `CR01:42`)
- **Target**: Base, "What the guard checks and when"; Known weaknesses; Spec wording changes (7.2)
- **Before**: The base checked only "the command line in its Task", with no command file read.
- **After**: (i) "Order of the checks" step 2 and "Why every copy": the guard reads every existing copy (project worktree copy and `~/.claude`); precedence marked UNVERIFIED with `ROOT-CLAUDE:88`; cases 1 and 2 only when all copies agree. (ii) Disagreement refusal with the plan's reason text (Position and step 3). (iii) Case 2 reason names both causes (step 5). (iv) Interactions K1: `make sync-dev` inside the worktree, `~/.claude` never reinstalled, `--setup run` performing it UNVERIFIED (`CR01:42`); Reliability "Copies" bullet and W14 step 1: 7.2 confirms the section in every existing copy. (v) Known weaknesses: skill copies can skew and are not checked.
- **Provenance tag**: `<!-- Source: Invariant probe INV-001, merged per Change #18 (revised for REVIEW B1) -->` and the Order-of-checks, Known-weaknesses, Interactions and W14 tags naming Change #18
- **Validation**: Structural integrity ✅ | References ✅ (`ROOT-CLAUDE:88` re-read: "skills read `~/.claude/skills/` first, then `.claude/skills/`"; `CR01:24`, `CR01:42` re-read) | Contradictions ✅

### Change 19: pr-submit is refused while D3 is (a) (INV-005)
- **Status**: Applied
- **Source**: INV-005; `SPEC:162`, `SPEC:197`, `SPEC:341`
- **Target**: Base, Position (guard case 3) and Safety
- **Before**: The base refused only the six coordinator-only commands (V3:3, V3:13).
- **After**: Position case 3 names a never-as-worker list in `WORKER-CONTRACT.md` (six section 4 commands plus `/sc:pr-submit` while D3 keeps it off workers). Safety gains the reason (pr-submit is unlisted and unsectioned under D3 (a), so a flagless brief would pass cases 1 and 2 and run attended with outward defaults on). Interactions, D3 subsection, carries "if D3 adds a worker route, D3 must say how it passes the guard". Known weaknesses notes the dependence on D3's final text.
- **Provenance tag**: Position tag; `<!-- Source: Base (original, modified): V3:13 kept and extended with pr-submit per Change #19 (INV-005) -->`; `<!-- Source: Invariant probe INV-005, merged per Change #19; D3 interaction per Change #24 (REVIEW M8) -->`
- **Validation**: Structural integrity ✅ | References ✅ (`SPEC:162`, `SPEC:197`, `SPEC:341` re-read) | Contradictions ✅

### Change 20: The guard runs on the brief before the command is invoked (INV-015)
- **Status**: Applied (guard text here; spec layout edits under Spec wording changes, see the change 24 and change 16 entries for the 7.2 and 7.3 parts)
- **Source**: INV-015; `CORE-CLAUDE:74`
- **Target**: Base, "What the guard checks and when"
- **Before**: The base checked "the brief before running it" with no order relative to the skill-first rule; R2-V3 #7 had moved the check to after the command loaded.
- **After**: "When it runs" subsection: the guard is part of reading the Task; template puts the guard line before the `Command:` lines so the Task text never starts with `/sc:`; case 3 by name only, cases 1 and 2 by a plain file read ("Order of the checks", steps 1-2). Both UNVERIFIED points carried exactly as the plan marks them (Task text could start with the command; mid-brief `Command:` invocation counts as direct top-level run, settled by AC-0.4 step 5). The case-3 live run confirming no side effects is in "Reliability and checks". The spec example-brief rewrites (`SPEC:90`, `SPEC:93`, AC-2.2, AC-2.6) are in Spec wording changes (REVIEW M6).
- **Provenance tag**: `<!-- Source: Invariant probe INV-015, merged per Change #20 (supersedes R2-V3 #7's "no separate file read") -->`
- **Validation**: Structural integrity ✅ | References ✅ (`CORE-CLAUDE:74` re-read: "before any other output. That step is blocking") | Contradictions ✅

### Change 21: Scope is the brief's `Command:` line only (INV-016)
- **Status**: Applied
- **Source**: INV-016; `WF:58`; R2-V3:33
- **Target**: Base, "What the guard checks and when"
- **Before**: Section did not exist; scope of "each top-level command" undefined for in-session Skill nesting.
- **After**: "Scope" subsection: one labelled `Command:` line per command; all checked once before any runs, so a refusal means nothing ran (closes INV-013, REVIEW M14); nested commands through the Skill tool or Agent tool never checked, with the workflow-reflect example (`WF:58`, `SPEC:193`).
- **Provenance tag**: Scope subsection tag (names Changes #21 and #23)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (consistent with case 1: the nested reflect load is not a `Command:` line)

### Change 22: `--unattended` propagates to nested commands, or the nested step is gate-free (INV-020)
- **Status**: Applied (as revised for REVIEW B2)
- **Source**: INV-020; `BS:185`; `SPEC:139`, `SPEC:145`
- **Target**: Base, new paragraph in "What the guard checks and when"; Spec wording changes (section 2.1 contract file rules)
- **Before**: Not present; only the tasklist row propagated the flag.
- **After**: "Nested commands: propagation rule" subsection with every element of the plan's integration point: Skill and Agent routes; flag only where accepted at this phase; nested report directory `<caller report-dir>/nested/<command>-<n>/` with the WC-4/WC-11 reasons; nested contract in `artifacts`, top-level contract drives WC-5; gate-free-or-skip-and-record fallback; sections name nested invocations; AC-2.1-style assertions; workflow-reflect and brainstorm-research cases with phases; brainstorm enrichment off until P2; workflow's reflect step gate-free; P2 edits for both callers although not in `SPEC:183`; "never stalls" only for converted gates. Spec side: W2, W3 (rule text), W15 (AC-1.1, AC-2.1 assertions), W16 (P2 row and the two section 3.1 rows).
- **Provenance tag**: `<!-- Source: Invariant probe INV-020, merged per Change #22 (revised for REVIEW B2); supersedes Change #15's "relies on AC-2.1" for nested commands (REVIEW M13) -->`; W16 tag
- **Validation**: Structural integrity ✅ | References ✅ (`SPEC:57`, `SPEC:68`, `SPEC:75`, `SPEC:139`, `SPEC:145`, `SPEC:183`, `SPEC:193` re-read; `WF:58`, `BS:179`, `BS:185` carried from the plan review's re-read) | Contradictions: see post-merge note on the tasklist row (`SPEC:145`)

### Change 23: MEDIUM invariants bundle (INV-002, 008, 009, 010, 017, 018, 022, 023)
- **Status**: Applied
- **Source**: `invariant-probe.md:35`, `:41-44`, `:50-51`, `:55-56`
- **Target**: Base, "What the guard checks and when", Checks, Known weaknesses, Spec wording changes
- **Before**: None of the eight items was addressed in the base.
- **After**:
  - INV-008, INV-023: "Who applies it" subsection (live preamble with Task and Dispatch IDs only); AC-1.3 coordinator-session manual run in Checks and W15.
  - INV-009: Scope subsection, labelled `Command:` lines only, so the guard's own wording cannot count as the flag; W3.
  - INV-018: Scope subsection (checked once; re-invoked line keeps every token); Known weakness for a dropped token (REVIEW M12); W3, W5.
  - INV-002: "How the coordinator decides on the flag" subsection, run on the worker's copies (REVIEW M9); W5.
  - INV-010: one P1 live run per case 1, 2, 3 with AC-1.5's pass conditions; case 3 with `/sc:help` (REVIEW M5); Checks and W15 (AC-1.7).
  - INV-017: "How a person works day to day" and W6: `guard refused:` body with no contract; at most 2 brief fixes (3 attempts), third refusal escalates (REVIEW M1).
  - INV-022: Known weakness (incomplete gate list, caught only by 7.2 steps 2-3).
- **Provenance tag**: tags naming Change #23 in "Who applies it", Scope, "How the coordinator decides", Checks, "How a person works day to day", Known weaknesses, W3, W5, W6, W15
- **Validation**: Structural integrity ✅ | References ✅ (`invariant-probe.md` rows re-read; `SPEC:261` re-read) | Contradictions ✅

### Change 24: Fixed user constraints K1-K4
- **Status**: Applied (K1 as revised for REVIEW B3; K4 as revised for REVIEW M8)
- **Source**: K1-K4 in the plan Overview
- **Target**: Base, Spec wording changes and a new "Interactions" section
- **Before**: Section did not exist; the base was silent on worktree placement and on the 2-cycle cap.
- **After**: "Interactions with other decisions and fixed constraints" with K1 (Orca-created worktree at the default path; phase edits committed to a branch with the user's authorization; `--base-branch`; `make sync-dev`; `orca worktree rm`), K2 (no GitHub interaction), K3 (2-fix cap; `/sc:implement` QA unchanged), K4 (per-session guard; CR-01 child setup), and a D3 subsection (T3 for the coordinator's or person's run; the D3 (c) handoff tab has no preamble). Spec side: W14 (`SPEC:235-236`). "How a person works day to day" names the per-phase commit decision.
- **Provenance tag**: `<!-- Source: Refactor plan fixed constraints K1-K4, merged per Change #24 ... -->`; W14 tag
- **Validation**: Structural integrity ✅ | References ✅ (`CR01:19`, `CR01:22-24`, `CR01:41-45`, `CR01:51`, `ROOT-CLAUDE:37`, D3 transcript line 665 re-read) | Contradictions: one sequencing gap found and closed, see post-merge validation

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: ✅ One H1; 11 H2 sections in the order the brief requires (Position; Citation key; Why this option; What the guard checks and when; Safety; Reliability and checks; How a person works day to day; Known weaknesses (accepted risks); Implementation cost; Interactions with other decisions and fixed constraints; Spec wording changes); every H3 sits under an H2; no level is skipped. No `<!-- TODO -->` remains.
- Section ordering: ✅ "Known weaknesses" follows "How a person works day to day", as change 5 specifies; the new sections "What the guard checks and when", "Interactions ..." and "Spec wording changes" sit where the brief's heading list puts them.
- Document flow: ✅ Position states the whole rule (switch, trigger, `Command:` lines, four refusal conditions, `guard refused:` body, 2-fix cap) and points to the detail section. Provenance header follows Section 6; 47 `<!-- Source: ... -->` tags, one per section or significant block. No em dashes or en dashes in either file (grep count 0).

### Internal References
- Total references: 102 (22 guard-case references, 28 check-ID references, 5 UNVERIFIED-item references, 19 references to sections or subsections of the merged text or to new spec terms, 28 spec section-number references). Provenance tags were excluded from the count.
- Resolved: 102. Cases 1, 2 and 3 are defined in Position and "Order of the checks"; the copies-disagree refusal is named, never numbered, so no "case 4" reference exists. Check IDs resolve to existing spec rows (AC-0.4, AC-1.1, AC-1.2, AC-1.3, AC-1.5, AC-1.6, AC-2.1, AC-2.2, AC-2.6, AC-2.8) or to rows the merged text defines in W15 (AC-1.7, AC-2.9; both unused in the spec). Items 9 and 13 exist in the spec (`SPEC:391`, `SPEC:395`); item 27 is defined in W13. Spec sections 2.1, 2.3, 3, 4, 6, 7.2 and 9 exist. "Brief guard", "Brief layout" and the nested propagation rule are defined in W3 and W5 before W6-W16 use them. No "change N" text appears outside provenance tags.
- Broken: 0.

### Contradiction Re-Scan
- New contradictions introduced: 0 remaining. One was found during the re-scan and fixed in place before this result was recorded (below).
- Details:
  - Found and fixed: a Safety bullet said a refused coordinator-only command "has no chance to act first", which contradicted the UNVERIFIED point (from change 20) that Orca's Task text might still start with the command. The bullet now says the claim holds only if the Task text does not start with the command (UNVERIFIED) and that the case-3 live run checks for side effects, matching the plan's change 20 wording.
  - Sequencing gap in the plan's K1 text, closed with one clarifying sentence: the plan allows `worker-start --worktree new-top-level` and also says the coordinator runs `make sync-dev` "before dispatch" when setup does not; `worker-start` sends the task once the agent is ready (`CAPS:46-47`), so those two cannot both hold. The merged text (Interactions, K1; W14 step 1) says to create the worktree first with `orca worktree create` in that case. This adds no new rule; it orders the two routes the plan already names. Flagged here because it is executor wording, not plan text.
  - Against K1: ✅ no worktree is placed under `.dev/worktrees/`; W14 replaces `SPEC:235`'s wording; the commit before 7.2 needs the user's authorization. Against K2: ✅ no step talks to GitHub or upstream. Against K3: ✅ "at most 2 brief fixes (3 attempts), third refusal escalates" appears identically in Position, "How a person works day to day", K3 and W6. Against K4: ✅ the guard is per session; child setup is the same step as the all-copies rule.
  - Self-consistency checks: "every existing copy" is used identically in Position, "Order of the checks", W3, W11 and W14; the never-as-worker list is identical in Position, Safety, W3 and the D3 subsection; "checked once, before the first run" agrees between Scope, Known weaknesses and W3; no "Deterministic", "P0 or P1" or "one-line change" claim survives.
  - Observation, not a contradiction: the tasklist row (`SPEC:145`) already passes `--unattended` to nested reflect. Under the new propagation rule (W3) each nested invocation also needs its own report directory; reflect's own `--output <dir>` is directory-valued, so it can serve (`SPEC:57`, `SPEC:111`), and the AC-2.1 extension in W15 asserts it for every section that names a nested invocation. The plan does not list a `SPEC:145` wording change, so none was added; the P2 tasklist plan should confirm it.
  - Observation, not a contradiction: the copies-disagree refusal has no dedicated live run; the plan specifies live runs for cases 1, 2 and 3 only, and 7.2 step 1 deliberately removes the disagreement before each run.

## Summary
- Total changes planned: 24
- Successfully applied: 24
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS (structure ✅; references 102/102 resolved; 0 contradictions remaining after one in-place fix; one executor clarification and two observations recorded above for the orchestrator)
