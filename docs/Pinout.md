Connect your peripherals according to the following pinout:
<table>
<tr>
<td width="400px">
<img alt="zero2-close-up webp" src="https://github.com/user-attachments/assets/b12df9a9-5fe8-4d1a-a2a3-672e65cdd50f" />
</td>
<td>

|Func.|Pin|Pin|Func.|
|-----|---|---|----|
| 3.3V | 1 | 2 | 5V |
| SDA (I2C) | 3 | 4 | **5V** |
| SCL (I2C) | 5 | 6 | **GND** |
| --- | 7 | 8 | TX (UART0) |
| --- | 9 | 10 | RX (UART0) |
| --- | 11 | 12 | **PWM1** |
| --- | 13 | 14 | GND |
| --- | 15 | 16 | --- |
| --- | 17 | 18 | --- |
| --- | 19 | 20 | GND |
| --- | 21 | 22 | --- |
| --- | 23 | 24 | --- |
| GND | 25 | 26 | --- |
| --- | 27 | 28 | --- |
| LED0* | 29 | 30 | GND |
| LED1* | 31 | 32 | PWM1.1* |
| **PWM2** | 33 | 34 | GND |
| PWM2.1* | 35 | 36 | LED2* |
| IO26* | 37 | 38 | --- |
| GND | 39 | 40 | IO21* |

</td>
</tr>
</table>

> **\*** those pins are additionally broken out on our custom Pi-Hat and you do not need to connect them if you don't want this extra functionality: LED0-2 Debugging LEDs showing current state of the streamer. IO21 & IO26 IO pins that do not have functionality yet but can be used for additional functionality. PWM2.1 and PWM1.1 Can either be used as additional GPIO or as Backup PWM pins in case the main ones get damaged for some reason. 

> Some pins might be configurable, but wiring up like this will be the easiest, most consistent and reliable way.

> ****NOTE:**** Although a Raspberry Pi Zero 2 W is depicted here, the pinout is the same for all supported Raspberry Pi's: ****Raspberry Pi Zero 2 W, Pi 3 and Pi 4****.

The only really mandatory connections are `PWM1` and `PWM2` for Servo and Speed-controller. The INA is highly recommended for Voltage monitoring.

UART0 is the only available hardware UART and can be used for one of the following:
* Serial console - great for debugging
* GPS

## Power supply

Best option to power the RPI and Modem directly through the 5V rail with a clean BEC (or DC/DC converter) capable of pushing at least 2A. Technically you could also power the setup via ESC if you can run your ESC at 5V.

> Technically the RPi should be fine to 6V input on the 5V rail, but this is out of spec and not recommended. Keep in mind that the RPi Zero 2 W has no over voltage or over current protection so a reliable BEC is really a must.

## INAxxx - current/voltage sensor

Voltage is measured via bus pin, not the main pins over the shunt - those are only used for current sensing (which is not yet implemented).

Tested options:
* INA226
* INA231
* INA219
