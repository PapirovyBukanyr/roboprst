"""
Kinematické výpočty
"""

def integrate(segment, torque, dt):
    """
    Integruje pohyb článku (Euler)
    """
    segment.angular_acceleration = torque / segment.inertia
    segment.angular_velocity += segment.angular_acceleration * dt
    segment.angle += segment.angular_velocity * dt
