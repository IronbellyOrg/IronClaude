# Orca Worker Contract (synthetic, flg-r1 shape)

## 1. Dispatch

The coordinator dispatches each command as one worker task. It sends the brief and the report path with every task (R1.1).

## 2. Questions

A worker asks the coordinator through the ask command. Each question carries the task id and a timeout of ten minutes (R1.2).

## 3. Reports

A worker finishes with worker_done and a report path. The report path is absolute and lies inside the worker's worktree (R1.3).

## 4. Retries

A failed task is retried once by the coordinator. A retry reuses the task id and records the failed attempt (R1.4).

## 5. Glossary

A worker is a session that runs one command.
