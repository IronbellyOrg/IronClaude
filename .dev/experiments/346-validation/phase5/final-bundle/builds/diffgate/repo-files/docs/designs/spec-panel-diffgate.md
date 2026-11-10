# Design: diffgate, a computed re-review surface for `/sc:spec-panel` (issue 346)

**Status:** Stage A and Stage B built as an additive variant; `/sc:spec-panel` is unchanged. Folding diffgate into `/sc:spec-panel` (Stage C) is a later decision taken on the S1 result class, never on the bar alone.
**Issue:** IronbellyOrg/IronClaude #346 (document review loops do not converge).
**Source:** the approved SPEC `.dev/brainstorms/346-diffgate/SPEC.md`, as amended by the owner rulings recorded in the plan package `TASK-WF-spec-20261108-181640` (Constraints section). This note trims that SPEC to decisions, formats, residual risks and the measurement plan.

## 1. Decisions

| # | Decision | Why |
|---|---|---|
| D1 | The variant command is `/sc:spec-panel-diffgate` (`src/superclaude/commands/spec-panel-diffgate.md`); it installs next to `/sc:spec-panel` and replaces nothing. | An additive variant can be measured against the earlier S1 arms without touching the shipped command. |
| D2 | The script lives in the infrastructure skill `sc-diffgate` (`src/superclaude/skills/sc-diffgate/`, script `scripts/diffgate.py`, standard library only). | `install_skills.py` (`_has_corresponding_command`) strips `sc-` and skips a skill whose name matches an existing command file; `sc-spec-panel-diffgate` would never install, `sc-diffgate` does. |
| D3 | The variant's base is the 472-line Arm B command file (sha256 prefix `c8d80346a96c`), byte for byte apart from this team's change; it is not the current `src/superclaude/commands/spec-panel.md` (486 lines). | Owner ruling: comparability with the earlier S1 arms, which ran that file. The tests keep a byte copy at `tests/skills/fixtures/diffgate/spec-panel-base-c8d80346a96c.md` and compare against it. |
| D4 | The variant has no `## Unattended mode` section, so it is never run with `--unattended`. | Owner ruling: the base has none and the S1 briefs never pass the flag; `tests/skills/test_worker_contract.py` stays unedited. |
| D5 | The base's one `src/superclaude` line (the examples path in the `**Read**` bullet) is kept; the test asserts the variant adds no occurrence beyond the base's. | Owner ruling KEEP: removing it from the base is a separate follow-up. |
| D6 | Who runs the script: the review and revision sessions run only read-only calls (`status`, `check --dry-run`, `fixcheck --dry-run`); the coordinator runs `begin`, `check` and `fixcheck` as inserted steps between the brief tasks. The reviser keeps its fix map as a `## Diffgate fixmap` block inside its own disposition file. | Owner ruling (SPEC open question 2, alternative chosen): the verbatim S1 briefs let a reviewer write only its report and a reviser only the spec and its disposition file. |
| D7 | The script, not the reviewer, decides blocking, origin, the verdict and the review count. The cap is a constant: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings. | Removes the measured prose causes: self-chosen scope, self-written verdict, copied review count. |
| D8 | Review 1 defers nothing: it has no computed surface and no prior ids, so its findings take a form without `hunk=` and get `origin=full`. Surface-based deferral applies from review 2 onward. | Advisory check QA-001: deferral at review 1 could turn every blocker into a false PASS. |
| D9 | `proxy_all` counts, once per id, every CRITICAL or MAJOR finding the script deferred, demoted or withdrew at any review from 1 to 3, plus the findings first raised in the current review and the prior blocking findings marked `open`, `regressed` or `withdrawn` in it. | Owner decision and ruling: the success measure counts what the script defers, demotes or withdraws as still open. |

## 2. Formats

The contract (subcommands, JSON fields, exit codes, the finding grammar, the files in the loop directory and the `PROFILES` extension point) is `src/superclaude/skills/sc-diffgate/SKILL.md`; this note does not duplicate it. In short:

| Step | Who | Call | Writes |
|---|---|---|---|
| Open review N | coordinator step | `begin --dir <dir> --doc <spec> --expect-round N` | `ledger.json`, `doc-r<N>.md`, `surface-r<N>.md` (N of 2 or more) |
| Review N | reviewer session | `status`, then the review, then `check --dry-run` (one repair turn) | its report only |
| Check N | coordinator step | `check --dir <dir> --report <report>`, then append `close-r<N>.md` to the report | `result-r<N>.json`, `report-r<N>.md`, `close-r<N>.md`, `deferred.md`, `reviser-brief-r<N>.md` |
| Fix cycle N | reviser session | edit the spec, write the `## Diffgate fixmap` block in its disposition file, `fixcheck --dry-run --map <disposition file>` | spec and disposition file only |
| Record fix N | coordinator step | `fixcheck --dir <dir> --doc <spec> --map <disposition file>` | `fixmap-r<N>.txt`, ledger fix record |

Rules the script enforces: one look per change (review k+1's surface is the line and token diff from what review k saw to the current spec, merged within 2 lines, whitespace and pure reflow dropped unless the list, heading or table line count changes); every fix hunk needs an open blocking owner (minor ids cannot own a hunk); anchors are read back against the snapshot and must overlap a changed token of the cited hunk; at most 2 `via` anchors per review; a finding with neither a hunk nor a prior id is deferred as pre-existing from review 2 onward and is never blocking; one repair turn, then finding-level violations degrade; a second structural failure ends the loop `invalid`; three failing `fixcheck` runs in one fix cycle record `fix-rejected` and escalate; `begin` replays every accepted check from its kept report copy, so a hand-edited ledger exits 6.

## 3. Residual risks

What stays prose: whether a finding is true and its severity label right; whether a `resolved by=` hunk really fixes the finding; whether a `via` dependency is real; whether a reviser's id on an edit is honest (the next review sees every such hunk once); and whether the coordinator uses the variant and one directory at all (caught by `--expect-round` and the experiment's validity rules, not by the script).

| Risk | How | Limit | Residual |
|---|---|---|---|
| Blind to a real regression | A defect in fix-k text that review k+1 misses is never re-opened (one look per change). | The blindness audit measures it; deferred items are listed. | Real; it is the price of a bounded loop. |
| Action at a distance | A fix to line A makes unchanged line B wrong. | `via=` with a checked quote of A, at most 2 per review. | A reviewer that does not think of `via`; a third `via` is deferred. |
| Scoped PASS with a known serious defect | A real blocker review 1 missed lands in `deferred: pre-existing`. | Shown once with its label; `acceptance: scoped`; counted in `R3-proxy-all`. | Unfit for a release gate that must block on every discovered defect. |
| Anchor gaming | A quote that straddles a changed word to attack the sentence around it. | Overlap with a changed token at the cited line; 12-character minimum. | Semantic fit of finding to anchor is not checked. |
| Reviser id gaming | A valid blocking id on an unrelated edit passes `fixcheck`. | Every such hunk is surfaced to the next review with its claimed owner. | Gaming adds surface, not hidden text. |
| Under-fixing | A strict gate pushes revisers to `declined`; a declined real blocker stays `open`. | `withdrawn` only after `declined`, counted in the proxy, forces `scoped`. | Counts move from "new" to "open". |
| Fail-closed stalls | A permission prompt, a script bug, a missing install, a wrong directory. | Pre-run gate; every stop names its reason; no fallback to a plain review. | A stall costs a replicate. |
| Format tax on reviewers | The machine block and anchors are new work. | One repair turn (read-only dry run), then degrade; review-1 comparability label. | Measured, not prevented. |
| Diff noise | A rewrite touching most of the file turns the surface back into the whole document. | `coverage:` printed, with a warning above 50%. | No move detection in v1. |

Known gaps recorded during implementation (non-blocking review notes): a `via` anchor on the unchanged words of a line inside another hunk is accepted (the check is token level); an empty lock file is treated as stale.

## 4. Measurement plan

S1 exactly as in the earlier arms: the Orca worker-contract spec (57,763 bytes), base commit `2cb683f5`, three reviews and two fix cycles, two replicates in fresh worktrees, compared with the control and Arm B. The review briefs are the verbatim S1 briefs with only the command token substituted and the `--diffgate-dir` and `--expect-round` arguments added; the review-3 brief keeps its sentence "any finding of any severity is FAIL" (owner decision; the script's verdict is reported beside it). The two fix-cycle reviser briefs gain one line; the T10 reviser brief is unchanged. The coordinator inserts the `begin`, `check` and `fixcheck` steps, and a mandatory blindness audit (a fresh plain `/sc:spec-panel` review of the final document) runs for every arm. The brief kit is `.dev/brainstorms/346-diffgate/briefs/` and the install note is `.dev/brainstorms/346-diffgate/INSTALL.md`.

Bar metric `R3-proxy-all`: CRITICAL or MAJOR labels on the findings first raised in review 3 (deferred, demoted and over-`via`-cap included) and on prior blocking findings marked `open`, `regressed` or `withdrawn` in review 3, plus, by the owner ruling, every critical or major finding the script deferred, demoted or withdrew at any review from 1 to 3; each id counted once. For the treatment it is `proxy_all` in `<dir>/result-r3.json`. An early terminal review (a PASS at review 1 or 2, scoped or clean) is scored from that review's own `proxy_all` in `result-r<N>.json`, spec growth is carried forward, `result-r3.json` is never fabricated, and the run is a clean pass only if that `proxy_all` is 0. The control and Arm B are recomputed by hand with the same function.

Bar: `R3-proxy-all` 3 or fewer in both replicates (or a clean PASS sooner) and growth after fix cycle 2 at or under 44.4%. Prediction: likely not met on the count (fixes of blocking findings still introduce blockers on the fixed text), likely met on growth. Falsifiers F1 to F6 and the three pre-registered result classes are in SPEC section 5 and 6.
