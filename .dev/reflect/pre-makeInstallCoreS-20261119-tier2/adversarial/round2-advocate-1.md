# Round 2 — Rebuttal by the Variant 1 advocate (opus-class alias)

## response_to_criticisms

**C-001 (V2: "outcome requirements need not prescribe every expression", 93%).** Plan:26 names every edit target as well as a line number (`_same_content`, the `stale` list, `import filecmp`), and plan:36 states a measurable requirement ("different bytes of the same length"), so F1 and F2 cannot cause a wrong edit; already conceded in round 1 (X-001 to V2, narrowly). But C-001 is wider than F1 and F2: V1 also has F3, F4, F5, the unreadable-file note (old helper at prompt-1-1.md:30-34 differs from `same_content` only by the `clear_cache` call; V2 never makes that comparison) and the `IndexError` extension, which both advocates now accept as a real weakness. V2's "None. No blocking, minor, or wording findings were established" (variant-2-original.md:9) is wrong as written; the V2 advocate concedes this in round 1 ("soften 'no findings'"). V1 stays ahead, with lower confidence because F1 and F2 are a large share of its minor items.

**C-002 (V2: "stronger existing-test and scope analysis", 91%).** V2's three edge cases are correct (copy branch install_core.py:68-79; false-positive case test_how_we_work_install.py:102-115; missing-file helper test), but they confirm risks already handled. C-002 asks which variant found risks the first run missed: V2 found none, V1 found one (the `IndexError`, t2-checks.log:8-10), which the V2 advocate concedes at 96% in X-002. A 91% for V2 on C-002 cannot sit with a 96% concession on X-002, since both concern the same risk list. Part of the sibling-file item (U-001) is conceded: low practical value.

**C-003 (V2: "no required changes; the optional diagnostic note remains valid", 92%).** Both recommendations accept the plan. The V2 advocate calls V1's optional note "valid" and "worthwhile" (round1-advocate-2.md:7,14); a recommendation that includes a valid, cheap follow-up beats one that leaves it out, and V1 marks it optional ("If you want a follow-up", variant-1-original.md:40). Conceded: the orca backlog item in V1's recommendation is too strong and should be optional at most; this lowers confidence on C-003 but does not reverse it.

## updated_assessment
The V2 advocate's round-1 statement is fair on S-001, X-002 and A-003; its scores for C-001, C-002 and C-003 contradict its own concessions. On A-003 the V1 advocate moves from ACCEPT to QUALIFY: the mutation `shipped[0] ^ 1` (test:128) is valid only while PRINCIPLES.md is shipped and non-empty. Both hold today (PRINCIPLES.md:1 is `# Software Engineering Principles`), but nothing in the test guards an empty file, which would raise `IndexError` before the installer is exercised. Credit to V1, which named the condition ("That works because PRINCIPLES.md is not empty", variant-1-original.md:10).

## new_evidence
1. **orca_worktree.py check (requested).** The round-1 claim is correct, with one addition. Line 499 is `shutil.copyfile(src_file, dst_file)` and line 500 is `if not filecmp.cmp(src_file, dst_file, shallow=False)`; `copyfile` writes a new file with a new modification time, so the cache signature of `dst_file` changes and line 500 cannot get a stale hit in practice. Line 480 runs once per file pair in the single loop of `copy_issue_dir` (lines 439-504). Addition: line 1682 (`stale_prompt`, called at line 1722) compares `source/launch-prompt.md` with `wt/.dev/issues/<n>/launch-prompt.md`, possibly the same pair `copy_issue_dir` compares; a wrong cached answer would need that file rewritten at the same size, keeping its old modification time, between two calls in one short-lived process, and no code does that. Result: the flaw exists in form, but no path found where it gives a wrong answer. V1's [INFERRED] tag was right; U-001 is an investigation lead, a backlog issue optional at most.
2. **The plan itself prescribed the assertion that fails unreadably.** Plan:36 says "assert `PRINCIPLES.md` is listed in `message.split("NOT updated")[1]`", so the `IndexError` weakness is a design flaw of the plan's Task 2, inside the reviewed scope; this strengthens X-002 and C-001 for V1.
3. **Against its own side.** The same pattern is the house style: the existing test does `stale_part = message.split("NOT updated")[1]` at test_how_we_work_install.py:113. V1's one-line fix (`assert "NOT updated" in message, message`) is still correct, but a consistent fix would cover lines 113 and 134 together; following an existing pattern lowers the severity. It stays minor and non-blocking.

## per-point positions
| id | superior variant | confidence |
|---|---|---|
| C-001 | V1 (F3-F5, unreadable-file note and `IndexError` extension are correct; V2's "None" is wrong; F1 and F2 weak) | 0.65 |
| C-002 | V1 (found the one real missed risk, t2-checks.log:8-10, prescribed by plan:36; orca item low practical value) | 0.65 |
| C-003 | V1 (same verdict plus a valid optional fix; orca backlog item optional at most) | 0.55 |
| A-003 | Changed: QUALIFY, credit to V1 (valid today; no test guards the non-empty condition) | 0.85 |
| X-002 | V1, unchanged and strengthened | 0.75 |
| U-001 / orca item | Conceded: investigation lead only (lines 480, 500, 1682 checked; no path found that gives a wrong answer) | 0.80 |

(Advocate's closing note: it read every file it cites and ran no commands; pass counts rest on the supplied log; it did not check whether some other caller runs `copy_issue_dir` and `stale_prompt` more than once in one process.)
