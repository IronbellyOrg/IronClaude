review: 2 of 3

# /sc:spec-panel re-review (critique mode, focus requirements,architecture)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` sha256 f33929128f30fe63da2c9835b134305b0ef77d6fc1b02b5c98f2a04864840102
- baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md` sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
- prior: `.dev/orca-command-refactor/review/round1.md` sha256 5e2c61ed07fe804d64a08eefa692b3c192b09d5c66419e772b1336f7d7dee082 (header `review: 1 of 3`, so N = 2)
- reviewer model used: claude-sonnet-5-5 (single reviewer; `superclaude` is not installed in this sandbox, so `superclaude review panel resolve` and `superclaude review merge` were not run)
- baseline note: the baseline hash equals the hash round 1 recorded for its candidate, so the roles are consistent.
- README read first (`.dev/orca-command-refactor/README.md:1-38`). Evidence checkable here: the three files under `inventory/` and the spec itself. Source-tree citations (`sk/...`, `cmd/...`, `EVIDENCE.md`) cannot be checked in this sandbox and are UNVERIFIED unless an inventory line quotes them.
- `--iterations` ignored, Improve step skipped, no revised specification written (Review Loop bullet 4).

## Step 1: evidence block (`diff -w` baseline candidate)

Roles fixed by the brief, not by reading order. Changed lines, verbatim (long table rows are abbreviated with `...` only where the unchanged remainder is identical; the changed clause is quoted in full).

BEFORE (baseline) | AFTER (candidate)

- WC-1 (candidate line 59)
  - BEFORE: `Any such prompt must fall back on its own well inside the readiness limit (default 60 s).`
  - AFTER: `Any such prompt must fall back on its own within 30 s (the readiness limit defaults to 60 s).`
- WC-3 (line 61)
  - BEFORE: `the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag.`
  - AFTER: `the session may instead, after the contract with `status: blocked` is written, ask the coordinator once with the preamble's `ask` command for the value of a flag section 3 lists, wait, then re-invoke the command with that flag (the contract is rewritten). It never relays an answer as a `/sc:implement` Ruling (D2). If no answer comes, it sends `worker_done --outcome failed` with that contract.`
- WC-4 (line 62)
  - BEFORE: `where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). ... `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` ...`
  - AFTER: `... the directory the coordinator passed (`--output-dir`), or the parent directory of the file passed as `--output <file>`; a command whose section 3 row names a different fixed path (adversarial) uses that path. With no output given in the brief the command stops before doing work. For `/sc:workflow` the path holds a generated id, so the coordinator learns it from `worker_done --report-path`, not before dispatch. ... `contract_version` (`1`), `status` (...; an existing contract's own status values are mapped to these) ... and is complete before `worker_done` is sent.`
- WC-5 (line 63): AFTER adds `or its `status` is missing or not one of the four`.
- WC-6 (line 64): AFTER adds `the retry's brief names that directory, so the contract path is known (WC-4)`.
- WC-10 (line 68)
  - BEFORE: `A command step that blocks a single tool call for longer than 5 minutes`
  - AFTER: `A command step that can block a single tool call for longer than 4 minutes`
- WC-12 (line 70): AFTER adds `(an empty result is not that)`.
- Section 2.3 (line 73): AFTER names the "Brief must pass" column and the 3.2 gate-resolution cell, adds the permission-mode sentence, `opens the report file before it starts any dependent Task (Orca records `partial` as completed, WC-5)`, and `It retries a blocked Task only with a brief that answers the `blocked_question`.`
- Section 3.1 intro (line 79): `until the phase in its row adds the contract` replaces `until Phase 1 adds the contract`.
- init-lite row (line 87): `Fresh `--output` file per attempt (WC-6)` and `None (P1)` replace `Re-run overwrites its marked report` and `None`.
- cli-portify row (line 105): `brief rule, no edit: dispatch only inside an IronClaude checkout (hardcoded template path)` replaces the bare "dispatch only ..." text.
- P1 and P2 rows of section 6 (lines 159-160): P1 now lists commands explicitly and limits `--unattended` to them; P2 adds `for release-split, tdd and troubleshoot the section also adds the WC-4 contract pointing at their named report file`.
- AC-C1 (line 172) now points to a code block (lines 178-181) with plain `|` alternation, extra verbs (`status|open|skills`) and exclusions for `WORKER-CONTRACT.md` and `HOW-WE-WORK.md`.
- AC-C5 (line 176) and AC-0.3 (line 198): `grep -E '^-[^-]'` replaced by `grep -E '^-' | grep -v '^--- a/'`.
- 7.2 step 3 (line 187): adds `(in P0, the command's existing report file)`. Step 5 (line 189): adds the Agent-tool search.
- AC-1.1 (line 200): list now bounded to the P1 row, excludes `/sc:load`, later phases extend it.

Self-check (Process step "grep -nF"): every `>` line, stripped of its prefix, was found exactly in the candidate (`grep -qxF`), and every `<` line in the baseline. No role swap. Result: none missing.

## Re-check of prior blocking findings (round 1: L1, L2, L4, L5)

| id | status | basis |
|---|---|---|
| L1 | open | Most of its sub-claims are resolved (list below). One residual is still a stated check that cannot pass: the P0 live check on `/sc:troubleshoot` (finding L1 below). Per the rule that an unmatched or deferred item counts as open, L1 stays open. |
| L2 | resolved | AC-C5 (line 176) and AC-0.3 (line 198) now use `grep -E '^-' \| grep -v '^--- a/'`. I ran the same pipeline on a scratch repo: deleting `- b` printed `-- b` and deleting `---` printed `----`. A deleted dash-led line is caught. |
| L4 | resolved | AC-C1 (lines 178-181) uses plain `|`. I ran it on a scratch tree: it matched `orca-ide orchestration` in a command file and `orca open` in `core/CLAUDE.md`, and skipped `ccsession-tag/`, `WORKER-CONTRACT.md` and `HOW-WE-WORK.md`. The scope problem (contract file and routing guide that SA-2/P0 allow) and the missing verbs (`status`, `open`, `skills`) are fixed. |
| L5 | resolved | P2 row (line 160) now adds the WC-4 contract for release-split, tdd and troubleshoot, and the 3.1 intro (line 79) points each command to the phase in its own row. AC-2.3 no longer requires a contract the plan never builds. |

L1 sub-claims, by group, against the AFTER text:

- Resolved: WC-3 Ruling relay (WC-3 line 61, now forbids it, consistent with D2 line 232 text); order of blocked contract, `ask` and `worker_done` (WC-3); `--output <file>` path (WC-4 parent directory); workflow generated id (WC-4); contract version and status mapping (WC-4, content of the mapping is a Medium below); unknown or missing status (WC-5); partial and FAIL-verdict settling as succeeded (2.3: coordinator opens the report before dependents); retry directory (WC-6); permission-mode prompt (2.3); 4-5 minute gap (WC-10 with the 4-minute trigger; AC-4.3 line 211 is consistent); empty `check` read as fenced (WC-12, matches `CAPS:67`); readiness fallback quantified at 30 s (WC-1, matches `CAPS:44-45` and the cited `EVIDENCE.md:45,56`, UNVERIFIED here); AC-1.1 against `/sc:load` and against P2-P4 commands (AC-1.1 line 200); `--unattended` accepted before gates convert (P1 row line 159); brainstorm and init-lite in no phase (both now in the P1 row); hardcoded template path as an unscheduled change (cli-portify row line 105 now a brief rule); AC-0.4 step 5 versus Agent-tool wrapper (line 189); contract complete before `worker_done` (WC-4); required flags absent from the 3.2 rows (2.3 now names the 3.2 gate-resolution cell).
- Still open: the P0 check below.

## Findings on lines changed against the baseline

Blocking:

### L1 (residual of round-1 L1.t3-2 F1) — origin=changed, MAJOR, blocking, category unpassable-check

An implementer who follows AC-0.4 and 7.2 as written runs the P0 live check on `/sc:troubleshoot` (candidate line 199) and applies step 4 to "the command's existing report file", which for troubleshoot is `REPORT.md` (candidate line 91; `INV-B:242`, "`report_path` (REPORT.md) ... `return-contract.yaml` only when `--caller task-unified`"). Step 4 (candidate line 188) is `test -s <contract>` plus a `yaml.safe_load` that asserts `d['status'] in {'succeeded','partial','failed','blocked'}` and `d['command']`; its pass condition is "both exit 0". A markdown report has no such keys, so the second command fails (a TypeError or an assertion error). Step 3 (line 187) likewise compares `--outcome` with "the contract's `status`", and there is no contract in P0. The edit swapped the path in step 3 but left the assertion in step 4 unchanged. AC-0.4 then fails for troubleshoot, and the same line says "a failure here reopens section 1", so a wording defect in the check reopens the architecture decision. The workflow run has the same exposure if its contract's own status values differ from the four (`INV-B:272` names `status` but no vocabulary; UNVERIFIED), because the status mapping of WC-4 only arrives in P1.

Fix scope for the reviser: make step 4 and the status comparison in step 3 apply to the existing report file in P0 as a presence check only (for example `test -s`), or state which P0 steps are skipped. Nothing else is named by this finding.

Medium and minor (warnings; none fails this review; follow-up candidates):

- R2-1 (MAJOR label, Medium grade, origin=changed): WC-4's parent-directory rule makes parallel workers collide. Two workers with `--output docs/a.md` and `docs/b.md` both write `docs/return-contract.yaml`, which WC-11 (line 69, "Two workers in one worktree must never write the same file") forbids, and the retry of init-lite or tdd into the same parent overwrites the first attempt's contract despite WC-6. Medium because it needs the coordinator to pick a shared directory, which 2.3 never forbids; a requirement is missing, not a stated text that does harm.
- R2-2 (MAJOR label, Medium, origin=changed): "With no output given in the brief the command stops before doing work" (line 62) sits against 3.1 rows whose brief passes no output and whose rows add no output flag: cleanup-audit (fixed `.claude-audit/` dir, `INV-A:42`), index-repo (`PROJECT_INDEX.md`, location "implied", `INV-A:53`), troubleshoot (default `.dev/troubleshoot/<slug>-<timestamp>/`, `INV-B:242`). Also the same sentence says the contract is written on "stops before any other output exists", yet a stop with no output directory has nowhere to write it; WC-5 (no report means failed) covers the outcome. D1's example passing `--output` to troubleshoot is unchanged (round-1 L7).
- R2-3 (MAJOR label, Medium, origin=changed): line 76 says "Every changed command also gains the `## Unattended mode` section" and 2.1 line 52 says "Each changed command adds a short ... section", while `/sc:load` is a 3.2 row that gets none (P1 row, load decision in the Decisions table) and AC-1.1 asserts it has none. The specific rows win, so Medium.
- R2-4 (MAJOR label, Medium, origin=changed): AC-C5 (line 176) and AC-0.3 (line 198) keep `\|` inside table cells. Copied raw from the file, `git diff -U0 ... -- <file> \| grep ...` passes `|` and `grep` to git as pathspecs and prints nothing, so the additive-edit check passes falsely. This is the same hazard round 1 fixed for AC-C1 only. Medium: it needs the raw-copy assumption, and rendered Markdown shows a plain `|`.
- R2-5 (MAJOR label, Medium, origin=changed): 2.3 now says the brief carries the 3.2 gate-resolution flags, but P0 (line 158) still limits the shared brief template to "the section 3.1 flags", and the five worker-session rules (WC-3, WC-5, WC-7, WC-10, WC-12) still have no stated carrier beyond the contract file (round-1 L1.t3-2 M12). Also the P0 smoke commands in AC-0.4 (line 199) omit `--unattended`, while 2.3 requires it in every brief and no ready command accepts it before P1/P2.
- R2-6 (MINOR, origin=changed): WC-4 says an existing contract's status values "are mapped to these" without giving the mapping, and the P1 workflow row (line 92, unchanged) writes a contract for "pre-creation STOPs" where no `<id>` directory exists yet, while WC-6 says a retry's brief names the fresh directory (workflow's id is generated). Neither names a location.
- R2-7 (MINOR, origin=unchanged): items from round 1 that stay as notes, not re-graded: L3, L6-L16 (`round1.md:317-328`), and "no fallback when the installed contract file is missing" (`round1.md:236`). None quotes a changed line, so none is blocking. UNVERIFIED: whether `src/superclaude/core/` already holds Orca text that would fail AC-C1 on day one (the spec's own baseline claim, E5, cites a grep I cannot rerun here).

## Inherited text

`origin=unchanged` findings above are notes and cite the changed line they depend on only where R2-2 and R2-5 do.

## Coverage

Covered: all diff hunks (evidence block), the four prior blocking ids, every WC row and sections 2.3, 3.1, 3.2 (phase column against the P1-P4 rows, all 43 commands counted: P1 15 entries incl. load, P2 15, P3 4, P4 3 = 37 plus 6 coordinator-only), 6, 7.1-7.3 and the Decisions table. Grep and diff runs: the diff itself, the self-check, the AC-C1 and AC-C5 pipelines on scratch trees (deleted afterwards). Not covered: the live source tree and `EVIDENCE.md` (outside the sandbox).

## Findings block

```findings-v1
{"id": "L1", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "step 4 uses the command's existing report file, since the contract arrives in P1", "anchor2": "assert d['status'] in {'succeeded','partial','failed','blocked'}", "refs": ["AC-0.4", "7.2"], "claim": "P0 step 4 still asserts a YAML status on troubleshoot's markdown REPORT.md, so AC-0.4 cannot pass and wrongly reopens section 1."}
{"id": "R2-1", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "or the parent directory of the file passed as `--output <file>`", "anchor2": "Two workers in one worktree must never write the same file", "refs": ["WC-4", "WC-11", "WC-6"], "claim": "Two workers with output files in one directory share one return-contract.yaml."}
{"id": "R2-2", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "With no output given in the brief the command stops before doing work", "refs": ["WC-4", "3.1"], "claim": "Ready commands with no output flag (cleanup-audit, index-repo, troubleshoot) cannot satisfy the new stop rule, and a stop with no directory cannot write its contract."}
{"id": "R2-3", "severity": "MINOR", "blocking": false, "category": "contradiction", "anchor": "Every changed command also gains the `## Unattended mode` section", "anchor2": "load (usage line only, no section)", "refs": ["3", "AC-1.1", "6"], "claim": "General text gives /sc:load a section that the P1 row and AC-1.1 say it must not have."}
{"id": "R2-4", "severity": "MAJOR", "blocking": false, "category": "unpassable-check", "anchor": "prints nothing: edits are additive (a deleted line that starts with a dash still shows)", "refs": ["AC-C5", "AC-0.3"], "claim": "Copied raw, the escaped pipes make git read grep as a pathspec and the additive-edit check passes falsely."}
{"id": "R2-5", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "a coordinator brief template listing the section 3.1 flags", "anchor2": "the exact command line including `--unattended`", "refs": ["P0", "2.3", "AC-0.4"], "claim": "The P0 template covers only 3.1 flags, and the P0 smoke commands omit the --unattended flag that 2.3 requires."}
{"id": "R2-6", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "an existing contract's own status values are mapped to these", "anchor2": "Write the contract for pre-creation STOPs too", "refs": ["WC-4", "WC-6", "3.1"], "claim": "The status mapping and the pre-creation workflow contract location are unspecified."}
{"prior": "L1", "status": "open"}
{"prior": "L2", "status": "resolved"}
{"prior": "L4", "status": "resolved"}
{"prior": "L5", "status": "resolved"}
```

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names (here AC-0.4 and the 7.2 step 3 and step 4 wording for P0); add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave R2-1 to R2-7 alone: they are Medium or minor, not blocking, and a brief cannot make them so.

verdict: FAIL
