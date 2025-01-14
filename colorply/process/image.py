"""
Defines an Image, with its orientation, focal, symmetry.
"""

import numpy as np


class Image:
    """
    Define an image, with its name, channels, data, rotation and autocollimation.
    """

    def __init__(self, name="None", channel="None", data=np.array([[]]), R=np.eye(3),
                 S=np.transpose(np.array([0, 0, 0])), size=(4000, 3000)):
        self.name = name
        self.channel = channel
        self.data = data
        self.R = R
        self.S = S
        self.size = size
