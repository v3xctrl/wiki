The streamer is the heart of the project: Transmitting (and recording) video, receiving control commands, and managing the actuators like servos and ESC.

## Installation

We provide a PiOS based - ready to flash - image. It can be flashed to an SD card using the [Raspberry Pi Imager Utility](https://www.raspberrypi.com/software/).

!!! warning
    You will need to use RPi Imager v2.x - the old v1.x version will not work reliably.

!!! note
    We are currently in the process of getting the image added to the official RPi Imager repository. Until this is done, you will have to point Imager to our custom repository located at https://v3xctrl.com/rpi-imager/v3xctrl_repo.json You can add this through "_App Options_" -> "_Content Repository_" ->"_Edit_" -> "_Use custom URL_". Be aware that this needs to be set every time you restart RPi Imager. When starting the imager via command line you can also pass the repository as a parameter: `sudo ./Raspberry_Pi_Imager-v2.0.3-desktop-x86_64.AppImage --repo https://v3xctrl.com/rpi-imager/v3xctrl_repo.json`

### Setup steps

* Device: Select "_Raspberry Pi Zero 2 W_"
* OS: Select "_v3xctrl_", in the version selection select the latest stable release
* Storage: Make sure your SD card is inserted and select it

### Customization
* **Hostname**: Set hostname to something unique in your network, preferably identifying your model like: `v3xctrl-scx24`
* **Localization**: set your actual timezone and preferred keyboard layout. The country setting also determines the WiFi regulatory domain, which affects available channels and maximum transmit power. The least restrictive regions are Belize (BZ) and Bolivia (BO) with 13 channels and 30 dBm, followed by the US with 11 channels and 30 dBm. Most EU countries allow 13 channels but cap power at 20 dBm. Note that the RPi Zero 2 W's WiFi chip (CYW43439) caps transmit power at ~20 dBm regardless of the regulatory setting.
* **User**: Set username and password of your choosing
* **Wifi**: Set SSID and password of your home network
* **Remote Access**: Enable SSH and if possible use SSH key for authentication. During normal usage you will do most things via the Web interface, but having direct system access might be necessary at times.
* **Raspberry Pi Connect**: This is optional and not really required for `v3xctrl` - we do provide other means of remote access should the need be

Write the image and wait for verification to pass.

### First boot
After flashing, insert the SD card into your RPi Zero 2 W and power it up.

> Do not attach your 4G modem yet, we want to make sure that everything is working through your internal network first.


First boot will take a while, but after about five minutes you should be able to connect via SSH using the user and hostname you chose during customization:

```bash
ssh pi@v3xctrl.local
```

If you can connect, you are ready for the next step of the configuration.


> Be aware that only the first boot will take longer, afterwards you should be able to connect via SSH after around 30 seconds from plugging in the streamer.

If you cannot connect, check the [troubleshooting section](Troubleshooting.md#ssh-connection)

!!! success
    If at this point you can connect, installation went fine and you can continue with configuration.

## WiFi
After going through setup via Imager, you should already be connected to your home WiFi. You can add arbitrary other Host WiFi networks. Keep in mind that on startup the streamer will attempt to connect to any of the pre-configured WiFi networks if possible.

!!! note
    Best practice is to only have one Host WiFi configured, this way you can be confident about which network the streamer will connect. If no pre-configured Host Network is found, the streamer will create an Access Point.

!!! warning
    Be careful when connecting to unknown or public WiFi networks. The streamer exposes a web interface on port 80 without authentication. Anyone on the same network could access the configuration, control your vehicle, or modify settings. Only connect to networks you trust.

### Adding a Host network
To add another host network, connect via SSH and scan for available networks:

```bash
sudo nmcli device wifi list --rescan yes
```

Then connect to the network, this will create a configuration file in `/data/config/netplan`:

```bash
sudo nmcli connection add \
    type wifi \
    con-name "ConnectionName" \
    ifname wlan0 \
    ssid "Exact ESSID from scan" \
    wifi-sec.key-mgmt wpa-psk \
    wifi-sec.psk "password" \
    connection.autoconnect yes
```

!!! note
    Be aware that this will only add a connection but not connect you. You will only be connected after a reboot.

To remove a network, simply delete the config file.

### Access Point
When WiFi is configured to operate in Access Point mode, or no host network is found, the ESSID of the Access Point will be `v3xctrl-$$$ID$$$` where `$$$ID$$$` is a part of your RPi's ID, eg.: v3xctrl-c2868cdc.

The password is: **raspberry**

> See [Defaults](Defaults.md) for all default credentials and ports.

## Services

After installation there will be a few services available, some of them enabled by default. `systemd` is used for service management and all the services can be controlled by it:

```bash
# See the status of a service
systemctl status v3xctrl-config-server

# Restart a service
systemctl restart v3xctrl-config-server

# See the last 50 lines of a service log
journalctl -u v3xctrl-config-server -n50
```

!!! warning
    Always start the services through `systemd`, this will ensure that they will run with the correct users and permissions.

### v3xctrl-config-server (enabled by default)

This service is responsible for the configuration web interface. It is running on port `80` by default and can be accessed via `http://v3xctrl.local`.

> NOTE: You of course can also reach it with the IP address assigned by your router.

### v3xctrl-wifi-mode (enabled by default)

This service checks your wifi config on startup and starts your WiFi device in **client** or **access point** mode.

### v3xctrl-service-manager (enabled by default)

This service starts services on startup according to the configuration.

### v3xctrl-video

This service is responsible for sending the video feed to the viewer.

> This service is not meant to be enabled. It is started by the `v3xctrl-service-manager` service if autostart is enabled in the config.

### v3xctrl-control

This service is responsible for the control connection between streamer and viewer and is ultimately what controls the actuators.

> This service is not meant to be enabled. It is started by the `v3xctrl-service-manager` service if autostart is enabled in the config.

## Recording

The streamer can record video to the local SD card in H.264/MP4 format. Recordings are stored in `/data/recordings/`.

### Auto-recording

To automatically start recording when the video stream starts, enable it in the web interface: go to the "_Config Editor_" tab, scroll down to "_Autostart_" and check "_recording_". Click "_Save_".

### Manual recording

Recording can also be started and stopped manually from the [viewer](Viewer.md#recording).

### Storage

Recording storage depends on the configured bitrate. At the default 1.8 Mbps, expect approximately 810 MB per hour of recording. Make sure your SD card has sufficient free space on the `/data` partition.

### Accessing recordings

Recordings can be accessed via the Samba share (see below), by connecting to the streamer via SSH or via SD card directly.

### SAMBA share

There is a samba share for the recordings directory. You can access it via `smb://v3xctrl.local/recordings`. The username and password are both `v3xctrl`.

Samba is not enabled by default, you need to enable it in the config in the `Extras` section.

## Helpers

There are a couple scripts in place that will assist you with configuration.

### v3xctrl-video-control
This script will allow you to change parameters of the running video pipeline, this is mainly meant to adjust camera settings on the fly, but you can use it to adjust any of the elements. Unfortunately there is no easy way to see which cameras support which parameters, so this is a bit of a trial and error situation. The following elements are available:

#### Camera Source
* `camera`

#### Test Source
* `testsrc`
* `overlay`

#### Always
* `input_caps`
* `queue_encoder`
* `encoder`
* `encoder_caps`
* `t`
* `queue_udp`
* `payloader`
* `udpsink`

#### Recording
* `queue_rec`
* `parser`
* `muxer`
* `filesink`

Examples:

```
v3xctrl-video-control list camera
```