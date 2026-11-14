# Step 3: position-bias disagreements to re-evaluate (14 criterion-variant pairs)

## Dimension 1 criterion C1 variant V1

- Pass 1 (forward) line: | C1 | V1 covers R-a to R-e for #409 and PR #539 | "Result: 39 claims checked"; "Smallest change" column per finding; "Missing for integration"; Verdict "NOT YET INTEGRABLE as written, but compatible in direction" | MET |
- Pass 2 (reverse) line: | C1 | Covers all explicit requirements from the source input | Sources validated ("Claim check of the new #409 body", 39 claims); action per point ("Smallest change" column, W-1..W-7); dependencies ("Missing for integration", 10 items); issue and PR coverage (#409, #539, #541, #532, #339, #534, #423, #444, #450, Coder#477); alignment verdicts (F-01..F-18, A-01..A-15). The built observer is absent: C-03 "No observer code exists; 20 synthetic designs await a human choice (L16)" is marked "Verified"; `round2-rebuttal-V1.md` row 1: "'No observer exists' is false ... Concede in full" | NOT MET |

## Dimension 1 criterion C1 variant V3

- Pass 1 (forward) line: | C1 | V3 covers R-a to R-e for Coder#477 | Claim-check table of 8 paths plus related-issue claims; F1..F17; Edits 1..12; "What IronClaude must supply or wait for" | MET |
- Pass 2 (reverse) line: | C1 | Covers all explicit requirements from the source input | Sources validated ("Claim check of Coder#477", 8 paths plus related issues); best action per point (Edits 1-12, Q1-Q7); dependencies ("What IronClaude must supply or wait for", 7 items); issue and PR coverage (Coder#477, #331, #450, #339, #409, PR #539); alignment verdicts (F1-F17). But the TUI-observer half is judged from the #409 draft only: scope read says of #409 "only checked that its live body contains 'Coder#477'", and `round2-rebuttal-V3.md` row 6 concedes "V3 never checked that a built observer exists or what 'TUI Panel' means" (V5 #6) | NOT MET |

## Dimension 1 criterion C1 variant V4

- Pass 1 (forward) line: | C1 | V4 covers R-a to R-e for #423 | "Claim check of #423" C1..C11; F1..F22; "Results of the four proposals"; Proposed edits for #423, #339, #409 | MET |
- Pass 2 (reverse) line: | C1 | Covers all explicit requirements from the source input | Sources validated (C1-C11 claim check), action per point ("Proposed edits" for #423, #339, #409), dependencies (F12), issue and PR coverage (#423, #339, #444, #534, #450, PR #539, Coder#477), alignment verdicts (F1-F22). But the observer half is judged only from the #409 body: the "Scope read" table lists no observer code, PR #503 or PR #514, and "(b) ... HOLDS" rests on "#409 already states it (Alignment decision 8)". `round2-rebuttal-V4.md` row 1: "Concede in full ... Edit 3 is withdrawn", `ls src/superclaude/cli/` shows `observe`. The "alignment with the TUI observer" requirement is not met | NOT MET |

## Dimension 1 criterion C4 variant V5

- Pass 1 (forward) line: | C4 | Completion criteria defined | D1 "Contract content: names ...; join key (`dispatchId` ... `row_id` minus `orca:`); who owns which fact; one word list ..."; each D has a "Smallest reversible first step" | MET |
- Pass 2 (reverse) line: | C4 | Defines success or completion criteria | Searched "Integration decisions", "Verdict", "Dependencies". Only "Smallest reversible first step" per decision and a re-test of the #409 acceptance criteria (A-01..A-07); the variant never says when the alignment work is done or what would pass | NOT MET |

## Dimension 2 criterion K1 variant V2

- Pass 1 (forward) line: | K1 | V2 has no disproved factual claims | W-01 default `worktree` level confirmed (SC-3: `issue.md:43,88`, `launch.py:33`); W-06 confirmed (SC-5); orchestrator absence confirmed (SC-6). R2-V2 concessions are scope and stale `/tmp` cites only: "a scope choice, not a defence" | MET |
- Pass 2 (reverse) line: | K1 | No factual errors or hallucinated claims | `round2-rebuttal-V2.md` section 1 withdraws: row 1 W-10 "observer reader" (the built observer has no watcher input); row 6 "absent by construction" for the Run record (inference, not proof); row 7 cites by line into a `/tmp` scratch copy of #409; row 4 W-05's mislabel claim depends on `session_join`, which V2 did not run | NOT MET |

## Dimension 2 criterion K1 variant V3

- Pass 1 (forward) line: | K1 | V3 has no disproved factual claims | Claim-check table (5 of 8 paths omit `image/`) confirmed SC-4; F1 confirmed SC-5. Disproved items are proposals, not stated facts (see K2). Residual: stale `/tmp` line cites conceded in R2-V3 item 3 (citation drift, not a wrong fact) | MET |
- Pass 2 (reverse) line: | K1 | No factual errors or hallucinated claims | `round2-rebuttal-V3.md` section 1 concedes: row 1 Edit 5 "produced without any write" is false for `sweep run` (it writes a report; a sidecar JSON breaks `test_readonly.py:400`); row 2 Edit 8 omits the second governed agent of `/sc:issue --claim`; row 3 all `i409-new-body.md:NN` cites are to a stale scratch copy, not the live #409 body | NOT MET |

## Dimension 2 criterion K2 variant V5

- Pass 1 (forward) line: | K2 | Proposed approach is feasible | D1(a) "keep them separate and write one contract"; first step "one short relationship note, linked from `docs/designs/orchestrator-mode.md` section 1"; D5 option (ii) needs only one owner sentence | MET |
- Pass 2 (reverse) line: | K2 | Technical approaches feasible with stated constraints | F-03 says "`<stem>.json` beside the report still has to be written by the sweep"; Round 2 row 7 withdraws it: design line 128 "a successful run never leaves two files (NFR-001)", `tests/sweep/test_readonly.py:300`, `test_cli_contract.py:1474` pin one report file. D5 recommendation (ii) "any Run the terminal holds" withdrawn (row 8: the Run named in the pass record is the coordinator's live Run, consumption unproven) | NOT MET |

## Dimension 2 criterion K4 variant V2

- Pass 1 (forward) line: | K4 | No internal contradictions | W-13/W-14 "aligned" sit beside W-01/W-06 "contradiction" on different points; verdict repeats the same two contradictions | MET |
- Pass 2 (reverse) line: | K4 | No internal contradictions | Fact 2 asserts "So the session has no Run and no Dispatch row" and W-04 says "Run binding is absent by construction", while the same fact 2 says "UNVERIFIED: that Orca writes no Run record at all" and W-04 asks to "Mark the sweep's 'no Run' statement in #409 item 9 UNVERIFIED until then" (it applies to #409 a standard it does not apply to its own claim) | NOT MET |

## Dimension 4 criterion L1 variant V2

- Pass 1 (forward) line: | L1 | Language is unambiguous | Fact 4: "so a registered watcher worktree is very likely scanned" is a hedge on the premise that W-05 builds on, with no UNVERIFIED label at that point | NOT MET |
- Pass 2 (reverse) line: | L1 | Unambiguous language | "Recommended: change the fixed prompt to `/sc:issue --claim <N> --pipeline none` (claim ends after the comments, no worktree, no agent: exactly decision D2)"; uncertain items carry "UNVERIFIED" | MET |

## Dimension 4 criterion L4 variant V1

- Pass 1 (forward) line: | L4 | Terms defined on first use | Defines "Body" and "UNVERIFIED" only. `WC-16`, `FIN-F7`, `D-05`, `SP-22`, `FR-012`, `Attention Ledger` are used without definition. Searched: Conventions line, tables C-10, C-24, F-05 | NOT MET |
- Pass 2 (reverse) line: | L4 | Acronyms and domain terms defined on first use | Conventions define "Body" and "UNVERIFIED"; the ten dimensions are enumerated in F-02; "WC-16 is a cap (at most once per 5 minutes) on coordinator wakes" (F-12); "SP-22: person deletes by hand" glossed; stray ids ("FIN-F7", "D-05 to D-12") sit in citation cells | MET |

## Dimension 4 criterion L4 variant V2

- Pass 1 (forward) line: | L4 | Terms defined on first use | `OB-H1`, `OB-H2`, `OB-H3`, `FU-1`..`FU-6`, `D2`, `W-ENFORCEMENT-ABSENT` used without definition (FU-1 and WC-13 get a short gloss; the OB-H gate does not). Searched: W-02, W-08, Proposed edits | NOT MET |
- Pass 2 (reverse) line: | L4 | Acronyms and domain terms defined on first use | Most are glossed where they appear ("FU-1 live test (a claim on a test issue)", "the claim's own ship gate ... OB-H1 item 1, OB-H2 and OB-H3", "path A ... path B" defined in W-03); stray ids ("T-10", "FU-6", "#315 problem") are peripheral | MET |

## Dimension 4 criterion L4 variant V3

- Pass 1 (forward) line: | L4 | Terms defined on first use | `AC1`..`AC5`, `NFR22`, `D1 option A`, `FU-1`, `heartbeat collector` used without definition; F3 explicitly says "the monitor" is undefined in the source | NOT MET |
- Pass 2 (reverse) line: | L4 | Acronyms and domain terms defined on first use | Options and gates are glossed inline ("D1 option A 'No listener, inbound port or address registry'", "bypass mode ... holds each message"); stray unglossed ids ("FU-1", "FU-2", "NFR22", "R9") are peripheral | MET |

## Dimension 4 criterion L4 variant V4

- Pass 1 (forward) line: | L4 | Terms defined on first use | `WC-3`, `WC-9`..`WC-16`, `GQ-109`, `INV-005`, `NFR`-style tags used without definition (F22 discusses the word "Orchestrator" but not these). Searched: scope table, F5, F7, F16 | NOT MET |
- Pass 2 (reverse) line: | L4 | Acronyms and domain terms defined on first use | Most are glossed inline ("WC-12 (`:61`, pulled not pushed)", "WC-13 (`:62`, a worker may not start workers or open sessions)", "WC-16 ... only on PR #539"); stray unglossed ids remain ("GQ-109", "INV-005", "Rule 4(a)", "Collision Lens") but they are not load-bearing | MET |

## Dimension 5 criterion R5 variant V4

- Pass 1 (forward) line: | R5 | Monitoring or validation mechanism | No evidence found: the added acceptance criteria are design-time statements ("The design names ...") with no runtime or test mechanism to detect the risks. Searched: AC list, F14, Proposed edits | NOT MET |
- Pass 2 (reverse) line: | R5 | Monitoring or validation mechanism | Proposed AC list is the validation mechanism for the future design; F6 "v2 prerequisite: the #534 live read-only capture (restores Rule 5 and Rule 4(a))"; F21 re-checks that v1 holds no v2 logic with `ls` | MET |
