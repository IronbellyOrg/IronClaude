# Refactor Plan Review (Step 4)

Abbreviations: A is the folder `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/adversarial/`. TL is the tasklist `TASK-RF-sweep-phase1-20261108-072653.md`. DESIGN is `docs/designs/orchestrator-mode.md`. CAL is a card's blind calibration block. Reviewed file: `A/refactor-plan.md` (25 changes, register F-01 to F-23).

## Verdict

FAIL. Two blocking findings: B-1 (F-03, Change 3: the preferred fix cannot do what step (6) needs) and B-2 (F-10, Change 10: the finding rests on a claim the tasklist disproves, and it is neither calibrated nor labelled probe-sourced). Everything else passes. Calibration, de-duplication of the owner-gate sites, the INV-001 and INV-002 mappings, and the "not being made" table are sound.

## Checks

### Check 1: Calibration. PASS

- No finding in any CAL block has holds=no, so there was nothing to drop. The plan drops none of the real findings.
- Every holds=yes or holds=partly finding is carried. Three findings are deliberately not carried as findings: R1-G5, R3-G9 and R3-G10. Each is a confirmation (R1-G5's recommendation reads "No plan change needed"), and the base-selection and the debate (S-007, C-011) treat them as confirmations. That is justified.
- Severities match the calibrated ones. HIGH is R2-G3, R2-G5, R2-G7 (F-01 to F-03). MEDIUM is R1-G3, R2-G1, R2-G6, R2-G8, R2-G10, R3-G4. LOW is the other 13. R2-G2 (calibrated MEDIUM) is merged into the HIGH F-01, and a merge keeps the higher severity, which is allowed.
- No register severity is above its calibrated value without debate evidence, except F-10, which has no CAL at all (see B-2).
- F-12 stays LOW although INV-015 (the probe item that widens its fix) is MEDIUM. This widens the fix scope and is not a new finding, so it is a minor note only (M-3).

### Check 2: De-duplication and affected items. PASS

- F-01 names every owner-gate site: TL:989 (6.2), TL:1140 (shared procedure), TL:1151, 1165, 1179, 1193, 1207, 1221 (the six inline copies in 7.2, 7.4, 7.6, 7.8, 7.10, 7.12), TL:1242 (7.15, INV-002), TL:2481 (14.7), TL:2488 (14.8 Branch B) and the HALT rule at TL:192 and TL:978. I re-read TL:1140, 1242 and 1248 to 1261 in this pass. The inline copies exist, and 7.15's Branch 1 depends on an empty `Run id:` that no step fills, so the plan is right to include 7.15.
- Change 1 item 4 (final else-branch) and item 5 (HALT when the owner's words are not in the current session) close INV-003 and INV-004.
- Change 1 item 6 adds the resume clause at TL:192, which closes INV-005 and INV-008.
- The F-01 check line says "9 lines plus 7.15". The nine listed lines are TL:989, 1140, 1151, 1165, 1179, 1193, 1207, 1221 and 2481. The count is consistent.

### Check 3: Invariant probe mapping. FAIL for INV-009 only

- INV-001: maps to Change 1 (all eight HALT sites plus 14.7). Sufficient.
- INV-002: maps to Change 1 steps 1 to 3 for 7.15 (transcribe `Run id:`, `Given by:`, `Source:`; HALT only when `Run id:` is empty). Sufficient.
- INV-009: maps to Change 3 / F-03, which lists TL:1248, TL:1257, TL:1258, TL:1260 and TL:1314. The site list is right, but the preferred option does not work (B-1). The fallback option works.
- INV-003, 004, 005, 006, 008, 010, 011, 012, 013, 014, 015 and 016 each map to a change. INV-017 maps only to the flawed F-10 (B-2).

### Check 4: Evidence and citations. PASS, with one false premise reported under Check 5

Spot-checked against the tasklist and repo (all resolved unless noted):

| Citation | Result |
|---|---|
| TL:989 (6.2 Branch 1 "PENDING or Chosen empty") | Confirmed |
| TL:1140 (shared procedure; "all four lines filled") | Confirmed |
| TL:1151 and TL:1165 (inline Branch 1 copies) | Confirmed |
| TL:1242 (7.15 Branch 1 on empty `Run id:`) | Confirmed |
| TL:1248 ("The ONLY commands allowed"), TL:1257 (forbidden list incl. `check`), TL:1258 (step 6 `echo` and `ls -la`), TL:1260 (verification grep) | Confirmed |
| TL:1298 to 1314 (7.22 and 7.24 lenses; 7.22 says OQ-8 uses three lines) | Confirmed |
| TL:1434 (8.3 "appears once") | Confirmed |
| TL:1634 (9.2) | Confirmed |
| TL:2481 and TL:2488 (14.7, 14.8) | Confirmed |
| DESIGN:894 (capture item 13, "read the files only") | Confirmed |
| src/superclaude/core/WORKER-CONTRACT.md:110 | Exists ("The sweep.") |
| tests/skills/test_worker_contract.py:25 (`RULE_PHRASES`) and :173 (`"heartbeats"`) | Confirmed |
| TL:224 (item 1.3) | Confirmed, but it contradicts F-10's claim (see Check 5) |
| reflect/pre/coverage-matrix.yaml:232-237 (NFR-004) and :849-880 (INF-005 to INF-008) | Confirmed; no B2 row exists, as F-22 says |
| git HEAD | `5dc29d23b15eb7db4ead50623bb409f696a0d7d3`, matches the plan's base |

Minor evidence defects are in the Minor notes (M-1, M-2, M-4).

### Check 5: F-10 provenance. FAIL

See B-2. F-10 comes only from INV-017. No CAL covers it. The register row lists INV-017 and A-007 in its source column but never says "probe-sourced, not calibrated", and its MEDIUM is the probe's own severity. Its central claim ("item 1.3 only records HEAD, with no comparison") is false against TL:224.

### Check 6: Changes not being made. PASS

The "Changes NOT Being Made" table gives a reason for each row. The reasons I checked hold up: the three confirmations are justified under Check 1. The one gap is that the table is silent on S-008 (no card has a deviation category); that is a minor note (M-5).

## Blocking findings

### B-1: Change 3 / F-03, the preferred fix is insufficient (INV-009)

- Class: insufficient fix.
- Where: `A/refactor-plan.md`, Change 3, "Recommendation text, preferred option", and the matching F-03 register row.
- Evidence: the preferred option says to replace step (6) at TL:1258 with "a file read of a literal path" so that TL:1248, TL:1260 and TL:1314 "stay correct unchanged". Step (6) exists to find which files are inside the tab-map folder `${XDG_STATE_HOME:-$HOME/.local/state}/ccsession/orca-tabs/` and then read them (DESIGN:894, capture item 13: "whether `orca-tabs/` holds an entry for its pane (read the files only)"). The file names are not known in advance, because each entry is named after a pane or terminal handle. A file read of one literal path cannot list a folder, and reading the folder path itself is not a file read. The plan does not say how the executor learns the names. A literal executor following the preferred option either cannot complete capture item 13 or invents `ls`, which TL:1248, TL:1260 and TL:1314 forbid. So the preferred option does not make the fix sufficient, which is exactly what the Check 3 requirement (INV-009) asks for. The fallback option in the same change (edit TL:1248, 1257, 1258, 1260 and 1314 together) is workable, but it is offered only as the second choice and its text is not given.
- Exact fix: in Change 3 and in F-03, delete the "preferred option" paragraph and make the allowance edit the single recommendation, with this text: "Allow exactly two extra commands in step (6) of 7.16 and nowhere else: `echo "${XDG_STATE_HOME:-$HOME/.local/state}/ccsession/orca-tabs/"` and `ls -la <printed path>`. Edit all four texts together: (a) TL:1248, change 'The ONLY commands allowed' to 'The ONLY commands allowed are the eight templates below and the two step (6) discovery commands (the `echo` of the tab-map path and `ls -la` of that printed path)'; (b) TL:1257 and TL:1258, keep step (6) as written and add that these two are the only non-template commands; (c) TL:1260, change 'one of the eight templates or a file read' to 'one of the eight templates, one of the two step (6) discovery commands, or a file read'; (d) the 7.24 lens at TL:1314, add the same two commands to the set it accepts, so that no breach is raised for them." Keep the three sub-bullets that follow (command records on `$ ` lines, the forbidden-list sentence, `check` in the grep). If the author prefers to avoid shell commands, the only other sufficient option is to state that a Glob of the literal tab-map folder counts as a file read, and to say so in the same four texts. Reword the Check line to: "a correct run's probe file passes TL:1260 and the 7.24 lens, and a grep for `ls` or `echo` in command records finds only the two step (6) commands".

### B-2: Change 10 / F-10, a probe-sourced finding with a false premise and an uncalibrated MEDIUM (INV-017)

- Class: carried false (overstated) finding, and a severity that has no calibration behind it.
- Where: `A/refactor-plan.md`, register row F-10 and Change 10.
- Evidence:
  - F-10 states "item 1.3 records HEAD with no comparison and no HALT". TL:224 (item 1.3, Action) does compare: "If the HEAD sha does not start with `5dc29d23`, record the actual sha and add a note to `### Phase 1 Findings` that every research anchor must be re-checked against the new base before it is used". So the comparison exists. INV-017 itself repeats the same wrong statement, and the plan copied it without reading TL:224.
  - Item 1.4 (TL:229 to 234) already re-reads 18 anchors, including `src/superclaude/core/WORKER-CONTRACT.md:110` and the `tests/skills/test_worker_contract.py` pins (`:25`, `:165-172`, `:173`, `:912`), and records each as CONFIRMED, MOVED or CHANGED. Change 10 asks the executor to "re-run the anchor checks" for exactly those anchors, which duplicates 1.4.
  - The true residual is smaller: neither item 1.3 nor item 1.4 HALTs when a status is CHANGED (1.4's verification only handles MOVED and a missing file). That is a LOW gap, and the plan's own Risk Summary rates F-10 low.
  - The finding has no CAL entry (no card holds it; the register row names only INV-017, A-007 and a V1 Round 2 note). The brief requires such a finding to be labelled probe-sourced, and the MEDIUM here is the probe's own, not a calibrated value. The row never says so.
- Exact fix: rewrite F-10 and Change 10 as follows. Severity: LOW. Add to the register row the words "probe-sourced (INV-017), no card holds it, not calibrated". Replace the claim with: "Item 1.3 (TL:224) already compares HEAD with `5dc29d23` and adds a re-check note; item 1.4 (TL:229 to 234) already re-reads the anchors. The only gap is that neither item HALTs when an anchor status is CHANGED." Replace the recommendation with one edit to item 1.4's Verification (TL:233): "If any row has status CHANGED, apply the HALT rule with a blocker_reason naming the anchor, instead of continuing." Delete the instruction to compare HEAD in item 1.3 and the instruction to re-run the anchor checks. Update the Risk Summary and the change count text if the number of changes or severities is quoted anywhere (the register totals become 3 HIGH, 6 MEDIUM, 14 LOW). The alternative, if the author wants to keep MEDIUM, is to cite debate evidence for MEDIUM (A-007 is QUALIFY, which is not a severity); I found none.

## Minor notes

These never fail the review.

- M-1: F-21 cites TL:2677, which is a 14.x QA item, not a delivery item. Move that citation to the QA group or drop it.
- M-2: Change 21 lists FR-023, NFR-003, FR-025, FR-002 and NFR-014 but does not map each id to one item. Add one item per id so an executor can act on each.
- M-3: F-12 is LOW while INV-015 (MEDIUM) widens its fix to nine scope notes and research/04:90. Add a sentence that the severity stays LOW because the finding is unchanged and only its fix scope grew.
- M-4: F-09 calls 8.18 (TL:1535 to 1539) "boundary tests"; it is a QA edge-case lens. F-23 quotes `coverage-matrix.yaml` lines without the folder, which is `reflect/pre/coverage-matrix.yaml`. Use the full path.
- M-5: no card carries a deviation category (S-008). The plan is silent. Add one line to "Changes NOT Being Made" saying this is accepted.
- M-6: Change 1 item 7 says "use one record line count everywhere (four lines, as TL:1140)". TL:1140's four lines are the `OPERATOR DECISION:` header plus `Chosen:`, `Decided by:`, `Decision source:`, while the six inline items name three lines, and OQ-8 (7.14, 7.15, 7.22) deliberately uses three (`Run id:`, `Given by:`, `Source:`). Read literally, "four everywhere" would force a fourth line into OQ-8. Reword to: "Use one count for the decision records (the header plus three named lines) and leave OQ-8 at its three lines, as the 7.22 lens already allows."
- M-7: R3-G9 is dropped as a confirmation with only a short reason. Add the evidence the card gave (recovery.py:424-434, atomic.py:22-38).

(Counts: 2 blocking, 7 minor.)

## Self-audit

- Read: the whole plan (328 lines), the invariant probe, the debate transcript, base-selection, the CAL blocks of all three variants, and the finding text of V1. I did not re-read every line of V2 and V3 outside their CAL blocks.
- Tasklist lines I read myself: 186-192, 222-234, 773-796, 827, 978-992, 1136-1153, 1165, 1233-1261, 1298-1317, 1417-1476, 1634, 1784, 1952, 2258-2293, 2470-2509, 2754, 2877. DESIGN lines read: 5, 78-80, 216, 466, 677-705, 777-783, 872-896, 932-940, 971-988.
- The dismissal of the preferred option in B-1 rests on reading TL:1258 and DESIGN:894. I did not run the probe or try a tool against the tab-map folder, so "a file read cannot list a folder" is reasoning from the plan's own wording, not an experiment.
- B-2 rests on TL:224 and TL:229 to 234 as read in this pass. I did not check whether `git status` at execution time would differ.
- Not verified: I did not re-count all 25 changes against the register line by line; I checked the cross-references of the changes named above. The suggested register totals in B-2 (3 HIGH, 6 MEDIUM, 14 LOW) assume only F-10 moves.
- Nothing was staged, committed or edited outside this file.
