from collections import defaultdict, deque

class TaskGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self.tasks = {}

    def add_task(self, task_id, task_fn):
        self.tasks[task_id] = task_fn
        self.in_degree[task_id] = self.in_degree.get(task_id, 0)

    def add_dependency(self, from_task, to_task):
        self.graph[from_task].append(to_task)
        self.in_degree[to_task] += 1

    def topological_sort(self):
        queue = deque([t for t in self.tasks if self.in_degree[t] == 0])
        sorted_tasks = []

        while queue:
            node = queue.popleft()
            sorted_tasks.append(node)

            for neighbor in self.graph[node]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_tasks) != len(self.tasks):
            raise Exception("Ciclo detectado en las dependencias.")

        return sorted_tasks
