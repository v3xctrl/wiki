# GPS Setup

V3XCTRL supports GPS for live position telemetry displayed in the viewer OSD (fix type, satellite count, coordinates, speed).

## Supported Modules

| Module type | Protocol | Notes |
|---|---|---|
| u-blox M8/M9/M10 | `ublox` | Supported - auto-configured on startup |
| Generic NMEA (MediaTek, SiRF, etc.) | `nmea` | Planned |
| Modem-integrated GPS (SIMCOM SIM7600 etc.) | `modem` | Planned |

## Hardware Connection

!!! warning
    If your GPS module is rated for 5V power, use 5V, not 3.3V. Running at 3.3V causes very poor signal quality (CN0 8-22 dBHz instead of the required 32+ dBHz) and the module will not get a reliable fix.

Connect the GPS module to the Raspberry Pi GPIO header via UART:

| GPS pin | Pi pin | Pi GPIO |
|---|---|---|
| VCC | **5V (pin 2 or 4)** | - |
| GND | GND (pin 6) | - |
| TX | RX (pin 10) | GPIO 15 |
| RX | TX (pin 8) | GPIO 14 |

### Enable UART for GPS

The serial port is enabled by default on the v3xctrl image and the serial login shell is disabled during first boot. If you have re-enabled the serial console for debugging (see [UART](UART.md)), you need to disable it again to free up the port for GPS.

Check `/boot/firmware/cmdline.txt` for `console=serial0,115200`. If it is present, switch to [RW mode](FAQ.md#how-can-i-enable-rw-mode) and edit the file with a text editor to remove it.

Reboot after making changes. You can verify the port is available with:

```bash
ls -l /dev/serial0
```

> To re-enable the serial console for debugging later, see [UART](UART.md).


## Configuration

GPS settings live in `config.json` under the `telemetry.gps` key:

| Setting | Default | Description |
|---|---|---|
| `path` | `/dev/serial0` | Serial port the GPS module is connected to |
| `protocol` | `ublox` | GPS module protocol - `ublox`, `nmea`, or `modem` |
| `rateHz` | `5` | Output rate in Hz - used by `ublox`, ignored by other protocols for now |

Example:

```json
"gps": {
  "path": "/dev/serial0",
  "rateHz": 5
}
```

On startup the `ublox` driver tries 115200 baud first, then falls back to 9600. The module is auto-configured to UBX protocol and the requested output rate.


## Testing

Test GPS on the Pi with the diagnostic scripts. Run them via the v3xctrl venv:

```bash
sudo /opt/v3xctrl-venv/bin/python3 -m v3xctrl_telemetry.apps.read_gps
```


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


## Fix Times

TTFF (Time To First Fix) is how long the module takes to acquire a position fix after power-on.

| Condition | Expected TTFF |
|---|---|
| Warm start (service restart, module powered) | 5-15 s |
| Cold start (battery change / full power cycle) | 30-90 s |

After a cold start the module downloads fresh satellite data from scratch. This only happens on a full power cycle - restarting the v3xctrl service does not reset satellite memory.


## Troubleshooting

### OSD shows "NO GPS"

The GPS module is not communicating. Check:
- UART is enabled (`/dev/serial0` exists)
- Wiring is correct (TX/RX not swapped)
- Module is powered (5V)
- `path` in `config.json` matches the actual port

### Satellite acquisition is slow or fails

The LTE modem transmitting at high power (during video streaming) can interfere with GPS reception - the LTE bands overlap with the GPS L1 frequency (1575 MHz).

If you are having trouble getting a fix, try running only `v3xctrl-control` without video until a fix is acquired, then start the full stream. This reduces LTE transmission and gives the GPS module a better chance to acquire satellites.

### Fix acquired but then drops repeatedly

Likely causes:
- Obstructed sky view - move the antenna away from carbon fiber, metal, or other signal-blocking material
- RF interference - check MON-RF jamming indicator with `debug_gps`
- Weak power supply causing module resets - confirm stable 5V
