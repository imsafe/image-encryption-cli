import numpy as np


class Slicer:
    def __init__(self, array, height, width):
        self.array = array
        self.height = height
        self.width = width

    def set_array(self, array):
        self.array = array

    def slice(self):
        mid_of_height = int(self.height / 2)
        mid_of_width = int(self.width / 2)

        top_left = self.array[:mid_of_height, :mid_of_width]
        top_right = self.array[:mid_of_height, mid_of_width:self.width]
        bottom_left = self.array[mid_of_height:self.height, :mid_of_width]
        bottom_right = self.array[mid_of_height:self.height, mid_of_width:self.width]

        return top_left, top_right, bottom_left, bottom_right

    @staticmethod
    def concatenate(en_image_top_left, en_image_top_right, en_image_bottom_left, en_image_bottom_right):
        top = np.concatenate((en_image_top_left, en_image_top_right), 1)
        bottom = np.concatenate((en_image_bottom_left, en_image_bottom_right), 1)
        son = np.concatenate((top, bottom), 0)
        return son
