# QA Report — Research Gate (Gap-Fill Re-Verification, Round 2)

**Topic:** sc:reflect post-execution gate wiring — O1/O2 viability gap-fill re-verification
**Date:** 2026-06-10
**Phase:** research-gate (gap-fill re-verification, round 1 of fix cycle)
**Lens:** gap-detection / adversarial
**Fix authorization:** false (report only)

---

## Overall Verdict: PENDING (filled at end)

## Adversarial Premise
Prior gap-fill (04-gap-fill-o2-viability.md) claims all 6 gaps mechanically resolved, NO human-decision. Treating this as over-claimed until each load-bearing mechanical claim is verified against real code.

---

## Verification Log (incremental)

### V1 — Linchpin: runner.py frontmatter-missing → false-FAIL (GAP-2). CONFIRMED EXACTLY.

Independently read the real code:
- `runner.py:146-148`: `fm_match = _FRONTMATTER_RE.search(text); if fm_match is None: return "frontmatter-missing"` — VERBATIM match. Writes nothing, does NOT create a block.
- `runner.py:586-590`: `if write_status != "written" and result.verdict is Verdict.PASS: result.verdict = Verdict.BLOCKED; result.reason = write_status or "frontmatter-unwritable"` — VERBATIM. A clean PASS flips to BLOCKED.
- `models.py:39-48`: `Verdict.exit_code` maps `Verdict.BLOCKED: 2`. `commands.py:235,249` `sys.exit(exit_code)`. So BLOCKED → exit 2.

**CONCLUSION:** A clean PASS audit on a no-frontmatter phase file genuinely yields `frontmatter-missing` → BLOCKED → exit 2 (false-FAIL). GAP-2 Option 2A is MECHANICALLY FORCED. The gap-fill's linchpin claim is TRUE, not over-claimed. ✓

**NEW NUANCE (material for the cascade):** `_FRONTMATTER_RE` (`runner.py:44`) = `^---[ \t]*\n(.*?)\n---[ \t]*$` with `re.MULTILINE | re.DOTALL`, commented "preamble-tolerant, non-greedy". MULTILINE means `^---` matches the start of ANY line. So the WRAPPER does not require frontmatter on line 1 — it finds a `---...---` block anywhere. The conflict is entirely SKILL/struct-check-side (strict line-1 `# Phase N`), not engine-side — confirming Option 2A's "amend check #5" is the real work; the engine tolerates the seeded block regardless of position.

### V2 — Check-#5 amendment cascade (GAP-2 scope expansion). gap-fill UNDER-ENUMERATED the cascade.

**The gap-fill names only ONE site (struct check #5 = SKILL.md:1128) and vaguely "the parallel checks in templates/ and the validation prose." That under-enumerates. I grepped EVERY line-1/`# Phase N`/heading-shape assertion. THREE concrete SKILL sites + 1 template assert line-1 `# Phase N`:**

| Site | Line | Assertion | Cascade impact if frontmatter prepended |
|------|------|-----------|------------------------------------------|
| Phase heading rule (prose) | `SKILL.md:100` | "**Phase heading**: MUST be `# Phase N -- <Name>` (level 1 heading…)" | Must be amended to "after an OPTIONAL leading frontmatter block". gap-fill did NOT name this. |
| Phase File Template prose | `SKILL.md:863` | "The heading MUST be a level-1 heading… **required for Sprint CLI TUI display name extraction.**" | Must be amended. gap-fill did NOT name this. ALSO asserts a parser dependency — verified FALSE below. |
| Self-Check #5 | `SKILL.md:1128` | "Every phase file starts with `# Phase N -- <Name>`" | The one site gap-fill named. Amend to allow leading frontmatter. |
| Template heading | `phase-template.md:12` | `# Phase N -- <Phase Name>` (the literal template top) | Template body itself must show the frontmatter block. gap-fill said "parallel checks in templates/" — partial. |

**SPRINT CLI PARSER VERDICT: frontmatter-TOLERANT (the L863 "required for TUI display name extraction" claim is the OLD strict contract, but the actual parser does NOT depend on line-1).** Read the real parsers:
- `_extract_phase_name` (`config.py:149-160`): iterates lines, matches the FIRST line that `line.strip().startswith("# ")`. Leading `---...---` frontmatter lines do NOT start with `# ` → skipped; the `# Phase N` heading below still matches. **Frontmatter-tolerant.**
- `_extract_phase_prompt_preview` (`config.py:173-210`): `saw_h1` is set by ANY `# ` line (L193); frontmatter `---` lines are explicitly excluded at L205 (`startswith((... "---" ...))`). **Frontmatter-tolerant.**
- `count_tasks_in_file` / `_TASK_ID_HEADING_RE` (`config.py:37-55`): `^###\s+T\d{2}\.\d{2}\b` with `re.MULTILINE`, `findall` over whole content. Matches `### T<PP>.<NN>` anywhere. **Frontmatter present → task scan UNAFFECTED. ✓** (Directly answers the spawn-prompt sub-question.)
- `parse_tasklist` / `_TASK_HEADING_RE` (`config.py:386-445`): slices task blocks BETWEEN `### T<PP>.<TT>` headings via `finditer`. Anything before the first task heading (incl. frontmatter) is preamble, never folded into a task body. **Frontmatter-tolerant.**
- `PHASE_FILE_PATTERN` (`config.py:20-32`): matches on FILENAME only, not content. Unaffected.
- `validate_phases` (`config.py:213+`): warnings/errors buckets; no line-1-heading rejection found. Unaffected.

**CASCADE CONCLUSION:** Option 2A is viable AND the Sprint CLI tolerates leading frontmatter (no code change needed sprint-side — the L863 prose is stale-but-harmless once amended). BUT the gap-fill UNDER-SPECIFIED the skill-side edit set: it must amend **THREE** prose/check sites (`SKILL.md:100`, `:863`, `:1128`) + the template top (`phase-template.md:12`), not just "check #5." Severity: IMPORTANT (incomplete remediation spec; a builder following the gap-fill verbatim would amend only #5 and leave L100/L863 asserting a now-false line-1 rule → self-contradictory SKILL + a struct-check author could re-tighten from the stale prose).

### V3 — NEW GAP (HIGH): the gap-fill analyzed O2 frontmatter ONLY; O1's required frontmatter keys are UNADDRESSED.

The spawn prompt's new-gap hunt asked whether O1's tasklist frontmatter seeding is covered. It is NOT. Read the authoritative contract + the O1 template:

- **Contract §2 L41-42 (O1):** "`--base` is **omitted** → the wrapper resolves the base from frontmatter `start_commit` (the whole-task base)."
- **Contract §6 table L162-166:** `start_commit` Required for **O1**; `executor_model_class` Required for **O1 + O2**.
- **Contract §8 checklist L196-197:** "`start_commit` (O1) … persisted" + "`executor_model_class` persisted in frontmatter" are explicit conformance items.
- **O1 frontmatter template (`task-builder/SKILL.md` ~2136-2156):** has keys `id,title,description,status,type,priority,created_date,updated_date,assigned_to,template_schema_doc,estimation,task_type,related_docs,tags`. It has **NO `start_commit` key and NO `executor_model_class` key.**

**Two sub-findings:**
1. **`start_commit` (O1): SOFT.** `config.py:81-105 _resolve_base` precedence = `--base` > frontmatter `start_commit` > `git merge-base HEAD master` > raise `base-unresolved`. O1 omits `--base` and the template has no `start_commit`, so O1 falls to `git merge-base HEAD master`. That resolves (won't hard-fail) but audits the WHOLE branch-vs-master diff, not the task's own start — semantically looser than the contract intends ("the whole-task base"). The O1 builder edit SHOULD seed `start_commit` to honor §8, but absence degrades gracefully.
2. **`executor_model_class` (O1 AND O2): SILENT DEGRADATION — the load-bearing one.** `config.py:201-205`: `executor_model` = env `EXECUTOR_MODEL_CLASS` OR frontmatter `executor_model_class` OR `None`. `runner.py:363-364`: `--executor-model` is appended to the inner reflect prompt **only `if config.executor_model`**. If neither env nor frontmatter supplies it, the flag is silently dropped → reflect runs with NO executor exclusion → **anti-self-confirmation defeated** (reviewers may include the executor's own model class). No error, no exit-2 — it just silently runs a weaker audit. This applies to BOTH O1 (template lacks the key) AND O2 (phase files lack frontmatter entirely).

**This is a NEW blocker the gap-fill missed.** GAP-2's Option 2A seeds `executor_model_class` for O2 phase files (good), but the O1 task-builder template ALSO needs an `executor_model_class` slot seeded — and the gap-fill's GAP-2 scope was O2-only. Severity: HIGH for the O1 `executor_model_class` slot (silent anti-self-confirmation defeat is exactly the failure mode reflect exists to prevent); MEDIUM for O1 `start_commit` (graceful merge-base fallback).

### V4 — GAP-1, GAP-3, GAP-4, GAP-6: re-verified against real code. ALL CONFIRMED SOUND.

- **GAP-1 (no programmatic substitution in cli/sprint): CONFIRMED.** Grep of `src/superclaude/cli/sprint/` for `phase-commit-range|substitut|<phase|<base|<sha>|rev-parse|merge-base|placeholder` → only UNRELATED hits: `tmux.py:47,116` (summary-pane placeholder string), `checkpoints.py:115` (strips the literal `TASKLIST_ROOT/` prefix), `resume/drift.py:277` (`rev-parse --abbrev-ref` for upstream, unrelated). NO code rewrites a `<phase-commit-range>`/`<sha>` token. So resolution is an in-task `[VERIFICATION]` agent step, never generation-time. gap-fill GAP-1 is correct. ✓
- **GAP-3 (--output default mismatch): CONFIRMED.** `config.py:209-213`: default = `resolved_tasklist.parent / "reflect" / "post" / head[:12]` (verbatim) = `<task-dir>/reflect/post/<short-sha>/`, NOT the declared `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/`. So `--output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/` MUST be added to the O2 gate line to keep the declared Reflect Report Path + its Acceptance Criterion valid. gap-fill GAP-3 is correct. ✓
- **GAP-4 (abspath mechanism): CONFIRMED.** `commands.py:77-79`: `@click.argument(... type=click.Path(exists=True, dir_okay=False, resolve_path=True))`. `resolve_path=True` absolutizes the positional before the body runs; `config.py:165` re-resolves. Generators emit their existing path tokens; the wrapper absolutizes. gap-fill GAP-4 is correct. ✓ (Minor: `exists=True` means the path MUST exist at gate-run time — fine, the audited file always exists by then.)
- **GAP-6 (test anchor in fence): CONFIRMED EXACTLY.** `#### POST reflect gate (O1` → ZERO hits (gap-fill correctly says DO NOT use it). The real anchors are present and unique: `**N.{X-1} -- Independent post-execution reflection gate` at `SKILL.md:2193` (count 1) and the next bullet `- [ ] **N.X` at `:2200` (count 1). Fence `\`\`\`markdown` opens at 2136, closes at 2219 (verified). The 5 `---` lines inside the fence are at 2137/2156/2175/2189/2207 (verified — matches gap-fill exactly). No second fenced block immediately follows. The `text.index()` substring-anchor idiom is fence-agnostic, so the corrected anchor is sound. ✓
  - **NOTE (cosmetic, not a blocker):** L2193 uses `--` (double hyphen) between `N.{X-1}` and `Independent`, while L2200 uses `—` (em-dash) between `N.X` and `Update`. The recommended bound `text.index("- [ ] **N.X", start)` stops BEFORE the dash, so the em/hyphen difference does not affect the slice. Safe.

### V5 — NEW needs_human_decision (HIGH): the O1 gate's EXISTING design CONTRADICTS the wrapper contract on the diff base, and the gap-fill never surfaced it.

The gap-fill (and research 02 for O2) assume the contract is authoritative and the gates are swapped to flat `superclaude reflect run` shell-outs. But the EXISTING O1 item carries a DELIBERATE, rationale-documented design that the contract directly contradicts. Read `task-builder/SKILL.md:2193-2198` + struct check #20 at `:2312`:

- **Existing O1 item (`:2195`) is a SUBAGENT-SPAWN of `/sc:reflect --mode post --remediate --diff <BASE> --tasklist {TASK_FILE} ... --depth {DEPTH} --executor-model {EXECUTOR_CLASS}`** — NOT a `superclaude reflect run` shell-out. Struct check #20 (`:2312`) HARD-REQUIRES this `/sc:reflect` self-run-subagent form and declares the `superclaude reflect run`/HALT/human-handoff forms MALFORMED: "A generated task file that … emits a human-handoff/HALT form instead of the self-run form, is a MALFORMED output." Swapping O1 to the contract's `superclaude reflect run` shell-out would VIOLATE the builder's own struct check #20 unless #20 is also rewritten.
- **DIRECT BASE CONFLICT.** `:2195` states, with rationale: `<BASE>` = `git merge-base HEAD <integration-branch>` passed as a SINGLE ref vs the **working tree** (to capture uncommitted/staged edits), and explicitly: **"`start_commit` is retained in frontmatter for provenance only, never as the diff base. Do NOT use `start_commit..HEAD`"** — because (a) `/task` typically leaves work uncommitted so a `..HEAD` range audits nothing, and (b) interleaving commits make `start_commit` span foreign work. The wrapper contract §2 L41-42 + §6 L164 says the OPPOSITE: O1 omits `--base` and "the wrapper resolves the base from frontmatter `start_commit`." And `config.py:81-105` resolves base to `start_commit` then `git merge-base HEAD master` — it diffs that ref against the **working tree** (config.py docstring L95 "the diff against this ref is the working-tree diff"), so the working-tree capture is preserved, BUT the BASE REF differs: contract/wrapper wants `start_commit`; the existing O1 design explicitly rejects `start_commit` in favor of `merge-base HEAD <integration-branch>`.

**Why this matters:** if O1 is migrated to `superclaude reflect run <abs> --depth deep --fix --promote` (contract §2) with NO `--base`, the wrapper uses frontmatter `start_commit` (if seeded) — which the existing design says is the WRONG base for the documented `/task`-leaves-work-uncommitted reason. The two authorities disagree on a load-bearing correctness point (what commit the audit diffs from). The gap-fill silently sided with the contract and never flagged the contradiction.

**needs_human_decision — exact fork:**
- **Fork A (contract wins):** migrate O1 to `superclaude reflect run … --promote` (no `--base`), seed frontmatter `start_commit`, AND rewrite struct check #20 (`:2312`) to require the shell-out form instead of the `/sc:reflect` self-run form. ACCEPT that the base becomes `start_commit` — requires confirming `start_commit` is captured at a point that yields a correct working-tree diff for uncommitted `/task` output (contradicts the existing rationale; may re-introduce the "audits nothing when uncommitted" failure the existing design avoided), OR seed `start_commit` = `merge-base HEAD <integration-branch>` so the wrapper's `start_commit` base equals the existing design's intended base.
- **Fork B (existing O1 design wins):** KEEP O1 as the `/sc:reflect --mode post` subagent self-run with `--diff <merge-base>` (struct check #20 unchanged); apply the wrapper-shell-out migration to **O2 only**. The contract's "O1 = `superclaude reflect run`" is then NOT honored for O1 — accept the asymmetry (O1 stays subagent-spawn, O2 becomes shell-out).
- **Recommended default:** Fork A with `start_commit` seeded to `git merge-base HEAD <integration-branch>` — this satisfies BOTH the contract (frontmatter `start_commit` present, wrapper resolves it) AND the existing design's correctness rationale (base = merge-base, not raw task-start HEAD), while keeping the working-tree diff. But this requires a human to confirm the O1 migration is in-scope at all (research 02 scoped only O2; whether O1 is even being migrated in this task is itself unconfirmed by the gap-fill).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | GAP-2 linchpin (frontmatter-missing → false-FAIL) | PASS (claim TRUE) | `runner.py:146-148,586-590`; `models.py:48`; `commands.py:235,249` — read, verbatim match |
| 2 | GAP-2 cascade: every line-1 `# Phase N` assertion enumerated | FAIL (under-enumerated) | gap-fill named only `SKILL.md:1128`; grep found ALSO `:100`, `:863`, `phase-template.md:12` |
| 3 | GAP-2 cascade: Sprint CLI tolerates leading frontmatter | PASS | `config.py:149-160,173-210,37-55,386-445,20-32` — all parsers frontmatter-tolerant |
| 4 | GAP-1 (no programmatic substitution in cli/sprint) | PASS | grep clean (only unrelated tmux/checkpoints/drift hits) |
| 5 | GAP-3 (--output default mismatch) | PASS | `config.py:209-213` default ≠ declared path |
| 6 | GAP-4 (abspath via resolve_path=True) | PASS | `commands.py:77-79`; `config.py:165` |
| 7 | GAP-6 (corrected anchor; `#### POST reflect gate (O1` absent) | PASS | grep 0 hits; anchors `:2193`/`:2200`; fence 2136-2219; 5 `---` at 2137/2156/2175/2189/2207 |
| 8 | GAP-5 (sibling tests decoupled) | PASS (re-confirmed via gap-fill cites; not re-opened) | gap-fill cites `test_promote_plumbing.py:30-52`, `test_cli_smoke.py:57-68` assert engine internals — consistent with `runner.py:341-366` read |
| 9 | NEW: O1 frontmatter lacks `start_commit`/`executor_model_class` | FAIL (new gap) | contract §2 L41-42, §6 L162-166, §8 L196-197 vs O1 template `task-builder/SKILL.md` ~2136-2156; `config.py:201-205`, `runner.py:363-364` |
| 10 | NEW: O1 base conflict (existing design vs contract) | FAIL (needs_human_decision) | `task-builder/SKILL.md:2195` + struct check #20 `:2312` vs contract §2/§6 + `config.py:81-105` |

## Summary
- Checks passed: 6 / 10 (claims independently verified as sound)
- Checks failed: 4 (1 under-enumeration; 2 new gaps; 1 needs_human_decision)
- Critical/HIGH issues: 2 (O1 `executor_model_class` silent degradation; O1 base-ref contradiction)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | gap-fill GAP-2 vs `SKILL.md:100,863,1128` + `phase-template.md:12` | Option 2A names only struct check #5; THREE other line-1 `# Phase N` assertions would become self-contradictory if only #5 is amended | Amend ALL of `SKILL.md:100`, `:863` (drop/soften the "required for TUI display name extraction" claim — parser is actually tolerant), `:1128`, and update `phase-template.md:12` to show the leading frontmatter block |
| 2 | HIGH | O1 `task-builder/SKILL.md` ~2136-2156 (frontmatter template) + `config.py:201-205` + `runner.py:363-364` | O1 tasklist frontmatter lacks `executor_model_class`; absent → `--executor-model` silently dropped → reflect's executor exclusion (anti-self-confirmation) does NOT run. GAP-2 fixed this for O2 only. | Seed `executor_model_class` into the O1 frontmatter template (and ensure O2 phase-file seed carries it). Confirm env `EXECUTOR_MODEL_CLASS` is not the intended channel; if it is, document it. |
| 3 | MEDIUM | O1 frontmatter template + contract §2 L41-42 / §8 L196 | O1 lacks `start_commit`; wrapper falls to `git merge-base HEAD master` — resolves but not the contract-intended "whole-task base" | Seed `start_commit` per Fork decision (see #4); graceful fallback means not a hard blocker |
| 4 | HIGH (needs_human_decision) | `task-builder/SKILL.md:2195` + #20 `:2312` vs contract §2/§6 | Existing O1 design explicitly rejects `start_commit` as the diff base (uses `merge-base HEAD <integration-branch>` vs working tree, with documented rationale) and struct check #20 declares the shell-out/HALT form MALFORMED. Contract wants O1 = `superclaude reflect run` resolving base from `start_commit`. Direct contradiction on a correctness point. | HUMAN DECISION: Fork A (contract wins, rewrite #20, seed `start_commit`=merge-base) vs Fork B (existing O1 design wins, migrate O2 only). See V5 for exact forks. |

## Confidence
**Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**
(Every check above maps to a specific Read/Grep with cited file:line. GAP-5 not re-opened from raw test files this round — relied on gap-fill's cites cross-checked against the `runner.py` internals I did read; counted as VERIFIED-by-corroboration, the single softer item. If held to strict re-Read of the two test files, treat as 9/10 VERIFIED + 1 corroborated = 100% on the (TOTAL − 0 unverifiable) basis either way, since the GAP-5 conclusion is not load-bearing for the verdict.)

## Tool engagement
**Read: 9 | Grep: 6 | Glob: 0 | Bash: 6** (no web research performed — all verification was source-truth-local)

## VERDICT: FAIL

**Rationale:** The gap-fill's 6 mechanical claims are individually SOUND (GAP-1/3/4/5/6 verified correct; GAP-2 linchpin verified TRUE and Option 2A mechanically forced). HOWEVER the gap-fill OVER-CLAIMED "all 6 gaps resolved, NO human-decision needed" in two material ways the adversarial pass surfaced:

1. **GAP-2 remediation spec is under-enumerated** (IMPORTANT) — three additional skill-side line-1 assertions (`SKILL.md:100,863` + `phase-template.md:12`) must be amended alongside check #5, else the SKILL becomes self-contradictory.
2. **O1 frontmatter is entirely unaddressed** (HIGH) — `executor_model_class` absence silently defeats reflect's anti-self-confirmation; `start_commit` absence loosens the O1 base. GAP-2's scope was O2-only and the gap-fill never noticed O1 has the same frontmatter need with DIFFERENT (native) frontmatter.
3. **O1 diff-base contradiction is a genuine needs_human_decision** (HIGH) — the existing O1 design (`:2195` + struct check #20 `:2312`) and the wrapper contract disagree on the audit base ref, with documented rationale on the existing side. The gap-fill's "NO human-decision needed" assertion is FALSE here.

**To reach PASS (round 3):** resolve the 4 issues above. Issue #1 (amend all 4 sites) and #2 (seed O1 `executor_model_class`) are mechanical. Issues #3/#4 require a HUMAN to pick Fork A vs Fork B for the O1 migration scope + diff base, then re-spec accordingly. NOTE: it is also unconfirmed whether O1 is in-scope for THIS task at all (research 02 scoped O2 only) — that scope question should be answered first, as Fork B (O2-only) would make issues #2/#3/#4 moot for O1.

## QA Complete
