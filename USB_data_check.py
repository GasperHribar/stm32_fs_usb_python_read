
import struct
import matplotlib.pyplot as plt

# File to analyze
filename = "usb_data.bin"

error_count = 0  # To count the number of integrity errors

try:
    with open(filename, "rb") as file:
        previous_value = None
        index = 0

        while True:
            # Read 4 bytes from the file
            data = file.read(4)
            
            # If we reach the end of the file (less than 4 bytes), stop
            if len(data) < 4:
                break

            # Convert 4 bytes to uint32 using big-endian (">" means big-endian in struct)
            current_value = struct.unpack(">I", data)[0]

            # Print the current value for debugging (optional)
            #print(f"Value {index}: {current_value}")

            # Check if current value is greater than the previous value
            if previous_value is not None and current_value != previous_value + 1:
                error_count += 1  # Increment the error count

            # Update previous_value and increment index
            previous_value = current_value
            index += 1

    # ANSI escape codes for text formatting
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    if error_count:
        print(f"{RED}File integrity check completed: {error_count} error(s) found.{RESET}")
    else:
        print(f"{GREEN}File integrity check completed: {error_count} error(s) found.{RESET}")

except IOError as e:
    print(f"Failed to open or read the file: {e}")
    


# Plot the data
print("Plotting data...")

data_list = []

# Read the data from the binary file
with open(filename, "rb") as file:
    while True:
        # Read 4 bytes from the file
        data = file.read(4)
        
        # If we reach the end of the file (less than 4 bytes), stop
        if len(data) < 4:
            break
        
        # Convert 4 bytes to uint32 using big-endian (">" means big-endian in struct)
        current_value = struct.unpack(">I", data)[0]
        
        # Append the current value to the list
        data_list.append(current_value)

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data_list, marker='o', linestyle='-', color='b')
plt.title('USB Data Plot')
plt.xlabel('Sample Index')
plt.ylabel('Data Value')
plt.grid(True)
plt.show()

