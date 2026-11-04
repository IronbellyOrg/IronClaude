# HC0 boundary scan
Mechanism statement: a gate's input tokenizer models only part of the grammar of the language it inspects, so inputs outside the modelled subset are misclassified (missed or falsely flagged); the decision stage itself maps the tokenizer's result correctly.

| boundary_type | producer / transformers / consumer | evidence_source | risk | decision | rationale |
|---|---|---|---|---|---|
| file-stdin-prompt | Claude Code PreToolUse JSON / jq (block-bare-python.sh:270) / awk on stdin (:271) | probe-baseline.out (scanner sees the full command; hook exit tracks scanner output in all 14 rows) | delivery could truncate or reinterpret the command | not_applicable | the defect is in awk word recognition after delivery; delivery was observed intact for every symptom input |
| gate-status-enum | WORD / case (:273-276) / exit 0 or 2 | block-bare-python.sh:273-279 and probe-baseline.out | status mapping could mis-route | not_applicable | the case statement maps the scanner word correctly in every observed row; only the word is wrong |
| duplicate-evaluator | src script / byte copy / plugins/superclaude/hooks/scripts/block-bare-python.sh | tests/cli/test_install_hooks.py:785 (`assert source.read_bytes() == mirror.read_bytes()`) | the mirror could diverge | not_applicable | the mirror is a byte-identical copy enforced by a test, not a separate evaluator |
| CLI/subprocess | tests/hooks/test_block_bare_python.py:38-40 / bash subprocess / the real hook script | test file lines 38-40 | tests could exercise a helper instead of the hook | not_applicable | the regression tests run the production script itself with JSON on stdin, the same boundary Claude Code uses |

known_escapes_caught: None claimed.
