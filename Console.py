from PyQt5.QtWidgets import QWidget, QLabel


class Console(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 200)
        self.label = QLabel(self)
        self.label.setGeometry(10, 0, self.width() - 10, self.height())
        self.setWindowTitle("Console")

    def GetAnswer(self, Answer):
        text = self.label.text()
        self.label.setText(text + "\n" + Answer)
