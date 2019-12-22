import tkinter as tk
from tkinter import filedialog

from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import plotter2d as pl
from window_v2 import *

function_list = list()


class MyMplCanvas(FigureCanvas):
    def __init__(self, fig, parent=None):
        self.fig = fig
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MyWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.fig, self.func, self.ox, self.ax = pl.create_fig()
        self.companovka_for_mlp = QVBoxLayout(self.widget)

        self.canvas = MyMplCanvas(self.fig)
        self.companovka_for_mlp.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.companovka_for_mlp.addWidget(self.toolbar)

        self.pushButton.clicked.connect(self.btn_clicked)
        self.toolButton.clicked.connect(self.tool_click)
        self.saveButton.clicked.connect(self.save_functions)
        self.loadButton.clicked.connect(self.load_functions)
        self.pushButton.setAutoDefault(True)
        self.lineEdit.returnPressed.connect(self.pushButton.click)

    def btn_clicked(self):
        if self.lineEdit.text():
            new = self.lineEdit.text()
            self.lineEdit.clear()
            pl.add_func(new, self.func, self.ox)
            pl.draw(self.ox, self.func, self.ax)
            self.canvas.draw()
            self.canvas.flush_events()
            self.textEdit.append(new)
            function_list.append(new)
            self.canvas.show()

    def tool_click(self):
        pl.clear_all(self.func, self.ax)
        # pl.draw(self.ox, self.func, self.ax)
        self.textEdit.clear()
        function_list.clear()

    def save_functions(self):
        root = tk.Tk()
        root.withdraw()

        file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
        if file is None:
            return

        for i in function_list:
            text = i + '\n'
            file.write(text)
        file.close()

    def load_functions(self):
        root = tk.Tk()
        root.withdraw()

        file = filedialog.askopenfile(mode='r')
        if file is None:
            return

        function_list.clear()
        self.textEdit.clear()
        for line in file:
            fun = line.replace('\n', '')
            if not fun:
                continue
            pl.add_func(fun, self.func, self.ox)
            pl.draw(self.ox, self.func, self.ax)
            self.canvas.draw()
            self.canvas.flush_events()
            self.textEdit.append(fun)
            function_list.append(fun)
            self.canvas.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
