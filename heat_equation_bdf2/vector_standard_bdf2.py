import numpy as np
from abstract_classes import vector
from scipy import linalg as la


class VectorStandardBDF2(vector.Vector):
    """
    """

    def __init__(self, size):
        super(VectorStandardBDF2, self).__init__()
        self.size = size
        self.vec_first_time_point = np.zeros(size)
        self.vec_second_time_point = np.zeros(size)

    def __add__(self, other):
        tmp = VectorStandardBDF2(self.size)
        tmp.vec_first_time_point = self.vec_first_time_point + other.vec_first_time_point
        tmp.vec_second_time_point = self.vec_second_time_point + other.vec_second_time_point
        return tmp

    def __sub__(self, other):
        tmp = VectorStandardBDF2(self.size)
        tmp.vec_first_time_point = self.vec_first_time_point - other.vec_first_time_point
        tmp.vec_second_time_point = self.vec_second_time_point - other.vec_second_time_point
        return tmp

    def norm(self):
        return la.norm(np.append(self.vec_first_time_point, self.vec_second_time_point))

    def clone_zeros(self):
        return VectorStandardBDF2(self.size)