import pygame
import numpy as np
import time as clock
import waterRocket as wr
import matplotlib.pyplot as plt


minYrocket = 700

def plotDat(dataIn, time):
    # time
    tstart = 0 #s
    tstop = 10 #s
    tstep = 0.001 #s this is delta t

    fig = plt.figure()
    fig.suptitle("Water Rocket Plots")

    grid = plt.GridSpec(2, 3, wspace=0.4, hspace=0.3)
    
    ayG = fig.add_subplot(grid[0,1])
    vyG = fig.add_subplot(grid[1,1])
    yG  = fig.add_subplot(grid[0:2,0])
    p = fig.add_subplot(grid[0:2,2])

    accY = dataIn[:, 3]
    velY = dataIn[:, 5]
    posX = dataIn[:, 6]
    posY = dataIn[:, 7]
    pres = dataIn[:, 8]
    t = time

    ayG.plot(t, accY)
    vyG.plot(t, velY)
    yG.plot(posX, posY)
    p.plot(t, pres)

    ayG.set_xlabel('time (s)')
    vyG.set_xlabel('time (s)')
    yG.set_xlabel('Position X (m)')
    p.set_xlabel('time (s)')

    ayG.set_ylabel('Accerlation Y (m/s^2)')
    vyG.set_ylabel('Velocity Y (m/s)')
    yG.set_ylabel('Position Y (m)')
    p.set_ylabel('Air Pressure (Pa)')

    plt.show()

    return 0

def initPyGame():
    #initilize the pygame lib
    pygame.init()

    # Set up the drawing window
    global screen
    screen = pygame.display.set_mode((1000,800))

    #title and icon
    pygame.display.set_caption("Water Bottle Rocket Sim V0.1")
    icon = pygame.image.load('rocketlogo.png')
    pygame.display.set_icon(icon)

    #font
    global font
    font = pygame.font.SysFont(None, 35)
    
    return 0

def rocket(pos):
    #rocket image
    rocketOn = pygame.image.load('rocket_on.png')
    rocketOff = pygame.image.load('rocket_off.png')
    
    if pos[1] < minYrocket-10:
        screen.blit(rocketOn, (pos[0], pos[1]))
    else:
        screen.blit(rocketOff, (pos[0], pos[1]))

def exit(event):
    if event.type == pygame.QUIT:
        return True
    return False

def rocketParamaters(events,i, dat):
    pygame.draw.rect(screen, (204, 204, 204), pygame.Rect(500, 50, 360, 160))
    time = font.render("Time   (s) = " + str(round(i,2)),True,(0,0,0))
    accel = font.render("Acceleration (m/s^2) = " + str(round(dat[3],2)),True,(0,0,0))
    vel = font.render("Velocity (m/s) = " + str(round(dat[5],2)),True,(0,0,0))
    position = font.render("Height (m) = " + str(round(dat[7],2)),True,(0,0,0))
    screen.blit(time,(510, 60))
    screen.blit(accel,(510, 100))
    screen.blit(vel,(510, 140))
    screen.blit(position,(510, 180))
    return False

def rocketWelcome():
    print()
    print()
    print()
    print("        |")
    print("       / \\")
    print("      / _ \\")
    print("     |.o '.|")
    print("     |'._.'|")
    print("     |     |")
    print("   ,'|  |  |`.")
    print("  /  |  |  |  \\")
    print("  |,-'--|--'-.|")
    print()
    print("University of Michigan, College of Engineernig")
    print("Mechanical Enginering - MECHENG 495 W2021")
    print("Justin Forester, Luthfor Khan, Ellie Mercer")
    print()
    print("Welcome to the Water Bottle Rocket Sim V0.1")
    print()
    print("We will need a couple Rocket Parameters before launch")
    print()

def errorMssg(max):
    print("The value entered is not between 0 and " + str(max))

def checkVal(str, i):
    num = float(str)
    if i > 0:
        #this is for height of water
        if num > 22 or num < 0:
            errorMssg(22)
            return False
        else:
            return True
    elif i < 0:
        #this is for pressure of air
        if num > 482633 or num < 0:
            errorMssg(482633)
            return False
        else:
            return True

def getUserInput():
    rocketWelcome()

    wH = True
    while wH:
        heightWater =input("Select height of water (cm - MAX 22cm): ")
        wH = not checkVal(heightWater, 1)
    
    aP = True
    while aP:
        airPress =input("Select Pressure of air (Pa - MAX 482633Pa): ")
        aP = not checkVal(airPress, -1)

    heightWater = float(heightWater)
    airPress = float(airPress)

    print()
    print("You have selected:")
    print("Water Height: " + str(round(heightWater,3)) + " cm")
    print("Air Pressure: " + str(round(airPress,3)) + " Pa")
    print()
    print("Importing Selected Values...")
    print("Begninning Rocket Calculations")
    
    return [heightWater, airPress]

def main(dataIn, time, maxHeight, maxDis):
    #init pygame
    initPyGame()
    
    # Run until the user asks to quit
    run = True
    i = 0

    print("Launching rocket")
    while run:
        t = time[i]
        #check to see if the user clicked the exit button
        events = pygame.event.get()
        for event in events:
            run = not exit(event)
        #background color
        screen.fill((201, 233, 246))
        # ground 
        pygame.draw.rect(screen, (126, 200, 80), pygame.Rect(0, 740, 1000, 60))
        
        py = data[i][7]*500/maxHeight
        px = data[i][6]*750/maxDis

        rocketParamaters(events,t, dataIn[i])

        #display rocket
        rocket([100+px,minYrocket-py])
        
        if i < time.size-1:
            i += 1
        
        #update display
        pygame.display.update()
        clock.sleep(.001)

    pygame.quit()

    return 0

if __name__ == "__main__":
    usrIn = getUserInput()
    phi = 45 #deg
    usrIn.append(phi)

    data, time, maxHeight, maxDis = wr.main(usrIn)
    
    print("Preparing Launch")
    

    #main(data, time[:data.shape[0]], maxHeight, maxDis)
    
    index = data.shape[0]-1
    flightDir = str(round(time[index],3)) + " seconds "
    height = str(round(maxHeight,3)) + " meters "
    dis = str(round(maxDis,3)) + " meters "
    print("The rocket flew for " + flightDir + "with max height of " + height + "and a max distance of " + dis)
    print()

    ans = 'n'#str(input("Would you like to see the plot? (y/n) "))
    
    if ans == 'y':
        plotDat(data, time[:data.shape[0]])

    print()
    print("That's all Folks!!")
    print()