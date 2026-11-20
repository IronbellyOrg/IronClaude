4ae82798c25abbfd4f726e36c1f674f43fa00bfd
family stale-fixed-prompt: a document still presents the old fixed watcher prompt as the only prompt
command: git grep -n -e "--pipeline none" -- src tests docs plugins
before: tech reference 1074 and 1416 and WORKER-CONTRACT.md:293 presented `--pipeline none` as the watcher prompt
coupled sites: SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md (265, 268, 1074, 1416, 1445), WORKER-CONTRACT.md:293, issue-watcher.md, issue-watcher-setup.md, docs/user-guide/commands.md
after: each remaining hit names `none` as one level of several, or is the claim command's own level documentation; reviewed hit by hit
