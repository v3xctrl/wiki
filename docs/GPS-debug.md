# GPS Debug Reference

Reference values for interpreting output from `debug_gps_ublox.py` (u-blox modules only).

!!! info
    This is a debug reference only. The GPS module handles all satellite selection,
    signal thresholds, and fix decisions automatically - these values cannot be manually configured.

Run the script on the Streamer:
```bash
cd /opt/v3xctrl-venv/lib/python3.11/site-packages
v3xctrl-python -m v3xctrl_telemetry.apps.debug_gps_ublox
```

> **Tip:** If satellite acquisition is slow during diagnosis, stop video streaming. LTE transmission can interfere with GPS reception at the L1 frequency (1575 MHz).


## NAV-PVT - Navigation Position, Velocity and Time

Reports the current position fix, satellite count, coordinates, and speed.

### Fix Type

| Fix Type              | Meaning                                                           |
|-----------------------|-------------------------------------------------------------------|
| No Fix                | No position fix - normal during cold start (up to 60s)           |
| Dead Reckoning        | Position estimated from motion sensors; no GNSS signal available |
| 2D Fix                | Horizontal position only - altitude not determined               |
| 3D Fix                | Full position fix - normal outdoor operation                     |
| GNSS+Dead Reckoning   | GNSS combined with motion sensor data                            |
| Time Only             | Time synchronized but no position fix                            |

**Expected:** `3D Fix` in open sky. `No Fix` is normal during cold start (up to 60s). Weak signal, jamming, or obstructions can significantly delay acquisition.

### Satellite Count (`satellites`)

| Count | Assessment                                              |
|-------|---------------------------------------------------------|
| 0     | No satellites - antenna issue, obstruction, or reset   |
| 1-3   | Weak - fix may be lost or inaccurate                   |
| 4-6   | Good - stable 3D fix expected outdoors                 |
| 7+    | Excellent                                              |

**Warning threshold:** Drop of 2 or more satellites in one cycle is flagged.

## NAV-SAT - Navigation Satellites

Per-satellite signal data for all satellites the module can see. Satellites are grouped as `used:` (actively contributing to the position fix), `seen:` (visible but not used), and `unhealthy:` (flagged by the module as unreliable and excluded from position calculation). The module can track up to 3 systems simultaneously: GPS, SBAS, Galileo, BeiDou, IMES, QZSS, GLONASS.

### Signal Strength (CN0, dBHz)

Carrier-to-noise density ratio per satellite. Higher is better.

| CN0 (dBHz) | Assessment                                    |
|------------|-----------------------------------------------|
| < 20       | Very weak - unusable                          |
| 20-25      | Poor - may not contribute to fix              |
| 25-30      | Marginal                                      |
| 30-35      | Good                                          |
| 35-45      | Excellent - clear sky view                    |
| > 45       | Outstanding                                   |

**Warning threshold:** < 25 dBHz for a satellite actively used in the nav solution.

Minimum to decode navigation data from a satellite: ~32 dBHz.

## MON-RF - RF Monitor

Antenna status and RF interference data reported by the module.

### Antenna Status

Expected: `OK power=On` - antenna connected and powered. `Short` or `Open` indicate a hardware problem - check the connector and cable. `Unknown` is normal for passive antennas (the module cannot detect passive antenna presence). `Initializing` appears briefly on startup.

### Jamming Indicator

Continuous-wave jamming indicator. Scale: 0-255.

| jamming | Assessment                                             |
|--------|---------------------------------------------------------|
| 0-20   | No jamming                                             |
| 21-50  | Low - likely normal variation                          |
| 51-100 | Elevated - possible interference nearby               |
| 101+   | High - likely active jamming or strong interference   |

**Warning threshold:** > 50.

Note: This indicator responds to narrow-band (CW) interference only.

### Jamming State

Expected: `OK` - no jamming. `Warning` means jamming detected. `Critical` means strong jamming - position may be unreliable. `Unknown` means jamming detection is not available on this module.

### Gain

Automatic gain control counter. Reflects the receiver's gain adjustment to maintain signal levels.

- **Stable** - normal RF environment
- **Sudden drop** - increased noise floor, possible wideband interference
- **Very low** - strong signal or close jamming source

No fixed threshold - watch for sudden changes relative to baseline.

### Noise per ms

Background RF noise measurement.

| noise | Assessment                               |
|-------|------------------------------------------|
| 80-120     | Normal outdoor environment          |
| > 150      | Elevated noise - possible interference |
| > 200      | High noise - likely RF issues nearby |

## Typical Healthy Output (open sky, 3D fix)

Each satellite in the `used:` and `unhealthy:` groups is shown as `{SYSTEM}{ID}({CN0}dBHz {elevation}°)`. For example, `GPS1(38dBHz 55°)` is GPS satellite 1 with a signal strength of 38 dBHz at 55° above the horizon. Higher elevation generally means better signal.

```
[16:11:06.064] POSITION [NAV-PVT]  fix=3D Fix  satellites=7  lat=48.123456  lon=11.567890  speed=0.0 km/h
[16:11:06.116] SATELLITES [NAV-SAT]  7 used / 24 visible
               used:        GPS1(38dBHz 55°)  GPS3(32dBHz 22°)  GAL5(36dBHz 41°)  ...
               seen:        17 satellites
[16:11:06.245] RF-STATUS [MON-RF]  antenna=OK power=On jamming=4/255 state=OK gain=8190 noise=98
```

## Typical Output During Satellite Drop

```
[16:11:05.064] POSITION [NAV-PVT]  fix=3D Fix  satellites=4  lat=48.123456  lon=11.567890  speed=1.2 km/h
[16:11:06.064] POSITION [NAV-PVT]  fix=No Fix  satellites=0  lat=--  lon=--  speed=--
[WARN] satellites dropped 4 -> 0
[16:11:06.116] SATELLITES [NAV-SAT]  0 used / 0 visible
               used:        (none)
[16:11:06.245] RF-STATUS [MON-RF]  antenna=OK power=On jamming=5/255 state=OK gain=8190 noise=100
```

If `antenna=OK` and `jamming` is low during a drop, the cause is likely signal obstruction, LTE interference, or a brief module reset - not an antenna or RF hardware problem.

## Warnings

All warnings are prefixed with `[WARN]`.

| Warning | Meaning |
|---------|---------|
| `satellites dropped N -> M` | Satellite count dropped by 2 or more in one cycle |
| `N used satellite(s) below signal threshold (25dBHz)` | N satellites used for position have weak CN0 |
| `No fix - strongest visible satellite only NdBHz, below acquisition threshold (25dBHz) for ephemeris/almanac data` | No fix and visible satellites too weak to download navigation data |
| `Antenna status: Short/Open` | Hardware problem - check connector and cable |
| `Jamming indicator high: N/255` | Jamming indicator above threshold (50) |
| `Jamming state: Warning/Critical` | Module flagged active jamming |
| `unexpected fixType=N` | Unknown fix type reported by module |

For full protocol details, see the [u-blox M10 Interface Description](https://www.u-blox.com/docs/UBX-21035062).
