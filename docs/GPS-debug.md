# GPS Debug Reference

Reference values for interpreting output from `debug_gps_ublox.py` (u-blox modules only).

Run the script on the Pi:
```bash
cd /opt/v3xctrl-venv/lib/python3.11/site-packages
v3xctrl-python -m v3xctrl_telemetry.apps.debug_gps_ublox
```

> **Tip:** If satellite acquisition is slow during diagnosis, stop video streaming. LTE transmission can interfere with GPS reception at the L1 frequency (1575 MHz).

On exit, the script prints a warning summary:
```
Stopped. Total warnings: 3
```
If no warnings occurred, nothing is printed.

## NAV-PVT - Fix Type

| Value | Name                              | Meaning                                    |
|-------|-----------------------------------|--------------------------------------------|
| 0     | No Fix (`NO_FIX`)                 | No position fix                            |
| 1     | Dead Reckoning (`DR`)             | Dead reckoning only (no GNSS)              |
| 2     | 2D Fix (`2D`)                     | 2D fix (altitude not determined)           |
| 3     | 3D Fix (`3D`)                     | 3D fix - normal outdoor operation          |
| 4     | GNSS+Dead Reckoning (`GNSS+DR`)   | GNSS + dead reckoning combined             |
| 5     | Time Only (`TIME_ONLY`)           | Time-only fix                              |

**Expected:** `3D` in open sky. `NO_FIX` is normal during cold start (can take 30-60s).

## NAV-PVT - Satellite Count (`numSV`)

| Count | Assessment                                              |
|-------|---------------------------------------------------------|
| 0     | No satellites - antenna issue, obstruction, or reset   |
| 1-3   | Weak - fix may be lost or inaccurate                   |
| 4-6   | Good - stable 3D fix expected outdoors                 |
| 7+    | Excellent                                              |

**Warning threshold:** Drop of 2 or more satellites in one cycle is flagged.

## NAV-SAT - Signal Strength (CN0, dBHz)

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

## NAV-SAT - Satellite Health

| Value | Meaning                  |
|-------|--------------------------|
| 0     | Unknown                  |
| 1     | Healthy - normal         |
| 2     | Unhealthy - ignore data  |

## NAV-SAT - GNSS System IDs

| ID | System  |
|----|---------|
| 0  | GPS     |
| 1  | SBAS    |
| 2  | Galileo |
| 3  | BeiDou  |
| 4  | IMES    |
| 5  | QZSS    |
| 6  | GLONASS |

The u-blox M10 can track up to 3 GNSS systems simultaneously.

## MON-RF - Antenna Status

| Value | Name                  | Meaning                                          |
|-------|-----------------------|--------------------------------------------------|
| 0     | Initializing (`INIT`) | Initializing                                     |
| 1     | Unknown (`UNKN`)      | Status unknown                                   |
| 2     | OK                    | Antenna connected and working - normal           |
| 3     | Short (`SHORT`)       | Antenna short circuit - check connector/cable    |
| 4     | Open (`OPEN`)         | Antenna open circuit - check connector/cable     |

**Expected:** `OK`. `Short` or `Open` indicate a hardware problem.

## MON-RF - Antenna Power

| Value | Name             | Meaning                              |
|-------|------------------|--------------------------------------|
| 0     | Off (`OFF`)      | Antenna power off                    |
| 1     | On (`ON`)        | Antenna powered - normal             |
| 2     | Unknown (`UNKN`) | Unknown                              |

## MON-RF - Jamming Indicator (`jamInd`)

Continuous-wave jamming indicator. Scale: 0-255.

| jamInd | Assessment                                              |
|--------|---------------------------------------------------------|
| 0-20   | No jamming                                             |
| 21-50  | Low - likely normal variation                          |
| 51-100 | Elevated - possible interference nearby               |
| 101+   | High - likely active jamming or strong interference   |

**Warning threshold:** > 50.

Note: This indicator responds to narrow-band (CW) interference only.

## MON-RF - Jamming State (flags bits 0-1)

| Value | State    | Meaning                                             |
|-------|----------|-----------------------------------------------------|
| 0     | Unknown  | Jamming detection not available                    |
| 1     | OK       | No jamming detected - normal                       |
| 2     | Warning  | Jamming detected                                   |
| 3     | Critical | Strong jamming - position may be unreliable        |

## MON-RF - Gain (`agcCnt`)

Automatic gain control counter. Reflects the receiver's gain adjustment to maintain signal levels.

| Behavior          | Possible cause                                     |
|-------------------|----------------------------------------------------|
| Stable            | Normal RF environment                              |
| Sudden drop       | Increased noise floor - possible wideband interference |
| Very low          | Strong signal or close jamming source             |

No fixed threshold - watch for sudden changes relative to baseline.

## MON-RF - Noise per ms (`noisePerMS`)

Background RF noise measurement.

| noisePerMS | Assessment                          |
|------------|-------------------------------------|
| 80-120     | Normal outdoor environment          |
| > 150      | Elevated noise - possible interference |
| > 200      | High noise - likely RF issues nearby |

## Typical Healthy Output (open sky, 3D fix)

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
Each satellite in the used: and unhealthy: groups is shown as {SYSTEM}{ID}({CN0}dBHz {elevation}°). For example, GPS1(38dBHz 55°) is GPS satellite 1 with a signal strength of 38 dBHz at 55° above the horizon. Higher elevation generally means better signal.

If `antenna=OK` and `jamming` is low during a drop, the cause is likely signal obstruction, LTE interference, or a brief module reset - not an antenna or RF hardware problem.

## Warnings

All warnings are prefixed with `[WARN]` and included in the exit summary count.

| Warning | Meaning |
|---------|---------|
| `satellites dropped N -> M` | Satellite count dropped by 2 or more in one cycle |
| `N used satellite(s) below signal threshold (25dBHz)` | N satellites used for position have weak CN0 |
| `No fix - strongest visible satellite only NdBHz, below acquisition threshold (25dBHz) for ephemeris/almanac data` | No fix and visible satellites too weak to download navigation data |
| `Antenna status: Short/Open` | Hardware problem - check connector and cable |
| `Jamming indicator high: N/255` | Jamming indicator above threshold (50) |
| `Jamming state: Warning/Critical` | Module flagged active jamming |
| `unexpected fixType=N` | Unknown fix type reported by module |
