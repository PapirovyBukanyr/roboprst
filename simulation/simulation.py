"""
Hlavní simulační smyčka
"""

from physics.kinematics import integrate
from physics.forces import tendon_torque
from config import TIME_STEP

class Simulation:
    def __init__(self, state, tendons):
        self.state = state
        self.tendons = tendons

    def step(self):
        """
        Jeden krok simulace
        """
        for i, segment in enumerate(self.state.finger.segments):
            torque = 0.0

            # vliv všech provázků
            for tendon in self.tendons:
                if i in tendon.attachment_points:
                    # Výběr ramene síly podle směru působení provázku
                    moment_arm = segment.flexor_moment_arm if tendon.direction > 0 else segment.extensor_moment_arm
                    torque += tendon.direction * tendon_torque(
                        tendon.tension,
                        moment_arm=moment_arm
                    )

            # Viskózní tření kloubu: brzdí pohyb úměrně úhlové rychlosti
            if segment.joint_params is not None:
                torque -= segment.joint_params.viscous_friction * segment.angular_velocity

            integrate(segment, torque, TIME_STEP)

            # Aplikace limitů úhlu kloubu a případné zastavení na dorazu
            if segment.joint_params is not None:
                jp = segment.joint_params
                if segment.angle < jp.angle_min:
                    segment.angle = jp.angle_min
                    segment.angular_velocity = 0.0
                    segment.angular_acceleration = 0.0
                elif segment.angle > jp.angle_max:
                    segment.angle = jp.angle_max
                    segment.angular_velocity = 0.0
                    segment.angular_acceleration = 0.0

        self.state.time += TIME_STEP
