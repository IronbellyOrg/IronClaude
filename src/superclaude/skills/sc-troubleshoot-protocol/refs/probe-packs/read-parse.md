# read/parse pack — optional, append-only, cited

Loaded by Wave 1.6 S1.6.4 only when a `surviving=yes` producer's primitive kind is `read/parse`; rows are appended to the discriminator rows as extra probes and are never a decision input (refs/primitive-differential.md Section 2 step 3).

```bash
fstype=$(stat -f -c %T "$NODE")          # sysbox-fs: fuseblk
size=$(stat -c %s "$NODE")               # kernel procfs 0; FUSE emulation 4096
seekable=$(python3 -c "import os;f=os.open('$NODE',0);os.lseek(f,1,0);print(1)" 2>/dev/null||echo 0)
# add rows only with an incident citation; never a decision input
```
