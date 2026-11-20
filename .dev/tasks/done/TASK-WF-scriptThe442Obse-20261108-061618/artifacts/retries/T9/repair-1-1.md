a4bb361e1c6375fe1dedddd00ccf6192329f8a51

# repair-1-1.md (repair round after the failing review r1-2)

family runbook-overclaim, one file: .dev/issues/442/observation-runbook.md (plus the case in runbook-selftest.sh).
search command: sed -n "/^### 4\.2/,/^## 5\./p;/^## 6\. Scripted path/,/^## Appendix/p" observation-runbook.md | grep -n -i -e "sent nothing" -e "could not authenticate" -e "every network" -e "only when" -e "never "
hits before: the "every script" sentence (fixed in the fix pass), the NEEDS_INPUT bullet ("sent nothing"), the BLOCKED bullet ("could not authenticate", fixed to "usually"), the "never copy credential files" sentence (true).
after: the NEEDS_INPUT bullet says the prompt may already have been sent and not to send it again, and that the session scripts print it as PENDING; the BLOCKED bullet says claude -p failed, usually on authentication; the timeout sentence names the calls it covers and says the interactive sessions are bounded by the driver wait; case sec6-needs-input-after-send added.
applied tree=9295b3b87ce56324ee611d4869e7c334b9a745dc
