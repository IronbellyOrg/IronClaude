# R5 mechanical gate checks (item 6.4)

Design file: `docs/designs/orchestrator-mode.md` (1047 lines). Section 4 is lines 157-222; `### Fix cycle 3` is at line 1037. Run on 2026-11-09T00:22:03Z.

## Command 1: agent-wait hits
```
$ grep -n 'agent-wait' docs/designs/orchestrator-mode.md
66:| GQ-109 | `gate-list`, `worker-read` and every `git stash` form are absent from both allowlists and from step 1.0a. 
535:    ("worktree", "ps", "--agent-wait"),      # allowed by R5 (owner 2026-11-08), not called in Phase 1
536:    ("worktree", "ps", "--agent-wait", "--json"),   # allowed by R5 (owner 2026-11-08), not called in Phase 1
555:Decision on `worktree list` and `worktree current` (M3): they stay in the pinned set because the owner sign-off for 
679:The coordinator keeps watching its Run until every Task it created is settled and every result has been inspected an
759:| `tests/sweep/test_probes_allowlist.py` | NFR-003, NFR-014, FR-021, FR-026, FR-020, NFR-007, GQ-109, M7, SPEC secti
833:| D6 | WC-14 (WC-16 in this design) text of SPEC section 10 (lines 404-408) | The same text renumbered WC-16, with m
837:| D10 | NFR-003 (line 132), NFR-014 (line 143) and SPEC lines 310, 323, 500, 504, 510, 562 and 619: `worktree ps` ne
895:- The `ALLOWED_ORCA` allowlist of section 7.3 has ten templates; step 1.0a issues only templates 1 to 8 of it, with 
1047:| R5 | Master's sweep runs `worktree ps --agent-wait`; INV-005 condition 1 forbade it | RESOLVED by the owner 2026-
```

## Command 2: the Fix cycle 3 R5 row
```
$ grep -n '^| R5 | Master' docs/designs/orchestrator-mode.md
1047:| R5 | Master's sweep runs `worktree ps --agent-wait`; INV-005 condition 1 forbade it | RESOLVE
```

## Command 3: em-dash count
```
$ grep -c '—' docs/designs/orchestrator-mode.md
0
```

## Command 4: TODO or TBD
```
$ grep -nw 'TODO\|TBD' docs/designs/orchestrator-mode.md
(no output expected; grep exit status 1)
```

## Command 5: deviation total
```
$ grep -n '^Total: 10 deviations.' docs/designs/orchestrator-mode.md
839:Total: 10 deviations.
```

## Command 6: open-item total
```
$ grep -n '^Total: 23 open items.' docs/designs/orchestrator-mode.md
1015:Total: 23 open items.
```

## Command 7: eight or 8 templates
```
$ grep -n 'eight\|8 templates' docs/designs/orchestrator-mode.md
837:| D10 | NFR-003 (line 132), NFR-014 (line 143) and SPEC lines 310, 323, 500, 504, 510, 562 and 619: `worktree ps` ne
```

## Command 8: the section 4 extension-point sentence
```
$ grep -n 'recorded owner decision (R5, 2026-11-08)' docs/designs/orchestrator-mode.md
221:Extension points, each additive: a new rule appended to `RULES` before `fall
```

## Command 9: FORBIDDEN_TOKENS
```
$ grep -n 'FORBIDDEN_TOKENS = frozenset' docs/designs/orchestrator-mode.md
539:FORBIDDEN_TOKENS = frozenset({"--include-remote"})   # rejected in any position
```

## Command 10: the ps templates
```
$ grep -n '("worktree", "ps"' docs/designs/orchestrator-mode.md
532:    ("worktree", "ps", "--json"),
535:    ("worktree", "ps", "--agent-wait"),      # allowed by R5 (owner 2026-11-08), not called in Phase 1
536:    ("worktree", "ps", "--agent-wait", "--json"),   # allowed by R5 (owner 2026-11-08), not called in Phase 1
```

## Checks

- Check 1: PASS - no agent-wait hit forbids the flag; the allowing hits are present: 7.3 templates (2), section 11 positive case (1), section 13 D10 (1), section 15.1 sentence (1); the GQ-109, R5 and /sc:sweep lines allow or do not concern the allowlist
- Check 2: PASS - 'recorded owner decision (R5, 2026-11-08)' appears once, in section 4 (line 221)
- Check 3: PASS - FORBIDDEN_TOKENS holds only --include-remote
- Check 4: PASS - the Fix cycle 3 R5 row exists once (line 1047, after line 1037); the section 9 routing row R5 starts with a different cell
- Check 5: PASS - em-dash count is 0
- Check 6: PASS - no TODO or TBD
- Check 7: PASS - one 'Total: 10 deviations.' hit (D10 added)
- Check 8: PASS - one 'Total: 23 open items.' hit (unchanged)
- Check 9: PASS - no 'eight' or '8 templates' hit says the allowlist has eight templates (the one hit is the D10 row, which says ten, not eight)
- Check 10: PASS - 3 ps templates in 7.3 (ps --json, ps --agent-wait, ps --agent-wait --json)
- Check 11: PASS - no stale '9 deviations' text
- Check 12: PASS - the diagram labels say ALLOWED_ORCA (10) and 10 read templates; no 8-template label is left

Result: 12 of 12 checks PASS.
