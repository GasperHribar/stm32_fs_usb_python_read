import usb.core
import usb.util
import usb.backend.libusb1
import time
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the DLL file in the same directory as the script
dll_path = os.path.join(script_dir, "libusb-1.0.dll")

# Initialize the backend and find the device (you need USB library libusb-1.0.dll)
backend = usb.backend.libusb1.get_backend(find_library=lambda x: dll_path)
stm32IdVendor = 0x0483 #specific for STM32
stm32idProduct = 0x572A #specific for STM32

dev = usb.core.find(idVendor = stm32IdVendor, idProduct = stm32idProduct, backend=backend)

if dev is None:
    raise ValueError("STM32 USB Device not found!")
else:
    print("STM32 USB Device found!")

# Set the active configuration
dev.set_configuration()

# Get the endpoint
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

# Debugging information
print("Device configuration:")
print(cfg)
print("Interfaces and Endpoints:")
for i in range(cfg.bNumInterfaces):
    interface = cfg[(i, 0)]
    print(f"Interface {interface.bInterfaceNumber}:")
    for endpoint in interface:
        print(f"  Endpoint address: 0x{endpoint.bEndpointAddress:02X}")

#Bulk IN endpoint address (same as on MCU)
bulkInEpAddress = 0x81

# Find the IN endpoint (assuming "bulkInEpAddress")
ep = usb.util.find_descriptor(
    intf,
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN and e.bEndpointAddress == bulkInEpAddress
)

assert ep is not None, "IN Endpoint not found!"

# File to store the data
filename = "usb_data.bin"

startTime = 0
endTime = 0
dataSize = 0

try:
    # Open the file before starting the loop
    with open(filename, "wb") as file:
        while True:
            try:
                # Read data from the bulk endpoint
                data = dev.read(ep.bEndpointAddress, size_or_buffer= 102400, timeout=5000)
                if data:
                    file.write(data) # Write data to the file immediately
                    dataSize += len(data)
                    if startTime == 0:
                        startTime = time.time()
                    if endTime < time.time():
                        endTime = time.time()
                    
            except usb.core.USBError as e:
                    # Handle timeout error
                    if e.errno == 10060:                        
                        if dataSize > 0:
                           print("All data received")
                           print(f"Transfered data size: {dataSize}")
                           transferTime = endTime - startTime
                           print(f"Transfer duration: {transferTime:.2f}")
                           transferSpeed = dataSize / transferTime
                           print(f"Transfer speed: {transferSpeed:.2f} Bytes/s")
                           break 
                        else:
                            print("USB reading Timeout occurred, retrying...")
                    else:
                        # For other USB errors, print and break the loop
                        print(f"USB Error: {e}")
                        break
except KeyboardInterrupt:
    print("Interrupted by user")

except Exception as e:
    print(f"Error: {e}")

