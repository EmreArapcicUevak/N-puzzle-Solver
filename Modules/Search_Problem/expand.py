from .node import Node
from .search_problem import Search_Problem

def expand(problem : Search_Problem, node : Node):
  state = node.state

  for action in problem.ACTIONS(state):
    new_state = problem.RESULT(state=state, action=action)

    cost = node.path_cost + problem.ACTION_COST(state = state, action = action, new_state = new_state)

    yield Node(new_state, parent=node, path_cost= cost)