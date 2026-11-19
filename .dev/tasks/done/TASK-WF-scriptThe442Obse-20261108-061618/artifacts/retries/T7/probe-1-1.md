55748bc9c1a8c925093d8afc7a84700ab26b235a

# Family probe probe-1-1.md (failing review r1-1)

## family: secret-scan-pattern
defect form: a scan or redaction pattern narrowed away from the quoted plan pattern to avoid a false positive, instead of keeping the quoted pattern and neutralising the false-positive word.
search command: grep -n -e 'SECRET_RE' -e 'sk-' -e 'redact' .dev/issues/442/scripts/evidence.sh .dev/issues/442/scripts/evidence-selftest.sh
before-output (touched files):
  evidence.sh:20-21: SECRET_RE with the narrowed sk- term
  evidence.sh:52: redact() uses SECRET_RE
  evidence.sh:54: run_text pipes cut then redact
  evidence.sh:389: the results file goes through redact
  evidence.sh:393: the copy scan uses grep -rnIE with SECRET_RE
  evidence-selftest.sh:45 and :185: the task-notification case
coupled sites: the redaction (52, 54, 389) and the copy scan (393) must use the same rule; the self-test case at 185 must still pass.
after: SECRET_RE is the plan's exact list; both redact() and the scan first turn the literal word task-notification into task<SOH>notification (and redact turns it back), so the word is never a match; a planted xsk-abcd value is still a match.

## family: item7-false-fail
defect form: a negative test on a tool name that also matches the legitimate MCP name form.
search command: grep -n -e 'send_?message' -e 'contains("__")' -e 'another form' .dev/issues/442/scripts/evidence.sh
before-output (touched files):
  evidence.sh:191: any name matching send_?message other than SendMessage gives FAIL (also matches mcp__x__send_message)
  evidence.sh:192: names containing __ that do not start with mcp__ give FAIL (correct)
coupled sites: the PASS branch at 194 lists mcp__ names; the self-test needs a case with mcp__x__send_message.
after: line 191 tests only names that do not start with mcp__; self-test case item7-mcp-send-message-pass.
