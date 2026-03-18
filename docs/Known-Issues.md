The following issues are known and cannot be easily fixed due to 3rd party dependencies:

* Frame-rate drops when window is being moved on Windows: This is a pygame(-ce) limitation - or rather intended behavior - caused by Windows.

For video micro stutter issues, see [Troubleshooting](Troubleshooting.md#micro-stutter).

### Purple lines in the video feed / Camera jitter in the video service log

#### Reason
This issue may be caused by EMI (electromagnetic interference). It can be induced by power cables, BECs, the modem, or antennas.

#### Solution
The easiest solution is to move the source of EMI away from the camera cable or the camera itself. If this is not possible, shielding the cable with copper tape may help. You can also connect the tape to GND to improve the shielding effectiveness.



