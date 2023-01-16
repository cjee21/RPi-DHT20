# Originally from https://github.com/DFRobot/DFRobot_DHT20/tree/master/python/raspberrypi
# Modified by https://github.com/cjee21/ on 16 January 2023

from time import strftime, sleep

from DFRobot_DHT20 import DFRobot_DHT20

# The first  parameter is to select i2c0 or i2c1
# The second parameter is the i2c device address
I2C_BUS     = 0x01  # default use I2C1 bus
I2C_ADDRESS = 0x38  # default I2C device address

dht20 = DFRobot_DHT20(I2C_BUS ,I2C_ADDRESS)

# Initialize sensor
if not dht20.begin():
  print("DHT20 sensor initialization failed")
else:
  while True:
    # Read ambient temperature and relative humidity and print them to terminal
    print(strftime("%Y-%m-%d %H:%M:%S %Z"))
    T_celcius, humidity, crc_error = dht20.get_temperature_and_humidity()
    if crc_error:
      print("CRC               : Error\n")
    else:
      T_fahrenheit = T_celcius*9/5 + 32
      print("Temperature       : %f\u00b0C / %f\u00b0F" %(T_celcius, T_fahrenheit))
      print("Relative Humidity : %f %%" %humidity)
      print("CRC               : OK\n")
      sleep(5)
