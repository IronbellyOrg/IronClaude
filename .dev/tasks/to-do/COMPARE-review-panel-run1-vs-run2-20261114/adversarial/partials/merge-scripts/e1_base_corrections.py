"""E1 base corrections: M-01 (V2:5), M-12, M-13, M-24 items 1-14 of refactor-plan.md.

Starts from the byte-exact base (variant-2-original.md), applies exact-text replacements
addressed by ORIGINAL line number (each old text must occur exactly once in that line),
appends one provenance comment at the end of every modified line, and writes
partials/merge-stage/base-corrected.md. Line count is unchanged.
Run: uv run --no-project python e1_base_corrections.py
"""
import json
import pathlib
import sys

ADV = pathlib.Path(__file__).resolve().parents[2]
BASE = ADV / "variant-2-original.md"
OUT = ADV / "partials" / "merge-stage" / "base-corrected.md"
REPORT = ADV / "partials" / "merge-stage" / "e1-edits.json"

SYN8 = ".dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/synthesis/synth-08-value-inventory.md"
CV = "[CODE-VERIFIED by the compare orchestrator at HEAD ad8f57560]"
# item 1: plan rewrite text
KE = ("a v2 citation-only finding is rejected by the v1 parser (`findings.py:104` `_check_flat(anchor)`; "
      "`parse_block` skips it at `findings.py:188-192`), so `annotate` never sees it on the shipped merge path; "
      "`findings.annotate` raises `KeyError: 'anchor'` (`findings.py:349`) only on a direct call or if the ledger "
      "were switched to the v2 parser " + CV)
KN = ("[corrected: on the shipped merge path the v1 parser rejects a citation-only line first (`findings.py:104`; "
      "`parse_block` skips it at `findings.py:188-192`), so `annotate` never sees it; `KeyError: 'anchor'` "
      "(`findings.py:349`) arises only on a direct `annotate` call or if the ledger were switched to the v2 parser; "
      "CODE-VERIFIED by the compare orchestrator at HEAD ad8f57560]")
WD = "[SOURCE WITHDRAWN: arXiv 2606.19544, withdrawn by arXiv Admin, v2 2026-11-03; figure not used]"
CAL = ("[CODE-VERIFIED: `src/superclaude/agents/confidence-calibrator.md:3,61` says 6 dimensions; "
       "`src/superclaude/skills/sc-reflect-protocol/SKILL.md:1262,1835` says 5; diff-analysis X-030]")
CALN = "[now CODE-VERIFIED, see Appendix E]"
PR47 = "[corrected from 50: `tests/pr_submit` has 47 test files, 49 tracked `.py`]"
RO_FULL = ("[R25-INV-006, R25-INV-007: `--tools <read-only set>` and `--restricted` leave MCP servers available, so "
           "`--strict-mcp-config` is also needed; `--restricted` refuses `bypassPermissions` and confines file tools to "
           "the working directories; the gate G2 must read the MCP server list from the `system/init` event; the product "
           "already has a restricted `claude --print` child (`src/superclaude/cli/pipeline/process.py:145-154` "
           "`reviewer_profile=True`, used at `runner.py:566` and `ensemble.py:548`), and the \"gated, not built\" launcher "
           "must say whether it reuses or replaces it. Flag help text source: local `claude --help` 2.1.325 "
           "(fault-finder row 27)]")
RO_SHORT = ("[R25-INV-006, R25-INV-007: `--tools` and `--restricted` leave MCP servers available, so `--strict-mcp-config` "
            "is also needed and G2 must read the MCP server list from the `system/init` event (local `claude --help` "
            "2.1.325, fault-finder row 27); a restricted `claude --print` child already exists "
            "(`pipeline/process.py:145-154`, `reviewer_profile=True`); full note in 5.2.4]")
K6 = ("[engine-A contract keys: 32 keys by default; 33 when `t2_fallback` is set (`ensemble.py:363`, 833-834); "
      "10 outside both frozen lists by default, 11 with the key; run 1 counted 33/11]")
K7 = ("[run 1 counted 43 call sites in 11 files (unit not stated, not reproducible by the grep); "
      "`grep -rEn 'subagent_type: *\"?rf-' src/superclaude/skills` gives 52 lines in 11 files, 44 of them in 8 SKILL.md files]")
K10 = ("(mixed definitions: values written before commit 9874d63fb were not first-parse; `git show 9874d63fb`, "
       "diff-analysis X-027; run 1 V1:162)")
K11 = ("shadow09 holds the one non-1.0 calibrated value 0.9328 (`.dev/reflect/*shadow09*/panel/clusters*.json`), which "
       "the exit script does not read because the contract does not parse; run 1 V1:163")
K12 = ("engine A predates the E1 shadow work (master baseline; PRs #213, #214, #220, #329; run 1 V1:414)")
K13 = ("195 chains among 1,398 rows (1,398 counts all rows; `audit2.py` increments `rows_total` before the `<3` "
       "members filter)")
K14 = ("(this narrows the fail-open path but does not close it: the acknowledgement is not bound to item ids "
       "(C-06 INV-006), the acknowledged-drop flag state is undefined (X-14 INV-019), `blocking_state` comes from the "
       "line's own flag (Q-60))")

# (change, line, old, new, reason)
E = [
    # M-01
    ("M-01", 5, "**Research files:** 24 codebase + 4 web research (+ 12 scope slices)",
     "**Research files:** Run 2: 24 codebase + 4 web research files (12 scope slices listed, not opened, V2:108). "
     "Run 1: 13 codebase + 4 web research files, plus 6 scope slices S00-S05 used as evidence (V1:113).",
     "research-files line covers both runs"),
    # M-24 item 9 (baseline note)
    ("M-24 item 9", 108, "and are not cited as evidence.",
     "and are not cited as evidence. [Compare-merge baseline note: `origin/master` `d4d1662a8` (2026-11-14) is 3 "
     "commits past merge-base `d2d8a2d16`; HEAD `ad8f57560` is 5 commits past it; line numbers in this document are "
     "valid at HEAD; on `origin/master` the pins that C14 and C26 cite sit at `tests/skills/test_worker_contract.py:787, "
     ":796, :1872` and `src/superclaude/output-styles/pragmatic.md:229, :235` (fault-finder row 3). `e2f2ac268` (E2) "
     "is 7 commits after `6c09843` and was not read by either report.]",
     "baseline note: origin/master moved, HEAD ad8f57560, e2f2ac268"),
    # M-24 item 12
    ("M-24 item 12", 154, "**Two Tier 2 engines that share only `contract.py`.**",
     "**Two Tier 2 engines that share only `contract.py`.** Provenance: " + K12 + ".",
     "engine A provenance"),
    ("M-24 item 6", 179, "89 of the 110 stable names absent |", "89 of the 110 stable names absent " + K6 + " |",
     "engine-A key count basis"),
    ("M-24 item 10", 215, "mean 0.704 over 9 runs (pilot)", "mean 0.704 over 9 runs (pilot) " + K10,
     "0.704 mixed definitions"),
    ("M-24 item 11", 216, "(`cluster.py:50`) |", "(`cluster.py:50`); " + K11 + " |", "shadow09 0.9328 not read"),
    ("M-24 item 7", 683, "lines in 8 SKILL.md files", "lines in 8 SKILL.md files " + K7, "rf-* census unit note"),
    ("M-24 item 4", 710, "50 `tests/pr_submit/` files", "47 `tests/pr_submit/` test files " + PR47,
     "pr_submit test-file count"),
    ("M-24 item 12", 845, "behind `superclaude reflect run`).",
     "behind `superclaude reflect run`); " + K12 + ".", "engine A provenance"),
    ("M-24 item 13", 874, "195 of 1,398 rows chained", K13, "1,398 unit"),
    ("M-24 item 11", 874, "1.000 over 9 runs [CODE-VERIFIED by execution, R06 section 0]",
     "1.000 over 9 runs [CODE-VERIFIED by execution, R06 section 0]; " + K11, "shadow09 0.9328 not read"),
    ("M-24 item 3", 891, "reflect's 5 [UNVERIFIED]", "reflect's 5 " + CAL, "calibrator 6 vs 5 is code-verified"),
    ("M-24 item 6", 892, "89 of the 110 stable names are absent", "89 of the 110 stable names are absent " + K6,
     "engine-A key count basis"),
    ("M-24 item 1", 940,
     "A citation-only finding raises `KeyError: 'anchor'` in v1 `annotate` (`findings.py:349`, probe P-a), so it "
     "cannot enter the v1 ledger path (`ledger.merge_round` calls `annotate` at `ledger.py:136`)",
     "A citation-only finding cannot enter the v1 ledger path: " + KE + " (probe P-a is a direct `annotate` call)",
     "KeyError mechanism"),
    ("M-24 item 13", 1027, "195 of 1,398 rows chained", K13, "1,398 unit"),
    ("M-24 item 3", 1033, "(6 against 5 dimensions)", "(6 against 5 dimensions) " + CALN, "calibrator code-verified"),
    ("M-24 item 1", 1177, "or a recorded `anchor_status`",
     "or a recorded `anchor_status` [mechanism note: today such a line never reaches `annotate`: the v1 parser "
     "rejects it (`findings.py:104`; `parse_block` skips it at `findings.py:188-192`); `KeyError: 'anchor'` "
     "(`findings.py:349`) arises only on a direct `annotate` call or with the v2 parser; CODE-VERIFIED by the compare "
     "orchestrator at HEAD ad8f57560]", "KeyError mechanism note on a target criterion"),
    ("M-24 item 4", 1202, "50 `tests/pr_submit/` files green", "47 `tests/pr_submit/` test files " + PR47 + " green",
     "pr_submit test-file count"),
    ("M-24 item 1", 1236,
     "A v2 citation-only finding raises `KeyError: 'anchor'` in `findings.annotate` (`findings.py:349`), which "
     "`ledger.merge_round` calls (`ledger.py:136`);",
     "A" + KE[1:] + ";", "KeyError mechanism"),
    ("M-24 item 6", 1255, "89 of the 110 stable names absent", "89 of the 110 stable names absent " + K6,
     "engine-A key count basis"),
    ("M-24 item 10", 1282, "first-parse compliance mean 0.704.",
     "first-parse compliance mean 0.704 " + K10 + ".", "0.704 mixed definitions (extra site)"),
    ("M-24 item 8", 1331, "`sc-reflect-protocol/SKILL.md` (6)",
     "`sc-reflect-protocol/SKILL.md` (5 lines, 7 occurrences [corrected from \"(6)\"; `grep -c` and `grep -o`])",
     "superclaude review mention count"),
    ("M-24 item 1", 1334,
     "the v2 PARSER accepts citation-only findings but `ledger.merge_round` -> `annotate` raises `KeyError: 'anchor'` "
     "(`findings.py:346-349`, `ledger.py:127-138`)",
     "the v2 PARSER accepts citation-only findings, but on the ledger path " + KE, "KeyError mechanism"),
    ("M-24 item 4", 1335, "has 50 test files", "has 47 test files " + PR47, "pr_submit test-file count"),
    ("M-24 item 7", 1341, "(52 lines in 11 files in the tree)", "(52 lines in 11 files in the tree) " + K7,
     "rf-* census unit note"),
    ("M-24 item 13", 1368, "195 of 1,398 multi-member rows are chains", K13, "1,398 unit"),
    ("M-24 item 6", 1430, "89 of 110 absent)", "89 of 110 absent) " + K6, "engine-A key count basis"),
    ("M-24 item 1", 1437, "(`annotate` `KeyError`)",
     "(`annotate` `KeyError`) " + KN, "KeyError mechanism"),
    ("M-24 item 2", 1647, "in contrast to the 2023 literature.", "in contrast to the 2023 literature. " + WD,
     "withdrawn source"),
    ("M-24 item 2", 1648, "https://arxiv.org/html/2606.19544v1 ;", "https://arxiv.org/html/2606.19544v1 " + WD + " ;",
     "withdrawn source"),
    ("M-24 item 2", 1648, "2606.19544 carries a mid-2026 id)",
     "2606.19544 carries a mid-2026 id) [corrected: arXiv lists 2510.27106 as accepted at EMNLP 2025 (run 2 QA "
     "P6-054, `qa-consolidated-findings-phase6.md:76`); 2606.19544 is withdrawn]", "2510.27106 tier"),
    ("M-24 item 2", 1655, "(AE-1 found it much reduced)", "(AE-1 found it much reduced) " + WD, "withdrawn source"),
    ("M-24 item 5", 1728, "not `--allowedTools` (a common mistake).",
     "not `--allowedTools` (a common mistake). " + RO_FULL, "read-only mechanism incomplete (MCP)"),
    ("M-24 item 5", 1792, "(which applies only to Agent-tool subagents).",
     "(which applies only to Agent-tool subagents). " + RO_SHORT, "read-only mechanism incomplete (MCP)"),
    ("M-24 item 2", 2044, "Verbosity bias appears much smaller in recent judges.",
     "Verbosity bias appears much smaller in recent judges. " + WD, "withdrawn source"),
    ("M-24 item 5", 2054, "covers only the Agent path.", "covers only the Agent path. " + RO_SHORT,
     "read-only mechanism incomplete (MCP)"),
    ("M-24 item 2", 2072, "| 5.1.5 AE-1 | Included |",
     "| 5.1.5 AE-1 | Included (AE-1's figures from arXiv 2606.19544 are marked " + WD + ") |", "withdrawn source"),
    ("M-24 item 2", 2078, "5.1.5 AE-1 | Included as source option |",
     "5.1.5 AE-1 | Included as source option (AE-1's figures from arXiv 2606.19544 are marked " + WD + ") |",
     "withdrawn source"),
    ("M-24 item 1", 2177,
     "a v2 citation-only finding crashes the v1 ledger path (`KeyError: 'anchor'`, `findings.py:349`, called from "
     "`ledger.py:136`).", KE + ".", "KeyError mechanism"),
    ("M-24 item 1", 2226, "a citation-only finding crashes the v1 ledger path (R01 P-a);",
     "a citation-only finding crashes the v1 ledger path (R01 P-a) " + KN + ";", "KeyError mechanism (extra site)"),
    ("M-24 item 10", 2370, "pilot mean 0.704 over 9 runs", "pilot mean 0.704 over 9 runs " + K10,
     "0.704 mixed definitions (extra site)"),
    ("M-24 item 6", 2507, "10 keys outside the frozen lists", "10 keys outside the frozen lists " + K6,
     "engine-A key count basis (extra site)"),
    ("M-24 item 6", 2703, "89 of 110 stable names absent", "89 of 110 stable names absent " + K6,
     "engine-A key count basis"),
    ("M-24 item 2", 2829, "(W01 AE-1; external, transfer unverified).",
     "(W01 AE-1; external, transfer unverified). " + WD, "withdrawn source"),
    ("M-24 item 7", 2953, "lines in 8 SKILL.md files", "lines in 8 SKILL.md files " + K7, "rf-* census unit note"),
    ("M-24 item 4", 2973, "50 test files pin", "47 test files " + PR47 + " pin", "pr_submit test-file count"),
    ("M-24 item 3", 3323, "the claim is [UNVERIFIED], carried from slice 10 and not re-read",
     "the claim is [UNVERIFIED], carried from slice 10 and not re-read; the calibrator part is now " + CAL,
     "calibrator 6 vs 5 is code-verified"),
    ("M-24 item 1", 3329,
     "a citation-only finding raises `KeyError: 'anchor'` in `annotate`, so v2 findings cannot enter the v1 ledger "
     "path (no code path from v2 findings to the ledger)",
     KE + "; so v2 findings cannot enter the v1 ledger path (no code path from v2 findings to the ledger)",
     "KeyError mechanism"),
    ("M-24 item 4", 3357, "the 50 `tests/pr_submit` files", "the 47 `tests/pr_submit` test files " + PR47,
     "pr_submit test-file count"),
    ("M-24 item 7", 3387, "lines over 8 skills are exact", "lines over 8 skills are exact " + K7,
     "rf-* census unit note (extra site)"),
    ("M-24 item 1", 3411,
     "a v2 citation-only finding raises `KeyError` in `annotate`, so location type blocks the ledger and merge path",
     KE + "; so location type blocks the ledger and merge path", "KeyError mechanism"),
    ("M-24 item 3", 3474, "5- versus 6-dimension calibrator", "5- versus 6-dimension calibrator " + CALN,
     "calibrator code-verified"),
    ("M-24 item 1", 3487, "a v2 citation-only finding raises `KeyError` in `annotate`;", KE + ";",
     "KeyError mechanism"),
    ("M-24 item 4", 3496, "the 50 `tests/pr_submit` files", "the 47 `tests/pr_submit` test files " + PR47,
     "pr_submit test-file count"),
    ("M-24 item 14", 3516, "a dropped-blocking refusal with an acknowledgement exit",
     "a dropped-blocking refusal with an acknowledgement exit " + K14, "fail-open narrowed, not closed"),
    ("M-24 item 5", 3517, "(no `--restricted` run on a gateway id exists)",
     "(no `--restricted` run on a gateway id exists) " + RO_SHORT, "read-only mechanism incomplete (MCP)"),
    ("M-24 item 1", 3636, "a citation-only finding crashes the v1 ledger path,",
     "a citation-only finding crashes the v1 ledger path " + KN + ",", "KeyError mechanism (extra site)"),
    ("M-24 item 1", 3637,
     "a v2 citation-only line crashes the v1 ledger path with `KeyError 'anchor'` (r01 §3 P-a, r17 DR-113, REPRODUCED)",
     KE + " (r01 §3 P-a, r17 DR-113, REPRODUCED as a direct `annotate` call)", "KeyError mechanism"),
    ("M-24 item 14", 3638, "a fail-closed refusal with an acknowledgement exit when a blocking line was dropped",
     "a fail-closed refusal with an acknowledgement exit when a blocking line was dropped " + K14,
     "fail-open narrowed, not closed"),
    ("M-24 item 5", 3640, "the CLI flags `--tools` and `--restricted` are named in W02 sections 4, 10).",
     "the CLI flags `--tools` and `--restricted` are named in W02 sections 4, 10). " + RO_FULL,
     "read-only mechanism incomplete (MCP)"),
    ("M-24 item 5", 3658, "(no `--restricted` run on a gateway id exists)",
     "(no `--restricted` run on a gateway id exists) " + RO_SHORT, "read-only mechanism incomplete (MCP)"),
    ("M-24 item 1", 3666, "a v2 citation-only finding raises `KeyError` in `annotate` (r01 §3 P-a)",
     KE + " (r01 §3 P-a)", "KeyError mechanism"),
    ("M-24 item 4", 3735, "50 test files under", "47 test files " + PR47 + " under", "pr_submit test-file count"),
    ("M-24 item 7", 3736, "(44 structured `subagent_type` lines in 8 SKILL.md files)",
     "(44 structured `subagent_type` lines in 8 SKILL.md files) " + K7, "rf-* census unit note"),
    ("M-24 item 13", 3743, "195 of 1,398 multi-member rows chained", K13, "1,398 unit"),
    ("M-24 item 4", 3797, "(50 files, 47 `test_*.py`)",
     "(50 files, 47 `test_*.py`) [corrected: 49 tracked `.py` files, 47 of them `test_*.py`; 91 tracked files "
     "including fixtures; no count gives 50]", "pr_submit file count (extra site)"),
    ("M-24 item 4", 3804, "50 test files under", "47 test files " + PR47 + " under", "pr_submit test-file count"),
    ("M-24 item 7", 3820, "lines in 8 SKILL.md files", "lines in 8 SKILL.md files " + K7, "rf-* census unit note"),
    ("M-24 item 1", 3882, "a v2 citation-only line raises `KeyError 'anchor'` in the ledger path", KE,
     "KeyError mechanism"),
    ("M-24 item 7", 3892, "44 structured lines exact", "44 structured lines exact " + K7, "rf-* census unit note"),
    ("M-24 item 5", 4085, "confines file tools to the working directories",
     "confines file tools to the working directories " + RO_SHORT, "read-only mechanism incomplete (MCP)"),
    # M-12
    ("M-12", 4234, "## 8. Value Inventory and Inputs for a Later Plan",
     "## 8. Value Inventory, Migration and Value-Capture Content, and Inputs for a Later Plan", "Section 8 retitle"),
    ("M-12", 4236,
     "Section 8 gives the value inventory (8.1) and the sequence and gates (8.2). Both are inputs for a later plan. "
     "Neither is a roadmap, a branch plan, a PR plan or a risk register.",
     "Section 8 gives run 2's value inventory (8.1) and the sequence and gates (8.2). Both are inputs for a later "
     "plan. For what this document adds there is no roadmap, no branch plan, no PR plan, no risk register, no "
     "estimate and no schedule. Subsections 8.3 to 8.8 carry run 1's value-capture and migration content as content "
     "(inventory rows, steps with their status against the adopted design, gates, risk inputs); that content orders "
     "no work and is not a plan.", "Section 8 lead"),
    # M-13
    ("M-13", 4280,
     "which is the file `" + SYN8 + "` (2,024,775 bytes, 6,127 lines, unchanged). Appendix A is part of the report "
     "package.",
     "which is the file `" + SYN8 + "` (2,024,775 bytes, 6,127 lines, unchanged). The 5,950 rows live in `" + SYN8
     + "`, committed at `ad8f57560`; the pointer is `ad8f57560:" + SYN8 + "`, which still resolves if the task folder "
     "moves (R25-INV-023). Run 2's Q-35 asked whether its `.dev/tasks` output may be committed; it was committed at "
     "`ad8f57560`; whether it was pushed is not checked here.", "value-inventory pointer pinned to a commit"),
    ("M-24 item 6", 4503, "lacks 89 of the 110 stable names.", "lacks 89 of the 110 stable names " + K6 + ".",
     "engine-A key count basis (extra site)"),
    ("M-24 item 1", 4508,
     "but `ledger.merge_round` calls `annotate` on every parsed finding and `annotate` does "
     "`locate(text, finding[\"anchor\"])` with no default, so the finding raises `KeyError 'anchor'`.",
     "but " + KE + " (`annotate` does `locate(text, finding[\"anchor\"])` with no default).", "KeyError mechanism"),
    ("M-24 item 4", 4479, "(50 test files plus", "(47 test files " + PR47 + " plus", "pr_submit test-file count"),
    ("M-24 item 4", 4593, "(50 test files)", "(47 test files " + PR47 + ")", "pr_submit test-file count"),
    ("M-24 item 7", 4602, "operational-guide, tdd)", "operational-guide, tdd) " + K7, "rf-* census unit note"),
    ("M-24 item 1", 4677, "on the ledger path:", "on the ledger path " + KN + ":", "KeyError mechanism"),
]


def main() -> int:
    raw = BASE.read_bytes()
    text = raw.decode("utf-8")
    lines = text.split("\n")
    assert len(lines) == 5099 and lines[-1] == "", "base must be 5,098 lines ending in a newline"
    orig = list(lines)
    tags: dict[int, list[str]] = {}
    log = []
    for change, n, old, new, reason in E:
        cur = lines[n - 1]
        c = cur.count(old)
        assert c == 1, f"{change} line {n}: old text occurs {c} times in the line: {old[:80]!r}"
        lines[n - 1] = cur.replace(old, new, 1)
        tags.setdefault(n, []).append(f"{change}: {reason}")
        log.append({"change": change, "line": n, "old": old, "new": new, "reason": reason,
                    "file_count_of_old_in_base": text.count(old)})
    for n, rs in tags.items():
        seen = []
        for r in rs:
            if r not in seen:
                seen.append(r)
        lines[n - 1] += " <!-- Source: Base (original, modified) — " + "; ".join(seen) + " -->"
    out = "\n".join(lines)
    assert len(lines) == len(orig)
    OUT.write_text(out, encoding="utf-8")
    REPORT.write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    # self-check: only tagged lines differ, every differing line ends with the provenance comment
    changed = [i + 1 for i, (a, b) in enumerate(zip(orig, lines)) if a != b]
    assert set(changed) == set(tags), "changed lines must equal tagged lines"
    assert all(lines[i - 1].endswith(" -->") and "<!-- Source: Base (original, modified)" in lines[i - 1]
               for i in changed)
    assert BASE.read_bytes() == raw, "base must be unchanged"
    print(f"edits={len(E)} changed_lines={len(changed)} lines={len(lines) - 1}")
    print("changed:", changed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
