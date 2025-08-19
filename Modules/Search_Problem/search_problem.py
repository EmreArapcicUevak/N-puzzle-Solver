class Search_Problem():
  def __init__(self, initial_state):
    self.initial_state = initial_state

  def IS_GOAL(self, state):
    raise NotImplementedError("This method should be overridden by subclasses")
  
  def ACTIONS(self, state):
    raise NotImplementedError("This method should be overridden by subclasses")
  
  def RESULT(self, state, action):
    raise NotImplementedError("This method should be overridden by subclasses")

  def ACTION_COST(self, state, action, new_state):
    raise NotImplementedError("This method should be overridden by subclasses")