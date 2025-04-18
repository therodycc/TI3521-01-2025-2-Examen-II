from task_graph import TaskGraph
from executor import TaskExecutor
from events import EventManager
import time
import sys

def show_progress_bar(task_name, duration):
    print(f"{task_name} is starting...")
    bar_length = 40  # Length of the progress bar (number of characters)
    for i in range(bar_length + 1):
        time.sleep(duration / bar_length)
        progress = "░" * i
        spaces = " " * (bar_length - i)
        sys.stdout.write(f"\r[{progress}{spaces}] {int((i / bar_length) * 100)}%")
        sys.stdout.flush()
    print("\nTask completed!\n")

def generic_task(name, duration=3):
    def task():
        print(f"\n{'-'*50}")
        show_progress_bar(name, duration)
        print(f"{'='*50}")
        print(f"  {name} completed.\n")
        print(f"{'-'*50}\n")
    return task

# Setup
task_graph = TaskGraph()
event_manager = EventManager()

# Define Tasks with more realistic names and actions
task_graph.add_task("Data_Extraction", generic_task("Data Extraction"))
task_graph.add_task("Data_Cleaning", generic_task("Data Cleaning"))
task_graph.add_task("Model_Training", generic_task("Model Training"))
task_graph.add_task("Model_Evaluation", generic_task("Model Evaluation"))

# Define Task Dependencies
task_graph.add_dependency("Data_Extraction", "Data_Cleaning")  # Data Cleaning depends on Data Extraction
task_graph.add_dependency("Data_Cleaning", "Model_Training")  # Model Training depends on Data Cleaning
task_graph.add_dependency("Model_Training", "Model_Evaluation")  # Model Evaluation depends on Model Training

# Event Handling - On task completion
def on_task_completed(task_id):
    print(f"[Event] Task '{task_id}' has been successfully completed! Moving on to the next task...\n")

# Subscribe to task completion event
event_manager.subscribe("task_completed", on_task_completed)

# Execute the tasks
task_executor = TaskExecutor(task_graph, event_manager)
task_executor.run()
