This is a list of tested and recommended Hardware. **Recommended** means it has been tested by the developers and works well (presumably out of the box). This is not a complete list of all compatible Hardware, but if you run into issues, consider using something that has been extensively tested. See the [Shopping List](Shopping-List.md) for vendor links and pricing.

## Recommended

* [Raspberry PI Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
* [Cat 1, 4G Modem hat (comes in EU and US versions, with and without GPS)](https://s.click.aliexpress.com/e/_oB0K4If) - Explicitly tested firmware versions: `AirM2M_780EU_V1138_LTE_AT`
* [PiCam V3 (Wide) - only cam so far with HDR](https://www.raspberrypi.com/products/camera-module-3/)
* [INA231](https://aliexpress.com/item/1005008863593081.html) - smallest breakout board for the INA current/voltage sensor

## Cameras

| Cam | Pros | Cons | Setup | Settings |
|-----|------|------|-------|----------|
|Raspberry Pi Cam V3 | + HDR  <br/> + different FOV options <br/> + No IR option for darkness<br/> + good noise handling<br /> + high resolution (12MP)| - autofocus [^1]<br /> - expensive | Works out of the box | Brightness, Sharpness, Contrast, Saturation, Focus (Auto & Manual), Exposure (Auto & Manual), Gain (Auto & Manual) |
|Arducam 12MP IMX708|+ HDR<br/> + M12 lens [^2]<br/> + small PCB<br/> + high resolution (12MP)| - availability<br /> - expensive | [additional Setup](#arducam-12mp-imx708) | Brightness, Sharpness, Contrast, Saturation, Focus (Manual), Exposure (Auto & Manual), Gain (Auto & Manual) |
|OV5647|+ fixed focus<br/> + Inexpensive<br/> + M12 lens [^2]<br/>|- low resolution (5MP)<br/> - no HDR<br/> - physical size<br/>| Works out of the box | Brightness, Sharpness, Contrast, Saturation, Exposure (Auto & Manual), Gain (Auto & Manual) |
|IMX219|+ fixed focus<br/> + Inexpensive<br/> + M12 lens [^2]<br/> + physical size <br/>|- medium resolution (8MP)<br/> - no HDR<br/>| [additional Setup](#imx219-arducam-8mp) | Brightness, Sharpness, Contrast, Saturation, Exposure (Auto & Manual), Gain (Auto & Manual) |

[^1]: Autofocus is a downside for our use-case because the lens assembly will shake during operation
[^2]: M12 lenses are a standard and can be exchanged for other lenses

### Additional Setup

Some third-party cameras are not picked up by the RPi's auto-detection and require a manual overlay. To set one up, switch to [RW mode](FAQ.md#how-can-i-enable-rw-mode) and edit `/boot/firmware/config.txt`:

1. Disable auto-detection by changing the existing line to:
    ```
    camera_auto_detect=0
    ```
    This is required when using manual overlays. Leaving auto-detect enabled can cause conflicting kernel modules to be loaded, resulting in the camera not being recognized.

2. Add the overlay for your camera:

    | Camera | Overlay |
    |--------|---------|
    | Arducam 12MP IMX708 | `dtoverlay=imx708` |
    | OV5647 (Picamera V1.3) | `dtoverlay=ov5647` |
    | IMX219 (Arducam 8MP, generic) | `dtoverlay=imx219` |

3. Reboot and verify the camera is detected:
    ```
    dmesg | grep -E "imx708|imx219"
    ```
    You should see output like:
    ```
    [   12.173300] imx708 10-001a: camera module ID 0x0302
    ```

!!! warning
    Do not forget to switch back to RO mode once you are done.

#### Camera notes

* **Arducam 12MP IMX708**: Same chipset as the RPi Cam v3 but with hardware differences that prevent auto-detection. Works out of the box once the overlay is set.
* **OV5647 (Picamera V1.3, Bewinner)**: Works out of the box with auto-detection, but can also be set up with a manual overlay. Generally speaking, IMX219 options will always be better than this one, so unless you already have one lying around, there is little upside of getting one.
* **IMX219 (Arducam 8MP, generic Ali-Express options)**: Same chipset as the RPi Cam v2 but needs a manual overlay. There are a lot of IMX219 based cameras on Ali-Express for very little money.
### Rotating Image
If you can only mount your camera upside down, you can rotate the image by adding the following overlay in `/boot/firmware/config.txt` after changing [RW mode](FAQ.md#how-can-i-enable-rw-mode):

For `IMX708` based cameras (they are usually rotated by 180 degrees):
```
camera_auto_detect=0
dtoverlay=imx708,rotation=0
```

For `OV5647` based cameras:
```
camera_auto_detect=0
dtoverlay=ov5647,rotation=180
```

!!! warning
    Do not forget to switch back to RO mode once you are done.

## Tested

### SBCs
Our main platform is the **Raspberry Pi Zero 2 W** but you can also use:

* RPi 3 (3B, 3B+ and 3A)
* RPi 4 (B)

### Modems

* [Cat 1, 4G Modem hat with GPS (Variant: Zero-4G-CAT1-GPS)](https://s.click.aliexpress.com/e/_oB0K4If) - Default frequency bands are set for the Chinese (Asian) market: `1, 3, 8, 34, 38, 39, 40, 41`

### Voltage Sensor

* [INA226](https://s.click.aliexpress.com/e/_om5BMkb) - slightly bigger than the INA231, but more readily available on places like Amazon

### V3xctrl PCB
If you are using the v3xctrl PCB, you need to set `Shunt resistance` to 5 milliohm and the `Max Expected Current` to 16A to get correct power draw readings.

## Potential Candidates

The following components are expected to work but have not been explicitly tested.

### SBC

* Any multi-core Raspberry Pi (or alternative SBC) with at least 512MB of RAM should be sufficient. A hardware encoder for H.264 is required.

### Modems

* Any 4G modem that provides an **RNDIS interface** should work.

!!! warning
    It is strongly recommended to use a modem that also provides a **serial interface** for querying modem stats via AT commands. Without this, features like reception monitoring, signal quality reporting, and band limitation configuration will not work.

* [Cat 4, 4G Modem hat with GPS (SIM7600G-H 4G HAT)](https://aliexpress.com/item/1005005628834373.html)

### Cameras

Technically, any compatible camera should work. However, we recommend the [PiCam V3 (Wide version)](https://www.raspberrypi.com/products/camera-module-3/) as it is currently the only camera that supports HDR, which helps with difficult lighting conditions.

If HDR is not important for your setup, any PiCam, ArduCam, or compatible clone should work. We recommend choosing one with a decent FOV (Field of View).
