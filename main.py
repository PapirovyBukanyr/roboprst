"""
Vstupní bod programu
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from config import TIME_STEP
from geometry.segment import Segment
from geometry.finger import Finger
from actuation.tendon import Tendon
from actuation.pneumatic_muscle import PneumaticMuscle
from simulation.state import SimulationState
from simulation.simulation import Simulation
from physics.joint import JointParameters


def create_finger():
    segments = [
        Segment(length=0.028, mass=0.01, inertia=1e-5, flexor_moment_arm=0.006, extensor_moment_arm=0.008),
        Segment(length=0.028, mass=0.01, inertia=8e-6, flexor_moment_arm=0.006, extensor_moment_arm=0.008),
        Segment(length=0.024, mass=0.01, inertia=5e-6, flexor_moment_arm=0.006, extensor_moment_arm=0.008),
    ]
    joint_params = [
        JointParameters(angle_min=-0.1, angle_max=np.pi/2, viscous_friction=1e-4),
        JointParameters(angle_min=-0.1, angle_max=np.pi/3, viscous_friction=1.5e-4),
        JointParameters(angle_min=-0.1, angle_max=np.pi/3, viscous_friction=2e-4),
    ]
    for seg, jp in zip(segments, joint_params):
        seg.joint_params = jp

    return Finger(segments)


def simulate_motion(num_steps=20000, freq_hz=0.5):
    finger = create_finger()
    tendon_flexor = Tendon([0, 1, 2], direction=+1.0)
    tendon_extensor = Tendon([0, 1, 2], direction=-1.0)
    muscle_flexor = PneumaticMuscle(max_force=50, max_pressure=600000)
    muscle_extensor = PneumaticMuscle(max_force=30, max_pressure=600000)

    state = SimulationState(finger)
    sim = Simulation(state, [tendon_flexor, tendon_extensor])

    positions_over_time = []
    pressures = []

    for step in range(num_steps):
        current_time = step * TIME_STEP

        flex_pressure = 4000 + 250 * np.sin(2 * freq_hz * current_time)
        ext_pressure = 5000 + 250 * np.sin(2 * freq_hz * current_time + np.pi)

        muscle_flexor.set_pressure(flex_pressure)
        muscle_extensor.set_pressure(ext_pressure)

        tendon_flexor.set_tension(muscle_flexor.compute_force())
        tendon_extensor.set_tension(muscle_extensor.compute_force())

        sim.step()
        positions_over_time.append(finger.get_joint_positions())
        pressures.append((flex_pressure, ext_pressure))

    return finger, positions_over_time, pressures


def animate_finger():
    finger, positions_over_time, pressures = simulate_motion()

    total_length = sum(seg.length for seg in finger.segments)
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_xlim(-0.05, total_length + 0.02)
    ax.set_ylim(-total_length - 0.02, total_length + 0.02)
    ax.set_title("Pohyb prstu dle tlaku ve svalech")

    line, = ax.plot([], [], "-o", lw=2, color="tab:blue")
    pressure_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, va="top")

    def init():
        line.set_data([], [])
        pressure_text.set_text("")
        return line, pressure_text

    def update(frame):
        xs, ys = zip(*positions_over_time[frame])
        line.set_data(xs, ys)

        flex_p, ext_p = pressures[frame]
        pressure_text.set_text(
              f"Flexor: {flex_p:.4f} Pa\nExtensor: {ext_p:.4f} Pa"
        )

        return line, pressure_text

    interval_ms = TIME_STEP * 1000
    anim = FuncAnimation(
        fig,
        update,
        frames=len(positions_over_time),
        init_func=init,
        interval=interval_ms,
        blit=True,
        repeat=True,
    )

    plt.show()

    # Drží referenci na animaci, aby ji neuklidil GC při zobrazení
    return anim


if __name__ == "__main__":
    animate_finger()
