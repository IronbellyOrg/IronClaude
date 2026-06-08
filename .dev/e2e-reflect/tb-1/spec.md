# Spec: Sandbox Config `version` Field (e2e tb-1)

A tiny, self-contained spec for an e2e test of the task-builder PRE reflect gate.
All work is confined to `.dev/e2e-reflect/tb-1/work/`.

## Functional Requirements

- **FR-1** Create `.dev/e2e-reflect/tb-1/work/config.yaml` containing a top-level
  `version: "1.0.0"` field.
- **FR-2** Add a top-level `name: "e2e-sandbox"` field to the same file.
- **FR-3** Create `.dev/e2e-reflect/tb-1/work/README.md` documenting the two
  fields in a small table.

## Non-Functional Requirements

- **NFR-1** All files live under `.dev/e2e-reflect/tb-1/work/`; no other path is touched.
