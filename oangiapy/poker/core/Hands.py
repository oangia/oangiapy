class Hands:
    def __init__(self, back, middle, front):
        self._back = back
        self._middle = middle
        self._front = front
        self._point = 0

    def get_back(self):
        return self._back

    def get_middle(self):
        return self._middle

    def get_front(self):
        return self._front    

    def get_point(self):
        return self._point

    def __lt__(self, other):
        _back = self._back.compare(other._back)
        if _back == 0:
            _middle = self._middle.compare(other._middle)
            if _middle == 0:
                _front = self._front.compare(other._front)
                return _front == -1
            return _middle == -1
        return _back == -1

    def __gt__(self, other):
        return self._point > other._point

    def compare(self, other, detailed=False):
        front  = self._front.compare(other._front)
        middle = self._middle.compare(other._middle)
        back   = self._back.compare(other._back)
        if detailed:
            return [front, middle, back]

        if front == 0 and middle == 0 and back == 0:
            return 0

        if front <= 0 and middle <= 0 and back <= 0:
            return -1

        if front >= 0 and middle >= 0 and back >= 0:
            return 1

        return 0
        
    def __repr__(self):
        return f"Back: {self._back}\nMiddle: {self._middle}\nFront: {self._front}"
