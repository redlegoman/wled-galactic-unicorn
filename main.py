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

# Persistent buffer to hold the full frame
pixel_buffer = bytearray(TOTAL_PIXELS * 3)

# WiFi Setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("ssid", "password")
while not wlan.isconnected(): pass
print("Pico Ready at:", wlan.ifconfig()[0])

# DDP Port 4048
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 4048))
sock.setblocking(False)

print("Synchronizing frames...")

while True:
    try:
        data, addr = sock.recvfrom(1500)
        
        if len(data) > 10:
            # Header flags are in byte 0
            # DDP Push flag (bit 0) tells us to display the buffer
            flags = data[0]
            
            # Byte 4-7 is the offset (where these pixels go)
            offset = struct.unpack('>I', data[4:8])[0]
            rgb_data = data[10:]
            
            # Fill the buffer at the correct position
            pixel_buffer[offset:offset + len(rgb_data)] = rgb_data
            
            # ONLY update the display if the 'Push' flag (0x01) is set
            # This ensures we don't draw until the final packet of the frame arrives
            if flags & 0x01:
                ptr = 0
                for y in range(HEIGHT):
                    for x in range(WIDTH):
                        if ptr + 2 < len(pixel_buffer):
                            r, g, b = pixel_buffer[ptr], pixel_buffer[ptr+1], pixel_buffer[ptr+2]
                            graphics.set_pen(graphics.create_pen(r, g, b))
                            graphics.pixel(x, y)
                            ptr += 3
                gu.update(graphics)
            
    except OSError:
        pass

