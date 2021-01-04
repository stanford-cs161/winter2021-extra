# First, let's implement a simple FIFO queue.
class myQueue:
    def __init__(self):
        self.lst = []

    def push(self,x):
        self.lst.append(x)

    def pop(self):
        return self.lst.pop(0)
    
    def getList(self):
        return self.lst
    
