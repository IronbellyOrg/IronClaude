# QA Report — Task Integrity Check (B2 Self-Containment Lens)

**Topic:** Wire flat `superclaude reflect run` O1/O2 POST gates + skip guard + frontmatter + Layer-A test rewrite (Option A)
**Date:** 2026-06-10
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Overall Verdict: FAIL (advisory — all findings MINOR/IMPORTANT; no CRITICAL)

The task file is unusually strong on B2 self-containment: every item carries Context + Action + Output + Verification + Completion-gate; file paths are absolute or repo-relative-specific; verification criteria are concrete grep/pytest commands; OQ cross-refs and the item DAG are sound. However, the adversarial pass surfaced a set of real self-containment / single-source-of-truth softnesses that a strict B2 gate must FAIL on. None are blocking-CRITICAL; the dominant one (F1) is an anchor-coordination hazard that can silently break the acceptance test.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| B2-1 | Every item has all 5 components | PASS | All items 1.1–6.4 carry Context/Action/Output/Verification/Completion-gate. Spot-verified 2.1, 3.1, 4.1–4.3, 6.3. |
| B2-2 | No item references prior context without restating | PASS-w/exception | Each item restates its surface + anchor. Exception: phase preamble blockquotes (P2/P3/P4) hold shared context ("all edits target X") that individual items rely on — acceptable as a phase-scoped restatement, but see F4. |
| B2-3 | QA-gate items 6.1/6.2 embed lens prompts (not "see above") | PASS | 6.1 embeds Agents A/B/C full lens prompts; 6.2 embeds Agents D/E/F. No "see above". Each names its output file + VERDICT requirement. |
| B2-4 | File paths specific (not "the relevant file") | PASS | Every edit item names `src/superclaude/skills/task-builder/SKILL.md`, `.../sc-tasklist-protocol/SKILL.md`, `.../templates/phase-template.md`, `tests/cli/reflect/test_no_nesting_guard.py` explicitly. Anchors L2193-2200/L2312/L2253/L1722-1724/L1062-1064/L153-155 verified accurate against source. |
| B2-5 | Verification criteria measurable | PASS-w/exception | Almost all are `grep -n`/`grep -c`/`uv run pytest` with a concrete expected result. Exceptions F5/F6 below ("scratch run of the helper", "byte-identical to baseline" without a recorded baseline artifact). |
| B2-6 | No batch items — each edit SITE has its own item | PASS | O1 = 8 items (2.1–2.8, one per surface). O2 = 6 items (3.1–3.6). Test rewrite = 4 items (4.1–4.4). Four `# Phase N` assertions handled in one item (3.5) — see F2. |
| B2-7 | Per-item Context referencing code surface carries file:line OR evidence-absence | PASS-w/exception | Items 2.1–2.8, 3.1–3.6, 4.1–4.4 carry `~L####` anchors or `file:line`. 1.3 carries an `<!-- evidence-absence -->` for the sibling-worktree contract. Exception F3: some anchors say "~L2312" (approximate) which the task itself flags as drift-tolerant. |
| TB-add | No TBD/TODO/FIXME | PASS | grep for `\bTBD\b\|\bTODO\b\|\bFIXME\b` = 0 hits. |
| TB-add | Blocked items reference their OQ by index | PASS | 4.3 → OQ-1 (L225-228); 2.2 → OQ-2 (L110). Both OQs (L343-344) back-reference their items. Bidirectional. |
| TB-add | Item deps form a DAG | PASS | 4.1 depends on 2.1's heading; 6.x depends on P2–P5; 3.2 mirrors 3.1; 5.x after edits. No back-edge (no later item feeds an earlier one). Acyclic. |
| TB-add | Uniform Verify form | PASS | Every item uses a bolded `**Verification**:` field with a concrete command/condition. |

## Verification performed (tool evidence)
- Read task file (346 lines) in full.
- Grep'd `src/superclaude/skills/task-builder/SKILL.md`: confirmed O1 POST item @ L2194, Rule 20 @ L2312, validation line @ L2253, A.11 banner @ L1724, A.9 POST block @ L1073-1076, frontmatter template @ L2137-2156 (confirmed `start_commit`/`executor_model_class`/`reflect_post` ABSENT — claim holds).
- Grep'd `sc-tasklist-protocol/SKILL.md`: O2 spawn directive @ L1062-1064, four `# Phase N` assertions @ L100/L863/L1128 + `phase-template.md:12` all confirmed present and matching the task's claims.
- Read `tests/cli/reflect/test_no_nesting_guard.py:40-95`: confirmed stale markers `auto-resolved-2` / `**Mode \`halt\`` (helper L57-60) exist and anchor nothing in any SKILL; confirmed `@pytest.mark.xfail(strict=False)` decorator + reason; confirmed Layer B + thinness guards present (DO-NOT-MODIFY targets real).
- Grep'd `src/superclaude/cli/reflect/commands.py`: confirmed `--depth`, `--fix/--no-fix`, `--promote/--no-promote`, `--base`, `--output` are real CLI flags (the test/items assert real flags).
- Confirmed contract file + research 01-04 + `qa-research-gap-report-round2.md` all exist on disk.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F1 | IMPORTANT | items 2.1 / 4.1 (anchor coordination) | The acceptance-test anchor is a SINGLE-SOURCE-OF-TRUTH dependency but item 2.1 fixes the heading only as an EXAMPLE: "Keep a greppable item heading, **e.g.** `**N.{X-1} -- Independent post-execution reflection gate (wrapper shell-out)**`". The `e.g.` makes the literal string non-binding at the producing site, while 4.1's `text.index(<exact heading>)` requires a byte-exact match. If the executor picks a different greppable heading at 2.1, 4.1 silently slices the wrong block (or raises ValueError). B2 self-containment requires the anchor literal be MANDATED at exactly one site and quoted verbatim at the consumer. | Change 2.1 from "e.g." to a binding "MUST use the EXACT heading `Independent post-execution reflection gate (wrapper shell-out)` — this literal is the single source of truth for item 4.1's `text.index()` anchor; do not paraphrase." Have 4.1 quote that same literal (it already does, parenthetically) and add an assertion that the helper raised no ValueError. |
| F2 | MINOR | item 3.5 vs B2-6 | Item 3.5 amends FOUR distinct assertion SITES (SKILL.md:100, :863, :1128, phase-template.md:12) in ONE checklist item. Under the lens's "each edit SITE has its own item" rule this is a batch item. It is defensible (identical edit, one rationale, cross-site consistency is the point) and the item's Verification greps all four — but strictly it bundles 4 sites + a stale-rationale note (`:863`) into one item exceeding the atomicity guidance. | Acceptable as-is IF the gate treats "same logical edit across mirror sites" as atomic; otherwise split into 3.5a (three SKILL.md assertions) + 3.5b (phase-template.md:12 + `:863` rationale). Recommend: keep as one item but add an explicit sub-checklist of the four anchors in the Action so none is skipped. |
| F3 | MINOR | items 2.2 / 2.3 / 2.4 / 2.6 / 2.7 / 2.8 (approximate anchors) | Several Context fields cite approximate line anchors (`~L2312`, `~L2253`, `~L1722-1724`, `~L2320`, `~L2356`, `~L2137-2156`). The task pre-emptively flags this ("line numbers may have shifted slightly — the executor re-greps each anchor"), and each item's Action begins with a re-grep, so this is mitigated. But two items (2.2, 2.7) cite a content grep token that must exist for the re-grep to succeed; F7 covers the one risky token. | No fix required for the approximate anchors themselves (re-grep mitigation is sound). Verified L2194/L2312/L2253/L1724/L2137-2156 are in fact accurate. |
| F4 | MINOR | Phase 2/3/4 preamble blockquotes | The phase preambles (`> All edits in this phase target …`) hold context that individual items lean on. Items mostly restate their target paths independently (e.g. 2.2's Verification grep restates the full `src/superclaude/skills/task-builder/SKILL.md` path — good), so self-containment holds, but the preamble is load-bearing for the re-grep-each-anchor discipline. | No fix required — items independently restate their target paths. Noting for completeness; the preamble is a convenience, not a hidden dependency. |
| F5 | MINOR | item 4.1 Verification | "A scratch run of the helper against the edited SKILL.md returns a non-empty block containing `superclaude reflect run`" is a B2-soft verification: "scratch run" is not a copy-pasteable command. A stricter form would be a literal `uv run python -c "..."` one-liner exercising `_extract_wrapper_branch`. | Replace "a scratch run of the helper" with the literal one-liner (or fold into running the actual test at 4.3). Minor because 4.3 + 5.4 run the real test, covering it transitively. |
| F6 | MINOR | items 3.6 / 4.4 Verification ("byte-identical to baseline") | 3.6 asserts the Stage-10.5 PRE block is "byte-identical to baseline" — but no item produces a recorded textual baseline of that region (1.2 baselines only TEST RESULTS, not the PRE-block text). "byte-identical to baseline" is therefore not mechanically checkable as written; the executor falls back to `git diff` judgement. (4.4 already uses `git diff --stat`/`git diff` — good.) | Reword 3.6's verification from "byte-identical to baseline" to the checkable `git diff <Stage-10.5 line range>` shows no change, OR add a 1.x capture of the PRE block via `git show HEAD:<file>`. |
| F7 | MINOR | item 2.2 Verification token | 2.2 greps for the exact string `never as the diff base` to confirm REMOVAL. Confirmed that exact string exists once at L2195 today (grep -c = 1), so the negative-grep-after-edit is valid. No defect — flagging that this is the load-bearing token from F3; it IS present, so the re-grep will find it. | No fix — verified the token exists verbatim. |

## Notes on what did NOT fail (adversarial due-diligence)
- The "O1 8 sites" lens claim is exact: 8 items 2.1–2.8, one per research-01 surface. Verified by item count.
- The stale test markers the rewrite removes (`auto-resolved-2`, `**Mode \`halt\``) genuinely exist in the test and anchor nothing in any SKILL — the rewrite premise is sound (grep -c = 2 in the test, 0 in SKILLs).
- OQ-1/OQ-2 are correctly marked non-blocking with a RECOMMENDED default, and the dependent items (4.3, 2.2) carry the default inline so the item is executable even if the OQ is never separately answered — strong B2.
- Item 6.3 (the task's OWN reflect gate) correctly dogfoods the O1 wrapper shell-out form it wires, with the recursion-breaker skip guard inline and exit-code consumption documented. Its heading coincidentally matches the 2.1 example but is a DIFFERENT artifact (task-file gate vs emitted-template gate) — no conflation defect, but F1's fix should make the distinction explicit so a reader does not assume 6.3 and the emitted-template heading are the same single source.

---

## Confidence Gate
- **Confidence:** "Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%" (every B2/TB-add check carries cited tool evidence)
- **Tool engagement:** "Read: 3 | Grep: ~18 (across 5 Bash batches) | Glob: 0 | Bash: 5"
- No UNCHECKED items. No UNVERIFIABLE items.

## Verdict reasoning
Verdict is **FAIL** because the strict B2 gate treats any self-containment softness (F1's non-binding anchor + F5/F6's non-mechanical verification) as a fail-condition. The dominant defect F1 is IMPORTANT (silent acceptance-test breakage risk); the rest are MINOR. There are NO CRITICAL issues and NO fabricated anchors — all 5 cited SKILL line ranges and the four `# Phase N` assertions are accurate against source. With F1 reworded to a binding single-source-of-truth anchor and F5/F6 reworded to mechanically-checkable commands, this task file would PASS the B2 lens.

## Status: COMPLETE
