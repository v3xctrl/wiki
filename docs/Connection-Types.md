There are several connection types available:

## Direct

The Viewer has a static IP and reserved ports to which the streamer can connect.

> This is the simplest, most reliable and recommended connection type for most use cases.

## Relay

If both the streamer and viewer are behind mobile NATs, lack a dedicated IP, or you have no control over port forwarding, a relay connection can be used as a fallback option.

In this setup, both the viewer and streamer send their control and video data to a relay server, which then forwards the data between them. This approach is more complex and should only be used when a direct connection is not possible or you want to achieve the following:

* Share your streamer with a different user who does not want to share their IP
* Allow other users to join your session as a spectator

### Caveats

Using a relay server adds a small amount of latency and depends on external infrastructure, which can sometimes be less reliable. We strive to keep our relay server highly available, but nothing beats a direct connection. We also reserve the right to make the Relay a paid feature: The relay needs extra hardware, bandwidth and maintenance. Once a critical user limit is reached, we can no longer pay this infrastructure out of our own pocket. Once this limit is reached we will strive to find a fair solution for everyone. 

### Access
If you need access to a relay, join us on Discord and we will help you out with a **Session ID**.

### Setup
Once you have your Relay **Session ID**, you need to set it up on the viewer and the streamer, and enable connection via relay on both sides.

> **CAUTION:** Do not share your session ID with anyone. Anyone with your session ID will be able to connect to your streamer, see the video stream and control your device.
