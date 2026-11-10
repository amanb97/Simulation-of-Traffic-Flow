import argparse
import random

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

from run_simulation import simulate


def fit_curve(function, x, y, sigma, p0=None):
    if np.any(np.asarray(sigma) == 0):
        print("Zero trial spread at one or more points; using an unweighted fit.")
        sigma = None
    try:
        return curve_fit(function, x, y, sigma=sigma, p0=p0, maxfev=10000)
    except RuntimeError as error:
        print(f"Fit did not converge: {error}. Showing the simulation points.")
        return None, None


def journeytimemax(trials, Event_Probability=0, seed='Random'):


    velocities = [1,2,3,4,5,6,7,8,9,10,11]
    singleplot = False
    multipleplot = False
    animation = False
    Road_Length = 200
    Time = 400
    Number_of_Cars = 20
    journeyarray = np.array([])
    journeyavg = np.array([])
    yerror = np.array([])
    queues = 'False'

    #Loops over all velocitites, and then uses a monte carlo sim to do x trials of the simulation
    #Calculates errors and averages for each velocity value
    for velocity in velocities:

        journeytotal = 0
        journeyarray = np.array([])

        for i in range(trials):
            flowcount, density, Journeytime = simulate(Road_Length,Time,Number_of_Cars,velocity,Event_Probability,singleplot,multipleplot,animation,seed,queues)
            journeyarray = np.append(journeyarray,Journeytime)
            journeytotal = np.sum(journeyarray)
            journeystd = np.std(journeyarray)

        yerror = np.append(yerror,journeystd)
        journeyavg = np.append(journeyavg,journeytotal/trials)
    return(velocities,journeyavg,yerror)


#used to fit
def inverse(x,a,b):
    return a/x+b
#used for derivative of fit
def derivativeinverse(x,a,b):
        return -a/((x+b)**2)


def inverse2(x,a,b,c):
    return ((a/(-x+b))+c)


def derivativeinverse2(x,a,b):
    return -a/((x-b)**2)


def plot_journeytimemax(trials):
    V_max_array, Journey_Time_array,yerror = journeytimemax(trials)

    popt, pcov = fit_curve(inverse, V_max_array, Journey_Time_array, sigma = yerror)


    if popt is not None:
        A, B = popt

        perrors = np.sqrt(np.diag(pcov))
        A_error, B_error = perrors

        xfit = np.linspace(min(V_max_array), max(V_max_array), 100)
        yfit = inverse(xfit,A,B)

        r_squared = r2_score(Journey_Time_array, inverse(V_max_array,A,B))

        derivative = derivativeinverse(xfit, A, B)


        print("R^2 = ", r_squared)
        print("A = ", A, "±", A_error)
        print("B = ", B, "±", B_error)
        print("average error", np.sum(yerror)/len(yerror))
        print(yerror)

    plt.figure(dpi=120)
    plt.grid()
    plt.scatter(V_max_array,Journey_Time_array,linestyle="None",marker="o")
    plt.errorbar(V_max_array, Journey_Time_array, yerr=yerror, fmt="o")
    if popt is not None:
        plt.plot(xfit, yfit, 'r-', label = "Inverse Function Fit")
    if popt is not None:
        plt.plot(xfit, derivative ,color = 'green',label = "Derivative")
    plt.xlabel(r"$v_{\mathrm{max}}$")
    plt.ylabel('Average Journey Time per Car')
    plt.yticks(np.linspace(-5, 10, 15))
    plt.xticks(np.linspace(0, 11, 12))
    if popt is not None:
        plt.legend()
    plt.title("Journey Time vs Maximum Velocity")
    plt.show()


def journeytimeevent(trials, seed='Random'):


    events = np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,86,87,88,89])
    singleplot = False
    multipleplot = False
    animation = False
    Road_Length = 200
    Time = 400
    Number_of_Cars = 20
    Max_Velocity = 5
    journeyarray = np.array([])
    journeyavg = np.array([])
    journeystd = np.array([])
    yerror = np.array([])
    queues = 'False'

    #Loops over all events, and then uses a monte carlo sim to do x trials of the simulation
    #Calculates errors and averages for each velocity value
    for event in events:

        journeytotal = 0
        journeyarray = np.array([])
        for i in range(trials):
            flowcount, density, Journeytime = simulate(Road_Length,Time,Number_of_Cars,Max_Velocity,event,singleplot,multipleplot,animation,seed,queues)
            journeyarray = np.append(journeyarray,Journeytime)
            journeytotal = np.sum(journeyarray)
            journeystd = np.std(journeyarray)
        journeyavg = np.append(journeyavg,journeytotal/trials)
        yerror = np.append(yerror,journeystd)

    return(events,journeyavg,yerror)


def plot_journeytimeevent(trials):
    events, Journey_Time_array,yerror = journeytimeevent(trials)

    events=events/10
    popt, pcov = fit_curve(inverse2, events, Journey_Time_array,p0=[80,90,3],sigma=yerror)


    if popt is not None:
        A, B, C= popt

        perrors = np.sqrt(np.diag(pcov))
        A_error, B_error,C_error = perrors

        xfit = np.linspace(min(events), max(events), 100)
        yfit = inverse2(xfit,A,B,C)

        r_squared = r2_score(Journey_Time_array, inverse2(events,A,B,C))

        derivative2 = derivativeinverse2(xfit, A, B)

        print("R^2 = ", r_squared)
        print("A = ", A, "±", A_error)
        print("B = ", B, "±", B_error)
        print("C = ", C, "±", C_error)
        print("average error", np.sum(yerror)/len(yerror))
        print(yerror)

    plt.figure(dpi=120)

    plt.grid()
    plt.scatter(events,Journey_Time_array,linestyle="None",marker="o")
    if popt is not None:
        plt.plot(xfit, yfit, 'r-',label = "Inverse Function Fit")
    plt.errorbar(events, Journey_Time_array, yerr=yerror, fmt="o")
    plt.gca().invert_xaxis()
    plt.xlabel('Event Probability (p)')
    plt.ylabel('Average Journey Time per Car (T)')
    plt.yticks(np.linspace(-10, 15, 26))
    plt.xticks(np.linspace(10, 1, 10))
    if popt is not None:
        plt.plot(xfit, derivative2 ,color = 'green',label = "Derivative")
    if popt is not None:
        plt.legend()
    plt.title("Journey Time vs Event Probability")

    plt.show()


def journeytimemultiple(trials, seed='Random'):


    velocities = np.array([4,5,6,7,8])
    singleplot = False
    multipleplot = False
    animation = False
    Road_Length = 200
    Time = 400
    Number_of_Cars = 20
    #colours for each individual velocity plot
    colourarray = ['b','g','r','c','m']
    #index is used to iterate the colours
    index=0
    queues = 'False'
    plt.figure(dpi=120)
    plt.grid()

    #Loops over all events, and then uses a monte carlo sim to do x trials of the simulation
    #Calculates errors and averages for each velocity value
    #Then loops over all velocities to get 5 different plots for different velocity values
    for velocity in velocities:
        events = np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,82,84,86,88,89])
        journeyarray = np.array([])
        journeyavg = np.array([])
        journeystd = np.array([])
        yerror = np.array([])
        for event in events:

            journeytotal = 0
            journeyarray = np.array([])
            for i in range(trials):
                flowcount, density, Journeytime = simulate(Road_Length,Time,Number_of_Cars,velocity,event,singleplot,multipleplot,animation,seed,queues)
                journeyarray = np.append(journeyarray,Journeytime)
                journeytotal = np.sum(journeyarray)
                journeystd = np.std(journeyarray)
            journeyavg = np.append(journeyavg,journeytotal/trials)
            yerror = np.append(yerror,journeystd)
        events = events/10
        popt, pcov = fit_curve(inverse2, events, journeyavg,p0=[10,10,3],sigma = yerror)

        colour = colourarray[index]
        index +=1
        if popt is None:
            plt.errorbar(events, journeyavg, yerr=yerror, fmt="o", color=colour, label=str(velocity))
            plt.legend(title=r"$v_{\mathrm{max}}$")
            continue
        A, B, C= popt
        perrors = np.sqrt(np.diag(pcov))
        A_error, B_error,C_error = perrors

        xfit = np.linspace(min(events), max(events), 100)
        yfit = inverse2(xfit,A,B,C)

        r_squared = r2_score(journeyavg, inverse2(events,A,B,C))

        label = str(velocity)
        plt.plot(xfit, yfit,color = colour , label = label)
        plt.legend(title = r"$v_{\mathrm{max}}$")
        plt.errorbar(events, journeyavg, yerr=yerror,fmt = 'o',color = colour)
        print("For a maximum velocity of ",velocity,":")
        print("R^2 = ", r_squared)
        print("A = ", A, "±", A_error)
        print("B = ", B, "±", B_error)
        print("C = ", C, "±", C_error)
    plt.xlabel('Event Probability (p/10)')
    plt.ylabel('Average Journey Time per Car (T)')
    plt.gca().invert_xaxis()
    plt.title("Journey Time vs Event Probability (Changing Max Velocity)")
    plt.yticks(np.linspace(0, 14, 15))
    plt.xticks(np.linspace(9, 1, 9))
    return(events,journeyavg,yerror)


def flowvsdensity(numbersteps,trials,Event_Probability=0):

    #number_cars_steps = int((Road_Length/numbersteps)) * np.arange(1,numbersteps)

    singleplot = False
    multipleplot = False
    animation = False
    seed = 'Random'
    queues = 'False'
    Time = 200
    Max_Velocity = 5
    Road_Length = 200
    colourarray = ['b','g','r','c','m']
    index=0
    queues = ['False','Skill','Aggression']
    labels = ['Normal','Hesitant','Aggressive']
    plt.figure(dpi=120)
    plt.grid()
    #Loops over all queue types, and then uses a monte carlo sim to do x trials of the simulation
    #Calculates errors and averages for each velocity value
    #Then loops over all velocities to get 5 different plots for different velocity values
    for queue in queues:
        number_cars_steps=[5,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80,84,88,92,95,100,110,120,130,140,150,160,170,180,190]
        flowavg = np.array([])
        densearray = np.array([])
        flow = np.array([])
        yerror = np.array([])
        for number in number_cars_steps:
            flowtotal = 0
            flow = np.array([])
            for i in range(trials):
                flowcount, density, journeytime = simulate(Road_Length,Time,number,Max_Velocity,Event_Probability,singleplot,multipleplot,animation,seed,queue)
                flow = np.append(flow,flowcount)
                flowtotal = np.sum(flow)
                flowstd = np.std(flow)
            flowavg = np.append(flowavg,flowtotal/trials)
            densearray = np.append(densearray,density)
            yerror = np.append(yerror,flowstd)
        print(np.max(flowavg))
        colour = colourarray[index]

        def skew_gauss(x, amp, loc, stdev_left, stdev_right, offset):
            return offset + amp * np.where(x <= loc, np.exp(-(x - loc)**2 / (2 * stdev_left**2)), np.exp(-(x - loc)**2 / (2 * stdev_right**2)))


        popt, pcov = fit_curve(skew_gauss, densearray, flowavg,sigma = yerror)

        if popt is None:
            plt.errorbar(densearray, flowavg, yerr=yerror, fmt="o", color=colour, label=labels[index])
            plt.legend(title="Driving Style")
            index += 1
            continue
        amp, loc, stdev_left, stdev_right, offset = popt

        perrors = np.sqrt(np.diag(pcov))
        amp_error, loc_error, stdev_left_error, stdev_right_error, offset_error = perrors

        xfit = np.linspace(min(densearray), max(densearray), 100)
        yfit = skew_gauss(xfit, amp, loc, stdev_left, stdev_right, offset)
        plt.plot(xfit, yfit, label = labels[index],color = colour)
        plt.errorbar(densearray,flowavg, yerr=yerror, fmt="o",color = colour)
        plt.legend(title="Driving Style")

        index +=1
        r_squared = r2_score(flowavg, skew_gauss(densearray, amp, loc, stdev_left, stdev_right, offset))

        #print("A = ", A, "±", A_error)
        #print("B = ", B, "±", B_error)
        print("Driving Style:", queue)
        print("R^2 = ", r_squared)
        print("maximum of fit (from curve fit function)=",loc,amp)
        print("minimum of fit (from data)=",np.max(flowavg))
        print("average error", np.sum(yerror)/len(yerror))
        print("error",yerror)
    plt.xlabel('Density (N/L)')
    plt.ylabel('Traffic Flow per Time Step')
    plt.title("Traffic Flow vs Number Density of Cars")
    return(densearray,flowavg,yerror)


def flowpeak(numbersteps,trials,Road_Length=200):

    number_cars_steps = int((Road_Length/numbersteps)) * np.arange(1,numbersteps)
    number_cars_steps=[30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
    flowavg = np.array([])
    densearray = np.array([])
    flow = np.array([])
    yerror = np.array([])
    singleplot = False
    multipleplot = False
    animation = False
    Event_Probability = 0.2
    Max_Velocity = 5
    Time = 200
    Queues = 'False'
    seed = 'Random'
    for number in number_cars_steps:

        flowtotal = 0
        flow = np.array([])

        for i in range(trials):
            flowcount, density, journeytime = simulate(Road_Length,Time,number,Max_Velocity,Event_Probability,singleplot,multipleplot,animation,seed,Queues)
            flow = np.append(flow,flowcount)
            flowtotal = np.sum(flow)
            flowstd = np.std(flow)

        flowavg = np.append(flowavg,flowtotal/trials)
        densearray = np.append(densearray,density)
        yerror = np.append(yerror,flowstd)

    return(densearray,flowavg,yerror)


def plot_flowpeak(trials):
    numberdensity,averageflow,averageflowerror = flowpeak(10,trials)
    plt.figure(dpi=120)
    plt.grid()
    plt.scatter(numberdensity,averageflow,linestyle="None",marker="o")
    plt.errorbar(numberdensity,averageflow, yerr=averageflowerror, fmt="o")
    plt.xlabel('Density (N/L)')
    plt.ylabel('Traffic Flow per Time Step')
    plt.title("Traffic Flow vs Number Density of Cars (Peak)")
    plt.show()


def main():
    options = {
        "velocity": (plot_journeytimemax, 5),
        "events": (plot_journeytimeevent, 100),
        "multiple": (journeytimemultiple, 100),
        "density": (lambda trials: flowvsdensity(10, trials), 140),
        "peak": (plot_flowpeak, 100),
    }
    parser = argparse.ArgumentParser(description="Run one traffic-flow experiment.")
    parser.add_argument("experiment", choices=options)
    parser.add_argument("--trials", type=int, help="Number of runs at each setting.")
    parser.add_argument("--seed", type=int, help="Repeat a sweep with the same sequence of trials.")
    args = parser.parse_args()
    experiment, default_trials = options[args.experiment]
    trials = default_trials if args.trials is None else args.trials
    if trials < 1:
        parser.error("--trials must be at least 1")
    if args.seed is not None:
        random.seed(args.seed)
    experiment(trials)
    if args.experiment in ("multiple", "density"):
        plt.show()


if __name__ == "__main__":
    main()
