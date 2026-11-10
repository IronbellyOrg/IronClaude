# QA qualitative verification of F12-F20 (A.10.5 review 2)

**Reviewer:** rf-qa-qualitative agent; report transcribed by the orchestrator (the agent's harness forbids writing report files; content is its inline return).
**Date:** 2026-11-07

Self-Audit (reviewer): did not rely on the structural verdict; read task-file lines 128-136, 169, 193, 218, 230, 234, 246, 250, 279, 304, 365, 387, 391, 393, 433, 488 in full plus `bmad-cli.js:31-52` and the `install.js` flags. Counts (91 items; 61 agent-side and 61 executor-side tails; 8 CLI rule copies) pass structurally but hide findings 1 and 2.

## Blocking (IMPORTANT)
1. F12 (136(3); items 193, 279, 304, 365, 234, 393): research, synthesis, assembler and fix agents have no route beyond .md or .json. Delegated agents may refuse .md files; a respawn with the same prompt repeats the refusal, then the task HALTs, making about 12 spawns and up to 10 fix agents single points of failure. Minimum fix: research, synthesis and assembler agents return the full file as their final message (unnamed agents are not truncated, so no 1500-char cap); the executor writes it with `cat`, not by retyping; fix agents return exact old/new edit pairs which the executor applies; state that a .json holds raw markdown and the executor decodes it if wrapped.
2. (136(3); items 387, 421, 423): the 1500-character inline cap with a mandatory Self-Audit truncates QA findings (N at least 5 per lens; Section 8 reproduction rows and the Web-source check table cannot fit). Line 423 says re-run once but not what then. Fix: allow about 4000 characters, blocking findings first, severity counts; HALT after the re-run.
3. F16 (items 246, 336, 401, 431, 461, 488): the Severity changes ledger is written but never read, so a gate can pass on orchestrator downgrades alone. Fix: each decision file records the count of downgraded reporter CRITICAL/IMPORTANT findings, and 488 lists them for the user.

## Minor
Gap-researcher `.addendum.json` (234, 254) has no owner to merge it into the research .md; line 304 tells the agent to read a task-file section with no offset (a 541 KB Read fails): point it at lines 159-165; the "Transcribed by orchestrator" first line displaces the report title, tell lenses to ignore it; the 279 tail ("web unavailable, mark complete") is ambiguous against the missing-file HALT.

## Passes
F13 (line 169 forbids whole-file reads; Read offset 193 limit 1 returns the whole line); F14 consistent and the flags exist; F15, F17-F20 implemented in items, not only worded; gate counts 3, 3, 7, 3, 3, one fix agent per gate, max 2 cycles; HALT rules do not conflict with the `/task` no-pause rule (`SKILL.md:120`).

VERDICT: FAIL
