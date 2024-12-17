from multiprocessing import Process, Queue
import time

"""
This program demonstrates IPC via message queue with multiple child processes.
Name: Rahul Kumar  
"""

def childProcess(q, process_number, num_messages):
    # A child process sends multiple messages to the queue
    for i in range(num_messages):
        message = f"Message {i+1} from child process {process_number}"
        q.put(message)  # Send message to the queue
        time.sleep(0.1)  # Simulate some delay

def parentProcess(num_children, num_messages):
    # Create a message queue to hold the messages
    q = Queue()

    # Create and start multiple child processes
    processes = []
    for i in range(num_children):
        p = Process(target=childProcess, args=(q, i+1, num_messages))
        processes.append(p)
        p.start()

    # Collect messages from the queue
    for _ in range(num_children * num_messages):
        print("Received:", q.get())

    # Wait for all child processes to finish
    for p in processes:
        p.join()

if __name__ == '__main__':
    #NOTE: Print your name and ID
    print("Hi, this is Rahul Kumar and 20349877")  # Add your name and student ID here

    # User inputs the number of child processes and messages per process
    num_children = int(input("Enter the number of child processes: "))
    num_messages = int(input("Enter the number of messages per child process: "))

    # Start the parent process
    parentProcess(num_children, num_messages)
