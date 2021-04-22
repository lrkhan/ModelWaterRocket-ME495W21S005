import numpy as np
import pandas as pd

#Returns an array for the drag froce for x and y directions
def dragForce(velX, velY):
    airDensity = 1.225 #kg/m^3
    dragCoeff = 0.4 #drag coefficient
    crosArea = np.pi*np.power(0.03556,2) #m^2 - cross sectional area of the rocket
    
    fDrag = np.array([velX * np.abs(velX), velY * np.abs(velY)])
    
    fDrag = fDrag * .5 * airDensity * dragCoeff * crosArea

    return fDrag

#rocket mass
def rocketMass(bottleMass, dataIn, deltaT, inThrust):
    waterDen = 997 #kg/m^3
    bottleVol = 0.000591471 #m^3 - 20 oz

    if not inThrust:
        return bottleMass
    else:
        M = bottleMass + (waterDen * (bottleVol - volume(height(dataIn,deltaT))))
        return M

#thrust force 
def thrustForce(datIn, deltaT, waterVol, pIn):
    pressureATM = 101325 #Pa - 1 atm
    areaNozzle = np.pi * np.power(radius(0),2)
    pres = pressure(datIn, deltaT, waterVol, pIn)

    return (2*areaNozzle*(pres-pressureATM)), pres

#pressure based on volume of air in bottle
def pressure(datIn, deltaT, waterVol, airPin):
    k = 1.4 #ratio of heat cap of air 
    pATM = 101325 #Pa - 1 atm
    pressureInitail = airPin + pATM #Pa - 70 PSI
    bottleVol = 0.000591471 #m^3 - 20 oz
    volInitial = bottleVol - waterVol
    v = volume(height(datIn,deltaT))

    return (pressureInitail * np.power(volInitial/v, k))

#volume of air based on height of water
def volume(hWat):
    #bottle height consts
    ht = 0.2257 #m - 8.89in tall bottle
    h_0 = 0.06858 #m - 2.7in 
    h_1 = 0.03302 #m - 1.3in
    rCy = 0.03175 #m - 1.25in 
    rNz = 0.0127 #m - 0.5in
    h = ht - hWat #m - this should be the height of air in the bottle

    if h <= ht and h >= h_0:
        return (np.pi*np.power(rCy,2)*h)
    elif h < h_0 and h >= h_1:
        h = hWat
        volCy =  np.pi*np.power(rCy,2)*(ht - h_0)
        volRnd = (np.pi*(3203126670000*np.power(h_0,7)-2164215851000*np.power(h_0,6)+616552901580*np.power(h_0,5)-91937563515*np.power(h_0,4)+7256906643*np.power(h_0,3)-261305877*np.power(h_0,2)+4233621*h_0-3203126670000*np.power(h,7)+2164215851000*np.power(h,6)-616552901580*np.power(h,5)+91937563515*np.power(h,4)-7256906643*np.power(h,3)+261305877*np.power(h,2)-4233621*h))/2100000000
        return (volRnd + volCy)
    else:
        h = h_1 - hWat
        volCy =  np.pi*np.power(rCy,2)*(ht - h_0)
        volRnd = (np.pi*(3203126670000*np.power(h_0,7)-2164215851000*np.power(h_0,6)+616552901580*np.power(h_0,5)-91937563515*np.power(h_0,4)+7256906643*np.power(h_0,3)-261305877*np.power(h_0,2)+4233621*h_0-3203126670000*np.power(h_1,7)+2164215851000*np.power(h_1,6)-616552901580*np.power(h_1,5)+91937563515*np.power(h_1,4)-7256906643*np.power(h_1,3)+261305877*np.power(h_1,2)-4233621*h_1))/2100000000
        volNz = np.pi*np.power(rNz,2)*(h)
        return (volCy + volRnd + volNz)
    return 0

#radius of bottle based on height of water
def radius(height):
    if height >= 0.06858:
        # returns large diameter of bottle if h>= 2.7in
        return 0.03175
    elif height < 0.06858 and height >= 0.03302:
        # from 3rd orde ployfit, output is in meters
        r = 103.33*np.power(height,3) - 29.921*np.power(height,2) + 2.7713*height - 0.0449 
        return r
    else:
        #returns nozzle radius
        rNz = 0.0127 #m - 0.5in
        return rNz
    return 0

#height of water
def height(datIn, delt):
    h0 = datIn[1] #m - initial height of water in
    velNozzle = datIn[0] #this is based on past data
    areaNozzle = np.pi * np.power(radius(0),2)
    areaCurr = np.pi * np.power(radius(h0),2) #this is based on past data

    return (h0 - delt*((areaNozzle*velNozzle)/areaCurr))

def initial(data, mass, phi):
    bottleVol = 0.000591471 #m^3 - 20 oz
    #global hWat0, airPressure0
    #hWat0 = 0.128 #m
    waterVol = bottleVol - volume(hWat0) #m^3 - 10 fluid oz
    #airPressure0 = 482633 #Pa - 70 PSI - guage pressure
    #airPressure0 = airPressure0 + 101325
    massBottle = mass #kg
    g = -9.81 #m/s^2
    x0 = 0 #m
    y0 = 0 #m
    v0 = 0 #m/s
    a0 = 0 #m/s^2
    theta =  phi #deg - launch angle
    theta = (np.pi * theta)/180 #rad

    areaNozzle = np.pi*np.power(radius(0),2)
    nozzlevelocity = np.sqrt(2*(airPressure0 - 101325)/997)

    dF = dragForce(v0*np.cos(theta),v0*np.sin(theta))
    m = massBottle + waterVol*997
    tF = np.power(nozzlevelocity,2)*areaNozzle*997
    tf = np.array([np.cos(theta), np.sin(theta)]) * tF
    # initial data
    data[0][0] = nozzlevelocity
    data[0][1] = hWat0
    data[0][2] = a0*np.cos(theta) + ((tf[0] - dF[0])/m)#x acl
    data[0][3] = a0*np.sin(theta) + g + ((tf[1] -  dF[1])/m)#y acl
    data[0][4] = v0*np.cos(theta) #x vel
    data[0][5] = v0*np.sin(theta) #y vel
    data[0][6] = x0 #x pos
    data[0][7] = y0 #x pos
    data[0][8] = airPressure0 #x pos
    data[0][9] = 0

    return data

def trimDat(dat, loc):
    trim = dat
    for r in range(np.shape(dat)[0]-1, loc, -1):
        trim = np.delete(trim, r, 0)

    return trim

def main(input):

    bottleVol = 0.000591471 #m^3 - 20 oz
    pATM = 101325
    airMm = 0.02897 #kg/mol - air molar mass
    R = 8.314 #J/mol K - ideal gas constant
    temp = 0 + 273.15 #K - temp in K
    
    global hWat0, airPressure0, waterVol0, phi
    
    hWat0 = input[0]/100
    airPressure0 = input[1] + pATM
    waterVol0 = bottleVol - volume(hWat0)
    phi = input[-1]
    theta = (np.pi * phi)/180 #rad 
    
    massBottle = 0.15 #kg - 150 g
    g = -9.81 #m/s^2
    # time
    tstart = 0 #s
    tstop = 10 #s
    tstep = 0.0005 #s this is delta t
    time = np.arange(tstart, tstop+tstep, tstep)

    data = np.empty([time.size, 10])

    data = initial(data, massBottle, phi)
    
    i = 1
    # thrust phase while water volume g8er than 0
    inThrust = True
    while inThrust:
        #thrust phase stuff
        denWat = 997 #kg/m^3
        mass = rocketMass(massBottle, data[i-1], tstep, inThrust)
        dForce = dragForce(data[i-1][4],data[i-1][5])
        tForce, pres = thrustForce(data[i-1], tstep, waterVol0, airPressure0)
        nozVel = np.sqrt(np.abs(tForce/(997*np.pi*np.power(radius(0),2))))
        tFx = tForce*np.power(np.cos(theta),2)
        tFy = tForce*np.power(np.sin(theta),2)

        data[i][0] = nozVel
        data[i][1] = height(data[i-1],tstep)
        data[i][2] = (tFx - dForce[0]/mass) #x acl
        data[i][3] = ((tFy -  dForce[1])/mass) + g #y acl
        data[i][4] = data[i-1][4] + tstep*(data[i-1][2]) #x vel
        data[i][5] = data[i-1][5] + tstep*(data[i-1][3]) #y vel
        data[i][6] = data[i-1][6] + tstep*(data[i-1][4])  #x pos
        data[i][7] = data[i-1][7] + tstep*(data[i-1][5])  #y pos
        data[i][8] = pres #air pressure 
        data[i][9] = time[i]
        #print("Time: " + str(round(time[i],6)) + ", PosX: "+str(round(data[i][6],2)) +", PosY: "+str(round(data[i][7],2)))
        inThrust = (data[i][1] > 0)
        i += 1
    
    i -= 2

    airMass = (data[i-1][8] * bottleVol * airMm)/(R*temp)
    mass = rocketMass(massBottle, data[i-1], tstep, inThrust)

    airBottle = True
    while airBottle:
        Cd = 0.8
        A = np.pi * np.power(radius(0),2)
        k = 1.4
        denAir = 1.204 #kg/m^3 - density of air at NTP
        pUp = data[i-1][8]
        if (pUp/pATM) >= 1.893:
            #choked flow
            mDot = Cd*A*np.sqrt(k*denAir*pUp*np.power(2/(k+1),(k+1)/(k-1)))
            airMass -= (mDot*tstep)
        elif (pUp >= pATM):
            #unchoked flow
            a = k/(k-1)
            b = (k+1)/k
            c = pATM/pUp
            mDot = Cd*A*np.sqrt(2*denAir*pUp*a*((np.power(c,2/k))-(np.power(c,b))))
            airMass -= (mDot*tstep)
        
        airPres = (airMass*R*temp)/(airMm*bottleVol)
        nozVel = np.sqrt((2*np.abs(airPres-pATM))/denAir)
        nozVelx = nozVel*np.cos(theta)
        nozVely = nozVel*np.sin(theta)
        fThrustx = denAir*A*np.power(nozVelx,2)
        fThrusty = denAir*A*np.power(nozVely,2)
        dForce = dragForce(data[i-1][4],data[i-1][5])

        data[i][0] = nozVel
        data[i][1] = 0
        data[i][2] = (fThrustx - dForce[0]/mass) #x acl
        data[i][3] = ((fThrusty -  dForce[1])/mass) + g #y acl
        data[i][4] = data[i-1][4] + tstep*(data[i-1][2]) #x vel
        data[i][5] = data[i-1][5] + tstep*(data[i-1][3]) #y vel
        data[i][6] = data[i-1][6] + tstep*(data[i-1][4])  #x pos
        data[i][7] = data[i-1][7] + tstep*(data[i-1][5])  #y pos
        data[i][8] = airPres #air pressure 
        data[i][9] = time[i]

        #print("Time: " + str(round(time[i],6)) + ", PosX: "+str(round(data[i][6],2)) +", PosY: "+str(round(data[i][7],2)))
        airBottle = (data[i][8] > pATM)
        i += 1

    i -= 2

    inAir = True
    while inAir:
        dForce = dragForce(data[i-1][4],data[i-1][5])
        tForce = 0

        data[i][0] = 0
        data[i][1] = 0
        data[i][2] = - (dForce[0]/mass) #x acl
        if data[i-1][3] > 0:
            data[i][3] = ((tForce -  dForce[1])/mass) + g #y acl
        else:
            data[i][3] = ((tForce +  dForce[1])/mass) + g #y acl
        data[i][4] = data[i-1][4] + tstep*(data[i-1][2]) #x vel
        data[i][5] = data[i-1][5] + tstep*(data[i-1][3]) #y vel
        data[i][6] = data[i-1][6] + tstep*(data[i-1][4])  #x pos
        data[i][7] = data[i-1][7] + tstep*(data[i-1][5])  #y pos
        data[i][8] = data[i-1][8] #air pressure 
        data[i][9] = time[i]

        inAir = data[i][7] > 0
        #print("Time: " + str(round(time[i],6)) + ", PosX: "+str(round(data[i][6],2)) +", PosY: "+str(round(data[i][7],2)))
        i += 1
    
    
    data = trimDat(data, i-2)
    pd.DataFrame(data).to_csv("output.csv", index=False)
    mH = np.max(data[:, 7])
    mV = np.max(data[:, 6])

    print("Calculations Complete")
    print()

    return data, time, mH, mV
