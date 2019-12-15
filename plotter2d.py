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
import fourFn as fn
from fourFn import BNF
import matplotlib.pyplot as plt


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
    exp = exp.replace('X', 'x')

    y = []
    expression = exp

    for x in ox:
        exp = exp.replace('x', str(x))
        fn.exprStack[:] = []
        try:
            BNF().parseString(exp, parseAll=True)
            val = fn.evaluate_stack(fn.exprStack[:])
        except fn.ParseException as pe:
            print(exp, "failed parse:", str(pe))
            return 0
        except Exception as e:
            print(exp, "failed eval:", str(e), fn.exprStack)
            return 0

        y.append(val)
        exp = expression
    return y


def save(fig):   # Сохранение фигуры
    fig.savefig('exmpl.png')


def draw(ox, func, ax):   # Еще одна функция отрисовки графика (с использованием списка линий) тест 2
    for i in func.items:
        try:
            ax.plot(ox, i)
        except Exception as e:
            print('There is incorrect functions in list')


def add_func(new, functions, ox):
    try:
        oy = set_ay(ox, new)
    except Exception as e:
        print('Incorrect input')
    else:
        functions.add(oy)


def clear_all(functions, ax):
    ln = len(ax.lines)
    for i in range(ln):
        ax.lines[0].remove()
    functions.clear()
