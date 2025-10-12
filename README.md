# SK5-Speaker-Recreation
# In Line 9, the device address is left blank because it currnetly needs to be hardcoded. To get yours please put "busctl tree org.bluez" in the terminal while your phone is connected to the rasbperry pi and find it there.
# It will be something like: hci_/dev_##_##..../player_

# this will also change whenever you turn off and turn off the raspberry pi

# This is the following code for the SK5 Speaker Recreation. The following code controls a raspberry pi 4B with a hifiberry amp2 amplifier connected a single full range speaker to play music. It is also controls a display to show the songs meta data, small display that shows the time bar, and buttons to control playback and bluetooth connection.
