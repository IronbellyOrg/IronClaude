# Discriminator: uptime-regex
Hypothesis A: the pseudo-file is served non-seekable so the shell's 1-byte read fallback fails
Hypothesis B: temp dir unwritable at mktemp
Observable that differs: uptime-regex — emitted at test-startup-boot.sh:444 as seed-diag-uptime-regex
Exact probe: IFS=' ' read -r up _ < /proc/uptime; [[ $up =~ ^[0-9] ]]
Primitive under dispute, fetched verbatim: procUptime.go Open() sets nonSeekable=true; bash read.def lseek ESPIPE -> zread(fd,&c,1)
Reference-context value: true
Pre-registered outcome table (written before the probe runs):
| Probe result | A | B |
|---|---|---|
| true  | refuted | consistent |
| false | consistent | consistent |
Falsifier sentence: "If uptime-regex=true on the next run, A is false."
Self-consistency: if Reference-context value ≠ the value actually observed in the reference context, mark THIS PROBE `suspect` under Grounding Gaps; do not read the outcome table for it.
