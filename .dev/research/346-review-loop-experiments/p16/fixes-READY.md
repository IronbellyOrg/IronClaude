# p16 fixes report

## Task 1: PN2 (/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab2)
- Cause: RESULTS.md/results.json were stale (written 05:21 UTC, before the 05:55 fingerprint fallback in analysis.find_transcripts, see its anomalies.log). Launches pasted prompt text, so the path match failed and nothing was ingested/counted. The code already carried the fix; no further edit was needed.
- Action: re-ran `python3 analysis.py` -> results.json and RESULTS.md regenerated: 6/6 completed, INCONCLUSIVE (noise band, EXTEND suggested). Per-step tokens for all runs are identical to tokens_generic.json (loop 54208/43213/50786/30082/47821/56090).
- Numbers vs MATRIX row: BLK 1.33, AUD 1.00, AUD2 1.67, growth 0.84 all match exactly (no difference). Also R_LOOP 0.47, R_B 0.45, THEME 0.58, R1 tokens 29208.
- `build_matrix.py` run: p13-pn2 row now 6/6 ... INCONCLUSIVE (not PENDING).

## Task 2: p14/haiku-baseline
- harness.py: STEPS += AUD2; prep/ingest treat AUD2 like AUD with sandbox runs/<run>/aud2 (brief, command.md, rules identical; verified PROMPT-AUD vs PROMPT-AUD2 differ only by the sandbox dir name). Output .dev/orca-command-refactor/review/audit.md inside aud2/ws.
- Six runs/a3-r*/PROMPT-AUD2.md prepped; nothing launched.
- advance.py (via drive.sh p14/haiku-baseline): prints `LAUNCH sonnet <path>` per pending AUD2 and records it in launch-ledger.jsonl (then RUNNING n); detects finish by DONE handback (PROMPT path or pasted-text fingerprint), ingests, and refreshes results.json via collect.py. Smoke tested (6 LAUNCH lines, 2nd call RUNNING 6); ledger deleted afterwards, so the first real drive prints the LAUNCH lines. The ingest path of AUD2 itself is untested until a real AUD2 finishes.
- collect.py: results.json gets mean_blocking_aud1 (1.83, current), mean_blocking_aud2, and mean_blocking = mean over 12 audits once all six AUD2 exist (until then equals aud1). Current results.json values unchanged.
- Token recount (recount.py, prompt-path match since these workers got a short "Read <PROMPT path>" first message; each message id once, no duplicate transcripts): mean loop tokens 167,382 HOLDS (per run 193519/187357/153211/83752/183203/203248; loop models all haiku, audits sonnet). tokens_generic.json now populated.
- Backups: *.bak-aud2, results.json.bak-aud2, tokens_generic.json.bak-before-recount. Log: p14/haiku-baseline/anomalies.log.
