# ab5 RESULTS (two arms from one harness: variant panel = d5-r*, variant full = d5f-r*)

# Variant `panel` (n=6; BRIEF.md: ab4 + PN1 panel + ab4-style merge over the four reports (cleaned blocks) + ADJ + clean VF.)

Outcome: **DROP** (DROP-2 cost without gain); R_LOOP 3.069558405693194 (decides, limit 2.69; LOOP includes ADJ), R_B 2.191739246740781 (reported only)

Baseline: B_BLK 1.50, B_AUDFAIL 0.917, B_THEME 0.833 over 12 audits; 

## Sonnet stratum (panel)

| run | loop end | rounds / agents | lost reviewers | lint findings 1/2/3 | growth | LOOP | AUD tokens | audit 1 BLK | audit 2 BLK | audit 1 | audit 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| d5-r1 | PASS | 2 / 5 | - | 0/0/- | +4.10% | 312336 | [69884, 65344] | 0 | 0 | PASS  | PASS  |
| d5-r2 | PASS | 2 / 5 | - | 0/0/- | +3.70% | 317545 | [56955, 61319] | 1 | 1 | FAIL F-1:T3 | FAIL F-01:T2 |
| d5-r3 | PASS | 2 / 5 | - | 0/0/- | +1.64% | 319802 | [66720, 86453] | 2 | 1 | FAIL R-01:other,R-02:other | FAIL F-1:other |
| d5-r4 | PASS | 2 / 5 | - | 0/0/- | +4.32% | 309961 | [68752, 62768] | 0 | 0 | PASS  | PASS  |
| d5-r5 | PASS | 2 / 5 | - | 0/0/- | +3.92% | 293102 | [61856, 50813] | 2 | 1 | FAIL R-01:T2,R-02:T1 | FAIL B-1:T1 |
| d5-r6 | PASS | 2 / 5 | - | 0/0/- | +1.93% | 296798 | [54867, 45080] | 2 | 2 | FAIL F-01:T1,F-02:other | FAIL F1:T1,F2:T2 |

## Tokens (loop only; output tokens, each message id once)

### Lanes

Lane map (decision.json `lanes`): primary = slots t1b + steps ADJ, VF1, V1, R2, VF2, V2, R3, VF3; tier234 = slots t2, t3, t4 + steps -; audit = slots - + steps AUD, AUD2; any other step = primary. Loop total = primary + tier234; audits are excluded. ADJ (adjudicator, Sonnet) sits in the primary lane and has its own column.

| run | primary (Sonnet) | of which ADJ (adjudicator, Sonnet) | parallel other-provider | t2-1 live GPT-6.1 Sol; used claude-haiku-5-5 (stand-in) | t3-1 live GPT-6.1 Terra (likely GLM-5.3 in practice); used claude-haiku-5-5 (stand-in) | t4-1 live GPT-6 Luna; used claude-haiku-5-5 (stand-in) | LOOP | audits (Sonnet, excluded) | loop/base | primary excl. ADJ/base | primary + ADJ/base |
|---|---|---|---|---|---|---|---|---|---|---|---|
| d5-r1 | 195,679 | 13,595 | 116,657 | 41,033 | 26,756 | 48,868 | 312,336 | 135,228 | 5.82 | 3.40 | 3.65 |
| d5-r2 | 190,484 | 12,065 | 127,061 | 44,044 | 40,781 | 42,236 | 317,545 | 118,274 | 5.92 | 3.33 | 3.55 |
| d5-r3 | 161,987 | 14,777 | 157,815 | 47,053 | 46,725 | 64,037 | 319,802 | 153,173 | 5.96 | 2.75 | 3.02 |
| d5-r4 | 182,992 | 13,041 | 126,969 | 56,336 | 35,825 | 34,808 | 309,961 | 131,520 | 5.78 | 3.17 | 3.41 |
| d5-r5 | 172,510 | 15,865 | 120,592 | 37,819 | 42,741 | 40,032 | 293,102 | 112,669 | 5.47 | 2.92 | 3.22 |
| d5-r6 | 171,643 | 12,235 | 125,155 | 46,991 | 33,385 | 44,779 | 296,798 | 99,947 | 5.53 | 2.97 | 3.20 |
| **mean (completed, n=6)** | 179,216 | 13,596 | 129,042 | 45,546 | 37,702 | 45,793 | 308,257 | 125,135 | 5.75 | 3.09 | 3.34 |

Headline ratios vs the fresh-baseline loop (53,623 tokens), means over completed runs: total loop 5.75; primary lane only (without ADJ) 3.09; primary + adjudicator 3.34.

### Loop-only output tokens per run, by step group

| run | panel (4 R1) | merge | ADJ | VF | revise | re-review | LOOP incl. ADJ | LOOP excl. ADJ | AUD | AUD2 | missing |
|---|---|---|---|---|---|---|---|---|---|---|---|
| d5-r1 | 195,794 | 0 | 13,595 | 14,597 | 32,139 | 56,211 | 312,336 | 298,741 | 69,884 | 65,344 | - |
| d5-r2 | 221,890 | 0 | 12,065 | 15,239 | 21,804 | 46,547 | 317,545 | 305,480 | 56,955 | 61,319 | - |
| d5-r3 | 227,380 | 0 | 14,777 | 16,675 | 15,183 | 45,787 | 319,802 | 305,025 | 66,720 | 86,453 | - |
| d5-r4 | 208,513 | 0 | 13,041 | 14,093 | 25,081 | 49,233 | 309,961 | 296,920 | 68,752 | 62,768 | - |
| d5-r5 | 187,705 | 0 | 15,865 | 13,614 | 28,155 | 47,763 | 293,102 | 277,237 | 61,856 | 50,813 | - |
| d5-r6 | 224,483 | 0 | 12,235 | 17,769 | 15,986 | 26,325 | 296,798 | 284,563 | 54,867 | 45,080 | - |
| mean (completed, n=6) | 210,961 | 0 | 13,596 | 15,331 | 23,058 | 45,311 | 308,257 | 294,661 | | | |

### Loop-only output tokens per run, per step (tokens / resolved model)

| run | R1.t1b-1 | R1.t2-1 | R1.t3-1 | R1.t4-1 | ADJ | VF1 | V1 | R2 | VF2 | V2 | R3 | VF3 | AUD | AUD2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d5-r1 | 79,137 / claude-sonnet-5-5 | 41,033 / claude-haiku-5-5 | 26,756 / claude-haiku-5-5 | 48,868 / claude-haiku-5-5 | 13,595 / claude-sonnet-5-5 | 14,597 / claude-sonnet-5-5 | 32,139 / claude-sonnet-5-5 | 56,211 / claude-sonnet-5-5 | . | . | . | . | 69,884 / claude-sonnet-5-5 | 65,344 / claude-sonnet-5-5 |
| d5-r2 | 94,829 / claude-sonnet-5-5 | 44,044 / claude-haiku-5-5 | 40,781 / claude-haiku-5-5 | 42,236 / claude-haiku-5-5 | 12,065 / claude-sonnet-5-5 | 15,239 / claude-sonnet-5-5 | 21,804 / claude-sonnet-5-5 | 46,547 / claude-sonnet-5-5 | . | . | . | . | 56,955 / claude-sonnet-5-5 | 61,319 / claude-sonnet-5-5 |
| d5-r3 | 69,565 / claude-sonnet-5-5 | 47,053 / claude-haiku-5-5 | 46,725 / claude-haiku-5-5 | 64,037 / claude-haiku-5-5 | 14,777 / claude-sonnet-5-5 | 16,675 / claude-sonnet-5-5 | 15,183 / claude-sonnet-5-5 | 45,787 / claude-sonnet-5-5 | . | . | . | . | 66,720 / claude-sonnet-5-5 | 86,453 / claude-sonnet-5-5 |
| d5-r4 | 81,544 / claude-sonnet-5-5 | 56,336 / claude-haiku-5-5 | 35,825 / claude-haiku-5-5 | 34,808 / claude-haiku-5-5 | 13,041 / claude-sonnet-5-5 | 14,093 / claude-sonnet-5-5 | 25,081 / claude-sonnet-5-5 | 49,233 / claude-sonnet-5-5 | . | . | . | . | 68,752 / claude-sonnet-5-5 | 62,768 / claude-sonnet-5-5 |
| d5-r5 | 67,113 / claude-sonnet-5-5 | 37,819 / claude-haiku-5-5 | 42,741 / claude-haiku-5-5 | 40,032 / claude-haiku-5-5 | 15,865 / claude-sonnet-5-5 | 13,614 / claude-sonnet-5-5 | 28,155 / claude-sonnet-5-5 | 47,763 / claude-sonnet-5-5 | . | . | . | . | 61,856 / claude-sonnet-5-5 | 50,813 / claude-sonnet-5-5 |
| d5-r6 | 99,328 / claude-sonnet-5-5 | 46,991 / claude-haiku-5-5 | 33,385 / claude-haiku-5-5 | 44,779 / claude-haiku-5-5 | 12,235 / claude-sonnet-5-5 | 17,769 / claude-sonnet-5-5 | 15,986 / claude-sonnet-5-5 | 26,325 / claude-sonnet-5-5 | . | . | . | . | 54,867 / claude-sonnet-5-5 | 45,080 / claude-sonnet-5-5 |

`.` = step not run; `-` = step ran, no transcript matched yet (run `python3 harness.py tokens`). Model = transcript's observed model, else the launch-ledger model, else the model on the step record (never from the step name). AUD/AUD2 are not loop steps.

## Metrics (pooled over completed audits; replicas below)

- n_completed: 6
- n_audits: 12
- BLK_T: 1.0
- audit_fail: 8
- theme_rate: 6
- theme_counts: {'T1': 4, 'T2': 3, 'T3': 1, 'other': 3}
- loop_pass: 6
- growth: 0.03268816831997415
- LOOP_T: 308257.3333333333
- TOK_T: 371429.6666666666
- R_LOOP: 3.069558405693194
- R_B: 2.191739246740781
- REJ1: 26
- N1: 82
- REJ1_rate: 0.3170731707317073
- replica audit 1 only: DROP (BLK_T 1.1666666666666667, DROP-2 cost without gain)
- replica audit 2 only: DROP (BLK_T 0.8333333333333334, DROP-2 cost without gain)

## Final spec per run (input of the 44-defect ledger scoring)

- d5-r1: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p18/ab5/runs/d5-r1/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
- d5-r2: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p18/ab5/runs/d5-r2/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
- d5-r3: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p18/ab5/runs/d5-r3/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
- d5-r4: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p18/ab5/runs/d5-r4/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
- d5-r5: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p18/ab5/runs/d5-r5/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
- d5-r6: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p18/ab5/runs/d5-r6/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md

## Haiku stratum (never pooled; not built in ab5)

{
 "state": "pending"
}

## Design-specific tables (Sonnet)

### Per-theme capture, panel (runs with at least one first review)

| theme | t1b-1 live Sonnet 5.5; used claude-sonnet-5-5 + AC sweep | t2-1 live GPT-6.1 Sol; used claude-haiku-5-5 (stand-in) | t3-1 live GPT-6.1 Terra (likely GLM-5.3 in practice); used claude-haiku-5-5 (stand-in) | t4-1 live GPT-6 Luna; used claude-haiku-5-5 (stand-in) | union (panel) | baseline k=1 |
|---|---|---|---|---|---|---|
| T1 | 6/6 | 3/6 | 0/6 | 2/6 | 6/6 | 6/6 |
| T2 | 6/6 | 4/6 | 5/6 | 4/6 | 6/6 | 2/6 |
| T3 | 6/6 | 4/6 | 4/6 | 4/6 | 6/6 | 3/6 |

| run | t1b-1 | t2-1 | t3-1 | t4-1 | union | lost reviewers | lint findings 1/2/3 | lint by check (lint-1) |
|---|---|---|---|---|---|---|---|---|
| d5-r1 | FAIL 6 T1,T2,T3 | FAIL 4 T1,T2 | FAIL 5 T2,T3 | FAIL 2 T2 | T1,T2,T3 | - | 0/0/- | {} |
| d5-r2 | FAIL 5 T1,T2,T3 | FAIL 2 T1,T2 | FAIL 2 T2 | FAIL 3 T2 | T1,T2,T3 | - | 0/0/- | {} |
| d5-r3 | FAIL 6 T1,T2,T3 | FAIL 4 T2,T3 | FAIL 2 T2,T3 | FAIL 3 T1,T2,T3 | T1,T2,T3 | - | 0/0/- | {} |
| d5-r4 | FAIL 5 T1,T2,T3 | FAIL 5 T2,T3 | FAIL 3 T2,T3 | FAIL 4 T2,T3 | T1,T2,T3 | - | 0/0/- | {} |
| d5-r5 | FAIL 4 T1,T2,T3 | FAIL 5 T1,T3 | FAIL 2 T2 | FAIL 4 T1,T3 | T1,T2,T3 | - | 0/0/- | {} |
| d5-r6 | FAIL 5 T1,T2,T3 | FAIL 3 T3 | FAIL 3 T3 | FAIL 1 T3 | T1,T2,T3 | - | 0/0/- | {} |

Cells: verdict, blocking count, themes. t1b-1 carries the ab4 acceptance-criteria sweep sentence; the other three have the plain brief.

### Merged-finding count

| run | raw | merged | dedup ratio |
|---|---|---|---|
| d5-r1 | 17 | 14 | 0.82 |
| d5-r2 | 12 | 12 | 1.00 |
| d5-r3 | 15 | 14 | 0.93 |
| d5-r4 | 17 | 15 | 0.88 |
| d5-r5 | 15 | 15 | 1.00 |
| d5-r6 | 12 | 12 | 1.00 |

### ADJ (PN1 adjudicator, measurement only) vs VF1

| run | merged | ADJ confirmed | rejected | unsure | VF1 confirmed | agree (confirm/other) | parse_ok |
|---|---|---|---|---|---|---|---|
| d5-r1 | 14 | 11 | 3 | 0 | 13 | 12/14 | True |
| d5-r2 | 12 | 10 | 0 | 2 | 7 | 9/12 | True |
| d5-r3 | 14 | 9 | 5 | 0 | 7 | 12/14 | True |
| d5-r4 | 15 | 10 | 3 | 2 | 11 | 14/15 | True |
| d5-r5 | 15 | 8 | 7 | 0 | 11 | 12/15 | True |
| d5-r6 | 12 | 4 | 5 | 3 | 7 | 9/12 | True |

### Verifier

| run | step | sent | confirmed | rejected | parse_ok |
|---|---|---|---|---|---|
| d5-r1 | VF1 | 14 | 13 | 1 | True |
| d5-r2 | VF1 | 12 | 7 | 5 | True |
| d5-r3 | VF1 | 14 | 7 | 7 | True |
| d5-r4 | VF1 | 15 | 11 | 4 | True |
| d5-r5 | VF1 | 15 | 11 | 4 | True |
| d5-r6 | VF1 | 12 | 7 | 5 | True |

pooled rejection rate over all VF steps: 26/82

### Noted, unactioned vs audits

| run | step | id | theme | verifier reason | matched audit blocker | eyeball |
|---|---|---|---|---|---|---|
| d5-r1 | VF1 | M9 | other | ` throughout (`:172`, `:175`). The "never matches" outcome needs the added assum | none | (eyeball) |
| d5-r2 | VF1 | M5 | other | The candidate does not say what `--resume` does at a gate (whether a resumed run | none | (eyeball) |
| d5-r2 | VF1 | M8 | T2 | The conflicting text (the command's existing file-valued `--output`) is outside  | AUD2/F-01 | (eyeball) |
| d5-r2 | VF1 | M9 | T2 | AC-1.1 only requires that load's `## Unattended mode` section name `return-contr | AUD2/F-01 | (eyeball) |
| d5-r2 | VF1 | M11 | other | The two texts can both be satisfied (pass `--unattended` plus the stated flags), | none | (eyeball) |
| d5-r2 | VF1 | M12 | other | Overwrite is not shown to be "corruption", and init-lite's brief passes `--outpu | none | (eyeball) |
| d5-r3 | VF1 | M7 | T3 | The regex matches only lowercase `orca`/`orca-ide` followed by orchestration, wo | none | (eyeball) |
| d5-r3 | VF1 | M8 | T2 | M8.a: the claim that spec-panel already has a file-valued `--output` and refuses | none | (eyeball) |
| d5-r3 | VF1 | M9 | other | M9.a: the entry contains no quoted text or claim to check. | none | (eyeball) |
| d5-r3 | VF1 | M10 | T2 | M10.a: line 73 makes the output directory part of every brief, the reflect and t | none | (eyeball) |
| d5-r3 | VF1 | M11 | T3 | M11.a: AC-0.4 does not list step 4 among the steps that must pass, so the YAML a | none | (eyeball) |
| d5-r3 | VF1 | M12 | T3 | M12.a: AC-0.4 spells out the three command lines without `--unattended`, and not | none | (eyeball) |
| d5-r3 | VF1 | M14 | T2 | M14.a: the cleanup-audit row itself restricts the coordinator to one audit per w | none | (eyeball) |
| d5-r4 | VF1 | M7 | other | L109 and L218 keep the Ruling rule unchanged, and L233 quotes it as rejecting "a | none | (eyeball) |
| d5-r4 | VF1 | M9 | other | ` matches (exit 0). That only matters if the table escape is left in when the co | none | (eyeball) |
| d5-r4 | VF1 | M10 | other | Section 3 rows (L102, L108) and SA-4 (L149) name each of these fixes explicitly, | none | (eyeball) |
| d5-r4 | VF1 | M12 | other | ` is the table-cell escape used throughout the file (L172 twice, L175, L176, L19 | none | (eyeball) |
| d5-r5 | VF1 | M3 | T2 | `:159` assigns "output flags for commands that lack one" to P1 without restricti | none | (eyeball) |
| d5-r5 | VF1 | M7 | other | Both rows sit in the 3.2 column headed "Unattended-mode gate resolution (WC-2)", | none | (eyeball) |
| d5-r5 | VF1 | M8 | other | The brief passes `--output <file>`, so the coordinator supplies a per-worker pat | none | (eyeball) |
| d5-r5 | VF1 | M9 | T1 | `:159` makes index-repo a P1 command and gives P1 "output flags for commands tha | none | (eyeball) |
| d5-r6 | VF1 | M4 | T2 | Line 159 says P1 adds "output flags for commands that lack one", so a directory  | AUD2/F2 | (eyeball) |
| d5-r6 | VF1 | M6 | other | WC-3 only permits asking ("may"). Line 109 leaves the Ruling rule unchanged and  | none | (eyeball) |
| d5-r6 | VF1 | M7 | other | grep -v` in the same cell uses the same escape. The pattern is a working alterna | none | (eyeball) |
| d5-r6 | VF1 | M9 | other | `. The empty result needs a literal raw copy of the cell. | none | (eyeball) |
| d5-r6 | VF1 | M11 | other | E3 claims only that the work "has worked before" and does not say the run was th | none | (eyeball) |

## Theme tags to eyeball

- d5-r1 R1.t1b-1 F1 T2 :: ### F1. WC-4 defines one contract path; four section 3 rows and two acceptance examples use other pa
- d5-r1 R1.t1b-1 F2 T3 :: ### F2. AC-0.4 step 3 and step 4 cannot pass in Phase 0
- d5-r1 R1.t1b-1 F3 other :: ### F3. AC-2.2 cannot pass for four of the fifteen P2 commands (two more depend on an undefined "ref
- d5-r1 R1.t1b-1 F4 other :: ### F4. AC-2.3 cannot pass for cli-portify
- d5-r1 R1.t1b-1 F5 T1 :: ### F5. `/sc:load`: the row and the decision say "no report, not a Task", AC-1.1 and AC-1.2 require 
- d5-r1 R1.t1b-1 F6 T1 :: ### F6. Phase 1 puts `--unattended` on 37 commands while the behaviour behind it is built for 15 in 
- d5-r1 R1.t2-1 B1 T1 :: ### B1. The `/sc:load` report contract is required and forbidden at once
- d5-r1 R1.t2-1 B2 T2 :: ### B2. The adversarial contract path is named two ways
- d5-r1 R1.t2-1 B3 T2 :: ### B3. The workflow contract path is not known before dispatch, and pre-creation STOPs have no loca
- d5-r1 R1.t2-1 B4 other :: ### B4. The AC-C1 grep pattern never matches, so the SA-2 and WC-8 check always passes
- d5-r1 R1.t3-1 B1 T2 :: ### B1. Adversarial contract path contradicts the WC-4 path
- d5-r1 R1.t3-1 B2 other :: ### B2. init-lite retry overwrites the first attempt, contrary to WC-6
- d5-r1 R1.t3-1 B3 other :: ### B3. cleanup-audit uses a fixed output path, contrary to WC-11
- d5-r1 R1.t3-1 B4 T2 :: ### B4. Contract path is not known before dispatch for four commands
- d5-r1 R1.t3-1 B5 T3 :: ### B5. AC-0.4 step 4 cannot pass for troubleshoot
- d5-r1 R1.t4-1 B-1 T2 :: **B-1 (MAJOR, blocking). The contract location is defined as a directory, but two rows pass a file.*
- d5-r1 R1.t4-1 B-2 other :: **B-2 (MAJOR, blocking). The load row writes no report, but the acceptance check requires one.**
- d5-r2 AUD F-1 T3 :: ### F-1 (blocking) The P0 acceptance check cannot pass for /sc:adversarial
- d5-r2 AUD2 F-01 T2 :: #### F-01 — MAJOR — blocking — WC-4 contract path for a file-valued flag collides with WC-11 (Whitta
- d5-r2 R1.t1b-1 B1 T2 :: ### B1 (blocking): WC-4's contract path and the adversarial row name two different paths for the sam
- d5-r2 R1.t1b-1 B2 T3 :: ### B2 (blocking): AC-0.4 cannot pass for `/sc:troubleshoot` (and cannot be run as briefed) in Phase
- d5-r2 R1.t1b-1 B3 T1 :: ### B3 (blocking): AC-1.1 and AC-1.2 cannot pass for `/sc:load`, and AC-1.2 cannot be run on P1 comm
- d5-r2 R1.t1b-1 B4 other :: ### B4 (blocking): AC-2.2 requires a `blocked` contract from every P2 command, but 6 of the 15 have 
- d5-r2 R1.t1b-1 B5 other :: ### B5 (blocking): AC-2.3 cannot reach `--outcome succeeded` for `/sc:cli-portify`
- d5-r2 R1.t2-1 B1 T2 :: ### B1. WC-4 names a report path that the workflow row cannot produce (two stated texts contradict)
- d5-r2 R1.t2-1 B2 T1 :: ### B2. AC-1.1 cannot pass at the end of P1, and two commands are never scheduled (acceptance criter
- d5-r2 R1.t3-1 F1 T2 :: ### F1 (blocking, MAJOR): spec-panel `--output` contradicts the command's existing flag
- d5-r2 R1.t3-1 F2 T2 :: ### F2 (blocking, MAJOR): `load` is required to write a contract it does not write
- d5-r2 R1.t4-1 B1 T2 :: ### B1. The WC-4 contract path rule contradicts the per-command rows (requirements)
- d5-r2 R1.t4-1 B2 other :: ### B2. Every brief must carry `--unattended`, but the ready-today commands do not accept it (requir
- d5-r2 R1.t4-1 B3 other :: ### B3. The init-lite re-run overwrites its report, which breaks WC-6 (requirements)
- d5-r3 AUD R-01 other :: ### R-01 (blocking): the `/sc:index` row contradicts UNVERIFIED item 6
- d5-r3 AUD R-02 other :: ### R-02 (blocking): the additive-only check cannot see deleted bullets
- d5-r3 AUD2 F-1 other :: **F-1. cli-portify has no route to a successful unattended run, so AC-2.3 cannot pass and Phase 2 ca
- d5-r3 R1.t1b-1 F1 T2 :: ### F1 (blocking) Adversarial contract path contradicts the WC-4 location rule
- d5-r3 R1.t1b-1 F2 T2 :: ### F2 (blocking) WC-4 requires a caller-passed directory, but tdd and init-lite take a file as `--o
- d5-r3 R1.t1b-1 F3 T1 :: ### F3 (blocking) `/sc:load` is required by AC-1.1 and AC-1.2 to have a contract that the spec says 
- d5-r3 R1.t1b-1 F4 T3 :: ### F4 (blocking) AC-0.4 and live-check step 3 cannot both pass in Phase 0
- d5-r3 R1.t1b-1 F5 other :: ### F5 (blocking) AC-2.2 expects `blocked` from commands whose section 3 rows never block
- d5-r3 R1.t1b-1 F6 T1 :: ### F6 (blocking, count mismatch) P1 scope and AC-1.1 cover 37 commands, but only 13 are scheduled i
- d5-r3 R1.t2-1 B1 T3 :: **B1. Acceptance check AC-C1 rejects the Orca mention that SA-2 allows (contradiction; Wiegers lead,
- d5-r3 R1.t2-1 B2 T2 :: **B2. The spec-panel row asks for an `--output` flag that the command already has, in the wrong form
- d5-r3 R1.t2-1 B3 T2 :: **B3. The fixed contract path and the fresh-directory rule for retries cannot both hold (contradicti
- d5-r3 R1.t2-1 C1 other :: 
- d5-r3 R1.t3-1 B-1 T2 :: **B-1. The report path is not known before dispatch for several rows that WC-4 requires it for.**
- d5-r3 R1.t3-1 B-2 T3 :: **B-2. The P0 acceptance check at AC-0.4 cannot pass as written.**
- d5-r3 R1.t4-1 B-1 T3 :: ### B-1. The P0 smoke runs cannot pass as written, because the brief they use has a flag that does n
- d5-r3 R1.t4-1 B-2 T1 :: ### B-2. Row for `/sc:load` breaks the contract that every changed command writes a return contract,
- d5-r3 R1.t4-1 B-3 T2 :: ### B-3. Fixed default output paths let parallel workers in one worktree write the same file, which 
- d5-r4 R1.t1b-1 F1 T2 :: #### F1 (MAJOR, blocking, Wiegers/Adzic) WC-4 gives no contract location when the output flag is a f
- d5-r4 R1.t1b-1 F2 T2 :: #### F2 (MAJOR, blocking, Fowler/Wiegers) The adversarial contract path contradicts the WC-4 path de
- d5-r4 R1.t1b-1 F3 T3 :: #### F3 (MAJOR, blocking, Crispin/Nygard) AC-0.4 cannot pass: step 3 needs the WC-4 contract, which 
- d5-r4 R1.t1b-1 F4 T1 :: #### F4 (MAJOR, blocking, Wiegers) AC-1.2 cannot pass for `/sc:load`, whose spec text says it writes
- d5-r4 R1.t1b-1 F5 T1 :: #### F5 (CRITICAL, blocking, Nygard/Whittaker Sequence attack) P1 makes `--unattended` accepted on e
- d5-r4 R1.t2-1 F-01 T2 :: ### F-01 (MAJOR, Wiegers) BLOCKING: section 3.1 says ten commands change only by small fixes, but WC
- d5-r4 R1.t2-1 F-02 other :: ### F-02 (CRITICAL, Whittaker FR-2.4 Sequence attack) BLOCKING: WC-3 lets a coordinator answer reach
- d5-r4 R1.t2-1 F-03 T3 :: ### F-03 (MAJOR, Adzic) BLOCKING: AC-0.4 cannot pass for /sc:troubleshoot as the spec describes it
- d5-r4 R1.t2-1 F-04 other :: ### F-04 (MAJOR, Adzic) BLOCKING: the AC-C1 grep cannot match, so the SA-2 / WC-8 guard always passe
- d5-r4 R1.t2-1 F-05 other :: ### F-05 (MAJOR, Cockburn/Fowler) BLOCKING: section 1.1 limits command changes to section 2, but sec
- d5-r4 R1.t3-1 B1 T3 :: **B1. The P0 acceptance check cannot pass for `/sc:troubleshoot` as written.**
- d5-r4 R1.t3-1 B2 other :: **B2. The AC-C1 grep never matches, so the SA-2 and WC-8 gate passes even when a command calls Orca.
- d5-r4 R1.t3-1 B3 T2 :: **B3. The report-path rule in WC-4 contradicts four commands the spec itself assigns to workers.**
- d5-r4 R1.t4-1 B1 T2 :: ### B1. The contract path is stated two ways
- d5-r4 R1.t4-1 B2 T3 :: ### B2. `--unattended` in every brief contradicts the P0 smoke runs
- d5-r4 R1.t4-1 B3 other :: ### B3. The scope of the `--unattended` flag is stated three ways
- d5-r4 R1.t4-1 B4 T3 :: ### B4. AC-0.4 step 4 cannot pass for two of the three P0 commands
- d5-r5 AUD R-01 T2 :: ### R-01 (blocking, CRITICAL, High priority): the WC-4 contract path contradicts the file-valued `--
- d5-r5 AUD R-02 T1 :: ### R-02 (blocking, CRITICAL, High priority): AC-1.1 requires 36 per-command sections in P1; the pha
- d5-r5 AUD2 B-1 T1 :: ### B-1 [MAJOR by label, BLOCKING by consequence] Phase 1 scope and AC-1.1 contradict the per-comman
- d5-r5 R1.t1b-1 F1 T1 :: ### F1. AC-1.2 (and AC-1.1) cannot pass for `/sc:load`, a P1 command that has no report and is not a
- d5-r5 R1.t1b-1 F2 T3 :: ### F2. WC-4 and 7.2 step 3 name one contract path, but AC-0.4 and the 3.1 rows put the contract els
- d5-r5 R1.t1b-1 F3 T2 :: ### F3. AC-1.2 prescribes `--output <dir>` for P1 commands that have no such flag (CRITICAL: an acce
- d5-r5 R1.t1b-1 F4 other :: ### F4. AC-2.2 requires a `blocked` outcome from P2 commands whose gate rows never resolve as blocke
- d5-r5 R1.t2-1 B1 other :: ### B1. AC-C1 cannot fail (safety-boundary check is vacuous)
- d5-r5 R1.t2-1 B2 T3 :: ### B2. P0 gate step 4 cannot pass for `/sc:troubleshoot`
- d5-r5 R1.t2-1 B3 other :: ### B3. Two rows add prompt or flag behaviour outside `--unattended`, against SA-1
- d5-r5 R1.t2-1 B4 other :: ### B4. init-lite row contradicts WC-6 and WC-11
- d5-r5 R1.t2-1 B5 T1 :: ### B5. index-repo default output path contradicts WC-11
- d5-r5 R1.t3-1 B1 T2 :: **B1. The `/sc:load` row contradicts WC-4 and AC-1.1.**
- d5-r5 R1.t3-1 B2 T2 :: **B2. The report path is not known before dispatch for three rows, contrary to section 2.3 and WC-4.
- d5-r5 R1.t4-1 B1 T3 :: **B1. AC-0.4 cannot pass as written.** Sentence: an implementer who follows AC-0.4 as written runs `
- d5-r5 R1.t4-1 B2 T1 :: **B2. The `load` row contradicts AC-1.1.** Sentence: an implementer who follows AC-1.1 (spec:195) ad
- d5-r5 R1.t4-1 B3 T1 :: **B3. Section 3.1 contradicts P1 on which commands change.** Sentence: an implementer who follows se
- d5-r5 R1.t4-1 B4 other :: **B4. AC-C1 cannot fail, so it does not check SA-2 or WC-8.** Sentence: an implementer who adds `orc
- d5-r6 AUD F-01 T1 :: ### F-01 (CRITICAL, blocking, priority High) - Wiegers, Cockburn
- d5-r6 AUD F-02 other :: ### F-02 (MAJOR, blocking, priority High) - Crispin, Whittaker
- d5-r6 AUD2 F1 T1 :: ### F1. Phase 1 acceptance check forces sections that the spec says wait for later phases and for op
- d5-r6 AUD2 F2 T2 :: ### F2. WC-4 defines the contract path from "the directory the coordinator passed", but the spec's o
- d5-r6 R1.t1b-1 F1 T3 :: ### F1 (CRITICAL, blocking): AC-0.4, the P0 gate, cannot pass as written
- d5-r6 R1.t1b-1 F2 T1 :: ### F2 (MAJOR, blocking): `/sc:load` is told to have no contract, and also to pass a contract check
- d5-r6 R1.t1b-1 F3 T2 :: ### F3 (MAJOR, blocking): `/sc:adversarial` gets two different contract paths
- d5-r6 R1.t1b-1 F4 T2 :: ### F4 (MAJOR, blocking): no contract path for commands that take no output directory
- d5-r6 R1.t1b-1 F5 other :: ### F5 (CRITICAL, blocking): AC-2.2 requires a `blocked` outcome from P2 commands whose rows never b
- d5-r6 R1.t2-1 F1 other :: **F1. WC-3 lets a coordinator answer any blocked gate, which contradicts the implement row and D2 (b
- d5-r6 R1.t2-1 F2 other :: **F2. The SA-2 / WC-8 grep check (AC-C1) cannot match, so it always passes (blocking).** Severity: M
- d5-r6 R1.t2-1 F3 T3 :: **F3. AC-0.4 cannot pass in P0 as written (blocking).** Severity: MAJOR.
- d5-r6 R1.t3-1 B1 other :: ### B1. AC-C1 cannot detect any Orca call (SA-2, WC-8 unenforced)
- d5-r6 R1.t3-1 B2 T3 :: ### B2. The brief rule and the P0 smoke runs contradict each other on `--unattended`
- d5-r6 R1.t3-1 B3 other :: ### B3. The spec contradicts itself on whether the direct (non-nested) route was observed
- d5-r6 R1.t4-1 B1 T3 :: ### B1 (BLOCKING, requirements): the brief flag set contradicts the "ready today" set and the P0 acc

## Theme overrides applied

none

# Variant `full` (n=6; owner change 2026-11-10: ab4 + everything in PN1: panel, PN1 merge with the typed ledger, ADJ over ledger rows, ledger-driven revise, PN1 re-review sandboxes/inputs; ab4 layers on top (lint, AC sweep on t1b-1, cleaned blocks, clean VF, confirmed line, ids_from cross-check, token matcher).)

Outcome: **DROP** (DROP-4 harm); R_LOOP 4.33087044265647 (decides, limit 2.69; LOOP includes ADJ), R_B 2.9692488650758055 (reported only)

Baseline: B_BLK 1.50, B_AUDFAIL 0.917, B_THEME 0.833 over 12 audits; 

## Sonnet stratum (full)

| run | loop end | rounds / agents | lost reviewers | lint findings 1/2/3 | growth | LOOP | AUD tokens | audit 1 BLK | audit 2 BLK | audit 1 | audit 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| d5f-r1 | ESCALATED | 3 / 6 | - | 0/0/0 | +5.03% | 467425 | [93917, 72378] | 0 | 0 | PASS  | PASS  |
| d5f-r2 | VERIFIED-PASS | 2 / 5 | - | 0/0/- | +6.42% | 467738 | [80566, 77160] | 1 | 0 | FAIL F-01:other | PASS  |
| d5f-r3 | ESCALATED | 3 / 6 | - | 0/0/0 | +4.14% | 486036 | [48160, 58000] | 0 | 0 | PASS  | PASS  |
| d5f-r4 | VERIFIED-PASS | 2 / 5 | - | 0/0/- | +4.49% | 415377 | [54989, 74663] | 0 | 0 | PASS  | PASS  |
| d5f-r5 | PASS | 2 / 5 | - | 0/0/- | +4.51% | 370307 | [70842, 55280] | 0 | 0 | PASS  | PASS  |
| d5f-r6 | VERIFIED-PASS | 2 / 5 | - | 0/0/- | +1.79% | 402657 | [61142, 74983] | 2 | 0 | FAIL F-01:T1,F-02:T2 | PASS  |

## Tokens (loop only; output tokens, each message id once)

### Lanes

Lane map (decision.json `lanes`): primary = slots t1b + steps ADJ, VF1, V1, R2, VF2, V2, R3, VF3; tier234 = slots t2, t3, t4 + steps -; audit = slots - + steps AUD, AUD2; any other step = primary. Loop total = primary + tier234; audits are excluded. ADJ (adjudicator, Sonnet) sits in the primary lane and has its own column.

| run | primary (Sonnet) | of which ADJ (adjudicator, Sonnet) | parallel other-provider | t2-1 live GPT-6.1 Sol; used claude-haiku-5-5 (stand-in) | t3-1 live GPT-6.1 Terra (likely GLM-5.3 in practice); used claude-haiku-5-5 (stand-in) | t4-1 live GPT-6 Luna; used claude-haiku-5-5 (stand-in) | LOOP | audits (Sonnet, excluded) | loop/base | primary excl. ADJ/base | primary + ADJ/base |
|---|---|---|---|---|---|---|---|---|---|---|---|
| d5f-r1 | 309,314 | 10,295 | 158,111 | 38,233 | 82,634 | 37,244 | 467,425 | 166,295 | 8.72 | 5.58 | 5.77 |
| d5f-r2 | 254,091 | 13,574 | 213,647 | 46,685 | 77,175 | 89,787 | 467,738 | 157,726 | 8.72 | 4.49 | 4.74 |
| d5f-r3 | 298,530 | 18,880 | 187,506 | 52,419 | 54,203 | 80,884 | 486,036 | 106,160 | 9.06 | 5.22 | 5.57 |
| d5f-r4 | 255,711 | 10,415 | 159,666 | 54,292 | 68,633 | 36,741 | 415,377 | 129,652 | 7.75 | 4.57 | 4.77 |
| d5f-r5 | 217,761 | 11,828 | 152,546 | 53,074 | 43,498 | 55,974 | 370,307 | 126,122 | 6.91 | 3.84 | 4.06 |
| d5f-r6 | 215,762 | 16,925 | 186,895 | 59,040 | 52,763 | 75,092 | 402,657 | 136,125 | 7.51 | 3.71 | 4.02 |
| **mean (completed, n=6)** | 258,528 | 13,653 | 176,395 | 50,624 | 63,151 | 62,620 | 434,923 | 137,013 | 8.11 | 4.57 | 4.82 |

Headline ratios vs the fresh-baseline loop (53,623 tokens), means over completed runs: total loop 8.11; primary lane only (without ADJ) 4.57; primary + adjudicator 4.82.

### Loop-only output tokens per run, by step group

| run | panel (4 R1) | merge | ADJ | VF | revise | re-review | LOOP incl. ADJ | LOOP excl. ADJ | AUD | AUD2 | missing |
|---|---|---|---|---|---|---|---|---|---|---|---|
| d5f-r1 | 247,716 | 0 | 10,295 | 58,309 | 46,469 | 104,636 | 467,425 | 457,130 | 93,917 | 72,378 | - |
| d5f-r2 | 293,412 | 0 | 13,574 | 44,734 | 39,860 | 76,158 | 467,738 | 454,164 | 80,566 | 77,160 | - |
| d5f-r3 | 285,493 | 0 | 18,880 | 48,822 | 33,428 | 99,413 | 486,036 | 467,156 | 48,160 | 58,000 | - |
| d5f-r4 | 236,813 | 0 | 10,415 | 52,538 | 36,994 | 78,617 | 415,377 | 404,962 | 54,989 | 74,663 | - |
| d5f-r5 | 230,838 | 0 | 11,828 | 22,470 | 33,388 | 71,783 | 370,307 | 358,479 | 70,842 | 55,280 | - |
| d5f-r6 | 264,696 | 0 | 16,925 | 47,955 | 20,074 | 53,007 | 402,657 | 385,732 | 61,142 | 74,983 | - |
| mean (completed, n=6) | 259,828 | 0 | 13,653 | 45,805 | 35,036 | 80,602 | 434,923 | 421,270 | | | |

### Loop-only output tokens per run, per step (tokens / resolved model)

| run | R1.t1b-1 | R1.t2-1 | R1.t3-1 | R1.t4-1 | ADJ | VF1 | V1 | R2 | VF2 | V2 | R3 | VF3 | AUD | AUD2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d5f-r1 | 89,605 / claude-sonnet-5-5 | 38,233 / claude-haiku-5-5 | 82,634 / claude-haiku-5-5 | 37,244 / claude-haiku-5-5 | 10,295 / claude-sonnet-5-5 | 39,383 / claude-sonnet-5-5 | 31,676 / claude-sonnet-5-5 | 42,743 / claude-sonnet-5-5 | 10,552 / claude-sonnet-5-5 | 14,793 / claude-sonnet-5-5 | 61,893 / claude-sonnet-5-5 | 8,374 / claude-sonnet-5-5 | 93,917 / claude-sonnet-5-5 | 72,378 / claude-sonnet-5-5 |
| d5f-r2 | 79,765 / claude-sonnet-5-5 | 46,685 / claude-haiku-5-5 | 77,175 / claude-haiku-5-5 | 89,787 / claude-haiku-5-5 | 13,574 / claude-sonnet-5-5 | 40,718 / claude-sonnet-5-5 | 39,860 / claude-sonnet-5-5 | 76,158 / claude-sonnet-5-5 | 4,016 / claude-sonnet-5-5 | . | . | . | 80,566 / claude-sonnet-5-5 | 77,160 / claude-sonnet-5-5 |
| d5f-r3 | 97,987 / claude-sonnet-5-5 | 52,419 / claude-haiku-5-5 | 54,203 / claude-haiku-5-5 | 80,884 / claude-haiku-5-5 | 18,880 / claude-sonnet-5-5 | 34,767 / claude-sonnet-5-5 | 25,416 / claude-sonnet-5-5 | 67,959 / claude-sonnet-5-5 | 11,771 / claude-sonnet-5-5 | 8,012 / claude-sonnet-5-5 | 31,454 / claude-sonnet-5-5 | 2,284 / claude-sonnet-5-5 | 48,160 / claude-sonnet-5-5 | 58,000 / claude-sonnet-5-5 |
| d5f-r4 | 77,147 / claude-sonnet-5-5 | 54,292 / claude-haiku-5-5 | 68,633 / claude-haiku-5-5 | 36,741 / claude-haiku-5-5 | 10,415 / claude-sonnet-5-5 | 39,775 / claude-sonnet-5-5 | 36,994 / claude-sonnet-5-5 | 78,617 / claude-sonnet-5-5 | 12,763 / claude-sonnet-5-5 | . | . | . | 54,989 / claude-sonnet-5-5 | 74,663 / claude-sonnet-5-5 |
| d5f-r5 | 78,292 / claude-sonnet-5-5 | 53,074 / claude-haiku-5-5 | 43,498 / claude-haiku-5-5 | 55,974 / claude-haiku-5-5 | 11,828 / claude-sonnet-5-5 | 22,470 / claude-sonnet-5-5 | 33,388 / claude-sonnet-5-5 | 71,783 / claude-sonnet-5-5 | . | . | . | . | 70,842 / claude-sonnet-5-5 | 55,280 / claude-sonnet-5-5 |
| d5f-r6 | 77,801 / claude-sonnet-5-5 | 59,040 / claude-haiku-5-5 | 52,763 / claude-haiku-5-5 | 75,092 / claude-haiku-5-5 | 16,925 / claude-sonnet-5-5 | 41,840 / claude-sonnet-5-5 | 20,074 / claude-sonnet-5-5 | 53,007 / claude-sonnet-5-5 | 6,115 / claude-sonnet-5-5 | . | . | . | 61,142 / claude-sonnet-5-5 | 74,983 / claude-sonnet-5-5 |

`.` = step not run; `-` = step ran, no transcript matched yet (run `python3 harness.py tokens`). Model = transcript's observed model, else the launch-ledger model, else the model on the step record (never from the step name). AUD/AUD2 are not loop steps.

## Metrics (pooled over completed audits; replicas below)

- n_completed: 6
- n_audits: 12
- BLK_T: 0.25
- audit_fail: 2
- theme_rate: 1
- theme_counts: {'T1': 1, 'T2': 1, 'T3': 0, 'other': 1}
- loop_pass: 4
- growth: 0.04397278534702145
- LOOP_T: 434923.3333333333
- TOK_T: 503192.6666666666
- R_LOOP: 4.33087044265647
- R_B: 2.9692488650758055
- REJ1: 5
- N1: 15
- REJ1_rate: 0.3333333333333333
- replica audit 1 only: DROP (BLK_T 0.5, DROP-4 harm)
- replica audit 2 only: DROP (BLK_T 0.0, DROP-4 harm)

## Final spec per run (input of the 44-defect ledger scoring)

- d5f-r1: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p18/ab5/runs/d5f-r1/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
- d5f-r2: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p18/ab5/runs/d5f-r2/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
- d5f-r3: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p18/ab5/runs/d5f-r3/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
- d5f-r4: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p18/ab5/runs/d5f-r4/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
- d5f-r5: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p18/ab5/runs/d5f-r5/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
- d5f-r6: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p18/ab5/runs/d5f-r6/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md

## Haiku stratum (never pooled; not built in ab5)

{
 "state": "pending"
}

## Design-specific tables (Sonnet)

### Per-theme capture, panel (runs with at least one first review)

| theme | t1b-1 live Sonnet 5.5; used claude-sonnet-5-5 + AC sweep | t2-1 live GPT-6.1 Sol; used claude-haiku-5-5 (stand-in) | t3-1 live GPT-6.1 Terra (likely GLM-5.3 in practice); used claude-haiku-5-5 (stand-in) | t4-1 live GPT-6 Luna; used claude-haiku-5-5 (stand-in) | union (panel) | baseline k=1 |
|---|---|---|---|---|---|---|
| T1 | 5/6 | 3/6 | 3/6 | 2/6 | 5/6 | 6/6 |
| T2 | 5/6 | 1/6 | 3/6 | 2/6 | 6/6 | 2/6 |
| T3 | 5/6 | 4/6 | 3/6 | 3/6 | 5/6 | 3/6 |

| run | t1b-1 | t2-1 | t3-1 | t4-1 | union | lost reviewers | lint findings 1/2/3 | lint by check (lint-1) |
|---|---|---|---|---|---|---|---|---|
| d5f-r1 | FAIL 6 T1,T2,T3 | FAIL 6 T1,T3 | FAIL 3 T1,T2,T3 | FAIL 3 T2,T3 | T1,T2,T3 | - | 0/0/0 | {} |
| d5f-r2 | FAIL 6 T1,T2,T3 | FAIL 3 T3 | FAIL 3 T1,T3 | FAIL 0 - | T1,T2,T3 | - | 0/0/- | {} |
| d5f-r3 | FAIL 6 T1,T2,T3 | FAIL 4 T1,T3 | FAIL 2 T1 | FAIL 0 - | T1,T2,T3 | - | 0/0/0 | {} |
| d5f-r4 | FAIL 7 T1,T2,T3 | FAIL 0 - | FAIL 0 - | FAIL 3 T1,T3 | T1,T2,T3 | - | 0/0/- | {} |
| d5f-r5 | FAIL 5 T1,T2,T3 | FAIL 4 T1,T2,T3 | FAIL 3 T2,T3 | FAIL 6 T1,T2,T3 | T1,T2,T3 | - | 0/0/- | {} |
| d5f-r6 | FAIL 0 - | FAIL 0 - | FAIL 2 T2 | FAIL 0 - | T2 | - | 0/0/- | {} |

Cells: verdict, blocking count, themes. t1b-1 carries the ab4 acceptance-criteria sweep sentence; the other three have the plain brief.

### Merged-finding count

| run | raw | merged | dedup ratio |
|---|---|---|---|
| d5f-r1 | 15 | 3 | 0.20 |
| d5f-r2 | 13 | 2 | 0.15 |
| d5f-r3 | 15 | 3 | 0.20 |
| d5f-r4 | 15 | 3 | 0.20 |
| d5f-r5 | 18 | 2 | 0.11 |
| d5f-r6 | 12 | 2 | 0.17 |

### ADJ (PN1 adjudicator, measurement only) vs VF1

| run | merged | ADJ confirmed | rejected | unsure | VF1 confirmed | agree (confirm/other) | parse_ok |
|---|---|---|---|---|---|---|---|
| d5f-r1 | 17 | 3 | 11 | 3 | 2 | 16/17 | True |
| d5f-r2 | 10 | 2 | 7 | 1 | 2 | 10/10 | True |
| d5f-r3 | 24 | 2 | 21 | 1 | 2 | 22/24 | True |
| d5f-r4 | 19 | 2 | 14 | 3 | 2 | 17/19 | True |
| d5f-r5 | 18 | 2 | 14 | 2 | 1 | 17/18 | True |
| d5f-r6 | 26 | 3 | 21 | 2 | 1 | 24/26 | True |

### Verifier

| run | step | sent | confirmed | rejected | parse_ok |
|---|---|---|---|---|---|
| d5f-r1 | VF1 | 3 | 2 | 1 | True |
| d5f-r1 | VF2 | 2 | 2 | 0 | True |
| d5f-r1 | VF3 | 2 | 1 | 1 | True |
| d5f-r2 | VF1 | 2 | 2 | 0 | True |
| d5f-r2 | VF2 | 1 | 0 | 1 | True |
| d5f-r3 | VF1 | 3 | 2 | 1 | True |
| d5f-r3 | VF2 | 1 | 1 | 0 | True |
| d5f-r3 | VF3 | 1 | 1 | 0 | True |
| d5f-r4 | VF1 | 3 | 2 | 1 | True |
| d5f-r4 | VF2 | 2 | 0 | 2 | True |
| d5f-r5 | VF1 | 2 | 1 | 1 | True |
| d5f-r6 | VF1 | 2 | 1 | 1 | True |
| d5f-r6 | VF2 | 1 | 0 | 1 | True |

pooled rejection rate over all VF steps: 10/25

### Noted, unactioned vs audits

| run | step | id | theme | verifier reason | matched audit blocker | eyeball |
|---|---|---|---|---|---|---|
| d5f-r1 | VF1 | L3 | other | The regex matches only lowercase `orca` or `orca-ide` followed by orchestration, | none | (eyeball) |
| d5f-r1 | VF3 | L2 | other | not in confirmed line | none | (eyeball) |
| d5f-r2 | VF2 | L1 | other | The two texts do not contradict, because WC-9 turns off every install under `--u | none | (eyeball) |
| d5f-r3 | VF1 | L23 | other | Section 1.4 states plainly that the PR #329 run proves only the nested route and | none | (eyeball) |
| d5f-r4 | VF1 | L2 | other | The AC-C1 pattern matches only command-shaped text (`orca orchestration`, `orca  | none | (eyeball) |
| d5f-r4 | VF2 | L1 | other | WC-4 and AC-1.2 both key the contract location to a flag the row names. These ro | none | (eyeball) |
| d5f-r4 | VF2 | L12 | other | The existing rule is keyed on `claude --print`, and the candidate says Orca does | none | (eyeball) |
| d5f-r5 | VF1 | L2 | other | The candidate does not say the allowed example is written as `orca orchestration | none | (eyeball) |
| d5f-r6 | VF1 | L3 | other | The scope mismatch is real, but AC-C1 is a case-sensitive lowercase regex requir | none | (eyeball) |
| d5f-r6 | VF2 | L1 | other | not in confirmed line | none | (eyeball) |

## Theme tags to eyeball

- d5f-r1 R1.t1b-1 F1 T2 :: ### F1 | MAJOR | blocking | WC-4's contract path cannot be formed for file-valued or fixed output lo
- d5f-r1 R1.t1b-1 F2 T2 :: ### F2 | MAJOR | blocking | WC-4's contract location contradicts the adversarial and workflow rows |
- d5f-r1 R1.t1b-1 F3 T3 :: ### F3 | CRITICAL | blocking | AC-0.4 cannot pass at Phase 0 | Wiegers, Crispin | priority High
- d5f-r1 R1.t1b-1 F4 T1 :: ### F4 | MAJOR | blocking | `/sc:load` is required to have a contract and has none | Wiegers, Adzic 
- d5f-r1 R1.t1b-1 F5 other :: ### F5 | MAJOR | blocking | AC-2.2 cannot pass for six of the fifteen P2 commands | Adzic, Crispin |
- d5f-r1 R1.t1b-1 F6 T1 :: ### F6 | MAJOR | blocking | P1 ships `--unattended` on commands whose gates and outward defaults it 
- d5f-r1 R1.t2-1 F1 other :: ### F1 (blocking, MAJOR): AC-C1 cannot fail
- d5f-r1 R1.t2-1 F2 T3 :: ### F2 (blocking, MAJOR): SA-2 allows what AC-C1 forbids
- d5f-r1 R1.t2-1 F3 T3 :: ### F3 (blocking, MAJOR): `--unattended` is required in briefs before the flag exists
- d5f-r1 R1.t2-1 F4 other :: ### F4 (Medium, graded MAJOR): default output paths collide
- d5f-r1 R1.t2-1 F5 T1 :: ### F5 (Medium, graded MAJOR): no heartbeat rule for fan-out commands
- d5f-r1 R1.t2-1 F6 other :: ### F6 (Medium, graded MINOR): the evidence statement contradicts itself on the route observed
- d5f-r1 R1.t3-1 F1 T3 :: ### F1 (CRITICAL, blocking): AC-0.4 requires a check that P0 cannot pass
- d5f-r1 R1.t3-1 F3 T1 :: ### F3 (MAJOR, blocking): AC-1.1 requires a contract name that the load row removes
- d5f-r1 R1.t3-1 F4 T2 :: ### F4 (MAJOR, blocking): WC-4 defines `<output-dir>` as a directory, but the briefs pass files
- d5f-r1 R1.t4-1 F1 T3 :: **F1 (blocking, contradiction).** Section 2.3 says each brief carries "the exact command line includ
- d5f-r1 R1.t4-1 F2 other :: **F2 (blocking, unpassable check).** SA-2 allows one mention of Orca in a changed file, "as an examp
- d5f-r1 R1.t4-1 F3 T2 :: **F3 (blocking, contradiction).** Section 2.3 says the output directory makes "the report path known
- d5f-r2 AUD F-01 other :: ### F-01 (MAJOR, graded blocking) cli-portify can never reach a succeeded end state
- d5f-r2 R1.t1b-1 F1 T1 :: ### F1 (blocking, MAJOR): AC-1.1 and AC-1.2 cannot pass for `/sc:load`
- d5f-r2 R1.t1b-1 F2 T1 :: ### F2 (blocking, MAJOR): P1 and AC-1.1 touch pr-submit, post-release and implement before D2-D4
- d5f-r2 R1.t1b-1 F3 T3 :: ### F3 (blocking, CRITICAL): AC-0.4 cannot pass at P0, so no later phase can start
- d5f-r2 R1.t1b-1 F4 T2 :: ### F4 (blocking, MAJOR): WC-4's contract path contradicts the adversarial and workflow rows
- d5f-r2 R1.t1b-1 F5 T2 :: ### F5 (blocking, MAJOR): `<output-dir>` is undefined where `--output` is a file or the command has 
- d5f-r2 R1.t1b-1 F6 other :: ### F6 (blocking, MAJOR): AC-2.2 cannot pass for 6 of the 15 P2 commands
- d5f-r2 R1.t2-1 B1 other :: ### B1. WC-3 lets a blocked gate be answered by the coordinator, which contradicts section 3.2 and D
- d5f-r2 R1.t2-1 B2 other :: ### B2. AC-C1 cannot fail as written, so the "no Orca calls in commands" check passes vacuously (blo
- d5f-r2 R1.t2-1 B3 T3 :: ### B3. Section 2.3 requires `--unattended` in every brief, but the P0 smoke runs use commands that 
- d5f-r2 R1.t3-1 F1 T3 :: ### F1. BLOCKING. MAJOR. Unpassable check. Expert: Wiegers (testability)
- d5f-r2 R1.t3-1 F2 other :: ### F2. BLOCKING. MAJOR. Contradiction, safety boundary (outward actions). Expert: Wiegers, with Nyg
- d5f-r2 R1.t3-1 F3 T1 :: ### F3. BLOCKING. MAJOR. Contradiction. Expert: Fowler (interface scope)
- d5f-r3 R1.t1b-1 F1 T1 :: ### F1 CRITICAL, blocking: AC-1.1 and AC-1.2 require a contract file from `/sc:load`, which the spec
- d5f-r3 R1.t1b-1 F2 T2 :: ### F2 CRITICAL, blocking: the WC-4 contract path and the adversarial row name two different files
- d5f-r3 R1.t1b-1 F3 T2 :: ### F3 CRITICAL, blocking: WC-4 derives the contract path from a directory, but tdd and init-lite ta
- d5f-r3 R1.t1b-1 F4 other :: ### F4 MAJOR, blocking: AC-2.2 requires a blocked outcome from six P2 commands whose gates never res
- d5f-r3 R1.t1b-1 F5 other :: ### F5 MAJOR, blocking: AC-2.3 asks for a succeeded happy path from `/sc:cli-portify`, whose three g
- d5f-r3 R1.t1b-1 F6 T3 :: ### F6 MAJOR, blocking: AC-0.4 says steps 1-3 pass in P0 but step 3 needs the WC-4 contract that P0 
- d5f-r3 R1.t2-1 F1 T3 :: ### F1 (blocking): AC-0.4 step 4 cannot pass for two of its three smoke commands
- d5f-r3 R1.t2-1 F2 T1 :: ### F2 (blocking): section 3.1 says only fixes change ready commands; P1 and AC-1.1 require the flag
- d5f-r3 R1.t2-1 F3 T1 :: ### F3 (blocking): `/sc:load` is required to write a contract and is also said to write none
- d5f-r3 R1.t2-1 F4 other :: ### F4 (blocking): the AC-C1 grep never matches, so the SA-2 and WC-8 gate passes any violation
- d5f-r3 R1.t3-1 F1 T1 :: **F1 (blocking, MAJOR, unpassable-check).** `.dev/orca-command-refactor/specs/orca-worker-contract-s
- d5f-r3 R1.t3-1 F2 T1 :: **F2 (blocking, MAJOR, contradiction).** SA-3 at `:148` says a standalone default run "writes the sa
- d5f-r4 R1.t1b-1 F1 T3 :: ### F1. AC-0.4 requires 7.2 step 3 to pass in Phase 0, but step 3 needs a WC-4 contract that Phase 0
- d5f-r4 R1.t1b-1 F2 T2 :: ### F2. WC-4 puts the contract at `<output-dir>/return-contract.yaml` for a coordinator-passed direc
- d5f-r4 R1.t1b-1 F3 T2 :: ### F3. WC-6 says each run goes into a fresh output directory; WC-4 and 2.3 fix one coordinator-pass
- d5f-r4 R1.t1b-1 F4 T1 :: ### F4. AC-1.1 requires an `## Unattended mode` section in every command of 3.1-3.2 at Phase 1, whic
- d5f-r4 R1.t1b-1 F5 T1 :: ### F5. `/sc:load` is in the P1 checks (AC-1.1, AC-1.2) but its own row gives it no report, no contr
- d5f-r4 R1.t1b-1 F6 other :: ### F6. AC-2.2 requires `outcome failed` and `status: blocked` for every P2 command, but six P2 rows
- d5f-r4 R1.t1b-1 F7 other :: ### F7. AC-2.3 expects a succeeded happy path for `/sc:cli-portify`, but its row resolves all three 
- d5f-r4 R1.t4-1 F1 other :: **F1. AC-C1 cannot fail.** Spec line 172 writes the alternation as `(orchestration\|worktree\|termin
- d5f-r4 R1.t4-1 F2 T1 :: **F2. Brainstorm and init-lite have no phase, and AC-1.1 needs their section.** Section 3.1 lists br
- d5f-r4 R1.t4-1 F3 T3 :: **F3. AC-0.4 requires a P1 artifact in P0.** AC-0.4 says steps 1-3 and 5-7 pass in P0 and that step 
- d5f-r5 R1.t1b-1 F1 T3 :: ### F1 (CRITICAL, blocking): AC-0.4 requires a WC-4 contract that Phase 0 has not built
- d5f-r5 R1.t1b-1 F2 T2 :: ### F2 (CRITICAL, blocking): WC-4 puts the contract in a directory the coordinator passed, but sever
- d5f-r5 R1.t1b-1 F3 T2 :: ### F3 (CRITICAL, blocking): the adversarial and workflow contract locations contradict WC-4's locat
- d5f-r5 R1.t1b-1 F4 T1 :: ### F4 (CRITICAL, blocking): AC-1.1 and AC-1.2 require `/sc:load` to carry a contract; the spec says
- d5f-r5 R1.t1b-1 F5 other :: ### F5 (CRITICAL, blocking): AC-2.2 demands a `blocked` result from commands that have no blocked pa
- d5f-r5 R1.t2-1 F1 T3 :: ### F1 (blocking): AC-0.4 cannot pass as written
- d5f-r5 R1.t2-1 F2 T1 :: ### F2 (blocking): the Unattended-section scope contradicts section 3.1 and AC-1.1
- d5f-r5 R1.t2-1 F3 T2 :: ### F3 (blocking): the contract file path is defined two ways
- d5f-r5 R1.t2-1 F4 T3 :: ### F4 (blocking): the Orca-free core rule forbids what SA-2 and P0 require
- d5f-r5 R1.t3-1 F1 T3 :: ### F1: AC-0.4 cannot pass as written (blocking)
- d5f-r5 R1.t3-1 F2 other :: ### F2: AC-C1 never matches, and would conflict with SA-2 once fixed (blocking)
- d5f-r5 R1.t3-1 F3 T2 :: ### F3: AC-1.2 cannot be run on /sc:workflow, and WC-4 gives it no contract path (blocking)
- d5f-r5 R1.t4-1 F1 T3 :: **F1. An acceptance check cannot pass as written (AC-0.4 step 4).** MAJOR, blocking. Expert: Wiegers
- d5f-r5 R1.t4-1 F2 T1 :: **F2. Brainstorm and init-lite are not scheduled, but the phase scope and AC-1.1 require them.** MAJ
- d5f-r5 R1.t4-1 F3 T1 :: **F3. `/sc:load` must write a report in AC-1.1 but is decided not to write one.** MAJOR, blocking. E
- d5f-r5 R1.t4-1 F4 T3 :: **F4. The core-file grep forbids what SA-2 allows.** MAJOR, blocking. Expert: Fowler (lead: boundary
- d5f-r5 R1.t4-1 F5 T2 :: **F5. A retry of init-lite overwrites the first attempt's report (data loss).** MAJOR, blocking. Exp
- d5f-r5 R1.t4-1 F6 other :: **F6. The worker contract can route a coordinator answer into the implement Ruling (safety boundary)
- d5f-r6 AUD F-01 T1 :: ### F-01 Phase 1 scope, AC-1.1, the `load` row and the Phase 4 deferral contradict each other (MAJOR
- d5f-r6 AUD F-02 T2 :: ### F-02 WC-4's single contract path contradicts the adversarial row, and the coordinator checks the
- d5f-r6 R1.t3-1 F1 other :: ### F1 (blocking): init-lite re-run is in-place, but WC-6 requires a fresh directory
- d5f-r6 R1.t3-1 F2 T2 :: ### F2 (blocking): standalone `/sc:workflow` would write a new contract file, which SA-3 forbids

## Theme overrides applied

none

