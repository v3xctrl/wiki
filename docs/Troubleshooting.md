If you encounter any issues, this document will help you troubleshoot and resolve them.

## SSH connection
If after installation and first boot, you cannot connect via SSH, check the following:

- Make sure your streamer gets assigned an IP address by your router
- Make sure you are using the correct hostname
- Try connecting to IP directly instead of using the hostname

### No IP assigned
If on the router you cannot see your streamer in the list of connected devices, it is very likely that you did not set your WiFi credentials correctly when flashing the image. Double check the settings and flash the image again.

## Stuck in firstboot mode
If you connect via SSH and you see the Firstboot message and Firstboot does not complete within 15 minutes (the system restarts automatically and removes the firstboot message), there is a high likelihood that something went wrong during firstboot setup, check the log:

`cat /boot/firmware/firstboot.log`

> **NOTE:** Oftentimes this is an issue with the SD card. Make sure you use a high quality SD card since problems will only accumulate from this point.

## Config Server
The webserver for configuration is started by default after installing the package.

### Can not connect
The webserver is by default running on port `80` and can be accessed via `http://$CLIENT_IP`. If the streamer is in Access Point mode, you will be able to connect via `http://192.168.23.1`.

If you cannot connect to the webserver, check the following:

- Make sure you are using the correct IP address - check your router
- Make sure the webserver is running: `systemctl status v3xctrl-config-server`
- If it is not running, enable it and start:

```bash
sudo systemctl enable v3xctrl-config-server
sudo systemctl start v3xctrl-config-server
```

- If status is failed, check the logs: `journalctl -u v3xctrl-config-server -n 50`

## Video stream

### Not receiving video stream
- Make sure the video stream is successfully started in the streamers *"Services"* tab, status should be `active`. If it is not, check the logs for further details.
- Make sure the video stream is
- Check the config server, have a look at the video port, by default this is `16384`
- Make sure the port is forwarded on your router to your viewer (consult the manual for your router to find out how to do this - usually this will be in a section called "port forwarding" or "NAT")

If you made sure that the port is forwarded correctly and still not receiving the video stream, try the following:

- Check the status of the `v3xctrl-video` service: `systemctl status v3xctrl-video` - this service is not started automatically unless you enable it to be autostarted in the config.
- Try to start it manually: `sudo systemctl start v3xctrl-video`

If there is still no video stream:
- Check the logs of the `v3xctrl-video` service: `journalctl -u v3xctrl-video -n 50` - this will give you more information about what is going on with the service.

Oftentimes an issue can be a bad connection with the camera. To rule out the camera as an error source you can enable `testSource` in the `video` config section, this will send a test pattern instead of the camera feed to the viewer.

If you can see the test pattern, double check your camera connection.

### Stream very laggy
Lag should not be an issue - we are dropping frames if they cannot be sent fast enough on the streamer or if the encoder cannot process them fast enough.

Monitor the FPS on the viewer - if the Main `Loop` does not run at the full framerate of 60FPS, it is an indicator that your viewer is not capable of handling the load.

### Drop in Video frames
If the `Video` FPS counter does not show the configured FPS (30 per default), there could be multiple reasons for this:

1. If the main `Loop` also is not running at full (60 by default) FPS, then your viewer machine is the issue.
2. If the main `Loop` is running at full FPS, but the `Video` loop is dropping, then this is most likely an issue with the network connection. Run the self check tests. The default video is set to 1.8Mbps, if your connection tests slower than that, then you need to adjust the bitrate accordingly. Tests have shown that a bitrate of 1Mbps is still usable.

> As a reference, with a Cat 1, 4G modem your maximum upload speed will be 5Mbps. Benchmarks have shown that more realistically your upload will be at around 3.5Mbps on average. But this depends a lot on your provider and the coverage in your area.

### A lot of blocking/artifacts

We are using h264 encoded video. This format uses reference frames (I frames) and the following frames are encoded based on the reference frames. If the reference frame is not received, then the following frames will be displayed wrongly and it might result in blocking/artifacting.

In this case you will also see a drop in video framerate - use the same steps to mitigate the issue as described above.

You can also try to decrease the `iFramePeriod` in the `video` config section. This will increase the number of I frames and thus reduce the blocking/artifacting.

## Modem

> SIM activation can be finicky at times. It is highly recommended to initially activate the SIM card on a phone, disable the pin and make sure that data works. Activation might differ from country to country and can be very hard to streamline just via the modem. Once you disabled the PIN and made sure that data works, the SIM card will most likely also work in the modem.

If the modem is not showing up in `ip a s`:

- Check that the modem is correctly connected and powered on

See what `dmesg` says:

* Unplug the modem
* Clear dmesg: `sudo dmesg -c`
* Plug in the modem
* Check dmesg: `sudo dmesg -c`

### Checking routing
To verify which device internet traffic is routed through, check the following commands

```bash
ip route show default
```

The default route with the lowest priority (or none at all) will be chosen. You can further verify:

```
> ip route get 8.8.8.8

8.8.8.8 via 192.168.10.1 dev eth0 src 192.168.10.2 uid 1000
    cache
```

This will show through which device the traffic is routed. In this case it is routed through `eth0`, which is the RNDIS modem.

### Modem keeps disconnecting
When you see the modem to connect, disconnect and re-enumerate in DMESG, it indicates a bad connection.

This might especially be a problem with the modem that comes with pogo pins. The best way to fix this is to remove the pogo pins and solder directly to the pads. This can be a bit finicky. Alternatively it can also help to tin the pads slightly.

## Reverse SSH shell
> Only use this when you know what you are doing or when any of the team asks you to.

Sometimes it might be helpful to have access to the streamer via SSH when in the field. For this a reverse SSH shell is in place. In the "Extras" tab you will find a setting for a remote Server which the reverse shell will open to.

On the computer you want the reverse shell to connect to, run:

```
socat TCP-LISTEN:9999 -
```

You can then start the Reverse Shell via the viewer's "Streamer" menu.

## SD card
SD card issues are more common than you might think and symptoms are unfortunately super random.
It is a good idea to benchmark fresh SD cards and keep track of their degradation over time.

> A good, high quality SD card is important. In normal use the SD card is only written for config files and recordings. For that, technically Class 10/U1 is fine. U3 is obviously better, and U3 with A2 (good random I/O performance) is optimum. Realistically you should go with a U3/A1 card - those are widely available. **Do not cheap out on SD cards, it's simply not worth the hassle.**

### Symptoms
* I/O errors are a dead giveaway
* If random things start happening that have no rhyme or reason

### Useful commands (NON-DESTRUCTIVE)
```
# Read entire card and check for errors
sudo dd if=/dev/sdX of=/dev/null bs=4M status=progress

# Non-destructive read test
sudo badblocks -v /dev/sdX
```

### Useful commands (DESTRUCTIVE)
```
# Read-write test (DESTROYS DATA)
sudo badblocks -wsv /dev/sdX
```

### Third party tools
You can also use [f3](https://github.com/AltraMayor/f3) or [H2testw](https://h2testw.org/).