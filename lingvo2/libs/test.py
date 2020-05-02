import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QPushButton, QLabel, QWidget, \
    QHBoxLayout, QSizePolicy, QSpacerItem, QComboBox, QGroupBox, QRadioButton
from libs.Spoiler import Spoiler

def fun(spoiler):
    if spoiler.isOpened():
        spoiler.close()
    else:
        spoiler.open()

app = QApplication(sys.argv)
w = QMainWindow()
cw = QWidget()
mainLayout = QHBoxLayout()
cw.setLayout(mainLayout)

gridLayout = QGridLayout()

spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
gridLayout.addItem(spacerItem1, 0, 0, 1, 1)

pushButton1 = QPushButton()
pushButton1.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
pushButton1.setText("")
gridLayout.addWidget(pushButton1, 0, 1, 1, 1)

label1 = QLabel()
label1.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
label1.setObjectName("")
gridLayout.addWidget(label1, 0, 2, 1, 1)

spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
gridLayout.addItem(spacerItem2, 0, 3, 1, 1)

label2 = QLabel()
label2.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
label2.setObjectName("")
gridLayout.addWidget(label2, 0, 4, 1, 1)

pushButton2 = QPushButton()
pushButton2.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
pushButton2.setText("")
gridLayout.addWidget(pushButton2, 0, 5, 1, 1)

spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
gridLayout.addItem(spacerItem3, 0, 6, 1, 1)

groupBox = QGroupBox()
groupBox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
verticalLayout = QVBoxLayout(groupBox)

radioButton1 = QRadioButton(groupBox)
radioButton1.setText("Name")
verticalLayout.addWidget(radioButton1)

radioButton2 = QRadioButton(groupBox)
radioButton1.setText("Cost")
verticalLayout.addWidget(radioButton2)

gridLayout.addWidget(groupBox, 1, 1, 1, 2, Qt.AlignTop)

comboBox = QComboBox()
comboBox.addItem("Dokkan Belga")
comboBox.addItem("Eamon Company")
gridLayout.addWidget(comboBox, 1, 4, 1, 2, Qt.AlignTop)

btn = QPushButton("Click me")
btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
spoiler = Spoiler(Spoiler.Orientation.VERTICAL)
spoiler.setContentLayout(gridLayout)

mainLayout.addWidget(btn)
mainLayout.addWidget(spoiler)
# mainLayout.setAlignment(Qt.AlignRight)

btn.clicked.connect(lambda : fun(spoiler))

w.setCentralWidget(cw)
w.show()
sys.exit(app.exec_())
