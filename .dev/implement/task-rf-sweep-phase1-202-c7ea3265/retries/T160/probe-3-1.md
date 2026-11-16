d29d79dbffd22062a70c65c1a0e6c35a8881aec6
family=citation-offset
defect form: a relative position ("N lines above/below") between two cited lines stated wrongly in the appended reader-level table.
command: grep -n -E 'lines? (above|below)' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/verify-cycle1-rf-qa-qualitative.md
before-output (state reviewed in review 3): line 331 "two lines above :1057"
coupled sites: none; the same phrase does not occur elsewhere in the report.
after: line 331 reads "the line above :1057" (verifier edit).
