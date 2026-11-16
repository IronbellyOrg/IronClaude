5dc29d23b15eb7db4ead50623bb409f696a0d7d3
Family: report-pin-frame-claim (covers F1.1 of review r1-1)
- Defect form: a sentence in qa-test-coverage-report.md says the failure pins carry their frame, but three of the five failure pins in tests/commands/test_sweep_command.py (malformed JSON, missing summary or report_path, Read failed or denied) are bare fragments of SKILL.md:29.
- Probe command: grep -n -i -e "includes its frame" -e "each pin" -e "its frame" .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/cmd-skill/qa-test-coverage-report.md
- Before-output: two hits: line 56 (the addendum negative-cases row, the defect) and line 60 (the unrelated phrase "each pinned string" in the style-sites row, not a frame claim).
- Coupled sites: none; no other row repeats the claim.
- after: (grep -n -i -e "includes its frame" -e "each pin" -e "its frame" on the report)
  - 60:Seven mandatory-table sites (primary bullet `pragmatic.md
  - (line 56 no longer hits; the remaining line 60 hit is the unrelated phrase "each pinned string")
