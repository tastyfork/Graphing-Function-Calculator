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
# y = tg x (y = ctg x)
# y = arctg x (y = arcctg x)
# y = sec x (y = cosec x)
#
# Иерархия функций:
#   Задается разбиение
#   Строится функция
#   Рисуется функция
# разбиение выражения бинарным деревом
################################################################

import numpy as np
import matplotlib.pyplot as plt


def razbienie(st=0, end=10):  # Функция, которая создает разбиение по Ох (множество точек на оси х)
    # Принимает начало и конец отрезка
    accuracy = (end - st) * 100
    ox = np.linspace(st, end, accuracy)
    return ox


def tan(ox, a=0, b=0):
    oy = np.tan(ox+a) + b
    return oy


def arcsinus(ox, a=0, b=0):
    y = np.arcsin(ox+a) + b
    return y


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


def confplot(a, b):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(a, b)
    ax.set_ylim(a, b)
    ax.grid(True)
    ax.set_xlabel(u'Аргумент')
    ax.set_ylabel(u'Функция')
    return ax


def plot(x, y, label, ax):  # Функция отрисовки графика
    # Принимает множество точек Ох, Оу и название графика
    label = label.encode("utf-8")
    ax.plot(x, y, label=label)
    ax.legend()
    plt.show()


def index(a):
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


def test():  # Функция для теста
    invalid_input = True
    print("Введите диапазон по Х:")
    start, end = input().split()
    ox = razbienie(float(start), float(end))
    ax = confplot(float(start), float(end))
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
    test()
