"""Independent adversarial probe of the FINAL _check_verdict_field regex."""
import time
import sys
sys.path.insert(0, "src")
from superclaude.cli.prd.gates import _check_verdict_field as v

def ok(s): return v(s) is True

# 1. ReDoS probes on the FINAL regex (label-side, value-side, pairing-side)
probes = {
    "value-side 40k *": "Verdict: " + "*" * 40000 + "PAXS",
    "label-side 40k _": "\n" + "_" * 40000 + "verdict",
    "label-side 40k *": "\n" + "*" * 40000 + "verdict",
    "pairing 40k space": "Verdict: PASS" + " " * 40000 + "/FAIL",
    "prefix dots 40k":  "\n" + "1." * 40000 + " Verdict: PASS",
}
for name, c in probes.items():
    t = time.perf_counter(); _ = v(c); e = time.perf_counter() - t
    print(f"REDOS  {name:22s} {e*1000:8.2f}ms  {'SLOW!!' if e>0.5 else 'ok'}")

# 2. Tasklist objective-1 required ACCEPT shapes
accept = ["1. Verdict: PASS", "__Verdict__: PASS", "1. __Verdict__: PASS"]
for s in accept:
    print(f"ACCEPT(obj1) {s!r:35s} -> {ok(f'## QA{chr(10)}{s}{chr(10)}x')}")

# 3. Tasklist constraint required REJECT shapes (invalid-shape protections)
reject = ["Verdict PASS", "Verdict::: PASS", "verdict pass", "Verdict: PASSING",
          "Verdict: FAILURE", "Verdict rationale"]
for s in reject:
    print(f"REJECT(cons) {s!r:35s} -> rejected={ok(f'## QA{chr(10)}{s}{chr(10)}x') is False}")

# 4. D5 false-negative regression cases (real verdict + prose starting with or// + PASS|FAIL word)
d5 = ["Verdict: PASS or FAILURE expected", "Verdict: PASS or PASSED later",
      "Verdict: PASS or FAILS fast", "Verdict: PASS\nor FAIL would have aborted"]
for s in d5:
    print(f"D5-ACCEPT     {s!r:40s} -> {ok(f'## QA{chr(10)}{s}{chr(10)}x')}")

# 5. Pairing-guard REJECT (genuine template placeholders)
pair = ["Verdict: PASS/FAIL", "Verdict: PASS or FAIL", "Verdict: PASS / FAIL",
        "1. Verdict: PASS/FAIL", "**Verdict:** PASS or FAIL"]
for s in pair:
    print(f"PAIR-REJECT  {s!r:35s} -> rejected={ok(f'## QA{chr(10)}{s}{chr(10)}x') is False}")

# 6. Adversarial edge cases NOT in the test suite (hunting for new defects)
edge = {
    "decorated pairing PASS__/__FAIL": "Verdict: __PASS__ / __FAIL__",
    "tab-pairing PASS\\t/\\tFAIL": "Verdict: PASS\t/\tFAIL",
    "value emoji + pairing": "Verdict: ✅ PASS or FAIL",
    "lowercase 'or' caps val": "Verdict: PASS Or FAIL",
    "FAIL/PASS reverse": "Verdict: FAIL/PASS",
    "PASS then slashFAIL nospace": "Verdict: PASS/FAIL",
    "genuine: PASS, see FAIL log": "Verdict: PASS, see FAIL log below",
}
for name, s in edge.items():
    print(f"EDGE  {name:34s} accept={ok(f'## QA{chr(10)}{s}{chr(10)}x')}")
