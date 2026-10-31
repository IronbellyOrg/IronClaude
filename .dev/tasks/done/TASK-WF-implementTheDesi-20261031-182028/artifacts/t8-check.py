"""T8 check: every row of the design section 6 tables, plus amendment A2."""
import sys

from superclaude.pr_submit.models import MonitorState as M
from superclaude.pr_submit.reviewers import augment_wait_outcome, codex_wait_outcome, merge_wait

ok = []


def check(name, got, want):
    ok.append(got == want)
    print(f"{'PASS' if got == want else 'FAIL'} {name}: got={got!r} want={want!r}")


# augment wait outcome (left column of the wait table)
check("augment polling + S2_CLASSIFY -> pending", augment_wait_outcome("polling", M.S2_CLASSIFY), "pending")
check("augment polling + S5C_SILENCE_REREQUEST -> pending", augment_wait_outcome("polling", M.S5C_SILENCE_REREQUEST), "pending")
for st in ("clean", "findings", "declined"):
    check(f"augment {st} -> done", augment_wait_outcome(st, M.S2_CLASSIFY), "done")
check("augment TERMINAL_AUGMENT_NO_RESPONSE -> absent", augment_wait_outcome("polling", M.TERMINAL_AUGMENT_NO_RESPONSE), "absent")
check("augment already absent (A2) -> absent", augment_wait_outcome("polling", M.S2_CLASSIFY, absent=True), "absent")
check("augment TERMINAL_TIMEOUT -> incomplete", augment_wait_outcome("polling", M.TERMINAL_TIMEOUT), "incomplete")

# codex wait outcome (right column)
kw = dict(elapsed=60, timeout=600, silence_timeout=300)
check("codex clean -> done", codex_wait_outcome("clean", active=True, other_settled=False, **kw), "done")
check("codex findings -> done", codex_wait_outcome("findings", active=True, other_settled=False, **kw), "done")
check("codex active, not timed out -> pending", codex_wait_outcome("polling", active=True, other_settled=False, **kw), "pending")
check("codex active at timeout -> incomplete", codex_wait_outcome("polling", active=True, other_settled=False, elapsed=600, timeout=600, silence_timeout=300), "incomplete")
check("codex inactive, before deadline, Augment pending -> pending", codex_wait_outcome("polling", active=False, other_settled=False, **kw), "pending")
check("codex inactive, Augment settled -> absent at once", codex_wait_outcome("polling", active=False, other_settled=True, **kw), "absent")
check("codex inactive at silence deadline -> absent", codex_wait_outcome("polling", active=False, other_settled=False, elapsed=300, timeout=600, silence_timeout=300), "absent")
check("codex already absent (A2) -> absent even if active", codex_wait_outcome("polling", active=True, other_settled=False, absent=True, **kw), "absent")


def out(a, c):
    return merge_wait(a, c)["outcome"]


P, D, AB, IN = "pending", "done", "absent", "incomplete"
check("pending | any -> polling", out((P, "polling"), (D, "clean")), "polling")
check("any | pending -> polling", out((D, "clean"), (P, "polling")), "polling")
check("declined | settled -> declined", out((D, "declined"), (D, "findings")), "declined")
check("declined | absent -> declined", out((D, "declined"), (AB, "polling")), "declined")
check("done | done (findings) -> findings", out((D, "clean"), (D, "findings")), "findings")
check("done | done (both clean) -> clean", out((D, "clean"), (D, "clean")), "clean")
check("done | absent -> Augment's state (Augment only)", out((D, "findings"), (AB, "polling")), "findings")
r = merge_wait((D, "clean"), (IN, "polling"))
check("done | incomplete -> Augment's state, Codex reported incomplete", (r["outcome"], r["used"], r["incomplete"]), ("clean", ["augment"], ["codex"]))
r = merge_wait((AB, "polling"), (D, "findings"))
check("absent | done -> Codex's state (Codex only)", (r["outcome"], r["used"], r["absent"]), ("findings", ["codex"], ["augment"]))
check("incomplete | done -> Codex's state", out((IN, "polling"), (D, "clean")), "clean")
check("absent | absent (neither) -> no_response", out((AB, "polling"), (AB, "polling")), "no_response")
check("incomplete | absent -> timeout", out((IN, "polling"), (AB, "polling")), "timeout")
check("incomplete | incomplete -> timeout", out((IN, "polling"), (IN, "polling")), "timeout")
check("absent | incomplete -> timeout", out((AB, "polling"), (IN, "polling")), "timeout")
# A2: Augment's silence outcome with Codex present continues with Codex instead of ending the run
a = augment_wait_outcome("polling", M.TERMINAL_AUGMENT_NO_RESPONSE)
c = codex_wait_outcome("findings", active=True, other_settled=True, **kw)
check("A2: Augment silent + Codex done -> continues with Codex findings", out((a, "polling"), (c, "findings")), "findings")
sys.exit(0 if all(ok) else 1)
