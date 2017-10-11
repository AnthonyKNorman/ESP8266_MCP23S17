#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  example.py
#  Put an led and a resistor on Port A, pin 0 and this will make the led blink
import mcp_gpio
from utime import sleep

mcp_gpio.registers()				# dump the contents of the registers

a = mcp_gpio.GPIO_Pin(0)
while 1:
	a.value(1)
	sleep(.5)
	a.value(0)
	sleep(.5)
