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

!!! warning
    Oftentimes this is an issue with the SD card. Make sure you use a high quality SD card since problems will only accumulate from this point.

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

!!! note
    As a reference, with a Cat 1, 4G modem your maximum upload speed will be 5Mbps. Benchmarks have shown that more realistically your upload will be at around 3.5Mbps on average. But this depends a lot on your provider and the coverage in your area.

### A lot of blocking/artifacts

We are using h264 encoded video. This format uses reference frames (I-frames) and the following frames are encoded based on the reference frames. If the reference frame is not received, then the following frames will be displayed wrongly and it might result in blocking/artifacting.

In this case you will also see a drop in video framerate - use the same steps to mitigate the issue as described above.

You can also try to decrease the `iFramePeriod` in the `video` config section. This will increase the number of I-frames and thus reduce the blocking/artifacting.

### Micro stutter
Sometimes micro stutter might happen in the viewer, this can be fixed by adjusting encoder settings. This usually happens in high detail environments like forests.

#### How to identify
This stutter occurs before an I-frame is received on the viewer, so it will happen in the I-frame interval (1 sec by default). You can verify this by looking for jitter in the viewer's log. If the max jitter is consistently above the length of a frame (33.3ms) then chances are that you are running into this issue.

#### Reason
The reason for this issue is that I-frames are bigger than p-frames and will take longer to be transmitted to the viewer. The size of an I-frame depends on how heavily it can be compressed.

#### Mitigation
There is a couple ways of mitigating this issue, which one is the right one for you really depends on your circumstances:

1. Decrease framerate: Oftentimes this is fixed by simply decreasing framerate to 24FPS. Lower framerate means that frames have more time to arrive, since less have to arrive per second
2. Decrease QP range, increase min QP - this will make I-frames smaller

##### Calculating maximum I-frame size
Maximum I-frame size can be calculated: Given the framerate and the maximum bandwidth you can calculate how big an I-frame can be to still be transmitted inbetween frames. (Keep in mind, this is an approximation not considering network conditions and jitter, just pure bandwidth).

Given a framerate of **30FPS and a maximum bandwidth of 2.8Mbps** we can calculate:

Time per frame: `1/FPS = 1/30 s = 33.3 ms`

So if we want each frame arrive before the next one is being processed we basically have 33.3ms to do so, bandwidth is our limiting factor:
Max frame size:
```
Bandwidth (bps) * Time per frame (s)
= 2.8 Mbps * (1/30) s
= 2800 bits/ms * 33.3 ms
= 93240 bits
= 11.655kB
```

So you should target I-frames no bigger than 11.655kB. You can assume that I-frames are always a multiple of the p-frames, so it is enough to find out maximum I-frame size to be in the optimal range.

> **NOTE:** The practical limit is usually higher here since the pipeline does have a buffer and you will always have some lag which will compensate for the I-frame burst in size. But with this conservative value you should definitely not see any stuttering. Additionally LTE can momentarily burst over your average bandwidth limit. So this calculated number should be seen as a worst case reference, you can move up from that and see what your practical limits are.

#### Verification
When stutter stops, you have mitigated the issue. For better debugging you can monitor the INFO debug output of the video service, it will show you I-frame size. You can use this as an indicator to find an I-frame size at which the stutter stops.

### Framerate drops with static image

This one is a bit counter-intuitive, and you need to understand how the video pipeline works in more detail. This is a simplified view to illustrate the relevant parts:

```
Camera (@30FPS) -> Queue -> Encoder -> Transmitter -> (NETWORK) -> Receiver -> Decoder -> Display(@60FPS)
```

The camera feeds images at 30 FPS into the queue. The queue is leaky, meaning it keeps only the latest 10 frames (for example) and drops all older ones. The encoder encodes frames as fast as it can and pushes UDP packets out via the transmitter. The receiver decodes the incoming frames and displays them, prioritizing the newest image to be displayed as quickly as possible.

A few things to keep in mind:

* The displayed framerate is the number of frames **rendered per second**, not the number of frames actually received.
* Video is **processed in "real-time"**, but this wording is misleading: nothing in computing is truly real-time, and nothing is instantaneous. At best, it feels real-time to us - there is always some kind of latency.
* Encoding times vary — the less change there is between frames, the faster the encoder can encode them. (This is not true for every encoder, but it is true for the H.264 encoder on the RPi Zero.)

There are two extreme scenarios:

#### Scenario 1
> The image is basically static; not much changes between frames.

The queue never gets bigger than three images because the encoder can push out new images very quickly. We can define this as a latency of three frames: while the receiver displays a frame, there are three newer frames in the queue ready to be encoded and transmitted. The transmitter has no synchronization, so it pushes packets out as fast as it can, resulting in bursts of images. Multiple images arrive at the receiver in a short period of time, faster than they can be displayed. For example, if the display renders at 60 FPS but frames arrive in bursts equivalent to 180 FPS, only every third arriving frame is displayed, and two-thirds of the frames are dropped.

#### Scenario 2
> The image is changing constantly; there is lots of movement.

The encoder takes longer to encode each frame, so the queue grows to its maximum of 10 frames. This results in a latency of 10 frames: while the receiver displays a frame, there are 10 newer frames in the queue waiting to be processed. The bursts are now smaller, and frames arrive at a more manageable rate. The receiver can display each frame without dropping any, simply because there is no newer frame to replace it. This results in a **higher video framerate**, as more of the received images can actually be rendered.

And this is where the counter-intuitive behavior comes in: more movement in the image results in **higher framerate**, but as we just saw, it also results in **higher latency**.

## Modem

!!! warning
    SIM activation can be finicky at times. It is highly recommended to initially activate the SIM card on a phone, disable the pin and make sure that data works. Activation might differ from country to country and can be very hard to streamline just via the modem. Once you disabled the PIN and made sure that data works, the SIM card will most likely also work in the modem.

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

## GPS Module does not find Satellites
If your GPS Modem can not find sattelites or the connection is unstable you may do some debuging about the signal/jammin/noise happening on your build. For details check [GPS-debug](https://wiki.v3xctrl.com/GPS-debug/)

## Reverse SSH shell
!!! warning
    Only use this when you know what you are doing or when any of the team asks you to.

Sometimes it might be helpful to have access to the streamer via SSH when in the field. For this a reverse SSH shell is in place. In the "Extras" tab you will find a setting for a remote Server which the reverse shell will open to.

On the computer you want the reverse shell to connect to, run:

```
socat TCP-LISTEN:9999 -
```

You can then start the Reverse Shell via the viewer's "Streamer" menu.

## SD card
SD card issues are more common than you might think and symptoms are unfortunately super random.
It is a good idea to benchmark fresh SD cards and keep track of their degradation over time.

!!! warning
    A good, high quality SD card is important. In normal use the SD card is only written for config files and recordings. For that, technically Class 10/U1 is fine. U3 is obviously better, and U3 with A2 (good random I/O performance) is optimum. Realistically you should go with a U3/A1 card - those are widely available. **Do not cheap out on SD cards, it's simply not worth the hassle.**

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
