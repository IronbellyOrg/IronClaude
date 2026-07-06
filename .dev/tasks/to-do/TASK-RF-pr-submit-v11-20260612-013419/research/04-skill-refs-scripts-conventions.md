# Research Track 04: Skill / Refs / Scripts — File Inventory + Patterns & Conventions

**Track:** pr_submit V1.1 extension — SKILL/refs/scripts surface + auggie-review.md command
**Scope:** `src/superclaude/skills/sc-pr-submit-protocol/` (SKILL.md, 8 refs, 2 scripts) + `commands/auggie-review.md` + one example hook
**Status:** Complete

---

## A. File Inventory (verified `ls`/`wc`)

Package root: `src/superclaude/skills/sc-pr-submit-protocol/`

| File | Lines | Role |
|------|-------|------|
| `SKILL.md` | 132 | Orchestrator — Waves 0-7, Output Contract, VAL gates, Will/WillNot/Error tables |
| `refs/detection-contract.md` | 50 | Probe-locked Augment detection contract (YAML); build BLOCKS arming while `locked:false` |
| `refs/augment-poll.md` | 49 | **[MOD target]** Poll surface + interval/timeout/backoff; gets 4th `declined` state |
| `refs/severity-routing.md` | 55 | Re-grade (defer to auggie rubric) + NEW C3 tier→troubleshoot route map |
| `refs/finding-verify.md` | 61 | Verify-before-remediate (C3a) — spawn `evidence-validator`, verified/unverified |
| `refs/troubleshoot-dispatch.md` | 51 | C3b seeding contract — verified findings → `/sc:troubleshoot` |
| `refs/state-machine.md` | 114 | **[CONFIRM-MOD]** The single FSM; states, ordinal gate table, INV-016 conjunction |
| `refs/thread-reply.md` | 74 | C4 reply (REST `in_reply_to`) + resolve (GraphQL `resolveReviewThread`) |
| `refs/loop-guard.md` | 78 | **[MOD target]** INV-001 round-counter + §11 run-log schema; gets INV-R1/R2/R3 + fallback_round_counter |
| `scripts/poll-augment-review.sh` | 60 | Single `gh` poll → one JSON line; fail-soft |
| `scripts/reply-resolve-thread.sh` | 102 | REST reply THEN GraphQL resolve; idempotent |

8 refs confirmed (spec §6.5 names augment-poll + loop-guard as [MOD] and 2 NEW). **state-machine.md MOD question resolved in §D below.**

---

## B. SKILL.md — Wave Structure, Output Contract, Lazy-load Mechanism

### Wave / Phase table (verbatim, `SKILL.md:72-81`)

```text
Wave 0: Open PR + verify target   ← (no ref; gh pr create --repo, pre-PR checks)
Wave 1: Arm + poll                ← loads refs/detection-contract.md (arm gate) + refs/augment-poll.md
Wave 2: Classify + re-grade       ← loads refs/severity-routing.md
Wave 3: Verify-before-remediate   ← loads refs/finding-verify.md
Wave 4: Diagnose + (L2+) fix      ← loads refs/troubleshoot-dispatch.md
Wave 5: Validate                  ← the VAL validator (§10 gate list, below)
Wave 6: (L3) push + reply + resolve ← loads refs/thread-reply.md
Wave 7: Loop / terminate          ← loads refs/loop-guard.md
```

**Lazy-load mechanism (header `SKILL.md:70`):** "refs are LAZY-loaded per wave, never pre-loaded." Each wave bullet (`SKILL.md:83-90`) names exactly which ref(s) it loads. The V1.1 NEW refs (`review-retrigger.md` R1, `auggie-fallback.md` R2/R3) must be slotted into this lazy-load table — the builder must add a row/clause naming the wave that loads each new ref.

### Wave 6 (L3 push + reply + resolve) — verbatim `SKILL.md:89`

> **Wave 6 (L3 only):** load `refs/thread-reply.md`. The deterministic core DECIDES (evaluates the INV-016 conjunction, records the write-ahead push triad `push_decision` → `push_initiated` (fsynced BEFORE the push) → `push_completed`, keyed on the PRE-push idempotency key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>`); the SKILL performs the actual `git push origin <target_sha>:<target_branch>` (never `upstream`, never `master`) ONLY when the conjunction holds, then reply (citing `applied_edits` status — `applied_edits==0` says "no code change applied", never "resolved") and resolve via `scripts/reply-resolve-thread.sh` (reply FIRST, then resolve).

**V1.1 [MOD] target:** spec §6.5 wants Wave 6 to also post the `auggie review` re-trigger comment (S5a) BEFORE polling (S5). The current Wave 6 has NO re-trigger comment surface — it only pushes/replies/resolves. The builder must insert an S5a step (post `auggie review` via `scripts/retrigger-review.sh`) into Wave 6's sequence, between push-completed and the S5/poll re-entry. NEW Wave 6b (decline fallback) must be added as a new wave bullet after `SKILL.md:89`.

### Wave 7 (loop / terminate) — verbatim `SKILL.md:90`

> **Wave 7:** load `refs/loop-guard.md`; the round counter ticks only at `S5_AWAITING_REREVIEW → S2_CLASSIFY`; HALT at `round_counter >= max_rounds`.

This is the loop/terminate gate. The V1.1 fallback_round_counter (separate from round_counter) and INV-R1/R2/R3 live in `refs/loop-guard.md`; Wave 7's bullet may need a clause referencing the fallback counter's HALT condition.

### Output Contract `status` enum (verbatim `SKILL.md:61`)

> `terminal_clean` / `terminal_max_rounds` / `terminal_halted` / `terminal_timeout` / `terminal_failed` / `proposed` / `halt_before_push`

7 status values. V1.1 §6.5 introduces a `declined` augment state + decline-fallback path — the builder should check whether a new terminal status (e.g. `terminal_declined_fallback_exhausted`) needs adding here, and whether the run-log `EventType` enum (currently EXACTLY 33 members, `loop-guard.md:53-62`) must grow for fallback events. **The 33-member count is asserted as a closed enum — any new event type is a breaking [MOD] to loop-guard.md §11.3.**

### Full Output Contract fields (`SKILL.md:59-68`)

`status` (enum), `pr_url`, `round_counter` (int), `push_count` (int), `reply_count` (int), `summary_posted` (bool), `applied_edits` (int), `run_log_path` (string). V1.1 may add `fallback_round_counter` and/or `fallback_invoked` fields.

### VAL validation gate list (`SKILL.md:97-103`) — owned by SKILL, not core

VG-1 targeted pytest → VG-2 cross-cut `make test` → VG-3 `make lint` (ruff check) → VG-4 `uv run ruff format --check src/ tests/` (SEPARATE gate) → VG-5 `make verify-sync` (skill-self-edits) → VG-6 PR-target check. A validation retry does NOT increment `round_counter` (`SKILL.md:104`).

---

## C. The 8 refs — 1-line roles + [MOD] details

1. **detection-contract.md** — Probe-locked YAML contract (`augment_bot_login`, `emission_shape`, `findings_locus`, `locked:false`). Build BLOCKS arming while `locked:false` (T-210). NOT a V1.1 [MOD] target.

2. **augment-poll.md** **[MOD]** — Poll surface (`gh pr view ... --json number,url,headRefName,headRefOid,baseRefName,reviews,comments`, `augment-poll.md:16`) + REST surfaces + interval≥30s/timeout-1800s/exponential-backoff. **Currently THREE classification states:** "three states no-review / clean / findings (T-201/202/203)" (`augment-poll.md:34`). **V1.1 adds a 4th `declined` state** — the builder must extend this 3-state classifier line to 4-state (no-review / clean / findings / **declined**), keying decline detection on the probe-locked contract. The division-of-labour seam (`augment-poll.md:43-49`) stays: script polls, FSM decides — so decline ARITHMETIC stays in core, decline raw-surfacing in the script.

3. **severity-routing.md** — Grade (defer to `sc-auggie-review-protocol/refs/severity-rubric.md`) + route (tier→troubleshoot map). STOP: never `--depth quick --fix` (`severity-routing.md:47`). NOT a V1.1 [MOD] target.

4. **finding-verify.md** — Verify-before-remediate (C3a); spawns `evidence-validator` agent; verified→dispatch, unverified→report-only-no-round. NOT a V1.1 [MOD] target.

5. **troubleshoot-dispatch.md** — C3b seeding for VERIFIED findings → `/sc:troubleshoot` (`--scope <file:line>`, `--type <category>`, route). NOT a V1.1 [MOD] target.

6. **state-machine.md** **[CONFIRM-MOD → YES, see §D]** — The single FSM. States, ordinal gate table (G-arm/G-edit/G-push), INV-016 5-predicate push conjunction, `S5_AWAITING_REREVIEW → S2_CLASSIFY` increment edge.

7. **thread-reply.md** — C4 reply (REST `in_reply_to`) FIRST then resolve (GraphQL `resolveReviewThread`); `applied_edits==0` → "no code change applied" never "resolved" (`thread-reply.md:18-20`). The single-summary-thread surface uses `gh api --method POST repos/IronbellyOrg/IronClaude/issues/<N>/comments` (`thread-reply.md:72`) — **this is the exact surface shape `retrigger-review.sh` must mirror** (issue-comment POST). NOT itself a V1.1 [MOD] target but is the closest convention template for R1's re-trigger comment.

8. **loop-guard.md** **[MOD]** — INV-001 round-counter (single increment site `S5_AWAITING_REREVIEW → S2_CLASSIFY`, `>=` gate, monotonic, default 2/cap 5) + §11 run-log schema (5 file locations, **EXACTLY 33 EventType members**, 5 idempotency sets). **V1.1 adds INV-R1/R2/R3 + `fallback_round_counter`** — a SEPARATE counter from `round_counter`, with its own increment site and clamp. Builder must: (a) add INV-R1/R2/R3 normative blocks, (b) define `fallback_round_counter` increment edge + strict-once clamp, (c) likely grow the 33-member EventType enum for fallback events (decline_detected, retrigger_posted, fallback_invoked) — this is a breaking change to the "EXACTLY 33" assertion and its test.

---

## D. state-machine.md — DOES it need a [MOD]? → **YES (CONFIRMED)**

Spec §6.5 lists augment-poll + loop-guard as [MOD] and 2 NEW refs, and does NOT name state-machine.md. **However, the new S5a (post `auggie review`) and S5b (decline-fallback) edges directly touch FSM topology, which is owned exclusively by state-machine.md.** Evidence:

- The FSM is "the **one** finite state machine" and "the single source for all `--monitor` ordinals" (`state-machine.md:1-4`). Any new state/edge MUST be defined here or the FSM is no longer the single source.
- Current states (`state-machine.md:21-38`) include `S5_AWAITING_REREVIEW` but NO `S5a`/`S5b`. The V1.1 S5a (re-trigger comment) and S5b (decline fallback re-entry) edges are absent.
- INV-001's increment edge `S5_AWAITING_REREVIEW → S2_CLASSIFY` (`state-machine.md:70-72`) is the ONLY transition out of S5 today. Adding an S5a emission step + an S5b decline branch out of S5 is a topology change.
- The §5.2 ordinal gate table (`state-machine.md:54-58`) and §5.4 "why a machine not nested ifs" (`state-machine.md:108-114`) both assert the FSM is the complete enumeration of reachable states — new edges that aren't reflected here break that completeness claim and the C6 row-by-row table assertions.

**Recommendation for the builder:** add a state-machine.md [MOD] item even though §6.5 omits it. Minimum: define S5a (emit re-trigger comment, edge `S4_PUSHING/S6_REPLYING → S5a → S5_AWAITING_REREVIEW`) and S5b (decline detected → fallback re-entry under clamp → re-enter S2..S6 once). Flag "spec §6.5 omits state-machine.md but the new edges require it — escalate as a coverage gap." **This is the single most important finding of this track: a NEW-ref-only V1.1 plan that touches S5a/S5b without amending state-machine.md will produce an FSM whose single-source-of-truth invariant is violated.**

---

## E. Both scripts — bash conventions (the shape `retrigger-review.sh` MUST match)

### Shared conventions (both `poll-augment-review.sh` + `reply-resolve-thread.sh`)

| Convention | Evidence |
|------------|----------|
| Shebang | `#!/usr/bin/env bash` (`poll:1`, `reply:1`) |
| Strict mode | `set -euo pipefail` (`poll:18`, `reply:18`) — note: **`-u` is part of `-euo`** (offer-pr-review.sh uses bare `set -u`; these skill scripts use full `set -euo pipefail`) |
| `die()` helper | `die() { printf 'NAME: %s\n' "$1" >&2; exit "${2:-1}"; }` (`poll:20`, `reply:20`) |
| Arg parsing | `while [ $# -gt 0 ]; do case "$1" in ... esac done` long-flag loop (`poll:23-28`, `reply:28-38`) |
| Required-arg guards | `[ -n "$X" ] \|\| die "missing required ..." 2` (`poll:31`, `reply:40-43`) |
| Dependency check | `command -v gh >/dev/null 2>&1 \|\| die "gh CLI not found on PATH" 2` + same for `jq` (`poll:32-33`, `reply:44-45`) |
| **gh --repo pin** | `gh pr view "$PR" --repo IronbellyOrg/IronClaude` (`poll:36`); `gh api "repos/IronbellyOrg/IronClaude/pulls/${PR}/comments"` (`poll:46`, `reply:49`); GraphQL `-f owner=IronbellyOrg -f repo=IronClaude` (`reply:68`) |
| Fail-soft / fail-open | poll: `... 2>/dev/null \|\| true` then emit `state:"polling"` on empty (`poll:36-43`); never hard-fails a transient poll |
| stdin/file JSON | reply reads body via `--body-file` → `-f body="$(cat "$BODY_FILE")"` (`reply:50`) |
| SoT comment | "Source of truth lives in src/superclaude/; do not edit the .claude/ mirror." (`poll:16`, `reply:16`) |
| Header block | Purpose/Usage/Output/Exit/Spec banner comment (`poll:3-14`, `reply:3-14`) |

### Exit-code conventions

- **`poll-augment-review.sh`:** `exit 0` always on a completed poll (fail-soft); `exit 2` on usage error (`poll:6-7,10`).
- **`reply-resolve-thread.sh`:** `exit 0` success/idempotent-skip; `exit 2` usage error; `exit 3` permissions HALT (resolve needs PR read+write) (`reply:11-12`).

### The exact surface `retrigger-review.sh` should emit (spec §6.5 NEW)

One issue-comment POST. The existing template is `thread-reply.md:72`:
```bash
gh api --method POST repos/IronbellyOrg/IronClaude/issues/<N>/comments -f body=...
```
So `retrigger-review.sh` core should be (matching §6.5):
```bash
gh api --method POST repos/IronbellyOrg/IronClaude/issues/<N>/comments -f body="auggie review"
```
Wrapped in the shared shape: `#!/usr/bin/env bash` + `set -euo pipefail` + `die()` + `--pr <N>` arg loop + `command -v gh`/`jq` guards + `--repo`/`repos/IronbellyOrg/IronClaude` pin + SoT footer comment + fail-soft `exit 0` / usage `exit 2`. **Per memory `reference_augment_review_triggers.md`: a manual `auggie review` PR comment is exactly the documented re-trigger surface — pushes do NOT re-trigger Augment, so this comment is the load-bearing re-trigger mechanism for INV-R1.**

---

## F. gh / repo-pin discipline — CONFIRMED across all surfaces

Every `gh`/`gh api`/`gh api graphql` call in the package pins the fork. Audit:

- `augment-poll.md:8-9` explicit rule: "Every `gh`/`gh api` call below pins `--repo IronbellyOrg/IronClaude` (FR-1.3 / AC-7). A bare `gh` without `--repo` is a defect (T-104 greps for it)."
- `augment-poll.md:16,27-29` — all `gh pr view`/`gh api` pinned.
- `thread-reply.md:5` — "Every call pins the fork (`--repo IronbellyOrg/IronClaude` for `gh pr`; `repos/IronbellyOrg/IronClaude/...` path for `gh api`)."
- `thread-reply.md:12,40-49,55-57,72` — REST replies, GraphQL queries (`-f owner=IronbellyOrg -f repo=IronClaude`), issue-comment POST all pinned.
- `poll-augment-review.sh:36,46` — pinned. `reply-resolve-thread.sh:49,68` — pinned.
- SKILL.md Wave 0 (`SKILL.md:83,108`) — `gh pr create --repo IronbellyOrg/IronClaude`.

**Verdict:** repo-pin discipline is uniform and explicitly tested (T-104 greps for bare `gh`). `retrigger-review.sh` MUST inherit this — a bare `gh api .../comments` without the `repos/IronbellyOrg/IronClaude` path is a T-104-class defect. This aligns with the CLAUDE.md ABSOLUTE RULE (PR target = fork, never upstream).

---

## G. auggie-review.md command (R2 fallback target) — flag surface CONFIRMED

The V1.1 decline-fallback (R2/R3) hands off to `> Skill sc:auggie-review-protocol` with flags `--depth quick --remediation-offer --auggie-model claude-sonnet-4-6`. **All three flags exist on the command surface:**

- `--depth quick` — `auggie-review.md:49` ("`quick` (auggie single-pass, ~2min)").
- `--remediation-offer` — `auggie-review.md:52` (default `true`; offers `/sc:design`→`task-builder`→`/sc:reflect` chain). Protocol honors it at `sc-auggie-review-protocol/SKILL.md:320` (gated on `--remediation-offer AND critical+high > 0`).
- `--auggie-model claude-sonnet-4-6` — `auggie-review.md:55` (exact example given is `--auggie-model claude-sonnet-4-6`).

**Critical cross-check for the auggie-fallback.md (R2/R3) ref:** the fallback uses `--depth quick`, but pr-submit's OWN severity-routing.md:47 + troubleshoot-dispatch.md:27 STOP on `--depth quick --fix`. **These do NOT conflict** — the STOP is on `--depth quick` to `/sc:troubleshoot --fix`, whereas the fallback's `--depth quick` goes to `/sc:auggie-review` (a review, no `--fix`). The builder's auggie-fallback.md must make this distinction explicit so a future maintainer doesn't "fix" the apparent contradiction. The "do NOT take the App's augment-review bait" rationale (R2) means: when Augment's own bot posts an `auggie review`-style comment, pr-submit must NOT treat it as the operator-initiated re-trigger; the fallback path is pr-submit invoking its OWN `> Skill sc:auggie-review-protocol`, distinct from the Augment App.

### Activation pattern for the fallback handoff

The command's Activation block (`auggie-review.md:67-71`) is `> Skill sc:auggie-review-protocol`. The R2/R3 fallback in pr-submit SKILL.md Wave 6b should invoke the SKILL directly (`> Skill sc:auggie-review-protocol`) with the flag string, NOT shell out to the command — matching how Wave 4 already does `> Skill sc:troubleshoot-protocol` (`SKILL.md:87`).

---

## H. Builder-facing item summary (modification vs creation)

**[MOD] items:**
1. `SKILL.md` — Wave 6: insert S5a (post `auggie review` re-trigger before poll). NEW Wave 6b bullet (decline fallback: strict-once gate → `> Skill sc:auggie-review-protocol --depth quick --remediation-offer --auggie-model claude-sonnet-4-6` → re-enter Waves 2-6 once under clamp). Possibly extend Output Contract `status` enum + add `fallback_round_counter`/`fallback_invoked` fields. Add lazy-load rows for the 2 NEW refs.
2. `refs/augment-poll.md` — 3-state classifier (`:34`) → 4-state (+`declined`).
3. `refs/loop-guard.md` — add INV-R1/R2/R3 + `fallback_round_counter` (separate increment site + strict-once clamp); likely grow the EXACTLY-33 EventType enum (`:53-62`) for fallback events.
4. `refs/state-machine.md` — **[ADD, beyond §6.5]** S5a + S5b edges (FSM single-source invariant requires it). Flag as spec-coverage gap.

**[NEW] items:**
5. `refs/review-retrigger.md` (R1) — re-trigger comment surface + watermark + INV-R1.
6. `refs/auggie-fallback.md` (R2/R3) — decline detection, strict-once, clamp, re-entry, flag table, "don't take the App's bait" rationale.
7. `scripts/retrigger-review.sh` — one pinned `gh api --method POST repos/IronbellyOrg/IronClaude/issues/<N>/comments -f body="auggie review"`, in the shared bash shape (§E).

**Post-edit gates (from VAL §10):** any SKILL/refs/scripts edit triggers `make sync-dev` → `make verify-sync` (VG-5); scripts should be `chmod +x` (both existing scripts are `-rwxr-xr-x`).

---

## I. Unverified / open questions for the builder

- **Unverified:** exact new `status` enum value name for decline-fallback-exhausted (spec §6.5 not read by this track — owned by R6). The builder should reconcile with the R6 spec-matrix track.
- **Unverified:** whether `fallback_round_counter` shares `max_rounds` or gets its own cap (strict-once implies cap=1, but confirm against R3/loop-guard python core via R1-R3 tracks).
- **Confirmed-but-flag:** state-machine.md [MOD] is required by FSM-single-source invariant but NOT named in §6.5 — treat as a spec discrepancy to surface.
