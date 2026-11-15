# Exporter retention rules (invented source for the plan fixtures)

## 2.1 Output formats

The exporter must support the formats csv, json, html and ndjson.

## 2.2 Guide

The guide must list the four formats and carry a section named Retention window.

## 2.3 Retention job

The job must write `deleted_count` to the run log and must halt with `RetentionError` when `age_limit_days` is unset. The purge step must skip a report whose `legal_hold` flag is set.

## 2.4 Notice

The notice must name the report id, state the expiry date, and give the appeal address.

## Decisions

Q4: the age limit is one setting, read once at the start of a run.
