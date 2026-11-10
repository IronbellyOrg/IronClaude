# ab1 tables (n=6)

Outcome: **INCONCLUSIVE** (no DROP and not a clear ADOPT); R_LOOP 1.221598754613771 (decides, limit 2.69), R_B 0.8989386393498083 (reported only)

Baseline: B_BLK 1.50, B_AUDFAIL 0.917, B_THEME 0.833 over 12 audits; 

## Sonnet stratum

| run | loop end | rounds / agents | growth | LOOP | AUD tokens | audit 1 | audit 2 |
|---|---|---|---|---|---|---|---|
| b1-r1 | PASS | 3 / 5 | +2.91% | 107044 | [18986, 19002] | FAIL R-1:T3 | FAIL F-1:T3 |
| b1-r2 | PASS | 3 / 5 | +1.59% | 130434 | [24650, 34332] | FAIL F-1:T2 | PASS  |
| b1-r3 | PASS | 2 / 4 | +1.68% | 128029 | [22078, 33494] | FAIL F-1:T3 | PASS  |
| b1-r4 | PASS | 2 / 4 | +0.82% | 105325 | [38062, 24743] | FAIL F-01:T1 | PASS  |
| b1-r5 | PASS | 2 / 4 | +1.43% | 118530 | [46127, 45374] | FAIL B-1:T3 | FAIL F-01:T1 |
| b1-r6 | PASS | 3 / 5 | +1.12% | 146705 | [28078, 22494] | FAIL R-1:T2 | FAIL B-1:T2,B-2:T2 |

## Metrics (pooled over completed audits; replicas below)

- n_completed: 6
- n_audits: 12
- BLK_T: 0.8333333333333334
- audit_fail: 9
- theme_rate: 9
- theme_counts: {'T1': 2, 'T2': 3, 'T3': 4, 'other': 0}
- loop_pass: 6
- growth: 0.01590118241781071
- LOOP_T: 122677.83333333333
- TOK_T: 152341.3333333333
- R_LOOP: 1.221598754613771
- R_B: 0.8989386393498083
- REJ1: 6
- N1: 33
- REJ1_rate: 0.18181818181818182
- replica audit 1 only: INCONCLUSIVE (BLK_T 1.0, no DROP and not a clear ADOPT)
- replica audit 2 only: INCONCLUSIVE (BLK_T 0.6666666666666666, no DROP and not a clear ADOPT)

## Haiku stratum (never pooled)

{
 "state": "pending"
}

## Design-specific tables (Sonnet)

### Per-theme capture across the reviewers (pooled first-review samples)

| theme | captured / samples | baseline k=1 |
|---|---|---|
| T1 | 15/18 | 6/6 |
| T2 | 13/18 | 2/6 |
| T3 | 4/18 | 3/6 |

| run | a | b | c | union |
|---|---|---|---|---|
| b1-r1 | FAIL 2 T1,T2 | FAIL 1 T1 | FAIL 2 T2 | T1,T2 |
| b1-r2 | FAIL 2 T1,T2 | FAIL 2 T1,T2 | FAIL 2 T1,T2 | T1,T2 |
| b1-r3 | FAIL 4 T1,T2 | FAIL 2 T1,T2 | FAIL 2 T1,T2 | T1,T2 |
| b1-r4 | FAIL 2 T1,T3 | FAIL 3 T1,T2 | FAIL 2 T1,T3 | T1,T2,T3 |
| b1-r5 | FAIL 2 T1,T2 | FAIL 2 - | FAIL 3 T1,T2 | T1,T2 |
| b1-r6 | FAIL 3 T2,T3 | FAIL 2 T1,T3 | FAIL 3 T1,T2 | T1,T2,T3 |

k=1 capture 0.78; k=2 capture 0.98; k=3 capture 1.00; pairs whose third reviewer adds a theme: 1 (k=2 would likely suffice)

### Merged-finding count

| run | raw | merged | dedup ratio |
|---|---|---|---|
| b1-r1 | 5 | 5 | 1.00 |
| b1-r2 | 6 | 5 | 0.83 |
| b1-r3 | 8 | 5 | 0.62 |
| b1-r4 | 7 | 5 | 0.71 |
| b1-r5 | 7 | 7 | 1.00 |
| b1-r6 | 8 | 6 | 0.75 |

### Verifier

| run | step | sent | confirmed | rejected | parse_ok |
|---|---|---|---|---|---|
| b1-r1 | VF1 | 5 | 5 | 0 | True |
| b1-r1 | VF2 | 1 | 1 | 0 | True |
| b1-r2 | VF1 | 5 | 5 | 0 | True |
| b1-r2 | VF2 | 1 | 1 | 0 | True |
| b1-r3 | VF1 | 5 | 4 | 1 | True |
| b1-r4 | VF1 | 5 | 3 | 2 | True |
| b1-r5 | VF1 | 7 | 5 | 2 | True |
| b1-r6 | VF1 | 6 | 5 | 1 | True |
| b1-r6 | VF2 | 2 | 2 | 0 | True |

pooled rejection rate over all VF steps: 6/37

### Noted, unactioned vs audits

| run | step | id | theme | verifier reason | matched audit blocker | eyeball |
|---|---|---|---|---|---|---|
| b1-r3 | VF1 | M4 | T1 | AC-1.1 only requires the section to name `return-contract.yaml`; a load section  | none | (eyeball) |
| b1-r4 | VF1 | M1 | T1 | A section that names the contract can say load writes none, so AC-1.1 does not f | AUD/F-01 | (eyeball) |
| b1-r4 | VF1 | M4 | T1 | The claimed outcome (auggie-review or post-release still posts or installs after | AUD/F-01 | (eyeball) |
| b1-r4 | VF1 | M5 | T1 | The claimed outcome (auggie-review or post-release still posts or installs after | AUD/F-01 | (eyeball) |
| b1-r4 | VF1 | M1 | T1 | A section that names the contract can say load writes none, so AC-1.1 does not f | AUD/F-01 | (eyeball) |
| b1-r4 | VF1 | M4 | T1 | The claimed outcome (auggie-review or post-release still posts or installs after | AUD/F-01 | (eyeball) |
| b1-r5 | VF1 | M3 | other | The finding states no text and no wrong outcome, so there is nothing to check. | none | (eyeball) |
| b1-r5 | VF1 | M7 | T1 | P1's Commands column lists only non-P4 commands and the spec says the flag is "a | AUD2/F-01 | (eyeball) |
| b1-r6 | VF1 | M3 | other | The text does not say a resumed run re-stops at the same gate or that no approva | none | (eyeball) |

## Theme tags to eyeball

- b1-r1 AUD R-1 T3 :: ### R-1 (blocking) AC-0.4 cannot pass as written; it gates every later phase
- b1-r1 AUD2 F-1 T3 :: ### F-1 (blocking, MAJOR, Wiegers/Adzic): the P0 acceptance check cannot pass as written
- b1-r1 R1a B1 T2 :: ### B1. CRITICAL (blocking). WC-4 fixes one contract location that the spec's own per-command rows c
- b1-r1 R1a B2 T1 :: ### B2. CRITICAL (blocking). Phase 1 and its acceptance check demand work that other parts of the sp
- b1-r1 R1b F1 T1 :: ### F1 - CRITICAL-by-consequence, BLOCKING: AC-1.1 and the P1 sweep contradict the `/sc:load` row an
- b1-r1 R1c B1 other :: ### B1 (CRITICAL by label, blocking by consequence). WC-3 lets a blocked gate be answered by `ask`; 
- b1-r1 R1c B2 T2 :: ### B2 (CRITICAL by label, blocking by consequence). WC-4 puts the report at `<output-dir>/return-co
- b1-r2 AUD F-1 T2 :: ### F-1 BLOCKING (MAJOR): the default contract location for a file-valued `--output` makes parallel 
- b1-r2 R1a B1 T2 :: ### B1. CRITICAL (blocking). The contract file location is stated three incompatible ways, and the a
- b1-r2 R1a B2 T1 :: ### B2. CRITICAL (blocking). AC-1.1 cannot pass for `/sc:load`, because P1 gives load only a usage-l
- b1-r2 R1b B1 T2 :: **B1 (MAJOR, blocking). WC-4 fixes the report path as `<output-dir>/return-contract.yaml`, "known be
- b1-r2 R1b B2 T1 :: **B2 (MAJOR, blocking). AC-1.1 requires every command in sections 3.1-3.2 to name `return-contract.y
- b1-r2 R1c B1 T1 :: ### B1: the P1 acceptance test requires an `## Unattended mode` section naming `return-contract.yaml
- b1-r2 R1c B2 T2 :: ### B2: WC-4 and section 2.3 say the report is `<output-dir>/return-contract.yaml`, known before dis
- b1-r3 AUD F-1 T3 :: ### F-1 [MAJOR, blocking] The P0 acceptance check cannot pass as written
- b1-r3 R1a B1 T1 :: ### B1 (MAJOR, blocking, Fowler / Wiegers): Phase 1 ships `--unattended` on every command, while the
- b1-r3 R1a B2 T2 :: ### B2 (MAJOR, blocking, Wiegers / Adzic): WC-4 puts the contract in an "output directory" but the t
- b1-r3 R1a B3 T2 :: ### B3 (MAJOR, blocking, Cockburn / Wiegers): workflow and adversarial contract paths contradict the
- b1-r3 R1a B4 T1 :: ### B4 (MAJOR, blocking, Wiegers / Adzic): AC-1.1 requires a contract-naming section in `/sc:load`, 
- b1-r3 R1b F1 T1 :: ### F1 - BLOCKING - `/sc:load` cannot satisfy both AC-1.1 and its own row
- b1-r3 R1b F2 T2 :: ### F2 - BLOCKING - Two different contract paths for the same command (adversarial, workflow) agains
- b1-r3 R1c B1 T2 :: ### B1. CRITICAL (blocking): WC-4's contract path is contradicted by the rows that apply it
- b1-r3 R1c B2 T1 :: ### B2. CRITICAL (blocking): AC-1.1 requires Phase 1 to finish text that Phase 4 is stated to wait f
- b1-r4 AUD F-01 T1 :: ### F-01 (blocking): AC-1.1 requires a contract section on three P1 commands whose own rows say they
- b1-r4 R1a F1 T1 :: ### F1 (blocking, Wiegers / Adzic): AC-1.1 requires a contract-naming `## Unattended mode` section o
- b1-r4 R1a F2 T3 :: ### F2 (blocking, Adzic / Wiegers): AC-0.4 step 3 cannot pass in P0 for the commands it names
- b1-r4 R1b B1 T1 :: ### B1 (CRITICAL, blocking): `/sc:load` is both given no report and required to have one
- b1-r4 R1b B2 T2 :: ### B2 (CRITICAL, blocking): the single report path rule cannot be met by commands whose `--output` 
- b1-r4 R1b B3 T1 :: ### B3 (CRITICAL, blocking): P1 makes `--unattended` accepted by every command, including those whos
- b1-r4 R1c F1 T1 :: ### F1 (blocking) - Wiegers, Cockburn - AC-1.1 contradicts D3(a), the P4 deferral and "Phases 1-3 ne
- b1-r4 R1c F2 T3 :: ### F2 (blocking) - Adzic, Crispin - AC-0.4 cannot pass as written
- b1-r5 AUD B-1 T3 :: ### B-1 [MAJOR, blocking] AC-0.4 requires a WC-4 contract path that no P0 smoke command can produce
- b1-r5 AUD2 F-01 T1 :: ### F-01 (blocking, MAJOR) Phase 1 scope states two different sets of commands, and AC-1.1 cannot pa
- b1-r5 R1a F1 T1 :: ### F1. CRITICAL-in-effect, blocking: AC-1.1 cannot pass for `load`, `brainstorm` and `init-lite` as
- b1-r5 R1a F2 T2 :: ### F2. CRITICAL-in-effect, blocking: the `/sc:adversarial` contract path in section 3.1 contradicts
- b1-r5 R1b F1 other :: ### F1 - CRITICAL (blocking) - Wiegers, Adzic, Cockburn
- b1-r5 R1b F2 other :: ### F2 - MAJOR graded blocking - Fowler, Nygard, Whittaker
- b1-r5 R1c B1 T2 :: **B1. WC-4 puts the contract file in a directory the brief cannot name for several commands (CRITICA
- b1-r5 R1c B2 T1 :: **B2. AC-1.1 cannot pass for `/sc:load` as the spec itself specifies it (CRITICAL, High)**
- b1-r5 R1c B3 T1 :: **B3. P1 and AC-1.1 require unattended sections for the P4 commands, which depend on decisions P1 is
- b1-r6 AUD R-1 T2 :: ### R-1 [MAJOR, blocking] Phase scope and acceptance checks disagree on which ready commands get the
- b1-r6 AUD2 B-1 T2 :: ### B-1 [MAJOR, blocking] WC-4 contract is required for every unattended outcome, but no phase adds 
- b1-r6 AUD2 B-2 T2 :: ### B-2 [MAJOR, blocking] Workflow's success contract location contradicts the WC-4 path that AC-1.2
- b1-r6 R1a F1 T2 :: ### F1 - CRITICAL (blocking) - Wiegers - load: acceptance check and phase scope contradict the load 
- b1-r6 R1a F2 T3 :: ### F2 - CRITICAL (blocking) - Crispin/Wiegers - AC-0.4 requires a step-3 condition that Phase 0 can
- b1-r6 R1a F3 other :: ### F3 - CRITICAL (blocking) - Adzic - cli-portify: the happy-path check cannot pass, because every 
- b1-r6 R1b B1 T3 :: ### B1 (CRITICAL; Wiegers, Adzic, Whittaker) Phase 0 acceptance check AC-0.4 cannot pass as written
- b1-r6 R1b B2 T1 :: ### B2 (MAJOR; Wiegers, Fowler) `/sc:load`: the per-command table and the P1 acceptance check contra
- b1-r6 R1c F1 T1 :: ### F1. BLOCKING (CRITICAL). `/sc:load` is required to carry a contract section by AC-1.1 and is als
- b1-r6 R1c F2 T1 :: ### F2. BLOCKING (CRITICAL). AC-1.1 at Phase 1 requires contract sections whose content waits on dec
- b1-r6 R1c F3 T2 :: ### F3. BLOCKING (CRITICAL). WC-4's contract path cannot be known before dispatch for workflow, rese
- b1h-r1 AUD B-1 T1 :: ### B-1 CRITICAL (blocking) [Wiegers, Whittaker (sequence attack), Fowler]: Phase 1 ships `--unatten
- b1h-r1 AUD B-2 T3 :: ### B-2 MAJOR (blocking) [Nygard, Crispin lens, Fowler]: the live worker check cannot pass for workf
- b1h-r1 AUD2 F1 T1 :: ### F1. CRITICAL-to-blocking (graded MAJOR, blocking): acceptance check AC-1.1 cannot pass at the en
- b1h-r1 R1a B1 T2 :: ### B1. Contract directory is undefined for file-valued or fixed-path commands (requirements, WC-4)
- b1h-r1 R1a B2 T3 :: ### B2. AC-0.4 step 4 cannot pass for the P0 smoke commands (acceptance)
- b1h-r1 R1a B3 T1 :: ### B3. Section 3.1 says ready commands change only in one column, which contradicts P1 and AC-1.1 (
- b1h-r1 R1a B4 T3 :: ### B4. AC-C1 matches nothing as written, and it cannot pass P0 as scoped (acceptance, SA-2)
- b1h-r1 R1b B1 T2 :: **B1. The contract path rule is contradicted, and the workflow path is not known before dispatch.** 
- b1h-r1 R1b B2 other :: **B2. WC-3 lets a coordinator's answer resume a command past a safety gate.** (Wiegers lead; Whittak
- b1h-r1 R1b B3 T3 :: **B3. The P0 acceptance run cannot pass as written.** (Adzic; Wiegers)
- b1h-r1 R1b B4 other :: **B4. Step 6 cannot pass for edit-in-place commands, including their P2 happy path.** (Wiegers; Cock
- b1h-r1 R1b B5 T3 :: **B5. AC-C1 forbids the Orca mention that SA-2 permits, and P0 writes that mention.** (Fowler; Newma
- b1h-r1 R1c B1 T3 :: ### B1. The SA-2 exception, AC-C1 and the P0 Orca sections contradict each other
- b1h-r1 R1c B2 T3 :: ### B2. The ready tier (section 3.1) says no command changes, but section 2.3, P0, P1 and AC-1.1 req
- b1h-r1 R1c B3 T3 :: ### B3. The fixed contract path in WC-4 does not fit the ready commands, so AC-0.4 and AC-1.2 cannot
- b1h-r2 AUD F-01 T1 :: ### F-01 (CRITICAL-adjacent MAJOR, blocking) Sequence attack: P1 makes `--unattended` available on c
- b1h-r2 AUD F-02 T1 :: ### F-02 (MAJOR, blocking) AC-1.1 contradicts the `/sc:load` row (zero/empty attack)
- b1h-r2 AUD2 F-1 T1 :: ### F-1 [MAJOR, blocking] Phase 1 ships `--unattended` on commands whose person-gates are only conve
- b1h-r2 R1a ARCH-1 T2 :: ### ARCH-1 (blocking): WC-4's `<output-dir>/return-contract.yaml` rule cannot be applied to the rows
- b1h-r2 R1a ARCH-2 T1 :: ### ARCH-2 (blocking): the P1 change to workflow writes a contract in standalone mode, which SA-3 fo
- b1h-r2 R1a ARCH-3 T1 :: ### ARCH-3 (blocking): P1 accepts `--unattended` on commands whose outward defaults stay on until P2
- b1h-r2 R1a ARCH-4 other :: ### ARCH-4 (blocking): the P2 reflect change makes a worker self-approve code remediation, which D2 
- b1h-r2 R1a REQ-1 other :: ### REQ-1 (blocking): the common acceptance check AC-C1 cannot pass in the phase that adds the contr
- b1h-r2 R1a REQ-2 T3 :: ### REQ-2 (blocking): AC-0.4 step 4 cannot pass for `/sc:troubleshoot`
- b1h-r2 R1b B1 other :: ### B1. CRITICAL. WC-3 lets a coordinator answer add a flag; WC-9 says only the brief can turn on an
- b1h-r2 R1b B2 other :: ### B2. CRITICAL. The AC-C1 grep cannot fail, so SA-2 and WC-8 have no working gate
- b1h-r2 R1b B3 other :: ### B3. MAJOR. WC-5 reports `succeeded` for a contract that is empty, unreadable or has an unknown s
- b1h-r2 R1b B4 T1 :: ### B4. CRITICAL. AC-1.1 cannot pass for `/sc:load`
- b1h-r2 R1b B5 T3 :: ### B5. CRITICAL. AC-0.4 step 4 cannot pass for `/sc:troubleshoot` as written
- b1h-r2 R1c RQ-1 other :: ### RQ-1 (BLOCKING). WC-3 lets a coordinator's reply become a gate answer, which contradicts the imp
- b1h-r2 R1c RQ-2 T3 :: ### RQ-2 (BLOCKING). The P0 phase cannot run the live check it is gated on
- b1h-r2 R1c AR-1 other :: ### AR-1 (BLOCKING). Two ready verdicts keep fixed output paths, which breaks WC-11 in the default s
- b1h-r3 AUD F-01 T3 :: ### F-01 BLOCKING (CRITICAL by consequence): AC-0.4 cannot pass as written, and its failure rule reo
- b1h-r3 AUD2 F1 T3 :: ### F1. CRITICAL-equivalent (blocking): the Phase 0 live-baseline check cannot pass as written
- b1h-r3 AUD2 F2 T1 :: ### F2. MAJOR (blocking): Phase 1 scope and AC-1.1 contradict the Phase 4 hold and the recommended D
- b1h-r3 R1a B1 other :: ### B1 (CRITICAL, blocking). The standalone-behaviour rule is contradicted by two rows
- b1h-r3 R1a B2 other :: ### B2 (CRITICAL, blocking). WC-3 lets a coordinator answer any gate, which contradicts the spec's o
- b1h-r3 R1a B3 T2 :: ### B3 (MAJOR, blocking). WC-5 reports a FAIL audit as `succeeded`, and no contract field carries th
- b1h-r3 R1a B4 T2 :: ### B4 (MAJOR, blocking). A contract with a missing or unrecognised `status` is reported as `succeed
- b1h-r3 R1a B5 T2 :: ### B5 (CRITICAL, blocking). Two contract paths for the same adversarial output
- b1h-r3 R1a B6 T3 :: ### B6 (MAJOR, blocking). Acceptance check AC-C1 cannot pass once P0 lands
- b1h-r3 R1a B7 T3 :: ### B7 (MAJOR, blocking). AC-0.4 step 4 cannot pass for the P0 ready commands
- b1h-r3 R1b F1 other :: **F1. MAJOR, blocking. Acceptance check AC-C1 cannot fail.** Expert: Wiegers (testability), Whittake
- b1h-r3 R1b F2 T2 :: **F2. MAJOR, blocking. The load row contradicts WC-4 and AC-1.1.** Expert: Wiegers (traceability). `
- b1h-r3 R1b F3 other :: **F3. MAJOR, FR-8 GAP, blocking. The outcome rule turns invalid status into success.** Expert: Nygar
- b1h-r3 R1c F1 T2 :: **F1. WC-4 says the report path is known before dispatch, but two §3 rows make it unknown or unnamed
- b1h-r3 R1c F2 other :: **F2. AC-C1 cannot fail on a real violation. [BLOCKING]**
- b1h-r3 R1c F3 other :: **F3. A retry can overwrite or misread the first attempt's contract. [BLOCKING]**
- b1h-r3 R1c F4 T2 :: **F4. The spec-panel row conflicts with the command definition on `--output`. [BLOCKING]**
- b1h-r4 AUD B-1 T1 :: **B-1. Phase 1 acceptance requires the `## Unattended mode` section on commands that other stated te
- b1h-r4 AUD B-2 other :: **B-2. WC-3 lets a worker obtain a blocked Ruling or authorization from the coordinator, which D2(a)
- b1h-r4 AUD B-3 other :: **B-3. The cli-portify row makes every unattended run end blocked, but AC-2.3 requires a happy-path 
- b1h-r4 AUD2 F-1 T2 :: ### F-1 [MAJOR, blocking] WC-4 places the contract under "the output directory", but the brief tells
- b1h-r4 AUD2 F-2 T1 :: ### F-2 [MAJOR, blocking] `--unattended` is required on every command in P1, but the gate conversion
- b1h-r4 R1a B1 T2 :: **B1. Output flag value types contradict each other (tdd, spec-panel, AC-2.2).** Expert: Fowler (lea
- b1h-r4 R1a B2 other :: **B2. init-lite re-run overwrites its report, which WC-6 forbids.** Expert: Nygard (lead), Fowler. S
- b1h-r4 R1a B3 other :: **B3. The outcome mapping treats an empty or status-less contract as success.** Expert: Whittaker (F
- b1h-r4 R1b B1 T3 :: ### B1. Phase 0 acceptance check AC-0.4 cannot pass as written. CRITICAL.
- b1h-r4 R1b B2 T1 :: ### B2. Phase 1 lets `--unattended` run with PR posting still on. CRITICAL.
- b1h-r4 R1b B3 T1 :: ### B3. Default output path breaks WC-11 for index-repo. MAJOR.
- b1h-r4 R1b B4 T2 :: ### B4. The load row contradicts WC-4 and AC-1.1. MAJOR.
- b1h-r4 R1c B-1 T2 :: #### B-1. WC-4 and the adversarial P1 fix name different contract paths (blocking)
- b1h-r4 R1c B-2 other :: #### B-2. AC-C1 cannot fail, so the SA-2 gate is non-functional (blocking)

## Theme overrides applied

none

## b1 vs b2 (k ablation)

ab2 metrics.json present: compare by hand (schema not fixed): /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/metrics.json
