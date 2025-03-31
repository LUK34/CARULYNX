# HACK-BASICS-PY

## 01_ErrorHandling.PY
- Teaches you how to handle error using try and except block

## 02_Threading.py
- This program demonstrates multithreading using Python's threading module.
- Two functions are executed concurrently using separate threads.
- 🔧 Function Definitions:
- print_number()
- Prints numbers from 1 to 5
- Waits 1 second between each print using time.sleep(1)
- print_letters()
- Prints letters from A to E
- Waits 1 second between each print using time.sleep(1)
- 🧵 Thread Creation:
- thread1 is created to run the print_number() function.
- thread2 is created to run the print_letters() function.
- ▶️ Thread Execution:
- Both threads are started using the .start() method.
- Since threads run simultaneously, the output is interleaved, showing both numbers and letters printed in a mixed order depending on the thread scheduler.

## 03_File_Write_Read.py
- This programme teaches you how to write the contexts to a file name `data.txt`.
- After writing the contents in that file, this programme will teach how to read the contents from that file.

## 04_ThreadExecutionPool.py
- concurrent.futures: Helps run tasks in parallel using threads or processes.
- time: Used to pause/sleep the program for a few seconds.
- random: Used to pick a random number (for sleep duration).
- threading: Lets you find the name of the current thread (worker).

- def task(name): The Task Function
- Defines a function called task that simulates some work.
- It gets the name of the current thread (worker) using threading.current_thread().name.
- It prints that the task has started and on which thread.
- Sleeps for 1 to 5 random seconds (to simulate work).
- Prints that the task is complete.
- Returns the number of seconds it slept.

- with concurrent.futures.ThreadPoolExecutor(max_workers=3, thread_name_prefix="Soldier") as executor:
- This is a Thread Pool Executor block
- Creates a pool of 3 threads (workers) that can run tasks in parallel.
- Each thread will be named like "Soldier_0", "Soldier_1", etc.
- executor is used to assign tasks to those threads.
- The with block makes sure threads are cleaned up after use.

- future_to_task = {executor.submit(task, i): i for i in range(1, 5)}
- This is a Dictionary Comprehension for submitting tasks
- Submits tasks task(1) to task(4) to the executor.
- executor.submit(task, i) sends the task to a worker thread and returns a future.
- future_to_task is a dictionary mapping each future to its task number i.
- This helps keep track of which result belongs to which task.

- for future in concurrent.futures.as_completed(future_to_task):
- Handling Completed Tasks
- Waits for the tasks to finish one by one, in the order they complete, not start.
- future is like a box that will contain the result of a task once it finishes.

- Getting the Result or Handling Exceptions
- task_name = future_to_task[future]: Gets the task number for that future.
- future.result():
- Returns the result of the task (i.e., how many seconds it slept).
- If the task raised an error, this will raise an exception.
- The result is printed, or the error is shown if there was one.



## 05_ProgressBar.py
- This imports the tqdm library, which is used to display a progress bar in the console for loops.
- It's especially helpful when running tasks that take time, like processing files, downloads, etc.

