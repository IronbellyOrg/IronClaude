# Q10: may the sweep ever read Orca's pending questions, or is that the observer's job alone

## The question, verbatim from the spec row

Source: `merged-requirements.md:537` (section 3, "Owner decisions").

> | Q10 | May the sweep read Orca messages with `check --all --types question`? | Observer's alone for now; correct the sweep's two sentences | PLAN INFERENCE: same as recommended; `check` stays forbidden in NFR-014 | SW-07 | W3 |

Original wording (ADJ Part 7, `alignment-findings-adjudicated.md:780`): "May the sweep ever read Orca messages with `check --all --types question`, or is that the observer's alone?"

## Spec's recommended answer

"Observer's alone for now; correct the sweep's two sentences (Part 2.2 action 6)" (ADJ:780; `merged-requirements.md:537`).

## Default if unanswered

PLAN INFERENCE (the spec's derivation): the same as recommended; `check` stays forbidden in NFR-014, the owner-signed allow-list of the exact Orca commands the sweep may run (`merged-requirements.md:537`; ADJ glossary line 84).

## What it gates (work items, in words)

- SW-07, post-merge sweep wording fixes: among other edits, `report.py:199,534` carry exactly: "This command reads no messages. A plain `check` consumes them. Whether `check --all --types question` consumes on a live Run is not established." (R2-V5 5.8), with the tests pinning those strings updated in the same PR; opened by the PR session after PR #539 merges (`merged-requirements.md:196`).
- Wave W3 (the batch after the #539 merge).

## Facts the question depends on

| Fact | Source |
|---|---|
| The sweep's allow-list has 10 templates over 7 verbs and no `check` verb | `src/superclaude/cli/sweep/probes.py:49-60` (read 2026-11-14) |
| The sweep's report says "Messages coverage: partial" (line 199) and "Messages coverage is partial: pending questions cannot be read without consuming them" (lines 534-535) | `src/superclaude/cli/sweep/report.py:199`, `:534-535` (read 2026-11-14); a test pins "Messages coverage: partial" (`tests/sweep/test_report.py:590`) |
| Whether `check --all --types question` consumes (removes) messages on a live coordinator Run is unproven both ways (61 percent); Orca's own help says `--all` "does not mark read"; a plain `check` consumes | ADJ X-016 (line 333), glossary line 97; `merged-requirements.md:239` |
| The observer reads questions with `orchestration check --all --types question --run <id> --json` behind its switched-off guard | `merged-requirements.md:233` |
| If the seeded consumption test (OB-03) shows consumption, Q10 "stays 'observer's alone' or becomes 'neither'" | `merged-requirements.md:261`, `:1000` |
| The sweep's caution stays and its two lines are reworded to state only what is established; this replaces a withdrawn rewording (V5 O-05) that claimed non-consumption | ADJ Part 2.2 action 6 (line 204 area), X-016 decision row (line 813) |
| Only the terminal holding a Run can read its questions (gate test Q-1 failed); a sweep runs in the coordinator's own session | ADJ INV-024 (line 465); glossary lines 80-81 |
| A coordinator sweeps at most once per 5 minutes and the sweep recommends nothing (WC-16) | ADJ glossary line 81 |
| Q1's risk choice does not authorize arbitrary allow-list edits (NFR-014) | `merged-requirements.md:571` |
