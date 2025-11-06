import pygame
from pydbus import SystemBus
import time
from gi.repository import GLib
from gpiozero import Button, Factory
import subprocess
import re
from gpiozero import RotaryEncoder


pygame.init()
last_time_update = time.time()

## Create Dbus and Bluez Connection to Phone
bus = SystemBus()
Service = 'org.bluez'
InterfaceData = 'org.freedesktop.DBus.Properties'

#finding the bluetooth device address
ObjPath2 = '/org/bluez/hci0'
InterfaceDiscover = 'org.bluez.Adapter1' 
Adapter = bus.get(Service , ObjPath2)
Adapter.StartDiscovery()
time.sleep(2)


# Get the ObjectManager to retrieve all Bluetooth objects
manager_obj = bus.get(Service, '/')
manager = manager_obj['org.freedesktop.DBus.ObjectManager']
everything = manager.GetManagedObjects()


#Disabling Pin Verification
#InterfaceAgent = 'org.bluez.AgentManager1'
#ObjPath3 = '/org/bluez'
#Agent_obj = bus.get (Service, ObjPath3)
#Agent = Agent_obj[InterfaceAgent]
#Pin_Unverification = Agent.RegisterAgent('/org/bluez/agent', 'NoInputNoOutput')
#Agent.RequestDefaultAgent('/org/bluez/agent')


device_addresses = None

for path, interfaces in everything.items():
    if 'org.bluez.Device1' in interfaces:
        device_props = interfaces['org.bluez.Device1']
        Name = device_props.get('Name')
        Address = device_props.get('Address')
        connected = device_props.get('Connected')
        if connected:
            device_addresses = path



X_Start = 0
Y_Start = 0
Screen_Width = 800
Screen_Height = 480
Screen = pygame.display.set_mode((Screen_Width, Screen_Height), pygame.FULLSCREEN)
No_Bluetooth_Connection = pygame.Rect((X_Start, Y_Start, Screen_Width, Screen_Height))
Font_Size = 45
text_font = pygame.font.SysFont("akzidenz-garotesk", Font_Size)
text_col = (0,0,0)
Y_Bluetooth_Text = Screen_Height / 3 
Bluetooth_Text = "Bluetooth Connection Open"
Bluetooth_Time = 10
Y_Bluetooth_Time = Y_Bluetooth_Text + 100
button_bluetooth = Button(24, bounce_time=.1)
button_previous = Button(22, bounce_time=.1)
button_pauseplay = Button(27, bounce_time=.1)
button_Next = Button(23, bounce_time=.1)
rotor = RotaryEncoder(16, 26, bounce_time=0.01)
Bluetooth_Start = pygame.USEREVENT + 1
def bluetooth():
    global InterfaceData, Adapter, InterfaceDiscover, is_discoverable, Discoverability, bluetooth_popup
    
    try:
        print("Bluetooth Button is Pressed")
        InterfaceAgent = 'org.bluez.AgentManager1'
        ObjPath3 = '/org/bluez'
        Agent_obj = bus.get (Service, ObjPath3)
        Agent = Agent_obj[InterfaceAgent]
        Pin_Unverification = Agent.RegisterAgent('/org/bluez/agent', 'NoInputNoOutput')
        Agent.RequestDefaultAgent('/org/bluez/agent')
    except Exception as e:
        print('Discoverability is on Please Wait')
    
    is_discoverable = True
    Discoverability = Adapter[InterfaceData]
    Discoverability.Set(InterfaceDiscover, 'Discoverable', GLib.Variant('b',is_discoverable))  
    bluetooth_popup = True
    pygame.time.set_timer(Bluetooth_Start, 10000)

    for path, interfaces in everything.items():
        if 'org.bluez.Device1' in interfaces:
            device_props = interfaces['org.bluez.Device1']
            Name = device_props.get('Name')
            connected = device_props.get('Connected')

def Centered_draw_text(text, font, text_col, y):
    img = font.render(text, True, text_col)
    Centered_Text = img.get_rect(center = (Screen_Width/2, y))
    Screen.blit(img, Centered_Text)

bluetooth_popup = False

button_bluetooth.when_pressed = bluetooth
Bluetooth_Window = pygame.Rect((X_Start, Y_Start, Screen_Width, Screen_Height))
Bluetooth_Timer = str(Bluetooth_Time)
if device_addresses == None:
    waiting = True
    while waiting:
        context = GLib.MainContext.default()
        while context.pending():
            context.iteration(False)
    
        pygame.draw.rect(Screen, (236,237,215), No_Bluetooth_Connection)
        No_Bluetooth_Text1 = 'No Bluetooth Connection Found'
        No_Bluetooth_Text2 = 'Please Connect a Device To Continue'
        Centered_draw_text(No_Bluetooth_Text1, text_font, text_col, Y_Bluetooth_Text)
        Centered_draw_text(No_Bluetooth_Text2, text_font, text_col, Y_Bluetooth_Text + 40)

        if bluetooth_popup == True:
            pygame.draw.rect(Screen, (236,237,215), Bluetooth_Window)
            Centered_draw_text(Bluetooth_Text, text_font, text_col, Y_Bluetooth_Text)
            Centered_draw_text(Bluetooth_Timer, text_font, text_col, Y_Bluetooth_Time)
            Bluetooth_Time -= 1
            Bluetooth_Timer = str(Bluetooth_Time)
        for event in pygame.event.get():
            if event.type == Bluetooth_Start:  
                is_discoverable = False
                bluetooth_popup = False
                Discoverability.Set(InterfaceDiscover, 'Discoverable', GLib.Variant('b',is_discoverable)) 
                pygame.time.set_timer(Bluetooth_Start, 0)
                Bluetooth_Time = 10


        pygame.display.update()
        everything = manager.GetManagedObjects()
        for path, interfaces in everything.items():
            if 'org.bluez.Device1' in interfaces:
                device_props = interfaces['org.bluez.Device1']
                Name = device_props.get('Name')
                Address = device_props.get('Address')
                connected = device_props.get('Connected')
                if connected:
                    device_addresses = path
                    waiting = False
                    break
        
        time.sleep(1)


waiting_for_music = True
while waiting_for_music:
    context = GLib.MainContext.default()
    while context.pending():
        context.iteration(False)
    for path, interfaces in everything.items():
        if 'org.bluez.Device1' in interfaces:
            Name = device_props.get('Name')
    pygame.draw.rect(Screen, (236,237,215), No_Bluetooth_Connection)
    No_Music_Connection1 = 'Bluetooth Connection to: ' + Name

    No_Music_Connection2 = 'Play Music To Continue'
    Centered_draw_text(No_Music_Connection1, text_font, text_col, Y_Bluetooth_Text)
    Centered_draw_text(No_Music_Connection2, text_font, text_col, Y_Bluetooth_Text + 40)
    pygame.display.update()

    device_addresses_checking = device_addresses + '/player2'
    everything = manager.GetManagedObjects()
    if device_addresses_checking in everything:
        waiting_for_music = False
        break

    time.sleep(1)


#Media Control Pause/Play


Pause_Event = pygame.USEREVENT + 1

#Reading Bluetooth MetaData
InterfaceCommands = 'org.bluez.MediaPlayer1'
InterfaceData = 'org.freedesktop.DBus.Properties'
time.sleep(1)
A1 = bus.get(Service , device_addresses + '/player2')
props = A1[InterfaceData]
MetaData = props.GetAll(InterfaceCommands)
is_discoverable = False

Status = "Status"

Discoverability = Adapter[InterfaceData]

def get_current_volume():
    result = subprocess.run(['amixer', 'get', 'Master'], capture_output=True, text=True)
    match = re.search(r'\[(\d+)%\]', result.stdout)
    if match:
        return int(match.group(1))
    return 50

last_steps = 0
current_volume = get_current_volume()

def adjust_volume():
    global last_steps, current_volume
    
    if rotor.steps > last_steps:
        current_volume += 5
    else:
        current_volume -= 5
    
    last_steps = rotor.steps
    current_volume = max(0, min(100, current_volume))
    
    subprocess.run(['amixer', 'set', 'Master', f'{current_volume}%'], capture_output=True)

rotor.when_rotated = adjust_volume




#Background Coordinates

#Song Name Coordinates
X_Song = Screen_Width//6 - 65
Y_Song = 100

#Artist Name Coordinates
X_Artist = X_Song
Y_Artist = Y_Song + 75

#Album Name Coordinates
X_Album = X_Song
Y_Album = Y_Artist + 75

#TimeBar Outline Coordinates and Dimensions
X_TimeBar = Screen_Width//6
Y_TimeBar = Screen_Height*3/4
TimeBar_Width = Screen_Width*4/6
TimeBar_Height = 30


#Border Width
Border_Width = 5

#TimeBar Loading Coordinates and Dimensions
X_Loading = X_TimeBar + Border_Width
Y_Loading = Y_TimeBar
Loading_Width = 0 
Loading_Height = TimeBar_Height

#Bluetooth Window Text

#Text Creation
Font_Size = 45
Font_Size_Small = 30
text_font = pygame.font.SysFont("akzidenz-garotesk", Font_Size)
text_font_small = pygame.font.SysFont("akzidenz-garotesk", Font_Size_Small)
text_col = (0,0,0)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    Screen.blit(img, (x,y))



#Song Length
X_Song_Length = Screen_Width//6 + TimeBar_Width + 5
Y_Song_Length = Y_TimeBar 
Song_Time = 0


#Current Time
X_Current_Time = Screen_Width//6 - 65
Y_Current_Time = Y_Song_Length
Current_Song_Time_Seconds = 0
Current_Song_Time_Minutes = 0



#Creating Pygame  Objects


Background = pygame.Rect((X_Start, Y_Start, Screen_Width, Screen_Height))
TimeBar = pygame.Rect((X_TimeBar, Y_TimeBar, TimeBar_Width, TimeBar_Height))

Loading_TimeBar = pygame.Rect((X_Loading, Y_Loading, Loading_Width, Loading_Height))

#Clock Creation 
clock=pygame.time.Clock()
FPS = 60
count = 0
Time = 0

#Bluetooth Function


#Pause Function
def PausePlay():
    MetaData = props.GetAll(InterfaceCommands)
    global device_addresses, Service
    Media_Control = bus.get(Service, device_addresses)
    if MetaData['Status'] == 'paused':
        Media_Control.Play()
        print("Paused Button Pressed")

    elif MetaData['Status'] == 'playing':
        Media_Control.Pause()
        print("Play Button Pressed")

#Next Function
def Next():
    MetaData = props.GetAll(InterfaceCommands)
    global device_addresses
    global Service
    Media_Control = bus.get(Service, device_addresses)
    Media_Control.Next()
    print("Next Button Pressed")

#Previous Function
def Previous():
    MetaData = props.GetAll(InterfaceCommands)
    global device_addresses, Time, last_time_update
    global Service, Current_Song_Time_Seconds, Current_Song_Time_Minutes
    Media_Control = bus.get(Service, device_addresses)
    Media_Control.Previous()
    last_time_update = time.time()
    print("Previous Button Pressed")

    Current_Song_Time_Seconds = 0
    Current_Song_Time_Minutes = 0
    Time = 0




button_previous.when_pressed = Previous
button_pauseplay.when_pressed = PausePlay
button_Next.when_pressed = Next


#Creates a function to retrieve data from the metadata
def Information(Data):
    """
    This function retrieves the meta data for the information requested in
    """
    if Data in MetaData['Track']:
        Data = MetaData['Track'][Data]
    else:
        Data = 'Not Availabe'
    
    return Data




ChangedProperties = 'PropertiesChanged'

TrackPlaying = True

def refresh(MetaData, ChangedProperties, Data):
    if 'Track' in ChangedProperties:
        global last_time_update, Current_Song_Time_Seconds, Total_Song_Length_Minutes, Total_Song_Length_Seconds, Current_Song_Time_Minutes, Time, Song_Title, Artist_Name, Album_Name, Total_Song_Length_MillieSeconds, Total_Song_Length_Seconds_All, Round_Total_Song_Length_Seconds, Total_Song_Length_Str, Current_Song_Time
        Song_Title = ChangedProperties['Track']['Title']
        Artist_Name = ChangedProperties['Track']['Artist']
        Album_Name = ChangedProperties['Track']['Album']
        Total_Song_Length_MillieSeconds = ChangedProperties['Track']['Duration']
        Total_Song_Length_Seconds_All = Total_Song_Length_MillieSeconds/1000
        Total_Song_Length_Minutes = Total_Song_Length_Seconds_All//60
        Total_Song_Length_Seconds = (Total_Song_Length_Seconds_All/60 - Total_Song_Length_Minutes)*60
        Round_Total_Song_Length_Seconds = round(Total_Song_Length_Seconds)
        Total_Song_Length_Str= str(int(Total_Song_Length_Minutes)) + ":" + str(Round_Total_Song_Length_Seconds).zfill(2)
        Current_Song_Time = str(Current_Song_Time_Minutes) + ":" +str(Current_Song_Time_Seconds).zfill(2)
        Current_Song_Time_Seconds = 0
        Current_Song_Time_Minutes = 0
        Time = 0
        last_time_update = time.time()
        
    if 'Status' in ChangedProperties:
        global TrackPlaying
        TrackPlaying = ChangedProperties['Status'] == 'playing'


props.PropertiesChanged.connect(refresh)



Song_Title = Information('Title')
Artist_Name = Information('Artist')
Album_Name = Information('Album')
Total_Song_Length_MillieSeconds = Information('Duration')
Total_Song_Length_Seconds_All = Total_Song_Length_MillieSeconds/1000
Total_Song_Length_Minutes = Total_Song_Length_Seconds_All//60
Total_Song_Length_Seconds = (Total_Song_Length_Seconds_All/60 - Total_Song_Length_Minutes)*60
Round_Total_Song_Length_Seconds = round(Total_Song_Length_Seconds)







run = True

while run:

    #Checking for D-Bus Events
    context = GLib.MainContext.default()
    while context.pending():
        context.iteration(False)

  
    #Setting FPS to 60 and Adding 1 Count Every Frame 
    clock.tick(FPS)
    count += 1

    #Initlization Key Pressing
    key = pygame.key.get_pressed()

    #Drawing Pygame Objects
    pygame.draw.rect(Screen, (236,237,215), Background)
    pygame.draw.rect(Screen, (0,0,0), TimeBar, 5, border_radius = 5)

    pygame.draw.rect(Screen, (0,0,0), Loading_TimeBar, border_radius = 5)



    if TrackPlaying:
        current_time = time.time()
        elapsed = current_time - last_time_update
        last_time_update = current_time
        Time += elapsed
        Percentage_TimeBar_Convert = (Time/Total_Song_Length_Seconds_All) * TimeBar_Width - Border_Width
        Loading_TimeBar = pygame.Rect((X_Loading, Y_Loading, Percentage_TimeBar_Convert, Loading_Height))

    if Time > Total_Song_Length_Seconds_All:
        Percentage_TimeBar_Convert = TimeBar_Width
        Loading_TimeBar = pygame.Rect((X_Loading, Y_Loading, Percentage_TimeBar_Convert, Loading_Height))



    #Creating Time Bar Strings
    #if count%60 == 0 and TrackPlaying:
        #Current_Song_Time_Seconds += 1


    #if Current_Song_Time_Seconds == 60 and TrackPlaying:
        #Current_Song_Time_Seconds = 0
        #Current_Song_Time_Minutes += 1

    Current_Song_Time_Minutes = int(Time // 60)
    Current_Song_Time_Seconds = int(Time % 60)
    

    if Song_Time > Total_Song_Length_Seconds_All:
        Song_Time = Total_Song_Length_Seconds_All

    

    #Creating Total Song Length
    Total_Song_Length_Str= str(int(Total_Song_Length_Minutes)) + ":" + str(Round_Total_Song_Length_Seconds).zfill(2)

    #Creating Current Song Time
    Current_Song_Time = str(Current_Song_Time_Minutes) + ":" +str(Current_Song_Time_Seconds).zfill(2)


    #Drawing Texts
    draw_text(Song_Title, text_font, text_col, X_Song, Y_Song)

    draw_text(Artist_Name, text_font, text_col, X_Artist, Y_Artist)

    draw_text(Album_Name, text_font, text_col, X_Album, Y_Album)

    draw_text(Total_Song_Length_Str, text_font, text_col, X_Song_Length, Y_Song_Length)

    draw_text(Current_Song_Time, text_font, text_col, X_Current_Time, Y_Current_Time)

    Connection = "Connection:" + Name
    if TrackPlaying == True:
        Status = "Status: Playing"
    else:
        Status = "Status: Pause"
        
    X_Connection = X_Current_Time
    Y_Connection = Y_Current_Time + 50
    X_Status = X_Song_Length - 90
    Y_Status = Y_Connection

    draw_text(Connection, text_font_small, text_col, X_Connection, Y_Connection)

    draw_text(Status, text_font_small, text_col, X_Status, Y_Status)



    #Bluetooth Button and Bluetooth Connection Window
    for event in pygame.event.get():
        if event.type == Bluetooth_Start:  
            is_discoverable = False
            bluetooth_popup = False
            Discoverability.Set(InterfaceDiscover, 'Discoverable', GLib.Variant('b',is_discoverable)) 
            pygame.time.set_timer(Bluetooth_Start, 0)
            Bluetooth_Time = 10

        if event.type == pygame.QUIT:
            run = False
        
        if key[pygame.K_ESCAPE] == True:
            run = False

    if bluetooth_popup == True:
        pygame.draw.rect(Screen, (236,237,215), Bluetooth_Window)
        Centered_draw_text(Bluetooth_Text, text_font, text_col, Y_Bluetooth_Text)
        Centered_draw_text(Bluetooth_Timer, text_font, text_col, Y_Bluetooth_Time)

        if count%60 == 0:
            Bluetooth_Time -= 1
        
        pygame.display.update()

    #Refreshing Screen
    pygame.display.update()

#end of start loop

button_bluetooth.close()
button_previous.close()
button_pauseplay.close()
button_Next.close()
pygame.display.quit()
time.sleep(.5)
pygame.quit()