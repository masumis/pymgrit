"""
Apply two-level MGRIT with F-relaxation
to solve Brusselator system, using RK4 time integration
"""

import pathlib
import numpy as np
import matplotlib.pyplot as plt

from pymgrit.brusselator.brusselator import Brusselator
from pymgrit.core.mgrit import Mgrit


def main():
    def output_fcn(self):
        # Set path to solution
        path = 'results/' + 'brusselator' + '/' + str(self.solve_iter)
        # Create path if not existing
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        # Save solution to file; here, we have two solution values at each time point.
        np.save(path + '/' + str(self.t[0][0]) + ':' + str(self.t[0][-1]),  # Local time interval
                [self.u[0][i] for i in self.index_local[0]])                # Save solution values at local time points

    # Create two-level time-grid hierarchy for the Brusselator system
    brusselator_lvl_0 = Brusselator(t_start=0, t_stop=12, nt=641)
    brusselator_lvl_1 = Brusselator(t_interval=brusselator_lvl_0.t[::20])

    # Set up the MGRIT solver using the two-level hierarchy and set the output function
    mgrit = Mgrit(problem=[brusselator_lvl_0, brusselator_lvl_1], output_fcn=output_fcn, output_lvl=2, cf_iter=0)

    # Solve Brusselator system
    infos = mgrit.solve()

    res = np.load('results/brusselator/' + str(len(infos['conv'])) + '/0.0:12.npy', allow_pickle=True)
    # Plot solution using member function of class VectorBrusselator
    for i in range(0, len(res)):
        res[i].plotSolution()
    plt.show()


if __name__ == '__main__':
    main()
