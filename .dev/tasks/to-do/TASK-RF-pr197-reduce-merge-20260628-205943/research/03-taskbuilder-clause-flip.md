# R3 — task-builder/SKILL.md CLI-mode clause-flip surface

**Researcher:** R3
**Target file:** `src/superclaude/skills/task-builder/SKILL.md` (branch `feat/rf-harness-sync`, 2604 lines)
**Goal of Step 4 (fed by this research):** RETAIN #197 net-new (EV-3/EV-4 + reflect_post_mode/--cli/CLI_MODE), and FLIP the "CLI mode anti-self-confirmation (POST engine binding)" clause polarity from #197's instance-level model to master's **executor-class-EXCLUSION** model (Decision A).
**Method:** read-only Read + Grep against the current branch file. Every quote carries a real line number.
**Status:** In progress

---

## CRITICAL SCOPE FINDING (read FIRST — addresses Task #7)

There are **TWO** distinct families of "instance-level independence / skill no longer class-excludes" text in this file:

- **Family A = CLI POST cluster (FLIPS).** Lines 2170, 2244–2252 (the 7-clause note), 2276, 2389. These describe the `--cli` POST engine binding and the wrapper's `executor_model_class` forwarding. These are the #197 surface Decision A targets. **FLIP these.**
- **Family B = PRE-gate + skill-mode-runner text (DO NOT FLIP in Step 4).** Lines 1668, 1678 (A.10.7 PRE invoke), 2218/2223–2224 (skill-mode dedicated-subagent runner prompt), 2371 (Rule 20 skill-arm + the "skill no longer excludes any model class" disclosure). These also say "the skill no longer excludes any model class / instance-level independence," but they live in the **PRE gate** and the **default skill-mode POST runner**, NOT the CLI POST cluster.

**The boundary is asserted by the file itself.** Clause (7) at line 2251 states: *"A.10.7 is the wording template, not an edit target … A.10.7 itself stays byte-for-byte untouched."* Line 2244 states the note *"REFERENCES, and does NOT edit, the A.10.7 PRE gate's instance-level framing."*

**Consequence / DECISION REQUIRED (flag to Step 4 author):** Under Decision A (master = executor-class EXCLUSION is the canonical model), the 7-clause note's own internal premise — that the CLI POST engine MUST match A.10.7's *instance-level* framing (clauses 6 & 7) — becomes **internally contradictory** if A.10.7 stays instance-level while the CLI cluster flips to exclusion. Two sub-options:

- **A-narrow (RECOMMENDED, matches the user's stated Step-4 goal + clause-7 "byte-for-byte untouched"):** Flip ONLY Family A (CLI POST cluster). Reword clauses 6 & 7 so they NO LONGER claim "uniformity with A.10.7's instance-level framing." Instead, clause 6 asserts executor-class exclusion is the mechanism for the CLI POST path, and clause 7 is either dropped or reworded to stop citing A.10.7 as the wording template. This keeps A.10.7/PRE (Family B) untouched, confining the flip to the CLI POST cluster as the user directed. **Scope creep risk: LOW.**
- **A-wide (NOT what the user asked; flag only):** Also flip Family B (A.10.7 line 1678, skill-mode runner 2223–2224, Rule 20 line 2371). This makes the whole skill uniformly exclusion-based but **violates the user's explicit Step-4 scope** ("flip the CLI POST cluster") and clause-7's "A.10.7 untouched." **Scope creep risk: HIGH. Do NOT do this in Step 4 without an explicit decision.**

**R3 recommendation:** Step 4 = **A-narrow.** Flip Family A only; reword clauses 6 & 7 to drop the "uniform-with-A.10.7-instance-level" claim rather than propagate the flip into A.10.7. R2 (reflect SKILL.md) and R4 (template/tests) own whether the *reflect* skill itself is exclusion or instance-level; if reflect remains instance-level, note the residual tension (see "Residual tension" at end).

---

## TASK 1 — The 7-clause CLI-mode note (verbatim, with line numbers)

Header + all 7 clauses, lines 2244–2251:

- **L2244 (header):** `> **CLI mode anti-self-confirmation (POST engine binding; 7 clauses).** This note governs the `--cli` POST path and lives in the CLI POST cluster; it REFERENCES, and does NOT edit, the A.10.7 PRE gate's instance-level framing.`
- **L2245 (clause 1):** `> (1) **POST engine pinned to OUR skill.** The `superclaude reflect run` wrapper's `claude --print` POST subprocess MUST resolve to OUR `sc-reflect-protocol` SKILL (instance-level independence), NOT IC's class-removing variant. Realized via a skill-trigger prompt (mechanism 1a) or a thin `/sc:reflect` command shim (mechanism 1b); either way the engine that runs is OUR instance-level skill.`
- **L2246 (clause 2):** `> (2) **`executor_model_class` is recorded-provenance + accepted-and-ignored compat, NOT a removal directive.** It is kept in frontmatter as provenance (which class executed); reflect under instance-level independence keeps that class in the reviewer pool.`
- **L2247 (clause 3):** `> (3) **Comment hygiene.** The `executor_model_class` frontmatter comment uses recorded-provenance / compat language only, never a removal-directive wording (it must not claim the named class is dropped from the reviewer panel).`
- **L2248 (clause 4):** `> (4) **`--executor-model` accept-and-ignore.** OUR reflect, handed `--executor-model <class>`, accepts the flag for back-compat and does NOT class-remove, does NOT degrade tier, and does NOT emit an `executor_exclusion_degraded` signal.`
- **L2249 (clause 5):** `> (5) **Contract-field disposition (OD-3 RESOLVED = DROP).** The `--cli` POST contract does NOT emit `executor_class_resolved` / `executor_exclusion_degraded`, not even as sentinels: those are class-removal readouts the anti-self-confirmation change deleted, and the wrapper port does not expect them. The separate `EXECUTOR_MODEL` factory-slot is the path to SET a specific executor, decoupled from any class removal.`
- **L2250 (clause 6):** `> (6) **Uniformity.** The anti-self-confirmation mechanism is IDENTICAL across default `task-builder`, `--cli` PRE, and `--cli` POST: instance-level independence (a fresh subagent or fresh `claude --print` process + no formation context + blind calibration); class diversity is a soft preference, never a removal.`
- **L2251 (clause 7):** `> (7) **A.10.7 is the wording template, not an edit target.** This note echoes A.10.7's instance-level framing as the shared template; A.10.7 itself stays byte-for-byte untouched.`

---

## TASK 2 — Every OTHER instance-level / does-NOT-class-exclude location (verbatim, with line numbers)

### Family A — IN the CLI POST cluster (these FLIP)

- **L2170 (frontmatter `executor_model_class` comment):**
  `executor_model_class: "<executor model-class alias, e.g. sonnet: recorded PROVENANCE of which class executed; passed through to reflect as a compat field. OUR sc-reflect does NOT class-exclude (instance-level independence); this class is NOT removed from the reviewer pool.>"   # CLI MODE ONLY (omitted in default skill mode)`

- **L2276 (Frontmatter Population (CLI Mode) note):**
  `> **Frontmatter population (wrapper gate keys, contract §6, CLI mode only):** … reflect RECORDS/ECHOES the executor class. OUR reflect does NOT class-exclude (instance-level independence: the executor's class stays in the reviewer pool; the forwarded `--executor-model` is accepted-and-ignored per clause (4) of the "CLI mode anti-self-confirmation (POST engine binding; 7 clauses)" note above). …`

- **L2389 (POST-Gate Mode Bifurcation Table row):**
  `| **`executor_model_class` frontmatter** | MUST be present (forwarded to reflect as `--executor-model`, accepted-and-ignored provenance) | MUST be absent | Only the wrapper forwards the compat flag |`

- **L2382–2383 (Bifurcation Table "SHARED" preamble):**
  `… Everything NOT listed here is SHARED (research fan-out, rf-* QA gates, the A.10.7 PRE gate, TCS computation, the instance-level anti-self-confirmation premise).`
  > NOTE: This line names the *premise* generically. Under A-narrow it should change "instance-level" → "executor-class-exclusion" to stay consistent with the flipped CLI cluster (the premise is what the CLI POST now uses). LOW risk, in-cluster (it is the table that documents the CLI bifurcation).

### Family B — OUTSIDE the CLI POST cluster (DO NOT FLIP in Step 4 under A-narrow; flag only)

- **L1668 (A.10.7 PRE, "Invoke reflect directly"):** `… this is NOT because subagent nesting is impossible: a subagent is EXPECTED to be able to invoke the Skill tool and have that skill spawn its own ensemble … reflect spawns its own heterogeneous reviewer ensemble via Task.` (no exclusion claim itself, but A.10.7 body)
- **L1678 (A.10.7 PRE):** `Do **NOT** pass `--executor-model` at PRE: no executor has run in `--mode pre`, so there is no executor class to pass. (The skill no longer excludes any model class in any case; reviewer-panel independence is guaranteed at the instance level, not by passing an executor class.)`
- **L2218 / L2223–2224 (skill-mode dedicated-subagent runner prompt):** the embedded runner prompt at L2223 says *"Do NOT pass `--executor-model` or any executor-exclusion flag: the skill no longer excludes any model class from its reviewer panel. It composes a class-diversity-preferring panel and guarantees independence at the instance level …"*
- **L2371 (Rule 20 skill-arm + disclosure):** *"… MUST NOT pass `--executor-model` or any executor-exclusion flag (the skill no longer excludes any model class; it composes a class-diversity-preferring panel and guarantees independence at the instance level)."*
- **L2310 (Validation checklist skill-arm):** *"… if it passes `--executor-model` or any executor-exclusion flag …"* (MALFORMED predicate for skill mode)

> Family B is governed by what the **reflect skill** actually does (R2's surface). If reflect stays instance-level, Family B is correct as-is and must NOT be flipped. If Decision A also flips reflect to exclusion (R2 to confirm), Family B becomes a SEPARATE, larger edit outside this Step-4 CLI-cluster scope — escalate, do not silently include.

---

## TASK 3 — Proposed exclusion-model rewording (per location), internally consistent under A-narrow

> Goal: the **CLI POST cluster** is internally consistent under executor-class EXCLUSION; A.10.7/PRE (Family B) left untouched.

### Clause 1 (L2245) — PRIMARY FLIP
**To:** `> (1) **POST engine pinned to OUR exclusion-model skill.** The `superclaude reflect run` wrapper's `claude --print` POST subprocess MUST resolve to OUR `sc-reflect-protocol` skill (the canonical executor-class-exclusion model), and MUST NOT resolve to a non-excluding / instance-only variant. Realized via a skill-trigger prompt (mechanism 1a) or a thin `/sc:reflect` command shim (mechanism 1b); either way the engine that runs is OUR executor-class-excluding skill.`

### Clause 2 (L2246) — provenance IS forwarded AND class IS excluded
**To:** `> (2) **`executor_model_class` is recorded-provenance AND a class-exclusion identity, forwarded to `--executor-model`.** It is kept in frontmatter as provenance (which class executed) AND is forwarded to reflect as `--executor-model`; reflect under executor-class exclusion removes that class from the reviewer pool (it is NOT accepted-and-ignored, NOT kept in the pool).`

### Clause 3 (L2247) — comment hygiene inverts to require removal-directive wording
**To:** `> (3) **Comment hygiene.** The `executor_model_class` frontmatter comment uses class-exclusion / forwarded-to-`--executor-model` language (it MUST state the named class is excluded from the reviewer pool), never "accepted-and-ignored" or "kept in pool" compat wording.`

### Clause 4 (L2248) — `--executor-model` DOES class-remove
**To:** `> (4) **`--executor-model` excludes the named class.** OUR reflect, handed `--executor-model <class>`, EXCLUDES that class from the reviewer panel, and if exclusion cannot be honored emits an `executor_exclusion_degraded` signal (loud, not silent). It is NOT accepted-and-ignored.`

### Clause 5 (L2249) — contract fields are EMITTED (invert OD-3 DROP)
**To:** `> (5) **Contract-field disposition (executor-class exclusion = EMIT).** The `--cli` POST contract DOES emit `executor_class_resolved` and `executor_exclusion_degraded`: these are the class-exclusion readouts the wrapper port consumes (which class was excluded; whether exclusion degraded). The `EXECUTOR_MODEL` factory-slot sets a specific executor; the `--executor-model` forward drives the class exclusion.`
> CAVEAT for Step-4 author: clause 5 asserts a CONTRACT shape (`executor_class_resolved` / `executor_exclusion_degraded` emitted vs dropped). This is a **claim about the reflect/wrapper return contract**, which is R2's surface. The wording flip here must MATCH whatever R2 establishes the master/exclusion contract actually emits. If master's contract does NOT emit these fields, soften clause 5 to "the wrapper forwards `--executor-model`; exclusion is honored class-side" rather than asserting specific field names. **Do not invent contract field names not confirmed by R2.**

### Clause 6 (L2250) — Uniformity = exclusion is FORCED, drop the instance-level/A.10.7 claim
**To:** `> (6) **Uniformity.** The anti-self-confirmation mechanism for the `--cli` POST path is executor-class exclusion: the executor's model class is FORCED out of the reviewer pool (class diversity is forced, not a soft preference). This is the CLI POST cluster's mechanism; it does not claim identity with the A.10.7 PRE gate's framing.`
> NOTE: original clause 6 claimed identity across "default task-builder, --cli PRE, --cli POST." Under A-narrow we DROP that cross-context identity claim (because A.10.7/PRE Family B is intentionally left instance-level). If R2 flips reflect globally to exclusion, clause 6 can restore a true uniformity claim — but that is A-wide, out of Step-4 scope.

### Clause 7 (L2251) — A.10.7 no longer the wording template
**To (A-narrow):** `> (7) **CLI POST cluster is self-contained.** This note governs ONLY the `--cli` POST cluster; it does NOT inherit A.10.7's wording and does NOT edit A.10.7, which stays byte-for-byte untouched.`
> RATIONALE: original clause 7 said the note "echoes A.10.7's instance-level framing as the shared template." Once clause 1/6 flip to exclusion, A.10.7 (still instance-level under A-narrow) can no longer be cited as the template without re-introducing the instance-level polarity. So clause 7 must stop citing A.10.7 as the wording source while STILL preserving "A.10.7 untouched."

### Header (L2244) — drop the "references A.10.7's instance-level framing" clause
**To:** `> **CLI mode anti-self-confirmation (POST engine binding; 7 clauses).** This note governs the `--cli` POST path and lives in the CLI POST cluster. It does NOT edit the A.10.7 PRE gate.`

### L2170 (frontmatter comment) — flip to exclusion provenance
**To:** `executor_model_class: "<executor model-class alias, e.g. sonnet: recorded PROVENANCE of which class executed; forwarded to reflect as `--executor-model`. OUR sc-reflect EXCLUDES this class from the reviewer pool (executor-class exclusion); it is NOT kept in the pool.>"   # CLI MODE ONLY (omitted in default skill mode)`

### L2276 (Frontmatter Population note) — flip the inline instance-level sentence + clause ref
**Change the sentence:** `… and reflect RECORDS/ECHOES the executor class. OUR reflect does NOT class-exclude (instance-level independence: the executor's class stays in the reviewer pool; the forwarded `--executor-model` is accepted-and-ignored per clause (4) …)`
**To:** `… and reflect EXCLUDES the executor class from the reviewer pool. OUR reflect class-excludes (executor-class exclusion: the executor's class is removed from the reviewer pool; the forwarded `--executor-model` drives that exclusion per clause (4) of the "CLI mode anti-self-confirmation (POST engine binding; 7 clauses)" note above).`

### L2389 (Bifurcation Table row) — flip the row justification text
**To:** `| **`executor_model_class` frontmatter** | MUST be present (forwarded to reflect as `--executor-model`, drives executor-class exclusion) | MUST be absent | Only the wrapper forwards the exclusion flag |`

### L2382–2383 (Bifurcation Table SHARED preamble) — flip the premise label
**To:** `… Everything NOT listed here is SHARED (research fan-out, rf-* QA gates, the A.10.7 PRE gate, TCS computation, the executor-class-exclusion anti-self-confirmation premise).`
> CAVEAT: this line lumps "the A.10.7 PRE gate" and "the …anti-self-confirmation premise" together as SHARED. If A.10.7/PRE stays instance-level (A-narrow), the premise is NOT actually shared between PRE (instance-level) and POST (exclusion). Step-4 author may instead **remove the premise from the SHARED list** rather than relabel it, to avoid asserting a false shared-ness. Flag for the author; either edit is in-cluster.

---

## TASK 4 — EV-3 / EV-4 hunks PRESENT and to be RETAINED unchanged (verbatim anchors)

Confirmed present on branch. **RETAIN unchanged** — the flip must not touch these.

- **EV-3 (skill-mode arm, L2232 Verification):** `… ORCHESTRATOR-VERIFIES-ON-DISK (EV-3): after the runner returns, the executor MUST independently read `{OUTPUT_DIR}/adversarial/` on disk (Glob or Bash file count, NOT inferring from a returned field) and confirm, for a Tier-2 resolved run, that `{OUTPUT_DIR}/adversarial/merged-verdict.yaml` exists with `merge_method: adversarial` AND `{OUTPUT_DIR}/reviewer-cards/` holds at least the resolved `--reviewers` count of cards …`
- **EV-3 completion gate (L2233):** `… The EV-3 on-disk `{OUTPUT_DIR}/adversarial/` verification (in Verification above) MUST also have passed …`
- **EV-4 (cli-wrapper arm, L2239 Verification):** `… EV-4 (ORCHESTRATOR-VERIFIES-ON-DISK): additionally, the executor MUST independently read the wrapper's on-disk `adversarial/` artifact directory (… `WRAPPER_OUT` = `<task-dir>/reflect/post/<short-sha>/` …) and confirm, for a Tier-2 run, that `WRAPPER_OUT/adversarial/merged-verdict.yaml` exists with `merge_method: adversarial` AND `WRAPPER_OUT/reviewer-cards/` holds at least the resolved `--reviewers` count of cards … `exit == 0` and the wrapper-written `reflect_post` are necessary but NOT sufficient; the on-disk read is authoritative …`
- **EV-4 completion gate (L2240):** `… AND the EV-4 on-disk verification passed (…), NOT `exit == 0` or the wrapper-written `reflect_post` alone). THEN the Update-status-to-Done item proceeds.`
- **`waves_attestation`** present at L2231 (subagent return), L2232 (Verification corroboration), L2233 (completion gate). Necessary-not-sufficient language ("necessary but NOT sufficient") at L2239; "necessary" also at L2240. RETAIN.

> NONE of EV-3/EV-4 reference instance-level vs exclusion — they verify on-disk merge artifacts. **Untouched by the flip.**

---

## TASK 5 — reflect_post_mode / --cli / CLI_MODE machinery PRESENT and RETAINED (verbatim anchors)

Confirmed present; **RETAIN** (this is #197 net-new value the user wants kept).

- **`--cli` flag definition (input #6), L43:** `6. **`--cli` -- programmatic-CLI POST reflect gate** (optional flag, **default OFF**) -- When present, the generated tasklist's POST reflect gate is emitted as a flat `superclaude reflect run` headless-CLI shell-out … Default (flag absent) = skill-only mode, the in-session subagent-runner POST gate. Resolved in priority order: explicit `--cli` on the invocation -> `CLI_MODE: true` in a BUILD_REQUEST file -> OFF. Written to the generated tasklist frontmatter as `reflect_post_mode: cli | skill` (provenance).`
- **CLI_MODE resolution var, L286:** `- **CLI_MODE**: Whether the POST reflect gate is the programmatic-CLI form. Resolved: explicit `--cli` … -> `CLI_MODE: true` field … -> `false` (default). … Recorded in the generated tasklist frontmatter as `reflect_post_mode: cli | skill`. Resolving CLI_MODE NEVER changes PRE-gate behavior (A.10.7), the TCS computation, or the rf-* QA gates.`
- **`reflect_post_mode` frontmatter, default-OFF=skill, L2168:** `reflect_post_mode: <skill|cli>   # ALWAYS emitted (every build): skill by default, cli when CLI_MODE true. …`
- **`start_commit` frontmatter (CLI-only), L2169:** `start_commit: "<git merge-base HEAD <integration-branch>, captured at build time, the wrapper's audit base when --base is omitted>"   # CLI MODE ONLY (omitted in default skill mode)`
- **`executor_model_class` frontmatter (CLI-only), L2170:** present (FLIPPED per Task 3, but the KEY itself is retained).
- **Rule 20 two-arm bifurcation, L2371; POST-Gate Mode Bifurcation Table, L2377–2398; key-presence validation, L2395–2398** — all present, RETAINED (text within them that asserts instance-level in the CLI rows is the Task-3 flip surface; the machinery is retained).

---

## TASK 6 — Step-4 validation (`make verify-sync`) + flip-landed grep

Per the user, Step-4 validation is just `make verify-sync` (after Edit + `make sync-dev`). That confirms `src/` and `.claude/` match but does NOT confirm the flip's semantic content. **R3 recommends ALSO a grep validation** that the polarity actually flipped in the CLI cluster:

**Proposed single-line grep validations (run from worktree root, against `src/`):**

Positive (flip landed — clause 1 now exclusion-model; expect a match):
```
grep -n "canonical executor-class-exclusion model" src/superclaude/skills/task-builder/SKILL.md
```

Negative (old instance-level polarity GONE from the CLI cluster lines 2244–2251; expect ZERO matches):
```
sed -n '2244,2251p' src/superclaude/skills/task-builder/SKILL.md | grep -c "instance-level independence"
```
(expected output: `0`)

Combined one-liner (PASS iff exclusion present in clause 1 AND no instance-level in the note body):
```
grep -q "canonical executor-class-exclusion model" src/superclaude/skills/task-builder/SKILL.md && ! sed -n '2244,2251p' src/superclaude/skills/task-builder/SKILL.md | grep -q "instance-level" && echo FLIP-OK || echo FLIP-FAIL
```

> Line numbers 2244–2251 will SHIFT slightly after the edit (reword length differs). Prefer a content-anchored range or grep on the note header string `"CLI mode anti-self-confirmation (POST engine binding"` to locate the block, rather than hardcoding 2244–2251, when authoring the actual Step-4 validation.

Also recommended — guard against accidental Family-B (A.10.7) edits (scope-creep tripwire); expect the A.10.7 PRE instance-level sentence STILL present (untouched) under A-narrow:
```
grep -c "reviewer-panel independence is guaranteed at the instance level" src/superclaude/skills/task-builder/SKILL.md
```
(expected `1` under A-narrow; `0` would signal A.10.7 was wrongly edited.)

---

## TASK 7 — A.10.7 PRE-gate scope caveat (RESOLVED above; restated)

- **The flip is CONFINED to the CLI POST cluster (Family A): L2170, L2244–2251, L2276, L2382–2383, L2389.**
- **A.10.7 PRE-gate text (Family B) MUST NOT be edited in Step-4** under A-narrow. The file's own clause 7 (L2251) and header (L2244) declare A.10.7 "byte-for-byte untouched." Editing L1678 / the skill-mode runner prompt (L2223–2224) / Rule 20 (L2371) / validation checklist (L2310) would be **scope creep** and would also entangle the *reflect skill's* own exclusion-vs-instance disposition (R2's surface), not just task-builder wording.
- **Internal-consistency consequence (flagged in clauses 6 & 7 rewordings):** because A.10.7/PRE stays instance-level while the CLI POST flips to exclusion, the note can no longer claim "uniformity with / template from A.10.7." The Task-3 rewordings of clauses 6 & 7 (and the header) therefore DROP the A.10.7-template/uniformity claims rather than propagate the flip into A.10.7. This is the correct A-narrow resolution.

---

## Residual tension (escalate to Step-4 author / cross-check R2)

If the **reflect skill itself** (R2's surface) stays instance-level under Decision A, then a CLI POST gate that forwards `--executor-model` to *exclude a class* would be handing an exclusion flag to a skill that "no longer excludes any model class" — a live contradiction between task-builder's flipped CLI cluster and reflect's behavior. **Step 4 must reconcile with R2:**
- If R2 flips reflect to exclusion too → CLI cluster flip is coherent; clauses 4/5 contract-field claims must match reflect's real contract.
- If R2 keeps reflect instance-level → the CLI cluster cannot truthfully say `--executor-model` excludes a class. In that case the flip wording must say "forwarded for exclusion; honored by reflect's exclusion model" ONLY if reflect supports it; otherwise the Decision-A flip is incoherent at the task-builder layer and needs a joint R2+R3 resolution before Step 4 edits land.

**R3 does not own this reconciliation** — flagging it as the single most important cross-researcher dependency for Step 4.

**Status: Complete**
