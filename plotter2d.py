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
################################################################

import numpy as np
import fourFn as fn
from fourFn import BNF
import matplotlib.pyplot as plt


class Queue:   # Класс очереди
    def __init__(self):
        self.x_values = []
        self.y_values = []
        self.colors = []

    def is_empty(self):
        return self.x_values == [] and self.y_values == [] and self.colors == []

    def add(self, x_values, y_values, color):
        self.x_values.append(x_values)
        self.y_values.append(y_values)
        self.colors.append(color)

    def length(self):
        return len(self.x_values)

    def clear(self):
        self.x_values.clear()
        self.y_values.clear()
        self.colors.clear()


class Function:
    def __init__(self, text, start, end, accuracy, color):
        self.text = text
        self.start = start
        self.end = end
        self.accuracy = accuracy
        self.color = color


def calculate_x_values(start=0, end=10, accuracy=0):    # Функция, которая создает разбиение по Ох
    # Принимает начало и конец отрезка
    if accuracy <= 0:
        accuracy = (end - start) * 10

    x_values = np.linspace(start, end, accuracy)
    return x_values


def calculate_y_values(x_values, expression):   # Формирование значений оси у по функции
    expression = expression.replace('X', 'x')
    y_values = []

    for x in x_values:
        fn.exprStack = []
        try:
            BNF().parseString(expression.replace('x', str(x)), parseAll=True)
            x_value = fn.evaluate_stack(fn.exprStack)
        except fn.ParseException as pe:
            print(expression, "failed parse:", str(pe))
            return 0
        except Exception as e:
            print(expression, "failed eval:", str(e), fn.exprStack)
            return 0

        y_values.append(x_value)

    return y_values


def create_figure_canvas(start=0, end=10):  # Тоже функция создания полотна
    plt.cla()
    figure_canvas = plt.figure()
    subplot = figure_canvas.add_subplot(111)
    subplot.set_xlim(start, end)
    subplot.set_ylim(start, end)
    subplot.grid(True)
    subplot.set_xlabel('Аргумент')
    subplot.set_ylabel('Функция')
    return figure_canvas, subplot


def draw(function_queue, axes):   # Еще одна функция отрисовки графика (с использованием списка линий)
    for i in range(0, len(function_queue.y_values)):
        try:
            axes.plot(function_queue.x_values[i], function_queue.y_values[i], color=str(function_queue.colors[i]))
        except Exception as e:
            print('There is incorrect functions in list ', e)


def add_function(expression, functions, x_values, color):
    try:
        y_values = calculate_y_values(x_values, expression)
    except Exception as e:
        print('Incorrect input')
    else:
        functions.add(x_values, y_values, color)


def edit_function(index, expression, functions, x_values, color):
    try:
        y_values = calculate_y_values(x_values, expression)
    except Exception as e:
        print('Incorrect input')
    else:
        functions.x_values[index] = x_values
        functions.y_values[index] = y_values
        functions.colors[index] = color


def clear_all(functions, axes):   # Очистка всех функций
    length = len(axes.lines)
    for i in range(length):
        axes.lines[0].remove()
    functions.clear()


def validate_text(text):
    try:
        BNF().parseString(text.replace('x', str(0)), parseAll=True)
        fn.evaluate_stack(fn.exprStack)
        print('validated')
    except fn.ParseException as pe:
        print(text, "failed parse:", str(pe))
        return False
    except Exception as e:
        print(text, "failed eval:", str(e), fn.exprStack)
        return False
    return True


def screenshot(figure_canvas):   # Сохранение фигуры
    figure_canvas.savefig('example.png')
