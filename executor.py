from concurrent.futures import ThreadPoolExecutor
import time

class TaskExecutor:
    def __init__(self, graph, event_manager):
        self.graph = graph
        self.event_manager = event_manager
        self.completed = set()

    def run(self):
        sorted_tasks = self.graph.topological_sort()

        with ThreadPoolExecutor() as executor:
            futures = {}

            for task_id in sorted_tasks:
                fn = self.graph.tasks[task_id]
                print(f"Ejecutando tarea: {task_id}")
                futures[task_id] = executor.submit(self.wrap_task, task_id, fn)

            for f in futures.values():
                f.result()

    def wrap_task(self, task_id, fn):
        fn()
        self.completed.add(task_id)
        self.event_manager.trigger("task_completed", task_id)
