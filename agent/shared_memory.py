class SharedMemory:
    def __init__(self, memory):
        self.memory = memory

    def get_last_memory(self):
        if (len(self.memory) > 0):
            return self.memory[-1]
        return []
