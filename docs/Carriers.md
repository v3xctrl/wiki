This page lists all the carriers that have been tested with this project. See [Modems](Modems.md) for modem specifications and debugging. Feel free to open an issue to share your experience with a new carrier.

In most countries, there are only a few main Mobile Network Operators (MNOs) that own and operate the network infrastructure. Many other carriers are Mobile Virtual Network Operators (MVNOs) that lease access from one of these MNOs. Because of this, if one MNO is supported, carriers using the same MNO are usually supported as well.

There are two types of MVNOs:

* Full MVNOs, which operate their own core network and SIM provisioning while using the host MNO only for radio access.

* Reseller or “light” MVNOs, which depend entirely on the host MNO for both radio and core network services.

MVNOs—especially reseller types—may have some limitations compared to the main operators. These can include lower traffic priority during network congestion, restricted access to certain frequency bands, or missing features such as VoLTE or 5G (which generally are not an issue for this project).

!!! tip
    For the most reliable performance, using a SIM from one of the main MNOs is recommended.

## Testing

To assess your carrier, follow the [Network Testing procedure](Network-Testing.md). A couple of tests will quickly show you if your carrier is up to snuff.

## Europe

### Austria

Country code is `232`.

| MNO     | CCs |
|---------|-----|
| A1      | 01, 02, 09, 11, 12 |
| Drei    | 10, 05, 14, 16, 19 |
| Magenta | 03 (Legacy: 04, 13, 23) |


| Name         | MNO     | Full | CC | Supported | Bands | APN | Notes |
|--------------|---------|------|----|-----------|-------|-----|-------|
| A1           | A1      | Yes  | 01 | Yes       | 3, 7, 8, 20 | webapn.at | |
| Bob          | A1      | No   | 11 | ???       | 3, 7, 8, 20 | | |
| Georg        | A1      | No   | 01 | Yes       | 3, 7, 20 | webapn.at | |
| Yesss!       | A1      | No   | 12 | ???       | 3, 7, 20 | | |
| Magenta      | Magenta | Yes  | 03 | Yes       | 1, 3, 7, 8, 20 | internet.t-mobile.at | |
| Hot          | Magenta | No   | ?? | Yes       | 1, 3, 7, 8, 20 | | |
| Drei         | Drei    | Yes  | 05 | Yes       | | drei.at | |
| eety         | Drei    | No   | ?? | ???       | |  | | |
| Lidl Connect | Drei    | No   | ?? | ???       | |  | | |
| spusu        | Drei    | Yes  | ?? | ???       | |  | | |


## USA

| Name      | MNO      | Supported |
|-----------|----------|-----------|
|Google Fi  | T-Mobile |       ??? |