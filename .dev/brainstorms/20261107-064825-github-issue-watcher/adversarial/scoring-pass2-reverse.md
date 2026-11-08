# Step 3 Scoring, Pass 2 (reverse order E, D, C, B, A)

Source: `seed-brief.md` (D1 option A, D2 claim-only, D3 integer-only prompt). Inputs: `blind/variant-A..E.md`, `diff-analysis.md`, `rounds/round2-tally.md`. Protocol: `scoring-protocol.md` (quant 50% + qual 50%).

## 1. Quantitative layer

Weights: RC 0.30, IC 0.25, SR 0.15, DC 0.15, SC 0.15.

- RC: 20 source requirements extracted from the seed (D1 poller, D2 claim-only, D3 integer prompt, `--repo IronbellyOrg/IronClaude`, `orca agent launch` argv, `--retry-launch` recovery, dispatch record, lease, attempt cap, launch cap, candidate cap, claim marker, approval label/Project gate, fail-closed at 100 items, bool/float/huge-int guards, same-login multi-workspace, mock-testable repo side, no secrets in prompt, rate-limit handling, follow-ups out of scope). Matched by ID or keyword.
- IC: 1 - contradictions / claims (claims = FR + NFR + OD + numbered risks); contradictions from `diff-analysis.md` X-points plus own read.
- SR: concrete requirement statements / (concrete + vague). Line grep cross-check (vague words: appropriate, as needed, might, may, etc.): A 0, B 1, C 6, D 2, E 0 hits; D's two hits are permissive "may" in OD text, not requirement statements.
- DC: resolved internal references / total (FR, NFR, OD, R, T, F, NG IDs).
- SC: H2 count / max H2 (all 12/12).

| Variant | RC | IC | SR | DC | SC | Quant |
|---|---|---|---|---|---|---|
| E | 1.000 (20/20) | 0.980 (1/51: FR-014 agent argv) | 0.973 (36/37) | 1.000 | 1.000 (12/12) | 0.991 |
| D | 1.000 (20/20) | 1.000 (0/57) | 1.000 (34/34) | 1.000 | 1.000 (12/12) | 1.000 |
| C | 0.950 (19/20: no launch argv) | 1.000 (0/38) | 0.545 (12/22) | 1.000 | 1.000 (12/12) | 0.917 |
| B | 1.000 (20/20) | 0.942 (3/52: FR-022, NFR-010, R9 vs NFR-007) | 0.971 (34/35) | 1.000 | 1.000 (12/12) | 0.981 |
| A | 1.000 (20/20) | 0.964 (2/56: OD-5 `off` vs §3; §7 retryable timeout) | 0.968 (30/31) | 0.971 (34/35: `launched_unclaimed` absent from NFR-007 enum) | 1.000 (12/12) | 0.982 |

## 2. Qualitative layer (CEV, reverse order)

Format per line: criterion | evidence (section) | verdict.

### Variant E (25/30)

Completeness 5/5
- C1 source reqs | FR-001..FR-023 map D1-D3 and seed criteria (§4, §12) | MET
- C2 edge/failure | FR-003 exactly 100 items fails closed, exit 4; FR-009 unreadable Project exits 3 (§4) | MET
- C3 dependencies | gh scopes (`read:project`), orca, Python prerequisites (§2, §5) | MET
- C4 success criteria | every FR carries a Given/When/Then "AC" line (§4) | MET
- C5 out of scope | non-goals and follow-ups listed (§2, §9) | MET

Correctness 4/5
- K1 no factual errors | FR-002 `gh issue list --repo IronbellyOrg/IronClaude ... -L 100` (§4) | MET
- K2 feasible | mock-testable repo deliverables (§8) | MET
- K3 terminology | dispatch-record states used consistently (§3, §7) | MET
- K4 no contradictions | FR-014 `--agent <agent>` vs seed fixed `--agent claude` (X-008) | NOT MET
- K5 rationale | O-1..O-8 carry recommended defaults with reasons (§10) | MET

Structure 5/5
- S1 ordering | definitions before FRs, state model after (§3, §4, §7) | MET
- S2 hierarchy | 12 H2 sections, no orphan H3 (§1-§12) | MET
- S3 separation | security, record, deliverables separate (§6, §7, §8) | MET
- S4 navigation | traceability table cross-references IDs (§12) | MET
- S5 conventions | FR/NFR IDs, open decisions, risk list (§4, §5, §10, §11) | MET

Clarity 3/5
- L1 unambiguous | FR-012 "deleted or marked abandoned" leaves outcome open (§4) | NOT MET
- L2 concrete | FR-005 `max_candidates` 10, cycles examine all 25 (§4) | MET
- L3 section purpose | each section opens with a scope line (§1-§12) | MET
- L4 terms defined | "AC" used throughout without definition (§4) | NOT MET
- L5 decision points | O-1..O-8 open decisions listed (§10) | MET

Risk 3/5
- R1 3 risks with P/I | R-1..R-7 bullets give no likelihood or impact (§11) | NOT MET
- R2 mitigation each | R-6, R-7 carry no mitigation (§11) | NOT MET
- R3 failure/recovery | `--retry-launch` recovery from unknown state (§7) | MET
- R4 external deps | R-2 shared per-login allowance, NFR-005/006 bounds (§11) | MET
- R5 monitoring | audit line `truncated=true`, `rejected_approval` counts (FR-003, FR-007) | MET

Edge 5/5
- E1 collections | FR-003 exactly 100 fails closed; FR-005 cap 10 of 25 (§4) | MET
- E2 state interactions | FR-008 per-issue `projectItems` read, Status `Backlog` gate (§4) | MET
- E3 guards | bool/float/oversized integer rejected for prompt (§6) | MET
- E4 count divergence | FR-011 `attempts=1` flushed before orca; daily cap FR-018 (§4) | MET
- E5 combined features | same-login multi-workspace claim race (§7) | MET

### Variant D (29/30)

Completeness 5/5
- C1 source reqs | FR-001..FR-021 trace to every seed item (§4, §12) | MET
- C2 edge/failure | `gh api user` exits 1 gives exit 3, no orca call (§4) | MET
- C3 dependencies | runbook pre-flight for `read:project` (§11 R2, §8) | MET
- C4 success criteria | GWT acceptance per FR; T1-T12 (§4, §8) | MET
- C5 out of scope | "Out of scope: anything live; any listener, port, webhook" (§1) | MET

Correctness 5/5
- K1 no factual errors | discovery argv list asserted exactly; no `title`/`body` fields (§4) | MET
- K2 feasible | package `src/superclaude/cli/issue_watch/`, stub gh/orca tests (§1, §8) | MET
- K3 terminology | `attempts`/`launches` counters used consistently (§7) | MET
- K4 no contradictions | IC 0/57; leads X-001, X-002, X-003, X-005 (round2-tally) | MET
- K5 rationale | OD-1..OD-9 with defaults and reasons (§10) | MET

Structure 5/5
- S1 ordering | definitions, FRs, NFRs, security, record (§3-§7) | MET
- S2 hierarchy | 12 numbered H2 sections (§1-§12) | MET
- S3 separation | operator runbook kept in design doc, apart from FRs (§1, §8) | MET
- S4 navigation | traceability table (§12) | MET
- S5 conventions | FR/NFR, OD, R, T, FU numbering (§4-§11) | MET

Clarity 4/5
- L1 unambiguous | "exit code is 4, zero launches, audit result truncated" (§4) | MET
- L2 concrete | lease 60, max_attempts 3, max_launches 1 (§7) | MET
- L3 section purpose | each section states its purpose (§1-§12) | MET
- L4 terms defined | "GWT" and "SLO" used undefined (header lens, §4) | NOT MET
- L5 decision points | OD list with recommended defaults (§10) | MET

Risk 5/5
- R1 3 risks with P/I | R1-R9 table with "Likelihood / impact" column (§11) | MET
- R2 mitigation each | Mitigation column per risk (§11) | MET
- R3 failure/recovery | `claim_not_observed` surfaces within one lease; runbook (§11 R1, §8) | MET
- R4 external deps | R2 token lacks `read:project`, Option D fallback (§11) | MET
- R5 monitoring | SLO targets and audit `result=` field (NFR-013, §4) | MET

Edge 5/5
- E1 collections | "Given 100 issues returned ... exit code is 4" and empty run exits 0 (§4) | MET
- E2 state interactions | approver-labeled, outsider-unlabeled, outsider-labeled sequence skipped (§4) | MET
- E3 guards | bool/float/10**9 rejected for issue number (§6) | MET
- E4 count divergence | attempts vs launches separation, `pending_orphan` (§7) | MET
- E5 combined features | same-login multi-workspace (§7) | MET

### Variant C (26/30)

Completeness 5/5
- C1 source reqs | FR-001..FR-013 cover D1-D3 (§4, §12) | MET
- C2 edge/failure | incomplete event history or bot fails approval (§3) | MET
- C3 dependencies | workspace tokens must read Projects; revisit conditions (§2) | MET
- C4 success criteria | "A successful launch does not prove a successful claim" outcomes split (§1) | MET
- C5 out of scope | claim command owns assignment, summary, `next-steps.md` (§1, §9) | MET

Correctness 5/5
- K1 no factual errors | Projects v2 node ID references issue node ID (§3) | MET
- K2 feasible | mock-testable deliverables (§8) | MET
- K3 terminology | Tagged/Approved/In a Project defined and reused (§3) | MET
- K4 no contradictions | IC 0/38; leads X-004 (round2-tally) | MET
- K5 rationale | "deliberately selects a stricter subset than the existing claim command" (§3) | MET

Structure 5/5
- S1 ordering | §1-§12 dependency order (§1-§12) | MET
- S2 hierarchy | 12 H2, flat (§1-§12) | MET
- S3 separation | security vs record vs deliverables (§6-§8) | MET
- S4 navigation | traceability table (§12) | MET
- S5 conventions | FR/NFR IDs (§4, §5) | MET

Clarity 3/5
- L1 unambiguous | NFR-004 "bounded retries" states no bound (§5) | NOT MET
- L2 concrete | FR-003 launch submission abstract, no argv (§4) | NOT MET
- L3 section purpose | each section summarisable in one line (§1-§12) | MET
- L4 terms defined | Tagged, Approved, In a Project, Intended owner defined (§3) | MET
- L5 decision points | open decisions listed (§10) | MET

Risk 3/5
- R1 3 risks with P/I | §11 prose, no IDs or probability (§11) | NOT MET
- R2 mitigation each | no per-risk mitigation (§11) | NOT MET
- R3 failure/recovery | unknown state recovery via retry (§7) | MET
- R4 external deps | persisted rate-limit reset time (NFR-004) | MET
- R5 monitoring | launch vs claim outcomes reported distinctly (§1, §5) | MET

Edge 5/5
- E1 collections | FR-006 pagination stops fail-closed at limit (§4) | MET
- E2 state interactions | account ID anchors identity; login kept for display (§3) | MET
- E3 guards | missing actor metadata fails approval; draft items excluded (§3) | MET
- E4 count divergence | unassigned and multi-assignee issues ineligible (§3) | MET
- E5 combined features | multi-workspace same login (§7) | MET

### Variant B (29/30)

Completeness 5/5
- C1 source reqs | FR-001..FR-022 trace to seed (§4, §12) | MET
- C2 edge/failure | `FakeOrca` modes ok, error, unknown, timeout, not_orca (§8) | MET
- C3 dependencies | FR-014 probes `orca-ide` then `orca`, accepts only `orca-cli` (§4) | MET
- C4 success criteria | Given/when/then column per FR and NFR (§4, §5) | MET
- C5 out of scope | NG1-NG5 and follow-ups (§2, §9) | MET

Correctness 4/5
- K1 no factual errors | launch argv matches seed (§4) | MET
- K2 feasible | single `once` verb CLI spelled out (§8) | MET
- K3 terminology | record states consistent (§3, §7) | MET
- K4 no contradictions | NFR-010 corrupt file "loads as empty"; FR-022 `--label-only` drops Project gate (X-003, X-005) | NOT MET
- K5 rationale | OD-5 "It drops two definitions; the degradation must stay visible" (§10) | MET

Structure 5/5
- S1 ordering | §1-§12 ordered (§1-§12) | MET
- S2 hierarchy | 12 numbered H2 (§1-§12) | MET
- S3 separation | security, record, deliverables split (§6-§8) | MET
- S4 navigation | traceability table (§12) | MET
- S5 conventions | FR/NFR/OD/R/T IDs in tables (§4-§11) | MET

Clarity 5/5
- L1 unambiguous | FR-014 "then `E-ORCA-NOT-FOUND`, zero launches" (§4) | MET
- L2 concrete | full `once` flag list with caps and lease (§8) | MET
- L3 section purpose | purpose line per section (§1-§12) | MET
- L4 terms defined | definitions section (§3) | MET
- L5 decision points | OD-1..OD-10 (§10) | MET

Risk 5/5
- R1 3 risks with P/I | R1-R9 "Likelihood / impact" column (§11) | MET
- R2 mitigation each | Mitigation column per risk (§11) | MET
- R3 failure/recovery | `--retry-launch` path for unknown (§7) | MET
- R4 external deps | T7 `orca` as GNOME screen reader, probe guards it (§6) | MET
- R5 monitoring | `mode` field on every audit line (FR-022) | MET

Edge 5/5
- E1 collections | exactly 100 items fails closed (§4) | MET
- E2 state interactions | re-approval does not reset attempts (OD-6) | MET
- E3 guards | bool/float/huge-int rejected (§6) | MET
- E4 count divergence | attempts vs launches caps (§7) | MET
- E5 combined features | marker still blocks relaunch after state loss (NFR-010) | MET

### Variant A (28/30)

Completeness 5/5
- C1 source reqs | FR-001..FR-020 trace to seed (§4, §12) | MET
- C2 edge/failure | `launched` unclaimed after lease audited `launched_unclaimed`, never relaunched (§7) | MET
- C3 dependencies | "no dependency is added"; stage protocols only (NFR-011) | MET
- C4 success criteria | Given/then acceptance per requirement (§4, §5) | MET
- C5 out of scope | NG-1..NG-6; F-1..F-7 follow-ups (§2, §9) | MET

Correctness 3/5
- K1 no factual errors | NFR-011 cites `make verify-deps`, not a documented make target (§5) | NOT MET
- K2 feasible | mock-testable repo deliverables (§8) | MET
- K3 terminology | record states and stage names consistent (§3, §7) | MET
- K4 no contradictions | OD-5 `off` widens §3 Project gate; §7 timeout path retryable (X-002, X-005) | NOT MET
- K5 rationale | OD-5 "a missing scope must not widen eligibility" (§10) | MET

Structure 5/5
- S1 ordering | definitions before requirements and record (§3-§7) | MET
- S2 hierarchy | 12 numbered H2 (§1-§12) | MET
- S3 separation | security, record, deliverables split (§6-§8) | MET
- S4 navigation | traceability table (§12) | MET
- S5 conventions | FR/NFR/OD/R/F/NG IDs (§4-§11) | MET

Clarity 5/5
- L1 unambiguous | vague-word grep 0 hits; "never relaunched automatically" (§7) | MET
- L2 concrete | `cycle.py` imports only stage protocols and public functions (NFR-011) | MET
- L3 section purpose | purpose line per section (§1-§12) | MET
- L4 terms defined | definitions section (§3) | MET
- L5 decision points | OD-1..OD-9 with recommended defaults (§10) | MET

Risk 5/5
- R1 3 risks with P/I | R-1..R-8 with likelihood and impact (§11) | MET
- R2 mitigation each | mitigation per risk (§11) | MET
- R3 failure/recovery | F-5 `issue-watch release <N>` for exhausted entries (§9) | MET
- R4 external deps | gh scope and orca failure handling (§5, §11) | MET
- R5 monitoring | `launched_unclaimed` audit state (§7) | MET

Edge 5/5
- E1 collections | exactly 100 items fails closed (§4) | MET
- E2 state interactions | lease expiry vs claim marker (§7) | MET
- E3 guards | bool/float/huge-int rejected (§6) | MET
- E4 count divergence | attempts vs launches caps (§7) | MET
- E5 combined features | same login across workspaces (§7) | MET

## 3. Qualitative summary

| Variant | Compl | Corr | Struct | Clar | Risk | Edge | Total | Qual |
|---|---|---|---|---|---|---|---|---|
| A | 5 | 3 | 5 | 5 | 5 | 5 | 28/30 | 0.933 |
| B | 5 | 4 | 5 | 5 | 5 | 5 | 29/30 | 0.967 |
| C | 5 | 5 | 5 | 3 | 3 | 5 | 26/30 | 0.867 |
| D | 5 | 5 | 5 | 4 | 5 | 5 | 29/30 | 0.967 |
| E | 5 | 4 | 5 | 3 | 3 | 5 | 25/30 | 0.833 |

Edge-case floor: every variant scores 5/5 on dimension 6; all eligible. Floor not suspended.

## 4. Combined scores

| Variant | Quant | Qual | Combined | Rank |
|---|---|---|---|---|
| D | 1.000 | 0.967 | 0.983 | 1 |
| B | 0.981 | 0.967 | 0.974 | 2 |
| A | 0.982 | 0.933 | 0.958 | 3 |
| E | 0.991 | 0.833 | 0.912 | 4 |
| C | 0.917 | 0.867 | 0.892 | 5 |

Margin D - B = 0.009 (< 0.05): tiebreaker applies. A (0.958) is also within 0.05 of D.

## 5. Tiebreaker

1. Debate performance (round2-tally, points where the variant is the single leading letter): D 6 (C-017, C-018, X-001, X-002, X-003, X-005); C 2 (C-011, X-004); A 1 (C-021); B 1 (S-007); E 1 (C-003). D beats B and A decisively; tiebreaker resolved at step 1.
2. Correctness count (not needed): D 5, B 4, A 3.

## 6. Selected base: Variant D

Strengths to preserve from D: operator runbook (§1, §8); `attempts`/`launches` counters and `pending_orphan` (§7); fail-closed corrupt record (NFR-011); SLOs (NFR-013); GWT acceptance on every FR (§4); risk table with likelihood/impact (§11).

Strengths to incorporate from others:
- E: per-issue `projectItems` read (FR-008); daily cap (FR-018).
- C: node and account IDs for identity (§3, §7); persisted rate-limit reset time (NFR-004).
- B: `orca-cli` probe (FR-014); re-approval not resetting attempts (OD-6); `_assumed_shape` fixtures (§8).
- A: stage protocols in `cycle.py` (NFR-011, §8); JSON config for Python 3.10 (OD-9).

Fixes for the base: define "GWT" and "SLO" on first use.

## 7. Position-bias note

This is pass 2 (reverse order) only. Reconciliation with pass 1 (forward order) belongs to the orchestrator.
