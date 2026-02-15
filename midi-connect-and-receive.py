import mido
import time
 
# --- 1. Connect midi device ---
# declare a MidiPort object that you use to receive and send messages
midiIODevicePort = None
searchMidiDevice = True
 
# - Choose the way you want to filter the device like using a keyboard input, ... -
# For the purose of the tutorial I choose to filter the name
nameFilter = "CASIO USB-MIDI"
timeoutDurationSec = 60
connectionTimeoutSec = time.time() + timeoutDurationSec

print(f"[Midi][ConnectionState] Start search '{nameFilter}' for {timeoutDurationSec} sec")

while searchMidiDevice:
    
    # - Timeout -
    if time.time() > connectionTimeoutSec:
        print(f"[Midi][ConnectionState] Failed - Timeout reached")
        searchMidiDevice = False
        break

    # - read connected device names -
    device_names = mido.get_input_names()
    # print(device_names)

    for device_name in device_names:
        
        if nameFilter in device_name:
            print(f"[Midi][ConnectionState] Connect with '{device_name}'")
            midiIODevicePort = mido.open_ioport(device_name)
             
            if midiIODevicePort != None:
                print(f"[Midi][ConnectionState] Complete")
                searchMidiDevice = False
            else:
                print(f"[Midi][ConnectionState] Failed to connect")
                searchMidiDevice = False

# if we don't find anything
if not midiIODevicePort:
    print(f"[Midi][ConnectionState] No device connected - Terminate program")
    exit

# --- 2. Listen to input ---
# Listen for 5 minutes
listeningDurationSec = (1 * 60)
listeningTimeoutSec = time.time() + listeningDurationSec

print(f"[Midi][ListenState] Start for {listeningDurationSec} sec")
 
# Keep loop alive as long as device is connected. See more exit rules inside.
while midiIODevicePort:

    currentTime = time.time()

    # timeout for opteration
    if currentTime > listeningTimeoutSec:
        print(f"[Midi][ListenState] Stop - Timeout reached")
        break

    # Read the incomming message buffer, while keeping the loop alive for other operations
    for msg in midiIODevicePort.iter_pending():
        # Message and time stamp
        print(f"[Midi][ListenState] message '{msg}' time '{currentTime}'")
 
 # disconnect port
if midiIODevicePort:
    print(f"[Midi][ListenState] Disconnect device '{midiIODevicePort.name}'")
    midiIODevicePort.close()

print(f"[Midi][ListenState] Complete")