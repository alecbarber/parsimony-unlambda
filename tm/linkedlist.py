class LinkedListNode:
    def __init__(self, list, value):
        self._parent = list
        self._value = value
        self._prev = None
        self._next = None
    
    def next(self):
        return self._next

    def nextorinsert(self, v):
        return self.next() if self.next() else self.insertafter(v).next()

    def prev(self):
        return self._prev

    def prevorinsert(self, v):
        return self.prev() if self.prev() else self.insertbefore(v).prev()

    def insertafter(self, v):
        return self._parent.insertafter(self, v)

    def insertbefore(self, v):
        return self._parent.insertbefore(self, v)

    def value(self):
        return self._value

    def setvalue(self, v):
        self._value = v
    
    def remove(self):
        return self._parent.remove(self)

class LinkedList:
    def __init__(self):
        self._head = None
        self._tail = None
        self._length = 0

    def begin(self):
        return self._head
    
    def end(self):
        return self._tail
    
    def length(self):
        return self._length

    def insertbefore(self, node, v):
        self._length = self._length + 1
        if not self._head:
            self._head = self._tail = LinkedListNode(self, v)
        else:
            if not node:
                node = self._head
            new = LinkedListNode(self, v)
            new._next = node
            new._prev = node._prev
            if node._prev is None:
                self._head = new
            else:
                node._prev._next = new
            node._prev = new
        return node
    
    def insertafter(self, node, v):
        self._length = self._length + 1
        if not self._tail:
            self._head = self._tail = LinkedListNode(self, v)
        else:
            if not node:
                node = self._tail
            new = LinkedListNode(self, v)
            new._prev = node
            new._next = node._next
            if not node._next:
                self._tail = new
            else:
                node._next._prev = new
            node._next = new
        return node
    
    def remove(self, node):
        self._length = self._length - 1
        if node._prev:
            node._prev._next = node._next
        else:
            self._head = node._next
        if node._next:
            node._next._prev = node._prev
        else:
            self._tail = node._prev
        return node._prev if node._prev else node._next
