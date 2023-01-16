# -*- coding: utf-8 -*

# Originally from https://github.com/DFRobot/DFRobot_DHT20/tree/master/python/raspberrypi
#
# Modified by https://github.com/cjee21/
# MIT License
# Copyright (c) 2022-2023 cjee21
# 
#
# Modifications:
#
# 25 February 2022
# - use smbus2
# - add decimal to temperature formula
# - add get_temperature_and_humidity function for getting temperature and humidity in a single read
#
# 16 January 2023
# - correct sensor initialization check and clean up init (begin) function
# - improve get_temperature_and_humidity function
# - add CRC-8 checking
# - remove functions no longer needed
# - add debug logging
# Note: Sensor initialization and CRC-8 calculation is based on Aosong sample code from
#       http://aosong.com/userfiles/files/software/AHT20-21%20DEMO%20V1_3(1).rar

"""
  *@file DFRobot_DHT20.py
  *@brief Define the basic structure of class DFRobot_DHT20
  *@copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  *@licence     The MIT License (MIT)
  *@author [fengli](li.feng@dfrobot.com)
  *@version  V1.0
  *@date  2021-6-25
  *@get from https://www.dfrobot.com
  *@https://github.com/DFRobot/DFRobot_DHT20
"""

import time
import smbus2 as smbus
import logging

# debug logging
logging.basicConfig()
logger = logging.getLogger(__name__)
# uncomment line below this to enable debug logging
#logger.setLevel(logging.DEBUG)
                
class DFRobot_DHT20(object):
  ''' Conversion data '''

  _addr      =  0x50

  def __init__(self,bus,address):
    self.i2cbus = smbus.SMBus(bus)
    self._addr = address
    self.idle =    0


  # Sensor initialization function
  # @return Return True if initialization succeeds, otherwise return False.
  def begin(self):

    # after power-on, wait no less than 100ms
    time.sleep(0.5)

    # check and return initialization status
    data = self.read_reg(0x71,1)
    if (data[0] & 0x18) != 0x18:
      return False
    else:
      return True


  # Get both temperature and humidity in a single read
  # @return Return temperature (C), humidity (%) and CRC result (True if error else False) as tuple
  def get_temperature_and_humidity(self):

    # trigger measurement
    self.write_reg(0xac,[0x33,0x00])

    # wait 80 ms and keep waiting until the measurement is completed
    while True:
      time.sleep(0.08)
      data = self.read_reg(0x71,1)
      if (data[0] & 0x80) == 0:
        break

    # read sensor data
    data = self.read_reg(0x71,7)

    # extract and convert temperature and humidity from data
    temperature_rawData = ((data[3]&0xf) << 16) + (data[4] << 8) + data[5]
    humidity_rawData = ((data[3]&0xf0) >> 4) + (data[1] << 12) + (data[2] << 4)
    temperature = float(temperature_rawData) / 5242.88 - 50
    humidity = float(humidity_rawData) / 0x100000 * 100

    # check CRC
    crc_error = self.calc_CRC8(data) != data[6]

    # debug logging
    if logger.isEnabledFor(logging.DEBUG):
      logger.debug("Raw data      : 0x" + ''.join(format(x, '02x') for x in data))
      logger.debug("Read CRC      : " + hex(data[6]))
      logger.debug("Calculated CRC: " + hex(self.calc_CRC8(data)))
      logger.debug("Temperature   : %f\u00b0C", temperature)
      logger.debug("Humidity      : %f %%", humidity)

    # return results
    return (temperature, humidity, crc_error)


  # CRC function
  # @param message - data from sensor which its CRC-8 is to be calculated
  # @return Return calculated CRC-8
  def calc_CRC8(self,data):

    crc = 0xFF

    for i in data[:-1]:
      crc ^= i
      for _ in range(8):
        if crc & 0x80:
          crc = (crc << 1)^0x31
        else:
          crc = crc << 1
    
    return (crc & 0xFF)

  
  def write_reg(self,reg,data):
    time.sleep(0.01)
    self.i2cbus.write_i2c_block_data(self._addr,reg,data)
  
  
  def read_reg(self,reg,len):
    time.sleep(0.01)
    rslt = self.i2cbus.read_i2c_block_data(self._addr,reg,len)
    #print(rslt)
    return rslt
