# Behaviour definitions
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | bash reserved word [[ | is recognized only when unquoted; a quoted or escaped [[ is an ordinary command word | bash manual, Reserved Words / QUOTING | the clause that specifies that quoted reserved words are not recognized | observed:this run (tier1-observation.md: `\[\[ a \]\]` and `"[[" a ]]` give `[[: command not found`, then the fake python3 ran) |
| 2 | bash process substitution <(...) | is a word (here a redirect target); the command word of the simple command follows it | bash manual, Process Substitution / Redirections | the clause that specifies process substitution as a word expansion | observed:this run (`< <(printf "") python3 -c 1` ran the fake python3) |
| 3 | bash arithmetic expansion $(( )) | performs command substitution (including backticks) on its contents before evaluation | bash manual, Arithmetic Expansion ("undergoes ... command substitution") | the clause that specifies the expansions applied inside $(( )) | observed:this run (`echo $(( \`python3 -c 1\` + 1 ))` ran the fake python3) |
