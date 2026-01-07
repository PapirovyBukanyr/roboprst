"""
Výpočet sil a momentů
"""

def tendon_torque(tension, moment_arm):
    """
    :param tension: tah provázku [N]
    :param moment_arm: rameno síly [m]
    """
    return tension * moment_arm
