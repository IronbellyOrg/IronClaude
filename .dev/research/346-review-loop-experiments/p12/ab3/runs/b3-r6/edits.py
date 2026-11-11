import difflib, json, sys
P='ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md'
t=open(P,encoding='utf-8').read()
before=len(t.encode())
E=[]
def ed(fid,old,new):
    global t
    assert t.count(old)==1,(fid,old[:60],t.count(old))
    t=t.replace(old,new)
    E.append((fid,old,new))

ed('F-01',"**One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`).",
"**One report file, at the path its section 3 row names, written on every outcome.** In unattended mode the command writes `return-contract.yaml` at the path its section 3 row names. The default is `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`); where `--output` names a file it is `<that file path>.return-contract.yaml`; adversarial and workflow keep the paths in their rows.")
ed('F-01',"including stops before any other output exists. Commands that already","including stops before any other output exists (except workflow stops before its package folder exists, which write none; WC-5 reads the missing file as `failed`). Commands that already")
ed('F-01',"the output directory, so the report path is known before dispatch (WC-4);","the output directory or file its row names, so the report path is known before dispatch (WC-4; workflow's is read from its run result, because its package `<id>` is made at run time);")
ed('F-02',"the exact command line including `--unattended` and every flag section 3 lists as required;","the exact command line including `--unattended` where the command's phase has added it (section 6) and every flag section 3 lists as required;")
ed('F-01','"Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1).',
'"Contract" means the WC-4 file at the path its row names, `<output-dir>/return-contract.yaml` by default.')
ed('F-02',"Phase numbers refer to section 6.\n","Every command in a phase scope that lists `--unattended` (section 6) gains the `## Unattended mode` section (section 2.1); the P1 small fixes to ready commands and the load usage line add none. Phase numbers refer to section 6.\n")
ed('F-01',"| Write the contract for pre-creation STOPs too (WC-4 \"every outcome\") (P1) |","| None: a stop before the package folder exists writes no contract, and WC-5 reads that as `failed` (WC-4) |")
ed('F-01',"adversarial and workflow contract gaps,","the adversarial contract gap,")
ed('F-02',"Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4.\n","Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4. A command accepts `--unattended` only from the phase that resolves all its gates; before then the coordinator briefs it without the flag.\n")
ed('F-02',"The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow |",
"The WC-4 contract in unattended mode, the `--unattended` flag and the `## Unattended mode` section for the eight no-gate commands first listed, with an output flag where a command lacks one; the small fixes to ready commands (no `--unattended`). | analyze, build, business-panel, design, document, explain, index, test; load (usage line only); fixes to adversarial, cleanup-audit, index-repo |")
ed('F-02',"the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one |",
"the test asserts that each of the eight P1 commands that take `--unattended` (analyze, build, business-panel, design, document, explain, index, test) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no other command and no section-4 command has one yet |")
ed('F-02',"7.2 live check on each P1 command with `--unattended --output <dir>` |","7.2 live check on each of those eight commands with `--unattended` and the output flag its row adds |")
ed('F-01',"`grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |",
"`grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` | adversarial names one fixed path |")
ed('F-02',"The coordinator writes it into every worker's command line; a person never types it.","The coordinator writes it into the command line of every worker whose command accepts it (section 6); a person never types it.")
ed('F-03',"| steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record",
"| steps 1-3 and 5-7 pass, read for P0 as follows: step 1's brief is the command line as written, with no `--unattended` (no command accepts it before P1); step 3's `--outcome` is `succeeded` when the command's existing report file was written and `failed` otherwise, and its report path is that file (the WC-4 and WC-5 contract rules start at P1); step 4 is `test -s` on that file, without the `status` check. Record")
open(P,'w',encoding='utf-8').write(t)
after=len(t.encode())
res={}
for fid,o,n in E:
    ob,nb=o.encode(),n.encode()
    sm=difflib.SequenceMatcher(None,ob,nb,autojunk=False)
    ins=dele=0
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag in('replace','delete'): dele+=i2-i1
        if tag in('replace','insert'): ins+=j2-j1
    r=res.setdefault(fid,[0,0,0]); r[0]+=ins; r[1]+=dele; r[2]+=1
print(before,after,res)
