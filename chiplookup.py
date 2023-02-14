from os import listdir
from os.path import isfile, join, splitext
from PyQt5.QtWidgets import (QApplication, QTabWidget, QGridLayout, QLineEdit, QComboBox,
                             QWidget, QLabel, QPushButton, QStyleFactory, QCompleter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

image_folder = 'resource/chips'


class ChipLookup(QWidget):
    def __init__(self, parent=None):
        super(ChipLookup, self).__init__()
        layout = QGridLayout()
        # layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.parent = parent
        self.current_chip = None

        # get names and files
        self.chip_files = [f for f in listdir(
            image_folder) if isfile(join(image_folder, f))]
        self.chip_names = [splitext(f)[0] for f in self.chip_files]

        # auto complete options
        completer = QCompleter(self.chip_names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        # create line edit and add auto complete
        lbl_chipname = QLabel("&Chip Name? ")
        # self.edit_chipname = QLineEdit()
        # self.edit_chipname.setCompleter(completer)
        self.edit_chipname = QComboBox()
        self.edit_chipname.setEditable(True)
        self.edit_chipname.addItems(self.chip_names)

        lbl_chipname.setBuddy(self.edit_chipname)
        layout.addWidget(lbl_chipname, 0, 0)
        layout.addWidget(self.edit_chipname, 0, 1)

        self.image_lbl = QLabel()
        layout.addWidget(self.image_lbl, 2, 0, 1, 2)

        # self.edit_chipname.returnPressed.connect(self.lookup_chip)
        self.edit_chipname.editTextChanged.connect(self.lookup_chip)
        self.edit_chipname.currentIndexChanged.connect(self.lookup_chip)
        self.setLayout(layout)

        self.lookup_chip()

    def lookup_chip(self):
        # new_chip = self.edit_chipname.text()
        new_chip = self.edit_chipname.currentText()
        if new_chip == self.current_chip:
            return  # no need for update
        if new_chip in self.chip_names:
            image_path = join(
                image_folder, self.chip_files[self.chip_names.index(new_chip)])
        else:
            image_path = join(image_folder, '..', "not_found.jpg")

        # get images from chips
        pixmap = QPixmap(image_path)

        # scale based on parent window size
        # if self.parent:
        #     width = self.parent.frameGeometry().width()
        #     height = self.parent.frameGeometry().height()
        # else:
        #     width = self.window().frameGeometry().width()
        #     height = self.window().frameGeometry().height()
        width = 500
        height = 500
        pixmap = pixmap.scaled(
            width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.image_lbl.setPixmap(pixmap)
        self.current_chip = new_chip


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    window = ChipLookup()
    window.show()
    sys.exit(app.exec())
