c2ca8c108d05aa8e61b3821a29565a1567c92c1b

# Family probe probe-2-1.md (failing review r2-1)

## family: T2-probe-source
defect form: a file installed from a computed checkout root that does not hold the file; failure silent without set -e.
search command: grep -n -e 'install -m' -e 'cp -r' .dev/issues/442/scripts/setup.sh
before-output (touched files):
  setup.sh:68-70: install from "$MAIN/tests/hooks/fixtures/..." and "$HOME/.claude/hooks/..."; cp -r commands skills agents
coupled sites: setup.sh:24 (MAIN=$(main_checkout)); setup.sh:95 (ob-probe.sh execs "$OB/bin/log-only-probe.sh"); setup-selftest.sh:36-38 (layout loop must name bin/log-only-probe.sh).
after:
  setup.sh: probe and fixture install from ROOT (the script's own checkout, computed like setup-selftest.sh:7); the install is fatal on failure; cp -r of the real HOME dirs is bounded.
  setup-selftest.sh: layout loop asserts bin/log-only-probe.sh exists and is executable.

## family: T2-ac2-listing
defect form: an AC that asks for a before/after comparison but the test compares one post-run value.
search command: grep -n -e 'fake-claude-clean' -e 'FAKE' .dev/issues/442/scripts/setup-selftest.sh
before-output (touched files):
  setup-selftest.sh:59-61: ck fake-claude-clean "$(ls "$FAKE/.claude/commands" | wc -l)" 1
coupled sites: setup-selftest.sh:12-22 (fake HOME construction, the right place for the before snapshot).
after:
  setup-selftest.sh: before-snapshots listing+digest of $FAKE/.claude taken before the run; after-snapshots diffed with diff; case renamed fake-claude-clean (before/after diff empty).

## family: T2-timeout-wrap
defect form: external calls left unbounded while sibling calls are wrapped (plan Constraints).
search command: grep -n -e 'install ' -e 'cp -r' -e 'chmod ' -e 'mkdir ' .dev/issues/442/scripts/setup.sh
before-output (touched files):
  setup.sh:22,68,69,70,99,117,154: mkdir/install/cp/chmod unwrapped
coupled sites: lib.sh gh_fork/main_checkout wrappers (already bounded) and setup.sh run_check (bounded) show the pattern.
after:
  setup.sh: every external call (mkdir, install, cp -r, chmod) runs under timeout "$T" (or a fatal `|| exit` helper where a partial tree must not continue).

## family: T2-p3-label
defect form: a recorded-check header emitted after the check's output, mislabeling the log.
search command: grep -n -e '== P3' -e '== P2' .dev/issues/442/scripts/setup.sh
before-output (touched files):
  setup.sh:41-46: cmp output appended, then '== P3' header
coupled sites: setup-selftest.sh prec id loop (must include P2, P3).
after:
  setup.sh: '== P3' header precedes the cmp block; P2 block unchanged.
  setup-selftest.sh: prec loop checks P2 and P3 too.
