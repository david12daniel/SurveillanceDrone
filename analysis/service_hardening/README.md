# D2.12 — Service Hardening for the Onboard Mission Application

**Task:** systemd unit, watchdog, logging, config, safe stand-down

**Status:** done + tested (unit tests + real ArduCopter SITL validation of the
safe-stand-down LAND sequence). This copy targets the **frozen**
[`analysis/autonomy_sim/mission_app.py`](../autonomy_sim/mission_app.py)
prototype, per the rest of this repo's convention (CLAUDE.md) — the
**production port lives in
[`DroneMissionApp`](https://github.com/david12daniel/DroneMissionApp)**
(`run_service.py` there, adapted to that repo's actual `MissionApp`/
`Detector`/`alerts` API; `mission_app_logging.py` and `SafeStandDown` carried
over unchanged). Keep both in sync if you touch the safe-stand-down or
config-merge logic here.

## Files in this directory

| File | Purpose |
|---|---|
| [`mission_app.service`](mission_app.service) | systemd unit template for the NanoPi M5 |
| [`mission_app_config.yaml`](mission_app_config.yaml) | Central configuration file (YAML) |
| [`mission_app_logging.py`](mission_app_logging.py) | Structured logging module (file rotation + stdout) |
| [`run_service.py`](run_service.py) | Service wrapper — config loading, logging init, signal handling, watchdog, safe stand-down |
| [`test_service_hardening.py`](test_service_hardening.py) | Unit tests (fake-connection SafeStandDown lifecycle, config deep-merge, logging extras, app construction) |
| [`../sitl_tests/test_service_hardening_sitl.py`](../sitl_tests/test_service_hardening_sitl.py) | Drives the real `SafeStandDown._safe_land()` against ArduCopter SITL |

## Integration point

The existing `MissionApp` in [`analysis/autonomy_sim/mission_app.py`](../autonomy_sim/mission_app.py) is the core autonomy loop. This module wraps it with a production-quality runtime layer:

1. Load config from YAML → `MissionApp.__init__()` kwargs
2. Initialize structured logging → replace bare `print()` / `self.events` with rotation-backed logs
3. Register signal handlers (SIGTERM, SIGINT) → graceful `set_mode(LAND)` before exit
4. Start a watchdog thread → touch a file every N seconds; systemd `WatchdogSec` monitors it
5. On any unhandled exception → log the traceback, attempt safe stand-down (RTL/LAND), then exit nonzero

## Deployment

Copy to the NanoPi M5 on first boot:

```bash
sudo cp mission_app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mission_app
sudo systemctl start mission_app
```

Config at `/etc/mission_app/config.yaml` (or modify the unit's `ExecStart` path).

## Dependencies on the M5

- Python 3.10+ (comes with FriendlyElec Ubuntu image)
- `pymavlink` (pip)
- `PyYAML` (pip) — used for config parsing; falls back to JSON if not available

## Design decisions

- **YAML config**: structured, comments OK, easier to maintain than env vars or CLI args for 20+ parameters. PyYAML is lightweight and available on the dev machine; the M5 gets it too.
- **JSON log format**: machine-parseable, works with systemd's journal, easy to pipe into `jq` during field debug. Each log line is a JSON object with `ts`, `level`, `module`, `msg`, and optional structured fields.
- **systemd watchdog** over internal watchdog: simpler, requires no kernel module, uses the same process lifecycle. The unit file sets `WatchdogSec=30`; the app calls `sd_notify("WATCHDOG=1")` every 10 s.
- **Safe-stand-down thread**: a separate daemon thread monitors a Python `Event` for crash detection; if the main loop exits unexpectedly, it sends a GUIDED → LAND sequence over a fresh MAVLink connection. This covers the case where the main thread crashes without a signal handler catching it (segfault in C extension, `os._exit()`, etc.).