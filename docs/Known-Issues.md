The following issues are known and cannot be easily fixed due to 3rd party dependencies:

* Frame-rate drops when window is being moved on Windows: This is a pygame(-ce) limitation - or rather intended behavior - caused by Windows.

### Micro stutter
Sometimes micro stutter might happen in the viewer, this can be fixed by adjusting encoder settings. This usually happens in high detail environments like forests.

#### How to identify
This stutter occurs before an iFrame is received on the viewer, so it will happen in the iFrame interval (1 sec by default). You can verify this by looking for jitter in the viewer's log. If the max jitter is consistently above the length of a frame (33.3ms) then chances are that you are running into this issue.

#### Reason
The reason for this issue is that i-frames are bigger than p-frames and will take longer to be transmitted to the viewer. The size of an i-frame depends on how heavily it can be compressed. 

#### Mitigation
There is a couple ways of mitigating this issue, which one is the right one for you really depends on your circumstances:

1. Decrease framerate: Oftentimes this is fixed by simply decreasing framerate to 24FPS. Lower framerate means that frames have more time to arrive, since less have to arrive per second
2. Decrease QP range, increase min QP - this will make i-frames smaller

##### Calculating maximum i-frame size
Maximum i-frame size can be calculated: Given the framerate and the maximum bandwidth you can calculate how big an i-frame can be to still be transmitted inbetween frames. (Keep in mind, this is an approximation not considering network conditions and jitter, just pure bandwidth).

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

So you should target i-frames no bigger than 11.655kB. You can assume that i-Frames are always a multiple of the p-frames, so it is enough to find out maximum i-frame size to be in the optimal range.

> **NOTE:** The practical limit is usually higher here since the pipeline does have a buffer and you will always have some lag which will compensate for the i-frame burst in size. But with this conservative value you should definitely not see any stuttering. Additionally LTE can momentarily burst over your average bandwidth limit. So this calculated number should be seen as a worst case reference, you can move up from that and see what your practical limits are.

#### Verification
When stutter stops, you have mitigated the issue. For better debugging you can monitor the INFO debug output of the video service, it will show you i-frame size. You can use this as an indicator to find an i-frame size at which the stutter stops.

### Purple lines in the video feed / Camera jitter in the video service log

#### Reason
This issue may be caused by EMI (electromagnetic interference). It can be induced by power cables, BECs, the modem, or antennas.

#### Solution
The easiest solution is to move the source of EMI away from the camera cable or the camera itself. If this is not possible, shielding the cable with copper tape may help. You can also connect the tape to GND to improve the shielding effectiveness.



