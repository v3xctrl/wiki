This page lists all default credentials, ports, and addresses used by v3xctrl.

## Access Point

When the streamer cannot connect to a configured WiFi network (or none is configured), it will create its own access point.

| Setting | Value |
|---------|-------|
| SSID | `v3xctrl-<device_id>` |
| Password | `raspberry` |
| IP address | `192.168.23.1` |

## Web Interface

| Setting | Value |
|---------|-------|
| Port | `80` |
| URL (client mode) | `http://v3xctrl.local` |
| URL (AP mode) | `http://192.168.23.1` |

## Video

| Setting | Value |
|---------|-------|
| Video port | `16384` (UDP) |

## Samba Share

The recordings directory is shared via Samba (disabled by default, enable in Extras config).

| Setting | Value |
|---------|-------|
| Path | `smb://v3xctrl.local/recordings` |
| Username | `v3xctrl` |
| Password | `v3xctrl` |
