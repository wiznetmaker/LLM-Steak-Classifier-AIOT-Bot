import board
import busio
import digitalio
import time
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

# WIZnet W5100S-EVB-Pico
SPI0_SCK = board.GP18
SPI0_TX = board.GP19
SPI0_RX = board.GP16
SPI0_CSn = board.GP17
W5x00_RSTn = board.GP15

cs = digitalio.DigitalInOut(SPI0_CSn)
spi = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)
eth = WIZNET5K(spi, cs, is_dhcp=True, debug=False)

ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
ethernetRst.direction = digitalio.Direction.OUTPUT
ethernetRst.value = False
time.sleep(1)
ethernetRst.value = True

# Initialize one-wire bus on board pin GP0.
ow_bus = OneWireBus(board.GP0)

# Scan for sensors and grab the first one found.
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

# edit host and port to match server
HOST = "192.168.11.146"
PORT = 50007
TIMEOUT = 5
INTERVAL = 3
MAXBUF = 256

# Main loop to print the temperature every second.
while True:
    print("Create TCP Client Socket")
    socket.set_interface(eth)
    s = socket.socket()
    s.settimeout(TIMEOUT)

    print("Connecting")
    s.connect((HOST, PORT))

    size = s.send("{0:0.1f}".format(ds18.temperature))
    print("Sent", size, "bytes")

    time.sleep(INTERVAL)
    break
