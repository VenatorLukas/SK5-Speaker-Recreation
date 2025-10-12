import pygame
from pydbus import SystemBus
import time


## Create Dbus and Bluez Connection to Phone
bus = SystemBus()
Service = 'org.bluez'
ObjPath = '/org/bluez/____/_____________'
InterfaceCommands = 'org.bluez.MediaPlayer1'
InterfaceData = 'org.freedesktop.DBus.Properties'
A1 = bus.get(Service , ObjPath)
props = A1[InterfaceData]
MetaData = props.GetAll(InterfaceCommands)



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






pygame.init()

#Background Coordinates
X_Start = 0
Y_Start = 0
Screen_Width = 800
Screen_Height = 480

#Song Name Coordinates
X_Song = 150
Y_Song = 100

#Artist Name Coordinates
X_Artist = X_Song
Y_Artist = Y_Song + 50

#Album Name Coordinates
X_Album = X_Song
Y_Album = Y_Artist + 50

#TimeBar Outline Coordinates and Dimensions
X_TimeBar = Screen_Width//6
Y_TimeBar = Screen_Height*3/4
TimeBar_Width = Screen_Width*4/6
TimeBar_Height = 30

#Song_Length
Total_Song_Length = 220
Total_Song_Length_Minutes = Total_Song_Length//60
Total_Song_Length_Seconds = (Total_Song_Length/60 - Total_Song_Length_Minutes)*60
Round_Total_Song_Lengths_Seconds = round(Total_Song_Length_Seconds)

#Border Wid
Border_Width = 5

#TimeBar Loading Coordinates and Dimensions
X_Loading = X_TimeBar + Border_Width
Y_Loading = Y_TimeBar
Loading_Width = 0 
Loading_Height = TimeBar_Height

#Text Creation
Font_Size = 45
text_font = pygame.font.SysFont("akzidenz-garotesk", Font_Size)
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
Screen = pygame.display.set_mode((Screen_Width, Screen_Height), pygame.FULLSCREEN)
 
Background = pygame.Rect((X_Start, Y_Start, Screen_Width, Screen_Height))
TimeBar = pygame.Rect((X_TimeBar, Y_TimeBar, TimeBar_Width, TimeBar_Height))

Loading_TimeBar = pygame.Rect((X_Loading, Y_Loading, Loading_Width, Loading_Height))

#Clock Creation 
clock=pygame.time.Clock()
FPS = 60
count = 0
Time = 0

run = True
while run:

    #Sets variable from the function
    Song_Title = Information('Title')
    Artist_Name = Information('Artist')
    Album_Name = Information('Album')
    Total_Song_Length_MillieSeconds = Information('Duration')
    Total_Song_Length_Seconds_All = Total_Song_Length_MillieSeconds/1000
    Total_Song_Length_Minutes = Total_Song_Length_Seconds_All//60
    Total_Song_Length_Seconds = (Total_Song_Length_Seconds_All/60 - Total_Song_Length_Minutes)*60
    Round_Total_Song_Length_Seconds = round(Total_Song_Length_Seconds)

    #Setting FPS to 60 and Adding 1 Count Every Frame 
    clock.tick(FPS)
    count += 1

    #Initlization Key Pressing
    key = pygame.key.get_pressed()

    #Drawing Pygame Objects
    pygame.draw.rect(Screen, (236,237,215), Background)
    pygame.draw.rect(Screen, (0,0,0), TimeBar, 5, border_radius = 5)

    pygame.draw.rect(Screen, (0,0,0), Loading_TimeBar, border_radius = 5)


    #Loading Part
    if count%1 == 0:
        Time += .05/3
        Percentage_TimeBar_Convert = (Time/Total_Song_Length) * TimeBar_Width - Border_Width
        Loading_TimeBar = pygame.Rect((X_Loading, Y_Loading, Percentage_TimeBar_Convert, Loading_Height))

    if Time > Total_Song_Length:
        Percentage_TimeBar_Convert = TimeBar_Width
        Loading_TimeBar = pygame.Rect((X_Loading, Y_Loading, Percentage_TimeBar_Convert, Loading_Height))



    #Creating Time Bar Strings
    if count%60 == 0:
        Current_Song_Time_Seconds += 1


    if Current_Song_Time_Seconds == 60:
        Current_Song_Time_Seconds = 0
        Current_Song_Time_Minutes =+ 1
    

    if Song_Time > Total_Song_Length:
        Song_Time = Total_Song_Length

    

    #Creating Total Song Length
    Total_Song_Length_Str= str(int(Total_Song_Length_Minutes)) + ":" + str(Round_Total_Song_Lengths_Seconds).zfill(2)

    #Creating Current Song Time
    Current_Song_Time = str(Current_Song_Time_Minutes) + ":" +str(Current_Song_Time_Seconds).zfill(2)


    #Drawing Texts
    draw_text(Song_Title, text_font, text_col, X_Song, Y_Song)

    draw_text(Artist_Name, text_font, text_col, X_Artist, Y_Artist)

    draw_text(Album_Name, text_font, text_col, X_Album, Y_Album)

    draw_text(Total_Song_Length_Str, text_font, text_col, X_Song_Length, Y_Song_Length)

    draw_text(Current_Song_Time, text_font, text_col, X_Current_Time, Y_Current_Time)



    #Exit Statements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if key[pygame.K_ESCAPE] == True:
            run = False

    #Refreshing Screen
    pygame.display.update()

pygame.display.quit()
time.sleep(.5)
pygame.quit()