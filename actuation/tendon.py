"""
Model provázku (tendonu)
"""

class Tendon:
    def __init__(self, attachment_points, direction=1.0):
        """
        :param attachment_points: seznam indexů článků, kde je provázek veden
        :param direction: směr působení momentu (+1 pro flexor, -1 pro extensor)
        """
        self.attachment_points = attachment_points
        self.direction = 1.0 if direction >= 0 else -1.0
        self.tension = 0.0  # aktuální tah [N]

    def set_tension(self, tension):
        """Nastavení tahu provázku"""
        self.tension = max(0.0, tension)
