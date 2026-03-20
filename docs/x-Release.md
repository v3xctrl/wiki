!!! note
    X-Files are only relevant for developers/maintainers!

## Packages

For building packages (chroot and on-device) and flashable images, see the [Development guide](Development.md#building).

## GitHub Workflows
### Viewer
This one is straight forward, new artifacts are built on every push and PR.

When creating a new release, just attach the latest builds to the release.

TODO: This can probably also be done automatically when tagging

### Streamer
Streamer is a bit more complicated:

#### Python
Build of custom python version can be triggered manually. This should not be necessary too often, unless we need to upgrade to a new specific version for some reason.

This will result in an artifact with a deb file, attach that to the latest release.

TODO: as above - do this automatically when tagging

#### v3xctrl
Build of v3xctrl can be triggered manually.

This will result in an artifact with a deb file, attach that to the latest release.

TODO: as above - do this automatically when tagging
TODO: This does not take too long to build, we could consider building this on every push and PR too.

### Image
Building of the custom PiOS image is triggered manually. This will use the `deb` packages attached to the latest release. Once the image is built, it can be attached to the latest release.

TODO: as above - do this automatically when tagging
