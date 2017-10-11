#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MCP23S17.py
#  
from machine import Pin, SPI
import time
# IOCON.BANK = 0 - default at reset
IODIRA		= const(0x00)
IODIRB		= const(0x01)
IPOLA		= const(0x02)
IPOLB		= const(0x03)
GPINTENA	= const(0x04)
GPINTENB	= const(0x05)
DEFVALA		= const(0x06)
DEFVALB		= const(0x07)
INTCONA		= const(0x08)
INTCONB		= const(0x09)
IOCONA		= const(0x0a)
IOCONB		= const(0x0b)
GPPUA		= const(0x0c)
GPPUB		= const(0x0d)
INTFA		= const(0x0e)
INTFB		= const(0x0f)
INTCAPA		= const(0x10)
INTCAPB		= const(0x11)
GPIOA		= const(0x12)
GPIOB		= const(0x13)
OLATA		= const(0x14)
OLATB		= const(0x15)

# masks
BANK		= 7	# changes how registers are mapped
MIRROR		= 6	# controls how the INTA and INTB pins function
SEQOP		= 5	# Sequential Operation
DISSLW		= 4	# Slew Rate
HAEN		= 3	# hardware address enable
ODR			= 2	# enables/disables the INT pin for open-drain configuration
INTPOL		= 1	# Interrupt Polarity

class MCP23S17():
	def __init__(self, spi, rst=4, cs=5, address=0):
		self._rst = Pin(rst, Pin.OUT)   # set up the rst pin
		self._rst.value(1)				# initialise the reset pin
		self._cs = Pin(cs, Pin.OUT)    	# set up the chip select pin
		self._cs.value(1)				# initialise the chip select pin
		self._addr = address

		# SPI
		self._spi = spi
		
		self.reset()
		self.write(IOCONA, 1 << HAEN)	# enable hardware address select from A0,A1,A2

	# write to register
	def write(self,c, d):
		b = bytearray(3)				# buffer to write data
		b[0] = 0x40 | self._addr << 1	# r/w bit clear. Address defined by pins A2, A1, A0
		b[1] = c						# c is register
		b[2] = d						# d is data
		self._cs.value(0)				# set CS low
		self._spi.write(b)				# write buffer on MOSI
		self._cs.value(1)				# set CS high
		
	# read from register
	def read(self,c):
		b = bytearray(1)				# buffer to write register and read data
		b[0] = 0x41 | self._addr << 1	# r/w bit set. Address defined by pins A2, A1, A0
		self._cs.value(0)				# lower chip select
		self._spi.write(b)				# tells mcp you want to read
		b[0] = c						# c is reg num
		self._spi.write(b)				# write the reg num
		self._spi.readinto(b)			# read data
		self._cs.value(1)				# raise chip select
		return b[0]						# return value read

	def reset(self):
		self._rst.value(0)				# set reset low (active)
		time.sleep_ms(50)				# sleep for 50 milliseconds
		self._rst.value(1)				# set reset high
		time.sleep_ms(50)				# sleep for 50 milliseconds

	def gpio_write(self, b, d):			# set bit b to state d
		ddr = IODIRA					# ddr register A
		gpio = GPIOA					# gpio register A
		if b > 7:						# pin is in the second bank
			b -= 8						# b is pin number in second bank
			ddr = IODIRB				# ddr register B
			gpio = GPIOB				# gpio register B
		
		mask = 1 << b					# shift '1' to bit position
		reg = self.read(ddr)			# read the data direction register
		reg &= ~mask & 0xff				# clear the relevant bit to enable 'write'
		self.write(ddr, reg)			# write it back
	
		reg = self.read(gpio)			# read the gpio
		if d:							# if we are writing a 1
			reg |= mask					# set the bit
		else:							# if we are writing a zero
			reg &= ~mask & 0xff			# clear the bit
		self.write(gpio, reg)			# write it back
	
	def gpio_read(self, b):				# read bit b state
		ddr = IODIRA					# ddr register A
		gpio = GPIOA					# gpio register A
		if b > 7:						# pin is in the second bank
			b -= 8						# b is pin number in second bank
			ddr = IODIRB				# ddr register B
			gpio = GPIOB				# gpio register B
		
		mask = 1 << b					# shift '1' to bit position
		reg = self.read(ddr)			# read the data direction register
		reg |= mask						# set the relevant bit
		self.write(ddr, reg)			# write it back
	
		reg = self.read(gpio)			# read the gpio
		reg &= mask
		if reg:							# if bit is set
			return 1					# return a '1'
		else:							# if bit is clear
			return 0					# return a '0'
	
			

		
