# Widget service spec

## 1. Scope

The widget service stores widgets for the billing team. It keeps one record per widget.

## 2. Requirements

| ID | Requirement | Check |
|---|---|---|
| FR-1 | The service rejects a widget whose owner is missing or empty. | unit test |
| FR-2 | The service keeps deleted widgets for 30 days, then purges them. | unit test |

The cache is refreshed every hour.

## 3. Failure handling

When the store is down, the service returns 503 to the caller. Retries are left to the caller.

## 4. Operations

The cache is refreshed every hour.

Logs are kept for seven days.
