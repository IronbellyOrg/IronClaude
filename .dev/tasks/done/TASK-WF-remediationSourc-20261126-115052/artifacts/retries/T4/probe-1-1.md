c4746625edd447c9bd3b729e6a884dc6957f6809
## family: pr-body-condensed
defect form: the Pull request body part restates a part of the note in shortened form instead of carrying it
command: grep -n -F -e 'if the id still shows the upstream' -e 'if the id reverts' -e 'or reverts' ./artifacts/t4-pr-note.md
before-output (./artifacts/t4-pr-note.md): 57:If the id still shows the upstream, or reverts, the next try is the second state change|81:Fallback: if the id still shows the upstream, the next try is the second state change t|
coupled sites: ./artifacts/t4-pr-note.md:55-57 (Fallback part, already correct); ./artifacts/t4-pr-note.md:77 (body Evidence); ./artifacts/t4-pr-note.md:81 (body Fallback); the body's Owner checks and Issue 769 and Keyword parts were compared and carry their content
after: 57:If the id still shows the upstream, or reverts, the next try is the|115:Fallback: if the id still shows the upstream, or reverts, the next|
