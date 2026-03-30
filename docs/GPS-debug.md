# GPS Debug Reference

Reference values for interpreting output from `debug_gps.py` (u-blox M10, RushFPV GNSS Mini).

Run the script on the Pi:
```bash
cd /opt/v3xctrl-venv/lib/python3.11/site-packages
v3xctrl-python -m v3xctrl_telemetry.apps.debug_gps
```

> **Tip:** If satellite acquisition is slow during diagnosis, stop video streaming. LTE transmission can interfere with GPS reception at the L1 frequency (1575 MHz).

On exit, the script prints a warning summary:
```
[WARN] Stopped. Total warnings: 3
```
If no warnings occurred, nothing is printed.

---

## NAV-PVT - Fix Type

| Value | Name        | Meaning                                    |
|-------|-------------|--------------------------------------------|
| 0     | NO_FIX      | No position fix                            |
| 1     | DR          | Dead reckoning only (no GNSS)              |
| 2     | 2D          | 2D fix (altitude not determined)           |
| 3     | 3D          | 3D fix - normal outdoor operation          |
| 4     | GNSS+DR     | GNSS + dead reckoning combined             |
| 5     | TIME_ONLY   | Time-only fix                              |

**Expected:** `3D` in open sky. `NO_FIX` is normal during cold start (can take 30-60s).

---

## NAV-PVT - Satellite Count (`numSV`)

| Count | Assessment                                              |
|-------|---------------------------------------------------------|
| 0     | No satellites - antenna issue, obstruction, or reset   |
| 1-3   | Weak - fix may be lost or inaccurate                   |
| 4-6   | Good - stable 3D fix expected outdoors                 |
| 7+    | Excellent                                              |

**Warning threshold:** Drop of 2 or more satellites in one cycle is flagged.

---

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

---

## NAV-SAT - Satellite Health

| Value | Meaning                  |
|-------|--------------------------|
| 0     | Unknown                  |
| 1     | Healthy - normal         |
| 2     | Unhealthy - ignore data  |

---

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

---

## MON-RF - Antenna Status

| Value | Name     | Meaning                                          |
|-------|----------|--------------------------------------------------|
| 0     | INIT     | Initializing                                     |
| 1     | UNKN     | Status unknown                                   |
| 2     | OK       | Antenna connected and working - normal           |
| 3     | SHORT    | Antenna short circuit - check connector/cable    |
| 4     | OPEN     | Antenna open circuit - check connector/cable     |

**Expected:** `OK`. `SHORT` or `OPEN` indicate a hardware problem.

---

## MON-RF - Antenna Power

| Value | Name | Meaning                              |
|-------|------|--------------------------------------|
| 0     | OFF  | Antenna power off                    |
| 1     | ON   | Antenna powered - normal             |
| 2     | UNKN | Unknown                              |

---

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

---

## MON-RF - Jamming State (flags bits 0-1)

| Value | State    | Meaning                                             |
|-------|----------|-----------------------------------------------------|
| 0     | unknown  | Jamming detection not available                    |
| 1     | ok       | No jamming detected - normal                       |
| 2     | WARNING  | Jamming detected                                   |
| 3     | CRITICAL | Strong jamming - position may be unreliable        |

---

## MON-RF - AGC Count (`agcCnt`)

Automatic gain control counter. Reflects the receiver's gain adjustment to maintain signal levels.

| Behavior          | Possible cause                                     |
|-------------------|----------------------------------------------------|
| Stable            | Normal RF environment                              |
| Sudden drop       | Increased noise floor - possible wideband interference |
| Very low          | Strong signal or close jamming source             |

No fixed threshold - watch for sudden changes relative to baseline.

---

## MON-RF - Noise per ms (`noisePerMS`)

Background RF noise measurement.

| noisePerMS | Assessment                          |
|------------|-------------------------------------|
| 80-120     | Normal outdoor environment          |
| > 150      | Elevated noise - possible interference |
| > 200      | High noise - likely RF issues nearby |

---

## Typical Healthy Output (open sky, 3D fix)

```
NAV-PVT  fix=3D  sats=7  lat=48.123456  lon=11.567890  speed=0.0 km/h
NAV-SAT  7 svs  | *GPS1 CN0=38 el=55 | *GPS3 CN0=32 el=22 | *GAL5 CN0=36 el=41 | ...
MON-RF   ant=OK pwr=ON jam=4/255 state=ok agc=8190 noise=98
```

In NAV-SAT, satellites prefixed with `*` are actively used in the navigation solution. Satellites without `*` are tracked but not contributing to the fix (low signal, wrong elevation, or unhealthy).

---

## Typical Output During Satellite Drop

```
NAV-PVT  fix=3D  sats=4  lat=...
NAV-PVT  fix=NO_FIX  sats=0  lat=--  lon=--  speed=--
[WARN] sats dropped 4 -> 0
NAV-SAT  0 svs  |
MON-RF   ant=OK pwr=ON jam=?/255 state=ok agc=? noise=?
```

If `ant=OK` and `jam` is low during a drop, the cause is likely signal obstruction, LTE interference, or a brief module reset - not an antenna or RF hardware problem.
