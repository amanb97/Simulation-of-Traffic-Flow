#Importing Libraries
import random

import numpy as np


def initial(Length,Numberofcars,Seed,Vmax,Queues):

    #Unoccupied road of length L
    Road = np.full(Length,-1)
    #carid stores unique identifiers for each car
    Carid = np.full(Length,0)
    #Colour stores unique colour values for each car
    Colour = np.zeros((Length, 3))
    #used in the extension, to specify hesitant drivers and how much they slow in random events
    Skill = np.full(Numberofcars,0)
    #used in the extension, stores whether cars are able to go over the speed limit
    Aggression = np.full(Numberofcars,0)


    #The seed can either be random or specified when calling the function
    if Seed != "Random":
        random.seed(Seed)

    #Samples random positions in the road for all N cars
    pos = random.sample(range(Length),Numberofcars)

    #sorts position so it assigns ids in chronological order
    pos=np.sort(pos)


    #Assigns each of the positions and ids with 0 velocity or an incrementing car id, going from 1 to N
    temp = 1
    for i in pos:
        Road[i] = 0
        Carid[i] = temp
        temp += 1

    #mirrors the road array and creates one for colour, so each car has a unique rgb value when plotting
    for i in pos:
        r=random.random()
        g=random.random()
        b=random.random()
        Colour[i]=(r,g,b)

    #Assigns random values to skill for how much a car slows down in an event, aggression gets random values of 0 or 1
    for i in range(Numberofcars):
        Skill[i] = random.randint(0,Vmax)
        Aggression[i] = random.randint(0,1)


    #Assigns colour values to normal and hesitant cars, going from green(normal) to yellow(hesitant)
    #this is why tempcolour adds a shift, creating this gradient
    #the loop iterates over each possible skill value, seeing which value each car has, and then alters the colour array with this colour

    if Queues != "False":
        tempcolour = (0,1,0)
        rshift = 1/(Vmax+1)
        for j in range(0,Vmax+1):
            tempcolour = np.add(tempcolour, (rshift,0,0))
            for i in range(Numberofcars):
                if Skill[i] == j:
                    Colour[np.where(Carid == (i+1))] = tempcolour

        if Queues == "Aggression" or Queues == "Skill and Aggression":
            for i in range(Numberofcars):
                if Aggression[i] == 1:
                    Colour[np.where(Carid == (i+1))] = (1,0,0)

    return(Road,Colour,Carid,Skill,Aggression)


def onesec(Length,Road,max_velocity,probability,colour,Carid,Queues,Skill,Aggression):
    #Defines the updated road, ids and colours after the onesec function is used
    new_Road = -np.ones(Length, dtype=int)
    new_id = -np.zeros(Length, dtype=int)
    new_colour = np.zeros((Length, 3))

    for i in range(len(Road)):

        #Rule 1
        #moves velocity forward until vmax is reached
        if Queues == 'False' or Queues == 'Skill':
            #If a space is actually occupied
            if -1 < Road[i] < max_velocity:
                #increases velocity
                Road[i]+=1

        #If aggression is enabled, then cars can increase to v_max + 5 in one time step
        if Queues == 'Aggression' or Queues == 'Skill and Aggression':
            #Car does not have aggression trait, regular rules
            if (Aggression[Carid[i]-1]) == 0 and -1 < Road[i] < max_velocity:
                Road[i]+=1
            #car is aggressive
            if (Aggression[Carid[i]-1]) == 1 and -1 < Road[i] < max_velocity:
                Road[i] += max_velocity + 5

        #Rule 2
        #if a car is moving
        if Road[i] >= 0:
            car_separation = 1
            #while loop looks until it finds a car in an occupied space
            while Road[(i + car_separation) % Length] == -1:
                #keeps iterating the separation until it finds a car
                car_separation += 1
            #If the car has more velocity than the separation, its velocity is reduced
            if Road[i] >= car_separation:
                Road[i] = car_separation - 1

        #Rule 3
        if Queues == 'False' or Queues == 'Aggression':
            #If a car is moving it has probability for a random slow down
            if (Road[i] > 0) and (random.randint(0,100) < probability) and (Aggression[Carid[i]-1] != 1):
                Road[i] += -1

        if Queues == 'Skill' or Queues == 'Skill and Aggression':
            #In the extension, hesitant cars slow down more based off of their unique skill value
            #Carid is used to find the index of the current ith car and supply it to skill.
            if (Road[i]> (Skill[Carid[i]-1] -1)) and (random.randint(0,100) < probability) and (Aggression[Carid[i]-1] != 1):
                Road[i] += - Skill[Carid[i]-1]


        #Rule 4
        if Road[i] >= 0:
            #updates to the new position, using the modulo operator to get a cycled index as the car loops round
            new_position = (i + Road[i]) % Length
            new_Road[new_position] = Road[i]
            new_colour[new_position] = colour[i]
            new_id[new_position] = Carid[i]


    Road = new_Road
    colour = new_colour
    Carid=new_id

    return(Road,colour,Carid)


def flowcheck(Road,Length,Flowcount):
    #This function is used to count how many cars pass the end of the road
    for i in range(len(Road)):
        #checks if a car has enough velocity to surpass the end
        if Road[i]  >= (Length - i):
            #if a car has looped, increase flow counter
            Flowcount +=1
    return(Flowcount)


def journeyt(Journeytime,Looped,End,Road,Length,Carid,j):
    for i in range(len(Road)):
        #checks if a car has enough velocity to surpass the end
        if Road[i]  >= (Length - i) or (Road[i] + 1) >= (Length - i) and End == 'False':
            #if a car has looped set its respective index in looped to 1
            Looped[Carid[i]-1] = 1
    #if all cars have looped, stop checking (end=true) and the journey time is whatever the current time is
    if np.all(Looped == 1) and End == 'False':
        End = 'True'
        Journeytime = j


    return(Journeytime,Looped,End)
