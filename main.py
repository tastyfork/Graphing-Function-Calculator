import tkinter as tk
from tkinter import filedialog

from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from design import *
import design


class MyMplCanvas(FigureCanvas):
    def __init__(self, figure_canvas, parent=None):
        self.figure_canvas = figure_canvas
        FigureCanvas.__init__(self, self.figure_canvas)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MyWin(QMainWindow, GuiMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setup(self)

        self.function_queue = plotter.Queue()
        self.figure_canvas, self.subplot = plotter.create_figure_canvas()
        self.graph_layout = QVBoxLayout(self.widget)

        self.canvas = MyMplCanvas(self.figure_canvas)
        self.graph_layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.graph_layout.addWidget(self.toolbar)

        self.push_button.clicked.connect(self.push_click)
        self.clear_button.clicked.connect(self.clear_click)
        self.save_button.clicked.connect(self.save_functions)
        self.load_button.clicked.connect(self.load_functions)
        self.input_line.returnPressed.connect(self.push_button.click)
        self.select_button.clicked.connect(self.select_click)
        self.deselect_button.clicked.connect(self.deselect_click)

        self.function_list = list()
        self.selected_function = None

    # Called on push button pressing
    def push_click(self):
        if self.input_line.text():
            if self.selected_function is not None:
                self.edit_function_in_list(self.selected_function)
                self.deselect_click()
            else:
                new_function = self.input_line.text()
                self.add_function_to_list(new_function)
                self.reset_input_lines()

    # Called on clear button pressing
    def clear_click(self):
        plotter.clear_all(self.function_queue, self.subplot)
        self.function_column.clear()
        self.input_line.clear()
        self.function_list.clear()
        self.canvas.draw()

    # Called on selecting
    def select_click(self):
        try:
            self.selected_function = int(self.select_line.text()) - 1
        except:
            design.error_message('Incorrect number')
            return
        else:
            count = 0
            function = None
            for i in self.function_list:
                if count == self.selected_function:
                    function = i
                    break
                count += 1

            if function is None:
                self.reset_input_lines()
            else:
                self.input_line.setText(str(function.text))
                self.start_line.setText(str(function.start))
                self.end_line.setText(str(function.end))
                self.accuracy_line.setText(str(function.accuracy))
                self.color_line.setText(str(function.color))
            self.function_seleted(self.selected_function + 1)

    # Called on deselecting
    def deselect_click(self):
        self.selected_function = None
        self.function_seleted(None)
        self.reset_input_lines()

    # Adds function to list and refresh graph
    def add_function_to_list(self, expression, start=0, end=0, accuracy=0, color=None):
        # Graph settings
        if start == end == accuracy:
            try:
                start = int(self.start_line.text())
                end = int(self.end_line.text())
                accuracy = int(self.accuracy_line.text())
            except:
                design.error_message('Incorrect number')
                return
        x_values = plotter.calculate_x_values(start, end, accuracy)
        if color is None:
            color = self.color_line.text()
            if len(color) == 0:
                design.error_message('Incorrect color: ' + str(color))
                return

        # Calculating
        plotter.add_function(expression, self.function_queue, x_values, color)
        plotter.draw(self.function_queue, self.subplot)

        # Drawing stuff
        self.canvas.draw()
        self.canvas.flush_events()
        self.canvas.show()

        # Store
        func = plotter.Function(expression, start, end, accuracy, color)
        self.function_list.append(func)
        self.function_column.append(str(len(self.function_list)) + ') ' + expression)

    def edit_function_in_list(self, index):
        # Graph settings
        function = self.input_line.text()
        try:
            start = int(self.start_line.text())
            end = int(self.end_line.text())
            accuracy = int(self.accuracy_line.text())
        except:
            design.error_message('Incorrect number')
            return
        x_values = plotter.calculate_x_values(start, end, accuracy)
        color = self.color_line.text()
        if len(color) == 0:
            design.error_message('Incorrect color: ' + str(color))
            return

        # Calculating
        plotter.edit_function(self.selected_function, function, self.function_queue, x_values, color)
        plotter.draw(self.function_queue, self.subplot)

        # Drawing stuff
        self.canvas.draw()
        self.canvas.flush_events()
        self.canvas.show()

        # Store
        func = plotter.Function(function, start, end, accuracy, color)
        self.function_list[index] = func
        self.function_column.clear()

        # Updatig function column
        cur = 1
        for f in self.function_list:
            self.function_column.append(str(cur) + ') ' + f.text)
            cur += 1

    # Asks file path and loads from it function list
    def load_functions(self):
        root = tk.Tk()
        root.withdraw()

        file = filedialog.askopenfile(mode='r')
        if file is None:
            return

        self.function_list.clear()
        self.function_column.clear()
        for line in file:
            text = line.replace('\n', '').split(' ')
            self.add_function_to_list(text[0], int(text[1]), int(text[2]), int(text[3]), str(text[4]))

    # Asks file path and saves function list there
    def save_functions(self):
        root = tk.Tk()
        root.withdraw()

        file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
        if file is None:
            return

        for func in self.function_list:
            text = func.text + ' ' + str(func.start) + ' ' + str(func.end) + ' ' + str(func.accuracy) + ' ' + str(func.color) + '\n'
            file.write(text)
        file.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyWin()
    window.show()
    sys.exit(app.exec_())
