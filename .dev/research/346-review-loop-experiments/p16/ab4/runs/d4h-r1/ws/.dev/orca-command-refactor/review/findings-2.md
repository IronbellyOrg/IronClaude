### M1
| M1 | open (deferred part) | :62, :83, :92 now name the paths; cli-portify is still unnamed at :62 and :105 | revise1.md:71 leaves the cli-portify location to P2. The reviser's deferral counts as open. |
(text of this finding in the prior report)
### M1
#### M1.a, from round1-a.md F1: *F1. The contract path rule in WC-4 cannot be followed by the commands the spec lists.** Severity MAJOR. Grade: blocking. Expert: Wiegers (lead), Cockburn.
- WC-4 says the contract is `<output-dir>/return-contract.yaml` where `<output-dir>` is the directory passed as `--output`/`--output-dir` (SPEC:62). SPEC:73 says the coordinator's brief gives the report path "so the report path is known before dispatch".
- SPEC:83 (adversarial) requires `<output>/adversarial/return-contract.yaml`, a subfolder. SPEC:87 (init-lite) takes `--output <file>`, not a directory. SPEC:90 (tdd) takes `--output <file>`. SPEC:92 (workflow) has no output flag; its contract lives under `.dev/tasks/to-do/<id>/`. SPEC:85 (cleanup-audit) uses a fixed `.claude-audit/` path. SPEC:105 (cli-portify) leaves the location unnamed.
- Grading sentence: an implementer who follows WC-4 and SPEC:73 has the coordinator open `<output-dir>/return-contract.yaml` for adversarial, but SPEC:83 makes the file `<output-dir>/adversarial/return-contract.yaml`, so the coordinator opens a path that does not exist.
