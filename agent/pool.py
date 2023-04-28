class Pool:
    def __init__(self, tasks):
        self.tasks = tasks

    def get_task(self):
        if not self.tasks:
            return None
        return self.tasks.pop(0)
    
    def add_task(self, task):
        self.tasks.insert(0, task)

class DevPool(Pool):
    pass

class TesterPool(Pool):
    pass
