We provide multiple options for the viewer.

## Desktop

We offer standalone apps for Windows and Linux, you can download them from the [releases](https://github.com/stylesuxx/v3xctrl/releases).

### Installation

#### Windows

Download the `.exe` from the [latest release](https://github.com/stylesuxx/v3xctrl/releases/latest) and run it.

#### Linux (Flatpak)

Download the `.flatpak` file from the [latest release](https://github.com/stylesuxx/v3xctrl/releases/latest) and install it:

```bash
flatpak install --user v3xctrl-viewer-linux-*.flatpak
```

Then run it:

```bash
flatpak run com.v3xctrl.viewer
```

!!! note
    You need Flatpak installed on your system. Most distributions include it by default. If not, see [flatpak.org/setup](https://flatpak.org/setup/) for instructions.

### Usage

Press ++esc++ at any time to toggle the menu.

Settings will be applied after you hit the "Save" button and click "Back".

### Recording

You can start and stop recording from the viewer menu: open the menu with ++esc++, switch to the "_Streamer_" tab, and click "_Start Recording_" or "_Stop Recording_".

You can also toggle recording with the ++r++ hotkey.

A recording indicator will appear in the OSD when recording is active, whether triggered from the viewer or via auto-recording on the streamer. See [Streamer - Recording](Streamer.md#recording) for auto-recording setup and storage details.

### Hotkeys

| Key | Action |
|-----|--------|
| ++esc++ | Toggle menu |
| ++f11++ | Toggle fullscreen |
| ++r++ | Toggle recording |
| ++w++ / ++s++ | Throttle forward / reverse |
| ++a++ / ++d++ | Steer left / right |
| ++arrow-left++ / ++arrow-right++ | Trim steering |

### OSD (On-Screen Display)

The viewer shows an on-screen display with real-time telemetry. You can toggle individual OSD elements in the menu under the "_OSD_" tab.

Available widgets:

| Widget | Description |
|--------|-------------|
| Clock | Real-time clock, useful for [latency measurement](Latency.md#measuring-latency) |
| FPS | Current framerate |
| Battery | Battery voltage, average voltage, percentage, and current draw from INA sensor |
| Signal Quality | Modem signal strength and active band |
| Recording | Recording indicator (visible when recording is active) |
| Steering | Steering input indicator |
| Throttle | Throttle input indicator |
| GPS | Fix type, satellite count, and speed |
| Debug | Latency breakdown, data rates, and diagnostic info |
| Cell ID | Cell tower ID (disabled by default for privacy) |

> Widget positions can be customized by editing `settings.toml` directly. See [Editing settings](#editing-settings) for the file location.

### Debug output

For troubleshooting, you can run the GUI with debug logging enabled:

```bash
v3xctrl --log DEBUG
```

By default, only **ERROR** level messages and above are shown. The debug log includes:

* UI state changes
* Incoming/outgoing control messages
* Errors and exceptions

Logs are printed directly to the terminal where the GUI was started.

### Editing settings

On first start, a `settings.toml` file is generated with all available configuration values.

* **Not all settings are exposed in the GUI.**
You can manually edit settings.toml to access additional options. Here you can find the path to your [config file](FAQ.md#where-can-i-find-my-viewer-config-file).

* **Example use case:** Moving or resizing OSD elements by adjusting their coordinates in the config file.

After manual edits, **restart the GUI** to apply changes.

## Mobile

We offer an APK for Android. It is currently not available through Google Play, but you can download it from the [releases](https://github.com/stylesuxx/v3xctrl/releases).

### Installation

Download the APK from the [latest release](https://github.com/stylesuxx/v3xctrl/releases/latest) and sideload it onto your Android device. You may need to enable "_Install from unknown sources_" in your device settings.

### Connection

The Android viewer only supports connection via the [relay](Connection-Types.md#relay), so you will need a valid session ID. You can obtain one by joining our [Discord](https://discord.v3xctrl.com).

Both UDP and TCP transport are supported. If your carrier blocks UDP, switch to TCP in the connection settings. See [Connection Types - Transport](Connection-Types.md#transport) for details.

### Features

* Hardware-accelerated H.264 video decoding
* Touch controls for steering and throttle
* Motion controls (tilt device to steer)
* Gamepad support via Bluetooth or USB
* Picture-in-Picture mode
* OSD with battery, signal quality, cell info, and latency
* Start/stop video and recording from portrait mode
* Inverted controls support
* Spectator mode

### Performance

30 FPS works on essentially any Android phone -- all devices from the last 5+ years have hardware-accelerated H.264 decoding.

60 FPS works on high-end and most mid-tier phones. If you experience frame drops at 60 FPS, try enabling your device's gaming/performance mode. This prevents the OS from throttling CPU and GPU clocks and prioritizes the app's resource usage.

| Brand | Feature | Where to find it |
|-------|---------|-----------------|
| Samsung | Game Booster | Settings > Advanced features > Game Launcher |
| Xiaomi/Redmi | Game Turbo | Settings > Special features > Game Turbo |
| OnePlus | Game Mode | Settings > Utilities > Game Mode |
| Stock Android / Nothing | Game Dashboard | Settings > Apps > Game Settings (swipe from left edge in-game) |
| Google Pixel | Game Dashboard | Settings > Apps > Game Settings |
| OPPO/Realme | Game Space | Settings > Special Features > Game Space |
| Vivo/iQOO | Ultra Game Mode | Settings > Ultra Game Mode |
| Huawei/HarmonyOS | GameCenter | Separate app from AppGallery |

### Known limitations

* Relay connection only (no direct mode)
* Control inputs may arrive with a slight delay in poor reception conditions
* Some carriers (e.g., Google Fi, VIVO) block UDP. Use TCP transport as a workaround.
