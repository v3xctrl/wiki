This page explains why certain design choices were made and the reasoning behind the current implementation.

## Thoughts and Considerations

Low latency is our **#1 priority**, and all technology choices are made accordingly. Since we do not want to reinvent the wheel (yet), we chose the best Layer 4 (transport) protocol for our use case. **UDP** and **QUIC** are both viable options, but because we are consistently updating in both directions, reliability is less important than speed - we can tolerate a few lost or out-of-order packets by handling sequencing on the streamer/viewer side.

> QUIC is designed for low latency but adds reliability and encryption we don’t need here.

UDP in the context of 4G networks has a couple downsides:
1. **Carrier restrictions:** Some carriers may filter or rate-limit UDP traffic, though this is uncommon.
2. **CGNAT:** Most 4G networks use Carrier-Grade NAT, meaning the streamer does not have a dedicated public IP. We rely on **UDP hole punching** to establish connectivity:

  * The streamer sends the initial packet to open a port mapping (“hole”) on the NAT.
  * The viewer responds through this hole.
  * The streamer keeps the hole alive by sending periodic UDP packets, which aligns with our need to transmit telemetry data anyway.

!!! note
    4G networks often use CGNAT, preventing direct inbound connections; UDP hole punching usually works, but some NAT types or carrier restrictions may require a relay server.

## Bandwidth Constraints

4G networks have limited uplink bandwidth, especially Cat 1 modems which are limited to about 5 Mbps uplink. Data usage depends on resolution and encoder settings. See [Network Testing](Network-Testing.md) for how to measure and evaluate your connection.

The system includes built-in self-tests for bandwidth, UDP round-trip time, and NAT hole duration. See [Network Testing](Network-Testing.md) for details.

## Packaging

We want installation to be straightforward:

* **Streamer:** Core functionality is packaged as a Debian `.deb` file for easy installation on Raspberry Pi OS.
* **Viewer:** Needs to be cross-platform (Windows, macOS, Linux) without complex setup requirements. This is why **GStreamer is avoided on the viewer side** - its cross-platform support is too unreliable for our needs.

## Configurability

We do not want to limit what users can do with this platform.

* The streamer includes a **web server for configuration**.
* Settings are stored in a **JSON schema**, which is easily expandable and supports user modifications.

## Client Hardware

We chose the Raspberry Pi Zero 2 W as the streamer platform for its combination of small size, hardware H.264 encoding, CSI camera interface, and GPIO support. See the [Hardware page](Hardware.md) for full details on compatible hardware and peripherals, and the [Pinout page](Pinout.md) for wiring.

## Software

We chose **PiOS (Bullseye Lite 64-bit)** as the base system.

> **Note:** Bookworm currently has issues with some RNDIS modems, so Bullseye (listed as Legacy in Raspberry Pi Imager) is recommended. Feel free to test Bookworm; any ARM64 Debian-based OS should work if your modem is supported.

We use:

* Python (custom build) for core logic
* GStreamer for video encoding and transmission on the streamer

When preparing the SD card, use the [Raspberry Pi Imager Utility](https://www.raspberrypi.com/news/raspberry-pi-imager-imaging-utility/) and pre-configure WiFi settings for convenience.
