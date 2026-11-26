# Locker door controller specification

Parent: ./parent1.md

## 1. Purpose

The controller opens one locker door when a valid pickup code is entered. It shall serve one hall of lockers.

## 2. Door behaviour

Source sections: 4.1, 4.2

The controller shall open the door within 3 seconds of a valid code.
The controller shall log each open event with the locker number.
The controller must refuse a code that has expired.
The controller shall never open two doors for one code.
This section applies to every locker model in the hall.
Add the heading "Locker hours" to `docs/locker-guide.md`, and the check `grep -c 'locker-hours' docs/locker-guide.md` shall print at least 1.

### Message format

```text
LOCKER 14 OPEN 2027-01-01T10:00:00
```

## 3. Alarm

Source sections: 4.3, Q2

A door that stays open longer than 60 seconds should raise an alarm.
The alarm tone shall be silenced when the door closes, and the controller must write `alarm_events` for each alarm.

## 4. Affects

- `src/locker/door.py`
- `src/locker/log.py`
- `docs/locker-guide.md`
- `src/locker/alarm.py`

## 5. Verification

- `make test` exits 0.
- `pytest tests/test_door.py` exits 0.
