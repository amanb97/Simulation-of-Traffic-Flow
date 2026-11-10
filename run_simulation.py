import numpy as np

from road import initial, onesec, flowcheck, journeyt
from plotting import singlesecondplot, multiplesecondplot, animate


def simulate(length,time,number_cars,vmax,event_prob,singleplot,multipleplot,animation,Seed,Queues):

    #2d array of all the roads in one simulation
    x2d=np.empty((0,length))

    #stores all the car ids, in every position, in every second of the road
    carid2d=np.empty((0,length))

    #stores all colour, in every position, in every second of the road
    colour3d=np.empty((0,length,3))

    #how many time steps
    totaltime = np.arange(1,time+1)

    #gets initial variables
    road, colour, car_id, skill,aggression= initial(length,number_cars,Seed,vmax,Queues)

    #used to count flow at the end of the road
    flowcount = 0

    #used to count the total journey time for all cars to complete a cycle of the road
    journeytime = 0
    #stays false until all cars have cycled
    end = 'False'
    #can be 1 or 0 if a car has looped
    looped = np.full(number_cars,0)


    for j in totaltime:
        road,colour,car_id= onesec(length,road,vmax,event_prob,colour,car_id,Queues,skill,aggression)
        if singleplot or multipleplot:
            #stacks/concatenate creates 1 array of the full road, in all time steps
            x2d=np.vstack((x2d,road))
            carid2d=np.vstack((carid2d,car_id))
            colour3d = np.concatenate((colour3d, [colour]), axis=0)
        flowcount = flowcheck(road,length,flowcount)
        journeytime, looped, end = journeyt(journeytime,looped,end,road,length,car_id,j)


    #only plots or animates if condition is met
    if singleplot == True:
        singlesecondplot(x2d,length,min(11, len(x2d)-1),colour3d)
    if animation == True:
        animate(totaltime,vmax,length,road,event_prob,colour,car_id,Queues,skill,aggression)
    if multipleplot == True:
        multiplesecondplot(x2d,length,totaltime,colour3d,Queues)

    return(flowcount/time,number_cars/length,journeytime/number_cars)


if __name__ == "__main__":
    #seed can take "Random" or any integer value
    seed = 43

    #Queues can take any of 'False' (Regular cell automaton rules), 'Skill' (hesitant driving), 'Aggression' and 'Skill and Aggression'
    queues = 'False'
    Road_Length = 200
    Time = 100
    Number_of_Cars = 20
    Max_Velocity = 5
    Event_Probability = 0
    singleplot = False
    multipleplot = True
    animation = False


    flowcount, density, journeytime = simulate(Road_Length,Time,Number_of_Cars,Max_Velocity,Event_Probability,singleplot,multipleplot,animation,seed,queues)

    print("Flow per time step:", flowcount)
    print("Density:", density)
    print("Journey-time statistic:", journeytime)
