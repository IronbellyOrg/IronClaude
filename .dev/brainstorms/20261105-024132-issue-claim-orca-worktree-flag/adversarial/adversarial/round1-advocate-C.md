# Round 1 Advocate Statement: Variant C (QA)

## Position summary

Variant C is the strongest regression-safety and traceability spec: byte-identical unflagged behavior as an observed acceptance criterion, a 15-row edge table each mapped to a test, and a re-claim fast path that works with the Orca daemon down. Its Orca interaction (inline commands, omitted `--repo`, one warn code) is weaker than A's script seam, it carries two verified factual errors (X-001, X-002) and the verified `cp -r` nesting defect (X-004), plus a renamed-branch re-check bug I found in my own text. The best merge takes A's seam and repo resolution, B's status field, re-list and minimal file surface, and C's test mapping and record fast path.

## Steelman of Variant A

A's best idea is the single seam: every Orca call behind `scripts/orca_worktree.py` (A FR-5, U-001). That turns the riskiest logic (argv construction, dedup, JSON parsing) from LLM-improvised prose into deterministic code tested in CI with a fake `orca` on PATH; it is the only variant whose reuse and failure logic executes in pytest at all. A is alone on 120 s timeouts (U-004) and a disk-existence stale check, and its `--repo path:<main>` via `--git-common-dir` was verified from a linked worktree (U-003). Its `--comment` marker is a stable key: verified in `orca worktree create --help` ("Comment stored in Orca metadata"), not a link flag.

## Steelman of Variant B

B is the disciplined minimalist: no new file, so `test_all_five_refs_exist` (tests/skills/test_issue_protocol.py:165) and the inventory pins stay green unedited (U-006). Never overwriting protects user notes (U-007). Re-listing after create instead of trusting the unverified create JSON (U-009) is the most robust path source. B alone named the upstream-projectId risk (U-008); I verified it live: every IronClaude row in `orca worktree list` carries `projectId: github:superclaude-org/superclaude_framework`.

## Strengths claimed

1. Strongest no-regression gate: unflagged output and `<D>` files byte-identical is acceptance criterion 1 (C s7), observed by diffing two runs; A FR-3 and B FR-1 assert equivalence, C makes it pass/fail.
2. Traceability: all 15 edge cases map to T1-T6 (C s6), so no edge is untested by construction (U-011).
3. Re-claim works with the daemon down: record plus local `git rev-parse` (C s5 step 1) reuses with no Orca call; A creates nothing when listing fails; B skips the same way.
4. Forbidden-flag regex pinned in CI (C T2), cheaper and stricter than review.
5. Honesty: R5 flags the B2 reading for debate; R1-R3 label every UNVERIFIED item with its verification step.

## Weaknesses identified in A and B

1. A breaks pinned test surface: a sixth `refs/*.md` fails `test_all_five_refs_exist` and the two-way inventory (tests/skills/test_issue_protocol.py:165, 136).
2. A's slug name needs code and rests on an unverified prefix rule; live rows are mixed (`ironbelly/bare-python-hook-357` prefixed, `issue-305-*` not).
3. A's list-failure skip means a transient Orca hiccup yields no worktree even when one exists (A s6).
4. Both mishandle B2 wording (X-003): A stretches it into "decision B16" while claiming it holds; B's "literally true" is overstated against docs/designs/sc-issue-command.md:27.
5. B's never-overwrite leaves a stale `next-steps.md` after a re-claim regenerates it (B 2.4); the user then runs outdated commands.
6. B's regex misses hand-made issue worktrees (A-004): verified rows `issue-305-pr-submit-conflicts`, `issue-315-ccsession-name-prompt`, `issue-330-ponytail-plugin`; `(^|/)issue-<N>(-[0-9]+)?$` matches none, so B creates duplicates for those issues.

## Concessions about Variant C

1. X-001 conceded: claim.md:90 step 4 is "Print the `next-steps.md` path and STOP"; a later Wave 7 never runs unless step 4 changes. "Wave 6 stays byte-identical" (C s5) contradicts itself; A/B's conditional rewrite is right.
2. X-002 conceded: verified 8 of 47 command files carry `version:` (brainstorm, pr-submit, reflect, task, tasklist, init-lite, cli-portify, swarm-wizard); C Q7's "no primitive carries a version marker" is factually wrong.
3. X-004 conceded: on reuse, `cp -r <D> <wt>/.dev/issues/<N>/` with the destination existing nests at `.dev/issues/<N>/<N>/`; E5's required re-copy triggers it.
4. Self-found bug: after a renamed create (E7) the record holds `issue-<N>-2`, but step 1 compares rev-parse output to literal `issue-<N>` (C s5), so the next re-claim misses record and exact list match and creates `issue-<N>-3`.
5. Omitted `--repo` leans on inference (C E11 admits it); `--setup run` forces repo hooks for an UNVERIFIED benefit (R2); one warn code cannot route remedies; one contract field loses the created/reused distinction my own T6 checks.

## Per-point verdicts

| Point | Winner | Confidence | Evidence |
|---|---|---|---|
| S-001 | A | 75% | Fake-orca tests exist only with the seam (U-001) |
| S-002 | A=B | 90% | Step 4 must become conditional; claim.md:90 verified |
| S-003 | B | 55% | Code table enumerates codes for pinning; cosmetic |
| S-004 | C | 85% | 15 rows each mapped to a test ID (U-011) |
| C-001 | B | 75% | `--branch` documented to bypass prefix; exact greppable key |
| C-002 | A | 80% | `--git-common-dir` main resolution verified (U-003) |
| C-003 | A | 70% | Omit; repo policy decides; C forces hooks for UNVERIFIED gain |
| C-004 | A | 70% | Comment marker survives suffix and title edits |
| C-005 | B | 65% | Create-nothing on ambiguity is the safe branch |
| C-006 | A | 60% | Only A checks disk existence; C's E8 misses row-without-disk |
| C-007 | A | 55% | Overwrite keeps next-steps fresh; B safer for notes; C broken |
| C-008 | B | 70% | Re-list never trusts create JSON (U-009); C has no fallback |
| C-009 | B | 70% | Path+status machine-checkable; C's T6 needs the status field |
| C-010 | B | 60% | Four codes route remedies; C's one cannot |
| C-011 | B | 75% | `version: "1.1.0"` matches the verified 8-command convention |
| C-012 | A | 75% | Only variant executing Orca logic in CI |
| C-013 | A | 90% | Only variant with timeouts |
| C-014 | tie | 60% | All three fire after comments post; no observable difference |
| C-015 | A | 55% | Explicit decision row beats "unchanged"; graft C's R5 |
| C-016 | B | 60% | Suffix-tolerant regex survives rename; C's re-check buggy |
| X-001 | A=B | 95% | claim.md:90 verified; C wrong |
| X-002 | A=B | 95% | 8 versioned commands verified; C wrong |
| X-003 | A | 65% | A at least amends the doc; B overstates; C's honesty grafted |
| X-004 | B | 85% | Skip-existing avoids nesting; A fixable in script; C broken |

## Shared assumption responses

- A-001 QUALIFY: B2's text (design line 27) says stop after writing next-steps.md; a worktree is infrastructure, not starting the chain, but the safe course is A's explicit amendment, conditioned on C's R5 confirmation.
- A-002 REJECT: `/sc:issue` installs to other projects where Orca or registration may be absent; all three already fail open on missing orca, but the wrong-repo inference case (verified upstream projectId rows) needs C's E11 remedy line.
- A-003 QUALIFY: Wave 1 runs `git fetch origin` (claim.md:28) so freshness normally holds; a failed fetch leaves a stale base that create silently uses; name it in the edge table.
- A-004 REJECT: three hand-made issue worktrees verified live; B and C miss them and duplicate; A's path-basename fallback is required.
- A-005 QUALIFY: `.gitignore` has no `.dev/issues/` rule (verified), so the copy is untracked but visible; `git add .` stages it; keep B's untracked warning and D24.

## Proposed merged design

- Wave 7 procedure in `refs/claim.md` (B/C: five-refs pin stays green); all Orca calls and the copy in A's new `scripts/orca_worktree.py` (the inventory globs `scripts/*.py`, so no pinned test breaks; verified the pin covers only `refs/*.md`).
- Boolean claim-only `--worktree`; `E-CLAIM-ONLY-FLAG`; conditional Wave 6 step 4 (A/B, X-001 conceded).
- Create args: `--name issue-<N> --branch issue-<N>` (B/C), `--repo path:<main>` via `--git-common-dir` (A), `--base-branch origin/<B>`, `--no-parent`, `--comment "sc:issue <R>#<N>"` (A); no `--setup`, no link flags.
- Dedup order: C's `worktree.json` + rev-parse fast path (daemon-down reuse), then comment-marker match (A), then path basename `^issue-<N>(-|$)` (A, fixes A-004), then B's suffix-tolerant regex; several matches: create nothing (B); stale disk path: detect (A) then create fresh (C's E8 outcome).
- Path from re-list after create (B). Copy in the script with correct semantics, overwriting generated files (A's intent; avoids C's X-004), plus B's untracked-files print.
- Contract: `worktree_path`, `worktree_status`, `worktree_warning` (B + A). Warn codes at B's granularity. 120 s timeouts (A).
- `version: "1.1.0"` in issue.md (B, X-002 conceded). Design doc: A's explicit decision row recording the B2 reading this debate confirms (resolving C's R5).
- Tests: A's fake-orca suite as the core; C's E1-E15 each mapped to a fake-orca case, static pin, or observed run; C's byte-identical unflagged-output diff and forbidden-flag regex as acceptance gates; B's no-new-ref property preserved.
