"""
Reprezentace jednoho článku prstu
"""

import numpy as np

class Segment:
    def __init__(self, length, mass, inertia, flexor_moment_arm=0.01, extensor_moment_arm=0.01):
        """
        :param length: délka článku [m]
        :param mass: hmotnost článku [kg]
        :param inertia: moment setrvačnosti [kg*m^2]
        :param flexor_moment_arm: vzdálenost flexorového provázku od osy kloubu [m]
        :param extensor_moment_arm: vzdálenost extensorového provázku od osy kloubu [m]
        """
        self.length = length
        self.mass = mass
        self.inertia = inertia
        self.flexor_moment_arm = flexor_moment_arm
        self.extensor_moment_arm = extensor_moment_arm

        # Stavové proměnné
        self.angle = 0.0           # úhel vůči předchozímu článku [rad]
        self.angular_velocity = 0.0
        self.angular_acceleration = 0.0
        
        # Parametry kloubu (limity úhlu a tření), nastavuje se zvenku
        self.joint_params = None
