"""Apply the D1-D5 common replacements to the three p12 plans (exact-string, each must match once)."""
import re
import sys
from pathlib import Path

PLANS = Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/plans")
FILES = {"b1": "PLAN-1-k3-union-verify.md", "b2": "PLAN-2-verify-gate.md", "b3": "PLAN-3-final-gate.md"}

OLD_ROWS = """| a3-r1 | 2 | PASS at R2 | 57,973 | +0.36% | 143,740 | 105,228 | FAIL | B1 T1, B2 T2 |
| a3-r2 | 2 | PASS at R2 | 59,034 | +2.20% | 216,311 | 157,213 | FAIL | F-01 T3, F-02 T1 |
| a3-r3 | 2 | PASS at R2 | 58,196 | +0.75% | 238,956 | 137,746 | FAIL | F-1 T1, F-2 T2 |
| a3-r4 | 2 | PASS at R2 | 57,873 | +0.19% | 156,933 | 118,901 | FAIL | A-01 other, A-02 T2 |
| a3-r5 | 2 | PASS at R2 | 58,448 | +1.19% | 210,181 | 170,577 | PASS | none |
| a3-r6 | 3 | PASS at R3 | 59,941 | +3.77% | 492,215 | 142,211 | FAIL | F-01 T2 |
| **mean** | **2.17** | **6/6 PASS** | | **+1.41%** | **243,056** | **138,646** | **1/6 PASS** | **1.50 per audit** |"""
NEW_ROWS = """| a3-r1 | 2 | PASS at R2 | 57,973 | +0.36% | 70,694 | 52,531 | FAIL | B1 T1, B2 T2 |
| a3-r2 | 2 | PASS at R2 | 59,034 | +2.20% | 109,207 | 78,276 | FAIL | F-01 T3, F-02 T1 |
| a3-r3 | 2 | PASS at R2 | 58,196 | +0.75% | 95,213 | 69,081 | FAIL | F-1 T1, F-2 T2 |
| a3-r4 | 2 | PASS at R2 | 57,873 | +0.19% | 81,415 | 59,033 | FAIL | A-01 other, A-02 T2 |
| a3-r5 | 2 | PASS at R2 | 58,448 | +1.19% | 94,998 | 84,759 | PASS | none |
| a3-r6 | 3 | PASS at R3 | 59,941 | +3.77% | 151,017 | 70,581 | FAIL | F-01 T2 |
| **mean** | **2.17** | **6/6 PASS** | | **+1.41%** | **100,424** | **69,044** | **1/6 PASS** | **1.50 per audit** |

Token columns are deduplicated (each message id counted once, section 2 convention below). Per-step baseline means used in section 7: R1 50,577 (50% of the loop), V1 14,255, R2 29,993, R3 28,871 and V2 4,726 (a3-r6 only), audit 69,044 (69% of the loop)."""

OLD_CONST = "`B_TOK = 381,702` (loop plus the one audit, the Stage 2 definition of tokens per replicate), `B_LOOP = 243,056` (loop only),"
NEW_CONST = "`A_BASE = 100,424` (loop only; every cost rule is a ratio to it), `AUD_BASE = 69,044` (one audit), `B_BASE = 169,468` (loop plus one audit; reported, never decides),"

OLD_TOKPARA = """Token correction: `STAGE2-REPORT.md` says 0.33M output tokens per replicate. That figure summed `state.json` `output_tokens`, which are missing for R1 of a3-r1..r3 and V1 of a3-r1. Recomputed from transcripts the loop mean is 243,056 and the loop plus one audit is 381,702. Use the transcript figures. `TOK` (the decision metric) is defined as in Stage 2: loop steps plus the first audit (AUD) only; the second audit (AUD2) is an added validity control and is excluded. Report loop-only tokens (`LOOP`) as well. Your `harness.py basetokens` must reproduce the per-run loop totals above within 1%; for a3-r1 R1 three transcripts exist (an Opus one of 6,189 tokens, an empty one and the Sonnet one of 101,293): take the Sonnet transcript with the most output tokens."""
NEW_TOKPARA = """Token convention (owner decision D2 in `$SP/p14/DECISIONS-ADDENDUM.md`, binding). A transcript logs an assistant message once per content block, every copy with the same `message.id` and usage, so summing lines double-counts. Count each message id ONCE: a step's output tokens = sum over unique `message.id` of the max `message.usage.output_tokens` seen for that id. The earlier figures (loop 243,056, loop plus audit 381,702, and the 0.33M of the first STAGE2-REPORT table) were inflated by this double count and are not used. `LOOP` (= A, the decision metric) sums every loop worker of a run (reviews, revises, verifies, gates, merges, adjudications) and excludes AUD and AUD2, which are measurement instrumentation. Every cost rule is the ratio `R_LOOP = LOOP_T / A_BASE` (= `LOOP_T / 100,424`). `TOK` (= B) = `LOOP` + AUD (first audit only) is reported beside it as `R_B = TOK_T / B_BASE` (= `TOK_T / 169,468`) and never decides. Your `harness.py basetokens` must reproduce the per-run loop and audit totals above within 1%; for a3-r1 R1 the glob finds one Sonnet transcript (49,641 tokens) and two Opus transcripts whose first message names the same prompt: keep the Sonnet one."""

COMMON = [
    ("- Experiment workers are Sonnet subagents. At most 6 workers of this experiment may run at once (the session limit is 20 across three parallel experiments).",
     "- Experiment loop workers are Sonnet subagents in the decision stratum and Haiku subagents (Agent model `haiku`) in the Haiku robustness stratum (section 3b); the AUD/AUD2 audits are always Sonnet. At most 6 workers of this experiment may run at once, both strata together (the session limit is 20 across three parallel experiments).\n- Owner decisions D1-D5 in `$SP/p14/DECISIONS-ADDENDUM.md` are binding and already applied in this file: D1 keeps the zones of section 3, D2 is the loop-only token convention (section 2), D3 the Haiku stratum (3b), D4 the extension (3c), D5 the private clone (A1)."),
    ("| Shared second audit of baseline (made by the coordinator, may be absent) | `$SP/p12/baseline-audit2/results.json` |",
     "| Shared second audit of baseline (made by the coordinator; all six reports present on 2026-11-10) | `$SP/p12/baseline-audit2/results.json` |\n| Owner decisions D1-D5 (binding) | `$SP/p14/DECISIONS-ADDENDUM.md` |\n| Shared Haiku baseline (made by the coordinator, may be absent; consume, never run your own) | `$SP/p14/haiku-baseline/results.json` (runs under `$SP/p14/haiku-baseline/runs/a3-r1` .. `a3-r6`) |"),
    (OLD_ROWS, NEW_ROWS),
    (OLD_CONST, NEW_CONST),
    (OLD_TOKPARA, NEW_TOKPARA),
    ("Orca is not installed on this machine and the main checkout is shared, so you work in a private clone (a plain `git clone`, not a `git worktree`) under your experiment directory. If the coordinator handed you a dedicated Orca worktree instead, use it and skip the clone.",
     "Private clones are accepted (owner decision D5): in this environment each implementer works in its own full `git clone` under `$SP`, with no git worktree and no Orca. The main checkout is shared, so never switch its branch."),
    ("sum `message.usage.output_tokens` over assistant lines; keep only transcripts whose assistant `model` contains `sonnet` (print a WARN for any other model);",
     "sum, over unique `message.id`, the max `message.usage.output_tokens` of the assistant lines (section 2; never sum lines); keep only transcripts whose assistant `model` contains the step's expected model (`sonnet` for every step of a Sonnet run and for AUD/AUD2 of every run, `haiku` for the loop steps of a Haiku run) and print a WARN for any other model;"),
    ("prints per-run loop and audit totals (must match section 2).",
     "prints per-run loop and audit totals (must match section 2: loop mean 100,424, audit mean 69,044)."),
    ("| `TOK` (tokens per replicate) | sum of `output_tokens` (B2 item 5) over every loop step plus AUD (not AUD2): the Stage 2 definition; baseline 381,702 |\n| `LOOP` | the same without AUD; baseline 243,056 |",
     "| `LOOP` (A, decides) | sum of deduplicated `output_tokens` (B2 item 5) over every loop step, excluding AUD and AUD2; baseline `A_BASE` 100,424; `R_LOOP = LOOP_T / 100,424` |\n| `TOK` (B, reported only) | `LOOP` plus AUD (not AUD2); baseline `B_BASE` 169,468; `R_B = TOK_T / 169,468`, printed beside `R_LOOP`, never decides |\n| Stratum | every `state.json`, log record and metrics row carries `stratum: \"sonnet\"` or `\"haiku\"`; every table is per stratum and Haiku is never pooled into a Sonnet number |"),
    ("about 0.7M output tokens by the Stage 2 figure, about 0.76M by the transcript figures)",
     "about 0.34M output tokens: 2 x (100,424 + 69,044), deduplicated)"),
    ("same model (`sonnet`), same stop rules", "same model (`sonnet` in the decision stratum), same stop rules"),
    ("- **Replicate decision is pre-registered.** n = 6. Lost runs are not replaced unless the coordinator asks; fewer than 5 completed runs makes the result INCONCLUSIVE.",
     "- **Replicate decision is pre-registered.** Sonnet n = 6, plus the one-time n = 9 extension of section 3c only when the n = 6 outcome is INCONCLUSIVE; Haiku n = 4 (section 3b), never extended. Lost runs are not replaced unless the coordinator asks; fewer than 5 completed Sonnet runs (8 at n = 9) makes the result INCONCLUSIVE."),
    ("(being produced now)", "(all six reports present as of 2026-11-10)"),
    ("For every line `LAUNCH <absolute path>` that `advance.py` prints, start one subagent with model `sonnet` and exactly this message:",
     "For every line `LAUNCH <absolute path> model=<sonnet|haiku>` that `advance.py` prints, start one subagent with that model (AUD/AUD2 lines always say `model=sonnet`) and exactly this message:"),
    ("basetokens: loop mean <n> (expected 243,056), audit mean <n> (expected 138,646)",
     "basetokens: loop mean <n> (expected 100,424), audit mean <n> (expected 69,044), deduplicated by message id\ndecision file: $AB/decision.json; D2 (loop-only R_LOOP, R_B reported) in <files>; D3 (stratum tag, Haiku loop model, Sonnet-only AUD) in <files>; D4 (extension) in <files>"),
    ("launch each LAUNCH line as a sonnet subagent with", "launch each LAUNCH line as a subagent of the model it names with"),
    ("(1) one-line outcome ADOPT / DROP / INCONCLUSIVE (+ PROVISIONAL if baseline-audit2 is absent) and the rule that decided it;",
     "(1) one-line outcome ADOPT / ADOPT (Haiku robustness pending) / DROP / INCONCLUSIVE (+ PROVISIONAL if baseline-audit2 is absent; + `n=9` if the 3c extension ran) and the rule that decided it, with `R_LOOP` and `R_B` side by side;"),
    ("(4) the design-specific tables (Part E);", "(4) the design-specific tables (Part E) and the separate Haiku stratum table (3b), never pooled;"),
    ("uv --version\n```", "ls $SP/p14/DECISIONS-ADDENDUM.md                                             # binding owner decisions\ntest -f $SP/p14/haiku-baseline/results.json && echo \"haiku baseline ready\" || echo \"haiku baseline not yet produced (Haiku comparison pending; run the Sonnet stratum first)\"\nuv --version\n```"),
]

ITEM9 = ("9. **Strata, decision file and extension (owner decisions D2-D4).** `harness.py build [--stratum sonnet|haiku] [--extend]`: the default `sonnet` creates `{d}-r1..{d}-r6`; `--stratum haiku` creates `{d}h-r1..{d}h-r4`; `--extend` (Sonnet only; refused unless `$AB/metrics.json` records a Sonnet n=6 outcome of INCONCLUSIVE, and refused if `{d}-r7` exists) creates `{d}-r7..{d}-r9`. Every `state.json` gets `\"stratum\": \"sonnet\"|\"haiku\"` and `\"loop_model\": \"sonnet\"|\"haiku\"`, and every log, telemetry and metrics record copies `stratum`. `advance.py` prints `LAUNCH <absolute path> model=<m>`, with `m` = the run's `loop_model` for loop steps and always `sonnet` for AUD/AUD2 (assert it: Haiku never audits). Prompt files are identical across strata; the model is the only difference. Sonnet runs are printed before Haiku runs. Decision constants (`A_BASE` 100,424, `AUD_BASE` 69,044, `B_BASE` 169,468, the default `B_*` of section 2, every threshold of section 3 including the n=9 fractions of 3c, `N_SONNET` 6, `N_HAIKU` 4, `N_EXTEND` 3, the Haiku baseline path) live in `$AB/decision.json`, written once from sections 2-3 and read by `analyze`; no threshold literal appears in code. `analyze` computes `R_LOOP` (decides) and `R_B` (reported) in one function and writes per-stratum tables.")

TEST13 = ("13. Convention and strata: `analyze` on synthetic records computes `R_LOOP = LOOP / 100,424` and `R_B = (LOOP + AUD) / 169,468`; a case where the `R_B` limit holds and the `R_LOOP` limit fails is decided by `R_LOOP`; a transcript that logs one message on two lines counts it once; `build --stratum haiku` writes `stratum: haiku` into 4 runs whose loop LAUNCH lines say `model=haiku` and whose AUD/AUD2 lines say `model=sonnet`; Haiku runs never enter the Sonnet `BLK_T`; `build --extend` is refused unless the Sonnet outcome is INCONCLUSIVE and creates r7..r9 only once.")


def sub_once(text, old, new, fname):
    n = text.count(old)
    if n != 1:
        sys.exit(f"{fname}: expected 1 match, got {n}: {old[:90]!r}")
    return text.replace(old, new)


for d, fname in FILES.items():
    p = PLANS / fname
    t = p.read_text(encoding="utf-8")
    for old, new in COMMON:
        t = sub_once(t, old, new, fname)
    # B2 item 9 after item 8 (single line starting with "8. Keep the p11 stop")
    m = re.search(r"(?m)^8\. Keep the p11 stop.*$", t)
    assert m, fname
    t = t[: m.end()] + "\n" + ITEM9.format(d=d) + t[m.end():]
    # build commands for the strata
    old_b = f"uv run --no-project python $AB/harness.py build            # once; creates {d}-r1..r6"
    t = sub_once(t, old_b, old_b + f"\nuv run --no-project python $AB/harness.py build --stratum haiku   # once; creates {d}h-r1..r4 (Haiku stratum, 3b)\nuv run --no-project python $AB/harness.py build --extend           # only after a Sonnet n=6 INCONCLUSIVE (3c); creates {d}-r7..r9", fname)
    # test 13 after test 12 line
    m = re.search(r"(?m)^12\. .*$", t)
    assert m, fname
    t = t[: m.end()] + "\n" + TEST13 + t[m.end():]
    p.write_text(t, encoding="utf-8")
    print("ok", fname)
