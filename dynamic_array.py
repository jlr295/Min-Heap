
from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index = self._index + 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Adjusts the capacity of the underlying storage of a StaticArray.
        """
        # We first need to validate the new_capacity requested.  The requested capacity should:
        # 1. Not be any smaller than the number of elements stored in the array.
        # 2. Be a positive integer.
        if new_capacity < self._size or new_capacity <= 0:
            return
        # Set the capacity to the new value.
        self._capacity = new_capacity
        # Create new array object that is the length of the new capacity.
        self._new_array = StaticArray(new_capacity)
        # Copy original array to new array
        if self._size > 0:
            for index in range(self._size):
                self._new_array.set(index, self._data.get(index))
        # Set new array to data variable
        self._data = self._new_array

    def append(self, value: object) -> None:
        """
        This method will add a new value to the end of an Array.  If the storage associated with this
        dynamic array is full, the capacity must be doubled using the resize() method.
        """
        # First determine whether storage is full.
        if self._size == self._capacity:
            self.resize(self._capacity * 2)
        # set value to last index (which would be the size)
        self._data.set(self._size, value)
        # Increment size
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Adds a new value at a specified index.  If the index is invalid, a "DynamicArrayException"
        will be raised.  If the storage is full than capacity needs to be doubled using
        the resize() method.
        """
        # Verify that the index passed is valid.
        if 0 <= index <= self._size:
            # Determine whether we need to double the capacity based on the size.
            if self._size == self._capacity:
                self.resize(self._capacity * 2)
            # Move each value up
            for inc in range(self._size - index):
                self._data.set(self._size - inc, self._data.get(self._size - (inc + 1)))
            # Set value to index
            self._data.set(index, value)
            # Increase size
            self._size += 1
        else:  # If index is not valid raise exception.
            raise DynamicArrayException

    def remove_at_index(self, index: int) -> None:
        """
        Removes an element of a specified index.  If the index is invalid, a "DynamicArrayException"
        will be raised.  If the storage is less than 1/4 of its capacity AND the current capacity is
        greater than 10 elements, AND reducing the capacity will not result in a capacity less than
        10 elements then the capacity should be reduce in half.
        """
        # Verify that the index passed is valid.
        if 0 <= index <= self._size - 1:
            # If the capacity is greater than 10
            # and the reduced capacity is greater than 10
            # and the size is less than a quarter of the capacity
            if self._capacity > 10 and self._size < (self._capacity / 4):
                if self._size * 2 < 10:
                    self.resize(10)
                else:
                    self.resize(self._size*2)
            # move each value down
            for dec in range(self._size - index - 1):
                self._data.set(index + dec, self._data.get(index+1+dec))
            self._data.set(self._size-1, None)
            self._size -= 1
        else:  # If the index is not valid raise exception
            raise DynamicArrayException

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Returns a dynamic array that contains the requested number of elements from the original
        array starting with the element of the starting index.
        """
        # Validate user input.
        if self._size >= size >= 0 and 0 <= start_index <= self._size-1:
            # Create Array
            new_array = DynamicArray()
            # Traverse list starting at the index provided
            for index in range(size):
                if start_index > self._size-1:
                    raise DynamicArrayException # raise exception if index goes beyond the size (runs off the array)
                new_array.append(self._data.get(start_index))
                start_index += 1
        else: # If the index is not valid.
            raise DynamicArrayException

        return new_array

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Takes a DynamicArray and appends all values within the object onto the current DynamicArray.
        """
        # If the current storage is at capacity or will be upon addition of the elements then increase the capacity.
        if self._capacity < self._size + second_da._size:
            self.resize(self._capacity*2)
        # Append each value to the end of the current DynamicArray
        for index in range(second_da._size):
            self.append(second_da._data.get(index))

    def map(self, map_func) -> "DynamicArray":
        """
        Creates a new DynamicArray where each element is derived by the given function.  Similar to the built-in
        map_fun in python
        """
        # Create new DynamicArray
        new_array = DynamicArray()
        # Traverse current DynamicArray
        for index in range(self._size):
            element = self._data.get(index) # Get each element
            new_element = map_func(element) # Generate new element
            new_array.append(new_element) # Add new element to array.

        return new_array

    def filter(self, filter_func) -> "DynamicArray":
        """
        Creates a new DynamicArray which is populated with values that satisfy the parameter 'filter_func'
        """
        # Create new DynamicArray object
        new_array = DynamicArray()
        # Traverse DynamicArray
        for index in range(self._size):
            element = self._data.get(index) # Get each element
            if filter_func(element) is not False:
                new_array.append(element)
        return new_array

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        This method applies reduce_func to all of the elements of the DynamicArray and returns the
        resulting value.  If the parameter is not provided, the first value of the array is used as the initializer.
        If the DynamicArray is empty, the method will return the value of the initializer.
        """
        result = 0
        # If the DynamicArray is empty return initializer
        if self._size == 0:
            return initializer
        # Set values based on initializer
        if initializer is None:
            x = self._data.get(0)
            y = self._data.get(1)
        else:
            x = initializer
            y = self._data.get(0)

        if self._size == 1 and initializer is None:
            return self._data.get(0)

        #traverse array
        for index in range(1, self._size+1):
            result = reduce_func(x,y)
            x = result
            if initializer is None:
                y = self._data.get(index+1)
            else:
                y = self._data.get(index)
            if y is None or x is None:
                break

        return result


def find_mode(arr: DynamicArray) -> (DynamicArray, int):
    """
    Receives a dynamic array in either descending or ascending order and return a tuple which contains
    a DynamicArray composed of the most frequently occurring values, and an integer that represents
    the frequency
    """
    # Check to see if array is ascending or descending order.
    new_array = DynamicArray()
    matches = 0
    max_count = 0
    max_val = 0
    mode_counter = 0
    mode_index = 0

    # If there is only one element in the array.
    if arr.length() == 1:
        new_array.append(arr.get_at_index(0))
        return new_array, 1

    for index in range(0, arr.length() - 1):  # Generate indices up to the end of arr.

        if arr.get_at_index(index) == arr.get_at_index(index + 1):  # If the current value matches the next value
            matches += 1  # increment matches
            if index == arr.length()-2:
                if matches > max_count:
                    max_count = matches
                    max_val = arr.get_at_index(index)
                    new_array.append(arr.get_at_index(index))
                    mode_counter = 1
                elif matches == max_count:
                    new_array.append(arr.get_at_index(index))
                    mode_counter+=1
                return new_array.slice(new_array.length()-mode_counter, mode_counter), max_count + 1

        else: # once we encounter a mismatch we need to fill in our values
            if matches > max_count:
                max_count = matches
                max_val = arr.get_at_index(index)
                new_array.append(arr.get_at_index(index))
                mode_index = new_array.length()-1
                mode_counter = 1
            elif matches == max_count and index != 0:
                new_array.append(arr.get_at_index(index))
                mode_counter+=1
            if index == arr.length()-2:
                if max_val == 0:
                    return arr, 1
                return new_array.slice(mode_index, mode_counter), max_count + 1
            matches = 0
