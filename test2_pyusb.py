import sys
import time
import array
import ctypes as ct

import usb.core as uc
import usb.util as uu

# import os
# os.environ['LIBUSB_DEBUG'] = '4'

VENDOR_ID = 0x320f
PRODUCT_ID = 0x5055

# print(uc.show_devices())

devh = uc.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

print(devh)

for cfg in devh:
  for intf in cfg:
    if devh.is_kernel_driver_active(intf.bInterfaceNumber):
      try:
        devh.detach_kernel_driver(intf.bInterfaceNumber)
      except uc.USBError as e:
        sys.exit("Could not detach kernel driver from interface({0}): {1}".format(intf.bInterfaceNumber, str(e)))
    print(f'Detached kernel driver for interface {intf.bInterfaceNumber}')


devh.set_configuration()

cfg = devh.get_active_configuration()
# print()
# print(cfg)

print(f'{devh.bus}.{devh.address}')

# bmRequestType = 0x21
# bRequest = 0x0a # SET_IDLE
# wValue = 0x0000
# wIndex = 0
# wLength = 0
# data = array.array('B', [0x41]*0)
# # bmRequestType = uu.build_request_type(
# #     direction=uu.CTRL_OUT,
# #     type=uu.CTRL_TYPE_CLASS,
# #     recipient=uu.CTRL_RECIPIENT_INTERFACE)
# print(hex(bmRequestType))
# ret = devh.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data)
# print(ret, data)



# load? change state? via .0
bmRequestType = 0x21
bRequest = 0x09
wValue = 0x0204
wIndex = 1
wLength = 64
if False:
    
  Data_Fragment = bytes.fromhex('04010001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
  ret = devh.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, Data_Fragment)
  # time.sleep(1)
  print(ret)

  # get a reply from .2 (inverted order in wireshark, hope it doesnt matter)
  resp1 = devh.read(0x82, 0x40, timeout=1000)
  # time.sleep(1)
  print(resp1.tobytes().hex())
  # TODO: Data_Fragment =?= resp

  # send the setting? (right to left)
  Data_Fragment = bytes.fromhex('042f03061c000000000104010001ffffff0800000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000')

  ret = devh.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, Data_Fragment)
  # time.sleep(1)
  print(ret)

  # get a reply from .2 (inverted order in wireshark, hope it doesnt matter)
  resp2 = devh.read(0x82, 0x40, timeout=1000)
  # time.sleep(1)
  print(resp2.tobytes().hex())
  # TODO: Data_Fragment =?= resp


  # apply and save setting?
  Data_Fragment = bytes.fromhex('04020002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

  ret = devh.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, Data_Fragment)
  # time.sleep(1)
  print(ret)

  # get a reply from .2 (inverted order in wireshark, hope it doesnt matter)
  resp3 = devh.read(0x82, 0x40, timeout=1000)
  # time.sleep(1)
  print(resp3.tobytes().hex())
  # TODO: Data_Fragment =?= resp





  time.sleep(5)






  # load? change state? via .0
  bmRequestType = 0x21
  bRequest = 0x09
  wValue = 0x0204
  wIndex = 1
  wLength = 64
  Data_Fragment = bytes.fromhex('04010001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
  ret = devh.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, Data_Fragment)
  # time.sleep(1)
  print(ret)

  # get a reply from .2 (inverted order in wireshark, hope it doesnt matter)
  resp1 = devh.read(0x82, 0x40, timeout=1000)
  # time.sleep(1)
  print(resp1.tobytes().hex())
  # TODO: Data_Fragment =?= resp

  # send the setting? (left to right)
  Data_Fragment = bytes.fromhex('042f03061c000000000104010001ffffff0800000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000')

  ret = devh.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, Data_Fragment)
  # time.sleep(1)
  print(ret)

  # get a reply from .2 (inverted order in wireshark, hope it doesnt matter)
  resp2 = devh.read(0x82, 0x40, timeout=1000)
  # time.sleep(1)
  print(resp2.tobytes().hex())
  # TODO: Data_Fragment =?= resp


  # apply and save setting?
  Data_Fragment = bytes.fromhex('04020002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

  ret = devh.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, Data_Fragment)
  # time.sleep(1)
  print(ret)

  # get a reply from .2 (inverted order in wireshark, hope it doesnt matter)
  resp3 = devh.read(0x82, 0x40, timeout=1000)
  # time.sleep(1)
  print(resp3.tobytes().hex())
  # TODO: Data_Fragment =?= resp

if True:
  bmRequestType = 0x21
  bRequest = 0x09
  wValue = 0x0204
  wIndex = 1
  wLength = 64

  print("light off?")
  Data_Fragment = bytes.fromhex('042b03061c000000000100010001ffffff0800000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000')
  ret = devh.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, Data_Fragment)
  print(ret)
  
  resp2 = devh.read(0x82, 0x40, timeout=1000) # get a reply from .2 (inverted order in wireshark, hope it doesnt matter)
  print(resp2.tobytes().hex(), Data_Fragment == resp2.tobytes())

  # time.sleep(5)

  print('lights on?')
  Data_Fragment = bytes.fromhex('042f03061c000000000104010001ffffff0800000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000')
  ret = devh.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, Data_Fragment)
  print(ret)
  resp2 = devh.read(0x82, 0x40, timeout=1000)
  print(resp2.tobytes().hex(), Data_Fragment == resp2.tobytes())

  # time.sleep(5)

  print('left to right?')
  Data_Fragment = bytes.fromhex('042f03061c000000000104010001ffffff0800000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000')
  ret = devh.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, Data_Fragment)
  print(ret)
  resp2 = devh.read(0x82, 0x40, timeout=1000)
  print(resp2.tobytes().hex(), Data_Fragment == resp2.tobytes())

  # time.sleep(5)

  print('right to left?')
  Data_Fragment = bytes.fromhex('043003061c000000000104010101ffffff0800000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000')
  ret = devh.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, Data_Fragment)
  print(ret)
  resp2 = devh.read(0x82, 0x40, timeout=1000)
  print(resp2.tobytes().hex(), Data_Fragment == resp2.tobytes())



  



for cfg in devh:
  for intf in cfg:
    try:
      devh.attach_kernel_driver(intf.bInterfaceNumber)
    except uc.USBError as e:
      sys.exit("Could not reattach kernel driver from interface({0}): {1}".format(intf.bInterfaceNumber, str(e)))
    print(f'Reattached kernel driver for interface {intf.bInterfaceNumber}')
