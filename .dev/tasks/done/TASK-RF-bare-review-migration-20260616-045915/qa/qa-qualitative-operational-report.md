# QA Report — Task Qualitative Review (Operational Correctness Lens)

**Topic:** sc-bare-review M8/M9 migration corrective tasklist
**Date:** 2026-06-16
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A (fix_authorization: false — report only)

---

## Overall Verdict: FAIL

One IMPORTANT operational defect (I-1: `--reviewers` clamp collides with preflight's
`workers.count == 4` self-reset and the un-resized `workers.models` pool) plus two MINOR
clarity items. The defect is recoverable via the item's own blocker-logging valve, but the
affirmative instruction in Step 2.2 is incomplete relative to the code it must integrate with,
and unlike its sibling Step 2.3 it carries no warning to look for the trap. Per the no-leniency /
all-severities-must-resolve rule, any finding = FAIL.

The plan is otherwise operationally excellent: the headline WS-0 discovery is byte-accurate, the
WS-0→A→B→C ordering is sound, every destructive op is correctly parity-gated, and the golden is
frozen before legacy deletion. With I-1 addressed (or its blocker-valve exercised), this task would
execute to success.

---

## Drift-baseline (AX-1)

BUILD_REQUEST.GOAL verbatim was NOT supplied in the spawn prompt (only a one-line TRACK GOAL:
"Corrective MDTM tasklist completing the sc-bare-review M8/M9 migration."). The task file
reproduces an equivalent GOAL in its `description`/`Key Objectives`. Per the drift-baseline rule
the AX-1 Drift axis is treated as **lens-limited** to the task-file-internal goal restatement
rather than a true BUILD_REQUEST.GOAL diff; `drift-axis-inactive` is NOT emitted because a
reproduced goal exists in-file. AX-1 was applied against citation-drift (stale file:line anchors)
across all checked items.

---

## Self-Audit

**(a) Reliance list — structural verdict items relied on (NOT re-verified):**
- Relied on inherited A.10 B2 self-containment + phase-structure PASS — did not re-check item
  self-containment, frontmatter shape, section numbering, or TB-Add structural gates.
- Relied on inherited A.10.25 research-alignment PASS — did not re-audit research-file coverage
  mapping.

**(b) Independent semantic / operational checks (the substance of this review):**
- WS-0 headline-stub claim — verified by `Read commands.py:1554-1578` (inline path calls ONLY
  `dispatch_wave1(...)` then emits stub stdout `swarm run: dispatched job (mode=...)` and exits;
  never calls normalize/reduce/emit_contract). Exact match to task claim.
- Resume-branch reference sequence — verified by `Read commands.py:1930-1985`
  (`dispatch_wave1`→`normalize_wave2(recipe_name=...)`→`reduce_wave3(resume=True)`).
- Function signatures — `grep`/`Read` confirmed `dispatch_wave1` (dispatch.py:334, `prompt:str=""`,
  `worker_spec=None`), `normalize_wave2` (normalize.py:500; final_path write 482-483),
  `reduce_wave3` (reduce.py:555 — calls `emit_contract` internally at 722), `emit_contract`
  (reduce.py:369), `CONTRACT_FILENAME="return-contract.yaml"` (reduce.py:139).
- `_build_spec_from_lens` hardcodes — `Read commands.py:728-830` confirmed `invocation_label` (:775),
  `timeout_sec:180` (:789), `count:workers_count` (:781), `line_cap:entry.default_target_line_cap`
  (:819), `models` list sized to `workers_count` (:788).
- preflight line_cap + workers self-reset — `grep preflight.py` confirmed `line_cap<=0 or ==4000`
  reset (527-528, the trap Step 2.3 correctly warns about) AND `workers.count<=0 or ==4` reset
  (523-524, the analogous trap Step 2.2 does NOT warn about → finding I-1).
- Lens fields — `Read bare_review.py` (system_prompt_fragment 47-52, user_template 53-57,
  default_workers 61, default_target_line_cap 62, suspect 63, recommended_next_command 65-68,
  CANONICAL_INJECTION_GUARD_SENTENCE import :29).
- Test anchors — `grep` confirmed parity-test `skipif(LEGACY_SCRIPT.exists())` whole-module guard
  (217-218), SCENARIOS all-success/partial-with-timeout/salvage-promoted (151/160/171),
  recipe-test bare `assert LEGACY_SCRIPT.exists()` (89), e2e absent-test
  `test_quickstart_does_not_emit_m5_artifacts` (104-114), `T2-Bare Review` header
  (recipe-test 268,327; source 192).
- OPS sources — `grep` confirmed phase-9 tasklist OPS-001..006 / R-150..155 / D-0135 / T09.0N
  mapping; parent spec :465 (three-layer observability) + :724 (Prometheus deferred);
  release-notes-v1.md:16 ("~60-line thin caller"); docs/dev/lens-contribution-policy.md C1-C5+
  validator+suspect (OPS-005 superset).
- Filesystem state — `ls`/`wc` confirmed current state matches plan premises (SKILL.md 231 lines,
  3 legacy scripts present, both orphaned refs present, refs/templates/bare-review-output.md
  survives, scripts/swarm_env_readiness.sh absent [NET-NEW], .claude mirror carries the scripts).
- start_commit 02582ca0 is a real commit (`git cat-file`); StubTransport(fixtures=...) real
  (stub.py:92-109); SWARM_REAL_E2E gating real (test_e2e_real_proxy.py:66-73); EXIT_USAGE real.

3. Why trust this review found real issues: 30+ independent tool calls (Read/Grep/Bash/wc/ls/git),
   every load-bearing file:line anchor in the plan was re-derived from current source, and the one
   IMPORTANT finding was uncovered by tracing the actual preflight override code path (523-524)
   that the plan's own Step 2.3 establishes as a known hazard class but Step 2.2 omits.
4. No web research was required (entirely local-file-bound); Tavily was therefore not invoked.

---

## Items Reviewed (operational-correctness lens)

| # | Operational Check | axis | Result | Evidence |
|---|-------------------|------|--------|----------|
| 1 | Gate/command dry-run preconditions | none | PASS | `uv run pytest tests/swarm/`, `make verify-sync`, `wc`/`grep`/`git rm` all have preconditions met by repo state or earlier items; baseline (1.3) captured before any edit; sync (3.2/5.9) runs after SKILL/deletion edits. |
| 2 | Project convention compliance (src→.claude sync; never stage .claude) | none | PASS | All skill-dir edits (WS-A,WS-C) followed by `make sync-dev && make verify-sync`; deletions via `git rm` on src side; .claude mirror exists with scripts so verify-sync semantics hold. |
| 3 | Intra/inter-phase execution-order simulation | none | PASS | WS-0→A→B→C strictly sequenced; golden frozen (4.1) before legacy deletion (5.x); thin caller (WS-A) only after WS-0 makes CLI emit contract; WS-E after WS-A+WS-C verdicts exist. |
| 4 | Function-signature verification (WS-0 wiring real) | none | PASS | dispatch_wave1/normalize_wave2/reduce_wave3/emit_contract all exist with the cited params; inline stub vs resume delta is byte-accurate (commands.py:1554-1578 vs 1930-1985). |
| 5 | Module-context analysis (spec_dict / _build_spec_from_lens hardcodes) | AX-1 | FAIL | _build_spec_from_lens builds `models` sized to workers_count AND preflight self-resets `workers.count==4`→default; Step 2.2 doesn't account for either → finding I-1. (Other hardcodes correctly anchored.) |
| 6 | Downstream-consumer analysis (flag→spec_dict→preflight→dispatch) | AX-3 | FAIL | `--reviewers` consumer chain: count→preflight workers_requested OK, but `workers.models` consumer NOT updated by Step 2.2 → finding I-1. line_cap chain correctly handled by Step 2.3. |
| 7 | Test validity (tests exercise real artifacts not stubs) | none | PASS | WS-B parity gate drives the CLI via CliRunner+stub vs frozen golden captured from REAL t2_normalize.py; presence test asserts real RESULT_CONTRACT_FILENAME + T2-Bare Review header + checksum. |
| 8 | Test coverage of primary use case | none | PASS | WS-0 presence test feeds full inline pipeline end-to-end; WS-B covers all 3 scenarios + 5 invariants + injection-guard; post-deletion gate proves coverage survives deletion. |
| 9 | Error-path coverage (new flags) | AX-4 | PASS-with-note | `--reviewers` [2,4] reject→EXIT_USAGE is specified; but the "honored" path for value 4 is silently defeated (I-1). Other flags (line_cap/timeout/label) have correct optional+default handling. |
| 10 | Runtime failure-path trace (data flow breaks?) | none | PASS | input→preflight→dispatch(prompt+worker_spec)→normalize_wave2(bare-review-v1)→reduce_wave3(emit_contract)→contract+bodies; e2e-flip (2.9) reads structured emission-scope handoff so it survives rollover. |
| 11 | Completion-scope honesty (open questions resolved) | none | PASS | WS-0 (the research-discovered blocker) is built FIRST, not ignored; OPS-004 rehearsal correctly HALTs as needs_human_decision rather than auto-stamping; disk-verify anti-attestation gates every "done". |
| 12 | Ambient-dependency completeness | AX-3 | PASS-with-note | SKILL frontmatter allowed-tools revised, release-notes reconciled, mirror synced, attestations superseded — touchpoints covered. Sole gap is workers.models resize (I-1, already counted). |
| 13 | Kwarg sequencing red flags | none | PASS | Step 2.4 (`--timeout-sec`) explicitly notes its dependency on Step 2.7/2.6 wiring worker_spec; Step 2.6 (prompt) precedes Step 2.7 (pipeline); no "add kwarg before add param" inversion. |
| 14 | Function-existence claims grep-verified | none | PASS | Every "exists at"/"is a stub" claim re-grepped: inline stub (real), resume pipeline (real), all 4 functions (real), lens fields (real), CANONICAL_INJECTION_GUARD_SENTENCE (real). |
| 15 | Cross-reference accuracy (template/source §N anchors) | AX-1 | PASS | All file:line anchors re-derived from current source match within tolerance (functions, lens lines, test lines, phase-9 OPS IDs, parent-spec :465/:724, release-notes:16). No stale citations found. |

---

## Summary
- Checks passed: 13 / 15 (2 FAIL: items 5 & 6, both tracing to the single defect I-1)
- Checks failed: 2 (same root cause)
- Critical issues: 0
- Important issues: 1 (I-1)
- Minor issues: 2 (M-1, M-2)
- Issues fixed in-place: 0 (fix_authorization: false — report only)
- Confidence: Verified 15/15 | Unverifiable 0 | Unchecked 0 | Confidence 100%
- Tool engagement: Read 6 | Grep/Bash 9 | Glob 0 (filesystem checks folded into Bash ls/wc/git)

---

## Issues Found

| # | Severity | Location (item) | Issue | Required Fix |
|---|----------|-----------------|-------|--------------|
| I-1 | IMPORTANT | Step 2.2 (`--reviewers` flag) | The mandated `[2,4]` clamp collides with TWO enabling code paths Step 2.2 does not account for: (a) `preflight.py:523-524` self-resets `workers.count == 4` back to `lens_entry.default_workers` (3) — so `--reviewers 4` (the top of the allowed range) is **silently clobbered to 3**, exactly the trap Step 2.3 warns about for `line_cap` but Step 2.2 carries NO equivalent warning; (b) `_build_spec_from_lens` (commands.py:788) builds `workers.models` sized to the lens default (3), and INV-005 (`preflight.py:1151-1229`) rejects/clamps when `workers.count` exceeds the model-pool size — so `--reviewers 4` (count=4 > 3 models) trips the pool guard unless `workers.models` is also resized. Net: an executor following Step 2.2 literally ships a `--reviewers` flag whose value `4` does not actually take effect. | Amend Step 2.2 to (a) add the same caveat Step 2.3 has — note that `preflight.py:523-524` resets `count==4` to the lens default and instruct the executor to thread the user value so a value of 4 survives (mirror the line_cap remedy); AND (b) when `--reviewers N` is supplied, also resize `spec_dict["workers"]["models"]` to N entries (or document that the stub model pool must be re-derived from count) so INV-005 does not clamp. The existing blocker-valve ("log if spec-dict wiring unclear") is a soft landing but should not substitute for the explicit instruction. |
| M-1 | MINOR | Step 2.7 (pipeline wiring) | The item says "then `reduce_wave3(...)` / `emit_contract` to write `return-contract.yaml`", phrasing `emit_contract` as a possibly-separate call. In source, `reduce_wave3` calls `emit_contract` **internally** (reduce.py:722) — the resume branch (the reference the item tells the executor to mirror) calls ONLY `reduce_wave3`. An executor adding a redundant explicit `emit_contract` call could double-emit. Low risk because the item also says "mirror the resume branch / reuse shared helpers", which self-corrects. | Reword to "then `reduce_wave3(...)` (which emits `return-contract.yaml` via its internal `emit_contract` call at reduce.py:722, exactly as the resume branch does)" to remove the implication of a separate call. |
| M-2 | MINOR | Step 2.6 (prompt assembly) | The item says "reuse the existing assembly helper if the resume branch has one rather than duplicating logic." Verification found NO standalone lens-prompt→`target_content` assembly helper that the resume branch calls — the resume branch rehydrates via `synthetic_preflight` and does not freshly assemble a prompt. So the "if the resume branch has one" hedge will resolve to "it does not," and the executor must assemble from the lens templates + preflight's truncated target. The item's blocker-valve covers this, but the framing mildly implies a reusable helper is likely to exist. | Tighten the guidance to "the resume branch rehydrates rather than re-assembling, so assemble from the lens `user_template`/`system_prompt_fragment` + preflight's truncated target content; only reuse a shared helper if one is found in the non-resume assembly path." |

---

## Actions Taken
None — `fix_authorization: false`. All findings are reported for the orchestrator/executor to remediate. No files were modified.

---

## Operational Strengths Worth Noting (not findings — confidence evidence)
- The **headline WS-0 discovery is exactly correct**: the inline path IS a dispatch-only stub
  (commands.py:1554-1578) and the resume branch IS the working reference (1930-1985). This is the
  single most consequential operational claim and it verifies byte-for-byte.
- **Step 2.3's line_cap caveat is a model of good task construction** — it anticipates the exact
  preflight.py:527-528 `==4000` override trap. The defect I-1 is precisely that Step 2.2 did NOT
  replicate this rigor for the structurally-identical `==4` workers reset.
- **Destructive-op gating is sound**: WS-C deletion is hard-gated on `parity-gate-status.md`
  recording `PARITY_GREEN: true` AND a complete frozen golden (Step 5.1), the golden is frozen
  BEFORE deletion (Step 4.1 while t2_normalize.py still exists), and every deletion item
  re-reads the authorization file.
- **Anti-attestation discipline is pervasive**: disk-verify items (3.3, 5.10, PC.1) prove every
  "done" claim on disk — directly countering the original phase-8 false-attestation failure mode
  the corrective task exists to fix.
- **HALT discipline correct**: OPS-004 tabletop sign-off is a genuine needs_human_decision HALT
  (Step 6.6) that writes PENDING + a follow-up entry and explicitly forbids auto-stamping.

---

## QA Complete

---

## FIX ROUND (I20 serialized fix agent) — 2026-06-16

**fix_authorization: true.** Applied the I-1 (IMPORTANT) operational fix + both MINOR clarity
fixes in-place via surgical Edit on the task file. The qa-gate-sufficiency lens PASSED separately
(no changes). Each load-bearing source anchor was independently re-verified against current source
this round before editing.

### Source re-verification (this round)
- `preflight.py:523-524` — re-read: `if spec.workers.count <= 0 or spec.workers.count == 4: spec.workers.count = lens_entry.default_workers`. CONFIRMED — `==4` reset is real and structurally identical to the `line_cap == 4000` reset at 527-528.
- `commands.py:788` — re-read: `"models": [f"lens-default-model-{i}" for i in range(workers_count)]`. CONFIRMED — `workers.models` is sized to `workers_count` (lens default), so a raised count needs a resized model pool to clear INV-005.
- `reduce.py:722` — re-read: `if should_emit and output_dir is not None: emit_contract(contract, Path(output_dir))` inside `reduce_wave3`. CONFIRMED — `emit_contract` is invoked INTERNALLY by `reduce_wave3`; not a mandatory separate call.

### Fixes applied

| Finding | Item | Fix applied | Re-verification |
|---------|------|-------------|-----------------|
| I-1 (IMPORTANT) | Step 2.2 (`--reviewers`) | Added (a) a `count == 4` default-equals reset CAVEAT mirroring Step 2.3 (cites `preflight.py:523-524`, instructs threading the user value so 4 survives expansion); (b) an ALSO REQUIRED clause to resize `spec_dict["workers"]["models"]` to N entries against the INV-005 pool guard (cites `commands.py:788` + `preflight.py:1151-1229`); (c) retained the existing "log a blocker if spec-dict wiring unclear" valve; (d) added a VERIFICATION clause requiring an integration check that `--reviewers 4 ... --transport stub` dispatches 4 workers (not silently 3). | Re-read item L191: all four sub-fixes present, `- [ ]` checkbox + "mark this item as complete." closer intact; item remains self-contained (B2). |
| M-1 (MINOR) | Step 2.7 (pipeline wiring) | Reworded `reduce_wave3(...) / emit_contract` → "call `reduce_wave3(...)` (which writes `return-contract.yaml` via its INTERNAL `emit_contract` call at `reduce.py:722` — do NOT add a separate explicit `emit_contract` call … a redundant explicit call would double-emit)". Removes the implication of a mandatory separate call; matches the resume branch (which calls only `reduce_wave3`). | Re-read item L211: phrasing now states the inline path calls reduce_wave3 which emits the contract; no separate emit_contract mandate. |
| M-2 (MINOR) | Step 2.6 (prompt assembly) | Reworded to state explicitly that the resume branch REHYDRATES (via `synthetic_preflight`) rather than re-assembling via a reusable helper, so there is no shared lens-prompt→`target_content` helper to call; the inline path must assemble the worker prompt + worker_spec directly from the resolved lens; "only reuse a shared helper if one is found in a non-resume assembly path." | Re-read item L207: hedge "reuse the existing assembly helper if the resume branch has one" replaced with the explicit "resume rehydrates, assemble directly" framing. |

### Scope / discipline check
- All edits confined to the task file under `.dev/tasks/...` — NO `.claude/` paths touched, NO source code modified (this round only refines task-item instructions, not the swarm code).
- All affected items (Step 2.2 / 2.6 / 2.7) appear in the task's checklist and are in-scope.
- No new findings introduced; item structure (checkboxes, self-containment, blocker valves) preserved.

### Fix-round self-audit
**(a) Reliance:** relied on cycle-1 operational report's already-verified anchors for the unchanged
items; did NOT re-run the full 15-check lens (this round is scoped to the 3 flagged items).
**(b) Independent verification this round:** re-Read `preflight.py:518-533`, `commands.py:780-791`,
`reduce.py:716-724` directly before editing — all three anchors confirmed byte-accurate against
current source. No web research required (local-file-bound); Tavily not invoked.

## FIX-ROUND VERDICT: PASS

I-1 (IMPORTANT) fully addressed with caveat + models-resize + verification clause; both MINOR
clarity items (M-1 emit_contract internal-call, M-2 resume-rehydrate-not-helper) addressed. No
residual findings. The task item Step 2.2 now integrates correctly with the `==4` reset and INV-005
pool guard; an executor following it literally will ship a `--reviewers` flag whose value 4 actually
takes effect.
