from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QToolTip

import plotter2d as plotter


class MathField(QtWidgets.QLineEdit):
    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return and not plotter.validate_text(self.text()):
            error_message('Incorrect function')
            return False
        else:
            return QtWidgets.QLineEdit.event(self, event)


class GuiMainWindow(object):

    def setup(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(820, 642)
        main_window.setMinimumSize(QtCore.QSize(820, 642))

        central_widget = QtWidgets.QWidget(main_window)
        central_widget.setObjectName("central_widget")
        self.fill_central_widget(central_widget)
        main_window.setCentralWidget(central_widget)

        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 820, 26))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.translate(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def fill_central_widget(self, central_widget):
        # PLOTTER
        horizontal_layout_1 = QtWidgets.QHBoxLayout(central_widget)
        horizontal_layout_1.setObjectName("horizontal_layout_1")

        vertical_layout_1 = QtWidgets.QVBoxLayout()
        vertical_layout_1.setObjectName("vertical_layout_1")

        self.widget = QtWidgets.QWidget(central_widget)
        self.widget.setMinimumSize(QtCore.QSize(600, 501))
        self.widget.setObjectName("widget")

        vertical_layout_1.addWidget(self.widget)
        # PLOTTER END

        # PUSHING
        horizontal_layout_2 = QtWidgets.QHBoxLayout()
        horizontal_layout_2.setObjectName("horizontal_layout_2")

        self.input_line = MathField(central_widget)
        self.input_line.setMinimumSize(QtCore.QSize(0, 30))
        self.input_line.setObjectName("input_line")
        horizontal_layout_2.addWidget(self.input_line)

        self.push_button = QtWidgets.QPushButton(central_widget)
        self.push_button.setObjectName("pushButton")
        self.push_button.setAutoDefault(True)
        horizontal_layout_2.addWidget(self.push_button)

        vertical_layout_1.addLayout(horizontal_layout_2)
        # PUSHING END

        # PLOT SETTINGS
        horizontal_layout_3 = QtWidgets.QHBoxLayout()
        horizontal_layout_3.setObjectName("horizontal_layout_3")

        start_line_label = QtWidgets.QLabel()
        start_line_label.setText('X start: ')
        start_line_label.setObjectName('start_line_label')
        start_line_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        horizontal_layout_3.addWidget(start_line_label)

        self.start_line = QtWidgets.QLineEdit(central_widget)
        self.start_line.setMinimumSize(QtCore.QSize(0, 30))
        self.start_line.setMaximumSize(QtCore.QSize(100, 30))
        self.start_line.setObjectName('start_line')
        horizontal_layout_3.addWidget(self.start_line)

        end_line_label = QtWidgets.QLabel()
        end_line_label.setText('X end: ')
        end_line_label.setObjectName('end_line_label')
        end_line_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        horizontal_layout_3.addWidget(end_line_label)

        self.end_line = QtWidgets.QLineEdit(central_widget)
        self.end_line.setMinimumSize(QtCore.QSize(0, 30))
        self.end_line.setMaximumSize(QtCore.QSize(100, 30))
        self.end_line.setObjectName('end_line')
        horizontal_layout_3.addWidget(self.end_line)

        accuracy_label = QtWidgets.QLabel()
        accuracy_label.setText('Amount of points: ')
        accuracy_label.setObjectName('accuracy_label')
        accuracy_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        horizontal_layout_3.addWidget(accuracy_label)

        self.accuracy_line = QtWidgets.QLineEdit(central_widget)
        self.accuracy_line.setMinimumSize(QtCore.QSize(0, 30))
        self.accuracy_line.setMaximumSize(QtCore.QSize(100, 30))
        self.accuracy_line.setObjectName('accuracy_line')
        horizontal_layout_3.addWidget(self.accuracy_line)

        color_label = QtWidgets.QLabel()
        color_label.setText('Color: ')
        color_label.setObjectName('color_label')
        color_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        horizontal_layout_3.addWidget(color_label)

        self.color_line = QtWidgets.QLineEdit(central_widget)
        self.color_line.setMinimumSize(QtCore.QSize(0, 30))
        self.color_line.setMaximumSize(QtCore.QSize(100, 30))
        self.color_line.setObjectName('color_line')
        horizontal_layout_3.addWidget(self.color_line)

        self.reset_input_lines()

        vertical_layout_1.addLayout(horizontal_layout_3)
        horizontal_layout_1.addLayout(vertical_layout_1)

        vertical_layout_2 = QtWidgets.QVBoxLayout()
        vertical_layout_2.setObjectName("vertical_layout_2")
        # PLOT SETTINGS END

        # SAVING & LOADING
        horizontal_layout_3 = QtWidgets.QHBoxLayout()
        horizontal_layout_3.setObjectName("horizontal_layout_3")

        self.save_button = QtWidgets.QToolButton(central_widget)
        self.save_button.setObjectName('save_button')
        horizontal_layout_3.addWidget(self.save_button)

        self.load_button = QtWidgets.QToolButton(central_widget)
        self.load_button.setObjectName('load_button')
        horizontal_layout_3.addWidget(self.load_button)

        vertical_layout_2.addLayout(horizontal_layout_3)

        # FUNCTIONS LIST
        self.function_column = QtWidgets.QTextEdit(central_widget)
        self.function_column.setMaximumSize(QtCore.QSize(400, 16777215))
        self.function_column.setObjectName("function_column")
        self.function_column.setReadOnly(True)
        vertical_layout_2.addWidget(self.function_column)

        # CLEAR BUTTON
        self.clear_button = QtWidgets.QToolButton(central_widget)
        self.clear_button.setObjectName("clear_button")
        vertical_layout_2.addWidget(self.clear_button)

        # SELECTING STUFF
        horizontal_layout_4 = QtWidgets.QHBoxLayout()
        horizontal_layout_4.setObjectName("horizontal_layout_4")

        select_label = QtWidgets.QLabel()
        select_label.setText('Function ID: ')
        select_label.setObjectName('select_label')
        select_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        horizontal_layout_4.addWidget(select_label)

        self.select_line = QtWidgets.QLineEdit(central_widget)
        self.select_line.setMinimumSize(QtCore.QSize(0, 20))
        self.select_line.setMaximumSize(QtCore.QSize(50, 20))
        self.select_line.setObjectName('select_line')
        horizontal_layout_4.addWidget(self.select_line)

        self.select_button = QtWidgets.QToolButton(central_widget)
        self.select_button.setObjectName("select_button")
        horizontal_layout_4.addWidget(self.select_button)

        vertical_layout_2.addLayout(horizontal_layout_4)

        horizontal_layout_4 = QtWidgets.QHBoxLayout()
        horizontal_layout_4.setObjectName("horizontal_layout_5")

        self.selected_label = QtWidgets.QLabel()
        self.selected_label.setText('Selected: None')
        self.selected_label.setObjectName('selected_label')
        self.selected_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        horizontal_layout_4.addWidget(self.selected_label)

        self.deselect_button = QtWidgets.QToolButton(central_widget)
        self.deselect_button.setObjectName("deselect_button")
        horizontal_layout_4.addWidget(self.deselect_button)

        vertical_layout_2.addLayout(horizontal_layout_4)
        horizontal_layout_1.addLayout(vertical_layout_2)

        self.function_seleted(None)
        # SELECTING STUFF END

    def create_input_with_label(self, central_widget, layout, label_text):
        label = QtWidgets.QLabel()
        label.setText(label_text)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)

        line = QtWidgets.QLineEdit(central_widget)
        line.setMinimumSize(QtCore.QSize(0, 30))
        line.setMaximumSize(QtCore.QSize(100, 30))
        layout.addWidget(line)
        return line

    def translate(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "Graphing Function Calculator"))
        self.push_button.setText(_translate("MainWindow", "Plot"))
        self.clear_button.setText(_translate("MainWindow", "Clear"))
        self.save_button.setText(_translate("MainWindow", 'Save'))
        self.load_button.setText(_translate("MainWindow", "Load"))
        self.select_button.setText(_translate('MainWindow', 'Select'))
        self.deselect_button.setText(_translate('MainWindow', 'Deselect'))

    def reset_input_lines(self):
        self.input_line.clear()
        self.start_line.setText('0')
        self.end_line.setText('10')
        self.accuracy_line.setText('50')
        self.color_line.setText('red')

    def function_seleted(self, function_id):
        if function_id is None:
            self.select_line.clear()
            self.selected_label.setText('Selected: None')
            self.deselect_button.setEnabled(False)
        else:
            self.select_line.setText(str(function_id))
            self.selected_label.setText('Selected: ' + str(function_id))
            self.deselect_button.setEnabled(True)


def error_message(text):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle('Error')
    msg.setText(text)
    msg.exec()
