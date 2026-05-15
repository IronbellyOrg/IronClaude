# Refactor Plan — `/sc:task` Deprecation (Phase 6 / T06.03)

**Task:** T06.03 — Refactor plans: `/sc:task` deprecation & references
**Roadmap Item:** R-021
**Tier:** STRICT
**Generated:** 2026-05-15
**Status:** Driving input for Phase 7 execution. Every change row is an eight-column directive that Phase 7 will translate into a concrete file edit / deletion against `[src]` first, with `[.claude]` refreshed by `make sync-dev`.

**Inputs (1:1 referenced):**
- `transfer-manifest.md` (T05.03) — TU-1..TU-8 (what was absorbed into `/task`), ME-1..ME-9, governing R-RULE-06 / R-RULE-10 / R-RULE-11.
- `rejected-features-ledger.md` (T05.03) — terminal REJECT/DEFER ledger; no entry may be re-litigated.
- `merge-roadmap.md` (T06.01) — milestone M4 (`/sc:task` deprecation, post-absorption); CS-M4-A artifact disposition; CS-M4-B reference enumeration.
- `refactor-task-skill.md` (T06.02) — confirms every absorbed pattern lands at `[src] src/superclaude/skills/task/SKILL.md`; deprecation therefore strands no absorbed pattern.

**Companion artifact:** `refactor-references.md` — every reference to `/sc:task`, `sc:task-unified`, `task-unified`, `sc-task-protocol`, `sc-task-unified-protocol` across the repo, with the per-reference treatment row.

**Scope boundary:**
- This file covers the **donor artifact disposition** (per-file soft vs hard deprecation) plus the never-load-bearing MCP-server / persona declarations inside the donor command frontmatter.
- The `/task` skill edits, MDTM frontmatter additions, distribution surface (`superclaude install`, `make sync-dev`), and user-/developer-/reference-guide doc rows are out of scope (T06.02 + T06.04).
- The exhaustive reference enumeration is in the companion `refactor-references.md`.

---

## 0. Side-tagging convention (R-RULE-10) — applied to every operative path

Every donor artifact below carries `[src]` (source of truth — `src/superclaude/...`) or `[.claude]` (dev-copy mirror — `.claude/...`). Phase 7 edits `[src]` first, then `make sync-dev` refreshes `[.claude]`; `make verify-sync` must return 0 before commit. T06.01 confirmed **zero byte-level drift** between paired sides on every path this refactor touches.

| # | Path | Side | Verified (T06.01) | Disposition role |
|---|---|---|---|---|
| 1 | `src/superclaude/commands/task.md` | [src] | md5 `23f50ebc6a89bbc7ef04644af71840f6` | `/sc:task` command, source of truth. Flat layout under `src/superclaude/commands/`. |
| 2 | `.claude/commands/sc/task.md` | [.claude] | md5 `23f50ebc6a89bbc7ef04644af71840f6` | Mirror, layout reshape to `commands/sc/` performed by `make sync-dev`. |
| 3 | `src/superclaude/skills/sc-task-protocol/SKILL.md` | [src] | 14925 B | Donor execution protocol. |
| 4 | `src/superclaude/skills/sc-task-protocol/__init__.py` | [src] | Present | Python package marker for the donor skill directory. |
| 5 | `.claude/skills/sc-task-protocol/SKILL.md` | [.claude] | 14925 B | Mirror of row 3; refreshed by `make sync-dev`. |

---

## 1. Column legend (every row carries all eight columns — T06.03 AC #1)

| Column | Meaning |
|---|---|
| **CR-ID** | Stable change-row identifier (`CR-DEP-NN`). Cross-referenced from `merge-master.md` and Phase 7 commits. |
| **File path (side-tagged)** | `[src]` path (the edit target) and the `[.claude]` mirror that `make sync-dev` refreshes. |
| **Change** | The disposition: `soft-deprecate` (file remains, body replaced with redirect stub + frontmatter cleanup); `hard-deprecate` (file/directory deleted, removed from installer + sync); `remove-field` (frontmatter line removed in place). |
| **Manifest feature(s)** | The TU-N / ME-N / merge-roadmap M-N that justifies the disposition. Confirms the deprecation strands no absorbed capability. |
| **Priority (P0–P3)** | P0 = blocks Phase 7 distribution + doc rows; P1 = direct dependent of P0; P2 = follow-on cleanup. |
| **Effort (XS–XL)** | Edit-size estimate: XS ≤ 5 lines, S ≤ 15, M ≤ 30, L ≤ 60. |
| **Dependencies** | Build-order edges (M1+M2+M3 absorption complete; other CR-DEP-NN rows that must land first). |
| **Acceptance criteria** | Observable post-condition Phase 7 verifies before marking the row done. |
| **Risk assessment** | The INV-NN / ME-NN the disposition could violate if applied wrong, plus the named mitigation. |

---

## 2. Soft- vs Hard-deprecation rubric (decision basis)

The merge-roadmap (M4) and transfer manifest jointly determine, per artifact, whether the artifact is **soft-** or **hard-**deprecated. The rubric is:

- **HARD-deprecate** when (a) every pattern the artifact carried has been absorbed into `[src] src/superclaude/skills/task/SKILL.md` (T06.02 change rows confirm this for `sc-task-protocol/SKILL.md`), AND (b) the artifact is internal — invoked only by another donor artifact, never by user-facing command grammar. Hard deprecation deletes the file and removes it from the installer/sync surfaces (T06.04). The patterns survive at the recipient; the donor body is now redundant ceremony (R-RULE-06 forbids carrying redundant ceremony forward).
- **SOFT-deprecate** when (a) the artifact is part of the user-facing command grammar (`/sc:task` is the typed entry point), AND (b) the artifact may continue to appear in user habits, scripts, and `.dev/releases/backlog/*` prompts long after the deprecation date. The file remains with the same name but the body is replaced by a minimal redirect stub that informs the user to use `/task` and exits. This protects users running `/sc:task` from a "skill not found" failure while the reference treatments in `refactor-references.md` propagate.
- **REMOVE-FIELD** when a never-load-bearing frontmatter declaration (per Phase 2/4 findings — `mcp-servers:` advertisement, `personas:` advertisement) exists on a soft-deprecated file. The advertisement is removed in place during the soft-deprecation rewrite (ME-9 binding).

**No absorbed capability is lost by deprecation.** § 4 enumerates the absorption traceability check.

---

## 3. Change rows — donor artifact disposition (`/sc:task` deprecation)

Five change rows (CR-DEP-01..CR-DEP-05). The order respects M1+M2+M3 → M4 (deprecation may not start before absorption ships) and `[src]` → `[.claude]` (sync follows source-of-truth edits).

### CR-DEP-01 — Soft-deprecate `/sc:task` command file (rewrite body, remove never-load-bearing advertisements)

| Column | Value |
|---|---|
| **CR-ID** | CR-DEP-01 |
| **File path (side-tagged)** | `[src] src/superclaude/commands/task.md` (the `/sc:task` command file, 170 lines). `[.claude] .claude/commands/sc/task.md` is the mirror — refreshed by `make sync-dev` after the `[src]` edit; the `sync-dev` Makefile target reshapes the flat `commands/` → nested `commands/sc/` layout. |
| **Change** | `soft-deprecate` — replace the entire 170-line body with a ~10-line deprecation stub: keep the file at its current path; rewrite the body so invoking `/sc:task` emits one line `/sc:task is deprecated. Use /task. Absorbed by /task skill on 2026-MM-DD (this sprint).` and exits without invoking any skill. Concurrently `remove-field` from frontmatter: drop the `mcp-servers: [sequential, context7, serena, playwright, magic, morphllm]` line (line 7) and the `personas: [architect, analyzer, qa, refactorer, frontend, backend, security, devops, python-expert, quality-engineer]` line (line 8). Retain `name:`, `description:` (rewritten as "Deprecated — see /task"), `category:` (rewrite to `deprecated`), `allowed-tools:` (collapse to none / empty), `version:` (bump). |
| **Manifest feature(s)** | Merge-roadmap M4 / CS-M4-A; ME-9 (D02 / Layer A REJECT — `mcp-servers:` advertisement stays out by R-RULE-06); donor row D10 (command-side dispatch — donor-traceability row inside TU-1; the dispatch pattern was absorbed by Gate 1 at the recipient, the donor command-side surface is now redundant). |
| **Priority** | **P0** — blocks CR-DEP-03 (the donor skill body cannot be removed until the command that invokes it stops invoking it). Also blocks T06.04 distribution rows (installer behavior depends on this file's state). |
| **Effort** | **S** — ~10 lines of stub body + frontmatter cleanup; the 160 lines of removed content are documented in the commit message, not retained. |
| **Dependencies** | M1+M2+M3 absorption complete (transfer-manifest TU-1..TU-8 landed in `[src] src/superclaude/skills/task/SKILL.md` via T06.02 change rows). |
| **Acceptance criteria** | (1) `grep -n "mcp-servers:" src/superclaude/commands/task.md` returns no match (ME-9 satisfied). (2) `grep -n "personas:" src/superclaude/commands/task.md` returns no match. (3) Invoking `/sc:task` in Claude Code emits the single deprecation line and exits without invoking `sc-task-protocol`. (4) `make verify-sync` returns 0 after `make sync-dev` propagates the edit to `[.claude] .claude/commands/sc/task.md`. (5) No `Skill sc:task-protocol` invocation reference remains in the file body. |
| **Risk assessment** | **INV at risk:** none direct (deprecation is a removal-of-capability with redirect, not a behavior change inside `/task`'s loop). **ME at risk: ME-9** if the `mcp-servers:` and `personas:` advertisement lines are left behind during the rewrite — re-affirms the R-RULE-06 prohibition on carrying donor advertisement forward. **Mitigation:** explicit `remove-field` directive on lines 7 and 8 of the frontmatter, validated by the grep checks in acceptance criteria (1) and (2). **Secondary risk:** breaking existing `/sc:task` invocations across user habits and backlog prompts. **Mitigation:** soft (not hard) deprecation — the file remains at its path; the redirect stub is human-readable; reference treatments in companion `refactor-references.md` migrate prompts to `/task`. |

### CR-DEP-02 — Sync soft-deprecated command file to `[.claude]` (mirror refresh)

| Column | Value |
|---|---|
| **CR-ID** | CR-DEP-02 |
| **File path (side-tagged)** | `[.claude] .claude/commands/sc/task.md` (the dev-copy mirror, layout-reshaped from `[src] src/superclaude/commands/task.md` by `make sync-dev`). |
| **Change** | `sync` (no manual edit) — run `make sync-dev` to propagate the CR-DEP-01 stub into the `[.claude]` mirror. The Makefile target rsyncs `src/superclaude/{skills,agents,commands}` → `.claude/`, applying the `commands/` → `commands/sc/` reshape. |
| **Manifest feature(s)** | R-RULE-10 (source of truth lives in `[src]`; `[.claude]` follows). Merge-roadmap §6 zero-drift finding obligates `make verify-sync` to return 0 after the edit. |
| **Priority** | **P0** — must land in the same commit as CR-DEP-01 so `make verify-sync` stays green throughout the sequence. |
| **Effort** | **XS** — single `make sync-dev` invocation; no manual file edit. |
| **Dependencies** | CR-DEP-01 (the `[src]` edit must complete first). |
| **Acceptance criteria** | (1) `md5sum src/superclaude/commands/task.md .claude/commands/sc/task.md` returns identical hashes for the body (modulo layout reshape — confirm with `diff` after stripping the path prefix). (2) `make verify-sync` returns 0. (3) The CR-DEP-01 deprecation stub is the visible content of `.claude/commands/sc/task.md`. |
| **Risk assessment** | **INV at risk:** R-RULE-10 (drift). **Mitigation:** the sync is mechanical — `make sync-dev` is the only authorized propagation path; manual edits to `[.claude]` are forbidden. **Secondary risk:** `make verify-sync` failing post-sync due to the layout reshape (`commands/` vs `commands/sc/`). **Mitigation:** merge-roadmap §6 already verified the reshape is architectural-not-drift and is handled by the Makefile target. |

### CR-DEP-03 — Hard-deprecate `sc-task-protocol` skill body (delete `SKILL.md` from `[src]`)

| Column | Value |
|---|---|
| **CR-ID** | CR-DEP-03 |
| **File path (side-tagged)** | `[src] src/superclaude/skills/sc-task-protocol/SKILL.md` (14925 B donor execution protocol). |
| **Change** | `hard-deprecate` — delete the file. T06.04 follow-on rows stop the installer and `make sync-dev` from carrying the directory; `[.claude]` mirror is removed via the sync rule update in T06.04 (CS-M5-A). |
| **Manifest feature(s)** | Every TU-1..TU-8 (the absorbed control patterns); merge-roadmap M4 / CS-M4-A. § 4 absorption traceability table confirms every pattern from this file landed at `[src] src/superclaude/skills/task/SKILL.md` via a T06.02 change row. R-RULE-06: carrying donor ceremony forward after absorption is forbidden. |
| **Priority** | **P1** — depends on CR-DEP-01 (the command that invokes this skill must stop invoking it first). |
| **Effort** | **XS** — single file delete. |
| **Dependencies** | CR-DEP-01 + CR-DEP-02 (the `/sc:task` command stub no longer invokes `sc:task-protocol`); all T06.02 change rows landed (`/task` skill carries every absorbed pattern). |
| **Acceptance criteria** | (1) `test ! -f src/superclaude/skills/sc-task-protocol/SKILL.md` returns true. (2) No file in the repo invokes `Skill sc:task-protocol` (verified via `grep -rn "sc:task-protocol" src/ .claude/`). (3) Every pattern the file carried is present at `[src] src/superclaude/skills/task/SKILL.md` per the T06.02 acceptance criteria (§ 4 traceability table). (4) T06.04 CS-M5-A installer change ensures fresh `superclaude install` does not create `~/.claude/skills/sc-task-protocol/SKILL.md`. |
| **Risk assessment** | **INV at risk:** INV-01 / INV-03 / INV-04 (loop control / verification floor / resumability) if any pattern is stranded by deletion. **Mitigation:** § 4 below enumerates per-TU absorption traceability; every TU-N landed at a CR-TASK-NN row in T06.02, observable post-conditions verified. **Secondary risk:** orphaned `[.claude] .claude/skills/sc-task-protocol/SKILL.md` mirror after `[src]` deletion. **Mitigation:** ship CR-DEP-04 in the same commit so the mirror is removed atomically; `make verify-sync` is the gate that catches a missed mirror removal. **Tertiary risk:** users running `/sc:task` get a "skill not found" if CR-DEP-01 / CR-DEP-02 didn't actually replace the body. **Mitigation:** CR-DEP-01 / CR-DEP-02 must precede CR-DEP-03 (dependency edge above); Phase 7 verifies the stub is in place before deleting the donor body. |

### CR-DEP-04 — Hard-deprecate `sc-task-protocol` skill directory (delete `__init__.py` + sync to `[.claude]`)

| Column | Value |
|---|---|
| **CR-ID** | CR-DEP-04 |
| **File path (side-tagged)** | `[src] src/superclaude/skills/sc-task-protocol/__init__.py` (Python package marker; removed alongside SKILL.md so the directory becomes a dead path). `[.claude] .claude/skills/sc-task-protocol/SKILL.md` (mirror — removed by sync rule update in T06.04 CS-M5-A; the `[.claude]` side has no `__init__.py`). |
| **Change** | `hard-deprecate` — delete `__init__.py` then `rmdir src/superclaude/skills/sc-task-protocol/`. After T06.04's `make sync-dev` filter rule update, run `make sync-dev` so the `[.claude]` mirror is removed in the same commit. |
| **Manifest feature(s)** | Same as CR-DEP-03 (TU-1..TU-8 absorbed; donor directory now redundant per R-RULE-06). |
| **Priority** | **P1** — ship in the same commit as CR-DEP-03. |
| **Effort** | **XS** — single file delete + directory remove. |
| **Dependencies** | CR-DEP-03 (SKILL.md deleted first); T06.04 CS-M5-A (sync filter rule must update before `make sync-dev` will remove the `[.claude]` mirror cleanly). |
| **Acceptance criteria** | (1) `test ! -d src/superclaude/skills/sc-task-protocol` returns true. (2) `test ! -d .claude/skills/sc-task-protocol` returns true after `make sync-dev`. (3) `make verify-sync` returns 0. (4) `superclaude install` (fresh user-side install) does not create either directory (verified per T06.04 CS-M5-A acceptance). |
| **Risk assessment** | **INV at risk:** R-RULE-10 (drift) if the two sides desynchronize during the staged removal. **Mitigation:** ship CR-DEP-03 + CR-DEP-04 + T06.04 CS-M5-A in a single commit so both sides clear atomically; `make verify-sync` is the gate. **Secondary risk:** leaving `__init__.py` behind without `SKILL.md` creates an inert importable package that asserts the skill exists — a worse state than fully removed. **Mitigation:** the change explicitly deletes `__init__.py` then `rmdir`s the parent directory; the acceptance criterion (1) is the gate. |

### CR-DEP-05 — Re-affirm `mcp-servers:` and `personas:` advertisement removal (R-RULE-11 audit, no re-litigation)

| Column | Value |
|---|---|
| **CR-ID** | CR-DEP-05 |
| **File path (side-tagged)** | Same as CR-DEP-01 (the rewrite already removes both fields). This row is an explicit audit row, not a separate edit. |
| **Change** | `audit` — confirm that the never-load-bearing `mcp-servers:` advertisement (line 7 of `src/superclaude/commands/task.md`) and `personas:` advertisement (line 8) **are not silently orphaned**. The merge-roadmap M4 CS-M4-A obligation: "Never-load-bearing donor declarations [...] M4 removes them explicitly (does not silently orphan them)." This row makes the obligation observable. |
| **Manifest feature(s)** | ME-9 (D02 / Layer A REJECT — R-RULE-06 override); rejected-features-ledger row 21 (D09b classifier) and adjacent — confirms R-RULE-11 audit: no REJECT / DEFER entry is being re-proposed by this deprecation (every entry below is a removal, not a re-introduction). |
| **Priority** | **P2** — audit row, follows CR-DEP-01..04. |
| **Effort** | **XS** — verification only; no separate edit beyond CR-DEP-01. |
| **Dependencies** | CR-DEP-01 (the rewrite that performs the removal). |
| **Acceptance criteria** | (1) `grep -rn "mcp-servers:" src/superclaude/commands/task.md .claude/commands/sc/task.md` returns no matches. (2) `grep -rn "personas:" src/superclaude/commands/task.md .claude/commands/sc/task.md` returns no matches. (3) Commit message for CR-DEP-01 explicitly cites ME-9 and the merge-roadmap M4 CS-M4-A obligation. (4) Phase 7 reviewer checks the rejected-features-ledger and confirms no REJECT/DEFER entry is re-introduced by this deprecation. |
| **Risk assessment** | **INV at risk:** R-RULE-11 (silent re-litigation of a ledger entry). **Mitigation:** the rejected-features-ledger cross-check in § 5 below is explicit; this row is the audit gate. **Secondary risk:** future re-introduction of `mcp-servers:` / `personas:` advertisement on the deprecation stub during a "cleanup" PR. **Mitigation:** the commit message cites ME-9; the deprecation stub body is < 10 lines so the advertisement re-appearing is grep-detectable. |

---

## 4. Absorption traceability — no capability lost by deprecation (T06.03 AC #4)

Per-TU map confirming every absorbed pattern survives in `[src] src/superclaude/skills/task/SKILL.md` (via a T06.02 CR-TASK-NN row) before its donor-side residence in `[src] src/superclaude/skills/sc-task-protocol/SKILL.md` is deleted by CR-DEP-03.

| TU | Pattern (from transfer-manifest) | Donor-side residence (CR-DEP-03 deletes) | Recipient-side residence (T06.02 CR-TASK row) | Absorption verified? |
|---|---|---|---|---|
| TU-1 | `Tier:` field + Gate 1 dispatch (D04 + D09a + D10) | `sc-task-protocol/SKILL.md` §0 NOTE + §3 Execution + classification tables | CR-TASK-02 (Tier validator + Gate 1) + CR-TASK-03 (per-item inline marker read) | **Yes** — T06.02 acceptance #2 (Gate 1 Task Log line) |
| TU-2 | Critical/Trivial Path Override (D17 + D18) | `sc-task-protocol/SKILL.md:121` (critical paths) + `:123` (trivial paths) | CR-TASK-01 (path-override-check at Gate 1) + CR-TASK-04 (path-override-check at Gate 2) — both inline the path-glob sets verbatim | **Yes** — path-glob sets read once and inlined; no runtime dependency on donor file after merge |
| TU-3 | Gate 2 Verification routing widening (D15a / D16) | `sc-task-protocol/SKILL.md` §4 Verification Phase + §4.5 TFEP routing | CR-TASK-04 + CR-TASK-05 (Gate 2 widening; verifier roster supplements `rf-qa` per ME-2) | **Yes** — T06.02 acceptance: `gate-2: profile=… roster=…` Task Log line |
| TU-4 | D15b Layer 2 pre-flight scaffolding | `sc-task-protocol/SKILL.md` §3 STRICT Execution (steps 1–5) | CR-TASK-06 (pre-flight at row 2, First Item Protocol) | **Yes** — T06.02 acceptance: `gate-1.5: pre-flight tier=… ran=[…]` line |
| TU-5 | TFEP Test baseline snapshot (D21) | `sc-task-protocol/SKILL.md:144-153` | CR-TASK-07 (baseline collection, tier-gated STRICT/STANDARD per ME-4) | **Yes** — T06.02 acceptance: `research/test-baseline.yaml` appears for STRICT/STANDARD |
| TU-6 | TFEP Prohibitions + Carve-outs (D19 + D20) | `sc-task-protocol/SKILL.md:127-135` (VIOLATIONS) + `:137-140` (carve-outs) | CR-TASK-08 (prohibition_check + carve_out_check at row 8) — strings inlined verbatim | **Yes** — T06.02 acceptance: `tfep: prohibition-refusal …` / `tfep: carve-out …` Task Log lines; F1 continues per ME-3 |
| TU-7 | TFEP Escalation trigger detection (D22) | `sc-task-protocol/SKILL.md:155-168` | CR-TASK-09 (escalation classification at row 8) — trigger strings inlined verbatim | **Yes** — T06.02 acceptance: `tfep: escalation-trigger fired=… tests=[…] classification=…` line |
| TU-8 | TFEP Incident reporting (D24) | `sc-task-protocol/SKILL.md:222-234` (seven-field schema) | CR-TASK-10 (post-completion incident report) — schema inlined verbatim | **Yes** — T06.02 acceptance: `research/tfep-incident-report.md` exists for STRICT items where TU-7 fired |

**Donor-traceability rows (already absorbed, zero implementation work — confirm no orphans):**

| Donor row | Absorbed-by TU | Donor location (residence) | Recipient location | Status |
|---|---|---|---|---|
| D10 (command-side dispatch) | TU-1 | `sc-task-protocol/SKILL.md` §0 NOTE: "Classification has already been performed by the `/sc:task` command" | Gate 1 at `[src] src/superclaude/skills/task/SKILL.md` Task File Validation section | Absorbed — recipient model has no command-side surface; pattern lives at Gate 1 |
| D15a (verifier routing) | TU-3 | `sc-task-protocol/SKILL.md` §4 Verification Phase | Gate 2 widening at `[src] src/superclaude/skills/task/SKILL.md` Phase-Gate QA Verification | Absorbed — donor-traceability annotation in transfer-manifest § TU-3 |
| D16 (verification timeout table) | TU-3 | `sc-task-protocol/SKILL.md:114-119` | Gate 2 widening (subsumed catalog row 34) | Absorbed |
| D17 + D18 (Critical/Trivial Path Override) | TU-2 | `sc-task-protocol/SKILL.md:121` + `:123` | CR-TASK-01 + CR-TASK-04 | Absorbed |

**Donor ceremony explicitly NOT carried forward (R-RULE-06; transfer-manifest § Donor ceremony dropped):**

| Donor row / pattern | Why dropped | Confirms hard-deprecation is safe |
|---|---|---|
| D09b (donor's runtime classifier with priority cascade + keyword tables) | REJECTed (rejected-features-ledger LR-REJECT-3 / row 21). `Tier:` arrives declaratively from frontmatter; no runtime classifier inside `/task`. | Hard-deprecation of `sc-task-protocol/SKILL.md` removes the classifier with no replacement — by design. |
| D15c (per-tier procedure synthesis) | REJECTed (LR-REJECT-7). ME-5 (NO PER-ITEM EXECUTE SUBSTITUTION) binds CR-TASK-06. | Hard-deprecation removes the donor's per-tier procedure scaffolding — by design. |
| D23 step 5/6 heading-insert + resume-from-inserted | Donor ceremony per transfer-manifest § Donor ceremony dropped. | Hard-deprecation removes; not absorbed. |
| D25 3-strike FULL STOP | Donor ceremony per transfer-manifest. | Hard-deprecation removes; not absorbed. |
| Donor verifier-replacement semantics (rf-qa replaced by quality-engineer) | ME-2 (`rf-qa` SUPPLEMENTED NOT REPLACED) binds CR-TASK-05 to supplement, not replace. | Hard-deprecation removes the donor's replacement framing — by design. |
| Donor F1-halting TFEP | ME-3 (SIDE-CHANNEL ONLY, NO F1 HALT) binds CR-TASK-08..10. | Hard-deprecation removes the F1-halting framing — by design. |
| D02 / Layer A `mcp-servers:` advertisement | REJECTed (LR-REJECT-2 cluster, ME-9). | CR-DEP-01 + CR-DEP-05 remove the advertisement from the soft-deprecated command file; no replacement. |
| `personas:` advertisement on command file | Never load-bearing at runtime (Phase 2/4 finding); R-RULE-06 forbids carrying advertisement forward. | CR-DEP-01 + CR-DEP-05 remove; no replacement. |

**Conclusion (T06.03 AC #4):** every absorbed pattern has a recipient-side residence verified by a T06.02 acceptance criterion. Every donor-only ceremony is explicitly REJECTed by the manifest or the rejected-features-ledger. **No capability is lost by the CR-DEP-03 + CR-DEP-04 hard-deprecation.**

---

## 5. R-RULE-11 audit — no rejected-features-ledger entry re-litigated

Per T06.03 governing R-RULE-11, the deprecation plan may not silently re-propose a REJECT or DEFER entry from the ledger. The audit:

| Ledger entry | Status | Audit verdict |
|---|---|---|
| LR-REJECT-2 (Layer A / `mcp-servers:` advertisement) | REJECTed | CR-DEP-01 + CR-DEP-05 **remove** the advertisement; not re-proposing. **Pass.** |
| LR-REJECT-3 / Row 21 (D09b classifier) | REJECTed | CR-DEP-03 deletes the file that carries the classifier; not re-proposing. **Pass.** |
| LR-REJECT-7 (D15c per-tier procedure synthesis) | REJECTed | CR-DEP-03 deletes the file that carries the synthesis; not re-proposing. **Pass.** |
| LR-DEFER-4 (D01 `allowed-tools:` enforcement) | DEFERRED (ME-8 binding) | CR-DEP-01 collapses `allowed-tools:` on the deprecation stub (no enforcement, since the stub invokes no tools); deferring the enforcement decision until the loader semantics + Rule 6 split land. **Pass.** |
| LR-DEFER-5 (D08 header emission) | DEFERRED (ME-7 binding) | This deprecation does not emit any header; defers the parser-ships decision. **Pass.** |
| All other REJECT/DEFER entries | Various | None touched by this deprecation. **Pass.** |

**Audit verdict:** zero ledger entries re-proposed; R-RULE-11 satisfied.

---

## 6. Disposition summary table

| Donor artifact | Disposition | Justification | CR-DEP row |
|---|---|---|---|
| `[src] src/superclaude/commands/task.md` (the `/sc:task` command) | **SOFT-deprecate** — body replaced with 10-line redirect stub; `mcp-servers:` + `personas:` advertisement fields removed | User-facing command grammar; soft preserves the `/sc:task` invocation surface during migration. ME-9 removes the never-load-bearing advertisement. | CR-DEP-01 |
| `[.claude] .claude/commands/sc/task.md` | **SOFT-deprecate (mirror)** — refreshed by `make sync-dev` from CR-DEP-01 | R-RULE-10 (source of truth lives in `[src]`). | CR-DEP-02 |
| `[src] src/superclaude/skills/sc-task-protocol/SKILL.md` | **HARD-deprecate** — file deleted | Every TU-1..TU-8 pattern absorbed by `[src] src/superclaude/skills/task/SKILL.md` (§ 4 traceability); R-RULE-06 forbids carrying redundant ceremony. Internal skill (invoked only by the soft-deprecated command). | CR-DEP-03 |
| `[src] src/superclaude/skills/sc-task-protocol/__init__.py` | **HARD-deprecate** — file deleted; parent directory removed | Skill body deleted; the package marker becomes a dead file. | CR-DEP-04 |
| `[.claude] .claude/skills/sc-task-protocol/SKILL.md` | **HARD-deprecate (mirror)** — directory removed via T06.04 sync-rule update + `make sync-dev` | R-RULE-10. | CR-DEP-04 (paired with T06.04 CS-M5-A) |
| `mcp-servers:` advertisement (line 7 of `src/superclaude/commands/task.md`) | **REMOVE-FIELD** during CR-DEP-01 rewrite | ME-9 (D02 / Layer A REJECT re-affirmed). | CR-DEP-01 + CR-DEP-05 audit |
| `personas:` advertisement (line 8 of `src/superclaude/commands/task.md`) | **REMOVE-FIELD** during CR-DEP-01 rewrite | Never load-bearing (Phase 2/4 finding); R-RULE-06 forbids carrying advertisement. | CR-DEP-01 + CR-DEP-05 audit |

---

## 7. Phase 7 execution-order constraint (within M4)

CR-DEP-01 → CR-DEP-02 (atomic, same commit, `make verify-sync` gate) → CR-DEP-03 + CR-DEP-04 + T06.04 CS-M5-A (atomic, same commit; sync filter rule and physical deletes coupled) → CR-DEP-05 (audit row, post-hoc verification).

The dependency edge from M1+M2+M3 → CR-DEP-01 (the entire M1+M2+M3 ADOPT/ADAPT absorption must land first) is the absorption-must-precede-deprecation rule from merge-roadmap §4. Phase 7 enforces this via the explicit dependency arrow in `merge-master.md` (T06.05).

---

## 8. Companion artifact handoff

`refactor-references.md` (T06.03's second artifact) consumes the disposition decisions in this file. Every reference to `/sc:task`, `task-unified`, `sc:task-unified`, `sc-task-protocol`, `sc-task-unified-protocol` across the repo carries one of three treatments — **update redirect to `/task`** (matches the soft-deprecation stub message), **remove** (if the reference is obsolete metadata), or **leave-with-deprecation-note** (if the reference is in an archived / frozen artifact). The companion file enumerates every reference and assigns the treatment.
