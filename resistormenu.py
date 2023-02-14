
"""
Inspired by: https://www.allaboutcircuits.com/tools/resistor-color-code-calculator/
"""
# from PyQt5.QtCore import Qt
from functools import partial
from PyQt5.QtWidgets import (QApplication, QTabWidget, QGridLayout, QLineEdit,
                             QWidget, QLabel, QPushButton, QStyleFactory)
from PyQt5.QtCore import Qt


resistor_band_colors = {
    "black": "rgb(38, 35, 35)",
    "red": "rgb(230, 5, 20)",
    "brown": "rgb(125 , 67  ,2 )",
    "orange": "rgb(242, 107, 49)",
    "yellow": "rgb(242, 234, 124)",
    "green": "rgb(60, 176, 87)",
    "blue": "rgb(4, 131, 222)",
    "violet": "rgb(157, 44, 163)",
    "gray": "rgb(89, 87, 89)",
    "white": "rgb(255, 255, 255)",
    "gold": "rgb(212, 175, 55)",
    "silver": "rgb(192, 192, 192)",
}


column_list_4bands = ["D1", "D2", "Mult", "Tol"]
column_list_5bands = ["D1", "D2", "D3", "Mult", "Tol"]
column_list_6bands = ["D1", "D2", "D3", "Mult", "Tol", "Tempco"]


color_list_4bands = [
    [None, "Brown", "Red", "Orange", "Yellow",
        "Green", "Blue", "Violet", "Gray", "White"],
    ["Black", "Brown", "Red", "Orange", "Yellow",
        "Green", "Blue", "Violet", "Gray", "White"],
    ["Black", "Brown", "Red", "Orange", "Yellow", "Green",
        "Blue", "Violet", "Gray", "White", "Gold", "Silver"],
    [None, "Brown", "Red", "Orange", "Yellow", "Green",
        "Blue", "Violet", "Gray", None, "Gold", "Silver"]
]

color_list_5bands = [
    [None, "Brown", "Red", "Orange", "Yellow",
        "Green", "Blue", "Violet", "Gray", "White"],
    ["Black", "Brown", "Red", "Orange", "Yellow",
        "Green", "Blue", "Violet", "Gray", "White"],
    ["Black", "Brown", "Red", "Orange", "Yellow",
        "Green", "Blue", "Violet", "Gray", "White"],
    ["Black", "Brown", "Red", "Orange", "Yellow", "Green",
        "Blue", "Violet", "Gray", "White", "Gold", "Silver"],
    [None, "Brown", "Red", "Orange", "Yellow", "Green",
        "Blue", "Violet", "Gray", None, "Gold", "Silver"]
]

color_list_6bands = [
    [None, "Brown", "Red", "Orange", "Yellow",
        "Green", "Blue", "Violet", "Gray", "White"],
    ["Black", "Brown", "Red", "Orange", "Yellow",
        "Green", "Blue", "Violet", "Gray", "White"],
    ["Black", "Brown", "Red", "Orange", "Yellow",
        "Green", "Blue", "Violet", "Gray", "White"],
    ["Black", "Brown", "Red", "Orange", "Yellow", "Green",
        "Blue", "Violet", "Gray", "White", "Gold", "Silver"],
    ["Black", "Brown", "Red", "Orange", "Yellow", "Green",
        "Blue", "Violet", "Gray", "White", "Gold", "Silver"],
    [None, "Brown", "Red", "Orange", "Yellow", None,
        "Blue", "Violet"]
]

tolerance_list = [None, 1, 2, 3, 4, 0.5, 0.25, 0.10,
                  0.05, None, 5, 10]  # convert row index to tolerance


def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


class ResistorTab(QWidget):
    def __init__(self, num_bands):
        super(ResistorTab, self).__init__()
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        col_width = 60

        self.num_bands = num_bands
        self.active_buttons = [None] * num_bands
        # self.active_colors = [None] * num_bands
        self.active_rows = [1] * num_bands

        if num_bands == 4:
            column_list = column_list_4bands
            color_list = color_list_4bands
        elif num_bands == 5:
            column_list = column_list_5bands
            color_list = color_list_5bands
        elif num_bands == 6:
            column_list = column_list_6bands
            color_list = color_list_6bands

        self.disp_resistor_value = QLineEdit("")
        self.disp_resistor_value.setFixedWidth(col_width)
        self.disp_resistor_value.setReadOnly(True)
        self.disp_resistor_tolerance = QLabel("")

        for col_idx, col_str in enumerate(column_list):
            lbl = QLabel(col_str)
            lbl.setStyleSheet("font-weight: bold")
            layout.addWidget(lbl, 0, col_idx, Qt.AlignCenter)

        self.buttons = []

        for col_idx, column_list in enumerate(color_list):
            self.buttons.append([])
            for row_idx, row_color in enumerate(column_list):
                if row_color:
                    if row_idx == 0:
                        x_color = 'white'
                    else:
                        x_color = 'black'
                    btn = QPushButton()
                    btn.setStyleSheet("font-weight: bold; background-color: " +
                                      resistor_band_colors[row_color.lower()] + f"; color: {x_color}")
                    btn.setFixedWidth(col_width)
                    btn.setFixedHeight(int(col_width / 2))
                    layout.addWidget(btn, row_idx + 1, col_idx)
                    btn.clicked.connect(
                        partial(self.set_active_button, col_idx, row_idx))
                    self.buttons[col_idx].append(btn)
                else:
                    # pass
                    self.buttons[col_idx].append(None)

                if row_idx == 1:
                    self.set_active_button(col_idx, row_idx)

        btn_reset = QPushButton("Reset")
        btn_reset.clicked.connect(self.reset_colors)

        layout.addWidget(QLabel("Resistance: "), 13, 0)
        layout.addWidget(QLabel("Resistance: "), 13, 0)
        layout.addWidget(self.disp_resistor_value, 13, 1)
        layout.addWidget(QLabel("Ohm"), 13, 2)
        layout.addWidget(self.disp_resistor_tolerance, 13, 3)
        layout.addWidget(btn_reset, 12, 0)

        self.setLayout(layout)

    def set_active_button(self, col_idx, row_idx):
        btn = self.buttons[col_idx][row_idx]
        if self.active_buttons[col_idx]:  # can be None in beginning
            self.active_buttons[col_idx].setText("")
        self.active_buttons[col_idx] = btn
        btn.setText("X")  # set new text last
        self.active_rows[col_idx] = row_idx
        self.calculate_resistance()  # and update the resistance value

    def reset_colors(self):
        for i, _ in enumerate(self.active_rows):
            self.active_rows[i] = 1
            self.set_active_button(i, 1)

    def calculate_resistance(self):
        rval = 0
        tidx = 0

        # check if no nones
        if None in self.active_rows:
            return

        if self.num_bands == 4:
            rval = self.active_rows[0] * 10 + self.active_rows[1]
            if self.active_rows[2] < 10:
                rval *= 10**self.active_rows[2]
            else:
                rval *= 10**(-1 * self.active_rows[2] - 9)
            tidx = self.active_rows[3]

        elif self.num_bands >= 5:
            rval = self.active_rows[0] * 100 + \
                self.active_rows[1] * 10 + self.active_rows[2]
            if self.active_rows[3] < 10:
                rval *= 10**self.active_rows[3]
            else:
                rval *= 10**(-1 * self.active_rows[3] - 9)
            tidx = self.active_rows[4]

        tval = tolerance_list[tidx]

        resistance_str = human_format(round(rval, 3))
        tolerance_str = str(round(tval, 2)) + "%"
        self.disp_resistor_value.setText(resistance_str)
        self.disp_resistor_tolerance.setText(tolerance_str)


class ResistorMenu(QTabWidget):
    def __init__(self):
        super(ResistorMenu, self).__init__()

        self.addTab(ResistorTab(4), "&4 Bands")
        self.addTab(ResistorTab(5), "&5 Bands")
        self.addTab(ResistorTab(6), "&6 Bands")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    window = ResistorMenu()
    window.show()
    sys.exit(app.exec())
