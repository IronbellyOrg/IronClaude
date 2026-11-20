a4bb361e1c6375fe1dedddd00ccf6192329f8a51

# Family probe probe-3-1.md (failing review r3-1)

## family: needs-input-resend
defect form: an instruction that tells the reader not to resend a prompt after a stop that can occur both before the send (nothing sent) and after it (prompt sent).
search command: sed -n '/^### 4\.2/,/^## 5\./p;/^## 6\. Scripted path/,/^## Appendix/p' .dev/issues/442/observation-runbook.md | grep -n -i -e 'resend' -e 'not send' -e 'sent' -e 'already'
before-output (touched file, section line numbers):
  4: the prompts bullet in 4.2 ("A prompt sent with orca terminal send ..." not a resend instruction)
  28: the NEEDS_INPUT row ends "Do not resend the prompt."
  30: the reason=needs-input row says "do not resend the prompt"
coupled sites: the NEEDS_INPUT claim row says "Same as NEEDS_INPUT" and needs no change; runbook-selftest.sh checks each quote against its cited line, so the new driver.sh:55 quote is checked.
after: rows 28 and 30 say the line can come before or after the send and tell the reader to read the saved screen: send the step's prompt again only when it is not shown.
