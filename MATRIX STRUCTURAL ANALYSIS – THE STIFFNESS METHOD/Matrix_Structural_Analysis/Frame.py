import numpy as np
import pandas as pd
from .Stiffiness_Matrix import Stiffiness_Matrix


class Frame(Stiffness_Matrix):
    """
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
