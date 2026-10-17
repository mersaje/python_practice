import math
import time
from types import TracebackType

class BasicShape:
    def __init__(self, *dots):
        self.dots = dots
        self.count_dots = len(self.dots)
        if self.count_dots < 3:
            raise ValueError("В многоугольнике должно быть минимум 3 точки")

    # волшебный метод, для того, чтобы при obj1 + obj2 возвращало сумму их площадей
    def __add__(self, other):
        return self.square + other.square

    # волшебный метод, для того, чтобы при obj1 - obj2 возвращало разницу их площадей
    def __sub__(self, other):
        return self.square - other.square

    # волшебный метод, для того, чтобы при obj1 * obj2 возвращало произведение их площадей
    def __mul__(self, other):
        return self.square * other.square

    # волшебный метод, для того, чтобы при obj1 / obj2 возвращало частное их площадей
    def __truediv__(self, other):
        return self.square / other.square

    # метод для вычисления периметра фигуры
    @property
    def perimeter(self):
        p = 0
        for i in range(self.count_dots):
            if self.count_dots - i == 1:
                p += self.calculate_side_length(self.dots[0], self.dots[i])
            else:
                p += self.calculate_side_length(self.dots[i], self.dots[i + 1])
        return p

    # метод для вычисления площади фигуры по Формуле площади Гаусса
    @property
    def square(self):
        s = 0
        for i in range(self.count_dots):
            if self.count_dots - i == 1:
                s += (self.dots[i][0] * self.dots[0][1] - self.dots[i][1] * self.dots[0][0])
            else:
                s += (self.dots[i][0]*self.dots[i + 1][1] - self.dots[i][1]*self.dots[i + 1][0])
        return abs(s) / 2

    # метод для вычисления длины стороны между двумя переданными точками
    @staticmethod
    def calculate_side_length(first, second):
        return math.sqrt((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2)

    # метод для добавления точки в многогранник, т.к. в условии не описано, что должна передаваться позиция в которую добавлять точку, то добавляем в конец
    def _add(self, coordinate: tuple[float, float]):
        if type(self.dots) is tuple:
            self.dots = list(self.dots)
        self.dots.append(coordinate)
        self.count_dots += 1

class Quadrilateral(BasicShape):
    def __init__(self, *dots):
        super().__init__(*dots)
        if self.count_dots != 4:
            raise ValueError("В четырехугольнике должно быть ровно 4 точки")

    # Переопределение родительского метода с вызовом исключения, т.к. по условию не должно быть доступно добавление точек в четырехугольник(а ещё этим нарушается принцип LSP из SOLID)
    def _add(self, coordinate):
        raise TypeError('Добавление точек в четырехугольник недопустимо')

    # метод, который сообщает, является ли объект прямоугольником
    @property
    def is_rectangle(self):

        # вычисление длины сторон, противоположными будут AB & CD, BC & AD
        AB = self.calculate_side_length(self.dots[0], self.dots[1])
        BC = self.calculate_side_length(self.dots[1], self.dots[2])
        CD = self.calculate_side_length(self.dots[2], self.dots[3])
        AD = self.calculate_side_length(self.dots[3], self.dots[0])

        # вычисление диагоналей D1(AC) и D2(BD)
        D1 = self.calculate_side_length(self.dots[0], self.dots[2])
        D2 = self.calculate_side_length(self.dots[1], self.dots[3])

        if AB == CD and BC == AD and D1 == D2:
            return True
        else:
            return False

    # метод, который сообщает, является ли объект квадратом
    @property
    def is_square(self):

        # вычисление длины сторон, противоположными будут AB & CD, BC & AD
        AB = self.calculate_side_length(self.dots[0], self.dots[1])
        BC = self.calculate_side_length(self.dots[1], self.dots[2])
        CD = self.calculate_side_length(self.dots[2], self.dots[3])
        AD = self.calculate_side_length(self.dots[3], self.dots[0])

        # вычисление диагоналей D1(AC) и D2(BD)
        D1 = self.calculate_side_length(self.dots[0], self.dots[2])
        D2 = self.calculate_side_length(self.dots[1], self.dots[3])

        # квадратом считается объект, у которого все стороны равны между собой и диагонали равны между собой
        if AB == BC and CD == AD and AB == CD and D1 == D2:
            return True
        else:
            return False

class Shapes:

    def __init__(self, *shape):
        self.shapes = list(shape)

    def add_shape(self, shape):
            self.shapes.append(shape)

    def square(self):
        total_square = 0
        for i in self.shapes:
            total_square += i.square
        return total_square

    def perimeter(self):
        total_perimeter = 0
        for i in self.shapes:
            total_perimeter += i.perimeter
        return total_perimeter

    def remove_shape(self, shape):
        self.shapes.remove(shape)

    def add(self, shape, dot):
        shape._add(dot)

    def __enter__(self):
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None):
        print(f"Суммарная площадь всех фигур {self.square()}")

# контекстный менеджер который замеряет время выполнения кода внутри него
class Timer:

    def __enter__(self):
        self.current_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None):
        print(f"Время выполнения {time.perf_counter() - self.current_time:.2f} секунд")

# 3 задание
a = BasicShape((0, 0), (0, 3), (4, 0))

# 4 задание
print(f"Периметр {a.perimeter}")
print(f"Площадь {a.square}")

# 5 задание
b = Quadrilateral((0, 0), (0, 1), (1, 1), (1, 0))
print(f"Периметр {b.perimeter}")
print(f"Площадь {b.square}")

# 6 задание
print(f"Длина стороны {BasicShape.calculate_side_length((0, 3), (4, 0))}")

# 7 задание - метод add() в BasicShape переименован в _add() для выполнения 11 задания

# 8 задание
print(f"Прямоугольник? {b.is_rectangle}")
print(f"Квадрат? {b.is_square}")

# 9 задание
print(f"Результат сложения a и b {a + b}")
print(f"Результат вычитания a из b {a - b}")
print(f"Результат умножения a на b {a * b}")
print(f"Результат деления a на b {a / b}")

# 10 задание
c = BasicShape((0, 3), (4, 5), (3, 0))
shapes = Shapes(a, b)
print(f"Shapes после создания {shapes.shapes}")
shapes.add_shape(c)
print(f"Shapes после добавления c {shapes.shapes}")
print(f"Суммарная площадь {shapes.square()}")
print(f"Суммарный периметр {shapes.perimeter()}")
shapes.remove_shape(b)
print(f"Shapes после удаления b {shapes.shapes}")

# 11 задание
print(f"a до изменения {a.dots}")
shapes.add(a, (8, 8))
print(f"a после изменения {a.dots}")
# если строку ниже раскомментить - будет ошибка, т.к. метод напрямую недоступен
# a.add()

# 12 задание
with shapes:
    shapes.add_shape(b)

# 13 задание - контекстный менеджер, который измеряет время выполнения блока кода внутри него
with Timer():
    time.sleep(2)
