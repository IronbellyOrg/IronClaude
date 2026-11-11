# Fix log: fix-only pass (owner decision 2026-11-08)

Scope: the 5 blocking findings of `review-adversarial-3.json`, fixed by text edit only. No review, validation or adversarial pass was run after these edits; the step-5 final review re-checks them. Orca run run_93bfa00cae2b, task task_ce88dd94e4d5.

Paths below are relative to this folder (`EXPERIENCE.md`, `DESIGN.md`) or to `_bmad-output/specs/spec-orca-observer/` (spec files) and `_bmad-output/planning-artifacts/orca-observer/prd.md` (PRD).

## Finding 1: fixture header string

Result: **fixed**. Finding confirmed: rendering-rules.md:17 says "Fixture mode always reads `SYNTHETIC FIXTURE <variant>, not Orca data`"; the T50 marking "synthetic fixture, not live evidence" is a per-render R0 marking (acceptance-tests.md:44, rendering-rules.md:5).

| Before | After | Change |
|---|---|---|
| EXPERIENCE.md:64 | EXPERIENCE.md:64 | Screen 0: header string quoted from rendering-rules.md:17; T50 marking kept as a separate per-render marking. |
| EXPERIENCE.md:215 | EXPERIENCE.md:215 | Header component: same split, "quoted exactly". |
| EXPERIENCE.md:296 | EXPERIENCE.md:298 | Fixture view state: same split. |
| EXPERIENCE.md:490 | EXPERIENCE.md:492 | UJ R0 step 2: same split. |
| DESIGN.md:121 | DESIGN.md:121 | warn colour row: badge text replaced by both strings, each cited. |

Proof (`B=/tmp/ux409-before` is the pre-edit copy, made before any edit and removed after this pass; `U` is this folder):
```
$ grep -c 'not live evidence (<variant>)' $U/EXPERIENCE.md $U/DESIGN.md
EXPERIENCE.md:0
DESIGN.md:0
$ grep -n -o 'SYNTHETIC FIXTURE <variant>, not Orca data' $U/EXPERIENCE.md $U/DESIGN.md
EXPERIENCE.md:64:SYNTHETIC FIXTURE <variant>, not Orca data
EXPERIENCE.md:215:SYNTHETIC FIXTURE <variant>, not Orca data
EXPERIENCE.md:298:SYNTHETIC FIXTURE <variant>, not Orca data
EXPERIENCE.md:492:SYNTHETIC FIXTURE <variant>, not Orca data
DESIGN.md:121:SYNTHETIC FIXTURE <variant>, not Orca data
```

## Finding 2: false claim at EXPERIENCE.md:54

Result: **fixed (finding partly correct)**. The old sentence was "The spec and PRD never mention the PLAN.md cockpit or the built layout." The "built layout" half is false: rendering-rules.md:8 records that the prototype's 116-column collapse claim does not match the built prototype (X-001), and rendering-rules.md:85 discusses the built Signal Bridge (`_request` in `signal_bridge`, its 116- and 80-column builds drop SIGNALS). The "PLAN.md cockpit" half is true: `grep -n -i "cockpit\|PLAN.md"` over the spec folder and prd.md returns no lines, so that half is kept. UX-OQ-1 is kept unchanged.

Before EXPERIENCE.md:54, after EXPERIENCE.md:54. Sources: rendering-rules.md:8, :85.

Proof:
```
$ grep -c 'never mention the PLAN.md cockpit or the built layout' $U/EXPERIENCE.md
0
$ grep -n -o 'records that the built layout departs from it' $U/EXPERIENCE.md
54:records that the built layout departs from it
$ grep -n -i "cockpit\|PLAN.md" <spec folder>/*.md prd.md
(no output)
```

## Finding 3: placement of `cycle overran (Ns)`

Result: **fixed**. Note: the dispatch brief worded this finding the other way round ("placed on the strip, but the source puts it on the status line"). The sources say the strip: adapter-contract.md:26 "An overrunning call is killed and reaped; the strip shows `cycle overran (Ns)`", and T40 (acceptance-tests.md:34) "overrunning call killed and strip shows `cycle overran (Ns)`". The UX spec had it on the status line, so it was moved to the freshness strip, as review-adversarial-3.json and handoff-step3.md:24 state.

| Before | After | Change |
|---|---|---|
| EXPERIENCE.md:292 | EXPERIENCE.md:293 | Cycle overrun view state now reads "in the freshness strip", cites adapter-contract.md:26 and T40. |
| (none) | EXPERIENCE.md:221 | Freshness strip component: new bullet saying the strip shows `cycle overran (Ns)`, same citations. |

Proof:
```
$ grep -c 'overran (Ns)` on the status line' $U/EXPERIENCE.md
0
$ grep -n -o 'cycle overran (Ns)` in the freshness strip\|the strip shows `cycle overran (Ns)`' $U/EXPERIENCE.md
221:the strip shows `cycle overran (Ns)`
293:cycle overran (Ns)` in the freshness strip
```

## Finding 4: missing test-pinned state strings

Result: **fixed**. All six strings in the finding were confirmed in the sources. The brief named three of them; the finding's own fix also lists `reported T (page k)` and `one Run only`, which the sources state, so both were added too.

| String | Source | Before | After |
|---|---|---|---|
| `FAILED (shape)`, last good snapshot kept | T32, acceptance-tests.md:21 | failed row EXPERIENCE.md:280 | EXPERIENCE.md:281 (source column adds acceptance-tests.md:21) |
| `reported unknown` (absent `page.total`) | T32, acceptance-tests.md:21 | partial row EXPERIENCE.md:278 | EXPERIENCE.md:279 |
| `reported T (page k)` | rendering-rules.md:55 | partial row EXPERIENCE.md:278 | EXPERIENCE.md:279 |
| `order unknown`, `conflict (time went back)` | T22, acceptance-tests.md:18 | (absent) | new view-state row "Row order flags", EXPERIENCE.md:296 |
| `one Run only` after `bound` scope | adapter-contract.md:63; K4, prd.md:363 | header line 1, EXPERIENCE.md:80 | EXPERIENCE.md:80 |

Proof (counts in the pre-edit copy and now; `reported unknown` was already in the PROPOSED loading state at line 287):
```
$ for s in ...; do grep -cF "$s" $B/EXPERIENCE.md; grep -cF "$s" $U/EXPERIENCE.md; grep -nF "$s" $U/EXPERIENCE.md; done
FAILED (shape): before=0 after=1 lines=281
reported unknown: before=1 after=2 lines=279 287
order unknown: before=0 after=1 lines=296
conflict (time went back): before=0 after=1 lines=296
reported T (page k): before=0 after=1 lines=279
one Run only: before=0 after=1 lines=80
```

## Finding 5: never-drop list labelled "spec"

Result: **fixed**. Finding confirmed: rendering-rules.md:19 says the COUNTS strip "is a minimum row and is never dropped"; rendering-rules.md:13 makes coverage, scope and `PARTIAL` minimum content. No spec line says header line 1, the freshness strip, the gap notice or the footer survive height pressure (`grep -n -i "never dropped\|never drop\|minimum row"` over the spec and PRD finds only rendering-rules.md:13 and :19). rendering-rules.md:31 places the gap notice "above the ledger, at every width", which is a width rule, not a drop rule; that is stated in the item.

Before EXPERIENCE.md:135-142 (heading "(spec)"), after EXPERIENCE.md:135-142: the heading states what the spec fixes, the COUNTS strip item cites rendering-rules.md:19, the other four items are labelled PROPOSED, and the coverage sentence cites rendering-rules.md:13.

Proof:
```
$ grep -c 'Rows that never drop\*\* (spec)' $U/EXPERIENCE.md
0
$ grep -n 'Rows that never drop\|(PROPOSED' $U/EXPERIENCE.md   (first lines)
135:**Rows that never drop.** The spec fixes only the COUNTS strip as never dropped (rendering-rules.md:19) an...
136:- header line 1 (PROPOSED);
137:- the freshness strip (PROPOSED);
139:- the gap notice (PROPOSED; the spec places it above the ledger at every width, rendering-rules.md:31, but...
140:- the footer, carrying `shown x/y | collected n / reported T` (PROPOSED).
```

## All changed hunks

```
$ diff /tmp/ux409-before/EXPERIENCE.md $U/EXPERIENCE.md | grep '^[0-9]'
54c54  64c64  80c80  135,140c135,140  142c142  215c215  220a221  278c279  280c281  292c293  294a296  296c298  490c492
$ diff /tmp/ux409-before/DESIGN.md $U/DESIGN.md | grep '^[0-9]'
121c121
```

## Not changed, still open

- The 8 minor findings of review-adversarial-3.json (inspector lines from adapter-contract.md:38/:62, B's 80-column invariant lines and R0 degraded strings, the DESIGN.md:193 citation, the NO_COLOR wording, the loading-state `collected 0`, the historical-evidence rule, inspector `m`/`e` not marked PROPOSED, the `OQ-B/C` ID) were not touched.
- UX-OQ-1 to UX-OQ-8 and the PRD's OQ/OI items are unchanged and unresolved.
- Contrast ratios, the palette and the per-call timeout (OI-1) remain UNVERIFIED.
- Both spines remain `status: draft`. These 5 fixes were made by edit and were NOT re-reviewed.

## Step 5 fix cycle 1 (final-review graded BLOCKING findings; edits only, NOT re-reviewed)

- UX-01: EXPERIENCE.md:257-258 inspector adds `n unrecognised keys` and the per-observer-process caps statement (adapter-contract.md:38, :62).
- UX-02: EXPERIENCE.md:328 PROPOSED help text = `superclaude observe --help`, carrying the rendering-rules.md:52 sentence and the caps sentence (adapter-contract.md:62).
- UX-03: EXPERIENCE.md:177 B 80-115 row keeps the two invariant lines (rendering-rules.md:42).
- UX-04: EXPERIENCE.md:240 historical evidence linked to a shown item is never hidden (rendering-rules.md:22).
- UX-05: EXPERIENCE.md:52 SIGNALS only in the 160-column Signal Bridge export (rendering-rules.md:85).
- UX-06: EXPERIENCE.md:82, :84 and DESIGN.md:205 filter count moved from the status line to the COUNTS strip beside source counts (rendering-rules.md:56).
- UX-07: EXPERIENCE.md:80 `as of <local time of last good poll>`, HH:MM:SS as display format (rendering-rules.md:17).
- UX-08: EXPERIENCE.md:251, DESIGN.md:173, :210 inspector replaces the ledger area only; header, freshness and COUNTS strips stay (rendering-rules.md:13, :19).
- UX-09: DESIGN.md:195 `--ascii` `?` replacement limited to ledger cells; inspector and export use `\uXXXX` escapes (PROPOSED; rendering-rules.md:24-25).
- UX-10: EXPERIENCE.md:253 PROPOSED fixed indent marker on multi-line value continuation lines (adapter-contract.md:51).
- XDOC-04: EXPERIENCE.md:243, :535 default now: each ledger row names `resource.worktreeId` per T20 (acceptance-tests.md:17); UX-OQ-8 kept open on placement and width behaviour.

## Step 5 fix cycle 2 (final-review graded BLOCKING findings; edits only, NOT re-reviewed)

- XDOC-04: EXPERIENCE.md:242, :534 T20 (acceptance-tests.md:29) asserts the shared `resource.worktreeId` through the inspector (`unknown (absent in source)`); the `worktree unknown` row line removed; PROPOSED default inspector and export only; UX-OQ-8 kept open on whether the row names it.
- NEW-3: EXPERIENCE.md:184, :294 label now `worker-list NOT AVAILABLE (no Orca CLI validated)` (adapter-contract.md:10).
- NEW-5: EXPERIENCE.md:530 UX-OQ-4 row describes the PROPOSED `--snapshot PATH` option, default `~/.local/state/superclaude/observe/`, owner-only 0600, atomic replace each live cycle (snapshot-export-schema.md:16); UX-OQ-4 kept open.
