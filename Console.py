from PyQt5.QtWidgets import QWidget, QLabel

class Console(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 200)
        self.label = QLabel(self)
        self.label.resize(self.width(), self.height())

    def GetAnswer(self, Answer):
        self.label.setText(Answer)



