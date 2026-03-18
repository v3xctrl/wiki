Calibration is done through the "_Calibration_" tab in the streamers web-interface, make sure the `control` service is disabled in the "_Services_" tab, otherwise calibration will not work.

Following the [pinout guide](Pinout.md) make sure that ESC and Servo are hooked up correctly.

* ESC: PWM1
* SERVO: PWM2

## Servo (Steering)
Steering calibration is quite straight forward, adjust min and max value according to your servo.

Decrease the min value until your preferred position is reached or until the servo starts making noises (that is a sign that you went to far) and dial the range back a bit.

Do the same for the max value, just increasing instead of decreasing the value.

Make sure to adjust trim such that the servo is centered. You will most likely have to fine tune this value during operation, but you should be able to make decent raw adjustments at this point.

## Throttle
**IMPORTANT:** Make sure you read the manual for your ESC, calibration for throttle differs from manufacturer to manufacturer. Most likely you will not have to change, min, max and idle values. Instead you will have to send min, idle and max values in a specific order.

## Testing control

After calibration you can use **[w]**, **[s]**, **[a]**, **[d]** in the viewer to verify movement. If steering is inverted, you can adjust it on your streamer in the *"Config editor"* tab under *"Controls" -> "Steering" -> "Invert Steering"*.

At this point you can also go ahead and [setup a controller]() of your choice.

Test
