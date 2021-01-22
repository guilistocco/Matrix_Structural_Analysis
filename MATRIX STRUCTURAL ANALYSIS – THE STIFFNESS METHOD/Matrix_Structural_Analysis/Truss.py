import numpy as np
import pandas as pd
from .Stiffiness_Matrix import Stiffiness_Matrix


class Truss(Stiffness_Matrix):
    """
    """
    def __init__(self, length, orientation_degrees , incidence_list, Deg_freedom, EA = 1):

        # list of attributes
        Stiffness_Matrix.__init__(self, length, orientation_degrees , incidence_list, EA)
        self.EA = EA
        self.DF = Deg_freedom
        self.orientation = orientation_degrees
        self.Stiff_M = np.array( [[1 ,0,-1,0],
                                   [0 ,0, 0,0],
                                   [-1,0, 1,0],
                                   [0 ,0, 0,0]] ) * (EA/length)

                                   
        self.local2global_T_M = np.array( [[np.cos(np.deg2rad(orientation_degrees)) ,np.sin(np.deg2rad(orientation_degrees)),0,0],
                            [-np.sin(np.deg2rad(orientation_degrees)) ,np.cos(np.deg2rad(orientation_degrees)), 0,0],
                            [0,0, np.cos(np.deg2rad(orientation_degrees)),np.sin(np.deg2rad(orientation_degrees))],
                            [0,0, -np.sin(np.deg2rad(orientation_degrees)),np.cos(np.deg2rad(orientation_degrees))]])
    

        rows = 4
        cols = Deg_freedom
        ones = [[incidence_list[0]-1], [incidence_list[1]-1], [incidence_list[2]-1], [incidence_list[3]-1]]

        INC = [ [ 0 for i in range(cols) ] for j in range(rows) ]

        for i,row in enumerate(ones):
            for col in row:
                INC[i][col] = 1
        self.Incidency_M = np.array(INC)


        self.Stiff_M_Global = self.local2global_T_M.transpose() @ self.Stiff_M @ self.local2global_T_M

        self.Stiff_M_Global_Spread = self.Incidency_M.transpose() @ self.Stiff_M_Global @ self.Incidency_M


    def updade_EA(self, new_EA):
        self.EA = new_EA