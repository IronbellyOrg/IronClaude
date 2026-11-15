# Locker hall requirements (an invented parent requirement document for the specification fixture)

## 4.1 Door timing

The door must open within `door_open_ms` of a valid code and must halt with `DoorTimeout` when it does not.

## 4.2 Pickup codes

A pickup code must expire after `code_ttl_min` minutes. The controller must never accept a code twice.

## 4.3 Alarm

The alarm shall sound only when `open_limit_s` is exceeded. The controller must write `alarm_events` to the log.

## Decisions

Q2: the open limit is one setting, read once at the start of a day.
