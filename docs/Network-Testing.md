Testing network performance is important in order to assess your mobile carrier and your network situation in general. `v3xctrl` is pretty flexible in regards to network requirements but will require at least an LTE connection with 2Mbps upload bandwidth on the streamer side and a connection with at least 2Mbps download bandwidth on the viewer side. Technically less than that is possible, but then the video quality will suffer. 4Mbps bandwidth will give you great results with smooth, clear video - this is achievable on LTE Cat-1 hardware, so basically the lowest specced LTE modems should be fine.

## Built-in Self-Tests

The viewer includes a built-in relay test that can be accessed from the menu: open the menu with ++esc++, switch to the "_Network_" tab, and use the test button.

This test verifies connectivity to the relay server and checks that your session or spectator ID is valid. It is a quick way to confirm your network setup is working before attempting a full connection.

For more detailed network testing (bandwidth, jitter, UDP hole duration), see the sections below.

## Performance
On the streamer, install `iperf3`:
```bash
sudo apt install iperf3
```

On the machine you are running the viewer on, also install `iperf3`. This will only work in direct mode with a fixed IP (or DynDNS for that matter).

!!! note
    Preferably test on the same port that you are using for your video stream. In the example this will be `9999`.

### Server
On the server run:
```
iperf3 -s -p 9999
```

Make sure that port `9999` is forwarded on your router.

### Streamer

#### Maximum bandwidth test

On the streamer run:
```bash
iperf3 -c <server-ip> -u -b 100M -t 60 -p 9999 -l 1400 --get-server-output
```

This will saturate your connection and show the actual maximum throughput. Look at the final "receiver" line to see the peak bitrate achieved. Your video stream target should be around 3/4 to 2/3 of this value to account for the control channel and leave headroom for reliability.

```
[ ID] Interval           Transfer     Bitrate         Jitter    Lost/Total Datagrams
[  5]   0.00-60.19  sec  28.7 MBytes  3.99 Mbits/sec  3.183 ms  2/21464 (0.0093%)  receiver
```

This test tells us that we had an average bitrate of 3.99Mbps for a duration of 60 seconds. This test makes me confident enough to choose the 3.0Mbps setting (realistic maximum for 4G, Cat-1)

!!! note
    We are testing up to 100Mbps, but since the video encoder uses h264 encoding level 4.1 which caps out at 50Mbps we would not be able to use the max bandwidth anyway.

#### Constant bitrate jitter and reliability test

With the value you found in the above test, run the following test to confirm consistent performance:
```
iperf3 -c <server-ip> -u -b 3M -t 60 -p 9999 -l 1400 --get-server-output
```

The interesting output is the "server output" section. It will look something like this:
```
Accepted connection from <streamer-ip>, port 4549
[  5] local 192.168.1.100 port 9999 connected to <streamer-ip> port 4550
[ ID] Interval           Transfer     Bitrate         Jitter    Lost/Total Datagrams
[  5]   0.00-1.00   sec   351 KBytes  2.88 Mbits/sec  1.915 ms  0/257 (0%)  
[  5]   1.00-2.00   sec   369 KBytes  3.02 Mbits/sec  2.066 ms  0/270 (0%)  
[  5]   2.00-3.00   sec   365 KBytes  2.99 Mbits/sec  2.556 ms  0/267 (0%)  
[  5]   3.00-4.00   sec   368 KBytes  3.01 Mbits/sec  1.635 ms  0/269 (0%)  
[  5]   4.00-5.00   sec   364 KBytes  2.98 Mbits/sec  1.818 ms  0/266 (0%)  
[  5]   5.00-6.00   sec   368 KBytes  3.01 Mbits/sec  1.989 ms  0/269 (0%)  
[  5]   6.00-7.00   sec   364 KBytes  2.98 Mbits/sec  2.295 ms  0/266 (0%)  
[  5]   7.00-8.00   sec   368 KBytes  3.01 Mbits/sec  1.876 ms  0/269 (0%)  
[  5]   8.00-9.00   sec   368 KBytes  3.01 Mbits/sec  1.600 ms  0/269 (0%)  
[  5]   9.00-10.00  sec   366 KBytes  3.00 Mbits/sec  1.420 ms  0/268 (0%)  
[  5]  10.00-11.00  sec   365 KBytes  2.99 Mbits/sec  1.394 ms  0/267 (0%)  
[  5]  11.00-12.00  sec   368 KBytes  3.01 Mbits/sec  1.679 ms  0/269 (0%)  
[  5]  12.00-13.00  sec   365 KBytes  2.99 Mbits/sec  1.701 ms  0/267 (0%)  
[  5]  13.00-14.00  sec   366 KBytes  3.00 Mbits/sec  1.649 ms  0/268 (0%)  
[  5]  14.00-15.00  sec   365 KBytes  2.99 Mbits/sec  2.093 ms  0/267 (0%)  
[  5]  15.00-16.00  sec   368 KBytes  3.01 Mbits/sec  1.657 ms  0/269 (0%)  
[  5]  16.00-17.00  sec   365 KBytes  2.99 Mbits/sec  1.631 ms  0/267 (0%)  
[  5]  17.00-18.00  sec   365 KBytes  2.99 Mbits/sec  2.011 ms  0/267 (0%)  
[  5]  18.00-19.00  sec   368 KBytes  3.01 Mbits/sec  1.713 ms  0/269 (0%)  
[  5]  19.00-20.00  sec   366 KBytes  3.00 Mbits/sec  2.000 ms  0/268 (0%)  
[  5]  20.00-21.00  sec   365 KBytes  2.99 Mbits/sec  1.877 ms  0/267 (0%)  
[  5]  21.00-22.00  sec   366 KBytes  3.00 Mbits/sec  1.816 ms  0/268 (0%)  
[  5]  22.00-23.00  sec   365 KBytes  2.99 Mbits/sec  1.851 ms  0/267 (0%)  
[  5]  23.00-24.00  sec   368 KBytes  3.01 Mbits/sec  1.707 ms  0/269 (0%)  
[  5]  24.00-25.00  sec   364 KBytes  2.98 Mbits/sec  1.676 ms  0/266 (0%)  
[  5]  25.00-26.00  sec   369 KBytes  3.02 Mbits/sec  1.584 ms  0/270 (0%)  
[  5]  26.00-27.00  sec   366 KBytes  3.00 Mbits/sec  1.833 ms  0/268 (0%)  
[  5]  27.00-28.00  sec   366 KBytes  3.00 Mbits/sec  1.833 ms  0/268 (0%)  
[  5]  28.00-29.00  sec   364 KBytes  2.98 Mbits/sec  1.653 ms  0/266 (0%)  
[  5]  29.00-30.00  sec   366 KBytes  3.00 Mbits/sec  1.967 ms  0/268 (0%)  
[  5]  30.00-31.00  sec   366 KBytes  3.00 Mbits/sec  2.158 ms  0/268 (0%)  
[  5]  31.00-32.00  sec   366 KBytes  3.00 Mbits/sec  2.201 ms  0/268 (0%)  
[  5]  32.00-33.00  sec   369 KBytes  3.02 Mbits/sec  1.640 ms  0/270 (0%)  
[  5]  33.00-34.00  sec   364 KBytes  2.98 Mbits/sec  2.040 ms  0/266 (0%)  
[  5]  34.00-35.00  sec   366 KBytes  3.00 Mbits/sec  1.774 ms  0/268 (0%)  
[  5]  35.00-36.00  sec   369 KBytes  3.02 Mbits/sec  1.522 ms  0/270 (0%)  
[  5]  36.00-37.00  sec   362 KBytes  2.97 Mbits/sec  1.755 ms  0/265 (0%)  
[  5]  37.00-38.00  sec   366 KBytes  3.00 Mbits/sec  2.040 ms  0/268 (0%)  
[  5]  38.00-39.00  sec   368 KBytes  3.01 Mbits/sec  1.769 ms  0/269 (0%)  
[  5]  39.00-40.00  sec   368 KBytes  3.01 Mbits/sec  1.679 ms  0/269 (0%)  
[  5]  40.00-41.00  sec   366 KBytes  3.00 Mbits/sec  1.582 ms  0/268 (0%)  
[  5]  41.00-42.00  sec   364 KBytes  2.98 Mbits/sec  2.045 ms  0/266 (0%)  
[  5]  42.00-43.00  sec   366 KBytes  3.00 Mbits/sec  1.978 ms  0/268 (0%)  
[  5]  43.00-44.00  sec   369 KBytes  3.02 Mbits/sec  1.718 ms  0/270 (0%)  
[  5]  44.00-45.00  sec   362 KBytes  2.97 Mbits/sec  1.980 ms  0/265 (0%)  
[  5]  45.00-46.00  sec   369 KBytes  3.02 Mbits/sec  1.543 ms  0/270 (0%)  
[  5]  46.00-47.00  sec   364 KBytes  2.98 Mbits/sec  1.789 ms  0/266 (0%)  
[  5]  47.00-48.00  sec   369 KBytes  3.02 Mbits/sec  1.623 ms  0/270 (0%)  
[  5]  48.00-49.00  sec   365 KBytes  2.99 Mbits/sec  1.821 ms  0/267 (0%)  
[  5]  49.00-50.00  sec   364 KBytes  2.98 Mbits/sec  2.006 ms  0/266 (0%)  
[  5]  50.00-51.00  sec   369 KBytes  3.02 Mbits/sec  1.712 ms  0/270 (0%)  
[  5]  51.00-52.00  sec   365 KBytes  2.99 Mbits/sec  1.704 ms  0/267 (0%)  
[  5]  52.00-53.00  sec   366 KBytes  3.00 Mbits/sec  1.866 ms  0/268 (0%)  
[  5]  53.00-54.00  sec   366 KBytes  3.00 Mbits/sec  1.563 ms  0/268 (0%)  
[  5]  54.00-55.00  sec   366 KBytes  3.00 Mbits/sec  1.799 ms  0/268 (0%)  
[  5]  55.00-56.00  sec   365 KBytes  2.99 Mbits/sec  1.727 ms  0/267 (0%)  
[  5]  56.00-57.00  sec   369 KBytes  3.02 Mbits/sec  1.555 ms  0/270 (0%)  
[  5]  57.00-58.00  sec   364 KBytes  2.98 Mbits/sec  1.867 ms  0/266 (0%)  
[  5]  58.00-59.00  sec   365 KBytes  2.99 Mbits/sec  1.885 ms  0/267 (0%)  
[  5]  59.00-60.00  sec   369 KBytes  3.02 Mbits/sec  1.504 ms  0/270 (0%)  
[  5]  60.00-60.04  sec  12.3 KBytes  2.67 Mbits/sec  1.669 ms  0/9 (0%)  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Jitter    Lost/Total Datagrams
[  5]   0.00-60.04  sec  21.5 MBytes  3.00 Mbits/sec  1.669 ms  0/16072 (0%)  receiver
```

### Interpreting the results
The last line shows us the average jitter: **1.669 ms**.
The last line also shows us packet loss: **0%** (Can't get any better than this, some loss is acceptable though).
Looking at the jitter column, we want to find the maximum jitter, which is **2.295 ms** - this happened during seconds 6-7.

When looking at the values, the weight is as follows, from most important to least important:

* Lowest possible max jitter
* Lowest possible average jitter
* Lowest possible packet loss

These metrics should be used when evaluating carriers, modems and antennas. Keep in mind that those tests need to be run under the same conditions to be comparable. Streamer needs to be in the same position, and server has to be the same one. So basically keep everything the same apart from the one thing you are trying to compare.

### Considerations
* The above test is only running for 60 seconds, consider running it for a longer time-frame to catch thermal throttling, congestion patterns or periodic interference.
* Run a couple of tests and average the results.
* Match the test bitrate to your target stream bitrate for results closest to reality
* the `-l` parameter is payload size, match this to your MTU value in the `gstreamer` transmitter
* Data usage - Just because you _can_ go with a higher bandwidth, doesn't mean you _should_. Also consider your data limits.

## Routing
To get a feeling of how your packets are routed, run:
```
mtr rendezvous.websium.at
```

Or even better - use the IP address of your Viewer machine if you are using a direct connection. This will show you if there is a particular hop that might be causing issues.

Unfortunately routing is not something you can change, but it can help you with debugging networking issues: You can identify hops that are causing issues (high loss or high jitter). This is very useful for comparing different carriers with each other. When looking at loss, focus at the loss at the destination hop first. If you see loss there, then work backwards through the hops to identify where it originates. Loss at an intermediate hop does not tell the full truth - it could just mean that the hop is deprioritizing ICMP replies and not actually dropping your packets.

Generally speaking you are looking for the least loss and lowest jitter. Less than 1% loss is ideal for video streaming, 1-5% is acceptable with modern codecs, and anything above 5% will likely cause visible problems.

## UDP Hole Duration
Without going into too much details, mobile devices usually are assigned a local (to the carrier) IP address, so they will not have their dedicated IP address. This makes it difficult to directly access a device behind a mobile carrier NAT. An easy way is to allow the mobile device to "punch a hole" through the carrier NAT, establishing an open channel to a different peer. While this hole is open, the two peers can communicate freely through the port they established the connection through. This hole is kept open as long as traffic flows. It is important to know how long this hole will be open, so that heartbeats can be sent in order to keep the hole open.

In order to test this, there are two scripts in place, you need to first run the server script on the viewer from the `src` directory:

```
cd ./src
python -m v3xctrl_self_test.viewer 9999
```

Then on the streamer change into the self test directory and run the tests
```
cd /opt/v3xctrl-venv/lib/python3.11/site-packages/v3xctrl_self_test/
v3xctrl-python -m v3xctrl_self_test.streamer <VIEWER_IP> 9999
```

This will test the hole opening duration in 30 second increments.

The output will look like this
```
--- UDP hole duration test ---
+ Received timeout request:   30.00 OK
+ Received timeout request:   60.00 OK
+ Received timeout request:   90.00 OK
+ Received timeout request:  120.00 FAILED
No new request received from client.
--- Results ---
Minimum hole lifetime: 90.0s
```

We now know that the minimum lifetime of the UDP hole is somewhere between 90 and 120 seconds.

Once you have found the rough range, you can try to fine tune it to start at the last known min time and increment by 10 seconds:
```
v3xctrl-python -m v3xctrl_self_test.streamer <VIEWER_IP> 9999 --min-timeout 90 --increment 10
```

```
--- UDP hole duration test ---
+ Received timeout request:   90.00 OK
+ Received timeout request:  100.00 OK
+ Received timeout request:  110.00 OK
+ Received timeout request:  120.00 OK
+ Received timeout request:  130.00 FAILED
No new request received from client.
--- Results ---
Minimum hole lifetime: 120.0s

```

And refine it one more time:
```
v3xctrl-python -m v3xctrl_self_test.streamer <VIEWER_IP> 9999 --min-timeout 120 --increment 1
```

```
--- UDP hole duration test ---
+ Received timeout request:  120.00 OK
+ Received timeout request:  121.00 FAILED
No new request received from client.
--- Results ---
Minimum hole lifetime: 120.0s
```

At this point you can conclude that the NAT keeps a UDP hole open for 120 seconds.