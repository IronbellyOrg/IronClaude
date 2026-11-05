# Reviewer 1 card (persona: analyzer; model class: sonnet). Persisted by the orchestrator from the reviewer's returned text, condensed; claims and evidence refs are unchanged.
reviewer: 1
persona: analyzer
findings:
  - id: F1
    claim: Lifting --name/-n and CCSESSION_NAME into `ccsession --name`, and starting every launch with an auto-name, has no fallback when ccsession --name or --auto-name fails. An invalid lifted or env name (control character, over 245 bytes) or an empty/invalid auto-name (worktree folder name failing validate_label, or set -e) makes ccsession exit 2 before Claude starts. Today every Orca path starts Claude and the ccsession-orca header promises it never ends up at a dead prompt.
    tag: grounded
    evidence: ccsession:1649-1653 (TOPIC=$(validate_label ...) || exit 2); ccsession:98 (set -e); ccsession-orca:20-24 header; ccsession-orca:34 (set -e)
    severity: blocking
    deviation_class: regression
    recommendation: ccsession-orca validates the lifted or env name first; if invalid, fall back to the pass-through (name left in the arguments) or to an auto-name. If --auto-name returns empty or non-zero, exec the untagged start. --auto-name sanitizes the folder-name part (control characters, empty) or falls back to a fixed word. Tests: worktree folder with a leading dot, --name with a tab, 300-character CCSESSION_NAME; each must still reach the fake Claude.
  - id: F2
    claim: A control-character check on the `read -r` result cannot see a leading or trailing tab, because `read -r name` without IFS= strips leading and trailing space and tab. An indented pasted line becomes a valid name and never reaches exit 3.
    tag: grounded
    evidence: ccsession:1482
    severity: minor
    deviation_class: drift
    recommendation: Use IFS= read -r, test the raw line for [[:cntrl:]] and the 245-byte rule, then trim spaces; or send every non-blank validate_label failure to exit 3. Test leading-tab, trailing-tab and mid-line tab lines.
  - id: F3
    claim: The multi-line-paste probe after read has a timing race; a zero-timeout select right after the first line misses a paste that has not fully arrived. A pty test that writes everything in one os.write hides it.
    tag: inferred
    evidence: null
    severity: minor
    deviation_class: none
    recommendation: Run the second probe with a 100-200 ms select timeout under stty -icanon min 0 time 0, restore from the saved tty_mode, keep the INT trap, and keep both probes inside if/&& lists because set -e is on (ccsession:98).
  - id: F4
    claim: Draining the rest of a paste cannot be done in portable bash (read -t 0.2 fails on bash 3.2, which the file supports); it needs python3 with raw bytes, a bounded loop, and a size cap because one exec argument over about 128 KiB fails.
    tag: grounded
    evidence: ccsession:1426
    severity: minor
    deviation_class: none
    recommendation: Task 2 uses python3 -c with os.read on fd 0 and sys.stdout.buffer.write, bounded loop and timeout, and caps or refuses text above about 128 KiB.
  - id: F5
    claim: Exit-3 text appended as the last positional argument without `--` is parsed as an option when it starts with `-`, and a variadic option earlier in Orca's arguments (--add-dir, --allowedTools, --mcp-config) swallows it.
    tag: grounded
    evidence: ccsession:630-633; ccsession-orca:115-117
    severity: minor
    deviation_class: none
    recommendation: Task 4 appends `-- "$text"` when the text starts with `-`; pty tests for "- a list" and "--version".
  - id: F6
    claim: Task 5 misses test_orca_invalid_name_asks_again (246 x's and 82 Japanese characters now go to exit 3), and test_orca_ctrl_c_while_line_mode_is_off_restores_the_terminal launches with the argument "the prompt", which under the new rule is never asked, so it must drop the prompt argument as well as expect 130.
    tag: grounded
    evidence: tests/unit/test_ccsession_tag.py:1592-1610; tests/unit/test_ccsession_tag.py:1536-1559
    severity: minor
    deviation_class: none
    recommendation: Add test_orca_invalid_name_asks_again to Task 5, rewritten; remove the prompt argument from the Ctrl+C test.
  - id: F7
    claim: _orca_env strips CCSESSION_AUTOSTART and CCSESSION_ASK_TIMEOUT but not the new CCSESSION_NAME, so a developer who exported it turns every asked test into a name-carried test.
    tag: grounded
    evidence: tests/unit/test_ccsession_tag.py:1335-1346
    severity: minor
    deviation_class: none
    recommendation: Add CCSESSION_NAME to that exclusion list in Task 5 (and tests/unit/test_ccsession_tiers.py:424).
  - id: F8
    claim: Neither Task 3 nor Task 4 removes CCSESSION_NAME from Claude's environment, so nested launches inherit it and resume the parent's conversation.
    tag: inferred
    evidence: null
    severity: minor
    deviation_class: none
    recommendation: ccsession-orca unsets CCSESSION_NAME before every exec; assert it is absent from env_names in the record.
  - id: F9
    claim: No-terminal launches with a non-session positional (mcp list, doctor, update) or --version/--help would get --name injected and a topic directory written; today they pass through unchanged.
    tag: inferred
    evidence: null
    severity: minor
    deviation_class: drift
    recommendation: Treat -v/--version/-h/--help and a first positional in {mcp, config, doctor, update, install, auth, plugin, setup-token, agents} as pass-through untagged; add a --version test.
  - id: F10
    claim: Lifting --name/-n is a behaviour change not in the source; a saved label now resumes the old conversation; with --session-id Claude rejects the combination; the lift is not skipped for resume-like launches (double --resume possible).
    tag: grounded
    evidence: ccsession:1692-1705; ccsession-orca:75-76
    severity: minor
    deviation_class: drift
    recommendation: Prefer leaving --name in Claude's arguments (no question, no auto-name) unless the owner confirms the lift; if kept, skip the lift for resume-like or --session-id launches and handle --name=x and a trailing --name with no value.
  - id: F11
    claim: Task 3 matches --session-id and --prefill only as separate words; the --session-id=<id> and --prefill=<text> forms would be neither positional nor listed, and the launch would still be asked.
    tag: grounded
    evidence: ccsession-orca:75-76
    severity: minor
    deviation_class: drift
    recommendation: Add --session-id=*, --prefill=* and --name=* to the classification; test one of each form.
  - id: F12
    claim: Placing --auto-name next to --ask puts it after the argument loop, which consumes --shim, --claude-args, --model, --tier, --profile and --name text, so `--auto-name "--model"` exits 2 and breaks "never break the shell".
    tag: grounded
    evidence: ccsession:597-628; ccsession:648-723; ccsession:1543-1546; ccsession:104
    severity: minor
    deviation_class: none
    recommendation: Add --auto-name to the early fast-path case (about ccsession:597-628) with ${2:-}; test the texts --model, --claude-args, --shim.
  - id: F13
    claim: Removing trap ':' INT works only if ccsession-orca handles status 130 explicitly; a SIGINT before ccsession's own trap is installed gives a signal death, not 130, and `|| name=""` discards the status.
    tag: inferred
    evidence: null
    severity: minor
    deviation_class: none
    recommendation: Keep `trap 'exit 130' INT` around the capture, use `rc=0; name=$(...) || rc=$?`, and have tests accept exactly 130 and check ICANON afterwards.
  - id: F14
    claim: Auto-name uniqueness checks only for an existing topic file, which the SessionStart hook writes later, so two parallel launches in the same folder, same text, same minute pick the same label; a label just written by another session would be resumed.
    tag: grounded
    evidence: ccsession:1681-1706; ccsession:328-338
    severity: minor
    deviation_class: none
    recommendation: Add seconds or a short random suffix to the stamp, or reserve the label with a marker.
risks_rejected:
  - R1 largely: exit status keys the message path; $(...) keeps inner newlines; the only real problems are set -e (use || rc=$? at ccsession-orca:108) and F4/F5.
  - R4: with an auto-name the topic file does not exist, so ccsession takes the new-session branch (ccsession:1707-1713); a conflict arises only with a lifted explicit saved name (F10).
verdict: ready-with-notes
self_confidence: 0.72
calibration:
  calibrator_model_class: opus
  calibrated_confidence: 0.75
  note: blind calibration; blocking finding F1 verified against ccsession:1649-1653, ccsession:98, ccsession-orca:20-24,34
