#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mcp_gpio.py
#  
import MCP23S17
from machine import SPI

# this dumps out the contents of all the registers for debugging
def registers():
	for i in range(0x16):
		print('{:02x}\t{:08b}'.format(i, mcp.read(i)))

spi = SPI(1, baudrate=10000000, polarity=0, phase=0)	# set up hardware SPI
mcp = MCP23S17.MCP23S17(spi)							# default rst=4, cs=5, address=0

class GPIO_Pin():
	""" 
		example use
		a = GPIO_Pin(5)			# a is Pin 5
		a.value(1)				# write 1 to pin 5
		b = GPIO_Pin(6)			# b is pin 6
		b.value()				# read Pin 6
	"""
	def __init__(self, pin):
		self._pin = pin
	
	# pass no parameter to read the pin. Pass 0 or 1 to write the state
	def value(self, val=None):
		if val==None:		# read
			return mcp.gpio_read(self._pin)
		else:				# write
			mcp.gpio_write(self._pin, val)
