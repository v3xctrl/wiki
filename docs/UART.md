The raspberry Pi Zero 2 W has unfortunately only one UART broken out.

During firstboot, the UART is used for serial console in order to make it easier to debug. Once set up, the serial console is disabled in order to free the UART up for peripherals like GPS modules.

In order to again enable the serial console, you need to edit `/boot/firmware/cmdline.txt`. You can do this either directly on the SD card or while you are connected via SSH (keep in mind that this change requires rebooting).

Add the following parameter to `/boot/firmware/cmdline.txt`:

```
console=serial0,115200
```

The whole entry might then look something like this:

```
console=serial0,115200 console=tty1 root=PARTUUID=8638ef4b-02 rootfstype=ext4 fsck.repair=yes rootwait  usbcore.autosuspend=-1 cfg80211.ieee80211_regdom=DE
```

Keep in mind, that this has to be all in one, single line.
