# RPi-DHT20
Raspberry Pi Python library for DHT20 Temperature and Humidity Sensor with CRC verification.

## Requirements
This library was tested with the following:
- Aosong DHT20 SIP Packaged Temperature and Humidity Sensor
- Raspberry Pi 3 Model B
- Ubuntu Server 22.10, 23.04 and 23.10

Similar configurations should also work.

## Set up
1. Connect the DHT20 sensor to the Raspberry Pi\
*Note: If a different Raspberry Pi model and/or operating system is used, it may be necessary to change the `I2C_BUS` in `DHT20_demo.py` and/or enable the I<sup>2</sup>C interface.*

2. Install smbus2 Python module that is used for accessing the I<sup>2</sup>C bus
   ```
   sudo apt install python3-smbus2
   ```
3. If `/dev/i2c*` does not exist, enable the i2c-dev kernel module by adding the following line to the `/etc/modules` file
   ```
   i2c-dev
   ```
4. Test by running the demo
   ```
   sudo python3 DHT20_demo.py
   ```

## Usage
Refer to the usage example in `DHT20_demo.py`.

## References
- [Aosong DHT20 datasheet](http://www.aosong.com/userfiles/files/media/Data%20Sheet%20DHT20%20%20A1.pdf)
- [Aosong AHT20 sample program](http://aosong.com/userfiles/files/software/AHT20-21%20DEMO%20V1_3(1).rar)
- [DFRobot_DHT20 Raspberry Pi library](https://github.com/DFRobot/DFRobot_DHT20/tree/master/python/raspberrypi)
