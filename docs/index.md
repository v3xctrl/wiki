This guide is meant to get you up and running as quick as possible. It is structured in such a way that you can set things up step by step, validating correct functionality in each step.

## 1. RPi Setup

Prerequisites:

* A Raspberry Pi Zero 2 W - without soldered pins
* A good quality SD card - preferably 32GB, Class 10, U3
* Power supply to power the Raspberry Pi

Follow the [Streamer installation guide](Streamer.md), if you can connect to the web interface: `http://v3xctrl.local` you are ready for the next step.

## 2. Viewer Setup
The Viewer is where the video feed will be displayed and your inputs connect to, basically the UI you will use to control your streamer.

Download, extract and run the GUI for your operating system from the [releases section](https://github.com/stylesuxx/v3xctrl/releases/latest).

On the machine running the viewer, make sure the following ports are open (you might need to forward them through your router):

* 16384: UDP for receiving video (UDP & TCP for running self-tests)
* 16386: UDP for receiving UDP messages

Take note of the **internal IP address** of the machine you are running the viewer on. It has to be in the same network that you set your streamer up to connect with in [step 1](#1-rpi-setup).

## 3. Initial configuration
While keeping the viewer running, open the streamers web interface: `http://v3xctrl.local`. In the server section make sure "_Connectino Mode_" is set to "_direct_". In the Host fiels, set the internal IP address of your viewer machine which you have established in [step 2](#step-2). Scroll to the bottom and click "_Save_".

Now switch to the "_Services_" tab, find the `v3xctrl-control` service and click the "_Start_" button.

In the viewer you should now see the "Latency" and "Data" field changing, further, the "No control signal" message should have disappeared.

On the viewer open the menu by pressing ++esc++, switch to the "_Steramer_" tab and click the "_Start Video_" button, click "_Back_" on the bottom right and after a couple of seconds you should see a Test image in the viewer.

> Congratulations - you have established your first connection!

In the web interface you can now set the control service to autostart on boot. Click the "_Config Editor_" tab, scroll down to "_Autostart_" and check "_control_". Scroll to the bottom and click "_Save_"

## 4. Camera configuration

Prerequisites:

* A Raspberry Pi Zero 2W compatible camera 
* Some cameras may need additional setup. You can check out the [Hardware](Hardware.md#cameras) section of the wiki for instructions.

Shut down your streamer via web-interface and attach your Raspberry Pi Zero 2W compatible camera. Double check the polarity of the CIFS connector. Once attached, power it up and wait for the web-interface to be available. 

With the viewer running, you will have an indication once the control service autostarts and connects to the viewer. Now open the web-interface, scroll down to the "_Video_" section and expand it. Scroll down to the "_Test image_" checkbox and uncheck it. Scroll to the bottom and click "Save".

On the viewer, open the menu by pressing ++esc++, switch to the "_Streamer_" tab and dlick the "Start Video" button, click "_Back_" on the bottom right and after a couple of seconds you should see the camera image in the viewer.

## 5. Peripherals
Following the [pinout guide](Pinout.md), connect your hardware. You can attach everything at once, or do it step by step for easier debugging. Attaching things step by step will make your life easier since you will only ever have one thing to debug before progressing to the next step, being confident that what you just set up is actually working.

### 5.a Servo and ESC

Prerequisites:

* ESC
* Servo

ESC should be connected to `GND` and `PWM1`, Servo should be connected to `GND` and `PWM2`.

> Before powering up the streamer, make sure that your vehicle is in a safe position. Depending on your ESC, your motor might start to spin if calibration is not yet done.

Make sure ESC has power and the servo is being powered from the ESC too. Start the streamer.

Once connected to the viewer, use ++w++, ++s++, ++a++, ++d++ buttons to test that ESC and Servo are reacting to inputs.

#### Servo
If the servo is moving in the wrong direction, go to the "_Controls_" section, expand it, scroll down to "_Steering_" and check the "_invert Steering_" checkbox.

> You can go through the full [Calibration](Calibration.md) step now, or leave it for after you are done with the base configuration.

### 5.b Power supply

Prerequisites:

* 5V power supply, preferably a high quality 5V buck converter powered from a Lipo battery

Before connecting the 5V power supply, make sure the Raspberry Pi is no longer powered via power brick. Connect the 5V power supply to `5V` and `GND`. Double check polarization. Make sure the streamer will boot from your power source.

### 5.c Voltage sensor

Prerequisites:

* INA231 or INA226

Voltage sensor is not mandatory, but highly recommended if you want to get the most out of your batteries. Connect the INA of your chosing to `3.3V`, `GND`, `SDA` and `SCL`. Finally connect the `VBUS` pin of your INA to the battery positive plug.

> The INA by default uses the I2C address of 0x40 and will be automatically picked up on boot if attached.

Attach your power source, wait for the streamer to boot up and verify with the viewer that voltage telemetry is being transmitted.

## 6. Modem Setup
Now that everything has been tested on the local network, the last step is to add the modem. Follow the steps in the [SIM card documentation](SIM.md) to prepare your SIM card. Insert the SIM card into your modem and attach the modem to the streamer.

Boot up the streamer, use the web-interface `http://v3xctrl.local` and go to the "_Modem_" tab.

> For the "_Modem_" tab to show details, you have to make sure that the control service is not running, you can stop it from the "_Services_" tab

Confirm the following details:

* "SIM Status" shows OK
* "Carrier" is not null
* "Context 1" is set to IP xxx.xxx.xxx.xxx (yyy)

If those above points are true, then you are ready to stream over your mobile network.

Go to the "_Config Editor_" tab, in the Server section enter the **external IP address** of your viewer (you can use [whatismyipaddress.com](https://whatismyipaddress.com/) to find it, if you don't know it), scroll down to "_Network_", expand scroll to "_routing_" and select "_RNDIS_". Further down in the Modem section, select the "_Model_" of your modem. Scroll to the bottom and click "_Save_".

> After changing routing type you will have to restart the streamer.

You know everything is working if you can see the OSD change in the viewer. You should now be able to see Latency and Modem details in the upper right corner.

> To make absolutely sure the modem is being used to transmit data you can connect to the streamer via `ssh` and use `nload` to verify the network device being used. If you see traffic on `eth0`, that is the modem.

## 7. Next steps
Congratulations, now that the base setup is completed, there is a couple things you can do next:

* [Calibration](Calibration.md)
* [Controller Setup](Controller-Setup.md)
* Tune image settings