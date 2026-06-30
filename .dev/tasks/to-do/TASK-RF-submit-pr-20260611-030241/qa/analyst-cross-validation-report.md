# Cross-Validation Report — sc:submit-pr Research (Track 1)

**Analysis type:** completeness-verification (lens: cross-validation)
**Date:** 2026-06-11
**Research dir:** `.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/research/`
**Spec:** `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md`
**Files cross-validated:** 01..07 (all read in full)
**Methodology:** Each ambiguous or potentially-conflicting claim was verified against the
actual repo (`Makefile`, `.claude/settings.json`, `.claude/hooks/`, `pyproject.toml`) and the
merged-spec, NOT trusted from the research prose. No web research (none authorized; none needed).

---

## VERDICT: **PASS**

The seven research files are **mutually consistent** on every load-bearing cross-cut. The three
"potential contradiction" seams the brief flagged (hook sync, troubleshoot edit-ownership, Python
location) all resolve to **agreement** when checked against the repo and spec. No file contradicts
another on a fact that would mislead the task builder. Findings below are (a) confirmed agreements,
(b) two minor count/wording discrepancies that do NOT rise to contradictions, and (c) one factual
imprecision in R1 that the builder should not propagate. None block task-file construction.

---

## Cross-check 1 — R1 (Python "core" stance) vs R4 (`src/superclaude/submit_pr/` + `--cov` correction)

**Verdict: CONSISTENT. No conflict on where Python lives.**

- R1 explicitly **defers the Python-core-module question to R4** and does NOT assert a competing
  location: 01-component-inventory.md:155-156 ("R4 owns test infra + the deterministic-core-module
  question … not duplicated here") and the test-inventory note at :154-156. R1 only inventories the
  **skill-package** markdown/bash files under the hyphenated `skills/sc-submit-pr-protocol/`.
- R4 owns and answers it: the deterministic core is a **real importable underscored package**
  `src/superclaude/submit_pr/` (04-test-infra:25-54), with the hyphenated skill dir holding only
  SKILL.md + bash. R4 reconciles the two as the **swarm split** precedent (skill `sc-bare-review` ↔
  importable `superclaude.cli.swarm`), 04:140-142.
- **No overlap/collision:** R1's paths are all `skills/sc-submit-pr-protocol/**` (markdown/bash) +
  `tests/submit_pr/`; R4's added path is `src/superclaude/submit_pr/**` (Python). They occupy
  disjoint trees by design. R1 never claims the FSM logic lives *in* the skill dir as Python.

**`--cov` correction — VERIFIED AGAINST SPEC, both researchers agree it is a defect:**
- Spec literally contains the broken target: `merged-spec.md:1025` (and §18.1) →
  `--cov=superclaude.skills.sc-submit-pr-protocol` (confirmed by direct grep — hyphens present).
- R4 flags it as unresolvable and corrects to `--cov=superclaude.submit_pr` (04:56-63, 281-285).
- R1 echoes the corrected target without contradiction (it cites R4 as owner).
- **Repo confirmation:** `pyproject.toml [tool.coverage.run] source = ["src/superclaude"]` (R4 cite
  04:144, :251) means a new `src/superclaude/submit_pr/` is auto-covered — R4's reasoning is sound.
  Coverage instruments only `.py`, so the hyphenated module path could never produce numbers.

→ **No contradiction.** R1 and R4 agree; R4 is the authoritative owner and its correction is
spec-grounded and repo-verified.

---

## Cross-check 2 — R1 vs R2 vs R5 on the hook (`offer-pr-review.sh`) sync + settings.json

**Verdict: CONSISTENT after repo verification — R5 is correct; R1's blanket "hooks NOT mirrored"
wording is FACTUALLY IMPRECISE and must not be propagated by the builder.**

This was the brief's flagged "real potential contradiction." I verified it against the Makefile
directly rather than trusting any researcher.

**Ground truth (Makefile `sync-dev` target, lines 137-142):**
```make
@mkdir -p .claude/hooks
@for hook in src/superclaude/hooks/scripts/*.sh; do \
    cp "$$hook" ".claude/hooks/$$name"; \
    chmod +x ".claude/hooks/$$name"; \
```
→ `make sync-dev` **DOES** copy every `src/superclaude/hooks/scripts/*.sh` to `.claude/hooks/<name>`,
**flattening** the `scripts/` subdir. `verify-sync` enforces the pairing bidirectionally
(Makefile:255-275, including the "MISSING in .claude/hooks/ (run 'make sync-dev')" check at :259).

**How each researcher characterized it:**

| File | Claim | Accurate? |
|------|-------|-----------|
| **R5** | 05:168-174 treats hooks as auto-synced by `make sync-dev` (Makefile:108-135); the discoverability checklist relies on sync-dev with no Makefile edit. | **CORRECT** — matches Makefile:137-142. |
| **R2** | Flags it as an **OPEN QUESTION** (02:493-502, :542-544): "Does `make sync-dev` copy `hooks/`? … Builder must grep the Makefile … do NOT assume. (This R2 pass did not read the Makefile)." | **CORRECT (honest non-claim)** — R2 explicitly declines to assert and defers to R1/R4. Not a contradiction; an unanswered question that R5 + this report answer. |
| **R1** | "hooks are NOT mirrored to `.claude/` the way skills/refs are (only the rubric copy was found)" (01:124-128, :201-203). | **FACTUALLY IMPRECISE.** Hooks ARE mirrored — just flattened (`scripts/` dropped) and the local `.claude/hooks/` happened to be **stale** at R1's observation time. |

**Why R1 reached the wrong observation (verified):** the live `.claude/hooks/` listing currently
holds only `auggie-flag-clear.sh` + the seven `freshness-*.sh` — it is **missing** `offer-pr-review.sh`,
`reject-workspace-writes.sh`, and `sc-recommend-phase0.sh` even though `.claude/settings.json:10,21,34`
registers all three. That is **local sync-staleness** (sync-dev not re-run after those hooks landed in
`src/`), NOT evidence that hooks aren't mirrored. R1 generalized a stale-snapshot observation into a
false rule.

**Is this a contradiction between research files?** **No — it is a single-file factual error, not a
disagreement where two files assert opposite facts the builder must choose between.** R2 didn't claim
hooks are unsynced (it asked); R5 claimed they ARE synced (correct). Only R1's *wording* is wrong, and
R1 itself hedges ("sync behavior … should be verified by the build … defer to R5", 01:127, :203). The
net guidance across all three, once R5's correct answer is taken, is coherent.

**The one thing all three AGREE on and is CORRECT:** the **C5 edit is `src/`-only** — edit
`src/superclaude/hooks/scripts/offer-pr-review.sh`, run `make sync-dev`, and **NEVER `git add
.claude/hooks/...`** (R1 01:128,:201-203; R2 02:470-476; R5 05:233-244). This is the load-bearing
staging rule and it is unanimous and correct.

**settings.json — does it need editing? CONSISTENT and CORRECT:**
- The hook is **already registered** (`.claude/settings.json:34` →
  `$CLAUDE_PROJECT_DIR/.claude/hooks/offer-pr-review.sh`, verified). C5 is an **EDIT to an
  existing registered hook**, so **no settings.json change is required**.
- R2's rule "edit `.claude/settings.json` ONLY if a NEW hook is registered" (02:432-435, :491)
  is correct and correctly **does not** fire for C5 (it's an edit, not a new hook).
- R5 says the same (05:35: "two source files" — command + skill; hook edit is to an existing file).

→ **Builder action:** propagate R5's correct sync model (hooks ARE synced, flattened). Override R1's
"hooks NOT mirrored" sentence. Keep the unanimous `src/`-only / never-stage-`.claude/hooks/` rule.
Do NOT add a settings.json edit item for C5.

---

## Cross-check 3 — R3 vs R5 on `/sc:troubleshoot` (Tier-3 won't auto-apply; submit-pr owns edits)

**Verdict: CONSISTENT — R3 and R5 AGREE, and the spec FSM itself confirms the separation. No
conflict on dispatch flags.**

- **R3** (03-reuse-surfaces:155-158, :207, :218): `--fix` only *authorizes* Tier 3; it does NOT
  auto-apply. Tier-3 builds an MDTM task file and **STOPS** (user runs `/task`); "auto-execute the
  Tier-3 task" is in R3's "Do NOT" column.
- **R5** (05-integration-points:144-154, :286-290): troubleshoot's Tier 3 is opt-in/user-gated and
  deliberately refuses to auto-apply edits; therefore `sc:submit-pr` "must own edit application at
  L2/L3" — it uses troubleshoot for *diagnosis* and applies the fix within its own FSM. R5 calls this
  "the single biggest wiring seam."
- **Spec confirms the separation (verified, §5.1 FSM, merged-spec.md:258-300):** the state machine has
  **`S3_DIAGNOSE ← /sc:troubleshoot`** as a distinct state, then a **separate** `S3_FIXING (worktree
  edits)` state gated by `G-edit: ordinal>=2`. The spec architecture itself puts the edit application
  in submit-pr's FSM, not inside troubleshoot. So R3 and R5 are not merely consistent with each other —
  they are both faithful to the spec.

**Dispatch flags — CONSISTENT, and R3 adds a spec-correcting caveat that R5 does not contradict:**
- Both agree on the FR-3.2 route map: Medium → `troubleshoot --fix`; High/Critical →
  `troubleshoot --depth deep --fix`. Verified at spec:190 (T-310/T-311/T-312).
- R3's extra finding (03:148-158, :221): **`--depth quick` + `--fix` is a troubleshoot STOP/conflict**
  (`sc-troubleshoot-protocol/SKILL.md:131`), so the Medium route must be bare `--fix` (defaults to
  `--depth standard`), never `--depth quick --fix`. R5 doesn't mention the conflict but also never
  proposes `--depth quick`, so there is **no contradiction** — R3 simply has the deeper flag-contract
  detail. Builder should honor R3's caveat.

→ **No contradiction.** R3 (reuse/flags) and R5 (runtime wiring) describe the same seam from two angles
and both match the spec FSM. The "submit-pr owns the edits" conclusion is unanimous and spec-grounded.

---

## Cross-check 4 — R6 (DET probe HALT) vs spec §18.4 (synthetic fixtures unblock other steps)

**Verdict: CONSISTENT — R6's HALT-encoding and the synthetic-fixtures-unblock model are
complementary, not conflicting, and both match the spec verbatim.**

- **R6** (06-detection-probe:74-117, :298-299): the DET probe is a manual operator step that **cannot
  run now** (zero captured Augment GitHub-App JSON in the repo; `find .dev -iname '*augment*'` empty)
  and must be encoded as a **`needs_human_decision` build-step-0 item that writes PENDING + HALTs**,
  never auto-locks. Acceptance = `detection-contract.md` `locked: true` + a real `probe_evidence` path;
  T-210 mechanically enforces the gate.
- **R6 explicitly reconciles HALT with not-blocking-everything** (06:104-111): "**Synthetic fixtures
  unblock everything else (§18.4).** All of steps 2–5 of the build DAG are internal-pure and testable
  with synthetic `tests/submit_pr/fixtures/*.json` … zero network. Once the real probe completes, a
  schema-validation test re-asserts fixture parity … keep the `locked` gate as the only thing the probe
  unblocks."
- **Spec verification (merged-spec.md):**
  - §3 DAG step [0] is a **HARD GATE** (spec:134, :148): "step 1 cannot begin until
    `detection-contract.md.locked == true`." Matches R6's HALT.
  - §3:149 (verified): "Steps 2–5 are internal-pure and testable with fixtures (no network)." — matches
    R6's "only the lock is gated."
  - §18.4 (verified): "Fixtures derive from the R1 empirical probe once completed. Until then they are
    synthetic but follow the expected GitHub API response schema; a schema-validation test asserts
    parity after the probe regenerates them from real data." — **verbatim** matches R6.
- **R1 agrees** the contract ships `locked:false` and the build blocks arming until R1 flips it
  (01:50, :206-207). **R5 agrees** the run-log/resume is the durability layer (05:268-276). No file
  contradicts the HALT-but-fixtures-unblock model.

→ **No contradiction.** The HALT gates **only the live-arming/lock**, while synthetic fixtures unblock
the pure FSM/router/loop-guard/reply build+test now. R6 and the spec are in exact agreement.

---

## Cross-check 5 — Severity tier names across R3 and the spec (Critical/High/Medium/Low/Nit)

**Verdict: CONSISTENT — identical 5-tier vocabulary in R3, the reused rubric, and the spec.**

- **R3** (03:30-38) lists the five tiers from `severity-rubric.md:12-61`: 🔴 Critical / 🟠 High /
  🟡 Medium / 🟢 Low / 💬 Nit.
- **Spec** uses the same names in the routing rule (verified spec:190, FR-3.2): "Medium → … ;
  High/Critical → … ; **Low/Nit** → report only." Same five tokens, same casing.
- **R1** references the rubric as the reuse source (01:96-105, :193) without renaming tiers.
- **No competing tier scheme** appears in any file. R3 explicitly warns against inventing a new tier
  scheme (03:216 "Do NOT … invent a new tier scheme").

→ **No contradiction.** Tier vocabulary is unanimous and spec-aligned.

---

## Cross-check 6 — File-count / test-count agreement (spec: 115 tests, 21 test files, 18 fixtures)

**Verdict: CONSISTENT on the load-bearing numbers (115 tests, 18 fixtures). Two MINOR count/wording
discrepancies on the test-MODULE tally that are bookkeeping, not contradictions.**

I counted the spec test layout (merged-spec.md:427-470) directly.

**115 tests — VERIFIED, unanimous:**
- Spec: "**Total: 115 tests.**" (merged-spec.md:360, verified).
- R1 cites 115 (01:90). R4 builds its file→module map around the same suite (04:151-184). No
  disagreement.

**18 fixtures — VERIFIED, unanimous:**
- Spec layout lists exactly **18** JSON fixtures (counted at :451-469: 10 `finding-*`, 4 `review-*`,
  `round-sequence-2`, `round-sequence-residual-x3`, `crash-after-push-before-completed`,
  `behavioral-drift`).
- R1 lists 18 fixtures by name (01:147-153) — **matches exactly**. R6 references the same fixture set
  (06:104-111). No disagreement.

**Test-FILE count — MINOR DISCREPANCY (not a contradiction):**
- **Ground truth (spec:428-449):** 20 `test_*.py` modules + `__init__.py` + `conftest.py` = **22 files
  total**, of which **20 are actual test modules**. The brief's "21 test files" appears to count the 20
  test modules + `conftest.py` (= 21), or to use the spec's own "21" shorthand.
- **R4** says "**The 21 test files → module mapping**" (04:150) and then lists **20 `test_*.py` rows +
  `(+ conftest.py, __init__.py, fixtures/)`** (04:155-177). R4's table body is correct (20 modules); its
  heading "21" matches the brief's framing. **Internally consistent with the spec's shorthand.**
- **R1** says "**22 test modules**" (01:90, :137) and lists 22 names — but R1's list of 22 **includes
  `__init__.py` and `conftest.py`** as two of the "modules" (01:138-139 starts the list with
  "`__init__.py`, `conftest.py` …"). So R1's "22" = 20 test modules + 2 scaffolding files. R1's later
  summary says "24 files: 22 modules + 18 fixtures" / "~42 files" (01:194, :197) using yet another
  rollup.
- **Are R1 and R4 contradicting?** **No.** Both enumerate the **same underlying files**; they differ
  only in whether `__init__.py`/`conftest.py` are counted as "modules." R1 counts them in (→22); R4
  counts only `test_*.py` (→20) and labels the section "21" to match the brief. The **file set is
  identical**; the labels differ. This is a bookkeeping nit, not a factual conflict.

→ **Builder note:** the authoritative counts are **115 tests, 20 `test_*.py` modules (+`__init__.py`
+`conftest.py`), 18 fixtures**. When generating one checklist item per test file, use the spec layout
(spec:428-469) as the source of truth, not either researcher's rollup phrasing.

---

## Additional cross-cut findings (beyond the 6 required)

### A. Pytest markers — R4 vs spec §18.2 (minor over-count, verified)
- **R4** (04:226-236, :292) says the spec adds markers **`loop_guard, autonomy, recovery, p0, loop`
  (5)** and none are registered. I verified `pyproject.toml`: grep for those tokens returns **empty** —
  **R4's "unregistered" claim is CORRECT** (the builder MUST add them or `--strict-markers` fails
  collection, pyproject.toml addopts).
- **Spec §18.2 (verified)** lists only **4** new markers: `loop_guard, autonomy, recovery, p0`. There is
  **no `loop` marker** in the spec's marker table. R4 over-counts by one (`loop`).
- **Impact:** trivial — R4 is the only file enumerating markers (no cross-file contradiction). Builder
  should register the **4 spec markers** (`loop_guard, autonomy, recovery, p0`); the 5th (`loop`) R4
  cited is not in §18.2 and should be dropped unless a test actually uses `@pytest.mark.loop`.

### B. `scripts/` subdir precedent — R1 vs R2 (consistent, mutually reinforcing)
- R1 (01:162-165) and R2 (02:178-225) both confirm `scripts/` under a skill has precedent
  (`sc-bare-review`, `sc-cleanup-audit-protocol`, `sc-crash-recovery`). R2 adds the `$SKILL_DIR/scripts/`
  invocation + `t2_preflight.sh` gold-template detail. No conflict; R2 is the deeper owner.

### C. `name:` frontmatter convention — R1 vs R2 vs R5 (consistent)
- All three recommend directory `sc-submit-pr-protocol/` + command `submit-pr.md` with `## Activation
  > Skill sc:submit-pr-protocol`. R2 (02:73-80) notes the `sc:` vs `sc-` `name:`-field inconsistency
  across the repo but lands on the same recommendation as R5 (05:184-185, :294). Verified against
  Makefile `lint-architecture` Check 6 (Makefile:410-414) — the pairing + Activation requirement is
  real. No conflict.

### D. `evidence-validator` agent reuse — R3 (consistent with spec NFR-6)
- R3 (03:115-119, :226) recommends reusing the existing `evidence-validator` agent for C3a's grounding
  floor rather than authoring a new verifier. This aligns with NFR-6 core-purity (no `gh`/`git` in the
  verify wave) cited by both R1 (01:64) and R5 (05:297). No cross-file conflict.

---

## Structured discrepancy list (for the builder — none are blocking)

| # | Type | Files | Issue | Resolution (verified) |
|---|------|-------|-------|----------------------|
| D1 | **Factual imprecision** (not a contradiction) | R1 vs R5 + Makefile | R1: "hooks NOT mirrored to `.claude/`". | **WRONG.** Makefile:137-142 mirrors `hooks/scripts/*.sh` → `.claude/hooks/` (flattened). R5 is correct. R1's observation was off a stale local `.claude/hooks/`. Builder: hooks ARE synced. |
| D2 | Count/wording nit | R1 vs R4 vs brief | "22 modules" (R1) vs "21 test files" (R4/brief) vs 20 `test_*.py` (spec). | Same file set; differ on counting `__init__`/`conftest`. Authoritative: **20 `test_*.py` + `__init__` + `conftest` + 18 fixtures**. Use spec:428-469. |
| D3 | Over-count nit | R4 vs spec §18.2 | R4 lists 5 new markers incl. `loop`; spec §18.2 lists 4 (`loop_guard, autonomy, recovery, p0`). | Register the **4** spec markers. Drop `loop` unless a test uses it. R4's "unregistered" core claim is verified-correct. |

**No CRITICAL or blocking contradictions found.** D1 is the most important (a false rule the builder
must not encode), but it does not conflict with the unanimous and correct staging rule (`src/`-only,
never `git add .claude/hooks/`), so the net build guidance is safe.

---

## Methodology / evidence trail

Repo facts independently verified (not taken from research prose):
- `Makefile:137-142` — `sync-dev` copies + flattens `hooks/scripts/*.sh` → `.claude/hooks/`.
- `Makefile:255-275` — `verify-sync` enforces hook pairing bidirectionally.
- `Makefile:382-414` — `lint-architecture` Check 6 (skill↔command pairing + Activation).
- `.claude/settings.json:10,21,34` — `offer-pr-review.sh` already registered (PostToolUse/Bash).
- `.claude/hooks/` listing — confirms local sync-staleness (missing `offer-pr-review.sh` etc.) that
  explains R1's mis-observation.
- `merged-spec.md:360` (115 tests), `:428-469` (20 test modules + 18 fixtures), `:190` (severity routes
  + tier names), `:258-300` (FSM separating `S3_DIAGNOSE`/troubleshoot from `S3_FIXING`/edits),
  `:1025` (the broken `--cov` path), `§18.2` (4 markers), `§18.4` (synthetic-then-probe fixtures), `§3`
  step 0 HARD GATE.
- `pyproject.toml` — grep confirms `loop_guard/autonomy/recovery/p0/loop` are unregistered.

No web research performed (none authorized in spawn prompt; none required — all claims are
repo/spec-local).

## Status: COMPLETE — VERDICT: PASS
