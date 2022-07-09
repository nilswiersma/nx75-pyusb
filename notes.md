https://github.com/pbludov/hv-kb390l-config

https://github.com/dokutan/rgb_keyboard

https://github.com/pyusb/pyusb

https://slomkowski.eu/tutorials/eavesdropping-usb-and-writing-driver-in-python/

https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst

usbmon3, 3.4.1
filter: usb.device_address==4

usb.src=='3.4.1' || usb.dest=='3.4.1'

https://mika-s.github.io/wireshark/lua/dissector/usb/2019/07/23/creating-a-wireshark-usb-dissector-in-lua-1.html

https://eleccelerator.com/usb-descriptor-and-request-parser/

https://github.com/TeamRocketIst/ctf-usb-keyboard-parser

usb.src != "3.5.1" \&& usb.dst != "3.5.1" && usb.src != "3.2.1" && usb.dst != "3.2.1"

https://docs.microsoft.com/en-us/windows-hardware/drivers/usbcon/usb-control-transfer

https://learn.adafruit.com/hacking-the-kinect/installing-python-and-pyusb?view=all

https://github.com/JohnDMcMaster/usbrply

https://wiki.wireshark.org/CaptureSetup/USB


https://stackoverflow.com/questions/70371707/how-to-write-to-control-endpoint-with-pyusb
https://stackoverflow.com/questions/37943825/send-hid-report-with-pyusb/52368526#52368526



- each setting from the gui sends 040100010... before the setting, and 040200020... after, not sure why, doesn't seem to be neccesary
    - not sending it might keep it in some weird state, replugging fixes

- test2_pyusb.py sends a few commands using pyusb

```
bmRequestType = 0x21
bRequest = 0x09
wValue = 0x0204
wIndex = 1
wLength = 64

lights off:       04 2b 03061c00000000 01 00 010001 ffffff08000000000000000000000100 00000000000000000000000000000000000000000000000000000000000000000000
lights on:        04 2f 03061c00000000 01 04 010001 ffffff08000000000000000000000100 00000000000000000000000000000000000000000000000000000000000000000000
r-to-l:           04 30 03061c00000000 01 04 010101 ffffff08000000000000000000000100 00000000000000000000000000000000000000000000000000000000000000000000
cloud:            04 31 03061c00000000 02 04 010101 ffffff08000000000000000000000100 00000000000000000000000000000000000000000000000000000000000000000000
corrugated:       04 30 03061c00000000 01 04 010101 ffffff08000000000000000000000100 00000000000000000000000000000000000000000000000000000000000000000000
cloud r2l:        04 30 03061c00000000 02 04 010001 ffffff08000000000000000000000100 00000000000000000000000000000000000000000000000000000000000000000000
serpentine:       04 31 03061c00000000 03 04 010001 ffffff08000000000000000000000100 00000000000000000000000000000000000000000000000000000000000000000000
serpentine clock: 04 32 03061c00000000 03 04 010101 ffffff08000000000000000000000100 00000000000000000000000000000000000000000000000000000000000000000000
usb rate to 500:  04 3f 03061c00000000 0f 04 010101 ffffff08000000000000000000000100 01000000000000000000000000000000000000000000000000000000000000000000
```

- adding a wireshark dissector in lua

https://www.golinuxcloud.com/wireshark-dissector-tutorial/

https://mika-s.github.io/wireshark/lua/dissector/usb/2019/07/23/creating-a-wireshark-usb-dissector-in-lua-1.html

https://false.ekta.is/2013/11/decoding-vendor-specific-usb-protocols-with-wireshark-lua-plugins/

all talk about leftover data, but modern wireshark catches it before me in setup data or hid data...

https://wiki.wireshark.org/Lua/Examples/PostDissector

postdissector is easier?

https://wiki.wireshark.org/Lua/Dissectors

https://www.wireshark.org/docs//wsdg_html_chunked/lua_module_Field.html

https://www.wireshark.org/docs/wsdg_html_chunked/lua_module_Tvb.html

https://www.wireshark.org/docs//wsdg_html_chunked/lua_module_Proto.html#lua_class_ProtoField

wireshark -i usbmon3 -Y \(usb.bmRequestType==0x21\)\&\&\(usbhid.setup.bRequest==0x09\)\&\&\(usbhid.setup.ReportID==4\) -X lua_script:/home/nils/projects/nexttime-75-libusb/wireshark-lua/nx75-dissect.lua

# light settings:

cmd1: checksum
cmd2: color mode
- 0x01 = corrugated
- 0x02 = cloud
- 0x03 = serpentine
- 0x04 = spectrum
- 0x05 = breath
- 0x06 = normal
- 0x07 = reaction
- 0x08 = ripples
- 0x09 = traverse
- 0x0a = stars
- 0x0b = flowers
- 0x0c = roll
- 0x0d = wave
- 0x0e = cartoon
- 0x0f = rain
- 0x10 = scan
- 0x11 = surmount
- 0x12 = speed

custom:
- 0x00 (x7)
- 0x13

## brightness

argword1, byte0, 5 levels 0x00 - 0x04 (5 levels)
- 0x00 lowest, 0x04 highest

cmd1 also plays a role

## speed
argword1, byte1, 5 levels 0x00 - 0x04 (5 levels)
- 0x00 fastest, 0x04 slowest

cmd1 also plays a role

## left-to-right, right-to-left

for corrugated:

argword1, byte2, 2 levels 0x00 - 0x01 (2 levels)


cmd1 is maybe a checksum?

argword1, byte3, 0/1 for rainbow mode it seems



