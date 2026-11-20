b7f78e146c3cd9609e42262d6d9f1255269308b6
A1 r1-1 F9.1 minor tests/issue_watch/test_cycle.py:2972 ac=T9.AC2 n,n,n,n the between-examine-and-launch test passes even without the exclusion at the re-read, because a newer approval event id already fails revalidation
A1 r1-1 F9.2 note src/superclaude/cli/issue_watch/cli.py:208 ac=T9.AC3 n,n,n,n check-config stays silent when the account is already excluded or owner_account_id is unset (no gh call can read the account)
