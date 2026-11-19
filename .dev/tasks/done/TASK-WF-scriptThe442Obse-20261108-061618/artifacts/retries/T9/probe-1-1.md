a4bb361e1c6375fe1dedddd00ccf6192329f8a51

# Family probe probe-1-1.md (failing review r1-1)

## family: runbook-overclaim
defect form: a universal statement ("every script", "each script") in delivered runbook text that the scripts folder does not satisfy.
search command: sed -n '/^## 6\. Scripted path/,/^## Appendix/p' .dev/issues/442/observation-runbook.md | grep -n -i -e 'every script' -e 'every external' -e 'never ' -e 'all run' -e 'never run'
before-output (touched file, section 6 line numbers):
  3: "Every script is bash with set -u -o pipefail and umask 077 ... bounds every external call with timeout" (false for the two sourced helpers and for local pgrep)
  16: "Each script has a test, ..." (the helpers and session-a2.sh have no test of their own)
  21: "The scripts never copy credential files" (true: setup.sh stops with BLOCKED login-isolated-home)
coupled sites: runbook-selftest.sh needs a case that the two sentences are gone.
after: line 3 reads "Every script you run ... (the sourced helpers lib.sh and driver-helpers.sh rely on their caller) ... bounds every network, Orca, Git and Claude call with timeout"; line 16 reads "The tests are ..."; runbook-selftest.sh case sec6-no-overclaim.
