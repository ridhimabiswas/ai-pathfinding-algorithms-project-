class MinHeap:

    def __init__(self):
        self.capacity = 10000
        self.queue = [0] * 10000
        self.size = 0

    def push(self, element):
        # If queue is full, double its capacity
        if self.size == self.capacity:
            self.queue.extend([0] * self.capacity)
            self.capacity *= 2

        # Insert the first element directly
        if self.size == 0:
            self.queue[0] = element
            self.size += 1
            return

        # Place the new element at the end
        self.queue[self.size] = element
        current_index = self.size
        self.size += 1

        # Sift up to maintain heap property
        while self.is_higher_priority(current_index, self.parent_index(current_index)):
            self.swap(current_index, self.parent_index(current_index))
            current_index = self.parent_index(current_index)

            # If the element is at the root, break
            if current_index == 0:
                break

    def pop(self):
        if self.size == 0:
            return None
        
        if self.size == 1:
            self.size -= 1
            return self.queue[0]
        
        if self.size == 2:
            min_value = self.queue[0]
            self.queue[0] = self.queue[1]
            self.size -= 1
            return min_value

        # Save the minimum value to return later
        min_value = self.queue[0]

        # Move the last element to the root
        self.queue[0] = self.queue[self.size - 1]
        self.size -= 1
        current_index = 0

        # Sift down to maintain heap property
        while not (self.is_higher_priority(current_index, self.left_child_index(current_index)) and 
                   self.is_higher_priority(current_index, self.right_child_index(current_index))):

            if self.is_higher_priority(self.left_child_index(current_index), self.right_child_index(current_index)):
                self.swap(current_index, self.left_child_index(current_index))
                current_index = self.left_child_index(current_index)
            else:
                self.swap(current_index, self.right_child_index(current_index))
                current_index = self.right_child_index(current_index)

            if self.right_child_index(current_index) >= self.size:
                break

        # Handle case where only the left child exists
        if self.left_child_index(current_index) < self.size:
            if self.is_higher_priority(self.left_child_index(current_index), current_index):
                self.swap(current_index, self.left_child_index(current_index))

        return min_value

    # Compare if element at index1 has a higher priority than at index2
    def is_higher_priority(self, index1, index2):
        # First, compare based on the primary value (f-value)
        if self.queue[index1][0] < self.queue[index2][0]:
            return True
        elif self.queue[index1][0] > self.queue[index2][0]:
            return False
        else:
            # If the primary values are equal, compare based on the secondary value (g-value)
            if self.queue[index1][1] < self.queue[index2][1]:
                return True
            elif self.queue[index1][1] > self.queue[index2][1]:
                return False
            else:
                # If the secondary values are also equal, compare the third value
                if self.queue[index1][2] < self.queue[index2][2]:
                    return True
                else:
                    return False

    # Swap elements at two indices
    def swap(self, index1, index2):
        temp = self.queue[index1]
        self.queue[index1] = self.queue[index2]
        self.queue[index2] = temp

    # Get the index of the parent of the given node
    def parent_index(self, index):
        return (index - 1) // 2

    # Get the index of the left child of the given node
    def left_child_index(self, index):
        return (2 * index) + 1

    # Get the index of the right child of the given node
    def right_child_index(self, index):
        return (2 * index) + 2

    # Get the current size of the heap
    def length(self):
        return self.size

    # Print the heap contents
    def display(self):
        for i in range(self.size):
            print(str(self.queue[i]), end=" ")
        print("")


'''
if __name__ == "__main__":
    pq = PriorityQueue()
    pq.push((100, 0, 0))
    print(pq.pop())
    pq.push((100, 0, 0))
    pq.push((10, 0, 0))
    pq.push((150, 0, 0))
    pq.push((80, 0, 0))
    pq.push((1, 0, 0))
    pq.display()
    print(pq.pop())
    pq.display()
'''
