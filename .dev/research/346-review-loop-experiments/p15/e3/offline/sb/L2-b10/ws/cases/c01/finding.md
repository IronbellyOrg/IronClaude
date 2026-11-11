**F-04. WC-4 says the report path is known before dispatch, but the rows give paths that are not.**
WC-4 (line 62) and §2.3 (line 73) require `<output-dir>/return-contract.yaml`, known to the coordinator before dispatch. Three rows conflict with this:
- adversarial (line 83): fixes the contract to `<output>/adversarial/return-contract.yaml`. That is not `<output-dir>/return-contract.yaml`, so one command has two paths. The inventory says the skill names no file (INV-A:35, INV-A:60).
- workflow (line 92): `.dev/tasks/to-do/<id>/return-contract.yaml`. `<id>` is created at run time, and the workflow never reuses a package (INV-B:52, INV-B:273), so the coordinator cannot know it before dispatch.
- research (line 116): a contract naming the generated `claudedocs/research_[topic]_[timestamp].md`. INV-B:132 says the exact name is generated at run time and "the worker must report the path it wrote".
An implementer following WC-4 cannot give the coordinator a path before dispatch for workflow or research, and the adversarial path differs from the rule. The coordinator then reads from the wrong place or none.
Fix: give workflow and research a fixed `--output` (or contract path parameter) in P1, and make the adversarial row use the WC-4 path, or amend WC-4 to allow the exception.
