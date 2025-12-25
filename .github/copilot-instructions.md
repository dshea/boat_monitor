# Copilot instructions for boat_monitor

Purpose: Quickly onboard an AI coding agent to the repo and provide actionable guidance

Core idea
- This repo collects sensor and pump data on a Raspberry Pi, stores it in a small local SQLite DB (`pi/boat.db`), exports JSON snapshots to `web/loadedFiles/`, and uses simple PHP pages in `web/phpTests/` to turn JSON into CSVs for static graphing.

Data flow
- Pi scripts (`pi/`) -> SQLite (`pi/boat.db`) -> JSON export (`pi/send_json.py` / `pi/boat_database.py`) -> `web/loadedFiles/` -> PHP import and CSV generation -> browser graphs (`web/chartTests/`).

Essential files to inspect
- `pi/boat_database.py`: DB schema helpers and JSON export (timestamps are integer epoch seconds). See `makeJSON()` and write helpers.
- `pi/bilge_pump.py`: Pump event capture (uses `gpiozero`) and `boat_database.writeBilge(name, duration)` calls.
- `pi/read_battery.py`: ADC + DHT reads, computes voltages, writes via `boat_database.writeBattery(...)`.
- `pi/read_adc.py`: ADC diagnostic script (prints raw/voltage), useful for hardware debugging.
- `pi/send_json.py`: Exporter placeholder — intended to call `boat_database.makeJSON()` and upload files to `web/loadedFiles/`.
- `web/phpTests/` and `web/chartTests/`: PHP readers and static graph CSVs; examples of expected JSON shape live in `web/`.

Project conventions (do not change without care)
- Timestamps: integer Unix epoch seconds everywhere.
- DB tables: `pump(time INT, name TEXT, duration INT)` and `battery(time INT, battery0 REAL, battery1 REAL, temperature REAL, humidity REAL)`.
- Pump `name` values are short (e.g., `main`, `backup`).
- Scripts are single-file procedural tools intended to run on a Pi; they often assume relative working dir is `pi/` and the DB file is `boat.db` in that working directory.

Environment & dependencies
- Hardware-specific libs: `gpiozero`, `board`, `busio`, `adafruit-ads1x15`, `Adafruit_DHT`. These require running on the Pi (or mocking) — imports will fail on macOS/desktops.
- I2C ADC: ADS1115 expected for voltage readings; DHT11 for temperature/humidity.

Key developer commands
- Inspect DB (quick):
  - sqlite3: `sqlite3 pi/boat.db` (query tables)
  - Python helper: `python3 -c "import pi.boat_database as b; b.dumpDatabase()"`
- Run one-off sensor read: `python3 pi/read_battery.py`
- Run ADC test: `python3 pi/read_adc.py` (Ctrl-C to stop)
- Run pump monitor (interactive): `python3 pi/bilge_pump.py` (requires GPIO hardware)

Integration notes & common pitfalls
- Many scripts will fail on non-Pi machines due to CircuitPython/GPIO imports — to develop on macOS, isolate or mock those imports.
- `send_json.py` is intentionally minimal; expect to extend it to call `boat_database.makeJSON()` and push files to `web/loadedFiles/` (e.g., via scp or HTTP upload).
- `boat.db` path is relative to where the script runs; prefer running scripts from `pi/` or refactor to accept an absolute DB path.

What an AI agent should do first
- Read `pi/boat_database.py`, then `pi/read_battery.py` and `pi/bilge_pump.py` to understand table usage.
- If adding features, keep timestamp format and DB schema stable; prefer adding new columns rather than renaming.
- When modifying exports, update `web/` sample JSONs (e.g., `web/2019-03-28T15:53:00.json`) to document the output shape.

If anything missing or you want this condensed into a checklist, tell me which focus (pi scripts, JSON export, or web import) to expand.
# Copilot instructions for boat_monitor

Purpose: Help an AI coding agent become productive quickly in this repository.

**Big Picture**
- **Overview:**: This repo contains Raspberry Pi data-collection scripts (`pi/`), a small SQLite-backed local database (`pi/boat.db` created by `pi/boat_database.py`), and a static web UI (`web/`) where the Pi uploads JSON snapshots for PHP pages to ingest and generate static CSVs for graphing.
- **Primary data flow:**: pump events & sensor reads (Pi) -> `pi/boat.db` (SQLite) -> periodic JSON export (`pi/send_json.py` / `pi/boat_database.py`) -> upload to `web/loadedFiles/` -> PHP pages import into web DB / CSV -> browser displays graphs.

**Key Files / Entry Points**
- **`pi/bilge_pump.py`**: Uses `gpiozero` to detect pump on/off events and writes pump records to the local DB via `pi/boat_database.writeBilge(name, duration)`.
- **`pi/read_battery.py`**: Reads ADC + DHT sensor values, computes battery voltages, and writes to DB via `boat_database.writeBattery(...)`.
- **`pi/read_adc.py`**: Quick ADC test script (prints raw and voltage values). Useful for hardware debugging.
- **`pi/boat_database.py`**: SQLite helpers (open/create DB, write records, dump). Timestamps are stored as integer Unix epoch seconds.
- **`pi/send_json.py`**: Intended uploader/exporter (currently minimal) — use `boat_database.makeJSON()` or extend `send_json.py` to create and transfer `web/*.json` files.
- **`web/phpTests/`**: PHP utilities that expect JSON files (e.g., `readJson.php`, `displayDatabase.php`) and generate CSVs for static graphing (`web/chartTests/`).

**Repo Conventions & Patterns**
- **Timestamps:**: Use integer Unix epoch seconds everywhere (see `boat_database` insertions).
- **DB layout:**: Table `pump(time INT, name TEXT, duration INT)` and `battery(time INT, battery0 REAL, battery1 REAL, temperature REAL, humidity REAL)`.
- **Naming:**: Pump names are short strings like `"main"` and `"backup"` (see `pi/bilge_pump.py`).
- **Single-file scripts:**: Most logic is procedural scripts runnable with `python3` from the `pi/` directory; they rely on running on a Raspberry Pi with I2C and GPIO available.

**Dependencies & Environment**
- **Python packages used on Pi:**: `gpiozero`, `board`, `busio`, `adafruit-ads1x15`, `Adafruit_DHT`, and standard `sqlite3`/`json` libs. Install these on the Pi, not on desktop, unless you mock hardware.
- **Hardware:**: ADC via I2C (ADS1115), DHT11 for temp/humidity, GPIO pins for pump switches and LEDs.

**Developer Workflows & Commands**
- **Inspect DB:**: `sqlite3 pi/boat.db` or run `python3 -c "import pi.boat_database as b; b.dumpDatabase()"` from repo root (adjust import path if running from `pi/`).
- **Run battery read once:**: `python3 pi/read_battery.py` (writes one point to DB).
- **Run ADC test:**: `python3 pi/read_adc.py` (continuous output, Ctrl-C to stop).
- **Run pump monitor (interactive):**: `python3 pi/bilge_pump.py` — this expects actual GPIO inputs and will block (use systemd or screen on Pi for long-running service).
- **Create JSON export:**: Extend or call `pi/boat_database.makeJSON(<earliest_epoch>)` to produce JSON snapshots for upload; the repository stores examples in `web/`.

**Integration Notes & Gotchas**
- **Running locally vs Pi:**: Many scripts import `board` and `busio` (CircuitPython). On non-Pi machines these imports fail — mock or run directly on target hardware.
- **`send_json.py` is a placeholder:**: The code currently only imports `time` — implement JSON generation and upload logic here if you want automated exports.
- **File locations matter:**: `boat.db` is created in the working directory where scripts run. Prefer running scripts from `pi/` or provide absolute DB path when refactoring.

If anything in these notes is unclear or you want more examples (e.g., a suggested `send_json.py` implementation, unit-test strategy, or systemd service file for the Pi), tell me which part to expand. 

---
Please review and tell me any missing pieces or preferred formatting for your agent instructions.
