from abc import ABC, abstractmethod


# De este modo podríamos sustituir la clase Shape por cualquiera de las dos
class Shape(ABC):
    @abstractmethod
    def calculate_area(self):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calculate_area(self):
        return self.width * self.height


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def calculate_area(self):
        return self.side**2


# El método comun calculate_area permite que se ejecute el comportamiento sin importar
# que sean formas diferentes


def get_total_area(shapes):
    return sum(shape.calculate_area() for shape in shapes)


get_total_area([Rectangle(10, 5), Square(5)])
