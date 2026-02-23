# wled-galactic-unicorn
This script when uploaded and run (via thony) to a raspyberry pi pico attached to a pimoroni galactic unicorn turns it into a device that can accept DDP network sync from a WLED installed elsewhere (an ESP32).

```
On WLED:
Settings > 2D Configuration in WLED:

Panel Setup: Ensure Width is 53 and Height is 11.

LED Layout: Set First LED to Top Left.

Orientation: Set to Horizontal.

Serpentine: Ensure this is Unchecked (The Galactic Unicorn rows are not serpentine; they all start from the same side).
```

```
Settings > LED Preferences

Add an Output: Click the + button 

Set Type: Select DDP RGB (network) from the dropdown menu.

Destination IP: Enter the Pico's IP

Length: Set this to 583 (the 53x11 pixels of the Unicorn).

Save: Scroll to the bottom and click Save.
```
