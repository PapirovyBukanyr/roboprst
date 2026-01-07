"""
Uchovává aktuální stav simulace
"""

class SimulationState:
    def __init__(self, finger):
        self.finger = finger
        self.time = 0.0
