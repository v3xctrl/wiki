Antenna selection is extremely important and will greatly affect the performance of your streamer.

4G uses [different bands](https://en.wikipedia.org/wiki/LTE_frequency_bands) depending on the location and provider. In those bands, different ranges are used for up/downlink.

You need to understand the topology of the area you are intending to use v3xctrl in.

> If you are in an urban area, the PCB/Flex antennas will probably do the job, but in any other case a good omni-directional antenna will make a big difference.

Use [cellmapper](https://www.cellmapper.net/) to find out more about your region. First set your location, then select your carrier and 4G - LTE as network. In the Band dropdown, you can already see the bands your provide is using in your selected area.

> E.g.: Location set to "Vienna", Provider set to "A1 Telekom Austria - Austria - 2321", Network set to "4G - LTE". Bands Dropdown shows B1, B3, B7 and B20 - so those are the bands you will be interested in. But you can check in with finer granularity: Select the specific bands and see hom many nodes are still left on the map.
In this case, B1 only shows a single tower which has not been seen for a significant amount of time, so we can exclude it.
B3 and B7 are the most widely used in this area, but B20 also has a fair amount of nodes.
So when looking for an antenna for this region, I would make sure that it performs well on those 3 bands.

LTE Band | DL (MHz) | Center | UL (MHz) | Center | Notes
-- | -- | -- | -- | -- | --
B7 | 2620–2690 | 2655 | 2500–2570 | 2535 | High-capacity urban (2600 MHz)
B3 | 1805–1880 | 1842 | 1710–1785 | 1747 | Most common in cities (1800 MHz)
B20 | 791–821 | 806 | 832–862 | 847 | Primary rural coverage, very common

You can see, that those bands have different bandwidths for up and downlink. When selecting Antennas, I would compare SWR at all those center frequencies. The best match would then be the one with the lowest SWR at all those frequencies.


## Testing Antennas
This part is unfortunately not possible without dedicated equipment. You will need a VNA. A low cost option is the LiteVNA64. You will then save the s1p file and run the script to generate the graphs.

We run two separate measurements:
1. 600-1000MHz
2. 1500-1800MHz

Save two separate s1p files and join them manually. This is just so we have more samples per range.

## Tested Antennas
Graphs for all the tested antennas can be found in `graphs`, the s1p file they were generated from are in `data`.

### Delock 88416
?

<img alt="Delock_88416_SWR" src="https://github.com/user-attachments/assets/c51590c4-29fa-4c33-a66d-fa07a9e87d95" />

### Vievre
[Shop EU](https://www.amazon.de/dp/B0D9NBCM6D)

<img alt="Vievre_SWR" src="https://github.com/user-attachments/assets/bf76cb04-8de1-4d59-8626-b8f05ad8182a" />

### Nelawya
[Shop EU](https://www.amazon.de/dp/B0BG6PLX2L)

<img alt="Nelawya_SWR" src="https://github.com/user-attachments/assets/22a89329-2edd-4fd5-96e7-8267feb594cb" />

### Retoo
[Shop EU](https://www.amazon.de/dp/B09MZ84YS6)

<img alt="Retoo_SWR" src="https://github.com/user-attachments/assets/c496a197-fb0c-4c38-b604-61ae59f55f2b" />

### Noname_01
[Shop EU](https://www.amazon.de/dp/B0DL5LHY9P)

<img alt="Noname_01_SWR" src="https://github.com/user-attachments/assets/06747eb9-0c61-4e23-b960-c8d1beb07e17" />

### Noname_02
[Shop EU](https://botland.de/lte-antennen/17836-antenne-lte-8db-sma-19cm-2st-5907621817305.html)

<img alt="Noname_02_SWR" src="https://github.com/user-attachments/assets/e2b58b7a-d56a-4e9b-8e2e-1a08618e99a5" />

### Flex_01
[Shop EU](https://de.aliexpress.com/item/1005004221609925.html)

<img alt="Flex_01_SWR" src="https://github.com/user-attachments/assets/68b39727-e97b-4e80-8d70-4faa8cea5dab" />

### DollaTek_Lora
[Shop EU](https://www.amazon.de/dp/B07QXPN3YR)

<img alt="DollaTek_Lora_SWR" src="https://github.com/user-attachments/assets/dbd0a298-51f5-4e68-894b-e152651c4736" />

### Emsea
[Shop EU](https://www.amazon.de/dp/B0DCZFRDJG)

<img alt="Emsea_SWR" src="https://github.com/user-attachments/assets/e4577193-172a-47bf-ab80-46f36874f99b" />

### EuAcesry
[Shop EU](https://www.amazon.de/dp/B0DPMTG5BG)

<img alt="EuAcesry_SWR" src="https://github.com/user-attachments/assets/d748192e-eac2-4225-8dea-aa44b99bb182" />

### Bingfu
[Shop EU](https://www.amazon.de/dp/B09MYBS23C)

<img alt="Bingfu_SWR" src="https://github.com/user-attachments/assets/793904ff-ef05-42c3-ae22-3a00265840b6" />
