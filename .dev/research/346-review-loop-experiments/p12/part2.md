
Self-check (run): every AFTER line (without its `>`) was found with `grep -nF` in the candidate and every BEFORE line (without its `<`) in the baseline; no quote was missing, so roles are not swapped. The diff is not empty.

## Prior blocking findings

| id | status | evidence (AFTER text only) |
|---|---|---|
| M1 (contract path stated three incompatible ways) | resolved | `spec:62` (WC-4) now says the path is "the contract path its section 3 row gives", default `<output-dir>/return-contract.yaml`, a file-valued `--output` uses the file's directory, and it names the three other locations (adversarial `<output>/adversarial/...`, pr-submit beside its run log, workflow `.dev/tasks/to-do/<id>/...`). `spec:73` limits "known before dispatch" to the default path. `spec:76` defines "Contract" as the path WC-4 gives per command. `spec:182` (7.2 step 3) reads the same per-command path, and for workflow "the path the command wrote". The adversarial row `spec:83` and the workflow row `spec:92` now agree with WC-4. `spec:195-196` no longer conflicts with `spec:62` for these rows. The adversarial path matches the on-disk uncertainty recorded at INV-A:60 (two different locations in the earlier run), so fixing it at `spec:83` is a stated P1 change. |
| M2 (AC-1.1 cannot pass for `load`) | resolved for AC-1.1 only | `spec:195` now says "every command in sections 3.1-3.2 except `load`" and asserts that `load` has none; `spec:112` says `load` gets no `## Unattended mode` section; `spec:159` says "except load". `spec:265` (Decisions) is unchanged and consistent. The same contradiction still exists under AC-1.2; see N1. |
| M3 (WC-4 and 2.3 vs the adversarial and workflow rows; AC-0.4) | resolved | Same edits as M1. The workflow pre-creation STOP is now stated: no contract is written (`spec:62`, `spec:92`, `spec:198`), WC-5 maps "no report" to `--outcome failed`, matching INV-B:272 ("Not written for pre-creation STOPs"). AC-0.4 step 3 residue (the contract does not exist in P0) is recorded as follow-up F1 because the prior finding rests on the WC-4 path contradiction, which is repaired, and `spec:194` already says step 4 uses the existing report file. |
| M4 (AC-1.1 vs the `load` row) | resolved for AC-1.1 only | Same as M2. |
| M5 (AC-1.1 vs `load`, the 3.1 "None" fixes, the P2-P4 commands) | resolved for AC-1.1 only | `spec:79` now lists the `## Unattended mode` section as a command change, so brainstorm and init-lite (`spec:84`, `spec:87`, fix "None") are consistent with `spec:76`. `spec:159` assigns the section to every 3.1-3.2 command except `load` in P1, so the P2-P4 gap in the AC-1.1 assertion is closed. The `load` part carries over to N1. |

## Findings on lines changed against the baseline

### N1. AC-1.2 requires a live `--unattended --output <dir>` check on every P1 command, and `load` is a P1 command that now takes neither (blocking)

- Origin: `changed` (the changed lines `spec:112` and `spec:159` make `load` explicitly outside `--unattended`; the unchanged line `spec:196` depends on them). Experts: Wiegers (traceability), Crispin (acceptance criterion cannot pass), Whittaker (Sequence Attack: run the P1 gate in its stated order).
- Stated texts:
  - `spec:159` (changed): P1 Commands cell lists "load (usage line only)", and the same row says the flag and section go "in every command in sections 3.1 and 3.2 except load".
  - `spec:112` (changed): `load` "gets no `## Unattended mode` section", Report "none", "not as its own Task".
  - `spec:196` (unchanged, AC-1.2): "7.2 live check on each P1 command with `--unattended --output <dir>`", pass condition "all steps pass".
  - `spec:182-183` (7.2 steps 3-4; `spec:182` changed): step 3 needs a `worker_done` whose report path is the contract path WC-4 gives; step 4 runs `test -s <contract>` and a YAML assertion on `status` and `command`.
  - `spec:167`: "A phase passes only when every check in its block and every common check passes."
- Grading sentence: An implementer who follows the stated text as written runs the 7.2 check on `load` with `--unattended --output <dir>` (`spec:196`, because `spec:159` lists `load` as a P1 command), and builds `load` with no `--unattended` flag, no section and no contract (`spec:112`, `spec:159`, `spec:265`). That is wrong because step 4 (`spec:183`) has no contract to open, step 3 has no contract path, so AC-1.2 fails, and by `spec:167` the P1 gate cannot pass; the only way to pass is to give `load` a contract, which `spec:265` rejects.
- Concrete attack (Whittaker, Sequence): state before: P1 edits done, `load` has the usage-line fix only. Steps: dispatch `/sc:load --unattended --output out/`; the worker ends with no report file. State after: `out/return-contract.yaml` absent, `test -s` exits 1, AC-1.2 red, P2 never starts (`spec:154`).
- Recommendation: one clause in AC-1.2 (`spec:196`) or in the P1 Commands cell (`spec:159`) saying the live check excludes `load`; no new rule is needed.
- Priority: High. Quality impact: the P1 gate is unpassable as written, the same defect class as M2 on a different row.

## Guard Condition Boundary Table (changed lines only)

Guards on changed lines: `--output` file versus directory (`spec:62`), "pre-creation STOP" versus post-creation (`spec:62`, `spec:92`, `spec:198`), "except load" (`spec:159`, `spec:195`). Classes that cannot occur for a guard are omitted with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--output` is a file | `spec:62` | Zero/Empty | `--output ""` | not stated | not stated | GAP (Medium, F3) |
| `--output` is a file | `spec:62` | Typical | `--output docs/x.md` | true | contract at `docs/return-contract.yaml` | OK |
| `--output` is a file | `spec:62` | Legitimate Edge Case | two workers, files in one directory | true for both | both write `docs/return-contract.yaml`; WC-11 (`spec:69`) speaks of default paths, not this case | GAP (Medium, F3) |
| pre-creation STOP (workflow) | `spec:62`, `spec:92` | Typical | invalid input before `<id>` exists | true | no contract; `--outcome failed` (WC-5) | OK |
| pre-creation STOP (workflow) | `spec:62` | Legitimate Edge Case | failure after `<id>` exists, before the contract is written | not stated; the ref line is UNVERIFIED here (`sk/sc-workflow-protocol/refs/return-contract.md:39,41` via INV-B:272 says "every post-creation outcome") | covered by INV-B:272, which is the stated source | OK |
| `except load` | `spec:159`, `spec:195` | Typical | `load` | true | no section; asserted absent | OK in AC-1.1, GAP in AC-1.2 (N1) |

Left out: Maximum/Overflow and Sentinel Value Match, which do not occur for these guards (no counts, no reserved values).

## Follow-up candidates (Medium and minor; none triggers a revision)

- F1 (Medium, origin=changed, `spec:182` vs `spec:194`): AC-0.4 requires steps 1-3 to pass in P0, but step 3 now needs the "contract path WC-4 gives", and in P0 `/sc:troubleshoot` and `/sc:adversarial` write no contract (`spec:79`, `spec:83`, `spec:91`; `spec:194` itself says "the contract arrives in P1" for step 4). Graded Medium because `spec:194` shows the intent and the wrong outcome needs a guess about which reading an implementer picks. Suggest one clause in step 3: "in P0, the command's existing report file".
- F2 (Medium, origin=changed, `spec:62`): "Three rows give another location" is not complete. `spec:85` (cleanup-audit, fixed `.claude-audit/`, no output flag) and `spec:86` (index-repo, no output flag) have no coordinator-passed `<output-dir>`, so the default has no value for them. Their P1 fixes (`spec:85`, `spec:86`) name a location but not a contract path.
- F3 (Medium, origin=changed, `spec:62`): the file-valued `--output` rule puts the contract in the file's directory, so two tdd or init-lite workers writing files into one directory write one `return-contract.yaml` (WC-11 at `spec:69` covers default output paths only).
- F4 (Medium, origin=changed, `spec:159` vs `spec:154`): P1 now puts the flag and section on implement, post-release and pr-submit (P4, which "waits for answers to D2-D4") and on validate-tests (P3, whose skill cannot write a file today, `spec:125`). The section would name a contract those commands do not yet write. If the flag is a no-op where a gate exists, a coordinator that passes `--unattended` to post-release in the P1 to P3 window gets WC-9's outward actions switched on (`spec:68`); the text says "a no-op where a command has no gate", which leaves gated commands unspecified.
- F5 (minor, origin=unchanged, `spec:149`): SA-4 still lists "adversarial and workflow contract gaps" as a section 3 defect fix; the workflow row now says "None" (`spec:92`). Depends on the changed row `spec:92`.
- F6 (minor, origin=changed, `spec:62`): WC-2(c) says a blocked gate writes `status: blocked` with the question, but a workflow pre-creation STOP now writes nothing, so a blocked question there goes only in the `worker_done` body. Workflow has no stated gate (the workflow entry at INV-B:267-275 states "None" for gates (a) and (b)), so no wrong outcome follows.

Medium and minor findings never trigger a revision. The session that ran this review asks the user once whether to open an issue for them and creates none without an answer. This run asked nothing and created nothing (no user channel in this sandbox).

## Coverage

Covered: all 10 changed hunks, the five prior blocking findings, the dependencies of the changed lines (`spec:62-73`, `76-79`, `83-92`, `112`, `149`, `154`, `159`, `167`, `182-183`, `194-198`, `265`), and INV-A:60 and INV-B:272 for the evidence. Not covered: the unchanged remainder of the document (whole-document assurance needs a separate, labelled first review); the `src/`, `sk/` and `cmd/` files, which are UNVERIFIED in this sandbox. Briefs and the Precedence rule: the brief did not widen scope, so no clause was overridden.

## Reviser brief

Blocking finding ids: N1.
Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. N1 text to repair: `spec:196` (AC-1.2) against `spec:112` and `spec:159`.

verdict: FAIL
