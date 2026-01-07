"""
Joint parameterization: angle limits and friction per joint
"""

class JointParameters:
    def __init__(self, angle_min, angle_max, viscous_friction=0.0):
        """
        :param angle_min: minimum allowed angle [rad]
        :param angle_max: maximum allowed angle [rad]
        :param viscous_friction: viscous friction coefficient [N*m*s/rad]
        """
        self.angle_min = angle_min
        self.angle_max = angle_max
        self.viscous_friction = viscous_friction
