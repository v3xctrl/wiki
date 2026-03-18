## Latency
**The main limitation for any FPV system is latency**. Latency must be as low as possible for smooth operations so that your inputs do what you expect them to. Latency is also something that everyone experiences subjectively, some people can adjust to more latency, some can't (or won't).

You can find more information about latency on our dedicated [wiki page](Latency.md).

Keep in mind, that we are running this on off-the-shelf commodity hardware and intended use is over a 4G/LTE network so we will never be able to compete with commercial FPV hardware. If you are looking for lowest possible latency, you will have to look at analog systems. The next best thing are digital FPV systems. Digital FPV systems offer less latency than v3xctrl but more than analog, with less theoretical range.

Currently our minimal avg glass-to-glass latency is **115ms**. On top of this you need to account for network latency for control input, bringing total input-to-response latency to around 120ms - before human reaction time. This can be a lot of time, or insignificant, depending on your exact use case. Generally speaking it is less of an issue on slower moving vehicles (e.g.: Crawlers) and more of an issue on fast moving vehicles - requiring very precise movement (e.g.: Quadcopters).

## Reception
This plays into latency but needs to be mentioned separately, your mobile reception will have a lot of influence in how the system works. Different providers perform differently in different areas. It is highly recommended to do your research of how well your area is covered by different providers using tools like [cellmapper.net](https://cellmapper.net)