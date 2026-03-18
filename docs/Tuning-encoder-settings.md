The default settings should work reliably in most cases, but they are not the optimum in all cases.

The perfect settings depend on a lot of factors:

* Available Bandwidth
* Lighting situation indoor/outdoor/day/night
* Quickly changing image (crawler vs. racecar)

To find the optimum for your situation, follow these steps:

1. Measure your bandwidth by running the [maximum Bandwidth test](Network-Testing.md#maximum-bandwidth-test) and adjust your bitrate in the configurator accordingly - do not forget to leave some headroom.
2. Set log level to `DEBUG`
3. Enable auto adjusting I-frame size
4. Lower `Min QP` to for example 10
5. Increase `Maximum I-frame bytes`: if you increased bandwidth from 1.8Mbps to 3Mbps for example, you can try increasing this value by the same factor (~1.5). 
6. Go use your rig for a couple of minutes. Watch for stutters
7. Check the video service log - look for dropped packets here
8. Check your viewer log - max jitter is a good indicator: if it is too high, it is a confirmation for stutter

If you did not see stutters and the log does not show any dropped frames, you can repeat steps 4-7, going lower with `Min QP` and higher with `Maximum I-frame bytes`.

Once you found your preferred settings, you can tighten them up a bit:
1. Check the video service log and have a look at the I-frame sizes. If you see that the sizes never come close to your `Maximum I-frame bytes` size, just lower that setting to be closer to real world circumstances. This will help you handling spikes better should the circumstances change.

## Example tuning session
Scenario: Driving a small 1/8 crawler inside the flat in a big city with good LTE coverage. There is some natural light but most of the driving is happening in the evening/night with artificial lighting.

We start with the default values:

* FPS: 30
* I-frame Interval: 15
* Bitrate: 1.8Mbps
* Min QP: 20
* Max QP: 44
* Max I-frame bytes: 40960

The bandwidth test shows close to maximum LTE performance:
```
[  5]   0.00-60.16  sec  34.1 MBytes  4.76 Mbits/sec  5.738 ms  0/28864 (0%)  receiver
```
I know that this is just the case because it is late in the evening but even during the day tests show that it does never drop below 4Mbps, so I set the `Bitrate` to 4.0Mbps. That is an increase of 2.2x.

I drop `Min QP` to 1 and set `Maximum I-frame bytes` to about 2.2x it's default size so `90112` (88KB). I check `Enable auto adjusting I-frame size` and leave the rest as it is. Since I am going slowly, I considered to increase `I-frame period` to 30, but I'll leave it at 15 for now.

I set `Log Level` to `DEBUG`.

Time to drive! I am connected via SSH and follow the video service log:

```
journalctl -u v3xctrl-video -f
```

In the back corners of my flat I see that frames start being dropped, but generally speaking, things are looking good. In the viewer I don't see stutter and the max Jitter is well below 100 ms.

I-frame size stays way below my set maximum of 88KB - sometimes the I-frame size spikes up to 53KB. At this point I am quite happy with how things are, I set `Maximum I-frame bytes` to 61440 (60KB). Just to have a sane limit which does not get hit anyway, but at least I can be sure to not go over this size should any factor change.

I could tighten up `Min QP` a bit, but since I have `Enable auto adjust I-frame size` checked, I am not really bothered by that. Should I see some stuttering in the future, I might increase `Min QP` for a smoother start.