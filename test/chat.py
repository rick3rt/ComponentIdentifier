from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

app = QApplication([])
window = QWidget()
layout = QGridLayout()
layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

for i in range(3):
    for j in range(3):
        label = QLabel("Label" + str(i) + str(j))
        layout.addWidget(label, i, j)  # , Qt.AlignTop | Qt.AlignLeft)

window.setLayout(layout)
window.show()
app.exec_()
