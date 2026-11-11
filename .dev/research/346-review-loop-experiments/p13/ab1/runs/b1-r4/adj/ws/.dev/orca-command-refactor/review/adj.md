# Adjudication of findings X1-X16

Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (cited as `SPEC:N`). Inventories: `inventory/commands-a.md` (`INV-A:N`), `inventory/commands-b.md` (`INV-B:N`).

Test applied to each finding: "An implementer who follows the stated text as written builds X, and X is wrong because Y." A finding is confirmed only if that sentence holds with no further assumption.

Limits: only the spec, the README and the three inventories exist in this sandbox. Every `cmd/`, `sk/`, `CLAUDE.md` and `CAPS`-quoted source line is UNVERIFIED here; no finding was confirmed on the strength of such a line.

Result: 2 confirmed (X12, X15), 14 rejected, 0 unsure.

## Confirmed

### X12 - confirmed
Sentence: An implementer who follows WC-4 as written builds, for `/sc:tdd` and `/sc:init-lite`, a contract at `<the --output value>/return-contract.yaml`, and that is wrong because for those two commands the `--output` value is a file, so the path lies under a regular file and cannot be created.
- WC-4 defines `<output-dir>` as "the directory the coordinator passed (`--output` / `--output-dir`)" (`SPEC:62`).
- The tdd row requires `--output <file>` and reports "the TDD at `--output`" (`SPEC:90`); the init-lite row requires `--output <file>` (`SPEC:87`). `INV-B:47` and `INV-A:55` agree that `--output` is the deliverable file for both.
- AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and requires a contract with `status: blocked` (`SPEC:200`); section 2.3 requires the report path to be known before dispatch (`SPEC:73`).
- No text says where the contract goes when `--output` is a file. Any fix (parent directory, a sibling name, a separate flag) is a choice the spec does not make, and the command and the coordinator must make the same one.

### X15 - confirmed
Sentence: An implementer who follows AC-C5 and AC-0.3 as written builds a check that pipes `git diff -U0` through `grep -E '^-[^-]'`, and that is wrong because a deleted line whose own text starts with `-` appears in the diff as `--...`, which the pattern does not match, so the deletion passes as "additive".
- Text: `SPEC:176` (AC-C5) and `SPEC:193` (AC-0.3).
- Checked in the sandbox: feeding a diff with the removed lines `-- bullet`, `----` and `-plain` through `grep -E '^-[^-]'` printed only `-plain`.
- Markdown bullets (`- item`), flag lines (`--flag`) and `---` rules all start with a dash, and they are common in command files, so the check cannot enforce SA-4 (`SPEC:149`) or the "no existing routing row changed" condition as stated.

## Rejected

### X1 - rejected
The sentence does not hold: the implementer builds the P0 smoke runs first (`SPEC:158`, AC-0.4 at `SPEC:194`), and section 1.4 states the missing end-to-end evidence itself (`SPEC:43`). The tdd stall is bounded by the required precise prompt (`SPEC:90`) and converted to blocked in P2. This is a wording overstatement in `SPEC:79`, not a wrong build.

### X2 - rejected
The `--output` on troubleshoot appears only in the illustrative example of D1 (`SPEC:228`); nothing is built from it. P1 adds "output flags for commands that lack one" (`SPEC:159`), and `INV-B` records a default output folder for troubleshoot (`.dev/troubleshoot/<slug>-<timestamp>/`), which does not show the flag is absent. Whether `cmd/troubleshoot.md` already has `--output` is UNVERIFIED here.

### X3 - rejected
E2 (`SPEC:22`) is a supporting argument for the decision. No requirement, phase or check is derived from tool parity, so no build step is wrong because of it.

### X4 - rejected
The finding says the row "may be stale"; it offers no line. `cmd/analyze.md` is not in the sandbox, and `INV-A:37` supports the row ("no path or filename is defined"). The sentence needs the assumption that the command file differs from the inventory.

### X5 - rejected
The spec does decide it: unattended `--remediate` follows reflect's existing headless auto-accept rule (`SPEC:88`, `SPEC:122`, SA-6 at `SPEC:151`). D2's rationale (`SPEC:236`) is about the `/sc:implement` Ruling rule only. Calling the reuse wrong requires the further assumption that accepting a remediation hand-off equals an agent approving its own work. Note: `INV-B:46` recommended dropping `--remediate` in Stage 10.5 instead; that is a design difference, not a blocking defect.

### X6 - rejected
AC-C1 (`SPEC:172`) fails on P0's new core text only if that text contains a literal `orca orchestration|worktree|terminal|agent` string, which the spec does not require; the text can name the caller's question channel without it. The missing `status/open/skills` subcommands make the check narrower than SA-2, but an implementer following SA-2 (`SPEC:147`) still builds no Orca call.

### X7 - rejected
The git row (`SPEC:133`) leaves `/sc:git` coordinator-only whichever evidence is cited. The quality of one citation changes nothing that is built.

### X8 - rejected
Section 1.1 (`SPEC:16`) is a summary. The implementer builds from section 3 and SA-4 (`SPEC:149`), which list the edits and the named defect fixes. A reader underestimating the work is not a wrong build.

### X9 - rejected
"Cannot misfire on a person" (`SPEC:228`) is a rationale sentence for D1. A misfire on quoted text needs an assumption about how the flag is parsed, which the spec does not state.

### X10 - rejected
P1's scope gives the contract and the `--unattended` flag to "every command in sections 3.1 and 3.2" (`SPEC:159`), and AC-1.1 requires every such command to have a `## Unattended mode` section naming `return-contract.yaml` in P1 (`SPEC:195`). So troubleshoot, tdd and release-split have a contract before AC-2.3 runs. The finding holds only if P1's "Commands" column is read as overriding its scope column and AC-1.1.

### X11 - rejected
The spec tells the implementer to point to the installed contract path (`SPEC:52`), and AC-1.1 asserts the section names `~/.claude/WORKER-CONTRACT.md` (`SPEC:195`). A missing negative check does not make an implementer who follows the text write a `src/superclaude/` path.

### X13 - rejected
WC-9 (`SPEC:67`) covers outward actions by design. Local edits are limited per row: cleanup and improve apply only items allowed without approval (`SPEC:103`, `SPEC:110`), and reflect's brief passes `--no-promote` when the coordinator owns moves (`SPEC:88`). The finding names no stated text that produces a wrong build.

### X14 - rejected
Writing the brief template is a P0 deliverable (`SPEC:158`), and section 2.3 lists what each brief must state (`SPEC:73`). Detail left to the deliverable is not a contradiction in the spec.

### X16 - rejected
The spec states the dependency itself: pr-submit "stays a worker candidate only if the user accepts open decision D3" (`SPEC:139`), P4 waits for D2-D4 (`SPEC:154`), and AC-4.3 is conditional on D3 (`SPEC:210`). The 27 count is a labelling matter and changes no build step.

```adj-v1
{"x": "X1", "verdict": "rejected", "reason": "Section 1.4 states the evidence gap itself and P0/AC-0.4 smoke-tests before anything is built, so the ready-today wording produces no wrong build."}
{"x": "X2", "verdict": "rejected", "reason": "The --output on troubleshoot is only in D1's illustrative example, P1 adds output flags where missing, and the inventory does not show the flag is absent."}
{"x": "X3", "verdict": "rejected", "reason": "E2 is a supporting argument from which no requirement, phase or check is derived, so nothing built is wrong because of it."}
{"x": "X4", "verdict": "rejected", "reason": "The finding only says the row may be stale, the command file is not available to check, and INV-A:37 supports the row."}
{"x": "X5", "verdict": "rejected", "reason": "The spec does decide it by reusing reflect's existing headless auto-accept rule, and D2's rationale covers only the implement Ruling rule, so the claim needs a further assumption."}
{"x": "X6", "verdict": "rejected", "reason": "AC-C1 fails on the new core text only if that text contains the literal pattern, which the spec does not require, and the uncovered subcommands narrow the check without causing a wrong build."}
{"x": "X7", "verdict": "rejected", "reason": "The git row keeps /sc:git coordinator-only whichever evidence is cited, so the citation quality changes nothing built."}
{"x": "X8", "verdict": "rejected", "reason": "Section 1.1 is a summary and the implementer builds from section 3 and SA-4, which list the edits and named defect fixes."}
{"x": "X9", "verdict": "rejected", "reason": "The cannot-misfire sentence is D1 rationale and a quoted-text misfire needs an unstated assumption about how the flag is parsed."}
{"x": "X10", "verdict": "rejected", "reason": "P1's scope and AC-1.1 give every section 3.1 and 3.2 command the unattended section and contract in P1, so those three commands have a contract before AC-2.3."}
{"x": "X11", "verdict": "rejected", "reason": "The spec tells the implementer to point to the installed contract path and AC-1.1 asserts it, so a missing negative check does not make a follower write a src/superclaude path."}
{"x": "X12", "verdict": "confirmed", "reason": "WC-4 puts the contract under the directory passed as --output, but tdd and init-lite take --output as a file, so the stated path cannot exist and AC-2.2's tdd contract check cannot pass."}
{"x": "X13", "verdict": "rejected", "reason": "WC-9 covers outward actions by design and local edits are limited in the cleanup, improve and reflect rows, so no stated text yields a wrong build."}
{"x": "X14", "verdict": "rejected", "reason": "The brief template is a P0 deliverable whose required contents section 2.3 lists, so its unwritten detail is not a spec defect."}
{"x": "X15", "verdict": "confirmed", "reason": "The grep '^-[^-]' does not match removed lines that themselves start with a dash (shown as '--...'), verified by running it, so deleted bullets and rules pass AC-C5 and AC-0.3 as additive."}
{"x": "X16", "verdict": "rejected", "reason": "The spec states that pr-submit is a worker candidate only under D3 and makes P4 and AC-4.3 conditional on it, so the count is a labelling matter."}
```
