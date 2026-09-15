Calibration is done through the "_Calibration_" tab in the streamer's web interface, make sure the `control` service is disabled in the "_Services_" tab, otherwise calibration will not work.

**IMPORTANT:** Disconnect the motors or cut their power before calibrating. Each mixer has its own idle pulse, so switching the mixer type, or changing idle, failsafe or reversible, can make a motor spin.

The tab shows the settings for the mixer selected in the *"Config editor"* tab under *"Control" -> "Mixer type"*.

## Ackermann
Following the [pinout guide](Pinout.md) make sure that ESC and Servo are hooked up correctly.

* ESC: PWM1
* SERVO: PWM2

### Servo (Steering)
Steering calibration is quite straight forward, adjust min and max value according to your servo.

Decrease the min value until your preferred position is reached or until the servo starts making noises (that is a sign that you went too far) and dial the range back a bit.

Do the same for the max value, just increasing instead of decreasing the value.

Make sure to adjust trim such that the servo is centered. You will most likely have to fine tune this value during operation, but you should be able to make decent raw adjustments at this point.

### Throttle
**IMPORTANT:** Make sure you read the manual for your ESC, calibration for throttle differs from manufacturer to manufacturer. Most likely you will not have to change min, max and idle values. Instead you will have to send min, idle and max values in a specific order.

## Differential thrust
Following the [pinout guide](Pinout.md) make sure both ESCs are hooked up correctly.

* Motor A: PWM1
* Motor B: PWM2

### Motors
Min, max and idle are shared by both motors, the dead-zones are set per motor.

**IMPORTANT:** Make sure you read the manual for your ESC, the order of operation differs from manufacturer to manufacturer.

If your motors do not reverse, min is simply off. Send idle (off) and then max (full throttle) to each motor.

If your motors reverse, send min (Reverse), max (Forward) and idle (neutral) to each motor, in the order your manual specifies.

Raise the dead-zone of the motor that needs more of a kick than the other to start moving.

### Motor balance
Balance is a live fine-tune for driving, it nudges Motor A up and Motor B down by the same amount and never applies while a motor is at rest.

If one motor consistently needs more of a kick to start, set its dead-zone instead. Use balance only for small corrections on the fly.

## Testing control

After calibration you can use ++w++, ++s++, ++a++, ++d++ in the viewer to verify movement. If steering is inverted, you can adjust it on your streamer in the *"Config editor"* tab under *"Control" -> "Mixer"*, in *"Ackermann steering settings" -> "Steering" -> "Invert steering"* or *"Differential thrust settings" -> "Mixing" -> "Invert steering"*.

At this point you can also go ahead and [set up a controller](Input-devices.md#setup) of your choice.

> If calibration is not working, see [Troubleshooting](Troubleshooting.md).
