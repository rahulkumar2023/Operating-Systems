# “I confirm that this submission is my own work and is consistent with the Queen's regulations on Academic Integrity.”
"""
This program simulates a collaborative writing and editing environment using threading, where writers submit articles, and editors review them, managing access and synchronization to avoid race conditions and deadlocks.
Author: Rahul Kumar
Date: November 2, 2024
Student Number: 20349877
"""

import threading
import time
import random

# Constants for the number of writers, editors, and available review slots
NUM_WRITERS = 5  # Number of writers to simulate
NUM_EDITORS = 2  # Number of editors to simulate
NUM_SLOTS = 3  # Maximum simultaneous reviews

# Semaphore to manage available review slots
review_slots = threading.Semaphore(NUM_SLOTS)

# Lock to ensure one editor reviews an article at a time
editor_lock = threading.Lock()

# Lock to prevent overlapping print output
print_lock = threading.Lock()

# Shared variables to track the submission and review process
articles_submitted = 0  # Number of articles submitted
TOTAL_ARTICLES = NUM_WRITERS  # Total articles expected

# Event to signal that all articles are reviewed
stop_editors = threading.Event()


def writer_task(writer_id):
    """Simulates a writer drafting and submitting an article."""
    with print_lock:
        print(f"Writer {writer_id} is drafting an article.")

    # Simulate drafting time
    time.sleep(random.uniform(1, 2))

    with print_lock:  # console is a shared resource, so we need to lock it
        print(f"Writer {writer_id} is waiting for a review slot.")

    # TODO 1: Acquire the review slot before submission
    review_slots.acquire()

    with print_lock:  # console is a shared resource, so we need to lock it
        print(f"Writer {writer_id} has submitted an article for review.")

    # TODO 2: Safely update the shared variable `articles_submitted` tracking the number of submitted articles
    # Acquire the editor lock to ensure exclusive access to update shared variable `articles_submitted`
    editor_lock.acquire()

    # Mark this section as modifying a shared resource
    global articles_submitted  # Use the global variable to increment the count of submitted articles
    articles_submitted += 1  # Increment the counter for articles submitted

    # Release the editor lock after updating `articles_submitted`
    editor_lock.release()

    # Safely print the submission message using print_lock to prevent output overlap
    with print_lock:
        print(f"Writer {writer_id} has provided an article for submission.")

    # TODO 3: Release the review slot after submission
    review_slots.release()



def editor_task(editor_id):
    """Simulates an editor reviewing articles."""
    while not stop_editors.is_set():
        # Simulate the time before checking for an article
        time.sleep(random.uniform(0.5, 1.5))

        with print_lock:  # console is a shared resource, so we need to lock it
            print(f"Editor {editor_id} is checking for an article to review.")

        # TODO 4: Acquire the editor lock with a timeout to avoid deadlock
        # Attempt to acquire the editor lock with a random timeout to avoid deadlock
        received = editor_lock.acquire(timeout=random.uniform(0.1, 0.5))

        # Check if the lock was not acquired within the timeout period
        if not received:
            # If lock acquisition failed, print a message indicating a retry attempt
            with print_lock:
                print(f"Editor {editor_id} could not acquire lock. Trying once again.")

            # Continue to the next iteration of the loop to retry lock acquisition
            continue

        try:
            # TODO 5: Check if there are articles to review
            global articles_submitted
            if articles_submitted > 0:
                with print_lock:  # console is a shared resource, so we need to lock it
                    print(f"Editor {editor_id} is reviewing an article.")
                time.sleep(random.uniform(1, 3))  # Simulate review time

                with print_lock:  # console is a shared resource, so we need to lock it
                    print(f"Editor {editor_id} has finished reviewing an article.")

                # TODO 7: Safely decrement the number of submitted articles
                articles_submitted -= 1

                # TODO 8: Stop editors if all articles are reviewed
                if articles_submitted <= 0:
                    stop_editors.set()
        finally:
            # TODO 9: Ensure the editor lock is released
            editor_lock.release()
            '''
            pass  # TODO 10: Remove this line after adding the code
            '''

    with print_lock:
        print(f"Editor {editor_id} is stopping as all reviews are complete.")


def main():
    """Main function to initialize the simulation."""
    writer_threads = []
    for i in range(NUM_WRITERS):
        t = threading.Thread(target=writer_task, args=(i,))
        writer_threads.append(t)
        t.start()

    editor_threads = []
    for i in range(NUM_EDITORS):
        t = threading.Thread(target=editor_task, args=(i,))
        editor_threads.append(t)
        t.start()

    for t in writer_threads:
        t.join()

    for t in editor_threads:
        t.join()

    print("All articles have been submitted and reviewed.")


if __name__ == "__main__":
    main()
