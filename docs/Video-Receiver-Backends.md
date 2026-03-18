By default the viewer uses **PyAV** as video receiver backend. This works cross platform and can be easily bundled.

A gstreamer backend is also available but the user has to make sure that all the dependencies are installed on their system and the viewer has to be run from source ([follow the developer setup](Development.md#viewer) to do so).
The viewer checks for those dependencies on startup and will notify you if they are satisfied, you will then see a log like this during startup:

> GStreamer receiver available. Set video.receiver = "gst" in settings to use it.

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