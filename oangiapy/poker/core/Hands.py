class Hands:
    def __init__(self, back, middle, front):
        self._back = back
        self._middle = middle
        self._front = front

    def get_back(self):
        return self._back

    def compare(self, other, detailed=False):
        front  = self._front.compare(other._front)
        middle = self._middle.compare(other._middle)
        back   = self._back.compare(other._back)
        if detailed:
            return [front, middle, back]

        if front == 0 and middle == 0 and back == 0:
            return 1 if self._front.compareZitchPoint(other._front) == 1 else -1

        if front <= 0 and middle <= 0 and back <= 0:
            return -1

        if front >= 0 and middle >= 0 and back >= 0:
            return 1

        return 0
        
    def __repr__(self):
        return f"Back: {self._back}\nMiddle: {self._middle}\nFront: {self._front}"
