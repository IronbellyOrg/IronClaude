# Orca Worker Contract (synthetic, flg-r1 shape)

## 1. Dispatch

The coordinator dispatches each command as one worker task.

## 2. Questions

A worker asks the coordinator through the ask command.

## 3. Reports

A worker finishes with worker_done and a report path.

## 4. Retries

A failed task is retried once by the coordinator.

## 5. Glossary

A worker is a session that runs one command.
