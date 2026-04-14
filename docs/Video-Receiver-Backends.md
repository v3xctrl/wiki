By default the viewer uses **PyAV** as video receiver backend. This works cross platform and can be easily bundled.

A GStreamer backend is also available but the user has to make sure that all the dependencies are installed on their system and the viewer has to be run from source ([follow the developer setup](Development.md#viewer) to do so).
The viewer checks for GStreamer dependencies on startup. If they are available, GStreamer will be used automatically as the preferred backend. You will see this in the startup log:

> GStreamer receiver available, will be used by default

## Installation
The installation differs depending on your operating system

### Linux
On a Debian-based Linux system you will have to install the following dependencies:

```
sudo apt install gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-libav
```

Install gst dependencies for python (within your venv):

```
 pip install -r build/requirements/viewer_gst.txt
```

Running with INFO log level will show you which plugins might be missing
```
python -m v3xctrl_ui.main --log INFO
```

### Windows

[WORK IN PROGRESS]