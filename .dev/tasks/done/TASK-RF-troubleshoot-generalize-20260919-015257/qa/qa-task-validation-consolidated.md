# Consolidated Task-Integrity Findings — cycle 1

**Task file:** `TASK-RF-troubleshoot-generalize-20260919-015257.md`
**Sources:** `qa-task-validation-b2-report.md` (B2 lens: 207/224 PASS, VERDICT FAIL), `qa-task-validation-structure-report.md` (structure lens: VERDICT FAIL), plus two CRITICAL research findings from `qa-research-evidence-round2-report.md` that surfaced after the round-3 check and were not folded into the builder brief (they affect the T15 regression expectations the task file carries in items 7.32/7.53).
**Fix authorization:** ONE fix agent (serialized). All findings below are to be applied to the task file only (never to repo source).

## Items Reviewed (union; FAIL = any lens failed it)

| item id | B2 | structure | consolidated |
|---|---|---|---|
| 0.3 | PASS | FAIL (OQ cite not in Context) | FAIL |
| 0.6 | FAIL (CRITICAL anchor) | FAIL (OQ cite) | FAIL |
| 0.7, 0.8 | FAIL (… placeholders) | — | FAIL |
| 2.6, 2.7 | PASS/note | MINOR (order) | FAIL-minor |
| 2.8 | FAIL | — | FAIL |
| 2.11 | FAIL | — | FAIL |
| 2.24 | FAIL | — | FAIL |
| 2.49 | FAIL | — | FAIL |
| 2.51 | note (regex) | — | FAIL-minor |
| 3.8, 3.10 | PASS | FAIL (TB-Add-8) | FAIL |
| 3.9 | FAIL (7.34→7.54) | FAIL (same) | FAIL |
| 3.16/3.17 | 3.17 FAIL | MINOR (order) | FAIL |
| 3.26 | FAIL-minor | — | FAIL-minor |
| 5.2 | PASS | FAIL (TB-Add-3) | FAIL |
| 6.3, 6.5, 6.9, 6.12, 6.13, 6.14, 6.15 | 6.9/6.12/6.13 FAIL; others note | — | FAIL |
| 7.32, 7.53 | PASS | PASS | **FAIL (research CRITICAL, see F-C1/F-C2)** |
| 7.33-7.53 | PASS | FAIL (TB-Add-8 evidence-absence) | FAIL |
| 7.47 | FAIL-minor | — | FAIL-minor |
| 9.9, 9.11, 9.12, 9.18, 9.19, 9.20, 9.21, 9.22, 9.23 | 9.18/9.20 FAIL; others note | 9.23 MINOR | FAIL |
| 10.3 | PASS | FAIL (no post-completion M3 gate) | FAIL |
| 10.6 | FAIL-minor | MINOR ×2 | FAIL-minor |
| Execution Context block | — | FAIL (file:line in header) | FAIL |
| `## Open Questions` heading | — | FAIL (H2 vs `### Open Questions`) | FAIL |
| Key Objectives 8 / Key Constraints / Phase 2 preamble / Phase 10 heading | — | MINOR | FAIL-minor |
| all other items | PASS | PASS | PASS |

## Findings (apply ALL)

### CRITICAL

- **F-C0 (B2 #1) item 0.6** — `old_string` `      tests/swarm/fixtures/bare_review_v1/golden/.*\|` does not exist in `.pre-commit-config.yaml` (real line 83 has 12-space indent and no trailing `\|`; same text also at line 38). Rewrite: `old_string` = the two-line block `            \.dev/.*\|` + newline + `            tests/swarm/fixtures/bare_review_v1/golden/.*` → `new_string` = same two lines with `\|` appended to the golden line + newline + `            tests/troubleshoot/fixtures/.*`. Verify: `grep -cF 'tests/troubleshoot/fixtures/.*' .pre-commit-config.yaml == 1` AND `grep -cF 'golden/.*\|' == 1` AND `pre-commit validate-config`. Fix item 0.8's expectation (`tests/troubleshoot/fixtures/` count 0 pre-edit) and the Context's block quote (`\.dev/.*`, block is `:77-84`).
- **F-C1 (research evidence-r2 #2) items 7.32/7.53 + harness §5 expected_flags** — Astra-A3 regression expectation `{A10}` is wrong: `retry3-internal-runner/REPORT.md` `## Summary` contains `` `runner-unavailable` `` and `confidence: null`; under the harness A1 predicate (definite enum token ∧ calibrated < 0.5, with `null` treated as < 0.5) A1 ALSO fires. Set Astra-A3 expected = `{A1, A10}` in 7.53's parametrization AND in the MANIFEST/expected table item 7.32 writes; add a one-line note in 7.53 Context: "A1 on Astra is a TRUE positive — `runner-unavailable` is asserted as the enum with confidence null (unobserved)". Cite `<!-- evidence-absence: harness §5 table predates evidence-r2 finding; corrected here -->`.
- **F-C2 (research evidence-r2 #3) items 7.2/7.53 + harness §1.2 A5** — GLM-RUN2 A5 (`consensus_on_unobserved`) can never fire as designed: `_card_fm` looks for line-start `evidence_class:`/`claim_class:` and the GLM card has no frontmatter (calibration `:13`/`:46` are prose "evidence_class none"). Fix in 7.2 (the `_assertions.py` item): A5's predicate must ALSO accept the prose proxy `re.search(r'(?im)^\s*[-*]?\s*evidence[_ ]class\**:?\s*\**(none|source_static|doc_static)', calibration_text)` (a line anywhere in the calibration file). Record in 7.2's Action as "A5 proxy per consolidated finding F-C2" and mirror the same proxy sentence in the canonical assertion table row for A5 (item 1.1 `refs/agent-assertions.md` trigger text: append "; or the calibration file states the evidence class is none/static"). Keep GLM-RUN2 expected `{A1, A3, A4, A5, C2, C3}`. The T13 parity check must still extract 19 ids — no `|` in the amended trigger.

### IMPORTANT

- **F-I1 (B2 #2) item 2.11** — quote the five full Output-Contract rows verbatim as `old_string`s (SKILL:67-71) or anchor each Edit on its unique fragment (`Wave 4.5 H5 off-path-review decision`, ``the H1 runtime-entrypoint card; `null` before H1 runs``, …), one Edit per fragment. Delete the phantom "Phase-2 preamble grep" reference (also in 2.6).
- **F-I2 (B2 #3) item 2.8** — state both Edits explicitly: `` H0 sets `pipeline_hardening_applicable=true` `` → `HC0 sets …`; `skip H1–H5` (exact live phrase, en-dash) → `skip HC1–HC5`. Verify: `sed -n '/^\*\*Trigger\*\*/p' "$SKILL" | grep -cE '\bH[0-5]\b'` == 0.
- **F-I3 (B2 #4) item 2.24** — pick ONE placement, quote its anchor (the closing fence line of step 4), Verify `` grep -cF '`cosmetic_overrun` = the highest overrun value' == 1 ``.
- **F-I4 (B2 #5) item 2.49** — embed the composed Wave 1 step-1b `new_string` verbatim (03 §R-01 v2:216-228 text + the two extra rules + closing sentence, as reconcile Edit-1 specifies) so the Action is a single Edit with a fixed `new_string`.
- **F-I5 (B2 #6) item 3.17** — `old_string` = `### Task 5: Add CI artifact upload for trace files` (unique) → that line + newline + the Task 6 heading + its `- ` line; drop "before the closing fence".
- **F-I6 (B2 #7) items 6.9, 9.18** — paste the 8 crossref chains (6.9) and the 10 resolved-conflict names (9.18) INSIDE the quoted subagent prompt string.
- **F-I7 (B2 #8) items 6.13, 9.20** — embed the exact markdownlint command (from 5.1), the HC guard command (from 5.3), and the do-not-touch list (from Key Constraints) verbatim inside each fixer prompt.
- **F-I8 (B2 #9 / structure #4) item 3.9** — "until item 7.34" → "until item 7.54". Preferably move 7.54 (`test_hardening_h1.py:46` update) and 7.55 (`test_hardening_verdict.py:51`) to directly after 3.11 / 3.3 respectively (ledger groups 2-3 co-locate them) so the suite is not red across Phases 4-6; renumber accordingly.
- **F-I9 (structure #1) `## Execution Context`** — strip every `:N` / `:N-M` / line-count parenthetical from the header block (`SKILL:530`, `RUB:20`, `CAL:127-134`, `CAL:5`/`VAL:5`, `refs/escalation-rubric.md:35`, `refs/calibrator-eval-cases.md:49,54`, `hardening-output-contract.md:68`, `:69`, `:103`, `:77-84`). Keep module/area names only; the cites already live in per-item Context.
- **F-I10 (structure #2) Phase 10** — add a post-completion M3 lens gate (≥6 agents: 3 rf-qa + 3 rf-qa-qualitative, fix_authorization:false → consolidate → one fixer → verify, max 3 cycles) over the FINAL state of all 19 markdown files + tests, because 9.20 fixes and 10.6 reflect remediations can alter `src/superclaude/**` after the Phase 6 gate. Insert before the commit item (10.4); items become 10.4a-10.4h or renumber.
- **F-I11 (structure #3)** — rename `## Open Questions` → `### Open Questions` (nest under Execution Context per template); make 9.23 and 10.6 reference the same heading level.
- **F-I12 (structure #5) TB-Add-3** — add "Depends on OQ-1 default (NO)" to 5.2 Context; move the OQ cites of 0.3 (OQ-1) and 0.6 (OQ-3) into their Context fields.
- **F-I13 (structure #6) TB-Add-8** — 3.8/3.10: cite the 01 §16 hit lines (`UAS:N…`, `CE:N…`) as 3.9/3.11 do. 7.33-7.53: append `<!-- evidence-absence: new test file; no prior code surface -->` to each Context.

### MINOR

- **F-M1 (B2 #10)** items 0.7, 0.8, 6.12 — expand `…` placeholders to full paths.
- **F-M2 (B2 #11)** 3.26 quote the anchor (`- **Cite real files.** …`); 7.47 assert the exact T14 count (16+9+9+1+1 = 36); 10.6 prefix Verification with `Verify:`.
- **F-M3 (B2 #12)** 6.5 seam sum 101 vs reconcile 100 — reconcile the arithmetic; align 2.51's forbidden-name regex with 5.4 (add `image-layers=`); use the strict `^(VERDICT|\*\*Verdict\*\*): (PASS|FAIL)` form on every report Verify (6.3, 6.14, 6.15, 9.9, 9.11, 9.12, 9.19, 9.21, 9.22).
- **F-M4 (structure #7)** Key Constraints (5)/(3) and the Phase 2 preamble: state explicitly that G-07 rule 3 (R-01 before R-02) is honoured by TEXT-ANCHORED bottom-up editing (Wave 1 step 1b lands after R-02's S1.6.0b in file order but the anchors are independent), or reorder 2.46-2.49; do not leave the deviation only in the Task Log.
- **F-M5 (structure #8)** Key Objectives 8 → "10 agents, N=15".
- **F-M6 (structure #9)** drop the empty `## Post-Completion Actions` H2 (or the empty `### Phase 10` H3) so items 10.x sit under one heading.
- **F-M7 (structure #10)** sub-phase 3D header: reword to "text-anchored; order not line-sensitive" or swap 3.16/3.17.
- **F-M8 (structure #11)** 9.23: remove the OQ-4+ conversion; on cap exhaustion write HALT, record the byte-exact message, stop and escalate.
- **F-M9 (structure #13)** 10.6 Action: "four placeholders" (or restore `{DEPTH}` and substitute five).
- **F-M10 (structure #14)** 2.6/2.7 order note.

## Fix-agent contract
- Edit the task file in place with small Edits; never rewrite whole phases.
- After each fix, `grep -cF` the new text to confirm exactly one occurrence.
- Do NOT touch any repo source file, research file, or `.claude/`.
- Append a `### Cycle-1 fixes applied` list to `## Task Log / Notes` naming every F-* id applied and any it could not apply (with reason).
- Return: count applied / not applied, and the new total item count.

---

# Cycle-2 findings (verify-cycle1 residual + A.10.25 research-alignment)

Sources: `qa-task-validation-verify-cycle1.md` (26/26 VERIFIED, 0 REGRESSED, 1 new MINOR), `qa-task-research-alignment-report.md` (VERDICT FAIL: HIGH 1, MEDIUM 1, LOW 5, INFO 1). ONE fix agent; max 1 cycle for alignment findings.

- **F-N1 (verify, MINOR)** item 0.1 — `mkdir -p` creates 10 leaf dirs; Output/Verify say 11. Make the count 10 (or add the missing dir if one was intended) so `find … -type d | wc -l` matches.
- **F-A1 (alignment HIGH)** — S1.6.4a "Hard-stop tasklist composition" section order (03 §0.5, v2:196-206 verbatim; critique AR-01/AR-03): `Header → ## Emitter search → ## Discriminator rows → ## Bracket → ## Fix candidate`, "One file, one counter", "Wave 5 renders unexecuted rows under Next Steps". No item writes this into `refs/diagnosability-audit.md` Section 7 and 2.45 cites it dangling. ADD one item in Phase 3 (sub-phase 3D, after the 3.16/3.17 skeleton items) that inserts the section-order paragraph verbatim from 03 §0.5 into `diagnosability-audit.md` Section 7 at a quoted unique anchor (read `refs/diagnosability-audit.md:255-284` and pick the line after the tasklist header composition, e.g. immediately after the line beginning `**Round**:`), with `grep -cF '## Emitter search' … == 1`-style Verify; update 2.45's cite to point to that item.
- **F-A2 (alignment MEDIUM)** — G-07 group order: reconcile says groups 5 (agents) and 6 (other refs) complete BEFORE 7 (SKILL waves); the task lands SKILL (Phase 2) before refs (Phase 3) and agents (Phase 4); also R-08 step 4.5 (2.36) and R-09 (2.39) cite the HCT form that lands in 3.30. Resolution (no re-ordering of 100 items): add to Key Constraints and the Phase 2 preamble an explicit, text-anchored justification: "Phases 2-4 edit disjoint files; every SKILL citation of a ref section is by section NAME (not line), and the Refs-table rows (Phase 1) already exist, so the G-07 group order is satisfied at the file level once Phase 4 completes; the intra-phase order is bottom-up by anchor. Groups 5/6-before-7 is honoured for the only cross-file DEPENDENCY (Refs rows) and relaxed for citations-by-name." Record the same sentence in the Task Log deviations entry.
- **F-A3 (LOW)** — add ONE item in Phase 3 (RT sub-phase) inserting into `refs/report-template.md` `## Next Steps` (anchor at `RT:146`, quote it) the line "The report stays `partial` until `<row>=<value>`" rendered per unexecuted discriminator row (03 R-06 / AR-03), with Verify grep.
- **F-A5 (LOW)** — items 4.4, 4.9: drop the `[R-14]` tags from the shipped agent prose `new_string`s (replace with "(refs/agent-assertions.md)").
- **F-A6 (LOW)** — item 2.49 Context: reword "composed VERBATIM from 03 §R-01 v2:216-228" → "verbatim except the v2:225 ten-item prompt list, which D9 folds into the eight-delta `refs/environment-deltas.md` table".
- **F-A7 (LOW)** — item 7.47 Verify: "≥ 34 tests pass, all green" (exact 36 is QA-derived, not harness-derived).
- **F-A8 (INFO)** — items 1.1/7.2: add the phrase "A5 amendment (F-C2)" so the M4 cross-source agent (9.18) treats the divergence from reconcile §X-3 as authorised.
- F-A4 — justified deviation, no change.
