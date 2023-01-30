from os import listdir
from os.path import isfile, join, splitext
from PyQt5.QtWidgets import (QApplication, QTabWidget, QGridLayout, QLineEdit,
                             QWidget, QLabel, QPushButton, QStyleFactory, QCompleter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

# chip_names = ['555', '556', 'TL072', 'TL074']
image_folder = 'resource/chips'
chip_files = [f for f in listdir(image_folder) if isfile(join(image_folder, f))]
chip_names = [splitext(f)[0] for f in chip_files]


class ChipLookup(QWidget):
    def __init__(self, parent=None):
        super(ChipLookup, self).__init__()
        layout = QGridLayout()
        # layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.parent = parent
        self.current_chip = None

        # auto complete options
        completer = QCompleter(chip_names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        # create line edit and add auto complete
        lbl_chipname = QLabel("&Chip Name? ")
        self.edit_chipname = QLineEdit()
        self.edit_chipname.setCompleter(completer)
        lbl_chipname.setBuddy(self.edit_chipname)
        layout.addWidget(lbl_chipname, 0, 0)
        layout.addWidget(self.edit_chipname, 0, 1)

        self.image_lbl = QLabel()
        layout.addWidget(self.image_lbl, 2, 0, 1, 2)

        self.edit_chipname.returnPressed.connect(self.lookup_chip)

        self.setLayout(layout)

    def lookup_chip(self):
        new_chip = self.edit_chipname.text()
        print(new_chip)
        if new_chip == self.current_chip:
            return  # no need for update
        if new_chip in chip_names:
            image_path = join(image_folder, chip_files[chip_names.index(new_chip)])
        else:
            image_path = join(image_folder, '..', "not_found.jpg")

        # get images from chips
        pixmap = QPixmap(image_path)

        # scale based on parent window size
        # if self.parent:
        #     width = self.parent.frameGeometry().width()
        #     height = self.parent.frameGeometry().height()
        # else:
        width = self.window().frameGeometry().width()
        height = self.window().frameGeometry().height()
        print(width, ", ", height)
        pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.image_lbl.setPixmap(pixmap)
        self.current_chip = new_chip


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    window = ChipLookup()
    window.show()
    sys.exit(app.exec())
