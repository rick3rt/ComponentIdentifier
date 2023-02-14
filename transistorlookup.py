from os import listdir
from os.path import isfile, join, splitext
from PyQt5.QtWidgets import (QApplication, QTabWidget, QGridLayout, QLineEdit, QComboBox,
                             QWidget, QLabel, QPushButton, QStyleFactory, QCompleter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

image_folder = 'resource/transistors'


class TransistorLookup(QWidget):
    def __init__(self, parent):
        super(TransistorLookup, self).__init__()
        layout = QGridLayout()
        self.parent = parent

        # get names and files
        self.transistor_files = [f for f in listdir(
            image_folder) if isfile(join(image_folder, f))]
        self.transistor_names = [splitext(f)[0] for f in self.transistor_files]

        # auto complete options
        completer = QCompleter(self.transistor_names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        # create line edit and add auto complete
        lbl_transistor_number = QLabel("&Transistor? ")
        self.edit_transistor_number = QComboBox()
        self.edit_transistor_number.setEditable(True)
        self.edit_transistor_number.addItems(self.transistor_names)
        # self.edit_transistor_number = QLineEdit()
        # self.edit_transistor_number.setCompleter(completer)

        lbl_transistor_number.setBuddy(
            self.edit_transistor_number)  # set buddy for alt+T
        layout.addWidget(lbl_transistor_number, 0, 0)
        layout.addWidget(self.edit_transistor_number, 0, 1)

        self.image_lbl = QLabel()
        layout.addWidget(self.image_lbl, 2, 0, 1, 2)

        # self.edit_transistor_number.returnPressed.connect(
        #     self.lookup_transistor)

        self.edit_transistor_number.editTextChanged.connect(
            self.lookup_transistor)
        self.edit_transistor_number.currentIndexChanged.connect(
            self.lookup_transistor)

        self.setLayout(layout)

        self.lookup_transistor()

    def lookup_transistor(self):
        # transistor_number = self.edit_transistor_number.text()
        transistor_number = self.edit_transistor_number.currentText()
        # if transistor_number == self.current_chip:
        # return  # no need for update
        if transistor_number in self.transistor_names:
            image_path = join(
                image_folder, self.transistor_files[self.transistor_names.index(transistor_number)])
        else:
            image_path = join(image_folder, '..', "not_found.jpg")

        # get images from chips
        pixmap = QPixmap(image_path)

        # scale based on parent window size
        # width = self.parent.frameGeometry().width()
        # height = self.parent.frameGeometry().height()
        width = 500
        height = 500
        pixmap = pixmap.scaled(
            width, height, Qt.KeepAspectRatio | Qt.SmoothTransformation)

        self.image_lbl.setPixmap(pixmap)
        # self.current_chip = transistor_number


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    window = TransistorLookup()
    window.show()
    sys.exit(app.exec())
