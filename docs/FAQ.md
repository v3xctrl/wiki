For framerate and video quality questions, see [Troubleshooting](Troubleshooting.md#video-stream).

## Where can I find my Viewer config file?

Linux: `~/.config/v3xctrl-viewer/settings.toml`

Windows: `C:\Users\Username\AppData\Local\v3xctrl-viewer\settings.toml`

macOS: `~/Library/Application Support/v3xctrl-viewer/settings.toml`

## How can I enable RW mode?
By default the system is in RO (read-only) mode. This helps with prolonging the life of the SD card. In this mode the only writable partition is `/data`. For system updates and some configuration changes you will need to switch to RW mode. In order to do so, you need to connect to your streamer via SSH and then run:

```
sudo v3xctrl-remount rw
sudo reboot
```

After you are done with your changes, switch back to RO mode
```
sudo v3xctrl-remount ro
sudo reboot
```