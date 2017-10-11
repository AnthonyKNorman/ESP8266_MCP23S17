# ESP8266_MCP23S17
Micropython library for using the MCP23S17 16-bit IO expander with the ESP8266

MCP23S17.py - Fundamentals for driving the MCP23S17

mcp_gpio.py - Extraction to provide simple bit-based io read and write
```python
import mcp_gpio
a = mcp_gpio.GPIO_Pin(5)      # a is Pin 5
a.value(1)                    # write 1 to pin 5
b = mcp_gpio.GPIO_Pin(6)      # b is pin 6
c = b.value()                 # read pin 6 into c
```

example.py - Example using mcp_gpio.py

