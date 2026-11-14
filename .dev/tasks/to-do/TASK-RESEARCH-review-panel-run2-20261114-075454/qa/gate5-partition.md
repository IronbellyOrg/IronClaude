# Gate 5 partition check (Item 6.54)

Date: 2026-11-14

Gate 4 passed (`qa/gate4-cycle-control.md`: `PASS at review 2`, no HALT), so Gate 5 may start.

## Measured lines (one read-only `wc -l` over every Gate 5 input)

Total: **24,386 lines** (research 01-24, web-01 to web-04, `gaps-and-questions.md`, synth-01 to synth-10, 15 `ADJUDICATION-RESULT.md` files).

Largest single files: `synthesis/synth-08-value-inventory.md` 6,127; `research/21-value-ledger-brainstorms.md` 1,797; `research/22-value-ledger-collab-designs.md` 1,046; `research/19-value-ledger-handoffs.md` 986; `research/20-value-ledger-e2-study.md` 935; `research/23-value-ledger-e1-e3-code.md` 894. The 15 debate results total 1,104 lines.

## Initial partition (as written in items 6.54-6.57)

| Agent | Files | Lines | Share of total |
|---|---|---|---|
| 1 | research 01-05 (1,239), web-01 (242), web-02 (159), synth-05 (991), synth-06 (440), synth-07 (673), 15 debate results (1,104) | 4,848 | 19.9% |
| 2 | research 06-11 (1,351), web-03 (162), web-04 (195), synth-04 (606), synth-09 (285), synth-10 (341) | 2,940 | 12.1% |
| 3 | research 12-18 (2,126), gaps-and-questions (579), synth-01 (749), synth-02 (283), synth-03 (405) | 4,142 | 17.0% |
| 4 | six value ledgers 19-24 (6,329), synth-08 (6,127) | 12,456 | 51.1% |

Agent 4 exceeds 30 percent (7,316 lines). No single file alone keeps an agent above 30 percent (synth-08 is 6,127 = 25.1%), so only whole files move.

## Moves (heaviest agent to lightest agent, whole files)

| # | File moved | Lines | From | To | Reason |
|---|---|---|---|---|---|
| 1 | `research/21-value-ledger-brainstorms.md` | 1,797 | agent 4 | agent 2 | agent 2 was lightest (2,940) |
| 2 | `research/22-value-ledger-collab-designs.md` | 1,046 | agent 4 | agent 3 | agent 3 was lightest (4,142) |
| 3 | `research/19-value-ledger-handoffs.md` | 986 | agent 4 | agent 1 | agent 1 was lightest (4,848) |
| 4 | `research/20-value-ledger-e2-study.md` | 935 | agent 4 | agent 2 | agent 2 was lightest (4,737) |
| 5 | `research/23-value-ledger-e1-e3-code.md` | 894 | agent 4 | agent 3 | agent 3 was lightest (5,188) |

## Final partition

| Agent | Files | Lines | Share of total |
|---|---|---|---|
| 1 | research 01-05, web-01, web-02, synth-05, synth-06, synth-07, 15 debate results, **plus ledger 19** | 5,834 | 23.9% |
| 2 | research 06-11, web-03, web-04, synth-04, synth-09, synth-10, **plus ledger 21 and ledger 20** | 5,672 | 23.3% |
| 3 | research 12-18, gaps-and-questions, synth-01, synth-02, synth-03, **plus ledger 22 and ledger 23** | 6,082 | 24.9% |
| 4 | ledger 24 (671), synth-08 (6,127) | 6,798 | 27.9% |

Check: 5,834 + 5,672 + 6,082 + 6,798 = 24,386. No agent exceeds 30 percent. Rules that travel with a moved ledger: the ledger-row enumeration and the `grep -c '^| VL-NN-'` recount (items 6.57), and the ledger-versus-defect-register pair check (ledgers 23 and 24 against `research/17-defect-register.md` rows). Ledger 23 now sits with agent 3, which also holds the defect register, so agent 3 applies the pair check for ledger 23; agent 4 applies it for ledger 24 and checks the synth-08 reconciliation line.
