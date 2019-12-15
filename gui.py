from PyQt5.QtWidgets import *
from window_v2 import *
import plotter2d as pl

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


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
            self.canvas.show()

    def tool_click(self):
        pl.clear_all(self.func, self.ax)
        self.canvas.draw()
        # pl.draw(self.ox, self.func, self.ax)
        self.textEdit.clear()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
