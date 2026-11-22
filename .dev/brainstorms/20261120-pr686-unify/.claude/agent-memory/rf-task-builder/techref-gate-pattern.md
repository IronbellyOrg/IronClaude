---
name: techref-gate-pattern
description: How a tech-reference MDTM task file with 4 standard-intensity QA gates was encoded (fixed items per gate, SKIPPED stubs, halt guards, dynamic gap-fill markers)
metadata:
  type: reference
---

Pattern used for TASK-TECHREF-issue-pipeline-20261120-040158 (83 items, 7 phases, about 2,360 lines):

- Append with an end-of-file marker line (`<!-- BUILDER-APPEND-MARKER -->`) and one Edit per item or small group; the Edit hook demands a Read of the file first in the session.
- Each gate has a FIXED item list: lens agents, consolidation, fix cycle 1, verification 1 (2 items), decision item, consolidation 2, fix 2, verification 2 (2 items), final verdict. Cycle-2 items write a one-line `SKIPPED:` file when the decision file does not say `CYCLE-2-REQUIRED`, so the item list never changes.
- Decision items order the checks: regression (byte-exact halt line), monotonicity (`[HALT-MONOTONICITY] |F|=<n>`), hard cap, proceed. HALT = frontmatter Blocked + SendMessage to `team-lead` + stop.
- Gate 1 "fix" is gap-filling research whose count is unknown: use DYNAMIC CONTENT markers plus an embedded item template; set `task_type: dynamic`.
- Prompts go in a fenced block indented under the item; cycle-2 items reuse the cycle-1 block with listed substitutions.
- Build request may conflict with the template (I22 partitioning >10 files vs BUILD-REQUEST partition of 6 synth files): BUILD-REQUEST wins; record in Builder Notes.
