# Reviewer Card 2 — QA (quality-engineer)

- Model class: haiku-alias (qwen3.6-plus) · Persona: qa · Stance: ADVERSARIAL
- Self-reported confidence: 0.93

## Verdict: ADEQUATE (one cosmetic doc gap, no regression)

### Coverage table
| Requirement | Test | file:line | Adequate |
|-------------|------|-----------|----------|
| omit `--monitor` → `monitor==1` | test_t103_default_monitor_one_armed | test_skill_parse.py:57-61 | Yes |
| omit → `armed==True` | same | test_skill_parse.py:61 | Yes |
| explicit `--monitor 0` → `monitor==0` | test_explicit_monitor_zero_not_armed | test_skill_parse.py:64-68 | Yes |
| explicit 0 → `armed==False` | same | test_skill_parse.py:68 | Yes |
| timeout default 600 | test_t112_timeout_honored | test_skill_parse.py:81-84 | Yes |
| explicit `--timeout` honored | same | test_skill_parse.py:83 | Yes |
| explicit-0 armed CONSEQUENCE (end-to-end) | test_t110_monitor_never_armed_at_l0 | test_monitor_arm.py:35-43 | Yes — `run_skill(RunConfig(monitor_ordinal=0))` → calls==0, state==S0_IDLE |
| L1 arms exactly once (new default consequence) | test_t109_monitor_armed_exactly_once_at_l1 | test_monitor_arm.py:26-32 | Yes |

Both parse-layer AND runtime/armed-consequence layer covered; explicit-0 escape hatch tested end-to-end.

### pytest: 191 passed / 0 failed
"185 passed" task evidence matches neither parent (190) nor head (191). The change splits one test into two (net +1), verified via git stash diff. **185 is a stale/inaccurate evidence figure — NOT missing/skipped tests** (collected==passed==191, zero skips).

### Stale/now-wrong test: none
Every `1800` literal is an explicit arg; every `run_skill(RunConfig(...))` passes explicit `monitor_ordinal=` (no bare `RunConfig()`), so the default flip changes no runtime test path silently.

### Cosmetic gap (non-blocking)
test_monitor_arm.py module docstring (lines 3-4) and test_skill_parse.py T-110/T-103 cross-ref still frame `--monitor 0` as the legacy "zero-regression guard" without noting it is now an explicit opt-out (not the default). Assertions correct; only narrative lags. test_explicit_monitor_zero_not_armed docstring already captures the new intent.

- regression_present: **false**
