# base-drift: READY

Exact replay of Stage 2 arm 3 (p11 a3), 2 fresh replicates `a3d-r1`, `a3d-r2`. Sonnet loop workers R1 V1 R2 V2 R3 (stop on PASS), then two frozen Sonnet audits AUD (sandbox `aud/`) and AUD2 (sandbox `aud2/`), both launched together once the loop ends.

## Files (all under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/base-drift)
- harness.py: copy-and-modify of p11/harness.py, arm 3 only. Commands: build, prep, ingest, status, unlaunch, tokens, analyze.
- advance.py: state machine; `--dry-run` writes R1 prompts and marks nothing. Works unchanged with `/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/drive.sh p16/base-drift` (drive.sh not modified).
- tests/test_drift.py: `cd /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/base-drift && python3 tests/test_drift.py`
- runs/a3d-r1, runs/a3d-r2: built sandboxes (state.json, PROMPT-R1.md written, nothing launched).

## Fidelity to p11
- command.md = p11/runs/a3-r1/command.md (sha e62e70b9...), rules file = p11/rules.md (sha 3eb772f9...), spec/overlay from S1 repo-overlay (sha d3cdbe57...); hashes asserted at build and at every audit prep. The audit command equals the arm-3 command, as in p11 AUD and p12 baseline-audit2.
- Briefs/WRAP/CMDPART are verbatim p11 text; tests prove PROMPT-R1, R2, V1, AUD equal p11's a3-r1 prompts after the sandbox-path substitution, AUD2 = AUD with `aud2`, and the sandbox file tree equals a p11 arm-3 sandbox. V ids use p11's ids_from parser.
- Audit sandbox layout is `<run>/aud/ws` and `<run>/aud2/ws` (same as p11 AUD and the central matrix rescoring path).

## Accounting and analysis
- Transcripts are matched by whitespace-normalised full PROMPT text (fallback: prompt contained in the first message); model must contain "sonnet"; tokens = sum over distinct assistant message ids of max output_tokens; picks the DONE transcript with most tokens if several.
- `python3 harness.py analyze`: per run loop A, R1, audit 1/2 tokens, blocking per audit (central/score_themes.py blocking_findings, FAIL/PASS only, as build_matrix._audit_blk), verdicts, loop end, reviews; then ratios of fresh loop mean and R1 mean (and V1/R2/V2/R3/audit) to the p11 per-step means taken live from `p12/ab1/harness.py basetokens`. p11 means now: R1 50,576; R2 29,993; R3 28,871; V1 14,255; V2 4,726; loop 100,424; audit 69,044 (matches expected).
- Run `python3 harness.py tokens` (or just let advance.py ingest) before analyze.

## Test results
7/7 passed: byte-identity of inputs and sandbox tree; prompts equal p11 modulo paths; dry run marks nothing and a real run launches then does not relaunch; full loop R1 FAIL, V1, R2 PASS, both audits launched together, ALL DONE, tokens counted once per message id; R3 path, relaunch-once then LOST; prompt-text and model matching; drive.sh integration (on a throwaway copy).

## First LAUNCH lines (what drive.sh prints; run in Claude Code, Agent with the prompt file text pasted verbatim, model sonnet)
LAUNCH p16/base-drift/runs/a3d-r1/PROMPT-R1.md model=sonnet
LAUNCH p16/base-drift/runs/a3d-r2/PROMPT-R1.md model=sonnet

## Open questions
- A review (R1/R2/R3/AUD) with verdict INCOMPLETE/NONE is auto-relaunched once (ab1 rule), whereas p11 only flagged it for manual check; baseline never hit this (6/6 clean).
- After R3 the audits run whatever R3's verdict (as p11); loop_end is recorded as "R3-FAIL" in that case.
- The launcher must paste the PROMPT file text unchanged as the Agent prompt; otherwise tokens cannot be matched (a wrapper around it still matches via the contained-text fallback).
