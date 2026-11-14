# Round 1 advocate statement: Variant 3 (decide later, duty not runnable)

Persona: qa (edge cases, failure scenarios, risk). Depth: quick, Round 1 only. Written 2026-11-14.

## Position summary

Variant 3 is the only proposal that commits to nothing the evidence cannot yet support: it keeps the owner's update rule intact, keeps the coordinator off a sweep it cannot run, and matches the spec's own default for Q29 word for word. But my own fact checking shows its central hope (the template delivers the sweep "without a decision") will not come true on this host, so Variant 3 is a sound interim state, not a sound final answer.

## Steelman of Variant 1

Variant 1 is the only route whose mechanism provably changes what the coordinator runs on this host, as the host stands today. Evidence:

- `which -a superclaude` (run 2026-11-14) lists `/home/coder/.local/bin/superclaude` before `/usr/local/bin/superclaude`; the user-level receipt `~/.local/share/uv/tools/superclaude/uv-receipt.toml` pins `rev=d2d8a2d166c9...`. Replacing that install is the one action that changes the first `superclaude` on `PATH`.
- It pins to the merge commit, never a branch (variant-1-original.md:23, diff U-001), which keeps provenance to reviewed code.
- It reaches SWEEP-RUNNABLE in minutes and lets XC-04 be scheduled the same day (variant-1-original.md:12, :16), which unblocks the side path SW-05 -> SWEEP-RUNNABLE -> XC-04 -> XC-07 (`merged-requirements.md:780`).
- It is honest about its cost: it names the owner rule it breaks and the drift it causes (variant-1-original.md:21-22).
- The spec itself allows this route with approval: "no in-place reinstall without the owner's approval" (`merged-requirements.md:1008`) implies an approved one is permitted.

## Steelman of Variant 2

Variant 2 is the route the owner already chose in writing and the one the spec recommends:

- Owner memory: "nobody updates IronClaude in place; updates reach workspaces only through the Coder template and workspace updates" (`ironclaude-updates-only-via-coder.md:11`).
- Spec recommended answer for Q29: "The Coder template" (`merged-requirements.md:556`).
- The pipeline exists: the monitor runs daily (`ironclaude-upstream-monitor.yml:12` `cron: "0 6 * * *"`), can be run by hand (`:13` `workflow_dispatch`, diff U-002), and opens "chore(deps): bump IronClaude pin to ..." (`:340`). The image pin is a single validated authority (`Dockerfile.coder:284-302`, 40 hex chars checked).
- Every workspace gets the same reviewed, image-built commit (diff X-003), so there is no host drift and no exception to record.
- It is the only variant that names, in its own risk section, the shadowing install that would defeat it (variant-2-original.md:23, :27). That is good failure analysis.

## Key strengths claimed

1. **Matches the spec default exactly.** Spec: "Default if unanswered: The WC-16 `/sc:sweep` duty is recorded as 'not runnable'; XC-04 is held" (`merged-requirements.md:556`); failure-mode table: "record the WC-16 `/sc:sweep` duty as 'not runnable' ... hold XC-04; ask the owner Q29; no in-place reinstall without the owner's approval" (`:1008`). Variant 3 steps 1-2 (variant-3-original.md:9-10) are that rule, so no new behavior is introduced.
2. **No false pass.** Variant 3 step 3 re-checks `superclaude sweep --help` before claiming the gate (variant-3-original.md:11), the same check the gate requires "in the coordinator's own environment" (`merged-requirements.md:601`).
3. **No exception to the owner rule and no host mutation before it is needed.** Q29 is a W3 question asked "when their item is next" (`merged-requirements.md:523`). XC-04 also needs Q24, LIVE, ORCA-AVAILABLE, TB-GIT, TB-GIT-ROW and SW-05 (`:828`); ORCA-AVAILABLE was found failing on 2026-11-13 (`:604`). Acting on Q29 early buys nothing while the other gates are open.
4. **Names the shadow risk.** variant-3-original.md:22 says the template update alone "may change nothing" because of `~/.local/bin`.
5. **Re-asks with fresh facts.** The state of the pin and the installs moves daily (monitor cron) and changed twice in three days (image 2026-11-11, user install 2026-11-12), so a decision made now ages badly.

## Weaknesses identified in Variant 1

- **Breaks a standing owner rule** (`ironclaude-updates-only-via-coder.md:11`). The only listed exception is `ccsession-models.json` (`:13`); a CLI reinstall is not it.
- **Entrenches the shadow.** `/home/coder` is a persistent named volume (`main.tf:174-176`, `:594-597`; `main.tf:585` "while /home/coder persisted"). A user-level install therefore survives every template update, so after Variant 1 this host silently ignores all future Coder pins until someone removes it. Variant 1 leaves "when to remove" unresolved (variant-1-original.md:27); in QA terms that is an open-ended drift with no owner and no trigger.
- **Replaces more than `superclaude`.** The receipt also installs `ic` (`uv-receipt.toml` entrypoints). I found no template use of `ic` (grep of `templates/VSCode-AIDev02`, no hits), but other callers are UNVERIFIED (diff A-002).
- **Environment risk.** The check is done in a worker shell whose `PATH` begins with `/home/coder/.config/orca/linux-orca-cli-shim` and lists `~/.local/bin` twice (observed 2026-11-14). A coordinator started by Orca or ccsession may resolve `superclaude` differently (A-001, UNVERIFIED); Variant 1 assumes they match.
- **Network install from GitHub at run time** depends on reachability and on `uv` resolving the same dependency set as the image build; the image build has provenance checks (`Dockerfile.coder:320-321`) that a manual `uv tool install` does not.

## Weaknesses identified in Variant 2

- **Does not work on this host by itself, now verified rather than UNVERIFIED.** Fact 7 in question.md marks home persistence UNVERIFIED; the template answers it: `/home/coder` is the `coder-<id>-home` docker volume (`main.tf:174-176`, `:594-597`), and the comment at `main.tf:583-587` states that across `coder update` "/home/coder persisted". So `~/.local/bin/superclaude` at `d2d8a2d16` survives the template update and still shadows the image copy. Variant 2 as written ends with SWEEP-RUNNABLE failing, which its own risk line admits (variant-2-original.md:23).
- **The fix it needs is itself an in-place change.** Removing the user-level install (`uv tool uninstall superclaude`) is a host mutation; Variant 2 does not say who does it or whether that also needs owner approval (variant-2-original.md:27).
- **Session disruption is more likely than "UNVERIFIED".** `main.tf:583-588` says every `coder update` looked like a new machine and "left Orca down after each template update", which implies the container is recreated (inference; that a coordinator session survives is UNVERIFIED but unlikely). The update must be timed when no coordinator Run is live.
- **Long chain with four human steps** (bump PR review, merge, image build, template push, workspace update), each a place to stall; the monitor can also open a "[needs-build-proof]" variant (`ironclaude-upstream-monitor.yml:373`), adding a further wait.

## Concessions

- Variant 3's step 3 is wrong on this host as written. "When the Coder monitor's pin bump lands ... the gate holds without a decision" (variant-3-original.md:11) cannot happen while the persistent user-level install shadows the image (`main.tf:594-597`). Diff U-003 is rightly rated Low.
- Variant 3 answers nothing (variant-3-original.md:27). It defers the same choice and will return it with the same options (variant-3-original.md:23), plus a new one: who removes the shadow.
- Variant 3 leaves the coordinator without the sweep it was designed around (WC-16, `merged-requirements.md:1021`) for an unbounded time.
- The owner rule plus the persistent home together mean the real decision is not "template or reinstall" but "who removes `~/.local/bin/superclaude`, and when". None of the three variants answers that, mine included.

## Shared assumption responses

| Assumption | Response | Reason |
|---|---|---|
| A-001 (coordinator resolves `superclaude` through the same `PATH` as this worker) | QUALIFY | The observed worker `PATH` starts with an Orca shim and repeats `~/.local/bin`, so it is shaped by launch context; the coordinator's `PATH` is UNVERIFIED. The gate already demands the check "in the coordinator's own environment" (`merged-requirements.md:601`), so every variant must run the check there, not in a worker shell. |
| A-002 (removing or replacing the user-level install is safe) | QUALIFY | The install also provides `ic` (receipt entrypoints); no template file references it (grep, no hits), but scripts or habits outside the template are UNVERIFIED. Safe enough if `ic` and `superclaude` are both checked after removal; not safe to assume. |
| A-003 (neither `superclaude install` nor `make sync-dev` upgrades the CLI) | ACCEPT | Stated at `merged-requirements.md:1154`; consistent with both installs lacking `sweep` after primitives were synced. |
| A-004 (`/sc:sweep` fallback to `uv run` does not trigger on "No such command") | ACCEPT | `sc-sweep-protocol/SKILL.md:24`: "Only when step 1 fails with 'command not found' ... No other failure leads to this step". Click's "No such command" is a different failure. |

## Per-point verdicts

| Point | Superior variant | Reason |
|---|---|---|
| S-001 Section set | Tie | All three use the same five sections and four steps. |
| C-001 Delivery route | V2 | It is the owner's stated route and the spec's recommendation; it needs one addition (remove the shadow install) that V1 also eventually needs. |
| C-002 Time to SWEEP-RUNNABLE | V1 | Minutes versus a day plus four human steps; V3 is unbounded. Speed matters little while ORCA-AVAILABLE and Q24 are open, but V1 wins the point. |
| C-003 Effect on other workspaces | V2 | Every workspace gets the same reviewed pin; V1 and V3 change only this host or nothing. |
| C-004 Effect on running sessions | V3 | No restart and no reinstall under a live Run; V2 likely recreates the container (`main.tf:583-588`, inference). |
| X-001 Owner rule | V2 | Follows the rule and still delivers; V3 follows it only by not acting; V1 needs an exception. |
| X-002 Does the template route alone change the coordinator's CLI on this host | V2 | Only V2 states plainly that it does not unless the user install is removed, and `main.tf:594-597` confirms home persists; V3 only says "may", V1 sidesteps it. |
| X-003 Provenance | V2 | Reviewed, pinned, image-built commit with build-time provenance checks (`Dockerfile.coder:298-321`). |
| A-001 Coordinator `PATH` | V3 | Only V3 makes no `PATH`-dependent change and re-checks before claiming the gate; V1 and V2 both reason from the worker's observed `PATH`. |
| A-002 Safety of removing or replacing the user install | V3 | V3 touches no install; V1 replaces `ic` and `superclaude` silently, V2 needs removal without naming who checks it. |

## Overall pick

V2 amended to include removing the persistent `~/.local/bin` user install (owner-approved, checked in the coordinator's own environment), with V3's "not runnable, XC-04 held" record as the interim state until both steps have run.
