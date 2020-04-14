import sys
from PyQt5.QtWidgets import QApplication

from gui import main as _main

def main():
    app = QApplication(sys.argv)
    main = _main.Main()
    main.show()
    # print(main.cardEditView.sides["front"].geometry())
    sys.exit(app.exec_())

main()


