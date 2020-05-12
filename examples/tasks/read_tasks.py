import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("ACCESS_KEY")
Config.secret_key = os.getenv("SECRET_KEY")

# Read all tasks
task_client = StaxClient("tasks")
all_tasks = task_client.ReadTasks()
print(all_tasks)

# Task Id in the response of a different StaxClient call
task_id = <Task Id>

# Get a specific task
task = task_client.ReadTask(task_id=task_id)
print(task)