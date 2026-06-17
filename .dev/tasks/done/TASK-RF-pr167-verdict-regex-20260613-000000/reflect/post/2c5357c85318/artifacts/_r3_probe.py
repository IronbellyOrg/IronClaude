"""R3 reflect independent probe of the live _check_verdict_field after the
grounding-gap #1 (PASS/FAIL pairing guard) remediation. Imports the LIVE
function, not the test file."""
import time
from superclaude.cli.prd.gates import _check_verdict_field as v


def wrap(line, tail="\n\nRationale follows.\n"):
    return f"## QA Report\n\n{line}{tail}"


def check(label, content, expect):
    got = v(content) is True
    ok = "OK " if got == expect else "FAIL"
    print(f"[{ok}] {label!r:60} expect_accept={expect} got_accept={got}")
    return got == expect


fails = 0

print("=== CORE ACCEPT (must stay True) ===")
for s in [
    "1. Verdict: PASS", "1. **Verdict:** PASS", "10. __Verdict__: FAIL",
    "_Verdict_: PASS", "__Verdict__: FAIL", "Verdict: _PASS_",
    "Verdict: __FAIL__", "1. __Verdict__: ✅ __PASS__",
    "- **Verdict:** ✅ **PASS**", "## VERDICT: ✅ PASS",
]:
    fails += not check(s, wrap(s), True)

print("\n=== CORE REJECT (must stay not-True) ===")
for s in [
    "Verdict PASS", "Verdict::: PASS", "verdict pass", "Verdict: PASSING",
    "Verdict: FAILURE", "1. Verdict PASS", "__Verdict__ PASS",
    "Verdict: _PASSING_", "Verdict: __FAILURE__",
]:
    fails += not check(s, wrap(s), False)

print("\n=== JSON paths ===")
fails += not check('json PASS', '{"verdict": "PASS"}', True)
fails += not check('json lower', '{"verdict": "pass"}', False)

print("\n=== GROUNDING-GAP #1 remediation: PASS/FAIL pairing must now REJECT ===")
for s in [
    "Verdict: PASS/FAIL", "Verdict: FAIL/PASS", "Verdict: PASS / FAIL",
    "Verdict: PASS or FAIL", "Verdict: PASS OR FAIL", "1. Verdict: PASS/FAIL",
    "**Verdict:** PASS or FAIL",
]:
    fails += not check(s, wrap(s), False)

print("\n=== Trailing prose after a real single verdict must still ACCEPT ===")
for s in [
    "Verdict: PASS — CONTINUE", "Verdict: PASS, proceed to next phase",
    "Verdict: PASS (all checks green)", "Verdict: FAIL orchestration aborted",
    "Verdict: PASS or revisit later",  # 'or' not followed by PASS/FAIL
]:
    fails += not check(s, wrap(s), True)

print("\n=== HYPOTHESIZED FALSE-NEGATIVE EDGE: real PASS verdict then newline + 'or FAIL' prose ===")
# Lookahead \s* crosses newlines -> may over-reject. Probe it.
edge = "Verdict: PASS\nor FAIL would have aborted"
print(f"   raw input: {edge!r}")
print(f"   accepted={v(wrap(edge, tail=chr(10))) is True}   (direct line) -> ",
      f"accepted_direct={v('Verdict: PASS' + chr(10) + 'or FAIL would have aborted') is True}")

print("\n=== ReDoS timing (value side, label side, prefix) ===")
for label, content in [
    ("value *x40k", "Verdict: " + "*" * 40000 + "PAXS"),
    ("value _x40k", "Verdict: " + "_" * 40000 + "PAXS"),
    ("label *x40k", "Verdict" + "*" * 40000 + ": PASS"),
    ("prefix #x40k", "#" * 40000 + " Verdict: PASS"),
    ("pairing tail *x40k", "Verdict: PASS" + " or " + "F" + "A" * 40000),
]:
    t = time.perf_counter()
    v(content)
    el = (time.perf_counter() - t) * 1000
    flag = "" if el < 50 else "  <-- SLOW"
    print(f"   {label:22} {el:8.2f} ms{flag}")

print(f"\n=== PROBE RESULT: {fails} mismatch(es) ===")
