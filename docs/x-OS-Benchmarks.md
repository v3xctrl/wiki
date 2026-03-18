This page is meant to document differences between OS versions:

## Tests
### Boot time

```
systemd-analyze
```

### Load
After 20 minutes of operation
* Connected to viewer
* Video from RPi v3 camera
```
uptime
```

### Resources
After 20 minutes of operation, see above
```
free -h
```

## Debian Bullseye
### Boot time
```
Startup finished in 9.422s (kernel) + 34.667s (userspace) = 44.089s 
multi-user.target reached after 34.598s in userspace
```

### Load
```
11:51:04 up 43 min,  1 user,  load average: 1.04, 1.07, 1.01
```

### Resources
```
               total        used        free      shared  buff/cache   available
Mem:           419Mi       183Mi       123Mi        26Mi       111Mi       154Mi
Swap:           99Mi       3.0Mi        96Mi
```

## Debian Trixie
### Boot time
```
Startup finished in 5.584s (kernel) + 23.014s (userspace) = 28.598s
multi-user.target reached after 23.011s in userspace.
```

### Load
```
10:28:59 up  1:19,  1 user,  load average: 0.92, 0.88, 0.81
```

### Resources
```
               total        used        free      shared  buff/cache   available
Mem:           416Mi       181Mi       105Mi       428Ki       181Mi       234Mi
Swap:          415Mi       109Mi       306Mi
```