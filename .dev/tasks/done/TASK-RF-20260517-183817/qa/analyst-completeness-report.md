# Research Completeness Verification

**Topic:** hook-sync-and-matcher-fix release
**Date:** 2026-05-17
**Files analyzed:** 4 (01-surface-verification.md, 02-makefile-patterns.md, 03-test-harness-patterns.md, 04-template-examples.md)
**Depth tier:** Standard
**Source spec:** /config/workspace/IronClaude/.dev/releases/current/hook-sync-and-matcher-fix/release-spec.md
**Sibling spec:** /config/workspace/IronClaude/.dev/releases/current/hook-sync-and-matcher-fix/hook-sync-coverage-spec.md

---

## Verdict: FAIL — 2 CRITICAL + 1 IMPORTANT + 2 MINOR gaps

R1 (surface-verification.md) contains a **load-bearing misreading** of the spec that, if propagated, would lead the builder to skip Part 2 of the release entirely. R1 declares both `hooks.json:60` and `auggie-flag-clear.sh:22` "ALREADY at target state — no change needed". This is incorrect: the spec's target adds a third prefix (`mcp__auggie-mcp__.*` / `mcp__auggie-mcp__*`) that is NOT present in either file at master HEAD. The current file content R1 captured IS the buggy state. The release REQUIRES patching it.

Additionally, R3 references a test file path (`tests/cli/test_install_hooks.py:438-465`) that I could not independently verify within this session, and R3 makes empirical claims about `uv run` PYTHONPATH behavior that I cannot adjudicate without running uv — but the logical reasoning is sound IFF the claim about `uv run` honoring inherited PYTHONPATH holds.

---

## Independent verification of spec-critical claims

I read the actual files cited in the focus directive. Findings below override any conflicting assertion in the research files.

### Claim A — Is hooks.json:60 currently the BUGGY state (missing `mcp__auggie-mcp__`)?

**YES — BUGGY.** Read of `/config/workspace/IronClaude/src/superclaude/hooks/hooks.json:60`:

```
"matcher": "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*",
```

This is exactly two prefixes: `mcp__auggie__.*` and `mcp__airis-mcp-gateway__auggie_.*`. The middle prefix `mcp__auggie-mcp__.*` is **MISSING**. Spec §4.1 mandates inserting it:

```
+ "matcher": "mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*",
```

R1's section "Summary of [CODE-VERIFIED] Claims" row 1 says "Already at target state" — **THIS IS WRONG**. The current file is the source state (gap), not the target state.

### Claim B — Is auggie-flag-clear.sh:22 currently the BUGGY state?

**YES — BUGGY.** Read of `/config/workspace/IronClaude/src/superclaude/hooks/scripts/auggie-flag-clear.sh:22`:

```
    mcp__auggie__*|mcp__airis-mcp-gateway__auggie_*)
```

Two glob alternatives. Spec §4.2 mandates three:

```
+    mcp__auggie__*|mcp__auggie-mcp__*|mcp__airis-mcp-gateway__auggie_*)
```

R1 row 2 again says "Already at target state" — **WRONG, same defect as Claim A**.

### Claim C — Does R2's POSIX-shell warning about `<(...)` in §4.2 hold up?

**YES — VALID.** I read hook-sync-coverage-spec.md §4.2. The spec snippet at lines 97-98:

```make
missing_from_list=$$(comm -23 <(echo "$$src_hooks") <(echo "$$registered")); \
extra_in_list=$$(comm -13 <(echo "$$src_hooks") <(echo "$$registered")); \
```

`<(...)` is bash-only process substitution. POSIX `/bin/sh` (including `dash`, default `/bin/sh` on Debian/Ubuntu) does NOT support this. If Make invokes the recipe with `/bin/sh` and `/bin/sh` is dash, this syntax fails and `comm` receives empty input, silently passing the section (false-clean). R2 correctly flags this as the highest-priority divergence and proposes two mitigations (declare `SHELL := /bin/bash` in the Makefile, or use temp files). This is a real defect in the spec snippet that the builder must address.

### Claim D — Does R3's PYTHONPATH-resolution logic hold up?

**LOGICALLY SOUND, EMPIRICALLY UNVERIFIED BY ME.** R3 claims that prepending `PYTHONPATH=<tmp_path>/src` makes `uv run python -c "from superclaude.cli.install_hooks ..."` import the mutated module instead of the editable install. R3 reports verifying this empirically by running uv commands. I did not re-run uv. The CPython import semantics are unambiguous (PYTHONPATH entries come before site-packages on `sys.path` unless explicitly mutated), so IF uv preserves the inherited PYTHONPATH (it normally does), the approach works. R3 explicitly acknowledges this caveat in §2 "Unverified / empirical risk". Acceptable.

---

## Checklist Results (9 items)

### 1. Source files identified with paths and exports?

**PASS (partial — see R1 defect)**

Evidence:
- `hooks.json:60` — captured by R1 (correct content, wrong conclusion about whether it needs patching).
- `auggie-flag-clear.sh:22` — captured by R1 (same defect as above).
- `Makefile:154-247` — captured by R1 (correct: 94-line target, banners at L158/190/216, drift footer 242-247) and R2 (extensive pattern catalog).
- `install_hooks.py:43-55` — captured by R1 (correct: list spans L43-L55, iterated at L178).
- All 9 src hook scripts + 11 .claude/hooks scripts inventoried by R1.

**Defect:** R1's "target state" conclusion is inverted for hooks.json:60 and auggie-flag-clear.sh:22 — these are CURRENTLY at the buggy (source) state, NOT the target state. The current content R1 quoted is the diff "-" side, not the diff "+" side. See CRITICAL Finding 1.

### 2. Output paths and formats clear or reasonably inferred?

**PASS**

Modified file paths (Makefile, hooks.json, auggie-flag-clear.sh) documented in R1. New test file path `tests/cli/test_verify_sync_hooks.py` documented in R3 §7 ("tests/cli/test_install_hooks.py (existing) → tests/cli/test_verify_sync_hooks.py (new). Same dir.") and confirmed against spec §9 + §2.1.

### 3. Logical breakdown of phases/steps present?

**PASS**

R4 §6 ("Recommended Phase/Item Structure for THIS Task") maps release-spec §10's 6-phase outline onto a 7-phase task structure (Phase 1 Prep + 6 execution phases + Post-Completion) with item counts per phase (estimated 27-37 items total). The mapping is explicit:

| Spec §10 phase | R4 phase |
|---|---|
| Phase 1 Part 2 patches | Phase 2 |
| Phase 2 Part 1 verify-sync | Phase 3 |
| Phase 3 Part 3 cross-consistency | Phase 4 |
| Phase 4 Tests | Phase 5 + Phase 6 |
| Phase 5 Orphan resolution | Phase 6.5 gate |
| Phase 6 Final QA | Phase 7 |

R4 also catalogs intermediate phase gates (2.5, 3.5, 6.5) for `make sync-dev`/`make verify-sync` smoke checks. Defensible structure.

### 4. Patterns and conventions documented with examples?

**PASS**

R2 provides the most comprehensive pattern catalog of any researcher:
- §2.1-§2.10: 10 enumerated pattern elements with file:line citations (e.g., section-header pattern §2.1 with L158/190/216, drift accumulator §2.2 with L156/164/170/etc., diff invocation variants §2.5 in a table).
- §4: cross-check of spec snippets against existing patterns, with 11 numbered divergences (D1-D11), each with recommendation.
- §5: paste-ready blocks for all three new sections with tab-indent preserved.
- §7: divergence summary table.

R3 provides equivalent depth for test patterns:
- §1a (hook-script harness), §1b (CLI/installer harness), §1c (conftest), §1d (pyproject pytest config).
- §8: paste-ready scaffolding for the new test file.
- §2 trade-off table for the tmp_path mutation gap (4 options evaluated with recommendation).

Both researchers cite file:line evidence throughout.

### 5. MDTM template notes present with rule references?

**PASS**

R4 §1 enumerates rules A-M with verbatim quotes for the critical rules:
- A3 quoted verbatim (lines 91-95 of template).
- A4 quoted verbatim (lines 97-116).
- B2 quoted verbatim (6-element pattern at lines 142-148).
- I15, I16, I17, I18 listed.
- L1-L7 patterns enumerated.
- M1/M2 composite patterns documented.

Rule names are tagged with section letters (A, B, L, M) matching the template's actual structure. Sufficient grounding for the builder.

### 6. Granularity sufficient for per-file/per-component checklist items?

**PASS**

R4 §6.3 explicitly addresses granularity decisions:
- "Each Makefile section = one item."
- "Each shell-script patch = one item. Each JSON patch = one item."
- "New pytest file creation = one big item with V1-V7 enumerated INSIDE the action paragraph."
- "Per-phase smoke tests as their own items."

R2 provides verbatim paste-ready Makefile blocks (§5.1/§5.2/§5.3) so each item can be self-contained per B2. R3 provides paste-ready pytest scaffolding (§8) plus per-scenario mutation snippets (V2-V7). R1 captures exact current content for each surface (so the builder knows what to diff against).

**Caveat:** Builder must apply R1's content but IGNORE R1's "Already at target state" conclusion for Part 2 patches. The diffs ARE required, not no-ops. If the builder uncritically reads R1's summary, they may emit a task file that skips Part 2 entirely.

### 7. Documentation cross-validation tagged correctly?

**PARTIAL FAIL — IMPORTANT**

R1 tags all six spec claims `[CODE-VERIFIED]`. The tags are technically accurate as to "did the file content match what the spec quoted as current state" — yes, the current state matches the spec's "before" side of the diff. **But R1 then misinterprets this as "matches target state" rather than "matches source-of-bug state".** The tags are correct; the prose interpretation is inverted.

R1 row 5 (orphan file existence) and row 6 (install_hooks.py:43, :178) are correctly verified and correctly interpreted.

R2 and R3 are pattern/harness research, not doc-cross-validation, so the tagging convention doesn't apply.

### 8. If new implementation: solution research evaluated approaches?

**PASS**

R3 §2 evaluates four candidate approaches to the `tmp_path` + `_FRESHNESS_SCRIPTS` mutation gap with a comparison table (Option a-d) including Works/Speed/Complexity/Recommendation columns. Recommendation (Option a — PYTHONPATH override) is rationalized empirically.

R2 §4.3 + §5.2 evaluates the POSIX-shell issue with two alternatives (`SHELL := /bin/bash` declaration vs temp-file rewrite) and recommends the former with the latter as fallback. Both alternatives include paste-ready code.

### 9. Unresolved ambiguities documented?

**PASS**

R1 §"Additional findings" enumerates three sibling concerns (Spec claims 1+2 already-satisfied conclusion [which is wrong — see Finding 1], reject-workspace-writes.sh registration question, session-init.sh whitelist requirement). All three are explicit; none are silently dropped.

R3 §2 "Unverified / empirical risk" explicitly captures the uv-version-dependence risk and the `--project` walk-up behavior.

R2 §7 divergence summary is the cleanest unresolved-ambiguity register: 11 numbered divergences each with a recommendation.

R4 §5 "Pitfalls / common deviations (AVOID)" + §6.4 "Specific anti-patterns to AVOID for this task" enumerate known failure modes from prior tasks.

---

## Coverage Audit

| Scope Item (from research-notes EXISTING_FILES) | Covered By | Status |
|---|---|---|
| src/superclaude/hooks/hooks.json | R1 §"Spec Claim 1" | COVERED (content correct; conclusion wrong) |
| src/superclaude/hooks/scripts/auggie-flag-clear.sh | R1 §"Spec Claim 2" & §"Spec Claim 3" | COVERED (content correct; conclusion wrong) |
| Makefile (verify-sync L154-247) | R1 §"Spec Claim 4", R2 entire file | COVERED (deep) |
| src/superclaude/cli/install_hooks.py (L43, L178) | R1 §"Spec Claim 6" | COVERED |
| src/superclaude/hooks/scripts/ (9 files) | R1 §"Spec Claim 5" | COVERED |
| .claude/hooks/ (11 files incl. orphan) | R1 §"Spec Claim 5" | COVERED |
| tests/hooks/test_auggie_first.py | R3 §1a | COVERED |
| tests/cli/test_install_hooks.py | R3 §1b | COVERED |
| tests/conftest.py | R3 §1c | COVERED |
| pyproject.toml pytest config | R3 §1d | COVERED |
| MDTM template 02 PART 1 | R4 §1 | COVERED |
| MDTM template 02 PART 2 | R4 §2 | COVERED |
| Prior task examples (track-2, track-3) | R4 §3, §4 | COVERED |
| tests/cli/test_verify_sync_hooks.py (new) | R3 §7, §8 | COVERED (scaffold) |

No scope items missing.

---

## Evidence Quality

| Research File | Evidenced Claims | Unsupported Claims | Quality Rating |
|---|---|---|---|
| 01-surface-verification.md | ~25 file:line cites | 0 (all claims cite paths) | **STRONG on evidence; FAIL on interpretation** — the summary conclusion for Spec Claims 1 & 2 ("Already at target state") inverts the spec's semantic. Evidence is solid; reasoning over evidence is broken. |
| 02-makefile-patterns.md | ~40 file:line cites; D4 POSIX-shell hazard correctly identified | 0 | STRONG |
| 03-test-harness-patterns.md | ~20 file:line cites including test_install_hooks.py:438-465 (unverified by analyst); paste-ready scaffold; empirical uv test commands provided | Empirical claims about `uv run` PYTHONPATH (R3 §2) were re-run by R3 itself but not by analyst — logically sound, version-dependent | STRONG |
| 04-template-examples.md | ~30 cites; template rule quotes are verbatim; example tasks cited by path | 0 | STRONG |

---

## Documentation Staleness

R1 is the only doc-cross-validation file. Six claims tagged `[CODE-VERIFIED]`. All six file:line citations are accurate against current master HEAD. None are `[CODE-CONTRADICTED]` or `[UNVERIFIED]`. **However, the verification framing is misapplied to Claims 1-3:** R1 verifies that "the current code matches the snippet the spec quoted" — which the spec quoted as the BEFORE state of the diff. R1's prose then concludes the code matches the target, which is the opposite of what the diff shows. This is not a tag-quality failure (the tags are accurate for what they assert); it is a downstream-interpretation failure that the analyst flags as CRITICAL.

---

## Completeness

| Research File | Status | Summary | Gaps Section | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 01-surface-verification.md | Complete | Yes (§"Summary of [CODE-VERIFIED] Claims") | Implicit in "Additional findings" — not labeled as "Gaps and Questions" | Implicit | Adequate (missing labeled Gaps section) |
| 02-makefile-patterns.md | Complete | Yes (§7 divergence summary + §8 final recommendation) | §7 acts as gaps register | Yes (§8) | Complete |
| 03-test-harness-patterns.md | Complete | Yes (§"Summary for the builder") | §2 + §6 + §7 cover gaps | Yes | Complete |
| 04-template-examples.md | Complete | Yes (§"Summary") | §5 pitfalls + §6.4 anti-patterns | Yes (§"Recommendation") | Complete |

R1 lacks an explicitly labeled "Gaps and Questions" section. MINOR.

---

## Contradictions Found

**Contradiction 1 — INTERNAL to R1: between evidence and conclusion**

R1 says (Spec Claim 1, line 31-33):
> "The matcher already uses the `airis-mcp-gateway__auggie_.*` form (regex suffix on `auggie_`), consistent with spec target. **This means the JSON matcher is ALREADY at the target state — no change needed in hooks.json per the spec's claim 1.**"

R1 also says (Spec Claim 2, lines 61-63):
> "**The case-glob pattern is ALREADY at the target state with the `airis-mcp-gateway__auggie_*` alternative present.** Shell case uses globs (not regex) — `auggie_*` is the correct glob form (no `.` prefix). This matches the spec."

But release-spec.md §4.1 clearly shows the target diff:
```
- "matcher": "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*",
+ "matcher": "mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*",
```

R1's quoted current content matches the `-` line (two prefixes). R1's "already at target state" conclusion requires the file to match the `+` line (three prefixes). The two are not the same line. R1 either (a) failed to see the `mcp__auggie-mcp__` insertion in the diff, or (b) confused "gateway suffix present" with "all required prefixes present". This is the single most impactful defect across all four research files.

**Contradiction 2 — between R1 summary and research-notes.md EXISTING_FILES table**

research-notes.md §EXISTING_FILES "Files to MODIFY" row 1:
> "`src/superclaude/hooks/hooks.json` | Line 60 matcher widened (add `\|mcp__auggie-mcp__.*`) | §4.1"

research-notes correctly states the patch is to ADD `mcp__auggie-mcp__.*`. R1's "no change needed" conclusion contradicts research-notes. The orchestrator's scope discovery was correct; R1 misread the spec on its own.

No contradictions between R2/R3/R4 detected.

---

## Compiled Gaps

### CRITICAL Gaps (block synthesis)

#### Finding 1: R1 declares Part 2 patches "no change needed" — INVERTED CONCLUSION

- **Severity:** CRITICAL
- **Source file:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260517-183817/research/01-surface-verification.md (lines 31-33, 61-63, 236-237, 246-250)
- **Why critical:** If the builder consumes R1's summary table at face value, the generated task file will SKIP Part 2 (the matcher-gap fix) entirely — leaving Bug A unfixed. Part 2 IS the user-facing fix; Parts 1 and 3 are the prevention layer. Without Part 2, the release is hollow.
- **Evidence (analyst-verified):**
  - hooks.json:60 currently reads `"mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*"` (2 prefixes).
  - Spec §4.1 target: `"mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*"` (3 prefixes — adds `mcp__auggie-mcp__.*` in the middle).
  - auggie-flag-clear.sh:22 currently reads `mcp__auggie__*|mcp__airis-mcp-gateway__auggie_*)` (2 glob alternatives).
  - Spec §4.2 target: `mcp__auggie__*|mcp__auggie-mcp__*|mcp__airis-mcp-gateway__auggie_*)` (3 alternatives — adds `mcp__auggie-mcp__*` in the middle).
  - Release-spec.md §1.1 ("Bug A — auggie-flag-clear.sh matcher misses mcp__auggie-mcp__*") and §12 ("gap confirmed" twice) further corroborate that the current state IS the buggy state.
- **Recommended remediation:** R1 must be revised (or the builder explicitly instructed to override R1) such that:
  1. Spec Claims 1, 2, 3 are tagged `[CODE-VERIFIED — current state is the SOURCE state of the diff, patches REQUIRED per spec §4.1/§4.2]`.
  2. The summary table row 1 changes from "Already at target state" to "Currently at source/buggy state; spec §4.1 diff required".
  3. The "Additional findings" first bullet ("Spec claims 1 + 2 are ALREADY satisfied at HEAD") must be deleted — it is incorrect.
  4. Also fix auggie-flag-clear.sh:2 header comment which IS the buggy state per R1's verbatim quote vs. spec §4.2's diff (the spec WIDENS the comment to enumerate all 3 prefixes; current comment only names `mcp__auggie__*`).

### IMPORTANT Gaps (affect quality)

#### Finding 2: R1 missing explicit "Gaps and Questions" section

- **Severity:** IMPORTANT (downgraded from Critical because Finding 1's revision will likely re-cast §"Additional findings" as a Gaps section)
- **Source file:** R1 overall structure
- **Why important:** Template 02 + research-notes.md prescribe an explicit Gaps and Questions section. R1's defects might have been self-caught if the file enforced a structured gap-listing discipline.
- **Recommended remediation:** Add an explicit `## Gaps and Questions` section to R1, with at minimum:
  - The 4 items currently in "Additional findings" (after Finding-1 correction).
  - An explicit acknowledgement that Spec Claims 1, 2, 3 require Part 2 patches.

### MINOR Gaps (lower priority but must still be fixed)

#### Finding 3: R3 references `tests/cli/test_install_hooks.py:438-465` — analyst did not independently re-verify

- **Severity:** MINOR
- **Source file:** R3 §1b
- **Why minor:** The line range is for a "real_hooks_json_gates_write_in_pre_tool_use" regression test that R3 cites as a "read live file + assert on shape" template. Even if the line numbers have drifted slightly, the pattern itself (`Path(__file__).resolve().parents[2] / "src" / ...`) is the load-bearing detail and is correctly captured.
- **Recommended remediation:** Builder should verify the line range when reading the file; if drifted, update the citation. Otherwise no blocker.

#### Finding 4: R3 empirical `uv run` PYTHONPATH claim not re-verified by analyst

- **Severity:** MINOR
- **Source file:** R3 §2 + §8 (commands at lines 287-298)
- **Why minor:** R3 explicitly flags this as version-dependent risk in §2 "Unverified / empirical risk". The logic is sound IFF uv preserves inherited PYTHONPATH (it normally does — uv documents not stripping env vars unless `--no-env` is passed). R3 provides the exact re-verification commands.
- **Recommended remediation:** Builder should re-run R3's two verification commands in §"Empirical verification commands" before relying on the PYTHONPATH override pattern. If uv has changed behavior, fall back to R3's Option (d) (grep-based check in Makefile).

---

## Depth Assessment

**Expected depth (Standard tier, 4 researchers):** file-level understanding with key function documentation, pattern extraction sufficient for builder to paste verbatim, paste-ready snippets for each surface change.

**Actual depth achieved:** Deep on R2, R3, R4. Adequate on R1's evidence, broken on R1's interpretation. Overall the Standard tier was MET in evidence collection but FAILED in cross-validation of the Part 2 spec claim.

**Missing depth elements:**
- R1 did not perform the "compare current quoted state against the spec's `+` side of the diff" step. The depth gap is interpretive, not evidentiary.

---

## Recommendations

1. **CRITICAL — Reject R1 in current form.** Spawn a remediation pass that rewrites R1's Spec Claim 1, 2, 3 sections and Summary table to correctly characterize the current state as the SOURCE (buggy) state, not the target state. Without this, the builder will produce a task file missing Part 2 entirely.

2. **CRITICAL — Add a "STOP — VERIFY DIFF DIRECTION" check to the builder's process.** When R1 is consumed, the builder should explicitly cross-reference each `[CODE-VERIFIED]` claim against the spec's `+`/`-` diff markers. If R1 says "current state matches spec snippet" and the spec snippet has a `-` marker, the patch IS required.

3. **IMPORTANT — Builder should adopt R2's `SHELL := /bin/bash` recommendation** (or temp-file rewrite) for the Installer Registration section, NOT the spec's verbatim `<(...)` snippet. Otherwise the verify-sync section will silently false-clean on dash-based systems.

4. **IMPORTANT — Builder should adopt R3's PYTHONPATH override approach** for the V3/V4 test scenarios, NOT a copytree-everything-and-uv-sync approach. R3's analysis is correct (PYTHONPATH wins), and the alternative is 10-30x slower.

5. **MINOR — Builder should re-verify R3's `uv run` PYTHONPATH commands** in §"Empirical verification commands" before relying on the test approach. Add a TODO note in the test file's docstring.

6. **MINOR — Builder should not bundle V1-V7 into a single mega-item.** R4 §6.3 leans this way but R3 §8 provides per-scenario mutation snippets. Recommend one `Write` item that creates the entire file in one shot (V1 inline; V2-V7 spec'd inside the same Write payload), then ONE pytest run item that asserts all 7 pass. This matches R4's "one big item for new test file" guidance while keeping the diff atomic.

7. **Process improvement (for future research spawns):** When the spec contains explicit `diff` blocks with `-`/`+` markers, the surface-verification researcher should be prompted to verify EACH diff direction independently: confirm the `-` content matches current HEAD AND confirm the `+` content is the required change. R1 verified only the first half.

---

## Verdict justification

The release has 4 surface changes (3 modify, 1 create). R1's flaw mis-characterizes 2 of the 3 modifications as "no-op" — that is a 67% defect rate on the most user-visible part of the release (Part 2 = the actual user-facing bug fix). Even though the underlying evidence is correctly captured, the prose conclusion would mislead a downstream agent. This is a FAIL by the analyst's adversarial-quality standard.

R2, R3, R4 individually PASS. The aggregate FAILS because of R1's interpretation defect.

**FAIL — remediation required before task-file generation.** Recommended: revise R1 (focused fix to Spec Claims 1, 2, 3 prose + Summary table + "Additional findings" first bullet), then re-run completeness check.
