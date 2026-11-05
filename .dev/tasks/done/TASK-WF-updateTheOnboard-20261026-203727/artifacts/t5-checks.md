# Task 5 checks (slides 1-4 and 11-14), 2026-10-26T21:43Z

Deck = `docs/onboarding/ironclaude-onboarding.html` (line numbers after the Task 5 edits). Guide = `src/superclaude/core/HOW-WE-WORK.md` (master adaa28d9).

| Slide / item | Claim | Source checked | Result |
|---|---|---|---|
| 1 (deck:179-183) | `superclaude install` copies the guide to `~/.claude/HOW-WE-WORK.md`; keep it open; the guide is the authority | guide:3 | match, no change |
| 2 (deck:189-190) | five runs, five versions; "about 70%" shown as a meeting opinion | transcript T119-121, T221-223, T576 (spec.md:194) | match, attributed story, no change |
| D1 (deck:192-230) | one prompt fans out to five results; two agents plus a debate merge the best parts | transcript T221-223 ("five different versions"; "two different agents do the same thing ... adversarial debate"), T576 ("five different variations"); "merged" from spec.md:224 ("a debate that merges the best parts") and guide:157 (`/sc:adversarial` stops at "comparison and merged artifacts"), not from the transcript | match as an attributed explanation; no command, flag or rule in D1 |
| 3 rule card (deck:252-261) | write it down; let a skill finish; do not repeat its checks; never turn off a quality check; read a plan first; do only what was asked | guide:277-283 | every rule present, no change |
| 3 other cards (deck:238-251) | meeting stories (tokens, 90%); `/sc:adversarial` runs the debate; `/sc:reflect` brings in several reviewers | transcript (spec.md:195); guide:157-158 (adversarial); `src/superclaude/commands/reflect.md:145` (Tier 2: 2-3 reviewers on different model classes when calibrated confidence is below threshold or `--depth deep`) | match, no change (reflect source added after the Task 5 review) |
| 4 / D2 (deck:268-311) | command 214 lines; skill 711 lines | `./artifacts/t5-wc.log` (wc -l 214 and 711) | match, no change |
| 11 (deck:532-535) | work saved to files, most under `.dev/`; `superclaude update` overwrites, no backup, re-copies skill folders; ccsession resume; same command on the work's files | guide:3, :227-235, :277 | match |
| 11 (deck:535) | `/sc:save` and `/sc:load` | guide:237 "store and load Serena project memory" | reworded to "Serena project memory (project notes)" |
| 13 trap (deck:573) | level 4 only on explicit MDTM selection or exceptional program need; existing MDTM task straight to `/task`; file count, sessions, spec, risk, auditability, drift or resume alone never select it | guide:18, :24, :296 | reworded (existing task only to `/task`; full guide:296 list) |
| 13 eyebrow (deck:557) | was "section 5, 3.12 and section 4" | slide now uses sections 1 (trap), 3.12 (`/sc:save` trap) and 5 (look-alikes) | changed to "sections 1, 3.12 and 5" |
| 13 look-alikes (deck:563-569) | seven pairs | guide:295-301 | all seven pairs present in section 5, no change |
| 13 `/sc:save` trap | not a way to resume | guide:237 | match |
| 13 story (deck:574) | many reviewer subagents start in the background | meeting story (attributed) | kept |
| 14 recommend card | `/sc:recommend` picks the command and writes a ready-to-paste prompt | guide:284; `src/superclaude/commands/recommend.md` description | match |
| 14 `/sc:help` card (deck:583) | lists installed commands and skills and shows the six levels | `src/superclaude/commands/help.md:3` ("show the six process levels"), :65-73 (prints the level table) | match, kept |
| 14 lead card | ask your lead; alone, read "your lead" as yourself | guide:284, :287 | match |
| 12 | issues #289 and #290 kept by number | FR-ONB.6 | unchanged |
