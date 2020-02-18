import numpy as np
from util import Utility as Util


class KnuthShuffle:
    def __init__(self):
        self.s_box = 0
        self.inverse_s_box = 0

    def create_s_box(self, random):
        x = np.arange(256)

        for i in range(255, -1, -1):
            j = random.randint(0, 255)
            temp = x[i]
            x[i] = x[j]
            x[j] = temp

        x = np.reshape(x, (16, 16))
        self.s_box = np.empty((16, 16), dtype='object')

        for i in range(0, 16):
            for j in range(0, 16):
                self.s_box[i][j] = Util.convert_dec_to_hex(x[i][j])

        return self.s_box

    def create_inverse_s_box(self):
        self.inverse_s_box = np.empty((16, 16), dtype='object')

        for i in range(0, 16):
            for j in range(0, 16):
                value = self.s_box[i, j]
                row = int(value[0], 16)
                column = int(value[1], 16)
                self.inverse_s_box[row, column] = np.base_repr(i, 16) + np.base_repr(j, 16)

        return self.inverse_s_box
