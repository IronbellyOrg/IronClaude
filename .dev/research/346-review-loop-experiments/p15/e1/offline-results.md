# E1 offline results: smoke

**SMOKE NO-GO-OFFLINE**: smoke STOP: false AUTO_CLOSE on ['sm-19', 'sm-20', 'sm-24'] (truth closure_correct = no)

- cases 40 (truth decided 39); eligible packets 34; AUTO_CLOSE 12; automation coverage 0.35294117647058826
- false AUTO_CLOSE: ['sm-19', 'sm-20', 'sm-24']; true AUTO_CLOSE: 8
- decisions {'FALLBACK': 22, 'AUTO_CLOSE': 12, 'NOT_ELIGIBLE': 4, 'OPEN': 2}; prechecks {'ok': 34, 'deps': 4, 'noop': 2}
- conventional checker: agreement with Jev closing decision 0.9705882352941176; false closures ['sm-20', 'sm-24']
- perturbation consistency: 9/10 groups identical decisions, 10/10 identical closing decision
- narrow-stage cost reduction (checker output tokens, D2): 0.3562049355899478
- Jev: calls 34, status {'ok': 34}, input tokens 44886, USD 0.001885 (reported apart, never added to worker tokens); latency p50/p95 179.0/210.79999999999998 ms
