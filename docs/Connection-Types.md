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
If you need access to a relay, join us on [Discord](https://discord.v3xctrl.com) and we will help you out with a **Session ID**.

### Setup
Once you have your Relay **Session ID**, you need to set it up on the viewer and the streamer, and enable connection via relay on both sides.

> **CAUTION:** Do not share your session ID with anyone. Anyone with your session ID will be able to connect to your streamer, see the video stream and control your device.

### Transport

By default, the relay uses **UDP** for data transport. If your carrier blocks or filters UDP traffic (e.g., Google Fi, VIVO), you can switch to **TCP** as an alternative transport.

You can select the transport independently on the streamer and the viewer. The following combinations are supported:

| Streamer | Viewer | Status |
|----------|--------|--------|
| UDP | UDP | Default |
| TCP | TCP | Fully supported |
| UDP | TCP | Supported (mixed) |
| TCP | UDP | Supported (mixed) |

To switch transport, change the "_Transport_" setting in the relay configuration on the streamer's web interface and/or in the viewer's network settings.

> TCP uses keepalive probes (10s idle, 5s intervals, 3 probes) to detect dead connections within approximately 25 seconds.

## Spectator

Spectator mode allows additional viewers to watch an active relay session without being able to control the vehicle. It is a **view-only, one-way stream** from the streamer to the spectator.

> Spectator mode only works with relay connections, not in direct mode.

### How it works

* A spectator needs a **Spectator ID** linked to an active session. You can obtain one from [Discord](https://discord.v3xctrl.com).
* Multiple spectators can watch the same session (one per source IP).
* Spectators can join before the session is fully established and will start receiving data once the streamer connects.
* Spectators can use either UDP or TCP transport, independently of what the streamer or viewer are using.

### Setup

In the viewer, enable "_Use UDP Relay_", select "_Spectator_" as the role, and enter your **Spectator ID**. Click "_Save_" and "_Back_" to connect.

> Spectators are automatically disconnected after 30 seconds of inactivity (unless connected via TCP).
