The following issues are known and cannot be easily fixed due to 3rd party dependencies:

For video micro stutter and framerate issues, see [Troubleshooting - Video stream](Troubleshooting.md#video-stream).

## Desktop Viewer

* **Framerate drops when window is being moved on Windows:** This is a pygame(-ce) limitation caused by Windows. The OS pauses rendering while a window is being dragged.

## Android Viewer

* **Control backlog in poor reception:** In areas with bad mobile reception, control inputs may arrive with a 1-2 second delay. This is caused by TCP buffering on the network level.

* **Some carriers block UDP:** Carriers like Google Fi and VIVO may drop UDP packets, preventing video from being received. Use [TCP transport](Connection-Types.md#transport) as a workaround.

## Hardware

### Purple lines in the video feed / Camera jitter in the video service log

#### Reason
This issue may be caused by EMI (electromagnetic interference). It can be induced by power cables, BECs, the modem, or antennas.

#### Solution
The easiest solution is to move the source of EMI away from the camera cable or the camera itself. If this is not possible, shielding the cable with copper tape may help. You can also connect the tape to GND to improve the shielding effectiveness.

## Builing Image in WSL2
Building a flashable Image in WSL2 will not work as F2FS is not supported by its kernel.
