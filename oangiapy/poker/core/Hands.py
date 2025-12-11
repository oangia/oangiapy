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

    def compare_point(self, other):
        if self.get_point() == other.get_point():
            return 0
        if self.get_point() > other.get_point():
            return 1
        return -1

    def compare_dominance(self, other):
        _back, _middle, _front = self.compare(other)
        if _back == 0 and _middle ==0 and _front == 0:
            return 0

        if _back >=0 and _middle >= 0 and _front >= 0:
            return 1

        if _back <=0 and _middle <= 0 and _front <= 0:
            return -1

        return 0
    
    def compare(self, other):
        _back = self._back.compare(other.get_back())
        _middle = self._middle.compare(other.get_middle())
        _front = self._front.compare(other.get_front())
        return (_back, _middle, _front)

    def __lt__(self, other):
        _back, _middle, _front = self.compare(other)
        if _back == 0:
            if _middle == 0:
                return _front == -1
            return _middle == -1
        return _back == -1

    def __gt__(self, other):
        return self._point > other._point
        
    def __repr__(self):
        return f"Back: {self._back}\nMiddle: {self._middle}\nFront: {self._front}"
