
import sys
import os

import random  # Import the random module for generating randomness

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from FIFO_Dynamic_Prio import FIFO_Dynamic_Prio


def possible_changes(fifo, n):
        """
        Returns a list of possible changes that can be made to the FIFO Dynamic Priority Queue.

        Args:
        - fifo: Instance of the FIFO_Dynamic_Prio class.
        - n: The number of machines (objects) to be considered in the simulation.

        Returns:
        - result: A list of tuples representing possible changes.
        """

        result = []  # List to store possible changes

        # Check if serving the next object is possible
        valid, next_serve = fifo.next_serve()
        if valid:
            result.append(("MCx", "serve next  "))  # Add the option to serve the next object

        # Simulate machines
        for i in range(1, n + 1):
            # Check if the object is in the queue
            idx_in_queue = -1  # Initialize index to -1 (not found)
            for j in range(fifo._queue_next_index):  # Iterate over the queue
                if fifo._queue[j] == f"MC{i}":  # Check if the object is in the queue
                    idx_in_queue = j  # Store the index if found
                    break

            # If the object is in the queue, add the option to dequeue it
            if idx_in_queue != -1:
                result.append((f"MC{i}", "dequeue     "))  # Add dequeue option
            else:
                result.append((f"MC{i}", "enqueue     "))  # Add enqueue option if it's not in the queue
            
            # If the object is in the queue, add the option to prioritise it
            if idx_in_queue != -1:
                result.append((f"MC{i}", "prioritise  "))  # Add prioritise option

                # Iterate through the heap and check if the object has already been prioritised
                for (queue_idx, prio) in fifo._heap:
                    if queue_idx - 1 == idx_in_queue:  # Check if the index matches the queue index
                        result.append((f"MC{i}", "deprioritise"))  # Add deprioritise option
                        break

        return result  # Return the list of possible changes


if __name__ == "__main__":
    
    object_cnt = 5  # Number of machines/objects to be simulated
    fifo = FIFO_Dynamic_Prio(object_cnt)  # Instantiate the FIFO Dynamic Priority Queue with the specified object count
    simulated_changes = 10000  # Number of simulated changes
    num_digits = len(str(simulated_changes))  # Number of digits for formatted output

    # Simulate the changes
    for i in range(simulated_changes):
        next_change = random.choice(possible_changes(fifo, object_cnt))  # Randomly select a possible change
        object, change = next_change
        match change:
            case "serve next  ":
                serve = fifo.serve()
            case "enqueue     ":
                fifo.enqueue_object(object)
            case "prioritise  ":
                fifo.prioritise_object(object, random.randint(1, 9))
            case "dequeue     ":
                fifo.dequeue_object(object)
            case "deprioritise":
                fifo.deprioritise_object(object)

        # Output the current status of the simulation
        print(str(i + 1).zfill(num_digits), f"{object}", change, "->", fifo)

    print(f"Done! - {simulated_changes} changes have been simulated.")  # Confirmation of completed simulation