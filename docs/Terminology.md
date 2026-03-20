A collection of terminology used throughout the project.

## General

* **Streamer** - The hardware platform responsible for capturing and streaming video (typically a Raspberry Pi Zero 2 W with a 4G modem).
* **Viewer** - The computer or mobile device that receives the video stream from the streamer, displays it, and sends control data back.
* **Relay** - A server used when the viewer does not have a fixed IP address (e.g., both devices are on mobile networks). The relay facilitates connectivity between the streamer and the viewer.
* **FPV** (First-Person View) - A control method where the operator sees real-time video from the vehicle's perspective.

## Networking

* **UDP** (User Datagram Protocol) - The default transport protocol used for sending both video and control data. Prioritizes speed over reliability.
* **TCP** (Transmission Control Protocol) - An alternative transport protocol available for relay connections. More reliable than UDP but slightly higher latency.
* **NAT** (Network Address Translation) - The process of translating IP addresses to allow devices behind a router or modem to communicate with the internet.
* **CGNAT** (Carrier-Grade NAT) - NAT applied at the mobile carrier level, meaning your device does not get a public IP address. This is why direct inbound connections to mobile devices are not possible and UDP hole punching or a relay is needed.
* **APN** (Access Point Name) - A configuration parameter that tells your modem how to connect to the carrier's data network.
* **RNDIS** (Remote Network Driver Interface Specification) - A protocol that allows 4G modems to present themselves as network devices to the host computer.
* **MNO** (Mobile Network Operator) - A carrier that owns and operates its own mobile network infrastructure.
* **MVNO** (Mobile Virtual Network Operator) - A carrier that provides mobile services by leasing network access from an MNO.
* **LTE** (Long-Term Evolution) - The 4G mobile network standard used for data connectivity.
* **Cat 1 / Cat 4** - LTE modem categories defining maximum bandwidth. Cat 1 supports up to 10 Mbps down / 5 Mbps up. Cat 4 supports up to 150 Mbps down / 50 Mbps up.
* **SSH** (Secure Shell) - A network protocol for secure remote access to the streamer's command line.
* **AP** (Access Point) - A WiFi mode where the streamer creates its own wireless network for configuration when no known WiFi network is available.

## Video

* **H.264** - The video codec used for encoding. It offers high compression efficiency, good quality at low bitrates, and is widely supported in hardware encoders.
* **I-frame** (Intra-coded frame) - A complete video frame that can be decoded independently. Sent periodically to allow recovery from packet loss.
* **P-frame** (Predicted frame) - A video frame that only contains changes from the previous frame, significantly reducing bandwidth usage.
* **QP** (Quantization Parameter) - An encoder setting that controls the quality-to-bitrate tradeoff. Lower QP means higher quality but larger frames.
* **FPS** (Frames Per Second) - The number of video frames captured and transmitted per second.
* **OSD** (On-Screen Display) - The overlay on the viewer showing real-time telemetry such as latency, battery voltage, signal quality, and FPS.
* **GStreamer** - An open-source multimedia framework used on the streamer for video capture, encoding, and streaming.
* **ISP** (Image Signal Processor) - Hardware that processes raw camera sensor data into usable image formats.

## Hardware

* **SBC** (Single Board Computer) - A complete computer on a single circuit board, such as the Raspberry Pi.
* **ESC** (Electronic Speed Controller) - A device that regulates power delivery to electric motors based on PWM input.
* **BEC** (Battery Elimination Circuit) - A DC-DC voltage converter that provides stable 5V power to the Raspberry Pi from a battery.
* **PWM** (Pulse Width Modulation) - A signal technique used to control servos and ESCs by varying the width of electrical pulses.
* **GPIO** (General Purpose Input/Output) - Programmable digital pins on the Raspberry Pi that can be used as inputs or outputs.
* **CSI** (Camera Serial Interface) - The ribbon cable interface on Raspberry Pi used to connect camera modules.
* **I2C** (Inter-Integrated Circuit) - A two-wire serial communication protocol used for connecting sensors like the INA voltage monitor.
* **SDA / SCL** - The data and clock lines of the I2C protocol.
* **INA** - A Texas Instruments current/voltage measurement IC (e.g., INA226, INA231) used for battery monitoring.
* **UART** (Universal Asynchronous Receiver-Transmitter) - A serial communication interface used for debugging and GPS connections.
* **VNA** (Vector Network Analyzer) - Test equipment used to measure antenna impedance and performance.
* **SWR** (Standing Wave Ratio) - A measurement of how well an antenna is matched to its transmission line. Lower SWR indicates better performance.

## Software

* **Python** - The programming language most of this project is written in. A custom build of Python is used on the streamer to ensure compatibility.
* **systemd** - The Linux service manager used to start, stop, and monitor v3xctrl services on the streamer.
* **OverlayFS** - A filesystem layer that makes the root partition read-only, protecting the SD card from corruption. Changes are stored in memory.
* **msgpack** - A binary serialization format used for efficiently encoding control channel messages between streamer and viewer.
