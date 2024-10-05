
import sys
import os

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from FIFO_Dynamic_Prio import FIFO_Dynamic_Prio


if __name__ == "__main__":
    # Create an instance of FIFO_Dynamic_Prio
    fifo_queue = FIFO_Dynamic_Prio(n=5)

    # Enqueue objects
    fifo_queue.enqueue_object("Task 1")
    fifo_queue.enqueue_object("Task 2")

    # Prioritize an object
    fifo_queue.prioritise_object("Task 2", prio=1)

    # Serve the next object
    valid, next_serve = fifo_queue.next_serve()
    if valid:
        print(f"Next to serve: {next_serve}")

    # Dequeue an object
    fifo_queue.dequeue_object("Task 1")