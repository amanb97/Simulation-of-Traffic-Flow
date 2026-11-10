import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import numpy as np

from road import onesec


def singlesecondplot(Road2d,Length,second,Colour3d):
    #converts single x array into 1s and 0s, allowing the road to be plotted

    xaxis=np.array([])
    yaxis=np.array([])
    colourmap=np.empty((0,3))

    for i in range(Length):
        # If any road value is occupied, add it to the y array with its respective second and x array with relative position
        if Road2d[second][i] != -1:
            xaxis = np.append(xaxis,i)
            yaxis = np.append(yaxis,second)
        #Removes 0s in colour array, so colour can be fed to matplotlib
        if not np.array_equal(Colour3d[second][i], [0, 0, 0]):
            colourmap = np.vstack((colourmap,Colour3d[second][i]))

    plt.figure(dpi=120)
    plt.grid()
    plt.xlim(-0.1,Length+0.1)
    plt.scatter(xaxis,yaxis,linestyle="None",marker=">",c=np.clip(colourmap,0,1))
    plt.xlabel('Position')
    plt.ylabel('Time(s)')
    plt.title("Traffic Flow")
    plt.savefig("singlesecond.png")
    plt.show()
    return()

def singleframe(Road,Length,Colour):
    'To plot 1 frame, do plt.plot(singleplot(road)[0],singleplot(road)[1])'
    #converts single x array into 1s and 0s, allowing the road to be plotted
    #This function is specifically used for the animation
    xaxis=np.array([])
    yaxis=np.array([])
    colourmap=np.empty((0,3))

    for i in range(Length):
        if Road[i] != -1:
            xaxis = np.append(xaxis,i)
            yaxis = np.append(yaxis,1)
        if not np.array_equal(Colour[i], [0, 0, 0]):
            colourmap = np.vstack((colourmap,Colour[i]))

    return(xaxis,yaxis,colourmap)


def animate(Time,max_velocity,Length,Road,eventprob,Colour,Carid,Queues,Skill,Aggression):

    fig = plt.figure(200)
    metadata = dict(title='Movie', artist='Aman')
    writer = PillowWriter(fps=60,metadata=metadata)

    with writer.saving(fig,"traf.gif",100):
        for j in Time:
            plt.clf()
            plt.xlim(-0.1, Length + 0.1)
            plt.xlabel("Position")
            plt.ylabel("Time")
            plt.title("Time vs Position (Varying Driver Ability)")
            Road, Colour, Carid= onesec(Length,Road,max_velocity,eventprob,Colour,Carid,Queues,Skill,Aggression)
            position , time, colourmap = singleframe(Road,Length,Colour)
            plt.scatter(position,time,linestyle="None",marker=">",c=np.clip(colourmap,0,1))
            writer.grab_frame()
    return()

def multiplesecondplot(Road2d,Length,Time,Colour3d,Queues):
    #Converting x so that it plots time on the y, and position on the x with 1's and 0's
    xaxis=np.array([])
    yaxis=np.array([])
    colourmap=np.empty((0,3))

    #plots the line of cars for each second which is why we iterate over time
    for j in Time:
        #now we check each array which defines each second, and convert each array into 1's and 0s specifying the cars location
        for i in range(Length):
            #here we take the array defining the 1st second (j-1) and then iterate over each value in that are([i]) and any values that are occupied are added to the axis
            if Road2d[j-1][i] != -1:
                xaxis = np.append(xaxis,i)
                yaxis = np.append(yaxis,j)
            if not np.array_equal(Colour3d[j-1][i], [0, 0, 0]):
                colourmap = np.vstack((colourmap,Colour3d[j-1][i]))

    title = 0
    #chooses title based off of skill:
    if Queues == "False":
        title = "Time vs Position (Cell Automaton)"
    if Queues == "Skill":
        title = "Time vs Position (Hesitant Driving)"
    if Queues == "Aggression":
        title = "Time vs Position (Aggressive Driving)"
    if Queues == "Skill and Aggression":
        title = "Time vs Position (Hesitant and Aggressive Driving)"

    plt.figure(dpi=200)
    plt.grid()
    plt.xlim(-0.1,Length+0.1)
    #plt.scatter(xaxis,yaxis,linestyle="None",marker=">",s=5)
    plt.scatter(xaxis,yaxis,linestyle="None",marker=">",c=np.clip(colourmap,0,1),s=5)
    plt.xlabel('Position')
    plt.ylabel('Time')
    plt.title(title)
    plt.savefig("MultipleSecondPlot.png")
    plt.show()
    return()
