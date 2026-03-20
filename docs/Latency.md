## Latency

This flow chart illustrates where latency occurs in the system. We consider two chains:

- Streamer → Viewer (video path)
- Viewer → Streamer (control path)

There are multiple stages where latency is introduced, and only some of them are under our control.

## Video Path (Streamer → Viewer)

```
------------
| Streamer |
------------
| Camera   | 15–33 ms    (sensor exposure)
| ISP      | 15–50 ms    (libcamerasrc ISP processing)
| Buffer   | 0–66 ms     (libcamerasrc queued frames; 0–2 frames typical)
| Encoder  | 20–30 ms    (v4l2h264enc hardware, 1280x720@30fps, no B-frames)
| UDP      | 1.5–3 ms    (rtph264pay + udpsink, sync=false)
------------
| Network  | 5–100 ms    (WiFi to 4G, variable; occasional spikes possible)
------------
| Viewer   |
------------
| UDP      | 0.5–1.5 ms
| Decoder  | 1.5–15 ms  (software FFmpeg H.264)
| Buffer   | 0–33 ms    (FPS, frame buffer, render_ratio dependent)
------------
| Display  | 8–30 ms    (monitor refresh)
------------
```

On the streamer it can take 51.5-116ms from the light hitting the lens until the frame leaves the streamer onto the network.
On the viewer it can take from 2-52 ms until the frame is ready to be displayed.
On the display it can take an additional 8-30ms 

From capturing a frame to displaying it on-screen, the pipeline latency is roughly **65–190 ms**, with real-world end-to-end measurements typically around **120–210 ms** depending on network conditions.

## Control Path (Viewer → Streamer)

```
------------
| Viewer   |
------------
| Control  | 0.1–0.3 ms (input event handling, message queueing)
| UDP      | 0.5–1.5 ms (kernel stack, NIC buffer)
------------
| Network  | 5–40 ms   (WiFi to 4G, variable)
------------
| Streamer |
------------
| UDP      | 0.5–1.5 ms (receive, buffer copy)
| Process  | 0.5–2 ms  (command parsing & execution)
------------
| Actuator | 1–5 ms    (GPIO/PWM write, motor driver response time)
------------
```

From reacting to a video frame and sending a control packet back to the streamer, the control latency is typically **8–50 ms**.

## Total End-to-End Latency

Combined latency (video + control round-trip) is therefore in the range of **75–240 ms** under normal conditions, with typical values around **190–230 ms**.

!!! note
    End-to-end latency below ~250 ms is generally considered acceptable for responsive remote control, though lower is better for fast maneuvers.
    The **largest contributor** to latency is the **cellular network**. Choosing a strong, low-congestion 4G provider is crucial for good performance.

## UDP Relay

When using a UDP Relay instead of a direct connection, expect **additional latency of 6–8 ms** due to extra packet processing and routing through the relay server. The increase is typically negligible compared to total pipeline latency but may add up if the relay server is geographically distant.

## Measuring Latency

### Network Latency
On the control channel, we are sending Latency packets to measure network latency. Those packets are measuring round trip time:
1. Viewer sends timestamped packet to streamer
2. Streamer echos that packet back to viewer
3. Viewer calculates round trip time
4. Viewer displays RTT/2 as an estimate of one way network latency

!!! note
    Be aware that there is a bit of overhead in this number since we need to process the packet on both sides but that overhead is consistent and in the range of 1-2ms

### End-to-End Latency
On the viewer, enable the Clock element in the OSD menu. This will display a clock in the bottom right of the screen. With the streamer, film the screen - make sure you are filming the clock on the bottom right so it can be seen properly in the center of the viewer. Record the viewer with screen recording software like OBS.

In the recording, pick a frame and calculate the difference between the time in the center of the screen and the reference on the bottom right. This is your end-to-end latency - or at least a pretty good approximation of it.

<img src="https://github.com/user-attachments/assets/cd5ea95d-bead-43da-a8d0-7ed5bbd9dcd5" />

* On the bottom right, we can see the reference time: **17:54:09.674**
* In the center we see the measured time: **17:54:09.545**
* The difference is the latency, we only need to look at the milliseconds. In our example that is **129ms**.

In the streamer and viewer logs you can find a breakdown of latency for the things we can measure in software.

Streamer:
```
[TIMING] capture: 17.8ms | encode: 23.8ms | package: 2.9ms | total: 44.5ms
```

Viewer:
```
[TIMING] receive: 1.7ms | decode: 8.8ms | buffer: 8.1ms (0.3-14.4) | total: 18.6ms
```

We can now compare that against the latency we read from the screenshot and calculate unaccounted latency:

```
measured - network - streamer - viewer = unaccounted
129 - 4 - 44.5 - 18.6 = 61.9ms
```

Our **unaccounted latency is 61.9ms**. This has to be latency from things we cannot measure in software:

**Pre-capture (streamer side):**

* Display input lag (the monitor being filmed, e.g., ~10-15ms for typical monitors)
* Camera sensor exposure time (varies with lighting)
* Camera sensor readout time
* libcamerasrc ISP processing and buffering

**Post-decode (viewer side):**

* Pygame rendering and blit to screen
* GPU compositing
* Display/monitor input lag

!!! note
    The display being filmed by the camera adds its own input lag to the measurement. This is unavoidable when using a camera-based glass-to-glass test. In the real-world use case, this display latency wouldn't exist since you're filming the real world, not a monitor.

## Real world latency tests
As you can see from above, latency has a LOT of variables, when testing, we want to reduce as many variables as possible, to do so we will run all the tests at the same settings:

* 1.8Mbit target
* 30FPS
* I-Frame interval: 15
* High Profile
* No HDR, no wide FOV
* No automatic I-Frame adjustments
* Control channel enabled
* Viewer: 60 FPS loop
* Viewer: Clock enabled, debug widget enabled
* RPi Cam v3

!!! note
    If anything deviates from these defaults, it is mentioned so in the following tests.

## Ethernet
In this test we use an USB-C Ethernet adapter to exclude as much network latency as possible. We use the above described method to measure latency, we will pick min and max latency measurements from the recording and calculate the average.

| GST      | min | max | avg |
|----------|-----|-----|-----|
| 60 FPS   | 120ms | 162ms | 141ms |
| Uncapped | 115ms | 125ms | 120ms |

## WiFi
A good WiFi should basically be on par with Ethernet - at least for our use case

| GST      | min | max | avg |
|----------|-----|-----|-----|
| 60 FPS   | 128ms | 161ms | 144ms |
| Uncapped | 114ms | 147ms | 130ms |

## 4G/LTE
Now this will depend on provider, location, band and reception. This is measured in a city with very dense coverage.

| GST      | min | max | avg |
|----------|-----|-----|-----|
| 60 FPS   | 164ms | 199ms | 181ms |
| Uncapped | 139ms | 165ms | 152ms |

!!! note
    This is a great example of fluctuations. Uncapped should improve by max 15ms, but in this case we could also see lower latency in general while doing the uncapped test.

## Pushing latency

!!! note
    When testing settings on the streamer and watching the logs, it is important to compare a consistent image, for this it makes sense to put something over the camera to have a black image. This obviously simulates a "best case" for the pipeline since the image is not changing at all, a "worst case" for the camera since it needs the longest exposure time, but also allows for easy comparisons.

### Force wide FOV / HDR enable
Using either of those options will increase the FOV significantly, but will also increase the time consumed to fetch the image from the camera - this option adds 15ms - 20ms of latency.

### Change encoder profile
Changing the encoder profile from "High" to "Constrained Baseline" saves about 5ms during the encoding step.

### Overclocking streamer
To decrease latency more, you can overclock the GPU frequency to 450MHz instead of the default 400MHz, this will give you an additional improvement of around 15ms. But keep an eye on the thermals. In order to overclock the GPU add the following line to `/boot/firmware/config.txt`:

```
gpu_freq=450
```

!!! warning
    When overclocking you will need some additional cooling, either a heatsink or a small fan, otherwise the RPi will overheat and start thermal throttling, resulting in jitter from the camera and ultimately, lots of dropped frames.

### Uncapping viewer
You can let the viewer run in uncapped mode - setting "_Main Loop FPS_" to 0, this will increase the loop to whatever the system can handle, resulting in frames being displayed significantly quicker if they are available. This can improve latency by about 10ms.