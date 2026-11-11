# A2 gates (lint-first table)

| spec | rows | code-flagged | to Jev | usable | Jev-flagged rows | Jev-flagged rows with no residual defect |
|---|---|---|---|---|---|---|
| orig | 32 | 5 | 27 | 25 | 24 | 8 |
| s15 | 32 | 6 | 26 | 24 | 23 | 8 |
| s25 | 32 | 4 | 28 | 25 | 24 | 8 |
| s29 | 32 | 5 | 27 | 25 | 24 | 8 |
| s33 | 32 | 5 | 27 | 25 | 24 | 9 |
| s35 | 32 | 4 | 28 | 26 | 25 | 9 |
| s38 | 33 | 5 | 28 | 26 | 25 | 8 |
| s45 | 32 | 5 | 27 | 25 | 24 | 8 |
| s47 | 32 | 5 | 27 | 25 | 22 | 10 |
| s52 | 32 | 5 | 27 | 25 | 24 | 8 |
| s62 | 32 | 5 | 27 | 25 | 23 | 11 |
| s65 | 32 | 5 | 27 | 25 | 24 | 8 |
| s66 | 32 | 6 | 26 | 24 | 23 | 10 |
| s70 | 32 | 6 | 26 | 24 | 23 | 8 |
| s71 | 32 | 7 | 25 | 23 | 22 | 8 |
| s72 | 33 | 5 | 28 | 26 | 25 | 11 |
| s73 | 33 | 5 | 28 | 26 | 25 | 15 |
| s74 | 32 | 7 | 25 | 23 | 21 | 11 |
| s75 | 32 | 5 | 27 | 25 | 24 | 8 |
| s76 | 32 | 5 | 27 | 25 | 24 | 8 |
| s77 | 32 | 6 | 26 | 24 | 23 | 9 |
| s78 | 32 | 6 | 26 | 24 | 23 | 10 |
| s79 | 32 | 5 | 27 | 25 | 22 | 8 |
| s80 | 32 | 9 | 23 | 21 | 20 | 8 |
| s81 | 32 | 5 | 27 | 25 | 24 | 9 |
| s82 | 35 | 3 | 32 | 30 | 29 | 13 |
| s83 | 32 | 5 | 27 | 25 | 23 | 11 |
| s84 | 32 | 6 | 26 | 24 | 22 | 12 |
| s85 | 32 | 5 | 27 | 25 | 23 | 9 |
| s86 | 32 | 5 | 27 | 25 | 23 | 9 |
| s87 | 32 | 7 | 25 | 23 | 22 | 11 |
| s88 | 32 | 5 | 27 | 25 | 23 | 11 |
| s89 | 32 | 6 | 26 | 24 | 23 | 14 |
| s90 | 32 | 5 | 27 | 25 | 24 | 12 |
| s91 | 32 | 6 | 26 | 24 | 21 | 9 |
| s92 | 32 | 5 | 27 | 25 | 24 | 9 |
| s93 | 32 | 4 | 28 | 26 | 25 | 13 |

summary: {"modes": ["live"], "tail_defects_caught_beyond_controls": ["D14", "D15", "D16", "D17", "D18", "D19", "D23", "D37", "D38", "D39", "D40", "D44"], "n_tail_defects_caught": 12, "tail_cells_caught": 358, "jev_flags_on_rows_without_residual_defect": 359, "note_false": "rows with no residual mapped defect are an UPPER BOUND on false flags (a row can be flawed with no ledger defect); the kill rule needs independent row labels (not available)"}
judge compare: null
verdict: {"tail_catch_ge_3": true}

## Row table for orig

| row | line | mapped defects | control flags | Jev |
|---|---|---|---|---|
| AC-C1 | 172 | D21,D22,D23 | exec:EXEC,regex:D21 | - |
| AC-C2 | 173 | - | - | cannot_pass |
| AC-C3 | 174 | - | - | cannot_pass |
| AC-C4 | 175 | D21 | exec:EXEC,regex:D21 | - |
| AC-C5 | 176 | D20,D21 | regex:D20,regex:D21 | - |
| AC-0.1 | 191 | - | - | - |
| AC-0.2 | 192 | - | - | - |
| AC-0.3 | 193 | D20,D21 | exec:EXEC,regex:D20,regex:D21 | - |
| AC-0.4 | 194 | D11,D12,D13,D14,D36 | exec:EXEC,lint:PHASE | - |
| AC-1.1 | 195 | D01,D03,D04 | - | cannot_pass |
| AC-1.2 | 196 | D03,D09 | - | cannot_pass |
| AC-1.3 | 197 | - | - | cannot_pass |
| AC-1.4 | 198 | D07,D08,D41 | - | cannot_pass |
| AC-2.1 | 199 | - | - | cannot_pass |
| AC-2.2 | 200 | D06,D10,D26,D28 | - | cannot_pass |
| AC-2.3 | 201 | D18,D27 | - | cannot_pass |
| AC-2.4 | 202 | - | - | cannot_pass |
| AC-2.5 | 203 | - | - | can_pass |
| AC-3.1 | 204 | - | - | cannot_pass |
| AC-3.2 | 205 | D33 | - | cannot_pass |
| AC-3.3 | 206 | - | - | cannot_pass |
| AC-3.4 | 207 | - | - | cannot_pass |
| AC-4.1 | 208 | D24,D26 | - | cannot_pass |
| AC-4.2 | 209 | D38,D39,D40 | - | cannot_pass |
| AC-4.3 | 210 | D44 | - | cannot_pass |
| 7.2#1 | 180 | D13,D17,D37 | - | cannot_pass |
| 7.2#2 | 181 | D15,D16,D37 | - | cannot_pass |
| 7.2#3 | 182 | D07,D11,D15,D26,D37 | - | cannot_pass |
| 7.2#4 | 183 | D03,D06,D12,D29 | - | cannot_pass |
| 7.2#5 | 184 | D14,D19 | - | cannot_pass |
| 7.2#6 | 185 | D17,D18 | - | cannot_discriminate |
| 7.2#7 | 186 | D37 | - | cannot_pass |
