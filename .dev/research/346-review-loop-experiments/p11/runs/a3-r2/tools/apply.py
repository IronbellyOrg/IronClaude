import difflib
P = "ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md"
s = open(P, encoding="utf-8").read()
before = len(s.encode())
E = []
def e(i, old, new):
    E.append((i, old, new))

# ---- R1-B1 ----
e("R1-B1",
 "Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers",
 "Every changed command also gains the `## Unattended mode` section (section 2.1) in the phase its row names, together with that row's gate resolutions (R1-B1). Phase numbers")
e("R1-B1",
 "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate);",
 "the `--unattended` flag and `## Unattended mode` section on the P1 commands only, each with the resolution its section 3 row gives (R1-B1);")
e("R1-B1",
 "Later phases do not start until the earlier phase's checks in section 7 pass. Phases 1-3",
 "Later phases do not start until the earlier phase's checks in section 7 pass. A command gains `--unattended` only in the phase its section 3 row names, together with its gate resolutions, so no command accepts the flag while it still prompts; the coordinator passes it only to a command whose phase has passed, and never to brainstorm or init-lite, which are unchanged (R1-B1). Phases 1-3")
e("R1-B1",
 "the exact command line including `--unattended` and every flag",
 "the exact command line including `--unattended` where the command's phase has passed (section 6, R1-B1) and every flag")
e("R1-B1",
 "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one |",
 "asserts that every command whose section 3 phase is P1 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no later-phase or section-4 command has one yet; each later phase extends the list to its own commands (R1-B1) |")
e("R1-B1",
 "no pr-submit changes in Phase 4.",
 "no pr-submit section or change, so it drops out of Phase 4 (R1-B1).")

# ---- R1-B2 ----
e("R1-B2",
 "\"Contract\" means the WC-4 file `<output-dir>/return-contract.yaml`.",
 "\"Contract\" means the WC-4 file, at the path WC-4's rule gives (R1-B2).")
e("R1-B2",
 "**One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows",
 "**One report file, at a path one rule fixes, written on every outcome.** In unattended mode the command writes `return-contract.yaml` at one of three places (R1-B2): `<dir>/return-contract.yaml` when the brief passes a directory (`--output` / `--output-dir`); `<file>.return-contract.yaml` beside the file when the flag names a file (tdd, init-lite, and any section 3 row that adds a file path), so parallel workers with different output files never share a contract; or, for the two commands that fix their own place, `<output>/adversarial/return-contract.yaml` (adversarial) and `.dev/tasks/to-do/<id>/return-contract.yaml` (workflow, whose id the command chooses, so the coordinator learns the path from `worker_done --report-path`). It follows")
e("R1-B2",
 "including stops before any other output exists. Commands",
 "including stops before any other output exists, except a workflow stop before its package exists, which has no place to write: it writes no contract and ends `failed` with no report (WC-5, R1-B2). Commands")
e("R1-B2",
 "the output directory, so the report path is known before dispatch (WC-4);",
 "the output directory or file, so the report path follows from WC-4's rule (R1-B2);")
e("R1-B2",
 "| Write the contract for pre-creation STOPs too (WC-4 \"every outcome\") (P1) |",
 "| None (WC-4 fixes its contract place; a stop before the package exists writes none, R1-B2) |")
e("R1-B2",
 "fixes to adversarial, cleanup-audit, index-repo, workflow |",
 "fixes to adversarial, cleanup-audit, index-repo |")
e("R1-B2",
 "adversarial and workflow contract gaps,",
 "adversarial contract gap,")
e("R1-B2",
 " and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |",
 " | adversarial names one fixed path, `<output>/adversarial/return-contract.yaml` (R1-B2) |")
e("R1-B2",
 "| contract naming the generated `claudedocs/research_*.md` path |",
 "| add `--output <dir>`; contract there, naming the generated `claudedocs/research_*.md` path (R1-B2) |")
e("R1-B2",
 "(for example `/sc:tdd \"auth\" --unattended --output <file>` with a bare topic;",
 "(for example `/sc:tdd \"auth\" --unattended --output <file>` with a bare topic, contract at `<file>.return-contract.yaml`;")

rep = {}
for i, old, new in E:
    assert s.count(old) == 1, (i, s.count(old), old[:60])
    s = s.replace(old, new)
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    a = d = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op in ("delete", "replace"):
            d += len(old[i1:i2].encode())
        if op in ("insert", "replace"):
            a += len(new[j1:j2].encode())
    r = rep.setdefault(i, [0, 0, 0])
    r[0] += a; r[1] += d; r[2] += 1
open(P, "w", encoding="utf-8").write(s)
print(before, len(s.encode()), rep)
