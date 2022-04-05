class Galua:
    def __init__(self, p) -> None:
        self.p = p

    def add(self, a, b):
        return (a + b) % self.p

    def mult(self, a, b):
        return (a * b) % self.p

    def add_inv(self, a):
        return self.p - a

    def mult_inv(self, a):
        for inv in range(self.p):
            if (inv * a) % self.p == 1:
                return inv



class Point:
    NULL_POINT = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other == Point.NULL_POINT:
            return False

        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return str(self)



class Elliptic:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        self.points = None
        self.galua = Galua(p)

    def __str__(self) -> str:
        return f'E{self.p}({self.a}, {self.b})'

    def __repr__(self) -> str:
        return str(self)

    def is_inv(self, p, q):
        if p == Point.NULL_POINT or q == Point.NULL_POINT:
            return p == q

        return p.x == q.x and (p.y + q.y) % self.p == 0

    def get_inv(self, p):
        if p == Point.NULL_POINT:
            return Point.NULL_POINT

        return Point(p.x, self.galua.add_inv(p.y))

    def addition(self, p: Point, q: Point):
        if p == Point.NULL_POINT or q == Point.NULL_POINT:
            return p or q

        if p == q:
            mult_inv = self.galua.mult_inv(2 * p.y)
            if mult_inv == Point.NULL_POINT:
                return Point.NULL_POINT

            l = ((3 * p.x ** 2 + self.a) * mult_inv) % self.p
            
            

        elif self.is_inv(p, q):
            return Point.NULL_POINT

        else:
            l = ((q.y + self.galua.add_inv(p.y)) * self.galua.mult_inv(q.x + self.galua.add_inv(p.x))) % self.p

        x = (l ** 2 + self.galua.add_inv(p.x) + self.galua.add_inv(q.x)) % self.p
        y = (l * (p.x + self.galua.add_inv(x)) + self.galua.add_inv(p.y)) % self.p
        return Point(x, y)

    def substruction(self, p, q):
        return self.addition(p, self.get_inv(q))

    def a_multiplication(self, p, a):
        m = p
        for _ in range(a - 1):
            m = self.addition(m, p)

        return m

    def _generate_points(self):
        if not self.points:
            domen = [d for d in range(self.p)]
            x_m = {x: (x ** 3 + self.a * x + self.b) % self.p for x in domen}
            y_m = {y: (y ** 2) % self.p for y in domen}
            self.points = [
                Point(x, y)
                for x in x_m
                for y in y_m
                if x_m[x] == y_m[y]
            ]
        
        return self.points
