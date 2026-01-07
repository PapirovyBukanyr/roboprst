"""
Model pneumatického svalu
"""

class PneumaticMuscle:
    def __init__(self, max_force, max_pressure):
        """
        :param max_force: maximální síla [N]
        :param max_pressure: maximální tlak [Pa]
        """
        self.max_force = max_force
        self.max_pressure = max_pressure
        self.pressure = 0.0

    def set_pressure(self, pressure):
        """Nastaví tlak ve svalu"""
        self.pressure = min(max(0.0, pressure), self.max_pressure)

    def compute_force(self):
        """Převede tlak na sílu"""
        return self.max_force * (self.pressure / self.max_pressure)
