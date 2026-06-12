# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** reflect post-gate wiring (sc:reflect --mode post wrapper gate)
**Date:** 2026-06-10
**Phase:** research-gate
**Lens:** GAPS the builder will hit
**Assigned files:** research/01, 02, 03 + ../research-notes.md
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Files read + independently grepped (evidence)
- research-notes.md (97 lines), research/01 (217), research/02 (364), research/03 (385)
- CONTRACT reflect-wrapper-contract.md (200 lines) — read in full
- Independently grepped BOTH SKILL files + phase-template.md for: reflect, --mode post, sc:reflect, superclaude reflect run, start_commit, executor_model_class, reflect_post, POST_REFLECT, --depth, --tier, --no-reflect, --no-promote, --base, SUPERCLAUDE_REFLECT_WRAPPER
- Read reflect CLI commands.py (output default, writeback, exit codes)
- Grepped tests/ for second consumers of the POST shape

## Verification of research line-anchor accuracy
All research-cited line anchors VERIFIED accurate against current src:
- task-builder: L207(PRE overview), L1073-1076(A.9 POST block), L1666(PRE note), L1724(banner POST), L2193-2198(O1 item, inside ```markdown fence L2136-2219), L2253(validation checklist), L2312(Rule 20), L2318/2320/2356(Reflect Depth/O4), L41/L282(spec doc/glossary) — ALL MATCH.
- sc-tasklist: L1036-1083(O2 block), L1041/L1063/L1067/L1074(directive/steps/AC), L1129(Self-Check#6), L1169-1171(checks #18-20), L1128(check#5), L1448-1465(PRE Stage 10.5), L1478 — ALL MATCH.
- phase-template: L127-174 mirror — MATCHES. Line counts: sc-tasklist 1617, phase-template 174, test 134 (research said 135 — off-by-one, immaterial; all in-scope markers L49/56/63/75 confirmed present).

## Verdict summary
The research is HIGH QUALITY and captured ~95% of the edit surface with accurate verbatim blocks and line anchors. However, gap-detection found **6 genuine gaps** the builder WILL hit, **2 of them CRITICAL** (O2 correctness questions the research left explicitly open). Per research-gate rules, ANY gap regardless of severity = FAIL. **VERDICT: FAIL** — gaps must be closed before synthesis/build.

---

## GAPS FOUND (severity-rated)

### GAP-1 [CRITICAL] — O2 `<phase-N-start-sha>` is UNKNOWABLE at generation time; resolution mechanism left OPEN
**Lens item 4.** Contract §2/§6 require O2 to emit `--base <PHASE_N_START_SHA>` (the SHA at which phase N's execution BEGINS). But `sc:tasklist` runs entirely BEFORE any phase executes — at generation time NO phase has started, so there is no phase-start SHA to capture or hardcode. Research 02 Surface 6 acknowledges "today's placeholder is `<phase-commit-range>` resolved by the Sprint executor at run time" and lists two options (prepend frontmatter vs `--base` on the gate line) but does **NOT resolve how a single start SHA is produced at execution time**: placeholder token the Sprint executor substitutes? a frontmatter field the wrapper resolves? Neither is specified. The contract's precedence note (`--base` > frontmatter `start_commit` > `git merge-base HEAD master`) hints the generator could emit a `<PHASE_N_START_SHA>` PLACEHOLDER and rely on Sprint-executor substitution — but that substitution path does not exist today (today's range token is executor-resolved via `--diff`, a different mechanism being removed). **This is a correctness blocker: O2 cannot be implemented as specified until the start-SHA resolution path is pinned.**
**Evidence:** sc-tasklist L67-74 (TASKLIST_ROOT resolution — generation-time, pre-execution), L1067 (Step 1 "git RANGE … at execution time"), research/02 Surface 6 (lines 256-273, "decide between … vs another mechanism"); contract §6 lines 162-173.
**Required fix:** Research must specify the EXACT O2 start-SHA mechanism. Recommended: emit a literal placeholder token (e.g. `<phase-N-start-sha>`) on the gate line that the Sprint executor resolves to `git rev-parse HEAD` at the moment phase-N execution begins, AND document where that substitution is wired (Sprint CLI executor, not the generator). If no such substitution hook exists, surface as an Open Question for the user / a prerequisite task.

### GAP-2 [CRITICAL] — O2 wrapper writes `reflect_post:` back to PHASE-FILE frontmatter, but phase files HAVE NO frontmatter (collides with structural check #5); `executor_model_class` persistence unresolved
**Lens item 2.** The reflect CLI (`commands.py` L53, L165) writes a `reflect_post:` block **back into the audited file's frontmatter**. For O2 the audited file is the PHASE file. Research 02 Surface 6 establishes phase files have NO YAML frontmatter and structural check #5 (L1128) mandates every phase file STARTS with `# Phase N -- <Name>`. The PRE gate sidesteps this by writing `reflect_pre:` to the INDEX file's "Pre-Reflect Sign-off" column (sc-tasklist L1463) — but the wrapper O2 cannot redirect; it writes to the file it audits. So BOTH (a) the contract-required `executor_model_class` persistence AND (b) the wrapper's `reflect_post:` writeback need a frontmatter slot on phase files that does not exist and whose creation collides with check #5. Research 02 FLAGS the check-#5 collision for the WRITE side but leaves resolution as an unresolved either/or, and NEVER connects it to the wrapper's `reflect_post:` writeback (it only knew "leave room", not "the writeback target is the frontmatter-less phase file").
**Evidence:** commands.py L53 ("writes a `reflect_post:` block back into"), L165; sc-tasklist L1128 (check #5), L1463 (PRE writes to index not phase frontmatter); research/02 Surface 6 (lines 258-273); contract §6 row 3 + note (lines 166, 174).
**Required fix:** Resolve the EXACT insertion mechanism. Either (a) amend check #5 to permit a leading YAML frontmatter block before `# Phase N` (and update the Sprint CLI TUI display-name extraction at L863 if it reads line 1), persisting `executor_model_class` + leaving room for `reflect_post:`; OR (b) confirm the wrapper can write `reflect_post:` to a non-frontmatter location for phase files and source `executor_model_class` another way. Decision must be made before build — it gates O2 viability.

### GAP-3 [IMPORTANT] — Flat O2/O1 lines DROP `--output`; the Reflect Report Path declaration + report-existence Acceptance Criterion become stale/unverifiable
**Lens item 1 (validation-checklist / Output-Structure coverage).** Today's O2 directive passes `--output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/` (L1063). The contract's flat O2 line `superclaude reflect run <abs> --depth deep --fix --no-promote --base <sha>` has **no `--output`**. Per `commands.py` L110 the default is `<task-dir>/reflect/post/<sha>/` — NOT `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/`, and the report file is not named `REPORT.md`. Research 02 marked L87, L121-123 (`reflect-post/` dir + Target Directory Layout) and L1060 (Reflect Report Path) and L1072 (AC "File …/REPORT.md exists") all as KEEP, but did NOT recognize that dropping `--output` orphans the producer of those paths. The `**Reflect Report Path:**` field (L1060), the directory-layout `reflect-post/` node (L123), and the report-existence Acceptance Criterion (L1072) all reference a path the wrapper will no longer write.
**Evidence:** contract §2 (O2 line, no --output); commands.py L108-110 (default `<task-dir>/reflect/post/<sha>/`); sc-tasklist L87, L121-123, L1060, L1072; research/02 Surface 1 (only addressed `--remediate`→`--fix` on the AC, not the path's producer) and Surface 7 (L87/L121-123 marked KEEP).
**Required fix:** Research must decide either (a) keep an explicit `--output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/` on the O2 line (deviates from the bare contract line but preserves the declared path + AC) — flag this as a contract-permitted addition; OR (b) drop the Reflect Report Path field + report-existence AC + `reflect-post/` layout node and rewrite the AC to consume the EXIT CODE only. Same question applies to O1 (Surface 1) if it declares any report path.

### GAP-4 [IMPORTANT] — Absolute-path emission mechanism for `<ABS_TASKLIST_PATH>` / `<ABS_PHASE_FILE_PATH>` not specified
**Lens item 4.** Contract O1/O2 require ABSOLUTE paths. `sc:tasklist` resolves `TASKLIST_ROOT` as a RELATIVE path (`.dev/releases/current/...`, L67-74) and phase files are referenced relatively (`TASKLIST_ROOT/phase-N-tasklist.md`). Research 01 Surface 1 says "`<ABS_TASKLIST>` = `{TASK_FILE}` resolved to absolute" and research 02 says "ABS_PHASE_FILE" but NEITHER specifies the resolution mechanism (e.g. `$(cd "$(dirname …)" && pwd)`, `realpath`, or `git rev-parse --show-toplevel`-anchored). For O1 (task-builder) `{TASK_FILE}` may already be absolute via `${TASK_DIR}`; for O2 the relative `TASKLIST_ROOT` definitely needs a documented absolutization step at emission or execution time. research-notes GAP #4 asked this and it remains unanswered.
**Evidence:** sc-tasklist L67-87 (relative TASKLIST_ROOT); research-notes GAP #4 (line 77); research/01 L36, research/02 Surface 6 — no abs-path mechanism given.
**Required fix:** Specify the absolutization mechanism for each gate (and whether it happens at generation time — generator writes the resolved abs path — or at execution time via a shell expansion the executor runs).

### GAP-5 [MINOR] — Second-consumer tests of `/sc:reflect --mode post` not enumerated/cleared by research 03
**Lens item 5.** `tests/cli/reflect/test_promote_plumbing.py:51` and `tests/cli/reflect/test_cli_smoke.py:66` both assert `"/sc:reflect --mode post" in result.output`. Research 03 analyzed ONLY `test_no_nesting_guard.py` + sibling-worktree copies and did not enumerate these. **Independent analysis (this QA): these are SAFE** — they assert the reflect CLI WRAPPER's own internal `claude --print` prompt (the wrapper internally spawns reflect via `/sc:reflect --mode post`), which is wrapper-engine behavior INDEPENDENT of the generator SKILL emission being rewritten. They will NOT break. But research should pre-clear them so the builder (running full `tests/cli/reflect/`) does not mistakenly "fix" a passing test.
**Evidence:** test_promote_plumbing.py L38-52, test_cli_smoke.py L60-68 (both assert wrapper output, not SKILL text); research/03 §2 + §5 (scope limited to test_no_nesting_guard.py).
**Required fix:** Add a one-line note to research 03: "test_promote_plumbing.py:51 and test_cli_smoke.py:66 assert the wrapper's internal `--mode post` prompt (CLI-side), unaffected by the SKILL rewrite — DO NOT MODIFY."

### GAP-6 [MINOR] — O1 test-anchor robustness: `#### POST reflect gate (O1` heading lives INSIDE the ```markdown fence (L2136-2219) containing multiple `---` rules; helper slice bound not reconciled
**Lens item 6 (integration risk).** Research 03's proposed `_extract_wrapper_branch` slices from `#### POST reflect gate (O1` to "the next `####` or `---`". But research 01 places the O1 item INSIDE the fenced ```markdown example block (L2136-2219), which contains `---` rules at L2189 and L2207 (and frontmatter `---` at L2137). A naive "next `---`" slice could mis-bound or capture too little. Research 01 (where the heading goes) and research 03 (how the helper slices) were never reconciled for the in-fence multi-`---` reality. NOT a structural-check break (task-builder has no #18-style heading check for the O1 item — confirmed: the O1 item is example text inside a fence, asserted only by validation-checklist L2253 prose + Rule 20, neither of which pins a `####` heading shape), so the rewrite is low-risk to task-builder's own checks. The risk is purely the test helper's slice precision.
**Evidence:** task-builder fence L2136(```markdown)…L2219(```), `---` at L2189/L2207, frontmatter `---` L2137; research/03 §3b (slice to next `####`/`---`); research/01 Surface 1 (heading inside template block).
**Required fix:** Research 03 + 01 coordinate the EXACT anchor: either (a) the helper slices to the next `#### ` ONLY (not `---`), since the O1 block is delimited by sub-headings; or (b) use the fenced-bash sentinel (Option ii) scanning the first ```bash block containing `superclaude reflect run`. Pin one and confirm it survives the surrounding `---` rules.

---

## NON-GAPS (verified clear — adversarial checks that PASSED)
- **Lens item 3 (sync-dev/verify-sync/ruff-format/full reflect-test-suite in scope):** PRESENT. research-notes TEMPLATE_NOTES (line 92) lists `make sync-dev`, `make verify-sync`, `uv run ruff format --check src/ tests/` (per memory `reference_make_lint_vs_ci_ruff_format`), full `uv run pytest tests/cli/reflect/`. SUGGESTED_PHASES P5 covers sync-dev + verification. NOT a gap.
- **Lens item 6 (sc-tasklist checks #18-20 / Self-Check #6):** research 02 Surface 4 correctly identified that keeping the `-- Post-Execution Reflection` heading PREFIX (dropping only `: sc:reflect --mode post`) means check #18 needs no edit; #19/#20/Self-Check#6 carry no invocation token. VERIFIED accurate against L1129, L1169-1171. NOT a gap (research handled it).
- **PRE gate fencing:** All PRE occurrences (L207, L1448-1465, L1666, L1724 PRE line, reflect_pre frontmatter) correctly scoped INTACT. Independently confirmed no PRE surface is mistakenly marked for change.
- **`--no-reflect` toggle:** Correctly identified as the gate on/off toggle (not the abandoned `--reflect` dial); KEEP. Verified L9 argument-hint + all handling sites.
- **Sibling worktree copies:** research 03 §5 correctly fences `reflectWrapper` (byte-identical) + `wrapper-onto-master` (stale) as DO-NOT-TOUCH. Aligns with memory `feedback_worktree_discipline`.

---

## Items Reviewed
| # | Check (lens) | Result | Evidence |
|---|------|--------|----------|
| 1 | Coverage gaps — POST occurrences missed (banner/checklist/Crit-Rules/layout/dirs) | FAIL | GAP-3 (`--output` drop orphans L87/L123/L1060/L1072); all other POST occurrences captured |
| 2 | Frontmatter executor_model_class insertion mechanism resolved | FAIL | GAP-2 (check#5 collision + reflect_post writeback to frontmatter-less phase file — unresolved) |
| 3 | sync-dev/verify-sync/ruff-format/test-suite in scope | PASS | research-notes L92 TEMPLATE_NOTES + P5 |
| 4 | ABS path emission + `<phase-N-start-sha>` execution-time resolution | FAIL | GAP-1 (CRITICAL: start-SHA unknowable at gen-time, mechanism open) + GAP-4 (abs-path mechanism unspecified) |
| 5 | Second consumer break (other tests / roadmap gates) | FAIL(minor) | GAP-5 (2 wrapper-output tests not cleared; independently verified safe) |
| 6 | heading/spawn rewrite breaks checks #18-20 / Self-Check #6 + test anchor | PASS / FAIL | checks #18-20 handled (PASS); GAP-6 test-anchor-in-fence not reconciled (MINOR) |

## Summary
- Lens checks passed: 1.5 / 6 (item 3 PASS; item 6 split)
- Lens checks with gaps: 4.5 / 6
- Gaps found: 6 (CRITICAL: 2, IMPORTANT: 2, MINOR: 2)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Confidence
**Verified:** 6/6 lens items checked with tool evidence | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 6 | Grep: 9 | Glob: 0 | Bash: 9 (all targeted at specific lens items: token sweeps, line-anchor verification, fence detection, CLI output default, second-consumer tests)
- No web research performed (all claims local/source-truth).
- Tool calls (24 Read+Grep+Bash) >> 6 lens items — engagement floor satisfied.

## Recommendations
1. Close GAP-1 and GAP-2 (CRITICAL) BEFORE synthesis — they are O2 correctness/viability blockers, not cosmetic.
2. Close GAP-3 and GAP-4 (IMPORTANT) — both are "the builder will write a stale/broken instruction" risks.
3. Fold GAP-5 and GAP-6 (MINOR) into research 03 as clearing notes / anchor decisions.
4. Per research-gate rules: ALL gaps regardless of severity must be resolved. Re-run this gap lens after gap-fill.

## QA Complete

## Status: COMPLETE
