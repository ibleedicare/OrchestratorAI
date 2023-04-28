import threading
import time

class DevPool:
    def __init__(self, tasks):
        self.tasks = tasks
    
    def get_task(self):
        if not self.tasks:
            return None
        return self.tasks.pop()

    def add_task(self, task):
        self.tasks.insert(0, task)

class TaskAdder(threading.Thread):
    def __init__(self, name, dev_pool):
        super().__init__()
        self.name = name
        self.dev_pool = dev_pool
        self.max_task = 10
        self.added_task = 0

    def run(self):
        while self.max_task > self.added_task:
            print(self.added_task)
            print(self.dev_pool.tasks)
            print("DEBUG: Added new task")
            self.dev_pool.add_task(f"New task {self.added_task}")
            self.added_task += 1
            time.sleep(3)

class DevAgentThread(threading.Thread):
    def __init__(self, name, dev_pool, duration):
        super().__init__()
        self.name = name
        self.dev_pool = dev_pool
        self.duration = duration

    def run(self):
        while True:
            print(f"DEBUG : {self.dev_pool.tasks}")
            task = self.dev_pool.get_task()
            if not task:
                print(f'{self.name}: No task available')
                time.sleep(1)
            print(f'{self.name}: Processing task {task}')
            time.sleep(self.duration)

tasks = [f'Task {i}' for i in range(1, 10)]
dev_pool = DevPool(tasks)

task_adder = TaskAdder('TaskAdder', dev_pool)
dev_agent_1_thread = DevAgentThread('Agent 1', dev_pool, 1)
dev_agent_2_thread = DevAgentThread('Agent 2', dev_pool, 2)

dev_agent_1_thread.start()
dev_agent_2_thread.start()
task_adder.start()

dev_agent_1_thread.join()
dev_agent_2_thread.join()
task_adder.join()

