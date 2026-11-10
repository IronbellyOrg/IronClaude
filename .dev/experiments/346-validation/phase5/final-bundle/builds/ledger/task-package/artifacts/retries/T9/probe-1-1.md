3765a9239b895a1af7de3f92acf1dfc00ef48ad5
## family readme-fill-values
defect form: a README fill-value claim that does not match the brief text
command: grep -n -o -e "overstated citations" -e "both citations" -e "24 round-1 findings" -e "N1-N13" .dev/brainstorms/346-ledger/briefs/T07-R2-reviewer-L11-aff19d65.txt .dev/brainstorms/346-ledger/briefs/T08-R2-reviser-L10-66468bab.txt .dev/brainstorms/346-ledger/briefs/T09-R3-reviewer-L11-1c9a7ec8.txt .dev/brainstorms/346-ledger/briefs/README.md
before:
.dev/brainstorms/346-ledger/briefs/T07-R2-reviewer-L11-aff19d65.txt:1:24 round-1 findings
.dev/brainstorms/346-ledger/briefs/T08-R2-reviser-L10-66468bab.txt:1:N1-N13
.dev/brainstorms/346-ledger/briefs/T08-R2-reviser-L10-66468bab.txt:1:overstated citations
.dev/brainstorms/346-ledger/briefs/T08-R2-reviser-L10-66468bab.txt:1:N1-N13
.dev/brainstorms/346-ledger/briefs/T08-R2-reviser-L10-66468bab.txt:1:both citations
.dev/brainstorms/346-ledger/briefs/T09-R3-reviewer-L11-1c9a7ec8.txt:1:N1-N13
.dev/brainstorms/346-ledger/briefs/T09-R3-reviewer-L11-1c9a7ec8.txt:1:overstated citations
.dev/brainstorms/346-ledger/briefs/README.md:37:N1-N13
.dev/brainstorms/346-ledger/briefs/README.md:46:24 round-1 findings
.dev/brainstorms/346-ledger/briefs/README.md:46:N1-N13
.dev/brainstorms/346-ledger/briefs/README.md:46:overstated citations
coupled sites: README fill-values bullet
after:
37:N1-N13
46:24 round-1 findings
46:N1-N13
46:overstated citations
after (corrected; the "after:" block above was captured before the edit applied):
37:N1-N13
46:24 round-1 findings
46:N1-N13
46:overstated citations
46:both citations
46:overstated citations
