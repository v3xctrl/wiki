Connect your peripherals according to the following pinout:
<table>
<tr>
<td width="400px">
<img alt="zero2-close-up webp" src="https://github.com/user-attachments/assets/b12df9a9-5fe8-4d1a-a2a3-672e65cdd50f" />
</td>
<td>

<table>
<tr><th>Func.</th><th>Pin</th><th>Pin</th><th>Func.</th></tr>
<tr><td>3.3V</td><td>1</td><td>2</td><td>5V</td></tr>
<tr><td>SDA (I2C)</td><td>3</td><td>4</td><td><b>5V</b></td></tr>
<tr><td>SCL (I2C)</td><td>5</td><td>6</td><td><b>GND</b></td></tr>
<tr><td>---</td><td>7</td><td>8</td><td>TX (UART0)</td></tr>
<tr><td>---</td><td>9</td><td>10</td><td>RX (UART0)</td></tr>
<tr><td>---</td><td>11</td><td>12</td><td><b>PWM1</b></td></tr>
<tr><td>---</td><td>13</td><td>14</td><td>GND</td></tr>
<tr><td>---</td><td>15</td><td>16</td><td>---</td></tr>
<tr><td>---</td><td>17</td><td>18</td><td>---</td></tr>
<tr><td>---</td><td>19</td><td>20</td><td>GND</td></tr>
<tr><td>---</td><td>21</td><td>22</td><td>---</td></tr>
<tr><td>---</td><td>23</td><td>24</td><td>---</td></tr>
<tr><td>GND</td><td>25</td><td>26</td><td>---</td></tr>
<tr><td>---</td><td>27</td><td>28</td><td>---</td></tr>
<tr><td>LED0*</td><td>29</td><td>30</td><td>GND</td></tr>
<tr><td>LED1*</td><td>31</td><td>32</td><td>PWM1.1*</td></tr>
<tr><td><b>PWM2</b></td><td>33</td><td>34</td><td>GND</td></tr>
<tr><td>PWM2.1*</td><td>35</td><td>36</td><td>LED2*</td></tr>
<tr><td>IO26*</td><td>37</td><td>38</td><td>---</td></tr>
<tr><td>GND</td><td>39</td><td>40</td><td>IO21*</td></tr>
</table>

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
