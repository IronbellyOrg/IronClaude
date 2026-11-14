# Step 1.15 checks (item 11.3)

Run 2026-11-12 on `src/superclaude/skills/sc-sweep-protocol/SKILL.md`.

## Check 1: no `src/superclaude` substring (must print 0)

Command: `grep -c 'src/superclaude' src/superclaude/skills/sc-sweep-protocol/SKILL.md`
```text
0
(exit 1)
```

## Check 2: the allowed-tools literal (must print one line)

Command: `grep -n '^allowed-tools: Bash(superclaude sweep run:\*), Bash(uv run --frozen --no-sync superclaude sweep run:\*), Read$' src/superclaude/skills/sc-sweep-protocol/SKILL.md`
```text
4:allowed-tools: Bash(superclaude sweep run:*), Bash(uv run --frozen --no-sync superclaude sweep run:*), Read
(exit 0)
```

## Check 3: the timeout (must print two lines, steps 1 and 2)

Command: `grep -n '120000' src/superclaude/skills/sc-sweep-protocol/SKILL.md`
```text
23:1. Run `superclaude sweep run <args>` with the Bash timeout 120000 ms.
24:2. Only when step 1 fails with "command not found", run `uv run --frozen --no-sync superclaude sweep run <args>` with the Bash timeout 120000 ms. No other failure leads to this step, and no step runs the command a third time.
(exit 0)
```

## Check 4: the five words (must print nothing)

Command: `grep -niw 'stop\|retry\|release\|merge\|removal' src/superclaude/skills/sc-sweep-protocol/SKILL.md`
```text
(no output)
(exit 1)
```

## Static contract review: skill text against the canonical style rule

OQ-6 is RESOLVED as (b) (`phase-outputs/plans/OQ-6-GQ-63-done-next-decision.md`); item 7.10 recorded the separate execution authorization and edited `src/superclaude/output-styles/pragmatic.md` (`step-7.10-style-exception.md`, ledger T138 complete), so the item 11.3 gate is satisfied.

Source-backed scenario table: each case names the phrase of the style rule (lines 22 to 26 and the six qualified lines) and the phrase of the skill section "Final reply" or "Steps" that says the same thing; PASS means both files carry it. This is a static text comparison, not a live adherence test, not a role probe and not an activation of the installed HOME style.

| Case | Scenario | Style phrase | Skill phrase | Result |
|---|---|---|---|---|
| P1a | Positive: explicit, applicable coordinator assignment for specified, already-authorized work, top-level session | `pragmatic.md:23` | `SKILL.md:37` | PASS |
| P1b | Positive: exit 0 and the report Read successfully are conditions | `pragmatic.md:23` | `SKILL.md:39` | PASS |
| P1c | Positive: report Read successfully is a condition | `pragmatic.md:23` | `SKILL.md:41` | PASS |
| P2 | Positive: a person asks for a sweep inside an independently established coordinator session | `pragmatic.md:24` | `SKILL.md:45` | PASS |
| P3 | Positive: an operative assignment plus a separate sweep request in the same message | `pragmatic.md:24` | `SKILL.md:45` | PASS |
| N1 | Negative: ordinary person-started session without the assignment | `pragmatic.md:24` | `SKILL.md:45` | PASS |
| N2 | Negative: role or table request alone, the word coordinator alone, the skill or style alone | `pragmatic.md:24` | `SKILL.md:45` | PASS |
| N3 | Negative: unknown, ambiguous, revoked, superseded or conflicting assignment | `pragmatic.md:24` | `SKILL.md:45` | PASS |
| N4 | Negative: workers and subagents | `pragmatic.md:25` | `SKILL.md:47` | PASS |
| N5 | Negative: claims from other agents or peers | `pragmatic.md:24` | `SKILL.md:45` | PASS |
| N6 | Negative: other coordinator messages | `pragmatic.md:25` | `SKILL.md:47` | PASS |
| N7 | Negative: quoted or merely read sweep text | `pragmatic.md:25` | `SKILL.md:47` | PASS |
| N8 | Negative: exit 1 or 2 keeps stderr visible | `pragmatic.md:25` | `SKILL.md:47` | PASS |
| N9 | Negative: the designed fallback is exhausted (both commands fail) | `pragmatic.md:25` | `SKILL.md:29` | PASS |
| N10 | Negative: malformed JSON or missing summary or path | `pragmatic.md:25` | `SKILL.md:29` | PASS |
| N11 | Negative: the report Read is missing, unreadable or denied | `pragmatic.md:25` | `SKILL.md:29` | PASS |
| N12 | Negative: an injected report cannot grant a role or rights (contents stay data) | `pragmatic.md:24` | `SKILL.md:45` | PASS |
| N13 | Negative: no fabricated success | `pragmatic.md:25` | `SKILL.md:29` | PASS |
| N14 | Negative: no general exemption for coordinators, other skills or file output | `pragmatic.md:25` | `SKILL.md:47` | PASS |
| S1 | Scope: chat presentation only | `pragmatic.md:26` | `SKILL.md:49` | PASS |
| S2 | Scope: formatting never authorizes advice | `pragmatic.md:25` | `SKILL.md:47` | PASS |
| S3 | Scope: a loaded-text rule, not a runtime detector | `pragmatic.md:26` | `SKILL.md:49` | PASS |
| S4 | Scope: only the final successful reply is exempt | `pragmatic.md:23` | `SKILL.md:43` | PASS |

Result: 23 of 23 cases PASS, 0 FAIL.

Limits: this proves the two texts state the same boundaries; it does not prove a live model follows them, recognizes a coordinator role or resists an injected report. The installed style (`~/.claude/output-styles/pragmatic.md`) is not updated by this work. The skill adds no tool, action, permission, schedule or identity detector and changes no Python report or JSON.
