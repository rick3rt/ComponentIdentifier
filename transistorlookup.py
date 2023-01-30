from os import listdir
from os.path import isfile, join, splitext
from PyQt5.QtWidgets import (QApplication, QTabWidget, QGridLayout, QLineEdit,
                             QWidget, QLabel, QPushButton, QStyleFactory, QCompleter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

image_folder = 'resource/transistors'
transistor_files = [f for f in listdir(image_folder) if isfile(join(image_folder, f))]
transistor_names = [splitext(f)[0] for f in transistor_files]

print(transistor_names)


class TransistorLookup(QWidget):
    def __init__(self, parent):
        super(TransistorLookup, self).__init__()
        layout = QGridLayout()
        self.parent = parent
        # auto complete options
        completer = QCompleter(transistor_names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        # create line edit and add auto complete
        lbl_transistor_number = QLabel("&Transistor? ")
        self.edit_transistor_number = QLineEdit()
        self.edit_transistor_number.setCompleter(completer)
        lbl_transistor_number.setBuddy(self.edit_transistor_number)
        layout.addWidget(lbl_transistor_number, 0, 0)
        layout.addWidget(self.edit_transistor_number, 0, 1)

        self.image_lbl = QLabel()
        layout.addWidget(self.image_lbl, 2, 0, 1, 2)

        self.edit_transistor_number.returnPressed.connect(self.lookup_transistor)

        self.setLayout(layout)

    def lookup_transistor(self):
        transistor_number = self.edit_transistor_number.text()
        print(transistor_number)
        # if transistor_number == self.current_chip:
        # return  # no need for update
        if transistor_number in transistor_names:
            image_path = join(
                image_folder, transistor_files[transistor_names.index(transistor_number)])
        else:
            image_path = join(image_folder, '..', "not_found.jpg")

        # get images from chips
        pixmap = QPixmap(image_path)

        # scale based on parent window size
        width = self.parent.frameGeometry().width()
        height = self.parent.frameGeometry().height()
        pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio | Qt.SmoothTransformation)
        
        self.image_lbl.setPixmap(pixmap)
        # self.current_chip = transistor_number


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    window = TransistorLookup()
    window.show()
    sys.exit(app.exec())
