class Node():
  def __init__(self, state, parent = None, path_cost = 0):
    self.state = state
    self.parent = parent
    self.path_cost = path_cost
    self.depth = 0 if parent is None else parent.depth + 1

  def __str__(self):
    return f"|Node|  State: {self.state} | Parent: {self.parent.state if self.parent else None} | Path Cost: {self.path_cost}\n"

  def __eq__(self, value: object) -> bool:
    return self.state == value.state if isinstance(value, Node) else False

  def __repr__(self):
    return f"Node({self.state}, cost={self.path_cost})"

  def get_path(self):
    path = []
    current = self
    while current:
      path.append(current.state)
      current = current.parent

    return path[::-1]