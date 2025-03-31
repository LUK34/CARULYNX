import concurrent.futures
import time
import random
import threading

def task(name):
    thread_name = threading.current_thread().name
    print(f'Task {name} is running on {thread_name}\n')
    sleep_time = random.randint(1, 5)
    time.sleep(sleep_time)
    print(f'Task {name} completed after {sleep_time} seconds on {thread_name}\n')
    return sleep_time

with concurrent.futures.ThreadPoolExecutor(max_workers=3,thread_name_prefix="Soldier") as executor:
    future_to_task = {executor.submit(task,i) : i for i in range(1,5)} # This is a dictionary comprehension

    for future in concurrent.futures.as_completed(future_to_task):
        task_name=future_to_task[future]
        try:
            result=future.result()
            print(f"Task {task_name} completed successfully with result {result}")
        except Exception as e:
            print(f"Task {task_name} generated an exception:{e}")



