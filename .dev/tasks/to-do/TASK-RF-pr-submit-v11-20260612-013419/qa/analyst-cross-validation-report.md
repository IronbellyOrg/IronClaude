# Cross-Validation Report — pr_submit V1.1 Research (Track 1)

**Analysis type:** completeness-verification (cross-validation lens)
**Topic:** pr_submit V1.1 (FR-8/9/10; +2 FSM states; +3 invariants; +1 idempotency set; +4 EventType)
**Date:** 2026-06-12
**Files in scope:** 01..07 (7 research files)
**Lens focus:** Cross-validate claims BETWEEN research files; flag every contradiction.

> Status: COMPLETE.

---

## Files read (all 7 + ground-truth code)

- `research/01-core-modules-current-state.md` (R1)
- `research/02-fsm-transition-runskill-anatomy.md` (R2)
- `research/03-runlog-idempotency-enum-patterns.md` (R3)
- `research/04-skill-refs-scripts-conventions.md` (R4)
- `research/05-test-infra-fixtures-markers.md` (R5)
- `research/06-spec-delta-extraction.md` (R6)
- `research/07-doc-crossvalidate-anchors.md` (R7)

Ground-truth code re-read this turn for adjudication:
- `src/superclaude/pr_submit/run_log.py:26-35` (IDEMPOTENCY_SETS, count comment)
- `src/superclaude/pr_submit/fsm.py:789-793` (the optimistic increment site)
- `src/superclaude/pr_submit/fsm.py:679-802` (run_skill body — transition() call count)
- `src/superclaude/pr_submit/models.py` EventType members (awk count) + the "33" prose sites
- `src/superclaude/pr_submit/recovery.py:25,111` (Branch A target)
- `src/superclaude/commands/auggie-review.md:47-56` (flag table)
- `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md:1-5,36,71` (FSM ownership)

---

## Method

1. Read all 7 research files completely.
2. Read the grounded code sources the orchestrator cited (run_log.py, models.py, fsm/transition, recovery.py, auggie-review.md, the :793 increment site, refs/state-machine.md).
3. For each known discrepancy, determine which research files cover the fact, compare their values, and adjudicate against code.
4. Surface every contradiction with both versions + adjudicated correct value.

---

## Adjudicated discrepancies (the 5 the orchestrator pre-grounded)

### D1 — Idempotency set count: R5 says "EXACTLY 4", R1/R3/R6/R7 say 5 → **5 is correct; R5 is a miscount the builder MUST NOT inherit**

| File | Claim | Where |
|------|-------|-------|
| R1 (01) | `IDEMPOTENCY_SETS` = **5** members, lists all 5 incl. `processed_review_ids` | 01:140, 01:247 |
| R3 (03) | "The 5 idempotency sets", lists all 5 incl. `processed_review_ids` | 03:33, 03:43, 03:208-218 |
| R6 (06) | "currently has 5 sets (→6)" | 06:172, 06:266 |
| R7 (07) | **[CODE-VERIFIED]** tuple = 5 members, all 5 named, "The 5 idempotency sets (§11.4)" comment | 07:25 (claim #5) |
| **R5 (05)** | **"idempotency sets today = EXACTLY 4"** — lists only `processed_finding_ids`, `replied_comment_ids`, `resolved_thread_ids`, `pushed_commit_shas` (**OMITS `processed_review_ids`**) | 05:343-345 |

**Ground truth (re-read this turn):** `run_log.py:26-33` —
```
# The 5 idempotency sets (§11.4).
IDEMPOTENCY_SETS = (
    "processed_review_ids",     # ← the member R5 dropped
    "processed_finding_ids",
    "replied_comment_ids",
    "resolved_thread_ids",
    "pushed_commit_shas",
)
```
Exactly **5** members. R5's "4" arises from omitting `processed_review_ids` (which is folded from `FINDINGS_NORMALIZED` at `run_log.py:179-185`, the least-obvious member).

**ADJUDICATED CORRECT VALUE: 5 today → 6 after V1.1** (adds `auggie_review_invoked`, FR-10.1 / addendum §6.3).

**Severity: IMPORTANT (not critical).** Two mitigating facts:
1. R5 itself flagged the conflict and deferred to R3: *"spec §9.1 says V1.1 adds a '6th set' — but the code has only 4 today … **Builder MUST reconcile the '6th set' wording with R3's run_log source**"* (05:345-349). R5 did not assert "4" as settled truth; it raised it as an open reconciliation.
2. Four independent files (R1/R3/R6/R7) plus live code agree on 5, and the spec target "6th set" only arithmetically closes if the base is 5 (5+1=6), not 4 (4+1=5). The "6th set" spec wording is itself corroborating evidence for base-5.

**Builder action:** Author the run_log.py item as "5 → 6" with the explicit member `auggie_review_invoked`. Do NOT write any "4 → 5" framing. If a test asserts the set count, it must be `len(IDEMPOTENCY_SETS) == 6` post-change (currently no numeric-count test exists for the tuple — see D3 note on enum). The builder should NOT have a test or prose that says "5th set."

---

### D2 — state-machine.md [MOD]: R4 flags it needs a [MOD] though addendum §6.5 omits it → **CONFIRMED internally consistent; builder SHOULD add a state-machine.md [MOD] item, flagged as a spec-coverage gap**

**The claim (R4 §D, 04:96-105):** addendum §6.5 lists only `augment-poll.md` + `loop-guard.md` as [MOD] refs (plus 2 NEW refs), and does NOT name `state-machine.md`. R4 argues state-machine.md nonetheless needs a [MOD] because the new S5a/S5b edges change FSM topology, which state-machine.md exclusively owns.

**Internal-consistency check (does state-machine.md actually own the FSM diagram?):** YES — verified against live source this turn:
- `state-machine.md:1-5`: *"the **one** finite state machine that the `sc:pr-submit` skill drives … There are **not four implementations** — there is a single FSM."* It is the declared single source of FSM topology.
- `state-machine.md:36`: lists `S5_AWAITING_REREVIEW` as a state but has **no** `S5a`/`S5b`.
- `state-machine.md:71`: documents the `S5_AWAITING_REREVIEW → S2_CLASSIFY` increment edge as the only transition out of S5 today.

Adding `S5A_RETRIGGER_REVIEW` / `S5B_AUGGIE_FALLBACK` and their edges (per R2 §1 / R6 §5.4 transition deltas) is unambiguously a topology change. A ref whose stated contract is "the complete enumeration of reachable states" becomes stale/incomplete the moment new reachable states exist that it doesn't list. So R4's claim is internally consistent and corroborated by the same FSM-delta the other files describe.

**Cross-file consistency:** R6 §5.5 (06:188-189) transcribes addendum §6.5 faithfully — it lists augment-poll + loop-guard [MOD] and the 2 NEW refs, and does NOT independently name state-machine.md. So R6 (the spec index) and R4 (the conventions track) are NOT in contradiction: R6 reports what the addendum literally says; R4 reports a gap in what the addendum says vs. what the FSM-single-source invariant requires. R7 (07:36, claim 11a) confirms state-machine.md EXISTS as one of the 8 refs and is a valid [MOD] target file. No file contradicts R4.

**ADJUDICATED: The builder SHOULD add a `refs/state-machine.md` [MOD] item** (define S5a + S5b states and their edges), and SHOULD surface it explicitly as **"spec addendum §6.5 omits state-machine.md but the new S5a/S5b edges require amending it — coverage gap, escalate."** This is consistent with `needs_human_decision`-style surfacing: the addendum is the source-of-truth for intent, but it has an internal omission, so the builder flags rather than silently expanding OR silently dropping. Treat as **Authorized expansion with a flagged spec discrepancy**, not drift.

---

### D3 — EventType count: all files should agree 33 → 37 → **CONFIRMED; no file dissents; the "33" prose count appears in 5 sites (R3 named 3 of them); R5's "no numeric-count test exists" is correct**

**Cross-file agreement on the count:**

| File | Current | Target | Where |
|------|---------|--------|-------|
| R1 (01) | 33 (awk-verified, full member list) | 37 | 01:34, 01:70, 01:247 |
| R2 (02) | (defers to R1/R3 for enum) | — | n/a (fsm scope) |
| R3 (03) | 33 | 37 | 03:16, 03:199-204 |
| R5 (05) | 33 ("EXACTLY 33 today") | 37 | 05:217-226, 05:339-341 |
| R6 (06) | 33 | 37 | 06:163, 06:266 |
| R7 (07) | **[CODE-VERIFIED]** 33 (awk between class boundaries) | 37 | 07:23 (claim #3) |

**Ground truth:** awk count of `^\s+[A-Z_]+ = "` between `class EventType` and `class Severity` = **33**. No file says otherwise. **ADJUDICATED: 33 → 37, unanimous.**

**Where the "EXACTLY N" docstring count appears (the places R3 §4.1 lists vs. ground truth):** R3 (03:199-204) lists three+ count-bearing prose sites: (a) models.py class docstring "EXACTLY 33", (b) models.py module docstring "exactly 33 members", (c) run_log.py ValueError "the 33 §11.3 events" + append() docstring "one of the 33". Ground-truth grep for `33` finds **5** occurrences:
- `models.py:3` — module docstring "exactly 33 members" ✓ (R3 (b))
- `models.py:20` — class docstring "EXACTLY 33 members" ✓ (R3 (a))
- `models.py:69` — a code COMMENT "the 33rd" (`# ... — the 33rd ---`) ← **R3 did NOT enumerate this one explicitly**
- `run_log.py:103` — append() docstring "one of the 33 closed" ✓ (R3 (c))
- `run_log.py:109` — ValueError "not one of the 33 §11.3 events" ✓ (R3 (c))

R1 (01:145, 01:70) also names the run_log.py docstring + ValueError pair and says "RE-GREP `33` across models.py + run_log.py" — which would catch the models.py:69 comment too. **No contradiction, but a minor completeness gap:** the `models.py:69` "the 33rd" comment is a 5th count-bearing site that R3's enumerated list does not call out by itself. The builder must update it to "the 33rd" → semantics (it currently labels `PUSH_ABORTED_OR_NOT_LANDED` as "the 33rd"; after +4 it is still the 33rd member positionally, so this comment may be left as-is OR clarified — it is NOT a "37" target, it's a positional label). **Builder note: grep ALL `33` occurrences (5 sites); 4 are count-claims to bump to 37; `models.py:69` "the 33rd" is a positional label for the 33rd member and is NOT bumped.**

**R5's "no numeric-count test exists today" claim — CONFIRMED.** R5 (05:217-226, 05:339-341) states no test asserts `len(EventType) == 33` numerically; the count lives only in docstrings + the run_log ValueError. R3 (03:24, 03:274) independently agrees ("the load-bearing gate is a test" but flags exact line Unverified; §5.1 says "none of these is self-asserting in source"). R7 does not claim a numeric test exists. **No contradiction — the `len(EventType)==37` assertion is NET-NEW**, the builder establishes it. Consistent across R3/R5/R7.

---

### D4 — fsm dual-surface: R2 says run_skill() re-implements the cycle inline (does NOT call transition()) → **CONFIRMED; no file contradicts; both transition() and run_skill() must be edited in lock-step**

**The claim (R2, 02:14, 02:234, 02:240):** `transition()` (fsm.py:560) and `run_skill()` (fsm.py:679) are two independent surfaces — `run_skill()` re-implements the round cycle as an inline `for cycle_index, cycle_findings in enumerate(cycles)` loop (fsm.py:718) and does NOT call `transition()`. Therefore the spec's new edges must be applied to BOTH or they drift.

**Ground truth:** grep of the `run_skill()` body (fsm.py:679-802) for `transition(` returns **0** matches. `run_skill()` never calls `transition()`. The `:793` increment + the `result.state = MonitorState.X` assignments are all inline state mutations, not `transition()` dispatches. **R2's dual-surface claim is CONFIRMED against code.**

**Cross-file consistency:** R1 (01:225) independently describes the same split — "`transition()` … is a flat `if edge == (...)` lookup table" AND "`run_skill()` … the optimistic increment `result.round_counter += 1` is at fsm.py:793 … inside the cycle loop." R6 §5.4 (06:175-185) lists the transition() edge deltas AND the run_skill() [MOD] (remove :793, add seams) as **separate** build-target bullets — consistent with two surfaces. R5 (05:44-72) drives tests through `run_skill(RunConfig(...))`, never through `transition()` directly for the loop scenarios, corroborating that run_skill is the runtime surface the loop tests assert on. **No file claims run_skill() calls transition(). No contradiction.**

**ADJUDICATED: CONFIRMED.** Builder must emit BOTH a transition()-edge item AND a run_skill()-loop item, and an explicit cross-link note that editing one does not propagate to the other (R2 §6, 02:234). This is the single highest-risk INV-001 coupling (the deferred-increment relocation must preserve `max_rounds=N ⇒ N pushes` in run_skill's inline loop — R2 §5, 02:215-217).

---

### D5 — recovery.py Branch-A: R1 flags hard-resume to S5_AWAITING_REREVIEW may need S5A post-V1.1 → **CONFIRMED unresolved; NO file resolves it; stays an OPEN QUESTION the builder must surface**

**The claim (R1 §RECOVERY, 01:193-203):** recovery.py's Branch A (`resolve_crash_window`) hard-resumes a "landed" crash to `MonitorState.S5_AWAITING_REREVIEW` (01:200, cited at recovery.py:111). With V1.1's `(RESOLVING, "resolved") → S5A_RETRIGGER_REVIEW` [MOD] edge, a crash recovered as "landed" might now need to resume at `S5A_RETRIGGER_REVIEW` (re-trigger comment not yet posted) rather than `S5_AWAITING_REREVIEW`. R1 marks recovery.py as "likely UNCHANGED per spec" but flags the Branch-A hardcode as "a latent interaction … Unverified whether spec intends a recovery change."

**Ground truth:** `recovery.py:25` `BRANCH_A_LANDED = "landed"`; `recovery.py:111` `return BRANCH_A_LANDED, MonitorState.S5_AWAITING_REREVIEW`. grep of recovery.py for `S5A`/`S5a` = **none**. So the Branch-A target is exactly `S5_AWAITING_REREVIEW` as R1 states, and recovery.py has no S5a awareness.

**Does any other file resolve it?**
- R6 (the spec index): addendum §6 build-target list (06:160-194) does **NOT** include recovery.py as a build target. R6 §9.1 (06:262-267) cites recovery.py only for FR-10.4 `--resume` rebuild_state strict-once, NOT for the Branch-A resume-target question. So R6 transcribes that the addendum is silent on a recovery.py edit — it neither resolves nor contradicts R1.
- R7 (07:52, cross-check notes): confirms recovery.py EXISTS and that `rebuild_state` folds are NEW, and notes `record_idempotent`/resume survive — but says nothing about the Branch-A → S5 vs S5a resume target. Does not resolve it.
- R2/R3/R4/R5: recovery.py is out of their scope; none addresses the Branch-A target.

**ADJUDICATED: UNRESOLVED — remains an OPEN QUESTION.** No file (and not the addendum, per R6) resolves whether a "landed" crash should resume at `S5_AWAITING_REREVIEW` (old behavior, but then the re-trigger comment that S5a is responsible for posting never gets posted → the same V1.0 stall bug the build exists to fix) or at `S5A_RETRIGGER_REVIEW` (new, so the recovered run posts the re-trigger). This is a genuine latent seam, NOT a research contradiction. **Builder action:** carry it as an explicit Open Question / `needs_human_decision` review item — do NOT silently default. The semantically-correct resume target is plausibly `S5A_RETRIGGER_REVIEW` (a landed-but-not-yet-re-triggered crash needs the re-trigger), but the addendum does not authorize a recovery.py edit, so this must be flagged for human decision rather than auto-applied (consistent with the "human-decision items must HALT, not auto-default" discipline).

---

## General cross-file consistency checks

### G1 — The `:793` increment site → **CONSISTENT across R1/R2/R6/R7 + live code**

| File | Claim | Where |
|------|-------|-------|
| R1 | "optimistic increment `result.round_counter += 1` is at fsm.py:793 … under the comment at :792 … inside the cycle loop" | 01:225 |
| R2 | "CONFIRMED at fsm.py:792-793 … the ONLY round_counter mutation in the file" | 02:118-127, 02:214 |
| R6 | "remove the optimistic `round_counter += 1` (spec claims line 793)" | 06:183, 06:263 |
| R7 | **[CODE-VERIFIED]** "fsm.py:793 is EXACTLY `result.round_counter += 1`, preceded by comment at :792" | 07:21-22 (claims #1,#2) |

**Ground truth (re-read):** `fsm.py:792` = `# Re-review attributed to our push: tick the monotonic round counter (INV-001).`, `fsm.py:793` = `result.round_counter += 1`, immediately after `result.state = MonitorState.S5_AWAITING_REREVIEW` (:790). **Unanimous and exact.** R2 additionally confirms it is the ONLY `round_counter` mutation site (no other `round_counter +=`/`=` in the file) — a single-site [MOD], surgically localizable. R7 §1 (07:45) adds the useful note that the **:792 comment** must also be removed/rewritten, not just the statement. No contradiction.

### G2 — auggie-review.md flag lines (49/52/55/50) → **CONSISTENT; all EXACT in live source; the seed's "stale" suspicion is itself stale**

| File | Claim | Where |
|------|-------|-------|
| R4 | `--depth quick` :49, `--remediation-offer` :52, `--auggie-model claude-sonnet-4-6` :55 — all exist | 04:163-167 |
| R6 | cites "auggie-review.md:49,50,52,55,26-27,36" as fallback flag sources | 06:265 |
| R7 | **[CODE-VERIFIED]** :49 (`--depth`), :50 (`--post-pr`), :52 (`--remediation-offer`), :55 (`--auggie-model`), :26-27/:36 (`<PR>` target) — **"Line numbers EXACT … No staleness"** | 07:29-33 (9a-9e), 07:47 |

**Ground truth (re-read auggie-review.md:47-56):** `--depth` = line 49, `--post-pr` = line 50, `--remediation-offer` = line 52, `--auggie-model … claude-sonnet-4-6` = line 55. **All four EXACT.** R7 explicitly rebuts the seed-list "stale (~49/~52/~55/~50)" framing: the lines are precise, not approximate. R4 and R7 agree on 49/52/55; R6 adds 50 (`--post-pr`) and 26-27/36 (PR target). **No contradiction.** Minor note: R4 §G (04:166) cites `sc-auggie-review-protocol/SKILL.md:320` for where `--remediation-offer` is honored — that is a *different* file (the protocol SKILL, not the command md) and was not re-verified this turn; it is a supporting pointer, not a count-claim, and not in conflict with any other file. Builder may re-grep it at edit time if it anchors an item.

**One cross-file nuance worth the builder's attention (NOT a contradiction):** R4 §G (04:169) and R6 §2 (06:79-82) both note the fallback uses `--depth quick` going to `/sc:auggie-review` (a review), whereas pr-submit's own `severity-routing.md:47` / `troubleshoot-dispatch.md:27` STOP on `--depth quick --fix` going to `/sc:troubleshoot`. Both files independently conclude these do **not** conflict (different target command, no `--fix`). Agreement, not contradiction — but the builder's `auggie-fallback.md` ref must state the distinction explicitly so a future maintainer doesn't "fix" the apparent clash (R4 04:169).

### G3 — NEW-vs-existing ref/script split → **CONSISTENT across R4/R6/R7 + live `ls`**

| Surface | Status | R4 | R6 | R7 (CODE-VERIFIED) |
|---------|--------|----|----|--------------------|
| `refs/augment-poll.md` | [MOD] (4th `declined` state) | 04:80 | 06:192 | 07:36 (exists) |
| `refs/loop-guard.md` | [MOD] (INV-R1/R2/R3 + fallback_round_counter) | 04:92 | 06:193 | 07:36 (exists) |
| `refs/state-machine.md` | [MOD] **(R4-added, §6.5 omits — see D2)** | 04:96-105 | not in §6.5 | 07:36 (exists, valid target) |
| `refs/review-retrigger.md` | NEW (R1) | 04:186 | 06:190 | 07:37 (absent → create) |
| `refs/auggie-fallback.md` | NEW (R2/R3) | 04:187 | 06:191 | 07:37 (absent → create) |
| `scripts/retrigger-review.sh` | NEW | 04:188 | 06:194 | 07:38 (absent → create) |
| `scripts/poll-augment-review.sh` | existing | 04:25 | — | 07:38 (exists) |
| `scripts/reply-resolve-thread.sh` | existing | 04:26 | — | 07:38 (exists) |

R7 (07:36-38) **[CODE-VERIFIED]** the existing 8 refs + 2 scripts via `ls`, and confirms the 2 NEW refs + 1 NEW script are ABSENT (correctly NEW). R4 and R6 agree on every NEW-vs-MOD assignment **except** state-machine.md, which is exactly discrepancy D2 (R4 adds it as a needed [MOD] beyond §6.5; R6 faithfully reports §6.5 without it). That single divergence is fully adjudicated in D2 and is a spec-coverage gap, not a research contradiction. **All other ref/script split assignments are unanimous.**

### G4 — Other corroborated facts (no disagreement found)

- **MonitorState count 19 → 21:** R1 (01:75, 01:247) is the only file giving a numeric (19→21); R3 §5.2 / R6 §5.1 / R7 claim #4 describe the +2 non-terminal S5a/S5b additions consistent with it; none contradicts. TERMINAL_STATES unchanged at 6 — R1/R3/R7 agree.
- **SkillResult +6 fields:** R1 (01:89), R3 (§4.4, 03:258-266), R6 (§5.1, 06:164), R7 (07:55) list the identical 6 field names + defaults. Unanimous.
- **DetectionContract +3 fields:** R1 (01:125, 01:131), R3 (implicit), R4/R6 (§6.2), R7 (claim #7) agree on `decline_phrase_regex`, `decline_retrigger_regex`, `accepted_trigger_phrases`. Unanimous.
- **`clamp_max_rounds` is NET-NEW in fsm.py:** R1 (01:228), R2 (02:186), R6 (06:184) agree; lives in fsm.py near the gate predicates, `min(effective, hard)`. Unanimous.
- **loop_guard.py source UNCHANGED:** R1 (01:167) and R2 (02:189) agree the fallback reuses the existing `should_halt(fallback_round_counter, 1)` signature — no source change to loop_guard.py, only the ref doc. R7 claim #8 confirms the signature exists. Unanimous.
- **NFR-6 core purity currently CLEAN:** R2 §4 (grep clean), R7 claim #12 (**[CODE-VERIFIED]**, only docstring/comment + redaction-regex mentions) agree. Unanimous.

---

## Contradiction inventory (structured)

| # | Type | Files | Outlier | Adjudicated correct value | Severity | Builder must NOT inherit |
|---|------|-------|---------|---------------------------|----------|--------------------------|
| D1 | Numeric miscount | R5 says 4; R1/R3/R6/R7 + code say 5 | **R5 (05:343-345)** | **IDEMPOTENCY_SETS = 5 today → 6** | IMPORTANT (R5 self-flagged & deferred to R3) | Any "4→5" framing; any "5th set" test/prose |
| D2 | Spec-coverage gap (not a file-vs-file contradiction) | R4 adds state-machine.md [MOD]; addendum §6.5 (via R6) omits it | n/a (addendum omission) | **Add state-machine.md [MOD]; flag as spec gap** | IMPORTANT | Silently dropping S5a/S5b from state-machine.md OR silently expanding without flagging |
| D3 | Completeness nuance | All agree 33→37; `models.py:69` "the 33rd" comment under-enumerated by R3 | none (all consistent) | **33→37; grep all 5 `33` sites; :69 is a positional label, NOT a count to bump to 37** | MINOR | Bumping the `models.py:69` positional "33rd" label to "37th" |
| D4 | (confirmation, no contradiction) | R2 claim; R1/R5/R6 + code corroborate | none | **run_skill() does NOT call transition(); edit BOTH in lock-step** | n/a (confirmed) | Editing only one surface |
| D5 | Open question (unresolved by any file) | R1 flags; R6/R7 neither resolve nor contradict | none | **UNRESOLVED — carry as Open Question / needs_human_decision** | IMPORTANT (latent seam) | Auto-defaulting the Branch-A resume target |

**Net:** exactly **one** genuine file-vs-file factual contradiction (D1, R5's idempotency-set miscount). D2 is a research-flagged spec-coverage gap (consistent reporting; the gap is in the addendum, not between files). D3 is a minor completeness nuance, not a contradiction. D4 is a cross-validated confirmation. D5 is an unresolved open question that no file purports to settle (so not a contradiction). All other cross-cutting facts (G1-G4) are unanimous.

---

## VERDICT: PASS

The 7 research files are **cross-consistent** with exactly one numeric outlier, and that outlier (D1, R5's "4" idempotency sets) was **self-flagged by R5 itself** as needing reconciliation against R3 rather than asserted as settled — so it will not silently mislead the builder provided the builder honors the "5→6" majority+code value. Four files plus live code agree on 5; the spec's own "6th set" target arithmetically requires base-5. No `[CODE-CONTRADICTED]` findings exist (R7 confirms zero). The high-risk facts the build hinges on — the `:793` single increment site, the run_skill/transition dual-surface, the 33→37 enum count, the auggie-review.md flag lines, and the NEW-vs-existing ref/script split — are all unanimous and code-verified.

**Two items the builder MUST carry forward explicitly (PASS is conditional on these being surfaced, not silently resolved):**

1. **D1 adjudication:** write the run_log item as **"IDEMPOTENCY_SETS 5 → 6"** with member `auggie_review_invoked`; do NOT inherit R5's "4". Any count test asserts 6.
2. **D2 + D5 surfacing:** add a **state-machine.md [MOD]** item flagged as an addendum §6.5 coverage gap (D2), and carry the **recovery.py Branch-A resume-target** question as an explicit Open Question / `needs_human_decision` (D5) — do not auto-default either.

No re-research of the 7 files is required; the research set is complete and accurate enough to build from once D1/D2/D5 are encoded as above.

### Adjudicated-correct-value summary (quick reference)

- **Idempotency sets:** 5 today → 6 after V1.1 (NOT 4→5). R5 miscounted.
- **state-machine.md:** needs a [MOD] (S5a/S5b edges) — addendum §6.5 omits it; flag as spec gap.
- **EventType:** 33 today → 37. Unanimous. Five `33` prose sites; bump 4 count-claims, leave the `models.py:69` positional "33rd" label.
- **fsm dual-surface:** run_skill() does NOT call transition() — confirmed; edit both in lock-step.
- **recovery.py Branch-A:** unresolved by all files — resumes to S5_AWAITING_REREVIEW today; whether it should resume to S5A post-V1.1 is an Open Question for human decision.
