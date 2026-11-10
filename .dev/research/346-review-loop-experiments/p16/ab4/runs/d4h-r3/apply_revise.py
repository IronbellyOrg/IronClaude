import sys, hashlib
path = sys.argv[1]
data = open(path, "rb").read()
before_size = len(data)
before_sha = hashlib.sha256(data).hexdigest()
text = data.decode("utf-8")

edits = []

# M2: WC-4 file-valued output rule
edits.append(("M2",
"""where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`).""",
"""where `<output-dir>` is the directory named by the command's contract path (M2, section 3): the directory the coordinator passed as `--output-dir`, or, when the output flag is a file, the directory holding that file."""))

# M9 + M2: per-command contract paths after section 3 intro
edits.append(("M9",
"""Phase numbers refer to section 6.""",
"""Phase numbers refer to section 6. **Contract path per command (M9; M2 for the output flags):** adversarial writes `<output>/adversarial/return-contract.yaml`. brainstorm, reflect, release-split and auggie-review write `<output-dir>/return-contract.yaml`. cleanup-audit and index-repo gain `--output-dir <dir>` in P1, and research gains it in P2 (M2); each writes `<dir>/return-contract.yaml`. tdd and init-lite, whose `--output` is a file, write a sibling `return-contract.yaml` in that file's directory (M2). spec-panel writes `<report-dir>/return-contract.yaml` with `--report-dir`, the unattended report directory (M9; the evidence for `--report-dir` is outside this workspace, so UNVERIFIED here). workflow writes `.dev/tasks/to-do/<id>/return-contract.yaml`; the brief passes `<id>` as a new `--package-id` flag in P1, so the path is known before dispatch, and the command creates that directory for a pre-creation STOP (M2, M9). troubleshoot writes `return-contract.yaml` beside `REPORT.md` (M9). load has no contract, because it is not dispatched as its own Task (section 3.2 row, M9)."""))

# M8: section 3.1 scope sentence
edits.append(("M8",
"""The only command changes are the small fixes in the last column.""",
"""Each command in this table gains the `--unattended` flag and the `## Unattended mode` section (M8), a no-op where the command has no gate. Beyond that, the only changes are the small fixes in the last column; brainstorm and init-lite have no fix, so their change is the flag and section alone."""))

# M8: P1 phase scope
edits.append(("M8",
"""index-repo, workflow | No person gate""",
"""index-repo, workflow; brainstorm and init-lite (flag and section only, M8) | No person gate"""))

# M9: research output flag; spec-panel report dir
edits.append(("M2",
"""| fresh file | none |""",
"""| fresh file | add `--output-dir` (M2) |"""))
edits.append(("M9",
"""| add `--output`; contract |""",
"""| add `--report-dir` (M9); contract |"""))

# M4: step 6 pass condition
edits.append(("M4",
"""6. `git status --short`. **Pass:** only files under the brief's output directory (and the command's documented artifacts) appear.""",
"""6. `git status --short`. **Pass:** only files under the brief's output directory, the command's documented artifacts, and product files the brief authorizes the command to edit appear (M4). Cleanup, improve, task, document (inline mode), implement and cli-portify edit product files on their happy path, per their section 3 rows."""))

# M6: AC-0.4 cell
edits.append(("M6",
"""| steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |""",
"""| M6: the P0 briefs omit `--unattended`, which P1 adds, so the command lines above are the P0 lines. Steps 1, 2, 5, 6 and 7 pass as written; step 5 also shows that no Agent-tool call precedes the command. Step 3 passes when `worker_done` arrives and its report path is the command's existing report (`REPORT.md` for troubleshoot; the existing `return-contract.yaml` for workflow and adversarial, section 3.1 "Report today" column). Step 4 is replaced by `test -s <existing report>`; the YAML key check applies only to workflow's existing contract, which has `status` and no `command` key (`INV-B:272`). Record the results in the phase report; a failure here reopens section 1 |"""))

# M10: AC-2.2 cell
edits.append(("M10",
"""Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |""",
"""Gate-trigger run per P2 command: a 7.2 live check with input that hits a gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`). M10: only gates whose section 3 row says blocked (WC-2 (c)) are tested this way: cli-eval, tdd, spec-panel, task, recommend, review-translation, troubleshoot `--depth deep`, release-split `--r1-scope custom`, cli-portify. Gates resolved by a default or a flag (WC-2 (a) or (b)), as in cleanup, improve, reflect, research, tasklist and auggie-review, are run the same way but expect the success outcome of AC-2.3 | Blocked gates: `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`. Default or flag gates: `--outcome succeeded` with no `blocked_question`. In both cases step 2 never shows `agentWait` |"""))

# M11: AC-2.3 cell
edits.append(("M11",
"""| Happy-path run per P2 command with every required flag in the brief | 7.2 passes with `--outcome succeeded` |""",
"""| Happy-path run per P2 command with every required flag in the brief, except cli-portify (M11) | 7.2 passes with `--outcome succeeded`. For cli-portify (M11), its three approval gates always resolve as blocked (section 3.2 row), so the run expects step 3 to show `--outcome failed` at the first gate, with the artifact to review named in the contract; this spec defines no cli-portify happy path |"""))

# M12: section 1.4 gap 1
edits.append(("M12",
"""so it proves the nested route, not the direct route this spec requires.""",
"""so it proves the nested route. Its return contract, cited in E3 as `invocation_method: "skill-direct"`, is partial direct-route evidence for `/sc:adversarial` only (M12); it does not show the rest of the 7.2 check (report, transcript, release). The contract is outside this workspace, so its content is UNVERIFIED here, and no direct-route run of this spec's kind exists."""))

report = {}
for fid, old, new in edits:
    n = text.count(old)
    assert n == 1, (fid, n, old[:60])
    text = text.replace(old, new)
    d = report.setdefault(fid, [0, 0, 0])
    d[0] += len(old.encode("utf-8"))
    d[1] += len(new.encode("utf-8"))
    d[2] += 1

out = text.encode("utf-8")
open(path, "wb").write(out)
print("before_size", before_size, "before_sha256", before_sha)
print("after_size", len(out), "after_sha256", hashlib.sha256(out).hexdigest())
for fid in sorted(report, key=lambda s: int(s[1:])):
    o, n, c = report[fid]
    print(fid, "edits", c, "deleted_bytes", o, "added_bytes", n, "net", n - o)
