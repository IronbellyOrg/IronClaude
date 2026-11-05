# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2, plus Round 2.5 (invariant probe) and one invariant-gate resolution round
- Convergence achieved: 94.7% (18 of 19 diff points)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 2 (Variant 1 = reviewer-1 card, analyzer persona; Variant 2 = reviewer-2 card, qa persona; both run on the orchestrator's default model, Mode A)
- Weighting: blind-calibrated confidence (V1 C = 0.75, V2 C = 0.77), not self-reported (0.80 / 0.82)
- Round 3: skipped (depth=standard)
- Constraint note: the Variant 2 advocate disclosed that it ran `mkdir -p /tmp/x` once, a write outside the repo and outside the output directory, against its read-only brief. Nothing in the repo changed. The orchestrator did not remove it, because removing it would also be a write outside `--output`.

## Round 1: Advocate Statements

### Variant 1 Advocate (reviewer-1 card)
- Position: real executability defects. After applying the plan:29 pull-forward Constraint, most IMPORTANT ratings fall to MINOR. C-004 (Task 18 sandbox rg) and C-005 (`CLAUDE_CONFIG_DIR`) stay IMPORTANT.
- Steelman of V2: checks what the plan claims to prove. Task 18 claims DoD-3 (plan:243) but seeds two files (plan:248) against DoD-3's "old core files" (source.md:269). §2.1 "Historical `.dev/` artifacts stay untouched" (source.md:261) and the §2.3 leftovers appear in no Constraint.
- Positions: C-001 MINOR, C-002 MINOR, C-003 MINOR, C-004 IMPORTANT, C-005 IMPORTANT, C-006 to C-009 MINOR, C-010 MINOR (ledger half only), C-011 MINOR (V2 wins), C-012 MINOR merged into the C-004 fix (V2 wins), X-001 merge, A-001 QUALIFY, A-002 QUALIFY, A-003 ACCEPT (`install_core.py:65-70`, `install_skill.py:47-52`, `update.sh:8`).
- Weaknesses in V2: R2-F2's "can therefore pass" is false; V2 misses `CLAUDE_CONFIG_DIR`; R2-F1's fix as worded would forbid the plan's own new `.dev/codegraph-migration/handoffs/` writes; V2 has no executability coverage.
- Concessions: R1-F1 is overstated (only `contract.py:30` and `reflection-rubric.md:127` lie outside the Task 11/12 files, and plan:167 already deletes the M8 calls). F2, F3, F6, F7 and F8 heal themselves under plan:29. R1-F3's extra rg is redundant (`_native_` already matches). R1-F10's main.py half is redundant (Task 6's cbm search covers it). Excluding `claude-calls.log` is speculative. R1-F5 is conditional (`CLAUDE_CONFIG_DIR` is unset here).

### Variant 2 Advocate (reviewer-2 card)
- Position: V1 found more real defects. R2-F2 is still a valid DoD-coverage gap, but its "can pass" wording is wrong. R2-F1 should be narrowed. R1-F4 and R2-F2 together make the Task 18 fix.
- Steelman of V1: it runs each acceptance command against file state at task end, which is the right test given plan:29 ("A task may not need a later task to go green"). All citations are grounded.
- Positions: C-001 MINOR (both), C-002 MINOR, C-003 IMPORTANT (spec-inherited, source.md:334), C-004 IMPORTANT, C-005 IMPORTANT, C-006 to C-009 MINOR, C-010 MINOR (ledger half), C-011 MINOR narrowed, C-012 MINOR merged, X-001 split verdict, A-001 QUALIFY ("blocked becomes reordered"), A-002 QUALIFY (same execution severity; deviation class differs; applies to C-002, C-003, C-004, C-012), A-003 ACCEPT.
- Weaknesses in V1: R1-F1 is overstated; severities ignore plan:29; V1 never marks spec-inherited defects; R1-F4's allowlist alone makes DoD-3 vacuous; half of R1-F10 is redundant.
- Concessions: R2-F2's "can pass" is false; R2-F1 overstates (plan:26 already blocks real-HOME installs, user-data deletion and other-repo edits); V2 missed F3, F4, F5, F8, F9 and the F10 ledger half; the practical risk behind R2-F2 is low.
- Proposed merged Task 18 fix: `CLAUDE_CONFIG_DIR` on every `env`; seed a stale `CLAUDE.md` and `commands/sc/reflect.md`; filter through the §2.4 allowlist; exclude `claude-calls.log`.

## Round 2: Rebuttals

### Variant 1 Advocate
- C-003 raised to IMPORTANT. Both literal readings of "replacing" fail. (1) Deleting the helper breaks `uninstall_codebase_memory_mcp` (`install_mcp.py:993`, `:999`), so the tavily tests at about :885-1008 fail. (2) Rewiring to the new remover also fails: the tests record calls through a patched run function (`tests/cli/test_install_mcp_tavily.py:426-430`, which asserts timeout ≤ 60) reached via `_run_registration_command` (`install_mcp.py:766-769`), while the spec's new direct-exec wrapper bypasses it (source.md:335), so the call-list assertions at :926-929 and :943-945 break. The orchestrator confirmed the fixture and the assertions. The only correct fix is to keep the old helper until Task 5.
- Accepts V2's Task 18 fix with amendments: (a) a line-level filter for installed paths, because ALLOW (source.md:621) is anchored to repo paths; (b) `CLAUDE_CONFIG_DIR` equal to the sandbox HOME (`install_mcp.py:731-736`); (c) keep the seeds, because `--force` overwrites them (`install_core.py:65-70`).
- Accepts the narrowed C-011 wording, provided it says "historical", and the spec-inherited tags.

### Variant 2 Advocate
- Accepts amendments (a)-(c) and adds: `CLAUDE_CONFIG_DIR` must never be empty (`install_mcp.py:731-732` returns "unknown" for an empty value).
- C-005 stays a separate finding (real-config mutation, a different defect class from a false-failing check) but shares the Task 18 edit.
- X-001 resolved: V1 is right about the literal outcome, V2 about what the check proves.

## Round 2.5: Invariant Probe
See `invariant-probe.md`: 9 findings; HIGH and UNADDRESSED: INV-001, INV-002. CONVERGENCE BLOCKED.

## Invariant-gate resolution
The orchestrator re-verified both blockers before the round. `rg -l --no-ignore -i serena .` lists 0 `/.serena/` paths, with `--hidden` it lists 2, and with the explicit root it lists 2. `install_hooks.py:293-297` and `install_user_setup.py:81-89` both `copy2` to `settings.json.bak.<%Y%m%dT%H%M%SZ>`.

| INV | V1 | V2 | Outcome |
|---|---|---|---|
| INV-001 | ACCEPT. Concedes that the `$T/fresh` half of R1-F4 had the direction wrong: it passes vacuously, it does not fail | ACCEPT | ADDRESSED. Folded into C-004: `rg -n -i --hidden --no-ignore` on both sandbox searches |
| INV-002 | ACCEPT | ACCEPT | ADDRESSED. Folded into C-004: filter `settings\.json\.bak\.[0-9]{8}T[0-9]{6}Z:`, assert at least one backup exists, never delete it |
| INV-005 | QUALIFY. MINOR, same Task 13 rows P78/P79/P80/P86, only the line lists are missing | ACCEPT | Folded into C-006 (MINOR) |
| INV-006 | ACCEPT | QUALIFY. :129 stays only if its step reference is retitled | Folded into C-006 with per-line actions and a G8 note for `onboarding_status` |
| INV-007 | ACCEPT | ACCEPT | Folded into C-011 wording and C-010 (stage exact file paths) |

After this round no HIGH item is UNADDRESSED, so the gate is cleared.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 | L1 | Variant 1 | 75% | Self-audit and line remap made the findings checkable; V2 agreed |
| S-002 | L1 | unresolved | 50% | V1 says single-line cites are better; V2 says style changes nothing |
| C-001 | L3 | Variant 1 (narrowed) | 90% | Both agree MINOR; only `contract.py:30` and `rubric.md:127` lie outside the Task 11/12 files |
| C-002 | L2 | Variant 1 | 90% | Both agree MINOR, spec-inherited (spec T9 has the same rg) |
| C-003 | L2 | Variant 1 | 95% | Both agree IMPORTANT after Round 2; both readings break the tavily tests |
| C-004 | L3 | Variant 1 (corrected) | 95% | Both agree IMPORTANT; the `$T/fresh` half corrected by INV-001; plus INV-002 |
| C-005 | L3 | Variant 1 | 90% | Both agree IMPORTANT, separate; latent here (unset) |
| C-006 | L3 | Variant 1 | 90% | Both agree MINOR (V1 conceded down from IMPORTANT); absorbs INV-005 and INV-006 |
| C-007 | L2 | Variant 1 | 95% | Agreed MINOR |
| C-008 | L3 | Variant 1 | 95% | Agreed MINOR |
| C-009 | L2 | Variant 1 | 95% | Agreed MINOR |
| C-010 | L2 | Variant 1 (ledger half) | 90% | Agreed MINOR; main.py half dropped |
| C-011 | L2 | Variant 2 (narrowed) | 90% | Agreed MINOR; INV-007 wording |
| C-012 | L3 | Variant 2 | 90% | Agreed MINOR, spec-inherited |
| C-013 | L2 | both | 80% | Complementary emphases |
| X-001 | L3 | both | 90% | V1 right on the outcome for `$T/old`; V2 right that the filtered check proves nothing without seeds |
| A-001 | L3 | both (QUALIFY) | 85% | Pull-forward heals in-task defects but not C-004 or C-005 |
| A-002 | L2 | both (QUALIFY) | 85% | Same execution severity; deviation class "spec-inherited"; add a spec errata note |
| A-003 | L3 | both (ACCEPT) | 95% | Verified in `install_core.py`, `install_skill.py`, `install_commands.py`, `update.sh:8` |

## Convergence Assessment
- Points resolved: 18 of 19
- Alignment: 94.7%
- Threshold: 80%
- Taxonomy gate: L1 (2 points), L2 (8), L3 (9), so every level is covered
- Invariant gate: blocked once (INV-001, INV-002), cleared after the resolution round; MEDIUM INV-005 and INV-006 folded into C-006
- Status: CONVERGED
- Unresolved points: S-002 (L1, cosmetic; no effect on any finding)
