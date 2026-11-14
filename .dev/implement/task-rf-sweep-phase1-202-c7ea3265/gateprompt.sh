#!/usr/bin/env bash
# Build the prompt for a QA-gate report-only lens agent straight from the item text (so the quoted texts stay verbatim).
# usage: gateprompt.sh T12   -> writes work/T12/gate-prompt.txt, prints its path, the output path and the subagent type
set -u
R=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
D=$R/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
id=$1
mkdir -p "$D/work/$id"
[ -f "$D/work/$id/brief.txt" ] || bash "$D/brief.sh" "$id" >/dev/null
perl -0777 -ne '
  my $t = $_;
  my ($ctx) = $t =~ /\n  - \*\*Context\*\*: (.*?)\n  - \*\*Action\*\*/s;
  my ($act) = $t =~ /\n  - \*\*Action\*\*: (.*?)\n  - \*\*Output\*\*/s;
  my ($out) = $t =~ /\n  - \*\*Output\*\*: `([^`]+)`/s;
  my ($pre) = $act =~ /preamble, verbatim: "(.*?)" Then this lens prompt: "/s;
  my ($lens) = $act =~ /Then this lens prompt: "(.*?)" Pass it the input list/s;
  my ($scope) = $act =~ /scope note, verbatim: "(.*?)" For this item, spawn/s;
  my ($stype) = $act =~ /spawn one `([a-z-]+)` agent/s;
  die "parse failure: pre=" . (defined $pre ? 1 : 0) . " lens=" . (defined $lens ? 1 : 0) . " scope=" . (defined $scope ? 1 : 0) . " out=" . (defined $out ? 1 : 0) . "\n" unless defined $pre && defined $lens && defined $scope && defined $out;
  open(my $fh, ">", "'"$D"'/work/'"$id"'/gate-prompt.txt") or die;
  print $fh "$pre\n\n$lens\n\n$scope\n\nInputs and sizing (from the task item, read inputs in chunks of at most 150 lines): $ctx\n\nWrite your report to exactly this path, and write no other file: $out\n";
  close $fh;
  print "$out\n" . ($stype // "UNKNOWN") . "\n";
' "$D/work/$id/brief.txt" | { read -r outp; read -r st; echo "prompt: $D/work/$id/gate-prompt.txt"; echo "output: $outp"; echo "subagent_type: $st"; }
