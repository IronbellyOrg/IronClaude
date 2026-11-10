# Revise 1: spec revision for the confirmed blocking findings

Prompt: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:60-62` (sandbox home copy, read in full).
Shared context: `.dev/orca-command-refactor/README.md:1-39` (read first).
Candidate (revised in place): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
Baseline for accounting: the candidate before this revision, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (identical copy at `vf1/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, read for `diff`).
Revised candidate: sha256 `bddecb0d53d012639197cb333a623b97ec5dd535120f7fee296fb97a980e41db`.
IDS revised (from `review/round1.md:140` and `review/verify-1.md`, the verifier's `confirmed:` line): M2, M4, M7, M8, M9, M10.
Not run: spec-panel (not requested). Verdict is not awarded here; the next review decides.

## Byte accounting

| | Bytes | Lines |
|---|---|---|
| Before | 57763 | 285 |
| After | 60031 | 288 |
| Net | +2268 | +3 |

Per finding id (added / deleted / net). A shared edit is counted once, under the shared label.

| Id | Added | Deleted | Net | Where (spec line in revised file) |
|---|---|---|---|---|
| M2 | 1003 | 557 | +446 | line 61 (WC-3) |
| M4 (own edits) | 625 | 560 | +65 | line 83 (adversarial row), line 199 (AC-1.4) |
| M4 + M9 (shared edit, counted once) | 886 | 492 | +394 | line 63 (WC-5 outcome rule), line 195 (AC-0.5 new row) |
| M7 | 560 | 270 | +290 | line 172 (AC-C1) |
| M8 | 684 | 512 | +172 | line 112 (load row, Report column), line 268 (load row in Decisions) |
| M10 | 1984 | 1083 | +901 | line 92 (workflow row), line 105 (cli-portify row), line 116 (research row), line 200 (AC-1.5 new row), line 206 (AC-2.6 new row) |
| Total | 5742 | 3474 | +2268 | |

Check: 57763 + 2268 = 60031. Per-id added sum (1003 + 625 + 886 + 560 + 684 + 1984) = 5742; deleted sum (557 + 560 + 492 + 270 + 512 + 1083) = 3474.

M9 has no bytes of its own; its only edits are the shared lines 63 and 195.

## Edits

- **M2, line 61 (WC-3).** The relay of a coordinator answer now applies only to a gate whose section 3 row names the flag that carries the answer, and the answer is passed verbatim as that flag. Safety and authorization gates never take a relayed answer: the implement Ruling (D2), post-release and pr-submit outward authorizations (D3, D4), cli-eval safety flags, and auggie-review posting (WC-9). They resolve as blocked, except that D2 option (b) still allows a relayed Ruling if the user chooses it. This also names the flag a free answer maps to (the section 3 row's flag), which the finding asked for. Ties to `spec:233-235` (D2) and `spec:245` (D4) in the revised file.
- **M4 and M9, line 63 (WC-5).** `--outcome succeeded` now only when `status` is `succeeded` or `partial`. A FAIL audit still maps to succeeded, as before. Every other case maps to failed: `failed` or `blocked`, a missing, unparseable or out-of-set `status`, or no report. The "otherwise" rule is gone. Basis: WC-4's four-value set (`spec:62`) and the Orca rule "Never encode failure only in prose" (`inventory/orca-capabilities.md:73`).
- **M4 and M9, line 195 (AC-0.5, new).** P0 check: a planted contract with `status: done`, with no `status`, and with `status: partial` (`uv run pytest tests/skills/test_worker_contract.py -q -k outcome`). `done` and missing must map to failed, and `partial` to succeeded. This is the planted invalid-status case M9 asked for.
- **M4, line 83 (adversarial row).** The contract is written at `<output>/return-contract.yaml`, the WC-4 path. The subdirectory `<output>/adversarial/...` is removed, so section 3 and WC-4 name one path (`spec:62` against the old `spec:83`).
- **M4, line 199 (AC-1.4).** The check now requires adversarial to name `<output-dir>/return-contract.yaml` with no subdirectory.
- **M7, line 172 (AC-C1).** The alternation `\|` is gone: the pattern is now `\borca\b` with `grep -i`, which matches `orca`, `orca-ide` and `orca-cli`, and `orca status` as well as the four subcommands. Two excluded files are named by path: `src/superclaude/core/WORKER-CONTRACT.md` (SA-2 contract example) and `src/superclaude/core/HOW-WE-WORK.md` (SA-5 Orca section). A self-test line is added. Probe run in this sandbox (no file written): `printf 'orca orchestration worker-start\n' | grep -iE '\borca\b'` exits 0, and `orca-ide status --json` matches. The exclusion of the two core files is needed only so the corrected check does not flag text the spec permits; the rest of HOW-WE-WORK.md is not checked by AC-C1. The verifier's rejected point M5 is not actioned; that residual gap stays noted.
- **M8, line 112 (load row, Report column).** Under `--unattended`, load writes a status-only contract (`status`, `command`, no `report_path`). WC-4 already allows `report_path` "if any". This is the first of the two options the finding offers (minimal contract); the exception option was not chosen, so WC-4 and AC-1.1 stay as written.
- **M8, line 268 (Decisions, `/sc:load handling`).** The row now says why no report file is added: the contract is status-only, so WC-4 and AC-1.1 hold and the standalone path writes nothing new (SA-3). It no longer says a contract would be "unrequested".
- **M10, line 92 (workflow row).** The brief adds `--output-dir <dir>` from P1. With that flag the contract goes to `<output-dir>/return-contract.yaml`. Until P1 the per-run `.dev/tasks/to-do/<id>/` path still applies, and the row says so, so P0's smoke run (`spec:158`, AC-0.4 at `spec:194`) is unchanged. Basis for the per-run path: `inventory/commands-b.md:52` and `:272` (`spec` cites them; read as cited).
- **M10, line 105 (cli-portify row).** The contract goes to `<output-dir>/return-contract.yaml`; the file location is named, and a new `--output-dir` flag (SA-3) is added for unattended runs.
- **M10, line 116 (research row).** The contract goes to `<output-dir>/return-contract.yaml`, and `--output-dir` is added as a new flag. The research file keeps its generated `claudedocs/research_*.md` path unless the flag is passed. Basis: `inventory/commands-b.md:38` and `:132`.
- **M10, line 200 (AC-1.5, new).** A 7.2 live run of `/sc:workflow --handoff none --unattended --output-dir <dir>`, including a pre-creation STOP case. The check is that `worker_done --report-path` equals `<dir>/return-contract.yaml` and the file exists.
- **M10, line 206 (AC-2.6, new).** The same check for `/sc:research` and `/sc:cli-portify`, both with `--unattended --output-dir <dir>`.

Scope notes:
- Section 3 counts (10 ready, 27 needing a change, 6 coordinator-only) are unchanged, because no row moved between sections. The counts do not add to the 43 commands in §3's intro (`spec:75`); that mismatch existed before this revision and is outside IDS, so it is left alone.
- No new rule, section or mechanism was added beyond what the six confirmed findings call for. Every addition cites its finding id in the revised text.
- Minor and Medium findings were not touched.

## Finding rows

Applied (confirmed by `review/verify-1.md`, `confirmed: M2, M4, M7, M8, M9, M10`):

| Id | Status | Applied where | Reason or evidence |
|---|---|---|---|
| M2 | applied | spec line 61 (WC-3) | Relay limited to flag-carrying gates; safety and authorization gates excluded; D2(b) noted. `review/round1.md:16-23`; `review/verify-1.md` row M2. |
| M4 | applied | spec line 83 (adversarial), line 63 (WC-5, shared), line 195 (AC-0.5, shared), line 199 (AC-1.4) | Missing or unknown `status` now maps to failed; adversarial uses the WC-4 path. `review/round1.md:25-38`; `review/verify-1.md` row M4. |
| M7 | applied | spec line 172 (AC-C1) | Alternation removed (pattern is now `\borca\b`), self-test added, two core files excluded by name. `review/round1.md:40-53`; `review/verify-1.md` row M7 (probe). |
| M8 | applied | spec line 112 (load row), line 268 (Decisions row) | Status-only contract under `--unattended`; WC-4, AC-1.1 unchanged. `review/round1.md:55-59`; `review/verify-1.md` row M8. |
| M9 | applied | spec line 63 (WC-5, shared with M4), line 195 (AC-0.5, shared with M4) | Only `succeeded` and `partial` map to succeeded; planted invalid-status case added. `review/round1.md:61-65`; `review/verify-1.md` row M9. |
| M10 | applied | spec line 92 (workflow), line 105 (cli-portify), line 116 (research), line 200 (AC-1.5), line 206 (AC-2.6) | Output flags and WC-4 paths for the three commands; path-match checks added. `review/round1.md:67-74`; `review/verify-1.md` row M10. |

Noted, not confirmed (verifier rejected; not revised, not prior blocking findings, per the REVISE prompt and `review/verify-1.md`):

| Id | Status | Reason (verifier) |
|---|---|---|
| M1 | noted, unactioned | Both rows sit in the §3.2 column headed "Unattended-mode gate resolution (WC-2)", so they scope to `--unattended` (`review/verify-1.md` row M1). Not revised. |
| M3 | noted, unactioned | The FAIL-audit-as-succeeded mapping is deliberate; its "wrong" reading depends on the UNVERIFIED Orca rule (`review/verify-1.md` row M3). Not revised. Note: my WC-5 edit keeps this mapping. |
| M5 | noted, unactioned | The `\|` argument is void as written; the fix for AC-C1 touches the same row but this noted point is not actioned (`review/verify-1.md` row M5). The excluded core files in AC-C1 are a side effect of M7, not of M5. |
| M6 | noted, unactioned | Depends on INV-B:272 field set, which is not in this sandbox (`review/verify-1.md` row M6). Not revised. |
| M11 | noted, unactioned | The stale-contract attack needs the retry to reuse an output directory, which §2.3 does not say (`review/verify-1.md` row M11). Not revised. |
| M12 | noted, unactioned | Depends on `command.md:23` and `:459-460`, not in this sandbox (`review/verify-1.md` row M12). Not revised. |

Citations I could not check here (`inventory/*` and `review/*` are the only evidence I can read; command and skill files under `src/` are not in this sandbox): `skills/...` and `cmd/...` lines are carried from the inventories and are UNVERIFIED in this revision. The new spec text relies on `inventory/orca-capabilities.md:73` (checked: line 73 holds the "Never encode failure only in prose" quote) and `inventory/commands-b.md:38, 52, 132, 272` (checked: lines exist and match the cited rows).

## Self-check
- Each applied row above names only text the confirmed finding quotes or cites.
- No minor or Medium finding was regraded or edited.
- The candidate was not run through spec-panel, and no PASS is awarded.
