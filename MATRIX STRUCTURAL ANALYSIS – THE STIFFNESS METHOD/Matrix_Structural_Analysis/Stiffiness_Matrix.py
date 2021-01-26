class Stiffiness_Matrix():
    """
    This class initiate the stiffiness matrix on a local system of coordinates
    of a 2D structure. This means that, after been stablished all degrees of 
    freedom of a Frame, Truss or Grill (not supported), the structure has it's
    stiffiness determined.

    This class works better with it's child classes, since more relevante 
    attributes are incorporated.

    Inputs:
        - length: length of each bar of the structure
        - orientation_degrees: starting on the first quadrant, it's the 
        direction of each bar
        - incidence_list: list that represents where each node of the beam land
        on each degree of freedom. It takes 4 arguments for a Truss and 6 for a
        Frame
        - EA: (optional, default=0) Young’s modulus * Area of a section of the 
        bar (supposed constant)
    	- EI: (optional, default=0) Young’s modulus * Inertia's Moment of a 
        section of the bar (supposed constant)

    Attributes:
        - l: gives the length of the bar
        - orientation: gives the direction of the bar on degrees
        - incidence: shows the incidence list of the bar

    """

    def __init__(self, length, orientation_degrees , incidence_list, EA = 0, EI = 0):
        self.l =  length
        self.orientation = orientation_degrees
        self.incidence = incidence_list
