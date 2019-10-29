################################################################
# 2D плоттер
# Скрипт использует библиотеки numpy и matplotlib
# для построения двумерных графиков заданных функций
#
# Разработчик: студентка 2-ого курса МГТУ СТАНКИН Белова Е. Ю.
# Данная версия скрипта может использоваться для построения простейших графиков функций:
# y = x^n
# y = x^n + x^(n-1) + ... + x^1 + x^0
# y = n^x
# y = log x
# y = sin x (y = cos x)
# y = arcsin x (y = arccos x)
# y = tg x
# y = arctg x (y = arcctg x)
# y = sec x (y = cosec x)
#
################################################################

import numpy as np
import numexpr as ne
import matplotlib.pyplot as plt
import re


class Line:  # класс линии
    def __init__(self, func, ox,
                 label, color='r', form='-'
                 ):
        self.y = set_ay(ox, func)  # Функция вычисления у по х
        self.x = ox
        if label is None:
            self.label = func
        else:
            self.label = label
        self.color = color
        self.form = form

    def set_label(self, name):
        self.label = name

    def set_color(self, name):
        self.color = name

    def set_form(self, name):
        self.form = name


class Axes:  # Класс полотна
    def __init__(self, fig, rows=1, cols=1, num=1):
        # self.ax = fig.add_subplot(rows, cols, num)
        self.array = []
        self.lines = []

    def set_array(self, start=-10.0, stop=10.0):
        self.array = set_ax(start, stop)

    def add_line(self, func, label, color, form):
        cur = Line(func, self.array, label, color, form)
        self.lines.append(cur)

    def del_line(self, name):
        for i in self.lines:
            if i.label == name:
                self.lines.remove(i)


class Figure:   # Класс фигуры для размещения полотен
    def __init__(self):

        self.list_axes = []

    def add(self, n=1):  # Добавить больше одного графика
        if n == 1:
            one = Axes(self, 1, 1, 1)
            self.list_axes.append(one)
        return one

    def clear(self):
        for i in self.list_axes:
            i.pop()


def create(func, label, color, form):  # Создание полотна для рисования
    myfig = Figure
    axes = myfig.add(myfig)
    axes.set_array()


class queue:   # Класс очереди
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def add(self, a):
        self.items.append(a)

    def pop(self, a):
        self.items.remove(a)

    def clear(self):
        self.items.clear()

    def get_func(self, ind):
        return self.items[ind]


def set_ax(st=0, end=10):  # Функция, которая создает разбиение по Ох (множество точек на оси х)
    # Принимает начало и конец отрезка
    accuracy = (end - st) * 100
    ox = np.linspace(st, end, accuracy)
    return ox


def cosec(ox, a=0, b=0):
    oy = 1/np.cos(ox+a) + b
    return oy


def sec(ox, a=0, b=0):
    oy = 1/np.sin(ox+a) + b
    return oy


def arctan(ox, a=0, b=0):
    oy = np.arctan(ox+a) + b
    return oy


def arccotan(ox, a=0, b=0):
    oy = np.pi/2 - np.arctan(ox+a) + b
    return oy


def cotan(ox, a=0, b=0):
    oy = 1/np.tan(ox+a) + b
    return oy


def tan(ox, a=0, b=0):
    oy = np.tan(ox+a) + b
    return oy


def arccosinus(ox, a=0, b=0):
    oy = np.arccos(ox+a) + b
    return oy


def arcsinus(ox, a=0, b=0):
    y = np.arcsin(ox+a) + b
    return y


def cosinus(ox, a=0, b=0):
    oy = np.cos(ox+a)+b
    return oy


def sinus(ox, a=0, b=0):
    oy = np.sin(ox+a) + b
    return oy


def logarifm(ox, a=0, b=0, n=np.e):
    oy = np.log(ox + a) / np.log(n) + b
    return oy


def stepen(ox, a=0, b=0, n=1):  # Степенная функция
    # Принимает коэффициенты и множество точек на Ох
    oy = ((ox+a) ** n) + b
    return oy


def pokaz(ox, a=0, b=0, n=2):  # Показательная функция
    # Принимает коэффициенты и множество точек на Ох
    oy = (n ** (ox+a)) + b
    return oy


def create_fig(a=0, b=10):  # Тоже функция создания полотна (тест 1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(a, b)
    ax.set_ylim(a, b)
    ax.grid(True)
    ax.set_xlabel(u'Аргумент')
    ax.set_ylabel(u'Функция')
    list_func = queue()
    ox = set_ax(a, b)
    return fig, list_func, ox, ax


def plot(x, y, label, ax, func):  # Функция отрисовки графика тест 1
    # Принимает множество точек Ох, Оу и название графика
    label = label.encode("utf-8")
    lines, = ax.plot(x, y, label=label)
    ax.legend()
    func.add(lines)


def index(a):   # Для теста 1
    if a == 2:
        print("Введите a, b")
    if a == 3:
        print("Введите a, b и n:")
    ind = input().split()
    for x in range(len(ind)):
        if ind[x] == 'e':
            ind[x] = np.e
        if ind[x] == 'pi':
            ind[x] = np.pi
        ind[x] = float(ind[x])
    return ind


def set_ay(ox, exp):   # Формирование значений оси у по функции
    exp = exp.replace('^', '**')
    exp = exp.replace('X', 'x')
    exp = exp.replace('ctg', '1/tan')
    exp = exp.replace('tg', 'tan')

    y = []
    for x in ox:
        y.append(ne.evaluate(exp))
    return y


def save(fig):   # Сохранение фигуры
    fig.savefig('exmpl.png')


def draw(ox, func, ax):   # Еще одна функция отрисовки графика (с использованием списка линий) тест 2
    for i in func.items:
        ax.plot(ox, i)


def add_func(new, functions, ox):
    oy = set_ay(ox, new)
    functions.add(oy)


def clear_all(functions, ax):
    ln = len(ax.lines)
    for i in range(ln):
        ax.lines[0].remove()
    functions.clear()


def test2():
    print("Введите количество функций: ")
    functions = queue()
    n = int(input())
    ox = set_ax()
    fig = create_fig()
    for i in range(n):
        print("Введите выражение:")
        curr = input()
        oy = set_ay(ox, curr)
        functions.add(oy)
    plot(ox, fig.axes, functions)
    draw(ox, functions, fig.axes)
    save(fig)


def test():  # Функция для теста
    invalid_input = True
    print("Введите диапазон по Х:")
    start, end = input().split()
    ox = set_ax(float(start), float(end))
    ax = config_plot(float(start), float(end))
    print("Введите количество графиков:")
    count = int(input())
    for i in range(count):
        print("Выберите график для построения:\n"
              "1. y = (x+a)^n + b\n"
              "2. y = n^(x+a) + b\n"
              "3. y = logn(x+a) + b\n"
              "4. y = sin(x+a) + b\n"
              "5. y = arcsin(x+a) + b\n"
              "6. y = tg(x+a) + b\n"
              "7. y = arctg(x+a) + b\n"
              "8. y = sec(x+a) + b\n"
              "9. y = cosec(x+a) + b\n"
              "10. y = cos(x+a) + b\n"
              "11. y = arccos(x+a) + b\n"
              "12. y = ctg(x+a) + b\n"
              "13. y = arcctg(x+a) + b\n"
              "14. y = a0*(x+b0)^n + a1*(x+b1)^(n-1) + ... + a(n-1)*(x+b(n-1))^1 + an*(x+bn)^0")
        ans = input()
        if ans == '1':  # Показательная функция
            a, b, n = index(3)
            label = "(x+{})^{}+{}".format(a, n, b)
            y = stepen(ox, a, b, n)
            plot(ox, y, label, ax)
        if ans == '2':  # Степенная функция
            a, b, n = index(3)
            label = "({}^(x+{})+{}".format(n, a, b)
            y = pokaz(ox, a, b, n)
            plot(ox, y, label, ax)
        if ans == '3':  # Логарифмическая функция
            a, b, n = index(3)
            label = "log{}(x+{})+{}".format(n, a, b)
            y = logarifm(ox, a, b, n)
            plot(ox, y, label, ax)
        if ans == '4':  # Функция синуса
            a, b = index(2)
            label = "sin(x+{})+{}".format(a, b)
            y = sinus(ox, a, b)
            plot(ox, y, label, ax)
        if ans == '5':  # Функция арксинуса
            a, b = index(2)
            label = "y = arcsin(x+{}) + {}".format(a, b)
            y = arcsinus(ox, a, b)
            plot(ox, y, label, ax)
        if ans == '6':   # Функция тангенса
            a, b = index(2)
            label = "y = tg(x+{}) + {}".format(a, b)
            y = tan(ox, a, b)
            plot(ox, y, label, ax)
        if ans == '7':  # Функция арктангенса
            a, b = index(2)
            label = "y = arctg(x + {}) + {}".format(a, b)
            y = arctan(ox, a, b)
            plot(ox, y, label, ax)
        if ans == '8':  # Функция секанса
            a, b = index(2)
            y = sec(ox, a, b)
            label = "y = sec(x+{}) + {}".format(a, b)
            plot(ox, y, label, ax)
        if ans == '9':  # Функция косеканса
            a, b = index(2)
            label = "y = cosec(x+{}) + {}".format(a, b)
            y = cosec(ox, a, b)
            plot(ox, y, label, ax)
        if ans == '10':  # Функция косинуса
            a, b = index(2)
            label = "y = cos(x+{}) + {}".format(a, b)
            y = cosinus(ox, a, b, ax)
            plot(ox, y, label)
        if ans == '11':  # Функция аркосинуса
            a, b = index(2)
            label = "y = arccos(x+{}) + {}".format(a, b)
            y = arccosinus(ox, a, b)
            plot(ox, y, label, ax)
        if ans == '12':  # Функция котангенса
            a, b = index(2)
            label = "y = ctg(x + {}) + {}".format(a, b)
            y = cotan(ox, a, b)
            plot(ox, y, label, ax)
        if ans == '13':  # Функция арккотагенса
            a, b = index(2)
            label = "y = arcctg(x+{}) + {}".format(a, b)
            y = arccotan(ox, a, b)
            plot(ox, y, label, ax)
        if ans == '14':  # Функция полинома
            a, b = index(2)
            label = "y = a0*(x+b0)^n + ... + an*(x+bn)^0".format(argA, argB)
            y = polinom(ox, argA, argB)
            plot(ox, y, label, ax)


if __name__ == "__main__":
    test2()
