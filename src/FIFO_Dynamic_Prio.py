class FIFO_Dynamic_Prio():
    """
    A class that implements a FIFO (First In, First Out) queue with dynamic prioritization.
    It allows objects to be queued and their prioritization to be adjusted dynamically, 
    enabling preference for certain queued objects when necessary.

    Note: This class is not optimized for Python and is designed for universal 
    implementation, particularly in low-level programming environments.
    """

    def __init__(self, n):
        """
        Initializes the FIFO_Dynamic_Prio object.

        Parameters:
        ----------
        n : int
            The maximum number of elements that the queue, heap, and other internal
            structures will hold.
        """
        
        # The maximum number of elements (n) for the queue
        self.n = n

        # A queue initialized with zeros, where elements will be enqueued.
        # Its size is determined by the provided 'n'.
        self._queue = [0] * n

        # The index in _queue where the next element will be inserted.
        self._queue_next_index = 0

        # A list to track elements that are not in the heap.
        # Initialized with zeros, size is also 'n'.
        self._not_in_heap = [0] * n

        # The index in _not_in_heap where the next element will be inserted.
        self._not_in_heap_next_index = 0

        # A heap (used for prioritization) represented as a list of [index_in_queue (with offset of +1), priority] pairs.
        # Initialized with [0,0] pairs, size is 'n'.
        self._heap = [[0, 0] for _ in range(n)]

        # The index in _heap where the next element will be inserted.
        self._heap_next_index = 0

        # A stack to track recursive function calls. 
        # Initialized with zeros, size is 'n'.
        self._recursive_calls_stack = [0] * n

        # The index in _recursive_calls_stack where the next element will be inserted.
        self._recursive_calls_stack_next_index = 1
    
    def __str__(self):
        """
        Returns a string representation of the queue and heap, showing the current state of the queue, 
        heap elements, and the next object to be served.
        """
        # Building the queue representation
        s = "queue: ["
        s += ", ".join(str(element) if element not in [None, 0] else "___" for element in self._queue)
        s += "], heap: ["
        
        # Building the heap representation
        for idx in range(self.n):
            index, prio = self._heap[idx]
            if index > 0:
                element = self._queue[index - 1]
                s += f"[{element}, {prio}]"
            else:
                s += "[___, _]"
            
            if idx != self.n - 1:
                s += ", "
        
        # Representing the next object to be served
        s += "], next object: "
        
        valid, next_object = self.next_serve()
        if valid:
            s += str(next_object)
        else:
            s += "___"

        return s

    def enqueue_object(self, object):
        """
        Adds an object to the queue. 
        Note: The prioritization of the object must be set separately after enqueuing.

        Parameters:
        ----------
        object : any type
            The object to be added to the queue and tracked.
        """
        
        if self._queue_next_index < self.n:

            # Adds the object to the next available position in the queue.
            self._queue[self._queue_next_index] = object
            
            # Tracks the object in the _not_in_heap list (these are elements not yet added to the heap).
            self._not_in_heap[self._not_in_heap_next_index] = object
            
            # Increment the index for the queue to point to the next empty position.
            self._queue_next_index += 1
            
            # Increment the index for not_in_heap to point to the next position where a new element can be added.
            self._not_in_heap_next_index += 1

    def next_serve(self):
        """
        Returns a tuple indicating if the next object can be served and the object itself.
        
        The first element of the tuple is a boolean that indicates whether a valid object is available,
        and the second element is the object with the highest priority or 0 if none exists.
        
        Returns:
        -------
        tuple:
            (bool, object):
                A tuple where the first element indicates if a valid object is available, 
                and the second element is the object or 0 if no valid object is present.
        """
        
        # Check if the heap is not empty.
        if self._heap:
            # Check if the top of the heap contains a valid object (index and priority both non-zero).
            if self._heap[0][0] != 0 and self._heap[0][1] != 0:
                next_object_idx = self._heap[0][0]  # Get the index of the object in the queue.
                return (True, self._queue[next_object_idx - 1])  # Return True and the object from the queue.
        
        # If the heap is empty or has no valid objects, check the queue.
        if self._queue:
            first_object = self._queue[0]  # Get the first object in the queue.
            if first_object:  # Check if the first object is not None or equivalent.
                return (True, first_object)  # Return True and the first object from the queue.
        
        # Return False and 0 if no valid object is found.
        return (False, 0)  # Using 0 as a placeholder for no valid object.
    
    def serve(self):
        """
        Serves the next object with the highest priority from the queue.
        
        The object is removed from the queue after being served.
        
        Returns:
        -------
        object or None:
            The object that has been served, or None if there was no valid object to serve.
        """
        
        # Get the next object to serve based on priority.
        valid, next_object = self.next_serve()
        
        # If there is a valid object, dequeue it from the queue.
        if valid:
            self.dequeue_object(next_object)  # Remove the object from the queue.
        
        return next_object  # Return the served object (or None if there was no object).

    def dequeue_object(self, object):
        """
        Removes an object from the queue and updates related structures.
        
        The method searches for the object in the queue and the not-in-heap list,
        removes it from both if found, and updates the heap if necessary.
        
        Parameters:
        ----------
        object : any type
            The object to be removed from the queue and related structures.
        """
        
        # Initialize the variable to hold the index of the object in the queue.
        queue_index_of_object = -1
        
        # Check if there are any elements in the queue.
        if self._queue_next_index > 0:
            # Find the object in the queue.
            for i in range(self._queue_next_index):
                if self._queue[i] == object:
                    queue_index_of_object = i  # Store the index of the object.
                    # Shift elements to the left to remove the object.
                    for j in range(i, self._queue_next_index - 1):
                        self._queue[j] = self._queue[j + 1]
                    # Set the last position to 0 (empty).
                    self._queue[self._queue_next_index - 1] = 0
                    # Decrement the next index for the queue.
                    self._queue_next_index -= 1
                    break
            
            if queue_index_of_object != -1:
                # Flag to check if the object is in the heap.
                is_in_heap = True
                # Check if the object is in the not-in-heap list.
                for i in range(self._not_in_heap_next_index):
                    if self._not_in_heap[i] == 0:
                        break  # Stop at the first empty position.
                    if self._not_in_heap[i] == object:
                        is_in_heap = False  # Object is found in not-in-heap.
                        # Shift elements to the left to remove the object.
                        for j in range(i, self._not_in_heap_next_index - 1):
                            self._not_in_heap[j] = self._not_in_heap[j + 1]
                        # Set the last position to 0 (empty).
                        self._not_in_heap[self._not_in_heap_next_index - 1] = 0
                        # Decrement the next index for not-in-heap.
                        self._not_in_heap_next_index -= 1
                        break

                # If the object was not found in not-in-heap, check in the heap.
                if is_in_heap:
                    for i in range(self._heap_next_index):
                        # Check if the object is in the heap using its index (adjusted for 1-based index).
                        if self._heap[i][0] == queue_index_of_object + 1:
                            self._heap_remove(i)  # Remove the object from the heap.
                            break

                # If the object was in the queue, adjust heap indices for remaining objects.
                if queue_index_of_object < self._queue_next_index:
                    for i in range(self._heap_next_index):
                        # Decrement the index of heap elements that come after the removed object.
                        if self._heap[i][0] > queue_index_of_object:
                            self._heap[i][0] -= 1

    def prioritise_object(self, object, prio=1):
        """
        Assigns a priority to a queued object.
        
        This method first checks if the object is in the queue. If it is,
        it removes any existing priority for the object and then adds it
        to the heap with the specified priority.

        Parameters:
        ----------
        object : any type
            The object for which the priority is being set.
        prio : int, optional
            The priority level to assign to the object. Default is 1.
        """
        
        # Check if the object is in the queue.
        is_in_queue = False
        for i in range(self._queue_next_index):
            if self._queue[i] == object:
                is_in_queue = True
                break

        # If the object is not in the queue, do not prioritise it.
        if not is_in_queue:
            return  # Exit the method if the object is not found in the queue.

        # First, remove any existing priority for the object.
        self.deprioritise_object(object)
        
        # Add the object to the heap with the new priority.
        self._heap_add(object, prio)

    def deprioritise_object(self, object):
        """
        Removes the priority of a queued object.
        
        If the object is found in the queue, its priority is removed from the heap.
        If the object is not found in the heap, it is added to the not-in-heap list.

        Parameters:
        ----------
        object : any type
            The object for which the priority is being removed.
        """
        
        # Check if the object is in the queue.
        index_in_queue = -1
        for i in range(self._queue_next_index):
            if self._queue[i] == object:
                index_in_queue = i
                break
        
        # If the object is not in the queue, exit the method.
        if index_in_queue == -1:
            return  # Exit if the object is not found in the queue.

        # Remove the object from the heap if it has a priority.
        for i in range(self._heap_next_index):
            if self._heap[i][0] == index_in_queue + 1:
                index_in_heap = i
                self._heap_remove(index_in_heap)
                break
        
        # Check if the object is already in the not-in-heap list.
        found = False
        for i in range(self._not_in_heap_next_index):
            if self._not_in_heap[i] == object:
                found = True
                break
        
        # If the object is not found in the not-in-heap list, add it.
        if not found:
            self._not_in_heap[self._not_in_heap_next_index] = object
            self._not_in_heap_next_index += 1

    def _heap_remove(self, index):
        """
        Removes an element from the heap at the specified index.

        This method replaces the element to be removed with the last element
        in the heap and then decreases the heap size. If the removed element
        is not the last element, it ensures the heap invariant is maintained.

        Parameters:
        ----------
        index : int
            The index of the element to be removed from the heap.
        """
        
        # Replace the element to be removed with the last element in the heap,
        # unless it is the last element itself.
        if index != self._heap_next_index - 1:
            self._heap[index] = self._heap[self._heap_next_index - 1]
        
        # Clear the last element in the heap.
        self._heap[self._heap_next_index - 1] = [0, 0]
        
        # Decrease the size of the heap.
        self._heap_next_index -= 1
        
        # If the removed element was not the last one, maintain the heap invariant.
        if index != self._heap_next_index:
            self._heap_invariante(index)
        
    def _heap_add(self, object, prio):
        """
        Adds an object to the heap with a specified priority.

        This method finds the index of the object in the queue, adds it to the heap,
        and ensures the heap invariant is maintained. If the object was previously
        in the not-in-heap list, it will be removed from there.

        Parameters:
        ----------
        object : any type
            The object to be added to the heap.
        
        prio : int
            The priority associated with the object.
        """
        
        # Find the index of the object in the queue.
        for i in range(self._queue_next_index):
            if self._queue[i] == object:
                object_idx = i + 1  # Convert to 1-based index.
                break

        # Add the object and its priority to the heap.
        self._heap[self._heap_next_index] = [object_idx, prio]
        
        # Increase the size of the heap.
        self._heap_next_index += 1
        
        # Maintain the heap invariant for the newly added element.
        self._heap_invariante(self._heap_next_index - 1)
        
        # Remove the object from the not-in-heap list, if it exists.
        self._not_in_heap_remove(object)

    def _not_in_heap_remove(self, object):
        """
        Removes an object from the not-in-heap list.

        This method searches for the specified object in the not-in-heap list
        and removes it by shifting the elements to fill the gap, if found.

        Parameters:
        ----------
        object : any type
            The object to be removed from the not-in-heap list.
        """
        
        # Iterate through the not-in-heap list to find the object.
        for i in range(self._not_in_heap_next_index):
            if self._not_in_heap[i] == object:
                # Shift elements to remove the object from the list.
                for j in range(i, self._not_in_heap_next_index - 1):
                    self._not_in_heap[j] = self._not_in_heap[j + 1]
                
                # Set the last position to zero (or equivalent empty value).
                self._not_in_heap[self._not_in_heap_next_index - 1] = 0
                
                # Decrease the count of elements in the not-in-heap list.
                self._not_in_heap_next_index -= 1
                break

    def _heap_invariante(self, index):
        """
        Maintains the heap invariant by checking and rearranging the heap structure
        starting from the specified index. The method ensures that the parent-child
        relationships in the heap are correctly established according to the priority.

        Parameters:
        ----------
        index : int
            The index of the element to start checking the heap invariant.
        """
        
        # Initialize the stack for recursive calls and track the current index.
        self._recursive_calls_stack[0] = index
        self._recursive_calls_stack_next_index = 1

        while self._recursive_calls_stack_next_index > 0:
            # Get the current index to check and remove it from the stack.
            current_index = self._recursive_calls_stack[0]
            for i in range(self._recursive_calls_stack_next_index - 1):
                self._recursive_calls_stack[i] = self._recursive_calls_stack[i + 1]
            self._recursive_calls_stack[self._recursive_calls_stack_next_index - 1] = 0
            self._recursive_calls_stack_next_index -= 1

            # Check if the current node has a parent.
            if current_index > 0:
                parent_index = (current_index - 1) // 2
                
                # Get the priorities and queue indices of the current and parent nodes.
                current_queue_idx = self._heap[current_index][0]
                current_prio = self._heap[current_index][1]
                parent_queue_idx = self._heap[parent_index][0]
                parent_prio = self._heap[parent_index][1]

                # Swap with the parent if the current node has a higher priority or the same priority but lower queue index.
                if current_prio > parent_prio or (current_prio <= parent_prio and current_queue_idx < parent_queue_idx):
                    self._heap[current_index], self._heap[parent_index] = self._heap[parent_index], self._heap[current_index]
                    self._recursive_calls_stack.append(parent_index)  # Re-check the parent index
                    self._recursive_calls_stack_next_index += 1

            # Check the child nodes.
            child1_index = current_index * 2 + 1
            child2_index = current_index * 2 + 2

            # Check the first child (left).
            if child1_index < self._heap_next_index:
                child1_queue_idx = self._heap[child1_index][0]
                child1_prio = self._heap[child1_index][1]
                current_queue_idx = self._heap[current_index][0]
                current_prio = self._heap[current_index][1]

                if child1_queue_idx != 0 and (child1_prio > current_prio or (child1_prio == current_prio and child1_queue_idx < current_queue_idx)):
                    # Swap with the first child if necessary.
                    self._heap[current_index], self._heap[child1_index] = self._heap[child1_index], self._heap[current_index]
                    self._recursive_calls_stack.append(child1_index)  # Re-check the child index
                    self._recursive_calls_stack_next_index += 1

            # Check the second child (right).
            if child2_index < self._heap_next_index:
                child2_queue_idx = self._heap[child2_index][0]
                child2_prio = self._heap[child2_index][1]
                current_queue_idx = self._heap[current_index][0]
                current_prio = self._heap[current_index][1]

                if child2_queue_idx != 0 and (child2_prio > current_prio or (child2_prio == current_prio and child2_queue_idx < current_queue_idx)):
                    # Swap with the second child if necessary.
                    self._heap[current_index], self._heap[child2_index] = self._heap[child2_index], self._heap[current_index]
                    self._recursive_calls_stack.append(child2_index)  # Re-check the child index
                    self._recursive_calls_stack_next_index += 1