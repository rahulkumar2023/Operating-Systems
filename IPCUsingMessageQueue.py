from multiprocessing import Process, Queue
import time

"""
This program demonstrates IPC via message queue with multiple child processes.
Name: Rahul Kumar
"""

def childProcess(q):
    # NOTE: Minor change - add the process number in the message
    message = "Message from child process"
    q.put(message)  # Send message to the queue

def parentProcess():
    q = Queue()

    # Create and start a child process
    p = Process(target=childProcess, args=(q,))
    p.start()

    # Collect the message from the queue
    print("Received:", q.get())

    # Wait for the child process to finish
    p.join()

if __name__ == '__main__':
    # NOTE: Print your name and ID
    print("Hi, this is Rahul Kumar and 20349877")
    parentProcess()
