start=55748bc9c1a8c925093d8afc7a84700ab26b235a tree=da148da3b864efabea732b16f27511c355e00c0d
AC T7.AC1 met .dev/issues/442/scripts/evidence-selftest.sh:59-73
AC T7.AC2 met .dev/issues/442/scripts/evidence-selftest.sh:78-87
AC T7.AC3 met .dev/issues/442/scripts/evidence-selftest.sh:99-104 (caveat: pinned runbook line range 505-520)
AC T7.AC4 met .dev/issues/442/scripts/evidence-selftest.sh:169-184
AC T7.AC5 met .dev/issues/442/scripts/evidence-selftest.sh:161-165
F7.1 sev=blocking trigger=B4 ac=T7.AC4 at=.dev/issues/442/scripts/evidence.sh:21 anchor="`gh[pousr]_[A-Za-z0-9]{20,}`, `github_pat_`, `sk-[A-Za-z0-9]`, `CLICKUP_API_TOKEN=`, `Bearer `" chk=amiss:n,false:n,harm:n,constraint:y family=secret-scan-pattern fix="use the plan's exact patterns and neutralise the literal word task-notification before the scan and the redaction instead of narrowing sk-" first=A1 origin=new: the scan used (^|[^A-Za-z0-9_])sk-[A-Za-z0-9], not the plan's quoted pattern; the plan text is at TASK-WF-scriptThe442Obse-20261108-061618.md:194 (Read back, quoted words present)
F7.2 sev=blocking trigger=B2 ac=scope at=.dev/issues/442/scripts/evidence.sh:191 anchor=.dev/issues/442/observation-runbook.md:467 chk=amiss:n,false:y,harm:n,constraint:n family=item7-false-fail fix="limit the another-form test to names that do not start with mcp__ and add a self-test line" first=A1 origin=new: an MCP tool such as mcp__slack__send_message matched send_?message and gave FAIL, though runbook line 467 says MCP tools arrive as mcp__<server>__<tool> (Read back, quoted words present)
F7.3 sev=minor trigger=none ac=scope at=.dev/issues/442/scripts/session-gov.sh:225 anchor=none chk=amiss:n,false:n,harm:n,constraint:n family=inode-unreadable fix="record PENDING when the claim printed no inode number" first=A1 origin=new: an unreadable inode in the claim made OB-H2 FAIL
F7.4 sev=minor trigger=none ac=T7.AC4 at=.dev/issues/442/scripts/evidence.sh:54 anchor=none chk=amiss:n,false:n,harm:n,constraint:n family=redact-order fix="redact before cut; redact single-item output" first=A1 origin=new: cut runs before redact, so a token split at column 240 could leave a prefix; single-item stdout is not redacted

--- re-review r1-2 tree=b4ac99c26790c217df357a90b08a40918a164f99 ---
F7.1 resolved
F7.2 resolved
No new findings; T7.AC1 to AC5 met. F7.3 and F7.4 (minor) were also fixed in the same pass.
