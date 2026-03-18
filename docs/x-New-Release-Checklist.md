## Quick function check

* [ ] Viewer starts
* [ ] Streamer starts
* [ ] Direct connection is working
* [ ] Relay connection is working

## In depth check
Most issues should be caught by the extensive test suite, a manual check should still be performed, especially before major releases.

### Viewer

#### Desktop

##### Menu

* [ ] Can open menu
* [ ] Can switch tabs
* [ ] Can close menu (via ++esc++ and back button)
* [ ] General: Disabling connection info works
* [ ] General: Fullscreen toggle works via checkbox and ++f11++ (updates the checkbox correctly)
* [ ] Input: Detects gamepad for calibration
* [ ] Input: Can calibrate Gamepad
* [ ] Input: Saves calibration between restarts
* [ ] Input: Saves calibration for multiple gamepads/wheels
* [ ] Input: can map buttons on gamepad
* [ ] Input: can set deadband on gamepad
* [ ] Input: can invert axis on gamepad
* [ ] Input: Can remap Key-bindings
* [ ] Input: Shows axis input for calibrated gamepad
* [ ] OSD: elements can be enabled/disabled
* [ ] OSD: Setting changes are visible without restart
* [ ] Network: Toggling "Use UDP Relay" checkbox reconnects on "Save" and Back
* [ ] Network: Spectator Mode connects with valid spectator ID
* [ ] Streamer: Can start/stop video
* [ ] Streamer: Can reboot streamer
* [ ] Streamer: Can shutdown streamer
* [ ] Streamer: Can start/stop recording via hotkey
* [ ] Streamer: Can start/stop recording via button on gamepad
* [ ] Quit button stops the viewer

##### Main screen

* [ ] Displays direct connection settings
* [ ] Keyboard inputs detected
* [ ] Gamepad inputs detected
* [ ] Throttle widget updates on input
* [ ] Steering widget updates on input
* [ ] Debug widgets are updating correctly
* [ ] Reception widget is updating correctly
* [ ] Battery widget is updating correctly
* [ ] Toggling fullscreen with ++f11++ works
* [ ] Fullscreen setting remembered between restarts
* [ ] Saving settings is working (settings are reloaded after viewer restart)
* [ ] Debug flag shows additional output
* [ ] Video from streamer is correctly displayed in viewer
* [ ] Viewer shows recording indicator when recording has been triggered from viewer
* [ ] Viewer shows recording indicator when auto recording is enabled on the streamer
* [ ] Trimming with hotkeys works
* [ ] Toggling recording works with hotkey

##### Edge Cases

* [ ] Reboot streamer while viewer is running, make sure viewer will re-connect

#### Android

* [ ] Can open app
* [ ] Shows warning without session ID
* [ ] Connects with valid session ID
* [ ] Shows error with invalid session ID
* [ ] Allows starting/stopping video from portrait mode
* [ ] Allows starting/stopping recording from portrait mode
* [ ] Shuts down from portrait mode
* [ ] Reboots from portrait mode
* [ ] Shows latency mode in portrait mode
* [ ] Shows battery voltage in portrait mode
* [ ] Shows signal reception in portrait mode
* [ ] Shows image in landscape mode
* [ ] Shows battery info in landscape mode
* [ ] Shows signal info in landscape mode
* [ ] Touch control works
* [ ] Motion control works
* [ ] Pairing gamepad works
* [ ] Control via gamepad works
* [ ] OSD elements are shown based on toggled settings
* [ ] No signal/video is shown when control/video channel are lost
* [ ] Disconnect works

### Streamer

* [ ] Web interface is accessible in Client mode
* [ ] Streamer starts in AP mode when no known Host WiFi is nearby
* [ ] Web interface is accessible in AP mode
* [ ] Control service auto starts by default
* [ ] Video service autostarts when configured to do so
* [ ] Settings are saved between reboots
* [ ] Remounting to RW works (disables overlay FS and remounts /root/firmware as RW)
* [ ] Remounting to RO works (reverse from above)
* [ ] Shows RO state on login via SSH
* [ ] Shows connection info on login via SSH

### Relay Testing
* Make sure, viewer, streamer and spectator all connect from the same IP.

#### Relay Test Button in Viewer Menu

* [ ] Use the test button with an invalid session ID
* [ ] Use the test button with a valid session ID
* [ ] Use the test button with an invalid spectator ID
* [ ] Use the test button with a valid spectator ID

#### UDP Detailed testing
Verify with the stats dashboard if needed - make sure UDP is used on both ends.

* [ ] Establish session, make sure the timeouts keep getting updated while both peers are connected
* [ ] Establish session, restart viewer, make sure session is picked up again.
* [ ] Establish session, restart streamer, make sure session is picked up again.
* [ ] Establish session, change ports on viewer, restart viewer, make sure session is picked up again.
* [ ] Establish session, change ports on streamer, restart streamer, make sure session is picked up again.
* [ ] Establish session, stop viewer, wait for the session to time out. Make sure session is picked up again when starting the viewer.
* [ ] Establish session, stop Streamer, wait for the session to time out. Make sure session is picked up again when starting the streamer.
* [ ] Make sure timeouts are updated while session is fully established
* [ ] Make sure timeouts are updated when viewer is disconnected and viewer is removed from session
* [ ] Make sure timeouts are updated when streamer is disconnected and streamer is removed from session
* [ ] Make sure timeouts are updated when streamer and viewer are disconnected and session is removed

#### TCP Detailed testing
Verify with the stats dashboard if needed - make sure TCP is used on both ends.

* [ ] Establish session, make sure the timeouts keep getting updated while both peers are connected
* [ ] Establish session, restart viewer, make sure session is picked up again.
* [ ] Establish session, restart streamer, make sure session is picked up again.
* [ ] Establish session, change ports on viewer, restart viewer, make sure session is picked up again.
* [ ] Establish session, change ports on streamer, restart streamer, make sure session is picked up again.
* [ ] Establish session, stop viewer, wait for the session to time out. Make sure session is picked up again when starting the viewer.
* [ ] Establish session, stop Streamer, wait for the session to time out. Make sure session is picked up again when starting the streamer.
* [ ] Make sure timeouts are updated while session is fully established
* [ ] Make sure timeouts are updated when viewer is disconnected and viewer is removed from session
* [ ] Make sure timeouts are updated when streamer is disconnected and streamer is removed from session
* [ ] Make sure timeouts are updated when streamer and viewer are disconnected and session is removed

#### Mixed Mode Detailed testing 1/3
Verify with the stats dashboard if needed - make sure TCP is used on the streamer, UDP on the viewer.

* [ ] Establish session, make sure the timeouts keep getting updated while both peers are connected
* [ ] Establish session, restart viewer, make sure session is picked up again.
* [ ] Establish session, restart streamer, make sure session is picked up again.
* [ ] Establish session, change ports on viewer, restart viewer, make sure session is picked up again.
* [ ] Establish session, change ports on streamer, restart streamer, make sure session is picked up again.
* [ ] Establish session, stop viewer, wait for the session to time out. Make sure session is picked up again when starting the viewer.
* [ ] Establish session, stop Streamer, wait for the session to time out. Make sure session is picked up again when starting the streamer.
* [ ] Make sure timeouts are updated while session is fully established
* [ ] Make sure timeouts are updated when viewer is disconnected and viewer is removed from session
* [ ] Make sure timeouts are updated when streamer is disconnected and streamer is removed from session
* [ ] Make sure timeouts are updated when streamer and viewer are disconnected and session is removed

#### Mixed Mode Detailed testing 2/3
Verify with the stats dashboard if needed - make sure UDP is used on the streamer, TCP on the viewer.

* [ ] Establish session, make sure the timeouts keep getting updated while both peers are connected
* [ ] Establish session, restart viewer, make sure session is picked up again.
* [ ] Establish session, restart streamer, make sure session is picked up again.
* [ ] Establish session, change ports on viewer, restart viewer, make sure session is picked up again.
* [ ] Establish session, change ports on streamer, restart streamer, make sure session is picked up again.
* [ ] Establish session, stop viewer, wait for the session to time out. Make sure session is picked up again when starting the viewer.
* [ ] Establish session, stop Streamer, wait for the session to time out. Make sure session is picked up again when starting the streamer.
* [ ] Make sure timeouts are updated while session is fully established
* [ ] Make sure timeouts are updated when viewer is disconnected and viewer is removed from session
* [ ] Make sure timeouts are updated when streamer is disconnected and streamer is removed from session
* [ ] Make sure timeouts are updated when streamer and viewer are disconnected and session is removed

#### Mixed Mode Detailed testing 3/3

* [ ] Make sure that switching protocol on the viewer will allow the viewer to reconnect
* [ ] Make sure that switching protocol on the streamer will allow the streamer to reconnect

#### Spectator
Make sure the session is established before attempting to connect.

* [ ] Make sure you can connect to a session as spectator via UDP while streamer is transmitting via UDP
* [ ] Make sure you can connect to a session as spectator via TCP while streamer is transmitting via UDP
* [ ] Make sure you can connect to a session as spectator via UDP while streamer is transmitting via TCP
* [ ] Make sure you can connect to a session as spectator via TCP while streamer is transmitting via TCP
* [ ] Restart Spectator, make sure you can reconnect via UDP
* [ ] Restart Spectator, make sure you can reconnect via TCP
* [ ] Make sure you can switch from TCP to UDP
* [ ] Make sure you can switch from UDP to TCP
* [ ] Make sure the timeout is properly updated while connected via UDP
* [ ] Make sure the timeout is properly updated while connected via TCP
* [ ] Make sure the timeout is properly updated when disconnected and spectator is removed via UDP
* [ ] Make sure the timeout is properly updated when disconnected and spectator is removed via TCP

#### Android
When you reached this point, we can assume that the relay itself is working as it is expected to. This will validate that the android viewer matches the functionality of the Desktop Viewer.

##### Viewer

* [ ] Make sure you can establish a new session via UDP
* [ ] Make sure you can establish a new session via TCP
* [ ] Make sure you can switch between UDP and TCP

##### Spectator

* [ ] Make sure you can join a session via UDP
* [ ] Make sure you can join a session via TCP
* [ ] Make sure you can switch between UDP and TCP
* [ ] Make sure timeouts are updated while connected
* [ ] Make sure spectator is removed when disconnected

#### Discord bot

* [ ] Requesting ID works (session ID & spectator id)
* [ ] Renewing ID works (session ID & spectator id are both changed)
* [ ] Stats are displayed
* [ ] Stats are only displayed to users with `stats` role
