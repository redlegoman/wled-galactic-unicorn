import network
import socket
import struct
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN

# Hardware Setup
gu = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY_GALACTIC_UNICORN)
WIDTH, HEIGHT = 53, 11
TOTAL_PIXELS = WIDTH * HEIGHT

# 1. PRE-CALCULATE GAMMA TABLE (Gamma 2.8)
# This maps 0-255 input to a 'corrected' 0-255 output
#GAMMA_LUT = bytearray([int(pow(i / 255, 2.8) * 255) for i in range(256)])
GAMMA_LUT = bytearray([int(pow(i / 255, 0.5) * 255) for i in range(256)])

# Persistent buffer
pixel_buffer = bytearray(TOTAL_PIXELS * 3)

# WiFi Setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("ssid", "password")
while not wlan.isconnected(): pass
print("Gamma Corrected DDP Ready!")

# DDP Port 4048
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 4048))
sock.setblocking(False)

while True:
    try:
        data, addr = sock.recvfrom(1500)
        
        if len(data) > 10:
            flags = data[0]
            offset = struct.unpack('>I', data[4:8])[0]
            rgb_data = data[10:]
            
            # Map data into the buffer
            pixel_buffer[offset:offset + len(rgb_data)] = rgb_data
            
            if flags & 0x01:
                ptr = 0
                for y in range(HEIGHT):
                    for x in range(WIDTH):
                        if ptr + 2 < len(pixel_buffer):
                            # We use .get() style logic or direct indexing
                            # Let's ensure these are explicitly integers
                            r = GAMMA_LUT[int(pixel_buffer[ptr])]
                            g = GAMMA_LUT[int(pixel_buffer[ptr+1])]
                            b = GAMMA_LUT[int(pixel_buffer[ptr+2])]
                            
                            graphics.set_pen(graphics.create_pen(r, g, b))
                            graphics.pixel(x, y)
                            ptr += 3
                gu.update(graphics)
                
    except OSError:
        pass

