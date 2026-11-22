# Explanation (advanced): `superclaude review safety-scan`

Source: origin/master, read with `git show`. Codegraph not used (graph:stale).

## Purpose
Reviewers sometimes grade a dangerous finding as minor (for example "nit: quoting" on a recipe that runs `rm -rf "$DIR/"` with `DIR` unset). A word scan, done by code and not by a model, catches such rows so a person sees them. The command only prints. It stores nothing and changes no verdict.

## Layers
1. `src/superclaude/cli/review/safety_route.py` is the pure logic.
   - `VOCABULARY` (lines 19-29): delete, overwrite, force, token, secret, password, chmod, credential, wipe. One list, called GR1 (guardrail 1: "safety is never downgraded") in the program spec.
   - `_PATTERN` (31-34): case-insensitive, must start at a word start. "deleted" and "tokens" hit, "reinforce" does not.
   - `scan_text` (63-84): one row per line, blank lines are not rows, a row starting with `superseded ` is counted as skipped and never scanned, first vocabulary match per row is the hit.
   - `scan_file` (87-102): reads bytes, decodes UTF-8. Missing file, directory, OS error and bad UTF-8 return an `Unreadable` result, which is a different type from "zero hits".
   - `raise_outcome` (105-114): GR12 raise-only rule. A hit moves Note or Medium to Blocking, never lowers anything, unknown outcome raises ValueError. Only tests call it today (UNVERIFIED beyond a grep of src and tests on origin/master).
2. `src/superclaude/cli/review/safety_cmd.py` is the click command `safety-scan <file> [--unattended]`.
   - Hit line format: `SAFETY HIT line N (word), graded blocking: <row>`.
   - Summary: `safety-scan: R rows read, S skipped, H hits` or `file is empty, 0 rows read`.
   - Attended with hits: prints "Show these rows to the person before they are treated as follow-ups."
   - `--unattended`: no prompt; last line `safety-scan signal: partial` (hits) or `none`.
   - Exit 0 on any readable input, exit 2 on unreadable input with no counts printed.
3. `src/superclaude/cli/review/__init__.py` registers `safety_cmd` in a tuple of optional modules loaded with importlib; a missing module is skipped, so branches adding different subcommands do not collide.

## Why "print-only"
It prints, asks nobody, calls no model or network, writes no tag and edits no ledger. The skill text for `/sc:implement` says it "asks the user nothing, makes no offer, changes no verdict, no final-review result and no archive outcome, adds no stop code" and a failed or missing command is printed as one line and the run continues. Test `test_module_imports_no_unrelated_reader_and_makes_no_call_out` pins the no-call-out property by parsing imports.

## Wiring into skills
`sc-implement-protocol/SKILL.md` (Done section) and `refs/managed-workspace.md` (after the FINAL block, before archive step 6) carry a "Follow-up print (record and print only)" paragraph: print every non-superseded minor line of each task notes file, then run the scan on each notes file; a hit prints first and stays blocking; a missing notes file prints "no notes file for T<id>". Both files are mirrored byte for byte in `plugins/superclaude/skills/sc-implement-protocol/`.

## Correction to the brief
PR #581 changed `sc-reflect-protocol/SKILL.md` and `refs/reviewer-spec.md`, but those edits are shadow-mode fixes (card model pinning, merged-verdict.yaml, findings-block compliance), not a safety-scan paragraph. No `safety-scan` text exists in sc-reflect-protocol on origin/master.

## Why it exists
Issue 552: review gates mark too many findings blocking. The program loosens that, with a classifier planned, but keeps one hard rule: safety is never downgraded. After a cuts debate (Revision 4 of the stage 1 request) the classifier, ledger codec and shadow stages were cut and only this scan and the print paragraph were kept.
