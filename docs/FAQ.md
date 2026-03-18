## Why does my framerate drop while there are no big changes in the image?

This one is a bit counter-intuitive, and you need to understand how the video pipeline works in more detail. This is a simplified view to illustrate the relevant parts:

```
Camera (@30FPS) -> Queue -> Encoder -> Transmitter -> (NETWORK) -> Receiver -> Decoder -> Display(@60FPS)
```

The camera feeds images at 30 FPS into the queue. The queue is leaky, meaning it keeps only the latest 10 frames (for example) and drops all older ones. The encoder encodes frames as fast as it can and pushes UDP packets out via the transmitter. The receiver decodes the incoming frames and displays them, prioritizing the newest image to be displayed as quickly as possible.

A few things to keep in mind:

* The displayed frame rate is the number of frames **rendered per second**, not the number of frames actually received.
* Video is **processed in "real-time"**, but this wording is misleading: nothing in computing is truly real-time, and nothing is instantaneous. At best, it feels real-time to us - there is always some kind of latency.
* Encoding times vary — the less change there is between frames, the faster the encoder can encode them. (This is not true for every encoder, but it is true for the H.264 encoder on the RPi Zero.)

There are two extreme scenarios:

### Scenario 1
> The image is basically static; not much changes between frames.

The queue never gets bigger than three images because the encoder can push out new images very quickly. We can define this as a latency of three frames: while the receiver displays a frame, there are three newer frames in the queue ready to be encoded and transmitted. The transmitter has no synchronization, so it pushes packets out as fast as it can, resulting in bursts of images. Multiple images arrive at the receiver in a short period of time, faster than they can be displayed. For example, if the display renders at 60 FPS but frames arrive in bursts equivalent to 180 FPS, only every third arriving frame is displayed, and two-thirds of the frames are dropped.

### Scenario 2
> The image is changing constantly; there is lots of movement.

The encoder takes longer to encode each frame, so the queue grows to its maximum of 10 frames. This results in a latency of 10 frames: while the receiver displays a frame, there are 10 newer frames in the queue waiting to be processed. The bursts are now smaller, and frames arrive at a more manageable rate. The receiver can display each frame without dropping any, simply because there is no newer frame to replace it. This results in a **higher video frame rate**, as more of the received images can actually be rendered.

And this is where the counter-intuitive behavior comes in: more movement in the image results in **higher frame rate**, but as we just saw, it also results in **higher latency**.

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