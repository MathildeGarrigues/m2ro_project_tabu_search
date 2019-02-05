import numpy as np 
import os
import flight

class Data:

    flights = []
    pb_data=dict()  #Dictionnary that contains number of flights N and gates M

    def read_instance(self, filename, N, P):
        # This file takes as an input the filename(.txt)
        #====== VARIABLES INITIALIZATION =====
        A=list()
        A_h=list()
        A_m=list()
        D=list()
        D_h=list()
        D_m=list()
        L0 = 0
        LNP1 = 0
        P = np.zeros(shape=(N,P), dtype=int) # change shape of P according to N and M
        n=0
        

        #====== Data File reading ======

        #filename = 'GAP5_25'  
                
        with open(filename+'.txt', 'r') as file:
            all_data = file.read()

        #====== Data formating ======    
        line = all_data.split("\n")  #corresponds to each line of the data file


        for i in range(len(line)):
            if i==0 or i==1 :
                temp = line[i].split(" ")
                self.pb_data[temp[0]]= temp[1]
            else:                           #contruction of vectors A, D and matrix P
                temp = line[i].split(" ")
                if len(temp) > 1:
                    A.append(temp[1])
                    D.append(temp[2])
                    for j in range(3, len(temp)-1):
                        P[n,int(temp[j])]=1
                    n+=1

        #====== Discrete time computation ======            
        for i in range(len(A)):
            A_split = str(A[i]).split(":")
            D_split = str(D[i]).split(":")
            A_h.append(A_split[0])
            A_m.append(A_split[1])
            D_h.append(D_split[0])
            D_m.append(D_split[1])
            A[i]= int(A_h[i])*12 + int(int(A_m[i])/5) 
            D[i]= int(D_h[i])*12 + int(int(D_m[i])/5) 

        L0 = int(A_h[0])*12
        LNP1 = (int(D_h[len(D)-1])+1) *12

        #======= Flight objects creation =======
        for i in range(int(self.pb_data["Flights"])):
            self.flights.append(flight.Flight())
            self.flights[i].number = i
            self.flights[i].arrival_time = A[i]
            self.flights[i].departure_time = D[i]
            self.flights[i].compatible_gates = P[i,:]

        return self.pb_data, self.flights


    def display_problem_data(self):
        """Affichage de la séquence d'avions à ordonnancer."""  
        print("*** Vols ***")
        for i in range(int(self.pb_data["Flights"])):
            print("Vol ", self.flights[i].number, 
                " : Heure d'arrivée = ", self.flights[i].arrival_time,
                " --- Heure de départ = ", self.flights[i].departure_time, 
                " --- Portes compatibles = ", self.flights[i].compatible_gates,
                " --- Porte assignée = ", self.flights[i].gate, sep="")



    def LIFO(self):
        """Heuristique 'dernier arrivé, dernier servi' pour une solution initiale"""
        sorted_flights = sorted(self.flights, key=lambda flight: flight.arrival_time, reverse=True)

        for i in range(int(self.pb_data["Flights"])):
            for g in range(int(self.pb_data["Gates"])):
                if sorted_flights[i].compatible_gates[g] == 1 :
                    last_flight = last_flight_assigned(sorted_flights, g)
                    print(last_flight)
                    if (last_flight==0) or (last_flight!=0 and sorted_flights[i].departure_time < last_flight.arrival_time):
                        sorted_flights[i].gate = g
                        sorted_flights[i].assigned = True
                        break


    def __init__(self, filename, N, P):
        # filename = 'GAP5_25'
        # N vols
        # P avions 

        self.read_instance(filename, N, P) 
        self.display_problem_data()
    

def last_flight_assigned(flights, gate):
    """ Renvoit le dernier avion affecté à la porte passée en argument """
    FlightsOnGate = []
    for i in range(len(flights)):
        if flights[i].gate == gate:
            FlightsOnGate.append(flights[i])
    
    FlightsOnGate = sorted(FlightsOnGate, key=lambda flight : flight.departure_time)
    if len(FlightsOnGate) == 0:
        return 0
    else:
        return FlightsOnGate[-1]