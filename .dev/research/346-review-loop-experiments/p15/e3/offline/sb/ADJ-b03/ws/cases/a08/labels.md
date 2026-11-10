## Label A
blocking: no
sentence: The coordinator is told per command which report file to read (section 3 rows). An implementer who follows the text builds adversarial writing <output>/adversarial/return-contract.yaml, which is a deterministic path derived from the passed --output, so the coordinator can know it; the claim that it reads the wrong place needs the assumption that the coordinator ignores the row. Workflow has no --output and its row lists its own existing path; research's contract sits in the output dir and only names the generated report (report_path), so the quoted problem for research does not follow. Only the adversarial/workflow rows are in tension with WC-4 and the rows are marked as pre-P1 small fixes.
evidence: L62 WC-4 '<output-dir>/return-contract.yaml'; L79 'worker reports the named file until Phase 1 adds the contract'; L83 '<output>/adversarial/return-contract.yaml'; L92 '.dev/tasks/to-do/<id>/return-contract.yaml'; L116 'contract naming the generated claudedocs/research_*.md path'; L62 report_path field
confidence: low

## Label B
blocking: no
sentence: An implementer following WC-4 writes <output-dir>/return-contract.yaml, but the adversarial row names <output>/adversarial/return-contract.yaml and the workflow row names an id-based path; whether <output> equals <output-dir> and how the workflow id is known before dispatch both need a guess, so the stated texts do not force a wrong build.
evidence: WC-4 line 62 '<output-dir>/return-contract.yaml'; section 2.3 line 73; adversarial row line 83 '<output>/adversarial/return-contract.yaml'; workflow row line 92 '.dev/tasks/to-do/<id>/return-contract.yaml' with 'Fresh package each run'; research row line 116 'claudedocs/research_*.md'
confidence: low
