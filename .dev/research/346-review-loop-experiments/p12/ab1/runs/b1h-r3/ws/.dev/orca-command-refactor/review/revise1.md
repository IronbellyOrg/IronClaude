# Revise 1 (REVISE prompt, document_review_loop_prompts.md)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
baseline sha256 (before revision): d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d (57763 bytes, 285 lines)
revised sha256 (after revision): e28114855e5685eb7f3f2e2652a756ffaac57ed4c9ffb0b7423b91d78a8e8d19 (59705 bytes, 293 lines)
prior report: .dev/orca-command-refactor/review/round1.md (review: 1 of 3, verdict FAIL)
verifier reply: .dev/orca-command-refactor/review/verify-1.md
blocking ids repaired (IDS): M3, M4, M6, M7, M8, M10

Scope: only the confirmed blocking ids were repaired. Minor and Medium findings were left alone. The spec-panel was not run, and the candidate was not given a PASS.

## Byte accounting

Byte counts are for each replaced span (old text deleted, new text added), measured in UTF-8 bytes. Edits that serve two ids are marked shared, and their full bytes are listed under both ids. The file total counts each shared edit once.

Total: 1747 bytes deleted, 3689 bytes added, net +1942 (57763 to 59705). Check: 59705 - 57763 = 1942.

| Edit (spec location) | Deleted | Added | Net | Finding id(s) |
|---|---|---|---|---|
| §2.2 WC-4 field list and exception (spec:62) | 191 | 349 | +158 | M3 (verdict field), M8 (load exception); shared |
| §2.2 WC-5 outcome mapping (spec:63) | 282 | 423 | +141 | M3 (gate on verdict), M4 (missing or unknown status); shared |
| §2.2 WC-5 evidence cell (spec:63) | 14 | 32 | +18 | M3, M4; shared |
| §3 intro, load exception (spec:76) | 80 | 154 | +74 | M8 |
| §3.1 workflow row (spec:92) | 179 | 346 | +167 | M10 |
| §3.1 adversarial row, filename fix (spec:83) | 77 | 112 | +35 | M4 |
| §3.2 research row (spec:116) | 85 | 178 | +93 | M10 |
| §3.2 cli-portify row (spec:105) | 60 | 112 | +52 | M10 |
| §3.2 load row, Report cell (spec:112) | 36 | 46 | +10 | M8 |
| §7.3 AC-0.4 (spec:194) | 180 | 535 | +355 | M6 |
| §7.1 AC-C1 table row (spec:172) | 269 | 121 | -148 | M7 |
| §7.1 AC-C1 block, self-test and grep outside the table (new, after spec:172) | 41 | 657 | +616 | M7 (the 41 deleted bytes are the §7.2 heading, which is re-emitted) |
| §7.3 AC-1.1 (spec:195) | 97 | 120 | +23 | M8 |
| §7.3 AC-1.4 (spec:198) | 100 | 137 | +37 | M4 |
| §7.3 AC-1.5 (new row, spec:198a) | 15 | 233 | +218 | M10 (the 15 deleted bytes are the AC-2.1 row, re-emitted) |
| §7.3 AC-2.3 (spec:201) | 41 | 134 | +93 | M10 |

Per finding id, edits attributed to it (shared edits included in full):

| Finding id | Edits | Deleted | Added |
|---|---|---|---|
| M3 | WC-4 (shared with M8), WC-5 (shared with M4), WC-5 evidence (shared with M4) | 487 | 804 |
| M4 | WC-5 (shared with M3), WC-5 evidence (shared with M3), adversarial row, AC-1.4 | 473 + 14 + 77 + 100 = 664 | 423 + 32 + 112 + 137 = 704 |
| M6 | AC-0.4 | 180 | 535 |
| M7 | AC-C1 row, AC-C1 block | 269 + 41 = 310 | 121 + 657 = 778 |
| M8 | WC-4 (shared with M3), §3 intro, load row, AC-1.1 | 191 + 80 + 36 + 97 = 404 | 349 + 154 + 46 + 120 = 669 |
| M10 | workflow row, research row, cli-portify row, AC-1.5 row, AC-2.3 | 179 + 85 + 60 + 15 + 41 = 380 | 346 + 178 + 112 + 233 + 134 = 1003 |

## Finding rows

Verdict column: applied = repaired in the candidate; noted = not revised, as the verifier rejected it (round1.md, "Noted, unactioned").

| Id | Disposition | Where applied (spec line in the revised file) | Reason or cited basis |
|---|---|---|---|
| M3 (M3.a) | applied | WC-4 (spec:62) adds the optional `verdict` field; WC-5 (spec:63) says an audit with verdict FAIL succeeds as a run and the coordinator gates dependent Tasks on `verdict`; §2.2 evidence cell (spec:63) notes the revision | round1.md M3.a. Basis for the field: the spec's own rule "Never encode failure only in prose" (`.dev/orca-command-refactor/inventory/orca-capabilities.md:73`, CAPS:73), and the WC-4 field list had no verdict (spec:62). CAPS:73 checked against the inventory file. |
| M4 (M4.a) | applied | WC-5 (spec:63): `--outcome failed` when `status` is missing or not one of the four values; `--outcome succeeded` only for `succeeded` or `partial` | round1.md M4.a. The four-value rule is in WC-4 (spec:62). The fix also covers the M9 case (`done` or empty status) because "unknown" includes it. M9 itself stays noted. |
| M4 (M4.b) | applied | §3.1 adversarial row (spec:83): filename becomes `<output>/return-contract.yaml`, the WC-4 path, when `--output` is passed; AC-1.4 (spec:198) names the WC-4 path | round1.md M4.b. The inventory names no contract filename for adversarial (`.dev/orca-command-refactor/inventory/commands-a.md:35`, INV-A:35), and the spec's WC-4 path is the one the coordinator reads. Choosing one rule, as the M4 recommendation asks. |
| M6 (M6.a) | applied | AC-0.4 (spec:194): step 4 is replaced for P0 per command. workflow: `status` only, since no `command` key exists (`.dev/orca-command-refactor/inventory/commands-b.md:272`, INV-B:272 lists `status`, `plan_path`, `reflect_report_path`); troubleshoot: `test -s <dir>/REPORT.md` (the report is markdown, INV-B:49, per round1.md; not re-read here, UNVERIFIED in this run); adversarial: `test -s` on its existing contract. Step 3's path is the one the command writes today | round1.md M6.a and its recommendation. P0 cannot use the WC-4 path before P1. |
| M7 (M7.a and M7.b) | applied | AC-C1 row (spec:172) now refers to the block below; the new block (spec:172a) holds the grep with `-E -i` and an unescaped `|` alternation, adds `status` to the subcommand list, keeps the ccsession-tag allowlist, and adds a self-test that must count 2 on a planted two-line sample | round1.md M7.a and M7.b. Verified in this run: the self-test prints 2 on the planted sample and 0 on `x`. The table cell turned `\|` into a literal pipe, so the pattern sits outside the table. The broad `\borca` form in M7.a was not adopted, because it would also match the Orca text SA-2 allows in the contract file (M5, noted). |
| M8 (M8.a) | applied | WC-4 (spec:62) adds the `/sc:load` exception; §3 intro (spec:76) names the exception; §3.2 load row (spec:112) Report cell says "WC-4 exception"; AC-1.1 (spec:195) excludes `/sc:load` | round1.md M8.a, option 2 (name load as the exception). The load row already says no report file (`.dev/orca-command-refactor/inventory/commands-b.md:65`, INV-B:65: it "writes no file"); §9 decision row (spec:265) is unchanged and consistent with it. |
| M10 (M10.a) | applied | §3.1 workflow row (spec:92): under `--unattended`, the contract goes to `<output-dir>/return-contract.yaml` from a new `--output <dir>` flag; standalone keeps the package path (SA-3). §3.2 research row (spec:116) and cli-portify row (spec:105): contract at `<output-dir>/return-contract.yaml` with an `--output <dir>` flag. AC-1.5 (new, spec:198a) and AC-2.3 (spec:201) check the path | round1.md M10.a. The inventory gives no output flag for workflow (`.dev/orca-command-refactor/inventory/commands-b.md:52`, INV-B:52: the contract is in the per-run package) or research (`.dev/orca-command-refactor/inventory/commands-b.md:38`, INV-B:38: the file name is generated). The chosen fix adds flags, which the M10 recommendation allows. The added flag is named in each changed row, so it stays traceable. |
| M1 | noted, unactioned | not revised | Verifier rejected (verify-1.md; round1.md "Noted, unactioned"): the column header scopes both rows to unattended mode, which matches WC-11 (spec:69) and SA-1 (spec:146). Not a prior blocking finding for the next re-review. |
| M2 | noted, unactioned | not revised | Verifier rejected (verify-1.md): the stated outcome (halt cleared) is blocked by the unchanged Ruling rule at spec:109 and spec:233; the candidate names no Ruling flag for implement. Not a prior blocking finding. |
| M5 | noted, unactioned | not revised | Verifier rejected (verify-1.md): SA-2 (spec:147) permits Orca text in the contract file and SA-5 (spec:150) requires an Orca section, but neither requires an `orca <subcommand>` string, so AC-C1 failing needs an assumed example. Not a prior blocking finding. The revised AC-C1 (M7) still matches only the `orca <subcommand>` form. |
| M9 | noted, unactioned | not revised (its case is covered by the M4 wording in WC-5, spec:63) | Verifier rejected (verify-1.md): the candidate does not state that a `done` or empty status is a failure. The M4 rule ("not one of the four values") covers that case as a side effect. The rule is not a separate addition and is not claimed as a verified M9 fix. |
| M11 | noted, unactioned | not revised | Verifier rejected (verify-1.md): WC-6 (spec:64) already requires a fresh output directory for commands with no resume flag, so the stale-contract retry needs an implementer who violates WC-6, and the §2.3 premise is not in §2.3. Not a prior blocking finding. |
| M12 | noted, unactioned | not revised | Verifier rejected (verify-1.md): the `--output` file-valued claim rests on `command.md:23,459-460` and `INV-B:43`, which are not in this workspace. Those citations are UNVERIFIED here. The spec-panel row (spec:120) is unchanged. |

## Checks run in this revision

- AC-C1 self-test pattern: planted sample `orca orchestration worker-start` and `orca-ide status --json` printed count 2; a non-matching line printed count 0.
- Table rows edited for AC-C1, AC-1.5 and AC-2.3 keep their cell counts (3 cells for AC-C1 and 4 for the phase rows).
- Citations used in this revision were checked against files in this workspace: spec lines, `commands-a.md:35`, `commands-b.md:38,52,65,272`, `orca-capabilities.md:73`. Not checked here and marked UNVERIFIED: `command.md:23,459-460`, `commands-b.md:43`, and the troubleshoot `REPORT.md` location in INV-B:49.

## Not done

- No spec-panel or review was run. The verdict stays with the next re-review.
- Nothing was committed or pushed.
