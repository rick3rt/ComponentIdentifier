#!/usr/bin/env python3

from functools import partial
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit, QMainWindow,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget)
from resistormenu import ResistorMenu, ResistorTab
from transistorlookup import TransistorLookup
from chiplookup import ChipLookup


class ComponentIdentifier(QMainWindow):
    def __init__(self, parent=None):
        super(ComponentIdentifier, self).__init__(parent)


        self.main_tabs = QTabWidget()

        self.create_capacitor_tab()
        self.create_resistor_tab()
        self.create_transistor_tab()
        self.create_chip_tab()
        # self.createBottomLeftTabWidget()
        # self.createBottomRightGroupBox()

        # styleComboBox.textActivated.connect(self.changeStyle)
        # self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        # disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        # disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        # disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        # disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

        # main_layout = QGridLayout()
        # main_layout.addWidget(self.capacitor_box, 0, 0)
        # main_layout.addWidget(self.resistor_tabs, 0, 1)
        # main_layout.addWidget(self.bottomLeftTabWidget, 1, 0)
        # main_layout.addWidget(self.bottomRightGroupBox, 1, 1)
        # main_layout.setRowStretch(1, 1)
        # main_layout.setRowStretch(2, 1)
        # main_layout.setColumnStretch(0, 1)
        # main_layout.setColumnStretch(1, 1)
        # self.main_widget = QWidget(self)
        # self.main_widget.setLayout(main_layout)
        # self.setCentralWidget(self.main_widget)

        self.setCentralWidget(self.main_tabs)

        self.setWindowTitle("ComponentIdentifier")
        self.setWindowIcon(QIcon('resource/icon.png'))

        QApplication.setStyle(QStyleFactory.create('Fusion'))

    def create_capacitor_tab(self):
        # self.capacitor_box = QGroupBox("Capacitors")
        self.capacitor_tab = QWidget()
        self.main_tabs.addTab(self.capacitor_tab, "&Capacitors")

        lbl_cap_code = QLabel("Code: ")
        edit_cap_code = QSpinBox()
        edit_cap_code.valueChanged.connect(self.calculate_capacitor_value)
        edit_cap_code.setMaximum(999)
        edit_cap_code.setMinimum(0)

        self.disp_micro_farad = QLineEdit()
        self.disp_nano_farad = QLineEdit()
        self.disp_pico_farad = QLineEdit()
        self.disp_micro_farad.setReadOnly(True)
        self.disp_nano_farad.setReadOnly(True)
        self.disp_pico_farad.setReadOnly(True)

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(lbl_cap_code, 0, 0)
        layout.addWidget(edit_cap_code, 0, 1)

        layout.addWidget(self.disp_micro_farad, 2, 1)
        layout.addWidget(self.disp_nano_farad, 3, 1)
        layout.addWidget(self.disp_pico_farad, 4, 1)

        layout.addWidget(QLabel("μF"), 2, 2)
        layout.addWidget(QLabel("nF"), 3, 2)
        layout.addWidget(QLabel("pF"), 4, 2)

        self.capacitor_tab.setLayout(layout)

    def calculate_capacitor_value(self, value):
        digits = [int(d) for d in str(value)]
        cap_pf = 0
        if len(digits) == 3:
            cap_pf = (digits[0] * 10 + digits[1]) * (10 ** digits[2])
        else:
            cap_pf = value
        self.disp_pico_farad.setText(str(round(cap_pf, 3)))
        self.disp_nano_farad.setText(str(round(cap_pf * 1e-3, 3)))
        self.disp_micro_farad.setText(str(round(cap_pf * 1e-6, 3)))

    def create_resistor_tab(self):
        self.resistor_tabs = ResistorMenu()
        self.main_tabs.addTab(self.resistor_tabs, "&Resistors")

    def create_transistor_tab(self):
        self.transistor_tabs = TransistorLookup(self)
        self.main_tabs.addTab(self.transistor_tabs, "&Transistors")

    def create_chip_tab(self):
        self.chip_tabs = ChipLookup(self)
        self.main_tabs.addTab(self.chip_tabs, "&ICs")


if __name__ == '__main__':
    import sys
    import os

    # change dir
    abspath = os.path.realpath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # run app
    app = QApplication(sys.argv)
    gallery = ComponentIdentifier()
    gallery.show()
    sys.exit(app.exec())
