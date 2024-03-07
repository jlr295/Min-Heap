from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)

    def add(self, node: object) -> None:
        """
        Adds a new object to the heap while maintaining heap property.
        """
        # First check to see if heap is empty
        if self.is_empty():
            self._heap.append(node)

        # heap is not empty
        else:
            # First add new element to the last index (length - 1)
            self._heap.append(node)

            child_index = self._heap.length() - 1  # Initialize child's value to last index variable
            parent_index = (child_index - 1) // 2  # Initialize parent's index to child's index

            # Percolate up the array until the parent is less than the value
            # Initialize values
            parent_val = self._heap.get_at_index(parent_index)
            child_val = self._heap.get_at_index(child_index)

            # While the child is less than parent and the parent_index is not negative
            while child_val < parent_val and parent_index >= 0 and child_index > 0:
                # Swap child with parent
                self._heap.set_at_index(parent_index, child_val)
                self._heap.set_at_index(child_index, parent_val)
                # Reset values
                child_index = parent_index  # Set child index to parent index
                child_val = self._heap.get_at_index(child_index)
                # If the child is at less than index 1, then there will be no
                # next parent as the current parent is at the root of the heap
                if child_index >= 1:
                    parent_index = (child_index - 1) // 2
                    parent_val = self._heap.get_at_index(parent_index)

    def is_empty(self) -> bool:
        """
        Returns true if the heap is empty, otherwise will return False
        """
        return self._heap.is_empty()

    def get_min(self) -> object:
        """
        Returns an object with the minimum key, without removing it from the heap.
        If the heap is empty, the method raises a MinHeapException
        """
        # Check to see if heap is empty.
        if self.is_empty():
            raise MinHeapException  # Raise exception
        else:
            return self._heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        Returns an object with the minimum key, and removes it from the heap.
        """
        # Check to see if heap is empty.
        if self.is_empty():
            raise MinHeapException  # Raise exception
        else:  # Heap is not empty
            # Save minimum
            minimum = self.get_min()
            # Replace first index with the last value
            self._heap.set_at_index(0, self._heap.get_at_index(self.size()-1))
            # Remove last value
            self._heap.remove_at_index(self.size() - 1)
            # Percolate down the heap if array is greater than 1
            if self.size() > 1:
                _percolate_down(self._heap, 0)

            return minimum

    def build_heap(self, da: DynamicArray) -> None:
        """
        Receives a dynamic array object with values in any order and builds
        a proper MinHeap from them
        """
        # Check to see if array is empty.
        if da.is_empty():
            self._heap = DynamicArray()
            return

        else:  # Array is not empty
            self._heap = DynamicArray(da)
            # Find the largest index in array
            largest_index = da.length()-1
            # Find the parent of the value at the largest index
            parent = (largest_index-1) // 2
            # iterate until root is reached
            while parent >= 0:
                _percolate_down(self._heap, parent)
                # Move parent to previous index
                parent -= 1

    def size(self) -> int:
        """
        Returns the number of items currently stored in the heap.
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Clears the contents of the heap.
        """
        # Set heap to empty DynamicArray
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    Receives a DynamicArray and sorts its contents in non ascending order
    using the HeapSort algorithm
    """
    # Build a heap out of the array.
    # Check to see if array is empty.
    if da.is_empty():
        return
    else:  # Array is not empty
        # We first need to turn the Array into a min heap.
        # Find the largest index in array
        largest_index = da.length() - 1
        # Find the parent of the value at the largest index
        parent = (largest_index - 1) // 2
        # iterate until root is reached
        while parent >= 0:
            _percolate_down(da, parent)
            # Move parent to previous index
            parent -= 1

    # Now we may sort the array in non-ascending order
    # Initialize counter to the last index
    count_down = da.length()-1
    count_up = 1
    while count_down != 0:
        back_val = da.get_at_index(count_down)
        first_val = da.get_at_index(0)
        da.set_at_index(count_down, first_val)
        da.set_at_index(0, back_val)
        count_up += 1
        if count_down != 1:
            _percolate_down(da, 0, count_up)
        count_down -= 1

def _percolate_down(da: DynamicArray, parent: int, stop = 0) -> None:
    """
    Moves down a passed heap starting with the parent passed.
    Preconditions: length of array is greater than 1
    """

    # Initialize variables
    first_child_index = 2 * parent + 1
    second_child_index = 2 * parent + 2
    # Set parent value
    parent_val = da.get_at_index(parent)
    counter = 0
    # Are either child's indices out of range?
    if first_child_index >= da.length()-stop or second_child_index >= da.length():
        if da.get_at_index(first_child_index):
            if parent_val > da.get_at_index(first_child_index):
                da.set_at_index(parent, da.get_at_index(first_child_index))
                da.set_at_index(first_child_index, parent_val)

        elif da.get_at_index(second_child_index):
            if parent_val > da.get_at_index(second_child_index):
                da.set_at_index(parent, da.get_at_index(second_child_index))
                da.set_at_index(second_child_index, parent_val)

    # Percolate down while the parent's index is 1 or greater (parent should not be less than or equal to 0)
    while parent < da.length()-stop and first_child_index <= da.length()-stop-1 or second_child_index <= da.length()-stop-1 \
            and counter != da.length() - stop:
        # If first and second indices are less than the length of da - 1
        if first_child_index < da.length() and second_child_index < da.length():
            # If left child is less than or equal to second child
            if da.get_at_index(first_child_index) <= da.get_at_index(second_child_index):
                first_child_val = da.get_at_index(first_child_index)
                # If parent is less than first child
                if parent_val > first_child_val:
                    # Set child to parent's index
                    da.set_at_index(parent, first_child_val)
                    # Set parent to child's index
                    da.set_at_index(first_child_index, parent_val)
                    # Set new indices
                    parent = first_child_index
                    first_child_index = 2 * parent + 1
                    second_child_index = 2 * parent + 2
                    counter+=1
                else:
                    break
            # second child is less than first child
            else:
                if parent_val > da.get_at_index(second_child_index):
                    # Set child to parent's index
                    da.set_at_index(parent,  da.get_at_index(second_child_index))
                    # Set parent to child's index
                    da.set_at_index(second_child_index, parent_val)
                    # Set new indices
                    parent = second_child_index
                    first_child_index = 2 * parent + 1
                    second_child_index = 2 * parent + 2
                    counter+=1
                else:
                    break
        else:
            # Either first child index or second child index is out of range
            if first_child_index < da.length():
                first_child_val = da.get_at_index(first_child_index)
                if parent_val > first_child_val:
                    # Set child to parent's index
                    da.set_at_index(parent, first_child_val)
                    # Set parent to child's index
                    da.set_at_index(first_child_index, parent_val)
                    # Set new indices
                    parent = first_child_index
                    first_child_index = 2 * parent + 1
                    second_child_index = 2 * parent + 2
                    counter +=1
                else:
                    break
            elif second_child_index < da.length():
                if parent_val > da.get_at_index(second_child_index):
                    # Set child to parent's index
                    da.set_at_index(parent,  da.get_at_index(second_child_index))
                    # Set parent to child's index
                    da.set_at_index(second_child_index, parent_val)
                    # Set new indices
                    parent = second_child_index
                    first_child_index = 2 * parent + 1
                    second_child_index = 2 * parent + 2
                    counter += 1
                else:
                    break
            else:
                break
