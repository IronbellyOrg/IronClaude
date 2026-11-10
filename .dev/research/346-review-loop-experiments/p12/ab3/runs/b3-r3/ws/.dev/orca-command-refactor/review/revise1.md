# Revise report, round 1: orca-worker-contract-spec.md

Revise brief applied: repair only the blocking findings F-01, F-02 (`.dev/orca-command-refactor/review/round1.md:28,224-228`). No PASS is claimed. Medium findings M-01 to M-10 and minor notes N-01 to N-05 were left alone.

Edited file: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (in place; the only file changed besides this report). Baseline for the accounting: `.dev/orca-command-refactor/specs/history/spec-v1.md`, byte-identical to the spec before this revision (`cmp` printed no difference).

## Byte accounting
| Measure | Before | After |
|---|---|---|
| bytes | 57763 | 59305 |
| lines | 285 | 285 |
| sha256 | d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d | e40e99ee4052bc08befc7a5c553a10250f30eed258a771b80b4e6936f8bf5bff |

Net change +1542 bytes. Added and deleted bytes are counted on a whitespace-separated token diff of baseline against candidate (a changed token counts as deleted plus added), measured once after the F-01 edits and once after the F-02 edits:

| Finding | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| F-01 | 1260 | 256 | +1004 |
| F-02 | 649 | 111 | +538 |
| Total | 1909 | 367 | +1542 |

Spec line numbers did not move (no line added or removed), so the line numbers named in `round1.md` still point at the same rows.

## Disposition per finding id
| id | Disposition | Where applied (spec line) | Reasoning |
|---|---|---|---|
| F-01 | Applied | WC-4 (line 62); section 2.3 (line 73); section 3 intro (line 76); init-lite row (line 87); tdd row (line 90); workflow row (line 92); cli-eval row (line 104); AC-1.2 (line 196); AC-2.2 (line 200) | See F-01 detail below. |
| F-02 | Applied | Section 3 intro (line 76); brainstorm row (line 84); load row (line 112); P1 row of section 6 (line 159); P4 row (line 162); AC-1.1 (line 195) | See F-02 detail below. |

### F-01 detail (WC-4 contract path had no answer for tdd, init-lite, cli-eval, workflow, adversarial)
Defect (`round1.md:54-65`): WC-4 defined the contract as `<output-dir>/return-contract.yaml` for a directory the coordinator passes, but the tdd and init-lite rows pass `--output <file>` (spec lines 87, 90 before the edit), cli-eval had no output flag (`inventory/commands-a.md:44`: "No single named report file", fixed workspaces only), workflow's contract sits under a generated `<id>` and is not written for pre-creation STOPs (`inventory/commands-b.md:272`), and adversarial's contract is `<output>/adversarial/return-contract.yaml` (`inventory/commands-a.md:35`).

Changes (each carries "F-01" or names WC-4):
- WC-4 (line 62): the path rule is now per command. Directory-valued flag: `<dir>/return-contract.yaml`. tdd and init-lite (file-valued `--output`): the `--output` path with `.return-contract.yaml` in place of its extension, with the worked example `.dev/tdd/auth.md` giving `.dev/tdd/auth.return-contract.yaml`. adversarial: `<dir>/adversarial/return-contract.yaml`. cli-eval and workflow: `<dir>/return-contract.yaml` for a new `--output <dir>` that only names the contract directory. Any other path is stated in its section 3 row.
- Section 2.3 (line 73): "the output directory, so the report path is known" became "the `--output` value, so the contract path is known", so the brief rule agrees with WC-4.
- Section 3 intro (line 76): the definition of "Contract" now says "at the path WC-4 gives for that command" instead of fixing `<output-dir>/return-contract.yaml`.
- init-lite row (line 87) and tdd row (line 90): the contract beside the `--output` file is stated in the "small fix" column with its phase (P1 for init-lite, P2 for tdd, matching the phase each command already had or, for init-lite, the no-gate P1 group).
- workflow row (line 92): "Brief must pass" gains `--output <dir>`; the fix now says the contract is also written at `<dir>/return-contract.yaml` on every outcome, including pre-creation STOPs where `<id>/` does not exist yet, and that the package copy keeps its path. This makes the path known before dispatch, which the old "pre-creation STOP" fix did not.
- cli-eval row (line 104): the report cell names the new `--output <dir>` and says the contract is also written for the blocked cases before any suite is chosen.
- AC-2.2 (line 200): the cli-eval example now passes `--output <dir>`, otherwise the check has no contract path; the tdd example already passes `--output <file>` and now resolves under WC-4.
- AC-1.2 (line 196): "`--output <dir>`" became "its `--output` as WC-4 gives it (a directory, or a file for init-lite)", since init-lite is a P1 command with a file-valued flag.
- 7.2 step 3 (line 182): left unchanged. "its report path is the WC-4 contract path" now resolves because WC-4 defines the path for every command; no edit was needed.
- adversarial row (line 83): left unchanged. Its fix already names `<output>/adversarial/return-contract.yaml`, which WC-4 now states as the exception.

New mechanism added: one flag, `--output <dir>` on cli-eval and workflow, limited to naming the contract directory. The finding's own recommendation calls for it ("a brief-supplied directory for cli-eval and workflow", `round1.md:64`); there is no way to know a path before dispatch without a brief-supplied value.

Not touched although related: cli-portify ("file location unnamed"), implement, pr-submit, research, recommend rows. `round1.md` does not name them under F-01 (`round1.md:227`), and any gap there is not a blocking finding.

### F-02 detail (AC-1.1 and the P1 scope contradict the load row, the P4 hold and recommended D3(a))
Defect (`round1.md:67-78`): AC-1.1 and the P1 scope required the flag and section on all 37 commands of sections 3.1 and 3.2 in P1, which contradicts the load row (no report, `INV-B:65`), the P4 hold on implement, post-release and pr-submit, and D3(a) ("no pr-submit changes in Phase 4"), and which leaves the flag without its WC-2 gate behavior for the commands whose gates convert in P2 to P4.

Changes (narrowing; each carries "F-02"):
- P1 row, scope (line 159): the flag and `## Unattended mode` section go "on the commands named in this row only"; "each later phase adds them to its own commands with their gate behavior".
- P1 row, commands (line 159): `load` moved out of the flag list to "usage line only, no flag and no section". Added `brainstorm` and `init-lite`, which sat in no phase's list (a count from the section 3 and section 6 tables: P1 13 + P2 15 + P3 4 + P4 3 = 35 of the 37, the two missing being these two; this is the "never (2)" of `round1.md:171`). Both have no gate, so their flag is a no-op and fits the P1 title. The P1 flag set is then 14 commands: 8 no-gate commands, brainstorm, init-lite and the 4 fix commands.
- brainstorm row (line 84): "Accept `--unattended` (no gate) (P1, F-02)" so the table matches the P1 list.
- load row (line 112): states it gets neither `--unattended` nor the section.
- Section 3 intro (line 76): "gains the section in the phase its row names, except `load` and `pr-submit` under D3 (a)".
- P4 row (line 162): implement and post-release gain the flag and section there; pr-submit does only under D3 (b), and under the recommended D3 (a) it gets neither. This agrees with D3 (a) and section 4's closing note.
- AC-1.1 (line 195): the test now asserts the section on every command named in the P1 row except `load`, and asserts that neither `load` nor any section-4 command has one.

## Verification done
- `diff history/spec-v1.md orca-worker-contract-spec.md`: 13 changed line ranges, all within the rows listed above; no section 4, section 5, section 8 or Decisions line changed.
- Citations in the added text were checked against `inventory/commands-a.md:35,44` and `inventory/commands-b.md:65,272`, which are inside the workspace. The spec's own source citations (`src/...`, `cmd/...`) were carried from the inventories and not re-read here, and are UNVERIFIED in this sandbox.
- The spec-panel was not run. No review verdict is given.

## Left open on purpose
- Medium findings M-01 to M-10 and minor notes N-01 to N-05 (`round1.md:30-50`). Two interact with this revision and should be considered in the next review: M-08 (SA-3 versus WC-4 trigger) is untouched, and M-10 (P0 briefs carry `--unattended` before any command accepts it) is not helped or worsened by P1 now covering fewer commands.
- With the narrower P1 scope, the 3.1 commands reflect, release-split, tdd and troubleshoot gain the flag only in P2 (their rows already say P2); a coordinator that wants to brief them before P2 must omit `--unattended`, as AC-0.4 already does.
