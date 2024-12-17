"""
This program explores I/O-Bound and CPU-Bound Task Performance Using Multiprocessing.
Author: Rahul Kumar
Date: September 20, 2024
"""

import multiprocessing
import os
import time
import random  # For simulating dynamic I/O delays
import psutil  # For measuring CPU usage

# A function to simulate I/O-bound task with a system call (simulates waiting for I/O)
def io_bound_system_call_worker(name):
    print("Demonstrating an I/O-bound task")
    print(f"Process {name} (PID: {os.getpid()}) is starting (I/O-bound task)...")

    # TODO-1:
    # 1- Print "Process {name} is entering system mode by a system-call"
    print(f"Process {name} is entering system mode by a system-call")

    # 2- Check the type of operating system. If it’s posix, assume Unix-like (Linux, macOS).
    # If not, assume Windows.
    system_type = os.name  # This checks the OS type.
    if system_type == 'posix':
        print(f"Process {name}: Detected Unix-like OS (POSIX compliant).")
    else:
        print(f"Process {name}: Detected Windows OS.  ")

    # 3- Execute a system shell command to list directory
    print(f"Process {name} is listing the current directory contents...")
    os.system("ls" if system_type == 'posix' else "dir")

    # TODO-2:
    # 4- Print "Process {name} is waiting for more I/O simulated by sleep"
    print(f"Process {name} is waiting for more I/O simulated by sleep")

    # 5- Delay the process for 5 seconds
    # Original code: time.sleep(5)
    io_wait_time = random.uniform(1, 5)  # Simulating random I/O wait times (1 to 5 seconds)
    time.sleep(io_wait_time)  # Dynamic delay for simulating I/O completion

    # 6- Print "Process {name} with PID {pid} has finished I/O-bound task"
    print(f"Process {name} with PID {os.getpid()} has finished I/O-bound task")

# A function to simulate CPU-bound task (no waiting for I/O)
def cpu_bound_task(name):
    print("Demonstrating a CPU-bound task")

    # TODO-3:
    # 7- Print "Process {name} with PID {pid} is starting CPU-bound task..."
    print(f"Process {name} with PID {os.getpid()} is starting CPU-bound task...")

    # 8- Calculate the sum of all integers from 1 to 10^6 − 1
    result = sum(range(1, 10 ** 6))

    # 9- Print "Process {name} with PID {pid} has finished CPU-bound task with result {result}"
    print(f"Process {name} with PID {os.getpid()} has finished CPU-bound task with result {result}")

if __name__ == "__main__":

    start_time = time.time()  # Start the timer

    # Question 3: Measure CPU utilization before running tasks
    # Original code did not measure CPU usage here
    # Added to measure initial CPU utilization
    initial_cpu = psutil.cpu_percent(interval=1)  # Capture initial CPU usage

    # Create a list to hold the process objects
    processes = []

    # Create I/O-bound processes with system call (simulating multiprogramming with I/O waits)
    # Original code: for i in range(2)  # Let's create 2 I/O-bound processes
    for i in range(5):  # Let's create 5 I/O-bound processes (adjusted for more I/O-bound processes for Q4)
        process = multiprocessing.Process(target=io_bound_system_call_worker, args=(f'IO-Worker-{i}',))

        # TODO-4:
        # 10- Append the process into processes
        processes.append(process)

        # 11- Start the I/O-bound process
        process.start()

    # Create CPU-bound processes (simulating CPU work)
    # Original code: for i in range(2)  # Let's create 2 CPU-bound processes
    for i in range(5):  # Let's create 5 CPU-bound processes (adjusted for more CPU-bound processes for Q4)

        # TODO-5:
        # 12- Create a CPU-bound process
        process = multiprocessing.Process(target=cpu_bound_task, args=(f'CPU-Worker-{i}',))

        # 13- Append the process into processes
        processes.append(process)

        # 14- Start the CPU-bound process
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()  # Ensure the main program waits for all processes to complete

    # Question 3: Measure CPU utilization after tasks complete
    # Original code did not measure CPU usage here
    # Added to measure final CPU utilization
    final_cpu = psutil.cpu_percent(interval=1)  # Capture final CPU usage

    # TODO-6
    # 15- Record the end-time of execution
    end_time = time.time()

    # 16- Print "All processes finished. Total execution time: {execution_time} seconds"
    print(f"All processes finished. Total execution time: {end_time - start_time} seconds")

    # Question 3: Print CPU utilization before and after
    # Original code did not print CPU usage changes
    # Added to display CPU utilization results
    print(f"Initial CPU usage: {initial_cpu}%")
    print(f"Final CPU usage: {final_cpu}%")
