## Analysis: the cooldown risk of candidate fix 2

Candidate fix 2 (a switch rule for this 400) would use the proxy's usage-error path, and that path parks the failing model. This comment records how big that risk is, measured on the real proxy log.

### What the park does (`origin/master`, `local-gateway-alias-proxy.py`)

- A matching switch rule calls `cool_down(model, Retry-After)` (lines 909-927). With no `Retry-After` header the park lasts `COOLDOWN_SECONDS`, default **3,600 s** (line 124). Whether the 400 carries a `Retry-After` header is not verified: the capture did not log headers.
- The park is keyed by model name (`_cooldowns[model]`, line 467), not by tier. Parking `glm-5.3` blocks it for tier 2 (second slot), tier 2b (the Terra to GLM 429 fallback) and tier 3 (first slot), and for requests that pick GLM by name.
- It is held in memory (no persistence seen in the code read), so a proxy restart clears it.

### Measured on 21 hours of real traffic (`~/.cache/ccsession/proxy.log.1`, 2026-11-11 16:47 to 2026-11-12 13:47)

- 14 of these 400s: at least 12 came from my own spawn tests and probes; 2 at 17:30 on Nov 11 cannot be attributed (before that session began).
- Tier 3 answered 2,310 requests on GLM-5.3 and 448 on Qwen3.8 Max, so the failing kind was about 0.6% of GLM-bound traffic.
- Replay of a switch rule with the default 1-hour park on those 14 events: it fires 4 times, parks GLM for 4.0 of the 21 hours and moves 584 of 2,310 GLM tier 3 requests (25%) to Qwen. This overstates normal use, because my probes caused most of it. With only the two unattributed events it is one 1-hour park.
- GLM already fails on its own: 29 failure events in the window (mostly `429 all accounts out of usage`), 9 five-minute parks. Qwen logged one failure (a 500 timeout) in 448 requests.

### Severity and likelihood

- **Answer quality: low.** Qwen3.8 Max answered every medium-effort probe; its benchmark score (45.4) is close to GLM-5.3 (44.8). Scores only, not a quality test on real work.
- **Lost redundancy: the real cost.** Tier 3 has two models. While GLM is parked for no reason, one Qwen failure would take the whole tier down although GLM works at other efforts.
- **Silent switch: low.** A user who picked GLM by name gets Qwen during a park, with no notice.
- **Likelihood: low today, rising with use.** Every subagent that reaches tier 3 with Claude Code's default effort fires the rule, and the first one each hour re-parks GLM. With members using tier 3, GLM could stay parked most of the time.

Overall: low to medium. Not a reason to skip the fix, a reason not to ship fix 2 as a plain switch rule.

### Change to the issue

The acceptance criteria now say that **this 400 must never park a model**, with a test showing the model still serves an `effort: high` request after one such 400. Candidate fix 2 now says it needs a no-cooldown path. Candidate fix 1 (retry with `effort` rewritten to `low`) has no park risk and keeps GLM serving.

Limits of this analysis: one 21-hour window; the Retry-After assumption above; Qwen versus GLM quality compared by benchmark scores only.
