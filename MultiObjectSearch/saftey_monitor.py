


class Monitor:
    """
    An online monitor component checks saftey and liveness properties of the system:

    Saftey properties:
    
    GA (Agent.location != Wall)

    Liveness properties:

    F(Objects collected)

    
    """

    def __init__(self,grid) -> None:
        """
        grid : gridworld map
        """ 
        self.grid = grid

    def collision_avoidance(observation,action):
        """
        Check if the action will take the agent into a wall. 
        """
        pass

    def objects_collected(action):
        """
        check if the action  will 
        """
        pass

    def stuck(action):
        pass 

    def llm_response_guardrail(action):
        pass
