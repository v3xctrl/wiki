When updating to a new OS version, this Checklist should help to catch broken functionality:

## Basic image functionality

* [ ] Boots with modem (best test without any customization applied)
* [ ] Packages build
* [ ] Custom image builds
* [ ] Custom image flashes with RPi Imager
* [ ] Custom image boots
* [ ] Serial console debugging output is present
* [ ] Defaults set in RPi Imager are applied (hostname, Wifi, locale)
* [ ] Firstboot script runs without errors
* [ ] Banner updates after firstboot ran
* [ ] SD expands /data partition
* [ ] SWAP is moved to /data and is active
* [ ] Config files are moved
* [ ] firstboot script is removed
* [ ] firstboot service is deactivated
* [ ] /boot/firmware is RO in /etc/fstab
* [ ] initramfs is installed
* [ ] OverlayFS is active after firstboot

## Functionality provided by v3xctrl.deb

* [ ] ENV is written on startup
* [ ] Starts services
* [ ] Webserver works
* [ ] Wifi works
* [ ] AP/client switch works
* [ ] routing works properly
* [ ] `v4l2-ctl` shows picam & controls
* [ ] Control service works
* [ ] Video service works
* [ ] overlay FS works
* [ ] rw/ro switch works
* [ ] SMB share works

After this has been verified, the [Release checklist](x-New-Release-Checklist.md) should be checked too.