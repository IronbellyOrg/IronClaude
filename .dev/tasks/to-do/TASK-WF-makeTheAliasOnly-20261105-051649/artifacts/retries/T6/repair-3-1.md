40950c4008013a396f395a09d8206bc392d6458a
reviewed=e52f672e732eef06f87ef805303e2a74a19d5ff8 ref=r3-1
F3.1 sev=blocking trigger=B2 ac=scope at=docs/reference/model-aliases.md:70 anchor=.dev/issues/384/analysis/probe-alias-remap.md:19 chk=n,y,n,n family=probe-scope-overstated fix=say the probe found ANTHROPIC_DEFAULT_OPUS_MODEL and ANTHROPIC_DEFAULT_HAIKU_MODEL accept tier ids and that ANTHROPIC_DEFAULT_SONNET_MODEL was not probed first=A3 origin=new: line 70 lists all three variables and says "the probe below found that these variables may hold tier ids". The probe record (line 19) says a tier id was accepted only for the opus and haiku variables, so the sonnet to claude-gw-tier1b mapping has no probe evidence.
applied tree=e80bbb4ed8cf6aca89f26f0667fedcaaa44def88
