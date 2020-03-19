try:
    import firedrake
except ImportError as e:
    import sys
    sys.exit("This examples requires firedrake. See https://pymgrit.github.io/pymgrit/coupling/firedrake.html")

import numpy as np

from mpi4py import MPI

from pymgrit.core.mgrit import Mgrit
from pymgrit.core.split import split_communicator
from pymgrit.core.application import Application
from pymgrit.core.vector import Vector

from firedrake import PeriodicSquareMesh
from firedrake import FunctionSpace, Constant, TestFunction, TrialFunction, Function, FacetNormal, inner, dx, grad, avg
from firedrake import outer, LinearVariationalProblem, NonlinearVariationalSolver, dS, exp, SpatialCoordinate


class VectorDiffusion2D(Vector):
    """
    Vector class for the 2D diffusion equation
    """

    def __init__(self, size):
        super(VectorDiffusion2D, self).__init__()
        self.size = size
        self.values = np.zeros(size)

    def __add__(self, other):
        tmp = VectorDiffusion2D(self.size)
        tmp.set_values(self.get_values() + other.get_values())
        return tmp

    def __sub__(self, other):
        tmp = VectorDiffusion2D(self.size)
        tmp.set_values(self.get_values() - other.get_values())
        return tmp

    def norm(self):
        return np.linalg.norm(self.values)

    def clone_zero(self):
        return VectorDiffusion2D(self.size)

    def clone_rand(self):
        tmp = VectorDiffusion2D(self.size)
        tmp.set_values(np.random.rand(self.size))
        return tmp

    def set_values(self, values):
        self.values = values

    def get_values(self):
        return self.values


class Diffusion2D(Application):
    """
    Class containing the description of the diffusion problem.

    The domain is given by the parameter mesh

    The initial condition is a Gaussian in the centre of the domain.

    The spatial discretisation is P1 DG (piecewise linear discontinous
    elements) and uses an interior penalty method which penalises jumps
    at element interfaces.
    """

    def __init__(self, mesh: object, kappa: float, mu: float = 5., *args, **kwargs):
        """
        Constructor
        :param mesh: domain
        :param kappa: the diffusion coefficient
        :param mu: the penalty weighting function
        :param args:
        :param kwargs:
        """
        super(Diffusion2D, self).__init__(*args, **kwargs)

        self.mesh = mesh
        V = FunctionSpace(self.mesh, "DG", 1)
        self.function_space = V

        # placeholder for timestep - will be updated in the update method
        self.dt = Constant(0.)

        # things we need for the form
        gamma = TestFunction(V)
        phi = TrialFunction(V)
        self.f = Function(V)
        n = FacetNormal(mesh)

        # set up the rhs and lhs of the equation
        a = (
                inner(gamma, phi) * dx
                + self.dt * (
                        inner(grad(gamma), grad(phi) * kappa) * dx
                        - inner(2 * avg(outer(phi, n)), avg(grad(gamma) * kappa)) * dS
                        - inner(avg(grad(phi) * kappa), 2 * avg(outer(gamma, n))) * dS
                        + mu * inner(2 * avg(outer(phi, n)), 2 * avg(outer(gamma, n) * kappa)) * dS
                )
        )
        L = inner(gamma, self.f) * dx

        # function to hold the solution
        self.soln = Function(V)

        # setup problem and solver
        prob = LinearVariationalProblem(a, L, self.soln)
        self.solver = NonlinearVariationalSolver(prob)

        # set initial condition
        self.vector_template = VectorDiffusion2D(len(self.function_space))
        self.vector_t_start = VectorDiffusion2D(len(self.function_space))

        # Setting up a Gaussian blob in the centre of the domain.
        x = SpatialCoordinate(self.mesh)
        initial_tracer = exp(-((x[0] - 5) ** 2 + (x[1] - 5) ** 2))
        tmp = Function(self.function_space)
        tmp.interpolate(initial_tracer)
        self.vector_t_start.set_values(np.copy(tmp.dat.data))

    def step(self, u_start: VectorDiffusion2D, t_start: float, t_stop: float) -> VectorDiffusion2D:
        """
        Performs one time step
        :param u_start: approximate solution for the input time t_start
        :param t_start: time associated with the input approximate solution u_start
        :param t_stop: time to evolve the input approximate solution to
        :return: approximate solution at input time t_stop
        """
        # compute backward Euler update
        self.dt.assign(t_stop - t_start)
        tmp = Function(self.function_space)
        for i in range(len(u_start.values)):
            tmp.dat.data[i] = u_start.values[i]
        self.f.assign(tmp)
        self.solver.solve()
        ret = VectorDiffusion2D(len(self.function_space))
        ret.set_values(np.copy(self.soln.dat.data))

        return ret


def main():
    # Split the communicator into space and time communicator
    comm_world = MPI.COMM_WORLD
    comm_x, comm_t = split_communicator(comm_world, 2)

    # The domain is a 10x10 square with periodic boundary conditions in each direction.
    n = 10
    mesh = PeriodicSquareMesh(n, n, 10, comm=comm_x)

    # Set up the problem
    diffusion0 = Diffusion2D(mesh=mesh, kappa=0.1, t_start=0, t_stop=10, nt=65)
    diffusion1 = Diffusion2D(mesh=mesh, kappa=0.1, t_start=0, t_stop=10, nt=17)
    diffusion2 = Diffusion2D(mesh=mesh, kappa=0.1, t_start=0, t_stop=10, nt=5)

    # Solve the problem, passing the space and time communicator to the MGRIT algorithm
    mgrit = Mgrit(problem=[diffusion0, diffusion1, diffusion2], comm_time=comm_t, comm_space=comm_x)
    info = mgrit.solve()


if __name__ == '__main__':
    main()