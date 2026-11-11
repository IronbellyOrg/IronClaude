# Sonnet vs Opus judges: same brief, same evidence, 3 judges each (scores 0-10)

| candidate | Sonnet J1/J2/J3 | Sonnet mean | Opus J1/J2/J3 | Opus mean |
|---|---|---|---|---|
| A1 | 6.5/5.5/6 | 6.00 | 7/7/6 | 6.67 |
| A2 | 5/4.5/5 | 4.83 | 6/5.5/5 | 5.50 |
| A3 | 4.5/5/4 | 4.50 | 5/4/4 | 4.33 |
| E2 | 3/3.5/3.5 | 3.33 | 2/3/3 | 2.67 |
| E1 | 2/3/2.5 | 2.50 | 3/3/2 | 2.67 |
| E3 | 2/1.5/2 | 1.83 | 1/2/2 | 1.67 |
| E4 | 1/1/1 | 1.00 | 1/1/1 | 1.00 |
| E5 | 0.5/0.5/0.5 | 0.50 | 0/1/1 | 0.67 |

Top-3 picked: all six judges chose {A1, A2, A3}. Order: A1 first for 6/6. A2 above A3 for 2/3 Sonnet and 3/3 Opus. Sonnet J2 put A3 second.

Spot-checks: all six independently found the same false advocate claim (E4: D09/D10 "never raised"; actually raised by 7 and 6 arms). Sonnet J3 additionally could not reproduce A3's "V2 resolved 2 of 10" and discounted A3's evidence. No Opus judge reported a factual discrepancy that no Sonnet judge found.

Differences in content: Opus judges gave point estimates for ab5 and ab6 (ab5 about 10.5-12 residual blocking, 12-15 fixed) where Sonnet gave only deltas; Opus J1 proposed the triage test (sort the 117 residual cells into already-briefed / raised-but-rejected / never-raised) and specified the A2 execution control and lint regexes in more detail; Sonnet J2 added "always append the fix-the-governing-rule sentence to the V2 brief"; Opus J3 added "log the spec state at each PASS". Tokens used per judge: Sonnet 144-163k, Opus 148-153k (Opus costs about 2x per token).

Verdict on "is Opus significantly better as a judge here": no. The decision, the ordering of the top candidate, the kill rules and the free tweaks are the same; Opus is slightly more detailed. One 3-vs-3 comparison without ground truth cannot show a quality difference smaller than a rank flip; the ledger-based judge evaluation (ADJ, verifier, audit, scorer roles) is where a measurable difference can be tested.
