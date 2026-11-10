# Revise report: Orca worker-contract spec, gate blocking findings B-1 to B-5

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Prompt: REVISE prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (lines 53-56)
- Input report: `.dev/orca-command-refactor/review/gate.md` (`verdict: FAIL`, Reviser brief at `gate.md:142-148`)
- Ids repaired: B-1, B-2, B-3, B-4, B-5 (`{{IDS}}` = the Reviser brief's blocking ids, `gate.md:144`). Medium (F-1 to F-7) and minor (N-1 to N-6) findings left alone.
- No PASS is awarded here. The gate loop's RE-REVIEW decides.
- Spec size before: 59962 bytes (sha256 `2a0ba05dc4158ae8fc6c4b9c265ce2ded840533c29031835d61d7c548122ac84`, matches `gate.md:6`).
- Spec size after: 61081 bytes (sha256 `060d1fb59804955f83e92638dceec3c2655f94b7c59c399f7112f8a8c9bfd1d2`), 285 lines (unchanged line count; every edit is inside an existing line).
- Net change: +1119 bytes. Gross: +1134 added, -15 deleted.

## Byte accounting per finding id

| Finding | Bytes added | Bytes deleted | Net | Where applied (spec lines after revision) |
|---|---|---|---|---|
| B-1 | 182 | 0 | +182 | `:61` (WC-3 excludes the implement Ruling halt); `:109` (implement row: no `ask` sent for this halt) |
| B-2 | 48 | 0 | +48 | `:73` (section 2.3: `--unattended` from P1 on; P0 briefs omit it) |
| B-3 | 541 | 0 | +541 | `:88` (reflect brief passes `--output <dir>`; timestamped default replaced); `:91` (troubleshoot brief passes `--output <dir>`); `:92` (workflow brief passes `--output <dir>`, added in P1); `:92` small-fix cell (the flag puts package and contract where the brief names) |
| B-4 | 282 | 15 | +267 | `:62` (WC-4: file-output contract is `<file-stem>.return-contract.yaml`); `:73` (section 2.3: shared directories need distinct contract names, or one directory per directory-output Task); `:90` (tdd row: fresh file per Dispatch, named contract) |
| B-5 | 81 | 0 | +81 | `:195` (AC-1.1 excludes `load`, which writes no contract) |
| **Total** | **1134** | **15** | **+1119** | |

Gross counts come from the exact old and new strings of each edit (difflib over each pair). Net counts match the measured file sizes: 59962 + 1119 = 61081.

## Row per finding id

| Id | Disposition | Applied where | Basis |
|---|---|---|---|
| B-1 | Applied | `:61` WC-3, new sentence after "as a flag.": the implement Ruling halt (`E-HALT-QA`, `E-NO-RULING`) is excluded from the `ask` path. `:109` implement row: "no `ask` is sent for this halt (B-1; see open decision D2)". | The two texts conflicted: WC-3 allowed an `ask` at a Ruling halt, while the implement row (`:109`) and D2(a) (`:235-236`) say the worker stops and ends `failed`. The safety rule is `sk/sc-implement-protocol/refs/qa.md:238`, quoted at `.dev/orca-command-refactor/inventory/commands-a.md:66`. Both are cited as in gate.md; the source file is outside the workspace, so the quote is UNVERIFIED against the source. |
| B-2 | Applied | `:73` section 2.3: "including `--unattended` (from P1 on; P0 briefs omit it, section 6; B-2)". | Section 2.3 required `--unattended` in every brief, but the P0 smoke runs use the ready commands, which have no such flag (`:158`, `:79`). AC-0.4 (`:194`) already runs them without it. Section 6's P0 row (`:158`) says "before any command changes", so P0 is the stated scope. The flag rule now starts at P1. |
| B-3 | Applied | `:88` reflect: brief passes `--output <dir>` (the `<output>` directory, `.dev/orca-command-refactor/inventory/commands-b.md:112`); the timestamped default `.dev/reflect/<mode>-<slug>-<ts>/` (`commands-b.md:112`) is replaced under `--unattended` (P2). `:91` troubleshoot: brief passes `--output <dir>`; the default `.dev/troubleshoot/<slug>-<timestamp>/` (`commands-b.md:242`) is replaced under `--unattended`, and the flag is added if absent (P2). `:92` workflow: brief passes `--output <dir>`, a flag added in P1, since none exists today (`commands-b.md:52`). | WC-4 (`:62`) refuses a run whose brief omits the directory flag. Reflect, troubleshoot and workflow named no such flag, so AC-1.2 (`:196`, which passes `--output <dir>` to each P1 command) could not pass for workflow. P1 (section 6, `:159`) already adds output flags to commands that lack one, so workflow is consistent with the phase plan. Flag spelling `--output` for reflect and troubleshoot is UNVERIFIED: the inventory names the `<output>` directory and the default path, not the flag. |
| B-4 | Applied | `:62` WC-4: for file-output commands (init-lite and tdd `--output <file>`) the contract is `<file-stem>.return-contract.yaml` in that file's directory, not a bare `return-contract.yaml`. `:73` section 2.3: "Two Tasks may share a directory only when their contract names differ (file-output commands, WC-4); each directory-output Task gets its own directory (B-4)." `:90` tdd row: "a fresh file per Dispatch, WC-11; its contract is `<file-stem>.return-contract.yaml` beside it, WC-4; B-4". | Two tdd dispatches with distinct `--output` files in one directory wrote one `return-contract.yaml` (the earlier text, `:62`), which breaches WC-11 (`:69`). A file stem per Dispatch keeps the names distinct. AC-1.1 (`:195`) still matches, since the new names end in `return-contract.yaml`. |
| B-5 | Applied | `:195` AC-1.1: "every command in sections 3.1-3.2 except `load` has a `## Unattended mode` section ...; and that no section-4 command, and not `load` (it writes no contract, its section 3.2 row; B-5), has one". | The `load` row (`:112`) says "Report (WC-4): none", and the Decision (`:265`) rejects a report file for `load`. AC-1.1 required a `return-contract.yaml` section for every command in 3.1-3.2, which contradicted both. The Decision is unchanged; `load` is now excluded from AC-1.1 and its no-contract rule is stated there. |

## Rejected findings

None. All five blocking findings were repaired.

## Notes for the RE-REVIEW

- Each edit is additive or a narrow replacement inside an existing line. No requirement was added beyond what B-1 to B-5 call for, and no Medium or minor finding was touched.
- Claims in the new text that depend on sources outside the workspace are marked UNVERIFIED in the spec: the `--output` flag spelling for reflect and troubleshoot (B-3), and the `qa.md:238` quote (B-1), as in `gate.md:27`.
- The P1 phase row (section 6, `:159`) and AC-1.2 (`:196`) were not edited; they already assume `--output <dir>` on P1 commands, which B-3 now supports for workflow.
