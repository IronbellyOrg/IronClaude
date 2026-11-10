import sys, collections
SPEC = "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r2/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md"

EDITS = [
# M1: WC-4 header and path rule
("M1", r'''| **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows''',
 r'''| **One report file, written on every outcome, at a path the coordinator can read.** In unattended mode the command writes its contract at the path section 3 gives for it. Where the command's output option names a directory, that path is `<output-dir>/return-contract.yaml`, with `<output-dir>` the directory the coordinator passed (`--output` / `--output-dir`); adversarial's is `<output>/adversarial/return-contract.yaml` (`INV-A:60`). Where the output option names a file (tdd, init-lite), the contract sits beside that file. Where the path is generated at run time (workflow, research), the worker passes it in `worker_done --report-path` and the coordinator reads it then (M1). It follows'''),
# M2: WC-4 exception for workflow pre-creation STOPs
("M2", r'''including stops before any other output exists. Commands that already write a contract''',
 r'''including stops before any other output exists, except workflow's pre-creation STOPs (M2; section 3, `INV-B:272`). Commands that already write a contract'''),
# M11: WC-3 exclusion for Ruling, outward action, safety boundary
("M11", r'''then re-invoke or resume the command with the answer as a flag. On an `ask` timeout''',
 r'''then re-invoke or resume the command with the answer as a flag, except that a gate guarding a Ruling, an outward action or a safety boundary resolves as blocked and no `ask` answer supplies it (M11; D2, D4, WC-9). On an `ask` timeout'''),
# M7: WC-9 coordinator answer never supplies outward flag
("M7", r'''It turns on only through the command's own explicit flag written in the brief.''',
 r'''It turns on only through the command's own explicit flag written in the brief (D4), and a coordinator's `ask` answer never supplies that flag (M7; WC-3).'''),
# M9: WC-5 unreadable or unknown-status contract is failed
("M9", r'''`--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise,''',
 r'''`--outcome failed` when the report says `failed` or `blocked`, when no report exists, or when the report is empty, unparseable or has a status outside `succeeded`, `partial`, `failed`, `blocked` (M9); `--outcome succeeded` otherwise,'''),
# M12: section 2.3 brief omits --unattended in P0
("M12", r'''the exact command line including `--unattended` and every flag section 3 lists as required''',
 r'''the exact command line, including `--unattended` from P1 on (P0 runs omit it, AC-0.4 (M12)), and every flag section 3 lists as required'''),
# M1: section 2.3 report path fixed only where WC-4 gives one
("M1", r'''the output directory, so the report path is known before dispatch (WC-4)''',
 r'''the output directory or file, so the report path is known before dispatch where WC-4 gives a fixed path (M1)'''),
# M13: one fixed-path audit/index Task per worktree at a time
("M13", r'''the worktree placement (`CAPS:115`). After `worker_done`''',
 r'''the worktree placement (`CAPS:115`). The coordinator dispatches at most one cleanup-audit or index-repo Task per worktree at a time, because their output paths are fixed (M13; WC-11). After `worker_done`'''),
# M1: section 3 definition of "Contract"
("M1", r'''"Contract" means the WC-4 file `<output-dir>/return-contract.yaml`.''',
 r'''"Contract" means the WC-4 file at the path WC-4 gives for the command (M1).'''),
# M1: tdd row, contract beside --output file
("M1", r'''lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`''',
 r'''lines resolve as blocked (P2); the contract sits beside the `--output` file (M1) | `sk/tdd/SKILL.md:48,52-61,190`'''),
# M1: init-lite row
("M1", r'''Re-run overwrites its marked report | None |''',
 r'''Re-run overwrites its marked report | The contract sits beside the `--output` file (M1; P1) |'''),
# M1: P1 scope adds init-lite
("M1", r'''fixes to adversarial, cleanup-audit, index-repo, workflow |''',
 r'''fixes to adversarial, cleanup-audit, index-repo, workflow, init-lite (M1) |'''),
# M1: research row
("M1", r'''contract naming the generated `claudedocs/research_*.md` path''',
 r'''contract beside the generated `claudedocs/research_*.md`, its path passed in `worker_done --report-path` (M1)'''),
# M2: workflow row, no contract for pre-creation STOPs
("M2", r'''Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1)''',
 r'''No contract for pre-creation STOPs, which have no package directory yet: the worker reports them as `worker_done --outcome failed` with the STOP in the body (M2; WC-5, `INV-B:272`) (P1)'''),
# M3: P1 refuses --unattended where an outward default stays on
("M3", r'''the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate);''',
 r'''the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate), except that auggie-review, task, pr-submit and post-release refuse it with an error until their P2 or P4 change lands, because each has an outward default that WC-9 requires off (M3; `INV-A:38`, `INV-B:94`);'''),
# M12: AC-0.4 P0 runs use no --unattended
("M12", r'''(no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass;''',
 r'''(no Agent-tool wrapper, verified in the step-5 transcript), with the stated flags only and no `--unattended`, since P0 adds no such flag (M12) | steps 1, 2 and 5-7 pass;'''),
# M6: AC-0.4 step 3 and step 4 use the existing report
("M6", r'''step 4 uses the command's existing report file, since the contract arrives in P1.''',
 r'''step 3 checks `--outcome` against the existing report, and its path is that report, not the WC-4 contract, since the contract arrives in P1 (M6). Step 4 is replaced (M6): troubleshoot's `REPORT.md` (`INV-B:49`) must exist and be non-empty, and workflow's and adversarial's existing `return-contract.yaml` must be non-empty and parse as YAML. The four-value `status` and `command` assertions move to AC-1.2.'''),
# M6: AC-1.2 applies the status/command assertions
("M6", r'''with `--unattended --output <dir>` | all steps pass |''',
 r'''with `--unattended --output <dir>` | all steps pass, and step 4 applies the four-value `status` and `command` assertions (M6) |'''),
# M2: AC-1.4 workflow statement
("M2", r'''workflow states the contract is written for pre-creation STOPs''',
 r'''workflow states that pre-creation STOPs write no contract (M2)'''),
# M8: AC-C1 pattern in plain form with positive control
("M8", r'''| AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |''',
 r'''| AC-C1 | Run the grep in the block below, which sets the pattern out in plain form because a table cell cannot hold a plain `|`. | The first command prints nothing (SA-2, WC-8). The positive control prints its planted line, which shows the pattern matches (M8). |

```bash
grep -rnE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core | grep -v '^src/superclaude/skills/ccsession-tag/'
# positive control (M8): must print one line
printf 'orca orchestration check --json\n' | grep -E '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b'
```'''),
# M13: cleanup-audit row
("M13", r'''output dir is fixed, so one audit per worktree at a time (WC-11) (P1)''',
 r'''output dir is fixed, so the coordinator runs one audit per worktree at a time (section 2.3, M13) (P1)'''),
# M13: index-repo row, location UNVERIFIED and serialized
("M13", r'''`PROJECT_INDEX.md` (location implied)''',
 r'''`PROJECT_INDEX.md` (location UNVERIFIED, `INV-A:53`; fixed path, so section 2.3 serializes its dispatches, M13)'''),
# M13: new check AC-1.5
("M13", r'''| P2 | AC-2.1 |''',
 r'''| P1 | AC-1.5 | Dispatch two cleanup-audit Tasks into one worktree; the second is dispatched only after the first `worker_done` (check the dispatch log and `worker-list --run <run_id>`) | the second dispatch comes only after the first `worker_done` (M13; section 2.3) |
| P2 | AC-2.1 |'''),
]

text = open(SPEC, encoding="utf-8").read()
before_bytes = len(text.encode("utf-8"))
acc = collections.OrderedDict()
for ident, old, new in EDITS:
    n = text.count(old)
    if n != 1:
        sys.exit(f"ABORT {ident}: match count {n} for: {old[:70]!r}")
    text = text.replace(old, new, 1)
    a = acc.setdefault(ident, [0, 0, 0])
    a[0] += len(new.encode("utf-8"))
    a[1] += len(old.encode("utf-8"))
    a[2] += 1
after_bytes = len(text.encode("utf-8"))
open(SPEC, "w", encoding="utf-8", newline="").write(text)
print(f"before_bytes={before_bytes} after_bytes={after_bytes} delta={after_bytes-before_bytes}")
for k, (add, dele, cnt) in acc.items():
    print(f"{k}: edits={cnt} added={add} deleted={dele} net={add-dele}")
print("lines:", text.count("\n"))
