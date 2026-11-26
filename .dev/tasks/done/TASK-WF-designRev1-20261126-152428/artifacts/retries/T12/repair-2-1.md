2a7b88e58a97f880e9155f3d02db7a78807d56e3
reviewed=d40ba11ee07691df05ce05b8bfba2f26881a4500 ref=r2-1
F3.1 sev=blocking trigger=B2 ac=scope at=.dev/issues/837/handoff-ryan.md:74 anchor=.dev/issues/837/handoff-ryan.md:68 chk=n,y,n,n family=selftest-path fix=add a RULESET_FILE variable naming the ruleset file in a separate checkout of IronClaude and read it with jq from that path first=A1 origin=late: Line 68 says to run the self-test from a scratch clone of the target repository, but line 74 reads the ruleset file by a relative path that exists only in an IronClaude checkout, so in the scratch clone jq fails, no scratch ruleset is created and the empty-commit push is not refused.
applied tree=102ecdb1d9b2597301645bb201c4a2bf6ba34547
