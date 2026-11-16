f2d9aa599c7902998c3d2f468eac1a3adc628b85
family=stale-citation
defect form: a line pointer or rule id copied from `research/09-gap-fill.md` Gap 1 into the "Constraint on Phase 1" column of `artifacts/owner-decisions.md` that no longer names the live text (the DESIGN and the rule numbering changed after research/09 was written on 2026-11-08).
command: grep -n -E -e 'DESIGN:[0-9]+|REPORT:[0-9]+|GAPS:[0-9]+|WC-14' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/owner-decisions.md
before-output:
41: REPORT:1277
42: WC-14 G7
43: GAPS:63, REPORT:1246
44: REPORT:1276, DESIGN:638
48: DESIGN:925
coupled sites: every pointer in the same column: D3 (REPORT:1277), D4 (WC-14 G7), D5 (GAPS:63, REPORT:1246), GIT (REPORT:1276, DESIGN:638), UPSTREAM (DESIGN:925). The REPORT and GAPS pointers name external research documents that this task does not re-read; the fix marks them as "as cited in research/09" instead of re-anchoring them. The two DESIGN pointers and the WC-14 label are re-anchored to the live lines (DESIGN:643 and 647, DESIGN:736, DESIGN:947, `src/superclaude/core/WORKER-CONTRACT.md:63`).
after:
41: REPORT:1277 (as cited in research/09, stated in the section preface)
42: WC-14 G7 (original text kept, followed by a bracketed note that names WC-16 and WORKER-CONTRACT.md:63)
43: GAPS:63, REPORT:1246 (as cited in research/09)
44: REPORT:1276 (as cited in research/09); DESIGN:638 (kept only inside the bracketed re-anchoring note, which names DESIGN:643 and DESIGN:647)
48: DESIGN:925 (kept only inside the bracketed re-anchoring note, which names DESIGN:947)
