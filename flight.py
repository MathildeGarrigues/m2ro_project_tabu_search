import numpy as np 
import os

class Flight:
    """Classe définissant un vol, caractérisé par :
    - son numéro
    - son heure d'arrivée
    - son heure de départ
    - les portes sur lesquelles il peut attérir
    - la date d'entrée à la porte qui lui est attribuée
    - la date de départ de la porte attribuée
    - la porte qui lui est attribuée"""


    def __init__(self):
        self.number = 0
        self.arrivalTime = int(0)
        self.departureTime = int(100)
        self.compatibleGates = []
        self.admissionTime = int(0)
        self.leavingTime = int(100)
        self.gate = int(9999)
        self.assigned = False
