"""
Vector and application class for the 2D heat equation

Time integration methods:
   Forward Euler
   Backward Euler
   Crank-Nicolson
"""

import numpy as np
from scipy.sparse import diags
from scipy.sparse import identity
from scipy.sparse.linalg import spsolve
from typing import Callable, Union

from pymgrit.core.application import Application
from pymgrit.core.vector import Vector


class VectorHeat2D(Vector):
    """
    Vector class for the 2D heat equation
    """

    def __init__(self, nx, ny):
        """
        Constructor.

        :param nx: number of degrees of freedom in x-direction
        :param ny: number of degrees of freedom in y-direction
        """
        super(VectorHeat2D, self).__init__()
        self.nx = nx
        self.ny = ny
        self.values = np.zeros((self.nx, self.ny))

    def __add__(self, other):
        """
        Addition of two vector objects (self and other)

        :param other: vector object to be added to self
        :return: sum of vector object self and input object other
        """
        tmp = VectorHeat2D(self.nx, self.ny)
        tmp.set_values(self.get_values() + other.get_values())
        return tmp

    def __sub__(self, other):
        """
        Subtraction of two vector objects (self and other)

        :param other: vector object to be subtracted from self
        :return: difference of vector object self and input object other
        """
        tmp = VectorHeat2D(self.nx, self.ny)
        tmp.set_values(self.get_values() - other.get_values())
        return tmp

    def norm(self):
        """
        Norm of a vector object

        :return: 2-norm of vector object
        """
        return np.linalg.norm(self.values)

    def clone_zero(self):
        """
        Initialize vector object with zeros

        :rtype: vector object with zero values
        """
        return VectorHeat2D(self.nx, self.ny)

    def clone_rand(self):
        """
        Initialize vector object with random values

        :rtype: vector object with random values
        """
        tmp = VectorHeat2D(self.nx, self.ny)
        tmp.set_values(np.random.rand((self.nx, self.ny)))
        return tmp

    def set_values(self, values):
        """
        Set vector data

        :param values: values for vector object
        """
        self.values = values

    def get_values(self):
        """
        Get vector data

        :return: values of vector object
        """
        return self.values


class Heat2D(Application):
    """
    Application class for the heat equation in 2D space,
        u_t - a(u_xx + u_yy) = b(x,y,t),  a > 0,
        in [x_start, x_end] x [y_start, y_end] x (t_start, t_end],
    with homogeneous Dirichlet boundary conditions in space.
    """

    def __init__(self, x_start: float, x_end: float, y_start: float, y_end: float, nx: int, ny: int,
                 a: float, rhs: Callable = lambda x, y, t: 0 * x * y,
                 init_cond: Callable = lambda x, y: x * y * 0, method: str = 'BE',
                 bc_left: Union[int, float, Callable] = 0, bc_right: Union[int, float, Callable] = 0,
                 bc_bottom: Union[int, float, Callable] = 0, bc_top: Union[int, float, Callable] = 0, *args, **kwargs):
        """
        Constructor.

        :param x_start: left bound of x-domain
        :param x_end: right bound of x-domain
        :param y_start: left bound of y-domain
        :param y_end: right bound of y-domain
        :param nx: number of points in x-direction
        :param ny: number of points in y-direction
        :param a: thermal conductivity
        :param rhs: right-hand side
        :param init_cond: initial condition
        :param method: method for solving Dahlquist's equation:
                       'BE' -> Backward Euler (default)
                       'FE' -> Forwared Euler
                       'CN' -> Crank-Nicolson
        :param bc_left: boundary condition for left boundary
        :param bc_right: boundary condition for right boundary
        :param bc_bottom: boundary condition for bottom boundary
        :param bc_top: boundary condition for top boundary
        """
        super(Heat2D, self).__init__(*args, **kwargs)
        # Spatial domain (including boundary points)
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end
        self.x = np.linspace(x_start, x_end, nx)
        self.y = np.linspace(x_end, y_end, ny)
        self.x_2d = self.x[:, np.newaxis]
        self.y_2d = self.y[np.newaxis, :]
        self.nx = nx
        self.ny = ny
        self.dx = self.x[1] - self.x[0]
        self.dy = self.y[1] - self.y[0]

        # Thermal conductivity
        self.a = a

        # Set right-hand side routine
        self.rhs = rhs

        # Set time integration method
        if method == 'BE':
            self.theta = 1
        elif method == 'FE':
            self.theta = 0
        elif method == 'CN':
            self.theta = 0.5
        else:
            raise Exception("Unknown method. Choose BE (Backward Euler), FE (Forward Euler) or CN (Crank-Nicolson")

        # Set Dirichlet boundary conditions
        if isinstance(bc_left, (float, int)):
            self.bc_left: Callable = lambda y: bc_left
        elif callable(bc_left):
            self.bc_left: Callable = bc_left
        else:
            raise Exception("Choose float, int or function for boundary condition bc_left")

        if isinstance(bc_right, (float, int)):
            self.bc_right: Callable = lambda y: bc_right
        elif callable(bc_right):
            self.bc_right: Callable = bc_right
        else:
            raise Exception("Choose float, int or function for boundary condition bc_right")

        if isinstance(bc_bottom, (float, int)):
            self.bc_bottom: Callable = lambda x: bc_bottom
        elif callable(bc_bottom):
            self.bc_bottom: Callable = bc_bottom
        else:
            raise Exception("Choose float, int or function for boundary condition bc_bottom")

        if isinstance(bc_top, (float, int)):
            self.bc_top: Callable = lambda x: bc_top
        elif callable(bc_top):
            self.bc_top: Callable = bc_top
        else:
            raise Exception("Choose float, int or function for boundary condition bc_top")

        # Set (spatial) identity matrix and spatial discretization matrix
        self.space_disc = self.compute_matrix()
        self.identity = identity(self.nx * self.ny, dtype='float', format='csr')

        # Set the data structure for any user-defined time point
        self.vector_template = VectorHeat2D(self.nx, self.ny)

        # Set initial condition
        self.init_cond = init_cond
        self.vector_t_start = VectorHeat2D(self.nx, self.ny)
        self.vector_t_start.set_values(self.init_cond(self.x_2d, self.y_2d))

    def compute_matrix(self):
        """
        Define spatial discretization matrix for 2D heat equation

        Second-order central finite differences with matrix stencil
            [          -f_y          ]
            [-f_x  2(f_x + f_y)  -f_x]
            [          -f_y          ]
        with f_x = (a / dx^2) and f_y = (a / dy^2)
        """
        fx = self.a / self.dx ** 2
        fy = (self.a / self.dy ** 2)
        n = self.nx * self.ny

        main = np.ones(n) * (2 * (fx + fy))
        main[:self.nx] = main[-self.nx:] = 0
        main[self.nx::self.nx] = main[2 * self.nx - 1::self.nx] = 0

        upper = np.ones(n - 1) * (-fx)
        upper[:self.nx] = upper[-self.nx:] = 0
        upper[self.nx::self.nx] = upper[2 * self.nx - 1:: self.nx] = 0

        lower = np.ones(n - 1) * (-fx)
        lower[:self.nx - 1] = lower[-self.nx:] = 0
        lower[self.nx - 1::self.nx] = lower[2 * self.nx - 2:: self.nx] = 0

        upper2 = np.ones(n - self.nx) * (-fy)
        upper2[:self.nx] = 0
        upper2[self.nx::self.nx] = upper2[2 * self.nx - 1:: self.nx] = 0

        lower2 = np.ones(n - self.nx) * (-fy)
        lower2[-self.nx:] = 0
        lower2[::self.nx] = lower2[self.nx - 1::self.nx] = 0

        matrix = diags(diagonals=[main, lower, upper, lower2, upper2],
                       offsets=[0, -1, 1, -self.nx, self.nx],
                       shape=(n, n), format='csr')
        return matrix

    def compute_rhs(self, u_start: np.ndarray, t_start: float, t_stop: float):
        """
        Right-hand side of spatial system for implicit time integratio nmethods

        :param u_start: approximate solution for the input time t_start
        :param t_start: time associated with the input approximate solution u_start
        :param t_stop: time to evolve the input approximate solution to
        :return: right-hand side of spatial system at each time step in case of implicit time integration
        """

        # Set boundary conditions
        b = np.zeros((self.nx, self.ny))

        b[0, :] = self.bc_left(self.y_2d)
        b[-1, :] = self.bc_right(self.y_2d)
        b[:, 0] = self.bc_bottom(self.x_2d)
        b[:, -1] = self.bc_top(self.x_2d)

        if self.theta == 1:
            # BE
            b[1:-1, 1:-1] = u_start[1:-1, 1:-1] + \
                            (t_stop - t_start) * self.rhs(x=self.x_2d[1:-1], y=self.y_2d[:, 1:-1], t=t_stop)
        else:
            # CN: theta = 1/2
            tmp = (self.identity - self.theta * (t_stop - t_start) * self.space_disc) * u_start.flatten()
            b += tmp.reshape(self.ny, self.nx).T

            # add RHS of PDE
            b[1:-1, 1:-1] += self.theta * (t_stop - t_start) * self.rhs(x=self.x_2d[1:-1], y=self.y_2d[:, 1:-1],
                                                                        t=t_stop) + \
                             (1 - self.theta) * (t_stop - t_start) * self.rhs(x=self.x_2d[1:-1], y=self.y_2d[:, 1:-1],
                                                                              t=t_start)

        return b.T.flatten()

    def step(self, u_start: VectorHeat2D, t_start: float, t_stop: float) -> VectorHeat2D:
        """
        Time integration routine for 2D heat equation example problem:
            Backward Euler (BE)
            Forward Euler (FE)
            Crank-Nicolson (CN)

        One-step method
           (u_i - u_{i-1})/dt + (theta*L*u_i + (1-theta)*L*u_{i-1} = theta*b_i + (1-theta)*b_{i-1},
        where L = self.space_disc is the spatial discretization operator and
           theta =  0  -> FE
           theta = 1/2 -> CN
           theta =  1  -> BE

        :param u_start: approximate solution for the input time t_start
        :param t_start: time associated with the input approximate solution u_start
        :param t_stop: time to evolve the input approximate solution to
        :return: approximate solution at input time t_stop
        """
        if self.theta == 0:
            # FE
            old = u_start.get_values()
            new = np.zeros((self.nx, self.ny))

            # Set BCs
            new[0, :] = self.bc_left(self.y_2d)
            new[-1, :] = self.bc_right(self.y_2d)
            new[:, 0] = self.bc_bottom(self.x_2d)
            new[:, -1] = self.bc_top(self.x_2d)

            tmp = (self.identity - (t_stop - t_start) * self.space_disc) * old.flatten()
            new += tmp.reshape(self.nx, self.ny).T

            # add RHS of PDE
            new[1:-1, 1:-1] += (t_stop - t_start) * self.rhs(x=self.x_2d[1:-1], y=self.y_2d[:, 1:-1], t=t_start)

            new.T.flatten()

        else:
            # set up and solve linear system
            rhs = self.compute_rhs(u_start=u_start.get_values(), t_start=t_start, t_stop=t_stop)
            new = spsolve((t_stop - t_start) * self.theta * self.space_disc + self.identity, rhs)

        ret = VectorHeat2D(self.nx, self.ny)
        ret.set_values(new.reshape(self.ny, self.nx).T)
        return ret
