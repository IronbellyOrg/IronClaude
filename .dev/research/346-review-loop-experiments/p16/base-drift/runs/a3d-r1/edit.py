import json
p='ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md'
s=open(p,encoding='utf-8').read()
log=[]
def rep(fid,old,new):
    global s
    assert s.count(old)==1,(fid,old[:40],s.count(old))
    s=s.replace(old,new)
    log.append((fid,len(old.encode()),len(new.encode())))
# B-1
rep('B-1',"In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows",
"In unattended mode the command writes the contract at a path the brief names: `<dir>/return-contract.yaml` when the coordinator passes a directory (`--output` / `--output-dir`), or `<file>.return-contract.yaml` beside the file when `--output` is a file (so two workers given `a.md` and `b.md` never share one, WC-11). Two named exceptions: adversarial writes `<output>/adversarial/return-contract.yaml`; workflow writes `.dev/tasks/to-do/<id>/return-contract.yaml`, whose `<id>` the command creates, so the worker finds the path after the package exists and a stop before the package exists writes no contract (WC-5: no report means `--outcome failed`). It follows")
rep('B-1',"It is written on success, failure, blocked and partial outcomes, including stops before any other output exists.",
"It is written on success, failure, blocked and partial outcomes, including stops before any other output exists (except workflow's pre-creation stops, above).")
rep('B-1','"Contract" means the WC-4 file `<output-dir>/return-contract.yaml`.','"Contract" means the WC-4 contract file.')
rep('B-1',"the output directory, so the report path is known before dispatch (WC-4)","the output directory or file, so the report path is known before dispatch (WC-4; workflow excepted)")
rep('B-1',"| Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) |","| Fix the contract filename to `<output>/adversarial/return-contract.yaml`, the WC-4 exception path (P1) |")
rep('B-1',"| Write the contract for pre-creation STOPs too (WC-4 \"every outcome\") (P1) |","| None: a pre-creation STOP writes no contract and the worker reports `--outcome failed` (WC-4 exception, WC-5) |")
rep('B-1',"fixes to adversarial, cleanup-audit, index-repo, workflow |","fixes to adversarial, cleanup-audit, index-repo |")
rep('B-1',"adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |","adversarial names the one fixed path `<output>/adversarial/return-contract.yaml` |")
rep('B-1',"(roadmap and validate-roadmap drift, validate-tests target, adversarial and workflow contract gaps,","(roadmap and validate-roadmap drift, validate-tests target, adversarial contract gap,")
# B-2
rep('B-2',"the worker reports the named file until Phase 1 adds the contract.","the worker reports the named file until the command's own phase (last column) adds the contract. `brainstorm` and `init-lite` have no change and no `## Unattended mode` section.")
rep('B-2',"Every changed command also gains the `## Unattended mode` section (section 2.1).","Every changed command also gains the `## Unattended mode` section (section 2.1) in its own phase, except `load` (no contract, usage-line fix only) and `pr-submit` (changed only if D3 (b) is chosen). Until a command's phase passes, the coordinator does not put `--unattended` in its brief.")
rep('B-2',"the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate);","the `--unattended` flag accepted by the commands listed in this row, except `load` (a no-op where a command has no gate);")
rep('B-2',"pr-submit as a worker. |","pr-submit as a worker (only if D3 (b)). |")
rep('B-2',"the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section","the test asserts that every P1 command (the commands listed in the P1 row, not `load`) has a `## Unattended mode` section")
open(p,'w',encoding='utf-8').write(s)
json.dump(log,open('log.json','w'))
print(log)
