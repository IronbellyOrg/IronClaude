# Verification 3: N2 and N4

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
sha256: `1a2d2f425ac57ef3f2392d0bfdf09996e8bf26606b0e7b94ee731ab5d177867d` (293 lines)

Citations to `INV-A`, `INV-B`, `CAPS` and `sk/` or `cmd/` files point outside this workspace and could not be checked. They are UNVERIFIED here and no decision below relies on them.

| id | found text (candidate line) | exists | outcome follows | verdict | reason |
|---|---|---|---|---|---|
| N2 | spec:62, WC-4: "`<parent>/<stem>.return-contract.yaml`, where `<parent>` is that file's parent directory and `<stem>` is its file name without its extension, so two runs whose files share a parent directory write two contracts [M1, N2]." Spec:87 (init-lite) and spec:90 (tdd) both have `--output <file>`. WC-11 at spec:69: "Two workers in one worktree must never write the same file." | yes | yes | confirm | The rule gives `.dev/superclaude/a.md` and `.dev/superclaude/a.txt` the same contract path, `.dev/superclaude/a.return-contract.yaml`, because both share parent and stem. The sentence claiming two contracts is false for this pair, so the text contradicts itself. The second run overwrites the first, so the first report path is lost and the coordinator reads a contract for the wrong worker. No exception to the rule appears in spec:62. WC-11 is also breached by the same pair. |
| N4 | spec:204, AC-1.2: "7.2 live check on each P1 command with `--unattended` and the one output flag section 3 names for it (`--output-dir <dir>` for cleanup-audit, index-repo and workflow; `--output <dir>` for the others)". Spec:112 (load row): "none: use it as a step inside another worker's brief, not as its own Task"; output-flag column "none (see note)". Spec:159 P1 list includes "load (usage line only)". Spec:187 "For each command under test"; spec:188 step 1 "`ORCA orchestration task-create --spec ...`, then `ORCA orchestration worker-start ...`". Spec:191 step 4 "`test -s <contract>`". | yes | yes | confirm | Literal reading: load is in the P1 list, so AC-1.2 applies 7.2 to it. Step 1 creates a Task, which spec:112 forbids for load. Spec:112 names no output flag for load, and the "see note" points to no note: a grep for "note" finds no load note in the candidate. So the `--output <dir>` required by AC-1.2 does not exist for load, and step 4's contract cannot be produced. The criterion cannot pass as written. The "(usage line only)" qualifier could be read as excluding load from the live check, but that reading is an extra assumption, and the literal P1 list does not exclude it. |

Scope notes: N2's premise (two extensions for one stem) is reached only by choice of inputs, as the finding says. I did not regrade either finding.

confirmed: N2, N4
