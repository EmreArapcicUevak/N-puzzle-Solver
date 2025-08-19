class Que():
  def __init__(self) -> None:
    self.que = []

  def pop(self):
    raise NotImplementedError("This method should be overridden by subclasses")
  
  def push(self, value):
    raise NotImplementedError("This method should be overridden by subclasses")
  
  def remove(self, value):
    self.que.remove(value)

  def __len__(self):
    return len(self.que)
  

class FIFO_Que(Que):
  def push(self, value):
    self.que.append(value)

  def pop(self):
    return self.que.pop(0)

class Priority_Que(Que):
  def __init__(self, evaluation_func):
    super().__init__()
    self.evaluation_func = evaluation_func # Returns true if element a has a higher prio then b

  def push(self, value):
    for index,que_value in enumerate(self.que):
      if self.evaluation_func(value) < self.evaluation_func(que_value):
        self.que.insert(index,value)
        return
    
    self.que.append(value)

  def pop(self):
    return self.que.pop(0)

class LIFO_Que(Que):
  def push(self, value):
    self.que.append(value)

  def pop(self):
    return self.que.pop()

# Alias
Stack = LIFO_Que