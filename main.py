import json

from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import design
from design import *


class MyMplCanvas(FigureCanvas):
    def __init__(self, figure_canvas, parent=None):
        self.figure_canvas = figure_canvas
        FigureCanvas.__init__(self, self.figure_canvas)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MyWin(QtWidgets.QMainWindow, GuiMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setup(self)

        self.function_queue = plotter.Queue()
        self.figure_canvas, self.axes = plotter.create_figure_canvas()
        self.graph_layout = QtWidgets.QVBoxLayout(self.widget)

        self.canvas = MyMplCanvas(self.figure_canvas)
        self.graph_layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.graph_layout.addWidget(self.toolbar)

        self.push_button.clicked.connect(self.push_click)
        self.clear_button.clicked.connect(self.clear_click)
        self.save_button.clicked.connect(self.save_functions)
        self.load_button.clicked.connect(self.load_functions)
        self.input_line.returnPressed.connect(self.push_button.click)

        for i in range(0, self.max_functions):
            self.function_column[i].toggled.connect(lambda state, idx=i: self.function_toggled(idx, self.function_column[idx]))
            self.function_edit_buttons[i].clicked.connect(lambda state, idx=i: self.select_click(idx))
            self.function_remove_buttons[i].clicked.connect(lambda state, idx=i: self.remove_click(idx))

        self.function_list = list()
        self.selected_function = None
        self.disabled_functions = list()

    # Called on push button pressing
    def push_click(self):
        if len(self.function_list) >= self.max_functions:
            error_message('You can\'t add more than ' + str(self.max_functions) + ' functions')
            return

        if self.input_line.text():
            if self.selected_function is not None:
                self.edit_function_in_list(self.selected_function)
                self.deselect_click()
                self.reset_input_lines()
            else:
                new_function = self.input_line.text()
                self.add_function_to_list(new_function)
                self.reset_input_lines()

    # Called on clear button pressing
    def clear_click(self):
        plotter.clear_all(self.function_queue, self.axes)
        self.clear_column()
        self.input_line.clear()
        self.function_list.clear()
        self.canvas.draw()

    def deselect_click(self):
        self.function_seleted(None)
        self.selected_function = None

    # Called on selecting
    def select_click(self, function_id):
        self.selected_function = function_id
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
            index = self.color_box.findText(str(function.color), QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.color_box.setCurrentIndex(index)

        self.function_seleted(self.selected_function)

    def remove_click(self, function_id):
        old_list = self.function_list.copy()
        self.clear_click()
        old_list.remove(old_list[function_id])

        if function_id in self.disabled_functions:
            self.disabled_functions.remove(function_id)

        # Re-adding
        for f in old_list:
            self.add_function_to_list(f.text, f.start, f.end, f.accuracy, f.color)

    def function_toggled(self, function_id, check_box):
        if not check_box.isChecked():
            self.disabled_functions.append(function_id)
        elif function_id in self.disabled_functions:
            self.disabled_functions.remove(function_id)
        self.update_functions()

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
            color = self.color_box.currentText()
            if len(color) == 0:
                design.error_message('Incorrect color: ' + str(color))
                return

        # Calculating
        plotter.add_function(expression, self.function_queue, x_values, color)
        plotter.draw(self.function_queue, self.axes)

        # Drawing stuff
        self.canvas.draw()
        self.canvas.flush_events()
        self.canvas.show()

        # Store
        func = plotter.Function(expression, start, end, accuracy, color)
        self.function_list.append(func)

        index = len(self.function_list) - 1
        self.function_column[index].setText(expression)
        if not self.function_column[index].isChecked():
            self.function_column[index].setChecked(True)
        self.function_column[index].setEnabled(True)

        self.function_edit_buttons[index].setVisible(True)
        self.function_edit_buttons[index].setEnabled(True)

        self.function_remove_buttons[index].setVisible(True)
        self.function_remove_buttons[index].setEnabled(True)

    def update_functions(self):
        plotter.clear_all(self.function_queue, self.axes)
        self.canvas.draw()

        for i in range(len(self.function_list)):
            function = self.function_list[i]

            if i not in self.disabled_functions:
                x_values = plotter.calculate_x_values(function.start, function.end, function.accuracy)
                plotter.add_function(function.text, self.function_queue, x_values, function.color)
                plotter.draw(self.function_queue, self.axes)

                # Drawing stuff
                self.canvas.draw()
                self.canvas.flush_events()
                self.canvas.show()

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
        color = self.color_box.currentText()
        if len(color) == 0:
            design.error_message('Incorrect color: ' + str(color))
            return

        # Clearing
        old_list = self.function_list.copy()
        self.clear_click()

        # Re-adding
        count = 0
        for f in old_list:
            if count == self.selected_function:
                self.add_function_to_list(function, start, end, accuracy, color)
            else:
                self.add_function_to_list(f.text, f.start, f.end, f.accuracy, f.color)
            count += 1

    # Asks file path and loads from it function list
    def load_functions(self):
        name = QtWidgets.QFileDialog.getOpenFileName(filter='Text files (*.json)')
        if name[0] == '':
            return

        self.clear_click()
        self.disabled_functions.clear()

        with open(name[0], 'r') as in_file:
            data = json.load(in_file)
            if 'functions' in data:
                for func in data['functions']:
                    expression = func['expression']
                    start = int(func['x_start'])
                    end = int(func['x_end'])
                    accuracy = int(func['accuracy'])
                    color = func['color']
                    self.add_function_to_list(expression, start, end, accuracy, color)
            if 'disabled' in data:
                for id in data['disabled']:
                    self.disabled_functions.append(id)

    # Asks file path and saves function list there
    def save_functions(self):
        name = QtWidgets.QFileDialog.getSaveFileName()
        if name[0] == '':
            return

        data = {}
        data['functions'] = []
        for func in self.function_list:
            data['functions'].append({
                'expression': str(func.text),
                'x_start': str(func.start),
                'x_end': str(func.end),
                'accuracy': str(func.accuracy),
                'color': str(func.color)
            })
        for id in self.disabled_functions:
            data['disabled'].append({
                'id': str(id)
            })

        with open(name[0], 'w') as out_file:
            json.dump(data, out_file)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()
    sys.exit(app.exec_())
