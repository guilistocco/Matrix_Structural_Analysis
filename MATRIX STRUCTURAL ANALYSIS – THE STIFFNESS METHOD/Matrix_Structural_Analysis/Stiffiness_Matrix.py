class Stiffiness_Matrix():
    """

    """

    def __init__(self, length, orientation_degrees , incidence_list, EA = 0, EI = 0):
        self.l =  length
        self.orientation = orientation_degrees
        self.incidence = incidence_list
