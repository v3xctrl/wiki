# GPS Setup

V3XCTRL supports GPS for live position telemetry displayed in the viewer OSD.

---

## Supported Modules

| Module type | Protocol | Notes |
|---|---|---|
| u-blox M8/M9/M10 | UBX | Recommended - auto-configured on startup |
| Generic (MediaTek, SiRF, etc.) | NMEA | Outputs at module default rate (~1 Hz) |

The system auto-detects the protocol on startup. If detection fails, use `--gps-module` to force a specific protocol.

---

## Hardware Connection

Connect the GPS module to the Raspberry Pi GPIO header via UART:

| GPS pin | Pi pin | Pi GPIO |
|---|---|---|
| VCC | **5V (pin 2 or 4)** | - |
| GND | GND (pin 6) | - |
| TX | RX (pin 10) | GPIO 15 |
| RX | TX (pin 8) | GPIO 14 |

> **Important:** Use 5V power, not 3.3V. Running at 3.3V causes very poor signal quality (CN0 8-22 dBHz instead of the required 32+ dBHz) and the module will not get a reliable fix.

### Enable UART on the Pi

The serial port must be enabled before the GPS is accessible at `/dev/serial0`:

```bash
sudo raspi-config
# → Interface Options → Serial Port
# → "Would you like a login shell over serial?" → No
# → "Would you like the serial port hardware to be enabled?" → Yes
```

Or add this to `/boot/firmware/config.txt` manually:

```
enable_uart=1
```

Reboot after making changes.

---

## Configuration

GPS settings live in `config.json` under the `telemetry.gps` key:

| Setting | Default | Description |
|---|---|---|
| `path` | `/dev/serial0` | Serial port the GPS module is connected to |
| `rateHz` | `5` | NAV-PVT output rate in Hz (u-blox modules only) |

Example:

```json
"gps": {
  "path": "/dev/serial0",
  "rateHz": 5
}
```

> **Note:** For NMEA modules the rate setting is ignored - the module outputs at its own fixed rate (usually 1 Hz).

---

## Testing

Test GPS on the Pi with the diagnostic scripts:

### Basic position readout

```bash
python -m v3xctrl_telemetry.apps.read_gps
```

Prints fix type and coordinates as they update. Useful to confirm the module is working and a fix has been acquired.

### Full diagnostics

```bash
python -m v3xctrl_telemetry.apps.debug_gps
```

Shows detailed per-satellite signal strength (CN0), RF health (AGC, jamming), antenna status, and warns about signal issues. See [GPS-Debug-Reference](GPS-Debug-Reference.md) for how to interpret the output.

---

## Fix Times

| Condition | Expected TTFF |
|---|---|
| Warm start (service restart, module powered) | 5-15 s |
| Cold start (battery change / full power cycle) | 30-90 s |

After a cold start the module downloads fresh satellite data from scratch. This only happens on a full power cycle - restarting the v3xctrl service does not reset satellite memory.
