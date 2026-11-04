# Behaviour definitions
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | bash function definition `name () compound-command` | defines a function and runs nothing; the name is not executed | bash manual, Shell Functions | the clause that specifies the function definition syntax | observed:this run (`python3() { uv run python "$@"; }; echo ready` printed only `ready`) |
| 2 | bash redirection `{varname}>` | allocates a file descriptor into varname; `{fd}` is part of the redirection, not a word, so the command word follows | bash manual, REDIRECTION ("{varname}") | the clause that specifies the {varname} redirection form | observed:this run (`{fd}>/dev/null python3 -c 1` ran the fake python3) |
