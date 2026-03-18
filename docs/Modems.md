This is a knowledge base for supported modems. Documentation is sparse at times, so we have collected relevant information here in one place.

## Zero-4G-CAT1-Hub

This is the modem most widely available on AliExpress, sold under different names by different vendors. The actual OEM appears to be **Mcuzone**.
It comes in **four distinct versions**, usually labeled on top of the MCU:

| Model    | Bands | GPS | Speed |
|----------|-------|-----|-------|
| CAT1/LTE | 1, 3, 5, 8, 34, 38, 39, 40, 41 | No  | 10Mbps down, 5Mbps up. On Band 34 - 41: 6Mbps down, 4 Mbps up. |
| CAT1-GPS | 1, 3, 5, 8, 34, 38, 39, 40, 41 | No  | 10Mbps down, 5Mbps up. On Band 34 - 41: 6Mbps down, 4 Mbps up. |
| CAT1-EU  | 1, 3, 7, 8, 20, 28 | No  | 10Mbps down, 5Mbps up |
| CAT1-EA  | 1, 3, 5, 7, 8, 28 | No  | 10Mbps down, 5Mbps up |

> **TIP:** Check which LTE bands are used by your carrier in your area on [cellmapper.net](https://www.cellmapper.net/map) before purchasing a modem. See [Antennas](Antennas.md) for a detailed guide on evaluating bands in your region.


### Enabling All Factory-Supported Bands

Example for CAT1-GPS:

| Model    | AT command |
|----------|------------|
| CAT1-GPS | AT*BAND=5,0,0,482,149,1,1,0 |

### Debugging

> Before attempting any debugging, make sure your SIM card is set up correctly. See [SIM card preparation](SIM.md) and the [Troubleshooting modem section](Troubleshooting.md#modem) for common issues.

Connect to the modem using `minicom`:

```bash
minicom -D /dev/ttyACM0 -b 115200
```

#### Checking Network Registration

Run these commands to check modem status:

```bash
AT
AT+CPIN?
AT+COPS?
```

Example output:

```
# Check modem availability
AT
AT

OK

# Check SIM status
AT+CPIN?
AT+CPIN?

+CPIN: READY

OK

# Check operator registration
AT+COPS?
AT+COPS?

+COPS: 0,2,"23201",7

OK
```

* `23201` is the MCC/MNC (operator code).
* The last value `7` indicates LTE connection (other values may indicate GSM/UMTS).

At this point, the modem is successfully registered on the mobile network with LTE access.

#### Checking IP assignment
Registration does not guarantee an active data session. Check your PDP context:

```bash
AT+CGDCONT?
```

Expected output:

```bash
AT+CGDCONT?

+CGDCONT: 1,"IP","a1.net","10.54.1.125",0,0

OK
```

This indicates you have a valid IPv4 address.

If multiple contexts are active:

```bash
AT+CGDCONT?

+CGDCONT: 1,"IP","a1.net","10.54.1.125",0,0
+CGDCONT: 2,"IPV6","a1.net","fe80::1234",0,0

OK
```

List active contexts:

```bash
AT+CGACT?
```

```bash
+CGACT: 1,1
+CGACT: 2,1
```

Disable IPv6 if needed:

```bash
AT+CGACT=0,2
```

> **NOTE:** Context changes may reset after a modem reboot.

## AT command cheat sheet
Useful commands when evaluating or debugging new modems.

> For more advanced scripting, try [python ATlib](https://pypi.org/project/atlib).

### Get Firmware version:

```
AT+VER?
```

### Check Network Registration

```
AT+CREG?

# Not connected
+CREG: 0,0

# Connected
+CREG: 0,1
```

### Show Currently Used Band

```
AT*BANDIND?
*BANDIND: 0, 3, 7
```

Here, the middle number (`3`) is the LTE band currently in use.

## Modem Test
The following AT commands must be understood by the modem, otherwise ATlib has to be updated accordingly:

GSM and LTE commands should be understood by any modem, the rest might need some custom adaptations per modem.

```
# AIR780
get_allowed_bands()
AT*BAND?

get_active_band()
AT*BANDIND?

get_signal_quality()
AT+CESQ

# LTE
get_contexts()
AT+CGDCONT?

get_addresses()
AT+CGPADDR

# GSM
set_operator_auto()
AT+COPS=0

get_current_operator()
AT+COPS?

get_sim_status()
AT+CPIN?

get_version()
AT+VER?

enable_location_reporting()
AT+CREG=2

get_cell_location()
AT+CREG?
```