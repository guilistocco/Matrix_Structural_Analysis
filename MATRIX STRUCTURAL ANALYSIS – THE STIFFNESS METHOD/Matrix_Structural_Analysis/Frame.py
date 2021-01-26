import numpy as np
import pandas as pd
from .Stiffiness_Matrix import Stiffiness_Matrix


class Frame(Stiffness_Matrix):
    """
    A 2D Frame is a type of structure where there are no traction or 
    perpendicular (to the plane of the structures) forces are present

    This class receives as an inheritance the Stiffiness Matrix

    The sum of the stiffiness matrix (on the global system) of many bars
    returns the stiffiness matrix of the whole structure

    Inputs:
        - length: length of each bar of the structure
        - orientation_degrees: starting on the first quadrant, it's the 
        direction of each bar
        - incidence_list: list that represents where each node of the beam land
        on each degree of freedom. It takes 4 arguments for a Truss and 6 for a
        Frame
        - Deg_freedom: represents the number of degrees of freedom of the full
        structure, not only of the bar. It is 2*(number of nodes)
        - EA: (optional, default=1) Young’s modulus * Area of a section of the 
        bar (supposed constant)
    	- EI: (optional, default=1) Young’s modulus * Inertia's Moment of a 
        section of the bar (supposed constant)

    Attributes:
        - EA: returns the value of the attribute 
        - DF: returns the value of the attribute 
        - Stiff_M: returns the stiffiness matrix of the Truss, based on a
        template
        - local2global: returns the transformation matrix from the local 
        coordinates system to global
        - Incidency_M: returns the standard incidence matrix based on the
        incidence list and degrees of freedom. The shape is 6xDoF
        - Stiff_M_Global: returns the stiffiness matrix on the global system.
        Shape is 6x6
        - Stiff_M_Global_Spread: returns the stiffines matrix but considering
        the incidence matrix. This matrix show how one bar individualy 
        contributes to the stiffiness of the whole structure. Shape is DoFxDoF


        Heritage attributes:
        - l: gives the length of the bar
        - orientation: gives the direction of the bar on degrees
        - incidence: shows the incidence list of the bar

    Methods:
        - updade_EA: update the value of EA
        - updade_EI: update the value of EI
    """
    def __init__(self, length, orientation_degrees , incidence_list, Deg_freedom, EA = 1, EI = 1):
        # list of attributes
        Stiffness_Matrix.__init__(self, length, orientation_degrees , incidence_list, EA, EI)
        self.EA = EA
        self.EI = EI
        self.DF = Deg_freedom
        self.orientation = orientation_degrees
        self.Stiff_M = np.array( [[(EA/length),0 ,0,(-(EA/length)),0,0],
                                   [0 ,(12*EI/(length^3)), (6*EI/(length^2)),0,(-(12*EI/(length^3))),(6*EI/(length^2))],
                                   [0,(6*EI/(length^2)), (4*EI/(length)),0,-(6*EI/(length^2)),(2*EI/(length))],
                                   [-(EA/length),0 ,0,(EA/length),0,0],
                                   [0 ,(-(12*EI/(length^3))), (-(6*EI/(length^2))),0,(12*EI/(length^3)),(-(6*EI/(length^2)))],
                                   [0,(6*EI/(length^2)), (2*EI/(length)),0,(-(6*EI/(length^2))),(4*EI/(length))]
                                   ])

        self.local2global_T_M = np.array( 
                    [ [np.cos(np.deg2rad(orientation_degrees)) ,np.sin(np.deg2rad(orientation_degrees)),0,0,0,0],
                    [-np.sin(np.deg2rad(orientation_degrees)) ,np.cos(np.deg2rad(orientation_degrees)), 0,0,0,0],
                    [0,0,1,0,0,0],
                    [0,0,0, np.cos(np.deg2rad(orientation_degrees)) ,np.sin(np.deg2rad(orientation_degrees)),0],
                    [0,0,0,-np.sin(np.deg2rad(orientation_degrees)) ,np.cos(np.deg2rad(orientation_degrees)), 0],
                    [0,0,0,0,0,1] ]
                    )
        
        rows = 6
        cols = Deg_freedom
        ones = [[incidence_list[0]-1], [incidence_list[1]-1], [incidence_list[2]-1], [incidence_list[3]-1],[incidence_list[4]-1],[incidence_list[5]-1]]

        INC = [ [ 0 for i in range(cols) ] for j in range(rows) ]

        for i,row in enumerate(ones):
            for col in row:
                INC[i][col] = 1
        self.Incidency_M = np.array(INC)


        self.Stiff_M_Global = self.local2global_T_M.transpose() @ self.Stiff_M @ self.local2global_T_M

        self.Stiff_M_Global_Spread = self.Incidency_M.transpose() @ self.Stiff_M_Global @ self.Incidency_M

    # methods

    def updade_EA(self, new_EA):
        self.EA =  new_EA

    def updade_EI(self, new_EI):
        self.EI =  new_EI
