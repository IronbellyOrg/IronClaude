bb81b38e05ceba722056deefcfe14c6e09506228
family=stale-self-line-ref
defect form: a "line N" pointer inside text this task inserted that no longer names the line it meant, because the task's own insertions shifted the lines.
command: grep -nE -e 'Time parsing \(design\).*line [0-9]+' -e 'first_record_ts.*line [0-9]+' -e 'dispatch_started.*line [0-9]+' docs/designs/orchestrator-mode.md
before-output:
468:Time parsing (design): every Orca and transcript time is ...
coupled sites: the three inserted rows/paragraph (lines 455, 457, 468) are the only text this task added; only line 468 carries a "line N" pointer.
after:
(no hits)
