We provide multiple options for the viewer

## Desktop
We offer standalone apps for Windows and Linux, you can download them from the [releases](https://github.com/stylesuxx/v3xctrl/releases).

### Usage
Press ++esc++ at any time to toggle the menu.

Settings will be applied after you hit the "Save" button and click "Back".

### Debug output
For troubleshooting, you can run the GUI with debug logging enabled:

```bash
./v3xctrl-gui --log DEBUG
```

By default, only **ERROR** level messages and above are shown. The debug log includes:

* UI state changes
* Incoming/outgoing control messages
* Errors and exceptions

Logs are printed directly to the terminal where the GUI was started.

#### Editing settings
On first start, a `settings.toml` file is generated with all available configuration values.

* **Not all settings are exposed in the GUI.**
You can manually edit settings.toml to access additional options. Here you can find the path to your [config file](FAQ.md#where-can-i-find-my-viewer-config-file).

* **Example use case:** Moving or resizing OSD (On-Screen Display) elements by adjusting their coordinates in the config file.

After manual edits, **restart the GUI** to apply changes.

## Mobile
We also offer an APK for Android - it is currently not available through Google Play, but you can download it from the [releases](https://github.com/stylesuxx/v3xctrl/releases).

The Android viewer only supports connection via the Relay, so you will need a valid session ID. You can obtain one by joining our [Discord](https://dsc.gg/v3xctrl).