"""
Model celého prstu složeného z několika článků
"""

import numpy as np
from geometry.segment import Segment

class Finger:
    def __init__(self, segments):
        """
        :param segments: seznam objektů Segment
        """
        self.segments = segments

    def get_joint_angles(self):
        """Vrátí seznam úhlů kloubů"""
        return [seg.angle for seg in self.segments]

    def get_tip_position(self):
        """
        Vypočítá polohu špičky prstu v rovině
        """
        x, y = 0.0, 0.0
        total_angle = 0.0

        for seg in self.segments:
            total_angle += seg.angle
            x += seg.length * np.cos(total_angle)
            y += seg.length * np.sin(total_angle)

        return x, y

    def get_joint_positions(self):
        """Vrátí souřadnice všech kloubů (včetně báze a špičky)."""
        positions = [(0.0, 0.0)]
        x, y = 0.0, 0.0
        total_angle = 0.0

        for seg in self.segments:
            total_angle += seg.angle
            x += seg.length * np.cos(total_angle)
            y += seg.length * np.sin(total_angle)
            positions.append((x, y))

        return positions
