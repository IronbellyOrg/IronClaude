# Wave 1B tasklist-to-artifact map (UC-2, docs-only work unit, attempt 2)

TASK = TASK-RESEARCH-orchestrator-supervision-20261107-073942.md (task folder root). No diff: the work unit makes no commit; the "hunks" are the produced files.

Checklist state at snapshot 2026-11-08T02:19:07Z: 78 checked, 2 unchecked (TASK:358 item 7.5 = this reflect gate; TASK:360 item 7.6 = close-out, gated on 7.5).

| Task / requirement | Card ID | Status (orchestrator pre-read) | Grounding |
|---|---|---|---|
| Obj 1: verify scope-01..04 citations (TASK:60) | C-01 | covered | research/scope-01..04 |
| Obj 2: G-A row schema + G-B open questions (TASK:61) | C-02 | covered | research/05-orca-row-schema.md, 06-orca-open-questions.md, 07-gate-gap-fill.md |
| Obj 3: research gate, max 2 fix cycles, gaps file (TASK:62) | C-03 | covered by coordinator exception (NB-4) | qa/qa-research-*, qa/qa-nb4-fix-log.md, gaps-and-questions.md |
| Obj 4: two external-pattern files (TASK:63) | C-04 | covered (WebSearch fallback deviation) | research/web-01..02 |
| Obj 5: six synthesis files + synthesis gate (TASK:64) | C-05 | covered | synthesis/synth-01..06, qa/qa-synthesis-*, qa/analyst-synthesis-* |
| Obj 6: report 10 sections; lens, fidelity, anti-omission gates (TASK:65) | C-06 | covered; anti-omission passed with owner exceptions (TASK:451, :558) | RESEARCH-REPORT-orchestrator-mode.md; qa/qa-lens-*, qa-fidelity-*, qa-anti-omission-* |
| Obj 7: close-out, summary, I17 check (TASK:66) | C-07 | 7.1-7.4 covered; 7.5-7.6 pending by design | synthesis/phase7-summary.md, TASK:366-376 |
| Read-only constraint: nothing outside the task folder changed | C-08 | covered | baseline-git-status.txt equals `git status --porcelain` at 02:19Z (3 identical untracked entries) |
| Owner exceptions GQ-101..110 recorded in gaps log; report deliberately not edited (TASK:456) | C-09 | covered, to verify | gaps-and-questions.md:135; TASK:456 |
| Report cross-file citations to gaps log (`gaps-and-questions.md:125` at report :229, :1127, :1474) still resolve | C-10 | candidate drift | report :229/:1127/:1474 vs gaps-and-questions.md:135 summary |
