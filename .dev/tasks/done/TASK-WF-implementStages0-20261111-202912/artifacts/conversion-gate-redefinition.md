# Conversion gate (T-9 / O-7) redefined

Decision: the owner, 2026-11-12 ("In terms of the conversion gate it should be redefined based on the findings"). This file records the new wording. `pilot-design.md` (T-9, Stage 0a table, Stage 0 exit item 2) points here. The plan file and its ledger are archived and unchanged.

## What the old gate said and what the findings show

Old T-9 (`src:408`, `src:542`, `src:555`): at least 90% of recorded findings convert to findings-v2 with an unambiguous `(path, line)`. Result on the 43 recorded card directories: 479 / 712 = 67.28% (`stage0a-report.md`, "Conversion share").

The unconverted 233 units by cause (same report):

| Cause | Units | Can a parser fix it? |
|---|---:|---|
| the finding names no `path:line` at all | 104 | No. The line was never written. |
| no plan path / no spec path | 17 | No. The reference was never written. |
| unlisted card (no table, or not a YAML list of findings) | 23 | Only with a new reader per layout; not built. |
| citation path not repo-relative | 31 | Yes, in principle (strip a root prefix); not done, so it counts as a miss. |
| "citations must be a list of N to N" | 54 | Unclear; that is the checker's own rule and the report does not say why each card broke it. UNVERIFIED. |
| severity not CRITICAL, MAJOR or MINOR | 4 | Yes, in principle. |

At least 121 of 233 misses (52%, the first two rows) are findings whose reviewer never wrote a line or a plan or spec path. Those cards were written under briefs that never asked for line-level citations, so the 67.28% measures how the history was written, not how well the parser works. Gating on it cannot tell a good parser from a bad one and can never pass, because the recorded cards are fixed.

## New definition

1. **Recorded cards: baseline, no gate.** The 67.28% and the cause table stay in `stage0a-report.md` as the descriptive baseline. Nothing is blocked by them.
2. **T-9 gate: cards written under the findings-v2 reviewer brief.** The shadow-mode reviewer brief ends with the instruction to write a fenced findings-v2 block (`refs/reviewer-spec.md:39`, the shadow exception; `SKILL.md` section 4.3a). The gate passes when at least 90% of the findings in those cards carry an unambiguous `(path, line)` that the findings-v2 checker accepts. The 90% value is unchanged; only the population changes.
3. **What blocks.** Before the gate is measured, findings-v2 stays dormant: the shadow mode keeps the legacy writers authoritative (Contract 1.8.0 is unchanged). Stage 3 entry needs this gate passed together with the first measurement (`src:411`). A fail does not change the shipped Stages 0-2 and does not stop the pilot; it blocks promoting findings-v2 from shadow to authoritative.

## How it is measured

- **Card level, available now:** `scripts/reflect_shadow_exit.py` prints the mean `findings_block_compliance_rate` over the shadow runs (the share of reviewer cards with a valid findings-v2 block). It reports the value and does not gate on it; the operator reads it against 0.90.
- **Finding level, the gate itself:** a script that runs the findings-v2 checker over every block of the shadow runs and prints findings with a valid `(path, line)` over all findings is NOT BUILT. Until it exists, the card-level rate is the available proxy and is labelled as a proxy in the report. Whether `scripts/reflect_stage0a_replay.py` (`--root <dir>`) reads findings-v2 blocks directly, rather than only the legacy card shapes, is UNVERIFIED.
- **Population and timing:** the 20 shadow runs of the Stage 2 exit, which need `superclaude install`, the owner's spend approval and about 1.4M tokens. Pilot arm C is the development-build panel and its cards can be added once the pilot runs.

## Stage 0 exit effect

Item 2 changes from FAIL to "redefined, not yet measured". The Stage 0 exit stays PENDING (item 1 still needs the owner's hand labels, item 2 needs the shadow-run measurement).
